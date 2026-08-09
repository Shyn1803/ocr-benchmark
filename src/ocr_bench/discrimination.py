"""C2 — thước đo có phân biệt được engine không.

C1 hỏi *"metric có giữ đúng lời hứa của chính nó không"*. Đây là câu khó hơn:
**metric có tách được engine tốt khỏi engine tồi không.** Một metric qua sạch C1 vẫn
có thể cho mọi engine cùng một điểm, và một bảng xếp hạng như vậy trông hoàn toàn
bình thường.

Hai phép đo, hai câu hỏi khác nhau — đừng gộp:

* **Cổng `sabotage`** (`kiem_sabotage`): engine bị cố tình làm hỏng có bị xếp bét
  không. Metric nào không xếp nó bét thì metric đó **sai**.
* **Độ phân tán** (`do_phan_tan`): các engine **thật** có chênh nhau đủ để nói lên
  điều gì không. Chênh dưới `NGUONG_PHAN_TAN` thì metric ấy không đáng nằm ở bảng
  chính.

## Ba chỗ dễ đo ra số đẹp mà vô nghĩa

**1. `sabotage` không được vào phép tính phân tán.** Nó là engine tổng hợp, sinh ra
để *chắc chắn* tệ. Cho nó vào thì mọi metric đều "phân tán tốt" — ta chỉ đang đo lại
cổng `sabotage` một lần nữa dưới cái tên khác. `noop` cũng vậy: nó không xuất gì.
Xem `ENGINE_TONG_HOP`.

**2. Chỉ so trên tài liệu cả hai engine cùng chấm được.** `marker` có 20 tài liệu,
`opendataloader` có 204. So hai trung bình trên hai bộ tài liệu khác nhau là so hai
đại lượng khác nhau — chênh lệch thu được nói về **bộ mẫu**, không nói về engine.

**3. "Không đủ dữ liệu" khác "không phân biệt được".** Metric chỉ có một engine đo
được thì nó không *thất bại* phép thử phân tán — nó chưa được thử. Gộp hai thứ này
là cách chắc chắn nhất để vứt nhầm một metric tốt vì bộ mẫu còn thiếu nhãn.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import ClassVar

from ocr_bench.adapters.base import Adapter
from ocr_bench.metrics.base import Aggregate, aggregate
from ocr_bench.scorer import ScoreTable
from ocr_bench.types import Capability, MetricResult, OcrResult

__all__ = [
    "NGUONG_PHAN_TAN",
    "ENGINE_TONG_HOP",
    "NGUON_SABOTAGE",
    "PhanQuyet",
    "PhanTan",
    "KetQuaCong",
    "NguonTuDia",
    "do_phan_tan",
    "dung_sabotage",
    "kiem_sabotage",
    "phan_nhom_metric",
]

NGUONG_PHAN_TAN = 0.02
"""Chênh dưới mức này thì metric không phân biệt được engine.

Lấy nguyên văn từ `task.md` TASK-086 ("4 engine chênh nhau dưới 2%"). Nới con số này
là một quyết định về **cách công bố số**, không phải một chi tiết kỹ thuật — nó có
test khoá riêng để việc nới phải nhìn thấy được trong diff.
"""

ENGINE_TONG_HOP = frozenset({"sabotage", "noop"})
"""Engine không đại diện cho một công cụ OCR thật.

`noop` không xuất gì; `sabotage` cố tình làm hỏng đầu ra của engine khác. Cả hai đều
là **dụng cụ đo**, không phải đối tượng đo. Chúng vào cổng `sabotage` (nơi chúng có
ích) và bị loại khỏi phép tính phân tán (nơi chúng làm số đẹp lên một cách vô nghĩa).
"""

NGUON_SABOTAGE = "opendataloader"
"""Engine làm nguồn cho `sabotage`. Một chỗ khai duy nhất — có lý do.

`SabotageAdapter()` mặc định bọc `noop`, và `noop` trả **chuỗi rỗng**. Làm hỏng cái
rỗng thì vẫn rỗng: `sabotage` hoà `0.0000` với `noop` ở mọi metric, mà **hoà ở đáy
không phải đứng bét** — cổng C2 xanh trong khi chưa kiểm được gì. Nguồn phải là một
engine thật, và phải là engine mạnh nhất có mặt: làm hỏng đầu ra tốt mới là phép thử
có ý nghĩa.

Trước đây hằng số này nằm trong `scripts/c2_report.py`, còn `prediction/sabotage/`
trên đĩa lại do `make_predictions.py` sinh với nguồn mặc định `noop`. Hệ quả: **hai
quần thể `sabotage` khác nhau** cùng mang một cái tên — bảng công bố (D1) chấm bản
`noop` 41 tài liệu, cổng C2 chấm bản `opendataloader` 205 tài liệu. Hai con số không
nói về cùng một thứ, và không có gì trong bảng chỉ ra điều đó. Đặt hằng số ở tầng thư
viện + dựng qua :func:`dung_sabotage` là để đường sinh ra đĩa và đường gác cổng
**không thể** lệch nhau lần nữa.
"""


class PhanQuyet:
    """Ba kết cục của phép thử phân tán. Cái thứ ba **không** phải một dạng thất bại."""

    PHAN_BIET_DUOC = "phan_biet_duoc"
    KHONG_PHAN_BIET_DUOC = "khong_phan_biet_duoc"
    KHONG_DU_DU_LIEU = "khong_du_du_lieu"


@dataclasses.dataclass(frozen=True)
class PhanTan:
    """Độ phân tán của một metric trên các engine thật."""

    metric: str
    engines: tuple[str, ...]
    n_doc_chung: int
    diem: Mapping[str, float]
    thap_nhat: float | None
    cao_nhat: float | None
    spread: float | None
    phan_quyet: str
    ly_do: str

    @property
    def vao_bang_chinh(self) -> bool:
        """Chỉ metric phân biệt được mới vào bảng chính.

        `KHONG_DU_DU_LIEU` cũng nằm ngoài — không phải vì metric tệ mà vì chưa có gì
        để nói. Công bố một cột chưa được thử là mời người đọc tin vào nó.
        """
        return self.phan_quyet == PhanQuyet.PHAN_BIET_DUOC


@dataclasses.dataclass(frozen=True)
class KetQuaCong:
    """Kết quả cổng `sabotage` cho một metric."""

    metric: str
    dat: bool
    engine_bet: str | None
    diem_sabotage: float | None
    diem_nguon: float | None
    nguon: str
    ly_do: str

    @property
    def do_duoc(self) -> bool:
        """Cổng có chạy thật không, hay chỉ đi qua vì không có dữ liệu."""
        return self.diem_sabotage is not None and self.diem_nguon is not None


class NguonTuDia(Adapter):
    """Adapter trả lại `OcrResult` đã lưu — không đọc PDF, không chạy engine.

    `SabotageAdapter.run()` gọi `source.execute(doc_path)`, tức đòi một adapter sống.
    Nhưng dự đoán của nguồn đã nằm trên đĩa từ lần chạy trước, và chạy lại
    `opendataloader` trên 205 tài liệu chỉ để lấy đúng những kết quả ấy là lãng phí.

    Quan trọng hơn: cách này dùng **chính** `SabotageAdapter` thật chứ không chép lại
    phép làm hỏng. Chép lại thì C2 kiểm bản sao, không kiểm bản đang chạy.

    ⚠️ `capabilities` ở đây khai đủ ở cấp lớp, nhưng năng lực **thực tế** đi theo
    từng `OcrResult` trả về — đúng như `SabotageAdapter` làm (`capabilities=src.capabilities`).
    Khai thiếu ở đây thì `sabotage` trả N/A và **biến mất khỏi bảng** thay vì đứng
    bét, tức cổng C2 xanh mà không kiểm gì.
    """

    name: ClassVar[str] = "nguon_tu_dia"
    capabilities: ClassVar[frozenset[Capability]] = frozenset(Capability)

    def __init__(self, ket_qua: Iterable[OcrResult], *, ten: str | None = None) -> None:
        self._ket_qua = {r.doc_id: r for r in ket_qua}
        if not self._ket_qua:
            raise ValueError("NguonTuDia rỗng — cổng C2 sẽ xanh mà không kiểm gì")
        ten_nguon = {r.engine for r in self._ket_qua.values()}
        if len(ten_nguon) > 1:
            raise ValueError(f"trộn nhiều engine làm nguồn: {sorted(ten_nguon)}")
        self.ten_nguon = ten or ten_nguon.pop()

    @property
    def ten_engine_that(self) -> str:
        """Danh tính engine là của **nguồn**, không phải của lớp phát lại này.

        Nhờ đó `SabotageAdapter` bọc `NguonTuDia(opendataloader)` ghi ra
        `sabotage/1+opendataloader` chứ không phải `sabotage/1+nguon_tu_dia`.
        """
        return self.ten_nguon

    @property
    def doc_ids(self) -> list[str]:
        return sorted(self._ket_qua)

    def duong_dan(self) -> list[Path]:
        """Đường dẫn giả để đưa vào `SabotageAdapter.execute()`."""
        return [Path(f"{d}.pdf") for d in self.doc_ids]

    def version(self) -> str:
        return f"tu_dia/{self.ten_nguon}"

    def run(self, doc_path: Path) -> OcrResult:
        return self._ket_qua[doc_path.stem]


def dung_sabotage(
    ket_qua: Iterable[OcrResult], *, nguon: str = NGUON_SABOTAGE
) -> list[OcrResult]:
    """Dựng quần thể `sabotage` từ dự đoán đã lưu của `nguon`. **Một** đường duy nhất.

    Cả `scripts/c2_report.py` (gác cổng) lẫn `scripts/make_sabotage.py` (ghi xuống
    `prediction/`) đều gọi hàm này, nên bản đem chấm ở bảng công bố và bản đem gác
    cổng luôn là cùng một quần thể — xem :data:`NGUON_SABOTAGE` để biết chuyện gì đã
    xảy ra khi chúng không phải.

    Dùng **chính** `SabotageAdapter` chứ không chép lại phép làm hỏng: chép lại thì C2
    kiểm bản sao, không kiểm bản đang chạy.

    Ném nếu `nguon` không có dự đoán nào — dựng `sabotage` rỗng thì cổng xanh mà
    không kiểm gì, đúng cái lỗi hàm này sinh ra để chặn.
    """
    from ocr_bench.adapters.sabotage import SabotageAdapter

    goc = [r for r in ket_qua if r.engine == nguon]
    if not goc:
        raise ValueError(
            f"không có dự đoán nào của {nguon!r} — không dựng được `sabotage`. "
            f"Chạy engine đó trước, hoặc đổi `nguon=`."
        )
    tu_dia = NguonTuDia(goc)
    sa = SabotageAdapter(tu_dia)
    return [sa.execute(p) for p in tu_dia.duong_dan()]


def _rows(bang: ScoreTable, metric: str, engine: str) -> list[MetricResult]:
    return [r for r in bang.rows if r.metric == metric and r.engine == engine]


def _doc_cham_duoc(bang: ScoreTable, metric: str, engine: str) -> set[str]:
    """Tài liệu mà engine này thật sự ra được một con số cho metric này."""
    return {r.doc_id for r in _rows(bang, metric, engine) if r.value is not None}


def _gop_tren(
    bang: ScoreTable, metric: str, engine: str, docs: set[str]
) -> Aggregate:
    return aggregate(
        [r for r in _rows(bang, metric, engine) if r.doc_id in docs],
        metric=metric,
        engine=engine,
    )


def do_phan_tan(
    bang: ScoreTable,
    metric: str,
    *,
    engine_tong_hop: frozenset[str] = ENGINE_TONG_HOP,
    nguong: float = NGUONG_PHAN_TAN,
) -> PhanTan:
    """Chênh lệch lớn nhất giữa các engine **thật**, trên **bộ tài liệu chung**.

    `max - min` chứ không phải độ lệch chuẩn: câu hỏi là "metric có tách nổi engine
    tốt nhất khỏi engine tệ nhất không", đó là một khoảng chứ không phải một phương sai.
    """
    that = [e for e in bang.engines() if e not in engine_tong_hop]
    do_duoc = [e for e in that if _doc_cham_duoc_khong(bang, metric, e)]

    if len(do_duoc) < 2:
        return PhanTan(
            metric=metric,
            engines=tuple(do_duoc),
            n_doc_chung=0,
            diem={},
            thap_nhat=None,
            cao_nhat=None,
            spread=None,
            phan_quyet=PhanQuyet.KHONG_DU_DU_LIEU,
            ly_do=(
                f"chỉ {len(do_duoc)} engine thật đo được metric này "
                f"({', '.join(do_duoc) or 'không có engine nào'}) — cần ít nhất 2 "
                "để nói về phân tán. Thiếu nhãn, không phải metric hỏng."
            ),
        )

    chung: set[str] = set.intersection(
        *(_doc_cham_duoc(bang, metric, e) for e in do_duoc)
    )
    if not chung:
        return PhanTan(
            metric=metric,
            engines=tuple(do_duoc),
            n_doc_chung=0,
            diem={},
            thap_nhat=None,
            cao_nhat=None,
            spread=None,
            phan_quyet=PhanQuyet.KHONG_DU_DU_LIEU,
            ly_do=(
                f"{len(do_duoc)} engine đo được nhưng không tài liệu nào chung — "
                "so trung bình trên hai bộ mẫu khác nhau là so hai đại lượng khác nhau."
            ),
        )

    diem: dict[str, float] = {}
    for e in do_duoc:
        g = _gop_tren(bang, metric, e, chung)
        if g.penalized_mean is not None:
            diem[e] = g.penalized_mean

    if len(diem) < 2:
        return PhanTan(
            metric=metric,
            engines=tuple(sorted(diem)),
            n_doc_chung=len(chung),
            diem=diem,
            thap_nhat=None,
            cao_nhat=None,
            spread=None,
            phan_quyet=PhanQuyet.KHONG_DU_DU_LIEU,
            ly_do="sau khi giới hạn về bộ tài liệu chung chỉ còn dưới 2 engine có điểm.",
        )

    thap, cao = min(diem.values()), max(diem.values())
    spread = cao - thap
    if spread < nguong:
        pq, ly_do = (
            PhanQuyet.KHONG_PHAN_BIET_DUOC,
            f"spread {spread:.4f} < ngưỡng {nguong} trên {len(diem)} engine / "
            f"{len(chung)} tài liệu chung — metric này không nói lên điều gì về "
            "engine nào tốt hơn.",
        )
    else:
        pq, ly_do = (
            PhanQuyet.PHAN_BIET_DUOC,
            f"spread {spread:.4f} ≥ ngưỡng {nguong} trên {len(diem)} engine / "
            f"{len(chung)} tài liệu chung.",
        )

    return PhanTan(
        metric=metric,
        engines=tuple(sorted(diem)),
        n_doc_chung=len(chung),
        diem=diem,
        thap_nhat=thap,
        cao_nhat=cao,
        spread=spread,
        phan_quyet=pq,
        ly_do=ly_do,
    )


def _doc_cham_duoc_khong(bang: ScoreTable, metric: str, engine: str) -> bool:
    return bool(_doc_cham_duoc(bang, metric, engine))


def kiem_sabotage(
    bang: ScoreTable,
    metric: str,
    *,
    nguon: str,
    ten_sabotage: str = "sabotage",
) -> KetQuaCong:
    """`sabotage` có đứng bét không — và có đứng bét vì **điểm thấp** không.

    Ba chỗ phải khẳng định, thiếu chỗ nào cũng thành cổng rỗng:

    1. Nó phải **có mặt** và **đo được**. Đứng cuối vì N/A là đúng cái lỗi cổng này
       sinh ra để bắt, không phải bằng chứng cổng đạt.
    2. Bảng phải có từ 2 engine trở lên. Bảng một cột thì "đứng bét" là hiển nhiên.
    3. Điểm của nó phải **thấp hơn nguồn**, không chỉ "đứng cuối". Bằng điểm nguồn mà
       thắng ở khoá phụ (tên engine) cũng ra đứng cuối — và đó là metric hỏng.

    "Đo được" ở đây là `n_scored > 0`, **không** phải `applicable`. Hai thứ này khác
    nhau đúng ở một chỗ: engine chỉ toàn tài liệu `ENGINE_FAILED` có `applicable=True`
    và `penalized_mean = 0.0` — nó xuống bét ở **mọi** metric, kể cả metric hoàn hảo,
    vì nó đổ vỡ chứ không phải vì metric xếp được nó. Cho nó vào cổng thì cổng báo
    "METRIC NÀY SAI" về một chuyện metric không gây ra. `do_phan_tan()` đã dùng đúng
    tiêu chí này (`_doc_cham_duoc`); chỗ này chỉ là bù cho khớp.

    Đây **không** phải giấu engine hỏng: tỉ lệ hỏng vẫn hiện nguyên ở `fail_rate` và
    ở cột `N/A` của bảng chính — chỉ là nó không còn được dùng làm bằng chứng buộc tội
    metric.
    """
    xh = bang.ranking(metric)
    sab = next((a for a in xh if a.engine == ten_sabotage), None)
    src = next((a for a in xh if a.engine == nguon), None)

    if sab is None:
        return KetQuaCong(
            metric, False, xh[-1].engine if xh else None, None, None, nguon,
            f"`{ten_sabotage}` không có trong bảng — không thể đứng bét cái nó không có mặt.",
        )
    if src is None:
        return KetQuaCong(
            metric, False, xh[-1].engine if xh else None, None, None, nguon,
            f"nguồn `{nguon}` không có trong bảng.",
        )

    if not sab.n_scored or not src.n_scored:
        return KetQuaCong(
            metric, True, xh[-1].engine, None, None, nguon,
            f"metric không đo được ở đây (sabotage n_scored={sab.n_scored}, "
            f"{nguon} n_scored={src.n_scored}) — cổng KHÔNG chạy, không tính là đạt.",
        )

    do_duoc = [a for a in xh if a.n_scored > 0]
    if len(do_duoc) < 2:
        return KetQuaCong(
            metric, True, xh[-1].engine, sab.penalized_mean, src.penalized_mean, nguon,
            "chỉ 1 engine đo được — bảng một cột thì đứng bét là hiển nhiên, cổng KHÔNG chạy.",
        )

    bet = do_duoc[-1]
    dat = bet.engine == ten_sabotage and sab.penalized_mean < src.penalized_mean
    if dat:
        ly_do = (
            f"đứng bét trong {len(do_duoc)} engine đo được, "
            f"{sab.penalized_mean:.4f} < {nguon} {src.penalized_mean:.4f}."
        )
    elif bet.engine != ten_sabotage:
        ly_do = (
            f"engine bét là `{bet.engine}` ({bet.penalized_mean:.4f}), không phải "
            f"`{ten_sabotage}` ({sab.penalized_mean:.4f}) — METRIC NÀY SAI."
        )
    else:
        ly_do = (
            f"đứng cuối nhưng không thấp hơn nguồn: {sab.penalized_mean:.4f} ≥ "
            f"{nguon} {src.penalized_mean:.4f} — METRIC NÀY SAI."
        )
    return KetQuaCong(
        metric, dat, bet.engine, sab.penalized_mean, src.penalized_mean, nguon, ly_do
    )


def phan_nhom_metric(
    phan_tan: Sequence[PhanTan], *, moi_metric: Iterable[str]
) -> dict[str, list[dict[str, object]]]:
    """Chia metric làm **đúng hai** nhóm: bảng chính và phụ lục.

    Ràng theo danh sách metric đăng ký chứ không theo `phan_tan` truyền vào — quên
    một metric thì hàm này ném, không im lặng. Cùng cơ chế AC-04 của C1, vì cùng một
    loại thất bại.

    Xuống phụ lục **không phải** xoá metric: nó vẫn có số, vẫn có lý do, chỉ không
    nằm ở bảng người ta đọc để ra quyết định.
    """
    can = set(moi_metric)
    co = {p.metric for p in phan_tan}
    if can != co:
        thieu, thua = sorted(can - co), sorted(co - can)
        raise ValueError(f"lệch danh sách metric — thiếu {thieu}, thừa {thua}")

    def _dong(p: PhanTan) -> dict[str, object]:
        return {
            "metric": p.metric,
            "engines": list(p.engines),
            "n_doc_chung": p.n_doc_chung,
            "diem": {k: round(v, 4) for k, v in sorted(p.diem.items())},
            "spread": None if p.spread is None else round(p.spread, 4),
            "phan_quyet": p.phan_quyet,
            "ly_do": p.ly_do,
        }

    return {
        "nguong": NGUONG_PHAN_TAN,
        "bang_chinh": [_dong(p) for p in phan_tan if p.vao_bang_chinh],
        "phu_luc": [_dong(p) for p in phan_tan if not p.vao_bang_chinh],
    }
