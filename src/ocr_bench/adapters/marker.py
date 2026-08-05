"""Bộ nối Marker (`marker-pdf`) — A4 (TASK-075).

Marker là ứng viên mạnh nhất của bench: nó trả **đủ sáu kênh** dữ liệu (text, bbox
block, bbox ảnh, bytes ảnh, bảng HTML, cấp mục) trong khi ba engine còn lại đều thiếu
ít nhất một.

Ba điều quyết định hình dạng file này:

1. **`build_document()` gọi đúng một lần.** `PdfConverter.__call__` là
   `build_document()` (đắt: layout + OCR + 27 processor) rồi `renderer(document)` (rẻ).
   Gọi `converter(path)` hai lần để lấy hai kiểu đầu ra là mất gấp đôi thời gian máy —
   200 trang CPU từ ~3h thành ~6h.
2. **Import marker là lười.** `pyproject.toml` chốt rằng `pytest` của repo phải xanh
   trên máy trắng; marker-pdf kéo theo torch + Surya vài GB nên nó là extra, không phải
   dependency. Import ở đầu module thì `import ocr_bench` trên máy trắng sẽ nổ và cả
   registry rụng theo.
3. **`page_x0`/`page_y0` lấy từ `page_info`, không giả định [0,0].** Nhánh `force_ocr`
   của Marker lấy bbox trang từ pdfium và bbox đó có thể không bắt đầu ở gốc. Bỏ qua
   chỗ này thì mọi box lệch một lượng cố định, và IoU ra một con số thấp-nhưng-hợp-lý
   trông y hệt "engine này cắt vùng dở" — cái bẫy nguy hiểm nhất của cả bench.

4. **Số trang lấy từ `id` block, không lấy từ trường `page`.** Trường
   `FlatBlockOutput.page` của Marker 1.10.2 tính sai — nó ra `block_id` của block Page
   chứ không ra số trang. Xem `page_index()`.

Chạy bằng venv riêng (`.venv-marker`, Python 3.12 — torch chưa có bánh xe cho 3.14):

    .venv-marker/Scripts/python.exe scripts/make_predictions.py --engines marker
"""

from __future__ import annotations

import base64
import io
import re
from html import unescape
from pathlib import Path
from typing import Any, ClassVar

from ocr_bench.adapters.base import Adapter
from ocr_bench.types import (
    Box,
    BlockType,
    Capability,
    OcrBlock,
    OcrImage,
    OcrResult,
    OcrTable,
)

__all__ = [
    "MarkerAdapter",
    "BLOCK_TYPE_MAP",
    "map_block_type",
    "heading_level",
    "page_index",
    "html_to_text",
]

# Ánh xạ 28 `BlockTypes` của Marker → 13 `BlockType` của bench. Tường minh, không đoán
# theo tên: `Form` là biểu mẫu (văn bản) chứ không phải hình, `TableOfContents` là bảng
# chứ không phải mục lục dạng heading.
BLOCK_TYPE_MAP: dict[str, BlockType] = {
    "Text": BlockType.TEXT,
    "TextInlineMath": BlockType.TEXT,
    "Handwriting": BlockType.TEXT,
    "Form": BlockType.TEXT,
    "ComplexRegion": BlockType.TEXT,
    "Reference": BlockType.TEXT,
    "SectionHeader": BlockType.HEADING,
    "ListItem": BlockType.LIST,
    "ListGroup": BlockType.LIST,
    "Table": BlockType.TABLE,
    "TableGroup": BlockType.TABLE,
    "TableOfContents": BlockType.TABLE,
    "Picture": BlockType.PICTURE,
    "PictureGroup": BlockType.PICTURE,
    "Figure": BlockType.PICTURE,
    "FigureGroup": BlockType.PICTURE,
    "Caption": BlockType.CAPTION,
    "Footnote": BlockType.FOOTNOTE,
    "PageHeader": BlockType.PAGE_HEADER,
    "PageFooter": BlockType.PAGE_FOOTER,
    "Equation": BlockType.FORMULA,
    "Code": BlockType.CODE,
}

# Loại block trả về ảnh cắt sẵn.
IMAGE_BLOCK_TYPES = frozenset({"Picture", "PictureGroup", "Figure", "FigureGroup"})


def map_block_type(marker_type: str) -> BlockType:
    """Loại lạ rơi vào `OTHER`, **không** bị bỏ.

    Bỏ block là mất recall: bảng sẽ báo Marker sót vùng mà thật ra nó tìm ra rồi. Một
    bản Marker mới thêm loại block là chuyện bình thường; nó không được phép làm điểm
    tụt.
    """
    return BLOCK_TYPE_MAP.get(marker_type, BlockType.OTHER)


def heading_level(html: str) -> int | None:
    """Cấp mục lấy từ thẻ `<h1>`–`<h6>` đầu tiên trong html của block.

    Marker không có kiểu `Title` riêng — `SectionHeader` cấp 1 đóng vai đó, và cấp nằm
    trong html chứ không nằm ở trường nào.
    """
    for level in range(1, 7):
        if f"<h{level}" in html:
            return level
    return None


def page_index(block_id: str, fallback: int) -> int:
    """Số trang lấy từ `id` của block, **không** lấy từ `FlatBlockOutput.page`.

    Marker 1.10.2 tính trường `page` bằng `int(block.id.split("/")[-1])` trên block
    `Page` (`renderers/chunk.py:json_to_chunks`). Nhưng `BlockId.__str__`
    (`schema/blocks/base.py:46`) in block Page ra `/page/0/Page/8` — phần tử cuối là
    **block_id**, không phải số trang. Đo thật trên `pdfs/sample_minimal.pdf` (1 trang):
    `page_info` có đúng khoá `0`, còn mọi block khai `page=8`.

    Tin trường đó thì không block nào tra được trang, tất cả bị bỏ, và Marker — engine
    mạnh nhất của bench — lên bảng với 0 vùng. Đây là kiểu hỏng tệ nhất: nó không ném
    lỗi, nó chỉ làm engine tốt trông như engine tồi.

    `id` thì đúng: `BlockId.__str__` là `/page/{page_id}/{block_type}/{block_id}`.
    """
    phan = block_id.split("/")
    if len(phan) >= 3 and phan[1] == "page":
        try:
            return int(phan[2])
        except ValueError:
            pass
    return fallback


_THE = re.compile(r"<[^>]+>")


def html_to_text(html: str) -> str:
    """Bỏ thẻ, gỡ thực thể, gom khoảng trắng. Dùng để lấy chữ của tiêu đề mục."""
    return " ".join(unescape(_THE.sub(" ", html)).split())


def _section_hierarchy(
    raw: dict[int, object] | None, tieu_de: dict[str, str]
) -> tuple[str, ...]:
    """`{1: BlockId("/page/0/SectionHeader/6")}` → `("Giới thiệu",)`.

    **Giá trị của `section_hierarchy` là `BlockId`, không phải chữ của tiêu đề.**
    `BlockOutput.section_hierarchy` khai `Dict[int, BlockId]`
    (`schema/blocks/base.py:36`). `str()` thẳng nó ra `/page/0/SectionHeader/6` — trông
    như một chuỗi hợp lệ, nên rất dễ tưởng là xong.

    Nhưng đường dẫn mục dạng id thì **không so được với ground truth**: mọi metric đối
    chiếu cấp mục sẽ ra 0 cho từng block, và Marker mang tiếng không dựng được cây mục
    dù nó dựng đúng. Cùng một lớp lỗi với `page_index` và khoá ảnh: sai một cách yên
    lặng và hợp lý.

    Nên phải tra ngược id → chữ. Bảng `tieu_de` dựng từ chính danh sách chunk (mọi
    block top-level của mọi trang), nên hàm này vẫn không cần import gì của Marker.

    Sắp theo **khoá** (cấp), không theo thứ tự chèn của dict: đường dẫn mục đảo cấp là
    một đường dẫn khác.
    """
    if not raw:
        return ()
    return tuple(tieu_de.get(str(raw[k]), str(raw[k])) for k in sorted(raw, key=int))


def _to_png(b64: str) -> bytes:
    """base64 (JPEG theo mặc định của Marker) → **bytes PNG**.

    `OcrImage.data` là PNG theo hợp đồng. Marker xuất theo `OUTPUT_IMAGE_FORMAT`, mặc
    định JPEG. Không quy đổi thì `data` mang hai định dạng khác nhau tuỳ engine và
    metric so ảnh nhận hai kiểu dữ liệu — hỏng âm thầm, không ai thấy trên bảng.
    """
    from PIL import Image

    with Image.open(io.BytesIO(base64.b64decode(b64))) as im:
        buf = io.BytesIO()
        im.convert("RGB").save(buf, format="PNG")
        return buf.getvalue()


def _box(
    bbox: list[float] | tuple[float, float, float, float],
    page: int,
    page_bbox: tuple[float, float, float, float],
) -> Box:
    """Quy đổi một bbox tuyệt đối của Marker về `Box` chuẩn hoá [0,1].

    Marker: gốc trên-trái, y hướng **xuống**, đơn vị điểm PDF → `y_axis="down"`.
    `page_x0`/`page_y0` truyền từ bbox trang thật (xem docstring module).
    """
    px0, py0, px1, py1 = page_bbox
    return Box.from_absolute(
        page=page,
        x0=bbox[0],
        y0=bbox[1],
        x1=bbox[2],
        y1=bbox[3],
        page_width=px1 - px0,
        page_height=py1 - py0,
        page_x0=px0,
        page_y0=py0,
        y_axis="down",
    )


def build_result(
    *,
    engine_version: str,
    doc_id: str,
    capabilities: frozenset[Capability],
    markdown: str,
    chunks: Any,
    block_bboxes: dict[str, tuple[int, list[float]]],
    config_fingerprint: dict[str, object],
) -> OcrResult:
    """Ghép `ChunkOutput` + markdown thành `OcrResult`.

    Tách khỏi `MarkerAdapter.run()` để test được **mà không cần cài marker**: hàm này
    chỉ đụng thuộc tính của `chunks`, không import gì của Marker.

    `block_bboxes` là `{str(block.id): (page_id, bbox)}` lấy từ `document`. Cần nó vì
    khoá của `FlatBlockOutput.images` là id block **con** (Figure nằm trong
    FigureGroup), mà danh sách chunk chỉ có block top-level — không tra bbox ảnh từ
    chunk được.
    """
    page_bbox: dict[int, tuple[float, float, float, float]] = {
        int(pid): tuple(info["bbox"]) for pid, info in chunks.page_info.items()
    }

    # id → chữ của tiêu đề, để giải `section_hierarchy` (vốn trỏ bằng BlockId). Dựng
    # trước vòng lặp vì một block có thể trỏ tới tiêu đề nằm ở TRANG TRƯỚC — cấp mục
    # bắc qua trang, `Document.render` chuyền `section_hierarchy` từ trang này sang
    # trang kia.
    tieu_de: dict[str, str] = {
        str(b.id): html_to_text(b.html)
        for b in chunks.blocks
        if map_block_type(b.block_type) is BlockType.HEADING
    }

    blocks: list[OcrBlock] = []
    tables: list[OcrTable] = []
    images: list[OcrImage] = []
    thieu_trang: set[int] = set()

    for blk in chunks.blocks:
        trang = page_index(blk.id, blk.page)
        pb = page_bbox.get(trang)
        if pb is None:
            # Không rơi về page_width=1: box chuẩn hoá sai còn tệ hơn box thiếu, vì nó
            # vẫn được chấm và kéo điểm xuống mà không để lại dấu vết nào.
            thieu_trang.add(trang)
            continue

        bt = map_block_type(blk.block_type)
        box = _box(blk.bbox, trang, pb)
        blocks.append(
            OcrBlock(
                block_type=bt,
                box=box,
                html=blk.html,
                level=heading_level(blk.html) if bt is BlockType.HEADING else None,
                section_hierarchy=_section_hierarchy(blk.section_hierarchy, tieu_de),
            )
        )

        if bt is BlockType.TABLE:
            # Giữ nguyên chuỗi `<table>` của Marker. TEDS (B2) chấm trên cây HTML; ép
            # thành chuỗi phẳng ở đây là vứt cấu trúc rồi bắt B2 dựng lại.
            tables.append(OcrTable(html=blk.html, box=box))

        for block_id_thô, b64 in (blk.images or {}).items():
            # Khoá của `images` là đối tượng `BlockId`, KHÔNG phải str — dù in ra thì
            # giống hệt `/page/0/Figure/1`. Ép về str ngay tại biên vì hai lẽ:
            #   1. `source_id` đi thẳng vào JSON của `prediction/`, mà `BlockId` không
            #      serialize được → cả lượt chạy đổ ở tài liệu đầu tiên có ảnh.
            #   2. Tra `block_bboxes` (khoá str) bằng `BlockId` chỉ chạy được nhờ
            #      `BlockId.__hash__` tình cờ là `hash(str(self))`. Dựa vào chi tiết
            #      nội bộ của thư viện khác là chỗ hỏng chờ sẵn ở bản sau.
            block_id = str(block_id_thô)
            vt = block_bboxes.get(block_id)
            img_box = box if vt is None else _box(vt[1], vt[0], page_bbox.get(vt[0], pb))
            images.append(OcrImage(box=img_box, data=_to_png(b64), source_id=block_id))

    loi = None
    if thieu_trang:
        loi = (
            "page_info thiếu trang " + ", ".join(str(p) for p in sorted(thieu_trang))
            + " — block của các trang đó bị bỏ"
        )

    return OcrResult(
        engine="marker",
        engine_version=engine_version,
        doc_id=doc_id,
        capabilities=capabilities,
        text_md=markdown,
        blocks=tuple(blocks),
        images=tuple(images),
        tables=tuple(tables),
        page_sizes=tuple(
            (page_bbox[p][2] - page_bbox[p][0], page_bbox[p][3] - page_bbox[p][1])
            for p in sorted(page_bbox)
        ),
        error=loi,
        config_fingerprint=config_fingerprint,
    )


class MarkerAdapter(Adapter):
    name: ClassVar[str] = "marker"
    capabilities: ClassVar[frozenset[Capability]] = frozenset(
        {
            Capability.TEXT_MD,
            Capability.BLOCK_BBOX,
            Capability.IMAGE_BBOX,
            Capability.IMAGE_BYTES,
            Capability.TABLE_HTML,
            Capability.SECTION_HIERARCHY,
        }
    )

    def __init__(self, *, force_ocr: bool = False) -> None:
        self.force_ocr = force_ocr
        self._converter: Any = None

    # ---- phần phải import marker ----------------------------------------

    def _marker_version(self) -> str:
        from importlib.metadata import version

        return version("marker-pdf")

    def converter(self) -> Any:
        """Dựng `PdfConverter` một lần rồi giữ lại.

        Nạp model Surya mất hàng chục giây; dựng lại cho mỗi tài liệu thì phần lớn thời
        gian đo được sẽ là thời gian nạp model, không phải thời gian OCR.
        """
        if self._converter is None:
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict

            self._converter = PdfConverter(
                artifact_dict=create_model_dict(),
                config={"force_ocr": self.force_ocr} if self.force_ocr else None,
            )
        return self._converter

    def version(self) -> str:
        return self._marker_version()

    def config_fingerprint(self) -> dict[str, object]:
        return {
            "marker_version": self._marker_version(),
            "force_ocr": self.force_ocr,
            "use_llm": False,
            "image_extraction_mode": "highres",
        }

    def run(self, doc_path: Path) -> OcrResult:
        from marker.renderers.chunk import ChunkRenderer
        from marker.renderers.markdown import MarkdownRenderer

        conv = self.converter()
        document = conv.build_document(str(doc_path))  # ← đắt, đúng MỘT lần

        markdown = conv.resolve_dependencies(MarkdownRenderer)(document).markdown
        chunks = conv.resolve_dependencies(ChunkRenderer)(document)

        block_bboxes = {
            str(b.id): (b.page_id, list(b.polygon.bbox))
            for b in document.contained_blocks()
        }

        return build_result(
            engine_version=self.version(),
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            markdown=markdown,
            chunks=chunks,
            block_bboxes=block_bboxes,
            config_fingerprint=self.config_fingerprint(),
        )
