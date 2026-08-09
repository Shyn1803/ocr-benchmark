"""Khung metric + quy tắc tổng hợp.

Hai thứ ở file này quyết định bảng xếp hạng có trung thực hay không:

1. **Cổng năng lực.** Metric không tự chạy trên engine thiếu năng lực rồi ra 0.
   Nó trả N/A. `Metric.score()` là chỗ duy nhất mở cổng — subclass viết
   `_compute()`, không override `score()`.
2. **Tổng hợp trả về `Aggregate`, không trả về một số.** `mean` đi kèm `fail_rate`
   và `penalized_mean` trong cùng một đối tượng, nên không thể lỡ tay in trung bình
   mà quên tỉ lệ hỏng.

Điểm 2 là để tránh đúng cái lỗi của `opendataloader-bench`: repo đó loại tài liệu
engine làm hỏng ra khỏi trung bình, tức là **thưởng cho engine hỏng nhiều hơn**.
"""

from __future__ import annotations

import abc
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import ClassVar

from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Capability,
    GroundTruth,
    MetricResult,
    NAReason,
    OcrResult,
)

__all__ = ["Metric", "Aggregate", "aggregate"]


class Metric(abc.ABC):
    """Lớp cha của mọi thước đo.

    Điểm luôn quy ước **cao hơn là tốt hơn** và nằm trong [0,1]. Metric bản chất là
    tỉ lệ lỗi (CER, WER) phải trả `1 - err` trong `_compute()`, không trả `err` —
    nếu không, test `sabotage` đứng bét ở C2 sẽ phải biết chiều của từng metric.
    """

    name: ClassVar[str]
    requires: ClassVar[frozenset[Capability]] = frozenset()
    gt_kinds: ClassVar[tuple[type, ...]] = (AnnotationGT, AssertionGT)

    def score(self, gt: GroundTruth, result: OcrResult) -> MetricResult:
        """Chấm một tài liệu. **Không override.**"""
        if result.failed:
            return self._na(result, NAReason.ENGINE_FAILED, {"error": result.error})

        missing = self.requires - result.capabilities
        if missing:
            return self._na(
                result,
                NAReason.MISSING_CAPABILITY,
                {"missing": sorted(c.value for c in missing)},
            )

        if not isinstance(gt, self.gt_kinds):
            return self._na(
                result,
                NAReason.WRONG_GT_KIND,
                {
                    "got": type(gt).__name__,
                    "wants": [k.__name__ for k in self.gt_kinds],
                },
            )

        rieng = self._na_rieng(gt, result)
        if rieng is not None:
            return self._na(result, rieng[0], rieng[1])

        value, detail = self._compute(gt, result)
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"{self.name} trả {value!r}, phải nằm trong [0,1]")
        return MetricResult(
            metric=self.name,
            engine=result.engine,
            doc_id=result.doc_id,
            value=value,
            detail=detail,
        )

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        """Điều kiện N/A **riêng của từng metric**, kiểm sau ba cổng chung.

        Có mặt vì cổng chung không đủ: CER cần *nhãn có chữ*, mà `AnnotationGT` cho
        phép `text=None` (tài liệu chỉ có nhãn bố cục). Đúng loại GT nhưng không có
        chữ để so thì phải ra `NO_GROUND_TRUTH`, không phải 0.0 — chấm 0 ở đây là
        phạt engine vì **nhãn** thiếu.

        Trả `None` = không có gì chặn. Đây là chỗ mở rộng duy nhất; `score()` vẫn là
        cổng duy nhất, subclass vẫn không được override nó.
        """
        return None

    @abc.abstractmethod
    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        """Trả `(điểm trong [0,1], chi tiết)`. Chỉ được gọi khi cổng đã mở."""

    def _na(
        self, result: OcrResult, reason: NAReason, detail: dict[str, object]
    ) -> MetricResult:
        return MetricResult(
            metric=self.name,
            engine=result.engine,
            doc_id=result.doc_id,
            value=None,
            na_reason=reason,
            detail=detail,
        )


@dataclass(frozen=True, slots=True)
class Aggregate:
    """Tổng hợp một metric trên một engine, qua nhiều tài liệu.

    `mean` và `fail_rate` cố ý nằm chung một đối tượng — in cái này thì có sẵn cái
    kia, không thể quên.
    """

    metric: str
    engine: str
    n_total: int
    n_scored: int
    n_failed: int
    n_na: int
    mean: float | None
    """Trung bình **chỉ trên tài liệu chấm được**. Đây là con số dễ nhìn và dễ gây
    hiểu nhầm — không bao giờ in một mình, luôn kèm `fail_rate`."""
    penalized_mean: float | None
    """Trung bình có phạt: tài liệu engine làm hỏng tính 0 điểm."""
    fail_rate: float
    applicable: bool
    """False = engine này không có năng lực để metric chạm tới. Ô trong bảng phải in
    ``N/A``, và **không** được bỏ dòng đi — bỏ đi là làm engine yếu trông mạnh."""
    n_thieu_nang_luc: int = 0
    """Số tài liệu N/A vì ``MISSING_CAPABILITY`` — engine không hứa làm việc này."""
    n_chua_nhan: int = 0
    """Số tài liệu N/A vì bộ mẫu chưa có nhãn hợp loại (``NO_GROUND_TRUTH`` hoặc
    ``WRONG_GT_KIND``). Engine **có** năng lực; cái thiếu là nhãn để đối chiếu.
    Gộp hai trạng thái này vào ``N/A`` là đổ lỗi cho engine vì bộ mẫu thiếu."""

    def cell(self) -> str:
        """Một ô trong bảng xếp hạng, dạng đọc được."""
        if not self.applicable:
            return "N/A"
        if self.n_scored == 0 and self.n_chua_nhan > 0:
            # Engine chạy được, bộ mẫu chưa có nhãn hợp loại. Đây là thiếu sót của
            # **bộ mẫu**, không phải của engine. Nhánh này đứng trước khẳng định dưới
            # vì nó là trường hợp duy nhất `applicable` bật mà mẫu số vẫn rỗng.
            return f"chưa có nhãn ({self.n_chua_nhan} tài liệu)"
        # Còn lại: applicable=True ⇒ denom>0 ⇒ penalized_mean khác None.
        assert self.penalized_mean is not None
        if self.n_scored == 0:
            # denom toàn tài liệu HỎNG, và `penalized_mean` bằng 0.0 vì mẫu
            # số toàn số 0. In "0.000" ở đây là nói engine **đo được và tệ nhất**,
            # trong khi sự thật là nó **chưa từng được đo** — sai theo đúng hướng gây
            # hiểu nhầm nặng nhất. Tiêu chí `n_scored == 0` giống hệt `_doc_cham_duoc`
            # của `do_phan_tan()` và `kiem_sabotage()` trong `discrimination.py`.
            return f"— ({self.n_failed} hỏng, 0 chấm được)"
        return f"{self.penalized_mean:.3f} (fail {self.fail_rate:.0%})"


def aggregate(
    results: Iterable[MetricResult], *, metric: str = "", engine: str = ""
) -> Aggregate:
    """Gộp điểm nhiều tài liệu theo đúng quy tắc N/A ở trên."""
    rows: Sequence[MetricResult] = list(results)
    if not rows:
        return Aggregate(
            metric=metric,
            engine=engine,
            n_total=0,
            n_scored=0,
            n_failed=0,
            n_na=0,
            mean=None,
            penalized_mean=None,
            fail_rate=0.0,
            applicable=False,
        )

    names = {r.metric for r in rows}
    engines = {r.engine for r in rows}
    if len(names) > 1 or len(engines) > 1:
        raise ValueError(
            f"aggregate() nhận lẫn metric/engine: {sorted(names)} × {sorted(engines)}"
        )

    scored = [r.value for r in rows if r.value is not None]
    failed = [r for r in rows if r.na_reason is NAReason.ENGINE_FAILED]
    na_other = [
        r
        for r in rows
        if r.value is None and r.na_reason is not NAReason.ENGINE_FAILED
    ]

    thieu_nang_luc = [r for r in na_other if r.na_reason is NAReason.MISSING_CAPABILITY]
    chua_nhan = [r for r in na_other if r.na_reason is not NAReason.MISSING_CAPABILITY]

    # Mẫu số của trung bình có phạt = chấm được + hỏng. Tài liệu N/A vì thiếu năng
    # lực KHÔNG vào mẫu số: engine không hứa làm việc đó thì không phạt nó ở đây,
    # đã có cột applicable/N-A nói thay.
    denom = len(scored) + len(failed)

    # `applicable` suy từ các tài liệu **không hỏng**, không từ `denom > 0`.
    #
    # Một tài liệu hỏng ở cấp engine sinh `ENGINE_FAILED` cho **mọi** metric, kể cả
    # metric engine không có năng lực chạm tới. Lấy `denom > 0` thì 10 tài liệu hỏng
    # đủ bật `applicable` cho cả 14 metric, và bảng in "— (10 hỏng, 0 chấm được)" ở
    # mọi ô — che mất 194 tài liệu chạy tốt và vu cho engine những năng lực nó chưa
    # bao giờ khai. Đã đọc nhầm `sovereign_light` là "hỏng toàn tập" vì đúng chỗ này
    # (2026-08-09).
    khong_hong = len(scored) + len(na_other)
    kha_dung = (
        # Không tài liệu nào chạy được ⇒ chưa biết năng lực; vẫn phải hiện dòng để
        # người đọc thấy engine hỏng, chứ N/A ở đây là giấu lỗi.
        denom > 0
        if khong_hong == 0
        else bool(scored or chua_nhan)
    )
    return Aggregate(
        metric=names.pop(),
        engine=engines.pop(),
        n_total=len(rows),
        n_scored=len(scored),
        n_failed=len(failed),
        n_na=len(na_other),
        mean=(sum(scored) / len(scored)) if scored else None,
        penalized_mean=(sum(scored) / denom) if denom else None,
        fail_rate=(len(failed) / denom) if denom else 0.0,
        applicable=kha_dung,
        n_thieu_nang_luc=len(thieu_nang_luc),
        n_chua_nhan=len(chua_nhan),
    )
