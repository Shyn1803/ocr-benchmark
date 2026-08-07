"""Sinh báo cáo C2 — cổng `sabotage` + độ phân tán từng metric.

    py -3 scripts/c2_report.py

Đọc dự đoán đã lưu ở `prediction/`, dựng `sabotage` bằng chính `SabotageAdapter` thật
(nguồn = engine mạnh nhất), chấm lại, rồi ghi:

    results/c2_discrimination.md     — bảng người đọc
    results/c2_metric_status.json    — bảng chính / phụ lục, máy đọc (AC-03)

Không chạy engine nào, không đụng PDF. Chấm lại 205 tài liệu mất vài giây.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC / "src"))

from ocr_bench import discrimination as D  # noqa: E402
from ocr_bench import registry  # noqa: E402
from ocr_bench.adapters.sabotage import SabotageAdapter  # noqa: E402
from ocr_bench.corpus import load_doclaynet, load_olmocr  # noqa: E402
from ocr_bench.prediction import load_predictions  # noqa: E402
from ocr_bench.scorer import ScoreTable, score_results  # noqa: E402

NGUON_MANH = "opendataloader"


def _cham() -> ScoreTable:
    gt: dict = {}
    gt.update(load_doclaynet())
    gt.update(load_olmocr())

    res = load_predictions(GOC / "prediction")
    nguon = [r for r in res if r.engine == NGUON_MANH]
    if not nguon:
        raise SystemExit(f"không có dự đoán nào của `{NGUON_MANH}` — không dựng được sabotage")

    tu_dia = D.NguonTuDia(nguon)
    sa = SabotageAdapter(tu_dia)
    sab = [sa.execute(p) for p in tu_dia.duong_dan()]

    ten = sorted(registry.list_metrics())
    metrics = [registry.get_metric(t)() for t in ten]
    print(f"nạp {len(res)} dự đoán · nguồn {len(nguon)} · sabotage {len(sab)}")
    return score_results([r for r in res if r.engine != "sabotage"] + sab, metrics, gt)


def _md(bang: ScoreTable, ten: list[str]) -> str:
    d: list[str] = [
        "# C2 — thước đo có phân biệt được engine không",
        "",
        "Sinh bằng `py -3 scripts/c2_report.py`. **Không** sửa tay — chạy lại để cập nhật.",
        "",
        f"Nguồn của `sabotage`: **{NGUON_MANH}** (không phải `noop` mặc định — làm hỏng "
        "đầu ra rỗng thì vẫn rỗng, cổng sẽ xanh mà không kiểm gì).",
        f"Ngưỡng phân tán: **{D.NGUONG_PHAN_TAN}**. Engine tổng hợp bị loại khỏi phép "
        f"tính phân tán: {', '.join(sorted(D.ENGINE_TONG_HOP))}.",
        "",
        "## 1. Cổng `sabotage` (AC-01)",
        "",
        "`chạy` = cổng thực sự kiểm được điều gì. Metric không đo được thì `sabotage` "
        "xuống cuối **vì N/A**, không phải vì kém — đó không tính là đạt.",
        "",
        "| Metric | Cổng chạy | Đạt | sabotage | nguồn | Ghi chú |",
        "|---|---|---|---|---|---|",
    ]
    chay = dat = 0
    for m in ten:
        k = D.kiem_sabotage(bang, m, nguon=NGUON_MANH)
        chay += k.do_duoc
        dat += k.do_duoc and k.dat
        s = "—" if k.diem_sabotage is None else f"{k.diem_sabotage:.4f}"
        n = "—" if k.diem_nguon is None else f"{k.diem_nguon:.4f}"
        d.append(
            f"| `{m}` | {'✅' if k.do_duoc else '⬜'} | "
            f"{'✅' if k.do_duoc and k.dat else '—' if not k.do_duoc else '❌'} | "
            f"{s} | {n} | {k.ly_do} |"
        )
    d += [
        "",
        f"**{chay}/{len(ten)}** metric có cổng chạy được; **{dat}/{chay}** trong số đó đạt.",
        "",
        "## 2. Độ phân tán giữa các engine thật (AC-02)",
        "",
        "`n` = số tài liệu **cả các engine cùng chấm được**. So trung bình trên hai bộ "
        "tài liệu khác nhau là so hai đại lượng khác nhau — chênh lệch thu được nói về "
        "bộ mẫu, không nói về engine.",
        "",
        "| Metric | Phán quyết | spread | n | Engine | Lý do |",
        "|---|---|---|---|---|---|",
    ]
    pt = [D.do_phan_tan(bang, m) for m in ten]
    for p in pt:
        sp = "—" if p.spread is None else f"{p.spread:.4f}"
        d.append(
            f"| `{p.metric}` | {p.phan_quyet} | {sp} | {p.n_doc_chung} | "
            f"{', '.join(p.engines) or '—'} | {p.ly_do} |"
        )

    chinh = [p for p in pt if p.vao_bang_chinh]
    thieu = [p for p in pt if p.phan_quyet == D.PhanQuyet.KHONG_DU_DU_LIEU]
    khong = [p for p in pt if p.phan_quyet == D.PhanQuyet.KHONG_PHAN_BIET_DUOC]
    d += [
        "",
        "## 3. Bảng chính / phụ lục (AC-03)",
        "",
        f"- **Bảng chính — {len(chinh)}/{len(ten)}**: "
        + (", ".join(f"`{p.metric}`" for p in chinh) or "_trống_"),
        f"- **Phụ lục, không phân biệt được — {len(khong)}**: "
        + (", ".join(f"`{p.metric}`" for p in khong) or "_trống_"),
        f"- **Phụ lục, chưa đủ dữ liệu — {len(thieu)}**: "
        + (", ".join(f"`{p.metric}`" for p in thieu) or "_trống_"),
        "",
        "Hai nhóm phụ lục **không** cùng nghĩa. `khong_phan_biet_duoc` là kết luận về "
        "**metric**: các engine chênh nhau quá ít để nói lên điều gì. "
        "`khong_du_du_lieu` là kết luận về **bộ mẫu**: chưa có đủ hai engine cùng đo "
        "được để mà so. Gộp chúng lại là vứt nhầm một metric tốt vì thiếu nhãn.",
        "",
    ]
    return "\n".join(d) + "\n"


def main() -> None:
    bang = _cham()
    ten = sorted(registry.list_metrics())
    ra = GOC / "results"
    ra.mkdir(exist_ok=True)

    (ra / "c2_discrimination.md").write_text(_md(bang, ten), encoding="utf-8")
    nhom = D.phan_nhom_metric([D.do_phan_tan(bang, m) for m in ten], moi_metric=ten)
    (ra / "c2_metric_status.json").write_text(
        json.dumps(nhom, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"→ results/c2_discrimination.md · results/c2_metric_status.json "
        f"(bảng chính {len(nhom['bang_chinh'])}/{len(ten)})"
    )


if __name__ == "__main__":
    main()
