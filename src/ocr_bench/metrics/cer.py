"""Độ chính xác chữ: CER và WER — B1 (TASK-079).

Hai thước đo nền. Mọi thước khác đo *cấu trúc*; hai cái này đo **nội dung đọc ra
có đúng không**, nên chúng là thứ đầu tiên bị nhìn khi một engine tụt hạng.

Ba quyết định ở file này, mỗi cái chặn một cách chấm sai:

1. **Chuẩn hoá trước khi so.** `normalize_text()` đưa cả hai vế về NFC. Không có
   bước này, "ề" dạng 1 code point và dạng 3 code point cho CER > 0 dù màn hình
   hiện y hệt nhau — và con số chênh đó không nói gì về chất lượng OCR. Với tiếng
   Việt (giai đoạn 2) đây không phải trường hợp hiếm mà là mặc định.

2. **Trả `1 - err`, và kẹp về [0,1].** `jiwer.cer("ab", "abcdefghij")` trả **4.0**:
   tỉ lệ lỗi chia cho độ dài *nhãn*, nên chèn thừa đẩy nó vượt 1 không giới hạn.
   `1 - 4.0 = -3.0` sẽ làm `Metric.score()` ném. Engine nói nhảm gấp năm lần và
   engine nói nhảm gấp năm mươi lần đều đáng 0 điểm — dưới 0 không có nghĩa gì.

3. **Nhãn không có chữ ⇒ N/A, không phải 0.** `AnnotationGT.text` được phép `None`
   (tài liệu chỉ có nhãn bố cục). `jiwer` không ném với nhãn rỗng — nó trả `3` cho
   `cer("", "abc")` — nên nếu không tự chặn thì ta sẽ lặng lẽ chấm 0 cho một engine
   hoàn toàn có thể đang đúng, chỉ vì *nhãn* thiếu.

CER hay WER quan trọng hơn thì tuỳ câu hỏi: WER phạt nặng lỗi dính/tách từ (đúng
thứ layout PDF hay gây ra), CER thấy được lỗi một ký tự mà WER làm tròn thành cả
từ sai. Giữ cả hai, không gộp thành một số.
"""

from __future__ import annotations

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

__all__ = ["CerMetric", "WerMetric"]


def _kep(err: float) -> float:
    """`1 - err`, kẹp về [0,1]. Xem quyết định 2 ở đầu file."""
    return max(0.0, min(1.0, 1.0 - err))


class _TextMetric(Metric):
    """Phần dùng chung của CER và WER: cùng cổng, cùng chuẩn hoá, khác hàm lỗi."""

    requires: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})
    gt_kinds: ClassVar[tuple[type, ...]] = (AnnotationGT,)

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AnnotationGT)  # gt_kinds đã lọc
        if not normalize_text(gt.text or ""):
            return NAReason.NO_GROUND_TRUTH, {"ly_do": "nhãn không có chữ để so"}
        return None

    def _doi(self, ref: str, hyp: str) -> float:
        """Tỉ lệ lỗi thô của jiwer. Subclass cài."""
        raise NotImplementedError  # pragma: no cover

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        ref = normalize_text(gt.text or "")
        # `text_md=None` trong khi engine ĐÃ khai TEXT_MD là lỗi của engine, không
        # phải thiếu năng lực — cổng năng lực ở `score()` đã cho qua. Chấm 0, không N/A.
        hyp = normalize_text(result.text_md or "")

        err = float(self._doi(ref, hyp))
        return _kep(err), {
            "err": err,
            "bi_kep": err > 1.0,
            "len_ref": len(ref),
            "len_hyp": len(hyp),
        }


class CerMetric(_TextMetric):
    """1 − tỉ lệ lỗi ký tự."""

    name: ClassVar[str] = "cer"

    def _doi(self, ref: str, hyp: str) -> float:
        import jiwer  # nhập lười: `jiwer` là extra `metrics`, không phải dep lõi

        return jiwer.cer(ref, hyp)


class WerMetric(_TextMetric):
    """1 − tỉ lệ lỗi từ.

    Tách từ theo khoảng trắng — đó là mặc định của `jiwer`, và `normalize_text()`
    đã gộp mọi khoảng trắng ngang về một dấu cách nên hai vế được tách như nhau.
    """

    name: ClassVar[str] = "wer"

    def _doi(self, ref: str, hyp: str) -> float:
        import jiwer

        return jiwer.wer(ref, hyp)
