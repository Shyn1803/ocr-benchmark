"""Chạy và chấm: (engine × tài liệu × metric) → bảng.

File này cố ý tách làm **hai nửa không dính nhau**:

    run_engines(adapters, docs)          → list[OcrResult]     ← đắt, ~3h cho Marker
    score_results(results, metrics, gt)  → ScoreTable          ← rẻ, vài giây

Cái khe ở giữa chính là A2 (TASK-073): chèn cache vào đó thì sửa một dòng trong
metric không còn phải chạy lại OCR. Viết liền một mạch bây giờ thì A2 sẽ phải tháo
ra — nên tách sẵn.

Quy tắc trình bày, giữ nguyên tinh thần của `metrics/base.py`:

* Ô **N/A** không bao giờ được thay bằng 0, và dòng N/A **không** bị bỏ khỏi bảng.
  Bỏ dòng là cách nhanh nhất làm engine yếu trông mạnh.
* Mọi số trung bình đều đi kèm tỉ lệ hỏng — `Aggregate.cell()` lo việc đó.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from ocr_bench.adapters.base import Adapter
from ocr_bench.metrics.base import Aggregate, Metric, aggregate
from ocr_bench.types import GroundTruth, MetricResult, NAReason, OcrResult

__all__ = ["run_engines", "score_results", "run_bench", "ScoreTable"]


def run_engines(
    adapters: Sequence[Adapter], docs: Sequence[Path]
) -> list[OcrResult]:
    """Nửa đắt tiền. Không ném: engine hỏng thành một dòng `failed=True`."""
    return [a.execute(d) for a in adapters for d in docs]


def score_results(
    results: Iterable[OcrResult],
    metrics: Sequence[Metric],
    ground_truth: Mapping[str, GroundTruth],
) -> ScoreTable:
    """Nửa rẻ tiền. Chỉ đọc `OcrResult`, không chạm engine nào."""
    rows: list[MetricResult] = []
    for r in results:
        gt = ground_truth.get(r.doc_id)
        for m in metrics:
            if gt is None:
                # Thiếu nhãn là lỗi của bộ mẫu, không phải của engine — nó không
                # được vào mẫu số phạt. `aggregate()` xử lý đúng như vậy.
                rows.append(
                    MetricResult(
                        metric=m.name,
                        engine=r.engine,
                        doc_id=r.doc_id,
                        value=None,
                        na_reason=NAReason.NO_GROUND_TRUTH,
                    )
                )
            else:
                rows.append(m.score(gt, r))
    return ScoreTable(tuple(rows))


def run_bench(
    adapters: Sequence[Adapter],
    docs: Sequence[Path],
    metrics: Sequence[Metric],
    ground_truth: Mapping[str, GroundTruth],
) -> ScoreTable:
    """Tiện lợi: chạy rồi chấm ngay. Dùng cho thử nhanh và cho test."""
    return score_results(run_engines(adapters, docs), metrics, ground_truth)


@dataclass(frozen=True, slots=True)
class ScoreTable:
    """Toàn bộ điểm thô, cộng các cách nhìn đã gộp.

    Giữ lại `rows` thô chứ không chỉ giữ số đã gộp: D2 (TASK-088) phải mở tay 20 ca
    điểm thấp nhất, mà một con số trung bình thì không chỉ được ca nào.
    """

    rows: tuple[MetricResult, ...]

    def engines(self) -> list[str]:
        return sorted({r.engine for r in self.rows})

    def metrics(self) -> list[str]:
        return sorted({r.metric for r in self.rows})

    def docs(self) -> list[str]:
        return sorted({r.doc_id for r in self.rows})

    def cell(self, metric: str, engine: str) -> Aggregate:
        return aggregate(
            [r for r in self.rows if r.metric == metric and r.engine == engine],
            metric=metric,
            engine=engine,
        )

    def aggregates(self) -> dict[tuple[str, str], Aggregate]:
        return {
            (m, e): self.cell(m, e) for m in self.metrics() for e in self.engines()
        }

    def ranking(self, metric: str) -> list[Aggregate]:
        """Xếp hạng engine theo một metric, tốt nhất trước.

        Engine không đo được (`applicable=False`) xuống cuối và **vẫn có mặt** —
        cổng C2 cần thấy chúng để phân biệt "đứng bét" với "không xuất hiện".
        """
        cells = [self.cell(metric, e) for e in self.engines()]
        return sorted(
            cells,
            key=lambda a: (a.applicable, a.penalized_mean or 0.0, a.engine),
            reverse=True,
        )

    def worst(self, n: int = 20) -> list[MetricResult]:
        """`n` ca điểm thấp nhất — đầu vào của D2, đọc tay từng ca.

        Bỏ N/A: "không đo được" không phải "đo được và tệ", trộn vào thì danh sách
        20 ca đọc tay sẽ toàn ô trống.
        """
        scored = [r for r in self.rows if r.value is not None]
        return sorted(scored, key=lambda r: (r.value, r.metric, r.engine, r.doc_id))[:n]

    def to_markdown(self) -> str:
        """Bảng xếp hạng dạng đọc được. Hàng = metric, cột = engine."""
        engines = self.engines()
        head = "| metric | " + " | ".join(engines) + " |"
        sep = "|" + "---|" * (len(engines) + 1)
        body = [
            "| "
            + " | ".join([m] + [self.cell(m, e).cell() for e in engines])
            + " |"
            for m in self.metrics()
        ]
        return "\n".join([head, sep, *body])
