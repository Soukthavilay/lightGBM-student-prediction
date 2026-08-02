# ADR 0001 — Nghiên cứu là nguồn chân lý duy nhất

**Trạng thái:** Đã chấp nhận · 2026-07-19

## Bối cảnh
Cùng một phương pháp (đặc trưng, chân trời, hiệu chỉnh, ngưỡng) có thể tồn tại ở hai nơi: mã nghiên cứu (`dropout_research.py` + luận văn) và hệ thống sản xuất. Nếu cả hai đều được phép *định nghĩa* phương pháp, chúng sẽ trôi (drift) khỏi nhau theo thời gian — nguồn lỗi âm thầm và nguy hiểm nhất của loại dự án này. Ngoài ra, luận văn đang chờ giảng viên duyệt nên phương pháp **chưa** đóng băng.

## Quyết định
Nghiên cứu là **nguồn chân lý duy nhất**. Production là *một hiện thực* của nghiên cứu, không phải một định nghĩa thứ hai của phương pháp. Khi hai bên lệch nhau: research đúng, sửa production. Production được đóng gói/phục vụ/trình bày phương pháp, **không** thay đổi nó.

## Hệ quả
- (+) Không thể có hai phương pháp "hợp lệ" cùng lúc → không drift.
- (+) Giảng viên đổi phương pháp → chỉ chạy lại export; định nghĩa vẫn ở một chỗ.
- (−) Production không được "tối ưu nhanh" bằng cách sửa logic tại chỗ; mọi thay đổi phương pháp phải quay về mã nghiên cứu trước.
- Ghi thành Rule #1 trong `RULES.md`.
