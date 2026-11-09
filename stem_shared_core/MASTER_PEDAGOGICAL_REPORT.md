# BÁO CÁO KIỂM ĐỊNH CHẤT LƯỢNG GIÁO DỤC STEM & TÍNH TOÁN HÌNH THỨC (GDPT 2018)

- **Thời điểm kiểm định:** `2026-11-07 23:53:00`
- **Hệ chương trình:** Chương trình Giáo dục Phổ thông 2018 (Bộ GD&ĐT Việt Nam)
- **Phạm vi kiểm thử:** 20 bài toán chuẩn SGK (Lớp 10, 11, 12) & 6 bài kiểm thử Lõi Khoa học Tự nhiên (Vật lý, Hóa học, Sinh học)

---

## 1. TỔNG QUAN CHỈ SỐ CHẤT LƯỢNG (EXECUTIVE QA METRICS)

| Chỉ số Kiểm định (Benchmark Metric) | Kết quả Đạt / Tổng số | Tỷ lệ (%) | Đánh giá Chuẩn Sư phạm |
| :--- | :---: | :---: | :---: |
| **1. Độ chính xác Toán học (Mathematical Accuracy)** | `20/20` bài | **100.00%** | ĐẠT CHUẨN (PASS) |
| **2. Tỷ lệ khử nghiệm ngoại lai (Extraneous Root Rejection)** | `9/9` bài (`10/10` nghiệm) | **100.00%** | ĐẠT CHUẨN (PASS) |
| **3. Tỷ lệ kiểm thử Khoa học (Science Kernel Pass Rate)** | `6/6` test | **100.00%** | ĐẠT CHUẨN (PASS) |
| **4. Tổng thời gian thực thi (Total Execution Time)** | `26` tác vụ | `2010.04 ms` | Trung bình `77.31 ms/bài` |

### Phân bổ Độ chính xác theo Khối lớp (Toán GDPT 2018)

| Khối lớp | Chuyên đề Trọng tâm | Số bài đạt | Tỷ lệ chính xác | Thời gian TB (ms) |
| :---: | :--- | :---: | :---: | :---: |
| **Lớp 10** | Phương trình chứa căn thức quy về bậc hai & Khử nghiệm ngoại lai | `5/5` | **100.00%** | `129.54 ms` |
| **Lớp 11** | Phương trình lượng giác trên đoạn & Cấp số cộng / Cấp số nhân | `5/5` | **100.00%** | `185.16 ms` |
| **Lớp 12** | Khảo sát hàm số (Bậc 3, Phân thức, Tham số m) & PT Căn/Trị tuyệt đối | `10/10` | **100.00%** | `35.81 ms` |

---

## 2. KẾT QUẢ CHI TIẾT 20 BÀI TOÁN SGK TOÁN (LỚP 10, 11, 12)

| Mã bài | Lớp | Hàm Kernel | Biểu thức / Hệ | Kết quả Chuẩn (Ground Truth) | Kết quả Thực tế (Kernel Output) | Khử ngoại lai | Thời gian (ms) | Trạng thái |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| `GDPT2018-G10-001` | 10 | `solve_radical_abs_equation` | `sqrt(2*x^2 - 5*x + 1) = sqrt(x^2 + 2*x - 9)` | S = ['5'], Ngoại lai = ['2'] | S = [5], Ngoại lai = [2] | Đạt (1/1) | `274.39` | **PASS** |
| `GDPT2018-G10-002` | 10 | `solve_radical_abs_equation` | `sqrt(3*x^2 - 9*x + 7) = x - 2` | S = [], Ngoại lai = ['1', '3/2'] | S = [], Ngoại lai = [1, 3/2] | Đạt (2/2) | `64.52` | **PASS** |
| `GDPT2018-G10-003` | 10 | `solve_radical_abs_equation` | `sqrt(x^2 + 3*x - 2) = sqrt(2*x + 4)` | S = ['2'], Ngoại lai = ['-3'] | S = [2], Ngoại lai = [-3] | Đạt (1/1) | `156.87` | **PASS** |
| `GDPT2018-G10-004` | 10 | `solve_radical_abs_equation` | `sqrt(2*x^2 + 3*x - 5) = x + 1` | S = ['2'], Ngoại lai = ['-3'] | S = [2], Ngoại lai = [-3] | Đạt (1/1) | `95.10` | **PASS** |
| `GDPT2018-G10-005` | 10 | `solve_radical_abs_equation` | `sqrt(x^2 - 4*x + 4) = 2*x - 5` | S = ['3'], Ngoại lai = ['7/3'] | S = [3], Ngoại lai = [7/3] | Đạt (1/1) | `56.83` | **PASS** |
| `GDPT2018-G11-001` | 11 | `solve_trig_equation` | `2*cos(x) - sqrt(3) = 0 trên [0, 2*pi]` | Nghiệm = ['pi/6', '11*pi/6'] | Nghiệm = [pi/6, 11*pi/6] | N/A | `192.36` | **PASS** |
| `GDPT2018-G11-002` | 11 | `solve_trig_equation` | `sin(2*x) - cos(x) = 0 trên [0, 2*pi]` | Nghiệm = ['pi/6', 'pi/2', '5*pi/6', '3*pi/2'] | Nghiệm = [pi/6, pi/2, 5*pi/6, 3*pi/2] | N/A | `411.11` | **PASS** |
| `GDPT2018-G11-003` | 11 | `solve_trig_equation` | `cos(2*x) + 3*sin(x) - 2 = 0 trên [0, 2*pi]` | Nghiệm = ['pi/6', 'pi/2', '5*pi/6'] | Nghiệm = [pi/6, pi/2, 5*pi/6] | N/A | `302.40` | **PASS** |
| `GDPT2018-G11-004` | 11 | `solve_system_2vars` | `{ 2*u1 + 4*d = 16 ; 2*u1 + 8*d = 24 }` | (u1, d) = [['4', '2']] | (u1, d) = [['4', '2']] | N/A | `11.61` | **PASS** |
| `GDPT2018-G11-005` | 11 | `solve_polynomial_equation` | `3*(1 + q + q^2) = 21` | Nghiệm = ['-3', '2'] | Nghiệm = [-3, 2] | N/A | `8.31` | **PASS** |
| `GDPT2018-G12-001` | 12 | `analyze_function_variation` | `x^3 - 3*x + 2` | Cực trị/Tới hạn=['-1', '1'], ĐB=['(-oo, -1)', '(1, oo)'], NB=['(-1, 1)'] | Cực trị/Tới hạn=[-1, 1], ĐB=['(-oo, -1)', '(1, oo)'], NB=['(-1, 1)'] | N/A | `21.72` | **PASS** |
| `GDPT2018-G12-002` | 12 | `analyze_function_variation` | `-x^3 + 3*x^2 - 3*x + 1` | Cực trị/Tới hạn=['1'], ĐB=[], NB=['(-oo, oo)'] | Cực trị/Tới hạn=[1], ĐB=[], NB=['(-oo, oo)'] | N/A | `15.70` | **PASS** |
| `GDPT2018-G12-003` | 12 | `analyze_function_variation` | `(2*x + 1)/(x - 1)` | Cực trị/Tới hạn=[], ĐB=[], NB=['(-oo, 1)', '(1, oo)'] | Cực trị/Tới hạn=[], ĐB=[], NB=['(-oo, 1)', '(1, oo)'] | N/A | `26.94` | **PASS** |
| `GDPT2018-G12-004` | 12 | `analyze_function_variation` | `(x^2 - 2*x + 5)/(x - 1)` | Cực trị/Tới hạn=['-1', '3'], ĐB=['(-oo, -1)', '(3, oo)'], NB=['(-1, 1)', '(1, 3)'] | Cực trị/Tới hạn=[-1, 3], ĐB=['(-oo, -1)', '(3, oo)'], NB=['(-1, 1)', '(1, 3)'] | N/A | `76.29` | **PASS** |
| `GDPT2018-G12-005` | 12 | `analyze_function_variation` | `x^3/3 - m*x^2 + (2*m - 1)*x + 1 (với {'m': '2'})` | Cực trị/Tới hạn=['1', '3'], ĐB=['(-oo, 1)', '(3, oo)'], NB=['(1, 3)'] | Cực trị/Tới hạn=[1, 3], ĐB=['(-oo, 1)', '(3, oo)'], NB=['(1, 3)'] | N/A | `30.89` | **PASS** |
| `GDPT2018-G12-006` | 12 | `analyze_function_variation` | `(x + m^2)/(x - 1) (với {'m': '2'})` | Cực trị/Tới hạn=[], ĐB=[], NB=['(-oo, 1)', '(1, oo)'] | Cực trị/Tới hạn=[], ĐB=[], NB=['(-oo, 1)', '(1, oo)'] | N/A | `26.86` | **PASS** |
| `GDPT2018-G12-007` | 12 | `solve_radical_abs_equation` | `sqrt(2*x + 3) = x` | S = ['3'], Ngoại lai = ['-1'] | S = [3], Ngoại lai = [-1] | Đạt (1/1) | `46.25` | **PASS** |
| `GDPT2018-G12-008` | 12 | `solve_radical_abs_equation` | `sqrt(x + 2) = x - 4` | S = ['7'], Ngoại lai = ['2'] | S = [7], Ngoại lai = [2] | Đạt (1/1) | `46.96` | **PASS** |
| `GDPT2018-G12-009` | 12 | `solve_radical_abs_equation` | `sqrt(x^2 - 3*x + 4) = 1 - x` | S = [], Ngoại lai = ['3'] | S = [], Ngoại lai = [3] | Đạt (1/1) | `45.91` | **PASS** |
| `GDPT2018-G12-010` | 12 | `solve_radical_abs_equation` | `Abs(x - 1) = 2*x - 5` | S = ['4'], Ngoại lai = ['2'] | S = [4], Ngoại lai = [2] | Đạt (1/1) | `20.58` | **PASS** |

---

## 3. PHÂN TÍCH SƯ PHẠM & KIỂM SOÁT SAI LẦM HỌC SINH (PEDAGOGICAL RUBRIC)

### GDPT2018-G10-001 (Lớp 10 - Mức độ: `comprehension`)
- **Đề bài:** Giải phương trình chứa căn thức $\sqrt{2x^2 - 5x + 1} = \sqrt{x^2 + 2x - 9}$.
- **Mục tiêu năng lực (Learning Objective):** Giải phương trình dạng $\sqrt{f(x)} = \sqrt{g(x)}$ bằng cách bình phương hai vế và thử lại để loại nghiệm ngoại lai $x = 2$ làm biểu thức dưới dấu căn âm.
- **Sai lầm thường gặp (Common Pitfall):** Quên kiểm tra điều kiện biểu thức dưới dấu căn không âm sau khi khử căn ở cả hai vế.
- **Đối chiếu tính toán hình thức:** `S = [5], Ngoại lai = [2]` (Thời gian: `274.39 ms` — **ĐẠT**)

### GDPT2018-G10-002 (Lớp 10 - Mức độ: `application`)
- **Đề bài:** Giải phương trình $\sqrt{3x^2 - 9x + 7} = x - 2$.
- **Mục tiêu năng lực (Learning Objective):** Nhận diện trường hợp cả hai nghiệm của phương trình hệ quả bậc hai ($x = 1$ và $x = 3/2$) đều vi phạm điều kiện $x \ge 2$, dẫn đến phương trình vô nghiệm.
- **Sai lầm thường gặp (Common Pitfall):** Thấy tam thức dưới căn $3x^2 - 9x + 7 > 0, \forall x \in \mathbb{R}$ nên kết luận nhầm rằng mọi nghiệm của phương trình bậc hai đều thỏa mãn.
- **Đối chiếu tính toán hình thức:** `S = [], Ngoại lai = [1, 3/2]` (Thời gian: `64.52 ms` — **ĐẠT**)

### GDPT2018-G10-003 (Lớp 10 - Mức độ: `comprehension`)
- **Đề bài:** Giải phương trình $\sqrt{x^2 + 3x - 2} = \sqrt{2x + 4}$.
- **Mục tiêu năng lực (Learning Objective):** Rèn kỹ năng đặt điều kiện $2x + 4 \ge 0$ để loại nghiệm âm ngoại lai $x = -3$.
- **Sai lầm thường gặp (Common Pitfall):** Không thử lại nghiệm $x = -3$ vào biểu thức dưới căn.
- **Đối chiếu tính toán hình thức:** `S = [2], Ngoại lai = [-3]` (Thời gian: `156.87 ms` — **ĐẠT**)

### GDPT2018-G10-004 (Lớp 10 - Mức độ: `comprehension`)
- **Đề bài:** Giải phương trình $\sqrt{2x^2 + 3x - 5} = x + 1$.
- **Mục tiêu năng lực (Learning Objective):** Phân biệt rõ tập xác định của căn thức $x \in (-\infty; -5/2] \cup [1; +\infty)$ với điều kiện có nghiệm của vế phải $x \ge -1$ (loại $x = -3$ dù $x = -3$ làm căn thức có nghĩa).
- **Sai lầm thường gặp (Common Pitfall):** Chỉ kiểm tra $2x^2 + 3x - 5 \ge 0$ (thấy tại $x = -3$ biểu thức bằng $4 > 0$) nên nhận nhầm $x = -3$.
- **Đối chiếu tính toán hình thức:** `S = [2], Ngoại lai = [-3]` (Thời gian: `95.10 ms` — **ĐẠT**)

### GDPT2018-G10-005 (Lớp 10 - Mức độ: `application`)
- **Đề bài:** Giải phương trình $\sqrt{x^2 - 4x + 4} = 2x - 5$.
- **Mục tiêu năng lực (Learning Objective):** Vận dụng hằng đẳng thức $\sqrt{(x - 2)^2} = |x - 2| = 2x - 5$ và loại nghiệm phân số ngoại lai $x = 7/3 < 5/2$.
- **Sai lầm thường gặp (Common Pitfall):** Khai căn $\sqrt{(x-2)^2} = x - 2$ mà quên dấu giá trị tuyệt đối hoặc quên điều kiện $2x - 5 \ge 0$.
- **Đối chiếu tính toán hình thức:** `S = [3], Ngoại lai = [7/3]` (Thời gian: `56.83 ms` — **ĐẠT**)

### GDPT2018-G11-001 (Lớp 11 - Mức độ: `recognition`)
- **Đề bài:** Tìm các nghiệm thuộc đoạn $[0; 2\pi]$ của phương trình lượng giác $2\cos(x) - \sqrt{3} = 0$.
- **Mục tiêu năng lực (Learning Objective):** Giải đúng phương trình lượng giác cơ bản $\cos(x) = \frac{\sqrt{3}}{2}$ và lọc nghiệm thuộc $[0; 2\pi]$.
- **Sai lầm thường gặp (Common Pitfall):** Dùng nhầm công thức nghiệm của hàm $\sin(x)$ ($\pi - \alpha$) cho phương trình $\cos(x)$.
- **Đối chiếu tính toán hình thức:** `Nghiệm = [pi/6, 11*pi/6]` (Thời gian: `192.36 ms` — **ĐẠT**)

### GDPT2018-G11-002 (Lớp 11 - Mức độ: `comprehension`)
- **Đề bài:** Giải phương trình lượng giác $\sin(2x) - \cos(x) = 0$ trên đoạn $[0; 2\pi]$.
- **Mục tiêu năng lực (Learning Objective):** Áp dụng công thức nhân đôi $\sin(2x) = 2\sin(x)\cos(x)$ để đặt nhân tử chung $\cos(x)$, tránh chia hai vế cho $\cos(x)$ làm mất nghiệm.
- **Sai lầm thường gặp (Common Pitfall):** Chia cả hai vế cho $\cos(x)$ dẫn đến bỏ sót hai nghiệm $x = \frac{\pi}{2}$ và $x = \frac{3\pi}{2}$.
- **Đối chiếu tính toán hình thức:** `Nghiệm = [pi/6, pi/2, 5*pi/6, 3*pi/2]` (Thời gian: `411.11 ms` — **ĐẠT**)

### GDPT2018-G11-003 (Lớp 11 - Mức độ: `application`)
- **Đề bài:** Tìm nghiệm trên đoạn $[0; 2\pi]$ của phương trình $\cos(2x) + 3\sin(x) - 2 = 0$.
- **Mục tiêu năng lực (Learning Objective):** Sử dụng công thức nhân đôi $\cos(2x) = 1 - 2\sin^2(x)$ để quy về phương trình bậc hai theo $\sin(x)$.
- **Sai lầm thường gặp (Common Pitfall):** Đếm trùng nghiệm $x = \frac{\pi}{2}$ thành 2 nghiệm trên một vòng tròn lượng giác.
- **Đối chiếu tính toán hình thức:** `Nghiệm = [pi/6, pi/2, 5*pi/6]` (Thời gian: `302.40 ms` — **ĐẠT**)

### GDPT2018-G11-004 (Lớp 11 - Mức độ: `comprehension`)
- **Đề bài:** Cho cấp số cộng $(u_n)$ có số hạng đầu $u_1$ và công sai $d$ thỏa mãn hệ $\begin{cases} u_1 + u_5 = 16 \\ u_3 + u_7 = 24 \end{cases}$. Tìm $(u_1, d)$.
- **Mục tiêu năng lực (Learning Objective):** Biểu diễn số hạng tổng quát cấp số cộng $u_n = u_1 + (n - 1)d$ để đưa về hệ phương trình bậc nhất hai ẩn $(u_1, d)$.
- **Sai lầm thường gặp (Common Pitfall):** Nhầm công thức số hạng tổng quát thành $u_n = u_1 + n\cdot d$.
- **Đối chiếu tính toán hình thức:** `(u1, d) = [['4', '2']]` (Thời gian: `11.61 ms` — **ĐẠT**)

### GDPT2018-G11-005 (Lớp 11 - Mức độ: `application`)
- **Đề bài:** Cho cấp số nhân $(u_n)$ có số hạng đầu $u_1 = 3$ và tổng 3 số hạng đầu tiên $S_3 = 21$. Tìm công bội $q$.
- **Mục tiêu năng lực (Learning Objective):** Thiết lập phương trình tổng cấp số nhân $S_3 = u_1(1 + q + q^2) = 21$ và tìm đầy đủ cả công bội dương lẫn công bội âm.
- **Sai lầm thường gặp (Common Pitfall):** Bỏ sót nghiệm công bội âm $q = -3$ khi đề bài không giới hạn cấp số nhân dương.
- **Đối chiếu tính toán hình thức:** `Nghiệm = [-3, 2]` (Thời gian: `8.31 ms` — **ĐẠT**)

### GDPT2018-G12-001 (Lớp 12 - Mức độ: `comprehension`)
- **Đề bài:** Khảo sát sự biến thiên và tìm các điểm cực trị của hàm số $y = x^3 - 3x + 2$.
- **Mục tiêu năng lực (Learning Objective):** Xác định đúng tập xác định, đạo hàm, bảng biến thiên và tọa độ điểm cực đại, cực tiểu của hàm bậc ba.
- **Sai lầm thường gặp (Common Pitfall):** Nhầm lẫn giữa 'điểm cực trị của hàm số' ($x_0$) và 'điểm cực trị của đồ thị hàm số' $(x_0; y_0)$.
- **Đối chiếu tính toán hình thức:** `Cực trị/Tới hạn=[-1, 1], ĐB=['(-oo, -1)', '(1, oo)'], NB=['(-1, 1)']` (Thời gian: `21.72 ms` — **ĐẠT**)

### GDPT2018-G12-002 (Lớp 12 - Mức độ: `application`)
- **Đề bài:** Khảo sát sự biến thiên và tìm cực trị của hàm số $y = -x^3 + 3x^2 - 3x + 1$.
- **Mục tiêu năng lực (Learning Objective):** Nhận diện nghiệm kép của đạo hàm $y' = -3(x-1)^2 \le 0$ không làm $y'$ đổi dấu nên hàm số nghịch biến trên toàn trục số $\mathbb{R}$ và không có cực trị.
- **Sai lầm thường gặp (Common Pitfall):** Kết luận sai rằng $x = 1$ là điểm cực trị chỉ vì $y'(1) = 0$ mà quên kiểm tra điều kiện đổi dấu của $y'$.
- **Đối chiếu tính toán hình thức:** `Cực trị/Tới hạn=[1], ĐB=[], NB=['(-oo, oo)']` (Thời gian: `15.70 ms` — **ĐẠT**)

### GDPT2018-G12-003 (Lớp 12 - Mức độ: `comprehension`)
- **Đề bài:** Khảo sát sự biến thiên và tìm các đường tiệm cận của hàm số phân thức $y = \frac{2x + 1}{x - 1}$.
- **Mục tiêu năng lực (Learning Objective):** Nắm vững cách tìm tập xác định, tiệm cận đứng, tiệm cận ngang và kết luận tính đơn điệu trên từng khoảng xác định của hàm nhất biến.
- **Sai lầm thường gặp (Common Pitfall):** Gộp hai khoảng nghịch biến thành $\mathbb{R} \setminus \{1\}$ thay vì viết tách biệt $(-\infty; 1)$ và $(1; +\infty)$ theo chuẩn SGK GDPT 2018.
- **Đối chiếu tính toán hình thức:** `Cực trị/Tới hạn=[], ĐB=[], NB=['(-oo, 1)', '(1, oo)']` (Thời gian: `26.94 ms` — **ĐẠT**)

### GDPT2018-G12-004 (Lớp 12 - Mức độ: `application`)
- **Đề bài:** Khảo sát sự biến thiên, tìm cực trị và các đường tiệm cận (đứng, xiên) của hàm số $y = \frac{x^2 - 2x + 5}{x - 1}$.
- **Mục tiêu năng lực (Learning Objective):** Khảo sát hàm phân thức bậc hai trên bậc nhất (trọng tâm mới của GDPT 2018), xác định tiệm cận xiên và các khoảng đơn điệu bị chia cắt bởi điểm gián đoạn $x = 1$.
- **Sai lầm thường gặp (Common Pitfall):** Quên điểm gián đoạn $x = 1$ và kết luận hàm số nghịch biến trên toàn khoảng $(-1; 3)$ thay vì $(-1; 1)$ và $(1; 3)$.
- **Đối chiếu tính toán hình thức:** `Cực trị/Tới hạn=[-1, 3], ĐB=['(-oo, -1)', '(3, oo)'], NB=['(-1, 1)', '(1, 3)']` (Thời gian: `76.29 ms` — **ĐẠT**)

### GDPT2018-G12-005 (Lớp 12 - Mức độ: `high_application`)
- **Đề bài:** Cho hàm số $y = \frac{1}{3}x^3 - mx^2 + (2m - 1)x + 1$ (với $m$ là tham số thực). Tìm điều kiện của $m$ để hàm số có hai điểm cực trị và khảo sát sự biến thiên khi $m = 2$.
- **Mục tiêu năng lực (Learning Objective):** Biện luận đạo hàm bậc hai chứa tham số $y' = x^2 - 2mx + 2m - 1 = (x - 1)(x - 2m + 1)$ và khảo sát chính xác tại giá trị tham số cụ thể.
- **Sai lầm thường gặp (Common Pitfall):** Quên loại giá trị $m = 1$ khiến hai nghiệm của $y' = 0$ trùng nhau ($x_1 = x_2 = 1$) làm suy biến cực trị.
- **Đối chiếu tính toán hình thức:** `Cực trị/Tới hạn=[1, 3], ĐB=['(-oo, 1)', '(3, oo)'], NB=['(1, 3)']` (Thời gian: `30.89 ms` — **ĐẠT**)

### GDPT2018-G12-006 (Lớp 12 - Mức độ: `application`)
- **Đề bài:** Cho hàm số phân thức $y = \frac{x + m^2}{x - 1}$ với tham số $m$. Chứng minh hàm số luôn nghịch biến trên từng khoảng xác định với mọi $m \in \mathbb{R}$ và khảo sát khi $m = 2$.
- **Mục tiêu năng lực (Learning Objective):** Tính đạo hàm chứa tham số của hàm phân thức $y' = \frac{-1 - m^2}{(x - 1)^2} < 0, \forall x \neq 1, \forall m \in \mathbb{R}$.
- **Sai lầm thường gặp (Common Pitfall):** Xét dấu tử số $-1 - m^2 \le 0$ thay vì khẳng định chặt $-1 - m^2 < 0$ (hàm phân thức không suy biến thành hàm hằng với mọi $m$).
- **Đối chiếu tính toán hình thức:** `Cực trị/Tới hạn=[], ĐB=[], NB=['(-oo, 1)', '(1, oo)']` (Thời gian: `26.86 ms` — **ĐẠT**)

### GDPT2018-G12-007 (Lớp 12 - Mức độ: `comprehension`)
- **Đề bài:** Giải phương trình vô tỉ $\sqrt{2x + 3} = x$ trên tập số thực $\mathbb{R}$.
- **Mục tiêu năng lực (Learning Objective):** Thực hiện đúng phép biến đổi tương đương $\sqrt{A} = B \iff \{B \ge 0, A = B^2\}$ để loại bỏ nghiệm ngoại lai $x = -1$.
- **Sai lầm thường gặp (Common Pitfall):** Chỉ đặt điều kiện trong căn $2x + 3 \ge 0 \iff x \ge -3/2$ rồi nhận luôn nghiệm $x = -1$ mà không thử lại.
- **Đối chiếu tính toán hình thức:** `S = [3], Ngoại lai = [-1]` (Thời gian: `46.25 ms` — **ĐẠT**)

### GDPT2018-G12-008 (Lớp 12 - Mức độ: `application`)
- **Đề bài:** Giải phương trình chứa căn thức $\sqrt{x + 2} = x - 4$.
- **Mục tiêu năng lực (Learning Objective):** Kiểm tra khả năng phát hiện nghiệm ngoại lai dương ($x = 2$) thỏa mãn điều kiện căn thức có nghĩa ($x \ge -2$) nhưng vi phạm điều kiện vế phải không âm ($x \ge 4$).
- **Sai lầm thường gặp (Common Pitfall):** Thấy $x = 2 > 0$ và $2 + 2 = 4 > 0$ nên chủ quan không thế lại vào vế phải $x - 4 = -2 < 0$.
- **Đối chiếu tính toán hình thức:** `S = [7], Ngoại lai = [2]` (Thời gian: `46.96 ms` — **ĐẠT**)

### GDPT2018-G12-009 (Lớp 12 - Mức độ: `application`)
- **Đề bài:** Giải phương trình vô tỉ $\sqrt{x^2 - 3x + 4} = 1 - x$.
- **Mục tiêu năng lực (Learning Objective):** Đánh giá trường hợp phương trình vô nghiệm hoàn toàn do nghiệm duy nhất sinh ra khi bình phương ($x = 3$) là nghiệm ngoại lai.
- **Sai lầm thường gặp (Common Pitfall):** Rút gọn $x^2$ hai vế ra phương trình bậc nhất $x = 3$ nên quên mất đây là phương trình hệ quả và không thử lại nghiệm.
- **Đối chiếu tính toán hình thức:** `S = [], Ngoại lai = [3]` (Thời gian: `45.91 ms` — **ĐẠT**)

### GDPT2018-G12-010 (Lớp 12 - Mức độ: `comprehension`)
- **Đề bài:** Giải phương trình chứa dấu giá trị tuyệt đối $|x - 1| = 2x - 5$.
- **Mục tiêu năng lực (Learning Objective):** Phá dấu giá trị tuyệt đối $|A| = B \iff \{B \ge 0, A = \pm B\}$ và loại bỏ nghiệm ngoại lai $x = 2$ sinh ra từ nhánh $A = -B$.
- **Sai lầm thường gặp (Common Pitfall):** Chia 2 trường hợp $A = B$ và $A = -B$ nhưng quên đặt điều kiện $B \ge 0$ dẫn đến nhận nhầm nghiệm ngoại lai $x = 2$.
- **Đối chiếu tính toán hình thức:** `S = [4], Ngoại lai = [2]` (Thời gian: `20.58 ms` — **ĐẠT**)

---

## 4. KẾT QUẢ KIỂM ĐỊNH 3 LÕI KHOA HỌC TỰ NHIÊN (VẬT LÝ - HÓA HỌC - SINH HỌC)

| Mã Test | Phân môn | Hàm API Kiểm thử | Đầu vào (Input) | Đầu ra Kỳ vọng | Đầu ra Thực tế | Thời gian (ms) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `SCI-PHY-001` | Vật lý (Physics) | `solve_harmonic_oscillator` | `A=0.1, omega=10.0, phi=0.0, mass=0.2` | `v_max=1.0, total_energy_W=0.1, x_str hợp lệ` | `x_str='cos(10*t)/10', v_max=1, W=0.1` | `77.70` | **PASS** |
| `SCI-PHY-002` | Vật lý (Physics) | `solve_rlc_circuit` | `R=40, L=0.5, C=5e-4, U=100, omega=100` | `Z=50.0, I_rms=2.0, power_P=160.0, cos_phi=0.8` | `Z=50, I_rms=2, power_P=160, cos_phi=0.8` | `0.03` | **PASS** |
| `SCI-CHEM-001` | Hóa học (Chemistry) | `balance_chemical_equation` | `'Fe + O2 -> Fe2O3'` | `'4Fe + 3O2 -> 2Fe2O3'` | `'4Fe + 3O2 -> 2Fe2O3'` | `0.38` | **PASS** |
| `SCI-CHEM-002` | Hóa học (Chemistry) | `calculate_solution_concentrations` | `m_solute_gram=11.7, molar_mass=58.5, v_solution_liter=0.5` | `C_M = 0.4 M` | `C_M = 0.4 M` | `0.01` | **PASS** |
| `SCI-BIO-001` | Sinh học (Biology) | `solve_mendelian_cross` | `parent1='AaBb', parent2='AaBb'` | `'9 A-B- : 3 A-bb : 3 aaB- : 1 aabb'` | `'9 A-B- : 3 A-bb : 3 aaB- : 1 aabb'` | `0.34` | **PASS** |
| `SCI-BIO-002` | Sinh học (Biology) | `analyze_hardy_weinberg` | `recessive_phenotype_freq=0.16` | `p_freq=0.6, q_freq=0.4, is_in_equilibrium=True` | `p_freq=0.6, q_freq=0.4, is_in_equilibrium=True` | `0.01` | **PASS** |

---

## 5. KẾT LUẬN CỦA HỘI ĐỒNG KIỂM ĐỊNH STEM

> **CHỨNG NHẬN ĐẠT CHUẨN (100% PASS):** Toàn bộ 20 bài toán đại số & giải tích (Lớp 10, 11, 12) theo Chương trình GDPT 2018 và 6 bài kiểm thử lõi Khoa học Tự nhiên (Vật lý, Hóa học, Sinh học) đều đạt độ chính xác tuyệt đối. Hệ thống xử lý chính xác 100% các trường hợp nghiệm ngoại lai phát sinh khi bình phương hai vế hoặc phá dấu giá trị tuyệt đối, đồng thời phân tách đúng các khoảng đơn điệu qua điểm gián đoạn.
