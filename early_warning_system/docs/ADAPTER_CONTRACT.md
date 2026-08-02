# Ràng buộc hiện thực (Adapter Contract)

> Cầu nối giữa *hợp đồng* (`contracts.py`) và *hiện thực* (adapter + artifact).
> Bất kỳ adapter production nào — hôm nay là `ResearchFeatureAdapter` + mô hình
> LightGBM, mai có thể là thứ khác — PHẢI thỏa **cả 4 điều** dưới đây thì mới
> được coi là một `Predictor` hợp lệ. Đây là tài liệu, KHÔNG phải mã.

## Bốn ràng buộc bắt buộc

### R1 — Trả đúng hình dạng `PredictionResult`
Mỗi phần tử adapter trả về phải khớp DTO trong `contracts.py`:
`student_id: str`, `probability: float ∈ [0,1]` (ĐÃ hiệu chỉnh), `tier ∈ {0,1,2}`,
`top_features` sắp theo |shap| giảm dần. `tier_label` do DTO tự dẫn xuất — adapter
không tự đặt nhãn. Không thêm/bớt trường ở tầng trả về công khai.

### R2 — Nhận `PredictionProfile`, tự phân giải vị trí qua Resolver
Adapter được khởi tạo với một `PredictionProfile(id, name, horizon)`. Nó **không**
tự ghép đường dẫn từ tên profile; nó hỏi một `ProfileResolver` (ADR 0005). Đổi nơi
lưu artifact (filesystem→S3→registry) không được làm adapter phải sửa.

### R3 — Kiểm phiên bản artifact khi NẠP, không phải khi chạy
Trước khi phục vụ dự báo, adapter đọc `artifact.json` và:
- `is_compatible(manifest["contract_version"])` = False → nâng `ArtifactMismatchError(expected, found)`.
- `manifest["feature_spec_version"]` khác bản adapter kỳ vọng → `ArtifactMismatchError`.
- (khuyến nghị) `dataset_md5` lệch → cảnh báo/nâng lỗi theo chính sách.
Mọi lệch phải lộ ra **lúc nạp**, dừng luôn — KHÔNG âm thầm dự báo sai (xem IT-05, IT-11).

### R4 — Tuyệt đối không dùng đặc trưng của học kỳ > horizon
Đây là bất biến phương pháp (landmarking §2.4) được nâng thành bất biến production.
Adapter dựng đặc trưng chỉ từ học kỳ 1..h; bất kỳ cột nào chạm học kỳ > h là rò rỉ.
Ủy quyền cho mã nghiên cứu (`build_features_raw(df, h)`) là cách bảo đảm điều này —
nhưng ràng buộc thuộc về *hành vi*, không về *thư viện* nào được dùng (Rule #2).

## Ngoài bốn ràng buộc (khuyến nghị, không bắt buộc)
- Nạp artifact một lần, giữ trong bộ nhớ (tránh đọc đĩa mỗi yêu cầu).
- SHAP giải thích mô hình cây gốc; hiệu chỉnh đơn điệu nên không đổi đặc trưng nào
  đẩy rủi ro (nhất quán §4.10).
- Mọi phát biểu SHAP ở mức **liên hệ**, không nhân quả (§2.7.3).

## Bảng truy vết ràng buộc → nơi kiểm chứng

| Ràng buộc | Kiểm bằng | Ngoại lệ khi vi phạm |
|---|---|---|
| R1 hình dạng | IT-01 | (sai hợp đồng — lỗi lập trình) |
| R2 profile/resolver | IT-08 | `ProfileNotFoundError` |
| R3 phiên bản | IT-05, IT-11 | `ArtifactMismatchError` |
| R4 không rò rỉ | IT-02 | (bất biến — phải chặn ở dựng đặc trưng) |

## Hiện trạng
`model/predict.py` là hiện thực THAM CHIẾU: đã thỏa R1 và R4 (ủy quyền cho
`build_features_raw`), **chưa** thỏa R2/R3 (chưa dùng Resolver, chưa kiểm
`artifact.json`). Sẽ hoàn thiện cho khớp 4 ràng buộc **sau khi** phương pháp đóng
băng — không phải bây giờ.
