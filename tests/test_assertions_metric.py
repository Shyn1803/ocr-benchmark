"""B5 — `metrics/assertions.py`.

Ba thứ được canh ở đây, theo thứ tự quan trọng:

1. **Không tồn tại metric gộp sáu loại** (AC-02) — canh bằng test đọc `Metric` con
   cháu, không bằng lời dặn trong docstring.
2. Cổng N/A: sai loại nhãn → `WRONG_GT_KIND` (AC-03); không có khẳng định loại này
   → `NO_GROUND_TRUTH`, **không** phải 0.0.
3. Từng loại: ít nhất một ca đạt và một ca trượt.
"""

from __future__ import annotations

import pytest

from ocr_bench.metrics.assertions import (
    METRIC_THEO_LOAI,
    AssertionMetric,
    BaselineMetric,
    MathPresenceMetric,
    ReadingOrderMetric,
    TableRelationMetric,
    TextAbsenceMetric,
    TextPresenceMetric,
    chuan_hoa_latex,
    co_mat,
    cua_so,
    doc_bang,
    tim_moi_vi_tri,
)
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Baseline,
    Capability,
    FailureKind,
    MathPresence,
    NAReason,
    OcrResult,
    ReadingOrder,
    TableRelation,
    TextAbsence,
    TextPresence,
)

pytest.importorskip("rapidfuzz")


def kq(text: str | None = "", *, failed: bool = False) -> OcrResult:
    return OcrResult(
        engine="thu",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md=text,
        failed=failed,
        error="hong" if failed else None,
        failure_kind=FailureKind.ENGINE_ERROR if failed else None,
    )


def gt(*tests) -> AssertionGT:
    return AssertionGT(doc_id="d1", tests=tuple(tests))


# ---------------------------------------------------------------------------
# AC-02 — không có đường nào ra một con số gộp
# ---------------------------------------------------------------------------


def test_moi_loai_mot_lop_va_moi_lop_mot_ten():
    assert len(METRIC_THEO_LOAI) == 6
    ten = {m.name for m in METRIC_THEO_LOAI.values()}
    assert len(ten) == 6, "hai lớp trùng tên sẽ chồng điểm lên nhau trong bảng"
    assert all(t.startswith("assert_") for t in ten)


def test_khong_lop_nao_cham_khang_dinh_ngoai_loai_cua_no():
    """Cốt lõi AC-02: cấu trúc không cho phép trộn.

    Một tài liệu mang đủ sáu loại; mỗi metric chỉ được nhìn thấy phần của mình.
    """
    tat_ca = gt(
        TextPresence(needle="a"),
        TextAbsence(needle="b"),
        ReadingOrder(before="a", after="b"),
        MathPresence(latex="x"),
        TableRelation(cell="c"),
        Baseline(),
    )
    for lop in METRIC_THEO_LOAI.values():
        r = lop().score(tat_ca, kq("a b"))
        assert r.detail["n_khang_dinh"] == 1, f"{lop.name} nhìn thấy loại khác"


def test_khong_co_lop_nao_gop_nhieu_loai():
    """Nếu ai đó thêm một metric nhận >1 loại, test này phải đỏ."""
    for lop in AssertionMetric.__subclasses__():
        assert isinstance(lop.loai, str), f"{lop.__name__} khai `loai` không phải chuỗi"
        assert lop.loai in METRIC_THEO_LOAI, f"{lop.__name__} nằm ngoài bảng tra"


# ---------------------------------------------------------------------------
# AC-03 + cổng N/A
# ---------------------------------------------------------------------------


def test_gap_AnnotationGT_thi_wrong_gt_kind():
    for lop in METRIC_THEO_LOAI.values():
        r = lop().score(AnnotationGT(doc_id="d1"), kq("gì đó"))
        assert r.is_na
        assert r.na_reason is NAReason.WRONG_GT_KIND
        assert r.detail["wants"] == ["AssertionGT"]


def test_khong_co_khang_dinh_loai_nay_thi_NA_chu_khong_phai_0():
    """Tài liệu chỉ hỏi về math — năm metric còn lại phải N/A.

    Chấm 0.0 ở đây là phạt engine vì bộ nhãn không hỏi. Đúng bẫy đã ghi từ B3.
    """
    chi_math = gt(MathPresence(latex="E=mc^2"))
    for loai, lop in METRIC_THEO_LOAI.items():
        r = lop().score(chi_math, kq("không liên quan"))
        if loai == "math_presence":
            assert r.value == 0.0
        else:
            assert r.is_na, f"{lop.name} chấm điểm cho loại nó không có nhãn"
            assert r.na_reason is NAReason.NO_GROUND_TRUTH


def test_thieu_nang_luc_text_md_thi_NA():
    khong_text = OcrResult(
        engine="thu", engine_version="0", doc_id="d1", capabilities=frozenset()
    )
    r = TextPresenceMetric().score(gt(TextPresence(needle="a")), khong_text)
    assert r.na_reason is NAReason.MISSING_CAPABILITY


def test_engine_hong_thi_engine_failed():
    r = TextPresenceMetric().score(gt(TextPresence(needle="a")), kq(None, failed=True))
    assert r.na_reason is NAReason.ENGINE_FAILED


# ---------------------------------------------------------------------------
# text_presence / text_absence
# ---------------------------------------------------------------------------


def test_presence_dat_va_truot():
    m = TextPresenceMetric()
    assert m.score(gt(TextPresence(needle="báo cáo")), kq("… báo cáo …")).value == 1.0
    assert m.score(gt(TextPresence(needle="báo cáo")), kq("không có")).value == 0.0


def test_max_diffs_that_su_noi_long():
    """`max_diffs` là ngưỡng của chính bộ nhãn — bỏ nó đi là chấm khắt hơn tác giả."""
    chat = TextPresence(needle="Nguyen Van A", max_diffs=0)
    long_ = TextPresence(needle="Nguyen Van A", max_diffs=2)
    doi = kq("ky ten: Nguyen Vsn A")
    assert TextPresenceMetric().score(gt(chat), doi).value == 0.0
    assert TextPresenceMetric().score(gt(long_), doi).value == 1.0


def test_case_sensitive():
    hoa = TextPresence(needle="ABC", case_sensitive=True)
    assert TextPresenceMetric().score(gt(hoa), kq("abc")).value == 0.0
    thuong = TextPresence(needle="ABC", case_sensitive=False)
    assert TextPresenceMetric().score(gt(thuong), kq("abc")).value == 1.0


def test_absence_va_cua_so_first_n():
    """"Không được nằm trong 200 ký tự đầu" ≠ "không được nằm ở đâu cả"."""
    trang = "TIÊU ĐỀ TRANG\n" + "x" * 300 + "\nTIÊU ĐỀ TRANG"
    m = TextAbsenceMetric()
    # Không ràng buộc vùng: chuỗi có mặt ⇒ trượt.
    assert m.score(gt(TextAbsence(needle="TIÊU ĐỀ TRANG")), kq(trang)).value == 0.0
    # Chỉ cấm ở 5 ký tự cuối: chỗ đó là "TRANG"… vẫn có ⇒ trượt.
    assert (
        m.score(gt(TextAbsence(needle="TRANG", last_n=5)), kq(trang)).value == 0.0
    )
    # Cấm trong 3 ký tự đầu — không chứa cả chuỗi ⇒ đạt.
    assert (
        m.score(gt(TextAbsence(needle="TIÊU ĐỀ TRANG", first_n=3)), kq(trang)).value
        == 1.0
    )


def test_cua_so_last_n_bang_0_la_rong_chu_khong_phai_toan_bo():
    assert cua_so("abcdef", None, 0) == ""
    assert cua_so("abcdef", None, 2) == "ef"
    assert cua_so("abcdef", 2, None) == "ab"


def test_co_mat_bien():
    assert co_mat("", "bất kỳ") is True
    assert co_mat("a", "") is False


# ---------------------------------------------------------------------------
# reading_order
# ---------------------------------------------------------------------------


def test_dao_thu_tu_thi_tut_diem():
    """AC cốt lõi của loại này: đổi chỗ hai đoạn phải đổi kết quả."""
    kd = gt(ReadingOrder(before="phần mở đầu", after="phần kết luận"))
    m = ReadingOrderMetric()
    assert m.score(kd, kq("phần mở đầu … phần kết luận")).value == 1.0
    assert m.score(kd, kq("phần kết luận … phần mở đầu")).value == 0.0


def test_thieu_mot_ve_thi_truot():
    kd = gt(ReadingOrder(before="có", after="vắng mặt hoàn toàn"))
    assert ReadingOrderMetric().score(kd, kq("chỉ có vế đầu")).value == 0.0


def test_lap_lai_thi_lay_moi_vi_tri():
    """Luật olmOCR: đạt nếu *một* vị trí `before` đứng trước *một* vị trí `after`."""
    kd = gt(ReadingOrder(before="A", after="B"))
    # B xuất hiện trước, nhưng cũng có một B sau A ⇒ đạt.
    assert ReadingOrderMetric().score(kd, kq("B … A … B")).value == 1.0


def test_tim_moi_vi_tri_tang_dan_va_khong_lap_vo_han():
    vt = tim_moi_vi_tri("abc", "abc xx abc yy abc")
    assert len(vt) == 3
    assert vt == sorted(vt)
    assert tim_moi_vi_tri("", "abc") == []
    assert tim_moi_vi_tri("abc", "") == []


def test_gioi_han_so_vi_tri():
    vt = tim_moi_vi_tri("ab", "ab" * 200, gioi_han=5)
    assert len(vt) == 5


# ---------------------------------------------------------------------------
# math_presence — CẬN DƯỚI
# ---------------------------------------------------------------------------


def test_math_khop_nguyen_van():
    r = MathPresenceMetric().score(gt(MathPresence(latex="E=mc^2")), kq("$E=mc^2$"))
    assert r.value == 1.0
    assert r.detail["n_khop_nguyen_van"] == 1
    assert r.detail["n_khop_sau_chuan_hoa"] == 0


def test_math_khop_nho_chuan_hoa_va_detail_tach_hai_con_so():
    """`\\dfrac` và `\\frac` hiển thị y hệt — đạt, nhưng phải ghi là nhờ chuẩn hoá."""
    r = MathPresenceMetric().score(
        gt(MathPresence(latex=r"\dfrac{1}{2}")), kq(r"công thức: $\frac{1}{2}$ ở đây")
    )
    assert r.value == 1.0
    assert r.detail["n_khop_nguyen_van"] == 0
    assert r.detail["n_khop_sau_chuan_hoa"] == 1
    assert "cận dưới" in str(r.detail["canh_bao"])


def test_math_sai_thi_truot():
    r = MathPresenceMetric().score(gt(MathPresence(latex="x^2+y^2=z^2")), kq("$a+b$"))
    assert r.value == 0.0


def test_chuan_hoa_latex_de_dat_khong_gop_bua():
    assert chuan_hoa_latex(r"$$\dfrac{1}{2}$$") == chuan_hoa_latex(r"\frac{1}{2}")
    assert chuan_hoa_latex(r"\left( x \right)") == chuan_hoa_latex("(x)")
    # KHÔNG được gộp hai công thức thật sự khác nhau.
    assert chuan_hoa_latex("x^2") != chuan_hoa_latex("x^3")
    assert chuan_hoa_latex(r"\alpha") != chuan_hoa_latex(r"\beta")


def test_math_rong_thi_truot_chu_khong_phai_dat_mien_phi():
    assert MathPresenceMetric().score(gt(MathPresence(latex="  ")), kq("gì đó")).value == 0.0


# ---------------------------------------------------------------------------
# table_relation
# ---------------------------------------------------------------------------

BANG_MD = """
| Tỉnh | 2024 | 2025 |
|---|---|---|
| Hà Nội | 10 | 12 |
| Đà Nẵng | 7 | 9 |
"""


def test_bang_quan_he_dung():
    kd = TableRelation(cell="12", left="10", top_heading="2025", left_heading="Hà Nội")
    assert TableRelationMetric().score(gt(kd), kq(BANG_MD)).value == 1.0


def test_bang_quan_he_sai_thi_truot():
    kd = TableRelation(cell="12", left="99")
    assert TableRelationMetric().score(gt(kd), kq(BANG_MD)).value == 0.0


def test_bang_len_xuong():
    tren = TableRelation(cell="9", up="12")
    duoi = TableRelation(cell="10", down="7")
    m = TableRelationMetric()
    assert m.score(gt(tren), kq(BANG_MD)).value == 1.0
    assert m.score(gt(duoi), kq(BANG_MD)).value == 1.0


def test_bang_html_cung_doc_duoc():
    html = (
        "<table><tr><th>A</th><th>B</th></tr>"
        "<tr><td>1</td><td>2</td></tr></table>"
    )
    kd = TableRelation(cell="2", left="1", top_heading="B")
    assert TableRelationMetric().score(gt(kd), kq(html)).value == 1.0


def test_khong_co_bang_thi_truot_chu_khong_no():
    kd = TableRelation(cell="12", left="10")
    assert TableRelationMetric().score(gt(kd), kq("văn bản trơn")).value == 0.0


def test_doc_bang_bo_hang_gach_ngan():
    luoi = doc_bang(BANG_MD)
    assert len(luoi) == 1
    assert luoi[0][0] == ["Tỉnh", "2024", "2025"]
    assert len(luoi[0]) == 3, "hàng |---|---| không được thành một hàng dữ liệu"


def test_doc_bang_nhieu_bang_roi_nhau():
    assert len(doc_bang(BANG_MD + "\nvăn bản chen giữa\n" + BANG_MD)) == 2


# ---------------------------------------------------------------------------
# baseline
# ---------------------------------------------------------------------------


def test_baseline_rong_thi_truot():
    assert BaselineMetric().score(gt(Baseline()), kq("   \n ")).value == 0.0
    assert BaselineMetric().score(gt(Baseline()), kq("có chữ")).value == 1.0


def test_baseline_bat_ky_tu_thay_the():
    kd = gt(Baseline(check_disallowed_characters=True))
    assert BaselineMetric().score(kd, kq("n�i dung")).value == 0.0
    # Không bật cờ thì không kiểm ký tự cấm.
    assert (
        BaselineMetric().score(gt(Baseline()), kq("n�i dung")).value == 1.0
    )


# ---------------------------------------------------------------------------
# chi tiết chung
# ---------------------------------------------------------------------------


def test_ty_le_dung_va_liet_ke_id_truot():
    kd = gt(
        TextPresence(needle="có", assertion_id="t1"),
        TextPresence(needle="vắng", assertion_id="t2"),
    )
    r = TextPresenceMetric().score(kd, kq("chỉ có cái này"))
    assert r.value == 0.5
    assert r.detail["id_truot"] == ["t2"]


def test_khang_dinh_trung_noi_dung_khong_che_nhau():
    """Lọc bằng `kd not in dat` sẽ sai ở đây: hai khẳng định bằng nhau theo `__eq__`."""
    kd = gt(TextPresence(needle="vắng"), TextPresence(needle="vắng"))
    r = TextPresenceMetric().score(kd, kq("không chứa gì"))
    assert r.value == 0.0
    assert r.detail["n_khang_dinh"] == 2


# ---------------------------------------------------------------------------
# đăng ký
# ---------------------------------------------------------------------------


def test_ca_sau_lop_deu_da_dang_ky():
    """Viết xong metric mà quên đăng ký thì `scorer` không bao giờ gọi tới nó.

    Đúng lỗi đã xảy ra thật ở B5: sáu lớp chạy xanh 34 test nhưng
    `registry.list_metrics()` không có tên nào, và chỉ lộ ra khi chấm thật.
    """
    import ocr_bench  # noqa: F401  — import để các metric tự đăng ký
    from ocr_bench import registry

    da_dang_ky = set(registry.list_metrics())
    for loai, lop in METRIC_THEO_LOAI.items():
        assert lop.name in da_dang_ky, f"{lop.name} ({loai}) chưa đăng ký"
