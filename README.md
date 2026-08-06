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
| OpenDataLoader | dưới-trái | **lên** | PDF point |
| **`Box` của bench** | **trên-trái** | **xuống** | **đã chuẩn hoá [0,1]** |

Trộn nhầm cho IoU thấp trông y hệt "engine tách ảnh kém". Adapter **phải** dùng
`Box.from_absolute(..., y_axis=...)`; dựng `Box` thẳng bằng toạ độ thô sẽ ném lỗi.

⚠️ Đừng giả định page box bắt đầu từ `(0,0)`: nhánh `force_ocr` của Marker lấy page box
từ `pdfium.get_bbox()`. Truyền `page_x0`/`page_y0` vào.

⚠️ **Nhưng cũng đừng truyền nó cho mọi engine.** OpenDataLoader **đã tự trừ gốc
MediaBox** — chép quy tắc trên từ Marker sang là trừ hai lần, và mọi box lệch đúng
một lượng cố định trên mọi tài liệu có MediaBox không bắt đầu từ gốc. Đây là loại
lỗi không có triệu chứng: IoU vẫn ra số, bảng vẫn xếp hạng, chỉ là sai.

Hàng OpenDataLoader ở trên **đo** bằng `scripts/measure_opendataloader_coords.py`
(A5, TASK-076), không suy từ tài liệu. Script dựng PDF có chữ đặt ở toạ độ biết
trước rồi đối chiếu box engine trả về:

```
1) TOPLEFT  = [50.0, 777.3, 104.012, 791.172]
   BOTRIGHT = [400.0, 37.3, 462.004, 51.172]
   → chữ ở mép TRÊN có y LỚN hơn ⇒ gốc DƯỚI-TRÁI, trục y hướng LÊN
2) x lớn nhất 462.00 ≤ chiều rộng trang 595.0        ⇒ đơn vị ĐIỂM PDF
3) box[2]-box[0] = 54.01 pt                          ⇒ thứ tự [x0, y0, x1, y1]
4) MediaBox dịch (100, 200) → Δx=+0.00 Δy=+0.00      ⇒ đã trừ gốc MediaBox
```

Hai điều nữa cần biết trước khi đọc điểm của engine này:

- **JSON của nó không có kích thước trang.** Đã kiểm mọi node của 24 tài liệu.
  Nguồn duy nhất là MediaBox đọc bằng `pypdf` — nên `pypdf` nằm trong extra
  `opendataloader`, dù engine không phụ thuộc nó.
- **`page number` là 1-indexed** (bench 0-based ở mọi nơi — xem mục 2). Adapter
  trừ 1 ngay ở biên; số ngoài khoảng thì **bỏ block và ghi `error`**, không rơi về
  trang 0.

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

### 5. Mặc định của engine có thể tắt hẳn một năng lực

Phát hiện ở A5 (TASK-076). OpenDataLoader nhận `table_method` với mặc định `default`
(dò bảng theo đường kẻ). Ở chế độ đó, trên **4 tài liệu DocLayNet nhiều bảng nhất**
(ground truth 5, 4, 4, 3 bảng), engine trả về **0** node `table`. Đổi sang `cluster`
thì ra bảng đủ `rows`/`cells`/`row span`/`column span`.

Nếu chạy bằng mặc định rồi công bố, OpenDataLoader sẽ có TEDS ≈ 0 và kết luận sẽ là
"engine này không đọc được bảng" — trong khi sự thật là "bench gọi sai cờ". Nên:

- adapter đặt `table_method="cluster"`, và
- `table_method` nằm trong `config_fingerprint()`, để bảng điểm luôn nói rõ đã chạy
  chế độ nào.

Đo thêm, và báo đúng như đã đo: `include_header_footer` **không đổi gì** trên bộ mẫu
này — bật/tắt cho ra số node y hệt nhau trên 8 tài liệu. Vẫn để `True` cho an toàn về
recall, nhưng đó là phòng xa, không phải một cải thiện đã chứng minh.

Điểm bảng của engine này vẫn yếu ngay cả ở `cluster` (tài liệu được gán nhãn 5 bảng
→ engine tìm ra 0). Đó là **kết quả chất lượng**, không phải lỗi bộ nối: đường bảng
đã được chứng minh chạy thông từ đầu tới cuối trên tài liệu khác.

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

⚠️ **Nhưng chỉ commit phần chấm được.** Prediction của bộ `olmocr` **không** vào repo:
bộ đó chưa có ground truth (`ground-truth/` chỉ phủ `doclaynet` + `sample`), nên 1.4 GB
ảnh tách ra từ 1403 tài liệu hiện không có metric nào chấm nổi. Đã chạy thật, **hỏng 0**,
số liệu ghi ở `.claude/tasks/TASK-076/review.md`; sinh lại mất ~31 phút:

```bash
.venv-odl/Scripts/python.exe scripts/make_predictions.py \
    --engines opendataloader --corpus olmocr --out prediction-local
```

`--out prediction-local/` chứ không ghi thẳng vào `prediction/`: `prediction-local/` nằm
trong `.gitignore`, nên lần sau `git add -A` không lỡ tay kéo 1.4 GB vào lịch sử nữa.
Tên tài liệu olmocr không có tiền tố chung nên không viết được glob lọc theo bộ — tách
thư mục là cách chặn duy nhất chắc chắn.

Và **đừng xoá `*.images/` mà giữ lại `*.json`** để tiết kiệm chỗ: `_image_from_json()`
(`src/ocr_bench/prediction.py`) băm SHA-256 từng file ảnh và ném `PredictionSchemaError`
khi thiếu — bỏ ảnh là bỏ cả `.json` đi kèm, hoặc sinh lại cả hai.

## Trạng thái

| Task | Trạng thái |
|---|---|
| A0 — khảo sát đầu ra 3 công cụ | xong |
| A1a — repo + hợp đồng dữ liệu + `noop` | xong — coverage 100% |
| A1b — `sabotage` + `scorer.py` | xong |
| A2 — lưu/nạp `prediction/` | xong |
| A3 — bộ mẫu + ground truth | xong |
| **A4 — bộ nối Marker** | **xong** — 63 test, coverage 100%, 20 tài liệu DocLayNet |
| **A5 — bộ nối OpenDataLoader** | **xong** — 49 test, coverage 91%, 1608 tài liệu, hỏng 0 |
| A6 — bộ nối pdf-inspector | chưa |
| A7 — bộ nối pipeline BE Sovereign | chưa |

## Cảnh báo dữ liệu

Bộ mẫu hiện tại là dữ liệu công khai. **Nếu** về sau đưa tài liệu thật của khách vào,
phải cho `pdfs/` của phần đó vào `.gitignore` và chỉ commit `manifest.yaml` + checksum.
Đưa tài liệu khách vào repo là rủi ro rò rỉ.

OmniDocBench là **research-only, cấm thương mại** — không đặt file của nó vào repo này.
