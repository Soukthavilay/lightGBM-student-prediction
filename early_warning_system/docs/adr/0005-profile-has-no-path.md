# ADR 0005 — Profile không chứa đường dẫn; Resolver ánh xạ vị trí

**Trạng thái:** Đã chấp nhận · 2026-07-19

## Bối cảnh
`PredictionProfile` ban đầu chứa `artifact_dir` — một đường dẫn filesystem. Nhưng *vị trí lưu artifact* là **hạ tầng**, không phải khái niệm nghiệp vụ. Nhét path vào domain khiến hợp đồng bị khoá vào filesystem: đổi sang S3 / cơ sở dữ liệu / model registry sẽ phải sửa cả `PredictionProfile` và mọi nơi dùng nó.

## Quyết định
`PredictionProfile` chỉ giữ `id`, `name`, `horizon` — thuần khái niệm nghiệp vụ. Việc ánh xạ `profile → vị trí artifact` giao cho một hợp đồng riêng `ProfileResolver.resolve(profile) -> ArtifactLocation`. Kiểu `ArtifactLocation` để mờ (đường dẫn/URI/handle) vì nó là chi tiết hạ tầng.

## Hệ quả
- (+) Đổi filesystem → S3 → registry: chỉ thay hiện thực `ProfileResolver`, hợp đồng và domain đứng yên.
- (+) Domain test được mà không cần biết artifact nằm ở đâu.
- (+) `ProfileResolver` là nơi tự nhiên để nâng `ProfileNotFoundError`.
- (−) Thêm một lớp gián tiếp (resolver) — chấp nhận được vì tách bạch rõ ràng.
- Được kiểm chứng: `PredictionProfile("hk12","HK1-2",2)` không còn tham chiếu đường dẫn nào.
