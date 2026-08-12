"""Ghép cặp hộp bao **tối ưu**, tất định — nền chung cho mọi metric có bbox.

## Vì sao không dùng tham lam

`imgf1.ghep_cap()` ghép tham lam theo IoU giảm dần, kèm một lập luận rằng ở
ngưỡng ≥ 0.5 phép ghép là **duy nhất** nên tham lam ra đúng kết quả tối ưu. Lập
luận đó đúng, nhưng nó có một tiền đề không được nói ra: **các box nhãn rời
nhau**. Với ảnh của DocLayNet thì gần đúng; với *block* thì sai hẳn — caption nằm
trong picture, ô nằm trong bảng, tiêu đề mục nằm trong khung mục. Nhãn lồng nhau
thì một box đoán có thể vượt 0.5 với **hai** box nhãn cùng lúc, và tham lam mất
cặp:

    nhãn a = (0.00,0.00)-(0.40,0.50)   diện tích 0.200
    nhãn b = (0.00,0.00)-(0.40,0.30)   nằm trong a, diện tích 0.120
    đoán p = (0.00,0.00)-(0.40,0.50)   IoU(a,p)=1.000  IoU(b,p)=0.600
    đoán q = (0.00,0.00)-(0.75,0.50)   IoU(a,q)=0.533  IoU(b,q)=0.320

    tham lam: lấy (a,p)=1.000 trước → q chỉ còn b, mà IoU(b,q)=0.32 < 0.5 → **1 cặp**
    tối ưu:   (b,p)=0.600 + (a,q)=0.533                                → **2 cặp**

Engine ở đây tìm ra **cả hai** block và khoanh đúng cả hai, nhưng tham lam chấm
nó recall 50%. Sai một chiều: tham lam chỉ có thể *hụt* cặp, không bao giờ thừa.

## Thứ tự ưu tiên: số cặp trước, độ khít sau

"Tối ưu" phải nói rõ tối ưu theo cái gì, vì hai mục tiêu này **xung đột**: một
cặp IoU 1.0 có tổng trọng số bằng hai cặp IoU 0.5. F1 đếm cặp, nên số cặp phải
thắng — bằng không metric sẽ chuộng một cặp khít hơn hai cặp đúng.

Cài bằng trọng số nguyên hai tầng: mỗi cạnh thật đáng `_CAN_NANG` (10¹⁵) cộng
phần IoU đã nhân `_TY_LE` (10⁹). Thêm một cạnh được lợi 10¹⁵, trong khi sắp xếp
lại toàn bộ phần IoU chỉ đổi tối đa `k × 10⁹` — số cặp thắng tuyệt đối với mọi
`k < 10⁶`, tức mọi tài liệu có thật. Nguyên chứ không thực: cộng dồn `float`
không kết hợp, nên hai thứ tự duyệt khác nhau có thể ra hai phép ghép khác nhau
trên cùng dữ liệu, và bench này phải tái lập được từng chữ số.

## Tất định khi hoà

Hoà điểm là chuyện thường (hai box bằng nhau tuyệt đối). Thuật toán Hungary bên
dưới luôn chọn **chỉ số cột nhỏ nhất** khi hoà, và `ghep_toi_uu()` chuyển vị theo
một quy tắc cố định chứ không theo thứ tự đầu vào, nên cùng đầu vào luôn cho cùng
đầu ra — kể cả `detail` đi vào bảng công bố.
"""

from __future__ import annotations

from collections.abc import Sequence

from ocr_bench.types import Box

__all__ = ["NGUONG_MAC_DINH", "ghep_toi_uu", "ghep_tham_lam"]

NGUONG_MAC_DINH = 0.5
"""Ngưỡng IoU coi hai box là "cùng một đối tượng"."""

_TY_LE = 10**9
"""Độ phân giải phần IoU khi quy về số nguyên (~1e-9, thừa cho mọi bbox)."""

_CAN_NANG = 10**15
"""Giá trị một cặp, đủ lớn để số cặp luôn thắng tổng IoU. Xem docstring module."""

_VO_CUC = 1 << 62


def _gan_toi_thieu(a: list[list[int]], n: int, m: int) -> list[int]:
    """Bài toán gán chi phí nhỏ nhất (Hungary có thế năng), `n <= m`.

    Trả `ans[i] = j` (cột được gán cho hàng `i`). Ma trận luôn đầy đủ nên mọi hàng
    đều được gán — cạnh "không tồn tại" được biểu diễn bằng chi phí 0, và chỗ gọi
    lọc chúng ra sau.

    Bản e-maxx quen thuộc, giữ nguyên 1-index của nó: đổi sang 0-index thì `p[0]`
    (ô lính canh giữ hàng đang tăng luồng) va vào cột thật.
    """
    u = [0] * (n + 1)
    v = [0] * (m + 1)
    p = [0] * (m + 1)
    way = [0] * (m + 1)

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [_VO_CUC] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = _VO_CUC
            j1 = 0
            for j in range(1, m + 1):
                if used[j]:
                    continue
                cur = a[i0 - 1][j - 1] - u[i0] - v[j]
                if cur < minv[j]:
                    minv[j] = cur
                    way[j] = j0
                # `<` chứ không `<=`: hoà thì giữ `j` nhỏ hơn. Đây là toàn bộ
                # cơ chế tất định khi hai cặp cùng điểm.
                if minv[j] < delta:
                    delta = minv[j]
                    j1 = j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1

    ans = [-1] * n
    for j in range(1, m + 1):
        if p[j]:
            ans[p[j] - 1] = j - 1
    return ans


def ghep_toi_uu(
    nhan: Sequence[Box],
    doan: Sequence[Box],
    nguong: float = NGUONG_MAC_DINH,
) -> list[tuple[int, int, float]]:
    """Ghép 1-1 tối đa hoá **số cặp**, rồi tổng IoU. Trả `(i_nhãn, j_đoán, iou)`.

    Chỉ cạnh có `iou >= nguong` mới được ghép; kết quả sắp theo chỉ số nhãn để
    `detail` của metric ổn định giữa các lần chạy.
    """
    if not nhan or not doan:
        return []

    # Hungary đòi số hàng ≤ số cột. Quy tắc chuyển vị cố định (theo kích thước,
    # không theo vai trò) để cùng dữ liệu luôn đi cùng một nhánh.
    chuyen_vi = len(nhan) > len(doan)
    hang: Sequence[Box] = doan if chuyen_vi else nhan
    cot: Sequence[Box] = nhan if chuyen_vi else doan
    n, m = len(hang), len(cot)

    iou = [[0.0] * m for _ in range(n)]
    chi_phi = [[0] * m for _ in range(n)]
    for i, x in enumerate(hang):
        for j, y in enumerate(cot):
            v = x.iou(y)
            if v >= nguong and v > 0.0:
                iou[i][j] = v
                chi_phi[i][j] = -(_CAN_NANG + round(v * _TY_LE))

    gan = _gan_toi_thieu(chi_phi, n, m)

    ra: list[tuple[int, int, float]] = []
    for i, j in enumerate(gan):
        if j < 0 or chi_phi[i][j] == 0:
            continue
        ra.append((j, i, iou[i][j]) if chuyen_vi else (i, j, iou[i][j]))
    ra.sort()
    return ra


def ghep_tham_lam(
    nhan: Sequence[Box],
    doan: Sequence[Box],
    nguong: float = NGUONG_MAC_DINH,
) -> list[tuple[int, int, float]]:
    """Phép ghép tham lam **cũ**, giữ lại để đối chiếu chứ không để chấm điểm.

    Không metric nào đang dùng hàm này. Nó tồn tại vì câu hỏi "đổi sang tối ưu thì
    số cũ có đổi không" phải trả lời được bằng máy trên bộ mẫu đã commit, chứ
    không bằng lập luận.
    """
    cap: list[tuple[float, int, int]] = []
    for i, a in enumerate(nhan):
        for j, b in enumerate(doan):
            v = a.iou(b)
            if v >= nguong and v > 0.0:
                cap.append((v, i, j))
    cap.sort(key=lambda t: (-t[0], t[1], t[2]))

    da_nhan: set[int] = set()
    da_doan: set[int] = set()
    ra: list[tuple[int, int, float]] = []
    for v, i, j in cap:
        if i in da_nhan or j in da_doan:
            continue
        da_nhan.add(i)
        da_doan.add(j)
        ra.append((i, j, v))
    ra.sort()
    return ra
