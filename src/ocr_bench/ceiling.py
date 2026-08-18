"""Trần đo được của **bộ nhãn** — tính trước khi bất kỳ engine nào chạy.

Bảng xếp hạng trả lời "engine nào tốt hơn". File này trả lời câu đứng trước nó:
*với bộ nhãn đang có, metric này nhiều nhất chấm được bao nhiêu tài liệu?* Không có
câu trả lời đó thì `teds = N/A` đọc y hệt `teds = engine không làm được`, trong khi
sự thật là 0/75 bảng ground truth có HTML — **không engine nào** chạm tới được nó.

Cách tính: **phát lại chính các cổng của metric**, không hardcode bảng
metric→trường-GT. Với mỗi tài liệu, dựng một `OcrResult` "thần thánh" — engine khai
đủ mọi năng lực, không hỏng, và trả về **đúng bằng ground truth** — rồi chạy
`isinstance(gt, metric.gt_kinds)` và `metric._na_rieng(gt, gia)`. Qua được cả hai
nghĩa là tài liệu đó chấm được **nếu có một engine hoàn hảo**; đó chính là định nghĩa
của trần. `_compute()` không bao giờ được gọi.

Vì sao phải là engine hoàn hảo chứ không phải engine rỗng: ba metric (`layout`,
`imgf1`, `cell_f1`) có cổng **đối xứng** — "nhãn rỗng **và** engine cũng rỗng" mới là
N/A — còn `heading` và `table_recall` đọc thêm đầu ra để phân biệt "nhãn thiếu" với
"engine thiếu". Cho engine rỗng vào thì `heading` rụng từ 17 xuống 0 và con số in ra
sẽ là trần của một engine mù, không phải trần của bộ nhãn.

Lý do in trong bảng là chuỗi `ly_do` **do chính metric sinh ra**, không phải văn của
người viết báo cáo. Sửa luật N/A trong metric thì dòng giải thích ở đây đổi theo,
không lệch pha được.

File này cố ý **không** nhắc tên engine nào. "Engine nào có năng lực chạm tới metric"
là câu hỏi khác, trả lời bằng `registry.applicable_metrics()` lúc dựng báo cáo; trộn
vào đây thì trần của bộ nhãn lại phụ thuộc vào danh sách engine của lượt chạy.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from typing import Literal

from ocr_bench import glossary, registry
from ocr_bench.metrics.base import Metric
from ocr_bench.types import (
    AnnotationGT,
    AssertionGT,
    Capability,
    GroundTruth,
    OcrImage,
    OcrResult,
)

__all__ = [
    "Tran",
    "tran_do_duoc",
    "thu_tu_metric",
    "du_lieu_tran",
    "bang_tran",
    "NGUONG_DO_DUOC",
]

NGUONG_DO_DUOC = 100
"""Từ đây trở lên mới gọi là ``do_duoc``.

Một ngưỡng, không hai: mọi trần trong khoảng 1..99 đều vào ``mong``. Đặt thêm mốc 50
thì `img_f1` (trần 64) rơi vào khe không tên, và một bậc không tên là chỗ để lát nữa
ai đó tự gán cho nó cái tên có lợi.
"""

Bac = Literal["do_duoc", "mong", "tran_0"]

_THU_TU_BAC: dict[str, int] = {"do_duoc": 0, "mong": 1, "tran_0": 2}


@dataclass(frozen=True, slots=True)
class Tran:
    """Trần đo được của một metric trên bộ nhãn hiện có."""

    metric: str
    nua_corpus: str
    """``doclaynet`` (nhãn bbox) · ``olmocr`` (nhãn khẳng định) · ``ca_hai``.

    Suy từ `Metric.gt_kinds`, không gán tay. Hai nửa **rời nhau** (giao = 0 tài liệu),
    nên hai metric khác nửa không bao giờ được đứng chung một hàng bảng xếp hạng.
    """
    n_ung_vien: int
    """Số tài liệu thuộc nửa corpus của metric này — mẫu số của `n_toi_da`."""
    n_toi_da: int
    """Trần: số tài liệu một engine **hoàn hảo** vẫn chấm được."""
    bac: Bac
    ly_do: str
    """Vì sao không nhiều hơn — chuỗi lấy từ `_na_rieng()` của chính metric.

    Rỗng khi trần bằng đúng `n_ung_vien` (không tài liệu nào bị chặn).
    """
    nang_luc_can: tuple[str, ...]
    """`Metric.requires` — engine phải **khai** đủ mới chạm tới, dù nhãn có sẵn."""

    def khoa_sap_xep(self) -> tuple[int, int, str]:
        """Bậc trước, trần giảm dần, rồi tên — tất định, không phụ thuộc thứ tự dict."""
        return (_THU_TU_BAC[self.bac], -self.n_toi_da, self.metric)

    def to_dict(self) -> dict[str, object]:
        return {
            "metric": self.metric,
            "nua_corpus": self.nua_corpus,
            "n_ung_vien": self.n_ung_vien,
            "n_toi_da": self.n_toi_da,
            "bac": self.bac,
            "ly_do": self.ly_do,
            "nang_luc_can": list(self.nang_luc_can),
        }


def _bac(n: int) -> Bac:
    if n == 0:
        return "tran_0"
    return "do_duoc" if n >= NGUONG_DO_DUOC else "mong"


def _nua_corpus(cls: type[Metric]) -> str:
    nhan = AnnotationGT in cls.gt_kinds
    khang_dinh = AssertionGT in cls.gt_kinds
    if nhan and khang_dinh:
        return "ca_hai"
    if khang_dinh:
        return "olmocr"
    return "doclaynet"


def _engine_hoan_hao(gt: GroundTruth) -> OcrResult:
    """Engine giả trả về **đúng** ground truth, khai đủ mọi năng lực, không hỏng.

    Đây là cận trên đúng nghĩa: không engine thật nào làm tốt hơn "trả lại đáp án".
    Với `AssertionGT` không có gì để phản chiếu — mọi `_na_rieng` của nhóm khẳng định
    chỉ đọc `gt`, `text_md` chưa từng được nhìn tới trước khi `_compute()` chạy.
    """
    chung = {
        "engine": "__tran_do_duoc__",
        "engine_version": "0",
        "doc_id": gt.doc_id,
        "capabilities": frozenset(Capability),
        "failed": False,
    }
    if isinstance(gt, AnnotationGT):
        return OcrResult(
            **chung,
            text_md=gt.text,
            blocks=gt.blocks,
            # `AnnotationGT.images` là `Box` trần, `OcrResult.images` là `OcrImage`
            # — bọc lại chứ không gán thẳng. Metric ảnh đọc qua `OcrImage.box`.
            images=tuple(OcrImage(box=b) for b in gt.images),
            tables=gt.tables,
            page_sizes=gt.page_sizes,
        )
    return OcrResult(**chung, text_md="")


def _cham_duoc(metric: Metric, gt: GroundTruth) -> str | None:
    """`None` = chấm được. Ngược lại là lý do chặn, lấy nguyên văn từ metric."""
    if not isinstance(gt, metric.gt_kinds):
        return f"sai loại nhãn (cần {'/'.join(k.__name__ for k in metric.gt_kinds)})"
    rieng = metric._na_rieng(gt, _engine_hoan_hao(gt))
    if rieng is None:
        return None
    ly_do = rieng[1].get("ly_do")
    return str(ly_do) if ly_do else rieng[0].value


def tran_do_duoc(
    gt_doclaynet: dict[str, AnnotationGT],
    gt_olmocr: dict[str, AssertionGT],
    *,
    metrics: list[str] | None = None,
) -> dict[str, Tran]:
    """Trần của **mọi** metric trong sổ đăng ký, khoá theo tên metric.

    Danh sách lấy từ `registry.list_metrics()` chứ không viết tay: thêm một metric mà
    quên thêm vào đây thì nó vắng mặt lặng lẽ, và vắng mặt đọc như "không có vấn đề".
    """
    ten = sorted(metrics) if metrics is not None else registry.list_metrics()
    ket: dict[str, Tran] = {}

    for m in ten:
        cls = registry.get_metric(m)
        metric = cls()
        nua = _nua_corpus(cls)
        ung_vien: list[GroundTruth] = []
        if nua in ("doclaynet", "ca_hai"):
            ung_vien += [gt_doclaynet[k] for k in sorted(gt_doclaynet)]
        if nua in ("olmocr", "ca_hai"):
            ung_vien += [gt_olmocr[k] for k in sorted(gt_olmocr)]

        chan: Counter[str] = Counter()
        n_dat = 0
        for gt in ung_vien:
            ly_do = _cham_duoc(metric, gt)
            if ly_do is None:
                n_dat += 1
            else:
                chan[ly_do] += 1

        # **Mọi** lý do chặn, không chỉ lý do đông nhất: `cell_f1` bị chặn bởi hai
        # luật rất khác nhau — 161 tài liệu không có bảng, và 43 tài liệu *có* bảng
        # nhưng nhãn không có nội dung ô. In mỗi cái đầu thì trần 0 đọc như "bộ mẫu
        # ít bảng", che mất sự thật là 43 bảng kia cũng không dùng được.
        # `most_common()` không tất định khi hoà, nên sắp lại theo (-số, chuỗi).
        giai_thich = "; ".join(
            f"{ly_do} ({k}/{len(ung_vien)} tài liệu)"
            for ly_do, k in sorted(chan.items(), key=lambda kv: (-kv[1], kv[0]))
        )

        ket[m] = Tran(
            metric=m,
            nua_corpus=nua,
            n_ung_vien=len(ung_vien),
            n_toi_da=n_dat,
            bac=_bac(n_dat),
            ly_do=giai_thich,
            nang_luc_can=tuple(sorted(c.value for c in cls.requires)),
        )

    return ket


def thu_tu_metric(trans: dict[str, Tran]) -> list[str]:
    """Tên metric xếp theo bậc — dùng chung cho mọi bảng và mọi hình."""
    return [t.metric for t in sorted(trans.values(), key=Tran.khoa_sap_xep)]


def du_lieu_tran(
    trans: dict[str, Tran],
    *,
    n_doclaynet: int,
    n_olmocr: int,
    generated_at: str,
) -> str:
    """`results/measurable-ceiling.json` — JSON tất định (sort_keys, LF do người gọi)."""
    return json.dumps(
        {
            "generated_at": generated_at,
            "nguon": "ground-truth/ (không đọc prediction/ — trần này độc lập engine)",
            "nguong_do_duoc": NGUONG_DO_DUOC,
            "corpus": {
                "doclaynet": n_doclaynet,
                "olmocr": n_olmocr,
                "giao": 0,
                "ghi_chu": "hai nửa rời nhau; tổng là tổng thật, không phải hợp",
            },
            # `mo_ta` lấy từ docstring lớp metric: người đọc JSON không có bảng
            # markdown bên cạnh để tra tên metric nghĩa là gì.
            "tran": [
                {**trans[m].to_dict(), "mo_ta": glossary.mo_ta_metric(m)}
                for m in thu_tu_metric(trans)
            ],
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


_TEN_BAC = {
    "do_duoc": f"đo được (≥{NGUONG_DO_DUOC} tài liệu)",
    "mong": f"mỏng (<{NGUONG_DO_DUOC} tài liệu)",
    "tran_0": "trần 0 — không engine nào chấm được",
}


def bang_tran(
    trans: dict[str, Tran],
    *,
    n_doclaynet: int,
    n_olmocr: int,
    generated_at: str,
) -> str:
    """`tables/ceiling.md` — bảng markdown xếp theo bậc."""
    d: list[str] = [
        "# Trần đo được của bộ nhãn",
        "",
        "Bảng này **không đọc `prediction/`**. Nó trả lời: với ground truth đang có,",
        "mỗi metric nhiều nhất chấm được bao nhiêu tài liệu — kể cả khi engine hoàn hảo.",
        "Trần 0 nghĩa là con số N/A trong bảng xếp hạng là lỗi của **bộ mẫu**, không",
        "phải của engine.",
        "",
        f"- DocLayNet (nhãn bbox): **{n_doclaynet}** tài liệu",
        f"- olmOCR (nhãn khẳng định): **{n_olmocr}** tài liệu",
        "- Giao hai nửa: **0** tài liệu — không metric nào bắc cầu được qua cả hai.",
        "",
        f"Sinh lúc `{generated_at}` bởi `src/ocr_bench/ceiling.py`; cột *vì sao* là",
        "chuỗi do chính `_na_rieng()` của metric trả về, cột *đo cái gì* lấy từ",
        "docstring của lớp metric.",
        "",
        *glossary.khoi_doc_bang("glossary.md"),
    ]
    mo_ta = glossary.cac_mo_ta()

    for bac in ("do_duoc", "mong", "tran_0"):
        nhom = [t for t in sorted(trans.values(), key=Tran.khoa_sap_xep) if t.bac == bac]
        if not nhom:
            continue
        d += [
            f"## {_TEN_BAC[bac]}",
            "",
            "| metric | đo cái gì | nửa corpus | trần | trên tổng | năng lực cần "
            "| vì sao không hơn |",
            "|---|---|---|---:|---:|---|---|",
        ]
        for t in nhom:
            nang_luc = ", ".join(f"`{c}`" for c in t.nang_luc_can) or "—"
            d.append(
                f"| `{t.metric}` | {mo_ta.get(t.metric) or '—'} | {t.nua_corpus} | "
                f"{t.n_toi_da} | {t.n_ung_vien} | {nang_luc} | {t.ly_do or '—'} |"
            )
        d.append("")

    return "\n".join(d) + "\n"
