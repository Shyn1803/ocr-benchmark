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


def load_doclaynet(root: Path | None = None) -> dict[str, AnnotationGT]:
    """`ground-truth/doclaynet/` → `{hash: AnnotationGT}`.

    Mỗi PDF của DocLayNet là **một trang**, nên mọi `Box` đều `page=0`.
    """
    gt_dir = (root or ROOT) / "ground-truth" / "doclaynet"
    coco_path = gt_dir / "layout_coco.json"
    if not coco_path.exists():
        raise CorpusError(f"thiếu {coco_path} — chạy `py -3 scripts/fetch_doclaynet.py`")

    coco = json.loads(coco_path.read_text(encoding="utf-8"))
    ten_lop = {c["id"]: c["name"] for c in coco["categories"]}

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
            page_sizes=(kich_thuoc,),
        )

    if not ra:
        raise CorpusError(f"{coco_path} không có ảnh nào")
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
