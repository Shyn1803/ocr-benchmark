"""Khôi phục registry sau mỗi test.

Registry là biến toàn cục ở cấp module. Test nào gọi `registry.clear()` hoặc đăng ký
một metric giả sẽ để lại trạng thái đó cho những test chạy sau — và vì pytest chạy
file theo thứ tự chữ cái, hỏng hay không hỏng phụ thuộc vào *tên file*. Đúng loại lỗi
mà sau này người ta gọi là "test bị flaky" rồi đi sửa nhầm chỗ.
"""

from __future__ import annotations

import pytest

from ocr_bench import registry


@pytest.fixture(autouse=True)
def _restore_registry():
    adapters = dict(registry._ADAPTERS)
    metrics = dict(registry._METRICS)
    yield
    registry._ADAPTERS.clear()
    registry._ADAPTERS.update(adapters)
    registry._METRICS.clear()
    registry._METRICS.update(metrics)
