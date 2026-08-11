"""Test registry + adapter `noop` + đường chạy end-to-end tối thiểu."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pytest

from ocr_bench import registry
from ocr_bench.adapters.base import Adapter
from ocr_bench.adapters.marker import MarkerAdapter
from ocr_bench.adapters.noop import NoopAdapter
from ocr_bench.metrics.base import Metric
from ocr_bench.profiles import EngineProfile, ProfileConfigError
from ocr_bench.types import AnnotationGT, Capability, OcrResult


def test_noop_da_dang_ky_san():
    assert "noop" in registry.list_adapters()
    assert registry.get_adapter("noop") is NoopAdapter


def test_noop_tra_chuoi_rong_va_khai_text_md():
    """`noop` phải khai TEXT_MD. Khai frozenset() thì mọi metric trả N/A và nó biến
    mất khỏi bảng thay vì đứng bét — đúng cái nó sinh ra để phát hiện."""
    r = NoopAdapter().execute(Path("pdfs/khong-ton-tai.pdf"))
    assert r.failed is False
    assert r.text_md == ""
    assert r.capabilities == frozenset({Capability.TEXT_MD})
    assert r.doc_id == "khong-ton-tai"
    assert r.seconds is not None and r.seconds >= 0


def test_execute_bien_exception_thanh_failed_chu_khong_nem():
    """Engine hỏng phải thành một dòng kết quả. Ném ra ngoài thì cả lượt chạy 3
    tiếng của Marker đổ theo, và FailRate mất luôn ca đó."""

    class Exploding(Adapter):
        name: ClassVar[str] = "exploding"
        capabilities: ClassVar[frozenset[Capability]] = frozenset()

        def run(self, doc_path: Path) -> OcrResult:
            raise RuntimeError("hết RAM")

    r = Exploding().execute(Path("x.pdf"))
    assert r.failed is True
    assert r.engine_family == "exploding"
    assert r.profile == "legacy"
    assert "hết RAM" in (r.error or "")
    assert r.seconds is not None


def test_adapter_tu_do_thoi_gian_thi_execute_khong_ghi_de():
    """B6 đo sec/trang. Adapter nào tự đo chính xác hơn (loại trừ thời gian tải
    model) thì `execute()` phải giữ nguyên số của nó."""

    class TuDo(Adapter):
        name: ClassVar[str] = "tu_do"
        capabilities: ClassVar[frozenset[Capability]] = frozenset()

        def run(self, doc_path: Path) -> OcrResult:
            return OcrResult(
                engine=self.name, engine_version="1", doc_id=doc_path.stem,
                capabilities=self.capabilities, seconds=42.0,
            )

    assert TuDo().execute(Path("x.pdf")).seconds == 42.0


def test_dang_ky_thieu_capabilities_thi_no_ngay_luc_import():
    class Quen(Adapter):
        name: ClassVar[str] = "quen"

        def run(self, doc_path: Path) -> OcrResult:  # pragma: no cover
            raise NotImplementedError

    with pytest.raises(TypeError, match="capabilities phải là frozenset"):
        registry.register_adapter(Quen)


def test_dang_ky_capabilities_dung_set_thuong_cung_no():
    class Sai(Adapter):
        name: ClassVar[str] = "sai"
        capabilities = {Capability.TEXT_MD}  # type: ignore[assignment]

        def run(self, doc_path: Path) -> OcrResult:  # pragma: no cover
            raise NotImplementedError

    with pytest.raises(TypeError, match="khai TĨNH"):
        registry.register_adapter(Sai)


def test_dang_ky_thieu_name_thi_no():
    class KhongTen(Adapter):
        capabilities: ClassVar[frozenset[Capability]] = frozenset()

        def run(self, doc_path: Path) -> OcrResult:  # pragma: no cover
            raise NotImplementedError

    with pytest.raises(TypeError, match="thiếu thuộc tính lớp `name`"):
        registry.register_adapter(KhongTen)

    class MetricKhongTen(Metric):
        requires = frozenset()

        def _compute(self, gt, result):  # pragma: no cover
            return 1.0, {}

    with pytest.raises(TypeError, match="thiếu thuộc tính lớp `name`"):
        registry.register_metric(MetricKhongTen)


def test_dang_ky_capability_la_gia_tri_la_thi_no():
    class La(Adapter):
        name: ClassVar[str] = "la"
        capabilities: ClassVar[frozenset] = frozenset({"text_md"})  # type: ignore[arg-type]

        def run(self, doc_path: Path) -> OcrResult:  # pragma: no cover
            raise NotImplementedError

    with pytest.raises(TypeError, match="giá trị lạ"):
        registry.register_adapter(La)

    class MetricLa(Metric):
        name = "metric_la"
        requires = frozenset({"image_bbox"})  # type: ignore[arg-type]

        def _compute(self, gt, result):  # pragma: no cover
            return 1.0, {}

    with pytest.raises(TypeError, match="giá trị lạ"):
        registry.register_metric(MetricLa)


def test_dang_ky_metric_trung_ten_thi_no():
    class M1(Metric):
        name = "trung"
        requires = frozenset()

        def _compute(self, gt, result):  # pragma: no cover
            return 1.0, {}

    class M2(Metric):
        name = "trung"
        requires = frozenset()

        def _compute(self, gt, result):  # pragma: no cover
            return 1.0, {}

    registry.register_metric(M1)
    try:
        assert registry.register_metric(M1) is M1
        with pytest.raises(ValueError, match="đã đăng ký"):
            registry.register_metric(M2)
    finally:
        registry._METRICS.clear()


def test_dang_ky_trung_ten_thi_no():
    class Gia(Adapter):
        name: ClassVar[str] = "noop"
        capabilities: ClassVar[frozenset[Capability]] = frozenset()

        def run(self, doc_path: Path) -> OcrResult:  # pragma: no cover
            raise NotImplementedError

    with pytest.raises(ValueError, match="đã đăng ký"):
        registry.register_adapter(Gia)


def test_dang_ky_lai_dung_lop_do_thi_khong_sao():
    assert registry.register_adapter(NoopAdapter) is NoopAdapter


def test_lay_adapter_khong_co_thi_bao_ro():
    with pytest.raises(KeyError, match="hiện có"):
        # Tên phải là tên KHÔNG bao giờ có thật. Trước đây chỗ này dùng "marker" —
        # đến A4 thì marker được đăng ký và test tự hỏng, dù registry không sai gì.
        registry.get_adapter("engine-khong-ton-tai")


def test_applicable_metrics_biet_truoc_khong_can_chay():
    """Biết TRƯỚC metric nào chạm tới engine nào — để in ô N/A thay vì lặng lẽ bỏ
    dòng. Bỏ dòng là cách làm engine yếu trông mạnh."""

    class CanText(Metric):
        name = "can_text"
        requires = frozenset({Capability.TEXT_MD})

        def _compute(self, gt, result):  # pragma: no cover
            return 1.0, {}

    class CanAnh(Metric):
        name = "can_anh"
        requires = frozenset({Capability.IMAGE_BBOX})

        def _compute(self, gt, result):  # pragma: no cover
            return 1.0, {}

    # Chụp lại rồi trả về nguyên trạng, KHÔNG `clear()`. Từ B1 trở đi registry đã có
    # metric thật (`cer`, `wer`) đăng ký lúc import; xoá sạch ở đây sẽ làm hỏng các
    # test chạy sau trong cùng phiên — một test làm hỏng test khác là kiểu hỏng tệ
    # nhất vì thủ phạm không nằm trong test báo đỏ.
    truoc = dict(registry._METRICS)
    registry.register_metric(CanText)
    registry.register_metric(CanAnh)
    try:
        ap = registry.applicable_metrics("noop")
        # Kiểm tập con: khẳng định trên *toàn bộ* registry sẽ tự hỏng mỗi lần thêm
        # một metric mới, dù registry không sai gì — đúng cái bẫy đã gặp với adapter.
        assert {k: ap[k] for k in ("can_text", "can_anh")} == {
            "can_anh": False,
            "can_text": True,
        }
        assert {"can_anh", "can_text"} <= set(registry.list_metrics())
        assert registry.list_metrics() == sorted(registry.list_metrics())
        assert registry.get_metric("can_text") is CanText
        with pytest.raises(KeyError):
            # Tên KHÔNG bao giờ được đăng ký. Trước đây chỗ này ghi "teds" và tự hỏng
            # ngay khi B2 đăng ký thật — cùng cái bẫy "đoán trước tương lai của
            # registry" đã gặp hai lần ở file này.
            registry.get_metric("__khong_bao_gio_ton_tai__")
    finally:
        registry._METRICS.clear()
        registry._METRICS.update(truoc)


def test_dang_ky_metric_sai_kieu_requires():
    class Sai(Metric):
        name = "sai_requires"
        requires = [Capability.TEXT_MD]  # type: ignore[assignment]

        def _compute(self, gt, result):  # pragma: no cover
            return 1.0, {}

    with pytest.raises(TypeError, match="requires phải là frozenset"):
        registry.register_metric(Sai)


def test_end_to_end_toi_thieu_noop_phai_dung_bet():
    """Đường chạy đủ ngắn: adapter → OcrResult → metric → điểm.
    `noop` trả rỗng nên phải ra 0.0, không phải N/A."""

    class DoDaiKhop(Metric):
        name = "do_dai_khop"
        requires = frozenset({Capability.TEXT_MD})
        gt_kinds = (AnnotationGT,)

        def _compute(self, gt, result):
            got, want = result.text_md or "", gt.text or ""
            if not want:
                return 1.0, {}
            return min(len(got), len(want)) / len(want), {"len": len(got)}

    gt = AnnotationGT(doc_id="mau", text="một hai ba bốn năm")
    r = NoopAdapter().execute(Path("pdfs/mau.pdf"))
    score = DoDaiKhop().score(gt, r)
    assert score.value == 0.0
    assert score.is_na is False


def test_clear_chi_dung_trong_test():
    registry.clear()
    assert registry.list_adapters() == []
    registry.register_adapter(NoopAdapter)
    assert registry.list_adapters() == ["noop"]


def test_build_adapter_uses_registered_profile_factory():
    """Skipping ``from_profile`` would lose the frozen publication identity."""

    class ProfiledFake(Adapter):
        name: ClassVar[str] = "profiled_fake"
        capabilities: ClassVar[frozenset[Capability]] = frozenset()

        @classmethod
        def from_profile(cls, profile: EngineProfile) -> "ProfiledFake":
            adapter = cls()
            adapter.name = profile.name
            return adapter

        def run(self, doc_path: Path) -> OcrResult:  # pragma: no cover
            raise NotImplementedError

    before = dict(registry._ADAPTERS)
    registry.register_adapter(ProfiledFake)
    try:
        profile = EngineProfile(
            name="marker_scan",
            family="marker",
            profile="scan",
            adapter="profiled_fake",
            config={"force_ocr": True},
            environment={},
        )

        built = registry.build_adapter(profile)

        assert isinstance(built, ProfiledFake)
        assert built.name == "marker_scan"
    finally:
        registry._ADAPTERS.clear()
        registry._ADAPTERS.update(before)


def test_build_adapter_rejects_legacy_adapter_without_profile_factory():
    """Using a legacy constructor would silently ignore publication configuration."""
    before = dict(registry._ADAPTERS)
    registry.register_adapter(MarkerAdapter)
    profile = EngineProfile(
        name="marker_default",
        family="marker",
        profile="default",
        adapter="marker",
        config={"force_ocr": False},
        environment={},
    )

    try:
        with pytest.raises(ProfileConfigError, match="from_profile"):
            registry.build_adapter(profile)
    finally:
        registry._ADAPTERS.clear()
        registry._ADAPTERS.update(before)


def test_build_adapter_rejects_mismatched_profile_name():
    """A returned legacy name would merge two profile result sets."""

    class WrongName(Adapter):
        name: ClassVar[str] = "wrong_name"
        capabilities: ClassVar[frozenset[Capability]] = frozenset()

        @classmethod
        def from_profile(cls, profile: EngineProfile) -> "WrongName":
            return cls()

        def run(self, doc_path: Path) -> OcrResult:  # pragma: no cover
            raise NotImplementedError

    before = dict(registry._ADAPTERS)
    registry.register_adapter(WrongName)
    try:
        profile = EngineProfile(
            name="marker_scan",
            family="marker",
            profile="scan",
            adapter="wrong_name",
            config={"force_ocr": True},
            environment={},
        )

        with pytest.raises(ProfileConfigError, match="cần 'marker_scan'"):
            registry.build_adapter(profile)
    finally:
        registry._ADAPTERS.clear()
        registry._ADAPTERS.update(before)
