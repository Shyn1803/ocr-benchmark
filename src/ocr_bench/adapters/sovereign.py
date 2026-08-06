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
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable, ClassVar

from ocr_bench.adapters.base import Adapter
from ocr_bench.types import Capability, OcrResult

__all__ = [
    "SovereignAdapter",
    "VuotTran",
    "ENV_CUONG_BUC",
    "duong_dan_be",
    "nap_pipeline",
    "kiem_config",
    "marker_san_sang",
]


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
    "GROQ_API_KEY": "",
    "GDOC_PARSER_URL": "",
}

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


def duong_dan_be() -> Path:
    """Thư mục gốc BE. Ghi đè bằng ``SOVEREIGN_BE_PATH`` nếu cây thư mục khác."""
    if thu_cong := os.environ.get("SOVEREIGN_BE_PATH"):
        return Path(thu_cong).resolve()
    # ocr-bench/src/ocr_bench/adapters/sovereign.py → lên 5 mức là sovereign/
    return (
        Path(__file__).resolve().parents[4] / "adminPortal" / "back-end-admin-portal"
    ).resolve()


def _ap_env() -> None:
    """Ghi ``ENV_CUONG_BUC`` vào ``os.environ``. Gọi **trước** mọi import BE."""
    os.environ.update(ENV_CUONG_BUC)


def kiem_config(get_settings: Callable[[], Any]) -> dict[str, object]:
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
    khoa = bool((getattr(s, "openrouter_api_key", "") or "").strip())
    gdoc = (getattr(s, "gdoc_parser_url", "") or "").strip()

    if vision or khoa:
        raise VuotTran(
            "Cưỡng bức env thất bại: "
            f"ocr_use_vision_api={vision}, api_key_present={khoa}. "
            "BE .env bật vision và mang khoá thật — chạy tiếp là gọi API tính tiền. Dừng."
        )
    return {
        "ocr_use_local_first": local_first,
        "ocr_use_vision_api": vision,
        # CHỈ boolean. Giá trị khoá không bao giờ được ghi ra: fingerprint đi vào
        # `prediction/` và `prediction/` được commit.
        "api_key_present": khoa,
        "gdoc_parser_url": gdoc,
    }


def marker_san_sang() -> bool:
    """Cache model Surya có sẵn không — phân biệt chế độ ``light`` và ``full``.

    Không được ném: ``Adapter.execute()`` gọi ``config_fingerprint()`` trong cả nhánh bắt
    lỗi, ném ở đó thì lỗi gốc bị nuốt (bài học A5 lỗi #3).
    """
    try:
        from app.services.marker_ocr_service import _surya_models_cached  # noqa: PLC0415

        return bool(_surya_models_cached())
    except BaseException:  # noqa: BLE001 — cố ý: hàm này tuyệt đối không được ném
        return False


def nap_pipeline() -> Callable[..., dict]:
    """Cưỡng bức env → thêm BE vào ``sys.path`` → import → kiểm config.

    Trả về chính ``extract_text_from_document``. Bốn bước **đúng thứ tự đó**, xem mục 2
    của docstring module.
    """
    _ap_env()
    goc = duong_dan_be()
    if not (goc / "app" / "services" / "openrouter_document_parser.py").is_file():
        raise VuotTran(
            f"không thấy pipeline BE ở {goc}. Đặt SOVEREIGN_BE_PATH trỏ đúng thư mục."
        )
    if str(goc) not in sys.path:
        sys.path.insert(0, str(goc))

    from app.config import get_settings  # noqa: PLC0415

    kiem_config(get_settings)

    from app.services.openrouter_document_parser import (  # noqa: PLC0415
        extract_text_from_document,
    )

    return extract_text_from_document


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
        self.tran_giay_moi_tai_lieu = tran_giay_moi_tai_lieu
        self.tran_giay_tong = tran_giay_tong
        self.tran_so_tai_lieu = tran_so_tai_lieu
        self._da_chay = 0
        self._tong_giay = 0.0
        self._pipeline: Callable[..., dict] | None = None
        self._config: dict[str, object] | None = None

    # -- config -----------------------------------------------------------

    def _nap(self) -> Callable[..., dict]:
        if self._pipeline is None:
            self._pipeline = nap_pipeline()
            from app.config import get_settings  # noqa: PLC0415

            self._config = kiem_config(get_settings)
        return self._pipeline

    def version(self) -> str:
        """Không có số phiên bản nào cho "pipeline BE" — dùng commit của repo BE."""
        import subprocess  # noqa: PLC0415

        try:
            r = subprocess.run(
                ["git", "-C", str(duong_dan_be()), "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return r.stdout.strip() or "unknown" if r.returncode == 0 else "unknown"
        except BaseException:  # noqa: BLE001 — version() không được ném, xem marker_san_sang
            return "unknown"

    def config_fingerprint(self) -> dict[str, object]:
        """AC-03 — **bắt buộc không rỗng**.

        Người đọc bảng điểm phải biết baseline được đo ở chế độ nào: cờ nào bật, có khoá
        API hay không, Marker có sẵn hay không. Thiếu ``marker_available`` thì hai lượt
        chạy chênh nhau hàng chục lần thời gian trông như cùng một thứ.
        """
        co_marker = marker_san_sang()
        return {
            **(self._config or {}),
            "mode": "full" if co_marker else "light",
            "marker_available": co_marker,
            "env_forced": dict(ENV_CUONG_BUC),
            "be_path": str(duong_dan_be()),
            "python": sys.version.split()[0],
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
        self._kiem_tran_truoc()
        pipeline = self._nap()

        duoi = doc_path.suffix.lstrip(".").lower() or _DUOI_MAC_DINH
        du_lieu = base64.b64encode(doc_path.read_bytes()).decode("ascii")

        t0 = time.perf_counter()
        ket = pipeline(du_lieu, duoi)
        giay = time.perf_counter() - t0

        self._da_chay += 1
        self._tong_giay += giay
        self._kiem_tran_sau(giay, doc_path.stem)

        van_ban = ket.get("fullText") or ""
        thanh_cong = bool(ket.get("success"))
        return OcrResult(
            engine=self.name,
            engine_version=self.version(),
            doc_id=doc_path.stem,
            capabilities=self.capabilities,
            # Thất bại của pipeline là *dữ liệu* của FailRate, không phải sự cố của bench:
            # `success=False` có `error_code` riêng (ocr.markerFailed, ocr.pdfEncrypted…),
            # giữ nguyên mã đó chứ không gộp thành "lỗi".
            text_md=van_ban if thanh_cong else None,
            seconds=giay,
            failed=not thanh_cong,
            error=None
            if thanh_cong
            else f"{ket.get('error_code') or 'ocr.failed'}: {ket.get('message') or 'không rõ'}",
            config_fingerprint=self.config_fingerprint(),
        )
