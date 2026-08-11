"""Test bộ nối Sovereign BE — A7 (TASK-078).

Khác ba adapter trước ở một điểm: rủi ro lớn nhất không phải "chuẩn hoá sai" mà là
**chạy trúng nhánh tính tiền**. Nên bộ test này tập trung vào ba cổng an toàn, và cả ba
đều chạy được trên máy **không có BE**:

* env bị cưỡng bức, và nếu cưỡng bức thất bại thì ném chứ không chạy tiếp (AC-01);
* trần chi phí chặn thật, và nó thoát ra khỏi ``execute()`` chứ không bị nuốt thành một
  dòng ``failed=True`` (AC-02);
* ``config_fingerprint`` không rỗng, có đủ hai cờ + ``marker_available``, và **không**
  chứa giá trị khoá nào (AC-03).

Test cần BE thật đánh dấu ``needs_be``.
"""

from __future__ import annotations

import importlib
import json
import os
import sys
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

import ocr_bench.adapters.sovereign as sov
from ocr_bench.adapters.sovereign import (
    ENV_CUONG_BUC,
    SovereignAdapter,
    VuotTran,
    duong_dan_be,
    kiem_config,
)
from ocr_bench.profiles import EngineProfile, ProfileConfigError, load_profile_catalog
from ocr_bench.types import Capability, FailureKind

ROOT = Path(__file__).resolve().parents[1]
CATALOG = load_profile_catalog(ROOT / "configs" / "profiles.json")


def _co_be() -> bool:
    """Có repo BE **và** có bao đóng import của nó.

    Hai điều kiện, không phải một: `.venv` sạch của bench cố ý không cài `pydantic`, nên
    file BE tồn tại mà import vẫn nổ. Đúng lớp "suy thoái âm thầm" mà A7 phải đề phòng —
    chỉ khác là ở đây nó nổ to, còn trong pipeline thật (thiếu `pdfminer`, thiếu cache
    Surya) nó chỉ log WARNING rồi trả kết quả tệ hơn.
    """
    from importlib.util import find_spec  # noqa: PLC0415

    if not (duong_dan_be() / "app" / "services" / "openrouter_document_parser.py").is_file():
        return False
    return all(find_spec(m) is not None for m in ("pydantic", "pydantic_settings", "fitz"))


needs_be = pytest.mark.skipif(
    not _co_be(),
    reason="cần repo BE + bao đóng import (venv .venv-sov hoặc .venv-marker)",
)


@pytest.fixture(autouse=True)
def _co_lap_trang_thai_toan_cuc():
    """Trả `_SECRET_VALUES` và cache `.env` về đúng chỗ cũ sau mỗi test.

    `_SECRET_VALUES` **chỉ lớn thêm** theo thiết kế (một profile không được làm mất khả
    năng bịt của profile sau). Hệ quả trong test: một test seed chuỗi bí mật thì test
    sau vẫn thấy nó, nên mọi khẳng định dạng `== 1` trở thành phụ thuộc thứ tự chạy —
    xanh khi chạy riêng, đỏ khi chạy cả file, và không ai đọc ra vì sao.
    """
    with sov._SECRET_VALUES_LOCK:
        anh_chup = set(sov._SECRET_VALUES)
    cache_cu = sov._ENV_BE_CACHE
    try:
        yield
    finally:
        with sov._SECRET_VALUES_LOCK:
            sov._SECRET_VALUES.clear()
            sov._SECRET_VALUES.update(anh_chup)
        sov._ENV_BE_CACHE = cache_cu


def _settings(**kw):
    """Giả ``get_settings`` có ``@lru_cache`` y như bản thật (``config.py:319-321``)."""
    mac_dinh = {
        "ocr_use_local_first": False,
        "ocr_use_vision_api": False,
        "openrouter_api_key": "",
        "openrouter_api_url": "",
        "groq_api_key": "",
        "gdoc_parser_url": "",
        "ocr_device": "cpu",
        "ocr_enable_marker_on_cpu": False,
    }
    return lru_cache()(lambda: NS(**{**mac_dinh, **kw}))


# --------------------------------------------------------------------------
# AC-01 — cưỡng bức config
# --------------------------------------------------------------------------


def test_env_cuong_buc_tat_ca_nhanh_ton_tien():
    """Cả hai cờ OCR và cả ba khoá/URL đều bị ép, không sót cái nào."""
    assert ENV_CUONG_BUC["OCR_USE_LOCAL_FIRST"] == "false"
    assert ENV_CUONG_BUC["OCR_USE_VISION_API"] == "false"
    assert ENV_CUONG_BUC["OPENROUTER_API_KEY"] == ""
    assert ENV_CUONG_BUC["GROQ_API_KEY"] == ""
    # gdoc-parser: host thật từ chối kết nối sau 2.06s → 204 tài liệu ≈ 7 phút ném đi.
    assert ENV_CUONG_BUC["GDOC_PARSER_URL"] == ""


def test_ap_env_ghi_that_vao_os_environ(monkeypatch):
    """Phải ghi **trước** khi import BE: `_api_key`, `_gdoc_parser_url`, `_groq_api_key`
    bị đóng băng ở cấp module lúc import (`openrouter_document_parser.py:30-38`)."""
    from ocr_bench.adapters.sovereign import _ap_env  # noqa: PLC0415

    monkeypatch.setenv("OCR_USE_VISION_API", "true")
    _ap_env()
    assert os.environ["OCR_USE_VISION_API"] == "false"
    assert os.environ["OPENROUTER_API_KEY"] == ""


def test_tran_tu_env_nem_khi_khong_doc_duoc(monkeypatch):
    """Nâng trần bằng env mà gõ sai thì phải **nổ**, không rơi về mặc định.

    Rơi về mặc định là kiểu hỏng tệ nhất của một cơ chế an toàn: người chạy tưởng đã nâng
    trần, lượt chạy dừng giữa chừng, không ai hiểu vì sao.
    """
    monkeypatch.setenv("SOVEREIGN_TRAN_SO_TAI_LIEU", "nhieu")
    with pytest.raises(ValueError, match="SOVEREIGN_TRAN_SO_TAI_LIEU"):
        SovereignAdapter()


def test_tran_tu_env_duoc_ap_dung(monkeypatch):
    monkeypatch.setenv("SOVEREIGN_TRAN_SO_TAI_LIEU", "7")
    assert SovereignAdapter().tran_so_tai_lieu == 7
    # tham số gọi hàm vẫn thắng env
    assert SovereignAdapter(tran_so_tai_lieu=3).tran_so_tai_lieu == 3


def test_kiem_config_chap_nhan_khi_da_tat():
    c = kiem_config(_settings())
    assert c["ocr_use_vision_api"] is False
    assert c["api_key_present"] is False


def test_kiem_config_nem_khi_vision_van_bat():
    """Đây là ca thật: `.env` và `.env.stag` của BE **đều** đặt OCR_USE_VISION_API=true."""
    with pytest.raises(VuotTran, match="Cưỡng bức env thất bại"):
        kiem_config(_settings(ocr_use_vision_api=True))


def test_kiem_config_nem_khi_con_khoa_api():
    """Khoá còn nạp là còn gọi được API tính tiền, dù cờ đã tắt."""
    with pytest.raises(VuotTran, match="api_key_present=True"):
        kiem_config(_settings(openrouter_api_key="sk-that-25-ky-tu-xxxx"))


@pytest.mark.parametrize(
    ("unsafe", "match"),
    [
        (
            {"openrouter_api_url": "https://paid.example/v1?token=raw"},
            "remote_url_present",
        ),
        ({"gdoc_parser_url": "http://paid.example/parser"}, "remote_url_present"),
        ({"groq_api_key": "seeded-groq-value"}, "api_key_present"),
    ],
)
def test_kiem_config_nem_khi_con_remote_url_hoac_groq_key(unsafe, match):
    """Removing any resolved URL/key check would re-enable an external call path."""
    with pytest.raises(VuotTran, match=match):
        kiem_config(_settings(**unsafe))


def test_kiem_config_xoa_cache_lru():
    """``get_settings`` có ``@lru_cache()``.

    Nếu tiến trình lỡ import ``app.config`` trước khi ta ghi ``os.environ`` thì bản cache
    vẫn mang giá trị của ``.env``. Không xoá cache = kiểm một đối tượng khác với đối
    tượng pipeline sẽ dùng.
    """
    goi = {"n": 0}

    @lru_cache()
    def get_settings():
        goi["n"] += 1
        return NS(
            ocr_use_local_first=False,
            ocr_use_vision_api=False,
            openrouter_api_key="",
            openrouter_api_url="",
            groq_api_key="",
            gdoc_parser_url="",
            ocr_device="cpu",
        )

    get_settings()  # nạp cache "cũ"
    kiem_config(get_settings)
    assert goi["n"] == 2, "kiem_config phải gọi cache_clear rồi giải lại"


# --------------------------------------------------------------------------
# AC-02 — trần chi phí
# --------------------------------------------------------------------------


def test_tran_phai_duong():
    with pytest.raises(ValueError):
        SovereignAdapter(tran_giay_tong=0)


def test_tran_so_tai_lieu_chan_truoc_khi_goi_pipeline(tmp_path: Path):
    a = SovereignAdapter(tran_so_tai_lieu=2)
    a._da_chay = 2
    f = tmp_path / "x.pdf"
    f.write_bytes(b"%PDF-1.4\n")
    with pytest.raises(VuotTran, match="trần số tài liệu"):
        a.run(f)


def test_tran_tong_thoi_gian_chan(tmp_path: Path):
    a = SovereignAdapter(tran_giay_tong=10.0)
    a._tong_giay = 10.5
    f = tmp_path / "x.pdf"
    f.write_bytes(b"%PDF-1.4\n")
    with pytest.raises(VuotTran, match="trần tổng thời gian"):
        a.run(f)


def test_tran_moi_tai_lieu_chan_sau_khi_chay():
    """Trần/tài liệu kiểm ở **biên**, vì lời gọi BE là đồng bộ, không cắt ngang được."""
    a = SovereignAdapter(tran_giay_moi_tai_lieu=1.0)
    with pytest.raises(VuotTran, match="trần thời gian một tài liệu"):
        a._kiem_tran_sau(54.0, "mot-trang-scan")


def test_vuot_tran_khong_bi_execute_nuot(tmp_path: Path):
    """Cổng quan trọng nhất của AC-02.

    ``Adapter.execute()`` bắt ``Exception`` và biến lỗi thành một dòng ``failed=True``
    rồi chạy tiếp — đúng cho engine hỏng, sai chết người cho trần chi phí. ``VuotTran``
    kế thừa ``BaseException`` chính vì thế. Test này là thứ giữ cho quyết định đó không
    bị ai "dọn dẹp" thành ``Exception``.
    """
    assert issubclass(VuotTran, BaseException)
    assert not issubclass(VuotTran, Exception)

    a = SovereignAdapter(tran_so_tai_lieu=1)
    a._da_chay = 1
    f = tmp_path / "x.pdf"
    f.write_bytes(b"%PDF-1.4\n")
    with pytest.raises(VuotTran):
        a.execute(f)


# --------------------------------------------------------------------------
# AC-03 — fingerprint
# --------------------------------------------------------------------------


def test_fingerprint_khong_rong_va_du_truong():
    fp = SovereignAdapter().config_fingerprint()
    for truong in (
        "mode",
        "marker_available",
        "be_commit",
        "be_dirty",
        "marker_version",
        "marker_package_available",
        "marker_model_cache_ready",
        "marker_model_cache",
        "marker_runtime_loaded",
        "marker_runtime_device",
        "python",
    ):
        assert truong in fp, truong
    assert fp["mode"] in ("light", "full")
    assert isinstance(fp["marker_available"], bool)
    assert "be_path" not in fp
    assert "env_forced" not in fp


def test_fingerprint_khong_chua_gia_tri_khoa():
    """`prediction/` được commit. Một khoá lọt vào fingerprint là lọt vào git."""
    a = SovereignAdapter()
    a._config = kiem_config(_settings())
    fp = a.config_fingerprint()
    assert fp["api_key_present"] is False
    assert all(not str(v).startswith("sk-") for v in fp.values())
    assert "openrouter_api_key" not in fp


def test_fingerprint_ghi_ca_tran():
    fp = SovereignAdapter(tran_giay_tong=99.0).config_fingerprint()
    assert fp["tran_giay_tong"] == 99.0


# --------------------------------------------------------------------------
# Task 6 — frozen publication profiles and fail-closed environment gates
# --------------------------------------------------------------------------


def test_sovereign_profiles_bind_exact_identity_and_config():
    default = SovereignAdapter.from_profile(CATALOG["sovereign_default"])
    scan = SovereignAdapter.from_profile(CATALOG["sovereign_scan"])

    assert (default.name, default.engine_family, default.profile) == (
        "sovereign_default",
        "sovereign",
        "default",
    )
    assert (scan.name, scan.engine_family, scan.profile) == (
        "sovereign_scan",
        "sovereign",
        "scan",
    )
    assert default.config_fingerprint()["profile_config_sha256"] == CATALOG[
        "sovereign_default"
    ].fingerprint
    assert scan.config_fingerprint()["profile_config_sha256"] == CATALOG[
        "sovereign_scan"
    ].fingerprint


def test_sovereign_profile_rejects_catalog_drift():
    source = CATALOG["sovereign_scan"]
    changed = EngineProfile(
        name=source.name,
        family=source.family,
        profile=source.profile,
        adapter=source.adapter,
        config={"ocr_use_vision_api": False, "api_enabled": True},
        environment=source.environment,
    )
    with pytest.raises(ProfileConfigError, match="config"):
        SovereignAdapter.from_profile(changed)


def test_sovereign_default_refuses_marker_environment(monkeypatch):
    monkeypatch.setattr(
        sov,
        "marker_runtime_state",
        lambda: _marker_state(package_available=True, model_cache_ready=True),
    )
    adapter = SovereignAdapter.from_profile(CATALOG["sovereign_default"])

    with pytest.raises(sov.ProfileEnvironmentError, match="marker_available"):
        adapter.preflight()


def test_sovereign_scan_requires_marker(monkeypatch):
    monkeypatch.setattr(
        sov,
        "marker_runtime_state",
        lambda: _marker_state(package_available=False, model_cache_ready=False),
    )
    adapter = SovereignAdapter.from_profile(CATALOG["sovereign_scan"])

    with pytest.raises(sov.ProfileEnvironmentError, match="marker_available"):
        adapter.preflight()


def test_sovereign_rejects_gpu_without_claiming_device(monkeypatch):
    adapter = SovereignAdapter.from_profile(CATALOG["sovereign_scan"])
    called = False

    def forbidden_preflight():
        nonlocal called
        called = True

    monkeypatch.setattr(adapter, "preflight", forbidden_preflight)
    with pytest.raises(RuntimeError, match="GPU|CUDA|verify"):
        adapter.configure_hardware("gpu")
    assert called is False
    assert adapter.config_fingerprint()["device"] == "unverified"


def test_sovereign_cpu_configuration_records_versioned_evidence(monkeypatch):
    adapter = SovereignAdapter.from_profile(CATALOG["sovereign_default"])
    monkeypatch.setattr(adapter, "preflight", lambda: adapter.config_fingerprint())

    assert adapter.configure_hardware("cpu") == "cpu"
    fingerprint = adapter.config_fingerprint()
    assert fingerprint["hardware"] == "cpu"
    assert fingerprint["device"] == "cpu"
    assert fingerprint["hardware_evidence_version"] == 1
    assert fingerprint["device_evidence"] == "be-settings-ocr-device-cpu"


def _profile_adapter(
    name: str,
    response: dict[str, object],
) -> SovereignAdapter:
    adapter = SovereignAdapter.from_profile(CATALOG[name])
    adapter._pipeline = lambda _data, _suffix, **_: response
    adapter._config = kiem_config(
        _settings(ocr_enable_marker_on_cpu=name.endswith("_scan")),
        marker_enabled=name.endswith("_scan"),
    )
    adapter._preflight_complete = True
    adapter._hardware = "cpu"
    adapter._hardware_verified = True
    is_scan = name.endswith("_scan")
    adapter._marker_state = sov.MarkerRuntimeState(
        package_available=is_scan,
        model_cache_ready=is_scan,
        runtime_loaded=False,
        runtime_device=None,
    )
    return adapter


@pytest.mark.parametrize(
    ("name", "success"),
    [("sovereign_default", True), ("sovereign_scan", False)],
)
def test_sovereign_result_keeps_profile_identity_for_success_and_failure(
    tmp_path, name, success
):
    response: dict[str, object] = {"success": success, "fullText": "public text"}
    if not success:
        response.update(error_code="ocr.markerFailed", message="cache failure")
    result = _profile_adapter(name, response).run(_pdf(tmp_path))

    assert (result.engine, result.engine_family, result.profile) == (
        name,
        "sovereign",
        CATALOG[name].profile,
    )
    assert result.raw_artifacts[0].name == "sovereign.json"
    assert result.raw_artifacts[0].data == json.dumps(
        {"fullText": "public text", "success": success},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def test_sovereign_raw_fingerprint_and_error_redact_seeded_secrets(
    tmp_path, monkeypatch
):
    openrouter = "seeded-openrouter-value-123"
    groq = "seeded-groq-value-456"
    monkeypatch.setenv("OPENROUTER_API_KEY", openrouter)
    monkeypatch.setenv("GROQ_API_KEY", groq)
    adapter = _profile_adapter(
        "sovereign_default",
        {
            "success": False,
            "fullText": f"leak {openrouter}",
            "message": f"failed with {groq}",
        },
    )
    result = adapter.run(_pdf(tmp_path))
    serialized = b"\n".join(
        [
            result.raw_artifacts[0].data,
            json.dumps(result.config_fingerprint, sort_keys=True).encode(),
            (result.error or "").encode(),
        ]
    )

    assert openrouter.encode() not in serialized
    assert groq.encode() not in serialized
    assert b"<redacted>" in serialized


@pytest.mark.parametrize(
    "env_name",
    [
        "OPENROUTER_API_KEY",
        "GROQ_API_KEY",
        "OPENROUTER_API_URL",
        "GDOC_PARSER_URL",
    ],
)
def test_sovereign_pipeline_exception_hides_opaque_env_secret_from_traceback(
    tmp_path, monkeypatch, env_name
):
    """The exception wrapper must hide exact secrets generic regexes cannot detect."""
    secret = f"opaque-value-for-{env_name.lower()}-94731"
    monkeypatch.setenv(env_name, secret)
    adapter = _profile_adapter("sovereign_default", {"success": True})

    def fail_pipeline(_data, _suffix, **_kwargs):
        raise RuntimeError(f"backend exploded with {secret}")

    adapter._pipeline = fail_pipeline
    result = adapter.execute(_pdf(tmp_path))
    serialized = json.dumps(
        {
            "error": result.error,
            "fingerprint": result.config_fingerprint,
        },
        sort_keys=True,
    )

    assert result.failed is True
    assert secret not in serialized
    assert "<redacted>" in serialized


@pytest.mark.parametrize(
    ("raised", "expected"),
    [
        (TimeoutError, FailureKind.TIMEOUT),
        (MemoryError, FailureKind.OOM),
        (FileNotFoundError, FailureKind.ENVIRONMENT_ERROR),
        (ImportError, FailureKind.ENVIRONMENT_ERROR),
        (RuntimeError, FailureKind.ENGINE_ERROR),
    ],
)
def test_sovereign_sanitized_wrapper_keeps_failure_taxonomy(
    tmp_path, monkeypatch, raised, expected
):
    """Hiding the backend exception must not collapse every crash into ENGINE_ERROR.

    Task 2 fixed the taxonomy at the adapter boundary; a timeout, an OOM and a missing
    dependency each drive a different reading of the fail-rate column. Redaction is a
    property of the *message*, not a reason to throw the classification away.
    """
    secret = "opaque-taxonomy-secret-55192"
    monkeypatch.setenv("OPENROUTER_API_KEY", secret)
    adapter = _profile_adapter("sovereign_default", {"success": True})

    def fail_pipeline(_data, _suffix, **_kwargs):
        raise raised(f"backend died holding {secret}")

    adapter._pipeline = fail_pipeline
    result = adapter.execute(_pdf(tmp_path))
    serialized = json.dumps(
        {"error": result.error, "fingerprint": result.config_fingerprint},
        sort_keys=True,
    )

    assert result.failed is True
    assert result.failure_kind is expected
    assert secret not in serialized
    assert "<redacted>" in serialized


def _marker_state(**changes):
    """Dựng `MarkerRuntimeState` thật, không phải `SimpleNamespace`.

    `marker_available` của lớp thật là **property dẫn xuất** từ hai cờ kia. Bản
    `SimpleNamespace` cho phép đặt tay `marker_available=True` cùng lúc với
    `package_available=False` — một trạng thái lớp thật không bao giờ tạo ra được —
    nên chính công thức mà fingerprint dùng chưa bao giờ được test chạy qua.
    """
    defaults = {
        "package_available": True,
        "model_cache_ready": True,
        "runtime_loaded": False,
        "runtime_device": None,
    }
    changes.pop("marker_available", None)
    return sov.MarkerRuntimeState(**{**defaults, **changes})


def test_sovereign_scan_cpu_rejects_preloaded_cuda_runtime():
    adapter = SovereignAdapter.from_profile(CATALOG["sovereign_scan"])

    with pytest.raises(sov.ProfileEnvironmentError, match="cuda|runtime_device"):
        adapter._validate_marker_runtime(
            _marker_state(runtime_loaded=True, runtime_device="cuda:0")
        )
    assert adapter._hardware_verified is False


def test_sovereign_default_rejects_loaded_marker_without_package_or_cache():
    adapter = SovereignAdapter.from_profile(CATALOG["sovereign_default"])

    with pytest.raises(sov.ProfileEnvironmentError, match="runtime_loaded"):
        adapter._validate_marker_runtime(
            _marker_state(
                package_available=False,
                model_cache_ready=False,
                marker_available=False,
                runtime_loaded=True,
                runtime_device="cpu",
            )
        )


@pytest.mark.parametrize(
    ("package_available", "cache_ready", "marker_available"),
    [(False, True, False), (True, False, False), (True, True, True)],
)
def test_marker_probe_keeps_package_and_cache_signals_separate(
    monkeypatch, package_available, cache_ready, marker_available
):
    service = NS(
        _surya_models_cached=lambda: cache_ready,
        _model_refs=None,
        _device_str=None,
    )
    monkeypatch.setattr(sov, "_load_marker_service", lambda: service, raising=False)
    monkeypatch.setattr(
        sov.importlib.util,
        "find_spec",
        lambda name: object() if name == "marker" and package_available else None,
    )

    state = sov.marker_runtime_state()

    assert state.package_available is package_available
    assert state.model_cache_ready is cache_ready
    assert state.marker_available is marker_available
    assert state.runtime_loaded is False
    assert state.runtime_device is None


class _NoMinhBach:
    """Đối tượng có `.device` và `.parameters` là property **ném**.

    Không phải trường hợp bịa: predictor của Marker/Surya nạp lười, và một property
    truy cập model chưa nạp (hoặc CUDA đã bị thu hồi) ném là chuyện bình thường.
    """

    @property
    def device(self):
        raise RuntimeError("thiết bị không đọc được")

    @property
    def parameters(self):
        raise RuntimeError("model chưa nạp")


class _LazyNoDict:
    """Predictor nạp lười: chạm vào `.model` là **nạp model**."""

    def __init__(self):
        self.da_nap = False

    def __getattr__(self, ten):
        if ten == "model":
            self.__dict__["da_nap"] = True
            return NS(device="cuda:0")
        raise AttributeError(ten)


def test_model_ref_probe_stays_fail_closed_when_an_attribute_raises():
    """Đầu dò thiết bị không được biến một tài liệu hỏng thành lượt chạy hỏng.

    `marker_runtime_live()` được gọi từ `config_fingerprint()` **bên trong** except
    handler của `execute()`. Ngoại lệ thoát ra từ đây không thành một dòng
    `failed=True` mà giết cả lượt chạy 204 tài liệu — và thứ nó bảo vệ chỉ là *nhãn
    thiết bị*, thông tin ít giá trị hơn nhiều so với 203 dòng còn lại.
    """
    assert sov._model_ref_devices(_NoMinhBach()) == set()
    assert sov._model_ref_devices({"layout": _NoMinhBach()}) == set()
    assert sov._model_ref_devices([_NoMinhBach(), NS(device="cpu")]) == {"cpu"}


def test_model_ref_probe_does_not_load_a_lazy_model_to_read_its_device():
    """Hỏi "model ở thiết bị nào" mà làm model được nạp là đã đổi thứ đang đo."""
    predictor = _LazyNoDict()

    assert sov._model_ref_devices({"layout": predictor}) == set()
    assert predictor.da_nap is False


def test_runtime_live_probe_stays_fail_closed_when_model_refs_raise(monkeypatch):
    service = NS(_model_refs={"layout": _NoMinhBach()}, _device_str=None)
    # Đầu dò đọc `sys.modules` chứ không import — nên test cũng phải đặt vào đúng đó.
    monkeypatch.setitem(sys.modules, "app.services.marker_ocr_service", service)

    assert sov.marker_runtime_live() == (True, None)


def test_runtime_state_probe_stays_fail_closed_when_model_refs_raise(monkeypatch):
    class _Service:
        @staticmethod
        def _surya_models_cached():
            return True

        @property
        def _model_refs(self):
            raise RuntimeError("BE sập giữa chừng")

        _device_str = None

    monkeypatch.setattr(sov, "_load_marker_service", lambda: _Service(), raising=False)
    monkeypatch.setattr(sov.importlib.util, "find_spec", lambda name: None)

    state = sov.marker_runtime_state()

    assert state.runtime_loaded is False
    assert state.runtime_device is None
    assert state.model_cache_ready is True


def test_sovereign_pipeline_dynamic_import_creates_no_bytecode(tmp_path, monkeypatch):
    module_name = "sovereign_be_dynamic_fixture"
    module_file = tmp_path / f"{module_name}.py"
    module_file.write_text("VALUE = 'loaded'\n", encoding="utf-8")
    monkeypatch.syspath_prepend(str(tmp_path))
    sys.modules.pop(module_name, None)
    adapter = _profile_adapter("sovereign_default", {"success": True})

    def importing_pipeline(_data, _suffix, **_kwargs):
        loaded = importlib.import_module(module_name)
        return {"success": True, "fullText": loaded.VALUE}

    adapter._pipeline = importing_pipeline
    try:
        result = adapter.run(_pdf(tmp_path))
    finally:
        sys.modules.pop(module_name, None)

    assert result.text_md == "loaded"
    assert not list(tmp_path.rglob("*.pyc"))


def test_sovereign_be_discovery_handles_nested_worktree(monkeypatch, tmp_path):
    repo = tmp_path / "sovereign"
    fake_module = (
        repo
        / "ocr-bench"
        / ".worktrees"
        / "ocr-parser-benchmark"
        / "src"
        / "ocr_bench"
        / "adapters"
        / "sovereign.py"
    )
    expected = repo / "adminPortal" / "back-end-admin-portal"
    expected.mkdir(parents=True)
    monkeypatch.delenv("SOVEREIGN_BE_PATH", raising=False)
    monkeypatch.setattr(sov, "__file__", str(fake_module))

    assert duong_dan_be() == expected.resolve()


def test_sovereign_be_explicit_path_remains_authoritative(monkeypatch, tmp_path):
    explicit = tmp_path / "chosen"
    monkeypatch.setenv("SOVEREIGN_BE_PATH", str(explicit))

    assert duong_dan_be() == explicit.resolve()


# --------------------------------------------------------------------------
# Khai báo năng lực
# --------------------------------------------------------------------------


def test_chi_khai_text_md():
    """Pipeline trả đúng ``{success, fullText}`` — khai thêm gì cũng là khai khống.

    ``images`` luôn rỗng chính là biểu hiện đo được của điểm mất dữ liệu #1 và #2 ở §2
    (ảnh Marker bị vứt, ảnh DOCX bị lột).
    """
    assert SovereignAdapter.capabilities == frozenset({Capability.TEXT_MD})


# --------------------------------------------------------------------------
# Chuẩn hoá đầu ra — chạy được không cần BE bằng cách tiêm thẳng pipeline giả
# --------------------------------------------------------------------------


def _adapter_gia(tra_ve: dict, **kw) -> SovereignAdapter:
    """Bỏ qua ``_nap()`` bằng cách gán sẵn ``_pipeline``.

    Hợp lệ vì đây đúng là hợp đồng của bộ nối với BE: một callable
    ``(base64, đuôi) -> dict``. Tiêm nó vào cho phép kiểm phần *chuẩn hoá* trên máy
    không có BE — mà chuẩn hoá mới là chỗ dễ sai lặng lẽ.
    """
    a = SovereignAdapter(**kw)
    a._pipeline = lambda du_lieu, duoi, **_: tra_ve
    a._config = kiem_config(_settings())
    return a


def _pdf(tmp_path: Path, ten: str = "x.pdf") -> Path:
    f = tmp_path / ten
    f.write_bytes(b"%PDF-1.4\n")
    return f


def test_thanh_cong_cho_ra_text_md(tmp_path: Path):
    a = _adapter_gia({"success": True, "fullText": "xin chào"})
    r = a.run(_pdf(tmp_path))
    assert r.failed is False
    assert r.text_md == "xin chào"
    assert r.error is None
    assert r.doc_id == "x"
    assert a._da_chay == 1


def test_that_bai_giu_nguyen_error_code(tmp_path: Path):
    """``success=False`` là **dữ liệu** của FailRate, không phải sự cố của bench.

    Mã lỗi riêng của pipeline (``ocr.markerFailed``, ``ocr.pdfEncrypted``…) phải đi qua
    nguyên vẹn — gộp hết thành "lỗi" là vứt đi thứ duy nhất cho biết *vì sao* hỏng.
    """
    a = _adapter_gia(
        {"success": False, "error_code": "ocr.markerFailed", "message": "models not cached"}
    )
    r = a.run(_pdf(tmp_path))
    assert r.failed is True
    assert r.text_md is None
    assert "ocr.markerFailed" in r.error and "models not cached" in r.error


def test_that_bai_khong_co_ma_van_co_error(tmp_path: Path):
    """``OcrResult.__post_init__`` ném nếu ``failed`` mà ``error`` rỗng — phải có mặc định."""
    a = _adapter_gia({"success": False})
    r = a.run(_pdf(tmp_path))
    assert r.failed is True
    assert r.error


def test_tong_giay_cong_don_qua_nhieu_tai_lieu(tmp_path: Path):
    """Trần tổng chỉ có nghĩa nếu thời gian thực sự được cộng dồn."""
    a = _adapter_gia({"success": True, "fullText": "a"})
    for i in range(3):
        a.run(_pdf(tmp_path, f"d{i}.pdf"))
    assert a._da_chay == 3
    assert a._tong_giay > 0.0


def test_duoi_file_duoc_truyen_xuong_pipeline(tmp_path: Path):
    """Pipeline BE nhánh theo đuôi file — truyền sai đuôi là đo nhầm nhánh."""
    thay = {}
    a = SovereignAdapter()
    a._config = kiem_config(_settings())
    a._pipeline = lambda du_lieu, duoi, **_: thay.update(duoi=duoi, n=len(du_lieu)) or {
        "success": True,
        "fullText": "x",
    }
    a.run(_pdf(tmp_path, "y.DOCX"))
    assert thay["duoi"] == "docx", "phải hạ chữ thường và bỏ dấu chấm"
    assert thay["n"] > 0, "phải truyền base64 chứ không truyền đường dẫn"


def test_version_khong_nem_khi_khong_co_repo(monkeypatch):
    monkeypatch.setenv("SOVEREIGN_BE_PATH", "/khong/ton/tai")
    assert isinstance(SovereignAdapter().version(), str)


# --------------------------------------------------------------------------
# Cần BE thật
# --------------------------------------------------------------------------


@needs_be
def test_that_config_giai_ra_false_du_env_bao_true():
    """Bằng chứng trực tiếp cho AC-01.

    ``.env`` của BE đặt cả hai cờ ``true`` và ``config.py:10`` ghim ``_ENV_FILE`` theo
    đường dẫn — nên nếu cưỡng bức không hiệu lực, test này đỏ.
    """
    from ocr_bench.adapters.sovereign import nap_pipeline

    nap_pipeline()
    from app.config import get_settings  # noqa: PLC0415

    s = get_settings()
    assert s.ocr_use_vision_api is False
    assert not (s.openrouter_api_key or "").strip()
    assert os.environ["OCR_USE_VISION_API"] == "false"


# ------------------------------------------------ vòng sửa 2: rò rỉ ngoài `run()`


def test_preflight_wraps_backend_errors_before_they_reach_artifacts(monkeypatch):
    """Lỗi lúc *nạp* BE cũng phải đi qua bộ lọc, không chỉ lỗi lúc chạy tài liệu.

    `nap_pipeline()` gọi `get_settings()`; một `ValidationError` của pydantic in lại
    **giá trị đầu vào** — và giá trị đầu vào ở đây chính là `.env` của BE. Trước fix
    này nó đi thẳng ra `error` và `config_fingerprint.traceback` mà chỉ qua regex chung.
    """
    secret = "opaque-preflight-secret-77213"
    monkeypatch.setenv("OPENROUTER_API_KEY", secret)
    adapter = SovereignAdapter.from_profile(CATALOG["sovereign_default"])

    def no_pipeline(**_kwargs):
        raise ValueError(f"1 validation error for Settings: input={secret}")

    monkeypatch.setattr(sov, "nap_pipeline", no_pipeline)
    monkeypatch.setattr(
        sov, "marker_runtime_state", lambda: _marker_state(
            package_available=False, model_cache_ready=False
        )
    )

    with pytest.raises(sov.SanitizedPipelineError) as thong_tin:
        adapter.preflight()
    assert secret not in str(thong_tin.value)
    assert "<redacted>" in str(thong_tin.value)


def test_preflight_still_raises_its_own_environment_error_unchanged(monkeypatch):
    """Bọc lỗi BE không được nuốt lỗi *của bench*.

    `configure_hardware` và runner bắt `ProfileEnvironmentError` theo kiểu; đổi kiểu
    thì cổng "profile này không khớp runtime" im lặng biến mất.

    Lỗi phải được ném **từ trong** `_boc_loi_be()` mới kiểm được điều đó. Bản trước
    dựng lỗi ở `_validate_marker_runtime()`, tức hai dòng *trước* khối được bọc — nó
    xanh kể cả khi `_LOI_NOI_BO` bị xoá sạch, nên nó chứng minh đúng con số không.
    """
    adapter = SovereignAdapter.from_profile(CATALOG["sovereign_scan"])
    monkeypatch.setattr(
        sov, "marker_runtime_state", lambda: _marker_state(
            package_available=True, model_cache_ready=True
        )
    )

    def nap_hong(**_kwargs):
        raise sov.ProfileEnvironmentError("runtime không khớp profile")

    monkeypatch.setattr(sov, "nap_pipeline", nap_hong)

    with pytest.raises(sov.ProfileEnvironmentError, match="runtime không khớp profile"):
        adapter.preflight()


def test_secret_inventory_survives_env_scrubbing_of_a_previous_profile(monkeypatch):
    """Profile thứ hai phải bịt được đúng chuỗi mà profile đầu đã xoá khỏi env."""
    secret = "opaque-two-profile-secret-31889"
    monkeypatch.setenv("OPENROUTER_API_KEY", secret)
    dau = SovereignAdapter.from_profile(CATALOG["sovereign_default"])
    assert secret in dau._sensitive_values

    sov._ap_env(marker_enabled=False)  # đúng thứ `preflight()` của profile #1 làm
    assert not os.environ.get("OPENROUTER_API_KEY")

    sau = SovereignAdapter.from_profile(CATALOG["sovereign_scan"])
    assert secret in sau._sensitive_values


def test_fingerprint_reports_redactions_made_to_the_scored_text(tmp_path, monkeypatch):
    """Bịt chuỗi trong `text_md` làm điểm accuracy tụt — phải có dấu vết, không im lặng."""
    secret = "opaque-inside-text-secret-40277"
    monkeypatch.setenv("OPENROUTER_API_KEY", secret)

    sach = _profile_adapter("sovereign_default", {"success": True, "fullText": "chỉ là văn bản"})
    ket_sach = sach.execute(_pdf(tmp_path))
    assert ket_sach.config_fingerprint["scored_text_redactions"] == 0

    ban = _profile_adapter(
        "sovereign_default", {"success": True, "fullText": f"tiêu đề {secret} kết"}
    )
    ket_ban = ban.execute(_pdf(tmp_path))
    assert secret not in (ket_ban.text_md or "")
    assert ket_ban.config_fingerprint["scored_text_redactions"] == 1


def test_marker_runtime_device_is_probed_at_scoring_time(tmp_path, monkeypatch):
    """`marker_runtime_*` phải là quan sát lúc chấm, không phải ảnh chụp preflight.

    Mọi preflight chạy xong trước tài liệu đầu tiên, nên ảnh chụp ấy **luôn** rỗng —
    204 dòng sẽ khai `runtime_device: null` kể cả khi Marker đã nạp model thật.
    """
    adapter = _profile_adapter("sovereign_scan", {"success": True, "fullText": "x"})
    assert adapter._marker_state.runtime_device is None

    monkeypatch.setattr(sov, "marker_runtime_live", lambda: (True, "cpu"))
    dau_van_tay = adapter.execute(_pdf(tmp_path)).config_fingerprint
    assert dau_van_tay["marker_runtime_loaded"] is True
    assert dau_van_tay["marker_runtime_device"] == "cpu"
    assert dau_van_tay["marker_preflight_runtime_device"] is None


def test_model_ref_probe_reaches_devices_held_on_attributes():
    """`_model_refs` thật là dict tên → predictor; device nằm ở thuộc tính của predictor."""
    predictor = NS(model=NS(device="cuda:0"))
    assert "cuda:0" in sov._model_ref_devices({"layout": predictor})


def test_failure_classification_never_raises_from_a_hostile_engine():
    class NoDoc(Exception):
        @property
        def failure_kind(self):
            raise RuntimeError("engine thù địch")

    from ocr_bench.adapters.base import classify_exception  # noqa: PLC0415

    assert classify_exception(NoDoc()) is FailureKind.ENGINE_ERROR


# --------------------------------------------------------------------------
# Ngưỡng độ dài, parser `.env`, cổng thiết bị lúc chạy
# --------------------------------------------------------------------------


def test_short_secret_is_redacted_from_errors_but_not_from_the_scored_text(
    tmp_path, monkeypatch
):
    """Ngưỡng 12 ký tự chỉ áp cho văn bản được chấm, không áp lúc thu thập.

    `.env` thật của BE có `BIZFLY_KEY` 10 ký tự. Áp ngưỡng lúc thu thập thì nó không
    bao giờ vào bộ thay-thế, nên nó lọt ra **cả** traceback lẫn thông điệp lỗi — nơi
    bịt thừa không tốn gì. Áp ngưỡng ở `fullText` thì ngược lại: thay một chuỗi 3 ký tự
    khỏi văn bản chấm điểm là làm tụt accuracy vì lý do không ai nhìn thấy.
    """
    ngan = "bf-key-99"  # 9 ký tự, dưới ngưỡng
    monkeypatch.setenv("BIZFLY_KEY", ngan)

    adapter = _profile_adapter("sovereign_default", {"success": True, "fullText": f"a {ngan} b"})
    assert ngan in adapter._sensitive_values, "phải được thu thập dù ngắn"

    ket = adapter.execute(_pdf(tmp_path))
    assert ngan in (ket.text_md or ""), "văn bản chấm điểm không được đụng vào"
    assert ket.config_fingerprint["scored_text_redactions"] == 0

    assert ngan not in sov._sanitize_runtime_text(f"boom {ngan}", adapter._sensitive_values)


def test_redaction_count_is_zero_on_the_failure_path(tmp_path, monkeypatch):
    """Không có văn bản nào được chấm thì không có điểm nào bị lớp bịt làm giảm."""
    secret = "opaque-failure-path-secret-70118"
    monkeypatch.setenv("OPENROUTER_API_KEY", secret)
    adapter = _profile_adapter(
        "sovereign_default",
        {"success": False, "error_code": "ocr.failed", "fullText": f"x {secret} y"},
    )
    ket = adapter.execute(_pdf(tmp_path))
    assert ket.failed is True
    assert ket.config_fingerprint["scored_text_redactions"] == 0


def test_env_parser_reaches_the_values_a_naive_split_would_miss(tmp_path, monkeypatch):
    """Ba dạng dòng dotenv hợp lệ; hụt dạng nào là chuỗi đó **lọt ra** artifact."""
    goc = tmp_path / "be"
    goc.mkdir()
    (goc / ".env").write_text(
        "\n".join(
            (
                "export API_KEY=ex-port-1234",
                "GROQ_TOKEN=gq-5678   # ghi chú cuối dòng",
                'DB_PASSWORD="quo-ted-90"',
                "HASH_SECRET=pass#word-11",
            )
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("SOVEREIGN_BE_PATH", str(goc))
    monkeypatch.setattr(sov, "_ENV_BE_CACHE", None, raising=False)

    doc = sov._doc_env_be()
    assert doc["API_KEY"] == "ex-port-1234", "`export ` phải bị gỡ khỏi tên"
    assert doc["GROQ_TOKEN"] == "gq-5678", "chú thích cuối dòng không phải một phần khoá"
    assert doc["DB_PASSWORD"] == "quo-ted-90"
    assert doc["HASH_SECRET"] == "pass#word-11", "`#` không có khoảng trắng trước là ký tự thường"


def test_env_file_is_read_once_not_once_per_document(tmp_path, monkeypatch):
    """`thu_thap_bi_mat()` chạy vài lần mỗi tài liệu; mỗi lần đọc lại là đọc khoá thật."""
    goc = tmp_path / "be"
    goc.mkdir()
    (goc / ".env").write_text("API_KEY=abcdefghijkl", encoding="utf-8")
    monkeypatch.setenv("SOVEREIGN_BE_PATH", str(goc))
    monkeypatch.setattr(sov, "_ENV_BE_CACHE", None, raising=False)

    dem = {"n": 0}
    that = Path.read_text

    def demdoc(self, *a, **k):
        if self.name == ".env":
            dem["n"] += 1
        return that(self, *a, **k)

    monkeypatch.setattr(Path, "read_text", demdoc)
    for _ in range(5):
        sov._doc_env_be()
    assert dem["n"] == 1


def test_secret_inventory_skips_values_that_would_corrupt_the_score(monkeypatch):
    """Tên khớp `key` không có nghĩa giá trị là khoá — `SCHEDULER_HOT_KEYWORDS` là ví dụ thật."""
    monkeypatch.setenv("SCHEDULER_HOT_KEYWORDS", "hợp đồng, quyết định, công văn")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-real-token-4417")
    bi_mat = sov.thu_thap_bi_mat()
    assert "sk-real-token-4417" in bi_mat
    assert "hợp đồng, quyết định, công văn" not in bi_mat


def test_run_refuses_to_publish_a_cpu_claim_next_to_a_non_cpu_runtime(tmp_path, monkeypatch):
    """Thiết bị đọc lúc chạy khác CPU → dừng, không ghi ra dòng khai `device: "cpu"`."""
    adapter = _profile_adapter("sovereign_scan", {"success": True, "fullText": "x"})
    monkeypatch.setattr(sov, "marker_runtime_live", lambda: (True, "cuda:0"))
    with pytest.raises(sov.ProfileEnvironmentError, match="cuda:0"):
        adapter.run(_pdf(tmp_path))
