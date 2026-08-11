"""Behavioral tests for the local OpenDataLoader hybrid launcher."""

from __future__ import annotations

import importlib.util
import ast
import json
import tomllib
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {
    "docling": "2.91.0",
    "easyocr": "1.7.2",
    "fastapi": "0.136.1",
    "opendataloader-pdf": "2.5.0",
    "packaging": "25.0",
    "pypdf": "5.0.0",
    "psutil": "7.0.0",
    "python-multipart": "0.0.28",
    "uvicorn": "0.46.0",
}


def _launcher():
    path = ROOT / "scripts" / "run_odl_hybrid.py"
    spec = importlib.util.spec_from_file_location("run_odl_hybrid", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakePsProcess:
    def __init__(self, pid, *, create_time=1234.5, children=(), connections=()):
        self.pid = pid
        self._create_time = create_time
        self._children = list(children)
        self._connections = list(connections)

    def create_time(self):
        return self._create_time

    def children(self, recursive=False):
        assert recursive is True
        return list(self._children)

    def net_connections(self, kind="inet"):
        assert kind == "inet"
        return list(self._connections)

    def is_running(self):
        return True


def _connection(pid, host="127.0.0.1", port=5002):
    return SimpleNamespace(pid=pid, laddr=(host, port), status="LISTEN")


def _fake_psutil(root, *children):
    processes = {process.pid: process for process in (root, *children)}
    return SimpleNamespace(
        CONN_LISTEN="LISTEN",
        Process=lambda pid: processes[pid],
    )


def _ok_report():
    return {"missing": [], "incompatible": [], "versions": dict(VERSIONS)}


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


def test_check_only_rejects_missing_and_incompatible_versions(monkeypatch, capsys):
    module = _launcher()
    installed = dict(VERSIONS)
    installed.update(
        {
            "easyocr": "1.6.0",
            "fastapi": "0.100.0",
            "opendataloader-pdf": "2.5.1",
            "pypdf": "4.9.0",
        }
    )
    installed.pop("python-multipart")
    monkeypatch.setattr(module, "_distribution_version", installed.get)

    assert module.main(["--check-only"]) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["missing"] == ["python-multipart>=0.0.28"]
    assert output["incompatible"] == [
        {
            "installed": "1.6.0",
            "requirement": "easyocr>=1.7,<2",
        },
        {
            "installed": "0.100.0",
            "requirement": "fastapi>=0.136.1",
        },
        {
            "installed": "2.5.1",
            "requirement": "opendataloader-pdf[hybrid]==2.5.0",
        },
        {
            "installed": "4.9.0",
            "requirement": "pypdf>=5",
        },
    ]
    assert output["versions"]["easyocr"] == "1.6.0"


def test_check_only_reports_missing_packaging_and_psutil_without_crashing(
    monkeypatch, capsys
):
    module = _launcher()
    installed = dict(VERSIONS)
    installed.pop("packaging")
    installed.pop("psutil")
    monkeypatch.setattr(module, "_distribution_version", installed.get)

    assert module.main(["--check-only"]) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["missing"] == ["packaging>=23", "psutil>=5"]
    assert output["incompatible"] == []


def test_check_only_rejects_too_old_packaging_before_version_parser_use(
    monkeypatch, capsys
):
    module = _launcher()
    installed = dict(VERSIONS, packaging="22.0")
    monkeypatch.setattr(module, "_distribution_version", installed.get)

    assert module.main(["--check-only"]) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["incompatible"] == [
        {"installed": "22.0", "requirement": "packaging>=23"}
    ]


def test_hybrid_extra_and_launcher_bootstrap_do_not_assume_packaging_installed():
    extra = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]["optional-dependencies"]["opendataloader-hybrid"]
    assert "easyocr>=1.7,<2" in extra
    assert "packaging>=23" in extra
    assert "psutil>=5" in extra

    tree = ast.parse((ROOT / "scripts" / "run_odl_hybrid.py").read_text(encoding="utf-8"))
    top_level_packaging_imports = [
        node
        for node in tree.body
        if isinstance(node, ast.ImportFrom) and node.module.startswith("packaging")
    ]
    assert top_level_packaging_imports == []


def test_stale_healthy_server_is_refused_before_spawn(monkeypatch, tmp_path):
    module = _launcher()
    monkeypatch.setattr(module, "dependency_report", _ok_report)
    monkeypatch.setattr(module, "_load_psutil", lambda: SimpleNamespace())
    monkeypatch.setattr(module, "_health_payload", lambda *_args, **_kwargs: {"status": "ok"})
    spawned = False

    def forbidden_spawn(*_args, **_kwargs):
        nonlocal spawned
        spawned = True
        raise AssertionError("must reject stale listener before Popen")

    monkeypatch.setattr(module.subprocess, "Popen", forbidden_spawn)

    assert module.main(["--manifest", str(tmp_path / "manifest.json")]) == 2
    assert spawned is False


def test_listener_ownership_accepts_child_and_rejects_foreign_process():
    module = _launcher()
    child = FakePsProcess(4243, connections=[_connection(4243)])
    root = FakePsProcess(4242, children=[child])
    psutil = _fake_psutil(root, child)

    assert module.listener_pids_owned_by_tree(
        psutil, pid=4242, host="127.0.0.1", port=5002
    ) == [4243]

    foreign = FakePsProcess(9999, connections=[_connection(9999)])
    with pytest.raises(RuntimeError, match="owned"):
        module.require_owned_listener(
            _fake_psutil(root, child, foreign),
            pid=4242,
            host="127.0.0.1",
            port=5002,
            observed_listener_pids=[9999],
        )


def test_owned_ready_server_exposes_manifest_then_removes_it_on_cleanup(
    monkeypatch, tmp_path, capsys
):
    module = _launcher()

    class FakeProcess:
        pid = 4242

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

    child = FakePsProcess(4243, connections=[_connection(4243)])
    root = FakePsProcess(4242, children=[child])
    psutil = _fake_psutil(root, child)
    process = FakeProcess()
    monkeypatch.setattr(module, "dependency_report", _ok_report)
    monkeypatch.setattr(module, "_load_psutil", lambda: psutil)
    monkeypatch.setattr(module, "ensure_endpoint_free", lambda **_kwargs: None)
    monkeypatch.setattr(module, "_health_payload", lambda *_args, **_kwargs: {"status": "ok"})
    spawned = {}

    def fake_popen(command, *, env):
        spawned["command"] = command
        spawned["env"] = env
        return process

    monkeypatch.setattr(module.subprocess, "Popen", fake_popen)
    manifest = tmp_path / "run-manifest.json"
    active = {}

    def inspect_while_active(_process):
        active["raw"] = manifest.read_bytes()

    monkeypatch.setattr(module, "serve_until_interrupted", inspect_while_active)
    monkeypatch.delenv(module.MANIFEST_ENV, raising=False)

    assert module.main(["--manifest", str(manifest)]) == 0
    raw = active["raw"]
    payload = json.loads(raw)
    assert raw == (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    assert payload["manifest_schema_version"] == 1
    assert payload["launcher_version"] == 1
    assert payload["pid"] == 4242
    assert payload["process_create_time"] == 1234.5
    assert payload["listener_pids"] == [4243]
    assert payload["host"] == "127.0.0.1"
    assert payload["port"] == 5002
    assert payload["url"] == "http://127.0.0.1:5002"
    assert payload["config"] == module.server_config()
    assert payload["config"]["device_enforcement_method"] == (
        "CUDA_VISIBLE_DEVICES-empty-before-spawn"
    )
    assert payload["versions"] == VERSIONS
    assert len(payload["run_id"]) == 64
    assert spawned["env"]["CUDA_VISIBLE_DEVICES"] == ""
    output = capsys.readouterr().out
    assert str(manifest.resolve()) in output
    assert f"$env:{module.MANIFEST_ENV}" in output
    assert module.MANIFEST_ENV not in module.os.environ
    assert not manifest.exists()
    assert process.terminated and process.waited


def test_manifest_path_precedence_supports_cross_process_default_and_overrides(
    monkeypatch, tmp_path
):
    module = _launcher()
    default = tmp_path / "build" / "odl-hybrid" / "manifest.json"
    environment = tmp_path / "environment.json"
    cli = tmp_path / "cli.json"
    monkeypatch.setattr(module, "DEFAULT_MANIFEST_PATH", default)
    monkeypatch.delenv(module.MANIFEST_ENV, raising=False)

    assert module.resolve_manifest_path(None) == default.resolve()
    monkeypatch.setenv(module.MANIFEST_ENV, str(environment))
    assert module.resolve_manifest_path(None) == environment.resolve()
    assert module.resolve_manifest_path(cli) == cli.resolve()
