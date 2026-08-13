# Hướng Dẫn Chạy Thử Nghiệm (Pilot) 6 Profile OCR Benchmark

Tài liệu này hướng dẫn chi tiết cách chạy 6 profile (Docling, OpenDataLoader, Marker) trên 20 file PDF mẫu, đồng thời giải thích rõ kết quả đầu ra và cách hệ thống chấm điểm hoạt động. Hướng dẫn này được viết theo ngôn ngữ phổ thông, dành cho người mới tiếp cận hệ thống.

---

## Phần 1: Cách Chạy 6 Profile Trên 20 File

Để chạy thử nghiệm lấy 20 file chung từ kho dữ liệu thật, bạn cần gọi script (`run_research_predictions.py`) ở chế độ `calibration` kèm theo 2 tham số cực kỳ quan trọng:
- `--dataset-manifest datasets/manifest.json`: Ép hệ thống dùng danh sách data thật (hơn 1600 file) thay vì danh sách nháp.
- `--limit 20`: Yêu cầu hệ thống đọc danh sách từ trên xuống dưới và lấy đúng 20 file đầu tiên. Nhờ cơ chế này, bất kỳ profile nào chạy với lệnh này cũng chắc chắn 100% bốc trúng 20 file đề thi giống hệt nhau.

> 💡 **Mẹo phụ:** Nếu bạn không muốn máy tự động bốc 20 file đầu tiên, mà muốn **chỉ định đích danh** tên các file bạn tự chọn để test, hãy bỏ `--limit 20` đi và dùng cờ `--only`. Ví dụ: `--only bao_cao_tai_chinh,hop_dong_vay`. Khi đó mọi profile sẽ chỉ chạy trên các file bạn chỉ định.

### Các lệnh cần chạy:

> ⚠️ **Lưu ý hệ điều hành:** Dưới đây là 2 phiên bản lệnh. Nếu bạn dùng **PowerShell** (mặc định của Windows), hãy copy khối lệnh PowerShell. Nếu bạn dùng **Git Bash** (màn hình đen chữ màu), hãy dùng khối lệnh Bash.

**1. Chạy cặp profile Docling:**
- **PowerShell:**
```powershell
$env:PYTHONIOENCODING="utf-8"
.\.venv\Scripts\python.exe scripts\run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --limit 20 --profiles docling_default,docling_scan --hardware cpu
```
- **Git Bash:**
```bash
PYTHONIOENCODING="utf-8" ./.venv/Scripts/python.exe scripts/run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --limit 20 --profiles docling_default,docling_scan --hardware cpu
```

**2. Chạy cặp profile Marker:**
- **PowerShell:**
```powershell
$env:PYTHONIOENCODING="utf-8"
.\.venv-marker\Scripts\python.exe scripts\run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --limit 20 --profiles marker_default,marker_scan --hardware cpu
```
- **Git Bash:**
```bash
PYTHONIOENCODING="utf-8" ./.venv-marker/Scripts/python.exe scripts/run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --limit 20 --profiles marker_default,marker_scan --hardware cpu
```

**3. Chạy cặp profile OpenDataLoader:**

> ⚠️ **ĐẶC BIỆT LƯU Ý VỚI OPENDATALOADER:** Chế độ scan của OpenDataLoader là chế độ "lai" (Hybrid) giữa Java và Python. Do đó, bạn **bắt buộc** phải mở thêm một cửa sổ Terminal (Git Bash/PowerShell) thứ hai, và chạy lệnh bật Server mồi này lên TRƯỚC:
> 
> ```bash
> # Bật ở một tab Terminal mới tinh và cứ để nó chạy ngầm
> # Nếu dùng PowerShell: $env:TORCH_COMPILE_DISABLE=1; $env:PYTHONIOENCODING="utf-8"; .\.venv-odl\Scripts\python.exe scripts\run_odl_hybrid.py
> # Nếu dùng Git Bash:
> TORCH_COMPILE_DISABLE=1 PYTHONIOENCODING="utf-8" ./.venv-odl/Scripts/python.exe scripts/run_odl_hybrid.py
> ```
> 
> Sau khi Server đã chạy, bạn quay lại Terminal chính và chạy lệnh chính:

- **PowerShell:**
```powershell
$env:PYTHONIOENCODING="utf-8"
.\.venv-odl\Scripts\python.exe scripts\run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --limit 20 --profiles opendataloader_default,opendataloader_scan --hardware cpu
```
- **Git Bash:**
```bash
PYTHONIOENCODING="utf-8" ./.venv-odl/Scripts/python.exe scripts/run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --limit 20 --profiles opendataloader_default,opendataloader_scan --hardware cpu
```

> 💡 **Một số hiện tượng bình thường khi chạy:**
> - **Chờ tải model:** Lần chạy đầu tiên có thể mất 1-3 phút im lặng tuyệt đối để tải hàng GB mô hình AI vào RAM.
> - **Tiến trình:** Hệ thống sẽ in ra màn hình từng bước dạng `[docling_default] (1/20) Xử lý abc... OK`.
> - **Cảnh báo `UserWarning: 'pin_memory'`:** Nếu bạn thấy dòng cảnh báo đỏ lè này từ PyTorch, đừng hoảng! Đó chỉ là thông báo cho biết hệ thống đang tắt tính năng của GPU do bạn đang chạy bằng `--hardware cpu`. File vẫn trích xuất thành công 100%.

---

## Phần 2: Dữ Liệu Sau Khi Chạy Trông Sẽ Ra Sao?

Khi các lệnh trên hoàn tất, hệ thống sẽ tự động tạo ra một thư mục `calibration/prediction/cpu/` để chứa kết quả. 

Bên trong thư mục này, kết quả sẽ được chia theo từng tên profile (ví dụ: thư mục `docling_default/`, `marker_scan/`). Mỗi file PDF (ví dụ file `bao_cao_2023.pdf`) sẽ sinh ra 2 loại dữ liệu:

### 1. File Chuẩn Hóa (Ví dụ: `bao_cao_2023.json`)
Đây là "bài làm" đã được chuyển về **ngôn ngữ chung của Benchmark (Schema v3)** để chuẩn bị đi chấm điểm. Mọi công cụ dù hoạt động khác nhau đều phải trả về đúng cấu trúc này:
- **`text`**: Toàn bộ chữ mà máy đọc được.
- **`blocks`**: Các khối văn bản (đoạn văn, tiêu đề) cùng tọa độ chính xác của chúng trên mặt giấy (x, y, width, height).
- **`tables`**: Cấu trúc các bảng biểu (chia rõ dòng, cột, ô nào gộp với ô nào).
- **`reading_order`**: Thứ tự đọc (máy nên đọc đoạn nào trước, đoạn nào sau).
- **`config_fingerprint`**: Bằng chứng chứng minh file này được chạy bằng công cụ gì, phiên bản bao nhiêu, chạy trên CPU hay GPU (để chống gian lận lấy kết quả từ máy khác đập vào).

### 2. Thư mục dữ liệu thô (Ví dụ: `bao_cao_2023.raw/`)
Chứa nguyên xi file kết quả gốc mà công cụ đó sinh ra (chưa bị hệ thống ép chuẩn hóa). 
Ví dụ: Docling thì sinh ra file `docling.json`, Marker thì sinh ra `marker.json`. Cái này dùng để các kỹ sư "khám nghiệm tử thi" xem tại sao công cụ lại nhận dạng sai một ký tự nào đó.

---

## Phần 3: Cách Phân Tích & So Sánh Để Ra Được Benchmark

Sau khi bạn đã có "bài làm" của 6 công cụ trong thư mục `prediction/`, làm thế nào để biết ai giỏi hơn ai? Hệ thống sử dụng một file **Đáp án (Ground Truth)** để đối chiếu.

### 1. File Đáp án (Ground Truth) lấy từ đâu?
Hệ thống đã chuẩn bị sẵn thư mục `ground-truth/`. Đây là đáp án chuẩn do con người (hoặc các tổ chức quốc tế uy tín như DocLayNet, olmOCR) tạo ra. Đáp án cũng được ghi dưới định dạng Schema v3 y hệt như bài làm của các công cụ.

### 2. Quá trình chấm điểm (Scorer) diễn ra thế nào?

> 🚨 **CẢNH BÁO — lệnh dưới đây KHÔNG chấm 20 file bạn vừa chạy.**
>
> Lượt `--mode calibration` ghi kết quả vào `calibration/prediction/cpu/`. Nhưng hàm chấm
> điểm (`_cham()` tại `src/ocr_bench/research_report.py:89`) **chốt cứng** đường dẫn
> `prediction/` và **bỏ qua cả cờ `--input`**. Chạy lệnh dựng báo cáo sau khi calibration
> xong sẽ ra bảng của **corpus đóng băng sẵn trong repo**, không phải của 20 file vừa chạy —
> và nó không hề báo lỗi, nên rất dễ tưởng nhầm là bảng đã cập nhật.
>
> Thêm nữa: `prediction/` chỉ có `marker`, `noop`, `opendataloader`, `pdf_inspector`,
> `sabotage`, `sovereign_full`, `sovereign_light` — **không có `docling`**. Nên kết quả
> Docling vừa chạy không có đường nào lọt vào bảng xếp hạng.
>
> Muốn chấm dữ liệu calibration thì phải nối hai đường đó lại trước (sửa `_cham()` để nhận
> `input_dir`, hoặc chép kết quả sang `prediction/`). Chừng nào chưa nối, đừng đọc báo cáo
> như thể nó phản ánh lượt pilot.

Lệnh dựng báo cáo (trên corpus đóng băng):
```powershell
.\.venv\Scripts\python.exe scripts\build_research_report.py --out .
```

Đặt `SOURCE_DATE_EPOCH` trước khi chạy nếu bạn cần bản dựng **tái lập được** (hai lần dựng ra
byte giống hệt nhau); không đặt thì báo cáo lấy đồng hồ máy và hai lần dựng sẽ khác nhau.

Khi lệnh này chạy, hệ thống `scorer.py` sẽ cầm **Bài làm** (tại `prediction/`) và soi với **Đáp án** (tại `ground-truth/`), sau đó dùng các "Thước đo" (Metrics) để trừ điểm:

- **Năng lực OCR (Nhận diện chữ):** Dùng thước đo CER (Đếm xem nhận dạng sai bao nhiêu ký tự, mất bao nhiêu dấu phẩy, dấu chấm).
- **Năng lực Bố cục (Layout):** Đo xem cái hộp vuông (bounding box) khoanh quanh đoạn văn của máy khoanh có khớp với cái hộp của đáp án không (chỉ số F1 và IoU).
- **Năng lực Kẻ bảng (Tables):** So sánh cấu trúc bảng (chỉ số TEDS). Nếu máy kẻ sót 1 cột hoặc gộp sai 2 ô, điểm sẽ bị tụt.
- **Năng lực Thứ tự (Reading Order):** Xem máy có bị đọc nhầm cột báo bên trái vắt sang cột báo bên phải không.

### 3. Sinh ra báo cáo so sánh (Report)
Cuối cùng, hệ thống sẽ gom tất cả các điểm số đó, chạy các phép thử thống kê khoa học để đảm bảo sự chênh lệch là đáng tin cậy (chứ không phải do ăn may), và tự động tạo ra file `paper-vi.md` và `executive-summary.md`.

Trong báo cáo, bạn sẽ thấy các công cụ được xếp hạng rành mạch:
- Bảng 1: Nhóm OCR (Ai đọc tiếng Việt chuẩn nhất).
- Bảng 2: Nhóm Bảng biểu (Ai kẻ bảng xịn nhất).
- Không có chuyện cộng dồn điểm lại thành 1 con số vô nghĩa. Máy A đọc chữ dở nhưng kẻ bảng giỏi sẽ được ghi nhận rõ ràng sự đánh đổi (trade-off) đó so với Máy B!
