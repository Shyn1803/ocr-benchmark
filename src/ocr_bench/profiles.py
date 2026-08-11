"""Frozen publication-profile catalog for reproducible benchmark runs."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from types import MappingProxyType

__all__ = ["EngineProfile", "ProfileConfigError", "load_profile_catalog"]


class ProfileConfigError(ValueError):
    """The publication profile catalog is invalid or an adapter violates it."""


_SECRET_KEY_PARTS = frozenset({"api_key", "password", "secret", "token"})


def _freeze_json(value: object) -> object:
    """Recursively freeze JSON-compatible values retained by a profile."""
    if isinstance(value, Mapping):
        frozen: dict[str, object] = {}
        for key, nested in value.items():
            if not isinstance(key, str):
                raise ProfileConfigError("JSON object key phải là chuỗi")
            frozen[key] = _freeze_json(nested)
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(nested) for nested in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise ProfileConfigError(f"giá trị profile không phải JSON: {type(value).__name__}")


def _canonical_json(value: object, *, key: str | None = None) -> object:
    """Return JSON data suitable for deterministic, secret-safe hashing."""
    if key is not None and any(part in key.lower() for part in _SECRET_KEY_PARTS):
        return "<redacted>"
    if isinstance(value, Mapping):
        return {
            nested_key: _canonical_json(nested, key=nested_key)
            for nested_key, nested in value.items()
        }
    if isinstance(value, tuple):
        return [_canonical_json(nested) for nested in value]
    return value


@dataclass(frozen=True, slots=True)
class EngineProfile:
    name: str
    family: str
    profile: Literal["default", "scan"]
    adapter: str
    config: Mapping[str, object]
    environment: Mapping[str, object]

    def __post_init__(self) -> None:
        object.__setattr__(self, "config", _freeze_json(self.config))
        object.__setattr__(self, "environment", _freeze_json(self.environment))

    @property
    def fingerprint(self) -> str:
        """Canonical SHA-256 of profile identity, config, and environment.

        Key ordering does not affect the digest. Values under keys that look
        secret-bearing are redacted before hashing so a fingerprint is safe to
        write into a publication artifact.
        """
        payload = _canonical_json(
            {
                "name": self.name,
                "family": self.family,
                "profile": self.profile,
                "adapter": self.adapter,
                "config": self.config,
                "environment": self.environment,
            }
        )
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_profile_catalog(path: Path) -> dict[str, EngineProfile]:
    """Load the checked-in catalog and reject profile names that would collide."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = raw["profiles"]
    profiles = {row["name"]: EngineProfile(**row) for row in rows}
    if len(profiles) != len(rows):
        raise ProfileConfigError("trùng tên profile")
    return profiles
