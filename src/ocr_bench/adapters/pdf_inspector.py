"""Bộ nối pdf-inspector — A6 (TASK-077).

Kế hoạch gốc xếp thư viện này là *classifier thuần*, "không trích text". A0 bác bỏ,
và đo lại ở A6 cho thấy nó còn rối hơn thế. Sáu điều dưới đây **đều là kết quả đo**
trên 204 tài liệu DocLayNet + PDF tự dựng, không phải suy từ tài liệu engine:

1. **Nó trích được Markdown.** `extract_pages_markdown()` cho ra `#`/`##` có phân
   cấp. Nên adapter khai **cả** ``TEXT_MD`` lẫn ``SCAN_LABEL``, không phải mỗi nhãn.

2. **Hai API trả lời trái ngược nhau, cả hai chiều.** Trên 204 tài liệu:

   ===================  ==================  =====
   ``classify_pdf``     ``extract_pages``   Số
   ===================  ==================  =====
   không cần OCR        không cần OCR        171
   cần OCR              cần OCR               11
   **không cần OCR**    **cần OCR**           18
   **cần OCR**          **không cần OCR**      4
   ===================  ==================  =====

   **22/204 = 10.8% bất đồng**, và 18 ca trong đó `classify_pdf` khai
   ``confidence=1.00``. Không API nào trội hơn. Nên ``ScanLabel.api`` là **bắt
   buộc** ghi rõ nhãn đến từ hàm nào — một con số "pdf-inspector nói cần OCR"
   không kèm tên hàm là con số vô nghĩa.

3. **Ba quy ước số trang trong một thư viện, hai trong đó cùng một object:**

   ========================================  =========
   Trường                                    Gốc
   ========================================  =========
   ``PageMarkdown.page``                     0-based
   ``PagesExtractionResult.pages_needing_ocr``  **1**-based
   ``classify_pdf().pages_needing_ocr``      0-based
   ``TextItem.page``                         **1**-based
   ========================================  =========

   Hai dòng đầu là hai thuộc tính của **cùng một** ``PagesExtractionResult``. Đo
   trên tài liệu 1 trang: ``pages[0].page == 0`` trong khi
   ``pages_needing_ocr == [1]``. Bench 0-based khắp nơi, nên quy đổi ở biên và
   quy đổi **riêng từng trường**.

4. **Engine KHÔNG trừ gốc MediaBox** — ngược hẳn OpenDataLoader. Dựng lại trang
   với MediaBox dịch (100, 200) thì toạ độ dịch theo đúng (+100, +200). Nên
   ``page_x0``/``page_y0`` phải **truyền vào** từ MediaBox. Chép quy tắc từ
   `adapters/opendataloader.py` sang (nơi phải để 0) là sai câm: box vẫn ra số
   trong [0,1] vì ``from_absolute`` có clamp, IoU vẫn xếp hạng được.

5. **Gốc dưới-trái, y hướng LÊN, đơn vị điểm PDF.** Chữ đặt ở y=780 trên trang
   cao 842 trả về đúng ``y=780.0``; item đầu thứ tự đọc có y **lớn nhất**.

6. **``TextItem.width`` bằng 0.0 ở 38% item — và dồn cục theo tài liệu.** Không
   rải đều: một tài liệu 93% (n=396), một tài liệu 1%, 22 tài liệu còn lại 0%.
   Chữ vẫn thật, ``height`` và ``font_size`` vẫn đúng — engine chỉ không cho biết
   bề rộng. Mà ``Box.from_absolute`` **chấp nhận ``x1 == x0``** không một tiếng
   động, nên bê thẳng ``x + width`` sẽ nạp vào bench 396 hộp diện tích 0 → IoU 0
   tuyệt đối → bảng đọc thành "engine định vị kém", sai sự thật.

   Xử lý: **giữ chữ, để ``box=None``** (``OcrBlock.box`` vốn ``| None``). Không
   suy bề rộng từ ``font_size × len(text)`` — đó là đoán, và số đoán ra sẽ đi
   thẳng vào IoU như thể là số đo. Số item bị bỏ hộp ghi vào ``OcrResult.error``
   để nó đếm được và nhìn thấy được, không im lặng.

Hai chuyện khác, ghi lại để không ai mất công dò lại:

* ``TextItem.item_type`` **mang cả dữ liệu**, không phải enum sạch: ngoài
  ``text``/``image`` còn có ``link:<URL đầy đủ>``. Muốn so kiểu thì phải cắt
  trước dấu hai chấm.
* ``process_pdf().markdown`` có thể là ``None`` trên chính tài liệu mà
  ``extract_pages_markdown()`` trích ra sạch (A0 §5.2). Nên adapter này **không**
  gọi ``process_pdf`` — text lấy từ ``extract_pages_markdown``, là API duy nhất
  vừa cho text vừa cho cờ OCR theo từng trang.

Chạy bằng venv riêng ``.venv-pi`` (engine là extra, `pypdf` cho kích thước trang)::

    .venv-pi/Scripts/python.exe scripts/make_predictions.py --engines pdf_inspector
"""

from __future__ import annotations

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
    ScanLabel,
)

__all__ = [
    "PdfInspectorAdapter",
    "SCAN_LABEL_APIS",
    "kich_thuoc_trang",
    "nhan_tu_classify",
    "nhan_tu_pages",
    "text_md_tu_pages",
    "blocks_tu_items",
    "build_result",
]

#: Hai API sinh nhãn. Tên ở đây đi thẳng vào ``ScanLabel.api`` — đó là điểm của AC-02.
SCAN_LABEL_APIS = ("classify_pdf", "extract_pages_markdown")

#: ``pdf_type`` engine trả về mà bench coi là "cần OCR".
LOAI_CAN_OCR = frozenset({"scanned", "image_based"})


def kich_thuoc_trang(pdf: Path) -> list[tuple[float, float, float, float]]:
    """``[(width, height, left, bottom), ...]`` theo MediaBox, đọc bằng ``pypdf``.

    pdf-inspector không khai kích thước trang ở bất kỳ API nào, mà
    ``Box.from_absolute`` bắt buộc phải có. Lấy cả ``left``/``bottom`` chứ không
    chỉ chiều: đo được rằng engine **không** trừ gốc MediaBox (mục 4 docstring
    module), nên hai số đó phải đi vào ``page_x0``/``page_y0``.
    """
    from pypdf import PdfReader  # noqa: PLC0415 — extra, import lười

    return [
        (
            float(t.mediabox.width),
            float(t.mediabox.height),
            float(t.mediabox.left),
            float(t.mediabox.bottom),
        )
        for t in PdfReader(str(pdf)).pages
    ]


# --------------------------------------------------------------------------
# Nhãn — hai nguồn, hai kết quả
# --------------------------------------------------------------------------


def nhan_tu_classify(c: Any) -> ScanLabel:
    """``classify_pdf()`` → ``ScanLabel``.

    ``pages_needing_ocr`` của API này **đã là 0-based** — không trừ. Object trả
    về không có trường lý do nào (chỉ ``pdf_type``, ``confidence``, ``page_count``,
    ``pages_needing_ocr``), nên ``reason`` lấy chính ``pdf_type``.
    """
    loai = getattr(c, "pdf_type", None)
    trang = tuple(
        int(p) for p in (getattr(c, "pages_needing_ocr", None) or []) if isinstance(p, int)
    )
    conf = getattr(c, "confidence", None)
    return ScanLabel(
        is_scanned=loai in LOAI_CAN_OCR or bool(trang),
        api="classify_pdf",
        confidence=float(conf) if isinstance(conf, (int, float)) else None,
        pages_needing_ocr=trang,
        reason=f"pdf_type={loai}" if loai else None,
    )


def nhan_tu_pages(r: Any) -> ScanLabel:
    """``extract_pages_markdown()`` → ``ScanLabel``.

    Số trang lấy từ ``PageMarkdown.page`` (**0-based**), *không* từ
    ``PagesExtractionResult.pages_needing_ocr`` (**1-based**) — hai thuộc tính của
    cùng một object, hai quy ước khác nhau. Dùng nhầm cái sau là lệch đúng một
    trang, không exception, không triệu chứng.

    Lý do cũng vậy: ``ocr_reasons_by_page`` của object cha đo được là **rỗng** kể
    cả khi có trang cần OCR — lý do thật nằm ở ``PageMarkdown.ocr_reason``.
    """
    trang: list[int] = []
    ly_do: list[str] = []
    for p in getattr(r, "pages", None) or []:
        so = getattr(p, "page", None)
        if getattr(p, "needs_ocr", False) and isinstance(so, int) and not isinstance(so, bool):
            trang.append(so)
            if ly_do_trang := getattr(p, "ocr_reason", None):
                ly_do.append(f"trang {so}: {ly_do_trang}")
    return ScanLabel(
        is_scanned=bool(trang),
        api="extract_pages_markdown",
        confidence=None,  # API này không khai độ tin cậy — để None, không bịa 1.0
        pages_needing_ocr=tuple(sorted(trang)),
        reason="; ".join(ly_do) if ly_do else None,
    )


def text_md_tu_pages(r: Any) -> str:
    """Nối Markdown từng trang theo thứ tự ``PageMarkdown.page`` (0-based)."""
    trang = [
        (getattr(p, "page", 0), getattr(p, "markdown", "") or "")
        for p in getattr(r, "pages", None) or []
    ]
    return "\n\n".join(md for _, md in sorted(trang, key=lambda t: t[0]) if md)


# --------------------------------------------------------------------------
# Block + toạ độ
# --------------------------------------------------------------------------


def _so_trang(item: Any) -> int | None:
    """``TextItem.page`` 1-indexed → 0-based. Thiếu/hỏng trả ``None``.

    ``isinstance(True, int)`` là ``True`` trong Python — nên chặn ``bool`` riêng.
    """
    v = getattr(item, "page", None)
    if not isinstance(v, int) or isinstance(v, bool) or v < 1:
        return None
    return v - 1


def _loai_block(item_type: Any) -> BlockType:
    """``item_type`` → ``BlockType``.

    Trường này **mang cả dữ liệu**: ``link:https://…`` là một giá trị thật quan
    sát được. Cắt trước dấu hai chấm rồi mới so; loại lạ vào ``OTHER`` chứ không
    bị bỏ (bỏ block là mất recall).
    """
    t = str(item_type or "").split(":", 1)[0].strip().lower()
    if t == "image":
        return BlockType.PICTURE
    if t == "text":
        return BlockType.TEXT
    return BlockType.OTHER


def blocks_tu_items(
    items: list[Any], trang: list[tuple[float, float, float, float]]
) -> tuple[list[OcrBlock], int, set[object]]:
    """``TextItem[]`` → ``OcrBlock[]``, kèm số item mất hộp và số trang hỏng.

    Trả về ``(blocks, so_item_mat_hop, trang_hong)``. Hai số sau đi vào
    ``OcrResult.error`` — mất hộp im lặng là đúng thứ task này sinh ra để chặn.
    """
    blocks: list[OcrBlock] = []
    mat_hop = 0
    trang_hong: set[object] = set()

    for it in items:
        so = _so_trang(it)
        if so is None or so >= len(trang):
            # Không rơi về trang 0: box chuẩn hoá sai còn tệ hơn box thiếu, vì nó
            # vẫn được chấm và kéo điểm xuống mà không để lại dấu vết.
            trang_hong.add(getattr(it, "page", None))
            continue

        w, h, x0_trang, y0_trang = trang[so]
        x = getattr(it, "x", None)
        y = getattr(it, "y", None)
        rong = getattr(it, "width", None)
        cao = getattr(it, "height", None)

        box: Box | None = None
        if all(isinstance(v, (int, float)) for v in (x, y, rong, cao)) and rong and cao:
            box = Box.from_absolute(
                page=so,
                x0=float(x),
                y0=float(y),
                x1=float(x) + float(rong),
                y1=float(y) + float(cao),
                page_width=w,
                page_height=h,
                page_x0=x0_trang,  # engine KHÔNG trừ gốc MediaBox — mục 4 docstring
                page_y0=y0_trang,
                y_axis="up",  # ← đo được, không phải giả định
            )
        else:
            # `width == 0.0` trên 38% item, dồn cục 93% ở một tài liệu. Giữ chữ,
            # bỏ hộp: engine thật sự không cho biết vùng, và hộp diện tích 0 sẽ
            # được chấm như một dự đoán sai thay vì như một chỗ thiếu dữ liệu.
            mat_hop += 1

        chu = (getattr(it, "text", None) or "").strip()
        blocks.append(
            OcrBlock(
                block_type=_loai_block(getattr(it, "item_type", None)),
                box=box,
                text=chu or None,
            )
        )

    return blocks, mat_hop, trang_hong


def build_result(
    *,
    engine_version: str,
    doc_id: str,
    capabilities: frozenset[Capability],
    classification: Any,
    pages_result: Any,
    items: list[Any],
    trang: list[tuple[float, float, float, float]],
    scan_label_api: str,
    config_fingerprint: dict[str, object],
) -> OcrResult:
    """Ghép ba API của pdf-inspector thành một ``OcrResult``.

    Tách khỏi ``run()`` để test được **mà không cần cài engine**: hàm này chỉ đụng
    object có thuộc tính, nên dữ liệu giả bằng ``SimpleNamespace`` là đủ.

    Nhãn nào vào ``OcrResult.scan_label`` do ``scan_label_api`` quyết, và khi hai
    API bất đồng thì ghi vào ``error`` — 10.8% bộ mẫu rơi vào ca này, im lặng là
    giấu mất chính cái task này sinh ra để đo.
    """
    nhan = {
        "classify_pdf": nhan_tu_classify(classification),
        "extract_pages_markdown": nhan_tu_pages(pages_result),
    }
    if scan_label_api not in nhan:
        raise ValueError(
            f"scan_label_api không hợp lệ: {scan_label_api!r}; chọn một trong {SCAN_LABEL_APIS}"
        )

    blocks, mat_hop, trang_hong = blocks_tu_items(items, trang)

    ghi_chu: list[str] = []
    a, b = nhan["classify_pdf"], nhan["extract_pages_markdown"]
    if a.is_scanned != b.is_scanned:
        ghi_chu.append(
            f"hai API bất đồng: classify_pdf.is_scanned={a.is_scanned} "
            f"(conf={a.confidence}) vs extract_pages_markdown.is_scanned={b.is_scanned}"
        )
    if mat_hop:
        ghi_chu.append(
            f"{mat_hop}/{len(items)} item không có bề rộng (width=0) — giữ chữ, bỏ hộp"
        )
    if trang_hong:
        ghi_chu.append(
            "item có `page` ngoài phạm vi "
            + ", ".join(repr(p) for p in sorted(trang_hong, key=repr))
            + f" (tài liệu {len(trang)} trang) — các item đó bị bỏ"
        )

    # Vùng ảnh phải nằm ở CẢ `blocks` lẫn `images`, đúng như phía nhãn làm
    # (`corpus.py`: `if loai is BlockType.PICTURE: images.append(box)`). `img_f1` chỉ
    # đọc `result.images`, nên chỉ đổ vào `blocks` là tìm ra ảnh rồi vứt đi.
    #
    # Dẫn xuất thẳng từ `blocks` để bất biến "mỗi hộp PICTURE là một ảnh" đúng theo
    # cấu trúc chứ không nhờ hai vòng lặp song song giữ đồng bộ.
    #
    # Bỏ qua block mất hộp (`box is None` — 38% item, xem `blocks_tu_items`): một
    # `OcrImage` không toạ độ không đo được, thêm vào chỉ làm phồng số đếm. Ảnh đó
    # thành miss của recall, đúng bản chất — engine không cho biết vùng.
    images = tuple(
        OcrImage(box=b.box)
        for b in blocks
        if b.block_type is BlockType.PICTURE and b.box is not None
    )

    return OcrResult(
        engine="pdf_inspector",
        engine_version=engine_version,
        doc_id=doc_id,
        capabilities=capabilities,
        text_md=text_md_tu_pages(pages_result),
        blocks=tuple(blocks),
        images=images,
        scan_label=nhan[scan_label_api],
        page_sizes=tuple((w, h) for w, h, _, _ in trang),
        error="; ".join(ghi_chu) or None,
        config_fingerprint=config_fingerprint,
    )


class PdfInspectorAdapter(Adapter):
    name: ClassVar[str] = "pdf_inspector"
    capabilities: ClassVar[frozenset[Capability]] = frozenset(
        {
            Capability.TEXT_MD,  # ← A0 bác bỏ giả định "không trích text" của kế hoạch
            Capability.BLOCK_BBOX,
            Capability.SCAN_LABEL,
            Capability.IMAGE_BBOX,
        }
    )
    # KHÔNG khai IMAGE_BYTES / TABLE_HTML / SECTION_HIERARCHY: engine trả *vùng* ảnh
    # (item_type ảnh → BlockType.PICTURE, 2384 hộp trên 1608 tài liệu) nhưng không trả
    # ảnh cắt, không dựng cấu trúc bảng, và heading chỉ là mức `#` trong Markdown chứ
    # không có cây mục. Khai thừa thì metric chấm 0.0 cho thứ engine không hứa.

    def __init__(self, *, scan_label_api: str = "classify_pdf") -> None:
        if scan_label_api not in SCAN_LABEL_APIS:
            raise ValueError(
                f"scan_label_api không hợp lệ: {scan_label_api!r}; chọn một trong {SCAN_LABEL_APIS}"
            )
        self.scan_label_api = scan_label_api

    @staticmethod
    def _pi_version() -> str:
        """Phiên bản engine — **không được ném**.

        ``Adapter.execute()`` gọi ``version()`` *và* ``config_fingerprint()` trong
        nhánh bắt lỗi để dựng bản ghi thất bại. Ném ở đó thì lỗi gốc bị nuốt và cả
        lượt chạy đổ ngay tài liệu đầu tiên. Đây là lỗi #3 của A5, chép nguyên
        bài học sang.
        """
        from importlib.metadata import PackageNotFoundError, version  # noqa: PLC0415

        try:
            return version("pdf-inspector")
        except PackageNotFoundError:
            return "chưa cài"

    def version(self) -> str:
        return self._pi_version()

    def config_fingerprint(self) -> dict[str, object]:
        return {
            "pdf_inspector_version": self._pi_version(),
            # Nhãn đến từ API nào là *cấu hình* của lượt chạy, và hai API bất đồng
            # 10.8% — bảng điểm không nói rõ cái này thì không đọc được.
            "scan_label_api": self.scan_label_api,
            "page_size_source": "pypdf MediaBox",
            "subtract_mediabox_origin": True,
            "zero_width_policy": "box=None, giữ text",
        }

    def run(self, doc_path: Path) -> OcrResult:
        import pdf_inspector as pi  # noqa: PLC0415 — cố ý lười, xem docstring module

        duong = str(doc_path)
        return build_result(
            engine_version=self.version(),
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            classification=pi.classify_pdf(duong),
            pages_result=pi.extract_pages_markdown(duong),
            items=list(pi.extract_text_with_positions(duong)),
            trang=kich_thuoc_trang(doc_path),
            scan_label_api=self.scan_label_api,
            config_fingerprint=self.config_fingerprint(),
        )
