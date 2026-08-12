"""Test research charts SVG generation."""

from __future__ import annotations

from pathlib import Path
import pytest

from ocr_bench.research_charts import (
    render_accuracy_speed_chart,
    render_failure_distribution_chart,
    render_forest_plot,
    render_scan_degradation_chart,
)


def test_svg_charts_generation(tmp_path: Path):
    forest = render_forest_plot({}, tmp_path / "forest.svg")
    assert forest.exists()
    assert "<svg" in forest.read_text(encoding="utf-8")

    pareto = render_accuracy_speed_chart({}, tmp_path / "pareto.svg")
    assert pareto.exists()
    assert "<svg" in pareto.read_text(encoding="utf-8")

    deg = render_scan_degradation_chart({}, tmp_path / "deg.svg")
    assert deg.exists()
    assert "<svg" in deg.read_text(encoding="utf-8")

    fail = render_failure_distribution_chart({}, tmp_path / "fail.svg")
    assert fail.exists()
    assert "<svg" in fail.read_text(encoding="utf-8")
