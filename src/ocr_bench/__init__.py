"""ocr-bench — đo và xếp hạng công cụ OCR cho Sovereign.

Xem `.claude/context/OCR-BENCHMARK-PLAN.md` (kế hoạch) và
`.claude/context/OCR-BENCH-A0-SPIKE.md` (hợp đồng dữ liệu được quyết ra sao).
"""

from __future__ import annotations

__version__ = "0.1.0"

from ocr_bench import registry
from ocr_bench.adapters.noop import NoopAdapter

registry.register_adapter(NoopAdapter)

__all__ = ["__version__", "registry"]
