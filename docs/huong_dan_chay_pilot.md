# Hướng Dẫn Chạy Thử Nghiệm (Pilot) 6 Profile OCR Benchmark

Tài liệu này hướng dẫn chi tiết cách chạy 6 profile (Docling, OpenDataLoader, Marker) trên 20 file PDF mẫu, đồng thời giải thích rõ kết quả đầu ra và cách hệ thống chấm điểm hoạt động. Hướng dẫn này được viết theo ngôn ngữ phổ thông, dành cho người mới tiếp cận hệ thống.

---

## Phần 1: Cách Chạy 6 Profile Trên 20 File

Để chạy thử nghiệm lấy 20 file chung từ kho dữ liệu thật, bạn cần gọi script (`run_research_predictions.py`) ở chế độ `calibration` kèm theo 2 tham số cực kỳ quan trọng:
- `--dataset-manifest datasets/manifest.json`: Ép hệ thống dùng danh sách data thật (hơn 1600 file) thay vì danh sách nháp.
- `--limit 20`: Yêu cầu hệ thống đọc danh sách từ trên xuống dưới và lấy đúng 20 file đầu tiên. Nhờ cơ chế này, bất kỳ profile nào chạy với lệnh này cũng chắc chắn 100% bốc trúng 20 file đề thi giống hệt nhau.

> 💡 **Mẹo phụ:** Nếu bạn không muốn máy tự động bốc 20 file đầu tiên, mà muốn **chỉ định đích danh** tên các file bạn tự chọn để test, hãy bỏ `--limit 20` đi và dùng cờ `--only`. Ví dụ: `--only bao_cao_tai_chinh,hop_dong_vay`. Khi đó mọi profile sẽ chỉ chạy trên các file bạn chỉ định.

### Các lệnh cần chạy trên Terminal (PowerShell):

Bạn hãy mở PowerShell tại thư mục gốc của dự án (`D:\vnpt-projects\sovereign\ocr-bench`) và lần lượt chạy 3 lệnh sau (tương ứng với 3 môi trường ảo khác nhau của 3 công cụ):

**1. Chạy cặp profile Docling:**
```powershell
# Chạy Docling (cần môi trường ảo của docling)
$env:PYTHONIOENCODING="utf-8"
.\.venv-docling\Scripts\python.exe scripts\run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --limit 20 --profiles docling_default,docling_scan --hardware cpu
```
*(Lưu ý: Bạn thay `\.venv-docling` bằng đường dẫn tới môi trường ảo cài Docling hiện tại của bạn)*

**2. Chạy cặp profile Marker:**
```powershell
# Chạy Marker (môi trường .venv-marker đã có sẵn)
$env:PYTHONIOENCODING="utf-8"
.\.venv-marker\Scripts\python.exe scripts\run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --limit 20 --profiles marker_default,marker_scan --hardware cpu
```

**3. Chạy cặp profile OpenDataLoader:**
```powershell
# Chạy OpenDataLoader (môi trường .venv-odl đã có sẵn và đã được cài đủ 100% thư viện)
$env:PYTHONIOENCODING="utf-8"
.\.venv-odl\Scripts\python.exe scripts\run_research_predictions.py --mode calibration --dataset-manifest datasets/manifest.json --limit 20 --profiles opendataloader_default,opendataloader_scan --hardware cpu
```
*(Cả 2 chế độ default và scan lai AI đều đã được cài đủ thư viện nên sẽ chạy rất mượt)*

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
Để hệ thống tự động đi chấm 20 bài làm này, bạn chỉ cần chạy lệnh:
```powershell
.\.venv\Scripts\python.exe scripts\build_research_report.py --out .
```
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
