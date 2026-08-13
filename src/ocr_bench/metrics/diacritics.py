"""B8 — dấu tiếng Việt: `diacritics_acc`.

## Định nghĩa toán học

Cho nhãn `g` và đoán `p`, đặt `base(s) = ` chuỗi `s` sau khi bỏ mọi dấu phụ (NFD,
loại ký tự có `combining != 0`) và quy `đ/Đ → d/D`. Căn `base(g)` với `base(p)`
bằng `rapidfuzz.distance.Indel.opcodes` để lấy các đoạn `equal`; phép căn này cho
mỗi vị trí nhãn `i` một vị trí đoán `j(i)` hoặc không có.

Gọi `D = {i : g[i] có dấu}` (tức `base(g[i]) != g[i]`). Khi đó

    diacritics_acc = 1 − |{i ∈ D : p[j(i)] != g[i]}| / |D|

và chia lỗi làm hai loại để chẩn đoán:

- **mất dấu** — `j(i)` không tồn tại, hoặc `p[j(i)]` không có dấu nào;
- **sai dấu** — `p[j(i)]` có dấu nhưng khác dấu của `g[i]`.

`|D| = 0` → `NO_GROUND_TRUTH`, **không** phải 1.0.

Bốn quyết định:

1. **Mẫu số là số ký tự có dấu trong nhãn, không phải toàn bộ ký tự.** Lấy toàn
   bộ thì "Việt Nam 2026" mất sạch dấu vẫn được 12/13 = 0.92 — một con số đẹp cho
   một đầu ra hỏng, và tài liệu càng ít dấu điểm càng cao miễn phí.

2. **Căn theo `Indel.opcodes`, không theo chỉ số.** Engine chèn thừa vài chữ ở đầu
   thì căn theo chỉ số làm cả câu lệch một ô và điểm về 0 dù engine đặt dấu hoàn
   hảo — đo lỗi chèn chứ không đo lỗi dấu.

3. **Vì sao không dùng `cer`.** `cer` đếm ký tự sai nhưng không tách được lỗi mất
   dấu khỏi lỗi đọc nhầm chữ. Với tiếng Việt đó là hai bệnh khác nhau: "hoa" ↔
   "hóa" là mô hình không có tiếng Việt, "hoa" ↔ "boa" là nhận dạng chữ sai. Engine
   mất sạch dấu vẫn có thể có `cer` ≈ 0.15 nghe khá ổn.

4. **Hai vế đi qua `normalize_text()` (NFC) trước khi so.** Metric so từng code
   point, nên nhãn NFC gặp đầu ra NFD thì "ề" một bên là 1 code point, bên kia là
   2–3, và *mọi* ký tự có dấu trượt: engine đọc đúng 100% vẫn bị chấm 0.2. Bỏ sót
   bước này tới 2026-08-13 (sửa cùng `cell_f1`, cùng một bệnh).
"""

from __future__ import annotations

import unicodedata
from typing import ClassVar

from ocr_bench.metrics.base import Metric
from ocr_bench.normalize import normalize_text
from ocr_bench.types import (
    AnnotationGT,
    Capability,
    GroundTruth,
    NAReason,
    OcrResult,
)

__all__ = ["chu_goc", "co_dau", "diacritic_scores", "DiacriticsMetric"]

# `đ`/`Đ` (U+0111/U+0110) là ký tự nguyên khối — NFD **không** phân rã được. Không
# xử lý riêng thì "đường" và "duong" không căn được với nhau, và mọi lỗi mất dấu
# của chữ `đ` bị đếm nhầm thành lỗi nhận dạng chữ.
_D_GACH = {"đ": "d", "Đ": "D"}


def chu_goc(ch: str) -> str:
    """Chữ cái gốc của một ký tự: bỏ hết dấu phụ, `đ`/`Đ` → `d`/`D`."""
    if ch in _D_GACH:
        return _D_GACH[ch]
    goc = "".join(
        c for c in unicodedata.normalize("NFD", ch) if not unicodedata.combining(c)
    )
    return goc or ch


def co_dau(ch: str) -> bool:
    """Ký tự này có mang dấu không."""
    return chu_goc(ch) != ch


def _can(g: str, p: str) -> dict[int, int]:
    """Vị trí nhãn → vị trí đoán, theo các đoạn `equal` của `Indel.opcodes`."""
    from rapidfuzz.distance import Indel  # nhập lười: extra `metrics`, đúng lệ nid.py

    nen_g = "".join(chu_goc(c) for c in g)
    nen_p = "".join(chu_goc(c) for c in p)
    ra: dict[int, int] = {}
    for op in Indel.opcodes(nen_g, nen_p):
        if op.tag != "equal":
            continue
        # `src` là chuỗi thứ nhất, `dest` là chuỗi thứ hai — xem ghi chú cùng nội
        # dung ở `metrics/assertions.py`.
        for k in range(op.src_end - op.src_start):
            ra[op.src_start + k] = op.dest_start + k
    return ra


def diacritic_scores(g: str, p: str) -> tuple[float, dict[str, object]]:
    """Trả `(điểm, chi tiết)`. `n_co_dau == 0` thì điểm là 0.0 và người gọi phải
    tự quyết N/A — `DiacriticsMetric` làm việc đó ở `_na_rieng()`."""
    # Chuẩn hoá NFC hai vế TRƯỚC khi so từng ký tự. Metric này so `p[j] == g[i]`
    # trên một code point, nên NFD làm "ề" tách thành 2–3 code point và mọi ký tự
    # có dấu đều trượt — engine đọc đúng hoàn toàn vẫn bị chấm 0.2. Đây đúng là
    # chỗ đau nhất của tiếng Việt, và cũng là hợp đồng đã ghi ở `normalize.py`.
    g = normalize_text(g)
    p = normalize_text(p)
    cap = _can(g, p)
    n_co_dau = n_mat_dau = n_sai_dau = 0
    vi_du: list[tuple[str, str]] = []

    for i, ch in enumerate(g):
        if not co_dau(ch):
            continue
        n_co_dau += 1
        j = cap.get(i)
        ra = p[j] if j is not None else ""
        if ra == ch:
            continue
        # Không căn được coi như mất dấu: dấu đó không xuất hiện ở đầu ra.
        if not ra or not co_dau(ra):
            n_mat_dau += 1
        else:
            n_sai_dau += 1
        if len(vi_du) < 20:
            vi_du.append((ch, ra))

    n_sai = n_mat_dau + n_sai_dau
    diem = 1.0 - n_sai / n_co_dau if n_co_dau else 0.0
    return diem, {
        "n_ky_tu_nhan": len(g),
        "n_co_dau": n_co_dau,
        "n_sai": n_sai,
        "n_mat_dau": n_mat_dau,
        "n_sai_dau": n_sai_dau,
        "vi_du_sai": vi_du,
    }


class DiacriticsMetric(Metric):
    """Tỷ lệ ký tự có dấu được engine đặt đúng dấu."""

    name: ClassVar[str] = "diacritics_acc"
    requires: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})
    gt_kinds: ClassVar[tuple[type, ...]] = (AnnotationGT,)

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AnnotationGT)  # gt_kinds đã lọc
        # Cùng lý do như trong `diacritic_scores`: nhãn ở dạng NFD thì `co_dau()`
        # nhìn thấy toàn chữ trần cộng dấu rời, kết luận "nhãn không có dấu nào"
        # và trả N/A cho một tài liệu tiếng Việt đầy dấu.
        chu_nhan = normalize_text(gt.text or "")
        if not chu_nhan:
            return NAReason.NO_GROUND_TRUTH, {"ly_do": "nhãn không có chữ"}
        if not any(co_dau(c) for c in chu_nhan):
            # Nhãn không có dấu nào thì không có gì để đo. Chấm 1.0 ở đây là rót
            # điểm miễn phí cho mọi tài liệu tiếng Anh trong bộ mẫu.
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "nhãn không có ký tự mang dấu nào"
            }
        return None

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        assert gt.text is not None  # `_na_rieng` đã chặn
        # Engine ĐÃ khai `TEXT_MD` mà `text_md` rỗng là lỗi của engine, không phải
        # thiếu năng lực — chấm 0, không N/A.
        return diacritic_scores(gt.text, result.text_md or "")
