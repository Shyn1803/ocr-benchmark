"""Hợp đồng dữ liệu của ocr-bench.

Adapter quy đổi output riêng của từng engine về các kiểu ở file này. Metric **chỉ**
nhìn thấy các kiểu ở file này — không metric nào được biết engine gốc dùng hệ toạ độ
gì, đánh số trang từ mấy, hay trả ảnh dạng base64 hay PIL.

Ba quy tắc bất di bất dịch, chốt ở A0 (xem `.claude/context/OCR-BENCH-A0-SPIKE.md` §8):

1. `Box` đã chuẩn hoá về [0,1], gốc **trên-trái**, y hướng **xuống**.
   Ba engine dùng ba hệ khác nhau (Marker trên-trái/y-xuống, pdf-inspector
   dưới-trái/y-lên, OpenDataLoader chưa rõ). Trộn nhầm không gây lỗi — nó chỉ cho
   IoU thấp trông y hệt "engine tách ảnh kém". Quy đổi bắt buộc tại biên adapter.
2. Số trang **0-based** ở mọi nơi. pdf-inspector trả 0-based ở API này và 1-based ở
   API kia trên cùng một file; adapter phải nuốt sự khác biệt đó.
3. Engine thiếu năng lực → metric trả **N/A**, không phải 0. `Capability` là cơ chế
   để biết trước, thay vì đoán từ việc trường dữ liệu rỗng.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import ClassVar, Literal

__all__ = [
    "Capability",
    "YAxis",
    "Box",
    "BlockType",
    "OcrBlock",
    "OcrImage",
    "OcrTable",
    "ScanLabel",
    "OcrResult",
    "AnnotationGT",
    "AssertionGT",
    "GroundTruth",
    "Assertion",
    "TextPresence",
    "TextAbsence",
    "ReadingOrder",
    "NAReason",
    "MetricResult",
]


class Capability(str, enum.Enum):
    """Năng lực mà một adapter **khai báo tĩnh** là nó cung cấp.

    Khai báo, không phải suy ra: một engine có thể chạy đúng trên một file mà không
    tìm thấy ảnh nào. `images == []` lúc đó nghĩa là "không có ảnh", còn thiếu
    `IMAGE_BBOX` nghĩa là "không bao giờ biết được". Hai chuyện khác hẳn nhau, và
    gộp lại là cách nhanh nhất để một engine làm ít việc hơn lại trông giỏi hơn.
    """

    TEXT_MD = "text_md"
    BLOCK_BBOX = "block_bbox"
    IMAGE_BBOX = "image_bbox"
    IMAGE_BYTES = "image_bytes"
    TABLE_HTML = "table_html"
    SECTION_HIERARCHY = "section_hierarchy"
    SCAN_LABEL = "scan_label"


YAxis = Literal["down", "up"]
"""Chiều trục y của không gian toạ độ **gốc** mà engine trả về.

``down`` — gốc trên-trái, y tăng khi đi xuống (Marker, hầu hết thư viện layout).
``up``   — gốc dưới-trái, y tăng khi đi lên (PDF user space, pdf-inspector).
"""

_EPS = 1e-6


@dataclass(frozen=True, slots=True)
class Box:
    """Hộp bao đã chuẩn hoá: [0,1], gốc trên-trái, y hướng xuống, trang 0-based.

    Không dựng trực tiếp từ số thô của engine — dùng :meth:`from_absolute` để việc
    quy đổi đi qua đúng một chỗ có test.
    """

    page: int
    x0: float
    y0: float
    x1: float
    y1: float

    def __post_init__(self) -> None:
        if self.page < 0:
            raise ValueError(f"page phải 0-based và không âm, nhận {self.page}")
        for name in ("x0", "y0", "x1", "y1"):
            v = getattr(self, name)
            if not (-_EPS <= v <= 1 + _EPS):
                raise ValueError(
                    f"{name}={v!r} nằm ngoài [0,1] — toạ độ chưa được chuẩn hoá. "
                    "Dùng Box.from_absolute() thay vì dựng Box trực tiếp."
                )
        if self.x1 < self.x0 or self.y1 < self.y0:
            raise ValueError(
                f"box lộn ngược: ({self.x0},{self.y0})-({self.x1},{self.y1}). "
                "from_absolute() đã sắp xếp giúp; nếu tự dựng thì phải x0<=x1, y0<=y1."
            )

    @classmethod
    def from_absolute(
        cls,
        *,
        page: int,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        page_width: float,
        page_height: float,
        y_axis: YAxis,
        page_x0: float = 0.0,
        page_y0: float = 0.0,
    ) -> Box:
        """Quy đổi toạ độ thô của engine về hệ chuẩn của bench.

        ``page_x0``/``page_y0`` là gốc của **page box** trong không gian engine.
        Mặc định (0,0) đúng cho đường thường của Marker, nhưng nhánh ``force_ocr``
        lấy page box từ ``pdfium.get_bbox()`` và nó **không** đảm bảo bắt đầu từ 0 —
        truyền vào chứ đừng giả định.
        """
        if page_width <= 0 or page_height <= 0:
            raise ValueError(f"page {page_width}x{page_height} không hợp lệ")

        lo_x, hi_x = sorted((x0, x1))
        lo_y, hi_y = sorted((y0, y1))

        nx0 = (lo_x - page_x0) / page_width
        nx1 = (hi_x - page_x0) / page_width

        if y_axis == "down":
            ny0 = (lo_y - page_y0) / page_height
            ny1 = (hi_y - page_y0) / page_height
        elif y_axis == "up":
            # y lớn = gần đỉnh trang → cạnh trên của box là hi_y.
            ny0 = 1.0 - (hi_y - page_y0) / page_height
            ny1 = 1.0 - (lo_y - page_y0) / page_height
        else:  # pragma: no cover - Literal đã chặn ở mức type
            raise ValueError(f"y_axis không hợp lệ: {y_axis!r}")

        clamp = lambda v: min(1.0, max(0.0, v))  # noqa: E731
        return cls(page=page, x0=clamp(nx0), y0=clamp(ny0), x1=clamp(nx1), y1=clamp(ny1))

    @property
    def area(self) -> float:
        return max(0.0, self.x1 - self.x0) * max(0.0, self.y1 - self.y0)

    def iou(self, other: Box) -> float:
        """IoU. Box khác trang luôn cho 0 — không bao giờ so chéo trang."""
        if self.page != other.page:
            return 0.0
        ix = min(self.x1, other.x1) - max(self.x0, other.x0)
        iy = min(self.y1, other.y1) - max(self.y0, other.y0)
        if ix <= 0 or iy <= 0:
            return 0.0
        inter = ix * iy
        union = self.area + other.area - inter
        return inter / union if union > 0 else 0.0


class BlockType(str, enum.Enum):
    """Từ điển chung. Ánh xạ tên riêng của engine về đây nằm trong adapter.

    Marker có cả ``Picture`` lẫn ``Figure``; OpenDataLoader gọi là "images".
    Metric không được biết những tên đó tồn tại.
    """

    TEXT = "text"
    HEADING = "heading"
    TITLE = "title"
    LIST = "list"
    TABLE = "table"
    PICTURE = "picture"
    CAPTION = "caption"
    FOOTNOTE = "footnote"
    PAGE_HEADER = "page_header"
    PAGE_FOOTER = "page_footer"
    FORMULA = "formula"
    CODE = "code"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class OcrBlock:
    block_type: BlockType
    box: Box | None = None
    text: str | None = None
    html: str | None = None
    level: int | None = None
    """Cấp tiêu đề 1..6, chỉ có nghĩa với ``HEADING``/``TITLE``."""
    section_hierarchy: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class OcrImage:
    box: Box | None = None
    data: bytes | None = None
    """Bytes PNG. Chuẩn hoá tại adapter: Marker trả PIL.Image ở MarkdownOutput
    nhưng base64 ở JSONBlockOutput — metric không được nhận hai kiểu."""
    source_id: str | None = None


@dataclass(frozen=True, slots=True)
class OcrTable:
    html: str
    """HTML ``<table>`` — đúng định dạng TEDS ăn vào, không cần chuyển đổi."""
    box: Box | None = None
    n_rows: int | None = None
    n_cols: int | None = None


@dataclass(frozen=True, slots=True)
class ScanLabel:
    """Nhãn scan/digital của engine kiểu router (pdf-inspector)."""

    is_scanned: bool
    api: str
    """Tên hàm engine đã dùng. **Bắt buộc.**

    ``classify_pdf()`` và ``extract_pages_markdown()`` của pdf-inspector cho hai câu
    trả lời trái ngược nhau trên cùng một file (A0 §5.2). "Độ chính xác phân loại
    của pdf-inspector" mà không nói rõ hàm nào là một con số vô nghĩa.
    """
    confidence: float | None = None
    pages_needing_ocr: tuple[int, ...] = ()
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class OcrResult:
    """Kết quả một engine chạy trên một tài liệu.

    Hợp của các kênh tuỳ chọn, không phải giao. Ba engine có năng lực không bằng
    nhau — ép chung một hình dạng bắt buộc thì hoặc mất B3, hoặc mất B5.
    """

    engine: str
    engine_version: str
    doc_id: str
    capabilities: frozenset[Capability]
    text_md: str | None = None
    blocks: tuple[OcrBlock, ...] = ()
    images: tuple[OcrImage, ...] = ()
    tables: tuple[OcrTable, ...] = ()
    scan_label: ScanLabel | None = None
    page_sizes: tuple[tuple[float, float], ...] = ()
    seconds: float | None = None
    peak_rss_mb: float | None = None
    failed: bool = False
    error: str | None = None
    config_fingerprint: dict[str, object] = field(default_factory=dict)
    """Config mà engine đã chạy. A7 bắt buộc ghi lại — người đọc phải biết baseline
    Sovereign được đo ở chế độ nào (``ocr_use_vision_api`` bật hay tắt)."""

    def __post_init__(self) -> None:
        if self.failed and not self.error:
            raise ValueError("failed=True thì phải có error")
        if not self.failed:
            self._require(Capability.TEXT_MD, self.text_md is not None, "text_md")
            self._require(
                Capability.BLOCK_BBOX,
                any(b.box is not None for b in self.blocks),
                "blocks[].box",
            )
            self._require(
                Capability.IMAGE_BBOX,
                any(i.box is not None for i in self.images),
                "images[].box",
            )
            self._require(
                Capability.IMAGE_BYTES,
                any(i.data is not None for i in self.images),
                "images[].data",
            )
            self._require(Capability.TABLE_HTML, bool(self.tables), "tables")
            self._require(
                Capability.SCAN_LABEL, self.scan_label is not None, "scan_label"
            )

    def _require(self, cap: Capability, populated: bool, where: str) -> None:
        if populated and cap not in self.capabilities:
            raise ValueError(
                f"{self.engine} trả {where} nhưng không khai báo {cap.value}. "
                "capabilities phải khai tĩnh ở adapter, không suy ra từ dữ liệu."
            )


# --------------------------------------------------------------------------
# Ground truth — GIỮ CẢ HAI DẠNG
#
# Kế hoạch đặt AnnotationGT *hay* AssertionGT. Chọn một là vứt một nhóm metric:
# chỉ AnnotationGT → mất B5 (olmOCR-bench là các khẳng định, không có annotation
# toàn văn); chỉ AssertionGT → mất B3 (IoU cần bbox thật của DocLayNet).
# Mỗi metric tự khai nó ăn dạng nào.
# --------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AnnotationGT:
    """Kiểu DocLayNet: đáp án đầy đủ cho cả trang."""

    doc_id: str
    text: str | None = None
    blocks: tuple[OcrBlock, ...] = ()
    images: tuple[Box, ...] = ()
    tables: tuple[OcrTable, ...] = ()
    page_sizes: tuple[tuple[float, float], ...] = ()
    human_ceiling: dict[str, float] = field(default_factory=dict)
    """Trần người, lấy từ phần DocLayNet được annotate 2-3 lần.

    Không có trần này, engine đạt 0.87 trong khi hai người annotate chỉ đồng ý với
    nhau 0.85 sẽ bị chấm "chưa đạt" dù nó đã chạm giới hạn của chính bài toán.
    """


@dataclass(frozen=True, slots=True)
class Assertion:
    """Một khẳng định đúng/sai về tài liệu.

    `kind` là ClassVar chứ không phải field: nó thuộc về *loại* khẳng định, không
    phải dữ liệu của từng thể hiện, và để nó thành field sẽ chặn subclass thêm
    trường bắt buộc.
    """

    kind: ClassVar[str] = "assertion"


@dataclass(frozen=True, slots=True)
class TextPresence(Assertion):
    needle: str
    kind: ClassVar[str] = "text_presence"


@dataclass(frozen=True, slots=True)
class TextAbsence(Assertion):
    needle: str
    kind: ClassVar[str] = "text_absence"


@dataclass(frozen=True, slots=True)
class ReadingOrder(Assertion):
    before: str
    after: str
    kind: ClassVar[str] = "reading_order"


@dataclass(frozen=True, slots=True)
class AssertionGT:
    """Kiểu olmOCR-bench: vài khẳng định đúng/sai thay cho annotate toàn văn.

    ~10 phút/tài liệu thay vì 45-60 phút. Đây là lý do bỏ được kế hoạch tự
    annotate 20 file.
    """

    doc_id: str
    tests: tuple[Assertion, ...] = ()


GroundTruth = AnnotationGT | AssertionGT


class NAReason(str, enum.Enum):
    MISSING_CAPABILITY = "missing_capability"
    ENGINE_FAILED = "engine_failed"
    NO_GROUND_TRUTH = "no_ground_truth"
    WRONG_GT_KIND = "wrong_gt_kind"


@dataclass(frozen=True, slots=True)
class MetricResult:
    """Điểm của một metric trên một (engine, tài liệu).

    ``value is None`` nghĩa là **N/A** — không đo được. Không bao giờ thay bằng 0.0.
    """

    metric: str
    engine: str
    doc_id: str
    value: float | None
    na_reason: NAReason | None = None
    detail: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.value is None and self.na_reason is None:
            raise ValueError(f"{self.metric}/{self.doc_id}: N/A thì phải nêu na_reason")
        if self.value is not None and self.na_reason is not None:
            raise ValueError(
                f"{self.metric}/{self.doc_id}: có điểm rồi thì không được kèm na_reason"
            )

    @property
    def is_na(self) -> bool:
        return self.value is None
