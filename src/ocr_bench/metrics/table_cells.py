"""B7 — ô bảng: `cell_f1` và `table_recall`.

## Định nghĩa toán học

**cell_f1.** Mỗi bảng HTML được dựng thành **lưới** `L: (hàng, cột) → nội dung`,
trong đó ô có `rowspan=r`/`colspan=c` chiếm đủ `r×c` toạ độ (xem `dung_luoi()`).
Bảng nhãn thứ `k` ghép với bảng đoán thứ `k` **theo thứ tự xuất hiện**; bảng lẻ ở
một bên thì mọi ô của nó vào FN (nhãn) hoặc FP (đoán). Với mỗi cặp lưới:

- `TP = |{(v, ô) : L_nhãn[v] = L_đoán[v]}|`
- `FN = |L_nhãn| - TP`, `FP = |L_đoán| - TP`
- `cell_f1 = 2·TP / (2·TP + FP + FN)` trên tổng cộng dồn của mọi bảng.

Ghép theo **toạ độ**, không theo nội dung: bảng chuyển vị giữ nguyên tập nội dung
nhưng đổi hết ý nghĩa, ghép theo nội dung thì nó được 1.0.

**table_recall.** `= |M| / |G_box|` với `G_box` là bảng nhãn **có khung** và `M`
là phép ghép bipartite tối ưu ở `IoU ≥ 0.5` (`metrics/matching.py`).

## Hai trạng thái thiếu, không bao giờ gộp

Repo này **không có `Capability.TABLE_BBOX`**. Nên với `table_recall`:

- nhãn có bảng nhưng không có khung → **bộ mẫu** thiếu → `NO_GROUND_TRUTH`;
- engine trả bảng nhưng không trả khung → engine **không hứa** định vị bảng →
  `MISSING_CAPABILITY`.

Chấm 0 cho vế sau là phạt engine vì một năng lực nó chưa từng khai; gộp hai vế
làm một là xoá mất phân biệt "chưa có nhãn" với "engine không làm được".

Vì sao có file này khi đã có `teds.py`: TEDS trả lời "cây bảng có giống nhau
không". Nó không nói **ô nào** lệch — điểm 0.72 không chỉ ra chỗ sai. File này
dùng `html.parser` của stdlib, không cần `apted`.
"""

from __future__ import annotations

from collections.abc import Sequence
from html.parser import HTMLParser
from typing import ClassVar

from ocr_bench.metrics.base import Metric
from ocr_bench.metrics.matching import NGUONG_MAC_DINH, ghep_toi_uu
from ocr_bench.types import (
    AnnotationGT,
    Box,
    Capability,
    GroundTruth,
    NAReason,
    OcrResult,
    OcrTable,
)

__all__ = [
    "NGUONG_MAC_DINH",
    "dung_luoi",
    "cell_scores",
    "CellF1Metric",
    "TableRecallMetric",
]

_O = ("td", "th")


def _so(gia_tri: str | None) -> int:
    """`rowspan`/`colspan` của engine có thể là `""`, `"0"` hoặc rác. Về 1."""
    try:
        n = int((gia_tri or "1").strip())
    except ValueError:
        return 1
    return n if n >= 1 else 1


class _BoDungLuoi(HTMLParser):
    """Dựng `(hàng, cột) → nội dung` từ một `<table>`.

    Thuật toán chiếm chỗ chuẩn: giữ tập toạ độ đã bị chiếm; mỗi ô mới lấy cột
    trống nhỏ nhất của hàng hiện tại rồi chiếm đủ `rowspan × colspan` ô.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.luoi: dict[tuple[int, int], str] = {}
        self._hang = -1
        self._chiem: set[tuple[int, int]] = set()
        self._trong_o = False
        self._chu: list[str] = []
        self._span = (1, 1)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self._hang += 1
            return
        if tag in _O:
            if self._trong_o:  # thẻ không đóng — chốt ô đang mở trước
                self._dong_o()
            d = dict(attrs)
            self._span = (_so(d.get("rowspan")), _so(d.get("colspan")))
            self._trong_o = True
            self._chu = []

    def handle_data(self, data: str) -> None:
        if self._trong_o:
            self._chu.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in _O and self._trong_o:
            self._dong_o()

    def _dong_o(self) -> None:
        self._trong_o = False
        hang = max(self._hang, 0)
        cot = 0
        while (hang, cot) in self._chiem:
            cot += 1
        # `"  a\n  b "` và `"a b"` là cùng một ô: không chuẩn hoá thì metric đang
        # chấm cách engine xuống dòng HTML chứ không phải nội dung bảng.
        noi_dung = " ".join("".join(self._chu).split())
        r, c = self._span
        for dr in range(r):
            for dc in range(c):
                o = (hang + dr, cot + dc)
                self._chiem.add(o)
                self.luoi[o] = noi_dung


def dung_luoi(html: str) -> dict[tuple[int, int], str]:
    """`<table>` → `{(hàng, cột): nội dung}`, có tính rowspan/colspan."""
    bo = _BoDungLuoi()
    bo.feed(html)
    bo.close()
    if bo._trong_o:  # HTML thiếu thẻ đóng cuối
        bo._dong_o()
    return bo.luoi


def cell_scores(
    nhan: Sequence[str], doan: Sequence[str]
) -> tuple[float, dict[str, object]]:
    """Trả `(f1, chi tiết)`. Bảng ghép theo thứ tự xuất hiện — xem docstring."""
    tp = fp = fn = 0
    n_o_nhan = n_o_doan = 0
    for k in range(max(len(nhan), len(doan))):
        l_nhan = dung_luoi(nhan[k]) if k < len(nhan) else {}
        l_doan = dung_luoi(doan[k]) if k < len(doan) else {}
        n_o_nhan += len(l_nhan)
        n_o_doan += len(l_doan)
        khop = sum(1 for v, noi in l_nhan.items() if l_doan.get(v) == noi)
        tp += khop
        fn += len(l_nhan) - khop
        fp += len(l_doan) - khop

    mau = 2 * tp + fp + fn
    f1 = 2 * tp / mau if mau else 0.0
    return f1, {
        "n_bang_nhan": len(nhan),
        "n_bang_doan": len(doan),
        "n_o_nhan": n_o_nhan,
        "n_o_doan": n_o_doan,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": tp / n_o_doan if n_o_doan else 0.0,
        "recall": tp / n_o_nhan if n_o_nhan else 0.0,
    }


class _BangBase(Metric):
    requires: ClassVar[frozenset[Capability]] = frozenset({Capability.TABLE_HTML})
    gt_kinds: ClassVar[tuple[type, ...]] = (AnnotationGT,)


class CellF1Metric(_BangBase):
    """F1 trên ô bảng theo toạ độ lưới — "ô nào bị mất, ô nào bịa ra"."""

    name: ClassVar[str] = "cell_f1"

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AnnotationGT)
        if not gt.tables and not result.tables:
            # Cùng quyết định 3 của `imgf1.py`: nhãn rỗng mà engine CÓ bảng thì
            # rơi xuống `_compute()` và ăn 0.0.
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "nhãn không có bảng và engine cũng không trả bảng nào"
            }
        return None

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        return cell_scores(
            [b.html for b in gt.tables], [b.html for b in result.tables]
        )


class TableRecallMetric(_BangBase):
    """Tỷ lệ bảng nhãn được engine định vị đúng ở IoU ≥ 0.5.

    Hai nhánh N/A tách riêng — xem docstring module. Engine trả **0 bảng** thì
    không phải N/A: nó đã khai `TABLE_HTML` và đã nói "không có bảng nào", đó là
    một khẳng định sai kiểm chứng được → recall 0.
    """

    name: ClassVar[str] = "table_recall"

    @staticmethod
    def _box(bang: Sequence[OcrTable]) -> list[Box]:
        return [b.box for b in bang if b.box is not None]

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AnnotationGT)
        if not gt.tables or not self._box(gt.tables):
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "nhãn không có khung bảng để đối chiếu",
                "n_bang_nhan": len(gt.tables),
            }
        if result.tables and not self._box(result.tables):
            # Engine trả HTML bảng nhưng không trả khung nào: nó không hứa định vị
            # bảng, và repo không có `Capability.TABLE_BBOX` để nó khai điều đó.
            return NAReason.MISSING_CAPABILITY, {
                "ly_do": "engine trả bảng nhưng không bảng nào có khung",
                "n_bang_doan": len(result.tables),
            }
        return None

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        nhan = self._box(gt.tables)
        doan = self._box(result.tables)
        cap = ghep_toi_uu(nhan, doan, NGUONG_MAC_DINH)
        return len(cap) / len(nhan), {
            "nguong": NGUONG_MAC_DINH,
            "n_nhan": len(nhan),
            "n_doan": len(doan),
            "tp": len(cap),
            "fn": len(nhan) - len(cap),
            "iou_tung_cap": [round(c[2], 6) for c in cap],
        }
