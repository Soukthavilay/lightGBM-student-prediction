# Hướng nghiên cứu tương lai (Future Work)

> Không viết "dùng deep learning" chung chung. Mỗi hướng: **vấn đề còn mở → cách tiếp cận cụ thể → nối với hạn chế nào** (tham chiếu `02_ThreatsToValidity.md`).
>
> ⚠️ **Đồng bộ 19/7:** tệp này nay khớp **1–1 với mục 5.5** của bản thảo (10 hướng, cùng thứ tự, cùng cách đánh số). Nếu sửa một bên, phải sửa bên còn lại. Ba hướng đầu là hướng **mới thêm 19/7** để lấp chỗ trống "hạn chế nội tại và thống kê không có hướng nghiên cứu rương ứng".

| # | Hướng | Vấn đề còn mở nó giải quyết | Nối với hạn chế (`02_ThreatsToValidity.md`) |
|---|---|---|---|
| 1 | **Kiểm chứng hai giả định bằng nguồn hành chính** — thay proxy `CreditsRegistered_k > 0` bằng ngày thôi học chính thức; đối chiếu ý nghĩa thực của `TermStatus_k` với quy chế học vụ, bật `DROP_TERMSTATUS` nếu cần | Hai giả định nền của thiết kế landmarking hiện **chưa được xác nhận**; chạy lại toàn bộ quy trình cho ra một **phân tích độ nhạy** | Internal §1 (proxy "còn hoạt động"; nhãn trá hình `TermStatus`) |
| 2 | **Mô hình hóa tường minh cơ chế dữ liệu thiếu** — kiểm tra giả thiết MNAR bằng nguồn hành chính ngoài; so sánh chiến lược giữ `NaN` với các phương án quy gán có mô hình | Cơ chế thiếu có thể không ngẫu nhiên, hiện chưa mô hình hóa | Internal §1 (dữ liệu thiếu / MNAR) |
| 3 | **Củng cố suy luận thống kê trên dự báo ngoài fold** — bootstrap theo khối hoặc kiểm định hoán vị tôn trọng cấu trúc fold; tăng số lần lặp để nâng công suất | CI hiện hơi hẹp, DeLong hơi dễ bác bỏ, kiểm định theo lần lặp chỉ n = 10 | Statistical §4 (bất định ước lượng; so sánh đa mô hình) |
| 4 | **Cảnh báo tại nhiều thời điểm liên tiếp** — cảnh báo lần đầu cuối HK1 rồi cập nhật cuối HK1-2 | Tận dụng trực tiếp cấu trúc chân trời; hiện luận văn chỉ vận hành ở một thời điểm | *(mở rộng phạm vi có chủ ý, không phải hạn chế)* |
| 5 | **Suy luận nhân quả cho can thiệp (đối chứng / uplift)** | Từ "ai có nguy cơ" sang "can thiệp nào hiệu quả cho ai" — mô phỏng chính sách phản thực | Phạm vi triển khai (không thử nghiệm can thiệp); Claim #9 (SHAP chỉ tương quan) |
| 6 | **Phân tích sống còn động (Dynamic Survival Analysis)** | Dự báo *thời điểm* bỏ học và rủi ro cạnh tranh (transfer vs nghỉ hẳn), thay vì nhãn nhị phân | Construct §3 (định nghĩa "bỏ học" bị gộp) |
| 7 | **Mô hình chuỗi (Transformer / LSTM)** | Khi có nhiều học kỳ hơn (6–8), khai thác phụ thuộc thời gian mịn mà chuỗi 4 học kỳ hiện chưa đủ | External §2 (mẫu thời gian nhỏ) |
| 8 | **Tích hợp yếu tố tâm lý – kinh tế xã hội – hành vi LMS** | Bổ sung tín hiệu ngoài học vụ, đặc biệt quan trọng ở bối cảnh Đông Nam Á | Construct §3 (thiếu yếu tố phi học vụ) |
| 9 | **Giám sát trôi mô hình và hiệu chỉnh lại định kỳ** (online / continual learning) | Cập nhật mô hình theo khóa mới, chống model drift | External §2 (model drift) |
| 10 | **Học liên kết (Federated Learning)** | Huấn luyện đa trường/đa quốc gia mà không chia sẻ dữ liệu thô — bảo vệ quyền riêng tư | External §2 (đặc thù một trường/nước) |

---

### Ghi chú

- Đóng góp cốt lõi (khung horizon-aware chống rò rỉ) **độc lập với bộ phân loại** → mọi hướng trên đều có thể "cắm" vào cùng khung mà không phá tính không-rò-rỉ.
- **Hướng 1 nên nói trước tiên khi bảo vệ.** Nó rẻ nhất (chỉ cần một trường dữ liệu bổ sung), nhưng lại quyết định mức tin cậy của mọi kết quả còn lại — và nó trả lời trực tiếp câu hỏi phản biện *"hai giả định ở 3.3.3 bao giờ mới được kiểm chứng?"*.
- Ba hướng gần luận văn nhất nếu cần rút gọn khi trình bày: **1** (kiểm chứng giả định), **5** (tác động can thiệp), **6** (sống còn động) — vì chúng nối thẳng từ ba trụ đã làm.
- ⛔ **Đã gỡ 19/7:** hướng *Graph Neural Network* (quan hệ sinh viên–môn học–bạn đồng khóa). Dữ liệu hiện có **không chứa** thông tin đồng ghi danh ở cấp môn học, nên đề xuất này không đứng trên hạn chế nào có thật của nghiên cứu; giữ lại sẽ là hướng nghiên cứu "lơ lửng". Không thêm lại trừ khi dữ liệu môn học được bổ sung.
