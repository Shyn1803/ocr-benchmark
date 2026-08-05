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


def tim_tai_lieu(corpus: str, limit: int | None) -> list[Path]:
    """Danh sách file, **sắp xếp** rồi mới cắt.

    Cắt theo thứ tự thư mục trả về (tuỳ hệ thống file) thì `--limit 20` trên máy này và
    máy kia ra hai bộ khác nhau, và hai bảng điểm không so được với nhau dù cùng lệnh.
    """
    mau = CORPUS[corpus]
    docs = sorted((ROOT / "pdfs").glob(mau))
    if not docs:
        raise SystemExit(
            f"không thấy tài liệu nào khớp pdfs/{mau}. "
            "Chạy scripts/fetch_doclaynet.py hoặc scripts/fetch_olmocr.py trước."
        )
    return docs[:limit] if limit else docs


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
    docs = tim_tai_lieu(a.corpus, a.limit)
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
