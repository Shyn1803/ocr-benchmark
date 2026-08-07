# Bảng tổng quan — mọi engine, mọi tài liệu

> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.

## Đọc bảng này thế nào

Mỗi engine chạy trên một tập tài liệu **khác nhau** (xem dòng `n`). Đặt hai ô cạnh nhau rồi kết luận cái nào hơn là **sai** trừ khi hai engine có cùng `n` trên cùng tập. Bảng so chéo hợp lệ nằm ở `common_set.md`.

### Cảnh báo

- `marker` chỉ có 20/205 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- `noop` chỉ có 41/205 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- `sabotage` chỉ có 41/205 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- `sovereign_full` chỉ có 2/205 tài liệu — không so ngang hàng được với engine chạy đủ bộ.
- Giao của cả 7 engine là 1 tài liệu. Bảng gộp toàn bộ KHÔNG phải một phép so sánh — xem `common_set.md`.

## Bảng

| metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_full | sovereign_light |
|---|---|---|---|---|---|---|---|
| **n (tài liệu)** | 20 | 41 | 205 | 205 | 41 | 2 | 204 |
| assert_baseline | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| assert_math_presence | N/A | 0.000 (fail 0%) | N/A | N/A | 0.000 (fail 0%) | N/A | — (10 hỏng, 0 chấm được) |
| assert_reading_order | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| assert_table_relation | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| assert_text_absence | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| assert_text_presence | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| cer | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| heading | N/A | N/A | 0.561 (fail 0%) | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| img_f1 | 0.667 (fail 0%) | N/A | 0.355 (fail 0%) | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| img_iou | 0.508 (fail 0%) | N/A | 0.303 (fail 0%) | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| nid | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| teds | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| teds_struct | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |
| wer | N/A | N/A | N/A | N/A | N/A | N/A | — (10 hỏng, 0 chấm được) |

Ô `N/A` = engine không có năng lực để metric chạm tới. Nó **không** phải 0 và dòng của nó **không** bị bỏ đi.
