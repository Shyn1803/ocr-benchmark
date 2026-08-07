"""Báo cáo D1 — bảng công bố + bản lưu `history/` (TASK-087).

Một bảng xếp hạng chỉ trung thực khi nó nói được **ba** thứ cùng lúc: điểm, tỉ lệ
hỏng, và **cỡ mẫu**. Hai thứ đầu đã có từ `Aggregate.cell()`. Thứ ba là lý do file
này tồn tại.

## Vì sao cỡ mẫu quan trọng tới mức phải có module riêng

Đo trên `prediction/` hiện tại:

    marker 20 · noop 41 · opendataloader 205 · pdf_inspector 205
    sabotage 41 · sovereign_full 2 · sovereign_light 204

và giao của **cả bảy** engine là **một** tài liệu (`sample_minimal`, file tổng hợp).
`opendataloader` chưa chạy tài liệu olmOCR nào; 20 tài liệu `arxiv_math` chỉ `noop`
và `sabotage` có.

Nghĩa là một bảng "metric × engine" gộp toàn bộ **không phải một phép so sánh** — nó
đặt cạnh nhau hai con số đo trên hai bộ tài liệu khác nhau. Cái sai đó không tự lộ
ra, vì cả hai ô đều là số thực trông hợp lệ. Cách duy nhất để người đọc thấy được là
in cỡ mẫu ngay cạnh điểm, và tách riêng một bảng chỉ chấm trên tập tài liệu **mọi
engine trong bảng đều có**.

## Quy tắc không được nới

* Mọi ô số đi qua :meth:`Aggregate.cell` — không chỗ nào tự ``f"{x:.3f}"``. Có test
  đọc lại markdown đã sinh để khoá điều này.
* Dòng ``N/A`` **không** bị bỏ khỏi bảng. Bỏ dòng là cách nhanh nhất làm engine yếu
  trông mạnh.
* Tập chung dưới :data:`TOI_THIEU_TAP_CHUNG` tài liệu thì in cảnh báo, **không** in
  bảng. Một trung bình trên 1 tài liệu vẫn là một con số; nó chỉ không có nghĩa.
"""

from __future__ import annotations

import json
import subprocess
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from ocr_bench.corpus import ROOT
from ocr_bench.scorer import ScoreTable
from ocr_bench.types import MetricResult, OcrResult

__all__ = [
    "TOI_THIEU_TAP_CHUNG",
    "THU_VIEN_CHAM_DIEM",
    "BaoCaoError",
    "nhom_tai_lieu",
    "coverage",
    "phien_ban_engine",
    "phien_ban_thu_vien",
    "thong_tin_git",
    "dung_manifest",
    "loc_theo_tai_lieu",
    "bang_markdown",
    "bao_cao_overall",
    "bao_cao_by_group",
    "bao_cao_common_set",
    "raw_json",
    "NHOM_ENGINE",
]

TOI_THIEU_TAP_CHUNG = 10
"""Dưới ngưỡng này thì `common_set.md` in cảnh báo thay cho bảng."""

THU_VIEN_CHAM_DIEM = ("jiwer", "rapidfuzz", "apted", "Pillow", "psutil", "pypdf")
"""Đổi bất kỳ gói nào ở đây là đổi con số **mà không đổi `prediction/`** — không ghi
lại thì lần sau không ai truy được vì sao bảng khác đi."""

NHOM_ENGINE: tuple[tuple[str, ...], ...] = (
    ("opendataloader", "pdf_inspector", "sovereign_light"),
    ("opendataloader", "pdf_inspector", "sovereign_light", "marker"),
    ("noop", "sabotage"),
)
"""Các nhóm engine đáng so chéo, định trước chứ không sinh tự động.

Sinh tự động mọi tổ hợp thì bảng nào cũng có, và người đọc sẽ chọn cái đẹp nhất.
Nhóm ở đây được chọn vì tập chung của chúng đủ lớn để nói được điều gì đó."""


class BaoCaoError(RuntimeError):
    """Dữ liệu không đủ điều kiện để công bố."""


# --------------------------------------------------------------------------- nhóm


def nhom_tai_lieu(root: Path | None = None) -> dict[str, str]:
    """`{doc_id: tên nhóm}` cho cả hai bộ mẫu.

    DocLayNet lấy nhóm từ ``doc_category`` trong COCO (6 nhóm, 34 tài liệu mỗi nhóm).
    olmOCR lấy từ thư mục con trong ``pdfs/olmocr/`` — tên file jsonl **không** trùng
    tên thư mục (``table_tests.jsonl`` ↔ ``pdfs/olmocr/tables/``), nên đi theo PDF là
    đường duy nhất không phải đoán.

    Tài liệu không thuộc bộ nào (vd `sample_minimal` do `make_sample_pdf.py` sinh)
    **không** có mặt trong dict. Người gọi phải tự quyết định — trả về một nhóm
    "khác" ở đây sẽ khiến nó lặng lẽ vào bảng công bố.
    """
    base = root or ROOT
    ra: dict[str, str] = {}

    coco_path = base / "ground-truth" / "doclaynet" / "layout_coco.json"
    if coco_path.exists():
        coco = json.loads(coco_path.read_text(encoding="utf-8"))
        for im in coco["images"]:
            ra[Path(im["file_name"]).stem] = f"doclaynet/{im['doc_category']}"

    pdf_dir = base / "pdfs" / "olmocr"
    if pdf_dir.is_dir():
        for sub in sorted(p for p in pdf_dir.iterdir() if p.is_dir()):
            for pdf in sub.glob("*.pdf"):
                ra[pdf.stem] = f"olmocr/{sub.name}"

    return ra


def coverage(rows: Iterable[MetricResult] | Iterable[OcrResult]) -> dict[str, set[str]]:
    """`{engine: {doc_id}}`. Nhận cả `MetricResult` lẫn `OcrResult`."""
    ra: dict[str, set[str]] = {}
    for r in rows:
        ra.setdefault(r.engine, set()).add(r.doc_id)
    return ra


def loc_theo_tai_lieu(bang: ScoreTable, docs: Iterable[str]) -> ScoreTable:
    """Bảng con chỉ gồm các tài liệu chỉ định. Không đụng `prediction/`."""
    giu = set(docs)
    return ScoreTable(tuple(r for r in bang.rows if r.doc_id in giu))


# ------------------------------------------------------------------------ manifest


def phien_ban_engine(results: Sequence[OcrResult]) -> dict[str, str]:
    """`{engine: engine_version}`, **ném** nếu một engine có nhiều hơn một version.

    Trộn hai lượt chạy khác version rồi lấy trung bình thì con số không thuộc về
    version nào. Đây là lỗi im lặng nhất trong cả pipeline: bảng vẫn in ra bình
    thường, chỉ là nó không mô tả bất cứ thứ gì có thật.
    """
    gom: dict[str, set[str]] = {}
    for r in results:
        gom.setdefault(r.engine, set()).add(r.engine_version)

    lan: dict[str, list[str]] = {e: sorted(v) for e, v in gom.items() if len(v) > 1}
    if lan:
        chi_tiet = "; ".join(f"{e}: {', '.join(v)}" for e, v in sorted(lan.items()))
        raise BaoCaoError(
            f"{len(lan)} engine có nhiều hơn một `engine_version` — dữ liệu trộn từ "
            f"nhiều lượt chạy, không công bố được: {chi_tiet}"
        )
    return {e: v.pop() for e, v in sorted(gom.items())}


def phien_ban_thu_vien(ten: Sequence[str] = THU_VIEN_CHAM_DIEM) -> dict[str, str]:
    """`{gói: version}`; gói chưa cài ghi `"chưa cài"`, không bỏ khỏi dict.

    Bỏ khỏi dict thì `manifest.json` của máy thiếu `psutil` trông giống hệt máy đủ —
    mà thiếu `psutil` là cột RSS bị đo hụt theo một hướng biết trước (xem
    `pyproject.toml`, extra `perf`).
    """
    ra: dict[str, str] = {}
    for g in ten:
        try:
            ra[g] = version(g)
        except PackageNotFoundError:
            ra[g] = "chưa cài"
    return ra


def thong_tin_git(root: Path | None = None) -> dict[str, object]:
    """`{commit, dirty}` của repo `ocr-bench`.

    `dirty=True` nghĩa là bản `history/` này sinh từ working tree có thay đổi chưa
    commit ⇒ **không truy ngược được**. Ghi ra chứ không chặn: chạy thử trên cây bẩn
    là chuyện bình thường, công bố một bản như vậy mà không biết mới là vấn đề.

    Riêng `history/` không tính — xem chú thích trong thân hàm.
    """
    base = root or ROOT

    def _git(*args: str) -> str | None:
        try:
            p = subprocess.run(
                ["git", *args], cwd=base, capture_output=True, text=True, timeout=15
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return p.stdout.strip() if p.returncode == 0 else None

    commit = _git("rev-parse", "HEAD")
    # Loại `history/` khỏi phép đo: nó là ĐẦU RA của chính lượt chạy này, không phải
    # đầu vào của con số. Không loại thì `dirty` luôn True — thư mục vừa ghi ra đã
    # làm bẩn cây mà nó đang báo cáo, và cờ mất sạch ý nghĩa.
    trang_thai = _git("status", "--porcelain", "--", ".", ":(exclude)history")
    return {
        "commit": commit or "không rõ",
        "dirty": bool(trang_thai) if trang_thai is not None else None,
    }


def dung_manifest(
    results: Sequence[OcrResult],
    bang: ScoreTable,
    *,
    generated_at: str,
    root: Path | None = None,
) -> dict[str, object]:
    """`manifest.json` — AC-01.

    Chứa đủ thứ để trả lời "con số này đo bằng gì, trên bao nhiêu tài liệu": version
    từng engine, version thư viện chấm điểm, commit + cây sạch/bẩn, và coverage.
    """
    cov = coverage(results)
    nhom = nhom_tai_lieu(root)
    ver = phien_ban_engine(results)

    engines: list[dict[str, object]] = []
    for e in sorted(cov):
        theo_nhom: dict[str, int] = {}
        ngoai_bo_mau = 0
        for d in cov[e]:
            g = nhom.get(d)
            if g is None:
                ngoai_bo_mau += 1
            else:
                theo_nhom[g] = theo_nhom.get(g, 0) + 1
        engines.append(
            {
                "engine": e,
                "version": ver[e],
                "n_docs": len(cov[e]),
                "n_ngoai_bo_mau": ngoai_bo_mau,
                "theo_nhom": dict(sorted(theo_nhom.items())),
            }
        )

    return {
        "generated_at": generated_at,
        "git": thong_tin_git(root),
        "libraries": phien_ban_thu_vien(),
        "engines": engines,
        "metrics": bang.metrics(),
        "n_docs_tong": len(set().union(*cov.values())) if cov else 0,
        "canh_bao": _canh_bao(cov),
    }


def _canh_bao(cov: dict[str, set[str]]) -> list[str]:
    """Những điều người đọc bảng phải biết trước khi đọc số."""
    ra: list[str] = []
    if not cov:
        return ra

    n = {e: len(d) for e, d in cov.items()}
    lon_nhat = max(n.values())
    for e in sorted(n):
        if n[e] < lon_nhat / 2:
            ra.append(
                f"`{e}` chỉ có {n[e]}/{lon_nhat} tài liệu — không so ngang hàng được "
                f"với engine chạy đủ bộ."
            )

    chung = set.intersection(*cov.values())
    ra.append(
        f"Giao của cả {len(cov)} engine là {len(chung)} tài liệu. Bảng gộp toàn bộ "
        f"KHÔNG phải một phép so sánh — xem `common_set.md`."
    )
    return ra


# --------------------------------------------------------------------------- bảng


def bang_markdown(
    bang: ScoreTable,
    *,
    engines: Sequence[str] | None = None,
    cov: dict[str, set[str]] | None = None,
) -> str:
    """Bảng metric × engine, **kèm dòng `n`** (cỡ mẫu từng engine).

    Mọi ô số đi qua `Aggregate.cell()`; không format số ở đây. Dòng `n` đứng ngay
    dưới tiêu đề để không ai đọc điểm mà bỏ qua cỡ mẫu.
    """
    es = list(engines) if engines is not None else bang.engines()
    if not es:
        return "_không có engine nào._"

    dem = cov if cov is not None else coverage(bang.rows)
    head = "| metric | " + " | ".join(es) + " |"
    sep = "|" + "---|" * (len(es) + 1)
    dong_n = "| **n (tài liệu)** | " + " | ".join(
        str(len(dem.get(e, ()))) for e in es
    ) + " |"
    body = [
        "| " + " | ".join([m] + [bang.cell(m, e).cell() for e in es]) + " |"
        for m in bang.metrics()
    ]
    return "\n".join([head, sep, dong_n, *body])


def bao_cao_overall(bang: ScoreTable, manifest: dict[str, object]) -> str:
    """`overall.md` — số tổng quan, cảnh báo đặt **trước** bảng."""
    canh_bao = manifest.get("canh_bao") or []
    d = [
        "# Bảng tổng quan — mọi engine, mọi tài liệu",
        "",
        "> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.",
        "",
        "## Đọc bảng này thế nào",
        "",
        "Mỗi engine chạy trên một tập tài liệu **khác nhau** (xem dòng `n`). Đặt hai ô "
        "cạnh nhau rồi kết luận cái nào hơn là **sai** trừ khi hai engine có cùng `n` "
        "trên cùng tập. Bảng so chéo hợp lệ nằm ở `common_set.md`.",
        "",
    ]
    if canh_bao:
        d += ["### Cảnh báo", ""] + [f"- {c}" for c in canh_bao] + [""]
    d += [
        "## Bảng",
        "",
        bang_markdown(bang),
        "",
        "Ô `N/A` = engine không có năng lực để metric chạm tới. Nó **không** phải 0 và "
        "dòng của nó **không** bị bỏ đi.",
        "",
    ]
    return "\n".join(d)


def bao_cao_by_group(bang: ScoreTable, root: Path | None = None) -> str:
    """`by_group.md` — AC-02, một bảng cho mỗi nhóm tài liệu."""
    nhom = nhom_tai_lieu(root)
    theo_nhom: dict[str, set[str]] = {}
    for doc, g in nhom.items():
        theo_nhom.setdefault(g, set()).add(doc)

    co_mat = {d for d in bang.docs()}
    ngoai = sorted(co_mat - set(nhom))

    d = [
        "# Bảng theo nhóm tài liệu",
        "",
        "> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.",
        "",
        "Tách theo nhóm làm số **rõ hơn**, không đẹp hơn: chia nhỏ thì cỡ mẫu của "
        "engine chạy ít tài liệu xuống còn vài đơn vị. Dòng `n` của từng bảng nói ra "
        "điều đó — đọc nó trước khi đọc điểm.",
        "",
    ]
    if ngoai:
        d += [
            f"Ngoài bộ mẫu, **không** vào bảng nào dưới đây: {', '.join(f'`{x}`' for x in ngoai)}.",
            "",
        ]

    for g in sorted(theo_nhom):
        con = loc_theo_tai_lieu(bang, theo_nhom[g])
        if not con.rows:
            continue
        d += [f"## {g}", "", bang_markdown(con), ""]
    return "\n".join(d)


def bao_cao_common_set(
    bang: ScoreTable,
    cov: dict[str, set[str]] | None = None,
    nhom_engine: Sequence[Sequence[str]] = NHOM_ENGINE,
) -> str:
    """`common_set.md` — bảng duy nhất so chéo được.

    Chỉ chấm trên tài liệu **mọi engine trong nhóm đều có**. Nhóm nào có tập chung
    dưới `TOI_THIEU_TAP_CHUNG` thì in cảnh báo thay cho bảng — in bảng trên 1 tài
    liệu là mời người đọc kết luận từ một mẫu.
    """
    dem = cov if cov is not None else coverage(bang.rows)
    d = [
        "# So chéo trên tập tài liệu chung",
        "",
        "> Sinh bằng `py -3 scripts/d1_report.py`. **Không** sửa tay.",
        "",
        "Mỗi bảng dưới đây chỉ chấm trên tài liệu **mọi engine trong bảng đều có**. "
        "Đây là bảng duy nhất mà việc so hai ô cạnh nhau là hợp lệ.",
        "",
    ]

    for nhom in nhom_engine:
        ten = " × ".join(f"`{e}`" for e in nhom)
        thieu = [e for e in nhom if e not in dem]
        if thieu:
            d += [
                f"## {ten}",
                "",
                f"Bỏ qua — không có dự đoán của: {', '.join(f'`{e}`' for e in thieu)}.",
                "",
            ]
            continue

        chung = set.intersection(*(dem[e] for e in nhom))
        if len(chung) < TOI_THIEU_TAP_CHUNG:
            d += [
                f"## {ten}",
                "",
                f"**Tập chung chỉ {len(chung)} tài liệu — quá nhỏ để so.** Không in "
                f"bảng: một trung bình trên {len(chung)} tài liệu vẫn là một con số, "
                f"nó chỉ không có nghĩa.",
                "",
            ]
            continue

        con = loc_theo_tai_lieu(bang, chung)
        d += [
            f"## {ten}",
            "",
            f"Tập chung: **{len(chung)}** tài liệu.",
            "",
            bang_markdown(con, engines=list(nhom)),
            "",
        ]
    return "\n".join(d)


def raw_json(bang: ScoreTable, *, generated_at: str) -> str:
    """Điểm thô, tất định — AC-04 so lại từng dòng chứ không so markdown.

    **Không làm tròn.** Làm tròn khi ghi là giấu đúng cái sai lệch mà AC-04 định bắt;
    làm tròn chỉ được xảy ra lúc in markdown.
    """
    rows = sorted(bang.rows, key=lambda r: (r.metric, r.engine, r.doc_id))
    return json.dumps(
        {
            "generated_at": generated_at,
            "rows": [
                {
                    "metric": r.metric,
                    "engine": r.engine,
                    "doc_id": r.doc_id,
                    "value": r.value,
                    "na_reason": r.na_reason.value if r.na_reason else None,
                }
                for r in rows
            ],
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
