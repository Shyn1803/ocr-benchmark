"""Bộ nối OpenDataLoader (`opendataloader-pdf`) — A5 (TASK-076).

OpenDataLoader không phải thư viện Python: gói pip chỉ là lớp bọc mỏng gọi một file
`.jar` bằng lệnh `java`. Bốn điều quyết định hình dạng file này, **cả bốn đều là kết
quả đo, không phải suy từ tài liệu**:

1. **Hệ toạ độ: gốc DƯỚI-trái, y hướng LÊN, đơn vị điểm PDF, `[x0, y0, x1, y1]`.**
   Đo bằng `scripts/measure_opendataloader_coords.py` trên PDF tự dựng, chữ đặt ở
   toạ độ biết trước. Khác Marker (gốc TRÊN-trái, y xuống) — nên `y_axis="up"`.

   Phép đo 4 của script đó lật ngược một giả định dễ mắc: dựng lại trang với
   MediaBox dịch đi (100, 200) thì box trả về **không đổi một chút nào**
   (Δx=0.00, Δy=0.00) → OpenDataLoader **đã tự trừ gốc MediaBox**, khác Marker.
   Nên ở đây `page_x0`/`page_y0` phải để **0**; chép theo Marker mà truyền
   `mb.left`/`mb.bottom` vào là trừ hai lần, và mọi box lệch đúng một lượng cố
   định trên mọi tài liệu có MediaBox không bắt đầu từ gốc.

2. **JSON của nó KHÔNG có kích thước trang.** Khoá cấp cao chỉ có `file name`,
   `number of pages`, `author`, `title`, ngày tháng, `kids`. Không có node trang,
   không có `width`/`height` ở bất kỳ đâu — kiểm bằng cách đổ toàn bộ node của 24
   tài liệu. Mà `Box.from_absolute` cần chiều trang để chuẩn hoá. Nên kích thước
   lấy từ **MediaBox đọc bằng `pypdf`** — cùng lối `corpus.py` lấy kích thước trang
   DocLayNet từ metadata file cell chứ không từ COCO.

3. **`page number` là 1-indexed.** A0 mới chỉ cảnh báo `row number`/`column number`
   của bảng; đo thật thì số trang cũng vậy. Bench 0-based khắp nơi (`Box(page=-1)`
   bị chặn), nên trừ 1 ngay tại biên. Không trừ thì mọi box lệch đúng một trang:
   tài liệu 1 trang thì rụng sạch, tài liệu nhiều trang thì IoU ra một con số
   thấp-nhưng-hợp-lý — đúng lớp hỏng yên lặng mà A4 đã dính ba lần.

4. **Bảng chỉ hiện ra với `table_method="cluster"`.** Mặc định của engine là
   `default` (dò theo đường kẻ). Chạy 4 tài liệu mà DocLayNet gắn nhãn nhiều bảng
   nhất (5, 4, 4, 3 bảng): `default` ra **0** node `table`, `cluster` ra bảng có đủ
   `rows`/`cells`/`row span`/`column span`. Để mặc định là tự nguyện bỏ toàn bộ
   nhóm metric bảng (B2).

Chạy bằng venv riêng (`.venv-odl`) và cần JRE — dựng bằng `scripts/setup_java.py`:

    py -3 scripts/setup_java.py
    .venv-odl/Scripts/python.exe scripts/make_predictions.py --engines opendataloader
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from html import escape
from pathlib import Path
from typing import Any, ClassVar, Iterator

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
    "OpenDataLoaderAdapter",
    "BLOCK_TYPE_MAP",
    "map_block_type",
    "node_phang",
    "node_khoi",
    "chay_cli",
    "kich_thuoc_trang",
    "bang_sang_html",
    "chu_cua_node",
    "build_result",
]

# 8 `type` quan sát được trên 24 tài liệu → `BlockType` của bench.
# `text block` là khung gom nhiều đoạn, không phải một khối nội dung — nó được đi
# xuyên qua trong `node_khoi()` chứ không tự thành block.
BLOCK_TYPE_MAP: dict[str, BlockType] = {
    "paragraph": BlockType.TEXT,
    "heading": BlockType.HEADING,
    "list": BlockType.LIST,
    "list item": BlockType.LIST,
    "image": BlockType.PICTURE,
    "caption": BlockType.CAPTION,
    "table": BlockType.TABLE,
    "table cell": BlockType.TABLE,
}

# Nút chỉ để gom, không tự là một khối nội dung.
KHUNG_GOM = frozenset({"text block"})

# Khoá chứa con. `list` để con ở `list items`, `table` ở `rows`, `table row` ở
# `cells` — không phải `kids` như mọi node khác. Dò thiếu một khoá là mất im lặng
# cả nhánh cây.
KHOA_CON = ("kids", "list items", "rows", "cells")


def map_block_type(odl_type: str) -> BlockType:
    """Loại lạ rơi vào `OTHER`, **không** bị bỏ — cùng lý do như Marker: bỏ block là
    mất recall, và bản engine mới thêm loại node không được phép làm điểm tụt."""
    return BLOCK_TYPE_MAP.get(odl_type, BlockType.OTHER)


# --------------------------------------------------------------------------
# Đi cây
# --------------------------------------------------------------------------


def node_phang(node: Any) -> Iterator[dict]:
    """Duyệt **toàn bộ** node, kể cả con của list item và ô bảng.

    Dùng cho việc dò/đo (`scripts/measure_opendataloader_coords.py`), không dùng để
    dựng block — dựng block bằng hàm này sẽ đếm trùng: `list` và `list item` và
    `paragraph` bên trong list item đều có `bounding box` chồng nhau.
    """
    if isinstance(node, list):
        for c in node:
            yield from node_phang(c)
        return
    if not isinstance(node, dict):
        return
    if "type" in node:
        yield node
    for khoa in KHOA_CON:
        if khoa in node:
            yield from node_phang(node[khoa])


def node_khoi(doc: dict) -> Iterator[dict]:
    """Duyệt đúng tầng khối nội dung — mô hình phẳng, khớp DocLayNet.

    Quy tắc, mỗi cái đều để tránh đếm trùng hoặc đếm thiếu:

    * `list` → đi xuống `list items`, **không** phát chính nó. DocLayNet gắn nhãn
      từng `List-item` một, không gắn nhãn cả cụm danh sách.
    * `list item` → phát, **không** đi xuống `kids`. Con của nó là `paragraph`
      có box gần trùng; phát cả hai là nhân đôi vùng và precision tụt vô cớ.
    * `table` → phát chính nó, **không** đi xuống ô. Ô đi vào `OcrTable.html`.
    * `text block` → chỉ là khung gom, đi xuyên qua.
    """
    def di(node: Any) -> Iterator[dict]:
        if isinstance(node, list):
            for c in node:
                yield from di(c)
            return
        if not isinstance(node, dict):
            return
        t = node.get("type")
        if t == "list":
            yield from di(node.get("list items", []))
        elif t in KHUNG_GOM or t is None:
            yield from di(node.get("kids", []))
        else:
            yield node

    yield from di(doc.get("kids", []))


def chu_cua_node(node: Any) -> str:
    """Gom `content` của node và mọi con của nó, giữ thứ tự đọc.

    `list item` và `table cell` không có `content` của riêng chúng — chữ nằm ở
    `paragraph` con. Lấy thẳng `node["content"]` thì mọi mục danh sách và mọi ô
    bảng ra chuỗi rỗng.
    """
    phan: list[str] = []
    for n in node_phang(node):
        if c := (n.get("content") or "").strip():
            phan.append(c)
    return " ".join(phan)


# --------------------------------------------------------------------------
# Gọi engine
# --------------------------------------------------------------------------


def _java() -> Path:
    """`java` dùng được, ưu tiên bản bỏ túi trong `.tools/`.

    `opendataloader_pdf.runner.run_jar` ghi cứng chuỗi `"java"` trong `command` —
    nó không nhận đường dẫn, không đọc `JAVA_HOME`. Nên cách duy nhất để trỏ nó
    vào JRE của `.tools/` là chèn thư mục `bin` đó lên đầu `PATH`.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
    try:
        from setup_java import tim_java  # type: ignore[import-not-found]
    except ImportError:
        tim_java = None  # type: ignore[assignment]

    if tim_java is not None and (java := tim_java()):
        return java
    if p := shutil.which("java"):
        return Path(p)
    raise RuntimeError(
        "Không tìm thấy java >= 11. Chạy `py -3 scripts/setup_java.py` trước."
    )


def chay_cli(
    inputs: list[Path],
    out_dir: Path,
    *,
    table_method: str = "cluster",
    include_header_footer: bool = True,
    quiet: bool = True,
) -> None:
    """Gọi `.jar` của OpenDataLoader, ghi `json` + `md` vào `out_dir`.

    Import `opendataloader_pdf` **lười**: `pyproject.toml` chốt rằng `pytest` của
    repo phải xanh trên máy trắng, mà gói này là extra. Import ở đầu module thì
    `import ocr_bench` trên máy chưa cài sẽ nổ và cả registry rụng theo.
    """
    import opendataloader_pdf  # noqa: PLC0415 — cố ý lười, xem docstring

    java = _java()
    moi_truong = os.environ.get("PATH", "")
    os.environ["PATH"] = str(java.parent) + os.pathsep + moi_truong
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        opendataloader_pdf.convert(
            input_path=[str(p) for p in inputs],
            output_dir=str(out_dir),
            format=["json", "markdown"],
            markdown_with_html=True,  # bảng nhiều dòng gộp cần thẻ HTML
            table_method=table_method,
            include_header_footer=include_header_footer,
            image_output="external",
            image_format="png",  # `OcrImage.data` là PNG theo hợp đồng
            quiet=quiet,
        )
    finally:
        os.environ["PATH"] = moi_truong


def kich_thuoc_trang(pdf: Path) -> list[tuple[float, float]]:
    """`[(width, height), ...]` theo MediaBox, đọc bằng `pypdf`.

    JSON của OpenDataLoader không có kích thước trang (xem docstring module), mà
    `Box.from_absolute` bắt buộc phải có. Đây là nguồn thứ hai — đúng kỷ luật của
    A4: không tin engine về thứ nó không tự khai.

    Chỉ lấy **chiều**, không lấy `left`/`bottom`: phép đo 4 cho thấy engine đã trừ
    gốc MediaBox rồi.
    """
    from pypdf import PdfReader  # noqa: PLC0415 — extra, import lười

    return [
        (float(t.mediabox.width), float(t.mediabox.height))
        for t in PdfReader(str(pdf)).pages
    ]


# --------------------------------------------------------------------------
# Quy đổi
# --------------------------------------------------------------------------


def _so_trang(node: dict) -> int | None:
    """`page number` 1-indexed → chỉ số 0-based. Thiếu/hỏng thì trả `None`."""
    v = node.get("page number")
    if not isinstance(v, int) or isinstance(v, bool) or v < 1:
        return None
    return v - 1


def _box(node: dict, trang: int, khung: tuple[float, float]) -> Box | None:
    bb = node.get("bounding box")
    if not isinstance(bb, (list, tuple)) or len(bb) != 4:
        return None
    w, h = khung
    return Box.from_absolute(
        page=trang,
        x0=float(bb[0]),
        y0=float(bb[1]),
        x1=float(bb[2]),
        y1=float(bb[3]),
        page_width=w,
        page_height=h,
        # page_x0/page_y0 để mặc định 0: engine đã trừ gốc MediaBox (phép đo 4).
        y_axis="up",  # ← đo được, không phải giả định. Xem docstring module.
    )


def bang_sang_html(node: dict) -> str:
    """Node `table` → chuỗi `<table>` cho TEDS (B2) ăn.

    `row number`/`column number` của engine là **1-indexed** — ở đây chỉ dùng để
    sắp thứ tự nên không cần quy đổi, nhưng `rowspan`/`colspan` thì phải chép
    đúng, nếu không TEDS chấm sai cấu trúc chứ không chỉ sai chữ.
    """
    dong_html: list[str] = []
    for dong in sorted(
        node.get("rows", []) or [],
        key=lambda d: d.get("row number", 0) if isinstance(d, dict) else 0,
    ):
        if not isinstance(dong, dict):
            continue
        o_html: list[str] = []
        for o in sorted(
            dong.get("cells", []) or [],
            key=lambda c: c.get("column number", 0) if isinstance(c, dict) else 0,
        ):
            if not isinstance(o, dict):
                continue
            the = "th" if o.get("is_header") else "td"
            thuoc_tinh = ""
            if (rs := o.get("row span", 1)) and rs > 1:
                thuoc_tinh += f' rowspan="{int(rs)}"'
            if (cs := o.get("column span", 1)) and cs > 1:
                thuoc_tinh += f' colspan="{int(cs)}"'
            o_html.append(f"<{the}{thuoc_tinh}>{escape(chu_cua_node(o))}</{the}>")
        dong_html.append("<tr>" + "".join(o_html) + "</tr>")
    return "<table>" + "".join(dong_html) + "</table>"


def build_result(
    *,
    engine_version: str,
    doc_id: str,
    capabilities: frozenset[Capability],
    doc: dict,
    markdown: str,
    trang: list[tuple[float, float]],
    anh_bytes: dict[str, bytes],
    config_fingerprint: dict[str, object],
) -> OcrResult:
    """Ghép JSON của OpenDataLoader thành `OcrResult`.

    Tách khỏi `run()` để test được **mà không cần Java, không cần cài engine**:
    hàm này chỉ đụng dict thuần.
    """
    blocks: list[OcrBlock] = []
    tables: list[OcrTable] = []
    images: list[OcrImage] = []
    thieu_trang: set[object] = set()

    for node in node_khoi(doc):
        so = _so_trang(node)
        if so is None or so >= len(trang):
            # Không rơi về trang 0: box chuẩn hoá sai còn tệ hơn box thiếu, vì nó
            # vẫn được chấm và kéo điểm xuống mà không để lại dấu vết.
            thieu_trang.add(node.get("page number"))
            continue

        bt = map_block_type(node.get("type", ""))
        box = _box(node, so, trang[so])
        chu = chu_cua_node(node)

        cap = node.get("heading level") if bt is BlockType.HEADING else None
        blocks.append(
            OcrBlock(
                block_type=bt,
                box=box,
                text=chu or None,
                level=cap if isinstance(cap, int) else None,
            )
        )

        if bt is BlockType.TABLE:
            tables.append(
                OcrTable(
                    html=bang_sang_html(node),
                    box=box,
                    n_rows=node.get("number of rows"),
                    n_cols=node.get("number of columns"),
                )
            )

        if node.get("type") == "image":
            # `source` là đường dẫn tương đối kiểu `<stem>_images/imageFile1.png`.
            # Ép về str tại biên: `source_id` đi thẳng vào JSON của `prediction/`.
            nguon = node.get("source")
            nguon = str(nguon) if nguon is not None else None
            images.append(
                OcrImage(
                    box=box,
                    data=anh_bytes.get(nguon) if nguon else None,
                    source_id=nguon,
                )
            )

    loi = None
    if thieu_trang:
        loi = (
            "node có `page number` ngoài phạm vi "
            + ", ".join(repr(p) for p in sorted(thieu_trang, key=repr))
            + f" (tài liệu {len(trang)} trang) — các node đó bị bỏ"
        )

    return OcrResult(
        engine="opendataloader",
        engine_version=engine_version,
        doc_id=doc_id,
        capabilities=capabilities,
        text_md=markdown,
        blocks=tuple(blocks),
        images=tuple(images),
        tables=tuple(tables),
        page_sizes=tuple(trang),
        error=loi,
        config_fingerprint=config_fingerprint,
    )


class OpenDataLoaderAdapter(Adapter):
    name: ClassVar[str] = "opendataloader"
    capabilities: ClassVar[frozenset[Capability]] = frozenset(
        {
            Capability.TEXT_MD,
            Capability.BLOCK_BBOX,
            Capability.IMAGE_BBOX,
            Capability.IMAGE_BYTES,
            Capability.TABLE_HTML,
        }
    )
    # KHÔNG khai SECTION_HIERARCHY: node `heading` có `heading level` nhưng JSON
    # phẳng, không node nào trỏ về mục cha. Dựng cây bằng cách suy từ thứ tự đọc
    # là đoán, và A5 cấm đoán.

    def __init__(
        self, *, table_method: str = "cluster", include_header_footer: bool = True
    ) -> None:
        self.table_method = table_method
        self.include_header_footer = include_header_footer

    @staticmethod
    def _odl_version() -> str:
        """Phiên bản engine — **không được ném**, cùng lý do với `_java_de_ghi()`.

        `importlib.metadata.version()` ném `PackageNotFoundError` khi extra chưa
        cài. Mà `Adapter.execute()` gọi `config_fingerprint()` *trong nhánh bắt
        lỗi* để dựng bản ghi thất bại — hàm này ném ở đó thì lỗi gốc bị nuốt và
        thay bằng một lỗi thứ hai chẳng liên quan gì.
        """
        from importlib.metadata import PackageNotFoundError, version  # noqa: PLC0415

        try:
            return version("opendataloader-pdf")
        except PackageNotFoundError:
            return "chưa cài"

    def version(self) -> str:
        return self._odl_version()

    def config_fingerprint(self) -> dict[str, object]:
        return {
            "opendataloader_version": self._odl_version(),
            "table_method": self.table_method,
            "include_header_footer": self.include_header_footer,
            "reading_order": "xycut",  # mặc định của engine, ghi lại cho rõ
            "image_output": "external",
            "image_format": "png",
            "markdown_with_html": True,
            "java": self._java_de_ghi(),
        }

    @staticmethod
    def _java_de_ghi() -> str:
        """Đường dẫn java cho dấu vân tay — **không được ném**.

        `Adapter.execute()` bắt lỗi của `run()` rồi gọi `config_fingerprint()` để
        dựng bản ghi thất bại. Nếu hàm này cũng ném thì lỗi gốc bị nuốt, cả lượt
        chạy đổ ngay tài liệu đầu tiên thay vì ghi `failed=True` và đi tiếp.
        """
        try:
            return str(_java())
        except RuntimeError as exc:
            return f"không tìm thấy: {exc}"

    def run(self, doc_path: Path) -> OcrResult:
        import json  # noqa: PLC0415

        with tempfile.TemporaryDirectory(prefix="odl-") as tmp:
            ra = Path(tmp)
            chay_cli(
                [doc_path],
                ra,
                table_method=self.table_method,
                include_header_footer=self.include_header_footer,
            )
            stem = doc_path.stem
            doc = json.loads((ra / f"{stem}.json").read_text(encoding="utf-8"))
            md_path = ra / f"{stem}.md"
            markdown = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
            anh_bytes = {
                str(p.relative_to(ra)).replace("\\", "/"): p.read_bytes()
                for p in ra.rglob("*_images/*")
                if p.is_file()
            }

        return build_result(
            engine_version=self.version(),
            doc_id=stem,
            capabilities=self.capabilities,
            doc=doc,
            markdown=markdown,
            trang=kich_thuoc_trang(doc_path),
            anh_bytes=anh_bytes,
            config_fingerprint=self.config_fingerprint(),
        )
