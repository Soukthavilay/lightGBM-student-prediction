# 2.4 Rò rỉ dữ liệu và nguyên lý Landmarking (Data Leakage and Landmarking)

> **BẢN THẢO (DRAFT v2)** — Mục lõi của Chương 2, đặt nền học thuật cho đóng góp chính của luận văn. Viết để dẫn tới hạn chế (1) và đóng góp (1) ở mục 2.9.

Mục này trình bày nền tảng học thuật cho đóng góp trung tâm của luận văn. Chúng tôi lần lượt định nghĩa rò rỉ dữ liệu, chỉ ra vì sao nó đặc biệt nguy hiểm trong dự báo bỏ học sớm, và giới thiệu nguyên lý *landmarking* như một giải pháp có nền tảng thống kê. Cần nói rõ ngay từ đầu để người đọc thấy mục này không chỉ thuần lý thuyết: luận văn khắc phục vấn đề rò rỉ bằng cách xây dựng tập dữ liệu **theo chân trời thời gian** (hàm `horizon_dataset()`) — chỉ dùng dữ liệu đến học kỳ *h* trên đúng nhóm sinh viên còn theo học — vốn là một hiện thực hóa trực tiếp của nguyên lý landmarking trình bày ở mục 2.4.3.

## 2.4.1 Khái niệm rò rỉ dữ liệu

Trong khai phá dữ liệu và học máy, **rò rỉ dữ liệu** (data leakage) được Kaufman và cộng sự (2012) định nghĩa là việc đưa vào mô hình những thông tin về biến mục tiêu mà lẽ ra *không khả dụng một cách hợp lệ* tại thời điểm dự báo. Các tác giả xếp rò rỉ vào nhóm những sai lầm nghiêm trọng và khó phát hiện nhất của khai phá dữ liệu, bởi nó không làm mô hình "hỏng" mà ngược lại làm mô hình *có vẻ tốt lên*: các chỉ số đánh giá trên tập kiểm tra bị nâng lên cao, trong khi năng lực thật khi triển khai lại thấp hơn nhiều.

Kaufman và cộng sự (2012) phân biệt hai dạng chính. Thứ nhất là **rò rỉ mục tiêu** (target leakage), khi một đặc trưng thực chất là hệ quả của nhãn chứ không phải nguyên nhân/tín hiệu có trước nhãn. Thứ hai là **rò rỉ theo thời gian** (temporal leakage), khi đặc trưng chứa thông tin chỉ tồn tại *sau* thời điểm mà dự báo cần được đưa ra. Chẳng hạn, nếu ta muốn dự báo ngay từ cuối học kỳ 1 nhưng lại đưa GPA của học kỳ 4 — hoặc trạng thái tốt nghiệp — vào làm đặc trưng, thì mô hình đã "nhìn thấy tương lai": đó là một trường hợp rò rỉ theo thời gian điển hình. Đối với các bài toán mang bản chất thời gian — mà dự báo bỏ học là một ví dụ điển hình — rò rỉ theo thời gian là mối đe dọa thường trực.

## 2.4.2 Vì sao rò rỉ đặc biệt nghiêm trọng trong dự báo bỏ học sớm

Mục tiêu của một hệ thống *cảnh báo sớm* là: tại một thời điểm nhất định trong quá trình học (ví dụ cuối học kỳ *h*), dự báo những sinh viên **còn đang theo học** nào có nguy cơ bỏ học *về sau*. Bản chất này đặt ra một ràng buộc chặt: mọi đặc trưng đưa vào mô hình phải khả dụng *tính đến* thời điểm *h*, và quần thể phân tích phải là những sinh viên còn "trong diện rủi ro" tại thời điểm đó.

Trên thực tế, nhiều công trình vi phạm ràng buộc này theo hai cách. (i) Về đặc trưng: sử dụng các biến chỉ có được ở *cuối* chương trình — điểm trung bình tích lũy toàn khóa, tổng số môn trượt, hay trạng thái đăng ký/tốt nghiệp — vốn là hệ quả trực tiếp của việc sinh viên đã (hoặc chưa) bỏ học. (ii) Về quần thể: huấn luyện và đánh giá trên toàn bộ khóa, kể cả những sinh viên đã rời trường *trước* thời điểm *h*; với nhóm này, các đặc trưng của học kỳ *h* (GPA bằng 0, không đăng ký tín chỉ) không còn là tín hiệu dự báo mà chính là dấu vết của nhãn.

Hậu quả đã được ghi nhận rõ trong tài liệu. Một số nghiên cứu báo cáo các chỉ số gần như hoàn hảo (F1 và AUC xấp xỉ 1,0) — điều gần như bất khả thi với dữ liệu giáo dục vốn nhiều nhiễu; rà soát sau đó cho thấy nguyên nhân là các biến hậu-kết-quả (trạng thái đăng ký, cờ tốt nghiệp) đã lọt vào tập đặc trưng và mã hóa gần như trực tiếp cho nhãn. Nói cách khác, mô hình không *dự báo* bỏ học mà chỉ *ghi lại hậu quả* của nó, khiến kết quả trông chính xác hơn nhiều so với hiệu năng thật khi vận hành.

Hình 2.1 minh họa ràng buộc thời gian này: chỉ dữ liệu trong *cửa sổ quan sát* (đến học kỳ mốc *h*) mới được phép dùng để dự báo biến cố nằm trong *chân trời kết quả* (sau *h*), và mọi đặc trưng chạm tới học kỳ sau *h* đều là rò rỉ.

**Hình 2.1.** Minh họa cửa sổ quan sát và chân trời kết quả. (a) Chỉ dùng dữ liệu đến học kỳ mốc *h* để dự báo biến cố xảy ra sau *h*. (b) Cách xây đặc trưng đúng (chỉ HK1..*h* → dự báo) so với cách rò rỉ (dùng cả HK1–HK4 rồi dự báo tại thời điểm *h*). *(Nguồn: tác giả; tệp `03_KetQua_Hinh/fig_2_4_landmark_horizon.png`.)*

## 2.4.3 Landmarking như một giải pháp có nền tảng thống kê

Vấn đề "dự báo một biến cố tương lai chỉ dựa trên thông tin đến một thời điểm quan sát" không mới; nó đã được nghiên cứu bài bản trong phân tích lịch sử biến cố (event history / survival analysis). van Houwelingen (2007) đề xuất phương pháp **landmarking**: chọn một *thời điểm mốc* (landmark time), giới hạn tập phân tích về đúng những cá thể **còn trong diện rủi ro** tại mốc đó, và xây dựng mô hình dự báo chỉ dựa trên thông tin có được *tính đến* mốc. Bằng cách này, mô hình luôn được ước lượng trên đúng quần thể và đúng tập thông tin mà nó sẽ gặp khi triển khai, qua đó loại bỏ rò rỉ theo thời gian *ngay từ khâu thiết kế dữ liệu* thay vì sửa chữa về sau.

Mặc dù landmarking ra đời trong phân tích sống còn, nguyên lý của nó chuyển giao tự nhiên sang bài toán dự báo bỏ học, bởi cả hai về bản chất đều là bài toán *thời gian-đến-biến-cố* (time-to-event): điều quan tâm không chỉ là *liệu* biến cố (tử vong hay bỏ học) có xảy ra, mà còn là *khi nào* nó xảy ra, và ở mỗi thời điểm luôn tồn tại một nhóm cá thể "còn trong diện rủi ro" thay đổi theo thời gian. Chính sự tương đồng cấu trúc này biện minh cho việc mượn khung landmarking từ y sinh để áp dụng cho giáo dục.

Cùng tinh thần đó, các khuyến nghị báo cáo minh bạch mô hình dự báo (TRIPOD; Collins và cộng sự, 2015) nhấn mạnh việc phân định rõ ràng thời điểm dự báo, thông tin khả dụng tại thời điểm đó, và chân trời kết quả — chính là sự tách bạch giữa **cửa sổ quan sát** (observation window) và **chân trời kết quả** (outcome horizon).

## 2.4.4 Định vị đóng góp của luận văn

Trên nền tảng trên, kỹ thuật **đặc trưng theo chân trời thời gian** (horizon-aware feature engineering) đề xuất trong luận văn **không nên hiểu là một thủ thuật kỹ thuật được đặt tên mới**, mà là **sự hiện thực hóa nguyên lý landmarking** (van Houwelingen, 2007) cho bài toán dự báo bỏ học đại học: với mỗi chân trời *h*, tập dữ liệu chỉ giữ những sinh viên còn hoạt động tại học kỳ *h* và chỉ dùng đặc trưng xây từ các học kỳ 1..*h*, trong khi nhãn được định nghĩa là "bỏ học sau cuối học kỳ *h*". Cách tiếp cận này vừa tôn trọng ràng buộc triển khai thực tế, vừa phù hợp với khuyến nghị minh bạch của TRIPOD, và trực tiếp khắc phục hạn chế (1) sẽ được tổng hợp ở mục 2.9.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- Chèn **bằng chứng định lượng từ chính dữ liệu luận văn** vào 2.4.2: AUC HK1-2 bị thổi phồng ~0,95, xấp xỉ mức mà chỉ riêng cột GPA4_2 đạt được → minh họa sống động cho target leakage.
- ✅ Hình 2.1 đã tạo (`03_KetQua_Hinh/fig_2_4_landmark_horizon.png`) — kiểm tra lại độ phân giải/khổ khi chèn vào bản Word cuối.
- Thêm 1 trích dẫn nguồn gốc cho ví dụ "F1=AUC≈1,0" (bài PLOS One về private-safe dropout) sau khi xác minh bản đầy đủ.
- Kiểm tra thuật ngữ Việt: "cửa sổ quan sát / chân trời kết quả / thời điểm mốc" — thống nhất với bảng thuật ngữ đầu luận văn.
