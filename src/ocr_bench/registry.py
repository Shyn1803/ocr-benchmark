"""Sổ đăng ký adapter và metric.

Kiểm tại thời điểm đăng ký, không đợi tới lúc chạy: một adapter quên khai
`capabilities`, hoặc một metric đòi năng lực không tồn tại, phải nổ ngay khi import
chứ không phải sau 3 tiếng chạy Marker.
"""

from __future__ import annotations

from ocr_bench.adapters.base import Adapter
from ocr_bench.metrics.base import Metric
from ocr_bench.types import Capability

__all__ = [
    "register_adapter",
    "get_adapter",
    "list_adapters",
    "register_metric",
    "get_metric",
    "list_metrics",
    "applicable_metrics",
    "clear",
]

_ADAPTERS: dict[str, type[Adapter]] = {}
_METRICS: dict[str, type[Metric]] = {}


def register_adapter(cls: type[Adapter]) -> type[Adapter]:
    """Dùng như decorator. Ném ngay nếu khai báo sai."""
    name = getattr(cls, "name", None)
    if not isinstance(name, str) or not name:
        raise TypeError(f"{cls.__name__} thiếu thuộc tính lớp `name`")
    caps = getattr(cls, "capabilities", None)
    if not isinstance(caps, frozenset):
        raise TypeError(
            f"{cls.__name__}.capabilities phải là frozenset khai TĨNH ở cấp lớp, "
            f"nhận {type(caps).__name__}"
        )
    unknown = {c for c in caps if not isinstance(c, Capability)}
    if unknown:
        raise TypeError(f"{cls.__name__}.capabilities có giá trị lạ: {unknown}")
    if name in _ADAPTERS and _ADAPTERS[name] is not cls:
        raise ValueError(f"adapter {name!r} đã đăng ký bởi {_ADAPTERS[name].__name__}")
    _ADAPTERS[name] = cls
    return cls


def register_metric(cls: type[Metric]) -> type[Metric]:
    name = getattr(cls, "name", None)
    if not isinstance(name, str) or not name:
        raise TypeError(f"{cls.__name__} thiếu thuộc tính lớp `name`")
    reqs = getattr(cls, "requires", None)
    if not isinstance(reqs, frozenset):
        raise TypeError(f"{cls.__name__}.requires phải là frozenset")
    unknown = {c for c in reqs if not isinstance(c, Capability)}
    if unknown:
        raise TypeError(f"{cls.__name__}.requires có giá trị lạ: {unknown}")
    if name in _METRICS and _METRICS[name] is not cls:
        raise ValueError(f"metric {name!r} đã đăng ký bởi {_METRICS[name].__name__}")
    _METRICS[name] = cls
    return cls


def get_adapter(name: str) -> type[Adapter]:
    try:
        return _ADAPTERS[name]
    except KeyError:
        raise KeyError(
            f"chưa có adapter {name!r}; hiện có: {sorted(_ADAPTERS)}"
        ) from None


def get_metric(name: str) -> type[Metric]:
    try:
        return _METRICS[name]
    except KeyError:
        raise KeyError(f"chưa có metric {name!r}; hiện có: {sorted(_METRICS)}") from None


def list_adapters() -> list[str]:
    return sorted(_ADAPTERS)


def list_metrics() -> list[str]:
    return sorted(_METRICS)


def applicable_metrics(adapter_name: str) -> dict[str, bool]:
    """Metric nào chạm tới được engine này — biết TRƯỚC khi chạy.

    Dùng để in bảng có ô ``N/A`` thay vì lặng lẽ bỏ dòng. Bỏ dòng là cách làm engine
    yếu trông mạnh.
    """
    caps = get_adapter(adapter_name).capabilities
    return {name: (cls.requires <= caps) for name, cls in sorted(_METRICS.items())}


def clear() -> None:
    """Chỉ dùng trong test."""
    _ADAPTERS.clear()
    _METRICS.clear()
