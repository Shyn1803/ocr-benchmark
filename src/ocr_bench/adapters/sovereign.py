"""Bộ nối pipeline Sovereign BE — A7 (TASK-078).

Đây là **baseline**: không có nó thì mọi con số của Marker/OpenDataLoader/pdf-inspector
đều lơ lửng, vì không ai biết cái đang chạy production làm được tới đâu. Adapter gọi lại
đúng ``extract_text_from_document()`` của BE (``app/services/openrouter_document_parser.py:616``)
— **đọc, không sửa**. Không một dòng nào của ``adminPortal/`` bị đụng.

Bốn điều dưới đây đều là **kết quả đo**, và ba trong số đó ngược với điều kế hoạch giả định:

1. **Config production KHÔNG phải mặc định của code.** ``config.py:122,127`` để cả hai cờ
   ``False``, nhưng ``.env`` và ``.env.stag`` **đều bật cả hai lên ``true``**. Tệ hơn:
   ``config.py:10`` ghim ``_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"``
   — **theo đường dẫn, không theo cwd**. Nên ocr-bench đứng ở thư mục khác import vào vẫn
   nuốt nguyên ``.env`` của BE. Đo trần: import không cưỡng bức cho ra
   ``ocr_use_vision_api = True`` kèm ``openrouter_api_key`` đã nạp.

   Chạy 204 tài liệu ở trạng thái đó là **bấm nút tính tiền trên khoá thật**. Nên module
   này ghi ``os.environ`` **trước** khi import BE, rồi **kiểm lại giá trị đã giải** — sai
   thì ném, không chạy tiếp.

2. **Thứ tự cưỡng bức có ý nghĩa.** ``_api_key``, ``_api_url``, ``_model``,
   ``_gdoc_parser_url``, ``_groq_api_key`` bị đóng băng ở cấp module lúc import
   (``openrouter_document_parser.py:30-38``); chỉ hai cờ OCR là đọc tươi trong hàm. Ghi
   ``os.environ`` *sau* khi import là ghi vào chỗ không ai đọc nữa.

3. **``ocr_use_vision_api=False`` không có nghĩa là "không OCR".**
   ``_apply_vision_fallback()`` (``:418-420``) và ``_maybe_ocr_embedded_images()``
   (``:560-561``) đều có cổng chặn theo cờ này — nhưng ``_maybe_escalate_to_marker()``
   **không**. Xác nhận chạy thật với vision tắt: log vẫn in "Escalate sang Marker OCR cho
   file .pdf". Marker là ML cục bộ trên CPU, ``workers/ocr_worker.py:133-134`` ghi ~54 s/trang.
   Nên trần của A7 phải chặn **thời gian máy**, không chỉ tiền API.

4. **Suy thoái âm thầm là kiểu hỏng đặc trưng ở đây.** Thiếu ``pdfminer`` không ném — chỉ
   log WARNING rồi trả kết quả *tệ hơn*. Thiếu cache Surya cũng vậy: ``ocr.markerFailed``
   bị nuốt, ``success=False`` lặng lẽ. Một baseline đo trong môi trường thiếu trông y hệt
   baseline thật. Nên ``config_fingerprint`` phải ghi cả ``marker_available`` — và đó là
   lý do AC-03 tồn tại.

Hai chế độ đo, cùng một adapter, **không được trộn số**::

    .venv-sov/Scripts/python.exe    scripts/make_predictions.py --engines sovereign   # light
    .venv-marker/Scripts/python.exe scripts/make_predictions.py --engines sovereign   # full

``light`` chỉ có nhánh trích cục bộ; ``full`` có thêm leo thang Marker và **mới là
production thật**. ``marker_available`` trong fingerprint phân biệt hai bên.

Pipeline trả về đúng ``{success, fullText}`` — không bbox, không ảnh, không cấu trúc
trang. Nên ``capabilities = {TEXT_MD}``, chấm hết.
"""

from __future__ import annotations

import base64
import importlib.util
import json
import os
import subprocess
import sys
import threading
import time
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path
from typing import Any, Callable, ClassVar, Literal

from ocr_bench.adapters.base import Adapter, classify_exception
from ocr_bench.profiles import EngineProfile, ProfileConfigError
from ocr_bench.secrets import sanitize_secret_text
from ocr_bench.types import Capability, FailureKind, OcrResult, RawArtifact

__all__ = [
    "SovereignAdapter",
    "ProfileEnvironmentError",
    "SanitizedPipelineError",
    "VuotTran",
    "ENV_CUONG_BUC",
    "duong_dan_be",
    "nap_pipeline",
    "kiem_config",
    "marker_san_sang",
]


class ProfileEnvironmentError(RuntimeError):
    """The installed Sovereign runtime does not match its frozen profile."""


class SanitizedPipelineError(RuntimeError):
    """Adapter-owned error whose message and traceback contain no BE exception.

    Giấu exception gốc **không** được làm mất phân loại thất bại của nó: ``failure_kind``
    được tính từ exception gốc trước khi nó bị vứt, rồi ``classify_exception`` đọc lại
    ở biên adapter (Task 2). Thiếu trường này thì mọi timeout/OOM/thiếu dependency của
    BE đều hiện ra là ``ENGINE_ERROR``.
    """

    def __init__(self, message: str, failure_kind: FailureKind) -> None:
        super().__init__(message)
        self.failure_kind = failure_kind


class VuotTran(BaseException):
    """Chạm trần chi phí → dừng cả lượt chạy.

    Kế thừa ``BaseException`` **có chủ đích**: ``Adapter.execute()`` bắt ``Exception`` và
    biến mọi lỗi thành một dòng ``failed=True`` rồi chạy tiếp tài liệu sau — đúng cho lỗi
    engine, sai chết người cho trần chi phí. AC-02 đòi "vượt thì dừng, không chạy tiếp";
    một exception bị nuốt thành dòng kết quả là *không* dừng.
    """


#: Env ghi đè **trước** khi import BE. Giá trị rỗng = tắt hẳn nhánh tương ứng.
#:
#: ``.env`` của BE bật ``OCR_USE_*`` lên ``true`` và có khoá thật; ba khoá dưới bị ép rỗng
#: để dù có nhánh nào lọt qua cổng cờ thì cũng không còn gì để gọi. ``GDOC_PARSER_URL``
#: rỗng vì host thật (``123.27.191.11:9010``) đo được là **từ chối kết nối sau 2.06 s** —
#: 204 tài liệu × 2 s ≈ 7 phút ném đi trước khi rơi về nhánh local.
ENV_CUONG_BUC: dict[str, str] = {
    "OCR_USE_LOCAL_FIRST": "false",
    "OCR_USE_VISION_API": "false",
    "OPENROUTER_API_KEY": "",
    "OPENROUTER_API_URL": "",
    "GROQ_API_KEY": "",
    "GDOC_PARSER_URL": "",
    "OCR_DEVICE": "cpu",
    "CUDA_VISIBLE_DEVICES": "",
}

_PROFILE_CONFIG = {
    "ocr_use_vision_api": False,
    "api_enabled": False,
}
_PROFILE_ENVIRONMENTS = {
    "sovereign_default": {"marker_available": False},
    "sovereign_scan": {"marker_available": True},
}
_SECRET_ENV_NAMES = (
    "OPENROUTER_API_KEY",
    "GROQ_API_KEY",
    "OPENROUTER_API_URL",
    "GDOC_PARSER_URL",
)
_BE_EXECUTION_LOCK = threading.RLock()

#: Tên biến *gợi ý* mang bí mật. Danh sách cứng `_SECRET_ENV_NAMES` chỉ phủ được cái
#: adapter tự ép; BE nạp `.env` riêng của nó với `DB_PASSWORD`, `JWT_SECRET`,
#: `MAIL_PASSWORD`, `SENTRY_DSN`… — không tên nào trong số đó có mặt ở `os.environ` của
#: ocr-bench, nên nếu chỉ đọc env thì bộ giá trị cần thay khớp chính xác sẽ **rỗng** và
#: cả cơ chế tụt về đúng cái regex mà nó sinh ra để đỡ lưng.
_SECRET_NAME_HINTS = (
    "key",
    "secret",
    "token",
    "password",
    "passwd",
    "credential",
    "dsn",
)

#: Giá trị ngắn hơn ngưỡng này không được thay khớp-chính-xác. `POSTGRES_PASSWORD=abc`
#: mà đem thay mọi "abc" trong văn bản trích ra thì chỉ số chính xác tụt đi vì lý do
#: không ai nhìn thấy — một kiểu hỏng tệ hơn cả rò rỉ, vì nó im lặng và làm sai số liệu.
_DO_DAI_BI_MAT_TOI_THIEU = 12

_SECRET_VALUES_LOCK = threading.Lock()
_SECRET_VALUES: set[str] = set()


def _co_ve_bi_mat(ten: str) -> bool:
    t = ten.lower()
    return ten in _SECRET_ENV_NAMES or any(g in t for g in _SECRET_NAME_HINTS)


def _doc_env_be() -> dict[str, str]:
    """Đọc `.env` của BE **chỉ để biết chuỗi nào cần bịt**. Không ghi, không lan ra.

    Giá trị vào thẳng bộ thay-thế trong tiến trình và không bao giờ được ghi ra
    artifact, log hay fingerprint. Không đọc thì `_sensitive_values` rỗng trong lượt
    chạy thật, vì BE ghim `.env` theo đường dẫn chứ không theo `os.environ`.
    """
    ra: dict[str, str] = {}
    try:
        p = duong_dan_be() / ".env"
        if not p.is_file():
            return ra
        for dong in p.read_text(encoding="utf-8", errors="replace").splitlines():
            dong = dong.strip()
            if not dong or dong.startswith("#") or "=" not in dong:
                continue
            ten, _, gia_tri = dong.partition("=")
            ra[ten.strip()] = gia_tri.strip().strip("'\"")
    except BaseException:  # noqa: BLE001 - thu thập bí mật không được làm hỏng lượt chạy
        return {}
    return ra


def thu_thap_bi_mat() -> tuple[str, ...]:
    """Bộ giá trị cần bịt, **chỉ lớn thêm** qua vòng đời tiến trình.

    Chỉ-lớn-thêm là điểm mấu chốt: `preflight()` của profile đầu tiên gọi `_ap_env()`
    xoá trắng bốn biến, nên adapter dựng sau đó mà tự đọc `os.environ` sẽ thu được
    con số không. Một cơ chế an toàn tự tắt ở profile thứ hai, không cảnh báo, còn tệ
    hơn là chưa từng có.
    """
    # Danh sách chứ không phải dict theo tên: `os.environ` và `.env` của BE hay có
    # **cùng một tên với hai giá trị khác nhau**, và bịt cái này rồi bỏ cái kia thì
    # đúng giá trị đang chạy mới là cái lọt ra.
    ung_vien: list[str] = [
        gia_tri for ten, gia_tri in os.environ.items() if _co_ve_bi_mat(ten)
    ]
    ung_vien += [v for t, v in _doc_env_be().items() if _co_ve_bi_mat(t)]
    with _SECRET_VALUES_LOCK:
        for gia_tri in ung_vien:
            if gia_tri and len(gia_tri) >= _DO_DAI_BI_MAT_TOI_THIEU:
                _SECRET_VALUES.add(gia_tri)
        return tuple(sorted(_SECRET_VALUES, key=len, reverse=True))


@dataclass(frozen=True, slots=True)
class SovereignIdentity:
    name: str
    engine_family: str
    profile: str
    config: Mapping[str, object]
    environment: Mapping[str, object]
    profile_config_sha256: str


@dataclass(frozen=True, slots=True)
class MarkerRuntimeState:
    package_available: bool
    model_cache_ready: bool
    runtime_loaded: bool
    runtime_device: str | None

    @property
    def marker_available(self) -> bool:
        return self.package_available and self.model_cache_ready


UNKNOWN_MARKER_STATE = MarkerRuntimeState(
    package_available=False,
    model_cache_ready=False,
    runtime_loaded=False,
    runtime_device=None,
)


LEGACY_IDENTITY = SovereignIdentity(
    name="sovereign",
    engine_family="sovereign",
    profile="legacy",
    config=_PROFILE_CONFIG,
    environment={},
    profile_config_sha256="legacy",
)

#: Đuôi file → chuỗi mà BE mong đợi (nó nhận `extension` **không** có dấu chấm).
_DUOI_MAC_DINH = "pdf"


def _tu_env(ten: str, thu_cong: Any, mac_dinh: Any, kieu: Callable[[str], Any]) -> Any:
    """Ưu tiên tham số gọi hàm > env > mặc định. Env hỏng thì **ném**, không im lặng.

    ``SOVEREIGN_TRAN_SO_TAI_LIEU=nhieu`` mà bị bỏ qua để rơi về mặc định là kiểu hỏng tệ
    nhất của một cơ chế an toàn: người chạy tưởng đã nâng trần, lượt chạy dừng giữa chừng,
    và không ai hiểu vì sao.
    """
    if thu_cong is not None:
        return thu_cong
    if (gia_tri := os.environ.get(ten)) is None:
        return mac_dinh
    try:
        return kieu(gia_tri)
    except ValueError as exc:
        raise ValueError(f"{ten}={gia_tri!r} không đọc được thành {kieu.__name__}") from exc


@contextmanager
def _be_read_only():
    """Serialize BE imports/calls and suppress Python bytecode writes within them."""
    with _BE_EXECUTION_LOCK:
        previous = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        try:
            yield
        finally:
            sys.dont_write_bytecode = previous


def duong_dan_be() -> Path:
    """Thư mục gốc BE. Ghi đè bằng ``SOVEREIGN_BE_PATH`` nếu cây thư mục khác."""
    if thu_cong := os.environ.get("SOVEREIGN_BE_PATH"):
        return Path(thu_cong).resolve()

    # Cả checkout thường và worktree lồng đều nằm dưới đúng một ancestor ``ocr-bench``.
    # Chỉ duyệt ancestor của chính file này; không quét ổ đĩa hay dò repo lân cận.
    module_path = Path(__file__).resolve()
    for ancestor in module_path.parents:
        if ancestor.name == "ocr-bench":
            return (
                ancestor.parent / "adminPortal" / "back-end-admin-portal"
            ).resolve()
    # Fallback cũ cho layout được vendored/đổi tên; explicit env vẫn luôn authoritative.
    return (module_path.parents[4] / "adminPortal" / "back-end-admin-portal").resolve()


def _ap_env(*, marker_enabled: bool | None = None) -> None:
    """Ghi ``ENV_CUONG_BUC`` vào ``os.environ``. Gọi **trước** mọi import BE."""
    os.environ.update(ENV_CUONG_BUC)
    if marker_enabled is not None:
        os.environ["OCR_ENABLE_MARKER_ON_CPU"] = (
            "true" if marker_enabled else "false"
        )


def kiem_config(
    get_settings: Callable[[], Any], *, marker_enabled: bool | None = None
) -> dict[str, object]:
    """Giải config *sau* khi cưỡng bức và **kiểm lại**. Sai thì ném ``VuotTran``.

    Đây là điểm của AC-01: không tin vào việc "đã set env" mà hỏi lại chính đối tượng
    settings mà pipeline sẽ dùng. ``get_settings`` có ``@lru_cache()`` nên phải xoá cache
    — nếu tiến trình đã lỡ import ``app.config`` từ trước thì bản cache đó vẫn mang
    giá trị của ``.env``.
    """
    if xoa := getattr(get_settings, "cache_clear", None):
        xoa()
    s = get_settings()
    local_first = bool(getattr(s, "ocr_use_local_first", False))
    vision = bool(getattr(s, "ocr_use_vision_api", False))
    openrouter_key = bool((getattr(s, "openrouter_api_key", "") or "").strip())
    groq_key = bool((getattr(s, "groq_api_key", "") or "").strip())
    openrouter_url = bool((getattr(s, "openrouter_api_url", "") or "").strip())
    gdoc_url = bool((getattr(s, "gdoc_parser_url", "") or "").strip())
    marker_cpu = bool(getattr(s, "ocr_enable_marker_on_cpu", False))
    device = str(getattr(s, "ocr_device", "") or "").strip().lower()
    api_key_present = openrouter_key or groq_key
    remote_url_present = openrouter_url or gdoc_url
    api_enabled = vision or api_key_present or remote_url_present

    if api_enabled:
        raise VuotTran(
            "Cưỡng bức env thất bại: "
            f"ocr_use_vision_api={vision}, api_key_present={api_key_present}, "
            f"remote_url_present={remote_url_present}. "
            "Resolved BE config còn đường gọi ngoài/tính phí. Dừng."
        )
    if device != "cpu":
        raise VuotTran(
            f"Cưỡng bức device thất bại: ocr_device={device!r}, cần 'cpu'. Dừng."
        )
    if marker_enabled is not None and marker_cpu is not marker_enabled:
        raise VuotTran(
            "Cưỡng bức Marker thất bại: "
            f"ocr_enable_marker_on_cpu={marker_cpu}, cần {marker_enabled}. Dừng."
        )
    return {
        "ocr_use_local_first": local_first,
        "ocr_use_vision_api": vision,
        "api_enabled": api_enabled,
        # Chỉ presence booleans. Không URL, query token hay credential thô nào được ghi.
        "api_key_present": api_key_present,
        "openrouter_api_key_present": openrouter_key,
        "groq_api_key_present": groq_key,
        "remote_url_present": remote_url_present,
        "openrouter_api_url_present": openrouter_url,
        "gdoc_parser_url_present": gdoc_url,
        "ocr_device": device,
        "marker_cpu_enabled": marker_cpu,
    }


def _load_marker_service() -> Any:
    """Import the exact BE Marker module without allowing `.pyc` writes."""
    goc = duong_dan_be()
    if not (goc / "app" / "services" / "marker_ocr_service.py").is_file():
        raise FileNotFoundError("Sovereign BE marker_ocr_service.py is missing")
    if str(goc) not in sys.path:
        sys.path.insert(0, str(goc))
    with _be_read_only():
        from app.services import marker_ocr_service  # noqa: PLC0415

    return marker_ocr_service


def _normalize_device(value: object) -> str | None:
    if value is None:
        return None
    device = str(value).strip().lower()
    return device or None


def _model_ref_devices(value: object) -> set[str]:
    """Read a bounded sample of cached model refs without moving or clearing models."""
    devices: set[str] = set()
    pending: list[tuple[object, int]] = [(value, 0)]
    # `id()` chỉ là định danh duy nhất khi đối tượng còn sống. Giữ luôn tham chiếu ở
    # `giu` để không có đối tượng nào bị thu hồi rồi một đối tượng khác tái dùng đúng
    # id đó — nếu xảy ra, nhánh chứa `device` thật sẽ bị bỏ qua vì tưởng đã thăm.
    giu: list[object] = []
    seen: set[int] = set()
    while pending and len(seen) < 64:
        current, depth = pending.pop()
        marker = id(current)
        if marker in seen:
            continue
        seen.add(marker)
        giu.append(current)
        if (device := _normalize_device(getattr(current, "device", None))) is not None:
            devices.add(device)
        parameters = getattr(current, "parameters", None)
        if callable(parameters):
            try:
                first = next(iter(parameters()), None)
            except BaseException:  # probe must stay fail-closed and read-only
                first = None
            if first is not None and (
                device := _normalize_device(getattr(first, "device", None))
            ) is not None:
                devices.add(device)
        if depth >= 2:
            continue
        if isinstance(current, Mapping):
            pending.extend((nested, depth + 1) for nested in list(current.values())[:32])
        elif isinstance(current, (list, tuple)):
            pending.extend((nested, depth + 1) for nested in current[:32])
        else:
            # `_model_refs` thật là dict tên → **predictor**, và predictor giữ model ở
            # thuộc tính chứ không phải phần tử. Chỉ duyệt Mapping/list thì vòng lặp
            # dừng ngay tại predictor và không bao giờ nhìn thấy device thật.
            for ten in ("model", "models", "predictor", "processor"):
                try:
                    nested = getattr(current, ten, None)
                except BaseException:  # noqa: BLE001 - probe phải fail-closed
                    nested = None
                if nested is not None:
                    pending.append((nested, depth + 1))
    return devices


def marker_runtime_state() -> MarkerRuntimeState:
    """Probe package, cache, and already-loaded BE runtime as separate signals."""
    try:
        package_available = importlib.util.find_spec("marker") is not None
    except BaseException:
        package_available = False

    try:
        with _be_read_only():
            service = _load_marker_service()
    except BaseException:
        return MarkerRuntimeState(
            package_available=package_available,
            model_cache_ready=False,
            runtime_loaded=False,
            runtime_device=None,
        )

    with _be_read_only():
        try:
            cache_ready = bool(service._surya_models_cached())
        except BaseException:
            cache_ready = False
        model_refs = getattr(service, "_model_refs", None)
        configured_device = _normalize_device(
            getattr(service, "_device_str", None)
        )
        model_devices = (
            _model_ref_devices(model_refs) if model_refs is not None else set()
        )

    runtime_loaded = model_refs is not None or configured_device is not None
    observed_devices = set(model_devices)
    if configured_device is not None:
        observed_devices.add(configured_device)
    runtime_device = None
    if len(observed_devices) == 1:
        runtime_device = next(iter(observed_devices))
    elif len(observed_devices) > 1:
        runtime_device = "conflict:" + ",".join(sorted(observed_devices))
    return MarkerRuntimeState(
        package_available=package_available,
        model_cache_ready=cache_ready,
        runtime_loaded=runtime_loaded,
        runtime_device=runtime_device,
    )


def marker_runtime_live() -> tuple[bool, str | None]:
    """Đọc lại `(runtime_loaded, runtime_device)` **tại thời điểm gọi**.

    `marker_runtime_state()` chỉ chạy trong `preflight()`, và mọi preflight đều xong
    trước tài liệu đầu tiên — nên `_model_refs`/`_device_str` chắc chắn còn `None` lúc
    đó. Dùng ảnh chụp ấy cho 204 dòng fingerprint thì cột `marker_runtime_device` luôn
    `null` kể cả khi Marker đã nạp model và đang chạy trên thiết bị khác CPU: một
    trường mang tên "runtime" nhưng không bao giờ quan sát runtime. Ở đây chỉ đọc hai
    thuộc tính module — không nạp model, không đụng vào cache.
    """
    try:
        with _be_read_only():
            service = _load_marker_service()
            model_refs = getattr(service, "_model_refs", None)
            device = _normalize_device(getattr(service, "_device_str", None))
    except BaseException:  # noqa: BLE001 - probe không được phép làm hỏng lượt chạy
        return (False, None)
    devices = set(_model_ref_devices(model_refs)) if model_refs is not None else set()
    if device is not None:
        devices.add(device)
    if len(devices) == 1:
        return (True, next(iter(devices)))
    if len(devices) > 1:
        return (True, "conflict:" + ",".join(sorted(devices)))
    return (model_refs is not None, None)


def marker_san_sang() -> bool:
    """Backward-compatible availability predicate derived from separate probes."""
    return marker_runtime_state().marker_available


def _kiem_pipeline_module(module: Any) -> None:
    """Reject module globals frozen from an earlier unsafe BE import."""
    api_key_present = bool((getattr(module, "_api_key", "") or "").strip()) or bool(
        (getattr(module, "_groq_api_key", "") or "").strip()
    )
    remote_url_present = bool((getattr(module, "_api_url", "") or "").strip()) or bool(
        (getattr(module, "_gdoc_parser_url", "") or "").strip()
    )
    if api_key_present or remote_url_present:
        raise VuotTran(
            "BE parser đã import với config không an toàn: "
            f"api_key_present={api_key_present}, "
            f"remote_url_present={remote_url_present}. Dừng."
        )


def nap_pipeline(*, marker_enabled: bool | None = None) -> Callable[..., dict]:
    """Cưỡng bức env → thêm BE vào ``sys.path`` → import → kiểm config.

    Trả về chính ``extract_text_from_document``. Bốn bước **đúng thứ tự đó**, xem mục 2
    của docstring module.
    """
    _ap_env(marker_enabled=marker_enabled)
    with _be_read_only():
        goc = duong_dan_be()
        if not (
            goc / "app" / "services" / "openrouter_document_parser.py"
        ).is_file():
            raise VuotTran(
                f"không thấy pipeline BE ở {goc}. "
                "Đặt SOVEREIGN_BE_PATH trỏ đúng thư mục."
            )
        if str(goc) not in sys.path:
            sys.path.insert(0, str(goc))

        from app.config import get_settings  # noqa: PLC0415

        kiem_config(get_settings, marker_enabled=marker_enabled)

        from app.services import openrouter_document_parser as parser  # noqa: PLC0415

        _kiem_pipeline_module(parser)
        return parser.extract_text_from_document


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _plain(nested) for key, nested in value.items()}
    if isinstance(value, tuple):
        return [_plain(nested) for nested in value]
    return value


def _marker_version() -> str:
    try:
        return package_version("marker-pdf")
    except PackageNotFoundError:
        return "not-installed"
    except BaseException:  # fingerprint must never mask the original adapter failure
        return "unknown"


def _be_git_metadata() -> dict[str, object]:
    """Return only commit/dirty state; never retain the BE path or Git diagnostics."""
    try:
        commit = subprocess.run(
            ["git", "-C", str(duong_dan_be()), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        dirty = subprocess.run(
            [
                "git",
                "-C",
                str(duong_dan_be()),
                "status",
                "--porcelain=v1",
                "--untracked-files=normal",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if commit.returncode != 0 or dirty.returncode != 0:
            return {"commit": "unknown", "dirty": None}
        return {
            "commit": commit.stdout.strip() or "unknown",
            "dirty": bool(dirty.stdout.strip()),
        }
    except BaseException:  # version/fingerprint are diagnostic paths and cannot throw
        return {"commit": "unknown", "dirty": None}


def _sanitize_dem(value: str, exact_secrets: tuple[str, ...]) -> tuple[str, int]:
    """Làm sạch và **đếm** số lần thay khớp-chính-xác.

    Đếm để chỗ gọi có thể nói ra. Thay chuỗi trong `text_md` là can thiệp vào chính
    thứ đang được chấm điểm; im lặng thì điểm tụt mà không có dấu vết nào giải thích.
    """
    sanitized = sanitize_secret_text(value) or ""
    dem = 0
    for secret in sorted(set(exact_secrets), key=len, reverse=True):
        if secret and len(secret) >= _DO_DAI_BI_MAT_TOI_THIEU and secret in sanitized:
            dem += sanitized.count(secret)
            sanitized = sanitized.replace(secret, "<redacted>")
    return sanitized, dem


def _sanitize_runtime_text(value: str, exact_secrets: tuple[str, ...]) -> str:
    return _sanitize_dem(value, exact_secrets)[0]


#: Lỗi *của bench*, không phải của BE — không bọc, không làm sạch. Bọc chúng lại thì
#: `preflight` mất kiểu ngoại lệ mà chỗ gọi đang bắt, và thông điệp chẩn đoán do chính
#: repo này viết (vốn không chứa bí mật) bị thay bằng một lớp vỏ mờ.
_LOI_NOI_BO: tuple[type[BaseException], ...] = (
    ProfileConfigError,
    ProfileEnvironmentError,
    SanitizedPipelineError,
    VuotTran,
)


@contextmanager
def _boc_loi_be(secrets: tuple[str, ...]):
    """Mọi lời gọi chạm BE đều phải nằm trong đây.

    `nap_pipeline()` → `from app.config import get_settings` → `get_settings()`: một
    `ValidationError` của pydantic in lại **giá trị đầu vào**, và trước fix này nó đi
    thẳng ra `error` + `config_fingerprint.traceback` chỉ qua regex chung — đúng loại
    bí mật đục mà regex không nhìn thấy.
    """
    try:
        yield
    except _LOI_NOI_BO:
        raise
    except Exception as exc:  # noqa: BLE001 - biên duy nhất giữa BE và artifact
        raise SanitizedPipelineError(
            _sanitize_runtime_text(f"{type(exc).__name__}: {exc}", secrets),
            classify_exception(exc),
        ) from None


def _canonical_response_bytes(success: bool, full_text: str) -> bytes:
    return json.dumps(
        {"success": success, "fullText": full_text},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


class SovereignAdapter(Adapter):
    """Baseline: pipeline BE hiện tại, chạy ngoài container.

    Trần chi phí kiểm ở **biên tài liệu**, không cắt ngang được một lời gọi đang chạy —
    ``extract_text_from_document`` là đồng bộ, không có tham số timeout, và bọc nó bằng
    thread thì thread Marker vẫn ngốn CPU sau khi bị bỏ rơi. Nói thẳng ra ở đây còn hơn
    để người đọc tưởng trần là cứng tuyệt đối: một tài liệu **có thể** vượt
    ``tran_giay_moi_tai_lieu``, nhưng nó là tài liệu cuối cùng được chạy.
    """

    name: ClassVar[str] = "sovereign"
    capabilities: ClassVar[frozenset[Capability]] = frozenset({Capability.TEXT_MD})
    # KHÔNG khai gì thêm: pipeline trả đúng {success, fullText}. Không bbox (BLOCK_BBOX),
    # không ảnh (IMAGE_*) — ảnh Marker bị vứt và ảnh DOCX bị lột, đó chính là điểm mất
    # dữ liệu #1 và #2 của §2. Không TABLE_HTML: nhánh PDF là `page.get_text()` thô,
    # không phát ra markup bảng nào cả.

    def __init__(
        self,
        *,
        tran_giay_moi_tai_lieu: float | None = None,
        tran_giay_tong: float | None = None,
        tran_so_tai_lieu: int | None = None,
        identity: SovereignIdentity = LEGACY_IDENTITY,
    ) -> None:
        # Nâng trần phải là **hành động có chủ ý**, nên nó đi qua env chứ không phải một
        # cờ dòng lệnh lẫn giữa mười cờ khác. Mặc định cố tình thấp hơn bộ mẫu olmocr
        # (1403 tài liệu): người chạy phải tự khai rằng mình biết mình đang mở cái gì.
        tran_giay_moi_tai_lieu = _tu_env(
            "SOVEREIGN_TRAN_GIAY_MOI_TAI_LIEU", tran_giay_moi_tai_lieu, 300.0, float
        )
        tran_giay_tong = _tu_env("SOVEREIGN_TRAN_GIAY_TONG", tran_giay_tong, 7200.0, float)
        tran_so_tai_lieu = _tu_env("SOVEREIGN_TRAN_SO_TAI_LIEU", tran_so_tai_lieu, 250, int)
        if min(tran_giay_moi_tai_lieu, tran_giay_tong) <= 0 or tran_so_tai_lieu <= 0:
            raise ValueError("trần phải dương")
        self.identity = identity
        self.name = identity.name
        self.engine_family = identity.engine_family
        self.profile = identity.profile
        self.tran_giay_moi_tai_lieu = tran_giay_moi_tai_lieu
        self.tran_giay_tong = tran_giay_tong
        self.tran_so_tai_lieu = tran_so_tai_lieu
        self._da_chay = 0
        self._tong_giay = 0.0
        self._pipeline: Callable[..., dict] | None = None
        self._config: dict[str, object] | None = None
        expected = identity.environment.get("marker_available")
        self._marker_expected = expected if isinstance(expected, bool) else None
        self._marker_state = UNKNOWN_MARKER_STATE
        self._preflight_complete = identity.profile == "legacy"
        self._hardware: Literal["cpu"] = "cpu"
        self._hardware_verified = False
        self._text_redactions = 0
        thu_thap_bi_mat()  # nạp sớm, trước khi `_ap_env` kịp xoá trắng env

    @property
    def _sensitive_values(self) -> tuple[str, ...]:
        """Đọc lại mỗi lần dùng, không đóng băng lúc `__init__`.

        Đóng băng làm bộ giá trị phụ thuộc thứ tự dựng adapter; đọc lại thì profile
        thứ hai vẫn thấy đủ những gì profile thứ nhất đã thấy.
        """
        return thu_thap_bi_mat()

    @classmethod
    def from_profile(cls, profile: EngineProfile) -> "SovereignAdapter":
        if profile.adapter != "sovereign" or profile.family != "sovereign":
            raise ProfileConfigError(
                f"SovereignAdapter không nhận profile {profile.name!r}/{profile.family!r}"
            )
        expected_environment = _PROFILE_ENVIRONMENTS.get(profile.name)
        expected_profile = {
            "sovereign_default": "default",
            "sovereign_scan": "scan",
        }.get(profile.name)
        if expected_profile is None or profile.profile != expected_profile:
            raise ProfileConfigError(f"profile Sovereign không hỗ trợ: {profile.name!r}")
        if _plain(profile.config) != _PROFILE_CONFIG:
            raise ProfileConfigError(
                f"{profile.name}: config không khớp catalog Sovereign đã khóa"
            )
        if _plain(profile.environment) != expected_environment:
            raise ProfileConfigError(
                f"{profile.name}: environment không khớp catalog Sovereign đã khóa"
            )
        return cls(
            identity=SovereignIdentity(
                name=profile.name,
                engine_family="sovereign",
                profile=profile.profile,
                config=profile.config,
                environment=profile.environment,
                profile_config_sha256=profile.fingerprint,
            )
        )

    # -- config -----------------------------------------------------------

    @property
    def _marker_enabled(self) -> bool | None:
        if self.profile == "scan":
            return True
        if self.profile == "default":
            return False
        return None

    def preflight(self) -> dict[str, object]:
        """Bind one profile to a matching, local-only BE runtime before execution."""
        _ap_env(marker_enabled=self._marker_enabled)
        state = marker_runtime_state()
        self._marker_state = state
        self._validate_marker_runtime(state)

        with _boc_loi_be(self._sensitive_values):
            pipeline = nap_pipeline(marker_enabled=self._marker_enabled)
            with _be_read_only():
                from app.config import get_settings  # noqa: PLC0415

                self._config = kiem_config(
                    get_settings, marker_enabled=self._marker_enabled
                )
        self._pipeline = pipeline
        self._preflight_complete = True
        return self.config_fingerprint()

    def _validate_marker_runtime(self, state: MarkerRuntimeState) -> None:
        marker_available = bool(
            state.package_available and state.model_cache_ready
        )
        if (
            self._marker_expected is not None
            and marker_available is not self._marker_expected
        ):
            raise ProfileEnvironmentError(
                f"{self.name}: marker_available={marker_available}, "
                f"profile requires {self._marker_expected}"
            )

        runtime_device = _normalize_device(state.runtime_device)
        if runtime_device is not None and not runtime_device.startswith("cpu"):
            raise ProfileEnvironmentError(
                f"{self.name}: cached Marker runtime_device={runtime_device!r}; "
                "CPU profile requires an already-loaded CPU runtime"
            )
        if state.runtime_loaded and runtime_device is None:
            raise ProfileEnvironmentError(
                f"{self.name}: Marker runtime_loaded=True but device is unverified"
            )
        if self.profile == "default" and state.runtime_loaded:
            raise ProfileEnvironmentError(
                f"{self.name}: default profile rejects Marker runtime_loaded=True"
            )

    def configure_hardware(self, hardware: str) -> str:
        if hardware not in {"cpu", "gpu"}:
            raise ValueError("Sovereign hardware phải là 'cpu' hoặc 'gpu'")
        if hardware == "gpu":
            raise RuntimeError(
                "Sovereign GPU/CUDA bị từ chối: BE Marker path không có handshake "
                "enforce/verify CUDA đáng tin cậy"
            )
        self._hardware_verified = False
        self.preflight()
        self._hardware = "cpu"
        self._hardware_verified = True
        return "cpu"

    def _nap(self) -> Callable[..., dict]:
        if self.profile != "legacy" and not self._hardware_verified:
            raise ProfileEnvironmentError(
                f"{self.name}: phải configure_hardware('cpu') trước document execution"
            )
        if self._pipeline is None:
            with _boc_loi_be(self._sensitive_values):
                pipeline = nap_pipeline(marker_enabled=self._marker_enabled)
                with _be_read_only():
                    from app.config import get_settings  # noqa: PLC0415

                    self._config = kiem_config(
                        get_settings, marker_enabled=self._marker_enabled
                    )
            self._pipeline = pipeline
        return self._pipeline

    def version(self) -> str:
        """Không có package version cho pipeline BE — dùng full Git commit."""
        return str(_be_git_metadata()["commit"])

    def config_fingerprint(self) -> dict[str, object]:
        """AC-03 — **bắt buộc không rỗng**.

        Người đọc bảng điểm phải biết baseline được đo ở chế độ nào: cờ nào bật, có khoá
        API hay không, Marker có sẵn hay không. Thiếu ``marker_available`` thì hai lượt
        chạy chênh nhau hàng chục lần thời gian trông như cùng một thứ.
        """
        marker_state = self._marker_state
        co_marker = marker_state.marker_available
        runtime_loaded, runtime_device = marker_runtime_live()
        git = _be_git_metadata()
        safe_config = {
            **_plain(self.identity.config),
            **(self._config or {}),
        }
        return {
            **safe_config,
            "mode": "full" if co_marker else "light",
            "marker_available": co_marker,
            "marker_package_available": marker_state.package_available,
            "marker_model_cache_ready": marker_state.model_cache_ready,
            "marker_model_cache": marker_state.model_cache_ready,
            # Đọc lại lúc chấm, không dùng ảnh chụp preflight — xem `marker_runtime_live`.
            "marker_runtime_loaded": runtime_loaded,
            "marker_runtime_device": runtime_device,
            "marker_preflight_runtime_loaded": marker_state.runtime_loaded,
            "marker_preflight_runtime_device": marker_state.runtime_device,
            "marker_version": _marker_version(),
            "be_commit": git["commit"],
            "be_dirty": git["dirty"],
            "python": sys.version.split()[0],
            "profile_config_sha256": self.identity.profile_config_sha256,
            "hardware": "cpu",
            "device": "cpu" if self._hardware_verified else "unverified",
            "hardware_evidence_version": 1,
            "device_evidence": (
                "be-settings-ocr-device-cpu"
                if self._hardware_verified
                else "none"
            ),
            # Bao nhiêu lần chuỗi bí mật bị thay **trong chính văn bản được chấm điểm**.
            # Khác 0 nghĩa là điểm accuracy của tài liệu đó đã bị chính lớp bảo vệ này
            # làm giảm; im lặng thì nó trông y hệt một lần OCR kém.
            "scored_text_redactions": self._text_redactions,
            "tran_giay_moi_tai_lieu": self.tran_giay_moi_tai_lieu,
            "tran_giay_tong": self.tran_giay_tong,
            "tran_so_tai_lieu": self.tran_so_tai_lieu,
        }

    # -- trần -------------------------------------------------------------

    def _kiem_tran_truoc(self) -> None:
        if self._da_chay >= self.tran_so_tai_lieu:
            raise VuotTran(
                f"trần số tài liệu: đã chạy {self._da_chay}/{self.tran_so_tai_lieu}"
            )
        if self._tong_giay >= self.tran_giay_tong:
            raise VuotTran(
                f"trần tổng thời gian: {self._tong_giay:.1f}s/{self.tran_giay_tong:.1f}s"
            )

    def _kiem_tran_sau(self, giay: float, doc_id: str) -> None:
        if giay > self.tran_giay_moi_tai_lieu:
            raise VuotTran(
                f"trần thời gian một tài liệu: {doc_id} mất {giay:.1f}s "
                f"> {self.tran_giay_moi_tai_lieu:.1f}s (Marker trên CPU ~54s/trang)"
            )

    # -- chạy -------------------------------------------------------------

    def run(self, doc_path: Path) -> OcrResult:
        self._text_redactions = 0  # đếm lại từng tài liệu, không cộng dồn
        self._kiem_tran_truoc()
        pipeline = self._nap()

        duoi = doc_path.suffix.lstrip(".").lower() or _DUOI_MAC_DINH
        du_lieu = base64.b64encode(doc_path.read_bytes()).decode("ascii")

        t0 = time.perf_counter()
        try:
            with _be_read_only():
                ket = pipeline(du_lieu, duoi)
        except Exception as exc:
            safe_error = _sanitize_runtime_text(
                f"{type(exc).__name__}: {exc}", self._sensitive_values
            )
            raise SanitizedPipelineError(safe_error, classify_exception(exc)) from None
        giay = time.perf_counter() - t0

        self._da_chay += 1
        self._tong_giay += giay
        self._kiem_tran_sau(giay, doc_path.stem)

        van_ban = ket.get("fullText") or ""
        if not isinstance(van_ban, str):
            van_ban = str(van_ban)
        van_ban, so_lan_bit = _sanitize_dem(van_ban, self._sensitive_values)
        self._text_redactions = so_lan_bit
        thanh_cong = bool(ket.get("success"))
        raw_bytes = _canonical_response_bytes(thanh_cong, van_ban)
        error = None
        if not thanh_cong:
            error = _sanitize_runtime_text(
                f"{ket.get('error_code') or 'ocr.failed'}: "
                f"{ket.get('message') or 'không rõ'}",
                self._sensitive_values,
            )
        return OcrResult(
            engine=self.name,
            engine_family=self.engine_family,
            profile=self.profile,
            engine_version=self.version(),
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            # Thất bại của pipeline là *dữ liệu* của FailRate, không phải sự cố của bench:
            # `success=False` có `error_code` riêng (ocr.markerFailed, ocr.pdfEncrypted…),
            # giữ nguyên mã đó chứ không gộp thành "lỗi".
            text_md=van_ban if thanh_cong else None,
            raw_artifacts=(
                RawArtifact("sovereign.json", "application/json", raw_bytes),
            ),
            seconds=giay,
            failed=not thanh_cong,
            error=error,
            failure_kind=None if thanh_cong else FailureKind.ENGINE_ERROR,
            config_fingerprint=self.config_fingerprint(),
        )
