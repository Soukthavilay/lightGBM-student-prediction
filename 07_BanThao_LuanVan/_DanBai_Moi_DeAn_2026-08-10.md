# DÀN BÀI MỚI (đề án thạc sĩ) — v0 · 2026-08-10

**Đề tài:** *Ứng dụng LightGBM xây dựng mô hình dự báo và phát hiện nguyên nhân bỏ học của sinh viên*

> 📌 **Cấu trúc bám theo template** `Đề-Án-NguyenThiPhucLoan` (dự báo đột quỵ bằng Ensemble + SHAP) và `Melasma_Thesis`. Đây là dàn ý để duyệt trước, chưa phải bản viết.
> 🟢 = tái sử dụng nội dung cũ · 🟡 = cần viết mới · 🔵 = chờ thầy xác nhận dữ liệu

---

## PHẦN MỞ ĐẦU

| # | Mục | Nội dung | Nguồn |
|---|---|---|---|
| 1 | **Lý do chọn đề tài** | Bỏ học là tổn thất; phần lớn phòng tránh được nếu cảnh báo sớm; vì sao cần ML và cụ thể LightGBM | 🟢 §1.1 cũ |
| 2 | **Tổng quan tình hình nghiên cứu** | Rút gọn: các hướng dự báo bỏ học, EDM, gradient boosting trên dữ liệu bảng | 🟢 gộp Ch2 cũ (2.1, 2.2) — cắt còn 2–3 trang |
| 3 | **Mục tiêu nghiên cứu** | (a) xây mô hình **dự báo** bỏ học; (b) **phát hiện nguyên nhân/yếu tố nguy cơ** bằng SHAP; (c) so sánh LightGBM với XGBoost/CatBoost | 🟡 viết mới theo hướng đề tài |
| 4 | **Đối tượng và phạm vi** | Đối tượng: sinh viên. Dữ liệu: **bộ chuẩn Kaggle (chính)** + **Testkhoa (thực tế)**. Phạm vi: dữ liệu học vụ dạng bảng | 🔵 chốt sau khi hỏi thầy |
| 5 | **Nội dung nghiên cứu** | Liệt kê 4–6 việc: chuẩn bị dữ liệu · huấn luyện 3 mô hình · so sánh · giải thích SHAP · áp dụng cho Testkhoa | 🟡 |
| 6 | **Phương pháp nghiên cứu** | Thực nghiệm định lượng: gradient boosting (LightGBM/XGBoost/CatBoost), CV, chỉ số đánh giá, SHAP | 🟢 rút từ Ch3 cũ |
| 7 | **Ý nghĩa khoa học và thực tiễn** | KH: quy trình dự báo + giải thích trên dữ liệu bảng. TT: công cụ cảnh báo cho cố vấn học tập | 🟢 §1.6 cũ |
| 8 | **Kết cấu của đề án** | Mô tả 3 chương | 🟡 |

---

## CHƯƠNG 1 — CƠ SỞ LÝ THUYẾT

| Mục | Nội dung | Nguồn |
|---|---|---|
| 1.1 **Bài toán bỏ học sinh viên và ứng dụng AI** | Khái niệm bỏ học, hệ quả; tổng quan ứng dụng AI/ML trong dự báo bỏ học | 🟢 §2.1 + §2.2 cũ |
| 1.2 **Tổng quan về Ensemble learning** | Bagging vs boosting; ý tưởng kết hợp mô hình; vì sao mạnh trên dữ liệu bảng | 🟡 viết mới (theo template) |
| 1.3 **Thuật toán XGBoost** | Nguyên lý, ưu/nhược | 🟡 **cần thêm mới** |
| 1.4 **Thuật toán LightGBM** | Histogram, leaf-wise, xử lý NaN & categorical native — **thuật toán trọng tâm của đề tài** | 🟢 §2.3 cũ (đã tốt) |
| 1.5 **Thuật toán CatBoost** | Ordered boosting, xử lý categorical | 🟡 **cần thêm mới** |
| 1.6 **Giải thích mô hình bằng SHAP** | Giá trị Shapley; SHAP để tìm **yếu tố nguy cơ**; lưu ý diễn giải | 🟢 §2.7 cũ (đổi hướng: nhấn "yếu tố nguy cơ") |
| 1.7 **Các tiêu chí đánh giá mô hình** | AUC, F1, precision/recall, accuracy, Brier/calibration | 🟢 §2.5 cũ |

---

## CHƯƠNG 2 — DỮ LIỆU VÀ PHÁT BIỂU BÀI TOÁN

| Mục | Nội dung | Nguồn |
|---|---|---|
| 2.1 **Phát biểu bài toán** | Bài toán phân loại: dự báo sinh viên bỏ học + phân tích yếu tố nguy cơ | 🟡 |
| 2.2.1 **Bộ dữ liệu chuẩn (Kaggle)** | Mô tả "Predict Students' Dropout" (UCI/Realinho): ~4.424 SV, biến, phân bố, EDA | 🟢 từ notebook Colab (`Student_Perfor.ipynb`) |
| 2.2.2 **Dữ liệu thực tế (Testkhoa)** | Mô tả dữ liệu trường: 7.514 SV, biến học vụ | 🟢 §3.2 cũ |
| 2.3 **Chuẩn bị quy trình thực nghiệm** | Tiền xử lý, xây đặc trưng, xử lý mất cân bằng, chia train/validation/test | 🟢 §3.4 + §3.5 cũ |

---

## CHƯƠNG 3 — THIẾT KẾ MÔ HÌNH VÀ THỰC NGHIỆM

| Mục | Nội dung | Nguồn |
|---|---|---|
| 3.1 **Thiết kế mô hình và thiết lập tham số** | Cấu hình LightGBM, XGBoost, CatBoost; siêu tham số; giao thức đánh giá (CV) | 🟢 §3.5–§3.7 cũ |
| 3.2 **Kết quả thực nghiệm trên bộ Kaggle** | So sánh 3 mô hình (+ baseline notebook), chọn mô hình tốt nhất, chỉ số | 🟢 notebook Colab + 🟡 thêm LightGBM/XGBoost/CatBoost |
| 3.3 **Phát hiện nguyên nhân bằng SHAP** | Top yếu tố nguy cơ, biểu đồ SHAP, độ ổn định — phần **"phát hiện nguyên nhân"** của đề tài | 🟢 §4.10 cũ (9 đặc trưng ổn định) |
| 3.4 **Áp dụng cho dữ liệu Testkhoa (case study Việt Nam)** | Chạy lại đúng quy trình trên Testkhoa; so sánh, bàn luận khả năng áp dụng | 🔵 chờ thầy chốt cách dùng 2 bộ dữ liệu |
| 3.5 *(tuỳ chọn)* **Hệ thống cảnh báo sớm** | Ngưỡng cảnh báo → phần "dự báo/cảnh báo"; prototype | 🟢 §4.11 + `early_warning_system/` |

---

## KẾT LUẬN VÀ KIẾN NGHỊ
🟢 rút từ Ch5 cũ — nhưng viết lại theo hướng đề tài (ứng dụng, không phải đóng góp phương pháp).

---

### 📌 Ghi chú cho tác giả (tiếng Thái/nhắc việc)
- **สิ่งที่ต้องเขียนใหม่จริงๆ:** 1.2 Ensemble · 1.3 XGBoost · 1.5 CatBoost · mục tiêu/nội dung ở mở đầu — ที่เหลือย้ายของเดิมมา
- **notebook:** ต้องเพิ่ม LightGBM + XGBoost + CatBoost + SHAP เข้า Colab (ตอนนี้มีแค่ LogReg/DT/SVM/RF/KNN)
- 🔵 **รอคำตอบอาจารย์:** วิธีใช้ 2 บ่อ (Kaggle chính + Testkhoa case study) → กระทบ §2.2, §3.4
- **ของเดิมที่อาจตัดทิ้ง:** เนื้อหา "chống rò rỉ / horizon / landmarking" ที่เป็นแก่นเล่มเก่า — เก็บเป็นย่อหน้าเล็กๆ ใน tiền xử lý ได้ ถ้าอยากคงไว้ แต่ไม่เป็นแก่นอีกต่อไป
