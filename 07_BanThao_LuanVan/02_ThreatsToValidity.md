# Các mối đe dọa tới tính hợp lệ (Threats to Validity)

> Nêu chủ động ở phần Hạn chế/Bàn luận. Mỗi mối đe dọa: **rủi ro → biện pháp giảm thiểu đã làm → hạn chế còn lại**. Khi hội đồng hỏi "điểm yếu là gì?", ta đã trả lời trước và cho thấy đã kiểm soát.

## 1. Tính hợp lệ nội tại (Internal Validity)
*Liệu quan hệ quan sát được có phản ánh đúng bản chất, không do lỗi thiết kế?*

| Mối đe dọa | Biện pháp trong luận văn | Hạn chế còn lại |
|---|---|---|
| **Rò rỉ dữ liệu (data leakage)** làm phồng kết quả | Thiết kế horizon-aware + cohort-strict (`horizon_dataset`, `build_features_raw` chỉ dùng HK1..h); minh chứng bằng số (AUC rò rỉ ~0,95) | Vẫn phụ thuộc proxy "còn hoạt động" (xem dưới) |
| **Thiên lệch chọn mẫu (selection bias)**: proxy "còn hoạt động" = `CreditsRegistered_k > 0` | Nêu rõ giả định; giới hạn quần thể tại mốc | Nếu proxy sai lệch với thực tế hành chính → chệch nhãn; cần ngày thôi học chính thức |
| **Dữ liệu thiếu (missing data)** | Điền khuyết **trong từng fold** (không rò rỉ); để NaN cho học kỳ không hoạt động (LightGBM xử lý native) | Cơ chế thiếu có thể *không ngẫu nhiên* (MNAR) — chưa mô hình hóa |
| **Nhãn trá hình**: `TermStatus_k` có thể mã hóa "đã thôi học" | Cờ `DROP_TERMSTATUS` để loại nếu phòng đào tạo xác nhận | Chưa xác nhận chính thức → rủi ro còn mở |

## 2. Tính hợp lệ ngoại tại (External Validity)
*Kết quả khái quát được tới đâu?*

| Mối đe dọa | Biện pháp | Hạn chế còn lại |
|---|---|---|
| **Đặc thù một trường/một nước** (dữ liệu Việt Nam) | Đóng góp chính là **khung phương pháp** khả chuyển, không phải một mô hình cố định | Mô hình đã huấn luyện không dùng trực tiếp cho trường khác — phải huấn luyện lại |
| **Chỉ 2 khóa (2020–2021)** đủ 4 học kỳ | Kiểm định temporal giữa hai khóa | Mẫu thời gian nhỏ → kết luận về độ bền còn hạn chế |
| **Model drift** theo thời gian/cohort | Nêu như hướng mở rộng (recalibrate/retrain định kỳ) | Chưa triển khai giám sát drift thực tế |

## 3. Tính hợp lệ khái niệm (Construct Validity)
*"Bỏ học" có được đo đúng như định nghĩa muốn đo?*

| Mối đe dọa | Biện pháp | Hạn chế còn lại |
|---|---|---|
| **Định nghĩa "bỏ học"**: nghỉ hẳn vs chuyển trường (transfer) vs tạm dừng (stop-out) đều có thể bị gộp vào cờ `Drop` | Nêu rõ định nghĩa thao tác đang dùng; đề nghị đối chiếu với phòng đào tạo | Nếu `Drop` gộp transfer/stop-out → cấu trúc mục tiêu bị nhiễu, diễn giải phải dè dặt |
| **Chuẩn hóa điểm** (GPA về thang 4, điểm đầu vào về thang 10) | Chuẩn hóa nhất quán | Khác biệt thang gốc giữa ngành/khóa có thể còn dư |
| **Đặc trưng đại diện cho "nguy cơ"** (cảnh báo học vụ, tín chỉ) | Xây từ dữ liệu học vụ chuẩn | Thiếu yếu tố tâm lý/kinh tế – xã hội (đặc biệt quan trọng ở bối cảnh Đông Nam Á) |

## 4. Tính hợp lệ của kết luận thống kê (Statistical Conclusion Validity)
*Các suy luận thống kê có vững không?*

| Mối đe dọa | Biện pháp | Hạn chế còn lại |
|---|---|---|
| **Mất cân bằng lớp** (bỏ học 11,5% ở HK1 · 7,4% ở HK1-2) đánh lừa chỉ số | Dùng F1/PR-AUC/AUC + `is_unbalance`; ngưỡng theo mục tiêu vận hành | Chỉ số vẫn nhạy với ngưỡng |
| **Lạc quan do tinh chỉnh** | **Nested CV** (Cawley & Talbot, 2010) đo mức phồng | Tốn tính toán; không gian tìm kiếm hữu hạn |
| **Bất định ước lượng** | Khoảng tin cậy **bootstrap**; DeLong cho AUC | CI bootstrap giả định tái chọn mẫu hợp lệ |
| **So sánh đa mô hình** dễ dương tính giả | Hiệu chỉnh **Holm** cho đa so sánh | Công suất giảm khi nhiều so sánh |
| **Cỡ mẫu nhóm nhỏ** trong phân tích fairness | Báo cáo CI theo nhóm | Nhóm hiếm → CI rộng, kết luận công bằng dè dặt |
| **Độ tin cậy xác suất** | Calibration + ECE + Brier (`calibration.pkl`) | Isotonic có thể quá khớp ở mẫu nhỏ |

---

### Ghi chú khi viết
- Đặt mục này ở cuối Chương 4 hoặc đầu Chương 5 (Bàn luận), trước Kết luận.
- Với mỗi ô "hạn chế còn lại", nối tới **Future Work** tương ứng để biến điểm yếu thành hướng nghiên cứu (ví dụ: proxy "hoạt động" → dùng dữ liệu thôi học chính thức; thiếu yếu tố tâm lý – kinh tế xã hội → tích hợp khảo sát).
