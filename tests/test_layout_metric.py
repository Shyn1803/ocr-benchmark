"""B3b — bố cục: `block_f1` và `type_f1` (Task 8).

Không `importorskip`: `layout.py` chỉ dùng số học của `Box` và bộ ghép thuần Python
ở `metrics/matching.py`.

Hai metric chứ không một, cùng lý do đã ghi ở `imgf1.py`: `block_f1` trả lời "tìm
đúng bao nhiêu khối", `type_f1` trả lời "gọi tên khối có đúng không". Engine tách
khối chuẩn nhưng gọi mọi thứ là ``TEXT`` sẽ có `block_f1` = 1.0 và `type_f1` thấp —
gộp một cột là mất đúng chẩn đoán đó.
"""

from __future__ import annotations

import pytest

from ocr_bench.metrics.layout import (
    BlockF1Metric,
    TypeF1Metric,
    layout_scores,
)
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    BlockType,
    Box,
    Capability,
    FailureKind,
    NAReason,
    OcrBlock,
    OcrResult,
)


def _b(x0: float, y0: float, x1: float, y1: float, page: int = 0) -> Box:
    return Box(x0=x0, y0=y0, x1=x1, y1=y1, page=page)


def _hang(i: int, cao: float = 0.08) -> Box:
    """Băng ngang thứ `i` — mô hình tài liệu một cột."""
    y = 0.05 + i * 0.1
    return _b(0.1, y, 0.9, y + cao)


def _khoi(box: Box, loai: BlockType = BlockType.TEXT) -> OcrBlock:
    return OcrBlock(block_type=loai, box=box)


def _gt(*khoi: OcrBlock) -> AnnotationGT:
    return AnnotationGT(doc_id="d1", blocks=tuple(khoi))


def _kq(*khoi: OcrBlock, caps: frozenset[Capability] | None = None) -> OcrResult:
    return OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.BLOCK_BBOX}) if caps is None else caps,
        blocks=tuple(khoi),
    )


# --- controls: thứ tự điểm phải đúng chiều -----------------------------------


def _bo_ba() -> tuple[AnnotationGT, OcrResult, OcrResult, OcrResult]:
    """Nhãn + ba mức đầu ra: khít, lệch một phần, hỏng nặng.

    Dùng chung cho control của cả hai metric bố cục. `severe` **có** trả box (không
    phải rỗng) — nếu không thì nó rơi vào nhánh N/A và control không kiểm được gì.
    """
    nhan = _gt(
        _khoi(_hang(0), BlockType.HEADING),
        _khoi(_hang(1), BlockType.TEXT),
        _khoi(_hang(2), BlockType.TABLE),
    )
    khit = _kq(
        _khoi(_hang(0), BlockType.HEADING),
        _khoi(_hang(1), BlockType.TEXT),
        _khoi(_hang(2), BlockType.TABLE),
    )
    # Một khối lệch nhẹ (vẫn ghép được), một khối bị bỏ, một khối đúng.
    mot_phan = _kq(
        _khoi(_b(0.1, 0.045, 0.9, 0.126), BlockType.HEADING),
        _khoi(_hang(1), BlockType.TEXT),
    )
    # Một box trùm cả trang: không ghép được với box nào ở IoU ≥ 0.5.
    nang = _kq(_khoi(_b(0.0, 0.0, 1.0, 1.0), BlockType.TEXT))
    return nhan, khit, mot_phan, nang


@pytest.mark.parametrize("metric", [BlockF1Metric(), TypeF1Metric()])
def test_metric_controls_are_ordered(metric) -> None:
    nhan, khit, mot_phan, nang = _bo_ba()
    diem = [metric.score(nhan, x).value for x in (khit, mot_phan, nang)]
    assert diem[0] == 1.0
    assert diem[0] > diem[1] > diem[2]


# --- block_f1: không xét type ------------------------------------------------


def test_block_f1_bo_qua_type() -> None:
    """Cắt khối đúng chỗ nhưng gọi sai tên vẫn là cắt đúng chỗ."""
    nhan = _gt(_khoi(_hang(0), BlockType.HEADING), _khoi(_hang(1), BlockType.TABLE))
    doan = _kq(_khoi(_hang(0), BlockType.TEXT), _khoi(_hang(1), BlockType.TEXT))
    assert BlockF1Metric().score(nhan, doan).value == 1.0


def test_block_f1_phat_box_thua() -> None:
    nhan = _gt(_khoi(_hang(0)))
    doan = _kq(_khoi(_hang(0)), _khoi(_hang(5)))
    ket = BlockF1Metric().score(nhan, doan)
    assert ket.value == pytest.approx(2 / 3)
    assert (ket.detail["tp"], ket.detail["fp"], ket.detail["fn"]) == (1, 1, 0)


# --- type_f1: kế toán FN/FP -------------------------------------------------


def test_type_f1_goi_sai_ten_bi_tinh_ca_fp_lan_fn() -> None:
    """Một cặp ghép đúng vị trí nhưng sai type là **hai** lỗi, không phải một:
    type nhãn mất một dương tính (FN), type đoán nhận một dương tính giả (FP)."""
    nhan = _gt(_khoi(_hang(0), BlockType.TABLE))
    doan = _kq(_khoi(_hang(0), BlockType.TEXT))
    ket = TypeF1Metric().score(nhan, doan)
    assert ket.value == 0.0
    theo_type = ket.detail["theo_type"]
    assert theo_type["table"]["fn"] == 1
    assert theo_type["text"]["fp"] == 1


def test_type_f1_macro_chi_tren_type_co_trong_nhan() -> None:
    """Engine bịa thêm một type nhãn không có thì đó là FP, **không** phải một
    dòng mới trong mẫu số macro. Cho type bịa vào mẫu số là để engine tự chọn
    mẫu số của chính nó: bịa càng nhiều type lạ, mỗi type sai càng ít trọng số.

    Hệ quả phải nói thẳng: khối bịa ra **không** bị `type_f1` phạt chút nào. Nó bị
    phạt ở `block_f1` (một FP). Đây là lý do hai cột luôn đọc cùng nhau; khẳng
    định cuối của test này chốt rằng hình phạt có tồn tại, chỉ là ở cột kia.
    """
    nhan = _gt(_khoi(_hang(0), BlockType.TEXT), _khoi(_hang(1), BlockType.TEXT))
    doan = _kq(
        _khoi(_hang(0), BlockType.TEXT),
        _khoi(_hang(1), BlockType.TEXT),
        _khoi(_hang(7), BlockType.FORMULA),
    )
    ket = TypeF1Metric().score(nhan, doan)
    assert ket.detail["types_macro"] == ["text"]
    # `formula` xuất hiện trong kế toán (1 FP) nhưng không vào mẫu số macro.
    assert ket.detail["theo_type"]["formula"]["fp"] == 1
    assert ket.value == 1.0
    assert BlockF1Metric().score(nhan, doan).value == pytest.approx(4 / 5)


def test_type_f1_khoi_nhan_khong_ghep_duoc_la_fn_cua_type_nhan() -> None:
    nhan = _gt(_khoi(_hang(0), BlockType.TEXT), _khoi(_hang(1), BlockType.TABLE))
    doan = _kq(_khoi(_hang(0), BlockType.TEXT))
    ket = TypeF1Metric().score(nhan, doan)
    assert ket.detail["theo_type"]["table"] == {"tp": 0, "fp": 0, "fn": 1}
    # macro trên {text: 1.0, table: 0.0}
    assert ket.value == 0.5


# --- ghép bipartite, không tham lam -----------------------------------------


def test_ghep_toi_uu_chu_khong_tham_lam() -> None:
    """Lập luận "ở ngưỡng ≥ 0.5 phép ghép là duy nhất" của `imgf1` có tiền đề
    **các box nhãn rời nhau**. Với block thì tiền đề đó sai: caption nằm trong
    picture, tiêu đề mục nằm trong khung mục. Phản ví dụ nguyên văn ở docstring
    của `metrics/matching.py` — tham lam ra 1 cặp, tối ưu ra 2, ở đúng ngưỡng
    mặc định 0.5."""
    nhan = [_b(0.0, 0.0, 0.4, 0.5), _b(0.0, 0.0, 0.4, 0.3)]
    doan = [_b(0.0, 0.0, 0.4, 0.5), _b(0.0, 0.0, 0.75, 0.5)]
    f1, _, ct = layout_scores(nhan, doan)
    assert ct["tp"] == 2
    assert f1 == 1.0


def test_ghep_khong_phu_thuoc_thu_tu_dau_vao() -> None:
    nhan = [_hang(0), _hang(1), _hang(2)]
    doan = [_hang(2), _hang(0), _hang(1)]
    f1, _, _ = layout_scores(nhan, doan)
    assert f1 == 1.0


# --- cổng N/A ----------------------------------------------------------------


def test_thieu_nang_luc_thi_na_chu_khong_phai_0() -> None:
    nhan = _gt(_khoi(_hang(0)))
    doan = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md="x",
    )
    ket = BlockF1Metric().score(nhan, doan)
    assert ket.value is None
    assert ket.na_reason is NAReason.MISSING_CAPABILITY


def test_nhan_khong_co_khoi_va_engine_cung_khong_thi_na() -> None:
    ket = BlockF1Metric().score(_gt(), _kq())
    assert ket.value is None
    assert ket.na_reason is NAReason.NO_GROUND_TRUTH


def test_nhan_khong_co_khoi_ma_engine_co_thi_phat_0() -> None:
    """Dương tính giả là lỗi thật — cùng quyết định 3 của `imgf1.py`."""
    ket = BlockF1Metric().score(_gt(), _kq(_khoi(_hang(0))))
    assert ket.value == 0.0


def test_sai_loai_nhan_thi_na() -> None:
    ket = BlockF1Metric().score(AssertionGT(doc_id="d1"), _kq(_khoi(_hang(0))))
    assert ket.na_reason is NAReason.WRONG_GT_KIND


def test_engine_hong_thi_na_chu_khong_phai_0() -> None:
    hong = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.BLOCK_BBOX}),
        failed=True,
        error="nổ",
        failure_kind=FailureKind.ENGINE_ERROR,
    )
    ket = BlockF1Metric().score(_gt(_khoi(_hang(0))), hong)
    assert ket.value is None
    assert ket.na_reason is NAReason.ENGINE_FAILED


def test_khoi_khong_co_box_khong_duoc_dem_la_du_doan() -> None:
    """`OcrBlock.box` được phép `None` (engine có chữ nhưng không có toạ độ). Khối
    không có khung thì không ghép được — bỏ khỏi cả tử lẫn mẫu, chứ đếm nó vào
    `n_doan` là phạt engine vì một khối nó chưa từng định vị."""
    nhan = _gt(_khoi(_hang(0)))
    doan = _kq(
        _khoi(_hang(0)),
        OcrBlock(block_type=BlockType.TEXT, box=None, text="không có khung"),
    )
    ket = BlockF1Metric().score(nhan, doan)
    assert ket.value == 1.0
    assert ket.detail["n_doan"] == 1
