# NHẬT KÝ TÍCH HỢP TOÁN CAO CẤP ĐẠI HỌC VÀO HỆ SINH THÁI STEM APP
**Thời gian hoàn thành:** 08/11/2026  
**Vị trí dự án:** `D:\AI DATA\STEM_APP`  
**Các phân hệ tác động:**
- `stem_shared_core/higher_math_kernel.py` (Lõi tính toán & suy luận Toán Cao Cấp)
- `stem_shared_core/higher_math_benchmark.py` (Trình kiểm định tự động 20 bài toán chuẩn ĐH)
- `stem_shared_core/HIGHER_MATH_PEDAGOGICAL_BENCHMARK_REPORT.md` (Báo cáo thẩm định sư phạm)
- `stem_shared_core/higher_math_dialog.py` (Giao diện Win32 CAD Studio tối ưu không gian nhập liệu)
- `cad_math_v2/cad_math_v2.py` (Tích hợp menu Chuyên đề & nút One-Click trên Toolbar)

---

## 1. QUÁ TRÌNH TRIỂN KHAI CHI TIẾT (STEP-BY-STEP IMPLEMENTATION)

### Bước 1: Xây dựng Lõi Tính Toán Cao Cấp (`higher_math_kernel.py`)
Được thiết kế gồm 6 Engine độc lập nhưng dùng chung một chuẩn ngoại lệ `HigherMathKernelError`:
1. **`LinearAlgebraEngine`**:
   - Phân tích toàn diện ma trận: Kích thước, Định thức, Hạng ma trận, Nghịch đảo, Vết ma trận.
   - Giải hệ phương trình tuyến tính tổng quát $Ax = B$: Áp dụng định lý Kronecker-Capelli, đưa về RREF, phân loại vô nghiệm / nghiệm duy nhất / vô số nghiệm phụ thuộc tham số tự do.
   - Khảo sát trị riêng, đa thức đặc trưng, không gian vector riêng và chéo hóa ma trận vuông.
   - Phân tích dạng toàn phương $Q(x)$: Lập ma trận đối xứng, tính các định thức con chính góc (Principal Minors) và phân loại dấu theo tiêu chuẩn Sylvester.
2. **`AdvancedCalculusEngine`**:
   - Giới hạn vô định nâng cao ($\frac{0}{0}, \frac{\infty}{\infty}, 0 \cdot \infty, 1^\infty$) với xấp xỉ Taylor địa phương.
   - Khai triển Taylor / Maclaurin hàm số với phần dư Peano cấp $n$.
   - Tích phân suy rộng loại 1 (cận $\pm\infty$) và loại 2 (hàm gián đoạn): Khảo sát sự hội tụ và tính giá trị chính xác.
3. **`SeriesEngine`**:
   - Kiểm tra điều kiện cần của chuỗi số ($\lim a_n \neq 0$).
   - Tiêu chuẩn tỷ số D'Alembert (Ratio test) và tiêu chuẩn căn số Cauchy (Root test).
   - Bán kính hội tụ $R$ và khoảng hội tụ của chuỗi lũy thừa $\sum a_n (x - x_0)^n$.
   - Khai triển chuỗi Fourier hàm tuần hoàn chu kỳ $2L$ trên $[-L, L]$ (tính hệ số $a_0, a_n, b_n$ và đa thức Fourier tổng riêng).
4. **`MultivariableEngine`**:
   - Đạo hàm riêng cấp 1, cấp cao; Vi phân toàn phần cấp 1 $df$; Gradient $\nabla f$ và Ma trận Hessian $H(f)$.
   - Tìm cực trị tự do hàm 2 biến $z = f(x, y)$: Giải hệ điểm dừng, tính $\Delta = AC - B^2$, phân loại cực tiểu, cực đại hoặc điểm yên ngựa (saddle point).
   - Cực trị có điều kiện bằng phương pháp nhân tử Lagrange: Thiết lập hàm Lagrange $L = f - \lambda g$, hệ điều kiện cần và giải ra các điểm dừng kèm giá trị cực trị.
   - Tích phân kép lặp $\iint_D f(x, y) \, dy dx$.
5. **`FieldTheoryEngine`**:
   - Toán tử vi phân trường vector: Divergence ($\text{div}\,\vec{F}$), Curl / Rotor ($\text{rot}\,\vec{F}$).
   - Kiểm tra trường thế: Khi $\text{rot}\,\vec{F} = \vec{0}$, tự động tích phân tìm hàm thế vị $U(x, y, z)$ sao cho $\nabla U = \vec{F}$.
6. **`DifferentialEquationsEngine`**:
   - Phương trình vi phân cấp 1 & cấp 2 hệ số hằng: Giải nghiệm tổng quát và bài toán Cauchy có điều kiện đầu $y(0) = y_0, y'(0) = y'_0$.
   - Biến đổi Laplace thuận $\mathcal{L}\{f(t)\} = F(s)$ và Laplace ngược $\mathcal{L}^{-1}\{F(s)\} = f(t)$.

---

### Bước 2: Thiết kế Giao diện Win32 CAD Studio Tối ưu Nhập liệu (`higher_math_dialog.py`)
- **Nguyên tắc thiết kế:** Tuân thủ 100% phong cách Win32 CAD cổ điển (#ECE9D8), không rườm rà, tập trung tối đa vào tốc độ và công thái học (ergonomics).
- **Tối ưu hóa không gian nhập liệu:**
  - Chia giao diện làm 2 nửa rõ ràng: Bên trái (430px) là khu vực nhập liệu & công cụ; Bên phải (fill) là khu vực kết quả hiển thị hai tầng (Bước sư phạm + Natural Math + LaTeX).
  - Tích hợp **Quick Math Symbol Palette** (thanh ký hiệu toán học nhanh 1 chạm): $\partial, \int, \iint, \iiint, \nabla, \lambda, \infty, \pi, \pm, \sqrt{}, x^2, y^2, e^x, y', y''$.
  - Tích hợp **Ví dụ mẫu chuẩn Đại học**: Bấm 1 nút nạp ngay bài toán mẫu chuẩn của các kỳ thi đại học (Ma trận 3x3, Hệ phương trình 3 ẩn, Cực trị Lagrange, Chuỗi D'Alembert...).
  - Trang bị phím tắt và các nút hành động một chạm: Sao chép Lời giải, Sao chép LaTeX, Xuất file Báo cáo (.txt / .md).

---

### Bước 3: Tích hợp Cấu trúc Phân cấp vào `cad_math_v2.py`
- Bổ sung Menu chính **`Chuyên đề (Curricula)`** ngay cạnh menu Xem (View):
  - Nhánh 1: *Toán Cao Cấp Đại Học (Higher Mathematics)* với 6 chuyên đề con và nút mở trọn bộ Studio hoặc Chạy kiểm định.
  - Nhánh 2: *Toán Phổ Thông THPT GDPT 2018 (Lớp 10, 11, 12)*.
- Bổ sung nút bấm trực quan nổi bật trên Toolbar: **`[ 🏛️ Toán Cao Cấp ]`** (Màu xanh dương đậm #0284c7) giúp sinh viên và giảng viên truy cập chỉ với 1 cú click.

---

## 2. NHẬT KÝ LỖI PHÁT SINH & GIẢI PHÁP KHẮC PHỤC (BUGS & FIXES)

Trong quá trình thực thi, một số lỗi thực tế đã được phát hiện và xử lý triệt để:

| STT | Lỗi phát sinh | Nguyên nhân | Cách khắc phục triệt để |
|:---:|:---|:---|:---|
| **1** | `UnicodeEncodeError: 'charmap' codec can't encode character '\u1ed8'` khi chạy benchmark trên Windows Console. | Mặc định Windows PowerShell/CMD sử dụng bảng mã `cp1252` thay vì UTF-8, làm gãy các ký tự tiếng Việt có dấu. | Thêm `sys.stdout.reconfigure(encoding='utf-8')` và `sys.stderr.reconfigure(encoding='utf-8')` ngay đầu script benchmark. |
| **2** | Nguy cơ sai lệch ký hiệu đạo hàm cấp 2 $y''$ khi phân tích chuỗi phương trình vi phân. | Người dùng gõ tự nhiên dạng `y'' - 5y' + 6y = 0`, nếu dùng SymPy `parse_expr` thông thường sẽ bị hiểu nhầm thành chuỗi ký tự hoặc lũy thừa. | Xây dựng bộ tiền xử lý Regex trong `DifferentialEquationsEngine`: Tự động nhận diện `y''` thành `Derivative(y(x), x, 2)` và `y'` thành `Derivative(y(x), x)` trước khi chuyển vào `sp.dsolve`. |
| **3** | Hàm Heaviside xuất hiện trong kết quả Biến đổi Laplace ngược. | SymPy mặc định trả về `Heaviside(t)` để đảm bảo miền $t > 0$. Khi hiển thị lời giải cho sinh viên, hàm Heaviside làm công thức trở nên rối rắm. | Sử dụng phép thế `.replace(sp.Heaviside, lambda arg: 1)` để hiển thị dạng nghiệm giải tích gọn gàng cho sinh viên: $1 - e^{-t}$. |
| **4** | Lỗi định dạng ma trận dạng văn bản không thẳng hàng khi số âm hoặc số có nhiều chữ số. | Chuỗi ma trận in thông thường bị lệch cột. | Viết hàm `format_matrix_plain(mat)` tự động tính độ rộng lớn nhất của từng cột và căn phải (`rjust`) kèm khung viền CAD `│  ...  │`. |

---

## 3. KẾT QUẢ KIỂM ĐỊNH BỘ ĐỀ CHUẨN ĐẠI HỌC (BENCHMARK 100% PASS)

Trình kiểm định tự động `higher_math_benchmark.py` đã thực thi **20 bài toán kinh điển** chọn lọc từ giáo trình ĐH Bách Khoa Hà Nội, ĐHQG TP.HCM, ĐH Sư Phạm và kỳ thi GRE Mathematics:
- **Đại số tuyến tính:** 5/5 bài PASS (Định thức, Hạng, Nghịch đảo, Hệ Kronecker-Capelli, Trị riêng chéo hóa, Sylvester).
- **Giải tích 1:** 3/3 bài PASS (Giới hạn 0/0 L'Hopital, Maclaurin cos(x), Tích phân suy rộng loại 1).
- **Chuỗi số & Fourier:** 3/3 bài PASS (Tiêu chuẩn D'Alembert, Bán kính hội tụ $R=3$, Chuỗi Fourier hàm lẻ).
- **Giải tích đa biến:** 4/4 bài PASS (Hessian, Cực trị tự do (0,0) & (1,1), Nhân tử Lagrange $f_{max}=5, f_{min}=-5$, Tích phân kép lặp $I=1/8$).
- **Lý thuyết trường:** 1/1 bài PASS (Trường thế $\text{rot}\,\vec{F} = \vec{0}$, Hàm thế vị $U = x^2 y + x z$).
- **Phương trình vi phân & Laplace:** 4/4 bài PASS (Cauchy cấp 1, Cauchy cấp 2 $y = e^{2x} + e^{3x}$, Laplace thuận $2/((s-3)^2+4)$, Laplace ngược $1 - e^{-t}$).

**Tổng kết:** **20/20 bài kiểm định đạt chuẩn tuyệt đối (100.0%) trong thời gian 1.27 giây!**  
Báo cáo đối chiếu chi tiết đã sẵn sàng tại: `stem_shared_core/HIGHER_MATH_PEDAGOGICAL_BENCHMARK_REPORT.md`.
