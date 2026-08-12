"""Capability ranking and engine grouping module (Bands A / B / C).

Groups engines into performance bands A, B, and C based on statistical significance,
practical threshold delta, and effect size bands without scientific tie-breaking.
"""

from __future__ import annotations

from typing import Sequence

from ocr_bench.statistics import PairedComparison


def capability_groups(
    comparisons: Sequence[PairedComparison],
    *,
    practical_delta: float = 0.02,
) -> dict[str, str]:
    """Group engines into capability bands A, B, C.

    - Band A: Top performer or statistically/practically equivalent to top performer.
    - Band B: Moderate performance drop relative to top performer.
    - Band C: Substantial performance drop relative to top performer.
    """
    if not comparisons:
        return {}

    # Collect all engines and their means relative to opponents
    engine_scores: dict[str, list[float]] = {}
    for comp in comparisons:
        engine_scores.setdefault(comp.engine_a, []).append(comp.mean_a)
        engine_scores.setdefault(comp.engine_b, []).append(comp.mean_b)

    avg_means = {eng: sum(vals) / len(vals) for eng, vals in engine_scores.items()}
    if not avg_means:
        return {}

    top_engine = max(avg_means, key=avg_means.get)

    groups: dict[str, str] = {}

    for eng in avg_means:
        if eng == top_engine:
            groups[eng] = "A"
            continue

        # Find direct comparison with top engine
        comp = next(
            (
                c
                for c in comparisons
                if (c.engine_a == top_engine and c.engine_b == eng)
                or (c.engine_a == eng and c.engine_b == top_engine)
            ),
            None,
        )

        if comp is None:
            groups[eng] = "A"
            continue

        # Determine delta from top engine
        if comp.engine_a == top_engine:
            delta = comp.mean_delta
            p_val = comp.adjusted_p_value if comp.adjusted_p_value is not None else comp.p_value
            eff = abs(comp.effect_size)
        else:
            delta = -comp.mean_delta
            p_val = comp.adjusted_p_value if comp.adjusted_p_value is not None else comp.p_value
            eff = abs(comp.effect_size)

        # Check equivalence to top engine
        is_significant = p_val < 0.05
        is_material = delta >= practical_delta

        if not is_significant or not is_material:
            groups[eng] = "A"
        elif eff >= 0.6:
            groups[eng] = "C"
        else:
            groups[eng] = "B"

    return groups
