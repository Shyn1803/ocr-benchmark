"""B4 — phân cấp tiêu đề: `heading`.

AC-02 cấm lấy "đếm đúng bao nhiêu tiêu đề" làm câu trả lời, và cấm đúng chỗ: một
engine gắn `#` cho *mọi* tiêu đề vẫn đếm đúng số lượng trong khi đã xoá sạch phân
cấp. Đếm không phân biệt được hai thứ đó.

Ba quyết định:

1. **So QUAN HỆ theo cặp, không so số cấp tuyệt đối.** Engine đánh `#`/`##`;
   DocLayNet đánh `Title`/`Section-header`. Đó là hai **thang** khác nhau, không
   phải hai câu trả lời khác nhau. So số tuyệt đối là phạt engine vì dùng thang
   khác. Với mỗi cặp tiêu đề ghép được, nhãn nói `<` `=` hay `>`, engine nói gì về
   cùng cặp ấy, điểm là tỉ lệ đồng ý. Bất biến với thang — đúng cái AC-02 muốn.

2. **⚠️ Trần của nhãn là 2 MỨC.** DocLayNet chỉ có `Title` và `Section-header`
   (ánh xạ ở `CAP_NHAN`: TITLE→1, HEADING→2). Metric này **không nhìn thấy** lỗi
   lồng sâu: `###` đặt nhầm chỗ so với `####` là vô hình ở đây. Điểm `heading` cao
   nghĩa là "không đảo ngược tiêu đề chính với tiêu đề mục", KHÔNG nghĩa là "phân
   cấp tốt". Đừng đọc nó rộng hơn thế.

3. **Nhãn chỉ có một cấp thì N/A, không phải 1.0.** Không có quan hệ nào để so thì
   không có gì để chấm; chấm 1.0 là rót điểm miễn phí, đúng lỗi đã tránh ở B3.

Ghép cặp dùng chung `ghep_theo_tam` của `nid.py` — cùng lý do độ mịn, xem
`nid` quyết định 2.
"""

from __future__ import annotations

import itertools
from typing import ClassVar

from ocr_bench.metrics.base import Metric
from ocr_bench.metrics.nid import ghep_theo_tam
from ocr_bench.types import (
    AnnotationGT,
    BlockType,
    Capability,
    GroundTruth,
    NAReason,
    OcrBlock,
    OcrResult,
)

__all__ = ["CAP_NHAN", "LOAI_TIEU_DE", "cap_cua_nhan", "dong_thuan_cap", "HeadingMetric"]

LOAI_TIEU_DE = frozenset({BlockType.TITLE, BlockType.HEADING})

CAP_NHAN = {BlockType.TITLE: 1, BlockType.HEADING: 2}
"""Hai lớp **có thật** của DocLayNet → hai cấp. Không suy diễn thêm cấp nào."""


def cap_cua_nhan(b: OcrBlock) -> int | None:
    """Cấp của một block tiêu đề. `None` nếu block không phải tiêu đề.

    `level` do engine khai được ưu tiên; thiếu thì rơi về ánh xạ theo loại. Nhãn
    DocLayNet luôn rơi vào nhánh sau (0/2941 block có `level`).
    """
    if b.block_type not in LOAI_TIEU_DE:
        return None
    if b.level is not None:
        return b.level
    return CAP_NHAN[b.block_type]


def dong_thuan_cap(
    cap_nhan: list[int], cap_doan: list[int]
) -> tuple[float, dict[str, object]]:
    """Tỉ lệ cặp mà hai bên nói cùng một quan hệ thứ tự. Hai danh sách đã ghép đôi."""

    def dau(x: int, y: int) -> int:
        return (x > y) - (x < y)

    dong = 0
    tong = 0
    for i, j in itertools.combinations(range(len(cap_nhan)), 2):
        tong += 1
        if dau(cap_nhan[i], cap_nhan[j]) == dau(cap_doan[i], cap_doan[j]):
            dong += 1
    if tong == 0:
        return 0.0, {"n_cap": 0}
    return dong / tong, {"n_cap": tong, "n_cap_dong_thuan": dong}


class HeadingMetric(Metric):
    """Phân cấp tiêu đề. 1.0 = mọi quan hệ trên/dưới giữa các tiêu đề đều khớp nhãn.

    Đọc kèm quyết định 2 ở docstring module: nhãn chỉ có 2 mức.
    """

    name: ClassVar[str] = "heading"
    requires: ClassVar[frozenset[Capability]] = frozenset(
        {Capability.BLOCK_BBOX, Capability.HEADING_LEVEL}
    )
    # Hai năng lực, hai lý do. `BLOCK_BBOX` vì ghép cặp là hình học. `HEADING_LEVEL`
    # vì đó **chính là** điều metric này kiểm chứng — engine không khai thì nó không
    # nhận làm việc phân cấp, và chấm nó 0 là phạt vì việc nó chưa từng nhận. Đây là
    # đúng lỗi B3 đã ghi lại (`img_f1`: thiếu năng lực → N/A, không phải 0.0), và
    # pdf_inspector là ca thật: 0 block tiêu đề trên toàn bộ 204 tài liệu.
    # KHÔNG đòi `SECTION_HIERARCHY` — cây là thứ khác, xem docstring `Capability`.
    gt_kinds: ClassVar[tuple[type, ...]] = (AnnotationGT,)

    @staticmethod
    def _tieu_de(blocks) -> list[OcrBlock]:
        return [b for b in blocks if b.block_type in LOAI_TIEU_DE and b.box is not None]

    @classmethod
    def _ghep(
        cls, gt: AnnotationGT, result: OcrResult
    ) -> tuple[list[int], list[int], dict[str, object]]:
        """Trả `(cấp nhãn, cấp đoán, chi tiết)` của những tiêu đề ghép được."""
        nhan = cls._tieu_de(gt.blocks)
        doan = cls._tieu_de(result.blocks)
        gan = ghep_theo_tam([b.box for b in nhan], [b.box for b in doan])

        # Một nhãn có thể hút nhiều block đoán (engine tách tiêu đề thành 2 dòng).
        # Lấy block đoán ĐẦU TIÊN — nó là cái mang cấp của tiêu đề; những dòng sau
        # là phần tiếp theo của cùng tiêu đề đó, không phải một tiêu đề mới.
        dau_tien: dict[int, int] = {}
        for vt_doan, vt_nhan in enumerate(gan):
            if vt_nhan is not None and vt_nhan not in dau_tien:
                dau_tien[vt_nhan] = vt_doan

        cap_nhan: list[int] = []
        cap_doan: list[int] = []
        for vt_nhan in sorted(dau_tien):
            cn = cap_cua_nhan(nhan[vt_nhan])
            cd = cap_cua_nhan(doan[dau_tien[vt_nhan]])
            assert cn is not None and cd is not None  # đã lọc theo LOAI_TIEU_DE
            cap_nhan.append(cn)
            cap_doan.append(cd)

        return (
            cap_nhan,
            cap_doan,
            {
                "n_tieu_de_nhan": len(nhan),
                "n_tieu_de_doan": len(doan),
                "n_ghep_duoc": len(cap_nhan),
                "so_cap_trong_nhan": len(set(cap_nhan)),
            },
        )

    def _na_rieng(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[NAReason, dict[str, object]] | None:
        assert isinstance(gt, AnnotationGT)
        nhan = self._tieu_de(gt.blocks)
        if len(nhan) < 2:
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "dưới 2 tiêu đề trong nhãn — không có quan hệ nào để so",
                "n_tieu_de_nhan": len(nhan),
            }
        if len({cap_cua_nhan(b) for b in nhan}) < 2:
            # Quyết định 3. Với DocLayNet đây là ca tài liệu chỉ có `Section-header`
            # mà không có `Title` — chiếm phần lớn bộ mẫu.
            return NAReason.NO_GROUND_TRUTH, {
                "ly_do": "nhãn chỉ có một cấp tiêu đề",
                "n_tieu_de_nhan": len(nhan),
            }

        cap_nhan, _, chi_tiet = self._ghep(gt, result)
        if len(cap_nhan) >= 2 and len(set(cap_nhan)) < 2:
            # Nhãn có 2 cấp, engine ghép trúng ≥2 tiêu đề, nhưng tất cả rơi vào
            # **cùng một** cấp nhãn. Mọi cặp đều là "=", nên engine gắn phẳng một
            # cấp cho tất cả sẽ được 1.0 — điểm đó không kiểm chứng được điều gì.
            # Chấm 0.0 cũng sai: engine không làm gì sai. Không chấm.
            return NAReason.NO_GROUND_TRUTH, {
                **chi_tiet,
                "ly_do": "phần ghép được của engine chỉ chạm một cấp nhãn",
            }
        return None

    def _compute(
        self, gt: GroundTruth, result: OcrResult
    ) -> tuple[float, dict[str, object]]:
        assert isinstance(gt, AnnotationGT)
        cap_nhan, cap_doan, chi_tiet = self._ghep(gt, result)
        if len(cap_nhan) < 2:
            # Nhãn ĐỦ điều kiện chấm (đã qua `_na_rieng`) mà engine không ghép nổi
            # 2 tiêu đề: đó là engine bỏ sót, không phải nhãn thiếu → 0.0, không N/A.
            # N/A ở đây sẽ **thưởng cho engine tìm được ít hơn** — nó biến mất khỏi
            # mẫu số thay vì đứng bét, đúng cái bẫy 1 của repo này.
            #
            # `n_cap = 0` phải có mặt, không được để trống: số 0.0 này là lỗi ĐỘ PHỦ
            # chứ không phải lỗi PHÂN CẤP, và nó có thật trong bảng (5/15 tài liệu
            # chấm được của opendataloader). Ai đọc bảng cũng phải tách được hai
            # nhóm mà không phải đoán — xem README bẫy 10.
            return 0.0, {
                **chi_tiet,
                "n_cap": 0,
                "ly_do": "engine không ghép được đủ 2 tiêu đề",
            }
        diem, them = dong_thuan_cap(cap_nhan, cap_doan)
        return diem, {**chi_tiet, **them}
