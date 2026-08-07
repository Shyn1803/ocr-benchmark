"""Chấm bộ khẳng định olmOCR, tách theo **loại** và theo **tầng** — B5 (TASK-083).

    py -3 scripts/score_assertions.py --pred prediction-local --engines opendataloader

Hai chiều tách, không một con số:

- **Theo loại** là yêu cầu của AC-02. Gộp sáu loại vào một điểm là vứt đi thông tin
  duy nhất mà bộ khẳng định có mà thước đo liên tục không có.
- **Theo tầng** thì AC không đòi, nhưng thiếu nó thì bảng theo loại *không đọc được*:
  olmOCR-bench trộn PDF số với ảnh quét, và một engine chỉ đọc lớp text sẵn có sẽ
  trượt sạch tầng quét vì lý do chẳng liên quan gì tới loại khẳng định. Một cột
  `text_presence = 0.27` gộp cả hai tầng trông y hệt một bộ so khớp hỏng.
"""

from __future__ import annotations

import argparse
import collections
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import ocr_bench  # noqa: F401  — import để metric tự đăng ký
from ocr_bench import registry
from ocr_bench.corpus import load_olmocr
from ocr_bench.prediction import load_prediction

ROOT = Path(__file__).resolve().parent.parent

LOAI = [
    "assert_text_presence",
    "assert_text_absence",
    "assert_reading_order",
    "assert_math_presence",
    "assert_table_relation",
    "assert_baseline",
]


def tang_theo_tai_lieu() -> dict[str, str]:
    """`{stem: tên thư mục tầng}` từ `pdfs/olmocr/<tầng>/<stem>.pdf`."""
    return {
        p.stem: p.parent.name
        for p in (ROOT / "pdfs" / "olmocr").glob("*/*.pdf")
    }


def _o(diem: list[float]) -> str:
    return f"{statistics.mean(diem):.3f}" if diem else "—"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pred", default="prediction-local", help="thư mục prediction")
    ap.add_argument("--engines", default=None, help="lọc engine, phân tách bằng dấu phẩy")
    a = ap.parse_args()

    goc = Path(a.pred)
    if not goc.is_absolute():
        goc = ROOT / goc
    if not goc.is_dir():
        raise SystemExit(f"không thấy {goc}")

    docs = load_olmocr()
    tang = tang_theo_tai_lieu()
    engines = (
        a.engines.split(",") if a.engines else sorted(p.name for p in goc.iterdir() if p.is_dir())
    )

    for eng in engines:
        preds = sorted((goc / eng).glob("*.json"))
        # (loại, tầng) → điểm;  (loại, tầng) → đếm N/A theo lý do
        diem: dict[tuple[str, str], list[float]] = collections.defaultdict(list)
        na: dict[tuple[str, str], collections.Counter] = collections.defaultdict(
            collections.Counter
        )
        n_kd: dict[tuple[str, str], int] = collections.Counter()
        cac_tang: set[str] = set()
        n_khop = 0

        for p in preds:
            gt = docs.get(p.stem)
            if gt is None:
                continue
            n_khop += 1
            t = tang.get(p.stem, "?")
            cac_tang.add(t)
            res = load_prediction(p)
            for l in LOAI:
                r = registry.get_metric(l)().score(gt, res)
                if r.na_reason is not None:
                    na[(l, t)][r.na_reason.name] += 1
                else:
                    diem[(l, t)].append(r.value)
                    n_kd[(l, t)] += r.detail.get("n_khang_dinh", 0)

        print(f"\n=== {eng} — {n_khop}/{len(docs)} tài liệu có nhãn olmOCR")
        if not n_khop:
            print("  (không tài liệu nào khớp bộ nhãn)")
            continue

        cot = sorted(cac_tang)
        print(f"\n{'loại':<24}" + "".join(f"{c[:13]:>15}" for c in cot) + f"{'gộp':>9}")
        for l in LOAI:
            hang = f"{l:<24}"
            for c in cot:
                d = diem[(l, c)]
                if d:
                    hang += f"{_o(d) + f' ({len(d)})':>15}"
                else:
                    # KHÔNG in cùng một ký hiệu cho mọi N/A. "engine hỏng" và "bộ nhãn
                    # không hỏi loại này" là hai chuyện ngược nhau: cái đầu là một lượt
                    # chạy phải vứt đi, cái sau là câu trả lời đúng. Gộp chúng vào `·`
                    # thì một lượt chạy hỏng sạch trông y hệt một bảng lành lặn.
                    hong = na[(l, c)].get("ENGINE_FAILED", 0)
                    hang += f"{f'HỎNG({hong})':>15}" if hong else f"{'·':>15}"
            tat_ca = [v for c in cot for v in diem[(l, c)]]
            hang += f"{_o(tat_ca):>9}"
            print(hang)

        gop_na = collections.Counter()
        for c in na.values():
            gop_na.update(c)
        print("\n  `·` = tầng đó không có khẳng định loại này (NO_GROUND_TRUTH)")
        print("  `HỎNG(n)` = engine chạy hỏng trên n tài liệu — lượt chạy phải làm lại")
        print(f"  (n) = số tài liệu · tổng khẳng định đã chấm: {sum(n_kd.values())}")
        print(f"  N/A theo lý do: {dict(gop_na)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
