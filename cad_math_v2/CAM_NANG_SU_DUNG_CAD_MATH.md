# Hướng Dẫn Sử Dụng CAD Math Studio
## Phần mềm giải toán đa năng và vẽ đồ thị hàm số

---

### Mục lục
1. [Giới thiệu](#1-giới-thiệu)
2. [Giao diện phần mềm](#2-giao-diện-phần-mềm)
   - [2.1 Thanh menu trên cùng](#21-thanh-menu-trên-cùng)
   - [2.2 Dải nút ký hiệu toán học (Ribbon)](#22-dải-nút-ký-hiệu-toán-học-ribbon)
   - [2.3 Hệ thống 6 tab giải toán](#23-hệ-thống-6-tab-giải-toán)
   - [2.4 Khung hiển thị lời giải và khung vẽ đồ thị](#24-khung-hiển-thị-lời-giải-và-khung-vẽ-đồ-thị)
3. [Cách dùng từng chức năng](#3-cách-dùng-từng-chức-năng)
   - [3.1 Tab 1: Phương trình, bất phương trình và hệ phương trình](#31-tab-1-phương-trình-bất-phương-trình-và-hệ-phương-trình)
   - [3.2 Tab 2: Tìm giá trị lớn nhất, nhỏ nhất và bất đẳng thức](#32-tab-2-tìm-giá-trị-lớn-nhất-nhỏ-nhất-và-bất-đẳng-thức)
   - [3.3 Tab 3: Đạo hàm, tích phân và giới hạn](#33-tab-3-đạo-hàm-tích-phân-và-giới-hạn)
   - [3.4 Tab 4: Tính toán ma trận](#34-tab-4-tính-toán-ma-trận)
   - [3.5 Tab 5: Xác suất và thống kê](#35-tab-5-xác-suất-và-thống-kê)
   - [3.6 Tab 6: Khảo sát và vẽ đồ thị hàm số](#36-tab-6-khảo-sát-và-vẽ-đồ-thị-hàm-số)
   - [3.7 Cách gõ công thức toán học](#37-cách-gõ-công-thức-toán-học)
   - [3.8 Xuất ảnh đồ thị, sao chép và xuất báo cáo HTML](#38-xuất-ảnh-đồ-thị-sao-chép-và-xuất-báo-cáo-html)
4. [Bảng phím tắt toàn tập](#4-bảng-phím-tắt-toàn-tập)
5. [Một số lưu ý khi sử dụng](#5-một-số-lưu-ý-khi-sử-dụng)

---

### 1. Giới thiệu

**CAD Math Studio** là phần mềm giải toán máy tính và vẽ đồ thị hàm số. Phần mềm giúp học sinh và giáo viên giải quyết các bài toán đại số, giải tích, ma trận và thống kê với lời giải từng bước rõ ràng.

Các tính năng chính:
- Giải phương trình bậc cao, bất phương trình, hệ phương trình, bài toán chứa tham số $m$ và phương trình số phức.
- Tìm giá trị lớn nhất, nhỏ nhất của hàm số và kiểm tra bất đẳng thức.
- Tính đạo hàm, tích phân từng bước, giới hạn và chuỗi số.
- Các phép tính ma trận: cộng trừ nhân ma trận, tính định thức $\det$, tìm ma trận nghịch đảo, giải hệ phương trình ma trận.
- Tính tổ hợp, chỉnh hợp, hoán vị và các chỉ số thống kê (trung bình, phương sai, độ lệch chuẩn, biểu đồ hộp boxplot).
- Khảo sát sự biến thiên và vẽ đồ thị hàm số trên hệ trục tọa độ Oxy.
- Lời giải hiển thị chi tiết, công thức toán dạng căn thức tự nhiên và phân số dễ đọc.
- Xuất bài làm ra file ảnh hoặc file web HTML có công thức đẹp.

---

### 2. Giao diện phần mềm

Giao diện được bố trí gọn gàng, chia thành các khu vực:

```
+---------------------------------------------------------------------------------------+
|  CAD Math Studio v2.1                                                     [_] [口] [X]|
+---------------------------------------------------------------------------------------+
| Tệp (File) | Chỉnh sửa (Edit) | Xem (View) | Chuyên đề | Công cụ | Giao diện | Trợ giúp|
+---------------------------------------------------------------------------------------+
| DẢI NÚT TOÁN (RIBBON): [√] [x²] [x³] [π] [≤] [≥] [≠] [∫] [d/dx] [lim] [∑] [∞] [i]    |
+---------------------------------------------------------------------------------------+
| [1. Phương trình] [2. Cực trị] [3. Giải tích] [4. Ma trận] [5. Thống kê] [6. Đồ thị]  |
+---------------------------------------------------+-----------------------------------+
| KHUNG NHẬP LIỆU & LỜI GIẢI CHI TIẾT               | KHUNG ĐỒ THỊ TƯƠNG TÁC (NẾU CÓ)   |
|                                                   |                                   |
| - Ô nhập biểu thức toán học                       | - Đồ thị hàm số y = f(x)          |
| - Các nút giải: [ Giải chi tiết ] [ Vẽ đồ thị ]   | - Điểm cực trị, tiệm cận          |
| - Khung hiển thị các bước giải từng bước          | - Phóng to, thu nhỏ, lưu ảnh đồ thị|
| - Công thức toán viết dạng tự nhiên               |                                   |
+---------------------------------------------------+-----------------------------------+
| Sẵn sàng | Ngôn ngữ: Tiếng Việt | Cỡ chữ: 100% | Phím tắt F1 để xem hướng dẫn         |
+---------------------------------------------------------------------------------------+
```

#### 2.1 Thanh menu trên cùng
- **Tệp (File):** Mở file bài toán (`Ctrl+O`), lưu bài giải ra file (`Ctrl+S`), lưu ảnh đồ thị (`Ctrl+Shift+S`), xuất báo cáo HTML (`Ctrl+P`), thoát (`Ctrl+Q`).
- **Chỉnh sửa (Edit):** Sao chép bài giải (`Ctrl+C`), xóa nội dung tab đang chọn (`Ctrl+L`).
- **Xem (View):** Phóng to chữ bài giải (`Ctrl++`), thu nhỏ chữ (`Ctrl+-`), đặt lại cỡ chữ 100% (`Ctrl+0`).
- **Chuyên đề:** Mở nhanh các phần toán phổ thông hoặc công cụ toán nâng cao.
- **Công cụ (Tools):** Bật dải ký hiệu Ribbon, kiểm định tính toán, giải toán AI (`F5`).
- **Giao diện (Themes):** Đổi màu giao diện (Sáng, Xanh hiện đại, Kỹ thuật cổ điển, Tối).
- **Ngôn ngữ (Language):** Đổi giữa Tiếng Việt và English.
- **Trợ giúp (Help):** Mở hướng dẫn sử dụng (`F1`), mở hướng dẫn bản web HTML, xem bảng phím tắt, hướng dẫn gõ cú pháp, thông tin phần mềm.

#### 2.2 Dải nút ký hiệu toán học (Ribbon)
Nằm ngay phía trên các ô nhập liệu, gồm các nút bấm nhanh: căn bậc hai $\sqrt{}$, lũy thừa $x^2, x^3, x^y$, hằng số $\pi, e$, các dấu $\le, \ge, \ne$, đạo hàm $\frac{d}{dx}$, tích phân $\int$, giới hạn $\lim$, vô cực $\infty$, đơn vị ảo $i$. Bấm nút nào thì ký hiệu đó sẽ tự động chèn vào ô nhập con trỏ đang đứng.

#### 2.3 Hệ thống 6 tab giải toán
Cho phép bạn chuyển đổi linh hoạt giữa 6 nhóm bài toán khác nhau mà không làm mất dữ liệu của các tab còn lại.

#### 2.4 Khung hiển thị lời giải và khung vẽ đồ thị
- Bên trái là khung hiển thị lời giải từng bước, có kết luận rõ ràng.
- Bên phải (ở các tab khảo sát đồ thị, thống kê) là khung vẽ đồ thị tương tác, có thể lăn chuột để phóng to thu nhỏ trục tọa độ.

---

### 3. Cách dùng từng chức năng

#### 3.1 Tab 1: Phương trình, bất phương trình và hệ phương trình
1. Nhấp vào tab **1. Phương trình**.
2. Nhập phương trình hoặc bất phương trình vào ô văn bản:
   - *Phương trình một ẩn:* `x^2 - 5x + 6 = 0` hoặc `sqrt(2x + 1) = x - 1`
   - *Bất phương trình:* `x^2 - 3x + 2 <= 0` hoặc `(x - 1)/(x + 2) > 0`
   - *Phương trình chứa tham số m:* `x^2 - 2*(m - 1)*x + m + 5 = 0` (phần mềm sẽ tìm điều kiện của $m$ để có nghiệm, có 2 nghiệm phân biệt...)
   - *Phương trình số phức:* `(1 + 2i)*z + 3 - i = 0` (sử dụng $i$ là đơn vị ảo, $z$ là ẩn số phức)
   - *Hệ phương trình:* Gõ mỗi phương trình trên một dòng hoặc cách nhau bởi dấu chấm phẩy `;`
     ```text
     2x + y = 5
     x - 3y = -1
     ```
3. Bấm nút **[ Giải Chi Tiết ]** (hoặc nhấn `Enter`). Lời giải từng bước sẽ hiện ra phía dưới.

#### 3.2 Tab 2: Tìm giá trị lớn nhất, nhỏ nhất và bất đẳng thức
1. Nhấp vào tab **2. Cực trị**.
2. Ô trên: Nhập biểu thức mục tiêu cần tìm giá trị lớn nhất / nhỏ nhất, ví dụ `P = x^2 + y^2 - 4x + 2y`.
3. Ô dưới: Nhập điều kiện ràng buộc (nếu có), ví dụ `x + 2y = 4` hoặc `x >= 0, y >= 0`. Nếu không có điều kiện, để trống.
4. Bấm **[ Tìm Cực Trị ]**. Phần mềm sẽ phân tích đạo hàm riêng, điểm dừng và đưa ra giá trị lớn nhất (GTLN), giá trị nhỏ nhất (GTNN) kèm tọa độ điểm đạt được.

#### 3.3 Tab 3: Đạo hàm, tích phân và giới hạn
1. Nhấp vào tab **3. Giải tích**.
2. Nhập biểu thức $f(x)$, ví dụ `x^3 - 3x^2 + 2` hoặc `sin(x)*cos(x)`.
3. Chọn phép tính mong muốn:
   - **Tính đạo hàm:** Bấm `[ Đạo hàm f'(x) ]` (có hỗ trợ đạo hàm cấp 1, cấp 2 hoặc đạo hàm riêng theo biến $x, y, z$).
   - **Tính tích phân bất định:** Bấm `[ Tích phân ∫ f(x)dx ]`.
   - **Tính tích phân xác định:** Nhập cận dưới và cận trên vào 2 ô bên cạnh (ví dụ cận từ $0$ đến $1$), rồi bấm tính.
   - **Tính giới hạn:** Chọn ẩn tiến về giá trị nào (ví dụ $x \to 0$, $x \to \infty$) rồi bấm `[ Giới hạn lim ]`.

#### 3.4 Tab 4: Tính toán ma trận
1. Nhấp vào tab **4. Ma trận**.
2. Nhập ma trận theo từng dòng, các phần tử cách nhau bằng dấu cách hoặc dấu phẩy:
   - *Ví dụ Ma trận A (cỡ 3x3):*
     ```text
     1  2 -1
     0  3  4
     2 -1  1
     ```
3. Các phép tính có sẵn:
   - Tính định thức: Bấm `[ Định thức det(A) ]`.
   - Tìm ma trận nghịch đảo: Bấm `[ Nghịch đảo A⁻¹ ]`.
   - Chuyển vị: Bấm `[ Chuyển vị Aᵀ ]`.
   - Phép nhân hai ma trận: Nhập thêm ma trận B rồi bấm `[ A × B ]`.
   - Giải hệ phương trình ma trận $AX = B$: Bấm `[ Giải AX = B ]`.

#### 3.5 Tab 5: Xác suất và thống kê
1. Nhấp vào tab **5. Thống kê**.
2. **Phần Tổ hợp - Xác suất:**
   - Nhập $n$ và $k$ để tính nhanh: chỉnh hợp $A_n^k$, tổ hợp $C_n^k$, hoán vị $P_n = n!$.
3. **Phần Thống kê mô tả:**
   - Nhập dãy số liệu mẫu, cách nhau bởi dấu phẩy hoặc khoảng trắng: `12, 15, 14, 18, 20, 15, 16, 22`.
   - Bấm **[ Phân tích thống kê ]**.
   - Phần mềm sẽ tính: Số trung bình $\bar{x}$, Trung vị $M_e$, Mốt $M_o$, Tứ phân vị $Q_1, Q_2, Q_3$, Phương sai $s^2$, Độ lệch chuẩn $s$.
   - Đồng thời tự động vẽ biểu đồ phân bố và biểu đồ hộp (Boxplot) trực quan ở khung bên cạnh.

#### 3.6 Tab 6: Khảo sát và vẽ đồ thị hàm số
1. Nhấp vào tab **6. Đồ thị**.
2. Nhập hàm số cần vẽ, ví dụ `y = x^3 - 3x + 1` hoặc `y = (2x + 1)/(x - 1)`.
3. Bấm **[ Khảo Sát & Vẽ Đồ Thị ]**.
4. Kết quả gồm hai phần:
   - *Khảo sát:* Tập xác định, đạo hàm $y'$, bảng xét dấu, các điểm cực đại/cực tiểu, tiệm cận đứng, tiệm cận ngang.
   - *Đồ thị:* Vẽ đường cong hàm số trên mặt phẳng tọa độ Oxy, đánh dấu rõ các điểm cực trị và đường tiệm cận nét đứt.
5. Thao tác trên đồ thị:
   - Lăn con lăn chuột trên đồ thị để phóng to hoặc thu nhỏ khoảng xem.
   - Bấm nút **[ Lưu ảnh đồ thị ]** để lưu hình ra file PNG.

#### 3.7 Cách gõ công thức toán học
Bạn có thể gõ công thức bằng bàn phím thông thường một cách rất tự nhiên:
- Dấu nhân: Có thể bỏ qua dấu nhân, ví dụ gõ `2x`, `x*y` hoặc `x y`, `3(x - 1)`.
- Lũy thừa: Dùng dấu `^`, ví dụ `x^2`, `(x+1)^3`.
- Căn bậc hai: Gõ `sqrt(x)` hoặc `\sqrt{x}`. Căn bậc ba gõ `cbrt(x)` hoặc `root(x, 3)`.
- Phân số: Gõ `(a + b)/(c + d)` hoặc `\frac{a+b}{c+d}`.
- Giá trị tuyệt đối: Gõ `|x - 2|` hoặc `abs(x - 2)`.
- Lượng giác: `sin(x)`, `cos(x)`, `tan(x)`, `cot(x)`.
- Số pi: Gõ `pi` hoặc bấm nút $\pi$ trên dải Ribbon.
- Vô cực: Gõ `oo` (hai chữ o thường) hoặc `infty`.

#### 3.8 Xuất ảnh đồ thị, sao chép và xuất báo cáo HTML
- **Sao chép lời giải (`Ctrl+C`):** Bấm nút hoặc nhấn `Ctrl+C` để copy toàn bộ lời giải chi tiết vào Clipboard, tiện dán vào Word.
- **Lưu ảnh đồ thị (`Ctrl+Shift+S`):** Lưu phần đồ thị bên phải ra file ảnh PNG chất lượng cao.
- **Xuất báo cáo HTML (`Ctrl+P`):** Xuất toàn bộ bài toán, lời giải và hình vẽ ra một file web HTML tự chứa, mở được trên mọi máy tính và in ra giấy dễ dàng.

---

### 4. Bảng phím tắt toàn tập

| Phím tắt | Tên chức năng | Mô tả |
| :--- | :--- | :--- |
| **`F1`** | **Hướng dẫn sử dụng** | Mở bảng hướng dẫn sử dụng và phím tắt |
| **`F5`** | **Giải toán AI** | Kích hoạt bộ phân tích AI cho bài toán đang nhập |
| **`Ctrl + O`** | **Mở file** | Mở tệp bài toán đã lưu từ trước |
| **`Ctrl + S`** | **Lưu bài giải** | Lưu bài giải chi tiết ra file văn bản |
| **`Ctrl + Shift + S`**| **Lưu ảnh đồ thị** | Lưu hình đồ thị hiện tại ra file ảnh PNG |
| **`Ctrl + P`** | **Xuất báo cáo** | Xuất báo cáo bài giải ra file HTML để in ấn |
| **`Ctrl + C`** | **Sao chép** | Sao chép nội dung bài giải tab hiện tại vào bộ nhớ tạm |
| **`Ctrl + V`** | **Dán** | Dán công thức vào ô đang nhập |
| **`Ctrl + L`** | **Xóa trắng tab** | Xóa nhanh dữ liệu nhập và kết quả trên tab đang mở |
| **`Ctrl + +`** hoặc **`+`** | **Phóng to chữ** | Tăng kích thước chữ bài giải |
| **`Ctrl + -`** hoặc **`-`** | **Thu nhỏ chữ** | Giảm kích thước chữ bài giải |
| **`Ctrl + 0`** | **Cỡ chữ ban đầu** | Đặt lại cỡ chữ bài giải về mức 100% |
| **`Ctrl + Q`** | **Thoát** | Đóng phần mềm |

---

### 5. Một số lưu ý khi sử dụng

1. **Khi chép lời giải vào tài liệu Word:**
   - Bạn chỉ cần bấm `Ctrl+C` để sao chép bài giải. Lời giải đã được định dạng rõ ràng từng bước, có kết luận nghiệm số học.
2. **Khi nhập hệ phương trình hoặc ma trận:**
   - Bạn chỉ cần xuống dòng bình thường cho mỗi phương trình hoặc mỗi hàng ma trận, không cần phải thêm các dấu ngoặc phức tạp.
3. **Khi đồ thị bị lệch khỏi vùng muốn xem:**
   - Bạn có thể điều chỉnh 2 ô $x_{min}$ và $x_{max}$ ở dưới đồ thị (ví dụ từ $-5$ đến $5$) rồi bấm Vẽ lại, hoặc dùng con lăn chuột để zoom trực tiếp trên hình.
4. **Đổi ngôn ngữ Tiếng Anh:**
   - Vào menu `Ngôn ngữ -> English`, toàn bộ giao diện, tên 6 tab và bảng kết quả sẽ chuyển sang tiếng Anh chuẩn để học tập các chương trình song ngữ.

---
*CAD Math Studio - Phần mềm giải toán và vẽ đồ thị học tập.*
