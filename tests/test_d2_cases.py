"""Test phân tầng của `scripts/d2_cases.py` — D2 (TASK-088).

Chỉ phần *phân tầng*. Đây là chỗ chứa quy tắc chọn mẫu: một ca rơi nhầm tầng thì nó
được đọc tay để trả lời câu hỏi chẩn đoán **khác** với câu hỏi nó thật sự trả lời được,
và kết luận trong `results/failure-analysis.md` sai mà không có tín hiệu nào.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from ocr_bench.types import MetricResult, NAReason

ROOT = Path(__file__).resolve().parents[1]


def _nap():
    duong = ROOT / "scripts" / "d2_cases.py"
    spec = importlib.util.spec_from_file_location("_d2c", duong)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_d2c"] = mod
    spec.loader.exec_module(mod)
    return mod


d2 = _nap()


def _r(metric, value, *, engine="e", doc_id="d", detail=None, na=None):
    return MetricResult(
        metric=metric, engine=engine, doc_id=doc_id, value=value, na_reason=na, detail=detail
    )


def test_tong_so_ca_cua_ke_hoach_bang_dung_20():
    """`TANG` và `TONG` khai hai lần cùng một con số — lệch nhau thì script vẫn chạy
    và trả về số ca khác 20 mà chỉ báo ở dòng cuối."""
    assert sum(n for _, n in d2.TANG) == d2.TONG == 20


def test_crash_dem_theo_tai_lieu_khong_theo_metric():
    """Một crash làm hỏng cả 14 metric của cùng tài liệu. Đếm theo metric thì 5 ca
    crash chiếm hết chỗ của 4 tầng còn lại."""
    rows = [
        _r(m, None, na=NAReason.ENGINE_FAILED)
        for m in ("img_f1", "img_iou", "heading", "nid")
    ]
    ho = d2._phan_tang(rows)
    assert len(ho["crash"]) == 1
    assert ho["crash"][0]["metric"] == "*"


def test_img_f1_zero_chia_ba_tang_theo_nhan_va_doan():
    rows = [
        _r("img_f1", 0.0, doc_id="a", detail={"n_nhan": 2, "n_doan": 0}),
        _r("img_f1", 0.0, doc_id="b", detail={"n_nhan": 0, "n_doan": 1}),
        _r("img_f1", 0.0, doc_id="c", detail={"n_nhan": 1, "n_doan": 1}),
    ]
    ho = d2._phan_tang(rows)
    assert [c["doc_id"] for c in ho["img_bo_sot"]] == ["a"]
    assert [c["doc_id"] for c in ho["img_duong_tinh_gia"]] == ["b"]
    assert [c["doc_id"] for c in ho["img_lech_khung"]] == ["c"]


def test_ca_khong_zero_khong_vao_tang_nao():
    """Tầng là danh sách ca *hỏng*. Lọt một ca điểm dương vào là 1/20 suất đọc tay
    tiêu vào một ca không có gì để chẩn đoán."""
    rows = [_r("img_f1", 0.4, detail={"n_nhan": 1, "n_doan": 1}), _r("heading", 1.0)]
    assert all(not v for v in d2._phan_tang(rows).values())


def test_assertion_metric_khong_lay_ca_nao():
    """40 ca zero của `assert_math_presence` (noop + sabotage) là hành vi đúng thiết kế
    của hai engine giả — loại có khai báo (xem comment trong `_phan_tang`)."""
    rows = [_r("assert_math_presence", 0.0, engine="sabotage")]
    assert all(not v for v in d2._phan_tang(rows).values())


def test_moi_tang_sap_xep_tat_dinh():
    """Script chọn `[:n]` từ mỗi tầng. Thứ tự phụ thuộc thứ tự nạp file thì bộ 20 ca
    đổi giữa hai lần chạy, và `results/d2-cases.json` đã commit không tái lập được."""
    detail = {"n_nhan": 1, "n_doan": 1}
    xuoi = [
        _r("img_f1", 0.0, engine="b", doc_id="z", detail=detail),
        _r("img_f1", 0.0, engine="a", doc_id="y", detail=detail),
        _r("img_f1", 0.0, engine="a", doc_id="x", detail=detail),
    ]
    khoa = lambda ho: [(c["engine"], c["doc_id"]) for c in ho["img_lech_khung"]]  # noqa: E731
    assert khoa(d2._phan_tang(xuoi)) == [("a", "x"), ("a", "y"), ("b", "z")]
    assert khoa(d2._phan_tang(list(reversed(xuoi)))) == khoa(d2._phan_tang(xuoi))
