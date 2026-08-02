# Thiết kế Production — Interface-First (Sprint 1.5)

> **Trạng thái:** luận văn đang chờ phản hồi của giảng viên → **Nghiên cứu là Source of Truth duy nhất**. Production **chưa** được phép trở thành nguồn chân lý.
>
> **Nguyên tắc:** định nghĩa *hợp đồng (contract)* trước, hiện thực (artifact, mô hình, API) sau. Khi phương pháp trong luận văn đổi, **chỉ hiện thực đổi — hợp đồng đứng yên.**

---

## 0. Vì sao interface-first, không phải implementation-first

Bản Sprint 1 đã vội `export → predict`, tức là **đóng băng chính sách triển khai** (isotonic fit toàn bộ, ngưỡng 0,10/0,40) **trước khi** phương pháp được duyệt. Nếu giảng viên yêu cầu đổi đặc trưng / ngưỡng / cách hiệu chỉnh, cả `predict.py` phải viết lại.

Interface-first đảo ngược rủi ro đó:

```
Hợp đồng (contract)  = ỔN ĐỊNH, không phụ thuộc mô hình hiện tại
Hiện thực (adapter)  = THAY ĐƯỢC, bám theo phương pháp mới nhất
```

`export_model.py` / `predict.py` hiện có **không bị xóa** — chúng lùi xuống thành **một hiện thực tham chiếu** (đã kiểm chứng end-to-end), sẽ được *chỉnh cho khớp* hợp đồng **sau khi methodology freeze**, không phải trước.

---

## 1. Luồng dữ liệu (data flow) — trục xương sống

```
Hồ sơ sinh viên thô (CSV)
        │
        ▼
  ┌───────────────┐   thiếu cột? sai kiểu? → báo lỗi, KHÔNG đoán
  │  Validator    │
  └───────┬───────┘
        ▼
  ┌───────────────┐   dựng đặc trưng ĐÚNG chân trời h (1..h), giữ NaN
  │ FeatureBuilder│   → MỘT hiện thực CÓ THỂ ủy quyền cho mã nghiên cứu
  └───────┬───────┘     (hợp đồng không biết tên implementation — Rule #2)
        ▼
  ┌───────────────┐   điểm rủi ro thô (chưa hiệu chỉnh)
  │  RiskScorer   │
  └───────┬───────┘
        ▼
  ┌───────────────┐   điểm thô → XÁC SUẤT đáng tin (isotonic/…)
  │  Calibrator   │   ← thay được: đổi phương pháp hiệu chỉnh ở đây
  └───────┬───────┘
        ▼
  ┌───────────────┐   xác suất → tầng {0,1,2} theo ngưỡng CẤU HÌNH
  │  TierPolicy   │   ← ngưỡng là config, không hard-code trong logic
  └───────┬───────┘
        ▼
  ┌───────────────┐   đặc trưng nào đẩy rủi ro? (SHAP trên cây gốc)
  │  Explainer    │
  └───────┬───────┘
        ▼
   PredictionResult  (hợp đồng đầu ra — mục 2)
```

Mỗi khối là **một hợp đồng độc lập**. Một hiện thực *được phép hợp nhất* các khối liền kề (ví dụ `CalibratedClassifierCV` gộp RiskScorer + Calibrator) miễn là hành vi tổng hợp thỏa cả hai hợp đồng.

---

## 2. Hợp đồng dữ liệu (field-level) — bất biến

### Đầu vào: một dòng hồ sơ thô
Cùng lược đồ `Testkhoa.csv`: `StudentID`, nhân khẩu, điểm tuyển sinh, và khối theo học kỳ `GPA4_i, Rating_i, CreditsRegistered_i, CreditsEarnned_i, TermStatus_i` (i = 1..h). Chỉ dùng đến học kỳ **h** — cột của học kỳ > h **không được** đưa vào (đúng nguyên tắc chân trời).

### Đầu ra: `PredictionResult`
```json
{
  "student_id": "5057459401",
  "probability": 0.42,
  "tier": 2,
  "tier_label": "Tầng 2 — can thiệp sâu",
  "top_features": [
    { "feature": "GPA4_2", "value": 1.2, "shap": 0.83, "direction": "tăng rủi ro" }
  ]
}
```

| Trường | Kiểu | Ràng buộc |
|---|---|---|
| `student_id` | string | định danh, không rỗng |
| `probability` | float | ∈ [0,1], **đã hiệu chỉnh** |
| `tier` | int | 0 = không cảnh báo · 1 = sàng lọc rộng · 2 = can thiệp sâu |
| `tier_label` | string | nhãn người đọc, dẫn xuất từ `tier` |
| `top_features[]` | list | ≤ top_k, sắp theo \|shap\| giảm dần |
| `top_features[].direction` | string | "tăng rủi ro" nếu shap > 0, ngược lại "giảm rủi ro" |

### Báo cáo kiểm tra: `ValidationReport`
```json
{ "ok": true, "n_rows": 120, "missing_columns": [], "warnings": ["..."] }
```

---

## 3. Một điểm vào công khai — nhiều chặng nội bộ

Tầng API **chỉ thấy MỘT dịch vụ**: `Predictor`. Bên trong, `Predictor` tự ghép các chặng; API không biết và không cần biết có mấy chặng. Đổi số chặng bên trong → API không đổi.

```
        API  ─────gọi─────►  Predictor  (hợp đồng CÔNG KHAI, điểm vào duy nhất)
                                 │
        ┌────────────────────────┼───────────────────────────────┐
        ▼            ▼           ▼            ▼            ▼       ▼
    Validator  FeatureBuilder RiskScorer  Calibrator  TierPolicy Explainer
                                        (hợp đồng NỘI BỘ — API không gọi trực tiếp)
```

| Chặng nội bộ | Nhận | Trả | Điều KHÔNG được làm |
|---|---|---|---|
| **RiskScorer** | ma trận đặc trưng | điểm thô | không tự quyết ngưỡng; không giải thích |
| **Calibrator** | điểm thô | xác suất ∈ [0,1] | không đổi *thứ hạng* rủi ro (đơn điệu) |
| **TierPolicy** | xác suất + config ngưỡng | tầng {0,1,2} | không tối ưu ngưỡng trên dữ liệu |
| **Explainer** | ma trận đặc trưng | đóng góp SHAP | không tuyên bố nhân quả (§2.7.3) |

Một hiện thực ĐƯỢC PHÉP hợp nhất các chặng liền kề (vd `CalibratedClassifierCV` gộp RiskScorer + Calibrator) miễn hành vi tổng hợp thỏa cả hai hợp đồng.

Ngưỡng `tier1=0,10`, `tier2=0,40` là **tham số của TierPolicy** (`TierConfig`), nạp từ config — đổi ngưỡng = đổi config, **không** đụng mã.

### FeatureBuilder ủy quyền qua một *adapter*, không gọi thẳng
```
FeatureBuilder (hợp đồng)  ◄──  ResearchFeatureAdapter (hiện thực)  ──►  mã nghiên cứu
```
Hợp đồng `FeatureBuilder` **không biết** tên mã nghiên cứu. Việc "ủy quyền cho research" là quyết định của *một adapter cụ thể*, không phải điều khoản của hợp đồng — nên đổi nguồn đặc trưng (research_v2, pipeline riêng…) chỉ thay adapter.

### Chân trời = Profile, không hard-code
Hệ thống không biết "HK1"/"HK1-2"; nó biết một `PredictionProfile(name, horizon, artifact_dir)`. Thêm chân trời mới (HK3…) = thêm một Profile, **không** sửa kiến trúc.

---

## 4. Điều KHÔNG làm cho tới khi methodology freeze

- ❌ Không viết FastAPI / React.
- ❌ Không coi artifact hiện tại là chuẩn — nó là *một* hiện thực tham chiếu.
- ❌ Không sửa/sao chép `dropout_research.py` (FeatureBuilder & RiskScorer **ủy quyền** cho nó).
- ✅ Chỉ chốt **hợp đồng** (`contracts.py`) và tài liệu này.

Khi luận văn được duyệt và phương pháp đóng băng → mới `export_model.py` bản cuối và cho hiện thực khớp hợp đồng.
