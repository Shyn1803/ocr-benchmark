#!/usr/bin/env python3
"""Fail-closed, document-free preflight for frozen Sovereign profiles."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Sequence

from ocr_bench.adapters.sovereign import (
    SovereignAdapter,
    _sanitize_runtime_text,
    thu_thap_bi_mat,
)
from ocr_bench.profiles import load_profile_catalog


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "configs" / "profiles.json"


def _sanitize(value: str, exact_secrets: Sequence[str]) -> str:
    """Dùng đúng bộ lọc của adapter.

    Bản sao trước đây ở file này liệt kê 2 tên biến môi trường trong khi adapter đã
    lên 4 và thêm cả `.env` của BE. Hai danh sách cạnh nhau thì cái ít được sửa hơn
    sẽ tụt lại, và ở đây tụt lại nghĩa là script chẩn đoán in ra thứ mà adapter đã
    bịt — không phải nguy cơ lý thuyết mà là một script thật, chạy tay, in ra stdout.
    """
    return _sanitize_runtime_text(value, tuple(exact_secrets))


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
    # `--be-path` phải được đặt trước: `thu_thap_bi_mat()` đọc `.env` của **đúng** BE
    # root đó để biết chuỗi nào cần bịt. Và bản thân nó phải chạy trước khi adapter
    # `_ap_env()` xoá trắng các biến môi trường nhạy cảm.
    if args.be_path is not None:
        os.environ["SOVEREIGN_BE_PATH"] = str(args.be_path.resolve())
    exact_secrets = thu_thap_bi_mat()
    try:
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
