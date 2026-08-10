"""Engine giả `noop` — trả chuỗi rỗng.

Không phải để so sánh. Nó là **thước kiểm tra chính bộ thước**: một engine không làm
gì thì không được chấm cao.

⚠️ Phát biểu cũ — *"`noop` phải đứng bét mọi metric; chỗ nào nó không đứng bét thì
metric đó sai"* — **đã bị bác** ở **D-010** (`.claude/context/DECISIONS.md`,
2026-08-10). Lý do: `noop` là sàn **theo cấu tạo**, nên nó đứng bét là điều hiển
nhiên, không chứng minh được gì về thước đo; và ngược lại, "không đứng bét" cũng
không kết tội được thước đo nào. Vì vậy cổng C2 **loại `noop`** khỏi tập so sánh
(`bo_qua = ENGINE_TONG_HOP - {ten_sabotage}`). Điều kiện đạt cổng bây giờ là
`sabotage` thấp hơn **chính engine nguồn** của nó, so ngặt — xem `discrimination.py`.

`noop` khai `TEXT_MD` vì nó **có** trả text (rỗng cũng là text). Đây là khác biệt cốt
lõi so với việc khai `frozenset()`: khai rỗng thì mọi metric trả N/A và `noop` biến
mất khỏi bảng thay vì bị chấm điểm sàn — đúng cái nó sinh ra để phát hiện.
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from ocr_bench.adapters.base import Adapter
from ocr_bench.types import Capability, OcrResult

__all__ = ["NoopAdapter"]


class NoopAdapter(Adapter):
    name: ClassVar[str] = "noop"
    capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})

    def version(self) -> str:
        return "1"

    def run(self, doc_path: Path) -> OcrResult:
        return OcrResult(
            engine=self.name,
            engine_version=self.version(),
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            text_md="",
        )
