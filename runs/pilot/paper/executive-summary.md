# Tóm tắt Thực thi — OCR Parser Benchmark

## Kết quả Tổng quan theo Từng Năng lực

Báo cáo tóm tắt hiệu năng của **4 profile** trên bộ dữ liệu kiểm thử chuẩn. Không sử dụng một điểm số tổng duy nhất để hiển thị trung thực các trade-off.

| Profile | Text & OCR | Layout & Struct | Tables | Reading Order | Robustness |
|---|---|---|---|---|---|
| `docling_default` | 0.533 | 0.555 | 0.303 | 0.297 | 0.226 |
| `docling_scan` | — | 0.610 | 0.000 | — | — |
| `opendataloader_default` | 0.295 | 0.424 | 0.155 | 0.408 | 0.501 |
| `opendataloader_scan` | 0.801 | 0.539 | 0.245 | 0.456 | — |

