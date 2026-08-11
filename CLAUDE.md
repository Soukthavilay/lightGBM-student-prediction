# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A master's **đề án thạc sĩ** (Vietnamese) titled *"Ứng dụng LightGBM xây dựng mô hình dự báo và phát hiện nguyên nhân bỏ học của sinh viên"*.

Two halves, both named in the title:
- **dự báo** — build and evaluate a LightGBM model that predicts student dropout.
- **phát hiện nguyên nhân** — use SHAP to surface the *yếu tố nguy cơ* (risk factors) behind the prediction.

> ⚠️ **This repo was re-scoped on 2026-08-10.** An earlier version framed the thesis around an anti-leakage / horizon-aware ("landmarking") research contribution on local data. The advisor rejected that framing. All code, results, and chapter drafts from that direction were deleted on 2026-08-11. Do not reintroduce `horizon_dataset`, `landmarking`, `mốc dự báo`-as-contribution, or the two-tier early-warning prototype unless the user explicitly asks.

## Current direction

- **Structure** follows a standard Vietnamese đề án skeleton, taken from two advisor-supplied templates in the repo root:
  - `Đề-Án-NguyenThiPhucLoan-26B-phiên bản 18092025.docx` — closest parallel (stroke prediction with Ensemble XGBoost/LightGBM/CatBoost + SHAP)
  - `Melasma_Thesis_Ngan__Copy_.pdf`
  - Shared skeleton: **Phần mở đầu** (8 numbered items) → **Chương 1 Cơ sở lý thuyết** → **Chương 2 Dữ liệu và phát biểu bài toán** → **Chương 3 Thiết kế mô hình và thực nghiệm** → **Kết luận và kiến nghị**.
- **Model focus:** LightGBM is the thesis model; XGBoost and CatBoost are comparison models; logistic regression and random forest are reference baselines.
- **Data:** the Kaggle/UCI benchmark set is the main training data. `Testkhoa.csv` (local Vietnamese registry data) is reserved for a later test/validation step — **the method for combining the two is still unconfirmed with the advisor.** The two sets have completely different feature schemas, so a single train-on-Kaggle/test-on-Testkhoa transfer is not possible; the likely intent is two separate experiments sharing one pipeline.

## Data

- **`data/student's dropout dataset.csv`** — the Kaggle/UCI set "Predict Students' Dropout and Academic Success" (Realinho et al.). **Separator is `;`**, not comma. 4.424 students, 36 features, 3-class target `{Dropout, Graduate, Enrolled}`. One column name carries a stray tab (`Daytime/evening attendance\t`) — strip column names on load. `Nacionality` is misspelled in the source and is renamed to `Nationality`.
- **`Testkhoa.csv`** — local Vietnamese registry data, 7.523 rows. **Encoding is `latin-1`**, not UTF-8 — reading as UTF-8 corrupts Vietnamese text. Not currently used by the notebook.

Target is binarised as `Dropout = 1, else = 0`. The notebook also reports a sensitivity variant that drops the `Enrolled` group entirely (§2.10).

## Running the work

Everything lives in **`Student_Perfor.ipynb`** — there is no separate pipeline script. Open the **`Thesis/` folder** in VS Code (not a parent folder — the notebook reads `data/…` by relative path), then **Restart Kernel → Run All**. Verified end to end: 44/44 code cells, 0 errors, ~6 minutes.

### Kernel — this machine has three Pythons and only one works

| interpreter | state |
|---|---|
| `/usr/bin/python3` (3.9.6, = the Xcode-bundled binary) | **has every package** — the one to use |
| `/opt/homebrew/bin/python3` (3.14) | empty; plain `python3` kernelspec resolves here and fails at `import plotly` |
| `Master_Class/student/.venv` (3.14) | has plotly/lightgbm but **not** xgboost, catboost, shap |

A kernel named **`thesis-lightgbm`** ("Python (Thesis LightGBM)") is registered against the working interpreter, and the notebook's `kernelspec` points at it — VS Code should select it automatically. If the packages ever go missing, re-register with:

```bash
/usr/bin/python3 -m ipykernel install --user --name thesis-lightgbm --display-name "Python (Thesis LightGBM)"
```

```bash
/usr/bin/python3 -m pip install lightgbm xgboost catboost shap scikit-learn pandas numpy matplotlib plotly kaleido
```

Note there is no `pip` on PATH — always use `python3 -m pip`. `nbconvert --execute` is broken in this environment (`RuntimeError: no running event loop` from jupyter_core on 3.9); to verify the notebook headlessly, drive `nbclient.NotebookClient` from inside `asyncio.run()` and set `resources={"metadata": {"path": <notebook dir>}}` so relative data paths resolve.

Notebook layout:
- **cells 0–40 — EDA** (kept from the student's original Colab work): distributions, gender/course/marital/financial breakdowns, correlation heatmap. Feeds Chương 2.
- **cells 41+ — "PHẦN 2"**: the modelling pipeline. Feeds Chương 3.

The hyperparameter-tuning cell (§2.6) runs 20 configurations × 5 folds × 3 models and takes a few minutes. Results are written to `08_KetQua_Kaggle/` by the last code cell.

`RANDOM_STATE = 42` everywhere; reproducibility matters for the thesis. There is no test suite or linter — verification is running the notebook and inspecting the printed metrics.

## Four methodological fixes (do not silently revert these)

The notebook's PHẦN 2 deliberately departs from the student's original Colab modelling section. Each was verified numerically before being adopted:

1. **AUC/AP are computed from `predict_proba()`, never `predict()`.** Feeding hard 0/1 labels to `roc_curve` yields a single-operating-point curve and understates AUC (0,86 vs 0,93 on this data). The original notebook reported 0,78 this way.
2. **The `Curricular units` feature group is kept**, not dropped for high correlation. Tree models make no independence assumption, and this is the strongest predictive block (AUC 0,891 → 0,908 when retained).
3. **No `StandardScaler` for tree models**, which are invariant to monotone transforms. For the baselines, scaling lives *inside* a `Pipeline` so it only ever fits on the training fold. The original scaled the full dataset before splitting, leaking test-set information.
4. **Nominal codes are declared `category`** (`Course` = 1..17 etc.) so the boosting models handle them natively instead of treating them as continuous.

Also: model selection uses **`roc_auc`**, not accuracy — the data is imbalanced (32,1% dropout, so a constant predictor already scores 67,9%). All three boosters get the **same tuning budget** so the comparison stays fair.

## Key conventions

- **Comments, prints, markdown, and figure labels are in Vietnamese.** Match that when editing. Thai is used only for chat with the user.
- **CatBoost quirk:** `cat_features` must be passed to `fit()`, *not* to the constructor. CatBoost mutates that parameter internally, which breaks `sklearn.base.clone()` — and `clone()` is required by every scikit-learn hyperparameter search. The notebook's `fit_model()` helper encapsulates this.
- **Honest framing of the model comparison.** The three boosters land within ~0,001 AUC of each other on internal CV; XGBoost sometimes edges ahead on the test split. The thesis does **not** claim LightGBM is the most accurate. It is chosen for: best F1/accuracy at the operating threshold, native categorical and missing-value handling, training speed, and `TreeExplainer` compatibility for the SHAP half of the title.
- **SHAP wording.** SHAP describes *model behaviour*, so findings are stated as *yếu tố nguy cơ có liên hệ*, never as proven causes — even though the title says "nguyên nhân".
- **Do not invent numbers or citations.** Mark gaps as `TODO` / `[cần bổ sung]` instead.

## Repository layout

- `Student_Perfor.ipynb` — the single source of truth for all analysis
- `data/` — Kaggle dataset · `Testkhoa.csv` (root) — local data, reserved
- `02_TaiLieu_ThamKhao/` — reference PDFs and `anchor_refs.bib`. **The .bib still holds the old direction's anchors** (Kaufman leakage, van Houwelingen landmarking, TRIPOD…). Still missing for the new direction: XGBoost (Chen & Guestrin 2016), CatBoost (Prokhorenkova 2018), and the dataset paper (Realinho et al. 2022).
- `03_KetQua_Hinh/kaggle/` — figures exported from the notebook
- `08_KetQua_Kaggle/` — result tables (`model_comparison_all.csv`, `target_comparison.csv`, `best_params_all.csv`, `shap_importance_{lightgbm,xgboost,catboost}.csv`)
- `07_BanThao_LuanVan/` — thesis drafts for the **new** direction only:
  - `_DanBai_Moi_DeAn_2026-08-10.md` — the outline mapping every section to its source
  - `Moi_PhanMoDau_draft.md` — PHẦN MỞ ĐẦU, drafted
  - `RaSoat_TiengViet_LuanVan.docx` — a reviewer's Vietnamese-language critique of the old draft. The *language* lessons still apply: prefer short sentences, avoid em-dash-enclosed clauses, keep one term per concept, and distinguish `độ chính xác tổng thể` (accuracy) from `độ chính xác dương tính` (precision).
There is deliberately no `README.md` or task checklist — both were written for the old direction and were deleted rather than rewritten. This file is the only project-level documentation.

## Status

Chương 1, 2, 3 and Kết luận are **not yet written**. PHẦN MỞ ĐẦU exists in draft and needs real citations added to item 2 (Tổng quan tình hình nghiên cứu) — the templates cite ~8 specific studies with author, year and reported accuracy, and the current draft has none.
