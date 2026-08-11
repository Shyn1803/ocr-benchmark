"""Fail-closed guards and provenance for reproducible publication runs."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from ocr_bench.profiles import EngineProfile

__all__ = [
    "CACHE_IDENTITY_KEY",
    "DatasetDocument",
    "PreflightContext",
    "PreflightError",
    "VerifiedDataset",
    "build_cache_identity",
    "build_run_manifest",
    "collect_dependency_versions",
    "collect_git_metadata",
    "collect_system_metadata",
    "publication_preflight",
    "sha256_file",
    "verify_cached_identity",
    "verify_dataset_manifest",
    "verify_fingerprint",
    "verify_manifest_unchanged",
    "verify_no_config_overrides",
    "verify_profile_selection",
]

Hardware = Literal["cpu", "gpu"]
CACHE_IDENTITY_KEY = "publication_cache"
_DEPENDENCIES = (
    "ocr-bench",
    "Pillow",
    "marker-pdf",
    "opendataloader-pdf",
    "pdf-inspector",
    "psutil",
    "torch",
)


class PreflightError(RuntimeError):
    """A run is not reproducible enough to publish safely."""


@dataclass(frozen=True, slots=True)
class DatasetDocument:
    """One locally resolved PDF whose bytes match a supplied manifest row."""

    doc_id: str
    path: Path
    pdf_sha256: str


@dataclass(frozen=True, slots=True)
class VerifiedDataset(Sequence[DatasetDocument]):
    """Manifest documents and provenance derived from one immutable byte snapshot."""

    documents: tuple[DatasetDocument, ...]
    manifest_sha256: str
    provisional: bool

    def __getitem__(self, index: int | slice) -> DatasetDocument | tuple[DatasetDocument, ...]:
        return self.documents[index]

    def __len__(self) -> int:
        return len(self.documents)


@dataclass(frozen=True, slots=True)
class PreflightContext:
    git: dict[str, object]
    system: dict[str, object]
    dependencies: dict[str, str | None]
    documents: tuple[DatasetDocument, ...] = ()
    dataset_manifest_path: Path | None = None
    dataset_manifest_sha256: str | None = None


def sha256_file(path: Path) -> str:
    """Hash file bytes without loading a potentially large PDF into memory."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _plain(nested) for key, nested in value.items()}
    if isinstance(value, tuple):
        return [_plain(nested) for nested in value]
    return value


def _lookup(mapping: Mapping[str, object], path: Sequence[str]) -> tuple[bool, object]:
    current: object = mapping
    for part in path:
        if not isinstance(current, Mapping) or part not in current:
            return False, None
        current = current[part]
    return True, current


def _verify_tree(
    profile: EngineProfile,
    expected: Mapping[str, object],
    actual_roots: Sequence[Mapping[str, object]],
    *,
    prefix: str,
) -> None:
    def walk(value: object, path: tuple[str, ...]) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                walk(nested, (*path, key))
            return
        found = False
        got: object = None
        for root in actual_roots:
            found, got = _lookup(root, path)
            if found:
                break
        label = ".".join((prefix, *path)) if prefix else ".".join(path)
        if not found:
            raise PreflightError(f"{profile.name}: fingerprint thiếu {label}")
        if _plain(got) != _plain(value):
            raise PreflightError(
                f"{profile.name}: fingerprint {label}={got!r}, catalog khóa {_plain(value)!r}"
            )

    walk(expected, ())


def verify_fingerprint(
    profile: EngineProfile, actual_config: Mapping[str, object]
) -> None:
    """Verify every locked config/environment leaf while allowing runtime metadata.

    Adapters may add engine/model versions to their fingerprint. Locked values may
    either be at the top level (legacy adapter convention) or beneath explicit
    ``config``/``environment`` objects.
    """
    config_roots: list[Mapping[str, object]] = [actual_config]
    nested_config = actual_config.get("config")
    if isinstance(nested_config, Mapping):
        config_roots.insert(0, nested_config)
    _verify_tree(profile, profile.config, config_roots, prefix="config")

    if profile.environment:
        environment_roots: list[Mapping[str, object]] = [actual_config]
        nested_environment = actual_config.get("environment")
        if isinstance(nested_environment, Mapping):
            environment_roots.insert(0, nested_environment)
        _verify_tree(
            profile,
            profile.environment,
            environment_roots,
            prefix="environment",
        )

    recorded = actual_config.get("profile_config_sha256")
    if recorded is not None and recorded != profile.fingerprint:
        raise PreflightError(
            f"{profile.name}: profile_config_sha256={recorded!r}, "
            f"catalog={profile.fingerprint!r}"
        )


def verify_profile_selection(
    catalog: Mapping[str, EngineProfile],
    selected: Sequence[str],
    *,
    mode: Literal["calibration", "publication"],
) -> dict[str, EngineProfile]:
    """Resolve names and require the complete catalog for publication."""
    if not selected:
        raise PreflightError("không có profile nào được chọn")
    duplicates = sorted({name for name in selected if selected.count(name) > 1})
    if duplicates:
        raise PreflightError(f"profile bị lặp: {', '.join(duplicates)}")
    unknown = sorted(set(selected) - set(catalog))
    if unknown:
        raise PreflightError(f"profile không có trong catalog: {', '.join(unknown)}")
    if mode == "publication" and set(selected) != set(catalog):
        missing = sorted(set(catalog) - set(selected))
        extra = sorted(set(selected) - set(catalog))
        details = []
        if missing:
            details.append(f"thiếu {', '.join(missing)}")
        if extra:
            details.append(f"thừa {', '.join(extra)}")
        raise PreflightError(
            "publication bắt buộc chạy toàn bộ profile catalog ("
            + "; ".join(details)
            + ")"
        )
    order = list(catalog) if mode == "publication" else list(selected)
    return {name: catalog[name] for name in order}


def verify_no_config_overrides(overrides: Mapping[str, object] | None) -> None:
    """Publication configuration comes only from the checked-in catalog."""
    if overrides:
        raise PreflightError(
            "publication không cho phép CLI config override: "
            + ", ".join(sorted(overrides))
        )


def _git(repo_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise PreflightError(f"git {' '.join(args)} thất bại: {detail}")
    return completed.stdout.strip()


def collect_git_metadata(
    repo_root: Path, *, require_clean: bool = False
) -> dict[str, object]:
    """Record commit/dirty state and optionally reject any tracked or untracked change."""
    commit = _git(repo_root, "rev-parse", "HEAD")
    dirty_output = _git(
        repo_root,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    )
    dirty = bool(dirty_output)
    if dirty and require_clean:
        first = dirty_output.splitlines()[0]
        raise PreflightError(f"working tree không sạch: {first}")
    return {"commit": commit, "dirty": dirty}


def _safe_manifest_target(repo_root: Path, relative: str) -> Path:
    candidate = (repo_root / Path(relative)).resolve()
    root = repo_root.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        raise PreflightError(f"checksum trỏ ra ngoài repo: {relative!r}") from None
    return candidate


def _manifest_pdf(row: Mapping[str, object], doc_id: str, repo_root: Path) -> Path:
    explicit = next(
        (
            row[key]
            for key in ("pdf_path", "path", "local_pdf")
            if key in row and row[key] is not None
        ),
        None,
    )
    if explicit is not None:
        if not isinstance(explicit, str) or not explicit.strip():
            raise PreflightError(
                f"{doc_id}: pdf_path phải là chuỗi tương đối không rỗng"
            )
        candidate = _safe_manifest_target(repo_root, explicit)
        if candidate.suffix.lower() != ".pdf":
            raise PreflightError(f"{doc_id}: pdf_path không phải PDF: {explicit!r}")
        if not candidate.is_file():
            raise PreflightError(f"{doc_id}: missing PDF: {explicit!r}")
        return candidate

    pdf_root = repo_root / "pdfs"
    search_root = pdf_root if pdf_root.is_dir() else repo_root
    matches = sorted(
        path.resolve()
        for path in search_root.rglob("*.pdf")
        if path.stem == doc_id
    )
    if not matches:
        raise PreflightError(f"{doc_id}: missing local PDF")
    if len(matches) != 1:
        raise PreflightError(
            f"{doc_id}: ambiguous local PDF ({len(matches)} matches); add explicit pdf_path"
        )
    return matches[0]


def verify_dataset_manifest(
    manifest_path: Path, repo_root: Path
) -> VerifiedDataset:
    """Resolve exactly the PDFs declared by the supplied per-document JSON manifest."""
    manifest_path = Path(manifest_path)
    repo_root = Path(repo_root).resolve()
    if not manifest_path.is_file():
        raise PreflightError(f"dataset manifest không tồn tại: {manifest_path}")
    try:
        manifest_bytes = manifest_path.read_bytes()
        manifest_sha256 = hashlib.sha256(manifest_bytes).hexdigest()
        raw = json.loads(manifest_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PreflightError(f"dataset manifest JSON không hợp lệ: {exc}") from None
    if not isinstance(raw, Mapping) or not isinstance(raw.get("documents"), list):
        raise PreflightError("dataset manifest phải có documents là một list không rỗng")
    if not raw["documents"]:
        raise PreflightError("dataset manifest documents rỗng")
    provisional = raw.get("provisional", False)
    if not isinstance(provisional, bool):
        raise PreflightError("dataset manifest provisional phải là boolean")

    documents: list[DatasetDocument] = []
    seen_ids: set[str] = set()
    seen_paths: set[Path] = set()
    for index, row in enumerate(raw["documents"]):
        if not isinstance(row, Mapping):
            raise PreflightError(f"documents[{index}] phải là object")
        doc_id = row.get("document_id", row.get("doc_id"))
        if not isinstance(doc_id, str) or not doc_id.strip():
            raise PreflightError(f"documents[{index}]: thiếu document_id/doc_id")
        doc_id = doc_id.strip()
        if doc_id in seen_ids:
            raise PreflightError(f"duplicate document_id: {doc_id}")
        seen_ids.add(doc_id)

        expected = row.get("pdf_sha256")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
            raise PreflightError(f"{doc_id}: pdf_sha256 không hợp lệ")
        path = _manifest_pdf(row, doc_id, repo_root)
        if path in seen_paths:
            raise PreflightError(f"duplicate PDF path in manifest: {path}")
        seen_paths.add(path)
        actual = sha256_file(path)
        if actual != expected.lower():
            raise PreflightError(
                f"{doc_id}: PDF checksum mismatch expected={expected.lower()} actual={actual}"
            )
        documents.append(DatasetDocument(doc_id, path, actual))
    return VerifiedDataset(tuple(documents), manifest_sha256, provisional)


def _gpu_name() -> str | None:
    try:
        completed = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError:
        return None
    names = sorted({line.strip() for line in completed.stdout.splitlines() if line.strip()})
    return "; ".join(names) if completed.returncode == 0 and names else None


def _ram_bytes_windows() -> int | None:
    """RAM vật lý trên Windows, không cần psutil.

    Windows không có `os.sysconf`, nên khi psutil vắng mặt thì hai nhánh cũ đều trượt và
    `ram_bytes` về `None` — `publication_preflight` coi đó là "không thu thập đủ CPU/RAM"
    và chặn toàn bộ lần công bố. Máy chạy bench này là Windows, nên nhánh thiếu đó không
    phải trường hợp hiếm mà là trường hợp mặc định.
    """
    if sys.platform != "win32":
        return None
    try:
        import ctypes  # noqa: PLC0415

        class _MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        trang_thai = _MEMORYSTATUSEX()
        trang_thai.dwLength = ctypes.sizeof(_MEMORYSTATUSEX)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(trang_thai)):
            return None
        return int(trang_thai.ullTotalPhys) or None
    except (ImportError, AttributeError, OSError, ValueError):
        return None


def _ram_bytes() -> int | None:
    try:
        import psutil  # noqa: PLC0415

        return int(psutil.virtual_memory().total)
    except (ImportError, OSError):
        pass
    if hasattr(os, "sysconf"):
        try:
            return int(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES"))
        except (OSError, ValueError):
            pass
    return _ram_bytes_windows()


def collect_system_metadata() -> dict[str, object]:
    """Collect explicit hardware/runtime facts without copying environment variables."""
    cpu = platform.processor().strip() or os.environ.get("PROCESSOR_IDENTIFIER", "").strip()
    return {
        "python": platform.python_version(),
        "os": platform.platform(),
        "cpu": cpu or None,
        "gpu": _gpu_name(),
        "ram_bytes": _ram_bytes(),
    }


def collect_dependency_versions() -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for package in _DEPENDENCIES:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    return versions


def publication_preflight(
    *,
    repo_root: Path,
    dataset_manifest: Path,
    hardware: Hardware,
    config_overrides: Mapping[str, object] | None = None,
    dataset_validator: Callable[[Path, Path], VerifiedDataset] = verify_dataset_manifest,
    system_probe: Callable[[], dict[str, object]] = collect_system_metadata,
    dependency_probe: Callable[[], dict[str, str | None]] = collect_dependency_versions,
) -> PreflightContext:
    """Run every publication-only guard before an adapter is constructed."""
    verify_no_config_overrides(config_overrides)
    dataset_manifest = Path(dataset_manifest)
    if not dataset_manifest.is_file():
        raise PreflightError(
            f"verified publication dataset manifest missing: {dataset_manifest}"
        )
    validated = dataset_validator(dataset_manifest, Path(repo_root))
    if not isinstance(validated, VerifiedDataset):
        raise PreflightError("dataset validator phải trả VerifiedDataset đã xác minh")
    if validated.provisional:
        raise PreflightError("publication dataset manifest is provisional, not verified")
    documents = tuple(validated)
    if not documents:
        raise PreflightError("dataset validator không trả document nào")
    if any(not isinstance(document, DatasetDocument) for document in documents):
        raise PreflightError("dataset validator trả phần tử không phải DatasetDocument")
    git = collect_git_metadata(Path(repo_root), require_clean=True)
    system = system_probe()
    if hardware == "gpu" and not system.get("gpu"):
        raise PreflightError("--hardware gpu nhưng không phát hiện GPU")
    if not system.get("cpu") or system.get("ram_bytes") is None:
        raise PreflightError("không thu thập đủ CPU/RAM cho publication manifest")
    return PreflightContext(
        git=git,
        system=system,
        dependencies=dependency_probe(),
        documents=documents,
        dataset_manifest_path=dataset_manifest.resolve(),
        dataset_manifest_sha256=validated.manifest_sha256,
    )


def verify_manifest_unchanged(manifest_path: Path, expected_sha256: str) -> None:
    """Fail if the manifest bytes differ from the snapshot used by preflight."""
    actual = sha256_file(Path(manifest_path))
    if actual != expected_sha256:
        raise PreflightError(
            "dataset manifest changed after validation "
            f"expected={expected_sha256} actual={actual}"
        )


def build_cache_identity(
    doc: Path,
    profile: EngineProfile,
    *,
    engine_version: str,
    hardware: Hardware,
    doc_id: str | None = None,
    pdf_sha256: str | None = None,
) -> dict[str, str]:
    """Build the complete identity that authorizes reuse of one prediction."""
    actual_pdf_sha256 = sha256_file(Path(doc))
    if pdf_sha256 is not None and actual_pdf_sha256 != pdf_sha256:
        raise PreflightError(
            f"{doc_id or Path(doc).stem}: PDF checksum changed after manifest validation "
            f"expected={pdf_sha256} actual={actual_pdf_sha256}"
        )
    return {
        "doc_id": doc_id or Path(doc).stem,
        "pdf_sha256": actual_pdf_sha256,
        "profile_config_sha256": profile.fingerprint,
        "engine_version": engine_version,
        "hardware": hardware,
    }


def verify_cached_identity(
    profile: EngineProfile,
    actual_fingerprint: Mapping[str, object],
    expected: Mapping[str, str],
) -> None:
    """Reject missing, extra, or changed publication cache identity fields."""
    raw_identity = actual_fingerprint.get(CACHE_IDENTITY_KEY)
    if not isinstance(raw_identity, Mapping):
        raise PreflightError(
            f"{profile.name}: cache thiếu config_fingerprint.{CACHE_IDENTITY_KEY}"
        )
    for key, expected_value in expected.items():
        actual_value = raw_identity.get(key)
        if actual_value != expected_value:
            raise PreflightError(
                f"{profile.name}: cache {key}={actual_value!r}, cần {expected_value!r}"
            )
    extras = sorted(set(raw_identity) - set(expected))
    if extras:
        raise PreflightError(f"{profile.name}: cache identity có field lạ {extras}")


def build_run_manifest(
    *,
    mode: Literal["calibration", "publication"],
    hardware: Hardware,
    profiles: Mapping[str, EngineProfile],
    dataset_manifest: Path,
    dataset_manifest_sha256: str,
    generated_at: str,
    git: Mapping[str, object],
    system: Mapping[str, object],
    dependencies: Mapping[str, str | None],
) -> dict[str, Any]:
    """Return a deterministic, secret-free run manifest payload."""
    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "mode": mode,
        "hardware": hardware,
        "git": {key: git[key] for key in sorted(git)},
        "system": {key: system[key] for key in sorted(system)},
        "dependencies": {
            key: dependencies[key] for key in sorted(dependencies)
        },
        "profiles": [
            {"name": name, "config_sha256": profile.fingerprint}
            for name, profile in profiles.items()
        ],
        "dataset_manifest": {
            "path": Path(dataset_manifest).name,
            "sha256": dataset_manifest_sha256,
        },
    }
