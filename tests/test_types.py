"""Test hợp đồng dữ liệu.

Ba nhóm test đầu tiên bảo vệ đúng ba cái bẫy tìm thấy ở A0. Chúng phải tồn tại
TRƯỚC khi có engine thật, vì cả ba đều thuộc loại lỗi không bao giờ ném exception —
chúng chỉ làm bảng xếp hạng sai một cách rất thuyết phục.
"""

from __future__ import annotations

import pytest

from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Box,
    Capability,
    MetricResult,
    NAReason,
    OcrBlock,
    BlockType,
    OcrImage,
    OcrResult,
    ReadingOrder,
    ScanLabel,
    TextPresence,
)

A4_W, A4_H = 595.28, 841.68


# --------------------------------------------------------------------------
# Bẫy 1 — trục y ngược nhau giữa các engine
# --------------------------------------------------------------------------


def test_y_up_box_o_nua_tren_van_o_nua_tren():
    """pdf-inspector: gốc dưới-trái, y hướng lên.

    Tiêu đề của `sample_ttf.pdf` đo thật ở y=791.18 trên trang cao 841.68 — tức là
    sát đỉnh. Sau quy đổi nó phải nằm ở nửa TRÊN. Quên lật trục thì nó rơi xuống
    đáy và IoU với DocLayNet ra gần 0, trông hệt như "engine tách ảnh kém".
    """
    box = Box.from_absolute(
        page=0,
        x0=72,
        y0=780.0,
        x1=520,
        y1=800.0,
        page_width=A4_W,
        page_height=A4_H,
        y_axis="up",
    )
    assert box.y1 < 0.5, f"tiêu đề sát đỉnh trang nhưng ra y={box.y0:.3f}..{box.y1:.3f}"
    assert box.y0 == pytest.approx(1 - 800.0 / A4_H, abs=1e-9)
    assert box.y1 == pytest.approx(1 - 780.0 / A4_H, abs=1e-9)


def test_y_down_va_y_up_cung_mo_ta_mot_vung_thi_trung_nhau():
    """Cùng một dải ngang trên trang, mô tả bằng hai hệ, phải cho cùng một Box."""
    down = Box.from_absolute(
        page=0, x0=72, y0=41.68, x1=520, y1=61.68,
        page_width=A4_W, page_height=A4_H, y_axis="down",
    )
    up = Box.from_absolute(
        page=0, x0=72, y0=A4_H - 61.68, x1=520, y1=A4_H - 41.68,
        page_width=A4_W, page_height=A4_H, y_axis="up",
    )
    assert down.iou(up) == pytest.approx(1.0, abs=1e-9)


def test_page_box_khong_bat_dau_tu_goc():
    """Nhánh force_ocr của Marker lấy page box từ pdfium.get_bbox(), không đảm bảo
    bắt đầu từ (0,0). Adapter phải truyền page_x0/page_y0, không giả định."""
    box = Box.from_absolute(
        page=0, x0=110, y0=60, x1=210, y1=160,
        page_width=400, page_height=400,
        y_axis="down", page_x0=10, page_y0=10,
    )
    assert (box.x0, box.y0, box.x1, box.y1) == pytest.approx((0.25, 0.125, 0.5, 0.375))


def test_box_tu_dung_bang_toa_do_tho_thi_no():
    with pytest.raises(ValueError, match="chưa được chuẩn hoá"):
        Box(page=0, x0=72, y0=100, x1=520, y1=200)


def test_box_lon_nguoc_thi_no():
    with pytest.raises(ValueError, match="lộn ngược"):
        Box(page=0, x0=0.8, y0=0.1, x1=0.2, y1=0.3)


def test_kich_thuoc_trang_khong_hop_le_thi_no():
    with pytest.raises(ValueError, match="không hợp lệ"):
        Box.from_absolute(
            page=0, x0=0, y0=0, x1=1, y1=1,
            page_width=0, page_height=A4_H, y_axis="down",
        )


def test_iou_khong_giao_nhau_bang_0():
    a = Box(page=0, x0=0.0, y0=0.0, x1=0.2, y1=0.2)
    assert a.iou(Box(page=0, x0=0.5, y0=0.5, x1=0.7, y1=0.7)) == 0.0
    assert a.iou(Box(page=0, x0=0.0, y0=0.5, x1=0.2, y1=0.7)) == 0.0


def test_iou_khac_trang_luon_bang_0():
    a = Box(page=0, x0=0.1, y0=0.1, x1=0.9, y1=0.9)
    b = Box(page=1, x0=0.1, y0=0.1, x1=0.9, y1=0.9)
    assert a.iou(b) == 0.0
    assert a.iou(Box(page=0, x0=0.1, y0=0.1, x1=0.9, y1=0.9)) == pytest.approx(1.0)


# --------------------------------------------------------------------------
# Bẫy 2 — số trang 0-based hay 1-based
# --------------------------------------------------------------------------


def test_trang_am_bi_tu_choi():
    """pdf-inspector trả 0-based ở classify_pdf và 1-based ở process_pdf trên cùng
    một file. Adapter nào trừ nhầm sẽ tạo ra trang -1 và bị chặn ở đây."""
    with pytest.raises(ValueError, match="0-based"):
        Box(page=-1, x0=0.0, y0=0.0, x1=1.0, y1=1.0)


def test_scan_label_bat_buoc_ghi_ten_api():
    """classify_pdf() và extract_pages_markdown() cho hai câu trả lời trái ngược
    nhau trên cùng một file — không ghi lại hàm nào thì con số vô nghĩa."""
    with pytest.raises(TypeError):
        ScanLabel(is_scanned=True)  # type: ignore[call-arg]
    ok = ScanLabel(is_scanned=True, api="classify_pdf", confidence=0.8)
    assert ok.api == "classify_pdf"


# --------------------------------------------------------------------------
# Bẫy 3 — năng lực phải khai, không được suy ra từ dữ liệu
# --------------------------------------------------------------------------


def test_tra_du_lieu_ma_khong_khai_nang_luc_thi_no():
    with pytest.raises(ValueError, match="không khai báo image_bbox"):
        OcrResult(
            engine="x",
            engine_version="1",
            doc_id="d",
            capabilities=frozenset({Capability.TEXT_MD}),
            text_md="hi",
            images=(OcrImage(box=Box(page=0, x0=0.1, y0=0.1, x1=0.2, y1=0.2)),),
        )


def test_khai_nang_luc_ma_khong_tim_thay_gi_van_hop_le():
    """Khai IMAGE_BBOX + images rỗng = "chạy rồi, trang này không có ảnh".
    Khác hẳn với không khai = "không bao giờ biết được". Gộp hai chuyện này là cách
    nhanh nhất để engine làm ít việc hơn lại trông giỏi hơn."""
    r = OcrResult(
        engine="x",
        engine_version="1",
        doc_id="d",
        capabilities=frozenset({Capability.TEXT_MD, Capability.IMAGE_BBOX}),
        text_md="hi",
    )
    assert r.images == ()
    assert Capability.IMAGE_BBOX in r.capabilities


def test_failed_phai_co_error():
    with pytest.raises(ValueError, match="failed=True"):
        OcrResult(
            engine="x", engine_version="1", doc_id="d",
            capabilities=frozenset(), failed=True,
        )


def test_failed_thi_khong_bi_kiem_nang_luc():
    """Engine hỏng giữa chừng có thể trả về mảnh dữ liệu dở dang — không được biến
    nó thành ValueError, vì thế FailRate sẽ mất luôn ca đó."""
    r = OcrResult(
        engine="x", engine_version="1", doc_id="d",
        capabilities=frozenset(), text_md="dở dang",
        failed=True, error="OOM",
    )
    assert r.failed and r.text_md == "dở dang"


# --------------------------------------------------------------------------
# MetricResult: N/A không bao giờ là 0
# --------------------------------------------------------------------------


def test_na_phai_neu_ly_do():
    with pytest.raises(ValueError, match="phải nêu na_reason"):
        MetricResult(metric="m", engine="e", doc_id="d", value=None)


def test_co_diem_thi_khong_duoc_kem_ly_do_na():
    with pytest.raises(ValueError, match="không được kèm na_reason"):
        MetricResult(
            metric="m", engine="e", doc_id="d",
            value=0.0, na_reason=NAReason.ENGINE_FAILED,
        )


def test_diem_0_khac_na():
    zero = MetricResult(metric="m", engine="e", doc_id="d", value=0.0)
    na = MetricResult(
        metric="m", engine="e", doc_id="d",
        value=None, na_reason=NAReason.MISSING_CAPABILITY,
    )
    assert not zero.is_na
    assert na.is_na


# --------------------------------------------------------------------------
# Ground truth: giữ CẢ HAI dạng
# --------------------------------------------------------------------------


def test_hai_dang_ground_truth_cung_ton_tai():
    ann = AnnotationGT(
        doc_id="d",
        text="xin chào",
        blocks=(OcrBlock(block_type=BlockType.HEADING, level=1, text="Chương 1"),),
        images=(Box(page=0, x0=0.1, y0=0.1, x1=0.4, y1=0.4),),
        human_ceiling={"imgf1": 0.85},
    )
    asr = AssertionGT(
        doc_id="d",
        tests=(TextPresence(needle="xin chào"), ReadingOrder(before="a", after="b")),
    )
    assert ann.human_ceiling["imgf1"] == 0.85
    assert {t.kind for t in asr.tests} == {"text_presence", "reading_order"}
