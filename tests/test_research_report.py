"""Test deterministic publication build pipeline and byte-identical output contract."""

from __future__ import annotations

import filecmp
from pathlib import Path
import pytest

from ocr_bench.research_report import build_publication, validate_publication_trace


def test_report_build_emits_all_required_artifacts(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    out_dir = tmp_path / "out"

    files = build_publication(input_dir, out_dir)

    required = {
        "paper/paper-vi.md",
        "paper/executive-summary.md",
        "results/raw-results.jsonl",
        "results/aggregate-results.json",
        "results/statistical-tests.json",
        "results/recommendations.json",
        "tables/text-ocr.md",
        "tables/layout.md",
        "tables/tables.md",
        "tables/reading-order.md",
        "tables/scan-robustness.md",
        "tables/performance.md",
        "figures/capability-ranking.svg",
        "figures/accuracy-speed.svg",
        "figures/scan-degradation.svg",
        "figures/failure-distribution.svg",
    }
    assert required <= set(files.keys())


def test_report_build_is_byte_identical_across_two_runs(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    out_a = tmp_path / "out_a"
    out_b = tmp_path / "out_b"

    files_a = build_publication(input_dir, out_a)
    files_b = build_publication(input_dir, out_b)

    for rel_path in files_a:
        path_a = files_a[rel_path]
        path_b = files_b[rel_path]

        assert path_a.read_bytes() == path_b.read_bytes(), f"Mismatch in {rel_path}"


def test_every_number_in_paper_has_trace_id(tmp_path: Path):
    out_dir = tmp_path / "out"
    build_publication(tmp_path, out_dir)
    errors = validate_publication_trace(out_dir)
    assert errors == []
