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
import hashlib
from dataclasses import dataclass, field
from typing import ClassVar, Literal, get_args

__all__ = [
    "Capability",
    "FailureKind",
    "RawArtifact",
    "RssScope",
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


RssScope = Literal["process", "process+children"]
"""Số RSS đếm tới đâu — xem `OcrResult.rss_scope`.

Là `Literal` chứ không phải `Enum` để đi thẳng vào JSON prediction mà không cần bộ
quy đổi riêng; giá trị bị kiểm trong `OcrResult.__post_init__`.
"""


class Capability(str, enum.Enum):
    """Năng lực mà một adapter **khai báo tĩnh** là nó cung cấp.

    Khai báo, không phải suy ra: một engine có thể chạy đúng trên một file mà không
    tìm thấy ảnh nào. `images == []` lúc đó nghĩa là "không có ảnh", còn thiếu
    `IMAGE_BBOX` nghĩa là "không bao giờ biết được". Hai chuyện khác hẳn nhau, và
    gộp lại là cách nhanh nhất để một engine làm ít việc hơn lại trông giỏi hơn.

    ``HEADING_LEVEL`` và ``SECTION_HIERARCHY`` là **hai** năng lực chứ không một, vì
    ``OcrBlock`` có hai trường riêng cho chúng:

    * ``HEADING_LEVEL`` → ``OcrBlock.level``: mỗi tiêu đề tự khai mình ở cấp mấy.
    * ``SECTION_HIERARCHY`` → ``OcrBlock.section_hierarchy``: đường dẫn tổ tiên, tức
      một cái **cây**.

    Có cấp không suy ra được cây: opendataloader khai cấp 1..7 nhưng JSON của nó
    phẳng, không node nào trỏ về mục cha (xem `OpenDataLoaderAdapter`). Gộp hai thứ
    này lại thì `heading` (B4, đo cấp) sẽ loại nhầm engine khai đúng cấp, hoặc metric
    nào đó cần cây sẽ nhận nhầm engine chỉ có cấp.
    """

    TEXT_MD = "text_md"
    BLOCK_BBOX = "block_bbox"
    IMAGE_BBOX = "image_bbox"
    IMAGE_BYTES = "image_bytes"
    TABLE_HTML = "table_html"
    HEADING_LEVEL = "heading_level"
    SECTION_HIERARCHY = "section_hierarchy"
    SCAN_LABEL = "scan_label"


class FailureKind(str, enum.Enum):
    """Nhóm lỗi ổn định để báo cáo fail-rate theo nguyên nhân, không theo message."""

    UNSUPPORTED = "unsupported"
    ENVIRONMENT_ERROR = "environment_error"
    TIMEOUT = "timeout"
    OOM = "oom"
    ENGINE_ERROR = "engine_error"
    ADAPTER_ERROR = "adapter_error"


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
class RawArtifact:
    """Output nguyên bản của engine, lưu sidecar để audit cách normalize."""

    name: str
    media_type: str
    data: bytes

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()


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
    engine_family: str | None = None
    profile: str = "legacy"
    text_md: str | None = None
    raw_artifacts: tuple[RawArtifact, ...] = ()
    blocks: tuple[OcrBlock, ...] = ()
    images: tuple[OcrImage, ...] = ()
    tables: tuple[OcrTable, ...] = ()
    scan_label: ScanLabel | None = None
    page_sizes: tuple[tuple[float, float], ...] = ()
    seconds: float | None = None
    """**Tổng** thời gian `run()`, kể cả thời gian nạp model."""
    model_load_seconds: float | None = None
    """Phần thời gian nạp model, tách khỏi `seconds` chứ không trừ sẵn (B6/AC-03).

    Trừ sẵn rồi vứt thì mất câu trả lời cho "chạy 100 tài liệu thì chi phí nạp phân
    bổ ra sao". Adapter không biết thì để `None` — cột hiện `—`. **Không** để 0.0:
    số 0 ở đây là câu "nạp model mất 0 giây", một lời nói dối chứ không phải thiếu số.
    """
    peak_rss_mb: float | None = None
    """Đỉnh RSS **trong cửa sổ chạy**, đã trừ mốc trước khi chạy.

    Không phải `max(RSS)` trần trụi: RSS là mốc nước cao của cả tiến trình và không
    bao giờ giảm, nên engine chạy sau sẽ thừa hưởng vùng nhớ của engine chạy trước và
    trông ngốn hơn **theo đúng thứ tự chạy**.
    """
    peak_vram_mb: float | None = None
    """Đỉnh VRAM trong cửa sổ chạy, `None` = **không đo được**, không phải 0 MB.

    Không có `vram_scope` đi kèm như RSS: VRAM được cấp theo tiến trình bởi driver
    và không có mốc nước cao thừa hưởng từ tiến trình chạy trước, nên câu hỏi "đếm
    tới đâu" không đặt ra. Nhưng câu hỏi "engine này có dùng GPU không" thì có —
    engine chạy CPU để `None`, và cột phải hiện `—` chứ không hiện 0.

    Số 0.0 chỉ hợp lệ khi thật sự đo được và thật sự bằng 0 (đã bật đo trên máy có
    GPU mà engine không cấp phát gì). Adapter không có handshake chứng minh thiết
    bị thì để `None`.
    """
    rss_scope: RssScope | None = None
    """`peak_rss_mb` đếm tới đâu. Bắt buộc có nếu `peak_rss_mb` có (xem `__post_init__`).

    `opendataloader` chạy một `.jar` bằng tiến trình `java` con, `sovereign` cũng có
    nhánh `subprocess`. RSS đo ở tiến trình Python **không nhìn thấy JVM heap**, nên
    một cột RSS không kèm phạm vi sẽ làm engine nuôi cả một JVM trông nhẹ nhất bảng.
    """
    failed: bool = False
    error: str | None = None
    failure_kind: FailureKind | None = None
    config_fingerprint: dict[str, object] = field(default_factory=dict)
    """Config mà engine đã chạy. A7 bắt buộc ghi lại — người đọc phải biết baseline
    Sovereign được đo ở chế độ nào (``ocr_use_vision_api`` bật hay tắt)."""

    def __post_init__(self) -> None:
        if self.engine_family is None:
            object.__setattr__(self, "engine_family", self.engine)
        if not isinstance(self.engine_family, str) or not self.engine_family:
            raise ValueError("engine_family phải là chuỗi không rỗng")
        if not isinstance(self.profile, str) or not self.profile:
            raise ValueError("profile phải là chuỗi không rỗng")
        if self.failed and not self.error:
            raise ValueError("failed=True thì phải có error")
        if self.failed and self.failure_kind is None:
            raise ValueError("failed=True thì phải có failure_kind")
        if self.failure_kind is not None and not isinstance(
            self.failure_kind, FailureKind
        ):
            raise ValueError("failure_kind phải là một giá trị FailureKind")
        if not self.failed and self.failure_kind is not None:
            raise ValueError("failed=False thì không được có failure_kind")
        # Ba kiểm tra dưới đây KHÔNG nằm trong nhánh `not failed`: một lượt chạy hỏng
        # vẫn có số giờ và số nhớ, và số đó vẫn phải tự mô tả được.
        if self.peak_rss_mb is not None and self.rss_scope is None:
            raise ValueError(
                f"{self.engine} trả peak_rss_mb={self.peak_rss_mb} nhưng không khai "
                "rss_scope. Một con số RSS không kèm phạm vi thì không so được giữa "
                "engine chạy trong tiến trình và engine gọi tiến trình con."
            )
        if self.peak_vram_mb is not None and self.peak_vram_mb < 0:
            raise ValueError(
                f"{self.engine} trả peak_vram_mb={self.peak_vram_mb}. VRAM âm là "
                "lỗi đo, không phải một con số nhỏ — để `None` nếu không đo được."
            )
        if self.rss_scope is not None and self.rss_scope not in get_args(RssScope):
            raise ValueError(
                f"rss_scope={self.rss_scope!r} không hợp lệ; "
                f"phải là một trong {list(get_args(RssScope))}"
            )
        if (
            self.model_load_seconds is not None
            and self.seconds is not None
            and self.model_load_seconds > self.seconds
        ):
            raise ValueError(
                f"{self.engine}: model_load_seconds={self.model_load_seconds} lớn hơn "
                f"seconds={self.seconds}. `seconds` là TỔNG thời gian run(), thời gian "
                "nạp là một phần của nó — không phải một khoản cộng thêm."
            )
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
    reading_order: tuple[int, ...] = ()
    """Thứ tự đọc **thật**, dưới dạng chỉ số vào ``blocks``. Rỗng = không có nhãn.

    ⚠️ Rỗng với DocLayNet, và đó không phải thiếu sót của loader. Thứ tự
    ``annotation.id`` của COCO là thứ tự người annotate **vẽ box** (gom theo loại),
    không phải thứ tự đọc: đo trên tài liệu **một cột** — nơi thứ tự đọc bắt buộc
    trùng thứ tự y — vẫn thấy 10% cặp nghịch thế và chỉ 5/11 tài liệu khớp.

    Đừng điền trường này bằng cách sắp hình học. Làm vậy là chấm engine theo
    heuristic của bench chứ không theo sự thật: engine sắp giống heuristic được
    điểm cao kể cả khi heuristic sai. Rỗng ⇒ metric `nid` trả N/A, và N/A là câu
    trả lời đúng cho tới khi có nhãn thật. Xem TASK-082 plan §0.
    """
    human_ceiling: dict[str, float] = field(default_factory=dict)
    """Trần người: mức đồng thuận giữa hai người cùng annotate một trang.

    Không có trần này, engine đạt 0.87 trong khi hai người annotate chỉ đồng ý với
    nhau 0.85 sẽ bị chấm "chưa đạt" dù nó đã chạm giới hạn của chính bài toán.

    ⚠️ Kế hoạch giả định lấy trần này **miễn phí** từ phần DocLayNet được annotate
    2-3 lần. Giả định đó **sai**: trong bản COCO công bố, `precedence` bằng 0 ở cả
    80.863 ảnh của train/val/test và không `file_name` nào lặp — các lần annotate
    trùng đã bị gộp trước khi phát hành. Còn hai đường: điền tay từ số đồng thuận
    trong **bài báo** DocLayNet (theo lớp, không theo trang), hoặc tự annotate lại
    một mẫu nhỏ. Để rỗng thì metric vẫn chạy, chỉ là không có trần để đối chiếu.
    Xem TASK-074 review.md.
    """


@dataclass(frozen=True, slots=True, kw_only=True)
class Assertion:
    """Một khẳng định đúng/sai về tài liệu.

    `kind` là ClassVar chứ không phải field: nó thuộc về *loại* khẳng định, không
    phải dữ liệu của từng thể hiện, và để nó thành field sẽ chặn subclass thêm
    trường bắt buộc.

    `kw_only=True` để lớp cha mang được field **có mặc định** mà lớp con vẫn khai
    được field bắt buộc — không có nó thì dataclass báo "non-default argument
    follows default argument" và ba trường chung dưới đây phải chép lại ở từng lớp con.

    Ba trường chung ấy không phải trang trí. `max_diffs` là **ngưỡng của chính bộ
    nhãn**: olmOCR-bench cho phép lệch tới ngần ấy ký tự khi so khớp mờ. Nạp nhãn mà
    bỏ nó đi thì B5 sẽ chấm khắt khe hơn tác giả bộ nhãn định, và điểm thu được không
    so sánh được với bảng đã công bố của họ — sai theo kiểu vẫn ra một con số đẹp.
    """

    kind: ClassVar[str] = "assertion"

    assertion_id: str | None = None
    page: int = 0
    """0-based, theo quy tắc 2 của bench. Nguồn olmOCR-bench đánh **1-based** — quy
    đổi nằm ở `corpus.load_olmocr()`."""
    max_diffs: int = 0
    checked: str | None = None
    """Xuất xứ nhãn ở nguồn (`"verified"` = người kiểm lại). 2.801/3.385 khẳng định
    `math` để trống — giữ lại để B5 lọc được "chỉ chấm phần đã kiểm" nếu cần."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TextPresence(Assertion):
    needle: str
    case_sensitive: bool = False
    first_n: int | None = None
    last_n: int | None = None
    """Giới hạn vùng tìm về N ký tự đầu/cuối của đầu ra. Chủ yếu dùng cho tầng
    `headers_footers`: "chuỗi này **không** được nằm trong 200 ký tự đầu" là một
    khẳng định khác hẳn "không được nằm ở đâu cả" — 104/823 khẳng định `absent`
    có ràng buộc này, bỏ nó đi là đổi nghĩa nhãn chứ không phải làm gọn."""
    kind: ClassVar[str] = "text_presence"


@dataclass(frozen=True, slots=True, kw_only=True)
class TextAbsence(Assertion):
    needle: str
    case_sensitive: bool = False
    first_n: int | None = None
    last_n: int | None = None
    kind: ClassVar[str] = "text_absence"


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadingOrder(Assertion):
    before: str
    after: str
    kind: ClassVar[str] = "reading_order"


@dataclass(frozen=True, slots=True, kw_only=True)
class MathPresence(Assertion):
    """Công thức LaTeX phải xuất hiện. Chiếm 3.385/7.019 khẳng định của olmOCR-bench.

    So khớp LaTeX **không phải** so chuỗi: `\\frac{1}{2}` và `\\dfrac{1}{2}` hiển thị
    như nhau. Cách so là việc của B5; ở đây chỉ giữ nguyên chuỗi gốc.
    """

    latex: str
    kind: ClassVar[str] = "math_presence"


@dataclass(frozen=True, slots=True, kw_only=True)
class TableRelation(Assertion):
    """Ô bảng `cell` phải có các ô lân cận / tiêu đề như mô tả.

    Kiểm quan hệ chứ không kiểm HTML: một bảng đúng có thể được viết bằng nhiều
    HTML khác nhau. Trường nào `None` là không ràng buộc.
    """

    cell: str
    up: str | None = None
    down: str | None = None
    left: str | None = None
    right: str | None = None
    top_heading: str | None = None
    left_heading: str | None = None
    kind: ClassVar[str] = "table_relation"


@dataclass(frozen=True, slots=True, kw_only=True)
class Baseline(Assertion):
    """Kiểm vệ sinh: đầu ra không rỗng, không rác. Chỉ 9 khẳng định, nhưng là loại
    duy nhất bắt được engine trả về đúng một trang toàn ký tự thay thế."""

    check_disallowed_characters: bool = False
    kind: ClassVar[str] = "baseline"


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
