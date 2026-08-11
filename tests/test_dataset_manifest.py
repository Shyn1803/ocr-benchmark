"""Test cho `dataset_manifest.py` — Task 7.

Manifest trả lời một câu hỏi mà bảng xếp hạng không tự trả lời được: **con số này
đo trên tài liệu nào, lấy ở đâu, ai cho phép dùng, và file đó có còn nguyên không.**
Nên phần lớn test ở đây là test *từ chối*: dataset chưa xác minh license không được
vào bảng chính, correction chưa đủ reviewer không được áp, và snapshot lệch checksum
phải nổ chứ không được âm thầm áp lên nhãn đã đổi.

Nhóm dựng tay chạy trên `tmp_path` nên xanh trên máy trắng; nhóm `needs_corpus` chạy
trên 204+1403 file thật.
"""

from __future__ import annotations

import json
import re

import pytest

from ocr_bench.dataset_manifest import (
    SCHEMA_VERSION,
    CorrectionError,
    DatasetManifestError,
    build_manifest,
    load_corrections,
    validate_catalog_entry,
)

# --------------------------------------------------------------- dữ liệu dựng tay

PDF_BYTES = b"%PDF-1.4\n% mot file gia de bam checksum\n"


def _entry(**over):
    e = {
        "name": "demo",
        "status": "included",
        "version": "v1.0",
        "source_url": "https://example.org/demo",
        "license": "CDLA-Permissive-1.0",
        "license_url": "https://example.org/license",
        "commercial_use": "allowed",
        "languages": ["en"],
        "annotation_kind": "layout_coco",
    }
    e.update(over)
    return e


def _dung_bo_mau(root):
    """Một dataset `demo` gồm 2 PDF + 1 file nhãn JSONL, đủ để build manifest."""
    (root / "datasets").mkdir(parents=True)
    pdfs = root / "pdfs" / "demo" / "mix"
    gt = root / "ground-truth" / "demo"
    pdfs.mkdir(parents=True)
    gt.mkdir(parents=True)
    for ten in ("alpha", "beta"):
        (pdfs / f"{ten}.pdf").write_bytes(PDF_BYTES + ten.encode())
    (gt / "demo.jsonl").write_text(
        "\n".join(
            json.dumps({"pdf": f"mix/{t}.pdf", "type": loai, "page": 1})
            for t, loai in (("alpha", "present"), ("beta", "order"))
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "datasets" / "catalog.json").write_text(
        json.dumps(
            {
                "schema_version": SCHEMA_VERSION,
                "datasets": [
                    _entry(
                        name="demo",
                        pdf_dir="pdfs/demo",
                        annotation_dir="ground-truth/demo",
                        annotation_kind="olmocr_assertions",
                        scan_category_source="dataset_split",
                        splits={"mix": "digital"},
                    )
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return root


# ------------------------------------------------------------------- catalog gate


def test_unverified_dataset_cannot_be_included():
    with pytest.raises(DatasetManifestError, match="license"):
        validate_catalog_entry(_entry(license=None))


def test_included_dataset_needs_public_https_source():
    with pytest.raises(DatasetManifestError, match="source_url"):
        validate_catalog_entry(_entry(source_url="file:///D:/local/copy"))


def test_candidate_dataset_needs_a_reason_but_not_a_license():
    """Chưa xác minh license thì được ghi nhận là candidate — không được ghi là dữ liệu."""
    entry = validate_catalog_entry(
        _entry(status="candidate", license=None, reason="license chưa rà soát")
    )
    assert entry["status"] == "candidate"
    with pytest.raises(DatasetManifestError, match="reason"):
        validate_catalog_entry(_entry(status="candidate", license=None))


def test_unknown_status_is_rejected():
    with pytest.raises(DatasetManifestError, match="status"):
        validate_catalog_entry(_entry(status="maybe"))


# ------------------------------------------------------------------ manifest rows


def test_every_included_document_has_reproducible_provenance(tmp_path):
    manifest = build_manifest(_dung_bo_mau(tmp_path))
    assert manifest["schema_version"] == SCHEMA_VERSION
    assert manifest["documents"]
    for row in manifest["documents"]:
        assert row["source_url"].startswith("https://")
        assert row["source_version"]
        assert row["source_license"]
        assert re.fullmatch(r"[0-9a-f]{64}", row["pdf_sha256"])
        assert re.fullmatch(r"[0-9a-f]{64}", row["annotation_sha256"])
        assert any(row["annotations"].values())
        assert row["language"]
        assert row["document_type"]
        assert row["scan_category"]


def test_documents_are_sorted_and_manifest_is_deterministic(tmp_path):
    root = _dung_bo_mau(tmp_path)
    a = build_manifest(root)
    b = build_manifest(root)
    assert a == b
    ids = [r["document_id"] for r in a["documents"]]
    assert ids == sorted(ids)


def test_annotation_capability_flags_come_from_the_labels_present(tmp_path):
    """Flag là *quan sát* trên nhãn thật, không phải lời khai ở cấp dataset.

    Gán cứng theo dataset sẽ hứa reading-order cho tài liệu chỉ có khẳng định
    `present`, và metric đọc flag đó sẽ chấm 0 thay vì `NO_GROUND_TRUTH`.
    """
    rows = {r["document_id"]: r for r in build_manifest(_dung_bo_mau(tmp_path))["documents"]}
    assert rows["alpha"]["annotations"]["text_presence"] is True
    assert rows["alpha"]["annotations"]["reading_order"] is False
    assert rows["beta"]["annotations"]["reading_order"] is True
    assert rows["beta"]["annotations"]["text_presence"] is False


def test_document_without_any_annotation_is_excluded_with_reason(tmp_path):
    root = _dung_bo_mau(tmp_path)
    (root / "pdfs" / "demo" / "mix" / "gamma.pdf").write_bytes(PDF_BYTES + b"gamma")
    manifest = build_manifest(root)
    assert "gamma" not in {r["document_id"] for r in manifest["documents"]}
    bo = {r["document_id"]: r for r in manifest["excluded_documents"]}
    assert bo["gamma"]["reason"] == "no_annotation"


def test_candidate_dataset_never_produces_documents(tmp_path):
    root = _dung_bo_mau(tmp_path)
    path = root / "datasets" / "catalog.json"
    cat = json.loads(path.read_text(encoding="utf-8"))
    cat["datasets"][0].update(status="candidate", license=None, reason="chưa rà soát")
    path.write_text(json.dumps(cat, ensure_ascii=False), encoding="utf-8")

    manifest = build_manifest(root)
    assert manifest["documents"] == []
    assert manifest["datasets"][0]["status"] == "candidate"


def test_manifest_records_missing_vietnamese_transcript_coverage(tmp_path):
    """Không có nguồn tiếng Việt thì manifest phải *nói ra*, không im lặng.

    Im lặng ở đây biến "chưa đo được tiếng Việt" thành "đã đo và không có gì bất
    thường" — đúng kiểu kết luận mà báo cáo này không được phép ngụ ý.
    """
    manifest = build_manifest(_dung_bo_mau(tmp_path))
    assert manifest["coverage"]["vietnamese_transcript"] == "absent"
    assert manifest["coverage"]["languages"] == ["en"]


# ------------------------------------------------------------ correction overlay


def _correction(**over):
    c = {
        "document_id": "alpha",
        "operation": "add_block",
        "item": {"block_type": "PICTURE", "box": [0.1, 0.1, 0.2, 0.2]},
        "evidence": ["PDF page 0 có XObject /Image1 tại đúng hộp này"],
        "reviewer_count": 2,
        "source_snapshot_sha256": "a" * 64,
    }
    c.update(over)
    return c


def _viet_corrections(tmp_path, *records):
    p = tmp_path / "corrections.jsonl"
    p.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8"
    )
    return p


def test_correction_needs_two_reviewers(tmp_path):
    with pytest.raises(CorrectionError, match="reviewer_count"):
        load_corrections(_viet_corrections(tmp_path, _correction(reviewer_count=1)))


def test_correction_needs_evidence(tmp_path):
    with pytest.raises(CorrectionError, match="evidence"):
        load_corrections(_viet_corrections(tmp_path, _correction(evidence=[])))


def test_correction_needs_source_snapshot(tmp_path):
    with pytest.raises(CorrectionError, match="source_snapshot_sha256"):
        load_corrections(_viet_corrections(tmp_path, _correction(source_snapshot_sha256="")))


def test_correction_is_rejected_when_the_labels_moved_underneath_it(tmp_path):
    """Nhãn nguồn đổi thì correction phải dừng, không được áp mù.

    Overlay được viết dựa trên một ảnh chụp cụ thể của bộ nhãn. Nguồn đổi mà overlay
    vẫn áp thì nó sửa một thứ khác với thứ reviewer đã đọc.
    """
    corrections = load_corrections(_viet_corrections(tmp_path, _correction()))
    with pytest.raises(CorrectionError, match="snapshot"):
        corrections.verify_snapshot("b" * 64)
    corrections.verify_snapshot("a" * 64)


def test_empty_correction_file_is_valid(tmp_path):
    corrections = load_corrections(_viet_corrections(tmp_path))
    assert corrections.records == ()
    corrections.verify_snapshot("c" * 64)


def test_duplicate_correction_is_rejected(tmp_path):
    with pytest.raises(CorrectionError, match="trùng"):
        load_corrections(_viet_corrections(tmp_path, _correction(), _correction()))


# -------------------------------------------------------------- bộ mẫu thật trên đĩa


@pytest.mark.needs_corpus
def test_real_corpus_manifest_covers_both_included_datasets():
    from ocr_bench.corpus import ROOT

    manifest = build_manifest(ROOT)
    ten = {d["name"] for d in manifest["datasets"] if d["status"] == "included"}
    assert ten == {"doclaynet", "olmocr-bench"}

    theo_bo = {}
    for row in manifest["documents"]:
        theo_bo.setdefault(row["dataset"], []).append(row)
    # 204 PDF trên đĩa nhưng **203** dòng có nhãn. Trang còn lại
    # (`7e1cd102…`, trang 504/506 của một sổ tay IBM) trắng thật: 0 hộp bố cục và 0
    # text cell. Nhãn của nó đúng — "không có gì" — nhưng recall bố cục chia cho 0 nên
    # không chấm được. Kéo nó vào bảng thì engine nào im lặng cũng nhận 0.0 cho một
    # trang mà im lặng mới là câu trả lời đúng.
    assert len(theo_bo["doclaynet"]) == 203
    assert theo_bo["olmocr-bench"]
    bo = {r["document_id"]: r["reason"] for r in manifest["excluded_documents"]}
    assert bo == {"7e1cd102c287adb1b34f17a6ab9fedec1ecf77b09ac37d7c4add2fb9c3a287b6": "blank_page"}

    for row in manifest["documents"]:
        assert re.fullmatch(r"[0-9a-f]{64}", row["pdf_sha256"])
        assert re.fullmatch(r"[0-9a-f]{64}", row["annotation_sha256"])
        assert any(row["annotations"].values())


@pytest.mark.needs_corpus
def test_real_corpus_has_no_vietnamese_transcript_source():
    """Bảng tiếng Việt phải là `N/A` có lý do, không phải điểm 0."""
    from ocr_bench.corpus import ROOT

    manifest = build_manifest(ROOT)
    assert manifest["coverage"]["vietnamese_transcript"] == "absent"
