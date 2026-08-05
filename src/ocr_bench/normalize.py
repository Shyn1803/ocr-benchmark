"""Chuẩn hoá text trước khi so.

Mọi metric text **phải** đi qua `normalize_text()`. Không có nó, hai chuỗi hiển thị
giống hệt nhau trên màn hình vẫn cho CER > 0 chỉ vì một bên dùng NFC còn bên kia
NFD — và điểm chênh lệch đó không nói gì về chất lượng OCR.

Việc này quan trọng gấp bội khi sang giai đoạn 2 (tiếng Việt): "ề" có thể là 1, 2
hay 3 code point tuỳ nguồn.
"""

from __future__ import annotations

import re
import unicodedata

__all__ = ["normalize_text", "normalize_ws"]

# Dấu nháy/gạch ngang mà OCR hay đổi qua lại — khác biệt kiểu chữ, không phải lỗi đọc.
_PUNCT_FOLD = {
    "‘": "'",
    "’": "'",
    "‚": "'",
    "“": '"',
    "”": '"',
    "„": '"',
    "–": "-",
    "—": "-",
    "―": "-",
    "−": "-",
    " ": " ",
    "​": "",
    "﻿": "",
}
_PUNCT_RE = re.compile("|".join(map(re.escape, _PUNCT_FOLD)))
_WS_RE = re.compile(r"[ \t\r\f\v]+")
_BLANKLINES_RE = re.compile(r"\n{3,}")


def normalize_ws(text: str) -> str:
    """Gộp khoảng trắng ngang, bỏ trắng cuối dòng, ép tối đa 1 dòng trống."""
    text = _WS_RE.sub(" ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    return _BLANKLINES_RE.sub("\n\n", text).strip()


def normalize_text(text: str, *, fold_punct: bool = True) -> str:
    """NFC + gộp khoảng trắng (+ gộp dấu nháy/gạch ngang).

    NFC chứ không NFD: NFC là dạng chuẩn của web và của hầu hết PDF text layer, nên
    nó giữ độ dài chuỗi gần với cái người đọc thấy — mà CER thì chia cho độ dài.
    """
    text = unicodedata.normalize("NFC", text)
    if fold_punct:
        text = _PUNCT_RE.sub(lambda m: _PUNCT_FOLD[m.group()], text)
        text = unicodedata.normalize("NFC", text)
    return normalize_ws(text)
