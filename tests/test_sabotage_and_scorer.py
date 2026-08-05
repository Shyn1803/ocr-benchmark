"""Test `sabotage` + `scorer` — A1b.

Câu hỏi trung tâm không phải "code có chạy không" mà là: **bộ khung này có phát hiện
được một metric hỏng không?** Vì thế phần lớn test ở đây cố tình dựng metric sai rồi
kiểm rằng cổng bắt được.
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pytest

from ocr_bench import registry
from ocr_bench.adapters.base import Adapter
from ocr_bench.adapters.noop import NoopAdapter
from ocr_bench.adapters.sabotage import SabotageAdapter
from ocr_bench.metrics.base import Metric
from ocr_bench.scorer import ScoreTable, run_bench, run_engines, score_results
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    BlockType,
    Box,
    Capability,
    MetricResult,
    NAReason,
    OcrBlock,
    OcrImage,
    OcrResult,
    OcrTable,
)

DOC = Path("pdfs/mau.pdf")
VAN_BAN = "\n".join(f"dòng số {i} có nội dung riêng" for i in range(10))
BANG = "<table>" + "".join(f"<tr><td>ô {i}</td></tr>" for i in range(6)) + "</table>"


class TotAdapter(Adapter):
    """Engine "tốt": trả đúng ground truth. Nguồn để `sabotage` làm hỏng."""

    name: ClassVar[str] = "tot"
    capabilities: ClassVar[frozenset[Capability]] = frozenset(
        {
            Capability.TEXT_MD,
            Capability.BLOCK_BBOX,
            Capability.IMAGE_BBOX,
            Capability.TABLE_HTML,
            Capability.SCAN_LABEL,
        }
    )

    def version(self) -> str:
        return "1"

    def run(self, doc_path: Path) -> OcrResult:
        return OcrResult(
            engine=self.name,
            engine_version=self.version(),
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            text_md=VAN_BAN,
            blocks=tuple(
                OcrBlock(
                    block_type=BlockType.TEXT,
                    box=Box(page=0, x0=0.1 * i, y0=0.1 * i, x1=0.1 * i + 0.2, y1=0.1 * i + 0.2),
                    text=f"khối {i}",
                )
                for i in range(6)
            ),
            images=tuple(
                OcrImage(box=Box(page=0, x0=0.1, y0=0.1 * i, x1=0.3, y1=0.1 * i + 0.05))
                for i in range(4)
            ),
            tables=(OcrTable(html=BANG, n_rows=6, n_cols=1),),
            scan_label=None,
        )


class GiongHetGT(Metric):
    """Metric thật thà: tỉ lệ ký tự khớp thô. Đủ để `sabotage` phải thua."""

    name = "giong_gt"
    requires = frozenset({Capability.TEXT_MD})
    gt_kinds = (AnnotationGT,)

    def _compute(self, gt, result):
        want = gt.text or ""
        got = result.text_md or ""
        if not want:
            return 1.0, {}
        chung = sum(1 for a, b in zip(want, got) if a == b)
        return chung / len(want), {"len_got": len(got)}


def gt() -> AnnotationGT:
    return AnnotationGT(doc_id="mau", text=VAN_BAN)


# ---------------------------------------------------------------- sabotage


def test_sabotage_luon_te_hon_nguon():
    """Lý do tồn tại của adapter này. Hỏng chỗ nào cũng được, trừ chỗ này."""
    tot = TotAdapter().execute(DOC)
    xau = SabotageAdapter(TotAdapter()).execute(DOC)
    m = GiongHetGT()
    assert m.score(gt(), xau).value < m.score(gt(), tot).value


def test_sabotage_tat_dinh():
    """Cùng seed, cùng tài liệu ⇒ cùng kết quả.

    Xáo ngẫu nhiên thật sẽ làm cổng C2 lúc đỏ lúc xanh, và cổng như vậy thì người ta
    tắt đi chứ không đi sửa.
    """
    a = SabotageAdapter(TotAdapter()).execute(DOC)
    b = SabotageAdapter(TotAdapter()).execute(DOC)
    assert a.text_md == b.text_md
    assert [x.box for x in a.images] == [x.box for x in b.images]
    assert [t.html for t in a.tables] == [t.html for t in b.tables]


def test_doi_seed_thi_doi_ket_qua():
    a = SabotageAdapter(TotAdapter(), seed=1).execute(DOC)
    b = SabotageAdapter(TotAdapter(), seed=2).execute(DOC)
    assert a.text_md != b.text_md


def test_sabotage_giu_nguyen_capabilities_cua_nguon():
    """Khai ít hơn nguồn thì metric ra N/A và `sabotage` BIẾN MẤT khỏi bảng thay vì
    đứng bét — đúng cái nó sinh ra để phát hiện."""
    xau = SabotageAdapter(TotAdapter()).execute(DOC)
    assert xau.capabilities == TotAdapter.capabilities


def test_sabotage_cat_con_mot_nua():
    xau = SabotageAdapter(TotAdapter()).execute(DOC)
    assert len(xau.blocks) == 3
    assert len(xau.images) == 2
    assert len(xau.text_md.split("\n")) == 5


def test_sabotage_xao_thu_tu_dong():
    xau = SabotageAdapter(TotAdapter()).execute(DOC)
    giu = xau.text_md.split("\n")
    goc = [ln for ln in VAN_BAN.split("\n") if ln in giu]
    assert giu != goc, "cắt mà không xáo thì metric thứ tự đọc không thấy gì"


def test_sabotage_van_ban_mot_dong_thi_xao_theo_tu():
    """Không có nhánh này, `sabotage` trên tài liệu ngắn ra điểm HỆT nguồn và C2 sẽ
    báo "metric không phân biệt được" trong khi lỗi nằm ở adapter."""

    class MotDong(Adapter):
        name: ClassVar[str] = "mot_dong"
        capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})

        def run(self, doc_path: Path) -> OcrResult:
            return OcrResult(
                engine=self.name, engine_version="1", doc_id=doc_path.stem,
                capabilities=self.capabilities,
                text_md="một hai ba bốn năm sáu bảy tám",
            )

    xau = SabotageAdapter(MotDong()).execute(DOC)
    assert "\n" not in xau.text_md
    assert len(xau.text_md.split()) == 4


def test_sabotage_lam_lech_bbox_nhung_khong_day_ra_ngoai():
    """IoU = 0 với mọi tài liệu thì mọi metric bbox cho cùng một điểm sàn, và ta mất
    khả năng thấy metric nào nhạy hơn."""
    tot = TotAdapter().execute(DOC)
    xau = SabotageAdapter(TotAdapter()).execute(DOC)
    goc = {b.text: b.box for b in tot.blocks}
    lech = [b.box.iou(goc[b.text]) for b in xau.blocks]
    assert all(0.0 < v < 1.0 for v in lech), f"IoU sau xô lệch: {lech}"


def test_khoi_khong_co_bbox_thi_de_yen_chu_khong_no():
    """Engine chỉ trả text (OpenDataLoader ở chế độ tối giản) vẫn phải sabotage được."""

    class KhongBbox(Adapter):
        name: ClassVar[str] = "khong_bbox"
        capabilities: ClassVar[frozenset[Capability]] = frozenset(
            {Capability.TEXT_MD, Capability.BLOCK_BBOX}
        )

        def run(self, doc_path: Path) -> OcrResult:
            return OcrResult(
                engine=self.name, engine_version="1", doc_id=doc_path.stem,
                capabilities=self.capabilities, text_md=VAN_BAN,
                blocks=(
                    OcrBlock(block_type=BlockType.TEXT, text="a"),
                    OcrBlock(block_type=BlockType.TEXT, text="b"),
                ),
            )

    xau = SabotageAdapter(KhongBbox()).execute(DOC)
    assert xau.failed is False
    assert [b.box for b in xau.blocks] == [None]


def test_sabotage_cat_bot_hang_trong_bang():
    xau = SabotageAdapter(TotAdapter()).execute(DOC)
    assert xau.tables[0].html.count("<tr>") == 3
    assert xau.tables[0].n_rows == 3


def test_sabotage_bang_mot_hang_thi_de_nguyen():
    """`<table>` một hàng cắt nữa thì thành rỗng — mất luôn khả năng phân biệt
    "hỏng nặng" với "không trả gì"."""

    class MotHang(Adapter):
        name: ClassVar[str] = "mot_hang"
        capabilities: ClassVar[frozenset[Capability]] = frozenset(
            {Capability.TEXT_MD, Capability.TABLE_HTML}
        )

        def run(self, doc_path: Path) -> OcrResult:
            return OcrResult(
                engine=self.name, engine_version="1", doc_id=doc_path.stem,
                capabilities=self.capabilities, text_md="x",
                tables=(OcrTable(html="<table><tr><td>a</td></tr></table>"),),
            )

    xau = SabotageAdapter(MotHang()).execute(DOC)
    assert xau.tables[0].html == "<table><tr><td>a</td></tr></table>"


def test_sabotage_dao_nhan_scan():
    class CoNhan(Adapter):
        name: ClassVar[str] = "co_nhan"
        capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.SCAN_LABEL})

        def run(self, doc_path: Path) -> OcrResult:
            from ocr_bench.types import ScanLabel

            return OcrResult(
                engine=self.name, engine_version="1", doc_id=doc_path.stem,
                capabilities=self.capabilities,
                scan_label=ScanLabel(is_scanned=True, api="classify_pdf"),
            )

    xau = SabotageAdapter(CoNhan()).execute(DOC)
    assert xau.scan_label.is_scanned is False
    assert xau.scan_label.api == "sabotage(classify_pdf)"


def test_nguon_hong_thi_sabotage_cung_hong():
    """Trả kết quả sạch ở đây sẽ làm `sabotage` trông TỐT HƠN nguồn đúng vào lúc
    nguồn tệ nhất — và FailRate của nó thành số dối."""

    class No(Adapter):
        name: ClassVar[str] = "no"
        capabilities: ClassVar[frozenset[Capability]] = frozenset()

        def run(self, doc_path: Path) -> OcrResult:
            raise RuntimeError("hết VRAM")

    xau = SabotageAdapter(No()).execute(DOC)
    assert xau.failed is True
    assert xau.engine == "sabotage"
    assert "hết VRAM" in xau.error
    assert "traceback" in xau.config_fingerprint, "mất traceback là mất manh mối gỡ lỗi"
    assert xau.config_fingerprint["source"] == "no"


def test_sabotage_mac_dinh_boc_noop_chay_duoc_tren_may_trang():
    xau = SabotageAdapter().execute(DOC)
    assert xau.failed is False
    assert xau.text_md == ""
    assert xau.capabilities == NoopAdapter.capabilities


def test_sabotage_da_dang_ky_san():
    assert registry.get_adapter("sabotage") is SabotageAdapter


def test_fingerprint_ghi_ro_nguon_va_seed():
    fp = SabotageAdapter(TotAdapter(), seed=7).config_fingerprint()
    assert fp == {"source": "tot", "seed": 7, "keep_ratio": 0.5}
    assert SabotageAdapter(TotAdapter()).version() == "sabotage/1+tot"


# ------------------------------------------------------------------ scorer


def test_end_to_end_sabotage_phai_dung_bet():
    """Đường chạy đầy đủ của A1b: adapter → OcrResult → metric → bảng xếp hạng."""
    bang = run_bench(
        [TotAdapter(), NoopAdapter(), SabotageAdapter(TotAdapter())],
        [DOC],
        [GiongHetGT()],
        {"mau": gt()},
    )
    thu_tu = [a.engine for a in bang.ranking("giong_gt")]
    assert thu_tu[0] == "tot"
    assert thu_tu[-1] in {"noop", "sabotage"}
    assert bang.cell("giong_gt", "tot").penalized_mean == 1.0
    assert bang.cell("giong_gt", "noop").penalized_mean == 0.0


def test_tach_chay_khoi_cham_la_cai_khe_cua_A2():
    """Chạy một lần, chấm nhiều lần với bộ metric khác nhau, không đụng engine."""
    ket_qua = run_engines([TotAdapter()], [DOC])
    a = score_results(ket_qua, [GiongHetGT()], {"mau": gt()})
    b = score_results(ket_qua, [GiongHetGT()], {"mau": gt()})
    assert a.rows == b.rows


def test_thieu_ground_truth_ra_NA_chu_khong_ra_0():
    """Thiếu nhãn là lỗi bộ mẫu, không phải lỗi engine — không được phạt engine."""
    bang = run_bench([TotAdapter()], [DOC], [GiongHetGT()], {})
    (r,) = bang.rows
    assert r.value is None
    assert r.na_reason is NAReason.NO_GROUND_TRUTH
    o = bang.cell("giong_gt", "tot")
    assert o.applicable is False
    assert o.cell() == "N/A"


def test_thieu_nang_luc_ra_NA_va_van_co_mat_trong_xep_hang():
    """Bỏ dòng N/A khỏi bảng là cách nhanh nhất làm engine yếu trông mạnh."""

    class CanAnh(Metric):
        name = "can_anh"
        requires = frozenset({Capability.IMAGE_BBOX})
        gt_kinds = (AnnotationGT,)

        def _compute(self, gt_, result):
            return 1.0, {}

    bang = run_bench(
        [TotAdapter(), NoopAdapter()], [DOC], [CanAnh()], {"mau": gt()}
    )
    o = bang.cell("can_anh", "noop")
    assert o.applicable is False and o.cell() == "N/A"
    assert o.n_na == 1 and o.n_failed == 0
    assert "noop" in [a.engine for a in bang.ranking("can_anh")]
    assert bang.ranking("can_anh")[-1].engine == "noop"


def test_engine_hong_van_vao_mau_so_phat():
    """Ngược với `opendataloader-bench`: ở đó tài liệu engine làm hỏng bị loại khỏi
    trung bình, tức thưởng cho engine hỏng nhiều hơn."""

    class HongMotNua(Adapter):
        name: ClassVar[str] = "hong_mot_nua"
        capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})

        def run(self, doc_path: Path) -> OcrResult:
            if doc_path.stem == "xau":
                raise RuntimeError("hỏng")
            return OcrResult(
                engine=self.name, engine_version="1", doc_id=doc_path.stem,
                capabilities=self.capabilities, text_md=VAN_BAN,
            )

    bang = run_bench(
        [HongMotNua()],
        [Path("pdfs/mau.pdf"), Path("pdfs/xau.pdf")],
        [GiongHetGT()],
        {"mau": gt(), "xau": AnnotationGT(doc_id="xau", text=VAN_BAN)},
    )
    o = bang.cell("giong_gt", "hong_mot_nua")
    assert o.mean == 1.0, "trung bình trên tài liệu chấm được"
    assert o.penalized_mean == 0.5, "có phạt: tài liệu hỏng tính 0"
    assert o.fail_rate == 0.5
    assert o.cell() == "0.500 (fail 50%)"


def test_bang_markdown_in_ca_o_NA():
    bang = run_bench(
        [TotAdapter(), NoopAdapter()], [DOC], [GiongHetGT()], {"mau": gt()}
    )
    md = bang.to_markdown()
    assert "| metric | noop | tot |" in md
    assert "0.000 (fail 0%)" in md and "1.000 (fail 0%)" in md
    assert bang.engines() == ["noop", "tot"]
    assert bang.metrics() == ["giong_gt"]
    assert bang.docs() == ["mau"]


def test_worst_la_dau_vao_cua_D2_va_bo_qua_NA():
    """"Không đo được" không phải "đo được và tệ" — trộn vào thì danh sách 20 ca đọc
    tay sẽ toàn ô trống."""
    bang = ScoreTable(
        (
            MetricResult(metric="m", engine="a", doc_id="d1", value=0.9),
            MetricResult(metric="m", engine="b", doc_id="d2", value=0.1),
            MetricResult(
                metric="m", engine="c", doc_id="d3", value=None,
                na_reason=NAReason.MISSING_CAPABILITY,
            ),
        )
    )
    assert [r.engine for r in bang.worst(10)] == ["b", "a"]
    assert [r.engine for r in bang.worst(1)] == ["b"]


def test_aggregates_phu_kin_moi_o_ke_ca_o_trong():
    bang = run_bench(
        [TotAdapter(), NoopAdapter()], [DOC], [GiongHetGT()], {"mau": gt()}
    )
    assert set(bang.aggregates()) == {("giong_gt", "tot"), ("giong_gt", "noop")}


def test_sai_gt_kind_ra_NA_chu_khong_no():
    bang = run_bench(
        [TotAdapter()], [DOC], [GiongHetGT()], {"mau": AssertionGT(doc_id="mau")}
    )
    (r,) = bang.rows
    assert r.na_reason is NAReason.WRONG_GT_KIND


def test_bang_rong_khong_no():
    bang = ScoreTable(())
    assert bang.to_markdown() == "| metric |  |\n|---|"
    assert bang.ranking("khong_co") == []
    assert bang.worst() == []


def test_metric_tra_diem_ngoai_khoang_thi_no_ngay():
    """Metric hỏng phải nổ, không được lặng lẽ đẩy engine lên đầu bảng."""

    class Lech(Metric):
        name = "lech"
        requires = frozenset()
        gt_kinds = (AnnotationGT,)

        def _compute(self, gt_, result):
            return 1.5, {}

    with pytest.raises(ValueError, match=r"phải nằm trong \[0,1\]"):
        run_bench([NoopAdapter()], [DOC], [Lech()], {"mau": gt()})
