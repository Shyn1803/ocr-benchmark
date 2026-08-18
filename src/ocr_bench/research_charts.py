"""Bốn hình của bản công bố — vẽ từ `ScoreTable` / `PerfAggregate` **thật**.

Bản trước của file này là lớp lỗi mà `runs/pilot/validation-report.md` đã phải rút lại
một lần: ba renderer nhận `data` rồi không đọc nó (SVG ra 736–992 B, chỉ có trục và
tiêu đề), còn `render_forest_plot` tra `data.get("profiles", [...])` — khoá `"profiles"`
chưa từng có trong `aggregate-results.json`, nên nó luôn rơi vào danh sách mặc định và
vẽ ra `marker_default` / `sovereign_scan`, bốn engine **chưa từng chạy**. Một hình đẹp
mang tên engine không tồn tại có sức thuyết phục lớn hơn hẳn một bảng số, nên nó là
kiểu sai đắt nhất trong repo này.

Nguyên tắc thay thế, thi hành bằng mã chứ không bằng lời hứa:

* **Thiếu dữ liệu thì `raise`.** Không default list, không `data.get(..., [...])`. Hình
  vắng mặt là chuyện người dựng phải xử lý; hình có mặt với số bịa thì không ai xử lý
  được vì không ai biết.
* **Không đo được thì ra chữ, không ra cột 0** — luật chung ở `ocr_bench.svgkit`.
* **Tất định** — không mốc thời gian, không màu ngẫu nhiên, không phụ thuộc thứ tự dict.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path

from ocr_bench.metrics.base import Aggregate
from ocr_bench.metrics.perf import PerfAggregate
from ocr_bench.scorer import ScoreTable
from ocr_bench.svgkit import MAU, bieu_do_cot, mo_svg, thoat
from ocr_bench.types import OcrResult

__all__ = [
    "GHI_CHU_THOI_GIAN",
    "render_forest_plot",
    "render_accuracy_speed_chart",
    "render_scan_degradation_chart",
    "render_failure_distribution_chart",
]


GHI_CHU_THOI_GIAN = (
    "`seconds` gồm cả thời gian nạp model (`model_load_seconds` không đo được ở lượt "
    "chạy này); thứ tự chạy không khôi phục được từ prediction nên không tách lượt nguội."
)
"""Hai hạn chế của trục thời gian, in nguyên văn trên hình.

Số đo có thật, nhưng nó là *tổng* thời gian một lượt, không phải thời gian xử lý thuần.
Gọi nó là "warm" thì đúng chữ mà sai nghĩa; nói ra thì người đọc tự trừ được.
"""


def _ghi(out_path: Path, noi_dung: str) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(noi_dung, encoding="utf-8", newline="")
    return out_path


def _khung_chu(tieu_de: str, dong: Sequence[str], *, rong: int = 820) -> str:
    """Hình "không vẽ được" — nói thiếu cái gì, thay vì vẽ một hình rỗng.

    Vẫn là file SVG thật để chỗ nhúng hình trong bài không hiện ảnh vỡ; nhưng nội dung
    là câu giải thích chứ không phải trục toạ độ trống, vốn đọc ra là "đã đo, không có
    gì".
    """
    cao = 70 + 20 * len(dong)
    d = mo_svg(rong, cao)
    d.append(f'<text x="16" y="30" font-size="14" font-weight="600">{thoat(tieu_de)}</text>')
    for i, s in enumerate(dong):
        d.append(f'<text x="16" y="{56 + i * 20}" font-size="11" fill="#475569">{thoat(s)}</text>')
    d.append("</svg>")
    return "\n".join(d) + "\n"


def _kiem_bang(bang: object, engines: Sequence[str], metrics: Sequence[str]) -> None:
    if not isinstance(bang, ScoreTable):
        raise TypeError(f"cần ScoreTable thật, nhận {type(bang).__name__}")
    if not engines:
        raise ValueError("không có engine nào để vẽ")
    if not metrics:
        raise ValueError("không có metric nào để vẽ")
    co = set(bang.engines())
    la = [e for e in engines if e not in co]
    if la:
        # Đúng cái bẫy cũ: tên engine trong hình mà không có trong bảng.
        raise ValueError(f"engine không có trong ScoreTable: {', '.join(sorted(la))}")


# ---------------------------------------------------------------------------
# 1. Xếp hạng năng lực — một hình mỗi nửa corpus
# ---------------------------------------------------------------------------


def render_forest_plot(
    bang: ScoreTable,
    out_path: Path,
    *,
    engines: Sequence[str],
    metrics: Sequence[str],
    tieu_de: str,
    phu_de: str,
) -> Path:
    """Cột ngang metric × engine cho **một** nửa corpus.

    Tên hàm giữ từ bản cũ để không phải sửa mọi chỗ tham chiếu, nhưng đây là biểu đồ
    cột chứ không phải forest plot: `Aggregate` không mang khoảng tin cậy, nên vẽ râu
    lỗi ở đây là vẽ ra một đại lượng chưa hề tính. Khoảng tin cậy có thật nằm ở
    `results/statistical-tests.json`.

    `metrics` do người gọi lọc và **phải** thuộc cùng một nửa corpus — hai nửa rời nhau
    hoàn toàn nên xếp chung một trục là mời so hai thứ không so được.
    """
    _kiem_bang(bang, engines, metrics)
    return _ghi(
        out_path,
        bieu_do_cot(bang, engines, metrics, tieu_de=tieu_de, phu_de=phu_de),
    )


# ---------------------------------------------------------------------------
# 2. Chính xác × tốc độ
# ---------------------------------------------------------------------------


def render_accuracy_speed_chart(
    perf: dict[str, PerfAggregate],
    diem: dict[str, Aggregate],
    out_path: Path,
    *,
    nhan_y: str,
    tieu_de: str = "Chính xác × tốc độ",
    ghi_chu_them: Sequence[str] = (),
) -> Path:
    """Điểm rải: X = giây/trang (trung vị), Y = điểm của metric `nhan_y`.

    Trung vị chứ không trung bình: phân bố giây/trang lệch nặng — vài tài liệu vài trăm
    trang kéo trung bình đi mà không nói gì về tài liệu điển hình.

    Engine đo được thời gian nhưng **không** chấm được `nhan_y` thì vẫn có mặt, nằm
    dưới trục X kèm nhãn lý do: bỏ nó đi là để người đọc tưởng engine ấy chưa chạy.

    `ghi_chu_them` in dưới chú thích thời gian — chỗ người gọi nói ra engine nào đã bị
    loại khỏi hình và vì sao, để "vắng mặt" không bao giờ là im lặng.
    """
    if not isinstance(perf, dict) or not perf:
        raise ValueError("không có PerfAggregate nào — không vẽ được trục thời gian")
    if not isinstance(diem, dict):
        raise TypeError(f"`diem` cần dict[str, Aggregate], nhận {type(diem).__name__}")
    thieu = [e for e in perf if e not in diem]
    if thieu:
        raise ValueError(f"thiếu điểm của engine: {', '.join(sorted(thieu))}")

    es = sorted(perf)
    x_co = [
        perf[e].sec_moi_trang_trung_vi
        for e in es
        if perf[e].sec_moi_trang_trung_vi is not None
    ]
    if not x_co:
        return _ghi(
            out_path,
            _khung_chu(
                tieu_de,
                [
                    "Không engine nào có `seconds` + `page_sizes` để tính giây/trang.",
                    GHI_CHU_THOI_GIAN,
                ],
            ),
        )

    rong, cao = 820, 460
    tr, ph, tren, duoi = 70, 30, 74, 96
    w = rong - tr - ph
    h = cao - tren - duoi
    x_max = max(x_co) * 1.15 or 1.0

    d = mo_svg(rong, cao)
    d += [
        f'<text x="16" y="24" font-size="14" font-weight="600">{thoat(tieu_de)}</text>',
        f'<text x="16" y="42" font-size="11" fill="#475569">'
        f"Trục Y: {thoat(nhan_y)} (trung bình có phạt) · trục X: giây/trang, trung vị</text>",
    ]

    # Lưới Y 0 · 0.5 · 1 và trục X
    for v in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = tren + (1 - v) * h
        d.append(f'<line x1="{tr}" y1="{y:.1f}" x2="{tr + w}" y2="{y:.1f}" stroke="#e2e8f0"/>')
        d.append(
            f'<text x="{tr - 8}" y="{y + 3:.1f}" font-size="10" fill="#94a3b8" '
            f'text-anchor="end">{v:g}</text>'
        )
    for k in range(5):
        gx = tr + k * w / 4
        gv = x_max * k / 4
        d.append(
            f'<line x1="{gx:.1f}" y1="{tren}" x2="{gx:.1f}" y2="{tren + h}" stroke="#f1f5f9"/>'
        )
        d.append(
            f'<text x="{gx:.1f}" y="{tren + h + 16}" font-size="10" fill="#94a3b8" '
            f'text-anchor="middle">{gv:.1f}s</text>'
        )

    ngoai = 0
    for i, e in enumerate(es):
        p, a = perf[e], diem[e]
        mau = MAU[i % len(MAU)]
        sec = p.sec_moi_trang_trung_vi
        if sec is None or a.n_scored == 0 or a.penalized_mean is None:
            # Có mặt nhưng không đặt được lên mặt phẳng — ghi ra dưới, kèm lý do đầy đủ.
            d.append(
                f'<text x="16" y="{cao - 58 + ngoai * 14}" font-size="10" fill="{mau}">'
                f"{thoat(e)}: {thoat(a.cell() if sec is not None else p.cell())}</text>"
            )
            ngoai += 1
            continue
        cx = tr + (sec / x_max) * w
        cy = tren + (1 - a.penalized_mean) * h
        d.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" fill="{mau}"/>')
        d.append(
            f'<text x="{cx + 10:.1f}" y="{cy + 4:.1f}" font-size="10" fill="#334155">'
            f"{thoat(e)} · {a.penalized_mean:.3f} (n={a.n_scored + a.n_failed}) · "
            f"{sec:.2f}s/trang</text>"
        )

    chu = [GHI_CHU_THOI_GIAN, *ghi_chu_them]
    for j, dong in enumerate(chu):
        d.append(
            f'<text x="16" y="{cao - 12 - (len(chu) - 1 - j) * 12}" font-size="9" '
            f'fill="#64748b">{thoat(dong)}</text>'
        )
    d.append("</svg>")
    return _ghi(out_path, "\n".join(d) + "\n")


# ---------------------------------------------------------------------------
# 3. Suy giảm khi bật chế độ scan
# ---------------------------------------------------------------------------


def _cap_default_scan(engines: Iterable[str]) -> list[tuple[str, str, str]]:
    """`[(họ, engine_default, engine_scan)]` — chỉ họ nào **đủ cả hai**."""
    co = set(engines)
    ra = []
    for e in sorted(co):
        if not e.endswith("_default"):
            continue
        ho = e[: -len("_default")]
        if f"{ho}_scan" in co:
            ra.append((ho, e, f"{ho}_scan"))
    return ra


def render_scan_degradation_chart(
    bang: ScoreTable,
    out_path: Path,
    *,
    metrics: Sequence[str],
    tieu_de: str = "Suy giảm khi bật chế độ scan",
) -> Path:
    """So `*_default` với `*_scan` của **cùng** họ engine.

    Chỉ vẽ họ nào có đủ cả hai profile. Ghép `docling_default` với `opendataloader_scan`
    thì hiệu số đo hai thứ cùng lúc (đổi engine *và* đổi chế độ) và không tách ra được.
    Họ thiếu vế thì ghi thẳng là thiếu — hiện `docling_scan` chưa chạy xong.
    """
    if not isinstance(bang, ScoreTable):
        raise TypeError(f"cần ScoreTable thật, nhận {type(bang).__name__}")
    if not metrics:
        raise ValueError("không có metric nào để vẽ")

    es = bang.engines()
    cap = _cap_default_scan(es)
    if not cap:
        le = sorted(
            e for e in es if e.endswith(("_default", "_scan"))
        )
        return _ghi(
            out_path,
            _khung_chu(
                tieu_de,
                [
                    "Không họ engine nào có đủ cả `*_default` lẫn `*_scan`.",
                    "Có mặt: " + (", ".join(le) if le else "không profile nào"),
                    "Hiệu số giữa hai họ khác nhau đo lẫn cả đổi engine lẫn đổi chế độ, "
                    "nên không vẽ.",
                ],
            ),
        )

    engines = [e for _ho, a, b in cap for e in (a, b)]
    return _ghi(
        out_path,
        bieu_do_cot(
            bang,
            engines,
            list(metrics),
            tieu_de=tieu_de,
            phu_de=(
                "Từng cặp cùng họ: "
                + " · ".join(f"{a} → {b}" for _ho, a, b in cap)
                + " — chênh lệch trong cặp là tác động của chế độ scan"
            ),
        ),
    )


# ---------------------------------------------------------------------------
# 4. Phân bố lỗi
# ---------------------------------------------------------------------------


def render_failure_distribution_chart(
    res: Sequence[OcrResult],
    out_path: Path,
    *,
    tieu_de: str = "Phân bố tài liệu hỏng theo nguyên nhân",
) -> Path:
    """Đếm `failed` theo `engine × failure_kind` từ chính các `OcrResult` đã nạp.

    Theo `failure_kind` chứ không theo `error`: message lỗi đổi theo phiên bản thư viện
    nên gộp theo nó thì hai lượt chạy ra hai biểu đồ khác nhau mà không có gì đổi thật.
    """
    if not isinstance(res, (list, tuple)) or not res:
        raise ValueError("không có OcrResult nào — không có gì để đếm")

    es = sorted({r.engine for r in res})
    tong = {e: sum(1 for r in res if r.engine == e) for e in es}
    dem: dict[str, dict[str, int]] = {e: {} for e in es}
    for r in res:
        if r.failed and r.failure_kind is not None:
            d = dem[r.engine]
            d[r.failure_kind.value] = d.get(r.failure_kind.value, 0) + 1

    loai = sorted({k for d in dem.values() for k in d})
    if not loai:
        return _ghi(
            out_path,
            _khung_chu(
                tieu_de,
                [
                    "0 tài liệu hỏng ở mọi engine — không có phân bố để vẽ.",
                    "Tổng lượt chạy: "
                    + " · ".join(f"{e} {tong[e]}" for e in es),
                ],
            ),
        )

    cao_dong, le_trai, rong_cot = 46, 210, 520
    rong = le_trai + rong_cot + 90
    cao = 76 + len(es) * cao_dong + 30
    max_hong = max(sum(d.values()) for d in dem.values()) or 1

    d_out = mo_svg(rong, cao)
    d_out += [
        f'<text x="16" y="24" font-size="14" font-weight="600">{thoat(tieu_de)}</text>',
        f'<text x="16" y="42" font-size="11" fill="#475569">'
        f"Số tài liệu `failed=True`, gộp theo `failure_kind`; mẫu số là tổng lượt chạy "
        f"của chính engine đó</text>",
    ]
    x = 16
    for i, k in enumerate(loai):
        d_out.append(f'<rect x="{x}" y="52" width="10" height="10" fill="{MAU[i % len(MAU)]}"/>')
        d_out.append(f'<text x="{x + 14}" y="61" font-size="11">{thoat(k)}</text>')
        x += 20 + 7 * len(k)

    for r_i, e in enumerate(es):
        y = 76 + r_i * cao_dong
        hong = sum(dem[e].values())
        d_out.append(
            f'<text x="{le_trai - 8}" y="{y + 18}" font-size="11" text-anchor="end" '
            f'fill="#0f172a">{thoat(e)}</text>'
        )
        cx = le_trai
        for i, k in enumerate(loai):
            n = dem[e].get(k, 0)
            if not n:
                continue
            w = max(1.0, n / max_hong * rong_cot)
            d_out.append(
                f'<rect x="{cx:.1f}" y="{y + 6}" width="{w:.1f}" height="20" '
                f'fill="{MAU[i % len(MAU)]}"/>'
            )
            cx += w
        d_out.append(
            f'<text x="{cx + 6:.1f}" y="{y + 21}" font-size="10" fill="#334155">'
            f"{hong}/{tong[e]} ({hong / tong[e]:.1%})</text>"
        )

    d_out.append("</svg>")
    return _ghi(out_path, "\n".join(d_out) + "\n")
