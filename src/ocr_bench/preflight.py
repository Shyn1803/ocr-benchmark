"""Fail-closed guards and provenance for reproducible publication runs."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from ocr_bench.profiles import EngineProfile

__all__ = [
    "CACHE_IDENTITY_KEY",
    "PreflightContext",
    "PreflightError",
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
    "verify_no_config_overrides",
    "verify_profile_selection",
]

Hardware = Literal["cpu", "gpu"]
CACHE_IDENTITY_KEY = "publication_cache"
_HASH_LENGTH = 64
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
class PreflightContext:
    git: dict[str, object]
    system: dict[str, object]
    dependencies: dict[str, str | None]


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
            "publication bắt buộc chạy toàn bộ profile catalog (" + "; ".join(details) + ")"
        )
    return {name: catalog[name] for name in selected}


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


def verify_dataset_manifest(manifest_path: Path, repo_root: Path) -> None:
    """Validate current legacy manifest/checksum files; Task 7 may inject stricter validation."""
    manifest_path = Path(manifest_path)
    if not manifest_path.is_file() or not manifest_path.read_bytes().strip():
        raise PreflightError(f"dataset manifest không tồn tại hoặc rỗng: {manifest_path}")
    checksums = Path(repo_root) / "checksums.sha256"
    if not checksums.is_file():
        raise PreflightError(f"thiếu checksum manifest: {checksums}")
    for line_number, raw_line in enumerate(
        checksums.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or len(parts[0]) != _HASH_LENGTH:
            raise PreflightError(f"{checksums}:{line_number}: dòng checksum không hợp lệ")
        expected, relative = parts
        target = _safe_manifest_target(Path(repo_root), relative.strip())
        if not target.is_file():
            raise PreflightError(f"checksum thiếu file: {relative.strip()}")
        actual = sha256_file(target)
        if actual != expected.lower():
            raise PreflightError(
                f"checksum lệch: {relative.strip()} expected={expected.lower()} actual={actual}"
            )


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


def _ram_bytes() -> int | None:
    try:
        import psutil  # noqa: PLC0415

        return int(psutil.virtual_memory().total)
    except (ImportError, OSError):
        if hasattr(os, "sysconf"):
            try:
                return int(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES"))
            except (OSError, ValueError):
                pass
    return None


def collect_system_metadata() -> dict[str, object]:
    """Collect explicit hardware/runtime facts without copying environment variables."""
    cpu = platform.processor().strip() or os.environ.get("PROCESSOR_IDENTIFIER", "").strip()
    return {
        "python": platform.python_version(),
        "os": platform.platform(),
        "cpu": cpu or "unknown",
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
    dataset_validator: Callable[[Path, Path], None] = verify_dataset_manifest,
    system_probe: Callable[[], dict[str, object]] = collect_system_metadata,
    dependency_probe: Callable[[], dict[str, str | None]] = collect_dependency_versions,
) -> PreflightContext:
    """Run every publication-only guard before an adapter is constructed."""
    verify_no_config_overrides(config_overrides)
    dataset_validator(Path(dataset_manifest), Path(repo_root))
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
    )


def build_cache_identity(
    doc: Path,
    profile: EngineProfile,
    *,
    engine_version: str,
    hardware: Hardware,
) -> dict[str, str]:
    """Build the complete identity that authorizes reuse of one prediction."""
    return {
        "doc_id": Path(doc).stem,
        "pdf_sha256": sha256_file(Path(doc)),
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
        "profiles": {
            name: profiles[name].fingerprint for name in sorted(profiles)
        },
        "dataset_manifest": {
            "path": Path(dataset_manifest).name,
            "sha256": sha256_file(Path(dataset_manifest)),
        },
    }
