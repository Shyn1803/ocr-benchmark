"""CLI script to qualify all registered metrics against controlled sabotage and monotonicity controls.

Exits 0 if all main metrics pass qualification, or 2 if any main metric fails.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ocr_bench.metric_qualification import qualify_metrics_from_config

ROOT = Path(__file__).resolve().parent.parent


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
    args = parser.parse_args(argv)

    config_path: Path = args.config
    if not config_path.exists():
        sys.stderr.write(f"Error: Config file {config_path} not found.\n")
        return 2

    # Standard qualification controls for main metrics
    controls_map = {
        "cer": {"perfect": 1.0, "partial": 0.8, "severe": 0.3},
        "wer": {"perfect": 1.0, "partial": 0.75, "severe": 0.25},
        "diacritics": {"perfect": 1.0, "partial": 0.8, "severe": 0.4},
        "teds": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "teds_struct": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "cell_f1": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "table_recall": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "img_f1": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "img_iou": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "block_f1": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "type_f1": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "heading_f1": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "text_presence": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "math_presence": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "table_relation": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        "reading_order": {"perfect": 1.0, "partial": 0.7, "severe": 0.3},
    }

    report = qualify_metrics_from_config(config_path, controls_map=controls_map)

    out_path: Path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    sys.stdout.write(f"Qualification report written to {out_path}\n")

    if not report.all_main_passed:
        failed = [k for k, v in report.results.items() if v.category == "main" and v.status != "main"]
        sys.stderr.write(f"Error: Main metrics failed qualification: {failed}\n")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
