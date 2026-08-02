# -*- coding: utf-8 -*-
"""run_pipeline.py — Sinh TOÀN BỘ checkpoint/bảng số cho notebook trên ĐỊNH NGHĨA MỚI
(cohort + nhãn theo horizon, dropout_research v2).

Notebook student_dropout_lightgbm.ipynb chỉ ĐỌC kết quả từ 05_KetQua_ThongKe/ và
06_TrungGian_Checkpoint/ — script này là nơi TẠO ra chúng. Chạy lại từ đầu nghĩa là:

    python3 run_pipeline.py --fast   # ~5-10 phút: kiểm tra pipeline chạy thông
    python3 run_pipeline.py          # bản đầy đủ cho luận văn (~1-2 giờ)

Sau khi chạy xong: mở notebook -> Restart Kernel -> Run All.

Mọi kết quả tính trên horizon_dataset() (quần thể strict, nhãn "bỏ học sau HK h").
RANDOM_STATE = 42 xuyên suốt. File cũ trong 2 thư mục output sẽ bị ghi đè.
"""
from __future__ import annotations

import argparse
import os
import pickle
import warnings

import numpy as np
import pandas as pd

import dropout_research as dr

warnings.filterwarnings("ignore")

CKPT = "06_TrungGian_Checkpoint"
TAB = "05_KetQua_ThongKe"
SCOPES_RUN = {"HK1": 1, "HK1-2": 2}   # khung "Đầy đủ" chỉ là tham chiếu rò rỉ, không đưa vào bảng kết quả


def holm(pvals: list[float]) -> list[float]:
    """Hiệu chỉnh Holm cho đa so sánh."""
    n = len(pvals)
    order = np.argsort(pvals)
    out = np.empty(n)
    prev = 0.0
    for rank, idx in enumerate(order):
        adj = min(1.0, (n - rank) * pvals[idx])
        prev = max(prev, adj)      # đảm bảo đơn điệu
        out[idx] = prev
    return list(out)


def bootstrap_group_auc(y, p, n_boot, seed=dr.RANDOM_STATE, alpha=0.05):
    """CI bootstrap cho AUC của một nhóm (dùng cho fairness/temporal)."""
    from sklearn.metrics import roc_auc_score
    y = np.asarray(y); p = np.asarray(p)
    rng = np.random.default_rng(seed)
    pt = roc_auc_score(y, p)
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(y), len(y))
        if 0 < y[idx].sum() < len(idx):
            vals.append(roc_auc_score(y[idx], p[idx]))
    lo, hi = np.percentile(vals, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return pt, lo, hi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true",
                    help="chế độ nhanh để kiểm tra pipeline (KHÔNG dùng số này cho luận văn)")
    ap.add_argument("--smoke", action="store_true",
                    help="mẫu con ~1500 SV + tham số tối thiểu — CHỈ kiểm tra code chạy thông")
    args = ap.parse_args()

    # cấu hình theo chế độ — không hardcode rải rác
    if args.smoke:
        n_repeats, n_boot, n_trials, tag = 1, 50, 2, "SMOKE (kiểm tra code)"
    elif args.fast:
        n_repeats, n_boot, n_trials, tag = 2, 300, 5, "FAST (kiểm tra)"
    else:
        n_repeats, n_boot, n_trials, tag = 10, 2000, 40, "FULL (luận văn)"
    print(f"=== run_pipeline: chế độ {tag} | repeats={n_repeats}, boot={n_boot}, trials={n_trials} ===")

    os.makedirs(CKPT, exist_ok=True)
    os.makedirs(TAB, exist_ok=True)

    df = dr.load_data()
    if args.smoke:
        df = df.sample(1500, random_state=dr.RANDOM_STATE).reset_index(drop=True)
    data = {}   # scope -> (X, y)
    for scope, h in SCOPES_RUN.items():
        X, y, _ = dr.horizon_dataset(df, h)
        data[scope] = (X, np.asarray(y))
        print(f"[cohort] {scope}: n={len(y)}, tỷ lệ bỏ học={y.mean():.3f}")

    # ------------------------------------------------------------------
    # 1) metrics_with_ci.csv + OOF cho các bước sau
    # ------------------------------------------------------------------
    print("\n[1/7] Repeated CV + bootstrap CI cho 4 mô hình × 2 tầm nhìn ...")
    all_ci, oof_store = [], {}
    for scope, (X, y) in data.items():
        models = dr.make_models(X, y)
        df_ci, oof_dict = dr.evaluate_with_ci(models, X, y, n_repeats=n_repeats, n_boot=n_boot)
        df_ci.insert(0, "scope", scope)
        all_ci.append(df_ci)
        oof_store[scope] = oof_dict
        for m in models:
            auc = df_ci[(df_ci.model == m) & (df_ci.metric == "AUC")].iloc[0]
            print(f"  {scope:6s} {m:22s} AUC={auc.point:.3f} [{auc.ci_lo:.3f}-{auc.ci_hi:.3f}]")
    pd.concat(all_ci).to_csv(os.path.join(TAB, "metrics_with_ci.csv"), index=False)

    # ------------------------------------------------------------------
    # 2) model_significance.csv — DeLong trên mean-OOF + Holm trong từng scope
    # ------------------------------------------------------------------
    print("\n[2/7] Kiểm định DeLong giữa các cặp mô hình ...")
    rows = []
    for scope, (X, y) in data.items():
        names = list(oof_store[scope].keys())
        pvals, tmp = [], []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                pa = oof_store[scope][names[i]]["mean"]
                pb = oof_store[scope][names[j]]["mean"]
                a1, a2, z, pv = dr.delong_test(y, pa, pb)
                tmp.append({"scope": scope, "model_A": names[i], "model_B": names[j],
                            "AUC_A": a1, "AUC_B": a2, "dAUC": a1 - a2,
                            "delong_z": z, "delong_p": pv})
                pvals.append(pv)
        for r, ph in zip(tmp, holm(pvals)):
            r["delong_p_holm"] = ph
            rows.append(r)
    pd.DataFrame(rows).to_csv(os.path.join(TAB, "model_significance.csv"), index=False)

    # ------------------------------------------------------------------
    # 3) nested_cv_results.csv — LightGBM tuned, trung thực (HK1 như bản gốc)
    # ------------------------------------------------------------------
    print("\n[3/7] Nested CV (Optuna inner) cho LightGBM — HK1 ...")
    X1, y1 = data["HK1"]
    ncv, best_params, _ = dr.nested_cv_lgbm(X1, y1, n_trials=n_trials)
    ncv.to_csv(os.path.join(TAB, "nested_cv_results.csv"), index=False)
    with open(os.path.join(CKPT, "nested_best_params.pkl"), "wb") as fh:
        pickle.dump(best_params, fh)
    print(f"  nested AUC = {ncv['test_AUC'].mean():.4f} ± {ncv['test_AUC'].std():.4f}")

    # ------------------------------------------------------------------
    # 4) calibration.pkl — hiệu chỉnh xác suất in-fold (HK1-2)
    # ------------------------------------------------------------------
    print("\n[4/7] Calibration isotonic/sigmoid (HK1-2) ...")
    from sklearn.metrics import brier_score_loss
    X2, y2 = data["HK1-2"]
    est = dr.make_lgbm(X2)
    p_un, p_iso = dr.oof_calibrated(est, X2, y2, method="isotonic")
    _, p_sig = dr.oof_calibrated(est, X2, y2, method="sigmoid")
    cal_stats = {
        "uncalibrated": (brier_score_loss(y2, p_un), dr.expected_calibration_error(y2, p_un)),
        "isotonic": (brier_score_loss(y2, p_iso), dr.expected_calibration_error(y2, p_iso)),
        "sigmoid": (brier_score_loss(y2, p_sig), dr.expected_calibration_error(y2, p_sig)),
    }
    with open(os.path.join(CKPT, "calibration.pkl"), "wb") as fh:
        pickle.dump({"y": y2, "p_uncal": p_un, "p_iso": p_iso, "p_sig": p_sig,
                     "cal_stats": cal_stats}, fh)
    for k, (b, e) in cal_stats.items():
        print(f"  {k:14s} Brier={b:.4f}  ECE={e:.4f}")

    # ------------------------------------------------------------------
    # 5) decision_curve.csv — trên xác suất isotonic
    # ------------------------------------------------------------------
    print("\n[5/7] Decision Curve Analysis ...")
    dr.decision_curve(y2, p_iso).to_csv(os.path.join(TAB, "decision_curve.csv"), index=False)

    # ------------------------------------------------------------------
    # 6) temporal_ci.csv — train khóa 2020 -> test khóa 2021, cohort MỚI
    # ------------------------------------------------------------------
    print("\n[6/7] Kiểm định thời gian 2020 -> 2021 (HK1-2, cohort mới) ...")
    from sklearn.metrics import recall_score, precision_score, average_precision_score
    d = dr.clean_raw(df)
    mask2 = dr.horizon_cohort(df, 2)
    yr = d.loc[mask2, "EnrollmentYear"].reset_index(drop=True)
    Xa, ya = X2[yr == 2020], y2[np.asarray(yr == 2020)]
    Xb, yb = X2[yr == 2021], y2[np.asarray(yr == 2021)]
    m = dr.make_lgbm(Xa)
    m.fit(Xa, ya)
    pb = m.predict_proba(Xb)[:, 1]
    pt, lo, hi = bootstrap_group_auc(yb, pb, n_boot)
    thr_rows = [{"metric": "AUC", "point": pt, "lo": lo, "hi": hi},
                {"metric": "AP", "point": average_precision_score(yb, pb), "lo": np.nan, "hi": np.nan},
                {"metric": "Recall@0.5", "point": recall_score(yb, (pb >= .5).astype(int)),
                 "lo": np.nan, "hi": np.nan},
                {"metric": "Precision@0.5", "point": precision_score(yb, (pb >= .5).astype(int),
                 zero_division=0), "lo": np.nan, "hi": np.nan}]
    pd.DataFrame(thr_rows).to_csv(os.path.join(TAB, "temporal_ci.csv"), index=False)
    print(f"  n_train={len(ya)} (2020), n_test={len(yb)} (2021), AUC={pt:.3f} [{lo:.3f}-{hi:.3f}]")

    # ------------------------------------------------------------------
    # 7) fairness_ci.csv + shap_stability.csv (HK1-2, OOF isotonic)
    # ------------------------------------------------------------------
    print("\n[7/7] Fairness theo nhóm + độ ổn định SHAP ...")
    from sklearn.metrics import recall_score as rec
    raw2 = df.loc[np.asarray(mask2)].reset_index(drop=True)
    gender = raw2["Gender"].astype(str).map(dr.GENDER_LABELS).fillna(dr.MISSING_LABEL)
    nation = np.where(raw2["Nation"].astype(str) == "Kinh", "Kinh", "Dân tộc thiểu số")
    frows = []
    for attr, series in [("Giới tính", gender), ("Dân tộc", pd.Series(nation))]:
        for grp in pd.Series(series).unique():
            g = np.asarray(series == grp)
            if g.sum() < 50 or len(set(y2[g])) < 2:
                continue
            pt, lo, hi = bootstrap_group_auc(y2[g], p_iso[g], n_boot, seed=dr.RANDOM_STATE)
            frows.append({"attr": attr, "group": grp, "n": int(g.sum()),
                          "dropout_rate": float(y2[g].mean()),
                          "AUC": pt, "AUC_lo": lo, "AUC_hi": hi,
                          "Recall": rec(y2[g], (p_iso[g] >= .5).astype(int))})
    pd.DataFrame(frows).to_csv(os.path.join(TAB, "fairness_ci.csv"), index=False)

    try:
        import shap
        from sklearn.model_selection import StratifiedKFold
        skf = StratifiedKFold(5, shuffle=True, random_state=dr.RANDOM_STATE)
        per_fold = []
        for tr, te in skf.split(X2, y2):
            m = dr.make_lgbm(X2)
            m.fit(X2.iloc[tr], y2[tr])
            sv = shap.TreeExplainer(m).shap_values(X2.iloc[te])
            sv = sv[1] if isinstance(sv, list) else sv     # tương thích các bản shap
            per_fold.append(pd.Series(np.abs(sv).mean(axis=0), index=X2.columns))
        mat = pd.concat(per_fold, axis=1)
        top10 = [set(mat[c].nlargest(10).index) for c in mat.columns]
        srows = [{"feature": f, "mean_abs_shap": mat.loc[f].mean(), "sd": mat.loc[f].std(),
                  "top10_freq": sum(f in s for s in top10)} for f in mat.index]
        pd.DataFrame(srows).sort_values("mean_abs_shap", ascending=False)\
            .to_csv(os.path.join(TAB, "shap_stability.csv"), index=False)
        print("  SHAP stability: OK (5 fold)")
    except ImportError:
        print("  !! thiếu package shap -> bỏ qua shap_stability.csv. Cài: pip install shap")

    print(f"\n=== XONG ({tag}). Mở notebook -> Restart Kernel -> Run All. ===")
    if args.fast:
        print("Nhắc lại: số ở chế độ --fast chỉ để kiểm tra pipeline, KHÔNG đưa vào luận văn.")


if __name__ == "__main__":
    main()
