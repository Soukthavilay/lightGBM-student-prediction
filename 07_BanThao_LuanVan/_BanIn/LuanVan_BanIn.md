# Chương 1. Mở đầu

---

## 1.1 Lý do chọn đề tài

Mỗi năm, một bộ phận sinh viên rời giảng đường trước khi hoàn thành chương trình. Với các em, đó là thời gian và chi phí đã bỏ ra mà không thu được bằng cấp; với nhà trường và xã hội, đó là nguồn lực đào tạo đã đầu tư nhưng không kết thành nhân lực có trình độ. Chương 2 sẽ phân tích hệ quả này cùng các hướng nghiên cứu đã có; ở đây chỉ cần ghi nhận rằng đó là một tổn thất đủ lớn để đáng được can thiệp.


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


\newpage

# Chương 2. Tổng quan tài liệu


## 2.1 Dự báo sinh viên bỏ học

### 2.1.1 Bài toán và ý nghĩa

Bỏ học ở bậc đại học là việc sinh viên rời khỏi chương trình đào tạo trước khi hoàn thành. Hệ quả của nó trải trên ba cấp độ. Với **cá nhân**, đó là chi phí thời gian và tài chính đã bỏ ra mà không thu được bằng cấp, kèm theo tác động tâm lý và cơ hội nghề nghiệp bị thu hẹp. Với **nhà trường**, tỷ lệ bỏ học ảnh hưởng tới nguồn thu, chỉ số kiểm định chất lượng và uy tín. Với **xã hội**, đó là sự lãng phí đầu tư công vào giáo dục và tổn thất nguồn nhân lực đã qua đào tạo một phần.


Điểm khiến bài toán này đáng được tiếp cận bằng dữ liệu là: **bỏ học hiếm khi là một sự kiện đột ngột**. Trong phần lớn trường hợp, nó là kết cục của một quá trình tích lũy — kết quả học tập sa sút, số tín chỉ đạt giảm dần, cảnh báo học vụ lặp lại — và quá trình đó để lại dấu vết trong hồ sơ học vụ của nhà trường. Nếu những dấu vết này được nhận diện đủ sớm, nhà trường có cơ hội can thiệp trước khi quyết định rời trường trở nên không thể đảo ngược.

### 2.1.2 Các hướng tiếp cận

Tài liệu về dự báo bỏ học có thể chia thành ba hướng chính.

**Hướng lý thuyết giáo dục** tập trung giải thích *vì sao* sinh viên rời trường. Hai mô hình nền tảng của hướng này là **mô hình hòa nhập của Tinto (1975)**, cho rằng quyết định rời trường phụ thuộc vào mức độ hòa nhập của sinh viên vào đời sống học thuật và xã hội của nhà trường, và **mô hình bỏ học của Bean (1980)**, vốn vay mượn khung lý thuyết về sự rời bỏ tổ chức trong nghiên cứu nhân sự và nhấn mạnh vai trò của các yếu tố ngoài trường học cùng ý định rời bỏ. Hướng này mạnh về khả năng diễn giải nhưng thường không nhằm mục tiêu dự báo ở cấp độ từng cá nhân.

**Hướng thống kê cổ điển** sử dụng hồi quy logistic hoặc phân tích sống còn để ước lượng nguy cơ. Ưu điểm là hệ số có ý nghĩa thống kê rõ ràng và có nền tảng suy luận vững; hạn chế là giả định về dạng hàm và khả năng nắm bắt tương tác phi tuyến còn giới hạn.

**Hướng học máy** coi bài toán như phân loại nhị phân trên dữ liệu hồ sơ sinh viên, sử dụng các mô hình cây, tổ hợp cây hoặc mạng nơ-ron. Đây là hướng chiếm ưu thế trong tài liệu gần đây, và cũng là hướng mà luận văn này theo đuổi.

Về **thời điểm dự báo**, các công trình khác nhau đáng kể: một số dự báo từ dữ liệu tiền nhập học, một số dự báo trong học kỳ dựa trên hoạt động trên hệ thống quản lý học tập, một số khác dự báo sau khi kết thúc một hoặc nhiều học kỳ. Sự khác biệt này quan trọng hơn vẻ ngoài của nó, vì thời điểm dự báo quyết định **thông tin nào được phép sử dụng** — chủ đề sẽ trở lại ở mục 2.4.

### 2.1.3 Hạn chế chung của tài liệu hiện có

Ba hạn chế khiến việc so sánh giữa các công trình trở nên khó khăn.

Thứ nhất, **định nghĩa "bỏ học" không thống nhất**: một số nghiên cứu gộp chung sinh viên chuyển trường, tạm nghỉ và thôi học hẳn; một số tách riêng. Cùng một bộ dữ liệu, hai định nghĩa khác nhau có thể cho ra tỷ lệ nền và kết quả rất khác nhau.

Thứ hai, **thời điểm dự báo ít khi được nêu tường minh**, khiến người đọc khó biết một chỉ số AUC cao là thành tựu của việc dự báo sớm hay chỉ là hệ quả của việc sử dụng dữ liệu muộn.

Thứ ba, **bối cảnh khác nhau** — hệ thống tín chỉ, quy chế học vụ, điều kiện kinh tế – xã hội — làm cho kết quả từ một quốc gia khó chuyển trực tiếp sang quốc gia khác.

### 2.1.4 Chuyển tiếp

Dự báo bỏ học không tồn tại biệt lập mà là một ứng dụng cụ thể của một lĩnh vực rộng hơn: khai phá dữ liệu giáo dục. Đặt bài toán trong khung này giúp thấy rõ bỏ học, giữ chân người học và thành công học tập là ba mặt của cùng một câu hỏi, đồng thời cho phép kế thừa các phương pháp và chuẩn mực đánh giá đã được lĩnh vực đó xây dựng.


## 2.2 Khai phá dữ liệu giáo dục

### 2.2.1 Lĩnh vực và các bài toán liên quan

Khai phá dữ liệu giáo dục (Educational Data Mining) và học phân tích (Learning Analytics) là hai lĩnh vực gần nhau, cùng hướng tới việc sử dụng dữ liệu người học để hiểu và cải thiện quá trình đào tạo. Trong khung này, dự báo bỏ học không phải một bài toán biệt lập mà là **một mặt của cụm câu hỏi về hành trình học tập**: dự báo bỏ học (ai có nguy cơ rời trường), giữ chân người học (làm gì để họ ở lại), và thành công học tập (điều gì giúp họ hoàn thành tốt). Ba câu hỏi này chia sẻ phần lớn nguồn dữ liệu và phương pháp; khác biệt chủ yếu nằm ở biến mục tiêu.

Việc luận văn chọn tập trung vào **bỏ học** thay vì kết quả học tập nói chung xuất phát từ tính chất của can thiệp: điểm số có thể cải thiện dần trong nhiều học kỳ, nhưng việc rời trường là một sự kiện **gần như không đảo ngược** — nên giá trị của việc phát hiện sớm ở đây cao hơn rõ rệt.

### 2.2.2 Các nguồn dữ liệu và đặc thù của chúng

Tài liệu trong lĩnh vực này thường khai thác ba nhóm dữ liệu:

1. **Hồ sơ học vụ hành chính** — thông tin nhân khẩu, điểm tuyển sinh, kết quả từng học kỳ, tín chỉ đăng ký và đạt, cảnh báo học vụ. Đây là nguồn phổ biến nhất vì mọi trường đều lưu trữ.
2. **Nhật ký hệ thống quản lý học tập (LMS)** — số lần đăng nhập, thời lượng truy cập, tương tác với tài liệu. Nguồn này giàu tín hiệu hành vi nhưng chỉ có ở những trường số hóa mạnh, và mức độ sử dụng biến thiên lớn giữa các ngành.
3. **Khảo sát tâm lý – kinh tế xã hội** — động lực học tập, hoàn cảnh gia đình, áp lực tài chính. Có giá trị giải thích cao nhưng tốn kém để thu thập và thường không sẵn có.

**Phạm vi dữ liệu của luận văn cần được nêu rõ ngay từ đây:** nghiên cứu sử dụng **duy nhất nhóm thứ nhất** — hồ sơ học vụ hành chính. Lựa chọn này có mặt được và mặt mất. Mặt được là **khả năng áp dụng rộng**: mọi trường đại học đều có sẵn loại dữ liệu này, nên quy trình đề xuất không đòi hỏi hạ tầng đặc biệt. Mặt mất là mô hình **không quan sát được** các yếu tố hành vi và hoàn cảnh cá nhân, vốn được ghi nhận là quan trọng trong bối cảnh Đông Nam Á; hạn chế này được nêu lại ở phần bàn luận.

### 2.2.3 Vì sao dữ liệu giáo dục có đặc thù riêng

Bốn tính chất của dữ liệu học vụ định hình cách tiếp cận mô hình hóa:

- **Dạng bảng, hỗn hợp kiểu** — vừa có biến số, vừa có biến hạng mục (ngành học, khu vực, dân tộc).
- **Có cấu trúc thời gian rời rạc** — dữ liệu đến theo từng học kỳ, không phải chuỗi liên tục; số mốc thời gian thường ít.
- **Nhiều giá trị thiếu, và giá trị thiếu *có nghĩa*** — một học kỳ không có dữ liệu thường không phải lỗi ghi chép mà phản ánh trạng thái thực của sinh viên.
- **Mất cân bằng lớp** — nhóm bỏ học luôn là thiểu số.

### 2.2.4 Hạn chế của tài liệu trong lĩnh vực

Điểm hạn chế nổi bật khi tổng hợp tài liệu là **khả năng so sánh giữa các công trình rất thấp**: định nghĩa biến mục tiêu, nguồn dữ liệu, cách xây dựng đặc trưng, giao thức đánh giá và thời điểm dự báo đều khác nhau và thường không được báo cáo đầy đủ. Hệ quả là một chỉ số hiệu năng đứng một mình gần như không mang thông tin nếu thiếu bối cảnh đi kèm — điều này cũng lý giải vì sao luận văn dành trọng tâm cho **giao thức đánh giá** chứ không chỉ cho con số cuối cùng.


### 2.2.5 Chuyển tiếp

Bốn đặc thù nêu ở mục 2.2.3 — dữ liệu dạng bảng với kiểu hỗn hợp, cấu trúc thời gian rời rạc và ngắn, giá trị thiếu mang ý nghĩa, và mất cân bằng lớp — trực tiếp thu hẹp không gian lựa chọn mô hình. Mục tiếp theo trình bày vì sao, trong không gian đó, các mô hình cây tăng cường độ dốc, và cụ thể là LightGBM, là lựa chọn phù hợp với nghiên cứu này.


## 2.3 LightGBM và cơ sở lựa chọn mô hình

### 2.3.1 Cây tăng cường độ dốc — định vị trong họ mô hình

Tăng cường độ dốc (gradient boosting) xây dựng mô hình theo hướng cộng dồn: mỗi cây quyết định mới được huấn luyện để giảm phần dư mà tổ hợp các cây trước còn để lại. Khác với rừng ngẫu nhiên vốn huấn luyện các cây độc lập rồi lấy trung bình, gradient boosting huấn luyện **tuần tự và có định hướng** — nhờ đó thường đạt độ chính xác cao hơn trên dữ liệu dạng bảng, đổi lại nhạy cảm hơn với siêu tham số. Trong khoảng một thập kỷ trở lại đây, họ mô hình này, với ba hiện thực tiêu biểu là XGBoost, LightGBM và CatBoost, đã trở thành lựa chọn phổ biến cho bài toán phân loại trên dữ liệu bảng.

### 2.3.2 LightGBM

LightGBM (Ke và cộng sự, 2017) là một hiện thực gradient boosting hướng tới tốc độ và hiệu quả bộ nhớ. Ở mức khái quát, hai đặc điểm đủ để hiểu vị trí của nó trong luận văn này: mô hình dùng **biểu đồ tần suất (histogram)** để rời rạc hóa giá trị liên tục khi tìm điểm chia, và phát triển cây theo hướng **leaf-wise** — mở rộng lá có mức giảm mất mát lớn nhất, thay vì mở rộng đều theo tầng. Các tối ưu hóa chi tiết khác của thư viện nằm ngoài phạm vi luận văn và có thể tham khảo trực tiếp ở công trình gốc.

### 2.3.3 Vì sao phù hợp với dữ liệu của nghiên cứu này

Bốn đặc điểm của bộ dữ liệu quyết định lựa chọn mô hình:

1. **Dữ liệu dạng bảng, quy mô trung bình.** Tập phân tích gồm 7.367 sinh viên với 25 đặc trưng ở chân trời HK1, và 7.034 sinh viên với 36 đặc trưng ở chân trời HK1-2 (trong đó 6 đặc trưng hạng mục). Đây là quy mô mà mô hình cây tỏ ra thích hợp, và LightGBM hỗ trợ đặc trưng hạng mục trực tiếp, không bắt buộc mã hóa one-hot.
2. **Giá trị thiếu là *có chủ đích*, không phải lỗi dữ liệu.** Thiết kế đặc trưng của luận văn cố ý gán `NaN` cho các học kỳ mà sinh viên không hoạt động (8 cột chứa `NaN` ở cả hai chân trời), nhằm tách bạch "không có dữ liệu" khỏi "trượt toàn bộ". LightGBM học hướng đi mặc định cho `NaN` ngay ở mức thuật toán, cho phép **giữ nguyên sự phân biệt này** — trong khi các mô hình nền phải điền khuyết (thực hiện trong từng fold để tránh rò rỉ).
3. **Tương tác phi tuyến giữa các học kỳ.** Nguy cơ bỏ học không phụ thuộc tuyến tính vào từng chỉ số đơn lẻ mà vào tương tác giữa chúng (ví dụ điểm trung bình thấp *kết hợp* tỷ lệ tín chỉ đạt giảm dần). Mô hình cây nắm bắt các tương tác này mà không cần đặc tả trước.
4. **Mất cân bằng lớp.** Tỷ lệ bỏ học sau chân trời là 11,5% (HK1) và 7,4% (HK1-2) — càng dự báo muộn, lớp dương càng hiếm. LightGBM cho phép bù mất cân bằng (`is_unbalance`) tính **trên đúng phần dữ liệu đang khớp**, nhất quán với nguyên tắc "mọi thao tác đều thực hiện trong fold" của luận văn.

Ngoài ra, là mô hình cây, LightGBM tương thích với `TreeExplainer` của SHAP, cho phép tính giá trị SHAP nhanh và chính xác — điều kiện cần cho mục tiêu xây dựng một hệ thống cảnh báo mà cố vấn học tập có thể hiểu và tin tưởng (xem 2.7).

### 2.3.4 Bằng chứng phản biện: không mô hình nào vượt trội trong mọi bối cảnh

Bảng 2.1 đối chiếu bốn lựa chọn thay thế thường được nêu ra, cùng lập luận ủng hộ và lý do chưa phù hợp với bối cảnh của nghiên cứu này.

**Bảng 2.1.** Các lựa chọn mô hình thay thế và cơ sở phản biện. *(Nguồn: tác giả tổng hợp.)*

| Lựa chọn thay thế | Lập luận ủng hộ nó | Vì sao chưa phù hợp ở đây |
|---|---|---|
| XGBoost / CatBoost | Một số benchmark ghi nhận ổn định hơn LightGBM trên vài bộ dữ liệu, nhất là **trước** khi tinh chỉnh | Sau tinh chỉnh, khác biệt giữa ba thư viện thường thu hẹp đáng kể |
| Học sâu cho dữ liệu bảng (FT-Transformer, TabR) | Liên tục được đề xuất với tuyên bố cạnh tranh được | Grinsztajn và cộng sự (2022) khảo sát 45 bộ dữ liệu: mô hình cây vẫn dẫn đầu ở quy mô ~10.000 mẫu — đúng phạm vi luận văn |
| Mô hình chuỗi (LSTM/Transformer) | Nắm bắt phụ thuộc thời gian, phù hợp khi chuỗi quan sát đủ dài | Chuỗi ở đây chỉ gồm **4 học kỳ** — quá ngắn để phát huy lợi thế, trong khi nguy cơ quá khớp tăng |
| Hồi quy logistic | Rất dễ diễn giải | Giả định tuyến tính, khó nắm tương tác giữa các học kỳ |

Tổng hợp lại, các bằng chứng trên cho thấy **không có mô hình nào vượt trội trong mọi bối cảnh**; hiệu năng tương đối phụ thuộc vào đặc điểm dữ liệu, quy mô mẫu và mục tiêu sử dụng.

### 2.3.5 Kết luận lựa chọn

Do đó, luận văn **không chọn LightGBM vì cho rằng đây là mô hình tốt nhất trong mọi bối cảnh**, mà vì nó phù hợp đồng thời với ba yếu tố: **đặc điểm dữ liệu** (dạng bảng, quy mô trung bình, giá trị thiếu có chủ đích, mất cân bằng lớp), **mục tiêu giải thích kết quả** (tương thích SHAP để phục vụ cố vấn học tập), và **khung đánh giá mà nghiên cứu này đề xuất** (chi phí tính toán chấp nhận được cho kiểm định chéo lặp lại, bootstrap và nested cross-validation).

Điều quan trọng cần nhấn mạnh: **đóng góp của luận văn không nằm ở việc lựa chọn bộ phân loại.** Khung thiết kế dữ liệu chống rò rỉ trình bày ở mục tiếp theo **độc lập với thuật toán** — có thể áp dụng nguyên vẹn cho XGBoost, CatBoost hay bất kỳ mô hình phân loại nào khác. Nếu một nghiên cứu tương lai chứng minh một thư viện khác phù hợp hơn với dữ liệu này, kết luận phương pháp luận của luận văn vẫn giữ nguyên giá trị; chỉ bộ phân loại được thay thế.

### 2.3.6 Chuyển tiếp

Tuy nhiên, chọn được mô hình phù hợp mới chỉ là một nửa vấn đề. **Nếu thiết kế dữ liệu không đúng, mô hình vẫn có thể học từ những thông tin rò rỉ từ tương lai** — và nghịch lý là, chính năng lực khớp mẫu mạnh của các mô hình như LightGBM lại khiến chúng khai thác các đặc trưng rò rỉ triệt để hơn, đẩy chỉ số đánh giá lên cao một cách giả tạo. Điều này đưa ta tới vấn đề cốt lõi của luận văn: rò rỉ dữ liệu.


## 2.4 Rò rỉ dữ liệu và nguyên lý Landmarking (Data Leakage and Landmarking)

Mục này trình bày nền tảng học thuật cho đóng góp trung tâm của luận văn. Chúng tôi lần lượt định nghĩa rò rỉ dữ liệu, chỉ ra vì sao nó đặc biệt nguy hiểm trong dự báo bỏ học sớm, và giới thiệu nguyên lý *landmarking* như một giải pháp có nền tảng thống kê. Cần nói rõ ngay từ đầu để người đọc thấy mục này không chỉ thuần lý thuyết: luận văn khắc phục vấn đề rò rỉ bằng cách xây dựng tập dữ liệu **theo chân trời thời gian** (hàm `horizon_dataset()`) — chỉ dùng dữ liệu đến học kỳ *h* trên đúng nhóm sinh viên còn theo học — vốn là một hiện thực hóa trực tiếp của nguyên lý landmarking trình bày ở mục 2.4.3.

### 2.4.1 Khái niệm rò rỉ dữ liệu

Trong khai phá dữ liệu và học máy, **rò rỉ dữ liệu** (data leakage) được Kaufman và cộng sự (2012) định nghĩa là việc đưa vào mô hình những thông tin về biến mục tiêu mà lẽ ra *không khả dụng một cách hợp lệ* tại thời điểm dự báo. Các tác giả xếp rò rỉ vào nhóm những sai lầm nghiêm trọng và khó phát hiện nhất của khai phá dữ liệu, bởi nó không làm mô hình "hỏng" mà ngược lại làm mô hình *có vẻ tốt lên*: các chỉ số đánh giá trên tập kiểm tra bị nâng lên cao, trong khi năng lực thật khi triển khai lại thấp hơn nhiều.

Kaufman và cộng sự (2012) phân biệt hai dạng chính. Thứ nhất là **rò rỉ mục tiêu** (target leakage), khi một đặc trưng thực chất là hệ quả của nhãn chứ không phải nguyên nhân/tín hiệu có trước nhãn. Thứ hai là **rò rỉ theo thời gian** (temporal leakage), khi đặc trưng chứa thông tin chỉ tồn tại *sau* thời điểm mà dự báo cần được đưa ra. Chẳng hạn, nếu ta muốn dự báo ngay từ cuối học kỳ 1 nhưng lại đưa GPA của học kỳ 4 — hoặc trạng thái tốt nghiệp — vào làm đặc trưng, thì mô hình đã "nhìn thấy tương lai": đó là một trường hợp rò rỉ theo thời gian điển hình. Đối với các bài toán mang bản chất thời gian — mà dự báo bỏ học là một ví dụ điển hình — rò rỉ theo thời gian là mối đe dọa thường trực.

### 2.4.2 Vì sao rò rỉ đặc biệt nghiêm trọng trong dự báo bỏ học sớm

Mục tiêu của một hệ thống *cảnh báo sớm* là: tại một thời điểm nhất định trong quá trình học (ví dụ cuối học kỳ *h*), dự báo những sinh viên **còn đang theo học** nào có nguy cơ bỏ học *về sau*. Bản chất này đặt ra một ràng buộc chặt: mọi đặc trưng đưa vào mô hình phải khả dụng *tính đến* thời điểm *h*, và quần thể phân tích phải là những sinh viên còn "trong diện rủi ro" tại thời điểm đó.

Trên thực tế, nhiều công trình vi phạm ràng buộc này theo hai cách. (i) Về đặc trưng: sử dụng các biến chỉ có được ở *cuối* chương trình — điểm trung bình tích lũy toàn khóa, tổng số môn trượt, hay trạng thái đăng ký/tốt nghiệp — vốn là hệ quả trực tiếp của việc sinh viên đã (hoặc chưa) bỏ học. (ii) Về quần thể: huấn luyện và đánh giá trên toàn bộ khóa, kể cả những sinh viên đã rời trường *trước* thời điểm *h*; với nhóm này, các đặc trưng của học kỳ *h* (GPA bằng 0, không đăng ký tín chỉ) không còn là tín hiệu dự báo mà chính là dấu vết của nhãn.

Hậu quả đã được ghi nhận rõ trong tài liệu. Một số nghiên cứu báo cáo các chỉ số gần như hoàn hảo (F1 và AUC xấp xỉ 1,0) — điều gần như bất khả thi với dữ liệu giáo dục vốn nhiều nhiễu; rà soát sau đó cho thấy nguyên nhân là các biến hậu-kết-quả (trạng thái đăng ký, cờ tốt nghiệp) đã lọt vào tập đặc trưng và mã hóa gần như trực tiếp cho nhãn. Nói cách khác, mô hình không *dự báo* bỏ học mà chỉ *ghi lại hậu quả* của nó, khiến kết quả trông chính xác hơn nhiều so với hiệu năng thật khi vận hành.

Hình 2.1 minh họa ràng buộc thời gian này: chỉ dữ liệu trong *cửa sổ quan sát* (đến học kỳ mốc *h*) mới được phép dùng để dự báo biến cố nằm trong *chân trời kết quả* (sau *h*), và mọi đặc trưng chạm tới học kỳ sau *h* đều là rò rỉ.

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/fig_2_4_landmark_horizon.png)

**Hình 2.1.** Minh họa cửa sổ quan sát và chân trời kết quả. (a) Chỉ dùng dữ liệu đến học kỳ mốc *h* để dự báo biến cố xảy ra sau *h*. (b) Cách xây đặc trưng đúng (chỉ HK1..*h* → dự báo) so với cách rò rỉ (dùng cả HK1–HK4 rồi dự báo tại thời điểm *h*). *(Nguồn: tác giả.)*


### 2.4.3 Landmarking như một giải pháp có nền tảng thống kê

Vấn đề "dự báo một biến cố tương lai chỉ dựa trên thông tin đến một thời điểm quan sát" không mới; nó đã được nghiên cứu bài bản trong phân tích lịch sử biến cố (event history / survival analysis). van Houwelingen (2007) đề xuất phương pháp **landmarking**: chọn một *thời điểm mốc* (landmark time), giới hạn tập phân tích về đúng những cá thể **còn trong diện rủi ro** tại mốc đó, và xây dựng mô hình dự báo chỉ dựa trên thông tin có được *tính đến* mốc. Bằng cách này, mô hình luôn được ước lượng trên đúng quần thể và đúng tập thông tin mà nó sẽ gặp khi triển khai, qua đó loại bỏ rò rỉ theo thời gian *ngay từ khâu thiết kế dữ liệu* thay vì sửa chữa về sau.

Mặc dù landmarking ra đời trong phân tích sống còn, nguyên lý của nó chuyển giao tự nhiên sang bài toán dự báo bỏ học, bởi cả hai về bản chất đều là bài toán *thời gian-đến-biến-cố* (time-to-event): điều quan tâm không chỉ là *liệu* biến cố (tử vong hay bỏ học) có xảy ra, mà còn là *khi nào* nó xảy ra, và ở mỗi thời điểm luôn tồn tại một nhóm cá thể "còn trong diện rủi ro" thay đổi theo thời gian. Chính sự tương đồng cấu trúc này biện minh cho việc mượn khung landmarking từ y sinh để áp dụng cho giáo dục.

Cùng tinh thần đó, các khuyến nghị báo cáo minh bạch mô hình dự báo (TRIPOD; Collins và cộng sự, 2015) nhấn mạnh việc phân định rõ ràng thời điểm dự báo, thông tin khả dụng tại thời điểm đó, và chân trời kết quả — chính là sự tách bạch giữa **cửa sổ quan sát** (observation window) và **chân trời kết quả** (outcome horizon).

### 2.4.4 Định vị đóng góp của luận văn

Trên nền tảng trên, kỹ thuật **đặc trưng theo chân trời thời gian** (horizon-aware feature engineering) đề xuất trong luận văn **không nên hiểu là một thủ thuật kỹ thuật được đặt tên mới**, mà là **sự hiện thực hóa nguyên lý landmarking** (van Houwelingen, 2007) cho bài toán dự báo bỏ học đại học: với mỗi chân trời *h*, tập dữ liệu chỉ giữ những sinh viên còn hoạt động tại học kỳ *h* và chỉ dùng đặc trưng xây từ các học kỳ 1..*h*, trong khi nhãn được định nghĩa là "bỏ học sau cuối học kỳ *h*". Cách tiếp cận này vừa tôn trọng ràng buộc triển khai thực tế, vừa phù hợp với khuyến nghị minh bạch của TRIPOD, và trực tiếp khắc phục hạn chế (1) sẽ được tổng hợp ở mục 2.9.


## 2.5 Hiệu chỉnh xác suất và phân tích đường cong quyết định

### 2.5.1 Phân biệt tốt không đồng nghĩa với xác suất đáng tin

Các chỉ số phổ biến nhất trong dự báo bỏ học — AUC, F1, độ chính xác — đều đo **khả năng phân biệt** (discrimination): mô hình có xếp sinh viên nguy cơ cao lên trên sinh viên nguy cơ thấp hay không. Tuy nhiên, AUC chỉ phụ thuộc vào **thứ tự** của các điểm số, không phụ thuộc vào **giá trị tuyệt đối** của chúng. Hai mô hình có cùng AUC có thể đưa ra những xác suất rất khác nhau: một mô hình nói "nguy cơ 12%" và một mô hình nói "nguy cơ 45%" cho cùng một sinh viên vẫn có thể xếp hạng giống hệt nhau.

Sự phân biệt này trở nên quan trọng ngay khi xác suất được dùng để **ra quyết định**. Nếu nhà trường muốn đặt quy tắc "liên hệ cố vấn học tập khi nguy cơ vượt 20%", thì con số 20% phải có ý nghĩa thực: trong nhóm sinh viên được mô hình gán nguy cơ 20%, phải có khoảng 20% thực sự bỏ học. Tính chất này gọi là **hiệu chỉnh** (calibration), và nó độc lập với khả năng phân biệt.

### 2.5.2 Các phương pháp hiệu chỉnh

Hai phương pháp hậu xử lý được dùng rộng rãi. **Hiệu chỉnh Platt** (sigmoid) khớp một hàm logistic từ điểm số của mô hình sang xác suất, phù hợp khi độ méo có dạng sigmoid và dữ liệu hiệu chỉnh ít. **Hồi quy đẳng hướng** (isotonic regression), do Zadrozny & Elkan (2002) đưa vào bài toán này, là phương pháp phi tham số tìm hàm đơn điệu từng khúc tối ưu; linh hoạt hơn nhưng cần nhiều dữ liệu hơn và có nguy cơ quá khớp ở mẫu nhỏ.

Điểm đặc biệt liên quan tới luận văn nằm ở khảo sát của **Niculescu-Mizil & Caruana (2005)**: các phương pháp lề tối đa, trong đó có **cây tăng cường** (boosted trees), có xu hướng đẩy khối xác suất ra xa hai đầu 0 và 1, tạo ra méo dạng sigmoid đặc trưng. Nói cách khác, **chính họ mô hình mà luận văn sử dụng (LightGBM) là họ mô hình được biết là hiệu chỉnh kém nếu không xử lý** — đây là lý do trực tiếp để đưa bước hiệu chỉnh vào quy trình, chứ không phải một thao tác thêm cho đủ.

Vấn đề này không chỉ tồn tại ở các mô hình cổ điển. **Guo và cộng sự (2017)** cho thấy các mạng nơ-ron hiện đại, dù chính xác hơn thế hệ trước, lại **hiệu chỉnh kém hơn**, và đề xuất temperature scaling như một giải pháp đơn giản. Kết luận chung: độ chính xác tăng không tự động kéo theo xác suất đáng tin.

### 2.5.3 Đo lường chất lượng hiệu chỉnh

- **Brier score** — sai số bình phương trung bình giữa xác suất dự báo và nhãn thực; là một *proper scoring rule*, đo đồng thời cả khả năng phân biệt lẫn độ hiệu chỉnh. Giá trị càng nhỏ càng tốt, nhưng phụ thuộc tỷ lệ lớp nên **không so sánh trực tiếp được giữa các bộ dữ liệu có tỷ lệ khác nhau**.
- **Biểu đồ độ tin cậy** (reliability diagram) — vẽ tần suất thực tế theo xác suất dự báo; trực quan nhưng phụ thuộc cách chia bin.
- **ECE** (Expected Calibration Error) — trung bình có trọng số của chênh lệch |tần suất thực − xác suất dự báo| trên từng bin.

ECE cần được diễn giải thận trọng vì ba lý do. Thứ nhất, giá trị phụ thuộc **số bin và cách chia bin** (đều theo độ rộng hay theo phân vị); các lựa chọn khác nhau cho ra con số khác nhau trên cùng dữ liệu. Thứ hai, ECE **không phải proper scoring rule** — một mô hình luôn dự báo tỷ lệ nền có thể đạt ECE rất thấp dù vô dụng. Thứ ba, ở cỡ mẫu hữu hạn, ECE có một **"sàn nhiễu"**: ngay cả một mô hình hiệu chỉnh hoàn hảo cũng cho ECE dương do dao động lấy mẫu. Vì vậy, một giá trị ECE rất nhỏ chỉ nên được diễn giải là *"không phát hiện được sai lệch hiệu chỉnh"*, **không phải** *"hiệu chỉnh gần như hoàn hảo"*.

### 2.5.4 Từ xác suất tới quyết định: đường cong quyết định

Ngay cả khi xác suất đã đáng tin, vẫn còn một câu hỏi: **dùng mô hình có lợi hơn không dùng hay không?** Phân tích đường cong quyết định (Decision Curve Analysis) của **Vickers & Elkin (2006)** trả lời câu hỏi này bằng khái niệm **lợi ích ròng** (net benefit):

$$NB = \frac{TP}{n} - \frac{FP}{n}\cdot\frac{p_t}{1-p_t}$$

trong đó $p_t$ là **ngưỡng xác suất** mà tại đó người ra quyết định thấy việc can thiệp là đáng. Khi một giá trị $p_t$ cụ thể được chọn để hệ thống vận hành, luận văn gọi đó là **ngưỡng vận hành** (operating point) — thuật ngữ này được dùng thống nhất từ đây tới hết Chương 5. Ý tưởng cốt lõi: $p_t$ không phải tham số kỹ thuật mà là **phát biểu về sự đánh đổi chi phí** — chọn $p_t = 0{,}2$ tương đương nói "tôi sẵn sàng can thiệp 4 trường hợp không cần thiết để bắt được 1 trường hợp thật".

Đường cong quyết định vẽ NB của mô hình theo dải $p_t$, so với hai chiến lược tham chiếu: **can thiệp tất cả** và **không can thiệp ai**. Mô hình chỉ thực sự hữu ích trong dải ngưỡng mà đường của nó nằm trên cả hai đường tham chiếu.

Cách tiếp cận này đặc biệt phù hợp với bối cảnh giáo dục, nơi nguồn lực cố vấn học tập là hữu hạn: câu hỏi thực tế không phải "mô hình chính xác bao nhiêu phần trăm" mà "với năng lực tiếp cận *k* sinh viên mỗi học kỳ, dùng mô hình có giúp tiếp cận đúng người hơn cách làm hiện tại không". Ngưỡng $p_t$ do đó trở thành cầu nối giữa mô hình thống kê và chính sách hỗ trợ sinh viên — ý tưởng sẽ được khai thác trong thiết kế cảnh báo hai tầng ở mục 2.8.

### 2.5.5 Khoảng trống trong tài liệu dự báo bỏ học

Mặc dù hiệu chỉnh và lợi ích quyết định là điều kiện cần để một mô hình rủi ro dùng được trong thực tế, **trong số các công trình được khảo sát**, chỉ một số rất ít có đánh giá hiệu chỉnh xác suất, và hầu như không công trình nào phân tích lợi ích ròng của quyết định; đại đa số **chỉ báo cáo các chỉ số phân biệt** (AUC, F1). Hệ quả là nhiều mô hình được công bố là "chính xác" nhưng chưa từng được kiểm chứng rằng xác suất của chúng có thể dùng để quyết định ai cần hỗ trợ trước.

### 2.5.6 Chuyển tiếp

Tuy nhiên, một xác suất được hiệu chỉnh tốt **trên tổng thể** vẫn có thể sai lệch một cách hệ thống **giữa các nhóm** sinh viên khác nhau — theo giới tính, khu vực hay dân tộc. Vì đây là mô hình dùng để phân bổ nguồn lực hỗ trợ, chênh lệch như vậy mang hệ quả đạo đức trực tiếp. Do đó, sau độ tin cậy tổng thể, cần xét tới tính công bằng.


## 2.6 Tính công bằng của mô hình dự báo bỏ học

### 2.6.1 Công bằng nghĩa là gì trong bài toán này

Trong dự báo bỏ học, mô hình không đưa ra phán quyết trừng phạt mà **phân bổ một nguồn lực khan hiếm**: sự chú ý của cố vấn học tập. Vì vậy khái niệm công bằng ở đây mang tính **phân bổ** (allocative): câu hỏi không phải "mô hình có đối xử tệ với nhóm nào không", mà là **"cơ hội được phát hiện và hỗ trợ kịp thời có phân bố đều giữa các nhóm sinh viên hay không"**.

Điều này dẫn tới một quan sát quan trọng về **tính bất đối xứng của sai sót**. Một *âm tính giả* (sinh viên có nguy cơ nhưng mô hình bỏ sót) đồng nghĩa với việc em đó không nhận được hỗ trợ và có thể rời trường — thiệt hại lớn và khó đảo ngược. Một *dương tính giả* (sinh viên được cảnh báo nhưng thực ra không bỏ học) chỉ tiêu tốn một buổi tư vấn không cần thiết. Do đó, trong bối cảnh cảnh báo sớm, **chênh lệch về tỷ lệ bỏ sót giữa các nhóm là mối lo ngại hàng đầu**, quan trọng hơn chênh lệch về tỷ lệ báo động giả.

Bối cảnh Việt Nam làm cho câu hỏi này cụ thể hơn: các thuộc tính như **giới tính** và **dân tộc** (đa số Kinh so với các dân tộc thiểu số) là những trục phân nhóm có ý nghĩa chính sách, nơi chênh lệch trong hệ thống hỗ trợ có thể khuếch đại bất bình đẳng vốn có.

### 2.6.2 Đo bằng cách nào

Tài liệu về công bằng thuật toán đề xuất nhiều tiêu chí nhóm khác nhau, trong đó ba nhóm phổ biến nhất là: **cân bằng hiệu năng** (mô hình phân biệt tốt như nhau ở mọi nhóm), **cơ hội bình đẳng** (equal opportunity — tỷ lệ phát hiện đúng, tức TPR/độ nhạy, ngang nhau giữa các nhóm), và **cân bằng tỷ lệ sai** (chênh lệch tỷ lệ dương tính giả hoặc âm tính giả giữa các nhóm). Cần lưu ý rằng các tiêu chí này **nhìn chung không thể thỏa mãn đồng thời** khi tỷ lệ nền giữa các nhóm khác nhau; do đó việc chọn tiêu chí là một quyết định có tính chuẩn tắc, phải được nêu rõ chứ không thể coi là kỹ thuật thuần túy.

Luận văn này sử dụng **hai thước đo, đo trên cùng bộ xác suất đã hiệu chỉnh**:

1. **AUC theo nhóm, kèm khoảng tin cậy bootstrap** — kiểm tra xem mô hình có *phân biệt* kém hơn ở nhóm nào không.
2. **Độ nhạy (recall) theo nhóm, đo tại một ngưỡng cố định** — **phản ánh** tiêu chí *cơ hội bình đẳng* (equal opportunity), trả lời trực tiếp câu hỏi "tỷ lệ sinh viên có nguy cơ được phát hiện có ngang nhau giữa các nhóm không". Cần lưu ý *cơ hội bình đẳng* là một **tính chất của hệ thống tại một ngưỡng đã chọn**, không phải bản thân một chỉ số; độ nhạy theo nhóm là đại lượng dùng để **kiểm tra** tính chất đó, và kết luận luôn gắn với đúng ngưỡng đã dùng để đo. Giá trị ngưỡng cụ thể được nêu ở mục 3.9.

Hai thước đo này được chọn vì chúng **bổ sung cho nhau ở hai tầng khác nhau**: AUC phản ánh khả năng phân biệt **độc lập với ngưỡng**, cho biết mô hình có xếp hạng nguy cơ kém chính xác hơn ở một nhóm nào đó hay không, bất kể chính sách cảnh báo được đặt ở đâu; trong khi độ nhạy tại ngưỡng vận hành phản ánh **hành vi thực tế của hệ thống khi được triển khai**, tức là tỷ lệ sinh viên có nguy cơ thực sự được đưa vào danh sách can thiệp. Một mô hình có thể công bằng ở tầng thứ nhất nhưng vẫn tạo ra chênh lệch ở tầng thứ hai; do đó chỉ đo một trong hai là chưa đủ.

Hai thuộc tính nhạy cảm được xét là **giới tính** và **dân tộc**; các nhóm có dưới 50 quan sát bị loại khỏi phân tích vì ước lượng không đủ tin cậy.

Cần phát biểu rõ phạm vi của phần này để tránh bị đọc quá rộng: **mục tiêu của luận văn không phải đánh giá mọi định nghĩa công bằng đã được đề xuất trong tài liệu về AI**, mà là kiểm tra xem hiệu năng của hệ thống có thay đổi đáng kể giữa các nhóm người học hay không, theo đúng những chỉ số phục vụ trực tiếp cho việc triển khai. Các tiêu chí khác — chẳng hạn *demographic parity* hay *equalized odds* — không được báo cáo, không phải vì chúng kém quan trọng, mà vì mỗi tiêu chí trả lời một câu hỏi chuẩn tắc khác nhau và việc chọn tiêu chí phải xuất phát từ mục đích sử dụng. Ở đây mục đích sử dụng là **phân bổ một nguồn lực hỗ trợ khan hiếm**, nên hai câu hỏi đáng quan tâm nhất là "mô hình có xếp hạng nguy cơ kém chính xác hơn ở nhóm nào không" (AUC theo nhóm) và "tỷ lệ sinh viên có nguy cơ được đưa vào danh sách can thiệp có ngang nhau không" (độ nhạy theo nhóm, phản ánh *cơ hội bình đẳng*) — đúng hai thước đo đã chọn.

Cần nêu rõ **giới hạn phạm vi**: luận văn **đo lường và báo cáo** chênh lệch giữa các nhóm, **chưa áp dụng kỹ thuật giảm thiểu** (mitigation) như adversarial debiasing hay hiệu chỉnh theo nhóm. Đây là ranh giới có chủ ý, được nêu lại ở phần hạn chế và hướng nghiên cứu tương lai.

### 2.6.3 Hạn chế cần lưu ý khi diễn giải

Thứ nhất, **so sánh ở một ngưỡng cố định có thể gây hiểu nhầm khi tỷ lệ nền khác nhau**: nếu hai nhóm có tỷ lệ bỏ học nền khác nhau, độ nhạy tại cùng một ngưỡng sẽ khác nhau ngay cả với một mô hình hiệu chỉnh hoàn hảo. Khi diễn giải, phải đọc chênh lệch độ nhạy **cùng với** tỷ lệ nền của từng nhóm.

Thứ hai, **nhóm thiểu số thường có cỡ mẫu nhỏ**, kéo theo khoảng tin cậy rộng; một chênh lệch điểm ước lượng lớn vẫn có thể không đủ bằng chứng thống kê. Kết luận về nhóm nhỏ phải dè dặt.

Thứ ba, tồn tại lo ngại phổ biến rằng cải thiện công bằng sẽ làm giảm độ chính xác. Tuy nhiên, bằng chứng thực nghiệm quy mô lớn trong lĩnh vực chính sách công của **Rodolfa, Lamba & Ghani (2021)** cho thấy đánh đổi này **thường không đáng kể** trên thực tế — nghĩa là việc đưa đánh giá công bằng vào quy trình không nhất thiết phải trả giá bằng hiệu năng.

### 2.6.4 Khoảng trống trong tài liệu dự báo bỏ học

Trong số các công trình được khảo sát, chỉ một số ít có phân tích công bằng; phần lớn báo cáo hiệu năng tổng thể mà không tách theo nhóm. Trong nhóm ít ỏi có xét công bằng, hiếm công trình nào đồng thời kiểm tra xem biện pháp can thiệp vào ngưỡng hay trọng số có **phá vỡ độ hiệu chỉnh** của xác suất hay không — trong khi đây là ràng buộc trực tiếp: một xác suất đã mất tính hiệu chỉnh thì không còn dùng được cho phân tích lợi ích quyết định ở mục 2.5.

### 2.6.5 Vì sao phải đo trước khi triển khai

Ba lý do khiến việc đánh giá công bằng là **điều kiện tiên quyết**, không phải bước tùy chọn hậu kỳ.

Thứ nhất, mô hình này được thiết kế để **phân bổ nguồn lực hỗ trợ thật**; một chênh lệch độ nhạy giữa các nhóm sẽ chuyển hóa trực tiếp thành chênh lệch về cơ hội được giúp đỡ.

Thứ hai, chênh lệch **không thể phát hiện được từ chỉ số tổng thể**: một mô hình có AUC cao trên toàn bộ dữ liệu vẫn có thể bỏ sót một nhóm cụ thể một cách hệ thống. Chỉ khi tách theo nhóm, vấn đề mới lộ ra.

Thứ ba, nếu chỉ đánh giá sau khi hệ thống đã vận hành, thiệt hại — những sinh viên đã rời trường mà không được tiếp cận — là **không thể hoàn nguyên**. Đo trước khi triển khai là cách duy nhất để thiệt hại đó không xảy ra.

### 2.6.6 Chuyển tiếp

Tuy nhiên, phát hiện được chênh lệch mới chỉ là bước đầu; để hiểu **vì sao** chênh lệch xuất hiện, và để nhà trường đủ tin tưởng mà hành động dựa trên dự báo, bản thân mô hình không thể là một hộp đen. Nhu cầu này dẫn ta tới các phương pháp giải thích mô hình.


## 2.7 Giải thích mô hình (Explainable AI)

### 2.7.1 Vì sao mô hình cần giải thích được

Trong một hệ thống cảnh báo sớm, kết quả dự báo không tự nó tạo ra giá trị; giá trị chỉ xuất hiện khi một cố vấn học tập **hành động** dựa trên kết quả đó. Điều này đặt ra ba yêu cầu về tính minh bạch.

Thứ nhất, **hành động cần định hướng**: biết một sinh viên có nguy cơ 30% là chưa đủ để tư vấn; người cố vấn cần biết tín hiệu nào đang đẩy con số đó lên — kết quả học tập sa sút, tỷ lệ tín chỉ đạt thấp, hay cảnh báo học vụ tích lũy — để chọn hình thức hỗ trợ phù hợp.

Thứ hai, **kiểm tra tính hợp lý của mô hình**: việc rà soát những đặc trưng có ảnh hưởng lớn là một cơ chế phát hiện sai sót, đặc biệt là phát hiện các đặc trưng có dấu hiệu rò rỉ. Nếu một biến lẽ ra không mang thông tin dự báo lại chi phối mô hình, đó là chỉ dấu cần điều tra lại thiết kế dữ liệu (liên hệ mục 2.4).

Thứ ba, **điều kiện để được chấp nhận**: một hệ thống mà nhà trường không hiểu cách vận hành sẽ khó được tin tưởng và khó đưa vào quy trình thực tế.

### 2.7.2 SHAP làm gì

SHAP (Lundberg & Lee, 2017) đặt bài toán quy gán đặc trưng vào khuôn khổ **giá trị Shapley** của lý thuyết trò chơi hợp tác: mỗi đặc trưng được coi như một "người chơi", còn dự báo của mô hình là "phần thưởng" cần phân chia. Giá trị SHAP của một đặc trưng là **mức đóng góp của nó vào chênh lệch giữa dự báo cho một quan sát cụ thể và một giá trị tham chiếu (baseline)**.

Cần phát biểu chính xác: SHAP **không tiết lộ cơ chế bên trong mô hình**, mà **ước lượng một phép phân bổ đóng góp** cho từng dự báo riêng lẻ. Với mô hình cây, `TreeExplainer` tính các giá trị này trực tiếp và hiệu quả, thay vì ước lượng bằng lấy mẫu như các phiên bản model-agnostic.

Chính đặc tính **giải thích ở cấp độ từng quan sát** này khiến SHAP phù hợp với một hệ thống cảnh báo sớm. Cố vấn học tập không cần biết "đặc trưng nào quan trọng nói chung", mà cần trả lời được câu hỏi rất cụ thể: *"vì sao sinh viên này xuất hiện trong danh sách cần quan tâm, và tín hiệu nào nên được đề cập trước trong buổi tư vấn?"* Đây là câu hỏi ở cấp độ từng trường hợp — và là mắt xích nối giữa mô hình dự báo với hành động can thiệp sẽ bàn ở mục 2.8 (xem Hình 2.2).

### 2.7.3 SHAP không phải quan hệ nhân quả

Đây là ranh giới quan trọng nhất cần giữ. Giá trị SHAP mô tả **hành vi của mô hình**, không mô tả **thế giới thực**. Nói rằng "GPA học kỳ 2 có giá trị SHAP lớn" chỉ có nghĩa: *trong mô hình này*, biến GPA học kỳ 2 đóng góp nhiều vào việc đẩy dự báo lên hay xuống. Nó **không** cho phép kết luận rằng nâng GPA của một sinh viên lên sẽ làm giảm nguy cơ bỏ học của em đó — bởi GPA có thể chỉ là *dấu hiệu* của những nguyên nhân sâu hơn (khó khăn kinh tế, sức khỏe, sự phù hợp ngành học) mà mô hình không quan sát được.

Vì vậy, mọi phát biểu dựa trên SHAP trong luận văn được diễn đạt ở mức **liên hệ (association)**, không phải nhân quả; và các đề xuất can thiệp được trình bày như **giả thuyết cần kiểm chứng**, không phải kết luận nhân quả.

### 2.7.4 Hạn chế của phương pháp quy gán đặc trưng

Tài liệu gần đây đã chỉ ra những giới hạn nghiêm túc, cần được nêu thay vì bỏ qua.

**Giới hạn lý thuyết.** Bilodeau, Jaques, Koh & Kim (2024) chứng minh rằng, với các lớp mô hình đủ phong phú, **mọi phương pháp quy gán đặc trưng thỏa mãn tính đầy đủ và tuyến tính — bao gồm SHAP — có thể không tốt hơn đoán ngẫu nhiên** khi dùng để suy ra một số tính chất hành vi của mô hình. Đây là kết quả bất khả thi, nghĩa là không thể khắc phục bằng cách cải tiến thuật toán.

**Tính bất ổn.** Giá trị quy gán có thể thay đổi giữa các lần huấn luyện lại với hạt giống hoặc phân chia dữ liệu khác nhau; ở các phiên bản dựa trên lấy mẫu, còn có thêm dao động do chính quá trình lấy mẫu.

**Đặc trưng tương quan.** Khi các đặc trưng phụ thuộc lẫn nhau — điều hiển nhiên với các chỉ số học tập qua nhiều học kỳ — việc "loại bỏ" một đặc trưng trong khuôn khổ Shapley có thể tạo ra những tổ hợp không tồn tại trong thực tế, khiến đóng góp bị phân bổ lệch giữa các biến tương quan.

**Phụ thuộc tham chiếu.** Giá trị SHAP luôn được định nghĩa *tương đối với một baseline*; thay đổi phân phối tham chiếu sẽ thay đổi con số.

**Khoảng trống trong tài liệu.** Trong số các công trình được khảo sát, nhiều công trình có sử dụng SHAP, nhưng phần lớn trình bày một biểu đồ tầm quan trọng đặc trưng duy nhất, **không kiểm tra độ ổn định của giải thích** qua các lần huấn luyện và không nêu giới hạn nhân quả.

### 2.7.5 Vì sao luận văn vẫn chọn SHAP

Lựa chọn SHAP ở đây được đưa ra **cùng với các biện pháp phòng vệ tương ứng với từng hạn chế nêu trên**.

1. **Dùng đúng mục đích.** SHAP được dùng như công cụ **mô tả và truyền đạt** cho cố vấn học tập, không phải bằng chứng nhân quả và không phải cơ sở cho quyết định tự động. Kết quả bất khả thi của Bilodeau và cộng sự (2024) nhắm vào việc dùng quy gán để *suy ra tính chất hành vi của mô hình*; nó không phủ nhận giá trị của SHAP như một phương tiện diễn đạt có kỷ luật, miễn là không bị đọc quá mức.
2. **Tránh dao động do lấy mẫu.** Vì mô hình là tổ hợp cây, luận văn dùng `TreeExplainer` — tính trực tiếp thay vì ước lượng bằng lấy mẫu, do đó không chịu nguồn bất ổn đặc thù của các biến thể model-agnostic.
3. **Kiểm tra độ ổn định một cách tường minh.** Thay vì giả định giải thích là ổn định, luận văn **đo nó**: tính giá trị SHAP trên nhiều fold độc lập, rồi báo cáo với mỗi đặc trưng cả **mức đóng góp trung bình**, **độ lệch chuẩn giữa các fold**, và **số lần đặc trưng lọt vào nhóm 10 quan trọng nhất**. Chỉ những đặc trưng ổn định qua các fold mới được đưa ra diễn giải; phần còn lại được xem là dao động. Đây chính là câu trả lời trực tiếp cho phê phán về tính bất ổn.
4. **So với các lựa chọn khác.** LIME (Ribeiro và cộng sự, 2016) xây dựng mô hình thay thế cục bộ và được biết là kém ổn định giữa các lần chạy; tầm quan trọng theo hoán vị chỉ cho cái nhìn toàn cục, không giải thích được từng trường hợp — trong khi hệ thống cảnh báo cần giải thích ở cấp độ **từng sinh viên**.

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/fig_2_7_shap_to_intervention.png)

**Hình 2.2.** Vai trò của giải thích trong chuỗi từ dự báo tới can thiệp: xác suất nguy cơ → quy gán SHAP ở cấp độ từng sinh viên → chỉ giữ các đặc trưng ổn định qua các fold → cố vấn học tập hiểu được lý do → can thiệp đúng vấn đề. Hai nửa của chuỗi tương ứng với "mô hình + giải thích" và "con người + hành động". *(Nguồn: tác giả.)*


### 2.7.6 Chuyển tiếp

Tuy nhiên, một giải thích chỉ thực sự có giá trị khi được nhúng vào một quy trình hành động cụ thể. Từ việc **dự báo** nguy cơ và **diễn giải** các tín hiệu dẫn tới nguy cơ đó, bước tự nhiên tiếp theo là chuyển thông tin thành can thiệp kịp thời — tức là các hệ thống cảnh báo sớm.


## 2.8 Hệ thống cảnh báo sớm và can thiệp

### 2.8.1 Chuỗi hành động: bốn khâu

Một mô hình dự báo, tự nó, không giữ được sinh viên nào ở lại trường. Giá trị chỉ hình thành khi dự báo đi hết một chuỗi bốn khâu:

**Dự báo** (ai có nguy cơ) → **Quyết định** (ai được đưa vào danh sách can thiệp) → **Can thiệp** (làm gì với họ) → **Kết quả** (điều đó có thay đổi được gì không).

Phần lớn nghiên cứu dừng lại ở khâu thứ nhất. Nhưng mỗi khâu chuyển tiếp đều có thể làm hỏng toàn bộ chuỗi: một mô hình chính xác nhưng đặt ngưỡng sai sẽ tạo ra danh sách vượt quá năng lực tiếp cận; một danh sách hợp lý nhưng hình thức can thiệp không phù hợp sẽ không tạo tác động; và một can thiệp tốt mà không đo kết quả thì không thể biết có nên tiếp tục hay không. Mục này lần lượt xem xét ba khâu sau — vì khâu đầu đã được bàn ở các mục trước.

### 2.8.2 Khâu quyết định: ngưỡng là một tuyên bố chính sách

Chuyển từ xác suất sang danh sách hành động đòi hỏi một **ngưỡng**, và như đã lập luận ở mục 2.5, ngưỡng không phải tham số kỹ thuật mà là **phát biểu về sự đánh đổi chi phí**: chọn ngưỡng thấp nghĩa là chấp nhận nhiều báo động giả để không bỏ sót; chọn ngưỡng cao nghĩa là ưu tiên độ chính xác của danh sách.

Trong bối cảnh trường đại học, ràng buộc quyết định thường **không phải là ngưỡng xác suất mà là năng lực**: một khoa chỉ có thể tiếp cận sâu một số lượng sinh viên nhất định mỗi học kỳ. Do đó câu hỏi vận hành thực tế không phải "ngưỡng tối ưu là bao nhiêu" mà là *"với năng lực tiếp cận k sinh viên, danh sách nào giúp tiếp cận đúng người nhất"*. Phân tích đường cong quyết định (mục 2.5) chính là công cụ trả lời câu hỏi này, vì nó đánh giá lợi ích ròng trên toàn dải ngưỡng thay vì tại một điểm duy nhất.

### 2.8.3 Khâu can thiệp: bằng chứng từ hệ thống đã triển khai

Hệ thống được trích dẫn nhiều nhất trong lĩnh vực này là **Course Signals** tại Đại học Purdue (Arnold & Pistilli, 2012). Cách tiếp cận của nó có hai đặc điểm đáng chú ý: kết quả dự báo được truyền đạt bằng **tín hiệu đèn giao thông** (xanh – vàng – đỏ) thay vì con số xác suất, và mỗi tín hiệu gắn với một **hành động cụ thể** của giảng viên, thường là email hoặc liên hệ trực tiếp. Nói cách khác, hệ thống được thiết kế quanh *hành động*, không quanh *mô hình*.

Tuy nhiên, cần nêu cả mặt phản biện. Thuật toán rủi ro của Course Signals là **độc quyền và không công bố**, khiến kết quả khó tái lập và khó kiểm tra tính công bằng. Quan trọng hơn, các tuyên bố về hiệu quả giữ chân sinh viên của hệ thống này về sau **đã bị đặt câu hỏi về phương pháp**: phân tích ban đầu không kiểm soát **số lượng môn học mà sinh viên đăng ký**, dẫn tới khả năng **đảo chiều quan hệ nhân quả** — sinh viên đăng ký nhiều môn có dùng Course Signals hơn *bởi vì* họ vẫn đang tiếp tục theo học, chứ không phải tiếp tục theo học *bởi vì* đã dùng hệ thống. Weidlich, Gašević & Drachsler (2022) dẫn lại trường hợp này khi phân tích các dạng thiên lệch thường gặp trong suy luận nhân quả ở học phân tích — nhiễu (confounding), overcontrol và collider — và đề xuất dùng **đồ thị nhân quả có hướng (DAG)** để làm rõ giả định trước khi kết luận về hiệu quả can thiệp.

Bài học rút ra không phải là bác bỏ mô hình cảnh báo sớm, mà là: **tác động của can thiệp phải được thiết kế để đo lường được ngay từ đầu**, thay vì suy ra từ tương quan sau khi triển khai.

### 2.8.4 Thiết kế nhiều tầng theo mức độ can thiệp

Một hệ thống chỉ dùng **một ngưỡng duy nhất** buộc phải chấp nhận một đánh đổi cứng nhắc: ngưỡng thấp thì danh sách quá rộng, vượt năng lực tiếp cận và làm loãng nguồn lực; ngưỡng cao thì bỏ sót nhiều sinh viên cần giúp. Vấn đề nằm ở chỗ **một con số không thể phục vụ hai mục đích khác nhau** — vừa "không bỏ sót ai" vừa "dồn nguồn lực đắt cho đúng người".

Thiết kế **nhiều tầng theo mức độ can thiệp** nới lỏng đánh đổi này bằng cách gắn *nhiều ngưỡng khác nhau với những hình thức hỗ trợ khác nhau*, trên cùng một bộ xác suất dự báo. **Tầng thứ nhất** dùng ngưỡng thấp để **sàng lọc rộng**, ưu tiên không bỏ sót; nhóm này nhận hình thức hỗ trợ nhẹ và rẻ, chẳng hạn cố vấn theo dõi và nhắc nhở định kỳ. **Tầng thứ hai** dùng ngưỡng cao để **can thiệp sâu**, ưu tiên độ chính xác; nhóm này nhỏ hơn nhiều nhưng nhận hình thức hỗ trợ tốn kém hơn, chẳng hạn gặp trực tiếp hoặc hỗ trợ tài chính, tâm lý. Nhờ đó, mỗi mức nguồn lực được phân bổ theo đúng mức rủi ro, thay vì áp một chính sách chung cho mọi trường hợp.

> **Làm rõ thuật ngữ.** Trong nghiên cứu này, "hai tầng" **không** biểu thị hai *thời điểm dự báo* khác nhau, mà biểu thị hai *mức độ can thiệp* khác nhau trên cùng một bộ xác suất đã hiệu chỉnh. Nói cách khác, **chân trời thời gian và tầng can thiệp là hai trục độc lập**: chân trời quyết định *khi nào và bằng dữ liệu gì* mô hình đưa ra dự báo (mục 2.4), còn tầng quyết định *làm gì với dự báo đó*. Việc mở rộng sang cảnh báo tại nhiều thời điểm liên tiếp (ví dụ cảnh báo lần đầu ở cuối HK1 rồi cập nhật ở cuối HK1-2) là một **hướng nghiên cứu tiếp theo**, không thuộc phạm vi luận văn này.

### 2.8.5 Khâu kết quả: khoảng trống lớn nhất, và ranh giới của luận văn

Trong số các công trình được khảo sát, rất ít công trình đi tới khâu can thiệp, và hầu như không công trình nào **đo được liệu can thiệp có thay đổi kết quả hay không**. Nguyên nhân dễ hiểu: đánh giá tác động đòi hỏi thiết kế thực nghiệm hoặc phương pháp suy luận nhân quả, vượt ra ngoài phạm vi một nghiên cứu mô hình hóa thông thường.

Luận văn này cũng nằm trong giới hạn đó, và điều này cần được nói rõ: nghiên cứu **xây dựng và đánh giá hệ thống cảnh báo tới khâu quyết định** — bao gồm việc lựa chọn ngưỡng vận hành và phân tích lợi ích ròng — nhưng **không tiến hành thử nghiệm can thiệp** và do đó **không đưa ra tuyên bố nào về hiệu quả giữ chân sinh viên**. Việc đo lường tác động thực tế, bằng thiết kế đối chứng hoặc mô hình uplift, được nêu như hướng nghiên cứu tiếp theo.

### 2.8.6 Kết luận mục

Nhìn lại toàn chuỗi, có thể phát biểu nguyên tắc chi phối thiết kế của luận văn: **giá trị của một hệ thống cảnh báo sớm không nằm ở khả năng dự báo của nó, mà ở khả năng biến dự báo đó thành sự hỗ trợ có thật.** Chính nguyên tắc này giải thích vì sao các mục trước không dừng ở độ chính xác, mà lần lượt yêu cầu dữ liệu không rò rỉ (2.4), xác suất đáng tin (2.5), phân bổ công bằng (2.6) và giải thích được ở cấp độ từng sinh viên (2.7) — bốn điều kiện cần để khâu cuối cùng của chuỗi có thể xảy ra.


## 2.9 Khoảng trống nghiên cứu (Research Gap)

Qua tổng quan các công trình dự báo sinh viên bỏ học đã khảo sát, có thể thấy hướng nghiên cứu chủ đạo tập trung vào việc **nâng cao độ chính xác** của mô hình phân loại. Trong số các công trình được khảo sát, phần lớn sử dụng các thuật toán cây tăng cường độ dốc (gradient boosting) như XGBoost và LightGBM (Ke và cộng sự, 2017) trên dữ liệu dạng bảng và thường báo cáo các chỉ số AUC, F1 ở mức cao. Tuy nhiên, khi đánh giá các công trình này dưới góc độ *"liệu một mô hình cảnh báo sớm có thực sự đáng tin và triển khai được hay không"*, bốn hạn chế mang tính hệ thống lộ ra rõ rệt.

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

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/fig_2_9_conceptual_framework.png)

**Hình 2.3.** Khung khái niệm của luận văn — từ dữ liệu sinh viên tới can thiệp, làm cầu nối giữa tổng quan tài liệu (Chương 2) và phương pháp (Chương 3). *(Nguồn: tác giả.)*


\newpage

# Chương 3. Phương pháp nghiên cứu

---

## 3.1 Thiết kế nghiên cứu tổng thể

Nghiên cứu sử dụng thiết kế **hồi cứu, quan sát** trên dữ liệu học vụ đã có, với mục tiêu xây dựng và đánh giá một mô hình dự báo bỏ học **tại thời điểm kết thúc học kỳ *h***, dành cho những sinh viên **còn đang theo học** tại thời điểm đó.

Quy trình gồm bảy bước, tương ứng các khối của Hình 2.3: (1) chuẩn bị dữ liệu; (2) xác định quần thể và nhãn theo chân trời thời gian; (3) xây dựng đặc trưng giới hạn trong cửa sổ quan sát; (4) huấn luyện và so sánh mô hình; (5) đánh giá trung thực bằng nested cross-validation; (6) hiệu chỉnh xác suất và phân tích lợi ích quyết định; (7) kiểm định độ bền theo thời gian, tính công bằng và độ ổn định của giải thích.

Toàn bộ nghiên cứu dùng hằng số ngẫu nhiên **`RANDOM_STATE = 42`** ở mọi khâu có yếu tố ngẫu nhiên. Hình 3.1 tóm tắt toàn bộ quy trình cùng mục tương ứng của từng bước.

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/fig_3_1_quy_trinh.png)

**Hình 3.1.** Quy trình nghiên cứu, từ dữ liệu gốc tới hệ thống cảnh báo hai tầng; mỗi khối ghi kèm mục trình bày chi tiết. *(Nguồn: tác giả.)*


---

## 3.2 Dữ liệu

### 3.2.1 Nguồn và phạm vi

Dữ liệu là hồ sơ học vụ thực tế của một trường đại học Việt Nam (`Testkhoa.csv`), gồm thông tin của sinh viên qua **bốn học kỳ đầu**. Tệp được đọc với mã hóa **`latin-1`**; đọc bằng UTF-8 sẽ làm hỏng ký tự tiếng Việt.

Nghiên cứu chỉ giữ **hai khóa tuyển sinh 2020 và 2021** — là hai khóa có đủ dữ liệu bốn học kỳ. Tệp gốc chứa **7.523** bản ghi; chín sinh viên thuộc khóa 2022–2023 bị loại ngay khi nạp dữ liệu vì chưa đủ thời gian quan sát, nên tập phân tích còn **7.514 sinh viên**, với tỷ lệ bỏ học chung 13,1%.

### 3.2.2 Biến

**Bảng 3.1.** Các nhóm biến trong tập dữ liệu. *(Nguồn: `Testkhoa.csv`.)*

| Nhóm | Biến |
|---|---|
| Định danh | `StudentID` |
| Nhân khẩu – bối cảnh | `Gender`, `Nation`, `Religion`, `Region`, `Aspiration`, `IndustryCode` |
| Tuyển sinh | `EntranceScore_1..3`, `SumScore` |
| Theo từng học kỳ *i* (i = 1..4) | `GPA4_i`, `Rating_i`, `CreditsRegistered_i`, `CreditsEarnned_i`, `TermStatus_i` |
| Biến mục tiêu | `Drop` |

Biến xếp loại `Rating_i` được ánh xạ sang thang số thứ bậc (Không xếp loại = 0 … Xuất sắc = 5). Do đặc thù mã hóa `latin-1`, bảng ánh xạ chứa cả các khóa ở dạng ký tự bị biến dạng để khớp với dữ liệu thô; giá trị không ánh xạ được được gán `NaN` kèm cảnh báo, thay vì mặc định quy về 0.

---

## 3.3 Quần thể và nhãn theo chân trời thời gian

Đây là khâu cốt lõi, hiện thực hóa nguyên lý landmarking (mục 2.4).

### 3.3.1 Định nghĩa

Với mỗi chân trời *h*:

- **Trạng thái còn hoạt động** tại học kỳ *k* được xác định bằng `CreditsRegistered_k > 0`.
- **Quần thể phân tích** chỉ gồm những sinh viên **còn hoạt động tại học kỳ *h***.
- **Nhãn** được định nghĩa lại là: *sinh viên bỏ học **sau** thời điểm kết thúc học kỳ h*.

Cơ chế này loại bỏ rò rỉ ở tầng quần thể: những sinh viên đã rời trường **trước** học kỳ *h* bị loại khỏi phân tích, nên các đặc trưng học kỳ *h* của họ (GPA = 0, không đăng ký tín chỉ) — vốn là *hệ quả* của việc đã nghỉ học — không thể đóng vai trò biến thay thế cho nhãn.

### 3.3.2 Hai chân trời được phân tích

Nghiên cứu phân tích hai chân trời triển khai được: **HK1** (*h* = 1) và **HK1-2** (*h* = 2). Chân trời bốn học kỳ chỉ được dùng làm **tham chiếu minh họa rò rỉ**, không đưa vào kết quả chính.

**Bảng 3.2.** Quy mô quần thể và số đặc trưng theo từng chân trời. *(Nguồn: `horizon_dataset()` trong `dropout_research.py`.)*

| Chân trời | Số sinh viên | Số đặc trưng | Trong đó: hạng mục | Tỷ lệ bỏ học sau chân trời |
|---|---|---|---|---|
| HK1 | 7.367 | 25 | 6 | 11,5% |
| HK1-2 | 7.034 | 36 | 6 | 7,4% |

Cần phân biệt rõ: tỷ lệ **13,1%** là tỷ lệ bỏ học của toàn bộ hai khóa (7.514 sinh viên) *trước khi* giới hạn theo chân trời; hai con số trong bảng là tỷ lệ của quần thể đã giới hạn, và giảm dần khi dự báo muộn hơn — vì những sinh viên bỏ học sớm đã không còn trong quần thể.

### 3.3.3 Hai giả định phải kiểm chứng

1. **Trạng thái "còn hoạt động"** được xấp xỉ bằng `CreditsRegistered_k > 0`. Nếu nhà trường có trường dữ liệu chính thức về thời điểm thôi học, cần thay thế xấp xỉ này.
2. **`TermStatus_k`** được coi là *cảnh báo học vụ đã biết tại cuối học kỳ k*, do đó giữ làm đặc trưng. Nếu trên thực tế biến này mã hóa trạng thái "đã thôi học", nó là **nhãn trá hình** và phải loại bỏ — mã nguồn có sẵn cờ `DROP_TERMSTATUS` cho tình huống này.

Cả hai giả định được nêu lại trong phần hạn chế.

---

## 3.4 Xây dựng đặc trưng

Đặc trưng được xây **chỉ từ các học kỳ 1 đến *h***, gồm hai nhóm:

**Đặc trưng theo từng học kỳ** — `GPA4_i`, `RatingNum_i`, `CreditRate_i` (tỷ lệ tín chỉ đạt trên tín chỉ đăng ký), `TermStatus_i`, với *i* ≤ *h*.

**Đặc trưng tích lũy** — trung bình, giá trị nhỏ nhất, độ lệch chuẩn và xu hướng của GPA; tỷ lệ tín chỉ đạt tích lũy; tổng số cảnh báo học vụ tích lũy.

### Chính sách giá trị thiếu

Với học kỳ mà sinh viên **không hoạt động**, các đặc trưng `GPA4_i`, `RatingNum_i`, `CreditRate_i` được gán **`NaN`, không phải 0**. Đây là quyết định thiết kế có chủ đích nhằm phân biệt *"không có dữ liệu"* với *"đạt kết quả bằng không"* — hai trạng thái mang ý nghĩa hoàn toàn khác nhau. Ở cả hai chân trời, có **8 cột chứa giá trị thiếu**.

Biến `EnrollmentYear` **bị loại khỏi tập đặc trưng** vì nó mã hóa khóa tuyển sinh (gây rò rỉ thông tin nhóm trong CV gộp) và là hằng số trong kiểm định thời gian.

---

## 3.5 Mô hình và tiền xử lý

**Ba** thuật toán được chọn để **bao phủ các họ phương pháp khác nhau về mặt cấu trúc**, chứ không phải để tìm mô hình thắng cuộc: hồi quy logistic đại diện cho **mô hình tuyến tính** — mốc tham chiếu dễ diễn giải nhất; rừng ngẫu nhiên đại diện cho **tổ hợp cây theo kiểu bagging**; và LightGBM đại diện cho **tổ hợp cây theo kiểu boosting**.

**Nguyên tắc so sánh: tất cả đều dùng tham số mặc định.** Mục này trả lời câu hỏi *"thuật toán nào phù hợp với dữ liệu này"*, nên mọi mô hình được đặt dưới cùng một điều kiện. Nếu chỉ tinh chỉnh riêng LightGBM rồi so với các mô hình chưa tinh chỉnh, phép so sánh sẽ **trộn lẫn hai câu hỏi khác nhau** — ưu thế của thuật toán và ưu thế của việc tối ưu siêu tham số — và không còn công bằng. Ảnh hưởng của việc tinh chỉnh do đó được đánh giá **riêng và đúng cách** bằng nested cross-validation ở mục 3.7, là nơi duy nhất trong luận văn bàn về tinh chỉnh siêu tham số.

**Bảng 3.3.** Ba thuật toán được so sánh, kèm cách xử lý giá trị thiếu và cân bằng lớp. *(Nguồn: `make_models()` trong `dropout_research.py`.)*

| Mô hình | Xử lý giá trị thiếu | Cân bằng lớp |
|---|---|---|
| Hồi quy logistic | Điền median (số) / mode (hạng mục) + chuẩn hóa + one-hot | `class_weight='balanced'` |
| Rừng ngẫu nhiên (400 cây, `min_samples_leaf=5`) | như trên | `class_weight='balanced'` |
| LightGBM | **native `NaN`** | `is_unbalance=True` |

Tham số mặc định của LightGBM: `n_estimators=300`, `learning_rate=0.05`, `num_leaves=31`, `subsample=0.8`, `colsample_bytree=0.8`, `reg_lambda=1.0`.

**Nguyên tắc "mọi thao tác đều trong fold".** Toàn bộ bước điền khuyết, chuẩn hóa, mã hóa one-hot (`min_frequency=20`) của các mô hình nền được đặt bên trong `Pipeline` của scikit-learn, nên chỉ được khớp trên phần dữ liệu huấn luyện của từng fold. Tương tự, cân bằng lớp của LightGBM dùng `is_unbalance=True` để trọng số được tính trên đúng dữ liệu đang khớp, thay vì tính một lần trên toàn bộ nhãn trước khi chia fold.

---

## 3.6 Giao thức đánh giá

### 3.6.1 Ước lượng ngoài fold

Sử dụng **kiểm định chéo phân tầng lặp lại**: 5 fold × 10 lần lặp (hạt giống `42 + r` cho mỗi lần lặp). Mỗi lần lặp cho một tập dự báo ngoài fold hoàn chỉnh; xác suất cuối cùng là **trung bình qua 10 lần lặp**. Độ lệch chuẩn của AUC giữa các lần lặp được báo cáo như chỉ số ổn định.

### 3.6.2 Khoảng tin cậy

**Bootstrap percentile**, `B = 2.000` lần lấy mẫu lại có hoàn lại, mức tin cậy **95%**. Các mẫu bootstrap chỉ chứa một lớp bị bỏ qua. Chỉ số báo cáo: AUC, AP, Brier, F1, Precision, Recall, Accuracy.

### 3.6.3 Kiểm định so sánh mô hình

- **DeLong** (bản nhanh theo Sun & Xu, 2014) cho cặp AUC, thống kê z hai phía.
- **Wilcoxon signed-rank** và **paired t-test** trên AUC của từng lần lặp (n = 10).
- Hiệu chỉnh đa so sánh bằng **Holm step-down**, kiểm soát FWER và mạnh hơn Bonferroni thuần ở cùng mức kiểm soát.

### 3.6.4 Hạn chế đã biết của giao thức (khai báo chủ động)

Các dự báo ngoài fold **không hoàn toàn độc lập với nhau**, vì các mô hình trong những lần lặp khác nhau được huấn luyện trên các tập dữ liệu chồng lấn. Hệ quả: khoảng tin cậy bootstrap có xu hướng **hơi hẹp**, và kiểm định DeLong trên dự báo ngoài fold **dễ bác bỏ giả thuyết không hơn mức danh nghĩa**. Vì lý do này, kiểm định theo từng lần lặp được xem là kênh bổ trợ đúng đắn hơn, và **cả hai loại kết quả đều được báo cáo** thay vì chọn loại thuận lợi hơn.

---

## 3.7 Đánh giá trung thực bằng nested cross-validation

Phân tích này được thực hiện trên **chân trời HK1**. Để tách quá trình tinh chỉnh khỏi quá trình đánh giá:

- **Vòng ngoài:** 5 fold phân tầng (hạt giống 42) — chỉ dùng để ước lượng hiệu năng.
- **Vòng trong:** 3 fold, tối ưu bằng **Optuna** với bộ lấy mẫu TPE (hạt giống `42 + k`), **40 thử nghiệm** mỗi fold ngoài, hàm mục tiêu là AUC trung bình của vòng trong.

Không gian tìm kiếm: `n_estimators` ∈ [100, 600]; `learning_rate` ∈ [0,01; 0,2] (thang log); `num_leaves` ∈ [15, 127]; `max_depth` ∈ [3, 12]; `min_child_samples` ∈ [10, 100]; `subsample` ∈ [0,6; 1,0]; `colsample_bytree` ∈ [0,6; 1,0]; `reg_alpha`, `reg_lambda` ∈ [10⁻³; 10] (thang log).

Việc so sánh giữa mô hình dùng tham số mặc định và mô hình được tinh chỉnh bằng nested cross-validation nhằm **minh họa ảnh hưởng của quá trình tối ưu siêu tham số dưới một quy trình đánh giá hợp lệ**, trong đó mỗi fold kiểm tra ngoài chưa từng tham gia vào bất kỳ bước chọn siêu tham số nào. Hình 3.2 minh họa cấu trúc hai vòng này.

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/fig_3_2_nested_cv.png)

**Hình 3.2.** Kiểm định chéo lồng nhau: vòng ngoài chỉ dùng để đánh giá, vòng trong chỉ dùng để tinh chỉnh bằng Optuna; fold kiểm tra ngoài không tham gia vào bất kỳ bước chọn siêu tham số nào. *(Nguồn: tác giả.)*


---

## 3.8 Hiệu chỉnh xác suất và lợi ích quyết định

**Hiệu chỉnh.** Áp dụng trên chân trời HK1-2. Hai phương pháp được so sánh: **isotonic** và **sigmoid (Platt)**, cả hai được bọc bằng `CalibratedClassifierCV` với `cv = 3` và **khớp bên trong train-fold**; dự báo ngoài fold thu được qua 5 fold phân tầng (hạt giống 42). So sánh với xác suất chưa hiệu chỉnh.

**Chỉ số.** `Brier score` (giá trị thô, không chuẩn hóa) và **ECE** với **10 bin đều**.

> ⚠️ **Quy ước diễn giải ECE.** Ở cỡ mẫu vài nghìn, ECE có "sàn nhiễu" khoảng 0,005–0,01 ngay cả khi mô hình hiệu chỉnh hoàn hảo. Do đó giá trị ECE dưới ngưỡng này chỉ được diễn giải là *"không phát hiện sai lệch hiệu chỉnh"*, không được diễn đạt là *"hiệu chỉnh gần như hoàn hảo"*.

**Đường cong quyết định.** Lợi ích ròng được tính theo Vickers & Elkin (2006): `NB = TP/n − (FP/n)·(p_t/(1−p_t))`, trên dải ngưỡng `p_t` từ 0,01 đến 0,60 (60 điểm), so sánh với hai chiến lược tham chiếu "can thiệp tất cả" và "không can thiệp ai". Phân tích thực hiện trên xác suất đã hiệu chỉnh bằng isotonic.

---

## 3.9 Kiểm định độ bền theo thời gian và tính công bằng

**Theo thời gian.** Huấn luyện trên khóa **2020**, kiểm tra trên khóa **2021** (chân trời HK1-2), báo cáo AUC kèm khoảng tin cậy bootstrap percentile, cùng AP, Recall và Precision tại ngưỡng 0,5.

**Công bằng.** Đánh giá trên xác suất đã hiệu chỉnh, theo hai thuộc tính: **giới tính** và **dân tộc** (Kinh so với dân tộc thiểu số). Với mỗi nhóm, báo cáo cỡ mẫu, tỷ lệ bỏ học nền, **AUC kèm khoảng tin cậy bootstrap**, và **độ nhạy tại ngưỡng 0,5**. Các nhóm có **dưới 50 quan sát** hoặc không đủ hai lớp bị loại khỏi phân tích.

> ⚠️ **Phạm vi.** Nghiên cứu **đo lường và báo cáo** chênh lệch giữa các nhóm; **không áp dụng kỹ thuật giảm thiểu** (mitigation).

**Về việc chọn ngưỡng 0,5 để đo — nói rõ để không bị hiểu sai.** Giá trị 0,5 ở đây **không phải một ngưỡng được thiết kế riêng cho phân tích công bằng**, mà là **ngưỡng mặc định của tầng phân tích**, được dùng thống nhất cho *mọi* chỉ số phụ thuộc ngưỡng trong luận văn: bảng so sánh thuật toán (mục 3.6), kiểm định theo thời gian và phân tích công bằng (mục này). Lý do giữ nguyên một giá trị duy nhất là để các con số F1, precision và độ nhạy ở những mục khác nhau **so sánh được với nhau**; nếu mỗi mục dùng một ngưỡng riêng thì không còn đối chiếu chéo được.

Hệ quả cần nêu thẳng: **0,5 không phải ngưỡng vận hành của hệ thống cảnh báo** (mục 3.11 dùng 0,10 và 0,40), và nó **không được chọn với cân nhắc về triển khai**. Vì *cơ hội bình đẳng* là tính chất gắn với một ngưỡng cụ thể, kết quả công bằng ở mục 4.9 chỉ có hiệu lực **tại ngưỡng 0,5**; việc đánh giá công bằng tại đúng hai ngưỡng vận hành được nêu như hướng nghiên cứu tiếp theo. Khi diễn giải chênh lệch độ nhạy, phải đọc kèm tỷ lệ bỏ học nền của từng nhóm, vì ở cùng một ngưỡng, hai nhóm có tỷ lệ nền khác nhau sẽ có độ nhạy khác nhau ngay cả với mô hình hiệu chỉnh hoàn hảo.

---

## 3.10 Giải thích và độ ổn định của giải thích

Giá trị SHAP được tính bằng **`TreeExplainer`** trên mô hình LightGBM, ở chân trời HK1-2.

Để kiểm tra độ ổn định thay vì giả định nó, quy trình được lặp trên **5 fold phân tầng độc lập** (hạt giống 42). Với mỗi đặc trưng, báo cáo ba đại lượng: **giá trị SHAP tuyệt đối trung bình**, **độ lệch chuẩn giữa các fold**, và **số fold mà đặc trưng lọt vào nhóm 10 quan trọng nhất**. Chỉ những đặc trưng ổn định qua các fold mới được đưa ra diễn giải ở Chương 4.


---

## 3.11 Thiết kế hệ thống cảnh báo hai tầng

Hệ thống vận hành theo **hai mức độ can thiệp**, đặt trên **cùng một bộ xác suất đã hiệu chỉnh bằng isotonic và thu được ngoài fold** (chân trời HK1-2). Thứ tự này cần được nêu rõ vì nó quyết định ý nghĩa của mọi ngưỡng: **hiệu chỉnh trước, đặt ngưỡng sau**. Nếu đặt ngưỡng trên xác suất chưa hiệu chỉnh, cùng một con số 0,40 sẽ ứng với một nhóm sinh viên khác, và toàn bộ phân tích lợi ích quyết định ở mục 3.8 sẽ không còn áp dụng được cho hệ thống này.

- **Tầng 1 — sàng lọc rộng (ngưỡng thấp):** ưu tiên **không bỏ sót** (độ nhạy cao), gắn với hình thức hỗ trợ nhẹ và chi phí thấp — cố vấn học tập theo dõi và nhắc nhở.
- **Tầng 2 — can thiệp sâu (ngưỡng cao):** ưu tiên **độ chính xác** của danh sách, gắn với hình thức hỗ trợ tốn kém hơn — gặp trực tiếp, hỗ trợ tài chính hoặc tâm lý.

> **Làm rõ:** "hai tầng" ở đây là hai *mức độ can thiệp*, **không phải** hai *thời điểm dự báo*. Chân trời thời gian (mục 3.3) và tầng can thiệp là hai trục độc lập. Việc cảnh báo tại nhiều thời điểm liên tiếp là hướng nghiên cứu tiếp theo.

Bảng ngưỡng được sinh bởi hàm `warning_tiers()` và ghi ra `05_KetQua_ThongKe/warning_thresholds.csv` như một bước của `run_pipeline.py`, nên tái lập được như mọi bảng kết quả khác. Bảng quét dải ngưỡng từ 0,05 đến 0,50 và báo cáo với từng ngưỡng: số sinh viên được gắn cờ, tỷ lệ gắn cờ, precision và recall — cho phép mỗi trường tự chọn ngưỡng vận hành theo năng lực tư vấn của mình. Hai ngưỡng được chọn làm tầng vận hành mặc định trong luận văn là **0,10** (tầng 1) và **0,40** (tầng 2); kết quả cụ thể trình bày ở mục 4.11.

> ⚠️ **Hai ngưỡng này không được tối ưu hóa trên dữ liệu nghiên cứu.** Chúng là hằng số cố định trong mã nguồn (`warning_tiers(..., tier1=0.10, tier2=0.40)`), **không** đi qua bất kỳ thủ tục tìm kiếm nào — không Optuna, không quét chọn điểm tối ưu theo F1 hay theo lợi ích ròng. Chúng chỉ đóng vai trò **hai mốc minh họa** cho hai mức độ can thiệp: một ngưỡng thấp ưu tiên độ nhạy và một ngưỡng cao ưu tiên độ chính xác. Đây là lựa chọn có chủ ý và nhất quán với nguyên tắc xuyên suốt của luận văn: **không tối ưu hóa trên chính tập dữ liệu dùng để báo cáo**. Vì vậy bảng ở mục 4.11 báo cáo **toàn bộ dải ngưỡng** thay vì chỉ hai điểm này, để mỗi cơ sở đào tạo tự chọn ngưỡng vận hành theo năng lực tư vấn thực tế của mình.

---

## 3.12 Tái lập nghiên cứu

**Bảng 3.4.** Thông tin tái lập nghiên cứu. *(Nguồn: môi trường chạy thực tế, ghi lại trong log `run_pipeline_log_2026-07-18_v2_3models.txt`.)*

| Thành phần | Giá trị |
|---|---|
| Python | 3.9.6 |
| lightgbm / scikit-learn | 4.5.0 / 1.6.1 |
| shap / optuna | 0.49.1 / 4.8.0 |
| numpy / scipy | 1.26.4 / 1.13.1 |
| Hệ điều hành | macOS (Darwin 25.5.0), kiến trúc arm64 |
| Thiết bị tính | CPU (không dùng GPU/CUDA) |
| Hạt giống | `RANDOM_STATE = 42` |
| Tệp dữ liệu | `Testkhoa.csv`, MD5 `09e5873d10cd15572e162c9fd705f34f` |
| Lệnh tái lập | `python3 run_pipeline.py` → mở notebook → Restart & Run All |


\newpage

# Chương 4. Kết quả nghiên cứu

---

## 4.1 Tổng quan chương

Chương này trình bày kết quả theo đúng trình tự giao thức ở Chương 3: đặc điểm quần thể theo chân trời (4.2), so sánh thuật toán kèm khoảng tin cậy (4.3) và kiểm định ý nghĩa (4.4), đánh giá LightGBM sau tinh chỉnh bằng nested cross-validation (4.5), hiệu chỉnh xác suất và lợi ích quyết định (4.6), bằng chứng định lượng về rò rỉ (4.7), độ bền theo thời gian (4.8), tính công bằng (4.9), giải thích và độ ổn định của giải thích (4.10), và hệ thống cảnh báo hai tầng (4.11).

Mọi **khoảng tin cậy** (viết tắt **KTC**) trong chương là **bootstrap percentile 95%** với B = 2.000, trừ khi ghi chú khác.

---

## 4.2 Đặc điểm quần thể theo chân trời

**Bảng 4.1.** Quy mô, số đặc trưng và tỷ lệ bỏ học theo từng chân trời.

| Chân trời | Số sinh viên | Số đặc trưng | Hạng mục | Cột chứa `NaN` | Tỷ lệ bỏ học sau chân trời |
|---|---|---|---|---|---|
| HK1 | 7.367 | 25 | 6 | 8 | 11,5% |
| HK1-2 | 7.034 | 36 | 6 | 8 | 7,4% |

*Nguồn: `horizon_dataset()` và `build_features_raw()` trong `dropout_research.py`; đối chiếu Bảng 3.2.*

Tỷ lệ bỏ học **giảm** khi chân trời muộn hơn (11,5% → 7,4%). Đây không phải dấu hiệu mô hình "tốt lên" mà là hệ quả trực tiếp của thiết kế landmarking: những sinh viên bỏ học sớm đã rời khỏi quần thể phân tích ở chân trời sau. Nói cách khác, càng dự báo muộn thì lớp dương càng hiếm, và bài toán càng khó về mặt mất cân bằng.

> ⚠️ Không lẫn hai con số này với **13,1%** — tỷ lệ bỏ học của toàn bộ hai khóa (7.514 sinh viên) *trước khi* giới hạn theo chân trời.

**Đây là quần thể được sử dụng thống nhất trong các phân tích còn lại của Chương 4, tương ứng với chân trời mà từng mục nêu rõ** — mục 4.3 và 4.4 báo cáo cả hai chân trời, mục 4.5 thực hiện trên HK1, còn các mục từ 4.6 tới 4.11 đều thực hiện trên HK1-2.

---

## 4.3 So sánh thuật toán

Ba thuật toán được so sánh dưới **cùng một giao thức và đều dùng tham số mặc định**, trả lời câu hỏi *thuật toán nào phù hợp với dữ liệu này*. Ảnh hưởng của tinh chỉnh siêu tham số được xét riêng ở mục 4.5.

**Bảng 4.2.** Hiệu năng ba thuật toán (ước lượng ngoài fold, 5 fold × 10 lần lặp).

| Chân trời | Thuật toán | AUC [KTC 95%] | AP | F1 | Precision | Recall | Brier | SD giữa các lần lặp |
|---|---|---|---|---|---|---|---|---|
| HK1 | Hồi quy logistic | **0,8464** [0,8321–0,8606] | 0,5226 | 0,4411 | 0,3137 | **0,7429** | 0,1503 | 0,0016 |
| HK1 | Rừng ngẫu nhiên | 0,8354 [0,8213–0,8501] | 0,5110 | 0,4664 | 0,4495 | 0,4846 | 0,0998 | 0,0023 |
| HK1 | LightGBM | 0,8436 [0,8292–0,8574] | **0,5366** | **0,4766** | **0,4552** | 0,5000 | **0,0900** | 0,0032 |
| HK1-2 | Hồi quy logistic | **0,9278** [0,9147–0,9398] | **0,7183** | 0,4929 | 0,3551 | **0,8054** | 0,0872 | 0,0015 |
| HK1-2 | Rừng ngẫu nhiên | 0,9212 [0,9078–0,9338] | 0,6889 | 0,6449 | 0,6442 | 0,6455 | 0,0458 | 0,0016 |
| HK1-2 | LightGBM | 0,9203 [0,9068–0,9331] | 0,7039 | **0,6495** | **0,6984** | 0,6069 | **0,0395** | 0,0029 |

*Nguồn: `05_KetQua_ThongKe/metrics_with_ci.csv`. In đậm = giá trị tốt nhất của từng cột trong cùng một chân trời (với Brier, tốt nhất là giá trị nhỏ nhất).*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_metric_ci.png)

**Hình 4.1.** Khoảng tin cậy AUC theo thuật toán và chân trời. *(Nguồn: tác giả.)*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_model_comparison.png)

**Hình 4.2.** Chênh lệch AUC từng cặp thuật toán. *(Nguồn: tác giả.)*


### Diễn giải

Về **khả năng phân biệt**, ba thuật toán rất gần nhau và mọi khoảng tin cậy đều chồng lấn. Hồi quy logistic đạt AUC cao nhất về mặt con số ở cả hai chân trời (0,8464 ở HK1 và 0,9278 ở HK1-2), nhỉnh hơn LightGBM lần lượt 0,0028 và 0,0074. Cần nói thẳng điều này, và mục 4.4 sẽ cho thấy các khác biệt so với LightGBM **không đạt mức ý nghĩa thống kê**.

Tuy nhiên, bức tranh đảo chiều rõ rệt khi xét **chất lượng xác suất và hiệu năng tại ngưỡng vận hành**. Ở HK1-2, Brier của hồi quy logistic là 0,0872 — **kém hơn LightGBM (0,0395) khoảng 2,2 lần**; F1 là 0,4929 so với 0,6495 của LightGBM, với precision chỉ 0,3551 so với 0,6984, trong khi độ nhạy lại cao hơn (0,8054 so với 0,6069).

Mẫu hình này — độ nhạy cao đi kèm precision thấp và Brier lớn — **phù hợp với ảnh hưởng có thể có** của việc kết hợp cơ chế bù mất cân bằng `class_weight='balanced'` với việc đánh giá tại ngưỡng cố định 0,5: trọng số lớp làm dịch chuyển phân bố xác suất dự báo về phía lớp thiểu số, khiến nhiều trường hợp vượt ngưỡng hơn. Cần lưu ý rằng đây là **cách diễn giải phù hợp với dữ liệu quan sát được**, chưa phải kết luận nhân quả đã được kiểm chứng bằng thí nghiệm riêng.

Dù cơ chế cụ thể là gì, **quan sát thực nghiệm vẫn vững**: hồi quy logistic có AUC cao hơn nhưng Brier kém hơn, F1 thấp hơn và precision thấp hơn ở cả hai chân trời.

Đây chính là minh họa thực nghiệm cho luận điểm đã trình bày ở mục 2.5: **khả năng phân biệt tốt không đồng nghĩa với xác suất đáng tin**. Một mô hình xếp hạng tốt vẫn có thể đưa ra những con số không dùng được để ra quyết định.

### Thuật toán được chọn cho các phân tích tiếp theo

**LightGBM** được chọn làm mô hình chính cho toàn bộ phần còn lại của chương. Lựa chọn này **không dựa trên việc đạt AUC cao nhất** — như trên đã thấy, nó không đạt. Cơ sở gồm năm điểm:

1. **Chất lượng xác suất vượt trội** (Brier 0,0395 so với 0,0872), điều kiện tiên quyết cho hệ thống cảnh báo dựa trên ngưỡng xác suất và cho phân tích lợi ích quyết định ở mục 4.6;
2. **Hiệu năng cao nhất tại ngưỡng vận hành** (F1 và precision cao nhất ở cả hai chân trời), phù hợp với ràng buộc nguồn lực tư vấn hữu hạn;
3. **Xử lý `NaN` ở mức thuật toán**, giữ nguyên sự phân biệt giữa "không có dữ liệu" và "kết quả bằng không" mà thiết kế đặc trưng cố ý tạo ra;
4. **Tương thích `TreeExplainer`**, điều kiện cần cho giải thích ở cấp độ từng sinh viên (mục 4.10);
5. **Chi phí tính toán** cho phép chạy trọn giao thức đánh giá nhiều lần.

---

## 4.4 Kiểm định ý nghĩa thống kê

**Bảng 4.3.** Kiểm định DeLong từng cặp, kèm hiệu chỉnh Holm (ba cặp trong mỗi chân trời).

| Chân trời | Thuật toán A | Thuật toán B | ΔAUC | z | p (DeLong) | **p (Holm)** |
|---|---|---|---|---|---|---|
| HK1 | Hồi quy logistic | Rừng ngẫu nhiên | +0,0110 | 2,397 | 0,0165 | **0,0496** |
| HK1 | Hồi quy logistic | LightGBM | +0,0028 | 0,682 | 0,4953 | 0,4953 |
| HK1 | Rừng ngẫu nhiên | LightGBM | −0,0083 | −2,031 | 0,0422 | 0,0845 |
| HK1-2 | Hồi quy logistic | Rừng ngẫu nhiên | +0,0066 | 1,842 | 0,0655 | 0,1309 |
| HK1-2 | Hồi quy logistic | LightGBM | +0,0074 | 2,180 | 0,0293 | 0,0878 |
| HK1-2 | Rừng ngẫu nhiên | LightGBM | +0,0009 | 0,261 | 0,7939 | 0,7939 |

*Nguồn: `05_KetQua_ThongKe/model_significance.csv`*

### Diễn giải

Sau hiệu chỉnh Holm, **chỉ một trong sáu cặp đạt mức ý nghĩa, và ở sát ngưỡng**: hồi quy logistic so với rừng ngẫu nhiên ở chân trời HK1 (p = 0,0496). Đáng chú ý, **chênh lệch giữa hồi quy logistic và LightGBM không đạt ý nghĩa thống kê ở cả hai chân trời** (p = 0,4953 và p = 0,0878), tức là ưu thế về AUC của hồi quy logistic nêu ở mục 4.3 không được bằng chứng thống kê ủng hộ.

Kết luận tổng thể: xét riêng khả năng phân biệt, ba thuật toán **về cơ bản tương đương** trên dữ liệu này; sự khác biệt có ý nghĩa thực tiễn nằm ở chất lượng xác suất và hiệu năng tại ngưỡng vận hành, chứ không ở AUC.

> ⚠️ **Hạn chế của kiểm định này (đã khai báo ở mục 3.6.4):** các dự báo ngoài fold không hoàn toàn độc lập, nên kiểm định DeLong trên dự báo ngoài fold có xu hướng **bác bỏ giả thuyết không dễ hơn mức danh nghĩa**. Do đó kết quả duy nhất đạt ý nghĩa (p = 0,0496, sát ngưỡng) cần được diễn giải **thận trọng**, và không nên dùng làm cơ sở cho bất kỳ kết luận mạnh nào.

---

## 4.5 Đánh giá LightGBM sau khi tinh chỉnh bằng nested cross-validation

Đây là **mục duy nhất** trong luận văn bàn về tinh chỉnh siêu tham số.

**Bảng 4.4.** Kết quả nested CV cho LightGBM (chân trời HK1).

| Fold ngoài | AUC kiểm tra | AP kiểm tra | AUC tốt nhất vòng trong |
|---|---|---|---|
| 0 | 0,8495 | 0,5447 | 0,8415 |
| 1 | 0,8519 | 0,5326 | 0,8477 |
| 2 | 0,8602 | 0,5041 | 0,8446 |
| 3 | 0,8332 | 0,5497 | 0,8483 |
| 4 | 0,8584 | 0,5794 | 0,8397 |
| **Trung bình ± SD** | **0,8506 ± 0,0107** | 0,5421 | 0,8444 |

**So sánh:** LightGBM tham số mặc định (mục 4.3) = 0,8436 · LightGBM tinh chỉnh (nested CV) = 0,8506 · **ΔAUC = +0,0070**

*Nguồn: `05_KetQua_ThongKe/nested_cv_results.csv`; siêu tham số tốt nhất từng fold: `nested_best_params.pkl`*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_nested_vs_flat.png)

**Hình 4.3.** LightGBM: tham số mặc định so với tinh chỉnh bằng nested CV. *(Nguồn: tác giả.)*


### Diễn giải

Việc tối ưu siêu tham số bằng Optuna, khi được đánh giá theo quy trình lồng nhau, mang lại cải thiện **ΔAUC ≈ +0,007** so với cấu hình mặc định. Con số 0,8506 là **ước lượng không bị thổi phồng**, vì mỗi fold kiểm tra ngoài chưa từng tham gia vào bất kỳ bước chọn siêu tham số nào. Độ lệch chuẩn giữa các fold ngoài (0,0107) lớn hơn mức cải thiện, cho thấy lợi ích của tinh chỉnh **khiêm tốn so với dao động do chia mẫu**.

> 🔴 **Cảnh báo diễn đạt:** **không được gọi hiệu số này là "optimism gap"**. Đo mức lạc quan đòi hỏi so sánh *tinh chỉnh phẳng* với *tinh chỉnh lồng nhau*; nghiên cứu này **không thực hiện quy trình tinh chỉnh phẳng độc lập**, nên không đưa ra kết luận nào về mức optimism. Ở đây chỉ so *mặc định* với *tinh chỉnh đánh giá đúng cách*.

---

## 4.6 Hiệu chỉnh xác suất và lợi ích quyết định

**Bảng 4.5.** Chất lượng hiệu chỉnh của LightGBM trên chân trời HK1-2 (n = 7.034).

| Phương pháp | Brier | ECE (10 bin đều) |
|---|---|---|
| Chưa hiệu chỉnh | 0,0415 | 0,0339 |
| **Isotonic** | **0,0363** | **0,0047** |
| Sigmoid (Platt) | 0,0374 | 0,0059 |

*Nguồn: `06_TrungGian_Checkpoint/calibration.pkl`; số liệu lợi ích ròng trong phần diễn giải lấy từ `05_KetQua_ThongKe/decision_curve.csv`*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_calibration.png)

**Hình 4.4.** Biểu đồ độ tin cậy trước và sau hiệu chỉnh. *(Nguồn: tác giả.)*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_decision_curve.png)

**Hình 4.5.** Đường cong quyết định. *(Nguồn: tác giả.)*


### Diễn giải

Hiệu chỉnh cải thiện rõ rệt cả hai chỉ số: Brier giảm từ 0,0415 xuống 0,0363 và ECE giảm từ 0,0339 xuống 0,0047 với phương pháp isotonic. Điều này xác nhận nhận định ở mục 2.5.2 rằng **cây tăng cường có xu hướng hiệu chỉnh kém nếu không xử lý** — và bước hiệu chỉnh là cần thiết, không phải tùy chọn.

> ⚠️ **Quy ước diễn giải ECE:** giá trị 0,0047 **nằm dưới sàn nhiễu** ước tính (~0,005–0,01 ở cỡ mẫu này). Do đó phải phát biểu là *"không phát hiện sai lệch hiệu chỉnh"*, **không được viết** *"hiệu chỉnh gần như hoàn hảo"*.

Về **lợi ích quyết định**, mô hình có lợi ích ròng dương và **vượt cả hai chiến lược tham chiếu trên toàn dải ngưỡng khảo sát (0,01–0,60)**. Khoảng cách đặc biệt lớn ở vùng ngưỡng thực tiễn: tại ngưỡng 0,10, lợi ích ròng của mô hình là 0,0461 trong khi "can thiệp tất cả" đã âm (−0,0291); tại ngưỡng 0,20 lần lượt là 0,0404 so với −0,1578. Nói cách khác, với bất kỳ mức đánh đổi chi phí hợp lý nào, dùng mô hình để chọn sinh viên can thiệp đều tốt hơn cả hai lựa chọn cực đoan.

**Liên hệ với hệ thống hai tầng.** Các ngưỡng vận hành của hai tầng ở mục 4.11 nằm trong dải này, tức là **trong vùng đã được chứng minh có lợi ích ròng dương**.

---

## 4.7 Bằng chứng định lượng về rò rỉ dữ liệu

**Bảng 4.6.** So sánh thiết kế có rò rỉ và thiết kế theo chân trời (LightGBM, kiểm định chéo phân tầng 5 fold).

| Thiết kế | Chân trời | Quần thể | Đặc trưng | AUC |
|---|---|---|---|---|
| Thiết kế cũ — toàn khóa, không lọc quần thể | HK1 | 7.514 | 25 | 0,8563 |
| Thiết kế cũ — toàn khóa, không lọc quần thể | HK1-2 | 7.514 | 36 | **0,9546** |
| Thiết kế cũ — toàn khóa, dùng cả 4 học kỳ | Đầy đủ | 7.514 | 48 | **1,0000** |
| **Chỉ một biến `GPA4_2`** (không dùng mô hình) | — | 7.514 | **1** | **0,9556** |
| Thiết kế theo chân trời (luận văn) | HK1 | 7.367 | 25 | 0,8386 |
| Thiết kế theo chân trời (luận văn) | HK1-2 | 7.034 | 36 | 0,9145 |

*Nguồn: `05_KetQua_ThongKe/leakage_validation.csv`*

### Diễn giải

Bảng trên cung cấp ba tầng bằng chứng, mỗi tầng mạnh hơn tầng trước.

**Thứ nhất, dấu hiệu hiển nhiên.** Với thiết kế cũ dùng cả bốn học kỳ, mô hình đạt **AUC = 1,0000** — phân loại hoàn hảo trên dữ liệu giáo dục vốn nhiều nhiễu. Một kết quả như vậy không thể là năng lực dự báo; nó chỉ có thể là hệ quả của việc trạng thái học kỳ 3–4 gần như trùng với nhãn.

**Thứ hai, bằng chứng quyết định.** Ở chân trời HK1-2, thiết kế cũ đạt AUC 0,9546 với 36 đặc trưng. Nhưng **riêng một biến `GPA4_2`, không qua bất kỳ mô hình nào, đã đạt 0,9556** — tức là *cao hơn* cả mô hình đầy đủ. Nói cách khác, 35 đặc trưng còn lại **không đóng góp gì**; toàn bộ khả năng phân biệt đến từ một cột duy nhất. Điều này chỉ có thể xảy ra khi cột đó là **biến thay thế của nhãn**: GPA học kỳ 2 bằng 0 hầu như chỉ xuất hiện ở nhóm đã rời trường, nên nó ghi lại *hậu quả* của việc bỏ học chứ không phải *tín hiệu* dự báo.

**Thứ ba, kết quả sau khi sửa.** Khi giới hạn quần thể về sinh viên còn hoạt động tại chân trời và chỉ dùng dữ liệu tới học kỳ *h*, AUC giảm còn 0,8386 (HK1) và 0,9145 (HK1-2). Con số **thấp hơn nhưng bảo vệ được**: nó phản ánh năng lực cảnh báo sớm thực sự trong điều kiện triển khai, khi thông tin về học kỳ sau chưa tồn tại.

### Vì sao chênh lệch này được quy cho thiết kế dữ liệu

Một phép so sánh chỉ cho phép qui kết nguyên nhân khi mọi yếu tố khác được giữ nguyên. Ở Bảng 4.6, điều đó được bảo đảm ngay trong mã nguồn: cả ba thiết kế đều dùng **cùng một thuật toán với cùng bộ siêu tham số và cùng hằng số ngẫu nhiên** (`make_lgbm`, `RANDOM_STATE = 42`), **cùng một giao thức đánh giá** (kiểm định chéo phân tầng 5 fold, xáo trộn, cùng hạt giống), **cùng một cách sinh dự báo** (ngoài fold) và **cùng một chỉ số** (AUC). Khác biệt duy nhất giữa các dòng là **cách xác định quần thể và tập đặc trưng theo thời điểm dự báo**. Vì vậy, chênh lệch quan sát được được quy cho **thiết kế dữ liệu**, không phải cho bộ phân loại hay cho quy trình đánh giá.

Cần nói thêm một điều để tránh hiểu nhầm: ở thiết kế theo chân trời, **quần thể thay đổi là có chủ ý** — chính việc giới hạn về những sinh viên còn theo học là một nửa của can thiệp, chứ không phải một biến gây nhiễu. Do đó câu hỏi "phải chăng chênh lệch chỉ vì hai tập dữ liệu khác nhau?" cần được trả lời cẩn thận, và bằng chứng thứ hai trong bảng làm được điều đó một cách dứt khoát: **kết quả `GPA4_2` đạt AUC 0,9556 được tính trên đúng quần thể 7.514 sinh viên của thiết kế cũ**, không hề đổi quần thể, không dùng mô hình nào. Nó cho thấy khả năng phân biệt của thiết kế cũ **không đến từ việc học các mẫu hình dự báo**, mà đến từ một cột duy nhất ghi lại hậu quả của nhãn. Lập luận này đứng vững ngay cả khi ta hoàn toàn bỏ qua các dòng của thiết kế mới.

> **Làm rõ kỹ thuật — vì sao con số ở hai bảng hơi khác nhau.** Các giá trị của thiết kế theo chân trời ở bảng này (0,8386 cho HK1 và 0,9145 cho HK1-2) được ước lượng bằng **một lần** kiểm định chéo 5 fold — cố ý dùng đúng phương pháp với thiết kế cũ để phép so sánh trong bảng là so sánh trực tiếp. Trong khi đó, các giá trị tương ứng ở Bảng 4.2 (0,8436 và 0,9203) dùng **kiểm định chéo lặp lại 5 × 10 rồi lấy trung bình**. Chênh lệch ở cả hai chân trời đều ≈ 0,005–0,006, nằm trong dao động do chia mẫu và không ảnh hưởng tới kết luận. Bảng 4.2 là ước lượng chính thức của luận văn; bảng này chỉ phục vụ mục đích so sánh hai thiết kế.

---

## 4.8 Độ bền theo thời gian

**Bảng 4.7.** Huấn luyện trên khóa 2020 (n = 3.159), kiểm tra trên khóa 2021 (n = 3.875), chân trời HK1-2.

| Chỉ số | Giá trị | KTC 95% |
|---|---|---|
| AUC | 0,8842 | [0,8579–0,9072] |
| AP | 0,6206 | — |
| Recall @0,5 | 0,5140 | — |
| Precision @0,5 | 0,7000 | — |

*Nguồn: `05_KetQua_ThongKe/temporal_ci.csv`*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_temporal_ci.png)

**Hình 4.6.** Hiệu năng khi chuyển khóa. *(Nguồn: tác giả.)*


### Diễn giải

Khi huấn luyện trên khóa 2020 và áp dụng cho khóa 2021, AUC đạt 0,8842 [0,8579–0,9072] — thấp hơn ước lượng gộp trong cùng khóa (0,9203) nhưng vẫn ở mức sử dụng được, và precision tại ngưỡng 0,5 giữ ở 0,70. Điều này cho thấy mô hình **không phụ thuộc chặt vào đặc thù của một khóa cụ thể**.

> ⚠️ **Hạn chế:** dữ liệu chỉ có **hai khóa**, nên đây là *một* phép kiểm chuyển khóa duy nhất. Kết quả này **không đủ** để kết luận về xu hướng trôi mô hình (model drift) theo thời gian; muốn vậy cần nhiều khóa hơn và giám sát định kỳ.

---

## 4.9 Tính công bằng giữa các nhóm

**Bảng 4.8.** Hiệu năng theo nhóm trên xác suất đã hiệu chỉnh (chân trời HK1-2).

| Thuộc tính | Nhóm | n | Tỷ lệ bỏ học nền | AUC [KTC 95%] | Recall @0,5 |
|---|---|---|---|---|---|
| Giới tính | Nữ | 4.978 | 5,20% | 0,9090 [0,8867–0,9294] | 0,4247 |
| Giới tính | Nam | 2.056 | 12,65% | 0,9156 [0,8950–0,9350] | 0,5769 |
| Dân tộc | Kinh | 6.479 | 7,33% | 0,9205 [0,9066–0,9336] | 0,5011 |
| Dân tộc | Dân tộc thiểu số | 555 | 7,93% | 0,8816 [0,8176–0,9382] | 0,5000 |

*Nguồn: `05_KetQua_ThongKe/fairness_ci.csv`*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_fairness_gap.png)

**Hình 4.7.** Chênh lệch hiệu năng giữa các nhóm. *(Nguồn: tác giả.)*


### Diễn giải

Về **khả năng phân biệt**, khoảng tin cậy của các nhóm trong cùng một thuộc tính đều **chồng lấn**: nữ 0,9090 [0,8867–0,9294] so với nam 0,9156 [0,8950–0,9350]; Kinh 0,9205 [0,9066–0,9336] so với dân tộc thiểu số 0,8816 [0,8176–0,9382]. Nói cách khác, **chưa quan sát được dấu hiệu chênh lệch** về khả năng phân biệt giữa các nhóm.

> ⚠️ **Phải đọc phát biểu trên cho đúng.** Tiêu chí sử dụng ở đây là **khoảng tin cậy của từng nhóm có chồng lấn hay không** — đây là một tiêu chí **mô tả**, *không phải* một kiểm định thống kê chính thức về chênh lệch giữa hai nhóm; nghiên cứu **không thực hiện** kiểm định như vậy. Cần lưu ý thêm rằng quan hệ giữa hai tiêu chí là **một chiều**: khoảng tin cậy *không* chồng lấn thì gần như chắc chắn có chênh lệch, nhưng khoảng tin cậy *có* chồng lấn **không** đủ để kết luận là không có chênh lệch. Vì vậy phát biểu đúng là *"chưa quan sát được chênh lệch"*, **không phải** *"đã chứng minh hai nhóm ngang nhau"*.

Về **độ nhạy tại ngưỡng 0,5**, xuất hiện chênh lệch đáng kể theo giới tính: 0,4247 ở nữ so với 0,5769 ở nam. Tuy nhiên **chênh lệch này phải được đọc kèm tỷ lệ bỏ học nền của hai nhóm**, vốn khác nhau rõ rệt (5,20% so với 12,65%). Ở cùng một ngưỡng tuyệt đối, nhóm có tỷ lệ nền thấp hơn tất yếu có ít trường hợp vượt ngưỡng hơn — hiện tượng này xảy ra **ngay cả với một mô hình hiệu chỉnh hoàn hảo** và **không tự nó là bằng chứng về thiên lệch**. Muốn kết luận chặt chẽ hơn, cần so sánh ở **cùng tỷ lệ sinh viên được cảnh báo** thay vì cùng ngưỡng tuyệt đối — đây là một hạn chế của phân tích hiện tại.

> ⚠️ Nhóm dân tộc thiểu số chỉ có **n = 555**, dẫn tới khoảng tin cậy rất rộng (0,8176–0,9382). Mọi kết luận về nhóm này phải dè dặt tương ứng. Nói riêng, **nghiên cứu không được thiết kế để chứng minh sự tương đương giữa các nhóm**: với cỡ mẫu này, một chênh lệch thực sự ở mức vừa phải vẫn có thể không bộc lộ. Nếu cỡ mẫu nhóm thiểu số tăng lên nhiều lần, kết quả **có thể thay đổi** — và đó là lý do phát biểu của luận văn dừng ở "chưa quan sát được", chứ không tiến tới "không có".
>
> ⚠️ Nhắc lại phạm vi: luận văn **đo lường và báo cáo** chênh lệch, **không áp dụng** kỹ thuật giảm thiểu (mitigation).
>
> ⚠️ **Ngưỡng dùng để đo công bằng không trùng với ngưỡng vận hành của hệ thống.** Phân tích trên đo độ nhạy tại **ngưỡng 0,5**, trong khi hệ thống cảnh báo ở mục 4.11 vận hành ở **0,10** (tầng 1) và **0,40** (tầng 2). Vì *cơ hội bình đẳng* là tính chất gắn với một ngưỡng cụ thể, kết quả ở đây **không tự động chuyển sang** hai tầng vận hành thực tế: về nguyên tắc, hệ thống có thể cân bằng ở ngưỡng 0,5 mà vẫn lệch ở 0,10 hoặc 0,40. Đây là một khoảng trống của phân tích hiện tại, được nêu lại ở mục 5.4 và khắc phục được với chi phí thấp (tính lại cùng chỉ số tại đúng hai ngưỡng vận hành).

---

## 4.10 Giải thích và độ ổn định của giải thích

**Bảng 4.9.** Chín đặc trưng ổn định nhất (lọt nhóm 10 quan trọng nhất ở ≥ 4/5 fold), chân trời HK1-2.

| Đặc trưng | SHAP tuyệt đối trung bình | SD giữa các fold | Số fold lọt top-10 |
|---|---|---|---|
| `IndustryCode` (ngành học) | 1,0985 | 0,0658 | **5/5** |
| `GPA4_2` (GPA học kỳ 2) | 0,8973 | 0,1854 | **5/5** |
| `SumScore` (tổng điểm đầu vào) | 0,2526 | 0,0242 | **5/5** |
| `Region` (khu vực) | 0,2134 | 0,0325 | **5/5** |
| `CreditRate_2` (tỷ lệ tín chỉ đạt HK2) | 0,2675 | 0,1184 | 4/5 |
| `GPA_min` (GPA thấp nhất) | 0,2530 | 0,0953 | 4/5 |
| `GPA_mean` (GPA trung bình) | 0,2499 | 0,0527 | 4/5 |
| `CumWarnings` (cảnh báo tích lũy) | 0,2178 | 0,0351 | 4/5 |
| `EntranceScore_3` | 0,1973 | 0,0240 | 4/5 |

*Nguồn: `05_KetQua_ThongKe/shap_stability.csv` (36 đặc trưng, 5 fold)*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_shap_overview.png)

**Hình 4.8.** Tổng quan giá trị SHAP. *(Nguồn: tác giả.)*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_shap_dependence_gpa2.png)

**Hình 4.9.** Quan hệ giữa GPA học kỳ 2 và giá trị SHAP. *(Nguồn: tác giả.)*

![](/Users/macvn/Projects/Master_Class/Thesis/03_KetQua_Hinh/nang_cap_thong_ke/fig_shap_stability.png)

**Hình 4.10.** Độ ổn định của giải thích qua các fold. *(Nguồn: tác giả.)*


### Diễn giải

Trong 36 đặc trưng, chỉ **9 đặc trưng lọt nhóm 10 quan trọng nhất ở từ 4/5 fold trở lên**, trong đó **4 đặc trưng ổn định ở cả 5/5 fold**: ngành học, GPA học kỳ 2, tổng điểm đầu vào và khu vực. Ngược lại, **21 trong 36 đặc trưng chưa từng lọt nhóm 10 quan trọng nhất** ở bất kỳ fold nào.

Kết quả này có hai ý nghĩa. Thứ nhất, nó **xác nhận mối lo ngại về tính bất ổn của quy gán đặc trưng** đã nêu ở mục 2.7.4: thứ hạng tầm quan trọng thay đổi giữa các lần huấn luyện, nên một biểu đồ SHAP đơn lẻ không đủ làm cơ sở diễn giải. Thứ hai, nó cho thấy vẫn tồn tại một **nhóm lõi ổn định** đủ để diễn giải một cách có kỷ luật.

Đáng chú ý, `GPA4_2` có độ lệch chuẩn giữa các fold khá cao (0,1854 trên giá trị trung bình 0,8973, tương đương khoảng 21%), nên khi diễn giải biến này cần nêu rõ mức biến thiên.

> ⚠️ Chỉ diễn giải chín đặc trưng trong bảng; phần còn lại được xem là dao động. Mọi phát biểu ở mức **liên hệ**, không phải nhân quả.

**Từ giải thích tới hành động.** Nhóm đặc trưng ổn định này chính là cơ sở để xây dựng nội dung tư vấn trong hệ thống cảnh báo hai tầng ở mục 4.11: khi một sinh viên được đưa vào danh sách, các tín hiệu thuộc nhóm này — kết quả học kỳ gần nhất, tỷ lệ tín chỉ đạt, cảnh báo học vụ tích lũy — là những điểm cố vấn nên đề cập trước. Các đặc trưng không ổn định **không được dùng làm căn cứ tư vấn**.

---

## 4.11 Hệ thống cảnh báo hai tầng

Hệ thống được xây trên **xác suất đã hiệu chỉnh bằng isotonic, thu được ngoài fold, ở chân trời HK1-2** (n = 7.034, tỷ lệ bỏ học nền 7,4%), với hai mức độ can thiệp tương ứng hai ngưỡng khác nhau. Mọi ngưỡng trong bảng dưới đây đều được áp lên **xác suất sau hiệu chỉnh** — nhắc lại điều này vì cùng một con số ngưỡng sẽ ứng với những nhóm sinh viên khác nhau nếu áp lên xác suất chưa hiệu chỉnh (mục 3.11).

**Bảng 4.10.** Hiệu năng theo dải ngưỡng vận hành.

| Ngưỡng | Số SV gắn cờ | % gắn cờ | Precision | Recall | Tầng |
|---|---|---|---|---|---|
| 0,05 | 1.769 | 25,1% | 0,256 | 0,871 | |
| **0,10** | **901** | **12,8%** | **0,424** | **0,736** | **Tầng 1 — sàng lọc rộng** |
| 0,15 | 662 | 9,4% | 0,529 | 0,674 | |
| 0,20 | 537 | 7,6% | 0,624 | 0,645 | |
| 0,25 | 475 | 6,8% | 0,674 | 0,617 | |
| 0,30 | 428 | 6,1% | 0,720 | 0,593 | |
| **0,40** | **361** | **5,1%** | **0,801** | **0,557** | **Tầng 2 — can thiệp sâu** |
| 0,50 | 311 | 4,4% | 0,836 | 0,501 | |

*Nguồn: `05_KetQua_ThongKe/warning_thresholds.csv`*

### Diễn giải

**Tầng 1 (p ≥ 0,10)** gắn cờ 901 sinh viên — khoảng 12,8% quần thể — và bắt được **73,6%** số trường hợp bỏ học thực tế, với precision 0,424. Đây là mức phù hợp cho hình thức hỗ trợ nhẹ, chi phí thấp: cố vấn học tập theo dõi và nhắc nhở. Ở mức này, cứ khoảng hai sinh viên được nhắc thì có gần một em thực sự có nguy cơ — chấp nhận được khi hình thức can thiệp không tốn kém.

**Tầng 2 (p ≥ 0,40)** thu hẹp còn 361 sinh viên (5,1%) nhưng đạt precision **0,801**: bốn trong năm sinh viên được gọi vào nhóm này thực sự bỏ học. Đây là mức phù hợp để dồn nguồn lực đắt — gặp trực tiếp, hỗ trợ tài chính hoặc tâm lý — vì tỷ lệ "làm phiền nhầm" đã thấp.

Cần nói rõ để tránh hiểu nhầm: **hai ngưỡng 0,10 và 0,40 không phải là ngưỡng tối ưu tìm được từ dữ liệu.** Chúng được ấn định trước trong mã nguồn như hai mốc minh họa cho hai mức độ can thiệp (mục 3.11), không qua bất kỳ thủ tục tối ưu hóa nào. Điều này nhất quán với nguyên tắc của luận văn là không tối ưu hóa trên chính tập dữ liệu dùng để báo cáo; và nó cũng có nghĩa là **không nên đọc hai dòng in đậm như một khuyến nghị vận hành phổ quát**. Hơn nữa, phân tích ở mục 4.6 cho thấy lợi ích ròng dương trên **toàn dải 0,01–0,60**, nên kết luận về tính hữu ích của hệ thống không phụ thuộc vào việc chọn đúng hai con số này.

Dải ngưỡng đầy đủ trong bảng cho phép mỗi trường **tự chọn ngưỡng vận hành theo năng lực tư vấn thực tế** của mình: một khoa chỉ đủ sức tiếp cận sâu khoảng 5% sinh viên có thể chọn ngưỡng 0,40; một khoa có nguồn lực rộng hơn có thể hạ xuống 0,20 để tăng độ bao phủ lên 64,5%. Toàn bộ dải này nằm trong vùng có **lợi ích ròng dương** đã xác lập ở mục 4.6.

> **Làm rõ thiết kế:** "hai tầng" ở đây là hai **mức độ can thiệp** trên cùng một mô hình HK1-2, **không phải** hai **thời điểm dự báo**. Chân trời thời gian và tầng can thiệp là hai trục độc lập. Việc mở rộng sang cảnh báo tại nhiều thời điểm liên tiếp (cảnh báo lần đầu cuối HK1, cập nhật cuối HK1-2) là **hướng nghiên cứu tiếp theo**, chưa được kiểm chứng trong luận văn này.

**Nội dung tư vấn** cho sinh viên trong cả hai tầng dựa trên nhóm đặc trưng ổn định xác định ở mục 4.10 — kết quả học kỳ gần nhất, tỷ lệ tín chỉ đạt và cảnh báo học vụ tích lũy — chứ không dựa trên toàn bộ biểu đồ tầm quan trọng đặc trưng.

---

## 4.12 Tóm tắt kết quả chính

**Bảng 4.11.** Luận điểm — bằng chứng — vị trí.

| # | Luận điểm | Bằng chứng | Mục |
|---|---|---|---|
| 1 | Rò rỉ dữ liệu làm phồng kết quả đánh giá | Thiết kế cũ: AUC 1,0000 (4 học kỳ) và 0,9546 (HK1-2); riêng một biến `GPA4_2` đạt 0,9556 — cao hơn cả mô hình 36 đặc trưng | §4.7 |
| 2 | Thiết kế theo chân trời loại được rò rỉ | Quần thể giới hạn còn 7.367 / 7.034 SV; cùng phương pháp ước lượng, AUC giảm từ 0,8563 / 0,9546 xuống 0,8386 / 0,9145 — thấp hơn nhưng bảo vệ được (ước lượng chính thức ở Bảng 4.2: 0,8436 / 0,9203) | §4.2, §4.7 |
| 3 | Ba thuật toán tương đương về khả năng phân biệt | Mọi KTC chồng lấn; 5/6 cặp không đạt ý nghĩa sau Holm | §4.3, §4.4 |
| 4 | LightGBM vượt trội về chất lượng xác suất | Brier 0,0395 so với 0,0872 (hồi quy logistic) ở HK1-2 | §4.3 |
| 5 | Tinh chỉnh mang lại cải thiện khiêm tốn | Nested CV 0,8506 ± 0,0107 so với mặc định 0,8436 (ΔAUC = +0,0070) | §4.5 |
| 6 | Xác suất sau hiệu chỉnh đáng tin | ECE 0,0339 → 0,0047 (isotonic); Brier 0,0415 → 0,0363 | §4.6 |
| 7 | Mô hình có lợi ích quyết định thực tế | Lợi ích ròng dương và vượt cả hai chiến lược tham chiếu trên toàn dải 0,01–0,60 | §4.6 |
| 8 | Mô hình bền khi chuyển khóa | 2020 → 2021: AUC 0,8842 [0,8579–0,9072] | §4.8 |
| 9 | **Chưa quan sát được** chênh lệch giữa các nhóm (không phải "đã chứng minh ngang nhau") | KTC theo nhóm đều chồng lấn; chênh lệch độ nhạy giải thích được bằng tỷ lệ nền | §4.9 |
| 10 | Giải thích có nhóm lõi ổn định | 9/36 đặc trưng lọt top-10 ở ≥ 4/5 fold; 4 đặc trưng ổn định 5/5 | §4.10 |
| 11 | Hệ thống hai tầng vận hành được | Tầng 1 (p≥0,10): 12,8% gắn cờ, recall 0,736 · Tầng 2 (p≥0,40): 5,1% gắn cờ, precision 0,801 | §4.11 |

### Diễn giải tổng hợp

Kết quả cho thấy một mô hình cảnh báo sớm **khả thi và trung thực**: với sinh viên còn theo học sau học kỳ 1, AUC đạt khoảng 0,85 và tăng lên khoảng 0,92 khi có thêm dữ liệu học kỳ 2. Quan trọng hơn con số tuyệt đối là **cách các con số này được tạo ra**: quần thể được giới hạn theo chân trời để loại rò rỉ, hiệu năng được ước lượng kèm khoảng tin cậy và kiểm định có hiệu chỉnh đa so sánh, tinh chỉnh siêu tham số được đánh giá tách biệt bằng nested CV, xác suất được hiệu chỉnh và kiểm chứng bằng lợi ích quyết định, và giải thích được kiểm tra độ ổn định thay vì mặc nhiên tin tưởng.

Một kết quả đáng chú ý về mặt phương pháp: **hồi quy logistic đạt AUC cao hơn LightGBM ở cả hai chân trời**, dù khác biệt không có ý nghĩa thống kê. Điều này không làm suy yếu luận văn mà **củng cố luận điểm trung tâm** đã nêu ở mục 2.3.5: đóng góp của nghiên cứu nằm ở **khung phương pháp chống rò rỉ và đánh giá nghiêm ngặt**, không ở việc lựa chọn thuật toán. Khung này áp dụng được cho bất kỳ bộ phân loại nào — và chính vì vậy, việc một mô hình đơn giản đạt hiệu năng tương đương là một phát hiện có giá trị, không phải điều cần che giấu.


\newpage

# Chương 5. Bàn luận và kết luận

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

