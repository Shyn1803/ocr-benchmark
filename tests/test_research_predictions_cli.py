"""Publication runner must fail closed before spending time on OCR engines."""

from __future__ import annotations

import importlib.util
import json
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

    def __init__(self) -> None:
        self.execute_count = 0

    def version(self) -> str:
        return "fake-1"

    def config_fingerprint(self) -> dict[str, object]:
        return {"force_ocr": False, "use_llm": False}

    def execute(self, doc: Path) -> OcrResult:
        self.execute_count += 1
        return OcrResult(
            engine=self.name,
            engine_family="marker",
            profile="default",
            engine_version=self.version(),
            doc_id=doc.stem,
            capabilities=self.capabilities,
            text_md="ok",
            config_fingerprint=self.config_fingerprint(),
        )


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
        generated_at="2026-08-11T00:00:00Z",
        **fixed,
    )
    second = build_run_manifest(
        mode="publication",
        hardware="cpu",
        profiles={profile.name: profile},
        dataset_manifest=manifest,
        generated_at="later",
        **fixed,
    )

    assert first | {"generated_at": "later"} == second
    assert first["profiles"] == {profile.name: profile.fingerprint}
    assert first["dataset_manifest"]["sha256"] == (
        "c5c0225cf54a86b0e729ca91a74107ab9fefb5cc84a8819a6d5a3cf40b732345"
    )
    serialized = json.dumps(first, sort_keys=True)
    assert "secret" not in serialized.lower()
