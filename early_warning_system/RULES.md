# Luật kiến trúc — đọc trước khi sửa bất cứ thứ gì

## Rule #1 — Nghiên cứu là nguồn chân lý DUY NHẤT

> **Research is the only Source of Truth.**
> **Production is an implementation of Research — not another definition of the methodology.**

Nghĩa là:

- Mọi định nghĩa *phương pháp* (đặc trưng, chân trời, hiệu chỉnh, ngưỡng) sống ở `dropout_research.py` và luận văn. Production **không được** định nghĩa lại — chỉ *hiện thực* lại.
- Khi hai bên lệch nhau, **research đúng, production sai** — sửa production.
- Production được phép *đóng gói, phục vụ, trình bày* phương pháp; **không** được *thay đổi* nó.

Luật này ngăn "drift" giữa mã nghiên cứu và hệ thống thật theo thời gian — nguồn lỗi âm thầm nguy hiểm nhất của loại dự án này.

## Rule #2 — Hợp đồng đứng yên, hiện thực thay được

`contracts.py` chỉ import thư viện chuẩn. Nó **không biết** tên bất kỳ hiện thực nào (không "dropout_research", không "sklearn", không "FastAPI"). Đổi phương pháp → đổi *adapter*, hợp đồng không đổi.

## Rule #3 — Export là bước CUỐI

Chỉ xuất artifact chính thức **sau khi** luận văn được duyệt và phương pháp đóng băng. Artifact hiện tại là nguyên mẫu (`"prototype": true`).
