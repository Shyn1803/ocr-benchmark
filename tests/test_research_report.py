"""Test deterministic publication build pipeline and byte-identical output contract."""

from __future__ import annotations

from pathlib import Path
import pytest

from ocr_bench.research_report import (
    build_publication,
    moc_tat_dinh,
    validate_publication_trace,
)

FIXED_TS = "2026-08-12T00:00:00+07:00"


def test_moc_uu_tien_tham_so_roi_den_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1786060800")
    assert moc_tat_dinh(FIXED_TS) == FIXED_TS
    assert moc_tat_dinh() == "2026-08-07T00:00:00Z"


def test_moc_khong_co_env_thi_dung_dong_ho_may(monkeypatch: pytest.MonkeyPatch):
    """Không có env thì vẫn chạy được — chỉ là mất tính tái lập, và đó là lựa chọn."""
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    assert moc_tat_dinh().startswith("20")


def test_report_build_emits_all_required_artifacts(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    out_dir = tmp_path / "out"

    files = build_publication(input_dir, out_dir, generated_at=FIXED_TS)

    required = {
        "paper/paper-vi.md",
        "paper/executive-summary.md",
        "results/raw-results.json",
        "results/aggregate-results.json",
        "results/statistical-tests.json",
        "tables/overall.md",
        "tables/common-set.md",
        "tables/by-group.md",
        "figures/capability-ranking.svg",
        "figures/accuracy-speed.svg",
        "figures/scan-degradation.svg",
        "figures/failure-distribution.svg",
    }
    assert required <= set(files.keys())


def test_report_build_is_byte_identical_across_two_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Dựng hai lần **bằng lệnh mặc định** phải ra byte giống hệt nhau.

    Cố ý *không* truyền `generated_at`: bản trước chỉ tất định khi người gọi tự chốt
    mốc thời gian, còn `scripts/build_research_report.py` thì không truyền gì cả —
    nên đường đi thật sự được dùng chưa từng được kiểm.
    """
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1786060800")
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    out_a = tmp_path / "out_a"
    out_b = tmp_path / "out_b"

    files_a = build_publication(input_dir, out_a)
    files_b = build_publication(input_dir, out_b)

    for rel_path in files_a:
        path_a = files_a[rel_path]
        path_b = files_b[rel_path]

        assert path_a.read_bytes() == path_b.read_bytes(), f"Mismatch in {rel_path}"


def test_prediction_dir_thuc_su_di_toi_cham_diem(monkeypatch: pytest.MonkeyPatch):
    """`prediction_dir` phải tới được `load_predictions`, không bị nuốt dọc đường.

    Chết khi revert: bản trước `_cham()` chốt cứng `ROOT / "prediction"`, nên chạy pilot
    xong rồi dựng báo cáo vẫn ra bảng của corpus đóng băng mà không báo gì.
    """
    from ocr_bench import research_report as R

    thay: list[Path] = []
    monkeypatch.setattr(R, "load_predictions", lambda p: thay.append(Path(p)) or [])
    monkeypatch.setattr(R, "load_doclaynet", dict)
    monkeypatch.setattr(R, "load_olmocr", dict)

    R._cham(Path("calibration/prediction/cpu"))
    assert thay == [Path("calibration/prediction/cpu")]

    thay.clear()
    R._cham()
    assert thay == [R.THU_MUC_PREDICTION_MAC_DINH]


def test_cli_chuyen_tiep_prediction_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Cờ `--prediction-dir` phải xuống tới `build_publication`."""
    import importlib.util

    from ocr_bench.research_report import ROOT as GOC

    spec = importlib.util.spec_from_file_location(
        "build_report_cli", GOC / "scripts" / "build_research_report.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    ghi: dict = {}
    monkeypatch.setattr(
        mod, "build_publication", lambda i, o, **kw: ghi.update(kw) or {}
    )
    monkeypatch.setattr(mod, "validate_publication_trace", lambda _o: [])

    assert mod.main(["--prediction-dir", str(tmp_path), "--out", str(tmp_path)]) == 0
    assert ghi["prediction_dir"] == tmp_path

    ghi.clear()
    assert mod.main(["--out", str(tmp_path)]) == 0
    assert ghi["prediction_dir"] is None


def test_every_number_in_paper_has_trace_id(tmp_path: Path):
    out_dir = tmp_path / "out"
    build_publication(tmp_path, out_dir, generated_at=FIXED_TS)
    errors = validate_publication_trace(out_dir)
    assert errors == []
