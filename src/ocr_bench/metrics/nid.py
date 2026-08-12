"""B4 — thứ tự đọc: `nid` (normalized indel distance trên chuỗi block).

Vì sao cần: văn bản đúng từng chữ nhưng đảo thứ tự đoạn thì vô dụng với RAG, và
CER/WER (B1) **không** bắt được chuyện đó — chúng so hai chuỗi ký tự đã nối liền,
đảo hai đoạn chỉ làm chúng nhúc nhích.

Bốn quyết định của file này:

1. **Không có nhãn thứ tự đọc thì N/A, tuyệt đối không tự chế nhãn.** Bộ mẫu hiện
   tại (DocLayNet) không có `reading_order` — xem docstring `AnnotationGT`. Cách
   "sửa" hấp dẫn nhất là sắp block theo hình học rồi lấy đó làm nhãn. **Sai.** Khi
   đó ta chấm engine theo heuristic của bench: engine sắp giống heuristic được
   điểm cao kể cả khi heuristic sai, và bảng xếp hạng đo sự giống nhau chứ không
   đo chất lượng. N/A là câu trả lời trung thực cho tới khi có nhãn.

2. **Ghép theo TÂM NẰM TRONG, không theo IoU.** Đây là khác biệt quan trọng nhất
   so với B3. Số block trên mỗi tài liệu: GT ≈ 14, opendataloader ≈ 16, marker
   ≈ 14, nhưng **pdf_inspector ≈ 82** — block của nó là *dòng*, không phải đoạn.
   Ghép bằng IoU ≥ 0.5 thì một dòng nằm gọn trong một đoạn ra IoU ≈ 0.1, không
   cặp nào khớp, và pdf_inspector bị chấm 0 vì **chia mịn hơn** chứ không phải vì
   **đọc sai thứ tự**. Metric khi đó đo nhầm thứ.

3. **Gộp trùng liên tiếp.** Hệ quả bắt buộc của quyết định 2: 5 dòng cùng thuộc
   một đoạn sinh ra `[3,3,3,3,3]`, gộp thành `[3]`. Engine chia nhỏ mà đọc đúng
   thứ tự vẫn được 1.0. Không gộp thì quyết định 2 vô nghĩa.

   **Vì thế phép ghép ở file này KHÔNG được thay bằng `metrics/matching.py`.**
   Task 8 đổi `imgf1.py` và `layout.py` sang ghép tối ưu **1-1**; ghép ở đây cố ý
   là **nhiều-một** và đó là toàn bộ nội dung của quyết định 2. Ép 1-1 vào đây thì
   82 dòng của pdf_inspector chỉ còn 14 dòng được ghép, 68 dòng còn lại thành
   `None`, và metric quay về đúng cái lỗi mà quyết định 2 tồn tại để tránh. Hai
   phép ghép giải hai bài toán khác nhau, không phải một bài toán bị viết hai lần.

4. **Đơn vị chuỗi là chỉ số block, không phải ký tự.** Bản gốc
   (`opendataloader-bench`) chạy NID trên ký tự văn bản. Không dùng được ở đây:
   nhãn DocLayNet **không có text** (0/2941 block). Xem bảng đối chiếu ở
   `MUON_VA_KHAC` bên dưới — AC-04 đòi ghi rõ mượn gì và khác chỗ nào.
"""

from __future__ import annotations

from typing import ClassVar

from ocr_bench.metrics.base import Metric
from ocr_bench.types import (
    AnnotationGT,
    Box,
    Capability,
    GroundTruth,
    NAReason,
    OcrResult,
)

__all__ = [
    "MUON_VA_KHAC",
    "ghep_theo_tam",
    "chuoi_thu_tu",
    "nid_score",
    "NidMetric",
]

MUON_VA_KHAC = {
    "y_tuong_goc": "NID trên chuỗi để đo thứ tự đọc — mượn nguyên từ opendataloader-bench",
    "chuan_hoa": "về [0,1] — mượn",
    "don_vi_chuoi": "chỉ số block, KHÁC: bản gốc dùng ký tự; nhãn DocLayNet không có text",
    "ghep_cap": "tâm nằm trong box, KHÁC: bản gốc ghép theo văn bản",
    "do_min": "gộp trùng liên tiếp, KHÁC: bản gốc không xử lý chênh lệch độ mịn",
    "thieu_nhan": "N/A, KHÁC: không chế nhãn bằng sắp hình học",
}
"""AC-04 — mượn gì, khác chỗ nào, và vì sao khác. Để ở dạng dữ liệu chứ không chỉ
trong docstring để test đọc được và giai đoạn D trích ra được."""


def _tam(b: Box) -> tuple[int, float, float]:
    return b.page, (b.x0 + b.x1) / 2.0, (b.y0 + b.y1) / 2.0


def _dien_tich(b: Box) -> float:
    return max(0.0, b.x1 - b.x0) * max(0.0, b.y1 - b.y0)


def ghep_theo_tam(nhan: list[Box], doan: list[Box]) -> list[int | None]:
    """Mỗi box đoán thuộc về box nhãn nào — theo tâm nằm trong.

    Trả danh sách cùng độ dài `doan`; `None` nghĩa là tâm không rơi vào box nhãn
    nào (engine bắt thừa).

    Nhãn lồng nhau (caption nằm trong picture, ô nằm trong bảng) thì chọn box
    **nhỏ nhất** chứa tâm: box lớn luôn chứa tâm của box nhỏ, nên chọn box lớn sẽ
    làm mọi thứ nằm trong nó biến thành cùng một chỉ số và bị bước gộp trùng xoá
    sạch.
    """
    ra: list[int | None] = []
    for b in doan:
        trang, cx, cy = _tam(b)
        ung_vien = [
            i
            for i, a in enumerate(nhan)
            if a.page == trang and a.x0 <= cx <= a.x1 and a.y0 <= cy <= a.y1
        ]
        if not ung_vien:
            ra.append(None)
            continue
        ra.append(min(ung_vien, key=lambda i: (_dien_tich(nhan[i]), i)))
    return ra


def chuoi_thu_tu(gan: list[int | None]) -> list[int]:
    """Bỏ `None`, gộp trùng **liên tiếp**. Xem quyết định 3.

    Chỉ gộp liên tiếp, không gộp toàn cục: `[3, 5, 3]` giữ nguyên, vì engine quay
    lại một đoạn đã đọc *là* một lỗi thứ tự thật, không phải chuyện độ mịn.
    """
    ra: list[int] = []
    for g in gan:
        if g is None:
            continue
        if ra and ra[-1] == g:
            continue
        ra.append(g)
    return ra


def nid_score(
    thu_tu_nhan: list[int], nhan: list[Box], doan: list[Box]
) -> tuple[float, dict[str, object]]:
    """Trả `(điểm, chi tiết)`. `thu_tu_nhan` là dãy chỉ số vào `nhan`, theo thứ tự đọc."""
    from rapidfuzz.distance import Indel  # nhập lười: `rapidfuzz` là extra `metrics`

    gan = ghep_theo_tam(nhan, doan)
    chuoi = chuoi_thu_tu(gan)
    # Chuỗi tham chiếu chỉ giữ những block engine thực sự chạm tới. Block nhãn mà
    # engine bỏ sót hoàn toàn là chuyện của B3/B6 (độ phủ), không phải của thứ tự
    # đọc — phạt ở đây là phạt hai lần cùng một lỗi.
    co_mat = set(chuoi)
    tham_chieu = [i for i in thu_tu_nhan if i in co_mat]

    khoang_cach = Indel.normalized_distance(tham_chieu, chuoi)
    diem = 1.0 - khoang_cach
    return diem, {
        "n_nhan": len(nhan),
        "n_doan": len(doan),
        "n_doan_khong_trung_nhan_nao": sum(1 for g in gan if g is None),
        "do_dai_chuoi_doan": len(chuoi),
        "do_dai_chuoi_tham_chieu": len(tham_chieu),
        "khoang_cach_indel_chuan_hoa": round(khoang_cach, 6),
    }


class NidMetric(Metric):
    """Thứ tự đọc. 1.0 = đúng thứ tự nhãn; đảo đoạn thì tụt.

    Độc lập với độ mịn: chia một đoạn thành nhiều block vẫn 1.0 (quyết định 2+3).
    """

    name: ClassVar[str] = "nid"
    requires: ClassVar[frozenset[Capability]] = frozenset({Capability.BLOCK_BBOX})
    gt_kinds: ClassVar[tuple[type, ...]] = (AnnotationGT,)

    @staticmethod
    def _box_nhan(gt: AnnotationGT) -> list[Box]:
        return [b.box for b in gt.blocks if b.box is not None]

    @staticmethod
    def _box_doan(result: OcrResult) -> list[Box]:
        return [b.box for b in result.blocks if b.box is not None]

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AnnotationGT)
        if not gt.reading_order:
            # Quyết định 1. Đây là ca xảy ra với 100% bộ mẫu hiện tại.
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "nhãn không có thứ tự đọc; xem AnnotationGT.reading_order"
            }
        if len(gt.reading_order) < 2:
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "dưới 2 block thì không có thứ tự nào để so"
            }
        return None

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        # Engine ĐÃ khai BLOCK_BBOX mà không trả block nào: lỗi engine, chấm 0.
        # `nid_score` tự ra 0.0 vì chuỗi đoán rỗng còn tham chiếu rỗng theo →
        # `Indel.normalized_distance([], [])` là 0.0 tức điểm 1.0, nên phải chặn.
        doan = self._box_doan(result)
        if not doan:
            return 0.0, {"ly_do": "engine khai BLOCK_BBOX nhưng không trả block nào"}
        return nid_score(list(gt.reading_order), self._box_nhan(gt), doan)
