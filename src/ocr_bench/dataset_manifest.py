"""Xuất xứ bộ dữ liệu — Task 7.

Bảng xếp hạng nói *engine nào hơn*. Nó không nói **đo trên tài liệu nào, lấy từ đâu,
ai cho phép dùng, và file lúc đo có còn giống file hôm nay không**. Module này trả lời
bốn câu đó, mỗi tài liệu một dòng, sinh ra từ đĩa chứ không viết tay.

Ba cổng chặn, đều fail-closed:

1. **License.** Bộ nào chưa xác minh được giấy phép thì `status: candidate` kèm lý do —
   nó xuất hiện trong báo cáo như một hạn chế, không xuất hiện trong bảng như một con số.
2. **Nhãn thật.** Cờ năng lực (`reading_order`, `table_structure`, …) suy ra từ **khẳng
   định có thật trên từng tài liệu**, không lấy từ lời khai ở cấp bộ. Khai thừa một cờ
   thì metric tương ứng chấm 0 cho tài liệu vốn không có nhãn — biến "chưa đo được"
   thành "engine làm sai", đúng loại sai lệch mà cả kế hoạch này đang cố tránh.
3. **Checksum.** Mỗi dòng mang SHA-256 của PDF và của nguồn nhãn. Overlay sửa nhãn chỉ
   được áp sau khi ảnh chụp nguồn khớp — nguồn đổi mà overlay vẫn áp thì nó đang sửa
   một thứ khác với thứ reviewer đã đọc.

`datasets/manifest.json` là **đầu ra**, sinh bằng `scripts/build_dataset_manifest.py`.
Đừng sửa tay: sửa tay được thì cổng checksum mất tác dụng.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

__all__ = [
    "SCHEMA_VERSION",
    "ANNOTATION_FLAGS",
    "DatasetManifestError",
    "CorrectionError",
    "Corrections",
    "validate_catalog_entry",
    "load_catalog",
    "load_corrections",
    "build_manifest",
]

SCHEMA_VERSION = 1

#: Tập cờ năng lực **cố định**. Cố định vì bảng cần cột như nhau cho mọi tài liệu:
#: thiếu khoá và `False` là hai chuyện khác nhau, và code đọc manifest không nên phải
#: đoán cái nào đang xảy ra.
ANNOTATION_FLAGS = (
    "layout_blocks",
    "image_regions",
    "table_region",
    "table_structure",
    "text_presence",
    "text_absence",
    "reading_order",
    "math_formula",
    "baseline",
)

TRANG_THAI = ("included", "candidate", "excluded")

#: Loại khẳng định olmOCR → cờ năng lực. Loại lạ sẽ bị ném ở `_co_nang_luc`, không
#: bị bỏ qua: nhãn thượng nguồn thêm loại mới mà manifest im lặng thì tài liệu đó
#: mang cờ thiếu và metric mới sẽ không bao giờ tìm thấy nó.
KHANG_DINH_FLAG = {
    "present": "text_presence",
    "absent": "text_absence",
    "order": "reading_order",
    "math": "math_formula",
    "table": "table_structure",
    "baseline": "baseline",
}

TEN_FILE_CATALOG = "catalog.json"
TEN_FILE_CORRECTIONS = "corrections.jsonl"

_SHA_RONG = hashlib.sha256(b"").hexdigest()


class DatasetManifestError(RuntimeError):
    """Catalog hoặc bộ mẫu trên đĩa không đủ điều kiện để sinh manifest."""


class CorrectionError(RuntimeError):
    """Overlay sửa nhãn không đạt cổng bằng chứng/reviewer/ảnh chụp."""


# ------------------------------------------------------------------------ tiện ích


def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


def _sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _la_sha(s: Any) -> bool:
    return isinstance(s, str) and len(s) == 64 and all(c in "0123456789abcdef" for c in s)


# ------------------------------------------------------------------ cổng 1: catalog


def validate_catalog_entry(entry: Mapping[str, Any]) -> dict[str, Any]:
    """Kiểm một mục catalog. Trả bản sao đã chuẩn hoá, hoặc ném.

    Thứ tự kiểm là cố ý: danh tính → trạng thái → nguồn → giấy phép → thư mục. Mục
    thiếu giấy phép phải báo *thiếu giấy phép*, không được báo *thiếu `pdf_dir`* —
    thông báo lỗi đầu tiên là thứ người ta đọc, và nó phải trỏ đúng vào rào cản thật.
    """
    e = dict(entry)

    ten = e.get("name")
    if not isinstance(ten, str) or not ten.strip():
        raise DatasetManifestError("mục catalog thiếu `name`")

    status = e.get("status")
    if status not in TRANG_THAI:
        raise DatasetManifestError(
            f"{ten}: `status` {status!r} không hợp lệ (phải là một trong {TRANG_THAI})"
        )

    url = e.get("source_url")
    if not isinstance(url, str) or not url.startswith("https://"):
        raise DatasetManifestError(
            f"{ten}: `source_url` phải là URL https công khai để người khác tải lại "
            f"đúng bộ này, đang là {url!r}"
        )

    if not e.get("version"):
        raise DatasetManifestError(f"{ten}: thiếu `version` — không có version thì không tái lập được")

    if status == "included":
        if not e.get("license"):
            raise DatasetManifestError(
                f"{ten}: `status: included` nhưng thiếu `license`. Bộ chưa xác minh giấy "
                f"phép thì để `candidate` kèm `reason`; nó vào phần hạn chế của báo cáo, "
                f"không vào bảng số."
            )
        for khoa in ("license_url", "commercial_use", "annotation_kind", "pdf_dir", "annotation_dir"):
            if not e.get(khoa):
                raise DatasetManifestError(f"{ten}: `status: included` nhưng thiếu `{khoa}`")
        if not e.get("languages"):
            raise DatasetManifestError(f"{ten}: thiếu `languages`")
    elif not e.get("reason"):
        raise DatasetManifestError(
            f"{ten}: `status: {status}` phải kèm `reason` — người đọc cần biết vì sao "
            f"bộ này không được dùng, nếu không nó trông như bị bỏ quên."
        )

    return e


def load_catalog(root: Path) -> list[dict[str, Any]]:
    p = Path(root) / "datasets" / TEN_FILE_CATALOG
    if not p.exists():
        raise DatasetManifestError(f"thiếu {p}")
    du_lieu = json.loads(p.read_text(encoding="utf-8"))
    if du_lieu.get("schema_version") != SCHEMA_VERSION:
        raise DatasetManifestError(
            f"{p}: schema_version {du_lieu.get('schema_version')!r} ≠ {SCHEMA_VERSION}"
        )
    muc = [validate_catalog_entry(e) for e in du_lieu.get("datasets", ())]
    ten = [m["name"] for m in muc]
    if len(set(ten)) != len(ten):
        raise DatasetManifestError(f"{p}: tên bộ dữ liệu trùng nhau")
    return sorted(muc, key=lambda m: m["name"])


# --------------------------------------------------------------- cổng 2: correction


@dataclass(frozen=True)
class Corrections:
    """Overlay sửa nhãn đã qua cổng, kèm ảnh chụp nguồn mà nó được viết dựa trên.

    Không tự áp: `verify_snapshot` phải được gọi với SHA của nguồn *hiện tại* trước.
    Tách hai bước để chỗ áp overlay buộc phải cầm SHA trong tay — API mà "áp luôn"
    thì không có chỗ nào để quên kiểm, và cũng không có chỗ nào để nhớ.
    """

    records: tuple[dict[str, Any], ...]
    path: Path | None = None

    def verify_snapshot(self, sha_hien_tai: str) -> None:
        for r in self.records:
            if r["source_snapshot_sha256"] != sha_hien_tai:
                raise CorrectionError(
                    f"{self.path}: correction cho {r['document_id']!r} viết trên snapshot "
                    f"{r['source_snapshot_sha256'][:12]}… nhưng nguồn hiện tại là "
                    f"{sha_hien_tai[:12]}…. Nhãn đã đổi dưới chân overlay — người review "
                    f"phải đọc lại trước khi áp."
                )

    def overlay_sha256(self) -> str:
        return _sha_text(_canonical([_canonical(r) for r in self.records]))


def load_corrections(path: Path) -> Corrections:
    """Đọc `corrections.jsonl`. File vắng mặt hoặc rỗng đều hợp lệ.

    Cổng: mỗi mục cần `document_id`, `operation`, `item`, `evidence` không rỗng,
    `reviewer_count >= 2`, và `source_snapshot_sha256`. Hai reviewer vì một mục sửa
    nhãn làm đổi số công bố — một người tự thấy "chỗ này nhãn sai" là giả thuyết,
    không phải bằng chứng.
    """
    p = Path(path)
    if not p.exists():
        return Corrections(records=(), path=p)

    ra: list[dict[str, Any]] = []
    da_thay: set[str] = set()
    for so, dong in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        # Dòng `#` là chú thích. File này thường **rỗng** — và một file rỗng trong repo
        # trông giống hệt một file bị bỏ quên. Cho phép nó tự nói nó rỗng có chủ đích.
        if not dong.strip() or dong.lstrip().startswith("#"):
            continue
        r = json.loads(dong)
        cho = f"{p} dòng {so}"

        for khoa in ("document_id", "operation", "item"):
            if not r.get(khoa):
                raise CorrectionError(f"{cho}: thiếu `{khoa}`")
        if not isinstance(r.get("evidence"), list) or not r["evidence"]:
            raise CorrectionError(
                f"{cho}: thiếu `evidence`. Không có bằng chứng thì không phân biệt được "
                f"sửa nhãn cho đúng với sửa nhãn cho bảng đẹp lên."
            )
        if not isinstance(r.get("reviewer_count"), int) or r["reviewer_count"] < 2:
            raise CorrectionError(
                f"{cho}: `reviewer_count` phải >= 2, đang là {r.get('reviewer_count')!r}"
            )
        if not _la_sha(r.get("source_snapshot_sha256")):
            raise CorrectionError(
                f"{cho}: `source_snapshot_sha256` phải là SHA-256 64 ký tự hex"
            )

        khoa_trung = _canonical([r["document_id"], r["operation"], r["item"]])
        if khoa_trung in da_thay:
            raise CorrectionError(
                f"{cho}: mục sửa trùng với một mục trước đó — áp hai lần sẽ nhân đôi nhãn"
            )
        da_thay.add(khoa_trung)
        ra.append(r)

    return Corrections(records=tuple(ra), path=p)


# ------------------------------------------------------------------ cổng 3: manifest


def _co_nang_luc_rong() -> dict[str, bool]:
    return {k: False for k in ANNOTATION_FLAGS}


def _quet_olmocr(root: Path, e: Mapping[str, Any]) -> tuple[dict, dict, dict]:
    """Trả (cờ theo doc, file nhãn theo doc, split theo doc) từ các file jsonl."""
    gt_dir = root / e["annotation_dir"]
    if not gt_dir.is_dir():
        raise DatasetManifestError(f"{e['name']}: thiếu thư mục nhãn {gt_dir}")

    co: dict[str, dict[str, bool]] = {}
    nguon: dict[str, set[str]] = {}
    split: dict[str, str] = {}
    for f in sorted(gt_dir.glob("*.jsonl")):
        for dong in f.read_text(encoding="utf-8").splitlines():
            if not dong.strip():
                continue
            d = json.loads(dong)
            rel = Path(d["pdf"])
            doc_id = rel.stem
            loai = d.get("type")
            if loai not in KHANG_DINH_FLAG:
                raise DatasetManifestError(
                    f"{f}: loại khẳng định lạ {loai!r}. Nhãn thượng nguồn đã thêm loại "
                    f"mới — bổ sung vào KHANG_DINH_FLAG, đừng bỏ qua im lặng."
                )
            co.setdefault(doc_id, _co_nang_luc_rong())[KHANG_DINH_FLAG[loai]] = True
            nguon.setdefault(doc_id, set()).add(f.name)
            split[doc_id] = rel.parent.name or e["name"]
    return co, nguon, split


def _sha_nhieu_nguon(gt_dir: Path, ten_file: Iterable[str]) -> str:
    ten = sorted(ten_file)
    if len(ten) == 1:
        return _sha_file(gt_dir / ten[0])
    return _sha_text(_canonical([[t, _sha_file(gt_dir / t)] for t in ten]))


def _dong_olmocr(root: Path, e: Mapping[str, Any]) -> tuple[list[dict], list[dict]]:
    co, nguon, split = _quet_olmocr(root, e)
    gt_dir = root / e["annotation_dir"]
    pdf_dir = root / e["pdf_dir"]
    splits = e.get("splits") or {}

    dong: list[dict] = []
    bo: list[dict] = []
    for pdf in sorted(pdf_dir.rglob("*.pdf")):
        doc_id = pdf.stem
        if doc_id not in co:
            bo.append({"dataset": e["name"], "document_id": doc_id, "reason": "no_annotation"})
            continue
        s = split[doc_id]
        if s not in splits:
            raise DatasetManifestError(
                f"{e['name']}: split {s!r} chưa khai trong `splits` của catalog — "
                f"không suy được `scan_category` thì không được đoán."
            )
        ngon_ngu = e["languages"][0] if len(e["languages"]) == 1 else "und"
        dong.append(
            {
                "dataset": e["name"],
                "document_id": doc_id,
                "pdf_path": pdf.relative_to(root).as_posix(),
                "pdf_sha256": _sha_file(pdf),
                "annotation_paths": sorted(
                    (gt_dir / t).relative_to(root).as_posix() for t in nguon[doc_id]
                ),
                "annotation_sha256": _sha_nhieu_nguon(gt_dir, nguon[doc_id]),
                "annotations": co[doc_id],
                "source_url": e["source_url"],
                "source_version": e["version"],
                "source_license": e["license"],
                "language": ngon_ngu,
                "language_source": "dataset_declaration" if ngon_ngu != "und" else "unverified",
                "document_type": s,
                "scan_category": splits[s],
                "scan_category_source": e.get("scan_category_source", "dataset_split"),
                "dataset_split": s,
                "pages": None,
            }
        )
    return dong, bo


def _dong_coco(root: Path, e: Mapping[str, Any], corrections: Corrections) -> tuple[list[dict], list[dict]]:
    gt_dir = root / e["annotation_dir"]
    pdf_dir = root / e["pdf_dir"]
    coco_path = gt_dir / e.get("annotation_file", "layout_coco.json")
    if not coco_path.exists():
        raise DatasetManifestError(f"{e['name']}: thiếu {coco_path}")

    coco = json.loads(coco_path.read_text(encoding="utf-8"))
    ten_lop = {c["id"]: c["name"] for c in coco["categories"]}
    theo_anh: dict[int, list[dict]] = {}
    for a in coco["annotations"]:
        theo_anh.setdefault(a["image_id"], []).append(a)

    # Nhãn của DocLayNet nằm trong **một** file COCO dùng chung, cộng với overlay sửa
    # tay. Nên "checksum nhãn" của mỗi tài liệu là cặp (nguồn, overlay): đổi một trong
    # hai là kết quả chấm có thể đổi, và dòng manifest phải phản ánh đúng điều đó.
    sha_coco = _sha_file(coco_path)
    overlay_path = gt_dir / e.get("correction_overlay", "fixes.json")
    sha_overlay = _sha_file(overlay_path) if overlay_path.exists() else _SHA_RONG
    sha_nhan = _sha_text(f"{sha_coco}:{sha_overlay}:{corrections.overlay_sha256()}")

    theo_ten = {Path(im["file_name"]).stem: im for im in coco["images"]}
    dong: list[dict] = []
    bo: list[dict] = []
    for pdf in sorted(pdf_dir.rglob("*.pdf")):
        doc_id = pdf.stem
        im = theo_ten.get(doc_id)
        if im is None:
            bo.append({"dataset": e["name"], "document_id": doc_id, "reason": "no_annotation"})
            continue

        cell_path = gt_dir / "cells" / f"{doc_id}.json"
        cells = json.loads(cell_path.read_text(encoding="utf-8")) if cell_path.exists() else None

        co = _co_nang_luc_rong()
        lop = {ten_lop[a["category_id"]] for a in theo_anh.get(im["id"], ())}
        co["layout_blocks"] = bool(lop)
        co["image_regions"] = "Picture" in lop
        co["table_region"] = "Table" in lop
        # `table_structure` cố tình để False: COCO cho hộp bảng, không cho ô/hàng/cột.
        # Bật cờ này ở đây sẽ khiến metric cấu trúc bảng chấm 204 tài liệu mà không có
        # nhãn ô nào để so.
        if not any(co.values()):
            # Trang **có mặt** trong nguồn nhãn nhưng nhãn rỗng. Hai trường hợp khác
            # nhau về bản chất và phải mang lý do khác nhau: `blank_page` là trang thật
            # sự trắng (không hộp, không text cell) — nhãn ĐÚNG là "không có gì", nhưng
            # recall của mọi metric bố cục đều chia cho 0 nên nó không chấm được;
            # `no_labels` là trang có chữ mà nhãn vắng, tức nhãn thiếu. Gộp hai cái vào
            # một chữ thì báo cáo không phân biệt được "không đo được" với "nhãn hụt".
            trang_trang = cells is not None and not cells.get("cells")
            bo.append(
                {
                    "dataset": e["name"],
                    "document_id": doc_id,
                    "reason": "blank_page" if trang_trang else "no_labels",
                }
            )
            continue

        if cells is not None:
            phan_loai = "digital" if cells.get("cells") else "no_text_layer"
            nguon_phan_loai = "text_layer_evidence"
        else:
            phan_loai = "unknown"
            nguon_phan_loai = "no_evidence"

        ngon_ngu = e["languages"][0] if len(e["languages"]) == 1 else "und"
        dong.append(
            {
                "dataset": e["name"],
                "document_id": doc_id,
                "pdf_path": pdf.relative_to(root).as_posix(),
                "pdf_sha256": _sha_file(pdf),
                "annotation_paths": sorted(
                    p.relative_to(root).as_posix()
                    for p in (coco_path, overlay_path)
                    if p.exists()
                ),
                "annotation_sha256": sha_nhan,
                "annotations": co,
                "source_url": e["source_url"],
                "source_version": e["version"],
                "source_license": e["license"],
                "language": ngon_ngu,
                "language_source": "dataset_declaration" if ngon_ngu != "und" else "unverified",
                "document_type": im.get("doc_category") or "unknown",
                "scan_category": phan_loai,
                "scan_category_source": nguon_phan_loai,
                "dataset_split": None,
                "pages": 1,
            }
        )
    return dong, bo


_BO_QUET = {
    "olmocr_assertions": lambda root, e, corr: _dong_olmocr(root, e),
    "layout_coco": _dong_coco,
}


def build_manifest(root: Path) -> dict[str, Any]:
    """Quét đĩa theo catalog → manifest tất định.

    Chỉ bộ `included` sinh dòng tài liệu. Bộ `candidate`/`excluded` vẫn xuất hiện
    trong `datasets` kèm lý do — đó là cách duy nhất để người đọc thấy *cái gì đã bị
    bỏ ra ngoài*; danh sách chỉ gồm bộ đã dùng thì không phân biệt được với danh sách
    đầy đủ.
    """
    root = Path(root)
    corrections = load_corrections(root / "datasets" / TEN_FILE_CORRECTIONS)

    dong: list[dict] = []
    bo: list[dict] = []
    tom_tat: list[dict] = []
    for e in load_catalog(root):
        d, b = ([], [])
        if e["status"] == "included":
            quet = _BO_QUET.get(e["annotation_kind"])
            if quet is None:
                raise DatasetManifestError(
                    f"{e['name']}: `annotation_kind` {e['annotation_kind']!r} chưa có bộ quét"
                )
            d, b = quet(root, e, corrections)
            dong.extend(d)
            bo.extend(b)
        tom_tat.append(
            {
                **{k: v for k, v in e.items() if k != "splits"},
                "document_count": len(d),
                "excluded_count": len(b),
            }
        )

    # Khoá tra nhãn ở `scorer.run_bench` là `doc.stem`, dùng chung cho mọi bộ. Hai bộ
    # đụng tên nhau thì một tài liệu sẽ bị chấm bằng nhãn của tài liệu khác — và bảng
    # vẫn in ra bình thường. Nên đây là lỗi, không phải cảnh báo.
    thay: dict[str, str] = {}
    for r in dong:
        if r["document_id"] in thay:
            raise DatasetManifestError(
                f"document_id {r['document_id']!r} xuất hiện ở cả {thay[r['document_id']]!r} "
                f"và {r['dataset']!r} — khoá tra nhãn sẽ trỏ nhầm bộ"
            )
        thay[r["document_id"]] = r["dataset"]

    included = [e for e in tom_tat if e["status"] == "included"]
    ngon_ngu = sorted({l for e in included for l in e.get("languages", ())})
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_by": "scripts/build_dataset_manifest.py",
        "datasets": tom_tat,
        "documents": sorted(dong, key=lambda r: r["document_id"]),
        "excluded_documents": sorted(bo, key=lambda r: (r["dataset"], r["document_id"])),
        "corrections": {
            "path": f"datasets/{TEN_FILE_CORRECTIONS}",
            "count": len(corrections.records),
            "overlay_sha256": corrections.overlay_sha256(),
        },
        "coverage": {
            "languages": ngon_ngu,
            "vietnamese_transcript": "present" if "vi" in ngon_ngu else "absent",
            "document_count": len(dong),
        },
    }
