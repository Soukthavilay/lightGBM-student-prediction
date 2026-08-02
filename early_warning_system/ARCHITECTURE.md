# Hệ thống Cảnh báo sớm Nguy cơ Bỏ học — Kiến trúc (Sprint 1)

> Nguyên mẫu triển khai (production prototype) của mô hình trong luận văn.
> **Nguyên tắc số một:** tách bạch tuyệt đối *nghiên cứu* và *sản xuất*.

---

> **Rule #1 (xem RULES.md):** *Research is the only Source of Truth. Production is an implementation of Research, not another definition of the methodology.*

## 0. Ranh giới Research ↔ Production (luật bất di bất dịch)

```
   NGHIÊN CỨU (đã đóng băng)              SẢN XUẤT (đang xây)
   ────────────────────────              ──────────────────────
   dropout_research.py   ──import──►  early_warning_system/
   run_pipeline.py                       ├─ model/     (đóng gói mô hình)
   Testkhoa.csv                          ├─ backend/   (FastAPI)
                                         └─ frontend/  (React)
```

- Production **import** `dropout_research` như thư viện; **không sao chép, không sửa** một dòng nào của mã nghiên cứu.
- Mọi quyết định mô hình (LightGBM mặc định, `is_unbalance`, chân trời HK1-2, cách dựng đặc trưng, ngưỡng 0,10/0,40) **thuộc về luận văn**; production chỉ đóng gói lại.
- Nếu phương pháp trong luận văn đổi → chỉ cần chạy lại `export_model.py`, không đụng backend/frontend.

**Vì sao quan trọng:** khi bảo vệ, câu "hệ thống chạy đúng mô hình trong luận văn chứ?" phải trả lời được bằng một dòng — vì production *dùng chung* mã nghiên cứu, không phải bản sao có thể lệch.

---

## 1. Trạng thái hiện tại (đã xong trong Sprint 1)

| Thành phần | Tệp | Trạng thái |
|---|---|---|
| Xuất mô hình sản xuất | `model/export_model.py` | ✅ chạy được |
| Lõi suy luận (dự báo + SHAP) | `model/predict.py` | ✅ test end-to-end |
| Artifact mô hình | `model/artifacts/` | ✅ 5 tệp, MD5 dữ liệu khớp §3.12 |

**Kiểm chứng đã đạt:** n=7.034 · 36 đặc trưng · tỷ lệ bỏ học 7,38% (khớp Bảng 4.1) · đặc trưng SHAP nổi bật (GPA4_2, IndustryCode…) khớp nhóm lõi §4.10.

### Khác biệt có chủ ý so với luận văn (phải nhớ khi trình bày)
- Luận văn báo cáo **xác suất ngoài fold** (đánh giá trung thực).
- Sản xuất dùng **một mô hình đã fit** trên toàn bộ dữ liệu → xác suất cá nhân *gần* nhưng **không trùng khít** số OOF. Đây là đúng phương pháp, không phải lỗi. Đã ghi trong `metadata.json`.

---

## 2. Kiến trúc mục tiêu

```
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND (React)                                            │
│  Đăng nhập → Tải CSV → Dashboard → Chi tiết SV → Xuất báo cáo│
└───────────────┬─────────────────────────────────────────────┘
                │  HTTP/JSON
┌───────────────▼─────────────────────────────────────────────┐
│  BACKEND (FastAPI)                                           │
│  /auth      đăng nhập (JWT)                                  │
│  /upload    nhận CSV hồ sơ sinh viên                         │
│  /predict   → gọi model/predict.py                          │
│  /students  danh sách + lọc theo tầng                       │
│  /student/{id}  chi tiết + giải thích SHAP                  │
│  /export    xuất Excel/PDF                                   │
└───────────────┬─────────────────────────────────────────────┘
                │  import (cùng tiến trình)
┌───────────────▼─────────────────────────────────────────────┐
│  MODEL  early_warning_system/model/                         │
│  predict.py ──import──► dropout_research.build_features_raw  │
│  artifacts/{calibrated_model, base_model, spec, thresholds} │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Hợp đồng API (đề xuất — Sprint 2 hiện thực)

| Method | Endpoint | Vào | Ra |
|---|---|---|---|
| POST | `/auth/login` | user, pass | JWT token |
| POST | `/upload` | CSV (multipart) | job_id, số dòng, kiểm tra cột |
| POST | `/predict` | job_id | danh sách {student_id, probability, tier} |
| GET | `/students?tier=1,2` | lọc | bảng tóm tắt |
| GET | `/student/{id}` | — | probability, tier, **top_features (SHAP)** |
| GET | `/export?format=xlsx\|pdf` | lọc | tệp tải về |

Định dạng `/student/{id}` = đúng cấu trúc `predict.py` đã trả về (không cần chuyển đổi).

---

## 4. Lộ trình Sprint

| Sprint | Nội dung | Trạng thái |
|---|---|---|
| **1** | Kiến trúc + đóng gói mô hình + lõi suy luận | ✅ **xong** |
| **2** | FastAPI: `/auth`, `/upload`, `/predict`, `/students`, `/student/{id}`, `/export` | ⬜ |
| **3** | React Dashboard: danh sách theo tầng, chi tiết SHAP, lịch sử can thiệp | ⬜ |
| **4** | Đóng gói triển khai (Docker), tài liệu vận hành | ⬜ |

---

## 5. Quyết định thiết kế (ghi lại để nhất quán)

1. **Chân trời gói trong `PredictionProfile`**, không hard-code. Hệ thống biết "Profile", không biết "HK1"/"HK1-2". Profile mặc định là HK1-2 (khớp §4.11); thêm chân trời khác = thêm một Profile trỏ tới artifact tương ứng, **không** sửa kiến trúc.
2. **Đầu vào = tải CSV theo lô** (giống cách phòng đào tạo làm việc), không phải nhập từng sinh viên.
3. **Xác thực = demo đơn giản** cho bảo vệ (một tài khoản cố vấn). **Không** xử lý dữ liệu nhạy cảm thật ở nguyên mẫu này.
4. **Hai tầng = hai MỨC ĐỘ CAN THIỆP** trên cùng một mô hình, **không** phải hai thời điểm (nhất quán §2.8.4, §3.11, §4.11).
5. **Giải thích chỉ hiển thị nhóm đặc trưng ổn định** — nội dung tư vấn dựa trên top SHAP, kèm nhắc "liên hệ, không phải nhân quả" (§2.7.3).

---

## 6. Không nằm trong phạm vi nguyên mẫu

- Không huấn luyện lại theo thời gian thực (retrain là thao tác ngoại tuyến qua `export_model.py`).
- Không đo lường tác động can thiệp (đúng ranh giới luận văn — §2.8.5).
- Không kết nối cơ sở dữ liệu trường thật; đọc từ CSV tải lên.
