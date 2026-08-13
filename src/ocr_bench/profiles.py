"""Frozen publication-profile catalog for reproducible benchmark runs."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from types import MappingProxyType

__all__ = [
    "EngineProfile",
    "ProfileConfigError",
    "MucSabotage",
    "load_profile_catalog",
    "load_sabotage_levels",
]


class ProfileConfigError(ValueError):
    """The publication profile catalog is invalid or an adapter violates it."""


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


def _canonical_json(value: object) -> object:
    """Return JSON data suitable for deterministic hashing."""
    if isinstance(value, Mapping):
        return {
            nested_key: _canonical_json(nested)
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

        Key ordering does not affect the digest. The catalog validation boundary
        forbids secret values, so every retained value remains in the digest.
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


@dataclass(frozen=True, slots=True)
class MucSabotage:
    """Một mức phá hoại đã khai trong catalog.

    Nằm ngoài :class:`EngineProfile` có chủ ý: `profiles[]` là danh mục **engine được
    công bố** (tập hợp bị khoá bằng test, `profile` chỉ nhận ``default``/``scan``).
    `sabotage` là dụng cụ dùng để kiểm chính bộ thước đo — khai nó như một engine công
    bố là tự thêm một cột vào bảng cho một công cụ OCR không tồn tại.
    """

    name: str
    severity: float
    source: str
    seed: int


def load_sabotage_levels(path: Path) -> tuple[MucSabotage, ...]:
    """Đọc `sabotage_levels` và bắt buộc mọi ràng buộc làm nó có nghĩa.

    Ba ràng buộc, thiếu cái nào cũng biến phép so đơn điệu thành phép so vô nghĩa:

    1. **Tên phải suy ra được từ severity** (`ten_muc_sabotage`). Tên khai tay lệch
       khỏi severity thì bảng điểm ghi một đằng, phép so đọc một nẻo.
    2. **Severity tăng ngặt.** Hai mức trùng nhau là hai cột giống hệt mang hai tên.
    3. **Cùng một seed.** Đổi seed giữa các mức thì chênh lệch điểm là chênh lệch
       *quần thể ngẫu nhiên*, không phải chênh lệch mức hỏng.
    """
    from ocr_bench.adapters.sabotage import ten_muc_sabotage

    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = raw.get("sabotage_levels", [])
    if not rows:
        raise ProfileConfigError(f"{path} không khai `sabotage_levels`")

    muc = tuple(MucSabotage(**row) for row in rows)

    for m in muc:
        mong_doi = ten_muc_sabotage(m.severity)
        if m.name != mong_doi:
            raise ProfileConfigError(
                f"tên mức sabotage {m.name!r} không khớp severity {m.severity} "
                f"(phải là {mong_doi!r})"
            )
        if not 0.0 < m.severity < 1.0:
            raise ProfileConfigError(f"severity phải trong (0, 1), gặp {m.severity}")

    sev = [m.severity for m in muc]
    if sev != sorted(set(sev)) or len(set(sev)) != len(sev):
        raise ProfileConfigError(f"severity phải tăng ngặt, gặp {sev}")

    seeds = {m.seed for m in muc}
    if len(seeds) > 1:
        raise ProfileConfigError(
            f"các mức sabotage phải dùng chung một seed, gặp {sorted(seeds)} — "
            "khác seed thì chênh lệch điểm là chênh lệch quần thể, không phải mức hỏng"
        )

    nguon = {m.source for m in muc}
    if len(nguon) > 1:
        raise ProfileConfigError(
            f"các mức sabotage phải chung một engine nguồn, gặp {sorted(nguon)}"
        )

    return muc


def load_profile_catalog(path: Path) -> dict[str, EngineProfile]:
    """Load the checked-in catalog and reject profile names that would collide."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = raw["profiles"]
    profiles = {row["name"]: EngineProfile(**row) for row in rows}
    if len(profiles) != len(rows):
        raise ProfileConfigError("trùng tên profile")
    return profiles
