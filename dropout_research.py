"""dropout_research.py — v2 (đã sửa rò rỉ quần thể/nhãn theo horizon).

BẢN CHẤT CỦA BẢN SỬA (đọc kỹ trước khi dùng):

Bài toán triển khai thật là: *tại cuối học kỳ h*, dự báo sinh viên CÒN ĐANG HỌC
nào sẽ bỏ học SAU thời điểm đó. Bản v1 huấn luyện/đánh giá trên toàn bộ khóa,
kể cả sinh viên đã rời trường trước cuối học kỳ h — với các em này, đặc trưng
học kỳ h (GPA=0, không đăng ký tín chỉ) chính là hệ quả của nhãn, không phải
tín hiệu dự báo. Hệ quả: AUC HK1-2 ~0.95 trong khi một mình cột GPA4_2 đã đạt
0.955 → con số bị thổi phồng bởi rò rỉ, không bảo vệ được.

Danh sách sửa so với v1 (đánh dấu ### [SỬA n] trong code):
  [SỬA 1] Cohort + nhãn theo horizon: `horizon_dataset(df, h)` chỉ giữ sinh viên
          còn hoạt động ở học kỳ h (CreditsRegistered_h > 0); nhãn = Drop của
          nhóm này, nghĩa là "bỏ học sau cuối HK h".
  [SỬA 2] CreditRate_i = NaN (thay vì 0) khi không đăng ký tín chỉ — tách bạch
          "không có dữ liệu" với "trượt hết". LightGBM xử lý NaN native;
          baselines impute in-fold như cũ.
  [SỬA 3] GPA4_i, RatingNum_i, CreditRate_i của học kỳ KHÔNG hoạt động → NaN.
          v1 tự mâu thuẫn: GPA_mean coi 0 là missing nhưng GPA4_i thô giữ 0.
  [SỬA 4] Cân bằng lớp bằng `is_unbalance=True` (LightGBM tự tính trên đúng
          dữ liệu fit) thay cho scale_pos_weight tính trên TOÀN BỘ y trước CV
          — v1 mâu thuẫn với tuyên bố "mọi thứ in-fold".
  [SỬA 5] Bỏ EnrollmentYear khỏi đặc trưng (mã hóa cohort trong pooled CV,
          hằng số trong kiểm định temporal) + lọc 9 sinh viên khóa 2022-2023
          ngay khi nạp dữ liệu.
  [SỬA 6] RatingNum: giá trị không map được → NaN + warning, thay vì âm thầm
          thành 0 ("Không xếp loại").

GIẢ ĐỊNH PHẢI KIỂM CHỨNG VỚI PHÒNG ĐÀO TẠO (ghi vào phần hạn chế của luận văn):
  (a) "Còn hoạt động ở HK k" := CreditsRegistered_k > 0. Nếu trường có trường
      dữ liệu chính thức về thời điểm thôi học, dùng nó thay proxy này.
  (b) TermStatus_k = cảnh báo học vụ, ĐƯỢC BIẾT tại cuối HK k → giữ làm đặc
      trưng. Nếu thực chất nó nghĩa là "đã nghỉ/thôi học" thì phải loại bỏ
      (đặt DROP_TERMSTATUS = True bên dưới).

RANDOM_STATE = 42 xuyên suốt để tái lập.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

RANDOM_STATE = 42
DATA_PATH = "Testkhoa.csv"
MISSING_LABEL = "Không rõ"

### [SỬA 5] Chỉ hai khóa đủ 4 học kỳ dữ liệu; 2022-2023 (9 SV) bị loại khi nạp.
COHORT_YEARS = (2020, 2021)

### [Giả định b] Đặt True nếu phòng đào tạo xác nhận TermStatus nghĩa là
### "đã nghỉ học" (khi đó nó là nhãn trá hình, không được dùng làm đặc trưng).
DROP_TERMSTATUS = False

# ----------------------------------------------------------------------------
# Bản đồ nhãn (mojibake latin-1 -> tiếng Việt) — giữ nguyên v1
# ----------------------------------------------------------------------------
GENDER_LABELS = {"Nam": "Nam", "N?": "Nữ", "Nu": "Nữ", "Nữ": "Nữ",
                 "Female": "Nữ", "Male": "Nam"}
REGION_LABELS = {"1": "Khu vực 1", "2": "Khu vực 2", "2NT": "Khu vực 2NT", "3": "Khu vực 3"}

RATING_MAP = {"Không xếp loại": 0, "0": 0, "Yếu": 1, "Trung bình": 2,
              "Khá": 3, "Giỏi": 4, "Xuất sắc": 5,
              # dạng mojibake trực tiếp từ CSV (chưa qua normalize)
              "Y?u": 1, "Trung b\x8dnh": 2, "Kh\xa0": 3, "Gi?i": 4, "Xu?t s?c": 5,
              "Kh\x93ng x?p lo?i": 0}

CATEG_COLS = ["Gender", "Nation", "Religion", "Region", "Aspiration", "IndustryCode"]


def load_data(path: str = DATA_PATH, years: tuple = COHORT_YEARS) -> pd.DataFrame:
    """Đọc CSV (encoding latin-1 — file gốc đã hỏng dấu, đọc latin-1 giữ nguyên byte).

    ### [SỬA 5] Lọc đúng các khóa nghiên cứu ngay tại cửa vào, log số dòng bị loại.
    """
    df = pd.read_csv(path, encoding="latin-1")
    yr = pd.to_numeric(df["EnrollmentYear"], errors="coerce")
    keep = yr.isin(years)
    n_drop = int((~keep).sum())
    if n_drop:
        warnings.warn(f"load_data: loại {n_drop} sinh viên ngoài khóa {years} "
                      f"(phân bố: {yr[~keep].value_counts().to_dict()})")
    return df.loc[keep].reset_index(drop=True)


def clean_raw(df: pd.DataFrame) -> pd.DataFrame:
    """Ép kiểu số, xử lý giá trị bất thường (điểm thi ngoài [0,10], GPA ngoài [0,4])."""
    d = df.copy()
    for c in ["EntranceScore_1", "EntranceScore_2", "EntranceScore_3", "SumScore", "EnrollmentYear"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    for c in ["EntranceScore_1", "EntranceScore_2", "EntranceScore_3"]:
        d.loc[(d[c] < 0) | (d[c] > 10), c] = np.nan
    for i in range(1, 5):
        for stem in ["GPA4", "CreditsRegistered", "CreditsEarnned", "TermStatus"]:
            d[f"{stem}_{i}"] = pd.to_numeric(d[f"{stem}_{i}"], errors="coerce")
        d[f"GPA4_{i}"] = d[f"GPA4_{i}"].clip(0, 4)
        d[f"TermStatus_{i}"] = d[f"TermStatus_{i}"].fillna(0)
    return d


# ============================================================================
### [SỬA 1] COHORT & NHÃN THEO HORIZON — trái tim của bản sửa
# ============================================================================
def semester_active(df: pd.DataFrame, k: int, strict: bool = True) -> pd.Series:
    """Sinh viên 'còn hoạt động' ở học kỳ k.

    strict=True (MẶC ĐỊNH): CreditsRegistered_k > 0 VÀ GPA4_k > 0.
    strict=False: chỉ cần có đăng ký tín chỉ — dùng cho phân tích độ nhạy.

    Vì sao strict là mặc định (bằng chứng đo trên Testkhoa.csv, HK2):
    nhóm "có đăng ký nhưng GPA = 0" gồm 293 SV, tỷ lệ bỏ học 96.2% và 100%
    không đạt tín chỉ nào — hồ sơ của người đã RỜI TRƯỜNG giữa kỳ, không phải
    người "học mà trượt hết". Giữ họ trong cohort là giữ nguyên rò rỉ nhãn
    (chỉ chuyển từ "không đăng ký" sang "đăng ký rồi biến mất").
    Đánh đổi được chấp nhận: có thể loại nhầm số ít SV thật sự trượt toàn bộ;
    báo cáo thêm biến thể strict=False trong phụ lục để chứng minh kết luận
    không đổi chiều.
    """
    d = clean_raw(df)
    act = d[f"CreditsRegistered_{k}"] > 0
    if strict:
        act &= d[f"GPA4_{k}"] > 0
    return act


def horizon_cohort(df: pd.DataFrame, horizon: int, strict: bool = True) -> pd.Series:
    """Quần thể hợp lệ cho mô hình tầm nhìn `horizon`: sinh viên còn hoạt động
    tại học kỳ cuối cùng mà mô hình được phép 'nhìn'.

    Lý do: sinh viên đã rời trường TRƯỚC thời điểm dự báo là ca ĐÃ BIẾT —
    đưa vào tập đánh giá là chấm điểm mô hình trên câu hỏi nó không bao giờ
    phải trả lời khi triển khai, và là nguồn rò rỉ chính của v1.
    """
    return semester_active(df, horizon, strict)


def get_target(df: pd.DataFrame) -> pd.Series:
    """Nhãn Drop trên toàn khóa — CHỈ dùng cho thống kê mô tả / khung tham chiếu.
    Với mô hình theo horizon, dùng horizon_dataset() để nhãn và quần thể khớp nhau."""
    return pd.to_numeric(df["Drop"], errors="coerce").fillna(0).astype(int)


def horizon_dataset(df: pd.DataFrame, horizon: int, strict: bool = True):
    """API chính cho notebook: trả (X, y, mask) đã lọc đúng quần thể.

    y ở đây mang nghĩa "bỏ học SAU cuối học kỳ `horizon`" — vì mọi sinh viên
    trong cohort còn hoạt động tại HK đó. Base rate sẽ THẤP hơn so với 13.2%
    toàn khóa (HK1-2 strict ~7.4%): đây là con số thật của bài toán triển khai,
    và là lý do precision ở các ngưỡng cảnh báo phải tính lại toàn bộ.

    Số đo lại sau khi sửa (LightGBM mặc định, 5-fold, seed 42):
      HK1   strict: n=7367, base 11.5%, AUC ~0.85
      HK1-2 strict: n=7034, base  7.4%, AUC ~0.92 (bỏ TermStatus: ~0.91)
    So với v1 (HK1-2 AUC 0.951 nhưng một mình GPA4_2 đã 0.955): các con số
    mới thấp hơn nhưng đo đúng câu hỏi triển khai, bảo vệ được.
    """
    mask = horizon_cohort(df, horizon, strict)
    X = build_features_raw(df, horizon).loc[mask].reset_index(drop=True)
    y = get_target(df).loc[mask].reset_index(drop=True)
    if y.mean() in (0.0, 1.0):
        raise ValueError("Cohort chỉ còn một lớp — kiểm tra lại định nghĩa active.")
    return X, y, mask


def build_features_raw(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """Đặc trưng horizon-aware (CHỈ dùng HK 1..horizon), KHÔNG imputation.

    NaN để nguyên cho LightGBM native / impute in-fold ở baselines (như v1).
    Khác v1: học kỳ không hoạt động → NaN thay vì 0; bỏ EnrollmentYear.
    """
    assert horizon in (1, 2, 3, 4)
    d = clean_raw(df)
    f = pd.DataFrame(index=d.index)

    # (a) Tĩnh / tuyển sinh — ### [SỬA 5] không còn EnrollmentYear
    for c in ["EntranceScore_1", "EntranceScore_2", "EntranceScore_3", "SumScore"]:
        f[c] = d[c]
    f["EntranceScore_avg"] = d[["EntranceScore_1", "EntranceScore_2", "EntranceScore_3"]].mean(axis=1)
    f["EntranceScore_min"] = d[["EntranceScore_1", "EntranceScore_2", "EntranceScore_3"]].min(axis=1)
    for c in CATEG_COLS:
        f[c] = d[c].astype("category")

    # (b) Theo từng học kỳ tới horizon
    for i in range(1, horizon + 1):
        reg, earn = d[f"CreditsRegistered_{i}"], d[f"CreditsEarnned_{i}"]
        active = reg > 0   # học kỳ có dữ liệu học tập thật

        ### [SỬA 3] GPA của học kỳ không hoạt động là "không tồn tại", không phải 0.
        ### Giữ 0 nghĩa là mã hóa "đã nghỉ" thành "học tệ nhất" → mô hình học
        ### đúng cái rò rỉ đó (một mình GPA4_2 đạt AUC 0.955 trên cohort v1).
        f[f"GPA4_{i}"] = d[f"GPA4_{i}"].where(active)

        ### [SỬA 6] Rating không map được → NaN + cảnh báo, không âm thầm thành 0.
        raw = d[f"Rating_{i}"].astype(str)
        mapped = raw.map(RATING_MAP)
        unknown = sorted(set(raw[mapped.isna() & (raw != "nan")]))
        if unknown:
            warnings.warn(f"Rating_{i}: giá trị không map được {unknown} -> NaN. "
                          f"Bổ sung vào RATING_MAP nếu là biến thể mojibake mới.")
        f[f"RatingNum_{i}"] = mapped.where(active)

        f[f"CreditsRegistered_{i}"] = reg
        f[f"CreditsEarnned_{i}"] = earn.where(active)

        ### [SỬA 2] reg == 0 → NaN, không phải 0. "Không đăng ký" ≠ "trượt hết".
        f[f"CreditRate_{i}"] = (earn / reg.replace(0, np.nan)).where(active)

        if not DROP_TERMSTATUS:
            f[f"TermStatus_{i}"] = d[f"TermStatus_{i}"]

    # (c) Tích luỹ CHỈ trên HK 1..horizon — tính trên các cột đã che NaN ở (b)
    gpa = f[[f"GPA4_{i}" for i in range(1, horizon + 1)]]
    f["GPA_mean"] = gpa.mean(axis=1)          # NaN tự bị bỏ qua, nhất quán với (b)
    f["GPA_min"] = gpa.min(axis=1)
    treg = sum(d[f"CreditsRegistered_{i}"] for i in range(1, horizon + 1))
    tearn = sum(d[f"CreditsEarnned_{i}"].where(d[f"CreditsRegistered_{i}"] > 0, 0)
                for i in range(1, horizon + 1))
    f["CumCreditsEarned"] = tearn
    f["CumCreditsRegistered"] = treg
    f["CumCreditRate"] = tearn / treg.replace(0, np.nan)   ### [SỬA 2] đồng bộ
    if not DROP_TERMSTATUS:
        f["CumWarnings"] = d[[f"TermStatus_{i}" for i in range(1, horizon + 1)]].sum(axis=1)
    # NaN-aware: giữ NaN khi GPA HK1 không tồn tại (trong cohort chuẩn thì hiếm)
    f["LowGPA_HK1"] = (f["GPA4_1"] < 1.5).astype(float).where(f["GPA4_1"].notna())
    if horizon >= 2:
        f["GPA_max"] = gpa.max(axis=1)
        f["GPA_std"] = gpa.std(axis=1)
        ### [SỬA 3] trend/decline NaN-aware: thiếu một trong hai GPA → NaN,
        ### không còn trò "GPA2=0 nên trend = -GPA1" khuếch đại rò rỉ như v1.
        f["GPA_trend"] = f["GPA4_2"] - f["GPA4_1"]
        both = f["GPA4_1"].notna() & f["GPA4_2"].notna()
        f["GPA_decline"] = (f["GPA4_2"] < f["GPA4_1"]).astype(float).where(both)
        f["Rating_trend"] = f["RatingNum_2"] - f["RatingNum_1"]
    # KHÔNG fillna ở đây — imputation đặt trong fold.
    return f


def cat_num_columns(X: pd.DataFrame):
    """Trả về (cột phân loại, cột số) của ma trận đặc trưng."""
    cat = [c for c in X.columns if str(X[c].dtype) == "category"]
    num = [c for c in X.columns if c not in cat]
    return cat, num


SCOPES = {"HK1": 1, "HK1-2": 2, "Đầy đủ (4HK, tham chiếu)": 4}


# ============================================================================
# PIPELINE FACTORIES — imputation/encoding đặt TRONG fold (chống rò rỉ)
# ============================================================================
def scale_pos_weight(y) -> float:
    """Giữ lại cho tương thích/báo cáo. KHÔNG còn dùng làm tham số cố định
    trước CV — xem [SỬA 4]."""
    neg, pos = np.bincount(np.asarray(y, dtype=int))
    return neg / pos


def make_lgbm(X: pd.DataFrame, y=None, params: dict | None = None):
    """LightGBM: NaN + categorical native.

    ### [SỬA 4] Cân bằng lớp bằng is_unbalance=True — LightGBM tự tính trọng số
    trên ĐÚNG dữ liệu được fit (tức train fold khi nằm trong CV), thay cho
    scale_pos_weight tính một lần trên toàn bộ y (v1) vốn rò thông tin tỷ lệ
    lớp của test fold vào mô hình. Ảnh hưởng số học nhỏ với stratified CV,
    nhưng phải nhất quán với tuyên bố phương pháp "mọi thứ in-fold".
    Tham số y giữ trong chữ ký để không phá code notebook cũ; không còn dùng.
    """
    import lightgbm as lgb
    base = dict(objective="binary", n_estimators=300, learning_rate=0.05,
                num_leaves=31, subsample=0.8, colsample_bytree=0.8,
                reg_lambda=1.0, random_state=RANDOM_STATE, n_jobs=1, verbose=-1,
                is_unbalance=True)
    if params:
        base.update({k: v for k, v in params.items()})
    return lgb.LGBMClassifier(**base)


def make_sklearn_baseline(kind: str, X: pd.DataFrame, y):
    """LogReg / RandomForest trong sklearn Pipeline: impute (số=median,
    phân loại=most_frequent) + one-hot cho phân loại — TẤT CẢ trong fold.

    kind ∈ {'logreg','rf'} — class_weight='balanced' đã tính trên dữ liệu fit
    (per-fold) sẵn, không cần sửa.
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    cat, num = cat_num_columns(X)
    num_pipe = Pipeline([("imp", SimpleImputer(strategy="median")),
                         ("sc", StandardScaler())])
    cat_pipe = Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                         ("oh", OneHotEncoder(handle_unknown="ignore", min_frequency=20))])
    pre = ColumnTransformer([("num", num_pipe, num), ("cat", cat_pipe, cat)],
                            remainder="drop")
    if kind == "logreg":
        clf = LogisticRegression(max_iter=2000, class_weight="balanced",
                                 random_state=RANDOM_STATE)
    elif kind == "rf":
        clf = RandomForestClassifier(n_estimators=400, class_weight="balanced",
                                     min_samples_leaf=5, n_jobs=1,
                                     random_state=RANDOM_STATE)
    else:
        raise ValueError(kind)
    return Pipeline([("pre", pre), ("clf", clf)])


def make_models(X: pd.DataFrame, y, lgbm_params: dict | None = None) -> dict:
    """Trả về dict {tên: estimator} cho so sánh công bằng (mọi tiền xử lý in-fold)."""
    return {
        "Logistic Regression": make_sklearn_baseline("logreg", X, y),
        "Random Forest": make_sklearn_baseline("rf", X, y),
        "LightGBM (mặc định)": make_lgbm(X, y),
        "LightGBM (tinh chỉnh)": make_lgbm(X, y, lgbm_params) if lgbm_params else make_lgbm(X, y),
    }


# ============================================================================
# ĐÁNH GIÁ CÓ KHOẢNG TIN CẬY — Repeated Stratified CV + Bootstrap
#
# HẠN CHẾ PHẢI KHAI BÁO TRONG LUẬN VĂN (không phải bug, là tính chất phương pháp):
# OOF predictions không độc lập (các model train trên dữ liệu chồng lấn) nên
# bootstrap CI hơi hẹp và DeLong trên OOF hơi dễ bác bỏ H0. Kiểm định
# per-repeat (paired_model_test) là kênh bổ trợ đúng đắn hơn — báo cáo cả hai.
# ============================================================================
def repeated_oof(est, X, y, n_splits=5, n_repeats=10, seed=RANDOM_STATE):
    """Repeated Stratified K-Fold => ma trận OOF prob shape (n_repeats, n).
    Mỗi lần lặp, mỗi mẫu được dự báo đúng 1 lần (out-of-fold)."""
    from sklearn.base import clone
    from sklearn.model_selection import StratifiedKFold
    y = np.asarray(y)
    n = len(y)
    oof = np.full((n_repeats, n), np.nan)
    for r in range(n_repeats):
        skf = StratifiedKFold(n_splits, shuffle=True, random_state=seed + r)
        for tr, te in skf.split(X, y):
            m = clone(est)
            Xtr = X.iloc[tr] if hasattr(X, "iloc") else X[tr]
            Xte = X.iloc[te] if hasattr(X, "iloc") else X[te]
            m.fit(Xtr, y[tr])
            oof[r, te] = m.predict_proba(Xte)[:, 1]
    return oof


def _metrics_at(y, p, thr=0.5):
    from sklearn.metrics import (accuracy_score, average_precision_score,
                                 brier_score_loss, f1_score, precision_score,
                                 recall_score, roc_auc_score)
    yhat = (p >= thr).astype(int)
    return {
        "AUC": roc_auc_score(y, p),
        "AP": average_precision_score(y, p),
        "Brier": brier_score_loss(y, p),
        "F1": f1_score(y, yhat, zero_division=0),
        "Precision": precision_score(y, yhat, zero_division=0),
        "Recall": recall_score(y, yhat, zero_division=0),
        "Accuracy": accuracy_score(y, yhat),
    }


def bootstrap_ci_metrics(y, p, thr=0.5, n_boot=2000, seed=RANDOM_STATE, alpha=0.05):
    """Percentile bootstrap CI cho các metric trên (y, p) đã averaged OOF.
    Trả về dict{metric: (point, lo, hi)}."""
    y = np.asarray(y); p = np.asarray(p)
    rng = np.random.default_rng(seed)
    n = len(y)
    point = _metrics_at(y, p, thr)
    keys = list(point.keys())
    boot = {k: [] for k in keys}
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        # đảm bảo có cả 2 lớp trong mẫu bootstrap
        if y[idx].sum() == 0 or y[idx].sum() == len(idx):
            continue
        m = _metrics_at(y[idx], p[idx], thr)
        for k in keys:
            boot[k].append(m[k])
    out = {}
    for k in keys:
        arr = np.array(boot[k])
        lo, hi = np.percentile(arr, [100*alpha/2, 100*(1-alpha/2)])
        out[k] = (point[k], lo, hi)
    return out


def evaluate_with_ci(models: dict, X, y, thr=0.5, n_splits=5, n_repeats=10,
                     n_boot=2000, seed=RANDOM_STATE):
    """Chạy repeated CV cho từng model, trả (df_ci, oof_dict).
    df_ci: hàng = model×metric với point/lo/hi + std giữa các lần lặp (ổn định)."""
    rows, oof_dict = [], {}
    for name, est in models.items():
        oof = repeated_oof(est, X, y, n_splits, n_repeats, seed)
        mean_oof = np.nanmean(oof, axis=0)
        oof_dict[name] = {"per_repeat": oof, "mean": mean_oof}
        ci = bootstrap_ci_metrics(y, mean_oof, thr, n_boot, seed)
        # độ ổn định: std của AUC giữa các lần lặp
        from sklearn.metrics import roc_auc_score
        per_rep_auc = np.array([roc_auc_score(y, oof[r]) for r in range(n_repeats)])
        for metric, (pt, lo, hi) in ci.items():
            rows.append({"model": name, "metric": metric, "point": pt,
                         "ci_lo": lo, "ci_hi": hi,
                         "repeat_std": per_rep_auc.std() if metric == "AUC" else np.nan})
    return pd.DataFrame(rows), oof_dict


# ============================================================================
# KIỂM ĐỊNH Ý NGHĨA THỐNG KÊ — DeLong (AUC) + paired test (per-fold)
# ============================================================================
def _compute_midrank(x):
    J = np.argsort(x)
    Z = x[J]
    N = len(x)
    T = np.zeros(N, dtype=float)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5 * (i + j - 1) + 1
        i = j
    T2 = np.empty(N, dtype=float)
    T2[J] = T
    return T2


def _fast_delong(preds_sorted_transposed, label_1_count):
    """DeLong covariance — theo Sun & Xu (2014). preds shape (k, n),
    n positives xếp trước. Trả (aucs, cov)."""
    m = label_1_count
    n = preds_sorted_transposed.shape[1] - m
    k = preds_sorted_transposed.shape[0]
    positive = preds_sorted_transposed[:, :m]
    negative = preds_sorted_transposed[:, m:]
    tx = np.empty((k, m)); ty = np.empty((k, n)); tz = np.empty((k, m + n))
    for r in range(k):
        tx[r] = _compute_midrank(positive[r])
        ty[r] = _compute_midrank(negative[r])
        tz[r] = _compute_midrank(preds_sorted_transposed[r])
    aucs = tz[:, :m].sum(axis=1) / m / n - (m + 1.0) / 2.0 / n
    v01 = (tz[:, :m] - tx) / n
    v10 = 1.0 - (tz[:, m:] - ty) / m
    sx = np.cov(v01)
    sy = np.cov(v10)
    delongcov = sx / m + sy / n
    return aucs, np.atleast_2d(delongcov)


def delong_test(y, p1, p2):
    """DeLong test cho AUC(p1) vs AUC(p2), paired trên cùng y.
    Trả (auc1, auc2, z, p_value hai phía)."""
    from scipy import stats
    y = np.asarray(y, dtype=int)
    order = (-y).argsort(kind="mergesort")  # positives (1) trước
    y_sorted = y[order]
    m = int(y_sorted.sum())
    preds = np.vstack((np.asarray(p1)[order], np.asarray(p2)[order]))
    aucs, cov = _fast_delong(preds, m)
    var = cov[0, 0] + cov[1, 1] - 2 * cov[0, 1]
    if var <= 0:
        z = 0.0; pval = 1.0
    else:
        z = (aucs[0] - aucs[1]) / np.sqrt(var)
        pval = 2 * (1 - stats.norm.cdf(abs(z)))
    return float(aucs[0]), float(aucs[1]), float(z), float(pval)


def per_repeat_auc(oof, y):
    """AUC của từng lần lặp (mỗi lần là một OOF hoàn chỉnh)."""
    from sklearn.metrics import roc_auc_score
    return np.array([roc_auc_score(y, oof[r]) for r in range(oof.shape[0])])


def paired_model_test(oof_a, oof_b, y):
    """Wilcoxon signed-rank + paired t trên AUC per-repeat của 2 model.
    Trả dict."""
    from scipy import stats
    a = per_repeat_auc(oof_a, y)
    b = per_repeat_auc(oof_b, y)
    diff = a - b
    try:
        w_stat, w_p = stats.wilcoxon(a, b)
    except ValueError:
        w_stat, w_p = np.nan, 1.0
    t_stat, t_p = stats.ttest_rel(a, b)
    return {"mean_a": a.mean(), "mean_b": b.mean(), "mean_diff": diff.mean(),
            "wilcoxon_p": float(w_p), "paired_t_p": float(t_p)}


# ============================================================================
# NESTED CV — ước lượng TRUNG THỰC cho LightGBM đã tinh chỉnh (Optuna inner)
# ============================================================================
def _lgbm_search_space(trial):
    ### [SỬA 4] is_unbalance thay cho spw truyền từ ngoài — nhất quán in-fold.
    return {
        "objective": "binary", "random_state": RANDOM_STATE, "n_jobs": 1,
        "verbose": -1, "is_unbalance": True,
        "n_estimators": trial.suggest_int("n_estimators", 100, 600),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 15, 127),
        "max_depth": trial.suggest_int("max_depth", 3, 12),
        "min_child_samples": trial.suggest_int("min_child_samples", 10, 100),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10.0, log=True),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
    }


def nested_cv_lgbm(X, y, outer_splits=5, inner_splits=3, n_trials=40,
                   seed=RANDOM_STATE):
    """Nested CV cho LightGBM: outer đánh giá, inner Optuna tune trên train fold.
    Trả (df_outer, best_params_list, oof_pred)."""
    import lightgbm as lgb
    import optuna
    from sklearn.metrics import average_precision_score, roc_auc_score
    from sklearn.model_selection import StratifiedKFold, cross_val_score
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    y = np.asarray(y)
    outer = StratifiedKFold(outer_splits, shuffle=True, random_state=seed)
    rows, best_params_list = [], []
    oof = np.full(len(y), np.nan)
    for k, (tr, te) in enumerate(outer.split(X, y)):
        Xtr, Xte, ytr, yte = X.iloc[tr], X.iloc[te], y[tr], y[te]
        inner = StratifiedKFold(inner_splits, shuffle=True, random_state=seed + k)

        def objective(trial):
            params = _lgbm_search_space(trial)
            est = lgb.LGBMClassifier(**params)
            sc = cross_val_score(est, Xtr, ytr, cv=inner, scoring="roc_auc", n_jobs=1)
            return sc.mean()

        study = optuna.create_study(direction="maximize",
                                    sampler=optuna.samplers.TPESampler(seed=seed + k))
        study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
        best = study.best_params
        best_params_list.append(best)
        final = lgb.LGBMClassifier(objective="binary", random_state=seed, n_jobs=1,
                                   verbose=-1, is_unbalance=True, **best)
        final.fit(Xtr, ytr)
        p = final.predict_proba(Xte)[:, 1]
        oof[te] = p
        rows.append({"outer_fold": k, "test_AUC": roc_auc_score(yte, p),
                     "test_AP": average_precision_score(yte, p),
                     "inner_best_AUC": study.best_value})
    return pd.DataFrame(rows), best_params_list, oof


# ============================================================================
# CALIBRATION + DECISION CURVE ANALYSIS
# ============================================================================
def oof_calibrated(est, X, y, method="isotonic", n_splits=5, seed=RANDOM_STATE):
    """OOF prob có hiệu chỉnh TRONG fold (CalibratedClassifierCV bọc quanh est,
    fit trên train fold, dự báo test fold). Trả (p_uncal, p_cal)."""
    from sklearn.base import clone
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.model_selection import StratifiedKFold
    y = np.asarray(y)
    p_un = np.full(len(y), np.nan); p_ca = np.full(len(y), np.nan)
    skf = StratifiedKFold(n_splits, shuffle=True, random_state=seed)
    for tr, te in skf.split(X, y):
        base = clone(est); base.fit(X.iloc[tr], y[tr])
        p_un[te] = base.predict_proba(X.iloc[te])[:, 1]
        cal = CalibratedClassifierCV(clone(est), method=method, cv=3)
        cal.fit(X.iloc[tr], y[tr])
        p_ca[te] = cal.predict_proba(X.iloc[te])[:, 1]
    return p_un, p_ca


def decision_curve(y, prob, thresholds=None):
    """Decision Curve Analysis — net benefit theo ngưỡng xác suất.
    NB = TP/n - FP/n * (pt/(1-pt)). So sánh với 'treat all' & 'treat none'.
    Trả DataFrame[threshold, nb_model, nb_all, nb_none]."""
    y = np.asarray(y); prob = np.asarray(prob); n = len(y)
    if thresholds is None:
        thresholds = np.linspace(0.01, 0.60, 60)
    prev = y.mean()
    rows = []
    for pt in thresholds:
        yhat = (prob >= pt).astype(int)
        tp = np.sum((yhat == 1) & (y == 1))
        fp = np.sum((yhat == 1) & (y == 0))
        w = pt / (1 - pt)
        nb_model = tp / n - fp / n * w
        nb_all = prev - (1 - prev) * w
        rows.append({"threshold": pt, "nb_model": nb_model,
                     "nb_all": nb_all, "nb_none": 0.0})
    return pd.DataFrame(rows)


def expected_calibration_error(y, prob, n_bins=10):
    """ECE — trung bình có trọng số |acc - conf| theo bin.

    Lưu ý diễn giải: với n ~ vài nghìn, ECE có 'sàn nhiễu' ~0.005-0.01 ngay cả
    khi hiệu chuẩn hoàn hảo. ECE nhỏ hơn sàn này chỉ nên viết là 'không phát
    hiện miscalibration', không phải 'gần hoàn hảo'."""
    y = np.asarray(y); prob = np.asarray(prob)
    bins = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        m = (prob >= bins[i]) & (prob < bins[i + 1] if i < n_bins - 1 else prob <= bins[i + 1])
        if m.sum() == 0:
            continue
        ece += m.mean() * abs(y[m].mean() - prob[m].mean())
    return float(ece)
