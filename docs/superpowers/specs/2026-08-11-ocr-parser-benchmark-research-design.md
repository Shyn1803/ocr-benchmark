# Thiết kế nghiên cứu benchmark OCR và PDF parser cho Sovereign

**Ngày:** 2026-08-11  
**Trạng thái:** Thiết kế đã được thống nhất, chờ người dùng duyệt tài liệu  
**Ngôn ngữ báo cáo:** Tiếng Việt  
**Loại đầu ra:** Báo cáo khoa học nội bộ kèm executive summary  

## 1. Tóm tắt điều hành

Nghiên cứu so sánh chất lượng OCR và phân tích cấu trúc PDF giữa bốn công cụ:

- Docling;
- OpenDataLoader;
- Marker;
- pipeline Sovereign hiện tại.

Mỗi công cụ được đánh giá ở hai cấu hình độc lập:

1. `default`: cấu hình mặc định chính thức;
2. `scan_optimized`: cấu hình tối ưu cho PDF scan, với mọi tham số ảnh hưởng chất lượng được công bố.

Nghiên cứu chỉ dùng dataset công khai để có thể tái lập. Kết quả không ép thành một điểm tổng hợp duy nhất. Thay vào đó, benchmark xếp hạng theo từng năng lực: OCR text, layout, thứ tự đọc, bảng, độ bền trên scan và hiệu năng. Kết luận cuối cùng là khuyến nghị theo tình huống sử dụng.

Đầu ra chính gồm bài báo tiếng Việt, executive summary, dữ liệu kết quả có thể kiểm toán, bảng, biểu đồ, cấu hình chạy và phụ lục phân tích lỗi.

## 2. Mục tiêu và phạm vi

### 2.1. Mục tiêu

- Đo chất lượng OCR và PDF parsing bằng ground truth độc lập.
- So sánh công bằng trên cùng tập tài liệu và cùng điều kiện phần cứng.
- Định lượng lợi ích và chi phí của cấu hình tối ưu cho scan.
- Xác định công cụ phù hợp với từng loại tài liệu và ràng buộc vận hành của Sovereign.
- Tạo quy trình benchmark có thể chạy lại khi engine, model hoặc cấu hình thay đổi.

### 2.2. Trong phạm vi

- Nhận dạng text và dấu tiếng Việt khi dataset có nhãn phù hợp.
- Phát hiện và phân loại block tài liệu.
- Bounding box và thứ tự đọc.
- Cấu trúc và nội dung bảng.
- Độ bền trên tài liệu scan khó.
- Thời gian xử lý, bộ nhớ và tỷ lệ thất bại.

### 2.3. Ngoài phạm vi

- Không chấm chất lượng embedding, retrieval hoặc câu trả lời cuối của RAG.
- Không dùng tài liệu nội bộ hoặc tài liệu khách hàng.
- Không tạo một điểm tổng hợp để tuyên bố một engine thắng mọi tình huống.
- Không dùng output của engine làm ground truth cho chính engine đó.

## 3. Câu hỏi nghiên cứu

- **RQ1:** Công cụ nào nhận dạng văn bản chính xác nhất?
- **RQ2:** Công cụ nào bảo toàn layout, loại block và thứ tự đọc tốt nhất?
- **RQ3:** Công cụ nào tái tạo cấu trúc và nội dung bảng tốt nhất?
- **RQ4:** Chất lượng của từng công cụ suy giảm thế nào trên PDF scan khó?
- **RQ5:** Cấu hình `scan_optimized` cải thiện bao nhiêu so với `default`?
- **RQ6:** Độ chính xác phải đánh đổi thế nào với thời gian, bộ nhớ và phần cứng?

## 4. Cách tổ chức nghiên cứu

Nghiên cứu dùng **benchmark phân tầng theo năng lực**. Mỗi tầng có dataset, ground truth và metric phù hợp. Tất cả tầng dùng chung contract dữ liệu, cơ chế cache prediction, quy tắc common set và hệ thống báo cáo.

| Tầng | Năng lực | Metric chính | Metric phụ |
|---|---|---|---|
| 1 | OCR text | CER | WER, lỗi dấu |
| 2 | Layout | Macro Block F1 | Mean IoU, precision, recall, Type F1 |
| 3 | Reading order | NID | Pairwise order accuracy |
| 4 | Bảng | TEDS-Struct | TEDS, Cell F1, Cell CER |
| 5 | Scan robustness | Relative degradation | Coverage và fail-rate degradation |
| 6 | Hiệu năng | Warm seconds/page | Cold start, p95, peak RSS, VRAM |

Reading order được tách khỏi layout vì engine có thể tìm đúng block nhưng nối text sai thứ tự.

## 5. Dataset và ground truth

### 5.1. Nguyên tắc lựa chọn

Dataset chỉ được đưa vào bảng chính khi thỏa mãn các điều kiện:

- nguồn và phiên bản xác định được;
- giấy phép cho phép mục đích nghiên cứu dự kiến;
- file và annotation có checksum;
- annotation phù hợp với ít nhất một metric đã định nghĩa;
- có thể ánh xạ về canonical ground-truth schema mà không suy diễn từ output engine.

### 5.2. Các nguồn công khai

| Dataset | Vai trò dự kiến | Giới hạn cần công bố |
|---|---|---|
| DocLayNet | Layout, block type, bounding box | Không phải ground truth OCR tiếng Việt đầy đủ |
| olmOCR-bench | Text/assertion, reading order, bảng, scan cũ | Chủ yếu không phải tài liệu tiếng Việt |
| UIT-DODV | Layout và tài liệu scan tiếng Việt | Chỉ sử dụng nếu truy cập và giấy phép được xác minh |
| PubTabNet | Cấu trúc và nội dung bảng | Thiên về bảng khoa học, không đại diện mọi PDF scan |
| FinTabNet | Bảng tài chính phức tạp | Domain tài chính, không đại diện toàn bộ tài liệu |
| OHR-Bench | Độ bền OCR và tác động của chất lượng scan | Chỉ dùng những phần có ground truth phù hợp phạm vi parser |

Không dataset nào bị coi là ground truth toàn năng. Metric thiếu nhãn trên một tài liệu phải trả `N/A`, không phải 0.

### 5.3. Manifest hợp nhất

Benchmark dùng một manifest chung thay vì sửa dữ liệu nguồn:

```json
{
  "document_id": "doclaynet_000001",
  "source_dataset": "DocLayNet",
  "source_version": "1.1",
  "source_url": "https://github.com/DS4SD/DocLayNet",
  "source_license": "CDLA-Permissive-2.0",
  "pdf_sha256": "computed_from_downloaded_pdf",
  "annotation_sha256": "computed_from_downloaded_annotation",
  "language": ["en"],
  "document_type": "scientific",
  "scan_category": "digital",
  "annotations": {
    "text": false,
    "layout": true,
    "reading_order": false,
    "tables": false
  }
}
```

### 5.4. Correction overlay

Dataset công khai vẫn có thể sai nhãn. Không sửa trực tiếp file nguồn. Mọi correction phải nằm trong overlay, có bằng chứng độc lập và được báo cáo trước/sau nếu ảnh hưởng đáng kể tới thứ hạng.

```json
{
  "document_id": "doc-123",
  "operation": "add",
  "item": {
    "type": "picture",
    "bbox": [0.10, 0.02, 0.21, 0.07]
  },
  "evidence": {
    "method": "PDF content stream and visual inspection",
    "reviewer_count": 2
  }
}
```

## 6. Engine và cấu hình thí nghiệm

Mỗi profile được xem như một engine độc lập trong báo cáo:

```text
docling_default
docling_scan
opendataloader_default
opendataloader_scan
marker_default
marker_scan
sovereign_default
sovereign_scan
```

### 6.1. Quy tắc cấu hình

- `default` bám theo cấu hình mặc định chính thức của phiên bản được khóa.
- `scan_optimized` bật OCR phù hợp, dùng ngôn ngữ tương ứng nếu engine hỗ trợ, render khoảng 300 DPI và chọn chế độ bảng chính xác.
- CPU và GPU là hai thí nghiệm riêng.
- API trả phí hoặc dịch vụ không tái lập không được trộn với local profile; nếu cần đo, phải thành profile riêng và công bố chi phí.
- Mọi profile phải lưu fingerprint đầy đủ.

```json
{
  "parser": "docling",
  "parser_version": "recorded_at_runtime",
  "ocr_engine": "rapidocr",
  "ocr_model": "recorded_model_identifier",
  "ocr_language": "vi",
  "force_full_page_ocr": true,
  "render_dpi": 300,
  "table_mode": "accurate",
  "cell_matching": true,
  "device": "cpu"
}
```

## 7. Contract dữ liệu benchmark

Raw JSON của engine phải được giữ nguyên làm artifact. Adapter chuyển raw output về canonical prediction để metric không phụ thuộc schema riêng của Docling, OpenDataLoader hay Marker.

```text
PDF
  -> raw engine output
  -> adapter
  -> canonical prediction
  -> metrics
  -> aggregate results
  -> tables/figures/paper
```

Canonical prediction cần giữ tối thiểu:

- document ID và engine profile;
- raw text và normalized text;
- block ID, type, page và bbox;
- reading order, parent/children hoặc section path nếu engine thực sự cung cấp;
- OCR confidence nếu có;
- provenance về raw item;
- table cells, row/column index, rowspan/colspan và cell bbox;
- thời gian, model-load time, peak RSS, RSS scope;
- trạng thái thất bại và mã lỗi;
- config fingerprint.

Quy ước hình học chung:

- page 0-based;
- bbox chuẩn hóa `[0,1]`;
- gốc trên-trái;
- trục y hướng xuống.

## 8. Chấm điểm và tổng hợp

### 8.1. Đơn vị thống kê

Đơn vị thống kê là tài liệu. Metric được tính trên từng tài liệu rồi lấy macro average để tài liệu dài không chi phối toàn bộ kết quả.

\[
Score_e = \frac{1}{N}\sum_{d=1}^{N} Score(e,d)
\]

Mỗi số trong bảng phải kèm:

- mean;
- khoảng tin cậy 95%;
- số tài liệu `n`;
- coverage;
- fail rate.

### 8.2. Conditional và end-to-end quality

Mỗi metric chất lượng cần báo cáo hai góc nhìn:

- **Conditional quality:** chất lượng trên tài liệu xử lý thành công.
- **End-to-end quality:** tài liệu engine thất bại được tính là 0.

Engine không có capability được ghi `N/A`. Engine khai có capability nhưng chạy hỏng được tính là thất bại.

### 8.3. Xếp hạng

Không có overall score. Metric chính của từng năng lực được dùng để xếp hạng:

| Năng lực | Tiêu chí xếp hạng |
|---|---|
| OCR | CER thấp hơn |
| Layout | Macro Block F1 cao hơn |
| Reading order | NID cao hơn |
| Bảng | TEDS-Struct, sau đó TEDS cao hơn |
| Scan robustness | Mức suy giảm tương đối thấp hơn |
| Hiệu năng | Warm seconds/page thấp hơn |

Không dùng hạng cứng nếu khác biệt không có ý nghĩa. Các profile được phân nhóm:

- **A:** không phân biệt thống kê với profile tốt nhất;
- **B:** thấp hơn nhóm A có ý nghĩa;
- **C:** thấp hơn rõ rệt;
- **N/A:** không hỗ trợ hoặc không có ground truth.

## 9. Bảng bắt buộc trong báo cáo

1. Thành phần và coverage ground truth của dataset.
2. Cấu hình đầy đủ của từng engine profile.
3. OCR text: CER, WER, lỗi dấu, coverage, fail rate.
4. Layout và reading order: Block F1, IoU, Type F1, NID.
5. Bảng: Table Recall, TEDS-Struct, TEDS, Cell F1, Cell CER.
6. So sánh `default` với `scan_optimized` bằng paired delta.
7. Hiệu năng: cold start, warm seconds/page, p95, RSS, VRAM.
8. Common-set coverage để ngăn so sánh các engine trên tập tài liệu khác nhau.
9. Failure taxonomy và số lượng lỗi theo nhóm.

Ví dụ cách hiển thị một ô kết quả:

```text
TEDS = 0,842 [95% CI: 0,816-0,867], n=184, fail=2,1%
```

## 10. Biểu đồ bắt buộc

- **Forest plot:** mean và khoảng tin cậy theo năng lực.
- **Accuracy-speed Pareto:** chất lượng, giây/trang và kích thước điểm theo RSS.
- **Scan degradation curve:** mức suy giảm từ digital đến severe scan.
- **Capability heatmap:** chỉ dùng cho executive summary; bài báo vẫn dùng số thực.
- **Failure distribution:** OCR sai, mất dòng, sai order, sai block, mất bảng, sai cell, timeout và OOM.

Không dùng radar chart làm bằng chứng chính vì diện tích hình dễ gây hiểu nhầm giữa metric khác thang đo.

## 11. Kiểm định thống kê

- Paired bootstrap 10.000 lần để tính confidence interval của chênh lệch.
- Wilcoxon signed-rank khi so hai profile trên cùng tài liệu.
- Holm-Bonferroni khi thực hiện nhiều phép so sánh.
- Báo effect size bên cạnh p-value.
- Chỉ tuyên bố profile thắng khi khác biệt có ý nghĩa thống kê và có ý nghĩa thực tế.
- Mọi so sánh trực tiếp phải dùng common set theo `doc_id`.

## 12. Xác thực ground truth, adapter và metric

### 12.1. Ground truth

- Lấy từ annotation chính thức, không lấy từ engine prediction.
- Khóa nguồn và annotation bằng SHA-256.
- Audit phân tầng các ca điểm cao, điểm thấp, chênh lệch lớn, ngẫu nhiên, điểm 0 và failure.
- Phân loại bất đồng thành `engine`, `adapter`, `ground_truth`, `metric` hoặc `unknown`.

### 12.2. Adapter

Mỗi adapter phải qua:

- known-coordinate test;
- kiểm tra page index và chiều trục y;
- round-trip overlay trên ảnh PDF;
- real-engine smoke test;
- kiểm tra block/text không rỗng ngoài trường hợp hợp lệ;
- kiểm tra config fingerprint;
- kiểm tra raw item truy được tới canonical item.

### 12.3. Metric controls

Mỗi metric phải có:

- positive control: prediction bằng ground truth;
- negative control: output rỗng hoặc hỏng nặng;
- intermediate control: sai một phần;
- property test cho biên và bất biến;
- đối chiếu với reference implementation hoặc kết quả tính tay.

Thứ tự bắt buộc:

```text
perfect > partially corrupted > severely corrupted
```

### 12.4. Sabotage test

Tạo prediction hỏng có kiểm soát từ output thật:

- xóa 10% rồi 30% ký tự;
- đảo thứ tự paragraph;
- dịch bbox;
- xóa rowspan/colspan;
- bỏ bảng;
- bỏ block theo tỷ lệ tăng dần.

Metric hợp lệ phải suy giảm đơn điệu theo mức phá. Metric không qua cổng này không được dùng trong bảng xếp hạng chính.

### 12.5. Tiêu chuẩn metric được công bố

Một metric chỉ vào bảng chính khi:

- có ground truth độc lập;
- có định nghĩa toán học;
- có reference implementation hoặc tính tay đối chứng;
- các control đều đạt;
- sabotage nặng hơn làm điểm xấu đi;
- adapter liên quan đã qua smoke/coordinate test;
- manual audit không phát hiện sai lệch hệ thống;
- common set đủ lớn.

Metric chưa đạt chỉ nằm trong phụ lục với nhãn `experimental`.

## 13. Phân tích lỗi

Mẫu bắt buộc để đọc tay:

- điểm 0 và điểm 1;
- chênh lệch lớn nhất giữa hai engine;
- engine có số block bất thường;
- metric mâu thuẫn với quan sát trực quan;
- toàn bộ timeout, OOM và crash;
- mẫu ngẫu nhiên phân tầng theo dataset và scan category.

Failure taxonomy tối thiểu:

```text
ocr_character
vietnamese_diacritic
missing_line
reading_order
block_split_merge
wrong_block_type
missing_table
table_cell_structure
bbox_coordinate
timeout
out_of_memory
unsupported
adapter_error
ground_truth_error
metric_error
```

## 14. Đầu ra nghiên cứu

```text
ocr-bench/
├── paper/
│   ├── paper-vi.md
│   ├── paper-vi.pdf
│   ├── executive-summary.md
│   └── appendices/
├── datasets/
│   └── manifest.json
├── results/
│   ├── raw-results.jsonl
│   ├── aggregate-results.json
│   ├── statistical-tests.json
│   └── recommendations.json
├── tables/
│   ├── text-ocr.md
│   ├── layout.md
│   ├── reading-order.md
│   ├── tables.md
│   ├── scan-robustness.md
│   └── performance.md
└── figures/
    ├── capability-ranking.svg
    ├── accuracy-speed.svg
    ├── scan-degradation.svg
    └── failure-distribution.svg
```

Tên báo cáo dự kiến:

> **Đánh giá thực nghiệm các pipeline OCR và phân tích cấu trúc PDF cho hệ thống quản trị tri thức tiếng Việt**

Mọi số trong bài phải truy được theo chuỗi:

```text
paper table/figure
  -> aggregate result
  -> raw metric result
  -> canonical prediction
  -> raw engine output
  -> source PDF + checksum
  -> public annotation + checksum
```

## 15. Executive summary và khuyến nghị

Executive summary không tuyên bố một công cụ thắng toàn diện. Nó dùng decision matrix:

| Tình huống | Cách chọn |
|---|---|
| PDF scan nhiều chữ | CER/WER tốt, coverage cao, fail thấp |
| Bảng phức tạp | TEDS-Struct và Cell F1 tốt |
| CPU-only | Profile nằm trên accuracy-speed Pareto frontier |
| Throughput lớn | Profile nhanh nhất trong nhóm chất lượng chấp nhận được |
| Tài liệu hỗn hợp | Coverage và scan robustness cao |
| Tài nguyên hạn chế | RSS thấp với mức giảm chất lượng được định lượng |

Mỗi khuyến nghị phải nêu engine profile, bằng chứng metric, confidence interval, đánh đổi và phạm vi dataset hỗ trợ kết luận.

## 16. Rủi ro và biện pháp kiểm soát

| Rủi ro | Biện pháp |
|---|---|
| Dataset công khai không đại diện tài liệu Sovereign | Công bố domain gap; không ngoại suy quá phạm vi mẫu |
| Dataset thiếu tiếng Việt hoặc thiếu text GT | Metric tương ứng trả N/A; không tự chế nhãn |
| Ground truth có lỗi | Audit phân tầng và correction overlay có bằng chứng |
| Adapter làm sai tọa độ/schema | Known-coordinate, overlay và real-engine tests |
| Engine chạy trên tập tài liệu khác nhau | Common-set tables và coverage bắt buộc |
| Loại failure khỏi trung bình làm đẹp kết quả | Báo cả conditional và end-to-end quality |
| Tuning trên test set | Khóa profile trước lượt chạy công bố; tách calibration/test nếu dataset cho phép |
| Thay đổi phiên bản engine/model | Version lock, model ID/hash và config fingerprint |
| Metric không phân biệt được chất lượng | Positive/negative/intermediate controls và sabotage gate |

## 17. Tiêu chí nghiệm thu thiết kế

- Có đủ tám engine profile hoặc giải thích `N/A` có bằng chứng cho profile không thể chạy.
- Dataset manifest chứa nguồn, version, license và checksum.
- Không metric nào dùng ground truth suy từ engine đang được chấm.
- Prediction giữ raw artifact và canonical representation.
- Mọi comparison chính dùng common set và paired statistics.
- Mọi metric chính qua control, property và sabotage tests.
- Báo cáo đủ `n`, coverage, fail rate và confidence interval.
- Có bảng riêng cho OCR, layout, reading order, bảng, scan robustness và hiệu năng.
- Có phân tích lỗi thủ công và correction log.
- Executive summary đưa khuyến nghị theo tình huống, không dùng overall score.
- Mọi số trong bài truy ngược được tới prediction, PDF và annotation nguồn.

## 18. Trình tự triển khai đề xuất

1. Khóa canonical schema và prediction schema mới.
2. Xây manifest hợp nhất cho dataset công khai.
3. Bổ sung `docling_default` và `docling_scan` adapters.
4. Tách OpenDataLoader, Marker và Sovereign thành profile mặc định/scan.
5. Viết adapter validation và raw-to-canonical trace tests.
6. Hoàn thiện metric controls và sabotage suite.
7. Chạy calibration để khóa cấu hình `scan_optimized`.
8. Chạy common-set predictions và lưu raw artifacts.
9. Chấm metric, bootstrap, significance và effect size.
10. Audit thủ công, phân loại failure và áp correction overlay nếu có bằng chứng.
11. Chạy lại phần bị ảnh hưởng, đóng băng results.
12. Sinh bảng, biểu đồ, bài báo và executive summary từ dữ liệu đã đóng băng.


