"""Sinh quần thể `sabotage` xuống `prediction/` từ dự đoán đã lưu của engine nguồn.

    py -3 scripts/make_sabotage.py            # xem sẽ làm gì, không ghi
    py -3 scripts/make_sabotage.py --ghi      # ghi thật

Không chạy engine nào, không đụng PDF: nguồn lấy từ `prediction/<nguồn>/` có sẵn.

## Vì sao cần script riêng thay vì `make_predictions.py --engines sabotage`

`make_predictions.py` dựng `SabotageAdapter()` không tham số, tức bọc `noop` mặc định.
`noop` trả chuỗi rỗng, làm hỏng cái rỗng thì vẫn rỗng — quần thể sinh ra hoà `0.0000`
với `noop` ở mọi metric. **Hoà ở đáy không phải đứng bét**, nên cổng C2 (AC-01 của
TASK-086) xanh mà không kiểm được gì.

Đó chính là thứ đã nằm trên đĩa: 41 file `sabotage/1+noop`, trong khi `c2_report.py`
dựng riêng một bản `sabotage/1+opendataloader` 205 tài liệu trong bộ nhớ. Hai quần
thể, một cái tên, hai bảng khác nhau. Script này ghi bản **đúng** xuống đĩa để bảng
công bố (D1) và cổng C2 chấm cùng một thứ; cả hai đều đi qua
`discrimination.dung_sabotage()`.

Mặc định **chạy khan** (in ra rồi thoát). Ghi đè một quần thể đang được trích số ra
báo cáo là việc phải gõ thêm một cờ mới xảy ra.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from collections import Counter
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "src"))

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ocr_bench import discrimination as D  # noqa: E402
from ocr_bench.prediction import load_predictions, save_predictions  # noqa: E402

TEN = "sabotage"


def _don_thu_muc(d: Path) -> int:
    """Xoá sạch quần thể cũ. Trả về số file `*.json` đã xoá.

    Phải xoá cả thư mục `<doc_id>.images/`: bỏ lại ảnh của quần thể cũ thì lần nạp sau
    `OcrImage.data` trỏ vào ảnh của một lượt chạy khác, và không có gì trong bảng chỉ
    ra điều đó.

    Xoá *cả* thư mục thay vì ghi đè từng file vì hai quần thể có bộ `doc_id` khác nhau
    (41 so với 205) — ghi đè chỉ phủ lên phần giao, phần còn lại nằm lại và trộn vào
    bảng dưới cùng một tên engine.
    """
    n = len(list(d.glob("*.json")))
    for con in sorted(d.iterdir()):
        shutil.rmtree(con) if con.is_dir() else con.unlink()
    return n


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "--nguon",
        default=D.NGUON_SABOTAGE,
        help=f"engine làm nguồn (mặc định {D.NGUON_SABOTAGE})",
    )
    p.add_argument("--ghi", action="store_true", help="ghi thật; thiếu cờ này là chạy khan")
    args = p.parse_args(argv)

    res = load_predictions(GOC / "prediction")
    cu = [r for r in res if r.engine == TEN]
    moi = D.dung_sabotage(res, nguon=args.nguon)

    ver_cu = Counter(r.engine_version for r in cu)
    ver_moi = {r.engine_version for r in moi}
    print(f"nạp {len(res)} dự đoán")
    print(f"  quần thể cũ trên đĩa : {len(cu):>4} tài liệu · {dict(ver_cu) or '(chưa có)'}")
    print(f"  quần thể sẽ ghi      : {len(moi):>4} tài liệu · {sorted(ver_moi)}")

    if len(ver_moi) != 1:
        print(f"LỖI: quần thể mới trộn nhiều version: {sorted(ver_moi)}", file=sys.stderr)
        return 1

    if not args.ghi:
        print("\n(chạy khan — thêm --ghi để thực hiện)")
        return 0

    d = GOC / "prediction" / TEN
    d.mkdir(parents=True, exist_ok=True)
    da_xoa = _don_thu_muc(d)
    save_predictions(moi, GOC / "prediction")
    print(f"\nxoá {da_xoa} file cũ · ghi {len(moi)} file mới vào {d}")
    print("Chạy lại `scripts/c2_report.py` rồi `scripts/d1_report.py` để cập nhật bảng.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
