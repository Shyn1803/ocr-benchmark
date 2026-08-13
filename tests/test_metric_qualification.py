"""Test metric qualification gate & controlled sabotage monotonicity."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ocr_bench.metric_qualification import (
    MetricQualificationReport,
    UnknownMetricError,
    qualify_metric,
    qualify_metrics_from_config,
)
from ocr_bench.scorer import MetricResult, ScoreTable
from ocr_bench.types import NAReason

GOC = Path(__file__).resolve().parents[1]


def _bang(diem: dict[str, dict[str, float | None]], metric: str) -> ScoreTable:
    """`{engine: {doc: value}}` → `ScoreTable`. `None` = engine không đo được doc đó."""
    return ScoreTable(
        tuple(
            MetricResult(
                metric=metric,
                engine=e,
                doc_id=d,
                value=v,
                na_reason=None if v is not None else NAReason.MISSING_CAPABILITY,
            )
            for e, docs in diem.items()
            for d, v in docs.items()
        )
    )


def _cfg(tmp_path: Path, metrics: dict[str, dict]) -> Path:
    f = tmp_path / "metric-registry.json"
    f.write_text(json.dumps({"metrics": metrics}), encoding="utf-8")
    return f


# --------------------------------------------------- đối chứng đơn điệu (thuần)


def test_qualify_metric_accepts_monotonic_controls():
    result = qualify_metric(
        metric="good_metric",
        controls={"perfect": 1.0, "partial": 0.7, "severe": 0.3},
        category="main",
    )
    assert result.status == "main"
    assert result.passed_monotonicity is True
    assert len(result.reasons) == 0


def test_qualify_metric_rejects_monotonic_violations():
    result = qualify_metric(
        metric="bad_metric",
        controls={"perfect": 1.0, "partial": 0.4, "severe": 0.6},
        category="main",
    )
    assert result.status == "experimental"
    assert result.passed_monotonicity is False
    assert any("monotonic" in r.lower() for r in result.reasons)


def test_qualify_metric_rejects_non_decreasing_sabotage():
    # When sabotage score is not strictly lower than source score
    result = qualify_metric(
        metric="non_monotonic_sabotage",
        sabotage_score=0.8,
        source_score=0.8,
        category="main",
    )
    assert result.status == "experimental"
    assert result.passed_monotonicity is False
    assert result.sabotage_gate == "failed"
    assert any("sabotage" in r.lower() or "source" in r.lower() for r in result.reasons)


def test_qualify_metrics_from_config(tmp_path: Path):
    """Đường thuần đối chứng: cả hai cổng chắn đều **tắt tường minh**.

    Tắt ở đây là để cô lập phép kiểm đơn điệu. Mặc định của hàm là ngược lại — xem
    `test_gate_not_run_khong_phai_gate_dat`.
    """
    cfg_file = _cfg(
        tmp_path,
        {
            "cer": {"category": "main", "capability": "text_md", "practical_delta": 0.02},
            "bad_metric": {"category": "main", "capability": "text_md", "practical_delta": 0.05},
            "exp_metric": {"category": "experimental", "capability": "layout", "practical_delta": 0.05},
        },
    )

    controls_map = {
        "cer": {"perfect": 1.0, "partial": 0.8, "severe": 0.4},
        "bad_metric": {"perfect": 1.0, "partial": 0.3, "severe": 0.5},
        "exp_metric": {"perfect": 1.0, "partial": 0.5, "severe": 0.2},
    }

    report = qualify_metrics_from_config(
        cfg_file,
        controls_map=controls_map,
        require_sabotage_gate=False,
        validate_against_registry=False,
    )
    assert isinstance(report, MetricQualificationReport)
    assert report.all_main_passed is False
    assert report.results["cer"].status == "main"
    assert report.results["bad_metric"].status == "experimental"
    assert report.results["exp_metric"].status == "experimental"


# ------------------------------------------------------------- cổng fail-closed


def test_gate_not_run_khong_phai_gate_dat(tmp_path: Path):
    """Thiếu `score_table` ⇒ metric `main` bị hạ, KHÔNG được coi là đạt.

    Chết-khi-revert cho lỗ hổng gốc: `scripts/qualify_metrics.py` gọi cổng mà không
    truyền `score_table`, nên phép so D-010 chưa từng chạy mà script vẫn thoát 0.
    """
    cfg_file = _cfg(tmp_path, {"cer": {"category": "main"}})
    report = qualify_metrics_from_config(
        cfg_file,
        score_table=None,
        controls_map={"cer": {"perfect": 1.0, "partial": 0.8, "severe": 0.4}},
        validate_against_registry=False,
    )
    kq = report.results["cer"]
    assert kq.sabotage_gate == "not_run"
    assert kq.status == "experimental"
    assert report.all_main_passed is False
    assert any("did not run" in r for r in kq.reasons)


def test_score_table_that_thi_cong_chay_that(tmp_path: Path):
    """Có `score_table` ⇒ điểm sabotage/nguồn phải xuất hiện trong báo cáo."""
    from ocr_bench.discrimination import NGUON_SABOTAGE

    bang = _bang({NGUON_SABOTAGE: {"a": 0.9, "b": 0.8}, "sabotage": {"a": 0.2, "b": 0.1}}, "cer")
    cfg_file = _cfg(tmp_path, {"cer": {"category": "main"}})

    report = qualify_metrics_from_config(cfg_file, score_table=bang, validate_against_registry=False)
    kq = report.results["cer"]
    assert kq.sabotage_gate == "passed"
    assert kq.sabotage_score is not None and kq.source_score is not None
    assert kq.sabotage_score < kq.source_score
    assert kq.status == "main"


def test_sabotage_bang_diem_nguon_la_truot(tmp_path: Path):
    """Hoà điểm cũng là trượt — D-010 so ngặt (`<`, không phải `<=`)."""
    from ocr_bench.discrimination import NGUON_SABOTAGE

    bang = _bang({NGUON_SABOTAGE: {"a": 0.5, "b": 0.5}, "sabotage": {"a": 0.5, "b": 0.5}}, "cer")
    cfg_file = _cfg(tmp_path, {"cer": {"category": "main"}})

    report = qualify_metrics_from_config(cfg_file, score_table=bang, validate_against_registry=False)
    kq = report.results["cer"]
    assert kq.sabotage_gate == "failed"
    assert kq.status == "experimental"
    assert report.all_main_passed is False


# ------------------------------------------------- phép so ba mức phá hoại


def _bang_phan_muc(
    metric: str,
    *,
    nguon: float,
    s10: float,
    s30: float,
    s60: float,
    sabotage: float = 0.01,
) -> ScoreTable:
    """Bảng đủ cột cho cả cổng một điểm lẫn phép so ba mức."""
    from ocr_bench.discrimination import NGUON_SABOTAGE

    return _bang(
        {
            NGUON_SABOTAGE: {"a": nguon},
            "sabotage": {"a": sabotage},
            "sabotage_s10": {"a": s10},
            "sabotage_s30": {"a": s30},
            "sabotage_s60": {"a": s60},
        },
        metric,
    )


def test_giam_ngat_qua_ba_muc_thi_graded_passed(tmp_path: Path):
    bang = _bang_phan_muc("cer", nguon=0.9, s10=0.7, s30=0.4, s60=0.1)
    cfg_file = _cfg(tmp_path, {"cer": {"category": "main"}})

    kq = qualify_metrics_from_config(
        cfg_file, score_table=bang, validate_against_registry=False
    ).results["cer"]
    assert kq.graded_gate == "passed"
    assert kq.graded_scores is not None and set(kq.graded_scores) >= {"sabotage_s10", "sabotage_s60"}
    assert kq.status == "main"


def test_bao_hoa_khong_ha_hang(tmp_path: Path):
    """Chạm sàn ở mức nhẹ rồi nằm im là quan trắc, không phải lỗi.

    Metric nhị phân bắt buộc bão hoà — hạ hạng vì điều đó là hạ vì một tính chất đúng.
    """
    bang = _bang_phan_muc("cer", nguon=0.9, s10=0.0, s30=0.0, s60=0.0)
    cfg_file = _cfg(tmp_path, {"cer": {"category": "main"}})

    report = qualify_metrics_from_config(
        cfg_file, score_table=bang, validate_against_registry=False
    )
    kq = report.results["cer"]
    assert kq.graded_gate == "saturated"
    assert kq.status == "main"
    assert report.all_main_passed is True


def test_muc_nang_hon_diem_cao_hon_thi_ha_hang(tmp_path: Path):
    """Inversion là lỗi thật: thước đo thưởng cho việc phá nhiều hơn."""
    bang = _bang_phan_muc("cer", nguon=0.9, s10=0.5, s30=0.7, s60=0.2)
    cfg_file = _cfg(tmp_path, {"cer": {"category": "main"}})

    report = qualify_metrics_from_config(
        cfg_file, score_table=bang, validate_against_registry=False
    )
    kq = report.results["cer"]
    assert kq.sabotage_gate == "passed"  # cổng một điểm vẫn qua — chỉ ba mức bắt được
    assert kq.graded_gate == "failed"
    assert kq.passed_monotonicity is False
    assert kq.status == "experimental"
    assert any("Graded sabotage inversion" in r for r in kq.reasons)
    assert report.all_main_passed is False


def test_thieu_cot_phan_muc_thi_not_run_chu_khong_phai_passed(tmp_path: Path):
    from ocr_bench.discrimination import NGUON_SABOTAGE

    bang = _bang({NGUON_SABOTAGE: {"a": 0.9}, "sabotage": {"a": 0.1}}, "cer")
    cfg_file = _cfg(tmp_path, {"cer": {"category": "main"}})

    report = qualify_metrics_from_config(
        cfg_file, score_table=bang, validate_against_registry=False
    )
    kq = report.results["cer"]
    assert kq.graded_gate == "not_run"
    assert kq.graded_note is not None and "dung_sabotage_phan_muc" in kq.graded_note
    assert report.summary["graded_gate"]["not_run"] == 1


def test_tong_ket_dem_du_bon_trang_thai(tmp_path: Path):
    bang = _bang_phan_muc("cer", nguon=0.9, s10=0.7, s30=0.4, s60=0.1)
    cfg_file = _cfg(tmp_path, {"cer": {"category": "main"}})

    summary = qualify_metrics_from_config(
        cfg_file, score_table=bang, validate_against_registry=False
    ).summary
    assert set(summary["graded_gate"]) == {"passed", "saturated", "failed", "not_run"}
    assert sum(summary["graded_gate"].values()) == summary["total_metrics"]


def test_loi_trong_cong_khong_bi_nuot(tmp_path: Path):
    """Cổng ném thì phải ném ra ngoài.

    Bản trước bọc `except Exception: pass`, nên mọi hỏng hóc bên trong biến thành
    "không đo được" và đi tiếp im lặng.
    """
    cfg_file = _cfg(tmp_path, {"cer": {"category": "main"}})

    class BangHong:
        def ranking(self, metric):  # noqa: ARG002
            raise RuntimeError("bảng hỏng")

    with pytest.raises(RuntimeError, match="bảng hỏng"):
        qualify_metrics_from_config(
            cfg_file, score_table=BangHong(), validate_against_registry=False
        )


# ------------------------------------------------- tên metric phải có thật


def test_ten_metric_la_khong_co_that_thi_tu_choi(tmp_path: Path):
    """Tên lệch bộ chấm là cách im lặng nhất để vô hiệu hoá cổng."""
    cfg_file = _cfg(tmp_path, {"khong_ton_tai": {"category": "main"}})
    with pytest.raises(UnknownMetricError, match="khong_ton_tai"):
        qualify_metrics_from_config(cfg_file)


def test_registry_that_khop_voi_bo_cham():
    """`configs/metric-registry.json` chỉ được khai metric mà bộ chấm có thật."""
    from ocr_bench import registry

    cfg = json.loads((GOC / "configs" / "metric-registry.json").read_text(encoding="utf-8"))
    thua = sorted(set(cfg["metrics"]) - set(registry.list_metrics()))
    assert thua == [], f"registry khai metric không có trong bộ chấm: {thua}"


# ------------------------------------------------------------------ CLI


def test_cli_thoat_2_khi_khong_dung_duoc_bang(tmp_path: Path):
    """Không dựng được bảng điểm ⇒ thoát 2, không phải 0."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "qualify_metrics_cli", GOC / "scripts" / "qualify_metrics.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    rc = mod.main(
        ["--prediction-dir", str(tmp_path / "trong-rong"), "--out", str(tmp_path / "ra.json")]
    )
    assert rc == 2


def test_cli_truyen_score_table_vao_cong(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """CLI **phải** truyền `score_table` xuống cổng.

    Đây là test chết-khi-revert đúng chỗ vỡ: bản trước gọi cổng chỉ với
    `controls_map`, và không một test nào bắt được.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "qualify_metrics_cli2", GOC / "scripts" / "qualify_metrics.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    sentinel = object()
    ghi: dict = {}

    monkeypatch.setattr(mod, "build_score_table", lambda _d: sentinel)

    def _gia(config_path, **kw):  # noqa: ANN001
        ghi.update(kw)
        return type(
            "R",
            (),
            {
                "all_main_passed": True,
                "results": {},
                # Stub phải mang đủ cả hai cổng: CLI in cả `graded_gate`, thiếu khoá
                # là `KeyError` chứ không phải "cổng không chạy".
                "summary": {
                    "sabotage_gate": {"passed": 0, "failed": 0, "not_run": 0},
                    "graded_gate": {"passed": 0, "saturated": 0, "failed": 0, "not_run": 0},
                },
                "to_dict": lambda self: {},
            },
        )()

    monkeypatch.setattr(mod, "qualify_metrics_from_config", _gia)

    rc = mod.main(["--out", str(tmp_path / "ra.json")])
    assert rc == 0
    assert ghi["score_table"] is sentinel
    assert ghi["require_sabotage_gate"] is True
