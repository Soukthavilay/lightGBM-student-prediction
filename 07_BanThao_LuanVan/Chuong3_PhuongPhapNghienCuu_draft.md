# Chương 3. Phương pháp nghiên cứu

> **BẢN THẢO (DRAFT v1)** — Mọi tham số trong chương này được lấy trực tiếp từ mã nguồn (`dropout_research.py`, `run_pipeline.py`) ở **chế độ FULL**. Chỗ chưa xác định → `TODO`, không suy đoán.
> Chương này hiện thực hóa khung khái niệm ở Hình 2.3: mỗi mục dưới đây tương ứng một khối của khung.

---

## 3.1 Thiết kế nghiên cứu tổng thể

Nghiên cứu sử dụng thiết kế **hồi cứu, quan sát** trên dữ liệu học vụ đã có, với mục tiêu xây dựng và đánh giá một mô hình dự báo bỏ học **tại thời điểm kết thúc học kỳ *h***, dành cho những sinh viên **còn đang theo học** tại thời điểm đó.

Quy trình gồm bảy bước, tương ứng các khối của Hình 2.3: (1) chuẩn bị dữ liệu; (2) xác định quần thể và nhãn theo chân trời thời gian; (3) xây dựng đặc trưng giới hạn trong cửa sổ quan sát; (4) huấn luyện và so sánh mô hình; (5) đánh giá trung thực bằng nested cross-validation; (6) hiệu chỉnh xác suất và phân tích lợi ích quyết định; (7) kiểm định độ bền theo thời gian, tính công bằng và độ ổn định của giải thích.

Toàn bộ nghiên cứu dùng hằng số ngẫu nhiên **`RANDOM_STATE = 42`** ở mọi khâu có yếu tố ngẫu nhiên. Hình 3.1 tóm tắt toàn bộ quy trình cùng mục tương ứng của từng bước.

**Hình 3.1.** Quy trình nghiên cứu, từ dữ liệu gốc tới hệ thống cảnh báo hai tầng; mỗi khối ghi kèm mục trình bày chi tiết. *(Nguồn: tác giả; tệp `03_KetQua_Hinh/fig_3_1_quy_trinh.png`.)*

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

**Hình 3.2.** Kiểm định chéo lồng nhau: vòng ngoài chỉ dùng để đánh giá, vòng trong chỉ dùng để tinh chỉnh bằng Optuna; fold kiểm tra ngoài không tham gia vào bất kỳ bước chọn siêu tham số nào. *(Nguồn: tác giả; tệp `03_KetQua_Hinh/fig_3_2_nested_cv.png`.)*

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

`TODO` — ghi rõ quy ước nền/nhiễu loạn của `TreeExplainer` (tree-path-dependent hay interventional) để bảo đảm tái lập.

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

`TODO` — bổ sung: mã commit Git của phiên bản dùng cho luận văn, và tệp `requirements.txt`. Hai mục này sẽ được cố định sau khi phương pháp được duyệt (xem kế hoạch "đóng băng" ở phần phụ lục).

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- Mọi tham số ở chương này lấy từ **chế độ FULL**; nếu chạy lại bằng `--fast` thì các con số `n_repeats`, `n_boot`, `n_trials` sẽ khác và **không được dùng cho luận văn**.
- Đối chiếu chéo: 3.4 (bốn nhóm đặc thù dữ liệu) ↔ 2.2.3; 3.5 ↔ 2.3.3; 3.6 ↔ 2.5; 3.9 ↔ 2.6; 3.10 ↔ 2.7; 3.11 ↔ 2.8.
- **Hai `TODO` còn mở:**
  1. 🟠 **IMPORTANT — quy ước nền của `TreeExplainer` (3.10).** Ảnh hưởng tới khả năng tái lập giá trị SHAP; nên chốt trước khi in.
  2. 🟡 **NICE TO HAVE — commit Git + `requirements.txt` (3.12).** Đang giữ ở trạng thái chờ có chủ đích cho tới khi phương pháp được duyệt.
- ✅ Nguồn sinh `warning_thresholds.csv` (3.11) đã khép — `warning_tiers()` là một bước của `run_pipeline.py`.
- ✅ Đã xác minh các tệp kết quả sinh ở **chế độ FULL** (log `run_pipeline_log_2026-07-18_v2_3models.txt` ghi rõ `repeats=10, boot=2000, trials=40`).
- Sau khi đọc liền Chương 2 → Chương 3, kiểm tra thuật ngữ thống nhất: *cửa sổ quan sát*, *chân trời kết quả*, *thời điểm mốc*, *ngưỡng vận hành*, *quy gán đặc trưng*.
