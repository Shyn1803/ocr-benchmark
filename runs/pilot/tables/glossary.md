# Chú giải — đọc bảng kết quả thế nào

File này **không chứa kết quả**. Nó giải thích các từ mà mọi file kết quả khác dùng, để người đọc lần đầu không phải suy ra nghĩa từ con số.

Sinh lúc `2025-08-18T00:00:00Z` bởi `src/ocr_bench/glossary.py`; cột *đo cái gì* lấy từ docstring của chính lớp metric, không viết tay.

## 1. Mỗi metric đo cái gì

Cột *trần* là số tài liệu nhiều nhất metric chấm được với bộ nhãn hiện có — chi tiết ở `tables/ceiling.md`.

| metric | nửa corpus | trần | đo cái gì |
|---|---|---:|---|
| `assert_math_presence` | olmocr | 558 | ⚠️ **CẬN DƯỚI.** So chuỗi sau chuẩn hoá, không dựng ảnh như olmOCR. |
| `assert_text_absence` | olmocr | 315 | Chuỗi **không** được có mặt (thường là đầu trang / chân trang lọt vào). |
| `assert_reading_order` | olmocr | 314 | `before` phải đứng trước `after` trong đầu ra. |
| `block_f1` | doclaynet | 203 | F1 của phép ghép khối ở IoU ≥ ngưỡng — "tìm đúng bao nhiêu khối". |
| `type_f1` | doclaynet | 203 | Macro-F1 theo loại khối — "gọi tên khối có đúng không". |
| `assert_table_relation` | olmocr | 188 | Ô bảng phải có lân cận / tiêu đề như mô tả. |
| `assert_text_presence` | olmocr | 160 | Chuỗi phải có mặt trong đầu ra. |
| `img_f1` | doclaynet | 64 | F1 của phép ghép ảnh ở IoU ≥ ngưỡng — "tìm đúng bao nhiêu ảnh". |
| `img_iou` | doclaynet | 64 | Chất lượng khung — "tìm ra rồi thì cắt có sát không". |
| `table_recall` | doclaynet | 43 | Tỷ lệ bảng nhãn được engine định vị đúng ở IoU ≥ 0.5. |
| `heading` | doclaynet | 17 | Phân cấp tiêu đề. 1.0 = mọi quan hệ trên/dưới giữa các tiêu đề đều khớp nhãn. |
| `assert_baseline` | olmocr | 9 | Vệ sinh đầu ra: không rỗng, không ký tự thay thế. |
| `cell_f1` | doclaynet | 0 | F1 trên ô bảng theo toạ độ lưới — "ô nào bị mất, ô nào bịa ra". |
| `cer` | doclaynet | 0 | 1 − tỉ lệ lỗi ký tự. |
| `diacritics_acc` | doclaynet | 0 | Tỷ lệ ký tự có dấu được engine đặt đúng dấu. |
| `nid` | doclaynet | 0 | Thứ tự đọc. 1.0 = đúng thứ tự nhãn; đảo đoạn thì tụt. |
| `teds` | doclaynet | 0 | TEDS đầy đủ: cấu trúc **và** nội dung ô. |
| `teds_struct` | doclaynet | 0 | TEDS-Struct: chỉ cấu trúc, bỏ nội dung ô. |
| `wer` | doclaynet | 0 | 1 − tỉ lệ lỗi từ. |

## 2. Ký hiệu và từ ngữ trong bảng

**`n`** — Số tài liệu thật sự chấm được **ô đó** — mẫu số của chính con số đứng cạnh, không phải số tài liệu engine chạy qua. Điểm không kèm `n` là điểm không đọc được: `1.000` trên 9 tài liệu và `0.910` trên 1403 tài liệu không cùng độ tin.

**`% hỏng`** — Tỉ lệ tài liệu engine chạy lỗi (timeout, crash, không ra đầu ra). Phải đọc **riêng**: các phép so sánh thống kê chỉ dùng tài liệu cả hai engine đều chấm được, nên chúng bỏ qua toàn bộ khác biệt về tỉ lệ hỏng.

**trung bình có phạt** — Trung bình trong đó tài liệu hỏng tính là 0, thay vì bị loại khỏi mẫu. Loại ra là thưởng cho engine hỏng nhiều — nó bỏ đi đúng những tài liệu khó.

**`N/A`** — Engine **không khai đủ năng lực** để metric chạm tới (ví dụ metric cần bbox mà engine chỉ trả văn bản). Đây không phải điểm 0, và dòng của nó không bị bỏ đi.

**`chưa có nhãn`** — Engine chạy được, nhưng bộ mẫu không có nhãn hợp loại để đối chiếu. Thiếu sót của **bộ mẫu**, không phải của engine.

**trần (`tables/ceiling.md`)** — Số tài liệu **nhiều nhất** metric chấm được nếu có một engine hoàn hảo trả về đúng bằng nhãn. Trần 0 nghĩa là không engine nào đo được gì ở metric đó — mọi ô N/A của nó là lỗi bộ mẫu.

**nửa corpus** — Bộ mẫu gồm hai nửa **rời nhau, giao đúng 0 tài liệu**: `doclaynet` (nhãn khung + loại khối) và `olmocr` (nhãn khẳng định đúng/sai về nội dung). Không bao giờ so một ô của nửa này với một ô của nửa kia.

**tập chung (`tables/common-set.md`)** — Tập tài liệu **mọi engine trong bảng đều có dự đoán**. Đây là bảng duy nhất mà đặt hai ô cạnh nhau rồi kết luận là hợp lệ.

**F1** — Trung bình điều hoà của độ chính xác (thứ tìm ra có đúng không) và độ bao phủ (bỏ sót bao nhiêu). 1.0 là hoàn hảo; đoán bừa nhiều làm tụt cả hai vế.

**macro-F1** — F1 tính riêng cho từng loại rồi lấy trung bình các loại, nên một loại hiếm nặng ngang một loại phổ biến.

**IoU** — Diện tích giao chia diện tích hợp của hai khung — hai khung trùng nhau tới đâu. `IoU ≥ 0.5` là quy ước "coi như tìm đúng".

**CER · WER** — Tỉ lệ lỗi ký tự · lỗi từ. Trong mọi bảng ở đây in dưới dạng `1 − lỗi`, để cùng chiều với các metric khác: **cao hơn là tốt hơn**.

**TEDS** — Khoảng cách sửa cây giữa bảng HTML engine sinh ra và bảng HTML trong nhãn. `teds_struct` chỉ xét cấu trúc, bỏ nội dung ô.

**NID** — Khoảng cách sửa chuỗi đã chuẩn hoá, dùng để đo thứ tự đọc: đảo đoạn thì tụt.

**†** — Metric **ngược chiều**: thấp hơn mới là tốt hơn. Bị loại khỏi mọi bảng xếp hạng theo điểm, và lý do in nguyên văn ngay dưới bảng có nó.

**‡** — Đo được nhưng **không phân biệt**: mọi engine chênh nhau dưới ngưỡng, nên con số đúng mà không dùng để chọn engine được. Khác hẳn N/A — ở đây phép đo chạy đủ, chỉ là nó không tách được các engine ra.

## 3. Thứ tự đọc một bảng kết quả

1. Bảng này thuộc **nửa corpus** nào? Hai nửa không so với nhau được.
2. **`n`** của ô là bao nhiêu? Dưới vài chục thì đừng kết luận gì.
3. **`% hỏng`** — engine điểm cao nhưng hỏng 55% không phải engine tốt hơn.
4. Chênh lệch có **ý nghĩa thống kê** không? Xem `results/statistical-tests.json`; mắt thường không phân biệt được 0.606 với 0.495 trên cỡ mẫu bất kỳ.
5. Muốn so hai engine trực tiếp thì đọc `tables/common-set.md`, không đọc `tables/overall.md` — ở đó mỗi engine chạy một tập tài liệu khác nhau.

