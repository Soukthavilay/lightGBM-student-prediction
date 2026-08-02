# ADR 0003 — Chân trời gói trong PredictionProfile, không hard-code

**Trạng thái:** Đã chấp nhận · 2026-07-19

## Bối cảnh
Bản đầu gắn cứng hai chân trời "HK1" và "HK1-2" vào kiến trúc (mặc định HK1-2, thêm HK1 bằng cờ `--horizon 1`). Nếu sau này cần HK3, học kỳ 6, hay một mốc khác, logic sẽ phải rẽ nhánh theo tên chân trời ở nhiều nơi — kiến trúc bị khoá vào tập chân trời hiện tại.

## Quyết định
Hệ thống **không biết** "HK1"/"HK1-2"; nó biết một `PredictionProfile(name, horizon, artifact_dir)`. `name` chỉ là nhãn hiển thị — logic **không được** rẽ nhánh theo giá trị của nó. Thêm chân trời mới = thêm một Profile trỏ tới artifact tương ứng.

## Hệ quả
- (+) Thêm HK3/HK4/… = dữ liệu (một Profile mới), không phải sửa kiến trúc.
- (+) Một `Predictor` được gắn với đúng một Profile khi khởi tạo → rõ ràng nó phục vụ chân trời nào.
- (−) Phải xuất và quản lý một artifact riêng cho mỗi Profile.
- Được kiểm chứng bằng test: tạo `PredictionProfile("HK3", horizon=3, …)` không cần đụng `contracts.py`.
