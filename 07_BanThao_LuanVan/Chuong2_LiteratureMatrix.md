# Bảng khảo sát tài liệu (Literature Survey Matrix) — Chương 2

> Công cụ làm việc để (a) điền số liệu `[XX]` cho mục 2.9, (b) quyết định đưa/loại từng công trình, (c) bảo đảm mỗi bài đều trả lời được "phục vụ mục nào trong Chương 2".
>
> **Chú giải ký hiệu:** ★ = đóng góp/điểm mạnh chính ở cột đó · ✔ = có đề cập · ✘ = không · ? = **cần kiểm chứng từ bản đầy đủ** · — = không áp dụng (bài phương pháp nền tảng).
> **Cột:** Obs = Observation Window (thời điểm dự báo) · Leak = Leakage Control · Cal = Calibration · Fair = Fairness · XAI = Explainability · EI = Early Intervention.
> ⚠️ Các bài MDPI (D4, D6–D10) bị chặn truy cập tự động (HTTP 403) → các ô `?` phải do tác giả đọc PDF xác nhận trước khi trích dẫn.

## A. Anchor / tài liệu phương pháp nền tảng (ĐÃ KHÓA — 12 bài)

| Ref | Yr | § | Dataset | Model | Obs | Leak | Cal | Fair | XAI | EI | Contribution (đóng góp) | Weakness (hạn chế/lưu ý khi dùng) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kaufman và cs. (2012) | 2012 | 2.4 | — | — | — | ★ | — | — | — | — | Hình thức hóa khái niệm *leakage*; quy trình phát hiện & phòng tránh | Tổng quát KDD, không có ví dụ giáo dục — cần diễn giải sang dropout |
| van Houwelingen (2007) | 2007 | 2.4 | Y sinh (survival) | Cox landmark supermodel | ★ | ★ | — | — | — | — | **Landmarking**: chỉ mô hình hóa cá thể còn *at-risk* tại thời điểm landmark | Lĩnh vực sống còn/y sinh, không phải phân loại ML — cần chuyển giao khái niệm |
| Collins và cs. (2015) TRIPOD | 2015 | 2.4 | — | — | ✔ | ✔ | ✔ | — | — | — | Checklist 22 mục báo cáo minh bạch mô hình dự báo | Hướng dẫn y khoa, không bắt buộc ngoài y tế |
| Ke và cs. (2017) LightGBM | 2017 | 2.3 | Benchmark chung | LightGBM | — | — | — | — | — | — | GBDT hiệu quả cao (GOSS, EFB), xử lý tabular + NaN | Bài báo thuật toán, không về dropout |
| Cawley & Talbot (2010) | 2010 | 2.x đánh giá | — | — | — | — | — | — | — | — | Chứng minh over-fitting khi chọn mô hình → luận cứ cho **nested CV** | Tổng quát ML |
| Niculescu-Mizil & Caruana (2005) | 2005 | 2.5 | — | 7 thuật toán | — | — | ★ | — | — | — | Đánh giá calibration; Platt & Isotonic | Mô hình tiền-deep learning; tổng quát |
| Zadrozny & Elkan (2002) | 2002 | 2.5 | — | — | — | — | ★ | — | — | — | **Isotonic regression** để hiệu chỉnh xác suất | Tổng quát |
| Guo và cs. (2017) | 2017 | 2.5 | Ảnh/văn bản | DNN | — | — | ★ | — | — | — | Mạng hiện đại kém calibrate; temperature scaling | Không phải tabular/dropout |
| Vickers & Elkin (2006) DCA | 2006 | 2.5 | Y khoa | — | — | — | ✔ | — | — | ✔ | **Decision curve analysis** (net benefit) | Bối cảnh y khoa — cần diễn giải sang can thiệp giáo dục |
| Lundberg & Lee (2017) SHAP | 2017 | 2.7 | — | — | — | — | — | — | ★ | — | SHAP: giải thích thống nhất trên nền Shapley | Tổng quát |
| Ribeiro và cs. (2016) LIME | 2016 | 2.7 | — | — | — | — | — | — | ★ | — | LIME: giải thích cục bộ model-agnostic | Giải thích cục bộ kém ổn định; tổng quát |
| Arnold & Pistilli (2012) Course Signals | 2012 | 2.8 | Purdue LMS | Thuật toán rủi ro riêng | Trong HK (real-time) | ? | ✘ | ✘ | ✘ | ★ | Hệ thống cảnh báo "đèn giao thông" + can thiệp thực tế | Thuật toán độc quyền; hiệu lực retention từng bị phản biện |

## B. Công trình theo lĩnh vực (dropout) — ứng viên supporting (~10–15; cần chốt)

> **Quyết định 19/7 — loại hai preprint.** Karimi-Haghighi và cs. (2021) và CAPIRE (2025) đều là bản tiền ấn bản chưa qua bình duyệt. Lập luận ở 2.4 đã đứng vững trên van Houwelingen (2007) + Kaufman và cs. (2012), và lập luận ở 2.6 đứng vững trên Rodolfa và cs. (2021); do đó hai mục này **không còn cần thiết** và đã được gỡ khỏi tấm bản. Giữ lại trong bảng để lưu vết quyết định, không đưa vào danh mục tài liệu tham khảo.

| Ref | Yr | § | Dataset | Model | Obs | Leak | Cal | Fair | XAI | EI | Contribution | Weakness |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~~Karimi-Haghighi và cs. (2021) *arXiv*~~ **ĐÃ LOẠI 19/7** | 2021 | ~~2.5/2.6~~ | ĐH Pompeu Fabra (nhập học) | ML có calibrate | Lúc nhập học (rất sớm) | ✔(pre-enrol) | ★ | ★ (GFPR/GFNR + mitigation) | ✘ | ✔ | Calibration + fairness mitigation **không phá calibration** | **PREPRINT** chưa peer-review; AUC 0.77–0.78; bỏ tín hiệu học kỳ |
| ~~CAPIRE (2025) *arXiv*~~ **ĐÃ LOẠI 19/7** | 2025 | ~~2.4~~ | 1.343 SV kỹ thuật (~57% dropout) | Multilevel + UMAP/DBSCAN | ★ (VOT) | ★ (leakage by construction) | ✘ | ✘ | ✔ (archetypes) | ✔ | **Leakage-aware data layer** + khái niệm VOT + 13 archetype quỹ đạo | **PREPRINT**; 1 trường, mẫu nhỏ; tỷ lệ dropout rất cao |
| EDM 2024 (early prediction) | 2024 | 2.1/2.4 | ĐH Israel, 8.267 SV | XGBoost, NN | ★ 5 mốc (4w,8w,thi1,thi2,cuối HK2) | ✔ (loại điểm ở mốc sớm, không phân tích hình thức) | ✘ | ✘ | ✘ | ✔ (thảo luận) | Dự báo sớm nhiều mốc thời gian; đặc trưng "studentship" | Không calibration/fairness; LMS biến thiên theo ngành |
| MDPI Appl. Sci. 13(21):12004 | 2023 | 2.3 | ? | **LightGBM** (F1≈0.84), SMOTE | ? | ? | ? | ? | ? | ✔ | LightGBM xử lý imbalance cho dropout | ? (MDPI 403 — đọc PDF); rủi ro leakage chưa rõ |
| MDPI Appl. Sci. 15:9202 (Day One) | 2025 | 2.1/2.8 | Tiền nhập học | XGBoost | Trước nhập học | ✔ | ? | ? | ? | ★ | Cảnh báo sớm từ dữ liệu tiền nhập học | Bỏ qua tín hiệu học kỳ; ? |
| MDPI Algorithms 18(10):662 | 2025 | 2.7 | ? | ? + SHAP | ? | ? | ? | ? | ★ | ✔ | Pipeline mô-đun + giải thích SHAP | ? (MDPI 403 — đọc PDF) |
| MDPI Computers 15(3):164 (Review) | 2025 | 2.1 | — (review) | — | — | ? | ? | ? | ? | — | Tổng quan ML/DL cho dropout | Bài review, không thực nghiệm — dùng trích bối cảnh |
| MDPI Computers 14(9):351 (Model Drift) | 2025 | 2.x bền thời gian | ? | ? | ✔ (theo thời gian) | ? | ? | ? | ✘ | ✘ | **Model drift** khi triển khai; đề xuất retrain định kỳ | ? (MDPI 403 — đọc PDF) |
| MDPI Electronics 14(22):4356 (semester records) | 2025 | 2.4 | ? | ? (sequential) | ★ (theo học kỳ) | ? | ? | ? | ? | ? | Khai thác mẫu thời gian trong hồ sơ học kỳ | ? (MDPI 403 — đọc PDF) |
| FairEduNet (Sci. Reports 2025) | 2025 | 2.6 | ? | Adversarial network | ? | ? | ? | ★ (adversarial debiasing) | ? | ? | Mạng đối kháng cho fairness trong dropout | Phức tạp; cần đọc bản đầy đủ |
| Finnish HE dropout (Technol. Soc.) | 2024 | 2.1 | ĐH Phần Lan | ML (RF/boosting) | Theo học kỳ | ? | ✘ | ✘ | ? | ✔ | Thực nghiệm dropout bối cảnh Bắc Âu | Bối cảnh khác Việt Nam; ? |
| Two-layer stacked ensemble (Comput. Educ. AI 2022) | 2022 | 2.3 | Lớp học ĐH | Stacked ensemble | ? | ? | ✘ | ✘ | ✘ | ✘ | Stacking cải thiện độ chính xác | Phức tạp; leakage/calibration chưa rõ |

---

### Cách dùng bảng này để viết 2.9 và chốt supporting
1. **Đếm để điền `[XX]`:** tổng số bài lĩnh vực (Bảng B) đưa vào Chương 2 = số công trình "được khảo sát". Ghi rõ tiêu chí chọn (năm, nguồn, có dữ liệu học kỳ…).
2. **Bằng chứng cho mỗi hạn chế ở 2.9:**
   - Rò rỉ: đa số Bảng B để trống cột **Leak** (`?`/`✘`) → củng cố hạn chế (1).
   - Calibration: cột **Cal** hầu hết `✘`/`?` → củng cố hạn chế (3).
   - Fairness: cột **Fair** chỉ 2–3 bài có `★` → củng cố hạn chế (3).
   - Early intervention: ít bài nối tới hệ thống vận hành → củng cố hạn chế (4).
3. **Việc cần làm tay:** đọc PDF 5 bài MDPI (D4, D6–D10) để thay `?` bằng dữ liệu thật; chốt danh sách supporting còn ~10–15 bài.
