"""Test cho `corpus.py` — A3 (TASK-074).

Chia hai nhóm. Nhóm đầu chạy trên dữ liệu **dựng tay** trong `tmp_path`: nó kiểm
*logic* nạp, chạy được ở mọi máy kể cả chưa tải bộ mẫu. Nhóm sau đánh dấu
`needs_corpus`, chạy trên 204+1403 file thật và tự bỏ qua nếu chưa có.

Ranh giới này quan trọng: nếu mọi test đều cần bộ mẫu thật (390 MB) thì CI sạch sẽ
xanh vì **skip hết**, và lỗi nạp nhãn sẽ đi thẳng vào bảng điểm.
"""

from __future__ import annotations

import json

import pytest

from ocr_bench.corpus import ROOT, COCO_BLOCK_TYPE, CorpusError, load_doclaynet, load_olmocr
from ocr_bench.types import (
    Baseline,
    BlockType,
    MathPresence,
    ReadingOrder,
    TableRelation,
    TextAbsence,
    TextPresence,
)

# --------------------------------------------------------------- dữ liệu dựng tay


def _dung_doclaynet(root, *, cells=True):
    gt = root / "ground-truth" / "doclaynet"
    (gt / "cells").mkdir(parents=True)
    coco = {
        "categories": [
            {"id": 1, "name": "Text"},
            {"id": 2, "name": "Picture"},
            {"id": 3, "name": "Section-header"},
            {"id": 4, "name": "Table"},
        ],
        "images": [
            {"id": 7, "width": 1025, "height": 1025, "file_name": "abc.png",
             "doc_category": "laws_and_regulations", "collection": "x", "page_no": 1,
             "doc_name": "d", "precedence": 0}
        ],
        "annotations": [
            {"id": 1, "image_id": 7, "category_id": 1, "bbox": [0, 0, 1025, 512.5]},
            {"id": 2, "image_id": 7, "category_id": 2, "bbox": [205, 205, 410, 410]},
            {"id": 3, "image_id": 7, "category_id": 3, "bbox": [0, 0, 100, 50]},
            {"id": 4, "image_id": 7, "category_id": 4, "bbox": [100, 600, 800, 300]},
        ],
    }
    (gt / "layout_coco.json").write_text(json.dumps(coco), encoding="utf-8")
    if cells:
        (gt / "cells" / "abc.json").write_text(
            json.dumps({
                "metadata": {"original_width": 612, "original_height": 792,
                             "coco_width": 1025, "coco_height": 1025},
                "cells": [],
            }),
            encoding="utf-8",
        )
    return root


def _dung_olmocr(root, dong):
    (root / "ground-truth" / "olmocr").mkdir(parents=True)
    (root / "pdfs" / "olmocr" / "tables").mkdir(parents=True)
    for d in dong:
        p = root / "pdfs" / "olmocr" / d["pdf"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"%PDF-1.4\n")
    (root / "ground-truth" / "olmocr" / "a.jsonl").write_text(
        "\n".join(json.dumps(d) for d in dong), encoding="utf-8"
    )
    return root


# ------------------------------------------------------------------- DocLayNet


def test_doclaynet_chuan_hoa_theo_khung_coco_khong_theo_trang_that(tmp_path):
    """Cái bẫy chính của AC-05.

    Hộp phủ nửa trên trang: bbox `[0,0,1025,512.5]` trong khung 1025×1025 → `y1=0.5`.
    Nếu ai đó chia nhầm cho `original_height=792` thì `y1` thành 0.647 rồi bị clamp —
    **không** ném lỗi, chỉ lệch. Nên phải kiểm bằng số, không kiểm bằng "không nổ".
    """
    gt = load_doclaynet(_dung_doclaynet(tmp_path))["abc"]
    hop = gt.blocks[0].box
    assert (hop.x0, hop.y0, hop.x1) == (0.0, 0.0, 1.0)
    assert hop.y1 == pytest.approx(0.5)


def test_doclaynet_y_huong_xuong(tmp_path):
    """Hộp ở đỉnh trang phải có `y0` nhỏ. Lật trục sẽ cho y0≈0.951 — đủ xa để bắt."""
    gt = load_doclaynet(_dung_doclaynet(tmp_path))["abc"]
    dinh = next(b for b in gt.blocks if b.block_type is BlockType.HEADING)
    assert dinh.box.y0 == pytest.approx(0.0)
    assert dinh.box.y1 == pytest.approx(50 / 1025)


def test_doclaynet_picture_vao_ca_blocks_lan_images(tmp_path):
    gt = load_doclaynet(_dung_doclaynet(tmp_path))["abc"]
    assert len(gt.blocks) == 4
    assert len(gt.images) == 1
    assert gt.images[0] == next(b.box for b in gt.blocks if b.block_type is BlockType.PICTURE)


def test_doclaynet_table_vao_ca_blocks_lan_tables(tmp_path):
    """Đối xứng với `Picture` ở trên — và đây là chỗ đã hỏng suốt.

    Loader đổ `Picture` vào cả `blocks` lẫn `images`, nhưng `Table` thì chỉ vào
    `blocks`. Hậu quả không phải một lỗi ném ra mà là hai con số sai lặng lẽ:
    `table_recall` trả `NO_GROUND_TRUTH` cho **toàn bộ** bộ mẫu (metric chết mà
    bảng vẫn đầy chữ "N/A" trông như engine không hỗ trợ), còn `cell_f1` rơi
    xuống `_compute()` với nhãn rỗng và trả đúng `0.000` cho mọi engine — một số
    đọc y hệt "engine nào cũng đọc sai bảng".
    """
    gt = load_doclaynet(_dung_doclaynet(tmp_path))["abc"]
    assert len(gt.tables) == 1
    assert gt.tables[0].box == next(
        b.box for b in gt.blocks if b.block_type is BlockType.TABLE
    )


def test_doclaynet_table_khong_bia_noi_dung_o(tmp_path):
    """DocLayNet chỉ có **khung** bảng, không có HTML ô.

    Điền `html` bằng bất cứ thứ gì khác `""` là bịa nhãn: `cell_f1`/`teds` sẽ chấm
    engine theo một bảng không ai gán. Rỗng ⇒ hai metric đó trả `NO_GROUND_TRUTH`,
    còn `table_recall` — vốn chỉ cần khung — chấm được.
    """
    gt = load_doclaynet(_dung_doclaynet(tmp_path))["abc"]
    assert gt.tables[0].html == ""


def test_doclaynet_page_sizes_lay_kich_thuoc_trang_that(tmp_path):
    """`page_sizes` là điểm PDF (612×792), **không** phải khung 1025 — hai con số
    khác nhau và chỉ cái đầu cho biết engine đang báo toạ độ trên trang bao nhiêu điểm."""
    gt = load_doclaynet(_dung_doclaynet(tmp_path))["abc"]
    assert gt.page_sizes == ((612.0, 792.0),)


def test_doclaynet_thieu_file_cells_van_nap_duoc(tmp_path):
    gt = load_doclaynet(_dung_doclaynet(tmp_path, cells=False))["abc"]
    assert gt.page_sizes == ((1025.0, 1025.0),)
    assert len(gt.blocks) == 4


def test_doclaynet_text_de_None(tmp_path):
    """Cell theo thứ tự nội dung PDF, không phải thứ tự đọc — nối lại rồi gọi là văn
    bản tham chiếu sẽ phạt oan chính engine sắp đúng thứ tự đọc."""
    assert load_doclaynet(_dung_doclaynet(tmp_path))["abc"].text is None


def test_doclaynet_thieu_coco_thi_no_chu_khong_tra_rong(tmp_path):
    with pytest.raises(CorpusError, match="fetch_doclaynet"):
        load_doclaynet(tmp_path)


def test_moi_lop_doclaynet_deu_co_anh_xa():
    """11 lớp của DocLayNet phải map hết. Thiếu một lớp thì nó rơi vào `OTHER` và
    im lặng biến mất khỏi mọi metric theo lớp."""
    assert len(COCO_BLOCK_TYPE) == 11
    assert BlockType.OTHER not in COCO_BLOCK_TYPE.values()


# ------------------------------------------------------------------ olmOCR-bench


def test_olmocr_page_doi_ve_0_based(tmp_path):
    """Nguồn đánh 1-based, bench quy ước 0-based (quy tắc 2). Quên trừ 1 thì mọi
    khẳng định trỏ sang trang sau — trên bộ này toàn PDF 1 trang nên **không có gì
    nổ**, chỉ ra điểm 0 ở khắp nơi."""
    root = _dung_olmocr(tmp_path, [
        {"pdf": "tables/x.pdf", "page": 1, "id": "i1", "type": "present",
         "text": "a", "max_diffs": 0, "case_sensitive": True, "first_n": None, "last_n": None},
    ])
    assert load_olmocr(root)["x"].tests[0].page == 0


@pytest.mark.parametrize(
    "dong, lop, kiem",
    [
        ({"type": "present", "text": "a", "case_sensitive": True, "first_n": 200, "last_n": None},
         TextPresence, lambda t: t.case_sensitive is True and t.first_n == 200),
        ({"type": "absent", "text": "b", "case_sensitive": False, "first_n": None, "last_n": 50},
         TextAbsence, lambda t: t.case_sensitive is False and t.last_n == 50),
        ({"type": "order", "before": "p", "after": "q"},
         ReadingOrder, lambda t: (t.before, t.after) == ("p", "q")),
        ({"type": "math", "math": r"\frac{1}{2}"},
         MathPresence, lambda t: t.latex == r"\frac{1}{2}"),
        ({"type": "table", "cell": "0.5", "up": None, "down": None, "left": None,
          "right": "R", "top_heading": None, "left_heading": "BO"},
         TableRelation, lambda t: t.right == "R" and t.left_heading == "BO" and t.up is None),
        ({"type": "baseline", "check_disallowed_characters": True},
         Baseline, lambda t: t.check_disallowed_characters is True),
    ],
)
def test_olmocr_nap_du_sau_loai(tmp_path, dong, lop, kiem):
    """Sáu loại, không phải ba.

    `types.py` ban đầu chỉ có present/absent/order — đúng **2.605/7.019** khẳng định.
    Nạp theo bản đó sẽ vứt lặng lẽ 63% bộ nhãn, và B5 vẫn in ra một bảng trông bình
    thường. Mỗi loại mới phải có test riêng, không gộp.
    """
    root = _dung_olmocr(tmp_path, [{"pdf": "tables/x.pdf", "page": 1, "id": "i", "max_diffs": 3, **dong}])
    t = load_olmocr(root)["x"].tests[0]
    assert isinstance(t, lop)
    assert t.max_diffs == 3 and t.assertion_id == "i"
    assert kiem(t)


def test_olmocr_gom_nhieu_khang_dinh_cua_mot_pdf(tmp_path):
    root = _dung_olmocr(tmp_path, [
        {"pdf": "tables/x.pdf", "page": 1, "id": "a", "type": "math", "math": "x"},
        {"pdf": "tables/x.pdf", "page": 1, "id": "b", "type": "math", "math": "y"},
        {"pdf": "tables/y.pdf", "page": 1, "id": "c", "type": "math", "math": "z"},
    ])
    ra = load_olmocr(root)
    assert sorted(ra) == ["x", "y"]
    assert len(ra["x"].tests) == 2


def test_olmocr_loai_la_thi_no_chu_khong_bo_qua(tmp_path):
    """Thượng nguồn thêm loại mới là chuyện sẽ xảy ra. Bỏ qua im lặng nghĩa là bộ
    nhãn teo dần qua từng lần cập nhật mà không ai thấy."""
    root = _dung_olmocr(tmp_path, [{"pdf": "tables/x.pdf", "page": 1, "id": "i", "type": "chart_qa"}])
    with pytest.raises(CorpusError, match="chart_qa"):
        load_olmocr(root)


def test_olmocr_thieu_pdf_thi_no(tmp_path):
    root = _dung_olmocr(tmp_path, [{"pdf": "tables/x.pdf", "page": 1, "id": "i", "type": "math", "math": "x"}])
    (root / "pdfs" / "olmocr" / "tables" / "x.pdf").unlink()
    with pytest.raises(CorpusError, match="không có trên đĩa"):
        load_olmocr(root)


def test_olmocr_thieu_thu_muc_thi_no(tmp_path):
    with pytest.raises(CorpusError, match="fetch_olmocr"):
        load_olmocr(tmp_path)


def test_olmocr_jsonl_rong_thi_no(tmp_path):
    """File jsonl có mặt nhưng rỗng (tải đứt giữa chừng) — trả `{}` ở đây sẽ hoá thành
    N/A ở toàn bảng, trông y hệt "engine không hỗ trợ" chứ không giống "thiếu dữ liệu"."""
    root = _dung_olmocr(tmp_path, [])
    (root / "ground-truth" / "olmocr" / "a.jsonl").write_text("\n \n", encoding="utf-8")
    with pytest.raises(CorpusError, match="không có khẳng định nào"):
        load_olmocr(root)


def test_doclaynet_coco_rong_thi_no(tmp_path):
    root = _dung_doclaynet(tmp_path)
    p = root / "ground-truth" / "doclaynet" / "layout_coco.json"
    coco = json.loads(p.read_text(encoding="utf-8"))
    coco["images"] = []
    p.write_text(json.dumps(coco), encoding="utf-8")
    with pytest.raises(CorpusError, match="không có ảnh nào"):
        load_doclaynet(root)


# ------------------------------------------------------- fixes.json (sửa nhãn tay)


def _ghi_fixes(root, muc: list[dict]):
    (root / "ground-truth" / "doclaynet" / "fixes.json").write_text(
        json.dumps({"fixes": muc}, ensure_ascii=False), encoding="utf-8"
    )


def _muc_hop_le(**thay):
    m = {
        "doc_id": "abc",
        "hanh_dong": "them",
        "lop": "Picture",
        "hop_diem_pdf": {"x0": 61.2, "y0": 396.0, "x1": 306.0, "y1": 792.0,
                         "page_width": 612.0, "page_height": 792.0, "y_axis": "up"},
        "ly_do": "test",
        "bang_chung": ["test"],
    }
    m.update(thay)
    return m


def test_fixes_thieu_file_thi_khong_doi_gi(tmp_path):
    """Không có `fixes.json` là trạng thái bình thường của mọi bộ nhãn chưa sửa tay."""
    ra = load_doclaynet(_dung_doclaynet(tmp_path))
    assert len(ra["abc"].blocks) == 4
    assert len(ra["abc"].images) == 1


def test_fixes_them_nhan_anh_vao_ca_blocks_lan_images(tmp_path):
    """`img_f1` đọc `.images`, các metric khác đọc `.blocks` — thiếu một bên là nhãn
    thêm vào chỉ có tác dụng với nửa số metric, mà nửa nào thì không ai biết."""
    _dung_doclaynet(tmp_path)
    _ghi_fixes(tmp_path, [_muc_hop_le()])
    g = load_doclaynet(tmp_path)["abc"]
    assert len(g.blocks) == 5
    assert len(g.images) == 2
    them = g.images[-1]
    # y_axis="up": y0=396 (nửa dưới theo PDF) → y1=0.5 theo hệ top-down của Box.
    assert (round(them.x0, 3), round(them.y0, 3)) == (0.1, 0.0)
    assert (round(them.x1, 3), round(them.y1, 3)) == (0.5, 0.5)


def test_fixes_lop_khong_phai_anh_thi_khong_chui_vao_images(tmp_path):
    _dung_doclaynet(tmp_path)
    _ghi_fixes(tmp_path, [_muc_hop_le(lop="Text")])
    g = load_doclaynet(tmp_path)["abc"]
    assert len(g.blocks) == 5 and len(g.images) == 1


@pytest.mark.parametrize(
    "thay, khop",
    [
        ({"bang_chung": []}, "bang_chung"),
        ({"lop": "Khong-Co-Lop-Nay"}, "không có trong COCO_BLOCK_TYPE"),
        ({"hanh_dong": "xoa"}, "chưa được hỗ trợ"),
    ],
)
def test_fixes_muc_hong_thi_nem_chu_khong_bo_qua(tmp_path, thay, khop):
    """Một mục sửa nhãn bị bỏ qua lặng lẽ là kiểu hỏng tệ nhất ở đây: người viết tin
    là đã sửa, bảng điểm thì vẫn chấm bằng nhãn cũ."""
    _dung_doclaynet(tmp_path)
    _ghi_fixes(tmp_path, [_muc_hop_le(**thay)])
    with pytest.raises(CorpusError, match=khop):
        load_doclaynet(tmp_path)


def test_fixes_tro_vao_tai_lieu_khong_ton_tai_thi_nem(tmp_path):
    """Gõ nhầm `doc_id` cho ra một mục nhìn như đã có hiệu lực mà không sửa gì cả."""
    _dung_doclaynet(tmp_path)
    _ghi_fixes(tmp_path, [_muc_hop_le(doc_id="khong-co-tai-lieu-nay")])
    with pytest.raises(CorpusError, match="khong-co-tai-lieu-nay"):
        load_doclaynet(tmp_path)


# ------------------------------------------------------------- bộ mẫu thật


@pytest.mark.needs_corpus
def test_bo_mau_that_nap_du_khong_mat_mat():
    """Con số chốt của A3. Lệch là bộ mẫu trên đĩa đã đổi — kiểm lại trước khi sửa test.

    2941 → 2942 ở TASK-088: `ground-truth/doclaynet/fixes.json` thêm 1 nhãn `Picture`
    (logo ENISA ở `14654fbc…`, bằng chứng lấy từ content stream PDF). Đây là **cách
    duy nhất** một mục trong `fixes.json` phải khai báo mình ra ngoài — sửa nhãn làm
    đổi số công bố, nên nó phải làm đỏ một test chứ không được lẳng lặng trôi qua.
    """
    dl, olm = load_doclaynet(), load_olmocr()
    assert len(dl) == 204
    assert sum(len(v.blocks) for v in dl.values()) == 2942
    assert len(olm) == 1403
    assert sum(len(v.tests) for v in olm.values()) == 7019


@pytest.mark.needs_corpus
def test_bo_mau_that_khong_dung_khoa():
    """Hai bộ trộn chung một dict `{doc_id: GroundTruth}`. Trùng khoá thì một bộ ăn
    mất nhãn của bộ kia, và loại nhãn sai sẽ ra N/A chứ không ra lỗi."""
    assert not (set(load_doclaynet()) & set(load_olmocr()))


@pytest.mark.needs_corpus
def test_manifest_va_corpus_noi_ve_cung_mot_bo_tai_lieu():
    """`datasets/manifest.json` và các loader phải mô tả **cùng** một bộ đĩa.

    Hai đường đọc độc lập trên cùng dữ liệu là chỗ trôi rất êm: manifest ghi 1606 tài
    liệu trong khi loader nạp 1607 thì báo cáo dẫn nguồn cho một con số được tính trên
    tập khác. Ràng buộc ở đây khoá đúng một chiều: mọi dòng manifest phải có nhãn nạp
    được, và mọi tài liệu bị manifest loại ra phải thật sự **không có nhãn nào** —
    loại một trang có nhãn ra khỏi bảng là tự chọn mẫu.
    """
    from ocr_bench.dataset_manifest import build_manifest

    manifest = build_manifest(ROOT)
    dl, olm = load_doclaynet(), load_olmocr()
    nhan = {**{k: len(v.blocks) for k, v in dl.items()}, **{k: len(v.tests) for k, v in olm.items()}}

    thieu = [r["document_id"] for r in manifest["documents"] if r["document_id"] not in nhan]
    assert not thieu, f"manifest có dòng mà loader không nạp được nhãn: {thieu[:5]}"

    for r in manifest["excluded_documents"]:
        assert nhan.get(r["document_id"], 0) == 0, (
            f"{r['document_id']} bị manifest loại vì {r['reason']!r} nhưng loader vẫn "
            f"nạp được nhãn cho nó — loại một trang có nhãn là tự chọn mẫu"
        )


@pytest.mark.needs_corpus
def test_manifest_da_dung_bo_nhip_voi_dia():
    """Manifest đã commit phải còn khớp đĩa — chính là cổng `--verify`, chạy trong suite.

    Không có nó thì `datasets/manifest.json` chỉ đúng vào ngày ai đó nhớ chạy script.
    """
    import json as _json

    from ocr_bench.dataset_manifest import build_manifest

    da_commit = _json.loads((ROOT / "datasets" / "manifest.json").read_text(encoding="utf-8"))
    assert da_commit == build_manifest(ROOT), (
        "datasets/manifest.json lệch đĩa — chạy py -3 scripts/build_dataset_manifest.py"
    )
