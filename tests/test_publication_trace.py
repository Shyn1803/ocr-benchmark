"""Trace ID phải **giải được** về aggregate thật, không chỉ tồn tại như chuỗi ký tự."""

from __future__ import annotations

import json
from pathlib import Path

from ocr_bench.research_report import MOI_METRIC, slug_nang_luc, validate_publication_trace


def _dung(tmp_path: Path, paper: str, aggregates: dict | None = None) -> Path:
    (tmp_path / "paper").mkdir(exist_ok=True)
    (tmp_path / "paper" / "paper-vi.md").write_text(paper, encoding="utf-8")
    if aggregates is not None:
        (tmp_path / "results").mkdir(exist_ok=True)
        (tmp_path / "results" / "aggregate-results.json").write_text(
            json.dumps({"generated_at": "T", "aggregates": aggregates}), encoding="utf-8"
        )
    return tmp_path


AGG = {"cer": {"marker_scan": {"mean": 0.5}}, "block_f1": {"marker_scan": {"mean": 0.4}}}


def test_trace_giai_duoc_thi_sach(tmp_path: Path):
    _dung(tmp_path, "# Paper\n<!-- trace: aggregate:text_ocr:marker_scan -->\n", AGG)
    assert validate_publication_trace(tmp_path) == []


def test_thieu_trace_thi_bao(tmp_path: Path):
    _dung(tmp_path, "# Paper không trace\n", AGG)
    errors = validate_publication_trace(tmp_path)
    assert len(errors) == 1
    assert "No resolvable trace" in errors[0]


def test_trace_phu_ca_bang_khong_con_duoc_coi_la_hop_le(tmp_path: Path):
    """`aggregate:all_metrics:all_engines` không trỏ tới bản ghi nào.

    Đây chính là trace duy nhất mà bài báo từng mang: nó qua được bộ kiểm cũ vì bộ
    kiểm cũ chỉ tìm chuỗi `"<!-- trace:"`.
    """
    _dung(tmp_path, "<!-- trace: aggregate:all_metrics:all_engines -->\n", AGG)
    errors = validate_publication_trace(tmp_path)
    assert errors and "all_engines" in errors[0]


def test_engine_khong_co_trong_aggregate_thi_bao(tmp_path: Path):
    _dung(tmp_path, "<!-- trace: aggregate:text_ocr:khong_ton_tai -->\n", AGG)
    errors = validate_publication_trace(tmp_path)
    assert errors and "khong_ton_tai" in errors[0]


def test_nang_luc_bia_thi_bao(tmp_path: Path):
    _dung(tmp_path, "<!-- trace: aggregate:nang_luc_bia:marker_scan -->\n", AGG)
    errors = validate_publication_trace(tmp_path)
    assert errors and "không có thật" in errors[0]


def test_nang_luc_khong_co_metric_nao_trong_aggregate_thi_bao(tmp_path: Path):
    """Trace trỏ tới một bảng rỗng cũng là trace không truy được số nào."""
    _dung(tmp_path, "<!-- trace: aggregate:tables:marker_scan -->\n", AGG)
    errors = validate_publication_trace(tmp_path)
    assert errors and "không giải được về metric nào" in errors[0]


def test_thieu_aggregate_thi_bao_chu_khong_im(tmp_path: Path):
    _dung(tmp_path, "<!-- trace: aggregate:text_ocr:marker_scan -->\n")
    errors = validate_publication_trace(tmp_path)
    assert errors and "aggregate-results.json" in errors[0]


def test_slug_nang_luc():
    assert slug_nang_luc("Text & OCR") == "text_ocr"
    assert slug_nang_luc("Layout & Structure") == "layout_structure"
    assert slug_nang_luc("Reading Order") == "reading_order"


def test_moi_metric_van_can_engine_co_that(tmp_path: Path):
    """`all_metrics` được miễn kiểm năng lực, nhưng không được miễn kiểm engine."""
    _dung(tmp_path, f"<!-- trace: aggregate:{MOI_METRIC}:marker_scan -->\n", AGG)
    assert validate_publication_trace(tmp_path) == []

    _dung(tmp_path, f"<!-- trace: aggregate:{MOI_METRIC}:ma -->\n", AGG)
    assert validate_publication_trace(tmp_path)
