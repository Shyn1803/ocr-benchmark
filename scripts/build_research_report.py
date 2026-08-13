"""CLI Script to Build Research Report.

    py -3 scripts/build_research_report.py [--input DIR] [--out DIR]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ocr_bench.research_report import build_publication, validate_publication_trace  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build OCR Parser Benchmark Research Report")
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT,
        help="Input directory containing frozen study data / templates",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT,
        help="Output directory for publication artifacts",
    )
    parser.add_argument(
        "--prediction-dir",
        type=Path,
        default=None,
        help=(
            "Thư mục prediction đem đi chấm (mặc định: corpus đóng băng `prediction/`). "
            "Trỏ sang `calibration/prediction/cpu` để chấm đầu ra pilot — nhớ đổi cả "
            "`--out` để khỏi ghi đè bảng công bố."
        ),
    )
    args = parser.parse_args(argv)

    out_files = build_publication(args.input, args.out, prediction_dir=args.prediction_dir)
    sys.stdout.write(f"Generated {len(out_files)} publication artifacts under {args.out}\n")

    trace_errors = validate_publication_trace(args.out)
    if trace_errors:
        sys.stderr.write(f"Trace validation errors: {trace_errors}\n")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
