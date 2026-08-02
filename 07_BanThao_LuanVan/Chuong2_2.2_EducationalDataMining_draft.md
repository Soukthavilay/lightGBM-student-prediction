# 2.2 Khai phá dữ liệu giáo dục

> **BẢN THẢO (DRAFT v1)** — Vai trò: đặt bài toán bỏ học vào khung lĩnh vực, và nêu **đặc thù của dữ liệu giáo dục** dẫn tới lựa chọn mô hình ở mục 2.3. Giữ ngắn; đây là mục bắc cầu, không phải tổng quan lĩnh vực đầy đủ.

## 2.2.1 Lĩnh vực và các bài toán liên quan

Khai phá dữ liệu giáo dục (Educational Data Mining) và học phân tích (Learning Analytics) là hai lĩnh vực gần nhau, cùng hướng tới việc sử dụng dữ liệu người học để hiểu và cải thiện quá trình đào tạo. Trong khung này, dự báo bỏ học không phải một bài toán biệt lập mà là **một mặt của cụm câu hỏi về hành trình học tập**: dự báo bỏ học (ai có nguy cơ rời trường), giữ chân người học (làm gì để họ ở lại), và thành công học tập (điều gì giúp họ hoàn thành tốt). Ba câu hỏi này chia sẻ phần lớn nguồn dữ liệu và phương pháp; khác biệt chủ yếu nằm ở biến mục tiêu.

Việc luận văn chọn tập trung vào **bỏ học** thay vì kết quả học tập nói chung xuất phát từ tính chất của can thiệp: điểm số có thể cải thiện dần trong nhiều học kỳ, nhưng việc rời trường là một sự kiện **gần như không đảo ngược** — nên giá trị của việc phát hiện sớm ở đây cao hơn rõ rệt.

## 2.2.2 Các nguồn dữ liệu và đặc thù của chúng

Tài liệu trong lĩnh vực này thường khai thác ba nhóm dữ liệu:

1. **Hồ sơ học vụ hành chính** — thông tin nhân khẩu, điểm tuyển sinh, kết quả từng học kỳ, tín chỉ đăng ký và đạt, cảnh báo học vụ. Đây là nguồn phổ biến nhất vì mọi trường đều lưu trữ.
2. **Nhật ký hệ thống quản lý học tập (LMS)** — số lần đăng nhập, thời lượng truy cập, tương tác với tài liệu. Nguồn này giàu tín hiệu hành vi nhưng chỉ có ở những trường số hóa mạnh, và mức độ sử dụng biến thiên lớn giữa các ngành.
3. **Khảo sát tâm lý – kinh tế xã hội** — động lực học tập, hoàn cảnh gia đình, áp lực tài chính. Có giá trị giải thích cao nhưng tốn kém để thu thập và thường không sẵn có.

**Phạm vi dữ liệu của luận văn cần được nêu rõ ngay từ đây:** nghiên cứu sử dụng **duy nhất nhóm thứ nhất** — hồ sơ học vụ hành chính. Lựa chọn này có mặt được và mặt mất. Mặt được là **khả năng áp dụng rộng**: mọi trường đại học đều có sẵn loại dữ liệu này, nên quy trình đề xuất không đòi hỏi hạ tầng đặc biệt. Mặt mất là mô hình **không quan sát được** các yếu tố hành vi và hoàn cảnh cá nhân, vốn được ghi nhận là quan trọng trong bối cảnh Đông Nam Á; hạn chế này được nêu lại ở phần bàn luận.

## 2.2.3 Vì sao dữ liệu giáo dục có đặc thù riêng

Bốn tính chất của dữ liệu học vụ định hình cách tiếp cận mô hình hóa:

- **Dạng bảng, hỗn hợp kiểu** — vừa có biến số, vừa có biến hạng mục (ngành học, khu vực, dân tộc).
- **Có cấu trúc thời gian rời rạc** — dữ liệu đến theo từng học kỳ, không phải chuỗi liên tục; số mốc thời gian thường ít.
- **Nhiều giá trị thiếu, và giá trị thiếu *có nghĩa*** — một học kỳ không có dữ liệu thường không phải lỗi ghi chép mà phản ánh trạng thái thực của sinh viên.
- **Mất cân bằng lớp** — nhóm bỏ học luôn là thiểu số.

## 2.2.4 Hạn chế của tài liệu trong lĩnh vực

Điểm hạn chế nổi bật khi tổng hợp tài liệu là **khả năng so sánh giữa các công trình rất thấp**: định nghĩa biến mục tiêu, nguồn dữ liệu, cách xây dựng đặc trưng, giao thức đánh giá và thời điểm dự báo đều khác nhau và thường không được báo cáo đầy đủ. Hệ quả là một chỉ số hiệu năng đứng một mình gần như không mang thông tin nếu thiếu bối cảnh đi kèm — điều này cũng lý giải vì sao luận văn dành trọng tâm cho **giao thức đánh giá** chứ không chỉ cho con số cuối cùng.

Bảng 2.1 tổng hợp các công trình được khảo sát theo những tiêu chí nêu trên, và là cơ sở cho các nhận định về khoảng trống nghiên cứu ở các mục 2.5–2.9. Mỗi công trình được đọc theo cùng một bộ câu hỏi: dự báo tại thời điểm nào, có kiểm soát rò rỉ không, có đánh giá hiệu chỉnh xác suất (cột *Cal*), tính công bằng (*Fair*), khả năng giải thích (*XAI*) và can thiệp sớm (*EI*) hay không.

**Bảng 2.1.** Tổng hợp các công trình dự báo bỏ học được khảo sát, theo thời điểm dự báo, kiểm soát rò rỉ, hiệu chỉnh xác suất, tính công bằng, khả năng giải thích và can thiệp sớm. *(Nguồn: tác giả tổng hợp.)*

Ký hiệu: ★ = có và là trọng tâm · ✔ = có · ✘ = không · ? = **chưa xác minh được từ bản đầy đủ**.

| Công trình | Năm | Thời điểm dự báo | Kiểm soát rò rỉ | *Cal* | *Fair* | *XAI* | *EI* |
|---|---|---|---|---|---|---|---|
| Dự báo sớm nhiều mốc (EDM) | 2024 | ★ 5 mốc trong học kỳ | ✔ (loại điểm ở mốc sớm) | ✘ | ✘ | ✘ | ✔ |
| LightGBM + SMOTE (Appl. Sci. 13:12004) | 2023 | ? | ? | ? | ? | ? | ✔ |
| Day One (Appl. Sci. 15:9202) | 2025 | Trước nhập học | ✔ | ? | ? | ? | ★ |
| Pipeline mô-đun + SHAP (Algorithms 18:662) | 2025 | ? | ? | ? | ? | ★ | ✔ |
| Tổng quan ML/DL (Computers 15:164) | 2025 | — (bài tổng quan) | ? | ? | ? | ? | — |
| Model drift (Computers 14:351) | 2025 | ✔ theo thời gian | ? | ? | ? | ✘ | ✘ |
| Mẫu thời gian theo học kỳ (Electronics 14:4356) | 2025 | ★ theo học kỳ | ? | ? | ? | ? | ? |
| FairEduNet (Scientific Reports) | 2025 | ? | ? | ? | ★ | ? | ? |
| Dropout đại học Phần Lan (Technol. Soc.) | 2024 | Theo học kỳ | ? | ✘ | ✘ | ? | ✔ |
| Stacked ensemble hai lớp (Comput. Educ. AI) | 2022 | ? | ? | ✘ | ✘ | ✘ | ✘ |

> **[ĐANG HOÀN THIỆN]** Các ô `?` là những tiêu chí chưa xác minh được vì chưa truy cập được bản đầy đủ của công trình. Bảng sẽ được hoàn tất trước khi nộp; các nhận định ở các mục 2.5–2.8 hiện chỉ dựa trên những ô **đã xác minh**, không suy đoán từ ô `?`.

## 2.2.5 Chuyển tiếp

Bốn đặc thù nêu ở mục 2.2.3 — dữ liệu dạng bảng với kiểu hỗn hợp, cấu trúc thời gian rời rạc và ngắn, giá trị thiếu mang ý nghĩa, và mất cân bằng lớp — trực tiếp thu hẹp không gian lựa chọn mô hình. Mục tiếp theo trình bày vì sao, trong không gian đó, các mô hình cây tăng cường độ dốc, và cụ thể là LightGBM, là lựa chọn phù hợp với nghiên cứu này.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- 📍 **Vị trí Bảng 2.1 (quyết định 19/7).** Bảng khảo sát tài liệu đặt ở cuối mục 2.2.4 vì đây là chỗ nêu nhận định "khả năng so sánh giữa các công trình rất thấp" — bảng chính là bằng chứng cho nhận định đó, và nó phải xuất hiện **trước** Bảng 2.2 (mục 2.3.4) để thứ tự đánh số khớp thứ tự đọc. Nội dung bảng lấy từ `Chuong2_LiteratureMatrix.md` (Bảng B).
- 🔴 **Chặn việc in:** bảng này còn nhiều ô `?` (5 bài MDPI chưa đọc được PDF) — xem M1 trong `MASTER_CHECKLIST.md`. Không đưa vào bản in khi còn ô trống, vì bốn mục 2.5–2.8 đều viện dẫn các cột của nó.
- Nếu cần trích dẫn định nghĩa EDM/Learning Analytics, bổ sung nguồn gốc (hiện diễn đạt khái quát, chưa gắn trích dẫn cụ thể để tránh trích chưa xác minh).
- Bổ sung trích dẫn cho nhận định "yếu tố kinh tế gia đình quan trọng ở Đông Nam Á" (2.2.2) — đã thấy trong tài liệu khảo sát, cần chốt nguồn cụ thể trước khi in.
- Mục 2.2.3 phải khớp với 2.3.3 (bốn đặc thù ↔ bốn lý do chọn mô hình) — kiểm tra lại sau khi đọc liền mạch cả chương.
