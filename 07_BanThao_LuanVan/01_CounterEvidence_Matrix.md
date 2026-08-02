# Ma trận phản biện (Counter-evidence Matrix)

> Mục đích: chủ động đưa vào tổng quan những **công trình không ủng hộ** lựa chọn của luận văn, rồi trả lời. Dùng khuôn "Mặc dù… Tuy nhiên…" (Although… However…) khi viết. Điều này khiến hội đồng khó "phục kích", vì mọi mũi công đã được nêu và phản hồi trước.
> ⚠️ Bài đánh dấu *(preprint)* cần dùng thận trọng; bài có DOI đã kiểm chứng author/năm/venue.

| # | Luận điểm của luận văn | Bằng chứng phản biện (counter) | Nguồn | Phản hồi của luận văn |
|---|---|---|---|---|
| 1 | LightGBM là lựa chọn phù hợp | Một số benchmark cho thấy LightGBM **kém ổn định** hơn XGBoost/CatBoost trên vài bộ dữ liệu (AUC thấp hơn *trước* khi tinh chỉnh) | Benchmark GBDT, arXiv:2305.17094 *(preprint)* | Sau tinh chỉnh chênh lệch nằm trong khoảng tin cậy; chọn LightGBM vì **xử lý NaN native** (khớp thiết kế đặc trưng để NaN), tốc độ thuận lợi cho nested CV + bootstrap, tái lập. Không tuyên bố "vượt trội tuyệt đối". |
| 2 | Không dùng mô hình chuỗi sâu (LSTM/Transformer) | LSTM/RNN nắm bắt phụ thuộc thời gian, đã dùng cho dropout (đặc biệt MOOC nhiều mốc thời gian) | *(không trích dẫn trong tấm bản — xem ghi chú cuối tệp)* | Chỉ **4 học kỳ** (chuỗi rất ngắn) + dữ liệu bảng cỡ vừa → mô hình cây vẫn SOTA (Grinsztajn và cộng sự, 2022); ưu tiên tính giải thích và triển khai. Landmarking áp cho *mọi* bộ phân loại → không mâu thuẫn. |
| 3 | Trên dữ liệu bảng, cây > học sâu | Nhiều kiến trúc DL tabular mới (FT-Transformer, TabR…) tuyên bố cạnh tranh được | TabR, arXiv:2307.14338 *(preprint)* | Grinsztajn và cộng sự (2022, NeurIPS) chỉ ra cây vẫn vượt trội ở dữ liệu cỡ vừa (~10K) — đúng phạm vi luận văn (~7.500 mẫu). |
| 4 | SHAP đủ tin để giải thích mô hình | Có bằng chứng **lý thuyết + thực nghiệm** rằng quy gán đặc trưng có thể bất ổn, lệch off-manifold khi đặc trưng tương quan, và *có thể thất bại* | Bilodeau, Jaques, Koh & Kim (2024), *PNAS* (DOI 10.1073/pnas.2304406120); Huang & Marques-Silva (2023) *(preprint)* | Dùng SHAP như công cụ **khám phá tương quan**, KHÔNG phải bằng chứng nhân quả (đã nêu ở hạn chế); có **phân tích độ ổn định SHAP** (`shap_stability.csv`); đối chiếu với tri thức chuyên môn; không dùng làm cơ sở quyết định duy nhất. |
| 5 | Đánh giá công bằng là cần thiết | Lo ngại phổ biến: tăng công bằng làm **giảm độ chính xác** (fairness–accuracy trade-off) | Quan điểm truyền thống về trade-off | Bằng chứng thực nghiệm cho thấy đánh đổi này **thường không đáng kể** trong chính sách công (Rodolfa, Lamba & Ghani, 2021, *Nature Machine Intelligence*, DOI 10.1038/s42256-021-00396-x) → có thể cải thiện công bằng mà không hi sinh đáng kể hiệu năng. |

---

## Câu mẫu "Mặc dù… Tuy nhiên…" (dán vào tổng quan)

- **(LightGBM)** "Mặc dù một số benchmark cho thấy LightGBM kém ổn định hơn XGBoost hay CatBoost trên vài bộ dữ liệu, *tuy nhiên* sau khi tinh chỉnh siêu tham số, chênh lệch thường nằm trong khoảng tin cậy; luận văn chọn LightGBM vì khả năng xử lý giá trị thiếu native phù hợp với thiết kế đặc trưng và vì tốc độ thuận lợi cho nested cross-validation."
- **(LSTM/Transformer)** "Mặc dù các mô hình chuỗi như LSTM và Transformer nắm bắt tốt phụ thuộc thời gian, *tuy nhiên* trên dữ liệu bảng cỡ vừa, mô hình cây vẫn giữ vị thế dẫn đầu (Grinsztajn và cộng sự, 2022); với chuỗi chỉ gồm bốn học kỳ, lợi thế của mô hình chuỗi không hiện rõ, trong khi tính giải thích và khả năng triển khai lại quan trọng hơn."
- **(SHAP)** "Mặc dù có bằng chứng lý thuyết rằng các phương pháp quy gán đặc trưng như SHAP có thể bất ổn hoặc không trung thực trong một số điều kiện (Bilodeau và cộng sự, 2024), *tuy nhiên* luận văn sử dụng SHAP như một công cụ khám phá *tương quan* chứ không phải bằng chứng nhân quả, đồng thời kiểm tra độ ổn định của giải thích qua nhiều lần lặp."
- **(Fairness)** "Mặc dù thường có lo ngại rằng tăng tính công bằng sẽ làm giảm độ chính xác, *tuy nhiên* bằng chứng thực nghiệm trong lĩnh vực chính sách công cho thấy đánh đổi này thường không đáng kể (Rodolfa và cộng sự, 2021)."

---

## Anchor phản biện — thư mục (cần bổ sung vào `anchor_refs.bib` nếu dùng)
- Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). *Why do tree-based models still outperform deep learning on tabular data?* NeurIPS 2022 (Datasets & Benchmarks). arXiv:2207.08815.
- Bilodeau, B., Jaques, N., Koh, P. W., & Kim, B. (2024). *Impossibility theorems for feature attribution.* PNAS, 121(2). DOI 10.1073/pnas.2304406120.
- Rodolfa, K. T., Lamba, H., & Ghani, R. (2021). *Empirical observation of negligible fairness–accuracy trade-offs in machine learning for public policy.* Nature Machine Intelligence, 3, 896–904. DOI 10.1038/s42256-021-00396-x.
- ⛔ **KHÔNG đưa vào danh mục tài liệu tham khảo** — Fei, M., & Yeung, D.-Y. (2015). *Temporal Models for Predicting Student Dropout in MOOCs.* IEEE ICDM Workshops. Đã gỡ khỏi tấm bản ngày 19/7 (chỉ là *existence claim*, không đỡ lập luận nào). Giữ ở đây **chỉ để trả lời miệng** nếu hội đồng hỏi "đã có ai dùng mô hình chuỗi chưa"; nếu nêu tên, phải nói rõ là dẫn từ trí nhớ về tài liệu và **chưa đối chiếu bản gốc**.
- *(preprint, dùng thận trọng)* Benchmark GBDT — arXiv:2305.17094; TabR — arXiv:2307.14338; Huang & Marques-Silva — arXiv:2302.08160.
