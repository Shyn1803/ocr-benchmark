# Bảng tổng quan — mọi engine, mọi tài liệu

> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.

## Đọc bảng này thế nào

Mỗi engine chạy trên một tập tài liệu **khác nhau** (xem dòng `n`). Đặt hai ô cạnh nhau rồi kết luận cái nào hơn là **sai** trừ khi hai engine có cùng `n` trên cùng tập. Bảng so chéo hợp lệ nằm ở `common_set.md`.

### Cảnh báo

- `docling_scan` chỉ có 203/1606 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- `opendataloader_scan` chỉ có 356/1606 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- Giao của cả 4 engine là 203 tài liệu. Bảng gộp toàn bộ KHÔNG phải một phép so sánh — xem `common_set.md`.

## Bảng

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

Ô `N/A` = engine không có năng lực để metric chạm tới. Nó **không** phải 0 và dòng của nó **không** bị bỏ đi.
