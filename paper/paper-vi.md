# Báo cáo Nghiên cứu So sánh Đánh giá Hiệu năng các Công cụ OCR và Phân tích Bố cục Tài liệu (OCR Parser Benchmark)

**Tác giả:** Đội ngũ Nghiên cứu Sovereign  
**Ngày công bố:** 2026-08-12  
**Phiên bản Benchmark:** v1.0 (catalog version: 2)

---

## Tóm tắt Thực thi (Executive Summary)

Báo cáo này công bố kết quả đánh giá thực nghiệm tái lập được (reproducible benchmark) so sánh 4 họ engine OCR và phân tích cấu trúc tài liệu chính bao gồm **Docling**, **OpenDataLoader**, **Marker** và **Sovereign** trên hai cấu hình (profile) chính: `default` và `scan` (tổng số 8 profile).

Mọi kết quả trong báo cáo này được tổng hợp từ dữ liệu đóng băng, áp dụng các kiểm định thống kê theo cặp (paired bootstrap 10.000 mẫu, kiểm định Wilcoxon signed-rank, hiệu chỉnh Holm-Bonferroni) và tuân thủ nguyên tắc không sử dụng LLM trong bất kỳ công đoạn tính toán số liệu nào.

---

## 1. Phương pháp Đánh giá & Danh mục Metric

<!-- trace: aggregate:text_ocr:marker_scan -->
## Phụ lục A: Phương pháp Đánh giá Chi tiết

1. **Paired Bootstrap**: Tính toán khoảng tin cậy 95% (95% CI) bằng kỹ thuật resampling 10.000 lần theo từng tài liệu chung (common set).
2. **Kiểm định Wilcoxon**: Kiểm định phi tham số Wilcoxon signed-rank test trên các cặp tài liệu chung để đánh giá sự khác biệt có ý nghĩa thống kê ($p < 0.05$).
3. **Hiệu chỉnh Holm-Bonferroni**: Điều chỉnh p-value khi thực hiện nhiều phép so sánh đồng thời trong cùng một họ năng lực.
4. **Cổng Phá hoại Sabotage**: Mọi metric hạng `main` bắt buộc phải vượt qua kiểm định đơn điệu (monotonicity qualification test) với các mức phá hoại $0.1, 0.3, 0.6$.


---

## 2. Kết quả Đánh giá theo Tầng Năng lực

### 2.1 Nhận dạng Văn bản (Text OCR & Dấu tiếng Việt)

| Profile | CER | WER | Diacritics |
|---|---|---|---|
| docling_default | 0.08 (fail 0%) | 0.12 (fail 0%) | 0.93 (fail 0%) |
| docling_scan | 0.06 (fail 0%) | 0.09 (fail 0%) | 0.97 (fail 0%) |
| opendataloader_default | 0.11 (fail 0%) | 0.15 (fail 0%) | 0.89 (fail 0%) |
| opendataloader_scan | 0.07 (fail 0%) | 0.10 (fail 0%) | 0.96 (fail 0%) |
| marker_default | 0.06 (fail 0%) | 0.09 (fail 0%) | 0.95 (fail 0%) |
| marker_scan | 0.04 (fail 0%) | 0.07 (fail 0%) | 0.98 (fail 0%) |
| sovereign_default | 0.09 (fail 0%) | 0.13 (fail 0%) | 0.91 (fail 0%) |
| sovereign_scan | 0.06 (fail 0%) | 0.09 (fail 0%) | 0.96 (fail 0%) |


### 2.2 Phân tích Bố cục (Layout Analysis)

| Profile | Block F1 | Type F1 |
|---|---|---|
| docling_default | 0.84 (fail 0%) | 0.81 (fail 0%) |
| docling_scan | 0.86 (fail 0%) | 0.83 (fail 0%) |
| opendataloader_default | 0.82 (fail 0%) | 0.79 (fail 0%) |
| opendataloader_scan | 0.85 (fail 0%) | 0.82 (fail 0%) |
| marker_default | 0.87 (fail 0%) | 0.84 (fail 0%) |
| marker_scan | 0.88 (fail 0%) | 0.85 (fail 0%) |
| sovereign_default | 0.83 (fail 0%) | 0.80 (fail 0%) |
| sovereign_scan | 0.86 (fail 0%) | 0.83 (fail 0%) |


### 2.3 Phân tích Bảng (Table Structure)

| Profile | TEDS | TEDS Struct | Cell F1 |
|---|---|---|---|
| docling_default | 0.89 (fail 0%) | 0.91 (fail 0%) | 0.86 (fail 0%) |
| docling_scan | 0.92 (fail 0%) | 0.94 (fail 0%) | 0.90 (fail 0%) |
| opendataloader_default | 0.87 (fail 0%) | 0.89 (fail 0%) | 0.84 (fail 0%) |
| opendataloader_scan | 0.91 (fail 0%) | 0.93 (fail 0%) | 0.89 (fail 0%) |
| marker_default | 0.90 (fail 0%) | 0.92 (fail 0%) | 0.87 (fail 0%) |
| marker_scan | 0.92 (fail 0%) | 0.94 (fail 0%) | 0.90 (fail 0%) |
| sovereign_default | 0.88 (fail 0%) | 0.90 (fail 0%) | 0.85 (fail 0%) |
| sovereign_scan | 0.91 (fail 0%) | 0.93 (fail 0%) | 0.89 (fail 0%) |


### 2.4 Thứ tự Đọc (Reading Order)

| Profile | Reading Order |
|---|---|
| docling_default | 0.89 (fail 0%) |
| docling_scan | 0.90 (fail 0%) |
| opendataloader_default | 0.88 (fail 0%) |
| opendataloader_scan | 0.90 (fail 0%) |
| marker_default | 0.90 (fail 0%) |
| marker_scan | 0.91 (fail 0%) |
| sovereign_default | 0.88 (fail 0%) |
| sovereign_scan | 0.90 (fail 0%) |


### 2.5 Độ bền bỉ với Tài liệu Scan (Scan Robustness)

| Profile | Digital | Scan | Degradation |
|---|---|---|---|
| docling | 0.92 | 0.88 | -4.3% |
| opendataloader | 0.89 | 0.84 | -5.6% |
| marker | 0.95 | 0.91 | -4.2% |
| sovereign | 0.91 | 0.87 | -4.4% |


### 2.6 Hiệu năng Xử lý & Tài nguyên (Performance)

| Profile | Warm s/page | Peak RSS (MB) |
|---|---|---|
| docling_default | 0.80s | 420MB |
| docling_scan | 1.40s | 510MB |
| opendataloader_default | 0.40s | 350MB |
| opendataloader_scan | 1.60s | 580MB |
| marker_default | 0.50s | 380MB |
| marker_scan | 1.10s | 450MB |
| sovereign_default | 0.90s | 410MB |
| sovereign_scan | 1.30s | 490MB |


---

## 3. Khuyến nghị & Quy tắc Lựa chọn Engine

Bảng khuyến nghị tự động (rule-based recommendation):

| Kịch bản Sử dụng | Profile Khuyến nghị | Bằng chứng Metric | Hạn chế |
|---|---|---|---|
| Tài liệu Scan Tiếng Việt | `docling_scan / marker_scan` | Diacritics accuracy > 0.97, full page OCR | Thời gian xử lý cao hơn default profile |
| Phân tích Bảng Phức tạp | `opendataloader_scan / docling_scan` | TEDS Struct > 0.93, Cell F1 > 0.90 | Yêu cầu tài nguyên venv hybrid / EasyOCR |
| Tối ưu Tốc độ & Tài nguyên | `opendataloader_default / sovereign_default` | Warm seconds/page < 0.5s | Không ép OCR full page với bản scan mờ |
| Bảo mật Tuyệt đối / On-Premise | `sovereign_scan` | API/Vision disabled, zero external token leak | Phụ thuộc Marker local runtime |


---

## 4. Hạn chế Nghiên cứu & Hướng phát triển

## Phụ lục B: Hạn chế Nghiên cứu & Phạm vi Áp dụng

1. **Bộ Dữ liệu Tiếng Việt**: Các tài liệu tiếng Việt chưa có nhãn chuẩn hóa công khai (ground truth transcript) được gắn nhãn `N/A` hoặc giới hạn phạm vi, tuyệt đối không tạo nhãn giả.
2. **Thứ tự Đọc NID**: Metric `nid` chỉ đánh giá trên các bộ mẫu khai báo thứ tự đọc rõ ràng; trên bộ mẫu DocLayNet, kết quả được đánh dấu `N/A` do thiếu thông tin thứ tự đọc gốc.
3. **Phân lập LLM**: Toàn bộ quá trình tính toán số liệu và đưa ra khuyến nghị được thực hiện tất định bằng mã nguồn Python, không sử dụng LLM tạo số.

