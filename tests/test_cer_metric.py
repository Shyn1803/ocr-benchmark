"""Test CER/WER — B1 (TASK-079).

Trọng tâm không phải "jiwer tính đúng không" (đó là việc của jiwer) mà là **ba
chỗ ta dễ chấm sai**: Unicode, điểm âm, và nhãn thiếu.
"""

from __future__ import annotations

import unicodedata

import pytest

from ocr_bench.metrics.cer import CerMetric, WerMetric
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Capability,
    FailureKind,
    NAReason,
    OcrResult,
)

jiwer = pytest.importorskip("jiwer", reason="cần extra `metrics`")

TEXT = frozenset({Capability.TEXT_MD})


def _kq(text: str | None, *, caps=TEXT, failed=False, error=None) -> OcrResult:
    return OcrResult(
        engine="x",
        engine_version="0",
        doc_id="d1",
        capabilities=caps,
        text_md=text,
        failed=failed,
        error=error,
        failure_kind=FailureKind.ENGINE_ERROR if failed else None,
    )


def _gt(text: str | None) -> AnnotationGT:
    return AnnotationGT(doc_id="d1", text=text)


# --- AC-03: Unicode. Cái bẫy chính của cả file. ---------------------------------


@pytest.mark.parametrize("M", [CerMetric, WerMetric])
def test_nfc_va_nfd_cho_diem_tuyet_doi(M):
    """Cùng một chuỗi tiếng Việt, hai dạng chuẩn hoá → phải 1.0.

    Không có `normalize_text()`, "Điện Biên Phủ" dạng NFD lệch NFC tới từng dấu
    thanh: engine đọc đúng 100% vẫn bị chấm dưới 1.0, và không ai nhìn ra vì hai
    chuỗi in ra màn hình giống hệt nhau.
    """
    goc = "Điện Biên Phủ — hồ sơ số 5"
    nfc, nfd = unicodedata.normalize("NFC", goc), unicodedata.normalize("NFD", goc)
    assert nfc != nfd, "test vô nghĩa nếu hai dạng đã bằng nhau"

    r = M().score(_gt(nfc), _kq(nfd))
    assert r.value == 1.0


@pytest.mark.parametrize("M", [CerMetric, WerMetric])
def test_dau_nhay_cong_veo_khong_bi_tinh_la_loi(M):
    """`normalize_text` gộp ‘ ’ “ ” – — về dạng thẳng. Đó là khác kiểu chữ, không
    phải lỗi đọc — engine không nên bị phạt vì PDF dùng dấu nháy cong."""
    assert M().score(_gt('nói "vâng" – rồi đi'), _kq("nói “vâng” — rồi đi")).value == 1.0


# --- AC-02: chiều và biên -------------------------------------------------------


@pytest.mark.parametrize("M", [CerMetric, WerMetric])
def test_giong_het_thi_1_khac_han_thi_thap(M):
    m = M()
    assert m.score(_gt("alpha beta"), _kq("alpha beta")).value == 1.0
    assert m.score(_gt("alpha beta"), _kq("")).value == 0.0


def test_chen_thua_bi_kep_ve_0_khong_am():
    """`jiwer.cer("ab", "abcdefghij")` = **4.0** → `1-err` = −3.0.

    `Metric.score()` ném khi điểm ngoài [0,1], nên không kẹp thì một engine nói
    nhảm sẽ làm sập cả lượt chấm thay vì bị xếp bét. Đây là lỗi hạ tầng đội lốt
    lỗi engine — kiểu khó lần nhất.
    """
    r = CerMetric().score(_gt("ab"), _kq("ab" + "c" * 200))
    assert r.value == 0.0
    assert r.detail["bi_kep"] is True
    assert r.detail["err"] > 1.0


@pytest.mark.parametrize("M", [CerMetric, WerMetric])
def test_moi_diem_deu_trong_khoang(M):
    m = M()
    for ref, hyp in [("a", "a"), ("a", "b"), ("xin chào", "xin chao"), ("a", "a" * 50)]:
        v = m.score(_gt(ref), _kq(hyp)).value
        assert v is not None and 0.0 <= v <= 1.0


def test_cer_thay_loi_mot_ky_tu_ma_wer_lam_tron_ca_tu():
    """Vì sao giữ cả hai thay vì gộp thành một số.

    Sai đúng 1 ký tự trong 1 từ: WER tính cả từ đó là sai, CER thấy đúng tỉ lệ.
    """
    ref, hyp = "abcdefghij", "abcdefghix"
    assert CerMetric().score(_gt(ref), _kq(hyp)).value > 0.85
    assert WerMetric().score(_gt(ref), _kq(hyp)).value == 0.0


# --- AC-04 + N/A: không bao giờ thay N/A bằng 0 ---------------------------------


@pytest.mark.parametrize("M", [CerMetric, WerMetric])
def test_engine_khong_khai_text_thi_na_chu_khong_phai_0(M):
    r = M().score(_gt("abc"), _kq(None, caps=frozenset()))
    assert r.value is None
    assert r.na_reason is NAReason.MISSING_CAPABILITY


@pytest.mark.parametrize("M", [CerMetric, WerMetric])
def test_nhan_khong_co_chu_thi_na_chu_khong_phai_0(M):
    """Nhãn thiếu là lỗi của *nhãn*. Chấm 0 ở đây là phạt engine vì việc nó không làm.

    `jiwer` không ném với nhãn rỗng — `cer("", "abc")` trả `3` — nên nếu không tự
    chặn thì ta chấm 0 một cách hoàn toàn im lặng.
    """
    for nhan in (None, "", "   \n\n  "):
        r = M().score(_gt(nhan), _kq("engine đọc ra đầy chữ"))
        assert r.value is None, f"nhãn {nhan!r}"
        assert r.na_reason is NAReason.NO_GROUND_TRUTH


@pytest.mark.parametrize("M", [CerMetric, WerMetric])
def test_engine_khai_text_nhung_tra_none_thi_cham_0(M):
    """Khai TEXT_MD rồi trả `None` là **lỗi engine**, không phải thiếu năng lực.

    Ranh giới này quan trọng: N/A không vào mẫu số của `penalized_mean`, còn 0 thì
    có. Cho engine hưởng N/A ở đây là thưởng cho việc khai khống năng lực.
    """
    r = M().score(_gt("abc"), _kq(None))
    assert r.value == 0.0


@pytest.mark.parametrize("M", [CerMetric, WerMetric])
def test_engine_hong_thi_na_engine_failed(M):
    r = M().score(_gt("abc"), _kq(None, failed=True, error="ocr.boom"))
    assert r.na_reason is NAReason.ENGINE_FAILED


@pytest.mark.parametrize("M", [CerMetric, WerMetric])
def test_gt_sai_loai_thi_na_chu_khong_ném(M):
    r = M().score(AssertionGT(doc_id="d1"), _kq("abc"))
    assert r.na_reason is NAReason.WRONG_GT_KIND


# --- AC-01: đúng là có chuẩn hoá, không phải trùng hợp ---------------------------


def test_chuan_hoa_thuc_su_duoc_goi_chu_khong_phai_may_man():
    """Khoảng trắng thừa/xuống dòng không được tính là lỗi ký tự."""
    assert CerMetric().score(_gt("a b c"), _kq("a   b\t\tc\n")).value == 1.0
