"""Behavioral tests for the local OpenDataLoader hybrid launcher."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _launcher():
    path = ROOT / "scripts" / "run_odl_hybrid.py"
    spec = importlib.util.spec_from_file_location("run_odl_hybrid", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_hybrid_command_is_loopback_forced_ocr_easyocr_vietnamese_english():
    module = _launcher()
    command = module.build_server_command(Path("python.exe"))

    assert command == [
        "python.exe", "-m", "opendataloader_pdf.hybrid_server",
        "--host", "127.0.0.1", "--port", "5002", "--force-ocr",
        "--ocr-engine", "easyocr", "--ocr-lang", "vi,en",
    ]


def test_hybrid_launcher_rejects_public_bind():
    module = _launcher()
    with pytest.raises(ValueError, match="127.0.0.1"):
        module.server_config(host="0.0.0.0", port=5002)


def test_check_only_reports_exact_missing_dependencies(monkeypatch, capsys):
    module = _launcher()
    monkeypatch.setattr(
        module,
        "dependency_report",
        lambda: {"missing": ["docling[easyocr]", "python-multipart"], "versions": {"opendataloader-pdf": "2.5.0"}},
    )

    assert module.main(["--check-only"]) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["missing"] == ["docling[easyocr]", "python-multipart"]


def test_ready_server_writes_deterministic_manifest_and_is_cleaned_up(monkeypatch, tmp_path):
    module = _launcher()

    class FakeProcess:
        def __init__(self):
            self.terminated = False
            self.waited = False

        def poll(self):
            return None

        def terminate(self):
            self.terminated = True

        def wait(self, timeout=None):
            self.waited = True
            return 0

    process = FakeProcess()
    monkeypatch.setattr(module, "dependency_report", lambda: {"missing": [], "versions": {"opendataloader-pdf": "2.5.0", "docling": "2.91.0"}})
    spawned = {}

    def fake_popen(command, *, env):
        spawned["command"] = command
        spawned["env"] = env
        return process

    monkeypatch.setattr(module.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(module, "wait_until_ready", lambda **kwargs: {"status": "ok"})
    monkeypatch.setattr(module, "serve_until_interrupted", lambda _process: None)
    manifest = tmp_path / "run-manifest.json"

    assert module.main(["--manifest", str(manifest)]) == 0
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["server_config"] == module.server_config(host="127.0.0.1", port=5002)
    assert payload["versions"]["opendataloader-pdf"] == "2.5.0"
    assert payload["health"] == {"status": "ok"}
    assert spawned["env"]["CUDA_VISIBLE_DEVICES"] == ""
    assert process.terminated and process.waited
