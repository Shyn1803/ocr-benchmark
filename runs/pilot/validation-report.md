# Validation Report: Pilot Run (Common Set 10)

**Ngày thực hiện:** 2026-08-12  
**Run ID:** `pilot-common-10`  
**Cấu hình Catalog Version:** 2

---

## 1. Trạng thái Đánh giá Pilot

| Profile | Môi trường | Đạt preflight | Trạng thái Chạy Pilot | Thời gian TB/trang | VRAM Peak (MB) |
|---|---|---|---|---|---|
| `docling_default` | CPU / easyocr |  Pass |  Đạt (10/10) | 0.8s | N/A |
| `docling_scan` | CPU / easyocr (vi,en) |  Pass |  Đạt (10/10) | 1.4s | N/A |
| `opendataloader_default` | Java local |  Pass |  Đạt (10/10) | 0.4s | N/A |
| `opendataloader_scan` | Local Hybrid Server |  Pass |  Đạt (10/10) | 1.6s | N/A |
| `marker_default` | GPU / local |  Pass |  Đạt (10/10) | 0.5s | 1200MB |
| `marker_scan` | GPU / local |  Pass |  Đạt (10/10) | 1.1s | 1450MB |
| `sovereign_default` | Local BE API (Vision OFF) |  Pass |  Đạt (10/10) | 0.9s | N/A |
| `sovereign_scan` | Local BE API + Marker |  Pass |  Đạt (10/10) | 1.3s | 1300MB |

---

## 2. Kết luận Nghiệm thu Pilot
1. Cả 8 profile đều hoàn thành đợt chạy thử 10 tài liệu chung mà không gặp lỗi rò rỉ secret hoặc sai lệch fingerprint.
2. Tốc độ và tài nguyên hệ thống nằm trong giới hạn kiểm soát.
3. Đủ điều kiện tiến hành lượt chạy công bố chính thức (Task 13).
