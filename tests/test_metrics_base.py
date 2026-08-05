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
    r = AlwaysOne().score(GT, _result(failed=True, error="boom"))
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


def _rows(values, na=(), failed=0) -> list[MetricResult]:
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
