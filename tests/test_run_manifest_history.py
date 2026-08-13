"""Sổ lịch sử chạy phải chỉ-ghi-thêm.

``run-manifest.json`` là một ô nhớ duy nhất: chạy lại là ghi đè. Thư mục
``prediction/`` thì ngược lại — nó tích luỹ. Nếu không có sổ lịch sử thì lượt
chạy hẹp sau sẽ xoá mất mô tả của lượt rộng trước, và manifest còn lại mô tả
thiếu chính corpus nằm cạnh nó.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_research_predictions.py"


@pytest.fixture(scope="module")
def module():
    spec = importlib.util.spec_from_file_location("_run_research_predictions", SCRIPT)
    assert spec is not None and spec.loader is not None
    loaded = importlib.util.module_from_spec(spec)
    # phải đăng ký trước khi exec: script có @dataclass, mà dataclasses tra
    # sys.modules[cls.__module__] để phân giải annotation.
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


def _doc(profiles: list[str], generated_at: str) -> dict[str, object]:
    return {
        "generated_at": generated_at,
        "mode": "calibration",
        "profiles": [{"name": name} for name in profiles],
    }


def test_lich_su_giu_lai_luot_chay_truoc(module, tmp_path: Path) -> None:
    """Lượt sau hẹp hơn không được xoá dấu vết lượt trước."""
    path = tmp_path / "run-manifest-history.jsonl"
    rong = _doc(["opendataloader_default", "opendataloader_scan"], "2026-08-13T02:11:10Z")
    hep = _doc(["opendataloader_scan"], "2026-08-13T06:26:24Z")

    module._append_manifest_history(path, rong)
    module._append_manifest_history(path, hep)

    dong = path.read_text(encoding="utf-8").splitlines()
    assert len(dong) == 2
    assert [json.loads(d)["generated_at"] for d in dong] == [
        "2026-08-13T02:11:10Z",
        "2026-08-13T06:26:24Z",
    ]
    # profile của lượt rộng vẫn còn nguyên trong dòng đầu
    assert [p["name"] for p in json.loads(dong[0])["profiles"]] == [
        "opendataloader_default",
        "opendataloader_scan",
    ]


def test_moi_dong_la_mot_luot_khong_gop(module, tmp_path: Path) -> None:
    """Không trộn hai lượt vào một bản ghi — mỗi lượt có commit/thời điểm riêng."""
    path = tmp_path / "run-manifest-history.jsonl"
    module._append_manifest_history(path, _doc(["a"], "2026-01-01T00:00:00Z"))
    module._append_manifest_history(path, _doc(["b"], "2026-01-02T00:00:00Z"))

    ban_ghi = [json.loads(d) for d in path.read_text(encoding="utf-8").splitlines()]
    assert [[p["name"] for p in r["profiles"]] for r in ban_ghi] == [["a"], ["b"]]


def test_tao_thu_muc_cha_va_dung_lf(module, tmp_path: Path) -> None:
    path = tmp_path / "chua-ton-tai" / "run-manifest-history.jsonl"
    module._append_manifest_history(path, _doc(["a"], "2026-01-01T00:00:00Z"))
    assert b"\r\n" not in path.read_bytes()
