# Bảng theo nhóm tài liệu

> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.

Tách theo nhóm làm số **rõ hơn**, không đẹp hơn: chia nhỏ thì cỡ mẫu của engine chạy ít tài liệu xuống còn vài đơn vị. Dòng `n` của từng bảng nói ra điều đó — đọc nó trước khi đọc điểm.

Ngoài bộ mẫu, **không** vào bảng nào dưới đây: `sample_minimal`.

## doclaynet/financial_reports

| metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_light |
|---|---|---|---|---|---|---|
| **n (tài liệu)** | 2 | 2 | 34 | 34 | 34 | 34 |
| assert_baseline | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_math_presence | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_reading_order | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_table_relation | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_text_absence | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_text_presence | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| cer | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| heading | N/A | N/A | 0.667 (fail 0%) | N/A | 0.000 (fail 0%) | — (1 hỏng, 0 chấm được) |
| img_f1 | N/A | N/A | 0.310 (fail 0%) | N/A | 0.071 (fail 0%) | — (1 hỏng, 0 chấm được) |
| img_iou | N/A | N/A | 0.226 (fail 0%) | N/A | 0.059 (fail 0%) | — (1 hỏng, 0 chấm được) |
| nid | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| teds | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| teds_struct | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| wer | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |

## doclaynet/government_tenders

| metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_light |
|---|---|---|---|---|---|---|
| **n (tài liệu)** | 5 | 5 | 34 | 34 | 34 | 34 |
| assert_baseline | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_math_presence | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_reading_order | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_table_relation | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_text_absence | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_text_presence | N/A | N/A | N/A | N/A | N/A | N/A |
| cer | N/A | N/A | N/A | N/A | N/A | N/A |
| heading | N/A | N/A | 1.000 (fail 0%) | N/A | 0.000 (fail 0%) | N/A |
| img_f1 | 0.833 (fail 0%) | N/A | 0.781 (fail 0%) | N/A | 0.000 (fail 0%) | N/A |
| img_iou | 0.595 (fail 0%) | N/A | 0.634 (fail 0%) | N/A | 0.000 (fail 0%) | N/A |
| nid | N/A | N/A | N/A | N/A | N/A | N/A |
| teds | N/A | N/A | N/A | N/A | N/A | N/A |
| teds_struct | N/A | N/A | N/A | N/A | N/A | N/A |
| wer | N/A | N/A | N/A | N/A | N/A | N/A |

## doclaynet/laws_and_regulations

| metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_full | sovereign_light |
|---|---|---|---|---|---|---|---|
| **n (tài liệu)** | 4 | 4 | 34 | 34 | 34 | 1 | 34 |
| assert_baseline | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| assert_math_presence | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| assert_reading_order | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| assert_table_relation | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| assert_text_absence | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| assert_text_presence | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| cer | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| heading | N/A | N/A | 0.500 (fail 0%) | N/A | 0.000 (fail 0%) | N/A | — (3 hỏng, 0 chấm được) |
| img_f1 | N/A | N/A | 0.111 (fail 0%) | N/A | 0.000 (fail 0%) | N/A | — (3 hỏng, 0 chấm được) |
| img_iou | N/A | N/A | 0.105 (fail 0%) | N/A | 0.000 (fail 0%) | N/A | — (3 hỏng, 0 chấm được) |
| nid | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| teds | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| teds_struct | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |
| wer | N/A | N/A | N/A | N/A | N/A | N/A | — (3 hỏng, 0 chấm được) |

## doclaynet/manuals

| metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_light |
|---|---|---|---|---|---|---|
| **n (tài liệu)** | 1 | 1 | 34 | 34 | 34 | 34 |
| assert_baseline | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_math_presence | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_reading_order | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_table_relation | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_text_absence | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| assert_text_presence | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| cer | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| heading | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| img_f1 | 1.000 (fail 0%) | N/A | 0.794 (fail 0%) | N/A | 0.480 (fail 0%) | — (1 hỏng, 0 chấm được) |
| img_iou | 0.939 (fail 0%) | N/A | 0.752 (fail 0%) | N/A | 0.285 (fail 0%) | — (1 hỏng, 0 chấm được) |
| nid | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| teds | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| teds_struct | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |
| wer | N/A | N/A | N/A | N/A | N/A | — (1 hỏng, 0 chấm được) |

## doclaynet/patents

| metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_full | sovereign_light |
|---|---|---|---|---|---|---|---|
| **n (tài liệu)** | 4 | 4 | 34 | 34 | 34 | 1 | 34 |
| assert_baseline | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| assert_math_presence | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| assert_reading_order | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| assert_table_relation | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| assert_text_absence | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| assert_text_presence | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| cer | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| heading | N/A | N/A | 0.550 (fail 0%) | N/A | 0.000 (fail 0%) | N/A | — (5 hỏng, 0 chấm được) |
| img_f1 | N/A | N/A | 0.115 (fail 0%) | N/A | 0.077 (fail 0%) | N/A | — (5 hỏng, 0 chấm được) |
| img_iou | N/A | N/A | 0.098 (fail 0%) | N/A | 0.054 (fail 0%) | N/A | — (5 hỏng, 0 chấm được) |
| nid | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| teds | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| teds_struct | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |
| wer | N/A | N/A | N/A | N/A | N/A | N/A | — (5 hỏng, 0 chấm được) |

## doclaynet/scientific_articles

| metric | marker | noop | opendataloader | pdf_inspector | sabotage | sovereign_light |
|---|---|---|---|---|---|---|
| **n (tài liệu)** | 4 | 4 | 34 | 34 | 34 | 34 |
| assert_baseline | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_math_presence | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_reading_order | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_table_relation | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_text_absence | N/A | N/A | N/A | N/A | N/A | N/A |
| assert_text_presence | N/A | N/A | N/A | N/A | N/A | N/A |
| cer | N/A | N/A | N/A | N/A | N/A | N/A |
| heading | N/A | N/A | 0.500 (fail 0%) | N/A | 0.000 (fail 0%) | N/A |
| img_f1 | N/A | N/A | 0.167 (fail 0%) | N/A | 0.167 (fail 0%) | N/A |
| img_iou | N/A | N/A | 0.131 (fail 0%) | N/A | 0.103 (fail 0%) | N/A |
| nid | N/A | N/A | N/A | N/A | N/A | N/A |
| teds | N/A | N/A | N/A | N/A | N/A | N/A |
| teds_struct | N/A | N/A | N/A | N/A | N/A | N/A |
| wer | N/A | N/A | N/A | N/A | N/A | N/A |

## olmocr/arxiv_math

| metric | noop |
|---|---|
| **n (tài liệu)** | 20 |
| assert_baseline | N/A |
| assert_math_presence | 0.000 (fail 0%) |
| assert_reading_order | N/A |
| assert_table_relation | N/A |
| assert_text_absence | N/A |
| assert_text_presence | N/A |
| cer | N/A |
| heading | N/A |
| img_f1 | N/A |
| img_iou | N/A |
| nid | N/A |
| teds | N/A |
| teds_struct | N/A |
| wer | N/A |
