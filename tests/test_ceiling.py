"""Trần đo được phải suy từ nhãn, và phải khớp số đếm tay.

Test ở đây dùng ground truth **giả** dựng tại chỗ: trần là một tính chất của bộ nhãn,
nên nó phải kiểm được mà không cần bộ mẫu thật nằm trên đĩa.
"""

from __future__ import annotations

from ocr_bench.ceiling import (
    NGUONG_DO_DUOC,
    bang_tran,
    du_lieu_tran,
    thu_tu_metric,
    tran_do_duoc,
)
from ocr_bench.types import (
    AnnotationGT,
    Assertion,
    AssertionGT,
    Box,
    OcrBlock,
    BlockType,
    OcrTable,
    TextPresence,
)

MOC = "2026-08-12T00:00:00+07:00"


def _khoi(y: float, loai: BlockType = BlockType.TEXT) -> OcrBlock:
    return OcrBlock(block_type=loai, box=Box(page=0, x0=0.0, y0=y, x1=1.0, y1=y + 0.1))


def _gt_nhan() -> dict[str, AnnotationGT]:
    """4 tài liệu: đủ khối · có ảnh · có bảng-không-ô · rỗng hoàn toàn."""
    return {
        "a": AnnotationGT(
            doc_id="a",
            blocks=(
                _khoi(0.0, BlockType.TITLE),
                _khoi(0.2, BlockType.HEADING),
                _khoi(0.4),
            ),
        ),
        "b": AnnotationGT(
            doc_id="b",
            blocks=(_khoi(0.0),),
            images=(Box(page=0, x0=0.0, y0=0.0, x1=0.4, y1=0.4),),
        ),
        "c": AnnotationGT(
            doc_id="c",
            blocks=(_khoi(0.0),),
            tables=(
                OcrTable(html="", box=Box(page=0, x0=0.0, y0=0.0, x1=0.9, y1=0.9)),
            ),
        ),
        "d": AnnotationGT(doc_id="d"),
    }


def _gt_khang_dinh() -> dict[str, AssertionGT]:
    def kd(i: int) -> Assertion:
        return TextPresence(assertion_id=f"t{i}", needle="x")

    return {
        "p": AssertionGT(doc_id="p", tests=(kd(1), kd(2))),
        "q": AssertionGT(doc_id="q", tests=(kd(3),)),
        "r": AssertionGT(doc_id="r", tests=()),
    }


def test_tran_khop_so_dem_tay():
    t = tran_do_duoc(_gt_nhan(), _gt_khang_dinh())

    # 3 tài liệu có khối; "d" rỗng cả hai vế → N/A đối xứng.
    assert t["block_f1"].n_toi_da == 3
    assert t["type_f1"].n_toi_da == 3
    # Chỉ "b" có nhãn ảnh.
    assert t["img_f1"].n_toi_da == 1
    assert t["img_iou"].n_toi_da == 1
    # Chỉ "c" có khung bảng.
    assert t["table_recall"].n_toi_da == 1
    # Chỉ "a" có hai cấp tiêu đề (TITLE + HEADING).
    assert t["heading"].n_toi_da == 1
    # 2/3 tài liệu khẳng định mang loại `text_presence`.
    assert t["assert_text_presence"].n_toi_da == 2
    assert t["assert_math_presence"].n_toi_da == 0


def test_tran_0_khi_nhan_thieu_hoan_toan():
    """Nhãn không có chữ / không có thứ tự đọc / bảng không có ô ⇒ trần 0."""
    t = tran_do_duoc(_gt_nhan(), _gt_khang_dinh())

    for m in ("cer", "wer", "diacritics_acc", "nid", "teds", "teds_struct", "cell_f1"):
        assert t[m].n_toi_da == 0, m
        assert t[m].bac == "tran_0", m
        assert t[m].ly_do, f"{m} trần 0 mà không nói vì sao"


def test_ly_do_liet_ke_moi_luat_chan():
    """`cell_f1` bị chặn bởi hai luật khác nhau — cả hai phải có mặt.

    Chết khi revert: in mỗi lý do đông nhất thì trần 0 của `cell_f1` đọc như "bộ mẫu
    ít bảng", che mất chuyện bảng có thật cũng không có nội dung ô.
    """
    t = tran_do_duoc(_gt_nhan(), _gt_khang_dinh())
    ly_do = t["cell_f1"].ly_do
    assert "không có bảng" in ly_do
    assert "không bảng nào có nội dung ô" in ly_do


def test_nua_corpus_suy_tu_gt_kinds_khong_gan_tay():
    t = tran_do_duoc(_gt_nhan(), _gt_khang_dinh())
    assert t["block_f1"].nua_corpus == "doclaynet"
    assert t["assert_text_presence"].nua_corpus == "olmocr"
    # Mẫu số là cỡ nửa corpus tương ứng, không phải tổng hai nửa.
    assert t["block_f1"].n_ung_vien == 4
    assert t["assert_text_presence"].n_ung_vien == 3


def test_moi_metric_dang_ky_deu_co_mat():
    """Thêm metric mà quên bảng trần thì nó vắng mặt lặng lẽ — chặn ở đây."""
    from ocr_bench import registry

    t = tran_do_duoc(_gt_nhan(), _gt_khang_dinh())
    assert sorted(t) == registry.list_metrics()


def test_thu_tu_theo_bac_roi_tran_giam_dan():
    t = tran_do_duoc(_gt_nhan(), _gt_khang_dinh())
    thu_tu = thu_tu_metric(t)
    bac = [t[m].bac for m in thu_tu]
    assert bac == sorted(bac, key=("do_duoc", "mong", "tran_0").index)
    # Trong cùng một bậc, trần giảm dần.
    for truoc, sau in zip(thu_tu, thu_tu[1:]):
        if t[truoc].bac == t[sau].bac:
            assert t[truoc].n_toi_da >= t[sau].n_toi_da


def test_bac_chi_mot_nguong():
    """1..NGUONG-1 đều là `mong`; không có khe nào không tên."""
    t = tran_do_duoc(_gt_nhan(), _gt_khang_dinh())
    for x in t.values():
        if x.n_toi_da == 0:
            assert x.bac == "tran_0"
        elif x.n_toi_da < NGUONG_DO_DUOC:
            assert x.bac == "mong"
        else:
            assert x.bac == "do_duoc"


def test_artifact_tat_dinh_va_khong_nhac_engine():
    t = tran_do_duoc(_gt_nhan(), _gt_khang_dinh())
    kw = {"n_doclaynet": 4, "n_olmocr": 3, "generated_at": MOC}

    js_a = du_lieu_tran(t, **kw)
    js_b = du_lieu_tran(t, **kw)
    md_a = bang_tran(t, **kw)
    md_b = bang_tran(t, **kw)

    assert js_a == js_b
    assert md_a == md_b
    # Trần là tính chất của nhãn: không tên engine nào được lọt vào.
    for van_ban in (js_a, md_a):
        for ten in ("docling", "opendataloader", "marker", "sovereign", "__tran"):
            assert ten not in van_ban
