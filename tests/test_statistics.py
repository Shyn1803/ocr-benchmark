"""Test paired statistical comparison and bootstrap analysis."""

from __future__ import annotations

import pytest

from ocr_bench.statistics import PairedComparison, paired_compare


def test_paired_comparison_uses_intersection_and_is_seeded():
    a = {f"d{i}": 0.9 for i in range(10)}
    a["a-only"] = 1.0

    b = {f"d{i}": 0.7 for i in range(10)}
    b["b-only"] = 0.0

    res1 = paired_compare(a, b, n_resamples=1000, seed=20260811)
    res2 = paired_compare(a, b, n_resamples=1000, seed=20260811)

    assert res1 == res2
    assert len(res1.doc_ids) == 10
    assert res1.mean_delta == pytest.approx(0.2)
    assert len(res1.doc_ids_sha256) == 64
    assert res1.p_value < 0.05
    assert res1.status == "significant"


def test_paired_comparison_handles_all_zero_deltas_without_raising():
    a = {"d1": 0.8, "d2": 0.8}
    b = {"d1": 0.8, "d2": 0.8}

    res = paired_compare(a, b, n_resamples=100, seed=20260811)

    assert res.mean_delta == 0.0
    assert res.status == "identical"
    assert res.p_value == 1.0
    assert res.effect_size == 0.0
