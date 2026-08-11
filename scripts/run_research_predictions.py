"""Run frozen OCR profiles in guarded calibration or publication mode."""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import ocr_bench  # noqa: F401 -- import registers adapters
from ocr_bench import registry
from ocr_bench.prediction import (
    PredictionSchemaError,
    load_prediction,
    prediction_path,
    save_prediction,
)
from ocr_bench.preflight import (
    CACHE_IDENTITY_KEY,
    DatasetDocument,
    PreflightContext,
    PreflightError,
    VerifiedDataset,
    build_cache_identity,
    build_run_manifest,
    collect_dependency_versions,
    collect_git_metadata,
    collect_system_metadata,
    publication_preflight,
    verify_cached_identity,
    verify_dataset_manifest,
    verify_fingerprint,
    verify_manifest_unchanged,
    verify_profile_selection,
)
from ocr_bench.profiles import EngineProfile, ProfileConfigError, load_profile_catalog
from ocr_bench.types import OcrResult

ROOT = Path(__file__).resolve().parent.parent
PROFILE_CATALOG = ROOT / "configs" / "profiles.json"
CALIBRATION_DATASET_MANIFEST = ROOT / "datasets" / "calibration-manifest.json"
PUBLICATION_DATASET_MANIFEST = ROOT / "datasets" / "manifest.json"
Mode = Literal["calibration", "publication"]


def _split_csv(value: str | None) -> list[str]:
    return [] if value is None else [part.strip() for part in value.split(",") if part.strip()]


def discover_documents(
    manifest_path: Path,
    repo_root: Path,
    *,
    limit: int | None = None,
    only: str | None = None,
    verified_dataset: VerifiedDataset | None = None,
) -> list[DatasetDocument]:
    """Select only verified rows from the supplied dataset manifest."""
    verified = verified_dataset or verify_dataset_manifest(manifest_path, repo_root)
    docs = list(verified)
    if only:
        requested = set(_split_csv(only))
        by_stem = {doc.doc_id: doc for doc in docs}
        missing = sorted(requested - set(by_stem))
        if missing:
            raise PreflightError(f"--only không có trong dataset: {', '.join(missing)}")
        docs = [by_stem[name] for name in sorted(requested)]
    if limit is not None:
        if limit < 1:
            raise PreflightError("--limit phải lớn hơn 0")
        docs = docs[:limit]
    if not docs:
        raise PreflightError("dataset manifest không trỏ tới PDF nào tồn tại")
    return docs


def attach_cache_identity(
    result: OcrResult, identity: Mapping[str, str]
) -> OcrResult:
    """Persist publication cache provenance under a secret-safe fingerprint key."""
    fingerprint = dict(result.config_fingerprint)
    fingerprint[CACHE_IDENTITY_KEY] = dict(identity)
    fingerprint["profile_config_sha256"] = identity["profile_config_sha256"]
    return dataclasses.replace(result, config_fingerprint=fingerprint)


def configure_process_hardware(hardware: Literal["cpu", "gpu"]) -> None:
    """Set process-wide hardware intent before importing/constructing an engine."""
    previous = os.environ.get("OCR_BENCH_HARDWARE")
    if hardware == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    elif previous == "cpu" and os.environ.get("CUDA_VISIBLE_DEVICES") == "":
        os.environ.pop("CUDA_VISIBLE_DEVICES", None)
    os.environ["OCR_BENCH_HARDWARE"] = hardware


def _configure_adapter_hardware(
    profile: EngineProfile,
    adapter: Any,
    hardware: Literal["cpu", "gpu"],
    mode: Mode,
) -> None:
    configure = getattr(adapter, "configure_hardware", None)
    if not callable(configure):
        if mode == "publication":
            raise PreflightError(
                f"{profile.name}: publication adapter thiếu configure_hardware(hardware)"
            )
        return
    resolved = configure(hardware)
    if resolved != hardware:
        raise PreflightError(
            f"{profile.name}: configure_hardware({hardware!r}) trả device={resolved!r}"
        )
    fingerprint = adapter.config_fingerprint()
    for key in ("hardware", "device"):
        claimed = fingerprint.get(key)
        if claimed is not None and claimed != hardware:
            raise PreflightError(
                f"{profile.name}: adapter fingerprint {key}={claimed!r}, cần {hardware!r}"
            )


def _normalize_profile_identity(
    result: OcrResult,
    profile: EngineProfile,
    *,
    doc: Path,
    doc_id: str,
    engine_version: str,
) -> OcrResult:
    if result.engine != profile.name:
        raise PreflightError(
            f"{doc}: adapter trả engine={result.engine!r}, cần {profile.name!r}"
        )
    if result.doc_id not in {doc_id, doc.stem}:
        raise PreflightError(
            f"{doc}: adapter trả doc_id={result.doc_id!r}, cần {doc_id!r}"
        )
    if result.engine_version != engine_version:
        raise PreflightError(
            f"{profile.name}/{doc.stem}: result version={result.engine_version!r}, "
            f"adapter version={engine_version!r}"
        )
    return dataclasses.replace(
        result,
        doc_id=doc_id,
        engine_family=profile.family,
        profile=profile.profile,
    )


def _verify_cached_result(
    cached: OcrResult,
    profile: EngineProfile,
    *,
    doc: Path,
    doc_id: str,
    engine_version: str,
) -> None:
    """Verify prediction payload identity independently of its embedded cache key."""
    expected = {
        "engine": profile.name,
        "engine_family": profile.family,
        "profile": profile.profile,
        "doc_id": doc_id,
        "engine_version": engine_version,
    }
    for field, expected_value in expected.items():
        actual_value = getattr(cached, field)
        if actual_value != expected_value:
            raise PreflightError(
                f"{profile.name}/{doc_id}: cached {field}={actual_value!r}, "
                f"cần {expected_value!r}"
            )
    verify_fingerprint(profile, cached.config_fingerprint)


def _verify_result_hardware(
    profile: EngineProfile,
    result: OcrResult,
    hardware: Literal["cpu", "gpu"],
    *,
    require_recorded: bool = False,
) -> None:
    for key in ("hardware", "device"):
        claimed = result.config_fingerprint.get(key)
        if claimed is None and require_recorded:
            raise PreflightError(
                f"{profile.name}: result fingerprint thiếu {key}={hardware!r}"
            )
        if claimed is not None and claimed != hardware:
            raise PreflightError(
                f"{profile.name}: result fingerprint {key}={claimed!r}, cần {hardware!r}"
            )


def _verify_publication_perf(profile: EngineProfile, result: OcrResult) -> None:
    missing = [
        field
        for field in ("seconds", "peak_rss_mb", "rss_scope")
        if getattr(result, field) is None
    ]
    if missing:
        raise PreflightError(
            f"{profile.name}/{result.doc_id}: publication thiếu perf {', '.join(missing)}"
        )


def run_profile_predictions(
    profile: EngineProfile,
    adapter: Any,
    docs: Sequence[Path | DatasetDocument],
    output_root: Path,
    *,
    hardware: Literal["cpu", "gpu"],
    mode: Mode,
    refresh: bool = False,
    dataset_manifest: Path | None = None,
    dataset_manifest_sha256: str | None = None,
) -> list[OcrResult]:
    """Run/resume one profile; publication cache drift is always fatal."""
    if mode == "publication" and refresh:
        raise PreflightError("publication không cho phép refresh cache")
    if (dataset_manifest is None) != (dataset_manifest_sha256 is None):
        raise PreflightError("dataset manifest path/hash phải được cung cấp cùng nhau")
    _configure_adapter_hardware(profile, adapter, hardware, mode)
    engine_version = adapter.version()
    verify_fingerprint(profile, adapter.config_fingerprint())
    results: list[OcrResult] = []
    for item in docs:
        if dataset_manifest is not None and dataset_manifest_sha256 is not None:
            verify_manifest_unchanged(dataset_manifest, dataset_manifest_sha256)
        if isinstance(item, DatasetDocument):
            doc = item.path
            doc_id = item.doc_id
            pdf_sha256 = item.pdf_sha256
        else:
            doc = Path(item)
            doc_id = doc.stem
            pdf_sha256 = None
        expected = build_cache_identity(
            doc,
            profile,
            engine_version=engine_version,
            hardware=hardware,
            doc_id=doc_id,
            pdf_sha256=pdf_sha256,
        )
        path = prediction_path(output_root, profile.name, doc_id)
        if path.is_file() and not refresh:
            try:
                cached = load_prediction(path)
                _verify_cached_result(
                    cached,
                    profile,
                    doc=doc,
                    doc_id=doc_id,
                    engine_version=engine_version,
                )
                verify_cached_identity(profile, cached.config_fingerprint, expected)
                _verify_result_hardware(
                    profile,
                    cached,
                    hardware,
                    require_recorded=mode == "publication",
                )
                if mode == "publication":
                    _verify_publication_perf(profile, cached)
            except (PredictionSchemaError, PreflightError, OSError, UnicodeError) as exc:
                if mode == "publication":
                    if isinstance(exc, PreflightError):
                        raise
                    raise PreflightError(
                        f"{path}: publication cache không hợp lệ: {exc}"
                    ) from None
            else:
                results.append(cached)
                continue
        result = adapter.execute(doc)
        result = _normalize_profile_identity(
            result,
            profile,
            doc=doc,
            doc_id=doc_id,
            engine_version=engine_version,
        )
        verify_fingerprint(profile, result.config_fingerprint)
        _verify_result_hardware(
            profile,
            result,
            hardware,
            require_recorded=mode == "publication",
        )
        if mode == "publication":
            _verify_publication_perf(profile, result)
        result = attach_cache_identity(result, expected)
        save_prediction(result, output_root)
        results.append(result)
    return results


def _calibration_context(
    hardware: str,
    dataset_manifest: Path,
    verified_dataset: VerifiedDataset,
) -> PreflightContext:
    system = collect_system_metadata()
    if hardware == "gpu" and not system.get("gpu"):
        raise PreflightError("--hardware gpu nhưng không phát hiện GPU")
    return PreflightContext(
        git=collect_git_metadata(ROOT),
        system=system,
        dependencies=collect_dependency_versions(),
        documents=tuple(verified_dataset),
        dataset_manifest_path=dataset_manifest.resolve(),
        dataset_manifest_sha256=verified_dataset.manifest_sha256,
    )


def _write_manifest(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("calibration", "publication"), default="publication")
    parser.add_argument(
        "--profiles",
        default=None,
        help="profile names separated by commas; publication defaults to the full catalog",
    )
    parser.add_argument("--hardware", choices=("cpu", "gpu"), default="cpu")
    parser.add_argument("--out", type=Path, default=ROOT)
    parser.add_argument(
        "--dataset-manifest",
        type=Path,
        default=None,
        help=(
            "JSON manifest; defaults to provisional datasets/calibration-manifest.json "
            "in calibration and verified datasets/manifest.json in publication"
        ),
    )
    parser.add_argument("--limit", type=int, default=None, help="calibration only")
    parser.add_argument("--only", default=None, help="calibration-only comma-separated doc IDs")
    parser.add_argument("--refresh", action="store_true", help="calibration only")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        catalog = load_profile_catalog(PROFILE_CATALOG)
        requested = list(catalog) if args.profiles is None else _split_csv(args.profiles)
        selected = verify_profile_selection(catalog, requested, mode=args.mode)

        default_manifest = (
            PUBLICATION_DATASET_MANIFEST
            if args.mode == "publication"
            else CALIBRATION_DATASET_MANIFEST
        )
        dataset_manifest = (args.dataset_manifest or default_manifest).resolve()
        if args.mode == "publication":
            overrides = {
                key: value
                for key, value in {
                    "limit": args.limit,
                    "only": args.only,
                    "refresh": True if args.refresh else None,
                }.items()
                if value is not None
            }
            context = publication_preflight(
                repo_root=ROOT,
                dataset_manifest=dataset_manifest,
                hardware=args.hardware,
                config_overrides=overrides,
                dataset_validator=verify_dataset_manifest,
            )
            run_root = args.out.resolve()
            docs: list[DatasetDocument] = list(context.documents)
        else:
            verified_dataset = verify_dataset_manifest(dataset_manifest, ROOT)
            docs = discover_documents(
                dataset_manifest,
                ROOT,
                limit=args.limit,
                only=args.only,
                verified_dataset=verified_dataset,
            )
            context = _calibration_context(
                args.hardware,
                dataset_manifest,
                verified_dataset,
            )
            run_root = args.out.resolve() / "calibration"

        configure_process_hardware(args.hardware)

        if context.dataset_manifest_sha256 is None:
            raise PreflightError("preflight không cung cấp dataset manifest hash")
        verify_manifest_unchanged(
            dataset_manifest,
            context.dataset_manifest_sha256,
        )

        # Construction happens only after every publication preflight guard passes.
        adapters: list[tuple[EngineProfile, Any]] = []
        for profile in selected.values():
            adapter = registry.build_adapter(profile)
            adapters.append((profile, adapter))

        generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        manifest = build_run_manifest(
            mode=args.mode,
            hardware=args.hardware,
            profiles=selected,
            dataset_manifest=dataset_manifest,
            dataset_manifest_sha256=context.dataset_manifest_sha256,
            generated_at=generated_at,
            git=context.git,
            system=context.system,
            dependencies=context.dependencies,
        )
        _write_manifest(run_root / "run-manifest.json", manifest)

        prediction_root = run_root / "prediction" / args.hardware
        total: list[OcrResult] = []
        for profile, adapter in adapters:
            total.extend(
                run_profile_predictions(
                    profile,
                    adapter,
                    docs,
                    prediction_root,
                    hardware=args.hardware,
                    mode=args.mode,
                    refresh=args.refresh,
                    dataset_manifest=dataset_manifest,
                    dataset_manifest_sha256=context.dataset_manifest_sha256,
                )
            )
        failed = sum(result.failed for result in total)
        print(
            f"{len(selected)} profiles × {len(docs)} documents → {prediction_root} "
            f"({failed} failed)"
        )
        return 0
    except (PreflightError, ProfileConfigError, KeyError, OSError, ValueError) as exc:
        print(f"preflight: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
