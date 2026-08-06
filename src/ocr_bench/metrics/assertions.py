"""B5 — bộ khẳng định đúng/sai của olmOCR-bench.

Loại thước đo thứ hai của bench, khác hẳn nhóm chấm liên tục (CER/TEDS/IoU): thay vì
so toàn văn với một đáp án, nó hỏi từng câu **đúng/sai** về đầu ra —
"chuỗi này phải có mặt", "đoạn A phải đứng trước đoạn B", "ô này phải nằm dưới ô kia".

## Vì sao SÁU lớp metric chứ không một

`Metric.score()` trả **một** `MetricResult` mang **một** `value`. Một lớp nhận cả sáu
loại khẳng định thì *buộc* phải gộp chúng thành một con số — đúng cái AC-02 của
TASK-083 cấm — và cách duy nhất giữ lại chi tiết là nhét vào `detail` rồi trông chờ
người đọc tự tách ra. Bẫy 10 (B4) vừa cho thấy chuyện đó không xảy ra: một trung bình
đã in ra là một trung bình sẽ được trích dẫn.

Nên mỗi loại có lớp riêng. Trong repo này **không tồn tại** đường nào tạo ra con số gộp
sáu loại; muốn có thì phải viết thêm lớp mới, tức là phải cố ý. AC-02 được bảo đảm bằng
cấu trúc, không bằng lời dặn. (Tiền lệ: `imgf1`/`imgiou`, `teds`/`teds_struct`.)

Bộ nhãn có **sáu** loại chứ không phải bốn như AC-02 viết — 4 là con số của lúc chưa
nạp dữ liệu. Số thật trên 1.403 tài liệu / 7.019 khẳng định::

    math_presence  3385   text_absence   823
    reading_order  1061   text_presence  721
    table_relation 1020   baseline         9

## Không có khẳng định thuộc loại này ⇒ N/A, không phải 0.0

Cổng dễ quên nhất, ở `_na_rieng`. Một PDF chỉ mang khẳng định `math` phải ra **N/A**
cho `assert_table_relation`: bộ nhãn không hỏi thì không có gì để chấm, và chấm 0 là
phạt engine vì **nhãn** thiếu. Đúng bài học B3 (`img_f1`) và B4 (`heading`), đổi metric.

## ⚠️ `assert_math_presence` cho CẬN DƯỚI, không cho số so sánh được

olmOCR **dựng ảnh** hai công thức LaTeX rồi so từng điểm ảnh; ở đây so chuỗi sau chuẩn
hoá. So chuỗi chặt hơn — hai LaTeX hiển thị y hệt mà viết khác nhau sẽ bị tính trượt.
Nên điểm loại này **thấp hơn hoặc bằng** điểm olmOCR công bố cho cùng engine. Đó là
chặn dưới và phải đọc như chặn dưới, không phải ước lượng. Loại này chiếm 48% toàn bộ
khẳng định nên cái ngoặc này không nhỏ. `detail` tách `n_khop_nguyen_van` và
`n_khop_sau_chuan_hoa` để thấy phần nào là công của chuẩn hoá.

Bốn loại còn lại bám đúng luật của olmOCR (xem `MUON_VA_KHAC`), nên `max_diffs` giữ
nguyên ý nghĩa gốc và số so sánh được với bảng đã công bố của họ.
"""

from __future__ import annotations

import re
from typing import ClassVar

from ocr_bench.metrics.base import Metric
from ocr_bench.types import (
    Assertion,
    AssertionGT,
    Baseline,
    Capability,
    GroundTruth,
    MathPresence,
    NAReason,
    OcrResult,
    ReadingOrder,
    TableRelation,
    TextAbsence,
    TextPresence,
)

__all__ = [
    "MUON_VA_KHAC",
    "KY_TU_CAM",
    "cua_so",
    "tim_moi_vi_tri",
    "co_mat",
    "chuan_hoa_latex",
    "doc_bang",
    "AssertionMetric",
    "TextPresenceMetric",
    "TextAbsenceMetric",
    "ReadingOrderMetric",
    "MathPresenceMetric",
    "TableRelationMetric",
    "BaselineMetric",
    "METRIC_THEO_LOAI",
]

MUON_VA_KHAC = {
    "text_presence": "y hệt olmOCR: partial_ratio ≥ 1 − max_diffs/len(needle)",
    "text_absence": "y hệt, đảo kết quả; giữ cả first_n/last_n",
    "reading_order": "cùng luật (một vị trí `before` đứng trước một vị trí `after`), "
    "KHÁC cách cài: lặp partial_ratio_alignment thay cho fuzzysearch — "
    "khỏi thêm phụ thuộc, kết quả cùng nghĩa",
    "math_presence": "KHÁC HẲN: olmOCR dựng ảnh so điểm ảnh, ở đây so chuỗi sau "
    "chuẩn hoá ⇒ điểm là CẬN DƯỚI của điểm họ công bố",
    "table_relation": "cùng luật dò quan hệ ô, KHÁC bộ đọc bảng (bảng ống markdown "
    "+ <table> HTML, đọc từ text_md chứ không đòi TABLE_HTML)",
    "baseline": "y hệt: rỗng hoặc chứa ký tự cấm là trượt",
}
"""Mượn gì / khác chỗ nào, để ở dạng dữ liệu để test đọc được và giai đoạn D trích được."""

KY_TU_CAM = "\ufffd"
"""U+FFFD REPLACEMENT CHARACTER — dấu vết của giải mã hỏng. Loại khẳng định `baseline`
là loại duy nhất bắt được engine trả về nguyên một trang toàn ký tự này."""


# ---------------------------------------------------------------------------
# So khớp mờ — dùng chung
# ---------------------------------------------------------------------------


def cua_so(text: str, first_n: int | None, last_n: int | None) -> str:
    """Thu vùng tìm về N ký tự đầu / cuối.

    "Chuỗi này **không** được nằm trong 200 ký tự đầu" là khẳng định khác hẳn "không
    được nằm ở đâu cả" — 104/823 khẳng định `absent` có ràng buộc này. Bỏ nó đi là
    đổi nghĩa nhãn, không phải làm gọn.
    """
    if first_n is not None:
        text = text[:first_n]
    if last_n is not None:
        text = text[-last_n:] if last_n else ""
    return text


def _nguong(needle: str, max_diffs: int) -> float:
    """Ngưỡng tương tự theo đúng công thức olmOCR: ``1 − max_diffs/len(needle)``."""
    if not needle:
        return 1.0
    return max(0.0, 1.0 - max_diffs / len(needle))


def _du_dai(needle: str, haystack: str, max_diffs: int) -> bool:
    """Vùng tìm có đủ dài để chứa `needle` không?

    Cái bẫy: `rapidfuzz.fuzz.partial_ratio` lấy chuỗi **ngắn hơn** làm mẫu rồi trượt
    trên chuỗi dài hơn. Nên khi vùng tìm ngắn hơn kim — chuyện xảy ra ngay khi có
    `first_n`/`last_n`, tức 104/823 khẳng định `absent` — nó đi tìm *vùng trong kim*
    và trả 100. Đọc theo nghĩa của ta thì đó là "có mặt", ngược hẳn sự thật.

    Với `absent` cái ngược ấy đúng chiều nguy hiểm nhất: khẳng định "chuỗi này không
    được nằm trong 200 ký tự đầu" sẽ luôn bị chấm trượt, và engine làm đúng bị trừ điểm.
    """
    return len(haystack) >= len(needle) - max_diffs


def co_mat(
    needle: str, haystack: str, *, max_diffs: int = 0, case_sensitive: bool = False
) -> bool:
    """`needle` có xuất hiện trong `haystack` (cho lệch tới `max_diffs` ký tự)?"""
    from rapidfuzz import fuzz  # extra `metrics` — import trong hàm, đúng lệ nid.py

    if not needle:
        return True
    if not _du_dai(needle, haystack, max_diffs):
        return False
    if not case_sensitive:
        needle, haystack = needle.lower(), haystack.lower()
    return fuzz.partial_ratio(needle, haystack) / 100.0 >= _nguong(needle, max_diffs)


def tim_moi_vi_tri(
    needle: str, haystack: str, *, max_diffs: int = 0, gioi_han: int = 64
) -> list[int]:
    """Mọi vị trí bắt đầu (không chồng nhau) mà `needle` khớp mờ trong `haystack`.

    olmOCR dùng `fuzzysearch.find_near_matches`. Ở đây lặp `partial_ratio_alignment`
    trên phần đuôi còn lại: cùng nghĩa, không phải thêm một phụ thuộc nữa. `gioi_han`
    chặn vòng lặp trên tài liệu dài có chuỗi lặp nhiều lần — quá ngần ấy vị trí thì
    kết luận thứ tự đã không còn dựa vào chuỗi ấy nữa.
    """
    from rapidfuzz import fuzz

    if not needle or not haystack:
        return []
    kim, dong = needle.lower(), haystack.lower()
    nguong = _nguong(kim, max_diffs) * 100.0

    vi_tri: list[int] = []
    lech = 0
    while len(vi_tri) < gioi_han and _du_dai(kim, dong[lech:], max_diffs):
        a = fuzz.partial_ratio_alignment(kim, dong[lech:])
        if a is None or a.score < nguong:
            break
        # `dest_*` chứ KHÔNG phải `src_*`: trong rapidfuzz, `src` là chuỗi thứ nhất
        # (cây kim) còn `dest` là chuỗi thứ hai (đống rơm). Lấy nhầm `src_start` thì
        # nó luôn bằng 0 và vòng lặp chỉ nhích đúng len(kim) mỗi lượt — sinh ra một
        # loạt vị trí đều đặn không có thật, và `reading_order` sẽ ăn điểm miễn phí
        # vì gần như luôn tìm được "một vị trí before đứng trước một vị trí after".
        vi_tri.append(lech + a.dest_start)
        # `max(...,+1)` phòng alignment rỗng → vòng vô hạn.
        lech += max(a.dest_end, a.dest_start + 1)
    return vi_tri


# ---------------------------------------------------------------------------
# LaTeX
# ---------------------------------------------------------------------------

_LATEX_DONG_NGHIA = (
    (re.compile(r"\\dfrac|\\tfrac|\\cfrac"), r"\\frac"),
    (re.compile(r"\\left|\\right|\\!|\\,|\\;|\\:|\\ "), ""),
    (re.compile(r"\\begin\{(?:equation|align|displaymath)\*?\}"), ""),
    (re.compile(r"\\end\{(?:equation|align|displaymath)\*?\}"), ""),
    (re.compile(r"\s+"), ""),
)


def chuan_hoa_latex(s: str) -> str:
    """Gọt những khác biệt LaTeX **chắc chắn** không đổi hình hiển thị.

    Cố ý dè dặt. Mỗi luật thêm vào là một lần nới ngưỡng đạt, và nới sai thì metric
    khen engine viết sai công thức. Thà để lại chặn dưới còn hơn có một con số rộng
    rãi mà không ai kiểm được — xem cảnh báo "cận dưới" ở docstring module.
    """
    s = s.strip()
    for cu, moi in ((re.compile(r"^\$\$|\$\$$"), ""), (re.compile(r"^\$|\$$"), "")):
        s = cu.sub(moi, s).strip()
    if s.startswith("\\[") and s.endswith("\\]"):
        s = s[2:-2]
    if s.startswith("\\(") and s.endswith("\\)"):
        s = s[2:-2]
    for cu, moi in _LATEX_DONG_NGHIA:
        s = cu.sub(moi, s)
    return s


def _cong_thuc_trong(text: str) -> list[str]:
    """Mọi đoạn trông như công thức trong đầu ra markdown."""
    ra: list[str] = []
    for mau in (r"\$\$(.+?)\$\$", r"\$([^$\n]+?)\$", r"\\\[(.+?)\\\]", r"\\\((.+?)\\\)"):
        ra.extend(re.findall(mau, text, flags=re.DOTALL))
    return ra


# ---------------------------------------------------------------------------
# Bảng
# ---------------------------------------------------------------------------

_HANG_NGAN = re.compile(r"^[\s|:\-+=]+$")


def doc_bang(text: str) -> list[list[list[str]]]:
    """Mọi bảng trong `text_md`, dạng lưới ô (hàng × cột).

    Đọc bảng ống markdown và `<table>` HTML. Không đòi năng lực `TABLE_HTML`: khẳng
    định olmOCR được kiểm trên **đầu ra văn bản cuối cùng**, mà phần lớn engine viết
    bảng thành bảng ống ngay trong `text_md`. Đòi `TABLE_HTML` sẽ N/A oan những engine
    làm đúng bằng cách khác.
    """
    bang: list[list[list[str]]] = []

    hien_tai: list[list[str]] = []
    for dong in text.splitlines():
        s = dong.strip()
        if s.startswith("|") and s.count("|") >= 2:
            if _HANG_NGAN.match(s):  # hàng gạch ngăn tiêu đề
                continue
            hien_tai.append([o.strip() for o in s.strip("|").split("|")])
            continue
        if hien_tai:
            bang.append(hien_tai)
            hien_tai = []
    if hien_tai:
        bang.append(hien_tai)

    for tbl in re.findall(r"<table[^>]*>(.*?)</table>", text, re.DOTALL | re.IGNORECASE):
        luoi = [
            [
                re.sub(r"<[^>]+>", "", o).strip()
                for o in re.findall(
                    r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.DOTALL | re.IGNORECASE
                )
            ]
            for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", tbl, re.DOTALL | re.IGNORECASE)
        ]
        luoi = [h for h in luoi if h]
        if luoi:
            bang.append(luoi)

    return bang


def _kiem_quan_he(kd: TableRelation, luoi: list[list[str]]) -> bool:
    """Ô `cell` có mặt trong lưới này và mọi ràng buộc lân cận đều đúng?"""
    md = kd.max_diffs
    for i, hang in enumerate(luoi):
        for j, o in enumerate(hang):
            if not co_mat(kd.cell, o, max_diffs=md):
                continue

            def lay(r: int, c: int) -> str:
                if 0 <= r < len(luoi) and 0 <= c < len(luoi[r]):
                    return luoi[r][c]
                return ""

            ung_vien = {
                "up": lay(i - 1, j),
                "down": lay(i + 1, j),
                "left": lay(i, j - 1),
                "right": lay(i, j + 1),
                "top_heading": lay(0, j),
                "left_heading": lay(i, 0),
            }
            if all(
                co_mat(mong, ung_vien[ten], max_diffs=md)
                for ten in ung_vien
                if (mong := getattr(kd, ten)) is not None
            ):
                return True
    return False


# ---------------------------------------------------------------------------
# Metric
# ---------------------------------------------------------------------------


class AssertionMetric(Metric):
    """Lớp cha: tỉ lệ khẳng định **thuộc đúng một loại** mà đầu ra thoả mãn.

    Lớp con khai `loai` (khớp `Assertion.kind`) và cài `_dat()`. Không lớp con nào
    nhìn thấy khẳng định của loại khác — đó chính là chỗ AC-02 được cài đặt.
    """

    loai: ClassVar[str]
    requires: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})
    gt_kinds: ClassVar[tuple[type, ...]] = (AssertionGT,)
    # AC-03: `Metric.score()` tự trả WRONG_GT_KIND khi gặp AnnotationGT. Không lớp
    # nào ở đây phải viết thêm dòng nào cho việc đó.

    @classmethod
    def _cua_toi(cls, gt: AssertionGT) -> list[Assertion]:
        return [t for t in gt.tests if t.kind == cls.loai]

    def _dat(self, kd: Assertion, text: str) -> bool:
        """Một khẳng định có được thoả mãn không."""
        raise NotImplementedError

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AssertionGT)
        if not self._cua_toi(gt):
            # Tài liệu không mang khẳng định loại này. Bộ nhãn không hỏi thì không
            # có gì để chấm — 0.0 ở đây là phạt engine vì nhãn thiếu.
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": f"tài liệu không có khẳng định loại {self.loai!r}",
                "n_khang_dinh_moi_loai": len(gt.tests),
            }
        return None

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AssertionGT)
        text = result.text_md or ""
        cua_toi = self._cua_toi(gt)
        # Duyệt MỘT lần và giữ kết quả theo vị trí. Lọc kiểu `kd not in dat` sẽ so
        # bằng `__eq__` của dataclass: hai khẳng định trùng nội dung là bằng nhau,
        # nên một cái đạt sẽ che mất cái kia trượt.
        ket_qua = [self._dat(kd, text) for kd in cua_toi]
        n_dat = sum(ket_qua)
        truot = [kd.assertion_id for kd, ok in zip(cua_toi, ket_qua) if not ok]
        return n_dat / len(cua_toi), {
            "loai": self.loai,
            "n_khang_dinh": len(cua_toi),
            "n_dat": n_dat,
            "id_truot": truot[:20],
        }


class TextPresenceMetric(AssertionMetric):
    """Chuỗi phải có mặt trong đầu ra."""

    name: ClassVar[str] = "assert_text_presence"
    loai: ClassVar[str] = TextPresence.kind

    def _dat(self, kd: Assertion, text: str) -> bool:
        assert isinstance(kd, TextPresence)
        return co_mat(
            kd.needle,
            cua_so(text, kd.first_n, kd.last_n),
            max_diffs=kd.max_diffs,
            case_sensitive=kd.case_sensitive,
        )


class TextAbsenceMetric(AssertionMetric):
    """Chuỗi **không** được có mặt (thường là đầu trang / chân trang lọt vào)."""

    name: ClassVar[str] = "assert_text_absence"
    loai: ClassVar[str] = TextAbsence.kind

    def _dat(self, kd: Assertion, text: str) -> bool:
        assert isinstance(kd, TextAbsence)
        return not co_mat(
            kd.needle,
            cua_so(text, kd.first_n, kd.last_n),
            max_diffs=kd.max_diffs,
            case_sensitive=kd.case_sensitive,
        )


class ReadingOrderMetric(AssertionMetric):
    """`before` phải đứng trước `after` trong đầu ra.

    Khác `nid` (B4) ở chỗ: `nid` cần nhãn thứ tự đọc **toàn tài liệu** (DocLayNet không
    có ⇒ N/A 205/205), còn ở đây nhãn chỉ ràng buộc **một cặp** — nên loại này là thứ
    duy nhất trong bench hiện đang thật sự chấm được thứ tự đọc.
    """

    name: ClassVar[str] = "assert_reading_order"
    loai: ClassVar[str] = ReadingOrder.kind

    def _dat(self, kd: Assertion, text: str) -> bool:
        assert isinstance(kd, ReadingOrder)
        truoc = tim_moi_vi_tri(kd.before, text, max_diffs=kd.max_diffs)
        sau = tim_moi_vi_tri(kd.after, text, max_diffs=kd.max_diffs)
        if not truoc or not sau:
            return False
        # Luật olmOCR: đạt nếu *một* vị trí `before` đứng trước *một* vị trí `after`.
        return min(truoc) < max(sau)


class MathPresenceMetric(AssertionMetric):
    """⚠️ **CẬN DƯỚI.** So chuỗi sau chuẩn hoá, không dựng ảnh như olmOCR.

    Điểm ở đây ≤ điểm olmOCR công bố cho cùng engine, vì hai LaTeX hiển thị y hệt mà
    viết khác nhau sẽ bị tính trượt. Đọc như chặn dưới, đừng đọc như ước lượng — xem
    docstring module.
    """

    name: ClassVar[str] = "assert_math_presence"
    loai: ClassVar[str] = MathPresence.kind

    @staticmethod
    def _khop(kd: MathPresence, text: str) -> tuple[bool, bool]:
        """`(đạt, đạt nhờ chuẩn hoá)`."""
        if kd.latex.strip() and kd.latex.strip() in text:
            return True, False
        muc_tieu = chuan_hoa_latex(kd.latex)
        if not muc_tieu:
            return False, False
        for ct in _cong_thuc_trong(text):
            if chuan_hoa_latex(ct) == muc_tieu:
                return True, True
        return False, False

    def _dat(self, kd: Assertion, text: str) -> bool:
        assert isinstance(kd, MathPresence)
        return self._khop(kd, text)[0]

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AssertionGT)
        text = result.text_md or ""
        cua_toi = self._cua_toi(gt)
        nguyen_van = nho_chuan_hoa = 0
        for kd in cua_toi:
            assert isinstance(kd, MathPresence)
            dat, nho = self._khop(kd, text)
            if dat:
                nho_chuan_hoa += nho
                nguyen_van += not nho
        n_dat = nguyen_van + nho_chuan_hoa
        return n_dat / len(cua_toi), {
            "loai": self.loai,
            "n_khang_dinh": len(cua_toi),
            "n_dat": n_dat,
            # Hai con số này là bằng chứng cho cảnh báo "cận dưới": phần nào đạt do
            # engine viết đúng nguyên văn, phần nào chỉ đạt nhờ ta gọt LaTeX.
            "n_khop_nguyen_van": nguyen_van,
            "n_khop_sau_chuan_hoa": nho_chuan_hoa,
            "canh_bao": "cận dưới — olmOCR so bằng ảnh, ở đây so chuỗi",
        }


class TableRelationMetric(AssertionMetric):
    """Ô bảng phải có lân cận / tiêu đề như mô tả."""

    name: ClassVar[str] = "assert_table_relation"
    loai: ClassVar[str] = TableRelation.kind

    def _dat(self, kd: Assertion, text: str) -> bool:
        assert isinstance(kd, TableRelation)
        # Bảng đọc không nổi thì khẳng định trượt, KHÔNG ném lỗi làm hỏng cả tài
        # liệu: một bảng lạ không được phép xoá sổ 6 khẳng định còn lại.
        return any(_kiem_quan_he(kd, luoi) for luoi in doc_bang(text))


class BaselineMetric(AssertionMetric):
    """Vệ sinh đầu ra: không rỗng, không ký tự thay thế.

    Chỉ 9 khẳng định trong toàn bộ bộ nhãn, nhưng là loại duy nhất bắt được engine
    trả về nguyên một trang rác mà mọi metric so khớp khác vẫn cho điểm 0 lặng lẽ.
    """

    name: ClassVar[str] = "assert_baseline"
    loai: ClassVar[str] = Baseline.kind

    def _dat(self, kd: Assertion, text: str) -> bool:
        assert isinstance(kd, Baseline)
        if not text.strip():
            return False
        if kd.check_disallowed_characters and KY_TU_CAM in text:
            return False
        return True


METRIC_THEO_LOAI: dict[str, type[AssertionMetric]] = {
    m.loai: m
    for m in (
        TextPresenceMetric,
        TextAbsenceMetric,
        ReadingOrderMetric,
        MathPresenceMetric,
        TableRelationMetric,
        BaselineMetric,
    )
}
"""Tra cứu loại → lớp. **Không** phải chỗ để gộp điểm: nó ánh xạ 1-1, mỗi loại vẫn ra
`MetricResult` riêng. Ai muốn một con số cho cả sáu loại phải tự viết, và tự chịu."""
