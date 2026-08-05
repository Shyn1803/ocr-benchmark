"""Lớp cha của adapter.

Adapter là chỗ **duy nhất** biết engine gốc kỳ quặc ra sao: hệ toạ độ nào, số trang
từ mấy, ảnh trả PIL hay base64, tên block là ``Picture`` hay ``Figure``. Từ đây trở
ra, mọi thứ đã chuẩn hoá.

`capabilities` khai **tĩnh** ở cấp lớp và bị kiểm ngay lúc đăng ký vào registry —
không đợi tới lúc chạy thật mới biết engine không có bbox.
"""

from __future__ import annotations

import abc
import dataclasses
import time
import traceback
from pathlib import Path
from typing import ClassVar

from ocr_bench.types import Capability, OcrResult

__all__ = ["Adapter"]


class Adapter(abc.ABC):
    name: ClassVar[str]
    capabilities: ClassVar[frozenset[Capability]]

    def version(self) -> str:
        """Version engine, ghi vào kết quả. D1 lưu `history/` kèm số này."""
        return "unknown"

    def config_fingerprint(self) -> dict[str, object]:
        """Config engine đang chạy ở chế độ nào.

        Bắt buộc không rỗng với `sovereign` (A7): người đọc phải biết baseline được
        đo với `ocr_use_vision_api` bật hay tắt.
        """
        return {}

    @abc.abstractmethod
    def run(self, doc_path: Path) -> OcrResult:
        """Chạy engine. Được phép ném exception — `execute()` bắt."""

    def execute(self, doc_path: Path) -> OcrResult:
        """Chạy có bọc: đo thời gian, biến exception thành `failed=True`.

        Engine hỏng phải thành một dòng kết quả, không được làm sập cả lượt chạy —
        `FailRate` chỉ có nghĩa khi thất bại được ghi lại chứ không bị nuốt.
        """
        doc_id = doc_path.stem
        t0 = time.perf_counter()
        try:
            result = self.run(doc_path)
        except Exception as exc:  # noqa: BLE001 - cố ý bắt tất cả
            return OcrResult(
                engine=self.name,
                engine_version=self.version(),
                doc_id=doc_id,
                capabilities=self.capabilities,
                seconds=time.perf_counter() - t0,
                failed=True,
                error=f"{type(exc).__name__}: {exc}",
                config_fingerprint={
                    **self.config_fingerprint(),
                    "traceback": traceback.format_exc(limit=5),
                },
            )
        if result.seconds is None:
            result = dataclasses.replace(result, seconds=time.perf_counter() - t0)
        return result
