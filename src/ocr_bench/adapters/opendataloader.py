"""Bộ nối OpenDataLoader (`opendataloader-pdf`) — A5 (TASK-076).

OpenDataLoader không phải thư viện Python: gói pip chỉ là lớp bọc mỏng gọi một file
`.jar` bằng lệnh `java`. Bốn điều quyết định hình dạng file này, **cả bốn đều là kết
quả đo, không phải suy từ tài liệu**:

1. **Hệ toạ độ: gốc DƯỚI-trái, y hướng LÊN, đơn vị điểm PDF, `[x0, y0, x1, y1]`.**
   Đo bằng `scripts/measure_opendataloader_coords.py` trên PDF tự dựng, chữ đặt ở
   toạ độ biết trước. Khác Marker (gốc TRÊN-trái, y xuống) — nên `y_axis="up"`.

   Phép đo 4 của script đó lật ngược một giả định dễ mắc: dựng lại trang với
   MediaBox dịch đi (100, 200) thì box trả về **không đổi một chút nào**
   (Δx=0.00, Δy=0.00) → OpenDataLoader **đã tự trừ gốc MediaBox**, khác Marker.
   Nên ở đây `page_x0`/`page_y0` phải để **0**; chép theo Marker mà truyền
   `mb.left`/`mb.bottom` vào là trừ hai lần, và mọi box lệch đúng một lượng cố
   định trên mọi tài liệu có MediaBox không bắt đầu từ gốc.

2. **JSON của nó KHÔNG có kích thước trang.** Khoá cấp cao chỉ có `file name`,
   `number of pages`, `author`, `title`, ngày tháng, `kids`. Không có node trang,
   không có `width`/`height` ở bất kỳ đâu — kiểm bằng cách đổ toàn bộ node của 24
   tài liệu. Mà `Box.from_absolute` cần chiều trang để chuẩn hoá. Nên kích thước
   lấy từ **MediaBox đọc bằng `pypdf`** — cùng lối `corpus.py` lấy kích thước trang
   DocLayNet từ metadata file cell chứ không từ COCO.

3. **`page number` là 1-indexed.** A0 mới chỉ cảnh báo `row number`/`column number`
   của bảng; đo thật thì số trang cũng vậy. Bench 0-based khắp nơi (`Box(page=-1)`
   bị chặn), nên trừ 1 ngay tại biên. Không trừ thì mọi box lệch đúng một trang:
   tài liệu 1 trang thì rụng sạch, tài liệu nhiều trang thì IoU ra một con số
   thấp-nhưng-hợp-lý — đúng lớp hỏng yên lặng mà A4 đã dính ba lần.

4. **Bảng chỉ hiện ra với `table_method="cluster"`.** Mặc định của engine là
   `default` (dò theo đường kẻ). Chạy 4 tài liệu mà DocLayNet gắn nhãn nhiều bảng
   nhất (5, 4, 4, 3 bảng): `default` ra **0** node `table`, `cluster` ra bảng có đủ
   `rows`/`cells`/`row span`/`column span`. Để mặc định là tự nguyện bỏ toàn bộ
   nhóm metric bảng (B2).

Chạy bằng venv riêng (`.venv-odl`) và cần JRE — dựng bằng `scripts/setup_java.py`:

    py -3 scripts/setup_java.py
    .venv-odl/Scripts/python.exe scripts/make_predictions.py --engines opendataloader
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from collections.abc import Mapping
from dataclasses import dataclass, replace
from html import escape
from pathlib import Path
from typing import Any, ClassVar, Iterator, Literal

from ocr_bench.adapters.base import Adapter, AdapterOutputError
from ocr_bench.profiles import EngineProfile, ProfileConfigError
from ocr_bench.types import (
    Box,
    BlockType,
    Capability,
    OcrBlock,
    OcrImage,
    OcrResult,
    OcrTable,
    RawArtifact,
)

__all__ = [
    "OpenDataLoaderAdapter",
    "BLOCK_TYPE_MAP",
    "map_block_type",
    "node_phang",
    "node_khoi",
    "chay_cli",
    "kich_thuoc_trang",
    "bang_sang_html",
    "chu_cua_node",
    "build_result",
]

HYBRID_MANIFEST_ENV = "OCR_BENCH_ODL_HYBRID_MANIFEST"
DEFAULT_HYBRID_MANIFEST_PATH = (
    Path(__file__).resolve().parents[3]
    / "build"
    / "odl-hybrid"
    / "manifest.json"
)
HYBRID_HOST = "127.0.0.1"
HYBRID_PORT = 5002
HYBRID_URL = "http://127.0.0.1:5002"
HYBRID_SERVER_CONFIG = {
    "device": "cpu",
    "device_enforcement": {"CUDA_VISIBLE_DEVICES": ""},
    "device_enforcement_method": "CUDA_VISIBLE_DEVICES-empty-before-spawn",
    "force_ocr": True,
    "health_url": f"{HYBRID_URL}/health",
    "host": HYBRID_HOST,
    "jit_enforcement": {"TORCHDYNAMO_DISABLE": "1"},
    "jit_enforcement_method": "TORCHDYNAMO_DISABLE-before-spawn",
    "ocr_engine": "easyocr",
    "ocr_languages": ["vi", "en"],
    "port": HYBRID_PORT,
}
HYBRID_ARGV_TAIL = [
    "-m", "opendataloader_pdf.hybrid_server",
    "--host", HYBRID_HOST,
    "--port", str(HYBRID_PORT),
    "--force-ocr",
    "--ocr-engine", "easyocr",
    "--ocr-lang", "vi,en",
]
HYBRID_VERSION_SPECS = {
    "docling": ">=2.91.0",
    "easyocr": ">=1.7,<2",
    "fastapi": ">=0.136.1",
    "opendataloader-pdf": "==2.5.0",
    "packaging": ">=23",
    "pypdf": ">=5",
    "psutil": ">=5",
    "python-multipart": ">=0.0.28",
    "uvicorn": ">=0.46.0",
}

# 8 `type` quan sát được trên 24 tài liệu → `BlockType` của bench.
# `text block` là khung gom nhiều đoạn, không phải một khối nội dung — nó được đi
# xuyên qua trong `node_khoi()` chứ không tự thành block.
BLOCK_TYPE_MAP: dict[str, BlockType] = {
    "paragraph": BlockType.TEXT,
    "heading": BlockType.HEADING,
    "list": BlockType.LIST,
    "list item": BlockType.LIST,
    "image": BlockType.PICTURE,
    "caption": BlockType.CAPTION,
    "table": BlockType.TABLE,
    "table cell": BlockType.TABLE,
}

# Nút chỉ để gom, không tự là một khối nội dung.
KHUNG_GOM = frozenset({"text block"})

# Khoá chứa con. `list` để con ở `list items`, `table` ở `rows`, `table row` ở
# `cells` — không phải `kids` như mọi node khác. Dò thiếu một khoá là mất im lặng
# cả nhánh cây.
KHOA_CON = ("kids", "list items", "rows", "cells")


def map_block_type(odl_type: str) -> BlockType:
    """Loại lạ rơi vào `OTHER`, **không** bị bỏ — cùng lý do như Marker: bỏ block là
    mất recall, và bản engine mới thêm loại node không được phép làm điểm tụt."""
    return BLOCK_TYPE_MAP.get(odl_type, BlockType.OTHER)


# --------------------------------------------------------------------------
# Đi cây
# --------------------------------------------------------------------------


def node_phang(node: Any) -> Iterator[dict]:
    """Duyệt **toàn bộ** node, kể cả con của list item và ô bảng.

    Dùng cho việc dò/đo (`scripts/measure_opendataloader_coords.py`), không dùng để
    dựng block — dựng block bằng hàm này sẽ đếm trùng: `list` và `list item` và
    `paragraph` bên trong list item đều có `bounding box` chồng nhau.
    """
    if isinstance(node, list):
        for c in node:
            yield from node_phang(c)
        return
    if not isinstance(node, dict):
        return
    if "type" in node:
        yield node
    for khoa in KHOA_CON:
        if khoa in node:
            yield from node_phang(node[khoa])


def node_khoi(doc: dict) -> Iterator[dict]:
    """Duyệt đúng tầng khối nội dung — mô hình phẳng, khớp DocLayNet.

    Quy tắc, mỗi cái đều để tránh đếm trùng hoặc đếm thiếu:

    * `list` → đi xuống `list items`, **không** phát chính nó. DocLayNet gắn nhãn
      từng `List-item` một, không gắn nhãn cả cụm danh sách.
    * `list item` → phát, **không** đi xuống `kids`. Con của nó là `paragraph`
      có box gần trùng; phát cả hai là nhân đôi vùng và precision tụt vô cớ.
    * `table` → phát chính nó, **không** đi xuống ô. Ô đi vào `OcrTable.html`.
    * `text block` → chỉ là khung gom, đi xuyên qua.
    """
    def di(node: Any) -> Iterator[dict]:
        if isinstance(node, list):
            for c in node:
                yield from di(c)
            return
        if not isinstance(node, dict):
            return
        t = node.get("type")
        if t == "list":
            yield from di(node.get("list items", []))
        elif t in KHUNG_GOM or t is None:
            yield from di(node.get("kids", []))
        else:
            yield node

    yield from di(doc.get("kids", []))


def chu_cua_node(node: Any) -> str:
    """Gom `content` của node và mọi con của nó, giữ thứ tự đọc.

    `list item` và `table cell` không có `content` của riêng chúng — chữ nằm ở
    `paragraph` con. Lấy thẳng `node["content"]` thì mọi mục danh sách và mọi ô
    bảng ra chuỗi rỗng.
    """
    phan: list[str] = []
    for n in node_phang(node):
        if c := (n.get("content") or "").strip():
            phan.append(c)
    return " ".join(phan)


# --------------------------------------------------------------------------
# Gọi engine
# --------------------------------------------------------------------------


def _java() -> Path:
    """`java` dùng được, ưu tiên bản bỏ túi trong `.tools/`.

    `opendataloader_pdf.runner.run_jar` ghi cứng chuỗi `"java"` trong `command` —
    nó không nhận đường dẫn, không đọc `JAVA_HOME`. Nên cách duy nhất để trỏ nó
    vào JRE của `.tools/` là chèn thư mục `bin` đó lên đầu `PATH`.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
    try:
        from setup_java import tim_java  # type: ignore[import-not-found]
    except ImportError:
        tim_java = None  # type: ignore[assignment]

    if tim_java is not None and (java := tim_java()):
        return java
    if p := shutil.which("java"):
        return Path(p)
    raise RuntimeError(
        "Không tìm thấy java >= 11. Chạy `py -3 scripts/setup_java.py` trước."
    )


def chay_cli(
    inputs: list[Path],
    out_dir: Path,
    *,
    table_method: str | None = "cluster",
    reading_order: str | None = "xycut",
    include_header_footer: bool = True,
    quiet: bool = True,
    hybrid: str | None = None,
    hybrid_mode: str | None = None,
    hybrid_url: str | None = None,
    hybrid_fallback: bool = False,
) -> None:
    """Gọi `.jar` của OpenDataLoader, ghi `json` + `md` vào `out_dir`.

    Import `opendataloader_pdf` **lười**: `pyproject.toml` chốt rằng `pytest` của
    repo phải xanh trên máy trắng, mà gói này là extra. Import ở đầu module thì
    `import ocr_bench` trên máy chưa cài sẽ nổ và cả registry rụng theo.
    """
    import opendataloader_pdf  # noqa: PLC0415 — cố ý lười, xem docstring

    java = _java()
    moi_truong = os.environ.get("PATH", "")
    os.environ["PATH"] = str(java.parent) + os.pathsep + moi_truong
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        opendataloader_pdf.convert(
            input_path=[str(p) for p in inputs],
            output_dir=str(out_dir),
            format=["json", "markdown"],
            markdown_with_html=True,  # bảng nhiều dòng gộp cần thẻ HTML
            table_method=table_method,
            reading_order=reading_order,
            include_header_footer=include_header_footer,
            image_output="external",
            image_format="png",  # `OcrImage.data` là PNG theo hợp đồng
            quiet=quiet,
            hybrid=hybrid,
            hybrid_mode=hybrid_mode,
            hybrid_url=hybrid_url,
            hybrid_fallback=hybrid_fallback,
        )
    finally:
        os.environ["PATH"] = moi_truong


def kich_thuoc_trang(pdf: Path) -> list[tuple[float, float]]:
    """`[(width, height), ...]` theo MediaBox, đọc bằng `pypdf`.

    JSON của OpenDataLoader không có kích thước trang (xem docstring module), mà
    `Box.from_absolute` bắt buộc phải có. Đây là nguồn thứ hai — đúng kỷ luật của
    A4: không tin engine về thứ nó không tự khai.

    Chỉ lấy **chiều**, không lấy `left`/`bottom`: phép đo 4 cho thấy engine đã trừ
    gốc MediaBox rồi.
    """
    from pypdf import PdfReader  # noqa: PLC0415 — extra, import lười

    return [
        (float(t.mediabox.width), float(t.mediabox.height))
        for t in PdfReader(str(pdf)).pages
    ]


# --------------------------------------------------------------------------
# Quy đổi
# --------------------------------------------------------------------------


def _so_trang(node: dict) -> int | None:
    """`page number` 1-indexed → chỉ số 0-based. Thiếu/hỏng thì trả `None`."""
    v = node.get("page number")
    if not isinstance(v, int) or isinstance(v, bool) or v < 1:
        return None
    return v - 1


def _box(node: dict, trang: int, khung: tuple[float, float]) -> Box | None:
    bb = node.get("bounding box")
    if not isinstance(bb, (list, tuple)) or len(bb) != 4:
        return None
    w, h = khung
    return Box.from_absolute(
        page=trang,
        x0=float(bb[0]),
        y0=float(bb[1]),
        x1=float(bb[2]),
        y1=float(bb[3]),
        page_width=w,
        page_height=h,
        # page_x0/page_y0 để mặc định 0: engine đã trừ gốc MediaBox (phép đo 4).
        y_axis="up",  # ← đo được, không phải giả định. Xem docstring module.
    )


def bang_sang_html(node: dict) -> str:
    """Node `table` → chuỗi `<table>` cho TEDS (B2) ăn.

    `row number`/`column number` của engine là **1-indexed** — ở đây chỉ dùng để
    sắp thứ tự nên không cần quy đổi, nhưng `rowspan`/`colspan` thì phải chép
    đúng, nếu không TEDS chấm sai cấu trúc chứ không chỉ sai chữ.
    """
    dong_html: list[str] = []
    for dong in sorted(
        node.get("rows", []) or [],
        key=lambda d: d.get("row number", 0) if isinstance(d, dict) else 0,
    ):
        if not isinstance(dong, dict):
            continue
        o_html: list[str] = []
        for o in sorted(
            dong.get("cells", []) or [],
            key=lambda c: c.get("column number", 0) if isinstance(c, dict) else 0,
        ):
            if not isinstance(o, dict):
                continue
            the = "th" if o.get("is_header") else "td"
            thuoc_tinh = ""
            if (rs := o.get("row span", 1)) and rs > 1:
                thuoc_tinh += f' rowspan="{int(rs)}"'
            if (cs := o.get("column span", 1)) and cs > 1:
                thuoc_tinh += f' colspan="{int(cs)}"'
            o_html.append(f"<{the}{thuoc_tinh}>{escape(chu_cua_node(o))}</{the}>")
        dong_html.append("<tr>" + "".join(o_html) + "</tr>")
    return "<table>" + "".join(dong_html) + "</table>"


@dataclass(frozen=True, slots=True)
class OpenDataLoaderIdentity:
    name: str
    engine_family: str
    profile: str
    config: Mapping[str, object]
    environment: Mapping[str, object]
    profile_config_sha256: str


DEFAULT_IDENTITY = OpenDataLoaderIdentity(
    name="opendataloader",
    engine_family="opendataloader",
    profile="legacy",
    config={"parser": "java", "table_method": "cluster", "reading_order": "xycut"},
    environment={},
    profile_config_sha256="legacy",
)


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _plain(nested) for key, nested in value.items()}
    if isinstance(value, tuple):
        return [_plain(nested) for nested in value]
    return value


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
        raise AdapterOutputError(
            f"OpenDataLoader {label} is not JSON serializable"
        ) from exc


def _load_psutil() -> Any:
    try:
        import psutil  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError(
            "psutil is required to validate OpenDataLoader hybrid process ownership"
        ) from exc
    return psutil


def _health_payload(url: str, *, timeout: float = 0.5) -> object | None:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return json.loads(response.read())
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return None


def _hybrid_connection_address(connection: object) -> tuple[str, int] | None:
    address = getattr(connection, "laddr", None)
    if not address:
        return None
    try:
        return str(address[0]), int(address[1])
    except (IndexError, TypeError, ValueError):
        return None


def _owned_hybrid_listener_pids(psutil: Any, process: Any) -> list[int]:
    processes = [process, *process.children(recursive=True)]
    listen_status = getattr(psutil, "CONN_LISTEN", "LISTEN")
    owned: set[int] = set()
    for candidate in processes:
        for connection in candidate.net_connections(kind="inet"):
            if (
                getattr(connection, "status", None) == listen_status
                and _hybrid_connection_address(connection)
                == (HYBRID_HOST, HYBRID_PORT)
            ):
                owned.add(int(candidate.pid))
    return sorted(owned)


def _validate_hybrid_versions(versions: object) -> dict[str, str]:
    if not isinstance(versions, dict):
        raise RuntimeError("OpenDataLoader hybrid manifest versions are malformed")
    # Lazy because the default Java profile must remain importable without this extra.
    try:
        from packaging.specifiers import SpecifierSet  # noqa: PLC0415
        from packaging.version import InvalidVersion, Version  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError(
            "packaging is required to validate OpenDataLoader hybrid versions"
        ) from exc
    validated: dict[str, str] = {}
    for distribution, specifier in HYBRID_VERSION_SPECS.items():
        installed = versions.get(distribution)
        if not isinstance(installed, str):
            raise RuntimeError(
                f"OpenDataLoader hybrid manifest versions missing {distribution}"
            )
        try:
            accepted = Version(installed) in SpecifierSet(specifier)
        except InvalidVersion:
            accepted = False
        if not accepted:
            raise RuntimeError(
                f"OpenDataLoader hybrid manifest version {distribution}={installed!r} "
                f"does not satisfy {specifier}"
            )
        validated[distribution] = installed
    return validated


def _validated_hybrid_manifest() -> dict[str, object]:
    manifest_path = Path(
        os.environ.get(HYBRID_MANIFEST_ENV, str(DEFAULT_HYBRID_MANIFEST_PATH))
    )
    try:
        raw = manifest_path.read_bytes()
        payload = json.loads(raw)
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"OpenDataLoader hybrid manifest is missing: {manifest_path}"
        ) from exc
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("OpenDataLoader hybrid manifest is malformed") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("OpenDataLoader hybrid manifest root is malformed")
    try:
        canonical_raw = _canonical_json_bytes(payload, label="hybrid manifest") + b"\n"
    except AdapterOutputError as exc:
        raise RuntimeError("OpenDataLoader hybrid manifest is malformed") from exc
    if raw != canonical_raw:
        raise RuntimeError("OpenDataLoader hybrid manifest is not canonical/tamper-safe")

    if payload.get("manifest_schema_version") != 1 or payload.get("launcher_version") != 1:
        raise RuntimeError("OpenDataLoader hybrid manifest schema/version is unsupported")
    if payload.get("host") != HYBRID_HOST or payload.get("port") != HYBRID_PORT:
        raise RuntimeError("OpenDataLoader hybrid manifest endpoint is not catalog-locked")
    if payload.get("url") != HYBRID_URL:
        raise RuntimeError("OpenDataLoader hybrid manifest URL is not catalog-locked")
    if payload.get("config") != HYBRID_SERVER_CONFIG:
        raise RuntimeError("OpenDataLoader hybrid manifest config is not catalog-locked")
    argv = payload.get("argv")
    if (
        not isinstance(argv, list)
        or not argv
        or not isinstance(argv[0], str)
        or not argv[0]
        or argv[1:] != HYBRID_ARGV_TAIL
    ):
        raise RuntimeError("OpenDataLoader hybrid manifest argv is not catalog-locked")
    if payload.get("health") != {"status": "ok"}:
        raise RuntimeError("OpenDataLoader hybrid manifest health evidence is invalid")
    run_id = payload.get("run_id")
    if (
        not isinstance(run_id, str)
        or len(run_id) != 64
        or any(character not in "0123456789abcdef" for character in run_id)
    ):
        raise RuntimeError("OpenDataLoader hybrid manifest run_id is malformed")
    versions = _validate_hybrid_versions(payload.get("versions"))

    pid = payload.get("pid")
    create_time = payload.get("process_create_time")
    listener_pids = payload.get("listener_pids")
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        raise RuntimeError("OpenDataLoader hybrid manifest pid is malformed")
    if not isinstance(create_time, (int, float)) or isinstance(create_time, bool):
        raise RuntimeError("OpenDataLoader hybrid manifest process_create_time is malformed")
    if (
        not isinstance(listener_pids, list)
        or not listener_pids
        or any(not isinstance(item, int) or isinstance(item, bool) for item in listener_pids)
    ):
        raise RuntimeError("OpenDataLoader hybrid manifest listener evidence is malformed")

    try:
        psutil = _load_psutil()
        process = psutil.Process(pid)
        if not process.is_running():
            raise RuntimeError("OpenDataLoader hybrid manifest process is no longer alive")
        if abs(float(process.create_time()) - float(create_time)) > 0.001:
            raise RuntimeError("OpenDataLoader hybrid manifest process create_time is stale")
        if list(process.cmdline()) != argv:
            raise RuntimeError(
                "OpenDataLoader hybrid manifest argv does not match the live process"
            )
        owned = _owned_hybrid_listener_pids(psutil, process)
    except RuntimeError:
        raise
    except Exception as exc:  # psutil's exception set is platform-specific
        raise RuntimeError(
            "OpenDataLoader hybrid manifest process ownership cannot be verified"
        ) from exc
    expected_listeners = sorted(set(listener_pids))
    if not owned or owned != expected_listeners:
        raise RuntimeError(
            "OpenDataLoader hybrid manifest listener ownership does not match live process"
        )
    if _health_payload(f"{HYBRID_URL}/health") != {"status": "ok"}:
        raise RuntimeError("OpenDataLoader hybrid manifest server is not ready")
    run_seed = dict(payload)
    del run_seed["run_id"]
    expected_run_id = hashlib.sha256(
        _canonical_json_bytes(run_seed, label="hybrid run seed") + b"\n"
    ).hexdigest()
    if run_id != expected_run_id:
        raise RuntimeError("OpenDataLoader hybrid manifest run_id is tampered")

    return {
        "manifest_path": str(manifest_path.resolve()),
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "run_id": run_id,
        "url": HYBRID_URL,
        "pid": pid,
        "process_create_time": float(create_time),
        "listener_pids": owned,
        "versions": versions,
        "config": dict(HYBRID_SERVER_CONFIG),
    }


def _build_result_unchecked(
    *,
    engine_version: str,
    doc_id: str,
    capabilities: frozenset[Capability],
    doc: dict,
    markdown: str,
    trang: list[tuple[float, float]],
    anh_bytes: dict[str, bytes],
    config_fingerprint: dict[str, object],
) -> OcrResult:
    """Ghép JSON của OpenDataLoader thành `OcrResult`.

    Tách khỏi `run()` để test được **mà không cần Java, không cần cài engine**:
    hàm này chỉ đụng dict thuần.
    """
    blocks: list[OcrBlock] = []
    tables: list[OcrTable] = []
    images: list[OcrImage] = []
    thieu_trang: set[object] = set()

    for node in node_khoi(doc):
        so = _so_trang(node)
        if so is None or so >= len(trang):
            # Không rơi về trang 0: box chuẩn hoá sai còn tệ hơn box thiếu, vì nó
            # vẫn được chấm và kéo điểm xuống mà không để lại dấu vết.
            thieu_trang.add(node.get("page number"))
            continue

        bt = map_block_type(node.get("type", ""))
        box = _box(node, so, trang[so])
        chu = chu_cua_node(node)

        cap = node.get("heading level") if bt is BlockType.HEADING else None
        blocks.append(
            OcrBlock(
                block_type=bt,
                box=box,
                text=chu or None,
                level=cap if isinstance(cap, int) else None,
            )
        )

        if bt is BlockType.TABLE:
            tables.append(
                OcrTable(
                    html=bang_sang_html(node),
                    box=box,
                    n_rows=node.get("number of rows"),
                    n_cols=node.get("number of columns"),
                )
            )

        if node.get("type") == "image":
            # `source` là đường dẫn tương đối kiểu `<stem>_images/imageFile1.png`.
            # Ép về str tại biên: `source_id` đi thẳng vào JSON của `prediction/`.
            nguon = node.get("source")
            nguon = str(nguon) if nguon is not None else None
            images.append(
                OcrImage(
                    box=box,
                    data=anh_bytes.get(nguon) if nguon else None,
                    source_id=nguon,
                )
            )

    loi = None
    if thieu_trang:
        loi = (
            "node có `page number` ngoài phạm vi "
            + ", ".join(repr(p) for p in sorted(thieu_trang, key=repr))
            + f" (tài liệu {len(trang)} trang) — các node đó bị bỏ"
        )

    return OcrResult(
        engine="opendataloader",
        engine_version=engine_version,
        doc_id=doc_id,
        capabilities=capabilities,
        text_md=markdown,
        blocks=tuple(blocks),
        images=tuple(images),
        tables=tuple(tables),
        page_sizes=tuple(trang),
        error=loi,
        config_fingerprint=config_fingerprint,
    )


def _node_paths(value: object, path: str = "") -> dict[int, str]:
    paths: dict[int, str] = {}
    if isinstance(value, dict):
        paths[id(value)] = path or "/"
        for key, nested in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            paths.update(_node_paths(nested, f"{path}/{escaped}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            paths.update(_node_paths(nested, f"{path}/{index}"))
    return paths


def build_result(
    *,
    engine_version: str,
    doc_id: str,
    capabilities: frozenset[Capability],
    doc: dict,
    markdown: str,
    trang: list[tuple[float, float]],
    anh_bytes: dict[str, bytes],
    config_fingerprint: dict[str, object],
    identity: OpenDataLoaderIdentity = DEFAULT_IDENTITY,
    raw_json_bytes: bytes | None = None,
    raw_markdown_bytes: bytes | None = None,
) -> OcrResult:
    """Validate and normalize ODL output while retaining exact engine files."""
    if not isinstance(doc, dict) or not isinstance(doc.get("kids"), list):
        raise AdapterOutputError(
            "OpenDataLoader document has malformed kids mapping"
        )
    if not isinstance(markdown, str):
        raise AdapterOutputError("OpenDataLoader markdown output is not a string")
    for node in node_phang(doc):
        if not isinstance(node.get("type"), str):
            raise AdapterOutputError(
                "OpenDataLoader node has malformed type mapping"
            )

    try:
        result = _build_result_unchecked(
            engine_version=engine_version,
            doc_id=doc_id,
            capabilities=capabilities,
            doc=doc,
            markdown=markdown,
            trang=trang,
            anh_bytes=anh_bytes,
            config_fingerprint=config_fingerprint,
        )
    except AdapterOutputError:
        raise
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise AdapterOutputError(
            "OpenDataLoader output cannot be mapped to canonical schema"
        ) from exc

    paths = _node_paths(doc)
    emitted = [
        node
        for node in node_khoi(doc)
        if (page := _so_trang(node)) is not None and page < len(trang)
    ]
    trace = {
        "blocks": {
            str(index): paths[id(node)] for index, node in enumerate(emitted)
        },
        "schema_version": 1,
    }
    if raw_json_bytes is None:
        raw_json_bytes = _canonical_json_bytes(doc, label="raw JSON")
    else:
        try:
            decoded = json.loads(raw_json_bytes)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AdapterOutputError("OpenDataLoader raw JSON is malformed") from exc
        if decoded != doc:
            raise AdapterOutputError(
                "OpenDataLoader raw JSON does not match parsed document"
            )
    if raw_markdown_bytes is None:
        raw_markdown_bytes = markdown.encode("utf-8")
    artifacts = (
        RawArtifact("opendataloader.json", "application/json", raw_json_bytes),
        RawArtifact("opendataloader.md", "text/markdown", raw_markdown_bytes),
        RawArtifact(
            "opendataloader-map.json",
            "application/json",
            _canonical_json_bytes(trace, label="trace map"),
        ),
    )
    return replace(
        result,
        engine=identity.name,
        engine_family=identity.engine_family,
        profile=identity.profile,
        raw_artifacts=artifacts,
    )


class OpenDataLoaderAdapter(Adapter):
    name: ClassVar[str] = "opendataloader"
    capabilities: ClassVar[frozenset[Capability]] = frozenset(
        {
            Capability.TEXT_MD,
            Capability.BLOCK_BBOX,
            Capability.IMAGE_BBOX,
            Capability.IMAGE_BYTES,
            Capability.TABLE_HTML,
            Capability.HEADING_LEVEL,
        }
    )
    # HEADING_LEVEL có, SECTION_HIERARCHY không — và đó là hai chuyện khác nhau.
    # Node `heading` mang sẵn `heading level` nên `OcrBlock.level` là dữ liệu engine
    # tự khai, không phải suy diễn: khai được. Nhưng JSON phẳng, không node nào trỏ
    # về mục cha, nên dựng **cây** thì phải đoán từ thứ tự đọc — A5 cấm đoán, và
    # `section_hierarchy` vẫn để rỗng. Xem docstring `Capability`.

    def __init__(
        self,
        *,
        table_method: str = "cluster",
        include_header_footer: bool = True,
        identity: OpenDataLoaderIdentity = DEFAULT_IDENTITY,
    ) -> None:
        self.identity = identity
        self.name = identity.name
        self.engine_family = identity.engine_family
        self.profile = identity.profile
        config = _plain(identity.config)
        assert isinstance(config, dict)
        if identity.profile == "scan":
            self.table_method = config.get("table_method")
            self.reading_order = config.get("reading_order")
        else:
            self.table_method = str(config.get("table_method", table_method))
            self.reading_order = str(config.get("reading_order", "xycut"))
        self.hybrid = config.get("hybrid")
        self.hybrid_mode = config.get("hybrid_mode")
        self.hybrid_fallback = bool(config.get("hybrid_fallback", False))
        self.include_header_footer = include_header_footer
        self._hardware: Literal["cpu"] = "cpu"
        self._hybrid_evidence: dict[str, object] | None = None
        self._hybrid_evidence_current = False

    @classmethod
    def from_profile(cls, profile: EngineProfile) -> "OpenDataLoaderAdapter":
        if profile.adapter != "opendataloader" or profile.family != "opendataloader":
            raise ProfileConfigError(
                f"OpenDataLoaderAdapter does not accept {profile.name!r}/{profile.family!r}"
            )
        expected: dict[str, tuple[str, dict[str, object], dict[str, object]]] = {
            "opendataloader_default": (
                "default",
                {
                    "parser": "java",
                    "table_method": "cluster",
                    "reading_order": "xycut",
                },
                {},
            ),
            "opendataloader_scan": (
                "scan",
                {
                    "hybrid": "docling-fast",
                    "hybrid_mode": "full",
                    "hybrid_fallback": False,
                },
                {
                    "hybrid_server": {
                        "host": "127.0.0.1",
                        "port": 5002,
                        "force_ocr": True,
                        "ocr_engine": "easyocr",
                        "ocr_languages": ["vi", "en"],
                    }
                },
            ),
        }
        wanted = expected.get(profile.name)
        if wanted is None or profile.profile != wanted[0]:
            raise ProfileConfigError(
                f"unsupported OpenDataLoader profile: {profile.name!r}"
            )
        if _plain(profile.config) != wanted[1]:
            raise ProfileConfigError(
                f"{profile.name}: config does not match frozen OpenDataLoader catalog"
            )
        if _plain(profile.environment) != wanted[2]:
            raise ProfileConfigError(
                f"{profile.name}: environment does not match frozen OpenDataLoader catalog"
            )
        identity = OpenDataLoaderIdentity(
            name=profile.name,
            engine_family="opendataloader",
            profile=profile.profile,
            config=profile.config,
            environment=profile.environment,
            profile_config_sha256=profile.fingerprint,
        )
        return cls(identity=identity)

    def configure_hardware(self, hardware: str) -> str:
        if hardware not in {"cpu", "gpu"}:
            raise ValueError("OpenDataLoader hardware must be 'cpu' or 'gpu'")
        if hardware == "gpu":
            raise RuntimeError(
                "OpenDataLoader 2.5.0 cannot verify GPU device through its Java CLI "
                "or hybrid /health endpoint"
            )
        if self.profile == "scan":
            try:
                candidate = _validated_hybrid_manifest()
                if self._hybrid_evidence is None:
                    self._hybrid_evidence = candidate
                else:
                    self._require_same_hybrid_identity(candidate)
            except RuntimeError:
                self._hybrid_evidence_current = False
                raise
            self._hybrid_evidence_current = True
        self._hardware = "cpu"
        return "cpu"

    def _refresh_hybrid_evidence(self) -> dict[str, object]:
        if self._hybrid_evidence is None:
            raise RuntimeError(
                "OpenDataLoader scan requires configure_hardware('cpu') before run"
            )
        try:
            candidate = _validated_hybrid_manifest()
            self._require_same_hybrid_identity(candidate)
        except RuntimeError:
            self._hybrid_evidence_current = False
            raise
        self._hybrid_evidence_current = True
        return self._hybrid_evidence

    def _require_same_hybrid_identity(self, candidate: Mapping[str, object]) -> None:
        assert self._hybrid_evidence is not None
        identity_fields = (
            "manifest_sha256",
            "run_id",
            "pid",
            "process_create_time",
            "url",
        )
        changed = [
            field
            for field in identity_fields
            if candidate.get(field) != self._hybrid_evidence.get(field)
        ]
        if changed:
            raise RuntimeError(
                "OpenDataLoader hybrid manifest identity rebind rejected: "
                + ", ".join(changed)
            )

    @staticmethod
    def _odl_version() -> str:
        """Phiên bản engine — **không được ném**, cùng lý do với `_java_de_ghi()`.

        `importlib.metadata.version()` ném `PackageNotFoundError` khi extra chưa
        cài. Mà `Adapter.execute()` gọi `config_fingerprint()` *trong nhánh bắt
        lỗi* để dựng bản ghi thất bại — hàm này ném ở đó thì lỗi gốc bị nuốt và
        thay bằng một lỗi thứ hai chẳng liên quan gì.
        """
        from importlib.metadata import PackageNotFoundError, version  # noqa: PLC0415

        try:
            return version("opendataloader-pdf")
        except PackageNotFoundError:
            return "chưa cài"

    def version(self) -> str:
        return self._odl_version()

    def config_fingerprint(self) -> dict[str, object]:
        config = _plain(self.identity.config)
        assert isinstance(config, dict)
        fingerprint = {
            **config,
            "opendataloader_version": self._odl_version(),
            "profile_config_sha256": self.identity.profile_config_sha256,
            "hardware": "cpu",
            "device": "cpu" if self.profile != "scan" else "unverified",
            "hardware_evidence_version": 1,
            "device_evidence": "java-cpu-only" if self.profile != "scan" else "none",
            "include_header_footer": self.include_header_footer,
            "image_output": "external",
            "image_format": "png",
            "markdown_with_html": True,
            "java": self._java_de_ghi(),
        }
        if self.table_method is not None:
            fingerprint["table_method"] = self.table_method
        if self.reading_order is not None:
            fingerprint["reading_order"] = self.reading_order
        if (
            self.profile == "scan"
            and self._hybrid_evidence is not None
            and self._hybrid_evidence_current
        ):
            evidence = self._hybrid_evidence
            versions = evidence["versions"]
            config_evidence = evidence["config"]
            assert isinstance(versions, dict)
            assert isinstance(config_evidence, dict)
            fingerprint.update(
                {
                    "device": "cpu",
                    "device_evidence": "owned-hybrid-launcher-manifest",
                    "hybrid_server": {
                        "host": config_evidence.get("host", "127.0.0.1"),
                        "port": config_evidence.get("port", 5002),
                        "force_ocr": config_evidence["force_ocr"],
                        "ocr_engine": config_evidence["ocr_engine"],
                        "ocr_languages": list(config_evidence["ocr_languages"]),
                    },
                    "cpu_enforcement": dict(config_evidence["device_enforcement"]),
                    "cpu_enforcement_method": config_evidence[
                        "device_enforcement_method"
                    ],
                    "opendataloader_version": versions["opendataloader-pdf"],
                    "docling_version": versions["docling"],
                    "easyocr_version": versions["easyocr"],
                    "pypdf_version": versions["pypdf"],
                    "hybrid_dependency_versions": dict(versions),
                    "hybrid_server_versions": {
                        name: versions[name]
                        for name in ("fastapi", "python-multipart", "uvicorn")
                    },
                    "hybrid_manifest_sha256": evidence["manifest_sha256"],
                    "hybrid_manifest_run_id": evidence["run_id"],
                    "hybrid_process_pid": evidence["pid"],
                    "hybrid_process_create_time": evidence["process_create_time"],
                    "hybrid_listener_pids": list(evidence["listener_pids"]),
                }
            )
        return fingerprint

    @staticmethod
    def _java_de_ghi() -> str:
        """Đường dẫn java cho dấu vân tay — **không được ném**.

        `Adapter.execute()` bắt lỗi của `run()` rồi gọi `config_fingerprint()` để
        dựng bản ghi thất bại. Nếu hàm này cũng ném thì lỗi gốc bị nuốt, cả lượt
        chạy đổ ngay tài liệu đầu tiên thay vì ghi `failed=True` và đi tiếp.
        """
        try:
            return str(_java())
        except RuntimeError as exc:
            return f"không tìm thấy: {exc}"

    def run(self, doc_path: Path) -> OcrResult:
        with tempfile.TemporaryDirectory(prefix="odl-") as tmp:
            ra = Path(tmp)
            kwargs: dict[str, object] = {
                "table_method": self.table_method,
                "reading_order": self.reading_order,
                "include_header_footer": self.include_header_footer,
            }
            if self.profile == "scan":
                self._refresh_hybrid_evidence()
                environment = _plain(self.identity.environment)
                assert isinstance(environment, dict)
                server = environment["hybrid_server"]
                assert isinstance(server, dict)
                kwargs.update(
                    hybrid=self.hybrid,
                    hybrid_mode=self.hybrid_mode,
                    hybrid_fallback=self.hybrid_fallback,
                    hybrid_url=f"http://{server['host']}:{server['port']}",
                )
            chay_cli([doc_path], ra, **kwargs)
            stem = doc_path.stem
            raw_json_bytes = (ra / f"{stem}.json").read_bytes()
            try:
                doc = json.loads(raw_json_bytes)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise AdapterOutputError(
                    "OpenDataLoader emitted malformed JSON"
                ) from exc
            md_path = ra / f"{stem}.md"
            if not md_path.is_file():
                raise AdapterOutputError(
                    "OpenDataLoader Markdown output is missing"
                )
            raw_markdown_bytes = md_path.read_bytes()
            try:
                markdown = raw_markdown_bytes.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise AdapterOutputError(
                    "OpenDataLoader emitted non-UTF-8 markdown"
                ) from exc
            anh_bytes = {
                str(p.relative_to(ra)).replace("\\", "/"): p.read_bytes()
                for p in ra.rglob("*_images/*")
                if p.is_file()
            }

        return build_result(
            engine_version=self.version(),
            doc_id=stem,
            capabilities=self.capabilities,
            doc=doc,
            markdown=markdown,
            trang=kich_thuoc_trang(doc_path),
            anh_bytes=anh_bytes,
            config_fingerprint=self.config_fingerprint(),
            identity=self.identity,
            raw_json_bytes=raw_json_bytes,
            raw_markdown_bytes=raw_markdown_bytes,
        )
