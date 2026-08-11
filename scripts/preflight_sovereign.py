#!/usr/bin/env python3
"""Fail-closed, document-free preflight for frozen Sovereign profiles."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Sequence

from ocr_bench.adapters.sovereign import SovereignAdapter
from ocr_bench.profiles import load_profile_catalog
from ocr_bench.secrets import sanitize_secret_text


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "configs" / "profiles.json"
SECRET_ENV_NAMES = ("OPENROUTER_API_KEY", "GROQ_API_KEY")


def _sanitize(value: str, exact_secrets: Sequence[str]) -> str:
    sanitized = sanitize_secret_text(value) or ""
    for secret in sorted(set(exact_secrets), key=len, reverse=True):
        if secret:
            sanitized = sanitized.replace(secret, "<redacted>")
    return sanitized


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "profile", choices=("sovereign_default", "sovereign_scan")
    )
    parser.add_argument("--hardware", choices=("cpu", "gpu"), default="cpu")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument(
        "--be-path",
        type=Path,
        default=None,
        help="authoritative Sovereign BE root (also available as SOVEREIGN_BE_PATH)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    exact_secrets = tuple(
        value for name in SECRET_ENV_NAMES if (value := os.environ.get(name))
    )
    try:
        if args.be_path is not None:
            os.environ["SOVEREIGN_BE_PATH"] = str(args.be_path.resolve())
        profile = load_profile_catalog(args.catalog.resolve())[args.profile]
        adapter = SovereignAdapter.from_profile(profile)
        resolved = adapter.configure_hardware(args.hardware)
        if resolved != args.hardware:
            raise RuntimeError(
                f"configure_hardware({args.hardware!r}) returned {resolved!r}"
            )
        payload = {
            "fingerprint": adapter.config_fingerprint(),
            "profile": profile.name,
            "status": "ok",
        }
    except BaseException as exc:  # VuotTran intentionally inherits BaseException
        message = _sanitize(f"{type(exc).__name__}: {exc}", exact_secrets)
        print(message, file=sys.stderr)
        return 2

    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
