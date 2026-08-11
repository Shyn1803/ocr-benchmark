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

from ocr_bench.rss import DoRss
from ocr_bench.secrets import sanitize_secret_text
from ocr_bench.types import Capability, FailureKind, OcrResult

__all__ = ["Adapter", "AdapterOutputError", "classify_exception"]


class AdapterOutputError(ValueError):
    """Adapter không thể normalize/map raw engine output sang canonical types."""


def classify_exception(exc: BaseException) -> FailureKind:
    """Phân loại lỗi engine tại một biên chung, trước khi message bị stringify."""
    if isinstance(exc, AdapterOutputError):
        return FailureKind.ADAPTER_ERROR
    if isinstance(exc, TimeoutError):
        return FailureKind.TIMEOUT
    if isinstance(exc, MemoryError):
        return FailureKind.OOM
    if isinstance(exc, (ImportError, FileNotFoundError)):
        return FailureKind.ENVIRONMENT_ERROR
    return FailureKind.ENGINE_ERROR


class Adapter(abc.ABC):
    name: ClassVar[str]
    capabilities: ClassVar[frozenset[Capability]]

    @property
    def ten_engine_that(self) -> str:
        """Engine **thật** đứng sau adapter này. Mặc định chính là `name`.

        Chỉ khác `name` ở adapter đóng vai trung gian: `NguonTuDia` phát lại kết quả
        đã lưu của một engine khác, nên `name` của nó (`nguon_tu_dia`) là chi tiết cài
        đặt chứ không phải danh tính engine.

        `SabotageAdapter` ghi tên nguồn vào `version()` và `config_fingerprint()`, và
        hai thứ đó đi thẳng vào `manifest.json` của bản công bố. Lấy `name` ở đó thì
        bảng ghi `sabotage/1+nguon_tu_dia` — người đọc mất luôn thông tin *engine nào
        đã bị làm hỏng*, tức mất ý nghĩa của cả cổng C2.
        """
        return self.name

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
        """Chạy có bọc: đo thời gian **và bộ nhớ**, biến exception thành `failed=True`.

        Engine hỏng phải thành một dòng kết quả, không được làm sập cả lượt chạy —
        `FailRate` chỉ có nghĩa khi thất bại được ghi lại chứ không bị nuốt. Lượt chạy
        hỏng vẫn giữ số giờ và số nhớ đo được: nó nói engine ngốn bao nhiêu trước khi
        chết, và vứt đi thì `FailRate` cao lại thành cách làm bảng perf đẹp lên.

        Số của adapter **luôn thắng số của lớp bọc** (B6/AC-04). Adapter tự đo bên
        trong `run()` thì nó đo hẹp hơn — không dính chi phí gọi hàm, đọc file, quy
        đổi toạ độ — nên nó chính xác hơn. Lớp bọc chỉ điền vào chỗ còn `None`.
        """
        doc_id = doc_path.stem
        do_rss = DoRss()
        t0 = time.perf_counter()
        try:
            with do_rss:
                result = self.run(doc_path)
        except Exception as exc:  # noqa: BLE001 - cố ý bắt tất cả
            giay = time.perf_counter() - t0
            rss, pham_vi = do_rss.ket_qua
            error = sanitize_secret_text(f"{type(exc).__name__}: {exc}")
            trace = sanitize_secret_text(traceback.format_exc(limit=5))
            return OcrResult(
                engine=self.name,
                engine_family=getattr(self, "engine_family", self.name),
                profile=getattr(self, "profile", "legacy"),
                engine_version=self.version(),
                doc_id=doc_id,
                capabilities=self.capabilities,
                seconds=giay,
                peak_rss_mb=rss,
                rss_scope=pham_vi,
                failed=True,
                error=error,
                failure_kind=classify_exception(exc),
                config_fingerprint={
                    **self.config_fingerprint(),
                    "traceback": trace,
                },
            )
        if result.seconds is None:
            result = dataclasses.replace(result, seconds=time.perf_counter() - t0)
        if result.peak_rss_mb is None:
            # Đi kèm nhau: `rss_scope` mô tả `peak_rss_mb`, ghi đè riêng một cái là
            # gán nhãn của phép đo này cho con số của phép đo kia.
            rss, pham_vi = do_rss.ket_qua
            result = dataclasses.replace(
                result, peak_rss_mb=rss, rss_scope=pham_vi
            )
        return result
