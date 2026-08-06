"""B3 — tách ảnh: `img_f1` và `img_iou`.

Bốn quyết định của file này, ghi tại chỗ để người sau không phải đọc lại task:

1. **Ngưỡng IoU = 0.5, và nó nằm trong `detail`, không chôn trong code.** Chọn 0.5
   không phải vì quen: ở IoU > 0.5 một box đoán **không thể** khớp hai box nhãn
   rời nhau cùng lúc (hai box nhãn rời nhau thì tổng diện tích giao với một box
   đoán không vượt quá diện tích box đó, nên không thể cả hai cùng > 0.5). Phép
   ghép vì thế là **duy nhất**, và ghép tham lam cho đúng kết quả tối ưu. Khẳng
   định này có test đối chiếu với vét cạn, không chỉ nằm ở đây.

2. **Hai cột chứ không một.** `img_f1` trả lời "tìm đúng bao nhiêu ảnh",
   `img_iou` trả lời "khung có sát không". `img_f1` cao mà `img_iou` thấp nghĩa
   là đếm đúng nhưng cắt lệch — gộp một số là mất đúng chẩn đoán đó.

3. **Nhãn 0 ảnh + engine 0 box = N/A, nhưng nhãn 0 ảnh + engine có box = 0.0.**
   Cùng một nhãn rỗng, hai kết quả, và đó là chủ ý. 141/204 tài liệu DocLayNet
   không có ảnh nào; chấm 1.0 cho ca đầu là rót điểm miễn phí vào 69% bảng và
   chôn mất chênh lệch ở phần còn lại. Ca sau thì engine **đã** nói sai một điều
   kiểm chứng được — dương tính giả là lỗi thật, phải phạt.

4. **File này không biết `Picture`, `Figure`, `PictureGroup` là gì.** Bốn tên đó
   là từ vựng của Marker và đã được quy về `BlockType.PICTURE` ngay tại
   `adapters/marker.py`; OpenDataLoader gọi là `"image"`, DocLayNet gọi là
   `"Picture"`. Docstring của `BlockType` chốt: metric không được biết những tên
   đó tồn tại. Metric chỉ so `AnnotationGT.images` với `OcrResult.images`.
"""

from __future__ import annotations

from typing import ClassVar

from ocr_bench.metrics.base import Metric
from ocr_bench.types import (
    AnnotationGT,
    Box,
    Capability,
    GroundTruth,
    NAReason,
    OcrResult,
)

__all__ = [
    "NGUONG_MAC_DINH",
    "ghep_cap",
    "img_scores",
    "ImgF1Metric",
    "ImgIouMetric",
]

NGUONG_MAC_DINH = 0.5
"""Ngưỡng IoU coi là "cùng một ảnh". Xem quyết định 1 ở docstring module."""


def ghep_cap(
    nhan: list[Box], doan: list[Box], nguong: float = NGUONG_MAC_DINH
) -> list[tuple[int, int, float]]:
    """Ghép nhãn với đoán, tham lam theo IoU giảm dần. Mỗi box dùng đúng một lần.

    Trả danh sách `(chỉ số nhãn, chỉ số đoán, iou)` đã sắp theo chỉ số nhãn — sắp
    lại để đầu ra ổn định, vì thứ tự tham lam phụ thuộc IoU chứ không phụ thuộc
    thứ tự đầu vào và `detail` bị so trong test.

    Ở `nguong > 0.5` kết quả này **là** phép ghép tối ưu (xem quyết định 1). Dưới
    0.5 thì tham lam chỉ là xấp xỉ — không dùng ngưỡng dưới 0.5 mà không đọc lại
    chỗ này.
    """
    cap: list[tuple[float, int, int]] = []
    for i, a in enumerate(nhan):
        for j, b in enumerate(doan):
            iou = a.iou(b)
            if iou >= nguong and iou > 0.0:
                cap.append((iou, i, j))
    # Khoá phụ `(i, j)` để hai cặp cùng IoU không đổi thứ tự theo tâm trạng của
    # `sort` — kết quả phải tái lập được giữa các lần chạy.
    cap.sort(key=lambda t: (-t[0], t[1], t[2]))

    da_nhan: set[int] = set()
    da_doan: set[int] = set()
    ra: list[tuple[int, int, float]] = []
    for iou, i, j in cap:
        if i in da_nhan or j in da_doan:
            continue
        da_nhan.add(i)
        da_doan.add(j)
        ra.append((i, j, iou))
    ra.sort()
    return ra


def img_scores(
    nhan: list[Box], doan: list[Box], nguong: float = NGUONG_MAC_DINH
) -> tuple[float, float, dict[str, object]]:
    """Trả `(f1, chất lượng IoU, chi tiết)`.

    `chất lượng IoU` = tổng IoU của các cặp khớp chia cho `TP + FP + FN`, tức
    box thừa và box thiếu đều bị tính vào mẫu số. Không lấy trung bình IoU của
    riêng các cặp khớp: engine chỉ xuất một ảnh duy nhất mà nó tự tin sẽ được
    1.0, đúng cái kiểu thưởng nhầm mà repo này tồn tại để chặn.
    """
    cap = ghep_cap(nhan, doan, nguong)
    tp = len(cap)
    fp = len(doan) - tp
    fn = len(nhan) - tp

    precision = tp / len(doan) if doan else 0.0
    recall = tp / len(nhan) if nhan else 0.0
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
            # Báo riêng, không chỉ F1: 319 box của opendataloader so với 121 nhãn
            # là thừa hay thiếu — F1 gộp lại thì không đọc ra được.
            "precision": precision,
            "recall": recall,
            "iou_tung_cap": [round(c[2], 6) for c in cap],
        },
    )


class _ImgBase(Metric):
    """Phần dùng chung: cùng cổng, cùng phép ghép, khác chỗ lấy số nào ra."""

    requires: ClassVar[frozenset[Capability]] = frozenset({Capability.IMAGE_BBOX})
    gt_kinds: ClassVar[tuple[type, ...]] = (AnnotationGT,)
    nguong: ClassVar[float] = NGUONG_MAC_DINH

    @staticmethod
    def _box_doan(result: OcrResult) -> list[Box]:
        """Box của engine. `OcrImage.box` được phép `None` (adapter có bytes ảnh
        nhưng không có toạ độ) — ảnh không có khung thì không ghép được, bỏ."""
        return [i.box for i in result.images if i.box is not None]

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AnnotationGT)  # gt_kinds đã lọc
        if not gt.images and not self._box_doan(result):
            # Quyết định 3: hai bên cùng rỗng là "không có gì để đo", không phải
            # "engine làm đúng". Nhãn rỗng mà engine CÓ box thì rơi xuống
            # `_compute()` và ăn 0.0 — dương tính giả vẫn bị phạt.
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "nhãn không có ảnh và engine cũng không trả box nào"
            }
        return None

    def _lay(self, f1: float, chat_luong: float) -> float:
        raise NotImplementedError  # pragma: no cover

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        # Engine ĐÃ khai IMAGE_BBOX mà không trả box nào là lỗi của engine, không
        # phải thiếu năng lực — cổng ở `score()` đã cho qua. Chấm 0, không N/A.
        f1, chat_luong, chi_tiet = img_scores(
            list(gt.images), self._box_doan(result), self.nguong
        )
        return self._lay(f1, chat_luong), chi_tiet


class ImgF1Metric(_ImgBase):
    """F1 của phép ghép ảnh ở IoU ≥ ngưỡng — "tìm đúng bao nhiêu ảnh"."""

    name: ClassVar[str] = "img_f1"

    def _lay(self, f1: float, chat_luong: float) -> float:
        return f1


class ImgIouMetric(_ImgBase):
    """Chất lượng khung — "tìm ra rồi thì cắt có sát không".

    Đọc cùng `img_f1`: bằng nhau ở mức cao là khung sát; `img_f1` cao mà cột này
    thấp là đếm đúng nhưng khung lệch.
    """

    name: ClassVar[str] = "img_iou"

    def _lay(self, f1: float, chat_luong: float) -> float:
        return chat_luong
