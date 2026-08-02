#!/usr/bin/env python3
"""Xuất MÔ HÌNH SẢN XUẤT (production model) từ mã nguồn nghiên cứu — KHÔNG sửa research.

> ⚠️ THEO THIẾT KẾ MỚI (interface-first, xem DESIGN.md), bước "export" là bước
>    CUỐI CÙNG, chỉ chạy bản chính thức SAU KHI phương pháp trong luận văn được
>    đóng băng. Artifact hiện có trong artifacts/ là NGUYÊN MẪU (metadata ghi
>    "prototype": true) để kiểm chứng luồng — không dùng cho bản nộp/triển khai thật.


Ranh giới research ↔ production (tuyệt đối không vượt qua):
  - Script này *import* `dropout_research` như một THƯ VIỆN, không sao chép logic.
  - KHÔNG chạm `dropout_research.py` hay `run_pipeline.py`.
  - Mọi tham số mô hình (LightGBM mặc định, is_unbalance, chân trời, đặc trưng)
    đều do research quyết định; production chỉ "đóng gói" lại để triển khai.

Khác biệt CÓ CHỦ Ý giữa mô hình đánh giá (luận văn) và mô hình sản xuất:
  - Luận văn dùng `oof_calibrated` (ngoài fold) để BÁO CÁO trung thực — không tái
    sử dụng được để dự báo sinh viên mới.
  - Sản xuất cần MỘT đối tượng đã fit: CalibratedClassifierCV(cv=5) trên toàn bộ
    dữ liệu HK1-2. Xác suất từng cá nhân sẽ *gần* nhưng KHÔNG trùng khít số OOF
    trong Bảng 4.5/4.10 — đây là điều đúng về phương pháp, không phải lỗi.
  - SHAP: giải thích trên mô hình cây gốc (base LightGBM fit toàn bộ). Hiệu chỉnh
    isotonic là đơn điệu nên KHÔNG đổi *đặc trưng nào* đẩy rủi ro, chỉ đổi thang
    xác suất → giải thích base model là lựa chọn nhất quán với mục 4.10.

Chạy:  python3 export_model.py            # chân trời HK1-2 (mặc định, khớp §4.11)
       python3 export_model.py --horizon 1   # HK1 (cảnh báo sớm hơn)
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
from sklearn.calibration import CalibratedClassifierCV

# --- nạp research như thư viện (không sửa) -------------------------------
THESIS_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(THESIS_ROOT))
import dropout_research as dr  # noqa: E402

ART = Path(__file__).parent / "artifacts"
ART.mkdir(exist_ok=True)

# Ngưỡng hai tầng — HẰNG SỐ do luận văn ấn định (§3.11), KHÔNG tối ưu trên dữ liệu.
TIER1, TIER2 = 0.10, 0.40
# MD5 dữ liệu ghi trong §3.12 — dùng để phát hiện dữ liệu đã đổi.
DATA_MD5_THESIS = "09e5873d10cd15572e162c9fd705f34f"


def md5(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def lib_versions() -> dict:
    import lightgbm, shap, sklearn
    return {"lightgbm": lightgbm.__version__, "scikit-learn": sklearn.__version__,
            "shap": shap.__version__, "numpy": np.__version__}


def main(horizon: int):
    scope = {1: "HK1", 2: "HK1-2"}[horizon]
    data_path = THESIS_ROOT / "Testkhoa.csv"     # tuyệt đối — chạy được từ bất kỳ cwd nào
    print(f"[1/5] Nạp dữ liệu (latin-1) và dựng tập theo chân trời {scope} ...")
    df = dr.load_data(str(data_path))            # đọc Testkhoa.csv, lọc cohort 2020-2021
    X, y, _ = dr.horizon_dataset(df, horizon)    # giới hạn quần thể + đặc trưng ≤ h
    y = np.asarray(y)
    print(f"      n = {len(y)} · đặc trưng = {X.shape[1]} · tỷ lệ bỏ học = {y.mean():.4f}")

    print("[2/5] Fit mô hình xác suất (LightGBM + hiệu chỉnh isotonic, cv=5) ...")
    calibrated = CalibratedClassifierCV(dr.make_lgbm(X), method="isotonic", cv=5)
    calibrated.fit(X, y)

    print("[3/5] Fit mô hình cây gốc cho SHAP (fit toàn bộ) ...")
    base = dr.make_lgbm(X)
    base.fit(X, y)

    print("[4/5] Lưu artifact ...")
    cat_cols, num_cols = dr.cat_num_columns(X)
    joblib.dump(calibrated, ART / "calibrated_model.pkl")
    joblib.dump(base, ART / "base_model.pkl")

    feature_spec = {
        "horizon": horizon, "scope": scope,
        "n_features": int(X.shape[1]),
        "feature_names": list(X.columns),
        "categorical": list(cat_cols),
        "numeric": list(num_cols),
    }
    (ART / "feature_spec.json").write_text(json.dumps(feature_spec, ensure_ascii=False, indent=2))

    thresholds = {"tier1": TIER1, "tier2": TIER2,
                  "note": "Hằng số ấn định trước (§3.11), không tối ưu trên dữ liệu."}
    (ART / "thresholds.json").write_text(json.dumps(thresholds, ensure_ascii=False, indent=2))

    data_md5 = md5(data_path)
    metadata = {
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "horizon": horizon, "scope": scope,
        "n": int(len(y)), "dropout_rate": float(y.mean()),
        "random_state": dr.RANDOM_STATE,
        "data_md5": data_md5,
        "data_md5_matches_thesis": data_md5 == DATA_MD5_THESIS,
        "libraries": lib_versions(),
        "prototype": True,
        "note": ("Artifact NGUYÊN MẪU. Xác suất cá nhân gần nhưng không trùng khít "
                 "số OOF trong luận văn (khác biệt có chủ ý về phương pháp). "
                 "Xuất lại sau khi phương pháp được đóng băng cuối cùng."),
    }
    (ART / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2))

    print("[5/5] Kiểm tra nhanh trên chính tập huấn luyện (in-sample, chỉ để smoke-test) ...")
    p = calibrated.predict_proba(X)[:, 1]
    for thr, name in [(TIER1, "Tầng 1"), (TIER2, "Tầng 2")]:
        flagged = (p >= thr).mean()
        print(f"      {name} (p≥{thr:.2f}): gắn cờ {flagged*100:.1f}% quần thể")
    if not metadata["data_md5_matches_thesis"]:
        print(f"      ⚠️  MD5 dữ liệu ({data_md5}) KHÁC bản luận văn — kiểm tra lại nguồn dữ liệu.")

    print(f"\n✅ Xuất xong vào {ART}/  (scope={scope})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--horizon", type=int, default=2, choices=[1, 2],
                    help="1 = HK1 (sớm hơn) · 2 = HK1-2 (khớp hệ thống hai tầng §4.11, mặc định)")
    main(ap.parse_args().horizon)
