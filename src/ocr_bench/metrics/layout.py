"""B3b — bố cục: `block_f1` và `type_f1`.

## Định nghĩa toán học

Cho tập khối nhãn `G` và khối đoán `P`, chỉ giữ khối **có khung** (`box is not
None`). Dựng đồ thị hai phía với cạnh `(g, p)` khi `IoU(g, p) >= 0.5`, rồi lấy
phép ghép 1-1 **tối đa hoá số cặp trước, tổng IoU sau** (`metrics/matching.py`).
Gọi `M` là phép ghép đó.

- `TP = |M|`, `FP = |P| - TP`, `FN = |G| - TP`
- **block_f1** `= 2·TP / (2·TP + FP + FN)` — **không** xét `block_type`.
- **type_f1** `= (1/|T_G|) · Σ_{t ∈ T_G} F1_t`, trong đó `T_G` là tập type **có
  mặt trong nhãn**, và với mỗi type `t`:
  - `TP_t` = số cặp `(g, p) ∈ M` mà `type(g) = type(p) = t`
  - `FN_t` = số khối nhãn type `t` không ghép được, **cộng** số cặp `(g, p) ∈ M`
    có `type(g) = t ≠ type(p)`
  - `FP_t` = số khối đoán type `t` không ghép được, **cộng** số cặp `(g, p) ∈ M`
    có `type(p) = t ≠ type(g)`
  - `F1_t = 2·TP_t / (2·TP_t + FP_t + FN_t)`

Ba chỗ dễ làm sai, ghi tại đây:

1. **Ghép tối ưu, không tham lam.** `imgf1.py` được phép tham lam vì nó lập luận
   trên tiền đề "các box nhãn rời nhau" — đúng với ảnh. Với khối thì sai: caption
   nằm trong picture, tiêu đề mục nằm trong khung mục. Phản ví dụ cụ thể ở
   docstring `metrics/matching.py`: tham lam ra 1 cặp, tối ưu ra 2, ngay tại
   ngưỡng 0.5.

2. **Mẫu số macro chỉ gồm type có trong nhãn.** Cho type engine bịa ra vào mẫu số
   là để engine tự chọn mẫu số của chính nó — bịa càng nhiều type lạ thì mỗi type
   sai càng ít trọng số. Hệ quả phải nói thẳng: khối bịa ra **không** bị `type_f1`
   phạt; nó bị phạt ở `block_f1` (một FP). Hai cột đọc cùng nhau, không tách.

3. **Hai cột chứ không một.** `block_f1` trả lời "tìm đúng bao nhiêu khối",
   `type_f1` trả lời "gọi tên khối có đúng không". Engine tách khối chuẩn nhưng
   gọi mọi thứ là ``TEXT`` có `block_f1` = 1.0 và `type_f1` thấp — gộp một cột là
   mất đúng chẩn đoán đó.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from ocr_bench.metrics.base import Metric
from ocr_bench.metrics.matching import NGUONG_MAC_DINH, ghep_toi_uu
from ocr_bench.types import (
    AnnotationGT,
    Box,
    Capability,
    GroundTruth,
    NAReason,
    OcrBlock,
    OcrResult,
)

__all__ = [
    "NGUONG_MAC_DINH",
    "layout_scores",
    "type_scores",
    "BlockF1Metric",
    "TypeF1Metric",
]


def layout_scores(
    nhan: Sequence[Box],
    doan: Sequence[Box],
    nguong: float = NGUONG_MAC_DINH,
) -> tuple[float, float, dict[str, object]]:
    """Trả `(f1, chất lượng IoU, chi tiết)` — cùng hình dạng với `img_scores()`.

    `chất lượng IoU` = tổng IoU các cặp khớp chia cho `TP + FP + FN`: box thừa và
    box thiếu đều vào mẫu số, nên engine chỉ xuất một khối duy nhất mà nó tự tin
    không được 1.0.
    """
    cap = ghep_toi_uu(nhan, doan, nguong)
    tp = len(cap)
    fp = len(doan) - tp
    fn = len(nhan) - tp

    f1 = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 0.0
    mau = tp + fp + fn
    chat_luong = sum(c[2] for c in cap) / mau if mau else 0.0

    return (
        f1,
        chat_luong,
        {
            "nguong": nguong,
            "n_nhan": len(nhan),
            "n_doan": len(doan),
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": tp / len(doan) if doan else 0.0,
            "recall": tp / len(nhan) if nhan else 0.0,
            "iou_tung_cap": [round(c[2], 6) for c in cap],
        },
    )


def _ke_toan_type(
    nhan: Sequence[OcrBlock],
    doan: Sequence[OcrBlock],
    cap: Sequence[tuple[int, int, float]],
) -> dict[str, dict[str, int]]:
    """Sổ TP/FP/FN theo từng tên type. Xem công thức ở docstring module."""
    so: dict[str, dict[str, int]] = {}

    def o(ten: str) -> dict[str, int]:
        return so.setdefault(ten, {"tp": 0, "fp": 0, "fn": 0})

    da_nhan = {c[0] for c in cap}
    da_doan = {c[1] for c in cap}

    for i, j, _ in cap:
        t_nhan = nhan[i].block_type.value
        t_doan = doan[j].block_type.value
        if t_nhan == t_doan:
            o(t_nhan)["tp"] += 1
        else:
            # Gọi sai tên là **hai** lỗi: type nhãn mất một dương tính, type đoán
            # nhận một dương tính giả.
            o(t_nhan)["fn"] += 1
            o(t_doan)["fp"] += 1

    for i, k in enumerate(nhan):
        if i not in da_nhan:
            o(k.block_type.value)["fn"] += 1
    for j, k in enumerate(doan):
        if j not in da_doan:
            o(k.block_type.value)["fp"] += 1

    return so


def type_scores(
    nhan: Sequence[OcrBlock],
    doan: Sequence[OcrBlock],
    nguong: float = NGUONG_MAC_DINH,
) -> tuple[float, dict[str, object]]:
    """Macro-F1 theo type, trung bình trên các type **có mặt trong nhãn**."""
    cap = ghep_toi_uu(
        [k.box for k in nhan if k.box is not None],
        [k.box for k in doan if k.box is not None],
        nguong,
    )
    theo_type = _ke_toan_type(nhan, doan, cap)
    types_macro = sorted({k.block_type.value for k in nhan})

    tung_type: dict[str, float] = {}
    for t in types_macro:
        s = theo_type.get(t, {"tp": 0, "fp": 0, "fn": 0})
        mau = 2 * s["tp"] + s["fp"] + s["fn"]
        tung_type[t] = 2 * s["tp"] / mau if mau else 0.0

    macro = sum(tung_type.values()) / len(types_macro) if types_macro else 0.0

    return macro, {
        "nguong": nguong,
        "n_nhan": len(nhan),
        "n_doan": len(doan),
        "tp": len(cap),
        "fp": len(doan) - len(cap),
        "fn": len(nhan) - len(cap),
        "theo_type": theo_type,
        # Chỉ những type này vào mẫu số macro — xem quyết định 2.
        "types_macro": types_macro,
        "f1_tung_type": {t: round(v, 6) for t, v in tung_type.items()},
    }


class _LayoutBase(Metric):
    """Phần dùng chung: cùng cổng năng lực, cùng cách loại khối không có khung."""

    requires: ClassVar[frozenset[Capability]] = frozenset({Capability.BLOCK_BBOX})
    gt_kinds: ClassVar[tuple[type, ...]] = (AnnotationGT,)
    nguong: ClassVar[float] = NGUONG_MAC_DINH

    @staticmethod
    def _khoi(blocks: Sequence[OcrBlock]) -> list[OcrBlock]:
        """`OcrBlock.box` được phép `None` (engine có chữ nhưng không có toạ độ).
        Khối không có khung thì không ghép được — bỏ khỏi cả tử lẫn mẫu, chứ đếm
        nó vào `n_doan` là phạt engine vì một khối nó chưa từng định vị."""
        return [k for k in blocks if k.box is not None]

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AnnotationGT)  # gt_kinds đã lọc
        if not self._khoi(gt.blocks) and not self._khoi(result.blocks):
            # Cùng quyết định 3 của `imgf1.py`: hai bên cùng rỗng là "không có gì
            # để đo". Nhãn rỗng mà engine CÓ khối thì rơi xuống `_compute()` và
            # ăn 0.0 — dương tính giả vẫn bị phạt.
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "nhãn không có khối và engine cũng không trả khung nào"
            }
        return None


class BlockF1Metric(_LayoutBase):
    """F1 của phép ghép khối ở IoU ≥ ngưỡng — "tìm đúng bao nhiêu khối"."""

    name: ClassVar[str] = "block_f1"

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        f1, _, chi_tiet = layout_scores(
            [k.box for k in self._khoi(gt.blocks) if k.box is not None],
            [k.box for k in self._khoi(result.blocks) if k.box is not None],
            self.nguong,
        )
        return f1, chi_tiet


class TypeF1Metric(_LayoutBase):
    """Macro-F1 theo loại khối — "gọi tên khối có đúng không".

    Đọc cùng `block_f1`: `block_f1` cao mà cột này thấp là cắt đúng chỗ nhưng gán
    nhãn sai; ngược lại là gán tên đúng trên một tập khối tìm được quá ít.
    """

    name: ClassVar[str] = "type_f1"

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        return type_scores(
            self._khoi(gt.blocks), self._khoi(result.blocks), self.nguong
        )
