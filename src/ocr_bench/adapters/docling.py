"""Lazy Docling 2.91 adapter for the frozen default and scan profiles.

Docling is an optional, heavy dependency.  This module deliberately imports no
``docling`` or ``docling_core`` module at import time so the base/dev install can
still import :mod:`ocr_bench` and collect its unit tests.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from types import SimpleNamespace
from typing import Any, ClassVar, Literal

from ocr_bench.adapters.base import Adapter, AdapterOutputError
from ocr_bench.profiles import EngineProfile, ProfileConfigError
from ocr_bench.types import (
    Box,
    BlockType,
    Capability,
    OcrBlock,
    OcrResult,
    OcrTable,
    RawArtifact,
)

__all__ = [
    "DEFAULT_IDENTITY",
    "SCAN_IDENTITY",
    "DoclingAdapter",
    "DoclingIdentity",
    "build_result",
]


_DEFAULT_CONFIG: dict[str, object] = {
    "do_ocr": True,
    "ocr_engine": "easyocr",
    "force_full_page_ocr": False,
    "table_mode": "default",
    "cell_matching": False,
}
_SCAN_CONFIG: dict[str, object] = {
    "do_ocr": True,
    "ocr_engine": "easyocr",
    "ocr_languages": ["vi", "en"],
    "force_full_page_ocr": True,
    "table_mode": "accurate",
    "cell_matching": True,
}


@dataclass(frozen=True, slots=True)
class DoclingIdentity:
    """Publication identity retained separately from Docling runtime objects."""

    name: Literal["docling_default", "docling_scan"]
    engine_family: Literal["docling"]
    profile: Literal["default", "scan"]
    config: Mapping[str, object]
    profile_config_sha256: str


def _literal_config(config: Mapping[str, object]) -> dict[str, object]:
    return {
        key: list(value) if isinstance(value, tuple) else value
        for key, value in config.items()
    }


def _make_identity(
    *,
    name: Literal["docling_default", "docling_scan"],
    profile: Literal["default", "scan"],
    config: Mapping[str, object],
) -> DoclingIdentity:
    engine_profile = EngineProfile(
        name=name,
        family="docling",
        profile=profile,
        adapter="docling",
        config=config,
        environment={},
    )
    return DoclingIdentity(
        name=name,
        engine_family="docling",
        profile=profile,
        config=engine_profile.config,
        profile_config_sha256=engine_profile.fingerprint,
    )


DEFAULT_IDENTITY = _make_identity(
    name="docling_default", profile="default", config=_DEFAULT_CONFIG
)
SCAN_IDENTITY = _make_identity(
    name="docling_scan", profile="scan", config=_SCAN_CONFIG
)


_LABEL_MAP: dict[str, BlockType] = {
    "caption": BlockType.CAPTION,
    "code": BlockType.CODE,
    "footnote": BlockType.FOOTNOTE,
    "formula": BlockType.FORMULA,
    "list_item": BlockType.LIST,
    "page_footer": BlockType.PAGE_FOOTER,
    "page_header": BlockType.PAGE_HEADER,
    "picture": BlockType.PICTURE,
    "chart": BlockType.PICTURE,
    "section_header": BlockType.HEADING,
    "table": BlockType.TABLE,
    "document_index": BlockType.TABLE,
    "text": BlockType.TEXT,
    "paragraph": BlockType.TEXT,
    "reference": BlockType.TEXT,
    "handwritten_text": BlockType.TEXT,
    "title": BlockType.TITLE,
}


def _canonical_json_bytes(value: object, *, label: str) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (OverflowError, TypeError, ValueError) as exc:
        raise AdapterOutputError(f"Docling {label} không JSON hoá được") from exc


def _collect_self_refs(value: object) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, Mapping):
        self_ref = value.get("self_ref")
        if isinstance(self_ref, str):
            refs.add(self_ref)
        for nested in value.values():
            refs.update(_collect_self_refs(nested))
    elif isinstance(value, (list, tuple)):
        for nested in value:
            refs.update(_collect_self_refs(nested))
    return refs


def _page_dimensions(document: Any) -> tuple[dict[int, tuple[float, float]], tuple[tuple[float, float], ...]]:
    pages = getattr(document, "pages", None)
    if not isinstance(pages, Mapping) or not pages:
        raise AdapterOutputError("Docling output thiếu pages")

    dimensions: dict[int, tuple[float, float]] = {}
    for key, page in pages.items():
        try:
            page_no = int(getattr(page, "page_no", key))
            size = page.size
            width = float(size.width)
            height = float(size.height)
        except (AttributeError, TypeError, ValueError) as exc:
            raise AdapterOutputError(f"Docling page {key!r} thiếu kích thước") from exc
        if page_no < 1 or width <= 0 or height <= 0:
            raise AdapterOutputError(
                f"Docling page {page_no} có kích thước không hợp lệ {width}x{height}"
            )
        if page_no in dimensions:
            raise AdapterOutputError(f"Docling output trùng page {page_no}")
        dimensions[page_no] = (width, height)

    expected = list(range(1, len(dimensions) + 1))
    if sorted(dimensions) != expected:
        raise AdapterOutputError(
            f"Docling pages phải liên tục 1-based, nhận {sorted(dimensions)}"
        )
    ordered = tuple(dimensions[page_no] for page_no in expected)
    return dimensions, ordered


def _item_box(item: Any, dimensions: Mapping[int, tuple[float, float]]) -> Box:
    prov = getattr(item, "prov", None)
    if not isinstance(prov, (list, tuple)) or not prov:
        raise AdapterOutputError(
            f"Docling item {getattr(item, 'self_ref', '<unknown>')} thiếu provenance"
        )
    try:
        item_prov = prov[0]
        page_no = int(item_prov.page_no)
        page_width, page_height = dimensions[page_no]
        bbox = item_prov.bbox.to_top_left_origin(page_height=page_height)
        return Box.from_absolute(
            page=page_no - 1,
            x0=float(bbox.l),
            y0=float(bbox.t),
            x1=float(bbox.r),
            y1=float(bbox.b),
            page_width=page_width,
            page_height=page_height,
            y_axis="down",
        )
    except AdapterOutputError:
        raise
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise AdapterOutputError(
            f"Docling item {getattr(item, 'self_ref', '<unknown>')} có provenance/bbox lỗi"
        ) from exc


def _default_fingerprint(
    identity: DoclingIdentity, engine_version: str
) -> dict[str, object]:
    return {
        **_literal_config(identity.config),
        "docling_version": engine_version,
        "profile_config_sha256": identity.profile_config_sha256,
        "hardware": "cpu",
        "device": "cpu",
        "hardware_evidence_version": 1,
        "docling_accelerator_device": "cpu",
    }


def build_result(
    document: Any,
    *,
    identity: DoclingIdentity,
    engine_version: str = "2.91.0",
    doc_id: str = "document",
    config_fingerprint: Mapping[str, object] | None = None,
) -> OcrResult:
    """Normalize one ``DoclingDocument`` without importing the optional package."""
    dimensions, page_sizes = _page_dimensions(document)
    try:
        raw = document.export_to_dict()
        markdown = document.export_to_markdown()
        items = list(document.iterate_items())
    except (AttributeError, TypeError, ValueError) as exc:
        raise AdapterOutputError("Docling document output không đúng contract") from exc

    raw_bytes = _canonical_json_bytes(raw, label="raw output JSON")
    if not isinstance(markdown, str):
        raise AdapterOutputError("Docling markdown không phải chuỗi")

    blocks: list[OcrBlock] = []
    tables: list[OcrTable] = []
    block_refs: dict[str, str] = {}
    table_refs: dict[str, str] = {}
    raw_refs = _collect_self_refs(raw)

    for pair in items:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise AdapterOutputError("Docling iterate_items() trả item lỗi")
        item, _tree_level = pair
        self_ref = getattr(item, "self_ref", None)
        if not isinstance(self_ref, str) or not self_ref:
            raise AdapterOutputError("Docling item thiếu self_ref")
        if self_ref not in raw_refs:
            raise AdapterOutputError(
                f"Docling item {self_ref} không truy ngược được trong raw output"
            )

        label_obj = getattr(item, "label", "other")
        label = str(getattr(label_obj, "value", label_obj))
        block_type = _LABEL_MAP.get(label, BlockType.OTHER)
        box = _item_box(item, dimensions)
        text = getattr(item, "text", None)
        if text is not None and not isinstance(text, str):
            raise AdapterOutputError(f"Docling item {self_ref} có text không phải chuỗi")

        html: str | None = None
        if block_type is BlockType.TABLE:
            try:
                html = item.export_to_html(doc=document, add_caption=False)
                n_rows = int(item.data.num_rows)
                n_cols = int(item.data.num_cols)
            except (AttributeError, RuntimeError, TypeError, ValueError) as exc:
                raise AdapterOutputError(f"Docling table {self_ref} bị lỗi") from exc
            if not isinstance(html, str) or not html.lstrip().startswith("<table"):
                raise AdapterOutputError(f"Docling table {self_ref} không trả HTML table")
            tables.append(
                OcrTable(html=html, box=box, n_rows=n_rows, n_cols=n_cols)
            )
            table_refs[str(len(tables) - 1)] = self_ref

        level: int | None = None
        if block_type in {BlockType.HEADING, BlockType.TITLE}:
            raw_level = 1 if block_type is BlockType.TITLE else getattr(item, "level", None)
            if raw_level is not None:
                try:
                    level = int(raw_level)
                except (TypeError, ValueError) as exc:
                    raise AdapterOutputError(
                        f"Docling heading {self_ref} có level lỗi"
                    ) from exc

        blocks.append(
            OcrBlock(
                block_type=block_type,
                box=box,
                text=text,
                html=html,
                level=level,
            )
        )
        block_refs[str(len(blocks) - 1)] = self_ref

    trace = {
        "blocks": block_refs,
        "schema_version": 1,
        "tables": table_refs,
    }
    trace_bytes = _canonical_json_bytes(trace, label="trace map JSON")
    fingerprint = dict(
        config_fingerprint
        if config_fingerprint is not None
        else _default_fingerprint(identity, engine_version)
    )

    return OcrResult(
        engine=identity.name,
        engine_family=identity.engine_family,
        profile=identity.profile,
        engine_version=engine_version,
        doc_id=doc_id,
        capabilities=DoclingAdapter.capabilities,
        text_md=markdown,
        raw_artifacts=(
            RawArtifact("docling.json", "application/json", raw_bytes),
            RawArtifact("docling-map.json", "application/json", trace_bytes),
        ),
        blocks=tuple(blocks),
        tables=tuple(tables),
        page_sizes=page_sizes,
        config_fingerprint=fingerprint,
    )


def _load_docling_api() -> SimpleNamespace:
    """Import only when options/conversion are actually requested."""
    from docling.datamodel.accelerator_options import (
        AcceleratorDevice,
        AcceleratorOptions,
    )
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import (
        EasyOcrOptions,
        PdfPipelineOptions,
        TableFormerMode,
        TableStructureOptions,
    )
    from docling.document_converter import DocumentConverter, PdfFormatOption

    return SimpleNamespace(
        AcceleratorDevice=AcceleratorDevice,
        AcceleratorOptions=AcceleratorOptions,
        DocumentConverter=DocumentConverter,
        EasyOcrOptions=EasyOcrOptions,
        InputFormat=InputFormat,
        PdfFormatOption=PdfFormatOption,
        PdfPipelineOptions=PdfPipelineOptions,
        TableFormerMode=TableFormerMode,
        TableStructureOptions=TableStructureOptions,
    )


class DoclingAdapter(Adapter):
    """Docling profile adapter with explicit CPU/CUDA selection."""

    name: ClassVar[str] = "docling"
    capabilities: ClassVar[frozenset[Capability]] = frozenset(
        {
            Capability.TEXT_MD,
            Capability.BLOCK_BBOX,
            Capability.TABLE_HTML,
            Capability.HEADING_LEVEL,
        }
    )

    def __init__(self, identity: DoclingIdentity = DEFAULT_IDENTITY) -> None:
        self.identity = identity
        self.name = identity.name
        self.engine_family = identity.engine_family
        self.profile = identity.profile
        self._hardware: Literal["cpu", "gpu"] = "cpu"
        self._converter: Any = None

    @classmethod
    def from_profile(cls, profile: EngineProfile) -> "DoclingAdapter":
        if profile.adapter != "docling" or profile.family != "docling":
            raise ProfileConfigError(
                f"DoclingAdapter không nhận profile {profile.name!r}/{profile.family!r}"
            )
        expected = {
            "docling_default": DEFAULT_IDENTITY,
            "docling_scan": SCAN_IDENTITY,
        }.get(profile.name)
        if expected is None or profile.profile != expected.profile:
            raise ProfileConfigError(f"profile Docling không hỗ trợ: {profile.name!r}")
        if _literal_config(profile.config) != _literal_config(expected.config):
            raise ProfileConfigError(
                f"{profile.name}: config không khớp catalog Docling đã khóa"
            )
        if profile.environment:
            raise ProfileConfigError(
                f"{profile.name}: environment phải rỗng theo catalog Docling đã khóa"
            )
        identity = DoclingIdentity(
            name=expected.name,
            engine_family="docling",
            profile=expected.profile,
            config=profile.config,
            profile_config_sha256=profile.fingerprint,
        )
        return cls(identity)

    def configure_hardware(self, hardware: str) -> str:
        if hardware not in {"cpu", "gpu"}:
            raise ValueError("Docling hardware phải là 'cpu' hoặc 'gpu'")
        self._hardware = hardware
        self._converter = None
        return hardware

    @staticmethod
    def _docling_version() -> str:
        try:
            return version("docling")
        except PackageNotFoundError:
            return "not-installed"

    def version(self) -> str:
        return self._docling_version()

    def config_fingerprint(self) -> dict[str, object]:
        accelerator_device = "cuda" if self._hardware == "gpu" else "cpu"
        return {
            **_literal_config(self.identity.config),
            "docling_version": self.version(),
            "profile_config_sha256": self.identity.profile_config_sha256,
            "hardware": self._hardware,
            "device": self._hardware,
            "hardware_evidence_version": 1,
            "docling_accelerator_device": accelerator_device,
            "enable_remote_services": False,
            "allow_external_plugins": False,
        }

    def pipeline_options(self) -> Any:
        api = _load_docling_api()
        device = (
            api.AcceleratorDevice.CUDA
            if self._hardware == "gpu"
            else api.AcceleratorDevice.CPU
        )
        accelerator = api.AcceleratorOptions(device=device)
        config = _literal_config(self.identity.config)
        ocr_kwargs: dict[str, object] = {
            "force_full_page_ocr": bool(config["force_full_page_ocr"]),
        }
        if "ocr_languages" in config:
            ocr_kwargs["lang"] = config["ocr_languages"]
        ocr_options = api.EasyOcrOptions(**ocr_kwargs)
        if self.profile == "scan":
            table_options = api.TableStructureOptions(
                mode=api.TableFormerMode.ACCURATE,
                do_cell_matching=True,
            )
        else:
            table_options = api.TableStructureOptions(do_cell_matching=False)
        return api.PdfPipelineOptions(
            do_ocr=True,
            ocr_options=ocr_options,
            table_structure_options=table_options,
            accelerator_options=accelerator,
            enable_remote_services=False,
            allow_external_plugins=False,
        )

    def converter(self) -> Any:
        if self._converter is None:
            api = _load_docling_api()
            options = self.pipeline_options()
            self._converter = api.DocumentConverter(
                allowed_formats=[api.InputFormat.PDF],
                format_options={
                    api.InputFormat.PDF: api.PdfFormatOption(
                        pipeline_options=options
                    )
                },
            )
        return self._converter

    def run(self, doc_path: Path) -> OcrResult:
        converted = self.converter().convert(doc_path)
        return build_result(
            converted.document,
            identity=self.identity,
            engine_version=self.version(),
            doc_id=doc_path.stem,
            config_fingerprint=self.config_fingerprint(),
        )
