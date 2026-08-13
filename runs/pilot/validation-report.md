# Pilot run (common set 10) — **CHƯA CÓ LƯỢT CHẠY NÀO SINH RA FILE NÀY**

**Run ID:** `pilot-common-10`
**Trạng thái:** `dang_chay_do` (2/8 profile có đầu ra, 6/8 chưa)
**Ngày ghi nhận:** 2026-08-12
**Nhánh:** `feature/ocr-parser-benchmark-research-v2`

---

## 1. Thu hồi bản trước

Bản `validation-report.md` trước đó của file này ghi cả 8 profile đều "Đạt (10/10)",
kèm thời gian trung bình mỗi trang (0.4s–1.6s) và VRAM đỉnh (1200–1450 MB).

**Toàn bộ những con số đó là bịa.** Không có lượt chạy nào sinh ra chúng:

- không có tệp kết quả nào dưới `runs/pilot/` ngoài chính hai file này;
- không có manifest nào trỏ tới tài liệu, checksum, hay dòng log của một lượt chạy;
- không có adapter nào trong repo có handshake báo thiết bị, nên con số VRAM không có
  đường nào để đo được — kể cả nếu lượt chạy đã thật sự diễn ra.

Bản này thay thế nó. Bản cũ còn trong lịch sử git để đối chiếu; không dùng lại số nào
từ đó.

## 2. Hiện trạng thật (kiểm 2026-08-12 trên repo chính)

Môi trường ở đây **tách venv theo engine**, không phải một `.venv` chung:

| venv | `docling` | `marker` | `opendataloader_pdf` |
|---|---|---|---|
| `.venv` | có | không | có |
| `.venv-marker` | không | có | không |
| `.venv-odl` | có | không | có |
| `.venv-pi`, `.venv-sov` | không | không | không |

`java` **không có trên PATH** — nhánh hybrid của OpenDataLoader cần `scripts/run_odl_hybrid.py`
chạy song song ở terminal thứ hai (xem `docs/huong_dan_chay_pilot.md` §1.3).

Tiến độ đầu ra thật, đếm dưới `calibration/prediction/cpu/`:

| Profile | Số tài liệu có đầu ra |
|---|---|
| `docling_default` | 20 |
| `docling_scan` | 20 |
| `marker_default`, `marker_scan` | 0 — chưa chạy |
| `opendataloader_default`, `opendataloader_scan` | 0 — chưa chạy |
| `sovereign_default`, `sovereign_scan` | 0 — chưa chạy |

Tức **2/8 profile** đã có đầu ra. Đó là lượt `calibration --limit 20`, **không phải** common
set 10 mà file này mang tên.

## 3. Điều này chặn gì

- Task 12 (nghiệm thu pilot) **chưa hoàn thành**. Không có kết luận "đủ điều kiện tiến
  hành lượt chạy công bố" khi mới 2/8 profile có đầu ra.
- Mọi bảng công bố hiện tại dựng từ `prediction/` đã đóng băng sẵn trong repo, **không**
  từ lượt chạy calibration này. Hai nguồn đó không được trộn lẫn khi báo cáo.
- ⚠️ **`scripts/build_research_report.py` không đọc `calibration/`.** Hàm `_cham()` trong
  `src/ocr_bench/research_report.py:89` chốt cứng `ROOT / "prediction"` và bỏ qua cả cờ
  `--input`. Chạy calibration xong rồi dựng báo cáo sẽ ra bảng của corpus đóng băng, **không
  phải** của 20 file vừa chạy — mà không có cảnh báo nào. Thêm nữa `prediction/` không hề
  có engine `docling`, nên không có đường nào để 20 file Docling vừa chạy lọt vào bảng.

## 4. Muốn gỡ thì cần gì

1. Chạy nốt 6 profile còn lại (Marker, OpenDataLoader, `sovereign_*`); OpenDataLoader cần
   `run_odl_hybrid.py` bật trước; `sovereign_*` cần BE API cục bộ.
2. Nối được đầu ra `calibration/` vào đường chấm điểm — hoặc sửa `_cham()` để nhận
   `input_dir`, hoặc chép vào `prediction/`. Chừng nào chưa nối thì đừng đọc bảng công bố
   như thể nó phản ánh lượt pilot.
3. Sinh `run-manifest.json` có checksum từng tài liệu.
4. Chỉ khi đó mới viết lại file này bằng số đo thật — và **không khai CPU/GPU/VRAM** nếu
   adapter vẫn chưa có handshake chứng minh thiết bị.
