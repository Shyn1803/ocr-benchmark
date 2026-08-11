# Bàn giao thực thi OCR/Parser Benchmark

**Cập nhật:** 2026-08-11

**Mục đích:** giúp một agent mới tiếp tục công việc mà không phải dựng lại lịch sử quyết định

**Trạng thái tổng quát:** Task 1–5 đã hoàn tất và qua review; Task 6 đã có commit đầu tiên nhưng đang ở vòng sửa review, có thay đổi chưa commit; Task 7–13 chưa bắt đầu.

## 1. Điểm tiếp tục chính xác

### Repository và nhánh

- Repository chính: `D:\vnpt-projects\sovereign\ocr-bench`
- Worktree phải tiếp tục làm việc: `D:\vnpt-projects\sovereign\ocr-bench\.worktrees\ocr-parser-benchmark`
- Branch: `feature/ocr-parser-benchmark-research`
- Commit implementation Task 6 dùng làm review/fix base: `e1d99ce570057274979079967a272157534d4233`
- Merge base của luồng thực thi: `d1a6085`
- Commit tài liệu bàn giao có thể nằm sau base trên; khi review code Task 6, giới hạn diff vào các file Task 6 hoặc dùng `e1d99ce` làm base.
- Không làm tiếp trong checkout chính `D:\vnpt-projects\sovereign\ocr-bench`; checkout đó đang ở branch khác.

### Trạng thái working tree tại thời điểm bàn giao

Có đúng hai file Task 6 đang thay đổi nhưng chưa commit:

```text
 M src/ocr_bench/adapters/sovereign.py
 M tests/test_sovereign_adapter.py
```

Thống kê hiện tại:

```text
216 insertions, 48 deletions  src/ocr_bench/adapters/sovereign.py
144 insertions, 3 deletions   tests/test_sovereign_adapter.py
```

Đây là phần sửa review có chủ đích. **Không reset, checkout, clean hoặc ghi đè hai file này.** Trước khi sửa tiếp, phải đọc `git diff` và giữ nguyên các test đã thêm.

### Tài liệu nguồn có thẩm quyền

- Thiết kế nghiên cứu: `docs/superpowers/specs/2026-08-11-ocr-parser-benchmark-research-design.md`
- Kế hoạch implementation chi tiết: `docs/superpowers/plans/2026-08-11-ocr-parser-benchmark-implementation.md`
- Ledger thực thi: `.superpowers/sdd/2026-08-11-ocr-parser-benchmark-implementation/progress.md`
- Brief/report từng task: `.superpowers/sdd/2026-08-11-ocr-parser-benchmark-implementation/task-<n>-brief.md` và `task-<n>-report.md`
- File hiện tại là tài liệu tiếp tục công việc; nếu có khác biệt, ưu tiên design/plan rồi đến bằng chứng code và test mới nhất.

## 2. Mục tiêu nghiên cứu đã thống nhất

Benchmark so sánh bốn họ engine/parser cho luồng extract PDF phục vụ RAG:

1. Docling;
2. OpenDataLoader;
3. Marker;
4. Sovereign.

Mỗi họ có hai cấu hình công bố trước:

- `default`: cấu hình mặc định/ưu tiên PDF digital;
- `scan`: cấu hình tối ưu cho PDF scan.

Tổng cộng có tám profile. Kết quả cuối phải là một báo cáo khoa học nội bộ bằng tiếng Việt, dùng duy nhất dataset công khai để dễ tái lập, xếp hạng theo từng năng lực và đưa khuyến nghị theo tình huống. Không tạo một điểm tổng duy nhất che khuất trade-off giữa OCR, layout, bảng, reading order, robustness và hiệu năng.

### Quyết định về LLM

- Không cần URL hoặc secret token LLM để tạo báo cáo.
- Báo cáo, bảng, biểu đồ và recommendation được sinh tất định từ metric/statistics/rule.
- Không gọi LLM để chấm gold, sửa ground truth hoặc chọn winner.
- OpenDataLoader hybrid chỉ được dùng local service đã khóa provenance; không dùng endpoint bên ngoài.

## 3. Baseline test đã được user chấp nhận

Baseline ban đầu trong isolated worktree:

- Unit suite khi loại `tests/test_discrimination.py` và `tests/test_report.py`: PASS.
- Full suite: **3 failed, 8 errors**.

Nguyên nhân baseline lúc đầu:

- prediction image sidecars nằm trong đường dẫn git-ignore nên không có ở linked worktree;
- hai subprocess report tests bị Windows `cp1252` decode.

Sau Prediction schema v3, một số corpus tests dừng sớm hơn vì artifacts trên đĩa vẫn là schema v2. Việc không migrate khoảng 7.884 prediction artifacts là quyết định có chủ đích. Tổng full-suite vẫn là 3 failed, 8 errors.

Quy tắc cho agent tiếp theo:

- Không tuyên bố full suite xanh.
- Không coi baseline là quyền tạo thêm failure.
- Mỗi task phải giữ full suite ở đúng baseline hoặc tốt hơn.
- Không tự migrate hàng nghìn artifacts khi chưa có chỉ đạo mới.

## 4. Những phần đã hoàn tất

### Task 1 — Catalog profile và factory

**Trạng thái:** hoàn tất, review sạch.

Commits:

- `8322198` — define reproducible benchmark profiles;
- `f9fa927` — deep immutability/canonical fingerprint;
- `ff648c4` — hash toàn bộ identity và chống collision.

Đã có:

- `configs/profiles.json` chứa đúng tám profile:
  - `docling_default`, `docling_scan`;
  - `opendataloader_default`, `opendataloader_scan`;
  - `marker_default`, `marker_scan`;
  - `sovereign_default`, `sovereign_scan`.
- `EngineProfile` deep-frozen.
- SHA-256 tất định từ toàn bộ identity/config/environment.
- `registry.build_adapter(profile)` và compatibility với legacy registry.

Deferred minor: docstring của `EngineProfile.fingerprint` nói catalog validation cấm secret, nhưng chính Task 1 chưa cài validation đó. Task 2 đã bổ sung kiểm soát secret khi persist provenance; final review vẫn cần quyết định sửa docstring hay thêm catalog validator.

### Task 2 — Prediction schema v3 và provenance

**Trạng thái:** hoàn tất, review sạch.

Commits:

- `a4a5faf` — schema v3/provenance;
- `54663e8` — secure persistence và raw preflight;
- `ebed2d2` — hạn chế metadata dưới sensitive keys.

Đã có:

- `FailureKind` và failure taxonomy;
- `RawArtifact` canonical;
- `engine_family`, `profile` và hardware provenance;
- raw sidecar trong `<document>.raw/`;
- SHA verification, path traversal guard, duplicate/casefold collision guard;
- lỗi adapter/timeout được phân loại nhất quán;
- redaction error/traceback và recursive fingerprint rejection;
- validation preflight trước mọi filesystem side effect;
- migration v1/v2 → v3 có `--dry-run` và alias legacy.

Covering suite sau vòng sửa cuối đã ghi nhận 166 tests pass. Artifacts trên đĩa chưa migrate theo quyết định nêu ở phần baseline.

### Task 3 — Publication runner và preflight

**Trạng thái:** hoàn tất, review sạch sau ba vòng sửa.

Commits:

- `c3de27d` — guarded publication runner;
- `582d38f` — đóng các provenance gaps;
- `aa15519` — bắt buộc recorded publication provenance;
- `5e3a109` — verify adapter evidence trước publication.

Đã có:

- `scripts/run_research_predictions.py`;
- `src/ocr_bench/preflight.py`;
- hai mode `calibration` và `publication`;
- gate đủ profile trước khi build/execute adapter;
- dataset checksum hook, clean-tree gate và perf metadata fail-closed;
- cache identity gồm document ID, PDF SHA-256, profile fingerprint, adapter version và hardware;
- manifest-selected documents và canonical profile order;
- `ConfiguredAdapter` handshake trước khi ghi run manifest;
- mọi adapter/result/cache phải có chính xác:
  - `hardware`;
  - `device`;
  - `hardware_evidence_version=1` với kiểu integer, không nhận boolean;
- chống TOCTOU khi PDF thay đổi giữa validate/cache/execute;
- `datasets/calibration-manifest.json` provisional cho sample calibration.

Publication mode cần non-provisional `datasets/manifest.json`, sẽ được Task 7 sinh.

Rủi ro chưa giải quyết: runner thiết kế lane CPU/GPU toàn bộ profile, nhưng OpenDataLoader và Sovereign hiện chỉ chứng minh được CPU. Task sau phải biểu diễn GPU unsupported/N/A theo profile; tuyệt đối không giả mạo device evidence.

### Task 4 — Docling default/scan

**Trạng thái:** hoàn tất, review sạch.

Commits:

- `2b97982` — Docling profiles;
- `d64a39a` — giữ identity khi fail và validate table HTML.

Đã có:

- lazy import Docling;
- default: EasyOCR/table defaults;
- scan: full-page OCR `vi,en`, accurate TableFormer và cell matching;
- page number 1-based → 0-based;
- bbox chuyển top-left với page dimensions;
- raw `docling.json` và trace `docling-map.json`;
- CPU/CUDA evidence thật;
- malformed table HTML → `AdapterOutputError`;
- real smoke Docling 2.91.0 trên Python 3.12 với PDF hai trang: PASS.

Deferred minor: `requirements/engines-docling.txt` là freeze thật nhưng được tạo từ venv `[dev,docling]`, nên gồm package dev. Final review nên cân nhắc regenerate từ environment engine-only.

### Task 5 — Marker và OpenDataLoader

**Trạng thái:** hoàn tất, review sạch sau hai vòng sửa.

Commits:

- `378f377` — tách Marker/ODL profiles;
- `78f6d58` — bind ODL scan vào owned hybrid launcher;
- `d1bfb45` — freeze hybrid manifest identity.

Marker:

- default/scan tách riêng;
- OCR false/true đúng profile, `use_llm=false`;
- raw trace chỉ tham chiếu item thực sự emitted;
- CPU/CUDA evidence thật;
- converter/model load được tái sử dụng;
- real Marker suite: PASS.

OpenDataLoader:

- default dùng cluster/xycut;
- scan dùng hybrid `docling-fast`, mode `full`, fallback false;
- `scripts/run_odl_hybrid.py` chỉ bind loopback;
- child CPU được enforce qua `CUDA_VISIBLE_DEVICES=''`, không phát minh cờ `--device`;
- ownership chứng minh bằng PID/create_time/descendant/listener qua psutil;
- manifest canonical, fixed identity, chống valid live rebind;
- precedence manifest: CLI > environment > ignored shared default path;
- version gates có `packaging`, `psutil`, `pypdf`, `easyocr` và dependency map;
- cleanup hash-guarded;
- real ODL/JRE suite: PASS.

Chưa có full hybrid readiness smoke vì `.venv-odl` còn thiếu năm hybrid dependencies; `--check-only` exit 2 và liệt kê thiếu dependency là kết quả đúng. GPU ODL bị từ chối vì `/health` không chứng minh được device.

## 5. Task 6 đang dở — điểm cần tiếp tục đầu tiên

### Commit đã có

`e1d99ce` — `feat: make Sovereign profiles fail closed`

Commit này đã cài:

- `sovereign_default/default` và `sovereign_scan/scan`;
- default cấm Marker usable; scan yêu cầu Marker package/cache;
- tắt vision/API/remote keys và URLs;
- enforce CPU, reject GPU;
- raw `sovereign.json` sanitized;
- BE commit/dirty và profile SHA trong fingerprint;
- bounded discovery cho BE worktree;
- `scripts/preflight_sovereign.py`;
- real preflight default qua `.venv-sov`, scan qua `.venv-marker`;
- initial focused verification: 114 pass, 1 skip; full suite giữ baseline 3F/8E.

BE được đọc tại:

```text
D:\vnpt-projects\sovereign\adminPortal\back-end-admin-portal
```

Không được sửa BE này. Fingerprint hiện ghi trung thực `be_dirty=true`.

### Bốn finding từ review

1. **P1 secret leak:** exception từ pipeline có thể chứa nguyên seeded secret trong error/traceback; regex sanitizer chung không đủ cho opaque secret.
2. **P1 false CPU evidence:** nếu BE Marker module đã cache `_device_str`/`_model_refs` CUDA, adapter có thể khai CPU sai.
3. **P2 marker fingerprint:** package availability và model cache readiness bị gộp thành một tín hiệu.
4. **P2 read-only violation:** import BE có thể tạo `.pyc`; phải suppress bytecode writes trong toàn bộ import/dynamic pipeline call và restore trạng thái trong `finally`.

### Nội dung diff chưa commit hiện có

Diff đã triển khai phần lớn vòng sửa:

- `MarkerRuntimeState` tách:
  - `package_available`;
  - `model_cache_ready`;
  - `runtime_loaded`;
  - `runtime_device`;
- `_validate_marker_runtime()` reject CUDA, conflicting hoặc unverified loaded runtime;
- fingerprint có các trường riêng `marker_package_available`, `marker_model_cache_ready`, `marker_runtime_loaded`, `marker_runtime_device`;
- context tạm đặt `sys.dont_write_bytecode=True` và restore;
- `_sanitize_runtime_text()` redacts cả exact values đã capture trước khi clear environment;
- wrapper exception được thiết kế để không chain backend exception chứa secret;
- tests mới cho opaque env secret, preloaded CUDA, cache/package separation và bytecode behavior.

### Verification vừa chạy tại thời điểm bàn giao

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_sovereign_adapter.py tests/test_sovereign_preflight.py -q -ra
```

Kết quả: exit 0, 50 pass và 1 skip `needs_be`.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_profiles.py tests/test_registry_and_noop.py tests/test_research_predictions_cli.py -q
```

Kết quả: exit 0, 74 pass.

`git diff --check`: sạch.

Đây mới là focused verification. Chưa rerun real preflight trên cả `.venv-sov`/`.venv-marker`, chưa rerun full baseline sau diff, chưa self-review cuối, chưa cập nhật `task-6-report.md`, chưa commit và chưa re-review.

### Các bước chính xác để đóng Task 6

1. Đọc toàn bộ diff hiện có; không viết lại từ đầu.
2. Xác nhận context `dont_write_bytecode` bao phủ mọi đường import BE và pipeline invocation, đồng thời luôn restore global flag.
3. Xác nhận exact secret values không tồn tại trong:
   - `OcrResult.error`;
   - traceback;
   - raw artifacts;
   - config fingerprint;
   - preflight stdout/stderr.
4. Xác nhận CPU profile reject mọi cached CUDA/conflicting/unverified state trước khi trả hardware evidence.
5. Chạy focused tests nêu trên.
6. Chạy real preflight:

   ```powershell
   $env:SOVEREIGN_BE_PATH='D:\vnpt-projects\sovereign\adminPortal\back-end-admin-portal'
   D:\vnpt-projects\sovereign\ocr-bench\.venv-sov\Scripts\python.exe scripts\preflight_sovereign.py sovereign_default --hardware cpu
   D:\vnpt-projects\sovereign\ocr-bench\.venv-marker\Scripts\python.exe scripts\preflight_sovereign.py sovereign_scan --hardware cpu
   ```

   Nếu CLI hiện tại dùng `--profile`, kiểm tra `-h` và dùng đúng interface đã commit; không thay contract chỉ để khớp ví dụ.
7. Chạy full suite và xác nhận không vượt baseline 3F/8E.
8. Chạy `compileall` cho file Task 6 và `git diff --check`.
9. Bổ sung phần fix round vào `task-6-report.md` và ledger.
10. Commit chỉ các file Task 6, ví dụ:

    ```text
    fix: secure Sovereign runtime evidence
    ```

11. Tạo review package từ `e1d99ce` tới commit mới và yêu cầu reviewer kiểm lại bốn finding.
12. Chỉ đánh dấu Task 6 complete khi reviewer trả review sạch.

## 6. Phần chưa làm: Task 7–13

### Task 7 — Dataset manifest, license và checksum gate

**Mục tiêu:** tạo nguồn ground truth công khai, tái lập và có provenance cho từng tài liệu.

Files chính:

- `datasets/catalog.json`;
- `datasets/manifest.json` (generated, không sửa tay);
- `datasets/corrections.jsonl`;
- `src/ocr_bench/dataset_manifest.py`;
- `scripts/build_dataset_manifest.py`;
- tests dataset/corpus.

Yêu cầu:

- included trước: DocLayNet và olmOCR-bench đang có;
- UIT-DODV, PubTabNet, FinTabNet, OHR-Bench giữ candidate/excluded cho đến khi license/access được xác minh;
- mỗi document có source URL/version/license, PDF SHA-256, annotation SHA-256, language, document type, scan category và capability flags;
- correction overlay cần source snapshot SHA, evidence và tối thiểu hai reviewer;
- thiếu transcript tiếng Việt phải báo rõ N/A, không tự tạo gold;
- publication mode chỉ nhận manifest non-provisional đã verify.

Gate:

```powershell
.\.venv\Scripts\python.exe scripts\build_dataset_manifest.py --verify
.\.venv\Scripts\python.exe -m pytest tests/test_dataset_manifest.py tests/test_corpus.py -q
```

Điểm dừng: nếu không có đủ GT cho một capability, capability đó phải N/A; không suy diễn gold từ output của engine.

### Task 8 — Metric theo sáu tầng năng lực

**Mục tiêu:** chấm riêng text/OCR, layout, reading order, tables, scan robustness và performance.

Phải cài:

- layout bipartite matching IoU ≥ 0.5;
- Block F1 và Type macro-F1;
- table recall, TEDS/TEDS-Struct;
- Cell F1 với rowspan/colspan và normalized content;
- Cell CER/lỗi dấu chỉ khi có transcript độc lập;
- NID chỉ khi có order labels thật;
- paired scan degradation trên cùng base document;
- performance: cold start, warm seconds/page, p95, RSS và nullable VRAM;
- thay greedy many-to-one bằng maximum-weight bipartite matching tất định;
- metric legacy phải versioned nếu giữ để so lịch sử.

Thiếu GT phải trả `NO_GROUND_TRUTH`, không trả 0.

### Task 9 — Metric qualification và sabotage

**Mục tiêu:** chỉ cho metric đã chứng minh phân biệt được mức lỗi đi vào bảng main.

Phải có:

- sabotage deterministic với severity 0.1/0.3/0.6;
- delete characters, swap paragraphs, bbox jitter, remove spans/tables/blocks;
- kiểm tra perfect > partial > severe;
- `configs/metric-registry.json` ghi `main` hoặc `experimental` và lý do;
- output `results/metric-qualification.json`;
- CLI exit 2 khi metric main không đạt.

Điểm dừng: không chạy publication nếu metric main chưa qualified.

### Task 10 — Paired statistics và capability ranking

Phải có:

- macro average ở document level;
- paired bootstrap 10.000 resamples, seed cố định `20260811`;
- Wilcoxon signed-rank, xử lý all-zero là `identical`;
- Holm-Bonferroni trong từng metric family/capability;
- matched-pairs rank-biserial effect size;
- CI riêng conditional mean và end-to-end mean;
- `doc_ids_sha256` cho mọi common set;
- nhóm A/B/C theo significance + practical threshold + effect-size band;
- N/A tách riêng, không lexical tie-break mang ý nghĩa khoa học.

### Task 11 — Report khoa học tiếng Việt tất định

Phải sinh:

- `paper/paper-vi.md`;
- `paper/executive-summary.md`;
- raw/aggregate/statistical/recommendation JSON artifacts;
- sáu bảng năng lực;
- SVG capability ranking, accuracy-speed, scan degradation, failure distribution;
- trace ID cho mọi số trong paper.

Pipeline bắt buộc theo thứ tự data → aggregate → statistics → rules → tables/charts → prose template. Recommendation là rule-based, không gọi LLM. N/A hiển thị chữ, không biến thành cột 0. Hai lần build cùng frozen fixture phải byte-for-byte giống nhau ngoài trường đã khai là volatile.

PDF là artifact mong muốn; ưu tiên Pandoc và font tiếng Việt. Nếu thiếu Pandoc, Markdown vẫn bắt buộc và script phải trả hướng dẫn dependency thay vì gọi dịch vụ ngoài.

### Task 12 — Calibration và pilot common-set

Phải:

- chọn calibration set phân tầng trước khi xem result, seed `20260811`;
- chỉ tune trong không gian đã công bố: OCR on/off/force, `vi,en`, table default/accurate, DPI ≤ 300 khi engine hỗ trợ;
- không tune tùy ý trên test set;
- ghi toàn bộ candidate, metric target, runtime và quyết định;
- tăng `catalog_version`, khóa SHA và commit profile trước publication;
- pilot 10 tài liệu chung cho tám profile;
- audit raw-to-canonical trace, coordinate overlay, coverage, failure taxonomy, metric qualification và ước tính time/RAM/disk.

Điểm dừng: nếu trace/coordinate sai hoặc chi phí vượt trần thì không chạy full corpus.

### Task 13 — Publication run, audit và freeze

Phải:

- tạo audit sample plan trước khi đọc output;
- chạy từng family/profile vào cùng run ID với cache provenance;
- không commit token; không cần LLM secret;
- chạy qualification, score, statistics và deterministic report builder;
- phân loại finding: engine/adapter/ground_truth/metric/unknown;
- mọi GT correction cần hai reviewer và evidence;
- nếu sửa adapter/metric phải invalidate đúng downstream artifacts;
- final checklist gồm tám profile hoặc N/A có bằng chứng, common-set hashes, CI/n/coverage/fail, qualified metrics, trace resolution và PDF tiếng Việt đúng;
- commit generated research artifacts và tag `ocr-parser-benchmark-v1` chỉ sau acceptance review.

## 7. Thứ tự tiếp tục và dependency

```text
Đóng Task 6
    |
Task 7 --------------------+
Task 8 -> Task 9 -> Task 10 -> Task 11 -> Task 12 -> Task 13
```

Task 7 và Task 8 có thể được nghiên cứu độc lập sau khi Task 6 sạch, nhưng publication chỉ hội tụ khi cả dataset manifest, metrics, adapters và profile catalog đều khóa. Task 13 chỉ bắt đầu trên working tree sạch với catalog và dataset manifest đã commit.

## 8. Quy trình Subagent-Driven phải tiếp tục dùng

User đã chọn cách làm **Subagent-Driven**. Với mỗi task còn lại:

1. Đọc plan và tạo/cập nhật task brief.
2. Giao một worker sở hữu rõ file/scope; nhắc worker không revert thay đổi của agent khác.
3. Worker làm TDD: ghi RED đúng feature gap, sau đó GREEN tối thiểu.
4. Worker tự review, chạy focused/related/full baseline và ghi report.
5. Commit implementation riêng, worktree sạch.
6. Giao reviewer độc lập đối chiếu spec/acceptance và diff range.
7. Nếu có finding, gửi lại worker thành fix round; tối đa năm vòng trước khi báo blocker.
8. Chỉ cập nhật ledger “complete” khi reviewer sạch.
9. Không chạy song song các task cùng sửa chung schema/registry/report core nếu chưa chia ownership rõ.

Task 6 là ngoại lệ hiện tại vì worker đã bị dừng giữa fix round để viết bàn giao. Agent mới phải tiếp tục diff hiện có, không dispatch lại implementation từ đầu.

## 9. Environment và lệnh hữu ích

### Venv

- Core worktree tests:
  `D:\vnpt-projects\sovereign\ocr-bench\.worktrees\ocr-parser-benchmark\.venv`
- Marker/Sovereign scan:
  `D:\vnpt-projects\sovereign\ocr-bench\.venv-marker`
- OpenDataLoader:
  `D:\vnpt-projects\sovereign\ocr-bench\.venv-odl`
- Sovereign default:
  `D:\vnpt-projects\sovereign\ocr-bench\.venv-sov`
- Docling smoke từng dùng temp Python 3.12 venv `%TEMP%\ocr-bench-docling-venv-py312`; phải kiểm tra còn tồn tại trước khi dựa vào nó.

### Khởi động phiên tiếp theo

```powershell
Set-Location D:\vnpt-projects\sovereign\ocr-bench\.worktrees\ocr-parser-benchmark
git branch --show-current
git status --short
git diff --check
git diff -- src/ocr_bench/adapters/sovereign.py tests/test_sovereign_adapter.py
Get-Content docs\superpowers\handoffs\2026-08-11-ocr-parser-benchmark-execution-handoff.md -Encoding utf8
Get-Content .superpowers\sdd\2026-08-11-ocr-parser-benchmark-implementation\progress.md -Encoding utf8
```

### Verification tối thiểu mỗi vòng

```powershell
.\.venv\Scripts\python.exe -m pytest <focused tests> -q
.\.venv\Scripts\python.exe -m pytest <related tests> -q
.\.venv\Scripts\python.exe -m pytest -q
git diff --check
git status --short
```

Khi full suite chạy, ghi rõ số 3F/8E baseline và phân biệt failure mới. Không che output hoặc sửa test để làm mất baseline.

## 10. Rủi ro và điều cấm

- Không đưa token/API secret vào config, fingerprint, manifest, raw, traceback, report hoặc git history.
- Không dùng LLM output làm ground truth.
- Không tự tải/include dataset khi license hoặc source version chưa được xác minh.
- Không sửa generated manifest/table/paper bằng tay; sửa nguồn hoặc builder rồi regenerate.
- Không biến missing GT thành điểm 0.
- Không gộp unsupported GPU thành failure chất lượng; biểu diễn N/A/unsupported có bằng chứng.
- Không khai CPU/GPU nếu adapter không có handshake chứng minh device.
- Không sửa read-only Sovereign BE hoặc tạo `.pyc`/cache trong đó.
- Không làm mất raw-to-canonical trace.
- Không thay metric semantics dưới cùng một metric name/version.
- Không xóa/migrate prediction corpus hiện có khi chưa được phê duyệt.
- Không dùng `git reset --hard`, `git checkout --` hoặc `git clean` trên worktree đang có Task 6 diff.

## 11. Definition of done toàn nghiên cứu

Nghiên cứu chỉ hoàn tất khi:

- tám profile đã khóa, hoặc profile/hardware unsupported được ghi N/A có bằng chứng;
- dataset công khai có manifest, license, version và checksums tái lập;
- metric main qua qualification;
- pairwise comparison dùng common set và có hash;
- bảng có CI, n, coverage và fail rate;
- ranking theo từng capability, không có điểm tổng gây hiểu nhầm;
- recommendation ghi evidence, trade-off, dataset scope và limitation;
- mọi số trong paper resolve được về raw/aggregate/statistics artifact;
- manual audit hoàn tất và correction có hai reviewer;
- Markdown report tất định; PDF tiếng Việt render đúng nếu toolchain có sẵn;
- no-secret scan sạch;
- full suite không có regression ngoài baseline đã công bố;
- final branch review sạch trước khi merge/tag.

## 12. Tóm tắt một câu cho agent nhận việc

Tiếp tục ngay từ **Task 6 review fix đang có trong hai file dirty**, verify và commit/re-review bốn finding; sau đó thực hiện tuần tự **Task 7 dataset → Task 8 metrics → Task 9 qualification → Task 10 statistics → Task 11 report builder → Task 12 calibration/pilot → Task 13 publication/audit**, giữ nguyên nguyên tắc public-only, deterministic, no-LLM và fail-closed provenance.
