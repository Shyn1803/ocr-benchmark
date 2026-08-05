"""Kiểm lại hệ toạ độ nhãn DocLayNet trên chính dữ liệu trong repo — AC-05 của A3.

    py -3 scripts/check_doclaynet_coords.py     # exit 0 nếu cả 3 kiểm đều đạt

Ba câu hỏi, ba phép đo, không phép nào dựa vào tài liệu thượng nguồn:

1. **y hướng lên hay xuống?** So y của `Page-header` với `Page-footer`. Đây là cặp
   lớp duy nhất mà vị trí trên/dưới nằm ngay trong tên — không cần biết gì thêm.
2. **nhãn bố cục và text cell có cùng hệ không?** Đếm tỉ lệ tâm text cell rơi vào
   một hộp bố cục, rồi đo lại sau khi lật trục y. Nếu cùng hệ và y hướng xuống thì
   số thứ nhất phải cao hẳn số thứ hai.
3. **kéo giãn riêng trục hay aspect-fit?** Nếu giữ tỉ lệ khung hình thì trên trang
   dọc, x không thể vượt `1025·W/max(W,H)`. Đếm số trang vi phạm.

Số ra khớp bảng trong `ground-truth/doclaynet/README.md`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
GT = ROOT / "ground-truth" / "doclaynet"


def main() -> int:
    coco_path = GT / "layout_coco.json"
    if not coco_path.exists():
        print(f"thiếu {coco_path} — chạy scripts/fetch_doclaynet.py trước")
        return 1
    coco = json.loads(coco_path.read_text(encoding="utf-8"))
    ten_lop = {c["id"]: c["name"] for c in coco["categories"]}

    hop_theo_anh: dict[int, list[list[float]]] = {}
    for a in coco["annotations"]:
        hop_theo_anh.setdefault(a["image_id"], []).append(a["bbox"])

    dat = True

    # --- 1. chiều trục y ------------------------------------------------------
    hy = [a["bbox"][1] for a in coco["annotations"] if ten_lop[a["category_id"]] == "Page-header"]
    fy = [a["bbox"][1] for a in coco["annotations"] if ten_lop[a["category_id"]] == "Page-footer"]
    if hy and fy:
        nguoc = sum(1 for h in hy if all(h > f for f in fy))
        print(f"1) Page-header y TB {sum(hy)/len(hy):.1f} (n={len(hy)}) | "
              f"Page-footer y TB {sum(fy)/len(fy):.1f} (n={len(fy)}) | ngược: {nguoc}")
        if not (sum(hy) / len(hy) < sum(fy) / len(fy) and nguoc == 0):
            dat = False
            print("   ✗ y KHÔNG hướng xuống như tài liệu ghi")

    # --- 2. chung hệ toạ độ ---------------------------------------------------
    trong = lat = tong = 0
    vi_pham = khong_vuong = 0
    for im in coco["images"]:
        cells_path = GT / "cells" / f"{Path(im['file_name']).stem}.json"
        if not cells_path.exists():
            continue
        d = json.loads(cells_path.read_text(encoding="utf-8"))
        md, cells = d["metadata"], d["cells"]
        hop = hop_theo_anh.get(im["id"], [])
        for c in cells:
            x, y, w, h = c["bbox"]
            cx, cy = x + w / 2, y + h / 2
            tong += 1
            if any(bx <= cx <= bx + bw and by <= cy <= by + bh for bx, by, bw, bh in hop):
                trong += 1
            cy_lat = md["coco_height"] - cy
            if any(bx <= cx <= bx + bw and by <= cy_lat <= by + bh for bx, by, bw, bh in hop):
                lat += 1

        # --- 3. kéo giãn riêng trục -------------------------------------------
        W, H = md["original_width"], md["original_height"]
        if W != H and cells:
            khong_vuong += 1
            if max(c["bbox"][0] + c["bbox"][2] for c in cells) > md["coco_width"] * W / max(W, H) + 1:
                vi_pham += 1

    if tong:
        p_trong, p_lat = 100 * trong / tong, 100 * lat / tong
        print(f"2) tâm cell trong hộp bố cục: {trong}/{tong} = {p_trong:.1f}% | nếu lật trục y: {p_lat:.1f}%")
        if not (p_trong > 95 and p_trong > p_lat + 20):
            dat = False
            print("   ✗ hai nguồn KHÔNG còn chung hệ toạ độ")

    if khong_vuong:
        print(f"3) trang không vuông: {khong_vuong} | vượt ngưỡng aspect-fit: {vi_pham}")
        if vi_pham < khong_vuong * 0.5:
            dat = False
            print("   ✗ trông như aspect-fit có viền đệm, KHÔNG phải kéo giãn riêng trục")

    print("\nKết luận: 1025×1025, gốc trên-trái, y xuống, kéo giãn riêng từng trục."
          if dat else "\nCÓ KIỂM KHÔNG ĐẠT — đọc lại ground-truth/doclaynet/README.md")
    return 0 if dat else 1


if __name__ == "__main__":
    raise SystemExit(main())
