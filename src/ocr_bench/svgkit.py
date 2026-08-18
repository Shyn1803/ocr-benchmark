"""Nguyên liệu vẽ SVG dùng chung cho mọi biểu đồ trong repo.

Tách ra vì hai chỗ vẽ biểu đồ — `scripts/d3_charts.py` (ảnh chụp `charts/<ngày>/`) và
`ocr_bench.research_charts` (hình của bản công bố) — phải tuân **cùng** ba luật, và
ba luật đó chỉ giữ được nếu chúng dùng chung một đoạn mã chứ không phải hai bản chép:

1. **Chỉ vẽ trên tập tài liệu chung.** Biểu đồ cột mời người đọc so hai cột cạnh nhau
   mạnh hơn hẳn bảng markdown, nên nó phải chịu ràng buộc chặt hơn chứ không lỏng hơn.
2. **Không đo được thì không có cột.** N/A, "chưa có nhãn", "toàn hỏng" đều vẽ thành
   **chữ**, không phải cột cao 0. Cột cao 0 đọc ra là "điểm 0" — tức *đo được và tệ
   nhất* — trong khi sự thật là chưa từng đo. Đây đúng cái sai `Aggregate.cell()` đã
   phải tránh; vẽ lại nó bằng hình là bỏ công vô ích.
3. **Tất định.** Không màu ngẫu nhiên, không thứ tự phụ thuộc `dict`, không nhúng mốc
   thời gian. Chạy hai lần phải ra hai file byte-giống-nhau.

SVG viết tay bằng stdlib: thêm matplotlib chỉ để vẽ cột là thêm một thư viện nữa vào
danh sách "đổi gói thì đổi số mà không đổi `prediction/`".
"""

from __future__ import annotations

from collections.abc import Sequence

from ocr_bench.metrics.base import Aggregate
from ocr_bench.scorer import ScoreTable

__all__ = [
    "MAU",
    "CAO_DONG",
    "LE_TRAI",
    "LE_PHAI",
    "RONG_COT",
    "CAO_DAU",
    "thoat",
    "nhan_ngan",
    "gia_tri_ve",
    "mo_svg",
    "bieu_do_cot",
]

# Bảng màu cố định theo **vị trí trong nhóm**, không theo tên engine: nhóm nào cũng
# đọc được bằng cùng một chú giải, và thêm engine mới không làm đổi màu engine cũ.
MAU = ("#2563eb", "#f59e0b", "#10b981", "#a855f7", "#ef4444", "#64748b")

CAO_DONG = 34
"""Chiều cao một dòng metric, px. Đủ chỗ cho mỗi engine một khe ~8px, vì khe của
engine không có cột vẫn phải in được lý do — xem `nhan_ngan`."""
LE_TRAI = 190
"""Chỗ cho tên metric. Rộng tay vì `assert_table_relation` là tên dài nhất."""
LE_PHAI = 70
RONG_COT = 560
CAO_DAU = 78


def thoat(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def nhan_ngan(a: Aggregate) -> str:
    """Nhãn rút gọn cho khe của **một** engine không có cột.

    Khe cao ~8px không chứa nổi `cell()` đầy đủ, nhưng bỏ trống thì tệ hơn hẳn: hàng
    `heading` có cột của `opendataloader` và khoảng trắng ở chỗ hai engine kia, đọc ra
    là "quên vẽ" chứ không phải "engine không hứa làm việc này". Trạng thái phải gắn
    được vào đúng engine, nên nhãn ngắn nằm trong khe của nó và tô đúng màu nó.
    """
    if a.n_thieu_nang_luc and not a.n_scored and not a.n_chua_nhan:
        return "N/A"
    if a.n_chua_nhan and not a.n_scored:
        return "chưa có nhãn"
    return f"{a.n_failed} hỏng, 0 chấm được"


def gia_tri_ve(a: Aggregate) -> tuple[float | None, str]:
    """`(giá trị vẽ được, nhãn)`. `None` = không vẽ cột, chỉ in nhãn.

    Nhãn lấy thẳng từ `Aggregate.cell()` để biểu đồ và bảng không bao giờ nói khác
    nhau — hai chỗ tự diễn giải trạng thái N/A là hai chỗ để chúng trôi ra khỏi nhau.
    """
    nhan = a.cell()
    if a.n_scored == 0 or a.penalized_mean is None:
        return None, nhan
    return a.penalized_mean, nhan


def mo_svg(rong: int, cao: int) -> list[str]:
    """Thẻ mở + nền trắng. Nền phải đặc: SVG trong suốt dán vào slide nền tối thì
    chữ `#0f172a` biến mất, và người dán không thấy nó biến mất."""
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{rong}" height="{cao}" '
        f'viewBox="0 0 {rong} {cao}" font-family="system-ui,sans-serif">',
        f'<rect width="{rong}" height="{cao}" fill="#ffffff"/>',
    ]


def bieu_do_cot(
    bang: ScoreTable,
    engines: Sequence[str],
    metrics: Sequence[str],
    *,
    tieu_de: str,
    phu_de: str,
) -> str:
    """Biểu đồ cột ngang metric × engine, mỗi ô đi qua `gia_tri_ve`.

    `metrics` là thứ tự in ra, do người gọi quyết định — hai nửa corpus rời nhau
    không bao giờ được đưa vào cùng một lần gọi.
    """
    engines = list(engines)
    metrics = list(metrics)
    cao = CAO_DAU + len(metrics) * CAO_DONG + 24
    rong = LE_TRAI + RONG_COT + LE_PHAI
    cao_thanh = max(3, (CAO_DONG - 8) // max(1, len(engines)))

    d = mo_svg(rong, cao)
    d += [
        f'<text x="12" y="22" font-size="14" font-weight="600">{thoat(tieu_de)}</text>',
        f'<text x="12" y="40" font-size="11" fill="#475569">{thoat(phu_de)}</text>',
    ]

    # Chú giải
    x = 12
    for i, e in enumerate(engines):
        d.append(f'<rect x="{x}" y="50" width="10" height="10" fill="{MAU[i % len(MAU)]}"/>')
        d.append(f'<text x="{x + 14}" y="59" font-size="11">{thoat(e)}</text>')
        x += 20 + 7 * len(e)

    # Lưới 0 · 0.5 · 1
    for v in (0.0, 0.5, 1.0):
        gx = LE_TRAI + v * RONG_COT
        d.append(
            f'<line x1="{gx:.1f}" y1="{CAO_DAU - 8}" x2="{gx:.1f}" '
            f'y2="{CAO_DAU + len(metrics) * CAO_DONG}" stroke="#e2e8f0"/>'
        )
        d.append(
            f'<text x="{gx:.1f}" y="{CAO_DAU - 12}" font-size="10" fill="#94a3b8" '
            f'text-anchor="middle">{v:g}</text>'
        )

    for r, m in enumerate(metrics):
        y0 = CAO_DAU + r * CAO_DONG
        d.append(
            f'<text x="{LE_TRAI - 8}" y="{y0 + CAO_DONG / 2 + 3:.1f}" font-size="11" '
            f'text-anchor="end" fill="#0f172a">{thoat(m)}</text>'
        )
        oo = [bang.cell(m, e) for e in engines]
        o = [(e, a, *gia_tri_ve(a)) for e, a in zip(engines, oo)]
        if all(gt is None for *_x, gt, _n in o):
            # Cả hàng không ai đo được: một nhãn đầy đủ ở giữa hàng đọc dễ hơn ba nhãn
            # rút gọn giống nhau xếp chồng.
            d.append(
                f'<text x="{LE_TRAI + 4}" y="{y0 + CAO_DONG / 2 + 3:.1f}" '
                f'font-size="10" fill="#94a3b8">{thoat(o[0][3])}</text>'
            )
            continue
        for i, (e, agg, gia_tri, _nhan) in enumerate(o):
            y = y0 + 4 + i * cao_thanh
            if gia_tri is None:
                # Hàng này có engine khác vẽ được cột, nên khe trống sẽ bị đọc là
                # "quên vẽ". Ghi lý do vào đúng khe, đúng màu engine.
                d.append(
                    f'<text x="{LE_TRAI + 4}" y="{y + cao_thanh - 1:.1f}" '
                    f'font-size="8" fill="{MAU[i % len(MAU)]}" opacity="0.75">'
                    f"{thoat(nhan_ngan(agg))}</text>"
                )
                continue
            w = max(1.0, gia_tri * RONG_COT)
            d.append(
                f'<rect x="{LE_TRAI}" y="{y:.1f}" width="{w:.1f}" '
                f'height="{cao_thanh}" fill="{MAU[i % len(MAU)]}"/>'
            )
            d.append(
                f'<text x="{LE_TRAI + w + 4:.1f}" y="{y + cao_thanh - 1:.1f}" '
                f'font-size="9" fill="#334155">{gia_tri:.3f}</text>'
            )

    d.append("</svg>")
    return "\n".join(d) + "\n"
