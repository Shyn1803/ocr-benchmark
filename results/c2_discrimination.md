# C2 — thước đo có phân biệt được engine không

Sinh bằng `py -3 scripts/c2_report.py`. **Không** sửa tay — chạy lại để cập nhật.

Nguồn của `sabotage`: **opendataloader** (không phải `noop` mặc định — làm hỏng đầu ra rỗng thì vẫn rỗng, cổng sẽ xanh mà không kiểm gì).
Ngưỡng phân tán: **0.02**. Engine tổng hợp bị loại khỏi phép tính phân tán: noop, sabotage.

## 1. Cổng `sabotage` (AC-01)

`chạy` = cổng thực sự kiểm được điều gì. Metric không đo được thì `sabotage` xuống cuối **vì N/A**, không phải vì kém — đó không tính là đạt.

| Metric | Cổng chạy | Đạt | sabotage | nguồn | Ghi chú |
|---|---|---|---|---|---|
| `assert_baseline` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `assert_math_presence` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `assert_reading_order` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `assert_table_relation` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `assert_text_absence` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `assert_text_presence` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `cer` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `heading` | ✅ | ✅ | 0.0000 | 0.5611 | đứng bét trong 2 engine đo được, 0.0000 < opendataloader 0.5611. |
| `img_f1` | ✅ | ✅ | 0.1446 | 0.3548 | đứng bét trong 3 engine đo được, 0.1446 < opendataloader 0.3548. |
| `img_iou` | ✅ | ✅ | 0.0912 | 0.3030 | đứng bét trong 3 engine đo được, 0.0912 < opendataloader 0.3030. |
| `nid` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `teds` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `teds_struct` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |
| `wer` | ⬜ | — | — | — | metric không đo được ở đây (sabotage n_scored=0, opendataloader n_scored=0) — cổng KHÔNG chạy, không tính là đạt. |

**3/14** metric có cổng chạy được; **3/3** trong số đó đạt.

## 2. Độ phân tán giữa các engine thật (AC-02)

`n` = số tài liệu **cả các engine cùng chấm được**. So trung bình trên hai bộ tài liệu khác nhau là so hai đại lượng khác nhau — chênh lệch thu được nói về bộ mẫu, không nói về engine.

| Metric | Phán quyết | spread | n | Engine | Lý do |
|---|---|---|---|---|---|
| `assert_baseline` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `assert_math_presence` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `assert_reading_order` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `assert_table_relation` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `assert_text_absence` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `assert_text_presence` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `cer` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `heading` | khong_du_du_lieu | — | 0 | opendataloader | chỉ 1 engine thật đo được metric này (opendataloader) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `img_f1` | phan_biet_duoc | 0.0667 | 5 | marker, opendataloader | spread 0.0667 ≥ ngưỡng 0.02 trên 2 engine / 5 tài liệu chung. |
| `img_iou` | phan_biet_duoc | 0.0633 | 5 | marker, opendataloader | spread 0.0633 ≥ ngưỡng 0.02 trên 2 engine / 5 tài liệu chung. |
| `nid` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `teds` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `teds_struct` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |
| `wer` | khong_du_du_lieu | — | 0 | — | chỉ 0 engine thật đo được metric này (không có engine nào) — cần ít nhất 2 để nói về phân tán. Thiếu nhãn, không phải metric hỏng. |

## 3. Bảng chính / phụ lục (AC-03)

- **Bảng chính — 2/14**: `img_f1`, `img_iou`
- **Phụ lục, không phân biệt được — 0**: _trống_
- **Phụ lục, chưa đủ dữ liệu — 12**: `assert_baseline`, `assert_math_presence`, `assert_reading_order`, `assert_table_relation`, `assert_text_absence`, `assert_text_presence`, `cer`, `heading`, `nid`, `teds`, `teds_struct`, `wer`

Hai nhóm phụ lục **không** cùng nghĩa. `khong_phan_biet_duoc` là kết luận về **metric**: các engine chênh nhau quá ít để nói lên điều gì. `khong_du_du_lieu` là kết luận về **bộ mẫu**: chưa có đủ hai engine cùng đo được để mà so. Gộp chúng lại là vứt nhầm một metric tốt vì thiếu nhãn.

