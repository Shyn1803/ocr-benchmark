"""Nạp bộ mẫu trên đĩa thành ground truth của bench — A3 (TASK-074).

    from ocr_bench.corpus import load_doclaynet, load_olmocr
    gt = load_doclaynet() | load_olmocr()      # {doc_id: AnnotationGT | AssertionGT}

Khoá của cả hai hàm là **stem của file PDF**, khớp cách `scorer.run_bench` tra nhãn
(`ground_truth[doc.stem]`). Hai bộ không đụng tên nhau: DocLayNet dùng hash SHA, olmOCR
dùng tên gốc.

## Hai bộ, hai loại nhãn — cố tình

| Bộ | Kiểu | Trả lời được câu hỏi |
|---|---|---|
| DocLayNet | `AnnotationGT` | hộp bố cục có nhãn → IoU/mAP (B3) |
| olmOCR-bench | `AssertionGT` | 7.019 khẳng định đúng/sai trên văn bản trích ra (B5) |

DocLayNet **không** cho văn bản tham chiếu theo thứ tự đọc, olmOCR **không** cho bbox.
Ép một bộ làm việc của bộ kia sẽ ra số nhìn thì đẹp mà vô nghĩa.

## Vì sao `text=None` cho DocLayNet

`cells` trong `JSON/<hash>.json` là text cell theo **thứ tự nội dung của PDF**, không
phải thứ tự đọc của người. Nối chúng lại rồi gọi là "văn bản tham chiếu" sẽ phạt oan
đúng những engine sắp lại thứ tự đọc cho đúng — tức là phạt cái đáng thưởng. CER/WER
lấy từ khẳng định `present` của olmOCR.

## Toạ độ DocLayNet (AC-05, đã kiểm bằng dữ liệu chứ không bằng suy đoán)

Nhãn COCO và text cell ở **cùng một hệ**: 1025×1025, gốc trên-trái, y hướng xuống,
`bbox = [x, y, w, h]`. Đó **không phải** aspect-fit có viền đệm mà là **kéo giãn riêng
từng trục** (x nhân `1025/original_width`, y nhân `1025/original_height`). Nên chuẩn hoá
phải chia cho `coco_width`/`coco_height`, tuyệt đối không chia cho kích thước trang thật.
Bằng chứng + cách kiểm lại: `ground-truth/doclaynet/README.md`.
"""

from __future__ import annotations

import json
from pathlib import Path

from .types import (
    AnnotationGT,
    Assertion,
    AssertionGT,
    Baseline,
    BlockType,
    Box,
    MathPresence,
    OcrBlock,
    OcrTable,
    ReadingOrder,
    TableRelation,
    TextAbsence,
    TextPresence,
)

ROOT = Path(__file__).resolve().parents[2]

# DocLayNet đặt tên lớp theo cách của nó; bench có từ điển riêng. Ánh xạ nằm ở đây,
# không nằm trong metric — metric không được biết chuỗi "Section-header" tồn tại.
COCO_BLOCK_TYPE: dict[str, BlockType] = {
    "Caption": BlockType.CAPTION,
    "Footnote": BlockType.FOOTNOTE,
    "Formula": BlockType.FORMULA,
    "List-item": BlockType.LIST,
    "Page-footer": BlockType.PAGE_FOOTER,
    "Page-header": BlockType.PAGE_HEADER,
    "Picture": BlockType.PICTURE,
    "Section-header": BlockType.HEADING,
    "Table": BlockType.TABLE,
    "Text": BlockType.TEXT,
    "Title": BlockType.TITLE,
}


class CorpusError(RuntimeError):
    """Bộ mẫu thiếu hoặc hỏng. Ném ra chứ không trả rỗng: một `{}` lặng lẽ sẽ biến
    thành `NAReason.NO_GROUND_TRUTH` ở khắp bảng, trông y hệt "engine không hỗ trợ"."""


# --------------------------------------------------------------------- DocLayNet

TEN_FILE_FIXES = "fixes.json"


def doc_fixes(gt_dir: Path) -> dict[str, list[tuple[BlockType, Box]]]:
    """`fixes.json` → `{doc_id: [(loại, hộp)]}` — nhãn thêm tay, có lý do ghi kèm.

    Vì sao là overlay chứ không sửa thẳng `layout_coco.json`: file đó là **đầu ra**
    của `scripts/fetch_doclaynet.py`; chạy lại script là mọi sửa tay biến mất mà
    không có tín hiệu nào. Overlay nằm ngoài đường sinh đó nên sống sót, và diff của
    nó đọc được — diff của một file COCO 1,5 MB thì không.

    Thiếu file thì trả `{}`: bộ mẫu chưa sửa gì là trạng thái hợp lệ. Nhưng file
    **có** mà nội dung sai (doc_id lạ, lớp lạ, hành động lạ) thì ném — một mục sửa
    lặng lẽ không có tác dụng là kiểu hỏng tệ nhất ở đây: người viết tin là đã sửa.
    """
    p = gt_dir / TEN_FILE_FIXES
    if not p.exists():
        return {}
    du_lieu = json.loads(p.read_text(encoding="utf-8"))
    ra: dict[str, list[tuple[BlockType, Box]]] = {}
    for i, f in enumerate(du_lieu.get("fixes", ())):
        if f.get("hanh_dong") != "them":
            raise CorpusError(
                f"{p} mục {i}: hành động {f.get('hanh_dong')!r} chưa được hỗ trợ "
                "(mới chỉ có 'them')"
            )
        if f["lop"] not in COCO_BLOCK_TYPE:
            raise CorpusError(f"{p} mục {i}: lớp {f['lop']!r} không có trong COCO_BLOCK_TYPE")
        if not f.get("bang_chung"):
            raise CorpusError(
                f"{p} mục {i}: thiếu `bang_chung`. Sửa nhãn làm đổi số công bố; "
                "không có bằng chứng thì không phân biệt được với sửa cho bảng đẹp lên."
            )
        h = f["hop_diem_pdf"]
        ra.setdefault(f["doc_id"], []).append(
            (
                COCO_BLOCK_TYPE[f["lop"]],
                Box.from_absolute(
                    page=int(f.get("page", 0)),
                    x0=h["x0"],
                    y0=h["y0"],
                    x1=h["x1"],
                    y1=h["y1"],
                    page_width=h["page_width"],
                    page_height=h["page_height"],
                    y_axis=h["y_axis"],
                ),
            )
        )
    return ra


def load_doclaynet(root: Path | None = None) -> dict[str, AnnotationGT]:
    """`ground-truth/doclaynet/` → `{hash: AnnotationGT}`.

    Mỗi PDF của DocLayNet là **một trang**, nên mọi `Box` đều `page=0`.

    Ô `Table` vào `tables` với `html=""`: DocLayNet gán **khung** bảng chứ không gán
    nội dung ô. Rỗng là câu trả lời đúng — `teds` và `cell_f1` lọc bảng không có ô
    rồi trả `NO_GROUND_TRUTH`, còn `table_recall` chỉ cần khung nên chấm được. Bỏ
    trống cả trường này (như trước 2026-08-17) thì `table_recall` chết lặng ở
    `NO_GROUND_TRUTH` toàn bộ mẫu, và `cell_f1` tệ hơn: nhãn rỗng lọt xuống
    `_compute()` và trả `0.000` cho mọi engine — một con số, không phải một N/A.
    """
    gt_dir = (root or ROOT) / "ground-truth" / "doclaynet"
    coco_path = gt_dir / "layout_coco.json"
    if not coco_path.exists():
        raise CorpusError(f"thiếu {coco_path} — chạy `py -3 scripts/fetch_doclaynet.py`")

    coco = json.loads(coco_path.read_text(encoding="utf-8"))
    ten_lop = {c["id"]: c["name"] for c in coco["categories"]}
    fixes = doc_fixes(gt_dir)

    theo_anh: dict[int, list[dict]] = {}
    for a in coco["annotations"]:
        theo_anh.setdefault(a["image_id"], []).append(a)

    ra: dict[str, AnnotationGT] = {}
    for im in coco["images"]:
        doc_id = Path(im["file_name"]).stem
        # `width`/`height` trong COCO chính là hệ 1025×1025 mà bbox sống trong đó.
        cw, ch = float(im["width"]), float(im["height"])

        blocks: list[OcrBlock] = []
        images: list[Box] = []
        tables: list[OcrTable] = []
        for a in sorted(theo_anh.get(im["id"], ()), key=lambda a: a["id"]):
            x, y, w, h = a["bbox"]
            box = Box.from_absolute(
                page=0,
                x0=x,
                y0=y,
                x1=x + w,
                y1=y + h,
                page_width=cw,
                page_height=ch,
                y_axis="down",
            )
            loai = COCO_BLOCK_TYPE.get(ten_lop[a["category_id"]], BlockType.OTHER)
            blocks.append(OcrBlock(block_type=loai, box=box))
            if loai is BlockType.PICTURE:
                images.append(box)
            elif loai is BlockType.TABLE:
                tables.append(OcrTable(html="", box=box))

        for loai, box in fixes.pop(doc_id, ()):
            blocks.append(OcrBlock(block_type=loai, box=box))
            if loai is BlockType.PICTURE:
                images.append(box)
            elif loai is BlockType.TABLE:
                tables.append(OcrTable(html="", box=box))

        # Kích thước trang thật (điểm PDF) nằm ở metadata của file cell, không ở COCO.
        # Box đã chuẩn hoá nên đây chỉ là thông tin, nhưng thiếu nó thì không ai suy
        # ngược ra được engine đang báo toạ độ trên trang bao nhiêu điểm.
        cell_path = gt_dir / "cells" / f"{doc_id}.json"
        if cell_path.exists():
            md = json.loads(cell_path.read_text(encoding="utf-8"))["metadata"]
            kich_thuoc = (float(md["original_width"]), float(md["original_height"]))
        else:
            kich_thuoc = (cw, ch)

        ra[doc_id] = AnnotationGT(
            doc_id=doc_id,
            text=None,  # xem docstring module
            blocks=tuple(blocks),
            images=tuple(images),
            tables=tuple(tables),
            page_sizes=(kich_thuoc,),
        )

    if not ra:
        raise CorpusError(f"{coco_path} không có ảnh nào")
    if fixes:
        # `pop` ở trên đã rút hết mục dùng được; còn lại là mục trỏ vào tài liệu
        # không có trong bộ mẫu. Bỏ qua sẽ để lại một mục sửa nhìn như đã có hiệu lực.
        raise CorpusError(
            f"{gt_dir / TEN_FILE_FIXES}: {sorted(fixes)} không có trong {coco_path.name}"
        )
    return ra


# -------------------------------------------------------------------- olmOCR-bench


def _mot_khang_dinh(d: dict) -> Assertion:
    """Một dòng jsonl → `Assertion`.

    `page` ở nguồn là **1-based**; bench quy ước 0-based (quy tắc 2). Trừ 1 ở đúng
    chỗ này để không chỗ nào khác phải nhớ.
    """
    chung = {
        "assertion_id": d.get("id"),
        "page": max(0, int(d.get("page", 1)) - 1),
        "max_diffs": int(d.get("max_diffs") or 0),
        "checked": d.get("checked"),
    }
    loai = d["type"]

    if loai in ("present", "absent"):
        lop = TextPresence if loai == "present" else TextAbsence
        return lop(
            **chung,
            needle=d["text"],
            case_sensitive=bool(d.get("case_sensitive", False)),
            first_n=d.get("first_n"),
            last_n=d.get("last_n"),
        )
    if loai == "order":
        return ReadingOrder(**chung, before=d["before"], after=d["after"])
    if loai == "math":
        return MathPresence(**chung, latex=d["math"])
    if loai == "table":
        return TableRelation(
            **chung,
            cell=d["cell"],
            up=d.get("up"),
            down=d.get("down"),
            left=d.get("left"),
            right=d.get("right"),
            top_heading=d.get("top_heading"),
            left_heading=d.get("left_heading"),
        )
    if loai == "baseline":
        return Baseline(
            **chung,
            check_disallowed_characters=bool(d.get("check_disallowed_characters", False)),
        )
    raise CorpusError(
        f"loại khẳng định lạ: {loai!r} (id={d.get('id')}). Bộ nhãn thượng nguồn đã thêm "
        "loại mới — bổ sung lớp trong types.py rồi map ở đây, đừng bỏ qua im lặng."
    )


def load_olmocr(root: Path | None = None) -> dict[str, AssertionGT]:
    """`ground-truth/olmocr/*.jsonl` → `{stem: AssertionGT}`.

    Gộp theo file PDF: một PDF thường mang nhiều khẳng định thuộc nhiều loại.
    Bỏ qua khẳng định trỏ tới PDF không có trên đĩa, và **báo ra** — im lặng ở đây
    nghĩa là bộ mẫu tải thiếu mà bảng điểm vẫn in ra bình thường.
    """
    base = root or ROOT
    gt_dir = base / "ground-truth" / "olmocr"
    pdf_dir = base / "pdfs" / "olmocr"
    if not gt_dir.is_dir():
        raise CorpusError(f"thiếu {gt_dir} — chạy `py -3 scripts/fetch_olmocr.py`")

    gom: dict[str, list[Assertion]] = {}
    thieu: set[str] = set()
    for f in sorted(gt_dir.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            rel = Path(d["pdf"])
            if not (pdf_dir / rel).exists():
                thieu.add(d["pdf"])
                continue
            gom.setdefault(rel.stem, []).append(_mot_khang_dinh(d))

    if thieu:
        raise CorpusError(
            f"{len(thieu)} PDF được khẳng định trỏ tới nhưng không có trên đĩa "
            f"(vd {sorted(thieu)[0]}). Chạy `py -3 scripts/fetch_olmocr.py`."
        )
    if not gom:
        raise CorpusError(f"{gt_dir} không có khẳng định nào")

    return {k: AssertionGT(doc_id=k, tests=tuple(v)) for k, v in sorted(gom.items())}
