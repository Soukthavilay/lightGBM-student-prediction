# ADR 0002 — Thiết kế theo hợp đồng trước (interface-first)

**Trạng thái:** Đã chấp nhận · 2026-07-19

## Bối cảnh
Bản nháp đầu đi thẳng `export → predict`, tức là đóng băng *chính sách triển khai* (isotonic fit toàn bộ, ngưỡng 0,10/0,40) **trước khi** phương pháp được duyệt. Nếu giảng viên yêu cầu đổi đặc trưng/ngưỡng/cách hiệu chỉnh, cả lõi suy luận phải viết lại. Rủi ro nằm ở chỗ hiện thực trở thành thứ mà mọi tầng khác phụ thuộc vào.

## Quyết định
Định nghĩa **hợp đồng trước, hiện thực sau**. `contracts.py` chỉ import thư viện chuẩn, không biết tên bất kỳ hiện thực nào (Rule #2). Mọi tầng phụ thuộc vào *hợp đồng*, không phụ thuộc vào *adapter/artifact*. Export là bước cuối (ADR chưa có nhưng ghi trong RULES #3).

## Hệ quả
- (+) Đổi phương pháp → chỉ thay adapter + artifact; hợp đồng và tầng API đứng yên.
- (+) Có thể viết test cho hợp đồng mà không cần sklearn/artifact → test nhanh, thuần.
- (+) Một unit test tự bảo vệ: nếu ai đó lỡ `import sklearn` vào contract, test đỏ ngay.
- (−) Cần kỷ luật: chống lại cám dỗ "cứ code thẳng cho nhanh".
- Tài liệu liên quan: `DESIGN.md`, `contracts.py`.
