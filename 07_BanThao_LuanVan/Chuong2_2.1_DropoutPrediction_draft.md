# 2.1 Dự báo sinh viên bỏ học

> **BẢN THẢO (DRAFT v1)** — Mục mở đầu Chương 2: xác định bài toán, vì sao nó đáng nghiên cứu, và các hướng tiếp cận đã có. Viết **sau cùng** để bảo đảm dẫn đúng vào mạch của cả chương.
> ⚠️ Các số liệu vĩ mô (tỷ lệ bỏ học quốc gia/quốc tế) chưa có nguồn xác minh → đánh dấu `TODO`, không được viết ước lượng.

## 2.1.1 Bài toán và ý nghĩa

Bỏ học ở bậc đại học là việc sinh viên rời khỏi chương trình đào tạo trước khi hoàn thành. Hệ quả của nó trải trên ba cấp độ. Với **cá nhân**, đó là chi phí thời gian và tài chính đã bỏ ra mà không thu được bằng cấp, kèm theo tác động tâm lý và cơ hội nghề nghiệp bị thu hẹp. Với **nhà trường**, tỷ lệ bỏ học ảnh hưởng tới nguồn thu, chỉ số kiểm định chất lượng và uy tín. Với **xã hội**, đó là sự lãng phí đầu tư công vào giáo dục và tổn thất nguồn nhân lực đã qua đào tạo một phần.

`TODO` — bổ sung số liệu có nguồn: tỷ lệ bỏ học bậc đại học (quốc tế và Việt Nam), kèm trích dẫn cơ quan thống kê hoặc báo cáo chính thức.

Điểm khiến bài toán này đáng được tiếp cận bằng dữ liệu là: **bỏ học hiếm khi là một sự kiện đột ngột**. Trong phần lớn trường hợp, nó là kết cục của một quá trình tích lũy — kết quả học tập sa sút, số tín chỉ đạt giảm dần, cảnh báo học vụ lặp lại — và quá trình đó để lại dấu vết trong hồ sơ học vụ của nhà trường. Nếu những dấu vết này được nhận diện đủ sớm, nhà trường có cơ hội can thiệp trước khi quyết định rời trường trở nên không thể đảo ngược.

## 2.1.2 Các hướng tiếp cận

Tài liệu về dự báo bỏ học có thể chia thành ba hướng chính.

**Hướng lý thuyết giáo dục** tập trung giải thích *vì sao* sinh viên rời trường. Hai mô hình nền tảng của hướng này là **mô hình hòa nhập của Tinto (1975)**, cho rằng quyết định rời trường phụ thuộc vào mức độ hòa nhập của sinh viên vào đời sống học thuật và xã hội của nhà trường, và **mô hình bỏ học của Bean (1980)**, vốn vay mượn khung lý thuyết về sự rời bỏ tổ chức trong nghiên cứu nhân sự và nhấn mạnh vai trò của các yếu tố ngoài trường học cùng ý định rời bỏ. Hướng này mạnh về khả năng diễn giải nhưng thường không nhằm mục tiêu dự báo ở cấp độ từng cá nhân.

**Hướng thống kê cổ điển** sử dụng hồi quy logistic hoặc phân tích sống còn để ước lượng nguy cơ. Ưu điểm là hệ số có ý nghĩa thống kê rõ ràng và có nền tảng suy luận vững; hạn chế là giả định về dạng hàm và khả năng nắm bắt tương tác phi tuyến còn giới hạn.

**Hướng học máy** coi bài toán như phân loại nhị phân trên dữ liệu hồ sơ sinh viên, sử dụng các mô hình cây, tổ hợp cây hoặc mạng nơ-ron. Đây là hướng chiếm ưu thế trong tài liệu gần đây, và cũng là hướng mà luận văn này theo đuổi.

Về **thời điểm dự báo**, các công trình khác nhau đáng kể: một số dự báo từ dữ liệu tiền nhập học, một số dự báo trong học kỳ dựa trên hoạt động trên hệ thống quản lý học tập, một số khác dự báo sau khi kết thúc một hoặc nhiều học kỳ. Sự khác biệt này quan trọng hơn vẻ ngoài của nó, vì thời điểm dự báo quyết định **thông tin nào được phép sử dụng** — chủ đề sẽ trở lại ở mục 2.4.

## 2.1.3 Hạn chế chung của tài liệu hiện có

Ba hạn chế khiến việc so sánh giữa các công trình trở nên khó khăn.

Thứ nhất, **định nghĩa "bỏ học" không thống nhất**: một số nghiên cứu gộp chung sinh viên chuyển trường, tạm nghỉ và thôi học hẳn; một số tách riêng. Cùng một bộ dữ liệu, hai định nghĩa khác nhau có thể cho ra tỷ lệ nền và kết quả rất khác nhau.

Thứ hai, **thời điểm dự báo ít khi được nêu tường minh**, khiến người đọc khó biết một chỉ số AUC cao là thành tựu của việc dự báo sớm hay chỉ là hệ quả của việc sử dụng dữ liệu muộn.

Thứ ba, **bối cảnh khác nhau** — hệ thống tín chỉ, quy chế học vụ, điều kiện kinh tế – xã hội — làm cho kết quả từ một quốc gia khó chuyển trực tiếp sang quốc gia khác.

## 2.1.4 Chuyển tiếp

Dự báo bỏ học không tồn tại biệt lập mà là một ứng dụng cụ thể của một lĩnh vực rộng hơn: khai phá dữ liệu giáo dục. Đặt bài toán trong khung này giúp thấy rõ bỏ học, giữ chân người học và thành công học tập là ba mặt của cùng một câu hỏi, đồng thời cho phép kế thừa các phương pháp và chuẩn mực đánh giá đã được lĩnh vực đó xây dựng.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- `TODO` số liệu tỷ lệ bỏ học có nguồn (2.1.1) — **không được ước lượng**; nếu không tìm được nguồn Việt Nam đáng tin, diễn đạt định tính.
- Nếu muốn nhắc mô hình lý thuyết về hòa nhập học thuật – xã hội ở 2.1.2, cần bổ sung trích dẫn gốc; hiện đang diễn đạt khái quát để tránh trích dẫn chưa xác minh.
- Kiểm tra: mục này **không** được lặp nội dung của 2.9 — ở đây chỉ nêu hạn chế *chung của lĩnh vực*, còn tổng hợp thành khoảng trống là việc của 2.9.
