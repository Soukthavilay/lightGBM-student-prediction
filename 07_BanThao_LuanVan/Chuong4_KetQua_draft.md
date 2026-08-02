# Chương 4. Kết quả nghiên cứu

> **BẢN THẢO (DRAFT v1 — đã điền số).** Toàn bộ số liệu lấy từ lần chạy **FULL v2** ngày 2026-07-18
> (log: `06_TrungGian_Checkpoint/run_pipeline_log_2026-07-18_v2_3models.txt`, xác nhận `chế độ FULL | repeats=10, boot=2000, trials=40`).
> Hình được kết xuất lại từ notebook cùng ngày. Mọi bảng trong chương đều truy được về một tệp kết quả do `run_pipeline.py` sinh.

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

**Hình 4.1.** Khoảng tin cậy AUC theo thuật toán và chân trời. *(`fig_metric_ci.png`)*
**Hình 4.2.** Chênh lệch AUC từng cặp thuật toán. *(`fig_model_comparison.png`)*

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

**Hình 4.3.** LightGBM: tham số mặc định so với tinh chỉnh bằng nested CV. *(`fig_nested_vs_flat.png`)*

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

**Hình 4.4.** Biểu đồ độ tin cậy trước và sau hiệu chỉnh. *(`fig_calibration.png`)*
**Hình 4.5.** Đường cong quyết định. *(`fig_decision_curve.png`)*

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

**Hình 4.6.** Hiệu năng khi chuyển khóa. *(`fig_temporal_ci.png`)*

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

**Hình 4.7.** Chênh lệch hiệu năng giữa các nhóm. *(`fig_fairness_gap.png`)*

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

**Hình 4.8.** Tổng quan giá trị SHAP. *(`fig_shap_overview.png`)*
**Hình 4.9.** Quan hệ giữa GPA học kỳ 2 và giá trị SHAP. *(`fig_shap_dependence_gpa2.png`)*
**Hình 4.10.** Độ ổn định của giải thích qua các fold. *(`fig_shap_stability.png`)*

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

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- ✅ Hai `TODO` CRITICAL cũ đã khép (18/7): §4.7 nay lấy từ `leakage_validation.csv`, §4.11 từ `warning_thresholds.csv` — cả hai đều do `run_pipeline.py` sinh.
- Thay số hình/bảng tạm bằng số thật sau khi chốt bố cục; đối chiếu với `05_EvidenceTraceability_Matrix.md`.
- Kiểm tra: mọi ⚠️ trong chương đã được tôn trọng trong câu diễn giải tương ứng.
- **Cập nhật ngược Chương 2 và 3 nếu cần:** phát hiện "Brier của hồi quy logistic kém hơn 2,2 lần" là minh chứng thực nghiệm rất tốt cho lập luận ở mục 2.5.1 (phân biệt ≠ hiệu chỉnh) — cân nhắc dẫn chiếu chéo.
- Provenance: log `run_pipeline_log_2026-07-18_v2_3models.txt`.
