"""Repo-level sanity check — bắt lỗi cấu trúc nhanh khi thay đổi tương lai lỡ tay.

KHÔNG cần sklearn/artifact. Kiểm: 3 module thuần import được · RULES phản ánh
Rule #1/2/3 · openapi.yaml parse được · các tài liệu contract còn đủ.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "model"))


# ── 3 module thuần import được (không kéo theo ML lib) ───────────────────────
def test_pure_modules_import():
    import contracts, errors, manifest  # noqa: F401
    assert contracts.CONTRACT_VERSION
    assert issubclass(errors.ConfigurationError, errors.EarlyWarningError)
    assert manifest.FEATURE_SPEC_VERSION


# ── RULES.md vẫn phản ánh ba luật ────────────────────────────────────────────
def test_rules_md_states_three_rules():
    txt = (ROOT / "RULES.md").read_text()
    assert "Rule #1" in txt and "Source of Truth" in txt
    assert "Rule #2" in txt          # hợp đồng đứng yên, hiện thực thay được
    assert "Rule #3" in txt          # export là bước cuối


# ── openapi.yaml parse được và khớp CONTRACT_VERSION ─────────────────────────
def test_openapi_parses_and_versions_match():
    try:
        import yaml
    except ImportError:
        import pytest
        pytest.skip("PyYAML không có — bỏ qua kiểm cú pháp YAML")
    spec = yaml.safe_load((ROOT / "api" / "openapi.yaml").read_text())
    assert spec["paths"], "openapi thiếu paths"
    assert "PredictionResult" in spec["components"]["schemas"]
    import contracts
    assert spec["info"]["version"] == contracts.CONTRACT_VERSION


# ── các tài liệu contract cốt lõi còn tồn tại ────────────────────────────────
def test_core_documents_present():
    must_exist = [
        "RULES.md", "ARCHITECTURE.md", "DESIGN.md",
        "contracts.py", "errors.py",
        "api/openapi.yaml",
        "docs/ERROR_MODEL.md", "docs/INTEGRATION_TEST_SPEC.md", "docs/ADAPTER_CONTRACT.md",
        "docs/adr/0001-source-of-truth.md", "docs/adr/0005-profile-has-no-path.md",
        "model/manifest.py",
    ]
    missing = [p for p in must_exist if not (ROOT / p).exists()]
    assert not missing, f"tài liệu contract bị thiếu: {missing}"


# ── 5 ADR đều có đủ ba mục Bối cảnh / Quyết định / Hệ quả ─────────────────────
def test_all_adrs_have_required_sections():
    adr_dir = ROOT / "docs" / "adr"
    adrs = sorted(adr_dir.glob("000*.md"))
    assert len(adrs) == 5, f"kỳ vọng 5 ADR, thấy {len(adrs)}"
    for a in adrs:
        t = a.read_text()
        for section in ("Bối cảnh", "Quyết định", "Hệ quả"):
            assert section in t, f"{a.name} thiếu mục '{section}'"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn(); print(f"  ✓ {fn.__name__}")
    print(f"\n✅ {len(fns)} smoke test qua")
