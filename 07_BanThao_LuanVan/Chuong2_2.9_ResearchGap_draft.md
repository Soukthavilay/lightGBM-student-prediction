# 2.9 Khoảng trống nghiên cứu (Research Gap)

> **BẢN THẢO (DRAFT v2)** — "La bàn" định hướng cho Chương 2, sẽ được rà soát lần cuối sau khi hoàn thành 2.1–2.8.
> ⚠️ Các chỗ đánh dấu `[XX]`, `[20XX]` là **số liệu cần tác giả điền** từ số công trình đã thực sự tổng quan — không được để nguyên khi in.

Qua tổng quan khoảng **[XX]** công trình dự báo sinh viên bỏ học được công bố trong giai đoạn **[20XX]–[20XX]**, có thể thấy hướng nghiên cứu chủ đạo tập trung vào việc **nâng cao độ chính xác** của mô hình phân loại. Trong số các công trình được khảo sát, phần lớn sử dụng các thuật toán cây tăng cường độ dốc (gradient boosting) như XGBoost và LightGBM (Ke và cộng sự, 2017) trên dữ liệu dạng bảng và thường báo cáo các chỉ số AUC, F1 ở mức cao. Tuy nhiên, khi đánh giá các công trình này dưới góc độ *"liệu một mô hình cảnh báo sớm có thực sự đáng tin và triển khai được hay không"*, bốn hạn chế mang tính hệ thống lộ ra rõ rệt.

**Thứ nhất, rò rỉ dữ liệu theo thời gian (temporal data leakage).** Trong các công trình được khảo sát, một tỷ lệ đáng kể sử dụng những biến chỉ có được ở *cuối* chương trình học — điểm trung bình tích lũy toàn khóa, tổng số môn trượt, hay trạng thái đăng ký/tốt nghiệp — để dự báo một sự kiện lẽ ra phải được cảnh báo từ sớm; trong khi chỉ một số ít tách bạch tường minh giữa **cửa sổ quan sát** (observation window) và **chân trời kết quả** (outcome horizon). Đây chính là hiện tượng rò rỉ mà Kaufman và cộng sự (2012) đã hình thức hóa: đưa vào mô hình những thông tin không khả dụng tại thời điểm dự báo. Hệ quả là các chỉ số được báo cáo có thể phản ánh khả năng "ghi lại hậu quả của nhãn" hơn là năng lực cảnh báo sớm thực sự — **khiến mô hình trông chính xác hơn đáng kể so với hiệu năng thật khi vận hành trong thực tế.**

**Thứ hai, sự lạc quan trong đánh giá do tinh chỉnh siêu tham số.** Việc lựa chọn mô hình và tối ưu siêu tham số trên cùng tập dữ liệu dùng để báo cáo kết quả dẫn tới thiên lệch lựa chọn và ước lượng hiệu năng lạc quan (Cawley & Talbot, 2010). Qua khảo sát, đa số công trình chỉ sử dụng kiểm định chéo "phẳng" (flat cross-validation), và chỉ một số ít áp dụng kiểm định chéo lồng nhau (nested cross-validation) để tách quá trình tinh chỉnh khỏi quá trình đánh giá.

**Thứ ba, thiếu đánh giá độ tin cậy của xác suất và tính công bằng.** Đa số nghiên cứu được khảo sát dừng lại ở các chỉ số phân biệt (AUC, F1) mà bỏ qua **độ hiệu chỉnh xác suất** (calibration) — điều kiện cần để một xác suất rủi ro có thể dùng cho quyết định can thiệp (Niculescu-Mizil & Caruana, 2005; Guo và cộng sự, 2017) — cũng như bỏ qua phân tích lợi ích ròng của quyết định (Vickers & Elkin, 2006). Tương tự, rất ít công trình kiểm tra tác động công bằng (fairness) giữa các nhóm nhân khẩu — giới tính, khu vực, dân tộc — dù mô hình có thể phân bổ nguồn lực hỗ trợ một cách bất bình đẳng.

**Thứ tư, khoảng cách giữa "dự báo" và "hành động".** Phần lớn công trình dừng lại ở việc phân loại chính xác mà không kết nối tới một hệ thống cảnh báo sớm và can thiệp có thể vận hành trong nhà trường (Arnold & Pistilli, 2012). Kết quả là mô hình có giá trị học thuật nhưng khó chuyển thành công cụ hỗ trợ quyết định cho cố vấn học tập.

Từ bốn hạn chế trên, **khoảng trống nghiên cứu** mà luận văn hướng tới là xây dựng một quy trình dự báo bỏ học **không rò rỉ và có thể triển khai** cho bối cảnh giáo dục đại học Việt Nam. Cụ thể, luận văn:

1. đề xuất kỹ thuật **đặc trưng theo chân trời thời gian** (horizon-aware feature engineering). Cần nhấn mạnh rằng đây không phải một kỹ thuật được đặt tên mới, mà là **sự hiện thực hóa (implementation) nguyên lý landmarking** trong phân tích lịch sử biến cố (van Houwelingen, 2007) cho bài toán dự báo bỏ học: chỉ sử dụng dữ liệu đến học kỳ *h* và giới hạn quần thể về những sinh viên còn trong diện rủi ro tại đúng thời điểm đó — phù hợp với khuyến nghị báo cáo minh bạch mô hình dự báo (TRIPOD; Collins và cộng sự, 2015);
2. **đánh giá nghiêm ngặt** bằng nested cross-validation để tránh lạc quan do tinh chỉnh (Cawley & Talbot, 2010);
3. kiểm tra **calibration** và **đường cong quyết định** (decision curve) nhằm bảo đảm xác suất dự báo đáng tin và hữu ích cho can thiệp;
4. đánh giá **tính công bằng** giữa các nhóm và **độ bền theo thời gian** giữa các khóa;
5. **giải thích** mô hình bằng SHAP (Lundberg & Lee, 2017) để tăng tính minh bạch;
6. phát triển một **hệ thống cảnh báo sớm hai tầng** có thể vận hành trong nhà trường, nối liền dự báo với hành động — **nhằm hỗ trợ quá trình can thiệp sớm đối với những sinh viên có nguy cơ cao** (Arnold & Pistilli, 2012).

Sáu nội dung trên có thể được nhóm lại thành **bốn đóng góp chính**, là cách chúng được trình bày ở mục 1.6 và mục 5.3: (i) **thiết kế dữ liệu chống rò rỉ theo chân trời thời gian** — tương ứng nội dung 1; (ii) **bằng chứng định lượng về rò rỉ** trên dữ liệu thật; (iii) **giao thức đánh giá đầy đủ** — gộp các nội dung 2–5, vì cả bốn đều là những thành phần của cùng một khung đánh giá chứ không phải bốn đóng góp độc lập; và (iv) **chiến lược triển khai nhiều tầng** — tương ứng nội dung 6.

## 2.10 Khung khái niệm của luận văn (Conceptual Framework)

Bốn đóng góp nêu trên không rời rạc mà hợp thành một quy trình thống nhất, đi từ dữ liệu thô đến hành động can thiệp. Hình 2.3 tóm tắt khung khái niệm đó: hồ sơ sinh viên được giới hạn trong *cửa sổ quan sát* (đến học kỳ mốc *h*), chuyển thành đặc trưng theo chân trời thời gian (hiện thực hóa nguyên lý landmarking), đưa vào mô hình LightGBM, rồi lần lượt được kiểm chứng qua nested cross-validation, hiệu chỉnh xác suất, đánh giá công bằng và giải thích bằng SHAP, trước khi kết tinh thành hệ thống cảnh báo sớm hai tầng dẫn tới can thiệp. Khung này vừa khép lại phần tổng quan (mỗi khối tương ứng một mục ở Chương 2), vừa là bản thiết kế trực tiếp cho phương pháp nghiên cứu trình bày ở Chương 3.

**Hình 2.3.** Khung khái niệm của luận văn — từ dữ liệu sinh viên tới can thiệp, làm cầu nối giữa tổng quan tài liệu (Chương 2) và phương pháp (Chương 3). *(Nguồn: tác giả; tệp `03_KetQua_Hinh/fig_2_9_conceptual_framework.png`.)*

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- **Điền số liệu thật** vào `[XX]`, `[20XX]`: cần một bảng/phụ lục liệt kê các công trình đã tổng quan để bảo vệ được các cụm "phần lớn", "một số ít", "một tỷ lệ đáng kể" khi phản biện.
- Cân nhắc chèn 1–2 câu **bằng chứng rò rỉ từ chính dữ liệu** (AUC HK1-2 bị thổi phồng ~0.95, xấp xỉ mức mà chỉ riêng cột GPA4_2 đạt được) để đoạn hạn chế (1) "có răng".
- Sau khi viết xong 2.1–2.8, đối chiếu: mỗi hạn chế (1)–(4) đã được đặt nền ở mục nào? (leakage→2.4; nested CV→mục phương pháp đánh giá; calibration/fairness→2.5–2.6; hành động→2.8).
- Kiểm tra đã trả lời trước câu hỏi phản biện "tại sao không dùng dữ liệu cuối khóa" chưa.
