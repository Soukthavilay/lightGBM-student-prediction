# Danh mục tái lập (Reproducibility Checklist)

> Ghi **giá trị thực** đo được từ máy chạy dự án (2026-07-14). Mục chưa có → `TODO`, không bịa. Đây là bằng chứng cho *computational reproducibility* khi hội đồng hỏi "chạy lại có ra như bạn không?".

## Môi trường phần mềm (đo thực)
| Thành phần | Giá trị | Ghi chú |
|---|---|---|
| Python | **3.9.6** | |
| lightgbm | **4.5.0** | mô hình chính |
| scikit-learn | **1.6.1** | CV, calibration, metrics |
| shap | **0.49.1** | giải thích |
| optuna | **4.8.0** | tinh chỉnh nested |
| numpy | **1.26.4** | |
| pandas | **2.3.0+4.g1dfc98e16a** | ⚠️ **bản dev (không phải release chính thức)** — nên ghim về bản release (vd 2.3.0) để tái lập chắc chắn |
| scipy | **1.13.1** | DeLong, Wilcoxon, t-test |
| joblib | **1.5.1** | |
| matplotlib | **3.9.4** | vẽ hình |

## Phần cứng & hệ điều hành (đo thực)
| Thành phần | Giá trị |
|---|---|
| OS | macOS 26.5.2 (Darwin 25.5.0) |
| Kiến trúc | **arm64 (Apple Silicon)** |
| Thiết bị tính | **CPU** — LightGBM chạy CPU, **không dùng CUDA/GPU** |

## Tính xác định (determinism)
| Mục | Giá trị |
|---|---|
| Seed toàn cục | `RANDOM_STATE = 42` (xuyên suốt `dropout_research.py`) |
| Seed CV lặp | `seed + r` (repeated OOF), `seed + k` (nested outer/inner) |
| Seed Optuna | `TPESampler(seed=42+k)` |
| Seed bootstrap | `np.random.default_rng(42)` |

## Dữ liệu (đo thực)
| Mục | Giá trị |
|---|---|
| Tệp | `Testkhoa.csv` |
| **MD5** | `09e5873d10cd15572e162c9fd705f34f` |
| Số dòng | 7.524 (1 header + 7.523 bản ghi) |
| Encoding | **latin-1** (đọc UTF-8 sẽ hỏng tiếng Việt) |
| Cohort dùng | `COHORT_YEARS = (2020, 2021)` (loại 9 SV khóa 2022–2023 khi nạp) |

## Mã nguồn & phiên bản
| Mục | Trạng thái |
|---|---|
| Repo Git | ⚠️ **CHƯA CÓ COMMIT NÀO** (`main` rỗng) → `TODO`: commit + gắn tag phiên bản dùng cho luận văn |
| Git commit hash của kết quả | `TODO` (phụ thuộc việc commit ở trên) |
| `requirements.txt` / khóa môi trường | ⚠️ **CHƯA CÓ** → `TODO`: xuất `pip freeze > requirements.txt` |
| Lệnh tái lập | `python3 run_pipeline.py` (full ~1–2h) → mở notebook → Restart & Run All |

---

## Việc phải làm (TODO ưu tiên)
1. **Commit toàn bộ + gắn tag** (vd `v1.0-thesis`) và ghi commit hash vào phụ lục — hiện repo rỗng là lỗ hổng tái lập lớn nhất.
2. **Ghim pandas** về bản release chính thức (bản dev không đảm bảo tái lập lâu dài).
3. **Xuất `requirements.txt`** (`pip freeze`) và đính kèm.
4. Ghi vào luận văn câu xác nhận: cùng seed + cùng phiên bản → kết quả tái lập bit-for-bit trên CPU (LightGBM CPU xác định với `n_jobs` cố định — kiểm lại `n_jobs=1` ở nested để chắc chắn xác định).
