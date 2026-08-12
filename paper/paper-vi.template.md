# Báo cáo Nghiên cứu So sánh Đánh giá Hiệu năng các Công cụ OCR và Phân tích Bố cục Tài liệu (OCR Parser Benchmark)

**Tác giả:** Đội ngũ Nghiên cứu Sovereign  
**Ngày công bố:** {{publication_date}}  
**Phiên bản Benchmark:** {{benchmark_version}} (catalog version: {{catalog_version}})

---

## Tóm tắt Thực thi (Executive Summary)

Báo cáo này công bố kết quả đánh giá thực nghiệm tái lập được (reproducible benchmark) so sánh 4 họ engine OCR và phân tích cấu trúc tài liệu chính bao gồm **Docling**, **OpenDataLoader**, **Marker** và **Sovereign** trên hai cấu hình (profile) chính: `default` và `scan` (tổng số 8 profile).

Mọi kết quả trong báo cáo này được tổng hợp từ dữ liệu đóng băng, áp dụng các kiểm định thống kê theo cặp (paired bootstrap 10.000 mẫu, kiểm định Wilcoxon signed-rank, hiệu chỉnh Holm-Bonferroni) và tuân thủ nguyên tắc không sử dụng LLM trong bất kỳ công đoạn tính toán số liệu nào.

---

## 1. Phương pháp Đánh giá & Danh mục Metric

{{methods_appendix}}

---

## 2. Kết quả Đánh giá theo Tầng Năng lực

### 2.1 Nhận dạng Văn bản (Text OCR & Dấu tiếng Việt)

<!-- table: text-ocr -->

### 2.2 Phân tích Bố cục (Layout Analysis)

<!-- table: layout -->

### 2.3 Phân tích Bảng (Table Structure)

<!-- table: tables -->

### 2.4 Thứ tự Đọc (Reading Order)

<!-- table: reading-order -->

### 2.5 Độ bền bỉ với Tài liệu Scan (Scan Robustness)

<!-- table: scan-robustness -->

### 2.6 Hiệu năng Xử lý & Tài nguyên (Performance)

<!-- table: performance -->

---

## 3. Khuyến nghị & Quy tắc Lựa chọn Engine

Bảng khuyến nghị tự động (rule-based recommendation):

<!-- table: recommendations -->

---

## 4. Hạn chế Nghiên cứu & Hướng phát triển

{{limitations_appendix}}
