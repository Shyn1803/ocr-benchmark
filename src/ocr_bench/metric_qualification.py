"""Metric qualification gate module.

Enforces monotonicity controls and sabotage checks on all metrics before
allowing them into the main publication ranking.

Cổng này **đóng khi thiếu bằng chứng**. Ba trạng thái, không phải hai:

``passed``
    ``sabotage`` đo được và **thấp ngặt** hơn chính engine nguồn của nó (D-010).
``failed``
    Đo được nhưng không thấp hơn — metric không thấy phép làm hỏng.
``not_run``
    Không đo được (thiếu ``score_table``, thiếu engine, metric N/A). Đây **không**
    phải là đạt: một metric hạng ``main`` chưa qua cổng bị hạ xuống
    ``experimental``. Phiên bản trước coi ``not_run`` như đạt, nên
    ``scripts/qualify_metrics.py`` — vốn không bao giờ truyền ``score_table`` —
    chỉ có thể thoát ``0``, và điều kiện D-010 chưa từng chạy một lần nào.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Literal

GateStatus = Literal["passed", "failed", "not_run"]

GradedStatus = Literal["passed", "saturated", "failed", "not_run"]
"""Kết cục phép so **ba mức** phá hoại 0.1 / 0.3 / 0.6.

``saturated`` là trạng thái riêng có chủ ý, không gộp vào ``failed``: metric chạm sàn
ở mức nhẹ nhất rồi nằm im vẫn *thấy* phép làm hỏng (nên qua được cổng một điểm), nó
chỉ không xếp được **mức độ** hỏng. Nhiều metric nhị phân bắt buộc bão hoà — hạ chúng
vì điều đó là hạ vì một tính chất đúng. ``failed`` thì khác hẳn: mức nặng hơn được
điểm **cao hơn**, tức thước đo thưởng cho việc phá nhiều hơn.
"""


class UnknownMetricError(ValueError):
    """Registry khai một metric mà bộ chấm không có.

    Tên lệch là cách im lặng nhất để vô hiệu hoá cổng: ``kiem_sabotage()`` tra một
    tên không tồn tại thì trả "không đo được", và nếu ``not_run`` được coi là đạt
    thì cả bảng xanh mà không phép so nào chạy.
    """


@dataclasses.dataclass(frozen=True)
class QualificationResult:
    metric: str
    status: Literal["main", "experimental"]
    category: str
    reasons: tuple[str, ...]
    controls: dict[str, float]
    sabotage_source_diff: float | None = None
    passed_monotonicity: bool = True
    sabotage_gate: GateStatus = "not_run"
    sabotage_score: float | None = None
    source_score: float | None = None
    graded_gate: GradedStatus = "not_run"
    graded_scores: dict[str, float] | None = None
    graded_note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric": self.metric,
            "status": self.status,
            "category": self.category,
            "reasons": list(self.reasons),
            "controls": self.controls,
            "sabotage_source_diff": self.sabotage_source_diff,
            "passed_monotonicity": self.passed_monotonicity,
            "sabotage_gate": self.sabotage_gate,
            "sabotage_score": self.sabotage_score,
            "source_score": self.source_score,
            "graded_gate": self.graded_gate,
            "graded_scores": self.graded_scores,
            "graded_note": self.graded_note,
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
    require_sabotage_gate: bool = False,
    gate_note: str | None = None,
    graded_gate: GradedStatus = "not_run",
    graded_scores: dict[str, float] | None = None,
    graded_note: str | None = None,
) -> QualificationResult:
    """Qualify a single metric against control and sabotage monotonicity.

    ``require_sabotage_gate=True`` là chế độ công bố: metric hạng ``main`` không đo
    được cổng sabotage thì **không** được vào bảng chính. Mặc định ``False`` chỉ để
    kiểm riêng phần đối chứng đơn điệu trong unit test.
    """
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

    # 2. Sabotage monotonicity check — D-010: sabotage < chính engine nguồn, so ngặt.
    diff: float | None = None
    gate: GateStatus
    if sabotage_score is not None and source_score is not None:
        diff = sabotage_score - source_score
        if sabotage_score >= source_score:
            gate = "failed"
            passed_monotonicity = False
            reasons.append(
                f"Sabotage score ({sabotage_score:.4f}) is not strictly lower than source score ({source_score:.4f})"
            )
        else:
            gate = "passed"
    else:
        gate = "not_run"
        if require_sabotage_gate and category != "experimental":
            note = f" ({gate_note})" if gate_note else ""
            reasons.append(
                f"Sabotage gate did not run for '{metric}'{note} — a main metric without a "
                "measured sabotage comparison cannot be published (D-010 fail-closed)"
            )

    # 2b. Phép so ba mức. Chỉ ``failed`` (mức nặng hơn được điểm cao hơn) mới hạ hạng —
    # ``saturated`` là quan trắc, xem :data:`GradedStatus`.
    if graded_gate == "failed":
        passed_monotonicity = False
        reasons.append(
            f"Graded sabotage inversion for '{metric}': "
            f"{graded_note or 'a harsher corruption level scored higher than a milder one'}"
        )

    # 3. Determine final status
    if category == "experimental":
        status = "experimental"
        if not reasons:
            reasons.append("Registered as experimental metric in registry")
    elif not passed_monotonicity:
        status = "experimental"
    elif gate == "not_run" and require_sabotage_gate:
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
        sabotage_gate=gate,
        sabotage_score=sabotage_score,
        source_score=source_score,
        graded_gate=graded_gate,
        graded_scores=graded_scores,
        graded_note=graded_note,
    )


_MAP_DON_DIEU: dict[str, GradedStatus] = {
    "dat": "passed",
    "bao_hoa": "saturated",
    "nghich": "failed",
    "khong_do_duoc": "not_run",
}


def _co_cot_phan_muc(score_table: Any) -> bool:
    """Bảng có mang theo quần thể ba mức không (để phân biệt "chưa dựng" với "N/A")."""
    from ocr_bench.adapters.sabotage import MUC_SABOTAGE, ten_muc_sabotage

    can = {ten_muc_sabotage(s) for s in MUC_SABOTAGE}
    try:
        return can <= set(score_table.engines())
    except AttributeError:
        return False


def _known_metric_names() -> set[str]:
    from ocr_bench import registry

    return set(registry.list_metrics())


def qualify_metrics_from_config(
    config_path: Path,
    *,
    score_table: Any = None,
    controls_map: dict[str, dict[str, float]] | None = None,
    require_sabotage_gate: bool = True,
    validate_against_registry: bool = True,
) -> MetricQualificationReport:
    """Qualify all metrics defined in `config_path` (`configs/metric-registry.json`).

    Mặc định là chế độ công bố: tên metric phải có thật trong bộ chấm, và metric
    hạng ``main`` phải qua được cổng sabotage đo trên ``score_table``.
    """
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    metrics_cfg: dict[str, dict[str, Any]] = raw.get("metrics", {})

    if validate_against_registry:
        known = _known_metric_names()
        unknown = sorted(set(metrics_cfg) - known)
        if unknown:
            raise UnknownMetricError(
                f"metric-registry.json khai {len(unknown)} metric không có trong bộ chấm: "
                f"{unknown}. Tên hợp lệ: {sorted(known)}"
            )

    results: dict[str, QualificationResult] = {}
    controls_map = controls_map or {}

    for metric_name, cfg in metrics_cfg.items():
        cat = cfg.get("category", "main")
        ctrls = controls_map.get(metric_name)

        sab_score: float | None = None
        src_score: float | None = None
        note: str | None = None
        graded: GradedStatus = "not_run"
        graded_scores: dict[str, float] | None = None
        graded_note: str | None = None

        if score_table is None:
            note = "no score_table supplied"
        else:
            # Lỗi ở đây không được nuốt: import hỏng hay metric sai tên là đúng cái
            # cổng này sinh ra để bắt, nuốt đi thì cổng trở thành cổng rỗng.
            from ocr_bench.discrimination import (
                NGUON_SABOTAGE,
                kiem_don_dieu_muc,
                kiem_sabotage,
            )

            kq = kiem_sabotage(score_table, metric_name, nguon=NGUON_SABOTAGE)
            if kq.do_duoc:
                sab_score = kq.diem_sabotage
                src_score = kq.diem_nguon
            else:
                note = getattr(kq, "ly_do", None) or "sabotage/source not measurable"

            dd = kiem_don_dieu_muc(score_table, metric_name, nguon=NGUON_SABOTAGE)
            graded = _MAP_DON_DIEU[dd.phan_quyet]
            graded_note = dd.ly_do
            graded_scores = dict(dd.diem) if dd.diem else None
            if graded == "not_run" and not _co_cot_phan_muc(score_table):
                graded_note = (
                    "graded sabotage populations absent from the score table — "
                    "build them with discrimination.dung_sabotage_phan_muc()"
                )

        results[metric_name] = qualify_metric(
            metric_name,
            controls=ctrls,
            sabotage_score=sab_score,
            source_score=src_score,
            category=cat,
            require_sabotage_gate=require_sabotage_gate,
            gate_note=note,
            graded_gate=graded,
            graded_scores=graded_scores,
            graded_note=graded_note,
        )

    all_main_passed = all(
        res.status == "main"
        for name, res in results.items()
        if metrics_cfg.get(name, {}).get("category") == "main"
    )

    gate_counts = {
        state: sum(1 for r in results.values() if r.sabotage_gate == state)
        for state in ("passed", "failed", "not_run")
    }

    summary = {
        "total_metrics": len(results),
        "main_passed": sum(1 for r in results.values() if r.status == "main"),
        "experimental_count": sum(1 for r in results.values() if r.status == "experimental"),
        "all_main_passed": all_main_passed,
        "sabotage_gate": gate_counts,
        "graded_gate": {
            state: sum(1 for r in results.values() if r.graded_gate == state)
            for state in ("passed", "saturated", "failed", "not_run")
        },
        "require_sabotage_gate": require_sabotage_gate,
    }

    return MetricQualificationReport(
        all_main_passed=all_main_passed,
        results=results,
        summary=summary,
    )
