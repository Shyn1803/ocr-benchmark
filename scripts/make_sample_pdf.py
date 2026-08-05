"""Sinh một PDF hợp lệ tối thiểu để chạy thử A1b.

Viết thẳng cú pháp PDF thay vì gọi reportlab/matplotlib: venv của bench cố ý **chưa
có thư viện PDF nào**, và A1b không phải là chỗ để kéo phụ thuộc vào. File ra là PDF
thật, mở được bằng mọi trình đọc.

⚠️ Đây **không phải** bộ mẫu. Bộ mẫu tiếng Anh có nhãn là việc của A3 (TASK-074).
File này chỉ để `run_engines()` có một `Path` thật mà đi qua.

    py -3 scripts/make_sample_pdf.py
"""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "pdfs" / "sample_minimal.pdf"

DONG = [
    "Sovereign OCR bench - sample document",
    "Line two of the sample text.",
    "Line three, for reading order.",
]


def build() -> bytes:
    text = "BT /F1 14 Tf 72 720 Td 18 TL\n" + "\n".join(
        f"({d}) Tj T*" for d in DONG
    ) + "\nET"
    stream = text.encode("latin-1")

    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + body + b"\nendobj\n"

    xref = len(out)
    out += b"xref\n0 %d\n" % (len(objs) + 1)
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += (
        b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
        % (len(objs) + 1, xref)
    )
    return bytes(out)


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(build())
    print(f"{OUT} — {OUT.stat().st_size} bytes")
