"""Test kỷ luật vẽ của `scripts/d3_charts.py`.

Biểu đồ nói mạnh hơn bảng: người đọc so hai cột cạnh nhau trước khi kịp đọc chú
thích. Nên mọi ràng buộc bảng đang chịu, biểu đồ phải chịu **chặt hơn**, và chỗ dễ
tuột nhất là vẽ ô "không đo được" thành cột cao 0 — trông như điểm 0, đọc ra là
*đo được và tệ nhất*, trong khi sự thật là chưa từng đo.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from ocr_bench.metrics.base import aggregate
from ocr_bench.types import MetricResult, NAReason

GOC = Path(__file__).resolve().parents[1]


def _nap_script():
    spec = importlib.util.spec_from_file_location(
        "d3_charts", GOC / "scripts" / "d3_charts.py"
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["d3_charts"] = mod
    spec.loader.exec_module(mod)
    return mod


D3 = _nap_script()


def _rows(values=(), *, failed=0, thieu_nang_luc=0, chua_nhan=0):
    rows = [
        MetricResult(metric="m", engine="e", doc_id=f"d{i}", value=v)
        for i, v in enumerate(values)
    ]
    for i in range(failed):
        rows.append(MetricResult(metric="m", engine="e", doc_id=f"f{i}",
                                 value=None, na_reason=NAReason.ENGINE_FAILED))
    for i in range(thieu_nang_luc):
        rows.append(MetricResult(metric="m", engine="e", doc_id=f"n{i}",
                                 value=None, na_reason=NAReason.MISSING_CAPABILITY))
    for i in range(chua_nhan):
        rows.append(MetricResult(metric="m", engine="e", doc_id=f"g{i}",
                                 value=None, na_reason=NAReason.NO_GROUND_TRUTH))
    return rows


@pytest.mark.parametrize(
    "rows",
    [
        _rows(thieu_nang_luc=5),                 # N/A
        _rows(chua_nhan=5),                      # chưa có nhãn
        _rows(failed=5),                         # hỏng hết
        _rows(chua_nhan=5, failed=2),            # thiếu nhãn + vài cái hỏng
    ],
    ids=["thieu_nang_luc", "chua_nhan", "hong_het", "thieu_nhan_va_hong"],
)
def test_khong_do_duoc_thi_khong_co_cot(rows):
    """Mọi trạng thái "chưa từng chấm được" đều phải trả `None` — không vẽ cột."""
    gia_tri, nhan = D3._o(aggregate(rows))
    assert gia_tri is None
    assert nhan, "phải có chữ thay cho cột, không để ô trống không giải thích"


def test_cham_duoc_thi_co_cot_va_khop_bang():
    """Có chấm được thì vẽ cột, và trị vẽ đúng bằng trung bình có phạt — biểu đồ
    không được là một phép tính thứ hai bên cạnh bảng."""
    a = aggregate(_rows([1.0, 1.0], failed=2))
    gia_tri, nhan = D3._o(a)
    assert gia_tri == a.penalized_mean == 0.5
    assert nhan == a.cell()


def test_diem_0_that_van_ve_cot():
    """Ca âm. Engine chấm được và đúng 0 điểm thì cột **phải** xuất hiện — nếu không
    thì phép loại "cột cao 0" đã nuốt luôn engine thật sự tệ, đổi một hiểu nhầm này
    lấy một hiểu nhầm khác."""
    gia_tri, _ = D3._o(aggregate(_rows([0.0, 0.0])))
    assert gia_tri == 0.0


def test_nhan_ngan_phan_biet_ba_trang_thai():
    """Ba lý do "không có cột" phải ra ba chữ khác nhau.

    Rút gọn nhãn là chỗ dễ đánh mất đúng cái phân biệt vừa dựng lên ở `Aggregate`:
    "engine không hứa làm việc này" (N/A), "bộ mẫu chưa có nhãn" và "engine hỏng" là
    ba kết luận khác hẳn nhau về ai chịu trách nhiệm. Gộp lại thành một chữ chung là
    đổ lỗi nhầm chỗ.
    """
    na = D3._nhan_ngan(aggregate(_rows(thieu_nang_luc=5)))
    thieu = D3._nhan_ngan(aggregate(_rows(chua_nhan=5)))
    hong = D3._nhan_ngan(aggregate(_rows(failed=5)))
    assert len({na, thieu, hong}) == 3, (na, thieu, hong)
    assert "5" in hong, "đếm được bao nhiêu cái hỏng thì phải nói ra"


def test_hang_co_cot_thi_moi_engine_trong_deu_co_chu():
    """Ca hồi quy. Hàng `heading`: `opendataloader` có cột, hai engine kia N/A. Trước
    đây chỉ engine thứ 0 in nhãn, nên khi engine 0 lại là engine *có* cột thì hai khe
    kia trống trơn — đọc ra là "quên vẽ", không phải "N/A"."""
    hang = [
        aggregate(_rows([0.5, 0.5])),
        aggregate(_rows(thieu_nang_luc=5)),
        aggregate(_rows(thieu_nang_luc=5)),
    ]
    co_cot = [D3._o(a)[0] is not None for a in hang]
    assert co_cot == [True, False, False]
    assert all(D3._nhan_ngan(a) for a, v in zip(hang, co_cot) if not v)


def test_thoat_ky_tu_xml():
    assert D3._thoat("a<b&c>d") == "a&lt;b&amp;c&gt;d"
