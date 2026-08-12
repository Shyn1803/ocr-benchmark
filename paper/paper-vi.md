# Báo cáo Nghiên cứu So sánh Đánh giá Hiệu năng các Công cụ OCR và Phân tích Bố cục Tài liệu (OCR Parser Benchmark)

**Tác giả:** Đội ngũ Nghiên cứu Sovereign  
**Ngày công bố:** 2026-08-12  
**Phiên bản Benchmark:** v1.0 (catalog version: 1)

---

## Tóm tắt Thực thi (Executive Summary)

Báo cáo này công bố kết quả đánh giá thực nghiệm tái lập được (reproducible benchmark) so sánh 4 họ engine OCR và phân tích cấu trúc tài liệu chính bao gồm **Docling**, **OpenDataLoader**, **Marker** và **Sovereign** trên hai cấu hình (profile) chính: `default` và `scan` (tổng số 8 profile).

Mọi kết quả trong báo cáo này được tổng hợp từ dữ liệu đóng băng, áp dụng các kiểm định thống kê theo cặp (paired bootstrap 10.000 mẫu, kiểm định Wilcoxon signed-rank, hiệu chỉnh Holm-Bonferroni) và tuân thủ nguyên tắc không sử dụng LLM trong bất kỳ công đoạn tính toán số liệu nào.

---

## 1. Phương pháp Đánh giá & Danh mục Metric

<!-- trace: aggregate:text_ocr:marker_scan -->
Chi tiết phương pháp.

---

## 2. Kết quả Đánh giá theo Tầng Năng lực

### 2.1 Nhận dạng Văn bản (Text OCR & Dấu tiếng Việt)

| Profile | CER | WER | Diacritics |
|---|---|---|---|
| marker_scan | 0.05 (fail 0%) | 0.08 (fail 0%) | 0.98 (fail 0%) |


### 2.2 Phân tích Bố cục (Layout Analysis)

| Profile | Block F1 | Type F1 |
|---|---|---|
| marker_scan | 0.88 (fail 0%) | 0.85 (fail 0%) |


### 2.3 Phân tích Bảng (Table Structure)

| Profile | TEDS | TEDS Struct | Cell F1 |
|---|---|---|---|
| marker_scan | 0.92 (fail 0%) | 0.94 (fail 0%) | 0.90 (fail 0%) |


### 2.4 Thứ tự Đọc (Reading Order)

| Profile | Reading Order |
|---|---|
| marker_scan | 0.91 (fail 0%) |


### 2.5 Độ bền bỉ với Tài liệu Scan (Scan Robustness)

| Profile | Digital | Scan | Degradation |
|---|---|---|---|
| marker | 0.95 | 0.91 | -4.2% |


### 2.6 Hiệu năng Xử lý & Tài nguyên (Performance)

| Profile | Warm s/page | Peak RSS (MB) |
|---|---|---|
| marker_scan | 1.25s | 450MB |


---

## 3. Khuyến nghị & Quy tắc Lựa chọn Engine

Bảng khuyến nghị tự động (rule-based recommendation):

<!-- table: recommendations -->

---

## 4. Hạn chế Nghiên cứu & Hướng phát triển

Chi tiết hạn chế.
