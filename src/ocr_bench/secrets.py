"""Nhận diện và redaction credential trước khi dữ liệu benchmark được lưu."""

from __future__ import annotations

import re

__all__ = ["contains_secret_pattern", "is_secret_bearing_key", "sanitize_secret_text"]


_BEARER_RE = re.compile(r"(?i)\bBearer(?P<space>\s+)(?P<value>[^\s,;'\"]+)")
_SK_RE = re.compile(r"(?i)\bsk-[A-Za-z0-9_-]+")
_KEY_VALUE_RE = re.compile(
    r"(?i)(?P<quote>['\"]?)(?P<key>\b(?:[A-Za-z0-9]+[_-])*"
    r"(?:api[_-]?key|access[_-]?token|token|secret|password)\b)"
    r"(?P=quote)(?P<sep>\s*[:=]\s*)"
    r"(?P<value>\"[^\"\r\n]*\"|'[^'\r\n]*'|[^\s,;}\]\r\n]+)"
)
_SECRET_KEY_RE = re.compile(
    r"(?i)(?:^|[_-])(?:api[_-]?key|access[_-]?token|token|secret|password)(?:$|[_-])"
)


def _redact_key_value(match: re.Match[str]) -> str:
    value = match.group("value")
    value_quote = value[0] if value[:1] in {'"', "'"} else ""
    raw_value = value[1:-1] if value_quote else value
    if raw_value in {"", "<redacted>"}:
        return match.group(0)
    replacement = f"{value_quote}<redacted>{value_quote}" if value_quote else "<redacted>"
    return (
        f"{match.group('quote')}{match.group('key')}{match.group('quote')}"
        f"{match.group('sep')}{replacement}"
    )


def sanitize_secret_text(value: str | None) -> str | None:
    """Redact các credential pattern phổ biến nhưng giữ nguyên metadata an toàn."""
    if value is None:
        return None
    sanitized = _BEARER_RE.sub(
        lambda m: f"Bearer{m.group('space')}<redacted>", value
    )
    sanitized = _SK_RE.sub("<redacted>", sanitized)
    return _KEY_VALUE_RE.sub(_redact_key_value, sanitized)


def contains_secret_pattern(value: str) -> bool:
    return sanitize_secret_text(value) != value


def is_secret_bearing_key(key: str) -> bool:
    return bool(_SECRET_KEY_RE.search(key))
