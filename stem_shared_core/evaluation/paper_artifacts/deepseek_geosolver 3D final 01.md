# BIÊN BẢN PHÊ DUYỆT CHÍNH THỨC (FINAL APPROVAL RECORD)
## GEOSOLVER 3D CAD STUDIO & SPATIAL GEOMETRY KERNEL

**Mã tài liệu:** `STEM-GEO3D-VERIF-R5-FAR`  
**Dự án:** GeoSolver 3D — Hệ thống Dựng hình Động (DGS) & Suy Luận Hình Học Không Gian  
**Phiên bản thẩm định:** `v3.1.0.0` (Release Candidate)  
**Commit cơ sở:** `ce6e40e17124e4bbb57a495657fb60e7a32e52e2` (Phân hệ `geosolver_3d` sạch: `git_dirty: false`)  
**Tệp thực thi chính:** `dist\GeoSolver_3D\GeoSolver3D.exe` (32.520.808 bytes)  
**Mã băm SHA-256 (PE Binary):** `5418B83FE18413A2872E9B49622AEAEBECA42DF979C4D97FA0FE8B86D2DA0C4E`  
**Mã băm SHA-256 (Tệp Manifest 2.700 mục):** `7ED7FF1648343AF905C0732A373FBAA93F3F95C530E02A1B24986DAE64FEDA1E`  
**Ngày lập biên bản:** 09/11/2026  
**Trạng thái phê duyệt:** **ĐỦ ĐIỀU KIỆN PHÊ DUYỆT CHÍNH THỨC (APPROVED FOR RELEASE)**

---

## 1. TỔNG QUAN HỒ SƠ THẨM ĐỊNH

### 1.1. Mục đích
Biên bản này ghi nhận kết quả thẩm định cuối cùng cho phân hệ **GeoSolver 3D v3.1.0.0** sau chuỗi 6 phiên bản báo cáo (R0 → R5), tổng hợp toàn bộ phản biện độc lập đã tiếp thu, các cải tiến kỹ thuật đã thực hiện, và xác nhận đủ điều kiện phát hành chính thức.

### 1.2. Phạm vi thẩm định
1. **Lõi thuật toán:** 22 Test Vector đối chuẩn giải tích (TV-3D-01 → TV-3D-22).
2. **Mã nguồn:** Trích dẫn nguyên văn 100% (zero-truncation) các hàm cốt lõi.
3. **Đóng gói:** Smoke Test 7/7 PASS + 4/4 benchmark số học trong binary, SHA-256 toàn vẹn, cấu hình MSIX.
4. **Kiến trúc dung sai:** 7 hằng số phân tầng, bất biến thang đo `L ∈ [10⁻³, 10³]`.

### 1.3. Môi trường thực thi
- **Hệ điều hành:** Microsoft Windows 11 Pro 64-bit (Build 10.0.26300)
- **Python:** 3.14.5 (AMD64 MSC v.1944)
- **PyInstaller:** 6.22.3
- **SymPy:** 1.13+
- **NumPy:** 2.x, **Pillow:** 11.x

---

## 2. LỊCH SỬ TIẾN TRÌNH THẨM ĐỊNH R0 → R5

### 2.1. Bảng tổng hợp tiến trình

| Tiêu chí | R0 | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|---|
| Số test vector | 15 | 18 | 20 | 20 | 22 | **22** |
| Hàm góc | `acos` | `acos` | `acos` | `atan2` | `atan2` | **`atan2`** |
| Ngưỡng det mặt cầu | Tuyệt đối | Tuyệt đối | Tuyệt đối | Chuẩn hóa | Chuẩn hóa | **Chuẩn hóa** |
| Bán kính mặt cầu | `d(I,p0)` | `d(I,p0)` | `d(I,p0)` | `d(I,p0)` | TB 4 đỉnh | **TB 4 đỉnh** |
| Giải hệ mặt cầu | Gốc `O` | Gốc `O` | Gốc `O` | Gốc `O` | Gốc `O` | **Dịch gốc về `P0`** |
| `TOL_SPHERE` | — | — | Tuyệt đối | Tương đối | Tương đối | **Tương đối thuần nhất** |
| Test dương/âm biên | Không | Không | Không | Không | Chỉ dương | **Dương + âm** |
| Benchmark trong `.exe` | Không | Không | Không | Không | Không | **4 benchmark** |
| `git_dirty` | `true` | `true` | `true` | `false` | `false` | **`false`** |
| Số ngưỡng dung sai | 1 | 1 | 6 | 6 | 6 | **7** |
| Trích dẫn mã nguồn | Lược bỏ | 100% | 100% | 100% | 100% | **100%** |

### 2.2. Tóm tắt cải tiến qua từng phiên bản

**R0 → R1 (Tiếp thu 7 phản biện đợt 1):**
- Giải trình `git_dirty: true`;
- Trích đầy đủ `circumscribed_sphere` (thay Cramer bằng Gauss pivot);
- Chuẩn hóa vector đơn vị trong `find_common_perpendicular` (`denom = 1 − b²`);
- Công bố `EPSILON = 1e-9`;
- Công bố SHA-256 của chính manifest;
- Bổ sung 3 test vector (TV-3D-16/17/18).

**R1 → R2 (Tiếp thu phản biện đợt 2):**
- Chống triệt tiêu số học: `denom = |v1 × v2|²`;
- `strict=True` kiểm định đồng cầu trong `circumscribed_sphere`;
- Hệ thống dung sai phân tầng (6 ngưỡng);
- Bổ sung TV-3D-19 (nhánh chéo), TV-3D-20 (negative test);
- Phân định rõ 2 kịch bản MSIX (sideload vs Store).

**R2 → R3 (Tiếp thu phản biện đợt 3):**
- Loại bỏ hoàn toàn `acos`, chuyển sang `atan2` (3 hàm góc);
- Chuẩn hóa tích hỗn tạp không thứ nguyên (`TOL_DET` bất biến thang đo);
- `TOL_SPHERE` chuyển sang sai số tương đối (`max(R, 1.0)`);
- `git_dirty: false` (commit sạch);
- Strict validation trong `compute_polyhedron_volume`;
- TV-3D-03 nâng cấp lên nhiễu 1 ULP (`math.nextafter`).

**R3 → R4 (Tiếp thu phản biện đợt 4):**
- Docstring `find_common_perpendicular` khớp code;
- Bán kính mặt cầu lấy trung bình 4 đỉnh cơ sở;
- TV-3D-21 (micro-scale `L=10⁻³`) và TV-3D-22 (macro-scale `L=10³`);
- `norm_scale > 1e-24` công khai.

**R4 → R5 (Tiếp thu phản biện đợt 5 — bản cuối):**
- **Dịch gốc tọa độ cục bộ** trong `circumscribed_sphere` (chống triệt tiêu khi xa gốc `O`);
- **`TOL_SPHERE` tương đối thuần nhất** (`max(R, 1e-12)` thay vì `max(R, 1.0)`);
- **TV-3D-21/22 nâng cấp thành cặp dương/âm** (kiểm chứng `strict` mode ở cả 2 biên);
- **Nhúng metadata build + 4 benchmark số học trong `.exe`** (bằng chứng binary thực thi đúng);
- Chuẩn hóa pháp tuyến mặt trong `compute_polyhedron_volume` + hằng số `TOL_SCALE_MIN`;
- TV-3D-18 sửa input + ghi sai số lý thuyết `(Lθ)²/(2d)`.

---

## 3. KIẾN TRÚC DUNG SAI PHÂN TẦNG (7 NGƯỠNG)

| Hằng số | Giá trị | Mục đích | Bất biến thang đo |
|---|---|---|---|
| `EPSILON` | `1e-9` | Song song/cộng tuyến toàn cục | Tương đối (góc) |
| `TOL_PIVOT` | `1e-10` | Suy biến pivot khử Gauss | Tương đối (hệ số) |
| `TOL_DET` | `1e-8` | Tích hỗn tạp chuẩn hóa | **Có** (không thứ nguyên) |
| `TOL_GEOM` | `1e-7` | Mút đoạn thẳng trên mặt phẳng | Không (độ dài tuyệt đối) |
| `TOL_CCW` | `1e-6` | Vector tham chiếu CCW | Không (độ dài tuyệt đối) |
| `TOL_SPHERE` | `1e-4` | Đồng cầu strict mode | **Có** (tương đối thuần nhất) |
| `TOL_SCALE_MIN` | `1e-24` | Bảo vệ chia 0 (micro-scale) | Có (sàn tuyệt đối) |

---

## 4. MA TRẬN 22 TEST VECTORS ĐỐI CHUẨN

Toàn bộ 22 test vector đạt **22/22 PASS (100%)** trong phạm vi công bố `L ∈ [10⁻³, 10³]`:

| Mã TV | Hạng mục | Kết quả | Sai số | Trạng thái |
|---|---|---|---|---|
| TV-3D-01 | Bất biến Euler (7 khối) | `V−E+F=2` | 0 | PASS |
| TV-3D-02 | Suy biến 3 điểm thẳng hàng | `ValueError` | 0 | PASS |
| TV-3D-03 | Góc lệch 1 ULP | `0.0000°` | `<10⁻¹²` | PASS |
| TV-3D-04 | Góc 2 mặt phẳng | `90.0000°` | `<10⁻¹²` | PASS |
| TV-3D-05 | Góc đường-mặt phẳng | `90.0000°` | `<10⁻¹²` | PASS |
| TV-3D-06 | Khoảng cách 2 đường song song | `5.0000` | `<10⁻¹²` | PASS |
| TV-3D-07 | Chân vuông góc chung Oxyz | `M₁(0,0,0), M₂(0,0,3), d=3.0` | `<10⁻¹²` | PASS |
| TV-3D-08 | Thiết diện hình hộp | `S=12.0, P=14.0` | `<10⁻⁹` | PASS |
| TV-3D-09 | Vị tự thiết diện chóp | `S=4.0` | `<10⁻⁹` | PASS |
| TV-3D-10 | Mút đoạn trên mặt phẳng | 1 giao điểm | 0 | PASS |
| TV-3D-11 | Thể tích đa diện | `60/20/30.16996` | `<10⁻⁷` | PASS |
| TV-3D-12 | Mặt cầu ngoại tiếp chóp | `R=3.535534` | `<10⁻⁷` | PASS |
| TV-3D-13 | Girard tam giác cầu | `S=15707.9633` | `<10⁻⁶` | PASS |
| TV-3D-14 | Haversine | `d_anti=20015.0868 km` | `<10⁻⁹` | PASS |
| TV-3D-15 | Ràng buộc hình học động | `d(M',P)=4.0` | `<10⁻⁹` | PASS |
| TV-3D-16 | Chéo nhau vuông góc | `d=6.0` | `<10⁻¹²` | PASS |
| TV-3D-17 | Song song trong `find_common_perpendicular` | `d=4.0277` | `<10⁻¹²` | PASS |
| TV-3D-18 | Góc lệch dưới ngưỡng (offset `L=1000`) | `d=5.000010` | `<2×10⁻⁵` | PASS |
| TV-3D-19 | Góc lệch trên ngưỡng (nhánh chéo) | `d=5.0` | `<10⁻⁷` | PASS |
| TV-3D-20 | Ca âm mặt cầu (hình thang vuông) | `ValueError` | 0 | PASS |
| TV-3D-21 | Micro-scale `L=10⁻³` (dương+âm) | `R=8.66×10⁻⁴`, âm: `ValueError` | `<10⁻¹²` | PASS |
| TV-3D-22 | Macro-scale `L=10³` (dương+âm) | `R=866.0254`, âm: `ValueError` | `<10⁻¹²` | PASS |

---

## 5. KẾT QUẢ KIỂM ĐỊNH ĐÓNG GÓI

### 5.1. Smoke Test + 4 Benchmark số học trong binary
```json
{
  "timestamp": "2026-11-09T13:46:54.117695+00:00",
  "git_commit": "ce6e40e17124e4bbb57a495657fb60e7a32e52e2",
  "git_dirty": false,
  "frozen": true,
  "executable_sha256": "5418B83FE18413A2872E9B49622AEAEBECA42DF979C4D97FA0FE8B86D2DA0C4E",
  "checks": {
    "geometry3d_kernel": true,
    "deductive3d_engine": true,
    "sympy": true,
    "tkinter_runtime": true,
    "critical_modules": true,
    "assets": true,
    "ssl_certifi": true
  },
  "status": "PASS",
  "exit_code": 0,
  "numeric_benchmarks": {
    "TV-3D-07_skew_orthogonal_d": 3.0,
    "TV-3D-12_sphere_radius": 3.5355,
    "TV-3D-19_skew_above_threshold_d": 5.0,
    "TV-3D-21_micro_radius": 0.0008660254
  }
}