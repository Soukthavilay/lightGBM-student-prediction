# Đặc tả kiểm thử tích hợp (Integration Test Specification)

> **Đặc tả, CHƯA phải mã.** Viết trước để khi có adapter/artifact chính thức (sau methodology freeze) thì chỉ việc hiện thực từng kịch bản. Khác `tests/test_contracts.py` (thuần, không cần mô hình) — các kịch bản ở đây **chạy qua adapter thật + artifact thật**.

## Phạm vi
Kiểm chứng toàn tuyến: `hồ sơ thô → Predictor → PredictionResult`, và các bất biến kiến trúc mà unit test không chạm tới.

## Kịch bản

### IT-01 — Toàn tuyến hợp lệ
- **Given** một lô hồ sơ sinh viên thật (lược đồ Testkhoa.csv), một Profile HK1-2 đã xuất artifact.
- **When** gọi `Predictor.predict(raw)`.
- **Then** mỗi phần tử khớp hợp đồng `PredictionResult`: `probability ∈ [0,1]`, `tier ∈ {0,1,2}`, `top_features` sắp theo |shap| giảm dần, `tier_label` khớp `tier`.

### IT-02 — Bất biến chân trời (chống rò rỉ) 🔴 quan trọng nhất
- **Given** Profile chân trời h.
- **When** dựng đặc trưng cho một sinh viên.
- **Then** **không** đặc trưng nào tham chiếu học kỳ > h. (Bảo vệ đúng nguyên tắc landmarking §2.4 ở tầng production.)

### IT-03 — Đơn điệu của tầng
- **Given** hai sinh viên có xác suất p₁ < p₂.
- **Then** `tier(p₁) ≤ tier(p₂)`. Xác suất cao hơn không bao giờ cho tầng thấp hơn.

### IT-04 — Tính lặp lại (determinism)
- **When** dự báo cùng một đầu vào hai lần.
- **Then** xác suất và tầng giống hệt (RANDOM_STATE cố định → artifact tất định).

### IT-05 — Lệch phiên bản hợp đồng
- **Given** artifact ghi `contract_version` khác MAJOR với `CONTRACT_VERSION`.
- **When** nạp.
- **Then** `ArtifactMismatchError(expected, found)` — nâng lúc **nạp**, không phải giữa lô.

### IT-06 — Lệch dữ liệu
- **Given** MD5 dữ liệu khác bản artifact được xuất.
- **Then** `ArtifactMismatchError` (hoặc cảnh báo rõ ràng theo chính sách).

### IT-07 — Đầu vào thiếu cột
- **Given** CSV thiếu cột bắt buộc.
- **Then** `ValidationError` kèm `ValidationReport.missing_columns`; **không** gọi tới suy luận.

### IT-08 — Profile không tồn tại
- **When** yêu cầu chân trời chưa xuất artifact.
- **Then** `ProfileNotFoundError`.

### IT-09 — Nhất quán giải thích (sanity, không phải khẳng định nhân quả)
- **Then** với sinh viên rủi ro cao, đặc trưng SHAP hàng đầu nằm trong nhóm lõi ổn định của luận văn (§4.10: `GPA4_2`, `IndustryCode`, …). Chỉ là kiểm tra tỉnh táo, **không** dùng làm bằng chứng nhân quả (§2.7.3).

### IT-10 — Khớp số với luận văn (ở mức phân phối, không từng cá nhân)
- **Then** tỷ lệ gắn cờ trên toàn tập gần các con số §4.11 *theo hướng* (tầng 2 hẹp hơn tầng 1). **Không** kỳ vọng trùng khít vì production dùng mô hình fit-toàn-bộ, luận văn dùng OOF (khác biệt có chủ ý — xem `artifact.json`).

### IT-11 — Feature schema drift 🔴 production hay chết vì cái này, không phải model
- **Given** `artifact.json.feature_spec_version` và `feature_spec.json` của artifact.
- **When** adapter dựng đặc trưng cho một lô mới.
- **Then** **thứ tự cột, kiểu dữ liệu, và SỐ cột** phải khớp đúng `feature_spec` — không dư, không thiếu, không đảo thứ tự. Lệch → `ArtifactMismatchError`, KHÔNG âm thầm dự báo sai.
- *Vì sao:* hệ thống production hỏng thường xuyên nhất ở **thứ tự/lược đồ đặc trưng**, không phải ở mô hình. `FEATURE_SPEC_VERSION` tăng mỗi khi tập đặc trưng đổi để bắt lệch này ngay.

## Ngoài phạm vi (thuộc test tầng API, Sprint 2)
- Xác thực/JWT, tải CSV multipart, ánh xạ mã HTTP, xuất Excel/PDF.
