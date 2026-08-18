"""Bốn hình của bản công bố — khoá lại đúng những chỗ đã từng sai.

Bản trước của file này gọi cả bốn renderer với `data={}` rồi chỉ khẳng định chuỗi
`"<svg"` có trong file. Nó xanh suốt thời gian `render_forest_plot` vẽ ra
`marker_default` / `sovereign_scan` — bốn profile chưa từng chạy — vì một hình bịa
vẫn là một hình có chữ `<svg`. Test ở đây kiểm bốn tính chất mà cái sai đó vi phạm:

1. mọi tên engine trong SVG phải thuộc bảng đầu vào;
2. metric không đo được ra **chữ**, không ra cột (cột cao 0 đọc thành "điểm 0");
3. hai lần render ra byte giống hệt;
4. đầu vào không phải `ScoreTable` thì **raise**, không im lặng lấy default.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from ocr_bench.metrics.perf import perf_aggregates, perf_rows
from ocr_bench.research_charts import (
    render_accuracy_speed_chart,
    render_failure_distribution_chart,
    render_forest_plot,
    render_scan_degradation_chart,
)
from ocr_bench.scorer import ScoreTable
from ocr_bench.types import Capability, FailureKind, MetricResult, NAReason, OcrResult

ENGINES = ("alpha_default", "alpha_scan")
DOCS = ("doc1", "doc2", "doc3")

# Mọi chuỗi dạng `<chữ>_default` / `<chữ>_scan` xuất hiện trong SVG. Đây chính là hình
# dạng của bốn cái tên bịa cũ (`marker_default`, `sovereign_scan`, …), nên quét theo nó
# thì hồi quy sẽ đỏ ngay ở test này chứ không đợi ai mở file hình ra xem.
TEN_PROFILE = re.compile(r"[A-Za-z][A-Za-z0-9]*_(?:default|scan)")


def _bang() -> ScoreTable:
    """Bảng nhỏ nhưng đủ ba trạng thái: chấm được · chưa có nhãn · thiếu năng lực."""
    rows: list[MetricResult] = []
    for i, doc in enumerate(DOCS):
        for j, eng in enumerate(ENGINES):
            rows.append(
                MetricResult(
                    metric="block_f1", engine=eng, doc_id=doc, value=0.5 + 0.1 * i - 0.2 * j
                )
            )
            # `teds`: engine có năng lực, bộ mẫu chưa có nhãn hợp loại → cả hàng không
            # ai vẽ được cột. Đây là hàng dùng để kiểm luật "ra chữ, không ra cột".
            rows.append(
                MetricResult(
                    metric="teds",
                    engine=eng,
                    doc_id=doc,
                    value=None,
                    na_reason=NAReason.NO_GROUND_TRUTH,
                )
            )
            # `img_f1`: một engine đo được, engine kia không khai năng lực — hàng có
            # cột nên khe trống phải mang nhãn lý do của **đúng** engine đó.
            rows.append(
                MetricResult(metric="img_f1", engine=eng, doc_id=doc, value=0.4)
                if eng == "alpha_default"
                else MetricResult(
                    metric="img_f1",
                    engine=eng,
                    doc_id=doc,
                    value=None,
                    na_reason=NAReason.MISSING_CAPABILITY,
                )
            )
    return ScoreTable(tuple(rows))


def _ket_qua() -> list[OcrResult]:
    ra: list[OcrResult] = []
    for eng, giay in zip(ENGINES, (2.0, 8.0)):
        for i, doc in enumerate(DOCS):
            hong = eng == "alpha_scan" and i == 2
            ra.append(
                OcrResult(
                    engine=eng,
                    engine_version="test",
                    doc_id=doc,
                    capabilities=frozenset({Capability.TEXT_MD}),
                    page_sizes=((595.0, 842.0),) * 2,
                    seconds=giay,
                    failed=hong,
                    error="bịa lỗi" if hong else None,
                    failure_kind=FailureKind.TIMEOUT if hong else None,
                )
            )
    return ra


def _ve_xep_hang(p: Path, **kw) -> str:
    render_forest_plot(
        _bang(),
        p,
        engines=list(ENGINES),
        metrics=kw.pop("metrics", ["block_f1", "img_f1", "teds"]),
        tieu_de="Xếp hạng năng lực",
        phu_de="bảng dựng trong test",
        **kw,
    )
    return p.read_text(encoding="utf-8")


def test_moi_ten_engine_trong_hinh_deu_thuoc_bang_dau_vao(tmp_path: Path):
    """Không tên profile nào lọt vào hình mà không có trong `ScoreTable`."""
    svg = _ve_xep_hang(tmp_path / "xh.svg")
    assert set(TEN_PROFILE.findall(svg)) == set(ENGINES)


def test_metric_khong_do_duoc_ra_chu_chu_khong_ra_cot(tmp_path: Path):
    """Hàng `teds` không ai chấm được ⇒ 0 cột, chỉ một nhãn lý do.

    Đếm `<rect`: nền của `mo_svg` một cái, chú giải mỗi engine một cái. Nhiều hơn thế
    nghĩa là có cột được vẽ cho một metric chưa từng đo — kể cả cột rộng 1px, vì
    `bieu_do_cot` kẹp `max(1.0, ...)` nên "cột cao 0" ở đây hiện ra dưới dạng vạch mảnh
    chứ không phải hình chữ nhật rỗng.
    """
    svg = _ve_xep_hang(tmp_path / "teds.svg", metrics=["teds"])
    assert svg.count("<rect") == 1 + len(ENGINES)
    assert "chưa có nhãn" in svg
    assert "0.000" not in svg


def test_khe_trong_mang_nhan_ly_do_cua_dung_engine(tmp_path: Path):
    """Hàng có cột thì engine thiếu năng lực vẫn phải in `N/A` vào khe của nó."""
    svg = _ve_xep_hang(tmp_path / "img.svg", metrics=["img_f1"])
    assert ">N/A<" in svg


def test_hai_lan_render_ra_byte_giong_het(tmp_path: Path):
    a = tmp_path / "a.svg"
    b = tmp_path / "b.svg"
    _ve_xep_hang(a)
    _ve_xep_hang(b)
    assert a.read_bytes() == b.read_bytes()


def test_dau_vao_khong_phai_score_table_thi_raise(tmp_path: Path):
    """`{}` từng là đường đi im lặng tới danh sách engine bịa. Giờ nó phải nổ."""
    with pytest.raises(TypeError):
        render_forest_plot(
            {},
            tmp_path / "x.svg",
            engines=list(ENGINES),
            metrics=["block_f1"],
            tieu_de="t",
            phu_de="p",
        )
    with pytest.raises(TypeError):
        render_scan_degradation_chart({}, tmp_path / "y.svg", metrics=["block_f1"])
    with pytest.raises(ValueError):
        render_failure_distribution_chart([], tmp_path / "z.svg")


def test_engine_ngoai_bang_thi_raise(tmp_path: Path):
    with pytest.raises(ValueError, match="không có trong ScoreTable"):
        render_forest_plot(
            _bang(),
            tmp_path / "x.svg",
            engines=["marker_default"],
            metrics=["block_f1"],
            tieu_de="t",
            phu_de="p",
        )


def test_accuracy_speed_ve_tu_so_do_that(tmp_path: Path):
    bang = _bang()
    perf = {p.engine: p for p in perf_aggregates(perf_rows(_ket_qua()))}
    out = render_accuracy_speed_chart(
        perf,
        {e: bang.cell("block_f1", e) for e in perf},
        tmp_path / "as.svg",
        nhan_y="block_f1 (doclaynet, trần 3)",
    )
    svg = out.read_text(encoding="utf-8")
    assert set(TEN_PROFILE.findall(svg)) == set(ENGINES)
    # Giây/trang có thật: 2.0s / 2 trang và 8.0s / 2 trang.
    assert "1.00s/trang" in svg and "4.00s/trang" in svg
    # Hai hạn chế của trục thời gian phải nằm trên hình, không nằm trong docstring.
    assert "không tách lượt nguội" in svg


def test_accuracy_speed_thieu_diem_thi_raise(tmp_path: Path):
    perf = {p.engine: p for p in perf_aggregates(perf_rows(_ket_qua()))}
    with pytest.raises(ValueError, match="thiếu điểm"):
        render_accuracy_speed_chart(perf, {}, tmp_path / "as.svg", nhan_y="block_f1")


def test_scan_degradation_chi_ghep_cung_ho_engine(tmp_path: Path):
    svg = render_scan_degradation_chart(
        _bang(), tmp_path / "sd.svg", metrics=["block_f1"]
    ).read_text(encoding="utf-8")
    assert "alpha_default → alpha_scan" in svg
    assert set(TEN_PROFILE.findall(svg)) == set(ENGINES)


def test_scan_degradation_thieu_ve_thi_noi_thang_la_thieu(tmp_path: Path):
    """Chỉ có `*_default` thì không vẽ hiệu số — và phải nói ra vì sao."""
    rows = [r for r in _bang().rows if r.engine == "alpha_default"]
    svg = render_scan_degradation_chart(
        ScoreTable(tuple(rows)), tmp_path / "sd1.svg", metrics=["block_f1"]
    ).read_text(encoding="utf-8")
    assert "Không họ engine nào có đủ" in svg
    assert set(TEN_PROFILE.findall(svg)) == {"alpha_default"}


def test_failure_distribution_dem_theo_failure_kind(tmp_path: Path):
    svg = render_failure_distribution_chart(
        _ket_qua(), tmp_path / "fd.svg"
    ).read_text(encoding="utf-8")
    assert "timeout" in svg
    assert "1/3" in svg and "0/3" in svg
    assert set(TEN_PROFILE.findall(svg)) == set(ENGINES)
