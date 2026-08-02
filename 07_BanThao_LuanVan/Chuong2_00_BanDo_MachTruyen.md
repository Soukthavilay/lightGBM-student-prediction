# Bản đồ mạch truyện Chương 2 (Chapter 2 Narrative Map)

> Mục đích: bảo đảm Chương 2 đọc như **một dòng lập luận liền mạch** dẫn tới Research Gap, chứ không phải nhiều bài báo ghép lại. Mỗi mục có (a) vai trò một dòng, (b) **câu chuyển tiếp** 2–3 câu sang mục sau. Viết/sửa mỗi mục xong thì dán đúng câu chuyển tiếp này vào cuối mục để "khâu" hai mục lại.

## Sơ đồ dòng chảy

```
2.1 Dropout Prediction
      ↓  (đặt bài toán trong bối cảnh rộng hơn)
2.2 Educational Data Mining
      ↓  (dữ liệu dạng bảng → chọn mô hình)
2.3 LightGBM
      ↓  (mô hình mạnh nhưng dễ khai thác đặc trưng rò rỉ)
2.4 Data Leakage & Landmarking   ◄─── TRỤC / XƯƠNG SỐNG
      ↓  (đã trung thực về năng lực → xác suất có đáng tin?)
2.5 Calibration & Decision Curve
      ↓  (đáng tin trên tổng thể ≠ công bằng giữa các nhóm)
2.6 Fairness
      ↓  (muốn phát hiện & tin tưởng → cần minh bạch)
2.7 Explainable AI (SHAP)
      ↓  (giải thích chỉ có nghĩa khi dẫn tới hành động)
2.8 Early Warning & Intervention
      ↓  (tổng hợp: hiếm công trình làm đủ tất cả)
2.9 Research Gap
      ↓  (đã biết thiếu gì → vậy luận văn dựng gì?)
2.10 Conceptual Framework   ◄─── CẦU NỐI SANG CHƯƠNG 3
```

**Ghi chú bố cục:** mục 2.4 là trục — toàn bộ mạch uốn quanh nó. 2.1–2.3 *dẫn vào* trục (đặt bài toán, dữ liệu, mô hình → rồi lộ ra rủi ro rò rỉ). 2.5–2.8 *đi ra* từ trục (khi đã có ước lượng trung thực thì lần lượt hỏi: xác suất có đáng tin? có công bằng? có giải thích được? có hành động được?). 2.9 buộc tất cả lại thành khoảng trống, và 2.10 chuyển khoảng trống đó thành bản thiết kế — **hai mục này có chức năng khác nhau và không được gộp**: 2.9 trả lời *"còn thiếu gì"*, 2.10 trả lời *"vậy ta dựng gì"*.

---

## Vai trò + câu chuyển tiếp từng mục

### 2.1 Student Dropout Prediction
**Vai trò:** Xác định bài toán, tầm quan trọng (tỷ lệ bỏ học, hệ quả), và các hướng tiếp cận đã có.
**→ Chuyển sang 2.2:** "Dự báo bỏ học không tồn tại biệt lập mà là một ứng dụng cụ thể của một lĩnh vực rộng hơn — khai phá dữ liệu giáo dục. Đặt bài toán trong khung này giúp thấy rõ bỏ học, giữ chân (retention) và thành công học tập (student success) là ba mặt của cùng một câu hỏi, đồng thời kế thừa được các phương pháp và chuẩn mực đánh giá của lĩnh vực."

### 2.2 Educational Data Mining (EDM)
**Vai trò:** Khung lĩnh vực; các loại dữ liệu và bài toán điển hình; vì sao dữ liệu giáo dục có đặc thù riêng.
**→ Chuyển sang 2.3:** "Trong EDM, dữ liệu sinh viên chủ yếu ở dạng bảng, với đặc trưng hỗn hợp (số và hạng mục), nhiều giá trị thiếu và quan hệ phi tuyến. Chính đặc điểm này giải thích vì sao các mô hình cây tăng cường độ dốc thường tỏ ra phù hợp hơn mạng nơ-ron trên dữ liệu giáo dục, và dẫn ta tới lựa chọn mô hình của luận văn."

### 2.3 LightGBM
**Vai trò:** Vì sao chọn LightGBM (hiệu quả, xử lý NaN, phù hợp tabular); so sánh ngắn với XGBoost/mô hình khác.
**→ Chuyển sang 2.4:** "Tuy nhiên, một mô hình mạnh chỉ đáng tin khi được huấn luyện trên dữ liệu 'sạch' về mặt thời gian. Nghịch lý là chính sức mạnh khớp mẫu của LightGBM lại khiến nó dễ khai thác triệt để các đặc trưng bị rò rỉ, đẩy chỉ số lên cao một cách giả tạo. Điều này đưa ta tới vấn đề cốt lõi của luận văn: rò rỉ dữ liệu."

### 2.4 Data Leakage & Landmarking  ◄ TRỤC
**Vai trò:** Định nghĩa rò rỉ; vì sao nguy hiểm trong cảnh báo sớm; landmarking như giải pháp; định vị đóng góp (horizon-aware = hiện thực hóa landmarking).
**→ Chuyển sang 2.5:** "Sau khi loại bỏ rò rỉ để có được ước lượng năng lực trung thực, một câu hỏi mới nảy sinh: các *xác suất* mà mô hình đưa ra có đáng tin để dựa vào mà hành động không? Một mô hình phân biệt tốt (AUC cao) vẫn có thể cho xác suất lệch. Đó là vấn đề hiệu chỉnh xác suất."

### 2.5 Calibration & Decision Curve
**Vai trò:** Vì sao calibration cần cho quyết định; Platt/Isotonic; đánh giá bằng ECE/Brier; net benefit (decision curve).
**→ Chuyển sang 2.6:** "Một xác suất được hiệu chỉnh tốt *trên tổng thể* vẫn có thể sai lệch một cách hệ thống *giữa các nhóm* sinh viên khác nhau — theo giới tính, khu vực hay dân tộc. Vì một mô hình dùng để phân bổ nguồn lực hỗ trợ, sự chênh lệch đó có hệ quả đạo đức trực tiếp. Do đó, sau độ tin cậy tổng thể, ta phải xét tới tính công bằng."

### 2.6 Fairness
**Vai trò:** Khái niệm & thước đo công bằng (chênh lệch AUC/FPR/FNR giữa nhóm); các cách giảm thiểu; ràng buộc "không phá calibration".
**→ Chuyển sang 2.7:** "Để phát hiện các chênh lệch công bằng, hiểu vì sao chúng xuất hiện, và để nhà trường đủ tin tưởng mà hành động, bản thân mô hình phải minh bạch — không thể là hộp đen. Nhu cầu này dẫn ta tới các phương pháp giải thích mô hình."

### 2.7 Explainable AI (SHAP)
**Vai trò:** Vì sao cần giải thích; SHAP (và so với LIME/permutation); tính ổn định của giải thích.
**→ Chuyển sang 2.8:** "Giải thích chỉ thực sự có giá trị khi được nhúng vào một quy trình hành động cụ thể. Từ việc *dự báo* và *giải thích* nguy cơ, bước tự nhiên tiếp theo là chuyển thông tin đó thành can thiệp kịp thời — tức là các hệ thống cảnh báo sớm."

### 2.8 Early Warning & Intervention
**Vai trò:** Từ dự báo tới hỗ trợ quyết định; các hệ thống cảnh báo sớm thực tế (Course Signals…); thiết kế nhiều tầng.
**→ Chuyển sang 2.9:** "Rà soát toàn bộ các hướng trên cho thấy: hiếm công trình nào đồng thời chống được rò rỉ, đánh giá nghiêm ngặt, hiệu chỉnh xác suất, kiểm tra công bằng, giải thích được, *và* nối liền tới can thiệp. Khoảng trống tổng hợp này chính là nội dung mục tiếp theo."

### 2.9 Research Gap
**Vai trò:** Tổng hợp 4 hạn chế lặp lại → phát biểu khoảng trống → 6 đóng góp của luận văn.
**→ Chuyển sang 2.10:** "Bốn đóng góp nêu trên không rời rạc mà hợp thành một quy trình thống nhất, đi từ dữ liệu thô đến hành động can thiệp. Phần tiếp theo tóm tắt quy trình đó dưới dạng một khung khái niệm."
*(19/7: 2.9 nay liệt kê sáu nội dung chi tiết rồi **nhóm lại thành bốn đóng góp chính** cho khớp 1.6 và 5.3 — câu chuyển tiếp đếm theo bốn.)*

### 2.10 Conceptual Framework  ◄ CẦU NỐI SANG CHƯƠNG 3
**Vai trò:** Trình bày Hình 2.3 — chuỗi *Hồ sơ sinh viên → Cửa sổ quan sát → Đặc trưng theo chân trời (landmarking) → LightGBM → Nested CV → Calibration → Fairness → SHAP → Cảnh báo hai tầng → Can thiệp*. Mỗi khối tương ứng một mục đã trình bày ở Chương 2, đồng thời là bản thiết kế cho Chương 3.
**→ Chuyển sang Chương 3:** "Khung khái niệm trên đòi hỏi một thiết kế phương pháp chặt chẽ để hiện thực hóa. Chương 3 trình bày dữ liệu, quy trình xây dựng đặc trưng theo chân trời thời gian, và giao thức đánh giá tương ứng với từng khối của khung."

---

## Cách dùng để giữ mạch liền
- Trước khi viết mỗi mục 2.x, đọc lại **câu chuyển tiếp *đến* nó** (từ mục trước) và **câu chuyển tiếp *ra khỏi* nó** — mục phải mở đầu hô ứng câu trước và kết thúc dẫn tới câu sau.
- Sau khi viết đủ 2.1–2.8, đọc *một mạch chỉ các câu chuyển tiếp* nối lại: nếu chúng đọc trôi như một đoạn văn thì cả chương đã liền mạch.
- Đối chiếu chéo với [Chuong2_LiteratureMatrix.md](Chuong2_LiteratureMatrix.md): mỗi mục 2.x phải có tối thiểu 1 anchor (cột §) + vài supporting.
