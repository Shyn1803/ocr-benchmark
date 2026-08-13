# C2 — thước đo có phân biệt được engine không

Sinh bằng `py -3 scripts/c2_report.py`. **Không** sửa tay — chạy lại để cập nhật.

Nguồn của `sabotage`: **opendataloader** (không phải `noop` mặc định — làm hỏng đầu ra rỗng thì vẫn rỗng, cổng sẽ xanh mà không kiểm gì).
Ngưỡng phân tán: **0.02**. Engine tổng hợp bị loại khỏi phép tính phân tán: noop, sabotage, sabotage_s10, sabotage_s30, sabotage_s60.

## 1. Cổng `sabotage` (AC-01)

Phán quyết là **một** phép so: `sabotage` phải thấp hơn chính **nguồn** của nó. Đó là phép cô lập được đúng một biến — cùng engine, cùng bộ tài liệu, chỉ khác chỗ đã bị làm hỏng. "Có đứng bét toàn bảng không" **không** phải điều kiện đạt: nó trộn phép làm hỏng với chênh lệch năng lực giữa các engine, nên nó kết tội thước đo vì một sự thật về engine.

`chạy` = cổng thực sự kiểm được điều gì. Metric không đo được thì `sabotage` xuống cuối **vì N/A**, không phải vì kém — đó không tính là đạt.

| Metric | Cổng chạy | Đạt | sabotage | nguồn | Ghi chú |
|---|---|---|---|---|---|
| `assert_baseline` | ✅ | ❌ | 1.0000 | 1.0000 | KHÔNG thấp hơn nguồn: 1.0000 ≥ opendataloader 1.0000 — METRIC NÀY SAI, làm hỏng đầu ra mà điểm không giảm. |
| `assert_math_presence` | ✅ | ✅ | 0.0010 | 0.0023 | thấp hơn nguồn: 0.0010 < opendataloader 0.0023. (Quan trắc, không phải lỗi metric: `pdf_inspector` còn thấp hơn cả bản làm hỏng.) |
| `assert_reading_order` | ✅ | ✅ | 0.0694 | 0.4076 | thấp hơn nguồn: 0.0694 < opendataloader 0.4076. |
| `assert_table_relation` | ✅ | ✅ | 0.0000 | 0.3101 | thấp hơn nguồn: 0.0000 < opendataloader 0.3101. |
| `assert_text_absence` | ✅ | ❌ | 0.7643 | 0.4589 | KHÔNG thấp hơn nguồn: 0.7643 ≥ opendataloader 0.4589 — METRIC NÀY SAI, làm hỏng đầu ra mà điểm không giảm. |
| `assert_text_presence` | ✅ | ✅ | 0.0737 | 0.1301 | thấp hơn nguồn: 0.0737 < opendataloader 0.1301. |
| `block_f1` | ✅ | ✅ | 0.0710 | 0.6086 | thấp hơn nguồn: 0.0710 < opendataloader 0.6086. |
| `cell_f1` | ✅ | ❌ | 0.0000 | 0.0000 | KHÔNG thấp hơn nguồn: 0.0000 ≥ opendataloader 0.0000 — METRIC NÀY SAI, làm hỏng đầu ra mà điểm không giảm. |
| `cer` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `diacritics_acc` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `heading` | ✅ | ✅ | 0.0588 | 0.5611 | thấp hơn nguồn: 0.0588 < opendataloader 0.5611. |
| `img_f1` | ✅ | ✅ | 0.1497 | 0.3650 | thấp hơn nguồn: 0.1497 < opendataloader 0.3650. |
| `img_iou` | ✅ | ✅ | 0.0947 | 0.3132 | thấp hơn nguồn: 0.0947 < opendataloader 0.3132. |
| `nid` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `table_recall` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `teds` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `teds_struct` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `type_f1` | ✅ | ✅ | 0.0390 | 0.2734 | thấp hơn nguồn: 0.0390 < opendataloader 0.2734. |
| `wer` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |

**12/19** metric có cổng chạy được; **9/12** trong số đó đạt.

## 2. Độ phân tán giữa các engine thật (AC-02)

`n` = số tài liệu **cả các engine cùng chấm được**. So trung bình trên hai bộ tài liệu khác nhau là so hai đại lượng khác nhau — chênh lệch thu được nói về bộ mẫu, không nói về engine.

| Metric | Phán quyết | spread | n | Engine | Lý do |
|---|---|---|---|---|---|
| `assert_baseline` | phan_biet_duoc | 0.4286 | 7 | opendataloader, pdf_inspector, sovereign_light | spread 0.4286 ≥ ngưỡng 0.02 trên 3 engine / 7 tài liệu chung. |
| `assert_math_presence` | phan_biet_duoc | 1.0000 | 1 | marker, opendataloader, pdf_inspector, sovereign_light | spread 1.0000 ≥ ngưỡng 0.02 trên 4 engine / 1 tài liệu chung. |
| `assert_reading_order` | phan_biet_duoc | 0.8000 | 1 | marker, opendataloader, pdf_inspector, sovereign_light | spread 0.8000 ≥ ngưỡng 0.02 trên 4 engine / 1 tài liệu chung. |
| `assert_table_relation` | phan_biet_duoc | 1.0000 | 1 | marker, opendataloader, pdf_inspector, sovereign_light | spread 1.0000 ≥ ngưỡng 0.02 trên 4 engine / 1 tài liệu chung. |
| `assert_text_absence` | phan_biet_duoc | 0.5000 | 1 | marker, opendataloader, pdf_inspector, sovereign_light | spread 0.5000 ≥ ngưỡng 0.02 trên 4 engine / 1 tài liệu chung. |
| `assert_text_presence` | khong_du_du_lieu | — | 0 | marker, opendataloader, pdf_inspector, sovereign_light | 4 engine đo được nhưng không tài liệu nào chung — so trung bình trên hai bộ mẫu khác nhau là so hai đại lượng khác nhau. |
| `block_f1` | phan_biet_duoc | 0.6369 | 20 | marker, opendataloader, pdf_inspector | spread 0.6369 ≥ ngưỡng 0.02 trên 3 engine / 20 tài liệu chung. |
| `cell_f1` | khong_du_du_lieu | — | 0 | marker, opendataloader | 2 engine đo được nhưng không tài liệu nào chung — so trung bình trên hai bộ mẫu khác nhau là so hai đại lượng khác nhau. |
| `cer` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `diacritics_acc` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `heading` | khong_du_du_lieu | — | 0 | opendataloader | chỉ 1 engine thật đo được metric này (opendataloader) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `img_f1` | phan_biet_duoc | 0.0667 | 5 | marker, opendataloader | spread 0.0667 ≥ ngưỡng 0.02 trên 2 engine / 5 tài liệu chung. |
| `img_iou` | phan_biet_duoc | 0.1075 | 5 | marker, opendataloader | spread 0.1075 ≥ ngưỡng 0.02 trên 2 engine / 5 tài liệu chung. |
| `nid` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `table_recall` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `teds` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `teds_struct` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `type_f1` | phan_biet_duoc | 0.7118 | 20 | marker, opendataloader, pdf_inspector | spread 0.7118 ≥ ngưỡng 0.02 trên 3 engine / 20 tài liệu chung. |
| `wer` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |

## 3. Bảng chính / phụ lục (AC-03)

- **Bảng chính — 7/19**: `assert_math_presence`, `assert_reading_order`, `assert_table_relation`, `block_f1`, `img_f1`, `img_iou`, `type_f1`
- **Phân tán đủ NHƯNG trượt cổng `sabotage` — 2**: `assert_baseline`, `assert_text_absence`
- **Phụ lục, không phân biệt được — 0**: _trống_
- **Phụ lục, chưa đủ dữ liệu — 10**: `assert_text_presence`, `cell_f1`, `cer`, `diacritics_acc`, `heading`, `nid`, `table_recall`, `teds`, `teds_struct`, `wer`

Hai nhóm phụ lục **không** cùng nghĩa. `khong_phan_biet_duoc` là kết luận về **metric**: các engine chênh nhau quá ít để nói lên điều gì. `khong_du_du_lieu` là kết luận về **bộ mẫu**: chưa có đủ hai engine cùng đo được để mà so. Gộp chúng lại là vứt nhầm một metric tốt vì thiếu nhãn.

