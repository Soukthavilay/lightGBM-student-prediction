# 2.7 Giải thích mô hình (Explainable AI)

> **BẢN THẢO (DRAFT v1)** — Nguyên tắc diễn đạt của mục này: SHAP **ước lượng mức đóng góp của đặc trưng vào một dự báo cụ thể trong khuôn khổ giá trị Shapley** — KHÔNG viết "SHAP giải thích mô hình" hay "SHAP cho biết nguyên nhân bỏ học".
> ⚠️ Kết quả thực nghiệm thuộc Chương 4; ở đây chỉ trình bày khái niệm, hạn chế và cơ sở lựa chọn.

## 2.7.1 Vì sao mô hình cần giải thích được

Trong một hệ thống cảnh báo sớm, kết quả dự báo không tự nó tạo ra giá trị; giá trị chỉ xuất hiện khi một cố vấn học tập **hành động** dựa trên kết quả đó. Điều này đặt ra ba yêu cầu về tính minh bạch.

Thứ nhất, **hành động cần định hướng**: biết một sinh viên có nguy cơ 30% là chưa đủ để tư vấn; người cố vấn cần biết tín hiệu nào đang đẩy con số đó lên — kết quả học tập sa sút, tỷ lệ tín chỉ đạt thấp, hay cảnh báo học vụ tích lũy — để chọn hình thức hỗ trợ phù hợp.

Thứ hai, **kiểm tra tính hợp lý của mô hình**: việc rà soát những đặc trưng có ảnh hưởng lớn là một cơ chế phát hiện sai sót, đặc biệt là phát hiện các đặc trưng có dấu hiệu rò rỉ. Nếu một biến lẽ ra không mang thông tin dự báo lại chi phối mô hình, đó là chỉ dấu cần điều tra lại thiết kế dữ liệu (liên hệ mục 2.4).

Thứ ba, **điều kiện để được chấp nhận**: một hệ thống mà nhà trường không hiểu cách vận hành sẽ khó được tin tưởng và khó đưa vào quy trình thực tế.

## 2.7.2 SHAP làm gì

SHAP (Lundberg & Lee, 2017) đặt bài toán quy gán đặc trưng vào khuôn khổ **giá trị Shapley** của lý thuyết trò chơi hợp tác: mỗi đặc trưng được coi như một "người chơi", còn dự báo của mô hình là "phần thưởng" cần phân chia. Giá trị SHAP của một đặc trưng là **mức đóng góp của nó vào chênh lệch giữa dự báo cho một quan sát cụ thể và một giá trị tham chiếu (baseline)**.

Cần phát biểu chính xác: SHAP **không tiết lộ cơ chế bên trong mô hình**, mà **ước lượng một phép phân bổ đóng góp** cho từng dự báo riêng lẻ. Với mô hình cây, `TreeExplainer` tính các giá trị này trực tiếp và hiệu quả, thay vì ước lượng bằng lấy mẫu như các phiên bản model-agnostic.

Chính đặc tính **giải thích ở cấp độ từng quan sát** này khiến SHAP phù hợp với một hệ thống cảnh báo sớm. Cố vấn học tập không cần biết "đặc trưng nào quan trọng nói chung", mà cần trả lời được câu hỏi rất cụ thể: *"vì sao sinh viên này xuất hiện trong danh sách cần quan tâm, và tín hiệu nào nên được đề cập trước trong buổi tư vấn?"* Đây là câu hỏi ở cấp độ từng trường hợp — và là mắt xích nối giữa mô hình dự báo với hành động can thiệp sẽ bàn ở mục 2.8 (xem Hình 2.2).

## 2.7.3 SHAP không phải quan hệ nhân quả

Đây là ranh giới quan trọng nhất cần giữ. Giá trị SHAP mô tả **hành vi của mô hình**, không mô tả **thế giới thực**. Nói rằng "GPA học kỳ 2 có giá trị SHAP lớn" chỉ có nghĩa: *trong mô hình này*, biến GPA học kỳ 2 đóng góp nhiều vào việc đẩy dự báo lên hay xuống. Nó **không** cho phép kết luận rằng nâng GPA của một sinh viên lên sẽ làm giảm nguy cơ bỏ học của em đó — bởi GPA có thể chỉ là *dấu hiệu* của những nguyên nhân sâu hơn (khó khăn kinh tế, sức khỏe, sự phù hợp ngành học) mà mô hình không quan sát được.

Vì vậy, mọi phát biểu dựa trên SHAP trong luận văn được diễn đạt ở mức **liên hệ (association)**, không phải nhân quả; và các đề xuất can thiệp được trình bày như **giả thuyết cần kiểm chứng**, không phải kết luận nhân quả.

## 2.7.4 Hạn chế của phương pháp quy gán đặc trưng

Tài liệu gần đây đã chỉ ra những giới hạn nghiêm túc, cần được nêu thay vì bỏ qua.

**Giới hạn lý thuyết.** Bilodeau, Jaques, Koh & Kim (2024) chứng minh rằng, với các lớp mô hình đủ phong phú, **mọi phương pháp quy gán đặc trưng thỏa mãn tính đầy đủ và tuyến tính — bao gồm SHAP — có thể không tốt hơn đoán ngẫu nhiên** khi dùng để suy ra một số tính chất hành vi của mô hình. Đây là kết quả bất khả thi, nghĩa là không thể khắc phục bằng cách cải tiến thuật toán.

**Tính bất ổn.** Giá trị quy gán có thể thay đổi giữa các lần huấn luyện lại với hạt giống hoặc phân chia dữ liệu khác nhau; ở các phiên bản dựa trên lấy mẫu, còn có thêm dao động do chính quá trình lấy mẫu.

**Đặc trưng tương quan.** Khi các đặc trưng phụ thuộc lẫn nhau — điều hiển nhiên với các chỉ số học tập qua nhiều học kỳ — việc "loại bỏ" một đặc trưng trong khuôn khổ Shapley có thể tạo ra những tổ hợp không tồn tại trong thực tế, khiến đóng góp bị phân bổ lệch giữa các biến tương quan.

**Phụ thuộc tham chiếu.** Giá trị SHAP luôn được định nghĩa *tương đối với một baseline*; thay đổi phân phối tham chiếu sẽ thay đổi con số.

**Khoảng trống trong tài liệu.** Trong số các công trình được tổng hợp ở Bảng 2.1, nhiều công trình có sử dụng SHAP (cột *XAI*), nhưng phần lớn trình bày một biểu đồ tầm quan trọng đặc trưng duy nhất, **không kiểm tra độ ổn định của giải thích** qua các lần huấn luyện và không nêu giới hạn nhân quả.

## 2.7.5 Vì sao luận văn vẫn chọn SHAP

Lựa chọn SHAP ở đây được đưa ra **cùng với các biện pháp phòng vệ tương ứng với từng hạn chế nêu trên**.

1. **Dùng đúng mục đích.** SHAP được dùng như công cụ **mô tả và truyền đạt** cho cố vấn học tập, không phải bằng chứng nhân quả và không phải cơ sở cho quyết định tự động. Kết quả bất khả thi của Bilodeau và cộng sự (2024) nhắm vào việc dùng quy gán để *suy ra tính chất hành vi của mô hình*; nó không phủ nhận giá trị của SHAP như một phương tiện diễn đạt có kỷ luật, miễn là không bị đọc quá mức.
2. **Tránh dao động do lấy mẫu.** Vì mô hình là tổ hợp cây, luận văn dùng `TreeExplainer` — tính trực tiếp thay vì ước lượng bằng lấy mẫu, do đó không chịu nguồn bất ổn đặc thù của các biến thể model-agnostic.
3. **Kiểm tra độ ổn định một cách tường minh.** Thay vì giả định giải thích là ổn định, luận văn **đo nó**: tính giá trị SHAP trên nhiều fold độc lập, rồi báo cáo với mỗi đặc trưng cả **mức đóng góp trung bình**, **độ lệch chuẩn giữa các fold**, và **số lần đặc trưng lọt vào nhóm 10 quan trọng nhất**. Chỉ những đặc trưng ổn định qua các fold mới được đưa ra diễn giải; phần còn lại được xem là dao động. Đây chính là câu trả lời trực tiếp cho phê phán về tính bất ổn.
4. **So với các lựa chọn khác.** LIME (Ribeiro và cộng sự, 2016) xây dựng mô hình thay thế cục bộ và được biết là kém ổn định giữa các lần chạy; tầm quan trọng theo hoán vị chỉ cho cái nhìn toàn cục, không giải thích được từng trường hợp — trong khi hệ thống cảnh báo cần giải thích ở cấp độ **từng sinh viên**.

**Hình 2.2.** Vai trò của giải thích trong chuỗi từ dự báo tới can thiệp: xác suất nguy cơ → quy gán SHAP ở cấp độ từng sinh viên → chỉ giữ các đặc trưng ổn định qua các fold → cố vấn học tập hiểu được lý do → can thiệp đúng vấn đề. Hai nửa của chuỗi tương ứng với "mô hình + giải thích" và "con người + hành động". *(Nguồn: tác giả; tệp `03_KetQua_Hinh/fig_2_7_shap_to_intervention.png`.)*

## 2.7.6 Chuyển tiếp

Tuy nhiên, một giải thích chỉ thực sự có giá trị khi được nhúng vào một quy trình hành động cụ thể. Từ việc **dự báo** nguy cơ và **diễn giải** các tín hiệu dẫn tới nguy cơ đó, bước tự nhiên tiếp theo là chuyển thông tin thành can thiệp kịp thời — tức là các hệ thống cảnh báo sớm.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- ✅ 19/7: `Bảng 2.x` đã thay bằng **Bảng 2.1** (bảng khảo sát tài liệu, đặt ở cuối mục 2.2.4).
- **Số liệu cho Chương 4** (đã có, `shap_stability.csv`, HK1-2, 5 fold, 36 đặc trưng): chỉ **4 đặc trưng lọt top-10 ở cả 5/5 fold** (IndustryCode, GPA4_2, SumScore, Region), 5 đặc trưng ở 4/5 fold, và **21 đặc trưng chưa bao giờ lọt top-10**.
- 💡 **Gợi ý diễn giải cho Chương 4:** đây là bằng chứng ủng hộ cách viết thận trọng — nên diễn giải **nhóm lõi ~9 đặc trưng ổn định** (top10_freq ≥ 4) và mô tả phần còn lại là dao động, thay vì bình luận từng đặc trưng trong biểu đồ. Lưu ý `GPA4_2` có độ lệch chuẩn tương đối cao (≈0,19 trên trung bình ≈0,90) → nhắc tới độ biến thiên khi diễn giải biến này.
- Cân nhắc nêu rõ quy ước baseline/perturbation của `TreeExplainer` (tree-path-dependent hay interventional) trong Chương 3 để bảo đảm tái lập.
- Kiểm tra thuật ngữ: "quy gán đặc trưng" (feature attribution) dùng thống nhất toàn luận văn.
