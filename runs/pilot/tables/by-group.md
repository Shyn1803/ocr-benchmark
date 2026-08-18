# Bảng theo nhóm tài liệu

> Sinh bằng `py -3 scripts/build_research_report.py`. **Không** sửa tay.

> **Chưa quen bộ metric này?** `glossary.md` giải thích từng metric đo cái gì và mọi ký hiệu trong bảng (`n`, `% hỏng`, `N/A`, `trần`, `†`, `‡`).
>
> Đọc theo thứ tự: **`n` trước, điểm sau** — một điểm cao trên 9 tài liệu không so được với một điểm thấp hơn trên 1403 tài liệu.

Tách theo nhóm làm số **rõ hơn**, không đẹp hơn: chia nhỏ thì cỡ mẫu của engine chạy ít tài liệu xuống còn vài đơn vị. Dòng `n` của từng bảng nói ra điều đó — đọc nó trước khi đọc điểm.

## doclaynet/financial_reports

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 34 | 34 | 34 | 34 |
| block_f1 | 0.834 (n=34, fail 0%) | 0.820 (n=34, fail 0%) | 0.698 (n=34, fail 0%) | 0.791 (n=34, fail 0%) |
| type_f1 | 0.573 (n=34, fail 0%) | 0.572 (n=34, fail 0%) | 0.358 (n=34, fail 0%) | 0.529 (n=34, fail 0%) |
| img_f1 | 0.688 (n=8, fail 0%) | 0.688 (n=8, fail 0%) | 0.310 (n=14, fail 0%) | 0.667 (n=8, fail 0%) |
| img_iou | 0.603 (n=8, fail 0%) | 0.603 (n=8, fail 0%) | 0.226 (n=14, fail 0%) | 0.562 (n=8, fail 0%) |
| table_recall | 0.944 (n=18, fail 0%) | 0.944 (n=18, fail 0%) | 0.102 (n=18, fail 0%) | 0.944 (n=18, fail 0%) |
| heading | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | 0.667 (n=1, fail 0%) | chưa có nhãn (34 tài liệu) |
| cell_f1 † | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| cer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| diacritics_acc | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| nid | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds_struct | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| wer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |

## doclaynet/government_tenders

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 34 | 34 | 34 | 34 |
| block_f1 | 0.856 (n=34, fail 0%) | 0.847 (n=34, fail 0%) | 0.733 (n=34, fail 0%) | 0.790 (n=34, fail 0%) |
| type_f1 | 0.594 (n=34, fail 0%) | 0.584 (n=34, fail 0%) | 0.377 (n=34, fail 0%) | 0.420 (n=34, fail 0%) |
| img_f1 | 0.929 (n=14, fail 0%) | 0.929 (n=14, fail 0%) | 0.781 (n=14, fail 0%) | 1.000 (n=14, fail 0%) |
| img_iou | 0.853 (n=14, fail 0%) | 0.853 (n=14, fail 0%) | 0.634 (n=14, fail 0%) | 0.902 (n=14, fail 0%) |
| table_recall | 1.000 (n=6, fail 0%) | 1.000 (n=6, fail 0%) | 0.667 (n=6, fail 0%) | 0.833 (n=6, fail 0%) |
| heading | 0.000 (n=1, fail 0%) | 0.000 (n=1, fail 0%) | 1.000 (n=1, fail 0%) | 0.000 (n=1, fail 0%) |
| cell_f1 † | 0.000 (n=1, fail 0%) | 0.000 (n=1, fail 0%) | 0.000 (n=1, fail 0%) | 0.000 (n=1, fail 0%) |
| cer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| diacritics_acc | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| nid | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds_struct | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| wer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |

## doclaynet/laws_and_regulations

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 34 | 34 | 34 | 34 |
| block_f1 | 0.801 (n=34, fail 0%) | 0.677 (n=34, fail 0%) | 0.615 (n=34, fail 0%) | 0.654 (n=34, fail 0%) |
| type_f1 | 0.457 (n=34, fail 0%) | 0.412 (n=34, fail 0%) | 0.224 (n=34, fail 0%) | 0.274 (n=34, fail 0%) |
| img_f1 | 0.667 (n=3, fail 0%) | 0.667 (n=3, fail 0%) | 0.111 (n=9, fail 0%) | 0.000 (n=3, fail 0%) |
| img_iou | 0.649 (n=3, fail 0%) | 0.649 (n=3, fail 0%) | 0.105 (n=9, fail 0%) | 0.000 (n=3, fail 0%) |
| table_recall | 1.000 (n=2, fail 0%) | 1.000 (n=2, fail 0%) | 1.000 (n=2, fail 0%) | 1.000 (n=2, fail 0%) |
| heading | 0.400 (n=6, fail 0%) | 0.344 (n=6, fail 0%) | 0.500 (n=4, fail 0%) | 0.344 (n=6, fail 0%) |
| cell_f1 † | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| cer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| diacritics_acc | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| nid | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds_struct | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| wer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |

## doclaynet/manuals

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 33 | 33 | 33 | 33 |
| block_f1 | 0.856 (n=33, fail 0%) | 0.837 (n=33, fail 0%) | 0.536 (n=33, fail 0%) | 0.554 (n=33, fail 0%) |
| type_f1 | 0.642 (n=33, fail 0%) | 0.626 (n=33, fail 0%) | 0.253 (n=33, fail 0%) | 0.369 (n=33, fail 0%) |
| img_f1 | 0.766 (n=22, fail 0%) | 0.766 (n=22, fail 0%) | 0.794 (n=17, fail 0%) | 0.766 (n=22, fail 0%) |
| img_iou | 0.733 (n=22, fail 0%) | 0.733 (n=22, fail 0%) | 0.752 (n=17, fail 0%) | 0.725 (n=22, fail 0%) |
| table_recall | 0.625 (n=6, fail 0%) | 0.583 (n=6, fail 0%) | 0.042 (n=6, fail 0%) | 0.583 (n=6, fail 0%) |
| heading | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) |
| cell_f1 † | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | 0.000 (n=1, fail 0%) | chưa có nhãn (33 tài liệu) |
| cer | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) |
| diacritics_acc | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) |
| nid | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) |
| teds | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) |
| teds_struct | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) |
| wer | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) | chưa có nhãn (33 tài liệu) |

## doclaynet/patents

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 34 | 34 | 34 | 34 |
| block_f1 | 0.504 (n=34, fail 0%) | 0.407 (n=34, fail 0%) | 0.495 (n=34, fail 0%) | 0.347 (n=34, fail 0%) |
| type_f1 | 0.351 (n=34, fail 0%) | 0.315 (n=34, fail 0%) | 0.208 (n=34, fail 0%) | 0.270 (n=34, fail 0%) |
| img_f1 | 0.829 (n=14, fail 0%) | 0.829 (n=14, fail 0%) | 0.115 (n=26, fail 0%) | 0.840 (n=14, fail 0%) |
| img_iou | 0.768 (n=14, fail 0%) | 0.768 (n=14, fail 0%) | 0.098 (n=26, fail 0%) | 0.733 (n=14, fail 0%) |
| table_recall | 0.444 (n=9, fail 0%) | 0.444 (n=9, fail 0%) | 0.000 (n=9, fail 0%) | 0.444 (n=9, fail 0%) |
| heading | 0.131 (n=4, fail 0%) | 0.131 (n=4, fail 0%) | 0.550 (n=5, fail 0%) | 0.131 (n=4, fail 0%) |
| cell_f1 † | 0.000 (n=1, fail 0%) | 0.000 (n=1, fail 0%) | 0.000 (n=2, fail 0%) | 0.000 (n=1, fail 0%) |
| cer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| diacritics_acc | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| nid | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds_struct | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| wer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |

## doclaynet/scientific_articles

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 34 | 34 | 34 | 34 |
| block_f1 | 0.889 (n=34, fail 0%) | 0.823 (n=34, fail 0%) | 0.572 (n=34, fail 0%) | 0.681 (n=34, fail 0%) |
| type_f1 | 0.639 (n=34, fail 0%) | 0.592 (n=34, fail 0%) | 0.219 (n=34, fail 0%) | 0.359 (n=34, fail 0%) |
| img_f1 | 1.000 (n=9, fail 0%) | 1.000 (n=9, fail 0%) | 0.167 (n=18, fail 0%) | 0.778 (n=9, fail 0%) |
| img_iou | 0.979 (n=9, fail 0%) | 0.979 (n=9, fail 0%) | 0.131 (n=18, fail 0%) | 0.693 (n=9, fail 0%) |
| table_recall | 1.000 (n=2, fail 0%) | 1.000 (n=2, fail 0%) | 0.500 (n=2, fail 0%) | 1.000 (n=2, fail 0%) |
| heading | 0.083 (n=4, fail 0%) | 0.083 (n=4, fail 0%) | 0.500 (n=4, fail 0%) | 0.083 (n=4, fail 0%) |
| cell_f1 † | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | 0.000 (n=3, fail 0%) | chưa có nhãn (34 tài liệu) |
| cer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| diacritics_acc | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| nid | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| teds_struct | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |
| wer | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) | chưa có nhãn (34 tài liệu) |

## olmocr/arxiv_math

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 522 | 522 | 522 | 522 |
| assert_math_presence | 0.000 (n=522, fail 2%) | 0.000 (n=522, fail 0%) | 0.001 (n=522, fail 0%) | 0.000 (n=522, fail 1%) |
| assert_text_absence | chưa có nhãn (511 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (519 tài liệu) |
| assert_reading_order | chưa có nhãn (511 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (519 tài liệu) |
| assert_table_relation | chưa có nhãn (511 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (519 tài liệu) |
| assert_text_presence | chưa có nhãn (511 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (519 tài liệu) |
| assert_baseline | chưa có nhãn (511 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (522 tài liệu) | chưa có nhãn (519 tài liệu) |

## olmocr/headers_footers

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 266 | 266 | 266 | 266 |
| assert_math_presence | chưa có nhãn (266 tài liệu) | chưa có nhãn (265 tài liệu) | chưa có nhãn (266 tài liệu) | chưa có nhãn (266 tài liệu) |
| assert_text_absence | 0.930 (n=266, fail 0%) | 0.951 (n=266, fail 0%) | 0.361 (n=266, fail 0%) | 0.910 (n=266, fail 0%) |
| assert_reading_order | chưa có nhãn (266 tài liệu) | chưa có nhãn (265 tài liệu) | chưa có nhãn (266 tài liệu) | chưa có nhãn (266 tài liệu) |
| assert_table_relation | chưa có nhãn (266 tài liệu) | chưa có nhãn (265 tài liệu) | chưa có nhãn (266 tài liệu) | chưa có nhãn (266 tài liệu) |
| assert_text_presence | chưa có nhãn (266 tài liệu) | chưa có nhãn (265 tài liệu) | chưa có nhãn (266 tài liệu) | chưa có nhãn (266 tài liệu) |
| assert_baseline | 1.000 (n=7, fail 0%) | 0.857 (n=7, fail 14%) | 1.000 (n=7, fail 0%) | 1.000 (n=7, fail 0%) |

## olmocr/long_tiny_text

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 62 | 62 | 62 | 62 |
| assert_math_presence | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) |
| assert_text_absence | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) |
| assert_reading_order | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) |
| assert_table_relation | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) |
| assert_text_presence | 0.401 (n=62, fail 0%) | 0.256 (n=62, fail 0%) | 0.336 (n=62, fail 0%) | 0.307 (n=62, fail 0%) |
| assert_baseline | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) | chưa có nhãn (62 tài liệu) |

## olmocr/multi_column

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 231 | 231 | 231 | 231 |
| assert_math_presence | chưa có nhãn (231 tài liệu) | chưa có nhãn (230 tài liệu) | chưa có nhãn (231 tài liệu) | chưa có nhãn (231 tài liệu) |
| assert_text_absence | chưa có nhãn (231 tài liệu) | chưa có nhãn (230 tài liệu) | chưa có nhãn (231 tài liệu) | chưa có nhãn (231 tài liệu) |
| assert_reading_order | 0.418 (n=231, fail 0%) | 0.233 (n=231, fail 0%) | 0.554 (n=231, fail 0%) | 0.465 (n=231, fail 0%) |
| assert_table_relation | chưa có nhãn (231 tài liệu) | chưa có nhãn (230 tài liệu) | chưa có nhãn (231 tài liệu) | chưa có nhãn (231 tài liệu) |
| assert_text_presence | chưa có nhãn (231 tài liệu) | chưa có nhãn (230 tài liệu) | chưa có nhãn (231 tài liệu) | chưa có nhãn (231 tài liệu) |
| assert_baseline | chưa có nhãn (231 tài liệu) | chưa có nhãn (230 tài liệu) | chưa có nhãn (231 tài liệu) | chưa có nhãn (231 tài liệu) |

## olmocr/old_scans

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 98 | 98 | 98 | 98 |
| assert_math_presence | chưa có nhãn (98 tài liệu) | chưa có nhãn (97 tài liệu) | chưa có nhãn (98 tài liệu) | chưa có nhãn (98 tài liệu) |
| assert_text_absence | 1.000 (n=49, fail 0%) | 0.980 (n=50, fail 2%) | 0.990 (n=49, fail 0%) | 0.990 (n=49, fail 0%) |
| assert_reading_order | 0.000 (n=83, fail 0%) | 0.000 (n=83, fail 1%) | 0.000 (n=83, fail 0%) | 0.000 (n=83, fail 0%) |
| assert_table_relation | chưa có nhãn (98 tài liệu) | chưa có nhãn (97 tài liệu) | chưa có nhãn (98 tài liệu) | chưa có nhãn (98 tài liệu) |
| assert_text_presence | 0.018 (n=98, fail 0%) | 0.018 (n=98, fail 1%) | 0.000 (n=98, fail 0%) | 0.018 (n=98, fail 0%) |
| assert_baseline | chưa có nhãn (98 tài liệu) | chưa có nhãn (97 tài liệu) | chưa có nhãn (98 tài liệu) | chưa có nhãn (98 tài liệu) |

## olmocr/old_scans_math

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 36 | 36 | 36 | 36 |
| assert_math_presence | 0.018 (n=36, fail 0%) | 0.006 (n=36, fail 0%) | 0.027 (n=36, fail 0%) | 0.015 (n=36, fail 0%) |
| assert_text_absence | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) |
| assert_reading_order | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) |
| assert_table_relation | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) |
| assert_text_presence | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) |
| assert_baseline | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) | chưa có nhãn (36 tài liệu) |

## olmocr/tables

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 188 | 188 | 188 | 188 |
| assert_math_presence | chưa có nhãn (188 tài liệu) | chưa có nhãn (187 tài liệu) | chưa có nhãn (188 tài liệu) | chưa có nhãn (188 tài liệu) |
| assert_text_absence | chưa có nhãn (188 tài liệu) | chưa có nhãn (187 tài liệu) | chưa có nhãn (188 tài liệu) | chưa có nhãn (188 tài liệu) |
| assert_reading_order | chưa có nhãn (188 tài liệu) | chưa có nhãn (187 tài liệu) | chưa có nhãn (188 tài liệu) | chưa có nhãn (188 tài liệu) |
| assert_table_relation | 0.641 (n=188, fail 0%) | 0.510 (n=188, fail 1%) | 0.310 (n=188, fail 0%) | 0.503 (n=188, fail 0%) |
| assert_text_presence | chưa có nhãn (188 tài liệu) | chưa có nhãn (187 tài liệu) | chưa có nhãn (188 tài liệu) | chưa có nhãn (188 tài liệu) |
| assert_baseline | 1.000 (n=2, fail 0%) | 0.667 (n=3, fail 33%) | 1.000 (n=2, fail 0%) | 1.000 (n=2, fail 0%) |

> † `cell_f1` **không** đo chất lượng ô ở bộ mẫu này. Không nhãn nào có ô, nên tài liệu duy nhất chấm được là tài liệu engine **tự sinh ra bảng** — theo định nghĩa metric thì điểm luôn 0.000 và thông tin nằm ở `n`: `n` là số tài liệu bị bảng ảo. **Thấp hơn là tốt hơn**, ngược chiều mọi metric còn lại, nên nó bị loại khỏi mọi bảng xếp hạng theo điểm. Thêm engine thứ tư cũng không đổi được điều này: thiếu ô trong nhãn là thiếu ở **bộ mẫu**, engine nào chạy vào cũng rơi đúng nhánh đó. Muốn `cell_f1` có nghĩa thì phải gán nhãn ô, không phải chạy thêm lượt.
