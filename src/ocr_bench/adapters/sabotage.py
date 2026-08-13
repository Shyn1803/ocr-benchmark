"""Engine giả `sabotage` — cái cân để kiểm tra chính bộ thước đo.

Nó không đọc PDF. Nó lấy kết quả của một engine khác rồi **cố tình làm hỏng**: xáo
dòng, cắt bớt, xô lệch bbox, xén bớt hàng trong bảng, xoá ký tự, và bỏ rowspan/colspan.

Công dụng của nó: **metric nào không chấm `sabotage` thấp hơn chính nguồn của nó thì
metric đó chưa được falsify.** C2 (TASK-086) dùng adapter này làm cổng cứng.
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

__all__ = [
    "SabotageAdapter",
    "KEEP_RATIO",
    "MUC_SABOTAGE",
    "SEED_SABOTAGE",
    "ten_muc_sabotage",
]

KEEP_RATIO = 0.5
"""Mặc định giữ lại bao nhiêu phần nội dung. 0.5 = cắt còn một nửa."""

SEED_SABOTAGE = 1337
"""Seed cố định cho mọi mức phá hoại. Đổi seed là đổi quần thể, tức đổi bảng."""

MUC_SABOTAGE: tuple[float, ...] = (0.1, 0.3, 0.6)
"""Ba mức nghiêm trọng của phép làm hỏng.

Một mức duy nhất chỉ trả lời được "metric có thấy phép làm hỏng không". Ba mức trả lời
được câu mạnh hơn: **điểm có giảm đơn điệu theo mức hỏng không**. Metric tụt xuống sàn
ngay ở 0.1 rồi nằm im, hoặc metric nhảy loạn giữa các mức, đều là metric không dùng
được để xếp hạng — mà phép so một điểm không bắt được cả hai.
"""


def ten_muc_sabotage(severity: float) -> str:
    """`0.3` → `"sabotage_s30"`. Tên engine của một mức, dùng làm khoá trong bảng điểm."""
    return f"sabotage_s{int(round(severity * 100)):02d}"


_ROW_RE = re.compile(r"<tr\b.*?</tr>", re.IGNORECASE | re.DOTALL)
_SPAN_RE = re.compile(r'\s*(rowspan|colspan)\s*=\s*(?:"[^"]*"|\'[^\']*\'|\d+)', re.IGNORECASE)


def _keep_ratio_items(items: list, rng: random.Random, ratio: float) -> list:
    """Xáo rồi giữ lại theo `ratio`. Danh sách 1 phần tử vẫn giữ 1."""
    if not items:
        return []
    shuffled = items[:]
    rng.shuffle(shuffled)
    n_keep = max(1, int(len(shuffled) * ratio))
    return shuffled[:n_keep]


def _corrupt_text(text: str, rng: random.Random, severity: float = 0.5) -> str:
    """Xáo dòng/từ và xoá bớt ký tự theo severity."""
    ratio = max(0.05, min(0.95, 1.0 - severity))

    lines = [ln for ln in text.split("\n") if ln.strip()]
    if len(lines) >= 2:
        kept_lines = _keep_ratio_items(lines, rng, ratio)
        result = "\n".join(kept_lines)
    else:
        words = text.split()
        kept_words = _keep_ratio_items(words, rng, ratio)
        result = " ".join(kept_words)

    # Apply character drop only if severity > 0.5
    if severity > 0.5:
        char_drop_prob = (severity - 0.5) * 0.3
        result = "".join(c for c in result if c == "\n" or c == " " or rng.random() >= char_drop_prob)

    return result


def _jitter(box: Box | None, rng: random.Random, severity: float = 0.5) -> Box | None:
    """Xô lệch bbox theo mức độ severity."""
    if box is None:
        return None
    d = max(0.02, min(0.3, 0.2 * severity))

    def nudge(v: float) -> float:
        return min(1.0, max(0.0, v + rng.uniform(-d, d)))

    x0, x1 = sorted((nudge(box.x0), nudge(box.x1)))
    y0, y1 = sorted((nudge(box.y0), nudge(box.y1)))
    return Box(page=box.page, x0=x0, y0=y0, x1=x1, y1=y1)


def _corrupt_table(table: OcrTable, rng: random.Random, severity: float = 0.5) -> OcrTable:
    """Bỏ rowspan/colspan và bỏ bớt hàng `<tr>`."""
    ratio = max(0.05, min(0.95, 1.0 - severity))
    html = table.html

    if severity > 0.5:
        html = _SPAN_RE.sub("", html)

    rows = _ROW_RE.findall(html)
    if len(rows) < 2:
        return dataclasses.replace(table, html=html)
    kept = _keep_ratio_items(rows, rng, ratio)
    return dataclasses.replace(
        table, html=f"<table>{''.join(kept)}</table>", n_rows=len(kept)
    )


class SabotageAdapter(Adapter):
    """Bọc một adapter khác và làm hỏng đầu ra của nó theo severity."""

    name: ClassVar[str] = "sabotage"
    capabilities: ClassVar[frozenset[Capability]] = frozenset(Capability)

    def __init__(
        self,
        source: Adapter | None = None,
        *,
        seed: int = SEED_SABOTAGE,
        severity: float = 0.5,
        ten: str | None = None,
    ) -> None:
        self.source = source or NoopAdapter()
        self.seed = seed
        self.severity = max(0.01, min(0.99, severity))
        # Mỗi mức phá hoại phải là một "engine" riêng trong bảng điểm, nếu không ba mức
        # ghi đè lẫn nhau lên cùng khoá `sabotage` và phép so đơn điệu không có gì để so.
        if ten is not None:
            self.name = ten

    def version(self) -> str:
        return f"sabotage/1+{self.source.ten_engine_that}"

    def config_fingerprint(self) -> dict[str, object]:
        fp: dict[str, object] = {
            "source": self.source.ten_engine_that,
            "seed": self.seed,
            "keep_ratio": round(1.0 - self.severity, 4),
        }
        if self.severity != 0.5:
            fp["severity"] = self.severity
        return fp

    def run(self, doc_path: Path) -> OcrResult:
        src = self.source.execute(doc_path)
        if src.failed:
            return dataclasses.replace(
                src,
                engine=self.name,
                engine_version=self.version(),
                capabilities=src.capabilities,
                error=f"nguồn {self.source.name} hỏng: {src.error}",
                config_fingerprint={
                    **src.config_fingerprint,
                    **self.config_fingerprint(),
                },
            )

        rng = random.Random(f"{self.seed}:{src.doc_id}:{self.severity}")
        ratio = 1.0 - self.severity

        blocks = tuple(
            dataclasses.replace(b, box=_jitter(b.box, rng, self.severity))
            for b in _keep_ratio_items(list(src.blocks), rng, ratio)
        )
        images = tuple(
            dataclasses.replace(i, box=_jitter(i.box, rng, self.severity))
            for i in _keep_ratio_items(list(src.images), rng, ratio)
        )
        tables = tuple(
            _corrupt_table(t, rng, self.severity)
            for t in _keep_ratio_items(list(src.tables), rng, ratio)
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
                _corrupt_text(src.text_md, rng, self.severity)
                if src.text_md is not None
                else None
            ),
            blocks=blocks,
            images=images,
            tables=tables,
            scan_label=scan_label,
            page_sizes=src.page_sizes,
            config_fingerprint=self.config_fingerprint(),
        )
