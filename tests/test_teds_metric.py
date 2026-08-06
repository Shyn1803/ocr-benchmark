"""B2 — TEDS và TEDS-Struct (TASK-080).

`apted` là extra `metrics`; README hứa `pytest` xanh trên máy trắng nên bỏ qua cả
file nếu chưa cài. `table_recognition_metric` chỉ dùng để đối chiếu — nó **không**
nằm trong bất kỳ extra nào, nên phần đối chiếu được skip riêng.
"""

from __future__ import annotations

import random

import pytest

pytest.importorskip("apted")
pytest.importorskip("rapidfuzz")

from ocr_bench.metrics.teds import (  # noqa: E402
    TedsMetric,
    TedsStructMetric,
    teds_score,
)
from ocr_bench.types import (  # noqa: E402
    AnnotationGT,
    Capability,
    NAReason,
    OcrResult,
    OcrTable,
)

_BANG = "<table><tr><td>Quý</td><td>Doanh thu</td></tr><tr><td>1</td><td>10</td></tr></table>"


def _kq(*html: str, caps: frozenset[Capability] | None = None) -> OcrResult:
    """`OcrResult` chỉ có bảng — đủ để đi qua cổng năng lực."""
    return OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.TABLE_HTML}) if caps is None else caps,
        tables=[OcrTable(html=h) for h in html],
    )


def _gt(*html: str) -> AnnotationGT:
    return AnnotationGT(doc_id="d1", tables=[OcrTable(html=h) for h in html])


# --- teds_score: hành vi lõi -------------------------------------------------


def test_giong_het_thi_1() -> None:
    assert teds_score(_BANG, _BANG) == 1.0
    assert teds_score(_BANG, _BANG, structure_only=True) == 1.0


def test_sai_chu_trong_o_thi_teds_tut_ma_struct_van_1() -> None:
    """Đây là lý do tồn tại của hai cột. Gộp một số là mất đúng chẩn đoán này."""
    sai = _BANG.replace("Doanh thu", "Doanh thn")
    assert teds_score(_BANG, sai) < 1.0
    assert teds_score(_BANG, sai, structure_only=True) == 1.0


def test_lech_colspan_thi_ca_hai_cot_deu_tut() -> None:
    """Ngược lại: lỗi cấu trúc phải hiện ở CẢ hai cột, không cột nào che được."""
    sai = _BANG.replace("<td>Quý</td>", '<td colspan="2">Quý</td>')
    assert teds_score(_BANG, sai) < 1.0
    assert teds_score(_BANG, sai, structure_only=True) < 1.0


def test_moi_diem_deu_trong_khoang() -> None:
    """`Metric.score()` NÉM khi điểm ngoài [0,1] — kẹp không phải cho đẹp."""
    for pred in ("<table></table>", "<table><tr><td>x</td></tr></table>", _BANG * 3):
        d = teds_score(_BANG, pred)
        assert d is not None and 0.0 <= d <= 1.0


def test_bang_nhan_rong_thi_None_chu_khong_phai_0() -> None:
    """AC-04. 0 nghĩa là 'engine trượt'; nhãn rỗng không nói gì về engine."""
    assert teds_score("<table></table>", _BANG) is None
    assert teds_score("", _BANG) is None


def test_nhan_co_bang_ma_doan_khong_co_thi_0() -> None:
    """Vế đối của test trên: đây MỚI là engine trượt thật."""
    assert teds_score(_BANG, "<p>không có bảng nào</p>") == 0.0


def test_the_thieu_dong_van_doc_duoc() -> None:
    """`<td>a<td>b` là HTML hợp lệ; engine có quyền sinh ra."""
    assert teds_score("<table><tr><td>a</td><td>b</td></tr></table>",
                      "<table><tr><td>a<td>b</table>") == 1.0


def test_bang_long_trong_o_khong_bi_keo_ra_ngoai() -> None:
    """Bẫy tự gây: đóng ngầm `td` khi gặp `<table>` sẽ tách bảng con khỏi ô mẹ."""
    long_nhau = "<table><tr><td><table><tr><td>x</td></tr></table></td></tr></table>"
    assert teds_score(long_nhau, long_nhau) == 1.0


def test_colspan_hong_khong_lam_no() -> None:
    """`colspan="two"` là HTML hỏng — trình duyệt coi như 1, ta cũng vậy."""
    assert teds_score('<table><tr><td colspan="two">a</td></tr></table>',
                      "<table><tr><td>a</td></tr></table>") == 1.0


def test_the_rong_trong_o_khong_lam_lech_cay() -> None:
    """`<br>` (và `<br/>`) là thẻ rỗng — không được đẩy vào ngăn xếp, nếu không
    mọi thứ sau nó sẽ chui vào trong nó và ô bị vỡ. Marker sinh `<br>` rất nhiều."""
    xuong_dong = "<table><tr><td>a<br>b</td><td>c</td></tr></table>"
    tu_dong = "<table><tr><td>a<br/>b</td><td>c</td></tr></table>"
    assert teds_score(xuong_dong, tu_dong) == 1.0
    # Ô thứ hai vẫn là ô riêng chứ không bị nuốt vào `<br>`:
    assert teds_score(xuong_dong, "<table><tr><td>a<br>b</td></tr></table>") < 1.0


def test_the_dong_thua_bi_bo_qua_chu_khong_lam_sap() -> None:
    """HTML engine sinh ra không phải lúc nào cũng cân; sập ở đây là mất cả tài liệu."""
    assert teds_score("<table><tr><td>a</td></tr></table>",
                      "</div><table><tr><td>a</td></tr></table></span>") == 1.0


# --- chuẩn hoá lớp vỏ (quyết định 2) ----------------------------------------


def test_tbody_va_th_khong_bi_tinh_la_loi() -> None:
    """Marker ra `<tbody><th>`, opendataloader ra `<tr><td>` — CÙNG một bảng.

    Không chuẩn hoá thì ta đo quy ước sinh HTML, không đo độ chính xác.
    """
    marker = "<table><thead><tr><th>A</th></tr></thead><tbody><tr><td>1</td></tr></tbody></table>"
    odl = "<table><tr><td>A</td></tr><tr><td>1</td></tr></table>"
    assert teds_score(marker, odl) == 1.0
    # ... và tắt chuẩn hoá thì đúng là bị trừ, chứng minh test trên không may mắn.
    assert teds_score(marker, odl, chuan_hoa=False) < 1.0


# --- đối chiếu bản tham chiếu (AC-01) ---------------------------------------


def _bang_ngau_nhien(seed: int, bang_chu: str) -> str:
    r = random.Random(seed)
    ra = ["<html><body><table>"]
    for _ in range(r.randint(1, 4)):
        ra.append("<tr>")
        for _ in range(r.randint(1, 4)):
            a = ""
            if r.random() < 0.25:
                a += ' colspan="%d"' % r.randint(1, 3)
            if r.random() < 0.25:
                a += ' rowspan="%d"' % r.randint(1, 3)
            t = "".join(r.choice(bang_chu) for _ in range(r.randint(0, 6)))
            if r.random() < 0.15:
                t = "<b>%s</b>" % t
            ra.append("<td%s>%s</td>" % (a, t))
        ra.append("</tr>")
    ra.append("</table></body></html>")
    return "".join(ra)


def test_khop_ban_tham_chieu_khi_o_khong_co_khoang_trang() -> None:
    """AC-01. Chỉ lệch ở đúng một chỗ ta CỐ Ý lệch — xem `_token()`."""
    TEDS = pytest.importorskip("table_recognition_metric").TEDS
    ref = TEDS()
    for i in range(120):
        a = _bang_ngau_nhien(i * 2, "abcXY0123")
        b = _bang_ngau_nhien(i * 2 + 1, "abcXY0123")
        assert teds_score(a, b, chuan_hoa=False) == pytest.approx(
            float(ref(a, b)), abs=1e-9
        ), "lệch ở cặp %d" % i


def test_struct_khop_ban_tham_chieu_ke_ca_khi_co_khoang_trang() -> None:
    """`teds_struct` bỏ nội dung ô nên chỗ cố ý lệch không còn ảnh hưởng."""
    TEDS = pytest.importorskip("table_recognition_metric").TEDS
    ref = TEDS(structure_only=True)
    for i in range(120):
        a = _bang_ngau_nhien(i * 2, "abcXY 0123")
        b = _bang_ngau_nhien(i * 2 + 1, "abcXY 0123")
        assert teds_score(a, b, chuan_hoa=False, structure_only=True) == pytest.approx(
            float(ref(a, b)), abs=1e-9
        ), "lệch ở cặp %d" % i


def test_khoang_trang_html_khong_bi_tinh_la_loi() -> None:
    """Chỗ cố ý lệch, khoá lại để không ai "sửa cho khớp bản gốc" mà không biết."""
    a = "<table><tr><td>  Doanh   thu </td></tr></table>"
    b = "<table><tr><td>Doanh thu</td></tr></table>"
    assert teds_score(a, b, chuan_hoa=False) == 1.0


# --- lớp Metric: các cổng ----------------------------------------------------


def test_engine_khong_khai_bang_thi_na_chu_khong_phai_0() -> None:
    kq = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.TEXT_MD}),
    )
    r = TedsMetric().score(_gt(_BANG), kq)
    assert r.value is None and r.na_reason is NAReason.MISSING_CAPABILITY


def test_nhan_khong_co_bang_dung_duoc_thi_no_ground_truth() -> None:
    """AC-04 ở tầng metric: bảng rỗng bị loại, hết bảng thì cả tài liệu ra N/A."""
    r = TedsMetric().score(_gt("<table></table>"), _kq(_BANG))
    assert r.value is None and r.na_reason is NAReason.NO_GROUND_TRUTH
    assert r.detail["n_bang_nhan"] == 1  # nhãn CÓ bảng, chỉ là không dùng được


def test_khai_bang_nhung_khong_tra_bang_nao_thi_cham_0() -> None:
    """Khai khống năng lực không được hưởng N/A — N/A không vào mẫu số phạt."""
    r = TedsMetric().score(_gt(_BANG), _kq())
    assert r.value == 0.0 and r.na_reason is None


def test_sai_loai_nhan_thi_wrong_gt_kind() -> None:
    from ocr_bench.types import AssertionGT

    r = TedsMetric().score(AssertionGT(doc_id="d1"), _kq(_BANG))
    assert r.value is None and r.na_reason is NAReason.WRONG_GT_KIND


def test_bang_thua_hay_thieu_deu_bi_phat() -> None:
    """Bỏ qua bảng lệch số sẽ thưởng cho engine chỉ xuất bảng nó tự tin."""
    thieu = TedsMetric().score(_gt(_BANG, _BANG), _kq(_BANG))
    thua = TedsMetric().score(_gt(_BANG), _kq(_BANG, _BANG))
    assert thieu.value == pytest.approx(0.5)  # một bảng đúng, một bảng thiếu
    assert thua.value == pytest.approx(0.5)


def test_hai_metric_dung_ten_khac_nhau() -> None:
    assert TedsMetric.name == "teds" and TedsStructMetric.name == "teds_struct"
    assert TedsStructMetric.structure_only and not TedsMetric.structure_only


def test_detail_giu_diem_tung_bang() -> None:
    """B6/D2 cần biết bảng NÀO hỏng, không chỉ điểm trung bình."""
    r = TedsMetric().score(_gt(_BANG, _BANG), _kq(_BANG, "<p>trượt</p>"))
    assert r.detail["tung_bang"] == [1.0, 0.0]
    assert r.value == pytest.approx(0.5)
