# Tóm tắt Thực thi — OCR Parser Benchmark

## Kết quả Tổng quan theo Nhóm Năng lực

Báo cáo tóm tắt cho lãnh đạo và kiến trúc sư hệ thống về hiệu năng relative của 8 engine profiles trên bộ dữ liệu kiểm thử chuẩn.

| Profile | Text OCR | Bố cục | Bảng | Tốc độ | Nhóm Năng lực Tổng thể |
|---|---|---|---|---|---|
| `marker_scan` | Band A | Band A | Band A | Trung bình | **Band A** |
| `docling_scan` | Band A | Band A | Band A | Trung bình | **Band A** |
| `opendataloader_scan` | Band A | Band A | Band A | Nhanh | **Band A** |
| `sovereign_scan` | Band A | Band A | Band A | Nhanh | **Band A** |
| `marker_default` | Band A | Band A | Band B | Nhanh | **Band A** |
| `docling_default` | Band B | Band B | Band B | Nhanh | **Band B** |
| `sovereign_default` | Band B | Band B | Band B | Rất nhanh | **Band B** |
| `opendataloader_default` | Band B | Band B | Band B | Rất nhanh | **Band B** |


## Các Điểm Cần Lưu Ý Khi Triển Khai
- Đối với tài liệu thuần văn bản tiếng Việt: Các profile hỗ trợ EasyOCR tiếng Việt (`vi,en`) nâng cao đáng kể độ chính xác dấu thanh (`diacritics`).
- Đối với phân tích bảng phức tạp: `docling_scan` và `opendataloader_scan` cung cấp độ chính xác cấu trúc ô cao nhất.
- Tài nguyên tính toán: Xem biểu đồ `figures/accuracy-speed.svg` và `figures/capability-ranking.svg`.
