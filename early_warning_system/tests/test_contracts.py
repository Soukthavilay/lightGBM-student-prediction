"""Unit tests cho hợp đồng Production — chạy được KHÔNG cần sklearn/artifact.

    python3 -m pytest early_warning_system/tests/ -q      # nếu có pytest
    python3 early_warning_system/tests/test_contracts.py   # chạy trực tiếp cũng được
"""
import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import contracts as c  # noqa: E402
import errors as e  # noqa: E402

_FORBIDDEN = {"dropout_research", "sklearn", "lightgbm",
              "shap", "pandas", "numpy", "joblib", "fastapi"}


def _imports_of(module) -> set[str]:
    tree = ast.parse(Path(module.__file__).read_text())
    imported = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imported |= {a.name.split(".")[0] for a in n.names}
        if isinstance(n, ast.ImportFrom) and n.module:
            imported.add(n.module.split(".")[0])
    return imported


# ── Rule #2 tự bảo vệ: contract & errors PHẢI trong sạch (chỉ stdlib) ─────────
def test_contracts_import_only_stdlib():
    assert not (_imports_of(c) & _FORBIDDEN)


def test_errors_import_only_stdlib():
    assert not (_imports_of(e) & _FORBIDDEN)


# ── Phiên bản hợp đồng ───────────────────────────────────────────────────────
def test_contract_version_present():
    assert c.CONTRACT_VERSION == "1.0.0"


def test_compatibility_same_major():
    assert c.is_compatible("1.0.0")
    assert c.is_compatible("1.9.3")        # cùng MAJOR = tương thích
    assert not c.is_compatible("2.0.0")    # khác MAJOR = không
    assert not c.is_compatible("0.9.0")


def test_compatibility_bad_input_is_false_not_crash():
    assert c.is_compatible("không-phải-số") is False
    assert c.is_compatible("") is False


# ── ThresholdTierPolicy: biên là chỗ dễ sai nhất ─────────────────────────────
def test_tier_boundaries_default():
    p = c.ThresholdTierPolicy()
    assert p.assign(0.099) == c.TIER_NONE
    assert p.assign(0.10) == c.TIER_SCREEN     # đúng ngưỡng tier1 → đã vào tầng 1
    assert p.assign(0.399) == c.TIER_SCREEN
    assert p.assign(0.40) == c.TIER_DEEP       # đúng ngưỡng tier2 → đã vào tầng 2
    assert p.assign(0.999) == c.TIER_DEEP


def test_tier_extremes():
    p = c.ThresholdTierPolicy()
    assert p.assign(0.0) == c.TIER_NONE
    assert p.assign(1.0) == c.TIER_DEEP


def test_tier_config_is_swappable_not_hardcoded():
    p = c.ThresholdTierPolicy(c.TierConfig(tier1=0.05, tier2=0.30))
    assert p.assign(0.06) == c.TIER_SCREEN     # 0.06 ≥ 0.05 nhưng < 0.30
    assert p.assign(0.30) == c.TIER_DEEP
    # cùng xác suất, chính sách mặc định lại cho tầng khác → chứng minh ngưỡng là config
    assert c.ThresholdTierPolicy().assign(0.06) == c.TIER_NONE


def test_tier_default_thresholds_match_thesis():
    cfg = c.TierConfig()
    assert (cfg.tier1, cfg.tier2) == (0.10, 0.40)


# ── FeatureContribution.direction ────────────────────────────────────────────
def test_direction_positive_and_negative():
    assert c.FeatureContribution("GPA4_2", 1.2, 0.83).direction == "tăng rủi ro"
    assert c.FeatureContribution("GPA4_2", 3.5, -0.4).direction == "giảm rủi ro"


def test_direction_zero_is_not_risk_increasing():
    # shap == 0 không đẩy rủi ro lên → quy ước "giảm rủi ro"
    assert c.FeatureContribution("x", None, 0.0).direction == "giảm rủi ro"


# ── PredictionResult ─────────────────────────────────────────────────────────
def test_tier_label_maps_from_tier():
    r = c.PredictionResult("SV1", 0.5, c.TIER_DEEP, [])
    assert r.tier_label == "Tầng 2 — can thiệp sâu"


def test_to_dict_shape_and_rounding():
    r = c.PredictionResult(
        "SV1", 0.123456, c.TIER_SCREEN,
        [c.FeatureContribution("GPA4_2", 1.2, 0.834567)])
    d = r.to_dict()
    assert d["student_id"] == "SV1"
    assert d["probability"] == 0.1235                 # làm tròn 4 chữ số
    assert d["tier"] == 1 and d["tier_label"].startswith("Tầng 1")
    assert d["top_features"][0] == {
        "feature": "GPA4_2", "value": 1.2,
        "shap": 0.8346, "direction": "tăng rủi ro"}


def test_missing_value_stays_none():
    r = c.PredictionResult("SV1", 0.2, c.TIER_SCREEN,
                           [c.FeatureContribution("GPA4_3", None, 0.1)])
    assert r.to_dict()["top_features"][0]["value"] is None


# ── PredictionProfile: chỉ là dữ liệu, KHÔNG chứa đường dẫn (ADR 0005) ────────
def test_profile_is_plain_data_without_path():
    prof = c.PredictionProfile(id="hk12", name="HK1-2", horizon=2)
    assert prof.horizon == 2
    # thêm profile mới không cần thay đổi gì trong contracts
    prof3 = c.PredictionProfile(id="hk3", name="HK3", horizon=3)
    assert prof3.horizon == 3


def test_profile_has_no_path_field():
    # đường dẫn là hạ tầng — KHÔNG được lọt vào domain
    assert not hasattr(c.PredictionProfile(id="x", name="X", horizon=1), "artifact_dir")


def test_standard_tier_policy_satisfies_protocol():
    assert isinstance(c.ThresholdTierPolicy(), c.TierPolicy)


# ── ConfigurationError: cấu hình sai KHÁC dữ liệu sai ─────────────────────────
def test_tier_config_rejects_inverted_thresholds():
    import pytest
    with pytest.raises(e.ConfigurationError):
        c.TierConfig(tier1=0.40, tier2=0.10)


def test_tier_config_rejects_out_of_range():
    import pytest
    with pytest.raises(e.ConfigurationError):
        c.TierConfig(tier1=-0.1, tier2=0.4)
    with pytest.raises(e.ConfigurationError):
        c.TierConfig(tier1=0.1, tier2=1.5)


def test_tier_config_default_is_valid():
    cfg = c.TierConfig()          # không nâng lỗi
    assert (cfg.tier1, cfg.tier2) == (0.10, 0.40)


def test_configuration_error_is_distinct_from_validation():
    assert not issubclass(e.ConfigurationError, e.ValidationError)
    assert issubclass(e.ConfigurationError, e.EarlyWarningError)


# ── chạy trực tiếp không cần pytest ──────────────────────────────────────────
if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in fns:
        fn()
        passed += 1
        print(f"  ✓ {fn.__name__}")
    print(f"\n✅ {passed}/{len(fns)} test qua")
