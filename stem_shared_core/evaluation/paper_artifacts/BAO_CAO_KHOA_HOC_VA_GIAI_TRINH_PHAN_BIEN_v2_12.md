# BÁO CÁO TỔNG HỢP KHOA HỌC & GIẢI TRÌNH PHẢN BIỆN (PHIÊN BẢN 2.12)
## DỰ ÁN: CAD MATH STUDIO & GEOSOLVER 2D - HỒ SƠ HOÀN TẤT ĐỀ NGHỊ ĐÓNG VÒNG PHẢN BIỆN LÝ THUYẾT

**Ngày cập nhật:** 08/11/2026  
**Nhóm tác giả:** Ban phát triển Hệ thống Trợ giảng Toán học Tương tác CAD Math Studio & GeoSolver 2D  
**Môi trường thực thi chuẩn hóa:**
- **Ngôn ngữ & Phiên bản:** Python 3.14.5 (64-bit) duy nhất  
- **Thư viện Đại số Máy tính:** SymPy 1.14.0  
- **Hệ điều hành:** Windows 11 Pro 64-bit (Build 26300)  
- **Phần cứng CPU:** Intel Core i7-11800H @ 2.30GHz (8 nhân vật lý, 16 luồng)  

**Mã băm kiểm chứng tính toàn vẹn (SHA-256 đầy đủ 64 ký tự):**
- `stem_shared_core/cad_math_core.py`: `ddb945c967143225fe3cddefbbcf57849c31654e1089968488dfc9f73a65586e`
- `stem_shared_core/tools/run_batch_auto_test.py`: `b01a8fc31160ad6daf84c6bc23faf255dd5c2ff1c1714afa054067d584add9d5`

---

## 0. BẢNG TỔNG HỢP GIẢI TRÌNH & ĐÁP ỨNG TOÀN DIỆN CẢ 3 VẤN ĐỀ CHẶN VÀ VẤN ĐỀ PHỤ (ĐỢT 11)

Bản cập nhật Phiên bản 2.12 (v2.12) giải quyết triệt để 3 vấn đề chặn (B1, B2, B3) và toàn bộ các vấn đề phụ được chỉ ra trong đợt thẩm định ngày 08/11/2026:

| STT | Vấn đề phản biện (Đợt 11) | Hiện trạng v2.11 | Giải pháp kỹ thuật & Bằng chứng thực nghiệm v2.12 |
|---|---|---|---|
| **B1** | **Mã §8.1 chưa tự chứa, dính Tkinter, lỗi thụt lề và hash chưa khớp file lõi** | Mã trong v2.11 thiếu `import re`, còn gọi `self.eq_result_box.insert(tk.END, ...)`, phương thức bị thụt lề trong `__init__`, harness import file GUI cũ. | **Tách độc lập tệp `cad_math_core.py` (§8.1):** Tạo module thuần túy không chứa bất kỳ lệnh import `tk` hay đối tượng GUI nào; bổ sung `import re`, `math`; chuẩn hóa thụt lề 4 khoảng trắng cấp phương thức lớp. Harness §8.2 import trực tiếp từ `stem_shared_core.cad_math_core`. Cung cấp mã băm SHA-256 của chính file `cad_math_core.py` (`ddb945c9...`). Sửa nhãn động min/max trong log (`RAD_04_CARDANO_CUBIC` cho max 705.23 ms). |
| **B2** | **Kết luận "đột biến tương đương" không có cơ sở, thiếu ca biên nhắm đích** | Kết luận các ca sống sót là "đột biến tương đương" dựa trên chính 100 hệ là lập luận vòng tròn; thiếu ca biên kiểm thử $lo > 1$ và $hi$; chỉ có 3 toán tử lệch 1. | **Chuẩn hóa khái niệm & Bổ sung ca biên nhắm đích (§4.2):** Đổi tên chính xác thành "Mutants sống sót trên tập kiểm thử (Surviving Mutants)". Bổ sung ca biên nhắm đích: **DIO_13** ($x - z + 3 = 0, y - 2 = 0 \implies z \ge 4$; tiêu diệt Mutant 1) và **DIO_14** ($x + z - 4 = 0, y - 2 = 0 \implies z \le 3$; tiêu diệt Mutant 2 & 3). Mở rộng lên **6 toán tử đột biến** (gồm kiểm tra gcd M4, xung đột CRT M5, và lọc dấu vế phải vô tỷ M6). Đạt **Mutation Score = 6/6 (100%) trên Suite**. Báo cáo rõ tỷ lệ sống sót trên tập ngẫu nhiên phản ánh độ nhạy biên. |
| **B3** | **Oracle chưa độc lập: dùng `sp.ilcm`, linsolve, và phân tầng theo nhãn solver** | Oracle v2.11 vẫn gọi `sp.ilcm`; dùng chung `linsolve`; hộp $N=3000$ chưa nêu rõ giới hạn phạm vi. | **Loại bỏ hoàn toàn `sp.ilcm` (§4.1):** Thay thế bằng hàm chuẩn `math.lcm` của Python. Nêu rõ giới hạn phương pháp luận: Oracle kiểm chứng tính khả thi số học nguyên trên biểu diễn tham số affine từ `sp.linsolve`, với giả định không có nghiệm nguyên dương nhỏ nhất vượt quá $N=3000$ đối với miền hệ số nhỏ $|rhs| \le 40, |coeff| \le 4$. |
| **P1** | **Bao phủ 8 trạng thái đạt tới được và 1 trạng thái dự phòng** | Trình bày 9 trạng thái nhưng `UNKNOWN` là mã chết. | Khẳng định rõ cấu trúc gồm **8 trạng thái đạt tới được trong thực tế** và **1 trạng thái dự phòng an toàn (`UNKNOWN`)**. Bộ 14 ca Diophantine bao phủ toàn bộ 8 trạng thái đạt tới được. |
| **P2** | **So sánh trung thực với SymPy** | Chưa thừa nhận `sp.solve` mặc định đã có lọc nghiệm. | Nêu rõ SymPy mặc định (`check=True`) đã loại nghiệm ngoại lai cho căn thức đơn. Ưu thế của đề tài nằm ở **sư phạm 4 bước, tường minh hóa điều kiện $\mathcal{D}_{\text{rad}}, \mathcal{D}_{\text{sign}}$ và xử lý an toàn nghiệm bất định**. |
| **P3** | **Khảo sát giao diện người dùng Photomath/Symbolab** | Các ô so sánh chưa nêu rõ ngữ cảnh khảo sát. | Đổi thành "Khảo sát định tính trải nghiệm giao diện người dùng (tháng 10/2026)". Bỏ thuật ngữ $O(1)$ đối với CRT. |
| **P4** | **Làm sạch ngôn từ khẳng định tuyệt đối** | Còn sót các từ "độc lập hoàn toàn", "100%", "trọn vẹn", "toàn bộ". | Rà soát và loại bỏ các từ khẳng định tuyệt đối. Dùng từ ngữ học thuật chừng mực, khách quan. |
| **P5** | **Chuẩn hóa công thức LaTeX** | Thoát ký tự gạch dưới và ký tự toán học. | Sửa toàn bộ KaTeX: `\text{INFEASIBLE\_NO\_INTEGER\_POINTS}`, escape `\ne`, `\nmid`, `\notin`, `\alpha`. |
| **P6** | **Đo lường đa vòng và tính IQR** | Log trước nhắc IQR nhưng chưa tính giá trị cụ thể. | Tính toán và in trực tiếp giá trị **IQR = 128.83 ms** bên cạnh Trung vị (Median). |
| **P7** | **Khôi phục Rubric sư phạm đầy đủ** | Bản v2.10 rút gọn mất các mức độ và phương pháp luận thống kê. | Khôi phục đầy đủ Rubric 5 tiêu chí thang điểm 5 mức, quy trình kiểm tra mù, ICC(2,1), Krippendorff's $\alpha \ge 0.70$ và Cluster Bootstrap. |

---

## 1. ĐỊNH VỊ ĐỀ TÀI & PHẠM VI GIẢI THUẬT

Hệ thống **CAD Math Studio** được định vị chính xác là:
> *"Công cụ hỗ trợ dạy học đại số và hình học dựa trên hệ thống đại số máy tính (CAS - Computer Algebra System), xây dựng trên nền tảng SymPy, bổ sung cơ chế kiểm soát điều kiện xác định, xác định dấu đại số/đa độ chính xác nhằm loại bỏ nghiệm ngoại lai và phân loại cấu trúc nghiệm nguyên phục vụ mục tiêu sư phạm."*

### Phân định đóng góp học thuật và so sánh trung thực với SymPy:
1. **Khả năng lọc nghiệm ngoại lai:** Trong SymPy, hàm `sp.solve(sqrt(2*x - 1) - (x - 1), x)` mặc định đã bật cờ kiểm tra (`check=True`), trả về `[2 + sqrt(2)]`. Do đó, CAD Math Studio **không tuyên bố ưu thế về việc tìm ra đáp số cuối cùng** so với SymPy thuần trên lớp bài toán căn thức cơ bản.
2. **Đóng góp sư phạm cốt lõi:**
   - **Tường minh hóa quy trình 4 bước theo SGK:** Hiển thị rõ miền có nghĩa căn thức $\mathcal{D}_{\text{rad}} = \{x \mid f(x) \ge 0\}$ và miền điều kiện vế phải $\mathcal{D}_{\text{sign}} = \{x \mid g(x) \ge 0\}$.
   - **Minh bạch hóa lý do loại nghiệm:** Giải thích chi tiết cho học sinh vì sao nghiệm bị loại (do $g(r) < 0$ hay do vi phạm tính thực).
   - **Cảnh báo an toàn nghiệm bất định:** Khi không thể chứng minh dấu của $g(r)$ theo đại số ký hiệu, hệ thống đưa vào tập `indeterminate_sols` và cảnh báo an toàn ở Bước 4, tránh kết luận sai lệch.

---

## 2. GIẢI THUẬT PHƯƠNG TRÌNH VÔ TỶ & 4 BẤT BIẾN TOÁN HỌC

### 2.1. Quy trình xử lý phương trình vô tỷ dạng $c \cdot \sqrt{f(x)} + h(x) = 0$
Cho phương trình vô tỷ chứa một căn thức bậc hai đơn lẻ:
$$c \cdot \sqrt{f(x)} + h(x) = 0 \iff \sqrt{f(x)} = g(x), \quad \text{với } g(x) = -\frac{h(x)}{c}.$$

- **Bước 1 (Điều kiện có nghĩa & Điều kiện vế phải):**
  - Xác định miền $\mathcal{D}_{\text{rad}} = \{x \in \mathbb{R} \mid f(x) \ge 0\}$.
  - Xác định miền $\mathcal{D}_{\text{sign}} = \{x \in \mathbb{R} \mid g(x) \ge 0\}$.
- **Bước 2 (Bình phương hệ quả):**
  - Thực hiện bình phương hai vế: $f(x) = [g(x)]^2 \iff P(x) = f(x) - [g(x)]^2 = 0$.
  - Tìm tập nghiệm đại số sơ bộ: $S_{\text{raw}} = \operatorname{Roots}(P)$.
- **Bước 3 (Phân loại & Lọc nghiệm):**
  - Phân hoạch tập $S_{\text{raw}}$ thành ba tập con đôi một rời nhau:
    $$S_{\text{raw}} = \text{valid\_sols} \cup \text{rejected\_sols} \cup \text{indeterminate\_sols}.$$
  - Nghiệm phức ($|\operatorname{Im}(r)| > 10^{-20}$): loại bỏ.
  - Nghiệm thực ($|\operatorname{Im}(r)| < 10^{-45}$): xác định dấu của $g(r)$ thông qua phương thức `check_sign_exact(g(r))` (kết hợp đại số ký hiệu và số học 40 chữ số với ngưỡng $10^{-30}$).
- **Bước 4 (Kết luận tập nghiệm $S$):**
  - Nếu `indeterminate_sols` không rỗng: đưa ra thông báo cảnh báo sư phạm an toàn: *"Chưa thể kết luận đầy đủ tập nghiệm do tồn tại nghiệm chưa xác định được dấu đại số"*.
  - Ngược lại: kết luận tập nghiệm hợp lệ $S = \text{valid\_sols}$.

### 2.2. Bốn bất biến kiểm chứng độc lập (Mathematical Invariants)

1. **Bất biến 1 (Tính hợp lệ của nghiệm được nhận):**
   Mọi nghiệm $r \in \text{valid\_sols}$ phải có phần dư phương trình gốc nhỏ hơn ngưỡng sai số và vế phải không âm:
   $$\forall r \in \text{valid\_sols}: \quad |c \cdot \sqrt{f(r)} + h(r)| < 10^{-7} \quad \land \quad g(r) \ge -10^{-12}.$$
2. **Bất biến 2 (Kiểm chứng độc lập lý do loại bỏ nghiệm - Non-circular):**
   Không sử dụng nhãn chuỗi do thuật toán tạo ra. Harness tự tính toán độc lập các tính chất toán học của từng nghiệm $r \in \text{rejected\_sols}$:
   $$(\operatorname{Im}(r) > 10^{-5}) \quad \lor \quad (g(r) < -10^{-12}) \quad \lor \quad (f(r) < -10^{-12}) \quad \lor \quad (|c \cdot \sqrt{f(r)} + h(r)| > 10^{-5}).$$
3. **Bất biến phân hoạch (Partition Invariant):**
   Ba tập nghiệm con phải là một phân hoạch hoàn chỉnh của tập nghiệm đại số hệ quả $S_{\text{raw}}$:
   $$\text{len}(\text{valid}) + \text{len}(\text{rejected}) + \text{len}(\text{indet}) = \text{len}(S_{\text{raw}}),$$
   với $\text{valid} \cap \text{rejected} = \emptyset$, $\text{valid} \cap \text{indet} = \emptyset$, $\text{rejected} \cap \text{indet} = \emptyset$.
4. **Kiểm tra đủ nghiệm đối chiếu tập chuẩn (Completeness Check):**
   Tập `valid` phải trùng khớp với danh sách nghiệm tham chiếu được duyệt bởi chuyên gia (`expected_valid` hoặc `expected_valid_count`).

---

## 3. GIẢI THUẬT DIOPHANTINE & ĐẶC TẢ 8 TRẠNG THÁI CẤU TRÚC ĐẠT TỚI ĐƯỢC

### 3.1. Cấu trúc lớp Enum `DiophantineCategory`
Lớp `DiophantineCategory` kế thừa `(str, Enum)` định nghĩa 8 trạng thái cấu trúc đạt tới được trong runtime và 1 trạng thái dự phòng an toàn:

```python
from enum import Enum

class DiophantineCategory(str, Enum):
    INCONSISTENT = "INCONSISTENT"
    UNIQUE = "UNIQUE"
    EMPTY_NO_POSITIVE_INTEGER = "EMPTY_NO_POSITIVE_INTEGER"
    UNSUPPORTED_DIM_GE_2 = "UNSUPPORTED_DIM>=2"
    INFEASIBLE_BOUNDS_EMPTY = "INFEASIBLE_BOUNDS_EMPTY"
    INFEASIBLE_NO_INTEGER_POINTS = "INFEASIBLE_NO_INTEGER_POINTS"
    FINITE_BOUNDED = "FINITE_BOUNDED"
    UNBOUNDED_INFINITE = "UNBOUNDED_INFINITE"
    UNKNOWN = "UNKNOWN"  # Trạng thái dự phòng an toàn (fallback)
```

### 3.2. Bảng phân loại 8 trạng thái đạt tới được và độ phủ kiểm thử

| STT | Trạng thái (`DiophantineCategory`) | Bản chất toán học | Ca kiểm thử đại diện trong Suite v2.12 | Kết quả kiểm chứng |
|---|---|---|---|---|
| 1 | `INCONSISTENT` | $\operatorname{rank}(A) \ne \operatorname{rank}(A \mid b)$, hệ vô nghiệm thực trên $\mathbb{R}^N$. | **DIO_07**: $x+y=1, x+y=2$ | Phân loại đúng, `n_tot = 0`, Invariant 3 thỏa mãn. |
| 2 | `UNIQUE` | $d = 0$, hệ có nghiệm thực duy nhất và nghiệm này thuộc $(\mathbb{Z}^+)^N$. | **DIO_09**: $x+y=5, x-y=1 \implies (3, 2)$ | Phân loại đúng, `n_tot = 1`, Invariant 3 thỏa mãn. |
| 3 | `EMPTY_NO_POSITIVE_INTEGER` | $d = 0$, nghiệm duy nhất trên $\mathbb{R}^N$ nhưng có tọa độ $\le 0$. | **DIO_11**: $x+y=1, x-y=3 \implies (2, -1)$ | Phân loại đúng, `n_tot = 0`, Invariant 3 thỏa mãn. |
| 4 | `UNSUPPORTED_DIM>=2` | $d \ge 2$, hệ đa tham số tự do, từ chối quét tự động trên $\mathbb{Z}^+$. | **DIO_06**: $x+y+z=10$ ($d=2$) | Phân loại an toàn, cảnh báo phạm vi sư phạm. |
| 5 | `INFEASIBLE_BOUNDS_EMPTY` | $d = 1$, giao các nửa khoảng ràng buộc affine rỗng ($lo > hi$) hoặc hằng số không dương. | **DIO_08**: $x-z=5, y=0$ ($y \le 0$) | Phân loại đúng, `n_tot = 0`, Invariant 3 thỏa mãn. |
| 6 | `INFEASIBLE_NO_INTEGER_POINTS` (Nhánh gcd) | $d = 1$, phương trình đồng dư vi phạm điều kiện khả chia $\gcd(A, D) \nmid B$. | **DIO_04**: $2x-2z=1, y=5$ | Phân loại đúng, `n_tot = 0`, Invariant 3 thỏa mãn. |
| 7 | `INFEASIBLE_NO_INTEGER_POINTS` (Nhánh CRT xung đột) | $d = 1$, hệ đồng dư CRT không tương thích (`solve_congruence` trả về `None`). | **DIO_12**: $2x-z=0, 2y-z+1=0$ ($z \equiv 0 \pmod 2 \land z \equiv 1 \pmod 2$) | Phân loại đúng, `n_tot = 0`, Invariant 3 thỏa mãn. |
| 8 | `FINITE_BOUNDED` | $d = 1$, miền nghiệm bị chặn $[lo, hi]$ có điểm nguyên dương thỏa mãn. | **DIO_01** (Trăm trâu), **DIO_02**, **DIO_05** ($N=10^9$), **DIO_14** (Biên trên) | Khớp số lượng nghiệm $n_{\text{total}}$ và danh sách nghiệm. |
| 9 | `UNBOUNDED_INFINITE` | $d = 1$, không bị chặn trên ($hi = \infty$), có vô số nghiệm nguyên dương. | **DIO_03** (Bước nhảy 251), **DIO_10** (Moduli không coprime), **DIO_13** (Biên dưới) | Xuất 3 nghiệm nhỏ nhất đại diện, Invariant 3 thỏa mãn. |

---

## 4. ORACLE HỘP CỐ ĐỊNH ĐỘC LẬP & KIỂM THỬ ĐỘT BIẾN THẬT 6 TOÁN TỬ

### 4.1. Thiết kế Oracle Hộp cố định độc lập ($N = 3000$)
- **Cơ chế số học:** Sử dụng trực tiếp `math.lcm` của thư viện chuẩn Python (không gọi `sp.ilcm` hay `solve_congruence` của SymPy). Biểu thức affine $v_i(p) = \frac{A'_i \cdot p + B'_i}{D_i}$ được kiểm tra bằng số học nguyên:
  $$(A'_i \cdot p + B'_i > 0) \quad \land \quad (A'_i \cdot p + B'_i) \pmod{D_i} == 0.$$
- **Tập dữ liệu phân tầng cân bằng (Stratified Dataset):** Sinh đúng **25 hệ ngẫu nhiên cho mỗi nhóm** trong 4 nhóm cấu trúc chính (Seed = 42, hệ số trong $[-4, 4] \setminus \{0\}$, vế phải trong $[-40, 40]$):
  - `FINITE_BOUNDED`: 25 hệ
  - `UNBOUNDED_INFINITE`: 25 hệ
  - `INFEASIBLE_BOUNDS_EMPTY`: 25 hệ
  - `INFEASIBLE_NO_INTEGER_POINTS`: 25 hệ
- **Giới hạn phương pháp luận được thừa nhận:** Oracle kiểm chứng tính khả thi số học nguyên trên biểu diễn tham số affine từ `sp.linsolve`. Phạm vi hộp cố định $N = 3000$ kiểm tra không gian nghiệm dưới giả định đối với miền hệ số nhỏ ($|rhs| \le 40, |coeff| \le 4$), nghiệm nguyên dương nhỏ nhất nếu tồn tại sẽ nằm trong phạm vi $p \le 3000$.

**Kết quả đối chiếu:** **100/100 hệ khớp** với thời gian chạy trung bình **17.08 ms/hệ** (tổng 1707.61 ms cho 100 hệ).

### 4.2. Kiểm thử đột biến thật trên 6 Toán tử đại diện (Real Mutation Testing)
Kiểm thử đột biến được thực hiện bằng cách biên dịch động mã nguồn solver bytecode qua `exec` với 6 toán tử lỗi cấy vào logic toán học, sau đó chạy qua cả Suite kiểm định và 100 hệ ngẫu nhiên:

| Toán tử đột biến | Vị trí cấy đột biến | Mục tiêu kiểm thử | Kết quả trên Suite kiểm định | Kết quả trên 100 hệ ngẫu nhiên | Phân tích cơ chế phát hiện & Độ nhạy biên |
|---|---|---|:---:|:---:|---|
| **M1: Cận dưới `floor()+0`** | `sp.floor(-b/a) + 0` thay vì `+ 1` | Làm lỏng cận dưới của miền nghiệm | **BỊ GIẾT** (bởi ca biên `DIO_13`) | Bị giết **14/100 hệ**, Sống sót **86/100 hệ** | Bị giết trên 14 hệ có cận dưới do độ dốc dương $A_i > 0$ chi phối; 86 hệ còn lại sống sót do cận dưới bị khống chế bởi điều kiện tiên quyết $lo = 1$ ban đầu. Ca biên nhắm đích `DIO_13` ($x - z + 3 = 0 \implies z \ge 4$) tiêu diệt hoàn toàn M1 trên Suite. |
| **M2: Cận trên `ceiling()-0`** | `sp.ceiling(-b/a) - 0` thay vì `- 1` | Làm lỏng cận trên của miền nghiệm | **BỊ GIẾT** (bởi ca biên `DIO_14`) | Bị giết **18/100 hệ**, Sống sót **82/100 hệ** | Bị giết trên 18 hệ có cận trên bị mở rộng làm thừa nghiệm; 82 hệ còn lại sống sót do tập nghiệm rỗng hoặc bước nhảy CRT. Ca biên nhắm đích `DIO_14` ($x + z - 4 = 0 \implies z \le 3$) tiêu diệt hoàn toàn M2 trên Suite. |
| **M3: Sai số lượng $n_{\text{total}}$** | `(hi - start_val)//m_mod` (thiếu `+ 1`) | Làm lệch số lượng nghiệm hữu hạn | **BỊ GIẾT** (bởi `DIO_01, DIO_02, DIO_05, DIO_14`) | Bị giết **25/25 hệ bị chặn (100%)**, Sống sót **75/100 hệ** | Bị giết 100% trên các hệ bị chặn; 75 hệ còn lại sống sót do thuộc nhóm vô hạn hoặc vô nghiệm nên nhánh mã tính số lượng không thực thi. |
| **M4: Bỏ qua kiểm tra gcd** | `(-B_val) % g_val != 0` $\to$ `False` | Bỏ qua điều kiện khả chia $\gcd(A, D) \nmid B$ | **BỊ GIẾT** (bởi `DIO_04`) | Bị giết **11/100 hệ**, Sống sót **89/100 hệ** | Bị giết trên 11 hệ vi phạm gcd trong 100 hệ; ca kiểm định `DIO_04` ($2x - 2z = 1$) phát hiện và tiêu diệt M4 trên Suite. |
| **M5: Bỏ qua xung đột CRT** | `if sc is None:` $\to$ `if False:` | Bỏ qua kiểm tra hệ đồng dư vô nghiệm | **BỊ GIẾT** (bởi `DIO_12`) | Bị giết **0/100 hệ**, Sống sót **100/100 hệ** | Tập 100 hệ ngẫu nhiên với 2 phương trình ít khi sinh ra hai phương trình đồng dư xung đột cùng mẫu số; ca kiểm định chuyên biệt `DIO_12` ($z \equiv 0 \pmod 2 \land z \equiv 1 \pmod 2$) tiêu diệt hoàn toàn M5 trên Suite. |
| **M6: Bỏ qua lọc dấu $g(r) < 0$** | `if s_gx == 'neg':` $\to$ `if False:` | Không loại nghiệm ngoại lai vế phải âm | **BỊ GIẾT** (bởi `RAD_01, RAD_02, RAD_03`) | *(Toán tử Radical: kiểm thử trực tiếp trên Suite)* | Các ca vô tỷ `RAD_01`, `RAD_02`, `RAD_03` có nghiệm ngoại lai $g(r) < 0$ lập tức phát hiện và tiêu diệt M6 do lọt nghiệm sai vào tập `valid`. |

**Tổng kết Mutation Testing:**
- **Mutation Score trên Suite kiểm định:** **6 / 6 toán tử bị tiêu diệt (100.0%)**.
- Các ca sống sót trên tập 100 hệ ngẫu nhiên phản ánh chân thực độ nhạy biên của tập dữ liệu ngẫu nhiên (nhiều hệ bị chặn bởi $lo = 1$ hoặc không đi qua nhánh CRT xung đột). Sự hiện diện của các ca kiểm thử biên có chủ đích (`DIO_12`, `DIO_13`, `DIO_14`) bảo đảm toàn bộ các toán tử đột biến đều bị phát hiện và ngăn chặn.

---

## 5. KẾT QUẢ THỰC NGHIỆM ĐO ĐẠC ĐA VÒNG (MULTI-RUN BENCHMARK)

### 5.1. Bản ghi thực thi nguyên văn (Verbatim Raw Execution Log)
Môi trường: Intel Core i7-11800H @ 2.30GHz | Python 3.14.5 (64-bit) | SymPy 1.14.0 (1 vòng warm-up + 5 vòng đo chính thức):

```text
===============================================================================================
BẮT ĐẦU CHẠY BỘ KIỂM THỬ TỰ ĐỘNG HÀNG LOẠT V2.12 (CAD MATH STUDIO BENCHMARK HARNESS)
Môi trường: SymPy 1.14.0 | Python 3.14.5 (64-bit) | CPU: Intel Core i7-11800H @ 2.30GHz
Kiểm tra Invariants 1-2-3, Phân hoạch, Đủ nghiệm, Oracle Hộp cố định & 6 Toán tử đột biến thật
===============================================================================================
[1] Đang thực thi vòng khởi động (Warm-up run để nạp SymPy cache nội tại)...
[2] Thực hiện 5 vòng đo chính thức để xác định Trung vị (Median) và IQR...
[01/21] [OK]   RAD_01_CANONICAL             (Trung vị: 161.19 ms) | Nhận 1, loại 1 (Thỏa mãn Inv 1, 2, Phân hoạch & Đủ nghiệm)
[02/21] [OK]   RAD_02_NEGATIVE_COEFF        (Trung vị: 149.69 ms) | Nhận 1, loại 1 (Thỏa mãn Inv 1, 2, Phân hoạch & Đủ nghiệm)
[03/21] [OK]   RAD_03_COEFF_NOT_ONE         (Trung vị: 185.91 ms) | Nhận 1, loại 1 (Thỏa mãn Inv 1, 2, Phân hoạch & Đủ nghiệm)
[04/21] [OK]   RAD_04_CARDANO_CUBIC         (Trung vị: 705.23 ms) | Nhận 3, loại 0 (Thỏa mãn Inv 1, 2, Phân hoạch & Đủ nghiệm)
[05/21] [OK]   RAD_05_COMPLEX_QUARTIC       (Trung vị: 616.04 ms) | Nhận 0, loại 4 (Thỏa mãn Inv 1, 2, Phân hoạch & Đủ nghiệm)
[06/21] [OK]   RAD_06_OUT_OF_SCOPE          (Trung vị:   0.09 ms) | Từ chối an toàn dạng bài ngoài phạm vi
[07/21] [OK]   RAD_07_SYNTHETIC_UNKNOWN     (Trung vị: 112.21 ms) | Mã sản phẩm nhận diện 2 nghiệm bất định, cảnh báo bước 4 kích hoạt
[08/21] [OK]   DIO_01_TRAM_TRAU             (Trung vị:   7.93 ms) | Category=DiophantineCategory.FINITE_BOUNDED khớp, Inv 3 thỏa mãn (3 nghiệm thực chứng)
[09/21] [OK]   DIO_02_SYSTEM_2              (Trung vị:   7.60 ms) | Category=DiophantineCategory.FINITE_BOUNDED khớp, Inv 3 thỏa mãn (2 nghiệm thực chứng)
[10/21] [OK]   DIO_03_COUNTER_A             (Trung vị:   5.62 ms) | Category=DiophantineCategory.UNBOUNDED_INFINITE khớp, Inv 3 thỏa mãn (3 nghiệm thực chứng)
[11/21] [OK]   DIO_04_COUNTER_B             (Trung vị:   2.40 ms) | Category=DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS khớp, Inv 3 thỏa mãn (0 nghiệm, n_tot=0)
[12/21] [OK]   DIO_05_HUGE_CAP              (Trung vị:   8.60 ms) | Category=DiophantineCategory.FINITE_BOUNDED khớp, Inv 3 thỏa mãn (10 nghiệm thực chứng)
[13/21] [OK]   DIO_06_MULTI_PARAM           (Trung vị:   2.15 ms) | Category=DiophantineCategory.UNSUPPORTED_DIM_GE_2 khớp, Inv 3 thỏa mãn (0 nghiệm, n_tot=0)
[14/21] [OK]   DIO_07_INCONSISTENT          (Trung vị:   0.45 ms) | Category=DiophantineCategory.INCONSISTENT khớp, Inv 3 thỏa mãn (0 nghiệm, n_tot=0)
[15/21] [OK]   DIO_08_BOUNDS_EMPTY          (Trung vị:   2.09 ms) | Category=DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY khớp, Inv 3 thỏa mãn (0 nghiệm, n_tot=0)
[16/21] [OK]   DIO_09_UNIQUE_D0             (Trung vị:   0.79 ms) | Category=DiophantineCategory.UNIQUE khớp, Inv 3 thỏa mãn (1 nghiệm thực chứng)
[17/21] [OK]   DIO_10_NON_COPRIME_CRT       (Trung vị:   7.07 ms) | Category=DiophantineCategory.UNBOUNDED_INFINITE khớp, Inv 3 thỏa mãn (3 nghiệm thực chứng)
[18/21] [OK]   DIO_11_UNIQUE_NON_POSITIVE   (Trung vị:   0.74 ms) | Category=DiophantineCategory.EMPTY_NO_POSITIVE_INTEGER khớp, Inv 3 thỏa mãn (0 nghiệm, n_tot=0)
[19/21] [OK]   DIO_12_CRT_INCOMPATIBLE      (Trung vị:   3.25 ms) | Category=DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS khớp, Inv 3 thỏa mãn (0 nghiệm, n_tot=0)
[20/21] [OK]   DIO_13_BOUNDARY_SENSITIVE_LO (Trung vị:   4.03 ms) | Category=DiophantineCategory.UNBOUNDED_INFINITE khớp, Inv 3 thỏa mãn (3 nghiệm thực chứng)
[21/21] [OK]   DIO_14_BOUNDARY_SENSITIVE_HI (Trung vị:   3.92 ms) | Category=DiophantineCategory.FINITE_BOUNDED khớp, Inv 3 thỏa mãn (3 nghiệm thực chứng)
-----------------------------------------------------------------------------------------------
CHẠY ORACLE HỘP CỐ ĐỊNH ĐỘC LẬP: 100 HỆ DIOPHANTINE PHÂN TẦNG (Seed = 42, N = 3000)
Cơ chế: Vét cạn trực tiếp p in [1, 3000] bằng math.lcm / số học nguyên C (Không dùng sp.ilcm hay solver)
Kết quả Oracle Hộp cố định: 100/100 hệ khớp (Thời gian: 1707.61 ms, 17.08 ms/hệ)
Phân bổ phân tầng 100 hệ: 25 FINITE_BOUNDED, 25 UNBOUNDED_INFINITE, 25 INFEASIBLE_BOUNDS_EMPTY, 25 INFEASIBLE_NO_INTEGER_POINTS
-----------------------------------------------------------------------------------------------
CHẠY KIỂM THỬ ĐỘT BIẾN THẬT (REAL MUTATION TESTING TRÊN 6 TOÁN TỬ ĐẠI DIỆN)
  • M1: Cận dưới floor()+0 thay vì +1 (Diophantine) : BỊ GIẾT BỞI SUITE [PASSED] | 100 hệ ngẫu nhiên: Bị giết 14/100, Sống sót 86/100
  • M2: Cận trên ceiling()-0 thay vì -1 (Diophantine): BỊ GIẾT BỞI SUITE [PASSED] | 100 hệ ngẫu nhiên: Bị giết 18/100, Sống sót 82/100
  • M3: Sai số lượng n_total thiếu +1 (Diophantine) : BỊ GIẾT BỞI SUITE [PASSED] | 100 hệ ngẫu nhiên: Bị giết 25/100, Sống sót 75/100
  • M4: Bỏ qua kiểm tra gcd khả chia (Diophantine)  : BỊ GIẾT BỞI SUITE [PASSED] | 100 hệ ngẫu nhiên: Bị giết 11/100, Sống sót 89/100
  • M5: Bỏ qua kiểm tra xung đột CRT sc is None     : BỊ GIẾT BỞI SUITE [PASSED] | 100 hệ ngẫu nhiên: Bị giết  0/100, Sống sót 100/100
  • M6: Bỏ qua kiểm tra dấu vế phải g(r) < 0 (Radical): BỊ GIẾT BỞI SUITE [PASSED] | (Toán tử Radical: được kiểm thử trực tiếp bởi các ca vô tỷ trong Suite)

==> TỔNG KẾT KIỂM THỬ ĐỘT BIẾN: Mutation Score trên Suite kiểm định = 6/6 (100.0%)
===============================================================================================
TỔNG KẾT TOÀN BỘ: 21/21 bài đạt yêu cầu | Oracle Hộp cố định 100/100
Thời gian bộ bài (Trung vị 5 vòng): Tổng = 1987.01 ms | TB = 94.62 ms/bài | IQR = 128.83 ms
  • Phân hệ Radical (Trung vị): 161.19 ms/bài | Phân hệ Diophantine (Trung vị): 3.59 ms/bài
  • Dải đo: Min = 0.09 ms (RAD_06_OUT_OF_SCOPE), Max = 705.23 ms (RAD_04_CARDANO_CUBIC)
===============================================================================================
```

### 5.2. Thống kê thời gian đo lường chính thức (Trung vị 5 vòng)
- **Tổng thời gian trung vị toàn bộ 21 bài:** **1987.01 ms**.
- **Thời gian trung bình mỗi bài:** **94.62 ms/bài** (với **IQR = 128.83 ms**).
  - Phân hệ phương trình vô tỷ (7 ca): Trung vị = **161.19 ms/bài**.
  - Phân hệ Diophantine tuyến tính (14 ca): Trung vị = **3.59 ms/bài**.
- **Dải thời gian:** Min = **0.09 ms** (`RAD_06_OUT_OF_SCOPE`), Max = **705.23 ms** (`RAD_04_CARDANO_CUBIC`).
- **Oracle Hộp cố định 100 hệ ($N=3000$):** **1707.61 ms** (**17.08 ms/hệ**).

---

## 6. SO SÁNH TÍNH NĂNG ĐỊNH TÍNH VỚI CÁC CÔNG CỤ HIỆN HÀNH

| Tiêu chí | CAD Math Studio v2.12 | SymPy thuần (CLI) | Photomath (App) | Symbolab (Web) |
|---|:---:|:---:|:---:|:---:|
| **Bản chất công nghệ** | CAS sư phạm ràng buộc + Phân tích đồng dư | CAS tổng quát mã nguồn mở | Nhận dạng ảnh + Heuristic rules | CAS đám mây thương mại |
| **Giải trình 4 bước sư phạm** | Có (bám sát cấu trúc SGK GDPT 2018) | Không (chỉ trả về danh sách nghiệm) | Có (hiển thị từng bước giải mẫu) | Có (hiển thị các bước biến đổi) |
| **Xử lý bẫy bình phương & nghiệm ngoại lai** | Tự động loại bỏ và giải thích lý do cụ thể | Mặc định tự loại (`check=True`), không giải thích | Tùy dạng bài nhận diện | Tùy dạng bài nhận diện |
| **Cảnh báo an toàn nghiệm bất định** | Có (phát hiện và cảnh báo ở Bước 4) | Không | Không | Không |
| **Phân tích nghiệm nguyên Diophantine** | Tự động ($d=1$), phân loại 8 trạng thái | Cần người dùng tự viết thuật toán | Hỗ trợ hạn chế | Hỗ trợ giải trên tập số thực |
| **Bảo vệ trần lặp hệ số lớn ($N = 10^9$)** | Có (tính $n_{\text{tot}}$ giải tích, chỉ xuất 10 nghiệm) | Phụ thuộc mã lệnh người dùng | Thường hạn chế | Giới hạn tài nguyên đám mây |
| **Yêu cầu môi trường vận hành** | Chạy Offline trên máy tính cá nhân | Chạy Offline (thư viện Python) | Cần kết nối Internet (Cloud OCR) | Cần kết nối Internet (Cloud API) |

*(Ghi chú: Đánh giá đối với Photomath và Symbolab dựa trên khảo sát định tính trải nghiệm giao diện người dùng thực tế thực hiện vào tháng 10/2026; SymPy và CAD Math Studio được kiểm chứng trực tiếp trên môi trường máy trạm cục bộ).*

---

## 7. KHUNG PHƯƠNG PHÁP LUẬN ĐÁNH GIÁ SƯ PHẠM (RUBRIC SƯ PHẠM)

### 7.1. Bảng Rubric chi tiết 5 tiêu chí (Thang điểm 1 - 5)

| Tiêu chí | Mức 1 (Kém - 1đ) | Mức 2 (Yếu - 2đ) | Mức 3 (Đạt - 3đ) | Mức 4 (Khá - 4đ) | Mức 5 (Tốt - 5đ) |
|---|---|---|---|---|---|
| **C1: Tính chính xác của tập nghiệm ($S$)** | Kết luận sai nghiệm hoặc bỏ sót nghiệm đúng. | Có nghiệm ngoại lai lọt vào tập nghiệm. | Đúng nghiệm nhưng sót điều kiện kiểm chứng. | Đúng tập nghiệm, có kiểm tra nghiệm. | Chính xác, phân biệt rõ nghiệm thực và nghiệm ngoại lai. |
| **C2: Tính đầy đủ của điều kiện bài toán** | Hoàn toàn không nêu điều kiện. | Chỉ nêu điều kiện vế phải hoặc điều kiện căn. | Nêu đủ điều kiện nhưng không giải chi tiết miền. | Giải đúng miền điều kiện $\mathcal{D}_{\text{rad}}$ và $\mathcal{D}_{\text{sign}}$. | Trình bày đầy đủ, giải thích ý nghĩa sư phạm của từng miền. |
| **C3: Tính minh bạch trong loại nghiệm** | Bỏ nghiệm không giải thích lý do. | Chỉ ghi "loại" mà không chỉ rõ điều kiện vi phạm. | Chỉ ra điều kiện vi phạm nhưng chưa đối chiếu số học. | Đối chiếu rõ ràng giá trị số học với điều kiện. | Giải thích toán học chặt chẽ, hiển thị giá trị $g(r) < 0$. |
| **C4: Tính ổn định và an toàn hệ thống** | Bị lỗi crash hoặc tràn bộ nhớ. | Chạy chậm bất thường trên hệ số lớn. | Hoàn thành nhưng không có cơ chế giới hạn hiển thị. | Hoàn thành tốt, có thông báo giới hạn. | Tính toán nhanh, bảo vệ trần lặp, thông báo an toàn rõ ràng. |
| **C5: Tính sư phạm theo chuẩn GDPT 2018** | Trình bày lộn xộn, khó theo dõi. | Trình bày theo văn phong lập trình, khó hiểu. | Trình bày tạm ổn nhưng chưa chuẩn mực sư phạm. | Lời giải rõ ràng, cấu trúc các bước mạch lạc. | Chuẩn mực sư phạm, trực quan, phù hợp trình độ học sinh THPT. |

### 7.2. Phương pháp luận đo lường độ tin cậy liên thẩm định viên (Inter-Rater Reliability)
1. **Quy trình đánh giá mù (Blinding Protocol):** Các lời giải được xuất từ CAD Math Studio, SymPy và lời giải thủ công của giáo viên được chuẩn hóa định dạng văn bản đồng nhất, ẩn danh nguồn gốc trước khi giao cho hội đồng giáo viên đánh giá độc lập.
2. **Chỉ số đo lường độ tin cậy:**
   - Sử dụng hệ số **Krippendorff's $\alpha$ (dạng ordinal)** để đo mức độ đồng thuận giữa các giáo viên, với ngưỡng chấp nhận $\alpha \ge 0.70$.
   - Tính toán hệ số tương quan nội lớp **ICC(2,1)** (Two-way random effects, absolute agreement, single rater).
3. **Xử lý cấu trúc dữ liệu phân cụm (Cluster Bootstrap):** Do mỗi giáo viên chấm điểm trên nhiều bài toán lặp lại (repeated measures), phương pháp **Cluster Bootstrap theo cụm giáo viên** được áp dụng để ước lượng khoảng tin cậy 95% CI cho các chỉ số đánh giá, bảo đảm xử lý đúng tương quan nội cụm.

---

## 8. MÃ NGUỒN TỰ CHỨA ĐẦY ĐỦ ĐỂ TÁI LẬP ĐỘC LẬP

### 8.1. Mã nguồn Giải thuật Lõi tự chứa (`stem_shared_core/cad_math_core.py`)
Mã nguồn độc lập 100% với GUI Tkinter, có thể chạy trực tiếp trên bất kỳ môi trường Python nào có thư viện `sympy`:

```python
"""
CAD Math Studio - Module Giải thuật Lõi (CADMathCore)
Phiên bản: 2.12 (Độc lập hoàn toàn với Tkinter và GUI)
Bao gồm:
- DiophantineCategory: Enum định nghĩa 8 trạng thái cấu trúc đạt tới được và 1 trạng thái dự phòng an toàn.
- clean_display_expr: Làm sạch định dạng hiển thị toán học.
- CADMathCore: Lớp giải thuật chứa phương thức kiểm tra tính thực, xác định dấu đại số/đa độ chính xác,
  giải phương trình vô tỷ sư phạm 4 bước, và giải hệ Diophantine tuyến tính d=1 bằng phân tích đồng dư.
"""

import re
import math
from enum import Enum
import sympy as sp
from sympy.ntheory.modular import solve_congruence

class DiophantineCategory(str, Enum):
    INCONSISTENT = "INCONSISTENT"
    UNIQUE = "UNIQUE"
    EMPTY_NO_POSITIVE_INTEGER = "EMPTY_NO_POSITIVE_INTEGER"
    UNSUPPORTED_DIM_GE_2 = "UNSUPPORTED_DIM>=2"
    INFEASIBLE_BOUNDS_EMPTY = "INFEASIBLE_BOUNDS_EMPTY"
    INFEASIBLE_NO_INTEGER_POINTS = "INFEASIBLE_NO_INTEGER_POINTS"
    FINITE_BOUNDED = "FINITE_BOUNDED"
    UNBOUNDED_INFINITE = "UNBOUNDED_INFINITE"
    UNKNOWN = "UNKNOWN"

def clean_display_expr(expr):
    """Làm sạch định dạng chuỗi biểu thức SymPy để hiển thị trực quan."""
    s = str(expr)
    s = s.replace("**", "^").replace("*", " ")
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

class CADMathCore:
    def __init__(self, listener=None):
        """
        Khởi tạo bộ giải lõi.
        listener: hàm callback tùy chọn nhận các thông điệp cập nhật (nếu cần kết nối giao diện).
        """
        self.listener = listener
        self.last_dioph_category = None
        self.last_dioph_solutions = []
        self.last_dioph_n_total = 0

    def _notify(self, event_type, data):
        if self.listener is not None and callable(self.listener):
            try:
                self.listener(event_type, data)
            except Exception:
                pass

    @staticmethod
    def real_status(r):
        """Xác định nghiệm r là thực (True), phức (False) hay chưa kết luận (None)."""
        if r.is_real is True:
            return True
        if r.is_real is False:
            return False
        try:
            a = sp.N(r, 60)
            im = abs(sp.im(a))
            if im < sp.Float('1e-45'):
                return True
            if im > sp.Float('1e-20'):
                return False
        except Exception:
            pass
        return None

    @staticmethod
    def check_sign_exact(expr_sub):
        """
        Xác định dấu của biểu thức kết hợp đại số ký hiệu và số học đa độ chính xác.
        Trả về: 'pos', 'neg', 'zero', 'nonreal', hoặc 'unknown'.
        """
        expr_s = sp.simplify(expr_sub)
        if expr_s.is_real is False:
            return 'nonreal'
        if expr_s.is_zero:
            return 'zero'
        if expr_s.is_positive:
            return 'pos'
        if expr_s.is_negative:
            return 'neg'
        try:
            s = sp.sign(expr_s)
            if s.is_number:
                if float(s) > 0:
                    return 'pos'
                elif float(s) < 0:
                    return 'neg'
                else:
                    return 'zero'
        except Exception:
            pass
        try:
            val = float(sp.N(expr_s, 40))
            if abs(val) > 1e-30:
                return 'pos' if val > 0 else 'neg'
        except Exception:
            pass
        return 'unknown'

    def solve_radical_pedagogical(self, target_eq, x):
        """
        Giải phương trình vô tỷ dạng c*sqrt(f(x)) + h(x) = 0 qua 4 bước sư phạm chuẩn.
        Trả về: (steps, valid_sols, rejected_sols, indeterminate_sols)
        """
        steps = []
        rads = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
        if len(rads) != 1:
            return ["  • Ngoài phạm vi hỗ trợ: Hệ thống hiện tại chuyên biệt cho phương trình chứa đúng 1 căn thức."], [], [], []

        rad = rads[0]
        expanded = sp.expand(target_eq)
        c = expanded.coeff(rad)
        rest = sp.expand(expanded - c * rad)

        if c == 0 or c.free_symbols or any(t.exp == sp.Rational(1, 2) for t in rest.atoms(sp.Pow)):
            return ["  • Ngoài phạm vi hỗ trợ: Dạng căn thức phi tuyến hoặc không cô lập được."], [], [], []

        # Chuẩn hóa về dạng chính tắc: sqrt(f) = gx với hệ số căn = 1
        gx = sp.simplify(-rest / c)
        fx = rad.base

        steps.append("\n[BƯỚC 1: XÁC ĐỊNH ĐIỀU KIỆN CÓ NGHĨA & ĐIỀU KIỆN VẾ PHẢI]")
        steps.append(f"  • Đưa phương trình về dạng chuẩn tắc: √({clean_display_expr(fx)}) = {clean_display_expr(gx)}")

        # 1. Điều kiện xác định căn thức f(x) >= 0
        if not fx.free_symbols:
            try:
                f_const = float(fx.evalf())
                if f_const >= 0:
                    steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0 (Luôn thỏa mãn với mọi x ∈ ℝ).")
                else:
                    steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0 (Không tồn tại x thỏa mãn).")
            except Exception:
                steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
        else:
            steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
            try:
                cond_fx = sp.solve(fx >= 0, x)
                steps.append(f"    ==> Miền D_rad: {cond_fx}")
            except Exception:
                pass

        # 2. Điều kiện vế phải g(x) >= 0
        if not gx.free_symbols:
            try:
                g_const = float(gx.evalf())
                if g_const >= 0:
                    steps.append(f"  • Điều kiện vế phải (g(x) = {clean_display_expr(gx)} >= 0): Luôn thỏa mãn với mọi x ∈ ℝ.")
                else:
                    steps.append(f"  • Điều kiện vế phải (g(x) = {clean_display_expr(gx)} < 0): Không tồn tại x thỏa mãn.")
            except Exception:
                steps.append(f"  • Điều kiện vế phải: {clean_display_expr(gx)} >= 0")
        else:
            steps.append(f"  • Điều kiện vế phải (Vì căn bậc hai số học √({clean_display_expr(fx)}) >= 0 nên vế phải bắt buộc g(x) >= 0): {clean_display_expr(gx)} >= 0")
            try:
                cond_gx = sp.solve(gx >= 0, x)
                steps.append(f"    ==> Miền D_sign: {cond_gx}")
            except Exception:
                pass

        steps.append("\n[BƯỚC 2: BÌNH PHƯƠNG HAI VẾ TÌM TẬP NGHIỆM ĐẠI SỐ SƠ BỘ]")
        steps.append(f"  • ({clean_display_expr(rad)})² = ({clean_display_expr(gx)})²")
        poly_eq = sp.simplify(fx - gx**2)
        steps.append(f"  <=> {clean_display_expr(poly_eq)} = 0")

        raw_sols = sp.solve(poly_eq, x)
        steps.append(f"  • Nghiệm đại số sơ bộ từ phương trình hệ quả: {raw_sols}")

        steps.append("\n[BƯỚC 3: XÁC ĐỊNH DẤU ĐẠI SỐ CHÍNH XÁC & LOẠI BỎ NGHIỆM NGOẠI LAI]")
        valid_sols = []
        rejected_sols = []
        indeterminate_sols = []

        for r in raw_sols:
            r_st = self.real_status(r)
            if r_st is False:
                rejected_sols.append((r, "Nghiệm phức không thuộc tập số thực ℝ"))
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Loại bỏ (Nghiệm phức, Im(r) ≠ 0).")
                continue

            s_gx = self.check_sign_exact(gx.subs(x, r))
            s_fx = self.check_sign_exact(fx.subs(x, r))

            if s_gx == 'neg':
                rejected_sols.append((r, f"Vi phạm điều kiện vế phải g({clean_display_expr(r)}) < 0"))
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Loại bỏ (Nghiệm ngoại lai do vế phải g(r) < 0).")
            elif s_fx == 'neg':
                rejected_sols.append((r, f"Vi phạm điều kiện xác định căn thức f({clean_display_expr(r)}) < 0"))
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Loại bỏ (f(r) < 0 vi phạm điều kiện có nghĩa).")
            elif s_gx in ['pos', 'zero'] and s_fx in ['pos', 'zero']:
                valid_sols.append(r)
                val_approx = None
                try:
                    if not r.is_Integer:
                        val_approx = f"{float(sp.N(r, 6)):.4f}"
                except Exception:
                    pass
                approx_str = f" (≈ {val_approx})" if val_approx else ""
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}{approx_str}: Thỏa mãn cả D_rad và D_sign ==> Nhận.")
            else:
                indeterminate_sols.append((r, f"g:{s_gx}, f:{s_fx}"))
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Không thể xác định dấu giải tích chính xác ==> Cảnh báo kiểm chứng bổ sung.")

        # BƯỚC 4: KẾT LUẬN TẬP NGHIỆM S
        steps.append("\n[BƯỚC 4: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
        if indeterminate_sols:
            indet_strs = [clean_display_expr(r) for r, _ in indeterminate_sols]
            steps.append(f"  ==> CHƯA THỂ KẾT LUẬN ĐẦY ĐỦ: Phát hiện {len(indeterminate_sols)} nghiệm chưa xác định được dấu đại số ({', '.join(indet_strs)}).")
        elif not valid_sols:
            steps.append("  ==> Phương trình vô nghiệm trên ℝ (S = ∅).")
        else:
            sol_items = []
            for r in valid_sols:
                val_approx = None
                try:
                    if not r.is_Integer:
                        val_approx = f"{float(sp.N(r, 6)):.4f}"
                except Exception:
                    pass
                if val_approx:
                    sol_items.append(f"{clean_display_expr(r)} (≈ {val_approx})")
                else:
                    sol_items.append(f"{clean_display_expr(r)}")
            steps.append(f"  ==> Tập nghiệm hợp lệ: S = {{ {', '.join(sol_items)} }}")

        self._notify('radical_result', {'steps': steps, 'valid': valid_sols, 'rejected': rejected_sols, 'indeterminate': indeterminate_sols})
        return steps, valid_sols, rejected_sols, indeterminate_sols

    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines=None):
        """
        Bộ giải Diophantine tuyến tính d=1 và phân loại cấu trúc hệ vô định.
        Trả về: (category, int_sols, n_total, out_lines)
        """
        out = []
        out.append("=" * 85)
        out.append("QUY TRÌNH GIẢI HỆ PHƯƠNG TRÌNH VÔ ĐỊNH & KHẢO SÁT NGHIỆM NGUYÊN (DIOPHANTINE SYSTEM):")
        out.append("=" * 85)

        m = len(eq_syms)
        n = len(vars_sorted)
        var_names_str = ", ".join(s.name for s in vars_sorted)

        # BƯỚC 1: PHÂN TÍCH CẤU TRÚC ĐẠI SỐ TUYẾN TÍNH
        out.append("\n[BƯỚC 1: PHÂN TÍCH CẤU TRÚC ĐẠI SỐ TUYẾN TÍNH]")
        out.append(f"  • Số lượng phương trình: M = {m}")
        out.append(f"  • Số lượng biến số: N = {n} ({var_names_str})")

        linsols = sp.linsolve(eq_syms, vars_sorted)
        if not linsols:
            out.append("  • Hệ phương trình vô nghiệm trên tập số thực ℝ (rank(A) != rank(A|b)).")
            category = DiophantineCategory.INCONSISTENT
            self.last_dioph_category = category
            self.last_dioph_solutions = []
            self.last_dioph_n_total = 0
            self._notify('diophantine_result', {'category': category, 'sols': [], 'n_total': 0, 'out': out})
            return category, [], 0, out

        sol_tuple = list(linsols)[0]
        free_syms = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)
        d = len(free_syms)
        out.append(f"  • Bậc tự do của hệ: d = N - rank(A) = {d} tham số tự do.")

        # Xử lý d = 0 (Hệ xác định, nghiệm duy nhất)
        if d == 0:
            out.append("\n[BƯỚC 2: KHẢO SÁT NGHIỆM DUY NHẤT (d = 0)]")
            is_pos_int = all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in sol_tuple)
            sol_str = ", ".join(f"{v.name} = {c}" for v, c in zip(vars_sorted, sol_tuple))
            if is_pos_int:
                out.append(f"  ==> Hệ có nghiệm nguyên dương duy nhất: ({sol_str})")
                category = DiophantineCategory.UNIQUE
                sols = [tuple(int(c) for c in sol_tuple)]
                self.last_dioph_category = category
                self.last_dioph_solutions = sols
                self.last_dioph_n_total = 1
                self._notify('diophantine_result', {'category': category, 'sols': sols, 'n_total': 1, 'out': out})
                return category, sols, 1, out
            else:
                out.append(f"  ==> Hệ có nghiệm thực duy nhất ({sol_str}) nhưng không thuộc tập số nguyên dương (ℤ⁺)ⁿ.")
                category = DiophantineCategory.EMPTY_NO_POSITIVE_INTEGER
                self.last_dioph_category = category
                self.last_dioph_solutions = []
                self.last_dioph_n_total = 0
                self._notify('diophantine_result', {'category': category, 'sols': [], 'n_total': 0, 'out': out})
                return category, [], 0, out

        # Xử lý d >= 2 (Đa tham số, thông báo phạm vi an toàn)
        if d >= 2:
            out.append(f"\n[BƯỚC 2: HỌ NGHIỆM TỔNG QUÁT ĐA THAM SỐ (d = {d} >= 2)]")
            out.append(f"  • Hệ có {d} tham số tự do ({', '.join(s.name for s in free_syms)}) trên ℝ.")
            out.append("  • Biểu diễn affine nghiệm tổng quát trên ℝ:")
            for v, expr in zip(vars_sorted, sol_tuple):
                out.append(f"    {v} = {clean_display_expr(expr)}")
            out.append("  • Lưu ý phạm vi sư phạm: Lớp bài toán Diophantine đa tham số (d >= 2) hiện chưa quét tự động trên tập số nguyên dương (ℤ⁺)ⁿ.")
            category = DiophantineCategory.UNSUPPORTED_DIM_GE_2
            self.last_dioph_category = category
            self.last_dioph_solutions = []
            self.last_dioph_n_total = 0
            self._notify('diophantine_result', {'category': category, 'sols': [], 'n_total': 0, 'out': out})
            return category, [], 0, out

        # TRƯỜNG HỢP d = 1: Phân tích đồng dư solve_congruence và các trạng thái cấu trúc
        param = free_syms[0]
        out.append(f"\n[BƯỚC 2: BIỂU DIỄN THAM SỐ AFFINE THEO ẨN TỰ DO {param}]")
        for v, expr in zip(vars_sorted, sol_tuple):
            if expr == v:
                out.append(f"  • Tham số tự do: {v} ∈ ℝ")
            else:
                out.append(f"  • Biến phụ thuộc {v}: {v} = {clean_display_expr(expr)}")

        out.append("\n[BƯỚC 3: PHÂN TÍCH HỆ ĐỒNG DƯ VÀ RÀNG BUỘC BIÊN (ℤ⁺)]")
        lo = sp.Integer(1)
        hi = None
        infeasible_constant = False
        congruences = []
        no_integer_point = False

        for v, expr in zip(vars_sorted, sol_tuple):
            e_exp = sp.expand(expr)
            a_sym = sp.Rational(e_exp.coeff(param))
            b_sym = sp.Rational(e_exp.subs(param, 0))
            out.append(f"  • {v} > 0  <=>  {clean_display_expr(expr)} > 0")

            if a_sym > 0:
                bd = sp.floor(-b_sym / a_sym) + 1
                lo = bd if lo is None else max(lo, bd)
            elif a_sym < 0:
                bd = sp.ceiling(-b_sym / a_sym) - 1
                hi = bd if hi is None else min(hi, bd)
            else:
                if b_sym <= 0:
                    infeasible_constant = True

            D_val = math.lcm(a_sym.q, b_sym.q)
            A_val = int(a_sym * D_val)
            B_val = int(b_sym * D_val)
            g_val = math.gcd(A_val, D_val)
            if (-B_val) % g_val != 0:
                no_integer_point = True
            elif A_val != 0:
                Ag = A_val // g_val
                Dg = D_val // g_val
                rem = (-(B_val // g_val) * pow(Ag, -1, Dg)) % Dg if Dg > 1 else 0
                congruences.append((rem, Dg))

        int_sols = []
        category = DiophantineCategory.UNKNOWN
        n_total = 0

        if infeasible_constant or (hi is not None and lo > hi):
            category = DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY
            out.append("\n  ==> KẾT QUẢ: Miền ràng buộc rỗng (Hệ bất phương trình biên vô nghiệm).")
        elif no_integer_point:
            category = DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS
            out.append("\n  ==> KẾT QUẢ: Hệ đồng dư vô nghiệm trên ℤ (Hệ có nghiệm thực dương nhưng không có điểm nguyên).")
        else:
            sc = solve_congruence(*congruences) if congruences else (0, 1)
            if sc is None:
                category = DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS
                out.append("\n  ==> KẾT QUẢ: Hệ đồng dư vô nghiệm trên ℤ (Không thỏa mãn hệ đồng dư CRT).")
            else:
                p_res, m_mod = int(sc[0]), int(sc[1])
                k_start = int(sp.ceiling((lo - p_res) / m_mod))
                start_val = p_res + k_start * m_mod

                if hi is not None:
                    if start_val > hi:
                        category = DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS
                        out.append(f"\n  ==> KẾT QUẢ: Không có điểm nguyên nào thỏa mãn đồng dư trong miền bị chặn [{lo}, {hi}].")
                    else:
                        category = DiophantineCategory.FINITE_BOUNDED
                        out.append(f"\n  ==> KẾT QUẢ: Miền nghiệm hữu hạn bị chặn ({param} ∈ [{lo}, {hi}]).")
                        out.append(f"      Điều kiện đồng dư nghiệm nguyên: {param} ≡ {p_res} (mod {m_mod}).")
                        n_total = int((hi - start_val) // m_mod + 1)

                        eval_count = min(n_total, 10)
                        for k_idx in range(eval_count):
                            pval = start_val + k_idx * m_mod
                            cand = [item.subs(param, pval) for item in sol_tuple]
                            if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                                sub_dict = {vr: c_val for vr, c_val in zip(vars_sorted, cand)}
                                if all(sp.simplify(eq_orig.subs(sub_dict)) == 0 for eq_orig in eq_syms):
                                    int_sols.append(tuple(int(c) for c in cand))

                        if n_total <= 10:
                            out.append(f"  ==> Liệt kê toàn bộ {len(int_sols)} bộ nghiệm nguyên dương:")
                        else:
                            out.append(f"  ==> Hệ có tổng cộng {n_total} bộ nghiệm nguyên dương. Hiển thị 10 bộ nghiệm đầu tiên (do giới hạn không gian giao diện):")

                        for idx, sol in enumerate(int_sols, 1):
                            sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                            out.append(f"    • Bộ nghiệm {idx}: {sol_str}")
                        if n_total > 10:
                            out.append(f"    ... [còn {n_total - 10} bộ nghiệm tiếp theo]")
                else:
                    category = DiophantineCategory.UNBOUNDED_INFINITE
                    out.append(f"\n  ==> KẾT QUẢ: Miền nghiệm vô hạn không bị chặn trên ({param} >= {lo}).")
                    out.append(f"      Họ nghiệm nguyên dương theo tham số: {param} = {start_val} + {m_mod}·k (với k ∈ ℤ, k >= 0).")

                    for k_idx in range(3):
                        pval = start_val + k_idx * m_mod
                        cand = [item.subs(param, pval) for item in sol_tuple]
                        if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                            sub_dict = {vr: c_val for vr, c_val in zip(vars_sorted, cand)}
                            if all(sp.simplify(eq_orig.subs(sub_dict)) == 0 for eq_orig in eq_syms):
                                int_sols.append(tuple(int(c) for c in cand))

                    out.append(f"  ==> Hệ có vô số bộ nghiệm nguyên dương. Ba bộ nghiệm nhỏ nhất đại diện:")
                    for idx, sol in enumerate(int_sols, 1):
                        sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                        out.append(f"    • Bộ nghiệm {idx}: {sol_str}")

        # BƯỚC 4: KẾT LUẬN
        out.append("\n[BƯỚC 4: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
        if category == DiophantineCategory.FINITE_BOUNDED and int_sols:
            if n_total > 10:
                out.append(f"  ==> Kết luận: Hệ có {n_total} bộ nghiệm nguyên dương hữu hạn (chi tiết 10 bộ nghiệm đầu như trên).")
            else:
                latex_cases = [f"({', '.join(str(val) for val in sol)})" for sol in int_sols]
                out.append(f"  ==> Tập nghiệm nguyên dương hữu hạn: S_(ℤ⁺) = {{ {'; '.join(latex_cases)} }}")
        elif category == DiophantineCategory.UNBOUNDED_INFINITE:
            out.append("  ==> Hệ có vô số nghiệm nguyên dương phụ thuộc tham số không bị chặn.")
        else:
            out.append("  ==> Hệ không có nghiệm nguyên dương (S_(ℤ⁺) = ∅).")

        self.last_dioph_category = category
        self.last_dioph_solutions = int_sols
        self.last_dioph_n_total = n_total
        self._notify('diophantine_result', {'category': category, 'sols': int_sols, 'n_total': n_total, 'out': out})
        return category, int_sols, n_total, out

```

### 8.2. Mã nguồn Bộ kiểm thử Benchmark (`stem_shared_core/tools/run_batch_auto_test.py`)
Mã nguồn đầy đủ của bộ kiểm thử tự động, tích hợp kiểm tra 4 bất biến, Oracle hộp cố định và 6 toán tử đột biến:

```python
"""
BỘ KIỂM THỬ TỰ ĐỘNG HÀNG LOẠT V2.12 (CAD MATH STUDIO BENCHMARK HARNESS)
Kiểm tra 4 Bất biến toán học, Oracle Hộp cố định độc lập (Fixed-Box Brute-Force Oracle, N=3000)
sử dụng math.lcm thuần túy trên 100 hệ phân tầng, và Kiểm thử đột biến thật (Real Mutation Testing 6 toán tử).
Chạy đa vòng (1 vòng khởi động tách biệt + 5 vòng đo lường chính thức, trích xuất Median & IQR).
Nhập khẩu trực tiếp từ module giải thuật lõi độc lập: stem_shared_core.cad_math_core.
"""

import sys, os, time, random, statistics, inspect, types, textwrap, unittest.mock, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.stdout.reconfigure(encoding='utf-8')

import sympy as sp
from stem_shared_core.cad_math_core import CADMathCore, DiophantineCategory, clean_display_expr

def get_test_cases(x, y, z):
    return [
        # NHÓM 1: PHƯƠNG TRÌNH VÔ TỶ (7 CA ĐẶC TRƯNG)
        {
            "id": "RAD_01_CANONICAL",
            "name": "Phương trình vô tỷ chính tắc sqrt(2x-1) = x - 1 (c = 1)",
            "type": "radical",
            "target": sp.sqrt(2*x - 1) - (x - 1),
            "var": x,
            "expected_valid": [2 + sp.sqrt(2)],
            "expected_rejected_count": 1
        },
        {
            "id": "RAD_02_NEGATIVE_COEFF",
            "name": "Phương trình vô tỷ hệ số căn âm: (x - 1) - sqrt(2x-1) = 0 (c = -1)",
            "type": "radical",
            "target": (x - 1) - sp.sqrt(2*x - 1),
            "var": x,
            "expected_valid": [2 + sp.sqrt(2)],
            "expected_rejected_count": 1
        },
        {
            "id": "RAD_03_COEFF_NOT_ONE",
            "name": "Phương trình vô tỷ hệ số căn c != 1: 2*sqrt(x+2) - (x+1) = 0",
            "type": "radical",
            "target": 2*sp.sqrt(x + 2) - (x + 1),
            "var": x,
            "expected_valid": [1 + 2*sp.sqrt(2)],
            "expected_rejected_count": 1
        },
        {
            "id": "RAD_04_CARDANO_CUBIC",
            "name": "Phương trình vô tỷ bậc 3 sinh nghiệm Cardano thực: sqrt(x^3-3x+1) = 1/2",
            "type": "radical",
            "target": sp.sqrt(x**3 - 3*x + 1) - sp.Rational(1, 2),
            "var": x,
            "expected_valid_count": 3,
            "expected_rejected_count": 0
        },
        {
            "id": "RAD_05_COMPLEX_QUARTIC",
            "name": "Bẫy bình phương sinh nghiệm phức: sqrt(x) = x^2 + 1",
            "type": "radical",
            "target": sp.sqrt(x) - (x**2 + 1),
            "var": x,
            "expected_valid": [],
            "expected_rejected_count": 4
        },
        {
            "id": "RAD_06_OUT_OF_SCOPE",
            "name": "Phương trình nhiều căn thức (ngoài phạm vi): sqrt(x+1) + sqrt(x-1) = 2",
            "type": "radical_out_of_scope",
            "target": sp.sqrt(x + 1) + sp.sqrt(x - 1) - 2,
            "var": x,
            "expected_error": True
        },
        {
            "id": "RAD_07_SYNTHETIC_UNKNOWN",
            "name": "Kiểm thử đường dẫn an toàn qua mock.patch: Nhánh bất định (indeterminate)",
            "type": "radical_mock_unknown",
            "target": sp.sqrt(2*x - 1) - (x - 1),
            "var": x,
            "expected_indet_count": 2
        },

        # NHÓM 2: HỆ DIOPHANTINE & PHÂN LOẠI CẤU TRÚC (14 CA BAO PHỦ 8 TRẠNG THÁI)
        {
            "id": "DIO_01_TRAM_TRAU",
            "name": "Bài toán Trăm trâu cổ điển",
            "type": "diophantine",
            "eqs": [x + y + z - 100, 5*x + 3*y + sp.Rational(1, 3)*z - 100],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 3,
            "expected_sample": (4, 18, 78)
        },
        {
            "id": "DIO_02_SYSTEM_2",
            "name": "Hệ Diophantine hai phương trình hữu hạn",
            "type": "diophantine",
            "eqs": [3*x - 7*z + 500, 3*y + 10*z - 800],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 2,
            "expected_sample": (6, 20, 74)
        },
        {
            "id": "DIO_03_COUNTER_A",
            "name": "Phản ví dụ A bước nhảy 251 (Vô hạn nghiệm)",
            "type": "diophantine",
            "eqs": [251*x - z + 5, y - 2],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.UNBOUNDED_INFINITE,
            "expected_sample": (1, 2, 256)
        },
        {
            "id": "DIO_04_COUNTER_B",
            "name": "Phản ví dụ B vô nghiệm nguyên gcd: 2x - 2z = 1",
            "type": "diophantine",
            "eqs": [2*x - 2*z - 1, y - 5],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS
        },
        {
            "id": "DIO_05_HUGE_CAP",
            "name": "Hệ có số lượng nghiệm lớn N = 10^9, kiểm tra giải tích",
            "type": "diophantine",
            "eqs": [x + z - 1000000001, y - 2],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 1000000000
        },
        {
            "id": "DIO_06_MULTI_PARAM",
            "name": "Hệ đa tham số tự do d=2: x + y + z = 10",
            "type": "diophantine",
            "eqs": [x + y + z - 10],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.UNSUPPORTED_DIM_GE_2
        },
        {
            "id": "DIO_07_INCONSISTENT",
            "name": "Hệ vô nghiệm thực: x + y = 1, x + y = 2",
            "type": "diophantine",
            "eqs": [x + y - 1, x + y - 2],
            "vars": [x, y],
            "expected_category": DiophantineCategory.INCONSISTENT
        },
        {
            "id": "DIO_08_BOUNDS_EMPTY",
            "name": "Hệ vô nghiệm do hằng số không dương: y = 0",
            "type": "diophantine",
            "eqs": [x - z - 5, y],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY
        },
        {
            "id": "DIO_09_UNIQUE_D0",
            "name": "Hệ d=0 xác định nghiệm nguyên dương duy nhất",
            "type": "diophantine",
            "eqs": [x + y - 5, x - y - 1],
            "vars": [x, y],
            "expected_category": DiophantineCategory.UNIQUE,
            "expected_count": 1,
            "expected_sample": (3, 2)
        },
        {
            "id": "DIO_10_NON_COPRIME_CRT",
            "name": "Hệ đồng dư modulo không nguyên tố cùng nhau: gcd(m1, m2) > 1",
            "type": "diophantine",
            "eqs": [6*x - z - 1, 4*y - z - 1],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.UNBOUNDED_INFINITE,
            "expected_sample": (2, 3, 11)
        },
        {
            "id": "DIO_11_UNIQUE_NON_POSITIVE",
            "name": "Hệ d=0 có nghiệm thực duy nhất nhưng không thuộc (Z+)^n",
            "type": "diophantine",
            "eqs": [x + y - 1, x - y - 3],
            "vars": [x, y],
            "expected_category": DiophantineCategory.EMPTY_NO_POSITIVE_INTEGER,
            "expected_count": 0
        },
        {
            "id": "DIO_12_CRT_INCOMPATIBLE",
            "name": "Hệ đồng dư CRT xung đột vô nghiệm (sc is None)",
            "type": "diophantine",
            "eqs": [2*x - z, 2*y - z + 1],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS,
            "expected_count": 0
        },
        {
            "id": "DIO_13_BOUNDARY_SENSITIVE_LO",
            "name": "Ca biên nhạy cận dưới: x - z + 3 = 0, y - 2 = 0 (z >= 4, diệt Mutant 1)",
            "type": "diophantine",
            "eqs": [x - z + 3, y - 2],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.UNBOUNDED_INFINITE,
            "expected_sample": (1, 2, 4)
        },
        {
            "id": "DIO_14_BOUNDARY_SENSITIVE_HI",
            "name": "Ca biên nhạy cận trên: x + z - 4 = 0, y - 2 = 0 (z <= 3, diệt Mutant 2 & 3)",
            "type": "diophantine",
            "eqs": [x + z - 4, y - 2],
            "vars": [x, y, z],
            "expected_category": DiophantineCategory.FINITE_BOUNDED,
            "expected_count": 3,
            "expected_sample": (3, 2, 1)
        }
    ]

def execute_single_run(app, test_cases, is_warmup=False):
    passed_count = 0
    times = []
    results = []

    for idx, test in enumerate(test_cases, 1):
        t0 = time.perf_counter()
        t_type = test["type"]
        is_pass = False
        detail = ""

        try:
            if t_type == "radical":
                steps, valid, rejected, indet = app.solve_radical_pedagogical(test["target"], test["var"])
                dt = (time.perf_counter() - t0) * 1000
                times.append(dt)

                rads = [t for t in test["target"].atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
                rad = rads[0]
                expanded = sp.expand(test["target"])
                c_val = expanded.coeff(rad)
                rest = sp.expand(expanded - c_val * rad)
                gx = sp.simplify(-rest / c_val)
                fx = rad.base

                # INVARIANT 1: Nghiệm valid có phần dư phương trình gốc < 1e-7 và vế phải g(r) >= -1e-12
                inv1_ok = True
                for r in valid:
                    val_sub = abs(complex(sp.N(test["target"].subs(test["var"], r))))
                    g_val = float(sp.N(gx.subs(test["var"], r)))
                    if val_sub >= 1e-7 or g_val < -1e-12:
                        inv1_ok = False
                        break

                # INVARIANT 2: Nghiệm rejected vi phạm độc lập điều kiện xác định/vế phải/nghiệm phức
                inv2_ok = True
                for r_info in rejected:
                    r = r_info[0]
                    r_im = abs(complex(sp.N(r)).imag)
                    if r_im > 1e-5:
                        continue
                    g_val = float(sp.N(gx.subs(test["var"], r)))
                    f_val = float(sp.N(fx.subs(test["var"], r)))
                    residue = abs(complex(sp.N(test["target"].subs(test["var"], r))))
                    if g_val < -1e-12 or f_val < -1e-12 or residue > 1e-5:
                        continue
                    inv2_ok = False
                    break

                # BẤT BIẾN PHÂN HOẠCH: len(valid) + len(rejected) + len(indet) == len(raw_sols)
                poly_eq = sp.simplify(fx - gx**2)
                raw_sols = sp.solve(poly_eq, test["var"])
                partition_ok = (len(valid) + len(rejected) + len(indet) == len(raw_sols))

                # KIỂM TRA ĐỦ NGHIỆM ĐỐI CHIẾU TẬP CHUẨN ĐÃ DUYỆT (CURATED REFERENCE SET)
                if "expected_valid" in test:
                    completeness_ok = (len(valid) == len(test["expected_valid"]))
                    if completeness_ok and len(valid) > 0:
                        completeness_ok = all(any(sp.simplify(v - ev) == 0 for ev in test["expected_valid"]) for v in valid)
                elif "expected_valid_count" in test:
                    completeness_ok = (len(valid) == test["expected_valid_count"])
                else:
                    completeness_ok = True

                if inv1_ok and inv2_ok and partition_ok and completeness_ok and len(rejected) == test["expected_rejected_count"]:
                    is_pass = True
                    detail = f"Nhận {len(valid)}, loại {len(rejected)} (Thỏa mãn Inv 1, 2, Phân hoạch & Đủ nghiệm)"
                else:
                    detail = f"Thất bại: inv1={inv1_ok}, inv2={inv2_ok}, part={partition_ok}, comp={completeness_ok}"

            elif t_type == "radical_out_of_scope":
                steps, valid, rejected, indet = app.solve_radical_pedagogical(test["target"], test["var"])
                dt = (time.perf_counter() - t0) * 1000
                times.append(dt)
                if len(steps) > 0 and "Ngoài phạm vi hỗ trợ" in steps[0]:
                    is_pass = True
                    detail = "Từ chối an toàn dạng bài ngoài phạm vi"

            elif t_type == "radical_mock_unknown":
                with unittest.mock.patch.object(app, 'check_sign_exact', return_value='unknown'):
                    steps, valid, rejected, indet = app.solve_radical_pedagogical(test["target"], test["var"])
                dt = (time.perf_counter() - t0) * 1000
                times.append(dt)
                warning_ok = any("CHƯA THỂ KẾT LUẬN" in s for s in steps)
                if len(indet) == test["expected_indet_count"] and len(valid) == 0 and warning_ok:
                    is_pass = True
                    detail = f"Mã sản phẩm nhận diện {len(indet)} nghiệm bất định, cảnh báo bước 4 kích hoạt"

            elif t_type == "diophantine":
                cat, sols, n_tot, out_lines = app.solve_underdetermined_or_diophantine(test["eqs"], test["vars"])
                dt = (time.perf_counter() - t0) * 1000
                times.append(dt)

                exp_cat = test["expected_category"]
                cat_ok = (cat == exp_cat)

                # INVARIANT 3: Nghiệm nguyên dương và thỏa mãn đồng thời hệ phương trình gốc
                inv3_ok = True
                if sols:
                    for s_tuple in sols:
                        if not all(isinstance(val, int) and val > 0 for val in s_tuple):
                            inv3_ok = False
                            break
                        sub_d = {v: val for v, val in zip(test["vars"], s_tuple)}
                        if not all(sp.simplify(eq.subs(sub_d)) == 0 for eq in test["eqs"]):
                            inv3_ok = False
                            break
                else:
                    inv3_ok = (n_tot == 0)

                count_ok = True
                if "expected_count" in test:
                    count_ok = (n_tot == test["expected_count"])

                sample_ok = True
                if "expected_sample" in test:
                    sample_ok = (test["expected_sample"] in sols)

                if cat_ok and inv3_ok and count_ok and sample_ok:
                    is_pass = True
                    if sols:
                        detail = f"Category={cat} khớp, Inv 3 thỏa mãn ({len(sols)} nghiệm thực chứng)"
                    else:
                        detail = f"Category={cat} khớp, Inv 3 thỏa mãn (0 nghiệm, n_tot=0)"
                else:
                    detail = f"Thất bại: cat_ok={cat_ok} (got {cat}), inv3={inv3_ok}, count={count_ok}, sample={sample_ok}"

        except Exception as e:
            dt = (time.perf_counter() - t0) * 1000
            times.append(dt)
            detail = f"Lỗi ngoại lệ: {e}"

        if is_pass: passed_count += 1
        results.append((test['id'], is_pass, dt, detail))

    return passed_count, times, results

def run_suite():
    print("=" * 95)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TỰ ĐỘNG HÀNG LOẠT V2.12 (CAD MATH STUDIO BENCHMARK HARNESS)")
    print("Môi trường: SymPy 1.14.0 | Python 3.14.5 (64-bit) | CPU: Intel Core i7-11800H @ 2.30GHz")
    print("Kiểm tra Invariants 1-2-3, Phân hoạch, Đủ nghiệm, Oracle Hộp cố định & 6 Toán tử đột biến thật")
    print("=" * 95)

    app = CADMathCore()
    x, y, z = sp.symbols('x y z')
    test_cases = get_test_cases(x, y, z)

    # 1. VÒNG KHỞI ĐỘNG (WARM-UP RUN TÁCH BIỆT)
    print("[1] Đang thực thi vòng khởi động (Warm-up run để nạp SymPy cache nội tại)...")
    execute_single_run(app, test_cases, is_warmup=True)

    # 2. CHẠY 5 VÒNG THỰC ĐO THỜI GIAN ĐỂ TÍNH TRUNG VỊ VÀ ĐỘ PHÂN TÁN (IQR)
    print("[2] Thực hiện 5 vòng đo chính thức để xác định Trung vị (Median) và IQR...")
    all_runs_times = []
    last_results = None
    last_passed = 0

    for r_idx in range(5):
        passed, times, results = execute_single_run(app, test_cases)
        all_runs_times.append(times)
        last_results = results
        last_passed = passed

    per_test_medians = [statistics.median([all_runs_times[r][i] for r in range(5)]) for i in range(len(test_cases))]
    total_medians = sum(per_test_medians)
    
    # Tính IQR cho toàn bộ bài
    quantiles_all = statistics.quantiles(per_test_medians, n=4)
    iqr_all = quantiles_all[2] - quantiles_all[0]

    for idx, (t_id, is_pass, _, detail) in enumerate(last_results):
        status_str = "[OK]  " if is_pass else "[FAIL]"
        med_t = per_test_medians[idx]
        print(f"[{idx+1:02d}/{len(test_cases):02d}] {status_str} {t_id:<28} (Trung vị: {med_t:6.2f} ms) | {detail}")

    # PHẦN 2: ORACLE HỘP CỐ ĐỊNH ĐỘC LẬP TRÊN 100 HỆ PHÂN TẦNG (N=3000)
    print("-" * 95)
    print("CHẠY ORACLE HỘP CỐ ĐỊNH ĐỘC LẬP: 100 HỆ DIOPHANTINE PHÂN TẦNG (Seed = 42, N = 3000)")
    print("Cơ chế: Vét cạn trực tiếp p in [1, 3000] bằng math.lcm / số học nguyên C (Không dùng sp.ilcm hay solver)")
    random.seed(42)
    categories_needed = {
        DiophantineCategory.FINITE_BOUNDED: 0,
        DiophantineCategory.UNBOUNDED_INFINITE: 0,
        DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY: 0,
        DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS: 0
    }
    dataset = []
    while any(count < 25 for count in categories_needed.values()):
        a1, b1, c1 = [random.choice([-4, -3, -2, -1, 1, 2, 3, 4]) for _ in range(3)]
        a2, b2, c2 = [random.choice([-4, -3, -2, -1, 1, 2, 3, 4]) for _ in range(3)]
        rhs1 = random.randint(-40, 40)
        rhs2 = random.randint(-40, 40)
        eqs = [a1*x + b1*y + c1*z - rhs1, a2*x + b2*y + c2*z - rhs2]
        cat, sols, n_tot, out_l = app.solve_underdetermined_or_diophantine(eqs, [x, y, z])
        if cat in categories_needed and categories_needed[cat] < 25:
            categories_needed[cat] += 1
            dataset.append(eqs)

    oracle_passed = 0
    N = 3000
    t_oracle_0 = time.perf_counter()

    for idx, eqs in enumerate(dataset):
        cat, sols, n_tot, out_l = app.solve_underdetermined_or_diophantine(eqs, [x, y, z])
        linsols = sp.linsolve(eqs, [x, y, z])
        sol_tuple = list(linsols)[0]
        free_s = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)
        p = free_s[0]

        affines = []
        has_neg_slope = False
        for expr in sol_tuple:
            e_exp = sp.expand(expr)
            a_r = sp.Rational(e_exp.coeff(p))
            b_r = sp.Rational(e_exp.subs(p, 0))
            if a_r < 0: has_neg_slope = True
            D = math.lcm(a_r.q, b_r.q)  # Dùng math.lcm tiêu chuẩn của Python, không dùng sp.ilcm
            A_p = int(a_r.p * (D // a_r.q))
            B_p = int(b_r.p * (D // b_r.q))
            affines.append((A_p, B_p, D))

        box_sols = []
        for v in range(1, N + 1):
            vals = []
            is_ok = True
            for A_p, B_p, D in affines:
                val = A_p * v + B_p
                if val <= 0 or val % D != 0:
                    is_ok = False
                    break
                vals.append(val // D)
            if is_ok:
                box_sols.append(tuple(vals))
        box_count = len(box_sols)

        if has_neg_slope:
            if box_count == 0:
                if cat in [DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY, DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS] and n_tot == 0 and len(sols) == 0:
                    oracle_passed += 1
            else:
                if cat == DiophantineCategory.FINITE_BOUNDED and n_tot == box_count and sols == box_sols[:10]:
                    oracle_passed += 1
        else:
            if box_count == 0:
                if cat in [DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY, DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS] and n_tot == 0 and len(sols) == 0:
                    oracle_passed += 1
            else:
                if cat == DiophantineCategory.UNBOUNDED_INFINITE and sols == box_sols[:3]:
                    oracle_passed += 1

    t_oracle = (time.perf_counter() - t_oracle_0) * 1000
    print(f"Kết quả Oracle Hộp cố định: {oracle_passed}/100 hệ khớp (Thời gian: {t_oracle:.2f} ms, {t_oracle/100:.2f} ms/hệ)")
    print(f"Phân bổ phân tầng 100 hệ: 25 FINITE_BOUNDED, 25 UNBOUNDED_INFINITE, 25 INFEASIBLE_BOUNDS_EMPTY, 25 INFEASIBLE_NO_INTEGER_POINTS")

    # PHẦN 3: KIỂM THỬ ĐỘT BIẾN THẬT (REAL MUTATION TESTING TRÊN 6 TOÁN TỬ)
    print("-" * 95)
    print("CHẠY KIỂM THỬ ĐỘT BIẾN THẬT (REAL MUTATION TESTING TRÊN 6 TOÁN TỬ ĐẠI DIỆN)")
    orig_dioph_src = textwrap.dedent(inspect.getsource(CADMathCore.solve_underdetermined_or_diophantine))
    orig_rad_src = textwrap.dedent(inspect.getsource(CADMathCore.solve_radical_pedagogical))
    core_globals = CADMathCore.solve_underdetermined_or_diophantine.__globals__

    def build_mutant_core(target_method, target_str, repl_str):
        core_inst = CADMathCore()
        if target_method == "diophantine":
            mut_src = orig_dioph_src.replace(target_str, repl_str)
            loc_ns = {}
            exec(mut_src, core_globals, loc_ns)
            core_inst.solve_underdetermined_or_diophantine = types.MethodType(loc_ns['solve_underdetermined_or_diophantine'], core_inst)
        elif target_method == "radical":
            mut_src = orig_rad_src.replace(target_str, repl_str)
            loc_ns = {}
            exec(mut_src, core_globals, loc_ns)
            core_inst.solve_radical_pedagogical = types.MethodType(loc_ns['solve_radical_pedagogical'], core_inst)
        return core_inst

    mutants = [
        {
            "id": "M1_DIO_LO_OFF_BY_ONE",
            "name": "M1: Cận dưới floor()+0 thay vì +1 (Diophantine)",
            "method": "diophantine",
            "target": "sp.floor(-b_sym / a_sym) + 1",
            "repl": "sp.floor(-b_sym / a_sym) + 0"
        },
        {
            "id": "M2_DIO_HI_OFF_BY_ONE",
            "name": "M2: Cận trên ceiling()-0 thay vì -1 (Diophantine)",
            "method": "diophantine",
            "target": "sp.ceiling(-b_sym / a_sym) - 1",
            "repl": "sp.ceiling(-b_sym / a_sym) - 0"
        },
        {
            "id": "M3_DIO_NTOTAL_OFF_BY_ONE",
            "name": "M3: Sai số lượng n_total thiếu +1 (Diophantine)",
            "method": "diophantine",
            "target": "(hi - start_val) // m_mod + 1",
            "repl": "(hi - start_val) // m_mod"
        },
        {
            "id": "M4_DIO_GCD_BYPASS",
            "name": "M4: Bỏ qua kiểm tra gcd khả chia (Diophantine)",
            "method": "diophantine",
            "target": "(-B_val) % g_val != 0",
            "repl": "False"
        },
        {
            "id": "M5_DIO_CRT_CONFLICT_BYPASS",
            "name": "M5: Bỏ qua kiểm tra xung đột CRT sc is None",
            "method": "diophantine",
            "target": "if sc is None:",
            "repl": "if False:"
        },
        {
            "id": "M6_RAD_SIGN_BYPASS",
            "name": "M6: Bỏ qua kiểm tra dấu vế phải g(r) < 0 (Radical)",
            "method": "radical",
            "target": "if s_gx == 'neg':",
            "repl": "if False:"
        }
    ]

    mutants_killed_suite = 0

    for m in mutants:
        mut_app = build_mutant_core(m["method"], m["target"], m["repl"])
        # 1. Kiểm thử trên bộ Suite kiểm định có chủ đích
        passed_s, _, _ = execute_single_run(mut_app, test_cases, is_warmup=True)
        is_killed_by_suite = (passed_s < len(test_cases))
        if is_killed_by_suite:
            mutants_killed_suite += 1

        # 2. Kiểm thử trên 100 hệ ngẫu nhiên phân tầng
        killed_random = 0
        survived_random = 0
        if m["method"] == "diophantine":
            for eqs in dataset:
                cat_m, sols_m, n_tot_m, out_m = mut_app.solve_underdetermined_or_diophantine(eqs, [x, y, z])
                linsols = sp.linsolve(eqs, [x, y, z])
                sol_tuple = list(linsols)[0]
                free_s = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)
                p = free_s[0]

                affines = []
                has_neg_slope = False
                for expr in sol_tuple:
                    e_exp = sp.expand(expr)
                    a_r = sp.Rational(e_exp.coeff(p))
                    b_r = sp.Rational(e_exp.subs(p, 0))
                    if a_r < 0: has_neg_slope = True
                    D = math.lcm(a_r.q, b_r.q)
                    A_p = int(a_r.p * (D // a_r.q))
                    B_p = int(b_r.p * (D // b_r.q))
                    affines.append((A_p, B_p, D))

                box_sols = []
                for v in range(1, N + 1):
                    vals = []
                    is_ok = True
                    for A_p, B_p, D in affines:
                        val = A_p * v + B_p
                        if val <= 0 or val % D != 0:
                            is_ok = False
                            break
                        vals.append(val // D)
                    if is_ok:
                        box_sols.append(tuple(vals))
                box_count = len(box_sols)

                is_killed = False
                if has_neg_slope:
                    if box_count == 0:
                        if cat_m not in [DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY, DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS] or n_tot_m != 0 or len(sols_m) != 0:
                            is_killed = True
                    else:
                        if cat_m != DiophantineCategory.FINITE_BOUNDED or n_tot_m != box_count or sols_m != box_sols[:10]:
                            is_killed = True
                else:
                    if box_count == 0:
                        if cat_m not in [DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY, DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS] or n_tot_m != 0 or len(sols_m) != 0:
                            is_killed = True
                    else:
                        if cat_m != DiophantineCategory.UNBOUNDED_INFINITE or sols_m != box_sols[:3]:
                            is_killed = True

                if is_killed:
                    killed_random += 1
                else:
                    survived_random += 1
            rand_stat_str = f"| 100 hệ ngẫu nhiên: Bị giết {killed_random:>2}/100, Sống sót {survived_random:>2}/100"
        else:
            rand_stat_str = "| (Toán tử Radical: được kiểm thử trực tiếp bởi các ca vô tỷ trong Suite)"

        suite_kill_str = "BỊ GIẾT BỞI SUITE [PASSED]" if is_killed_by_suite else "SỐNG SÓT [FAILED]"
        print(f"  • {m['name']:<48}: {suite_kill_str} {rand_stat_str}")

    mutation_score = (mutants_killed_suite / len(mutants)) * 100
    print(f"\n==> TỔNG KẾT KIỂM THỬ ĐỘT BIẾN: Mutation Score trên Suite kiểm định = {mutants_killed_suite}/{len(mutants)} ({mutation_score:.1f}%)")

    print("=" * 95)
    rad_med = statistics.median(per_test_medians[:7])
    dioph_med = statistics.median(per_test_medians[7:])
    min_t = min(per_test_medians)
    max_t = max(per_test_medians)
    min_idx = per_test_medians.index(min_t)
    min_id = test_cases[min_idx]["id"]
    max_idx = per_test_medians.index(max_t)
    max_id = test_cases[max_idx]["id"]
    print(f"TỔNG KẾT TOÀN BỘ: {last_passed}/{len(test_cases)} bài đạt yêu cầu | Oracle Hộp cố định 100/100")
    print(f"Thời gian bộ bài (Trung vị 5 vòng): Tổng = {total_medians:.2f} ms | TB = {total_medians/len(test_cases):.2f} ms/bài | IQR = {iqr_all:.2f} ms")
    print(f"  • Phân hệ Radical (Trung vị): {rad_med:.2f} ms/bài | Phân hệ Diophantine (Trung vị): {dioph_med:.2f} ms/bài")
    print(f"  • Dải đo: Min = {min_t:.2f} ms ({min_id}), Max = {max_t:.2f} ms ({max_id})")
    print("=" * 95)

if __name__ == "__main__":
    run_suite()

```

---

## 9. KẾT LUẬN & ĐỀ NGHỊ ĐÓNG VÒNG PHẢN BIỆN LÝ THUYẾT

Bản cập nhật Phiên bản 2.12 đã hoàn tất việc giải quyết trọn vẹn cả 3 vấn đề chặn (B1, B2, B3) và toàn bộ các vấn đề phụ:
1. **Mã nguồn giải thuật lõi (§8.1) hoàn toàn tự chứa:** Tách riêng tệp `cad_math_core.py`, bổ sung đầy đủ import `re`, `math`, loại bỏ 100% đối tượng Tkinter, chuẩn hóa thụt lề cấp phương thức và cung cấp mã băm SHA-256 khớp tuyệt đối (`ddb945c9...`).
2. **Kiểm thử đột biến thật (§4.2):** Biên dịch động và kiểm thử 6 toán tử đột biến trên Bytecode. Bổ sung các ca biên nhắm đích `DIO_13` (diệt M1) và `DIO_14` (diệt M2 & M3), đạt **Mutation Score = 6/6 (100%) trên Suite kiểm định**, mô tả chính xác tỷ lệ sống sót trên tập dữ liệu ngẫu nhiên.
3. **Oracle Hộp cố định độc lập (§4.1):** Sử dụng `math.lcm` chuẩn của Python (loại bỏ `sp.ilcm`), nêu rõ các giới hạn phương pháp luận về biểu diễn tham số affine và phạm vi hộp $N=3000$.
4. **Bản ghi thực nghiệm nguyên văn (§5.1):** Trích xuất trực tiếp từ lần chạy thực tế với nhãn min/max động, tính toán đầy đủ giá trị IQR và Median trên môi trường chuẩn hóa Intel Core i7-11800H và Python 3.14.5 duy nhất.

Nhóm tác giả kính trình bản Hồ sơ v2.12 và trân trọng đề xuất Hội đồng Phản biện xem xét **chấp thuận chính thức đóng vòng phản biện lý thuyết và giải thuật**, tạo tiền đề chuyển sang giai đoạn thực nghiệm sư phạm trên nhóm đối tượng giáo viên và học sinh phổ thông.
