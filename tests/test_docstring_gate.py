"""Chặn phát biểu cổng C2 **cũ** quay lại tài liệu và mã nguồn.

Bối cảnh: phát biểu *"engine giả phải đứng bét mọi metric; metric nào không xếp được
như vậy thì metric đó sai"* đã bị bác ở **D-010** (`.claude/context/DECISIONS.md`,
2026-08-10). Nó bị bác vì `noop` là sàn **theo cấu tạo** — đứng bét là hiển nhiên,
không chứng minh gì về thước đo. Cổng hiện tại: `sabotage` phải thấp hơn **chính
engine nguồn** của nó, so ngặt, `noop` bị loại khỏi tập so sánh.

Vì sao cần một test cho việc này thay vì chỉ sửa tay: D-010 sửa 3 trong 4 chỗ mang
phát biểu cũ và **sót** docstring của `discrimination.py`; sót được vì đoạn văn vẫn
đọc mạch lạc — chỉ là mạch lạc theo một định nghĩa đã chết. Mắt người không bắt loại
lỗi này (lần quét sau còn tìm ra thêm 3 chỗ nữa: `noop.py`, `__init__.py`,
`metrics/base.py`). Grep thì bắt được.

Luật: được phép **trích lại** phát biểu cũ để bác nó — nên một dòng khớp vẫn xanh nếu
cửa sổ quanh nó có dấu hiệu bác bỏ (`D-010`, `đã bị bác`, `không phải đứng bét`, …).
Nhắc lại nó như một luật đang có hiệu lực thì đỏ.
"""

from __future__ import annotations

import re
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
THU_MUC_QUET = ("src", "results", "scripts")
DUOI_FILE = (".py", ".md")

# Dạng **khẳng định** của luật đã chết. Chỉ bắt dạng khẳng định, không bắt mọi lần
# nhắc tới "đứng bét" — cụm đó vẫn xuất hiện hợp lệ trong các đoạn giải thích.
MAU_CAM = (
    re.compile(r"phải đứng bét"),
    re.compile(r"(metric|thước đo) đó sai"),
    re.compile(r"đứng bét (mọi metric|toàn bảng)"),
)

# Có bất kỳ dấu hiệu nào trong cửa sổ ⇒ đoạn đó đang *bác* phát biểu cũ, không phải
# đang phát biểu nó. `\*{0,2}` để nuốt phần in đậm Markdown xen giữa ("**không** phải").
DAU_HIEU_BAC = (
    re.compile(r"D-010"),
    re.compile(r"đã bị bác"),
    re.compile(r"Phát biểu cũ"),
    re.compile(r"(?i)\*{0,2}không\*{0,2}\s+(phải|còn)\b"),
)
BAN_KINH = 4  # số dòng nhìn lên/xuống quanh dòng khớp


def _co_dau_hieu_bac(dong: list[str], i: int) -> bool:
    dau = max(0, i - BAN_KINH)
    cuoi = min(len(dong), i + BAN_KINH + 1)
    cua_so = "\n".join(dong[dau:cuoi])
    return any(d.search(cua_so) for d in DAU_HIEU_BAC)


def _quet(goc: Path) -> list[tuple[Path, int, str]]:
    """Trả về mọi dòng nhắc lại luật cũ mà **không** kèm dấu hiệu bác bỏ."""
    vi_pham: list[tuple[Path, int, str]] = []
    for thu_muc in THU_MUC_QUET:
        d = goc / thu_muc
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*")):
            if f.suffix not in DUOI_FILE or "__pycache__" in f.parts:
                continue
            if f.resolve() == Path(__file__).resolve():
                continue
            try:
                dong = f.read_text(encoding="utf-8").splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            for i, noi_dung in enumerate(dong):
                if any(m.search(noi_dung) for m in MAU_CAM) and not _co_dau_hieu_bac(dong, i):
                    vi_pham.append((f.relative_to(goc), i + 1, noi_dung.strip()))
    return vi_pham


def test_khong_con_phat_bieu_cong_cu() -> None:
    vi_pham = _quet(GOC)
    assert not vi_pham, "Phát biểu cổng C2 cũ (đã bị bác ở D-010) xuất hiện trở lại:\n" + "\n".join(
        f"  {f}:{n}: {t}" for f, n, t in vi_pham
    )


def test_chinh_bo_bat_duoc_vi_pham(tmp_path: Path) -> None:
    """Ca âm: bộ bắt phải đỏ khi luật cũ được chèn lại mà không có dấu hiệu bác bỏ.

    Không có ca này thì `test_khong_con_phat_bieu_cong_cu` có thể xanh vĩnh viễn vì
    một lỗi regex chứ không phải vì mã nguồn sạch.
    """
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "gia.py").write_text(
        '"""Engine giả phải đứng bét mọi metric. Không xếp được thì metric đó sai."""\n',
        encoding="utf-8",
    )
    assert _quet(tmp_path), "Bộ bắt không nhận ra phát biểu cũ — regex hỏng"


def test_trich_de_bac_thi_khong_bi_tinh_la_vi_pham(tmp_path: Path) -> None:
    """Ca đối chứng: trích lại luật cũ **để bác** thì phải xanh."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "that.py").write_text(
        '"""Phát biểu cũ "engine giả phải đứng bét mọi metric" đã bị bác ở D-010."""\n',
        encoding="utf-8",
    )
    assert not _quet(tmp_path), "Đoạn đang bác phát biểu cũ bị tính nhầm thành vi phạm"
