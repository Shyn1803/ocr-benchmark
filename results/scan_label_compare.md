# Bất đồng nhãn “cần OCR” — bộ `doclaynet` (n=204)

Sinh bởi `scripts/compare_scan_label.py`. Ngưỡng Sovereign: khớp — openrouter_document_parser.py: `needs = chars_per_page < 50 or len(text) < 100`

**Không bộ nào là ground truth.** DocLayNet gán nhãn bố cục, không gán nhãn
“text layer”. Bảng dưới đo *sự bất đồng*, không xếp hạng đúng/sai.

## Bất đồng từng cặp

| Cặp | Lệch | % |
|---|---:|---:|
| `classify_pdf` vs `extract_pages_markdown` (**cùng thư viện**) | 22 | 10.8% |
| `classify_pdf` vs Sovereign | 4 | 2.0% |
| `extract_pages_markdown` vs Sovereign | 24 | 11.8% |

Ba bộ đồng thuận: **179/204** (87.7%).

### Phân bố `pdf_type`

| Giá trị | Số | % |
|---|---:|---:|
| text_based | 189 | 92.6% |
| scanned | 10 | 4.9% |
| image_based | 5 | 2.5% |

### Tổ hợp ba phán quyết

| Giá trị | Số | % |
|---|---:|---:|
| classify=0 pages=0 sovereign=0 | 168 | 82.4% |
| classify=0 pages=1 sovereign=0 | 18 | 8.8% |
| classify=1 pages=1 sovereign=1 | 11 | 5.4% |
| classify=1 pages=0 sovereign=1 | 3 | 1.5% |
| classify=0 pages=0 sovereign=1 | 3 | 1.5% |
| classify=1 pages=0 sovereign=0 | 1 | 0.5% |

## Bất đồng theo loại tài liệu (AC-04)

| Loại | n | classify≠pages | classify≠sovereign | pages≠sovereign |
|---|---:|---:|---:|---:|
| financial_reports | 34 | 2 | 2 | 4 |
| government_tenders | 34 | 0 | 0 | 0 |
| laws_and_regulations | 34 | 4 | 0 | 4 |
| manuals | 34 | 1 | 1 | 0 |
| patents | 34 | 15 | 0 | 15 |
| scientific_articles | 34 | 0 | 1 | 1 |

## Ca đáng ngại: `classify_pdf` bất đồng với chính thư viện mình **ở conf=1.00**

**18/22** ca bất đồng có `confidence = 1.00`. Độ tin cậy của
`classify_pdf` **không** dùng được làm cổng chặn — nó tự tin ngay ở chỗ nó lệch.

| doc | loại | pdf_type | conf | classify | pages | sovereign | chars/trang |
|---|---|---|---:|---|---|---|---:|
| `166041d9317b` | laws_and_regulations | text_based | 1.00 | False | True | False | 3961.0 |
| `190774629a25` | patents | text_based | 1.00 | False | True | False | 6641.0 |
| `304c1d231ac6` | patents | text_based | 1.00 | False | True | False | 4150.0 |
| `3221cb93f983` | laws_and_regulations | text_based | 1.00 | False | True | False | 4216.0 |
| `3de34e2ac095` | laws_and_regulations | text_based | 1.00 | False | True | False | 657.0 |
| `3e00231419b4` | patents | text_based | 1.00 | False | True | False | 1881.0 |
| `44f401a12f88` | patents | text_based | 1.00 | False | True | False | 4971.0 |
| `6b981a958f7d` | patents | text_based | 1.00 | False | True | False | 205.0 |
| `7e4d03325ebb` | patents | text_based | 1.00 | False | True | False | 131.0 |
| `89d44ab3dc6c` | patents | text_based | 1.00 | False | True | False | 1493.0 |
| `8ca8795058ee` | patents | text_based | 1.00 | False | True | False | 307.0 |
| `908f83f51ee2` | patents | text_based | 1.00 | False | True | False | 1036.0 |
| `92ca38114851` | laws_and_regulations | text_based | 1.00 | False | True | False | 418.0 |
| `9fccb657d9f0` | patents | text_based | 1.00 | False | True | False | 209.0 |
| `a199b5dceac0` | patents | text_based | 1.00 | False | True | False | 173.0 |
| `a8378ad494a6` | patents | text_based | 1.00 | False | True | False | 129.0 |
| `b4edd6ffdde4` | patents | text_based | 1.00 | False | True | False | 5992.0 |
| `edd710f64005` | patents | text_based | 1.00 | False | True | False | 1668.0 |
