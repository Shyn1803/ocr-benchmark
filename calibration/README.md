# Calibration Guidelines & Decision History

Thư mục này lưu trữ quy trình hiệu chuẩn thông số profile và nhật ký quyết định (decision log) trước khi đóng băng cấu hình phục vụ lượt chạy công bố chính thức.

## Quy tắc Hiệu chuẩn
1. Mọi hiệu chuẩn chỉ được chọn trong không gian thông số đã khai trước (pre-declared search space):
   - `force_ocr` (`true`/`false`)
   - `ocr_languages` (`["vi", "en"]`)
   - `table_mode` (`default`/`accurate`)
   - `cell_matching` (`true`/`false`)
2. Việc hiệu chuẩn chỉ thực hiện trên tập mẫu calibration độc lập (stratified sample 5 tài liệu/nhóm, seed `20260811`), không sử dụng tập test chính để điều chỉnh thông số.
