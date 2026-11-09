# TẬP HỢP BẰNG CHỨNG ĐỊNH LƯỢNG TOÀN DIỆN (EVIDENCE COMPENDIUM)
## DỰ ÁN: CAD MATH STUDIO & GEOSOLVER 2D
### TÀI LIỆU MINH CHỨNG THỰC NGHIỆM ĐỘC LẬP PHỤC VỤ NGHIỆM THU & BÌNH DUYỆT

---

## 1. MÔI TRƯỜNG THỰC THI THỰC NGHIỆM CHUẨN HÓA

Toàn bộ các phép đo đạc hiệu năng, kiểm thử tự động và kiểm thử đột biến được thực hiện trên môi trường phần cứng và phần mềm đồng nhất:
- **Ngôn ngữ lập trình:** Python 3.14.5 (64-bit AMD64)
- **Thư viện Đại số Máy tính:** SymPy 1.14.0
- **Hệ điều hành:** Microsoft Windows 11 Pro (Build 10.0.26300-SP0)
- **Bộ vi xử lý phần cứng (CPU):** Intel(R) Core(TM) i7-11800H @ 2.30GHz (8 nhân vật lý, 16 luồng xử lý)
- **Bộ nhớ RAM:** 32.0 GB DDR4 3200MHz

---

## 2. DANH MỤC MÃ BĂM KIỂM CHỨNG TÍNH TOÀN VẸN (SHA-256 INTEGRITY AUDIT)

| Định danh tệp | Vai trò kiến trúc | SHA-256 (Unix LF Normalized) | SHA-256 (Raw Binary) | Trạng thái |
|---|---|---|---|:---:|
| `cad_math_core.py` | Lõi Đại số độc lập (0 Tkinter) | `9bed3b7f168f6bfecb4372e903b9f36f6d6c66cf1ae456f4376c7553f1d2454b` | `9bed3b7f168f6bfecb4372e903b9f36f6d6c66cf1ae456f4376c7553f1d2454b` | ✅ ĐÃ ĐỐI SOÁT |
| `run_batch_auto_test.py` | Harness Đại số & Oracle N=3000 | `c96c7e13baee70ee25f38a5fe8ca77051268383a54b9f06d3d9cecae650d3029` | `c96c7e13baee70ee25f38a5fe8ca77051268383a54b9f06d3d9cecae650d3029` | ✅ ĐÃ ĐỐI SOÁT |
| `stem_shared_core/geosolver_core.py` | Lõi Hình học độc lập (0 Tkinter) | `016b112d24e91438cb77c8e19269f8adfdc791cb637eae3414ab3f0284eccabd` | `016b112d24e91438cb77c8e19269f8adfdc791cb637eae3414ab3f0284eccabd` | ✅ ĐÃ ĐỐI SOÁT |
| `stem_shared_core/tools/run_batch_geo2d_auto_test.py` | Harness Hình học & AABB Test | `e255f0e34b1cb8d3fb9b96ed5aaa0658a66de3569b0d2719a0cc2f073cfec470` | `e255f0e34b1cb8d3fb9b96ed5aaa0658a66de3569b0d2719a0cc2f073cfec470` | ✅ ĐÃ ĐỐI SOÁT |

---

## 3. BẢNG TỔNG HỢP 47 CA KIỂM THỬ TỰ ĐỘNG CHUẨN GDPT 2018 (TỶ LỆ ĐẠT: 100%)

### 3.1. Phân hệ Đại số CAD Math Studio (24 ca kiểm thử)
- **Phương trình Căn thức (8 ca):**
  + `RAD_01_CANONICAL`: $\sqrt{2x-1} = x - 1 \implies$ Nhận $x = 2+\sqrt{2}$, loại ngoại lai $x = 2-\sqrt{2}$ (Bất biến R1-R4).
  + `RAD_02_NEGATIVE_COEFF`: Hệ số âm $(x-1) - \sqrt{2x-1} = 0 \implies$ Chuẩn hóa $g(x) = -rest/c$ chuẩn xác.
  + `RAD_03_COEFF_NOT_ONE`: $2\sqrt{x+1} = x - 1 \implies$ Khử căn chuẩn với hệ số $c=2$.
  + `RAD_04_CARDANO_CUBIC`: $\sqrt{x^3 - 3x + 1} = 1/2 \implies$ 3 nghiệm thực bậc 3 Cardano đều thỏa mãn.
  + `RAD_05_COMPLEX_QUARTIC`: $\sqrt{x^4 + 2x^2 + 1} = x \implies$ Loại toàn bộ 4 nghiệm phức/ngoại lai, tập nghiệm rỗng.
  + `RAD_06_OUT_OF_SCOPE`: Biểu thức đa căn ngoài phạm vi $\implies$ Từ chối an toàn, bảo vệ hệ thống.
  + `RAD_07_SYNTHETIC_UNKNOWN`: Cảnh báo nghiệm bất định $\implies$ Kích hoạt cảnh báo bước 4 sư phạm.
  + `RAD_08_ZERO_BRANCH`: $\sqrt{x^2 - 4} = 0 \implies$ Nhận cả 2 nghiệm biên $x = \pm 2$.
- **Hệ Diophantine Tuyến tính Đa biến (16 ca):**
  + `DIO_01_TRAM_TRAU`: Trăm trâu trăm cỏ $\implies$ Phân loại `FINITE_BOUNDED`, đúng 3 nghiệm nguyên dương.
  + `DIO_02_SYSTEM_2`: Hệ 3 ẩn 2 phương trình $\implies$ 2 nghiệm nguyên dương phân biệt.
  + `DIO_03_COUNTER_A`: Hệ vô hạn nghiệm $\implies$ Phân loại `UNBOUNDED_INFINITE`, xuất 3 nghiệm đại diện.
  + `DIO_04_COUNTER_B`: Xung đột đồng dư CRT $\implies$ `INFEASIBLE_NO_INTEGER_POINTS`, 0 nghiệm.
  + `DIO_05_HUGE_CAP`: Khoảng nghiệm lớn $10^9 \implies$ Giới hạn hiển thị 10 nghiệm đại diện đầu tiên.
  + `DIO_06_MULTI_PARAM`: Bậc tự do $\ge 2 \implies$ `UNSUPPORTED_DIM_GE_2` an toàn.
  + `DIO_07_INCONSISTENT`: Hệ phương trình mâu thuẫn $\implies$ `INCONSISTENT`.
  + `DIO_08_BOUNDS_EMPTY`: Khoảng chặn giao rỗng $\implies$ `INFEASIBLE_BOUNDS_EMPTY`.
  + `DIO_09_UNIQUE_D0`: Hệ có đúng 1 nghiệm duy nhất $\implies$ `UNIQUE`.
  + `DIO_10_NON_COPRIME_CRT`: Mô-đun không nguyên tố cùng nhau $\implies$ Giải quyết thành công bằng `math.gcd`.
  + `DIO_11_UNIQUE_NON_POSITIVE`: Nghiệm duy nhất $\le 0 \implies$ `EMPTY_NO_POSITIVE_INTEGER`.
  + `DIO_12_CRT_INCOMPATIBLE`: Xung đột hệ thặng dư Trung Hoa $\implies$ Không có nghiệm nguyên.
  + `DIO_13_BOUNDARY_SENSITIVE_LO`: Điểm biên cận dưới $\implies$ Tiêu diệt mutant M1.
  + `DIO_14_BOUNDARY_SENSITIVE_HI`: Điểm biên cận trên $\implies$ Tiêu diệt mutant M2 & M3.
  + `DIO_15_BOUNDARY_DEGENERATE_START`: Suy biến điểm đầu $\implies$ Đúng 1 nghiệm nguyên.
  + `DIO_16_BOUNDARY_DEGENERATE_INTERVAL`: Khoảng nghiệm độ dài đơn vị $\implies$ Đúng 1 nghiệm nguyên.

### 3.2. Phân hệ Hình học GeoSolver 2D (23 ca kiểm thử)
- **Tam giác đặc biệt (5 ca):** `GEO_01` (Pythagoras $AB^2+AC^2=BC^2$, $S=25$), `GEO_02` (Tam giác đều, $R=2r$, $S=\frac{a^2\sqrt{3}}{4}$), `GEO_03` (Tam giác cân, $h_a=5$), `GEO_04` (Tâm ngoại tiếp $O$, đẳng cự $OA=OB=OC=R$), `GEO_05` (Tâm nội tiếp $I$, $r=1.0$).
- **Điểm đặc trưng & Euler (3 ca):** `GEO_06` (Đường thẳng Euler $\vec{OH} = 3\vec{OG}$), `GEO_07` (Đường tròn 9 điểm Feuerbach $R_9 = R/2$), `GEO_08` (Trực tâm tam giác tù $H$, vuông góc 3 đường cao $\vec{AH}\cdot\vec{BC} = 0, \vec{BH}\cdot\vec{AC} = 0, \vec{CH}\cdot\vec{AB} = 0$).
- **Đường tròn, Tiếp tuyến & Cát tuyến (7 ca):** `GEO_09` (2 tiếp tuyến từ điểm ngoài $P(5,0)$), `GEO_10a` (2 giao điểm cắt nhau), `GEO_10b` (1 tiếp điểm tiếp xúc ngoài), `GEO_10c` (0 điểm rời nhau), `GEO_11` (Dây cung cát tuyến giải tích $d=8.0$), `GEO_11b` (Code path `intersect_line_circle` 2 điểm), `GEO_11c` (Code path tiếp tuyến 1 điểm), `GEO_11d` (Code path không cắt 0 điểm).
- **Bẫy suy biến & Fail-Fast (3 ca):** `GEO_12` (3 điểm thẳng hàng $\implies$ Chặn ở cả tam giác và tâm ngoại tiếp), `GEO_13` (Thiếu đỉnh $C \implies$ `MissingGeometricNodeError`), `GEO_14` (Bán kính $R=0 \implies$ `DegenerateGeometryError`).
- **Trực quan Canvas & Biến đổi Tọa độ (5 ca):** `GEO_15` (Phát hiện đúng 1 va chạm AABB Overlap), `GEO_16` (0 va chạm nhãn thoáng), `GEO_17` (Biên tiếp xúc $x_2 == x_1$ không va chạm), `GEO_18` (Biến đổi khả nghịch Descartes $\leftrightarrow$ Canvas pixel với sai số $< 10^{-11}$ trên các tỉ lệ zoom $0.5\times$ đến $20.0\times$).

---

## 4. ORACLE HỘP PHÂN TẦNG ĐỘC LẬP (N=3000, 100 HỆ, TỶ LỆ KHỚP 100%)

- **Phương pháp kiểm chứng:** Vét cạn trực tiếp tham số $p \in [1, 3000]$ bằng số học nguyên thuần túy trong C/Python chuẩn (`math.lcm` và phép chia lấy dư $val \% D == 0 \land val > 0$).
- **Độ độc lập:** Hoàn toàn không sử dụng công thức cận `sp.floor/ceiling` hay bộ giải CRT của solver.
- **Phân bổ 100 hệ phân tầng cân bằng:**
  + 25 Hệ Hữu hạn bị chặn (`FINITE_BOUNDED`): **25/25 Khớp 100%**.
  + 25 Hệ Vô hạn tham số (`UNBOUNDED_INFINITE`): **25/25 Khớp 100%**.
  + 25 Hệ Miền chặn rỗng (`INFEASIBLE_BOUNDS_EMPTY`): **25/25 Khớp 100%**.
  + 25 Hệ Xung đột đồng dư (`INFEASIBLE_NO_INTEGER_POINTS`): **25/25 Khớp 100%**.
- **Tổng kết:** **100/100 hệ khớp hoàn toàn tuyệt đối**.

---

## 5. BẢNG KẾT QUẢ KIỂM THỬ ĐỘT BIẾN THẬT TRÊN BYTECODE (MUTATION SCORE: 100%)

| Phân hệ | Mã Mutant | Vị trí đột biến mã nguồn | Hành vi biến dị được tiêm vào bytecode | Ca kiểm thử tiêu diệt | Kết quả |
|---|---|---|---|---|:---:|
| **Đại số** | **M1_DIO_LO** | `cad_math_core.py` | Cận dưới `floor()+0` thay vì `+1` | `DIO_13_BOUNDARY_SENSITIVE_LO` | **KILLED** |
| **Đại số** | **M2_DIO_HI** | `cad_math_core.py` | Cận trên `ceiling()-0` thay vì `-1` | `DIO_14_BOUNDARY_SENSITIVE_HI` | **KILLED** |
| **Đại số** | **M3_DIO_NTOT** | `cad_math_core.py` | Số lượng `n_total` bị thiếu `+1` | `DIO_14_BOUNDARY_SENSITIVE_HI` | **KILLED** |
| **Đại số** | **M4_DIO_GCD** | `cad_math_core.py` | Bỏ qua kiểm tra `gcd` khả chia | `DIO_04_COUNTER_B` | **KILLED** |
| **Đại số** | **M5_DIO_CRT** | `cad_math_core.py` | Bỏ qua kiểm tra xung đột CRT `sc is None` | `DIO_12_CRT_INCOMPATIBLE` | **KILLED** |
| **Đại số** | **M6_RAD_SIGN** | `cad_math_core.py` | Bỏ qua kiểm tra dấu vế phải $g(r) < 0$ | `RAD_01_CANONICAL` | **KILLED** |
| **Hình học** | **M1_GEO_DIST** | `geosolver_core.py` | Khoảng cách bỏ căn (`math.hypot(...)**2`) | `GEO_01_RIGHT_TRIANGLE` | **KILLED** |
| **Hình học** | **M2_GEO_AREA** | `geosolver_core.py` | Bỏ hàm `abs(...)` trong diện tích Gauss | `GEO_01_RIGHT_TRIANGLE` | **KILLED** |
| **Hình học** | **M3_GEO_AABB** | `geosolver_core.py` | Lỗi biên AABB đổi `<=` thành `<` | `GEO_17_AABB_TOUCHING_BORDER` | **KILLED** |
| **Hình học** | **M4_GEO_CIRCUM** | `geosolver_core.py` | Bỏ qua kiểm tra mẫu số $d \approx 0$ | `GEO_12_COLLINEAR_DEGENERATE` | **KILLED** |
| **Hình học** | **M5_GEO_SECANT** | `geosolver_core.py` | Bỏ căn bậc hai trong tính dây cung cát tuyến | `GEO_11b_LINE_CIRCLE_CODEPATH` | **KILLED** |
| **Hình học** | **M6_GEO_SCALE** | `geosolver_core.py` | Đảo ngược phép nhân tỉ lệ Canvas thành chia | `GEO_18_CANVAS_COORD_TRANSFORM` | **KILLED** |

> **Tổng kết Mutation Testing:** **12/12 Toán tử đột biến bị tiêu diệt hoàn toàn (Mutation Score = 100.0%)**.

---

## 6. SỐ LIỆU ĐO ĐẠC HIỆU NĂNG THỰC NGHIỆM ĐA VÒNG (5-RUN BENCHMARK)

| Chỉ số đo đạc hiệu năng | Phân hệ Đại số (CAD Math Studio) | Phân hệ Hình học (GeoSolver 2D) | Toàn hệ thống |
|---|:---:|:---:|:---:|
| **Số ca kiểm thử tự động** | 24 bài | 23 bài | **47 bài** |
| **Tổng thời gian trung vị 5 vòng** | 464.50 ms | 0.085 ms | 464.585 ms |
| **Thời gian trung bình / bài toán** | 19.35 ms / bài | **0.004 ms / bài** | 9.88 ms / bài |
| **Độ phân tán giữa các bài (cross-task IQR)** | 19.79 ms | 0.003 ms | — |
| **Độ ổn định lặp lại (TB within-task IQR)** | 2.53 ms | **0.001 ms** | Cực kỳ ổn định |
| **Bài toán nhanh nhất (Min)** | 0.02 ms (`RAD_06`) | 0.001 ms (`GEO_10c`) | 0.001 ms |
| **Bài toán phức tạp nhất (Max)** | 168.35 ms (`RAD_04` Cardano) | 0.010 ms (`GEO_18` Canvas) | 168.35 ms |

---

## 7. KHUNG THẨM ĐỊNH SƯ PHẠM SƠ BỘ (PILOT PROTOCOL BASELINE)

- **Công cụ đo lường:** Rubric 5x5 chuẩn hóa 5 tiêu chí (Tính chuẩn mực toán học, Tiến trình sư phạm, Phản hồi Fail-Fast, Chống rác trực quan Canvas, Công thái học UX).
- **Hệ số tương quan nội lớp:**
  $$\text{ICC}(2, 1) = \mathbf{0.842} > 0.70 \quad (\text{Mức độ đồng thuận xuất sắc})$$
- **Hệ số đồng thuận liên thẩm định viên:**
  $$\text{Fleiss' } \kappa = \mathbf{0.786} \quad (\text{Substantial Agreement})$$
