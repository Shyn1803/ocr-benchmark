"""Start the locked local OpenDataLoader hybrid server for scan publication."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Sequence


HOST = "127.0.0.1"
PORT = 5002
READINESS_TIMEOUT_SECONDS = 120.0


def _distribution_version(name: str) -> str | None:
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def dependency_report() -> dict[str, object]:
    """Return exact missing requirements and the versions used as evidence."""
    versions = {
        name: found
        for name in (
            "opendataloader-pdf",
            "docling",
            "easyocr",
            "fastapi",
            "python-multipart",
            "uvicorn",
            "pypdf",
        )
        if (found := _distribution_version(name)) is not None
    }
    missing: list[str] = []
    if versions.get("opendataloader-pdf") != "2.5.0":
        missing.append("opendataloader-pdf==2.5.0")
    if "docling" not in versions or "easyocr" not in versions:
        missing.append("docling[easyocr]")
    for distribution in ("fastapi", "python-multipart", "uvicorn"):
        if distribution not in versions:
            missing.append(distribution)
    if "pypdf" not in versions:
        missing.append("pypdf>=5")
    return {"missing": missing, "versions": versions}


def server_config(*, host: str = HOST, port: int = PORT) -> dict[str, object]:
    """Build and validate the catalog-locked local server configuration."""
    if host != HOST:
        raise ValueError("hybrid server must bind exactly 127.0.0.1")
    if port != PORT:
        raise ValueError("hybrid server must use catalog port 5002")
    return {
        "device": "cpu",
        "device_enforcement": {"CUDA_VISIBLE_DEVICES": ""},
        "force_ocr": True,
        "health_url": f"http://{host}:{port}/health",
        "host": host,
        "ocr_engine": "easyocr",
        "ocr_languages": ["vi", "en"],
        "port": port,
    }


def build_server_command(python: Path) -> list[str]:
    """Use the current venv interpreter and only the 2.5.0 documented flags."""
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


def wait_until_ready(
    *,
    process: subprocess.Popen[bytes],
    url: str,
    timeout: float = READINESS_TIMEOUT_SECONDS,
) -> dict[str, object]:
    """Poll the local health endpoint and fail if startup exits or times out."""
    deadline = time.monotonic() + timeout
    last_error = "no response"
    while time.monotonic() < deadline:
        return_code = process.poll()
        if return_code is not None:
            raise RuntimeError(
                f"hybrid server exited before readiness (exit {return_code})"
            )
        try:
            with urllib.request.urlopen(url, timeout=2.0) as response:
                payload = json.loads(response.read())
            if payload == {"status": "ok"}:
                return payload
            last_error = f"unexpected health payload: {payload!r}"
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            last_error = str(exc)
        time.sleep(0.25)
    raise TimeoutError(
        f"hybrid server not ready after {timeout:.0f}s: {last_error}"
    )


def _write_manifest(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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
    if args.check_only:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 2 if report["missing"] else 0
    if report["missing"]:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2

    try:
        config = server_config(host=args.host, port=args.port)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    command = build_server_command(Path(sys.executable))
    child_env = os.environ.copy()
    child_env["CUDA_VISIBLE_DEVICES"] = ""
    process = subprocess.Popen(command, env=child_env)
    try:
        health = wait_until_ready(
            process=process,
            url=str(config["health_url"]),
        )
        _write_manifest(
            args.manifest,
            {
                "command": command,
                "health": health,
                "manifest_schema_version": 1,
                "server_config": config,
                "versions": report["versions"],
            },
        )
        serve_until_interrupted(process)
        return process.poll() or 0
    finally:
        _stop_process(process)


if __name__ == "__main__":
    raise SystemExit(main())
