# OCR/Parser Benchmark Research Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Nâng `ocr-bench` thành một benchmark nghiên cứu tái lập, so sánh Docling, OpenDataLoader, Marker và Sovereign theo hai profile `default`/`scan`, xếp hạng riêng từng năng lực và sinh báo cáo khoa học tiếng Việt hoàn toàn từ artifact đã đóng băng.

**Architecture:** Giữ ranh giới hiện tại `adapter -> canonical prediction -> metric -> aggregate/report`. Bổ sung profile như danh tính engine độc lập, prediction schema v3 có provenance/raw artifact/failure taxonomy, manifest dataset theo từng tài liệu, metric theo tầng năng lực, paired statistics trên common set, và một publication builder tất định. Không dùng LLM trong đường sinh số, bảng, biểu đồ hay khuyến nghị; Markdown/PDF là hàm thuần của config + manifest + prediction + metric result.

**Tech Stack:** Python 3.11+, pytest, dataclasses/JSON, Docling, OpenDataLoader PDF hybrid, Marker, scipy (Wilcoxon), stdlib SVG, Pandoc hoặc WeasyPrint chỉ ở bước xuất PDF.

---

## Nguyên tắc thực thi

1. Mỗi task làm theo red-green-refactor: thêm test thất bại, chạy đúng test để thấy đỏ, viết thay đổi nhỏ nhất, chạy lại, rồi commit.
2. Không chạy lại engine khi chỉ sửa metric/report. Prediction và raw artifact là ranh giới đóng băng.
3. Không đưa một dataset vào bảng chính trước khi nguồn, version, license và checksum đều qua validation.
4. DocLayNet và olmOCR-bench là scope dữ liệu công bố đầu tiên vì repo đã có fetcher, annotation và checksum. Dataset tiếng Việt chưa qua license/transcript gate phải hiện là limitation hoặc `N/A`, không được thay bằng pseudo-gold.
5. Mỗi profile là một engine độc lập: `docling_default`, `docling_scan`, `opendataloader_default`, `opendataloader_scan`, `marker_default`, `marker_scan`, `sovereign_default`, `sovereign_scan`.
6. Không có overall score. Hạng chỉ tồn tại theo năng lực và chỉ trên common set.
7. LLM, nếu sau này dùng để biên tập văn phong, chỉ được đọc bản nháp sau khi số liệu đã đóng băng; nội dung LLM không được ghi đè bảng, số, CI, p-value hay recommendation rule.

## Definition of done toàn chương trình

- Tám profile có prediction hoặc có bản ghi `unsupported`/`environment_error` giải thích được.
- `datasets/manifest.json` truy được từng `doc_id` tới URL công khai, license, SHA-256 PDF và SHA-256 annotation.
- Mỗi prediction schema v3 truy được tới profile config và raw artifact.
- Mọi metric trong bảng chính qua positive, intermediate, negative, property và monotonic sabotage controls.
- Mọi so sánh trực tiếp dùng common `doc_id`, paired bootstrap 10.000 mẫu, Wilcoxon, Holm correction và effect size.
- Các bảng có mean, CI 95%, `n`, coverage và fail rate; N/A không bị đổi thành 0.
- `paper/paper-vi.md`, executive summary, bảng, SVG, raw/aggregate/statistical JSON được sinh lại bằng một lệnh từ artifact đóng băng.
- Test suite xanh, `git diff --check` xanh, publication build hai lần cho output byte-identical trừ manifest thời gian chạy được định danh rõ.

## Task 1: Khóa catalog profile và preflight cấu hình

**Files:**

- Create: `configs/profiles.json`
- Create: `src/ocr_bench/profiles.py`
- Modify: `src/ocr_bench/registry.py`
- Modify: `src/ocr_bench/__init__.py`
- Test: `tests/test_profiles.py`
- Test: `tests/test_registry_and_noop.py`

**Step 1: Viết test đỏ cho catalog profile**

```python
def test_publication_profiles_are_exact_and_unique():
    catalog = load_profile_catalog(ROOT / "configs" / "profiles.json")
    assert set(catalog) == {
        "docling_default", "docling_scan",
        "opendataloader_default", "opendataloader_scan",
        "marker_default", "marker_scan",
        "sovereign_default", "sovereign_scan",
    }
    assert all(p.family in {"docling", "opendataloader", "marker", "sovereign"}
               for p in catalog.values())
    assert all(p.profile in {"default", "scan"} for p in catalog.values())
```

**Step 2: Chạy test và xác nhận đỏ**

Run: `py -3 -m pytest tests/test_profiles.py -q`

Expected: FAIL vì chưa có `ocr_bench.profiles`.

**Step 3: Cài đặt model và validation tối thiểu**

```python
@dataclass(frozen=True, slots=True)
class EngineProfile:
    name: str
    family: str
    profile: Literal["default", "scan"]
    adapter: str
    config: dict[str, object]
    environment: dict[str, object]

def load_profile_catalog(path: Path) -> dict[str, EngineProfile]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    profiles = {row["name"]: EngineProfile(**row) for row in raw["profiles"]}
    if len(profiles) != len(raw["profiles"]):
        raise ProfileConfigError("trùng tên profile")
    return profiles
```

`configs/profiles.json` phải khóa các quyết định sau:

- Docling default: OCR tự động, EasyOCR, table mode mặc định.
- Docling scan: force full-page OCR, EasyOCR `vi,en`, table mode accurate, cell matching bật.
- OpenDataLoader default: Java parser, `table_method=cluster`, `reading_order=xycut`.
- OpenDataLoader scan: `hybrid=docling-fast`, `hybrid_mode=full`, server local force OCR với EasyOCR `vi,en`, không fallback im lặng.
- Marker default: `force_ocr=false`, `use_llm=false`.
- Marker scan: `force_ocr=true`, `use_llm=false`.
- Sovereign default: môi trường không có Marker escalation; API/vision bị cưỡng bức tắt.
- Sovereign scan: môi trường có Marker local; API/vision vẫn bị cưỡng bức tắt.

Mọi giá trị thay đổi sau calibration phải tạo commit mới; không cho phép CLI override trong publication run.

**Step 4: Thêm factory profile-aware vào registry**

```python
def build_adapter(profile: EngineProfile) -> Adapter:
    cls = get_adapter(profile.adapter)
    adapter = cls.from_profile(profile)
    if adapter.name != profile.name:
        raise ProfileConfigError(
            f"adapter trả name={adapter.name!r}, cần {profile.name!r}"
        )
    return adapter
```

Giữ `get_adapter()` để không phá test/CLI cũ; publication CLI chỉ dùng `build_adapter()`.

**Step 5: Chạy test**

Run: `py -3 -m pytest tests/test_profiles.py tests/test_registry_and_noop.py -q`

Expected: PASS.

**Step 6: Commit**

```bash
git add configs/profiles.json src/ocr_bench/profiles.py src/ocr_bench/registry.py src/ocr_bench/__init__.py tests/test_profiles.py tests/test_registry_and_noop.py
git commit -m "feat: define reproducible benchmark profiles"
```

## Task 2: Prediction schema v3, provenance, raw artifact và failure taxonomy

**Files:**

- Modify: `src/ocr_bench/types.py`
- Modify: `src/ocr_bench/adapters/base.py`
- Modify: `src/ocr_bench/prediction.py`
- Modify: `scripts/migrate_predictions.py`
- Test: `tests/test_types.py`
- Test: `tests/test_prediction.py`
- Test: `tests/test_sabotage_and_scorer.py`

**Step 1: Viết test đỏ cho identity và raw artifact**

```python
def test_schema_v3_round_trip_keeps_profile_and_raw_artifact(tmp_path):
    result = OcrResult(
        engine="marker_scan",
        engine_family="marker",
        profile="scan",
        engine_version="1.10.2",
        doc_id="x",
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md="xin chào",
        raw_artifacts=(RawArtifact("marker.json", "application/json", b"{}"),),
        config_fingerprint={"force_ocr": True},
    )
    path = save_prediction(result, tmp_path)
    got = load_prediction(path)
    assert got == result
    assert (tmp_path / "marker_scan" / "x.raw" / "marker.json").read_bytes() == b"{}"
```

```python
def test_failed_result_requires_failure_kind():
    with pytest.raises(ValueError, match="failure_kind"):
        OcrResult(
            engine="marker_scan",
            engine_family="marker",
            profile="scan",
            engine_version="1.10.2",
            doc_id="x",
            capabilities=frozenset(),
            failed=True,
            error="boom",
        )
```

**Step 2: Chạy test và xác nhận đỏ**

Run: `py -3 -m pytest tests/test_types.py tests/test_prediction.py -q`

Expected: FAIL vì chưa có field/type mới.

**Step 3: Mở rộng canonical types**

```python
class FailureKind(str, enum.Enum):
    UNSUPPORTED = "unsupported"
    ENVIRONMENT_ERROR = "environment_error"
    TIMEOUT = "timeout"
    OOM = "oom"
    ENGINE_ERROR = "engine_error"
    ADAPTER_ERROR = "adapter_error"

@dataclass(frozen=True, slots=True)
class RawArtifact:
    name: str
    media_type: str
    data: bytes

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()
```

Thêm vào `OcrResult`: `engine_family`, `profile`, `raw_artifacts`, `failure_kind`. `failed=True` bắt buộc có `failure_kind`; `failed=False` cấm có `failure_kind`.

**Step 4: Nâng prediction schema**

- Đặt `SCHEMA_VERSION = 3`.
- JSON chỉ lưu metadata raw artifact (`name`, `media_type`, `file`, `sha256`); bytes nằm trong `<doc_id>.raw/`.
- Chặn path traversal và kiểm SHA-256 giống image sidecar.
- Migration v2 -> v3 gán `engine_family=engine`, `profile=legacy`, `raw_artifacts=[]`; prediction lỗi cũ gán `failure_kind=engine_error` và ghi cảnh báo migration.
- Không import adapter từ `prediction.py`.

**Step 5: Phân loại exception tại biên adapter**

```python
def classify_exception(exc: BaseException) -> FailureKind:
    if isinstance(exc, TimeoutError):
        return FailureKind.TIMEOUT
    if isinstance(exc, MemoryError):
        return FailureKind.OOM
    if isinstance(exc, (ImportError, FileNotFoundError)):
        return FailureKind.ENVIRONMENT_ERROR
    return FailureKind.ENGINE_ERROR
```

Adapter phát hiện lỗi normalize/raw mapping phải chủ động ném `AdapterOutputError`; lớp bọc ánh xạ nó thành `ADAPTER_ERROR`.

**Step 6: Chạy test và migration dry-run**

Run: `py -3 -m pytest tests/test_types.py tests/test_prediction.py tests/test_sabotage_and_scorer.py -q`

Run: `py -3 scripts/migrate_predictions.py prediction --dry-run`

Expected: test PASS; dry-run liệt kê v2 -> v3 nhưng không sửa file.

**Step 7: Commit**

```bash
git add src/ocr_bench/types.py src/ocr_bench/adapters/base.py src/ocr_bench/prediction.py scripts/migrate_predictions.py tests/test_types.py tests/test_prediction.py tests/test_sabotage_and_scorer.py
git commit -m "feat: add provenance to prediction schema v3"
```

## Task 3: Publication CLI và preflight không cho chạy lệch profile

**Files:**

- Create: `scripts/run_research_predictions.py`
- Create: `src/ocr_bench/preflight.py`
- Modify: `scripts/make_predictions.py`
- Test: `tests/test_research_predictions_cli.py`
- Test: `tests/test_make_predictions_cli.py`

**Step 1: Viết test đỏ**

```python
def test_publication_cli_refuses_partial_profile_set(tmp_path):
    rc = main(["--profiles", "marker_default", "--out", str(tmp_path)])
    assert rc == 2

def test_preflight_fingerprint_must_match_locked_config():
    with pytest.raises(PreflightError, match="force_ocr"):
        verify_fingerprint(profile, {"force_ocr": False})
```

**Step 2: Chạy test đỏ**

Run: `py -3 -m pytest tests/test_research_predictions_cli.py -q`

**Step 3: Cài CLI hai chế độ**

- `--mode calibration`: cho phép một profile/tập nhỏ, ghi vào `calibration/`, không ghi `results/`.
- `--mode publication`: bắt buộc đủ profile được catalog bật, manifest dataset hợp lệ, working tree sạch, checksum đúng, không override config.
- `--hardware cpu|gpu`: là chiều thí nghiệm; output nằm `prediction/<hardware>/<profile>/...`.
- Ghi `run-manifest.json` gồm commit, Python, OS, CPU/GPU, RAM, dependency versions, profile config hash, dataset manifest hash.
- `scripts/make_predictions.py` được giữ cho developer smoke run và in cảnh báo “không dùng cho publication”.

**Step 4: Thêm resume an toàn**

Cache key phải gồm `doc_id + pdf_sha256 + profile_config_sha256 + engine_version + hardware`. Mismatch mặc định là lỗi trong publication, không tự dùng file cũ.

**Step 5: Chạy test**

Run: `py -3 -m pytest tests/test_research_predictions_cli.py tests/test_make_predictions_cli.py -q`

Expected: PASS.

**Step 6: Commit**

```bash
git add scripts/run_research_predictions.py src/ocr_bench/preflight.py scripts/make_predictions.py tests/test_research_predictions_cli.py tests/test_make_predictions_cli.py
git commit -m "feat: add guarded publication prediction runner"
```

## Task 4: Docling default và scan adapters

**Files:**

- Create: `src/ocr_bench/adapters/docling.py`
- Modify: `src/ocr_bench/__init__.py`
- Modify: `pyproject.toml`
- Create: `requirements/engines-docling.txt`
- Test: `tests/test_docling_adapter.py`

**Step 1: Viết unit test đỏ bằng fake DoclingDocument**

```python
def test_docling_build_result_maps_pages_boxes_tables_and_raw():
    result = build_result(fake_docling_document(), identity=SCAN_IDENTITY)
    assert result.engine == "docling_scan"
    assert result.blocks[0].box.page == 0
    assert result.tables[0].html.startswith("<table")
    assert result.raw_artifacts[0].name == "docling.json"
```

```python
def test_docling_scan_profile_forces_ocr_and_accurate_tables(monkeypatch):
    adapter = DoclingAdapter.from_profile(scan_profile())
    opts = adapter.pipeline_options()
    assert opts.do_ocr is True
    assert opts.ocr_options.force_full_page_ocr is True
    assert opts.ocr_options.lang == ["vi", "en"]
    assert opts.table_structure_options.mode.value == "accurate"
```

**Step 2: Chạy test đỏ**

Run: `py -3 -m pytest tests/test_docling_adapter.py -q`

**Step 3: Cài adapter với lazy imports**

- Pin extra `docling = ["docling[easyocr]==2.91.0"]`; sau khi cài, tạo `requirements/engines-docling.txt` bằng `pip freeze` từ venv chạy thật.
- Default dùng `PdfPipelineOptions(do_ocr=True)` và không ép full page.
- Scan dùng `EasyOcrOptions(lang=["vi", "en"], force_full_page_ocr=True)` và `TableFormerMode.ACCURATE` với cell matching.
- Chuẩn hóa page index về 0-based, box về top-left `[0,1]`; unit test phải có trang cao/rộng khác nhau để bắt đổi trục.
- Raw artifact là `document.export_to_dict()` đã JSON hóa tất định với `sort_keys=True`.
- Capability chỉ khai những field adapter thực sự điền.

**Step 4: Thêm real-engine smoke test có marker**

Test dùng `tests/fixtures/two_page_layout.pdf`, tự skip khi thiếu extra `docling`, và kiểm text không rỗng, page index, fingerprint, raw SHA.

**Step 5: Chạy test**

Run: `py -3 -m pytest tests/test_docling_adapter.py -q`

Expected: unit tests PASS; real-engine smoke PASS trong `.venv-docling`, skip có lý do trên máy trắng.

**Step 6: Commit**

```bash
git add src/ocr_bench/adapters/docling.py src/ocr_bench/__init__.py pyproject.toml requirements/engines-docling.txt tests/test_docling_adapter.py
git commit -m "feat: add Docling benchmark profiles"
```

## Task 5: Tách Marker và OpenDataLoader thành hai profile khóa cấu hình

**Files:**

- Modify: `src/ocr_bench/adapters/marker.py`
- Modify: `src/ocr_bench/adapters/opendataloader.py`
- Create: `scripts/run_odl_hybrid.py`
- Modify: `pyproject.toml`
- Test: `tests/test_marker_adapter.py`
- Test: `tests/test_opendataloader_adapter.py`
- Test: `tests/test_odl_hybrid.py`

**Step 1: Viết test đỏ cho mapping profile**

```python
@pytest.mark.parametrize(("name", "force"), [
    ("marker_default", False), ("marker_scan", True),
])
def test_marker_profile_controls_force_ocr(name, force):
    adapter = MarkerAdapter.from_profile(profile(name))
    assert adapter.name == name
    assert adapter.force_ocr is force
```

```python
def test_odl_scan_calls_hybrid_full_without_fallback(fake_convert):
    OpenDataLoaderAdapter.from_profile(profile("opendataloader_scan")).run(PDF)
    assert fake_convert.kwargs["hybrid"] == "docling-fast"
    assert fake_convert.kwargs["hybrid_mode"] == "full"
    assert fake_convert.kwargs["hybrid_fallback"] is False
```

**Step 2: Chạy test đỏ**

Run: `py -3 -m pytest tests/test_marker_adapter.py tests/test_opendataloader_adapter.py tests/test_odl_hybrid.py -q`

**Step 3: Cài factory và raw artifact**

- Instance `name` lấy từ `EngineProfile`, không dùng tên legacy trong publication.
- Marker lưu JSON block output làm `marker.json`; markdown vẫn vào `text_md`.
- ODL giữ nguyên JSON/Markdown của JAR làm raw artifacts trước khi normalize.
- Fingerprint thêm profile config hash, OCR model/language khi có, và dependency versions.

**Step 4: Cài local hybrid launcher có health check**

`scripts/run_odl_hybrid.py` gọi đúng binary trong venv:

```text
opendataloader-pdf-hybrid --host 127.0.0.1 --port 5002 \
  --force-ocr --ocr-engine easyocr --ocr-lang vi,en
```

Launcher phải:

- kiểm `127.0.0.1`, không tự bind public interface;
- poll health endpoint có timeout 120 giây;
- ghi server config/version vào `run-manifest.json`;
- dừng publication run nếu server config không khớp catalog;
- không bật `hybrid_fallback`, vì fallback sẽ làm cùng profile chứa hai pipeline khác nhau.

Pin extra `opendataloader-hybrid = ["opendataloader-pdf[hybrid]==2.5.0", "pypdf>=5"]`.

**Step 5: Chạy test và smoke**

Run: `py -3 -m pytest tests/test_marker_adapter.py tests/test_opendataloader_adapter.py tests/test_odl_hybrid.py -q`

Run: `.venv-odl\Scripts\python.exe scripts/run_odl_hybrid.py --check-only`

Expected: PASS; `--check-only` xác nhận dependency hoặc trả exit 2 với danh sách gói thiếu.

**Step 6: Commit**

```bash
git add src/ocr_bench/adapters/marker.py src/ocr_bench/adapters/opendataloader.py scripts/run_odl_hybrid.py pyproject.toml tests/test_marker_adapter.py tests/test_opendataloader_adapter.py tests/test_odl_hybrid.py
git commit -m "feat: split Marker and OpenDataLoader profiles"
```

## Task 6: Làm profile Sovereign có danh tính ổn định và fail-closed

**Files:**

- Modify: `src/ocr_bench/adapters/sovereign.py`
- Create: `scripts/preflight_sovereign.py`
- Test: `tests/test_sovereign_adapter.py`
- Test: `tests/test_sovereign_preflight.py`

**Step 1: Viết test đỏ cho mode mismatch**

```python
def test_sovereign_default_refuses_marker_environment(monkeypatch):
    monkeypatch.setattr(sov, "marker_san_sang", lambda: True)
    adapter = SovereignAdapter.from_profile(profile("sovereign_default"))
    with pytest.raises(ProfileEnvironmentError, match="marker_available"):
        adapter.preflight()

def test_sovereign_scan_requires_marker(monkeypatch):
    monkeypatch.setattr(sov, "marker_san_sang", lambda: False)
    adapter = SovereignAdapter.from_profile(profile("sovereign_scan"))
    with pytest.raises(ProfileEnvironmentError):
        adapter.preflight()
```

**Step 2: Chạy test đỏ**

Run: `py -3 -m pytest tests/test_sovereign_adapter.py tests/test_sovereign_preflight.py -q`

**Step 3: Cài profile gate**

- `sovereign_default` chỉ chạy trong venv không có Marker cache/escalation.
- `sovereign_scan` chỉ chạy khi Marker local sẵn sàng.
- Cả hai tiếp tục cưỡng bức `OCR_USE_VISION_API=false`, khóa API rỗng và giữ cost/time ceilings.
- Fingerprint ghi BE commit, dirty state, resolved config, Marker version/model cache, Python và profile hash.
- Không gọi API ngoài; nếu config resolved có key/URL trả phí, preflight dừng bằng `VuotTran`.

**Step 4: Ghi raw response an toàn**

Lưu response `{success, fullText}` đã loại token/secret thành `sovereign.json`. Thêm test quét artifact và fingerprint không chứa giá trị của biến `OPENROUTER_API_KEY`, `GROQ_API_KEY`.

**Step 5: Chạy test**

Run: `py -3 -m pytest tests/test_sovereign_adapter.py tests/test_sovereign_preflight.py -q`

Expected: PASS.

**Step 6: Commit**

```bash
git add src/ocr_bench/adapters/sovereign.py scripts/preflight_sovereign.py tests/test_sovereign_adapter.py tests/test_sovereign_preflight.py
git commit -m "feat: make Sovereign profiles fail closed"
```

## Task 7: Manifest dataset hợp nhất và license/checksum gate

**Files:**

- Create: `datasets/catalog.json`
- Create: `src/ocr_bench/dataset_manifest.py`
- Create: `scripts/build_dataset_manifest.py`
- Create: `datasets/corrections.jsonl`
- Modify: `scripts/make_manifest.py`
- Test: `tests/test_dataset_manifest.py`
- Test: `tests/test_corpus.py`

**Step 1: Viết test đỏ cho provenance từng tài liệu**

```python
def test_every_included_document_has_reproducible_provenance(tmp_path):
    manifest = build_manifest(ROOT)
    assert manifest["documents"]
    for row in manifest["documents"]:
        assert row["source_url"].startswith("https://")
        assert row["source_version"]
        assert row["source_license"]
        assert re.fullmatch(r"[0-9a-f]{64}", row["pdf_sha256"])
        assert re.fullmatch(r"[0-9a-f]{64}", row["annotation_sha256"])
        assert any(row["annotations"].values())
```

```python
def test_unverified_dataset_cannot_be_included():
    with pytest.raises(DatasetManifestError, match="license"):
        validate_catalog_entry({
            "name": "unverified",
            "status": "included",
            "version": "1",
            "source_url": "https://example.org/public-dataset",
            "license": None,
        })
```

**Step 2: Chạy test đỏ**

Run: `py -3 -m pytest tests/test_dataset_manifest.py tests/test_corpus.py -q`

**Step 3: Xây manifest v1 từ nguồn đã có**

- Included: DocLayNet và olmOCR-bench hiện có.
- Candidate/excluded: UIT-DODV, PubTabNet, FinTabNet, OHR-Bench; mỗi entry ghi trạng thái và lý do, không tải khi license/access chưa xác minh.
- `datasets/manifest.json` được sinh, không sửa tay; thứ tự theo `document_id`, JSON `sort_keys=True`.
- Mỗi row có `language`, `document_type`, `scan_category`, annotation capability flags và cả source checksum.
- Annotation checksum của olmOCR phải là JSONL nguồn tương ứng; DocLayNet là COCO source cộng correction overlay hash.

**Step 4: Cài correction overlay bất biến**

Mỗi correction bắt buộc `document_id`, operation, item, evidence, reviewer_count >= 2 và source snapshot SHA. Loader áp overlay sau khi verify source checksum; báo cáo sinh cả trước/sau nếu overlay làm thay đổi hạng.

**Step 5: Verify**

Run: `py -3 scripts/build_dataset_manifest.py --verify`

Run: `py -3 -m pytest tests/test_dataset_manifest.py tests/test_corpus.py -q`

Expected: PASS; manifest báo rõ chưa có transcript tiếng Việt nếu chưa có nguồn included phù hợp.

**Step 6: Commit**

```bash
git add datasets/catalog.json datasets/corrections.jsonl datasets/manifest.json src/ocr_bench/dataset_manifest.py scripts/build_dataset_manifest.py scripts/make_manifest.py tests/test_dataset_manifest.py tests/test_corpus.py
git commit -m "feat: add public dataset provenance manifest"
```

## Task 8: Hoàn thiện metric theo sáu tầng năng lực

**Files:**

- Create: `src/ocr_bench/metrics/layout.py`
- Create: `src/ocr_bench/metrics/table_cells.py`
- Create: `src/ocr_bench/metrics/diacritics.py`
- Create: `src/ocr_bench/metrics/robustness.py`
- Modify: `src/ocr_bench/metrics/imgf1.py`
- Modify: `src/ocr_bench/metrics/nid.py`
- Modify: `src/ocr_bench/metrics/perf.py`
- Modify: `src/ocr_bench/__init__.py`
- Test: `tests/test_layout_metric.py`
- Test: `tests/test_table_cells_metric.py`
- Test: `tests/test_diacritics_metric.py`
- Test: `tests/test_robustness.py`
- Modify: `tests/test_imgf1_metric.py`
- Modify: `tests/test_nid_metric.py`
- Modify: `tests/test_perf.py`

**Step 1: Viết controls đỏ cho từng metric mới**

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

**Step 2: Chạy test đỏ**

Run: `py -3 -m pytest tests/test_layout_metric.py tests/test_table_cells_metric.py tests/test_diacritics_metric.py tests/test_robustness.py -q`

**Step 3: Cài metric và định nghĩa toán học trong docstring**

- Layout: bipartite matching theo IoU >= 0.5; Block F1 không xét type; Type macro-F1 xét type trên cặp đã match.
- Table recall: bảng GT được match nếu IoU >= 0.5; TEDS/TEDS-Struct giữ implementation hiện có.
- Cell F1: parse grid có rowspan/colspan; match cell theo tọa độ lưới và normalized content.
- Cell CER và lỗi dấu chỉ chạy khi có transcript/cell text GT độc lập; thiếu thì `NO_GROUND_TRUTH`.
- Reading order NID chỉ chạy trên nhãn order thật; không tạo thứ tự GT bằng heuristic hình học.
- Scan robustness là paired relative degradation giữa nhóm `digital` và mức scan trên cùng base document; nếu dataset không có cặp, metric là experimental/N/A.
- Perf thêm pages, cold start, warm seconds/page, p95, peak RSS, VRAM nullable.

**Step 4: Sửa matching đã biết có rủi ro**

Thay greedy many-to-one trong image/layout matching bằng maximum-weight bipartite matching tất định. Giữ metric legacy dưới tên versioned nếu cần so lịch sử; không thay số cũ dưới cùng một metric name.

**Step 5: Chạy toàn bộ metric tests**

Run: `py -3 -m pytest tests/test_*metric.py tests/test_robustness.py tests/test_perf.py -q`

Expected: PASS.

**Step 6: Commit**

```bash
git add src/ocr_bench/metrics src/ocr_bench/__init__.py tests/test_*metric.py tests/test_robustness.py tests/test_perf.py
git commit -m "feat: add capability-layer benchmark metrics"
```

## Task 9: Metric qualification gate và sabotage theo mức độ

**Files:**

- Modify: `src/ocr_bench/adapters/sabotage.py`
- Create: `src/ocr_bench/metric_qualification.py`
- Create: `scripts/qualify_metrics.py`
- Create: `configs/metric-registry.json`
- Modify: `src/ocr_bench/discrimination.py`
- Test: `tests/test_metric_qualification.py`
- Modify: `tests/test_discrimination.py`

**Step 1: Viết test đỏ cho monotonic gate**

```python
def test_metric_is_rejected_when_severe_corruption_scores_higher():
    result = qualify_metric(
        metric="bad_metric",
        controls={"perfect": 1.0, "partial": 0.4, "severe": 0.6},
    )
    assert result.status == "experimental"
    assert "monotonic" in result.reasons
```

**Step 2: Chạy test đỏ**

Run: `py -3 -m pytest tests/test_metric_qualification.py tests/test_discrimination.py -q`

**Step 3: Mở rộng sabotage**

Mỗi operation nhận severity 0.1/0.3/0.6 với seed cố định:

- delete characters;
- swap paragraphs;
- jitter bbox;
- remove rowspan/colspan;
- remove tables;
- drop blocks.

Qualification output ghi reference check, controls, property tests, sabotage monotonicity, adapter validation và common-set size. Chỉ metric `main` mới đi vào ranking; `experimental` chỉ vào appendix.

**Step 4: Chạy gate**

Run: `py -3 scripts/qualify_metrics.py --out results/metric-qualification.json`

Expected: exit 0 khi mọi metric main đạt; exit 2 và nêu metric/reason nếu không.

**Step 5: Commit**

```bash
git add src/ocr_bench/adapters/sabotage.py src/ocr_bench/metric_qualification.py src/ocr_bench/discrimination.py scripts/qualify_metrics.py configs/metric-registry.json tests/test_metric_qualification.py tests/test_discrimination.py
git commit -m "feat: gate published metrics with controlled sabotage"
```

## Task 10: Paired statistics, effect size và capability ranking

**Files:**

- Create: `src/ocr_bench/statistics.py`
- Create: `src/ocr_bench/ranking.py`
- Modify: `pyproject.toml`
- Test: `tests/test_statistics.py`
- Test: `tests/test_ranking.py`

**Step 1: Viết test đỏ với ví dụ tính tay**

```python
def test_paired_comparison_uses_intersection_and_is_seeded():
    a = {"d1": .9, "d2": .8, "a-only": 1.0}
    b = {"d1": .7, "d2": .6, "b-only": 0.0}
    x = paired_compare(a, b, n_resamples=10_000, seed=20260811)
    y = paired_compare(a, b, n_resamples=10_000, seed=20260811)
    assert x == y
    assert x.doc_ids == ("d1", "d2")
    assert x.mean_delta == pytest.approx(.2)
```

```python
def test_rank_ties_best_when_difference_is_not_material():
    groups = capability_groups(comparisons, practical_delta=.01)
    assert groups["engine_a"] == "A"
    assert groups["engine_b"] == "A"
```

**Step 2: Chạy test đỏ**

Run: `py -3 -m pytest tests/test_statistics.py tests/test_ranking.py -q`

**Step 3: Cài thống kê**

- Macro average ở đơn vị tài liệu.
- Percentile paired bootstrap 10.000 lần, seed cố định và ghi seed.
- Wilcoxon signed-rank qua scipy; all-zero deltas trả trạng thái `identical`, không ném.
- Holm-Bonferroni trong từng family metric/capability.
- Effect size: matched-pairs rank-biserial correlation.
- CI riêng cho conditional mean và end-to-end mean.
- Mọi object output có `doc_ids_sha256` để chứng minh common set.

**Step 4: Cài nhóm A/B/C**

Profile thuộc A nếu không thua best profile đồng thời theo adjusted p-value và practical threshold đã khóa trong `configs/metric-registry.json`. B/C dựa trên effect-size band đã khóa; N/A giữ riêng. Không dùng lexical rank để phá tie khoa học.

**Step 5: Chạy test**

Run: `py -3 -m pytest tests/test_statistics.py tests/test_ranking.py -q`

Expected: PASS.

**Step 6: Commit**

```bash
git add src/ocr_bench/statistics.py src/ocr_bench/ranking.py pyproject.toml tests/test_statistics.py tests/test_ranking.py
git commit -m "feat: add paired statistical capability ranking"
```

## Task 11: Sinh raw results, bảng, biểu đồ và paper tiếng Việt tất định

**Files:**

- Create: `src/ocr_bench/research_report.py`
- Create: `src/ocr_bench/research_charts.py`
- Create: `scripts/build_research_report.py`
- Create: `paper/paper-vi.template.md`
- Create: `paper/executive-summary.template.md`
- Create: `paper/appendices/methods.md`
- Create: `paper/appendices/limitations.md`
- Test: `tests/test_research_report.py`
- Test: `tests/test_research_charts.py`
- Test: `tests/test_publication_trace.py`

**Step 1: Viết test đỏ cho output contract**

```python
def test_report_build_emits_all_required_artifacts(frozen_fixture, tmp_path):
    build_publication(frozen_fixture, tmp_path)
    required = {
        "paper/paper-vi.md", "paper/executive-summary.md",
        "results/raw-results.jsonl", "results/aggregate-results.json",
        "results/statistical-tests.json", "results/recommendations.json",
        "tables/text-ocr.md", "tables/layout.md", "tables/reading-order.md",
        "tables/tables.md", "tables/scan-robustness.md", "tables/performance.md",
        "figures/capability-ranking.svg", "figures/accuracy-speed.svg",
        "figures/scan-degradation.svg", "figures/failure-distribution.svg",
    }
    assert required <= relative_files(tmp_path)
```

```python
def test_every_number_in_paper_has_trace_id(frozen_fixture, tmp_path):
    build_publication(frozen_fixture, tmp_path)
    assert validate_publication_trace(tmp_path) == []
```

**Step 2: Chạy test đỏ**

Run: `py -3 -m pytest tests/test_research_report.py tests/test_research_charts.py tests/test_publication_trace.py -q`

**Step 3: Sinh data artifacts trước prose**

`build_research_report.py` thực hiện theo thứ tự:

1. verify dataset/run manifests và prediction checksums;
2. score per-document metric -> `raw-results.jsonl`;
3. aggregate/CI -> `aggregate-results.json`;
4. paired tests/Holm/effect size -> `statistical-tests.json`;
5. rule-based scenario matrix -> `recommendations.json`;
6. render Markdown tables và SVG;
7. inject only traceable values vào paper template.

Mỗi value có `trace_id`; paper dùng cú pháp comment `<!-- trace: aggregate:text_ocr:marker_scan -->` ngay sau bảng/claim số.

**Step 4: Sinh bảng và biểu đồ đúng semantics**

- Forest plot: mean + CI theo capability.
- Accuracy-speed Pareto: x=warm seconds/page, y=quality metric đã khai trong caption, size=RSS; không nối metric khác thang.
- Scan degradation chỉ vẽ paired data.
- Failure distribution theo `FailureKind`.
- Capability heatmap chỉ nằm executive summary.
- N/A hiện chữ, không vẽ thành cột 0.

**Step 5: Sinh recommendation bằng rule, không LLM**

Ví dụ rule cho scan nhiều chữ:

```python
eligible = [r for r in rows if r.capability == "ocr" and r.coverage >= .95]
winner = max(eligible, key=lambda r: (r.group == "A", r.end_to_end_mean, -r.fail_rate))
```

Mỗi recommendation bắt buộc profile, metric evidence, CI, trade-off, dataset scope và limitation. Nếu không có GT phù hợp, output phải là “chưa đủ bằng chứng”, không chọn winner.

**Step 6: Export PDF không cần LLM**

Ưu tiên Pandoc nếu có; nếu thiếu, Markdown vẫn là artifact bắt buộc và script trả hướng dẫn cài dependency thay vì gọi dịch vụ ngoài. PDF embed font hỗ trợ tiếng Việt và ghi tool/version vào publication manifest.

**Step 7: Chạy test và reproducibility check**

Run: `py -3 -m pytest tests/test_research_report.py tests/test_research_charts.py tests/test_publication_trace.py -q`

Run: `py -3 scripts/build_research_report.py --input tests/fixtures/frozen-study --out build/a`

Run: `py -3 scripts/build_research_report.py --input tests/fixtures/frozen-study --out build/b`

Run: `git diff --no-index -- build/a build/b`

Expected: PASS và không có diff.

**Step 8: Commit**

```bash
git add src/ocr_bench/research_report.py src/ocr_bench/research_charts.py scripts/build_research_report.py paper tests/test_research_report.py tests/test_research_charts.py tests/test_publication_trace.py
git commit -m "feat: generate deterministic Vietnamese research report"
```

## Task 12: Calibration, đóng băng cấu hình và pilot common-set

**Files:**

- Modify: `configs/profiles.json`
- Create: `calibration/README.md`
- Create: `calibration/decision-log.md`
- Create: `runs/pilot/run-manifest.json`
- Create: `runs/pilot/validation-report.md`

**Step 1: Chọn calibration set trước khi xem test result**

Lấy mẫu phân tầng 5 tài liệu mỗi nhóm từ DocLayNet và olmOCR bằng seed `20260811`; ghi danh sách/doc checksum vào `calibration/decision-log.md`. Không dùng tài liệu calibration trong bảng test chính nếu dataset đủ tách; nếu không đủ, công bố overlap.

**Step 2: Preflight từng environment**

Run:

```text
py -3 scripts/build_dataset_manifest.py --verify
.venv-docling\Scripts\python.exe scripts/run_research_predictions.py --mode calibration --profiles docling_default,docling_scan
.venv-odl\Scripts\python.exe scripts/run_odl_hybrid.py --check-only
.venv-marker\Scripts\python.exe scripts/run_research_predictions.py --mode calibration --profiles marker_default,marker_scan
.venv-sov\Scripts\python.exe scripts/preflight_sovereign.py --profile sovereign_default
.venv-marker\Scripts\python.exe scripts/preflight_sovereign.py --profile sovereign_scan
```

**Step 3: Calibration chỉ chọn trong không gian đã khai trước**

Được chọn: OCR on/off/force, language `vi,en`, table default/accurate, render DPI tối đa 300 nếu engine hỗ trợ chính thức. Không được thử tùy ý trên test set. Ghi mọi candidate, metric mục tiêu, runtime và quyết định vào decision log.

**Step 4: Khóa profile**

Cập nhật `configs/profiles.json`, tăng `catalog_version`, ghi SHA-256 và commit trước publication run.

**Step 5: Chạy pilot common-set**

Chạy 10 tài liệu chung cho đủ tám profile. `validation-report.md` phải ghi:

- profile chạy được/không được và lý do;
- raw-to-canonical trace sample;
- coordinate overlay review;
- coverage/capability matrix;
- failure taxonomy;
- metric qualification status;
- ước tính thời gian/RAM/disk của full run.

**Step 6: Commit**

```bash
git add configs/profiles.json calibration runs/pilot
git commit -m "research: freeze profiles after pilot calibration"
```

## Task 13: Publication run, manual audit và đóng băng nghiên cứu

**Files:**

- Create: `audit/sample-plan.json`
- Create: `audit/findings.jsonl`
- Create: `runs/publication/run-manifest.json`
- Create: `results/` generated artifacts
- Create: `tables/` generated artifacts
- Create: `figures/` generated artifacts
- Create: `paper/paper-vi.md` generated artifact
- Create: `paper/executive-summary.md` generated artifact
- Create: `paper/paper-vi.pdf` generated artifact

**Step 1: Tạo sample audit trước khi đọc output**

`audit/sample-plan.json` chọn phân tầng: random, điểm thấp, điểm cao, chênh lệch profile lớn, điểm 0 và failure. Reviewer phân loại mỗi bất đồng thành `engine`, `adapter`, `ground_truth`, `metric`, `unknown`; correction chỉ hợp lệ khi có hai reviewer và evidence.

**Step 2: Chạy publication prediction theo environment**

Chạy từng family/profile vào cùng run ID; runner resume theo cache key và từ chối config/version mismatch. Không commit token; không cần URL/secret LLM. OpenDataLoader hybrid chỉ dùng local URL đã khóa.

**Step 3: Chạy score/statistics/report**

Run:

```text
py -3 scripts/qualify_metrics.py --out results/metric-qualification.json
py -3 scripts/build_research_report.py --input runs/publication --out .
py -3 -m pytest -q
git diff --check
```

**Step 4: Manual audit và correction loop**

Nếu finding là adapter/metric bug: sửa bằng task TDD riêng, invalidation các artifact phụ thuộc, chấm lại từ prediction nếu raw mapping không đổi hoặc chạy lại engine nếu prediction đổi. Nếu là GT bug: thêm correction overlay, regenerate manifest, chấm lại và báo before/after. Không sửa trực tiếp generated table/paper.

**Step 5: Acceptance review**

Checklist cuối:

- tám profile hoặc N/A có bằng chứng;
- không secret trong repo (`rg -n "sk-|OPENROUTER_API_KEY=.+|GROQ_API_KEY=.+"` không có hit giá trị);
- common-set hash có ở mọi pairwise comparison;
- bảng đủ CI/n/coverage/fail;
- metric main đều qualified;
- recommendation không vượt phạm vi dataset;
- mọi trace ID resolve được;
- PDF hiển thị đúng dấu tiếng Việt, bảng và figure.

**Step 6: Đóng băng và commit artifact nghiên cứu**

```bash
git add audit runs/publication results tables figures paper datasets/manifest.json configs/profiles.json
git commit -m "research: publish OCR parser benchmark report"
git tag ocr-parser-benchmark-v1
```

## Thứ tự phụ thuộc và điểm dừng kiểm soát

```text
Task 1 -> Task 2 -> Task 3
                    |-> Task 4
                    |-> Task 5
                    |-> Task 6
Task 7 -------------+
Task 8 -> Task 9 -> Task 10 -> Task 11 -> Task 12 -> Task 13
```

- Sau Task 7: dừng nếu dataset manifest không có đủ GT cho bất kỳ năng lực chính nào; báo N/A thay vì tự sinh gold.
- Sau Task 9: dừng publication nếu metric main không qua qualification.
- Sau Task 12: dừng full run nếu pilot phát hiện coordinate/raw trace sai hoặc chi phí vượt trần.
- Task 13 chỉ bắt đầu khi profile catalog và dataset manifest đã được commit trên working tree sạch.

## Ước lượng thực thi

| Pha | Tasks | Công việc kỹ thuật | Thời gian máy phụ thuộc dữ liệu |
|---|---:|---|---|
| Hạ tầng tái lập | 1-3, 7 | 4-6 ngày kỹ sư | thấp |
| Adapter/profile | 4-6 | 5-8 ngày kỹ sư | tải model + smoke |
| Metric/thống kê | 8-10 | 6-9 ngày kỹ sư | thấp đến trung bình |
| Publication builder | 11 | 3-5 ngày kỹ sư | thấp |
| Calibration/pilot | 12 | 2-4 ngày | vài giờ đến vài ngày |
| Full run/audit/paper | 13 | 3-7 ngày người | phụ thuộc CPU/GPU, có thể nhiều ngày |

Ước lượng là planning range, không phải số đo cam kết. Pilot ở Task 12 phải thay range thời gian máy bằng dự báo từ throughput thật trước khi chạy toàn bộ corpus.
