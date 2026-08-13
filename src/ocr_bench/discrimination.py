"""C2 — thước đo có phân biệt được engine không.

C1 hỏi *"metric có giữ đúng lời hứa của chính nó không"*. Đây là câu khó hơn:
**metric có tách được engine tốt khỏi engine tồi không.** Một metric qua sạch C1 vẫn
có thể cho mọi engine cùng một điểm, và một bảng xếp hạng như vậy trông hoàn toàn
bình thường.

Hai phép đo, hai câu hỏi khác nhau — đừng gộp:

* **Cổng `sabotage`** (`kiem_sabotage`): engine bị cố tình làm hỏng có bị chấm thấp
  hơn **chính nguồn** của nó không. Không đạt thì metric đó **chưa được falsify** —
  cẩn thận, đó không đồng nghĩa với "metric sai": phép phá hiện có chỉ xoá chứ không
  bao giờ chèn, nên nó bất lực trước metric được thưởng khi văn bản ngắn đi
  (`assert_text_absence`, `assert_baseline`). Xem D-010 và TASK-097.
  "Có đứng bét toàn bảng không" **không** phải điều kiện đạt — nó trộn phép làm hỏng
  với chênh lệch năng lực giữa các engine.
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
    "KetQuaDonDieu",
    "NguonTuDia",
    "do_phan_tan",
    "dung_sabotage",
    "dung_sabotage_phan_muc",
    "kiem_sabotage",
    "kiem_don_dieu_muc",
    "phan_nhom_metric",
]

NGUONG_PHAN_TAN = 0.02
"""Chênh dưới mức này thì metric không phân biệt được engine.

Lấy nguyên văn từ `task.md` TASK-086 ("4 engine chênh nhau dưới 2%"). Nới con số này
là một quyết định về **cách công bố số**, không phải một chi tiết kỹ thuật — nó có
test khoá riêng để việc nới phải nhìn thấy được trong diff.
"""

def _ten_muc_tong_hop() -> frozenset[str]:
    from ocr_bench.adapters.sabotage import MUC_SABOTAGE, ten_muc_sabotage

    return frozenset(ten_muc_sabotage(s) for s in MUC_SABOTAGE)


ENGINE_TONG_HOP = frozenset({"sabotage", "noop"}) | _ten_muc_tong_hop()
"""Engine không đại diện cho một công cụ OCR thật.

Gồm cả ba mức `sabotage_s??`. Bỏ sót chúng ở đây là cách yên lặng nhất để hỏng bảng:
ba cột phá hoại sẽ được tính như engine thật trong `do_phan_tan`, và **mọi** metric
lập tức "phân tán tốt" — ta chỉ đang đo lại phép làm hỏng dưới một cái tên khác.

`noop` không xuất gì; `sabotage` cố tình làm hỏng đầu ra của engine khác. Cả hai đều
là **dụng cụ đo**, không phải đối tượng đo, nên cả hai bị loại khỏi phép tính phân
tán — ở đó chúng chỉ làm số đẹp lên một cách vô nghĩa.

Ở cổng `sabotage` thì `sabotage` là **chủ thể** của phép thử, còn `noop` vẫn bị loại:
nó là sàn theo cấu tạo, và "làm hỏng phải tệ hơn không có gì" là một đòi hỏi sai chứ
không phải một phép thử về thước đo. Xem `kiem_sabotage`.
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
    duoi_sabotage: tuple[str, ...] = ()
    """Engine **thật** chấm thấp hơn `sabotage`. Quan trắc, không phải phán quyết.

    Đây là kết luận về **engine**, không phải về thước đo — xem `kiem_sabotage`. Để
    trống ở hầu hết metric; không trống thì phải in ra, vì "một công cụ thật còn tệ
    hơn bản cố tình làm hỏng" là câu đáng đọc dù nó không kết tội metric.
    """

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


def dung_sabotage_phan_muc(
    ket_qua: Iterable[OcrResult],
    *,
    nguon: str = NGUON_SABOTAGE,
    muc: Sequence[float] | None = None,
    seed: int | None = None,
) -> list[OcrResult]:
    """Dựng **một quần thể riêng cho mỗi mức** phá hoại, cùng nguồn và cùng seed.

    Mỗi mức mang một tên engine riêng (`sabotage_s10`, `sabotage_s30`, `sabotage_s60`)
    để ba mức nằm thành ba cột trong bảng điểm. Nếu để chung một tên `sabotage` thì
    mức sau ghi đè mức trước và không còn gì để so.

    Đây là phép thử **mạnh hơn** cổng một điểm: cổng một điểm chỉ hỏi "metric có thấy
    phép làm hỏng không", còn ba mức hỏi "metric có xếp được **mức độ** hỏng không".
    Một metric tụt thẳng xuống sàn ở mức 0.1 rồi nằm im vẫn qua cổng một điểm, dù nó
    không phân biệt nổi tài liệu hỏng nhẹ với tài liệu hỏng nát.
    """
    from ocr_bench.adapters.sabotage import (
        MUC_SABOTAGE,
        SEED_SABOTAGE,
        SabotageAdapter,
        ten_muc_sabotage,
    )

    muc = tuple(MUC_SABOTAGE if muc is None else muc)
    seed = SEED_SABOTAGE if seed is None else seed

    goc = [r for r in ket_qua if r.engine == nguon]
    if not goc:
        raise ValueError(
            f"không có dự đoán nào của {nguon!r} — không dựng được `sabotage` phân mức."
        )
    tu_dia = NguonTuDia(goc)
    duong_dan = tu_dia.duong_dan()

    ra: list[OcrResult] = []
    for s in muc:
        sa = SabotageAdapter(tu_dia, seed=seed, severity=s, ten=ten_muc_sabotage(s))
        ra.extend(sa.execute(p) for p in duong_dan)
    return ra


@dataclasses.dataclass(frozen=True)
class KetQuaDonDieu:
    """Điểm có giảm theo **mức** phá hoại không.

    Bốn kết cục, không phải hai — gộp lại là mất đúng thông tin cần đọc:

    ``dat``
        Giảm ngặt qua từng mức: nguồn > 0.1 > 0.3 > 0.6. Metric xếp được mức hỏng.
    ``bao_hoa``
        Không tăng, nhưng có chỗ hoà. Metric chạm sàn (hoặc trần) rồi nằm im. Không
        kết tội metric — nhiều metric nhị phân *phải* bão hoà — nhưng phải in ra, vì
        nó nói rằng cột này không dùng để so hai bản hỏng với nhau được.
    ``nghich``
        Có mức nặng hơn lại được điểm **cao hơn** mức nhẹ hơn. Đây là hỏng thật:
        thước đo thưởng cho việc phá nhiều hơn.
    ``khong_do_duoc``
        Thiếu cột hoặc metric N/A. Chưa thử, không phải đã đạt.
    """

    DAT: ClassVar[str] = "dat"
    BAO_HOA: ClassVar[str] = "bao_hoa"
    NGHICH: ClassVar[str] = "nghich"
    KHONG_DO_DUOC: ClassVar[str] = "khong_do_duoc"

    metric: str
    nguon: str
    diem: Mapping[str, float]
    diem_nguon: float | None
    phan_quyet: str
    ly_do: str

    @property
    def do_duoc(self) -> bool:
        return self.phan_quyet != KetQuaDonDieu.KHONG_DO_DUOC


def kiem_don_dieu_muc(
    bang: ScoreTable,
    metric: str,
    *,
    nguon: str = NGUON_SABOTAGE,
    muc: Sequence[float] | None = None,
) -> KetQuaDonDieu:
    """Điểm phải giảm dần khi mức phá hoại tăng dần.

    Chỉ đọc bảng — quần thể ba mức phải được dựng trước bằng
    :func:`dung_sabotage_phan_muc` và chấm cùng bảng.
    """
    from ocr_bench.adapters.sabotage import MUC_SABOTAGE, ten_muc_sabotage

    muc = tuple(MUC_SABOTAGE if muc is None else muc)
    ten = [ten_muc_sabotage(s) for s in muc]

    xh = {a.engine: a for a in bang.ranking(metric)}
    src = xh.get(nguon)

    thieu = [t for t in ten if t not in xh or not xh[t].n_scored]
    if thieu or src is None or not src.n_scored:
        return KetQuaDonDieu(
            metric=metric,
            nguon=nguon,
            diem={},
            diem_nguon=None if src is None else src.penalized_mean,
            phan_quyet=KetQuaDonDieu.KHONG_DO_DUOC,
            ly_do=(
                f"không đo được: thiếu/N/A ở {thieu or [nguon]} — "
                "chưa thử thì không phải đã đạt."
            ),
        )

    diem = {t: xh[t].penalized_mean for t in ten}
    chuoi = [src.penalized_mean, *(diem[t] for t in ten)]
    nhan = [nguon, *ten]

    nghich = [
        f"{nhan[i + 1]} ({chuoi[i + 1]:.4f}) > {nhan[i]} ({chuoi[i]:.4f})"
        for i in range(len(chuoi) - 1)
        if chuoi[i + 1] > chuoi[i]
    ]
    if nghich:
        return KetQuaDonDieu(
            metric, nguon, diem, src.penalized_mean, KetQuaDonDieu.NGHICH,
            "phá nặng hơn lại được điểm cao hơn: " + "; ".join(nghich),
        )

    hoa = [
        f"{nhan[i]} = {nhan[i + 1]} ({chuoi[i]:.4f})"
        for i in range(len(chuoi) - 1)
        if chuoi[i + 1] == chuoi[i]
    ]
    if hoa:
        return KetQuaDonDieu(
            metric, nguon, diem, src.penalized_mean, KetQuaDonDieu.BAO_HOA,
            "không tăng nhưng bão hoà: " + "; ".join(hoa),
        )

    return KetQuaDonDieu(
        metric, nguon, diem, src.penalized_mean, KetQuaDonDieu.DAT,
        "giảm ngặt qua từng mức: "
        + " > ".join(f"{n} {v:.4f}" for n, v in zip(nhan, chuoi, strict=True)),
    )


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
    """Làm hỏng đầu ra của một engine thì điểm có **giảm** không.

    Phán quyết `dat` là **một** phép so duy nhất: `sabotage` phải thấp hơn chính
    **nguồn** của nó. Đó là phép cô lập được đúng một biến — cùng engine, cùng bộ tài
    liệu, chỉ khác chỗ đã bị làm hỏng. Metric không thấy sự khác biệt đó là metric sai.

    "`sabotage` có đứng bét toàn bảng không" **không** còn là điều kiện đạt: nó trộn
    phép làm hỏng với chênh lệch năng lực giữa các engine, nên nó kết tội thước đo vì
    một sự thật về engine. Vẫn tính, nhưng trả ra `duoi_sabotage` như quan trắc.

    Ba chỗ phải khẳng định trước khi cổng được coi là đã chạy, thiếu chỗ nào cũng
    thành cổng rỗng:

    1. Nó phải **có mặt** và **đo được**. Vắng mặt hoặc N/A là đúng cái lỗi cổng này
       sinh ra để bắt, không phải bằng chứng cổng đạt.
    2. Bảng phải có từ 2 engine **thật** trở lên. Bảng một cột thì so gì cũng vô nghĩa.
    3. Bằng điểm nguồn cũng là trượt — `<` chứ không phải `<=`. Hoà nghĩa là phép làm
       hỏng đi qua mà thước đo không nhúc nhích.

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

    # Chỉ so với engine **thật**. `noop` là sàn theo cấu tạo — nó không xuất gì, nên
    # trên mọi khẳng định kiểu "chữ này phải có mặt" nó luôn 0.0. Bắt `sabotage` phải
    # thấp hơn nó là bắt "làm hỏng" phải tệ hơn "không có gì", điều không đúng và
    # cũng không nói gì về chất lượng thước đo: bản làm hỏng vẫn giữ lại một phần nội
    # dung đúng, nên nó *phải* trên bản rỗng. Module này đã loại engine tổng hợp khỏi
    # `do_phan_tan` vì đúng lý do đó (xem `ENGINE_TONG_HOP` và §1 của docstring); chỗ
    # này trước đây quên áp, nên cổng báo "METRIC NÀY SAI" cho 4 metric chỉ vì `noop`
    # nằm dưới `sabotage` (2026-08-10).
    #
    # Điều kiện 3 (thấp hơn nguồn) KHÔNG đổi — đó mới là phép phản chứng thật, và nó
    # vẫn bắt được `assert_baseline` (hoà với nguồn) lẫn `assert_text_absence`
    # (sabotage *cao hơn* nguồn).
    bo_qua = ENGINE_TONG_HOP - {ten_sabotage}
    do_duoc = [a for a in xh if a.n_scored > 0 and a.engine not in bo_qua]
    if len(do_duoc) < 2:
        return KetQuaCong(
            metric, True, xh[-1].engine, sab.penalized_mean, src.penalized_mean, nguon,
            "chỉ 1 engine đo được — bảng một cột thì đứng bét là hiển nhiên, cổng KHÔNG chạy.",
        )

    bet = do_duoc[-1]
    # Phán quyết = **chỉ** phép so với nguồn. Đó là phép duy nhất cô lập được đúng một
    # biến: cùng engine, cùng bộ tài liệu, khác nhau mỗi chỗ đã bị làm hỏng. Metric
    # nào không thấy sự khác biệt ấy là metric sai — không cần thêm điều kiện nào.
    #
    # "Ai đứng bét" thì KHÔNG cô lập được biến nào: nó trộn phép làm hỏng với chênh
    # lệch **năng lực** giữa các engine. `pdf_inspector` được 0.0000 ở
    # `assert_math_presence` vì nó thật sự không xuất công thức — một thước đo hoàn
    # hảo vẫn phải xếp nó dưới bản `opendataloader` đã bị làm hỏng. Giữ nó làm điều
    # kiện đạt/trượt là kết tội thước đo vì một sự thật về engine (2026-08-10).
    #
    # Nên nó xuống hạng **quan trắc**: vẫn tính, vẫn in ra ở `duoi_sabotage`, nhưng
    # không bật đèn đỏ. Đây là nới cổng ở một chiều và phải nhìn thấy được: hai test
    # khoá riêng ở `TestCongSabotage` giữ chiều còn lại (`test_loai_noop_...`,
    # `test_engine_that_nam_duoi_sabotage_...`).
    duoi = tuple(
        a.engine
        for a in do_duoc
        if a.engine != ten_sabotage and a.penalized_mean < sab.penalized_mean
    )
    dat = sab.penalized_mean < src.penalized_mean
    if dat:
        ly_do = (
            f"thấp hơn nguồn: {sab.penalized_mean:.4f} < {nguon} "
            f"{src.penalized_mean:.4f}."
        )
        if duoi:
            ly_do += (
                f" (Quan trắc, không phải lỗi metric: {', '.join(f'`{e}`' for e in duoi)}"
                f" còn thấp hơn cả bản làm hỏng.)"
            )
    else:
        ly_do = (
            f"KHÔNG thấp hơn nguồn: {sab.penalized_mean:.4f} ≥ {nguon} "
            f"{src.penalized_mean:.4f} — METRIC NÀY SAI, làm hỏng đầu ra mà điểm "
            f"không giảm."
        )
    return KetQuaCong(
        metric, dat, bet.engine, sab.penalized_mean, src.penalized_mean, nguon, ly_do,
        duoi,
    )


def phan_nhom_metric(
    phan_tan: Sequence[PhanTan],
    *,
    moi_metric: Iterable[str],
    cong: Mapping[str, KetQuaCong] | None = None,
) -> dict[str, list[dict[str, object]]]:
    """Chia metric làm **đúng hai** nhóm: bảng chính và phụ lục.

    Ràng theo danh sách metric đăng ký chứ không theo `phan_tan` truyền vào — quên
    một metric thì hàm này ném, không im lặng. Cùng cơ chế AC-04 của C1, vì cùng một
    loại thất bại.

    Xuống phụ lục **không phải** xoá metric: nó vẫn có số, vẫn có lý do, chỉ không
    nằm ở bảng người ta đọc để ra quyết định.

    Hai điều kiện để **được** ở bảng chính, không phải một:

    1. Phân tán đủ (`vao_bang_chinh`) — các engine chênh nhau đủ để nói lên điều gì.
    2. **Qua cổng `sabotage`** — làm hỏng đầu ra thì điểm phải giảm.

    Điều kiện 2 trước đây không được áp ở đây, nên một metric trượt cổng vẫn lọt vào
    bảng người ta đọc để chọn engine. Đó là lỗ hổng nghiêm trọng hơn cả cái nó bỏ
    sót: `assert_text_absence` phân tán rất đẹp (0.5) *và* thưởng điểm cho việc phá
    tài liệu — đúng loại metric trông thuyết phục nhất trong khi sai nhất
    (2026-08-10). `cong=None` giữ nguyên hành vi cũ cho chỗ gọi chưa có kết quả cổng.
    """
    can = set(moi_metric)
    co = {p.metric for p in phan_tan}
    if can != co:
        thieu, thua = sorted(can - co), sorted(co - can)
        raise ValueError(f"lệch danh sách metric — thiếu {thieu}, thừa {thua}")

    def _truot_cong(m: str) -> KetQuaCong | None:
        k = (cong or {}).get(m)
        return k if k is not None and k.do_duoc and not k.dat else None

    def _dong(p: PhanTan) -> dict[str, object]:
        k = _truot_cong(p.metric)
        return {
            "metric": p.metric,
            "engines": list(p.engines),
            "n_doc_chung": p.n_doc_chung,
            "diem": {k2: round(v, 4) for k2, v in sorted(p.diem.items())},
            "spread": None if p.spread is None else round(p.spread, 4),
            "phan_quyet": p.phan_quyet,
            "ly_do": p.ly_do,
            "truot_cong_sabotage": None if k is None else k.ly_do,
        }

    def _vao_chinh(p: PhanTan) -> bool:
        return p.vao_bang_chinh and _truot_cong(p.metric) is None

    return {
        "nguong": NGUONG_PHAN_TAN,
        "bang_chinh": [_dong(p) for p in phan_tan if _vao_chinh(p)],
        "phu_luc": [_dong(p) for p in phan_tan if not _vao_chinh(p)],
    }
