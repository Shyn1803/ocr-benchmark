"""Publication profile catalog contracts."""

from __future__ import annotations

from pathlib import Path

import pytest

import ocr_bench
from ocr_bench.profiles import EngineProfile, ProfileConfigError, load_profile_catalog


ROOT = Path(__file__).resolve().parents[1]


def test_package_exports_profile_catalog_api():
    """A public catalog API avoids publication callers depending on internals."""
    assert ocr_bench.EngineProfile.__name__ == "EngineProfile"
    assert ocr_bench.ProfileConfigError.__name__ == "ProfileConfigError"
    assert ocr_bench.load_profile_catalog is load_profile_catalog


def test_profile_fingerprint_is_stable_for_equivalent_key_order():
    """Changing JSON key order must not create a distinct publication profile."""
    first = EngineProfile(
        name="marker_scan",
        family="marker",
        profile="scan",
        adapter="marker",
        config={"force_ocr": True, "options": {"languages": ["vi", "en"]}},
        environment={"runner": {"host": "127.0.0.1", "port": 5002}},
    )
    reordered = EngineProfile(
        name="marker_scan",
        family="marker",
        profile="scan",
        adapter="marker",
        config={"options": {"languages": ["vi", "en"]}, "force_ocr": True},
        environment={"runner": {"port": 5002, "host": "127.0.0.1"}},
    )

    assert first.fingerprint == reordered.fingerprint
    assert len(first.fingerprint) == 64


def test_profile_fingerprint_changes_for_every_configured_value():
    """Colliding config or environment values would merge distinct runs."""
    baseline = EngineProfile(
        name="marker_scan",
        family="marker",
        profile="scan",
        adapter="marker",
        config={"force_ocr": True, "access_token": "first"},
        environment={"runner": {"host": "127.0.0.1"}},
    )
    changed_config = EngineProfile(
        name="marker_scan",
        family="marker",
        profile="scan",
        adapter="marker",
        config={"force_ocr": False, "access_token": "first"},
        environment={"runner": {"host": "127.0.0.1"}},
    )
    changed_environment = EngineProfile(
        name="marker_scan",
        family="marker",
        profile="scan",
        adapter="marker",
        config={"force_ocr": True, "access_token": "first"},
        environment={"runner": {"host": "127.0.0.2"}},
    )
    changed_token_named_value = EngineProfile(
        name="marker_scan",
        family="marker",
        profile="scan",
        adapter="marker",
        config={"force_ocr": True, "access_token": "second"},
        environment={"runner": {"host": "127.0.0.1"}},
    )

    assert changed_config.fingerprint != baseline.fingerprint
    assert changed_environment.fingerprint != baseline.fingerprint
    assert changed_token_named_value.fingerprint != baseline.fingerprint


def test_loaded_profile_json_is_deeply_immutable():
    """Mutating nested profile data would invalidate its recorded fingerprint."""
    profile = load_profile_catalog(ROOT / "configs" / "profiles.json")[
        "opendataloader_scan"
    ]
    hybrid = profile.environment["hybrid_server"]

    with pytest.raises(TypeError):
        profile.config["hybrid_mode"] = "partial"  # type: ignore[index]
    with pytest.raises(TypeError):
        hybrid["host"] = "0.0.0.0"  # type: ignore[index]
    with pytest.raises(AttributeError):
        hybrid["ocr_languages"].append("fr")  # type: ignore[union-attr]


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
        "ocr_languages": ("vi", "en"),
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
            "ocr_languages": ("vi", "en"),
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
