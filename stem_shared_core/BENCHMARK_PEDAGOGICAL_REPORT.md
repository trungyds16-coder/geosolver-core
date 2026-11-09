# BÁO CÁO THẨM ĐỊNH SƯ PHẠM & ĐỘ CHÍNH XÁC LÕI ĐẠI SỐ (`algebra_kernel.py`)

- **Mã bộ dữ liệu:** `VN_GDPT2018_G12_CALC_BENCH_V1`
- **Chương trình giáo dục:** `VN_GDPT_2018` (Lớp 12)
- **Phiên bản:** `1.0.0`
- **Thời điểm kiểm định:** `2026-11-05 16:38:47`

---

## 1. Tổng quan Kết quả Thẩm định (Executive Summary)

| Chỉ số đánh giá (Benchmark Metric) | Kết quả | Đánh giá Sư phạm |
|---|---|---|
| **1. Tính đúng đắn toán học (Mathematical Correctness)** | **10/10 (100.0%)** | ĐẠT CHUẨN SGK |
| **2. Tỷ lệ loại bỏ nghiệm ngoại lai (Extraneous Root Rejection)** | **4/4 (100.0%)** | TUYỆT ĐỐI AN TOÀN |
| **3. Tổng thời gian thực thi (Total Execution Time)** | **1077.732 ms** | Thời gian phản hồi tức thời |
| **4. Thời gian trung bình mỗi bài (Mean Latency)** | **107.773 ms / bài** | Đạt chuẩn tương tác thời gian thực |

---

## 2. Bảng Kết quả Chi tiết Từng Bài toán

| Mã bài toán | Phân loại | Hàm Kernel | Độ đúng đắn | Khử nghiệm ngoại lai | Điểm Rubric | Thời gian (ms) |
|---|---|---|---|---|---|---|
| `GDPT2018-G12-001` | `cubic_variation` | `analyze_function_variation` | **PASS** | **N/A** | 10.0/10.0 | 303.295 |
| `GDPT2018-G12-002` | `cubic_variation` | `analyze_function_variation` | **PASS** | **N/A** | 10.0/10.0 | 30.971 |
| `GDPT2018-G12-003` | `rational_variation` | `analyze_function_variation` | **PASS** | **N/A** | 10.0/10.0 | 80.002 |
| `GDPT2018-G12-004` | `rational_variation` | `analyze_function_variation` | **PASS** | **N/A** | 10.0/10.0 | 141.612 |
| `GDPT2018-G12-005` | `parametric_variation` | `analyze_function_variation` | **PASS** | **N/A** | 10.0/10.0 | 78.06 |
| `GDPT2018-G12-006` | `parametric_variation` | `analyze_function_variation` | **PASS** | **N/A** | 10.0/10.0 | 83.589 |
| `GDPT2018-G12-007` | `radical_equation` | `solve_radical_abs_equation` | **PASS** | **PASS (100%)** | 10.0/10.0 | 88.223 |
| `GDPT2018-G12-008` | `radical_equation` | `solve_radical_abs_equation` | **PASS** | **PASS (100%)** | 10.0/10.0 | 104.005 |
| `GDPT2018-G12-009` | `radical_equation` | `solve_radical_abs_equation` | **PASS** | **PASS (100%)** | 10.0/10.0 | 103.733 |
| `GDPT2018-G12-010` | `abs_equation` | `solve_radical_abs_equation` | **PASS** | **PASS (100%)** | 10.0/10.0 | 64.242 |

---

## 3. Phân tích Sư phạm & Đối sánh Ground-Truth Chi tiết

### Bài toán `GDPT2018-G12-001` (cubic_variation - Mức độ: `comprehension`)
- **Đề bài:** Khảo sát sự biến thiên và tìm các điểm cực trị của hàm số $y = x^3 - 3x + 2$.
- **Mục tiêu sư phạm:** Xác định đúng tập xác định, đạo hàm, bảng biến thiên và tọa độ điểm cực đại, cực tiểu của hàm bậc ba.
- **Thời gian tính toán:** `303.295 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định:** `Reals` (Chuẩn: `Reals`)
- **Đạo hàm cấp 1 ($y'$):** `3*x**2 - 3`
- **Khoảng đồng biến:** `['(-oo, -1)', '(1, oo)']` | **Khoảng nghịch biến:** `['(-1, 1)']`
- **Điểm cực đại:** `[('-1', '4')]` | **Điểm cực tiểu:** `[('1', '0')]`
- **Tiệm cận:** TCĐ `[]`, TCN `[]`, TCX `[]`
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[FIND_DOMAIN]` (20%): Tìm tập xác định $D = \mathbb{R}$.
  2. `[COMPUTE_DERIVATIVE]` (30%): Tính đạo hàm $y' = 3x^2 - 3$ và giải $y' = 0 \iff x = \pm 1$.
  3. `[VARIATION_TABLE]` (30%): Lập bảng xét dấu $y'$ và kết luận khoảng đồng biến $(-\infty; -1)$, $(1; +\infty)$, nghịch biến $(-1; 1)$.
  4. `[CONCLUDE_EXTREMA]` (20%): Kết luận điểm cực đại $(-1; 4)$ và điểm cực tiểu $(1; 0)$.
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Nhầm lẫn giữa 'điểm cực trị của hàm số' ($x_0$) và 'điểm cực trị của đồ thị hàm số' $(x_0; y_0)$.

### Bài toán `GDPT2018-G12-002` (cubic_variation - Mức độ: `application`)
- **Đề bài:** Khảo sát sự biến thiên và tìm cực trị của hàm số $y = -x^3 + 3x^2 - 3x + 1$.
- **Mục tiêu sư phạm:** Nhận diện nghiệm kép của đạo hàm $y' = -3(x-1)^2 \le 0$ không làm $y'$ đổi dấu nên hàm số nghịch biến trên toàn trục số $\mathbb{R}$ và không có cực trị.
- **Thời gian tính toán:** `30.971 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định:** `Reals` (Chuẩn: `Reals`)
- **Đạo hàm cấp 1 ($y'$):** `-3*x**2 + 6*x - 3`
- **Khoảng đồng biến:** `[]` | **Khoảng nghịch biến:** `['(-oo, oo)']`
- **Điểm cực đại:** `[]` | **Điểm cực tiểu:** `[]`
- **Tiệm cận:** TCĐ `[]`, TCN `[]`, TCX `[]`
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[FIND_DOMAIN]` (20%): Tập xác định $D = \mathbb{R}$.
  2. `[CHECK_DERIVATIVE_SIGN]` (50%): Tính $y' = -3x^2 + 6x - 3 = -3(x-1)^2 \le 0, \forall x \in \mathbb{R}$ (dấu bằng chỉ xảy ra tại $x = 1$).
  3. `[MERGE_MONOTONIC_INTERVAL]` (30%): Kết luận hàm số nghịch biến trên $(-\infty; +\infty)$ và không có cực trị.
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Kết luận sai rằng $x = 1$ là điểm cực trị chỉ vì $y'(1) = 0$ mà quên kiểm tra điều kiện đổi dấu của $y'$.

### Bài toán `GDPT2018-G12-003` (rational_variation - Mức độ: `comprehension`)
- **Đề bài:** Khảo sát sự biến thiên và tìm các đường tiệm cận của hàm số phân thức $y = \frac{2x + 1}{x - 1}$.
- **Mục tiêu sư phạm:** Nắm vững cách tìm tập xác định, tiệm cận đứng, tiệm cận ngang và kết luận tính đơn điệu trên từng khoảng xác định của hàm nhất biến.
- **Thời gian tính toán:** `80.002 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định:** `R \ {1}` (Chuẩn: `R \ {1}`)
- **Đạo hàm cấp 1 ($y'$):** `-3/(x - 1)**2`
- **Khoảng đồng biến:** `[]` | **Khoảng nghịch biến:** `['(-oo, 1)', '(1, oo)']`
- **Điểm cực đại:** `[]` | **Điểm cực tiểu:** `[]`
- **Tiệm cận:** TCĐ `['1']`, TCN `['2']`, TCX `[]`
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[FIND_DOMAIN]` (25%): Tập xác định $D = \mathbb{R} \setminus \{1\}$.
  2. `[COMPUTE_DERIVATIVE]` (35%): Tính $y' = \frac{-3}{(x - 1)^2} < 0, \forall x \neq 1$.
  3. `[FIND_ASYMPTOTES]` (40%): Xác định tiệm cận đứng $x = 1$ và tiệm cận ngang $y = 2$.
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Gộp hai khoảng nghịch biến thành $\mathbb{R} \setminus \{1\}$ thay vì viết tách biệt $(-\infty; 1)$ và $(1; +\infty)$ theo chuẩn SGK GDPT 2018.

### Bài toán `GDPT2018-G12-004` (rational_variation - Mức độ: `application`)
- **Đề bài:** Khảo sát sự biến thiên, tìm cực trị và các đường tiệm cận (đứng, xiên) của hàm số $y = \frac{x^2 - 2x + 5}{x - 1}$.
- **Mục tiêu sư phạm:** Khảo sát hàm phân thức bậc hai trên bậc nhất (trọng tâm mới của GDPT 2018), xác định tiệm cận xiên và các khoảng đơn điệu bị chia cắt bởi điểm gián đoạn $x = 1$.
- **Thời gian tính toán:** `141.612 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định:** `R \ {1}` (Chuẩn: `R \ {1}`)
- **Đạo hàm cấp 1 ($y'$):** `(x**2 - 2*x - 3)/(x**2 - 2*x + 1)`
- **Khoảng đồng biến:** `['(-oo, -1)', '(3, oo)']` | **Khoảng nghịch biến:** `['(-1, 1)', '(1, 3)']`
- **Điểm cực đại:** `[('-1', '-4')]` | **Điểm cực tiểu:** `[('3', '4')]`
- **Tiệm cận:** TCĐ `['1']`, TCN `[]`, TCX `['x - 1']`
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[FIND_DOMAIN]` (15%): Tập xác định $D = \mathbb{R} \setminus \{1\}$.
  2. `[COMPUTE_DERIVATIVE]` (35%): Viết $y = x - 1 + \frac{4}{x - 1}$, tính $y' = 1 - \frac{4}{(x - 1)^2} = \frac{x^2 - 2x - 3}{(x - 1)^2}$, giải $y' = 0 \iff x = -1$ hoặc $x = 3$.
  3. `[VARIATION_AND_EXTREMA]` (25%): Lập bảng biến thiên có gạch sọc kép tại $x = 1$; cực đại tại $(-1; -4)$, cực tiểu tại $(3; 4)$.
  4. `[OBLIQUE_ASYMPTOTE]` (25%): Xác định tiệm cận đứng $x = 1$ và tiệm cận xiên $y = x - 1$.
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Quên điểm gián đoạn $x = 1$ và kết luận hàm số nghịch biến trên toàn khoảng $(-1; 3)$ thay vì $(-1; 1)$ và $(1; 3)$.

### Bài toán `GDPT2018-G12-005` (parametric_variation - Mức độ: `high_application`)
- **Đề bài:** Cho hàm số $y = \frac{1}{3}x^3 - mx^2 + (2m - 1)x + 1$ (với $m$ là tham số thực). Tìm điều kiện của $m$ để hàm số có hai điểm cực trị và khảo sát sự biến thiên khi $m = 2$.
- **Mục tiêu sư phạm:** Biện luận đạo hàm bậc hai chứa tham số $y' = x^2 - 2mx + 2m - 1 = (x - 1)(x - 2m + 1)$ và khảo sát chính xác tại giá trị tham số cụ thể.
- **Thời gian tính toán:** `78.06 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định:** `Reals` (Chuẩn: `Reals`)
- **Đạo hàm cấp 1 ($y'$):** `x**2 - 4*x + 3`
- **Đạo hàm chứa tham số $m$:** `-2*m*x + 2*m + x**2 - 1` (Điều kiện: `m != 1`)
- **Khoảng đồng biến:** `['(-oo, 1)', '(3, oo)']` | **Khoảng nghịch biến:** `['(1, 3)']`
- **Điểm cực đại:** `[('1', '7/3')]` | **Điểm cực tiểu:** `[('3', '1')]`
- **Tiệm cận:** TCĐ `[]`, TCN `[]`, TCX `[]`
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[PARAMETRIC_DERIVATIVE]` (50%): Tính $y' = x^2 - 2mx + 2m - 1$, tính $\Delta' = m^2 - 2m + 1 = (m - 1)^2$. Hàm số có 2 cực trị khi $\Delta' > 0 \iff m \neq 1$.
  2. `[SUBSTITUTE_PARAMETER]` (50%): Với $m = 2$, $y' = x^2 - 4x + 3 = 0 \iff x = 1$ hoặc $x = 3$; lập bảng biến thiên và tìm cực đại $(1; \frac{7}{3})$, cực tiểu $(3; 1)$.
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Quên loại giá trị $m = 1$ khiến hai nghiệm của $y' = 0$ trùng nhau ($x_1 = x_2 = 1$) làm suy biến cực trị.

### Bài toán `GDPT2018-G12-006` (parametric_variation - Mức độ: `application`)
- **Đề bài:** Cho hàm số phân thức $y = \frac{x + m^2}{x - 1}$ với tham số $m$. Chứng minh hàm số luôn nghịch biến trên từng khoảng xác định với mọi $m \in \mathbb{R}$ và khảo sát khi $m = 2$.
- **Mục tiêu sư phạm:** Tính đạo hàm chứa tham số của hàm phân thức $y' = \frac{-1 - m^2}{(x - 1)^2} < 0, \forall x \neq 1, \forall m \in \mathbb{R}$.
- **Thời gian tính toán:** `83.589 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định:** `R \ {1}` (Chuẩn: `R \ {1}`)
- **Đạo hàm cấp 1 ($y'$):** `-5/(x - 1)**2`
- **Đạo hàm chứa tham số $m$:** `(-m**2 - 1)/(x - 1)**2` (Điều kiện: `ForAll(m, Reals)`)
- **Khoảng đồng biến:** `[]` | **Khoảng nghịch biến:** `['(-oo, 1)', '(1, oo)']`
- **Điểm cực đại:** `[]` | **Điểm cực tiểu:** `[]`
- **Tiệm cận:** TCĐ `['1']`, TCN `['1']`, TCX `[]`
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[PARAMETRIC_DERIVATIVE]` (60%): Tính $y' = \frac{-1 - m^2}{(x - 1)^2} < 0$ do $-1 - m^2 \le -1 < 0, \forall m \in \mathbb{R}$.
  2. `[ANALYZE_AT_M]` (40%): Thay $m = 2$, ta có $y' = \frac{-5}{(x - 1)^2}$, tiệm cận đứng $x = 1$, tiệm cận ngang $y = 1$.
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Xét dấu tử số $-1 - m^2 \le 0$ thay vì khẳng định chặt $-1 - m^2 < 0$ (hàm phân thức không suy biến thành hàm hằng với mọi $m$).

### Bài toán `GDPT2018-G12-007` (radical_equation - Mức độ: `comprehension`)
- **Đề bài:** Giải phương trình vô tỉ $\sqrt{2x + 3} = x$ trên tập số thực $\mathbb{R}$.
- **Mục tiêu sư phạm:** Thực hiện đúng phép biến đổi tương đương $\sqrt{A} = B \iff \{B \ge 0, A = B^2\}$ để loại bỏ nghiệm ngoại lai $x = -1$.
- **Thời gian tính toán:** `88.223 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định của phương trình:** `Interval(-3/2, oo)`
- **Điều kiện khử nghiệm ngoại lai:** $x \ge 0$
- **Nghiệm chính thức (Official Roots):** `['3']` (Chuẩn: `['3']`)
- **Nghiệm ngoại lai đã loại bỏ (Extraneous Roots Rejected):** `['-1']` (Chuẩn: `['-1']`)
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[SET_CONDITION]` (30%): Đặt điều kiện có nghĩa và điều kiện vế phải không âm: $x \ge 0$.
  2. `[SQUARE_BOTH_SIDES]` (40%): Bình phương hai vế được $2x + 3 = x^2 \iff x^2 - 2x - 3 = 0 \iff x = 3$ hoặc $x = -1$.
  3. `[FILTER_EXTRANEOUS]` (30%): Đối chiếu điều kiện $x \ge 0$: nhận $x = 3$, loại nghiệm ngoại lai $x = -1$.
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Chỉ đặt điều kiện trong căn $2x + 3 \ge 0 \iff x \ge -3/2$ rồi nhận luôn nghiệm $x = -1$ mà không thử lại.

### Bài toán `GDPT2018-G12-008` (radical_equation - Mức độ: `application`)
- **Đề bài:** Giải phương trình chứa căn thức $\sqrt{x + 2} = x - 4$.
- **Mục tiêu sư phạm:** Kiểm tra khả năng phát hiện nghiệm ngoại lai dương ($x = 2$) thỏa mãn điều kiện căn thức có nghĩa ($x \ge -2$) nhưng vi phạm điều kiện vế phải không âm ($x \ge 4$).
- **Thời gian tính toán:** `104.005 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định của phương trình:** `Interval(-2, oo)`
- **Điều kiện khử nghiệm ngoại lai:** $x - 4 \ge 0 \iff x \ge 4$
- **Nghiệm chính thức (Official Roots):** `['7']` (Chuẩn: `['7']`)
- **Nghiệm ngoại lai đã loại bỏ (Extraneous Roots Rejected):** `['2']` (Chuẩn: `['2']`)
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[SET_CONDITION]` (30%): Điều kiện tương đương khi bình phương: $x - 4 \ge 0 \iff x \ge 4$.
  2. `[SQUARE_BOTH_SIDES]` (40%): Bình phương hai vế: $x + 2 = (x - 4)^2 \iff x^2 - 9x + 14 = 0 \iff x = 7$ hoặc $x = 2$.
  3. `[FILTER_EXTRANEOUS]` (30%): Đối chiếu điều kiện $x \ge 4$: nhận $x = 7$, loại nghiệm ngoại lai $x = 2$.
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Thấy $x = 2 > 0$ và $2 + 2 = 4 > 0$ nên chủ quan không thế lại vào vế phải $x - 4 = -2 < 0$.

### Bài toán `GDPT2018-G12-009` (radical_equation - Mức độ: `application`)
- **Đề bài:** Giải phương trình vô tỉ $\sqrt{x^2 - 3x + 4} = 1 - x$.
- **Mục tiêu sư phạm:** Đánh giá trường hợp phương trình vô nghiệm hoàn toàn do nghiệm duy nhất sinh ra khi bình phương ($x = 3$) là nghiệm ngoại lai.
- **Thời gian tính toán:** `103.733 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định của phương trình:** `Reals`
- **Điều kiện khử nghiệm ngoại lai:** $1 - x \ge 0 \iff x \le 1$
- **Nghiệm chính thức (Official Roots):** `[]` (Chuẩn: `[]`)
- **Nghiệm ngoại lai đã loại bỏ (Extraneous Roots Rejected):** `['3']` (Chuẩn: `['3']`)
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[SET_CONDITION]` (35%): Biểu thức trong căn $x^2 - 3x + 4 = (x - \frac{3}{2})^2 + \frac{7}{4} > 0, \forall x \in \mathbb{R}$. Điều kiện vế phải: $1 - x \ge 0 \iff x \le 1$.
  2. `[SQUARE_BOTH_SIDES]` (35%): Bình phương hai vế: $x^2 - 3x + 4 = 1 - 2x + x^2 \iff -x + 3 = 0 \iff x = 3$.
  3. `[FILTER_EXTRANEOUS]` (30%): Vì $x = 3$ không thỏa mãn $x \le 1$, loại $x = 3$ và kết luận phương trình vô nghiệm ($S = \varnothing$).
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Rút gọn $x^2$ hai vế ra phương trình bậc nhất $x = 3$ nên quên mất đây là phương trình hệ quả và không thử lại nghiệm.

### Bài toán `GDPT2018-G12-010` (abs_equation - Mức độ: `comprehension`)
- **Đề bài:** Giải phương trình chứa dấu giá trị tuyệt đối $|x - 1| = 2x - 5$.
- **Mục tiêu sư phạm:** Phá dấu giá trị tuyệt đối $|A| = B \iff \{B \ge 0, A = \pm B\}$ và loại bỏ nghiệm ngoại lai $x = 2$ sinh ra từ nhánh $A = -B$.
- **Thời gian tính toán:** `64.242 ms` | **Điểm Rubric:** `10.0/10.0`
- **Tập xác định của phương trình:** `Reals`
- **Điều kiện khử nghiệm ngoại lai:** $2x - 5 \ge 0 \iff x \ge \frac{5}{2}$
- **Nghiệm chính thức (Official Roots):** `['4']` (Chuẩn: `['4']`)
- **Nghiệm ngoại lai đã loại bỏ (Extraneous Roots Rejected):** `['2']` (Chuẩn: `['2']`)
- **Các bước giải chuẩn SGK (Pedagogical Rubric Steps):**
  1. `[SET_CONDITION]` (30%): Điều kiện vế phải không âm: $2x - 5 \ge 0 \iff x \ge \frac{5}{2}$.
  2. `[SPLIT_BRANCHES]` (40%): Chia 2 trường hợp: $x - 1 = 2x - 5 \iff x = 4$ hoặc $x - 1 = -(2x - 5) \iff 3x = 6 \iff x = 2$.
  3. `[FILTER_EXTRANEOUS]` (30%): Đối chiếu điều kiện $x \ge 2.5$: nhận $x = 4$, loại nghiệm ngoại lai $x = 2$.
- **Sai lầm thường gặp của học sinh được hệ thống ngăn chặn:**
  - *Lưu ý:* Chia 2 trường hợp $A = B$ và $A = -B$ nhưng quên đặt điều kiện $B \ge 0$ dẫn đến nhận nhầm nghiệm ngoại lai $x = 2$.
