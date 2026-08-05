# `prediction/` — kết quả chạy engine, được commit

Mỗi file là đầu ra của **một engine trên một tài liệu**:

```
prediction/<engine>/<doc_id>.json
prediction/<engine>/<doc_id>.images/000.png     ← chỉ khi engine trả bytes ảnh
```

Đọc bằng `ocr_bench.prediction.load_predictions()`, sinh bằng
`scripts/make_predictions.py`.

## Vì sao commit

Marker chạy 200 trang trên CPU mất khoảng 3 giờ. Nếu sửa một dòng trong metric là phải
trả lại 3 giờ đó thì sẽ không ai sửa metric nữa — và một bộ thước không ai dám sửa là
bộ thước sai vĩnh viễn. Chạy và chấm là hai bước tách hẳn:

```
scripts/make_predictions.py            → prediction/     (một lần, hàng giờ)
load_predictions() + score_results()   → bảng điểm       (bao nhiêu lần cũng được, <30s)
```

`ocr_bench.prediction` không import `ocr_bench.adapters`, nên đường chấm lại **không có
cách nào** gọi engine kể cả khi nhầm.

Lợi ích thứ hai: `git diff` trên thư mục này cho thấy **đầu ra engine đổi ở đâu** giữa
hai lần nâng cấp. Đó là lý do ảnh PNG nằm ở file riêng chứ không base64 nhúng trong
JSON — một pixel đổi sẽ làm cả dòng hàng trăm KB đổi theo và diff thành vô dụng.

## Bộ đang commit là gì

| engine | tài liệu |
|---|---|
| `noop` | 1 sample + 20 DocLayNet + 20 olmOCR-bench |
| `sabotage` | như trên |

⚠️ Cả hai đều là **engine giả**, có mặt để đo *bộ thước* chứ không đo OCR: `noop` trả
chuỗi rỗng, `sabotage` bọc `noop` nên cũng ra rỗng. Bộ này chứng minh đường ống
ghi/đọc chạy được trên bộ mẫu thật — nó **không** nói gì về chất lượng nhận dạng. Số
liệu thật đến từ A4→A7 (Marker, OpenDataLoader, pdf-inspector, BE hiện tại).

Cắt còn 20 tài liệu mỗi bộ là cố ý: bộ mẫu đầy đủ là 204 DocLayNet + 1.403 olmOCR, và
2.806 file đầu ra rỗng thì không ai đọc nổi khi review. Sinh lại toàn bộ:

```bash
py -3 scripts/make_predictions.py --engines noop,sabotage --corpus doclaynet
py -3 scripts/make_predictions.py --engines noop,sabotage --corpus olmocr
```

## Sinh lại một phần

Mặc định **bỏ qua** tài liệu đã có prediction — chạy lại lệnh trên chỉ bù phần thiếu.
Ép chạy lại thì thêm `--refresh`. Lúc đó `seconds` sẽ đổi ở mọi file: đó là phép đo
thời gian thật, không phải nhiễu, nên đừng commit `--refresh` lẫn vào một thay đổi
khác — diff sẽ không đọc được nữa.
