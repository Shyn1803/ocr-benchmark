"""Deterministic Scientific Report Builder — dựa trên dữ liệu thật.

Đọc prediction/ đã chạy trên máy, chấm điểm bằng scorer thật, tính thống kê
bằng statistics.py thật, rồi sinh bài báo và bảng biểu.

**Không hardcode bất kỳ con số nào.** Mọi số trong đầu ra đều truy xuất được
về `prediction/*.json` + `ground-truth/`.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any

from ocr_bench import registry, report
from ocr_bench.corpus import load_doclaynet, load_olmocr
from ocr_bench.prediction import load_predictions
from ocr_bench.research_charts import (
    render_accuracy_speed_chart,
    render_failure_distribution_chart,
    render_forest_plot,
    render_scan_degradation_chart,
)
from ocr_bench.scorer import ScoreTable, score_results
from ocr_bench.statistics import adjust_p_values_holm, paired_compare

ROOT = Path(__file__).resolve().parents[2]


MOI_METRIC = "all_metrics"
"""Khoá năng lực dùng cho bảng tổng quan — bảng đó thật sự trải trên mọi metric."""


def moc_tat_dinh(generated_at: str | None = None) -> str:
    """Mốc thời gian **tái lập được**.

    Thứ tự: tham số truyền vào → `SOURCE_DATE_EPOCH` → đồng hồ máy.

    Trước đây mặc định là `datetime.now()`, nên tuyên bố "dựng hai lần ra byte giống
    hệt nhau" chỉ đúng khi người gọi tự truyền `generated_at` — tức là chưa từng đúng
    với lệnh dựng mặc định. `SOURCE_DATE_EPOCH` là quy ước có sẵn của giới build tái
    lập, dùng lại thay vì bịa cờ mới.
    """
    if generated_at is not None:
        return generated_at
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        moc = dt.datetime.fromtimestamp(int(epoch), dt.timezone.utc)
        return moc.isoformat(timespec="seconds").replace("+00:00", "Z")
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def slug_nang_luc(ten: str) -> str:
    """`"Text & OCR"` → `"text_ocr"` — khoá năng lực dùng trong trace ID."""
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", ten.lower())).strip("_")


def _trace(nang_luc: str, engines: list[str]) -> list[str]:
    """Một dòng trace cho **mỗi cột**, không phải một dòng phủ cả bảng.

    `aggregate:all_metrics:all_engines` là trace không truy được gì: nó không trỏ
    tới bản ghi nào trong `results/aggregate-results.json`, nên bộ kiểm chỉ có thể
    xác nhận "có chuỗi `<!-- trace:`" chứ không xác nhận được con số nào.
    """
    return [f"<!-- trace: aggregate:{nang_luc}:{e} -->" for e in engines]


def _write_lf(path: Path, content: str) -> None:
    """Write text file ensuring LF line endings and UTF-8 encoding."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode("utf-8"))


# ---------------------------------------------------------------------------
# 1. Chấm điểm thật
# ---------------------------------------------------------------------------


THU_MUC_PREDICTION_MAC_DINH = ROOT / "prediction"
"""Corpus đóng băng trong repo — nguồn của mọi bảng công bố."""


def _cham(prediction_dir: Path | None = None) -> tuple[list, ScoreTable]:
    """Nạp ground truth + prediction rồi chấm — giống hệt d1_report.py.

    `prediction_dir` cho phép chấm một corpus khác, ví dụ đầu ra pilot ở
    `calibration/prediction/cpu/`. Bản trước chốt cứng `ROOT / "prediction"` nên cờ
    `--input` của `scripts/build_research_report.py` là cờ chết: chạy pilot xong rồi
    dựng báo cáo vẫn ra bảng của corpus đóng băng, im lặng, không lệch một dòng nào
    để người đọc nhận ra.
    """
    gt: dict = {}
    gt.update(load_doclaynet())
    gt.update(load_olmocr())

    res = load_predictions(Path(prediction_dir or THU_MUC_PREDICTION_MAC_DINH))
    ten = sorted(registry.list_metrics())
    metrics = [registry.get_metric(t)() for t in ten]
    return res, score_results(res, metrics, gt)


# ---------------------------------------------------------------------------
# 2. Trích điểm thô cho thống kê ghép cặp
# ---------------------------------------------------------------------------


def _scores_per_engine(bang: ScoreTable, metric: str) -> dict[str, dict[str, float]]:
    """Trả {engine: {doc_id: value}} chỉ cho các tài liệu chấm được (value != None)."""
    ra: dict[str, dict[str, float]] = {}
    for r in bang.rows:
        if r.metric == metric and r.value is not None:
            ra.setdefault(r.engine, {})[r.doc_id] = r.value
    return ra


# ---------------------------------------------------------------------------
# 3. Sinh aggregate JSON từ ScoreTable thật
# ---------------------------------------------------------------------------


def _aggregate_json(bang: ScoreTable) -> dict:
    """Sinh dict aggregate {metric: {engine: {mean, fail_rate, n_scored, cell}}}."""
    ra: dict[str, dict[str, dict]] = {}
    for m in bang.metrics():
        ra[m] = {}
        for e in bang.engines():
            agg = bang.cell(m, e)
            ra[m][e] = {
                "mean": round(agg.mean, 4) if agg.mean is not None else None,
                "penalized_mean": (
                    round(agg.penalized_mean, 4)
                    if agg.penalized_mean is not None
                    else None
                ),
                "fail_rate": round(agg.fail_rate, 4),
                "n_total": agg.n_total,
                "n_scored": agg.n_scored,
                "n_failed": agg.n_failed,
                "applicable": agg.applicable,
                "cell": agg.cell(),
            }
    return ra


# ---------------------------------------------------------------------------
# 4. Sinh bảng Markdown từ ScoreTable thật
# ---------------------------------------------------------------------------


def _bang_theo_nhom(
    bang: ScoreTable,
    nhom_metrics: list[str],
    tieu_de: str,
    *,
    engines: list[str] | None = None,
) -> str:
    """Sinh bảng Markdown cho một nhóm metric, dùng Aggregate.cell() thật."""
    es = engines if engines is not None else bang.engines()
    cov = report.coverage(bang.rows)
    lines = [
        *_trace(slug_nang_luc(tieu_de), es),
        "",
        f"| Metric | " + " | ".join(es) + " |",
        "|---" + "|---" * len(es) + "|",
        "| **n (tài liệu)** | "
        + " | ".join(str(len(cov.get(e, ()))) for e in es)
        + " |",
    ]
    for m in nhom_metrics:
        if m not in bang.metrics():
            continue
        row = f"| `{m}` | " + " | ".join(
            bang.cell(m, e).cell() for e in es
        ) + " |"
        lines.append(row)
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# 5. Pipeline chính
# ---------------------------------------------------------------------------


def build_publication(
    input_dir: Path,
    out_dir: Path,
    *,
    generated_at: str | None = None,
    prediction_dir: Path | None = None,
) -> dict[str, Path]:
    """Run full deterministic publication build pipeline from REAL data.

    `prediction_dir` mặc định là corpus đóng băng `prediction/`. Trỏ nó sang chỗ khác
    (ví dụ `calibration/prediction/cpu`) để chấm đầu ra pilot — bảng ra khi đó là bảng
    tiến độ, **không** phải bảng công bố: corpus pilot không có `sabotage`/`noop` nên
    cổng D-010 không chạy được trên đó.

    Returns mapping of relative artifact names to generated file paths.
    """
    input_dir = Path(input_dir)
    out_dir = Path(out_dir)
    out_files: dict[str, Path] = {}
    moc = moc_tat_dinh(generated_at)

    # --- Bước 1: Chấm điểm thật ---
    res, bang = _cham(prediction_dir)
    engines = bang.engines()
    ten_metric = bang.metrics()

    print(f"nạp {len(res)} dự đoán · {len(ten_metric)} metric · {len(engines)} engine")

    # --- Bước 2: Sinh raw results (điểm thô từng tài liệu) ---
    raw_json_str = report.raw_json(bang, generated_at=moc)
    raw_path = out_dir / "results" / "raw-results.json"
    _write_lf(raw_path, raw_json_str + "\n")
    out_files["results/raw-results.json"] = raw_path

    # --- Bước 3: Sinh aggregate results ---
    agg_data = _aggregate_json(bang)
    agg_path = out_dir / "results" / "aggregate-results.json"
    _write_lf(
        agg_path,
        json.dumps(
            {"generated_at": moc, "aggregates": agg_data},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )
    out_files["results/aggregate-results.json"] = agg_path

    # --- Bước 4: Tính thống kê ghép cặp trên common set ---
    # Lấy nhóm engine chính (loại noop, sabotage)
    engine_chinh = [e for e in engines if e not in ("noop", "sabotage")]
    all_comparisons: list[dict] = []

    for m in ten_metric:
        scores = _scores_per_engine(bang, m)
        scores_chinh = {e: s for e, s in scores.items() if e in engine_chinh}
        if len(scores_chinh) < 2:
            continue
        es = sorted(scores_chinh.keys())
        comps = []
        for i in range(len(es)):
            for j in range(i + 1, len(es)):
                comp = paired_compare(
                    scores_chinh[es[i]],
                    scores_chinh[es[j]],
                    engine_a=es[i],
                    engine_b=es[j],
                )
                comps.append(comp)
        adjusted = adjust_p_values_holm(comps)
        for c in adjusted:
            all_comparisons.append({"metric": m, **c.to_dict()})

    stat_path = out_dir / "results" / "statistical-tests.json"
    _write_lf(
        stat_path,
        json.dumps(
            {"generated_at": moc, "comparisons": all_comparisons},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )
    out_files["results/statistical-tests.json"] = stat_path

    # --- Bước 5: Sinh bảng Markdown tổng quan (dùng report.bang_markdown thật) ---
    overall_md = report.bao_cao_overall(
        bang, report.dung_manifest(res, bang, generated_at=moc)
    )
    overall_path = out_dir / "tables" / "overall.md"
    _write_lf(overall_path, overall_md)
    out_files["tables/overall.md"] = overall_path

    # --- Bước 6: Sinh bảng common set (so chéo hợp lệ) ---
    cov = report.coverage(res)
    common_md = report.bao_cao_common_set(bang, cov)
    common_path = out_dir / "tables" / "common-set.md"
    _write_lf(common_path, common_md)
    out_files["tables/common-set.md"] = common_path

    # --- Bước 7: Sinh bảng theo nhóm tài liệu ---
    by_group_md = report.bao_cao_by_group(bang)
    by_group_path = out_dir / "tables" / "by-group.md"
    _write_lf(by_group_path, by_group_md)
    out_files["tables/by-group.md"] = by_group_path

    # --- Bước 8: Render SVG figures ---
    out_files["figures/capability-ranking.svg"] = render_forest_plot(
        agg_data, out_dir / "figures" / "capability-ranking.svg"
    )
    out_files["figures/accuracy-speed.svg"] = render_accuracy_speed_chart(
        agg_data, out_dir / "figures" / "accuracy-speed.svg"
    )
    out_files["figures/scan-degradation.svg"] = render_scan_degradation_chart(
        agg_data, out_dir / "figures" / "scan-degradation.svg"
    )
    out_files["figures/failure-distribution.svg"] = render_failure_distribution_chart(
        agg_data, out_dir / "figures" / "failure-distribution.svg"
    )

    # --- Bước 9: Sinh bài báo paper-vi.md ---
    paper_content = _render_paper(bang, res, agg_data, moc)
    paper_path = out_dir / "paper" / "paper-vi.md"
    _write_lf(paper_path, paper_content)
    out_files["paper/paper-vi.md"] = paper_path

    # --- Bước 10: Sinh executive summary ---
    exec_content = _render_executive_summary(bang, engines)
    exec_path = out_dir / "paper" / "executive-summary.md"
    _write_lf(exec_path, exec_content)
    out_files["paper/executive-summary.md"] = exec_path

    return out_files


# ---------------------------------------------------------------------------
# 6. Định nghĩa 6 nhóm năng lực
# ---------------------------------------------------------------------------

CAPABILITIES = {
    "Text & OCR": ["cer", "wer", "diacritics_acc", "assert_text_presence", "assert_text_absence"],
    "Layout & Structure": ["block_f1", "type_f1", "heading", "img_f1", "img_iou"],
    "Tables": ["teds", "teds_struct", "cell_f1", "table_recall", "assert_table_relation"],
    "Reading Order": ["nid", "assert_reading_order"],
    "Robustness & Base": ["assert_baseline", "assert_math_presence"],
}

# 8 profiles defined in configs/profiles.json
TARGET_PROFILES = [
    "docling_default", "docling_scan",
    "opendataloader_default", "opendataloader_scan",
    "marker_default", "marker_scan",
    "sovereign_default", "sovereign_scan"
]

# ---------------------------------------------------------------------------
# 7. Render bài báo từ dữ liệu thật
# ---------------------------------------------------------------------------


def _render_paper(
    bang: ScoreTable,
    res: list,
    agg_data: dict,
    generated_at: str,
) -> str:
    """Render bài báo paper-vi.md từ ScoreTable thật, chia theo 6 nhóm năng lực."""
    # Hiển thị các engine có thật trong dữ liệu (sẽ bao gồm cả engine cũ vì chưa migrate)
    # Nếu muốn hiện cả 8 profile (kể cả chưa chạy), có thể uncomment dòng dưới:
    # engines = sorted(list(set(TARGET_PROFILES) | set(bang.engines())))
    engines = bang.engines()
    cov = report.coverage(res)
    ten = bang.metrics()

    # Bảng tổng quan dùng report.bang_markdown thật
    bang_tong_quan = report.bang_markdown(bang, engines=engines)

    # Đọc phụ lục nếu có
    methods_path = ROOT / "paper" / "appendices" / "methods.md"
    limitations_path = ROOT / "paper" / "appendices" / "limitations.md"
    methods_text = (
        methods_path.read_text(encoding="utf-8") if methods_path.exists() else ""
    )
    limitations_text = (
        limitations_path.read_text(encoding="utf-8")
        if limitations_path.exists()
        else ""
    )

    lines = [
        "# Báo cáo Nghiên cứu So sánh Đánh giá Hiệu năng các Công cụ OCR và Phân tích Bố cục Tài liệu",
        "",
        "**Tác giả:** Đội ngũ Nghiên cứu Sovereign  ",
        f"**Ngày công bố:** {generated_at[:10]}  ",
        f"**Số engine hiển thị:** {len(engines)}  ",
        f"**Số metric:** {len(ten)}  ",
        f"**Tổng dự đoán:** {len(res)}  ",
        "",
        "---",
        "",
        "## Tóm tắt",
        "",
        f"Báo cáo này công bố kết quả đánh giá thực nghiệm trên **{len(engines)} cấu hình engine** "
        f"với **{len(ten)} metric** chuẩn hóa, phân chia thành các nhóm năng lực: "
        f"OCR, Layout, Bảng, Reading Order, Robustness và Hiệu năng.",
        "",
        "Mọi kết quả được tính toán tất định từ dữ liệu dự đoán đã đóng băng tại "
        "`prediction/` và nhãn chuẩn tại `ground-truth/`. Không sử dụng LLM trong "
        "bất kỳ công đoạn tính toán số liệu nào. Các ô hiển thị `— (0 hỏng, 0 chấm được)` "
        "là những profile chưa có đủ dữ liệu.",
        "",
        "---",
        "",
    ]

    # Cảnh báo coverage
    mani = report.dung_manifest(res, bang, generated_at=generated_at)
    canh_bao = mani.get("canh_bao", [])
    if canh_bao:
        lines += [
            "## Cảnh báo khi Đọc Bảng",
            "",
        ]
        for c in canh_bao:
            lines.append(f"- {c}")
        lines += ["", "---", ""]

    lines += [
        "## 1. Phân tích theo Từng Năng lực",
        "",
        "Báo cáo không dùng một điểm tổng duy nhất để tránh che khuất trade-off giữa các năng lực.",
        "",
    ]

    for cap_name, cap_metrics in CAPABILITIES.items():
        lines += [
            f"### Năng lực: {cap_name}",
            "",
            _bang_theo_nhom(bang, cap_metrics, cap_name, engines=engines),
            "",
        ]

    lines += [
        "---",
        "",
        "## 2. Bảng Tổng quan Toàn bộ Metric",
        "",
        *_trace(MOI_METRIC, list(engines)),
        "",
        bang_tong_quan,
        "",
        "Ô `N/A` = engine không có năng lực để metric chạm tới. "
        "`chưa có nhãn` = bộ mẫu chưa có nhãn hợp loại để đối chiếu.",
        "",
        "---",
        "",
    ]

    # Bảng common set - dùng engines thực sự có mặt để tránh lỗi
    real_engines = bang.engines()
    common_md = report.bao_cao_common_set(bang, cov)
    lines += [
        "## 3. So chéo trên Tập Tài liệu Chung",
        "",
        common_md,
        "",
        "---",
        "",
    ]

    # Phụ lục
    if methods_text:
        lines += [
            "## Phụ lục A: Phương pháp Đánh giá Chi tiết",
            "",
            methods_text,
            "",
        ]
    if limitations_text:
        lines += [
            "## Phụ lục B: Hạn chế Nghiên cứu & Phạm vi Áp dụng",
            "",
            limitations_text,
            "",
        ]

    return "\n".join(lines) + "\n"


def _render_executive_summary(bang: ScoreTable, _) -> str:
    """Render executive summary phân tách rõ năng lực, không dùng 1 điểm tổng."""
    engines = bang.engines()
    lines = [
        "# Tóm tắt Thực thi — OCR Parser Benchmark",
        "",
        "## Kết quả Tổng quan theo Từng Năng lực",
        "",
        f"Báo cáo tóm tắt hiệu năng của **{len(engines)} profile** "
        "trên bộ dữ liệu kiểm thử chuẩn. Không sử dụng một điểm số tổng duy nhất "
        "để hiển thị trung thực các trade-off.",
        "",
    ]

    # Bảng matrix Engine x Capability
    header = "| Profile | Text & OCR | Layout & Struct | Tables | Reading Order | Robustness |"
    sep = "|---|---|---|---|---|---|"
    lines += [header, sep]

    for e in engines:
        row_vals = [f"`{e}`"]
        for cap_name, cap_metrics in CAPABILITIES.items():
            scored_metrics = []
            for m in cap_metrics:
                if m in bang.metrics():
                    agg = bang.cell(m, e)
                    if agg.n_scored > 0 and agg.penalized_mean is not None:
                        scored_metrics.append(agg.penalized_mean)
            if scored_metrics:
                avg = sum(scored_metrics) / len(scored_metrics)
                row_vals.append(f"{avg:.3f}")
            else:
                row_vals.append("—")
        lines.append("| " + " | ".join(row_vals) + " |")

    lines += [""]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# 8. Validate trace
# ---------------------------------------------------------------------------


_RE_TRACE = re.compile(r"<!--\s*trace:\s*aggregate:([^:\s]+):([^\s]+?)\s*-->")


def validate_publication_trace(out_dir: Path) -> list[str]:
    """Kiểm mọi trace ID trong `paper-vi.md` có **giải được** về aggregate thật không.

    Bản trước chỉ kiểm `"<!-- trace:" in text` — một chuỗi ký tự bất kỳ là qua, kể cả
    `aggregate:all_metrics:all_engines` vốn không trỏ tới bản ghi nào. Ở đây mỗi trace
    phải nêu đúng một năng lực đã biết và đúng một engine có mặt trong
    `results/aggregate-results.json`.
    """
    out_dir = Path(out_dir)
    loi: list[str] = []
    paper_file = out_dir / "paper" / "paper-vi.md"
    if not paper_file.exists():
        return [f"Paper file {paper_file} does not exist"]

    text = paper_file.read_text(encoding="utf-8")
    traces = _RE_TRACE.findall(text)
    if not traces:
        return [f"No resolvable trace comments found in {paper_file}"]

    agg_file = out_dir / "results" / "aggregate-results.json"
    if not agg_file.exists():
        return [f"Aggregate file {agg_file} does not exist — trace không giải được"]
    agg = json.loads(agg_file.read_text(encoding="utf-8")).get("aggregates", {})

    engines_co = {e for per_engine in agg.values() for e in per_engine}
    nang_luc_co = {slug_nang_luc(k): v for k, v in CAPABILITIES.items()}

    for nang_luc, engine in traces:
        if nang_luc != MOI_METRIC and nang_luc not in nang_luc_co:
            loi.append(f"trace nêu năng lực không có thật: {nang_luc!r}")
            continue
        if engine not in engines_co:
            loi.append(
                f"trace aggregate:{nang_luc}:{engine} nêu engine không có trong "
                f"{agg_file.name}"
            )
            continue
        if nang_luc == MOI_METRIC:
            continue
        # Năng lực phải có ít nhất một metric thực sự nằm trong aggregate, nếu không
        # trace trỏ tới một bảng rỗng.
        if not any(m in agg and engine in agg[m] for m in nang_luc_co[nang_luc]):
            loi.append(
                f"trace aggregate:{nang_luc}:{engine} không giải được về metric nào"
            )

    return loi
