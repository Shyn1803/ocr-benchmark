"""Đo hệ toạ độ của OpenDataLoader trên PDF do chính ta dựng — AC-02 của A5.

    py -3 scripts/measure_opendataloader_coords.py     # exit 0 nếu cả 4 phép đo ra kết luận

A0 để trống ba ô của OpenDataLoader trong bảng hệ toạ độ (`README.md` §1): gốc,
chiều trục y, đơn vị. Bài học của A4 là **không tin trường nào của engine cho tới
khi đối chiếu được với nguồn thứ hai** — nên ở đây nguồn thứ hai là PDF *ta tự
sinh*, đặt chữ vào đúng toạ độ đã biết trước.

Bốn câu hỏi, bốn phép đo:

1. **Gốc ở trên hay dưới?** Đặt chữ `TOPLEFT` gần mép trên, `BOTRIGHT` gần mép
   dưới. Cái nào có `y` nhỏ hơn thì biết trục y chạy về phía nào.
2. **Đơn vị là điểm PDF hay pixel?** Trang rộng 595 pt. Nếu số lớn nhất bám 595
   thì là điểm; nếu bám ~1240 thì là pixel 150 dpi.
3. **Thứ tự 4 số trong `bounding box`?** `[x0, y0, x1, y1]` hay `[x, y, w, h]`?
   Phân biệt được vì chữ ngắn: `w` chỉ vài chục pt còn `x1` thì hàng trăm.
4. **MediaBox không bắt đầu từ (0,0) thì sao?** Đây đúng cái bẫy `force_ocr` của
   Marker (README §1). Dựng lại trang thứ hai với MediaBox dịch đi (100, 200) và
   xem engine có trừ gốc đi không.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

RONG, CAO = 595.0, 842.0
# Toạ độ trong PDF content stream là hệ user space: gốc dưới-trái, y hướng LÊN.
# Đây là quy ước của chính định dạng PDF, không phải của engine nào.
TOP_X, TOP_Y = 50.0, 780.0
BOT_X, BOT_Y = 400.0, 40.0
DICH_X, DICH_Y = 100.0, 200.0  # phép đo 4


def _pdf(media_x0: float = 0.0, media_y0: float = 0.0) -> bytes:
    """PDF một trang, hai chuỗi ở hai góc đối nhau, MediaBox dịch được."""
    text = (
        f"BT /F1 12 Tf {media_x0 + TOP_X:.1f} {media_y0 + TOP_Y:.1f} Td (TOPLEFT) Tj ET\n"
        f"BT /F1 12 Tf {media_x0 + BOT_X:.1f} {media_y0 + BOT_Y:.1f} Td (BOTRIGHT) Tj ET"
    ).encode("latin-1")

    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [%.1f %.1f %.1f %.1f] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        % (media_x0, media_y0, media_x0 + RONG, media_y0 + CAO),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length %d >>\nstream\n" % len(text) + text + b"\nendstream",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += (
        b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
        % (len(objs) + 1, xref)
    )
    return bytes(out)


def _chay(pdf_bytes: bytes, ten: str) -> list[dict]:
    """Chạy OpenDataLoader, trả danh sách node phẳng có `bounding box`."""
    from ocr_bench.adapters.opendataloader import chay_cli, node_phang

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / f"{ten}.pdf").write_bytes(pdf_bytes)
        ra = d / "out"
        chay_cli([d / f"{ten}.pdf"], ra)
        doc = json.loads((ra / f"{ten}.json").read_text(encoding="utf-8"))
    return [n for n in node_phang(doc) if n.get("bounding box")]


def _tim(nodes: list[dict], chu: str) -> tuple[str, list[float]] | None:
    for n in nodes:
        if chu in (n.get("content") or ""):
            return n.get("content", ""), [float(v) for v in n["bounding box"]]
    return None


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if shutil.which("java") is None:
        print("Chưa có java trên PATH. Chạy `py -3 scripts/setup_java.py` trước.")
        return 1

    dat = True
    print(f"Trang dựng: {RONG} x {CAO} pt (điểm PDF)")
    print(f"  TOPLEFT  đặt ở user space ({TOP_X}, {TOP_Y})  ← gần mép TRÊN")
    print(f"  BOTRIGHT đặt ở user space ({BOT_X}, {BOT_Y})  ← gần mép DƯỚI\n")

    nodes = _chay(_pdf(), "probe")
    top, bot = _tim(nodes, "TOPLEFT"), _tim(nodes, "BOTRIGHT")
    if not (top and bot):
        print(f"✗ Không tìm thấy cả hai chuỗi. Node đọc được: {[n.get('content') for n in nodes]}")
        return 1
    (_, htop), (_, hbot) = top, bot
    print(f"1) bounding box TOPLEFT  = {htop}")
    print(f"   bounding box BOTRIGHT = {hbot}")

    # --- 1. chiều trục y ------------------------------------------------------
    if htop[1] > hbot[1]:
        print("   → chữ ở mép TRÊN có y LỚN hơn ⇒ gốc DƯỚI-TRÁI, trục y hướng LÊN")
        y_len = True
    elif htop[1] < hbot[1]:
        print("   → chữ ở mép TRÊN có y NHỎ hơn ⇒ gốc TRÊN-TRÁI, trục y hướng XUỐNG")
        y_len = False
    else:
        print("   ✗ hai y bằng nhau — phép đo hỏng")
        return 1

    # --- 2. đơn vị ------------------------------------------------------------
    lon_nhat_x = max(htop[2], hbot[2])
    if lon_nhat_x <= RONG + 1:
        print(f"\n2) x lớn nhất = {lon_nhat_x:.2f} ≤ chiều rộng trang {RONG} ⇒ đơn vị ĐIỂM PDF")
    else:
        print(f"\n2) ✗ x lớn nhất = {lon_nhat_x:.2f} > {RONG} — KHÔNG phải điểm PDF")
        dat = False

    # --- 3. thứ tự 4 số -------------------------------------------------------
    rong_neu_x1 = htop[2] - htop[0]
    if htop[2] > htop[0] and htop[3] > htop[1] and rong_neu_x1 > 20:
        print(f"3) box[2]-box[0] = {rong_neu_x1:.2f} pt — bằng bề ngang chuỗi 7 ký tự 12 pt")
        print("   ⇒ thứ tự là [x0, y0, x1, y1], KHÔNG phải [x, y, w, h]")
    else:
        print(f"3) ✗ không kết luận được thứ tự: {htop}")
        dat = False

    # --- 3b. gốc x ------------------------------------------------------------
    if abs(htop[0] - TOP_X) < 5:
        print(f"3b) x0 của TOPLEFT = {htop[0]:.2f} ≈ {TOP_X} đã đặt ⇒ gốc x ở mép TRÁI")
    else:
        print(f"3b) ✗ x0 = {htop[0]:.2f}, đã đặt {TOP_X}")
        dat = False

    # --- 4. MediaBox lệch gốc -------------------------------------------------
    nodes2 = _chay(_pdf(DICH_X, DICH_Y), "probe_dich")
    top2 = _tim(nodes2, "TOPLEFT")
    if top2 is None:
        print("\n4) ✗ trang MediaBox lệch: không đọc ra chuỗi nào")
        return 1
    _, h2 = top2
    lech_x, lech_y = h2[0] - htop[0], h2[1] - htop[1]
    print(f"\n4) MediaBox dịch ({DICH_X}, {DICH_Y}) → box TOPLEFT = {h2}")
    print(f"   lệch so với trang gốc: Δx={lech_x:+.2f}  Δy={lech_y:+.2f}")
    if abs(lech_x - DICH_X) < 2 and abs(lech_y - DICH_Y) < 2:
        print("   ⇒ engine trả toạ độ TUYỆT ĐỐI, KHÔNG trừ gốc MediaBox.")
        print("     Adapter BẮT BUỘC truyền page_x0/page_y0 — đúng cái bẫy force_ocr của Marker.")
    elif abs(lech_x) < 2 and abs(lech_y) < 2:
        print("   ⇒ engine đã trừ gốc MediaBox, toạ độ tính từ (0,0) của trang.")
    else:
        print("   ✗ lệch không khớp cả hai giả thuyết")
        dat = False

    print("\n" + "=" * 72)
    print(f"KẾT LUẬN: gốc {'DƯỚI' if y_len else 'TRÊN'}-TRÁI · "
          f"trục y hướng {'LÊN' if y_len else 'XUỐNG'} · đơn vị điểm PDF · [x0,y0,x1,y1]")
    print("=" * 72)
    return 0 if dat else 1


if __name__ == "__main__":
    sys.exit(main())
