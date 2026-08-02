# Hỏi–Đáp bảo vệ luận văn (Defense Q&A)

> Chuẩn bị trước các câu hỏi phản biện có xác suất cao. Mỗi câu: **ý trả lời cốt lõi** (đủ để trả lời miệng) + gạch đầu dòng luận cứ. Ngôn ngữ trả lời khi bảo vệ: tiếng Việt. Cập nhật khi có thêm câu hỏi mới.

---

## Nhóm A — Lựa chọn mô hình

### A1. Vì sao chọn LightGBM mà không phải XGBoost?
**Cốt lõi:** Cả hai đều là GBDT mạnh trên dữ liệu bảng; luận văn chọn LightGBM vì phù hợp *đặc thù dữ liệu và mục tiêu triển khai* của bài toán, không phải vì nó "tốt hơn tuyệt đối".
- Xử lý **giá trị thiếu (NaN) native** — quan trọng vì thiết kế đặc trưng cố ý để NaN cho học kỳ không hoạt động (tách "không có dữ liệu" khỏi "trượt hết").
- Huấn luyện nhanh (histogram + leaf-wise), thuận tiện cho **nested CV** nhiều vòng và bootstrap CI vốn tốn tính toán.
- Hỗ trợ đặc trưng hạng mục và mất cân bằng lớp (`is_unbalance`) trực tiếp.
- *Phòng thủ:* có thể nói thêm rằng khác biệt hiệu năng XGBoost/LightGBM trên bài toán này thường nằm trong khoảng tin cậy — nên tiêu chí quyết định là tính thực dụng, không phải vài phần nghìn AUC.

### A3. Nếu ngày mai có nghiên cứu chứng minh CatBoost (hay mô hình khác) tốt hơn LightGBM, luận văn có phải viết lại không?
**Cốt lõi: KHÔNG.** Đóng góp của luận văn không nằm ở việc chọn bộ phân loại, mà ở **thiết kế dữ liệu horizon-aware, giao thức đánh giá nghiêm ngặt và khung triển khai hai tầng** — cả ba đều **độc lập với thuật toán**.
- LightGBM chỉ là bộ phân loại *phù hợp với bối cảnh dữ liệu này*, không phải tuyên bố "tốt nhất mọi nơi".
- Thay LightGBM bằng CatBoost/XGBoost → toàn bộ kết luận phương pháp luận (chống rò rỉ, nested CV, calibration, fairness, two-stage) **giữ nguyên**; chỉ cần chạy lại và cập nhật bảng số.
- *Câu chốt:* "Khung này áp được cho bất kỳ bộ phân loại nào; việc thay mô hình là một dòng mã, không phải một luận văn mới."

### A2. Vì sao chọn Landmarking/Horizon-aware mà không dùng LSTM/Transformer hay mô hình chuỗi thời gian?
**Cốt lõi:** Bài toán là *dự báo rủi ro sớm trên dữ liệu bảng, chuỗi rất ngắn*, ưu tiên tính minh bạch và khả năng triển khai — điều kiện mà mô hình chuỗi sâu không có lợi thế.
- Chỉ có **4 học kỳ** → chuỗi quá ngắn để LSTM/Transformer phát huy; nguy cơ quá khớp cao trên ~7.500 mẫu.
- Dữ liệu là **bảng tĩnh theo học kỳ**, không phải chuỗi mịn; GBDT vốn vượt trội trên tabular.
- Mục tiêu là **hệ thống cảnh báo tính giải thích được** cho cố vấn học tập — SHAP trên LightGBM minh bạch hơn nhiều so với mạng sâu.
- **Landmarking không mâu thuẫn với mô hình chuỗi**: nó là nguyên lý *thiết kế dữ liệu/nhãn* chống rò rỉ, có thể áp cho bất kỳ bộ phân loại nào; luận văn chọn bộ phân loại đơn giản, mạnh, dễ triển khai.
- *Phòng thủ:* thừa nhận hướng mở rộng — nếu có nhiều học kỳ hơn (6–8) và mục tiêu thuần độ chính xác, mô hình chuỗi là hướng nghiên cứu tương lai hợp lý.

---

## Nhóm B — Chống rò rỉ & thiết kế dữ liệu

### B1. Landmarking khác gì so với random split thông thường?
**Cốt lõi:** Random split trộn lẫn thời gian và quần thể → rò rỉ; landmarking cố định *thời điểm dự báo* và *quần thể còn rủi ro*, phản ánh đúng điều kiện triển khai.
- Random split có thể để một sinh viên xuất hiện với đặc trưng hậu-biến-cố trong tập huấn luyện → mô hình học "hệ quả" thay vì "tín hiệu".
- Landmarking: tại mốc *h*, chỉ giữ sinh viên còn hoạt động và chỉ dùng dữ liệu ≤ *h* → không đặc trưng nào "nhìn thấy tương lai".
- Xem Hình 2.1 (cửa sổ quan sát vs chân trời kết quả).

### B2. Horizon-aware Dataset khác gì Time-Series Classification?
**Cốt lõi:** Time-series classification thường phân loại *toàn bộ chuỗi đã hoàn tất*; horizon-aware dự báo *về tương lai từ một mốc cắt*, với quần thể động.
- TS classification: nhãn gắn với chuỗi đầy đủ → nếu áp cho dropout dễ dùng nhầm dữ liệu sau mốc.
- Horizon-aware: mỗi mốc *h* là một bài toán riêng, quần thể = người còn rủi ro tại *h*, nhãn = biến cố *sau* *h*.
- Đây chính là điểm mượn từ landmarking (van Houwelingen, 2007).

### B3. Vì sao không dùng dữ liệu cuối khóa cho chính xác hơn?
**Cốt lõi:** Vì mục tiêu là *cảnh báo sớm* để còn kịp can thiệp; dữ liệu cuối khóa không tồn tại tại thời điểm cần cảnh báo và là nguồn rò rỉ.
- Dùng GPA/ trạng thái cuối khóa = dự báo quá khứ, vô dụng cho hành động.
- Đã chứng minh bằng số liệu: AUC bị thổi phồng do rò rỉ (xem B4).

### B4. Nếu bỏ rò rỉ, độ chính xác giảm — giải thích thế nào?
**Cốt lõi:** Có, chỉ số *danh nghĩa* giảm, nhưng đó là **con số trung thực**; mô hình cũ cao giả tạo do rò rỉ, không dùng được thực tế.
- Số liệu minh họa: AUC HK1-2 khi rò rỉ ~0,95 (xấp xỉ mức chỉ riêng GPA4_2 đạt được) → sau khi sửa còn mức thấp hơn nhưng *bảo vệ được*.
- Luận điểm mấu chốt: **"chính xác hơn nhưng vô nghĩa" thua "khiêm tốn hơn nhưng triển khai được".**
- Bổ trợ bằng calibration + decision curve: mô hình sạch cho *net benefit* thực tế, mô hình rò rỉ thì không đánh giá được vì không tồn tại ở thời điểm dự báo.

### B5. "Anh chỉ thử một thuật toán. Sao kết luận được rằng thiết kế dữ liệu quan trọng hơn thuật toán nói chung?"

> ⚠️ **Câu hỏi nguy hiểm nhất về external validity. Bắt đầu bằng việc NHẬN, đừng biện hộ.**

**Bước 1 — nhận thẳng:** *"Luận văn không kiểm chứng điều đó."* Thí nghiệm rò rỉ ở mục 4.7 chỉ chạy với LightGBM; em không có bằng chứng rằng độ lớn của mức thổi phồng giữ nguyên với XGBoost, CatBoost hay mô hình học sâu.

**Bước 2 — nêu điều mình THỰC SỰ khẳng định:** luận văn không nói "thiết kế dữ liệu quan trọng hơn thuật toán", mà nói **rò rỉ xảy ra *trước khi* thuật toán bắt đầu học**. Đây là phát biểu mạnh hơn về mặt phương pháp và không cần so sánh với thuật toán nào.

**Bước 3 — bằng chứng không phụ thuộc thuật toán:** riêng biến `GPA4_2`, **không qua bất kỳ mô hình nào**, đạt AUC **0,9556** — cao hơn cả mô hình 36 đặc trưng (0,9546). Khi thông tin của nhãn đã nằm sẵn trong đặc trưng, bất kỳ bộ phân loại đủ mạnh nào cũng có nguy cơ học đúng tín hiệu đó. Con số này **không dùng LightGBM**, nên lập luận đứng vững độc lập với lựa chọn thuật toán.

**Bước 4 — đóng bằng hướng nghiên cứu:** việc lặp lại thí nghiệm với nhiều bộ phân loại đã được nêu ở mục 5.5 (hướng 12); chi phí thấp vì quy trình sẵn sàng, chỉ thay bộ phân loại.

**Câu chốt một dòng:** *"Em không khẳng định mọi thuật toán đều như nhau. Em khẳng định rằng nếu đặc trưng đã mang thông tin của nhãn thì vấn đề đã xảy ra trước khi thuật toán được chọn."*

---

## Nhóm C — Đánh giá & độ tin cậy

### C1. Vì sao chọn F1 làm chỉ số chính (không phải Accuracy)?
**Cốt lõi:** Dữ liệu **mất cân bằng** (11,5% ở HK1 và 7,4% ở HK1-2 sau khi giới hạn theo chân trời); accuracy đánh lừa, F1 cân bằng precision–recall cho lớp thiểu số.
- ⚠️ **Ba con số không được lẫn:** 13,1% (toàn khóa, n=7.514) · 11,5% (HK1, n=7.367) · 7,4% (HK1-2, n=7.034).
- Kèm AUC (phân biệt), PR-AUC, và **calibration/decision curve** cho khía cạnh quyết định.
- Bảng so sánh thuật toán (4.3) và phân tích công bằng (4.9) báo cáo **tại ngưỡng 0,5**; hệ thống cảnh báo vận hành ở **0,10 / 0,40** — hai ngưỡng này là **hằng số ấn định trước**, không tối ưu trên dữ liệu (xem D4).

### C2. Nested CV để làm gì, khác gì CV thường?
**Cốt lõi:** Tách *tinh chỉnh* khỏi *đánh giá* để tránh lạc quan do chọn siêu tham số trên cùng dữ liệu báo cáo (Cawley & Talbot, 2010).
- Vòng ngoài ước lượng hiệu năng; vòng trong (Optuna) tinh chỉnh.
- Cho biết mức "phồng" do tuning — minh bạch, tăng độ tin cậy trước hội đồng.

### C3. Calibration để làm gì nếu đã có AUC cao?
**Cốt lõi:** AUC chỉ đo *thứ tự*, không đo *độ đúng của xác suất*; muốn dùng xác suất để quyết định can thiệp thì phải hiệu chỉnh (Niculescu-Mizil & Caruana, 2005; Guo và cộng sự, 2017).

---

## Nhóm D — Công bằng, giải thích, triển khai

### D1. Hệ thống hai tầng lợi hơn một tầng ở điểm nào?
> ⚠️ **ĐÃ SỬA 19/7 — bản cũ của mục này mô tả sai thiết kế.** Trước đây viết "tầng 1 (HK1) → tầng 2 (HK1-2)", tức hai *thời điểm dự báo*. Đó **không** phải thứ mã nguồn hiện thực. Nếu trả lời theo bản cũ sẽ mâu thuẫn với mục 3.11 và 4.11 của chính luận văn.

**Cốt lõi:** Hai tầng là **hai mức độ can thiệp** đặt trên **cùng một bộ xác suất** (isotonic, HK1-2), **không phải** hai thời điểm dự báo. Một ngưỡng duy nhất buộc phải phục vụ hai mục đích mâu thuẫn — vừa "không bỏ sót ai" vừa "dồn nguồn lực đắt cho đúng người" — mà một con số không làm được cả hai.
- **Tầng 1 (p ≥ 0,10):** sàng lọc rộng, gắn cờ 12,8% quần thể, bắt được **73,6%** ca bỏ học, precision 0,424 → hỗ trợ nhẹ, chi phí thấp (cố vấn theo dõi, nhắc nhở).
- **Tầng 2 (p ≥ 0,40):** thu hẹp còn 5,1%, precision **0,801** → dồn nguồn lực đắt (gặp trực tiếp, hỗ trợ tài chính/tâm lý).
- **Chân trời thời gian và tầng can thiệp là hai trục độc lập:** chân trời quyết định *khi nào và bằng dữ liệu gì*; tầng quyết định *làm gì với dự báo*. Cảnh báo tại nhiều thời điểm liên tiếp là **hướng nghiên cứu tiếp theo**, không thuộc phạm vi luận văn.
- *Câu chốt:* "Hai tầng không phải hai lần dự báo, mà là hai mức can thiệp trên cùng một dự báo."

### D2. SHAP có phải quan hệ nhân quả không?
**Cốt lõi:** Không. SHAP giải thích *đóng góp của đặc trưng vào dự báo của mô hình*, là *tương quan/association*, không phải nhân quả. Cần nói rõ trong phần hạn chế.

### D3. Đổi trường/quốc gia thì mô hình còn dùng được không?
**Cốt lõi:** Bản thân *mô hình đã huấn luyện* gắn với dữ liệu Việt Nam; nhưng **quy trình** (horizon-aware + nested CV + calibration + fairness + two-stage) có tính khả chuyển, cần *huấn luyện lại* trên dữ liệu địa phương.
- Nhấn mạnh: đóng góp là **khung phương pháp chống rò rỉ**, không phải một mô hình cố định.
- Cảnh báo model drift theo thời gian/cohort → cần recalibrate/retrain định kỳ (hướng mở rộng).

### D4. "Ngưỡng 0,10 và 0,40 xác định TRƯỚC hay SAU khi hiệu chỉnh? Và ai chọn hai con số đó?"

> ⚠️ **Câu hỏi hai tầng — phải trả lời cả hai vế, đừng trả lời nửa đầu rồi dừng.**

**Vế 1 — trước hay sau hiệu chỉnh?** **SAU.** Ngưỡng được áp lên xác suất **đã hiệu chỉnh bằng isotonic và thu được ngoài fold**. Truy được về mã: `run_pipeline.py` gọi `warning_tiers(y2, p_iso)`, trong đó `p_iso` đến từ `oof_calibrated(..., method="isotonic")`. Nêu ở mục 3.11 và 4.11.
*Vì sao quan trọng:* nếu áp lên xác suất chưa hiệu chỉnh, cùng con số 0,40 sẽ ứng với một nhóm sinh viên khác, và phân tích lợi ích quyết định không còn áp dụng được.

**Vế 2 — ai chọn?** **Không ai tối ưu cả — đó là chủ ý.** Hai giá trị là hằng số cố định trong chữ ký hàm (`tier1=0.10, tier2=0.40`), `run_pipeline.py` gọi mà **không truyền tham số ngưỡng**. Không Optuna, không quét tìm điểm tối ưu theo F1 hay net benefit.

**Nếu bị hỏi tiếp "vậy có phải data-driven threshold không?":**
*"Không. Nếu em dò ngưỡng tối ưu trên chính tập dữ liệu dùng để báo cáo, em sẽ vi phạm đúng nguyên tắc mà cả chương 3 của em dựng lên. Hai con số này chỉ là mốc minh họa cho hai mức độ can thiệp; vì vậy Bảng 4.10 báo cáo **toàn dải ngưỡng** chứ không chỉ hai điểm, để mỗi trường tự chọn theo năng lực tư vấn."*

**Đòn chốt:** mục 4.6 cho thấy lợi ích ròng dương trên **toàn dải 0,01–0,60** — nên kết luận "hệ thống có ích" **không phụ thuộc** vào việc chọn đúng hai con số này.

### D5. "Anh nói không phát hiện chênh lệch giữa các nhóm. Có phải vì nghiên cứu không đủ power không?"

> ⚠️ **Bẫy kinh điển của gjury sạch thống kê. Câu trả lời đúng bắt đầu bằng "Có thể", không phải "Không".**

**Trả lời thẳng:** *"Có thể — và luận văn nói đúng điều đó."* Nghiên cứu **không được thiết kế để chứng minh sự tương đương** giữa các nhóm. Nhóm dân tộc thiểu số chỉ có **n = 555**, khoảng tin cậy 0,8176–0,9382 rất rộng; một chênh lệch thực sự ở mức vừa phải hoàn toàn có thể không bộc lộ với cỡ mẫu này.

**Chủ động khai thêm một điểm nữa (gây thiện cảm, và tránh bị bắt sau):** tiêu chí em dùng là **khoảng tin cậy của từng nhóm có chồng lấn hay không** — đây là tiêu chí **mô tả**, không phải kiểm định chênh lệch chính thức; em **không** chạy kiểm định giữa nhóm. Và quan hệ này là một chiều: không chồng lấn ⇒ gần như chắc chắn khác nhau, nhưng **chồng lấn ⇏ giống nhau**.

**Nếu hỏi "tăng mẫu gấp bốn thì kết quả đổi không?":** *"Có thể đổi. Vì vậy luận văn chỉ kết luận rằng trong phạm vi dữ liệu hiện có, **chưa quan sát được** bằng chứng đủ mạnh về chênh lệch."*

**Nếu hỏi "sao không dùng Equalized Odds / Demographic Parity?":** mục tiêu không phải đánh giá mọi định nghĩa công bằng trong AI, mà kiểm tra hiệu năng có đổi giữa các nhóm hay không **theo chỉ số phục vụ trực tiếp việc triển khai**. Hệ thống này **phân bổ nguồn lực hỗ trợ khan hiếm**, nên hai câu hỏi đáng quan tâm là "xếp hạng nguy cơ có kém chính xác hơn ở nhóm nào không" (AUC theo nhóm) và "tỷ lệ được đưa vào danh sách can thiệp có ngang nhau không" (độ nhạy theo nhóm — **phản ánh** tiêu chí *equal opportunity*). Xem mục 2.6.2.

**Nếu hỏi "anh đo ở ngưỡng nào?" — chủ động khai luôn:** em đo độ nhạy theo nhóm tại **ngưỡng 0,5**, trong khi hệ thống hai tầng vận hành ở **0,10** và **0,40**. Vì *equal opportunity* là tính chất gắn với một ngưỡng cụ thể, kết quả này **không tự động chuyển sang** hai tầng vận hành — em nêu đây là khoảng trống ở mục 5.4 và là hướng 11 ở mục 5.5, khắc phục được chỉ bằng cách tính lại ở đúng hai ngưỡng đó.

**Câu chốt:** *"Em báo cáo 'chưa quan sát được chênh lệch, tại ngưỡng đã đo', không báo cáo 'đã chứng minh công bằng'. Hai câu đó khác nhau, và em chỉ có bằng chứng cho câu thứ nhất."*

---

## Nhóm E — Giả định & hạn chế (chủ động nêu trước)

### E1. Hai giả định phải kiểm chứng với phòng đào tạo
- "Còn hoạt động ở HK k" ≈ `CreditsRegistered_k > 0` — thay bằng ngày thôi học chính thức nếu có.
- `TermStatus_k` được coi là **cảnh báo học vụ đã biết**; nếu thực chất là "đã thôi học" thì phải loại (đặt `DROP_TERMSTATUS=True`), vì khi đó nó là nhãn trá hình.

### E2. Hạn chế dữ liệu
- Chỉ 2 khóa đủ 4 học kỳ (2020–2021); cần thêm khóa để kiểm định temporal mạnh hơn.
- Proxy "hoạt động" bằng tín chỉ đăng ký có thể sai lệch với thực tế hành chính.

---

### Ghi chú
- Trước buổi bảo vệ, tập nói to Nhóm A2, B1, B4 — ba câu dễ bị "xoáy" nhất.
- Mỗi câu chuẩn bị 1 con số hoặc 1 hình để chỉ tay vào (Hình 2.1 cho B1–B4; bảng metrics_with_ci cho C1–C3).
