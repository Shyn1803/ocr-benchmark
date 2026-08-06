"""Test bộ nối pdf-inspector — A6 (TASK-077).

Chia hai nửa như A4/A5:

* **Không cần engine** — nhãn, số trang, toạ độ, hộp suy biến, `item_type` bẩn.
  Chạy trên `SimpleNamespace` giả nên xanh trên máy trắng.
* **Cần engine** (`needs_pi`) — chạy thật. Bài học A4/A5: dữ liệu giả được dựng
  để khớp giả định của chính mình, nên nó **không bao giờ** bắt được lớp lỗi
  "trường có giá trị, đúng kiểu, và sai" — mà A6 dính đúng lớp đó ba lần
  (`width=0`, gốc MediaBox không bị trừ, `pages_needing_ocr` 1-based nằm cạnh
  `PageMarkdown.page` 0-based trong **cùng một object**).
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

from ocr_bench.adapters.pdf_inspector import (
    SCAN_LABEL_APIS,
    PdfInspectorAdapter,
    blocks_tu_items,
    build_result,
    kich_thuoc_trang,
    nhan_tu_classify,
    nhan_tu_pages,
    text_md_tu_pages,
)
from ocr_bench.types import BlockType, Capability

ROOT = Path(__file__).resolve().parents[1]

needs_pi = pytest.mark.skipif(
    __import__("importlib.util", fromlist=["util"]).find_spec("pdf_inspector") is None,
    reason="cần extra `pdfinspector` (+ pypdf) — venv .venv-pi",
)


# --------------------------------------------------------------------------
# Object giả — đúng hình dạng đo được từ engine thật
# --------------------------------------------------------------------------

TRANG_A4 = [(612.0, 792.0, 0.0, 0.0)]


def item(text="xin chào", page=1, x=50.0, y=700.0, width=40.0, height=10.0, item_type="text"):
    return NS(
        text=text,
        page=page,
        x=x,
        y=y,
        width=width,
        height=height,
        item_type=item_type,
        font="F1",
        font_size=10.0,
    )


def classification(pdf_type="text_based", confidence=1.0, pages=(), page_count=1):
    # Đúng bộ trường thật: KHÔNG có trường lý do nào.
    return NS(
        pdf_type=pdf_type,
        confidence=confidence,
        pages_needing_ocr=list(pages),
        page_count=page_count,
    )


def pages_result(*pages, needing=(), reasons=()):
    return NS(
        pages=list(pages),
        # 1-based, cố ý để lệch với `PageMarkdown.page` — y như engine thật.
        pages_needing_ocr=list(needing),
        ocr_reasons_by_page=list(reasons),
        is_complex=False,
        pages_with_columns=[],
        pages_with_tables=[],
    )


def trang_md(page=0, markdown="# Tiêu đề", needs_ocr=False, ocr_reason=None):
    return NS(page=page, markdown=markdown, needs_ocr=needs_ocr, ocr_reason=ocr_reason)


# --------------------------------------------------------------------------
# AC-01 — khai CẢ scan_label LẪN text_md
# --------------------------------------------------------------------------


def test_khai_ca_text_md_lan_scan_label():
    """A0 bác bỏ giả định "pdf-inspector không trích text" của kế hoạch gốc."""
    caps = PdfInspectorAdapter.capabilities
    assert Capability.TEXT_MD in caps
    assert Capability.SCAN_LABEL in caps
    assert Capability.BLOCK_BBOX in caps


def test_khong_khai_nang_luc_engine_khong_co():
    """Khai thừa thì metric chấm 0.0 cho thứ engine không hứa — phạt oan."""
    caps = PdfInspectorAdapter.capabilities
    assert Capability.TABLE_HTML not in caps
    assert Capability.IMAGE_BYTES not in caps
    assert Capability.SECTION_HIERARCHY not in caps


def test_text_md_noi_theo_thu_tu_trang():
    r = pages_result(trang_md(2, "ba"), trang_md(0, "một"), trang_md(1, "hai"))
    assert text_md_tu_pages(r) == "một\n\nhai\n\nba"


# --------------------------------------------------------------------------
# AC-02 — ScanLabel.api ghi rõ nhãn đến từ hàm nào
# --------------------------------------------------------------------------


def test_hai_api_cho_hai_ten_khac_nhau():
    a = nhan_tu_classify(classification())
    b = nhan_tu_pages(pages_result(trang_md()))
    assert a.api == "classify_pdf"
    assert b.api == "extract_pages_markdown"
    assert a.api != b.api
    assert set(SCAN_LABEL_APIS) == {a.api, b.api}


def test_hai_api_bat_dong_thi_ghi_vao_error():
    """10.8% bộ mẫu rơi vào ca này — im lặng là giấu mất chính thứ A6 đo."""
    r = build_result(
        engine_version="0.2.6",
        doc_id="t",
        capabilities=PdfInspectorAdapter.capabilities,
        classification=classification("image_based", 0.8, pages=(0,)),
        pages_result=pages_result(trang_md(0, "chữ sạch", needs_ocr=False)),
        items=[item()],
        trang=TRANG_A4,
        scan_label_api="classify_pdf",
        config_fingerprint={},
    )
    assert "bất đồng" in (r.error or "")
    assert "classify_pdf.is_scanned=True" in r.error
    assert "extract_pages_markdown.is_scanned=False" in r.error


def test_hai_api_dong_thuan_thi_khong_bao_gi():
    r = build_result(
        engine_version="0.2.6",
        doc_id="t",
        capabilities=PdfInspectorAdapter.capabilities,
        classification=classification("text_based", 1.0),
        pages_result=pages_result(trang_md(0, "chữ", needs_ocr=False)),
        items=[item()],
        trang=TRANG_A4,
        scan_label_api="classify_pdf",
        config_fingerprint={},
    )
    assert r.error is None


@pytest.mark.parametrize("api", SCAN_LABEL_APIS)
def test_scan_label_lay_dung_api_duoc_chon(api):
    r = build_result(
        engine_version="0.2.6",
        doc_id="t",
        capabilities=PdfInspectorAdapter.capabilities,
        classification=classification(),
        pages_result=pages_result(trang_md()),
        items=[item()],
        trang=TRANG_A4,
        scan_label_api=api,
        config_fingerprint={},
    )
    assert r.scan_label is not None
    assert r.scan_label.api == api


def test_api_khong_hop_le_bi_chan_som():
    with pytest.raises(ValueError, match="scan_label_api"):
        PdfInspectorAdapter(scan_label_api="process_pdf")


def test_khong_bia_do_tin_cay_cho_api_khong_khai():
    """`extract_pages_markdown` không có `confidence` — để None, không lấy 1.0."""
    assert nhan_tu_pages(pages_result(trang_md())).confidence is None
    assert nhan_tu_classify(classification(confidence=0.8)).confidence == 0.8


def test_ly_do_lay_tu_tung_trang_khong_lay_tu_object_cha():
    """Đo được: `ocr_reasons_by_page` **rỗng** kể cả khi có trang cần OCR."""
    r = pages_result(
        trang_md(0, needs_ocr=True, ocr_reason="suspected_garbled_text"),
        reasons=[],  # object cha rỗng — y như engine thật
    )
    nhan = nhan_tu_pages(r)
    assert nhan.reason == "trang 0: suspected_garbled_text"


# --------------------------------------------------------------------------
# AC-03 — ba quy ước số trang, chuẩn hoá về 0-based
# --------------------------------------------------------------------------


@pytest.mark.parametrize("thô,mong", [(1, 0), (2, 1), (17, 16)])
def test_text_item_page_tru_mot(thô, mong):
    blocks, _, _ = blocks_tu_items(
        [item(page=thô)], [(612.0, 792.0, 0.0, 0.0)] * 20
    )
    assert blocks[0].box is not None
    assert blocks[0].box.page == mong


def test_trang_mot_khong_bi_hieu_thanh_trang_hai():
    """Không trừ thì tài liệu 1 trang rụng **sạch** block."""
    blocks, _, hong = blocks_tu_items([item(page=1)], TRANG_A4)
    assert not hong
    assert blocks[0].box is not None and blocks[0].box.page == 0


@pytest.mark.parametrize("xau", [0, -1, None, "1", True, 1.0])
def test_so_trang_hong_thi_bo_item_va_ghi_loi(xau):
    """`isinstance(True, int)` là True trong Python — `bool` phải chặn riêng."""
    blocks, _, hong = blocks_tu_items([item(page=xau)], TRANG_A4)
    assert blocks == []
    assert hong == {xau}


def test_page_ngoai_pham_vi_bi_bo_chu_khong_roi_ve_trang_0():
    blocks, _, hong = blocks_tu_items([item(page=9)], TRANG_A4)
    assert blocks == []
    assert hong == {9}


def test_page_markdown_giu_nguyen_vi_da_0_based():
    """`PageMarkdown.page` 0-based, `pages_needing_ocr` 1-based — cùng một object."""
    r = pages_result(trang_md(0, needs_ocr=True), needing=[1])
    nhan = nhan_tu_pages(r)
    # Lấy từ `PageMarkdown.page` (0-based), KHÔNG từ `pages_needing_ocr` (1-based).
    assert nhan.pages_needing_ocr == (0,)


def test_classify_pages_needing_ocr_da_0_based_thi_khong_tru():
    assert nhan_tu_classify(classification(pages=(0, 2))).pages_needing_ocr == (0, 2)


# --------------------------------------------------------------------------
# Toạ độ — gốc dưới-trái, y lên, KHÔNG tự trừ gốc MediaBox
# --------------------------------------------------------------------------


def test_toa_do_y_huong_len():
    """y lớn = gần đỉnh trang → y0 chuẩn hoá phải NHỎ."""
    tren, _, _ = blocks_tu_items([item(y=700.0, height=10.0)], TRANG_A4)
    duoi, _, _ = blocks_tu_items([item(y=50.0, height=10.0)], TRANG_A4)
    assert tren[0].box.y0 < duoi[0].box.y0


def test_item_sat_dinh_trang_ra_y0_gan_0():
    b, _, _ = blocks_tu_items([item(y=782.0, height=10.0)], TRANG_A4)
    assert b[0].box.y0 == pytest.approx(0.0, abs=1e-6)


def test_tru_goc_mediabox_vi_engine_khong_tu_tru():
    """Ngược hẳn OpenDataLoader. Chép quy tắc từ đó sang là sai **câm**."""
    lech = [(612.0, 792.0, 100.0, 200.0)]
    b, _, _ = blocks_tu_items([item(x=150.0, y=900.0, width=61.2, height=79.2)], lech)
    assert b[0].box.x0 == pytest.approx(50.0 / 612.0)
    # y=900 với gốc bottom=200 → 700 trong trang; đỉnh box = 700+79.2 = 779.2
    assert b[0].box.y0 == pytest.approx(1.0 - 779.2 / 792.0)


def test_khong_tru_goc_thi_ket_qua_khac_han():
    """Bằng chứng rằng bỏ `page_x0` không phải chuyện vô hại."""
    lech = [(612.0, 792.0, 100.0, 200.0)]
    goc0 = [(612.0, 792.0, 0.0, 0.0)]
    a, _, _ = blocks_tu_items([item(x=150.0, y=900.0)], lech)
    b, _, _ = blocks_tu_items([item(x=150.0, y=900.0)], goc0)
    assert a[0].box.x0 != pytest.approx(b[0].box.x0)


# --------------------------------------------------------------------------
# width == 0 — giữ chữ, bỏ hộp, và ĐẾM ĐƯỢC
# --------------------------------------------------------------------------


def test_width_0_thi_bo_hop_nhung_giu_chu():
    blocks, mat, _ = blocks_tu_items([item(text="and", width=0.0)], TRANG_A4)
    assert len(blocks) == 1
    assert blocks[0].text == "and"
    assert blocks[0].box is None
    assert mat == 1


def test_khong_suy_be_rong_tu_font_size():
    """Suy ra là đoán, và số đoán đi thẳng vào IoU như thể là số đo."""
    blocks, _, _ = blocks_tu_items([item(text="mười ký tự", width=0.0)], TRANG_A4)
    assert blocks[0].box is None


def test_khong_bao_gio_sinh_hop_dien_tich_0():
    """`Box.from_absolute` chấp nhận x1==x0 im lặng — nên chặn ở tầng trên."""
    blocks, _, _ = blocks_tu_items(
        [item(width=0.0), item(height=0.0), item(width=30.0, height=10.0)], TRANG_A4
    )
    assert all(b.box is None or b.box.area > 0 for b in blocks)


def test_so_item_mat_hop_hien_ra_o_error():
    r = build_result(
        engine_version="0.2.6",
        doc_id="t",
        capabilities=PdfInspectorAdapter.capabilities,
        classification=classification(),
        pages_result=pages_result(trang_md()),
        items=[item(width=0.0), item(width=0.0), item()],
        trang=TRANG_A4,
        scan_label_api="classify_pdf",
        config_fingerprint={},
    )
    assert "2/3 item không có bề rộng" in (r.error or "")


# --------------------------------------------------------------------------
# item_type mang cả dữ liệu
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "thô,mong",
    [
        ("text", BlockType.TEXT),
        ("image", BlockType.PICTURE),
        # Giá trị thật quan sát được — URL nhét thẳng vào trường "kiểu".
        ("link:https://webgate.ec.europa.eu/x?y=1", BlockType.OTHER),
        ("TEXT", BlockType.TEXT),
        ("loại-chưa-từng-thấy", BlockType.OTHER),
        (None, BlockType.OTHER),
    ],
)
def test_item_type_ban_van_ra_loai_hop_le(thô, mong):
    blocks, _, _ = blocks_tu_items([item(item_type=thô)], TRANG_A4)
    assert blocks[0].block_type is mong


def test_loai_la_khong_bi_bo():
    """Bỏ block là mất recall; bản engine mới thêm loại không được làm điểm tụt."""
    blocks, _, _ = blocks_tu_items([item(item_type="link:https://x")], TRANG_A4)
    assert len(blocks) == 1 and blocks[0].text


# --------------------------------------------------------------------------
# Không-ném ở nhánh bắt lỗi của execute() — lỗi #2 và #3 của A5
# --------------------------------------------------------------------------


def test_version_khong_nem_khi_chua_cai():
    assert isinstance(PdfInspectorAdapter().version(), str)


def test_config_fingerprint_khong_nem_va_ghi_ro_api_da_dung():
    fp = PdfInspectorAdapter(scan_label_api="extract_pages_markdown").config_fingerprint()
    assert fp["scan_label_api"] == "extract_pages_markdown"
    assert isinstance(fp["pdf_inspector_version"], str)


def test_execute_ghi_that_bai_chu_khong_no(tmp_path):
    """`execute()` gọi `version()` + `config_fingerprint()` **trong nhánh bắt lỗi**."""
    r = PdfInspectorAdapter().execute(tmp_path / "khong-ton-tai.pdf")
    assert r.failed
    assert r.error


# --------------------------------------------------------------------------
# Import lười — một import hỏng làm rụng CẢ registry
# --------------------------------------------------------------------------


def test_khong_import_engine_o_cap_cao_nhat():
    nguon = (ROOT / "src/ocr_bench/adapters/pdf_inspector.py").read_text(encoding="utf-8")
    cay = ast.parse(nguon)
    cam = {"pdf_inspector", "pypdf", "fitz"}
    for n in cay.body:  # chỉ cấp cao nhất — trong hàm thì được phép
        if isinstance(n, ast.Import):
            assert not ({a.name.split(".")[0] for a in n.names} & cam)
        elif isinstance(n, ast.ImportFrom) and n.module:
            assert n.module.split(".")[0] not in cam


def test_dang_ky_trong_registry():
    from ocr_bench import registry

    assert registry.get_adapter("pdf_inspector") is PdfInspectorAdapter


# --------------------------------------------------------------------------
# Chạy thật — nửa duy nhất bắt được lớp lỗi "có giá trị, đúng kiểu, và sai"
# --------------------------------------------------------------------------

CORPUS = ROOT / "pdfs" / "doclaynet"


@needs_pi
@pytest.mark.needs_corpus
@pytest.mark.skipif(not CORPUS.is_dir(), reason="chưa có bộ mẫu doclaynet")
def test_that_blocks_va_text_khong_rong():
    """Bài học A4: `OcrResult` hợp lệ mà rỗng vẫn trượt qua toàn bộ test giả."""
    pdf = sorted(CORPUS.glob("*.pdf"))[0]
    r = PdfInspectorAdapter().execute(pdf)
    assert not r.failed, r.error
    assert r.blocks, "engine trả 0 block"
    assert r.text_md and r.text_md.strip(), "engine trả text rỗng"
    assert r.scan_label is not None and r.scan_label.api == "classify_pdf"


@needs_pi
@pytest.mark.needs_corpus
@pytest.mark.skipif(not CORPUS.is_dir(), reason="chưa có bộ mẫu doclaynet")
def test_that_moi_box_nam_trong_khoang_0_1():
    pdf = sorted(CORPUS.glob("*.pdf"))[0]
    r = PdfInspectorAdapter().execute(pdf)
    for b in r.blocks:
        if b.box is None:
            continue
        assert 0.0 <= b.box.x0 <= b.box.x1 <= 1.0
        assert 0.0 <= b.box.y0 <= b.box.y1 <= 1.0


@needs_pi
@pytest.mark.needs_corpus
@pytest.mark.skipif(not CORPUS.is_dir(), reason="chưa có bộ mẫu doclaynet")
def test_that_so_trang_khop_pypdf():
    pdf = sorted(CORPUS.glob("*.pdf"))[0]
    r = PdfInspectorAdapter().execute(pdf)
    assert len(r.page_sizes) == len(kich_thuoc_trang(pdf))
    for b in r.blocks:
        if b.box is not None:
            assert 0 <= b.box.page < len(r.page_sizes)


@needs_pi
@pytest.mark.needs_corpus
@pytest.mark.skipif(not CORPUS.is_dir(), reason="chưa có bộ mẫu doclaynet")
def test_that_hai_api_that_su_bat_dong_tren_bo_mau():
    """Nếu test này thành xanh-vì-không-có-ca-nào thì tiền đề của A6 sai."""
    import pdf_inspector as pi

    bat_dong = 0
    for pdf in sorted(CORPUS.glob("*.pdf"))[:60]:
        a = nhan_tu_classify(pi.classify_pdf(str(pdf)))
        b = nhan_tu_pages(pi.extract_pages_markdown(str(pdf)))
        bat_dong += a.is_scanned != b.is_scanned
    assert bat_dong > 0, "hai API đồng thuận hết — đọc lại giả định của A6"
