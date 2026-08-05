"""Tải olmOCR-bench (allenai/olmOCR-bench) về `pdfs/olmocr/` + `ground-truth/olmocr/`.

    py -3 scripts/fetch_olmocr.py            # tải phần còn thiếu
    py -3 scripts/fetch_olmocr.py --check    # chỉ kiểm, không tải

Giấy phép **ODC-BY-1.0** — cho phép dùng thương mại, kèm điều kiện ghi công. Khác hẳn
OmniDocBench (research-only) mà plan §11 đã loại. Ghi công đặt ở `pdfs/olmocr/LICENSE.md`.

Vì sao tải trực tiếp qua HTTP chứ không `datasets.load_dataset`: mỗi mục ở đây là một
**file PDF thật**, không phải hàng trong bảng. Adapter nhận `Path`, nên tải thẳng ra đĩa
là đúng hình dạng dữ liệu; kéo `datasets` + `pyarrow` vào venv chỉ để rồi ghi file ra là
thêm phụ thuộc mà không thêm gì.

Tải lại được: bỏ qua file đã có đúng kích thước, nên chạy lại sau khi đứt mạng là an toàn.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = "allenai/olmOCR-bench"
API = f"https://huggingface.co/api/datasets/{REPO}"
RAW = f"https://huggingface.co/datasets/{REPO}/resolve/main/"

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "pdfs" / "olmocr"
GT_DIR = ROOT / "ground-truth" / "olmocr"


def liet_ke() -> list[str]:
    with urllib.request.urlopen(API, timeout=60) as r:
        meta = json.load(r)
    return [s["rfilename"] for s in meta["siblings"]]


def dich(remote: str) -> Path | None:
    """`bench_data/pdfs/<split>/x.pdf` → `pdfs/olmocr/<split>/x.pdf`; `.jsonl` → ground-truth."""
    if remote.startswith("bench_data/pdfs/") and remote.endswith(".pdf"):
        return PDF_DIR / Path(remote).relative_to("bench_data/pdfs")
    if remote.startswith("bench_data/") and remote.endswith(".jsonl"):
        return GT_DIR / Path(remote).name
    return None


def tai(remote: str, dest: Path) -> tuple[str, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(RAW + remote, timeout=180) as r:
        data = r.read()
    tmp.write_bytes(data)
    tmp.replace(dest)
    return remote, len(data)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="chỉ báo thiếu bao nhiêu file")
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()

    cap = [(r, d) for r in liet_ke() if (d := dich(r)) is not None]
    thieu = [(r, d) for r, d in cap if not d.exists()]
    print(f"{REPO}: {len(cap)} file cần có, {len(thieu)} còn thiếu")
    if args.check or not thieu:
        return 0 if not thieu else 1

    tong = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for i, (remote, n) in enumerate(ex.map(lambda a: tai(*a), thieu), start=1):
            tong += n
            if i % 100 == 0 or i == len(thieu):
                print(f"  {i}/{len(thieu)}  {tong / 1e6:.1f} MB")

    print(f"Xong: {tong / 1e6:.1f} MB → {PDF_DIR} + {GT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
