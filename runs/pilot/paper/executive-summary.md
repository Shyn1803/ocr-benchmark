# Tóm tắt Thực thi — OCR Parser Benchmark

**4 profile** · **19 metric** · mốc dựng tất định.

Không có điểm tổng và **không có trung bình cộng giữa các metric**: các metric khác nhau về trần đo được và thuộc hai nửa corpus rời nhau (xem `tables/ceiling.md`), nên trung bình của chúng không truy được về tập tài liệu nào. Mỗi dòng dưới đây là một metric, kèm cỡ mẫu `n` của chính con số đó.

> **Chưa quen bộ metric này?** `tables/glossary.md` giải thích từng metric đo cái gì và mọi ký hiệu trong bảng (`n`, `% hỏng`, `N/A`, `trần`, `†`, `‡`).
>
> Đọc theo thứ tự: **`n` trước, điểm sau** — một điểm cao trên 9 tài liệu không so được với một điểm thấp hơn trên 1403 tài liệu.

**Cách đọc một dòng:** *trần* là số tài liệu nhiều nhất metric chấm được với bộ nhãn hiện có; *độ trải* là khoảng cách điểm giữa engine cao nhất và thấp nhất — dưới 0.05 thì metric không tách được các engine ra và dòng mang dấu `‡`; *giá trị* luôn kèm `n` là cỡ mẫu của chính ô đó.

## Text & OCR — đo được 2/5 metric

| metric | nửa corpus | trần | độ trải | engine dẫn đầu | giá trị |
|---|---|---:|---:|---|---|
| cer | doclaynet | 0 | — | — | chưa có nhãn (203 tài liệu) |
| wer | doclaynet | 0 | — | — | chưa có nhãn (203 tài liệu) |
| diacritics_acc | doclaynet | 0 | — | — | chưa có nhãn (203 tài liệu) |
| assert_text_presence ‡ | olmocr | 160 | 0.048 | `docling_default` | 0.156 (n=171, fail 6%) |
| assert_text_absence | olmocr | 315 | 0.491 | `docling_scan` | 0.950 (n=318, fail 1%) |

## Layout & Structure — đo được 2/5 metric

| metric | nửa corpus | trần | độ trải | engine dẫn đầu | giá trị |
|---|---|---:|---:|---|---|
| block_f1 | doclaynet | 203 | 0.181 | `docling_default` | 0.790 (n=203, fail 0%) |
| type_f1 | doclaynet | 203 | 0.269 | `docling_default` | 0.542 (n=203, fail 0%) |
| heading | doclaynet | 17 | 0.366 | `opendataloader_default` | 0.561 (n=15, fail 0%) |
| img_f1 | doclaynet | 64 | 0.463 | `docling_scan` | 0.828 (n=70, fail 0%) |
| img_iou | doclaynet | 64 | 0.464 | `docling_scan` | 0.777 (n=70, fail 0%) |

## Tables — đo được 1/5 metric

| metric | nửa corpus | trần | độ trải | engine dẫn đầu | giá trị |
|---|---|---:|---:|---|---|
| teds | doclaynet | 0 | — | — | chưa có nhãn (203 tài liệu) |
| teds_struct | doclaynet | 0 | — | — | chưa có nhãn (203 tài liệu) |
| cell_f1 † | doclaynet | 0 | 0.000 | — | ngược chiều, không xếp hạng theo điểm |
| table_recall | doclaynet | 43 | 0.597 | `docling_default` | 0.808 (n=43, fail 0%) |
| assert_table_relation | olmocr | 188 | 0.295 | `docling_default` | 0.606 (n=199, fail 6%) |

> † `cell_f1` **không** đo chất lượng ô ở bộ mẫu này. Không nhãn nào có ô, nên tài liệu duy nhất chấm được là tài liệu engine **tự sinh ra bảng** — theo định nghĩa metric thì điểm luôn 0.000 và thông tin nằm ở `n`: `n` là số tài liệu bị bảng ảo. **Thấp hơn là tốt hơn**, ngược chiều mọi metric còn lại, nên nó bị loại khỏi mọi bảng xếp hạng theo điểm. Thêm engine thứ tư cũng không đổi được điều này: thiếu ô trong nhãn là thiếu ở **bộ mẫu**, engine nào chạy vào cũng rơi đúng nhánh đó. Muốn `cell_f1` có nghĩa thì phải gán nhãn ô, không phải chạy thêm lượt.

## Reading Order — đo được 1/2 metric

| metric | nửa corpus | trần | độ trải | engine dẫn đầu | giá trị |
|---|---|---:|---:|---|---|
| nid | doclaynet | 0 | — | — | chưa có nhãn (203 tài liệu) |
| assert_reading_order | olmocr | 314 | 0.237 | `opendataloader_default` | 0.408 (n=314, fail 0%) |

## Robustness & Base — đo được 1/2 metric

| metric | nửa corpus | trần | độ trải | engine dẫn đầu | giá trị |
|---|---|---:|---:|---|---|
| assert_baseline | olmocr | 9 | 0.550 | `opendataloader_default` | 1.000 (n=9, fail 0%) |
| assert_math_presence ‡ | olmocr | 558 | 0.002 | `opendataloader_default` | 0.002 (n=558, fail 0%) |

> ‡ Metric **đo được nhưng không phân biệt**: mọi engine chênh nhau dưới 0.05 điểm, nên con số đúng mà không dùng để chọn engine được. Đây không phải `N/A` — phép đo chạy đủ trên cỡ mẫu thật; nó chỉ nói rằng ở khía cạnh này các engine hành xử như nhau, và kết luận nào rút ra từ thứ tự của chúng cũng là kết luận rút ra từ nhiễu.

