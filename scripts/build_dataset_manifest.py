#!/usr/bin/env python3
"""Sinh `datasets/manifest.json` từ `datasets/catalog.json` + bộ mẫu trên đĩa.

    py -3 scripts/build_dataset_manifest.py            # ghi manifest.json
    py -3 scripts/build_dataset_manifest.py --verify   # đối chiếu, không ghi; exit 2 nếu lệch

`--verify` là cổng chạy trước mỗi lần công bố. Nó không kiểm "file có tồn tại" mà kiểm
**manifest đã commit có còn mô tả đúng đĩa hiện tại hay không**: thêm một PDF, sửa một
nhãn, hay đổi một dòng trong `corrections.jsonl` đều làm nó đỏ. Đó là điểm khác nhau
giữa một manifest và một tờ khai.

Manifest là **đầu ra**, không phải nguồn. Sửa tay nó thì cổng checksum mất tác dụng, và
nguyên nhân duy nhất khiến bảng xếp hạng truy ngược được về dữ liệu cũng mất theo.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ocr_bench.dataset_manifest import (  # noqa: E402
    CorrectionError,
    DatasetManifestError,
    build_manifest,
)

DICH = ROOT / "datasets" / "manifest.json"


def _viet(obj: dict) -> str:
    # `sort_keys` + `indent=2` + newline cuối: manifest được commit, nên diff của nó
    # phải đọc được bằng mắt. `ensure_ascii=False` để lý do tiếng Việt không thành
    # ạ — reviewer đọc lý do chứ không đọc escape.
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def _tom_tat(m: dict) -> str:
    ds = ", ".join(
        f"{d['name']}={d['document_count']}" for d in m["datasets"] if d["status"] == "included"
    )
    return (
        f"{m['coverage']['document_count']} tài liệu ({ds}); "
        f"loại ra {len(m['excluded_documents'])}; "
        f"ngôn ngữ {m['coverage']['languages']}; "
        f"bản chép tiếng Việt: {m['coverage']['vietnamese_transcript']}"
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args(argv)

    try:
        manifest = build_manifest(ROOT)
    except (DatasetManifestError, CorrectionError) as exc:
        print(f"catalog/bộ mẫu không hợp lệ: {exc}", file=sys.stderr)
        return 2

    moi = _viet(manifest)
    if args.verify:
        if not DICH.exists():
            print(f"chưa có {DICH.relative_to(ROOT)} — chạy lại không có --verify", file=sys.stderr)
            return 2
        cu = DICH.read_text(encoding="utf-8")
        if cu != moi:
            print(
                f"{DICH.relative_to(ROOT)} không khớp đĩa hiện tại. "
                f"Đĩa: {_tom_tat(manifest)}",
                file=sys.stderr,
            )
            try:
                truoc = json.loads(cu)
            except json.JSONDecodeError:
                print("manifest đã commit không phải JSON hợp lệ", file=sys.stderr)
                return 2
            print(f"Manifest: {_tom_tat(truoc)}", file=sys.stderr)
            _in_khac_biet(truoc, manifest)
            return 2
        print(f"Khớp: {_tom_tat(manifest)}")
        return 0

    DICH.parent.mkdir(parents=True, exist_ok=True)
    # `newline="\n"`: mặc định trên Windows là dịch `\n` thành CRLF khi ghi, trong khi
    # `.gitattributes` ép `*.json` về LF lúc checkout. Để lệch thì `--verify` xanh trên
    # máy vừa sinh ra file và đỏ trên máy vừa clone — cổng chỉ nổ với người vô can.
    #
    # Chiều đọc thì ngược lại: `read_text` mặc định bật universal newlines, tức CRLF trên
    # đĩa vẫn đọc ra `\n`. Nới ở chiều đọc mà siết ở chiều ghi là có chủ ý — một bản
    # checkout lỡ thành CRLF vẫn so sánh đúng thay vì báo "lệch manifest" vì lý do
    # không liên quan gì tới dữ liệu.
    DICH.write_text(moi, encoding="utf-8", newline="\n")
    print(f"{DICH.relative_to(ROOT)} — {_tom_tat(manifest)}")
    return 0


def _in_khac_biet(truoc: dict, sau: dict) -> None:
    """Chỉ ra tài liệu nào thêm/mất/đổi checksum. `--verify` báo đỏ mà không nói chỗ
    nào đỏ thì người nhận phải tự diff 200 dòng JSON — và thường sẽ chọn ghi đè."""
    a = {r["document_id"]: r for r in truoc.get("documents", ())}
    b = {r["document_id"]: r for r in sau.get("documents", ())}
    for nhan, ds in (
        ("chỉ có trên đĩa", sorted(set(b) - set(a))),
        ("chỉ có trong manifest", sorted(set(a) - set(b))),
        (
            "đổi checksum/nhãn",
            sorted(d for d in set(a) & set(b) if a[d] != b[d]),
        ),
    ):
        if ds:
            print(f"  {nhan}: {len(ds)}", file=sys.stderr)
            for d in ds[:10]:
                print(f"    {d}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
