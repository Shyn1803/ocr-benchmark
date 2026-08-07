"""Nâng file prediction từ schema 1 lên 2 — tại chỗ, không chạy lại engine.

    py -3 scripts/migrate_predictions.py prediction
    py -3 scripts/migrate_predictions.py prediction --thu        # xem trước, không ghi

Schema 2 (B6/TASK-084) thêm hai trường: `model_load_seconds` và `rss_scope`. Cả hai
đều là **số đo mới**, không suy được từ file cũ — và cũng không nên suy: file bản 1
được ghi ra bởi một `execute()` chưa hề đo bộ nhớ, nên giá trị đúng của chúng là
"không đo", tức `null`. Script này chỉ thêm hai khoá null và tăng `schema_version`.

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

# Trường thêm ở schema 2 → giá trị mặc định khi nâng cấp.
THEM_V2 = {"model_load_seconds": None, "rss_scope": None}

DICH = 2

# Thứ tự khoá đúng như `save_prediction()` dựng payload. Chỉ `setdefault` rồi ghi thì
# hai khoá mới rơi xuống cuối file; lần chạy engine thật kế tiếp sẽ ghi lại theo thứ
# tự này và `git diff` đỏ nguyên file — che mất thay đổi thật của engine, đúng cái
# `prediction/` được commit để nhìn thấy.
THU_TU = (
    "schema_version",
    "engine",
    "engine_version",
    "doc_id",
    "capabilities",
    "text_md",
    "blocks",
    "images",
    "tables",
    "scan_label",
    "page_sizes",
    "seconds",
    "model_load_seconds",
    "peak_rss_mb",
    "rss_scope",
    "failed",
    "error",
    "config_fingerprint",
)


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
    if ver != 1:
        # Không đoán. Bản lạ có thể là bản mới hơn script này, và ghi đè nó là làm
        # mất dữ liệu mà không có đường phục hồi.
        print(f"  BỎ   {path}: schema_version={ver!r}, script chỉ nâng 1→2", file=sys.stderr)
        return "bo"

    for k, v in THEM_V2.items():
        raw.setdefault(k, v)
    raw["schema_version"] = DICH
    if set(raw) != set(THU_TU):
        # Không tự ý sắp lại một file có khoá lạ: sắp theo THU_TU sẽ **vứt** khoá
        # không có trong danh sách, im lặng.
        print(
            f"  BỎ   {path}: khoá lệch schema 2 "
            f"({sorted(set(raw) ^ set(THU_TU))})",
            file=sys.stderr,
        )
        return "bo"
    raw = {k: raw[k] for k in THU_TU}

    if thu:
        return "se_nang"
    # Giữ đúng khuôn `save_prediction()`: indent 2, không escape unicode, newline "\n",
    # có dòng trắng cuối. Lệch khuôn thì `git diff` lần chạy sau sẽ đỏ toàn bộ file.
    path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return "da_nang"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("root", type=Path, help="thư mục prediction/")
    p.add_argument(
        "--thu",
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
        "da_nang": "đã nâng lên schema 2",
        "se_nang": "sẽ nâng (chạy lại không có --thu để ghi)",
        "da_moi": "đã ở schema 2, không đụng",
        "bo": "bỏ qua (schema lạ)",
        "loi": "lỗi đọc",
    }
    for k, v in dem.items():
        print(f"{v:5d}  {ten.get(k, k)}")
    return 1 if dem.get("loi") else 0


if __name__ == "__main__":
    raise SystemExit(main())
