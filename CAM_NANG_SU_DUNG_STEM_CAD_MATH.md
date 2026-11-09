# CẨM NANG HƯỚNG DẪN SỬ DỤNG TOÀN TẬP
## BỘ CÔNG CỤ TOÁN HỌC STEM SUITE (CAD MATH STUDIO v2.1 & GEOSOLVER 2D CAD)

---

### MỤC LỤC
1. [GIỚI THIỆU TỔNG QUAN](#1-giới-thiệu-tổng-quan)
2. [PHẦN I: CẨM NANG SỬ DỤNG CAD MATH STUDIO v2.1](#2-phần-i-cẩm-nang-sử-dụng-cad-math-studio-v21)
   - [2.1 Giao diện & Chuyển đổi ngôn ngữ](#21-giao-diện--chuyển-đổi-ngôn-ngữ)
   - [2.2 Tab 1: Phương trình, Bất phương trình & Hệ (Tham số m, Số phức)](#22-tab-1-phương-trình-bất-phương-trình--hệ-tham-số-m-số-phức)
   - [2.3 Tab 2: Cực trị VDC & Bất đẳng thức Đa biến](#23-tab-2-cực-trị-vdc--bất-đẳng-thức-đa-biến)
   - [2.4 Tab 3: Vi tích phân & Giải tích đa biến](#24-tab-3-vi-tích-phân--giải-tích-đa-biến)
   - [2.5 Tab 4: Đại số tuyến tính & Ma trận](#25-tab-4-đại-số-tuyến-tính--ma-trận)
   - [2.6 Tab 5: Tổ hợp - Xác suất & Thống kê](#26-tab-5-tổ-hợp---xác-suất--thống-kê)
   - [2.7 Tab 6: Khảo sát hàm số & Đồ thị Oxy](#27-tab-6-khảo-sát-hàm-số--đồ-thị-oxy)
   - [2.8 Hộp nhập công thức toán học (MathFormulaCanvas)](#28-hộp-nhập-công-thức-toán-học-mathformulacanvas)
   - [2.9 Xuất kết quả, Sao chép ảnh & Báo cáo kỹ thuật](#29-xuất-kết-quả-sao-chép-ảnh--báo-cáo-kỹ-thuật)
3. [PHẦN II: CẨM NANG SỬ DỤNG GEOSOLVER 2D CAD STUDIO](#3-phần-ii-cẩm-nang-sử-dụng-geosolver-2d-cad-studio)
   - [3.1 Không gian làm việc & Thao tác điều hướng CAD](#31-không-gian-làm-việc--thao-tác-điều-hướng-cad)
   - [3.2 Chi tiết 4 thanh công cụ Ribbon](#32-chi-tiết-4-thanh-công-cụ-ribbon)
   - [3.3 Công cụ vẽ Elip thế hệ mới](#33-công-cụ-vẽ-elip-thế-hệ-mới)
   - [3.4 Cơ chế Tự động phát hiện quan hệ hình học (Deep Invariant Detection)](#34-cơ-chế-tự-động-phát-hiện-quan-hệ-hình-học-deep-invariant-detection)
   - [3.5 Khung Trình bày bài toán & Các nút ký hiệu toán học](#35-khung-trình-bày-bài-toán--các-nút-ký-hiệu-toán-học)
   - [3.6 Cơ chế Ẩn/Hiện đối tượng (Ghost Mode) & Khôi phục](#36-cơ-chế-ẩnhiện-đối-tượng-ghost-mode--khôi-phục)
   - [3.7 Xuất ảnh bản vẽ CAD & Xuất báo cáo HTML](#37-xuất-ảnh-bản-vẽ-cad--xuất-báo-cáo-html)
   - [3.8 Hỗ trợ giải toán: Thuần thuật toán Python & AI Support](#38-hỗ-trợ-giải-toán-thuần-thuật-toán-python--ai-support)
4. [PHẦN III: BẢNG TRA CỨU PHÍM TẮT TOÀN TẬP (KEYBOARD SHORTCUTS)](#4-phần-iii-bảng-tra-cứu-phím-tắt-toàn-tập-keyboard-shortcuts)
5. [PHẦN IV: MẸO & KINH NGHIỆM TỐI ƯU HÓA THAO TÁC (PRO TIPS)](#5-phần-iv-mẹo--kinh-nghiệm-tối-ưu-hóa-thao-tác-pro-tips)

---

### 1. GIỚI THIỆU TỔNG QUAN

Hệ thống **STEM Mathematics Suite** là bộ giải pháp công nghệ toán học hiện đại gồm 2 phân hệ chuyên sâu kết hợp chặt chẽ:
1. **CAD Math Studio v2.1**: Phần mềm chuyên giải quyết toàn diện Đại số, Giải tích, Ma trận, Thống kê và Khảo sát hàm số với giao diện đa tab khoa học, hỗ trợ biểu diễn công thức LaTeX và đồ thị tương tác cao.
2. **GeoSolver 2D CAD Studio**: Phần mềm mô hình hóa hình học phẳng động (Dynamic Geometry) kết hợp phân tích đại số hình thức. Cho phép dựng hình chuẩn CAD cơ khí, tự động nhận diện các quan hệ bất biến (cân, đều, vuông, song song, trung điểm) và giải bài toán hình học tự động bằng thuật toán hình thức SymPy kết hợp AI Support.

---

### 2. PHẦN I: CẨM NANG SỬ DỤNG CAD MATH STUDIO v2.1

#### 2.1 Giao diện & Chuyển đổi ngôn ngữ
- **Màn hình chính**: Gồm thanh menu hệ thống, thanh nút thao tác nhanh, khung nhập công thức toán học (`MathFormulaCanvas`), hệ thống 6 tab chuyên đề và khu vực đồ thị tương tác Matplotlib bên phải.
- **Chuyển đổi ngôn ngữ**: 
  - Menu `Ngôn ngữ (Language)` -> chọn `🇻🇳 Tiếng Việt` hoặc `🇬🇧 English`.
  - Toàn bộ giao diện, tiêu đề tab, nhãn nút và bảng hướng dẫn cú pháp sẽ cập nhật ngay lập tức mà không làm mất dữ liệu đang làm việc.

#### 2.2 Tab 1: Phương trình, Bất phương trình & Hệ (Tham số m, Số phức)
- **Chức năng chính**: Giải phương trình bậc cao, bất phương trình đại số, căn thức phức tạp, bài toán chứa tham số $m$ và phương trình số phức.
- **Quy tắc nhập liệu tự nhiên**:
  - Dấu bất đẳng thức: Dùng `<=`, `>=`, `<`, `>`, `!=` hoặc mã LaTeX `\le`, `\ge`.
  - Phép nhân ngầm định: Viết liền thuận tiện như sách giáo khoa, ví dụ: `2x`, `x sqrt(y)`, `(x+1)(x-2)`.
  - Căn thức: `sqrt(x)`, `căn(x)`, `\sqrt{x}`, `\sqrt[3]{x}`, `\sqrt[4]{x-1}`.
  - Trị tuyệt đối & Lũy thừa: `|x|`, `Abs(x - 2)`, `x^2`, `e^(2x)`.
  - Tham số $m$: Nhập trực tiếp biểu thức chứa $m$, ví dụ: `x^2 - 2(m-1)x + m + 5 >= 0` hoặc `sqrt(x-1) + sqrt(5-x) <= m`. Phần mềm sẽ tự động cô lập tham số, lập bảng biến thiên hàm số phụ và đưa ra điều kiện chính xác của $m$.
  - Hệ phương trình/bất phương trình: Nhập các phương trình trên nhiều dòng khác nhau hoặc phân tách bằng dấu chấm phẩy `;`.
  - Số phức: Ký hiệu đơn vị ảo là `i`. Hỗ trợ số phức liên hợp (`\bar{z}` hoặc `z_bar`). Ví dụ: `(1 + 2i)z + 3 - i = 0`.
- **Thao tác**: Nhấn nút `[Giải phương trình / BPT]` hoặc phím `Enter` / `F5`.

#### 2.3 Tab 2: Cực trị VDC & Bất đẳng thức Đa biến
- **Chức năng chính**: Tìm giá trị lớn nhất (GTLN / Max), giá trị nhỏ nhất (GTNN / Min) của biểu thức đa biến với các điều kiện ràng buộc đẳng thức hoặc bất đẳng thức.
- **Cách thức hoạt động**:
  - Nhập hàm mục tiêu $f(x, y, z)$ và danh sách ràng buộc (mỗi ràng buộc một dòng).
  - Thuật toán phối hợp: Giải tích hình thức (SymPy với phương pháp nhân tử Lagrange / ma trận Hessian) kết hợp thuật toán tối ưu hóa số học Nelder-Mead đa điểm khởi tạo.
  - Bản đồ đường mức (Contour Plot): Trực quan hóa miền nghiệm và các điểm dừng, cực trị trên không gian 2D Oxy.

#### 2.4 Tab 3: Vi tích phân & Giải tích đa biến
- **Chức năng chính**:
  - Tính đạo hàm cấp cao, đạo hàm riêng phần ($\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}, \frac{\partial f}{\partial z}$).
  - Tính tích phân xác định và nguyên hàm bất định (hỗ trợ tích phân từng phần, đổi biến số).
  - Khai triển chuỗi Taylor / Maclaurin tại điểm $x_0$ với bậc tùy chọn.
  - Tính giới hạn (Limit) một bên và hai bên ($\lim_{x \to x_0^+}, \lim_{x \to \infty}$).

#### 2.5 Tab 4: Đại số tuyến tính & Ma trận
- **Chức năng chính**: Tính toán ma trận số thực và ma trận chứa tham số.
- **Quy tắc nhập ma trận**:
  - Mỗi hàng trên một dòng, các phần tử cách nhau bởi dấu cách hoặc dấu phẩy `,`.
  - Ví dụ:
    ```
    1  2  -1
    0  3   4
    2 -1   5
    ```
- **Các phép toán hỗ trợ**:
  - Định thức ma trận: $\det(A)$ với các bước khai triển Laplace.
  - Ma trận nghịch đảo: $A^{-1}$ bằng ma trận phụ hợp hoặc biến đổi Gauss-Jordan.
  - Hạng ma trận: $\text{rank}(A)$ đưa về ma trận bậc thang.
  - Tích ma trận: $A \times B$.
  - Giải hệ phương trình tuyến tính dạng ma trận: $A \cdot X = B$.

#### 2.6 Tab 5: Tổ hợp - Xác suất & Thống kê
- **Chức năng chính**: Phân tích thống kê mô tả toàn diện cho mẫu số liệu và giải toán tổ hợp.
- **Cách dùng**:
  - Nhập mẫu số liệu rời rạc (cách nhau bởi dấu phẩy hoặc dấu cách): `12, 15, 18, 14, 22, 19, 15, 24, 30`.
  - Tự động tính: Giá trị trung bình ($\bar{x}$), Trung vị ($\text{Me}$), Mốt ($\text{Mo}$), Phương sai ($s^2$), Độ lệch chuẩn ($s$), Khoảng biến thiên ($R$), Khoảng tứ phân vị ($\Delta_Q = Q_3 - Q_1$).
  - Đồ thị trực quan: Tự động vẽ Biểu đồ tần số (Histogram) và Biểu đồ hộp (Boxplot) có đánh dấu giá trị ngoại lai.

#### 2.7 Tab 6: Khảo sát hàm số & Đồ thị Oxy
- **Chức năng chính**: Khảo sát đầy đủ các bước của hàm số 1 biến $y = f(x)$ theo chương trình Toán phổ thông:
  - Tập xác định và tính chẵn / lẻ / tuần hoàn.
  - Đạo hàm $y'$, tìm các điểm tới hạn, lập bảng biến thiên.
  - Điểm cực đại, cực tiểu, giá trị cực trị.
  - Đạo hàm cấp hai $y''$, điểm uốn, khoảng lồi lõm của đồ thị.
  - Các đường tiệm cận: Tiệm cận đứng, tiệm cận ngang, tiệm cận xiên.
  - Viết phương trình tiếp tuyến tại tiếp điểm hoặc khi biết hệ số góc $k$.
  - Vẽ đồ thị hàm số sắc nét, tự động đánh dấu các điểm đặc biệt (cực trị, điểm uốn, giao điểm trục tọa độ).

#### 2.8 Hộp nhập công thức toán học (MathFormulaCanvas)
- Khung hiển thị thời gian thực phía trên cửa sổ:
  - Tự động chuyển đổi công thức bạn gõ thành dạng MathText/LaTeX chuẩn xuất bản.
  - Nút **[Copy LaTeX]**: Chép mã nguồn LaTeX vào Clipboard.
  - Nút **[Copy Text]**: Chép biểu thức toán dạng văn bản đơn giản.
  - Nút **[📋 Chép Ảnh]**: Chụp và dán công thức toán độ phân giải cao trực tiếp vào bộ nhớ tạm Windows (dán ngay vào Word/PowerPoint bằng `Ctrl + V`).
  - Nút **[💾 Lưu Ảnh]**: Lưu ảnh công thức dưới định dạng PNG chất lượng cao.

#### 2.9 Xuất kết quả, Sao chép ảnh & Báo cáo kỹ thuật
- **Sao chép đồ thị**: Tất cả 5 tab đồ thị đều có thanh công cụ chuyên dụng:
  - Nút **[📋 Chép Ảnh]**: Sao chép đồ thị nền trắng sắc nét vào Clipboard Windows (sử dụng chuẩn Native 64-bit DIB).
  - Nút **[💾 Lưu Ảnh]**: Lưu đồ thị ra file PNG/PDF với độ phân giải tùy chọn.
- **Xuất báo cáo HTML (`Ctrl + P`)**: Tạo hồ sơ lời giải hoàn chỉnh gồm cả đề bài, công thức toán LaTeX, từng bước lập luận chi tiết và ảnh đồ thị nhúng, sẵn sàng in ra PDF hoặc gửi cho học sinh/đồng nghiệp.

---

### 3. PHẦN II: CẨM NANG SỬ DỤNG GEOSOLVER 2D CAD STUDIO

#### 3.1 Không gian làm việc & Thao tác điều hướng CAD
- **Khu vực vẽ (Canvas)**: Hệ tọa độ 2D không giới hạn, hỗ trợ trục Oxy, hệ lưới tọa độ Grid và tính năng Bắt điểm thông minh (Snap to Grid/Point).
- **Thao tác chuột**:
  - **Chuột trái (LMB)**: Chọn đối tượng, dựng hình theo công cụ đang kích hoạt, kéo di chuyển điểm/hình.
  - **Kéo chuột trái trên vùng trống**: Quét vùng chọn nhiều đối tượng cùng lúc (Box Selection).
  - **Chuột phải (RMB)**: Nhấn chuột phải để hủy công cụ vẽ đang chọn quay về chế độ [Dời]; nhấn chuột phải vào nút [Ẩn/Hiện] để mở bảng quản lý hoặc Khôi phục tất cả đối tượng ẩn.
  - **Cuộn chuột giữa (Mouse Wheel)**: Phóng to (Zoom In) / Thu nhỏ (Zoom Out) mượt mà tâm xoay tại vị trí con trỏ chuột.
  - **Giữ chuột giữa (MMB) & Kéo**: Di chuyển toàn bộ góc nhìn bản vẽ (Pan view).

#### 3.2 Chi tiết 4 thanh công cụ Ribbon

##### Dòng 1: Thao tác tệp, Lịch sử, Biến hình & Báo cáo
- `[Mới]`: Xóa toàn bộ bản vẽ và dữ liệu để lập bài toán mới (`Ctrl + N`).
- `[Xóa hình]`: Chỉ xóa các đối tượng hình vẽ trên canvas, giữ nguyên nội dung ô đề bài.
- `[Hoàn tác]`: Quay lại bước trước đó (`Ctrl + Z`).
- `[Làm lại]`: Tiến tới bước vừa hoàn tác (`Ctrl + Y`).
- `[Chép] / [Dán]`: Sao chép và dán cụm đối tượng hình học đang chọn.
- `[Chọn hết]`: Chọn toàn bộ các điểm, đoạn, đường tròn trên bản vẽ (`Ctrl + A`).
- `[Xoay -15°] / [Xoay +15°]`: Xoay cụm đối tượng đã chọn góc 15 độ.
- `[Góc xoay...]`: Nhập góc xoay chính xác bất kỳ và chọn tâm xoay.
- `[Ẩn/Hiện]`: Ẩn đối tượng đang chọn hoặc bật chế độ xem mờ Ghost Mode.
- `[Xuất ảnh...]`: Hộp thoại xuất ảnh bản vẽ chuyên nghiệp độ phân giải 300 DPI (`Ctrl + E`).
- `[Báo cáo]`: Xuất toàn bộ tiến trình giải và hình vẽ ra báo cáo HTML chuẩn A4 (`Ctrl + P`).

##### Dòng 2: Nhóm công cụ dựng đối tượng cơ bản & quan hệ
- `[↖ Dời]`: Chế độ con trỏ tự do, click để chọn hoặc kéo rê điểm để biến dạng hình vẽ.
- `[↻ Xoay]`: Chọn tâm và kéo đối tượng để xoay tương tác trực tiếp.
- `[✕ Xóa]`: Click vào bất kỳ điểm, đường, elip nào để xóa ngay lập tức.
- `[• Điểm]`: Click vào vùng trống để tạo điểm tự do; click vào đường/đoạn để tạo điểm thuộc đường.
- `[✕ Giao]`: Click vào 2 đường thẳng / đoạn thẳng / đường tròn để tìm và đánh dấu giao điểm chính xác.
- `[✛ T.điểm]`: Click vào 2 điểm hoặc 1 đoạn thẳng để tạo trung điểm chuẩn xác.
- `[⊥ H.chiếu]`: Click 1 điểm và 1 đoạn thẳng để hạ đường vuông góc và lấy chân đường vuông góc.
- `[→ T.tiến]`: Tịnh tiến đối tượng theo vector cho trước.
- `[/ Đoạn]`: Click điểm đầu và điểm cuối để vẽ đoạn thẳng.
- `[- Nét đứt]`: Click 2 điểm để vẽ đoạn thẳng nét đứt (thích hợp cho nét phụ, đường gióng).
- `[— Đường]`: Vẽ đường thẳng vô hạn đi qua 2 điểm.
- `[⊥ Vuông]`: Dựng đường thẳng đi qua điểm cho trước và vuông góc với một đoạn thẳng.
- `[∥ S.song]`: Dựng đường thẳng đi qua điểm cho trước và song song với một đoạn thẳng.
- `[∠ P.giác]`: Click lần lượt 3 điểm $A - B - C$ để dựng đường phân giác góc $\widehat{ABC}$.
- `[∠ Đánh góc]`: Click 3 điểm để vẽ cung tròn đánh dấu góc trên hình.
- `[📐 Góc/Tỉ lệ]`: Hiển thị số đo góc hoặc tỷ lệ các đoạn thẳng trực tiếp.

##### Dòng 3: Đa giác, Đường tròn, Tiếp tuyến & Elip
- `[▱ B.hành]`: Click 3 điểm để dựng hình bình hành hoàn chỉnh (tự động tính điểm thứ 4).
- `[◇ Thoi]`: Dựng hình thoi theo 2 đường chéo hoặc 3 điểm cân xứng.
- `[⏢ Thang cân]`: Dựng hình thang cân chuẩn xác.
- `[□ Vuông]`: Click 2 điểm cạnh để dựng hình vuông hoàn hảo.
- `[⬭ Elip]`: Công cụ dựng Elip chuẩn 2 tiêu điểm + 1 điểm trên đường elip.
- `[⚙ T.tuyến]`: Dựng tiếp tuyến từ 1 điểm nằm ngoài tới đường tròn.
- `[⚙ T.tuyến 2C]`: Dựng tiếp tuyến chung của 2 đường tròn.
- `[▲ Trực tâm]`: Click 3 đỉnh tam giác để tìm trực tâm $H$ (giao 3 đường cao).
- `[⊙ Tâm nội]`: Dựng tâm đường tròn nội tiếp (giao 3 đường phân giác).
- `[⊙ Tròn nội]`: Vẽ trọn vẹn đường tròn nội tiếp tam giác.
- `[⊙ Tâm ngoại]`: Dựng tâm đường tròn ngoại tiếp (giao 3 đường trung trực).
- `[📐 D.tích]`: Click vào các đỉnh đa giác để tính diện tích tức thời.
- `[Bảng chọn Màu]`: Đỏ, Xanh dương, Đen, Lục để phân tách rõ ràng các đường gióng và yếu tố chính/phụ.

##### Dòng 4: Mẫu bài tập, Thiết lập bài toán & Bộ giải
- `Mẫu bài`: Hơn 20 bài toán hình học kinh điển chọn lọc (Đường tròn Euler, Điểm Simson, Tứ giác nội tiếp, Quỹ tích...).
- `Mục tiêu`: Chọn dạng câu hỏi (Chứng minh vuông góc, song song, thẳng hàng, đồng quy, tính góc, tìm quỹ tích...).
- `Đối tượng`: Chọn đối tượng hình học cần kiểm tra mục tiêu.
- `[Nút ký hiệu]`: `∠`, `|x|`, `cos`, `√`, `π` chèn nhanh vào ô đề bài.
- `[▶ GIẢI TOÁN (SymPy)]`: Kích hoạt bộ giải thuần thuật toán đại số hình thức.
- `Hộp chọn AI`: `Thuần thuật toán Python`, `Offline AI`, `Online AI`.
- `[AI giải toán (F5)]`: Khởi chạy trợ lý giải toán tự động kết hợp phân tích hình ảnh và dữ kiện.
- `[Cấu hình]`: Tùy biến tham số mô hình AI, bộ nhớ ngữ cảnh và độ sâu phân tích.

#### 3.3 Công cụ vẽ Elip thế hệ mới
- **Định nghĩa toán học**: Elip được dựng theo định nghĩa hình học cổ điển của Apollonius:
  $$\mathcal{E} = \{M \mid MF_1 + MF_2 = 2a\}$$
  Trong đó: $F_1, F_2$ là hai tiêu điểm, tiêu cự $2c = |F_1F_2|$, $a$ là bán trục lớn ($a > c$), bán trục nhỏ $b = \sqrt{a^2 - c^2}$.
- **Quy trình 3 bước trực quan**:
  1. Click chuột trái chọn Tiêu điểm thứ nhất ($F_1$).
  2. Click chuột trái chọn Tiêu điểm thứ hai ($F_2$). Lúc này trên màn hình sẽ xuất hiện **đường xem trước trực quan (Rubber-band preview)** co giãn theo chuyển động chuột.
  3. Di chuyển chuột đến vị trí điểm $M$ mong muốn và click chuột trái để xác nhận.
- **Tính năng tự động**:
  - Tự động sinh tâm đối xứng $O$ (trung điểm của đoạn $F_1F_2$).
  - Tự động tính toán và lưu trữ: Bán trục lớn $a$, bán trục nhỏ $b$, tiêu cự $c$, góc xoay nghiêng $\theta$, chu vi xấp xỉ Ramanujan và diện tích $S = \pi a b$.
  - **Khả năng tương tác CAD**: Click vào elip để chọn (hiển thị viền cam nổi bật) và kéo chuột để **di chuyển toàn bộ elip cùng các tiêu điểm** một cách mượt mà.
  - Elip được xuất đầy đủ, mịn màng và chuẩn tỉ lệ trên ảnh PNG 300 DPI và báo cáo HTML.

#### 3.4 Cơ chế Tự động phát hiện quan hệ hình học (Deep Invariant Detection)
Khi bạn vẽ các hình hoặc kéo thả các đỉnh trên màn hình, GeoSolver 2D không chỉ coi đó là các nét vẽ vô hồn mà có một **bộ máy quét bất biến hình học (Invariant Engine)** chạy ngầm với sai số thông minh:
- **Tự động nhận diện các loại tam giác**:
  - Tam giác đều ($AB \approx BC \approx CA$).
  - Tam giác vuông cân ($AB \perp AC$ và $AB \approx AC$).
  - Tam giác cân ($AB \approx AC$ hoặc $BA \approx BC$).
  - Tam giác vuông ($AB \perp BC$).
- **Tự động nhận diện quan hệ đoạn & đường**:
  - Các đoạn thẳng bằng nhau ($AB = CD$).
  - Các cặp đường thẳng song song ($AB \parallel CD$).
  - Các cặp đường thẳng vuông góc ($AB \perp CD$).
  - Trung điểm ($M$ là trung điểm $AB$).
- **Hiệu quả thực tế**: Các quan hệ phát hiện được sẽ tự động hiển thị trong bảng quan hệ và **tự động nạp vào bộ giả thiết của bài toán**. Nhờ đó, người dùng không cần phải gõ lại bằng tay các giả thiết như "Tam giác ABC cân tại A" hay "M là trung điểm BC", giúp bộ giải thuật toán Python có thể suy luận trực tiếp ngay lập tức!

#### 3.5 Khung Trình bày bài toán & Các nút ký hiệu toán học
- Nằm ngay dưới thanh công cụ, chia làm 2 phần trực quan:
  - **Giả thiết bài toán**: Tự động sinh từ hình vẽ, người dùng có thể gõ thêm điều kiện bổ sung.
  - **Yêu cầu / Câu hỏi**: Ghi rõ mục tiêu (Ví dụ: "Chứng minh AH vuông góc BC", "Tính diện tích tam giác ABC").
- **Thanh công cụ ký hiệu nhanh**: Đặt ngay bên cạnh ô nhập:
  - `∠`: Ký hiệu góc hình học.
  - `|x|`: Độ dài đoạn thẳng hoặc giá trị tuyệt đối.
  - `cos`: Hàm lượng giác cosin.
  - `√`: Dấu căn thức bậc hai.
  - `π`: Hằng số Pi.
  - Giúp thao tác gõ đề bài nhanh gấp 3 lần so với việc tìm ký hiệu trên bàn phím.

#### 3.6 Cơ chế Ẩn/Hiện đối tượng (Ghost Mode) & Khôi phục
- **Mục đích**: Trong các bài toán hình học phức tạp, việc dựng nhiều đường phụ, đường trung trực, đường tròn ngoại tiếp có thể khiến bản vẽ bị rối mắt.
- **Cách thức hoạt động**:
  - Chọn một hoặc nhiều đối tượng -> Bấm nút `[Ẩn/Hiện]` trên thanh công cụ: Đối tượng sẽ được ẩn đi. Dù bị ẩn, đối tượng **vẫn giữ nguyên liên kết toán học** trong bộ giải.
  - **Chế độ Nét ẩn (Ghost View)**: Khi không chọn đối tượng nào, bấm nút `[Ẩn/Hiện]` sẽ chuyển đổi giữa việc giấu hẳn đối tượng và hiển thị đối tượng dưới dạng **nét chấm mờ màu xám nhạt (`#adb5bd`)**. Giúp bạn định vị được đường phụ mà không làm phân tâm mắt nhìn.
  - **Khôi phục toàn bộ (`Unhide All`)**: 
    - Cách 1: **Click chuột phải** trực tiếp vào nút `[Ẩn/Hiện]`.
    - Cách 2: Vào menu `Tùy chọn` -> chọn `Hiện lại tất cả đối tượng ẩn (Unhide All)`.

#### 3.7 Xuất ảnh bản vẽ CAD & Xuất báo cáo HTML
- **Sao chép ảnh nhanh vào Clipboard**:
  - Bấm menu `Tùy chọn` -> `Sao chép ảnh bản vẽ vào Clipboard`.
  - Ảnh bản vẽ nền trắng với nét vẽ vector sắc nét sẽ được đưa vào bộ nhớ tạm Windows để dán ngay lập tức (`Ctrl + V`) vào Microsoft Word, PowerPoint, Zalo, Paint.
- **Hộp thoại Xuất ảnh nâng cao (`Ctrl + E`)**:
  - Độ phân giải chuẩn xuất bản: **300 DPI**.
  - Các tùy chọn hoạt động hoàn toàn độc lập:
    - `[✓] Trục tọa độ Oxy`: Quyết định hiển thị hoặc bỏ hệ trục Oxy.
    - `[✓] Lưới tọa độ Grid`: Quyết định hiển thị hoặc ẩn lưới ô vuông.
    - `[✓] Đường thẳng kéo dài`: Bật/tắt các tia đường thẳng vô hạn vượt ngoài khung hình.
    - `[✓] Tự động cắt sát hình (Auto-crop)`: Tự động tính toán bounding-box của toàn bộ hình vẽ kèm lề an toàn 25px để tạo ra file ảnh gọn gàng, không bị thừa khoảng trắng.
- **Xuất báo cáo HTML (`Ctrl + P`)**: Xuất file HTML trình bày đẹp mắt gồm hình vẽ, danh sách đối tượng, các quan hệ hình học đã nhận diện và từng bước giải thuật toán chi tiết.

#### 3.8 Hỗ trợ giải toán: Thuần thuật toán Python & AI Support
- **Bộ giải Thuần thuật toán Python (SymPy Engine)**:
  - Hoạt động 100% Offline, không phụ thuộc mạng Internet.
  - Áp dụng các định lý hình học thuần túy (Talet, Menelaus, Ceva, Carnot, phương tích đường tròn, tích vô hướng).
  - Đảm bảo tính chính xác tuyệt đối, lập luận từng bước logic kèm tham chiếu định lý.
- **AI Support**:
  - Menu `Tùy chọn` -> `AI Support Offline` hoặc bấm nút cam `[AI giải toán (F5)]`.
  - Phân tích hình ảnh bản vẽ, đề xuất các đường kẻ phụ (Auxiliary Lines) độc đáo cho các bài toán hình học khó cấp tỉnh và quốc gia.

---

### 4. PHẦN III: BẢNG TRA CỨU PHÍM TẮT TOÀN TẬP (KEYBOARD SHORTCUTS)

#### 4.1 Bảng phím tắt CAD Math Studio v2.1

| Phím tắt | Tác vụ tương ứng | Mô tả chức năng |
| :--- | :--- | :--- |
| **`F1`** | **Mở Cẩm nang sử dụng** | Mở tài liệu cẩm nang hướng dẫn và phím tắt này |
| **`F5`** | **Giải bài toán (Solve)** | Kích hoạt bộ giải toán cho tab hiện tại |
| **`Enter`** | **Tính toán / Giải nhanh** | Thực thi giải khi đang nhập trong ô công thức |
| **`Ctrl + P`** | **Xuất báo cáo HTML** | Tạo báo cáo tổng hợp kết quả giải và đồ thị |
| **`Ctrl + S`** | **Lưu lời giải** | Lưu toàn bộ tiến trình lời giải ra file văn bản |
| **`Ctrl + Shift + S`**| **Lưu ảnh đồ thị** | Lưu đồ thị Matplotlib hiện hành ra file PNG |
| **`Ctrl + O`** | **Mở tệp đề bài** | Nạp tệp bài toán đã lưu từ đĩa |
| **`Ctrl + L`** | **Xóa sạch Tab hiện tại** | Xóa nhanh dữ liệu đầu vào và kết quả của tab |
| **`Ctrl + +` / `Ctrl + =`** | **Phóng to cỡ chữ** | Tăng kích thước phông chữ hiển thị kết quả |
| **`Ctrl + -`** | **Thu nhỏ cỡ chữ** | Giảm kích thước phông chữ hiển thị kết quả |
| **`Ctrl + 0`** | **Khôi phục cỡ chữ** | Đặt lại cỡ chữ hiển thị về mặc định (10pt) |
| **`Ctrl + Q`** | **Thoát ứng dụng** | Đóng phần mềm an toàn |

---

#### 4.2 Bảng phím tắt GeoSolver 2D CAD Studio

| Phím tắt | Tác vụ tương ứng | Mô tả chức năng |
| :--- | :--- | :--- |
| **`F1`** | **Mở Cẩm nang sử dụng** | Mở tài liệu cẩm nang hướng dẫn và phím tắt này |
| **`F5`** | **AI giải toán** | Kích hoạt AI Support phân tích hình học |
| **`Ctrl + Z`** | **Hoàn tác (Undo)** | Hoàn tác thao tác dựng hình hoặc xóa trước đó |
| **`Ctrl + Y`** | **Làm lại (Redo)** | Phục hồi lại thao tác vừa Undo |
| **`Ctrl + A`** | **Chọn tất cả** | Chọn toàn bộ các điểm, đoạn, đường, elip |
| **`Ctrl + C`** | **Sao chép** | Sao chép cụm đối tượng hình học đang chọn |
| **`Ctrl + V`** | **Dán** | Dán các đối tượng hình học đã sao chép |
| **`Ctrl + N`** | **Tạo bản vẽ mới** | Xóa sạch bản vẽ và đề bài để vẽ bài mới |
| **`Ctrl + E`** | **Xuất ảnh bản vẽ** | Mở hộp thoại xuất ảnh PNG 300 DPI chuyên nghiệp |
| **`Ctrl + P`** | **Xuất báo cáo HTML** | Xuất bài toán, bản vẽ và lời giải ra báo cáo web |
| **`Delete` / `Backspace`** | **Xóa đối tượng chọn** | Xóa ngay các điểm hoặc đường đang được chọn |
| **`Escape` (Esc)** | **Hủy lệnh vẽ** | Trả con trỏ về công cụ di chuyển mặc định `[Dời]` |
| **`Cuộn chuột giữa`** | **Thu phóng (Zoom)** | Phóng to / Thu nhỏ góc nhìn tại vị trí chuột |
| **`Giữ chuột giữa + Kéo`** | **Trượt bản vẽ (Pan)** | Di chuyển vùng quan sát không gian bản vẽ CAD |
| **`Chuột phải vào [Ẩn/Hiện]`** | **Khôi phục tất cả** | Hiện lại toàn bộ các đường phụ đang bị ẩn |

---

### 5. PHẦN IV: MẸO & KINH NGHIỆM TỐI ƯU HÓA THAO TÁC (PRO TIPS)

> [!TIP]
> **1. Dán ảnh bài tập trực tiếp vào Word & PowerPoint không qua trung gian**
> Không cần phải bấm "Lưu ảnh ra file rồi Insert Picture". Chỉ cần bấm nút **[📋 Chép Ảnh]** trên bất kỳ tab nào của CAD Math Studio hoặc dùng menu `Tùy chọn -> Sao chép ảnh bản vẽ` trong GeoSolver 2D, sau đó chuyển sang Word/PowerPoint và bấm `Ctrl + V`. Ảnh sẽ được dán ngay lập tức với nền trắng tinh khiết, viền trong suốt và độ phân giải cao!

> [!TIP]
> **2. Tận dụng cơ chế Bắt điểm & Nhận diện thông minh**
> Trong GeoSolver 2D, khi muốn dựng tam giác cân hoặc các cạnh bằng nhau, bạn chỉ cần ước lượng vẽ độ dài xấp xỉ bằng nhau (dung sai tự động cho phép sai lệch nhẹ khi thao tác tay). Bộ máy *Deep Invariant Detection* sẽ lập tức nhận biết và bắt cố định quan hệ bằng nhau, giúp tam giác chuyển thành tam giác cân hoàn hảo trong bộ giải mà không cần tính toán tọa độ thủ công.

> [!TIP]
> **3. Kỹ thuật dùng Nét ẩn (Ghost Mode) cho đề thi trắc nghiệm & tự luận**
> Khi vẽ hình để xuất vào đề thi, hãy dùng công cụ `[- Nét đứt]` cho các nét khuất, và chọn các đường tròn phụ/đường trung trực rồi bấm `[Ẩn/Hiện]`. Sau đó mở hộp thoại `[Xuất ảnh...] (Ctrl + E)`, tích chọn `Tự động cắt sát hình` và bỏ tích `Trục tọa độ Oxy`, `Lưới tọa độ`. Bạn sẽ thu được một bức hình chuẩn mực sách giáo khoa chỉ trong chưa đầy 3 giây!

> [!TIP]
> **4. Xử lý bài toán chứa tham số $m$ phức tạp trong CAD Math**
> Với các bất phương trình có tham số $m$ kết hợp căn thức như $\sqrt{x-1} + \sqrt{5-x} \le m$, bạn chỉ cần gõ nguyên văn vào Tab 1. CAD Math Studio sẽ tự động xác định tập xác định $D = [1; 5]$, khảo sát hàm $f(x) = \sqrt{x-1} + \sqrt{5-x}$, tìm giá trị lớn nhất và nhỏ nhất bằng đạo hàm, rồi kết luận điều kiện chính xác của $m$ để BPT có nghiệm hoặc nghiệm đúng với mọi $x \in D$.

---
*Tài liệu được biên soạn đồng bộ cho Hệ sinh thái STEM Mathematics Suite.*
