"""Tốc độ, bộ nhớ, tỉ lệ hỏng — B6 (TASK-084).

    rows = perf_rows(results)                  # engine × tài liệu  (AC-01)
    aggs = perf_aggregates(rows)               # engine
    print(bang_chi_tiet(rows))
    print(bang_tong_hop(aggs))

## Vì sao đây KHÔNG phải một `Metric`

`Metric.score()` ép điểm về `[0,1]` và ném `ValueError` nếu ra ngoài, với quy ước
**cao hơn là tốt hơn**. Perf ngược cả hai: giây và MB không có cận trên, và thấp hơn
mới là tốt hơn. Nhét perf vào `Metric` thì chỉ còn hai đường, cả hai đều tệ:

* bỏ cổng `[0,1]` — phá đúng cái cổng đang giữ 14 metric kia trung thực;
* chuẩn hoá kiểu ``1/(1+t)`` — ra một con số không ai đọc được đơn vị, và "0.31"
  không trả lời được câu hỏi thật là "chạy 1.400 tài liệu mất bao lâu".

Nên perf là một họ dữ liệu riêng, đi **cạnh** `ScoreTable` chứ không đi trong nó.

## Vì sao `FailRate` nằm trong cùng đối tượng với trung bình (AC-02)

Đúng lý do của `Aggregate` ở `metrics/base.py`: `PerfAggregate` là dataclass frozen
mang cả `sec_moi_trang_tb` lẫn `fail_rate`, và `cell()` in cả hai. Không có đường
nào lấy trung bình mà không cầm sẵn tỉ lệ hỏng. Đây là bảo đảm bằng **cấu trúc**,
không phải bằng kỷ luật của người viết bảng sau này.

Bảng perf là chỗ dễ mất `FailRate` nhất trong cả repo: engine chết ngay lập tức sẽ
có ``sec/trang`` **thấp nhất bảng**. Không có cột hỏng đi kèm thì bảng tốc độ trao
giải nhất cho engine sập nhanh nhất.

## Trung vị đi cùng trung bình

Nợ ghi từ B1. Một tài liệu 400 trang trong bộ mẫu đủ kéo lệch trung bình sec/trang;
trung vị nói phần lớn tài liệu chạy ra sao. Hai số cạnh nhau, lệch nhiều nghĩa là
phân bố có đuôi — chính là thông tin cần để đọc bảng.
"""

from __future__ import annotations

import statistics
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from ocr_bench.types import OcrResult, RssScope

__all__ = [
    "PerfRow",
    "PerfAggregate",
    "perf_rows",
    "perf_aggregate",
    "perf_aggregates",
    "bang_chi_tiet",
    "bang_tong_hop",
]

HON_HOP = "hỗn hợp"
"""Phạm vi RSS khi các tài liệu của cùng một engine không khai giống nhau."""


def _so(x: float | None, n: int = 2) -> str:
    return "—" if x is None else f"{x:.{n}f}"


@dataclass(frozen=True, slots=True)
class PerfRow:
    """Số perf của **một engine trên một tài liệu** — mức chi tiết mà AC-01 đòi."""

    engine: str
    doc_id: str
    n_trang: int | None
    """`len(page_sizes)`. `None` = engine không khai số trang."""
    seconds: float | None
    """Tổng thời gian `run()`, kể cả nạp model."""
    model_load_seconds: float | None
    seconds_per_page: float | None
    """`(seconds - model_load_seconds) / n_trang` khi trừ được, `seconds / n_trang`
    khi không. `None` nếu thiếu thời gian hoặc thiếu số trang.

    **Không** có nhánh `seconds / 1` cho engine không khai `page_sizes`: chia cho
    một trang giả làm engine trông nhanh gấp N lần trên tài liệu N trang, và không
    có triệu chứng nào để phát hiện.
    """
    da_tru_nap: bool
    """`seconds_per_page` đã trừ thời gian nạp model hay chưa (AC-03).

    Cột này phải in ra cùng số: hai engine, một đã trừ một chưa, đặt cạnh nhau mà
    không nói ra thì bảng đang so hai đại lượng khác nhau.
    """
    peak_rss_mb: float | None
    rss_scope: RssScope | None
    failed: bool


def perf_rows(results: Iterable[OcrResult]) -> list[PerfRow]:
    """Rút số perf từ kết quả engine. Sắp xếp tất định theo (engine, doc_id)."""
    rows: list[PerfRow] = []
    for r in results:
        n_trang = len(r.page_sizes) or None
        tru = r.model_load_seconds is not None
        spp: float | None = None
        if r.seconds is not None and n_trang:
            giay = r.seconds - (r.model_load_seconds or 0.0)
            spp = giay / n_trang
        rows.append(
            PerfRow(
                engine=r.engine,
                doc_id=r.doc_id,
                n_trang=n_trang,
                seconds=r.seconds,
                model_load_seconds=r.model_load_seconds,
                seconds_per_page=spp,
                da_tru_nap=tru,
                peak_rss_mb=r.peak_rss_mb,
                rss_scope=r.rss_scope,
                failed=r.failed,
            )
        )
    return sorted(rows, key=lambda x: (x.engine, x.doc_id))


@dataclass(frozen=True, slots=True)
class PerfAggregate:
    """Perf của một engine trên nhiều tài liệu.

    `fail_rate` cố ý nằm cùng đối tượng với các trung bình — xem docstring module.
    """

    engine: str
    n_total: int
    n_do_duoc: int
    """Số tài liệu có `seconds_per_page`. Nhỏ hơn `n_total` khi engine không khai
    số trang, chứ không chỉ khi engine hỏng."""
    n_failed: int
    sec_moi_trang_tb: float | None
    sec_moi_trang_trung_vi: float | None
    rss_dinh_mb: float | None
    """Đỉnh **cao nhất** qua các tài liệu — đây là con số quyết định máy cần bao
    nhiêu RAM, nên lấy max chứ không lấy trung bình."""
    rss_trung_vi_mb: float | None
    rss_scope: str | None
    """`process` · `process+children` · `hỗn hợp` · `None` (không đo được)."""
    model_load_seconds: float | None
    """Thời gian nạp model, lấy lớn nhất trong các tài liệu. Tách khỏi sec/trang
    (AC-03); `None` = engine không khai, **không** phải 0."""
    fail_rate: float
    da_tru_nap: bool

    def cell(self) -> str:
        """Một ô đọc được. Luôn có `fail` — không có đường nào bỏ nó đi."""
        rss = "—" if self.rss_dinh_mb is None else f"{self.rss_dinh_mb:.0f}MB"
        if self.rss_scope is not None:
            rss += f"[{self.rss_scope}]"
        return (
            f"{_so(self.sec_moi_trang_tb)}s/trang · {rss} · "
            f"fail {self.fail_rate:.0%}"
        )


def perf_aggregate(rows: Iterable[PerfRow]) -> PerfAggregate:
    """Gộp các dòng của **một** engine."""
    rs: Sequence[PerfRow] = list(rows)
    if not rs:
        raise ValueError("perf_aggregate() cần ít nhất một dòng")
    engines = {r.engine for r in rs}
    if len(engines) > 1:
        raise ValueError(f"perf_aggregate() nhận lẫn engine: {sorted(engines)}")

    spp = [r.seconds_per_page for r in rs if r.seconds_per_page is not None]
    rss = [r.peak_rss_mb for r in rs if r.peak_rss_mb is not None]
    nap = [r.model_load_seconds for r in rs if r.model_load_seconds is not None]
    hong = [r for r in rs if r.failed]

    pham_vi = {r.rss_scope for r in rs if r.rss_scope is not None}
    if not pham_vi:
        scope = None
    elif len(pham_vi) == 1:
        scope = pham_vi.pop()
    else:
        # Không chọn một cái làm đại diện. Một lượt chạy nửa đo được tiến trình con
        # nửa không là một lượt chạy phải xem lại, chứ không phải một ô bảng gọn.
        scope = HON_HOP

    return PerfAggregate(
        engine=engines.pop(),
        n_total=len(rs),
        n_do_duoc=len(spp),
        n_failed=len(hong),
        sec_moi_trang_tb=statistics.mean(spp) if spp else None,
        sec_moi_trang_trung_vi=statistics.median(spp) if spp else None,
        rss_dinh_mb=max(rss) if rss else None,
        rss_trung_vi_mb=statistics.median(rss) if rss else None,
        rss_scope=scope,
        model_load_seconds=max(nap) if nap else None,
        # Mẫu số là **toàn bộ** tài liệu đã thử, không phải số tài liệu đo được.
        # Lấy mẫu số là `n_do_duoc` thì engine hỏng càng nhiều `fail_rate` càng
        # thấp — đúng cái lỗi mà `metrics/base.py` được viết ra để chặn.
        fail_rate=len(hong) / len(rs),
        da_tru_nap=all(r.da_tru_nap for r in rs),
    )


def perf_aggregates(rows: Iterable[PerfRow]) -> list[PerfAggregate]:
    """Một `PerfAggregate` cho mỗi engine, sắp xếp theo tên engine."""
    theo_engine: dict[str, list[PerfRow]] = {}
    for r in rows:
        theo_engine.setdefault(r.engine, []).append(r)
    return [perf_aggregate(v) for _, v in sorted(theo_engine.items())]


# ---------------------------------------------------------------------------
# Bảng
# ---------------------------------------------------------------------------


def _chu_thich(scopes: set[str | None]) -> list[str]:
    """Chú thích bắt buộc dưới mọi bảng có cột RSS."""
    ghi = []
    if "process" in scopes:
        ghi.append(
            "⚠️ `process` = chỉ đếm tiến trình Python. Engine gọi tiến trình con "
            "(`opendataloader` chạy JVM, `sovereign` có nhánh subprocess) đang bị "
            "**đo hụt** — cài extra `perf` (`psutil`) để đếm cả tiến trình con."
        )
    if HON_HOP in scopes:
        ghi.append(
            f"⚠️ `{HON_HOP}` = các tài liệu của engine này khai phạm vi khác nhau. "
            "Không so cột RSS của nó với engine khác cho tới khi chạy lại đồng nhất."
        )
    if None in scopes:
        ghi.append("`—` ở cột RSS = không đo được (thiếu `psutil`), không phải 0 MB.")
    return ghi


def bang_chi_tiet(rows: Iterable[PerfRow]) -> str:
    """Bảng markdown engine × tài liệu — mức AC-01 đòi."""
    rs = list(rows)
    dong = [
        "| engine | doc_id | trang | giây | s/trang | trừ nạp | RSS (MB) | phạm vi | hỏng |",
        "|---|---|---:|---:|---:|:---:|---:|---|:---:|",
    ]
    for r in rs:
        dong.append(
            f"| {r.engine} | {r.doc_id} | {r.n_trang or '—'} | {_so(r.seconds)} | "
            f"{_so(r.seconds_per_page, 3)} | {'có' if r.da_tru_nap else '—'} | "
            f"{_so(r.peak_rss_mb, 1)} | {r.rss_scope or '—'} | "
            f"{'HỎNG' if r.failed else ''} |"
        )
    ghi = _chu_thich({r.rss_scope for r in rs})
    return "\n".join(dong + ([""] + [f"- {g}" for g in ghi] if ghi else []))


def bang_tong_hop(aggs: Iterable[PerfAggregate]) -> str:
    """Bảng markdown một dòng mỗi engine. **Luôn** có cột FailRate (AC-02)."""
    ags = list(aggs)
    dong = [
        "| engine | n | s/trang TB | s/trang trung vị | trừ nạp | nạp model (s) "
        "| RSS đỉnh (MB) | RSS trung vị | phạm vi | FailRate |",
        "|---|---:|---:|---:|:---:|---:|---:|---:|---|---:|",
    ]
    for a in ags:
        dong.append(
            f"| {a.engine} | {a.n_total} | {_so(a.sec_moi_trang_tb, 3)} | "
            f"{_so(a.sec_moi_trang_trung_vi, 3)} | "
            f"{'có' if a.da_tru_nap else '—'} | {_so(a.model_load_seconds)} | "
            f"{_so(a.rss_dinh_mb, 1)} | {_so(a.rss_trung_vi_mb, 1)} | "
            f"{a.rss_scope or '—'} | {a.fail_rate:.0%} |"
        )
    ghi = _chu_thich({a.rss_scope for a in ags})
    ghi.append(
        "Engine chết ngay lập tức có `s/trang` **thấp nhất** bảng. Đọc cột "
        "`FailRate` trước cột tốc độ, không phải sau."
    )
    return "\n".join(dong + [""] + [f"- {g}" for g in ghi])
