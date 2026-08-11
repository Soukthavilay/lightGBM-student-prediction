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

The notebook reads the CSV with **PySpark** (`SparkSession`, `sep=";"`), does the EDA on Spark DataFrames converted to pandas for plotting, then `.collect()`s into numpy for the sklearn-family models. Spark adds no speed at 4.424 rows — it is a presentation choice, and the advisor may ask about it.

Notebook layout (141 cells, 77 code):
- **imports → data dictionary → cleaning → EDA** — target/age/gender/course/marital/financial breakdowns, correlation. Feeds Chương 2.
- **feature selection → split → scaling → 6 models → comparison → cross-validation → SHAP → sensitivity → save**. Feeds Chương 3.

Hyper-parameter tuning is 48 configurations × 3 boosters, then 5-fold CV × 4 models. A full run is ~6 minutes. **The last code cell writes every table to `08_KetQua_Kaggle/` and calls `spark.stop()`**; figures are written to `03_KetQua_Hinh/kaggle/` as they are produced.

`random_state=42` / `seed=42` everywhere; reproducibility matters for the thesis. There is no test suite or linter — verification is running the notebook and inspecting the printed metrics.

## Methodological decisions (do not silently revert these)

Each was verified numerically before being adopted. Several were re-established on 2026-08-11 after a full audit of the imported Spark notebook.

1. **AUC/AP are computed from `predict_proba()`, never `predict()`.** Feeding hard 0/1 labels to `roc_curve` collapses the curve to a single operating point and understates AUC.
   For the Spark baselines use the **`probability`** column, not `rawPrediction` — for a decision tree `rawPrediction` holds raw leaf *counts*, which is not a monotone function of the probability.
2. **The `Curricular units` feature group is kept**, not compressed with PCA. Tree models make no independence assumption, and a PCA component cannot be named as a cause. PCA is run only to *report* that one component explains 61,3% of that block.
3. **Split first, scale second.** The scaler is fitted on the training split only. Fitting on the full dataset before splitting leaks test-set statistics.
4. **Tree models train on the RAW `features` column, not `scaled_features`.** They are invariant to monotone transforms, and SHAP must display original units ("age 34", "0 units passed") — with scaled inputs the waterfall reads "Age at enrollment = 4.51", which no advisor can act on. `X_test_disp` holds the unscaled frame used for every SHAP plot.
5. **Nominal codes are declared `category`** — 8 columns (`Course` = 33…9991, `Application mode`, `Father's occupation`, …). LightGBM detects the dtype, XGBoost needs `enable_categorical=True` + `tree_method='hist'`, CatBoost needs `cat_features` at `fit()`.
6. **Categorical redundancy is judged with Cramér's V, not Pearson.** Pearson on nominal codes measures only how the codes happen to be numbered. `Nationality`×`International` = 0,998 (an exact functional dependency — `Nationality` is dropped), but `Mother's occupation`×`Father's occupation` = 0,571 while Pearson claims 0,910. **The parents' variables are kept** — dropping them is unsupported and contradicts the advisor's variable groups.
7. **Only 4 columns are dropped:** `Nationality` (duplicate of `International`) and `Unemployment rate` / `Inflation rate` / `GDP` (|corr with dropout| ≤ 0,05; national context, not a student attribute). → **32 features**.
8. **EDA and the model use the same population** — all 4.424 students, three outcomes. An earlier version explored `Graduate`+`Dropout` only (39,1% dropout) while training on all rows (32,1%), so every percentage in Chương 2 disagreed with Chương 3.
9. **`Enrolled` is kept, labelled 0**, with the snapshot limitation stated, and a **sensitivity analysis** at the end refits without them (AUC 0,9004 → 0,9397; 8/10 risk factors identical).
10. **Model selection uses AUC, not accuracy** — a constant predictor already scores 67,9%. All three boosters get the **same 48-configuration budget**.
11. **Feature importances are compared by RANK.** The six models report on six incompatible scales (split count / gain / PredictionValuesChange / impurity share / |coefficient|). The rank table is the comparable artefact; SHAP is the trustworthy one.

## Key conventions

- **The notebook is entirely in English** — comments, prints, markdown and figure labels — because the advisor asked for it (*"các dữ liệu em chuyển sử dụng ngôn ngữ tiếng Anh nhé"*). The **thesis document** stays Vietnamese. Thai is used only for chat with the user.
- **`from pyspark.sql.functions import *` shadows the built-ins** `max`, `min`, `sum`, `round`. Use `builtins.` explicitly for plain Python numbers — this has already caused one crash.
- **CatBoost quirk:** `cat_features` must be passed to `fit()`, *not* to the constructor. CatBoost mutates that parameter internally, which breaks `sklearn.base.clone()` — and `clone()` is required by every scikit-learn hyperparameter search. `tune_by_auc(..., fit_kwargs={'cat_features': ...})` encapsulates this.
- **Plotly figures are NOT stored in the .ipynb.** They vanish on export to PDF/Word. Every Plotly cell goes through the `save_fig(fig, name)` helper, which writes a PNG *and* displays; matplotlib cells call `plt.savefig(FIG_DIR / ...)` before `plt.show()`.
- **Honest framing of the model comparison.** On 5-fold CV (3.581 students) the four leading models span 0,0075 AUC while the fold-to-fold standard deviation is 0,014–0,021 — **they are statistically indistinguishable**, and logistic regression is among them. The thesis must **not** claim LightGBM is the most accurate.
  The real argument for the ensembles is **recall at the operating threshold**: CatBoost 0,779 · LightGBM 0,750 · XGBoost 0,717 versus logistic regression 0,636 and LinearSVC 0,592. For an early-warning system, logistic regression misses 36% of the students who drop out where CatBoost misses 22% — and accuracy/AUC hide that completely. LightGBM is chosen for native categorical and missing-value handling, training speed, and `TreeExplainer` compatibility for the SHAP half of the title.
- **SHAP wording.** SHAP describes *model behaviour*, so findings are stated as *yếu tố nguy cơ có liên hệ*, never as proven causes — even though the title says "nguyên nhân".
- **Do not invent numbers or citations.** Mark gaps as `TODO` / `[cần bổ sung]` instead.

## Repository layout

- `Student_Perfor.ipynb` — the single source of truth for all analysis
- `data/` — Kaggle dataset · `Testkhoa.csv` (root) — local data, reserved
- `02_TaiLieu_ThamKhao/` — reference PDFs and `anchor_refs.bib`. **The .bib still holds the old direction's anchors** (Kaufman leakage, van Houwelingen landmarking, TRIPOD…). Still missing for the new direction: XGBoost (Chen & Guestrin 2016), CatBoost (Prokhorenkova 2018), and the dataset paper (Realinho et al. 2022).
- `03_KetQua_Hinh/kaggle/` — 27 figures written by the notebook, numbered `01_`–`22_` in the order they appear. **Everything here is regenerated on every run**; nothing is hand-made.
- `08_KetQua_Kaggle/` — 9 result tables, also regenerated on every run: `model_comparison_all.csv` · `cv_results.csv` · `best_params_all.csv` · `threshold_sweep.csv` · `sensitivity_enrolled.csv` · `feature_importance_ranks.csv` · `shap_importance_{lightgbm,xgboost,catboost}.csv`.
  ⚠️ Any file in these two folders that the notebook does **not** write is stale output from a deleted notebook — check before citing a number from one.
- `07_BanThao_LuanVan/` — thesis drafts for the **new** direction only:
  - `_DanBai_Moi_DeAn_2026-08-10.md` — the outline mapping every section to its source
  - `Moi_PhanMoDau_draft.md` — PHẦN MỞ ĐẦU, drafted
  - `RaSoat_TiengViet_LuanVan.docx` — a reviewer's Vietnamese-language critique of the old draft. The *language* lessons still apply: prefer short sentences, avoid em-dash-enclosed clauses, keep one term per concept, and distinguish `độ chính xác tổng thể` (accuracy) from `độ chính xác dương tính` (precision).
There is deliberately no `README.md` or task checklist — both were written for the old direction and were deleted rather than rewritten. This file is the only project-level documentation.

## Status

Chương 1, 2, 3 and Kết luận are **not yet written**. PHẦN MỞ ĐẦU exists in draft and needs real citations added to item 2 (Tổng quan tình hình nghiên cứu) — the templates cite ~8 specific studies with author, year and reported accuracy, and the current draft has none.
