"""Fixture dùng chung: khôi phục registry, và bỏ qua test cần bộ mẫu thật.

Khôi phục registry sau mỗi test.

Registry là biến toàn cục ở cấp module. Test nào gọi `registry.clear()` hoặc đăng ký
một metric giả sẽ để lại trạng thái đó cho những test chạy sau — và vì pytest chạy
file theo thứ tự chữ cái, hỏng hay không hỏng phụ thuộc vào *tên file*. Đúng loại lỗi
mà sau này người ta gọi là "test bị flaky" rồi đi sửa nhầm chỗ.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from ocr_bench import registry

_CORPUS = Path(__file__).resolve().parents[1] / "ground-truth" / "doclaynet" / "layout_coco.json"


def pytest_collection_modifyitems(config, items):
    """`needs_corpus` → skip khi chưa tải bộ mẫu (390 MB, không nằm trong CI mặc định).

    Skip chứ không fail: máy trắng vừa clone về phải `pytest` xanh được. Nhưng số
    skip có in ra ở cuối phiên — người chạy thấy được là có phần chưa kiểm, khác hẳn
    việc lặng lẽ không có test nào.
    """
    if not _CORPUS.exists():
        bo = pytest.mark.skip(
            reason="chưa có bộ mẫu — chạy scripts/fetch_doclaynet.py + fetch_olmocr.py"
        )
        for it in items:
            if "needs_corpus" in it.keywords:
                it.add_marker(bo)

    if importlib.util.find_spec("marker") is None:
        # Cùng lý lẽ với `needs_corpus`: skip chứ không fail, nhưng số skip có in ra
        # nên người chạy thấy được là có phần chưa kiểm.
        bo = pytest.mark.skip(
            reason="chưa cài marker-pdf — xem plan TASK-075 (venv riêng, Python 3.12)"
        )
        for it in items:
            if "needs_marker" in it.keywords:
                it.add_marker(bo)


@pytest.fixture(autouse=True)
def _restore_registry():
    adapters = dict(registry._ADAPTERS)
    metrics = dict(registry._METRICS)
    yield
    registry._ADAPTERS.clear()
    registry._ADAPTERS.update(adapters)
    registry._METRICS.clear()
    registry._METRICS.update(metrics)
