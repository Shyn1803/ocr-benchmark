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
from collections import Counter
from pathlib import Path
from typing import Any

from ocr_bench import glossary, registry, report
from ocr_bench.ceiling import (
    NGUONG_DO_DUOC,
    Tran,
    bang_tran,
    du_lieu_tran,
    thu_tu_metric,
    tran_do_duoc,
)
from ocr_bench.corpus import load_doclaynet, load_olmocr
from ocr_bench.metrics.perf import perf_aggregates, perf_rows
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


def _cham(
    prediction_dir: Path | None = None,
) -> tuple[list, ScoreTable, dict, dict]:
    """Nạp ground truth + prediction rồi chấm — giống hệt d1_report.py.

    Trả về cả **hai nửa ground truth** chứ không chỉ dict phẳng đã gộp: trần đo được
    (`ceiling.py`) và các bảng tách theo nửa corpus đều cần biết tài liệu nào thuộc
    nửa nào. Gộp xong mới chia lại thì không chia được — hai nửa rời nhau nhưng
    `doc_id` không mang dấu vết nửa nào.

    `prediction_dir` cho phép chấm một corpus khác, ví dụ đầu ra pilot ở
    `calibration/prediction/cpu/`. Bản trước chốt cứng `ROOT / "prediction"` nên cờ
    `--input` của `scripts/build_research_report.py` là cờ chết: chạy pilot xong rồi
    dựng báo cáo vẫn ra bảng của corpus đóng băng, im lặng, không lệch một dòng nào
    để người đọc nhận ra.
    """
    gt_layout = dict(load_doclaynet())
    gt_assert = dict(load_olmocr())
    gt: dict = {**gt_layout, **gt_assert}

    res = load_predictions(Path(prediction_dir or THU_MUC_PREDICTION_MAC_DINH))
    ten = sorted(registry.list_metrics())
    metrics = [registry.get_metric(t)() for t in ten]
    return res, score_results(res, metrics, gt), gt_layout, gt_assert


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


def _hai_nua(
    trans: dict[str, Tran], gt_layout: dict, gt_assert: dict
) -> list[report.NuaCorpus]:
    """Hai nửa corpus, metric của mỗi nửa **đã xếp theo trần đo được**.

    Metric trần 0 vẫn có mặt trong danh sách: bỏ dòng đi là giấu chuyện bộ mẫu thiếu
    nhãn, và người đọc sẽ tưởng metric đó chưa từng được cân nhắc. `tables/ceiling.md`
    nói vì sao từng dòng bằng 0.

    Metric `ca_hai` (không ràng `gt_kinds`) xuất hiện ở **cả hai** nửa — nó chấm được
    trên cả hai bộ, và mỗi lần chấm chỉ trên tài liệu của nửa đang in.
    """
    thu_tu = thu_tu_metric(trans)

    def cua(*nua: str) -> tuple[str, ...]:
        return tuple(m for m in thu_tu if trans[m].nua_corpus in nua)

    return [
        report.NuaCorpus(
            ten="DocLayNet — nhãn bố cục (bbox)",
            docs=frozenset(gt_layout),
            metrics=cua("doclaynet", "ca_hai"),
            ghi_chu=(
                f"{len(gt_layout)} tài liệu, nhãn là khung + loại khối. Không giao "
                "một tài liệu nào với nửa dưới, nên **không so ô của hai bảng với nhau**."
            ),
            slug="doclaynet",
        ),
        report.NuaCorpus(
            ten="olmOCR — nhãn khẳng định",
            docs=frozenset(gt_assert),
            metrics=cua("olmocr", "ca_hai"),
            ghi_chu=(
                f"{len(gt_assert)} tài liệu, nhãn là các khẳng định đúng/sai về nội "
                "dung. Trần đo được của từng metric xem `tables/ceiling.md`."
            ),
            slug="olmocr",
        ),
    ]


def _chon_truc_y(
    bang: ScoreTable, trans: dict[str, Tran], docs_nua: dict[str, frozenset[str]]
) -> str | None:
    """Metric làm trục Y cho `accuracy-speed.svg`: metric **tách các engine ra xa nhất**.

    Bản trước chọn metric có trần lớn nhất. Tất định thì có, nhưng vô dụng: trần lớn
    nhất ở lượt chạy này là `assert_math_presence`, nơi cả ba engine đều 0.001–0.002 và
    không cặp nào có ý nghĩa thống kê. Hình ra ba điểm bẹp dí trên đáy — trục X nói được
    điều gì đó, trục Y thì phẳng lì. Trần lớn không đồng nghĩa phân biệt tốt.

    Chọn theo `report.do_trai` tính **trên đúng nửa corpus của metric đó** (tính trên
    bảng đầy đủ thì các tài liệu của nửa kia vào làm mẫu số và dìm mọi độ trải xuống).
    Hoà thì xét trần, rồi tới tên — vẫn tất định. Bỏ qua metric ngược chiều: độ trải của
    một metric mà thấp hơn là tốt hơn không đọc theo chiều trục Y được.
    """
    ung_vien: list[tuple[float, int, str]] = []
    for m in thu_tu_metric(trans):
        t = trans[m]
        if t.bac != "do_duoc" or m in report.NGUOC_CHIEU:
            continue
        trai = report.do_trai(report.loc_theo_tai_lieu(bang, docs_nua[t.nua_corpus]), m)
        if trai is None:
            continue
        ung_vien.append((trai, t.n_toi_da, m))
    if not ung_vien:
        return None
    # `-tên` không sắp được nên đảo bằng cách lấy max theo (trải, trần) rồi tên nhỏ nhất.
    tot_nhat = max(u[:2] for u in ung_vien)
    return min(m for trai, tran, m in ung_vien if (trai, tran) == tot_nhat)


def _nhan_truc_y(metric: str, trans: dict[str, Tran], trai: float | None) -> str:
    """Nhãn trục Y nói luôn vì sao metric này được chọn, và nó có phân biệt không."""
    t = trans[metric]
    nhan = f"{metric} ({t.nua_corpus}, trần {t.n_toi_da}"
    if trai is None:
        return nhan + ", chưa đủ 2 engine để so)"
    if trai < report.NGUONG_PHAN_BIET:
        return nhan + f", trải {trai:.3f} — dưới ngưỡng phân biệt)"
    return nhan + f", trải {trai:.3f})"


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
    res, bang, gt_layout, gt_assert = _cham(prediction_dir)
    engines = bang.engines()
    ten_metric = bang.metrics()

    print(f"nạp {len(res)} dự đoán · {len(ten_metric)} metric · {len(engines)} engine")

    # --- Bước 1b: Trần đo được — chỉ từ ground truth, không đọc prediction ---
    # Đứng trước mọi bảng có engine: nó là thước để đọc các bảng đó. Một ô N/A chỉ
    # đọc được đúng khi biết trần của metric ấy là 0 (lỗi bộ mẫu) hay 203 (lỗi engine).
    trans = tran_do_duoc(gt_layout, gt_assert)
    kich_thuoc = {
        "n_doclaynet": len(gt_layout),
        "n_olmocr": len(gt_assert),
        "generated_at": moc,
    }
    tran_json_path = out_dir / "results" / "measurable-ceiling.json"
    _write_lf(tran_json_path, du_lieu_tran(trans, **kich_thuoc) + "\n")
    out_files["results/measurable-ceiling.json"] = tran_json_path

    tran_md_path = out_dir / "tables" / "ceiling.md"
    _write_lf(tran_md_path, bang_tran(trans, **kich_thuoc))
    out_files["tables/ceiling.md"] = tran_md_path

    # Chú giải sinh cùng lúc với trần, và cũng chỉ từ ground truth + docstring metric:
    # nó phải có mặt kể cả khi lượt chạy không có prediction nào, vì nó là thứ người
    # đọc mở ra trước tiên khi không hiểu một cột tên gì.
    chu_giai_path = out_dir / "tables" / "glossary.md"
    _write_lf(chu_giai_path, glossary.bang_thuat_ngu(trans, generated_at=moc))
    out_files["tables/glossary.md"] = chu_giai_path

    nua = _hai_nua(trans, gt_layout, gt_assert)

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
        bang, report.dung_manifest(res, bang, generated_at=moc), nua=nua
    )
    overall_path = out_dir / "tables" / "overall.md"
    _write_lf(overall_path, overall_md)
    out_files["tables/overall.md"] = overall_path

    # --- Bước 6: Sinh bảng common set (so chéo hợp lệ) ---
    cov = report.coverage(res)
    common_md = report.bao_cao_common_set(bang, cov, nua=nua)
    common_path = out_dir / "tables" / "common-set.md"
    _write_lf(common_path, common_md)
    out_files["tables/common-set.md"] = common_path

    # --- Bước 7: Sinh bảng theo nhóm tài liệu ---
    by_group_md = report.bao_cao_by_group(bang, nua=nua)
    by_group_path = out_dir / "tables" / "by-group.md"
    _write_lf(by_group_path, by_group_md)
    out_files["tables/by-group.md"] = by_group_path

    # --- Bước 8: Render SVG figures ---
    # Mọi hình đọc chính `bang` / `res` vừa dựng ở trên, không đọc `agg_data`: đi vòng
    # qua JSON là mở lại đúng khe cũ, nơi một khoá thiếu biến thành danh sách mặc định.
    for n in nua:
        con = report.loc_theo_tai_lieu(bang, n.docs)
        do_duoc = [m for m in n.metrics if trans[m].bac == "do_duoc"]
        if not do_duoc:
            # Không bịa một hình rỗng mang tên "xếp hạng"; ceiling.md nói vì sao trống.
            continue
        # Engine của **nửa này**, không phải của cả lượt chạy: engine không chạy tài
        # liệu nào của nửa này thì mọi ô của nó là `aggregate([])` — in ra "N/A", đọc
        # thành "engine không có năng lực" trong khi sự thật là "không có dự đoán ở
        # đây". Bỏ nó khỏi trục và ghi tên nó vào phụ đề, không đổi nó thành ô trắng.
        co_o_nua = set(con.engines())
        engines_nua = [e for e in engines if e in co_o_nua]
        vang = [e for e in engines if e not in co_o_nua]
        if not engines_nua:
            continue
        slug = n.slug or slug_nang_luc(n.ten)
        f_xh = f"figures/capability-ranking-{slug}.svg"
        out_files[f_xh] = render_forest_plot(
            con,
            out_dir / f_xh,
            engines=engines_nua,
            metrics=do_duoc,
            tieu_de=f"Xếp hạng năng lực — {n.ten}",
            phu_de=(
                f"{len(n.docs)} tài liệu · chỉ metric trần ≥{NGUONG_DO_DUOC} "
                f"(xem `tables/ceiling.md`) · trung bình có phạt"
                + (
                    f" · không có dự đoán ở nửa này: {', '.join(vang)}"
                    if vang
                    else ""
                )
            ),
        )
        # Hình scan cũng tách theo nửa: một trục chứa metric của cả hai nửa là mời
        # so hai bộ mẫu rời nhau, đúng cái `_hai_nua` sinh ra để chặn.
        f_scan = f"figures/scan-degradation-{slug}.svg"
        out_files[f_scan] = render_scan_degradation_chart(
            con,
            out_dir / f_scan,
            metrics=do_duoc,
            tieu_de=f"Suy giảm khi bật chế độ scan — {n.ten}",
        )

    docs_nua = {
        "doclaynet": frozenset(gt_layout),
        "olmocr": frozenset(gt_assert),
    }

    # Trục Y của hình tốc độ là **một** metric có tên, không phải trung bình các metric:
    # trung bình cộng qua các metric khác trần, khác nửa corpus là con số không truy được
    # về đâu.
    y_metric = _chon_truc_y(bang, trans, docs_nua)
    if y_metric is not None:
        docs_y = docs_nua[trans[y_metric].nua_corpus]
        con_y = report.loc_theo_tai_lieu(bang, docs_y)
        # Chỉ engine có dự đoán trên nửa chứa `y_metric`. `con_y.cell()` của engine
        # vắng mặt là `aggregate([])` → in "N/A", tức "engine không có năng lực" —
        # sai lý do. Engine bị loại được gọi tên ở chú thích chân hình.
        co_y = set(con_y.engines())
        perf_y = {
            p.engine: p for p in perf_aggregates(perf_rows(res)) if p.engine in co_y
        }
        vang_y = sorted(
            {p.engine for p in perf_aggregates(perf_rows(res))} - set(perf_y)
        )
        if perf_y:
            out_files["figures/accuracy-speed.svg"] = render_accuracy_speed_chart(
                perf_y,
                {e: con_y.cell(y_metric, e) for e in perf_y},
                out_dir / "figures" / "accuracy-speed.svg",
                nhan_y=_nhan_truc_y(y_metric, trans, report.do_trai(con_y, y_metric)),
                ghi_chu_them=(
                    [f"Không có dự đoán trên nửa {trans[y_metric].nua_corpus}: "
                     f"{', '.join(vang_y)}."]
                    if vang_y
                    else []
                ),
            )

    out_files["figures/failure-distribution.svg"] = render_failure_distribution_chart(
        res, out_dir / "figures" / "failure-distribution.svg"
    )

    # --- Bước 9: Sinh bài báo paper-vi.md ---
    paper_content = _render_paper(
        bang,
        res,
        moc,
        nguon_prediction=duong_dan_hien(
            Path(prediction_dir or THU_MUC_PREDICTION_MAC_DINH)
        ),
        trans=trans,
        nua=nua,
        so_sanh=all_comparisons,
        # Chỉ hình **thật sự sinh ra** ở lượt này. Nhúng theo danh sách cứng thì
        # lượt thiếu một họ engine sẽ để lại một ảnh vỡ trong bài báo.
        hinh={
            k.removeprefix("figures/"): v
            for k, v in out_files.items()
            if k.startswith("figures/")
        },
    )
    paper_path = out_dir / "paper" / "paper-vi.md"
    _write_lf(paper_path, paper_content)
    out_files["paper/paper-vi.md"] = paper_path

    # --- Bước 10: Sinh executive summary ---
    exec_content = _render_executive_summary(bang, trans, docs_nua=docs_nua)
    exec_path = out_dir / "paper" / "executive-summary.md"
    _write_lf(exec_path, exec_content)
    out_files["paper/executive-summary.md"] = exec_path

    return out_files


# ---------------------------------------------------------------------------
# 6. Định nghĩa 6 nhóm năng lực
# ---------------------------------------------------------------------------

def duong_dan_hien(p: Path) -> str:
    """Đường dẫn để **in ra**: tương đối với gốc repo nếu nằm trong, không thì tuyệt đối.

    Tương đối để hai máy dựng ra cùng một byte; `posix` để không lẫn `\\` vào markdown.
    """
    p = Path(p).resolve()
    try:
        return p.relative_to(ROOT).as_posix() + "/"
    except ValueError:
        return p.as_posix() + "/"


CAPABILITIES = {
    "Text & OCR": ["cer", "wer", "diacritics_acc", "assert_text_presence", "assert_text_absence"],
    "Layout & Structure": ["block_f1", "type_f1", "heading", "img_f1", "img_iou"],
    "Tables": ["teds", "teds_struct", "cell_f1", "table_recall", "assert_table_relation"],
    "Reading Order": ["nid", "assert_reading_order"],
    "Robustness & Base": ["assert_baseline", "assert_math_presence"],
}

# `TARGET_PROFILES` đã bị xoá: nó liệt kê 8 profile trong đó `marker_*` và `sovereign_*`
# chưa từng chạy lượt nào, và chỗ duy nhất dùng nó là một dòng comment mời hợp nhất nó
# vào danh sách engine hiển thị. Engine hiển thị suy từ `bang.engines()` — tức từ
# prediction có thật — chứ không từ một danh sách mong muốn.

# ---------------------------------------------------------------------------
# 7. Render bài báo từ dữ liệu thật
# ---------------------------------------------------------------------------


def _bo_tieu_de_dau(md: str) -> str:
    """Bỏ dòng `# …` đầu tiên (và dòng trống ngay sau) của một tài liệu đem nhúng."""
    dong = md.splitlines()
    for i, d in enumerate(dong):
        if not d.strip():
            continue
        if d.startswith("# "):
            j = i + 1
            while j < len(dong) and not dong[j].strip():
                j += 1
            return "\n".join(dong[:i] + dong[j:])
        break
    return md


def _ha_cap_tieu_de(md: str, muc: int) -> str:
    """Hạ mọi tiêu đề ATX của một đoạn markdown nhúng xuống `muc` bậc.

    `report.bao_cao_common_set` là một **tài liệu độc lập** — nó mở bằng `#`. Nhúng
    nguyên xi vào giữa bài báo thì bài có hai `#` cấp một, và mọi mục lục sinh tự động
    cắt bài làm đôi ở đúng chỗ đó. Bỏ qua nội dung trong khối ```` ``` ````: một dòng
    `# comment` trong ví dụ lệnh không phải tiêu đề.
    """
    ra: list[str] = []
    trong_code = False
    for dong in md.splitlines():
        if dong.lstrip().startswith("```"):
            trong_code = not trong_code
        elif not trong_code and dong.startswith("#"):
            dong = "#" * muc + dong
        ra.append(dong)
    return "\n".join(ra)


DOC_HINH: dict[str, str] = {
    "capability-ranking": (
        "Mỗi hàng là một metric, mỗi điểm là một engine; trục ngang là trung bình có "
        "phạt. Chỉ vẽ metric bậc *đo được* — metric trần thấp nằm ở `tables/ceiling.md`, "
        "không lên hình, vì một điểm dựng trên 9 tài liệu trông y hệt một điểm dựng "
        "trên 203 tài liệu."
    ),
    "scan-degradation": (
        "So `*_default` với `*_scan` của **cùng một họ engine**. Cột hướng xuống nghĩa "
        "là bật chế độ scan làm điểm tệ đi. Họ engine thiếu một trong hai profile thì "
        "không có cột — hình ghi rõ thiếu cái gì thay vì vẽ cột 0."
    ),
    "accuracy-speed": (
        "Trục ngang là **giây mỗi trang, trung vị**; trục dọc là một metric có tên "
        "(metric tách các engine ra xa nhất, tên metric ghi ngay trên trục). Góc trên "
        "bên trái là vừa nhanh vừa đúng. Đọc kèm hai hạn chế in ở chân hình: `seconds` "
        "gồm cả thời gian nạp model, và thứ tự chạy không khôi phục được nên không tách "
        "được lượt nguội."
    ),
    "failure-distribution": (
        "Tài liệu engine **không xử lý được**, tách theo loại hỏng. Đây là con số đứng "
        "cạnh mọi điểm trong báo cáo: một engine điểm cao trên phần nó chạy được mà hỏng "
        "20% đầu vào thì không dùng được, và bảng điểm một mình không nói ra điều đó."
    ),
}
"""Cách đọc từng hình, tra theo tiền tố tên file — không theo tên đầy đủ.

Hình xếp hạng và hình scan tách theo nửa corpus nên tên file mang hậu tố `-doclaynet` /
`-olmocr`; cách đọc thì giống nhau, viết một lần.
"""


TEN_HINH: dict[str, str] = {
    "capability-ranking": "Xếp hạng engine theo từng metric",
    "scan-degradation": "Bật chế độ scan thì điểm đổi thế nào",
    "accuracy-speed": "Nhanh và đúng: đánh đổi giữa hai bên",
    "failure-distribution": "Tài liệu engine không xử lý được",
}
"""Tiêu đề mục cho từng hình, tra theo tiền tố tên file.

Bản trước lấy thẳng tên file làm tiêu đề mục (`### accuracy-speed.svg`), nên mục lục
bài báo là một danh sách tên file — người đọc phải mở từng hình mới biết hình nào nói
chuyện gì. Tên file vẫn in, nhưng ở dòng chú thích dưới hình, không làm tiêu đề.
"""

NUA_TRONG_TEN_HINH: dict[str, str] = {
    "doclaynet": "nửa DocLayNet",
    "olmocr": "nửa olmOCR",
}
"""Hậu tố nửa corpus trong tên file → cụm chữ ghép vào tiêu đề."""


def _cach_doc_hinh(ten_file: str) -> str:
    for tien_to, mo_ta in DOC_HINH.items():
        if ten_file.startswith(tien_to):
            return mo_ta
    return ""


def _tieu_de_hinh(ten_file: str) -> str:
    """Tên file → tiêu đề mục đọc được. Không tra được thì trả lại chính tên file."""
    goc = Path(ten_file).stem
    for tien_to, ten in TEN_HINH.items():
        if not goc.startswith(tien_to):
            continue
        duoi = goc[len(tien_to) :].strip("-")
        nua = NUA_TRONG_TEN_HINH.get(duoi)
        return f"{ten} — {nua}" if nua else ten
    return ten_file


def _dan_dau_theo_nua(
    bang: ScoreTable, trans: dict[str, Tran], nua: list[report.NuaCorpus]
) -> dict[str, tuple[Counter[str], int, dict[str, str]]]:
    """Ai dẫn đầu ở nửa nào — tính **một lần**, dùng lại ở tóm tắt, mục 3 và mục 6.

    Trước đây phép đếm này nằm gọn trong mục 6. Tóm tắt đầu bài vì thế không có một
    kết quả nào, và người đọc phải đi hết 600 dòng bảng mới biết bài báo kết luận gì.
    Chép phép đếm ra chỗ thứ hai thì hai chỗ sẽ trôi khác nhau, nên nó thành hàm.

    "Dẫn đầu" chỉ tính trên metric vừa **đo được** (bậc `do_duoc`) vừa **phân biệt
    được** (độ trải ≥ ngưỡng) và không ngược chiều: dẫn đầu ở một metric mà mọi engine
    chênh nhau 0.002 là dẫn đầu trong sai số, đếm nó vào là đếm nhiễu.

    Trả `{khoá nửa: (đếm theo engine, số metric xét, {metric: engine dẫn đầu})}`.
    """
    ra: dict[str, tuple[Counter[str], int, dict[str, str]]] = {}
    for n in nua:
        con = report.loc_theo_tai_lieu(bang, n.docs)
        dem: Counter[str] = Counter()
        theo_metric: dict[str, str] = {}
        for m in n.metrics:
            if trans[m].bac != "do_duoc" or m in report.NGUOC_CHIEU:
                continue
            trai = report.do_trai(con, m)
            if trai is None or trai < report.NGUONG_PHAN_BIET:
                continue
            xep = [a for a in con.ranking(m) if a.n_scored > 0]
            if not xep:
                continue
            theo_metric[m] = xep[0].engine
            dem[xep[0].engine] += 1
        ra[n.slug or n.ten] = (dem, len(theo_metric), theo_metric)
    return ra


def _muc_ket_luan(
    bang: ScoreTable,
    res: list,
    trans: dict[str, Tran],
    nua: list[report.NuaCorpus],
    so_sanh: list[dict],
) -> list[str]:
    """Kết luận **suy ra từ bảng vừa in**, không phải một đoạn văn viết tay.

    Ba câu hỏi người đọc mang tới: chạy nhanh nhất là ai, đúng nhất là ai, và câu trả
    lời đó chắc tới đâu. Mỗi câu trả lời ở đây là một phép đếm trên chính `bang` và
    `res` — đổi dữ liệu thì kết luận đổi theo, không có chỗ nào để một câu cũ sống sót.

    "Dẫn đầu" chỉ tính trên metric vừa **đo được** (bậc `do_duoc`) vừa **phân biệt
    được** (độ trải ≥ ngưỡng) và không ngược chiều: dẫn đầu ở một metric mà mọi engine
    chênh nhau 0.002 là dẫn đầu trong sai số, đếm nó vào là đếm nhiễu.
    """
    lines = [
        "## 6. Kết luận & Khuyến nghị",
        "",
        "Mục này không thêm dữ liệu mới — nó đếm lại các bảng ở trên theo ba câu hỏi "
        "thường gặp. Mọi con số đều tra ngược được về mục tương ứng.",
        "",
    ]

    # --- Tốc độ: từ chính prediction, không từ bảng điểm ---
    perf = sorted(
        perf_aggregates(perf_rows(res)),
        key=lambda p: (
            p.sec_moi_trang_trung_vi is None,
            p.sec_moi_trang_trung_vi or 0.0,
            p.engine,
        ),
    )
    if perf:
        lines += [
            "### 6.1 Tốc độ",
            "",
            "| engine | giây/trang (trung vị) | tài liệu đo được | tỉ lệ hỏng |",
            "|---|---:|---:|---:|",
        ]
        for p in perf:
            tv = (
                "—"
                if p.sec_moi_trang_trung_vi is None
                else f"{p.sec_moi_trang_trung_vi:.2f}"
            )
            lines.append(
                f"| `{p.engine}` | {tv} | {p.n_do_duoc} | {p.fail_rate:.0%} |"
            )
        lines += [
            "",
            "`seconds` đo được ở mọi tài liệu nhưng **gồm cả thời gian nạp model** "
            "(`model_load_seconds` không đo được ở lượt chạy này), và thứ tự chạy không "
            "khôi phục được từ prediction nên không tách được lượt nguội. Con số này so "
            "được giữa các engine, không đọc thành thông lượng ổn định của một dịch vụ.",
            "",
        ]

    # --- Dẫn đầu: đếm trên từng nửa corpus ---
    dan_dau_nua = _dan_dau_theo_nua(bang, trans, nua)
    lines += ["### 6.2 Ai dẫn đầu, trên nửa corpus nào", ""]
    for n in nua:
        dem, xet, theo_metric = dan_dau_nua[n.slug or n.ten]
        lines += [
            f"**{n.ten}** — {xet} metric vừa đo được vừa phân biệt được các engine.",
            "",
        ]
        if not xet:
            lines += [
                "Không metric nào của nửa này tách được các engine ra: hoặc trần quá "
                "thấp, hoặc các engine chênh nhau dưới ngưỡng. Không có engine dẫn đầu "
                "để nêu tên.",
                "",
            ]
            continue
        lines += ["| engine | số metric dẫn đầu | dẫn đầu ở metric nào |", "|---|---:|---|"]
        for e in sorted(dem, key=lambda e: (-dem[e], e)):
            ten = ", ".join(
                f"`{m}`" for m in sorted(theo_metric) if theo_metric[m] == e
            )
            lines.append(f"| `{e}` | {dem[e]}/{xet} | {ten} |")
        lines += [""]

    # --- Độ chắc của các so sánh ---
    trang_thai = Counter(str(c.get("status", "?")) for c in so_sanh)
    if trang_thai:
        lines += [
            "### 6.3 Các so sánh có chắc không",
            "",
            f"{sum(trang_thai.values())} cặp engine × metric được kiểm ghép cặp trên "
            "tập tài liệu chung, p-value đã hiệu chỉnh Holm:",
            "",
            "| kết luận thống kê | số cặp |",
            "|---|---:|",
        ]
        for tt in sorted(trang_thai):
            lines.append(f"| `{tt}` | {trang_thai[tt]} |")
        lines += [
            "",
            "`not_significant` **không** nghĩa là hai engine như nhau — nghĩa là dữ "
            "liệu hiện có không đủ để nói chúng khác nhau. Chi tiết từng cặp ở "
            "`results/statistical-tests.json`.",
            "",
        ]

    # --- Khuyến nghị: một luật nói thẳng, áp lên các số vừa đếm ---
    lines += ["### 6.4 Khuyến nghị", "", "Luật áp dụng, nói trước khi ra kết luận:", ""]
    nhanh = perf[0] if perf and perf[0].sec_moi_trang_trung_vi is not None else None
    if nhanh is not None:
        lines += [
            f"- **Cần thông lượng** → chọn theo giây/trang trung vị thấp nhất: "
            f"`{nhanh.engine}` ({nhanh.sec_moi_trang_trung_vi:.2f} s/trang, hỏng "
            f"{nhanh.fail_rate:.0%}).",
        ]
    for n in nua:
        dem, xet, _ = dan_dau_nua[n.slug or n.ten]
        if not dem:
            lines.append(
                f"- **{n.ten}** → không khuyến nghị được: không metric nào của nửa này "
                "phân biệt được các engine."
            )
            continue
        top = min(dem, key=lambda e: (-dem[e], e))
        hoa = [e for e in dem if dem[e] == dem[top]]
        p = {p.engine: p for p in perf}.get(top)
        hong = f", hỏng {p.fail_rate:.0%}" if p else ""
        if len(hoa) > 1:
            lines.append(
                f"- **{n.ten}** → hoà ở {dem[top]}/{xet} metric giữa "
                + ", ".join(f"`{e}`" for e in sorted(hoa))
                + " — chọn theo tốc độ hoặc theo metric cụ thể mục 3, không có engine "
                "trội chung."
            )
        else:
            lines.append(
                f"- **{n.ten}** → `{top}` dẫn đầu {dem[top]}/{xet} metric phân biệt "
                f"được{hong}."
            )
    lines += [
        "",
        "Không có khuyến nghị \"engine tốt nhất\" chung cho cả bộ mẫu: hai nửa corpus "
        "không giao một tài liệu nào, nên một thứ hạng gộp sẽ là thứ hạng của phép "
        "cộng, không phải của engine.",
        "",
        "---",
        "",
    ]
    return lines


def _ket_qua_mot_doan(
    bang: ScoreTable, res: list, trans: dict[str, Tran], nua: list[report.NuaCorpus]
) -> list[str]:
    """Kết quả gói trong mấy gạch đầu dòng, đặt ở ngay đầu bài.

    Tóm tắt bản trước chỉ nói **phạm vi** — bao nhiêu engine, bao nhiêu metric, dữ liệu
    lấy ở đâu — mà không nói một kết quả nào, nên người đọc phải đi hết 600 dòng bảng
    tới mục 6 mới biết bài kết luận gì. Các số ở đây lấy từ đúng hai phép đếm của mục
    6.1 và 6.2, không tính lại theo cách khác.
    """
    perf = sorted(
        (p for p in perf_aggregates(perf_rows(res)) if p.sec_moi_trang_trung_vi),
        key=lambda p: (p.sec_moi_trang_trung_vi, p.engine),
    )
    ra = ["**Kết quả trong một đoạn.**", ""]
    if perf:
        ra.append(
            f"- Nhanh nhất: `{perf[0].engine}` "
            f"({perf[0].sec_moi_trang_trung_vi:.2f} giây/trang, trung vị) — chậm nhất "
            f"`{perf[-1].engine}` ({perf[-1].sec_moi_trang_trung_vi:.2f}), "
            f"chênh khoảng {perf[-1].sec_moi_trang_trung_vi / perf[0].sec_moi_trang_trung_vi:.0f} lần."
        )
    for n in nua:
        dem, xet, _ = _dan_dau_theo_nua(bang, trans, nua)[n.slug or n.ten]
        if not xet:
            ra.append(
                f"- {n.ten}: không metric nào tách được các engine ra — nửa này chưa "
                "kết luận được ai hơn ai."
            )
            continue
        top = min(dem, key=lambda e: (-dem[e], e))
        hoa = sorted(e for e in dem if dem[e] == dem[top])
        if len(hoa) > 1:
            ra.append(
                f"- {n.ten}: hoà {dem[top]}/{xet} metric giữa "
                + ", ".join(f"`{e}`" for e in hoa)
                + " — không có engine trội chung."
            )
        else:
            ra.append(
                f"- {n.ten}: `{top}` dẫn đầu {dem[top]}/{xet} metric phân biệt được."
            )
    ra += [
        "",
        "Ba dòng trên là toàn bộ kết luận; phần còn lại của bài nói vì sao chúng đứng "
        "được và ở đâu chúng không đứng được.",
        "",
    ]
    return ra


def _ban_do_doc() -> list[str]:
    """Mỗi mục trả lời câu hỏi nào — đặt trước khi người đọc bước vào mục 1.

    Người đọc lần đầu gặp sáu tiêu đề kiểu "Trần Đo được", "So chéo trên Tập Tài liệu
    Chung" thì không biết mục nào trả lời câu hỏi của mình, nên đọc tuần tự từ đầu và
    lạc ở mục 3. Bảng này nói thẳng mục nào trả lời gì để họ nhảy thẳng tới đó.
    """
    return [
        "**Bài này bố cục thế nào.** Mỗi mục trả lời đúng một câu hỏi:",
        "",
        "| mục | trả lời câu hỏi |",
        "|---|---|",
        "| 1. Đọc kết quả thế nào | `0.790 (n=203, fail 1%)` nghĩa là gì, mỗi metric đo cái gì |",
        "| 2. Trần đo được | ô trống là vì engine kém hay vì bộ mẫu thiếu nhãn |",
        "| 3. Kết quả theo nhóm năng lực | điểm từng engine, tách theo hai nửa corpus |",
        "| 4. Hình | vẫn số đó, nhìn bằng mắt |",
        "| 5. So chéo | so từng cặp engine trên đúng tập tài liệu cả hai cùng chấm được |",
        "| 6. Kết luận | nhanh nhất là ai, đúng nhất là ai, chắc tới đâu |",
        "",
        "Cần câu trả lời ngay thì đọc mục 6. Cần biết một con số có tin được không thì "
        "đọc mục 2 trước mục 3.",
        "",
    ]


def _render_paper(
    bang: ScoreTable,
    res: list,
    generated_at: str,
    *,
    nguon_prediction: str,
    trans: dict[str, Tran],
    nua: list[report.NuaCorpus],
    so_sanh: list[dict],
    hinh: dict[str, Path],
) -> str:
    """Render bài báo paper-vi.md từ ScoreTable thật.

    Bố cục theo đúng thứ tự người đọc cần: metric nghĩa là gì → đo được tới đâu → kết
    quả (tách theo nửa corpus) → hình → so chéo → kết luận. Bản trước mở thẳng bằng
    bảng điểm, và mọi bảng trộn hai nửa corpus rời nhau vào chung một cột.

    `agg_data` đã bị bỏ khỏi tham số: nó được truyền vào nhưng thân hàm chưa từng đọc,
    nên nó chỉ tạo ấn tượng bài báo đi qua JSON gộp trong khi thật ra nó đọc `bang`.
    """
    engines = bang.engines()
    cov = report.coverage(res)
    ten = bang.metrics()

    # Đọc phụ lục nếu có. **Không** thêm tiêu đề: hai file đã tự mở bằng `## Phụ lục A`
    # / `## Phụ lục B` ở dòng đầu, nên bản trước in tiêu đề hai lần liên tiếp.
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
        *_ket_qua_mot_doan(bang, res, trans, nua),
        f"Báo cáo này công bố kết quả đánh giá thực nghiệm trên **{len(engines)} cấu hình engine** "
        f"với **{len(ten)} metric** chuẩn hóa, phân chia thành các nhóm năng lực: "
        f"OCR, Layout, Bảng, Reading Order, Robustness và Hiệu năng.",
        "",
        "Bộ mẫu gồm **hai nửa rời nhau** — "
        + " và ".join(f"{n.ten} ({len(n.docs)} tài liệu)" for n in nua)
        + " — giao nhau **0 tài liệu**. Mọi bảng dưới đây đều tách theo hai nửa đó; "
        "không bảng nào đặt một metric của nửa này cạnh một metric của nửa kia, và "
        "không có điểm tổng nào cộng ngang qua chúng.",
        "",
        # In **đúng** thư mục đã chấm. Câu cũ ghi cứng `prediction/` kể cả khi báo cáo
        # dựng từ `calibration/prediction/cpu/`, tức là dòng nói về xuất xứ lại là dòng
        # sai xuất xứ.
        f"Mọi kết quả được tính toán tất định từ dữ liệu dự đoán tại "
        f"`{nguon_prediction}` và nhãn chuẩn tại `ground-truth/`. Không sử dụng LLM trong "
        "bất kỳ công đoạn tính toán số liệu nào. Các ô hiển thị `— (0 hỏng, 0 chấm được)` "
        "là những profile chưa có đủ dữ liệu.",
        "",
        *_ban_do_doc(),
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
        lines += [
            "",
            # Cảnh báo sinh cho `overall.md`, nơi `common-set.md` là một file cạnh bên.
            # Trong bài báo thì nó là mục 5 — người đọc gặp một tên file không có trong
            # bài và không biết phải mở cái gì.
            "Trong bài báo này, `common-set.md` chính là **mục 5**: ở đó mỗi bảng chỉ "
            "chấm trên tài liệu mà mọi engine trong bảng đều xử lý được, nên hai ô "
            "cạnh nhau mới so được với nhau.",
            "",
            "---",
            "",
        ]

    # --- 1. Mỗi metric đo cái gì -------------------------------------------
    # Đứng **trước** mọi bảng điểm. Bản trước mở thẳng bằng bảng, nên người đọc gặp
    # `type_f1 | 0.542` trước khi có bất kỳ đường nào biết `type_f1` đo cái gì.
    mo_ta = glossary.cac_mo_ta()
    lines += [
        "## 1. Đọc Kết quả Thế nào",
        "",
        "### 1.1 Một ô trong bảng nói gì",
        "",
        # Khối này đứng trước bảng metric, không phải sau: người đọc gặp `0.790` rồi mới
        # đi tìm nghĩa thì đã kịp hiểu nó thành "đúng 79%".
        *glossary.doc_mot_o(),
        "### 1.2 Mỗi metric đo cái gì",
        "",
        "Mô tả lấy thẳng từ định nghĩa của chính lớp metric trong mã nguồn, không chép "
        "tay — sửa luật chấm mà quên sửa mô tả là không biểu diễn được. Cột *trần* "
        "(*ceiling*) là số tài liệu nhiều nhất metric chấm được với bộ nhãn hiện có "
        "(mục 2) — cột này giải thích ở mục 2 ngay dưới đây. Bảng thuật ngữ đầy đủ: "
        "`tables/glossary.md`.",
        "",
        *glossary.cac_ho_diem(),
    ]
    for cap_name, cap_metrics in CAPABILITIES.items():
        lines += [
            f"#### {cap_name}",
            "",
            "| metric | nửa corpus | trần | đo cái gì |",
            "|---|---|---:|---|",
        ]
        for m in cap_metrics:
            t = trans.get(m)
            lines.append(
                f"| `{m}` | {t.nua_corpus if t else '?'} | "
                f"{t.n_toi_da if t else '?'} | {mo_ta.get(m) or '—'} |"
            )
        lines += [""]
    lines += [
        report.NGUOC_CHIEU["cell_f1"],
        "",
        "---",
        "",
    ]

    # --- 2. Trần đo được ----------------------------------------------------
    bac_dem = Counter(t.bac for t in trans.values())
    tran_0 = sorted(m for m, t in trans.items() if t.bac == "tran_0")
    lines += [
        "## 2. Trần Đo được của Bộ mẫu (*measurable ceiling*)",
        "",
        "Trần tính **chỉ từ nhãn**, trước khi chạy engine nào: nó là giới hạn của bộ "
        "mẫu, không phải của engine. Một ô trống chỉ đọc được đúng khi biết trần của "
        "metric ấy là 0 (bộ mẫu thiếu nhãn) hay 203 (engine không làm được).",
        "",
        "| bậc | số metric | nghĩa |",
        "|---|---:|---|",
        f"| đo được | {bac_dem.get('do_duoc', 0)} | trần ≥ {NGUONG_DO_DUOC} tài liệu "
        "— kết luận đứng được |",
        f"| mỏng | {bac_dem.get('mong', 0)} | trần thấp — đọc được, nhưng mỗi tài liệu "
        "kéo điểm rất mạnh |",
        f"| trần 0 | {bac_dem.get('tran_0', 0)} | bộ mẫu **không có nhãn** để chấm; "
        "engine không liên quan |",
        "",
    ]
    if tran_0:
        lines += [
            "Metric trần 0 ở lượt này: "
            + ", ".join(f"`{m}`" for m in tran_0)
            + ". Chúng vẫn được in trong mọi bảng, ô ghi lý do — bỏ dòng đi là giấu "
            "chuyện bộ mẫu thiếu nhãn.",
            "",
        ]
    lines += [
        "Từng dòng kèm lý do: `tables/ceiling.md` · dữ liệu máy đọc: "
        "`results/measurable-ceiling.json`.",
        "",
        "---",
        "",
        "## 3. Kết quả theo Nhóm Năng lực",
        "",
        "Báo cáo không dùng một điểm tổng duy nhất — điểm tổng che mất trade-off giữa "
        "các năng lực, và ở đây nó còn phải cộng ngang qua hai bộ tài liệu rời nhau. "
        "Mỗi bảng dưới đây thuộc **một** nửa corpus, lọc về đúng tài liệu của nửa đó.",
        "",
    ]

    # --- 3. Kết quả, tách theo nửa corpus -----------------------------------
    # Mỗi nửa mở bằng một câu kết quả trước khi vào bảng: bảng tổng quan của nửa
    # DocLayNet có 7 trên 13 dòng ghi `chưa có nhãn`, nên người đọc lướt qua nó và
    # không mang theo được gì. Câu này nói trước bảng nói cái gì.
    dan_dau = _dan_dau_theo_nua(bang, trans, nua)
    for n in nua:
        con = report.loc_theo_tai_lieu(bang, n.docs)
        co_o_nua = set(con.engines())
        engines_nua = [e for e in engines if e in co_o_nua]
        lines += [f"### {n.ten}", "", n.ghi_chu, ""]
        dem_n, xet_n, theo_metric_n = dan_dau[n.slug or n.ten]
        if xet_n:
            top_n = min(dem_n, key=lambda e: (-dem_n[e], e))
            hoa_n = sorted(e for e in dem_n if dem_n[e] == dem_n[top_n])
            ai = (
                "hoà giữa " + ", ".join(f"`{e}`" for e in hoa_n)
                if len(hoa_n) > 1
                else f"`{top_n}` dẫn đầu"
            )
            lines += [
                f"**Đọc nhanh.** Trong {len(n.metrics)} metric của nửa này, {xet_n} "
                f"metric vừa đo được vừa tách được các engine ra ("
                + ", ".join(f"`{m}`" for m in sorted(theo_metric_n))
                + f"); trên số đó, {ai} với {dem_n[top_n]}/{xet_n}. Các dòng còn lại "
                "ghi `chưa có nhãn` hoặc `N/A` — đó là giới hạn của bộ mẫu, không phải "
                "điểm 0 của engine.",
                "",
            ]
        else:
            lines += [
                f"**Đọc nhanh.** Không metric nào trong {len(n.metrics)} metric của "
                "nửa này vừa đo được vừa tách được các engine ra, nên nửa này không "
                "kết luận được ai hơn ai — xem mục 2 để biết vì sao.",
                "",
            ]
        if not engines_nua:
            lines += ["Không engine nào có dự đoán trên nửa này.", ""]
            continue
        vang = [e for e in engines if e not in co_o_nua]
        if vang:
            lines += [
                "Không có dự đoán ở nửa này: "
                + ", ".join(f"`{e}`" for e in vang)
                + " — bỏ khỏi bảng thay vì in `N/A`, vì `N/A` đọc thành \"engine "
                "không có năng lực\".",
                "",
            ]
        for cap_name, cap_metrics in CAPABILITIES.items():
            trong_nua = [m for m in cap_metrics if m in n.metrics]
            if not trong_nua:
                continue
            lines += [
                f"#### {cap_name}",
                "",
                _bang_theo_nhom(con, trong_nua, cap_name, engines=engines_nua),
                "",
            ]
        lines += [
            f"##### {n.ten} — tổng quan mọi metric của nửa này",
            "",
            _bang_theo_nhom(con, list(n.metrics), MOI_METRIC, engines=engines_nua),
            "",
            "Ô `N/A` = engine không có năng lực để metric chạm tới. "
            "`chưa có nhãn` = bộ mẫu chưa có nhãn hợp loại để đối chiếu (mục 2).",
            "",
        ]
    lines += ["---", ""]

    # --- 4. Hình ------------------------------------------------------------
    # Chỉ nhúng hình **đã sinh ra thật**: `hinh` là tập con figures của `out_files`.
    # Viết cứng 6 đường dẫn thì một hình bị bỏ qua (nửa corpus không có metric đo được)
    # để lại một ảnh vỡ, và ảnh vỡ trông giống hệt lỗi hiển thị chứ không giống "không
    # có dữ liệu".
    if hinh:
        lines += [
            "## 4. Hình",
            "",
            "Mọi hình vẽ từ chính bảng ở mục 3 — không hình nào có nguồn riêng.",
            "",
        ]
        for rel in sorted(hinh):
            ten_file = Path(rel).name
            lines += [
                f"### {_tieu_de_hinh(ten_file)}",
                "",
                f"![{ten_file}](../figures/{ten_file})",
                "",
                f"*File: `figures/{ten_file}`*",
                "",
            ]
            cach_doc = _cach_doc_hinh(ten_file)
            if cach_doc:
                lines += [f"**Cách đọc.** {cach_doc}", ""]
        lines += ["---", ""]

    # --- 5. So chéo ---------------------------------------------------------
    # `bao_cao_common_set` là tài liệu độc lập, mở bằng `#`. Hạ 2 bậc để nó nằm gọn
    # dưới mục này thay vì cắt bài báo làm đôi ở giữa.
    lines += [
        "## 5. So chéo trên Tập Tài liệu Chung",
        "",
        # Bỏ H1 riêng của tài liệu đứng một mình — nhúng vào đây thì `## 5.` ở trên đã
        # là tiêu đề của nó, in tiếp là hai dòng tiêu đề cùng nghĩa chồng lên nhau.
        _ha_cap_tieu_de(
            _bo_tieu_de_dau(report.bao_cao_common_set(bang, cov, nua=nua)), 2
        ),
        "",
        "---",
        "",
    ]

    # --- 6. Kết luận --------------------------------------------------------
    lines += _muc_ket_luan(bang, res, trans, nua, so_sanh)

    # --- Phụ lục ------------------------------------------------------------
    # Không thêm dòng tiêu đề: cả hai file mở sẵn bằng `## Phụ lục A` / `## Phụ lục B`.
    if methods_text:
        lines += [methods_text, ""]
    if limitations_text:
        lines += [limitations_text, ""]

    return "\n".join(lines) + "\n"


def _render_executive_summary(
    bang: ScoreTable, trans: dict[str, Tran], *, docs_nua: dict[str, frozenset[str]]
) -> str:
    """Mỗi nhóm năng lực: đo được mấy metric, và **từng** metric ai dẫn đầu, kèm `n`.

    Bản trước in trung bình cộng `penalized_mean` của các metric trong cùng nhóm. Con
    số đó không truy được về đâu: nó trộn metric trần 203 với metric trần 17, trộn hai
    nửa corpus rời nhau, và nuốt mất `n` lẫn `fail_rate` vì đi qua f-string thô thay vì
    `Aggregate.cell()`. Ở đây không còn phép trung bình nào giữa các metric — mỗi dòng
    là một metric có tên, một engine có tên, một cỡ mẫu có thật.

    Mỗi metric chấm trên **nửa corpus của chính nó** (`docs_nua`), không trên cả bảng.
    Chấm trên cả bảng thì `cer` — trần 0, nửa `doclaynet`, 204 tài liệu — in ra "chưa
    có nhãn (1595 tài liệu)": con số 1595 gộp luôn 1403 tài liệu olmOCR vốn không
    thuộc nửa của nó. Cột `nửa corpus` nói một đằng, cỡ mẫu nói một nẻo.
    """
    con_nua = {k: report.loc_theo_tai_lieu(bang, d) for k, d in docs_nua.items()}
    engines = bang.engines()
    co = set(bang.metrics())
    lines = [
        "# Tóm tắt Thực thi — OCR Parser Benchmark",
        "",
        f"**{len(engines)} profile** · **{len(co)} metric** · mốc dựng tất định.",
        "",
        "Không có điểm tổng và **không có trung bình cộng giữa các metric**: các metric "
        "khác nhau về trần đo được và thuộc hai nửa corpus rời nhau (xem "
        "`tables/ceiling.md`), nên trung bình của chúng không truy được về tập tài liệu "
        "nào. Mỗi dòng dưới đây là một metric, kèm cỡ mẫu `n` của chính con số đó.",
        "",
        *glossary.khoi_doc_bang(),
        "**Cách đọc một dòng:** *trần* là số tài liệu nhiều nhất metric chấm được với bộ "
        "nhãn hiện có; *độ trải* là khoảng cách điểm giữa engine cao nhất và thấp nhất — "
        f"dưới {report.NGUONG_PHAN_BIET:.2f} thì metric không tách được các engine ra và "
        "dòng mang dấu `‡`; *giá trị* luôn kèm `n` là cỡ mẫu của chính ô đó.",
        "",
    ]
    co_khong_phan_biet = False

    for cap_name, cap_metrics in CAPABILITIES.items():
        trong_bang = [m for m in cap_metrics if m in co]
        do_duoc = [m for m in trong_bang if m in trans and trans[m].bac == "do_duoc"]
        lines += [
            f"## {cap_name} — đo được {len(do_duoc)}/{len(cap_metrics)} metric",
            "",
            "| metric | nửa corpus | trần | độ trải | engine dẫn đầu | giá trị |",
            "|---|---|---:|---:|---|---|",
        ]
        for m in trong_bang:
            t = trans.get(m)
            nua_m = t.nua_corpus if t else "?"
            tran_m = str(t.n_toi_da) if t else "?"
            # Chấm trên đúng nửa của metric. `bang` chỉ dùng khi metric không có
            # trần (`t is None`) hoặc nằm ở cả hai nửa — khi đó cỡ mẫu toàn corpus
            # mới là cỡ mẫu thật của nó.
            con = con_nua.get(nua_m, bang) if t else bang
            trai = report.do_trai(con, m)
            # `None` = chưa tới hai engine chấm được. In "—" chứ không in 0.000: một
            # số 0 ở cột này đọc thành "các engine giống hệt nhau", trong khi thật ra
            # không có gì để so.
            o_trai = "—" if trai is None else f"{trai:.3f}"
            if m in report.NGUOC_CHIEU:
                # Ngược chiều: "dẫn đầu theo điểm" ở đây là câu vô nghĩa. In lý do.
                lines.append(
                    f"| {m} † | {nua_m} | {tran_m} | {o_trai} | — | "
                    "ngược chiều, không xếp hạng theo điểm |"
                )
                continue
            xep = [a for a in con.ranking(m) if a.n_scored > 0]
            if not xep:
                # Không ai chấm được: in nguyên `cell()` của engine đầu bảng để giữ
                # đúng lý do (N/A · chưa có nhãn · toàn hỏng), không rút thành "—".
                ly_do = con.cell(m, engines[0]).cell() if engines else "N/A"
                lines.append(f"| {m} | {nua_m} | {tran_m} | {o_trai} | — | {ly_do} |")
                continue
            dau = xep[0]
            # `‡` là bậc thứ tư, tách khỏi ba bậc của `ceiling.py`: ở đó là tính chất
            # của bộ nhãn, ở đây là tính chất của lượt chạy. Engine "dẫn đầu" vẫn in
            # tên, nhưng dấu ‡ nói thẳng rằng dẫn đầu ở đây không đáng để chọn theo.
            khong_pb = trai is not None and trai < report.NGUONG_PHAN_BIET
            co_khong_phan_biet = co_khong_phan_biet or khong_pb
            lines.append(
                f"| {m}{' ‡' if khong_pb else ''} | {nua_m} | {tran_m} | {o_trai} | "
                f"`{dau.engine}` | {dau.cell()} |"
            )
        lines += [""]
        chu = report.chu_thich_nguoc_chieu(trong_bang)
        if chu:
            lines += chu

    if co_khong_phan_biet:
        lines += [report.CHU_THICH_KHONG_PHAN_BIET, ""]

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

    loi += _kiem_ten_engine_trong_hinh(out_dir, engines_co)
    return loi


def _kiem_ten_engine_trong_hinh(out_dir: Path, engines_co: set[str]) -> list[str]:
    """Mọi tên engine hiện trong `figures/*.svg` phải có trong aggregate thật.

    Đây là cổng chặn đúng cái lỗi đã xảy ra một lần: `render_forest_plot` rơi vào một
    danh sách engine mặc định viết sẵn trong source và vẽ ra `marker_*` / `sovereign_*`
    — bốn profile chưa từng chạy — mà không artifact nào khác lệch một dòng. Bảng thì
    đã có trace ID soi, hình thì trước nay không ai soi.

    Chỉ đối chiếu **tên đã biết**: quét chuỗi tự do trong SVG sẽ bắt nhầm chữ tiếng Việt
    trong tiêu đề. Danh sách nghi phạm là các profile trong `configs/profiles.json` cộng
    với chính các engine có trong aggregate.
    """
    fig_dir = Path(out_dir) / "figures"
    if not fig_dir.is_dir():
        return []

    cau_hinh = ROOT / "configs" / "profiles.json"
    ten_biet: set[str] = set(engines_co)
    if cau_hinh.exists():
        try:
            doc = json.loads(cau_hinh.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            doc = {}
        if isinstance(doc, dict):
            ten_biet |= {k for k in doc if isinstance(k, str)}
            ps = doc.get("profiles")
            if isinstance(ps, dict):
                ten_biet |= {k for k in ps if isinstance(k, str)}
            elif isinstance(ps, list):
                ten_biet |= {
                    p.get("name", "") for p in ps if isinstance(p, dict)
                } - {""}

    loi: list[str] = []
    for svg in sorted(fig_dir.glob("*.svg")):
        noi_dung = svg.read_text(encoding="utf-8")
        la = sorted(
            t
            for t in ten_biet - engines_co
            # Bỏ tên là khúc con của một engine có thật (`docling` ⊂ `docling_default`):
            # nó xuất hiện trong SVG vì engine thật xuất hiện, không phải vì ai bịa.
            if t and t in noi_dung and not any(t in e for e in engines_co)
        )
        if la:
            loi.append(
                f"figures/{svg.name} vẽ engine không có trong aggregate-results.json: "
                f"{', '.join(la)}"
            )
    return loi
