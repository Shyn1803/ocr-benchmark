"""Nắn `prediction/sovereign_*` về đúng quy ước `prediction/<engine>/<doc>.json`.

    py -3 scripts/fix_sovereign_layout.py --dry-run
    py -3 scripts/fix_sovereign_layout.py

Lượt chạy A7 truyền `root=prediction/sovereign_full`, nên `prediction_path()` ghép thêm
một cấp `sovereign/`. Hệ quả: `load_predictions(prediction/)` chỉ quét một cấp và bỏ im
lặng 206 file.

Script này làm đúng hai việc, một lần:

1. dời `prediction/<biến thể>/sovereign/*.json` lên `prediction/<biến thể>/*.json`
2. ghi lại trường `engine`: `"sovereign"` → `"sovereign_full"` / `"sovereign_light"`

Việc (2) không phải chuyện thẩm mỹ. `ScoreTable` gom theo chuỗi `engine`; để nguyên thì
2 tài liệu chạy chế độ `full` trộn với 204 tài liệu chế độ `light` thành một trung bình
không mô tả cấu hình nào có thật. Biến thể hiện chỉ ghi ở `config_fingerprint.mode` —
chỗ `ScoreTable` không nhìn tới.

KHÔNG đụng bất kỳ trường đo nào (`text_md`, `seconds`, `peak_rss_mb`,
`config_fingerprint`, …). Không chạy engine, không đọc PDF.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
DU_DOAN = GOC / "prediction"
TEN_LONG = "sovereign"
BIEN_THE = ("sovereign_full", "sovereign_light")


def _nan_mot(thu_muc: Path, *, that: bool) -> tuple[int, list[str]]:
    """Nắn một biến thể. Trả (số file, cảnh báo)."""
    canh_bao: list[str] = []
    long = thu_muc / TEN_LONG
    if not long.is_dir():
        return 0, [f"{thu_muc.name}: không có thư mục lồng `{TEN_LONG}/` — bỏ qua"]

    files = sorted(long.glob("*.json"))
    if not files:
        return 0, [f"{long}: rỗng"]

    for f in files:
        dich = thu_muc / f.name
        if dich.exists():
            canh_bao.append(f"{dich}: ĐÃ TỒN TẠI — không ghi đè")
            continue

        raw = json.loads(f.read_text(encoding="utf-8"))
        cu = raw.get("engine")
        if cu not in (TEN_LONG, thu_muc.name):
            canh_bao.append(f"{f}: engine={cu!r} lạ — không đụng")
            continue
        raw["engine"] = thu_muc.name

        if that:
            # Ghi đích TRƯỚC rồi mới xoá nguồn: đứt giữa chừng thì mất nhiều nhất là
            # một bản sao thừa, không mất dữ liệu.
            dich.write_text(
                json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            f.unlink()

    if that:
        con_lai = list(long.iterdir())
        if not con_lai:
            long.rmdir()
        else:
            canh_bao.append(f"{long}: còn {len(con_lai)} mục — không xoá thư mục")

    return len(files), canh_bao


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="chỉ in, không ghi")
    ns = ap.parse_args()
    that = not ns.dry_run

    truoc = len(list(DU_DOAN.rglob("*.json")))
    print(f"{'CHẠY THẬT' if that else 'THỬ (dry-run)'} · {truoc} file json dưới prediction/")

    tong = 0
    moi_canh_bao: list[str] = []
    for ten in BIEN_THE:
        n, cb = _nan_mot(DU_DOAN / ten, that=that)
        tong += n
        moi_canh_bao += cb
        print(f"  {ten:18s} {n:4d} file")

    sau = len(list(DU_DOAN.rglob("*.json")))
    print(f"tổng nắn {tong} file · trước {truoc} → sau {sau}")
    if truoc != sau:
        print("LỖI: số file thay đổi — phải bằng nhau, chỉ dời chỗ chứ không tạo/xoá")
        return 1

    for c in moi_canh_bao:
        print(f"  ⚠️  {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
