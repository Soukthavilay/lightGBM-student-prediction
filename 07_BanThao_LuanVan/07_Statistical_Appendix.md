# Phụ lục thống kê (Statistical Appendix)

> Mô tả **chính xác** từng phương pháp/kiểm định đúng như đã cài trong `dropout_research.py` và `run_pipeline.py`, kèm giả định. Mọi tham số dưới đây là giá trị **chế độ FULL** (luận văn). Mục cần bổ sung → `TODO`.

## 1. Ước lượng ngoài-fold (Out-of-fold, OOF)
- **Repeated Stratified K-Fold**: `n_splits = 5`, `n_repeats = 10`, seed `42 + r` mỗi lần lặp. Mỗi mẫu được dự báo out-of-fold đúng một lần/lần lặp; lấy **trung bình xác suất** qua 10 lần lặp (`mean_oof`).
- Độ ổn định: báo cáo **độ lệch chuẩn AUC giữa các lần lặp** (`repeat_std`).

## 2. Khoảng tin cậy (Confidence Interval)
- **Phương pháp: bootstrap percentile** (KHÔNG phải BCa, không phải normal-approx).
- `B = 2000` lần lấy mẫu lại có hoàn lại; mức **95%** (`alpha = 0.05`) → lấy phân vị 2,5% và 97,5%.
- Mẫu bootstrap chỉ-một-lớp bị **bỏ qua** (đảm bảo tính được AUC/F1).
- Seed `np.random.default_rng(42)`.
- *Giả định:* mẫu bootstrap phản ánh phân phối tổng thể; các quan sát trao đổi được. *Lưu ý trung thực:* xác suất OOF không hoàn toàn độc lập giữa các mẫu → CI percentile có thể hơi hẹp; đây là hạn chế cần nêu.
- *`TODO` (nếu hội đồng sâu về thống kê):* cân nhắc BCa để hiệu chỉnh chệch/độ lệch.

## 3. So sánh AUC giữa mô hình
- **DeLong test** (bản nhanh theo **Sun & Xu, 2014**), paired trên cùng nhãn; thống kê **z hai phía**, p từ phân phối chuẩn.
- *Giả định:* xấp xỉ chuẩn tiệm cận của hiệu AUC (hợp lý với n vài nghìn).

## 4. So sánh mô hình theo lần lặp
- **Wilcoxon signed-rank** + **paired t-test** trên AUC per-repeat (10 giá trị/mô hình).
- *Lưu ý:* n = 10 lần lặp → **công suất thấp**; dùng như bằng chứng bổ trợ, không phải quyết định.

## 5. Hiệu chỉnh đa so sánh
- **Holm step-down** (`(n − rank) × p`, ép đơn điệu). Kiểm soát FWER.
- *Vì sao Holm không phải Bonferroni:* Holm **mạnh hơn đều** (uniformly more powerful) Bonferroni trong khi vẫn kiểm soát cùng mức FWER — không lý do gì chọn Bonferroni thuần.

## 6. Tinh chỉnh & đánh giá trung thực (Nested CV)
- **Outer** 5-fold Stratified (seed 42) để đánh giá; **inner** 3-fold để tinh chỉnh.
- **Optuna TPESampler** (seed `42 + k`), `n_trials = 40`, scoring `roc_auc`.
- Không gian tìm: `n_estimators∈[100,600]`, `learning_rate∈[0.01,0.2]` (log), `num_leaves∈[15,127]`, `max_depth∈[3,12]`, `min_child_samples∈[10,100]`, `subsample∈[0.6,1.0]`, `colsample_bytree∈[0.6,1.0]`, `reg_alpha,reg_lambda∈[1e-3,10]` (log).
- Mất cân bằng lớp: `is_unbalance = True` (tính **trong fold**).

## 7. Hiệu chỉnh xác suất (Calibration)
- **CalibratedClassifierCV** bọc quanh LightGBM, **isotonic** và **sigmoid (Platt)**, `cv = 3`, fit **trong train-fold**; OOF qua 5-fold Stratified (seed 42).
- **ECE**: `n_bins = 10`, **bin đều** (equal-width), trung bình có trọng số `|acc − conf|`.
  - ⚠️ **Lưu ý diễn giải (đã ghi trong code):** với n vài nghìn, ECE có **"sàn nhiễu" ~0,005–0,01** ngay cả khi hiệu chỉnh hoàn hảo; ECE dưới sàn chỉ nên viết *"không phát hiện miscalibration"*, KHÔNG viết *"gần hoàn hảo"*. (Điểm này thể hiện sự thận trọng thống kê — nên nhấn khi bảo vệ.)
- **Brier score**: `sklearn.brier_score_loss` — **giá trị thô, không chuẩn hóa**.
- *`TODO`:* nếu hỏi về ECE adaptive-binning, ghi rõ đang dùng equal-width và có thể mở rộng.

## 8. Phân tích đường cong quyết định (Decision Curve)
- **Net benefit**: `NB = TP/n − (FP/n)·(pt/(1−pt))`, so với "điều trị tất cả" và "không điều trị"; ngưỡng `pt ∈ linspace(0.01, 0.60, 60)`. Theo **Vickers & Elkin (2006)**.

## 9. Kiểm định thời gian & công bằng
- Train khóa **2020** → test khóa **2021** (HK1-2); AUC kèm CI **bootstrap percentile** (`bootstrap_group_auc`, B như trên).
- Fairness: AUC + CI theo nhóm **Giới tính** và **Dân tộc (Kinh vs Dân tộc thiểu số)**; **loại nhóm < 50 mẫu** hoặc không đủ 2 lớp.

---

### Tóm tắt giả định cần nêu trong luận văn
- Chuẩn tiệm cận (DeLong); trao đổi được khi bootstrap; độc lập OOF chỉ gần đúng.
- Công suất thấp của Wilcoxon (n=10 lặp).
- Sàn nhiễu ECE ở cỡ mẫu này.
- Nhóm hiếm trong fairness → CI rộng.
