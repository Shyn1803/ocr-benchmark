"""C1 — tự kiểm tra từng thước đo.

Nhóm B viết ra 14 metric. Không nhóm nào trong B kiểm được rằng chúng **đúng**: một
metric viết sai vẫn trả về một con số trong `[0,1]`, vẫn xếp hạng được, vẫn in ra bảng
trông rất thuyết phục. Nó không ném exception và không nhìn thấy bằng mắt. Đây là chỗ
duy nhất bắt được.

Ba tính chất, áp cho **mọi** metric chứ không cho vài cái tiêu biểu:

1. **Identity** — dự đoán trùng đáp án thì phải ra đúng `1.0`.
2. **Đơn điệu** — càng hỏng điểm càng thấp. Áp cho metric ăn chữ.
3. **Bất biến Unicode** — cùng một chữ viết NFC hay NFD phải ra cùng điểm. Áp cho
   metric ăn chữ.

Và một tính chất về chính bộ test: **không metric nào được miễn**. Xem `BANG`.

## Vì sao thang phá huỷ khai ở đây chứ không ở metric

Nếu metric tự cung cấp cách phá huỷ chính nó thì một metric viết sai sẽ cung cấp một
cách phá huỷ mà nó vượt qua được. Thang phải đến từ bên ngoài, và phải hợp ngữ nghĩa
từng metric — `assert_text_absence` chấm chuỗi cấm **vắng mặt**, nên làm hỏng chữ
dự đoán khiến nó ăn điểm *cao hơn*. Một thang dùng chung cho cả 14 metric sẽ báo lỗi ở
đó, mà lỗi nằm ở thang. Xem bẫy 12 của README.

## Gọi `score()`, không gọi `_compute()`

`Metric.score()` mới là cổng: nó chặn `failed`, `requires`, `gt_kinds`, `_na_rieng()`,
rồi ép kết quả về `[0,1]`. Gọi thẳng `_compute()` là bỏ qua đúng cái cổng đang bảo vệ
cả 14 metric — test sẽ xanh trong khi metric trả 1.7.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, replace
from typing import Callable

import pytest

from ocr_bench import registry
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Baseline,
    BlockType,
    Box,
    Capability,
    GroundTruth,
    MathPresence,
    OcrBlock,
    OcrImage,
    OcrResult,
    OcrTable,
    ReadingOrder,
    TableRelation,
    TextAbsence,
    TextPresence,
)

pytest.importorskip("rapidfuzz")
pytest.importorskip("jiwer")
pytest.importorskip("apted")


# ---------------------------------------------------------------------------
# Nguyên liệu
# ---------------------------------------------------------------------------

# Chữ fixture **bắt buộc có dấu tiếng Việt**. Chuỗi ASCII thuần thì NFC và NFD giống
# hệt nhau, và test bất biến Unicode sẽ xanh mà không kiểm gì cả. Có test riêng canh
# điều này (`test_fixture_chu_deu_khac_nhau_giua_nfc_va_nfd`).
CAU = "Điều 5 khoản 2 về việc cấp phép hoạt động"
A, B, C = "Điều 5", "khoản 2", "cấp phép"

BANG_MD = (
    "| Tiêu đề A | Tiêu đề B |\n"
    "| --- | --- |\n"
    "| Điều 5 | khoản 2 |\n"
    "| về việc | cấp phép |\n"
)

BANG_HTML = (
    "<table>"
    "<tr><td>Điều 5</td><td>khoản 2</td></tr>"
    "<tr><td>về việc</td><td>cấp phép</td></tr>"
    "</table>"
)


def _kq(caps: frozenset[Capability], **kw) -> OcrResult:
    return OcrResult(
        engine="thu", engine_version="0", doc_id="d1", capabilities=caps, **kw
    )


def _box(i: int) -> Box:
    return Box(page=0, x0=0.1, y0=0.1 * i, x1=0.9, y1=0.1 * i + 0.08)


def chu_mang_theo(r: OcrResult) -> str:
    """Mọi chữ mà một `OcrResult` chở — dùng để canh fixture và để đổi dạng Unicode."""
    phan = [r.text_md or ""]
    phan += [t.html for t in r.tables]
    phan += [b.text or "" for b in r.blocks]
    phan += [b.html or "" for b in r.blocks]
    return "".join(phan)


def doi_dang(r: OcrResult, dang: str) -> OcrResult:
    """Đổi dạng chuẩn hoá Unicode của **mọi** chữ trong kết quả. Không đụng đáp án.

    Đúng ca thật: đáp án ở dạng NFC, engine xuất ra NFD. Người đọc thấy hai chuỗi y
    hệt nhau.
    """

    def n(s: str | None) -> str | None:
        return None if s is None else unicodedata.normalize(dang, s)

    return replace(
        r,
        text_md=n(r.text_md),
        tables=[replace(t, html=unicodedata.normalize(dang, t.html)) for t in r.tables],
        blocks=tuple(replace(b, text=n(b.text), html=n(b.html)) for b in r.blocks),
    )


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Fixture:
    """Nguyên liệu tính chất cho **một** metric.

    `thang` là thang phá huỷ: bậc 0 phải là dự đoán hoàn hảo, các bậc sau hỏng dần.
    """

    gt: GroundTruth
    thang: tuple[OcrResult, ...]
    la_metric_chu: bool
    mien: str = ""

    @property
    def hoan_hao(self) -> OcrResult:
        return self.thang[0]


# --- cer / wer -------------------------------------------------------------

_GT_CHU = AnnotationGT(doc_id="d1", text=CAU)
_CAP_CHU = frozenset({Capability.TEXT_MD})


def _fx_chu() -> Fixture:
    hong_nhe = CAU.replace("khoản", "khoan").replace("phép", "phep")
    hong_nang = " ".join(CAU.split()[:3])
    return Fixture(
        gt=_GT_CHU,
        thang=tuple(
            _kq(_CAP_CHU, text_md=t) for t in (_GT_CHU.text, hong_nhe, hong_nang)
        ),
        la_metric_chu=True,
    )


# --- teds / teds_struct ----------------------------------------------------

_GT_BANG = AnnotationGT(doc_id="d1", tables=[OcrTable(html=BANG_HTML)])
_CAP_BANG = frozenset({Capability.TABLE_HTML})
_MOT_O = "<table><tr><td>Điều 5</td></tr></table>"


def _kq_bang(html: str) -> OcrResult:
    return _kq(_CAP_BANG, tables=[OcrTable(html=html)])


def _fx_teds() -> Fixture:
    # Nội dung ô sai trước, rồi mất luôn cấu trúc.
    sai_noi_dung = BANG_HTML.replace("khoản 2", "xxx").replace("cấp phép", "yyy")
    return Fixture(
        gt=_GT_BANG,
        thang=(_kq_bang(BANG_HTML), _kq_bang(sai_noi_dung), _kq_bang(_MOT_O)),
        la_metric_chu=True,
    )


def _fx_teds_struct() -> Fixture:
    # `teds_struct` cố tình bỏ qua nội dung ô, nên thang phải phá **cấu trúc**.
    thieu_o = "<table><tr><td>Điều 5</td></tr><tr><td>về việc</td><td>cấp phép</td></tr></table>"
    return Fixture(
        gt=_GT_BANG,
        thang=(_kq_bang(BANG_HTML), _kq_bang(thieu_o), _kq_bang(_MOT_O)),
        la_metric_chu=True,
    )


# --- khẳng định ------------------------------------------------------------


def _gt_kd(*tests) -> AssertionGT:
    return AssertionGT(doc_id="d1", tests=tuple(tests))


def _kq_chu(text: str) -> OcrResult:
    return _kq(_CAP_CHU, text_md=text)


def _fx_text_presence() -> Fixture:
    return Fixture(
        gt=_gt_kd(
            TextPresence(assertion_id="p1", needle=A),
            TextPresence(assertion_id="p2", needle=C),
        ),
        thang=(_kq_chu(CAU), _kq_chu(CAU.replace(C, "")), _kq_chu("")),
        la_metric_chu=True,
    )


def _fx_text_absence() -> Fixture:
    # Nghịch chiều: phá bằng cách **chèn** chuỗi cấm vào. Làm hỏng chữ như các metric
    # khác sẽ khiến chuỗi cấm càng vắng ⇒ điểm càng cao. Bẫy 12 của README.
    cam1, cam2 = "Bản nháp", "Trang 1/2"
    return Fixture(
        gt=_gt_kd(
            TextAbsence(assertion_id="a1", needle=cam1),
            TextAbsence(assertion_id="a2", needle=cam2),
        ),
        thang=(
            _kq_chu(CAU),
            _kq_chu(f"{cam1}\n{CAU}"),
            _kq_chu(f"{cam1}\n{CAU}\n{cam2}"),
        ),
        la_metric_chu=True,
    )


def _fx_reading_order() -> Fixture:
    return Fixture(
        gt=_gt_kd(
            ReadingOrder(assertion_id="r1", before=A, after=B),
            ReadingOrder(assertion_id="r2", before=B, after=C),
        ),
        thang=(
            _kq_chu(f"{A}\n\n{B}\n\n{C}"),
            _kq_chu(f"{A}\n\n{C}\n\n{B}"),  # r2 hỏng
            _kq_chu(f"{C}\n\n{B}\n\n{A}"),  # cả hai hỏng
        ),
        la_metric_chu=True,
    )


_CT1, _CT2 = "E = mc^2", "a^2 + b^2 = c^2"


def _fx_math() -> Fixture:
    return Fixture(
        gt=_gt_kd(
            MathPresence(assertion_id="m1", latex=_CT1),
            MathPresence(assertion_id="m2", latex=_CT2),
        ),
        thang=(
            _kq_chu(f"Công thức Điều 5: ${_CT1}$ và ${_CT2}$."),
            _kq_chu(f"Công thức Điều 5: ${_CT1}$ và $a^2 + b^2 = d^2$."),
            _kq_chu("Công thức Điều 5: không có gì."),
        ),
        la_metric_chu=True,
    )


def _fx_table_relation() -> Fixture:
    return Fixture(
        gt=_gt_kd(
            TableRelation(
                assertion_id="t1", cell="Điều 5", right="khoản 2", top_heading="Tiêu đề A"
            ),
            TableRelation(
                assertion_id="t2",
                cell="cấp phép",
                left="về việc",
                top_heading="Tiêu đề B",
            ),
        ),
        thang=(
            _kq_chu(BANG_MD),
            _kq_chu(BANG_MD.replace("khoản 2", "xxx")),  # t1 hỏng
            _kq_chu(CAU),  # không còn bảng nào
        ),
        la_metric_chu=True,
    )


def _fx_baseline() -> Fixture:
    return Fixture(
        gt=_gt_kd(Baseline(assertion_id="b1", check_disallowed_characters=True)),
        thang=(_kq_chu(CAU), _kq_chu(f"{CAU}�")),
        la_metric_chu=True,
    )


# --- hình học --------------------------------------------------------------

_HOP = (_box(0), _box(1), _box(2))
_LY_DO_HINH = "chỉ ăn toạ độ hộp, không ăn chữ — AC-02/AC-03 không có nghĩa"


def _fx_anh() -> Fixture:
    caps = frozenset({Capability.IMAGE_BBOX})
    return Fixture(
        gt=AnnotationGT(doc_id="d1", images=_HOP),
        thang=(_kq(caps, images=tuple(OcrImage(box=b) for b in _HOP)),),
        la_metric_chu=False,
        mien=_LY_DO_HINH,
    )


def _fx_nid() -> Fixture:
    caps = frozenset({Capability.BLOCK_BBOX})
    khoi = tuple(OcrBlock(block_type=BlockType.TEXT, box=b) for b in _HOP)
    return Fixture(
        gt=AnnotationGT(doc_id="d1", blocks=khoi, reading_order=(0, 1, 2)),
        thang=(_kq(caps, blocks=khoi),),
        la_metric_chu=False,
        mien=_LY_DO_HINH,
    )


def _fx_heading() -> Fixture:
    loai = (BlockType.TITLE, BlockType.HEADING, BlockType.HEADING)
    return Fixture(
        gt=AnnotationGT(
            doc_id="d1",
            blocks=tuple(
                OcrBlock(block_type=t, box=b) for t, b in zip(loai, _HOP)
            ),
        ),
        thang=(
            _kq(
                frozenset({Capability.BLOCK_BBOX, Capability.HEADING_LEVEL}),
                blocks=tuple(
                    OcrBlock(block_type=BlockType.HEADING, box=b, level=c)
                    for b, c in zip(_HOP, (1, 2, 2))
                ),
            ),
        ),
        la_metric_chu=False,
        mien="chỉ ăn loại/cấp block, không ăn chữ — AC-02/AC-03 không có nghĩa",
    )


# --- dấu tiếng Việt --------------------------------------------------------


def _fx_dau() -> Fixture:
    # Phá bằng cách **bỏ dấu**, không phải bằng cách đổi chữ: metric này chỉ nhìn
    # dấu, nên hỏng kiểu khác thì điểm không nhúc nhích.
    bo_mot_phan = CAU.replace("khoản", "khoan").replace("phép", "phep")
    bo_het = unicodedata.normalize("NFD", CAU)
    bo_het = "".join(c for c in bo_het if not unicodedata.combining(c))
    return Fixture(
        gt=_GT_CHU,
        thang=tuple(_kq(_CAP_CHU, text_md=t) for t in (CAU, bo_mot_phan, bo_het)),
        la_metric_chu=True,
    )


# --- bố cục ----------------------------------------------------------------

_LOAI_KHOI = (BlockType.TEXT, BlockType.TABLE, BlockType.PICTURE)
_KHOI_NHAN = tuple(
    OcrBlock(block_type=t, box=b) for t, b in zip(_LOAI_KHOI, _HOP)
)
_CAP_KHOI = frozenset({Capability.BLOCK_BBOX})


def _fx_block_f1() -> Fixture:
    return Fixture(
        gt=AnnotationGT(doc_id="d1", blocks=_KHOI_NHAN),
        thang=(_kq(_CAP_KHOI, blocks=_KHOI_NHAN),),
        la_metric_chu=False,
        mien=_LY_DO_HINH,
    )


def _fx_type_f1() -> Fixture:
    return Fixture(
        gt=AnnotationGT(doc_id="d1", blocks=_KHOI_NHAN),
        thang=(_kq(_CAP_KHOI, blocks=_KHOI_NHAN),),
        la_metric_chu=False,
        mien="chỉ ăn loại/khung block, không ăn chữ — AC-02/AC-03 không có nghĩa",
    )


# --- ô bảng / định vị bảng -------------------------------------------------


def _fx_cell_f1() -> Fixture:
    thieu_o = (
        "<table><tr><td>Điều 5</td></tr>"
        "<tr><td>về việc</td><td>cấp phép</td></tr></table>"
    )
    return Fixture(
        gt=_GT_BANG,
        thang=(_kq_bang(BANG_HTML), _kq_bang(thieu_o), _kq_bang(_MOT_O)),
        la_metric_chu=True,
    )


def _fx_table_recall() -> Fixture:
    # `table_recall` chỉ nhìn khung, nhưng vẫn qua cổng `TABLE_HTML` — nhãn phải có
    # cả html lẫn box, nếu không `_na_rieng()` trả NO_GROUND_TRUTH.
    khung = _box(0)
    return Fixture(
        gt=AnnotationGT(
            doc_id="d1", tables=[OcrTable(html=BANG_HTML, box=khung)]
        ),
        thang=(
            _kq(_CAP_BANG, tables=[OcrTable(html=BANG_HTML, box=khung)]),
        ),
        la_metric_chu=False,
        mien="chỉ ăn khung bảng, không ăn chữ — AC-02/AC-03 không có nghĩa",
    )


# ---------------------------------------------------------------------------
# BẢNG — nguồn sự thật của AC-04
# ---------------------------------------------------------------------------

BANG: dict[str, Fixture] = {
    "cer": _fx_chu(),
    "wer": _fx_chu(),
    "teds": _fx_teds(),
    "teds_struct": _fx_teds_struct(),
    "assert_text_presence": _fx_text_presence(),
    "assert_text_absence": _fx_text_absence(),
    "assert_reading_order": _fx_reading_order(),
    "assert_math_presence": _fx_math(),
    "assert_table_relation": _fx_table_relation(),
    "assert_baseline": _fx_baseline(),
    "img_f1": _fx_anh(),
    "img_iou": _fx_anh(),
    "nid": _fx_nid(),
    "heading": _fx_heading(),
    "diacritics_acc": _fx_dau(),
    "block_f1": _fx_block_f1(),
    "type_f1": _fx_type_f1(),
    "cell_f1": _fx_cell_f1(),
    "table_recall": _fx_table_recall(),
}

MOI_METRIC = sorted(BANG)
METRIC_CHU = sorted(t for t, f in BANG.items() if f.la_metric_chu)


def cham(ten: str, r: OcrResult):
    """Qua `score()` — cổng thật. Xem docstring module."""
    return registry.get_metric(ten)().score(BANG[ten].gt, r)


# ---------------------------------------------------------------------------
# AC-04 — không metric nào được miễn
# ---------------------------------------------------------------------------


def test_moi_metric_dang_ky_deu_co_fixture():
    """Thêm metric mà quên fixture ⇒ đỏ. Xoá metric mà quên dọn fixture ⇒ cũng đỏ.

    Đây là lý do `BANG` được so với `registry.list_metrics()` chứ không phải với một
    danh sách chép tay: danh sách chép tay im lặng đúng lúc cần kêu.
    """
    assert set(registry.list_metrics()) == set(BANG)


def test_fixture_chu_deu_khac_nhau_giua_nfc_va_nfd():
    """Canh chính bộ test: chuỗi ASCII thuần làm AC-03 kiểm rỗng mà vẫn xanh."""
    for ten in METRIC_CHU:
        chu = chu_mang_theo(BANG[ten].hoan_hao)
        assert unicodedata.normalize("NFC", chu) != unicodedata.normalize("NFD", chu), (
            f"{ten}: fixture không có ký tự tổ hợp được, test bất biến Unicode sẽ rỗng"
        )


def test_metric_hinh_hoc_phai_khai_ly_do_duoc_mien():
    """Miễn AC-02/AC-03 phải là lựa chọn viết ra, không phải hệ quả của việc quên."""
    for ten, fx in BANG.items():
        if not fx.la_metric_chu:
            assert fx.mien, f"{ten}: miễn mà không nói vì sao"


# ---------------------------------------------------------------------------
# AC-01 — identity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("ten", MOI_METRIC)
def test_identity_dung_dap_an_ra_mot_cham_khong(ten: str):
    """Dự đoán dựng **từ** đáp án phải ra đúng 1.0.

    Khẳng định cả `is_na` và `na_reason`, không chỉ `value`: N/A ở đây nghĩa là fixture
    dựng sai (thiếu capability, sai `gt_kinds`, trượt `_na_rieng()`) chứ không phải
    metric đúng — và `value is None` đem so với 1.0 chỉ ném `TypeError`, không nói ra
    được lý do.
    """
    kq = cham(ten, BANG[ten].hoan_hao)
    assert kq.is_na is False, f"{ten}: {kq.na_reason} · {kq.detail}"
    assert kq.na_reason is None, f"{ten}: {kq.detail}"
    assert kq.value == pytest.approx(1.0), f"{ten}: {kq.value} · {kq.detail}"


# ---------------------------------------------------------------------------
# AC-02 — đơn điệu
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("ten", METRIC_CHU)
def test_hong_cang_nhieu_diem_cang_thap(ten: str):
    """Không tăng, và có **ít nhất một** lần giảm thật.

    Chỉ đòi "không tăng" là chưa đủ: một metric trả hằng số 1.0 cũng không tăng.
    """
    diem = [cham(ten, r).value for r in BANG[ten].thang]
    assert diem[0] == pytest.approx(1.0), f"{ten}: bậc 0 phải là dự đoán hoàn hảo"
    for i in range(1, len(diem)):
        assert diem[i] <= diem[i - 1] + 1e-9, f"{ten}: bậc {i} tăng — {diem}"
    assert min(diem) < diem[0] - 1e-9, f"{ten}: thang không hạ được điểm — {diem}"


# ---------------------------------------------------------------------------
# AC-03 — bất biến Unicode
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("ten", METRIC_CHU)
def test_nfd_van_ra_mot_cham_khong(ten: str):
    """Đáp án NFC, engine xuất NFD — người đọc thấy hai chuỗi y hệt nhau.

    Tiếng Việt là chỗ này nguy hiểm nhất: "ề" viết được bằng 1, 2 hoặc 3 điểm mã.
    Không chuẩn hoá thì điểm của một engine phụ thuộc vào việc nó xuất dạng nào,
    chứ không phụ thuộc vào việc nó đọc đúng hay sai.
    """
    kq = cham(ten, doi_dang(BANG[ten].hoan_hao, "NFD"))
    assert kq.value == pytest.approx(1.0), f"{ten}: {kq.value} · {kq.detail}"


@pytest.mark.parametrize("ten", METRIC_CHU)
def test_nfc_va_nfd_ra_cung_mot_diem_o_moi_bac(ten: str):
    """Bất biến không chỉ ở điểm 1.0 — nếu chỉ đúng ở đỉnh thì bảng vẫn lệch."""
    for i, r in enumerate(BANG[ten].thang):
        a = cham(ten, doi_dang(r, "NFC")).value
        b = cham(ten, doi_dang(r, "NFD")).value
        assert a == pytest.approx(b), f"{ten} bậc {i}: NFC={a} NFD={b}"
