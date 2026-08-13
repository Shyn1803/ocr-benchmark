"""Test bộ nối OpenDataLoader — A5 (TASK-076).

Chia làm hai nửa, cùng lối A4:

* **Không cần engine** — đi cây, ánh xạ loại, quy đổi toạ độ, số trang, bảng, ảnh.
  Chạy trên dict giả nên xanh trên máy trắng (không Java, không `opendataloader-pdf`).
* **Cần engine** (`needs_odl`) — chạy thật. Bài học đắt nhất của A4: dữ liệu giả
  được dựng để khớp giả định của chính mình, nên nó **không bao giờ** bắt được lớp
  lỗi "trường có giá trị, đúng kiểu, và sai". Hai lỗi của A5 —
  `setup_java.tim_java()` không thấy JRE lồng hai tầng, và `config_fingerprint()`
  ném khiến `execute()` nuốt mất lỗi gốc — đều chỉ lộ ra khi chạy thật.
"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from ocr_bench.adapters.base import AdapterOutputError
from ocr_bench.adapters.opendataloader import (
    BLOCK_TYPE_MAP,
    OpenDataLoaderAdapter,
    bang_sang_html,
    build_result,
    chu_cua_node,
    kich_thuoc_trang,
    map_block_type,
    node_khoi,
    node_phang,
)
from ocr_bench.profiles import EngineProfile, ProfileConfigError, load_profile_catalog
from ocr_bench.types import BlockType, Capability, FailureKind

ROOT = Path(__file__).resolve().parents[1]
CATALOG = load_profile_catalog(ROOT / "configs" / "profiles.json")
HYBRID_VERSIONS = {
    "docling": "2.91.0",
    "easyocr": "1.7.2",
    "fastapi": "0.136.1",
    "opendataloader-pdf": "2.5.0",
    "packaging": "25.0",
    "pypdf": "5.0.0",
    "psutil": "7.0.0",
    "python-multipart": "0.0.28",
    "uvicorn": "0.46.0",
}


class _HybridProcess:
    def __init__(self, pid, *, create_time=1234.5, children=(), listening=False, cmdline=()):
        self.pid = pid
        self._create_time = create_time
        self._children = list(children)
        self._listening = listening
        self._cmdline = list(cmdline)

    def create_time(self):
        return self._create_time

    def children(self, recursive=False):
        assert recursive is True
        return list(self._children)

    def net_connections(self, kind="inet"):
        assert kind == "inet"
        if not self._listening:
            return []
        return [SimpleNamespace(laddr=("127.0.0.1", 5002), status="LISTEN")]

    def is_running(self):
        return True

    def cmdline(self):
        return list(self._cmdline)


def _hybrid_runtime(
    monkeypatch,
    module,
    tmp_path,
    *,
    payload_changes=None,
    process=None,
    pid=4242,
    use_env=True,
):
    child = _HybridProcess(pid + 1, listening=True)
    root = process or _HybridProcess(pid, children=[child])
    processes = {root.pid: root, child.pid: child}
    fake_psutil = SimpleNamespace(
        CONN_LISTEN="LISTEN",
        Process=lambda pid: processes[pid],
    )
    payload = {
        "argv": [
            str((tmp_path / "python.exe").resolve()),
            "-m",
            "opendataloader_pdf.hybrid_server",
            "--host",
            "127.0.0.1",
            "--port",
            "5002",
            "--force-ocr",
            "--ocr-engine",
            "easyocr",
            "--ocr-lang",
            "vi,en",
        ],
        "config": {
            "device": "cpu",
            "device_enforcement": {"CUDA_VISIBLE_DEVICES": ""},
            "device_enforcement_method": "CUDA_VISIBLE_DEVICES-empty-before-spawn",
            "force_ocr": True,
            "health_url": "http://127.0.0.1:5002/health",
            "host": "127.0.0.1",
            "jit_enforcement": {"TORCHDYNAMO_DISABLE": "1"},
            "jit_enforcement_method": "TORCHDYNAMO_DISABLE-before-spawn",
            "ocr_engine": "easyocr",
            "ocr_languages": ["vi", "en"],
            "port": 5002,
        },
        "health": {"status": "ok"},
        "host": "127.0.0.1",
        "launcher_version": 1,
        "listener_pids": [pid + 1],
        "manifest_schema_version": 1,
        "pid": pid,
        "port": 5002,
        "process_create_time": 1234.5,
        "url": "http://127.0.0.1:5002",
        "versions": dict(HYBRID_VERSIONS),
    }
    root._cmdline = list(payload["argv"])
    payload["run_id"] = hashlib.sha256(
        (
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
    ).hexdigest()
    if payload_changes:
        payload.update(payload_changes)
    manifest = tmp_path / "odl-hybrid-manifest.json"
    manifest.write_bytes(
        (
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
    )
    if use_env:
        monkeypatch.setenv(module.HYBRID_MANIFEST_ENV, str(manifest))
    else:
        monkeypatch.delenv(module.HYBRID_MANIFEST_ENV, raising=False)
        monkeypatch.setattr(module, "DEFAULT_HYBRID_MANIFEST_PATH", manifest)
    monkeypatch.setattr(module, "_load_psutil", lambda: fake_psutil)
    monkeypatch.setattr(
        module, "_health_payload", lambda *_args, **_kwargs: {"status": "ok"}
    )
    return manifest

needs_odl = pytest.mark.skipif(
    __import__("importlib.util", fromlist=["util"]).find_spec("opendataloader_pdf")
    is None,
    reason="cần extra `opendataloader` + JRE (scripts/setup_java.py)",
)


# --------------------------------------------------------------------------
# Node giả — đúng hình dạng đo được từ 24 tài liệu thật
# --------------------------------------------------------------------------


def doan(chu="xin chào", trang=1, box=(10.0, 700.0, 110.0, 720.0), **them):
    return {
        "type": "paragraph",
        "pdfua_tag": "P",
        "page number": trang,
        "bounding box": list(box),
        "content": chu,
        **them,
    }


def tai_lieu(*kids, so_trang=1):
    return {"file name": "t.pdf", "number of pages": so_trang, "kids": list(kids)}


def dung_ket_qua(doc, trang=None, anh_bytes=None):
    return build_result(
        engine_version="2.5.0",
        doc_id="tai-lieu",
        capabilities=OpenDataLoaderAdapter.capabilities,
        doc=doc,
        markdown="# Tiêu đề",
        trang=trang or [(595.0, 842.0)],
        anh_bytes=anh_bytes or {},
        config_fingerprint={"opendataloader_version": "2.5.0"},
    )


# --------------------------------------------------------------------------
# AC-03 — khai báo & đăng ký
# --------------------------------------------------------------------------


def test_khai_cap_tieu_de_nhung_khong_khai_cay_muc():
    """Hai chuyện khác nhau, và ranh giới giữa chúng là lý do `Capability` tách
    `HEADING_LEVEL` khỏi `SECTION_HIERARCHY` (B4/TASK-082).

    * **Cấp thì khai**: node `heading` mang sẵn `heading level` — dữ liệu engine tự
      nói, không phải bench suy diễn.
    * **Cây thì không**: JSON phẳng, không node nào trỏ về mục cha. Suy cây từ thứ
      tự đọc là đoán, mà A5 cấm đoán.
    """
    assert OpenDataLoaderAdapter.capabilities == frozenset(
        {
            Capability.TEXT_MD,
            Capability.BLOCK_BBOX,
            Capability.IMAGE_BBOX,
            Capability.IMAGE_BYTES,
            Capability.TABLE_HTML,
            Capability.HEADING_LEVEL,
        }
    )
    assert Capability.SECTION_HIERARCHY not in OpenDataLoaderAdapter.capabilities


def test_dang_ky_san_trong_registry():
    from ocr_bench import registry

    assert registry.get_adapter("opendataloader") is OpenDataLoaderAdapter


def test_module_khong_import_engine_o_dau_file():
    """Kiểm bằng AST. `opendataloader-pdf` và `pypdf` đều là extra — import ở đầu
    module thì `import ocr_bench` trên máy trắng nổ và **cả registry rụng theo**."""
    cay = ast.parse(
        (ROOT / "src" / "ocr_bench" / "adapters" / "opendataloader.py").read_text(
            "utf-8"
        )
    )
    for nut in cay.body:  # chỉ cấp cao nhất — trong hàm thì được phép
        if isinstance(nut, ast.Import):
            ten = [a.name for a in nut.names]
        elif isinstance(nut, ast.ImportFrom):
            ten = [nut.module or ""]
        else:
            continue
        for t in ten:
            assert not t.startswith(("opendataloader", "pypdf")), (
                f"import {t} ở đầu module — phải đưa vào trong hàm"
            )


# --------------------------------------------------------------------------
# AC-03 — quy đổi toạ độ (theo KẾT QUẢ ĐO, xem docstring module adapter)
# --------------------------------------------------------------------------


def test_toa_do_y_huong_len():
    """Gốc dưới-trái, y hướng LÊN: block sát mép TRÊN phải ra `y0` ≈ 0.

    Đây là chỗ khác Marker. Chép `y_axis="down"` sang thì mọi box lộn ngược theo
    trục hoành — IoU vẫn ra một con số hợp lý, không ai thấy gì sai trên bảng.
    """
    r = dung_ket_qua(
        tai_lieu(doan(box=(0.0, 800.0, 100.0, 842.0))), trang=[(595.0, 842.0)]
    )
    box = r.blocks[0].box
    assert box is not None
    assert box.y0 == pytest.approx(0.0, abs=1e-9)
    assert box.y1 == pytest.approx(42.0 / 842.0, abs=1e-9)


def test_block_sat_mep_duoi_ra_y1_bang_mot():
    r = dung_ket_qua(tai_lieu(doan(box=(0.0, 0.0, 100.0, 42.0))))
    box = r.blocks[0].box
    assert box is not None
    assert box.y1 == pytest.approx(1.0, abs=1e-9)


def test_khong_tru_goc_mediabox_lan_hai():
    """Phép đo 4: engine ĐÃ trừ gốc MediaBox.

    Nên với trang MediaBox `[100 200 695 1042]`, một block engine báo ở `y=800`
    vẫn phải chuẩn hoá theo chiều trang (595×842), **không** trừ thêm 200. Chép
    theo Marker (`page_y0=mb.bottom`) là trừ hai lần.
    """
    r = dung_ket_qua(
        tai_lieu(doan(box=(0.0, 800.0, 100.0, 842.0))), trang=[(595.0, 842.0)]
    )
    box = r.blocks[0].box
    assert box is not None
    assert box.y0 == pytest.approx(0.0, abs=1e-9)


def test_bounding_box_hong_thi_box_rong_chu_khong_no():
    r = dung_ket_qua(tai_lieu(doan() | {"bounding box": [1.0, 2.0]}))
    assert r.blocks[0].box is None


def test_page_sizes_lay_tu_mediabox_truyen_vao():
    """JSON của engine không có kích thước trang — nguồn duy nhất là `pypdf`."""
    r = dung_ket_qua(tai_lieu(doan()), trang=[(595.0, 842.0), (612.0, 792.0)])
    assert r.page_sizes == ((595.0, 842.0), (612.0, 792.0))


# --------------------------------------------------------------------------
# AC-04 — quy ước 1-indexed
# --------------------------------------------------------------------------


@pytest.mark.parametrize("so,mong_doi", [(1, 0), (2, 1), (7, 6)])
def test_so_trang_tru_mot(so, mong_doi):
    """`page number` của engine 1-indexed, bench 0-based."""
    r = dung_ket_qua(
        tai_lieu(doan(trang=so)), trang=[(595.0, 842.0)] * 8
    )
    assert r.blocks[0].box.page == mong_doi


def test_trang_mot_khong_bi_hieu_thanh_trang_hai():
    """Chốt riêng ca 1 trang — ca mà quên trừ 1 thì rụng SẠCH block."""
    r = dung_ket_qua(tai_lieu(doan(trang=1)), trang=[(595.0, 842.0)])
    assert len(r.blocks) == 1
    assert r.blocks[0].box.page == 0
    assert r.error is None


@pytest.mark.parametrize("xau", [0, -1, None, "1", True])
def test_so_trang_hong_thi_bo_block_va_ghi_loi(xau):
    """Không rơi về trang 0: box chuẩn hoá sai còn tệ hơn box thiếu.

    `True` nằm trong danh sách vì `isinstance(True, int)` là đúng trong Python —
    một `page number: true` sẽ lọt qua kiểm kiểu ngây thơ và thành trang 0.
    """
    r = dung_ket_qua(tai_lieu(doan(trang=xau)))
    assert r.blocks == ()
    assert r.error is not None and "page number" in r.error


def test_trang_vuot_so_trang_that_thi_bo():
    r = dung_ket_qua(tai_lieu(doan(trang=9)), trang=[(595.0, 842.0)])
    assert r.blocks == ()
    assert r.error is not None and "1 trang" in r.error


def test_bang_giu_row_column_1_indexed_de_sap_thu_tu():
    """`row number`/`column number` 1-indexed — ở HTML chỉ dùng để sắp thứ tự."""
    bang = {
        "type": "table",
        "page number": 1,
        "bounding box": [0.0, 0.0, 100.0, 100.0],
        "number of rows": 2,
        "number of columns": 2,
        "rows": [
            {
                "type": "table row",
                "row number": 2,
                "cells": [
                    {"type": "table cell", "row number": 2, "column number": 2,
                     "row span": 1, "column span": 1, "is_header": False,
                     "kids": [doan("d2c2")]},
                    {"type": "table cell", "row number": 2, "column number": 1,
                     "row span": 1, "column span": 1, "is_header": False,
                     "kids": [doan("d2c1")]},
                ],
            },
            {
                "type": "table row",
                "row number": 1,
                "cells": [
                    {"type": "table cell", "row number": 1, "column number": 1,
                     "row span": 1, "column span": 1, "is_header": True,
                     "kids": [doan("d1c1")]},
                ],
            },
        ],
    }
    assert bang_sang_html(bang) == (
        "<table><tr><th>d1c1</th></tr>"
        "<tr><td>d2c1</td><td>d2c2</td></tr></table>"
    )


def test_bang_chep_dung_rowspan_colspan():
    """TEDS chấm trên cây HTML — mất span là sai cấu trúc, không chỉ sai chữ."""
    bang = {
        "type": "table",
        "rows": [
            {
                "type": "table row",
                "row number": 1,
                "cells": [
                    {"type": "table cell", "row number": 1, "column number": 1,
                     "row span": 2, "column span": 3, "is_header": False,
                     "kids": [doan("gộp")]},
                ],
            }
        ],
    }
    assert '<td rowspan="2" colspan="3">gộp</td>' in bang_sang_html(bang)


def test_bang_span_bang_mot_thi_khong_ghi_thuoc_tinh():
    bang = {
        "type": "table",
        "rows": [
            {"type": "table row", "row number": 1, "cells": [
                {"type": "table cell", "row number": 1, "column number": 1,
                 "row span": 1, "column span": 1, "is_header": False,
                 "kids": [doan("a")]}]}
        ],
    }
    assert bang_sang_html(bang) == "<table><tr><td>a</td></tr></table>"


def test_bang_thoat_ky_tu_html():
    bang = {
        "type": "table",
        "rows": [
            {"type": "table row", "row number": 1, "cells": [
                {"type": "table cell", "row number": 1, "column number": 1,
                 "row span": 1, "column span": 1, "is_header": False,
                 "kids": [doan("a < b & c")]}]}
        ],
    }
    assert "a &lt; b &amp; c" in bang_sang_html(bang)


# --------------------------------------------------------------------------
# Đi cây — chỗ dễ đếm trùng / đếm thiếu nhất
# --------------------------------------------------------------------------


def _danh_sach(*muc):
    return {
        "type": "list",
        "page number": 1,
        "bounding box": [0.0, 0.0, 100.0, 100.0],
        "number of list items": len(muc),
        "list items": [
            {
                "type": "list item",
                "page number": 1,
                "bounding box": [0.0, float(i * 10), 100.0, float(i * 10 + 9)],
                "kids": [doan(m)],
            }
            for i, m in enumerate(muc)
        ],
    }


def test_list_phat_tung_muc_khong_phat_ca_cum():
    """DocLayNet gắn nhãn từng `List-item`, không gắn nhãn cả cụm danh sách."""
    r = dung_ket_qua(tai_lieu(_danh_sach("một", "hai")))
    assert [b.block_type for b in r.blocks] == [BlockType.LIST, BlockType.LIST]
    assert [b.text for b in r.blocks] == ["một", "hai"]


def test_list_item_khong_phat_them_paragraph_con():
    """Phát cả `list item` lẫn `paragraph` con là nhân đôi vùng — precision tụt
    mà không có dấu hiệu nào."""
    r = dung_ket_qua(tai_lieu(_danh_sach("một")))
    assert len(r.blocks) == 1


def test_text_block_chi_la_khung_gom_di_xuyen_qua():
    khung = {
        "type": "text block",
        "page number": 1,
        "bounding box": [0.0, 0.0, 100.0, 100.0],
        "kids": [doan("a"), doan("b")],
    }
    r = dung_ket_qua(tai_lieu(khung))
    assert [b.text for b in r.blocks] == ["a", "b"]


def test_table_khong_di_xuong_o():
    """Ô đi vào `OcrTable.html`, không thành block riêng."""
    bang = {
        "type": "table", "page number": 1,
        "bounding box": [0.0, 0.0, 100.0, 100.0],
        "number of rows": 1, "number of columns": 1,
        "rows": [{"type": "table row", "row number": 1, "cells": [
            {"type": "table cell", "row number": 1, "column number": 1,
             "row span": 1, "column span": 1, "is_header": False,
             "kids": [doan("ô")]}]}],
    }
    r = dung_ket_qua(tai_lieu(bang))
    assert len(r.blocks) == 1
    assert r.blocks[0].block_type is BlockType.TABLE
    assert len(r.tables) == 1
    assert r.tables[0].n_rows == 1 and r.tables[0].n_cols == 1


def test_node_phang_di_het_moi_khoa_con():
    """`list items`/`rows`/`cells` không phải `kids` — dò thiếu một khoá là mất im
    lặng cả nhánh cây."""
    ds = _danh_sach("một", "hai")
    loai = [n["type"] for n in node_phang(ds)]
    assert loai == ["list", "list item", "paragraph", "list item", "paragraph"]


def test_chu_cua_list_item_lay_tu_paragraph_con():
    """`list item` không có `content` của riêng nó."""
    muc = _danh_sach("nội dung")["list items"][0]
    assert "content" not in muc
    assert chu_cua_node(muc) == "nội dung"


def test_node_khoi_bo_qua_root_khong_co_type():
    doc = tai_lieu(doan("a"))
    assert "type" not in doc
    assert [n["type"] for n in node_khoi(doc)] == ["paragraph"]


# --------------------------------------------------------------------------
# Ánh xạ loại
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "odl,mong_doi",
    [
        ("paragraph", BlockType.TEXT),
        ("heading", BlockType.HEADING),
        ("list item", BlockType.LIST),
        ("image", BlockType.PICTURE),
        ("caption", BlockType.CAPTION),
        ("table", BlockType.TABLE),
    ],
)
def test_anh_xa_loai(odl, mong_doi):
    assert map_block_type(odl) is mong_doi


def test_loai_la_thanh_other_chu_khong_bi_bo():
    """Bản engine mới thêm loại node không được phép làm điểm tụt."""
    assert map_block_type("sơ đồ nhạc") is BlockType.OTHER
    r = dung_ket_qua(tai_lieu(doan() | {"type": "sơ đồ nhạc"}))
    assert len(r.blocks) == 1
    assert r.blocks[0].block_type is BlockType.OTHER


def test_moi_loai_quan_sat_duoc_deu_co_trong_bang():
    """8 `type` đã thấy trên 24 tài liệu thật. `text block` cố ý không nằm trong
    bảng — nó là khung gom, `node_khoi()` đi xuyên qua."""
    da_thay = {
        "paragraph", "heading", "list", "list item",
        "image", "caption", "table", "table cell",
    }
    assert da_thay <= set(BLOCK_TYPE_MAP)


def test_cap_muc_chi_gan_cho_heading():
    tieu_de = {
        "type": "heading", "page number": 1,
        "bounding box": [0.0, 0.0, 10.0, 10.0],
        "content": "Chương", "heading level": 2,
    }
    r = dung_ket_qua(tai_lieu(tieu_de, doan() | {"heading level": 3}))
    assert r.blocks[0].level == 2
    assert r.blocks[1].level is None


def test_cap_muc_khong_phai_so_thi_bo():
    tieu_de = {
        "type": "heading", "page number": 1,
        "bounding box": [0.0, 0.0, 10.0, 10.0],
        "content": "Chương", "heading level": "hai",
    }
    assert dung_ket_qua(tai_lieu(tieu_de)).blocks[0].level is None


# --------------------------------------------------------------------------
# Ảnh
# --------------------------------------------------------------------------


def _anh(nguon="t_images/imageFile1.png"):
    return {
        "type": "image", "pdfua_tag": "Figure", "page number": 1,
        "bounding box": [0.0, 0.0, 100.0, 100.0],
        "alt_source": "missing", "source": nguon,
    }


def test_anh_gan_bytes_theo_source():
    r = dung_ket_qua(
        tai_lieu(_anh()), anh_bytes={"t_images/imageFile1.png": b"\x89PNG..."}
    )
    assert len(r.images) == 1
    assert r.images[0].data == b"\x89PNG..."
    assert r.images[0].source_id == "t_images/imageFile1.png"
    assert r.images[0].box is not None


def test_anh_thieu_file_thi_van_giu_bbox():
    """Mất bytes không được kéo theo mất vùng — B3 chấm vùng, B5 mới cần bytes."""
    r = dung_ket_qua(tai_lieu(_anh()), anh_bytes={})
    assert r.images[0].data is None
    assert r.images[0].box is not None


def test_source_id_luon_la_str():
    """`source_id` đi thẳng vào JSON của `prediction/` — kiểu lạ là đổ cả lượt
    chạy ở tài liệu đầu tiên có ảnh."""
    r = dung_ket_qua(tai_lieu(_anh(nguon=123)))
    assert isinstance(r.images[0].source_id, str)


def test_khong_co_anh_thi_rong():
    assert dung_ket_qua(tai_lieu(doan())).images == ()


# --------------------------------------------------------------------------
# Dấu vân tay cấu hình
# --------------------------------------------------------------------------


def test_van_tay_noi_ra_che_do_bang():
    """`table_method` phải nằm trong vân tay: `default` ra 0 bảng trên bộ mẫu,
    `cluster` ra bảng đủ cấu trúc. Người đọc bảng điểm phải biết đã chạy chế độ nào."""
    a = OpenDataLoaderAdapter()
    assert a.table_method == "cluster"
    vt = a.config_fingerprint()
    assert vt["table_method"] == "cluster"
    assert vt["include_header_footer"] is True
    assert vt["image_format"] == "png"


def test_van_tay_khong_nem_khi_thieu_java(monkeypatch):
    """`Adapter.execute()` gọi `config_fingerprint()` để dựng bản ghi THẤT BẠI.
    Hàm này ném thì lỗi gốc bị nuốt và cả lượt chạy đổ ở tài liệu đầu tiên."""
    import ocr_bench.adapters.opendataloader as m

    def khong_co_java():
        raise RuntimeError("Không tìm thấy java >= 11.")

    monkeypatch.setattr(m, "_java", khong_co_java)
    vt = m.OpenDataLoaderAdapter().config_fingerprint()
    assert "không tìm thấy" in vt["java"]
    assert vt["table_method"] == "cluster"


def test_van_tay_khong_nem_khi_chua_cai_extra():
    """Cùng bẫy, nguồn khác: `importlib.metadata.version()` ném khi extra chưa cài.

    Bắt được là nhờ chạy test trong `.venv` sạch — venv có engine thì test này
    xanh dù `_odl_version()` vẫn ném.
    """
    vt = OpenDataLoaderAdapter().config_fingerprint()
    assert isinstance(vt["opendataloader_version"], str)


def test_opendataloader_profiles_bind_exact_identity_and_config():
    default = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_default"])
    scan = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])

    assert (default.name, default.engine_family, default.profile) == (
        "opendataloader_default", "opendataloader", "default"
    )
    assert (scan.name, scan.engine_family, scan.profile) == (
        "opendataloader_scan", "opendataloader", "scan"
    )
    assert default.table_method == "cluster"
    assert default.reading_order == "xycut"
    assert scan.hybrid == "docling-fast"
    assert scan.hybrid_mode == "full"
    assert scan.hybrid_fallback is False
    for adapter, source in ((default, CATALOG["opendataloader_default"]), (scan, CATALOG["opendataloader_scan"])):
        fingerprint = adapter.config_fingerprint()
        assert fingerprint["profile_config_sha256"] == source.fingerprint
        assert fingerprint["hardware"] == "cpu"
        assert type(fingerprint["hardware_evidence_version"]) is int
        assert fingerprint["hardware_evidence_version"] == 1
    assert default.config_fingerprint()["device"] == "cpu"
    assert scan.config_fingerprint()["device"] == "unverified"
    scan_fingerprint = scan.config_fingerprint()
    assert "table_method" not in scan_fingerprint
    assert "reading_order" not in scan_fingerprint


def test_opendataloader_rejects_changed_hybrid_environment():
    source = CATALOG["opendataloader_scan"]
    changed = EngineProfile(
        name=source.name,
        family=source.family,
        profile=source.profile,
        adapter=source.adapter,
        config=source.config,
        environment={"hybrid_server": {"host": "0.0.0.0", "port": 5002}},
    )
    with pytest.raises(ProfileConfigError, match="environment"):
        OpenDataLoaderAdapter.from_profile(changed)


def test_opendataloader_gpu_fails_when_runtime_cannot_prove_device():
    adapter = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])
    with pytest.raises(RuntimeError, match="GPU.*verify|verify.*GPU"):
        adapter.configure_hardware("gpu")


def test_opendataloader_scan_requires_manifest_for_cpu_configuration(monkeypatch, tmp_path):
    import ocr_bench.adapters.opendataloader as module

    monkeypatch.delenv(module.HYBRID_MANIFEST_ENV, raising=False)
    monkeypatch.setattr(
        module, "DEFAULT_HYBRID_MANIFEST_PATH", tmp_path / "missing.json"
    )
    adapter = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])

    with pytest.raises(RuntimeError, match="manifest is missing"):
        adapter.configure_hardware("cpu")
    assert adapter.config_fingerprint()["device"] == "unverified"


def test_opendataloader_scan_fingerprint_uses_validated_launcher_evidence(
    monkeypatch, tmp_path
):
    import ocr_bench.adapters.opendataloader as module

    manifest = _hybrid_runtime(monkeypatch, module, tmp_path)
    adapter = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])

    assert adapter.configure_hardware("cpu") == "cpu"
    fingerprint = adapter.config_fingerprint()
    assert fingerprint["device"] == "cpu"
    assert fingerprint["hybrid_server"]["force_ocr"] is True
    assert fingerprint["hybrid_server"]["ocr_engine"] == "easyocr"
    assert fingerprint["hybrid_server"]["ocr_languages"] == ["vi", "en"]
    assert fingerprint["cpu_enforcement"] == {"CUDA_VISIBLE_DEVICES": ""}
    assert fingerprint["cpu_enforcement_method"] == (
        "CUDA_VISIBLE_DEVICES-empty-before-spawn"
    )
    assert fingerprint["opendataloader_version"] == "2.5.0"
    assert fingerprint["docling_version"] == "2.91.0"
    assert fingerprint["easyocr_version"] == "1.7.2"
    assert fingerprint["pypdf_version"] == "5.0.0"
    assert fingerprint["hybrid_dependency_versions"] == HYBRID_VERSIONS
    assert fingerprint["hybrid_server_versions"] == {
        "fastapi": "0.136.1",
        "python-multipart": "0.0.28",
        "uvicorn": "0.46.0",
    }
    assert fingerprint["hybrid_manifest_run_id"] == json.loads(
        manifest.read_text(encoding="utf-8")
    )["run_id"]
    assert fingerprint["hybrid_manifest_sha256"] == hashlib.sha256(
        manifest.read_bytes()
    ).hexdigest()
    assert fingerprint["device_evidence"] == "owned-hybrid-launcher-manifest"


@pytest.mark.parametrize(
    ("payload_changes", "process", "message"),
    [
        ({"config": {"force_ocr": False}}, None, "config"),
        ({"process_create_time": 1.0}, None, "create_time"),
        ({"listener_pids": [9999]}, None, "listener"),
        ({"run_id": "a" * 64}, None, "run_id"),
    ],
)
def test_opendataloader_scan_rejects_tampered_or_stale_manifest(
    monkeypatch, tmp_path, payload_changes, process, message
):
    import ocr_bench.adapters.opendataloader as module

    _hybrid_runtime(
        monkeypatch,
        module,
        tmp_path,
        payload_changes=payload_changes,
        process=process,
    )
    adapter = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])

    with pytest.raises(RuntimeError, match=message):
        adapter.configure_hardware("cpu")


def test_odl_scan_calls_hybrid_full_without_fallback(monkeypatch, tmp_path):
    import ocr_bench.adapters.opendataloader as module

    captured = {}

    def fake_cli(inputs, out_dir, **kwargs):
        captured.update(kwargs)
        (out_dir / "sample.json").write_bytes(
            b'{"file name":"sample.pdf","number of pages":1,"kids":'
            b'[{"type":"paragraph","page number":1,"bounding box":[0,0,10,10],"content":"hello"}]}'
        )
        (out_dir / "sample.md").write_bytes(b"# raw markdown\n")

    monkeypatch.setattr(module, "chay_cli", fake_cli)
    monkeypatch.setattr(module, "kich_thuoc_trang", lambda _path: [(100.0, 100.0)])
    _hybrid_runtime(monkeypatch, module, tmp_path)
    adapter = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])
    adapter.configure_hardware("cpu")
    result = adapter.run(tmp_path / "sample.pdf")

    assert captured["hybrid"] == "docling-fast"
    assert captured["hybrid_mode"] == "full"
    assert captured["hybrid_fallback"] is False
    assert captured["hybrid_url"] == "http://127.0.0.1:5002"
    artifacts = {artifact.name: artifact.data for artifact in result.raw_artifacts}
    assert artifacts["opendataloader.json"].startswith(b'{"file name"')
    assert artifacts["opendataloader.md"] == b"# raw markdown\n"
    assert b'"0"' in artifacts["opendataloader-map.json"]


def test_odl_scan_revalidates_manifest_before_each_run(monkeypatch, tmp_path):
    import ocr_bench.adapters.opendataloader as module

    manifest = _hybrid_runtime(monkeypatch, module, tmp_path)
    adapter = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])
    adapter.configure_hardware("cpu")
    manifest.write_text("{}", encoding="utf-8")
    called = False

    def forbidden_cli(*_args, **_kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(module, "chay_cli", forbidden_cli)

    with pytest.raises(RuntimeError, match="manifest"):
        adapter.run(tmp_path / "sample.pdf")
    assert called is False


def test_odl_scan_rejects_valid_live_manifest_rebind_after_configuration(
    monkeypatch, tmp_path
):
    import ocr_bench.adapters.opendataloader as module

    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _hybrid_runtime(monkeypatch, module, first, pid=4242)
    adapter = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])
    adapter.configure_hardware("cpu")
    frozen = dict(adapter._hybrid_evidence)

    _hybrid_runtime(monkeypatch, module, second, pid=5252)
    called = False

    def forbidden_cli(*_args, **_kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(module, "chay_cli", forbidden_cli)
    with pytest.raises(RuntimeError, match="identity|rebind"):
        adapter.run(tmp_path / "sample.pdf")

    assert called is False
    assert adapter._hybrid_evidence == frozen
    assert adapter.config_fingerprint()["device"] == "unverified"


def test_odl_scan_uses_shared_default_manifest_without_process_local_env(
    monkeypatch, tmp_path
):
    import ocr_bench.adapters.opendataloader as module

    manifest = _hybrid_runtime(
        monkeypatch, module, tmp_path, use_env=False
    )
    adapter = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])

    assert module.HYBRID_MANIFEST_ENV not in module.os.environ
    assert adapter.configure_hardware("cpu") == "cpu"
    assert adapter._hybrid_evidence["manifest_path"] == str(manifest.resolve())


def test_odl_scan_environment_manifest_override_wins_over_default(
    monkeypatch, tmp_path
):
    import ocr_bench.adapters.opendataloader as module

    monkeypatch.setattr(
        module, "DEFAULT_HYBRID_MANIFEST_PATH", tmp_path / "missing-default.json"
    )
    manifest = _hybrid_runtime(monkeypatch, module, tmp_path, use_env=True)
    adapter = OpenDataLoaderAdapter.from_profile(CATALOG["opendataloader_scan"])

    adapter.configure_hardware("cpu")
    assert adapter._hybrid_evidence["manifest_path"] == str(manifest.resolve())


def test_opendataloader_malformed_document_mapping_is_adapter_error():
    with pytest.raises(AdapterOutputError, match="OpenDataLoader"):
        build_result(
            engine_version="2.5.0",
            doc_id="bad",
            capabilities=OpenDataLoaderAdapter.capabilities,
            doc={"kids": "not-a-list"},
            markdown="",
            trang=[(100.0, 100.0)],
            anh_bytes={},
            config_fingerprint={"hardware": "cpu", "device": "cpu", "hardware_evidence_version": 1},
        )


@pytest.mark.parametrize(
    ("json_bytes", "markdown_bytes"),
    [
        (b"not-json", b"# valid"),
        (b'{"number of pages":1,"kids":[]}', b"\xff"),
    ],
)
def test_opendataloader_malformed_raw_files_are_adapter_failures(
    monkeypatch, tmp_path, json_bytes, markdown_bytes
):
    import ocr_bench.adapters.opendataloader as module

    def fake_cli(inputs, out_dir, **kwargs):
        (out_dir / "sample.json").write_bytes(json_bytes)
        (out_dir / "sample.md").write_bytes(markdown_bytes)

    monkeypatch.setattr(module, "chay_cli", fake_cli)
    monkeypatch.setattr(module, "kich_thuoc_trang", lambda _path: [(100.0, 100.0)])
    result = OpenDataLoaderAdapter.from_profile(
        CATALOG["opendataloader_default"]
    ).execute(tmp_path / "sample.pdf")

    assert result.failed is True
    assert result.failure_kind is FailureKind.ADAPTER_ERROR


def test_opendataloader_missing_markdown_is_adapter_error(monkeypatch, tmp_path):
    import ocr_bench.adapters.opendataloader as module

    def fake_cli(inputs, out_dir, **kwargs):
        (out_dir / "sample.json").write_bytes(
            b'{"number of pages":1,"kids":[]}'
        )

    monkeypatch.setattr(module, "chay_cli", fake_cli)
    monkeypatch.setattr(module, "kich_thuoc_trang", lambda _path: [(100.0, 100.0)])

    with pytest.raises(AdapterOutputError, match="Markdown.*missing"):
        OpenDataLoaderAdapter.from_profile(
            CATALOG["opendataloader_default"]
        ).run(tmp_path / "sample.pdf")


def test_opendataloader_existing_empty_markdown_is_preserved(monkeypatch, tmp_path):
    import ocr_bench.adapters.opendataloader as module

    def fake_cli(inputs, out_dir, **kwargs):
        (out_dir / "sample.json").write_bytes(
            b'{"number of pages":1,"kids":[]}'
        )
        (out_dir / "sample.md").write_bytes(b"")

    monkeypatch.setattr(module, "chay_cli", fake_cli)
    monkeypatch.setattr(module, "kich_thuoc_trang", lambda _path: [(100.0, 100.0)])
    result = OpenDataLoaderAdapter.from_profile(
        CATALOG["opendataloader_default"]
    ).run(tmp_path / "sample.pdf")

    assert result.text_md == ""
    artifacts = {artifact.name: artifact.data for artifact in result.raw_artifacts}
    assert artifacts["opendataloader.md"] == b""


# --------------------------------------------------------------------------
# Chạy thật — phần dữ liệu giả không bao giờ bắt được
# --------------------------------------------------------------------------


@needs_odl
def test_that_chay_ra_block_khong_rong():
    """Cổng chống lớp lỗi của A4: adapter trả `OcrResult` hợp lệ nhưng RỖNG.

    Dữ liệu giả được dựng khớp giả định của chính mình nên không bắt được. Chỉ
    có khẳng định trên lượt chạy thật mới bắt.
    """
    r = OpenDataLoaderAdapter().execute(ROOT / "pdfs" / "sample_minimal.pdf")
    assert not r.failed, r.error
    assert r.blocks, "chạy thật mà không ra block nào"
    assert any(b.box is not None for b in r.blocks)
    assert r.text_md
    assert r.page_sizes


@needs_odl
def test_that_moi_box_nam_trong_khoang_0_1():
    r = OpenDataLoaderAdapter().execute(ROOT / "pdfs" / "sample_minimal.pdf")
    for b in r.blocks:
        if b.box is None:
            continue
        assert 0.0 <= b.box.x0 <= b.box.x1 <= 1.0
        assert 0.0 <= b.box.y0 <= b.box.y1 <= 1.0
        assert b.box.page >= 0


@needs_odl
def test_that_kich_thuoc_trang_khop_mediabox():
    """Nguồn thứ hai kiểm nguồn thứ nhất: số trang engine khai phải khớp `pypdf`."""
    import json

    pdf = ROOT / "pdfs" / "sample_minimal.pdf"
    kt = kich_thuoc_trang(pdf)
    assert kt == [(595.0, 842.0)]

    r = OpenDataLoaderAdapter().execute(pdf)
    assert r.page_sizes == tuple(kt)
    assert json  # giữ import cho rõ ý: dữ liệu đối chiếu đến từ hai đường
