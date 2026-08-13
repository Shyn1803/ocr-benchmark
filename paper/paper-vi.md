# Báo cáo Nghiên cứu So sánh Đánh giá Hiệu năng các Công cụ OCR và Phân tích Bố cục Tài liệu

**Tác giả:** Đội ngũ Nghiên cứu Sovereign  
**Ngày công bố:** 2026-08-07  
**Số engine hiển thị:** 7  
**Số metric:** 19  
**Tổng dự đoán:** 7884  

---

## Tóm tắt

Báo cáo này công bố kết quả đánh giá thực nghiệm trên **7 cấu hình engine** với **19 metric** chuẩn hóa, phân chia thành các nhóm năng lực: OCR, Layout, Bảng, Reading Order, Robustness và Hiệu năng.

Mọi kết quả được tính toán tất định từ dữ liệu dự đoán đã đóng băng tại `prediction/` và nhãn chuẩn tại `ground-truth/`. Không sử dụng LLM trong bất kỳ công đoạn tính toán số liệu nào. Các ô hiển thị `— (0 hỏng, 0 chấm được)` là những profile chưa có đủ dữ liệu.

---

## Cảnh báo khi Đọc Bảng

- `marker` chỉ có 27/1608 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- `sovereign_full` chỉ có 2/1608 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- Giao của cả 7 engine là 1 tài liệu. Bảng gộp toàn bộ KHÔNG phải một phép so sánh — xem `common_set.md`.

---

## 1. Phân tích theo Từng Năng lực

Báo cáo không dùng một điểm tổng duy nhất để tránh che khuất trade-off giữa các năng lực.

### Năng lực: Text & OCR

<!-- trace: aggregate:text_ocr:marker -->
<!-- trace: aggregate:text_ocr:noop -->
<!-- trace: aggregate:text_ocr:opendataloader -->
<!-- trace: aggregate:text_ocr:pdf_inspector -->
<!-- trace: aggregate:text_ocr:sabotage -->
<!-- trace: aggregate:text_ocr:sovereign_full -->
<!-- trace: aggregate:text_ocr:sovereign_light -->

| Metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_full | sovereign_light |
|---|---|---|---|---|---|---|---|
| **n (tài liệu)** | 27 | 1424 | 1608 | 1608 | 1608 | 2 | 1607 |
| `cer` | chưa có nhãn (27 tài liệu) | chưa có nhãn (1424 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (2 tài liệu) | chưa có nhãn (1419 tài liệu) |
| `wer` | chưa có nhãn (27 tài liệu) | chưa có nhãn (1424 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (2 tài liệu) | chưa có nhãn (1419 tài liệu) |
| `diacritics_acc` | chưa có nhãn (27 tài liệu) | chưa có nhãn (1424 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (2 tài liệu) | chưa có nhãn (1419 tài liệu) |
| `assert_text_presence` | 0.375 (fail 0%) | 0.000 (fail 0%) | 0.130 (fail 0%) | 0.076 (fail 0%) | 0.059 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.074 (fail 83%) |
| `assert_text_absence` | 1.000 (fail 0%) | 1.000 (fail 0%) | 0.459 (fail 0%) | 0.628 (fail 0%) | 0.756 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.248 (fail 43%) |


### Năng lực: Layout & Structure

<!-- trace: aggregate:layout_structure:marker -->
<!-- trace: aggregate:layout_structure:noop -->
<!-- trace: aggregate:layout_structure:opendataloader -->
<!-- trace: aggregate:layout_structure:pdf_inspector -->
<!-- trace: aggregate:layout_structure:sabotage -->
<!-- trace: aggregate:layout_structure:sovereign_full -->
<!-- trace: aggregate:layout_structure:sovereign_light -->

| Metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_full | sovereign_light |
|---|---|---|---|---|---|---|---|
| **n (tài liệu)** | 27 | 1424 | 1608 | 1608 | 1608 | 2 | 1607 |
| `block_f1` | 0.778 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.609 (fail 0%) | 0.181 (fail 0%) | 0.077 (fail 0%) | N/A | N/A |
| `type_f1` | 0.762 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.273 (fail 0%) | 0.055 (fail 0%) | 0.043 (fail 0%) | N/A | N/A |
| `heading` | chưa có nhãn (7 tài liệu) | chưa có nhãn (1 tài liệu) | 0.561 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.000 (fail 0%) | N/A | N/A |
| `img_f1` | 0.867 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.365 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.145 (fail 0%) | N/A | N/A |
| `img_iou` | 0.664 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.313 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.091 (fail 0%) | N/A | N/A |


### Năng lực: Tables

<!-- trace: aggregate:tables:marker -->
<!-- trace: aggregate:tables:noop -->
<!-- trace: aggregate:tables:opendataloader -->
<!-- trace: aggregate:tables:pdf_inspector -->
<!-- trace: aggregate:tables:sabotage -->
<!-- trace: aggregate:tables:sovereign_full -->
<!-- trace: aggregate:tables:sovereign_light -->

| Metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_full | sovereign_light |
|---|---|---|---|---|---|---|---|
| **n (tài liệu)** | 27 | 1424 | 1608 | 1608 | 1608 | 2 | 1607 |
| `teds` | chưa có nhãn (27 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | N/A | N/A |
| `teds_struct` | chưa có nhãn (27 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | N/A | N/A |
| `cell_f1` | 0.000 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.000 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.000 (fail 0%) | N/A | N/A |
| `table_recall` | chưa có nhãn (27 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | N/A | N/A |
| `assert_table_relation` | 1.000 (fail 0%) | 0.000 (fail 0%) | 0.310 (fail 0%) | 0.405 (fail 0%) | 0.000 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.002 (fail 52%) |


### Năng lực: Reading Order

<!-- trace: aggregate:reading_order:marker -->
<!-- trace: aggregate:reading_order:noop -->
<!-- trace: aggregate:reading_order:opendataloader -->
<!-- trace: aggregate:reading_order:pdf_inspector -->
<!-- trace: aggregate:reading_order:sabotage -->
<!-- trace: aggregate:reading_order:sovereign_full -->
<!-- trace: aggregate:reading_order:sovereign_light -->

| Metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_full | sovereign_light |
|---|---|---|---|---|---|---|---|
| **n (tài liệu)** | 27 | 1424 | 1608 | 1608 | 1608 | 2 | 1607 |
| `nid` | chưa có nhãn (27 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | N/A | N/A |
| `assert_reading_order` | 0.500 (fail 0%) | 0.000 (fail 0%) | 0.408 (fail 0%) | 0.202 (fail 0%) | 0.091 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.108 (fail 46%) |


### Năng lực: Robustness & Base

<!-- trace: aggregate:robustness_base:marker -->
<!-- trace: aggregate:robustness_base:noop -->
<!-- trace: aggregate:robustness_base:opendataloader -->
<!-- trace: aggregate:robustness_base:pdf_inspector -->
<!-- trace: aggregate:robustness_base:sabotage -->
<!-- trace: aggregate:robustness_base:sovereign_full -->
<!-- trace: aggregate:robustness_base:sovereign_light -->

| Metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_full | sovereign_light |
|---|---|---|---|---|---|---|---|
| **n (tài liệu)** | 27 | 1424 | 1608 | 1608 | 1608 | 2 | 1607 |
| `assert_baseline` | chưa có nhãn (27 tài liệu) | 0.000 (fail 0%) | 1.000 (fail 0%) | 0.444 (fail 0%) | 1.000 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.036 (fail 96%) |
| `assert_math_presence` | 0.611 (fail 0%) | 0.000 (fail 0%) | 0.002 (fail 0%) | 0.000 (fail 0%) | 0.001 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.002 (fail 26%) |


---

## 2. Bảng Tổng quan Toàn bộ Metric

<!-- trace: aggregate:all_metrics:marker -->
<!-- trace: aggregate:all_metrics:noop -->
<!-- trace: aggregate:all_metrics:opendataloader -->
<!-- trace: aggregate:all_metrics:pdf_inspector -->
<!-- trace: aggregate:all_metrics:sabotage -->
<!-- trace: aggregate:all_metrics:sovereign_full -->
<!-- trace: aggregate:all_metrics:sovereign_light -->

| metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_full | sovereign_light |
|---|---|---|---|---|---|---|---|
| **n (tài liệu)** | 27 | 1424 | 1608 | 1608 | 1608 | 2 | 1607 |
| assert_baseline | chưa có nhãn (27 tài liệu) | 0.000 (fail 0%) | 1.000 (fail 0%) | 0.444 (fail 0%) | 1.000 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.036 (fail 96%) |
| assert_math_presence | 0.611 (fail 0%) | 0.000 (fail 0%) | 0.002 (fail 0%) | 0.000 (fail 0%) | 0.001 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.002 (fail 26%) |
| assert_reading_order | 0.500 (fail 0%) | 0.000 (fail 0%) | 0.408 (fail 0%) | 0.202 (fail 0%) | 0.091 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.108 (fail 46%) |
| assert_table_relation | 1.000 (fail 0%) | 0.000 (fail 0%) | 0.310 (fail 0%) | 0.405 (fail 0%) | 0.000 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.002 (fail 52%) |
| assert_text_absence | 1.000 (fail 0%) | 1.000 (fail 0%) | 0.459 (fail 0%) | 0.628 (fail 0%) | 0.756 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.248 (fail 43%) |
| assert_text_presence | 0.375 (fail 0%) | 0.000 (fail 0%) | 0.130 (fail 0%) | 0.076 (fail 0%) | 0.059 (fail 0%) | chưa có nhãn (2 tài liệu) | 0.074 (fail 83%) |
| block_f1 | 0.778 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.609 (fail 0%) | 0.181 (fail 0%) | 0.077 (fail 0%) | N/A | N/A |
| cell_f1 | 0.000 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.000 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.000 (fail 0%) | N/A | N/A |
| cer | chưa có nhãn (27 tài liệu) | chưa có nhãn (1424 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (2 tài liệu) | chưa có nhãn (1419 tài liệu) |
| diacritics_acc | chưa có nhãn (27 tài liệu) | chưa có nhãn (1424 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (2 tài liệu) | chưa có nhãn (1419 tài liệu) |
| heading | chưa có nhãn (7 tài liệu) | chưa có nhãn (1 tài liệu) | 0.561 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.000 (fail 0%) | N/A | N/A |
| img_f1 | 0.867 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.365 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.145 (fail 0%) | N/A | N/A |
| img_iou | 0.664 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.313 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.091 (fail 0%) | N/A | N/A |
| nid | chưa có nhãn (27 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | N/A | N/A |
| table_recall | chưa có nhãn (27 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | N/A | N/A |
| teds | chưa có nhãn (27 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | N/A | N/A |
| teds_struct | chưa có nhãn (27 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1 tài liệu) | chưa có nhãn (1608 tài liệu) | N/A | N/A |
| type_f1 | 0.762 (fail 0%) | chưa có nhãn (1 tài liệu) | 0.273 (fail 0%) | 0.055 (fail 0%) | 0.043 (fail 0%) | N/A | N/A |
| wer | chưa có nhãn (27 tài liệu) | chưa có nhãn (1424 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (1608 tài liệu) | chưa có nhãn (2 tài liệu) | chưa có nhãn (1419 tài liệu) |

Ô `N/A` = engine không có năng lực để metric chạm tới. `chưa có nhãn` = bộ mẫu chưa có nhãn hợp loại để đối chiếu.

---

## 3. So chéo trên Tập Tài liệu Chung

# So chéo trên tập tài liệu chung

> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.

Mỗi bảng dưới đây chỉ chấm trên tài liệu **mọi engine trong bảng đều có**. Đây là bảng duy nhất mà việc so hai ô cạnh nhau là hợp lệ.

## `opendataloader` × `pdf_inspector` × `sovereign_light`

Tập chung: **1607** tài liệu.

| metric | opendataloader | pdf_inspector | sovereign_light |
|---|---|---|---|
| **n (tài liệu)** | 1607 | 1607 | 1607 |
| assert_baseline | 1.000 (fail 0%) | 0.444 (fail 0%) | 0.036 (fail 96%) |
| assert_math_presence | 0.002 (fail 0%) | 0.000 (fail 0%) | 0.002 (fail 26%) |
| assert_reading_order | 0.408 (fail 0%) | 0.202 (fail 0%) | 0.108 (fail 46%) |
| assert_table_relation | 0.310 (fail 0%) | 0.405 (fail 0%) | 0.002 (fail 52%) |
| assert_text_absence | 0.459 (fail 0%) | 0.628 (fail 0%) | 0.248 (fail 43%) |
| assert_text_presence | 0.130 (fail 0%) | 0.076 (fail 0%) | 0.074 (fail 83%) |
| block_f1 | 0.609 (fail 0%) | 0.181 (fail 0%) | N/A |
| cell_f1 | 0.000 (fail 0%) | N/A | N/A |
| cer | chưa có nhãn (1607 tài liệu) | chưa có nhãn (1607 tài liệu) | chưa có nhãn (1419 tài liệu) |
| diacritics_acc | chưa có nhãn (1607 tài liệu) | chưa có nhãn (1607 tài liệu) | chưa có nhãn (1419 tài liệu) |
| heading | 0.561 (fail 0%) | N/A | N/A |
| img_f1 | 0.365 (fail 0%) | N/A | N/A |
| img_iou | 0.313 (fail 0%) | N/A | N/A |
| nid | chưa có nhãn (1607 tài liệu) | chưa có nhãn (1607 tài liệu) | N/A |
| table_recall | chưa có nhãn (1607 tài liệu) | N/A | N/A |
| teds | chưa có nhãn (1607 tài liệu) | N/A | N/A |
| teds_struct | chưa có nhãn (1607 tài liệu) | N/A | N/A |
| type_f1 | 0.273 (fail 0%) | 0.055 (fail 0%) | N/A |
| wer | chưa có nhãn (1607 tài liệu) | chưa có nhãn (1607 tài liệu) | chưa có nhãn (1419 tài liệu) |

## `opendataloader` × `pdf_inspector` × `sovereign_light` × `marker`

Tập chung: **27** tài liệu.

| metric | opendataloader | pdf_inspector | sovereign_light | marker |
|---|---|---|---|---|
| **n (tài liệu)** | 27 | 27 | 27 | 27 |
| assert_baseline | chưa có nhãn (27 tài liệu) | chưa có nhãn (27 tài liệu) | chưa có nhãn (23 tài liệu) | chưa có nhãn (27 tài liệu) |
| assert_math_presence | 0.000 (fail 0%) | 0.000 (fail 0%) | 0.000 (fail 80%) | 0.611 (fail 0%) |
| assert_reading_order | 0.400 (fail 0%) | 0.200 (fail 0%) | 0.040 (fail 80%) | 0.500 (fail 0%) |
| assert_table_relation | 0.000 (fail 0%) | 0.333 (fail 0%) | 0.000 (fail 80%) | 1.000 (fail 0%) |
| assert_text_absence | 0.750 (fail 0%) | 0.750 (fail 0%) | 0.100 (fail 80%) | 1.000 (fail 0%) |
| assert_text_presence | 0.000 (fail 0%) | 0.000 (fail 0%) | chưa có nhãn (23 tài liệu) | 0.375 (fail 0%) |
| block_f1 | 0.684 (fail 0%) | 0.141 (fail 0%) | N/A | 0.778 (fail 0%) |
| cell_f1 | chưa có nhãn (27 tài liệu) | N/A | N/A | 0.000 (fail 0%) |
| cer | chưa có nhãn (27 tài liệu) | chưa có nhãn (27 tài liệu) | chưa có nhãn (23 tài liệu) | chưa có nhãn (27 tài liệu) |
| diacritics_acc | chưa có nhãn (27 tài liệu) | chưa có nhãn (27 tài liệu) | chưa có nhãn (23 tài liệu) | chưa có nhãn (27 tài liệu) |
| heading | chưa có nhãn (27 tài liệu) | N/A | N/A | chưa có nhãn (7 tài liệu) |
| img_f1 | 0.467 (fail 0%) | N/A | N/A | 0.867 (fail 0%) |
| img_iou | 0.386 (fail 0%) | N/A | N/A | 0.664 (fail 0%) |
| nid | chưa có nhãn (27 tài liệu) | chưa có nhãn (27 tài liệu) | N/A | chưa có nhãn (27 tài liệu) |
| table_recall | chưa có nhãn (27 tài liệu) | N/A | N/A | chưa có nhãn (27 tài liệu) |
| teds | chưa có nhãn (27 tài liệu) | N/A | N/A | chưa có nhãn (27 tài liệu) |
| teds_struct | chưa có nhãn (27 tài liệu) | N/A | N/A | chưa có nhãn (27 tài liệu) |
| type_f1 | 0.339 (fail 0%) | 0.050 (fail 0%) | N/A | 0.762 (fail 0%) |
| wer | chưa có nhãn (27 tài liệu) | chưa có nhãn (27 tài liệu) | chưa có nhãn (23 tài liệu) | chưa có nhãn (27 tài liệu) |

## `noop` × `sabotage`

Tập chung: **1424** tài liệu.

| metric | noop | sabotage |
|---|---|---|
| **n (tài liệu)** | 1424 | 1424 |
| assert_baseline | 0.000 (fail 0%) | 1.000 (fail 0%) |
| assert_math_presence | 0.000 (fail 0%) | 0.001 (fail 0%) |
| assert_reading_order | 0.000 (fail 0%) | 0.091 (fail 0%) |
| assert_table_relation | 0.000 (fail 0%) | 0.000 (fail 0%) |
| assert_text_absence | 1.000 (fail 0%) | 0.756 (fail 0%) |
| assert_text_presence | 0.000 (fail 0%) | 0.059 (fail 0%) |
| block_f1 | chưa có nhãn (1 tài liệu) | 0.063 (fail 0%) |
| cell_f1 | chưa có nhãn (1 tài liệu) | chưa có nhãn (1424 tài liệu) |
| cer | chưa có nhãn (1424 tài liệu) | chưa có nhãn (1424 tài liệu) |
| diacritics_acc | chưa có nhãn (1424 tài liệu) | chưa có nhãn (1424 tài liệu) |
| heading | chưa có nhãn (1 tài liệu) | chưa có nhãn (1424 tài liệu) |
| img_f1 | chưa có nhãn (1 tài liệu) | 0.000 (fail 0%) |
| img_iou | chưa có nhãn (1 tài liệu) | 0.000 (fail 0%) |
| nid | chưa có nhãn (1 tài liệu) | chưa có nhãn (1424 tài liệu) |
| table_recall | chưa có nhãn (1 tài liệu) | chưa có nhãn (1424 tài liệu) |
| teds | chưa có nhãn (1 tài liệu) | chưa có nhãn (1424 tài liệu) |
| teds_struct | chưa có nhãn (1 tài liệu) | chưa có nhãn (1424 tài liệu) |
| type_f1 | chưa có nhãn (1 tài liệu) | 0.033 (fail 0%) |
| wer | chưa có nhãn (1424 tài liệu) | chưa có nhãn (1424 tài liệu) |


---

## Phụ lục A: Phương pháp Đánh giá Chi tiết

## Phụ lục A: Phương pháp Đánh giá Chi tiết

1. **Paired Bootstrap**: Tính toán khoảng tin cậy 95% (95% CI) bằng kỹ thuật resampling 10.000 lần theo từng tài liệu chung (common set).
2. **Kiểm định Wilcoxon**: Kiểm định phi tham số Wilcoxon signed-rank test trên các cặp tài liệu chung để đánh giá sự khác biệt có ý nghĩa thống kê ($p < 0.05$).
3. **Hiệu chỉnh Holm-Bonferroni**: Điều chỉnh p-value khi thực hiện nhiều phép so sánh đồng thời trong cùng một họ năng lực.
4. **Cổng Phá hoại Sabotage**: Mọi metric hạng `main` bắt buộc phải vượt qua kiểm định đơn điệu (monotonicity qualification test) với các mức phá hoại $0.1, 0.3, 0.6$.


## Phụ lục B: Hạn chế Nghiên cứu & Phạm vi Áp dụng

## Phụ lục B: Hạn chế Nghiên cứu & Phạm vi Áp dụng

1. **Bộ Dữ liệu Tiếng Việt**: Các tài liệu tiếng Việt chưa có nhãn chuẩn hóa công khai (ground truth transcript) được gắn nhãn `N/A` hoặc giới hạn phạm vi, tuyệt đối không tạo nhãn giả.
2. **Thứ tự Đọc NID**: Metric `nid` chỉ đánh giá trên các bộ mẫu khai báo thứ tự đọc rõ ràng; trên bộ mẫu DocLayNet, kết quả được đánh dấu `N/A` do thiếu thông tin thứ tự đọc gốc.
3. **Phân lập LLM**: Toàn bộ quá trình tính toán số liệu và đưa ra khuyến nghị được thực hiện tất định bằng mã nguồn Python, không sử dụng LLM tạo số.


