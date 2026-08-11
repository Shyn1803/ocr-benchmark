"""Start the locked, locally-owned OpenDataLoader hybrid server."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Sequence

from packaging.specifiers import SpecifierSet
from packaging.version import InvalidVersion, Version


HOST = "127.0.0.1"
PORT = 5002
READINESS_TIMEOUT_SECONDS = 120.0
MANIFEST_ENV = "OCR_BENCH_ODL_HYBRID_MANIFEST"
MANIFEST_SCHEMA_VERSION = 1
LAUNCHER_VERSION = 1

# distribution, accepted versions, user-facing locked requirement
REQUIREMENTS = (
    ("docling", ">=2.91.0", "docling>=2.91.0"),
    ("easyocr", ">=0", "easyocr (required by docling[easyocr])"),
    ("fastapi", ">=0.136.1", "fastapi>=0.136.1"),
    (
        "opendataloader-pdf",
        "==2.5.0",
        "opendataloader-pdf[hybrid]==2.5.0",
    ),
    ("pypdf", ">=5", "pypdf>=5"),
    ("python-multipart", ">=0.0.28", "python-multipart>=0.0.28"),
    ("uvicorn", ">=0.46.0", "uvicorn>=0.46.0"),
)


def _distribution_version(name: str) -> str | None:
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def dependency_report() -> dict[str, object]:
    """Resolve and validate every dependency required by the publication server."""
    versions: dict[str, str] = {}
    missing: list[str] = []
    incompatible: list[dict[str, str]] = []
    for distribution, specifier, requirement in REQUIREMENTS:
        installed = _distribution_version(distribution)
        if installed is None:
            missing.append(requirement)
            continue
        versions[distribution] = installed
        try:
            accepted = Version(installed) in SpecifierSet(specifier)
        except InvalidVersion:
            accepted = False
        if not accepted:
            incompatible.append(
                {"installed": installed, "requirement": requirement}
            )
    return {
        "missing": sorted(missing),
        "incompatible": sorted(incompatible, key=lambda item: item["requirement"]),
        "versions": dict(sorted(versions.items())),
    }


def server_config(*, host: str = HOST, port: int = PORT) -> dict[str, object]:
    if host != HOST:
        raise ValueError("hybrid server must bind exactly 127.0.0.1")
    if port != PORT:
        raise ValueError("hybrid server must use catalog port 5002")
    return {
        "device": "cpu",
        "device_enforcement": {"CUDA_VISIBLE_DEVICES": ""},
        "device_enforcement_method": "CUDA_VISIBLE_DEVICES-empty-before-spawn",
        "force_ocr": True,
        "health_url": f"http://{host}:{port}/health",
        "host": host,
        "ocr_engine": "easyocr",
        "ocr_languages": ["vi", "en"],
        "port": port,
    }


def build_server_command(python: Path) -> list[str]:
    """Use only flags actually exposed by OpenDataLoader 2.5.0."""
    config = server_config()
    return [
        str(python),
        "-m",
        "opendataloader_pdf.hybrid_server",
        "--host",
        str(config["host"]),
        "--port",
        str(config["port"]),
        "--force-ocr",
        "--ocr-engine",
        str(config["ocr_engine"]),
        "--ocr-lang",
        ",".join(config["ocr_languages"]),
    ]


def _load_psutil() -> Any:
    try:
        import psutil  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError(
            "psutil is required to prove hybrid listener process ownership"
        ) from exc
    return psutil


def _health_payload(url: str, *, timeout: float = 0.5) -> object | None:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return json.loads(response.read())
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return None


def ensure_endpoint_free(*, host: str, port: int) -> None:
    """Refuse stale/foreign services before creating our child process."""
    url = f"http://{host}:{port}/health"
    if _health_payload(url) is not None:
        raise RuntimeError(f"hybrid endpoint is already healthy/occupied: {url}")
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.bind((host, port))
    except OSError as exc:
        raise RuntimeError(f"hybrid endpoint is already occupied: {host}:{port}") from exc
    finally:
        probe.close()


def _connection_address(connection: object) -> tuple[str, int] | None:
    address = getattr(connection, "laddr", None)
    if not address:
        return None
    try:
        return str(address[0]), int(address[1])
    except (IndexError, TypeError, ValueError):
        return None


def listener_pids_owned_by_tree(
    psutil: Any, *, pid: int, host: str, port: int
) -> list[int]:
    root = psutil.Process(pid)
    processes = [root, *root.children(recursive=True)]
    owned: set[int] = set()
    listen_status = getattr(psutil, "CONN_LISTEN", "LISTEN")
    for process in processes:
        for connection in process.net_connections(kind="inet"):
            if (
                getattr(connection, "status", None) == listen_status
                and _connection_address(connection) == (host, port)
            ):
                owned.add(int(process.pid))
    return sorted(owned)


def require_owned_listener(
    psutil: Any,
    *,
    pid: int,
    host: str,
    port: int,
    observed_listener_pids: Sequence[int],
) -> list[int]:
    owned = listener_pids_owned_by_tree(psutil, pid=pid, host=host, port=port)
    observed = sorted({int(item) for item in observed_listener_pids})
    if not owned or observed != owned:
        raise RuntimeError(
            f"listener is not exclusively owned by child process tree: "
            f"owned={owned}, observed={observed}"
        )
    return owned


def wait_until_ready(
    *,
    process: subprocess.Popen[bytes],
    url: str,
    host: str,
    port: int,
    psutil: Any,
    timeout: float = READINESS_TIMEOUT_SECONDS,
) -> tuple[dict[str, object], list[int]]:
    deadline = time.monotonic() + timeout
    last_error = "no response"
    while time.monotonic() < deadline:
        return_code = process.poll()
        if return_code is not None:
            raise RuntimeError(
                f"hybrid server exited before readiness (exit {return_code})"
            )
        payload = _health_payload(url, timeout=2.0)
        if payload == {"status": "ok"}:
            try:
                owned = listener_pids_owned_by_tree(
                    psutil, pid=process.pid, host=host, port=port
                )
            except Exception as exc:  # psutil has platform-specific error classes
                last_error = f"listener ownership unavailable: {exc}"
            else:
                if owned:
                    return payload, owned
                last_error = "healthy endpoint has no listener owned by child tree"
        elif payload is not None:
            last_error = f"unexpected health payload: {payload!r}"
        time.sleep(0.25)
    raise TimeoutError(f"hybrid server not ready after {timeout:.0f}s: {last_error}")


def _canonical_bytes(payload: object) -> bytes:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _write_manifest(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical_bytes(payload))


def serve_until_interrupted(process: subprocess.Popen[bytes]) -> None:
    try:
        process.wait()
    except KeyboardInterrupt:
        return


def _stop_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=10)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--manifest", type=Path, default=Path("run-manifest.json"))
    args = parser.parse_args(argv)

    report = dependency_report()
    invalid = bool(report["missing"] or report["incompatible"])
    if args.check_only:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 2 if invalid else 0
    if invalid:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2

    try:
        config = server_config(host=args.host, port=args.port)
        psutil = _load_psutil()
        ensure_endpoint_free(host=args.host, port=args.port)
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    command = build_server_command(Path(sys.executable).resolve())
    child_env = os.environ.copy()
    child_env["CUDA_VISIBLE_DEVICES"] = ""
    process = subprocess.Popen(command, env=child_env)
    try:
        health, listener_pids = wait_until_ready(
            process=process,
            url=str(config["health_url"]),
            host=args.host,
            port=args.port,
            psutil=psutil,
        )
        process_create_time = float(psutil.Process(process.pid).create_time())
        payload: dict[str, object] = {
            "argv": command,
            "config": config,
            "health": health,
            "host": args.host,
            "launcher_version": LAUNCHER_VERSION,
            "listener_pids": listener_pids,
            "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
            "pid": int(process.pid),
            "port": args.port,
            "process_create_time": process_create_time,
            "url": f"http://{args.host}:{args.port}",
            "versions": report["versions"],
        }
        payload["run_id"] = hashlib.sha256(_canonical_bytes(payload)).hexdigest()
        manifest = args.manifest.resolve()
        _write_manifest(manifest, payload)
        os.environ[MANIFEST_ENV] = str(manifest)
        serve_until_interrupted(process)
        return process.poll() or 0
    finally:
        _stop_process(process)


if __name__ == "__main__":
    raise SystemExit(main())
