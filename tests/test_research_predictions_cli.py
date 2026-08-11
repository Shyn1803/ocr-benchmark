"""Publication runner must fail closed before spending time on OCR engines."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

from ocr_bench.prediction import save_prediction
from ocr_bench.profiles import EngineProfile
from ocr_bench.types import Capability, OcrResult

ROOT = Path(__file__).resolve().parents[1]


def _load_script():
    path = ROOT / "scripts" / "run_research_predictions.py"
    spec = importlib.util.spec_from_file_location("_research_predictions", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _profile(name: str = "marker_default", *, force_ocr: bool = False) -> EngineProfile:
    family, variant = name.rsplit("_", 1)
    return EngineProfile(
        name=name,
        family=family,
        profile=variant,
        adapter=family,
        config={"force_ocr": force_ocr, "use_llm": False},
        environment={},
    )


class _FakeAdapter:
    name = "marker_default"
    capabilities = frozenset({Capability.TEXT_MD})

    def __init__(self, *, configured_as: str | None = None, perf: bool = True) -> None:
        self.execute_count = 0
        self.configured_as = configured_as
        self.perf = perf
        self.events: list[str] = []

    def configure_hardware(self, hardware: str) -> str:
        self.events.append(f"configure:{hardware}")
        return self.configured_as or hardware

    def version(self) -> str:
        return "fake-1"

    def config_fingerprint(self) -> dict[str, object]:
        return {"force_ocr": False, "use_llm": False}

    def execute(self, doc: Path) -> OcrResult:
        self.events.append("execute")
        self.execute_count += 1
        return OcrResult(
            engine=self.name,
            engine_family="marker",
            profile="default",
            engine_version=self.version(),
            doc_id=doc.stem,
            capabilities=self.capabilities,
            text_md="ok",
            seconds=1.0 if self.perf else None,
            peak_rss_mb=2.0 if self.perf else None,
            rss_scope="process" if self.perf else None,
            config_fingerprint=self.config_fingerprint(),
        )


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _dataset_manifest(path: Path, rows: list[dict[str, object]]) -> Path:
    path.write_text(json.dumps({"documents": rows}), encoding="utf-8")
    return path


def test_publication_cli_refuses_partial_profile_set_before_build(tmp_path, monkeypatch):
    runner = _load_script()
    built = False

    def forbidden_build(_profile):
        nonlocal built
        built = True
        raise AssertionError("publication subset reached adapter construction")

    monkeypatch.setattr(runner.registry, "build_adapter", forbidden_build)
    rc = runner.main(["--profiles", "marker_default", "--out", str(tmp_path)])

    assert rc == 2
    assert built is False
    assert not list(tmp_path.iterdir()), "a rejected publication run must not create output"


def test_preflight_fingerprint_must_match_locked_config():
    from ocr_bench.preflight import PreflightError, verify_fingerprint

    profile = _profile("marker_scan", force_ocr=True)
    with pytest.raises(PreflightError, match="force_ocr"):
        verify_fingerprint(profile, {"force_ocr": False, "use_llm": False})


def test_dataset_manifest_alone_selects_and_verifies_documents(tmp_path):
    from ocr_bench.preflight import verify_dataset_manifest

    pdfs = tmp_path / "pdfs"
    pdfs.mkdir()
    keep = pdfs / "keep.pdf"
    keep.write_bytes(b"%PDF-keep")
    (pdfs / "not-listed.pdf").write_bytes(b"%PDF-extra")
    manifest = _dataset_manifest(
        tmp_path / "manifest.json",
        [
            {
                "document_id": "keep",
                "pdf_path": "pdfs/keep.pdf",
                "pdf_sha256": _sha(b"%PDF-keep"),
            }
        ],
    )

    documents = verify_dataset_manifest(manifest, tmp_path)

    assert [(row.doc_id, row.path) for row in documents] == [("keep", keep.resolve())]


def test_pdf_changed_after_manifest_validation_is_rejected_before_execute(tmp_path):
    from ocr_bench.preflight import PreflightError, verify_dataset_manifest

    runner = _load_script()
    pdfs = tmp_path / "pdfs"
    pdfs.mkdir()
    doc = pdfs / "doc.pdf"
    doc.write_bytes(b"%PDF-original")
    manifest = _dataset_manifest(
        tmp_path / "manifest.json",
        [
            {
                "document_id": "doc",
                "pdf_path": "pdfs/doc.pdf",
                "pdf_sha256": _sha(b"%PDF-original"),
            }
        ],
    )
    verified = verify_dataset_manifest(manifest, tmp_path)
    doc.write_bytes(b"%PDF-mutated")
    adapter = _FakeAdapter()

    with pytest.raises(PreflightError, match="checksum|sha256"):
        runner.run_profile_predictions(
            _profile(),
            adapter,
            verified,
            tmp_path / "prediction" / "cpu",
            hardware="cpu",
            mode="publication",
        )
    assert adapter.execute_count == 0


@pytest.mark.parametrize("case", ["missing", "duplicate", "escape", "checksum"])
def test_dataset_manifest_rejects_unsafe_or_ambiguous_rows(tmp_path, case):
    from ocr_bench.preflight import PreflightError, verify_dataset_manifest

    pdfs = tmp_path / "pdfs"
    pdfs.mkdir()
    doc = pdfs / "doc.pdf"
    doc.write_bytes(b"%PDF-doc")
    outside = tmp_path.parent / f"{tmp_path.name}-outside.pdf"
    outside.write_bytes(b"%PDF-outside")
    valid = {
        "document_id": "doc",
        "pdf_path": "pdfs/doc.pdf",
        "pdf_sha256": _sha(b"%PDF-doc"),
    }
    if case == "missing":
        rows = [{**valid, "pdf_path": "pdfs/missing.pdf"}]
    elif case == "duplicate":
        rows = [valid, valid]
    elif case == "escape":
        rows = [{**valid, "pdf_path": f"../{outside.name}"}]
    else:
        rows = [{**valid, "pdf_sha256": "0" * 64}]
    manifest = _dataset_manifest(tmp_path / "manifest.json", rows)

    with pytest.raises(PreflightError, match=case if case != "escape" else "ngoài"):
        verify_dataset_manifest(manifest, tmp_path)


def test_calibration_subset_writes_only_under_calibration_tree(tmp_path, monkeypatch):
    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-test")
    adapter = _FakeAdapter()

    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(runner, "discover_documents", lambda *_args, **_kw: [doc])
    monkeypatch.setattr(runner.registry, "build_adapter", lambda _profile: adapter)

    rc = runner.main(
        [
            "--mode",
            "calibration",
            "--profiles",
            profile.name,
            "--out",
            str(tmp_path / "run"),
        ]
    )

    assert rc == 0
    prediction = (
        tmp_path
        / "run"
        / "calibration"
        / "prediction"
        / "cpu"
        / profile.name
        / "fixture.json"
    )
    assert prediction.is_file()
    assert not (tmp_path / "run" / "results").exists()
    assert adapter.execute_count == 1


def test_cli_reports_missing_profile_adapter_without_traceback(tmp_path, monkeypatch):
    runner = _load_script()
    profile = _profile("missing_default")
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-test")
    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(runner, "discover_documents", lambda *_args, **_kw: [doc])

    rc = runner.main(
        [
            "--mode",
            "calibration",
            "--profiles",
            profile.name,
            "--out",
            str(tmp_path / "run"),
        ]
    )

    assert rc == 2
    assert not (tmp_path / "run" / "calibration" / "prediction").exists()


def test_publication_cache_identity_mismatch_is_error_not_rerun(tmp_path):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    adapter = _FakeAdapter()
    output_root = tmp_path / "prediction" / "cpu"
    stale = adapter.execute(doc)
    stale = runner.attach_cache_identity(
        stale,
        {
            "doc_id": doc.stem,
            "pdf_sha256": "0" * 64,
            "profile_config_sha256": profile.fingerprint,
            "engine_version": adapter.version(),
            "hardware": "cpu",
        },
    )
    save_prediction(stale, output_root)
    adapter.execute_count = 0

    with pytest.raises(PreflightError, match="pdf_sha256"):
        runner.run_profile_predictions(
            profile,
            adapter,
            [doc],
            output_root,
            hardware="cpu",
            mode="publication",
        )

    assert adapter.execute_count == 0


def test_publication_cache_rejects_wrong_result_profile_even_with_matching_key(tmp_path):
    from ocr_bench.preflight import PreflightError, build_cache_identity

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    adapter = _FakeAdapter()
    output_root = tmp_path / "prediction" / "cpu"
    identity = build_cache_identity(
        doc,
        profile,
        engine_version=adapter.version(),
        hardware="cpu",
    )
    wrong_profile = OcrResult(
        engine=profile.name,
        engine_family=profile.family,
        profile="scan",
        engine_version=adapter.version(),
        doc_id=doc.stem,
        capabilities=adapter.capabilities,
        text_md="stale",
        config_fingerprint=adapter.config_fingerprint(),
    )
    save_prediction(runner.attach_cache_identity(wrong_profile, identity), output_root)

    with pytest.raises(PreflightError, match="profile"):
        runner.run_profile_predictions(
            profile,
            adapter,
            [doc],
            output_root,
            hardware="cpu",
            mode="publication",
        )


def test_publication_configures_hardware_before_execute_and_records_device(tmp_path):
    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    adapter = _FakeAdapter()

    result = runner.run_profile_predictions(
        profile,
        adapter,
        [doc],
        tmp_path / "prediction" / "cpu",
        hardware="cpu",
        mode="publication",
    )[0]

    assert adapter.events == ["configure:cpu", "execute"]
    assert result.config_fingerprint["hardware"] == "cpu"
    assert result.config_fingerprint["device"] == "cpu"


def test_publication_rejects_adapter_hardware_mismatch_before_execute(tmp_path):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    adapter = _FakeAdapter(configured_as="gpu")
    with pytest.raises(PreflightError, match="hardware|device"):
        runner.run_profile_predictions(
            _profile(),
            adapter,
            [],
            tmp_path,
            hardware="cpu",
            mode="publication",
        )
    assert adapter.execute_count == 0


def test_publication_rejects_adapter_without_hardware_protocol(tmp_path):
    from ocr_bench.preflight import PreflightError

    class Unsupported:
        name = "marker_default"

        def version(self):
            return "fake-1"

        def config_fingerprint(self):
            return {"force_ocr": False, "use_llm": False}

        def execute(self, _doc):
            raise AssertionError("unsupported adapter must not execute")

    runner = _load_script()
    with pytest.raises(PreflightError, match="configure_hardware"):
        runner.run_profile_predictions(
            _profile(),
            Unsupported(),
            [],
            tmp_path,
            hardware="cpu",
            mode="publication",
        )


def test_publication_rejects_missing_perf_before_save(tmp_path):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")

    with pytest.raises(PreflightError, match="seconds"):
        runner.run_profile_predictions(
            profile,
            _FakeAdapter(perf=False),
            [doc],
            tmp_path / "prediction" / "cpu",
            hardware="cpu",
            mode="publication",
        )
    assert not (tmp_path / "prediction").exists()


def test_publication_rejects_cached_result_with_missing_perf_without_execute(tmp_path):
    from ocr_bench.preflight import PreflightError, build_cache_identity

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    adapter = _FakeAdapter(perf=False)
    identity = build_cache_identity(
        doc, profile, engine_version=adapter.version(), hardware="cpu"
    )
    output_root = tmp_path / "prediction" / "cpu"
    save_prediction(
        runner.attach_cache_identity(adapter.execute(doc), identity), output_root
    )
    adapter.execute_count = 0

    with pytest.raises(PreflightError, match="seconds"):
        runner.run_profile_predictions(
            profile,
            adapter,
            [doc],
            output_root,
            hardware="cpu",
            mode="publication",
        )
    assert adapter.execute_count == 0


@pytest.mark.parametrize("bad_bytes", [b"{broken", b'{"schema_version":2}'])
@pytest.mark.parametrize("mode,should_execute", [("calibration", True), ("publication", False)])
def test_bad_cache_reruns_only_in_calibration(tmp_path, bad_bytes, mode, should_execute):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    output_root = tmp_path / "prediction" / "cpu"
    cache = output_root / profile.name / "fixture.json"
    cache.parent.mkdir(parents=True)
    cache.write_bytes(bad_bytes)
    adapter = _FakeAdapter()

    if mode == "publication":
        with pytest.raises(PreflightError):
            runner.run_profile_predictions(
                profile, adapter, [doc], output_root, hardware="cpu", mode=mode
            )
    else:
        runner.run_profile_predictions(
            profile, adapter, [doc], output_root, hardware="cpu", mode=mode
        )
    assert bool(adapter.execute_count) is should_execute


def test_publication_helper_rejects_refresh_even_when_called_directly(tmp_path):
    from ocr_bench.preflight import PreflightError

    runner = _load_script()
    with pytest.raises(PreflightError, match="refresh"):
        runner.run_profile_predictions(
            _profile(),
            _FakeAdapter(),
            [],
            tmp_path,
            hardware="cpu",
            mode="publication",
            refresh=True,
        )


def test_run_manifest_is_deterministic_except_generated_at(tmp_path):
    from ocr_bench.preflight import build_run_manifest

    manifest = tmp_path / "dataset.json"
    manifest.write_text('{"dataset":"fixed"}\n', encoding="utf-8")
    profile = _profile()
    fixed = {
        "git": {"commit": "a" * 40, "dirty": False},
        "system": {
            "python": "3.12.0",
            "os": "TestOS",
            "cpu": "Test CPU",
            "gpu": None,
            "ram_bytes": 1024,
        },
        "dependencies": {"ocr-bench": "0.1.0"},
    }

    first = build_run_manifest(
        mode="publication",
        hardware="cpu",
        profiles={profile.name: profile},
        dataset_manifest=manifest,
        generated_at="2026-08-11T00:00:00Z",
        **fixed,
    )
    second = build_run_manifest(
        mode="publication",
        hardware="cpu",
        profiles={profile.name: profile},
        dataset_manifest=manifest,
        generated_at="later",
        **fixed,
    )

    assert first | {"generated_at": "later"} == second
    assert first["profiles"] == [
        {"name": profile.name, "config_sha256": profile.fingerprint}
    ]
    assert first["dataset_manifest"]["sha256"] == (
        "c5c0225cf54a86b0e729ca91a74107ab9fefb5cc84a8819a6d5a3cf40b732345"
    )
    serialized = json.dumps(first, sort_keys=True)
    assert "secret" not in serialized.lower()


def test_publication_profile_order_is_catalog_order_for_every_cli_order():
    from ocr_bench.preflight import verify_profile_selection

    scan = _profile("marker_scan", force_ocr=True)
    default = _profile()
    catalog = {scan.name: scan, default.name: default}

    first = verify_profile_selection(
        catalog, [default.name, scan.name], mode="publication"
    )
    second = verify_profile_selection(
        catalog, [scan.name, default.name], mode="publication"
    )

    assert list(first) == list(second) == [scan.name, default.name]


def test_cli_orders_execution_and_manifest_by_catalog_for_two_cli_orders(
    tmp_path, monkeypatch
):
    from ocr_bench.preflight import DatasetDocument

    runner = _load_script()
    scan = _profile("marker_scan", force_ocr=True)
    default = _profile()
    catalog = {scan.name: scan, default.name: default}
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    manifest = _dataset_manifest(tmp_path / "manifest.json", [])
    verified_doc = DatasetDocument(doc.stem, doc, _sha(doc.read_bytes()))
    executions: list[str] = []

    class OrderedAdapter(_FakeAdapter):
        def __init__(self, profile):
            super().__init__()
            self.bound_profile = profile
            self.name = profile.name

        def config_fingerprint(self):
            return dict(self.bound_profile.config)

        def execute(self, path):
            executions.append(self.name)
            return OcrResult(
                engine=self.name,
                engine_family=self.bound_profile.family,
                profile=self.bound_profile.profile,
                engine_version=self.version(),
                doc_id=path.stem,
                capabilities=self.capabilities,
                text_md="ok",
                seconds=1.0,
                peak_rss_mb=2.0,
                rss_scope="process",
                config_fingerprint=self.config_fingerprint(),
            )

    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: catalog)
    monkeypatch.setattr(runner.registry, "build_adapter", OrderedAdapter)
    monkeypatch.setattr(
        runner,
        "publication_preflight",
        lambda **_kw: runner.PreflightContext(
            git={"commit": "a" * 40, "dirty": False},
            system={"python": "3", "os": "x", "cpu": "cpu", "gpu": None, "ram_bytes": 1},
            dependencies={},
            documents=(verified_doc,),
        ),
    )

    manifests = []
    for index, order in enumerate(
        ([default.name, scan.name], [scan.name, default.name])
    ):
        executions.clear()
        out = tmp_path / f"run-{index}"
        assert (
            runner.main(
                [
                    "--profiles",
                    ",".join(order),
                    "--dataset-manifest",
                    str(manifest),
                    "--out",
                    str(out),
                ]
            )
            == 0
        )
        assert executions == [scan.name, default.name]
        payload = json.loads((out / "run-manifest.json").read_text(encoding="utf-8"))
        payload["generated_at"] = "ignored"
        manifests.append(payload)

    assert manifests[0] == manifests[1]
    assert [row["name"] for row in manifests[0]["profiles"]] == [
        scan.name,
        default.name,
    ]


def test_cpu_probe_does_not_turn_missing_identity_into_unknown(monkeypatch):
    import ocr_bench.preflight as preflight

    monkeypatch.setattr(preflight.platform, "processor", lambda: "")
    monkeypatch.delenv("PROCESSOR_IDENTIFIER", raising=False)
    monkeypatch.setattr(preflight, "_gpu_name", lambda: None)
    monkeypatch.setattr(preflight, "_ram_bytes", lambda: 1024)

    assert preflight.collect_system_metadata()["cpu"] is None


@pytest.mark.parametrize(
    "hardware,system,match",
    [
        (
            "gpu",
            {"python": "3", "os": "x", "cpu": "cpu", "gpu": None, "ram_bytes": 1},
            "GPU",
        ),
        (
            "cpu",
            {"python": "3", "os": "x", "cpu": None, "gpu": None, "ram_bytes": 1},
            "CPU",
        ),
    ],
)
def test_publication_preflight_rejects_unavailable_hardware_identity(
    tmp_path, monkeypatch, hardware, system, match
):
    import ocr_bench.preflight as preflight

    doc = tmp_path / "doc.pdf"
    doc.write_bytes(b"%PDF")
    verified = preflight.DatasetDocument("doc", doc, _sha(doc.read_bytes()))
    monkeypatch.setattr(
        preflight,
        "collect_git_metadata",
        lambda *_args, **_kw: {"commit": "a" * 40, "dirty": False},
    )

    with pytest.raises(preflight.PreflightError, match=match):
        preflight.publication_preflight(
            repo_root=tmp_path,
            dataset_manifest=tmp_path / "manifest.json",
            hardware=hardware,
            dataset_validator=lambda *_args: (verified,),
            system_probe=lambda: system,
            dependency_probe=lambda: {},
        )


def test_cpu_mask_is_applied_before_adapter_construction(tmp_path, monkeypatch):
    runner = _load_script()
    profile = _profile()
    doc = tmp_path / "fixture.pdf"
    doc.write_bytes(b"%PDF-current")
    manifest = _dataset_manifest(
        tmp_path / "manifest.json",
        [
            {
                "document_id": doc.stem,
                "pdf_path": str(doc.relative_to(tmp_path)),
                "pdf_sha256": _sha(doc.read_bytes()),
            }
        ],
    )
    adapter = _FakeAdapter()
    observed: dict[str, str | None] = {}

    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "load_profile_catalog", lambda _path: {profile.name: profile})
    monkeypatch.setattr(
        runner,
        "publication_preflight",
        lambda **_kw: runner.PreflightContext(
            git={"commit": "a" * 40, "dirty": False},
            system={"python": "3", "os": "x", "cpu": "cpu", "gpu": None, "ram_bytes": 1},
            dependencies={},
            documents=(),
        ),
    )

    def build(_profile):
        observed["hardware"] = os.environ.get("OCR_BENCH_HARDWARE")
        observed["cuda"] = os.environ.get("CUDA_VISIBLE_DEVICES")
        return adapter

    monkeypatch.setattr(runner.registry, "build_adapter", build)
    monkeypatch.setattr(runner, "discover_documents", lambda *_args, **_kw: [doc])

    assert runner.main(["--dataset-manifest", str(manifest), "--out", str(tmp_path / "out")]) == 0
    assert observed == {"hardware": "cpu", "cuda": ""}
