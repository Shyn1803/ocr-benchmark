"""Test publication trace comment validation."""

from __future__ import annotations

from pathlib import Path
import pytest

from ocr_bench.research_report import validate_publication_trace


def test_validate_publication_trace_passes_on_valid_paper(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    paper_dir.mkdir()
    (paper_dir / "paper-vi.md").write_text("# Paper\n<!-- trace: aggregate:text_ocr:marker_scan -->\n", encoding="utf-8")

    errors = validate_publication_trace(tmp_path)
    assert errors == []


def test_validate_publication_trace_fails_when_missing_trace(tmp_path: Path):
    paper_dir = tmp_path / "paper"
    paper_dir.mkdir()
    (paper_dir / "paper-vi.md").write_text("# Paper without trace\n", encoding="utf-8")

    errors = validate_publication_trace(tmp_path)
    assert len(errors) == 1
    assert "No trace comments found" in errors[0]
