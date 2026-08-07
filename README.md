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

Thêm `.[perf]` (`psutil`) trước khi lấy số bộ nhớ để công bố. Thiếu nó thì cột RSS hiện
`—` chứ không hiện 0, nhưng engine gọi tiến trình con sẽ **không đo được** — xem bẫy 13.

## Mười ba cái bẫy mà repo này chủ động chặn

Bảy cái đầu thuộc loại **không bao giờ ném exception** — chúng chỉ làm bảng xếp hạng sai
một cách rất thuyết phục. Cái thứ 8 và cái thứ 9 mỗi cái có một nửa ném được, và nửa ném
được luôn dễ chịu hơn nửa im lặng. Cái thứ 10 thì không ném gì cả: nó ra **một con số
trông dùng được**. Hai cái tiếp (B5) tệ hơn nữa — chúng ra con số dùng được *và* con số
đó lệch **có hệ thống theo một hướng biết trước**. Cái thứ 13 (B6) cũng vậy, nhưng lệch
theo *thứ tự chạy*. Vì thế mỗi cái có test riêng, viết trước cả khi có engine thật.

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

⚠️ **Và quy tắc đó không suy được từ engine hàng xóm.** pdf-inspector **không** trừ
gốc MediaBox: dịch MediaBox đi (100, 200) làm mọi toạ độ dịch đúng (+100, +200).
Nên adapter của nó **phải** truyền `page_x0`/`page_y0` — ngược hẳn OpenDataLoader,
dù hai engine có cùng gốc và cùng chiều trục y. Chép quy tắc giữa hai bộ nối liền kề
là cách nhanh nhất để sai câm.

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

Bench dùng **0-based ở mọi nơi**; `Box(page=-1)` bị chặn.

pdf-inspector 0.2.6 dùng **ba** quy ước, và **hai trong số đó nằm trong cùng một object
trả về** (đo ở A6, TASK-077):

| Trường | Quy ước |
|---|---|
| `classify_pdf().pages_needing_ocr` | 0-based |
| `PagesExtractionResult.pages[i].page` | 0-based |
| `PagesExtractionResult.pages_needing_ocr` | **1-based** ← cùng object với hàng trên |
| `TextItem.page` (`extract_text_with_positions`) | **1-based** |

Nên adapter chuẩn hoá **từng trường một**, và lấy số trang cần OCR từ
`PageMarkdown.page`, **không** từ `pages_needing_ocr` nằm ngay cạnh nó. Lấy nhầm thì
lệch đúng một trang: không exception, không triệu chứng.

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

### 6. Hộp diện tích 0, và hai API của **cùng một thư viện** cãi nhau

Cả hai phát hiện ở A6 (TASK-077), engine `pdf_inspector`.

**(a) `TextItem.width == 0.0` ở 370/971 item (38%) — và nó dồn cục.** Không rải đều:
một tài liệu chiếm 93% (`12c38f48a5bf`, n=396), một tài liệu 1%, 22 tài liệu còn lại 0%.
Chữ vẫn thật, `height` và `font_size` vẫn đúng — engine chỉ không cho biết bề rộng.

`Box.from_absolute()` **chấp nhận `x1 == x0`** (đã thử: không ném; `__post_init__` chỉ
chặn box lộn ngược). Bê thẳng `x + width` thì tài liệu đó vào bench với 396 hộp diện
tích 0 → IoU 0 tuyệt đối → bảng đọc thành "pdf-inspector định vị kém", trong khi nó
định vị tốt ở 22 tài liệu kia.

Adapter **giữ chữ, để `box=None`**, và đếm — số item mất hộp ghi vào `OcrResult.error`
dạng cảnh báo không-thất-bại. Hai hướng còn lại đều bị bỏ: suy bề rộng từ
`font_size × len(text)` là đoán, và số đoán đi thẳng vào IoU như thể là số đo; bỏ luôn
item thì mất 38% văn bản ở CER — sửa một chỗ sai thành hai chỗ sai.

**(b) `classify_pdf()` và `extract_pages_markdown()` bất đồng 22/204 (10.8%).** Hai
chiều, không phải một chiều. Và **18/22 ca bất đồng có `confidence = 1.00`** — độ tin
cậy của `classify_pdf` không dùng được làm cổng chặn, nó tự tin ngay ở chỗ nó lệch.

Bất đồng dồn theo **loại tài liệu**: `patents` 15/34 (44%), `laws_and_regulations` 4/34,
`government_tenders` và `scientific_articles` **0/34**. Ở 14/18 ca, `needs_ocr=True`
mà `ocr_reason` là `None` — cờ bật không kèm lý do nào.

Vì vậy `ScanLabel.api` là **bắt buộc**: ghi "pdf-inspector nói tài liệu này cần OCR" mà
không nói hàm nào là một con số vô nghĩa. Bảng đầy đủ + so với heuristic sản xuất của
Sovereign: `results/scan_label_compare.md`, sinh bởi `scripts/compare_scan_label.py`.

### 7. Baseline đo nhầm cấu hình — và cấu hình đó tính tiền theo trang

Phát hiện ở A7 (TASK-078), engine `sovereign` (chính pipeline BE đang chạy production).

Đề bài ghi cấu hình production là `ocr_use_local_first=False`, `ocr_use_vision_api=False`,
dẫn chứng `app/config.py:122` và `:127`. Mặc định lớp đúng là `False` thật. Nhưng `.env` và
`.env.stag` của BE **đều đặt cả hai thành `true`**, và `config.py:10` ghim
`_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"` — **theo đường dẫn, không theo
cwd**. Import trần từ `ocr-bench/` (thư mục hoàn toàn khác) vẫn giải ra `vision=True` kèm
`OPENROUTER_API_KEY` thật đã nạp. Chạy 204 tài liệu ở trạng thái đó là gửi hoá đơn theo trang.

Bộ nối vì thế ghi `os.environ` **trước** khi import BE — bắt buộc đúng thứ tự đó, vì
`_api_key`/`_api_url`/`_gdoc_parser_url`/`_groq_api_key` bị đóng băng ở cấp module lúc import
(`openrouter_document_parser.py:30-38`); ghi env sau đó là ghi vào chỗ không ai đọc nữa. Rồi
`kiem_config()` gọi `get_settings.cache_clear()` (hàm có `@lru_cache`) và **giải lại**, ném
nếu vision còn bật hoặc khoá còn nạp. Kiểm cái mình vừa ghi, không tin là nó đã có hiệu lực.

Ba hệ quả kéo theo:

**(a) Tắt vision không có nghĩa là không OCR.** `_apply_vision_fallback` (`:418-420`) và
`_maybe_ocr_embedded_images` (`:560-561`) có cổng chặn theo cờ; `_maybe_escalate_to_marker`
**không có**. Chạy thật với vision tắt vẫn thấy log "Escalate sang Marker OCR". Marker là ML
cục bộ trên CPU, ~54 s/trang. Nên trần chi phí phải bao **thời gian máy**, không chỉ tiền API.

**(b) Trần chi phí phải thoát ra khỏi `execute()`.** `Adapter.execute()` bắt `Exception` và
biến lỗi thành một dòng `failed=True` rồi **chạy tiếp** — đúng cho engine hỏng, sai chết người
cho trần chi phí. `VuotTran` vì thế kế thừa `BaseException`, không phải `Exception`, và có test
khoá đúng chuyện đó. Trần đã nổ thật một lần trên bộ olmocr (`đã chạy 250/250`, dừng ngay).

**(c) Cùng một bộ nối, hai con số hoàn toàn khác nhau.** `.venv-sov` (bao đóng nhẹ, không
torch) không leo thang được sang Marker; `.venv-marker` thì có. Chênh nhau hàng chục lần thời
gian mà nhìn bảng thì trông như cùng một thứ — nên `marker_available` nằm trong
`config_fingerprint` của **mọi** kết quả, cạnh cả hai cờ OCR và ba mức trần.

Đo được, trên đúng một tài liệu: ở `light` nó hỏng `ocr.extractEmpty` trong ~0.0 s; ở `full`
nó **thành công**, 838 ký tự, **162.8 s**. Tài liệu kế tiếp mất 550.5 s và đâm vào trần. Tắt
vision không làm pipeline rẻ đi — nó đổi hoá đơn API lấy hoá đơn CPU.

Fingerprint ghi `api_key_present` dạng **boolean**, không bao giờ ghi giá trị khoá: `prediction/`
được commit, nên một khoá lọt vào fingerprint là lọt thẳng vào lịch sử git. Có test riêng.

Và **suy thoái âm thầm**: thiếu `pdfminer` hay thiếu cache Surya không ném — chỉ log WARNING
rồi trả kết quả *tệ hơn*. Một baseline đo trong môi trường thiếu trông y hệt baseline thật.

### 8. Tỉ lệ lỗi **vượt 1**, và nhãn rỗng không hề báo lỗi

Phát hiện ở B1 (TASK-079), khi cài `cer`/`wer`.

`jiwer.cer(ref, hyp)` chia số lỗi cho độ dài **nhãn**, nên phần chèn thừa không có trần:
`jiwer.cer("ab", "abcdefghij")` trả **4.0**. Công thức hiển nhiên `1 - err` cho **−3.0**, mà
`Metric.score()` ném khi điểm ra ngoài [0,1] → **một engine nói nhảm làm sập cả lượt chấm**
thay vì bị xếp bét. Lỗi hạ tầng đội lốt lỗi engine, kiểu khó lần nhất. Nên `_kep()` kẹp về
[0,1] và ghi `bi_kep=True` cùng `err` thô vào `detail` — kẹp mà không để lại dấu vết thì
sau này không ai phân biệt được "sai vừa" với "nói nhảm gấp năm mươi lần".

Cái thứ hai nguy hiểm hơn vì **im lặng**: `jiwer` không ném với nhãn rỗng. `cer("", "abc")`
trả `3`, `cer("", "")` trả `0`. Mà `AnnotationGT.text` được phép `None` (DocLayNet chỉ có
nhãn bố cục). Không tự chặn thì mọi tài liệu thiếu nhãn chữ bị chấm **0 điểm cho engine** —
phạt engine vì cái *nhãn* không có. Vì thế `metrics/base.py` mọc thêm móc `_na_rieng()`:
điều kiện N/A riêng của từng metric, kiểm **sau** ba cổng chung, `score()` vẫn là cổng duy
nhất và subclass vẫn không được override nó.

Hệ quả cần biết trước khi đọc bảng: trên bộ mẫu **hiện tại**, `cer`/`wer` ra N/A **toàn bộ** —
DocLayNet là `text=None` (→ `no_ground_truth`), olmOCR là `AssertionGT` (→ `wrong_gt_kind`).
Thước đo đã có, **dữ liệu để đo thì chưa**. Đó là việc của nhóm D, không phải lỗi metric — và
đúng theo bẫy 3, nó hiện ra thành ô `N/A` chứ không thành điểm 0.

### 9. TEDS đo **cách viết HTML** nếu không chặn, và bản tham chiếu có hai bản khác nhau

Phát hiện ở B2 (TASK-080), khi cài `teds`/`teds_struct`.

**(a) Cùng một bảng, hai kiểu HTML, điểm khác nhau.** Đo trên `prediction/` đã lưu: Marker
sinh `<table><thead><tr><th>…`, opendataloader sinh `<table><tr><td>…`. Cùng nội dung, cùng
lưới. Không chuẩn hoá thì mỗi bảng bị trừ một nút `tbody` cộng một `rename` cho mỗi ô tiêu
đề — cùng một bảng logic cho **0.5714** thay vì **1.0**. Đó là đo quy ước sinh HTML, không
phải đo độ chính xác. Nên `thead/tbody/tfoot/colgroup` bị bỏ và `th` → `td` **mặc định**;
`teds_score(..., chuan_hoa=False)` giữ lại hành vi thô để đối chiếu bản tham chiếu.

**(b) Bản tham chiếu không thống nhất với chính nó.** Nguồn PubTabNet dùng mẫu số
`len(table.xpath('.//*'))`; gói `table_recognition_metric` (bản đóng gói lại, và là bản duy
nhất *chạy được* để đối chiếu) dùng `tree.size()`. Bảng một ô: **0.5** so với **0.6667**.
Chọn `tree.size()` — thẻ inline trong ô (`<b>`, `<br/>`) **không phải nút của cây** nên
khoảng cách sửa cây không bao giờ chạm tới chúng; để chúng trong mẫu số là cộng điểm miễn
phí theo lượng markup. Khác về thang, không khác về thứ hạng. Đừng so số ở đây với bảng TEDS
in trong bài báo mà không quy về cùng mẫu số.

**(c) Một chỗ cố ý lệch, đã khoá bằng test.** Chữ trong ô đi qua `normalize_text()`. Bản
tham chiếu chấm `<td>  Doanh   thu </td>` với `<td>Doanh thu</td>` là **0.0** — hai ô hiển
thị y hệt nhau. Ngoài chỗ đó thì khớp tuyệt đối: 120 cặp bảng ngẫu nhiên khớp 120/120 khi ô
không có khoảng trắng, và `teds_struct` khớp 120/120 kể cả khi có.

**(d) Bảng nhãn rỗng ⇒ N/A, không phải 0 và cũng không phải 1.0.** Bản gốc trả 0 khi một
phía thiếu `<table>`. Với bench thì đó là phạt engine vì nhãn hỏng. 1.0 cũng sai theo hướng
ngược lại: nó **thưởng** cho engine phun `<table></table>` rỗng.

Và cùng hệ quả với bẫy 8: trên bộ mẫu hiện tại `teds`/`teds_struct` ra N/A **toàn bộ** —
`load_doclaynet()` không dựng `AnnotationGT.tables` cho tài liệu nào (0/204), dù engine
**có** trả bảng (opendataloader 28, marker 2). Thước đo đã có, nhãn bảng thì chưa.

### 10. Trung bình của `heading` **không** đo phân cấp, và `nid` không có nhãn để đo

Phát hiện ở B4 (TASK-082), và cả hai vế đều là chuyện "có số ≠ số có nghĩa".

**(a) Bộ mẫu không có nhãn thứ tự đọc. `nid` ra N/A trên cả 205 tài liệu.** DocLayNet
không phát hành thứ tự đọc; `corpus.py` xếp block theo `annotation["id"]` của COCO, tức
**thứ tự người gán nhãn vẽ hộp** — không phải thứ tự đọc. Cám dỗ ở đây rất cụ thể: điền
`reading_order` bằng cách sắp xếp hình học (trên xuống, trái sang) thì `nid` lập tức ra số
đẹp cho mọi tài liệu. Số đó là **bench tự chấm heuristic của chính nó**: engine nào sắp xếp
giống hàm sort của bench thì thắng, không liên quan gì tới đọc đúng hay sai. `nid` được
viết đủ và có test cho đường chấm thật (kể cả test chứng minh nó đọc `reading_order` chứ
không đọc hình học), rồi báo N/A cho tới ngày có nhãn thật.

**(b) `heading` ra 0.5611 trên 15 tài liệu — và con số đó mô tả gần như không tài liệu
nào.** Phân bố lưỡng cực: 7 tài liệu 1.0, 6 tài liệu 0.0. Tách theo số **cặp** so được:

| nhóm | n | trung bình | đọc thế nào |
|---|---|---|---|
| 0 cặp (điểm 0.0 ép) | 5 | 0.0 | engine ghép được <2 tiêu đề — lỗi **độ phủ**, không phải lỗi phân cấp |
| đúng 1 cặp | 6 | — | chỉ có thể 0.0 hoặc 1.0, không có giá trị giữa |
| >1 cặp | 4 | **0.8542** | vùng duy nhất con số nói về phân cấp |
| có ≥1 cặp | 10 | **0.8417** | |

0.5611 bị kéo xuống bởi 5 tài liệu **không so cặp nào**. Vì thế `detail["n_cap"]` luôn có
mặt kể cả ở nhánh 0.0, để tách hai nhóm mà không phải đoán. **Đừng in trung bình `heading`
một mình.**

**(c) Trần nhãn là 2 mức.** DocLayNet chỉ có `Title` và `Section-header`. `heading` cao chỉ
có nghĩa "không đảo tiêu đề chính với tiêu đề mục" — lỗi lồng sâu (`###` so với `####`) là
**vô hình**, và có test khẳng định đúng cái vô hình đó. Chỉ **17/204** tài liệu có đủ 2 cấp.

**(d) `HEADING_LEVEL` và `SECTION_HIERARCHY` là hai năng lực, gộp lại là chấm sai.**
`OcrBlock` có hai trường riêng: `level` (tiêu đề tự khai cấp mấy) và `section_hierarchy`
(đường dẫn tổ tiên — một cái **cây**). Có cấp không suy ra cây: opendataloader khai cấp 1..7
nhưng JSON của nó phẳng, không node nào trỏ về mục cha. Đòi cây ở `heading` sẽ loại đúng
engine duy nhất chấm được. Ca thật theo chiều ngược lại: bản đầu chỉ gate theo `BLOCK_BBOX`,
và pdf_inspector — **0 block tiêu đề trên toàn bộ 204 tài liệu** — rơi vào nhánh 0.0, ăn
**0.0000 trên 17 tài liệu** vì một việc nó chưa từng khai nhận. Đúng bẫy 3, chỉ đổi metric.
Số 0.0000 lặp lại y hệt ấy là thứ đáng nghi ngay từ đầu, không phải thứ đáng đem đi báo cáo.

### 11. `assert_math_presence` ở đây là **cận dưới**, không phải điểm công thức thật

Phát hiện ở B5 (TASK-083). olmOCR gốc chấm công thức bằng cách **dựng cả hai biểu thức
LaTeX ra ảnh rồi so pixel** — `\frac{a}{b}` và `\dfrac{a}{b}` cho ra cùng một hình nên
được tính là khớp. Bản ở đây so **chuỗi sau chuẩn hoá**, chặt hơn hẳn: mọi cách viết
tương đương mà chuẩn hoá không gộp được đều bị chấm trượt. Điểm `math_presence` của
repo này **≤ điểm olmOCR công bố**, luôn luôn, và độ lệch không đo được nếu không dựng
ảnh.

Chuyện này không nhỏ: `math_presence` là **3.385/7.019 khẳng định — 48% cả bộ nhãn**.
Một engine bị trừ oan ở đây sẽ tụt hạng vì cách so, không phải vì đọc sai.

Hai việc để bẫy này không âm thầm: `detail` tách `n_khop_nguyen_van` khỏi
`n_khop_sau_chuan_hoa` (khoảng cách giữa hai số là phần chuẩn hoá đang gánh, và nếu nó
lớn thì cận dưới đang lỏng), và docstring của metric ghi thẳng chữ "cận dưới". **So
LaTeX bằng ảnh là task riêng** — nó kéo theo bộ dựng công thức + so ảnh, không nhét vào
được B5.

Ghi chú đọc số: `opendataloader` ra **0.000** trên cả `arxiv_math` (25 tài liệu) lẫn
`old_scans_math` (8). Dò tay cho thấy nó xuất ký hiệu Unicode (`θ`, `ρ`) chứ không xuất
LaTeX — tức 0.000 ở đây là sự thật về engine, **không** phải do cận dưới. Cận dưới là
rủi ro cho engine *có* xuất LaTeX, chưa engine nào trong bộ này làm.

### 12. `assert_text_absence` **thưởng cho engine không xuất gì cả**

Cũng ở B5, và đây là cái bẫy khó chịu nhất của toàn bộ khẳng định: "chuỗi X không được
xuất hiện" là đúng một cách tầm thường khi đầu ra rỗng. Không có gì thì không có gì bị cấm.

Số thật, không phải giả thuyết: `opendataloader` trên tầng `old_scans` xuất **32–33 ký tự**
mỗi tài liệu — đúng một dòng `![](<1_images/imageFile1.png>)`, tức là *không đọc được gì* —
và ăn **`assert_text_absence` = 1.000**, điểm tuyệt đối, trong khi `text_presence` và
`reading_order` của chính nó ở tầng đó là **0.000**.

Thứ duy nhất chặn được chiêu này trong bộ nhãn là `assert_baseline` (đòi đầu ra phải có
tối thiểu nội dung), và cả 1.403 tài liệu **chỉ có 9 khẳng định baseline**. Không đủ để
cân. Vì thế:

- **Không bao giờ đọc `text_absence` một mình.** Nó chỉ có nghĩa khi đặt cạnh
  `text_presence` của cùng engine trên cùng tầng. Cao ở cột này + 0 ở cột kia = engine
  im lặng, không phải engine sạch.
- Đây cũng là lý do thứ hai để **tách điểm theo tầng**: gộp tầng lại thì `text_absence`
  0.517 của opendataloader trông như một con số tầm trung bình thường, chứ không lộ ra
  rằng nó là trung bình của 0.356 (đọc thật) và 1.000 (không đọc gì).

### 13. Cột RSS xếp hạng bộ nhớ theo **thứ tự chạy**, và khen engine nuôi JVM là nhẹ nhất

Hai nửa, cả hai đều im lặng (B6):

**Nửa thứ nhất — RSS không bao giờ giảm.** RSS là mốc nước cao của *cả tiến trình*: nó
không tụt khi Python trả vùng nhớ về allocator. Chạy ba engine trong một tiến trình rồi
lấy `max(RSS)` cho từng engine thì engine thứ ba luôn thừa hưởng đỉnh của hai engine
trước — bảng "ngốn RAM" sẽ đúng bằng thứ tự chạy, và đảo thứ tự sẽ ra một bảng khác.
Chặn bằng cách đo **delta trong cửa sổ chạy**: lấy mốc ngay trước `run()`, lấy mẫu bằng
luồng nền, báo `đỉnh − mốc`. Mốc chính là mẫu đầu tiên nên hiệu không có đường nào ra
số âm — không phải kẹp về 0.

**Nửa thứ hai — RSS của Python không thấy tiến trình con.** `opendataloader` chạy một
`.jar` bằng tiến trình `java`, `sovereign` có nhánh `subprocess`. In một cột RSS trần
trụi sẽ làm engine đang nuôi cả một JVM trông **nhẹ nhất bảng** — sai theo một hướng
biết trước, tức còn tệ hơn nhiễu. Chặn bằng `rss_scope` đi kèm **mọi** con số RSS:
`OcrResult` ném nếu có `peak_rss_mb` mà không có `rss_scope`, và bảng in kèm cảnh báo
khi phạm vi là `process`. Đọc một tiến trình con không được thì **hạ** phạm vi xuống
`process` chứ không im lặng báo thiếu.

Cái bẫy thứ ba, nhỏ hơn nhưng cùng họ: **engine chết ngay lập tức có `s/trang` thấp
nhất bảng.** Vì thế `PerfAggregate` mang `fail_rate` trong cùng dataclass với các trung
bình, đúng như `Aggregate` — không có đường nào lấy trung bình mà không cầm sẵn tỉ lệ
hỏng.

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
├── rss.py          đo đỉnh RSS (psutil, lấy mẫu 50ms) — tầng thấp, không biết gì về bảng
├── adapters/       base.py · noop.py  (sabotage → A1b, engine thật → A4-A7)
└── metrics/        base.py            (cer/teds/imgf1/nid/heading → nhóm B)
    └── perf.py     sec/trang · RSS · FailRate — **không** kế thừa `Metric`, xem đầu file

pdfs/ ground-truth/ prediction/ results/ history/ charts/
```

`perf.py` nằm trong `metrics/` cho gần chỗ dùng, nhưng nó là **họ dữ liệu riêng**: `Metric`
chặn giá trị ngoài `[0,1]` và quy ước cao là tốt, còn giây và MB thì không chặn trên và
thấp mới tốt. Ép nó vào `Metric` chỉ có hai đường, đều hỏng: bỏ cổng `[0,1]` (mất cổng
đang bảo vệ 14 metric) hoặc chuẩn hoá `1/(1+t)` (ra số không đơn vị, không trả lời nổi
"1400 tài liệu mất bao lâu").

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
| **A6 — bộ nối pdf-inspector** | **xong** — engine duy nhất khai `SCAN_LABEL`; xem bẫy 6 |
| **A7 — bộ nối pipeline BE Sovereign** | **xong** — baseline, 16 test, 2 chế độ đo; xem bẫy 7 |
| **B1 — CER/WER** | **xong** — 21 test; N/A toàn bộ trên bộ mẫu hiện tại, xem bẫy 8 |
| **B2 — TEDS / TEDS-Struct** | **xong** — 22 test, coverage 100%; khớp bản tham chiếu 240/240 cặp; N/A toàn bộ, xem bẫy 9 |
| **B3 — ImgF1 / ImgIou** | **xong** — 23 test, coverage 100%; **thước đo đầu tiên ra số thật**: opendataloader F1 0.355 (98 tài liệu), marker 0.667 (5) |
| **B4 — NID / Heading** | **xong** — 42 test, coverage 100%; `nid` N/A toàn bộ (không có nhãn thứ tự đọc), `heading` chỉ 15 tài liệu / 1 engine và **không được đọc trung bình một mình** — xem bẫy 10 |
| **B5 — bộ khẳng định olmOCR** | **xong** — 35 test, coverage 96%; **sáu** metric riêng cho sáu loại (AC-02 cấm gộp), chấm tách theo loại × theo tầng bằng `scripts/score_assertions.py`; xem bẫy 11 và 12 |
| **B6 — tốc độ / bộ nhớ / tỉ lệ hỏng** | **xong** — 27 test, coverage 100% (`perf`) & 95% (`rss`); perf **không** kế thừa `Metric`; schema prediction lên bản 2, nâng 718 file tại chỗ không chạy lại engine; xem bẫy 13 |

## Cảnh báo dữ liệu

Bộ mẫu hiện tại là dữ liệu công khai. **Nếu** về sau đưa tài liệu thật của khách vào,
phải cho `pdfs/` của phần đó vào `.gitignore` và chỉ commit `manifest.yaml` + checksum.
Đưa tài liệu khách vào repo là rủi ro rò rỉ.

OmniDocBench là **research-only, cấm thương mại** — không đặt file của nó vào repo này.
