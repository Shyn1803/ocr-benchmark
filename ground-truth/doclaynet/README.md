# Nhãn DocLayNet — hệ toạ độ và cách quy đổi

> AC-05 của TASK-074. Điểm này ở A0 §10 còn để ngỏ ("chưa kiểm chứng"); dưới đây là
> kết luận **đo trên chính 204 trang trong repo**, kèm lệnh chạy lại.

## Kết luận

| Câu hỏi | Trả lời |
|---|---|
| Khung toạ độ | **1025 × 1025** với mọi trang (`coco_width`/`coco_height`) |
| Gốc | trên-trái, **y hướng xuống** |
| Dạng bbox | `[x, y, w, h]` (COCO chuẩn) — **không** phải `[x0,y0,x1,y1]` |
| Quan hệ với trang thật | **kéo giãn riêng từng trục**: `x·1025/original_width`, `y·1025/original_height` |
| `cells[].bbox` (text cell) | **cùng một hệ** với nhãn bố cục |

Quy đổi về `Box` của bench: chia cho `coco_width`/`coco_height`, `y_axis="down"`,
`page=0` (mỗi PDF của DocLayNet là một trang). Đã cài ở
[`src/ocr_bench/corpus.py`](../../src/ocr_bench/corpus.py) — đừng viết lại chỗ khác.

## Cái bẫy: đừng chia cho kích thước trang thật

`metadata.original_width/height` (vd 612×792 điểm) **không** phải hệ của bbox. Chia
nhầm cho nó thì trên trang A4 dọc, toạ độ y bị thổi lên ~1.29 lần — box vẫn "trông
hợp lệ", `Box.__post_init__` vẫn cho qua sau khi clamp, và IoU tụt đều ở **mọi**
engine. Sai kiểu này không nổ ở đâu cả, chỉ làm cả bảng B3 thấp hơn sự thật.

Cũng **không** phải aspect-fit có viền đệm (kiểu thư viện thị giác hay làm: giữ tỉ lệ
rồi độn hai bên). Nếu là aspect-fit thì trên trang dọc 612×792, mọi toạ độ x phải
≤ `1025·612/792 ≈ 792`. Thực tế **192/203** trang không vuông có text cell vượt quá
ngưỡng đó → trang bị kéo giãn đầy khung theo cả hai trục, tỉ lệ khung hình **không**
được giữ.

Hệ quả: box của DocLayNet **méo** so với trang thật. Chỉ so được với box của engine
sau khi cả hai đã chuẩn hoá về [0,1] — đúng cái `Box` làm. Đừng bao giờ so số tuyệt đối.

## Bằng chứng

```bash
cd ocr-bench
.venv/Scripts/python.exe scripts/check_doclaynet_coords.py
```

| Kiểm | Kết quả | Nói lên điều gì |
|---|---|---|
| y trung bình `Page-header` vs `Page-footer` | **67.3** vs **944.5**; 0/154 header có y lớn hơn mọi footer | y tăng khi đi xuống → gốc trên-trái |
| tâm text cell nằm trong một hộp bố cục | **99.4%** (17.907/18.008) | hai nguồn dùng chung một hệ |
| … nếu giả sử y hướng lên (lật trục) | tụt còn **66.4%** | giả thuyết y-up bị bác |
| cell vượt ngưỡng aspect-fit | **192/203** trang không vuông | kéo giãn riêng trục, không độn viền |

## Giới hạn đã biết — `precedence` không dùng được

Kế hoạch trông đợi lấy **trần người** miễn phí từ phần DocLayNet được annotate 2–3
lần (trường `precedence`). Bản COCO công bố **không có** phần đó: `precedence == 0`
ở cả **80.863** ảnh của train/val/test và không `file_name` nào lặp lại — các lần
annotate trùng đã được gộp trước khi phát hành.

Vì vậy `AnnotationGT.human_ceiling` để **rỗng**. Hai đường đi tiếp, chọn ở B3:

1. điền tay từ số đồng thuận công bố trong **bài báo** DocLayNet (theo lớp, không
   theo trang — thô hơn, nhưng miễn phí);
2. tự annotate lại một mẫu nhỏ để có trần theo trang (tốn công).

Để rỗng thì metric vẫn chạy bình thường, chỉ là không có mốc "người cũng chỉ tới đây".

## Nguồn và giấy phép

DocLayNet — IBM Deep Search, **CDLA-Permissive-1.0** (cho phép dùng thương mại).
<https://developer.ibm.com/exchanges/data/all/doclaynet/>
Ghi công đầy đủ: [`LICENSE.md`](LICENSE.md). Lấy về bằng
[`scripts/fetch_doclaynet.py`](../../scripts/fetch_doclaynet.py) (204/81.472 trang,
phân tầng theo `doc_category`).
