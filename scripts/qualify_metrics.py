"""CLI script to qualify all registered metrics against controlled sabotage and monotonicity controls.

    py -3 scripts/qualify_metrics.py

Chấm lại dự đoán đã lưu ở `prediction/`, dựng `sabotage` bằng chính `SabotageAdapter`
thật (nguồn = `discrimination.NGUON_SABOTAGE`), rồi đưa bảng điểm đó vào cổng thẩm
định. Không chạy engine nào, không đụng PDF — cùng đường đi mà `scripts/c2_report.py`
dùng.

Exits 0 if all main metrics pass qualification, or 2 if any main metric fails **or the
gate could not run**. Cổng không chạy được thì không có gì để tuyên bố là đạt: bản
trước dựng `controls_map` cứng rồi gọi cổng mà không hề truyền `score_table`, nên phép
so D-010 (`sabotage` thấp ngặt hơn engine nguồn) chưa từng thực thi và script chỉ có
thể thoát `0`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ocr_bench.metric_qualification import (  # noqa: E402
    UnknownMetricError,
    qualify_metrics_from_config,
)

# Đối chứng đơn điệu: điểm mong đợi trên bản hoàn hảo / hỏng vừa / hỏng nặng. Đây là
# phần *không* phụ thuộc corpus; phép so thật với `sabotage` lấy từ `score_table`.
CONTROLS_MAP: dict[str, dict[str, float]] = {
    "cer": {"perfect": 1.0, "partial": 0.8, "severe": 0.3},
    "wer": {"perfect": 1.0, "partial": 0.75, "severe": 0.25},
    "diacritics_acc": {"perfect": 1.0, "partial": 0.8, "severe": 0.4},
    "teds": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "teds_struct": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "cell_f1": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "table_recall": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "img_f1": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "img_iou": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "block_f1": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "type_f1": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "heading": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "assert_text_presence": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "assert_math_presence": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "assert_table_relation": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    "assert_reading_order": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
}


def build_score_table(prediction_dir: Path):
    """Chấm lại corpus đã lưu + `sabotage` dựng từ engine nguồn.

    Cùng phép dựng mà `scripts/c2_report.py` dùng. Ném ra ngoài nếu thiếu dữ liệu —
    người gọi phải thấy, không được coi là "cổng đạt".
    """
    from ocr_bench import discrimination as D
    from ocr_bench import registry
    from ocr_bench.corpus import load_doclaynet, load_olmocr
    from ocr_bench.prediction import load_predictions
    from ocr_bench.scorer import score_results

    gt: dict = {}
    gt.update(load_doclaynet())
    gt.update(load_olmocr())

    res = load_predictions(prediction_dir)
    if not res:
        raise FileNotFoundError(f"không có dự đoán nào ở {prediction_dir}")
    if not any(r.engine == D.NGUON_SABOTAGE for r in res):
        raise FileNotFoundError(
            f"không có dự đoán nào của engine nguồn '{D.NGUON_SABOTAGE}' — "
            "cổng D-010 so sabotage với chính nguồn của nó, thiếu nguồn thì không so được"
        )

    sab = D.dung_sabotage(res)
    # Cộng thêm ba mức 0.1/0.3/0.6 để phép so đơn điệu theo mức có cột mà chấm. Thiếu
    # chúng thì `graded_gate` báo `not_run` — không phải `passed`.
    sab += D.dung_sabotage_phan_muc(res)
    metrics = [registry.get_metric(t)() for t in sorted(registry.list_metrics())]
    goc = [r for r in res if not r.engine.startswith("sabotage")]
    return score_results(goc + sab, metrics, gt)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Qualify benchmark metrics")
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs" / "metric-registry.json",
        help="Path to metric registry JSON config",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results" / "metric-qualification.json",
        help="Output JSON file for qualification results",
    )
    parser.add_argument(
        "--prediction-dir",
        type=Path,
        default=ROOT / "prediction",
        help="Directory of stored predictions used to rebuild the score table",
    )
    parser.add_argument(
        "--no-score-table",
        action="store_true",
        help=(
            "Chỉ kiểm đối chứng đơn điệu, bỏ qua cổng sabotage. Luôn thoát 2: "
            "không chạy cổng thì không có gì để chứng nhận."
        ),
    )
    args = parser.parse_args(argv)

    config_path: Path = args.config
    if not config_path.exists():
        sys.stderr.write(f"Error: Config file {config_path} not found.\n")
        return 2

    score_table = None
    if not args.no_score_table:
        try:
            score_table = build_score_table(args.prediction_dir)
        except Exception as exc:  # noqa: BLE001 — báo ra rồi thoát 2, không nuốt
            sys.stderr.write(
                f"Error: không dựng được bảng điểm nên cổng sabotage không chạy: {exc}\n"
                "Cổng không chạy KHÔNG phải là cổng đạt — xem D-010.\n"
            )
            return 2

    try:
        report = qualify_metrics_from_config(
            config_path,
            score_table=score_table,
            controls_map=CONTROLS_MAP,
            require_sabotage_gate=True,
        )
    except UnknownMetricError as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 2

    out_path: Path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Ghi bytes chứ không `write_text`: trên Windows `write_text` đổi `\n` thành `\r\n`,
    # nên cùng một báo cáo lại ra hai tệp khác nhau tuỳ hệ điều hành.
    out_path.write_bytes(
        (json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    )

    sys.stdout.write(f"Qualification report written to {out_path}\n")
    gates = report.summary["sabotage_gate"]
    sys.stdout.write(
        f"sabotage gate: passed={gates['passed']} failed={gates['failed']} not_run={gates['not_run']}\n"
    )
    g = report.summary["graded_gate"]
    sys.stdout.write(
        f"graded gate (0.1/0.3/0.6): passed={g['passed']} saturated={g['saturated']} "
        f"failed={g['failed']} not_run={g['not_run']}\n"
    )

    if args.no_score_table:
        sys.stderr.write(
            "Error: --no-score-table nghĩa là cổng sabotage chưa chạy; không chứng nhận.\n"
        )
        return 2

    if not report.all_main_passed:
        failed = [k for k, v in report.results.items() if v.category == "main" and v.status != "main"]
        sys.stderr.write(f"Error: Main metrics failed qualification: {failed}\n")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
