# Handoff — ocr-parser-benchmark, 2026-08-12

Thay cho bản `2026-08-11-*-execution-handoff.md`. Đọc file này trước, bản cũ chỉ còn giá
trị lịch sử.

- **Plan gốc:** `docs/superpowers/plans/2026-08-11-ocr-parser-benchmark-implementation.md`
- **Worktree:** `ocr-bench/.worktrees/ocr-parser-benchmark`
- **Commit gần nhất:** `52afc41` — Task 6 vòng sửa 4
- **Ledger:** `.superpowers/sdd/2026-08-11-ocr-parser-benchmark-implementation/progress.md`
  (gitignored — không có trong commit, đọc trực tiếp trên đĩa)

---

## 0. Ba điều phải biết trước khi gõ lệnh đầu tiên

1. **Mọi lệnh Python đều cần `PYTHONIOENCODING=utf-8`.** Toàn bộ docstring và thông điệp
   lỗi là tiếng Việt; thiếu biến này thì Windows dùng cp1252 và chết bằng
   `UnicodeEncodeError: 'charmap' codec`. Trình thông dịch của worktree là
   `./.venv/Scripts/python.exe` — `python`/`python3` trên máy này là Store stub hỏng.
2. **`ruff` không có trong venv.** Đừng khai "lint pass".
3. **Suite không xanh, và không được nói là xanh.** Mốc đã chấp nhận:

   ```
   3 failed, 753 passed, 17 skipped, 3 warnings, 8 errors
   ```

   Ba fail là `test_report.py::test_file_ghi_ra_khong_co_crlf`,
   `test_report.py::test_chay_hai_lan_cho_raw_json_giong_het`,
   `test_discrimination.py::test_moi_file_du_doan_tren_dia_deu_duoc_nap`; 8 error đều ở
   `test_discrimination.py` (thiếu corpus). Chúng có **trước** loạt việc này và thuộc
   phạm vi Task 11. Mỗi task phải giữ mốc này hoặc tốt hơn; đừng "sửa" chúng ngoài Task 11.

   ```bash
   cd ocr-bench/.worktrees/ocr-parser-benchmark && PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe -m pytest --tb=no
   ```

   (Dùng `--tb=no` không `-q`: ở `-q` dòng đếm cuối bị nuốt trên terminal này.)

## 1. Ràng buộc không được vi phạm (nguyên văn, còn hiệu lực)

- Không đưa token/API secret vào config, fingerprint, manifest, raw, traceback, report
  hoặc git history.
- Không sửa Sovereign BE (read-only) hoặc tạo `.pyc`/cache trong đó. Gốc BE:
  `D:\vnpt-projects\sovereign\adminPortal\back-end-admin-portal`.
- Không dùng `git reset --hard`, `git checkout --`, `git clean` trên worktree này.
- Không khai CPU/GPU nếu adapter không có handshake chứng minh thiết bị.
- Không dùng LLM output làm ground truth. Không biến missing GT thành điểm 0. Không
  xoá/migrate prediction corpus hiện có khi chưa được phê duyệt.
- Dataset không có cổng license/transcript thì xuất hiện dưới dạng *limitation* hoặc
  `N/A`, không bao giờ thay bằng pseudo-gold (plan, nguyên tắc 4).
- LLM chỉ được biên tập **văn xuôi** sau khi số đã đóng băng; không đụng bảng, số, CI,
  p-value, quy tắc khuyến nghị (plan, nguyên tắc 7).
- Một phiên trước đây có lệnh chẩn đoán in ra giá trị secret thật của `.env` BE lên
  terminal. **Không in lại, không trích, không ghi vào bất kỳ artifact nào** — chỉ gọi
  tên biến.

## 2. Đã xong

### Task 6 — adapter Sovereign, vòng sửa 4 (commit `52afc41`)

Sửa hai phát hiện P1 của reviewer vòng 3, **ở gốc** chứ không ở test:

| Vấn đề | Gốc rễ | Cách sửa |
|---|---|---|
| Cổng thiết bị không chặn được gì | `_kiem_thiet_bi_song()` ném `ProfileEnvironmentError`, mà `execute()` bắt `Exception` → biến thành dòng `failed=True`, mà dòng ấy **vẫn mang `config_fingerprint`**, tức vẫn công bố `device: "cpu"` | Thêm `class KhaiSaiThietBi(BaseException)` để đi xuyên `execute()` |
| Bịt bí mật vừa thừa vừa thiếu | Thu thập và *dùng* bị gộp làm một; lọc lúc thu thập làm chuỗi biến mất khỏi cả traceback | Ba tầng: kho giữ tất → chẩn đoán lọc theo độ dài (`floor=6`) → văn bản chấm điểm lọc theo độ dài (12) **và** hình dạng (`loc_hinh_dang=True`) → `_SECRET_VALUES_CHAC` (4 tên khai cứng) vượt mọi bộ lọc |

Kèm theo:

- `MarkerRuntimeState.probe_failed` + cổng thứ ba trong `_validate_marker_runtime()`:
  đầu dò ném không còn lẫn với "máy sạch chưa nạp Marker".
- `marker_runtime_live()` trả `(True, "unknown")` (`THIET_BI_KHONG_RO`) cho **cả hai**
  nhánh mù: except, và "runtime đã nạp mà không ref nào khai thiết bị". Cổng bỏ qua
  `None` nhưng chặn `unknown` — đó là toàn bộ khác biệt.
- `_quet_gia_tri_env()`: đọc `.env` nhiều dòng, `\n` thoát, `"a""b"` nối chuỗi, chú thích
  cuối dòng chỉ khi ngoài nháy. Bịt hụt thân khoá PEM tệ hơn không bịt, vì vẫn báo một
  con số `redactions` khác 0.
- `_ENV_BE_CACHE` → `dict[Path, dict[str, str]]` khoá theo gốc BE đã resolve.
- `config_fingerprint` thêm `raw_artifact_redactions` bên cạnh `scored_text_redactions`.
- Fixture cô lập `_SECRET_VALUES` / `_SECRET_VALUES_CHAC` / `_ENV_BE_CACHE` chuyển từ
  `test_sovereign_adapter.py` sang `tests/conftest.py` — `test_sovereign_preflight.py`
  đụng đúng các biến toàn cục ấy trong cùng tiến trình.

Test mới: cổng `probe_failed`; parser `.env` nhiều dòng/thoát; tên khai cứng vượt mọi bộ
lọc; tên đoán-bằng-gợi-ý (`MAIL_PASSWORD`) bịt ở chẩn đoán nhưng **cố ý không** bịt ở văn
bản chấm điểm (đánh đổi có ghi rõ trong docstring). Cả hai file test Sovereign xanh
(77 passed, 1 skipped).

### Task 8 — mới làm một phần

`src/ocr_bench/metrics/matching.py` **đã viết xong** (chưa commit, chưa có test):
ghép cặp bbox tối ưu bằng Hungary có thế năng (e-maxx, O(n³), pure Python — repo không có
numpy/scipy). Trọng số nguyên hai tầng (`_CAN_NANG = 10¹⁵` cho mỗi cặp, `_TY_LE = 10⁹` cho
phần IoU) để **số cặp luôn thắng tổng IoU**; hoà thì chọn chỉ số cột nhỏ nhất → tất định.
`ghep_tham_lam()` giữ lại **chỉ để** trả lời bằng máy câu hỏi "đổi sang tối ưu thì số đã
công bố có đổi không". Docstring module mang phản ví dụ chứng minh tham lam hụt cặp khi
nhãn lồng nhau (caption trong picture, ô trong bảng).

## 3. Việc còn lại

### 3.1 Đóng Task 6

Vòng 4 đã commit nhưng **chưa gửi reviewer**. Còn 1 vòng sửa trong hạn mức 5.
Gói diff: `git diff <sha-vòng-3>..52afc41`. Nếu vòng 5 vẫn CHANGES REQUIRED thì phải
dừng và báo, không tự nới hạn mức.

### 3.2 Task 8 — lớp metric theo năng lực

Tạo mới: `metrics/layout.py`, `metrics/table_cells.py`, `metrics/diacritics.py`,
`metrics/robustness.py`. Sửa: `metrics/imgf1.py`, `metrics/nid.py`, `metrics/perf.py`,
`src/ocr_bench/__init__.py`, `types.py`.
Test: `test_layout_metric.py`, `test_table_cells_metric.py`, `test_diacritics_metric.py`,
`test_robustness.py`; sửa `test_imgf1_metric.py`, `test_nid_metric.py`, `test_perf.py`.
Commit: `feat: add capability-layer benchmark metrics`.

Quy trình bắt buộc theo plan: **Step 1 viết test đỏ trước**, Step 2 chạy cho thấy nó đỏ,
rồi mới cài. Hai hình dạng test plan viết thẳng ra:

```python
@pytest.mark.parametrize("metric", [BlockF1Metric(), TypeF1Metric(), CellF1Metric()])
def test_metric_controls_are_ordered(metric, gt, perfect, partial, severe):
    scores = [metric.score(gt, x).value for x in (perfect, partial, severe)]
    assert scores[0] == 1.0
    assert scores[0] > scores[1] > scores[2]
```

```python
def test_scan_degradation_uses_paired_documents_only():
    got = relative_degradation(digital, severe)
    assert got.n_pairs == 2
    assert got.excluded_doc_ids == ("only-in-digital",)
```

Thiết kế đã chốt từ khảo sát trước (giữ nguyên):

- **TypeF1** đếm block nhãn không ghép được là FN, block đoán thừa là FP; macro-average
  **chỉ trên những type có mặt trong GT**.
- **Table**: không có capability `TABLE_BBOX`. GT thiếu box → `NO_GROUND_TRUTH`; đoán
  thiếu box → `MISSING_CAPABILITY`, qua `_na_rieng`. Hai trạng thái khác nhau, đừng gộp.
- **Dấu tiếng Việt**: căn trên chuỗi NFD đã bỏ dấu (`đ`/`Đ` → `d`/`D`), dùng
  `rapidfuzz.distance.Indel.opcodes`; mẫu số là số ký tự GT **có mang dấu**.
- **Robustness**: `relative_degradation(digital, scan) -> Degradation`, ghép cặp bằng
  `base_doc_id()`, ở mức tổng hợp chứ không mức tài liệu; `n_pairs == 0` →
  `kha_dung=False`, không phải điểm 0.
- **Cold start**: `PerfRow` cần thêm `thu_tu: int` (thứ tự đầu vào) vì `perf_rows()` sắp
  theo `(engine, doc_id)` nên thông tin "tài liệu nào chạy đầu tiên" đã mất.
- `OcrResult` thêm `peak_vram_mb: float | None = None` (thêm trường, không đổi trường cũ).

⚠️ Hai file nằm **ngoài** danh sách Task 8 của plan và phải ghi rõ trong task report:
`metrics/matching.py` (đã viết) và `types.py` (thêm trường VRAM).

### 3.3 Task 9 — cổng đủ tư cách của metric

Sabotage có mức độ (0.1 / 0.3 / 0.6, seed cố định). `scripts/qualify_metrics.py` thoát
0 hoặc 2. `configs/metric-registry.json`. Chỉ metric `main` được vào bảng xếp hạng.

### 3.4 Task 10 — thống kê + xếp hạng

`statistics.py` + `ranking.py`: bootstrap phân vị theo cặp (10.000 lần lấy lại, seed
`20260811`), Wilcoxon signed-rank (delta toàn 0 → trả `identical`, **không** ném),
Holm-Bonferroni, rank-biserial cho cặp khớp, `doc_ids_sha256`, nhóm năng lực A/B/C.

### 3.5 Task 11 — báo cáo khoa học tiếng Việt, tất định

`research_report.py`, `research_charts.py`, `build_research_report.py`, template bài báo
+ phụ lục. Trace ID dạng `<!-- trace: aggregate:text_ocr:marker_scan -->`. Dựng hai lần
phải ra file **giống nhau từng byte**. Ba fail baseline nằm ở đây — đây là task được phép
sửa chúng.

### 3.6 Task 12 — hiệu chuẩn + đóng băng profile

Nhật ký hiệu chuẩn/quyết định, đóng băng profile với `catalog_version` tăng, chạy thử
common-set + `validation-report.md`.

### 3.7 Task 13 — chạy công bố

Chạy thật, kiểm thủ công (`audit/sample-plan.json`, `audit/findings.jsonl`), checklist
nghiệm thu, đóng băng, tag `ocr-parser-benchmark-v1`.

> **Task 12–13 cần engine chạy thật trên nhiều venv và nhiều dataset — hàng giờ đến hàng
> ngày máy.** Phần nào không chạy được thì báo thẳng là chưa chạy, không suy ra số.

## 4. Quy trình (SDD)

Mỗi task: brief → worker → tự soát → reviewer độc lập → vòng sửa (tối đa 5) → commit.
Artifact đặt ở `.superpowers/sdd/<plan>/`: `task-N-brief.md`, `task-N-report.md`,
`review-<from>..<to>.diff`, và `progress.md` ghi thêm chỉ-nối-đuôi.
