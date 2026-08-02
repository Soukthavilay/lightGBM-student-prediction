#!/usr/bin/env python3
"""Lõi suy luận (inference core) — HIỆN THỰC THAM CHIẾU, chưa phải chuẩn.

> ⚠️ TRẠNG THÁI (19/7): đây là *một* hiện thực đã kiểm chứng end-to-end, KHÔNG
>    phải Source of Truth. Hợp đồng nằm ở `../contracts.py` (DESIGN.md). Sau khi
>    luận văn được duyệt và phương pháp đóng băng, tệp này sẽ được chỉnh cho khớp
>    các Protocol (Validator / FeatureBuilder / RiskScorer / Calibrator /
>    TierPolicy / Explainer). Chưa dựng API/web cho tới lúc đó.

Lõi suy luận — API (Sprint 2) sẽ gọi hàm ở đây, không lặp lại logic.

Đầu vào: DataFrame hồ sơ sinh viên THÔ (cùng cột với Testkhoa.csv).
Đầu ra mỗi sinh viên: xác suất đã hiệu chỉnh + tầng cảnh báo + đóng góp SHAP.

Tái sử dụng `dropout_research.build_features_raw` để dựng đặc trưng — bảo đảm
đặc trưng lúc dự báo GIỐNG HỆT lúc huấn luyện (không rò rỉ, đúng chân trời).
"""
import json
import sys
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

THESIS_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(THESIS_ROOT))
import dropout_research as dr  # noqa: E402

ART = Path(__file__).parent / "artifacts"


@lru_cache(maxsize=1)
def _load():
    """Nạp artifact một lần rồi giữ trong bộ nhớ (API gọi nhiều lần)."""
    spec = json.loads((ART / "feature_spec.json").read_text())
    thr = json.loads((ART / "thresholds.json").read_text())
    import shap
    base = joblib.load(ART / "base_model.pkl")
    return {
        "calibrated": joblib.load(ART / "calibrated_model.pkl"),
        "base": base,
        "explainer": shap.TreeExplainer(base),
        "spec": spec,
        "thr": thr,
    }


def _tier(p: float, thr: dict) -> int:
    """0 = không cảnh báo · 1 = sàng lọc rộng · 2 = can thiệp sâu."""
    if p >= thr["tier2"]:
        return 2
    if p >= thr["tier1"]:
        return 1
    return 0


TIER_LABEL = {0: "Không cảnh báo", 1: "Tầng 1 — sàng lọc rộng", 2: "Tầng 2 — can thiệp sâu"}


def predict(raw_df: pd.DataFrame, top_k: int = 5) -> list[dict]:
    """Dự báo cho một lô sinh viên.

    raw_df: hồ sơ thô (cùng cột Testkhoa.csv). Chỉ số hàng được giữ để tham chiếu.
    Trả về: danh sách dict {student_id, probability, tier, tier_label, top_features}.
    """
    m = _load()
    spec = m["spec"]

    # 1) dựng đặc trưng đúng như research, rồi căn cột theo đúng thứ tự lúc train
    X = dr.build_features_raw(raw_df, spec["horizon"])
    X = X.reindex(columns=spec["feature_names"])   # thiếu cột -> NaN (LightGBM xử lý được)

    # 2) xác suất đã hiệu chỉnh
    probs = m["calibrated"].predict_proba(X)[:, 1]

    # 3) đóng góp SHAP trên mô hình cây gốc (giải thích ai bị đẩy rủi ro lên/xuống)
    sv = m["explainer"].shap_values(X)
    if isinstance(sv, list):        # một số phiên bản shap trả [lớp0, lớp1]
        sv = sv[1]
    sv = np.asarray(sv)

    ids = (raw_df["StudentID"].astype(str).tolist()
           if "StudentID" in raw_df.columns else [str(i) for i in raw_df.index])

    out = []
    for i, sid in enumerate(ids):
        order = np.argsort(-np.abs(sv[i]))[:top_k]
        top = [{"feature": spec["feature_names"][j],
                "shap": round(float(sv[i][j]), 4),
                "value": (None if pd.isna(X.iloc[i, j]) else float(X.iloc[i, j])),
                "direction": "tăng rủi ro" if sv[i][j] > 0 else "giảm rủi ro"}
               for j in order]
        p = float(probs[i])
        t = _tier(p, m["thr"])
        out.append({"student_id": sid, "probability": round(p, 4),
                    "tier": t, "tier_label": TIER_LABEL[t], "top_features": top})
    return out


if __name__ == "__main__":
    # Test nhanh: lấy 5 sinh viên thật từ Testkhoa.csv chạy thử end-to-end.
    df = dr.load_data(str(THESIS_ROOT / "Testkhoa.csv"))
    sample = df.head(5)
    for r in predict(sample):
        print(f"SV {r['student_id']:>10} · p={r['probability']:.3f} · {r['tier_label']}")
        for f in r["top_features"][:3]:
            print(f"      {f['direction']:<11} {f['feature']} (SHAP {f['shap']:+.3f})")
