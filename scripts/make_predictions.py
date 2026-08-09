"""Chạy engine một lần rồi ghi kết quả xuống `prediction/` — A2 (TASK-073).

    py -3 scripts/make_predictions.py --engines noop,sabotage --corpus olmocr
    py -3 scripts/make_predictions.py --engines noop --corpus doclaynet --limit 20
    py -3 scripts/make_predictions.py --engines noop --refresh        # chạy lại tất

Đây là **nửa đắt tiền** của bench, tách hẳn khỏi nửa chấm điểm. Marker chạy 200 trang
trên CPU mất khoảng 3 giờ; sửa một dòng trong metric mà phải trả lại 3 giờ đó thì
không ai sửa metric nữa — và một bộ thước không ai dám sửa là bộ thước sai vĩnh viễn.

Mặc định **không chạy lại** tài liệu đã có prediction. Version engine lệch so với file
đã lưu thì chạy lại (`--on-version-mismatch`), vì ở đường này engine vốn đang sẵn sàng;
giữ số cũ dưới nhãn version mới sinh ra một bảng không truy ngược được về đâu.

⚠️ Prediction đang commit trong repo là của `noop` + `sabotage`. Cả hai là **engine
giả**, có mặt để đo *bộ thước* chứ không đo OCR: `noop` trả chuỗi rỗng, `sabotage` bọc
`noop` nên cũng ra rỗng. Chúng chứng minh đường ống ghi/đọc chạy trên bộ mẫu thật, chứ
không nói gì về chất lượng nhận dạng. Số liệu thật đến từ A4→A7 (Marker,
OpenDataLoader, pdf-inspector, BE hiện tại).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import ocr_bench  # noqa: F401  — import để hai engine giả tự đăng ký
from ocr_bench import registry
from ocr_bench.prediction import run_engines_cached

ROOT = Path(__file__).resolve().parent.parent

CORPUS: dict[str, str] = {
    "sample": "sample_minimal.pdf",
    "doclaynet": "doclaynet/*.pdf",
    "olmocr": "olmocr/*/*.pdf",
}


def _trai_deu(docs: list[Path], limit: int) -> list[Path]:
    """Cắt còn `limit` file nhưng **trải đều trên các thư mục con**, xoay vòng.

    `sorted(...)[:limit]` là cái bẫy: bộ `olmocr` xếp theo nhóm (`arxiv_math/`,
    `tables/`, `old_scans/`, ...) và nhóm đầu bảng chữ cái có 522 file, nên
    `--limit 60` lấy trọn 60 file `arxiv_math`. Chấm bộ đó thì **chỉ**
    `assert_math_presence` có số, 5 metric assert còn lại trả N/A — trông y hệt
    "engine không có năng lực" trong khi thật ra là mẫu chạy bị lệch. Đã mất một
    lượt chạy vì chuyện này (2026-08-09).

    Vẫn tất định: sắp trong từng nhóm, xoay vòng theo tên nhóm đã sắp.
    """
    theo_nhom: dict[str, list[Path]] = {}
    for d in docs:
        theo_nhom.setdefault(d.parent.name, []).append(d)
    if len(theo_nhom) < 2:
        return docs[:limit]

    lay: list[Path] = []
    hang = [theo_nhom[k] for k in sorted(theo_nhom)]
    i = 0
    while len(lay) < limit and any(i < len(h) for h in hang):
        for h in hang:
            if i < len(h):
                lay.append(h[i])
                if len(lay) == limit:
                    break
        i += 1
    return sorted(lay)


def tim_tai_lieu(corpus: str, limit: int | None, chi: str | None = None) -> list[Path]:
    """Danh sách file, **sắp xếp** rồi mới cắt.

    Cắt theo thứ tự thư mục trả về (tuỳ hệ thống file) thì `--limit 20` trên máy này và
    máy kia ra hai bộ khác nhau, và hai bảng điểm không so được với nhau dù cùng lệnh.
    Bộ nhiều nhóm thì cắt **trải đều** — xem `_trai_deu`.

    ``chi`` lọc theo tên (stem) — dùng khi engine đắt tới mức chạy cả bộ là không khả
    thi và ta chỉ cần trả lời một câu hỏi hẹp (A7: "10 tài liệu hỏng ở chế độ nhẹ có được
    Marker cứu không"). Stem không khớp thì **ném**, không âm thầm chạy ít hơn: một lượt
    chạy 3 tài liệu in ra như lượt chạy 10 tài liệu là cách hỏng khó thấy nhất.
    """
    mau = CORPUS[corpus]
    docs = sorted((ROOT / "pdfs").glob(mau))
    if not docs:
        raise SystemExit(
            f"không thấy tài liệu nào khớp pdfs/{mau}. "
            "Chạy scripts/fetch_doclaynet.py hoặc scripts/fetch_olmocr.py trước."
        )
    if chi:
        muon = {t.strip() for t in chi.split(",") if t.strip()}
        theo_stem = {d.stem: d for d in docs}
        thieu = sorted(muon - set(theo_stem))
        if thieu:
            raise SystemExit(f"--only: không có trong bộ {corpus}: {', '.join(thieu)}")
        docs = [theo_stem[s] for s in sorted(muon)]
    return _trai_deu(docs, limit) if limit else docs


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "--engines",
        default="noop,sabotage",
        help=f"tên engine, phân tách bằng dấu phẩy. Có: {','.join(registry.list_adapters())}",
    )
    p.add_argument("--corpus", choices=sorted(CORPUS), default="sample")
    p.add_argument("--limit", type=int, default=None, help="chỉ lấy N tài liệu đầu")
    p.add_argument(
        "--only",
        default=None,
        help="chỉ chạy các tài liệu có stem này (phân tách bằng dấu phẩy)",
    )
    p.add_argument(
        "--out", default=str(ROOT / "prediction"), help="thư mục prediction (mặc định: repo)"
    )
    p.add_argument(
        "--refresh", action="store_true", help="chạy lại kể cả khi đã có prediction"
    )
    p.add_argument(
        "--on-version-mismatch",
        choices=["rerun", "error", "use"],
        default="rerun",
        help="file cũ ghi bằng version engine khác thì làm gì (mặc định: chạy lại)",
    )
    a = p.parse_args(argv)

    ten = [t.strip() for t in a.engines.split(",") if t.strip()]
    adapters = [registry.get_adapter(t)() for t in ten]
    docs = tim_tai_lieu(a.corpus, a.limit, a.only)
    out = Path(a.out)

    print(f"{len(adapters)} engine × {len(docs)} tài liệu → {out}")
    ket_qua = run_engines_cached(
        adapters,
        docs,
        out,
        refresh=a.refresh,
        on_version_mismatch=a.on_version_mismatch,
    )

    hong = [r for r in ket_qua if r.failed]
    for e in ten:
        cua_e = [r for r in ket_qua if r.engine == e]
        giay = sum(r.seconds or 0.0 for r in cua_e)
        print(f"  {e:12s} {len(cua_e):5d} tài liệu  {giay:8.1f}s")
    # In cả số hỏng chứ không im lặng: `failed=True` là dữ liệu của `FailRate`, còn
    # một lượt chạy hỏng hàng loạt mà bảng vẫn in bình thường là cách hỏng tệ nhất.
    print(f"  hỏng: {len(hong)}")
    for r in hong[:5]:
        print(f"    - {r.engine}/{r.doc_id}: {r.error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
