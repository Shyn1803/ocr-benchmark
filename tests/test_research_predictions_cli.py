"""Publication runner must fail closed before spending time on OCR engines."""

from __future__ import annotations

import dataclasses
import importlib.util
import hashlib
import inspect
import json
import os
import sys
from pathlib import Path

import pytest

from ocr_bench.prediction import save_prediction
from ocr_bench.profiles import EngineProfile
from ocr_bench.types import Capability, OcrResult

ROOT = Path(__file__).resolve().parents[1]


def _load_script():
    path = ROOT / "scripts" / "run_research_predictions.py"
    spec = importlib.util.spec_from_file_location("_research_predictions", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _profile(name: str = "marker_default", *, force_ocr: bool = False) -> EngineProfile:
    family, variant = name.rsplit("_", 1)
    return EngineProfile(
        name=name,
        family=family,
        profile=variant,
        adapter=family,
        config={"force_ocr": force_ocr, "use_llm": False},
        environment={},
    )


class _FakeAdapter:
    name = "marker_default"
    capabilities = frozenset({Capability.TEXT_MD})

    def __init__(
        self,
        *,
        configured_as: str | None = None,
        perf: bool = True,
        record_hardware: bool = True,
        record_evidence_version: bool = True,
        evidence_version: object = 1,
        result_hardware: str | None = None,
        omit_result_hardware: bool = False,
    ) -> None:
        self.execute_count = 0
        self.configured_as = configured_as
        self.perf = perf
        self.record_hardware = record_hardware
        self.record_evidence_version = record_evidence_version
        self.evidence_version = evidence_version
        self.result_hardware = result_hardware
        self.omit_result_hardware = omit_result_hardware
        self.effective_hardware: str | None = None
        self.events: list[str] = []

    def configure_hardware(self, hardware: str) -> str:
        self.events.append(f"configure:{hardware}")
        self.effective_hardware = self.configured_as or hardware
        return self.effective_hardware

    def version(self) -> str:
        return "fake-1"

    def config_fingerprint(self) -> dict[str, object]:
        fingerprint: dict[str, object] = {"force_ocr": False, "use_llm": False}
        if self.record_hardware and self.effective_hardware is not None:
            fingerprint.update(
                hardware=self.effective_hardware,
                device=self.effective_hardware,
            )
            if self.record_evidence_version:
                fingerprint["hardware_evidence_version"] = self.evidence_version
        return fingerprint

    def execute(self, doc: Path) -> OcrResult:
        self.events.append("execute")
        self.execute_count += 1
        fingerprint = self.config_fingerprint()
        if self.omit_result_hardware:
            for key in ("hardware", "device", "hardware_evidence_version"):
                fingerprint.pop(key, None)
        if self.result_hardware is not None:
            fingerprint.update(
                hardware=self.result_hardware,
                device=self.result_hardware,
            )
        return OcrResult(
            engine=self.name,
            engine_family="marker",
            profile="default",
            engine_version=self.version(),
            doc_id=doc.stem,
            capabilities=self.capabilities,
            text_md="ok",
            seconds=1.0 if self.perf else None,
            peak_rss_mb=2.0 if self.perf else None,
            rss_scope="process" if self.perf else None,
            config_fingerprint=fingerprint,
        )


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _dataset_manifest(path: Path, rows: list[dict[str, object]]) -> Path:
    path.write_text(json.dumps({"documents": rows}), encoding="utf-8")
    return path


def test_publication_cli_refuses_partial_profile_set_before_build(tmp_path, monkeypatch):
    runner = _load_script()
    built = False

    def forbidden_build(_profile):
        nonlocal built
        built = True
        raise AssertionError("publication subset reached adapter construction")

    monkeypatch.setattr(runner.registry, "build_adapter", forbidden_build)
    rc = runner.main(["--profiles", "marker_default", "--out", str(tmp_path)])

    assert rc == 2
    assert built is False
    assert not list(tmp_path.iterdir()), "a rejected publication run must not create output"


def test_preflight_fingerprint_must_match_locked_config():
    from ocr_bench.preflight import PreflightError, verify_fingerprint

    profile = _profile("marker_scan", force_ocr=True)
    with pytest.raises(PreflightError, match="force_ocr"):
        verify_fingerprint(profile, {"force_ocr": False, "use_llm": False})


def test_dataset_manifest_alone_selects_and_verifies_documents(tmp_path):
    from ocr_bench.preflight import verify_dataset_manifest

    pdfs = tmp_path / "pdfs"
    pdfs.mkdir()
    keep = pdfs / "keep.pdf"
    keep.write_bytes(b"%PDF-keep")
    (pdfs / "not-listed.pdf").write_bytes(b"%PDF-extra")
    manifest = _dataset_manifest(
        tmp_path / "manifest.json",
        [
            {
                "document_id": "keep",
                "pdf_path": "pdfs/keep.pdf",
                "pdf_sha256": _sha(b"%PDF-keep"),
            }
        ],
    )

    documents = verify_dataset_manifest(manifest, tmp_path)

    assert [(row.doc_id, row.path) for row in documents] == [("keep", keep.resolve())]
    assert documents.manifest_sha256 == _sha(manifest.read_bytes())
    assert documents.provisional is False


def test_pdf_changed_after_manifest_validation_is_rejected_before_execute(tmp_path):
    from ocr_bench.preflight import PreflightError, verify_dataset_manifest

    runner = _load_script()
    pdfs = tmp_path / "pdfs"
    pdfs.mkdir()
    doc = pdfs / "doc.pdf"
    doc.write_bytes(b"%PDF-original")
    manifest = _dataset_manifest(
        tmp_path / "manifest.json",
        [
            {
                "document_id": "doc",
                "pdf_path": "pdfs/doc.pdf",
                "pdf_sha256": _sha(b"%PDF-original"),
            }
        ],
    )
    verified = verify_dataset_manifest(manifest, tmp_path)
    doc.write_bytes(b"%PDF-mutated")
    adapter = _FakeAdapter()

    with pytest.raises(PreflightError, match="checksum|sha256"):
        runner.run_profile_predictions(
            _profile(),
            adapter,
            verified,
            tmp_path / "prediction" / "cpu",
            hardware="cpu",
            mode="publication",
        )
    assert adapter.execute_count == 0


@pytest.mark.parametrize("case", ["missing", "duplicate", "escape", "checksum"])
def test_dataset_manifest_rejects_unsafe_or_ambiguous_rows(tmp_path, case):
    from ocr_bench.preflight import PreflightError, verify_dataset_manifest

    pdfs = tmp_path / "pdfs"
    pdfs.mkdir()
    doc = pdfs / "doc.pdf"
    doc.write_bytes(b"%PDF-doc")
    outside = tmp_path.parent / f"{tmp_path.name}-outside.pdf"
    outside.write_bytes(b"%PDF-outside")
    valid = {
        "document_id": "doc",
        "pdf_path": "pdfs/doc.pdf",
        "pdf_sha256": _sha(b"%PDF-doc"),
    }
    if case == "missing":
        rows = [{**valid, "pdf_path": "pdfs/missing.pdf"}]
    elif case == "duplicate":
        rows = [valid, valid]
    elif case == "escape":
        rows = [{**valid, "pdf_path": f"../{outside.name}"}]
    else:
        rows = [{**valid, "pdf_sha256": "0" * 64}]
    manifest = _dataset_manifest(tmp_path / "manifest.json", rows)

    with pytest.raises(PreflightError, match=case if case != "escape" else "ngoài"):
        verify_dataset_manifest(manifest, tmp_path)


def test_calibration_subset_writes_only_under_calibration_tree(tmp_path, monkeypatch):
    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-test")
    adapter = _FakeAdapter()

    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(runner, "discover_documents", lambda *_args, **_kw: [doc])
    monkeypatch.setattr(runner.registry, "build_adapter", lambda _profile: adapter)

    rc = runner.main(
        [
            "--mode",
            "calibration",
            "--profiles",
            profile.name,
            "--out",
            str(tmp_path / "run"),
        ]
    )

    assert rc == 0
    prediction = (
        tmp_path
        / "run"
        / "calibration"
        / "prediction"
        / "cpu"
        / profile.name
        / "fixture.json"
    )
    assert prediction.is_file()
    assert not (tmp_path / "run" / "results").exists()
    assert adapter.execute_count == 1


def test_cli_reports_missing_profile_adapter_without_traceback(tmp_path, monkeypatch):
    runner = _load_script()
    profile = _profile("missing_default")
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-test")
    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(runner, "discover_documents", lambda *_args, **_kw: [doc])

    rc = runner.main(
        [
            "--mode",
            "calibration",
            "--profiles",
            profile.name,
            "--out",
            str(tmp_path / "run"),
        ]
    )

    assert rc == 2
    assert not (tmp_path / "run" / "calibration" / "prediction").exists()


def test_default_calibration_manifest_is_honest_and_runnable(tmp_path, monkeypatch, capsys):
    runner = _load_script()
    profile = _profile()
    adapter = _FakeAdapter()
    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(runner.registry, "build_adapter", lambda _profile: adapter)

    args = runner._parser().parse_args(["--mode", "calibration"])
    assert args.dataset_manifest is None
    assert (
        runner.main(
            [
                "--mode",
                "calibration",
                "--profiles",
                profile.name,
                "--limit",
                "1",
                "--out",
                str(tmp_path),
            ]
        )
        == 0
    )
    assert adapter.execute_count == 1
    assert "JSON không hợp lệ" not in capsys.readouterr().err


def test_default_publication_requires_verified_non_provisional_manifest(
    tmp_path, monkeypatch, capsys
):
    runner = _load_script()
    profile = _profile()
    built = False

    def forbidden_build(_profile):
        nonlocal built
        built = True
        raise AssertionError("missing verified manifest reached adapter construction")

    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(runner.registry, "build_adapter", forbidden_build)
    # Trước Task 7 `datasets/manifest.json` chưa tồn tại, nên test này xanh nhờ **sự vắng
    # mặt tình cờ** của một file. Task 7 sinh ra đúng file đó và test đổi ý nghĩa lúc
    # nào không hay: nó bắt đầu chạy qua cổng manifest rồi đỏ ở một cổng khác. Trỏ thẳng
    # vào một đường dẫn không tồn tại để nó kiểm đúng thứ tên nó nói — chế độ publication
    # phải dừng trước khi dựng adapter khi manifest mặc định không có.
    monkeypatch.setattr(runner, "PUBLICATION_DATASET_MANIFEST", tmp_path / "khong-co.json")

    assert runner.main(["--out", str(tmp_path)]) == 2
    error = capsys.readouterr().err
    assert "verified" in error.lower()
    assert "dataset" in error.lower()
    assert "calibration-manifest" not in error
    assert built is False


def test_publication_rejects_explicit_provisional_manifest_before_build(
    tmp_path, monkeypatch, capsys
):
    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    manifest = tmp_path / "provisional.json"
    manifest.write_text(
        json.dumps(
            {
                "provisional": True,
                "documents": [
                    {
                        "document_id": doc.stem,
                        "pdf_path": doc.name,
                        "pdf_sha256": _sha(doc.read_bytes()),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(
        runner.registry,
        "build_adapter",
        lambda _profile: (_ for _ in ()).throw(
            AssertionError("provisional manifest reached adapter construction")
        ),
    )

    assert (
        runner.main(
            ["--dataset-manifest", str(manifest), "--out", str(tmp_path / "out")]
        )
        == 2
    )
    assert "provisional" in capsys.readouterr().err.lower()


def test_publication_cache_identity_mismatch_is_error_not_rerun(tmp_path):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    adapter = _FakeAdapter()
    output_root = tmp_path / "prediction" / "cpu"
    stale = adapter.execute(doc)
    stale = runner.attach_cache_identity(
        stale,
        {
            "doc_id": doc.stem,
            "pdf_sha256": "0" * 64,
            "profile_config_sha256": profile.fingerprint,
            "engine_version": adapter.version(),
            "hardware": "cpu",
        },
    )
    save_prediction(stale, output_root)
    adapter.execute_count = 0

    with pytest.raises(PreflightError, match="pdf_sha256"):
        runner.run_profile_predictions(
            profile,
            adapter,
            [doc],
            output_root,
            hardware="cpu",
            mode="publication",
        )

    assert adapter.execute_count == 0


def test_publication_cache_rejects_wrong_result_profile_even_with_matching_key(tmp_path):
    from ocr_bench.preflight import PreflightError, build_cache_identity

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    adapter = _FakeAdapter()
    output_root = tmp_path / "prediction" / "cpu"
    identity = build_cache_identity(
        doc,
        profile,
        engine_version=adapter.version(),
        hardware="cpu",
        capabilities=adapter.capabilities,
    )
    wrong_profile = OcrResult(
        engine=profile.name,
        engine_family=profile.family,
        profile="scan",
        engine_version=adapter.version(),
        doc_id=doc.stem,
        capabilities=adapter.capabilities,
        text_md="stale",
        config_fingerprint=adapter.config_fingerprint(),
    )
    save_prediction(runner.attach_cache_identity(wrong_profile, identity), output_root)

    with pytest.raises(PreflightError, match="profile"):
        runner.run_profile_predictions(
            profile,
            adapter,
            [doc],
            output_root,
            hardware="cpu",
            mode="publication",
        )


def test_publication_configures_hardware_before_execute_and_records_device(tmp_path):
    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    adapter = _FakeAdapter()

    result = runner.run_profile_predictions(
        profile,
        adapter,
        [doc],
        tmp_path / "prediction" / "cpu",
        hardware="cpu",
        mode="publication",
    )[0]

    assert adapter.events == ["configure:cpu", "execute"]
    assert result.config_fingerprint["hardware"] == "cpu"
    assert result.config_fingerprint["device"] == "cpu"
    assert result.config_fingerprint["hardware_evidence_version"] == 1


@pytest.mark.parametrize(
    "adapter,match",
    [
        (_FakeAdapter(record_hardware=False), "hardware"),
        (_FakeAdapter(record_evidence_version=False), "hardware_evidence_version"),
        (_FakeAdapter(evidence_version=2), "hardware_evidence_version"),
        (_FakeAdapter(evidence_version=True), "hardware_evidence_version"),
    ],
)
def test_publication_adapter_preflight_requires_versioned_hardware_evidence(
    adapter, match
):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    with pytest.raises(PreflightError, match=match):
        runner._configure_adapter_hardware(
            _profile(), adapter, "cpu", "publication"
        )


def test_runner_has_no_hardware_configuration_bypass():
    runner = _load_script()

    assert "hardware_configured" not in inspect.signature(
        runner.run_profile_predictions
    ).parameters


@pytest.mark.parametrize(
    "adapter,match",
    [
        (_FakeAdapter(omit_result_hardware=True), "thiếu hardware"),
        (_FakeAdapter(result_hardware="gpu"), "hardware.*gpu"),
    ],
)
def test_publication_rejects_missing_or_mismatched_fresh_hardware_evidence(
    tmp_path, adapter, match
):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    output_root = tmp_path / "prediction" / "cpu"

    with pytest.raises(PreflightError, match=match):
        runner.run_profile_predictions(
            _profile(),
            adapter,
            [doc],
            output_root,
            hardware="cpu",
            mode="publication",
        )

    assert adapter.execute_count == 1
    assert not (output_root / _profile().name / "fixture.json").exists()


def test_publication_rejects_adapter_hardware_mismatch_before_execute(tmp_path):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    adapter = _FakeAdapter(configured_as="gpu")
    with pytest.raises(PreflightError, match="hardware|device"):
        runner.run_profile_predictions(
            _profile(),
            adapter,
            [],
            tmp_path,
            hardware="cpu",
            mode="publication",
        )
    assert adapter.execute_count == 0


def test_publication_rejects_adapter_without_hardware_protocol(tmp_path):
    from ocr_bench.preflight import PreflightError

    class Unsupported:
        name = "marker_default"

        def version(self):
            return "fake-1"

        def config_fingerprint(self):
            return {"force_ocr": False, "use_llm": False}

        def execute(self, _doc):
            raise AssertionError("unsupported adapter must not execute")

    runner = _load_script()
    with pytest.raises(PreflightError, match="configure_hardware"):
        runner.run_profile_predictions(
            _profile(),
            Unsupported(),
            [],
            tmp_path,
            hardware="cpu",
            mode="publication",
        )


def test_publication_rejects_missing_perf_before_save(tmp_path):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")

    with pytest.raises(PreflightError, match="seconds"):
        runner.run_profile_predictions(
            profile,
            _FakeAdapter(perf=False),
            [doc],
            tmp_path / "prediction" / "cpu",
            hardware="cpu",
            mode="publication",
        )
    assert not (tmp_path / "prediction").exists()


def test_publication_rejects_cached_result_with_missing_perf_without_execute(tmp_path):
    from ocr_bench.preflight import PreflightError, build_cache_identity

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    adapter = _FakeAdapter(perf=False)
    identity = build_cache_identity(
        doc,
        profile,
        engine_version=adapter.version(),
        hardware="cpu",
        capabilities=adapter.capabilities,
    )
    output_root = tmp_path / "prediction" / "cpu"
    adapter.configure_hardware("cpu")
    save_prediction(
        runner.attach_cache_identity(adapter.execute(doc), identity), output_root
    )
    adapter.execute_count = 0

    with pytest.raises(PreflightError, match="seconds"):
        runner.run_profile_predictions(
            profile,
            adapter,
            [doc],
            output_root,
            hardware="cpu",
            mode="publication",
        )
    assert adapter.execute_count == 0


@pytest.mark.parametrize("bad_bytes", [b"{broken", b'{"schema_version":2}'])
@pytest.mark.parametrize("mode,should_execute", [("calibration", True), ("publication", False)])
def test_bad_cache_reruns_only_in_calibration(tmp_path, bad_bytes, mode, should_execute):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    output_root = tmp_path / "prediction" / "cpu"
    cache = output_root / profile.name / "fixture.json"
    cache.parent.mkdir(parents=True)
    cache.write_bytes(bad_bytes)
    adapter = _FakeAdapter()

    if mode == "publication":
        with pytest.raises(PreflightError):
            runner.run_profile_predictions(
                profile, adapter, [doc], output_root, hardware="cpu", mode=mode
            )
    else:
        runner.run_profile_predictions(
            profile, adapter, [doc], output_root, hardware="cpu", mode=mode
        )
    assert bool(adapter.execute_count) is should_execute


@pytest.mark.parametrize("mode,should_execute", [("calibration", True), ("publication", False)])
def test_non_object_cache_fingerprint_reruns_only_in_calibration(
    tmp_path, mode, should_execute
):
    from ocr_bench.preflight import PreflightError, build_cache_identity

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    output_root = tmp_path / "prediction" / "cpu"
    adapter = _FakeAdapter()
    adapter.configure_hardware("cpu")
    identity = build_cache_identity(
        doc,
        profile,
        engine_version=adapter.version(),
        hardware="cpu",
        capabilities=adapter.capabilities,
    )
    cache = save_prediction(
        runner.attach_cache_identity(adapter.execute(doc), identity), output_root
    )
    payload = json.loads(cache.read_text(encoding="utf-8"))
    payload["config_fingerprint"] = []
    cache.write_text(json.dumps(payload), encoding="utf-8")
    adapter.execute_count = 0
    adapter.events.clear()

    if mode == "publication":
        with pytest.raises(PreflightError, match="config_fingerprint"):
            runner.run_profile_predictions(
                profile, adapter, [doc], output_root, hardware="cpu", mode=mode
            )
    else:
        runner.run_profile_predictions(
            profile, adapter, [doc], output_root, hardware="cpu", mode=mode
        )

    assert bool(adapter.execute_count) is should_execute


@pytest.mark.parametrize("mode,should_execute", [("calibration", True), ("publication", False)])
def test_old_runner_stamped_cache_without_evidence_version_is_not_reused(
    tmp_path, mode, should_execute
):
    from ocr_bench.preflight import PreflightError, build_cache_identity

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    output_root = tmp_path / "prediction" / "cpu"
    adapter = _FakeAdapter()
    adapter.configure_hardware("cpu")
    identity = build_cache_identity(
        doc,
        profile,
        engine_version=adapter.version(),
        hardware="cpu",
        capabilities=adapter.capabilities,
    )
    old_result = adapter.execute(doc)
    old_fingerprint = dict(old_result.config_fingerprint)
    old_fingerprint.pop("hardware_evidence_version")
    old_result = dataclasses.replace(
        old_result,
        config_fingerprint=old_fingerprint,
    )
    save_prediction(runner.attach_cache_identity(old_result, identity), output_root)
    adapter.execute_count = 0
    adapter.events.clear()

    if mode == "publication":
        with pytest.raises(PreflightError, match="hardware_evidence_version"):
            runner.run_profile_predictions(
                profile, adapter, [doc], output_root, hardware="cpu", mode=mode
            )
    else:
        runner.run_profile_predictions(
            profile, adapter, [doc], output_root, hardware="cpu", mode=mode
        )

    assert bool(adapter.execute_count) is should_execute


def test_publication_helper_rejects_refresh_even_when_called_directly(tmp_path):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    with pytest.raises(PreflightError, match="refresh"):
        runner.run_profile_predictions(
            _profile(),
            _FakeAdapter(),
            [],
            tmp_path,
            hardware="cpu",
            mode="publication",
            refresh=True,
        )


def test_run_manifest_is_deterministic_except_generated_at(tmp_path):
    from ocr_bench.preflight import build_run_manifest

    manifest = tmp_path / "dataset.json"
    manifest.write_text('{"dataset":"fixed"}\n', encoding="utf-8")
    validated_manifest_sha256 = _sha(manifest.read_bytes())
    profile = _profile()
    fixed = {
        "git": {"commit": "a" * 40, "dirty": False},
        "system": {
            "python": "3.12.0",
            "os": "TestOS",
            "cpu": "Test CPU",
            "gpu": None,
            "ram_bytes": 1024,
        },
        "dependencies": {"ocr-bench": "0.1.0"},
    }

    first = build_run_manifest(
        mode="publication",
        hardware="cpu",
        profiles={profile.name: profile},
        dataset_manifest=manifest,
        dataset_manifest_sha256=validated_manifest_sha256,
        generated_at="2026-08-11T00:00:00Z",
        **fixed,
    )
    manifest.write_text('{"dataset":"changed after validation"}\n', encoding="utf-8")
    second = build_run_manifest(
        mode="publication",
        hardware="cpu",
        profiles={profile.name: profile},
        dataset_manifest=manifest,
        dataset_manifest_sha256=validated_manifest_sha256,
        generated_at="later",
        **fixed,
    )

    assert first | {"generated_at": "later"} == second
    assert first["profiles"] == [
        {"name": profile.name, "config_sha256": profile.fingerprint}
    ]
    assert first["dataset_manifest"]["sha256"] == (
        "c5c0225cf54a86b0e729ca91a74107ab9fefb5cc84a8819a6d5a3cf40b732345"
    )
    serialized = json.dumps(first, sort_keys=True)
    assert "secret" not in serialized.lower()


def test_manifest_changed_after_preflight_stops_before_execute_or_run_manifest(
    tmp_path, monkeypatch
):
    import ocr_bench.preflight as preflight

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    manifest = _dataset_manifest(
        tmp_path / "manifest.json",
        [
            {
                "document_id": doc.stem,
                "pdf_path": doc.name,
                "pdf_sha256": _sha(doc.read_bytes()),
            }
        ],
    )
    original_hash = _sha(manifest.read_bytes())
    adapter = _FakeAdapter()
    actual_preflight = runner.publication_preflight

    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(runner.registry, "build_adapter", lambda _profile: adapter)
    monkeypatch.setattr(
        preflight,
        "collect_git_metadata",
        lambda *_args, **_kwargs: {"commit": "a" * 40, "dirty": False},
    )

    def mutate_after_preflight(**kwargs):
        context = actual_preflight(
            **kwargs,
            system_probe=lambda: {
                "python": "3",
                "os": "x",
                "cpu": "cpu",
                "gpu": None,
                "ram_bytes": 1,
            },
            dependency_probe=lambda: {},
        )
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        payload["changed_after_preflight"] = True
        manifest.write_text(json.dumps(payload), encoding="utf-8")
        assert _sha(manifest.read_bytes()) != original_hash
        return context

    monkeypatch.setattr(runner, "publication_preflight", mutate_after_preflight)
    out = tmp_path / "out"

    assert (
        runner.main(
            ["--dataset-manifest", str(manifest), "--out", str(out)]
        )
        == 2
    )
    assert adapter.execute_count == 0
    assert not (out / "run-manifest.json").exists()


@pytest.mark.parametrize(
    "case",
    ["missing_method", "configure_raises", "return_mismatch", "fingerprint_bad"],
)
def test_adapter_preflight_failure_writes_no_manifest_or_prediction(
    tmp_path, monkeypatch, case
):
    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    manifest = _dataset_manifest(tmp_path / "manifest.json", [])
    verified_doc = runner.DatasetDocument(doc.stem, doc, _sha(doc.read_bytes()))

    class MissingMethod(_FakeAdapter):
        configure_hardware = None

    class ConfigureRaises(_FakeAdapter):
        def configure_hardware(self, hardware):
            self.events.append(f"configure:{hardware}")
            raise RuntimeError("hardware setup failed")

    adapters = {
        "missing_method": MissingMethod(),
        "configure_raises": ConfigureRaises(),
        "return_mismatch": _FakeAdapter(configured_as="gpu"),
        "fingerprint_bad": _FakeAdapter(record_evidence_version=False),
    }
    adapter = adapters[case]

    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(runner.registry, "build_adapter", lambda _profile: adapter)
    monkeypatch.setattr(
        runner,
        "publication_preflight",
        lambda **_kw: runner.PreflightContext(
            git={"commit": "a" * 40, "dirty": False},
            system={"python": "3", "os": "x", "cpu": "cpu", "gpu": None, "ram_bytes": 1},
            dependencies={},
            documents=(verified_doc,),
            dataset_manifest_path=manifest,
            dataset_manifest_sha256=_sha(manifest.read_bytes()),
        ),
    )
    out = tmp_path / "out"

    assert (
        runner.main(
            ["--dataset-manifest", str(manifest), "--out", str(out)]
        )
        == 2
    )
    assert adapter.execute_count == 0
    assert not (out / "run-manifest.json").exists()
    assert not (out / "prediction").exists()


def test_all_adapters_are_configured_once_before_run_manifest(
    tmp_path, monkeypatch
):
    runner = _load_script()
    default = _profile()
    scan = _profile("marker_scan", force_ocr=True)
    catalog = {default.name: default, scan.name: scan}
    manifest = _dataset_manifest(tmp_path / "manifest.json", [])

    class BoundAdapter(_FakeAdapter):
        def __init__(self, profile):
            super().__init__()
            self.profile = profile

        def config_fingerprint(self):
            fingerprint = dict(self.profile.config)
            if self.effective_hardware is not None:
                fingerprint.update(
                    hardware=self.effective_hardware,
                    device=self.effective_hardware,
                    hardware_evidence_version=1,
                )
            return fingerprint

    adapters = {name: BoundAdapter(profile) for name, profile in catalog.items()}
    snapshots: list[dict[str, list[str]]] = []
    real_write_manifest = runner._write_manifest

    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: catalog)
    monkeypatch.setattr(
        runner.registry,
        "build_adapter",
        lambda profile: adapters[profile.name],
    )
    monkeypatch.setattr(
        runner,
        "publication_preflight",
        lambda **_kw: runner.PreflightContext(
            git={"commit": "a" * 40, "dirty": False},
            system={"python": "3", "os": "x", "cpu": "cpu", "gpu": None, "ram_bytes": 1},
            dependencies={},
            documents=(),
            dataset_manifest_path=manifest,
            dataset_manifest_sha256=_sha(manifest.read_bytes()),
        ),
    )

    def observe_write(path, payload):
        snapshots.append({name: list(adapter.events) for name, adapter in adapters.items()})
        real_write_manifest(path, payload)

    monkeypatch.setattr(runner, "_write_manifest", observe_write)

    assert (
        runner.main(
            ["--dataset-manifest", str(manifest), "--out", str(tmp_path / "out")]
        )
        == 0
    )
    expected = {name: ["configure:cpu"] for name in catalog}
    assert snapshots == [expected]
    assert {name: adapter.events for name, adapter in adapters.items()} == expected


def test_publication_profile_order_is_catalog_order_for_every_cli_order():
    from ocr_bench.preflight import verify_profile_selection

    scan = _profile("marker_scan", force_ocr=True)
    default = _profile()
    catalog = {scan.name: scan, default.name: default}

    first = verify_profile_selection(
        catalog, [default.name, scan.name], mode="publication"
    )
    second = verify_profile_selection(
        catalog, [scan.name, default.name], mode="publication"
    )

    assert list(first) == list(second) == [scan.name, default.name]


def test_cli_orders_execution_and_manifest_by_catalog_for_two_cli_orders(
    tmp_path, monkeypatch
):
    from ocr_bench.preflight import DatasetDocument

    runner = _load_script()
    scan = _profile("marker_scan", force_ocr=True)
    default = _profile()
    catalog = {scan.name: scan, default.name: default}
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    manifest = _dataset_manifest(tmp_path / "manifest.json", [])
    verified_doc = DatasetDocument(doc.stem, doc, _sha(doc.read_bytes()))
    executions: list[str] = []

    class OrderedAdapter(_FakeAdapter):
        def __init__(self, profile):
            super().__init__()
            self.bound_profile = profile
            self.name = profile.name

        def config_fingerprint(self):
            fingerprint = dict(self.bound_profile.config)
            if self.effective_hardware is not None:
                fingerprint.update(
                    hardware=self.effective_hardware,
                    device=self.effective_hardware,
                    hardware_evidence_version=1,
                )
            return fingerprint

        def execute(self, path):
            executions.append(self.name)
            return OcrResult(
                engine=self.name,
                engine_family=self.bound_profile.family,
                profile=self.bound_profile.profile,
                engine_version=self.version(),
                doc_id=path.stem,
                capabilities=self.capabilities,
                text_md="ok",
                seconds=1.0,
                peak_rss_mb=2.0,
                rss_scope="process",
                config_fingerprint=self.config_fingerprint(),
            )

    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: catalog)
    monkeypatch.setattr(runner.registry, "build_adapter", OrderedAdapter)
    monkeypatch.setattr(
        runner,
        "publication_preflight",
        lambda **_kw: runner.PreflightContext(
            git={"commit": "a" * 40, "dirty": False},
            system={"python": "3", "os": "x", "cpu": "cpu", "gpu": None, "ram_bytes": 1},
            dependencies={},
            documents=(verified_doc,),
            dataset_manifest_path=manifest,
            dataset_manifest_sha256=_sha(manifest.read_bytes()),
        ),
    )

    manifests = []
    for index, order in enumerate(
        ([default.name, scan.name], [scan.name, default.name])
    ):
        executions.clear()
        out = tmp_path / f"run-{index}"
        assert (
            runner.main(
                [
                    "--profiles",
                    ",".join(order),
                    "--dataset-manifest",
                    str(manifest),
                    "--out",
                    str(out),
                ]
            )
            == 0
        )
        assert executions == [scan.name, default.name]
        payload = json.loads((out / "run-manifest.json").read_text(encoding="utf-8"))
        payload["generated_at"] = "ignored"
        manifests.append(payload)

    assert manifests[0] == manifests[1]
    assert [row["name"] for row in manifests[0]["profiles"]] == [
        scan.name,
        default.name,
    ]


def test_cpu_probe_does_not_turn_missing_identity_into_unknown(monkeypatch):
    import ocr_bench.preflight as preflight

    monkeypatch.setattr(preflight.platform, "processor", lambda: "")
    monkeypatch.delenv("PROCESSOR_IDENTIFIER", raising=False)
    monkeypatch.setattr(preflight, "_gpu_name", lambda: None)
    monkeypatch.setattr(preflight, "_ram_bytes", lambda: 1024)

    assert preflight.collect_system_metadata()["cpu"] is None


def test_ram_probe_works_on_the_machine_that_will_run_the_publication():
    """`ram_bytes` phải đo được **ở đây**, không chỉ ở nơi có psutil.

    `publication_preflight` chặn khi thiếu CPU/RAM. Trước đó hai nhánh duy nhất là psutil
    và `os.sysconf` — psutil không nằm trong dependency, `os.sysconf` không tồn tại trên
    Windows, nên trên máy chạy bench này mọi lần công bố đều bị chặn bởi một khiếm khuyết
    của *đầu dò*, không phải của môi trường. Lỗi đó nấp được lâu vì một cổng phía trước
    (`datasets/manifest.json` chưa tồn tại) đỏ trước và che mất.
    """
    import ocr_bench.preflight as preflight

    ram = preflight.collect_system_metadata()["ram_bytes"]
    assert isinstance(ram, int)
    # Chặn cả 0 lẫn giá trị vô lý: một API trả 0 vì gọi sai vẫn là "có số".
    assert ram > 1 << 30


def test_ram_probe_reports_nothing_rather_than_guessing(monkeypatch):
    """Không đo được thì trả `None` để cổng chặn — không bịa một con số mặc định."""
    import ocr_bench.preflight as preflight

    monkeypatch.setitem(sys.modules, "psutil", None)  # import psutil -> ImportError
    monkeypatch.delattr(preflight.os, "sysconf", raising=False)
    monkeypatch.setattr(preflight, "_ram_bytes_windows", lambda: None)

    assert preflight._ram_bytes() is None


@pytest.mark.parametrize(
    "hardware,system,match",
    [
        (
            "gpu",
            {"python": "3", "os": "x", "cpu": "cpu", "gpu": None, "ram_bytes": 1},
            "GPU",
        ),
        (
            "cpu",
            {"python": "3", "os": "x", "cpu": None, "gpu": None, "ram_bytes": 1},
            "CPU",
        ),
    ],
)
def test_publication_preflight_rejects_unavailable_hardware_identity(
    tmp_path, monkeypatch, hardware, system, match
):
    import ocr_bench.preflight as preflight

    doc = tmp_path / "doc.pdf"
    doc.write_bytes(b"%PDF")
    verified = preflight.DatasetDocument("doc", doc, _sha(doc.read_bytes()))
    manifest = _dataset_manifest(tmp_path / "manifest.json", [])
    verified_dataset = preflight.VerifiedDataset(
        (verified,), _sha(manifest.read_bytes()), False
    )
    monkeypatch.setattr(
        preflight,
        "collect_git_metadata",
        lambda *_args, **_kw: {"commit": "a" * 40, "dirty": False},
    )

    with pytest.raises(preflight.PreflightError, match=match):
        preflight.publication_preflight(
            repo_root=tmp_path,
            dataset_manifest=manifest,
            hardware=hardware,
            dataset_validator=lambda *_args: verified_dataset,
            system_probe=lambda: system,
            dependency_probe=lambda: {},
        )


def test_cpu_mask_is_applied_before_adapter_construction(tmp_path, monkeypatch):
    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    manifest = _dataset_manifest(
        tmp_path / "manifest.json",
        [
            {
                "document_id": doc.stem,
                "pdf_path": str(doc.relative_to(tmp_path)),
                "pdf_sha256": _sha(doc.read_bytes()),
            }
        ],
    )
    adapter = _FakeAdapter()
    observed: dict[str, str | None] = {}

    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(
        runner,
        "publication_preflight",
        lambda **_kw: runner.PreflightContext(
            git={"commit": "a" * 40, "dirty": False},
            system={"python": "3", "os": "x", "cpu": "cpu", "gpu": None, "ram_bytes": 1},
            dependencies={},
            documents=(),
            dataset_manifest_path=manifest,
            dataset_manifest_sha256=_sha(manifest.read_bytes()),
        ),
    )

    def build(_profile):
        observed["hardware"] = os.environ.get("OCR_BENCH_HARDWARE")
        observed["cuda"] = os.environ.get("CUDA_VISIBLE_DEVICES")
        return adapter

    monkeypatch.setattr(runner.registry, "build_adapter", build)
    monkeypatch.setattr(runner, "discover_documents", lambda *_args, **_kw: [doc])

    assert runner.main(["--dataset-manifest", str(manifest), "--out", str(tmp_path / "out")]) == 0
    assert observed == {"hardware": "cpu", "cuda": ""}


# --------------------------------------------------------------------------
# Năng lực nằm trong khoá cache — sửa adapter phải làm cache cũ hết hạn
# --------------------------------------------------------------------------


def test_capabilities_nam_trong_khoa_cache(tmp_path):
    """Thiếu trường này thì thêm năng lực cho adapter là một thay đổi *im lặng*.

    Ca thật 2026-08-13: docling/pdf_inspector được sửa để khai `IMAGE_BBOX`, nhưng
    1648 dự đoán đã cache vẫn không có `images[]` và `img_f1` vẫn trả
    `MISSING_CAPABILITY` — không có gì báo rằng bản sửa chưa có hiệu lực.
    """
    from ocr_bench.preflight import build_cache_identity

    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    chung = dict(engine_version="1.0.0", hardware="cpu")

    hep = build_cache_identity(
        doc, _profile(), capabilities=frozenset({Capability.TEXT_MD}), **chung
    )
    rong = build_cache_identity(
        doc,
        _profile(),
        capabilities=frozenset({Capability.TEXT_MD, Capability.IMAGE_BBOX}),
        **chung,
    )
    assert hep != rong
    assert hep["capabilities"] == "text_md"


def test_khoa_cache_khong_phu_thuoc_thu_tu_nang_luc(tmp_path):
    """`frozenset` không có thứ tự — khoá phải ổn định giữa hai lần chạy."""
    from ocr_bench.preflight import build_cache_identity

    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    caps = (Capability.IMAGE_BBOX, Capability.TEXT_MD, Capability.BLOCK_BBOX)
    chung = dict(engine_version="1.0.0", hardware="cpu")

    a = build_cache_identity(doc, _profile(), capabilities=frozenset(caps), **chung)
    b = build_cache_identity(
        doc, _profile(), capabilities=frozenset(reversed(caps)), **chung
    )
    assert a == b
    assert a["capabilities"] == "block_bbox,image_bbox,text_md"


def test_cache_cu_khong_co_capabilities_bi_tu_choi():
    """Corpus cũ phải bị coi là hết hạn, không được dùng lại im lặng."""
    from ocr_bench import preflight
    from ocr_bench.preflight import PreflightError, verify_cached_identity

    expected = {"doc_id": "d", "capabilities": "image_bbox,text_md"}
    cu = {preflight.CACHE_IDENTITY_KEY: {"doc_id": "d"}}

    with pytest.raises(PreflightError, match="capabilities"):
        verify_cached_identity(_profile(), cu, expected)
