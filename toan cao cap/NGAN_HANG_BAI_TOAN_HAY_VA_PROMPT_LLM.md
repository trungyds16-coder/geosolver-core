# NGÂN HÀNG BÀI TOÁN CAO CẤP CHỌN LỌC & KHUNG LỆNH HƯỚNG DẪN GIẢI CHO MÔ HÌNH NGÔN NGỮ
**Mục đích:** Cung cấp tài liệu bài toán chọn lọc từ kho lưu trữ `D:\AI DATA\toan cao cap` kèm khung hướng dẫn giải (System Prompt) có cấu trúc.  
**Cách dùng:** Sao chép nội dung bài toán và khung prompt dán vào giao diện tương tác của mô hình ngôn ngữ để tạo lời giải chi tiết và đoạn mã xác thực SymPy.

---

## 1. KHUNG LỆNH HỆ THỐNG (SYSTEM PROMPT)
*(Hãy sao chép đoạn khung này đặt ở đầu mỗi câu hỏi khi bạn chat với AI)*

```text
[VAI TRÒ & NHIỆM VỤ]
Bạn là một giảng viên chuyên ngành Toán cao cấp.
Nhiệm vụ của bạn là giải chi tiết, rõ ràng và chuẩn xác bài toán dưới đây cho sinh viên các ngành kỹ thuật và khoa học tự nhiên.

[QUY CHUẨN TRÌNH BÀY BẮT BUỘC]
1. BƯỚC 1: PHÂN TÍCH BẢN CHẤT & ĐỊNH HƯỚNG GIẢI:
   - Nêu rõ dạng toán, các định lý/công thức nền tảng áp dụng (ví dụ: Định lý Lagrange, Kronecker-Capelli, Tiêu chuẩn Sylvester, Định lý Green, Gauss-Ostrogradsky, Biến đổi Laplace...).
2. BƯỚC 2: CÁC BƯỚC BIẾN ĐỔI TOÁN HỌC CHI TIẾT:
   - Trình bày từng bước biến đổi đại số/giải tích tường minh, không được nhảy cóc bước tính.
   - Toàn bộ công thức toán học phải định dạng bằng LaTeX chuẩn mực ($...$ cho công thức nội dòng, $$...$$ cho khối công thức riêng).
3. BƯỚC 3: PHÂN TÍCH CÁC BẪY SAI LẦM THƯỜNG GẶP (PEDAGOGICAL PITFALLS):
   - Chỉ ra các bẫy mà sinh viên dễ mắc phải (ví dụ: quên xét ma trận suy biến det=0, vi phạm điều kiện hội tụ tích phân suy rộng, nhầm lẫn hướng pháp tuyến mặt cong, nghiệm ngoại lai...).
4. BƯỚC 4: KẾT LUẬN & ĐOẠN MÃ XÁC MINH SYMPY (PYTHON VERIFICATION):
   - Kết luận đáp số chính xác.
   - Cung cấp một đoạn mã Python ngắn gọn (3-5 dòng sử dụng thư viện SymPy) để sinh viên có thể tự chạy kiểm chứng lại kết quả trên máy tính.
```

---

## 2. CHUYÊN ĐỀ 1: ĐẠI SỐ TUYẾN TÍNH & MA TRẬN (OLYMPIC & ĐẠI HỌC)
*(Trích xuất từ tài liệu bài tập đại số và giải tích nâng cao)*

### Bài 1.1: Tính lũy thừa ma trận và Chéo hóa ma trận
**Đề bài:**
Cho ma trận vuông cấp 3:
$$A = \begin{pmatrix} 1 & 2 & 0 \\ 0 & 2 & 0 \\ -2 & -2 & -1 \end{pmatrix}$$
1. Tìm tất cả các giá trị riêng và cơ sở không gian vector riêng tương ứng của $A$.
2. Kiểm tra xem ma trận $A$ có chéo hóa được không? Nếu có, hãy tìm ma trận khả nghịch $P$ và ma trận đường chéo $D$ sao cho $P^{-1} A P = D$.
3. Từ đó, hãy tính lũy thừa $A^n$ với $n$ là số nguyên dương tùy ý.

---

### Bài 1.2: Ma trận nghịch đảo của đa thức ma trận (Olympic Đại Số)
**Đề bài:**
Cho ma trận vuông $A$ cấp $n$ thỏa mãn phương trình đa thức:
$$A^3 - 3A^2 + 2A - 5I = 0$$
(trong đó $I$ là ma trận đơn vị cấp $n$).
1. Chứng minh rằng ma trận $A$ là ma trận khả nghịch (khác suy biến).
2. Biểu diễn ma trận nghịch đảo $A^{-1}$ dưới dạng một đa thức theo $A$.
3. Tính định thức $\det(A)$ nếu biết kích thước $n = 3$ và ma trận $A$ có một giá trị riêng thực $\lambda_1 = 5$.

---

### Bài 1.3: Biện luận hạng của ma trận theo tham số $m$
**Đề bài:**
Cho ma trận $A$ phụ thuộc tham số $m$:
$$A = \begin{pmatrix} 1 & -1 & 2 & 3 \\ 2 & 1 & 1 & m \\ 3 & 0 & 3 & 5 \\ -1 & 2 & -1 & 1 \end{pmatrix}$$
1. Tính định thức $\det(A)$ theo tham số $m$.
2. Tìm tất cả các giá trị của $m$ để ma trận $A$ khả nghịch.
3. Tìm hạng $\text{rank}(A)$ tùy theo các giá trị của tham số thực $m$.

---

### Bài 1.4: Dạng toàn phương và Tiêu chuẩn Sylvester
**Đề bài:**
Trong không gian $\mathbb{R}^3$, cho dạng toàn phương:
$$Q(x_1, x_2, x_3) = x_1^2 + 5x_2^2 + 2x_3^2 + 4x_1 x_2 - 2x_1 x_3 - 4x_2 x_3$$
1. Viết ma trận đối xứng $A$ liên kết với dạng toàn phương $Q$.
2. Áp dụng phương pháp phân tích Lagrange (tạo các bình phương độc lập) để đưa $Q$ về dạng chính tắc.
3. Áp dụng tiêu chuẩn định thức con chính Sylvester để phân loại dấu của $Q$ (xác định dương, xác định âm, nửa xác định hay không xác định).

---

## 3. CHUYÊN ĐỀ 2: GIẢI TÍCH ĐƠN BIẾN NÂNG CAO, GIỚI HẠN & TÍCH PHÂN SUY RỘNG
*(Trích xuất từ `Exercise_Calculus1_2022.pdf` và `TCC2-Download_com_vn.pdf`)*

### Bài 2.1: Giới hạn dãy số đệ quy vô hạn căn thức
**Đề bài:**
Cho dãy số thực $(u_n)$ được xác định bởi công thức đệ quy:
$$u_1 = \sqrt{2}, \quad u_{n+1} = \sqrt{2 + u_n} \quad (\forall n \ge 1)$$
1. Chứng minh bằng quy nạp rằng dãy số $(u_n)$ bị chặn trên bởi 2 và là dãy đơn điệu tăng.
2. Áp dụng định lý Weierstrass về giới hạn của dãy đơn điệu bị chặn để chứng minh $(u_n)$ hội tụ.
3. Tính chính xác $\lim_{n \to \infty} u_n$.

---

### Bài 2.2: Giới hạn dạng vô định $1^\infty$ và Quy tắc L'Hôpital / Taylor
**Đề bài:**
Tính các giới hạn vô định sau:
1. $L_1 = \lim_{x \to 0} \left(\frac{\tan x}{x}\right)^{\frac{1}{x^2}}$
2. $L_2 = \lim_{x \to 0} \frac{e^x - \cos x - x}{x \cdot \sin x}$ bằng phương pháp khai triển Maclaurin với phần dư Peano.

---

### Bài 2.3: Tích phân suy rộng loại 1 có chứa tham số
**Đề bài:**
Khảo sát sự hội tụ và tính giá trị của tích phân suy rộng:
$$I = \int_{0}^{+\infty} x^2 e^{-2x} \, dx$$
1. Khảo sát tính hội tụ bằng định nghĩa giới hạn cận vô cùng.
2. Tính chính xác giá trị của $I$ bằng phương pháp tích phân từng phần.
3. Mở rộng: Xét sự hội tụ của tích phân $\int_{1}^{+\infty} \frac{x^\alpha}{1 + x^4} \, dx$ theo tham số $\alpha \in \mathbb{R}$.

---

## 4. CHUYÊN ĐỀ 3: CHUỖI SỐ, CHUỖI LŨY THỪA & CHUỖI FOURIER
*(Trích xuất từ tài liệu giải tích nâng cao)*

### Bài 3.1: Khảo sát sự hội tụ của chuỗi số dương và chuỗi đan dấu
**Đề bài:**
Xét sự hội tụ (hội tụ tuyệt đối, bán hội tụ hay phân kỳ) của các chuỗi số sau:
1. $\sum_{n=1}^{\infty} \frac{n^2 + 1}{2^n}$ (Áp dụng tiêu chuẩn tỷ số D'Alembert).
2. $\sum_{n=1}^{\infty} \frac{1}{n \cdot \ln(n+1)}$ (Áp dụng tiêu chuẩn tích phân Cauchy-Maclaurin).
3. $\sum_{n=1}^{\infty} \frac{(-1)^n}{\sqrt{n} + 1}$ (Áp dụng tiêu chuẩn Leibniz cho chuỗi đan dấu).

---

### Bài 3.2: Bán kính hội tụ và Miền hội tụ chuỗi lũy thừa
**Đề bài:**
Cho chuỗi lũy thừa:
$$\sum_{n=1}^{\infty} \frac{(x - 3)^n}{n \cdot 4^n}$$
1. Tìm bán kính hội tụ $R$ của chuỗi.
2. Tìm khoảng hội tụ mở.
3. Khảo sát tính hội tụ tại hai mút biên $x = 3 - R$ và $x = 3 + R$ để kết luận miền hội tụ đầy đủ.

---

### Bài 3.3: Khai triển chuỗi Fourier hàm tuần hoàn
**Đề bài:**
Cho hàm số $f(x) = x$ xác định trên đoạn $[-\pi, \pi]$ và tuần hoàn với chu kỳ $T = 2\pi$.
1. Nhận xét tính chẵn/lẻ của $f(x)$ để suy ra các hệ số Fourier $a_0$ và $a_n$.
2. Tính chính xác các hệ số $b_n$.
3. Viết chuỗi Fourier của $f(x)$. Từ đó, áp dụng định lý Dirichlet tại $x = \frac{\pi}{2}$ để tính tổng chuỗi số Leibniz:
$$1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \dots = \frac{\pi}{4}$$

---

## 5. CHUYÊN ĐỀ 4: GIẢI TÍCH ĐA BIẾN & TÍCH PHÂN BỘI (Calculus 2 & 3)
*(Trích xuất từ `CalculusIII.pdf` và `TCC2-Download_com_vn.pdf`)*

### Bài 4.1: Cực trị có điều kiện bằng Phương pháp Nhân tử Lagrange
**Đề bài:**
Tìm giá trị lớn nhất và giá trị nhỏ nhất của hàm số 3 biến:
$$f(x, y, z) = x \cdot y \cdot z$$
trên mặt phẳng ràng buộc:
$$g(x, y, z) = x + y + z - 3 = 0 \quad (\text{với } x > 0, y > 0, z > 0)$$
1. Thiết lập hàm Lagrange: $L(x, y, z, \lambda) = f(x, y, z) - \lambda \cdot (x + y + z - 3)$.
2. Thiết lập và giải hệ phương trình đạo hàm riêng $\nabla L = 0$.
3. Khảo sát vi phân cấp hai $d^2 L$ hoặc ma trận Hessian có viền để kết luận tính chất cực trị.

---

### Bài 4.2: Tích phân kép đổi biến sang Tọa độ cực
**Đề bài:**
Tính tích phân kép:
$$I = \iint_{D} \sqrt{x^2 + y^2} \, dx \, dy$$
trong đó miền $D$ là nửa hình tròn nằm ở nửa mặt phẳng trên:
$$D = \left\{ (x, y) \in \mathbb{R}^2 \mid x^2 + y^2 \le 4, \quad y \ge 0 \right\}$$
1. Mô tả miền lấy tích phân $D$ trong hệ tọa độ cực $(r, \varphi)$.
2. Nêu công thức đổi biến và định thức Jacobi $J = r$.
3. Thiết lập tích phân lặp và tính kết quả chính xác.

---

### Bài 4.3: Tích phân bội ba đổi biến sang Tọa độ cầu
**Đề bài:**
Tính tích phân bội ba:
$$J = \iiint_{V} z \, dx \, dy \, dz$$
trong đó miền $V$ là vật thể giới hạn bởi nửa mặt cầu trên $z = \sqrt{4 - x^2 - y^2}$ và mặt phẳng đáy $z = 0$.
1. Thiết lập miền lấy tích phân trong hệ tọa độ cầu $(\rho, \theta, \varphi)$.
2. Tính tích phân và đối chiếu với tọa độ khối tâm hình học.

---

## 6. CHUYÊN ĐỀ 5: TÍCH PHÂN ĐƯỜNG - MẶT & LÝ THUYẾT TRƯỜNG
*(Trích xuất từ `CalculusIII.pdf`)*

### Bài 5.1: Tích phân đường loại 2 & Định lý Green
**Đề bài:**
Tính công của trường lực $\vec{F} = (P, Q) = (x^2 - y, x + y^2)$ làm dịch chuyển một chất điểm dọc theo chu trình khép kín $C$ là biên của tam giác có các đỉnh $O(0, 0), A(1, 0), B(0, 1)$ định hướng ngược chiều kim đồng hồ:
$$W = \oint_{C} (x^2 - y) \, dx + (x + y^2) \, dy$$
1. Tính trực tiếp bằng cách tham số hóa từng cạnh của tam giác.
2. Áp dụng Định lý Green chuyển về tích phân kép trên miền tam giác $D$:
$$\oint_{C} P \, dx + Q \, dy = \iint_{D} \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right) \, dx \, dy$$
3. So sánh kết quả của hai cách tính.

---

### Bài 5.2: Phân tích Trường thế (Conservative Vector Field) & Hàm thế vị
**Đề bài:**
Cho trường vector trong không gian 3 chiều:
$$\vec{F}(x, y, z) = (2x y + z) \vec{i} + (x^2 + 2y z) \vec{j} + (x + y^2) \vec{k}$$
1. Tính vectơ xoáy $\text{rot}\,\vec{F} = \nabla \times \vec{F}$.
2. Chứng minh $\vec{F}$ là một trường thế (Conservative Field) trên toàn bộ $\mathbb{R}^3$.
3. Tìm hàm thế vị $U(x, y, z)$ thỏa mãn $\nabla U = \vec{F}$ và $U(0, 0, 0) = 0$.
4. Tính tích phân đường $\int_{A}^{B} \vec{F} \cdot d\vec{r}$ với điểm đầu $A(0, 0, 0)$ và điểm cuối $B(1, 2, 3)$.

---

### Bài 5.3: Tích phân mặt loại 2 & Định lý Gauss-Ostrogradsky
**Đề bài:**
Tính thông lượng (Flux) của trường vector $\vec{F}(x, y, z) = (x^3, y^3, z^3)$ đi qua mặt ngoài của mặt cầu kín $S: x^2 + y^2 + z^2 = 1$:
$$\Phi = \iint_{S} x^3 \, dy \, dz + y^3 \, dz \, dx + z^3 \, dx \, dy$$
1. Tính độ phân kỳ $\text{div}\,\vec{F} = \nabla \cdot \vec{F}$.
2. Áp dụng định lý Gauss-Ostrogradsky để chuyển tích phân mặt kín về tích phân bội ba trên khối cầu $V$.
3. Đổi biến sang tọa độ cầu để tính ra đáp số cuối cùng.

---

## 7. CHUYÊN ĐỀ 6: PHƯƠNG TRÌNH VI PHÂN & BIẾN ĐỔI LAPLACE
*(Trích xuất từ `CalculusIII.pdf` và `Tối_ưu.pdf`)*

### Bài 6.1: Phương trình vi phân tuyến tính cấp 2 hệ số hằng có vế phải cộng hưởng
**Đề bài:**
Giải bài toán Cauchy cho phương trình vi phân dao động:
$$y'' + 4y = \sin(2x), \quad y(0) = 0, \quad y'(0) = 1$$
1. Viết phương trình đặc trưng và tìm nghiệm tổng quát của phương trình thuần nhất $y_h(x)$.
2. Xác định nghiệm riêng $y_p(x)$ theo phương pháp hệ số bất định trong trường hợp vế phải cộng hưởng tần số riêng.
3. Kết hợp điều kiện ban đầu để xác định nghiệm duy nhất của bài toán Cauchy.

---

### Bài 6.2: Ứng dụng Biến đổi Laplace giải phương trình vi phân
**Đề bài:**
Sử dụng biến đổi Laplace để giải bài toán giá trị ban đầu:
$$y'' - 3y' + 2y = e^{3t}, \quad y(0) = 1, \quad y'(0) = 0$$
1. Áp dụng biến đổi Laplace cho cả hai vế phương trình với biến ảnh $s$: $\mathcal{L}\{y(t)\} = Y(s)$.
2. Biểu diễn hàm ảnh $Y(s)$ dưới dạng phân thức hữu tỉ.
3. Phân tích phân thức thành các phân thức đơn giản (Partial Fractions).
4. Áp dụng biến đổi Laplace ngược $\mathcal{L}^{-1}\{Y(s)\}$ để tìm nghiệm gốc $y(t)$.

---

## 8. HƯỚNG DẪN THỰC THI CHO NGƯỜI DÙNG
1. **Bạn muốn giải bài nào?** Hãy chọn bài đó, bôi đen cả phần đề bài và paste vào ô chat của **Gemini, Claude hoặc ChatGPT**.
2. **Kèm thêm câu lệnh:** *"Hãy giải chi tiết bài toán trên theo đúng 4 bước trong khung hướng dẫn đính kèm."*
3. Bạn sẽ nhận được lời giải hoàn chỉnh bằng LaTeX kèm đoạn mã SymPy để kiểm chứng lại trong phần mềm.
