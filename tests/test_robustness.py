"""B9 — sụt điểm khi tài liệu bị quét (Task 8).

Đây **không** phải một `Metric`. `Metric` chấm một (engine, tài liệu); độ bền khi
quét chỉ tồn tại giữa **hai** tài liệu — bản số và bản quét của cùng một gốc — nên
nó sống ở mức tổng hợp, cạnh `Aggregate`, đúng chỗ `perf.py` đang đứng.

Quy tắc duy nhất khiến con số này có nghĩa: **chỉ so trên cặp**. So trung bình
nhóm digital với trung bình nhóm scan khi hai nhóm không cùng tập tài liệu là đo
độ khó của hai bộ mẫu khác nhau rồi gọi đó là độ bền của engine.
"""

from __future__ import annotations

import pytest

from ocr_bench.metrics.robustness import (
    Degradation,
    base_doc_id,
    relative_degradation,
)
from ocr_bench.types import MetricResult, NAReason


def _mr(doc_id: str, value: float | None, *, ly_do: NAReason | None = None) -> MetricResult:
    return MetricResult(
        metric="cer",
        engine="giả",
        doc_id=doc_id,
        value=value,
        na_reason=ly_do if value is None else None,
    )


# --- base_doc_id -------------------------------------------------------------


def test_base_doc_id_cat_hau_to_bien_the() -> None:
    assert base_doc_id("vb-001::digital") == "vb-001"
    assert base_doc_id("vb-001::scan200") == "vb-001"


def test_base_doc_id_giu_nguyen_id_khong_co_hau_to() -> None:
    """Dấu tách phải là chuỗi **không xuất hiện tự nhiên** trong doc_id. Cắt theo
    `-digital` thì "only-in-digital" biến thành "only-in" và hai tài liệu khác
    nhau bị gộp làm một cặp giả."""
    assert base_doc_id("only-in-digital") == "only-in-digital"
    assert base_doc_id("bao-cao-scan-2024") == "bao-cao-scan-2024"


# --- ghép cặp ----------------------------------------------------------------


def test_scan_degradation_uses_paired_documents_only() -> None:
    digital = [
        _mr("a::digital", 0.90),
        _mr("b::digital", 0.80),
        _mr("only-in-digital", 0.10),
    ]
    severe = [_mr("a::scan", 0.45), _mr("b::scan", 0.40)]
    got = relative_degradation(digital, severe)
    assert got.n_pairs == 2
    assert got.excluded_doc_ids == ("only-in-digital",)


def test_excluded_tra_doc_id_goc_chu_khong_phai_base() -> None:
    """Người đọc báo cáo phải tìm lại được **file**. Trả base id thì họ cầm một
    chuỗi không tồn tại trên đĩa."""
    got = relative_degradation(
        [_mr("a::digital", 0.9)], [_mr("a::scan", 0.5), _mr("z::scan", 0.5)]
    )
    assert got.excluded_doc_ids == ("z::scan",)


def test_sut_tuong_doi_tinh_tren_cap() -> None:
    digital = [_mr("a::digital", 0.80), _mr("b::digital", 0.60)]
    scan = [_mr("a::scan", 0.40), _mr("b::scan", 0.30)]
    got = relative_degradation(digital, scan)
    assert got.mean_digital == pytest.approx(0.70)
    assert got.mean_scan == pytest.approx(0.35)
    assert got.relative_drop == pytest.approx(0.50)
    assert got.kha_dung is True


def test_trung_binh_khong_lay_tren_tai_lieu_bi_loai() -> None:
    """Tài liệu chỉ có ở một bên **không** được vào trung bình của bên đó. Nếu vào
    thì `mean_digital` và `mean_scan` được tính trên hai tập khác nhau, và hiệu
    của chúng không còn là độ sụt của engine."""
    digital = [_mr("a::digital", 0.80), _mr("le::digital", 0.00)]
    scan = [_mr("a::scan", 0.40)]
    got = relative_degradation(digital, scan)
    assert got.mean_digital == pytest.approx(0.80)
    assert got.n_pairs == 1


# --- không có cặp: N/A, không phải 0 ----------------------------------------


def test_khong_co_cap_nao_thi_khong_kha_dung() -> None:
    """Bộ mẫu chưa có bản quét thì câu trả lời đúng là "chưa đo được", không phải
    "engine sụt 0%" (nghe như engine rất bền) và cũng không phải 0.0 (nghe như
    engine mất sạch điểm)."""
    got = relative_degradation([_mr("a::digital", 0.9)], [])
    assert got.n_pairs == 0
    assert got.kha_dung is False
    assert got.relative_drop is None
    assert got.mean_digital is None


def test_cap_chi_dem_khi_ca_hai_ben_deu_cham_duoc() -> None:
    """Một bên N/A thì cặp đó không đo được độ sụt. Coi N/A là 0 điểm ở bên quét
    sẽ biến "chưa chấm được" thành "sụt 100%"."""
    digital = [_mr("a::digital", 0.9), _mr("b::digital", 0.8)]
    scan = [_mr("a::scan", 0.5), _mr("b::scan", None, ly_do=NAReason.ENGINE_FAILED)]
    got = relative_degradation(digital, scan)
    assert got.n_pairs == 1
    assert "b::scan" in got.excluded_doc_ids


def test_diem_goc_bang_0_khong_gay_chia_cho_0() -> None:
    """Engine 0 điểm ở bản số thì "sụt bao nhiêu phần trăm" không có nghĩa. Trả
    `None` chứ không ném, và cũng không lặng lẽ trả 0.0."""
    got = relative_degradation([_mr("a::digital", 0.0)], [_mr("a::scan", 0.0)])
    assert got.n_pairs == 1
    assert got.relative_drop is None


def test_ket_qua_la_dataclass_bat_bien() -> None:
    got = relative_degradation([_mr("a::digital", 0.9)], [_mr("a::scan", 0.5)])
    assert isinstance(got, Degradation)
    with pytest.raises(Exception):
        got.n_pairs = 5  # type: ignore[misc]


def test_lan_lon_engine_thi_bao_loi() -> None:
    """Ghép độ sụt giữa hai engine khác nhau là so engine A với engine B rồi gọi
    đó là độ bền của một engine."""
    khac = MetricResult(metric="cer", engine="khac", doc_id="a::scan", value=0.5)
    with pytest.raises(ValueError, match="engine"):
        relative_degradation([_mr("a::digital", 0.9)], [khac])


def test_lan_lon_metric_thi_bao_loi() -> None:
    khac = MetricResult(metric="img_f1", engine="giả", doc_id="a::scan", value=0.5)
    with pytest.raises(ValueError, match="metric"):
        relative_degradation([_mr("a::digital", 0.9)], [khac])
