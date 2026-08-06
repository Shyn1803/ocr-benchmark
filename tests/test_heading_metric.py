"""B4 — `heading` (TASK-082).

`heading` không gọi `rapidfuzz`, nhưng nó import `ghep_theo_tam` từ `nid.py`, và
`nid.py` chỉ import `rapidfuzz` **bên trong hàm** — nên file này chạy được trên máy
chưa cài extra. Không `importorskip`, và đó là chủ ý: nếu ai đó đưa import
`rapidfuzz` lên đầu `nid.py` thì file này đỏ ngay.
"""

from __future__ import annotations

import pytest

from ocr_bench.metrics.heading import (
    CAP_NHAN,
    HeadingMetric,
    cap_cua_nhan,
    dong_thuan_cap,
)
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Box,
    BlockType,
    Capability,
    NAReason,
    OcrBlock,
    OcrResult,
)


def _b(i: int) -> Box:
    y = 0.05 + i * 0.1
    return Box(x0=0.1, y0=y, x1=0.9, y1=y + 0.08, page=0)


def _nhan(*loai: BlockType) -> AnnotationGT:
    return AnnotationGT(
        doc_id="d1",
        blocks=tuple(
            OcrBlock(block_type=t, box=_b(i)) for i, t in enumerate(loai)
        ),
    )


def _doan(*cap: int | None) -> OcrResult:
    """Engine trả tiêu đề ở cùng vị trí, với `level` cho trước."""
    return OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=CAP_DU,
        blocks=tuple(
            OcrBlock(block_type=BlockType.HEADING, box=_b(i), level=c)
            for i, c in enumerate(cap)
        ),
    )


T, H, X = BlockType.TITLE, BlockType.HEADING, BlockType.TEXT

CAP_DU = frozenset({Capability.BLOCK_BBOX, Capability.HEADING_LEVEL})


# --- cấp của nhãn ------------------------------------------------------------


def test_nhan_doclaynet_khong_co_level_thi_lay_theo_loai() -> None:
    assert cap_cua_nhan(OcrBlock(block_type=T, box=_b(0))) == CAP_NHAN[T] == 1
    assert cap_cua_nhan(OcrBlock(block_type=H, box=_b(0))) == CAP_NHAN[H] == 2


def test_level_do_engine_khai_duoc_uu_tien() -> None:
    assert cap_cua_nhan(OcrBlock(block_type=H, box=_b(0), level=4)) == 4


def test_khong_phai_tieu_de_thi_None() -> None:
    assert cap_cua_nhan(OcrBlock(block_type=X, box=_b(0))) is None


# --- AC-02: đo phân cấp, KHÔNG đếm -------------------------------------------


def test_cung_so_tieu_de_nhung_phan_cap_khac_nhau_thi_diem_khac_nhau() -> None:
    """Đây là AC-02 phát biểu thành test. Cả hai engine đều trả **đúng 3 tiêu đề**
    ở **đúng 3 vị trí** — phép đếm không phân biệt nổi. Phân cấp thì có."""
    gt = _nhan(T, H, H)
    dung = HeadingMetric().score(gt, _doan(1, 2, 2))
    phang = HeadingMetric().score(gt, _doan(1, 1, 1))
    assert dung.value == 1.0
    assert phang.value is not None and phang.value < 1.0


def test_thang_khac_nhau_khong_bi_phat() -> None:
    """Engine đánh `##`/`###` còn nhãn đánh 1/2. Quan hệ giống nhau ⇒ 1.0. So số
    tuyệt đối sẽ chấm 0 ở đây, và đó là phạt engine vì dùng thang khác."""
    r = HeadingMetric().score(_nhan(T, H, H), _doan(2, 3, 3))
    assert r.value == 1.0


def test_dao_nguoc_phan_cap_thi_tut_sau() -> None:
    """Engine coi tiêu đề chính là cấp sâu nhất và hai mục con là cấp trên.

    Không phải 0.0, và đó là đúng: cặp (mục con, mục con) nhãn nói "=", engine
    cũng nói "=" — quan hệ đó engine nói **đúng**. Chỉ 2/3 cặp sai. Chấm 0.0 sẽ là
    tính cả cặp engine làm đúng thành sai.
    """
    r = HeadingMetric().score(_nhan(T, H, H), _doan(3, 1, 1))
    assert r.value == pytest.approx(1 / 3)


def test_dong_thuan_cap_dem_dung_so_cap() -> None:
    diem, ct = dong_thuan_cap([1, 2, 2], [1, 2, 2])
    assert diem == 1.0 and ct["n_cap"] == 3
    diem, ct = dong_thuan_cap([1, 2, 2], [1, 1, 1])
    assert ct["n_cap_dong_thuan"] == 1  # chỉ cặp (2,3) là "=" ở cả hai bên
    assert diem == pytest.approx(1 / 3)


def test_dong_thuan_cap_rong_thi_0_khong_phai_chia_cho_0() -> None:
    assert dong_thuan_cap([], [])[0] == 0.0


# --- ghép cặp ----------------------------------------------------------------


def test_engine_xe_mot_tieu_de_thanh_hai_dong_thi_lay_dong_dau() -> None:
    gt = _nhan(T, H)
    tren = _b(0)
    nua = Box(x0=0.1, y0=tren.y0, x1=0.9, y1=tren.y0 + 0.04, page=0)
    duoi = Box(x0=0.1, y0=tren.y0 + 0.04, x1=0.9, y1=tren.y1, page=0)
    kq = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=CAP_DU,
        blocks=(
            OcrBlock(block_type=H, box=nua, level=1),
            OcrBlock(block_type=H, box=duoi, level=1),
            OcrBlock(block_type=H, box=_b(1), level=2),
        ),
    )
    r = HeadingMetric().score(gt, kq)
    assert r.detail["n_ghep_duoc"] == 2
    assert r.value == 1.0


def test_block_khong_phai_tieu_de_bi_bo_qua() -> None:
    gt = _nhan(T, X, H)
    r = HeadingMetric().score(gt, _doan(1, 9, 2))
    assert r.detail["n_tieu_de_nhan"] == 2
    assert r.value == 1.0


# --- ranh giới N/A (§6) ------------------------------------------------------


def test_khong_khai_BLOCK_BBOX_thi_NA() -> None:
    khong_khai = OcrResult(
        engine="giả", engine_version="0", doc_id="d1", capabilities=frozenset()
    )
    r = HeadingMetric().score(_nhan(T, H), khong_khai)
    assert r.na_reason is NAReason.MISSING_CAPABILITY


def test_khai_BLOCK_BBOX_ma_khong_khai_HEADING_LEVEL_thi_NA_chu_khong_phai_0() -> None:
    """Ca thật của pdf_inspector: nó cắt được box (`block_bbox`) nhưng không phân
    loại tiêu đề bao giờ — 0 block tiêu đề trên cả 204 tài liệu. Gate chỉ theo
    `BLOCK_BBOX` sẽ chấm nó **0.0 trên 17 tài liệu**, tức phạt nó vì một việc nó
    chưa từng nhận làm. Đúng lỗi B3 đã ghi lại và tránh được.
    """
    chi_co_box = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.BLOCK_BBOX}),
        blocks=(OcrBlock(block_type=X, box=_b(0)),),
    )
    r = HeadingMetric().score(_nhan(T, H), chi_co_box)
    assert r.na_reason is NAReason.MISSING_CAPABILITY
    assert r.value is None


def test_khong_doi_SECTION_HIERARCHY() -> None:
    """Cấp không phải cây. opendataloader khai cấp 1..7 nhưng JSON phẳng nên không
    khai được `section_hierarchy`; đòi cây ở đây sẽ loại đúng cái engine duy nhất
    hiện chấm được, và `heading` không còn số nào.
    """
    assert Capability.SECTION_HIERARCHY not in HeadingMetric.requires
    assert HeadingMetric.requires == {Capability.BLOCK_BBOX, Capability.HEADING_LEVEL}


def test_duoi_2_tieu_de_trong_nhan_thi_NA() -> None:
    r = HeadingMetric().score(_nhan(T, X, X), _doan(1, 2, 2))
    assert r.na_reason is NAReason.NO_GROUND_TRUTH


def test_nhan_chi_co_MOT_cap_thi_NA_chu_khong_phai_1() -> None:
    """Chấm 1.0 ở đây là rót điểm miễn phí cho phần lớn bộ mẫu (tài liệu chỉ có
    `Section-header`, không có `Title`) — đúng lỗi đã tránh ở B3."""
    r = HeadingMetric().score(_nhan(H, H, H), _doan(1, 2, 3))
    assert r.na_reason is NAReason.NO_GROUND_TRUTH
    assert r.value is None


def test_engine_chi_cham_mot_cap_nhan_thi_NA() -> None:
    """Nhãn có 2 cấp nhưng engine chỉ ghép trúng hai `Section-header`. Mọi cặp đều
    là "=", nên engine gắn phẳng sẽ được 1.0 — điểm đó không kiểm chứng gì. Chấm 0
    cũng sai: engine không làm gì sai."""
    gt = _nhan(T, H, H)
    kq = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=CAP_DU,
        blocks=(
            OcrBlock(block_type=H, box=_b(1), level=1),
            OcrBlock(block_type=H, box=_b(2), level=1),
        ),
    )
    r = HeadingMetric().score(gt, kq)
    assert r.na_reason is NAReason.NO_GROUND_TRUTH


def test_engine_khong_ghep_duoc_tieu_de_nao_thi_0_khong_phai_NA() -> None:
    """Khai `BLOCK_BBOX` rồi mà bỏ sót hết tiêu đề là lỗi engine — tiền lệ B3."""
    gt = _nhan(T, H, H)
    kq = OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=CAP_DU,
        blocks=(),
    )
    r = HeadingMetric().score(gt, kq)
    assert r.na_reason is None and r.value == 0.0


def test_sai_kieu_ground_truth_thi_NA() -> None:
    r = HeadingMetric().score(AssertionGT(doc_id="d1"), _doan(1, 2))
    assert r.na_reason is NAReason.WRONG_GT_KIND


# --- trần 2 mức: nói thẳng, không im lặng ------------------------------------


def test_docstring_canh_bao_tran_hai_muc() -> None:
    """Trần nhãn 2 mức là giới hạn dễ bị đọc thành "engine phân cấp tốt". Nếu ai
    đó xoá cảnh báo khỏi docstring thì test này đỏ."""
    import ocr_bench.metrics.heading as m

    assert "2 MỨC" in m.__doc__
    assert "###" in m.__doc__


def test_khong_phan_biet_duoc_long_sau_dung_hay_sai() -> None:
    """Vế thực nghiệm của cảnh báo trên.

    Hai engine lồng ngược nhau ở hai mục con (`###`/`####` so với `####`/`###`) —
    **một trong hai sai**. Nhãn chỉ có 2 mức nên nó nói cả hai mục con là "=", và
    metric chấm **hai engine bằng nhau**. Đây là giới hạn ĐÃ BIẾT của nhãn, không
    phải bug của metric: `heading` cao chỉ có nghĩa "không đảo tiêu đề chính với
    tiêu đề mục".
    """
    gt = _nhan(T, H, H)
    a = HeadingMetric().score(gt, _doan(1, 3, 4))
    b = HeadingMetric().score(gt, _doan(1, 4, 3))
    assert a.value == b.value
