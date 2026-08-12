"""B7 — ô bảng: `cell_f1` và `table_recall` (Task 8).

`teds.py` đã trả lời "cây bảng có giống nhau không". Nó **không** trả lời được
"ô nào bị mất", vì một điểm TEDS 0.72 không nói ô nào lệch. `cell_f1` dựng lưới
có rowspan/colspan rồi ghép ô theo (hàng, cột) — sai ở đâu thì đọc ra ở đó.

Không `importorskip`: bộ dựng lưới dùng `html.parser` của stdlib, không dùng
`apted` như `teds.py`.
"""

from __future__ import annotations

import pytest

from ocr_bench.metrics.table_cells import (
    CellF1Metric,
    TableRecallMetric,
    cell_scores,
    dung_luoi,
)
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Box,
    Capability,
    FailureKind,
    NAReason,
    OcrResult,
    OcrTable,
)

_BANG_2x2 = "<table><tr><td>a</td><td>b</td></tr><tr><td>c</td><td>d</td></tr></table>"


def _b(x0: float, y0: float, x1: float, y1: float, page: int = 0) -> Box:
    return Box(x0=x0, y0=y0, x1=x1, y1=y1, page=page)


def _gt(*bang: OcrTable) -> AnnotationGT:
    return AnnotationGT(doc_id="d1", tables=tuple(bang))


def _kq(*bang: OcrTable, caps: frozenset[Capability] | None = None) -> OcrResult:
    return OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.TABLE_HTML}) if caps is None else caps,
        tables=tuple(bang),
    )


# --- dựng lưới ---------------------------------------------------------------


def test_luoi_phang_dung_toa_do() -> None:
    assert dung_luoi(_BANG_2x2) == {
        (0, 0): "a",
        (0, 1): "b",
        (1, 0): "c",
        (1, 1): "d",
    }


def test_colspan_chiem_dung_so_cot() -> None:
    """Ô `colspan=2` chiếm hai toạ độ. Bỏ qua colspan thì mọi ô bên phải nó lệch
    một cột, và bảng đúng bị chấm sai toàn bộ hàng."""
    html = (
        "<table><tr><td colspan='2'>tiêu đề</td></tr>"
        "<tr><td>a</td><td>b</td></tr></table>"
    )
    assert dung_luoi(html) == {
        (0, 0): "tiêu đề",
        (0, 1): "tiêu đề",
        (1, 0): "a",
        (1, 1): "b",
    }


def test_rowspan_day_o_hang_duoi_sang_phai() -> None:
    html = (
        "<table><tr><td rowspan='2'>gộp</td><td>b</td></tr>"
        "<tr><td>c</td></tr></table>"
    )
    assert dung_luoi(html) == {
        (0, 0): "gộp",
        (0, 1): "b",
        (1, 0): "gộp",
        (1, 1): "c",
    }


def test_th_cung_la_o() -> None:
    html = "<table><tr><th>H</th></tr><tr><td>v</td></tr></table>"
    assert dung_luoi(html) == {(0, 0): "H", (1, 0): "v"}


def test_noi_dung_duoc_chuan_hoa_khoang_trang() -> None:
    """`<td>  a\\n b </td>` và `<td>a b</td>` là cùng một ô. Không chuẩn hoá thì
    metric đang chấm cách engine xuống dòng HTML, không phải nội dung bảng."""
    a = dung_luoi("<table><tr><td>  a\n  b </td></tr></table>")
    b = dung_luoi("<table><tr><td>a b</td></tr></table>")
    assert a == b == {(0, 0): "a b"}


# --- cell_f1 -----------------------------------------------------------------


def test_metric_controls_are_ordered() -> None:
    """Cùng dạng control mà kế hoạch đòi: khít = 1.0, rồi giảm dần."""
    nhan = _gt(OcrTable(html=_BANG_2x2))
    khit = _kq(OcrTable(html=_BANG_2x2))
    mot_phan = _kq(
        OcrTable(
            html="<table><tr><td>a</td><td>b</td></tr>"
            "<tr><td>c</td><td>SAI</td></tr></table>"
        )
    )
    nang = _kq(OcrTable(html="<table><tr><td>x</td></tr></table>"))
    diem = [CellF1Metric().score(nhan, x).value for x in (khit, mot_phan, nang)]
    assert diem[0] == 1.0
    assert diem[0] > diem[1] > diem[2]


def test_cell_f1_o_thieu_la_fn_o_thua_la_fp() -> None:
    f1, ct = cell_scores(
        [_BANG_2x2],
        ["<table><tr><td>a</td><td>b</td></tr><tr><td>c</td></tr></table>"],
    )
    assert (ct["tp"], ct["fp"], ct["fn"]) == (3, 0, 1)
    assert f1 == pytest.approx(2 * 3 / (2 * 3 + 0 + 1))


def test_cell_f1_dung_noi_dung_dung_o_sai_vi_tri_van_la_sai() -> None:
    """Chuyển vị bảng giữ nguyên tập nội dung nhưng đổi hết ý nghĩa. Ghép theo
    nội dung mà bỏ toạ độ thì bảng chuyển vị được 1.0."""
    f1, _ = cell_scores(
        [_BANG_2x2],
        ["<table><tr><td>a</td><td>c</td></tr><tr><td>b</td><td>d</td></tr></table>"],
    )
    assert f1 < 1.0


def test_nhan_khong_co_bang_va_engine_cung_khong_thi_na() -> None:
    ket = CellF1Metric().score(_gt(), _kq())
    assert ket.value is None
    assert ket.na_reason is NAReason.NO_GROUND_TRUTH


def test_nhan_khong_co_bang_ma_engine_co_thi_phat_0() -> None:
    ket = CellF1Metric().score(_gt(), _kq(OcrTable(html=_BANG_2x2)))
    assert ket.value == 0.0


def test_thieu_nang_luc_table_html_thi_na() -> None:
    doan = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md="x",
    )
    ket = CellF1Metric().score(_gt(OcrTable(html=_BANG_2x2)), doan)
    assert ket.na_reason is NAReason.MISSING_CAPABILITY


def test_engine_hong_thi_na() -> None:
    hong = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.TABLE_HTML}),
        failed=True,
        error="nổ",
        failure_kind=FailureKind.ENGINE_ERROR,
    )
    assert (
        CellF1Metric().score(_gt(OcrTable(html=_BANG_2x2)), hong).na_reason
        is NAReason.ENGINE_FAILED
    )


def test_sai_loai_nhan_thi_na() -> None:
    ket = CellF1Metric().score(AssertionGT(doc_id="d1"), _kq(OcrTable(html=_BANG_2x2)))
    assert ket.na_reason is NAReason.WRONG_GT_KIND


# --- table_recall: hai trạng thái thiếu, không gộp ---------------------------


def test_table_recall_khop_theo_iou() -> None:
    nhan = _gt(OcrTable(html=_BANG_2x2, box=_b(0.1, 0.1, 0.9, 0.5)))
    doan = _kq(OcrTable(html=_BANG_2x2, box=_b(0.1, 0.1, 0.9, 0.5)))
    ket = TableRecallMetric().score(nhan, doan)
    assert ket.value == 1.0


def test_table_recall_nhan_khong_co_box_la_thieu_nhan() -> None:
    """Không có `Capability.TABLE_BBOX` trong repo này. Nhãn có bảng nhưng không
    có khung thì **bộ mẫu** thiếu, không phải engine thiếu — `NO_GROUND_TRUTH`."""
    nhan = _gt(OcrTable(html=_BANG_2x2, box=None))
    doan = _kq(OcrTable(html=_BANG_2x2, box=_b(0.1, 0.1, 0.9, 0.5)))
    ket = TableRecallMetric().score(nhan, doan)
    assert ket.value is None
    assert ket.na_reason is NAReason.NO_GROUND_TRUTH


def test_table_recall_engine_khong_co_box_la_thieu_nang_luc() -> None:
    """Engine trả HTML bảng nhưng không trả khung: nó **không hứa** định vị bảng.
    Chấm 0 ở đây là phạt engine vì một năng lực nó chưa từng khai. Hai trạng thái
    này khác nhau và không bao giờ được gộp — đó là cả lý do metric có hai nhánh
    N/A riêng."""
    nhan = _gt(OcrTable(html=_BANG_2x2, box=_b(0.1, 0.1, 0.9, 0.5)))
    doan = _kq(OcrTable(html=_BANG_2x2, box=None))
    ket = TableRecallMetric().score(nhan, doan)
    assert ket.value is None
    assert ket.na_reason is NAReason.MISSING_CAPABILITY


def test_hai_trang_thai_thieu_khong_tra_cung_mot_ly_do() -> None:
    thieu_nhan = TableRecallMetric().score(
        _gt(OcrTable(html=_BANG_2x2, box=None)),
        _kq(OcrTable(html=_BANG_2x2, box=_b(0.1, 0.1, 0.9, 0.5))),
    )
    thieu_engine = TableRecallMetric().score(
        _gt(OcrTable(html=_BANG_2x2, box=_b(0.1, 0.1, 0.9, 0.5))),
        _kq(OcrTable(html=_BANG_2x2, box=None)),
    )
    assert thieu_nhan.na_reason is not thieu_engine.na_reason
