"""Đo đỉnh RSS trong cửa sổ chạy của một engine — B6 (TASK-084).

    with DoRss() as do:
        result = adapter.run(path)
    mb, pham_vi = do.ket_qua

File này nằm ở tầng thấp (cạnh `types`), **không** ở `metrics/`: `adapters/base.py`
dùng nó, mà adapter không được phụ thuộc vào tầng chấm điểm.

## Vì sao đo delta chứ không đo `max(RSS)`

RSS là **mốc nước cao** của cả tiến trình: nó không giảm khi Python trả vùng nhớ về
allocator. Chạy ba engine trong một tiến trình rồi lấy `max(RSS)` cho mỗi engine thì
engine thứ ba luôn thừa hưởng đỉnh của hai engine trước — bảng xếp hạng bộ nhớ sẽ
đúng bằng **thứ tự chạy**, và không có triệu chứng nào để phát hiện.

Nên: lấy mốc ngay trước khi chạy, lấy mẫu trong lúc chạy, báo `đỉnh - mốc`. Mốc được
tính là **mẫu đầu tiên**, nên hiệu không bao giờ âm — không phải kẹp về 0, mà là
không có đường nào ra số âm.

Con số này vẫn là cận dưới: nếu engine cấp phát rồi giải phóng giữa hai lần lấy mẫu,
đỉnh thật lọt lưới. Chu kỳ 50 ms là đánh đổi có chủ ý.

## Vì sao phải khai phạm vi

`opendataloader` chạy một `.jar` bằng tiến trình `java` con; `sovereign` có nhánh
`subprocess`. RSS của tiến trình Python **không thấy JVM heap**. In một cột RSS mà
không nói nó đếm tới đâu sẽ làm engine nuôi cả một JVM trông nhẹ nhất bảng — sai
theo một hướng biết trước, tức là còn tệ hơn nhiễu.

Có `psutil` thì cộng cả tiến trình con và khai ``process+children``. Đọc một tiến
trình con bị từ chối quyền thì **hạ** phạm vi xuống ``process`` chứ không im lặng
báo thiếu: khai `process+children` trong khi thực tế đếm hụt là đúng thứ cột phạm vi
sinh ra để chặn.

Không có `psutil` thì trả ``(None, None)`` — ô trong bảng hiện ``—``. `psutil` là
extra (`perf`), `pytest` phải xanh trên máy trắng.
"""

from __future__ import annotations

import threading

from ocr_bench.types import RssScope

__all__ = ["DoRss", "co_psutil"]

CHU_KY = 0.05
"""Giây giữa hai lần lấy mẫu. Mỗi lần chỉ đọc vài số nguyên từ OS."""


def _psutil():
    """`psutil` nếu có, `None` nếu không. Nhập lười — cùng kỷ luật với `jiwer`."""
    try:
        import psutil
    except ImportError:
        return None
    return psutil


def co_psutil() -> bool:
    """Máy này đo được RSS hay không. Test dùng để bỏ qua nhánh không đo được."""
    return _psutil() is not None


class DoRss:
    """Bộ lấy mẫu RSS chạy trên luồng nền.

    Dùng như context manager. Đọc `ket_qua` **sau** khi ra khỏi `with` — lúc đó luồng
    đã dừng và đỉnh đã chốt.
    """

    def __init__(self, chu_ky: float = CHU_KY) -> None:
        self.chu_ky = chu_ky
        self._proc = None
        self._moc: float | None = None
        self._dinh: float | None = None
        self._du_quyen = True
        """False = có tiến trình con đọc không được → hạ phạm vi xuống `process`."""
        self._dung = threading.Event()
        self._luong: threading.Thread | None = None

    # -- vòng đời -----------------------------------------------------------

    def __enter__(self) -> DoRss:
        ps = _psutil()
        if ps is None:
            return self
        self._proc = ps.Process()
        self._moc = self._doc()
        self._dinh = self._moc
        self._luong = threading.Thread(
            target=self._vong, name="do-rss", daemon=True
        )
        self._luong.start()
        return self

    def __exit__(self, *_exc: object) -> None:
        self._dung.set()
        if self._luong is not None:
            # Chờ hẳn: đọc `ket_qua` trong lúc luồng còn ghi `_dinh` là điều kiện
            # đua. Luồng chỉ ngủ tối đa một chu kỳ nên chờ là rẻ.
            self._luong.join(timeout=5 * self.chu_ky + 1.0)
            self._luong = None

    # -- đo -----------------------------------------------------------------

    def _doc(self) -> float | None:
        """RSS hiện tại theo MB, cộng cả tiến trình con nếu đọc được."""
        ps = _psutil()
        if ps is None or self._proc is None:
            return None
        try:
            tong = self._proc.memory_info().rss
        except Exception:  # noqa: BLE001 — tiến trình chính biến mất: hết đo được
            return None
        try:
            con = self._proc.children(recursive=True)
        except Exception:  # noqa: BLE001
            self._du_quyen = False
            con = []
        for c in con:
            try:
                tong += c.memory_info().rss
            except Exception:  # noqa: BLE001 — chết giữa chừng hoặc bị từ chối
                # Tiến trình con vừa kết thúc là chuyện thường và không làm hụt số
                # (nó đã trả nhớ). Nhưng phân biệt "vừa chết" với "bị từ chối quyền"
                # đòi bắt hai lớp exception riêng của psutil, mà `psutil` ở đây là
                # tuỳ chọn nên không import được ở chỗ này. Hạ phạm vi cho cả hai —
                # khai thiếu thì người đọc mất một chút thông tin, khai thừa thì họ
                # tin vào một con số không đếm hết.
                self._du_quyen = False
        return tong / (1024 * 1024)

    def _vong(self) -> None:
        while not self._dung.is_set():
            mb = self._doc()
            if mb is None:
                return
            if self._dinh is None or mb > self._dinh:
                self._dinh = mb
            self._dung.wait(self.chu_ky)

    @property
    def ket_qua(self) -> tuple[float | None, RssScope | None]:
        """`(MB tăng thêm trong cửa sổ chạy, phạm vi)`; `(None, None)` nếu không đo được."""
        if self._dinh is None or self._moc is None:
            return None, None
        pham_vi: RssScope = "process+children" if self._du_quyen else "process"
        return self._dinh - self._moc, pham_vi
