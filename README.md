# Dự báo sinh viên bỏ học bằng LightGBM — Bản đồ thư mục

> **Luận văn thạc sĩ** · Dữ liệu thật `Testkhoa.csv` (7.523 sinh viên, khóa 2020–2021, tỷ lệ bỏ học 13,2%).
> Thư mục được sắp xếp theo **đúng dòng thời gian (timeline) của một dự án khoa học dữ liệu**.
> Đọc theo thứ tự đánh số `00 → 06` là đi đúng hành trình phân tích.

---

## 🚀 Bắt đầu từ đâu?

**Đọc một file duy nhất để hiểu toàn bộ:** [`student_dropout_lightgbm.ipynb`](student_dropout_lightgbm.ipynb)

Notebook này được viết **như một câu chuyện 14 bước** — mỗi bước gồm một đoạn *kể chuyện* (vì sao làm)
và một ô *code* (làm thế nào), đã chạy sẵn và nhúng kết quả + hình. Đọc từ trên xuống là hiểu ngay
dữ liệu đã được phân tích thế nào, mô hình đáng tin ra sao, và vì sao sinh viên bỏ học.

| Muốn xem | Mở file |
|---|---|
| **Câu chuyện phân tích đầy đủ (đã chạy)** | `student_dropout_lightgbm.ipynb` |
| **Báo cáo 9 nâng cấp thống kê** | `01_DeAn_BaoCao/research_upgrade_report.md` |
| **Bảng số có khoảng tin cậy** | `05_KetQua_ThongKe/*.csv` |
| **Hình xuất bản** | `03_KetQua_Hinh/` |
| **Khung mở rộng Việt Nam / Lào** | `khung_da_quoc_gia/` |

---

## 🗂️ Cấu trúc thư mục theo timeline khoa học dữ liệu

### 📌 File gốc (ở thư mục Thesis — KHÔNG di chuyển)
Bốn file này phải ở gốc vì có phụ thuộc đường dẫn (import module, đường dẫn tương đối):

| File | Vai trò |
|---|---|
| `Testkhoa.csv` | **Dữ liệu thật** — 7.523 sinh viên, mã hóa latin-1. Nguồn của toàn bộ phân tích. |
| `dropout_research.py` | **Khung phân tích** — nạp dữ liệu, dựng đặc trưng theo tầm nhìn thời gian, dựng mô hình, kiểm định thống kê. Notebook `import` module này. |
| `student_dropout_lightgbm.ipynb` | **Notebook câu chuyện** — 14 bước, đã chạy, nhúng kết quả. Điểm vào chính. |
| `CLAUDE.md` | Ghi chú ngữ cảnh dự án. |

### 🔢 Các bước theo dòng thời gian

```
00_Du_Lieu/               ← BƯỚC 1: Dữ liệu
01_DeAn_BaoCao/           ← Đề án, báo cáo, đề cương (sản phẩm viết)
02_TaiLieu_ThamKhao/      ← Tài liệu tham khảo (lý thuyết nền)
03_KetQua_Hinh/           ← BƯỚC 4-6: Hình EDA + mô hình + nâng cấp thống kê
04_Model_KetQua/          ← BƯỚC 5: Mô hình đã huấn luyện (.pkl) + cấu hình
05_KetQua_ThongKe/        ← BƯỚC 6: Bảng kết quả có khoảng tin cậy (CSV)
06_TrungGian_Checkpoint/  ← Checkpoint kết quả nặng (nạp nhanh, không tính lại)
khung_da_quoc_gia/        ← BƯỚC 7: Mở rộng Việt Nam / Lào
_LuuTru/                  ← Lưu trữ: bản sao lưu, file cũ, hình trùng lặp
```

| Thư mục | Nội dung chi tiết |
|---|---|
| **`00_Du_Lieu/`** | `dataset.csv` — bản dữ liệu minh họa (mô phỏng). *Dữ liệu thật dùng cho phân tích là `Testkhoa.csv` ở gốc.* |
| **`01_DeAn_BaoCao/`** | Đề án Word (`DeAn_DuBaoBoHoc_LightGBM.docx`), **`research_upgrade_report.md`** (báo cáo chi tiết 9 nâng cấp thống kê), đánh giá triển khai, đề cương Lào (`de_cuong_soukthavilay_k27b.pdf`), phân tích so sánh HTML. |
| **`02_TaiLieu_ThamKhao/`** | 17 tài liệu nền: giáo trình thống kê, học máy, phân lớp, phát hiện bất thường, bài báo tham chiếu. |
| **`03_KetQua_Hinh/`** | Hình xuất bản. `fig_01`–`fig_30`: EDA, so sánh mô hình, SHAP, hiệu chỉnh, hai tầng, kiểm định thời gian. Thư mục con **`nang_cap_thong_ke/`**: 11 hình của phần nâng cấp thống kê (KTC, DeLong, nested CV, calibration, DCA, công bằng, ổn định SHAP) — chính là các hình notebook nhúng. |
| **`04_Model_KetQua/`** | Mô hình LightGBM đã huấn luyện: `lightgbm_stage1_hk1.pkl` (cảnh báo sớm), `lightgbm_stage2_hk12.pkl` (triển khai), `lightgbm_warning_hk12.pkl` (mô hình cảnh báo), kèm cấu hình hai tầng và danh sách đặc trưng. |
| **`05_KetQua_ThongKe/`** | 8 bảng kết quả có khoảng tin cậy 95%: `metrics_with_ci`, `model_significance` (DeLong), `nested_cv_results`, `decision_curve`, `temporal_ci`, `fairness_ci`, `temporal_fairness_ci`, `shap_stability`. |
| **`06_TrungGian_Checkpoint/`** | 5 checkpoint kết quả nặng để notebook nạp lại nhanh (`RECOMPUTE=False`): `calibration.pkl`, `nested_cv.pkl`, `oof_predictions.pkl`, `shap_data.pkl`, `temporal_fairness.pkl`. |
| **`khung_da_quoc_gia/`** | Khung mở rộng đa quốc gia: cấu hình `config_vietnam.json` / `config_laos_*.json`, pipeline `dropout_framework.py`, dashboard HTML, đặc trưng + mô hình cho từng nước. *Dữ liệu Lào là mô phỏng để minh họa khả năng mở rộng.* |
| **`_LuuTru/`** | Sao lưu an toàn: **`student_dropout_lightgbm_PRE_REWRITE_20260704_1346.ipynb`** (notebook gốc trước khi viết lại thành câu chuyện), `student_dropout_lightgbm_BACKUP.ipynb`, hình trùng lặp ở gốc, và một số file luận văn/bài trình bày không liên quan trực tiếp. |

---

## 🧭 Thứ tự đọc đề xuất

1. **`student_dropout_lightgbm.ipynb`** — đọc câu chuyện 14 bước từ đầu đến cuối (khuyến nghị mở bằng Jupyter/VS Code, kernel `dropout-ml`).
2. **`01_DeAn_BaoCao/research_upgrade_report.md`** — chi tiết phương pháp và 9 nâng cấp thống kê.
3. **`05_KetQua_ThongKe/`** + **`03_KetQua_Hinh/nang_cap_thong_ke/`** — tra cứu con số và hình gốc.
4. **`khung_da_quoc_gia/README.md`** — cách áp dụng cho Việt Nam & Lào.

---

## ⚠️ Ghi chú quan trọng về dữ liệu

- **Dữ liệu thật:** chỉ có `Testkhoa.csv` (gốc) — 7.523 sinh viên Việt Nam, khóa 2020–2021, latin-1.
- **Dữ liệu mô phỏng (không phải thật):** `00_Du_Lieu/dataset.csv` và toàn bộ file `*Laos*` trong `khung_da_quoc_gia/` — dùng để **minh họa khả năng mở rộng**, không phải kết quả nghiên cứu thật.
- **Ba tầm nhìn thời gian (horizon):** HK1 (cảnh báo sớm, AUC ~0,87) · HK1-2 (triển khai, AUC ~0,95) · Đầy đủ 4HK (tham chiếu — **bị rò rỉ nhãn**, AUC ≈ 1,0, không dùng để kết luận).

---

## 🔑 Kết quả cốt lõi (trung thực, có kiểm định)

| Câu hỏi | Trả lời |
|---|---|
| Dự báo sớm được không? | Được. HK1 AUC ~0,87; thêm HK2 lên ~0,95. |
| Mô hình nào thắng? | **Không ai thắng rõ** (DeLong + Holm, mọi p > 0,05). Chọn LightGBM vì Brier tốt nhất + giải thích được. |
| Tinh chỉnh có thổi phồng? | Không. Nested CV AUC 0,8698 ± 0,0210, optimism gap ≈ 0. |
| Xác suất có đáng tin? | Có. Isotonic → ECE 0,004 (gần hoàn hảo). |
| Bền theo thời gian? | Có. Train 2020 → test 2021: AUC 0,936 [0,921–0,950]. |
| Công bằng giữa nhóm? | Có. Mọi KTC AUC (giới tính, dân tộc) chồng lấn. |
| Vì sao bỏ học? | GPA HK2 thấp, ngành học rủi ro, cảnh báo học vụ tích lũy, tỷ lệ tín chỉ đạt thấp (ổn định 5/5 fold SHAP). |
| Can thiệp thế nào? | Hệ thống **hai tầng**: Tầng 1 (p≥0,20, recall 0,82) sàng lọc rộng; Tầng 2 (p≥0,40, precision 0,89) can thiệp sâu. |

---
*Môi trường chạy: conda env `dropout-ml` (Python 3.11 — lightgbm, optuna, shap, scikit-learn, pandas, statsmodels).*
