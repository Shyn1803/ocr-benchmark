"""B4 — `nid` (TASK-082).

`importorskip("rapidfuzz")`: `nid_score` gọi `rapidfuzz.distance.Indel`, mà
`rapidfuzz` là extra `metrics`. Hai hàm thuần (`ghep_theo_tam`, `chuoi_thu_tu`)
không cần nó, nhưng skip cả file thì đơn giản hơn là skip lẻ từng test.
"""

from __future__ import annotations

import random

import pytest

pytest.importorskip("rapidfuzz")

from ocr_bench.metrics.nid import (  # noqa: E402
    MUON_VA_KHAC,
    NidMetric,
    chuoi_thu_tu,
    ghep_theo_tam,
    nid_score,
)
from ocr_bench.types import (  # noqa: E402
    AnnotationGT,
    AssertionGT,
    Box,
    BlockType,
    Capability,
    NAReason,
    OcrBlock,
    OcrResult,
)


def _b(x0: float, y0: float, x1: float, y1: float, page: int = 0) -> Box:
    return Box(x0=x0, y0=y0, x1=x1, y1=y1, page=page)


def _hang(i: int, cao: float = 0.08) -> Box:
    """Băng ngang thứ `i`, xếp từ trên xuống — mô hình tài liệu một cột."""
    y = 0.05 + i * 0.1
    return _b(0.1, y, 0.9, y + cao)


def _gt(*boxes: Box, thu_tu: tuple[int, ...] | None = None) -> AnnotationGT:
    return AnnotationGT(
        doc_id="d1",
        blocks=tuple(OcrBlock(block_type=BlockType.TEXT, box=b) for b in boxes),
        reading_order=tuple(range(len(boxes))) if thu_tu is None else thu_tu,
    )


def _kq(*boxes: Box) -> OcrResult:
    return OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.BLOCK_BBOX}),
        blocks=tuple(OcrBlock(block_type=BlockType.TEXT, box=b) for b in boxes),
    )


# --- ghép theo tâm -----------------------------------------------------------


def test_tam_nam_trong_thi_ghep_duoc_ke_ca_khi_iou_rat_thap() -> None:
    """Đây là toàn bộ lý do B4 không dùng IoU: một DÒNG nằm trong một ĐOẠN."""
    doan_nhan = _b(0.1, 0.1, 0.9, 0.5)
    mot_dong = _b(0.1, 0.12, 0.9, 0.16)
    assert doan_nhan.iou(mot_dong) < 0.2  # IoU sẽ loại cặp này
    assert ghep_theo_tam([doan_nhan], [mot_dong]) == [0]


def test_tam_ngoai_moi_nhan_thi_None() -> None:
    assert ghep_theo_tam([_b(0.1, 0.1, 0.2, 0.2)], [_b(0.7, 0.7, 0.8, 0.8)]) == [None]


def test_khac_trang_thi_khong_ghep() -> None:
    assert ghep_theo_tam(
        [_b(0.1, 0.1, 0.9, 0.9, page=0)], [_b(0.2, 0.2, 0.3, 0.3, page=1)]
    ) == [None]


def test_nhan_long_nhau_thi_chon_box_NHO_NHAT() -> None:
    """Caption nằm trong picture. Chọn box lớn thì mọi thứ bên trong quy về cùng
    một chỉ số và bị bước gộp trùng xoá sạch — mất luôn thông tin thứ tự."""
    to = _b(0.1, 0.1, 0.9, 0.9)
    nho = _b(0.4, 0.4, 0.6, 0.6)
    assert ghep_theo_tam([to, nho], [_b(0.45, 0.45, 0.55, 0.55)]) == [1]


# --- gộp trùng liên tiếp -----------------------------------------------------


def test_gop_trung_lien_tiep() -> None:
    assert chuoi_thu_tu([3, 3, 3, 5, 5, 7]) == [3, 5, 7]


def test_khong_gop_khi_khong_lien_tiep() -> None:
    """`[3,5,3]` là engine quay lại đoạn đã đọc — lỗi thứ tự thật, phải giữ."""
    assert chuoi_thu_tu([3, 5, 3]) == [3, 5, 3]


def test_bo_None() -> None:
    assert chuoi_thu_tu([None, 2, None, 2, 4]) == [2, 4]


# --- AC-03: đảo đoạn phải làm điểm giảm --------------------------------------


def test_dung_thu_tu_thi_1() -> None:
    nhan = [_hang(i) for i in range(5)]
    diem, _ = nid_score([0, 1, 2, 3, 4], nhan, list(nhan))
    assert diem == 1.0


def test_dao_hai_doan_lien_nhau_thi_TUT() -> None:
    nhan = [_hang(i) for i in range(5)]
    doan = [nhan[0], nhan[2], nhan[1], nhan[3], nhan[4]]
    diem, _ = nid_score([0, 1, 2, 3, 4], nhan, doan)
    assert diem < 1.0


def test_dao_cang_nhieu_diem_cang_thap() -> None:
    nhan = [_hang(i) for i in range(8)]
    tt = list(range(8))
    diem_dung, _ = nid_score(tt, nhan, list(nhan))
    diem_dao1, _ = nid_score(tt, nhan, [nhan[i] for i in [0, 2, 1, 3, 4, 5, 6, 7]])
    diem_dao_het, _ = nid_score(tt, nhan, list(reversed(nhan)))
    assert diem_dung > diem_dao1 > diem_dao_het


def test_chia_mot_doan_thanh_5_block_dung_thu_tu_thi_VAN_1() -> None:
    """Vế đối bắt buộc của test trên. Không có nó thì `nid` có thể đang đo độ mịn
    mà mọi test kia vẫn xanh — và pdf_inspector (block = dòng, mịn gấp 6 lần) sẽ
    bị chấm 0 vì chia nhỏ chứ không phải vì đọc sai."""
    nhan = [_hang(i) for i in range(3)]
    doan: list[Box] = []
    for h in nhan:
        cao = (h.y1 - h.y0) / 5
        doan += [_b(h.x0, h.y0 + k * cao, h.x1, h.y0 + (k + 1) * cao) for k in range(5)]
    assert len(doan) == 15
    diem, ct = nid_score([0, 1, 2], nhan, doan)
    assert diem == 1.0
    assert ct["n_doan"] == 15 and ct["do_dai_chuoi_doan"] == 3


def test_chia_nho_NHUNG_dao_thu_tu_thi_van_tut() -> None:
    """Gộp trùng không được nuốt mất lỗi thứ tự."""
    nhan = [_hang(i) for i in range(3)]

    def xe(h: Box) -> list[Box]:
        cao = (h.y1 - h.y0) / 3
        return [_b(h.x0, h.y0 + k * cao, h.x1, h.y0 + (k + 1) * cao) for k in range(3)]

    doan = xe(nhan[0]) + xe(nhan[2]) + xe(nhan[1])
    diem, _ = nid_score([0, 1, 2], nhan, doan)
    assert diem < 1.0


def test_bo_sot_block_khong_bi_phat_o_day() -> None:
    """Bỏ sót là chuyện của B3/B6 (độ phủ). Phạt ở `nid` nữa là phạt hai lần cùng
    một lỗi, và làm `nid` không còn đo riêng thứ tự."""
    nhan = [_hang(i) for i in range(5)]
    diem, ct = nid_score([0, 1, 2, 3, 4], nhan, [nhan[0], nhan[3]])
    assert diem == 1.0
    assert ct["do_dai_chuoi_tham_chieu"] == 2


# --- khoảng giá trị ----------------------------------------------------------


def test_moi_diem_deu_trong_khoang() -> None:
    rng = random.Random(82)
    for _ in range(200):
        n = rng.randint(2, 7)
        nhan = [_hang(i) for i in range(n)]
        doan = [nhan[i] for i in rng.sample(range(n), rng.randint(1, n))]
        doan += [_b(0.95, 0.95, 0.99, 0.99)] * rng.randint(0, 2)  # box bắt thừa
        rng.shuffle(doan)
        diem, _ = nid_score(list(range(n)), nhan, doan)
        assert 0.0 <= diem <= 1.0


# --- ranh giới N/A (§6) ------------------------------------------------------


def test_khong_khai_BLOCK_BBOX_thi_NA() -> None:
    nhan = [_hang(i) for i in range(3)]
    khong_khai = OcrResult(
        engine="giả", engine_version="0", doc_id="d1", capabilities=frozenset()
    )
    r = NidMetric().score(_gt(*nhan), khong_khai)
    assert r.na_reason is NAReason.MISSING_CAPABILITY


def test_khong_co_nhan_thu_tu_doc_thi_NA_chu_khong_phai_diem_bia() -> None:
    """Ca xảy ra với 100% bộ mẫu hiện tại. Nếu test này đổi thành một con số thì
    ai đó đã chế nhãn bằng sắp hình học — đọc `AnnotationGT.reading_order` trước."""
    nhan = [_hang(i) for i in range(3)]
    gt = AnnotationGT(
        doc_id="d1",
        blocks=tuple(OcrBlock(block_type=BlockType.TEXT, box=b) for b in nhan),
    )
    assert gt.reading_order == ()
    r = NidMetric().score(gt, _kq(*nhan))
    assert r.na_reason is NAReason.NO_GROUND_TRUTH


def test_duoi_2_block_thi_NA() -> None:
    h = _hang(0)
    r = NidMetric().score(_gt(h), _kq(h))
    assert r.na_reason is NAReason.NO_GROUND_TRUTH


def test_khai_BLOCK_BBOX_ma_khong_tra_block_nao_thi_0_khong_phai_NA() -> None:
    """Tiền lệ B3: khai năng lực rồi mà không trả gì là lỗi engine."""
    nhan = [_hang(i) for i in range(3)]
    r = NidMetric().score(_gt(*nhan), _kq())
    assert r.na_reason is None and r.value == 0.0


def test_sai_kieu_ground_truth_thi_NA() -> None:
    r = NidMetric().score(AssertionGT(doc_id="d1"), _kq(_hang(0), _hang(1)))
    assert r.na_reason is NAReason.WRONG_GT_KIND


# --- đường đi có nhãn: chỉ chạy được khi nhãn được đắp tay ---------------------


def test_co_nhan_thu_tu_thi_cham_that_qua_ca_lop_Metric() -> None:
    """Mọi test `NidMetric` khác đều dừng ở N/A hoặc ở chốt chặn rỗng, vì bộ mẫu
    thật không có nhãn thứ tự đọc. Không có test này thì thân `_compute` — chỗ nối
    `Metric.score()` với `nid_score()` — chưa từng chạy, và `nid` sẽ nằm im cho tới
    ngày có nhãn rồi hỏng ngay lần đầu dùng thật.
    """
    nhan = [_hang(i) for i in range(4)]
    dung = NidMetric().score(_gt(*nhan), _kq(*nhan))
    assert dung.na_reason is None and dung.value == 1.0
    assert dung.detail["n_nhan"] == 4

    dao = NidMetric().score(_gt(*nhan), _kq(nhan[0], nhan[2], nhan[1], nhan[3]))
    assert dao.value is not None and dao.value < 1.0


def test_nhan_thu_tu_khac_thu_tu_hinh_hoc() -> None:
    """Nhãn nói đọc từ dưới lên. Engine đọc từ trên xuống phải TỤT — nếu nó vẫn 1.0
    thì `reading_order` đang bị bỏ qua và metric đo hình học chứ không đo nhãn.
    """
    nhan = [_hang(i) for i in range(4)]
    gt = _gt(*nhan, thu_tu=(3, 2, 1, 0))
    r = NidMetric().score(gt, _kq(*nhan))
    assert r.value is not None and r.value < 1.0
    nguoc = NidMetric().score(gt, _kq(*reversed(nhan)))
    assert nguoc.value == 1.0


# --- AC-04 -------------------------------------------------------------------


def test_bang_doi_chieu_muon_va_khac_o_dang_du_lieu() -> None:
    """AC-04 đòi ghi rõ mượn gì / khác gì. Để ở dạng dữ liệu chứ không chỉ trong
    văn xuôi để giai đoạn D trích ra được và test khoá được."""
    assert set(MUON_VA_KHAC) == {
        "y_tuong_goc",
        "chuan_hoa",
        "don_vi_chuoi",
        "ghep_cap",
        "do_min",
        "thieu_nhan",
    }
    khac = [v for v in MUON_VA_KHAC.values() if "KHÁC" in v]
    assert len(khac) == 4
