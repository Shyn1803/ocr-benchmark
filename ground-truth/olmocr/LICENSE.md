# olmOCR-bench — giấy phép và ghi công

**Giấy phép: ODC-BY-1.0** (Open Data Commons Attribution License v1.0)
<https://opendatacommons.org/licenses/by/1-0/>

**Cho phép dùng thương mại, kèm điều kiện ghi công.** ODC-BY cho phép chia sẻ, sửa
đổi và dùng dữ liệu vào bất kỳ mục đích nào, kể cả thương mại, miễn là **ghi công**
nguồn theo cách hợp lý. File này là phần ghi công đó; khi công bố số đo lấy từ bộ
nhãn này ra ngoài, nhắc lại nguồn ở nơi công bố.

Khác hẳn **OmniDocBench** (research-only / phi thương mại) — bộ đó plan §11 đã loại,
không tải về repo và không trích số liệu vào tài liệu nội bộ có giá trị thương mại
khi chưa có rà soát pháp lý.

## Nguồn

- Chủ sở hữu: **Allen Institute for AI (AI2)**
- Bộ dữ liệu: <https://huggingface.co/datasets/allenai/olmOCR-bench>
- Công cụ: <https://github.com/allenai/olmocr>

## Trích dẫn

> Jake Poznanski, Jon Borchardt, Jason Dunkelberger, Regan Huff, Daniel Lin,
> Aman Rangapur, Christopher Wilhelm, Kyle Lo, Luca Soldaini.
> *olmOCR: Unlocking Trillions of Tokens in PDFs with Vision Language Models.*
> arXiv:2502.18443. <https://arxiv.org/abs/2502.18443>

## Phần được đưa vào repo này

**Toàn bộ** bộ nhãn: 1.403 PDF (`pdfs/olmocr/<tầng>/`) + 7 file jsonl chứa **7.019
khẳng định** (`ground-truth/olmocr/*.jsonl`). 7 tầng: `arxiv_math`, `headers_footers`,
`long_tiny_text`, `multi_column`, `old_scans`, `old_scans_math`, `tables`.

Nhãn ở đây là **khẳng định đúng/sai** trên văn bản trích xuất (dạng unit test), không
phải văn bản tham chiếu toàn văn — vì vậy nạp thành `AssertionGT` chứ không phải
`AnnotationGT`. Sáu loại: `math` (3.385), `order` (1.061), `table` (1.020),
`absent` (823), `present` (721), `baseline` (9).

Lấy lại toàn bộ: `py -3 scripts/fetch_olmocr.py`.
