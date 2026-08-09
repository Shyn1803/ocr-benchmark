# Đọc tay 20 ca hỏng nặng nhất — D2 (TASK-088)

> **Cổng §5 đã qua (2026-08-10) — nhưng chưa qua cho mọi metric.** Hai chuyện đã chặn D3
> nay không còn: hai quần thể `sabotage` đã hợp nhất về một (nguồn `opendataloader`,
> 1608 tài liệu), và thế hoà `0.000` đã bị phá vì `sabotage` giờ làm hỏng đầu ra **thật**
> chứ không phải đầu ra rỗng.
>
> Còn lại **2/9 metric có cổng chạy được vẫn trượt** và đã bị loại khỏi bảng chính:
> `assert_baseline` (hoà đúng bằng nguồn, 1.0000) và `assert_text_absence` (0.7556 >
> nguồn 0.4589 — làm hỏng tài liệu lại **được thưởng** điểm). Số của hai metric đó nằm ở
> phụ lục và **không** được dùng để xếp hạng engine. Xem `results/c2_discrimination.md`.
>
> Tài liệu này vẫn là phân tích nội bộ, không phải bản đánh giá engine. Lý lẽ cho việc
> làm D2 trước khi cổng xanh: `.claude/tasks/TASK-088/plan.md` §1.

Bộ 20 ca đã phân tích: `results/d2-cases.json` (đã commit).

```bash
py -3 scripts/d2_cases.py
```

⚠️ **Chạy lại lệnh trên BÂY GIỜ sẽ KHÔNG ra đúng 20 ca trong `d2-cases.json`** — và đó là
dấu hiệu tốt, không phải lỗi. Bộ ca được chọn *trước* khi sửa nhãn ở §4; sau khi sửa, hai ca
`14654fbc` (`marker` và `opendataloader`) hết điểm 0 nên rời tầng `img_duong_tinh_gia`, và
hai ca khác (`190774629a25`, `1a40fc845186`) lên thế chỗ. Muốn tái lập chính xác bộ đã phân
tích thì checkout về commit trước khi thêm `ground-truth/doclaynet/fixes.json`. File
`d2-cases.json` đã commit chính là ảnh chụp đó.

---

## 1. Mẫu này cố ý lệch — đọc số ở đây đừng ngoại suy

Bản công bố có 10 052 ô, nhưng chỉ **261 ô có điểm thật**, và **164/261 ô bằng đúng 0.0**.
Sắp xếp tăng dần rồi cắt 20 ca đầu là chọn theo thứ tự `doc_id` — ngẫu nhiên mà trông có
phương pháp. Nên 20 ca được chọn theo **tầng**, mỗi tầng trả lời một câu hỏi chẩn đoán khác
(quy tắc: `plan.md` §2, cài đặt: `scripts/d2_cases.py`).

Hệ quả bắt buộc phải nói: **tỉ lệ nguyên nhân tìm được trên 20 ca này KHÔNG ngoại suy ra
toàn bộ bộ mẫu.** Mẫu được chọn để tối đa hoá thông tin chẩn đoán, không phải để đại diện.

---

## 2. Kết quả phân loại — AC-02

Ba cột mà AC-02 đòi tách được:

| Kết luận | Số ca | Ý nghĩa |
|---|---:|---|
| **engine hỏng** | 9 | Engine làm sai thật, số 0.0 là công bằng |
| **nhãn sai** | 2 | Ground truth thiếu/sai, engine bị phạt oan |
| **metric đo sai** | 2 | Engine làm đúng, cách chấm không nhận ra |
| **không phải lỗi engine** | 5 | Hành vi đúng thiết kế, 0.0 là kết quả đúng |
| **biện hộ được** | 2 | Engine sai nhưng có lý do khách quan (scan thuần) |
| Tổng | 20 | |

Bảng chi tiết:

| # | Tầng | Engine | doc_id | nhãn/đoán | Kết luận |
|--:|---|---|---|---|---|
| 1–5 | crash | `sovereign_light` | `1560acef` `299b84b2` `312b4f8e` `38dfbe14` `3e266b14` | — | **không phải lỗi engine** |
| 6 | img_lech_khung | `opendataloader` | `28aceccd` | 1/1 | **engine hỏng** — hộp `(0,0,1,1)` |
| 7 | img_lech_khung | `opendataloader` | `304c1d23` | 1/1 | **engine hỏng** — hộp `(0,0,1,1)` |
| 8 | img_lech_khung | `opendataloader` | `3e002314` | 2/1 | **engine hỏng** — hộp `(0,0,1,1)` |
| 9 | img_lech_khung | `opendataloader` | `6b981a95` | 6/1 | **engine hỏng** — hộp `(0,0,1,1)` |
| 10 | img_lech_khung | `opendataloader` | `7272f231` | 1/3 | **metric đo sai** — engine TÁCH cái nhãn gọi là một |
| 11 | img_duong_tinh_gia | `marker` | `14654fbc` | 0/1 | **nhãn sai** → đã sửa, xem §4 |
| 12 | img_duong_tinh_gia | `opendataloader` | `14654fbc` | 0/1 | **nhãn sai** → đã sửa, xem §4 |
| 13 | img_duong_tinh_gia | `opendataloader` | `12c38f48` | 0/1 | **engine hỏng** — hộp `(0,0,1,1)` trên trang có 2246 ký tự |
| 14 | img_duong_tinh_gia | `opendataloader` | `1560acef` | 0/1 | **biện hộ được** — scan thuần 0 ký tự |
| 15 | img_duong_tinh_gia | `opendataloader` | `166041d9` | 0/14 | **engine hỏng** — chia trang thành 14 dải ngang |
| 16 | img_bo_sot | `opendataloader` | `4d1758f5` | 3/0 | **engine hỏng** — bỏ sót cả 3 ảnh |
| 17 | img_bo_sot | `opendataloader` | `5cda25ba` | 1/0 | **engine hỏng** — bỏ sót logo EPO |
| 18 | img_bo_sot | `opendataloader` | `6e877f30` | 1/0 | **engine hỏng** — bỏ sót Fig. 2 |
| 19 | heading_zero | `opendataloader` | `3106daee` | — | **metric đo sai** — engine GỘP cái nhãn chia làm hai |
| 20 | heading_zero | `opendataloader` | `44173ee2` | — | **engine hỏng** — bỏ sót 2/3 tiêu đề |

Ảnh dựng lại cho từng ca (không commit, sinh lại được):

```bash
py -3 scripts/d2_render.py <doc_id 12 ký tự đầu> <engine>
```

---

## 3. Ba phát hiện đáng giá hơn bảng trên

### 3.1 Metric chấm 0.0 cho engine làm đúng, theo hai chiều đối xứng

Hai ca này là cùng một khuyết tật đo, soi từ hai phía:

| | `7272f231` (img_f1) | `3106daee` (heading) |
|---|---|---|
| Engine làm gì | **Tách**: 1 barcode → 3 dải | **Gộp**: 2 tiêu đề → 1 hộp |
| Số đo | IoU từng dải 0.326 < ngưỡng 0.5 | hộp `0.352,0.078,0.646,0.122`, tâm y ≈ 0.100 |
| Nhưng | 3 dải **hợp lại** phủ IoU **0.944** | Hai hộp nhãn ở `0.078–0.096` và `0.103–0.122` |
| Vì sao ra 0.0 | Khớp 1–1 theo IoU, không có hợp nhất | `ghep_theo_tam` khớp theo **tâm nằm trong**; tâm 0.100 rơi vào **khe** giữa hai hộp ⇒ `gan = [None]`, `n_ghep_duoc = 0` |

Cả hai bị chấm **0.0, không phân biệt được với "không tìm thấy gì"**. Đây là bằng chứng mạnh
nhất cho ô "metric đo sai" của AC-02: engine tìm ra đúng vật thể, đặt hộp đúng chỗ, và bị
chấm bằng điểm của engine không tìm thấy gì.

Nợ kỹ thuật rút ra (chưa sửa trong task này — sửa metric là đổi số công bố, phải là task riêng):
- `img_f1` cần khớp **nhiều-nhiều** (hợp nhất các đoán chồng lên cùng một nhãn) trước khi tính IoU.
- `ghep_theo_tam` cần dự phòng khi tâm rơi ngoài mọi hộp: lùi về IoU lớn nhất thay vì `None`.

### 3.2 Một giả thuyết có lợi cho engine đã bị bác bằng đo

Giả thuyết ban đầu: *"opendataloader ra hộp phủ cả trang `(0,0,1,1)` là nó nhận ra trang
scan không có lớp văn bản — hành vi hợp lý, không phải lỗi."*

Đo: đếm ký tự lớp văn bản của từng trang liên quan. **`12c38f48` có 2246 ký tự** mà vẫn ra
hộp phủ cả trang. Chỉ **`1560acef`** (0 ký tự) là scan thật.

⇒ Giả thuyết **sai**. Hộp `(0,0,1,1)` là lỗi thật của engine trong **5/6** ca, không phải
tín hiệu "đây là scan". Kết quả này bất lợi cho engine và vẫn được ghi.

### 3.3 5 ca "crash" không phải lỗi engine

Cả 5 là `sovereign_light` trên PDF scan thuần (0 ký tự lớp văn bản). Ở chế độ `light` mọi
đường OCR bị tắt theo thiết kế, nên engine **báo đúng** rằng nó không trích được gì. Xếp vào
"crash" là do `na_reason=engine_failed` gộp chung hai thứ khác nhau: *hỏng* và *từ chối có
lý do*. Đây là chỗ đáng tách mã lỗi, không phải chỗ đáng sửa engine.

---

## 4. Sửa nhãn — AC-03, kèm trước/sau

**Sửa đúng 1 nhãn.** 19 ca còn lại nhãn đúng.

### 4.1 Sửa gì

`14654fbc59c74412…`, thêm một `Picture`: logo ENISA ở góc trên-trái. Nhãn gốc khẳng định
trang **không có ảnh nào**, nên mọi engine tìm ra nó đều bị chấm 0.0.

Mục sửa nằm ở `ground-truth/doclaynet/fixes.json`, **không** sửa `layout_coco.json` —
file đó do `scripts/fetch_doclaynet.py:227` sinh lại và mọi sửa tay trong đó sẽ bị ghi đè
lặng lẽ. Overlay được `corpus.doc_fixes()` áp sau khi dựng nhãn gốc, và nằm trong vùng
băm của `make_manifest.py` nên số nào sinh ra từ bộ nhãn nào vẫn truy ngược được.

### 4.2 Bằng chứng — ba nguồn độc lập, không nguồn nào là engine

1. **Từ chính file PDF.** Page 0 có duy nhất một XObject `/Image15`, đặt bằng
   `59.25 0 0 39.15 62.3 788.52 cm`; MediaBox `[0, 0, 595.32, 841.92]`. Hộp trong `fixes.json`
   lấy thẳng từ ma trận đó ⇒ chuẩn hoá `0.1047 / 0.0169 / 0.2042 / 0.0634`.
2. **Từ chính bộ nhãn.** Cùng logo này **được** gán `Picture` ở tài liệu khác trong bộ mẫu —
   `149e13c5815d…` có Picture tại `0.109 / 0.019 / 0.202 / 0.064`, trùng khít vị trí. Nên đây
   là bỏ sót của người gán nhãn, không phải quy ước "logo thì không gán".
3. **Ảnh dựng lại**, xem được bằng mắt: `py -3 scripts/d2_render.py 14654fbc59c74412 opendataloader`.

**Hộp nhãn không lấy từ engine.** Lấy hộp engine làm nhãn là chấm engine bằng chính nó.
Việc hộp tính từ content stream trùng đầu ra `opendataloader` tới 3 chữ số thập phân
(`0.105 / 0.017 / 0.204 / 0.063`) là **kiểm chứng engine**, không phải ngược lại.

### 4.3 Trước/sau — sửa nhãn này LÀM ĐẸP BẢNG, nên phải công bố

Trên tài liệu `14654fbc`:

| Engine | img_f1 trước | sau | IoU |
|---|---:|---:|---:|
| `marker` | 0.0 | **1.0** | 0.779 |
| `opendataloader` | 0.0 | **1.0** | 1.000 |

Trên trung bình toàn bảng:

| Engine | Metric | Trước | Sau | n ca chấm được |
|---|---|---:|---:|---:|
| `marker` | `img_f1` | 0.6667 | **0.8667** | 5 |
| `marker` | `img_iou` | 0.5083 | **0.6640** | 5 |
| `opendataloader` | `img_f1` | 0.3548 | **0.3650** | 98 |
| `opendataloader` | `img_iou` | 0.3030 | **0.3132** | 98 |

⚠️ **`marker` nhảy 20 điểm vì nó chỉ có 5 ca ảnh chấm được.** Một nhãn sửa đúng vẫn đủ để
đổi thứ hạng khi cỡ mẫu bằng 5. Đây đúng là rủi ro `plan.md` §4 nêu ("sửa nhãn cho bảng đẹp
lên"); phòng vệ không nằm ở chỗ tránh sửa, mà ở chỗ **mọi mục sửa phải có `bang_chung` đọc
được từ PDF hoặc từ chính bộ nhãn** — `corpus.doc_fixes()` ném lỗi nếu thiếu, và
`test_bo_mau_that_nap_du_khong_mat_mat` bắt buộc mọi mục sửa phải làm đỏ một test trước khi
đi vào bảng.

Bản chấm lại: `history/2026-08-07-sau-sua-nhan/` (bản trước: `history/2026-08-07/`).
Không dùng `--force` để đè bản cũ — đè là làm mất đúng thứ cần để so.

---

## 5. Còn nợ lại

| Nợ | Vì sao chưa làm ở đây |
|---|---|
| `img_f1` chưa khớp nhiều-nhiều (§3.1) | Sửa metric là đổi số công bố — phải là task riêng có cổng QA |
| `ghep_theo_tam` trả `None` khi tâm rơi vào khe (§3.1) | Như trên |
| `na_reason=engine_failed` gộp "hỏng" với "từ chối có lý do" (§3.3) | Đổi mã lỗi ảnh hưởng mọi bảng đã công bố |
| 19 ca còn lại chưa sửa nhãn | Nhãn của chúng đúng — không có gì để sửa |
| Cổng §5 vẫn chưa qua | Việc của D3, không phải của D2 |
