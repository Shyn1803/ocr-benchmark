"""Publication profile catalog contracts."""

from __future__ import annotations

from pathlib import Path

import pytest

import ocr_bench
from ocr_bench.profiles import ProfileConfigError, load_profile_catalog


ROOT = Path(__file__).resolve().parents[1]


def test_package_exports_profile_catalog_api():
    """A public catalog API avoids publication callers depending on internals."""
    assert ocr_bench.EngineProfile.__name__ == "EngineProfile"
    assert ocr_bench.ProfileConfigError.__name__ == "ProfileConfigError"
    assert ocr_bench.load_profile_catalog is load_profile_catalog


def test_publication_profiles_are_exact_and_unique():
    """Removing or renaming a published profile breaks reproducible comparisons."""
    catalog = load_profile_catalog(ROOT / "configs" / "profiles.json")

    assert set(catalog) == {
        "docling_default", "docling_scan",
        "opendataloader_default", "opendataloader_scan",
        "marker_default", "marker_scan",
        "sovereign_default", "sovereign_scan",
    }
    assert all(
        profile.family in {"docling", "opendataloader", "marker", "sovereign"}
        for profile in catalog.values()
    )
    assert all(profile.profile in {"default", "scan"} for profile in catalog.values())

    assert catalog["docling_default"].config == {
        "do_ocr": True,
        "ocr_engine": "easyocr",
        "force_full_page_ocr": False,
        "table_mode": "default",
        "cell_matching": False,
    }
    assert catalog["docling_scan"].config == {
        "do_ocr": True,
        "ocr_engine": "easyocr",
        "ocr_languages": ["vi", "en"],
        "force_full_page_ocr": True,
        "table_mode": "accurate",
        "cell_matching": True,
    }
    assert catalog["opendataloader_default"].config == {
        "parser": "java",
        "table_method": "cluster",
        "reading_order": "xycut",
    }
    assert catalog["opendataloader_scan"].config == {
        "hybrid": "docling-fast",
        "hybrid_mode": "full",
        "hybrid_fallback": False,
    }
    assert catalog["opendataloader_scan"].environment == {
        "hybrid_server": {
            "host": "127.0.0.1",
            "port": 5002,
            "force_ocr": True,
            "ocr_engine": "easyocr",
            "ocr_languages": ["vi", "en"],
        }
    }
    assert catalog["marker_default"].config == {
        "force_ocr": False,
        "use_llm": False,
    }
    assert catalog["marker_scan"].config == {
        "force_ocr": True,
        "use_llm": False,
    }
    assert catalog["sovereign_default"].environment == {"marker_available": False}
    assert catalog["sovereign_scan"].environment == {"marker_available": True}
    assert all(
        profile.config["ocr_use_vision_api"] is False
        and profile.config["api_enabled"] is False
        for profile in (catalog["sovereign_default"], catalog["sovereign_scan"])
    )


def test_duplicate_profile_name_is_rejected(tmp_path):
    """A duplicate profile name would silently replace a publication configuration."""
    path = tmp_path / "profiles.json"
    path.write_text(
        '{"profiles": ['
        '{"name": "same", "family": "marker", "profile": "default", '
        '"adapter": "marker", "config": {}, "environment": {}}, '
        '{"name": "same", "family": "marker", "profile": "scan", '
        '"adapter": "marker", "config": {}, "environment": {}}]}',
        encoding="utf-8",
    )

    with pytest.raises(ProfileConfigError, match="trùng tên profile"):
        load_profile_catalog(path)
