"""Sinh `manifest.yaml` + `checksums.sha256` cho bộ mẫu — AC-03 của A3 (TASK-074).

    py -3 scripts/make_manifest.py            # ghi manifest.yaml + checksums.sha256
    py -3 scripts/make_manifest.py --verify   # đối chiếu, không ghi; exit≠0 nếu lệch

Manifest ghi **nguồn + giấy phép + số trang từng tầng**, checksum ghi từng file. Hai thứ
này trả lời hai câu hỏi khác nhau: manifest trả lời "bộ mẫu này gồm gì và có được dùng
không", checksum trả lời "file trên đĩa có còn đúng file đã đo hay không". Thiếu cái sau
thì một con số trong `results/` không truy ngược được về dữ liệu sinh ra nó.

`--verify` là thứ đáng chạy trước mỗi lần công bố bảng xếp hạng.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "manifest.yaml"
CHECKSUMS = ROOT / "checksums.sha256"

# Chỉ những thư mục thuộc bộ mẫu. `pdfs/sample_minimal.pdf` (A1b) cố tình không nằm đây:
# nó là file dựng tay để chạy thử đường ống, không phải dữ liệu đo.
VUNG = ["pdfs/doclaynet", "pdfs/olmocr", "ground-truth/doclaynet", "ground-truth/olmocr"]


def bam(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


def liet_ke() -> list[Path]:
    ra: list[Path] = []
    for v in VUNG:
        d = ROOT / v
        if d.is_dir():
            ra += [p for p in sorted(d.rglob("*")) if p.is_file()]
    return ra


def tang_doclaynet() -> dict[str, int]:
    p = ROOT / "ground-truth" / "doclaynet" / "layout_coco.json"
    if not p.exists():
        return {}
    coco = json.loads(p.read_text(encoding="utf-8"))
    return dict(sorted(Counter(i["doc_category"] for i in coco["images"]).items()))


def tang_olmocr() -> dict[str, int]:
    d = ROOT / "pdfs" / "olmocr"
    if not d.is_dir():
        return {}
    return {s.name: len(list(s.glob("*.pdf"))) for s in sorted(d.iterdir()) if s.is_dir()}


def dem_assertion() -> dict[str, int]:
    d = ROOT / "ground-truth" / "olmocr"
    if not d.is_dir():
        return {}
    return {
        p.stem: sum(1 for line in p.read_text(encoding="utf-8").splitlines() if line.strip())
        for p in sorted(d.glob("*.jsonl"))
    }


def viet_manifest(files: list[Path]) -> str:
    dl, olm, asr = tang_doclaynet(), tang_olmocr(), dem_assertion()
    tong_byte = sum(p.stat().st_size for p in files)

    def khoi(d: dict[str, int], thut: str = "    ") -> str:
        return "\n".join(f"{thut}{k}: {v}" for k, v in d.items()) or f"{thut}{{}}"

    return f"""# Bộ tài liệu mẫu của ocr-bench — sinh bởi scripts/make_manifest.py
# Đừng sửa tay: chạy lại script sau khi thêm/bớt file, rồi commit cả manifest.yaml
# lẫn checksums.sha256 trong cùng một commit với dữ liệu.
#
# Kiểm lại:  py -3 scripts/make_manifest.py --verify

tong_ket:
  so_file: {len(files)}
  dung_luong_mb: {tong_byte / 1e6:.1f}
  trang_doclaynet: {sum(dl.values())}
  pdf_olmocr: {sum(olm.values())}
  assertion_olmocr: {sum(asr.values())}

nguon:
  - ten: DocLayNet
    chu_so_huu: IBM Deep Search
    giay_phep: CDLA-Permissive-1.0
    thuong_mai: cho phep
    trang_chu: https://developer.ibm.com/exchanges/data/all/doclaynet/
    lay_tu: DocLayNet_extra.zip (PDF mot trang) + DocLayNet_core.zip (COCO/test.json)
    cach_lay: scripts/fetch_doclaynet.py — HTTP range doc rieng tung member trong ZIP
    ghi_chu: >-
      Toan bo DocLayNet la 38 GB. Chi lay mau phan tang, khong tai het.
      Toa do COCO o he 1025x1025 — xem ground-truth/doclaynet/README.md.
    phan_tang_theo_doc_category:
{khoi(dl, "      ")}

  - ten: olmOCR-bench
    chu_so_huu: Allen Institute for AI (AI2)
    giay_phep: ODC-BY-1.0
    thuong_mai: cho phep, kem dieu kien ghi cong
    trang_chu: https://huggingface.co/datasets/allenai/olmOCR-bench
    cach_lay: scripts/fetch_olmocr.py
    ghi_chu: >-
      Nhan la assertion dang jsonl (unit test tren van ban trich xuat), khong phai
      van ban tham chieu day du. La nguon chinh cho B5.
    phan_tang_theo_split:
{khoi(olm, "      ")}
    assertion_moi_file:
{khoi(asr, "      ")}

khong_dua_vao_repo:
  - ten: OmniDocBench
    ly_do: >-
      Research-only / phi thuong mai. Plan §11 da chot loai. Khong tai file ve repo,
      khong trich so lieu vao tai lieu noi bo co gia tri thuong mai khi chua co ra soat
      phap ly. Day la quyet dinh cua chu du an, khong phai cua agent.
  - ten: Tai lieu that cua khach hang
    ly_do: >-
      Neu ve sau dua vao, phan do PHAI gitignore, chi commit manifest + checksum.
      Dua file khach vao repo la rui ro ro ri.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    files = liet_ke()
    if not files:
        print("Chưa có file nào trong bộ mẫu. Chạy scripts/fetch_*.py trước.")
        return 1

    dong = {str(p.relative_to(ROOT)).replace("\\", "/"): bam(p) for p in files}

    if args.verify:
        if not CHECKSUMS.exists():
            print("Chưa có checksums.sha256")
            return 1
        cu = {}
        for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                h, _, n = line.partition("  ")
                cu[n] = h
        thieu = sorted(set(cu) - set(dong))
        thua = sorted(set(dong) - set(cu))
        lech = sorted(n for n in set(cu) & set(dong) if cu[n] != dong[n])
        for nhan, ds in (("thiếu", thieu), ("thừa", thua), ("sai checksum", lech)):
            if ds:
                print(f"{nhan}: {len(ds)}")
                for n in ds[:10]:
                    print(f"  {n}")
        if thieu or thua or lech:
            return 1
        print(f"Khớp toàn bộ {len(dong)} file.")
        return 0

    CHECKSUMS.write_text(
        "# sha256  đường-dẫn (tương đối tới gốc ocr-bench)\n"
        + "".join(f"{h}  {n}\n" for n, h in sorted(dong.items())),
        encoding="utf-8",
    )
    MANIFEST.write_text(viet_manifest(files), encoding="utf-8")
    print(f"{len(dong)} file → {MANIFEST.name} + {CHECKSUMS.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
