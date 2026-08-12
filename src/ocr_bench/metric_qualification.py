"""Metric qualification gate module.

Enforces monotonicity controls and sabotage checks on all metrics before
allowing them into the main publication ranking.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Literal


@dataclasses.dataclass(frozen=True)
class QualificationResult:
    metric: str
    status: Literal["main", "experimental"]
    category: str
    reasons: tuple[str, ...]
    controls: dict[str, float]
    sabotage_source_diff: float | None = None
    passed_monotonicity: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric": self.metric,
            "status": self.status,
            "category": self.category,
            "reasons": list(self.reasons),
            "controls": self.controls,
            "sabotage_source_diff": self.sabotage_source_diff,
            "passed_monotonicity": self.passed_monotonicity,
        }


@dataclasses.dataclass(frozen=True)
class MetricQualificationReport:
    all_main_passed: bool
    results: dict[str, QualificationResult]
    summary: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "all_main_passed": self.all_main_passed,
            "results": {k: v.to_dict() for k, v in self.results.items()},
            "summary": self.summary,
        }


def qualify_metric(
    metric: str,
    *,
    controls: dict[str, float] | None = None,
    sabotage_score: float | None = None,
    source_score: float | None = None,
    category: str = "main",
) -> QualificationResult:
    """Qualify a single metric against control and sabotage monotonicity."""
    reasons: list[str] = []
    passed_monotonicity = True
    ctrls = controls.copy() if controls else {}

    # 1. Monotonicity check on controls (perfect >= partial >= severe)
    if ctrls:
        perfect = ctrls.get("perfect", 1.0)
        partial = ctrls.get("partial")
        severe = ctrls.get("severe")

        if partial is not None and perfect < partial:
            passed_monotonicity = False
            reasons.append(
                f"Monotonicity violation in controls: perfect ({perfect:.4f}) < partial ({partial:.4f})"
            )
        if severe is not None and partial is not None and partial < severe:
            passed_monotonicity = False
            reasons.append(
                f"Monotonicity violation in controls: partial ({partial:.4f}) < severe ({severe:.4f})"
            )
        if severe is not None and partial is None and perfect < severe:
            passed_monotonicity = False
            reasons.append(
                f"Monotonicity violation in controls: perfect ({perfect:.4f}) < severe ({severe:.4f})"
            )

    # 2. Sabotage monotonicity check (sabotage_score < source_score)
    diff: float | None = None
    if sabotage_score is not None and source_score is not None:
        diff = sabotage_score - source_score
        if sabotage_score >= source_score:
            passed_monotonicity = False
            reasons.append(
                f"Sabotage score ({sabotage_score:.4f}) is not strictly lower than source score ({source_score:.4f})"
            )

    # 3. Determine final status
    if category == "experimental":
        status = "experimental"
        if not reasons:
            reasons.append("Registered as experimental metric in registry")
    elif not passed_monotonicity:
        status = "experimental"
    else:
        status = "main"

    return QualificationResult(
        metric=metric,
        status=status,
        category=category,
        reasons=tuple(reasons),
        controls=ctrls,
        sabotage_source_diff=diff,
        passed_monotonicity=passed_monotonicity,
    )


def qualify_metrics_from_config(
    config_path: Path,
    *,
    score_table: Any = None,
    controls_map: dict[str, dict[str, float]] | None = None,
) -> MetricQualificationReport:
    """Qualify all metrics defined in `config_path` (`configs/metric-registry.json`)."""
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    metrics_cfg: dict[str, dict[str, Any]] = raw.get("metrics", {})

    results: dict[str, QualificationResult] = {}
    controls_map = controls_map or {}

    for metric_name, cfg in metrics_cfg.items():
        cat = cfg.get("category", "main")
        ctrls = controls_map.get(metric_name)

        sab_score: float | None = None
        src_score: float | None = None

        if score_table is not None:
            # Look up sabotage and source scores from ScoreTable if available
            try:
                from ocr_bench.discrimination import NGUON_SABOTAGE, kiem_sabotage
                kq = kiem_sabotage(score_table, metric_name, nguon=NGUON_SABOTAGE)
                if kq.do_duoc:
                    sab_score = kq.diem_sabotage
                    src_score = kq.diem_nguon
            except Exception:
                pass

        results[metric_name] = qualify_metric(
            metric_name,
            controls=ctrls,
            sabotage_score=sab_score,
            source_score=src_score,
            category=cat,
        )

    all_main_passed = all(
        res.status == "main"
        for name, res in results.items()
        if metrics_cfg.get(name, {}).get("category") == "main"
    )

    summary = {
        "total_metrics": len(results),
        "main_passed": sum(1 for r in results.values() if r.status == "main"),
        "experimental_count": sum(1 for r in results.values() if r.status == "experimental"),
        "all_main_passed": all_main_passed,
    }

    return MetricQualificationReport(
        all_main_passed=all_main_passed,
        results=results,
        summary=summary,
    )
