# Ma trận truy vết bằng chứng (Evidence Traceability Matrix)

> **Mục đích khi bảo vệ:** hội đồng chỉ vào **một câu bất kỳ** trong luận văn → người trình bày đi được **Câu trong bản in → Mục → Hình/Bảng → Tệp kết quả → Hàm trong mã nguồn** trong vòng 30 giây. Chỉ ghi những gì **thực sự tồn tại**; không suy diễn.
>
> Nguồn kiểm chứng: `run_pipeline.py` (sinh CSV/PKL, 9 bước), `dropout_research.py` (hàm), notebook `student_dropout_lightgbm.ipynb` (kết xuất hình). Hình PNG ở `03_KetQua_Hinh/` và `03_KetQua_Hinh/nang_cap_thong_ke/`.
>
> ⚠️ **Số Hình/Bảng dưới đây là số của BẢN IN** (`_BanIn/LuanVan_BanIn.docx`). Bản in tạm rút Bảng khảo sát tài liệu nên Bảng 2.2 của tệp nguồn hiển thị là **Bảng 2.1**; mọi số Chương 3–5 không bị ảnh hưởng.

| # | Luận điểm | Mục | Bước pipeline | Hình (bản in / tệp PNG) | Bảng | Tệp kết quả | Hàm |
|---|---|---|---|---|---|---|---|
| 1 | Rò rỉ làm phồng kết quả đánh giá | §4.7 | `[9/9]` | — | **Bảng 4.6** | `leakage_validation.csv` | `leakage_validation` |
| 2 | Chênh lệch quy được cho thiết kế dữ liệu (mọi yếu tố khác giữ nguyên) | §4.7 | `[9/9]` | — | **Bảng 4.6** | `leakage_validation.csv` | `leakage_validation` (dùng chung `make_lgbm`, cùng `cv`, cùng seed) |
| 3 | Horizon-aware loại rò rỉ ở tầng thiết kế | §3.3, §4.2 | — (thiết kế dữ liệu) | **Hình 2.1** / `fig_2_4_landmark_horizon.png` | **Bảng 3.2**, **Bảng 4.1** | — (là thiết kế, không phải kết quả số) | `horizon_dataset`, `build_features_raw` |
| 4 | Ba thuật toán tương đương về khả năng phân biệt | §4.3, §4.4 | `[1/9]`, `[2/9]` | **Hình 4.1**, **Hình 4.2** / `fig_metric_ci.png`, `fig_model_comparison.png` | **Bảng 4.2**, **Bảng 4.3** | `metrics_with_ci.csv`, `model_significance.csv` | `make_models`, `evaluate_with_ci`, `delong_test`, `paired_model_test` |
| 5 | LightGBM vượt trội về chất lượng xác suất (Brier) | §4.3 | `[1/9]` | **Hình 4.1** / `fig_metric_ci.png` | **Bảng 4.2** | `metrics_with_ci.csv` | `evaluate_with_ci` |
| 6 | Tinh chỉnh siêu tham số, đánh giá đúng cách, cho cải thiện khiêm tốn | §4.5 | `[3/9]` | **Hình 4.3** / `fig_nested_vs_flat.png` | **Bảng 4.4** | `nested_cv_results.csv`, `nested_best_params.pkl` | `nested_cv_lgbm` |
| 7 | Xác suất sau hiệu chỉnh đáng tin | §4.6 | `[4/9]` | **Hình 4.4** / `fig_calibration.png` | **Bảng 4.5** | `calibration.pkl` | `oof_calibrated`, `expected_calibration_error` |
| 8 | Mô hình có lợi ích quyết định thực tế | §4.6 | `[5/9]` | **Hình 4.5** / `fig_decision_curve.png` | — (số dẫn trong đoạn) | `decision_curve.csv` | `decision_curve` |
| 9 | Bền khi chuyển khóa (2020 → 2021) | §4.8 | `[7/9]` | **Hình 4.6** / `fig_temporal_ci.png` | **Bảng 4.7** | `temporal_ci.csv` | `bootstrap_group_auc` (+ thân `[7/9]`) |
| 10 | Chưa quan sát được chênh lệch giữa các nhóm, **tại ngưỡng 0,5** | §4.9 | `[8/9]` | **Hình 4.7** / `fig_fairness_gap.png` | **Bảng 4.8** | `fairness_ci.csv` | `bootstrap_group_auc` (+ thân `[8/9]`) |
| 11 | Giải thích có nhóm lõi ổn định (9/36 đặc trưng) | §4.10 | `[8/9]` | **Hình 4.8–4.10** / `fig_shap_overview.png`, `fig_shap_dependence_gpa2.png`, `fig_shap_stability.png` | **Bảng 4.9** | `shap_stability.csv` | `shap.TreeExplainer` (thân `[8/9]`) |
| 12 | Hệ thống cảnh báo hai tầng vận hành được | §4.11 | `[6/9]` | — | **Bảng 4.10** | `warning_thresholds.csv` | `warning_tiers` |
| 13 | Mỗi hạn chế đều có hướng nghiên cứu tương ứng | §5.4, §5.5 | — | — | **Bảng 5.1** | — (đối chiếu trong bản thảo) | — |

---

## Ba câu hỏi truy vết dễ bị hỏi nhất — đường đi có sẵn

| Hội đồng chỉ vào | Đi theo đường này |
|---|---|
| "AUC 0,9556 của một biến ở đâu ra?" | §4.7 → Bảng 4.6 dòng `Chỉ một biến GPA4_2` → `leakage_validation.csv` → `leakage_validation()` dòng 679–683 `roc_auc_score(y_all, -d["GPA4_2"])` |
| "Ngưỡng 0,10 / 0,40 lấy đâu ra?" | §3.11 hộp ⚠️ → `warning_tiers(..., tier1=0.10, tier2=0.40)` là **hằng số mặc định trong chữ ký hàm**; `run_pipeline.py` gọi **không truyền tham số ngưỡng** → không qua tối ưu hóa |
| "Sao công bằng lại đo ở 0,5?" | §3.9 → `thr=0.5` là **mặc định của `_metrics_at` / `evaluate_with_ci`**, dùng thống nhất cho mọi chỉ số phụ thuộc ngưỡng (§4.3, §4.8, §4.9) để so sánh chéo được — **không phải** ngưỡng vận hành |

---

## Việc còn lại để "khép" ma trận

- ✅ **Số Hình/Bảng đã gán** (19/7) — thay toàn bộ `TODO` cũ bằng số thật của bản in.
- ✅ **Claim rò rỉ đã khép** — `leakage_validation()` (`### [SỬA 8]`) sinh `leakage_validation.csv` ở bước `[9/9]`.
- ✅ **Claim hai tầng đã khép** — `warning_tiers()` (`### [SỬA 9]`) sinh `warning_thresholds.csv` ở bước `[6/9]`.
- ✅ **Số bước pipeline đã cập nhật** (19/7) — bản cũ ghi `[n/7]` từ thời pipeline còn 7 bước; nay là **9 bước**.
- ✅ **Bỏ chữ "optimism"** ở luận điểm nested CV — luận văn **không** đo mức lạc quan (không có quy trình tinh chỉnh phẳng độc lập để so); chỉ so *mặc định* với *tinh chỉnh đánh giá đúng cách*.
- 🔒 **Còn một việc về provenance:** cần **một lần chạy FULL cuối cùng** để cả 9 tệp cùng xuất hiện trong **một log duy nhất** trước khi nộp (xem cổng FINAL FULL RUN trong `MASTER_CHECKLIST.md`).
