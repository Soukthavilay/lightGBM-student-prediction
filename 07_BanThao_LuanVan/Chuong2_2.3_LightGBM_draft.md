# 2.3 LightGBM và cơ sở lựa chọn mô hình

> **BẢN THẢO (DRAFT v2)** — Nguyên tắc viết mục này: **giải thích *lý do chọn* LightGBM cho khung nghiên cứu này, KHÔNG dạy lại LightGBM là gì.** Tránh mọi tuyên bố kiểu "tốt nhất"; chỉ dùng "phù hợp / thích hợp / hiệu quả trong bối cảnh này".
> **Phép thử thành công của mục này:** đọc xong, người đọc phải tự trả lời được câu hỏi *"nếu ngày mai có nghiên cứu chứng minh CatBoost tốt hơn LightGBM, luận văn này có phải viết lại không?"* — câu trả lời phải là **không**.

## 2.3.1 Cây tăng cường độ dốc — định vị trong họ mô hình

Tăng cường độ dốc (gradient boosting) xây dựng mô hình theo hướng cộng dồn: mỗi cây quyết định mới được huấn luyện để giảm phần dư mà tổ hợp các cây trước còn để lại. Khác với rừng ngẫu nhiên vốn huấn luyện các cây độc lập rồi lấy trung bình, gradient boosting huấn luyện **tuần tự và có định hướng** — nhờ đó thường đạt độ chính xác cao hơn trên dữ liệu dạng bảng, đổi lại nhạy cảm hơn với siêu tham số. Trong khoảng một thập kỷ trở lại đây, họ mô hình này, với ba hiện thực tiêu biểu là XGBoost, LightGBM và CatBoost, đã trở thành lựa chọn phổ biến cho bài toán phân loại trên dữ liệu bảng.

## 2.3.2 LightGBM

LightGBM (Ke và cộng sự, 2017) là một hiện thực gradient boosting hướng tới tốc độ và hiệu quả bộ nhớ. Ở mức khái quát, hai đặc điểm đủ để hiểu vị trí của nó trong luận văn này: mô hình dùng **biểu đồ tần suất (histogram)** để rời rạc hóa giá trị liên tục khi tìm điểm chia, và phát triển cây theo hướng **leaf-wise** — mở rộng lá có mức giảm mất mát lớn nhất, thay vì mở rộng đều theo tầng. Các tối ưu hóa chi tiết khác của thư viện nằm ngoài phạm vi luận văn và có thể tham khảo trực tiếp ở công trình gốc.

## 2.3.3 Vì sao phù hợp với dữ liệu của nghiên cứu này

Bốn đặc điểm của bộ dữ liệu quyết định lựa chọn mô hình:

1. **Dữ liệu dạng bảng, quy mô trung bình.** Tập phân tích gồm 7.367 sinh viên với 25 đặc trưng ở chân trời HK1, và 7.034 sinh viên với 36 đặc trưng ở chân trời HK1-2 (trong đó 6 đặc trưng hạng mục). Đây là quy mô mà mô hình cây tỏ ra thích hợp, và LightGBM hỗ trợ đặc trưng hạng mục trực tiếp, không bắt buộc mã hóa one-hot.
2. **Giá trị thiếu là *có chủ đích*, không phải lỗi dữ liệu.** Thiết kế đặc trưng của luận văn cố ý gán `NaN` cho các học kỳ mà sinh viên không hoạt động (8 cột chứa `NaN` ở cả hai chân trời), nhằm tách bạch "không có dữ liệu" khỏi "trượt toàn bộ". LightGBM học hướng đi mặc định cho `NaN` ngay ở mức thuật toán, cho phép **giữ nguyên sự phân biệt này** — trong khi các mô hình nền phải điền khuyết (thực hiện trong từng fold để tránh rò rỉ).
3. **Tương tác phi tuyến giữa các học kỳ.** Nguy cơ bỏ học không phụ thuộc tuyến tính vào từng chỉ số đơn lẻ mà vào tương tác giữa chúng (ví dụ điểm trung bình thấp *kết hợp* tỷ lệ tín chỉ đạt giảm dần). Mô hình cây nắm bắt các tương tác này mà không cần đặc tả trước.
4. **Mất cân bằng lớp.** Tỷ lệ bỏ học sau chân trời là 11,5% (HK1) và 7,4% (HK1-2) — càng dự báo muộn, lớp dương càng hiếm. LightGBM cho phép bù mất cân bằng (`is_unbalance`) tính **trên đúng phần dữ liệu đang khớp**, nhất quán với nguyên tắc "mọi thao tác đều thực hiện trong fold" của luận văn.

Ngoài ra, là mô hình cây, LightGBM tương thích với `TreeExplainer` của SHAP, cho phép tính giá trị SHAP nhanh và chính xác — điều kiện cần cho mục tiêu xây dựng một hệ thống cảnh báo mà cố vấn học tập có thể hiểu và tin tưởng (xem 2.7).

## 2.3.4 Bằng chứng phản biện: không mô hình nào vượt trội trong mọi bối cảnh

Bảng 2.2 đối chiếu bốn lựa chọn thay thế thường được nêu ra, cùng lập luận ủng hộ và lý do chưa phù hợp với bối cảnh của nghiên cứu này.

**Bảng 2.2.** Các lựa chọn mô hình thay thế và cơ sở phản biện. *(Nguồn: tác giả tổng hợp.)*

| Lựa chọn thay thế | Lập luận ủng hộ nó | Vì sao chưa phù hợp ở đây |
|---|---|---|
| XGBoost / CatBoost | Một số benchmark ghi nhận ổn định hơn LightGBM trên vài bộ dữ liệu, nhất là **trước** khi tinh chỉnh | Sau tinh chỉnh, khác biệt giữa ba thư viện thường thu hẹp đáng kể |
| Học sâu cho dữ liệu bảng (FT-Transformer, TabR) | Liên tục được đề xuất với tuyên bố cạnh tranh được | Grinsztajn và cộng sự (2022) khảo sát 45 bộ dữ liệu: mô hình cây vẫn dẫn đầu ở quy mô ~10.000 mẫu — đúng phạm vi luận văn |
| Mô hình chuỗi (LSTM/Transformer) | Nắm bắt phụ thuộc thời gian, phù hợp khi chuỗi quan sát đủ dài | Chuỗi ở đây chỉ gồm **4 học kỳ** — quá ngắn để phát huy lợi thế, trong khi nguy cơ quá khớp tăng |
| Hồi quy logistic | Rất dễ diễn giải | Giả định tuyến tính, khó nắm tương tác giữa các học kỳ |

Tổng hợp lại, các bằng chứng trên cho thấy **không có mô hình nào vượt trội trong mọi bối cảnh**; hiệu năng tương đối phụ thuộc vào đặc điểm dữ liệu, quy mô mẫu và mục tiêu sử dụng.

## 2.3.5 Kết luận lựa chọn

Do đó, luận văn **không chọn LightGBM vì cho rằng đây là mô hình tốt nhất trong mọi bối cảnh**, mà vì nó phù hợp đồng thời với ba yếu tố: **đặc điểm dữ liệu** (dạng bảng, quy mô trung bình, giá trị thiếu có chủ đích, mất cân bằng lớp), **mục tiêu giải thích kết quả** (tương thích SHAP để phục vụ cố vấn học tập), và **khung đánh giá mà nghiên cứu này đề xuất** (chi phí tính toán chấp nhận được cho kiểm định chéo lặp lại, bootstrap và nested cross-validation).

Điều quan trọng cần nhấn mạnh: **đóng góp của luận văn không nằm ở việc lựa chọn bộ phân loại.** Khung thiết kế dữ liệu chống rò rỉ trình bày ở mục tiếp theo **độc lập với thuật toán** — có thể áp dụng nguyên vẹn cho XGBoost, CatBoost hay bất kỳ mô hình phân loại nào khác. Nếu một nghiên cứu tương lai chứng minh một thư viện khác phù hợp hơn với dữ liệu này, kết luận phương pháp luận của luận văn vẫn giữ nguyên giá trị; chỉ bộ phân loại được thay thế.

## 2.3.6 Chuyển tiếp

Tuy nhiên, chọn được mô hình phù hợp mới chỉ là một nửa vấn đề. **Nếu thiết kế dữ liệu không đúng, mô hình vẫn có thể học từ những thông tin rò rỉ từ tương lai** — và nghịch lý là, chính năng lực khớp mẫu mạnh của các mô hình như LightGBM lại khiến chúng khai thác các đặc trưng rò rỉ triệt để hơn, đẩy chỉ số đánh giá lên cao một cách giả tạo. Điều này đưa ta tới vấn đề cốt lõi của luận văn: rò rỉ dữ liệu.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- ✅ Số liệu ở 2.3.3 đã lấy từ dữ liệu thật (chạy `horizon_dataset`): HK1 n=7.367/25 đặc trưng/11,46%; HK1-2 n=7.034/36 đặc trưng/7,38%; 8 cột chứa `NaN`. **Lưu ý:** tỷ lệ **13,1%** (7.514 SV) là của *toàn khóa trước khi giới hạn theo chân trời* — không dùng lẫn ba con số 13,1% / 11,5% / 7,4%.
- Bổ sung trích dẫn peer-reviewed cho benchmark GBDT (hiện chỉ có preprint arXiv:2305.17094) hoặc diễn đạt trung tính hơn.
- ✅ 19/7: đã gỡ trích dẫn Fei & Yeung (2015) khỏi bảng 2.3.4. Nó chỉ đóng vai trò "đã từng có người dùng LSTM cho MOOC" — một *existence claim* ở cột lập luận đối lập, không đỡ lập luận nào của luận văn. Phần phản biện đứng trên đặc điểm dữ liệu (chuỗi 4 học kỳ) và Grinsztajn và cộng sự (2022), nên vẫn nguyên vẹn. **Không thêm lại.**
- Số liệu giao thức đánh giá nhắc ở 2.3.5 phải khớp Chương 3 (5×10 CV, bootstrap 2.000, nested 40 trials).
