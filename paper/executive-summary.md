# Tóm tắt Thực thi — OCR Parser Benchmark

## Kết quả Tổng quan theo Từng Năng lực

Báo cáo tóm tắt hiệu năng của **7 profile** trên bộ dữ liệu kiểm thử chuẩn. Không sử dụng một điểm số tổng duy nhất để hiển thị trung thực các trade-off.

| Profile | Text & OCR | Layout & Struct | Tables | Reading Order | Robustness |
|---|---|---|---|---|---|
| `marker` | 0.688 | 0.768 | 0.500 | 0.500 | 0.611 |
| `noop` | 0.500 | — | 0.000 | 0.000 | 0.000 |
| `opendataloader` | 0.295 | 0.424 | 0.155 | 0.408 | 0.501 |
| `pdf_inspector` | 0.352 | 0.118 | 0.405 | 0.202 | 0.222 |
| `sabotage` | 0.407 | 0.071 | 0.000 | 0.091 | 0.501 |
| `sovereign_full` | — | — | — | — | — |
| `sovereign_light` | 0.161 | — | 0.002 | 0.108 | 0.019 |

