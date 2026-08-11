"""Test cổng N/A và quy tắc tổng hợp.

Đây là chỗ chặn lỗi của `opendataloader-bench`: loại tài liệu hỏng ra khỏi trung
bình tức là **thưởng cho engine hỏng nhiều hơn**.
"""

from __future__ import annotations

import pytest

from ocr_bench.metrics.base import Aggregate, Metric, aggregate
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Capability,
    FailureKind,
    MetricResult,
    NAReason,
    OcrResult,
)


class AlwaysOne(Metric):
    name = "always_one"
    requires = frozenset({Capability.TEXT_MD})
    gt_kinds = (AnnotationGT,)

    def _compute(self, gt, result):
        return 1.0, {}


class NeedsImages(Metric):
    name = "needs_images"
    requires = frozenset({Capability.IMAGE_BBOX})
    gt_kinds = (AnnotationGT,)

    def _compute(self, gt, result):  # pragma: no cover - không bao giờ được gọi
        raise AssertionError("cổng năng lực đã phải chặn trước khi tới đây")


class OutOfRange(Metric):
    name = "out_of_range"
    requires = frozenset()
    gt_kinds = (AnnotationGT,)

    def _compute(self, gt, result):
        return 1.5, {}


def _result(**kw) -> OcrResult:
    base = dict(
        engine="e",
        engine_version="1",
        doc_id="d",
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md="hi",
    )
    return OcrResult(**{**base, **kw})


GT = AnnotationGT(doc_id="d", text="hi")


def test_thieu_nang_luc_ra_na_chu_khong_ra_0():
    """Cốt lõi. Engine không hứa tách ảnh mà bị chấm 0 điểm tách ảnh thì bảng xếp
    hạng đang so hai thứ khác nhau."""
    r = NeedsImages().score(GT, _result())
    assert r.value is None
    assert r.na_reason is NAReason.MISSING_CAPABILITY
    assert r.detail["missing"] == ["image_bbox"]


def test_engine_hong_ra_na_rieng_mot_loai():
    r = AlwaysOne().score(
        GT,
        _result(
            failed=True,
            error="boom",
            failure_kind=FailureKind.ENGINE_ERROR,
        ),
    )
    assert r.value is None
    assert r.na_reason is NAReason.ENGINE_FAILED


def test_sai_dang_ground_truth_ra_na():
    r = AlwaysOne().score(AssertionGT(doc_id="d"), _result())
    assert r.na_reason is NAReason.WRONG_GT_KIND
    assert r.detail["wants"] == ["AnnotationGT"]


def test_metric_tra_diem_ngoai_khoang_thi_no():
    with pytest.raises(ValueError, match=r"phải nằm trong \[0,1\]"):
        OutOfRange().score(GT, _result())


# --------------------------------------------------------------------------
# Tổng hợp
# --------------------------------------------------------------------------


def _rows(values, na=(), failed=0, chua_nhan=0) -> list[MetricResult]:
    rows = [
        MetricResult(metric="m", engine="e", doc_id=f"d{i}", value=v)
        for i, v in enumerate(values)
    ]
    rows += [
        MetricResult(
            metric="m", engine="e", doc_id=f"f{i}",
            value=None, na_reason=NAReason.ENGINE_FAILED,
        )
        for i in range(failed)
    ]
    rows += [
        MetricResult(
            metric="m", engine="e", doc_id=f"n{i}",
            value=None, na_reason=NAReason.MISSING_CAPABILITY,
        )
        for i in range(len(na))
    ]
    rows += [
        MetricResult(
            metric="m", engine="e", doc_id=f"g{i}",
            value=None, na_reason=NAReason.NO_GROUND_TRUTH,
        )
        for i in range(chua_nhan)
    ]
    return rows


def test_tai_lieu_hong_keo_trung_binh_co_phat_xuong():
    """Engine A chấm được 2 file điểm 1.0 và làm hỏng 2 file.
    Engine B chấm được cả 4 file điểm 1.0. `mean` bằng nhau — đó chính là cái bẫy.
    `penalized_mean` và `fail_rate` phải tách được chúng ra."""
    a = aggregate(_rows([1.0, 1.0], failed=2))
    b = aggregate(_rows([1.0, 1.0, 1.0, 1.0]))

    assert a.mean == b.mean == 1.0
    assert a.penalized_mean == 0.5
    assert b.penalized_mean == 1.0
    assert a.fail_rate == 0.5
    assert b.fail_rate == 0.0


def test_na_vi_thieu_nang_luc_khong_lam_loang_trung_binh():
    """Khác với hỏng: engine không hứa làm việc đó thì không bị phạt ở cột điểm —
    nó bị đánh dấu N/A ở ô riêng."""
    agg = aggregate(_rows([1.0, 0.5], na=("x", "y", "z")))
    assert agg.n_na == 3
    assert agg.n_total == 5
    assert agg.mean == pytest.approx(0.75)
    assert agg.penalized_mean == pytest.approx(0.75)
    assert agg.fail_rate == 0.0


def test_toan_bo_na_thi_applicable_false():
    agg = aggregate(_rows([], na=("x", "y")))
    assert agg.applicable is False
    assert agg.penalized_mean is None
    assert agg.cell() == "N/A"


def test_o_bang_luon_kem_ti_le_hong():
    """Không thể in trung bình mà quên FailRate — chúng nằm trong cùng một ô."""
    assert aggregate(_rows([1.0, 1.0], failed=2)).cell() == "0.500 (fail 50%)"


def test_hong_het_thi_o_khong_in_0_000():
    """Hỏng hết ⇒ `penalized_mean` = 0/N = 0.0, nhưng đó **không phải một trung
    bình** — không tài liệu nào được chấm. In "0.000 (fail 100%)" là nói engine
    *đo được và tệ nhất*, trong khi sự thật là nó *chưa từng được đo*.

    Đây là cùng một tiêu chí (`n_scored == 0`) mà `do_phan_tan()` và
    `kiem_sabotage()` đã dùng để từ chối kết luận.
    """
    agg = aggregate(_rows([], failed=10))
    assert agg.applicable is True          # có mẫu số ⇒ dòng vẫn phải hiện
    assert agg.penalized_mean == 0.0       # con số 0.0 vẫn có, chỉ không được in ra
    assert agg.n_scored == 0
    o = agg.cell()
    assert "0.000" not in o
    assert o == "— (10 hỏng, 0 chấm được)"


def test_vai_tai_lieu_hong_khong_bat_applicable_cho_metric_thieu_nang_luc():
    """Ca hồi quy. Tài liệu hỏng ở cấp engine sinh `ENGINE_FAILED` cho **mọi** metric,
    kể cả metric engine không có năng lực chạm tới. Lấy `denom > 0` làm `applicable`
    thì 10 tài liệu hỏng bật sáng cả 14 metric, bảng in "— (10 hỏng, 0 chấm được)" ở
    mọi ô, và 194 tài liệu chạy tốt biến mất khỏi báo cáo.

    Đúng: 194 tài liệu N/A vì thiếu năng lực ⇒ metric này **không áp dụng**, bất kể
    có bao nhiêu tài liệu hỏng bên cạnh.
    """
    agg = aggregate(_rows([], na=tuple(range(194)), failed=10))
    assert agg.n_thieu_nang_luc == 194
    assert agg.applicable is False
    assert agg.cell() == "N/A"


def test_thieu_nhan_khac_thieu_nang_luc():
    """Engine **có** năng lực, bộ mẫu chưa có nhãn hợp loại. In `N/A` ở đây là đổ lỗi
    cho engine vì thiếu sót của bộ mẫu — hai chuyện khác hẳn nhau khi quyết định phải
    đi bổ sung nhãn hay đi đổi engine."""
    agg = aggregate(_rows([], chua_nhan=204))
    assert agg.n_chua_nhan == 204
    assert agg.n_thieu_nang_luc == 0
    assert agg.applicable is True
    assert agg.penalized_mean is None      # mẫu số rỗng — vẫn không được khẳng định
    assert agg.cell() == "chưa có nhãn (204 tài liệu)"


def test_thieu_nhan_van_uu_tien_hon_bao_hong():
    """Vừa thiếu nhãn vừa có tài liệu hỏng: nói "chưa có nhãn" mới đúng nguyên nhân
    gốc — chấm được hay không là do nhãn, không phải do 10 tài liệu hỏng kia."""
    agg = aggregate(_rows([], chua_nhan=194, failed=10))
    assert agg.cell() == "chưa có nhãn (194 tài liệu)"


def test_diem_thap_that_van_in_binh_thuong():
    """Ca âm: chấm được mà điểm thấp thì vẫn phải in số — nhánh trên không được
    nuốt luôn engine thật sự tệ."""
    agg = aggregate(_rows([0.0, 0.0], failed=2))
    assert agg.n_scored == 2
    assert agg.cell() == "0.000 (fail 50%)"


def test_aggregate_rong():
    agg = aggregate([])
    assert agg == Aggregate(
        metric="", engine="", n_total=0, n_scored=0, n_failed=0, n_na=0,
        mean=None, penalized_mean=None, fail_rate=0.0, applicable=False,
    )


def test_aggregate_tu_choi_tron_lan_engine():
    rows = [
        MetricResult(metric="m", engine="a", doc_id="d", value=1.0),
        MetricResult(metric="m", engine="b", doc_id="d", value=0.0),
    ]
    with pytest.raises(ValueError, match="lẫn metric/engine"):
        aggregate(rows)
