"""Chú giải: mỗi metric đo cái gì, và mỗi từ trong bảng nghĩa là gì.

Người đọc lần đầu gặp dòng ``type_f1 | 0.542 (0% hỏng, n=203)`` không có đường nào
biết ``type_f1`` đo cái gì, ``0.542`` là cao hay thấp, hay ``n=203`` là nhiều hay ít.
Mọi artifact trước đây đều mặc định người đọc đã biết — mặc định đó không đúng với
bất kỳ ai chưa viết bộ metric này.

**Mô tả từng metric lấy thẳng từ docstring của lớp metric**, không chép tay sang đây.
Chép tay thì sửa luật trong metric mà quên sửa chú giải, và một dòng chú giải sai còn
tệ hơn không có: nó dạy người đọc hiểu sai rồi tin. Đổi lại, dòng mô tả phải nằm ngay
ở **câu đầu** docstring của metric — `test_moi_metric_deu_co_mo_ta` khoá điều đó.

Phần từ ngữ (``F1``, ``IoU``, ``trần``, ``nửa corpus``, ``†``, ``‡``) viết một lần ở
đây vì nó không thuộc về metric nào. Nhắc lại dưới mỗi bảng thì sẽ có bốn bản sao,
và bốn bản sao sẽ lệch nhau.
"""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

from ocr_bench import registry

if TYPE_CHECKING:  # pragma: no cover - chỉ để chú thích kiểu
    from ocr_bench.ceiling import Tran

__all__ = [
    "mo_ta_metric",
    "cac_mo_ta",
    "THUAT_NGU",
    "bang_thuat_ngu",
    "khoi_doc_bang",
    "doc_mot_o",
]


def mo_ta_metric(ten: str) -> str:
    """Một câu: metric này đo cái gì. Nguồn là docstring của chính lớp metric.

    Trả chuỗi rỗng khi metric không có docstring — người gọi in ``—``. Không bịa một
    câu thay thế: một mô tả sinh ra ở đây sẽ không có gì ràng nó với hành vi thật.
    """
    cls = registry.get_metric(ten)
    doc = inspect.getdoc(cls) or ""
    return doc.split("\n", 1)[0].strip()


def cac_mo_ta() -> dict[str, str]:
    """`{tên metric: mô tả}` cho **mọi** metric trong sổ đăng ký."""
    return {m: mo_ta_metric(m) for m in registry.list_metrics()}


THUAT_NGU: tuple[tuple[str, str], ...] = (
    (
        "`n`",
        "Số tài liệu thật sự chấm được **ô đó** — mẫu số của chính con số đứng cạnh, "
        "không phải số tài liệu engine chạy qua. Điểm không kèm `n` là điểm không đọc "
        "được: `1.000` trên 9 tài liệu và `0.910` trên 1403 tài liệu không cùng độ tin.",
    ),
    (
        "`% hỏng`",
        "Tỉ lệ tài liệu engine chạy lỗi (timeout, crash, không ra đầu ra). Phải đọc "
        "**riêng**: các phép so sánh thống kê chỉ dùng tài liệu cả hai engine đều chấm "
        "được, nên chúng bỏ qua toàn bộ khác biệt về tỉ lệ hỏng.",
    ),
    (
        "trung bình có phạt (*penalized mean*)",
        "Trung bình trong đó tài liệu hỏng tính là 0, thay vì bị loại khỏi mẫu. Loại "
        "ra là thưởng cho engine hỏng nhiều — nó bỏ đi đúng những tài liệu khó.",
    ),
    (
        "`N/A`",
        "Engine **không khai đủ năng lực** để metric chạm tới (ví dụ metric cần bbox mà "
        "engine chỉ trả văn bản). Đây không phải điểm 0, và dòng của nó không bị bỏ đi.",
    ),
    (
        "`chưa có nhãn`",
        "Engine chạy được, nhưng bộ mẫu không có nhãn hợp loại để đối chiếu. Thiếu sót "
        "của **bộ mẫu**, không phải của engine.",
    ),
    (
        "trần — *ceiling* (`tables/ceiling.md`)",
        "Số tài liệu **nhiều nhất** metric chấm được nếu có một engine hoàn hảo trả về "
        "đúng bằng nhãn. Trần 0 nghĩa là không engine nào đo được gì ở metric đó — "
        "mọi ô N/A của nó là lỗi bộ mẫu.",
    ),
    (
        "nửa corpus (*corpus half*)",
        "Bộ mẫu gồm hai nửa **rời nhau, giao đúng 0 tài liệu**: `doclaynet` (nhãn khung "
        "+ loại khối) và `olmocr` (nhãn khẳng định đúng/sai về nội dung). Không bao giờ "
        "so một ô của nửa này với một ô của nửa kia.",
    ),
    (
        "tập chung — *common set* (`tables/common-set.md`)",
        "Tập tài liệu **mọi engine trong bảng đều có dự đoán**. Đây là bảng duy nhất mà "
        "đặt hai ô cạnh nhau rồi kết luận là hợp lệ.",
    ),
    (
        "F1",
        "Trung bình điều hoà của độ chính xác (thứ tìm ra có đúng không) và độ bao phủ "
        "(bỏ sót bao nhiêu). 1.0 là hoàn hảo; đoán bừa nhiều làm tụt cả hai vế.",
    ),
    (
        "macro-F1",
        "F1 tính riêng cho từng loại rồi lấy trung bình các loại, nên một loại hiếm nặng "
        "ngang một loại phổ biến.",
    ),
    (
        "IoU",
        "Diện tích giao chia diện tích hợp của hai khung — hai khung trùng nhau tới đâu. "
        "`IoU ≥ 0.5` là quy ước \"coi như tìm đúng\".",
    ),
    (
        "CER · WER",
        "Tỉ lệ lỗi ký tự · lỗi từ. Trong mọi bảng ở đây in dưới dạng `1 − lỗi`, để cùng "
        "chiều với các metric khác: **cao hơn là tốt hơn**.",
    ),
    (
        "TEDS",
        "Khoảng cách sửa cây giữa bảng HTML engine sinh ra và bảng HTML trong nhãn. "
        "`teds_struct` chỉ xét cấu trúc, bỏ nội dung ô.",
    ),
    (
        "NID",
        "Khoảng cách sửa chuỗi đã chuẩn hoá, dùng để đo thứ tự đọc: đảo đoạn thì tụt.",
    ),
    (
        "†",
        "Metric **ngược chiều**: thấp hơn mới là tốt hơn. Bị loại khỏi mọi bảng xếp hạng "
        "theo điểm, và lý do in nguyên văn ngay dưới bảng có nó.",
    ),
    (
        "‡",
        "Đo được nhưng **không phân biệt**: mọi engine chênh nhau dưới ngưỡng, nên con "
        "số đúng mà không dùng để chọn engine được. Khác hẳn N/A — ở đây phép đo chạy "
        "đủ, chỉ là nó không tách được các engine ra.",
    ),
)
"""Từ ngữ xuất hiện trong bảng, kèm nghĩa. Thứ tự cố định — đây là thứ tự in ra."""


def doc_mot_o() -> list[str]:
    """Giải nghĩa **một ô thật** trong bảng, từng mảnh một.

    Câu hỏi đầu tiên của mọi người đọc là "0.790 nói lên điều gì" — và trước khối này
    không artifact nào trả lời. Bảng thuật ngữ định nghĩa từng ký hiệu rời rạc (`n`,
    `% hỏng`, `F1`), nhưng người đọc gặp chúng **dính liền trong một ô** và phải tự
    ghép lại. Ghép sai kiểu phổ biến nhất là đọc `0.790` thành "đúng 79%", rồi mang
    con số đó đi báo cáo như một lời hứa về chất lượng.

    Ngưỡng phân biệt lấy từ `report.NGUONG_PHAN_BIET`, không chép số vào đây: đổi
    ngưỡng trong luật chấm mà đoạn văn vẫn ghi số cũ thì đoạn văn thành lời nói dối.
    """
    from ocr_bench import report  # nội bộ: `report` đã nạp `glossary`, tránh vòng

    nguong = report.NGUONG_PHAN_BIET
    return [
        "Mọi ô điểm trong báo cáo đều có dạng dưới đây. Lấy một ô thật ở mục 3 làm ví dụ:",
        "",
        "```",
        "| block_f1 | 0.790 (n=203, fail 0%) |",
        "```",
        "",
        "| mảnh | đọc là |",
        "|---|---|",
        "| `block_f1` | tên metric — đo cái gì thì tra bảng ngay dưới đây |",
        "| `0.790` | điểm trung bình trên thang **0 → 1**, cao hơn là tốt hơn |",
        "| `n=203` | con số đó tính trên **203 tài liệu**, không phải trên cả bộ mẫu |",
        "| `fail 0%` | không tài liệu nào engine chạy lỗi |",
        "",
        "**Thang điểm.** `1.000` là engine trùng khớp hoàn toàn với nhãn; `0.000` là "
        "không trùng gì.",
        "",
        "**Nhưng `0.790` KHÔNG có nghĩa là \"đúng 79%\".** Đây là chỗ dễ hiểu sai nhất, "
        "vì hai lý do:",
        "",
        "1. Phần lớn metric ở đây là **F1** — trung bình điều hoà của hai tỉ lệ khác "
        "nhau (tìm ra có đúng không, và bỏ sót bao nhiêu). Nó không phải tỉ lệ phần "
        "trăm của bất cứ thứ gì đếm được.",
        "2. Điểm phụ thuộc vào **ngưỡng quy ước** trong luật chấm (ví dụ `IoU ≥ 0.5` "
        "mới coi là tìm đúng một khung). Đổi ngưỡng thì điểm đổi theo trong khi engine "
        "không đổi một dòng nào.",
        "",
        "Vì vậy con số này dùng để **xếp hạng các engine trên cùng bộ mẫu, cùng luật "
        "chấm** — không dùng để hứa với khách hàng rằng công cụ \"chính xác 79%\".",
        "",
        "**Chênh bao nhiêu mới đáng kể?** Dưới "
        f"**{nguong:.2f}** thì báo cáo đánh dấu `‡` và không kết luận engine nào hơn. "
        "Trên ngưỡng đó vẫn phải xem `results/statistical-tests.json` — chênh lệch lớn "
        "trên 15 tài liệu có thể yếu hơn chênh lệch nhỏ trên 1403 tài liệu.",
        "",
    ]


def khoi_doc_bang(duong_dan_chu_giai: str = "tables/glossary.md") -> list[str]:
    """Vài dòng đặt đầu mỗi artifact: đọc bảng theo thứ tự nào, tra nghĩa ở đâu."""
    return [
        f"> **Chưa quen bộ metric này?** `{duong_dan_chu_giai}` giải thích từng metric "
        "đo cái gì và mọi ký hiệu trong bảng (`n`, `% hỏng`, `N/A`, `trần`, `†`, `‡`).",
        ">",
        "> Đọc theo thứ tự: **`n` trước, điểm sau** — một điểm cao trên 9 tài liệu không "
        "so được với một điểm thấp hơn trên 1403 tài liệu.",
        "",
    ]


def bang_thuat_ngu(trans: dict[str, Tran], *, generated_at: str) -> str:
    """`tables/glossary.md` — metric nào đo gì, ký hiệu nào nghĩa gì.

    Bảng metric ở đây **có cột `nửa corpus`**, nên nó được phép liệt kê cả hai nửa
    trong một bảng: luật cấm trộn nhắm vào bảng đặt hai con số cạnh nhau mà không nói
    chúng đến từ hai tập rời nhau. Ở đây không có con số nào để so — chỉ có mô tả.
    """
    mo_ta = cac_mo_ta()
    d: list[str] = [
        "# Chú giải — đọc bảng kết quả thế nào",
        "",
        "File này **không chứa kết quả**. Nó giải thích các từ mà mọi file kết quả khác "
        "dùng, để người đọc lần đầu không phải suy ra nghĩa từ con số.",
        "",
        f"Sinh lúc `{generated_at}` bởi `src/ocr_bench/glossary.py`; cột *đo cái gì* lấy "
        "từ docstring của chính lớp metric, không viết tay.",
        "",
        "## 1. Một ô trong bảng nói gì",
        "",
        *doc_mot_o(),
        "## 2. Mỗi metric đo cái gì",
        "",
        "Cột *trần* là số tài liệu nhiều nhất metric chấm được với bộ nhãn hiện có — "
        "chi tiết ở `tables/ceiling.md`.",
        "",
        "| metric | nửa corpus | trần | đo cái gì |",
        "|---|---|---:|---|",
    ]

    from ocr_bench.ceiling import Tran as _Tran  # nội bộ: tránh vòng import lúc nạp

    for t in sorted(trans.values(), key=_Tran.khoa_sap_xep):
        d.append(
            f"| `{t.metric}` | {t.nua_corpus} | {t.n_toi_da} | "
            f"{mo_ta.get(t.metric) or '—'} |"
        )

    d += ["", "## 3. Ký hiệu và từ ngữ trong bảng", ""]
    for tu, nghia in THUAT_NGU:
        d += [f"**{tu}** — {nghia}", ""]

    d += [
        "## 4. Thứ tự đọc một bảng kết quả",
        "",
        "1. Bảng này thuộc **nửa corpus** nào? Hai nửa không so với nhau được.",
        "2. **`n`** của ô là bao nhiêu? Dưới vài chục thì đừng kết luận gì.",
        "3. **`% hỏng`** — engine điểm cao nhưng hỏng 55% không phải engine tốt hơn.",
        "4. Chênh lệch có **ý nghĩa thống kê** không? Xem "
        "`results/statistical-tests.json`; mắt thường không phân biệt được 0.606 với "
        "0.495 trên cỡ mẫu bất kỳ.",
        "5. Muốn so hai engine trực tiếp thì đọc `tables/common-set.md`, không đọc "
        "`tables/overall.md` — ở đó mỗi engine chạy một tập tài liệu khác nhau.",
        "",
    ]
    return "\n".join(d) + "\n"
