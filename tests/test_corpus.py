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

from ocr_bench.corpus import COCO_BLOCK_TYPE, CorpusError, load_doclaynet, load_olmocr
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
    assert len(gt.blocks) == 3
    assert len(gt.images) == 1
    assert gt.images[0] == next(b.box for b in gt.blocks if b.block_type is BlockType.PICTURE)


def test_doclaynet_page_sizes_lay_kich_thuoc_trang_that(tmp_path):
    """`page_sizes` là điểm PDF (612×792), **không** phải khung 1025 — hai con số
    khác nhau và chỉ cái đầu cho biết engine đang báo toạ độ trên trang bao nhiêu điểm."""
    gt = load_doclaynet(_dung_doclaynet(tmp_path))["abc"]
    assert gt.page_sizes == ((612.0, 792.0),)


def test_doclaynet_thieu_file_cells_van_nap_duoc(tmp_path):
    gt = load_doclaynet(_dung_doclaynet(tmp_path, cells=False))["abc"]
    assert gt.page_sizes == ((1025.0, 1025.0),)
    assert len(gt.blocks) == 3


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


# ------------------------------------------------------------- bộ mẫu thật


@pytest.mark.needs_corpus
def test_bo_mau_that_nap_du_khong_mat_mat():
    """Con số chốt của A3. Lệch là bộ mẫu trên đĩa đã đổi — kiểm lại trước khi sửa test."""
    dl, olm = load_doclaynet(), load_olmocr()
    assert len(dl) == 204
    assert sum(len(v.blocks) for v in dl.values()) == 2941
    assert len(olm) == 1403
    assert sum(len(v.tests) for v in olm.values()) == 7019


@pytest.mark.needs_corpus
def test_bo_mau_that_khong_dung_khoa():
    """Hai bộ trộn chung một dict `{doc_id: GroundTruth}`. Trùng khoá thì một bộ ăn
    mất nhãn của bộ kia, và loại nhãn sai sẽ ra N/A chứ không ra lỗi."""
    assert not (set(load_doclaynet()) & set(load_olmocr()))
