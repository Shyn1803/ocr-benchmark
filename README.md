# ocr-bench

Đo và xếp hạng công cụ OCR cho Sovereign. Không phải khảo sát — mục tiêu là **số đo**,
và mọi câu trong tài liệu đánh giá cuối cùng phải truy được về `results/` hoặc một
`file:line`.

- Kế hoạch đầy đủ (20 task, 70h, 4 cổng nghiệm thu): [`.claude/context/OCR-BENCHMARK-PLAN.md`](../.claude/context/OCR-BENCHMARK-PLAN.md)
- Backlog đã tạo: **TASK-070 → TASK-089** trong `.claude/tasks/` (A0→D3, đã nối phụ thuộc)
- Vì sao hợp đồng dữ liệu có hình dạng như hiện tại: [`.claude/context/OCR-BENCH-A0-SPIKE.md`](../.claude/context/OCR-BENCH-A0-SPIKE.md)

## Chạy

```bash
py -3 -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev]"
.venv/Scripts/python.exe -m pytest
```

`pytest` phải xanh trên **máy trắng, không cài engine nào**. Engine thật là extra rời
(`.[marker]`, `.[opendataloader]`, `.[pdfinspector]`) vì marker kéo theo torch + model
Surya vài GB và opendataloader cần Java 11+.

## Bốn cái bẫy mà repo này chủ động chặn

Cả bốn đều thuộc loại **không bao giờ ném exception** — chúng chỉ làm bảng xếp hạng sai
một cách rất thuyết phục. Vì thế mỗi cái có test riêng, viết trước cả khi có engine thật.

### 1. Ba engine dùng ba hệ toạ độ khác nhau

| Engine | Gốc | Trục y | Đơn vị |
|---|---|---|---|
| Marker (block bbox) | trên-trái | xuống | PDF point |
| pdf-inspector (`TextItem`) | dưới-trái | **lên** | PDF point |
| OpenDataLoader | chưa rõ — A5 phải đo | chưa rõ | chưa rõ |
| **`Box` của bench** | **trên-trái** | **xuống** | **đã chuẩn hoá [0,1]** |

Trộn nhầm cho IoU thấp trông y hệt "engine tách ảnh kém". Adapter **phải** dùng
`Box.from_absolute(..., y_axis=...)`; dựng `Box` thẳng bằng toạ độ thô sẽ ném lỗi.

⚠️ Đừng giả định page box bắt đầu từ `(0,0)`: nhánh `force_ocr` của Marker lấy page box
từ `pdfium.get_bbox()`. Truyền `page_x0`/`page_y0` vào.

### 2. Số trang 0-based hay 1-based

pdf-inspector trả **0-based** ở `classify_pdf()` và **1-based** ở `process_pdf()` trên
cùng một file. Bench dùng **0-based ở mọi nơi**; `Box(page=-1)` bị chặn.

### 3. Thiếu năng lực ≠ điểm 0

Adapter khai `capabilities` **tĩnh** ở cấp lớp, kiểm ngay lúc `register_adapter()`.
Metric khai `requires`. Engine thiếu năng lực → `MetricResult.value is None` kèm
`na_reason`, **không phải 0.0**.

Phân biệt hai chuyện dễ lẫn:

- khai `IMAGE_BBOX` + `images == ()` → "đã chạy, trang này không có ảnh"
- không khai `IMAGE_BBOX` → "không bao giờ biết được"

Gộp lại là cách nhanh nhất để engine làm ít việc hơn lại trông giỏi hơn.

### 4. Trường số trang của engine có thể sai — đừng tin, hãy đối chiếu

Phát hiện ở A4 (TASK-075) khi chạy thật, **sau khi** 46 test dữ liệu giả đã xanh hết.

`marker-pdf` 1.10.2 tính `FlatBlockOutput.page` bằng `int(block.id.split("/")[-1])` trên
block `Page` (`renderers/chunk.py:json_to_chunks`). Nhưng `BlockId.__str__` in block Page
ra `/page/0/Page/8` — phần tử cuối là **`block_id`**, không phải số trang. Đo trên
`pdfs/sample_minimal.pdf` (đúng 1 trang): `page_info` có khoá `0`, mọi block khai `page=8`.

Hậu quả nếu tin trường đó: không block nào tra được kích thước trang, tất cả bị bỏ, và
Marker — engine mạnh nhất của bench — lên bảng với **0 vùng**. Không có exception nào.

Quy tắc rút ra, áp cho cả A5/A6/A7: **số trang phải đối chiếu được với nguồn thứ hai**
(ở đây là `id` của chính block), và adapter phải có một test *chạy thật* khẳng định
`blocks` không rỗng — test dữ liệu giả không bắt được lớp lỗi này, vì dữ liệu giả là do
chính ta dựng cho khớp.

A4 tìm ra **ba** lỗi cùng lớp này, cả ba sau khi 46 test dữ liệu giả đã xanh:

| # | Triệu chứng nếu tin engine | Loại |
|---|---|---|
| `FlatBlockOutput.page` sai | Marker lên bảng với **0 vùng** | số sai |
| khoá `images` là `BlockId`, không phải `str` | `json.dumps` nổ ở tài liệu thứ 4 | kiểu sai |
| `section_hierarchy` chứa `BlockId`, không chứa chữ | metric cấp mục ra **0 cho mọi block** | nội dung sai |

Nên trước khi tin bất kỳ trường nào của engine, **kiểm kiểu và kiểm nội dung**, đừng chỉ
kiểm "có giá trị". Ba lỗi trên đều có giá trị, đúng cấu trúc, và sai.

## Vì sao `aggregate()` trả về một đối tượng chứ không trả về một số

`opendataloader-bench` loại tài liệu engine làm hỏng ra khỏi trung bình — tức là
**thưởng cho engine hỏng nhiều hơn**. Ở đây `mean`, `penalized_mean` (hỏng = 0 điểm) và
`fail_rate` nằm trong cùng một `Aggregate`, nên không thể lỡ tay in trung bình mà quên
tỉ lệ hỏng.

## Bố cục

```
src/ocr_bench/
├── types.py        hợp đồng dữ liệu — mọi quyết định của A0 nằm ở đây
├── normalize.py    NFC + gộp khoảng trắng; mọi metric text phải đi qua
├── registry.py     đăng ký adapter/metric, kiểm ngay lúc import
├── adapters/       base.py · noop.py  (sabotage → A1b, engine thật → A4-A7)
└── metrics/        base.py            (cer/teds/imgf1/nid/heading → nhóm B)

pdfs/ ground-truth/ prediction/ results/ history/ charts/
```

`prediction/` **được commit**: chấm lại không cần chạy lại OCR — đó là cả điểm của A2,
và Marker tốn ~3h cho 200 trang trên CPU.

## Trạng thái

| Task | Trạng thái |
|---|---|
| A0 — khảo sát đầu ra 3 công cụ | xong |
| A1a — repo + hợp đồng dữ liệu + `noop` | xong — coverage 100% |
| A1b — `sabotage` + `scorer.py` | xong |
| A2 — lưu/nạp `prediction/` | xong |
| A3 — bộ mẫu + ground truth | xong |
| **A4 — bộ nối Marker** | **xong** — 63 test, coverage 100%, 20 tài liệu DocLayNet |
| A5 — bộ nối OpenDataLoader | chưa |
| A6 — bộ nối pdf-inspector | chưa |
| A7 — bộ nối pipeline BE Sovereign | chưa |

## Cảnh báo dữ liệu

Bộ mẫu hiện tại là dữ liệu công khai. **Nếu** về sau đưa tài liệu thật của khách vào,
phải cho `pdfs/` của phần đó vào `.gitignore` và chỉ commit `manifest.yaml` + checksum.
Đưa tài liệu khách vào repo là rủi ro rò rỉ.

OmniDocBench là **research-only, cấm thương mại** — không đặt file của nó vào repo này.
