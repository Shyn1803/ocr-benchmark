"""Test chuẩn hoá text — nền của mọi metric text."""

from __future__ import annotations

import unicodedata

from ocr_bench.normalize import normalize_text, normalize_ws


def test_nfc_va_nfd_ve_cung_mot_chuoi():
    """Bất biến Unicode. Hai chuỗi hiện lên màn hình giống hệt nhau mà cho CER > 0
    thì con số đó không nói gì về chất lượng OCR."""
    s = "Điều 5 — Bảo hành 24 tháng"
    nfc = unicodedata.normalize("NFC", s)
    nfd = unicodedata.normalize("NFD", s)
    assert nfc != nfd
    assert normalize_text(nfc) == normalize_text(nfd)


def test_gop_dau_nhay_va_gach_ngang():
    assert normalize_text("“trích” – dài") == normalize_text('"trích" - dài')


def test_bo_ky_tu_vo_hinh():
    assert normalize_text("a​b﻿c") == "abc"


def test_gop_khoang_trang_ngang_giu_xuong_dong():
    assert normalize_ws("a   b\t\tc") == "a b c"
    assert normalize_ws("dòng 1  \n  dòng 2") == "dòng 1\ndòng 2"


def test_ep_toi_da_mot_dong_trong():
    assert normalize_ws("a\n\n\n\n\nb") == "a\n\nb"


def test_khong_gop_dau_nhay_khi_tat():
    assert normalize_text("“x”", fold_punct=False) == "“x”"
