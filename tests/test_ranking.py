"""Test capability ranking and band A/B/C assignment."""

from __future__ import annotations

import pytest

from ocr_bench.ranking import capability_groups
from ocr_bench.statistics import PairedComparison


def test_rank_ties_best_when_difference_is_not_material():
    # Construct mock comparison results where delta is small (< practical_delta)
    comparisons = [
        PairedComparison(
            engine_a="engine_a",
            engine_b="engine_b",
            doc_ids=("d1", "d2"),
            doc_ids_sha256="dummy_hash",
            mean_a=0.90,
            mean_b=0.89,
            mean_delta=0.01,
            ci_95_low=0.005,
            ci_95_high=0.015,
            p_value=0.20,
            adjusted_p_value=0.20,
            effect_size=0.05,
            status="not_significant",
        )
    ]

    groups = capability_groups(comparisons, practical_delta=0.02)
    assert groups["engine_a"] == "A"
    assert groups["engine_b"] == "A"


def test_rank_separates_engine_when_difference_is_significant_and_material():
    comparisons = [
        PairedComparison(
            engine_a="engine_a",
            engine_b="engine_b",
            doc_ids=("d1", "d2"),
            doc_ids_sha256="dummy_hash",
            mean_a=0.95,
            mean_b=0.70,
            mean_delta=0.25,
            ci_95_low=0.20,
            ci_95_high=0.30,
            p_value=0.001,
            adjusted_p_value=0.005,
            effect_size=0.80,
            status="significant",
        )
    ]

    groups = capability_groups(comparisons, practical_delta=0.02)
    assert groups["engine_a"] == "A"
    assert groups["engine_b"] in ("B", "C")
