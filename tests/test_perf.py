"""Test thước đo perf — B6 (TASK-084).

Bốn AC được chốt ở đây, cộng hai cái bẫy mà B6 tồn tại để chặn: chia cho một trang
giả, và in RSS mà giấu phạm vi đếm.
"""

from __future__ import annotations

import dataclasses
import time
from pathlib import Path

import pytest

from ocr_bench.adapters.base import Adapter
from ocr_bench.metrics.perf import (
    HON_HOP,
    PerfAggregate,
    bang_chi_tiet,
    bang_tong_hop,
    perf_aggregate,
    perf_aggregates,
    perf_rows,
)
from ocr_bench.rss import DoRss, co_psutil
from ocr_bench.types import Capability, OcrResult


def kq(doc_id: str = "d1", engine: str = "e", **kw) -> OcrResult:
    """`OcrResult` tối thiểu, chỉ khai những trường test đang nói tới."""
    base = dict(
        engine=engine,
        engine_version="1",
        doc_id=doc_id,
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md="x",
        page_sizes=((612.0, 792.0),) * 4,
        seconds=8.0,
    )
    base.update(kw)
    return OcrResult(**base)


# ---------------------------------------------------------------------------
# AC-01 — sec/trang và peak RSS ở mức engine × tài liệu
# ---------------------------------------------------------------------------


def test_ac01_moi_engine_moi_tai_lieu_mot_dong():
    rows = perf_rows(
        [
            kq("d1", "a", peak_rss_mb=100.0, rss_scope="process"),
            kq("d2", "a", peak_rss_mb=120.0, rss_scope="process"),
            kq("d1", "b", peak_rss_mb=90.0, rss_scope="process"),
        ]
    )
    assert [(r.engine, r.doc_id) for r in rows] == [
        ("a", "d1"),
        ("a", "d2"),
        ("b", "d1"),
    ]
    for r in rows:
        assert r.seconds_per_page == pytest.approx(2.0)
        assert r.peak_rss_mb is not None


def test_ac01_khong_co_page_sizes_thi_khong_chia_cho_mot_trang_gia():
    """`seconds / 1` làm engine trông nhanh gấp N lần trên tài liệu N trang."""
    (row,) = perf_rows([kq(page_sizes=())])
    assert row.n_trang is None
    assert row.seconds_per_page is None
    assert row.seconds == 8.0  # tổng thời gian vẫn giữ, chỉ không chia được


# ---------------------------------------------------------------------------
# AC-02 — FailRate đi cùng mọi trung bình
# ---------------------------------------------------------------------------


def test_ac02_fail_rate_la_truong_cua_chinh_dataclass():
    """Không có đường nào lấy trung bình mà không cầm sẵn tỉ lệ hỏng."""
    ten = {f.name for f in dataclasses.fields(PerfAggregate)}
    assert "fail_rate" in ten
    assert {"sec_moi_trang_tb", "sec_moi_trang_trung_vi"} <= ten


def test_ac02_cell_va_bang_luon_in_fail():
    agg = perf_aggregate(
        perf_rows(
            [
                kq("d1", peak_rss_mb=100.0, rss_scope="process"),
                kq("d2", failed=True, error="bùm"),
            ]
        )
    )
    assert agg.fail_rate == 0.5
    assert "fail" in agg.cell()
    assert "FailRate" in bang_tong_hop([agg])


def test_ac02_mau_so_la_toan_bo_tai_lieu_khong_phai_so_do_duoc():
    """Lấy mẫu số là số tài liệu đo được thì engine hỏng nhiều lại có fail_rate thấp."""
    agg = perf_aggregate(
        perf_rows(
            [
                kq("d1"),
                kq("d2", failed=True, error="bùm", seconds=None, page_sizes=()),
                kq("d3", failed=True, error="bùm", seconds=None, page_sizes=()),
            ]
        )
    )
    assert agg.n_do_duoc == 1  # chỉ d1 có sec/trang
    assert agg.fail_rate == pytest.approx(2 / 3)  # mẫu số vẫn là 3


# ---------------------------------------------------------------------------
# AC-03 — thời gian nạp model tính riêng
# ---------------------------------------------------------------------------


def test_ac03_thoi_gian_nap_bi_tru_khoi_sec_moi_trang():
    (co,) = perf_rows([kq(seconds=8.0, model_load_seconds=4.0)])
    (khong,) = perf_rows([kq(seconds=8.0)])
    assert co.seconds_per_page == pytest.approx(1.0)  # (8-4)/4
    assert khong.seconds_per_page == pytest.approx(2.0)  # 8/4
    assert co.da_tru_nap is True
    assert khong.da_tru_nap is False


def test_ac03_bang_khai_ro_da_tru_hay_chua():
    """Hai engine, một đã trừ một chưa, đặt cạnh nhau mà không nói ra là so nhầm."""
    bang = bang_chi_tiet(
        perf_rows([kq("d1", "a", model_load_seconds=4.0), kq("d1", "b")])
    )
    assert "trừ nạp" in bang


def test_ac03_khong_khai_thi_hien_gach_khong_hien_khong():
    """`—` = không đo; `0` = "nạp model mất 0 giây", một lời nói dối."""
    agg = perf_aggregate(perf_rows([kq()]))
    assert agg.model_load_seconds is None

    dong = bang_tong_hop([agg]).splitlines()
    cot = [c.strip() for c in dong[0].split("|")].index("nạp model (s)")
    assert [c.strip() for c in dong[2].split("|")][cot] == "—"


def test_ac03_nap_lau_hon_tong_la_loi_ngay_o_types():
    with pytest.raises(ValueError, match="lớn hơn"):
        kq(seconds=3.0, model_load_seconds=9.0)


# ---------------------------------------------------------------------------
# AC-04 — số của adapter thắng số của lớp bọc
# ---------------------------------------------------------------------------


class TuDo(Adapter):
    """Adapter tự đo cả thời gian lẫn bộ nhớ bên trong `run()`."""

    name = "tu_do"
    capabilities = frozenset({Capability.TEXT_MD})

    def run(self, doc_path: Path) -> OcrResult:
        time.sleep(0.02)  # để lớp bọc đo ra một số KHÁC nếu nó ghi đè
        return OcrResult(
            engine=self.name,
            engine_version="1",
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            text_md="x",
            seconds=0.5,
            model_load_seconds=0.1,
            peak_rss_mb=42.0,
            rss_scope="process",
        )


class KhongDo(Adapter):
    name = "khong_do"
    capabilities = frozenset({Capability.TEXT_MD})

    def run(self, doc_path: Path) -> OcrResult:
        return OcrResult(
            engine=self.name,
            engine_version="1",
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            text_md="x",
        )


def test_ac04_execute_giu_nguyen_so_cua_adapter(tmp_path):
    doc = tmp_path / "d1.pdf"
    doc.write_bytes(b"%PDF-1.4\n")
    r = TuDo().execute(doc)
    assert r.seconds == 0.5
    assert r.model_load_seconds == 0.1
    assert r.peak_rss_mb == 42.0
    assert r.rss_scope == "process"


def test_execute_dien_vao_cho_adapter_de_trong(tmp_path):
    doc = tmp_path / "d1.pdf"
    doc.write_bytes(b"%PDF-1.4\n")
    r = KhongDo().execute(doc)
    assert r.seconds is not None and r.seconds >= 0
    if co_psutil():
        assert r.peak_rss_mb is not None and r.rss_scope is not None
    else:
        assert (r.peak_rss_mb, r.rss_scope) == (None, None)


def test_execute_bat_exception_van_giu_so_do_duoc(tmp_path):
    class Sap(Adapter):
        name = "sap"
        capabilities = frozenset({Capability.TEXT_MD})

        def run(self, doc_path: Path) -> OcrResult:
            raise RuntimeError("bùm")

    doc = tmp_path / "d1.pdf"
    doc.write_bytes(b"%PDF-1.4\n")
    r = Sap().execute(doc)
    assert r.failed and "bùm" in (r.error or "")
    # Vứt số của lượt chạy hỏng đi thì FailRate cao lại thành cách làm bảng perf đẹp.
    assert r.seconds is not None


# ---------------------------------------------------------------------------
# RSS: phạm vi phải đi cùng con số
# ---------------------------------------------------------------------------


def test_rss_khong_khai_pham_vi_la_loi():
    with pytest.raises(ValueError, match="rss_scope"):
        kq(peak_rss_mb=10.0)


def test_rss_pham_vi_la_gia_tri_lung_tung_la_loi():
    with pytest.raises(ValueError, match="rss_scope"):
        kq(peak_rss_mb=10.0, rss_scope="toàn máy")


def test_pham_vi_lech_nhau_thi_bao_hon_hop_chu_khong_chon_dai_dien():
    agg = perf_aggregate(
        perf_rows(
            [
                kq("d1", peak_rss_mb=100.0, rss_scope="process"),
                kq("d2", peak_rss_mb=200.0, rss_scope="process+children"),
            ]
        )
    )
    assert agg.rss_scope == HON_HOP
    assert HON_HOP in bang_tong_hop([agg])


def test_bang_canh_bao_khi_chi_dem_tien_trinh_chinh():
    """opendataloader nuôi một JVM con — cột RSS trần trụi sẽ khen nó nhẹ nhất bảng."""
    agg = perf_aggregate(perf_rows([kq(peak_rss_mb=100.0, rss_scope="process")]))
    assert "tiến trình con" in bang_tong_hop([agg])


def test_rss_dinh_lay_max_con_trung_vi_lay_median():
    agg = perf_aggregate(
        perf_rows(
            [
                kq("d1", peak_rss_mb=100.0, rss_scope="process"),
                kq("d2", peak_rss_mb=300.0, rss_scope="process"),
                kq("d3", peak_rss_mb=110.0, rss_scope="process"),
            ]
        )
    )
    assert agg.rss_dinh_mb == 300.0
    assert agg.rss_trung_vi_mb == 110.0


def test_do_rss_khong_bao_gio_ra_so_am():
    """Mốc là mẫu đầu tiên nên hiệu không có đường nào âm — không phải kẹp về 0."""
    with DoRss(chu_ky=0.005) as do:
        rac = [b"x" * 1024 for _ in range(2000)]
        time.sleep(0.02)
        del rac
    mb, pham_vi = do.ket_qua
    if co_psutil():
        assert mb is not None and mb >= 0.0
        assert pham_vi in {"process", "process+children"}
    else:
        assert (mb, pham_vi) == (None, None)


def test_do_rss_khong_co_psutil_thi_tra_none(monkeypatch):
    """`pytest` phải xanh trên máy trắng — `psutil` là extra `perf`."""
    monkeypatch.setattr("ocr_bench.rss._psutil", lambda: None)
    with DoRss() as do:
        pass
    assert do.ket_qua == (None, None)


# -- nhánh tiến trình con: đúng cái `rss_scope` sinh ra để nói thật ----------

MB = 1024 * 1024


class _Nho:
    def __init__(self, mb: float) -> None:
        self.rss = int(mb * MB)


class _TienTrinh:
    """Tiến trình giả. `con` là list `_TienTrinh` hoặc exception để ném."""

    def __init__(self, mb, con=None) -> None:
        self._mb = mb
        self._con = con if con is not None else []

    def memory_info(self):
        if isinstance(self._mb, Exception):
            raise self._mb
        return _Nho(self._mb)

    def children(self, recursive: bool = False):
        if isinstance(self._con, Exception):
            raise self._con
        return self._con


def _gia(proc):
    """Module `psutil` giả trả về `proc` cho `Process()`."""
    return type("psutil", (), {"Process": staticmethod(lambda: proc)})


def test_rss_cong_ca_tien_trinh_con_va_khai_process_children(monkeypatch):
    """JVM của opendataloader phải được đếm, không chỉ RSS của Python."""
    proc = _TienTrinh(100.0, [_TienTrinh(50.0), _TienTrinh(25.0)])
    monkeypatch.setattr("ocr_bench.rss._psutil", lambda: _gia(proc))
    do = DoRss(chu_ky=0.005)
    with do:
        time.sleep(0.01)
    mb, pham_vi = do.ket_qua
    assert pham_vi == "process+children"
    assert mb == pytest.approx(0.0)  # mốc = đỉnh vì số giả không đổi
    assert do._doc() == pytest.approx(175.0)  # 100 + 50 + 25


def test_doc_con_bi_tu_choi_thi_HA_pham_vi_chu_khong_im_lang(monkeypatch):
    """Khai `process+children` trong khi đếm hụt là đúng thứ cột phạm vi phải chặn."""
    proc = _TienTrinh(100.0, PermissionError("không đủ quyền"))
    monkeypatch.setattr("ocr_bench.rss._psutil", lambda: _gia(proc))
    do = DoRss(chu_ky=0.005)
    with do:
        time.sleep(0.01)
    _, pham_vi = do.ket_qua
    assert pham_vi == "process"


def test_mot_tien_trinh_con_chet_giua_chung_cung_ha_pham_vi(monkeypatch):
    proc = _TienTrinh(100.0, [_TienTrinh(ProcessLookupError("đã thoát"))])
    monkeypatch.setattr("ocr_bench.rss._psutil", lambda: _gia(proc))
    do = DoRss(chu_ky=0.005)
    with do:
        time.sleep(0.01)
    mb, pham_vi = do.ket_qua
    assert pham_vi == "process"
    assert mb is not None  # vẫn có số, chỉ khai hẹp hơn


def test_tien_trinh_chinh_bien_mat_thi_khong_bia_ra_so(monkeypatch):
    proc = _TienTrinh(ProcessLookupError("tiến trình chính đã thoát"))
    monkeypatch.setattr("ocr_bench.rss._psutil", lambda: _gia(proc))
    do = DoRss(chu_ky=0.005)
    with do:
        time.sleep(0.01)
    assert do.ket_qua == (None, None)


# ---------------------------------------------------------------------------
# Tổng hợp
# ---------------------------------------------------------------------------


def test_perf_aggregates_mot_dong_moi_engine():
    aggs = perf_aggregates(perf_rows([kq("d1", "b"), kq("d2", "b"), kq("d1", "a")]))
    assert [a.engine for a in aggs] == ["a", "b"]
    assert [a.n_total for a in aggs] == [1, 2]


def test_perf_aggregate_lan_engine_la_loi():
    with pytest.raises(ValueError, match="lẫn engine"):
        perf_aggregate(perf_rows([kq("d1", "a"), kq("d1", "b")]))


def test_perf_aggregate_rong_la_loi():
    with pytest.raises(ValueError, match="ít nhất một dòng"):
        perf_aggregate([])


def test_khong_do_duoc_gi_thi_o_hien_gach_khong_hien_khong():
    agg = perf_aggregate(perf_rows([kq(seconds=None, page_sizes=())]))
    assert agg.sec_moi_trang_tb is None
    assert agg.rss_dinh_mb is None
    assert "—" in agg.cell()
