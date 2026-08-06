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

import os
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

from ocr_bench.adapters.sovereign import (
    ENV_CUONG_BUC,
    SovereignAdapter,
    VuotTran,
    duong_dan_be,
    kiem_config,
)
from ocr_bench.types import Capability

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


def _settings(**kw):
    """Giả ``get_settings`` có ``@lru_cache`` y như bản thật (``config.py:319-321``)."""
    mac_dinh = {
        "ocr_use_local_first": False,
        "ocr_use_vision_api": False,
        "openrouter_api_key": "",
        "gdoc_parser_url": "",
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
            gdoc_parser_url="",
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
    for truong in ("mode", "marker_available", "env_forced", "be_path", "python"):
        assert truong in fp, truong
    assert fp["mode"] in ("light", "full")
    assert isinstance(fp["marker_available"], bool)


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
