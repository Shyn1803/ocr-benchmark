"""So ba bộ phán "tài liệu này có cần OCR không" trên cùng một bộ mẫu — A6 (TASK-077).

Ba bộ phán:

1. `pdf_inspector.classify_pdf()`             — `pdf_type` ∈ {text_based, scanned, image_based}
2. `pdf_inspector.extract_pages_markdown()`   — `PageMarkdown.needs_ocr` của **cùng thư viện**
3. `_needs_vision_fallback()` của Sovereign   — chép lại quy tắc, xem mục "Chép, không gọi"

Không có "đáp án đúng" ở đây. Không bộ nào là ground truth: DocLayNet gán nhãn *bố cục*,
không gán nhãn "trang này có text layer hay không". Nên script này **báo cáo bất đồng**,
tách theo `doc_category`, chứ không xếp hạng thắng thua. A0 phát hiện mâu thuẫn trên
**n=1**; đây là chỗ đưa n lên 204.

## Chép, không gọi (AC-05)

`_needs_vision_fallback()` sống trong `app/services/openrouter_document_parser.py` của BE.
Không import được: nó `from app.services.marker_ocr_service import IMAGE_EXTENSIONS`, kéo
theo cả cây phụ thuộc của BE. Nên quy tắc PDF được **chép lại** ở `sovereign_can_ocr()`.

Chép là nợ: bản chép trôi lệch khỏi bản gốc mà không ai biết. Trả nợ bằng
`kiem_nguong_con_khop()` — đọc thẳng file BE, khẳng định dòng quyết định vẫn nguyên văn.
BE **chỉ được đọc**; task này không sửa heuristic sản xuất.

Chạy:
    .venv-pi/Scripts/python.exe scripts/compare_scan_label.py --bo doclaynet
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BE = (
    ROOT.parent
    / "adminPortal/back-end-admin-portal/app/services/openrouter_document_parser.py"
)

# Nguyên văn dòng quyết định trong BE, tính tới 2026-08-06.
DONG_QUYET_DINH = "needs = chars_per_page < 50 or len(text) < 100"
NGUONG_CHARS_PER_PAGE = 50
NGUONG_TONG_KY_TU = 100


def kiem_nguong_con_khop() -> str:
    """Khẳng định bản chép chưa trôi lệch khỏi BE. Ném nếu lệch."""
    if not BE.is_file():
        return f"BỎ QUA — không thấy file BE tại {BE}"
    nguon = BE.read_text(encoding="utf-8", errors="replace")
    if DONG_QUYET_DINH not in nguon:
        thay = re.findall(r"^\s*needs = .*$", nguon, re.M)
        raise SystemExit(
            "Quy tắc BE đã đổi — bản chép trong script này không còn đúng.\n"
            f"  mong đợi: {DONG_QUYET_DINH}\n"
            f"  thấy    : {thay or '(không thấy dòng nào)'}\n"
            "Sửa hằng số ở đầu file rồi chạy lại. ĐỪNG sửa file BE."
        )
    return f"khớp — {BE.name}: `{DONG_QUYET_DINH}`"


def sovereign_can_ocr(pdf: Path) -> tuple[bool, float, int, int]:
    """Chép quy tắc PDF của `_needs_vision_fallback()`. Trả (cần_ocr, cpp, len, trang).

    Giữ nguyên cả những chi tiết dễ bỏ sót của bản gốc: `max(page_count, 1)` và
    `.strip()` trước khi đếm — đổi một trong hai là ra số khác ở tài liệu biên.
    """
    import fitz  # noqa: PLC0415  # PyMuPDF, đúng thư viện BE dùng

    with fitz.open(str(pdf)) as doc:
        so_trang = max(doc.page_count, 1)
        text = "\n".join(t.get_text() for t in doc).strip()
    cpp = len(text) / so_trang
    can = cpp < NGUONG_CHARS_PER_PAGE or len(text) < NGUONG_TONG_KY_TU
    return can, cpp, len(text), so_trang


def loai_tai_lieu(bo: str) -> dict[str, str]:
    """doc_id → doc_category. DocLayNet mới có; bộ khác trả rỗng."""
    coco = ROOT / "ground-truth" / bo / "layout_coco.json"
    if not coco.is_file():
        return {}
    d = json.loads(coco.read_text(encoding="utf-8"))
    return {
        Path(im["file_name"]).stem: im.get("doc_category", "?") for im in d["images"]
    }


def bang(tieu_de: str, dem: Counter, tong: int) -> str:
    dong = [f"### {tieu_de}", "", "| Giá trị | Số | % |", "|---|---:|---:|"]
    for k, v in dem.most_common():
        dong.append(f"| {k} | {v} | {100 * v / tong:.1f}% |")
    return "\n".join(dong)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bo", default="doclaynet", help="tên bộ trong pdfs/")
    ap.add_argument("--gioi-han", type=int, default=0, help="0 = chạy hết")
    ap.add_argument("--out", type=Path, default=ROOT / "results/scan_label_compare.md")
    a = ap.parse_args()

    import pdf_inspector as pi  # noqa: PLC0415

    sys.path.insert(0, str(ROOT / "src"))
    from ocr_bench.adapters.pdf_inspector import nhan_tu_classify, nhan_tu_pages

    thu_muc = ROOT / "pdfs" / a.bo
    files = sorted(thu_muc.glob("*.pdf"))
    if a.gioi_han:
        files = files[: a.gioi_han]
    if not files:
        raise SystemExit(f"không thấy PDF nào trong {thu_muc}")

    kiem = kiem_nguong_con_khop()
    print(f"Ngưỡng Sovereign: {kiem}")

    loai = loai_tai_lieu(a.bo)
    dem_type: Counter[str] = Counter()
    dem_bo_ba: Counter[str] = Counter()
    theo_loai: dict[str, Counter[str]] = defaultdict(Counter)
    hong: list[tuple[str, str]] = []
    chi_tiet: list[dict[str, object]] = []

    for i, pdf in enumerate(files, 1):
        try:
            c = pi.classify_pdf(str(pdf))
            p = pi.extract_pages_markdown(str(pdf))
            A = nhan_tu_classify(c)
            B = nhan_tu_pages(p)
            S, cpp, n_ky_tu, n_trang = sovereign_can_ocr(pdf)
        except Exception as e:  # noqa: BLE001 — báo cáo, không đổ cả lượt chạy
            hong.append((pdf.stem[:12], f"{type(e).__name__}: {e}"))
            continue

        dem_type[c.pdf_type] += 1
        ma = f"classify={int(A.is_scanned)} pages={int(B.is_scanned)} sovereign={int(S)}"
        dem_bo_ba[ma] += 1
        theo_loai[loai.get(pdf.stem, "?")][ma] += 1
        chi_tiet.append(
            {
                "doc": pdf.stem[:12],
                "loai": loai.get(pdf.stem, "?"),
                "pdf_type": c.pdf_type,
                "conf": A.confidence,
                "classify": A.is_scanned,
                "pages": B.is_scanned,
                "sovereign": S,
                "chars_per_page": round(cpp, 1),
                "text_len": n_ky_tu,
                "page_count": n_trang,
            }
        )
        if i % 25 == 0:
            print(f"  {i}/{len(files)}…", flush=True)

    tong = len(chi_tiet)
    if not tong:
        raise SystemExit("không tài liệu nào chạy được")

    dong_thuan_3 = sum(
        1
        for r in chi_tiet
        if r["classify"] == r["pages"] == r["sovereign"]
    )
    ab = sum(1 for r in chi_tiet if r["classify"] != r["pages"])
    a_s = sum(1 for r in chi_tiet if r["classify"] != r["sovereign"])
    b_s = sum(1 for r in chi_tiet if r["pages"] != r["sovereign"])

    md = [
        f"# Bất đồng nhãn “cần OCR” — bộ `{a.bo}` (n={tong})",
        "",
        f"Sinh bởi `scripts/compare_scan_label.py`. Ngưỡng Sovereign: {kiem}",
        "",
        "**Không bộ nào là ground truth.** DocLayNet gán nhãn bố cục, không gán nhãn",
        "“text layer”. Bảng dưới đo *sự bất đồng*, không xếp hạng đúng/sai.",
        "",
        "## Bất đồng từng cặp",
        "",
        "| Cặp | Lệch | % |",
        "|---|---:|---:|",
        f"| `classify_pdf` vs `extract_pages_markdown` (**cùng thư viện**) | {ab} | {100*ab/tong:.1f}% |",
        f"| `classify_pdf` vs Sovereign | {a_s} | {100*a_s/tong:.1f}% |",
        f"| `extract_pages_markdown` vs Sovereign | {b_s} | {100*b_s/tong:.1f}% |",
        "",
        f"Ba bộ đồng thuận: **{dong_thuan_3}/{tong}** ({100*dong_thuan_3/tong:.1f}%).",
        "",
        bang("Phân bố `pdf_type`", dem_type, tong),
        "",
        bang("Tổ hợp ba phán quyết", dem_bo_ba, tong),
        "",
        "## Bất đồng theo loại tài liệu (AC-04)",
        "",
        "| Loại | n | classify≠pages | classify≠sovereign | pages≠sovereign |",
        "|---|---:|---:|---:|---:|",
    ]
    for lt in sorted(theo_loai):
        rows = [r for r in chi_tiet if r["loai"] == lt]
        n = len(rows)
        md.append(
            f"| {lt} | {n} "
            f"| {sum(1 for r in rows if r['classify'] != r['pages'])} "
            f"| {sum(1 for r in rows if r['classify'] != r['sovereign'])} "
            f"| {sum(1 for r in rows if r['pages'] != r['sovereign'])} |"
        )

    tu_tin_ma_sai = [
        r for r in chi_tiet if r["classify"] != r["pages"] and (r["conf"] or 0) >= 1.0
    ]
    md += [
        "",
        "## Ca đáng ngại: `classify_pdf` bất đồng với chính thư viện mình **ở conf=1.00**",
        "",
        f"**{len(tu_tin_ma_sai)}/{ab}** ca bất đồng có `confidence = 1.00`. Độ tin cậy của",
        "`classify_pdf` **không** dùng được làm cổng chặn — nó tự tin ngay ở chỗ nó lệch.",
        "",
        "| doc | loại | pdf_type | conf | classify | pages | sovereign | chars/trang |",
        "|---|---|---|---:|---|---|---|---:|",
    ]
    for r in tu_tin_ma_sai[:20]:
        md.append(
            f"| `{r['doc']}` | {r['loai']} | {r['pdf_type']} | {r['conf']:.2f} "
            f"| {r['classify']} | {r['pages']} | {r['sovereign']} | {r['chars_per_page']} |"
        )

    if hong:
        md += ["", f"## Tài liệu chạy hỏng ({len(hong)})", ""]
        md += [f"- `{d}` — {e}" for d, e in hong]

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(md) + "\n", encoding="utf-8")
    a.out.with_suffix(".json").write_text(
        json.dumps(chi_tiet, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"n={tong} hong={len(hong)} classify!=pages={ab} -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
