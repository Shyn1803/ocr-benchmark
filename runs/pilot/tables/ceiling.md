# Trần đo được của bộ nhãn

Bảng này **không đọc `prediction/`**. Nó trả lời: với ground truth đang có,
mỗi metric nhiều nhất chấm được bao nhiêu tài liệu — kể cả khi engine hoàn hảo.
Trần 0 nghĩa là con số N/A trong bảng xếp hạng là lỗi của **bộ mẫu**, không
phải của engine.

- DocLayNet (nhãn bbox): **204** tài liệu
- olmOCR (nhãn khẳng định): **1403** tài liệu
- Giao hai nửa: **0** tài liệu — không metric nào bắc cầu được qua cả hai.

Sinh lúc `2025-08-18T00:00:00Z` bởi `src/ocr_bench/ceiling.py`; cột *vì sao* là
chuỗi do chính `_na_rieng()` của metric trả về, cột *đo cái gì* lấy từ
docstring của lớp metric.

> **Chưa quen bộ metric này?** `glossary.md` giải thích từng metric đo cái gì và mọi ký hiệu trong bảng (`n`, `% hỏng`, `N/A`, `trần`, `†`, `‡`).
>
> Đọc theo thứ tự: **`n` trước, điểm sau** — một điểm cao trên 9 tài liệu không so được với một điểm thấp hơn trên 1403 tài liệu.

## đo được (≥100 tài liệu)

| metric | đo cái gì | nửa corpus | trần | trên tổng | năng lực cần | vì sao không hơn |
|---|---|---|---:|---:|---|---|
| `assert_math_presence` | ⚠️ **CẬN DƯỚI.** So chuỗi sau chuẩn hoá, không dựng ảnh như olmOCR. | olmocr | 558 | 1403 | `text_md` | tài liệu không có khẳng định loại 'math_presence' (845/1403 tài liệu) |
| `assert_text_absence` | Chuỗi **không** được có mặt (thường là đầu trang / chân trang lọt vào). | olmocr | 315 | 1403 | `text_md` | tài liệu không có khẳng định loại 'text_absence' (1088/1403 tài liệu) |
| `assert_reading_order` | `before` phải đứng trước `after` trong đầu ra. | olmocr | 314 | 1403 | `text_md` | tài liệu không có khẳng định loại 'reading_order' (1089/1403 tài liệu) |
| `block_f1` | F1 của phép ghép khối ở IoU ≥ ngưỡng — "tìm đúng bao nhiêu khối". | doclaynet | 203 | 204 | `block_bbox` | nhãn không có khối và engine cũng không trả khung nào (1/204 tài liệu) |
| `type_f1` | Macro-F1 theo loại khối — "gọi tên khối có đúng không". | doclaynet | 203 | 204 | `block_bbox` | nhãn không có khối và engine cũng không trả khung nào (1/204 tài liệu) |
| `assert_table_relation` | Ô bảng phải có lân cận / tiêu đề như mô tả. | olmocr | 188 | 1403 | `text_md` | tài liệu không có khẳng định loại 'table_relation' (1215/1403 tài liệu) |
| `assert_text_presence` | Chuỗi phải có mặt trong đầu ra. | olmocr | 160 | 1403 | `text_md` | tài liệu không có khẳng định loại 'text_presence' (1243/1403 tài liệu) |

## mỏng (<100 tài liệu)

| metric | đo cái gì | nửa corpus | trần | trên tổng | năng lực cần | vì sao không hơn |
|---|---|---|---:|---:|---|---|
| `img_f1` | F1 của phép ghép ảnh ở IoU ≥ ngưỡng — "tìm đúng bao nhiêu ảnh". | doclaynet | 64 | 204 | `image_bbox` | nhãn không có ảnh và engine cũng không trả box nào (140/204 tài liệu) |
| `img_iou` | Chất lượng khung — "tìm ra rồi thì cắt có sát không". | doclaynet | 64 | 204 | `image_bbox` | nhãn không có ảnh và engine cũng không trả box nào (140/204 tài liệu) |
| `table_recall` | Tỷ lệ bảng nhãn được engine định vị đúng ở IoU ≥ 0.5. | doclaynet | 43 | 204 | `table_html` | nhãn không có khung bảng để đối chiếu (161/204 tài liệu) |
| `heading` | Phân cấp tiêu đề. 1.0 = mọi quan hệ trên/dưới giữa các tiêu đề đều khớp nhãn. | doclaynet | 17 | 204 | `block_bbox`, `heading_level` | dưới 2 tiêu đề trong nhãn — không có quan hệ nào để so (119/204 tài liệu); nhãn chỉ có một cấp tiêu đề (68/204 tài liệu) |
| `assert_baseline` | Vệ sinh đầu ra: không rỗng, không ký tự thay thế. | olmocr | 9 | 1403 | `text_md` | tài liệu không có khẳng định loại 'baseline' (1394/1403 tài liệu) |

## trần 0 — không engine nào chấm được

| metric | đo cái gì | nửa corpus | trần | trên tổng | năng lực cần | vì sao không hơn |
|---|---|---|---:|---:|---|---|
| `cell_f1` | F1 trên ô bảng theo toạ độ lưới — "ô nào bị mất, ô nào bịa ra". | doclaynet | 0 | 204 | `table_html` | nhãn không có bảng và engine cũng không trả bảng nào (161/204 tài liệu); nhãn có bảng nhưng không bảng nào có nội dung ô (43/204 tài liệu) |
| `cer` | 1 − tỉ lệ lỗi ký tự. | doclaynet | 0 | 204 | `text_md` | nhãn không có chữ để so (204/204 tài liệu) |
| `diacritics_acc` | Tỷ lệ ký tự có dấu được engine đặt đúng dấu. | doclaynet | 0 | 204 | `text_md` | nhãn không có chữ (204/204 tài liệu) |
| `nid` | Thứ tự đọc. 1.0 = đúng thứ tự nhãn; đảo đoạn thì tụt. | doclaynet | 0 | 204 | `block_bbox` | nhãn không có thứ tự đọc; xem AnnotationGT.reading_order (204/204 tài liệu) |
| `teds` | TEDS đầy đủ: cấu trúc **và** nội dung ô. | doclaynet | 0 | 204 | `table_html` | nhãn không có bảng nào dùng được (204/204 tài liệu) |
| `teds_struct` | TEDS-Struct: chỉ cấu trúc, bỏ nội dung ô. | doclaynet | 0 | 204 | `table_html` | nhãn không có bảng nào dùng được (204/204 tài liệu) |
| `wer` | 1 − tỉ lệ lỗi từ. | doclaynet | 0 | 204 | `text_md` | nhãn không có chữ để so (204/204 tài liệu) |

