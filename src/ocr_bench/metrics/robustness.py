"""B9 — sụt điểm khi tài liệu bị quét.

Đây **không** phải một `Metric`. `Metric` chấm một `(engine, tài liệu)`; độ bền
khi quét chỉ tồn tại giữa **hai** tài liệu — bản số và bản quét của cùng một gốc —
nên nó sống ở mức tổng hợp, cạnh `Aggregate`, đúng chỗ `perf.py` đang đứng.

## Định nghĩa toán học

Cho hai danh sách `MetricResult` cùng engine và cùng metric: `S` (bản số) và `Q`
(bản quét). Ghép theo `base_doc_id()`. Gọi

    P = { (s, q) : base(s) = base(q), s.value ≠ None, q.value ≠ None }

- `mean_digital = (1/|P|) Σ s.value`,  `mean_scan = (1/|P|) Σ q.value`
- `relative_drop = (mean_digital − mean_scan) / mean_digital`

Ba quyết định:

1. **Chỉ so trên cặp.** So trung bình nhóm digital với trung bình nhóm scan khi
   hai nhóm không cùng tập tài liệu là đo độ khó của hai bộ mẫu khác nhau rồi gọi
   đó là độ bền của engine. Tài liệu chỉ có ở một bên bị loại khỏi **cả hai**
   trung bình, không phải chỉ khỏi tử số.

2. **Không có cặp ⇒ `kha_dung=False`, không phải 0.0 và không phải "sụt 0%".**
   Bộ mẫu chưa có bản quét thì câu trả lời đúng là "chưa đo được". "Sụt 0%" nghe
   như engine rất bền; 0.0 nghe như engine mất sạch điểm. Cả hai đều là bịa.

3. **`excluded_doc_ids` trả `doc_id` gốc, không phải base.** Người đọc báo cáo
   phải tìm lại được **file**; trả base id thì họ cầm một chuỗi không tồn tại trên
   đĩa.

## Quy ước tên tài liệu

Biến thể phân cách bằng `"::"`: `vb-001::digital`, `vb-001::scan200`. Dấu tách
phải là chuỗi **không xuất hiện tự nhiên** trong `doc_id` — cắt theo `-digital`
thì `"only-in-digital"` biến thành `"only-in"` và hai tài liệu khác nhau bị gộp
làm một cặp giả.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ocr_bench.types import MetricResult

__all__ = ["TACH", "base_doc_id", "Degradation", "relative_degradation"]

TACH = "::"
"""Dấu tách biến thể trong `doc_id`. Xem "Quy ước tên tài liệu"."""


def base_doc_id(doc_id: str) -> str:
    """`"vb-001::scan200"` → `"vb-001"`. Không có dấu tách thì giữ nguyên."""
    return doc_id.split(TACH, 1)[0]


@dataclass(frozen=True, slots=True)
class Degradation:
    """Độ sụt tương đối giữa bản số và bản quét, tính trên cặp."""

    engine: str
    metric: str
    n_pairs: int
    excluded_doc_ids: tuple[str, ...]
    mean_digital: float | None
    mean_scan: float | None
    relative_drop: float | None
    kha_dung: bool


def _mot_gia_tri(cac: Sequence[MetricResult], truong: str) -> str:
    """Lấy giá trị chung của `truong`; lẫn lộn thì ném."""
    ten = {getattr(r, truong) for r in cac}
    if len(ten) > 1:
        raise ValueError(
            f"trộn nhiều {truong} trong một phép so độ bền: {sorted(ten)!r} — "
            f"ghép độ sụt giữa hai {truong} khác nhau không có nghĩa"
        )
    return next(iter(ten)) if ten else ""


def _theo_base(cac: Sequence[MetricResult]) -> dict[str, MetricResult]:
    ra: dict[str, MetricResult] = {}
    for r in cac:
        b = base_doc_id(r.doc_id)
        if b in ra:
            raise ValueError(
                f"hai tài liệu cùng base id {b!r} ở cùng một phía "
                f"({ra[b].doc_id!r} và {r.doc_id!r}) — không biết ghép cái nào"
            )
        ra[b] = r
    return ra


def relative_degradation(
    digital: Sequence[MetricResult], scan: Sequence[MetricResult]
) -> Degradation:
    """Sụt tương đối của một engine trên một metric, chỉ tính trên cặp."""
    tat_ca = list(digital) + list(scan)
    engine = _mot_gia_tri(tat_ca, "engine")
    metric = _mot_gia_tri(tat_ca, "metric")

    m_so = _theo_base(digital)
    m_quet = _theo_base(scan)

    cap: list[tuple[MetricResult, MetricResult]] = []
    dung_duoc: set[str] = set()
    for b, s in m_so.items():
        q = m_quet.get(b)
        # Một bên N/A thì cặp đó không đo được độ sụt. Coi N/A là 0 điểm ở bên
        # quét sẽ biến "chưa chấm được" thành "sụt 100%".
        if q is None or s.value is None or q.value is None:
            continue
        cap.append((s, q))
        dung_duoc.add(b)

    loai = tuple(
        r.doc_id
        for r in list(digital) + list(scan)
        if base_doc_id(r.doc_id) not in dung_duoc
    )

    n = len(cap)
    if n == 0:
        return Degradation(
            engine=engine,
            metric=metric,
            n_pairs=0,
            excluded_doc_ids=loai,
            mean_digital=None,
            mean_scan=None,
            relative_drop=None,
            kha_dung=False,
        )

    tb_so = sum(s.value for s, _ in cap) / n  # type: ignore[misc]
    tb_quet = sum(q.value for _, q in cap) / n  # type: ignore[misc]
    # Engine 0 điểm ở bản số thì "sụt bao nhiêu phần trăm" không có nghĩa. Trả
    # `None` chứ không ném, và cũng không lặng lẽ trả 0.0.
    sut = (tb_so - tb_quet) / tb_so if tb_so else None

    return Degradation(
        engine=engine,
        metric=metric,
        n_pairs=n,
        excluded_doc_ids=loai,
        mean_digital=tb_so,
        mean_scan=tb_quet,
        relative_drop=sut,
        kha_dung=True,
    )
