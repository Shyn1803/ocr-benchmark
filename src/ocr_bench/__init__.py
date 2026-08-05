"""ocr-bench — đo và xếp hạng công cụ OCR cho Sovereign.

Xem `.claude/context/OCR-BENCHMARK-PLAN.md` (kế hoạch) và
`.claude/context/OCR-BENCH-A0-SPIKE.md` (hợp đồng dữ liệu được quyết ra sao).
"""

from __future__ import annotations

__version__ = "0.1.0"

from ocr_bench import registry
from ocr_bench.adapters.marker import MarkerAdapter
from ocr_bench.adapters.noop import NoopAdapter
from ocr_bench.adapters.sabotage import SabotageAdapter

# Hai engine giả đăng ký sẵn. Chúng không đo engine nào cả — chúng đo *bộ thước*:
# `noop` không làm gì, `sabotage` làm hỏng đầu ra engine khác, và cả hai phải đứng
# bét mọi metric. Metric nào không xếp được như vậy thì metric đó sai (cổng C2).
registry.register_adapter(NoopAdapter)
registry.register_adapter(SabotageAdapter)

# Engine thật đầu tiên (A4). Module `adapters.marker` KHÔNG import marker ở đầu file —
# import ở trong hàm — nên dòng dưới chạy được trên máy chưa cài marker-pdf; chỉ
# `MarkerAdapter.run()` mới đòi.
registry.register_adapter(MarkerAdapter)

__all__ = ["__version__", "registry"]
