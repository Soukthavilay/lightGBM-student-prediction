# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A master's thesis project (Vietnamese) on **early prediction of university student dropout** using LightGBM. The intellectual core is **cohort- and horizon-aware modeling to prevent label leakage**: the goal is an *early-warning* model that, *at the end of semester h*, predicts which **still-enrolled** students will drop out *after* that point — using only data available up to semester h, not end-of-program data that trivially predicts dropout.

The work is split across three files that form one pipeline:

1. **`dropout_research.py`** — the research module (v2, leakage-fixed). All modeling logic lives here: data loading, cohort/horizon labeling, feature building, models, cross-validation, CIs, DeLong test, nested CV, calibration, decision curve. Imported by `run_pipeline.py`; not run directly.
2. **`run_pipeline.py`** — the compute driver. Runs the whole analysis on the new cohort/horizon definition and **writes every result table and checkpoint** into `05_KetQua_ThongKe/` and `06_TrungGian_Checkpoint/`.
3. **`student_dropout_lightgbm.ipynb`** — the thesis narrative (a 14-step story). It **only reads** the pre-computed tables/checkpoints and renders figures + prose. This is the source of record for the thesis write-up, but it does **not** recompute the heavy results — `run_pipeline.py` does.

## Data

- **`Testkhoa.csv`** — the real Vietnam dataset. **Encoding is `latin-1`**, not UTF-8 — reading as UTF-8 corrupts Vietnamese text. `dropout_research.py` depends on this, and its label maps deliberately contain mojibake keys (e.g. `"Y?u"`, `"Xu?t s?c"`) to match the raw bytes.
- The raw file has **7,523 rows**. After filtering to the two cohorts with full 4-semester data (`COHORT_YEARS = (2020, 2021)`; 9 students from 2022–2023 are dropped on load), the working set is **7,514 students, dropout rate ≈ 13.1%**. Note the horizon-restricted analysis sets are smaller still: **HK1 n=7,367 (11.5% dropout)** and **HK1-2 n=7,034 (7.4%)** — do not mix these three figures.
- Columns: `StudentID`, demographics (`Gender`, `Nation`, `Religion`, `Region`, `Aspiration`, `IndustryCode`), entrance scores (`EntranceScore_1..3`, `SumScore`), and per-semester blocks for 4 terms (`GPA4_i`, `Rating_i`, `CreditsRegistered_i`, `CreditsEarnned_i` [sic — double-n], `TermStatus_i`). Target is `Drop`.

## Running the pipeline

```bash
pip install lightgbm scikit-learn pandas numpy shap optuna joblib

python3 run_pipeline.py --fast   # ~5-10 min: smoke-test that the pipeline runs end-to-end
python3 run_pipeline.py          # full thesis run (~1-2 hours); overwrites files in the two output dirs
```

Then open `student_dropout_lightgbm.ipynb` → **Restart Kernel → Run All** to re-render the narrative and figures against the freshly generated tables.

There is **no test suite, linter, or build step** — this is research code. Verification is running `run_pipeline.py --fast` and inspecting the printed metrics, then re-running the notebook. `RANDOM_STATE = 42` everywhere; reproducibility matters for the thesis.

## Architecture of `dropout_research.py`

The leakage fix (v2) is the whole point. Key stages:

1. **Cohort + horizon labeling** — `semester_active(df, k)` marks students still active at semester k (proxy: `CreditsRegistered_k > 0`). `horizon_dataset(df, horizon)` keeps **only students active at semester `horizon`**, and the label becomes "drops out *after* the end of HK `horizon`". This is what prevents the leak: students who already left before HK h are excluded, so their HK-h features (GPA=0, 0 credits) can't act as a label proxy.
2. **`build_features_raw(df, horizon)`** — builds features from **terms 1..horizon only**, plus cumulative aggregates (GPA mean/min/trend/std, cumulative credit rate, cumulative warnings). Semesters that are not active → `NaN` (not 0), to separate "no data" from "failed everything"; LightGBM handles `NaN` natively, baselines impute in-fold.
3. **Models & evaluation** — `make_models()` builds LightGBM (`make_lgbm`, class imbalance via `is_unbalance=True`, computed in-fold) plus sklearn baselines. `repeated_oof` / `evaluate_with_ci` produce repeated stratified OOF predictions with bootstrap CIs (`bootstrap_ci_metrics`). `delong_test` / `paired_model_test` do significance testing. `nested_cv_lgbm` (Optuna inner loop) checks for tuning-induced optimism. `oof_calibrated`, `decision_curve`, `expected_calibration_error` cover calibration and clinical/policy utility.

`run_pipeline.py` runs scopes `{"HK1": 1, "HK1-2": 2}` (the "full" 4-term scope is reference-only and deliberately leaks) and writes: `metrics_with_ci.csv`, `model_significance.csv`, `nested_cv_results.csv` + `nested_best_params.pkl`, `calibration.pkl`, `decision_curve.csv`, `temporal_ci.csv`, `fairness_ci.csv`, `shap_stability.csv`.

## Key conventions

- **Horizon-aware + cohort-strict = anti-leakage.** Two independent guards: (a) restrict the cohort to students active at horizon h (`horizon_dataset`), and (b) build features only from terms `1..h` (`build_features_raw`). Any feature touching term `i > horizon`, or any student not active at h, is a leak. The file header of `dropout_research.py` documents the fixes as `### [SỬA n]` markers.
- **Two assumptions to verify with the registrar** (document in the thesis limitations): (a) "active at HK k" ≈ `CreditsRegistered_k > 0` — replace with an official withdrawal date if available; (b) `TermStatus_k` is treated as a known academic-warning feature — if it actually encodes "already withdrawn", set `DROP_TERMSTATUS = True` in `dropout_research.py`, because then it is a disguised label.
- **The notebook does not compute — it reads.** Change modeling logic in `dropout_research.py`, regenerate with `run_pipeline.py`, then re-run the notebook. Editing numbers in the notebook directly will desync it from the tables.
- Comments, prints, and docs are in Vietnamese — match that when editing these files.

## Repository layout

- `02_TaiLieu_ThamKhao/` — reference papers (PDF)
- `03_KetQua_Hinh/` — exported figures (`fig_*.png`) rendered by the notebook; `nang_cap_thong_ke/` holds the statistical-upgrade figures
- `05_KetQua_ThongKe/` — result tables with confidence intervals (`*.csv`), written by `run_pipeline.py`
- `06_TrungGian_Checkpoint/` — intermediate pickles (`calibration.pkl`, `nested_best_params.pkl`), written by `run_pipeline.py`
- `_LuuTru_backup_*.ipynb` (repo root) — notebook backups from earlier stages
- `README.md` — Vietnamese directory map (note: it still references a planned `khung_da_quoc_gia/` framework and an `01_DeAn_BaoCao/` report that do not exist in the repo yet)
