"""B3 — ImgF1 / ImgIou (TASK-081).

Không `importorskip`: `imgf1.py` chỉ dùng số học của `Box`, không phụ thuộc extra
nào. Đây là metric đầu tiên chạy được trên máy trắng không cần cài gì thêm.
"""

from __future__ import annotations

import itertools
import random

import pytest

from ocr_bench.metrics.imgf1 import (
    ImgF1Metric,
    ImgIouMetric,
    ghep_cap,
    img_scores,
)
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Box,
    Capability,
    FailureKind,
    NAReason,
    OcrImage,
    OcrResult,
)


def _b(x0: float, y0: float, x1: float, y1: float, page: int = 0) -> Box:
    return Box(x0=x0, y0=y0, x1=x1, y1=y1, page=page)


def _kq(*boxes: Box | None, caps: frozenset[Capability] | None = None) -> OcrResult:
    return OcrResult(
        engine="giả",
        engine_version="0",
        doc_id="d1",
        capabilities=frozenset({Capability.IMAGE_BBOX}) if caps is None else caps,
        images=tuple(OcrImage(box=b) for b in boxes),
    )


def _gt(*boxes: Box) -> AnnotationGT:
    return AnnotationGT(doc_id="d1", images=tuple(boxes))


# --- ghép cặp ----------------------------------------------------------------


def test_trung_khit_thi_f1_va_iou_deu_1() -> None:
    a = [_b(0.1, 0.1, 0.4, 0.4), _b(0.5, 0.5, 0.9, 0.9)]
    f1, iou, ct = img_scores(a, list(a))
    assert f1 == 1.0 and iou == 1.0
    assert (ct["tp"], ct["fp"], ct["fn"]) == (2, 0, 0)


def test_duoi_nguong_thi_khong_phai_la_cap() -> None:
    """Chồng nhau một tí không phải là "tìm thấy ảnh" — nếu không thì engine
    phun một box to trùm cả trang sẽ khớp mọi ảnh."""
    nhan = [_b(0.0, 0.0, 0.2, 0.2)]
    doan = [_b(0.15, 0.15, 0.9, 0.9)]
    assert nhan[0].iou(doan[0]) < 0.5
    f1, iou, ct = img_scores(nhan, doan)
    assert f1 == 0.0 and iou == 0.0
    assert (ct["tp"], ct["fp"], ct["fn"]) == (0, 1, 1)


def test_f1_cao_ma_iou_thap_moi_la_ly_do_co_hai_cot() -> None:
    """Đếm đúng ảnh nhưng khung lệch. Gộp một cột là mất đúng chẩn đoán này."""
    nhan = [_b(0.0, 0.0, 0.5, 0.5)]
    doan = [_b(0.05, 0.05, 0.6, 0.6)]
    f1, iou, _ = img_scores(nhan, doan)
    assert f1 == 1.0
    assert 0.5 < iou < 0.8


def test_box_thua_bi_tinh_vao_mau_so_cua_iou() -> None:
    """Không lấy trung bình IoU của riêng cặp khớp: engine chỉ xuất một ảnh nó
    tự tin sẽ được 1.0, đúng kiểu thưởng nhầm repo này tồn tại để chặn."""
    nhan = [_b(0.0, 0.0, 0.3, 0.3)]
    doan = [_b(0.0, 0.0, 0.3, 0.3), _b(0.6, 0.6, 0.9, 0.9), _b(0.6, 0.0, 0.9, 0.3)]
    f1, iou, ct = img_scores(nhan, doan)
    assert ct["tp"] == 1 and ct["fp"] == 2 and ct["fn"] == 0
    assert iou == pytest.approx(1 / 3)  # 1.0 / (1 + 2 + 0)
    assert f1 == pytest.approx(0.5)


def test_precision_va_recall_bao_rieng() -> None:
    """319 box của opendataloader so với 121 nhãn là thừa hay thiếu — F1 gộp lại
    thì không đọc ra được."""
    nhan = [_b(0.0, 0.0, 0.2, 0.2), _b(0.5, 0.5, 0.7, 0.7)]
    doan = [_b(0.0, 0.0, 0.2, 0.2), _b(0.8, 0.8, 0.95, 0.95)]
    _, _, ct = img_scores(nhan, doan)
    assert ct["precision"] == pytest.approx(0.5)
    assert ct["recall"] == pytest.approx(0.5)


def test_khac_trang_khong_bao_gio_ghep() -> None:
    """DocLayNet 1 trang/tài liệu nên chưa lộ ra, nhưng olmOCR thì nhiều trang."""
    assert ghep_cap([_b(0.1, 0.1, 0.9, 0.9, page=0)],
                    [_b(0.1, 0.1, 0.9, 0.9, page=1)]) == []


def test_ghep_tham_lam_bang_ghep_vet_can_o_nguong_05() -> None:
    """Khẳng định của quyết định 1, kiểm bằng máy chứ không bằng lời: ở IoU > 0.5
    phép ghép là duy nhất nên tham lam = tối ưu."""
    r = random.Random(20260806)
    for _ in range(300):
        nhan = [_box_ngau_nhien(r) for _ in range(r.randint(1, 4))]
        doan = [_box_ngau_nhien(r) for _ in range(r.randint(1, 4))]
        tham_lam = sum(c[2] for c in ghep_cap(nhan, doan))
        assert tham_lam == pytest.approx(_vet_can(nhan, doan), abs=1e-12)


def _box_ngau_nhien(r: random.Random) -> Box:
    x0 = r.uniform(0.0, 0.8)
    y0 = r.uniform(0.0, 0.8)
    return _b(x0, y0, x0 + r.uniform(0.05, 0.2), y0 + r.uniform(0.05, 0.2))


def _vet_can(nhan: list[Box], doan: list[Box]) -> float:
    """Tổng IoU lớn nhất trên MỌI phép ghép hợp lệ (chỉ dùng trong test)."""
    tot = 0.0
    k = min(len(nhan), len(doan))
    for chon_n in itertools.combinations(range(len(nhan)), k):
        for hoan_vi in itertools.permutations(range(len(doan)), k):
            s = 0.0
            for i, j in zip(chon_n, hoan_vi):
                iou = nhan[i].iou(doan[j])
                if iou >= 0.5:
                    s += iou
            tot = max(tot, s)
    return tot


def test_mot_box_doan_tranh_chap_hai_nhan_thi_chi_duoc_ghep_mot_lan() -> None:
    """Tính duy nhất ở IoU > 0.5 chỉ đúng khi hai box nhãn RỜI nhau — docstring
    `ghep_cap` nói đúng thế. Nhãn chồng nhau thì tranh chấp là có thật, và box
    đoán phải được dùng đúng một lần, không ghép hai."""
    nhan = [_b(0.0, 0.0, 0.30, 0.30), _b(0.01, 0.01, 0.31, 0.31)]
    doan = [_b(0.0, 0.0, 0.30, 0.30)]
    assert nhan[1].iou(doan[0]) > 0.5  # cặp thứ hai CŨNG qua ngưỡng
    cap = ghep_cap(nhan, doan)
    assert cap == [(0, 0, 1.0)]  # nhưng chỉ một cặp được lấy
    _, _, ct = img_scores(nhan, doan)
    assert (ct["tp"], ct["fp"], ct["fn"]) == (1, 0, 1)


def test_ghep_cap_on_dinh_khi_iou_bang_nhau() -> None:
    """Hai cặp cùng IoU không được đổi thứ tự theo tâm trạng của `sort` —
    `detail` bị so trong test và trong lịch sử kết quả ở giai đoạn D."""
    nhan = [_b(0.0, 0.0, 0.2, 0.2), _b(0.5, 0.0, 0.7, 0.2)]
    doan = [_b(0.5, 0.0, 0.7, 0.2), _b(0.0, 0.0, 0.2, 0.2)]
    assert ghep_cap(nhan, doan) == [(0, 1, 1.0), (1, 0, 1.0)]


# --- AC-02: hai trục y ---------------------------------------------------------


def test_hai_truc_y_cung_mot_vung_thi_iou_1() -> None:
    """AC-02, và là bẫy đắt nhất của B3: trộn nhầm hệ toạ độ cho IoU thấp trông
    Y HỆT "engine tách ảnh kém". Không có test này thì không phân biệt được."""
    W, H = 612.0, 792.0
    # Cùng một vùng vật lý: cách mép trên 100pt, cao 200pt.
    tren = _tu_tuyet_doi(50.0, 100.0, 350.0, 300.0, W, H, "down")
    duoi = _tu_tuyet_doi(50.0, H - 300.0, 350.0, H - 100.0, W, H, "up")
    assert tren.iou(duoi) == pytest.approx(1.0)
    assert img_scores([tren], [duoi])[0] == 1.0


def _tu_tuyet_doi(
    x0: float, y0: float, x1: float, y1: float, w: float, h: float, truc: str
) -> Box:
    return Box.from_absolute(
        page=0, x0=x0, y0=y0, x1=x1, y1=y1,
        page_width=w, page_height=h, y_axis=truc,  # type: ignore[arg-type]
    )


def test_lat_truc_y_nham_thi_iou_TUT_chu_khong_phai_van_1() -> None:
    """Vế đối: nếu `from_absolute` bỏ qua `y_axis` thì test trên vẫn xanh một
    cách vô nghĩa. Vùng lệch tâm phải KHÁC nhau khi hiểu sai trục."""
    W, H = 612.0, 792.0
    dung = _tu_tuyet_doi(50.0, 100.0, 350.0, 300.0, W, H, "down")
    sai = _tu_tuyet_doi(50.0, 100.0, 350.0, 300.0, W, H, "up")
    assert dung.iou(sai) < 0.5


# --- AC-04: bốn ranh giới ------------------------------------------------------


def test_khong_khai_image_bbox_thi_na_chu_khong_phai_0() -> None:
    kq = _kq(caps=frozenset({Capability.TEXT_MD}))
    r = ImgF1Metric().score(_gt(_b(0.1, 0.1, 0.3, 0.3)), kq)
    assert r.value is None and r.na_reason is NAReason.MISSING_CAPABILITY


def test_khai_image_bbox_nhung_khong_tra_box_nao_thi_cham_0() -> None:
    """AC-04 nói thẳng "ra điểm thật". Khai khống không được hưởng N/A —
    N/A không vào mẫu số phạt của `penalized_mean`."""
    r = ImgF1Metric().score(_gt(_b(0.1, 0.1, 0.3, 0.3)), _kq())
    assert r.value == 0.0 and r.na_reason is None


def test_nhan_khong_anh_va_engine_cung_khong_thi_na() -> None:
    """141/204 tài liệu DocLayNet rơi vào đây. Chấm 1.0 là rót điểm miễn phí
    vào 69% bảng và chôn mất chênh lệch ở 63 tài liệu còn lại."""
    r = ImgF1Metric().score(_gt(), _kq())
    assert r.value is None and r.na_reason is NAReason.NO_GROUND_TRUTH


def test_nhan_khong_anh_ma_engine_doan_co_thi_0_chu_khong_na() -> None:
    """Cùng nhãn rỗng, khác kết quả — và đó là chủ ý. Dương tính giả là lỗi thật."""
    r = ImgF1Metric().score(_gt(), _kq(_b(0.1, 0.1, 0.3, 0.3)))
    assert r.value == 0.0 and r.na_reason is None
    assert r.detail["fp"] == 1


def test_anh_khong_co_khung_thi_khong_ghep_duoc() -> None:
    """`OcrImage.box` được phép None (có bytes ảnh, không có toạ độ)."""
    r = ImgF1Metric().score(_gt(_b(0.1, 0.1, 0.3, 0.3)), _kq(None, None))
    assert r.value == 0.0 and r.detail["n_doan"] == 0


def test_sai_loai_nhan_thi_wrong_gt_kind() -> None:
    r = ImgF1Metric().score(AssertionGT(doc_id="d1"), _kq(_b(0.1, 0.1, 0.3, 0.3)))
    assert r.value is None and r.na_reason is NAReason.WRONG_GT_KIND


def test_engine_hong_thi_engine_failed() -> None:
    kq = OcrResult(
        engine="giả", engine_version="0", doc_id="d1",
        capabilities=frozenset({Capability.IMAGE_BBOX}),
        failed=True, error="hết RAM", failure_kind=FailureKind.OOM,
    )
    r = ImgF1Metric().score(_gt(_b(0.1, 0.1, 0.3, 0.3)), kq)
    assert r.value is None and r.na_reason is NAReason.ENGINE_FAILED


# --- lớp metric ----------------------------------------------------------------


def test_hai_metric_dung_ten_khac_nhau_va_cung_nguong() -> None:
    assert ImgF1Metric.name == "img_f1" and ImgIouMetric.name == "img_iou"
    assert ImgF1Metric.nguong == ImgIouMetric.nguong == 0.5


def test_nguong_nam_trong_detail_chu_khong_chon_trong_code() -> None:
    r = ImgF1Metric().score(_gt(_b(0.1, 0.1, 0.3, 0.3)), _kq(_b(0.1, 0.1, 0.3, 0.3)))
    assert r.detail["nguong"] == 0.5


def test_hai_metric_lay_hai_so_khac_nhau_tu_cung_mot_phep_ghep() -> None:
    gt = _gt(_b(0.0, 0.0, 0.5, 0.5))
    kq = _kq(_b(0.05, 0.05, 0.6, 0.6))
    assert ImgF1Metric().score(gt, kq).value == 1.0
    assert ImgIouMetric().score(gt, kq).value < 0.8


def test_moi_diem_deu_trong_khoang() -> None:
    """`Metric.score()` NÉM khi điểm ngoài [0,1]."""
    r = random.Random(7)
    for _ in range(200):
        gt = _gt(*[_box_ngau_nhien(r) for _ in range(r.randint(1, 3))])
        kq = _kq(*[_box_ngau_nhien(r) for _ in range(r.randint(0, 3))])
        for m in (ImgF1Metric(), ImgIouMetric()):
            v = m.score(gt, kq).value
            assert v is not None and 0.0 <= v <= 1.0


# --- AC-03: Picture vs Figure, giải ở tầng adapter -----------------------------


def test_bon_ten_anh_cua_marker_deu_ve_mot_block_type() -> None:
    """AC-03. Marker phân biệt `Picture` với `Figure`; bench thì không, và chỗ
    quy về một mối là ADAPTER chứ không phải metric — docstring `BlockType` chốt
    "metric không được biết những tên đó tồn tại". Test đặt ở đây vì đây là chỗ
    quyết định đó có hệ quả: `imgf1.py` chỉ đọc `images`, không đọc tên nhãn."""
    from ocr_bench.adapters.marker import IMAGE_BLOCK_TYPES, BLOCK_TYPE_MAP
    from ocr_bench.types import BlockType

    assert IMAGE_BLOCK_TYPES == {"Picture", "PictureGroup", "Figure", "FigureGroup"}
    assert {BLOCK_TYPE_MAP[t] for t in IMAGE_BLOCK_TYPES} == {BlockType.PICTURE}

    # OpenDataLoader gọi là "image", DocLayNet gọi là "Picture" — cùng đích.
    from ocr_bench.adapters.opendataloader import BLOCK_TYPE_MAP as ODL_MAP
    from ocr_bench.corpus import COCO_BLOCK_TYPE

    assert ODL_MAP["image"] is BlockType.PICTURE
    assert COCO_BLOCK_TYPE["Picture"] is BlockType.PICTURE

    # Và `imgf1.py` không nhắc tới bất kỳ tên nào trong số đó.
    from pathlib import Path

    import ocr_bench.metrics.imgf1 as mod

    nguon = Path(mod.__file__).read_text(encoding="utf-8")
    than = nguon.split('"""', 2)[2]  # bỏ docstring module (nó CÓ giải thích)
    for ten in ("PictureGroup", "FigureGroup", '"image"', "Picture'"):
        assert ten not in than
