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
def _co_lap_bi_mat_sovereign():
    """Trả `_SECRET_VALUES` và cache `.env` của adapter Sovereign về đúng chỗ cũ.

    `_SECRET_VALUES` **chỉ lớn thêm** theo thiết kế (một profile không được làm mất khả
    năng bịt của profile sau). Hệ quả trong test: một test seed chuỗi bí mật thì test
    sau vẫn thấy nó, nên mọi khẳng định dạng `== 1` trở thành phụ thuộc thứ tự chạy —
    xanh khi chạy riêng, đỏ khi chạy cả file, và không ai đọc ra vì sao.

    Nằm ở `conftest.py` chứ không ở `test_sovereign_adapter.py`: hai file test khác
    (`test_sovereign_preflight.py` và bất kỳ file nào gọi `thu_thap_bi_mat()`) dùng
    chung đúng các biến toàn cục ấy trong cùng một tiến trình pytest. Fixture chỉ rộng
    bằng một file thì nó bảo vệ file đã nghĩ tới nó và bỏ mặc phần còn lại.

    Import trong thân hàm: `ocr_bench.adapters.sovereign` kéo theo `importlib`/`json`
    ở cấp module, và `conftest.py` được nạp cho **mọi** phiên chạy kể cả những phiên
    không đụng tới Sovereign.
    """
    from ocr_bench.adapters import sovereign as sov

    with sov._SECRET_VALUES_LOCK:
        anh_chup = set(sov._SECRET_VALUES)
        anh_chup_chac = set(sov._SECRET_VALUES_CHAC)
    cache_cu = dict(sov._ENV_BE_CACHE)
    try:
        yield
    finally:
        with sov._SECRET_VALUES_LOCK:
            sov._SECRET_VALUES.clear()
            sov._SECRET_VALUES.update(anh_chup)
            sov._SECRET_VALUES_CHAC.clear()
            sov._SECRET_VALUES_CHAC.update(anh_chup_chac)
        sov._ENV_BE_CACHE.clear()
        sov._ENV_BE_CACHE.update(cache_cu)


@pytest.fixture(autouse=True)
def _restore_registry():
    adapters = dict(registry._ADAPTERS)
    metrics = dict(registry._METRICS)
    yield
    registry._ADAPTERS.clear()
    registry._ADAPTERS.update(adapters)
    registry._METRICS.clear()
    registry._METRICS.update(metrics)
