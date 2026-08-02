# Bảng luận điểm và bằng chứng (Research Claims vs Evidence)

> "Vũ khí" một trang cho buổi bảo vệ: mọi câu hỏi của hội đồng đều có thể quy về một **Claim** và chỉ ngay tới **Evidence** (bằng chứng thực nghiệm trong luận văn + tài liệu nền + vị trí). Học thuộc cột Claim.

| # | Luận điểm (Claim) | Bằng chứng thực nghiệm (trong luận văn) | Tài liệu nền | Vị trí |
|---|---|---|---|---|
| 1 | Rò rỉ dữ liệu làm **phồng** kết quả đánh giá | AUC HK1-2 khi rò rỉ ~0,95, xấp xỉ mức chỉ riêng `GPA4_2` đạt được | Kaufman và cộng sự (2012) | §2.4; Bước 5–5b |
| 2 | **Horizon-aware** loại được rò rỉ theo thời gian | Thiết kế `horizon_dataset()` + `build_features_raw` (HK1..h); Hình 2.1 | van Houwelingen (2007); TRIPOD (Collins và cộng sự, 2015) | §2.4; Hình 2.1 |
| 3 | **LightGBM** phù hợp bài toán | `metrics_with_ci.csv`; `model_significance.csv`; DeLong | Ke và cộng sự (2017); Grinsztajn và cộng sự (2022) | §2.3; Bước 7–8 |
| 4 | Tinh chỉnh **không** làm mô hình "ảo" quá mức | `nested_cv_results.csv` (so nested vs flat) | Cawley & Talbot (2010) | Bước 9 |
| 5 | Xác suất dự báo **đáng tin** | `calibration.pkl`; ECE, Brier; đường hiệu chỉnh | Niculescu-Mizil & Caruana (2005); Guo và cộng sự (2017) | §2.5; Bước 10 |
| 6 | Mô hình có **lợi ích quyết định** thực tế | `decision_curve.csv` (net benefit) | Vickers & Elkin (2006) | §2.5; Bước 10 |
| 7 | Mô hình **bền theo thời gian** | `temporal_ci.csv` (train 2020 → test 2021) | — | Bước 11 |
| 8 | Mô hình **công bằng** giữa các nhóm | `fairness_ci.csv` (CI theo nhóm) | Rodolfa và cộng sự (2021) | §2.6; Bước 11 |
| 9 | Giải thích **có ý nghĩa** (tương quan, không nhân quả) | `shap_stability.csv`; hình SHAP overview/dependence | Lundberg & Lee (2017); *cảnh báo:* Bilodeau và cộng sự (2024) | §2.7; Bước 12 |
| 10 | Hệ thống cảnh báo **hai tầng** triển khai được | Ngưỡng precision-target hai tầng; thiết kế HK1 → HK1-2 | Arnold & Pistilli (2012) | §2.8; Bước 13 |

---

### Cách dùng khi bảo vệ
- Hội đồng hỏi bất kỳ → xác định câu hỏi thuộc **Claim #mấy** → trả lời bằng đúng ô Evidence + chỉ tay vào bảng/hình tương ứng.
- Ba claim dễ bị xoáy nhất: **#1, #2, #5** (rò rỉ, horizon-aware, calibration) — luyện nói trơn.
- Claim #9 luôn kèm mệnh đề phòng thủ "tương quan, không nhân quả" để tránh bị bắt lỗi over-claim.
- Mỗi claim khớp một dòng trong Hình 2.3 (Khung khái niệm) → có thể trình bày cả hai song song.
