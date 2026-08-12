# Bảng tổng quan — mọi engine, mọi tài liệu

> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.

## Đọc bảng này thế nào

Mỗi engine chạy trên một tập tài liệu **khác nhau** (xem dòng `n`). Đặt hai ô cạnh nhau rồi kết luận cái nào hơn là **sai** trừ khi hai engine có cùng `n` trên cùng tập. Bảng so chéo hợp lệ nằm ở `common_set.md`.

### Cảnh báo

- `marker` chỉ có 27/1608 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- `sovereign_full` chỉ có 2/1608 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- Giao của cả 7 engine là 1 tài liệu. Bảng gộp toàn bộ KHÔNG phải một phép so sánh — xem `common_set.md`.

## Bảng

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

Ô `N/A` = engine không có năng lực để metric chạm tới. Nó **không** phải 0 và dòng của nó **không** bị bỏ đi.
