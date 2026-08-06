"""Độ chính xác cấu trúc bảng: TEDS và TEDS-Struct — B2 (TASK-080).

TEDS (Tree-Edit-Distance-based Similarity, Zhong et al., PubTabNet) coi mỗi bảng là
một cây `table > tr > td` và đo khoảng cách sửa cây giữa nhãn và kết quả:

    TEDS = 1 − EditDistance(cây_nhãn, cây_đoán) / max(số_nút_nhãn, số_nút_đoán)

Đây là thước duy nhất bắt được điểm mất dữ liệu nặng nhất của Sovereign hiện nay:
`" | ".join(cells)` ở `marker_ocr_service.py` làm phẳng `<table>` thành một dòng,
tức là `rowspan`/`colspan`/số cột **biến mất hoàn toàn** trong khi CER/WER gần như
không đổi — chữ vẫn còn đủ, chỉ cấu trúc là mất.

Bốn quyết định ở file này:

1. **Bám sát cài đặt tham chiếu ở phần lõi.** Chi phí `rename` = 1 khi khác thẻ
   hoặc khác `colspan`/`rowspan`; với `td` cùng dạng thì = Levenshtein chuẩn hoá
   trên **chuỗi token** của ô. Mẫu số là **số nút cây** (`_kich_thuoc`), theo bản
   `table_recognition_metric` chứ không theo `xpath(".//*")` của bản gốc — lý do
   đầy đủ ở docstring của `_kich_thuoc`. `teds_score(..., chuan_hoa=False)` khớp
   đúng bản tham chiếu đó, và `tests/test_teds_metric.py` đối chiếu bằng máy.

2. **Chuẩn hoá lớp vỏ HTML, mặc định BẬT.** Đo thật trên `prediction/` cho thấy hai
   engine viết cùng một bảng theo hai kiểu: Marker ra `<table><tbody><tr><th>…`,
   opendataloader ra `<table><tr><td>…`. Không chuẩn hoá thì mỗi bảng bị trừ đúng
   một nút `tbody` và mỗi ô tiêu đề bị trừ 1 điểm `rename` — đó là đo **quy ước
   sinh HTML**, không phải đo độ chính xác. Nên `thead/tbody/tfoot/colgroup` bị bỏ
   (con `tr` được kéo lên) và `th` đổi thành `td`.

3. **Hai cột, không một.** `teds` tính cả nội dung ô; `teds_struct` bỏ nội dung
   (`structure_only`). Chênh lệch giữa hai cột chỉ đúng một thứ: engine dựng đúng
   lưới nhưng đọc sai chữ trong ô. Gộp lại thành một số là mất chẩn đoán đó.

4. **Nhãn bảng rỗng ⇒ N/A, không phải 0 và cũng không phải 1.0.** Bản gốc trả
   **0.0** khi một phía không có `<table>` — với bench thì đó là bẫy: nhãn hỏng bị
   tính thành engine kém. Ở đây bảng nhãn không có nút nào bị **loại khỏi phép
   đo**; hết bảng nhãn dùng được thì cả tài liệu ra `NO_GROUND_TRUTH`. Chọn N/A chứ
   không chọn 1.0 vì 1.0 sẽ thưởng cho engine phun `<table></table>` rỗng.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from itertools import zip_longest
from typing import ClassVar

from ocr_bench.metrics.base import Metric
from ocr_bench.normalize import normalize_text
from ocr_bench.types import (
    AnnotationGT,
    Capability,
    GroundTruth,
    NAReason,
    OcrResult,
)

__all__ = ["TedsMetric", "TedsStructMetric", "teds_score"]

# Thẻ không có nội dung — `<br>` trong bảng Marker là thẻ hay gặp nhất.
_RONG = frozenset(
    {"br", "img", "hr", "col", "input", "meta", "link", "area", "base", "wbr"}
)
# Lớp vỏ chỉ mang tính quy ước sinh HTML. Xem quyết định 2 ở đầu file.
_VO = frozenset({"thead", "tbody", "tfoot", "colgroup"})
_O = frozenset({"td", "th"})


@dataclass(slots=True)
class _El:
    """Một phần tử HTML. Đủ dùng cho bảng, không phải DOM đầy đủ."""

    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    text: str = ""
    """Chữ ngay sau thẻ mở, trước con đầu tiên."""
    tail: str = ""
    """Chữ ngay sau thẻ đóng của chính nó."""
    children: list[_El] = field(default_factory=list)


class _Doc(HTMLParser):
    """Dựng cây `_El` từ HTML bảng, chịu được thẻ thiếu đóng.

    Không dùng `lxml`: nó là phụ thuộc biên dịch, mà phần HTML cần xử ở đây chỉ là
    một tập con rất nhỏ. Đổi lại phải tự đóng thẻ ngầm — `<td>a<td>b` là hợp lệ
    trong HTML và engine có quyền sinh ra.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.goc = _El("#goc")
        self._ngan: list[_El] = [self.goc]

    # -- tiện ích ---------------------------------------------------------
    def _dong_den(self, tags: frozenset[str]) -> None:
        """Đóng ngầm các thẻ đang mở thuộc `tags` (từ trong ra)."""
        while len(self._ngan) > 1 and self._ngan[-1].tag in tags:
            self._ngan.pop()

    # -- HTMLParser -------------------------------------------------------
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _O:
            self._dong_den(_O)
        elif tag == "tr":
            self._dong_den(_O | {"tr"})
        elif tag in _VO:
            # KHÔNG đóng ngầm khi gặp `<table>`: bảng lồng trong ô là hợp lệ, đóng
            # ngầm ở đó sẽ kéo bảng con ra ngoài ô mẹ.
            self._dong_den(_O | {"tr"} | _VO)

        el = _El(tag, {k: (v or "") for k, v in attrs})
        self._ngan[-1].children.append(el)
        if tag not in _RONG:
            self._ngan.append(el)

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        el = _El(tag, {k: (v or "") for k, v in attrs})
        self._ngan[-1].children.append(el)

    def handle_endtag(self, tag: str) -> None:
        # Thẻ đóng không khớp gì đang mở thì bỏ qua, không làm sập cây.
        for i in range(len(self._ngan) - 1, 0, -1):
            if self._ngan[i].tag == tag:
                del self._ngan[i:]
                return

    def handle_data(self, data: str) -> None:
        hien = self._ngan[-1]
        if hien.children:
            hien.children[-1].tail += data
        else:
            hien.text += data


def _phan_tich(html: str) -> _El:
    p = _Doc()
    p.feed(html)
    p.close()
    return p.goc


def _tim_bang(el: _El) -> _El | None:
    """`<table>` đầu tiên theo thứ tự duyệt trước."""
    if el.tag == "table":
        return el
    for con in el.children:
        thay = _tim_bang(con)
        if thay is not None:
            return thay
    return None


def _chuan_hoa(el: _El) -> _El:
    """Bỏ lớp vỏ, đổi `th` → `td`. Xem quyết định 2 ở đầu file."""
    con: list[_El] = []
    for c in el.children:
        c = _chuan_hoa(c)
        if c.tag in _VO:
            # Kéo `tr` lên thẳng dưới `table`; `tail` của lớp vỏ không mang nghĩa.
            con.extend(c.children)
        else:
            con.append(c)
    return _El(
        tag="td" if el.tag == "th" else el.tag,
        attrs=el.attrs,
        text=el.text,
        tail=el.tail,
        children=con,
    )


def _dem_hau_due(el: _El) -> int:
    """Số phần tử nằm trong `el`. Chỉ dùng để hỏi "bảng này có gì không"."""
    return sum(1 + _dem_hau_due(c) for c in el.children)


def _token(el: _El, *, goc: bool = True) -> list[str]:
    """Chuỗi token của một ô, theo `tokenize()` của bản gốc.

    Bản gốc phát `<td>` … `</td>` rồi cắt bỏ hai đầu (`__tokens__[1:-1]`); ở đây bỏ
    luôn cho khỏi cắt.

    Một chỗ **cố ý lệch** bản tham chiếu: chữ đi qua `normalize_text()` trước khi
    tách ký tự. Lý do NFC/NFD giống hệt B1, cộng thêm: khoảng trắng trong HTML không
    mang nghĩa. Đo thật —

        gt  <td>  Doanh   thu </td>
        pr  <td>Doanh thu</td>
        table_recognition_metric → 0.0      ở đây → 1.0

    Bản tham chiếu chấm **0** cho hai ô hiển thị y hệt nhau. Với bench thì đó là đo
    cách engine thụt lề HTML, không phải đo độ chính xác.

    Lệch chỉ ở đúng chỗ này: quét 600 cặp bảng ngẫu nhiên với nội dung ô **không có
    khoảng trắng** cho 0/600 chênh lệch (`test_khop_ban_tham_chieu_khi_o_khong_co_khoang_trang`),
    và `teds_struct` khớp 600/600 kể cả có khoảng trắng.
    """
    ra: list[str] = []
    if not goc:
        ra.append(f"<{el.tag}>")
    ra.extend(normalize_text(el.text))
    for c in el.children:
        ra.extend(_token(c, goc=False))
    if not goc and el.tag not in _RONG:
        ra.append(f"</{el.tag}>")
    if not goc:
        ra.extend(normalize_text(el.tail))
    return ra


@dataclass(slots=True)
class _Nut:
    """Nút cây cho APTED. Tên trường theo đúng cái `apted.Config` mong đợi."""

    name: str
    colspan: int | None
    rowspan: int | None
    content: list[str] | None
    children: list[_Nut] = field(default_factory=list)


def _so(x: str | None, mac_dinh: int = 1) -> int:
    try:
        return int(str(x))
    except (TypeError, ValueError):
        # `colspan="two"` là HTML hỏng; trình duyệt cũng coi như 1.
        return mac_dinh


def _cay(el: _El, *, structure_only: bool) -> _Nut:
    if el.tag == "td":
        return _Nut(
            name="td",
            colspan=_so(el.attrs.get("colspan")),
            rowspan=_so(el.attrs.get("rowspan")),
            content=[] if structure_only else _token(el),
        )
    return _Nut(
        name=el.tag,
        colspan=None,
        rowspan=None,
        content=None,
        children=[_cay(c, structure_only=structure_only) for c in el.children],
    )


def _kich_thuoc(nut: _Nut) -> int:
    """Số nút của cây — **mẫu số** của TEDS.

    Hai bản tham chiếu đếm khác nhau, và khác biệt này có thật:

    * PubTabNet gốc dùng `len(table.xpath('.//*'))` — hậu duệ của `<table>`, bỏ
      chính nó, nhưng **tính cả** thẻ inline trong ô (`<b>`, `<br/>`).
    * `table_recognition_metric` (bản đóng gói lại, chạy được, dùng để đối chiếu
      trong `tests/test_teds_metric.py`) dùng `tree.size()` — đúng số nút cây, tính
      cả `<table>`, không tính thẻ inline.

    Chọn bản thứ hai, vì hai lý do đo được:

    1. Thẻ inline **không phải nút của cây** — chúng nằm trong `content` của ô, nên
       khoảng cách sửa cây không bao giờ chạm tới chúng. Đưa vào mẫu số là cộng
       điểm miễn phí theo lượng markup: một bảng Marker đầy `<br/>` tự nhiên được
       điểm cao hơn cùng bảng đó viết phẳng.
    2. Đây là bản duy nhất **chạy được** để đối chiếu (AC-01). Bám bản gốc theo chữ
       thì không còn cách nào kiểm chứng bằng máy.

    Chênh lệch thực tế: bảng một ô cho 1 − 1/3 = 0.6667 (ở đây) so với 1 − 1/2 = 0.5
    (công thức `.//*`). Khác về thang, không khác về thứ hạng — mọi bảng đều cùng
    cộng đúng một nút gốc.
    """
    return 1 + sum(_kich_thuoc(c) for c in nut.children)


def _lam_config():  # type: ignore[no-untyped-def]
    """Dựng `CustomConfig` của bản gốc. Nhập lười — `apted` là extra `metrics`."""
    from apted import Config

    class _Config(Config):  # type: ignore[misc]
        valuecls = float

        def rename(self, node1: _Nut, node2: _Nut) -> float:
            if (
                node1.name != node2.name
                or node1.colspan != node2.colspan
                or node1.rowspan != node2.rowspan
            ):
                return 1.0
            a, b = node1.content, node2.content
            if a or b:
                assert a is not None and b is not None
                return _lev(a, b) / max(len(a), len(b))
            return 0.0

    return _Config()


def _lev(a: list[str], b: list[str]) -> int:
    """Levenshtein trên chuỗi token.

    Bản gốc dùng gói `Distance`; ở đây dùng `rapidfuzz` — xem AC-02 trong
    `review.md`: hai gói cho **cùng** kết quả trên 6000 cặp ngẫu nhiên (cả chuỗi ký
    tự lẫn danh sách token), nhưng `rapidfuzz` đã nằm sẵn trong extra `metrics`, có
    wheel dựng sẵn, và còn được bảo trì.
    """
    from rapidfuzz.distance import Levenshtein

    return int(Levenshtein.distance(a, b))


def teds_score(
    html_nhan: str,
    html_doan: str,
    *,
    structure_only: bool = False,
    chuan_hoa: bool = True,
) -> float | None:
    """TEDS của **một** cặp bảng.

    Trả `None` khi bảng nhãn không có nút nào — không có cơ sở để chấm (quyết định
    4). Trả `0.0` khi nhãn có bảng mà phía đoán không có gì đọc được: đó là engine
    trượt thật, không phải nhãn hỏng.
    """
    b_nhan = _tim_bang(_phan_tich(html_nhan or ""))
    if b_nhan is None:
        return None
    if chuan_hoa:
        b_nhan = _chuan_hoa(b_nhan)
    if _dem_hau_due(b_nhan) == 0:
        return None

    b_doan = _tim_bang(_phan_tich(html_doan or ""))
    if b_doan is None:
        return 0.0
    if chuan_hoa:
        b_doan = _chuan_hoa(b_doan)

    from apted import APTED

    cay_nhan = _cay(b_nhan, structure_only=structure_only)
    cay_doan = _cay(b_doan, structure_only=structure_only)
    d = APTED(cay_nhan, cay_doan, _lam_config()).compute_edit_distance()
    diem = 1.0 - float(d) / max(_kich_thuoc(cay_nhan), _kich_thuoc(cay_doan))
    # Kẹp như B1: khoảng cách sửa cây KHÔNG bị chặn bởi mẫu số (hai cây rời nhau
    # hoàn toàn thì phải xoá hết bên này, chèn hết bên kia), nên điểm âm là có thật
    # và sẽ làm `Metric.score()` ném — một engine tệ làm sập cả lượt chấm.
    return max(0.0, min(1.0, diem))


class _TedsBase(Metric):
    """Phần dùng chung: cùng cổng, cùng cách ghép bảng, khác mỗi `structure_only`."""

    requires: ClassVar[frozenset[Capability]] = frozenset({Capability.TABLE_HTML})
    gt_kinds: ClassVar[tuple[type, ...]] = (AnnotationGT,)
    structure_only: ClassVar[bool] = False

    @staticmethod
    def _nhan_dung_duoc(gt: AnnotationGT) -> list[str]:
        """Bảng nhãn có nút. Bảng rỗng bị loại — quyết định 4."""
        ra = []
        for t in gt.tables:
            b = _tim_bang(_phan_tich(t.html or ""))
            if b is not None and _dem_hau_due(_chuan_hoa(b)) > 0:
                ra.append(t.html)
        return ra

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AnnotationGT)  # gt_kinds đã lọc
        if not self._nhan_dung_duoc(gt):
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "nhãn không có bảng nào dùng được",
                "n_bang_nhan": len(gt.tables),
            }
        return None

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        nhan = self._nhan_dung_duoc(gt)
        doan = [t.html for t in result.tables]

        # Ghép theo THỨ TỰ trong tài liệu. Bảng thừa/thiếu ở bất kỳ phía nào đều
        # tính 0: thiếu là engine bỏ sót, thừa là engine bịa — cả hai đều sai, và
        # bỏ qua chúng sẽ thưởng cho engine chỉ xuất đúng những bảng nó tự tin.
        diems: list[float] = []
        for a, b in zip_longest(nhan, doan):
            if a is None or b is None:
                diems.append(0.0)
                continue
            d = teds_score(a, b, structure_only=self.structure_only)
            diems.append(0.0 if d is None else d)

        return sum(diems) / len(diems), {
            "n_bang_nhan": len(nhan),
            "n_bang_doan": len(doan),
            "tung_bang": [round(x, 4) for x in diems],
        }


class TedsMetric(_TedsBase):
    """TEDS đầy đủ: cấu trúc **và** nội dung ô."""

    name: ClassVar[str] = "teds"
    structure_only: ClassVar[bool] = False


class TedsStructMetric(_TedsBase):
    """TEDS-Struct: chỉ cấu trúc, bỏ nội dung ô.

    Cặp `teds` / `teds_struct` mới nói được engine hỏng ở đâu: `teds_struct` cao mà
    `teds` thấp = dựng đúng lưới, đọc sai chữ; cả hai cùng thấp = mất luôn cấu trúc.
    """

    name: ClassVar[str] = "teds_struct"
    structure_only: ClassVar[bool] = True
