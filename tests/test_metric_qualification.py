"""Test metric qualification gate & controlled sabotage monotonicity."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from ocr_bench.metric_qualification import (
    MetricQualificationReport,
    QualificationResult,
    qualify_metric,
    qualify_metrics_from_config,
)


def test_qualify_metric_accepts_monotonic_controls():
    result = qualify_metric(
        metric="good_metric",
        controls={"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        category="main",
    )
    assert result.status == "main"
    assert result.passed_monotonicity is True
    assert len(result.reasons) == 0


def test_qualify_metric_rejects_monotonic_violations():
    result = qualify_metric(
        metric="bad_metric",
        controls={"perfect": 1.0, "partial": 0.4, "severe": 0.6},
        category="main",
    )
    assert result.status == "experimental"
    assert result.passed_monotonicity is False
    assert any("monotonic" in r.lower() for r in result.reasons)


def test_qualify_metric_rejects_non_decreasing_sabotage():
    # When sabotage score is not strictly lower than source score
    result = qualify_metric(
        metric="non_monotonic_sabotage",
        sabotage_score=0.8,
        source_score=0.8,
        category="main",
    )
    assert result.status == "experimental"
    assert result.passed_monotonicity is False
    assert any("sabotage" in r.lower() or "source" in r.lower() for r in result.reasons)


def test_qualify_metrics_from_config(tmp_path: Path):
    config = {
        "metrics": {
            "cer": {"category": "main", "capability": "text_md", "practical_delta": 0.02},
            "bad_metric": {"category": "main", "capability": "text_md", "practical_delta": 0.05},
            "exp_metric": {"category": "experimental", "capability": "layout", "practical_delta": 0.05},
        }
    }
    cfg_file = tmp_path / "metric-registry.json"
    cfg_file.write_text(json.dumps(config), encoding="utf-8")

    controls_map = {
        "cer": {"perfect": 1.0, "partial": 0.8, "severe": 0.4},
        "bad_metric": {"perfect": 1.0, "partial": 0.3, "severe": 0.5},
        "exp_metric": {"perfect": 1.0, "partial": 0.5, "severe": 0.2},
    }

    report = qualify_metrics_from_config(cfg_file, controls_map=controls_map)
    assert isinstance(report, MetricQualificationReport)
    assert report.all_main_passed is False
    assert report.results["cer"].status == "main"
    assert report.results["bad_metric"].status == "experimental"
    assert report.results["exp_metric"].status == "experimental"
