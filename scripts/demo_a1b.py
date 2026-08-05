"""Chạy end-to-end trên một file thật — AC-03 của A1b (TASK-072).

    py -3 scripts/make_sample_pdf.py && py -3 scripts/demo_a1b.py

Ba engine, một metric, một tài liệu thật. Điều cần nhìn ở bảng ra:

* `demo` (engine "tốt", trả đúng nhãn) đứng đầu;
* `sabotage` **thấp hơn hẳn nguồn của nó** — nếu không thì bộ thước sai, không phải
  engine sai. Đây là cổng mà C2 (TASK-086) sẽ dựng thành test tự động;
* `noop` ra **0.000**, không phải N/A: nó *có* khai `TEXT_MD` và trả chuỗi rỗng —
  tức là "đo được, và bằng 0". Ô N/A dành cho trường hợp khác hẳn (engine không khai
  năng lực đó, hoặc thiếu nhãn); đánh đồng hai thứ là cách nhanh nhất bịa ra một
  bảng xếp hạng sai, nên `to_markdown()` in `N/A` chứ không in `0.000`.
  Xem `tests/test_sabotage_and_scorer.py::test_thieu_nang_luc_ra_NA_va_van_co_mat_trong_xep_hang`.

⚠️ Ở A1b chưa có engine OCR thật nào (Marker/OpenDataLoader/pdf-inspector là A4→A7),
nên `demo` không thật sự đọc file — nó dựng sẵn kết quả. Cái được chứng minh ở đây là
*đường ống* chạy thông từ `Path` thật tới bảng xếp hạng, không phải chất lượng OCR.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import ClassVar

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ocr_bench.adapters.base import Adapter
from ocr_bench.adapters.noop import NoopAdapter
from ocr_bench.adapters.sabotage import SabotageAdapter
from ocr_bench.metrics.base import Metric
from ocr_bench.scorer import run_bench
from ocr_bench.types import AnnotationGT, Capability, OcrResult

PDF = Path(__file__).resolve().parent.parent / "pdfs" / "sample_minimal.pdf"

VAN_BAN = (
    "Sovereign OCR bench - sample document\n"
    "Line two of the sample text.\n"
    "Line three, for reading order."
)


class DemoAdapter(Adapter):
    """Engine giả lập trả đúng nội dung file — đóng vai "engine tốt"."""

    name: ClassVar[str] = "demo"
    capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})

    def version(self) -> str:
        return "demo/1"

    def run(self, doc_path: Path) -> OcrResult:
        return OcrResult(
            engine=self.name,
            engine_version=self.version(),
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            text_md=VAN_BAN,
        )


class KhopKyTu(Metric):
    """Tỉ lệ ký tự khớp đúng vị trí. Thô, nhưng đủ để xếp hạng ở A1b.

    CER thật là B1 (TASK-079).
    """

    name = "khop_ky_tu"
    requires = frozenset({Capability.TEXT_MD})
    gt_kinds = (AnnotationGT,)

    def _compute(self, gt, result):
        want, got = gt.text or "", result.text_md or ""
        if not want:
            return 1.0, {}
        khop = sum(1 for a, b in zip(want, got) if a == b)
        return khop / len(want), {"n_ky_tu": len(got)}


def main() -> int:
    if not PDF.exists():
        print(f"Chưa có {PDF}. Chạy: py -3 scripts/make_sample_pdf.py")
        return 1

    bang = run_bench(
        adapters=[DemoAdapter(), NoopAdapter(), SabotageAdapter(DemoAdapter())],
        docs=[PDF],
        metrics=[KhopKyTu()],
        ground_truth={PDF.stem: AnnotationGT(doc_id=PDF.stem, text=VAN_BAN)},
    )

    print(f"Tài liệu: {PDF.name} ({PDF.stat().st_size} bytes)\n")
    print(bang.to_markdown())
    print("\nXếp hạng theo khop_ky_tu:")
    for i, o in enumerate(bang.ranking("khop_ky_tu"), start=1):
        print(f"  {i}. {o.engine:10s} {o.cell()}")

    tot = bang.cell("khop_ky_tu", "demo").penalized_mean
    xau = bang.cell("khop_ky_tu", "sabotage").penalized_mean
    print(f"\nsabotage ({xau:.3f}) < demo ({tot:.3f}): {xau < tot}")
    return 0 if xau < tot else 1


if __name__ == "__main__":
    raise SystemExit(main())
