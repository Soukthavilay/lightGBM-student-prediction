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

Everything lives in **`Student_Perfor.ipynb`** — there is no separate pipeline script. Open the **`Thesis/` folder** in VS Code (not a parent folder — the notebook reads `data/…` by relative path), then **Restart Kernel → Run All**. Verified end to end: **72/72 code cells, 0 errors**, ~30 minutes (the 10-fold grid search dominates; set `CV_FOLDS = 5` in the CV-machinery cell to halve it).

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

**The notebook is pure pandas + scikit-learn.** PySpark was removed on 2026-08-12 — see *Why Spark was dropped* below. Do not reintroduce it.

Notebook layout (137 cells, 72 code):
- **imports → data dictionary → cleaning → EDA** — target/age/gender/course/marital/financial breakdowns, correlation. Feeds Chương 2.
- **feature selection → split → 10-fold CV (tuning + comparison) → holdout evaluation → SHAP → sensitivity → data augmentation → save**. Feeds Chương 3.

Hyper-parameter tuning is 48 configurations × 10 folds × 3 boosters (~1.440 fits), plus a 20-depth CV sweep for the decision tree, 20 split seeds, and 4 augmentation variants × 3 boosters on ~79k rows. A full run is ~30 minutes. The last code cell writes every table to `08_KetQua_Kaggle/`; figures are written to `03_KetQua_Hinh/kaggle/` as they are produced.

### Why Spark was dropped (2026-08-12)

Spark ML requires every feature to be squeezed into a single `Vector` column via `VectorAssembler`. That step **destroys the column names and casts everything to float64**, which is what forced most of the complexity the notebook used to carry: nominal codes had to be re-declared as `category` afterwards, SHAP needed a reconstructed display frame, and `from pyspark.sql.functions import *` shadowed the built-in `max`/`min`/`sum`/`round` in 50 places (it caused two real crashes). pandas hands the DataFrame to `fit()` directly, so names and dtypes survive end to end. At 4.424 rows — and at 79k in the augmentation section — Spark bought nothing but JVM start-up. The advisor's own sample code in the guidance docx is pandas + sklearn + lightgbm.

Consequences of the migration, all deliberate: `randomSplit` → **stratified** `train_test_split` (test 843 → 885 students); the Spark baselines → `LogisticRegression` / `DecisionTreeClassifier` / `LinearSVC` (note sklearn regularises by default where Spark did not); `rawPrediction`/`probability` → `predict_proba`, with `decision_function` for LinearSVC.

`random_state=42` / `seed=42` everywhere; reproducibility matters for the thesis. There is no test suite or linter — verification is running the notebook and inspecting the printed metrics.

## Methodological decisions (do not silently revert these)

Each was verified numerically before being adopted. Several were re-established on 2026-08-11 after a full audit of the imported Spark notebook.

1. **AUC/AP are computed from `predict_proba()`, never `predict()`.** Feeding hard 0/1 labels to `roc_curve` collapses the curve to a single operating point and understates AUC. `LinearSVC` has no `predict_proba`; its `decision_function` (the signed margin) is the correct ranking score.
2. **The `Curricular units` feature group is kept**, not compressed into a component. Tree models make no independence assumption, and a principal component cannot be named as a cause — SHAP has to point at something an advisor can act on. The correlation heat map is the evidence that the block is redundant; the PCA probe that used to report it was removed on 2026-08-12 as a dead end (nothing consumed its output).
3. **One stratified split, then 10-fold CV inside the training pool** (adopted 2026-08-12; there is no fixed validation set any more).
   `X_train` = 3.539 students carries **everything** — encoding, scaling, the depth sweep, the 48-configuration grid, cross-validation. `X_test` = 885 students is sealed and scored **once**, at the end, by models refitted on the whole pool.
   **Scaling lives inside a `Pipeline`**, never fitted before the folds: `Pipeline([('scaler', StandardScaler()), ('clf', …)])`. Cross-validation clones it per fold, so the scaler learns from 9 folds and only *transforms* the 10th. Fitting a scaler on the pool before `cross_val_score` would leak every validation fold's statistics into training.
   ⚠️ **Selection bias, disclosed in the notebook:** hyper-parameters are chosen by the same CV that reports their score, so the winning configuration's CV number is the maximum of 48 noisy estimates and is **slightly optimistic**. The holdout is the unbiased figure. A nested CV would remove the bias but costs 10× more.
4. **Tree models train on the RAW `features` column, not `scaled_features`.** They are invariant to monotone transforms, and SHAP must display original units ("age 34", "0 units passed") — with scaled inputs the waterfall reads "Age at enrollment = 4.51", which no advisor can act on. `X_test_disp` holds the unscaled frame used for every SHAP plot.
5. **Nominal codes are declared `category`** — 8 columns (`Course` = 33…9991, `Application mode`, `Father's occupation`, …). LightGBM detects the dtype, XGBoost needs `enable_categorical=True` + `tree_method='hist'`, CatBoost needs `cat_features` at `fit()`. Since the data never leaves pandas this is a one-line dtype change, not a reconstruction.
6. **Categorical redundancy is judged with Cramér's V, not Pearson.** Pearson on nominal codes measures only how the codes happen to be numbered. `Nationality`×`International` = 0,998 (an exact functional dependency — `Nationality` is dropped), but `Mother's occupation`×`Father's occupation` = 0,571 while Pearson claims 0,910. **The parents' variables are kept** — dropping them is unsupported and contradicts the advisor's variable groups.
7. **Only 4 columns are dropped:** `Nationality` (duplicate of `International`) and `Unemployment rate` / `Inflation rate` / `GDP` (|corr with dropout| ≤ 0,05; national context, not a student attribute). → **32 features**.
8. **EDA and the model use the same population** — all 4.424 students, three outcomes. An earlier version explored `Graduate`+`Dropout` only (39,1% dropout) while training on all rows (32,1%), so every percentage in Chương 2 disagreed with Chương 3.
9. **`Enrolled` is kept, labelled 0**, with the snapshot limitation stated, and a **sensitivity analysis** at the end refits without them (AUC 0,9004 → 0,9397; 8/10 risk factors identical).
10. **Model selection uses AUC, not accuracy** — a constant predictor already scores 67,9%. All three boosters get the **same 48-configuration budget**.
11. **Synthetic training data never enters the test set, and a leakage gate cleans the training pool before the experiment runs.** The Playground S4E6 file is generated *from the UCI dataset this study tests on*, and the hazard is real, not theoretical: **19 of the 843 test students appear verbatim in it**, and 35 land within 0,10 of a test student in standardised space. Exact matching alone is not sufficient (shifting one grade by 0,1 defeats it), so the gate uses nearest-neighbour distance, **removes the 40 offending synthetic rows** (0,05% of the file) and re-measures. Only a `PASS` makes the numbers reportable — a table marked `FAIL - do not report` must not reach Chương 3. Never re-run the augmentation section against the raw file without the gate.
12. **The augmentation result is "no new information", and that is the finding.** On the frozen 843-student test set: LightGBM 0,9004 → 0,9033 and CatBoost 0,9041 → 0,9074 (both inside noise); XGBoost 0,8934 → 0,9294, but **variant D — trained on synthetic data ALONE, never seeing a real student — scores 0,9304, i.e. as well as or better than real+synthetic for all three models.** The 2.918 real students therefore add nothing once 76k generated rows are present, so XGBoost's gain is variance reduction on an over-deep configuration (max_depth 10), not new knowledge. The generator also flattens the rare groups the study cares about (`Curricular units credited` mean 0,54 → 0,14; `Debtor` 0,11 → 0,07; `Educational special needs` 0,01 → 0,00).
13. **Feature importances are compared by RANK.** The six models report on six incompatible scales (split count / gain / PredictionValuesChange / impurity share / |coefficient|). The rank table is the comparable artefact; SHAP is the trustworthy one.

## Key conventions

- **The notebook is entirely in English** — comments, prints, markdown and figure labels — because the advisor asked for it (*"các dữ liệu em chuyển sử dụng ngôn ngữ tiếng Anh nhé"*). The **thesis document** stays Vietnamese. Thai is used only for chat with the user.
- **`from pyspark.sql.functions import *` shadows the built-ins** `max`, `min`, `sum`, `round`. Use `builtins.` explicitly for plain Python numbers — this has already caused one crash.
- **CatBoost quirk:** `cat_features` must be passed to `fit()`, *not* to the constructor. CatBoost mutates that parameter internally, which breaks `sklearn.base.clone()` — and `clone()` is required by every scikit-learn hyperparameter search. `tune_by_auc(..., fit_kwargs={'cat_features': ...})` encapsulates this.
- **Plotly figures are NOT stored in the .ipynb.** They vanish on export to PDF/Word. Every Plotly cell goes through the `save_fig(fig, name)` helper, which writes a PNG *and* displays; matplotlib cells call `plt.savefig(FIG_DIR / ...)` before `plt.show()`.
- **Honest framing of the model comparison — the single-split number is mostly luck.** Refitting the same LightGBM on 20 different stratified splits of the same 4.424 students moves the test AUC over a range of **0,038** (mean 0,918 · std 0,009) — **wider than the entire six-model table**. The holdout figure the notebook reports (0,9323) sits at the **100th percentile** of that distribution, i.e. above all 20 other draws, partly because the hyper-parameters were tuned on that split's own folds.
  ➡️ **Quote the 10-fold cross-validated figure — LightGBM 0,9186 ± 0,0122 — not the holdout 0,9323**, and never rank two models on one split.
- **All six models are weighted for the class imbalance in the same way** — `class_weight='balanced'` for logistic regression, the decision tree and LinearSVC; `is_unbalance` / `scale_pos_weight` / `auto_class_weights='Balanced'` for the boosters. Correcting this on 2026-08-12 **destroyed the recall argument that used to justify the ensembles**: on the holdout all six now land between 0,799 and 0,835 recall.
  **10-fold CV result:** LightGBM 0,9186 · XGBoost 0,9183 · CatBoost 0,9174 · LinearSVC 0,9145 · logistic regression 0,9140 · decision tree 0,8717 (fold std 0,012–0,017). **Five of the six sit inside one fold-to-fold standard deviation of the best** — statistically indistinguishable; LightGBM leads XGBoost by 0,0003 against a std of 0,0122. Only the **decision tree is genuinely behind** (>3 std), which is a claim the thesis *can* make.
  Note that the earlier 5-fold run put CatBoost first and this 10-fold run puts LightGBM first — the ranking flipping between protocols is itself evidence that it is noise.
  **So LightGBM is not chosen for accuracy or recall, and the thesis must not claim either.** The defensible reasons are: native handling of the 8 categorical variables (up to 46 levels) without one-hot expansion, native missing-value handling, training speed, and exact, fast SHAP through `TreeExplainer` — which is what the *phát hiện nguyên nhân* half of the title actually rests on.
- **The baselines are deliberately NOT one-hot encoded** — decided 2026-08-12, and it is an argument of the thesis rather than an oversight. They receive the eight nominal variables as standardised numbers (`Course` = 9500 read as a magnitude), the mis-specification the boosters are protected from by the `category` dtype. One-hot encoding was measured and rejected: it takes the feature count from **32 to 215 (6,7×)** and drops the sample from **88 rows per feature to 13**, on 2.831 training students — trading one mis-specification for overfitting on near-empty dummy columns.
  The notebook says this in the *"Limitation — how the baselines see the categorical variables"* section and gives the wording for **Chương 3 (Hạn chế)**: the baseline scores are a **lower bound**, which does not affect the conclusions because the study never claims LightGBM is more accurate. The point being made is that *handling categorical data is the classical models' weakness*, and that LightGBM removes the choice entirely while keeping the feature named `Course` intact — which is what lets SHAP say "this student's programme raised their risk" instead of "dummy variable 137 raised their risk".
- **SHAP wording.** SHAP describes *model behaviour*, so findings are stated as *yếu tố nguy cơ có liên hệ*, never as proven causes — even though the title says "nguyên nhân".
- **Do not invent numbers or citations.** Mark gaps as `TODO` / `[cần bổ sung]` instead.

## Repository layout

- `Student_Perfor.ipynb` — the single source of truth for all analysis
- `data/` — Kaggle dataset · `Testkhoa.csv` (root) — local data, reserved
  - **`data/playground_s4e6_train.csv`** — the 76.518-row synthetic training set from Kaggle *Playground Series S4E6*, downloaded by hand (there are no Kaggle credentials on this machine and the Kaggle connector is unauthenticated). Used for the *"tăng thêm dữ liệu cho huấn luyện"* experiment. The whole augmentation section skips cleanly if the file is removed, so Run All still passes without it.
- `02_TaiLieu_ThamKhao/` — reference PDFs and `anchor_refs.bib`. **The .bib still holds the old direction's anchors** (Kaufman leakage, van Houwelingen landmarking, TRIPOD…). Still missing for the new direction: XGBoost (Chen & Guestrin 2016), CatBoost (Prokhorenkova 2018), and the dataset paper (Realinho et al. 2022).
- `03_KetQua_Hinh/kaggle/` — 32 figures written by the notebook, numbered `01_`–`27_` in the order they appear. **Everything here is regenerated on every run**; nothing is hand-made.
- `08_KetQua_Kaggle/` — 14 result tables, also regenerated on every run: `model_comparison_all.csv` · `cv_results.csv` · `best_params_all.csv` · `threshold_sweep.csv` · `sensitivity_enrolled.csv` · `feature_importance_ranks.csv` · `split_variation.csv` · `shap_importance_{lightgbm,xgboost,catboost}.csv` · `augmentation_{leakage_gate,experiment,shap_stability}.csv` · `distribution_real_vs_synthetic.csv`.
  ⚠️ Any file in these two folders that the notebook does **not** write is stale output from a deleted notebook — check before citing a number from one.
- `07_BanThao_LuanVan/` — thesis drafts for the **new** direction only:
  - `_DanBai_Moi_DeAn_2026-08-10.md` — the outline mapping every section to its source
  - `Moi_PhanMoDau_draft.md` — PHẦN MỞ ĐẦU, drafted
  - `RaSoat_TiengViet_LuanVan.docx` — a reviewer's Vietnamese-language critique of the old draft. The *language* lessons still apply: prefer short sentences, avoid em-dash-enclosed clauses, keep one term per concept, and distinguish `độ chính xác tổng thể` (accuracy) from `độ chính xác dương tính` (precision).
There is deliberately no `README.md` or task checklist — both were written for the old direction and were deleted rather than rewritten. This file is the only project-level documentation.

## Status

Chương 1, 2, 3 and Kết luận are **not yet written**. PHẦN MỞ ĐẦU exists in draft and needs real citations added to item 2 (Tổng quan tình hình nghiên cứu) — the templates cite ~8 specific studies with author, year and reported accuracy, and the current draft has none.
