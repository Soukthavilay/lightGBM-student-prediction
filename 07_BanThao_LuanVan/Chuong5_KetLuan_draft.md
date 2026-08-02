# Chương 5. Bàn luận và kết luận

> **BẢN THẢO (DRAFT v1).** Mọi số liệu dẫn lại từ Chương 4 (lần chạy FULL 2026-07-18). Chương này **không giới thiệu kết quả mới**, chỉ diễn giải, đặt vào bối cảnh tài liệu, và nêu giới hạn.

---

## 5.1 Tóm tắt kết quả chính

Luận văn đặt ra ba câu hỏi nghiên cứu. Kết quả ở Chương 4 cho phép trả lời cả ba.

**Thứ nhất, có thể dự báo sớm được không, và sớm tới đâu?** Được. Với những sinh viên còn theo học sau **học kỳ 1**, mô hình đạt AUC **0,8436**; khi có thêm dữ liệu **học kỳ 2**, AUC tăng lên **0,9203**. Ở ngưỡng vận hành thực tế, hệ thống gắn cờ 12,8% quần thể và bắt được 73,6% số trường hợp bỏ học (tầng sàng lọc), hoặc gắn cờ 5,1% với độ chính xác 80,1% (tầng can thiệp sâu). Cảnh báo sớm là khả thi, và tạo điều kiện để nhà trường hành động trước khi quyết định rời trường trở nên không thể đảo ngược.

> **Làm rõ — mô hình nào là mô hình của luận văn.** Cần phân định rõ hai cấu hình để tránh nhầm lẫn. **LightGBM với tham số mặc định** (AUC 0,8436 ở HK1 và 0,9203 ở HK1-2) là mô hình được dùng xuyên suốt các phân tích triển khai — hiệu chỉnh xác suất, đường cong quyết định, kiểm định thời gian, công bằng, giải thích SHAP và hệ thống cảnh báo hai tầng; **mọi con số vận hành trong luận văn đều đến từ cấu hình này**. Riêng **LightGBM sau tinh chỉnh bằng nested cross-validation** (0,8506 ± 0,0107 ở HK1, mục 4.5) chỉ phục vụ **một mục đích duy nhất**: đo xem việc tối ưu siêu tham số mang lại thay đổi bao nhiêu khi được đánh giá đúng cách. Cấu hình này **không** được đưa vào các phân tích triển khai, vì mức cải thiện (ΔAUC ≈ +0,007) nhỏ hơn cả độ lệch chuẩn giữa các fold (0,0107), không đủ để biện minh cho việc thay thế một cấu hình đơn giản và ổn định hơn.

**Thứ hai, kết quả có đáng tin không?** Có — và điều quan trọng là *đáng tin theo nghĩa nào*. Ba thuật toán được so sánh cho hiệu năng phân biệt gần như tương đương, với năm trong sáu cặp không đạt ý nghĩa thống kê sau hiệu chỉnh Holm. Xác suất sau hiệu chỉnh isotonic có Brier 0,0363 và ECE 0,0047 — dưới sàn nhiễu ước tính, nghĩa là **không phát hiện sai lệch hiệu chỉnh**. Mô hình giữ được hiệu năng khi chuyển khóa (2020 → 2021: AUC 0,8842 [0,8579–0,9072]), và **chưa quan sát được** chênh lệch giữa các nhóm giới tính hay dân tộc — một phát biểu cần đọc đúng phạm vi, vì nghiên cứu không được thiết kế để chứng minh sự tương đương (mục 5.4). Về **độ ổn định của giải thích** — câu hỏi thứ tư trong nhóm này — kết quả lại đòi hỏi sự dè dặt: chỉ **9 trong 36 đặc trưng** giữ được vị trí trong nhóm mười quan trọng nhất ở từ 4/5 fold trở lên, nghĩa là phần lớn thứ hạng tầm quan trọng **không ổn định** giữa các lần huấn luyện; vì vậy chỉ nhóm lõi này được đưa ra diễn giải. Phân tích đường cong quyết định cho thấy mô hình có lợi ích ròng dương trên toàn dải ngưỡng khảo sát.

**Thứ ba, yếu tố nào liên quan tới nguy cơ bỏ học?** Trong 36 đặc trưng, chỉ **chín đặc trưng ổn định** qua ít nhất 4/5 fold, trong đó bốn đặc trưng ổn định tuyệt đối: ngành học, GPA học kỳ 2, tổng điểm đầu vào và khu vực. Các yếu tố còn lại trong nhóm ổn định gồm tỷ lệ tín chỉ đạt, GPA thấp nhất, GPA trung bình, cảnh báo học vụ tích lũy và một thành phần điểm đầu vào. Cần nhấn mạnh: đây là quan hệ **liên hệ trong mô hình**, không phải quan hệ nhân quả.

---

## 5.2 Bàn luận

### 5.2.1 Rò rỉ dữ liệu: từ nghi ngờ tới bằng chứng

Đóng góp có sức thuyết phục nhất của luận văn không nằm ở con số cao nhất mà ở con số **bị hạ xuống**. Bảng 4.6 cho thấy thiết kế cũ đạt AUC 1,0000 khi dùng cả bốn học kỳ — một kết quả bất khả thi với dữ liệu giáo dục — và 0,9546 ở chân trời HK1-2. Nhưng bằng chứng quyết định là: **riêng một biến `GPA4_2`, không qua bất kỳ mô hình nào, đạt 0,9556** — cao hơn cả mô hình 36 đặc trưng. Khi 35 đặc trưng còn lại không đóng góp gì, chỉ có một lời giải thích: biến đó là **biến thay thế của nhãn**, ghi lại hậu quả của việc đã rời trường chứ không dự báo tương lai.

Chênh lệch này được quy cho thiết kế dữ liệu chứ không phải cho bộ phân loại, vì trong phép so sánh ở Bảng 4.6 **thuật toán, siêu tham số, hằng số ngẫu nhiên, giao thức kiểm định chéo và chỉ số đánh giá đều được giữ nguyên**; yếu tố duy nhất thay đổi là cách xác định quần thể và tập đặc trưng theo thời điểm dự báo (mục 4.7). Hơn nữa, bằng chứng `GPA4_2` được tính **trên chính quần thể của thiết kế cũ**, nên nó không phụ thuộc vào việc quần thể có thay đổi hay không.

Phát hiện này nhất quán với cảnh báo của Kaufman và cộng sự (2012) rằng rò rỉ nguy hiểm chính vì nó làm mô hình *trông tốt lên*, và với ghi nhận trong tài liệu về những công trình dự báo bỏ học báo cáo chỉ số gần như hoàn hảo do biến hậu-kết-quả lọt vào tập đặc trưng. Sau khi giới hạn quần thể theo nguyên lý landmarking (van Houwelingen, 2007), AUC giảm còn 0,8386 và 0,9145. Con số thấp hơn, nhưng **phản ánh đúng năng lực cảnh báo sớm trong điều kiện triển khai**.

### 5.2.2 Khung phương pháp độc lập với lựa chọn thuật toán

Một kết quả ban đầu có vẻ bất lợi lại củng cố luận điểm trung tâm của luận văn: **hồi quy logistic đạt AUC cao hơn LightGBM ở cả hai chân trời** (0,8464 so với 0,8436; 0,9278 so với 0,9203), dù khác biệt không đạt ý nghĩa thống kê sau hiệu chỉnh Holm.

Điều này không làm suy yếu nghiên cứu, vì luận văn **chưa bao giờ tuyên bố LightGBM là mô hình tốt nhất** (mục 2.3.5). Ngược lại, nó cho thấy khung phương pháp không được thiết kế để một thuật toán cụ thể thắng. Nếu một nghiên cứu tương lai chứng minh một mô hình khác phù hợp hơn, các kết luận phương pháp luận — chống rò rỉ theo chân trời, đánh giá bằng nested CV, hiệu chỉnh xác suất, kiểm tra công bằng và độ ổn định giải thích — **vẫn giữ nguyên giá trị**.

Đồng thời, kết quả cũng cho thấy **AUC một mình không đủ để chọn mô hình triển khai**. Hồi quy logistic có Brier 0,0872 ở HK1-2, kém hơn LightGBM (0,0395) khoảng 2,2 lần, với precision 0,3551 so với 0,6984. Với một hệ thống vận hành bằng ngưỡng xác suất và phân bổ nguồn lực tư vấn hữu hạn, khác biệt này quan trọng hơn 0,0074 điểm AUC. Đây là minh chứng thực nghiệm cho lập luận ở mục 2.5.1: **khả năng phân biệt tốt không đồng nghĩa với xác suất đáng tin**.

### 5.2.3 Giải thích được, nhưng phải kiểm chứng độ ổn định

Kết quả phân tích SHAP xác nhận mối lo ngại nêu ở mục 2.7.4. Chỉ 9 trong 36 đặc trưng lọt nhóm mười quan trọng nhất ở từ 4/5 fold trở lên, và **21 đặc trưng chưa từng lọt nhóm này ở bất kỳ fold nào**. Nói cách khác, nếu chỉ trình bày một biểu đồ SHAP duy nhất rồi diễn giải toàn bộ thứ hạng — cách làm phổ biến trong tài liệu — thì phần lớn nội dung diễn giải sẽ không tái lập được.

Cách xử lý của luận văn là **đo độ ổn định thay vì giả định nó**, rồi chỉ diễn giải nhóm lõi. Cách này phù hợp với các giới hạn lý thuyết mà Bilodeau và cộng sự (2024) chỉ ra: quy gán đặc trưng không phải công cụ suy luận vạn năng, nhưng vẫn hữu ích nếu được dùng có kỷ luật và trong phạm vi phù hợp.

### 5.2.4 Công bằng: chưa phát hiện chênh lệch, nhưng chưa thể kết luận là công bằng

Khoảng tin cậy AUC của các nhóm đều chồng lấn, và độ nhạy chênh lệch theo giới tính (0,4247 ở nữ so với 0,5769 ở nam) **giải thích được phần lớn bằng chênh lệch tỷ lệ nền** (5,20% so với 12,65%) tại cùng một ngưỡng tuyệt đối. Đây là kết quả đáng khích lệ, nhưng cần phát biểu chính xác: **"không phát hiện được chênh lệch có ý nghĩa" không đồng nghĩa với "đã chứng minh là công bằng"**, đặc biệt khi nhóm dân tộc thiểu số chỉ có 555 quan sát và khoảng tin cậy rộng tương ứng.

Kết quả này phù hợp với ghi nhận của Rodolfa và cộng sự (2021) rằng đánh đổi giữa công bằng và độ chính xác thường không đáng kể trên thực tế — nghĩa là việc đưa đánh giá công bằng vào quy trình không phải gánh nặng, mà là bước kiểm tra nên có.

---

## 5.3 Đóng góp của luận văn

Đóng góp được phát biểu ở tầng **thiết kế dữ liệu, quy trình đánh giá và chiến lược triển khai** — không phải ở tầng thuật toán.

1. **Thiết kế dữ liệu chống rò rỉ:** quy trình horizon-aware tách bạch tường minh **cửa sổ quan sát** (dữ liệu đến học kỳ mốc *h*) khỏi **chân trời kết quả** (biến cố xảy ra sau *h*), bằng cách kết hợp giới hạn quần thể (chỉ sinh viên còn hoạt động tại thời điểm mốc) với giới hạn đặc trưng (chỉ học kỳ 1..*h*). Đây là hiện thực hóa nguyên lý landmarking cho bài toán bỏ học đại học Việt Nam.
2. **Bằng chứng định lượng về rò rỉ** trên dữ liệu thật, có thể tái lập từ tệp (`leakage_validation.csv`), thay vì chỉ lập luận định tính.
3. **Quy trình đánh giá đầy đủ:** repeated OOF, bootstrap CI, DeLong với hiệu chỉnh Holm, nested CV, hiệu chỉnh xác suất, đường cong quyết định, kiểm định thời gian, phân tích công bằng và độ ổn định SHAP — kết hợp một cách hệ thống mà ít công trình dự báo bỏ học thực hiện trọn vẹn.
4. **Chiến lược triển khai hai tầng** gắn mỗi mức rủi ro với một hình thức can thiệp và mức chi phí tương ứng, kèm dải ngưỡng để mỗi trường tự chọn ngưỡng vận hành theo năng lực.

**Những gì luận văn KHÔNG tuyên bố:** không phát minh thuật toán mới; không khẳng định LightGBM vượt trội tuyệt đối; không đưa ra kết luận nhân quả từ SHAP; không chứng minh hệ thống làm giảm tỷ lệ bỏ học trên thực tế; và không cung cấp một mô hình dùng được ngay cho trường khác mà không huấn luyện lại.

---

## 5.4 Hạn chế

**Về tính hợp lệ nội tại.** Trạng thái "còn hoạt động" được xấp xỉ bằng `CreditsRegistered_k > 0`; nếu nhà trường có dữ liệu chính thức về thời điểm thôi học thì nên thay thế. Biến `TermStatus_k` được giả định là cảnh báo học vụ đã biết tại cuối học kỳ; nếu thực chất nó ghi nhận "đã nghỉ học" thì đó là nhãn trá hình và phải loại bỏ. Cơ chế dữ liệu thiếu chưa được mô hình hóa tường minh. **Cách kiểm chứng cả ba điểm này được trình bày cụ thể ở mục 5.5 (hướng 1 và 2)** — đều chỉ đòi hỏi bổ sung dữ liệu hành chính, không đòi hỏi thay đổi phương pháp.

**Về tính hợp lệ ngoại tại.** Dữ liệu đến từ một trường và chỉ gồm **hai khóa** (2020–2021), nên phép kiểm định chuyển khóa chỉ thực hiện được **một lần** và không đủ để kết luận về xu hướng trôi mô hình. Mô hình đã huấn luyện không áp dụng trực tiếp cho trường hay quốc gia khác.

Cần nêu thêm một giới hạn về phạm vi suy rộng của thí nghiệm rò rỉ ở mục 4.7: **thí nghiệm này chỉ được thực hiện với một bộ phân loại duy nhất là LightGBM**. Luận văn **không kiểm chứng** liệu độ lớn của mức thổi phồng có giữ nguyên với XGBoost, CatBoost hay các mô hình học sâu cho dữ liệu bảng hay không. Vì vậy kết luận được phát biểu ở phạm vi đúng với bằng chứng: nghiên cứu **không** khẳng định "thiết kế dữ liệu quan trọng hơn thuật toán nói chung", mà khẳng định rằng **rò rỉ phát sinh ở khâu xây dựng dữ liệu, tức trước khi bất kỳ thuật toán nào bắt đầu học** — và bằng chứng `GPA4_2` cho thấy điều đó đúng ngay cả khi không dùng mô hình nào. Việc lặp lại thí nghiệm với nhiều bộ phân loại là một kiểm chứng đơn giản và đáng làm.

**Về tính hợp lệ khái niệm.** Biến mục tiêu `Drop` có thể gộp chung việc thôi học hẳn, chuyển trường và tạm dừng — ba hiện tượng có ý nghĩa chính sách khác nhau. Ngoài ra, dữ liệu chỉ gồm hồ sơ học vụ hành chính, **không có** yếu tố tâm lý, hoàn cảnh kinh tế gia đình hay hành vi học tập trực tuyến — vốn được ghi nhận là quan trọng trong bối cảnh Đông Nam Á.

**Về kết luận thống kê.** Các dự báo ngoài fold không hoàn toàn độc lập, nên khoảng tin cậy bootstrap có xu hướng hơi hẹp và kiểm định DeLong dễ bác bỏ giả thuyết không hơn mức danh nghĩa; vì vậy kết quả duy nhất đạt ý nghĩa (p = 0,0496) được diễn giải thận trọng. Kiểm định theo lần lặp chỉ có 10 quan sát nên công suất thấp. Về phân tích công bằng, cần nêu ba giới hạn cùng nhau. Thứ nhất, tiêu chí so sánh giữa các nhóm là **khoảng tin cậy có chồng lấn hay không** — một tiêu chí mô tả, **không phải kiểm định thống kê chính thức**; nghiên cứu không thực hiện kiểm định chênh lệch giữa nhóm. Thứ hai, **nghiên cứu không được thiết kế để chứng minh sự tương đương**: nhóm dân tộc thiểu số chỉ có 555 quan sát nên khoảng tin cậy rộng, và một chênh lệch thực sự ở mức vừa phải vẫn có thể không bộc lộ; nếu cỡ mẫu tăng nhiều lần, kết quả có thể thay đổi. Thứ ba, **ngưỡng dùng để đo công bằng (0,5) không trùng với hai ngưỡng vận hành của hệ thống (0,10 và 0,40)**; vì *cơ hội bình đẳng* là tính chất gắn với một ngưỡng cụ thể, kết quả hiện có không tự động áp dụng cho hai tầng cảnh báo thực tế. Do cả ba giới hạn trên, mọi phát biểu về công bằng trong luận văn dừng ở **"chưa quan sát được chênh lệch, tại ngưỡng đã đo"**, và tuyệt đối không được đọc thành "hệ thống đã được chứng minh là công bằng". ECE phụ thuộc cách chia bin và có sàn nhiễu ở cỡ mẫu này.

**Về phạm vi triển khai.** Luận văn dừng ở khâu **quyết định** — lựa chọn ngưỡng vận hành và phân tích lợi ích ròng — mà **không tiến hành thử nghiệm can thiệp**, do đó không đưa ra tuyên bố nào về hiệu quả giữ chân sinh viên trên thực tế.

---

## 5.5 Hướng nghiên cứu tiếp theo

1. **Kiểm chứng hai giả định về dữ liệu bằng nguồn hành chính chính thức** — đây là hướng cần làm **trước tiên**, vì nó quyết định mức độ tin cậy của mọi kết quả còn lại. Cụ thể: (a) thay proxy `CreditsRegistered_k > 0` bằng **ngày thôi học chính thức** từ phòng đào tạo, rồi chạy lại toàn bộ quy trình để so sánh — nếu kết luận không đổi, đó là một **phân tích độ nhạy** củng cố kết quả hiện tại; nếu đổi, con số phải được cập nhật theo định nghĩa đúng; (b) đối chiếu ý nghĩa thực của `TermStatus_k` với quy chế học vụ — nếu biến này ghi nhận trạng thái "đã thôi học" thay vì cảnh báo học vụ, bật cờ `DROP_TERMSTATUS` và chạy lại, vì khi đó nó là nhãn trá hình. Cả hai chỉ đòi hỏi một trường dữ liệu bổ sung, không đòi hỏi thay đổi phương pháp.
2. **Mô hình hóa tường minh cơ chế dữ liệu thiếu** — kiểm tra giả thiết thiếu không ngẫu nhiên (MNAR) bằng cách đối chiếu với nguồn hành chính bên ngoài, và so sánh chiến lược hiện tại (giữ `NaN`) với các phương án quy gán có mô hình.
3. **Củng cố suy luận thống kê trên dự báo ngoài fold** — dùng bootstrap theo khối hoặc kiểm định hoán vị tôn trọng cấu trúc fold, để khắc phục việc khoảng tin cậy hiện hơi hẹp và kiểm định DeLong hơi dễ bác bỏ; đồng thời tăng số lần lặp để nâng công suất của kiểm định theo lần lặp (hiện chỉ n = 10).
4. **Cảnh báo tại nhiều thời điểm liên tiếp** — mở rộng từ hai tầng can thiệp sang cảnh báo lần đầu ở cuối HK1 rồi cập nhật ở cuối HK1-2, tận dụng trực tiếp cấu trúc chân trời.
5. **Đánh giá tác động can thiệp** bằng thiết kế đối chứng hoặc mô hình uplift, để chuyển từ "ai có nguy cơ" sang "can thiệp nào hiệu quả cho ai" — khắc phục giới hạn về phạm vi triển khai nêu ở mục 5.4.
6. **Phân tích sống còn động** để dự báo *thời điểm* bỏ học và xử lý rủi ro cạnh tranh (thôi học hẳn so với chuyển trường), khắc phục hạn chế về định nghĩa biến mục tiêu.
7. **Mô hình chuỗi** (LSTM, Transformer) khi có dữ liệu nhiều học kỳ hơn, nơi lợi thế của mô hình chuỗi mới có điều kiện thể hiện.
8. **Bổ sung yếu tố phi học vụ** — tâm lý, kinh tế gia đình, hành vi trên hệ thống quản lý học tập.
9. **Giám sát trôi mô hình và hiệu chỉnh lại định kỳ** khi có thêm khóa mới.
10. **Học liên kết (federated learning)** cho hợp tác đa trường mà không chia sẻ dữ liệu thô.
11. **Đánh giá công bằng tại đúng hai ngưỡng vận hành** (0,10 và 0,40) thay vì tại ngưỡng 0,5, và bổ sung so sánh ở **cùng tỷ lệ được cảnh báo** giữa các nhóm để tách ảnh hưởng của tỷ lệ nền; đồng thời tăng cỡ mẫu nhóm thiểu số để có đủ độ mạnh cho kết luận về tương đương. Đây là hướng rẻ nhất trong danh sách — chỉ tính lại cùng bộ chỉ số ở ngưỡng khác.
12. **Lặp lại thí nghiệm rò rỉ trên nhiều bộ phân loại** (XGBoost, CatBoost, mô hình học sâu cho dữ liệu bảng) để xem mức thổi phồng có phụ thuộc lựa chọn thuật toán hay không — chi phí thấp vì quy trình đã sẵn sàng, chỉ thay bộ phân loại.

Bảng 5.1 đối chiếu từng hạn chế ở mục 5.4 với hướng nghiên cứu tương ứng, để cho thấy các đề xuất trên **xuất phát từ giới hạn cụ thể của nghiên cứu này**, không phải danh sách chung chung.

**Bảng 5.1.** Đối chiếu hạn chế của nghiên cứu với hướng nghiên cứu tiếp theo. *(Nguồn: tác giả.)*

| Hạn chế (mục 5.4) | Hướng nghiên cứu tương ứng |
|---|---|
| Proxy "còn hoạt động"; giả định về `TermStatus` | (1) Kiểm chứng bằng nguồn hành chính chính thức |
| Cơ chế dữ liệu thiếu chưa mô hình hóa | (2) Mô hình hóa tường minh cơ chế thiếu |
| Dự báo ngoài fold không độc lập; công suất thấp | (3) Bootstrap theo khối / kiểm định hoán vị |
| Một trường, hai khóa; chưa kết luận được về trôi mô hình | (9) Giám sát trôi mô hình · (10) Học liên kết |
| `Drop` gộp thôi học hẳn / chuyển trường / tạm dừng | (6) Phân tích sống còn động với rủi ro cạnh tranh |
| Thiếu yếu tố tâm lý – kinh tế xã hội – hành vi | (8) Bổ sung yếu tố phi học vụ |
| Không tiến hành thử nghiệm can thiệp | (5) Đánh giá tác động bằng đối chứng hoặc uplift |
| Chuỗi chỉ bốn học kỳ | (7) Mô hình chuỗi khi có thêm học kỳ |
| Công bằng đo ở ngưỡng 0,5, không phải ngưỡng vận hành; nhóm thiểu số cỡ mẫu nhỏ | (11) Đo lại tại ngưỡng 0,10 và 0,40 · so ở cùng tỷ lệ cảnh báo · tăng cỡ mẫu |
| Thí nghiệm rò rỉ chỉ chạy với một bộ phân loại | (12) Lặp lại thí nghiệm rò rỉ trên nhiều bộ phân loại |

Đóng góp cốt lõi — khung horizon-aware chống rò rỉ — **độc lập với bộ phân loại**, nên mọi hướng trên đều có thể áp dụng trong cùng khung mà không phá vỡ tính không-rò-rỉ.

---

## 5.6 Kết luận

Luận văn xây dựng và đánh giá một mô hình cảnh báo sớm nguy cơ bỏ học cho sinh viên đại học Việt Nam, với trọng tâm không đặt ở việc tối đa hóa chỉ số mà ở việc bảo đảm **con số báo cáo phản ánh đúng năng lực dự báo trong điều kiện triển khai**.

Kết quả cho thấy hai điều. Một là, dự báo sớm khả thi: ngay sau học kỳ đầu tiên, mô hình đã phân biệt được nhóm nguy cơ ở mức đủ để hành động, và chất lượng tăng rõ khi có thêm một học kỳ dữ liệu. Hai là — và đây là điểm nghiên cứu muốn nhấn mạnh — **rò rỉ dữ liệu xảy ra trước khi thuật toán bắt đầu học**: một khi tập đặc trưng đã mang sẵn thông tin của nhãn, thì bất kỳ bộ phân loại đủ mạnh nào cũng có nguy cơ học đúng tín hiệu đó thay vì học quy luật dự báo. Bằng chứng rõ nhất cho điều này không cần tới mô hình nào cả: **riêng một biến `GPA4_2` đã đạt AUC 0,9556**, cao hơn cả mô hình 36 đặc trưng của thiết kế cũ. Và trong nghiên cứu này, cùng một bộ dữ liệu, cùng một thư viện, chỉ khác nhau ở việc **cửa sổ quan sát** có được tách bạch khỏi **chân trời kết quả** hay không, đã tạo ra chênh lệch giữa AUC 0,955 (không bảo vệ được) và 0,915 (bảo vệ được).

Việc chấp nhận con số thấp hơn để đổi lấy con số đúng là lựa chọn trung tâm của nghiên cứu này. Đối với một hệ thống mà đầu ra sẽ quyết định sinh viên nào được nhà trường quan tâm trước, đó là lựa chọn duy nhất có thể biện minh.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- Chương này **không được chứa số liệu mới**; mọi con số phải dẫn lại từ Chương 4 — kiểm tra chéo từng số sau khi Chương 4 chốt.
- Đối chiếu 5.3 với `08_ContributionBoundary.md`, 5.4 với `02_ThreatsToValidity.md`, 5.5 với `04_FutureWork.md` để bảo đảm không mâu thuẫn.
- Sau FINAL FULL RUN: rà lại toàn bộ số trong chương này lần cuối.
- Cân nhắc rút gọn 5.2 nếu tổng độ dài chương vượt quy định của khoa.
