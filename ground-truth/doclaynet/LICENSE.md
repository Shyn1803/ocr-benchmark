# DocLayNet — giấy phép và ghi công

**Giấy phép: CDLA-Permissive-1.0** (Community Data License Agreement – Permissive, v1.0)
<https://cdla.dev/permissive-1-0/>

**Cho phép dùng thương mại.** CDLA-Permissive-1.0 cho phép dùng, sửa đổi và phân phối
lại dữ liệu, kể cả trong sản phẩm thương mại, và **không** áp điều kiện copyleft lên
kết quả sinh ra từ dữ liệu (mô hình, số đo, báo cáo). Nghĩa vụ chính: giữ lại thông
báo giấy phép này khi phân phối lại chính dữ liệu.

## Nguồn

- Chủ sở hữu: **IBM Deep Search** (IBM Research)
- Trang: <https://developer.ibm.com/exchanges/data/all/doclaynet/>
- Kho: <https://github.com/DS4SD/DocLayNet>

## Trích dẫn

> Birgit Pfitzmann, Christoph Auer, Michele Dolfi, Ahmed S. Nassar, Peter Staar.
> *DocLayNet: A Large Human-Annotated Dataset for Document-Layout Analysis.*
> KDD 2022. <https://doi.org/10.1145/3534678.3539043>

## Phần được đưa vào repo này

**204 trang / 81.472** của tập `test`, chọn phân tầng theo `doc_category`
(xem `manifest.yaml`). Mỗi trang gồm ba mảnh:

| Mảnh | Trong repo |
|---|---|
| PDF một trang | `pdfs/doclaynet/<hash>.pdf` |
| text cell + metadata | `ground-truth/doclaynet/cells/<hash>.json` |
| hộp bố cục có nhãn | mục trong `ground-truth/doclaynet/layout_coco.json` |

Không đưa PNG (bản gốc 30 GB) vào repo — mọi adapter của bench nhận PDF.
Lấy lại toàn bộ: `py -3 scripts/fetch_doclaynet.py`.
