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
