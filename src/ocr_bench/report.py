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

from ocr_bench import glossary
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
    "NGUOC_CHIEU",
    "chu_thich_nguoc_chieu",
    "NuaCorpus",
    "bao_cao_overall",
    "bao_cao_by_group",
    "bao_cao_common_set",
    "raw_json",
    "NHOM_ENGINE",
]

TOI_THIEU_TAP_CHUNG = 10
"""Dưới ngưỡng này thì `common-set.md` in cảnh báo thay cho bảng."""

THU_VIEN_CHAM_DIEM = ("jiwer", "rapidfuzz", "apted", "Pillow", "psutil", "pypdf")
"""Đổi bất kỳ gói nào ở đây là đổi con số **mà không đổi `prediction/`** — không ghi
lại thì lần sau không ai truy được vì sao bảng khác đi."""

NHOM_ENGINE: tuple[tuple[str, ...], ...] = (
    ("docling_default", "opendataloader_default"),
    ("docling_scan", "opendataloader_scan"),
    ("docling_default", "docling_scan"),
    ("opendataloader_default", "opendataloader_scan"),
    # Lượt chạy 2026-08: `docling_scan` chưa xong, ba engine kia đủ 1606/1606. Không
    # có bộ này thì nhóm 4-engine rơi vào nhánh "Bỏ qua" và cả lượt chạy không so
    # chéo được gì, dù ba phần tư dữ liệu đã có.
    ("docling_default", "opendataloader_default", "opendataloader_scan"),
    ("docling_default", "docling_scan", "opendataloader_default", "opendataloader_scan"),
    ("noop", "sabotage"),
)
"""Các nhóm engine đáng so chéo, định trước chứ không sinh tự động.

Sinh tự động mọi tổ hợp thì bảng nào cũng có, và người đọc sẽ chọn cái đẹp nhất.
Nhóm ở đây được chọn vì tập chung của chúng đủ lớn để nói được điều gì đó.

Tên phải là **tên profile** trong `configs/profiles.json` (`<họ>_<profile>`), không
phải tên engine trần. Tới 2026-08-17 danh sách này vẫn giữ tên của lần chạy cũ
(`opendataloader`, `pdf_inspector`, `sovereign_light`, `marker`) trong khi catalog
đã đổi sang dạng có profile — không gì ném lỗi, mọi nhóm rơi vào nhánh "Bỏ qua", và
`common-set.md` ra lò rỗng ruột suốt. `test_nhom_engine_mac_dinh_chi_gom_ten_profile_co_that`
chặn lần sau; `noop`/`sabotage` là engine hiệu chuẩn nên không nằm trong catalog."""


SINH_BOI_MAC_DINH = "scripts/build_research_report.py"
"""Script ghi trong dòng xuất xứ của mỗi bảng.

Là tham số chứ không phải hằng nhúng sẵn vì **hai** script sinh ra các bảng này
(`build_research_report.py` cho bản công bố, `d1_report.py` cho ảnh chụp `history/`).
Chốt cứng một tên thì bảng của script kia chỉ người ta tới lệnh không dựng lại được
nó — đúng loại sai mà dòng xuất xứ sinh ra để chặn."""


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
        f"KHÔNG phải một phép so sánh — xem `common-set.md`."
    )
    return ra


# --------------------------------------------------------------------------- bảng


NGUOC_CHIEU: dict[str, str] = {
    "cell_f1": (
        "`cell_f1` **không** đo chất lượng ô ở bộ mẫu này. Không nhãn nào có ô, nên "
        "tài liệu duy nhất chấm được là tài liệu engine **tự sinh ra bảng** — theo "
        "định nghĩa metric thì điểm luôn 0.000 và thông tin nằm ở `n`: `n` là số tài "
        "liệu bị bảng ảo. **Thấp hơn là tốt hơn**, ngược chiều mọi metric còn lại, nên "
        "nó bị loại khỏi mọi bảng xếp hạng theo điểm. Thêm engine thứ tư cũng không đổi "
        "được điều này: thiếu ô trong nhãn là thiếu ở **bộ mẫu**, engine nào chạy vào "
        "cũng rơi đúng nhánh đó. Muốn `cell_f1` có nghĩa thì phải gán nhãn ô, không "
        "phải chạy thêm lượt."
    ),
}
"""Metric mà con số in ra đọc ngược quy ước "cao hơn là tốt hơn".

Không sửa `Metric` để đảo dấu: điểm 0.000 ở đây là **đúng** theo định nghĩa metric,
cái sai nằm ở chỗ bộ mẫu không có nhãn ô nên phép đo mất nghĩa. Đảo dấu sẽ biến một
metric vô nghĩa thành một metric trông có nghĩa — tệ hơn hẳn. Thay vào đó đánh dấu
`†` ở tên hàng và in nguyên văn lý do dưới bảng, để người đọc không thể đọc con số
mà không đọc lý do."""


def _nhan_metric(m: str) -> str:
    return f"{m} †" if m in NGUOC_CHIEU else m


def chu_thich_nguoc_chieu(metrics: Iterable[str]) -> list[str]:
    """Các dòng `†` cho những metric **thực sự có mặt** trong bảng vừa in.

    In vô điều kiện thì file nào cũng mang chú thích cho một hàng không tồn tại, và
    chú thích thừa dạy người đọc bỏ qua chú thích.
    """
    co = [m for m in dict.fromkeys(metrics) if m in NGUOC_CHIEU]
    if not co:
        return []
    return ["> † " + NGUOC_CHIEU[m] for m in co] + [""]


NGUONG_PHAN_BIET = 0.05
"""Dưới mức này thì coi như các engine **không tách được nhau** ở metric đó.

Cùng ngưỡng vật chất đã dùng khi lọc các phép so sánh có ý nghĩa thống kê: một chênh
lệch nhỏ hơn 0.05 thì dù p có nhỏ tới đâu cũng không đổi được lựa chọn engine nào.
Giữ một hằng số cho cả hai chỗ để không có hai định nghĩa "đáng kể" cùng tồn tại."""

_TRAI_KHONG_TINH_DUOC = None
"""Ký hiệu rõ ràng cho "chưa tới hai engine chấm được" — khác hẳn độ trải bằng 0."""


def do_trai(bang: ScoreTable, metric: str) -> float | None:
    """Độ trải điểm giữa các engine ở một metric: `max − min` của trung bình có phạt.

    Trả `None` khi **chưa tới hai** engine chấm được metric đó — độ trải của một điểm
    duy nhất là 0, và một số 0 ở đây đọc thành "các engine giống hệt nhau" trong khi
    sự thật là không có gì để so.

    Đây là tính chất **phụ thuộc lượt chạy**, nên nó nằm ở đây chứ không ở `ceiling.py`:
    trần đo được là tính chất của bộ nhãn, còn "các engine có tách được nhau không" đổi
    theo chính danh sách engine đem ra so.
    """
    diem = [
        a.penalized_mean
        for a in bang.ranking(metric)
        if a.n_scored > 0 and a.penalized_mean is not None
    ]
    if len(diem) < 2:
        return _TRAI_KHONG_TINH_DUOC
    return max(diem) - min(diem)


def khong_phan_biet(bang: ScoreTable, metric: str) -> bool:
    """Metric chấm được ở ≥2 engine nhưng mọi engine chênh nhau dưới ngưỡng."""
    trai = do_trai(bang, metric)
    return trai is not None and trai < NGUONG_PHAN_BIET


CHU_THICH_KHONG_PHAN_BIET = (
    "> ‡ Metric **đo được nhưng không phân biệt**: mọi engine chênh nhau dưới "
    f"{NGUONG_PHAN_BIET:.2f} điểm, nên con số đúng mà không dùng để chọn engine được. "
    "Đây không phải `N/A` — phép đo chạy đủ trên cỡ mẫu thật; nó chỉ nói rằng ở khía "
    "cạnh này các engine hành xử như nhau, và kết luận nào rút ra từ thứ tự của chúng "
    "cũng là kết luận rút ra từ nhiễu."
)
"""Một dòng, đặt dưới bảng có ít nhất một hàng `‡`."""


def bang_markdown(
    bang: ScoreTable,
    *,
    engines: Sequence[str] | None = None,
    cov: dict[str, set[str]] | None = None,
    metrics: Sequence[str] | None = None,
) -> str:
    """Bảng metric × engine, **kèm dòng `n`** (cỡ mẫu từng engine).

    Mọi ô số đi qua `Aggregate.cell()`; không format số ở đây. Dòng `n` đứng ngay
    dưới tiêu đề để không ai đọc điểm mà bỏ qua cỡ mẫu.

    `metrics` chọn **hàng nào và theo thứ tự nào**. Mặc định là mọi metric có trong
    bảng, xếp theo `ScoreTable.metrics()`. Người gọi truyền vào để (a) không trộn
    metric của hai nửa corpus rời nhau vào cùng một bảng, (b) xếp theo trần đo được
    thay vì theo bảng chữ cái. Tên không có trong bảng bị bỏ qua — bảng con lọc theo
    tài liệu có thể thiếu hẳn một metric.
    """
    es = list(engines) if engines is not None else bang.engines()
    if not es:
        return "_không có engine nào._"

    co = set(bang.metrics())
    ms = [m for m in metrics if m in co] if metrics is not None else bang.metrics()

    dem = cov if cov is not None else coverage(bang.rows)
    head = "| metric | " + " | ".join(es) + " |"
    sep = "|" + "---|" * (len(es) + 1)
    dong_n = "| **n (tài liệu)** | " + " | ".join(
        str(len(dem.get(e, ()))) for e in es
    ) + " |"
    body = [
        "| " + " | ".join([_nhan_metric(m)] + [bang.cell(m, e).cell() for e in es]) + " |"
        for m in ms
    ]
    return "\n".join([head, sep, dong_n, *body])


@dataclass(frozen=True, slots=True)
class NuaCorpus:
    """Một nửa bộ mẫu: tập tài liệu của nó, và các metric chấm được trên nó.

    Bộ mẫu gồm hai nửa **rời nhau** — DocLayNet mang nhãn bbox, olmOCR mang nhãn
    khẳng định, giao bằng 0. Một bảng trộn cả hai in `block_f1` (trần 203) ngay cạnh
    `assert_math_presence` (trần 558) mà không gì trong bảng nói ra rằng hai con số
    đến từ hai bộ tài liệu không giao nhau; người đọc mặc định chúng so được với nhau.
    Tách ở đây để việc trộn trở thành không biểu diễn được, không phải một quy ước
    phải nhớ.
    """

    ten: str
    """Tiêu đề section, ví dụ `"DocLayNet — nhãn bố cục"`."""
    docs: frozenset[str]
    """`doc_id` thuộc nửa này. Bảng được lọc về đúng tập này trước khi in."""
    metrics: tuple[str, ...]
    """Metric của nửa này, **đã xếp thứ tự** (xem `ceiling.thu_tu_metric`)."""
    ghi_chu: str = ""
    """Câu đặt ngay dưới tiêu đề — chỗ nói trần đo được, hoặc vì sao nửa này ít metric."""
    slug: str = ""
    """Khoá ngắn, ổn định, dùng đặt tên file hình của nửa này (`doclaynet` / `olmocr`).

    Không suy từ `ten`: tiêu đề là câu tiếng Việt có dấu, băm nó ra tên file cho chuỗi
    như `doclaynet_nh_n_b_c_c_bbox`, và mỗi lần sửa chữ trong tiêu đề là một lần đổi
    tên file mà không ai định đổi.
    """


def _cac_nua(bang: ScoreTable, nua: Sequence[NuaCorpus] | None) -> list[NuaCorpus]:
    """Không truyền nửa nào ⇒ một nửa duy nhất phủ cả bảng (hành vi cũ)."""
    if nua is not None:
        return list(nua)
    return [NuaCorpus(ten="", docs=frozenset(bang.docs()), metrics=tuple(bang.metrics()))]


def bao_cao_overall(
    bang: ScoreTable,
    manifest: dict[str, object],
    *,
    nua: Sequence[NuaCorpus] | None = None,
    sinh_boi: str = SINH_BOI_MAC_DINH,
) -> str:
    """`overall.md` — số tổng quan, cảnh báo đặt **trước** bảng."""
    canh_bao = manifest.get("canh_bao") or []
    d = [
        "# Bảng tổng quan — mọi engine, mọi tài liệu",
        "",
        f"> Sinh bằng `py -3 {sinh_boi}`. **Không** sửa tay.",
        "",
        # Ba bảng kết quả nằm cùng thư mục `tables/` với chú giải, nên đường dẫn là
        # tên file trần — người đọc mở file cạnh bên, không phải lần ngược thư mục.
        *glossary.khoi_doc_bang("glossary.md"),
        "## Đọc bảng này thế nào",
        "",
        "Mỗi engine chạy trên một tập tài liệu **khác nhau** (xem dòng `n`). Đặt hai ô "
        "cạnh nhau rồi kết luận cái nào hơn là **sai** trừ khi hai engine có cùng `n` "
        "trên cùng tập. Bảng so chéo hợp lệ nằm ở `common-set.md`.",
        "",
    ]
    if canh_bao:
        d += ["### Cảnh báo", ""] + [f"- {c}" for c in canh_bao] + [""]

    da_in: list[str] = []
    for n in _cac_nua(bang, nua):
        con = loc_theo_tai_lieu(bang, n.docs) if nua is not None else bang
        d += [f"## {n.ten or 'Bảng'}", ""]
        if n.ghi_chu:
            d += [n.ghi_chu, ""]
        d += [bang_markdown(con, metrics=n.metrics), ""]
        da_in += [m for m in n.metrics if m in set(con.metrics())]

    d += chu_thich_nguoc_chieu(da_in)
    d += [
        "Ô `N/A` = engine không có năng lực để metric chạm tới. Nó **không** phải 0 và "
        "dòng của nó **không** bị bỏ đi.",
        "",
    ]
    return "\n".join(d)


def bao_cao_by_group(
    bang: ScoreTable,
    root: Path | None = None,
    *,
    nua: Sequence[NuaCorpus] | None = None,
    sinh_boi: str = SINH_BOI_MAC_DINH,
) -> str:
    """`by-group.md` — AC-02, một bảng cho mỗi nhóm tài liệu.

    Mỗi nhóm nằm gọn trong **một** nửa corpus (`nhom_tai_lieu()` đã gắn tiền tố
    `doclaynet/` hoặc `olmocr/`), nên `nua` ở đây chỉ dùng để chọn danh sách metric
    cho từng nhóm — không cần chia lại tài liệu.
    """
    nhom = nhom_tai_lieu(root)
    theo_nhom: dict[str, set[str]] = {}
    for doc, g in nhom.items():
        theo_nhom.setdefault(g, set()).add(doc)

    co_mat = {d for d in bang.docs()}
    ngoai = sorted(co_mat - set(nhom))

    d = [
        "# Bảng theo nhóm tài liệu",
        "",
        f"> Sinh bằng `py -3 {sinh_boi}`. **Không** sửa tay.",
        "",
        *glossary.khoi_doc_bang("glossary.md"),
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

    cac_nua = _cac_nua(bang, nua)
    da_in: list[str] = []
    for g in sorted(theo_nhom):
        con = loc_theo_tai_lieu(bang, theo_nhom[g])
        if not con.rows:
            continue
        da_in += con.metrics()
        # Nhóm thuộc nửa nào thì lấy thứ tự metric của nửa đó. Không nửa nào nhận
        # (nhóm ngoài cả hai bộ mẫu) thì để `None` — in mọi metric có trong bảng con,
        # còn hơn in một bảng rỗng mà không nói vì sao.
        cua_nhom = next(
            (n.metrics for n in cac_nua if theo_nhom[g] & n.docs), None
        )
        d += [f"## {g}", "", bang_markdown(con, metrics=cua_nhom), ""]
    d += chu_thich_nguoc_chieu(da_in)
    return "\n".join(d)


def _vi_sao_nhom(nhom: Sequence[str]) -> str:
    """Nhóm này đặt ra để trả lời câu hỏi gì — suy từ chính tên profile.

    Sáu bảng của mục so chéo trước đây chỉ khác nhau ở dòng tiêu đề `A × B`, nên đọc
    tuần tự thì thấy sáu bảng số gần giống nhau mà không rõ vì sao phải có sáu. Tên
    profile là `<họ>_<chế độ>`, nên chỉ cần nhìn phần nào giữ nguyên là biết bảng đang
    giữ gì cố định và đổi gì.

    Suy từ tên chứ không chép tay: thêm một nhóm vào `NHOM_ENGINE` là có ngay câu giải
    thích đúng, không phải nhớ sửa thêm chỗ thứ hai.
    """
    if set(nhom) == {"noop", "sabotage"}:
        return (
            "Chốt kiểm soát, không phải engine thật: `noop` không trả gì và `sabotage` "
            "trả kết quả cố ý sai. Nếu hai cái này không rơi xuống đáy thì luật chấm "
            "hỏng, không phải engine giỏi."
        )
    ho = {e.rsplit("_", 1)[0] for e in nhom}
    che_do = {e.rsplit("_", 1)[-1] for e in nhom if "_" in e}
    if len(ho) == 1 and len(che_do) > 1:
        return (
            f"Cùng một họ engine (`{next(iter(ho))}`), khác chế độ — bảng này trả lời: "
            "bật chế độ scan lên thì được gì và mất gì."
        )
    if len(che_do) == 1 and len(ho) > 1:
        return (
            f"Cùng chế độ `{next(iter(che_do))}`, khác họ engine — bảng này trả lời: "
            "ở cùng một cách chạy thì engine nào chấm cao hơn."
        )
    return (
        "Nhiều họ engine và nhiều chế độ cùng lúc — bảng tổng, dùng để nhìn tất cả "
        "trên **cùng một** tập tài liệu; tách riêng từng câu hỏi thì xem các bảng trên."
    )


def bao_cao_common_set(
    bang: ScoreTable,
    cov: dict[str, set[str]] | None = None,
    nhom_engine: Sequence[Sequence[str]] = NHOM_ENGINE,
    *,
    nua: Sequence[NuaCorpus] | None = None,
    sinh_boi: str = SINH_BOI_MAC_DINH,
) -> str:
    """`common-set.md` — bảng duy nhất so chéo được.

    Chỉ chấm trên tài liệu **mọi engine trong nhóm đều có**. Nhóm nào có tập chung
    dưới `TOI_THIEU_TAP_CHUNG` thì in cảnh báo thay cho bảng — in bảng trên 1 tài
    liệu là mời người đọc kết luận từ một mẫu.
    """
    dem = cov if cov is not None else coverage(bang.rows)
    d = [
        "# So chéo trên tập tài liệu chung",
        "",
        f"> Sinh bằng `py -3 {sinh_boi}`. **Không** sửa tay.",
        "",
        *glossary.khoi_doc_bang("glossary.md"),
        "Mỗi bảng dưới đây chỉ chấm trên tài liệu **mọi engine trong bảng đều có**. "
        "Đây là bảng duy nhất mà việc so hai ô cạnh nhau là hợp lệ.",
        "",
    ]

    # Ghi chú của mỗi nửa corpus in **một lần ở đây**, không lặp trong từng bảng. Bản
    # trước in nó lại dưới mỗi tiêu đề nửa của mỗi nhóm — sáu nhóm × hai nửa là mười
    # hai lần cùng một đoạn văn, và người đọc học cách nhảy qua nó ngay từ lần thứ ba.
    if nua is not None:
        ghi_chu = [(n.ten, n.ghi_chu) for n in nua if n.ghi_chu]
        if ghi_chu:
            d += ["Mọi nhóm dưới đây đều cắt làm hai nửa corpus:", ""]
            d += [f"- **{ten}** — {gc}" for ten, gc in ghi_chu]
            d += [""]

    da_in_bang = 0
    da_in: list[str] = []
    for nhom in nhom_engine:
        ten = " × ".join(f"`{e}`" for e in nhom)
        d += [f"## {ten}", "", _vi_sao_nhom(nhom), ""]
        thieu = [e for e in nhom if e not in dem]
        if thieu:
            d += [
                f"Bỏ qua — không có dự đoán của: {', '.join(f'`{e}`' for e in thieu)}.",
                "",
            ]
            continue

        chung = set.intersection(*(dem[e] for e in nhom))
        if len(chung) < TOI_THIEU_TAP_CHUNG:
            d += [
                f"**Tập chung chỉ {len(chung)} tài liệu — quá nhỏ để so.** Không in "
                f"bảng: một trung bình trên {len(chung)} tài liệu vẫn là một con số, "
                f"nó chỉ không có nghĩa.",
                "",
            ]
            continue

        d += [f"Tập chung: **{len(chung)}** tài liệu.", ""]
        for n in _cac_nua(bang, nua):
            # Cắt tập chung theo nửa **sau** khi giao các engine: giao trước rồi cắt
            # cho ra đúng tập, còn cắt trước rồi giao thì mỗi nửa lại có một "tập
            # chung" riêng và con số ở tiêu đề không còn mô tả bảng nào.
            docs = chung & n.docs if nua is not None else chung
            if not docs:
                continue
            con = loc_theo_tai_lieu(bang, docs)
            if nua is not None:
                d += [f"### {n.ten} — {len(docs)} tài liệu", ""]
            d += [bang_markdown(con, engines=list(nhom), metrics=n.metrics), ""]
            da_in += con.metrics()
        da_in_bang += 1

    d += chu_thich_nguoc_chieu(da_in)
    if not da_in_bang:
        # Không nhóm nào in được bảng ⇒ file này không so chéo gì, trong khi
        # `overall.md` vẫn trỏ người đọc sang đây như "bảng duy nhất hợp lệ".
        # Chèn cảnh báo lên đầu, không phụ lục ở cuối: người đọc dừng ở bảng đầu
        # tiên họ thấy, và ở đây không có bảng nào để dừng.
        d[5:5] = [
            f"> ⚠️ **Báo cáo này KHÔNG so chéo được gì.** Cả {len(nhom_engine)} nhóm "
            "đều bị bỏ qua — xem lý do từng nhóm bên dưới. Thường là `NHOM_ENGINE` "
            "trong `report.py` còn tên của lần chạy trước, hoặc lần chạy này thiếu "
            "engine. Đừng trích số từ `overall.md` để thay: các engine ở đó không "
            "chạy trên cùng tập tài liệu.",
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
