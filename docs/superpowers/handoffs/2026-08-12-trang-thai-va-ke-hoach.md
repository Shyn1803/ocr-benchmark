# OCR Parser Benchmark — trạng thái & kế hoạch còn lại

**Ngày:** 2026-08-12
**Worktree:** `ocr-bench/.worktrees/ocr-parser-benchmark`
**Nhánh:** `feature/ocr-parser-benchmark-research`
**HEAD:** `6f81e8f`
**Kế hoạch gốc:** `docs/superpowers/plans/2026-08-11-ocr-parser-benchmark-implementation.md`

---

## 1. Mục tiêu tổng

Nâng `ocr-bench` thành một benchmark nghiên cứu tái lập được, so sánh **Docling,
OpenDataLoader, Marker, Sovereign** — mỗi engine 2 profile, tổng **8 profile** — xếp hạng
theo từng năng lực, và sinh một báo cáo khoa học tiếng Việt **hoàn toàn tất định** từ
artifact đã đóng băng.

Ràng buộc xuyên suốt: **không có LLM ở bất kỳ đâu trong đường đi của số liệu, bảng, biểu
đồ hay khuyến nghị.** LLM chỉ được biên tập câu chữ *sau khi* số đã đóng băng, và không
được đụng vào bảng/số/CI/p-value/luật khuyến nghị.

---

## 2. Đã xong

| Task | Nội dung | Commit |
|------|----------|--------|
| 1–5 | Nền: kiểu dữ liệu, registry, profile catalog, adapter Docling/OpenDataLoader/Marker, manifest nguồn dữ liệu | `59069b8` và trước |
| 6 | Adapter Sovereign + 5 vòng review bảo mật | `de90724` → `52afc41` → **`6f81e8f`** |
| 7 | Ghép cặp bbox tối ưu (Hungarian) cho `imgf1`/`layout` | `7ec2ddf` |
| 8 | Tầng metric theo năng lực: `diacritics`, `layout`, `robustness`, `table_cells`, `nid`, `perf` | `55ea1c7` |

### Task 6 — vòng 5 vừa đóng (`6f81e8f`)

Năm phát hiện của reviewer đều là **rò rỉ im lặng** hoặc **khai sai phần cứng**:

- **P1-a** — `config_fingerprint()` từng công bố `device: "cpu"` ngay cạnh
  `marker_runtime_device: "cuda:0"` trên mọi dòng tài liệu hỏng, vì
  `SanitizedPipelineError` là `RuntimeError` nên `run()` thoát *trước* cổng
  `_kiem_thiet_bi_song()`. Nay hạ cấp xuống `"unverified"` (hạ chứ không ném — hàm này
  chạy trong except handler của `execute()`).
- **P1-c + P2-b** — `_doc_env_be()` nuốt dòng nối vô hạn: một nháy lẻ trong `.env` làm
  mọi biến phía sau biến mất khỏi bộ thay-thế, tức bí mật của chúng **lọt ra artifact**,
  không một lỗi nào. Nay dừng ở dòng gán kế tiếp, cảnh báo ra stderr thay vì trả `{}`.
  Bỏ luôn phép nối O(n²) (đo được 37.58s trên 4000 dòng).
- **P2-a** — `raw_bytes` dùng lại kết quả tầng chấm điểm. Tầng đó cố ý *hẹp* để không ăn
  nhầm cụm từ tự nhiên; dùng lại nghĩa là bí mật có khoảng trắng đi thẳng vào
  `sovereign.json` trên đĩa. Nay quét riêng ở tầng chẩn đoán, đếm riêng.
- **P3-a** — `probe_failed` không được bật khi đầu dò ném. Nay bật, nhưng **chỉ khi
  package marker có mặt** — máy sạch không cài marker thì "không có" là câu trả lời trung
  thực, bật ở đó sẽ giết profile `sovereign_default` trên mọi máy.
- **P1-b/P3-b** — `_SECRET_ENV_NAMES` so khớp casefold; tập bỏ-qua-ngưỡng có sàn
  `_SAN_CHAC_TOI_THIEU = 3` đo trên chuỗi đã strip.

Kèm **4 test chết-khi-revert** mà reviewer chỉ ra là còn thiếu: `probe_failed is True`;
`raw_artifact_redactions`; hai tầng bịt kiểm **qua `run()`** thay vì gọi thẳng
`_sanitize_dem`; fingerprint trên đường pipeline-ném không mang `device: "cpu"`.

> Vòng 5 là **vòng cuối được phép** theo quy trình (trần 5 vòng). Nếu reviewer vẫn trả
> CHANGES REQUIRED thì **dừng và báo cáo**, không nới trần.

---

## 3. Trạng thái test

```
Full suite: 3 failed, 894 passed, 15 skipped, 3 warnings, 8 errors in 28.68s
tests/test_sovereign_adapter.py: 76 passed, 1 skipped
```

Đây **đúng baseline đã chấp nhận**. 3 failed + 8 errors đều thuộc `test_report.py` và
`test_discrimination.py` — chúng chờ Task 11 (bộ dựng báo cáo), là task **duy nhất** được
phép sửa chúng. `passed` 891→894 là 3 test mới của vòng 5.

**Không được tuyên bố "full suite xanh".** Mỗi task phải giữ baseline này hoặc tốt hơn.

---

## 4. Còn phải làm

### Task 9 — cổng thẩm định metric + phá hoại có mức độ
- Phá hoại 3 mức nghiêm trọng `0.1 / 0.3 / 0.6`, seed cố định.
- `scripts/qualify_metrics.py` thoát `0` / `2`.
- `configs/metric-registry.json` — chỉ metric hạng `main` được vào bảng xếp hạng.
- Điều kiện đạt (D-010): `sabotage` phải **thấp hơn chính engine nguồn của nó**, so ngặt.
  `noop` bị **loại** khỏi cổng vì nó là sàn theo cấu tạo.

### Task 10 — thống kê & xếp hạng
- `statistics.py`: bootstrap phân vị theo cặp, **10.000 lần lấy lại**, seed `20260811`.
- Wilcoxon signed-rank — delta toàn 0 thì trả `identical`, **không ném**.
- Hiệu chỉnh Holm-Bonferroni; matched-pairs rank-biserial làm cỡ hiệu ứng.
- `doc_ids_sha256` để chốt đúng bộ tài liệu đã dùng.
- `ranking.py`: nhóm năng lực A/B/C.

### Task 11 — bộ dựng báo cáo tiếng Việt (tất định)
- `research_report.py`, `research_charts.py`, `build_research_report.py`.
- Template bài báo + phụ lục.
- Trace ID dạng `<!-- trace: aggregate:text_ocr:marker_scan -->` để mọi con số truy được
  về artifact sinh ra nó.
- **Dựng hai lần phải giống nhau từng byte.**
- Đây là task được phép sửa 3 failed + 8 errors đang treo.

### Task 12 — hiệu chuẩn & đóng băng
- Nhật ký hiệu chuẩn/quyết định.
- Đóng băng profile, tăng `catalog_version`.
- Chạy thử trên bộ tài liệu chung + `validation-report.md`.

### Task 13 — công bố
- Lượt chạy công bố, kiểm thủ công (`audit/sample-plan.json`, `audit/findings.jsonl`).
- Checklist nghiệm thu, đóng băng, gắn thẻ `ocr-parser-benchmark-v1`.

---

## 5. Rủi ro đã biết, chưa xử lý

**Task 12–13 cần chạy engine thật trên nhiều venv và nhiều bộ dữ liệu — hàng giờ đến hàng
ngày thời gian máy.** Phần nào không thực sự chạy được thì **phải báo cáo thẳng**, không
được khai như đã chạy.

**Corpus dự đoán vẫn 100% `schema_version=2`** (`Counter({2: 7884})`), chưa migrate.
`scripts/migrate_predictions.py` đã có và đã sửa lỗi migrate theo lô, nhưng **chưa chạy vì
chưa được phê duyệt**. Không xoá/migrate corpus khi chưa có phê duyệt.

**Thư mục ảnh đi kèm dự đoán** (`<doc_id>.images/`) không được commit, nên
`load_prediction()` từ chối dự đoán của marker — điều kiện có sẵn của corpus, không phải
lỗi mới.

**Bộ dữ liệu thiếu giấy phép hoặc thiếu bản chép** phải xuất hiện dưới dạng *hạn chế* hoặc
`N/A`, **tuyệt đối không thay bằng nhãn giả**. `nid` hiện `N/A` trên toàn bộ mẫu vì
DocLayNet không có nhãn thứ tự đọc — đó là câu trả lời trung thực, không phải lỗ hổng.

---

## 6. Ràng buộc vận hành trên máy này

- Mọi lệnh Python: `PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ...` — thiếu biến
  này thì tiếng Việt chết với `UnicodeEncodeError: 'charmap' codec`.
- **`ruff` chưa cài** → không được tuyên bố đã qua cổng lint.
- pytest có `addopts = "-q --strict-markers"`; ở `-q` dòng tổng kết bị nuốt trên terminal
  này — đọc tổng số bằng `--tb=no` **không kèm** `-q`. Thêm `-p no:randomly` cho tất định.
- Extra còn thiếu: `jiwer`, `apted`, `psutil` (test RSS bị skip). `rapidfuzz`, `Pillow` đã có.
- Không dùng heredoc bash cho nội dung có dấu `\` — nó biến `\\n` thành xuống dòng thật.
- Không `git reset --hard` / `git checkout --` / `git clean` trên worktree này.
- Không sửa BE read-only, không tạo `.pyc`/cache trong đó.
- Không đưa token/secret vào config, fingerprint, manifest, raw, traceback, report hay
  lịch sử git.
