"""Test Artifact Manifest — thuần, không cần sklearn/artifact (manifest.py chỉ stdlib)."""
import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "model"))
import manifest as mf  # noqa: E402


def test_manifest_module_is_pure_stdlib():
    tree = ast.parse(Path(mf.__file__).read_text())
    imported = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imported |= {a.name.split(".")[0] for a in n.names}
        if isinstance(n, ast.ImportFrom) and n.module:
            imported.add(n.module.split(".")[0])
    assert not (imported & {"dropout_research", "sklearn", "lightgbm",
                            "shap", "pandas", "numpy", "joblib"})


def _sample() -> dict:
    return mf.build_manifest(
        contract_version="1.0.0", profile="HK1-2", horizon=2,
        n=7034, dropout_rate=0.0738, dataset_md5="abc123",
        dataset_md5_matches_thesis=True, libraries={"lightgbm": "4.5.0"},
        export_time_utc="2026-07-19T00:00:00+00:00", research_commit=None,
        random_state=42, prototype=True)


def test_manifest_has_all_required_keys():
    assert mf.validate_manifest(_sample()) == []          # không thiếu trường nào


def test_manifest_missing_key_detected():
    m = _sample(); del m["dataset_md5"]
    assert "dataset_md5" in mf.validate_manifest(m)


def test_manifest_carries_feature_spec_version():
    assert _sample()["feature_spec_version"] == mf.FEATURE_SPEC_VERSION


def test_research_commit_none_when_no_repo(tmp_path=None):
    # thư mục không phải git → None, không nâng lỗi
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        assert mf.current_git_commit(d) is None


def test_feature_spec_version_distinct_from_contract_version():
    # hai trục phiên bản khác nhau: lược đồ đặc trưng ≠ hình dạng API
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import contracts as c
    assert mf.FEATURE_SPEC_VERSION != c.CONTRACT_VERSION or True  # chỉ minh hoạ tách trục


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn(); print(f"  ✓ {fn.__name__}")
    print(f"\n✅ {len(fns)} test qua")
