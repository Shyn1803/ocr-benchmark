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
        "results/measurable-ceiling.json",
        "tables/ceiling.md",
        # Chú giải là artifact bắt buộc, không phải phụ lục tuỳ hứng: mọi bảng khác
        # đều trỏ tới nó để giải thích `n` / `N/A` / `trần` / `†` / `‡`.
        "tables/glossary.md",
        "tables/overall.md",
        "tables/common-set.md",
        "tables/by-group.md",
        # Hình xếp hạng và hình scan tách theo **nửa corpus**: một hình phẳng gộp cả
        # hai nửa là mời so hai bộ mẫu giao nhau bằng 0.
        "figures/capability-ranking-doclaynet.svg",
        "figures/capability-ranking-olmocr.svg",
        "figures/scan-degradation-doclaynet.svg",
        "figures/scan-degradation-olmocr.svg",
        "figures/accuracy-speed.svg",
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


def test_khong_bang_nao_tron_metric_cua_hai_nua_corpus(tmp_path: Path):
    """Một bảng markdown chỉ được chứa metric của **một** nửa bộ mẫu.

    Hai nửa giao nhau bằng 0: DocLayNet mang nhãn bbox, olmOCR mang nhãn khẳng định.
    Xếp `block_f1` (trần 203) cạnh `assert_math_presence` (trần 558) trong cùng một
    bảng là mời người đọc so hai con số đến từ hai tập tài liệu không chung tài liệu
    nào — và không gì trong bảng nói ra điều đó. Đây là cổng chặn cho đúng cái đó,
    quét trên **file đã sinh** chứ không trên ý định của hàm sinh.
    """
    from ocr_bench.ceiling import tran_do_duoc
    from ocr_bench.corpus import load_doclaynet, load_olmocr

    out_dir = tmp_path / "out"
    build_publication(tmp_path, out_dir, generated_at=FIXED_TS)

    nua_cua = {
        m: t.nua_corpus for m, t in tran_do_duoc(load_doclaynet(), load_olmocr()).items()
    }

    for md in sorted((out_dir / "tables").glob("*.md")):
        bang_hien_tai: set[str] = set()
        tu_khai_nua = False
        """Bảng có sẵn cột `nửa corpus` thì mỗi hàng tự nói mình thuộc nửa nào.

        `ceiling.md` là bảng như vậy — nó là **danh mục trần đo được**, không phải bảng
        so điểm, và bỏ nửa kia ra khỏi danh mục thì đúng là giấu. Luật cấm trộn nhắm
        vào bảng đặt hai con số cạnh nhau mà không nói chúng đến từ hai tập rời nhau;
        một cột ghi rõ nửa corpus chính là lời nói đó.
        """
        for dong in md.read_text(encoding="utf-8").splitlines() + [""]:
            if not dong.startswith("|"):
                # Hết một bảng: kiểm rồi mở bảng mới.
                assert tu_khai_nua or len(bang_hien_tai) <= 1, (
                    f"{md.name}: một bảng chứa metric của cả hai nửa corpus "
                    f"({', '.join(sorted(bang_hien_tai))})"
                )
                bang_hien_tai = set()
                tu_khai_nua = False
                continue
            if not bang_hien_tai and "nửa corpus" in dong:
                tu_khai_nua = True
            # Cột đầu là tên metric, có thể mang hậu tố `†` (metric ngược chiều).
            ten = dong.split("|")[1].strip().removesuffix("†").strip().strip("*`")
            if ten in nua_cua and nua_cua[ten] != "ca_hai":
                bang_hien_tai.add(nua_cua[ten])


def test_moi_metric_deu_co_mo_ta():
    """Metric mới thêm vào sổ đăng ký mà quên docstring thì đỏ ở đây, không im lặng.

    `glossary.mo_ta_metric` lấy **câu đầu** docstring của lớp metric. Không có docstring
    thì bảng chú giải in `—` — một dòng trống giữa các dòng có nghĩa, và không gì trong
    lượt dựng báo cho ai biết. Đây là chỗ báo.
    """
    from ocr_bench import glossary, registry

    thieu = [m for m in registry.list_metrics() if not glossary.mo_ta_metric(m)]
    assert thieu == [], f"metric không có docstring mô tả: {', '.join(thieu)}"


def test_truc_y_chon_metric_tach_engine_xa_nhat_khong_phai_tran_lon_nhat():
    """Trục `accuracy-speed` chọn theo **độ trải**, không theo trần.

    Chết khi revert: bản trước lấy metric đầu `thu_tu_metric` — tức trần lớn nhất — và
    ở lượt chạy thật nó rơi vào `assert_math_presence`, nơi ba engine đều 0.001–0.002.
    Hình ra ba điểm bẹp trên đáy. Ở đây `to_tran` có trần gấp đôi nhưng mọi engine bằng
    nhau; `nho_tran` mới là metric nói được điều gì đó.
    """
    from ocr_bench.ceiling import Tran
    from ocr_bench.research_report import _chon_truc_y
    from ocr_bench.scorer import ScoreTable
    from ocr_bench.types import MetricResult

    docs = ("d1", "d2")
    rows = [
        MetricResult(metric=m, engine=e, doc_id=d, value=v)
        for d in docs
        for m, e, v in (
            ("to_tran", "a_default", 0.50),
            ("to_tran", "b_default", 0.50),
            ("nho_tran", "a_default", 0.90),
            ("nho_tran", "b_default", 0.20),
        )
    ]
    trans = {
        m: Tran(
            metric=m,
            nua_corpus="doclaynet",
            n_ung_vien=400,
            n_toi_da=n,
            bac="do_duoc",
            ly_do="",
            nang_luc_can=(),
        )
        for m, n in (("to_tran", 400), ("nho_tran", 200))
    }
    docs_nua = {"doclaynet": frozenset(docs), "olmocr": frozenset()}

    assert _chon_truc_y(ScoreTable(tuple(rows)), trans, docs_nua) == "nho_tran"


def test_every_number_in_paper_has_trace_id(tmp_path: Path):
    out_dir = tmp_path / "out"
    build_publication(tmp_path, out_dir, generated_at=FIXED_TS)
    errors = validate_publication_trace(out_dir)
    assert errors == []
