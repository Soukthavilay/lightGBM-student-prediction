# 2.8 Hệ thống cảnh báo sớm và can thiệp

> **BẢN THẢO (DRAFT v1)** — Mục này viết theo trục **chuỗi hành động**: *Dự báo → Quyết định → Can thiệp → Kết quả*. ⛔ **Không** viết như một tổng quan lĩnh vực learning analytics; mọi nội dung không nằm trên chuỗi bốn khâu này đều ngoài phạm vi.
> ⚠️ Kết quả thực nghiệm thuộc Chương 4.

## 2.8.1 Chuỗi hành động: bốn khâu

Một mô hình dự báo, tự nó, không giữ được sinh viên nào ở lại trường. Giá trị chỉ hình thành khi dự báo đi hết một chuỗi bốn khâu:

**Dự báo** (ai có nguy cơ) → **Quyết định** (ai được đưa vào danh sách can thiệp) → **Can thiệp** (làm gì với họ) → **Kết quả** (điều đó có thay đổi được gì không).

Phần lớn nghiên cứu dừng lại ở khâu thứ nhất. Nhưng mỗi khâu chuyển tiếp đều có thể làm hỏng toàn bộ chuỗi: một mô hình chính xác nhưng đặt ngưỡng sai sẽ tạo ra danh sách vượt quá năng lực tiếp cận; một danh sách hợp lý nhưng hình thức can thiệp không phù hợp sẽ không tạo tác động; và một can thiệp tốt mà không đo kết quả thì không thể biết có nên tiếp tục hay không. Mục này lần lượt xem xét ba khâu sau — vì khâu đầu đã được bàn ở các mục trước.

## 2.8.2 Khâu quyết định: ngưỡng là một tuyên bố chính sách

Chuyển từ xác suất sang danh sách hành động đòi hỏi một **ngưỡng**, và như đã lập luận ở mục 2.5, ngưỡng không phải tham số kỹ thuật mà là **phát biểu về sự đánh đổi chi phí**: chọn ngưỡng thấp nghĩa là chấp nhận nhiều báo động giả để không bỏ sót; chọn ngưỡng cao nghĩa là ưu tiên độ chính xác của danh sách.

Trong bối cảnh trường đại học, ràng buộc quyết định thường **không phải là ngưỡng xác suất mà là năng lực**: một khoa chỉ có thể tiếp cận sâu một số lượng sinh viên nhất định mỗi học kỳ. Do đó câu hỏi vận hành thực tế không phải "ngưỡng tối ưu là bao nhiêu" mà là *"với năng lực tiếp cận k sinh viên, danh sách nào giúp tiếp cận đúng người nhất"*. Phân tích đường cong quyết định (mục 2.5) chính là công cụ trả lời câu hỏi này, vì nó đánh giá lợi ích ròng trên toàn dải ngưỡng thay vì tại một điểm duy nhất.

## 2.8.3 Khâu can thiệp: bằng chứng từ hệ thống đã triển khai

Hệ thống được trích dẫn nhiều nhất trong lĩnh vực này là **Course Signals** tại Đại học Purdue (Arnold & Pistilli, 2012). Cách tiếp cận của nó có hai đặc điểm đáng chú ý: kết quả dự báo được truyền đạt bằng **tín hiệu đèn giao thông** (xanh – vàng – đỏ) thay vì con số xác suất, và mỗi tín hiệu gắn với một **hành động cụ thể** của giảng viên, thường là email hoặc liên hệ trực tiếp. Nói cách khác, hệ thống được thiết kế quanh *hành động*, không quanh *mô hình*.

Tuy nhiên, cần nêu cả mặt phản biện. Thuật toán rủi ro của Course Signals là **độc quyền và không công bố**, khiến kết quả khó tái lập và khó kiểm tra tính công bằng. Quan trọng hơn, các tuyên bố về hiệu quả giữ chân sinh viên của hệ thống này về sau **đã bị đặt câu hỏi về phương pháp**: phân tích ban đầu không kiểm soát **số lượng môn học mà sinh viên đăng ký**, dẫn tới khả năng **đảo chiều quan hệ nhân quả** — sinh viên đăng ký nhiều môn có dùng Course Signals hơn *bởi vì* họ vẫn đang tiếp tục theo học, chứ không phải tiếp tục theo học *bởi vì* đã dùng hệ thống. Weidlich, Gašević & Drachsler (2022) dẫn lại trường hợp này khi phân tích các dạng thiên lệch thường gặp trong suy luận nhân quả ở học phân tích — nhiễu (confounding), overcontrol và collider — và đề xuất dùng **đồ thị nhân quả có hướng (DAG)** để làm rõ giả định trước khi kết luận về hiệu quả can thiệp.

Bài học rút ra không phải là bác bỏ mô hình cảnh báo sớm, mà là: **tác động của can thiệp phải được thiết kế để đo lường được ngay từ đầu**, thay vì suy ra từ tương quan sau khi triển khai.

## 2.8.4 Thiết kế nhiều tầng theo mức độ can thiệp

Một hệ thống chỉ dùng **một ngưỡng duy nhất** buộc phải chấp nhận một đánh đổi cứng nhắc: ngưỡng thấp thì danh sách quá rộng, vượt năng lực tiếp cận và làm loãng nguồn lực; ngưỡng cao thì bỏ sót nhiều sinh viên cần giúp. Vấn đề nằm ở chỗ **một con số không thể phục vụ hai mục đích khác nhau** — vừa "không bỏ sót ai" vừa "dồn nguồn lực đắt cho đúng người".

Thiết kế **nhiều tầng theo mức độ can thiệp** nới lỏng đánh đổi này bằng cách gắn *nhiều ngưỡng khác nhau với những hình thức hỗ trợ khác nhau*, trên cùng một bộ xác suất dự báo. **Tầng thứ nhất** dùng ngưỡng thấp để **sàng lọc rộng**, ưu tiên không bỏ sót; nhóm này nhận hình thức hỗ trợ nhẹ và rẻ, chẳng hạn cố vấn theo dõi và nhắc nhở định kỳ. **Tầng thứ hai** dùng ngưỡng cao để **can thiệp sâu**, ưu tiên độ chính xác; nhóm này nhỏ hơn nhiều nhưng nhận hình thức hỗ trợ tốn kém hơn, chẳng hạn gặp trực tiếp hoặc hỗ trợ tài chính, tâm lý. Nhờ đó, mỗi mức nguồn lực được phân bổ theo đúng mức rủi ro, thay vì áp một chính sách chung cho mọi trường hợp.

> **Làm rõ thuật ngữ.** Trong nghiên cứu này, "hai tầng" **không** biểu thị hai *thời điểm dự báo* khác nhau, mà biểu thị hai *mức độ can thiệp* khác nhau trên cùng một bộ xác suất đã hiệu chỉnh. Nói cách khác, **chân trời thời gian và tầng can thiệp là hai trục độc lập**: chân trời quyết định *khi nào và bằng dữ liệu gì* mô hình đưa ra dự báo (mục 2.4), còn tầng quyết định *làm gì với dự báo đó*. Việc mở rộng sang cảnh báo tại nhiều thời điểm liên tiếp (ví dụ cảnh báo lần đầu ở cuối HK1 rồi cập nhật ở cuối HK1-2) là một **hướng nghiên cứu tiếp theo**, không thuộc phạm vi luận văn này.

## 2.8.5 Khâu kết quả: khoảng trống lớn nhất, và ranh giới của luận văn

Trong số các công trình được tổng hợp ở Bảng 2.1, rất ít công trình đi tới khâu can thiệp (cột *EI*), và hầu như không công trình nào **đo được liệu can thiệp có thay đổi kết quả hay không**. Nguyên nhân dễ hiểu: đánh giá tác động đòi hỏi thiết kế thực nghiệm hoặc phương pháp suy luận nhân quả, vượt ra ngoài phạm vi một nghiên cứu mô hình hóa thông thường.

Luận văn này cũng nằm trong giới hạn đó, và điều này cần được nói rõ: nghiên cứu **xây dựng và đánh giá hệ thống cảnh báo tới khâu quyết định** — bao gồm việc lựa chọn ngưỡng vận hành và phân tích lợi ích ròng — nhưng **không tiến hành thử nghiệm can thiệp** và do đó **không đưa ra tuyên bố nào về hiệu quả giữ chân sinh viên**. Việc đo lường tác động thực tế, bằng thiết kế đối chứng hoặc mô hình uplift, được nêu như hướng nghiên cứu tiếp theo.

## 2.8.6 Kết luận mục

Nhìn lại toàn chuỗi, có thể phát biểu nguyên tắc chi phối thiết kế của luận văn: **giá trị của một hệ thống cảnh báo sớm không nằm ở khả năng dự báo của nó, mà ở khả năng biến dự báo đó thành sự hỗ trợ có thật.** Chính nguyên tắc này giải thích vì sao các mục trước không dừng ở độ chính xác, mà lần lượt yêu cầu dữ liệu không rò rỉ (2.4), xác suất đáng tin (2.5), phân bổ công bằng (2.6) và giải thích được ở cấp độ từng sinh viên (2.7) — bốn điều kiện cần để khâu cuối cùng của chuỗi có thể xảy ra.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- ✅ 19/7: `Bảng 2.x` đã thay bằng **Bảng 2.1** (bảng khảo sát tài liệu, đặt ở cuối mục 2.2.4).
- ✅ **Nguồn phản biện Course Signals đã có (peer-reviewed):** Weidlich, J., Gašević, D., & Drachsler, H. (2022). *Causal Inference and Bias in Learning Analytics: A Primer on Pitfalls Using Directed Acyclic Graphs.* Journal of Learning Analytics, 9(3), 183–199. DOI 10.18608/jla.2022.7577 — đã thêm vào `anchor_refs.bib`.
- ⚠️ Phê phán gốc là của **Caulfield (2013)**, công bố dưới dạng **bài blog**, không phải bài báo bình duyệt. Trong luận văn **nên trích dẫn gián tiếp qua Weidlich và cộng sự (2022)** như hiện tại, hoặc nếu muốn nêu tên Caulfield thì phải ghi rõ đây là nguồn không bình duyệt.
- Giá trị ngưỡng vận hành cụ thể của hai tầng thuộc Chương 3–4; ở đây chỉ nêu nguyên tắc thiết kế.
- ✅ Nguồn gốc `warning_thresholds.csv` đã khép: sinh bởi `warning_tiers()` như một bước của `run_pipeline.py` (18/7).
- ✅ 19/7: đã thống nhất dùng **"ngưỡng vận hành"** (operating point) toàn luận văn, bỏ hẳn cách gọi "điểm vận hành". Định nghĩa đặt ở mục 2.5.4 cùng ký hiệu $p_t$.
