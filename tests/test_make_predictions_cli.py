"""Test chọn tài liệu của `scripts/make_predictions.py`.

Chỉ phần *chọn* — không chạy engine nào. Cờ `--only` sinh ra ở A7 vì `sovereign` ở chế độ
`full` leo thang sang Marker (~54 s/trang CPU): chạy cả 204 tài liệu để trả lời một câu hỏi
về 10 tài liệu là vài giờ ném đi.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _nap():
    """Nạp script như một module — nó nằm ở `scripts/`, không phải trong gói."""
    duong = ROOT / "scripts" / "make_predictions.py"
    spec = importlib.util.spec_from_file_location("_mp", duong)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_mp"] = mod
    spec.loader.exec_module(mod)
    return mod


mp = _nap()

needs_corpus = pytest.mark.skipif(
    not sorted((ROOT / "pdfs").glob("doclaynet/*.pdf")),
    reason="cần bộ doclaynet (scripts/fetch_doclaynet.py)",
)


@needs_corpus
def test_only_loc_dung_va_giu_thu_tu():
    het = mp.tim_tai_lieu("doclaynet", None)
    muon = [het[3].stem, het[0].stem]
    ra = mp.tim_tai_lieu("doclaynet", None, ",".join(muon))
    assert [d.stem for d in ra] == sorted(muon), "phải sắp xếp, không theo thứ tự người gõ"


@needs_corpus
def test_only_nem_khi_stem_khong_ton_tai():
    """Không âm thầm chạy ít hơn.

    Gõ nhầm một stem mà script vẫn chạy 9/10 tài liệu rồi in bảng bình thường là cách
    hỏng khó thấy nhất — người đọc bảng không có cách nào biết.
    """
    het = mp.tim_tai_lieu("doclaynet", None)
    with pytest.raises(SystemExit, match="khong-co-that"):
        mp.tim_tai_lieu("doclaynet", None, f"{het[0].stem},khong-co-that")


@needs_corpus
def test_khong_only_thi_khong_doi_gi():
    assert mp.tim_tai_lieu("doclaynet", None, None) == mp.tim_tai_lieu("doclaynet", None)
