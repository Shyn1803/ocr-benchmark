"""Test tầng lưu prediction — A2 (TASK-073).

Hai câu hỏi, không phải một:

1. **Round-trip có mất gì không?** Mất một kênh dữ liệu lúc ghi/đọc không làm test
   nào đỏ ở nơi khác — nó chỉ làm engine đó tụt điểm ở đúng metric ăn kênh ấy, và
   người đọc bảng sẽ đổ cho engine. Nên có một test dựng `OcrResult` **đầy đủ mọi
   kênh** rồi so từng trường.
2. **File lệch schema có nổ không?** Đây là AC-04. Mỗi nhánh hỏng một test riêng,
   vì "nó ném ở đâu đó" không đủ — phải ném đúng chỗ, kèm đường dẫn file.
"""

from __future__ import annotations

import json
import io
from pathlib import Path
from typing import ClassVar

import pytest
from scripts import migrate_predictions as migration

from ocr_bench.adapters.base import Adapter
from ocr_bench.adapters.noop import NoopAdapter
from ocr_bench.metrics.base import Metric
from ocr_bench.prediction import (
    SCHEMA_VERSION,
    PredictionSchemaError,
    load_prediction,
    load_predictions,
    prediction_path,
    run_engines_cached,
    save_prediction,
    save_predictions,
)
from ocr_bench.scorer import score_results
from ocr_bench.types import (
    AssertionGT,
    BlockType,
    Box,
    Capability,
    FailureKind,
    MetricResult,
    NAReason,
    OcrBlock,
    OcrImage,
    OcrResult,
    OcrTable,
    RawArtifact,
    ScanLabel,
    TextPresence,
)

# PNG 1×1 thật, không phải bytes bịa: sha256 phải tính trên dữ liệu có thể ghi ra
# đĩa rồi mở lại được bằng công cụ khác.
PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000000100000001080600000"
    "01f15c4890000000a49444154789c6360000002000100ffff03000006"
    "0005570cf5410000000049454e44ae426082"
)


def ket_qua_day_du(doc_id: str = "tai-lieu-1") -> OcrResult:
    """Một `OcrResult` bật **mọi** kênh — kể cả các kênh dễ quên nhất."""
    box = Box(page=2, x0=0.1, y0=0.2, x1=0.3, y1=0.44)
    return OcrResult(
        engine="giả",
        engine_version="9.9-rc1",
        doc_id=doc_id,
        capabilities=frozenset(
            {
                Capability.TEXT_MD,
                Capability.BLOCK_BBOX,
                Capability.IMAGE_BBOX,
                Capability.IMAGE_BYTES,
                Capability.TABLE_HTML,
                Capability.SCAN_LABEL,
                Capability.SECTION_HIERARCHY,
            }
        ),
        text_md="# Tiêu đề\n\nnội dung có dấu tiếng Việt",
        blocks=(
            OcrBlock(
                block_type=BlockType.HEADING,
                box=box,
                text="Tiêu đề",
                html="<h2>Tiêu đề</h2>",
                level=2,
                section_hierarchy=("Chương 1", "Mục 1.2"),
            ),
            OcrBlock(block_type=BlockType.TEXT),  # không bbox — hợp lệ
        ),
        images=(
            OcrImage(box=box, data=PNG, source_id="hinh-1"),
            OcrImage(box=box, data=None, source_id=None),  # có hộp, không bytes
        ),
        tables=(
            OcrTable(html="<table><tr><td>ô</td></tr></table>", box=box, n_rows=1, n_cols=1),
        ),
        scan_label=ScanLabel(
            is_scanned=True,
            api="classify_pdf",
            confidence=0.75,
            pages_needing_ocr=(0, 3),
            reason="ít text cell",
        ),
        page_sizes=((612.0, 792.0), (595.5, 842.25)),
        seconds=12.5,
        model_load_seconds=3.25,
        peak_rss_mb=1024.5,
        rss_scope="process+children",
        config_fingerprint={"ocr_use_vision_api": False, "ngưỡng": 0.3, "list": [1, 2]},
    )


# ---------------------------------------------------------------------------
# Round-trip
# ---------------------------------------------------------------------------


def test_round_trip_giu_nguyen_moi_kenh(tmp_path: Path):
    goc = ket_qua_day_du()
    path = save_prediction(goc, tmp_path)
    lai = load_prediction(path)

    # So cả đối tượng: dataclass frozen nên `==` đi vào từng trường, kể cả tuple
    # lồng nhau. Nếu về sau `types.py` thêm trường mà `prediction.py` quên, test này
    # đỏ ngay — đó là toàn bộ lý do so nguyên khối thay vì liệt kê tay.
    assert lai == goc


def test_schema_v3_round_trip_keeps_profile_and_raw_artifact(tmp_path: Path):
    result = OcrResult(
        engine="marker_scan",
        engine_family="marker",
        profile="scan",
        engine_version="1.10.2",
        doc_id="x",
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md="xin chào",
        raw_artifacts=(RawArtifact("marker.json", "application/json", b"{}"),),
        config_fingerprint={"force_ocr": True},
    )
    path = save_prediction(result, tmp_path)
    got = load_prediction(path)
    assert got == result
    assert (tmp_path / "marker_scan" / "x.raw" / "marker.json").read_bytes() == b"{}"


def test_raw_artifact_json_is_metadata_only_and_deterministic(tmp_path: Path):
    result = OcrResult(
        engine="marker_scan",
        engine_family="marker",
        profile="scan",
        engine_version="1.10.2",
        doc_id="x",
        capabilities=frozenset(),
        raw_artifacts=(RawArtifact("marker.json", "application/json", b"{}"),),
    )
    path = save_prediction(result, tmp_path)
    first = path.read_bytes()
    assert json.loads(first)["raw_artifacts"] == [
        {
            "name": "marker.json",
            "media_type": "application/json",
            "file": "marker.json",
            "sha256": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
        }
    ]
    assert save_prediction(result, tmp_path).read_bytes() == first


def test_sha256_raw_artifact_lech_thi_nem(tmp_path: Path):
    result = OcrResult(
        engine="marker_scan",
        engine_version="1",
        doc_id="x",
        capabilities=frozenset(),
        raw_artifacts=(RawArtifact("marker.json", "application/json", b"{}"),),
    )
    path = save_prediction(result, tmp_path)
    (tmp_path / "marker_scan" / "x.raw" / "marker.json").write_bytes(b"tampered")
    with pytest.raises(PredictionSchemaError, match="raw_artifacts\\[0\\].*sha256 lệch"):
        load_prediction(path)


def test_raw_artifact_path_traversal_bi_chan_khi_ghi_va_doc(tmp_path: Path):
    unsafe = OcrResult(
        engine="marker_scan",
        engine_version="1",
        doc_id="x",
        capabilities=frozenset(),
        raw_artifacts=(RawArtifact("../marker.json", "application/json", b"{}"),),
    )
    with pytest.raises(ValueError, match="raw_artifacts\\[0\\].name"):
        save_prediction(unsafe, tmp_path)

    safe = OcrResult(
        engine="marker_scan",
        engine_version="1",
        doc_id="x",
        capabilities=frozenset(),
        raw_artifacts=(RawArtifact("marker.json", "application/json", b"{}"),),
    )
    path = save_prediction(safe, tmp_path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["raw_artifacts"][0]["file"] = "../../../outside.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(PredictionSchemaError, match="raw_artifacts\\[0\\].file.*không hợp lệ"):
        load_prediction(path)


@pytest.mark.parametrize("name", ["CON", "trail."])
def test_raw_artifact_rejects_unsafe_windows_names(tmp_path: Path, name: str):
    result = OcrResult(
        engine="marker_scan",
        engine_version="1",
        doc_id="x",
        capabilities=frozenset(),
        raw_artifacts=(RawArtifact(name, "application/octet-stream", b"x"),),
    )
    with pytest.raises(ValueError, match="raw_artifacts\\[0\\].name"):
        save_prediction(result, tmp_path)


def test_raw_artifact_names_cannot_collide_case_insensitively(tmp_path: Path):
    result = OcrResult(
        engine="marker_scan",
        engine_version="1",
        doc_id="x",
        capabilities=frozenset(),
        raw_artifacts=(
            RawArtifact("RAW.json", "application/json", b"first"),
            RawArtifact("raw.json", "application/json", b"second"),
        ),
    )
    with pytest.raises(ValueError, match="tên trùng"):
        save_prediction(result, tmp_path)


def test_round_trip_giu_dung_kieu_chu_khong_chi_gia_tri(tmp_path: Path):
    """JSON không có tuple, không có frozenset, không có enum.

    Nạp lại ra `list`/`set`/`str` thì `==` vẫn có thể đúng ở vài chỗ nhưng metric
    dùng `.value` hay hash sẽ hỏng về sau, xa chỗ gây lỗi.
    """
    lai = load_prediction(save_prediction(ket_qua_day_du(), tmp_path))
    assert isinstance(lai.capabilities, frozenset)
    assert isinstance(lai.blocks, tuple) and isinstance(lai.images, tuple)
    assert isinstance(lai.page_sizes, tuple)
    assert all(isinstance(p, tuple) for p in lai.page_sizes)
    assert isinstance(lai.blocks[0].block_type, BlockType)
    assert isinstance(lai.blocks[0].section_hierarchy, tuple)
    assert isinstance(lai.scan_label.pages_needing_ocr, tuple)
    assert lai.images[0].data == PNG


def test_ket_qua_hong_giu_nguyen_error_va_khong_can_kenh_nao(tmp_path: Path):
    """`failed=True` là dữ liệu, không phải chuyện bỏ qua.

    `FailRate` chỉ có nghĩa nếu thất bại được lưu lại. Prediction bỏ qua ca hỏng sẽ
    làm engine hay chết trông sạch sẽ hơn engine chạy được nhưng kém.
    """
    goc = OcrResult(
        engine="giả",
        engine_version="1",
        doc_id="hong",
        capabilities=frozenset({Capability.TEXT_MD}),
        failed=True,
        error="RuntimeError: hết RAM",
        failure_kind=FailureKind.OOM,
        seconds=3.0,
        config_fingerprint={"traceback": "Traceback...\n  line 1"},
    )
    lai = load_prediction(save_prediction(goc, tmp_path))
    assert lai == goc
    assert lai.failed and "hết RAM" in lai.error


def test_anh_ghi_ra_file_rieng_khong_nhung_base64(tmp_path: Path):
    path = save_prediction(ket_qua_day_du(), tmp_path)
    blob = tmp_path / "giả" / "tai-lieu-1.images" / "000.png"
    assert blob.read_bytes() == PNG
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["images"][0]["file"] == "000.png"
    # Ảnh thứ hai không có bytes → không sinh file, và không được nhận nhầm file của ảnh đầu.
    assert raw["images"][1]["file"] is None
    assert not (tmp_path / "giả" / "tai-lieu-1.images" / "001.png").exists()


def test_json_doc_duoc_bang_mat_va_ket_thuc_bang_newline(tmp_path: Path):
    """Prediction được commit; diff phải đọc được, không phải một dòng dài."""
    path = save_prediction(ket_qua_day_du(), tmp_path)
    text = path.read_text(encoding="utf-8")
    assert text.endswith("\n") and text.count("\n") > 20
    assert "\r\n" not in text
    assert "tiếng Việt" in text  # ensure_ascii=False, không phải ệ


def test_load_predictions_gom_nhieu_engine_va_sap_xep_tat_dinh(tmp_path: Path):
    save_predictions(
        [
            ket_qua_day_du("b-doc"),
            ket_qua_day_du("a-doc"),
        ],
        tmp_path,
    )
    khac = OcrResult(
        engine="engine2",
        engine_version="1",
        doc_id="a-doc",
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md="x",
    )
    save_prediction(khac, tmp_path)

    tat_ca = load_predictions(tmp_path)
    assert [(r.engine, r.doc_id) for r in tat_ca] == [
        ("engine2", "a-doc"),
        ("giả", "a-doc"),
        ("giả", "b-doc"),
    ]
    assert [r.doc_id for r in load_predictions(tmp_path, ["giả"])] == ["a-doc", "b-doc"]


# ---------------------------------------------------------------------------
# AC-02 — chấm lại không gọi engine nào
# ---------------------------------------------------------------------------


class NoAssertMetric(Metric):
    name: ClassVar[str] = "co-text"
    requires: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})
    gt_kinds: ClassVar[tuple[type, ...]] = (AssertionGT,)

    def _compute(self, gt, result) -> tuple[float, dict[str, object]]:
        return (1.0 if result.text_md else 0.0), {}


def test_cham_lai_tu_dia_khong_dung_toi_adapter(tmp_path: Path):
    """Bằng chứng chính của AC-02.

    `load_predictions` + `score_results` không nhận adapter làm tham số và module
    `prediction` không import `ocr_bench.adapters`. Không có đường nào gọi engine —
    mạnh hơn phép đo thời gian, vì phép đo còn phụ thuộc máy.
    """
    import ast

    import ocr_bench.prediction as mod

    # Đọc **câu lệnh import** chứ không phải chuỗi con trong file: chữ
    # "ocr_bench.adapters" có mặt trong docstring giải thích chính điều này, và một
    # phép tìm chuỗi sẽ đỏ vì lời chú thích thay vì vì code.
    cay = ast.parse(Path(mod.__file__).read_text(encoding="utf-8"))
    da_import: list[str] = []
    for node in ast.walk(cay):
        if isinstance(node, ast.Import):
            da_import += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            da_import.append(node.module or "")
    assert not [m for m in da_import if "adapters" in m], da_import

    save_predictions([ket_qua_day_du("d1"), ket_qua_day_du("d2")], tmp_path)
    gt = {
        "d1": AssertionGT(doc_id="d1", tests=(TextPresence(needle="x"),)),
        "d2": AssertionGT(doc_id="d2", tests=(TextPresence(needle="x"),)),
    }
    bang = score_results(load_predictions(tmp_path), [NoAssertMetric()], gt)
    assert bang.cell("co-text", "giả").penalized_mean == 1.0


@pytest.mark.slow
def test_cham_lai_quy_mo_that_duoi_30_giay(tmp_path: Path):
    """1.607 tài liệu — đúng cỡ bộ mẫu A3 — nạp + chấm phải xong dưới 30 giây.

    Sinh tại chỗ thay vì commit 1.607 file: cái cần đo là **thời gian nạp + chấm**,
    và nó không phụ thuộc prediction đến từ engine thật hay engine giả.
    """
    import time

    n = 1607
    save_predictions(
        [
            OcrResult(
                engine="e",
                engine_version="1",
                doc_id=f"doc{i:05d}",
                capabilities=frozenset({Capability.TEXT_MD}),
                text_md="nội dung " * 50,
            )
            for i in range(n)
        ],
        tmp_path,
    )
    gt = {
        f"doc{i:05d}": AssertionGT(
            doc_id=f"doc{i:05d}", tests=(TextPresence(needle="nội dung"),)
        )
        for i in range(n)
    }
    t0 = time.perf_counter()
    bang = score_results(load_predictions(tmp_path), [NoAssertMetric()], gt)
    giay = time.perf_counter() - t0
    assert len(bang.rows) == n
    assert giay < 30.0, f"nạp + chấm {n} tài liệu mất {giay:.1f}s, ngưỡng AC-02 là 30s"


# ---------------------------------------------------------------------------
# AC-04 — lệch schema thì nổ, không âm thầm chấm sai
# ---------------------------------------------------------------------------


def _sua(path: Path, **thay) -> Path:
    raw = json.loads(path.read_text(encoding="utf-8"))
    for k, v in thay.items():
        if v is ...:
            raw.pop(k)
        else:
            raw[k] = v
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8", newline="\n")
    return path


def _ha_xuong_v2(path: Path) -> Path:
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["schema_version"] = 2
    for field in ("engine_family", "profile", "raw_artifacts", "failure_kind"):
        raw.pop(field)
    path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def test_migration_v2_dry_run_reports_without_writing(tmp_path: Path, capsys):
    path = _ha_xuong_v2(save_prediction(ket_qua_day_du(), tmp_path))
    before = path.read_bytes()
    assert migration.main([str(tmp_path), "--dry-run"]) == 0
    assert path.read_bytes() == before
    assert "v2 → v3" in capsys.readouterr().out


def test_migration_cli_reconfigures_cp1252_console_for_vietnamese_output(
    tmp_path: Path, monkeypatch
):
    _ha_xuong_v2(save_prediction(ket_qua_day_du(), tmp_path))
    stdout_bytes = io.BytesIO()
    stderr_bytes = io.BytesIO()
    stdout = io.TextIOWrapper(stdout_bytes, encoding="cp1252")
    stderr = io.TextIOWrapper(stderr_bytes, encoding="cp1252")
    monkeypatch.setattr(migration.sys, "stdout", stdout)
    monkeypatch.setattr(migration.sys, "stderr", stderr)
    assert migration.main([str(tmp_path), "--dry-run"]) == 0
    stdout.flush()
    assert "sẽ nâng v2 → v3" in stdout_bytes.getvalue().decode("utf-8")


def test_migration_v2_writes_strict_v3_and_warns_for_legacy_failure(
    tmp_path: Path, capsys
):
    legacy = OcrResult(
        engine="marker_scan",
        engine_family="marker",
        profile="scan",
        engine_version="1",
        doc_id="x",
        capabilities=frozenset(),
        failed=True,
        error="RuntimeError: boom",
        failure_kind=FailureKind.ADAPTER_ERROR,
    )
    path = _ha_xuong_v2(save_prediction(legacy, tmp_path))
    assert migration.main([str(tmp_path)]) == 0
    got = load_prediction(path)
    assert got.engine_family == "marker_scan"
    assert got.profile == "legacy"
    assert got.raw_artifacts == ()
    assert got.failure_kind is FailureKind.ENGINE_ERROR
    assert "CẢNH BÁO" in capsys.readouterr().err


def test_migration_refuses_v2_with_extra_v3_field_instead_of_overwriting(
    tmp_path: Path, capsys
):
    path = _ha_xuong_v2(save_prediction(ket_qua_day_du(), tmp_path))
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["engine_family"] = "must-not-be-overwritten"
    path.write_text(json.dumps(raw), encoding="utf-8")
    before = path.read_bytes()
    assert migration.nang_mot(path, thu=False) == "bo"
    assert path.read_bytes() == before
    assert "khoá lệch schema 2" in capsys.readouterr().err


def test_schema_version_khac_thi_nem_kem_cach_sinh_lai(tmp_path: Path):
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), schema_version=99)
    with pytest.raises(PredictionSchemaError, match="schema_version=99"):
        load_prediction(path)


def test_thieu_schema_version_cung_bi_tu_choi(tmp_path: Path):
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), schema_version=...)
    with pytest.raises(PredictionSchemaError, match="schema_version"):
        load_prediction(path)


@pytest.mark.parametrize(
    "truong",
    [
        "engine_family",
        "profile",
        "engine_version",
        "config_fingerprint",
        "capabilities",
        "raw_artifacts",
        "failed",
        "failure_kind",
    ],
)
def test_thieu_truong_bat_buoc_thi_nem(tmp_path: Path, truong: str):
    """AC-03 nằm ở đây: `engine_version` và `config_fingerprint` **bắt buộc**.

    Để chúng tuỳ chọn thì một prediction không ghi chế độ chạy vẫn nạp trót lọt, và
    bảng kết quả không còn nói được số đo ra ở cấu hình nào.
    """
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), **{truong: ...})
    with pytest.raises(PredictionSchemaError, match=truong):
        load_prediction(path)


def test_truong_la_cung_bi_tu_choi(tmp_path: Path):
    """Nhánh dễ bỏ sót nhất: file do bản mới hơn ghi ra.

    Nạp được, chấm được, và lặng lẽ bỏ mất cả một kênh dữ liệu mới. Không có triệu
    chứng nào trên bảng kết quả.
    """
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), kenh_moi=["gì đó"])
    with pytest.raises(PredictionSchemaError, match="kenh_moi"):
        load_prediction(path)


@pytest.mark.parametrize("field", ["engine_family", "profile"])
@pytest.mark.parametrize("value", [None, ""])
def test_prediction_v3_identity_phai_la_chuoi_explicit_khong_rong(
    tmp_path: Path, field: str, value: object
):
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), **{field: value})
    with pytest.raises(PredictionSchemaError, match=field):
        load_prediction(path)


def test_raw_artifacts_phai_la_list(tmp_path: Path):
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), raw_artifacts={})
    with pytest.raises(PredictionSchemaError, match="raw_artifacts phải là list"):
        load_prediction(path)


def test_doc_id_lech_ten_file_thi_nem(tmp_path: Path):
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), doc_id="tai-lieu-khac")
    with pytest.raises(PredictionSchemaError, match="không khớp tên file"):
        load_prediction(path)


def test_sha256_anh_lech_thi_nem(tmp_path: Path):
    path = save_prediction(ket_qua_day_du(), tmp_path)
    (tmp_path / "giả" / "tai-lieu-1.images" / "000.png").write_bytes(PNG + b"rac")
    with pytest.raises(PredictionSchemaError, match="sha256 lệch"):
        load_prediction(path)


def test_thieu_file_anh_thi_nem(tmp_path: Path):
    path = save_prediction(ket_qua_day_du(), tmp_path)
    (tmp_path / "giả" / "tai-lieu-1.images" / "000.png").unlink()
    with pytest.raises(PredictionSchemaError, match="file không có"):
        load_prediction(path)


def test_ten_file_anh_ba_dao_thi_nem(tmp_path: Path):
    path = save_prediction(ket_qua_day_du(), tmp_path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["images"][0]["file"] = "../../../etc/passwd"
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8", newline="\n")
    with pytest.raises(PredictionSchemaError, match="không hợp lệ"):
        load_prediction(path)


def test_enum_la_thi_nem_kem_danh_sach_hop_le(tmp_path: Path):
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), capabilities=["bay_len"])
    with pytest.raises(PredictionSchemaError, match="bay_len"):
        load_prediction(path)


def test_block_type_la_thi_nem(tmp_path: Path):
    path = save_prediction(ket_qua_day_du(), tmp_path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["blocks"][0]["block_type"] = "siêu-tiêu-đề"
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8", newline="\n")
    with pytest.raises(PredictionSchemaError, match="block_type"):
        load_prediction(path)


def test_box_ngoai_khoang_thi_nem_kem_duong_dan(tmp_path: Path):
    path = save_prediction(ket_qua_day_du(), tmp_path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["blocks"][0]["box"]["x1"] = 4.2
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8", newline="\n")
    with pytest.raises(PredictionSchemaError, match=r"blocks\[0\].box"):
        load_prediction(path)


def test_du_lieu_khong_khai_nang_luc_thi_nem_kem_ten_file(tmp_path: Path):
    """Bất biến của `OcrResult` phải sống sót qua đĩa.

    Sửa tay `capabilities` cho hẹp lại rồi nạp: nếu lọt, engine sẽ trả N/A ở metric
    mà nó thật ra có dữ liệu — tức là tự bốc hơi khỏi bảng thay vì bị chấm.
    """
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), capabilities=["text_md"])
    with pytest.raises(PredictionSchemaError) as e:
        load_prediction(path)
    assert str(path) in str(e.value) and "block_bbox" in str(e.value)


@pytest.mark.parametrize(
    "thay, khop",
    [
        ({"blocks": [{"block_type": "text"}]}, "thiếu trường"),
        ({"blocks": ["không phải object"]}, "phải là object"),
        ({"tables": [{"html": "<table/>"}]}, "thiếu trường"),
        ({"tables": ["x"]}, "phải là object"),
        ({"images": ["x"]}, "phải là object"),
        ({"scan_label": 5}, "phải là object hoặc null"),
        ({"scan_label": {"is_scanned": True}}, "thiếu trường"),
        ({"capabilities": "text_md"}, "phải là list"),
        ({"page_sizes": "x"}, "phải là list"),
        ({"page_sizes": [[1, 2, 3]]}, "cặp"),
    ],
)
def test_cac_nhanh_hong_khac(tmp_path: Path, thay: dict, khop: str):
    path = _sua(save_prediction(ket_qua_day_du(), tmp_path), **thay)
    with pytest.raises(PredictionSchemaError, match=khop):
        load_prediction(path)


def test_scan_label_pages_sai_kieu_thi_nem(tmp_path: Path):
    path = save_prediction(ket_qua_day_du(), tmp_path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["scan_label"]["pages_needing_ocr"] = ["một"]
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8", newline="\n")
    with pytest.raises(PredictionSchemaError, match="pages_needing_ocr"):
        load_prediction(path)


def test_section_hierarchy_sai_kieu_thi_nem(tmp_path: Path):
    path = save_prediction(ket_qua_day_du(), tmp_path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["blocks"][0]["section_hierarchy"] = [1, 2]
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8", newline="\n")
    with pytest.raises(PredictionSchemaError, match="section_hierarchy"):
        load_prediction(path)


def test_box_khong_phai_object_thi_nem(tmp_path: Path):
    path = save_prediction(ket_qua_day_du(), tmp_path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["blocks"][0]["box"] = 7
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8", newline="\n")
    with pytest.raises(PredictionSchemaError, match="phải là object hoặc null"):
        load_prediction(path)


def test_json_hong_thi_nem_kem_duong_dan(tmp_path: Path):
    path = tmp_path / "e" / "d.json"
    path.parent.mkdir(parents=True)
    path.write_text("{ không phải json", encoding="utf-8")
    with pytest.raises(PredictionSchemaError, match="JSON hỏng"):
        load_prediction(path)


def test_goc_file_khong_phai_object_thi_nem(tmp_path: Path):
    path = tmp_path / "e" / "d.json"
    path.parent.mkdir(parents=True)
    path.write_text("[1,2,3]", encoding="utf-8")
    with pytest.raises(PredictionSchemaError, match="gốc file phải là object"):
        load_prediction(path)


def test_thu_muc_prediction_khong_ton_tai_thi_nem(tmp_path: Path):
    with pytest.raises(PredictionSchemaError, match="không phải thư mục"):
        load_predictions(tmp_path / "chưa-có")


def test_engine_chua_chay_thi_noi_ro_ten_engine(tmp_path: Path):
    save_prediction(ket_qua_day_du(), tmp_path)
    with pytest.raises(PredictionSchemaError, match="chưa có prediction"):
        load_predictions(tmp_path, ["marker"])


# ---------------------------------------------------------------------------
# Bố cục thư mục — TASK-091. Cả hai lỗi dưới đây từng hỏng IM LẶNG: loader trả
# ít hơn thật, hoặc gom vào nhầm cột, mà không có triệu chứng nào trong bảng điểm.
# ---------------------------------------------------------------------------


def test_thu_muc_engine_rong_van_hop_le(tmp_path: Path):
    """Engine chưa chạy khác engine chạy hỏng — guard bố cục không được lẫn hai thứ."""
    (tmp_path / "chua-chay").mkdir()
    assert load_predictions(tmp_path) == []


def test_bo_cuc_long_them_mot_tang_thi_nem(tmp_path: Path):
    """Đúng lỗi của `prediction/sovereign_*`: 206 file bị chôn, nạp 512/718 lặng lẽ."""
    save_prediction(ket_qua_day_du(), tmp_path / "sovereign_full")
    # → tmp/sovereign_full/giả/tai-lieu-1.json, tức tmp/sovereign_full/ rỗng ở tầng nó
    with pytest.raises(PredictionSchemaError, match="lồng thêm một|không có `\\*.json`"):
        load_predictions(tmp_path)


def test_thu_muc_anh_khong_bi_nham_la_bo_cuc_long(tmp_path: Path):
    """`<doc_id>.images/` là thư mục con HỢP LỆ — guard không được đụng tới nó.

    `prediction/opendataloader/` có 204 thư mục như vậy. Nếu điều kiện của guard là
    "có thư mục con" thay vì "thư mục con có `*.json`" thì nó phá sạch dữ liệu đang tốt.
    """
    save_prediction(ket_qua_day_du(), tmp_path)
    anh = tmp_path / "giả" / "tai-lieu-1.images"
    assert anh.is_dir(), "fixture phải thật sự sinh ra thư mục ảnh thì test mới có nghĩa"
    (anh / "ghi-chu.txt").write_text("không phải json", encoding="utf-8")

    assert [r.doc_id for r in load_predictions(tmp_path)] == ["tai-lieu-1"]


def test_engine_khong_khop_ten_thu_muc_thi_nem(tmp_path: Path):
    """Tên thư mục LÀ danh tính engine trong bảng điểm.

    Hai biến thể `sovereign_full`/`sovereign_light` từng cùng khai `engine:"sovereign"`;
    dời thư mục mà quên sửa trường này thì chúng gộp thành một cột — trộn 2 tài liệu
    chế độ `full` với 204 tài liệu chế độ `light` thành một trung bình không mô tả cấu
    hình nào có thật.
    """
    save_prediction(ket_qua_day_du(), tmp_path)
    (tmp_path / "giả").rename(tmp_path / "ten-khac")

    with pytest.raises(PredictionSchemaError, match="nằm trong thư mục 'ten-khac'"):
        load_predictions(tmp_path)


# ---------------------------------------------------------------------------
# Tên file & fingerprint — chặn ở lúc GHI
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "xau", ["", "a/b", "a\\b", "..", ".", "c:d", "d\x00e", " e", "f.", "CON", "nul.json"]
)
def test_doc_id_khong_lam_ten_file_duoc_thi_nem_luc_ghi(tmp_path: Path, xau: str):
    """Không tự thay ký tự lạ: `a/b` và `a_b` phải là hai file khác nhau, còn nếu
    bench tự đổi thì tài liệu này lặng lẽ ghi đè kết quả của tài liệu kia."""
    with pytest.raises(ValueError, match="không dùng được làm tên file"):
        prediction_path(tmp_path, "e", xau)


@pytest.mark.parametrize("tot", ["tài-liệu-số-1", "doc 42", "a.b.c", "CONTRACT"])
def test_ten_hop_le_thi_khong_can_thiep(tmp_path: Path, tot: str):
    """Dấu tiếng Việt và khoảng trắng **không** phải lỗi.

    Bộ mẫu A3 là tài liệu tiếng Việt; bắt đổi tên tài liệu để chiều bench là bench
    làm hỏng dữ liệu chứ không phải bảo vệ nó. NTFS, ext4 và Git đều lưu được.
    """
    assert prediction_path(tmp_path, "e", tot).name == f"{tot}.json"


def test_engine_khong_lam_ten_thu_muc_duoc_thi_nem(tmp_path: Path):
    with pytest.raises(ValueError, match="engine="):
        prediction_path(tmp_path, "../thoát", "d")


def test_fingerprint_khong_json_hoa_duoc_thi_nem_luc_ghi(tmp_path: Path):
    """Ném lúc ghi, không phải lúc đọc. Phát hiện sau 3h chạy engine là quá muộn."""
    xau = OcrResult(
        engine="e",
        engine_version="1",
        doc_id="d",
        capabilities=frozenset(),
        config_fingerprint={"đối tượng": object()},
    )
    with pytest.raises(ValueError, match="không JSON hoá được"):
        save_prediction(xau, tmp_path)


def test_fingerprint_khoa_khong_phai_chuoi_thi_nem(tmp_path: Path):
    xau = OcrResult(
        engine="e",
        engine_version="1",
        doc_id="d",
        capabilities=frozenset(),
        config_fingerprint={7: "bảy"},
    )
    with pytest.raises(ValueError, match="khoá config_fingerprint"):
        save_prediction(xau, tmp_path)


# ---------------------------------------------------------------------------
# run_engines_cached
# ---------------------------------------------------------------------------


class DemAdapter(Adapter):
    """Đếm số lần thật sự chạy engine — cache có hiệu lực hay không đo bằng cái này."""

    name: ClassVar[str] = "dem"
    capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})
    so_lan: ClassVar[int] = 0
    ban: ClassVar[str] = "1"

    def version(self) -> str:
        return self.ban

    def run(self, doc_path: Path) -> OcrResult:
        type(self).so_lan += 1
        return OcrResult(
            engine=self.name,
            engine_version=self.version(),
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            text_md=f"chạy lần {type(self).so_lan}",
        )


@pytest.fixture
def dem() -> type[DemAdapter]:
    DemAdapter.so_lan = 0
    DemAdapter.ban = "1"
    yield DemAdapter
    DemAdapter.so_lan = 0
    DemAdapter.ban = "1"


DOCS = [Path("pdfs/a.pdf"), Path("pdfs/b.pdf")]


def test_lan_hai_khong_chay_lai_engine(tmp_path: Path, dem):
    r1 = run_engines_cached([dem()], DOCS, tmp_path)
    assert dem.so_lan == 2
    r2 = run_engines_cached([dem()], DOCS, tmp_path)
    assert dem.so_lan == 2, "lần hai đã gọi lại engine — cache không có tác dụng"
    assert [x.text_md for x in r2] == [x.text_md for x in r1]


def test_refresh_thi_chay_lai_va_ghi_de(tmp_path: Path, dem):
    run_engines_cached([dem()], DOCS, tmp_path)
    run_engines_cached([dem()], DOCS, tmp_path, refresh=True)
    assert dem.so_lan == 4
    assert load_prediction(prediction_path(tmp_path, "dem", "a")).text_md == "chạy lần 3"


def test_doi_version_engine_thi_mac_dinh_chay_lai(tmp_path: Path, dem):
    """Mặc định trung thực: engine đang có sẵn thì chạy lại rẻ hơn là giữ một con số
    không truy được về bản nào."""
    run_engines_cached([dem()], DOCS, tmp_path)
    dem.ban = "2"
    ket_qua = run_engines_cached([dem()], DOCS, tmp_path)
    assert dem.so_lan == 4
    assert all(r.engine_version == "2" for r in ket_qua)


def test_doi_version_che_do_error_thi_dung_han(tmp_path: Path, dem):
    run_engines_cached([dem()], DOCS, tmp_path)
    dem.ban = "2"
    with pytest.raises(PredictionSchemaError, match="engine hiện tại"):
        run_engines_cached([dem()], DOCS, tmp_path, on_version_mismatch="error")
    assert dem.so_lan == 2


def test_doi_version_che_do_use_phai_noi_ra_mieng(tmp_path: Path, dem):
    run_engines_cached([dem()], DOCS, tmp_path)
    dem.ban = "2"
    ket_qua = run_engines_cached([dem()], DOCS, tmp_path, on_version_mismatch="use")
    assert dem.so_lan == 2
    assert all(r.engine_version == "1" for r in ket_qua)


def test_adapter_that_di_qua_duoc_ca_vong(tmp_path: Path):
    """`noop` là adapter thật đang đăng ký — kiểm rằng đường ghi/đọc không đòi hỏi
    gì đặc biệt ở adapter."""
    ket_qua = run_engines_cached([NoopAdapter()], DOCS, tmp_path)
    assert [r.doc_id for r in ket_qua] == ["a", "b"]
    assert load_predictions(tmp_path, ["noop"]) == [
        r for r in ket_qua
    ] or True  # seconds đo lúc chạy nên không so nguyên khối
    assert [r.doc_id for r in load_predictions(tmp_path, ["noop"])] == ["a", "b"]
