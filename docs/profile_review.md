# Đánh Giá Chi Tiết 8 Profile Công Cụ OCR & Bố Cục (Dành Cho Người Mới)

Dự án này là một Benchmark (bài kiểm tra chuẩn) để chấm điểm 4 "họ" công cụ OCR (nhận diện chữ) và phân tích bố cục PDF phổ biến nhất hiện nay. Để công bằng, mỗi công cụ sẽ được thi ở **2 hạng mục** (Profile):
- **`default`**: Chuyên dùng cho file PDF gốc (PDF sinh từ Word/Excel, text máy tính có sẵn).
- **`scan`**: Chuyên dùng cho file PDF dạng ảnh chụp, tài liệu scan mờ nhòe (bắt buộc phải chạy AI nhận diện chữ).

Tổng cộng chúng ta có $4 \times 2 = 8$ thí sinh (profiles). Dưới đây là giải thích chi tiết cho từng cấu hình:

---

## 1. Mức độ sẵn sàng: Cái nào có thể chạy được ngay?

Dựa trên tài liệu bàn giao (`2026-08-11-ocr-parser-benchmark-execution-handoff.md`), tình trạng sẵn sàng của 8 profile như sau:

| Profile | Tình trạng chạy thực tế | Môi trường ảo (Venv) cần dùng |
| :--- | :--- | :--- |
| **`docling_default`** | 🟢 **Sẵn sàng** (Đã test pass 100%) | `[dev,docling]` (hoặc venv py312) |
| **`docling_scan`** | 🟢 **Sẵn sàng** (Đã test pass 100%) | `[dev,docling]` (hoặc venv py312) |
| **`marker_default`** | 🟢 **Sẵn sàng** (Đã test pass 100%) | `.venv-marker` |
| **`marker_scan`** | 🟢 **Sẵn sàng** (Đã test pass 100%) | `.venv-marker` |
| **`opendataloader_default`** | 🟢 **Sẵn sàng** (Java thuần) | `.venv-odl` (cần cài Java) |
| **`opendataloader_scan`** | 🟡 **Chưa sẵn sàng hoàn toàn** | `.venv-odl` (Đang báo thiếu 5 thư viện hybrid) |
| **`sovereign_default`** | 🟡 **Đang phát triển dở dang** (Task 6) | `.venv-sov` |
| **`sovereign_scan`** | 🟡 **Đang phát triển dở dang** (Task 6) | `.venv-marker` |

**Kết luận:** Nhóm `docling` và `marker` cùng `opendataloader_default` đã có thể chạy được ngay. Các profile còn lại cần hoàn thiện code/cài cắm thêm thư viện (như đã ghi trong Task 6, Task 7).

---

## 2. Từng Profile sẽ chạy những gì? (Cơ chế hoạt động)

Mỗi công cụ có một triết lý hoạt động riêng, cấu hình được hệ thống quy định chặt chẽ trong file `configs/profiles.json`.

### Họ 1: Docling (IBM)
Công cụ siêu mạnh về đọc bảng biểu và phân tích bố cục phức tạp.
- **`docling_default`**: Ưu tiên đọc chữ số hóa có sẵn trong PDF. Chỉ gọi EasyOCR khi vấp phải ảnh. Xử lý bảng ở mức mặc định (`table_mode: default`), không ép ghép nối từng ô.
- **`docling_scan`**: Ép buộc phải quét ảnh toàn bộ trang (`force_full_page_ocr: true`) bằng EasyOCR (tiếng Anh + Việt). Bật thuật toán nhận diện bảng cao cấp nhất (`table_mode: accurate`), ép căn chỉnh từng cell (`cell_matching: true`).

### Họ 2: OpenDataLoader
Công cụ được tinh chỉnh đặc biệt, lai giữa Java và AI.
- **`opendataloader_default`**: Hoàn toàn không dùng AI năng nặng. Chạy bằng ngôn ngữ Java, dùng thuật toán gom cụm (`cluster`) để tìm bảng và thuật toán cắt XY (`xycut`) để xác định thứ tự đọc chữ từ trên xuống dưới. Siêu nhanh!
- **`opendataloader_scan`**: Là chế độ "Hybrid" (Lai). Nó sẽ gọi một server Python chạy cục bộ (`docling-fast`). Ép quét OCR (tiếng Việt, Anh) toàn bộ tài liệu bằng EasyOCR. Tuy nhiên, hiện tại thư viện cho server lai này đang bị thiếu.

### Họ 3: Marker
Công cụ AI đang rất nổi, biến PDF thẳng thành Markdown.
- **`marker_default`**: Đọc PDF chữ thông thường. Tuyệt đối **không** dùng LLM (`use_llm: false`) để tránh bịa chữ. Cố gắng trích xuất chữ có sẵn, không ép chạy OCR.
- **`marker_scan`**: Bật chế độ cày ải ảnh chụp (`force_ocr: true`), dùng AI nhận diện từng điểm ảnh. Vẫn cấm tuyệt đối LLM.

### Họ 4: Sovereign
Hệ thống lõi nội bộ của team (Backend).
- **`sovereign_default`**: Dùng engine mặc định của backend. Đã khóa hoàn toàn kết nối API ra ngoài (`api_enabled: false`) và khóa API Vision (`ocr_use_vision_api: false`) để đảm bảo bảo mật và tính tất định. Không liên kết với Marker.
- **`sovereign_scan`**: Tương tự như default, nhưng được tích hợp thêm sức mạnh của Marker (`marker_available: true`) để chuyên trị các tài liệu scan phức tạp.

---

## 3. Chúng sẽ được chạy trên Data nào?

Toàn bộ 8 thí sinh sẽ phải làm chung một bài thi duy nhất để đảm bảo công bằng.
- **Nguồn Data**: Nằm trong thư mục `datasets/`. Dữ liệu này được tổng hợp từ các bộ test công khai chuẩn quốc tế (như **DocLayNet** và **olmOCR-bench**).
- **Quy trình test (Task 12)**: 
  - Ban đầu, tất cả sẽ thi thử trên một tập **Pilot (10 tài liệu chung)** để xem có lỗi sập nguồn hay tốn quá nhiều RAM không.
  - Nếu qua vòng Pilot, chúng sẽ chạy trên toàn bộ tập dữ liệu thật được khai báo trong file `datasets/manifest.json`.

---

## 4. Output (Đầu ra) của từng cái sẽ ra sao?

Khi một profile chạy xong 1 file PDF (ví dụ `tai_lieu.pdf`), hệ thống sẽ sinh ra kết quả trong thư mục `prediction/`. Output được chuẩn hóa theo định dạng **Schema v3**, bao gồm 2 phần chính:

1. **Dữ liệu chuẩn hóa (Canonical)**:
   Mọi công cụ dù chạy kiểu gì cũng phải trả về chung 1 format giống nhau (để hệ thống chấm điểm tự động):
   - Chữ đọc được là gì?
   - Thứ tự đọc (Reading Order) đi từ đoạn nào sang đoạn nào?
   - Bảng biểu được cấu trúc ra sao (row, column, header)?
   - Tọa độ (Bounding Box) của từng câu chữ nằm ở đâu trên hình.
   - **Bằng chứng phần cứng (Provenance)**: Đóng dấu rõ file này được chạy trên CPU hay GPU, cấu hình phần cứng ra sao, để chống gian lận.

2. **Dữ liệu thô (Raw Sidecar)**:
   Nằm trong thư mục `<document>.raw/`. Chứa các file kết quả gốc chưa chỉnh sửa của công cụ (ví dụ `docling.json` hay `docling-map.json`). Dùng để kỹ sư sau này mở ra xem xét lại nếu bị chấm điểm kém.

**Tóm lại:** Dù là Docling, Marker hay Sovereign... đầu ra cuối cùng đều bị ép phải trả về một file cấu trúc JSON/Markdown chung, nhờ đó Report Builder mới có thể dùng bộ chấm điểm (`scorer.py`) soi xét từng lỗi sai và gen ra cái báo cáo 6 năng lực mà tôi vừa sửa ban nãy!
