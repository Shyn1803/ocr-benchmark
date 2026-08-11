"""Executable preflight contract for the frozen Sovereign profiles."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "preflight_sovereign.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("preflight_sovereign", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_preflight_script_emits_deterministic_safe_payload(monkeypatch, capsys):
    script = _load_script()

    class FakeAdapter:
        name = "sovereign_default"

        def configure_hardware(self, hardware):
            assert hardware == "cpu"
            return "cpu"

        def config_fingerprint(self):
            return {
                "hardware": "cpu",
                "device": "cpu",
                "hardware_evidence_version": 1,
                "api_enabled": False,
            }

    monkeypatch.setattr(
        script.SovereignAdapter,
        "from_profile",
        classmethod(lambda cls, profile: FakeAdapter()),
    )

    assert script.main(["sovereign_default", "--hardware", "cpu"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "fingerprint": {
            "api_enabled": False,
            "device": "cpu",
            "hardware": "cpu",
            "hardware_evidence_version": 1,
        },
        "profile": "sovereign_default",
        "status": "ok",
    }


def test_preflight_script_redacts_seeded_secret_on_failure(monkeypatch, capsys):
    script = _load_script()
    secret = "seeded-openrouter-value-789"
    monkeypatch.setenv("OPENROUTER_API_KEY", secret)

    class FailingAdapter:
        def configure_hardware(self, _hardware):
            raise RuntimeError(f"unsafe {secret}")

    monkeypatch.setattr(
        script.SovereignAdapter,
        "from_profile",
        classmethod(lambda cls, profile: FailingAdapter()),
    )

    assert script.main(["sovereign_default"]) == 2
    output = capsys.readouterr()
    assert secret not in output.out
    assert secret not in output.err
    assert "<redacted>" in output.err


def test_preflight_script_rejects_gpu_before_document_execution(monkeypatch, capsys):
    script = _load_script()
    configured = False

    class FakeAdapter:
        def configure_hardware(self, hardware):
            nonlocal configured
            configured = True
            raise RuntimeError(f"GPU {hardware} cannot be verified")

    monkeypatch.setattr(
        script.SovereignAdapter,
        "from_profile",
        classmethod(lambda cls, profile: FakeAdapter()),
    )

    assert script.main(["sovereign_scan", "--hardware", "gpu"]) == 2
    assert configured is True
    assert "GPU" in capsys.readouterr().err
