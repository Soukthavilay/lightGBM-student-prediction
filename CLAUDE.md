# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A master's thesis project (Vietnamese) on **early prediction of university student dropout** using LightGBM. The intellectual core is **horizon-aware feature engineering to prevent label leakage**: the goal is an *early-warning* model that uses only data available up to a given semester (HK = học kỳ), not end-of-program data that trivially predicts dropout.

Two parallel implementations of the same modeling idea live here:
1. **`student_dropout_lightgbm.ipynb`** — the thesis research notebook (EDA → feature engineering → Optuna tuning → SHAP → fairness/temporal validation). This is the source of record for thesis figures and results.
2. **`khung_da_quoc_gia/`** — a productionized, **config-driven framework** that generalizes the notebook so the same code runs for any country/school by editing a JSON column mapping (Vietnam validated; Laos is a template). Code never changes between countries — only the config does.

Most reusable conventions and notes (Vietnamese) live in `khung_da_quoc_gia/README.md`.

## Data

- **`Testkhoa.csv`** — the real Vietnam dataset (~7,500 students). **Encoding is `latin-1`**, not UTF-8 — reading as UTF-8 will corrupt Vietnamese text (this is why `config_vietnam.json` sets `"encoding": "latin-1"` and `rating_order` contains mojibake like `"Y?u"`). The notebook and framework both depend on this.
- Columns: `StudentID`, demographics (`Gender`, `Nation`, `Region`, `Aspiration`, `IndustryCode`), entrance scores (`EntranceScore_1..3`, `SumScore`), and per-semester blocks for 4 terms (`GPA4_i`, `Rating_i`, `CreditsRegistered_i`, `CreditsEarnned_i` [sic — double-n], `TermStatus_i`). Target is `Drop`.
- `dataset.csv` and `khung_da_quoc_gia/example_laos_synthetic.csv` are **synthetic/illustration only** — never use their results in the thesis.

## Running the framework

From inside `khung_da_quoc_gia/` (the scripts `import dropout_framework` and configs use relative paths like `../Testkhoa.csv`):

```bash
pip install lightgbm scikit-learn pandas numpy joblib

python run.py config_vietnam.json            # train + evaluate + save model/features/summary
python3 dashboard_manager.py config_vietnam.json --open   # build & open manager HTML dashboard
```

Outputs: `model_<country>.pkl`, `features_<country>.csv`, `summary_<country>.json`, `dashboard_<country>.html`.

There is **no test suite, linter, or build step** — this is research code. Verification is done by running `run.py` and inspecting printed metrics, and by re-running notebook cells.

## Architecture of `dropout_framework.py`

A canonical-schema pipeline in three stages, all keyed off the config's `columns` mapping (source column name → canonical name):

1. **`load_canonical(config)`** — reads the source CSV and maps it to a fixed canonical schema (`student_id`, `target`, static fields, and per-term `gpa_i`/`credits_*_i`/`academic_status_i`/`rating_num_i`). Normalizes GPA to a 4.0 scale and entrance scores to a 10 scale regardless of source scale. Derives the binary `target` from `target_positive_values`. Optional fields (ethnicity, admission_preference, rating, entrance_total) are silently skipped if the config maps them to `null`.
2. **`build_features(canon, cfg, horizon)`** — the leakage-prevention core. Builds features using **only terms 1..horizon**, plus cumulative aggregates (gpa_mean/min/trend/std, cumulative credit rate, cumulative warnings). The same function produces HK1 (horizon=1) and HK1-2 (horizon=2) feature sets.
3. **`train_eval(...)`** — `LightGBMClassifier` with `make_params()` defaults, an 80/10/10 stratified split (`split_data`), early stopping on validation AUC, class imbalance via `scale_pos_weight`, and F1-optimal threshold selection on the validation set. `threshold_for_precision` picks a precision-targeted operating point instead.

`run.py` orchestrates: compares horizon scopes (HK1 / HK1-2 / full), then builds the **two-stage warning workflow** — Stage 1 (HK1, precision target `t1_precision`) flags students early; Stage 2 (HK1-2, `t2_precision`) catches the rest. The "full" horizon is reference-only and deliberately leaks.

## Key conventions

- **Horizon-aware = anti-leakage.** Any feature touching term `i > horizon` is a leak. Keep `build_features` strictly bounded by `horizon`. The notebook's section 4.1 documents the leakage evidence.
- The framework and the notebook should stay conceptually in sync, but the **notebook (and `04_Model_KetQua/` artifacts) is authoritative for thesis numbers**; the framework is the generalized re-implementation. Deployed two-stage config and tuned models live in `04_Model_KetQua/` (`two_stage_config.json`, `*.pkl`, `warning_model_metadata.json`).
- `RANDOM_STATE = 42` everywhere; reproducibility matters for the thesis.
- Comments, prints, and docs are in Vietnamese — match that when editing these files.

## Repository layout (non-code)

- `01_DeAn_BaoCao/` — thesis proposal & report documents (.docx/.pdf/.md)
- `02_TaiLieu_ThamKhao/` — reference papers (PDF)
- `03_KetQua_Hinh/` — exported figures (`fig_NN_*.png`) generated by the notebook
- `04_Model_KetQua/` — saved deployment models, thresholds, feature lists, metadata
- `_LuuTru/` — archive/backups (includes a notebook backup)
