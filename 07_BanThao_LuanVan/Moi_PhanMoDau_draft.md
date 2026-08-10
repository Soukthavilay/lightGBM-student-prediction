# PHẦN MỞ ĐẦU

> **BẢN THẢO MỚI (đề án) — v0 · 2026-08-10.** Viết theo cấu trúc template `Đề-Án-NguyenThiPhucLoan`. Trọng tâm: **LightGBM** (XGBoost, CatBoost dùng để so sánh); mục tiêu kép **dự báo** và **phát hiện nguyên nhân** bỏ học.

## 1. Lý do chọn đề tài

Bỏ học là một trong những vấn đề dai dẳng của giáo dục đại học. Mỗi năm, một bộ phận sinh viên rời giảng đường trước khi hoàn thành chương trình học. Với bản thân sinh viên, đó là thời gian và chi phí đã bỏ ra nhưng không đổi được tấm bằng. Với nhà trường và xã hội, đó là nguồn lực đào tạo đã đầu tư nhưng không chuyển hóa thành nhân lực có trình độ. Vì vậy, giảm tỷ lệ bỏ học là một mục tiêu quan trọng của mọi cơ sở đào tạo.

`TODO` — bổ sung số liệu có nguồn về tỷ lệ bỏ học đại học tại Việt Nam và trên thế giới, kèm trích dẫn chính thức. Không được ước lượng nếu chưa có nguồn.

Điều đáng chú ý là trong nhiều trường hợp, tổn thất này có thể phòng tránh được. Quyết định rời trường hiếm khi xảy ra đột ngột; nó thường là điểm cuối của một quá trình tích lũy, và quá trình đó để lại dấu vết ngay trong hồ sơ học vụ mà mọi trường đại học đều đang lưu trữ. Nếu phát hiện được sinh viên có nguy cơ đủ sớm, nhà trường còn kịp hỗ trợ trước khi quyết định rời trường trở nên không thể đảo ngược.

Học máy mở ra một hướng giải quyết cho bài toán này. Với dữ liệu học vụ ở dạng bảng, các thuật toán cây tăng cường gradient (gradient boosting) như XGBoost, LightGBM và CatBoost thường cho hiệu năng cao và chi phí tính toán hợp lý. Trong đó, **LightGBM** nổi bật ở tốc độ huấn luyện, khả năng xử lý trực tiếp giá trị thiếu và biến hạng mục, nên phù hợp với đặc thù dữ liệu học vụ. Đây là lý do đề tài chọn LightGBM làm mô hình trọng tâm.

Tuy nhiên, một mô hình chỉ đưa ra con số nguy cơ là chưa đủ để hành động. Người cố vấn học tập còn cần biết **vì sao** một sinh viên bị xếp vào nhóm nguy cơ, tức những yếu tố nào đang đẩy nguy cơ đó lên. Vì vậy, bên cạnh việc dự báo, đề tài sử dụng kỹ thuật giải thích mô hình SHAP để **phát hiện các yếu tố nguy cơ** liên quan tới bỏ học. Sự kết hợp giữa *dự báo* và *phát hiện nguyên nhân* chính là định hướng của đề tài.

## 2. Tổng quan tình hình nghiên cứu

Trên thế giới, dự báo bỏ học là một chủ đề được quan tâm trong lĩnh vực khai phá dữ liệu giáo dục (Educational Data Mining) và học phân tích (Learning Analytics). Nhiều nghiên cứu đã sử dụng các thuật toán học máy để dự báo nguy cơ bỏ học từ hồ sơ học vụ, nhật ký hệ thống quản lý học tập hoặc dữ liệu khảo sát, và thường báo cáo các chỉ số phân biệt như AUC, F1 ở mức cao.

Trong nhóm phương pháp được sử dụng, các mô hình cây tăng cường gradient chiếm ưu thế trên dữ liệu dạng bảng. XGBoost, LightGBM và CatBoost liên tục được ghi nhận là những lựa chọn hiệu quả, vừa đạt độ chính xác cao vừa dễ triển khai. Song song đó, xu hướng gần đây nhấn mạnh yêu cầu **giải thích được** mô hình: thay vì chỉ dự báo, các nghiên cứu bắt đầu sử dụng những kỹ thuật như SHAP để làm rõ đóng góp của từng đặc trưng, phục vụ cho việc ra quyết định của con người.

Tại Việt Nam, số công trình khai thác dữ liệu học vụ để dự báo bỏ học còn hạn chế, và phần lớn dừng ở mức phân loại mà chưa đi sâu vào giải thích nguyên nhân. Đây là khoảng trống mà đề tài hướng tới: áp dụng mô hình LightGBM trên một bộ dữ liệu chuẩn được cộng đồng thừa nhận, kết hợp giải thích bằng SHAP, rồi kiểm chứng khả năng áp dụng trên dữ liệu thực tế của một trường đại học Việt Nam.

## 3. Mục tiêu nghiên cứu

**Mục tiêu tổng quát:** xây dựng và đánh giá một mô hình học máy dựa trên LightGBM để **dự báo nguy cơ bỏ học** của sinh viên, đồng thời **phát hiện các yếu tố nguy cơ** liên quan bằng phương pháp giải thích mô hình.

**Mục tiêu cụ thể:**

- Xây dựng mô hình LightGBM dự báo bỏ học trên bộ dữ liệu chuẩn.
- So sánh LightGBM với XGBoost, CatBoost và một số mô hình nền (hồi quy logistic, rừng ngẫu nhiên) dưới cùng một giao thức đánh giá.
- Sử dụng SHAP để xác định và diễn giải những yếu tố nguy cơ có ảnh hưởng lớn nhất tới nguy cơ bỏ học.
- Kiểm chứng khả năng áp dụng của quy trình trên dữ liệu học vụ thực tế của một trường đại học Việt Nam.
- Đề xuất hướng sử dụng kết quả dự báo cho việc cảnh báo và hỗ trợ sinh viên có nguy cơ cao.

## 4. Đối tượng và phạm vi nghiên cứu

**Đối tượng nghiên cứu:** nguy cơ bỏ học của sinh viên đại học và các yếu tố liên quan.

**Phạm vi dữ liệu:** nghiên cứu sử dụng hai bộ dữ liệu. Thứ nhất là **bộ dữ liệu chuẩn quốc tế** (bộ "Predict Students' Dropout and Academic Success" được công bố công khai) dùng để xây dựng và đánh giá mô hình. Thứ hai là **dữ liệu học vụ thực tế** của một trường đại học Việt Nam, dùng để kiểm chứng khả năng áp dụng của quy trình. 🔵 *(Cách phối hợp hai bộ dữ liệu sẽ được chốt sau khi trao đổi với giảng viên hướng dẫn — xem ghi chú cuối.)*

**Phạm vi mô hình:** LightGBM là mô hình trọng tâm; XGBoost và CatBoost được dùng để so sánh, nhằm định vị LightGBM trong nhóm thuật toán cây tăng cường gradient.

**Phạm vi dữ liệu đầu vào:** nghiên cứu chỉ sử dụng dữ liệu dạng bảng (nhân khẩu, kết quả học tập, thông tin học vụ). Đề tài không sử dụng dữ liệu tâm lý hay nhật ký hệ thống quản lý học tập.

## 5. Nội dung nghiên cứu

Đề tài tập trung vào các nội dung sau:

- Tổng quan cơ sở lý thuyết: bài toán bỏ học, học kết hợp (Ensemble learning), các thuật toán XGBoost, LightGBM, CatBoost và phương pháp giải thích SHAP.
- Thu thập, mô tả và phân tích khám phá (EDA) hai bộ dữ liệu nghiên cứu.
- Tiền xử lý dữ liệu: làm sạch, xây dựng đặc trưng, xử lý mất cân bằng lớp, chia tập huấn luyện/kiểm định/kiểm tra.
- Huấn luyện mô hình LightGBM và so sánh với XGBoost, CatBoost cùng các mô hình nền.
- Đánh giá hiệu năng bằng các chỉ số phù hợp cho bài toán phân loại mất cân bằng.
- Giải thích mô hình bằng SHAP để phát hiện các yếu tố nguy cơ.
- Áp dụng quy trình cho dữ liệu thực tế của trường đại học Việt Nam và bàn luận khả năng triển khai cảnh báo.

## 6. Phương pháp luận và phương pháp nghiên cứu

Đề tài được thực hiện trên cơ sở kết hợp giữa lý thuyết và thực nghiệm, theo quy trình: nghiên cứu tài liệu, phân tích dữ liệu, xây dựng mô hình học máy, đánh giá hiệu năng và xác định các đặc trưng quan trọng. Các bước cụ thể gồm:

a) Tìm hiểu về bài toán bỏ học và khảo sát hiện trạng các mô hình học máy phổ biến áp dụng cho dữ liệu giáo dục, từ đó xác định các nhóm đặc trưng có ý nghĩa dự báo.

b) Khai thác nguyên lý hoạt động của các thuật toán trọng tâm, đặc biệt là LightGBM, bao gồm cơ chế huấn luyện, cách tối ưu tham số và cách áp dụng vào bài toán dự báo bỏ học.

c) Ở giai đoạn tiền huấn luyện, vận dụng phân tích khám phá dữ liệu (EDA) để mô tả, làm sạch và trực quan hóa đặc điểm của dữ liệu học vụ.

d) Mô hình hóa dữ liệu, đối chiếu hiệu năng của LightGBM với XGBoost và CatBoost trên cùng một tập dữ liệu và cùng một giao thức đánh giá, để định vị vai trò của LightGBM.

Sau khi có mô hình đã huấn luyện, đề tài áp dụng kỹ thuật SHAP (Shapley Additive exPlanations) — một phương pháp giải thích cho mô hình học máy — nhằm xem xét và đánh giá đóng góp của từng đặc trưng vào dự báo, qua đó phát hiện các yếu tố nguy cơ liên quan tới bỏ học.

## 7. Ý nghĩa khoa học và thực tiễn của đề tài

**Về mặt khoa học.** Đề tài góp phần làm rõ giá trị của các thuật toán học kết hợp (đặc biệt là LightGBM, bên cạnh XGBoost và CatBoost) trong bài toán dự báo bỏ học trên dữ liệu học vụ dạng bảng. Việc kết hợp mô hình dự báo với kỹ thuật giải thích SHAP mang lại một góc nhìn minh bạch: nghiên cứu không dừng ở việc dự báo mà còn giải thích được mức độ ảnh hưởng của từng đặc trưng, mở rộng khả năng ứng dụng trí tuệ nhân tạo có giải thích (XAI) trong giáo dục. Kết quả cũng có thể làm tài liệu tham khảo cho các nghiên cứu tiếp theo về học máy ứng dụng trong lĩnh vực giáo dục.

**Về mặt thực tiễn.** Đề tài có giá trị hỗ trợ các cơ sở đào tạo trong việc phát hiện sớm sinh viên có nguy cơ bỏ học. Mô hình có thể trở thành công cụ hỗ trợ cho cố vấn học tập trong việc rà soát, xác định nhóm cần quan tâm và phân bổ nguồn lực hỗ trợ hợp lý. Ngoài ra, kết quả giải thích bằng SHAP giúp nhà trường hiểu rõ hơn các yếu tố nguy cơ, từ đó thiết kế biện pháp can thiệp phù hợp với từng nhóm sinh viên.

## 8. Kết cấu của đề án thạc sĩ

Đề án được chia thành ba chương:

**Chương 1. Cơ sở lý thuyết.** Trình bày nền tảng lý thuyết của đề tài. Mở đầu là tổng quan về bài toán bỏ học của sinh viên và ứng dụng của trí tuệ nhân tạo. Tiếp đó, chương giới thiệu học kết hợp (Ensemble learning), nhấn mạnh kỹ thuật gradient boosting và các thuật toán tiêu biểu XGBoost, LightGBM, CatBoost, kèm phân tích khác biệt giữa chúng. Chương cũng trình bày phương pháp giải thích mô hình SHAP và các tiêu chí đánh giá mô hình, tạo nền tảng cho các chương sau.

**Chương 2. Dữ liệu và phát biểu bài toán.** Phát biểu rõ bài toán dự báo bỏ học và phân tích yếu tố nguy cơ. Chương mô tả hai bộ dữ liệu nghiên cứu (bộ chuẩn quốc tế và dữ liệu thực tế của trường đại học Việt Nam), tiến hành phân tích khám phá dữ liệu, và trình bày các bước chuẩn bị cho quy trình thực nghiệm.

**Chương 3. Thiết kế mô hình và cài đặt thực nghiệm.** Trình bày thiết kế mô hình và thiết lập tham số, kết quả huấn luyện và so sánh LightGBM với XGBoost, CatBoost cùng các mô hình nền. Sau bước đánh giá hiệu năng, kết quả được giải thích bằng SHAP để phát hiện các yếu tố nguy cơ. Chương cũng bàn về khả năng áp dụng cho dữ liệu thực tế và hướng sử dụng cho cảnh báo sớm.

---

### 📌 Ghi chú cho tác giả (không đưa vào bản in)
- 🔵 **Chờ thầy chốt:** cách phối hợp hai bộ dữ liệu (Kaggle = xây dựng/đánh giá; Testkhoa = kiểm chứng, mỗi bộ có train/test riêng). Ảnh hưởng câu chữ ở mục 4 và Chương 2–3.
- `TODO` số liệu tỷ lệ bỏ học có nguồn ở mục 1.
- Chưa chèn số kết quả (AUC…) vào mục 7 — chờ chạy thực nghiệm trên khung mới; **không bịa số như template (96%)**.
- Thuật ngữ dùng thống nhất với bản đã sửa: "cây tăng cường gradient (gradient boosting)", "yếu tố nguy cơ", "độ chính xác dương tính" (precision) khi vào phần chỉ số.
