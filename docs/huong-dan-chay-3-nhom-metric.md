# Hướng Dẫn Chạy 3 Nhóm Metric Có Cơ Sở Đối Chiếu

> **Tài liệu này chỉ nói CHẠY NHƯ THẾ NÀO.** Muốn hiểu *vì sao* chỉ chạy 3 nhóm này mà
> không chạy 8 metric còn lại, đọc [`ma-tran-nhan-va-metric.md`](ma-tran-nhan-va-metric.md).
>
> **Khác gì [`huong_dan_chay_pilot.md`](huong_dan_chay_pilot.md)?** File kia hướng dẫn chạy
> **20 file mẫu** để làm quen hệ thống. File này chạy **toàn bộ bộ nhãn** (203 + 1403 tài
> liệu) để ra bảng thật.
>
> **Kiểm chứng lần cuối:** 2026-08-13.

---

## 0. Trước khi bắt đầu — 4 điều bắt buộc nhớ

### 0.1 Luôn `cd` về gốc repo

Mọi lệnh trong tài liệu này chạy từ `ocr-bench/`. Trong Git Bash:

```bash
cd /d/vnpt-projects/sovereign/ocr-bench
```

### 0.2 Dùng đúng venv

Repo có **5 môi trường Python riêng**, không phải một:

| Venv | Chứa | Dùng cho |
|---|---|---|
| `.venv` | docling 2.91.0 · opendataloader-pdf 2.5.0 (đủ gói hybrid) | **docling_\*, opendataloader_\*, mọi lệnh chấm điểm** |
| `.venv-odl` | docling **2.119.0** · opendataloader-pdf 2.5.0 | (dự phòng — xem cảnh báo dưới) |
| `.venv-marker` | marker-pdf 1.10.2 | marker_\* (chưa dùng trong lượt này) |
| `.venv-pi` | — | pdf_inspector |
| `.venv-sov` | — | sovereign (BE API chưa dựng) |

> ⚠️ **`.venv` và `.venv-odl` cài docling khác phiên bản.** Server hybrid của OpenDataLoader
> gọi docling bên trong nó. Nếu bạn chạy server bằng `.venv-odl` (docling 2.119.0) nhưng
> chạy profile `docling_*` bằng `.venv` (docling 2.91.0) thì hai nhánh kết quả dùng hai bản
> docling khác nhau — vẫn chạy được, nhưng khi so sánh sẽ có một biến nhiễu không khai báo.
>
> **Khuyến nghị: dùng `.venv` cho tất cả.** Bản `build/odl-hybrid/manifest.json` hiện tại
> được sinh từ `.venv` và ghi `docling: 2.91.0`. Đổi venv thì `run_id` của manifest đổi theo.

### 0.3 Luôn có `PYTHONIOENCODING=utf-8`

Thiếu nó là script chết giữa chừng khi in tên file tiếng Việt trên Windows.

### 0.4 TUYỆT ĐỐI không dùng `--refresh`

Hệ thống có **cache**: file `.json` đã tồn tại trong thư mục đầu ra thì lượt sau in
`CACHE HIT` và bỏ qua. Nhờ vậy bạn ngắt lúc nào cũng được, chạy lại lệnh y hệt là nó đi
tiếp từ chỗ dở.

`--refresh` **xoá sạch** cache đó. Với lượt 1403 tài liệu, một lần gõ nhầm là mất hàng chục
giờ máy.

---

## 1. Tổng thời gian dự kiến

Đo thật trên máy này (CPU), giây/tài liệu:

| Profile | s/doc | 203 tài liệu (DocLayNet) | 1403 tài liệu (olmOCR) |
|---|---:|---:|---:|
| `opendataloader_default` | 2.4 | ~8 phút | ~56 phút |
| `docling_default` | 14.9 | ~50 phút | ~5h48 |
| `opendataloader_scan` | 28.1 | ~1h35 | ~10h57 |
| `docling_scan` | 34.7 | ~1h58 | ~13h32 |
| **Tổng** | | **~4h31** | **~31h13** |

**Tổng cộng ~36 giờ máy.** Đó là lý do phải làm theo thứ tự bước 1 → 2 → 3: bước 1 chỉ mất
1 tiếng và đã mở khoá được nhóm B, đủ để kiểm xem đường ống có thông không trước khi đốt
31 tiếng cho bước 3.

---

## 2. Bước 1 — Bật server hybrid (bắt buộc cho mọi profile OpenDataLoader)

`opendataloader_scan` là chế độ **lai**: phần Java gọi sang một server Python
(FastAPI + docling + easyocr) ở `127.0.0.1:5002`. Không bật server thì profile này hỏng
toàn bộ.

**Mở một cửa sổ terminal RIÊNG, chạy lệnh này, rồi để yên nó suốt cả lượt chạy:**

```bash
cd /d/vnpt-projects/sovereign/ocr-bench && PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe scripts/run_odl_hybrid.py
```

### Server bật thành công trông như thế nào

Script tự kiểm tra 9 gói phụ thuộc trước khi bật. Nếu thiếu, nó in JSON rồi **thoát với mã 2**:

```json
{"incompatible": [], "missing": ["fastapi>=0.136.1", "python-multipart>=0.0.28", "uvicorn>=0.46.0"], "versions": {...}}
```

Gặp đúng thông báo này thì cài bản có phần mở rộng `[hybrid]`:

```bash
cd /d/vnpt-projects/sovereign/ocr-bench && ./.venv/Scripts/python.exe -m pip install "opendataloader-pdf[hybrid]==2.5.0"
```

*(Chính chữ `[hybrid]` mới là thứ kéo về fastapi/uvicorn/python-multipart. Cài
`opendataloader-pdf` trơn sẽ luôn thiếu 3 gói này.)*

### Kiểm tra server đã sẵn sàng

```bash
cd /d/vnpt-projects/sovereign/ocr-bench && ./.venv/Scripts/python.exe -c "
import json, pathlib
m = json.loads(pathlib.Path('build/odl-hybrid/manifest.json').read_text(encoding='utf-8'))
print('url        ', m['url'])
print('listener   ', m['listener_pids'])
print('docling    ', m['versions']['docling'])
print('jit        ', m['config']['jit_enforcement'], m['config']['jit_enforcement_method'])
"
```

Phải thấy `jit {'TORCHDYNAMO_DISABLE': '1'} TORCHDYNAMO_DISABLE-before-spawn`.

> 🩹 **Vì sao cần dòng `TORCHDYNAMO_DISABLE` đó.** docling bên trong server gọi
> `torch.compile`. TorchInductor cần trình biên dịch `cl.exe` của MSVC, mà máy này không cài
> Build Tools → **mọi** PDF trả về HTTP 500 `InvalidCxxCompiler`, **trong khi `/health` vẫn
> trả `ok`**. Trước khi vá, lượt chạy hỏng 20/20 tài liệu mà server trông vẫn khoẻ mạnh.
> Bản vá đặt `TORCHDYNAMO_DISABLE=1` vào môi trường tiến trình con trước khi spawn
> (`scripts/run_odl_hybrid.py`), và khai luôn vào manifest để kiểm tra được.
>
> Đã chạy thử 5 tài liệu DocLayNet sau khi vá: **5/5 OK, 0 failed**.

> ⚠️ **Server chết khi bạn đóng terminal.** Đừng bật nó trong một tab rồi đóng tab đi.

---

## 3. Bước 2 — DocLayNet 203 tài liệu → mở khoá nhóm B + C (~4h31)

Danh sách 203 `document_id` đã được chuẩn bị sẵn ở `runs/doclaynet-ids.txt` (phân tách bằng
dấu phẩy, đúng định dạng mà cờ `--only` cần).

**2 profile nhanh trước (~1 giờ):**

```bash
cd /d/vnpt-projects/sovereign/ocr-bench && PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe scripts/run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --hardware cpu --profiles docling_default,opendataloader_default --only "$(cat runs/doclaynet-ids.txt)"
```

**2 profile quét sau (~3h33):**

```bash
cd /d/vnpt-projects/sovereign/ocr-bench && PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe scripts/run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --hardware cpu --profiles docling_scan,opendataloader_scan --only "$(cat runs/doclaynet-ids.txt)"
```

> ⚠️ **`--dataset-manifest datasets/manifest.json` là BẮT BUỘC.**
> Mặc định script đọc `datasets/calibration-manifest.json`, mà file đó hiện chỉ có **1 tài
> liệu** (bản nháp tạm). Quên cờ này là chạy đúng 1 file rồi báo xong.

---

## 4. Bước 3 — olmOCR 1403 tài liệu → mở khoá nhóm A (~31h13)

Không cần `--only`: bỏ cờ đó đi thì script chạy toàn bộ manifest.

**Chạy từng profile một**, đổi tên ở `--profiles`. Chạy từng cái để nếu phải dừng thì bạn
biết chính xác cái nào đã xong:

```bash
cd /d/vnpt-projects/sovereign/ocr-bench && PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe scripts/run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --hardware cpu --profiles opendataloader_default
```

Thứ tự đề nghị (rẻ → đắt): `opendataloader_default` → `docling_default` →
`opendataloader_scan` → `docling_scan`.

**Ngắt giữa chừng hoàn toàn an toàn.** Ctrl-C, rồi lúc nào rảnh chạy lại **đúng lệnh cũ** —
những file đã xong sẽ in `CACHE HIT` và bị bỏ qua.

---

## 5. Bước 4 — Chấm điểm

### 5.1 Nhóm A — khẳng định

```bash
cd /d/vnpt-projects/sovereign/ocr-bench && PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe scripts/score_assertions.py --pred calibration/prediction/cpu | tee runs/pilot/A-assertions.txt
```

> **Script này chỉ in ra màn hình, không tự ghi file.** Phải có `| tee ...` (hoặc `> ...`)
> nếu muốn giữ lại kết quả.

Bảng ra có dạng **loại × tầng**, kèm chú giải quan trọng:

- `(n)` = số tài liệu đã chấm ở ô đó
- `·` = tầng đó **không có** khẳng định loại này (`NO_GROUND_TRUTH`) — đây là câu trả lời đúng
- `HỎNG(n)` = engine chạy hỏng trên n tài liệu — **lượt chạy đó phải làm lại**

Hai ký hiệu cuối cố tình khác nhau. Một lượt hỏng sạch và một bảng lành lặn mà in cùng ký
hiệu thì không phân biệt được.

### 5.2 Nhóm B + C — bố cục và ảnh

```bash
cd /d/vnpt-projects/sovereign/ocr-bench && PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe scripts/build_research_report.py --prediction-dir calibration/prediction/cpu --out runs/pilot
```

> 🚨 **Hai cờ này đều bắt buộc, và mỗi cờ chặn một tai nạn khác nhau:**
>
> - **Thiếu `--prediction-dir`** → chấm nhầm corpus đóng băng ở `prediction/` (các engine
>   `marker`, `noop`, `sabotage`, `pdf_inspector`, `sovereign_full`), **không** phải kết quả
>   bạn vừa chạy. Nó không báo lỗi gì cả.
> - **Thiếu `--out runs/pilot`** → **ghi đè** thư mục `results/`, tức là phá mất bộ đối
>   chiếu dùng để kiểm metric có phân biệt được engine tốt/xấu hay không.

Muốn bản dựng **tái lập được byte-for-byte** thì đặt `SOURCE_DATE_EPOCH` trước khi chạy;
không đặt thì báo cáo lấy đồng hồ máy và hai lần dựng sẽ khác nhau.

---

## 6. Đọc kết quả — 3 điều dễ hiểu nhầm

### 6.1 Docling vẫn N/A ở nhóm ảnh cho tới khi bạn chạy lại nó

Trước 2026-08-13 adapter `docling` (và `pdf_inspector`) dò ra vùng ảnh rồi đổ vào `blocks[]`
mà **không** ghi gì vào `images[]` — đúng chỗ mà `img_f1` / `img_iou` đọc. Nay đã sửa: cả hai
adapter đổ song song vào `blocks` **và** `images`, và cùng khai `image_bbox`.

⚠️ **Nhưng dự đoán đã cache thì không tự cập nhật.** Khoá cache không tính năng lực, nên mọi
kết quả `docling_*` / `pdf_inspector` đang nằm trong `prediction/` vẫn thiếu `images[]` và vẫn
ra `MISSING_CAPABILITY`. Muốn docling có điểm nhóm C thì phải **chạy lại** hai profile docling
(mục 4) — chấm lại corpus cũ không đủ. Chưa chạy lại thì bảng vẫn chỉ có OpenDataLoader ở nhóm C,
và N/A đó là *cache cũ*, không phải giới hạn engine.

### 6.2 Tám metric N/A vẫn nằm trong `raw-results.json`, đừng xoá

`cer`, `wer`, `diacritics_acc`, `nid`, `teds`, `teds_struct`, `cell_f1`, `table_recall` sẽ
xuất hiện với `value: null` + `na_reason`. Giữ nguyên — đó là hồ sơ kiểm toán trả lời câu
*"vì sao không có TEDS"*. Chỉ **bảng in cho người đọc** mới rút gọn.

### 6.3 Nhóm C có hai mẫu số

64 tài liệu **có** ảnh đo *tìm được không*; 140 tài liệu **không** ảnh đo *có bịa ảnh không*.
Gộp thành một cột là mất hẳn chỉ số dương tính giả.

### 6.4 `run-manifest.json` chỉ mô tả lượt chạy **cuối cùng**

Mỗi lượt chạy ghi đè file này. Trong khi đó thư mục `prediction/` thì **tích luỹ** — đầu ra
của các lượt trước vẫn nằm nguyên đó. Nên nếu hôm nay bạn chỉ chạy lại một profile, manifest
sẽ chỉ còn liệt kê đúng profile đó, dù cạnh nó có đầu ra của nhiều profile khác.

Muốn biết corpus hiện tại được sinh ra bởi những lượt nào thì đọc
`<run_root>/run-manifest-history.jsonl` — sổ chỉ-ghi-thêm, mỗi dòng là manifest đầy đủ của
đúng một lượt. Không gộp các dòng lại với nhau: mỗi lượt có commit, thời điểm và phiên bản
thư viện riêng, gộp lại sẽ tạo ra một bản ghi không mô tả lượt chạy nào có thật.

```bash
# xem nhanh: mỗi lượt chạy những profile nào
py -3 -c "import json,sys;[print(r['generated_at'],[p['name'] for p in r['profiles']]) for r in map(json.loads,open(sys.argv[1],encoding='utf-8'))]" calibration/run-manifest-history.jsonl
```

---

## 7. Sự cố thường gặp

| Hiện tượng | Nguyên nhân | Xử lý |
|---|---|---|
| `./.venv/Scripts/python.exe: No such file or directory` | terminal đang ở thư mục khác | thêm `cd /d/vnpt-projects/sovereign/ocr-bench &&` vào đầu lệnh |
| Chạy xong ngay, chỉ 1 tài liệu | quên `--dataset-manifest datasets/manifest.json` | thêm cờ, chạy lại |
| OpenDataLoader hỏng 100%, java exit 1, không có thư mục `.raw/` | server 5002 chưa bật, hoặc bật mà thiếu `TORCHDYNAMO_DISABLE` | xem mục 2 |
| `missing: [fastapi, python-multipart, uvicorn]`, thoát mã 2 | cài `opendataloader-pdf` thiếu `[hybrid]` | `pip install "opendataloader-pdf[hybrid]==2.5.0"` |
| Im lặng 1–3 phút lúc mới chạy | đang nạp vài GB model vào RAM | bình thường, chờ |
| `UserWarning: 'pin_memory'` từ PyTorch | đang chạy `--hardware cpu`, tính năng GPU bị tắt | bình thường, kết quả không ảnh hưởng |
| Bảng ra trông giống hệt lần trước dù vừa chạy xong | quên `--prediction-dir` → chấm nhầm corpus đóng băng | thêm cờ, dựng lại |

---

## 8. Danh sách kiểm tra

- [ ] `cd` về `ocr-bench/`
- [ ] Server hybrid đang chạy ở terminal riêng, manifest có `TORCHDYNAMO_DISABLE`
- [ ] Bước 2 — DocLayNet, 2 profile nhanh (~1h)
- [ ] Bước 2 — DocLayNet, 2 profile quét (~3h33)
- [ ] Bước 3 — olmOCR, 4 profile, từng cái một (~31h)
- [ ] Bước 4.1 — `score_assertions.py` có `| tee`
- [ ] Bước 4.2 — `build_research_report.py` có **cả** `--prediction-dir` **và** `--out runs/pilot`
- [ ] Không lần nào gõ `--refresh`
