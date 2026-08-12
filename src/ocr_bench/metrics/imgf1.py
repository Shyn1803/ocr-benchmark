"""B3 — tách ảnh: `img_f1` và `img_iou`.

Bốn quyết định của file này, ghi tại chỗ để người sau không phải đọc lại task:

1. **Ngưỡng IoU = 0.5, và nó nằm trong `detail`, không chôn trong code.** Chọn 0.5
   không phải vì quen: ở IoU > 0.5 một box đoán **không thể** khớp hai box nhãn
   rời nhau cùng lúc (hai box nhãn rời nhau thì tổng diện tích giao với một box
   đoán không vượt quá diện tích box đó, nên không thể cả hai cùng > 0.5). Phép
   ghép vì thế là **duy nhất**, và ghép tham lam cho đúng kết quả tối ưu. Khẳng
   định này có test đối chiếu với vét cạn, không chỉ nằm ở đây.

   Tiền đề "box nhãn rời nhau" đúng với **ảnh**, không đúng với **khối** (caption
   nằm trong picture). Nên từ Task 8 file này gọi thẳng `ghep_toi_uu()` của
   `metrics/matching.py` thay vì giữ một bản tham lam riêng: cùng kết quả ở nơi
   tiền đề đúng, đúng kết quả ở nơi tiền đề sai, và chỉ còn **một** phép ghép
   trong repo để kiểm.

   Đổi phép ghép **không** đổi số nào đã commit — đo trực tiếp trên corpus, không
   suy luận: 266 cặp (engine, tài liệu) có box ảnh và 854 cặp có box khối,
   tham lam và tối ưu cho `f1` lẫn `chất lượng IoU` **giống hệt** trên toàn bộ.
   Vì thế không cần tên metric versioned: `img_f1`/`img_iou` giữ nguyên ý nghĩa
   lịch sử.

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
from ocr_bench.metrics.matching import NGUONG_MAC_DINH, ghep_toi_uu
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

def ghep_cap(
    nhan: list[Box], doan: list[Box], nguong: float = NGUONG_MAC_DINH
) -> list[tuple[int, int, float]]:
    """Ghép nhãn với đoán 1-1: **nhiều cặp trước, tổng IoU sau**.

    Trả `(chỉ số nhãn, chỉ số đoán, iou)` đã sắp theo chỉ số nhãn.

    Tên này giữ lại vì nó là API cũ của file; phần việc nằm ở `ghep_toi_uu()`
    của `metrics/matching.py`. Trước Task 8 đây là một bản ghép tham lam riêng —
    xem quyết định 1 để biết vì sao đổi và vì sao không số nào đã commit thay đổi.
    """
    return ghep_toi_uu(nhan, doan, nguong)


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
