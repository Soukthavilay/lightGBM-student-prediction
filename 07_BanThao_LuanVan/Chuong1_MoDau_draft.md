# Chương 1. Mở đầu

> **BẢN THẢO (DRAFT v1).** Chương này chỉ trả lời ba câu: *làm gì, vì sao làm, và cuốn luận văn dẫn người đọc đi đâu.* Không tổng quan tài liệu (Chương 2) và không trình bày chi tiết phương pháp (Chương 3).

---

## 1.1 Lý do chọn đề tài

Mỗi năm, một bộ phận sinh viên rời giảng đường trước khi hoàn thành chương trình. Với các em, đó là thời gian và chi phí đã bỏ ra mà không thu được bằng cấp; với nhà trường và xã hội, đó là nguồn lực đào tạo đã đầu tư nhưng không kết thành nhân lực có trình độ. Chương 2 sẽ phân tích hệ quả này cùng các hướng nghiên cứu đã có; ở đây chỉ cần ghi nhận rằng đó là một tổn thất đủ lớn để đáng được can thiệp.

`TODO` — bổ sung số liệu có nguồn về tỷ lệ bỏ học bậc đại học tại Việt Nam và trên thế giới, kèm trích dẫn chính thức. **Không được ước lượng nếu chưa tìm được nguồn.**

Điều đáng chú ý là tổn thất ấy **không phải lúc nào cũng không thể tránh được**. Quyết định rời trường hiếm khi xảy ra đột ngột; nó thường là điểm cuối của một quá trình tích lũy để lại dấu vết trong chính hồ sơ học vụ mà mọi trường đại học đều đang lưu trữ. Nghĩa là về nguyên tắc, **tồn tại một khoảng thời gian mà nhà trường vẫn còn cơ hội hành động** — và bài toán đặt ra là làm sao nhận ra được ai đang ở trong khoảng thời gian đó.

Học máy hứa hẹn giải quyết bài toán này, và tài liệu hiện có không thiếu những mô hình báo cáo độ chính xác rất cao. Nhưng khi đọc kỹ, một vấn đề phương pháp nổi lên: nhiều mô hình trong số đó sử dụng những thông tin **chưa tồn tại tại thời điểm cần đưa ra cảnh báo** — kết quả học tập của các học kỳ sau, hay trạng thái đăng ký cuối khóa. Khi đó, con số ấn tượng không phản ánh năng lực dự báo mà phản ánh việc mô hình đã "nhìn thấy" hệ quả của chính điều cần dự báo. Một mô hình như vậy **không thể dùng để cảnh báo sớm**, dù chỉ số đánh giá rất đẹp — bởi vào ngày cần cảnh báo, những thông tin làm nên con số ấy vẫn chưa có.

Nghịch lý ở đây là: càng dùng dữ liệu muộn, chỉ số càng đẹp, nhưng cảnh báo càng vô dụng. Vì vậy, vấn đề cần giải quyết trước tiên không phải là làm cho mô hình chính xác hơn, mà là **làm cho con số báo cáo phản ánh đúng những gì mô hình thực sự biết tại thời điểm dự báo** — và đó cũng chính là khoảng trống mà luận văn này hướng tới.

## 1.2 Mục tiêu nghiên cứu

**Mục tiêu tổng quát:** xây dựng và đánh giá một mô hình cảnh báo sớm nguy cơ bỏ học cho sinh viên đại học Việt Nam, trong đó kết quả báo cáo phản ánh đúng năng lực dự báo ở điều kiện triển khai thực tế.

**Mục tiêu cụ thể:**

1. Thiết kế quy trình xây dựng dữ liệu và nhãn **theo chân trời thời gian**, bảo đảm mô hình chỉ sử dụng thông tin khả dụng tại thời điểm dự báo.
2. Chứng minh bằng số rằng thiết kế không kiểm soát thời điểm dự báo dẫn tới kết quả bị thổi phồng.
3. So sánh các thuật toán phân loại dưới cùng một giao thức đánh giá nghiêm ngặt, kèm khoảng tin cậy và kiểm định ý nghĩa thống kê.
4. Đánh giá **độ tin cậy của xác suất** dự báo và **lợi ích quyết định** khi dùng mô hình để phân bổ nguồn lực hỗ trợ.
5. Kiểm tra **độ bền theo thời gian**, **tính công bằng** giữa các nhóm sinh viên, và **độ ổn định của giải thích** mô hình.
6. Đề xuất một hệ thống cảnh báo sớm nhiều tầng có thể vận hành trong điều kiện nguồn lực tư vấn hữu hạn.

## 1.3 Câu hỏi nghiên cứu

1. **Có thể dự báo nguy cơ bỏ học từ sớm hay không, và sớm tới mức nào?** Cụ thể: tại thời điểm kết thúc học kỳ 1 và học kỳ 2, mô hình phân biệt được nhóm nguy cơ ở mức nào?
2. **Kết quả đó có đáng tin cậy không?** Xác suất dự báo có được hiệu chỉnh tốt không, kết quả có bền khi chuyển khóa không, có chênh lệch giữa các nhóm sinh viên không, và các giải thích mô hình có ổn định không?
3. **Những yếu tố nào liên quan tới nguy cơ bỏ học**, và trong số đó yếu tố nào đủ ổn định để dùng làm cơ sở tư vấn?

## 1.4 Đối tượng và phạm vi nghiên cứu

**Đối tượng nghiên cứu:** nguy cơ bỏ học của sinh viên đại học trong những học kỳ đầu của chương trình đào tạo.

**Phạm vi dữ liệu:** hồ sơ học vụ của một trường đại học Việt Nam, gồm **7.514 sinh viên** thuộc hai khóa tuyển sinh 2020 và 2021 — hai khóa có đủ dữ liệu bốn học kỳ.

**Phạm vi thời điểm dự báo:** hai chân trời triển khai được là **cuối học kỳ 1** (7.367 sinh viên còn theo học) và **cuối học kỳ 1-2** (7.034 sinh viên). Chân trời bốn học kỳ chỉ được dùng làm tham chiếu để minh họa hiện tượng rò rỉ dữ liệu.

**Phạm vi dữ liệu đầu vào:** nghiên cứu chỉ sử dụng **hồ sơ học vụ hành chính** — thông tin nhân khẩu, điểm tuyển sinh và kết quả học tập theo từng học kỳ. Nghiên cứu **không** sử dụng dữ liệu tâm lý, hoàn cảnh kinh tế gia đình hay nhật ký hệ thống quản lý học tập. Lựa chọn này đánh đổi chiều sâu giải thích lấy **khả năng áp dụng rộng**, vì mọi trường đại học đều có sẵn loại dữ liệu này.

**Giới hạn phạm vi kết luận:** luận văn xây dựng và đánh giá hệ thống tới **khâu quyết định** — lựa chọn ngưỡng vận hành và phân tích lợi ích ròng. Nghiên cứu **không tiến hành thử nghiệm can thiệp**, do đó **không đưa ra kết luận nào về hiệu quả giữ chân sinh viên** trên thực tế.

## 1.5 Phương pháp nghiên cứu

Nghiên cứu sử dụng thiết kế **hồi cứu, quan sát** trên dữ liệu học vụ đã có. Quy trình gồm bảy bước chính, trình bày chi tiết ở Chương 3:

1. Chuẩn bị dữ liệu và xác định **quần thể, nhãn theo chân trời thời gian** — chỉ giữ những sinh viên còn theo học tại thời điểm dự báo, với nhãn là "bỏ học *sau* thời điểm đó".
2. Xây dựng đặc trưng **chỉ từ các học kỳ tính đến chân trời**, giữ giá trị thiếu để phân biệt "không có dữ liệu" với "kết quả bằng không".
3. So sánh **ba thuật toán** — hồi quy logistic, rừng ngẫu nhiên và LightGBM — dưới cùng một giao thức, với mọi bước tiền xử lý đặt trong từng fold.
4. Đánh giá bằng **kiểm định chéo phân tầng lặp lại** kèm khoảng tin cậy bootstrap, kiểm định DeLong và hiệu chỉnh đa so sánh Holm.
5. Đánh giá ảnh hưởng của tinh chỉnh siêu tham số bằng **kiểm định chéo lồng nhau**.
6. **Hiệu chỉnh xác suất** và phân tích **đường cong quyết định**.
7. Kiểm định **độ bền theo thời gian**, **tính công bằng** theo nhóm, và **độ ổn định của giải thích SHAP**.

Toàn bộ phân tích được thực hiện bằng Python với hằng số ngẫu nhiên cố định, và mọi bảng kết quả trong luận văn đều được sinh tự động từ một quy trình tái lập được.

## 1.6 Đóng góp của luận văn

Đóng góp của luận văn nằm ở tầng **thiết kế dữ liệu, quy trình đánh giá và chiến lược triển khai**, không phải ở tầng thuật toán:

1. **Quy trình xây dựng dữ liệu chống rò rỉ theo chân trời thời gian**, kết hợp giới hạn quần thể với giới hạn đặc trưng.
2. **Bằng chứng định lượng về rò rỉ** trên dữ liệu thật, tái lập được từ tệp kết quả.
3. **Giao thức đánh giá đầy đủ**, kết hợp một cách hệ thống khoảng tin cậy, kiểm định ý nghĩa, kiểm định chéo lồng nhau, hiệu chỉnh xác suất, đường cong quyết định, kiểm định thời gian, phân tích công bằng và độ ổn định của giải thích.
4. **Hệ thống cảnh báo nhiều tầng** gắn mỗi mức rủi ro với một hình thức can thiệp và mức chi phí tương ứng, kèm dải ngưỡng để mỗi đơn vị tự chọn ngưỡng vận hành.

Luận văn **không** tuyên bố phát minh thuật toán mới, **không** khẳng định một thuật toán vượt trội tuyệt đối, và **không** rút ra kết luận nhân quả từ các phân tích giải thích mô hình.

## 1.7 Cấu trúc luận văn

Luận văn gồm năm chương:

- **Chương 1 — Mở đầu:** đặt vấn đề, mục tiêu, câu hỏi, phạm vi và đóng góp.
- **Chương 2 — Tổng quan tài liệu:** đi từ bài toán dự báo bỏ học và lĩnh vực khai phá dữ liệu giáo dục, tới lựa chọn mô hình, rồi tới trục trung tâm là **rò rỉ dữ liệu và nguyên lý landmarking**; từ đó lần lượt đặt các yêu cầu về hiệu chỉnh xác suất, tính công bằng, khả năng giải thích và hệ thống cảnh báo, kết lại thành khoảng trống nghiên cứu và khung khái niệm.
- **Chương 3 — Phương pháp nghiên cứu:** dữ liệu, định nghĩa quần thể và nhãn theo chân trời, xây dựng đặc trưng, mô hình và toàn bộ giao thức đánh giá, kèm thông tin tái lập.
- **Chương 4 — Kết quả nghiên cứu:** trình bày kết quả theo đúng trình tự giao thức, kèm bằng chứng định lượng về rò rỉ và hệ thống cảnh báo hai tầng.
- **Chương 5 — Bàn luận và kết luận:** diễn giải kết quả trong bối cảnh tài liệu, nêu đóng góp, hạn chế và hướng nghiên cứu tiếp theo.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- `TODO` duy nhất của chương: số liệu tỷ lệ bỏ học có nguồn (mục 1.1). Nếu không tìm được nguồn Việt Nam đáng tin cậy, diễn đạt định tính và ghi rõ giới hạn.
- Kiểm tra chéo: 1.3 (ba câu hỏi) phải khớp với 5.1 (ba câu trả lời); 1.6 phải khớp 5.3 và `08_ContributionBoundary.md`; 1.4 phải khớp 3.2 và 3.3.
- Chương này **không được chứa số liệu kết quả** (AUC, Brier…) — chỉ nêu quy mô dữ liệu và phạm vi.
- Tránh trùng lặp với Chương 2: mục 1.1 chỉ nêu vấn đề, **không** tổng quan tài liệu.
