"""Run frozen OCR profiles in guarded calibration or publication mode."""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

import ocr_bench  # noqa: F401 -- import registers adapters
from ocr_bench import registry
from ocr_bench.prediction import (
    load_prediction,
    prediction_path,
    save_prediction,
)
from ocr_bench.preflight import (
    CACHE_IDENTITY_KEY,
    PreflightContext,
    PreflightError,
    build_cache_identity,
    build_run_manifest,
    collect_dependency_versions,
    collect_git_metadata,
    collect_system_metadata,
    publication_preflight,
    verify_cached_identity,
    verify_dataset_manifest,
    verify_fingerprint,
    verify_profile_selection,
)
from ocr_bench.profiles import EngineProfile, ProfileConfigError, load_profile_catalog
from ocr_bench.types import OcrResult

ROOT = Path(__file__).resolve().parent.parent
PROFILE_CATALOG = ROOT / "configs" / "profiles.json"
DATASET_MANIFEST = ROOT / "manifest.yaml"
Mode = Literal["calibration", "publication"]


def _split_csv(value: str | None) -> list[str]:
    return [] if value is None else [part.strip() for part in value.split(",") if part.strip()]


def discover_documents(
    manifest_path: Path,
    repo_root: Path,
    *,
    limit: int | None = None,
    only: str | None = None,
) -> list[Path]:
    """Resolve checked PDFs from the legacy checksum manifest deterministically.

    Task 7 can replace this boundary when its unified JSON dataset manifest lands.
    """
    del manifest_path  # existence/content is validated independently by preflight
    checksums = Path(repo_root) / "checksums.sha256"
    docs: list[Path] = []
    for raw_line in checksums.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or not parts[1].lower().endswith(".pdf"):
            continue
        path = (Path(repo_root) / parts[1].strip()).resolve()
        if path.is_file():
            docs.append(path)
    docs.sort(key=lambda path: path.relative_to(repo_root).as_posix())
    if only:
        requested = set(_split_csv(only))
        by_stem = {doc.stem: doc for doc in docs}
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
    duplicate_stems = sorted(
        {doc.stem for doc in docs if sum(other.stem == doc.stem for other in docs) > 1}
    )
    if duplicate_stems:
        raise PreflightError(
            "doc_id trùng giữa các PDF: " + ", ".join(duplicate_stems[:5])
        )
    return docs


def attach_cache_identity(
    result: OcrResult, identity: Mapping[str, str]
) -> OcrResult:
    """Persist publication cache provenance under a secret-safe fingerprint key."""
    fingerprint = dict(result.config_fingerprint)
    fingerprint[CACHE_IDENTITY_KEY] = dict(identity)
    fingerprint["profile_config_sha256"] = identity["profile_config_sha256"]
    return dataclasses.replace(result, config_fingerprint=fingerprint)


def _normalize_profile_identity(
    result: OcrResult,
    profile: EngineProfile,
    *,
    doc: Path,
    engine_version: str,
) -> OcrResult:
    if result.engine != profile.name:
        raise PreflightError(
            f"{doc}: adapter trả engine={result.engine!r}, cần {profile.name!r}"
        )
    if result.doc_id != doc.stem:
        raise PreflightError(
            f"{doc}: adapter trả doc_id={result.doc_id!r}, cần {doc.stem!r}"
        )
    if result.engine_version != engine_version:
        raise PreflightError(
            f"{profile.name}/{doc.stem}: result version={result.engine_version!r}, "
            f"adapter version={engine_version!r}"
        )
    return dataclasses.replace(
        result,
        engine_family=profile.family,
        profile=profile.profile,
    )


def _verify_cached_result(
    cached: OcrResult,
    profile: EngineProfile,
    *,
    doc: Path,
    engine_version: str,
) -> None:
    """Verify prediction payload identity independently of its embedded cache key."""
    expected = {
        "engine": profile.name,
        "engine_family": profile.family,
        "profile": profile.profile,
        "doc_id": doc.stem,
        "engine_version": engine_version,
    }
    for field, expected_value in expected.items():
        actual_value = getattr(cached, field)
        if actual_value != expected_value:
            raise PreflightError(
                f"{profile.name}/{doc.stem}: cached {field}={actual_value!r}, "
                f"cần {expected_value!r}"
            )
    verify_fingerprint(profile, cached.config_fingerprint)


def run_profile_predictions(
    profile: EngineProfile,
    adapter: Any,
    docs: Sequence[Path],
    output_root: Path,
    *,
    hardware: Literal["cpu", "gpu"],
    mode: Mode,
    refresh: bool = False,
) -> list[OcrResult]:
    """Run/resume one profile; publication cache drift is always fatal."""
    if mode == "publication" and refresh:
        raise PreflightError("publication không cho phép refresh cache")
    engine_version = adapter.version()
    verify_fingerprint(profile, adapter.config_fingerprint())
    results: list[OcrResult] = []
    for doc in docs:
        expected = build_cache_identity(
            doc,
            profile,
            engine_version=engine_version,
            hardware=hardware,
        )
        path = prediction_path(output_root, profile.name, doc.stem)
        if path.is_file() and not refresh:
            cached = load_prediction(path)
            try:
                _verify_cached_result(
                    cached,
                    profile,
                    doc=doc,
                    engine_version=engine_version,
                )
                verify_cached_identity(profile, cached.config_fingerprint, expected)
            except PreflightError:
                if mode == "publication":
                    raise
            else:
                results.append(cached)
                continue
        result = adapter.execute(doc)
        result = _normalize_profile_identity(
            result,
            profile,
            doc=doc,
            engine_version=engine_version,
        )
        verify_fingerprint(profile, result.config_fingerprint)
        result = attach_cache_identity(result, expected)
        save_prediction(result, output_root)
        results.append(result)
    return results


def _calibration_context(hardware: str) -> PreflightContext:
    system = collect_system_metadata()
    if hardware == "gpu" and not system.get("gpu"):
        raise PreflightError("--hardware gpu nhưng không phát hiện GPU")
    return PreflightContext(
        git=collect_git_metadata(ROOT),
        system=system,
        dependencies=collect_dependency_versions(),
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
    parser.add_argument("--dataset-manifest", type=Path, default=DATASET_MANIFEST)
    parser.add_argument("--limit", type=int, default=None, help="calibration only")
    parser.add_argument("--only", default=None, help="calibration-only comma-separated doc IDs")
    parser.add_argument("--refresh", action="store_true", help="calibration only")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        catalog = load_profile_catalog(PROFILE_CATALOG)
        requested = sorted(catalog) if args.profiles is None else _split_csv(args.profiles)
        selected = verify_profile_selection(catalog, requested, mode=args.mode)

        dataset_manifest = args.dataset_manifest.resolve()
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
        else:
            if not dataset_manifest.is_file():
                raise PreflightError(f"dataset manifest không tồn tại: {dataset_manifest}")
            context = _calibration_context(args.hardware)
            run_root = args.out.resolve() / "calibration"

        docs = discover_documents(
            dataset_manifest,
            ROOT,
            limit=args.limit,
            only=args.only,
        )

        # Construction happens only after every publication preflight guard passes.
        adapters: list[tuple[EngineProfile, Any]] = []
        for profile in selected.values():
            adapter = registry.build_adapter(profile)
            verify_fingerprint(profile, adapter.config_fingerprint())
            adapters.append((profile, adapter))

        generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        manifest = build_run_manifest(
            mode=args.mode,
            hardware=args.hardware,
            profiles=selected,
            dataset_manifest=dataset_manifest,
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
