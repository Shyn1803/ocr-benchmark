"""Dựng Java cho OpenDataLoader mà KHÔNG cài gì vào máy.

OpenDataLoader là wrapper Python gọi một file `.jar` — nó cần JRE 11+. Máy phát
triển ở đây không có `java`, không có `winget`, và cài JDK toàn máy là việc nằm
ngoài phạm vi `ocr-bench/`. Nên script này tải một bản **Temurin JRE bỏ túi**
(zip, không có bộ cài) về `.tools/`, kiểm SHA-256, giải nén, rồi in ra đường dẫn
`java.exe`.

    py -3 scripts/setup_java.py            # tải nếu chưa có, in đường dẫn
    py -3 scripts/setup_java.py --check    # chỉ kiểm, không tải

`.tools/` nằm trong `.gitignore`. Chạy lại nhiều lần không tải lại.

Vì sao không dùng JRE mà DBeaver mang theo (`C:/Program Files/DBeaver/jre`, đúng
Temurin 21): nó chạy được, nhưng nó là phụ phẩm của một phần mềm không liên quan —
gỡ DBeaver là bench chết, và không tái lập được trên máy khác. Script này thì tái
lập được.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / ".tools"

# Bản chính chủ Eclipse Adoptium. Ghim ở major 21 (LTS); bản vá lấy từ API để
# khỏi ôm một URL sẽ mục. Checksum lấy cùng lượt API đó và LUÔN được kiểm.
API = (
    "https://api.adoptium.net/v3/assets/latest/21/hotspot"
    "?architecture=x64&image_type=jre&os=windows&vendor=eclipse"
)

JAVA_TOI_THIEU = 11

# api.adoptium.net trả 403 cho User-Agent mặc định của urllib.
UA = {"User-Agent": "ocr-bench/setup_java (+https://api.adoptium.net)"}


def _mo(url: str, timeout: int):
    return urllib.request.urlopen(  # noqa: S310 — HTTPS, host cố định
        urllib.request.Request(url, headers=UA), timeout=timeout
    )


def _tai_metadata() -> tuple[str, str, str]:
    """Trả (release_name, url, sha256) của bản JRE mới nhất."""
    with _mo(API, 60) as r:
        data = json.loads(r.read())
    if not data:
        raise SystemExit("Adoptium không trả bản nào cho windows/x64/jre/21.")
    asset = data[0]
    pkg = asset["binary"]["package"]
    return asset["release_name"], pkg["link"], pkg["checksum"]


def _tai_file(url: str, dich: Path, sha256_cho_doi: str) -> None:
    dich.parent.mkdir(parents=True, exist_ok=True)
    tam = dich.with_suffix(dich.suffix + ".tmp")
    print(f"Tải {url}")
    with _mo(url, 600) as r, tam.open("wb") as f:
        h = hashlib.sha256()
        while chunk := r.read(1 << 20):
            f.write(chunk)
            h.update(chunk)
    thuc_te = h.hexdigest()
    if thuc_te != sha256_cho_doi:
        tam.unlink(missing_ok=True)
        raise SystemExit(
            f"SHA-256 lệch.\n  chờ đợi: {sha256_cho_doi}\n  thực tế: {thuc_te}"
        )
    tam.replace(dich)
    print(f"  OK, SHA-256 khớp ({dich.stat().st_size:,} byte)")


def _giai_nen(zip_path: Path, dich: Path) -> Path:
    """Giải nén rồi trả về thư mục gốc JRE (cái có `bin/java.exe`)."""
    if dich.exists():
        shutil.rmtree(dich)
    dich.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dich)
    for java in dich.rglob("bin/java.exe"):
        return java.parent.parent
    raise SystemExit(f"Giải nén xong nhưng không thấy bin/java.exe trong {dich}")


def _phien_ban(java: Path) -> int:
    """Số major của `java -version`. `21.0.12` → 21; `1.8.0` → 8."""
    out = subprocess.run(  # noqa: S603
        [str(java), "-version"], capture_output=True, text=True, timeout=60
    )
    text = out.stderr + out.stdout
    for dong in text.splitlines():
        if "version" in dong and '"' in dong:
            so = dong.split('"')[1]
            phan = so.split(".")
            major = int(phan[0])
            return int(phan[1]) if major == 1 and len(phan) > 1 else major
    raise SystemExit(f"Không đọc được phiên bản từ:\n{text}")


def tim_java() -> Path | None:
    """Java dùng được (>= 11), theo thứ tự: .tools/ → JAVA_HOME → PATH."""
    ung_vien: list[Path] = []
    # `rglob`, KHÔNG phải `glob("jre-*/bin/java.exe")`: zip của Temurin bung ra
    # thêm một tầng (`jre-<tên>/<tên>-jre/bin/java.exe`), nên mẫu một tầng không
    # khớp gì cả. Lỗi này im lặng — `tim_java()` chỉ rơi xuống PATH, và ai đã
    # export PATH bằng tay thì không bao giờ thấy.
    ung_vien += sorted(TOOLS.rglob("jre-*/**/bin/java.exe"))
    if jh := os.environ.get("JAVA_HOME"):
        ung_vien.append(Path(jh) / "bin" / "java.exe")
    if p := shutil.which("java"):
        ung_vien.append(Path(p))
    for java in ung_vien:
        if java.exists() and _phien_ban(java) >= JAVA_TOI_THIEU:
            return java
    return None


def bao_dam_java() -> Path:
    if java := tim_java():
        return java
    ten, url, sha = _tai_metadata()
    zip_path = TOOLS / f"{ten}.zip"
    if not zip_path.exists():
        _tai_file(url, zip_path, sha)
    goc = _giai_nen(zip_path, TOOLS / f"jre-{ten}")
    java = goc / "bin" / "java.exe"
    v = _phien_ban(java)
    if v < JAVA_TOI_THIEU:
        raise SystemExit(f"Tải về Java {v}, cần >= {JAVA_TOI_THIEU}.")
    zip_path.unlink(missing_ok=True)
    return java


def main() -> int:
    # Console Windows mặc định cp1252, không in được tiếng Việt có dấu.
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="chỉ kiểm, không tải")
    args = ap.parse_args()

    java = tim_java() if args.check else bao_dam_java()
    if java is None:
        print("Không tìm thấy Java >= 11. Bỏ --check để script tự tải bản bỏ túi.")
        return 1

    print(f"java   = {java}")
    print(f"major  = {_phien_ban(java)}")
    print(f"JAVA_HOME cho OpenDataLoader = {java.parent.parent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
