"""Nâng file prediction schema 1/2/3 lên 4 — tại chỗ, không chạy lại engine.

    py -3 scripts/migrate_predictions.py prediction
    py -3 scripts/migrate_predictions.py prediction --dry-run    # xem trước, không ghi

Schema 3 thêm identity `engine_family`/`profile`, raw artifact metadata và failure
taxonomy. Prediction v2 chưa có raw sidecar nên `raw_artifacts=[]`; identity legacy
được ghi rõ bằng `engine_family=engine`, `profile="legacy"`. Với ca lỗi cũ, message
không đủ tin cậy để suy timeout/OOM nên script gán bảo thủ `engine_error` và cảnh báo.

Schema 4 thêm `peak_vram_mb`. File cũ chạy trước khi bench biết đo VRAM nên giá trị
đúng của chúng là `null` — "không đo được", không phải "đo ra 0 MB". Điền 0 sẽ biến
những lần chạy đó thành bằng chứng rằng engine không đụng GPU, thứ mà không lần chạy
nào trong số đó nói.

## Vì sao là script chứ không phải "chạy lại cho sạch"

Repo đang giữ hơn một nghìn file prediction đã commit; riêng marker mất khoảng 3
tiếng CPU để dựng lại. `prediction.py` tồn tại chính là để khỏi trả cái giá đó mỗi
lần sửa metric — bắt chạy lại engine chỉ vì đổi hình dạng file là tự phá công dụng
của nó.

## Vì sao không nới lỏng `load_prediction()` thay vì migrate

Nới lỏng nghĩa là "thiếu trường thì coi như null". Nhưng cổng thiếu/thừa trường ở
`prediction.py` đang chặn một lỗi thật: file do bản mới ghi ra, có thêm một kênh dữ
liệu, bản cũ nạp trót lọt và lặng lẽ chấm thiếu. Mở cổng cho một trường hôm nay là
mở cho mọi trường về sau. Nâng file rẻ hơn nhiều so với mất cái cổng đó.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Trường thêm ở schema 2 → giá trị mặc định khi nâng từ v1.
THEM_V2 = {"model_load_seconds": None, "rss_scope": None}

DICH = 4

# Thứ tự khoá đúng như `save_prediction()` dựng payload. Chỉ `setdefault` rồi ghi thì
# hai khoá mới rơi xuống cuối file; lần chạy engine thật kế tiếp sẽ ghi lại theo thứ
# tự này và `git diff` đỏ nguyên file — che mất thay đổi thật của engine, đúng cái
# `prediction/` được commit để nhìn thấy.
THU_TU = (
    "schema_version",
    "engine",
    "engine_family",
    "profile",
    "engine_version",
    "doc_id",
    "capabilities",
    "text_md",
    "raw_artifacts",
    "blocks",
    "images",
    "tables",
    "scan_label",
    "page_sizes",
    "seconds",
    "model_load_seconds",
    "peak_rss_mb",
    "rss_scope",
    "peak_vram_mb",
    "failed",
    "error",
    "failure_kind",
    "config_fingerprint",
)
THEM_V4 = {"peak_vram_mb": None}
THEM_V3 = frozenset({"engine_family", "profile", "raw_artifacts", "failure_kind"})
KHOA_V3 = frozenset(THU_TU) - frozenset(THEM_V4)
KHOA_V2 = KHOA_V3 - THEM_V3
KHOA_V1 = KHOA_V2 - frozenset(THEM_V2)
KHOA_CU = {1: KHOA_V1, 2: KHOA_V2, 3: KHOA_V3}
"""Bộ khoá đầy đủ của từng schema nguồn. Kiểm **bằng nhau**, không phải "chứa":
file thiếu khoá thì nâng sẽ đẻ ra `KeyError` giữa chừng, file thừa khoá thì có kênh
dữ liệu mà bản này không biết và sắp lại theo `THU_TU` sẽ vứt nó đi lặng lẽ."""


def _ensure_utf8_console() -> None:
    """Windows có thể mở stdout/stderr bằng cp1252 và làm CLI nổ khi in tiếng Việt."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def nang_mot(path: Path, *, thu: bool) -> str:
    """Nâng một file. Trả về nhãn kết quả để đếm."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  LỖI  {path}: {exc}", file=sys.stderr)
        return "loi"
    if not isinstance(raw, dict):
        print(f"  LỖI  {path}: gốc file không phải object", file=sys.stderr)
        return "loi"

    ver = raw.get("schema_version")
    if ver == DICH:
        return "da_moi"
    if ver not in KHOA_CU:
        # Không đoán. Bản lạ có thể là bản mới hơn script này, và ghi đè nó là làm
        # mất dữ liệu mà không có đường phục hồi.
        print(
            f"  BỎ   {path}: schema_version={ver!r}, script chỉ nâng 1/2/3→{DICH}",
            file=sys.stderr,
        )
        return "bo"

    khoa_dung = KHOA_CU[ver]
    if set(raw) != khoa_dung:
        print(
            f"  BỎ   {path}: khoá lệch schema {ver} "
            f"({sorted(set(raw) ^ khoa_dung)})",
            file=sys.stderr,
        )
        return "bo"

    if ver < 2:
        for k, v in THEM_V2.items():
            raw.setdefault(k, v)
    if ver < 3:
        # Chỉ ca v1/v2 mới bịa identity legacy. File v3 đã mang identity thật của
        # lần chạy — ghi đè bằng `profile="legacy"` là xoá dữ liệu đúng bằng dữ liệu bịa.
        raw["engine_family"] = raw["engine"]
        raw["profile"] = "legacy"
        raw["raw_artifacts"] = []
        if raw.get("failed"):
            raw["failure_kind"] = "engine_error"
            print(
                f"  CẢNH BÁO  {path}: prediction lỗi v{ver} được gán "
                "failure_kind=engine_error vì schema cũ không lưu taxonomy",
                file=sys.stderr,
            )
        else:
            raw["failure_kind"] = None
    for k, v in THEM_V4.items():
        raw.setdefault(k, v)
    raw["schema_version"] = DICH
    if set(raw) != set(THU_TU):
        # Không tự ý sắp lại một file có khoá lạ: sắp theo THU_TU sẽ **vứt** khoá
        # không có trong danh sách, im lặng.
        print(
            f"  BỎ   {path}: khoá lệch schema {DICH} "
            f"({sorted(set(raw) ^ set(THU_TU))})",
            file=sys.stderr,
        )
        return "bo"
    raw = {k: raw[k] for k in THU_TU}

    if thu:
        return f"se_nang_v{ver}"
    # Giữ đúng khuôn `save_prediction()`: indent 2, không escape unicode, newline "\n",
    # có dòng trắng cuối. Lệch khuôn thì `git diff` lần chạy sau sẽ đỏ toàn bộ file.
    path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return f"da_nang_v{ver}"


def main(argv: list[str] | None = None) -> int:
    _ensure_utf8_console()
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("root", type=Path, help="thư mục prediction/")
    p.add_argument(
        "--dry-run",
        "--thu",
        dest="thu",
        action="store_true",
        help="chỉ báo sẽ nâng file nào, không ghi gì",
    )
    a = p.parse_args(argv)

    if not a.root.is_dir():
        print(f"{a.root}: không phải thư mục", file=sys.stderr)
        return 2

    dem: dict[str, int] = {}
    for f in sorted(a.root.rglob("*.json")):
        nhan = nang_mot(f, thu=a.thu)
        dem[nhan] = dem.get(nhan, 0) + 1

    if not dem:
        print(f"{a.root}: không tìm thấy file .json nào")
        return 0

    ten = {
        **{f"da_nang_v{v}": f"đã nâng v{v} → v{DICH}" for v in sorted(KHOA_CU)},
        **{
            f"se_nang_v{v}": f"sẽ nâng v{v} → v{DICH} (bỏ --dry-run để ghi)"
            for v in sorted(KHOA_CU)
        },
        "da_moi": f"đã ở schema {DICH}, không đụng",
        "bo": "bỏ qua (schema lạ)",
        "loi": "lỗi đọc",
    }
    for k, v in dem.items():
        print(f"{v:5d}  {ten.get(k, k)}")
    return 1 if dem.get("loi") else 0


if __name__ == "__main__":
    raise SystemExit(main())
