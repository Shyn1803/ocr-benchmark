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

_GHI_DE: list[str] = []
"""Tên file bị **cố ý** ghi đè ở `_tach_theo_che_do`.

Cần đếm riêng vì bất biến "chỉ dời chỗ, không tạo/xoá" ở `main` sẽ báo đỏ oan: chạy
lại một engine để nắn version lệch thì file mới thay chỗ file cũ, tổng **phải** giảm
đúng bằng số bị thay. Bỏ qua mã thoát cho xong là cách để lần sau mất file thật mà
không ai biết; nên trừ đúng con số, và in nó ra.
"""


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


def _tach_theo_che_do(that: bool) -> tuple[int, list[str]]:
    """`prediction/sovereign/` → `prediction/sovereign_{light,full}/`, chia theo
    `config_fingerprint.mode` của **chính từng file**.

    `make_predictions.py --engines sovereign` ghi thẳng vào `prediction/sovereign/`
    vì adapter tên là `sovereign`; chế độ chỉ lộ ra ở `config_fingerprint.mode`, chỗ
    `ScoreTable` không nhìn tới. Để nguyên thì tài liệu chạy `full` (có Marker/Surya)
    trộn chung trung bình với tài liệu chạy `light` — một con số không mô tả cấu hình
    nào có thật, và đó đúng là loại sai lệch bảng điểm không tự tố cáo.

    Chia theo từng file chứ không theo cả lượt chạy: một lượt có thể đổi chế độ giữa
    chừng nếu cache model xuất hiện, và khi đó gán cả lượt về một chế độ là nói dối.
    """
    canh_bao: list[str] = []
    thu_muc = DU_DOAN / TEN_LONG
    if not thu_muc.is_dir():
        return 0, []
    files = sorted(thu_muc.glob("*.json"))
    if not files:
        return 0, [f"{thu_muc}: rỗng"]

    n = 0
    for f in files:
        raw = json.loads(f.read_text(encoding="utf-8"))
        mode = (raw.get("config_fingerprint") or {}).get("mode")
        if mode not in ("light", "full"):
            canh_bao.append(f"{f}: config_fingerprint.mode={mode!r} lạ — không đụng")
            continue
        ten_moi = f"{TEN_LONG}_{mode}"
        dich = DU_DOAN / ten_moi / f.name
        if dich.exists():
            canh_bao.append(f"{dich}: ĐÃ TỒN TẠI — ghi đè bằng bản mới")
            _GHI_DE.append(dich.name)
        raw["engine"] = ten_moi
        if that:
            dich.parent.mkdir(parents=True, exist_ok=True)
            dich.write_text(
                json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            f.unlink()
        n += 1

    if that and not list(thu_muc.iterdir()):
        thu_muc.rmdir()
    return n, canh_bao


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="chỉ in, không ghi")
    ns = ap.parse_args()
    that = not ns.dry_run

    # Đếm **chỉ** các thư mục script này đụng tới, không phải cả `prediction/`.
    # Đếm cả cây thì một lượt chạy engine khác đang ghi song song sẽ làm bất biến
    # "chỉ dời chỗ" báo đỏ dù script không tạo/xoá gì — cổng kêu oan thì người ta tắt
    # cổng. Phạm vi hẹp lại cũng chính xác hơn: đây đúng là tập file bị ảnh hưởng.
    lien_quan = [DU_DOAN / TEN_LONG, *(DU_DOAN / t for t in BIEN_THE)]

    def _dem() -> int:
        return sum(len(list(d.rglob("*.json"))) for d in lien_quan if d.is_dir())

    truoc = _dem()
    pham_vi = ", ".join(d.name for d in lien_quan)
    print(f"{'CHẠY THẬT' if that else 'THỬ (dry-run)'} · {truoc} file json trong {pham_vi}")

    tong = 0
    moi_canh_bao: list[str] = []
    for ten in BIEN_THE:
        n, cb = _nan_mot(DU_DOAN / ten, that=that)
        tong += n
        moi_canh_bao += cb
        print(f"  {ten:18s} {n:4d} file")

    n, cb = _tach_theo_che_do(that=that)
    tong += n
    moi_canh_bao += cb
    print(f"  {TEN_LONG + '/ (tách)':18s} {n:4d} file")

    sau = _dem()
    ghi_de = len(_GHI_DE)
    mong = truoc - (ghi_de if that else 0)
    print(f"tổng nắn {tong} file · trước {truoc} → sau {sau} (ghi đè {ghi_de})")
    if sau != mong:
        print(
            f"LỖI: chờ {mong} file sau khi nắn, thấy {sau} — chỉ được dời chỗ, "
            f"và chỉ được mất đúng {ghi_de} file bị ghi đè."
        )
        return 1

    for c in moi_canh_bao:
        print(f"  ⚠️  {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
