"""Vẽ trang PDF kèm khung nhãn và khung engine — TASK-088 (D2).

    py -3 scripts/d2_render.py <doc_id> <engine> [--out FILE]

D2 đòi "đọc tay". Không có ảnh thì "đọc tay" chỉ là đọc lại toạ độ, mà toạ độ đúng là
thứ đang bị nghi ngờ — dùng nó để kiểm chính nó thì không kết luận được gì.

Xanh = nhãn (`AnnotationGT.images`) · Đỏ = engine · Vàng = khối nhãn khác ảnh, vẽ mờ để
biết chỗ đó nhãn gọi là gì.

Ảnh sinh ra ở `results/d2-render/`, **không** commit (xem `.gitignore`): chúng là dẫn
xuất từ PDF + nhãn đã có trong repo, sinh lại được bằng đúng lệnh trên.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pypdfium2 as pdfium
from PIL import ImageDraw

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "src"))

from ocr_bench.corpus import load_doclaynet  # noqa: E402
from ocr_bench.prediction import load_predictions  # noqa: E402

TY_LE = 2.0  # 2x để chữ nhỏ trong logo vẫn đọc được


def _tim_pdf(doc_id: str) -> Path:
    for p in (GOC / "pdfs").rglob(f"{doc_id}.pdf"):
        return p
    raise SystemExit(f"không thấy PDF của `{doc_id}`")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doc_id")
    ap.add_argument("engine")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    gt = load_doclaynet()
    khop = [k for k in gt if k.startswith(args.doc_id)]
    if len(khop) != 1:
        raise SystemExit(f"`{args.doc_id}` khớp {len(khop)} tài liệu — cần đúng 1")
    doc_id = khop[0]
    g = gt[doc_id]

    res = {(r.engine, r.doc_id): r for r in load_predictions(GOC / "prediction")}
    r = res.get((args.engine, doc_id))
    if r is None:
        raise SystemExit(f"`{args.engine}` không có dự đoán cho tài liệu này")

    trang = pdfium.PdfDocument(str(_tim_pdf(doc_id)))[0]
    anh = trang.render(scale=TY_LE).to_pil().convert("RGB")
    W, H = anh.size
    ve = ImageDraw.Draw(anh)

    def khung(b, mau: str, day: int, nhan: str) -> None:
        xy = (b.x0 * W, b.y0 * H, b.x1 * W, b.y1 * H)
        ve.rectangle(xy, outline=mau, width=day)
        ve.text((xy[0] + 3, max(0, xy[1] - 12)), nhan, fill=mau)

    for b in g.blocks:
        if b.box:
            khung(b.box, "#c8a200", 1, b.block_type.value)
    for i, b in enumerate(g.images):
        khung(b, "#0066ff", 3, f"NHAN img{i}")
    for i, im in enumerate(r.images):
        if im.box:
            khung(im.box, "#ff0000", 3, f"{args.engine} img{i}")

    out = args.out or (GOC / "results" / "d2-render" / f"{doc_id[:12]}-{args.engine}.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    anh.save(out)
    print(f"{out}  ({W}x{H})  nhãn_ảnh={len(g.images)} đoán_ảnh={len(r.images)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
