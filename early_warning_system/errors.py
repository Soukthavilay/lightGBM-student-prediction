"""Mô hình lỗi Production — hệ phân cấp ngoại lệ THUẦN (chỉ stdlib).

Cùng luật với contracts.py: KHÔNG import implementation nào. Đây là bề mặt hợp
đồng, không phải logic. Ánh xạ sang mã HTTP nằm ở docs/ERROR_MODEL.md (tầng API
Sprint 2 sẽ dùng), KHÔNG nhúng ở đây để errors.py độc lập với web framework.
"""
from __future__ import annotations


class EarlyWarningError(Exception):
    """Gốc của mọi lỗi hệ thống cảnh báo. Bắt cái này = bắt tất cả lỗi domain."""


class ValidationError(EarlyWarningError):
    """Hồ sơ đầu vào không hợp lệ (thiếu cột, sai kiểu, rỗng).
    Đính kèm ValidationReport để tầng trên trả lý do cụ thể, không đoán."""
    def __init__(self, message: str, report: object | None = None) -> None:
        super().__init__(message)
        self.report = report


class ArtifactMismatchError(EarlyWarningError):
    """Artifact không khớp hợp đồng hiện tại — phát hiện lúc NẠP, không phải runtime.
    Ví dụ: contract v2 nhưng artifact xuất theo v1; hoặc MD5 dữ liệu đã đổi."""
    def __init__(self, message: str, *, expected: str | None = None,
                 found: str | None = None) -> None:
        super().__init__(message)
        self.expected = expected
        self.found = found


class PredictionError(EarlyWarningError):
    """Suy luận thất bại sau khi đầu vào đã hợp lệ (lỗi nạp mô hình, SHAP, …).
    Tách khỏi ValidationError để phân biệt 'lỗi của người dùng' với 'lỗi hệ thống'."""


class ProfileNotFoundError(EarlyWarningError):
    """Yêu cầu một PredictionProfile không tồn tại (vd chân trời chưa xuất artifact)."""


class ConfigurationError(EarlyWarningError):
    """Cấu hình sai — KHÁC với dữ liệu sai (ValidationError) và suy luận hỏng
    (PredictionError). Ví dụ: tier1 > tier2, ngưỡng âm/ngoài [0,1], thiếu config,
    profile khai báo không hợp lệ. Thường lộ ra lúc KHỞI ĐỘNG/nạp cấu hình, không
    phải theo từng yêu cầu — nên bắt sớm, dừng luôn, thay vì để chạy với config hỏng."""
