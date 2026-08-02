# ADR 0004 — Một điểm vào công khai (Predictor), nhiều chặng nội bộ

**Trạng thái:** Đã chấp nhận · 2026-07-19

## Bối cảnh
Luồng suy luận có nhiều chặng: validate → build đặc trưng → score → calibrate → tier → explain. Nếu tầng API phải gọi từng chặng, thì API biết quá nhiều về bên trong; đổi số chặng (vd tách hay gộp hiệu chỉnh) sẽ phá vỡ mọi nơi gọi.

## Quyết định
Tầng API **chỉ thấy MỘT hợp đồng công khai**: `Predictor` với một phương thức `predict(raw, top_k) -> Sequence[PredictionResult]`. Các chặng (RiskScorer, Calibrator, TierPolicy, Explainer, FeatureBuilder, Validator) là **hợp đồng nội bộ** — `Predictor` tự ghép, API không gọi trực tiếp. Một hiện thực được phép hợp nhất các chặng liền kề (vd `CalibratedClassifierCV` gộp score + calibrate).

## Hệ quả
- (+) Đổi số chặng bên trong → tầng API không đổi.
- (+) API chỉ cần học một phương thức; hợp đồng đầu ra (`PredictionResult`) là thứ duy nhất API phụ thuộc.
- (+) Vẫn giữ được sự phân tách nội bộ để test từng chặng và để nói rõ trách nhiệm.
- (−) `Predictor` trở thành điểm hội tụ — cần giữ nó mỏng (chỉ điều phối), không nhồi logic.
- Tài liệu liên quan: `DESIGN.md` §3, `contracts.py` (mục "Hợp đồng CÔNG KHAI").
