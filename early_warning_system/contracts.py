"""Hợp đồng Production (contracts) — interface-first, ỔN ĐỊNH.

QUY TẮC BẤT DI BẤT DỊCH của tệp này (xem RULES.md):
  - CHỈ import thư viện chuẩn (typing, dataclasses).
  - KHÔNG biết tên bất kỳ hiện thực nào: không "dropout_research", không sklearn,
    không lightgbm/shap/pandas, không artifact. Sự trong sạch này khiến hợp đồng
    độc lập với phương pháp hiện tại — methodology đổi thì tệp này KHÔNG đổi.

Phân tầng hợp đồng:
  • DTO            — hình dạng dữ liệu vào/ra, bất biến.
  • Hợp đồng NỘI BỘ — các chặng ghép lại: Validator, FeatureBuilder, RiskScorer,
                      Calibrator, TierPolicy, Explainer. Tầng API KHÔNG gọi chúng.
  • Hợp đồng CÔNG KHAI — `Predictor`: điểm vào DUY NHẤT mà API được phép gọi.
                      Bên trong Predictor tự ghép các chặng; API không biết có
                      mấy chặng.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, Sequence, runtime_checkable

# ─────────────────────────── Phiên bản hợp đồng ──────────────────────────────
# SemVer. Quy ước tương thích: cùng số MAJOR ⇒ tương thích.
# Artifact ghi lại phiên bản nó được xuất dựa trên; lúc nạp, so với hằng số này
# để phát hiện lệch (API v2 nhưng artifact v1) NGAY, thay vì lỗi lúc runtime.
CONTRACT_VERSION = "1.0.0"


def _major(v: str) -> int:
    return int(v.split(".")[0])


def is_compatible(artifact_version: str) -> bool:
    """True nếu artifact khớp MAJOR của hợp đồng hiện tại. Thuần logic, không nâng lỗi.
    (Việc NÂNG ArtifactMismatchError để cho loader/adapter — xem errors.py.)"""
    try:
        return _major(artifact_version) == _major(CONTRACT_VERSION)
    except (ValueError, AttributeError, IndexError):
        return False


# ─────────────────────────── DTO (hợp đồng dữ liệu) ───────────────────────────

TIER_NONE, TIER_SCREEN, TIER_DEEP = 0, 1, 2
TIER_LABELS = {
    TIER_NONE: "Không cảnh báo",
    TIER_SCREEN: "Tầng 1 — sàng lọc rộng",
    TIER_DEEP: "Tầng 2 — can thiệp sâu",
}


@dataclass(frozen=True)
class PredictionProfile:
    """Một cấu hình dự báo — hệ thống chỉ biết 'Profile', KHÔNG biết 'HK1'/'HK1-2'.

    Thêm chân trời mới (HK3, học kỳ 6…) = thêm một Profile, KHÔNG sửa kiến trúc.
    `name` chỉ là nhãn hiển thị; logic không được rẽ nhánh theo giá trị của nó."""
    name: str
    horizon: int
    artifact_dir: str


@dataclass(frozen=True)
class FeatureContribution:
    """Một đặc trưng đóng góp vào dự báo của MỘT sinh viên (theo SHAP)."""
    feature: str
    value: float | None          # giá trị đặc trưng (None nếu thiếu — học kỳ không hoạt động)
    shap: float                  # đóng góp SHAP (dương = đẩy rủi ro lên)

    @property
    def direction(self) -> str:
        return "tăng rủi ro" if self.shap > 0 else "giảm rủi ro"


@dataclass(frozen=True)
class PredictionResult:
    """Kết quả cho MỘT sinh viên — hợp đồng đầu ra bất biến (xem DESIGN.md §2)."""
    student_id: str
    probability: float           # ∈ [0,1], ĐÃ hiệu chỉnh
    tier: int                    # TIER_NONE | TIER_SCREEN | TIER_DEEP
    top_features: Sequence[FeatureContribution]

    @property
    def tier_label(self) -> str:
        return TIER_LABELS[self.tier]

    def to_dict(self) -> dict[str, Any]:
        return {
            "student_id": self.student_id,
            "probability": round(self.probability, 4),
            "tier": self.tier,
            "tier_label": self.tier_label,
            "top_features": [
                {"feature": f.feature, "value": f.value,
                 "shap": round(f.shap, 4), "direction": f.direction}
                for f in self.top_features
            ],
        }


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    n_rows: int
    missing_columns: Sequence[str] = field(default_factory=tuple)
    warnings: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class TierConfig:
    """Ngưỡng hai tầng — THAM SỐ, không phải hằng số trong logic.
    Mặc định khớp §3.11; đổi ngưỡng = đổi config, không đụng mã."""
    tier1: float = 0.10
    tier2: float = 0.40


# ─────────────── Hợp đồng NỘI BỘ (các chặng — API không gọi) ──────────────────
# "FeatureMatrix" / "RawRecords" cố ý để mờ (Any) ở tầng hợp đồng — kiểu cụ thể
# (DataFrame…) là chi tiết hiện thực, không thuộc hợp đồng.

FeatureMatrix = Any
RawRecords = Any


@runtime_checkable
class Validator(Protocol):
    def validate(self, raw: RawRecords) -> ValidationReport: ...


@runtime_checkable
class FeatureBuilder(Protocol):
    """Dựng đặc trưng theo đúng chân trời h (chỉ dùng học kỳ 1..h, giữ NaN).

    Hợp đồng KHÔNG quy định dùng thư viện nào. *Một* hiện thực có thể ủy quyền
    cho mã nghiên cứu; một hiện thực khác có thể dùng pipeline riêng — miễn là
    kết quả khớp lược đồ đặc trưng của Profile."""
    horizon: int
    def build(self, raw: RawRecords) -> FeatureMatrix: ...


@runtime_checkable
class RiskScorer(Protocol):
    """Điểm rủi ro THÔ (chưa hiệu chỉnh)."""
    def score(self, features: FeatureMatrix) -> Sequence[float]: ...


@runtime_checkable
class Calibrator(Protocol):
    """Điểm thô → xác suất đáng tin. PHẢI đơn điệu (không đổi thứ hạng rủi ro)."""
    def calibrate(self, scores: Sequence[float]) -> Sequence[float]: ...


@runtime_checkable
class TierPolicy(Protocol):
    config: TierConfig
    def assign(self, probability: float) -> int: ...


@runtime_checkable
class Explainer(Protocol):
    """Đóng góp đặc trưng cấp từng sinh viên. KHÔNG hàm ý nhân quả (§2.7.3)."""
    def explain(self, features: FeatureMatrix, top_k: int = 5
                ) -> Sequence[Sequence[FeatureContribution]]: ...


# ─────────────── Hợp đồng CÔNG KHAI (điểm vào DUY NHẤT của API) ────────────────
@runtime_checkable
class Predictor(Protocol):
    """Dịch vụ dự báo — API CHỈ gọi tệp này.

    Bên trong tự ghép: validate → build đặc trưng → score → calibrate → tier →
    explain, rồi trả PredictionResult. API **không biết và không cần biết** bên
    trong có mấy chặng; đổi số chặng không phá vỡ tầng API.

    Gắn với một Profile (chân trời + artifact) khi khởi tạo."""
    profile: PredictionProfile
    def predict(self, raw: RawRecords, top_k: int = 5) -> Sequence[PredictionResult]: ...


# ───────────────────────── TierPolicy chuẩn (thuần logic) ─────────────────────
# Đặt ở đây vì nó KHÔNG phụ thuộc mô hình — chỉ là quy tắc so ngưỡng.
class ThresholdTierPolicy:
    """Hiện thực TierPolicy duy nhất cần thiết: so xác suất với hai ngưỡng."""
    def __init__(self, config: TierConfig | None = None) -> None:
        self.config = config or TierConfig()

    def assign(self, probability: float) -> int:
        if probability >= self.config.tier2:
            return TIER_DEEP
        if probability >= self.config.tier1:
            return TIER_SCREEN
        return TIER_NONE
