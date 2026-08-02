# Ranh giới đóng góp (Scope of Contributions)

> Một trang, trả lời ba câu: **làm gì / không làm gì / khác gì trước đây.** Mục tiêu: định vị đóng góp ở tầng *thiết kế dữ liệu + quy trình đánh giá + chiến lược triển khai*, KHÔNG phải phát minh thuật toán — và cho thấy điều đó **mạnh hơn**, không phải yếu hơn.

## Luận văn ĐÓNG GÓP (what this work contributes)
1. **Thiết kế dữ liệu chống rò rỉ (data design):** quy trình *horizon-aware + cohort-strict* — với mỗi mốc *h*, giới hạn quần thể về sinh viên còn hoạt động và chỉ dùng đặc trưng HK1..*h*; là **hiện thực hóa nguyên lý landmarking** (van Houwelingen, 2007) cho bài toán bỏ học đại học Việt Nam.
2. **Bằng chứng thực nghiệm rò rỉ** trên dữ liệu thật, tái lập được từ `leakage_validation.csv`: thiết kế cũ đạt AUC 1,0000 (bốn học kỳ) và 0,9546 (HK1-2), trong khi **riêng một biến `GPA4_2` đạt 0,9556** — cao hơn cả mô hình 36 đặc trưng. Minh chứng định lượng cho vấn đề, không chỉ lập luận.
3. **Quy trình đánh giá trung thực (evaluation pipeline):** kết hợp có hệ thống — repeated OOF + bootstrap CI + DeLong + Holm + **nested CV** + **calibration/decision curve** + **kiểm định thời gian** + **fairness** + **độ ổn định của giải thích** — thành một khung đánh giá đầy đủ mà ít công trình dropout làm trọn vẹn.
4. **Chiến lược triển khai (deployment strategy):** hệ thống **cảnh báo hai tầng theo mức độ can thiệp**, đặt trên cùng một bộ xác suất đã hiệu chỉnh ở chân trời HK1-2 — tầng 1 (p ≥ 0,10) sàng lọc rộng, tầng 2 (p ≥ 0,40) can thiệp sâu — kèm dải ngưỡng để mỗi trường tự chọn điểm vận hành theo năng lực tư vấn.

> ⚠️ **Đã sửa 19/7 — đừng viết lại theo bản cũ.** (a) Thứ tự bốn đóng góp nay khớp **đúng** mục 1.6 và 5.3 (mục 2.9 trình bày cùng nội dung dưới dạng sáu nội dung chi tiết rồi nhóm lại thành bốn). (b) Trước đây mục "chiến lược triển khai" mô tả hai tầng là *"HK1 precision cao → HK1-2 quét phần còn lại"*, tức hai **thời điểm dự báo** — đó **không** phải thứ mã nguồn hiện thực. Hai tầng là hai **mức độ can thiệp** trên cùng một mô hình HK1-2; chân trời thời gian và tầng can thiệp là hai trục độc lập (xem 2.8.4, 3.11, 4.11).

## Luận văn KHÔNG đóng góp (what this work does NOT claim)
- **Không** phát minh thuật toán mới: LightGBM (Ke và cộng sự, 2017), SHAP (Lundberg & Lee, 2017), nested CV (Cawley & Talbot, 2010), DeLong, landmarking (van Houwelingen, 2007), decision curve (Vickers & Elkin, 2006) đều là công cụ **có sẵn**.
- **Không** tuyên bố LightGBM vượt trội tuyệt đối so với XGBoost/CatBoost/mô hình chuỗi.
- **Không** tuyên bố quan hệ **nhân quả** (SHAP chỉ là tương quan).
- **Không** tạo mô hình dùng được ngay cho trường/nước khác (phải huấn luyện lại).

## KHÁC BIỆT so với công trình trước (positioning)
| Khía cạnh | Phần lớn công trình trước | Luận văn này |
|---|---|---|
| Rò rỉ thời gian | Thường không kiểm soát tường minh | Chống bằng thiết kế (landmarking) + chứng minh định lượng |
| Đánh giá | Chủ yếu AUC/F1, CV phẳng | + nested CV, CI, calibration, decision curve, temporal, fairness |
| Xác suất | Ít khi hiệu chỉnh | Calibration + ECE/Brier + net benefit |
| Từ dự báo → hành động | Thường dừng ở phân loại | Hệ thống cảnh báo hai tầng theo mức độ can thiệp |
| Độ ổn định của giải thích | Thường trình bày một biểu đồ SHAP duy nhất | Đo độ ổn định qua 5 fold, chỉ diễn giải nhóm lõi |

## Câu định vị một dòng (dùng trong Kết luận)
> "Đóng góp của luận văn không nằm ở một thuật toán mới, mà ở một **khung phương pháp không-rò-rỉ, đánh giá nghiêm ngặt và triển khai được** cho dự báo bỏ học sớm — nơi giá trị đến từ thiết kế dữ liệu, quy trình đánh giá và chiến lược can thiệp, chứ không phải từ việc thay thế các thuật toán nền tảng."
