"""Chọn 20 ca hỏng để đọc tay — TASK-088 (D2).

    py -3 scripts/d2_cases.py [--json FILE]

Vì sao cần một script thay vì `sort()[:20]`: trong 261 ô có điểm thật của bản công bố,
**164 ô bằng đúng 0.0**. Sắp xếp rồi cắt 20 là chọn theo thứ tự `doc_id` — ngẫu nhiên
mà trông có phương pháp. Script này chọn theo **tầng**, mỗi tầng trả lời một câu hỏi
chẩn đoán khác nhau; quy tắc đầy đủ ở `.claude/tasks/TASK-088/plan.md` §2.

Mẫu này **cố ý lệch**. Tỉ lệ nguyên nhân tìm được trên 20 ca KHÔNG ngoại suy ra toàn bộ.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "src"))

from ocr_bench import registry  # noqa: E402
from ocr_bench.corpus import load_doclaynet, load_olmocr  # noqa: E402
from ocr_bench.prediction import load_predictions  # noqa: E402
from ocr_bench.scorer import score_results  # noqa: E402

# (tên tầng, số ca lấy) — tổng đúng 20. Xem plan.md §2 để biết vì sao là con số này.
TANG: list[tuple[str, int]] = [
    ("crash", 5),
    ("img_lech_khung", 5),
    ("img_duong_tinh_gia", 5),
    ("img_bo_sot", 3),
    ("heading_zero", 2),
]
TONG = 20


def _phan_tang(rows) -> dict[str, list[dict]]:
    """Chia mọi ca đáng ngờ vào tầng. Một ca thuộc đúng một tầng."""
    ra: dict[str, list[dict]] = {ten: [] for ten, _ in TANG}
    for r in rows:
        d = r.detail or {}
        if r.na_reason is not None and r.na_reason.value == "engine_failed":
            # Crash làm hỏng cả 14 metric của cùng tài liệu; đếm theo tài liệu.
            if r.metric == "img_f1":
                ra["crash"].append({"engine": r.engine, "doc_id": r.doc_id, "metric": "*"})
            continue
        if r.value != 0.0:
            continue
        if r.metric == "heading":
            ra["heading_zero"].append({"engine": r.engine, "doc_id": r.doc_id, "metric": "heading"})
        elif r.metric == "img_f1":
            nn, nd = d.get("n_nhan"), d.get("n_doan")
            ten = (
                "img_bo_sot"
                if nn and not nd
                else "img_duong_tinh_gia"
                if nd and not nn
                else "img_lech_khung"
            )
            ra[ten].append(
                {
                    "engine": r.engine,
                    "doc_id": r.doc_id,
                    "metric": "img_f1",
                    "n_nhan": nn,
                    "n_doan": nd,
                }
            )
    # `assert_math_presence` (40 ca zero của noop + sabotage) không có tầng nào: cả hai
    # là engine giả, zero là hành vi đúng thiết kế. Loại có khai báo, không im lặng bỏ.
    for v in ra.values():
        v.sort(key=lambda c: (c["engine"], c["doc_id"]))
    return ra


def _duong_dan(c: dict) -> dict[str, str]:
    """Đường dẫn để người đọc mở tay. Ghi cả khi file không tồn tại — thiếu file cũng
    là một phát hiện, giấu đi thì ca đó trông như đã kiểm."""
    d = c["doc_id"]
    for bo in ("doclaynet", "olmocr"):
        p = GOC / "pdfs" / bo / f"{d}.pdf"
        if p.exists():
            pdf = p
            break
    else:
        pdf = GOC / "pdfs" / f"{d}.pdf"
    return {
        "pdf": str(pdf.relative_to(GOC)).replace("\\", "/"),
        "du_doan": f"prediction/{c['engine']}/{d}.json",
        "nhan": f"ground-truth/doclaynet/JSON/{d}.json",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", type=Path, default=None, help="ghi danh sách ra file JSON")
    args = ap.parse_args()

    gt: dict = {}
    gt.update(load_doclaynet())
    gt.update(load_olmocr())
    res = load_predictions(GOC / "prediction")
    metrics = [registry.get_metric(t)() for t in ("img_f1", "heading")]
    bang = score_results(res, metrics, gt)

    ho = _phan_tang(bang.rows)
    chon: list[dict] = []
    for ten, n in TANG:
        co = ho[ten]
        if len(co) < n:
            print(f"LỖI: tầng `{ten}` chỉ có {len(co)} ca, kế hoạch đòi {n}.")
            return 1
        for c in co[:n]:
            chon.append({"tang": ten, **c, **_duong_dan(c)})

    if len(chon) != TONG:
        print(f"LỖI: chọn ra {len(chon)} ca, phải đúng {TONG}.")
        return 1

    print(f"{'#':>2}  {'tầng':<20} {'engine':<16} {'doc_id':<16} nhãn/đoán")
    for i, c in enumerate(chon, 1):
        nd = (
            f"{c.get('n_nhan')}/{c.get('n_doan')}"
            if c.get("n_nhan") is not None
            else ""
        )
        print(f"{i:>2}  {c['tang']:<20} {c['engine']:<16} {c['doc_id'][:16]:<16} {nd}")
    print()
    for ten, n in TANG:
        print(f"  tầng {ten:<20} lấy {n}/{len(ho[ten])}")

    if args.json:
        args.json.write_text(
            json.dumps(chon, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="",  # xem TASK-087 04-lf-va-cay-sach.md §4.2
        )
        print(f"\nđã ghi {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
