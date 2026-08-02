"""Artifact Manifest — 'căn cước' của một artifact đã xuất.

Trả lời trong 5 giây câu hỏi lúc bảo vệ: "Mô hình này xuất từ revision nào,
dữ liệu nào, hợp đồng phiên bản mấy?" — không cần mở git.

Thuần stdlib (subprocess/hashlib/datetime/json). KHÔNG import ML lib → test được
mà không cần sklearn. `build_manifest` nhận tham số tường minh nên kiểm thử dễ.
"""
from __future__ import annotations

import subprocess
from typing import Any

# Phiên bản LƯỢC ĐỒ đặc trưng. Tăng khi tập/đặc trưng đổi → phát hiện feature drift
# (xem IT-11). Khác CONTRACT_VERSION (phiên bản hình dạng API).
FEATURE_SPEC_VERSION = "1"

REQUIRED_KEYS = (
    "contract_version", "feature_spec_version", "profile", "horizon",
    "n", "dropout_rate", "dataset_md5", "dataset_md5_matches_thesis",
    "research_commit", "export_time_utc", "random_state", "libraries", "prototype",
)


def current_git_commit(repo_dir: str) -> str | None:
    """SHA commit hiện tại, hoặc None nếu repo chưa có commit/không phải git."""
    try:
        out = subprocess.run(
            ["git", "-C", repo_dir, "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5)
        return out.stdout.strip() if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def build_manifest(*, contract_version: str, profile: str, horizon: int,
                   n: int, dropout_rate: float, dataset_md5: str,
                   dataset_md5_matches_thesis: bool, libraries: dict,
                   export_time_utc: str, research_commit: str | None,
                   random_state: int, prototype: bool = True) -> dict[str, Any]:
    """Dựng manifest dạng dict (chưa ghi đĩa). Mọi trường tường minh → dễ test."""
    return {
        "contract_version": contract_version,
        "feature_spec_version": FEATURE_SPEC_VERSION,
        "profile": profile,
        "horizon": horizon,
        "n": n,
        "dropout_rate": dropout_rate,
        "dataset_md5": dataset_md5,
        "dataset_md5_matches_thesis": dataset_md5_matches_thesis,
        "research_commit": research_commit,       # None cho tới khi repo có commit
        "export_time_utc": export_time_utc,
        "random_state": random_state,
        "libraries": libraries,
        "prototype": prototype,
    }


def validate_manifest(m: dict) -> list[str]:
    """Trả danh sách trường thiếu (rỗng = đầy đủ). Dùng trong test và lúc nạp."""
    return [k for k in REQUIRED_KEYS if k not in m]
