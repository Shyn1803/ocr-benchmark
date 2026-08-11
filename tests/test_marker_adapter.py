"""Test bộ nối Marker — A4 (TASK-075).

Chia làm hai nửa:

* **Không cần marker** — ánh xạ loại block, cấp mục, quy đổi toạ độ, bảng, ảnh. Chạy
  trên `ChunkOutput` giả nên xanh trên máy trắng. Đây là phần chiếm gần hết logic của
  adapter, và cũng là phần dễ sai âm thầm nhất.
* **Cần marker** (`needs_marker`) — AC-03: chạy thật rồi so hai đường. Không có cách
  nào giả được, vì câu hỏi chính là "Marker có mutate document khi render không".
"""

from __future__ import annotations

import ast
import base64
import io
from pathlib import Path

import pytest

from ocr_bench.adapters.base import AdapterOutputError
from ocr_bench.adapters.marker import (
    BLOCK_TYPE_MAP,
    MarkerAdapter,
    build_result,
    heading_level,
    html_to_text,
    map_block_type,
    page_index,
)
from ocr_bench.profiles import EngineProfile, ProfileConfigError, load_profile_catalog
from ocr_bench.types import BlockType, Capability

ROOT = Path(__file__).resolve().parents[1]
CATALOG = load_profile_catalog(ROOT / "configs" / "profiles.json")


# --------------------------------------------------------------------------
# Giả lập `ChunkOutput` — chỉ cần đúng những thuộc tính adapter đụng tới.
# --------------------------------------------------------------------------


class FakeBlock:
    """`id` mặc định dựng khớp với `page` — dạng Marker in ra:
    `/page/{page_id}/{block_type}/{block_id}`.

    Có test cố tình cho hai cái lệch nhau, vì Marker thật cũng lệch (xem
    `page_index`)."""

    def __init__(
        self,
        *,
        block_type,
        html,
        page,
        bbox,
        section_hierarchy=None,
        images=None,
        id=None,
    ):
        self.block_type = block_type
        self.html = html
        self.page = page
        self.bbox = bbox
        self.section_hierarchy = section_hierarchy
        self.images = images
        self.id = id if id is not None else f"/page/{page}/{block_type}/0"


class FakeChunks:
    def __init__(self, blocks, page_info):
        self.blocks = blocks
        self.page_info = page_info


def png_b64(color=(255, 0, 0)) -> str:
    """Một ảnh JPEG base64 — đúng như Marker trả về (OUTPUT_IMAGE_FORMAT mặc định)."""
    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (4, 4), color).save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def dung_ket_qua(blocks, page_info=None, block_bboxes=None):
    return build_result(
        engine_version="1.10.2",
        doc_id="tai-lieu",
        capabilities=MarkerAdapter.capabilities,
        markdown="# Tiêu đề",
        chunks=FakeChunks(blocks, page_info or {0: {"bbox": [0.0, 0.0, 100.0, 200.0]}}),
        block_bboxes=block_bboxes or {},
        config_fingerprint={"marker_version": "1.10.2"},
    )


# --------------------------------------------------------------------------
# AC-01 — khai đủ năng lực
# --------------------------------------------------------------------------


def test_khai_du_bay_nang_luc():
    """Marker là engine duy nhất khai CẢ HAI `HEADING_LEVEL` và `SECTION_HIERARCHY`:
    nó vừa đặt `level` (từ `#`/`##`) vừa dựng được đường dẫn tổ tiên. So với
    opendataloader — chỉ có cấp, không có cây."""
    assert MarkerAdapter.capabilities == frozenset(
        {
            Capability.TEXT_MD,
            Capability.BLOCK_BBOX,
            Capability.IMAGE_BBOX,
            Capability.IMAGE_BYTES,
            Capability.TABLE_HTML,
            Capability.HEADING_LEVEL,
            Capability.SECTION_HIERARCHY,
        }
    )


def test_dang_ky_san_trong_registry():
    from ocr_bench import registry

    assert registry.get_adapter("marker") is MarkerAdapter


# --------------------------------------------------------------------------
# Import lười — điều kiện để `pytest` xanh trên máy trắng
# --------------------------------------------------------------------------


def test_module_khong_import_marker_o_dau_file():
    """Kiểm bằng AST, không bằng `try: import`.

    marker-pdf kéo theo torch + Surya vài GB nên nó là extra. Import ở đầu module thì
    `import ocr_bench` trên máy trắng nổ và **cả registry rụng theo** — không chỉ
    Marker biến mất khỏi bảng mà `noop`/`sabotage` cũng mất.
    """
    cay = ast.parse((ROOT / "src" / "ocr_bench" / "adapters" / "marker.py").read_text("utf-8"))
    for nut in cay.body:  # chỉ cấp cao nhất — trong hàm thì được phép
        if isinstance(nut, ast.Import):
            ten = [a.name for a in nut.names]
        elif isinstance(nut, ast.ImportFrom):
            ten = [nut.module or ""]
        else:
            continue
        for t in ten:
            assert not t.startswith(("marker", "torch", "surya", "PIL")), (
                f"import {t} ở đầu module — phải đưa vào trong hàm"
            )


# --------------------------------------------------------------------------
# AC-04 — quy đổi toạ độ
# --------------------------------------------------------------------------


def test_toa_do_y_huong_xuong():
    """Marker gốc trên-trái, y xuống: block ở đỉnh trang phải ra y0 ≈ 0."""
    r = dung_ket_qua([FakeBlock(block_type="Text", html="<p>a</p>", page=0, bbox=[0, 0, 50, 20])])
    b = r.blocks[0].box
    assert b.y0 == pytest.approx(0.0)
    assert b.y1 == pytest.approx(0.1)
    assert b.x1 == pytest.approx(0.5)


def test_trang_khong_bat_dau_o_goc_van_ra_dung():
    """Nhánh `force_ocr` lấy bbox trang từ pdfium; nó có thể không bắt đầu ở [0,0].

    Bỏ qua `page_x0`/`page_y0` thì mọi box lệch **một lượng cố định**, và IoU ra một
    con số thấp-nhưng-hợp-lý trông y hệt "engine này cắt vùng dở". Không có test này
    thì cái lệch đó không để lại triệu chứng nào trên bảng kết quả.
    """
    r = dung_ket_qua(
        [FakeBlock(block_type="Text", html="<p>a</p>", page=0, bbox=[10, 20, 60, 120])],
        page_info={0: {"bbox": [10.0, 20.0, 110.0, 220.0]}},
    )
    b = r.blocks[0].box
    assert (b.x0, b.y0) == (pytest.approx(0.0), pytest.approx(0.0))
    assert (b.x1, b.y1) == (pytest.approx(0.5), pytest.approx(0.5))


def test_page_sizes_lay_tu_page_info():
    r = dung_ket_qua(
        [FakeBlock(block_type="Text", html="<p>a</p>", page=1, bbox=[0, 0, 10, 10])],
        page_info={
            0: {"bbox": [0.0, 0.0, 100.0, 200.0]},
            1: {"bbox": [5.0, 5.0, 105.0, 305.0]},
        },
    )
    assert r.page_sizes == ((100.0, 200.0), (100.0, 300.0))


def test_thieu_trang_thi_bo_block_va_ghi_loi():
    """Không rơi về `page_width=1`.

    Box chuẩn hoá sai còn tệ hơn box thiếu: nó vẫn được chấm, vẫn kéo điểm xuống, và
    không để lại dấu vết nào để lần ra.
    """
    r = dung_ket_qua(
        [
            FakeBlock(block_type="Text", html="<p>a</p>", page=0, bbox=[0, 0, 10, 10]),
            FakeBlock(block_type="Text", html="<p>b</p>", page=7, bbox=[0, 0, 10, 10]),
        ]
    )
    assert len(r.blocks) == 1
    assert "7" in (r.error or "")


# --------------------------------------------------------------------------
# Số trang — trường `page` của Marker không đáng tin
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "block_id, fallback, mong_doi",
    [
        ("/page/0/Text/3", 99, 0),
        ("/page/12/SectionHeader/1", 99, 12),
        ("/page/7", 99, 7),  # block Page, không có block_type
        ("khong-phai-dang-nay", 5, 5),  # không parse được → dùng fallback
        ("/trang/2/Text/1", 5, 5),  # phân đoạn đầu không phải "page"
        ("/page/x/Text/1", 5, 5),  # số trang không phải số
    ],
)
def test_so_trang_lay_tu_id(block_id, fallback, mong_doi):
    assert page_index(block_id, fallback) == mong_doi


def test_khong_tin_truong_page_cua_marker():
    """Hồi quy cho lỗi thật của marker-pdf 1.10.2.

    `json_to_chunks` tính `page` bằng `int(block.id.split("/")[-1])` trên block Page,
    mà `BlockId.__str__` in block Page ra `/page/0/Page/8` → lấy nhầm `block_id`. Đo
    thật trên `pdfs/sample_minimal.pdf` (1 trang): `page_info` có khoá `0`, mọi block
    khai `page=8`.

    Tin trường đó thì mọi block bị bỏ và Marker lên bảng với 0 vùng — hỏng mà không
    ném lỗi, chỉ làm engine tốt trông như engine tồi.
    """
    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="Text",
                html="<p>a</p>",
                page=8,  # ← số Marker khai, sai
                bbox=[0, 0, 10, 10],
                id="/page/0/Text/0",  # ← số thật, nằm trong id
            )
        ],
        page_info={0: {"bbox": [0.0, 0.0, 100.0, 200.0]}},
    )
    assert r.error is None
    assert len(r.blocks) == 1
    assert r.blocks[0].box.page == 0


# --------------------------------------------------------------------------
# Ánh xạ loại block
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "marker_type,mong_doi",
    [
        ("Text", BlockType.TEXT),
        ("TextInlineMath", BlockType.TEXT),
        ("Form", BlockType.TEXT),
        ("SectionHeader", BlockType.HEADING),
        ("ListItem", BlockType.LIST),
        ("Table", BlockType.TABLE),
        ("TableOfContents", BlockType.TABLE),
        ("Figure", BlockType.PICTURE),
        ("PictureGroup", BlockType.PICTURE),
        ("Caption", BlockType.CAPTION),
        ("Footnote", BlockType.FOOTNOTE),
        ("PageHeader", BlockType.PAGE_HEADER),
        ("PageFooter", BlockType.PAGE_FOOTER),
        ("Equation", BlockType.FORMULA),
        ("Code", BlockType.CODE),
    ],
)
def test_anh_xa_loai_block(marker_type, mong_doi):
    assert map_block_type(marker_type) is mong_doi


def test_loai_la_thanh_other_chu_khong_bi_bo():
    """Bản Marker mới thêm loại block không được phép làm điểm tụt.

    Bỏ block là mất recall: bảng báo Marker sót vùng mà thật ra nó tìm ra rồi.
    """
    assert map_block_type("MotLoaiHoanToanMoi") is BlockType.OTHER
    r = dung_ket_qua(
        [FakeBlock(block_type="MotLoaiHoanToanMoi", html="<p>a</p>", page=0, bbox=[0, 0, 1, 1])]
    )
    assert len(r.blocks) == 1
    assert r.blocks[0].block_type is BlockType.OTHER


def test_moi_loai_marker_that_deu_co_trong_bang_hoac_ra_other():
    """Bảng ánh xạ không được trỏ tới `BlockType` không tồn tại."""
    assert all(isinstance(v, BlockType) for v in BLOCK_TYPE_MAP.values())


# --------------------------------------------------------------------------
# Cấp mục + đường dẫn mục
# --------------------------------------------------------------------------


@pytest.mark.parametrize("cap", [1, 2, 3, 4, 5, 6])
def test_cap_muc_lay_tu_the_h(cap):
    assert heading_level(f'<h{cap} id="x">Tiêu đề</h{cap}>') == cap


def test_khong_co_the_h_thi_khong_co_cap():
    assert heading_level("<p>văn bản thường</p>") is None


def test_chi_heading_moi_co_level():
    r = dung_ket_qua(
        [
            FakeBlock(block_type="SectionHeader", html="<h2>Điều 3</h2>", page=0, bbox=[0, 0, 1, 1]),
            FakeBlock(block_type="Text", html="<h2>bẫy</h2>", page=0, bbox=[0, 0, 1, 1]),
        ]
    )
    assert r.blocks[0].level == 2
    assert r.blocks[1].level is None


def test_duong_dan_muc_sap_theo_cap_khong_theo_thu_tu_chen():
    """Dict Python giữ thứ tự chèn; đường dẫn mục đảo cấp là một đường dẫn khác."""
    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="Text",
                html="<p>a</p>",
                page=0,
                bbox=[0, 0, 1, 1],
                section_hierarchy={2: "Điều 3", 1: "Chương I"},
            )
        ]
    )
    assert r.blocks[0].section_hierarchy == ("Chương I", "Điều 3")


def test_khong_co_duong_dan_muc_thi_rong():
    r = dung_ket_qua([FakeBlock(block_type="Text", html="<p>a</p>", page=0, bbox=[0, 0, 1, 1])])
    assert r.blocks[0].section_hierarchy == ()


def test_duong_dan_muc_ra_CHU_chu_khong_ra_id():
    """Hồi quy: giá trị của `section_hierarchy` là `BlockId`, không phải chữ tiêu đề.

    `BlockOutput.section_hierarchy` khai `Dict[int, BlockId]`. `str()` thẳng ra
    `/page/0/SectionHeader/6` — trông như chuỗi hợp lệ nên rất dễ tưởng là xong, và
    lượt chạy DocLayNet đầu tiên đã ghi ra đúng như vậy.

    Đường dẫn mục dạng id thì không so được với ground truth: metric cấp mục ra 0 cho
    mọi block, và Marker mang tiếng không dựng được cây mục dù nó dựng đúng.
    """

    class KhoaBlockId:
        def __init__(self, s):
            self._s = s

        def __str__(self):
            return self._s

    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="SectionHeader",
                html="<h1>Chương I &amp; II</h1>",
                page=0,
                bbox=[0, 0, 10, 10],
                id="/page/0/SectionHeader/6",
            ),
            FakeBlock(
                block_type="Text",
                html="<p>nội dung</p>",
                page=0,
                bbox=[0, 20, 10, 30],
                section_hierarchy={1: KhoaBlockId("/page/0/SectionHeader/6")},
            ),
        ]
    )
    assert r.blocks[1].section_hierarchy == ("Chương I & II",)


def test_duong_dan_muc_bac_qua_trang():
    """Tiêu đề ở trang trước vẫn phải giải ra chữ.

    `Document.render` chuyền `section_hierarchy` từ trang này sang trang kia, nên block
    ở trang 1 thường trỏ tới tiêu đề nằm ở trang 0. Vì thế bảng tra phải dựng TRƯỚC
    vòng lặp, không dựng dần trong lúc duyệt.
    """

    class KhoaBlockId:
        def __init__(self, s):
            self._s = s

        def __str__(self):
            return self._s

    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="Text",
                html="<p>thân bài trang 1</p>",
                page=1,
                bbox=[0, 0, 10, 10],
                id="/page/1/Text/0",
                section_hierarchy={1: KhoaBlockId("/page/0/SectionHeader/2")},
            ),
            FakeBlock(
                block_type="SectionHeader",
                html="<h1>Tiêu đề trang 0</h1>",
                page=0,
                bbox=[0, 0, 10, 10],
                id="/page/0/SectionHeader/2",
            ),
        ],
        page_info={
            0: {"bbox": [0.0, 0.0, 100.0, 200.0]},
            1: {"bbox": [0.0, 0.0, 100.0, 200.0]},
        },
    )
    assert r.blocks[0].section_hierarchy == ("Tiêu đề trang 0",)


def test_khong_giai_duoc_id_thi_giu_nguyen_id():
    """Giữ id còn lần ra được nguồn; bỏ hẳn thì mất dấu vết."""

    class KhoaBlockId:
        def __init__(self, s):
            self._s = s

        def __str__(self):
            return self._s

    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="Text",
                html="<p>a</p>",
                page=0,
                bbox=[0, 0, 1, 1],
                section_hierarchy={1: KhoaBlockId("/page/9/SectionHeader/99")},
            )
        ]
    )
    assert r.blocks[0].section_hierarchy == ("/page/9/SectionHeader/99",)


@pytest.mark.parametrize(
    "html, mong_doi",
    [
        ("<h1>Chương I</h1>", "Chương I"),
        ("<h2>Điều 3 &amp; 4</h2>", "Điều 3 & 4"),
        ("<h1>  nhiều   khoảng \n trắng </h1>", "nhiều khoảng trắng"),
        ("<h1>a<br/>b</h1>", "a b"),
        ("<h1></h1>", ""),
    ],
)
def test_go_the_lay_chu(html, mong_doi):
    assert html_to_text(html) == mong_doi


# --------------------------------------------------------------------------
# AC-05 — bảng giữ nguyên HTML
# --------------------------------------------------------------------------


def test_bang_giu_nguyen_chuoi_table_html():
    """TEDS (B2) chấm trên cây HTML; ép thành chuỗi phẳng là vứt cấu trúc."""
    html = "<table><tr><td>A</td><td>B</td></tr></table>"
    r = dung_ket_qua([FakeBlock(block_type="Table", html=html, page=0, bbox=[0, 0, 50, 50])])
    assert len(r.tables) == 1
    assert r.tables[0].html == html
    assert r.tables[0].box is not None


def test_bang_vua_o_blocks_vua_o_tables():
    """Bảng là một vùng bố cục (chấm IoU) **và** một cấu trúc (chấm TEDS)."""
    r = dung_ket_qua(
        [FakeBlock(block_type="Table", html="<table></table>", page=0, bbox=[0, 0, 5, 5])]
    )
    assert r.blocks[0].block_type is BlockType.TABLE
    assert len(r.tables) == 1


def test_khong_phai_bang_thi_khong_vao_tables():
    r = dung_ket_qua([FakeBlock(block_type="Text", html="<p>a</p>", page=0, bbox=[0, 0, 1, 1])])
    assert r.tables == ()


# --------------------------------------------------------------------------
# Ảnh
# --------------------------------------------------------------------------


def test_anh_quy_ve_png_bytes():
    """Marker xuất JPEG theo mặc định; `OcrImage.data` là PNG theo hợp đồng.

    Không quy đổi thì `data` mang hai định dạng tuỳ engine và metric so ảnh nhận hai
    kiểu dữ liệu — hỏng âm thầm, không thấy trên bảng.
    """
    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="Figure",
                html="<p>hình</p>",
                page=0,
                bbox=[0, 0, 50, 50],
                images={"/page/0/Figure/1": png_b64()},
            )
        ]
    )
    assert len(r.images) == 1
    assert r.images[0].data.startswith(b"\x89PNG\r\n")


def test_bbox_anh_lay_tu_block_con_chu_khong_lay_cua_block_cha():
    """Khoá của `images` là id block **con** (Figure trong FigureGroup).

    Danh sách chunk chỉ có block top-level, nên bbox ảnh phải tra từ `document`. Lấy
    bừa bbox của cha thì ảnh nhỏ nằm trong nhóm lớn sẽ mang bbox của cả nhóm, và IoU
    ảnh tụt mà không có lý do nhìn thấy được.
    """
    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="FigureGroup",
                html="<p>nhóm</p>",
                page=0,
                bbox=[0, 0, 100, 200],
                images={"/page/0/Figure/1": png_b64()},
            )
        ],
        block_bboxes={"/page/0/Figure/1": (0, [0.0, 0.0, 50.0, 50.0])},
    )
    anh = r.images[0]
    assert anh.source_id == "/page/0/Figure/1"
    assert anh.box.x1 == pytest.approx(0.5)
    assert anh.box.y1 == pytest.approx(0.25)


def test_khoa_anh_khong_phai_str_van_ra_str():
    """Hồi quy: Marker khoá `images` bằng đối tượng `BlockId`, không phải `str`.

    `BaseRenderer.extract_block_html` (`renderers/__init__.py:144,152`) gán
    `images[block_output.id]` với `id` là `BlockId`. In ra thì giống hệt chuỗi, nên đọc
    source dễ tưởng là `str`.

    Không ép về str thì `source_id` mang `BlockId` và `json.dumps` ném
    `TypeError: Object of type BlockId is not JSON serializable` — cả lượt chạy đổ ở
    tài liệu **đầu tiên có ảnh**, tức là sau khi đã đốt hàng chục phút CPU. Chính lỗi
    này đã hạ lượt chạy DocLayNet ở tài liệu thứ 4.
    """

    class KhoaBlockId:
        """Bắt chước `BlockId`: `__str__` ra đường dẫn, `__hash__` là hash của str."""

        def __init__(self, s):
            self._s = s

        def __str__(self):
            return self._s

        def __hash__(self):
            return hash(self._s)

        def __eq__(self, other):
            return str(other) == self._s

    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="Picture",
                html="<p>ảnh</p>",
                page=0,
                bbox=[0, 0, 100, 200],
                images={KhoaBlockId("/page/0/Picture/2"): png_b64()},
            )
        ],
        block_bboxes={"/page/0/Picture/2": (0, [0.0, 0.0, 50.0, 50.0])},
    )
    anh = r.images[0]
    assert type(anh.source_id) is str
    assert anh.source_id == "/page/0/Picture/2"
    # bbox vẫn tra được sau khi ép khoá — đúng block con, không phải block cha
    assert anh.box.x1 == pytest.approx(0.5)


def test_ket_qua_co_anh_ghi_xuong_dia_duoc(tmp_path):
    """Cổng chặn thật: `OcrResult` phải **ghi xuống `prediction/` được**.

    `source_id` đi thẳng vào `json.dumps` trong `save_prediction`. Một kiểu dữ liệu lạ
    lọt tới đây thì hỏng ở chỗ xa nhất khỏi nguyên nhân — sau khi PNG đã ghi ra đĩa,
    sau hàng chục phút CPU, và chỉ ở tài liệu đầu tiên có ảnh chứ không ở tài liệu
    đầu tiên. Test kiểu dữ liệu ở trên bắt được nguyên nhân; test này bắt được lớp lỗi.
    """
    from ocr_bench.prediction import load_prediction, save_prediction

    class KhoaBlockId:
        def __init__(self, s):
            self._s = s

        def __str__(self):
            return self._s

        def __hash__(self):
            return hash(self._s)

        def __eq__(self, other):
            return str(other) == self._s

    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="Picture",
                html="<p>ảnh</p>",
                page=0,
                bbox=[0, 0, 100, 200],
                images={KhoaBlockId("/page/0/Picture/2"): png_b64()},
            )
        ],
        block_bboxes={"/page/0/Picture/2": (0, [0.0, 0.0, 50.0, 50.0])},
    )
    p = save_prediction(r, tmp_path)
    lai = load_prediction(p)
    assert lai.images[0].source_id == "/page/0/Picture/2"
    assert lai.images[0].data is not None


def test_khong_tra_duoc_bbox_anh_thi_dung_bbox_block():
    """Thà bbox rộng hơn còn hơn mất hẳn ảnh khỏi bảng."""
    r = dung_ket_qua(
        [
            FakeBlock(
                block_type="Picture",
                html="<p>hình</p>",
                page=0,
                bbox=[0, 0, 100, 200],
                images={"/page/0/Picture/9": png_b64()},
            )
        ],
        block_bboxes={},
    )
    assert r.images[0].box.x1 == pytest.approx(1.0)


def test_khong_co_anh_thi_rong():
    r = dung_ket_qua([FakeBlock(block_type="Text", html="<p>a</p>", page=0, bbox=[0, 0, 1, 1])])
    assert r.images == ()


# --------------------------------------------------------------------------
# Vân tay cấu hình
# --------------------------------------------------------------------------


def test_ket_qua_mang_van_tay_cau_hinh():
    r = dung_ket_qua([FakeBlock(block_type="Text", html="<p>a</p>", page=0, bbox=[0, 0, 1, 1])])
    assert r.config_fingerprint["marker_version"] == "1.10.2"
    assert r.engine == "marker"
    assert r.engine_version == "1.10.2"
    assert r.text_md == "# Tiêu đề"


def test_van_tay_noi_ra_che_do_chay():
    """Không ghi `force_ocr` thì bảng không nói được số đo ra ở cấu hình nào."""
    a = MarkerAdapter(force_ocr=True)
    assert a.force_ocr is True
    b = MarkerAdapter()
    assert b.force_ocr is False


@pytest.mark.parametrize(
    ("name", "force_ocr"),
    [("marker_default", False), ("marker_scan", True)],
)
def test_marker_profile_controls_force_ocr(name, force_ocr):
    adapter = MarkerAdapter.from_profile(CATALOG[name])

    assert (adapter.name, adapter.engine_family, adapter.profile) == (
        name,
        "marker",
        CATALOG[name].profile,
    )
    assert adapter.force_ocr is force_ocr
    assert adapter.use_llm is False
    fingerprint = adapter.config_fingerprint()
    assert fingerprint["profile_config_sha256"] == CATALOG[name].fingerprint
    assert fingerprint["hardware"] == "cpu"
    assert fingerprint["device"] == "cpu"
    assert type(fingerprint["hardware_evidence_version"]) is int
    assert fingerprint["hardware_evidence_version"] == 1


def test_marker_rejects_config_outside_frozen_profile():
    source = CATALOG["marker_default"]
    changed = EngineProfile(
        name=source.name,
        family=source.family,
        profile=source.profile,
        adapter=source.adapter,
        config={"force_ocr": True, "use_llm": False},
        environment=source.environment,
    )

    with pytest.raises(ProfileConfigError, match="config"):
        MarkerAdapter.from_profile(changed)


def test_marker_hardware_gpu_requires_real_cuda(monkeypatch):
    import ocr_bench.adapters.marker as module

    adapter = MarkerAdapter.from_profile(CATALOG["marker_scan"])
    monkeypatch.setattr(module, "_cuda_available", lambda: False)
    with pytest.raises(RuntimeError, match="CUDA"):
        adapter.configure_hardware("gpu")

    monkeypatch.setattr(module, "_cuda_available", lambda: True)
    assert adapter.configure_hardware("gpu") == "gpu"
    assert adapter.config_fingerprint()["device"] == "gpu"


def test_marker_raw_json_and_trace_are_attached_to_profile_result():
    block = FakeBlock(
        block_type="Text",
        html="<p>a</p>",
        page=0,
        bbox=[0, 0, 1, 1],
        id="/page/0/Text/7",
    )
    adapter = MarkerAdapter.from_profile(CATALOG["marker_default"])
    result = build_result(
        engine_version="1.10.2",
        doc_id="tai-lieu",
        capabilities=adapter.capabilities,
        markdown="# Heading",
        chunks=FakeChunks([block], {0: {"bbox": [0, 0, 100, 200]}}),
        block_bboxes={},
        config_fingerprint=adapter.config_fingerprint(),
        identity=adapter.identity,
        raw_json_bytes=b'{"blocks":[{"id":"/page/0/Text/7"}]}',
    )

    assert (result.engine, result.engine_family, result.profile) == (
        "marker_default",
        "marker",
        "default",
    )
    artifacts = {artifact.name: artifact.data for artifact in result.raw_artifacts}
    assert artifacts["marker.json"] == b'{"blocks":[{"id":"/page/0/Text/7"}]}'
    assert b'"0":"/page/0/Text/7"' in artifacts["marker-map.json"]


def test_marker_malformed_block_mapping_raises_adapter_output_error():
    with pytest.raises(AdapterOutputError, match="Marker"):
        build_result(
            engine_version="1.10.2",
            doc_id="tai-lieu",
            capabilities=MarkerAdapter.capabilities,
            markdown="# Heading",
            chunks=FakeChunks("not-a-block-list", {0: {"bbox": [0, 0, 100, 200]}}),
            block_bboxes={},
            config_fingerprint={"hardware": "cpu", "device": "cpu", "hardware_evidence_version": 1},
        )


def test_marker_raw_json_must_trace_the_chunks_being_normalized():
    block = FakeBlock(
        block_type="Text", html="<p>a</p>", page=0, bbox=[0, 0, 1, 1]
    )
    with pytest.raises(AdapterOutputError, match="raw JSON.*blocks"):
        build_result(
            engine_version="1.10.2",
            doc_id="tai-lieu",
            capabilities=MarkerAdapter.capabilities,
            markdown="# Heading",
            chunks=FakeChunks([block], {0: {"bbox": [0, 0, 100, 200]}}),
            block_bboxes={},
            config_fingerprint={"hardware": "cpu", "device": "cpu", "hardware_evidence_version": 1},
            raw_json_bytes=b'{"blocks":[]}',
        )


# --------------------------------------------------------------------------
# AC-02 + AC-03 — cần marker thật
# --------------------------------------------------------------------------


@pytest.mark.needs_marker
@pytest.mark.slow
def test_ac03_render_nhieu_lan_khong_doi_ket_qua():
    """A0 §10 để ngỏ đúng chỗ này; A0 tự ghi "suy luận đọc từ source, chưa chạy".

    `JSONRenderer.__call__` gọi `document.render()`, và `Document.render` chuyền
    `section_hierarchy` từ trang trước sang trang sau. Nếu có trạng thái bám lại trên
    `document` thì render lần hai khác lần một — và cả A4 sụp: tối ưu "build một lần"
    sẽ đang âm thầm đổi kết quả.
    """
    from marker.renderers.chunk import ChunkRenderer
    from marker.renderers.markdown import MarkdownRenderer

    pdf = ROOT / "pdfs" / "sample_minimal.pdf"
    conv = MarkerAdapter().converter()
    doc = conv.build_document(str(pdf))

    md1 = conv.resolve_dependencies(MarkdownRenderer)(doc).markdown
    conv.resolve_dependencies(ChunkRenderer)(doc)  # chen renderer khác vào giữa
    md2 = conv.resolve_dependencies(MarkdownRenderer)(doc).markdown

    assert md1 == md2, "render mutate document — tối ưu build-một-lần không hợp lệ"


@pytest.mark.needs_marker
@pytest.mark.slow
def test_ac03_duong_tat_cho_ket_qua_giong_duong_thang():
    """Vế đắt và là vế trả lời câu hỏi thật: đi đường tắt có ra cùng kết quả không.

    Đường thẳng = `converter(path)` chạy lại từ đầu. Đường tắt = build một lần rồi
    render nhiều kiểu.
    """
    from marker.renderers.markdown import MarkdownRenderer

    pdf = ROOT / "pdfs" / "sample_minimal.pdf"
    conv = MarkerAdapter().converter()

    duong_tat = conv.resolve_dependencies(MarkdownRenderer)(conv.build_document(str(pdf))).markdown
    duong_thang = conv(str(pdf)).markdown

    assert duong_tat == duong_thang


@pytest.mark.needs_marker
@pytest.mark.slow
def test_ac02_build_document_goi_dung_mot_lan():
    """Gọi `converter(path)` hai lần là mất gấp đôi thời gian máy (~3h → ~6h/200 trang)."""
    a = MarkerAdapter()
    conv = a.converter()
    dem = {"n": 0}
    that = conv.build_document

    def dem_lan(path):
        dem["n"] += 1
        return that(path)

    conv.build_document = dem_lan
    try:
        kq = a.run(ROOT / "pdfs" / "sample_minimal.pdf")
    finally:
        conv.build_document = that

    assert dem["n"] == 1
    assert kq.text_md
    assert kq.engine == "marker"
    # Chạy thật trên tài liệu thật phải ra vùng thật. Ba dòng dưới là cái đã bắt được
    # lỗi trường `page` của Marker (xem `page_index`): lượt chạy đầu tiên ra
    # `blocks == ()` với `error` báo thiếu trang, mà mọi test dùng dữ liệu giả vẫn xanh.
    assert kq.error is None
    assert kq.blocks, "chạy thật mà không ra block nào — số trang tra hỏng"
    assert all(0.0 <= b.box.x0 <= 1.0 and 0.0 <= b.box.y0 <= 1.0 for b in kq.blocks)
