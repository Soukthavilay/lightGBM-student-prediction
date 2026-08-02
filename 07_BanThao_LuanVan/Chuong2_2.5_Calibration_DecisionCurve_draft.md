# 2.5 Hiệu chỉnh xác suất và phân tích đường cong quyết định

> **BẢN THẢO (DRAFT v1)** — Trả lời câu hỏi: *vì sao đánh giá một mô hình cảnh báo sớm không thể dừng ở độ chính xác, mà phải xét tới độ tin cậy của xác suất và lợi ích của quyết định?*
> ⚠️ Mục này là **tổng quan tài liệu** — mọi số liệu thực nghiệm của luận văn thuộc Chương 4, ở đây chỉ dẫn chiếu.

## 2.5.1 Phân biệt tốt không đồng nghĩa với xác suất đáng tin

Các chỉ số phổ biến nhất trong dự báo bỏ học — AUC, F1, độ chính xác — đều đo **khả năng phân biệt** (discrimination): mô hình có xếp sinh viên nguy cơ cao lên trên sinh viên nguy cơ thấp hay không. Tuy nhiên, AUC chỉ phụ thuộc vào **thứ tự** của các điểm số, không phụ thuộc vào **giá trị tuyệt đối** của chúng. Hai mô hình có cùng AUC có thể đưa ra những xác suất rất khác nhau: một mô hình nói "nguy cơ 12%" và một mô hình nói "nguy cơ 45%" cho cùng một sinh viên vẫn có thể xếp hạng giống hệt nhau.

Sự phân biệt này trở nên quan trọng ngay khi xác suất được dùng để **ra quyết định**. Nếu nhà trường muốn đặt quy tắc "liên hệ cố vấn học tập khi nguy cơ vượt 20%", thì con số 20% phải có ý nghĩa thực: trong nhóm sinh viên được mô hình gán nguy cơ 20%, phải có khoảng 20% thực sự bỏ học. Tính chất này gọi là **hiệu chỉnh** (calibration), và nó độc lập với khả năng phân biệt.

## 2.5.2 Các phương pháp hiệu chỉnh

Hai phương pháp hậu xử lý được dùng rộng rãi. **Hiệu chỉnh Platt** (sigmoid) khớp một hàm logistic từ điểm số của mô hình sang xác suất, phù hợp khi độ méo có dạng sigmoid và dữ liệu hiệu chỉnh ít. **Hồi quy đẳng hướng** (isotonic regression), do Zadrozny & Elkan (2002) đưa vào bài toán này, là phương pháp phi tham số tìm hàm đơn điệu từng khúc tối ưu; linh hoạt hơn nhưng cần nhiều dữ liệu hơn và có nguy cơ quá khớp ở mẫu nhỏ.

Điểm đặc biệt liên quan tới luận văn nằm ở khảo sát của **Niculescu-Mizil & Caruana (2005)**: các phương pháp lề tối đa, trong đó có **cây tăng cường** (boosted trees), có xu hướng đẩy khối xác suất ra xa hai đầu 0 và 1, tạo ra méo dạng sigmoid đặc trưng. Nói cách khác, **chính họ mô hình mà luận văn sử dụng (LightGBM) là họ mô hình được biết là hiệu chỉnh kém nếu không xử lý** — đây là lý do trực tiếp để đưa bước hiệu chỉnh vào quy trình, chứ không phải một thao tác thêm cho đủ.

Vấn đề này không chỉ tồn tại ở các mô hình cổ điển. **Guo và cộng sự (2017)** cho thấy các mạng nơ-ron hiện đại, dù chính xác hơn thế hệ trước, lại **hiệu chỉnh kém hơn**, và đề xuất temperature scaling như một giải pháp đơn giản. Kết luận chung: độ chính xác tăng không tự động kéo theo xác suất đáng tin.

## 2.5.3 Đo lường chất lượng hiệu chỉnh

- **Brier score** — sai số bình phương trung bình giữa xác suất dự báo và nhãn thực; là một *proper scoring rule*, đo đồng thời cả khả năng phân biệt lẫn độ hiệu chỉnh. Giá trị càng nhỏ càng tốt, nhưng phụ thuộc tỷ lệ lớp nên **không so sánh trực tiếp được giữa các bộ dữ liệu có tỷ lệ khác nhau**.
- **Biểu đồ độ tin cậy** (reliability diagram) — vẽ tần suất thực tế theo xác suất dự báo; trực quan nhưng phụ thuộc cách chia bin.
- **ECE** (Expected Calibration Error) — trung bình có trọng số của chênh lệch |tần suất thực − xác suất dự báo| trên từng bin.

ECE cần được diễn giải thận trọng vì ba lý do. Thứ nhất, giá trị phụ thuộc **số bin và cách chia bin** (đều theo độ rộng hay theo phân vị); các lựa chọn khác nhau cho ra con số khác nhau trên cùng dữ liệu. Thứ hai, ECE **không phải proper scoring rule** — một mô hình luôn dự báo tỷ lệ nền có thể đạt ECE rất thấp dù vô dụng. Thứ ba, ở cỡ mẫu hữu hạn, ECE có một **"sàn nhiễu"**: ngay cả một mô hình hiệu chỉnh hoàn hảo cũng cho ECE dương do dao động lấy mẫu. Vì vậy, một giá trị ECE rất nhỏ chỉ nên được diễn giải là *"không phát hiện được sai lệch hiệu chỉnh"*, **không phải** *"hiệu chỉnh gần như hoàn hảo"*.

## 2.5.4 Từ xác suất tới quyết định: đường cong quyết định

Ngay cả khi xác suất đã đáng tin, vẫn còn một câu hỏi: **dùng mô hình có lợi hơn không dùng hay không?** Phân tích đường cong quyết định (Decision Curve Analysis) của **Vickers & Elkin (2006)** trả lời câu hỏi này bằng khái niệm **lợi ích ròng** (net benefit):

$$NB = \frac{TP}{n} - \frac{FP}{n}\cdot\frac{p_t}{1-p_t}$$

trong đó $p_t$ là **ngưỡng xác suất** mà tại đó người ra quyết định thấy việc can thiệp là đáng. Khi một giá trị $p_t$ cụ thể được chọn để hệ thống vận hành, luận văn gọi đó là **ngưỡng vận hành** (operating point) — thuật ngữ này được dùng thống nhất từ đây tới hết Chương 5. Ý tưởng cốt lõi: $p_t$ không phải tham số kỹ thuật mà là **phát biểu về sự đánh đổi chi phí** — chọn $p_t = 0{,}2$ tương đương nói "tôi sẵn sàng can thiệp 4 trường hợp không cần thiết để bắt được 1 trường hợp thật".

Đường cong quyết định vẽ NB của mô hình theo dải $p_t$, so với hai chiến lược tham chiếu: **can thiệp tất cả** và **không can thiệp ai**. Mô hình chỉ thực sự hữu ích trong dải ngưỡng mà đường của nó nằm trên cả hai đường tham chiếu.

Cách tiếp cận này đặc biệt phù hợp với bối cảnh giáo dục, nơi nguồn lực cố vấn học tập là hữu hạn: câu hỏi thực tế không phải "mô hình chính xác bao nhiêu phần trăm" mà "với năng lực tiếp cận *k* sinh viên mỗi học kỳ, dùng mô hình có giúp tiếp cận đúng người hơn cách làm hiện tại không". Ngưỡng $p_t$ do đó trở thành cầu nối giữa mô hình thống kê và chính sách hỗ trợ sinh viên — ý tưởng sẽ được khai thác trong thiết kế cảnh báo hai tầng ở mục 2.8.

## 2.5.5 Khoảng trống trong tài liệu dự báo bỏ học

Mặc dù hiệu chỉnh và lợi ích quyết định là điều kiện cần để một mô hình rủi ro dùng được trong thực tế, **trong số các công trình được tổng hợp ở Bảng 2.1** (bảng khảo sát tài liệu), chỉ một số rất ít có đánh giá hiệu chỉnh xác suất, và hầu như không công trình nào phân tích lợi ích ròng của quyết định; đại đa số **chỉ báo cáo các chỉ số phân biệt** (AUC, F1) — xem cột *Cal* của bảng. Hệ quả là nhiều mô hình được công bố là "chính xác" nhưng chưa từng được kiểm chứng rằng xác suất của chúng có thể dùng để quyết định ai cần hỗ trợ trước.

## 2.5.6 Chuyển tiếp

Tuy nhiên, một xác suất được hiệu chỉnh tốt **trên tổng thể** vẫn có thể sai lệch một cách hệ thống **giữa các nhóm** sinh viên khác nhau — theo giới tính, khu vực hay dân tộc. Vì đây là mô hình dùng để phân bổ nguồn lực hỗ trợ, chênh lệch như vậy mang hệ quả đạo đức trực tiếp. Do đó, sau độ tin cậy tổng thể, cần xét tới tính công bằng.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- **Số liệu cho Chương 4** (đã có sẵn, `calibration.pkl`, n = 7.034, HK1-2): chưa hiệu chỉnh Brier 0,0415 / ECE 0,0339 · isotonic 0,0363 / 0,0047 · sigmoid 0,0374 / 0,0059. Decision curve (`decision_curve.csv`, 60 ngưỡng 0,01–0,60).
- ⚠️ **Cảnh báo diễn giải cho Chương 4:** ECE isotonic = 0,0047 **nằm dưới sàn nhiễu** (~0,005–0,01 ở cỡ mẫu này, theo ghi chú trong `expected_calibration_error`). Phải viết *"không phát hiện sai lệch hiệu chỉnh"*, **tuyệt đối không viết** *"hiệu chỉnh gần hoàn hảo"*.
- Cân nhắc thêm 1 câu về **decomposition của Brier** (reliability–resolution–uncertainty) nếu hội đồng có người sâu về thống kê.
- Kiểm tra công thức LaTeX render đúng trong bản Word cuối (hoặc chuyển thành ảnh công thức).
- Đối chiếu ký hiệu $p_t$ với ký hiệu dùng ở 2.8 và Chương 3 cho thống nhất.
