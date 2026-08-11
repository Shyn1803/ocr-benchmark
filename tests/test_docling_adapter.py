"""Contracts for the optional Docling 2.91 benchmark adapter."""

from __future__ import annotations

import hashlib
import importlib
import json
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import SimpleNamespace

import pytest

from ocr_bench.adapters.base import AdapterOutputError
from ocr_bench.prediction import load_prediction, save_prediction
from ocr_bench.profiles import EngineProfile, ProfileConfigError, load_profile_catalog
from ocr_bench.types import BlockType, FailureKind


ROOT = Path(__file__).resolve().parents[1]
CATALOG = load_profile_catalog(ROOT / "configs" / "profiles.json")


@dataclass
class FakeBox:
    l: float
    t: float
    r: float
    b: float
    coord_origin: str = "TOPLEFT"

    def to_top_left_origin(self, page_height: float) -> "FakeBox":
        if self.coord_origin == "TOPLEFT":
            return FakeBox(self.l, self.t, self.r, self.b)
        return FakeBox(
            self.l,
            page_height - self.t,
            self.r,
            page_height - self.b,
        )


@dataclass
class FakeProv:
    page_no: int
    bbox: FakeBox


class FakeTableData:
    num_rows = 2
    num_cols = 2


class FakeItem:
    def __init__(
        self,
        *,
        self_ref: str,
        label: str,
        page_no: int,
        bbox: FakeBox,
        text: str | None = None,
        level: int | None = None,
    ) -> None:
        self.self_ref = self_ref
        self.label = label
        self.prov = [FakeProv(page_no, bbox)]
        self.text = text
        self.level = level
        if label == "table":
            self.data = FakeTableData()

    def export_to_html(self, *, doc, add_caption=False) -> str:
        assert doc is not None
        assert add_caption is False
        return "<table><tr><td>A</td><td>B</td></tr></table>"


class FakeDocument:
    def __init__(self) -> None:
        self.pages = {
            1: SimpleNamespace(page_no=1, size=SimpleNamespace(width=100.0, height=200.0)),
            2: SimpleNamespace(page_no=2, size=SimpleNamespace(width=400.0, height=100.0)),
        }
        self.items = [
            FakeItem(
                self_ref="#/texts/0",
                label="section_header",
                page_no=1,
                bbox=FakeBox(10.0, 20.0, 50.0, 60.0),
                text="Mục một",
                level=2,
            ),
            FakeItem(
                self_ref="#/texts/1",
                label="text",
                page_no=2,
                # Bottom-left coordinates exercise the y-axis conversion. The
                # top-left box is (100, 10)-(300, 50) on a 400x100 page.
                bbox=FakeBox(100.0, 90.0, 300.0, 50.0, "BOTTOMLEFT"),
                text="Nội dung trang hai",
            ),
            FakeItem(
                self_ref="#/tables/0",
                label="table",
                page_no=2,
                bbox=FakeBox(40.0, 55.0, 360.0, 95.0),
            ),
        ]

    def iterate_items(self):
        return iter((item, 1) for item in self.items)

    def export_to_markdown(self) -> str:
        return "## Mục một\n\nNội dung trang hai\n\n| A | B |"

    def export_to_dict(self):
        # Deliberately non-canonical key order; the adapter owns stable bytes.
        return {
            "tables": [{"self_ref": "#/tables/0", "data": {"num_rows": 2}}],
            "texts": [
                {"text": "Mục một", "self_ref": "#/texts/0"},
                {"text": "Nội dung trang hai", "self_ref": "#/texts/1"},
            ],
            "pages": {"2": {"width": 400}, "1": {"width": 100}},
        }


def _docling_module():
    return importlib.import_module("ocr_bench.adapters.docling")


def test_docling_build_result_maps_pages_boxes_tables_and_raw():
    """A 1-based/bottom-left Docling item must not leak either convention."""
    module = _docling_module()
    result = module.build_result(FakeDocument(), identity=module.SCAN_IDENTITY)

    assert result.engine == "docling_scan"
    assert result.engine_family == "docling"
    assert result.profile == "scan"
    assert result.page_sizes == ((100.0, 200.0), (400.0, 100.0))
    assert result.blocks[0].box.page == 0
    assert result.blocks[0].box.x0 == pytest.approx(0.1)
    assert result.blocks[0].box.y0 == pytest.approx(0.1)
    assert result.blocks[1].box.page == 1
    assert result.blocks[1].box.x0 == pytest.approx(0.25)
    assert result.blocks[1].box.y0 == pytest.approx(0.1)
    assert result.blocks[1].box.y1 == pytest.approx(0.5)
    assert result.blocks[0].block_type is BlockType.HEADING
    assert result.blocks[0].level == 2
    assert result.tables[0].html.startswith("<table")
    assert result.tables[0].n_rows == 2
    assert result.tables[0].n_cols == 2
    assert result.raw_artifacts[0].name == "docling.json"


def test_docling_raw_and_trace_artifacts_are_deterministic_and_resolve_refs(tmp_path: Path):
    """Every canonical item must point back to a self_ref present in verbatim raw JSON."""
    module = _docling_module()
    first = module.build_result(FakeDocument(), identity=module.SCAN_IDENTITY)
    second = module.build_result(FakeDocument(), identity=module.SCAN_IDENTITY)

    assert [a.name for a in first.raw_artifacts] == ["docling.json", "docling-map.json"]
    assert first.raw_artifacts[0].data == second.raw_artifacts[0].data
    assert first.raw_artifacts[1].data == second.raw_artifacts[1].data
    assert first.raw_artifacts[0].data == json.dumps(
        FakeDocument().export_to_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")

    raw = json.loads(first.raw_artifacts[0].data)
    trace = json.loads(first.raw_artifacts[1].data)
    raw_refs = {
        item["self_ref"]
        for collection in (raw["texts"], raw["tables"])
        for item in collection
    }
    assert set(trace["blocks"].values()) <= raw_refs
    assert set(trace["tables"].values()) <= raw_refs
    assert set(trace["blocks"]) == {str(i) for i in range(len(first.blocks))}
    assert set(trace["tables"]) == {str(i) for i in range(len(first.tables))}

    prediction = save_prediction(first, tmp_path)
    loaded = load_prediction(prediction)
    assert loaded.raw_artifacts[0].sha256 == hashlib.sha256(
        first.raw_artifacts[0].data
    ).hexdigest()


@pytest.mark.parametrize(
    "mutate,match",
    [
        (lambda doc: setattr(doc.items[0], "prov", []), "provenance"),
        (lambda doc: setattr(doc.pages[1].size, "width", 0), "page 1"),
        (lambda doc: setattr(doc, "export_to_dict", lambda: {"bad": float("nan")}), "JSON"),
        (
            lambda doc: setattr(
                doc.items[2],
                "export_to_html",
                lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("bad grid")),
            ),
            "table",
        ),
    ],
)
def test_docling_malformed_output_raises_adapter_output_error(mutate, match):
    """Malformed engine output is an adapter failure, not a generic engine failure."""
    module = _docling_module()
    document = FakeDocument()
    mutate(document)
    with pytest.raises(AdapterOutputError, match=match):
        module.build_result(document, identity=module.DEFAULT_IDENTITY)


@pytest.mark.parametrize(
    "html",
    [
        "<table",
        "<tablex></tablex>",
        "<table><tr><td>A</td></tr>",
        "<table></table><table></table>",
        "<table><tr><td>A</tr></td></table>",
    ],
)
def test_docling_rejects_malformed_or_multiple_table_roots(html: str):
    """A table-looking prefix must not publish malformed HTML to TEDS."""
    module = _docling_module()
    document = FakeDocument()
    document.items[2].export_to_html = lambda **_kwargs: html

    with pytest.raises(AdapterOutputError, match="table"):
        module.build_result(document, identity=module.DEFAULT_IDENTITY)


def test_docling_accepts_structured_table_html_with_attributes_and_entities():
    """The strict validator still accepts ordinary Docling table structure."""
    module = _docling_module()
    document = FakeDocument()
    html = (
        '<table class="data"><thead><tr><th rowspan="2">A &amp; B</th></tr></thead>'
        "<tbody><tr><td>C</td></tr></tbody></table>"
    )
    document.items[2].export_to_html = lambda **_kwargs: html

    result = module.build_result(document, identity=module.DEFAULT_IDENTITY)

    assert result.tables[0].html == html


def test_docling_profiles_bind_exact_publication_identity_and_catalog_config():
    """Profile construction must not collapse default and scan into one registry name."""
    module = _docling_module()
    default = module.DoclingAdapter.from_profile(CATALOG["docling_default"])
    scan = module.DoclingAdapter.from_profile(CATALOG["docling_scan"])

    assert (default.name, default.engine_family, default.profile) == (
        "docling_default",
        "docling",
        "default",
    )
    assert (scan.name, scan.engine_family, scan.profile) == (
        "docling_scan",
        "docling",
        "scan",
    )
    for adapter, profile in (
        (default, CATALOG["docling_default"]),
        (scan, CATALOG["docling_scan"]),
    ):
        fingerprint = adapter.config_fingerprint()
        assert fingerprint["profile_config_sha256"] == profile.fingerprint
        for key, value in profile.config.items():
            expected = list(value) if isinstance(value, tuple) else value
            assert fingerprint[key] == expected


def test_docling_profile_rejects_environment_outside_frozen_catalog():
    """An unrecorded environment toggle would produce a third, mislabeled profile."""
    module = _docling_module()
    original = CATALOG["docling_default"]
    changed = EngineProfile(
        name=original.name,
        family=original.family,
        profile=original.profile,
        adapter=original.adapter,
        config=original.config,
        environment={"enable_remote_services": True},
    )
    with pytest.raises(ProfileConfigError, match="environment"):
        module.DoclingAdapter.from_profile(changed)


class FakeDevice(str, Enum):
    CPU = "cpu"
    CUDA = "cuda"


class FakeAcceleratorOptions:
    def __init__(self, *, device):
        self.device = device


_MISSING = object()


class FakeEasyOcrOptions:
    def __init__(
        self,
        *,
        lang=_MISSING,
        force_full_page_ocr=False,
        use_gpu=None,
    ):
        if lang is None:
            raise TypeError("lang must be a list, not None")
        self.lang = ["fr", "de", "es", "en"] if lang is _MISSING else lang
        self.force_full_page_ocr = force_full_page_ocr
        self.use_gpu = use_gpu


class FakeTableMode(str, Enum):
    FAST = "fast"
    ACCURATE = "accurate"


class FakeTableOptions:
    def __init__(self, *, mode=FakeTableMode.ACCURATE, do_cell_matching=True):
        self.mode = mode
        self.do_cell_matching = do_cell_matching


class FakePdfPipelineOptions:
    def __init__(
        self,
        *,
        do_ocr=True,
        ocr_options=None,
        table_structure_options=None,
        accelerator_options=None,
        enable_remote_services=False,
        allow_external_plugins=False,
    ):
        self.do_ocr = do_ocr
        self.ocr_options = ocr_options or FakeEasyOcrOptions()
        self.table_structure_options = table_structure_options or FakeTableOptions()
        self.accelerator_options = accelerator_options
        self.enable_remote_services = enable_remote_services
        self.allow_external_plugins = allow_external_plugins


@pytest.fixture
def fake_docling_api(monkeypatch):
    module = _docling_module()
    api = SimpleNamespace(
        AcceleratorDevice=FakeDevice,
        AcceleratorOptions=FakeAcceleratorOptions,
        EasyOcrOptions=FakeEasyOcrOptions,
        PdfPipelineOptions=FakePdfPipelineOptions,
        TableFormerMode=FakeTableMode,
        TableStructureOptions=FakeTableOptions,
    )
    monkeypatch.setattr(module, "_load_docling_api", lambda: api)
    return module


def test_docling_scan_profile_forces_ocr_and_accurate_tables(fake_docling_api):
    adapter = fake_docling_api.DoclingAdapter.from_profile(CATALOG["docling_scan"])
    opts = adapter.pipeline_options()

    assert opts.do_ocr is True
    assert opts.ocr_options.force_full_page_ocr is True
    assert opts.ocr_options.lang == ["vi", "en"]
    # Docling 2.91 derives EasyOCR GPU use from AcceleratorOptions. Setting the
    # legacy EasyOcrOptions.use_gpu field emits a deprecation warning.
    assert opts.ocr_options.use_gpu is None
    assert opts.table_structure_options.mode.value == "accurate"
    assert opts.table_structure_options.do_cell_matching is True
    assert opts.enable_remote_services is False
    assert opts.allow_external_plugins is False


def test_docling_default_matches_catalog_without_forcing_full_page(fake_docling_api):
    adapter = fake_docling_api.DoclingAdapter.from_profile(CATALOG["docling_default"])
    opts = adapter.pipeline_options()

    assert opts.do_ocr is True
    assert opts.ocr_options.force_full_page_ocr is False
    assert opts.table_structure_options.do_cell_matching is False


@pytest.mark.parametrize(
    "hardware,expected_public,expected_docling",
    [
        ("cpu", "cpu", FakeDevice.CPU),
        ("gpu", "gpu", FakeDevice.CUDA),
    ],
)
def test_docling_hardware_handshake_uses_official_accelerator_options(
    fake_docling_api, hardware, expected_public, expected_docling
):
    adapter = fake_docling_api.DoclingAdapter.from_profile(CATALOG["docling_scan"])

    assert adapter.configure_hardware(hardware) == expected_public
    opts = adapter.pipeline_options()
    assert opts.accelerator_options.device is expected_docling
    assert opts.ocr_options.use_gpu is None
    assert adapter.config_fingerprint()["hardware"] == expected_public
    assert adapter.config_fingerprint()["device"] == expected_public
    assert type(adapter.config_fingerprint()["hardware_evidence_version"]) is int
    assert adapter.config_fingerprint()["hardware_evidence_version"] == 1


def test_docling_hardware_rejects_unknown_mode(fake_docling_api):
    adapter = fake_docling_api.DoclingAdapter.from_profile(CATALOG["docling_default"])
    with pytest.raises(ValueError, match="cpu.*gpu"):
        adapter.configure_hardware("auto")


def test_docling_result_keeps_adapter_owned_hardware_evidence(fake_docling_api):
    adapter = fake_docling_api.DoclingAdapter.from_profile(CATALOG["docling_scan"])
    adapter.configure_hardware("gpu")
    result = fake_docling_api.build_result(
        FakeDocument(),
        identity=adapter.identity,
        config_fingerprint=adapter.config_fingerprint(),
    )
    assert result.config_fingerprint["hardware"] == "gpu"
    assert result.config_fingerprint["device"] == "gpu"
    assert type(result.config_fingerprint["hardware_evidence_version"]) is int
    assert result.config_fingerprint["hardware_evidence_version"] == 1


@pytest.mark.parametrize("hardware", ["cpu", "gpu"])
def test_docling_execute_failure_keeps_profile_identity_and_hardware_evidence(
    fake_docling_api, monkeypatch, hardware
):
    """A failed profile run remains attributable to the exact configured engine."""
    adapter = fake_docling_api.DoclingAdapter.from_profile(CATALOG["docling_scan"])
    adapter.configure_hardware(hardware)

    def fail(_path: Path):
        raise RuntimeError("engine failed")

    monkeypatch.setattr(adapter, "run", fail)
    result = adapter.execute(Path("broken.pdf"))

    assert result.failed is True
    assert result.failure_kind is FailureKind.ENGINE_ERROR
    assert result.engine == "docling_scan"
    assert result.engine_family == "docling"
    assert result.profile == "scan"
    assert result.config_fingerprint["hardware"] == hardware
    assert result.config_fingerprint["device"] == hardware
    assert type(result.config_fingerprint["hardware_evidence_version"]) is int
    assert result.config_fingerprint["hardware_evidence_version"] == 1


def test_base_package_import_is_lazy_for_docling():
    """Registering the adapter must not import the multi-GB optional engine."""
    code = (
        "import sys; import ocr_bench; "
        "assert not any(n == 'docling' or n.startswith('docling.') for n in sys.modules); "
        "assert 'docling' in ocr_bench.registry.list_adapters()"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr


@pytest.mark.needs_docling
@pytest.mark.slow
def test_docling_real_engine_smoke():
    """Real optional engine: text, canonical pages, hardware evidence, stable raw SHA."""
    if importlib.util.find_spec("docling") is None:
        pytest.skip("chưa cài extra docling[easyocr]==2.91.0")
    module = _docling_module()
    adapter = module.DoclingAdapter.from_profile(CATALOG["docling_default"])
    adapter.configure_hardware("cpu")
    fixture = ROOT / "tests" / "fixtures" / "two_page_layout.pdf"
    if not fixture.exists():
        pytest.skip("thiếu tests/fixtures/two_page_layout.pdf")

    first = adapter.run(fixture)
    second = adapter.run(fixture)
    assert first.text_md and first.text_md.strip()
    assert all(block.box is None or block.box.page >= 0 for block in first.blocks)
    assert first.config_fingerprint["hardware"] == "cpu"
    assert first.config_fingerprint["device"] == "cpu"
    assert first.config_fingerprint["hardware_evidence_version"] == 1
    assert first.raw_artifacts[0].sha256 == second.raw_artifacts[0].sha256
