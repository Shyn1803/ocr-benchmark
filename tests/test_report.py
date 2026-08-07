"""Test bản công bố D1 (TASK-087).

Bốn AC của task này, và cái mà mỗi test thật sự chặn:

* **AC-01** — `manifest.json` đủ version. Chặn: dữ liệu trộn hai lượt chạy khác
  version mà bảng vẫn in ra bình thường.
* **AC-02** — tách theo nhóm. Chặn: một tài liệu rơi vào hai nhóm, hoặc lặng lẽ
  rơi ra ngoài mọi nhóm.
* **AC-03** — mọi trung bình kèm FailRate. Chặn: có chỗ tự `f"{x:.3f}"`.
* **AC-04** — chạy lại ra đúng cùng số. Chặn: nguồn bất định lọt vào.

Test AC-03 (`test_moi_o_so_deu_kem_fail_rate`) đọc **markdown đã sinh ra** rồi soi
từng ô. Viết bằng cách mock `Aggregate.cell()` thì nó chỉ kiểm rằng ta gọi đúng hàm
mình vừa mock — không kiểm gì cả.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from ocr_bench import report
from ocr_bench.scorer import ScoreTable
from ocr_bench.types import Capability, MetricResult, NAReason, OcrResult

GOC = Path(__file__).resolve().parents[1]

# Ba dạng ô hợp lệ, không có dạng thứ tư:
#   0.812 (fail 10%)          — đo được
#   N/A                       — thiếu năng lực, không đo
#   — (10 hỏng, 0 chấm được)  — có mẫu số nhưng không chấm được cái nào
O_HOP_LE = re.compile(r"^(\d\.\d{3} \(fail \d+%\)|N/A|— \(\d+ hỏng, 0 chấm được\))$")


def _kq(engine: str, doc: str, *, ver: str = "1.0") -> OcrResult:
    return OcrResult(
        engine=engine,
        engine_version=ver,
        doc_id=doc,
        capabilities=frozenset({Capability.TEXT_MD}),
        text_md="x",
    )


def _diem(metric: str, engine: str, doc: str, value: float | None,
          na: NAReason | None = None) -> MetricResult:
    return MetricResult(
        metric=metric, engine=engine, doc_id=doc, value=value, na_reason=na
    )


@pytest.fixture
def bang_nho() -> ScoreTable:
    """2 metric × 3 engine. `c` hỏng sạch — đúng ca sinh ra ô "— (n hỏng...)"."""
    rows = []
    for m in ("cer", "heading"):
        for d in ("d1", "d2"):
            rows.append(_diem(m, "a", d, 0.8))
            rows.append(_diem(m, "b", d, None, NAReason.MISSING_CAPABILITY))
            rows.append(_diem(m, "c", d, None, NAReason.ENGINE_FAILED))
    return ScoreTable(tuple(rows))


# ----------------------------------------------------------------- AC-01 manifest


def test_manifest_co_du_version_engine(bang_nho):
    res = [_kq("a", "d1"), _kq("b", "d1"), _kq("c", "d1")]
    mani = report.dung_manifest(res, bang_nho, generated_at="T")
    assert {e["engine"] for e in mani["engines"]} == {"a", "b", "c"}
    assert all(e["version"] for e in mani["engines"])


def test_manifest_nem_khi_mot_engine_co_hai_version(bang_nho):
    """Ca dương của guard: guard chỉ có giá trị khi có test làm nó ném."""
    res = [_kq("a", "d1", ver="1.0"), _kq("a", "d2", ver="2.0")]
    with pytest.raises(report.BaoCaoError, match="nhiều hơn một"):
        report.dung_manifest(res, bang_nho, generated_at="T")


def test_manifest_ghi_version_thu_vien_cham_diem():
    lib = report.phien_ban_thu_vien()
    assert set(lib) == set(report.THU_VIEN_CHAM_DIEM)
    # Gói chưa cài phải ghi "chưa cài", KHÔNG được biến mất khỏi dict — biến mất
    # thì manifest của máy thiếu psutil trông giống hệt máy đủ.
    assert all(isinstance(v, str) and v for v in lib.values())
    assert report.phien_ban_thu_vien(["khong_ton_tai_dau_x"]) == {
        "khong_ton_tai_dau_x": "chưa cài"
    }


def test_manifest_danh_dau_cay_ban(tmp_path):
    g = report.thong_tin_git(tmp_path)  # không phải repo git
    assert set(g) == {"commit", "dirty"}
    that = report.thong_tin_git(GOC)
    assert that["dirty"] in (True, False)


# -------------------------------------------------------------------- AC-02 nhóm


def test_nhom_tai_lieu_phu_kin_va_khong_chong_nhau():
    nhom = report.nhom_tai_lieu()
    assert nhom, "không nạp được nhóm nào — bộ mẫu hỏng?"
    # dict ⇒ mỗi doc đúng một nhóm theo cấu trúc; kiểm tên nhóm có tiền tố bộ mẫu
    assert all(v.startswith(("doclaynet/", "olmocr/")) for v in nhom.values())
    # `sample_minimal` không thuộc bộ nào ⇒ phải VẮNG MẶT, không được gán nhóm "khác"
    assert "sample_minimal" not in nhom


def test_by_group_co_du_sau_nhom_doclaynet():
    md = report.bao_cao_by_group(
        ScoreTable(tuple(
            _diem("cer", "a", d, 0.5) for d in report.nhom_tai_lieu()
        ))
    )
    tieu_de = [l for l in md.splitlines() if l.startswith("## ")]
    assert sum(1 for t in tieu_de if "doclaynet/" in t) == 6


def test_moi_bang_ghi_n_cua_tung_engine(bang_nho):
    md = report.bang_markdown(bang_nho)
    assert "**n (tài liệu)**" in md
    # dòng n phải đứng ngay dưới header+separator, trước mọi dòng điểm
    dong = md.splitlines()
    assert "n (tài liệu)" in dong[2]


# --------------------------------------------------------------- AC-03 ô + failrate


def test_moi_o_so_deu_kem_fail_rate(bang_nho):
    """Test khoá. Đọc markdown đã sinh, soi từng ô — không mock gì cả."""
    md = "\n".join([
        report.bang_markdown(bang_nho),
        report.bao_cao_overall(bang_nho, {"canh_bao": []}),
        report.bao_cao_by_group(bang_nho),
        report.bao_cao_common_set(bang_nho, {"a": {"d1"}, "b": {"d1"}, "c": {"d1"}}),
    ])
    o_da_soi = 0
    for dong in md.splitlines():
        if not dong.startswith("| ") or "---" in dong or "n (tài liệu)" in dong:
            continue
        cot = [c.strip() for c in dong.strip("|").split("|")]
        if cot[0] in ("metric",):
            continue
        for o in cot[1:]:
            assert O_HOP_LE.match(o), f"ô không hợp lệ: {o!r} ở dòng {dong!r}"
            o_da_soi += 1
    assert o_da_soi >= 6, "không soi được ô nào — fixture hỏng, test xanh giả"


def test_o_na_khong_bi_bo_dong(bang_nho):
    """Ca âm: engine chỉ toàn N/A vẫn phải có cột. Bỏ đi = làm engine yếu trông mạnh."""
    md = report.bang_markdown(bang_nho)
    assert "| b |" in md.splitlines()[0] or " b " in md.splitlines()[0]
    assert "N/A" in md


def test_o_hong_sach_khong_in_0_000(bang_nho):
    """`c` hỏng cả 2 tài liệu ⇒ ô phải nói "không chấm được", không phải "0.000"."""
    o = bang_nho.cell("cer", "c").cell()
    assert o == "— (2 hỏng, 0 chấm được)"
    assert "0.000" not in report.bang_markdown(bang_nho)


# ------------------------------------------------------------------- AC-04 tất định


def test_raw_json_khong_lam_tron():
    b = ScoreTable((_diem("cer", "a", "d1", 0.123456789012345),))
    d = json.loads(report.raw_json(b, generated_at="T"))
    assert d["rows"][0]["value"] == 0.123456789012345


def test_raw_json_sap_xep_on_dinh():
    xuoi = ScoreTable((
        _diem("cer", "a", "d1", 0.1), _diem("cer", "b", "d2", 0.2),
    ))
    nguoc = ScoreTable(tuple(reversed(xuoi.rows)))
    assert report.raw_json(xuoi, generated_at="T") == report.raw_json(
        nguoc, generated_at="T"
    )


def _chay_script(out: Path, *them: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GOC / "scripts" / "d1_report.py"), "--out", str(out), *them],
        cwd=GOC, capture_output=True, text=True,
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )


@pytest.mark.slow
def test_chay_hai_lan_cho_raw_json_giong_het(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    assert _chay_script(a).returncode == 0
    assert _chay_script(b).returncode == 0
    ja = json.loads((a / "raw.json").read_text(encoding="utf-8"))
    jb = json.loads((b / "raw.json").read_text(encoding="utf-8"))
    del ja["generated_at"], jb["generated_at"]
    assert ja == jb
    assert ja["rows"], "không có dòng nào — script chấm hụt, test xanh giả"


@pytest.mark.slow
def test_file_ghi_ra_khong_co_crlf(tmp_path):
    """`.gitattributes` khai `eol=lf`, nên blob trong git luôn là LF.

    Nếu script ghi CRLF (mặc định của Python trên Windows) thì bản trên đĩa khác
    bản checkout ra ở **mọi dòng**, và người kiểm AC-04 bằng `diff` thấy một khác
    biệt toàn tập không liên quan gì tới con số. Báo động giả kiểu đó tệ hơn không
    kiểm, vì nó dạy người ta bỏ qua phép kiểm.
    """
    out = tmp_path / "x"
    assert _chay_script(out).returncode == 0
    da_soi = 0
    for f in sorted(out.iterdir()):
        b = f.read_bytes()
        assert b"\r\n" not in b, f"{f.name} ghi CRLF"
        assert b"\n" in b, f"{f.name} không có dòng nào — soi rỗng"
        da_soi += 1
    assert da_soi == 5, f"chờ 5 file, thấy {da_soi}"


def test_khong_ghi_de_history_neu_thieu_force(tmp_path):
    """Ca âm: ghi đè lặng lẽ một bản `history/` là làm mất đúng thứ D1 sinh ra để giữ."""
    out = tmp_path / "co_san"
    out.mkdir()
    (out / "raw.json").write_text("cu", encoding="utf-8")
    p = _chay_script(out)
    assert p.returncode == 1
    assert "--force" in p.stdout
    assert (out / "raw.json").read_text(encoding="utf-8") == "cu"


# --------------------------------------------------------------- tập chung quá nhỏ


def test_tap_chung_qua_nho_thi_canh_bao_thay_vi_in_bang():
    cov = {"x": {"d1", "d2"}, "y": {"d2", "d3"}}          # giao = {"d2"} → 1
    chung = cov["x"] & cov["y"]
    # Khẳng định fixture THẬT SỰ dựng ra ca cần kiểm, nếu không test xanh mà
    # chẳng kiểm gì (đúng cái bẫy của TASK-091).
    assert 0 < len(chung) < report.TOI_THIEU_TAP_CHUNG

    bang = ScoreTable(tuple(
        _diem("cer", e, d, 0.5) for e in cov for d in cov[e]
    ))
    md = report.bao_cao_common_set(bang, cov, nhom_engine=[("x", "y")])
    assert "quá nhỏ để so" in md
    assert "| cer |" not in md, "vẫn in bảng dù tập chung quá nhỏ"


def test_tap_chung_du_lon_thi_van_in_bang():
    """Ca đối chứng: ngưỡng không được chặn cả nhóm hợp lệ."""
    docs = {f"d{i}" for i in range(report.TOI_THIEU_TAP_CHUNG + 2)}
    cov = {"x": set(docs), "y": set(docs)}
    bang = ScoreTable(tuple(_diem("cer", e, d, 0.5) for e in cov for d in docs))
    md = report.bao_cao_common_set(bang, cov, nhom_engine=[("x", "y")])
    assert "quá nhỏ để so" not in md
    assert "| cer |" in md


# ------------------------------------------------------------ nhánh phòng thủ


def test_nhom_tai_lieu_thieu_bo_mau_thi_rong_chu_khong_nem(tmp_path):
    """Chạy trong cây không có `ground-truth/` lẫn `pdfs/` — không được ném."""
    assert report.nhom_tai_lieu(tmp_path) == {}


def test_thong_tin_git_khong_co_git_thi_ghi_khong_ro(tmp_path, monkeypatch):
    def _no(*a, **k):
        raise OSError("không có git")

    monkeypatch.setattr(report.subprocess, "run", _no)
    assert report.thong_tin_git(tmp_path) == {"commit": "không rõ", "dirty": None}


def test_dirty_khong_tinh_thu_muc_history(tmp_path):
    """`history/` là đầu ra của chính lượt chạy — nó không được tự làm bẩn báo cáo
    của mình. Nhưng một file nguồn chưa commit thì PHẢI làm `dirty` bật lên."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "x"],
                   cwd=tmp_path, check=True,
                   env={**__import__("os").environ,
                        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
    assert report.thong_tin_git(tmp_path)["dirty"] is False

    (tmp_path / "history").mkdir()
    (tmp_path / "history" / "raw.json").write_text("{}", encoding="utf-8")
    assert report.thong_tin_git(tmp_path)["dirty"] is False, "history/ tự làm bẩn"

    (tmp_path / "nguon.py").write_text("x = 1", encoding="utf-8")
    assert report.thong_tin_git(tmp_path)["dirty"] is True, "bỏ sót file nguồn mới"


def test_canh_bao_rong_khi_khong_co_engine():
    assert report._canh_bao({}) == []


def test_canh_bao_goi_ten_engine_chay_it_tai_lieu():
    cb = report._canh_bao({"to": set(f"d{i}" for i in range(100)), "nho": {"d0"}})
    assert any("`nho` chỉ có 1/100" in c for c in cb)
    assert not any(c.startswith("`to`") for c in cb)


def test_bang_rong_thi_noi_ra_chu_khong_in_bang_trong():
    assert "không có engine" in report.bang_markdown(ScoreTable(()))


def test_overall_in_canh_bao_truoc_bang(bang_nho):
    md = report.bao_cao_overall(bang_nho, {"canh_bao": ["ĐỌC CÁI NÀY TRƯỚC"]})
    assert md.index("ĐỌC CÁI NÀY TRƯỚC") < md.index("## Bảng")


def test_manifest_dem_tai_lieu_ngoai_bo_mau(bang_nho):
    res = [_kq("a", "khong_thuoc_bo_mau_nao_x")]
    mani = report.dung_manifest(res, bang_nho, generated_at="T")
    assert mani["engines"][0]["n_ngoai_bo_mau"] == 1
    assert mani["engines"][0]["theo_nhom"] == {}


def test_manifest_dem_tai_lieu_theo_nhom():
    """Đối chứng của test trên: tài liệu THUỘC bộ mẫu phải vào `theo_nhom`."""
    nhom = report.nhom_tai_lieu()
    doc, ten_nhom = next(iter(sorted(nhom.items())))
    mani = report.dung_manifest(
        [_kq("a", doc)], ScoreTable((_diem("cer", "a", doc, 0.5),)), generated_at="T"
    )
    assert mani["engines"][0]["theo_nhom"] == {ten_nhom: 1}
    assert mani["engines"][0]["n_ngoai_bo_mau"] == 0


def test_common_set_bo_qua_nhom_thieu_engine(bang_nho):
    md = report.bao_cao_common_set(bang_nho, {"a": {"d1"}}, nhom_engine=[("a", "vang_mat")])
    assert "Bỏ qua" in md and "`vang_mat`" in md
