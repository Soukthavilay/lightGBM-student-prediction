# 2.6 Tính công bằng của mô hình dự báo bỏ học

> **BẢN THẢO (DRAFT v1)** — Phạm vi mục này **chỉ trả lời ba câu hỏi**: (1) công bằng nghĩa là gì trong bài toán dự báo bỏ học, (2) đo bằng cách nào, (3) vì sao phải đo *trước khi* đưa mô hình vào sử dụng.
> ⛔ **Không** mở rộng thành khảo luận về đạo đức AI / Responsible AI — mọi nội dung không phục vụ ba câu hỏi trên đều nằm ngoài phạm vi.
> ⚠️ Kết quả thực nghiệm thuộc Chương 4; ở đây chỉ giới thiệu khái niệm và thước đo.

## 2.6.1 Công bằng nghĩa là gì trong bài toán này

Trong dự báo bỏ học, mô hình không đưa ra phán quyết trừng phạt mà **phân bổ một nguồn lực khan hiếm**: sự chú ý của cố vấn học tập. Vì vậy khái niệm công bằng ở đây mang tính **phân bổ** (allocative): câu hỏi không phải "mô hình có đối xử tệ với nhóm nào không", mà là **"cơ hội được phát hiện và hỗ trợ kịp thời có phân bố đều giữa các nhóm sinh viên hay không"**.

Điều này dẫn tới một quan sát quan trọng về **tính bất đối xứng của sai sót**. Một *âm tính giả* (sinh viên có nguy cơ nhưng mô hình bỏ sót) đồng nghĩa với việc em đó không nhận được hỗ trợ và có thể rời trường — thiệt hại lớn và khó đảo ngược. Một *dương tính giả* (sinh viên được cảnh báo nhưng thực ra không bỏ học) chỉ tiêu tốn một buổi tư vấn không cần thiết. Do đó, trong bối cảnh cảnh báo sớm, **chênh lệch về tỷ lệ bỏ sót giữa các nhóm là mối lo ngại hàng đầu**, quan trọng hơn chênh lệch về tỷ lệ báo động giả.

Bối cảnh Việt Nam làm cho câu hỏi này cụ thể hơn: các thuộc tính như **giới tính** và **dân tộc** (đa số Kinh so với các dân tộc thiểu số) là những trục phân nhóm có ý nghĩa chính sách, nơi chênh lệch trong hệ thống hỗ trợ có thể khuếch đại bất bình đẳng vốn có.

## 2.6.2 Đo bằng cách nào

Tài liệu về công bằng thuật toán đề xuất nhiều tiêu chí nhóm khác nhau, trong đó ba nhóm phổ biến nhất là: **cân bằng hiệu năng** (mô hình phân biệt tốt như nhau ở mọi nhóm), **cơ hội bình đẳng** (equal opportunity — tỷ lệ phát hiện đúng, tức TPR/độ nhạy, ngang nhau giữa các nhóm), và **cân bằng tỷ lệ sai** (chênh lệch tỷ lệ dương tính giả hoặc âm tính giả giữa các nhóm). Cần lưu ý rằng các tiêu chí này **nhìn chung không thể thỏa mãn đồng thời** khi tỷ lệ nền giữa các nhóm khác nhau; do đó việc chọn tiêu chí là một quyết định có tính chuẩn tắc, phải được nêu rõ chứ không thể coi là kỹ thuật thuần túy.

Luận văn này sử dụng **hai thước đo, đo trên cùng bộ xác suất đã hiệu chỉnh**:

1. **AUC theo nhóm, kèm khoảng tin cậy bootstrap** — kiểm tra xem mô hình có *phân biệt* kém hơn ở nhóm nào không.
2. **Độ nhạy (recall) theo nhóm, đo tại một ngưỡng cố định** — **phản ánh** tiêu chí *cơ hội bình đẳng* (equal opportunity), trả lời trực tiếp câu hỏi "tỷ lệ sinh viên có nguy cơ được phát hiện có ngang nhau giữa các nhóm không". Cần lưu ý *cơ hội bình đẳng* là một **tính chất của hệ thống tại một ngưỡng đã chọn**, không phải bản thân một chỉ số; độ nhạy theo nhóm là đại lượng dùng để **kiểm tra** tính chất đó, và kết luận luôn gắn với đúng ngưỡng đã dùng để đo. Giá trị ngưỡng cụ thể được nêu ở mục 3.9.

Hai thước đo này được chọn vì chúng **bổ sung cho nhau ở hai tầng khác nhau**: AUC phản ánh khả năng phân biệt **độc lập với ngưỡng**, cho biết mô hình có xếp hạng nguy cơ kém chính xác hơn ở một nhóm nào đó hay không, bất kể chính sách cảnh báo được đặt ở đâu; trong khi độ nhạy tại ngưỡng vận hành phản ánh **hành vi thực tế của hệ thống khi được triển khai**, tức là tỷ lệ sinh viên có nguy cơ thực sự được đưa vào danh sách can thiệp. Một mô hình có thể công bằng ở tầng thứ nhất nhưng vẫn tạo ra chênh lệch ở tầng thứ hai; do đó chỉ đo một trong hai là chưa đủ.

Hai thuộc tính nhạy cảm được xét là **giới tính** và **dân tộc**; các nhóm có dưới 50 quan sát bị loại khỏi phân tích vì ước lượng không đủ tin cậy.

Cần phát biểu rõ phạm vi của phần này để tránh bị đọc quá rộng: **mục tiêu của luận văn không phải đánh giá mọi định nghĩa công bằng đã được đề xuất trong tài liệu về AI**, mà là kiểm tra xem hiệu năng của hệ thống có thay đổi đáng kể giữa các nhóm người học hay không, theo đúng những chỉ số phục vụ trực tiếp cho việc triển khai. Các tiêu chí khác — chẳng hạn *demographic parity* hay *equalized odds* — không được báo cáo, không phải vì chúng kém quan trọng, mà vì mỗi tiêu chí trả lời một câu hỏi chuẩn tắc khác nhau và việc chọn tiêu chí phải xuất phát từ mục đích sử dụng. Ở đây mục đích sử dụng là **phân bổ một nguồn lực hỗ trợ khan hiếm**, nên hai câu hỏi đáng quan tâm nhất là "mô hình có xếp hạng nguy cơ kém chính xác hơn ở nhóm nào không" (AUC theo nhóm) và "tỷ lệ sinh viên có nguy cơ được đưa vào danh sách can thiệp có ngang nhau không" (độ nhạy theo nhóm, phản ánh *cơ hội bình đẳng*) — đúng hai thước đo đã chọn.

Cần nêu rõ **giới hạn phạm vi**: luận văn **đo lường và báo cáo** chênh lệch giữa các nhóm, **chưa áp dụng kỹ thuật giảm thiểu** (mitigation) như adversarial debiasing hay hiệu chỉnh theo nhóm. Đây là ranh giới có chủ ý, được nêu lại ở phần hạn chế và hướng nghiên cứu tương lai.

## 2.6.3 Hạn chế cần lưu ý khi diễn giải

Thứ nhất, **so sánh ở một ngưỡng cố định có thể gây hiểu nhầm khi tỷ lệ nền khác nhau**: nếu hai nhóm có tỷ lệ bỏ học nền khác nhau, độ nhạy tại cùng một ngưỡng sẽ khác nhau ngay cả với một mô hình hiệu chỉnh hoàn hảo. Khi diễn giải, phải đọc chênh lệch độ nhạy **cùng với** tỷ lệ nền của từng nhóm.

Thứ hai, **nhóm thiểu số thường có cỡ mẫu nhỏ**, kéo theo khoảng tin cậy rộng; một chênh lệch điểm ước lượng lớn vẫn có thể không đủ bằng chứng thống kê. Kết luận về nhóm nhỏ phải dè dặt.

Thứ ba, tồn tại lo ngại phổ biến rằng cải thiện công bằng sẽ làm giảm độ chính xác. Tuy nhiên, bằng chứng thực nghiệm quy mô lớn trong lĩnh vực chính sách công của **Rodolfa, Lamba & Ghani (2021)** cho thấy đánh đổi này **thường không đáng kể** trên thực tế — nghĩa là việc đưa đánh giá công bằng vào quy trình không nhất thiết phải trả giá bằng hiệu năng.

## 2.6.4 Khoảng trống trong tài liệu dự báo bỏ học

Trong số các công trình được tổng hợp ở Bảng 2.1, chỉ một số ít có phân tích công bằng (cột *Fair*); phần lớn báo cáo hiệu năng tổng thể mà không tách theo nhóm. Trong nhóm ít ỏi có xét công bằng, hiếm công trình nào đồng thời kiểm tra xem biện pháp can thiệp vào ngưỡng hay trọng số có **phá vỡ độ hiệu chỉnh** của xác suất hay không — trong khi đây là ràng buộc trực tiếp: một xác suất đã mất tính hiệu chỉnh thì không còn dùng được cho phân tích lợi ích quyết định ở mục 2.5.

## 2.6.5 Vì sao phải đo trước khi triển khai

Ba lý do khiến việc đánh giá công bằng là **điều kiện tiên quyết**, không phải bước tùy chọn hậu kỳ.

Thứ nhất, mô hình này được thiết kế để **phân bổ nguồn lực hỗ trợ thật**; một chênh lệch độ nhạy giữa các nhóm sẽ chuyển hóa trực tiếp thành chênh lệch về cơ hội được giúp đỡ.

Thứ hai, chênh lệch **không thể phát hiện được từ chỉ số tổng thể**: một mô hình có AUC cao trên toàn bộ dữ liệu vẫn có thể bỏ sót một nhóm cụ thể một cách hệ thống. Chỉ khi tách theo nhóm, vấn đề mới lộ ra.

Thứ ba, nếu chỉ đánh giá sau khi hệ thống đã vận hành, thiệt hại — những sinh viên đã rời trường mà không được tiếp cận — là **không thể hoàn nguyên**. Đo trước khi triển khai là cách duy nhất để thiệt hại đó không xảy ra.

## 2.6.6 Chuyển tiếp

Tuy nhiên, phát hiện được chênh lệch mới chỉ là bước đầu; để hiểu **vì sao** chênh lệch xuất hiện, và để nhà trường đủ tin tưởng mà hành động dựa trên dự báo, bản thân mô hình không thể là một hộp đen. Nhu cầu này dẫn ta tới các phương pháp giải thích mô hình.

---

### Ghi chú cho vòng rà soát sau (không đưa vào bản in)
- ✅ 19/7: `Bảng 2.x` đã thay bằng **Bảng 2.1** (bảng khảo sát tài liệu, đặt ở cuối mục 2.2.4).
- **Số liệu cho Chương 4** (đã có, `fairness_ci.csv`, HK1-2): Giới tính — Nữ n=4.978 (nền 5,2%), Nam n=2.056 (nền 12,6%); Dân tộc — Kinh n=6.479, Dân tộc thiểu số n=555. Đo AUC (kèm CI) và Recall@0,5 theo nhóm.
- ⚠️ **Cảnh báo diễn giải cho Chương 4:** chênh lệch **độ nhạy theo giới tính** khá lớn ở ngưỡng 0,5, nhưng **tỷ lệ nền của hai nhóm cũng khác nhau rõ rệt** (5,2% so với 12,6%). Bắt buộc phải diễn giải hai con số cùng nhau, và cân nhắc so sánh ở **cùng tỷ lệ được cảnh báo** thay vì cùng ngưỡng tuyệt đối.
- ⚠️ Nhóm *Dân tộc thiểu số* chỉ n=555 → khoảng tin cậy rộng; kết luận phải dè dặt (nhất quán với `02_ThreatsToValidity.md`).
- Kiểm tra thuật ngữ: "cơ hội bình đẳng" (equal opportunity) dùng thống nhất toàn luận văn.
