"""Lưu kết quả engine ra đĩa và nạp lại — A2 (TASK-073).

    from ocr_bench.prediction import save_predictions, load_predictions

    results = run_engines(adapters, docs)      # ~3h với Marker trên CPU
    save_predictions(results, Path("prediction"))

    # về sau, sửa metric bao nhiêu lần cũng được:
    table = score_results(load_predictions(Path("prediction")), metrics, gt)

Marker chạy 200 trang trên CPU mất khoảng 3 tiếng. Sửa một dòng trong metric mà phải
chạy lại 3 tiếng thì không ai sửa metric nữa — người ta sẽ giữ nguyên metric đầu tiên
viết ra, kể cả khi biết nó sai. Đó mới là cái giá thật của việc không có file này.

## Bố cục trên đĩa

```
prediction/<engine>/<doc_id>.json
prediction/<engine>/<doc_id>.images/000.png     ← chỉ khi engine trả bytes ảnh
```

Ảnh **không** nhúng base64 vào JSON. Một trang scan cho vài trăm KB PNG; nhúng vào thì
JSON phình lên, `git diff` thành một dòng khổng lồ đổi toàn bộ mỗi lần chạy lại, và
lợi ích lớn nhất của việc commit prediction — nhìn thấy engine đổi hành vi ở chỗ nào —
biến mất. Tách ra thì JSON vẫn đọc được bằng mắt, PNG thì Git coi là binary
(`.gitattributes`) và chỉ báo đổi/không đổi.

## Vì sao chặt tay chuyện schema

`load_predictions()` là đường đi tới **bảng xếp hạng**. Một prediction nạp sai mà không
báo gì sẽ không hiện ra thành lỗi: nó hiện ra thành một engine tự dưng kém đi, và người
đọc bảng sẽ đi tìm nguyên nhân ở engine. Nên ở đây:

* thiếu trường → ném;
* **thừa** trường cũng ném. Đây là nhánh dễ bỏ qua mà nguy hiểm hơn: file do bản mới
  hơn ghi ra, có thêm một kênh dữ liệu, bản cũ nạp trót lọt và lặng lẽ chấm thiếu kênh
  đó. Không có cách nào phát hiện từ bảng kết quả;
* sai `schema_version` → ném, kèm câu lệnh phải chạy để sinh lại;
* sha256 ảnh không khớp → ném. File JSON và thư mục ảnh đi lệch nhau sau một lần
  rebase hỏng là chuyện có thật, và hậu quả là chấm tài liệu này bằng ảnh của tài liệu
  khác.

Mọi lỗi trên đều là :class:`PredictionSchemaError`, và thông báo luôn nói rõ **file
nào**. Ở quy mô 1.607 tài liệu, một thông báo lỗi không kèm đường dẫn là vô dụng.

## Đường chấm lại không đụng được vào engine

Module này import `json`, `hashlib`, `pathlib` và `ocr_bench.types` — **không** import
`ocr_bench.adapters`. Nạp rồi chấm thì không có đường nào gọi engine, kể cả nhầm. Đó là
bằng chứng cho AC-02 chắc hơn phép đo thời gian, vì phép đo còn phụ thuộc vào máy.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any, Literal

from ocr_bench.secrets import (
    contains_secret_pattern,
    is_secret_bearing_key,
    sanitize_secret_text,
)
from ocr_bench.types import (
    Box,
    BlockType,
    Capability,
    FailureKind,
    OcrBlock,
    OcrImage,
    OcrResult,
    OcrTable,
    RawArtifact,
    ScanLabel,
)

__all__ = [
    "SCHEMA_VERSION",
    "PredictionSchemaError",
    "prediction_path",
    "save_prediction",
    "save_predictions",
    "load_prediction",
    "load_predictions",
    "run_engines_cached",
]

SCHEMA_VERSION = 4
"""Tăng khi đổi *hình dạng* file. Prediction schema cũ sẽ bị từ chối thẳng chứ không
được cố nạp — nạp một nửa rồi chấm là đúng thứ AC-04 cấm.

Lịch sử:

* **1** — bản đầu (A2/TASK-073).
* **2** — thêm `model_load_seconds` và `rss_scope` (B6/TASK-084). File bản 1 nâng
  được **không cần chạy lại engine**: hai trường mới đều là "không đo" =
  ``null``, không suy được từ dữ liệu cũ và cũng không cần suy::

      py -3 scripts/migrate_predictions.py prediction

  Đây là lý do bản nâng cấp là script chứ không phải "sinh lại": repo đang giữ hơn
  một nghìn file prediction, riêng marker mất khoảng 3 tiếng để chạy lại — đúng cái
  giá mà module này tồn tại để khỏi phải trả.
* **3** — thêm danh tính family/profile, raw artifact sidecar và taxonomy lỗi.
* **4** — thêm `peak_vram_mb` (B10/Task 8). Cũng nâng được **không cần chạy lại
  engine**: file cũ chạy trước khi bench biết đo VRAM, nên giá trị đúng của chúng
  là ``null`` = "không đo được", chứ không phải 0. Ghi 0 sẽ nói rằng những lần
  chạy đó đã được đo và đo ra 0 MB VRAM — một khẳng định về thiết bị mà không lần
  chạy nào trong số đó đưa ra.
"""

_IMAGE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")
"""Tên file ảnh sidecar. Do chính bench sinh ra (`000.png`) nên siết chặt được: bất kỳ
thứ gì khác trong trường `file` đều là file đã bị sửa tay hoặc bị dựng để thoát thư mục."""

_BAD_CHARS = frozenset('/\\:*?"<>|') | {chr(c) for c in range(32)}
"""Ký tự không đặt được vào tên file trên Windows **hoặc** POSIX.

Không siết về ASCII: `doc_id` của bộ mẫu Việt hoàn toàn có thể có dấu, mà NTFS, ext4 và
Git đều lưu được. Cấm ASCII thì A3 sẽ phải đổi tên tài liệu để chiều bench — đó là bench
làm hỏng dữ liệu, không phải bảo vệ nó.
"""

_RESERVED = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{i}" for i in range(1, 10)}
    | {f"LPT{i}" for i in range(1, 10)}
)
"""Tên thiết bị DOS. `CON.json` trên Windows không phải file — mở ra là console."""

_ResultKeys = frozenset(
    {
        "schema_version",
        "engine",
        "engine_family",
        "profile",
        "engine_version",
        "doc_id",
        "capabilities",
        "text_md",
        "raw_artifacts",
        "blocks",
        "images",
        "tables",
        "scan_label",
        "page_sizes",
        "seconds",
        "model_load_seconds",
        "peak_rss_mb",
        "rss_scope",
        "peak_vram_mb",
        "failed",
        "error",
        "failure_kind",
        "config_fingerprint",
    }
)


class PredictionSchemaError(ValueError):
    """File prediction không dùng được. Luôn kèm đường dẫn file."""


# ---------------------------------------------------------------------------
# Ghi
# ---------------------------------------------------------------------------


def _check_name(value: str, what: str) -> str:
    """Kiểm `engine`/`doc_id` có làm được một thành phần đường dẫn hay không.

    Cố ý **không** tự thay ký tự lạ bằng `_`: hai tên khác nhau sẽ ra cùng một tên
    file, và tài liệu này lặng lẽ ghi đè kết quả của tài liệu kia.
    """
    ly_do = None
    if not value:
        ly_do = "rỗng"
    elif xau := sorted(_BAD_CHARS.intersection(value)):
        ly_do = f"chứa ký tự cấm {[c for c in xau]!r}"
    elif set(value) == {"."}:
        ly_do = "chỉ gồm dấu chấm — nó trỏ ra ngoài thư mục prediction"
    elif value != value.strip() or value.endswith("."):
        ly_do = "có khoảng trắng đầu/cuối hoặc dấu chấm cuối — Windows sẽ cắt bỏ"
    elif value.split(".", 1)[0].upper() in _RESERVED:
        ly_do = "trùng tên thiết bị DOS (CON, NUL, COM1…)"
    if ly_do:
        raise ValueError(
            f"{what}={value!r} không dùng được làm tên file: {ly_do}. "
            "Đổi tên ở nguồn; bench cố ý không tự thay ký tự vì hai tên khác nhau "
            "có thể bị gộp thành một file."
        )
    return value


def prediction_path(root: Path, engine: str, doc_id: str) -> Path:
    """`root/<engine>/<doc_id>.json`. Kiểm tên trước khi ghép."""
    return (
        Path(root)
        / _check_name(engine, "engine")
        / f"{_check_name(doc_id, 'doc_id')}.json"
    )


def _box_to_json(box: Box | None) -> dict[str, Any] | None:
    if box is None:
        return None
    return {"page": box.page, "x0": box.x0, "y0": box.y0, "x1": box.x1, "y1": box.y1}


def _block_to_json(b: OcrBlock) -> dict[str, Any]:
    return {
        "block_type": b.block_type.value,
        "box": _box_to_json(b.box),
        "text": b.text,
        "html": b.html,
        "level": b.level,
        "section_hierarchy": list(b.section_hierarchy),
    }


def _table_to_json(t: OcrTable) -> dict[str, Any]:
    return {
        "html": t.html,
        "box": _box_to_json(t.box),
        "n_rows": t.n_rows,
        "n_cols": t.n_cols,
    }


def _scan_label_to_json(s: ScanLabel | None) -> dict[str, Any] | None:
    if s is None:
        return None
    return {
        "is_scanned": s.is_scanned,
        "api": s.api,
        "confidence": s.confidence,
        "pages_needing_ocr": list(s.pages_needing_ocr),
        "reason": s.reason,
    }


def _jsonable_fingerprint(fp: dict[str, object], doc_id: str) -> dict[str, Any]:
    """Ném **lúc ghi** nếu fingerprint có thứ không JSON hoá được.

    `config_fingerprint` khai kiểu `dict[str, object]` nên adapter nhét gì vào cũng
    được. Để tới lúc đọc mới phát hiện thì đã mất 3 tiếng chạy engine.
    """
    def validate(value: object, where: str, *, key: str | None = None) -> None:
        if key is not None and is_secret_bearing_key(key):
            safe_secret_metadata = (
                value is None
                or isinstance(value, bool)
                or (isinstance(value, str) and value in {"", "<redacted>"})
            )
            if not safe_secret_metadata:
                raise ValueError(
                    f"{doc_id}: {where} chứa secret thô dưới khoá {key!r}; "
                    "chỉ lưu boolean/None/chuỗi rỗng hoặc '<redacted>'."
                )
        if isinstance(value, str):
            if contains_secret_pattern(value):
                raise ValueError(
                    f"{doc_id}: {where} chứa credential pattern; redaction trước khi lưu."
                )
            return
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                if not isinstance(nested_key, str):
                    raise ValueError(
                        f"{doc_id}: khoá {where} phải là str, gặp {nested_key!r}"
                    )
                validate(
                    nested_value,
                    f"{where}[{nested_key!r}]",
                    key=nested_key,
                )
            return
        if isinstance(value, (list, tuple)):
            for i, nested_value in enumerate(value):
                validate(nested_value, f"{where}[{i}]")

    validate(fp, "config_fingerprint")
    try:
        json.dumps(fp)
    except TypeError as exc:
        raise ValueError(
            f"{doc_id}: config_fingerprint không JSON hoá được ({exc}). "
            "Adapter phải quy về str/số/bool/list/dict trước khi trả về."
        ) from None
    return dict(fp)


def _check_sidecar_name(name: object, where: str) -> str:
    """Sidecar chỉ được là một tên file ASCII, không phải đường dẫn."""
    if not isinstance(name, str):
        raise ValueError(f"{where}={name!r} không hợp lệ; phải là một tên file an toàn")
    try:
        _check_name(name, where)
    except ValueError as exc:
        raise ValueError(f"{where}={name!r} không hợp lệ — {exc}") from None
    if not _IMAGE_NAME.fullmatch(name):
        raise ValueError(f"{where}={name!r} không hợp lệ; phải là một tên file an toàn")
    return name


def save_prediction(result: OcrResult, root: Path) -> Path:
    """Ghi một `OcrResult`. Trả về đường dẫn file JSON.

    Ảnh có bytes được ghi ra `<doc_id>.images/NNN.png` kèm sha256 trong JSON.
    """
    path = prediction_path(root, result.engine, result.doc_id)
    sidecar_writes: list[tuple[Path, bytes]] = []

    images: list[dict[str, Any]] = []
    img_dir = path.with_name(f"{result.doc_id}.images")
    for i, im in enumerate(result.images):
        entry: dict[str, Any] = {
            "box": _box_to_json(im.box),
            "source_id": im.source_id,
            "file": None,
            "sha256": None,
        }
        if im.data is not None:
            name = f"{i:03d}.png"
            sidecar_writes.append((img_dir / name, im.data))
            entry["file"] = name
            entry["sha256"] = hashlib.sha256(im.data).hexdigest()
        images.append(entry)

    raw_artifacts: list[dict[str, str]] = []
    raw_dir = path.with_name(f"{result.doc_id}.raw")
    seen_raw_names: set[str] = set()
    for i, artifact in enumerate(result.raw_artifacts):
        name = _check_sidecar_name(artifact.name, f"raw_artifacts[{i}].name")
        portable_name = name.casefold()
        if portable_name in seen_raw_names:
            raise ValueError(
                f"{result.doc_id}: raw_artifacts có tên trùng {name!r}; "
                "ghi tiếp sẽ đè bytes của artifact trước"
            )
        seen_raw_names.add(portable_name)
        if not isinstance(artifact.media_type, str) or not artifact.media_type:
            raise ValueError(
                f"{result.doc_id}: raw_artifacts[{i}].media_type "
                "phải là chuỗi không rỗng"
            )
        if not isinstance(artifact.data, bytes):
            raise ValueError(f"{result.doc_id}: raw_artifacts[{i}].data phải là bytes")
        sidecar_writes.append((raw_dir / name, artifact.data))
        raw_artifacts.append(
            {
                "name": artifact.name,
                "media_type": artifact.media_type,
                "file": name,
                "sha256": artifact.sha256,
            }
        )

    payload = {
        "schema_version": SCHEMA_VERSION,
        "engine": result.engine,
        "engine_family": result.engine_family,
        "profile": result.profile,
        "engine_version": result.engine_version,
        "doc_id": result.doc_id,
        # Nguyên văn, sắp xếp cho ổn định giữa các lần chạy. Nạp lại phải dựng đúng
        # frozenset này — suy ra từ "kênh nào có dữ liệu" là sai: engine có năng lực
        # mà không tìm thấy ảnh nào khác hẳn engine không bao giờ biết tìm ảnh.
        "capabilities": sorted(c.value for c in result.capabilities),
        "text_md": result.text_md,
        "raw_artifacts": raw_artifacts,
        "blocks": [_block_to_json(b) for b in result.blocks],
        "images": images,
        "tables": [_table_to_json(t) for t in result.tables],
        "scan_label": _scan_label_to_json(result.scan_label),
        "page_sizes": [list(p) for p in result.page_sizes],
        "seconds": result.seconds,
        "model_load_seconds": result.model_load_seconds,
        "peak_rss_mb": result.peak_rss_mb,
        # Đi cùng `peak_rss_mb` trong cả ghi lẫn đọc: một con số RSS không kèm phạm vi
        # là một con số không so sánh được (xem `types.OcrResult.rss_scope`).
        "rss_scope": result.rss_scope,
        # `None` ≠ 0.0: xem `types.OcrResult.peak_vram_mb`. Không có `vram_scope`
        # đi kèm vì VRAM được cấp theo tiến trình, không thừa hưởng mốc nước cao.
        "peak_vram_mb": result.peak_vram_mb,
        "failed": result.failed,
        "error": sanitize_secret_text(result.error),
        "failure_kind": (
            result.failure_kind.value if result.failure_kind is not None else None
        ),
        "config_fingerprint": _jsonable_fingerprint(
            result.config_fingerprint, result.doc_id
        ),
    }
    serialized = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    # Mọi validation ở trên phải hoàn tất trước side effect đầu tiên. Nếu một raw
    # artifact trùng tên hoặc fingerprint không an toàn, prediction/sidecar cũ phải
    # còn nguyên thay vì bị ghi đè nửa chừng rồi mới ném.
    path.parent.mkdir(parents=True, exist_ok=True)
    for sidecar_path, data in sidecar_writes:
        sidecar_path.parent.mkdir(parents=True, exist_ok=True)
        sidecar_path.write_bytes(data)
    path.write_text(
        serialized,
        encoding="utf-8",
        newline="\n",
    )
    return path


def save_predictions(results: Iterable[OcrResult], root: Path) -> list[Path]:
    return [save_prediction(r, root) for r in results]


# ---------------------------------------------------------------------------
# Đọc
# ---------------------------------------------------------------------------


def _exact_keys(
    d: dict[str, Any], allowed: frozenset[str], path: Path, where: str
) -> None:
    """Thiếu **và** thừa đều ném. Xem docstring module về nhánh 'thừa'."""
    got = set(d)
    if missing := allowed - got:
        raise PredictionSchemaError(
            f"{path}: {where} thiếu trường {sorted(missing)}"
        )
    if extra := got - allowed:
        raise PredictionSchemaError(
            f"{path}: {where} có trường lạ {sorted(extra)} — nhiều khả năng file do "
            f"bản ocr-bench mới hơn ghi ra. Nạp tiếp sẽ bỏ mất dữ liệu mà không báo; "
            "cập nhật ocr-bench hoặc sinh lại prediction."
        )


def _box_from_json(d: Any, path: Path, where: str) -> Box | None:
    if d is None:
        return None
    if not isinstance(d, dict):
        raise PredictionSchemaError(f"{path}: {where} phải là object hoặc null")
    _exact_keys(d, frozenset({"page", "x0", "y0", "x1", "y1"}), path, where)
    try:
        return Box(
            page=int(d["page"]),
            x0=float(d["x0"]),
            y0=float(d["y0"]),
            x1=float(d["x1"]),
            y1=float(d["y1"]),
        )
    except (TypeError, ValueError) as exc:
        raise PredictionSchemaError(f"{path}: {where} không hợp lệ — {exc}") from None


def _enum_from_json(cls: type, value: Any, path: Path, where: str):
    try:
        return cls(value)
    except ValueError:
        raise PredictionSchemaError(
            f"{path}: {where} có giá trị {value!r} không thuộc {cls.__name__}; "
            f"hợp lệ: {sorted(m.value for m in cls)}"
        ) from None


def _str_tuple(value: Any, path: Path, where: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
        raise PredictionSchemaError(f"{path}: {where} phải là list chuỗi")
    return tuple(value)


def _block_from_json(d: Any, path: Path, where: str) -> OcrBlock:
    if not isinstance(d, dict):
        raise PredictionSchemaError(f"{path}: {where} phải là object")
    _exact_keys(
        d,
        frozenset(
            {"block_type", "box", "text", "html", "level", "section_hierarchy"}
        ),
        path,
        where,
    )
    return OcrBlock(
        block_type=_enum_from_json(
            BlockType, d["block_type"], path, f"{where}.block_type"
        ),
        box=_box_from_json(d["box"], path, f"{where}.box"),
        text=d["text"],
        html=d["html"],
        level=d["level"],
        section_hierarchy=_str_tuple(
            d["section_hierarchy"], path, f"{where}.section_hierarchy"
        ),
    )


def _table_from_json(d: Any, path: Path, where: str) -> OcrTable:
    if not isinstance(d, dict):
        raise PredictionSchemaError(f"{path}: {where} phải là object")
    _exact_keys(d, frozenset({"html", "box", "n_rows", "n_cols"}), path, where)
    return OcrTable(
        html=d["html"],
        box=_box_from_json(d["box"], path, f"{where}.box"),
        n_rows=d["n_rows"],
        n_cols=d["n_cols"],
    )


def _image_from_json(d: Any, path: Path, img_dir: Path, where: str) -> OcrImage:
    if not isinstance(d, dict):
        raise PredictionSchemaError(f"{path}: {where} phải là object")
    _exact_keys(d, frozenset({"box", "source_id", "file", "sha256"}), path, where)

    data: bytes | None = None
    if d["file"] is not None:
        name = d["file"]
        if not isinstance(name, str) or not _IMAGE_NAME.match(name):
            raise PredictionSchemaError(f"{path}: {where}.file={name!r} không hợp lệ")
        blob = img_dir / name
        if blob.is_file():
            data = blob.read_bytes()
            got = hashlib.sha256(data).hexdigest()
            if got != d["sha256"]:
                raise PredictionSchemaError(
                    f"{path}: {where} sha256 lệch ({got} ≠ {d['sha256']}) ở {blob}. "
                    "Chấm tiếp là chấm tài liệu này bằng ảnh của lần chạy khác."
                )
    return OcrImage(
        box=_box_from_json(d["box"], path, f"{where}.box"),
        data=data,
        source_id=d["source_id"],
    )


def _raw_artifact_metadata_from_json(
    d: Any, path: Path, where: str
) -> tuple[str, str, str, str]:
    if not isinstance(d, dict):
        raise PredictionSchemaError(f"{path}: {where} phải là object")
    _exact_keys(d, frozenset({"name", "media_type", "file", "sha256"}), path, where)
    try:
        name = _check_sidecar_name(d["name"], f"{where}.name")
        file_name = _check_sidecar_name(d["file"], f"{where}.file")
    except ValueError as exc:
        raise PredictionSchemaError(f"{path}: {exc}") from None
    if not isinstance(d["media_type"], str) or not d["media_type"]:
        raise PredictionSchemaError(f"{path}: {where}.media_type phải là chuỗi không rỗng")
    if not isinstance(d["sha256"], str):
        raise PredictionSchemaError(f"{path}: {where}.sha256 phải là chuỗi")
    return name, d["media_type"], file_name, d["sha256"]


def _raw_artifact_from_json(
    metadata: tuple[str, str, str, str],
    path: Path,
    raw_dir: Path,
    where: str,
) -> RawArtifact:
    name, media_type, file_name, expected_sha256 = metadata
    blob = raw_dir / file_name
    if not blob.is_file():
        raise PredictionSchemaError(
            f"{path}: {where} trỏ tới {blob} nhưng file không có. "
            "JSON và thư mục raw artifact đã đi lệch nhau — sinh lại prediction."
        )
    data = blob.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != expected_sha256:
        raise PredictionSchemaError(
            f"{path}: {where} sha256 lệch ({got} ≠ {expected_sha256}) ở {blob}. "
            "Không thể audit output nguyên bản nếu sidecar thuộc lần chạy khác."
        )
    return RawArtifact(name=name, media_type=media_type, data=data)


def _scan_label_from_json(d: Any, path: Path, where: str) -> ScanLabel | None:
    if d is None:
        return None
    if not isinstance(d, dict):
        raise PredictionSchemaError(f"{path}: {where} phải là object hoặc null")
    _exact_keys(
        d,
        frozenset(
            {"is_scanned", "api", "confidence", "pages_needing_ocr", "reason"}
        ),
        path,
        where,
    )
    pages = d["pages_needing_ocr"]
    if not isinstance(pages, list) or any(not isinstance(p, int) for p in pages):
        raise PredictionSchemaError(
            f"{path}: {where}.pages_needing_ocr phải là list số nguyên"
        )
    return ScanLabel(
        is_scanned=d["is_scanned"],
        api=d["api"],
        confidence=d["confidence"],
        pages_needing_ocr=tuple(pages),
        reason=d["reason"],
    )


def _page_sizes_from_json(
    value: Any, path: Path
) -> tuple[tuple[float, float], ...]:
    if not isinstance(value, list):
        raise PredictionSchemaError(f"{path}: page_sizes phải là list")
    out: list[tuple[float, float]] = []
    for i, p in enumerate(value):
        if not isinstance(p, list) or len(p) != 2:
            raise PredictionSchemaError(
                f"{path}: page_sizes[{i}] phải là cặp [rộng, cao], nhận {p!r}"
            )
        out.append((float(p[0]), float(p[1])))
    return tuple(out)


def _required_string(value: Any, path: Path, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise PredictionSchemaError(f"{path}: {where} phải là chuỗi không rỗng")
    return value


def load_prediction(path: Path) -> OcrResult:
    """Nạp một file prediction. Ném :class:`PredictionSchemaError` nếu có gì lệch."""
    path = Path(path)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PredictionSchemaError(f"{path}: JSON hỏng — {exc}") from None

    if not isinstance(raw, dict):
        raise PredictionSchemaError(f"{path}: gốc file phải là object JSON")

    version = raw.get("schema_version")
    if version not in (2, 3, SCHEMA_VERSION):
        raise PredictionSchemaError(
            f"{path}: schema_version={version!r}, bản đang chạy đọc được "
            f"{SCHEMA_VERSION}. Nâng cấp tại chỗ bằng "
            "`py -3 scripts/migrate_predictions.py prediction` (không chạy lại "
            "engine), hoặc sinh lại bằng `scripts/make_predictions.py` — "
            "cố nạp file schema khác là cách chấm sai mà không có triệu chứng."
        )

    if version in (2, 3):
        raw.setdefault("engine_family", raw.get("engine", "unknown"))
        raw.setdefault("profile", "default")
        raw.setdefault("raw_artifacts", [])
        raw.setdefault("peak_vram_mb", None)
        if raw.get("failed") and raw.get("failure_kind") is None:
            raw["failure_kind"] = FailureKind.ENGINE_ERROR.value
        elif "failure_kind" not in raw:
            raw["failure_kind"] = None

    _exact_keys(raw, _ResultKeys, path, "gốc file")

    doc_id = raw["doc_id"]
    if doc_id != path.stem:
        raise PredictionSchemaError(
            f"{path}: doc_id={doc_id!r} không khớp tên file {path.stem!r}. "
            "Đổi tên file thủ công sẽ làm bench tra nhãn của tài liệu khác."
        )

    fingerprint = raw["config_fingerprint"]
    if not isinstance(fingerprint, dict):
        raise PredictionSchemaError(f"{path}: config_fingerprint phải là object")
    try:
        fingerprint = _jsonable_fingerprint(fingerprint, doc_id)
    except ValueError as exc:
        raise PredictionSchemaError(f"{path}: {exc}") from None

    caps = raw["capabilities"]
    if not isinstance(caps, list):
        raise PredictionSchemaError(f"{path}: capabilities phải là list")
    capabilities = frozenset(
        _enum_from_json(Capability, c, path, "capabilities[]") for c in caps
    )
    raw_artifacts = raw["raw_artifacts"]
    if not isinstance(raw_artifacts, list):
        raise PredictionSchemaError(f"{path}: raw_artifacts phải là list")
    raw_metadata = tuple(
        _raw_artifact_metadata_from_json(a, path, f"raw_artifacts[{i}]")
        for i, a in enumerate(raw_artifacts)
    )
    seen_raw_names: set[str] = set()
    seen_raw_files: set[str] = set()
    for i, (name, _media_type, file_name, _sha256) in enumerate(raw_metadata):
        for field, value, seen in (
            ("name", name, seen_raw_names),
            ("file", file_name, seen_raw_files),
        ):
            portable_value = value.casefold()
            if portable_value in seen:
                raise PredictionSchemaError(
                    f"{path}: raw_artifacts[{i}].{field}={value!r} có tên trùng "
                    "không phân biệt hoa/thường"
                )
            seen.add(portable_value)

    img_dir = path.with_name(f"{doc_id}.images")
    raw_dir = path.with_name(f"{doc_id}.raw")
    try:
        return OcrResult(
            engine=raw["engine"],
            engine_family=_required_string(
                raw["engine_family"], path, "engine_family"
            ),
            profile=_required_string(raw["profile"], path, "profile"),
            engine_version=raw["engine_version"],
            doc_id=doc_id,
            capabilities=capabilities,
            text_md=raw["text_md"],
            raw_artifacts=tuple(
                _raw_artifact_from_json(a, path, raw_dir, f"raw_artifacts[{i}]")
                for i, a in enumerate(raw_metadata)
            ),
            blocks=tuple(
                _block_from_json(b, path, f"blocks[{i}]")
                for i, b in enumerate(raw["blocks"])
            ),
            images=tuple(
                _image_from_json(im, path, img_dir, f"images[{i}]")
                for i, im in enumerate(raw["images"])
            ),
            tables=tuple(
                _table_from_json(t, path, f"tables[{i}]")
                for i, t in enumerate(raw["tables"])
            ),
            scan_label=_scan_label_from_json(raw["scan_label"], path, "scan_label"),
            page_sizes=_page_sizes_from_json(raw["page_sizes"], path),
            seconds=raw["seconds"],
            model_load_seconds=raw["model_load_seconds"],
            peak_rss_mb=raw["peak_rss_mb"],
            rss_scope=raw["rss_scope"],
            peak_vram_mb=raw["peak_vram_mb"],
            failed=raw["failed"],
            error=raw["error"],
            failure_kind=(
                None
                if raw["failure_kind"] is None
                else _enum_from_json(
                    FailureKind, raw["failure_kind"], path, "failure_kind"
                )
            ),
            config_fingerprint=fingerprint,
        )
    except ValueError as exc:
        # `OcrResult.__post_init__` giữ bất biến "có dữ liệu thì phải khai năng lực".
        # File sửa tay có thể phá bất biến đó; báo kèm đường dẫn chứ đừng để lộ ra
        # một ValueError trần không biết của file nào trong 1.607 file.
        if isinstance(exc, PredictionSchemaError):
            raise
        raise PredictionSchemaError(f"{path}: {exc}") from None


def _kiem_bo_cuc(d: Path) -> None:
    """Thư mục engine rỗng mà bên dưới lại có `*.json` ⇒ bố cục lồng, phải ném.

    Thư mục engine **rỗng** vẫn hợp lệ: engine chưa chạy khác với engine chạy hỏng.
    Nhưng rỗng *ở tầng này* mà có dữ liệu *ở tầng dưới* thì không phải "chưa chạy" —
    đó là dữ liệu bị chôn, và cách hỏng của nó là im lặng: loader trả ít hơn thật mà
    không có triệu chứng nào. Đúng chuyện đã xảy ra với `prediction/sovereign_*`
    (206 file, xem TASK-091).

    Điều kiện phải là "thư mục con **có `*.json`**", không phải "có thư mục con":
    `prediction/opendataloader/` có 204 thư mục con `<doc_id>.images` chứa ảnh trích
    ra, tất cả đều hợp lệ.
    """
    if any(d.glob("*.json")):
        return
    for con in sorted(d.iterdir()):
        if con.is_dir() and any(con.glob("*.json")):
            raise PredictionSchemaError(
                f"{d}: không có `*.json` ở tầng này nhưng `{con.name}/` thì có. "
                "Bố cục đúng là `prediction/<engine>/<doc_id>.json` — lồng thêm một "
                "tầng thì `load_predictions()` bỏ qua toàn bộ mà không báo. "
                "Thường do truyền `root=prediction/<engine>` vào `prediction_path()`."
            )


def load_predictions(
    root: Path, engines: Sequence[str] | None = None
) -> list[OcrResult]:
    """Nạp toàn bộ prediction dưới `root`, sắp xếp tất định theo (engine, doc_id).

    `engines=None` nghĩa là mọi thư mục con. Thư mục rỗng không phải lỗi — engine
    chưa chạy khác với engine chạy hỏng, và cái sau đã nằm trong file với
    `failed=True`. Thư mục rỗng mà **bên dưới** có `*.json` thì lại là lỗi:
    xem :func:`_kiem_bo_cuc`.

    Tên thư mục **là** danh tính engine. File nằm trong `prediction/X/` mà khai
    `engine != "X"` sẽ bị ném — nếu không, dữ liệu chui vào nhầm cột của bảng điểm
    và không có gì trong bảng chỉ ra điều đó.
    """
    root = Path(root)
    if not root.is_dir():
        raise PredictionSchemaError(f"{root}: không phải thư mục prediction")
    dirs = (
        sorted(d for d in root.iterdir() if d.is_dir())
        if engines is None
        else [root / e for e in engines]
    )
    out: list[OcrResult] = []
    for d in dirs:
        if not d.is_dir():
            raise PredictionSchemaError(f"{d}: chưa có prediction cho engine này")
        _kiem_bo_cuc(d)
        for p in sorted(d.glob("*.json")):
            r = load_prediction(p)
            if r.engine != d.name:
                raise PredictionSchemaError(
                    f"{p}: engine={r.engine!r} nhưng nằm trong thư mục {d.name!r}. "
                    "Tên thư mục là danh tính engine trong bảng điểm; lệch nhau thì "
                    "kết quả bị gom vào nhầm cột."
                )
            out.append(r)
    return out


# ---------------------------------------------------------------------------
# Đường tiện lợi: chạy có nhớ
# ---------------------------------------------------------------------------

VersionMismatch = Literal["rerun", "use", "error"]


def run_engines_cached(
    adapters: Sequence[Any],
    docs: Sequence[Path],
    root: Path,
    *,
    refresh: bool = False,
    on_version_mismatch: VersionMismatch = "rerun",
) -> list[OcrResult]:
    """Như `scorer.run_engines` nhưng dùng lại prediction đã có trên đĩa.

    Chỉ dùng ở lúc **chạy**. Lúc chấm lại thì gọi thẳng `load_predictions()` — nó
    không import adapter nên không có đường nào lỡ tay gọi engine.

    `on_version_mismatch` xử lý file cũ do bản engine khác ghi ra:

    * ``"rerun"`` (mặc định) — chạy lại. Ở đường này engine vốn đang có sẵn, nên
      chạy lại là lựa chọn trung thực; giữ số cũ rồi ghi nhãn version mới là cách
      tạo ra một bảng không ai truy được về đâu.
    * ``"error"`` — dừng. Dùng khi engine nặng và muốn tự quyết từng ca.
    * ``"use"`` — cứ dùng. Phải nói ra miệng, không bao giờ là mặc định.
    """
    out: list[OcrResult] = []
    for a in adapters:
        for doc in docs:
            path = prediction_path(root, a.name, doc.stem)
            if not refresh and path.is_file():
                cached = load_prediction(path)
                if cached.engine_version == a.version():
                    out.append(cached)
                    continue
                if on_version_mismatch == "use":
                    out.append(cached)
                    continue
                if on_version_mismatch == "error":
                    raise PredictionSchemaError(
                        f"{path}: prediction ghi bởi {a.name} bản "
                        f"{cached.engine_version!r}, engine hiện tại là "
                        f"{a.version()!r}. Chạy lại (refresh=True) hoặc chấp nhận "
                        'số cũ bằng on_version_mismatch="use".'
                    )
            result = a.execute(doc)
            save_prediction(result, root)
            out.append(result)
    return out
