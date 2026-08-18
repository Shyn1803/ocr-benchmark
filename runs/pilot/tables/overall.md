# Bảng tổng quan — mọi engine, mọi tài liệu

> Sinh bằng `py -3 scripts/build_research_report.py`. **Không** sửa tay.

> **Chưa quen bộ metric này?** `glossary.md` giải thích từng metric đo cái gì và mọi ký hiệu trong bảng (`n`, `% hỏng`, `N/A`, `trần`, `†`, `‡`).
>
> Đọc theo thứ tự: **`n` trước, điểm sau** — một điểm cao trên 9 tài liệu không so được với một điểm thấp hơn trên 1403 tài liệu.

## Đọc bảng này thế nào

Mỗi engine chạy trên một tập tài liệu **khác nhau** (xem dòng `n`). Đặt hai ô cạnh nhau rồi kết luận cái nào hơn là **sai** trừ khi hai engine có cùng `n` trên cùng tập. Bảng so chéo hợp lệ nằm ở `common-set.md`.

### Cảnh báo

- Giao của cả 4 engine là 1606 tài liệu. Bảng gộp toàn bộ KHÔNG phải một phép so sánh — xem `common-set.md`.

## DocLayNet — nhãn bố cục (bbox)

204 tài liệu, nhãn là khung + loại khối. Không giao một tài liệu nào với nửa dưới, nên **không so ô của hai bảng với nhau**.

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 203 | 203 | 203 | 203 |
| block_f1 | 0.790 (n=203, fail 0%) | 0.735 (n=203, fail 0%) | 0.609 (n=203, fail 0%) | 0.637 (n=203, fail 0%) |
| type_f1 | 0.542 (n=203, fail 0%) | 0.516 (n=203, fail 0%) | 0.273 (n=203, fail 0%) | 0.370 (n=203, fail 0%) |
| img_f1 | 0.828 (n=70, fail 0%) | 0.828 (n=70, fail 0%) | 0.365 (n=98, fail 0%) | 0.785 (n=70, fail 0%) |
| img_iou | 0.777 (n=70, fail 0%) | 0.777 (n=70, fail 0%) | 0.313 (n=98, fail 0%) | 0.708 (n=70, fail 0%) |
| table_recall | 0.808 (n=43, fail 0%) | 0.802 (n=43, fail 0%) | 0.211 (n=43, fail 0%) | 0.779 (n=43, fail 0%) |
| heading | 0.217 (n=15, fail 0%) | 0.195 (n=15, fail 0%) | 0.561 (n=15, fail 0%) | 0.195 (n=15, fail 0%) |
| cell_f1 † | 0.000 (n=2, fail 0%) | 0.000 (n=2, fail 0%) | 0.000 (n=7, fail 0%) | 0.000 (n=2, fail 0%) |
| cer | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) |
| diacritics_acc | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) |
| nid | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) |
| teds | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) |
| teds_struct | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) |
| wer | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) | chưa có nhãn (203 tài liệu) |

## olmOCR — nhãn khẳng định

1403 tài liệu, nhãn là các khẳng định đúng/sai về nội dung. Trần đo được của từng metric xem `tables/ceiling.md`.

| metric | docling_default | docling_scan | opendataloader_default | opendataloader_scan |
|---|---|---|---|---|
| **n (tài liệu)** | 1403 | 1403 | 1403 | 1403 |
| assert_math_presence | 0.001 (n=558, fail 2%) | 0.001 (n=562, fail 1%) | 0.002 (n=558, fail 0%) | 0.001 (n=558, fail 1%) |
| assert_text_absence | 0.910 (n=326, fail 3%) | 0.950 (n=318, fail 1%) | 0.459 (n=315, fail 0%) | 0.914 (n=318, fail 1%) |
| assert_reading_order | 0.297 (n=325, fail 3%) | 0.171 (n=316, fail 1%) | 0.408 (n=314, fail 0%) | 0.339 (n=317, fail 1%) |
| assert_table_relation | 0.606 (n=199, fail 6%) | 0.502 (n=191, fail 2%) | 0.310 (n=188, fail 0%) | 0.495 (n=191, fail 2%) |
| assert_text_presence | 0.156 (n=171, fail 6%) | 0.108 (n=163, fail 2%) | 0.130 (n=160, fail 0%) | 0.128 (n=163, fail 2%) |
| assert_baseline | 0.450 (n=20, fail 55%) | 0.667 (n=12, fail 33%) | 1.000 (n=9, fail 0%) | 0.750 (n=12, fail 25%) |

> † `cell_f1` **không** đo chất lượng ô ở bộ mẫu này. Không nhãn nào có ô, nên tài liệu duy nhất chấm được là tài liệu engine **tự sinh ra bảng** — theo định nghĩa metric thì điểm luôn 0.000 và thông tin nằm ở `n`: `n` là số tài liệu bị bảng ảo. **Thấp hơn là tốt hơn**, ngược chiều mọi metric còn lại, nên nó bị loại khỏi mọi bảng xếp hạng theo điểm. Thêm engine thứ tư cũng không đổi được điều này: thiếu ô trong nhãn là thiếu ở **bộ mẫu**, engine nào chạy vào cũng rơi đúng nhánh đó. Muốn `cell_f1` có nghĩa thì phải gán nhãn ô, không phải chạy thêm lượt.

Ô `N/A` = engine không có năng lực để metric chạm tới. Nó **không** phải 0 và dòng của nó **không** bị bỏ đi.
