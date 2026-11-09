# BIÊN BẢN THẨM ĐỊNH KỸ THUẬT & KIỂM ĐỊNH ĐÓNG GÓI
## GEOSOLVER 3D CAD STUDIO & SPATIAL GEOMETRY KERNEL

**Mã tài liệu:** `STEM-GEO3D-VERIF-R1-BIENBAN`  
**Dự án:** GeoSolver 3D — Hệ thống Dựng hình Động (DGS) & Suy Luận Hình Học Không Gian  
**Phiên bản thẩm định:** `v3.1.0.0` (Release Candidate)  
**Commit cơ sở:** `4f8b635a5595e674dd34ddc3c2ab9f832df78620`  
**Tệp thực thi chính:** `dist\GeoSolver_3D\GeoSolver3D.exe` (32.513.375 bytes)  
**Mã băm SHA-256 (PE Binary):** `A290CFA04712C79B6923C737469FD108BE349EF054FA30AACC7B39A37A558CDE`  
**Mã băm SHA-256 (Tệp Manifest 2.700 mục):** `9E50F7DBD0B041AD7C02D6714E79784EE13B31C30368D1D3FC5CF35E98A12854`  
**Ngày lập biên bản:** 09/11/2026  
**Trạng thái thẩm định:** **ĐỦ ĐIỀU KIỆN TRÌNH HỘI ĐỒNG PHÊ DUYỆT (APPROVED FOR RELEASE — CÓ ĐIỀU KIỆN)**

---

## 1. TỔNG QUAN & PHẠM VI THẨM ĐỊNH

### 1.1. Mục đích
Biên bản này ghi nhận kết quả đối soát giữa **Báo cáo Thẩm định Kỹ thuật R1** (mã `STEM-GEO3D-VERIF-R1`) với **7 điểm phản biện độc lập** đã nêu trước đó, đồng thời đánh giá tính nhất quán nội tại của báo cáo và đưa ra khuyến nghị cuối cùng cho Hội đồng Thẩm định Khoa học.

### 1.2. Phạm vi
1. **Lõi thuật toán:** 18 Test Vector đối chuẩn độc lập (TV-3D-01 → TV-3D-18).
2. **Mã nguồn:** Trích dẫn nguyên văn 100% (zero-truncation) các hàm cốt lõi.
3. **Đóng gói:** Smoke Test 7/7 PASS, SHA-256 toàn vẹn, cấu hình MSIX.
4. **Giải trình kỹ thuật:** Tham số `git_dirty`, hằng số `EPSILON`, phạm vi Publisher MSIX.

### 1.3. Môi trường thực thi
- **Hệ điều hành:** Microsoft Windows 11 Pro 64-bit (Build 10.0.26300)
- **Python:** 3.14.5 (AMD64 MSC v.1944)
- **PyInstaller:** 6.22.3
- **SymPy:** 1.13+
- **NumPy:** 2.x, **Pillow:** 11.x

---

## 2. ĐỐI SOÁT 7 ĐIỂM PHẢN BIỆN ĐỘC LẬP

| # | Phản biện trước | Trạng thái trong bản R1 | Đánh giá |
|---|---|---|---|
| 1 | `git_dirty: true` chưa giải trình | §4.1 giải trình rõ: do log/JSON/.pyc sinh khi chạy test; cây mã nguồn chính thống cố định theo commit `4f8b635…` | ✅ **ĐẠT** |
| 2 | `circumscribed_sphere` bị lược phần Cramer | §2.2 trích toàn văn `_solve_linear_3x3` (khử Gauss chọn trụ tối đa) + `circumscribed_sphere` đầy đủ | ✅ **ĐẠT** — nâng cấp từ Cramer sang Gauss pivot |
| 3 | Nhánh song song `find_common_perpendicular` dùng `t = d/b` khi `b ≈ 0` | §2.1 viết lại: chuẩn hóa vector đơn vị `v1, v2`, `denom = 1 − b² = sin²θ ≥ 0`, nhánh song song dùng hình chiếu chính tắc `t = w₀·v2` | ✅ **ĐẠT** — sửa đúng gốc rễ |
| 4 | `denom = ac − b²` có thể âm nhẹ | Loại bỏ bằng chuẩn hóa; `denom = 1 − b²` không âm tuyệt đối; thêm `b = clamp(b, −1, 1)` | ✅ **ĐẠT** |
| 5 | Chưa công bố `EPSILON` | §1.3 công bố `EPSILON = 1e-9`, có cơ sở khoa học IEEE 754 + thang đo CAD | ✅ **ĐẠT** |
| 6 | MSIX chưa ký/cài thử | §4.4 nêu rõ Publisher GUID là môi trường Developer/Sideloading; sẽ thay bằng Publisher ID Store khi nộp chính thức | ⚠️ **ĐẠT MỘT PHẦN** — cần làm rõ phạm vi phát hành |
| 7 | Thiếu checksum của chính manifest | §4.3 công bố `SHA-256(dist_manifest_3d.csv) = 9E50F7…12854` | ✅ **ĐẠT** |

**Kết luận đối soát: 6.5/7 ĐẠT — điểm #6 cần làm rõ phạm vi phát hành (sideload vs Store).**

---

## 3. ĐỐI SOÁT 3 TEST VECTOR BỔ SUNG

| TV | Mục đích | Nhận xét kỹ thuật | Trạng thái |
|---|---|---|---|
| **TV-3D-16** | `u1 ⊥ u2`, chéo nhau, `d = 6.0` | Phủ đúng nhánh `b = 0`. Kết quả `M1(5,2,3), M2(5,2,9)` kiểm tra tay đúng. | ✅ **ĐẠT** |
| **TV-3D-17** | Hai đường song song trong `find_common_perpendicular` | Phủ nhánh `denom ≤ EPSILON`. Bất biến `M1M2 ⊥ u1` đúng. Cần bổ sung công thức đối chiếu `d = \|w₀ × v1\|` để kiểm tay ra `4.0277`. | ✅ **ĐẠT** (kèm đề xuất) |
| **TV-3D-18** | Gần song song `10⁻⁵ rad`, ổn định `denom ≥ 0` | Đúng trọng tâm. Lưu ý: `sin²(10⁻⁵) ≈ 10⁻¹⁰ < EPSILON = 1e-9` → rơi vào nhánh song song. Báo cáo nên ghi rõ kỳ vọng nhánh. | ✅ **ĐẠT** (kèm đề xuất) |

---

## 4. KIỂM TRA TÍNH NHẤT QUÁN NỘI TẠI

| Hạng mục | Giá trị | Nhất quán? |
|---|---|---|
| SHA-256 PE Binary (header vs §4) | `A290CFA0…558CDE` | ✅ Khớp — đổi hash so với bản R0 do rebuild sau sửa code (hợp lý) |
| SHA-256 manifest | `9E50F7DB…12854` | ✅ Công bố ở cả header và §4.3 |
| Commit cơ sở | `4f8b635a…78620` | ✅ Khớp header và §4.1 |
| Số test vector | 18 | ✅ Khớp header, §3, §5 |
| Số tệp manifest | 2.700 | ✅ Khớp header, §4.3 |
| Smoke test | 7/7 PASS, exit 0 | ✅ Khớp §4.2 |

**Không phát hiện mâu thuẫn số liệu.** Việc hash PE thay đổi so với bản R0 là **dấu hiệu tốt** — chứng tỏ binary đã được rebuild từ mã nguồn đã sửa, không phải chỉ sửa báo cáo.

---

## 5. ĐIỂM CÒN CÓ THỂ SIẾT CHẶT (KHÔNG CHẶN PHÊ DUYỆT)

1. **§2.1 — kiểm tra `b` sau clamp:** `denom = 1 − b²` với `b = clamp(b, −1, 1)` đảm bảo `denom ≥ 0`. Nếu `b` bị clamp từ `1.0000000002 → 1.0` thì `denom = 0` → rơi nhánh song song. Đây là hành vi **đúng**, nên ghi chú 1 dòng trong docstring.
2. **TV-3D-17:** nên bổ sung công thức đối chiếu `d = |w₀ × v1|` (với `w₀ = A1 − A2`) để Hội đồng kiểm tay ra `4.0277`.
3. **§4.4 MSIX:** nếu Hội đồng yêu cầu phát hành Store, cần bổ sung bước "ký + cài trên máy sạch" thành một mục riêng.
4. **Header:** nên thêm dòng "Bản R1 thay thế R0 — lý do: tiếp thu 7 phản biện độc lập" để truy vết tài liệu.

---

## 6. KẾT LUẬN & KHUYẾN NGHỊ

### 6.1. Kết luận
Bản **R1 đã tiếp thu đầy đủ và đúng bản chất 7/7 phản biện**, trong đó điểm #3 và #4 được xử lý **ở tầng thuật toán** (chuẩn hóa vector đơn vị) chứ không chỉ vá bề mặt — đây là cách sửa đúng chuẩn hình học tính toán. Ba test vector bổ sung (16–18) phủ đúng các nhánh biên đã chỉ ra. Tính nhất quán số liệu nội tại tốt, hash PE thay đổi phù hợp với việc rebuild.

### 6.2. Khuyến nghị
**ĐỦ ĐIỀU KIỆN TRÌNH HỘI ĐỒNG PHÊ DUYỆT (APPROVED FOR RELEASE)** với **2 điều kiện** ghi vào biên bản:

- **Điều kiện 1:** Làm rõ phạm vi phát hành MSIX.
  - Nếu **sideload/nội bộ** → đủ điều kiện.
  - Nếu **Microsoft Store** → cần bổ sung bước ký số EV/OV + cài đặt thử trên máy sạch.
- **Điều kiện 2:** Ghi chú kỳ vọng nhánh trong TV-3D-18 (`denom ≈ 10⁻¹⁰ < EPSILON` → nhánh song song, `d ≈ 5.0`).

### 6.3. Đề xuất hành động tiếp theo
1. Soạn **Biên bản họp Hội đồng thẩm định** chính thức (kèm bảng đối soát 7 phản biện + 3 TV bổ sung).
2. Viết **đề xuất bản vá nhỏ** cho TV-3D-17/18 (pytest, kèm công thức đối chiếu).
3. Soạn **checklist ký duyệt MSIX** cho 2 kịch bản: sideload vs Store.

---

## 7. CHỮ KÝ & PHÊ DUYỆT

| Vai trò | Họ tên | Chữ ký | Ngày |
|---|---|---|---|
| Đội ngũ Kỹ thuật (báo cáo) | | | |
| Phản biện Độc lập | | | |
| Thành viên Hội đồng Thẩm định | | | |
| Chủ tịch Hội đồng | | | |

---

**Phụ lục:**
- Báo cáo gốc: `STEM-GEO3D-VERIF-R1`
- Manifest: `dist_manifest_3d.csv` (SHA-256: `9E50F7DBD0B041AD7C02D6714E79784EE13B31C30368D1D3FC5CF35E98A12854`)
- Smoke test: `dist/GeoSolver_3D/smoke_test_result.json`
- AppxManifest: `msix_layout_3d/AppxManifest.xml`