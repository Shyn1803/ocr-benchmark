"""Frozen publication-profile catalog for reproducible benchmark runs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

__all__ = ["EngineProfile", "ProfileConfigError", "load_profile_catalog"]


class ProfileConfigError(ValueError):
    """The publication profile catalog is invalid or an adapter violates it."""


@dataclass(frozen=True, slots=True)
class EngineProfile:
    name: str
    family: str
    profile: Literal["default", "scan"]
    adapter: str
    config: dict[str, object]
    environment: dict[str, object]


def load_profile_catalog(path: Path) -> dict[str, EngineProfile]:
    """Load the checked-in catalog and reject profile names that would collide."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = raw["profiles"]
    profiles = {row["name"]: EngineProfile(**row) for row in rows}
    if len(profiles) != len(rows):
        raise ProfileConfigError("trùng tên profile")
    return profiles
