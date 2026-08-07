"""C2 — cổng phân biệt: thước đo có tách nổi engine tốt khỏi engine tồi không.

Hai loại test trong file này, đừng lẫn:

* **Test tính chất trên dữ liệu dựng sẵn** — chạy ở mọi máy, không cần corpus. Chúng
  kiểm *logic* của `discrimination.py`: cổng có bắt được metric xếp sai không, có
  phân biệt "chênh ít" với "chưa đủ dữ liệu" không.
* **Test trên corpus thật** — cần `ground-truth/`, đánh dấu `needs_corpus`. Chúng
  kiểm *bộ mẫu hiện tại*, và kết quả của chúng đổi khi bộ mẫu đổi.

Loại thứ nhất là cổng. Loại thứ hai là quan trắc. Một cổng chỉ chạy khi có corpus là
một cổng thường xuyên không chạy.

## Cái bẫy trung tâm của cả file

Một cổng `sabotage` viết cẩu thả sẽ **xanh mà không kiểm gì**, theo ít nhất bốn cách,
và tất cả bốn đều trông giống nhau từ ngoài:

1. `sabotage` không có trong bảng → "không có ai xếp trên nó".
2. `sabotage` có mặt nhưng `applicable=False` → xuống cuối vì N/A, không phải vì kém.
3. Bảng chỉ có 1 engine → đứng bét là hiển nhiên.
4. `sabotage` bằng điểm nguồn, thắng ở khoá phụ (tên engine) → vẫn ra đứng cuối.

Vì vậy `kiem_sabotage` trả thêm `do_duoc`, và mọi test dưới đây khẳng định **`do_duoc`
trước** rồi mới tới `dat`. Xem `test_cong_khong_chay_thi_khong_duoc_tinh_la_dat`.

Có một cách hỏng thứ năm, ngược chiều: cổng **đỏ mà không phải lỗi metric**. Engine
chỉ toàn `ENGINE_FAILED` có `penalized_mean = 0.0` nên xuống bét ở *mọi* metric —
buộc tội metric vì một engine đổ vỡ. Xem `test_engine_chi_toan_hong_khong_ket_toi_metric`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ocr_bench import discrimination as D
from ocr_bench import registry
from ocr_bench.adapters.sabotage import SabotageAdapter
from ocr_bench.discrimination import PhanQuyet
from ocr_bench.prediction import load_predictions
from ocr_bench.scorer import ScoreTable, score_results
from ocr_bench.types import Capability, MetricResult, NAReason, OcrResult

GOC = Path(__file__).resolve().parents[1]
NGUON_MANH = "opendataloader"
"""Engine mạnh nhất hiện có làm nguồn cho `sabotage`.

Nguồn mặc định của `SabotageAdapter` là `NoopAdapter`, mà `noop` không xuất gì — làm
hỏng đầu ra rỗng thì vẫn rỗng, và cổng thành một phép so hai số 0. Nợ này đã ghi ở
`TASK-085/review.md` §7. Chọn nguồn ở đây là **lựa chọn có ý thức**, không phải mặc định.
"""


# ---------------------------------------------------------------- dữ liệu dựng sẵn


def _dong(metric: str, engine: str, doc: str, value: float | None) -> MetricResult:
    return MetricResult(
        metric=metric,
        engine=engine,
        doc_id=doc,
        value=value,
        na_reason=None if value is not None else NAReason.MISSING_CAPABILITY,
    )


def _bang(diem: dict[str, dict[str, float | None]], metric: str = "m") -> ScoreTable:
    """`{engine: {doc: value}}` → `ScoreTable`. `None` = engine không đo được doc đó."""
    return ScoreTable(
        tuple(
            _dong(metric, e, d, v)
            for e, docs in diem.items()
            for d, v in docs.items()
        )
    )


# ------------------------------------------------------- AC-01: cổng sabotage


class TestCongSabotage:
    """AC-01 — `sabotage` phải đứng BÉT ở mọi metric."""

    def test_bat_duoc_metric_xep_sai(self) -> None:
        """Metric xếp `sabotage` trên nguồn ⇒ cổng phải ĐỎ.

        Đây là lý do cổng tồn tại. Test này đỏ nghĩa là cổng hỏng, không phải metric hỏng.
        """
        bang = _bang({NGUON_MANH: {"a": 0.3}, "sabotage": {"a": 0.9}})
        kq = D.kiem_sabotage(bang, "m", nguon=NGUON_MANH)
        assert kq.do_duoc, "cổng phải chạy được trên dữ liệu này"
        assert not kq.dat
        assert kq.engine_bet == NGUON_MANH
        assert "METRIC NÀY SAI" in kq.ly_do

    def test_dat_khi_sabotage_thap_hon_nguon(self) -> None:
        bang = _bang({NGUON_MANH: {"a": 0.9}, "sabotage": {"a": 0.2}})
        kq = D.kiem_sabotage(bang, "m", nguon=NGUON_MANH)
        assert kq.do_duoc and kq.dat
        assert kq.engine_bet == "sabotage"

    def test_bang_diem_nguon_khong_duoc_tinh_la_dat(self) -> None:
        """Bằng điểm nguồn mà vẫn "đứng cuối" — vì `ranking()` phá hoà bằng tên engine.

        `sorted(..., reverse=True)` với khoá `(applicable, mean, engine)`: `"sabotage"`
        đứng sau `"opendataloader"` theo alphabet, đảo chiều thành đứng **trước**...
        tuỳ tên engine. Nói cách khác, ở thế hoà, ai đứng bét do **tên** quyết định.
        Một metric cho mọi engine cùng điểm sẽ đi qua phép thử "đứng bét" khoảng một nửa
        số lần — đúng loại cổng tệ nhất: đôi khi xanh.
        """
        bang = _bang({NGUON_MANH: {"a": 0.5}, "sabotage": {"a": 0.5}})
        kq = D.kiem_sabotage(bang, "m", nguon=NGUON_MANH)
        assert kq.do_duoc
        assert not kq.dat, "hoà điểm với nguồn không phải là 'tệ hơn nguồn'"

    def test_cong_khong_chay_thi_khong_duoc_tinh_la_dat(self) -> None:
        """`sabotage` N/A ⇒ `do_duoc` False. `dat` có thể True nhưng vô nghĩa.

        Đây là chỗ nguy hiểm nhất: metric không đo được thì `sabotage` xuống cuối bảng
        **vì N/A**, và một cổng chỉ nhìn "ai đứng cuối" sẽ báo đạt. Ta không cho nó
        đỏ (không đo được không phải lỗi metric) nhưng bắt buộc phải phân biệt được —
        báo cáo chỉ đếm những cổng có `do_duoc`.
        """
        bang = _bang({NGUON_MANH: {"a": 0.9}, "sabotage": {"a": None}})
        kq = D.kiem_sabotage(bang, "m", nguon=NGUON_MANH)
        assert not kq.do_duoc
        assert "KHÔNG chạy" in kq.ly_do

    def test_mot_engine_thi_dung_bet_la_hien_nhien(self) -> None:
        bang = _bang({NGUON_MANH: {"a": None}, "sabotage": {"a": 0.2}})
        kq = D.kiem_sabotage(bang, "m", nguon=NGUON_MANH)
        assert not kq.do_duoc

    def test_sabotage_vang_mat_khong_phai_la_dat(self) -> None:
        """Engine không có trong bảng thì cũng không đứng bét được.

        `ranking()` cố ý giữ cả engine `applicable=False` lại đúng để phân biệt
        "đứng bét" với "không xuất hiện"; test này canh cho phần còn lại của cổng
        không tự ý coi vắng mặt là đạt.
        """
        bang = _bang({NGUON_MANH: {"a": 0.9}})
        kq = D.kiem_sabotage(bang, "m", nguon=NGUON_MANH)
        assert not kq.dat and not kq.do_duoc
        assert "không có trong bảng" in kq.ly_do

    def test_engine_chi_toan_hong_khong_ket_toi_metric(self) -> None:
        """Engine chỉ toàn `ENGINE_FAILED` không được coi là "engine bét".

        `aggregate()` cho nó `penalized_mean = 0.0` (đúng: hỏng thì bị phạt) và
        `applicable = True` (mẫu số > 0). Nhưng con số 0.0 ấy giống hệt nhau ở **mọi**
        metric — nó nói engine đổ vỡ, không nói metric xếp hạng ra sao. Lấy nó làm
        engine bét thì cổng báo "METRIC NÀY SAI" cho một metric hoàn toàn lành.

        Ca thật: `sovereign_light` hỏng 10 tài liệu và không khai `IMAGE_BBOX`, nên ở
        `img_f1` nó có đúng 0 tài liệu chấm được và 10 tài liệu hỏng → 0.0000, thấp hơn
        `sabotage` (0.1446). TASK-091 phát hiện khi 206 file dự đoán bị bỏ quên được nạp
        trở lại.
        """
        rows = (
            *(_dong("m", NGUON_MANH, d, v) for d, v in {"a": 0.9, "b": 0.8}.items()),
            *(_dong("m", "sabotage", d, v) for d, v in {"a": 0.2, "b": 0.1}.items()),
            MetricResult(
                metric="m",
                engine="do_vo",
                doc_id="a",
                value=None,
                na_reason=NAReason.ENGINE_FAILED,
            ),
        )
        bang = ScoreTable(rows)
        do_vo = next(a for a in bang.ranking("m") if a.engine == "do_vo")
        assert do_vo.applicable and do_vo.penalized_mean == 0.0, (
            "tiền đề của test: engine hỏng toàn tập vẫn applicable với điểm 0.0"
        )

        kq = D.kiem_sabotage(bang, "m", nguon=NGUON_MANH)
        assert kq.do_duoc and kq.dat, kq.ly_do
        assert kq.engine_bet == "sabotage"


# ------------------------------------------------------ AC-02: độ phân tán


class TestPhanTan:
    """AC-02 — spread dưới ngưỡng ⇒ đánh dấu 'không phân biệt được'."""

    def test_chenh_it_thi_khong_phan_biet_duoc(self) -> None:
        bang = _bang(
            {"marker": {"a": 0.500}, NGUON_MANH: {"a": 0.510}, "pdf_inspector": {"a": 0.505}}
        )
        p = D.do_phan_tan(bang, "m")
        assert p.phan_quyet == PhanQuyet.KHONG_PHAN_BIET_DUOC
        assert p.spread == pytest.approx(0.01)
        assert not p.vao_bang_chinh

    def test_chenh_nhieu_thi_phan_biet_duoc(self) -> None:
        bang = _bang({"marker": {"a": 0.90}, NGUON_MANH: {"a": 0.30}})
        p = D.do_phan_tan(bang, "m")
        assert p.phan_quyet == PhanQuyet.PHAN_BIET_DUOC
        assert p.spread == pytest.approx(0.60)
        assert p.vao_bang_chinh

    def test_sabotage_khong_duoc_vao_phep_tinh_phan_tan(self) -> None:
        """Cho engine tổng hợp vào thì **mọi** metric đều "phân tán tốt".

        `sabotage` sinh ra để chắc chắn tệ; đưa nó vào là đo lại cổng AC-01 một lần
        nữa dưới cái tên khác, và AC-02 mất sạch tác dụng. Test này khoá điều đó:
        cùng một bảng, thêm `sabotage` điểm 0.0 mà phán quyết **không được** đổi.
        """
        diem = {"marker": {"a": 0.500}, NGUON_MANH: {"a": 0.505}}
        khong_sab = D.do_phan_tan(_bang(diem), "m")
        co_sab = D.do_phan_tan(_bang({**diem, "sabotage": {"a": 0.0}}), "m")
        assert khong_sab.phan_quyet == co_sab.phan_quyet == PhanQuyet.KHONG_PHAN_BIET_DUOC
        assert co_sab.spread == pytest.approx(khong_sab.spread)
        assert "sabotage" not in co_sab.engines

    def test_noop_cung_bi_loai(self) -> None:
        diem = {"marker": {"a": 0.500}, NGUON_MANH: {"a": 0.505}}
        co_noop = D.do_phan_tan(_bang({**diem, "noop": {"a": 0.0}}), "m")
        assert co_noop.phan_quyet == PhanQuyet.KHONG_PHAN_BIET_DUOC
        assert "noop" not in co_noop.engines

    def test_chi_so_tren_bo_tai_lieu_chung(self) -> None:
        """Hai engine chấm hai bộ tài liệu khác nhau ⇒ chênh lệch nói về **bộ mẫu**.

        `marker` dễ ở `a`, `opendataloader` khó ở `b`: so trung bình toàn phần cho
        spread 0.6, nhưng trên tài liệu **cả hai cùng chấm** (`a`) thì chỉ 0.01.
        Con số thứ hai mới là câu trả lời cho "metric có tách được engine không".
        """
        bang = _bang(
            {
                "marker": {"a": 0.90, "b": None},
                NGUON_MANH: {"a": 0.89, "b": 0.30},
            }
        )
        p = D.do_phan_tan(bang, "m")
        assert p.n_doc_chung == 1
        assert p.spread == pytest.approx(0.01)
        assert p.phan_quyet == PhanQuyet.KHONG_PHAN_BIET_DUOC

    def test_khong_du_du_lieu_khac_khong_phan_biet_duoc(self) -> None:
        """Một engine đo được ⇒ metric **chưa được thử**, không phải đã trượt.

        Gộp hai kết cục này là cách chắc chắn nhất để vứt nhầm một metric tốt chỉ vì
        bộ mẫu còn thiếu nhãn. Đây là kết cục của 11/14 metric hiện tại
        (xem `TestCorpusThat`), nên phân biệt được nó không phải chuyện lý thuyết.
        """
        bang = _bang({NGUON_MANH: {"a": 0.9}, "marker": {"a": None}})
        p = D.do_phan_tan(bang, "m")
        assert p.phan_quyet == PhanQuyet.KHONG_DU_DU_LIEU
        assert p.spread is None
        assert not p.vao_bang_chinh

    def test_khong_tai_lieu_chung_cung_la_khong_du_du_lieu(self) -> None:
        bang = _bang({"marker": {"a": 0.9, "b": None}, NGUON_MANH: {"a": None, "b": 0.3}})
        p = D.do_phan_tan(bang, "m")
        assert p.phan_quyet == PhanQuyet.KHONG_DU_DU_LIEU
        assert p.n_doc_chung == 0

    def test_ngay_tai_nguong_thi_phan_biet_duoc(self) -> None:
        """Biên `>=` chứ không `>`. Ngưỡng là "dưới 2% thì bỏ", nên đúng 2% thì giữ."""
        bang = _bang({"marker": {"a": 0.50}, NGUON_MANH: {"a": 0.50 + D.NGUONG_PHAN_TAN}})
        assert D.do_phan_tan(bang, "m").phan_quyet == PhanQuyet.PHAN_BIET_DUOC

    def test_nguong_dung_bang_hai_phan_tram(self) -> None:
        """Khoá con số vào test.

        Nới ngưỡng là quyết định về **cách công bố số**, không phải một hằng số kỹ
        thuật — nó phải hiện ra trong diff chứ không lặng lẽ trôi đi. 0.02 lấy nguyên
        văn từ `task.md` TASK-086.
        """
        assert D.NGUONG_PHAN_TAN == 0.02


# ------------------------------------------------- AC-03: phân nhóm bảng chính


class TestPhanNhom:
    """AC-03 — metric không phân biệt được bị chuyển khỏi bảng chính, có ghi lý do."""

    def test_moi_metric_thuoc_dung_mot_nhom(self) -> None:
        pt = [
            D.do_phan_tan(_bang({"marker": {"a": 0.9}, NGUON_MANH: {"a": 0.1}}, "x"), "x"),
            D.do_phan_tan(_bang({"marker": {"a": 0.50}, NGUON_MANH: {"a": 0.505}}, "y"), "y"),
            D.do_phan_tan(_bang({NGUON_MANH: {"a": 0.9}}, "z"), "z"),
        ]
        nhom = D.phan_nhom_metric(pt, moi_metric=["x", "y", "z"])
        chinh = {d["metric"] for d in nhom["bang_chinh"]}
        phu = {d["metric"] for d in nhom["phu_luc"]}
        assert chinh == {"x"}
        assert phu == {"y", "z"}
        assert not (chinh & phu), "không metric nào được nằm ở cả hai nhóm"

    def test_moi_dong_deu_co_ly_do_khac_rong(self) -> None:
        """AC-03 đòi "có ghi lý do" — một bảng phụ lục không lý do là một bảng bị xoá."""
        pt = [D.do_phan_tan(_bang({"marker": {"a": 0.50}, NGUON_MANH: {"a": 0.505}}, "y"), "y")]
        nhom = D.phan_nhom_metric(pt, moi_metric=["y"])
        assert nhom["phu_luc"], "fixture phải rơi xuống phụ lục thì test mới có nghĩa"
        for d in nhom["bang_chinh"] + nhom["phu_luc"]:
            assert d["ly_do"].strip(), f"{d['metric']} xuống phụ lục mà không nói vì sao"

    def test_thieu_metric_thi_nem_chu_khong_im_lang(self) -> None:
        """Cùng cơ chế AC-04 của C1: quên một metric phải ĐỎ, không được lặng lẽ bỏ qua."""
        pt = [D.do_phan_tan(_bang({"marker": {"a": 0.9}, NGUON_MANH: {"a": 0.1}}, "x"), "x")]
        with pytest.raises(ValueError, match="thiếu"):
            D.phan_nhom_metric(pt, moi_metric=["x", "y"])

    def test_thua_metric_cung_nem(self) -> None:
        pt = [
            D.do_phan_tan(_bang({"marker": {"a": 0.9}, NGUON_MANH: {"a": 0.1}}, t), t)
            for t in ("x", "thua")
        ]
        with pytest.raises(ValueError, match="thừa"):
            D.phan_nhom_metric(pt, moi_metric=["x"])


# --------------------------------------------------------- canh chính bộ đo


class TestNguonTuDia:
    """Canh cái adapter dùng để dựng `sabotage` — nó cũng hỏng im lặng được."""

    def _kq(self, doc: str, engine: str = NGUON_MANH) -> OcrResult:
        return OcrResult(
            engine=engine,
            engine_version="test",
            doc_id=doc,
            text_md="xin chào",
            capabilities=frozenset({Capability.TEXT_MD}),
        )

    def test_tra_lai_dung_ket_qua_da_luu(self) -> None:
        n = D.NguonTuDia([self._kq("a"), self._kq("b")])
        assert n.run(Path("a.pdf")).doc_id == "a"
        assert n.doc_ids == ["a", "b"]

    def test_rong_thi_nem(self) -> None:
        """Nguồn rỗng ⇒ 0 kết quả sabotage ⇒ cổng xanh mà không kiểm gì."""
        with pytest.raises(ValueError, match="rỗng"):
            D.NguonTuDia([])

    def test_tron_nhieu_engine_thi_nem(self) -> None:
        """Trộn nguồn thì "làm hỏng đầu ra của engine mạnh nhất" không còn đúng nữa."""
        with pytest.raises(ValueError, match="trộn nhiều engine"):
            D.NguonTuDia([self._kq("a"), self._kq("b", engine="marker")])

    def test_sabotage_thua_ke_nang_luc_cua_nguon(self) -> None:
        """Năng lực đi theo từng `OcrResult`, không theo lớp adapter.

        Khai thiếu ở `NguonTuDia` thì `sabotage` trả N/A và **biến mất khỏi bảng** thay
        vì đứng bét — cổng AC-01 sẽ xanh mà không kiểm gì (đúng nhánh
        `test_cong_khong_chay_thi_khong_duoc_tinh_la_dat`).
        """
        nang_luc = frozenset({Capability.TEXT_MD, Capability.IMAGE_BBOX})
        kq = OcrResult(
            engine=NGUON_MANH,
            engine_version="test",
            doc_id="a",
            text_md="xin chào",
            capabilities=nang_luc,
        )
        sab = SabotageAdapter(D.NguonTuDia([kq])).execute(Path("a.pdf"))
        assert not sab.failed
        assert sab.capabilities == nang_luc

    def test_khong_dung_nguon_mac_dinh(self) -> None:
        """`SabotageAdapter()` không nguồn ⇒ `noop` ⇒ cổng rỗng. Nợ ghi ở TASK-085 §7."""
        assert SabotageAdapter().source.name == "noop"
        assert NGUON_MANH != "noop"


# ------------------------------------------------------------ corpus thật


@pytest.fixture(scope="module")
def bang_that() -> ScoreTable:
    """Chấm lại toàn bộ dự đoán trên đĩa + `sabotage` dựng từ engine mạnh nhất.

    Không chạy engine nào: `NguonTuDia` trả lại dự đoán đã lưu, còn `SabotageAdapter`
    **thật** làm phần làm hỏng. Dùng adapter thật chứ không chép lại phép làm hỏng —
    chép lại thì C2 kiểm bản sao, không kiểm bản đang chạy.
    """
    corpus = pytest.importorskip("ocr_bench.corpus")
    gt: dict = {}
    gt.update(corpus.load_doclaynet())
    gt.update(corpus.load_olmocr())

    res = load_predictions(GOC / "prediction")
    nguon = [r for r in res if r.engine == NGUON_MANH]
    if not nguon:
        pytest.skip(f"không có dự đoán nào của {NGUON_MANH}")

    tu_dia = D.NguonTuDia(nguon)
    sa = SabotageAdapter(tu_dia)
    sab = [sa.execute(p) for p in tu_dia.duong_dan()]

    ten = sorted(registry.list_metrics())
    metrics = [registry.get_metric(t)() for t in ten]
    return score_results([r for r in res if r.engine != "sabotage"] + sab, metrics, gt)


@pytest.mark.needs_corpus
class TestCorpusThat:
    """Quan trắc bộ mẫu hiện tại. Các con số ở đây **đổi khi bộ mẫu đổi**."""

    def test_ac01_moi_metric_do_duoc_deu_xep_sabotage_bet(
        self, bang_that: ScoreTable
    ) -> None:
        """AC-01 trên dữ liệu thật — chỉ phán ở metric cổng **chạy được**.

        Metric không đo được thì cổng không chạy; coi nó là "đạt" là tự lừa mình, và
        coi nó là "trượt" là đổ lỗi cho metric vì bộ mẫu thiếu nhãn. Nó được đếm riêng
        ở `test_bao_cao_so_metric_cong_thuc_su_chay`.
        """
        hong = []
        for m in sorted(registry.list_metrics()):
            kq = D.kiem_sabotage(bang_that, m, nguon=NGUON_MANH)
            if kq.do_duoc and not kq.dat:
                hong.append(f"{m}: {kq.ly_do}")
        assert not hong, "metric xếp sai `sabotage`:\n" + "\n".join(hong)

    def test_bao_cao_so_metric_cong_thuc_su_chay(self, bang_that: ScoreTable) -> None:
        """Đếm to lên: cổng AC-01 hiện chạy trên **bao nhiêu** trong 14 metric.

        Test này không phán đúng/sai, nó chống một kiểu tự lừa: "AC-01 xanh" nghe như
        14/14 metric đã được kiểm, trong khi thực tế chỉ vài cái. Nó đỏ nếu con số
        tụt về 0 — lúc đó AC-01 xanh mà không kiểm gì cả.
        """
        chay = [
            m
            for m in sorted(registry.list_metrics())
            if D.kiem_sabotage(bang_that, m, nguon=NGUON_MANH).do_duoc
        ]
        assert chay, (
            "KHÔNG metric nào chạy được cổng sabotage — AC-01 xanh mà không kiểm gì. "
            "Nguyên nhân gần như chắc chắn nằm ở bộ mẫu, không ở metric."
        )

    def test_phan_nhom_bao_phu_du_14_metric(self, bang_that: ScoreTable) -> None:
        ten = sorted(registry.list_metrics())
        pt = [D.do_phan_tan(bang_that, m) for m in ten]
        nhom = D.phan_nhom_metric(pt, moi_metric=ten)
        assert len(nhom["bang_chinh"]) + len(nhom["phu_luc"]) == len(ten)

    def test_metric_thieu_du_lieu_khong_bi_ghi_nham_la_hong(
        self, bang_that: ScoreTable
    ) -> None:
        """Phần lớn phụ lục hiện nay là `khong_du_du_lieu`, và đó là chuyện của bộ mẫu.

        Ghi nhầm chúng thành `khong_phan_biet_duoc` là kết tội metric vì DocLayNet
        không có nhãn chữ và không engine mạnh nào có dự đoán trên corpus olmOCR.
        """
        for m in sorted(registry.list_metrics()):
            p = D.do_phan_tan(bang_that, m)
            if p.phan_quyet == PhanQuyet.KHONG_PHAN_BIET_DUOC:
                assert p.spread is not None, f"{m}: kết tội mà không có số"
                assert len(p.diem) >= 2, f"{m}: kết tội mà chỉ có {len(p.diem)} engine"


# ------------------------------------------------- lỗ hổng dữ liệu — đã vá, giữ canh


@pytest.mark.needs_corpus
def test_moi_file_du_doan_tren_dia_deu_duoc_nap() -> None:
    """Nạp thiếu là cách hỏng im lặng nhất của cả bench — giữ test này mãi.

    Viết ở C2 (TASK-086) dưới dạng `xfail(strict=True)`: lúc đó 206 dự đoán
    `sovereign_*` nằm ở `prediction/<biến thể>/sovereign/*.json`, sâu hơn một cấp so
    với chỗ `load_predictions()` quét ⇒ nạp 512/718 mà không báo gì. TASK-091 nắn bố
    cục và thêm hai guard vào loader, nên `strict` đã làm đúng việc của nó: xfail
    chuyển thành pass là lỗi, và nó tự báo ngày sửa xong.

    Không xoá test cùng với dấu xfail — lỗ hổng đã vá, nhưng cái canh thì vẫn cần.
    """
    tren_dia = len(list((GOC / "prediction").rglob("*.json")))
    nap_duoc = len(load_predictions(GOC / "prediction"))
    assert nap_duoc == tren_dia, f"nạp {nap_duoc}/{tren_dia}"


# ------------------------------------------------------------------ báo cáo


@pytest.mark.needs_corpus
def test_bao_cao_khop_voi_lan_cham_hien_tai(bang_that: ScoreTable) -> None:
    """`results/c2_metric_status.json` phải là ảnh chụp của lần chấm hiện tại.

    Báo cáo cũ hơn code là báo cáo sai — và không ai phát hiện ra bằng mắt. Chạy lại
    `py -3 scripts/c2_report.py` để cập nhật.
    """
    f = GOC / "results" / "c2_metric_status.json"
    if not f.exists():
        pytest.skip("chưa sinh báo cáo — chạy scripts/c2_report.py")

    ten = sorted(registry.list_metrics())
    moi = D.phan_nhom_metric([D.do_phan_tan(bang_that, m) for m in ten], moi_metric=ten)
    cu = json.loads(f.read_text(encoding="utf-8"))
    for nhom in ("bang_chinh", "phu_luc"):
        assert [d["metric"] for d in cu[nhom]] == [d["metric"] for d in moi[nhom]], (
            f"nhóm `{nhom}` trong báo cáo lệch so với lần chấm hiện tại"
        )
