# Ma Trận Nhãn ↔ Metric — Cái Gì Đo Được, Cái Gì Chưa, Và Vì Sao

> **Mục đích.** Trả lời đúng một câu hỏi: trong 19 metric đã đăng ký, cái nào **có cơ sở
> đối chiếu thật** để lấy ra bảng, cái nào **chưa có** và cụ thể còn thiếu gì.
>
> **Kiểm chứng lần cuối:** 2026-08-13, bằng cách gọi trực tiếp `load_olmocr()`,
> `load_doclaynet()` và `registry.get_adapter(...).capabilities` trên máy. Mọi con số
> trong tài liệu này là số đo được, không phải số chép lại từ tài liệu cũ.
>
> **Hướng dẫn chạy nằm ở file khác:** [`huong-dan-chay-3-nhom-metric.md`](huong-dan-chay-3-nhom-metric.md).

---

## 0. Nguyên tắc nền: một metric cần đủ HAI vế

Một metric chỉ ra được con số khi thỏa **cả hai** điều kiện, thiếu vế nào cũng thành N/A:

| Vế | Câu hỏi | Thiếu thì mã lý do là |
|---|---|---|
| **Nhãn** | Bộ mẫu có đáp án cho thứ này không? | `NO_GROUND_TRUTH` / `WRONG_GT_KIND` |
| **Năng lực** | Engine có *hứa* xuất thứ này không? | `MISSING_CAPABILITY` |

Cơ chế: `registry.applicable_metrics()` chỉ nhận metric có `Metric.requires ⊆ Adapter.capabilities`.

> **Vì sao không điền 0.0 cho ô trống?** Vì 0.0 nghĩa là "engine làm và làm sai", còn N/A
> nghĩa là "không có căn cứ để phán". Trộn hai cái đó lại là bịa dữ liệu. `MetricResult`
> ép: `value is None` thì **bắt buộc** có `na_reason` — không có đường nào lách.

---

## 1. Hai họ nhãn rời nhau — gốc rễ của mọi giới hạn bên dưới

Repo có đúng hai bộ nhãn, và **không tài liệu nào có cả hai**:

### 1.1 `AssertionGT` — olmOCR-bench

- **1403 tài liệu**, **7019 câu khẳng định** đúng/sai.
- Không có toàn văn, không có toạ độ. Chỉ có các mệnh đề rời rạc kiểu *"chuỗi X phải
  xuất hiện"*, *"X phải nằm trước Y"*.

Phân bố theo loại khẳng định:

| Loại | Số khẳng định |
|---|---:|
| `math_presence` | 3385 |
| `reading_order` | 1061 |
| `table_relation` | 1020 |
| `text_absence` | 823 |
| `text_presence` | 721 |
| `baseline` | 9 |
| **Tổng** | **7019** |

Phân bố theo **tầng** (thư mục `pdfs/olmocr/<tầng>/`):

| Tầng | Số tài liệu |
|---|---:|
| `arxiv_math` | 522 |
| `headers_footers` | 266 |
| `multi_column` | 231 |
| `tables` | 188 |
| `old_scans` | 98 |
| `long_tiny_text` | 62 |
| `old_scans_math` | 36 |
| **Tổng** | **1403** |

> **Tầng quét = `old_scans` + `old_scans_math` = 134 tài liệu.** Đây là toàn bộ tài liệu
> ảnh quét trong repo. Bảng khẳng định **bắt buộc** phải tách theo tầng: một engine chỉ
> đọc lớp text có sẵn sẽ trượt sạch 134 tài liệu này vì lý do chẳng liên quan gì tới loại
> khẳng định, và nếu gộp lại thì cột `text_presence = 0.27` trông y hệt một bộ so khớp hỏng.

### 1.2 `AnnotationGT` — DocLayNet

- **204 mục nhãn** (manifest liệt kê **203** `document_id` — chênh 1, dùng 203 khi chạy).
- **2942 hộp** có gán nhãn loại. Không có chữ (`text=None`), không có thứ tự đọc.

| Loại khối | Số hộp | % |
|---|---:|---:|
| TEXT | 1328 | 45.1% |
| LIST | 578 | 19.6% |
| HEADING | 322 | 10.9% |
| PAGE_FOOTER | 169 | 5.7% |
| PAGE_HEADER | 154 | 5.2% |
| PICTURE | 122 | 4.1% |
| TABLE | 75 | 2.5% |
| FORMULA | 57 | 1.9% |
| CAPTION | 50 | 1.7% |
| FOOTNOTE | 44 | 1.5% |
| TITLE | 43 | 1.5% |
| **Tổng** | **2942** | |

Về ảnh: **64 tài liệu có ảnh** (122 hộp PICTURE), **140 tài liệu không có ảnh**.
Về bảng: **43 tài liệu có khối TABLE**, nhưng **0 tài liệu có `AnnotationGT.tables`** —
xem mục 3.3 để hiểu vì sao đó không phải lỗi.

---

## 2. Năng lực engine — bảng này quyết định profile nào có số

```
docling         block_bbox · heading_level · table_html · text_md
opendataloader  block_bbox · heading_level · table_html · text_md · image_bbox · image_bytes
marker          block_bbox · heading_level · table_html · text_md · image_bbox · image_bytes · section_hierarchy
sovereign       text_md
pdf_inspector   block_bbox · scan_label · text_md
noop            text_md
sabotage        (tất cả — engine phá hoại dùng để kiểm metric có phân biệt được không)
```

> ⚠️ **Docling KHÔNG khai `image_bbox`** → `img_f1` / `img_iou` của `docling_default` và
> `docling_scan` là N/A với lý do `MISSING_CAPABILITY`, phải để ở cột khác hẳn N/A vì thiếu
> nhãn khi lên bảng.
>
> **Nhưng đừng đọc thành "docling không bóc tách được ảnh".** Nó bóc tách được: 20 tài liệu
> `docling_scan` trong `calibration/` cho ra **14 block `picture`**, mỗi block có `box` đầy đủ
> (kiểm chứng 2026-08-13). Vấn đề nằm ở chỗ khác — adapter đổ chúng vào `blocks[]` với
> `block_type: picture` và **không bao giờ ghi gì vào `OcrResult.images`**, trong khi `img_f1`
> chỉ đọc `result.images` ([imgf1.py:130](../src/ocr_bench/metrics/imgf1.py#L130)). Không có
> `images[].box` thì không được phép khai `IMAGE_BBOX` — `OcrResult._require` sẽ chặn
> ([types.py:398](../src/ocr_bench/types.py#L398)).
>
> Nói cách khác đây là **quyết định ánh xạ ở adapter, không phải giới hạn của engine**. Phía
> nhãn đã làm đúng phép ánh xạ đó rồi: `corpus.py:174` làm `if loai is BlockType.PICTURE:
> images.append(box)`. Muốn docling có điểm nhóm C thì làm đối xứng ở
> `adapters/docling.py` rồi thêm `Capability.IMAGE_BBOX`. Vẫn không có `IMAGE_BYTES` (docling
> không trả ảnh cắt trừ khi bật `generate_picture_images`), nhưng `img_f1`/`img_iou` chỉ cần
> `IMAGE_BBOX` nên thế là đủ.

> ⚠️ **`sovereign` chỉ có `text_md`.** Kể cả khi API cục bộ dựng xong, nó vẫn không bao giờ
> có dòng nào ở nhóm bố cục hay nhóm ảnh. Đừng chờ đợi điều đó.

---

## 3. Kết luận: 11 metric CÓ cơ sở, 8 metric CHƯA

### Nhóm A — 6 metric khẳng định ✅

| | |
|---|---|
| **Đối chiếu là gì** | 7019 câu khẳng định đúng/sai |
| **Bộ mẫu** | olmOCR-bench, **1403 tài liệu** |
| **Năng lực cần** | `text_md` |
| **Có số cho** | cả 4 profile chạy được (docling ×2, opendataloader ×2) |

`assert_text_presence` · `assert_text_absence` · `assert_reading_order` ·
`assert_math_presence` · `assert_table_relation` · `assert_baseline`

### Nhóm B — 3 metric bố cục ✅

| | |
|---|---|
| **Đối chiếu là gì** | 2942 hộp có gán nhãn loại |
| **Bộ mẫu** | DocLayNet, **203 tài liệu** |
| **Năng lực cần** | `block_bbox` (+ `heading_level` cho `heading`) |
| **Có số cho** | cả 4 profile |

- **`block_f1`** — tìm được khối không. **Không xét loại khối.**
- **`type_f1`** — gọi tên loại có đúng không (macro trên 11 loại).
- **`heading`** — nhận ra tiêu đề không.

> **Bảng nhóm B phải in kèm `n` của từng loại, và in CẢ macro lẫn micro.** Dưới macro,
> 57 hộp FORMULA nặng ngang 1328 hộp TEXT. Chỉ in macro là để một engine bỏ qua toàn bộ
> văn bản thường nhưng bắt tốt công thức trông giỏi hơn thực tế.

### Nhóm C — 2 metric ảnh ✅ (nhưng chỉ 2/4 profile)

| | |
|---|---|
| **Đối chiếu là gì** | 122 hộp PICTURE |
| **Bộ mẫu** | DocLayNet — **64 tài liệu có ảnh** + **140 tài liệu không ảnh** |
| **Năng lực cần** | `image_bbox` |
| **Có số cho** | `opendataloader_default`, `opendataloader_scan` — **docling: N/A** |

`img_f1` (tìm đúng bao nhiêu ảnh) · `img_iou` (khung có sát không)

> **Nhóm C phải có hai mẫu số, không phải một.**
> - **64 tài liệu có ảnh** → đo *tìm được không*.
> - **140 tài liệu không ảnh** → đo *dương tính giả*. Quy tắc trong `imgf1.py`: GT 0 ảnh
>   và engine cũng 0 hộp thì N/A (không có gì để đo); GT 0 ảnh mà engine vẽ ra hộp thì
>   **0.0** (bịa ảnh, phải bị phạt).
>
> Gộp hai mẫu số vào một cột là làm mất hẳn thông tin dương tính giả.

*(Nhỏ: docstring `imgf1.py` ghi "141/204 tài liệu không có ảnh"; số đo hôm nay là **140** —
`fixes.json` đã thêm một hộp PICTURE. Lệch 1, vô hại, nhưng nên sửa docstring.)*

---

## 4. Tám metric CHƯA có cơ sở — thiếu chính xác cái gì

### 4.1 `cer` · `wer` · `diacritics_acc` ❌

**Thiếu:** văn bản tham chiếu toàn trang. DocLayNet chỉ có hộp, không có chữ. olmOCR chỉ có
khẳng định rời rạc, không có toàn văn.

**Cần để mở khoá:** một bộ tài liệu kèm bản gõ tay toàn văn, **theo đúng thứ tự người đọc**.

> 🚫 **Đừng lấy `cells/*.json` của DocLayNet nối lại làm văn bản tham chiếu.**
> File đó có chữ thật, nhưng theo thứ tự nội dung trong file PDF, **không phải** thứ tự
> người đọc. Đây chính là lý do `load_doclaynet()` cố tình đặt `text=None` (xem docstring
> module `corpus.py`). Dùng nó sẽ phạt đúng những engine sắp lại thứ tự cho đúng — tức là
> phạt cái đáng thưởng.

**Riêng `diacritics_acc`:** bộ mẫu hiện tại **100% tiếng Anh**. Metric này đo dấu tiếng Việt.
Không có tài liệu tiếng Việt thì nó vô nghĩa kể cả khi đã có toàn văn.

### 4.2 `nid` (thứ tự đọc) ❌

**Thiếu:** nhãn thứ tự đọc thật. `AnnotationGT.reading_order` rỗng, **và đó là cố ý**.

**Vì sao không suy ra được:** trong COCO, `annotation.id` là thứ tự người annotate *vẽ hộp*
— họ vẽ gom theo loại, không vẽ theo thứ tự đọc. Đã kiểm trên tài liệu **một cột** (nơi thứ
tự đọc bắt buộc trùng thứ tự trên-xuống): vẫn có **10% cặp nghịch thế**, và chỉ **5/11**
tài liệu khớp hoàn toàn.

**Cần để mở khoá:** người đánh số thứ tự đọc cho 203 trang. Sắp theo hình học rồi chấm là
chấm engine theo heuristic của chính bench — vô nghĩa.

> `assert_reading_order` (1061 khẳng định) **vẫn chạy bình thường** và nằm ở nhóm A. Nó hỏi
> "X có trước Y không", không đòi thứ tự đầy đủ. Đừng nhầm hai cái.

### 4.3 `teds` · `teds_struct` · `cell_f1` · `table_recall` ❌

**Thiếu:** cấu trúc ô bên trong bảng. DocLayNet có 75 hộp TABLE trên 43 tài liệu, nhưng đó
là *khung bao quanh cả cái bảng* — không có thông tin mấy hàng, mấy cột, ô nào gộp ô nào.

**Cần để mở khoá:** bộ mẫu kiểu **PubTabNet** hoặc **FinTabNet** — mỗi bảng kèm HTML đầy đủ.

**`table_recall` cần thêm một thứ nữa:** repo **không có `Capability.TABLE_BBOX`**. Nghĩa là
chưa engine nào *hứa* chỉ ra bảng nằm ở đâu trên trang. Có nhãn khung bảng cũng vô ích cho
tới khi thêm capability này và adapter khai nó.

> 🚫 **Đừng "sửa nhanh" bằng cách nhét 75 hộp TABLE vào `AnnotationGT.tables`.**
> `OcrTable` **bắt buộc** có trường `html`, mà DocLayNet không có → chỉ điền được `html=""`
> → `cell_f1` so lưới rỗng với lưới thật → **mọi engine ăn 0.0**.
>
> Đổi 3 cái N/A trung thực lấy 1 cái 0.0 sai + 2 cái N/A vẫn còn nguyên. `table_cells.py`
> tồn tại **chính là để chặn** con số 0 giả kiểu đó. **Không sửa code.**

---

## 5. Tổ chức output

### 5.1 Giữ nguyên nguồn gốc, chỉ rút gọn bảng in

**Không xoá 8 metric N/A khỏi `raw-results.json`.** Chúng ở lại kèm `NAReason` làm bằng
chứng kiểm toán. Chỉ **bảng đọc cho người** mới rút còn 11 metric có số, kèm một sổ phụ giải
thích 8 cái kia.

Bỏ hẳn khỏi file gốc là mất khả năng trả lời *"vì sao không có TEDS"* sáu tháng sau.

### 5.2 Bốn khung nhìn đề xuất

| File | Nội dung | Yêu cầu bắt buộc |
|---|---|---|
| `A-assertions.md` | 6 metric khẳng định | tách **loại × tầng**, in `n` từng ô |
| `B-layout.md` | `block_f1`, `type_f1`, `heading` | in `n` từng loại khối, in **cả macro lẫn micro** |
| `C-images.md` | `img_f1`, `img_iou` | **hai mẫu số** (64 có ảnh / 140 không ảnh) |
| `Z-na-ledger.md` | 8 metric còn lại | nhóm theo `NAReason`, **tách** `MISSING_CAPABILITY` khỏi `NO_GROUND_TRUTH` |

Nguồn cho cả bốn: `raw-results.json` + `aggregate-results.json` (file thứ hai đã sẵn có các
trường `applicable` / `cell` / `fail_rate` / `mean` / `n_scored` / `n_total` / `penalized_mean`).

### 5.3 Bảng tra nhanh

| Metric | Bộ mẫu | n | Profile có số | Trạng thái |
|---|---|---:|---|---|
| 6 × `assert_*` | olmOCR | 1403 | cả 4 | ✅ |
| `block_f1`, `type_f1`, `heading` | DocLayNet | 203 | cả 4 | ✅ |
| `img_f1`, `img_iou` | DocLayNet | 64 (+140) | chỉ OpenDataLoader | ✅ |
| `cer`, `wer` | — | 0 | — | ❌ cần bộ toàn văn |
| `diacritics_acc` | — | 0 | — | ❌ cần tài liệu tiếng Việt |
| `nid` | — | 0 | — | ❌ cần người đánh thứ tự đọc |
| `teds`, `teds_struct`, `cell_f1` | — | 0 | — | ❌ cần PubTabNet/FinTabNet |
| `table_recall` | — | 0 | — | ❌ cần nhãn khung **và** `Capability.TABLE_BBOX` |

---

## 6. Hai cái bẫy khi đọc kết quả

1. **Đừng ghi đè `results/`.** Thư mục đó giữ corpus đóng băng với các engine
   `marker` / `noop` / `sabotage` / `pdf_inspector` / `sovereign_full` — dùng để kiểm xem
   metric có phân biệt được engine tốt/xấu hay không. Luôn dùng `--out runs/pilot`.

2. **N/A không phải một loại.** `MISSING_CAPABILITY` (docling với ảnh) và `NO_GROUND_TRUTH`
   (TEDS) là hai chuyện ngược nhau. Cái đầu là engine không làm; cái sau là chưa có gì để
   so. In cùng một ký hiệu `·` cho cả hai là xoá mất thông tin quan trọng nhất của bảng.
