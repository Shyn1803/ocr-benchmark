"""ocr-bench — đo và xếp hạng công cụ OCR cho Sovereign.

Xem `.claude/context/OCR-BENCHMARK-PLAN.md` (kế hoạch) và
`.claude/context/OCR-BENCH-A0-SPIKE.md` (hợp đồng dữ liệu được quyết ra sao).
"""

from __future__ import annotations

__version__ = "0.1.0"

from ocr_bench import registry
from ocr_bench.adapters.marker import MarkerAdapter
from ocr_bench.adapters.noop import NoopAdapter
from ocr_bench.adapters.opendataloader import OpenDataLoaderAdapter
from ocr_bench.adapters.pdf_inspector import PdfInspectorAdapter
from ocr_bench.adapters.sabotage import SabotageAdapter
from ocr_bench.adapters.sovereign import SovereignAdapter
from ocr_bench.metrics.assertions import (
    BaselineMetric,
    MathPresenceMetric,
    ReadingOrderMetric,
    TableRelationMetric,
    TextAbsenceMetric,
    TextPresenceMetric,
)
from ocr_bench.metrics.cer import CerMetric, WerMetric
from ocr_bench.metrics.heading import HeadingMetric
from ocr_bench.metrics.imgf1 import ImgF1Metric, ImgIouMetric
from ocr_bench.metrics.nid import NidMetric
from ocr_bench.metrics.teds import TedsMetric, TedsStructMetric

# Hai engine giả đăng ký sẵn. Chúng không đo engine nào cả — chúng đo *bộ thước*:
# `noop` không làm gì, `sabotage` làm hỏng đầu ra engine khác, và cả hai phải đứng
# bét mọi metric. Metric nào không xếp được như vậy thì metric đó sai (cổng C2).
registry.register_adapter(NoopAdapter)
registry.register_adapter(SabotageAdapter)

# Engine thật đầu tiên (A4). Module `adapters.marker` KHÔNG import marker ở đầu file —
# import ở trong hàm — nên dòng dưới chạy được trên máy chưa cài marker-pdf; chỉ
# `MarkerAdapter.run()` mới đòi.
registry.register_adapter(MarkerAdapter)

# A5 — cùng kỷ luật import lười; `adapters.opendataloader` không import
# `opendataloader_pdf` (và không đụng tới Java) cho tới khi `run()` được gọi.
registry.register_adapter(OpenDataLoaderAdapter)

# A6 — engine duy nhất tới giờ khai `SCAN_LABEL`. Cũng import lười: `pdf_inspector`
# và `pypdf` đều là extra.
registry.register_adapter(PdfInspectorAdapter)

# A7 — baseline: pipeline BE hiện tại. Import lười triệt để hơn cả ba cái trên, vì
# import BE *sớm* là nguy hiểm chứ không chỉ nặng: `app/config.py` ghim `.env` của BE
# theo đường dẫn, mà `.env` đó bật `OCR_USE_VISION_API=true` kèm khoá API thật. Module
# `adapters.sovereign` không đụng `sys.path` cho tới khi `run()` được gọi, và khi gọi
# thì cưỡng bức `os.environ` TRƯỚC rồi mới import.
registry.register_adapter(SovereignAdapter)

# B1 — hai thước đo nền. `jiwer` là extra `metrics` và cũng được import lười (trong
# `_doi()`), nên đăng ký ở đây không đòi máy phải cài nó.
registry.register_metric(CerMetric)
registry.register_metric(WerMetric)

# B2 — bảng. Hai cột chứ không một: chênh lệch giữa `teds` và `teds_struct` là thứ
# duy nhất phân biệt "dựng đúng lưới nhưng đọc sai chữ" với "mất luôn cấu trúc".
# `apted`/`rapidfuzz` cũng nhập lười, cùng lý do với B1.
registry.register_metric(TedsMetric)
registry.register_metric(TedsStructMetric)

# B3 — ảnh. Cũng hai cột: `img_f1` đếm ảnh tìm đúng, `img_iou` đo khung có sát
# không. Không có phụ thuộc ngoài — `Box.iou()` là số học thuần.
registry.register_metric(ImgF1Metric)
registry.register_metric(ImgIouMetric)

# B4 — thứ tự đọc + phân cấp tiêu đề. `nid` ra N/A trên toàn bộ mẫu hiện tại vì
# DocLayNet KHÔNG có nhãn thứ tự đọc (thứ tự `annotation.id` là thứ tự vẽ box, đo
# trên tài liệu một cột vẫn lệch 10%) — xem `AnnotationGT.reading_order` và
# TASK-082 plan §0. Đăng ký vẫn đúng: metric sẵn sàng cho lúc có nhãn, và N/A là
# câu trả lời trung thực chứ không phải lỗ hổng.
registry.register_metric(NidMetric)
registry.register_metric(HeadingMetric)

# B5 — bộ khẳng định olmOCR. **Sáu** metric riêng biệt chứ không một metric sáu chế độ:
# `Metric.score()` trả đúng một `value`, nên gộp sáu loại vào một lớp là *buộc* phải
# gộp sáu loại vào một con số — đúng cái AC-02 của TASK-083 cấm. Muốn có số gộp thì
# phải viết thêm lớp mới, tức là phải cố ý. `rapidfuzz` nhập lười như B1/B2.
registry.register_metric(TextPresenceMetric)
registry.register_metric(TextAbsenceMetric)
registry.register_metric(ReadingOrderMetric)
registry.register_metric(MathPresenceMetric)
registry.register_metric(TableRelationMetric)
registry.register_metric(BaselineMetric)

__all__ = ["__version__", "registry"]
