"""Paired statistical comparison and percentile bootstrap module (Pure Python).

Computes paired document-level comparisons, 95% bootstrap confidence intervals,
Wilcoxon signed-rank tests, Holm-Bonferroni p-value corrections, and
matched-pairs rank-biserial effect sizes without external third-party dependencies.
"""

from __future__ import annotations

import dataclasses
import hashlib
import math
import random
import statistics
from typing import Sequence


@dataclasses.dataclass(frozen=True)
class PairedComparison:
    engine_a: str
    engine_b: str
    doc_ids: tuple[str, ...]
    doc_ids_sha256: str
    mean_a: float
    mean_b: float
    mean_delta: float
    ci_95_low: float
    ci_95_high: float
    p_value: float
    adjusted_p_value: float | None = None
    effect_size: float = 0.0
    status: str = "not_significant"

    def to_dict(self) -> dict[str, object]:
        return {
            "engine_a": self.engine_a,
            "engine_b": self.engine_b,
            "n_docs": len(self.doc_ids),
            "doc_ids_sha256": self.doc_ids_sha256,
            "mean_a": round(self.mean_a, 4),
            "mean_b": round(self.mean_b, 4),
            "mean_delta": round(self.mean_delta, 4),
            "ci_95": [round(self.ci_95_low, 4), round(self.ci_95_high, 4)],
            "p_value": round(self.p_value, 6),
            "adjusted_p_value": (
                round(self.adjusted_p_value, 6)
                if self.adjusted_p_value is not None
                else None
            ),
            "effect_size": round(self.effect_size, 4),
            "status": self.status,
        }


def _normal_cdf(x: float) -> float:
    """Standard normal cumulative distribution function using math.erf."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _wilcoxon_signed_rank(deltas: list[float]) -> tuple[float, float]:
    """Pure Python Wilcoxon signed-rank test.

    Returns (statistic, p_value). Returns (0.0, 1.0) if all deltas are zero.
    """
    non_zero = [d for d in deltas if abs(d) > 1e-12]
    n = len(non_zero)
    if n == 0:
        return 0.0, 1.0

    # Sort by absolute value along with sign
    abs_items = sorted((abs(d), d) for d in non_zero)

    # Assign fractional ranks for ties
    ranks: list[float] = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n and abs(abs_items[j][0] - abs_items[i][0]) < 1e-12:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    r_plus = sum(r for r, (_, val) in zip(ranks, abs_items) if val > 0)
    r_minus = sum(r for r, (_, val) in zip(ranks, abs_items) if val < 0)

    stat = min(r_plus, r_minus)

    # Normal approximation for z-statistic
    t_sum = 0.0  # Tie correction term
    # Group sizes for ties
    i = 0
    while i < n:
        j = i
        while j < n and abs(abs_items[j][0] - abs_items[i][0]) < 1e-12:
            j += 1
        t_size = j - i
        if t_size > 1:
            t_sum += t_size**3 - t_size
        i = j

    mean_w = n * (n + 1) / 4.0
    var_w = n * (n + 1) * (2 * n + 1) / 24.0 - t_sum / 48.0

    if var_w <= 0:
        return stat, 1.0

    std_w = math.sqrt(var_w)
    # Continuity correction
    z = (abs(stat - mean_w) - 0.5) / std_w
    p_val = 2.0 * (1.0 - _normal_cdf(abs(z)))
    p_val = max(0.0, min(1.0, p_val))

    return stat, p_val


def _effect_size_rank_biserial(deltas: list[float]) -> float:
    """Matched-pairs rank-biserial correlation: r = (R+ - R-) / (R+ + R-)."""
    non_zero = [d for d in deltas if abs(d) > 1e-12]
    n = len(non_zero)
    if n == 0:
        return 0.0

    abs_items = sorted((abs(d), d) for d in non_zero)
    ranks: list[float] = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n and abs(abs_items[j][0] - abs_items[i][0]) < 1e-12:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    r_plus = sum(r for r, (_, val) in zip(ranks, abs_items) if val > 0)
    r_minus = sum(r for r, (_, val) in zip(ranks, abs_items) if val < 0)
    total = r_plus + r_minus

    return (r_plus - r_minus) / total if total > 0 else 0.0


def paired_compare(
    scores_a: dict[str, float],
    scores_b: dict[str, float],
    *,
    engine_a: str = "engine_a",
    engine_b: str = "engine_b",
    n_resamples: int = 10000,
    seed: int = 20260811,
) -> PairedComparison:
    """Perform paired document-level statistical comparison between two engines."""
    common_docs = sorted(set(scores_a.keys()) & set(scores_b.keys()))
    doc_hash = hashlib.sha256(",".join(common_docs).encode("utf-8")).hexdigest()

    if not common_docs:
        return PairedComparison(
            engine_a=engine_a,
            engine_b=engine_b,
            doc_ids=(),
            doc_ids_sha256=doc_hash,
            mean_a=0.0,
            mean_b=0.0,
            mean_delta=0.0,
            ci_95_low=0.0,
            ci_95_high=0.0,
            p_value=1.0,
            adjusted_p_value=1.0,
            effect_size=0.0,
            status="identical",
        )

    vals_a = [float(scores_a[d]) for d in common_docs]
    vals_b = [float(scores_b[d]) for d in common_docs]
    deltas = [a - b for a, b in zip(vals_a, vals_b)]

    mean_a = statistics.mean(vals_a)
    mean_b = statistics.mean(vals_b)
    mean_delta = statistics.mean(deltas)

    if all(abs(d) < 1e-12 for d in deltas):
        return PairedComparison(
            engine_a=engine_a,
            engine_b=engine_b,
            doc_ids=tuple(common_docs),
            doc_ids_sha256=doc_hash,
            mean_a=mean_a,
            mean_b=mean_b,
            mean_delta=0.0,
            ci_95_low=0.0,
            ci_95_high=0.0,
            p_value=1.0,
            adjusted_p_value=1.0,
            effect_size=0.0,
            status="identical",
        )

    # 1. Percentile Paired Bootstrap
    rng = random.Random(seed)
    n_docs = len(deltas)
    boot_means: list[float] = []
    for _ in range(n_resamples):
        sample = rng.choices(deltas, k=n_docs)
        boot_means.append(statistics.mean(sample))

    boot_means.sort()
    idx_low = int(0.025 * n_resamples)
    idx_high = int(0.975 * n_resamples)
    ci_low = boot_means[idx_low]
    ci_high = boot_means[idx_high]

    # 2. Wilcoxon signed-rank test
    _, p_val = _wilcoxon_signed_rank(deltas)

    # 3. Matched-pairs rank-biserial correlation
    effect_size = _effect_size_rank_biserial(deltas)

    status = "significant" if p_val < 0.05 else "not_significant"

    return PairedComparison(
        engine_a=engine_a,
        engine_b=engine_b,
        doc_ids=tuple(common_docs),
        doc_ids_sha256=doc_hash,
        mean_a=mean_a,
        mean_b=mean_b,
        mean_delta=mean_delta,
        ci_95_low=ci_low,
        ci_95_high=ci_high,
        p_value=p_val,
        adjusted_p_value=p_val,
        effect_size=effect_size,
        status=status,
    )


def adjust_p_values_holm(
    comparisons: Sequence[PairedComparison],
) -> list[PairedComparison]:
    """Apply Holm-Bonferroni correction to a family of p-values."""
    if not comparisons:
        return []

    indexed = sorted(enumerate(comparisons), key=lambda x: x[1].p_value)
    m = len(indexed)
    adjusted_list: list[float] = [1.0] * m

    cum_max = 0.0
    for k, (orig_idx, comp) in enumerate(indexed):
        adjusted_p = min(1.0, comp.p_value * (m - k))
        cum_max = max(cum_max, adjusted_p)
        adjusted_list[orig_idx] = cum_max

    result: list[PairedComparison] = []
    for idx, comp in enumerate(comparisons):
        adj_p = adjusted_list[idx]
        st = (
            comp.status
            if comp.status == "identical"
            else ("significant" if adj_p < 0.05 else "not_significant")
        )
        result.append(
            dataclasses.replace(comp, adjusted_p_value=adj_p, status=st)
        )

    return result
