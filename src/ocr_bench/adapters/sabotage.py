"""Engine giả `sabotage` — cái cân để kiểm tra chính bộ thước đo.

Nó không đọc PDF. Nó lấy kết quả của một engine khác rồi **cố tình làm hỏng**: xáo
dòng, cắt còn một nửa, xô lệch bbox, xén bớt hàng trong bảng.

Công dụng của nó: **metric nào không chấm `sabotage` thấp hơn chính nguồn của nó thì
metric đó chưa được falsify.** Một metric viết hỏng vẫn cho ra bảng xếp hạng trông rất
thuyết phục — không nhìn bằng mắt mà phát hiện được. C2 (TASK-086) dùng adapter này
làm cổng cứng.

⚠️ Phát biểu cũ — *"metric nào không xếp `sabotage` **đứng bét toàn bảng**"* — đã bị bác
(D-010, 2026-08-10). Nó trộn hai câu hỏi: *phép làm hỏng có bị phạt không* và *engine nào
giỏi hơn engine nào*. `assert_math_presence` từng báo đỏ chỉ vì `pdf_inspector` thật sự
chấm 0,0000 (nó không sinh công thức). So sánh đúng là **với nguồn**, và `noop` — vốn là
sàn theo cấu tạo — bị loại khỏi tập so sánh.

**Giới hạn của chính adapter này:** mọi phép ở đây **chỉ xoá, không bao giờ chèn**. Nên
nó **không thể** falsify metric nào được thưởng khi văn bản ngắn đi: `assert_text_absence`
(xoá chữ làm chuỗi cấm biến mất ⇒ khẳng định lật sang đạt) và `assert_baseline`
(`_keep_half` trả `max(1, ...)` phần tử nên đầu ra không bao giờ rỗng, và xoá thì không
sinh được U+FFFD ⇒ luôn hoà 1,0000). Hai metric đó **không hỏng** — falsifier thiếu năng
lực. Bản chèn (`sabotage_insert`) là TASK-097, làm thành engine **thứ hai**, không sửa
engine này.

Hai ràng buộc bắt buộc:

* **Cùng `capabilities` với nguồn.** Khai ít hơn thì metric trả N/A và `sabotage`
  *biến mất khỏi bảng* thay vì đứng bét — đúng cái nó sinh ra để phát hiện.
* **Tất định.** Seed cố định theo `doc_id`, nên C2 chạy lại luôn ra cùng thứ hạng.
  Xáo ngẫu nhiên thật sẽ làm cổng C2 thỉnh thoảng đỏ thỉnh thoảng xanh, và một cổng
  như vậy thì người ta tắt đi chứ không đi sửa.
"""

from __future__ import annotations

import dataclasses
import random
import re
from pathlib import Path
from typing import ClassVar

from ocr_bench.adapters.base import Adapter
from ocr_bench.adapters.noop import NoopAdapter
from ocr_bench.types import Box, Capability, OcrResult, OcrTable

__all__ = ["SabotageAdapter", "KEEP_RATIO"]

KEEP_RATIO = 0.5
"""Giữ lại bao nhiêu phần nội dung. 0.5 = cắt còn một nửa."""

_ROW_RE = re.compile(r"<tr\b.*?</tr>", re.IGNORECASE | re.DOTALL)


def _keep_half(items: list, rng: random.Random) -> list:
    """Xáo rồi cắt còn ~một nửa. Danh sách 1 phần tử vẫn giữ lại 1 — cắt về rỗng
    thì mất luôn khả năng phân biệt "hỏng nhiều" với "không trả gì"."""
    if not items:
        return []
    shuffled = items[:]
    rng.shuffle(shuffled)
    return shuffled[: max(1, int(len(shuffled) * KEEP_RATIO))]


def _corrupt_text(text: str, rng: random.Random) -> str:
    """Xáo dòng rồi cắt còn một nửa.

    Văn bản một dòng thì xáo dòng không đổi gì cả — rơi xuống xáo theo từ. Không có
    nhánh này, `sabotage` trên tài liệu ngắn sẽ ra điểm **hệt** nguồn, và C2 báo
    "metric không phân biệt được" trong khi lỗi nằm ở chỗ này.
    """
    lines = [ln for ln in text.split("\n") if ln.strip()]
    if len(lines) >= 2:
        return "\n".join(_keep_half(lines, rng))
    words = text.split()
    return " ".join(_keep_half(words, rng))


def _jitter(box: Box | None, rng: random.Random) -> Box | None:
    """Xô lệch bbox ~10% chiều rộng/cao trang để IoU tụt mà không về 0 hẳn.

    Cố ý *không* đẩy hẳn ra ngoài: IoU = 0 với mọi tài liệu thì mọi metric bbox đều
    cho `sabotage` cùng một điểm sàn, và ta mất khả năng thấy metric nào nhạy hơn.

    Sắp lại toạ độ **trước khi** dựng `Box`: xô lệch hai mép ngược chiều nhau có thể
    làm x1 < x0, mà `Box.__post_init__` chặn box lộn ngược — sắp sau khi dựng thì
    không bao giờ chạy tới.
    """
    if box is None:
        return None
    d = 0.1

    def nudge(v: float) -> float:
        return min(1.0, max(0.0, v + rng.uniform(-d, d)))

    x0, x1 = sorted((nudge(box.x0), nudge(box.x1)))
    y0, y1 = sorted((nudge(box.y0), nudge(box.y1)))
    return Box(page=box.page, x0=x0, y0=y0, x1=x1, y1=y1)


def _corrupt_table(table: OcrTable, rng: random.Random) -> OcrTable:
    """Bỏ bớt hàng `<tr>`. TEDS phải bắt được; CER thì gần như không."""
    rows = _ROW_RE.findall(table.html)
    if len(rows) < 2:
        return table
    kept = _keep_half(rows, rng)
    return dataclasses.replace(
        table, html=f"<table>{''.join(kept)}</table>", n_rows=len(kept)
    )


class SabotageAdapter(Adapter):
    """Bọc một adapter khác và làm hỏng đầu ra của nó.

    `capabilities` là thuộc tính **lớp** (registry đòi vậy) nên nó khai đủ mọi năng
    lực — nghĩa là "cái gì nguồn có thì tôi chuyển tiếp". Năng lực *thực tế* của mỗi
    lần chạy lấy theo nguồn và ghi vào `OcrResult`, nên `Metric.score()` vẫn ra N/A
    đúng chỗ.

    ⚠️ Hệ quả: `registry.applicable_metrics("sabotage")` trả về toàn ``True`` dù
    nguồn có thể không có năng lực đó — hàm ấy chỉ nhìn được cấp lớp, mà nguồn thì
    là thuộc tính của thể hiện. Vì vậy `scorer` tính khả dụng từ kết quả **thật**
    (`Aggregate.applicable`), không từ `applicable_metrics()`.
    """

    name: ClassVar[str] = "sabotage"
    capabilities: ClassVar[frozenset[Capability]] = frozenset(Capability)

    def __init__(self, source: Adapter | None = None, *, seed: int = 1337) -> None:
        # Mặc định là `noop` để adapter này chạy được ngay trên máy chưa cài engine
        # nào. Thực chiến thì truyền engine tốt nhất vào — hỏng đầu ra của engine
        # mạnh mới là phép thử có ý nghĩa.
        self.source = source or NoopAdapter()
        self.seed = seed

    def version(self) -> str:
        # `ten_engine_that`, không phải `name`: nguồn có thể là `NguonTuDia` phát lại
        # kết quả đã lưu, và khi đó `name` là `nguon_tu_dia` — bảng công bố sẽ ghi
        # `sabotage/1+nguon_tu_dia` và giấu mất engine nào thực sự bị làm hỏng.
        return f"sabotage/1+{self.source.ten_engine_that}"

    def config_fingerprint(self) -> dict[str, object]:
        return {
            "source": self.source.ten_engine_that,
            "seed": self.seed,
            "keep_ratio": KEEP_RATIO,
        }

    def run(self, doc_path: Path) -> OcrResult:
        src = self.source.execute(doc_path)
        if src.failed:
            # Nguồn hỏng thì `sabotage` cũng hỏng. Trả kết quả "sạch" ở đây sẽ khiến
            # nó trông tốt hơn nguồn đúng vào lúc nguồn tệ nhất.
            return dataclasses.replace(
                src,
                engine=self.name,
                engine_version=self.version(),
                capabilities=src.capabilities,
                error=f"nguồn {self.source.name} hỏng: {src.error}",
                # Giữ nguyên fingerprint của nguồn (có traceback) rồi chồng thêm
                # của mình — mất traceback là mất manh mối gỡ lỗi duy nhất.
                config_fingerprint={
                    **src.config_fingerprint,
                    **self.config_fingerprint(),
                },
            )

        rng = random.Random(f"{self.seed}:{src.doc_id}")

        blocks = tuple(
            dataclasses.replace(b, box=_jitter(b.box, rng))
            for b in _keep_half(list(src.blocks), rng)
        )
        images = tuple(
            dataclasses.replace(i, box=_jitter(i.box, rng))
            for i in _keep_half(list(src.images), rng)
        )
        tables = tuple(
            _corrupt_table(t, rng) for t in _keep_half(list(src.tables), rng)
        )
        scan_label = (
            dataclasses.replace(
                src.scan_label,
                is_scanned=not src.scan_label.is_scanned,
                api=f"sabotage({src.scan_label.api})",
            )
            if src.scan_label is not None
            else None
        )

        return OcrResult(
            engine=self.name,
            engine_version=self.version(),
            doc_id=src.doc_id,
            capabilities=src.capabilities,
            text_md=(
                _corrupt_text(src.text_md, rng) if src.text_md is not None else None
            ),
            blocks=blocks,
            images=images,
            tables=tables,
            scan_label=scan_label,
            page_sizes=src.page_sizes,
            config_fingerprint=self.config_fingerprint(),
        )
