"""Rút một mẫu phân tầng của DocLayNet về `pdfs/doclaynet/` + `ground-truth/doclaynet/`.

    py -3 scripts/fetch_doclaynet.py --per-category 34      # ~204 trang, 6 loại
    py -3 scripts/fetch_doclaynet.py --check

Giấy phép **CDLA-Permissive-1.0** (cho phép dùng thương mại). Nguồn:
IBM Deep Search, https://developer.ibm.com/exchanges/data/all/doclaynet/

## Vì sao không `git clone` / `load_dataset`

Bộ đầy đủ là hai file ZIP: `DocLayNet_core.zip` **30 GB** (PNG + COCO) và
`DocLayNet_extra.zip` **8 GB** (PDF một trang + JSON text cell). Đĩa D: còn 31 GB —
kéo về rồi giải nén là không đủ chỗ, mà ta cũng chỉ cần ~200 trang trong 81.472 trang.

Bản parquet trên HuggingFace (`docling-project/DocLayNet-v1.1`) **chỉ có PNG**, trong khi
mọi adapter của bench nhận PDF. Nên phải lấy từ `DocLayNet_extra.zip`.

Cách làm: cả hai ZIP đều trả `Accept-Ranges: bytes`, và ZIP lưu **central directory ở
cuối file**. Đọc 25 MB central directory là biết offset từng member, rồi tải riêng
member cần bằng một range request và tự `zlib.decompress(..., -15)`. Tổng lưu lượng
cho 200 trang: vài chục MB thay vì 38 GB.

## Ba mảnh ghép cho mỗi trang

| Mảnh | Lấy từ | Dùng cho |
|---|---|---|
| `PDF/<hash>.pdf` | extra.zip | đầu vào cho adapter |
| `JSON/<hash>.json` | extra.zip | text cell + `metadata` (`doc_category`, kích thước trang) |
| mục trong `COCO/test.json` | core.zip | hộp bố cục có nhãn — ground truth của B3 |

`<hash>` là cùng một chuỗi ở cả ba nơi (`file_name` trong COCO bỏ đuôi `.png`).

⚠️ Toạ độ COCO ở hệ **1025×1025**, không phải kích thước trang thật (`original_width/height`
trong JSON metadata), và là **kéo giãn riêng từng trục** chứ không phải aspect-fit.
Quy đổi về `Box` chuẩn hoá nằm ở `src/ocr_bench/corpus.py::load_doclaynet`; bằng chứng
và cách kiểm lại ở `ground-truth/doclaynet/README.md` (`scripts/check_doclaynet_coords.py`).
"""

from __future__ import annotations

import argparse
import json
import pickle
import random
import struct
import sys
import urllib.request
import zlib
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
PDF_DIR = ROOT / "pdfs" / "doclaynet"
GT_DIR = ROOT / "ground-truth" / "doclaynet"

BASE = "https://codait-cos-dax.s3.us.cloud-object-storage.appdomain.cloud/dax-doclaynet/1.0.0/"
CORE = BASE + "DocLayNet_core.zip"
EXTRA = BASE + "DocLayNet_extra.zip"


# ---------------------------------------------------------------- ZIP qua HTTP range

def _rng(url: str, a: int, b: int) -> bytes:
    req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read()


def _size(url: str) -> int:
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers["Content-Length"])


def _parse_cd(d: bytes) -> dict[str, tuple[int, int, int]]:
    """central directory → {tên: (method, compressed_size, local_header_offset)}."""
    out: dict[str, tuple[int, int, int]] = {}
    i = 0
    while i < len(d) - 4 and d[i : i + 4] == b"PK\x01\x02":
        f = struct.unpack("<IHHHHHHIIIHHHHHII", d[i : i + 46])
        meth, csz, usz, nl, el, cl, lho = f[4], f[8], f[9], f[10], f[11], f[12], f[16]
        name = d[i + 46 : i + 46 + nl].decode("utf-8", "replace")
        extra = d[i + 46 + nl : i + 46 + nl + el]
        if 0xFFFFFFFF in (csz, usz, lho):
            # ZIP64: các trường tràn 32 bit nằm trong extra field 0x0001, theo thứ tự
            # usz → csz → lho, và **chỉ** trường nào thật sự tràn mới có mặt.
            k = 0
            while k < len(extra) - 4:
                hid, hsz = struct.unpack("<HH", extra[k : k + 4])
                body, q = extra[k + 4 : k + 4 + hsz], 0
                if hid == 1:
                    if usz == 0xFFFFFFFF:
                        usz = struct.unpack("<Q", body[q : q + 8])[0]; q += 8
                    if csz == 0xFFFFFFFF:
                        csz = struct.unpack("<Q", body[q : q + 8])[0]; q += 8
                    if lho == 0xFFFFFFFF:
                        lho = struct.unpack("<Q", body[q : q + 8])[0]; q += 8
                k += 4 + hsz
        out[name] = (meth, csz, lho)
        i += 46 + nl + el + cl
    return out


def central_directory(url: str, ten_cache: str) -> dict[str, tuple[int, int, int]]:
    p = CACHE / f"{ten_cache}.pkl"
    if p.exists():
        cu = pickle.loads(p.read_bytes())
        # Kiểm kiểu chứ không tin tên file: `.cache/` không được version, nên có thể còn
        # sót cache do bản script cũ ghi ra với cấu trúc khác. Tin nhầm thì lỗi nổ mãi
        # tận trong `member()` với thông báo chẳng liên quan gì tới cache.
        if isinstance(cu, dict):
            return cu
        print(f"  bỏ cache {p.name} (cấu trúc cũ: {type(cu).__name__}), dựng lại")
    size = _size(url)
    tail = _rng(url, size - 70000, size - 1)
    j = tail.rfind(b"PK\x06\x07")
    if j < 0:
        raise RuntimeError(f"{url}: không thấy ZIP64 locator — file đổi định dạng?")
    off = struct.unpack("<IIQI", tail[j : j + 20])[2]
    z = struct.unpack("<IQHHIIQQQQ", _rng(url, off, off + 55))
    cd = _parse_cd(_rng(url, z[9], z[9] + z[8] - 1))
    CACHE.mkdir(exist_ok=True)
    p.write_bytes(pickle.dumps(cd))
    return cd


def member(url: str, cd: dict[str, tuple[int, int, int]], name: str) -> bytes:
    meth, csz, lho = cd[name]
    # Local header có độ dài tên/extra **riêng**, khác central directory — phải đọc
    # 30 byte header trước mới biết dữ liệu nén bắt đầu ở đâu.
    h = _rng(url, lho, lho + 29)
    nl, el = struct.unpack("<HH", h[26:30])
    start = lho + 30 + nl + el
    raw = _rng(url, start, start + csz - 1)
    return zlib.decompress(raw, -15) if meth == 8 else raw


def _cached(url: str, cd, name: str, dest: Path) -> Path:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".part")
        tmp.write_bytes(member(url, cd, name))
        tmp.replace(dest)
    return dest


# ---------------------------------------------------------------- chọn mẫu

def coco_test() -> dict:
    p = CACHE / "coco_test.json"
    if not p.exists():
        CACHE.mkdir(exist_ok=True)
        cd = central_directory(CORE, "core_cd")
        p.write_bytes(member(CORE, cd, "COCO/test.json"))
    return json.loads(p.read_text(encoding="utf-8"))


def chon(coco: dict, moi_loai: int, seed: int) -> list[dict]:
    """Chọn `moi_loai` trang mỗi `doc_category`, ưu tiên trải đều **collection**.

    Chọn ngẫu nhiên thuần trong một loại sẽ dồn vào collection đông nhất — ví dụ
    `financial_reports` có nhiều `ann_reports_*` khác nhau, mà báo cáo "fancy" trình bày
    khác hẳn báo cáo thường. Xếp vòng theo collection để 34 trang không rơi hết vào một kiểu.
    """
    rng = random.Random(seed)
    theo_loai: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for im in coco["images"]:
        theo_loai[im["doc_category"]][im["collection"]].append(im)

    ra: list[dict] = []
    for loai in sorted(theo_loai):
        nhom = [sorted(v, key=lambda i: i["file_name"]) for _, v in sorted(theo_loai[loai].items())]
        for g in nhom:
            rng.shuffle(g)
        lay, i = [], 0
        while len(lay) < moi_loai and any(nhom):
            g = nhom[i % len(nhom)]
            if g:
                lay.append(g.pop())
            i += 1
            nhom = [g for g in nhom if g]
        ra.extend(lay)
    return ra


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-category", type=int, default=34)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    coco = coco_test()
    mau = chon(coco, args.per_category, args.seed)
    print(f"Chọn {len(mau)} trang: {dict(Counter(i['doc_category'] for i in mau))}")

    hashes = [Path(i["file_name"]).stem for i in mau]
    thieu = [h for h in hashes if not (PDF_DIR / f"{h}.pdf").exists()]
    print(f"{len(thieu)}/{len(hashes)} PDF còn thiếu")
    if args.check:
        return 0 if not thieu else 1

    cd = central_directory(EXTRA, "extra_cd")
    viec = [(f"PDF/{h}.pdf", PDF_DIR / f"{h}.pdf") for h in hashes]
    viec += [(f"JSON/{h}.json", GT_DIR / "cells" / f"{h}.json") for h in hashes]
    viec = [(n, d) for n, d in viec if not d.exists()]

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for i, _ in enumerate(ex.map(lambda a: _cached(EXTRA, cd, *a), viec), start=1):
            if i % 50 == 0 or i == len(viec):
                print(f"  {i}/{len(viec)}")

    # Cắt COCO xuống đúng các trang đã chọn — giữ nguyên cấu trúc để đọc bằng công cụ COCO chuẩn.
    giu = {i["id"] for i in mau}
    con = {
        "categories": coco["categories"],
        "images": mau,
        "annotations": [a for a in coco["annotations"] if a["image_id"] in giu],
        "_note": "Tập con của DocLayNet COCO/test.json. Toạ độ ở hệ 1025x1025, gốc trên-trái.",
    }
    GT_DIR.mkdir(parents=True, exist_ok=True)
    (GT_DIR / "layout_coco.json").write_text(
        json.dumps(con, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"{len(con['annotations'])} hộp bố cục → {GT_DIR / 'layout_coco.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
