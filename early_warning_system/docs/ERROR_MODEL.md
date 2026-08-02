# Mô hình lỗi (Error Model)

> Thiết kế TRƯỚC khi hiện thực. Lớp ngoại lệ thuần đã có ở `errors.py`; ánh xạ HTTP ở đây dành cho tầng API (Sprint 2) — cố ý **không** nhúng vào `errors.py` để lớp lỗi độc lập với web framework.

## Hệ phân cấp

```
EarlyWarningError                (gốc — bắt cái này = bắt mọi lỗi domain)
├── ValidationError              đầu vào sai (thiếu cột, sai kiểu, rỗng)
├── ArtifactMismatchError        artifact ≠ hợp đồng (phát hiện lúc NẠP)
├── PredictionError              suy luận hỏng SAU khi đầu vào đã hợp lệ
└── ProfileNotFoundError         Profile/chân trời chưa có artifact
```

## Nguyên tắc phân loại
- **Lỗi của người dùng** (`ValidationError`, `ProfileNotFoundError`) — sửa được ở phía gọi. Trả lý do cụ thể, không đoán.
- **Lỗi hệ thống** (`ArtifactMismatchError`, `PredictionError`) — người dùng không sửa được; log để vận hành xử lý.

## Khi nào nâng lỗi nào

| Tình huống | Ngoại lệ | Chặng phát hiện |
|---|---|---|
| CSV thiếu cột bắt buộc / rỗng / sai kiểu | `ValidationError` (kèm `ValidationReport`) | Validator, TRƯỚC khi dựng đặc trưng |
| `is_compatible(artifact_version)` = False | `ArtifactMismatchError(expected, found)` | Loader, lúc nạp artifact |
| MD5 dữ liệu artifact ≠ dữ liệu hiện tại | `ArtifactMismatchError` | Loader |
| Yêu cầu Profile không tồn tại | `ProfileNotFoundError` | Điều phối, trước khi nạp |
| Nạp mô hình / tính SHAP thất bại | `PredictionError` | Predictor, trong lúc suy luận |

## Ánh xạ HTTP (cho Sprint 2 — chưa hiện thực)

| Ngoại lệ | HTTP | Thân phản hồi |
|---|---|---|
| `ValidationError` | **422** Unprocessable Entity | `{error, report}` |
| `ProfileNotFoundError` | **404** Not Found | `{error}` |
| `ArtifactMismatchError` | **409** Conflict | `{error, expected, found}` |
| `PredictionError` | **500** Internal Server Error | `{error}` (chi tiết chỉ vào log) |

## Bất biến
1. Không bao giờ trả xác suất khi đầu vào chưa qua Validator.
2. `ArtifactMismatchError` phải xảy ra lúc **nạp**, không phải giữa lô dự báo.
3. Thông điệp lỗi không lộ đường dẫn hệ thống / dấu vết stack ra client.
