"""Sinh bản công bố D1 và lưu vào `history/` — TASK-087.

    py -3 scripts/d1_report.py [--out DIR] [--force]

Chấm lại từ `prediction/` (không chạy engine nào, không đụng PDF) rồi ghi 5 file:

    history/<YYYY-MM-DD>/manifest.json     — version engine + thư viện + git + coverage
    history/<YYYY-MM-DD>/overall.md        — bảng gộp, kèm cỡ mẫu và cảnh báo so chéo
    history/<YYYY-MM-DD>/by_group.md       — tách theo nhóm tài liệu (AC-02)
    history/<YYYY-MM-DD>/common_set.md     — bảng duy nhất so chéo được
    history/<YYYY-MM-DD>/raw.json          — điểm thô, tất định (AC-04)

`--force` là bắt buộc để ghi đè một thư mục đã có. Ghi đè lặng lẽ một bản `history/`
là làm mất đúng thứ task này sinh ra để giữ.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "src"))

from ocr_bench import registry, report  # noqa: E402
from ocr_bench.corpus import load_doclaynet, load_olmocr  # noqa: E402
from ocr_bench.prediction import load_predictions  # noqa: E402
from ocr_bench.scorer import ScoreTable, score_results  # noqa: E402


def _cham() -> tuple[list, ScoreTable]:
    gt: dict = {}
    gt.update(load_doclaynet())
    gt.update(load_olmocr())

    res = load_predictions(GOC / "prediction")
    ten = sorted(registry.list_metrics())
    metrics = [registry.get_metric(t)() for t in ten]
    print(f"nạp {len(res)} dự đoán · {len(ten)} metric")
    return res, score_results(res, metrics, gt)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=None, help="thư mục đích (mặc định history/<ngày>)")
    ap.add_argument("--force", action="store_true", help="cho phép ghi đè thư mục đã có")
    args = ap.parse_args()

    out = args.out or (GOC / "history" / dt.date.today().isoformat())
    if out.exists() and any(out.iterdir()) and not args.force:
        print(f"LỖI: {out} đã có dữ liệu. Dùng --force nếu thật sự muốn ghi đè.")
        return 1

    res, bang = _cham()
    # Một mốc thời gian cho cả lượt: hai file ghi hai mốc khác nhau thì không ai
    # biết chúng có thuộc cùng lượt chạy không.
    moc = dt.datetime.now().astimezone().isoformat(timespec="seconds")

    mani = report.dung_manifest(res, bang, generated_at=moc)
    cov = report.coverage(res)

    out.mkdir(parents=True, exist_ok=True)
    import json

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    def ghi(ten: str, noi_dung: str) -> None:
        (out / ten).write_bytes(noi_dung.encode("utf-8"))

    ghi("manifest.json", json.dumps(mani, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    ghi("overall.md", report.bao_cao_overall(bang, mani, sinh_boi="scripts/d1_report.py"))
    ghi("by_group.md", report.bao_cao_by_group(bang, sinh_boi="scripts/d1_report.py"))
    ghi("common_set.md", report.bao_cao_common_set(bang, cov, sinh_boi="scripts/d1_report.py"))
    ghi("raw.json", report.raw_json(bang, generated_at=moc) + "\n")

    print(f"ghi {out}")
    for c in mani["canh_bao"]:
        print("  ! " + c)
    if mani["git"]["dirty"]:
        print("  ! working tree BẨN — bản này không truy ngược được")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
