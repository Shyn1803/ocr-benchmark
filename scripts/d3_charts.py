"""Sinh biểu đồ SVG cho bản công bố — TASK-089.

    py -3 scripts/d3_charts.py [--out DIR] [--force]

Đọc `prediction/`, chấm lại, rồi ghi vào `charts/<YYYY-MM-DD>/`:

    <nhóm>.svg   — một biểu đồ cột cho mỗi nhóm engine trong `report.NHOM_ENGINE`
    index.md     — mục lục, kèm cỡ tập chung của từng nhóm

Ba quy tắc, tất cả đều để biểu đồ không nói nhiều hơn số liệu:

1. **Chỉ vẽ trên tập tài liệu chung.** Một biểu đồ cột mời người đọc so hai cột cạnh
   nhau mạnh hơn hẳn một bảng markdown, nên nó phải chịu ràng buộc chặt hơn chứ không
   lỏng hơn — cùng ràng buộc `common_set.md` đang chịu, cùng ngưỡng
   `TOI_THIEU_TAP_CHUNG`.
2. **Không đo được thì không có cột.** N/A, "chưa có nhãn", "toàn hỏng" đều vẽ thành
   **chữ** trong ô, không phải cột cao 0. Cột cao 0 đọc ra là "điểm 0" — tức là
   *đo được và tệ nhất* — trong khi sự thật là chưa từng đo. Đây đúng là cái sai mà
   `Aggregate.cell()` đã phải tránh; vẽ lại nó bằng hình là bỏ công vô ích.
3. **Tất định.** Không màu ngẫu nhiên, không thứ tự phụ thuộc `dict`, không nhúng mốc
   thời gian vào SVG. Chạy hai lần phải ra hai file byte-giống-nhau, để `diff` còn
   dùng được như AC-04 của D1.

SVG viết tay bằng stdlib: thêm matplotlib chỉ để vẽ cột là thêm một thư viện nữa vào
danh sách "đổi gói thì đổi số mà không đổi `prediction/`".
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "src"))

from ocr_bench import registry, report  # noqa: E402
from ocr_bench.corpus import load_doclaynet, load_olmocr  # noqa: E402
from ocr_bench.prediction import load_predictions  # noqa: E402
from ocr_bench.scorer import ScoreTable, score_results  # noqa: E402
from ocr_bench.svgkit import bieu_do_cot, gia_tri_ve, nhan_ngan, thoat  # noqa: E402

# Ba luật ở đầu file này giờ nằm trong `ocr_bench.svgkit` và được dùng chung với
# `ocr_bench.research_charts`. Hai bản chép sẽ trôi ra khỏi nhau; một bản thì không.
# Giữ tên riêng tư ở đây vì file này còn được test nạp theo đường dẫn.
_thoat = thoat
_nhan_ngan = nhan_ngan
_o = gia_tri_ve


def _svg_mot_nhom(
    bang: ScoreTable, engines: list[str], metrics: list[str], n_chung: int
) -> str:
    return bieu_do_cot(
        bang,
        engines,
        metrics,
        tieu_de=" × ".join(engines),
        phu_de=(
            f"Tập chung {n_chung} tài liệu · trung bình có phạt (tài liệu hỏng tính 0)"
        ),
    )


def _ten_file(engines: list[str]) -> str:
    return "__".join(engines) + ".svg"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--force", action="store_true", help="cho phép ghi đè thư mục đã có")
    args = ap.parse_args()

    out = args.out or (GOC / "charts" / dt.date.today().isoformat())
    if out.exists() and any(p for p in out.iterdir() if p.name != ".gitkeep") and not args.force:
        print(f"LỖI: {out} đã có dữ liệu. Dùng --force nếu thật sự muốn ghi đè.")
        return 1

    gt: dict = {}
    gt.update(load_doclaynet())
    gt.update(load_olmocr())
    res = load_predictions(GOC / "prediction")
    ten_metric = sorted(registry.list_metrics())
    bang = score_results(res, [registry.get_metric(t)() for t in ten_metric], gt)
    cov = report.coverage(res)
    print(f"nạp {len(res)} dự đoán · {len(ten_metric)} metric")

    out.mkdir(parents=True, exist_ok=True)
    muc_luc = [
        "# Biểu đồ so sánh",
        "",
        "> Sinh bằng `py -3 scripts/d3_charts.py`. **Không** sửa tay.",
        "",
        "Mỗi biểu đồ chỉ vẽ trên tài liệu **mọi engine trong nhóm đều có**. Ô không "
        "đo được in chữ, **không** vẽ cột cao 0 — cột cao 0 đọc ra là điểm 0, tức là "
        "*đo được và tệ nhất*, trong khi sự thật là chưa từng đo.",
        "",
    ]

    n_ve = 0
    for nhom in report.NHOM_ENGINE:
        engines = list(nhom)
        ten = " × ".join(f"`{e}`" for e in engines)
        thieu = [e for e in engines if e not in cov]
        if thieu:
            muc_luc += [f"## {ten}", "", f"Bỏ qua — không có dự đoán của: "
                        f"{', '.join(f'`{e}`' for e in thieu)}.", ""]
            continue
        chung = set.intersection(*(cov[e] for e in engines))
        if len(chung) < report.TOI_THIEU_TAP_CHUNG:
            muc_luc += [
                f"## {ten}",
                "",
                f"**Tập chung chỉ {len(chung)} tài liệu — quá nhỏ để vẽ.** Cùng ngưỡng "
                f"`common_set.md` đang dùng.",
                "",
            ]
            continue

        con = report.loc_theo_tai_lieu(bang, chung)
        f = _ten_file(engines)
        (out / f).write_text(
            _svg_mot_nhom(con, engines, ten_metric, len(chung)),
            encoding="utf-8",
            newline="",
        )
        muc_luc += [f"## {ten}", "", f"Tập chung: **{len(chung)}** tài liệu.", "",
                    f"![{' × '.join(engines)}]({f})", ""]
        n_ve += 1
        print(f"  {f}  ({len(chung)} tài liệu chung)")

    (out / "index.md").write_text("\n".join(muc_luc), encoding="utf-8", newline="")
    print(f"ghi {out} · {n_ve} biểu đồ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
