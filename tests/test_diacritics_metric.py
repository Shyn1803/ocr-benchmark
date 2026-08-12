"""B8 — dấu tiếng Việt: `diacritics_acc` (Task 8).

`cer` đã đếm ký tự sai. Nó **không** tách được lỗi mất dấu khỏi lỗi đọc nhầm chữ,
mà với tiếng Việt đó là hai bệnh khác nhau: "hoa" ↔ "hóa" là lỗi dấu (mô hình
không có tiếng Việt), "hoa" ↔ "boa" là lỗi nhận dạng chữ. Engine mất sạch dấu vẫn
có thể có CER 0.15 nghe khá ổn, trong khi văn bản ra là không dùng được.

Cách đo: căn theo **chữ cái gốc** (bỏ dấu, `đ` → `d`) rồi hỏi ở mỗi vị trí nhãn có
dấu, engine có đặt đúng dấu đó không. Mẫu số là số ký tự **có dấu trong nhãn** —
không phải toàn bộ ký tự, vì thế thì tài liệu càng ít dấu điểm càng cao miễn phí.

`importorskip("rapidfuzz")`: phép căn dùng `rapidfuzz.distance.Indel.opcodes`,
thuộc extra `metrics`.
"""

from __future__ import annotations

import pytest

pytest.importorskip("rapidfuzz")

from ocr_bench.metrics.diacritics import (  # noqa: E402
    DiacriticsMetric,
    chu_goc,
    diacritic_scores,
)
from ocr_bench.types import (  # noqa: E402
    AnnotationGT,
    AssertionGT,
    Capability,
    FailureKind,
    NAReason,
    OcrResult,
)

_CAU = "Đường lối đổi mới của Việt Nam"
_MAT_DAU = "Duong loi doi moi cua Viet Nam"


def _gt(text: str | None = _CAU) -> AnnotationGT:
    return AnnotationGT(doc_id="d1", text=text)


def _kq(text: str) -> OcrResult:
    return OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md=text,
    )


# --- chữ gốc -----------------------------------------------------------------


@pytest.mark.parametrize(
    ("co_dau", "goc"),
    [
        ("ế", "e"),
        ("Ế", "E"),
        ("ạ", "a"),
        ("ữ", "u"),
        ("ơ", "o"),
        ("â", "a"),
        ("a", "a"),
        ("1", "1"),
    ],
)
def test_chu_goc_bo_het_dau(co_dau: str, goc: str) -> None:
    assert chu_goc(co_dau) == goc


def test_chu_goc_xu_ly_d_gach_ngang() -> None:
    """`đ` không phân rã được bằng NFD — U+0111 là một ký tự nguyên khối. Không
    xử lý riêng thì "đường" và "duong" không căn được với nhau, và mọi lỗi mất
    dấu của chữ `đ` bị đếm thành lỗi nhận dạng chữ."""
    assert chu_goc("đ") == "d"
    assert chu_goc("Đ") == "D"


# --- điểm --------------------------------------------------------------------


def test_khop_hoan_toan_thi_1() -> None:
    diem, ct = diacritic_scores(_CAU, _CAU)
    assert diem == 1.0
    assert ct["n_sai"] == 0


def test_mat_sach_dau_thi_0() -> None:
    """Đây là ca mà `cer` không phân biệt được — chuỗi vẫn đọc gần đúng."""
    diem, ct = diacritic_scores(_CAU, _MAT_DAU)
    assert diem == 0.0
    assert ct["n_mat_dau"] == ct["n_co_dau"]


def test_metric_controls_are_ordered() -> None:
    mot_phan = "Đường lối đổi mơi cua Việt Nam"
    diem = [
        DiacriticsMetric().score(_gt(), _kq(x)).value
        for x in (_CAU, mot_phan, _MAT_DAU)
    ]
    assert diem[0] == 1.0
    assert diem[0] > diem[1] > diem[2]


def test_sai_dau_khac_mat_dau() -> None:
    """"hòa" thay vì "hóa" là đặt sai dấu; "hoa" là mất dấu. Cùng trừ điểm nhưng
    phải đếm riêng — chẩn đoán khác nhau, cách sửa mô hình cũng khác nhau."""
    _, sai = diacritic_scores("hóa", "hòa")
    _, mat = diacritic_scores("hóa", "hoa")
    assert (sai["n_sai_dau"], sai["n_mat_dau"]) == (1, 0)
    assert (mat["n_sai_dau"], mat["n_mat_dau"]) == (0, 1)


def test_mau_so_chi_dem_ky_tu_co_dau_trong_nhan() -> None:
    """13 ký tự, đúng **một** ký tự có dấu. Lấy mẫu số là toàn bộ ký tự thì engine
    mất sạch dấu vẫn được 12/13 = 0.92 — một con số đẹp cho một đầu ra hỏng."""
    diem, ct = diacritic_scores("Việt Nam 2026", "Viet Nam 2026")
    assert ct["n_co_dau"] == 1
    assert diem == 0.0


def test_them_chu_khong_lam_hong_can_le() -> None:
    """Engine chèn thêm chữ ở đầu thì phần còn lại vẫn phải căn đúng — nếu căn
    theo chỉ số thay vì theo `Indel.opcodes` thì cả câu lệch một ô và điểm về 0
    dù engine đặt dấu hoàn hảo."""
    diem, _ = diacritic_scores(_CAU, "XX " + _CAU)
    assert diem == 1.0


# --- cổng N/A ----------------------------------------------------------------


def test_nhan_khong_co_dau_nao_thi_na_chu_khong_phai_1() -> None:
    ket = DiacriticsMetric().score(_gt("Ha Noi 2026"), _kq("Ha Noi 2026"))
    assert ket.value is None
    assert ket.na_reason is NAReason.NO_GROUND_TRUTH


def test_nhan_khong_co_chu_thi_na() -> None:
    ket = DiacriticsMetric().score(_gt(None), _kq(_CAU))
    assert ket.value is None
    assert ket.na_reason is NAReason.NO_GROUND_TRUTH


def test_thieu_nang_luc_text_md_thi_na() -> None:
    doan = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.BLOCK_BBOX}),
    )
    ket = DiacriticsMetric().score(_gt(), doan)
    assert ket.na_reason is NAReason.MISSING_CAPABILITY


def test_engine_hong_thi_na() -> None:
    hong = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.TEXT_MD}),
        failed=True,
        error="nổ",
        failure_kind=FailureKind.ENGINE_ERROR,
    )
    assert DiacriticsMetric().score(_gt(), hong).na_reason is NAReason.ENGINE_FAILED


def test_sai_loai_nhan_thi_na() -> None:
    ket = DiacriticsMetric().score(AssertionGT(doc_id="d1"), _kq(_CAU))
    assert ket.na_reason is NAReason.WRONG_GT_KIND
