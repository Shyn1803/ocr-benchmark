"""Engine giả `noop` — trả chuỗi rỗng.

Không phải để so sánh. Nó là **thước kiểm tra chính bộ thước**: một engine không làm
gì phải đứng bét mọi metric. Nếu nó không đứng bét ở đâu đó, metric đó sai.

`noop` khai `TEXT_MD` vì nó **có** trả text (rỗng cũng là text). Đây là khác biệt cốt
lõi so với việc khai `frozenset()`: khai rỗng thì mọi metric trả N/A và `noop` biến
mất khỏi bảng thay vì đứng bét — đúng cái nó sinh ra để phát hiện.
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
