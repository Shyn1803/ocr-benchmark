# Báo cáo Nghiên cứu So sánh Đánh giá Hiệu năng các Công cụ OCR và Phân tích Bố cục Tài liệu

**Tác giả:** Đội ngũ Nghiên cứu Sovereign  
**Ngày công bố:** 2026-08-17  
**Số engine hiển thị:** 4  
**Số metric:** 19  
**Tổng dự đoán:** 3771  

---

## Tóm tắt

Báo cáo này công bố kết quả đánh giá thực nghiệm trên **4 cấu hình engine** với **19 metric** chuẩn hóa, phân chia thành các nhóm năng lực: OCR, Layout, Bảng, Reading Order, Robustness và Hiệu năng.

Mọi kết quả được tính toán tất định từ dữ liệu dự đoán đã đóng băng tại `prediction/` và nhãn chuẩn tại `ground-truth/`. Không sử dụng LLM trong bất kỳ công đoạn tính toán số liệu nào. Các ô hiển thị `— (0 hỏng, 0 chấm được)` là những profile chưa có đủ dữ liệu.

---

## Cảnh báo khi Đọc Bảng

- `docling_scan` chỉ có 203/1606 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- `opendataloader_scan` chỉ có 356/1606 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- Giao của cả 4 engine là 203 tài liệu. Bảng gộp toàn bộ KHÔNG phải một phép so sánh — xem `common_set.md`.

---

## 1. Phân tích theo Từng Năng lực

Báo cáo không dùng một điểm tổng duy nhất để tránh che khuất trade-off giữa các năng lực.

### Năng lực: Text & OCR

<!-- trace: aggregate:text_ocr:docling_default -->
<!-- trace: aggregate:text_ocr:docling_scan -->
<!-- trace: aggregate:text_ocr:opendataloader_default -->
<!-- trace: aggregate:text_ocr:opendataloader_scan -->

| Metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 1606 | 203 | 1606 | 356 |
| `cer` | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| `wer` | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| `diacritics_acc` | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| `assert_text_presence` | 0.156 (fail 6%) | chưa có nhãn (203 tài liệu) | 0.130 (fail 0%) | chưa có nhãn (356 tài liệu) |
| `assert_text_absence` | 0.910 (fail 3%) | chưa có nhãn (203 tài liệu) | 0.459 (fail 0%) | 0.801 (fail 0%) |


### Năng lực: Layout & Structure

<!-- trace: aggregate:layout_structure:docling_default -->
<!-- trace: aggregate:layout_structure:docling_scan -->
<!-- trace: aggregate:layout_structure:opendataloader_default -->
<!-- trace: aggregate:layout_structure:opendataloader_scan -->

| Metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 1606 | 203 | 1606 | 356 |
| `block_f1` | 0.749 (fail 5%) | 0.735 (fail 0%) | 0.609 (fail 0%) | 0.637 (fail 0%) |
| `type_f1` | 0.514 (fail 5%) | 0.516 (fail 0%) | 0.273 (fail 0%) | 0.370 (fail 0%) |
| `heading` | 0.125 (fail 42%) | 0.195 (fail 0%) | 0.561 (fail 0%) | 0.195 (fail 0%) |
| `img_f1` | 0.716 (fail 14%) | 0.828 (fail 0%) | 0.365 (fail 0%) | 0.785 (fail 0%) |
| `img_iou` | 0.672 (fail 14%) | 0.777 (fail 0%) | 0.313 (fail 0%) | 0.708 (fail 0%) |


### Năng lực: Tables

<!-- trace: aggregate:tables:docling_default -->
<!-- trace: aggregate:tables:docling_scan -->
<!-- trace: aggregate:tables:opendataloader_default -->
<!-- trace: aggregate:tables:opendataloader_scan -->

| Metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 1606 | 203 | 1606 | 356 |
| `teds` | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| `teds_struct` | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| `cell_f1` | 0.000 (fail 22%) | 0.000 (fail 0%) | 0.000 (fail 0%) | 0.000 (fail 0%) |
| `table_recall` | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| `assert_table_relation` | 0.606 (fail 6%) | chưa có nhãn (203 tài liệu) | 0.310 (fail 0%) | 0.490 (fail 0%) |


### Năng lực: Reading Order

<!-- trace: aggregate:reading_order:docling_default -->
<!-- trace: aggregate:reading_order:docling_scan -->
<!-- trace: aggregate:reading_order:opendataloader_default -->
<!-- trace: aggregate:reading_order:opendataloader_scan -->

| Metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 1606 | 203 | 1606 | 356 |
| `nid` | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| `assert_reading_order` | 0.297 (fail 3%) | chưa có nhãn (203 tài liệu) | 0.408 (fail 0%) | 0.456 (fail 0%) |


### Năng lực: Robustness & Base

<!-- trace: aggregate:robustness_base:docling_default -->
<!-- trace: aggregate:robustness_base:docling_scan -->
<!-- trace: aggregate:robustness_base:opendataloader_default -->
<!-- trace: aggregate:robustness_base:opendataloader_scan -->

| Metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 1606 | 203 | 1606 | 356 |
| `assert_baseline` | 0.450 (fail 55%) | chưa có nhãn (203 tài liệu) | 1.000 (fail 0%) | chưa có nhãn (356 tài liệu) |
| `assert_math_presence` | 0.001 (fail 2%) | chưa có nhãn (203 tài liệu) | 0.002 (fail 0%) | chưa có nhãn (356 tài liệu) |


---

## 2. Bảng Tổng quan Toàn bộ Metric

<!-- trace: aggregate:all_metrics:docling_default -->
<!-- trace: aggregate:all_metrics:docling_scan -->
<!-- trace: aggregate:all_metrics:opendataloader_default -->
<!-- trace: aggregate:all_metrics:opendataloader_scan -->

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 1606 | 203 | 1606 | 356 |
| assert_baseline | 0.450 (fail 55%) | chưa có nhãn (203 tài liệu) | 1.000 (fail 0%) | chưa có nhãn (356 tài liệu) |
| assert_math_presence | 0.001 (fail 2%) | chưa có nhãn (203 tài liệu) | 0.002 (fail 0%) | chưa có nhãn (356 tài liệu) |
| assert_reading_order | 0.297 (fail 3%) | chưa có nhãn (203 tài liệu) | 0.408 (fail 0%) | 0.456 (fail 0%) |
| assert_table_relation | 0.606 (fail 6%) | chưa có nhãn (203 tài liệu) | 0.310 (fail 0%) | 0.490 (fail 0%) |
| assert_text_absence | 0.910 (fail 3%) | chưa có nhãn (203 tài liệu) | 0.459 (fail 0%) | 0.801 (fail 0%) |
| assert_text_presence | 0.156 (fail 6%) | chưa có nhãn (203 tài liệu) | 0.130 (fail 0%) | chưa có nhãn (356 tài liệu) |
| block_f1 | 0.749 (fail 5%) | 0.735 (fail 0%) | 0.609 (fail 0%) | 0.637 (fail 0%) |
| cell_f1 | 0.000 (fail 22%) | 0.000 (fail 0%) | 0.000 (fail 0%) | 0.000 (fail 0%) |
| cer | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| diacritics_acc | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| heading | 0.125 (fail 42%) | 0.195 (fail 0%) | 0.561 (fail 0%) | 0.195 (fail 0%) |
| img_f1 | 0.716 (fail 14%) | 0.828 (fail 0%) | 0.365 (fail 0%) | 0.785 (fail 0%) |
| img_iou | 0.672 (fail 14%) | 0.777 (fail 0%) | 0.313 (fail 0%) | 0.708 (fail 0%) |
| nid | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| table_recall | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| teds | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| teds_struct | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |
| type_f1 | 0.514 (fail 5%) | 0.516 (fail 0%) | 0.273 (fail 0%) | 0.370 (fail 0%) |
| wer | chưa có nhãn (1595 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (1606 tài liệu) | chưa có nhãn (356 tài liệu) |

Ô `N/A` = engine không có năng lực để metric chạm tới. `chưa có nhãn` = bộ mẫu chưa có nhãn hợp loại để đối chiếu.

---

## 3. So chéo trên Tập Tài liệu Chung

# So chéo trên tập tài liệu chung

> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.

Mỗi bảng dưới đây chỉ chấm trên tài liệu **mọi engine trong bảng đều có**. Đây là bảng duy nhất mà việc so hai ô cạnh nhau là hợp lệ.

## `opendataloader` × `pdf_inspector` × `sovereign_light`

Bỏ qua — không có dự đoán của: `opendataloader`, `pdf_inspector`, `sovereign_light`.

## `opendataloader` × `pdf_inspector` × `sovereign_light` × `marker`

Bỏ qua — không có dự đoán của: `opendataloader`, `pdf_inspector`, `sovereign_light`, `marker`.

## `noop` × `sabotage`

Bỏ qua — không có dự đoán của: `noop`, `sabotage`.


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


