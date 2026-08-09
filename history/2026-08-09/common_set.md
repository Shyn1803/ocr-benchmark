# So chéo trên tập tài liệu chung

> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.

Mỗi bảng dưới đây chỉ chấm trên tài liệu **mọi engine trong bảng đều có**. Đây là bảng duy nhất mà việc so hai ô cạnh nhau là hợp lệ.

## `opendataloader` × `pdf_inspector` × `sovereign_light`

Tập chung: **204** tài liệu.

| metric | opendataloader | pdf_inspector | sovereign_light |
|---|---|---|---|
| **n (tài liệu)** | 204 | 204 | 204 |
| assert_baseline | N/A | N/A | — (10 hỏng, 0 chấm được) |
| assert_math_presence | N/A | N/A | — (10 hỏng, 0 chấm được) |
| assert_reading_order | N/A | N/A | — (10 hỏng, 0 chấm được) |
| assert_table_relation | N/A | N/A | — (10 hỏng, 0 chấm được) |
| assert_text_absence | N/A | N/A | — (10 hỏng, 0 chấm được) |
| assert_text_presence | N/A | N/A | — (10 hỏng, 0 chấm được) |
| cer | N/A | N/A | — (10 hỏng, 0 chấm được) |
| heading | 0.561 (fail 0%) | N/A | — (10 hỏng, 0 chấm được) |
| img_f1 | 0.365 (fail 0%) | N/A | — (10 hỏng, 0 chấm được) |
| img_iou | 0.313 (fail 0%) | N/A | — (10 hỏng, 0 chấm được) |
| nid | N/A | N/A | — (10 hỏng, 0 chấm được) |
| teds | N/A | N/A | — (10 hỏng, 0 chấm được) |
| teds_struct | N/A | N/A | — (10 hỏng, 0 chấm được) |
| wer | N/A | N/A | — (10 hỏng, 0 chấm được) |

## `opendataloader` × `pdf_inspector` × `sovereign_light` × `marker`

Tập chung: **20** tài liệu.

| metric | opendataloader | pdf_inspector | sovereign_light | marker |
|---|---|---|---|---|
| **n (tài liệu)** | 20 | 20 | 20 | 20 |
| assert_baseline | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| assert_math_presence | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| assert_reading_order | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| assert_table_relation | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| assert_text_absence | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| assert_text_presence | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| cer | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| heading | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| img_f1 | 0.467 (fail 0%) | N/A | — (1 hỏng, 0 chấm được) | 0.867 (fail 0%) |
| img_iou | 0.386 (fail 0%) | N/A | — (1 hỏng, 0 chấm được) | 0.664 (fail 0%) |
| nid | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| teds | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| teds_struct | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |
| wer | N/A | N/A | — (1 hỏng, 0 chấm được) | N/A |

## `noop` × `sabotage`

Tập chung: **21** tài liệu.

| metric | noop | sabotage |
|---|---|---|
| **n (tài liệu)** | 21 | 21 |
| assert_baseline | N/A | N/A |
| assert_math_presence | N/A | N/A |
| assert_reading_order | N/A | N/A |
| assert_table_relation | N/A | N/A |
| assert_text_absence | N/A | N/A |
| assert_text_presence | N/A | N/A |
| cer | N/A | N/A |
| heading | N/A | N/A |
| img_f1 | N/A | 0.000 (fail 0%) |
| img_iou | N/A | 0.000 (fail 0%) |
| nid | N/A | N/A |
| teds | N/A | N/A |
| teds_struct | N/A | N/A |
| wer | N/A | N/A |
