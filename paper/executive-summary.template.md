# Tóm tắt Thực thi — OCR Parser Benchmark

## Kết quả Tổng quan theo Nhóm Năng lực

Báo cáo tóm tắt cho lãnh đạo và kiến trúc sư hệ thống về hiệu năng relative của 8 engine profiles trên bộ dữ liệu kiểm thử chuẩn.

<!-- table: executive-summary-matrix -->

## Các Điểm Cần Lưu Ý Khi Triển Khai
- Đối với tài liệu thuần văn bản tiếng Việt: Các profile hỗ trợ EasyOCR tiếng Việt (`vi,en`) nâng cao đáng kể độ chính xác dấu thanh (`diacritics`).
- Đối với phân tích bảng phức tạp: `docling_scan` và `opendataloader_scan` cung cấp độ chính xác cấu trúc ô cao nhất.
- Tài nguyên tính toán: Xem biểu đồ `figures/accuracy-speed.svg` và `figures/capability-ranking.svg`.
