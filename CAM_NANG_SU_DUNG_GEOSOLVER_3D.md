# Hướng Dẫn Sử Dụng GeoSolver 3D
## Phần mềm vẽ hình và hỗ trợ học hình học không gian 3D

---

### Mục lục
1. [Giới thiệu](#1-giới-thiệu)
2. [Giao diện phần mềm](#2-giao-diện-phần-mềm)
   - [2.1 Thanh menu trên cùng](#21-thanh-menu-trên-cùng)
   - [2.2 Hai hàng nút bấm nhanh (Ribbon)](#22-hai-hàng-nút-bấm-nhanh-ribbon)
   - [2.3 Khung vẽ hình 3D (Canvas)](#23-khung-vẽ-hình-3d-canvas)
   - [2.4 Cột thông số bên phải (Sidebar)](#24-cột-thông-số-bên-phải-sidebar)
3. [Cách dùng từng chức năng](#3-cách-dùng-từng-chức-năng)
   - [3.1 Chọn các hình khối mẫu](#31-chọn-các-hình-khối-mẫu)
   - [3.2 Xoay hình, phóng to, thu nhỏ và đặt lại góc nhìn](#32-xoay-hình-phóng-to-thu-nhỏ-và-đặt-lại-góc-nhìn)
   - [3.3 Kéo dời đỉnh và thêm điểm trên cạnh](#33-kéo-dời-đỉnh-và-thêm-điểm-trên-cạnh)
   - [3.4 Cắt hình bằng mặt phẳng (thiết diện)](#34-cắt-hình-bằng-mặt-phẳng-thiết-diện)
   - [3.5 Gạch sọc mặt cắt (hatching) và đổi màu](#35-gạch-sọc-mặt-cắt-hatching-và-đổi-màu)
   - [3.6 Xem mặt cầu ngoại tiếp](#36-xem-mặt-cầu-ngoại-tiếp)
   - [3.7 Xem các bài toán và lời giải mẫu (12 dạng bài)](#37-xem-các-bài-toán-và-lời-giải-mẫu-12-dạng-bài)
   - [3.8 Xuất ảnh và xuất báo cáo](#38-xuất-ảnh-và-xuất-báo-cáo)
   - [3.9 Hoàn tác (Undo/Redo), sao chép và dán](#39-hoàn-tác-undoredo-sao-chép-và-dán)
4. [Bảng phím tắt và thao tác chuột](#4-bảng-phím-tắt-và-thao-tác-chuột)
5. [Một số lưu ý khi sử dụng](#5-một-số-lưu-ý-khi-sử-dụng)

---

### 1. Giới thiệu

**GeoSolver 3D** là phần mềm vẽ hình học không gian 3 chiều và hỗ trợ giải toán hình học. Phần mềm giúp bạn:
- Quan sát các hình khối không gian (hình chóp, hình lăng trụ, hình hộp, hình lập phương...).
- Tự động vẽ nét đứt cho các cạnh bị che khuất và nét liền cho các cạnh nhìn thấy.
- Tạo mặt phẳng cắt để xem thiết diện, gạch sọc mặt cắt, tính diện tích thiết diện.
- Xem lời giải chi tiết cho 12 dạng bài tập quen thuộc, công thức hiển thị dạng căn thức dễ nhìn thay vì số thập phân dài.
- Xuất hình vẽ ra file ảnh PNG (có tùy chọn nền trong suốt để chèn vào Word) hoặc file báo cáo.

---

### 2. Giao diện phần mềm

Giao diện gồm 4 khu vực chính:

```
+---------------------------------------------------------------------------------------+
|  GeoSolver 3D - Hình Học Không Gian & Vẽ Kỹ Thuật CAD                     [_] [口] [X]|
+---------------------------------------------------------------------------------------+
| Tệp (File) | Chỉnh sửa (Edit) | Hiển thị (View) | Công cụ (Tools) | Tùy chọn | Thông tin|
+---------------------------------------------------------------------------------------+
| HÀNG 1: [Chọn khối] [↶ Hoàn tác] [↷ Làm lại] [Xuất ảnh] [Báo cáo] [AI] [Ngôn ngữ]     |
| HÀNG 2: [Thu phóng] [Xoay 3D] [Trục Oxyz] [Nét đứt] [Thiết diện] [Mặt cầu]            |
+-------------------------------------------------------------------+-------------------+
|                                                                   | CỘT BÊN PHẢI      |
|                                                                   |                   |
|                        KHUNG VẼ 3D (CANVAS)                       | - Kích thước đáy  |
|                                                                   | - Chiều cao       |
|            - Giữ chuột trái để xoay hình                          | - Hướng mặt cắt   |
|            - Lăn chuột để phóng to / thu nhỏ                      | - Kết quả đo đạc: |
|            - Bấm vào đỉnh để kéo dời                              |   Thể tích,       |
|                                                                   |   Diện tích,      |
|                                                                   |   Bán kính cầu... |
+-------------------------------------------------------------------+-------------------+
| Trạng thái: Sẵn sàng | Góc xoay: (30°, 25°) | Tỉ lệ: 1.00x | Khối: Chóp tam giác S.ABC|
+---------------------------------------------------------------------------------------+
```

#### 2.1 Thanh menu trên cùng
- **Tệp (File):** Mở hình khối mẫu, xuất file ảnh (`Ctrl+E`), xuất báo cáo HTML (`Ctrl+P`), xuất lời giải ra file văn bản, thoát chương trình (`Alt+F4`).
- **Chỉnh sửa (Edit):** Hoàn tác bước trước (`Ctrl+Z`), làm lại bước vừa hủy (`Ctrl+Y`), sao chép thông số (`Ctrl+C`), dán thông số (`Ctrl+V`), đặt lại vị trí các đỉnh ban đầu (`Ctrl+R`).
- **Hiển thị (View):** Phóng to (`Ctrl++`), thu nhỏ (`Ctrl+-`), đặt lại góc nhìn ban đầu (`Ctrl+0`), bật chế độ xoay (`M`), bật chế độ kéo đỉnh (`V`), bật/tắt trục tọa độ Oxyz (`X`), bật/tắt nét đứt (`H`), bật/tắt thiết diện (`S`), bật/tắt mặt cầu (`C`), đổi nét đậm/mảnh (`B`).
- **Công cụ (Tools):** Dựng hình, thêm điểm trên cạnh theo tỉ số $k$, tô màu mặt phẳng, mở hộp thoại giải toán 12 chuyên đề (`F5` hoặc `D`).
- **Tùy chọn (Options):** Đổi ngôn ngữ giữa Tiếng Việt và English; mục AI hỗ trợ (tạm khóa chờ bổ sung thêm ở bản sau).
- **Thông tin (Help):** Hướng dẫn sử dụng (`F1`), xem bảng phím tắt, thông tin về phần mềm.

#### 2.2 Hai hàng nút bấm nhanh (Ribbon)
- **Hàng 1:** Chứa nút chọn khối mẫu, hai nút hoàn tác / làm lại, nút xuất ảnh, nút xuất báo cáo và nút đổi ngôn ngữ.
- **Hàng 2:** Chứa các nút thao tác nhanh: phóng to, thu nhỏ, đặt lại góc nhìn, bật trục Oxyz, bật nét đứt, bật thiết diện, bật mặt cầu và đổi độ đậm nét vẽ.

#### 2.3 Khung vẽ hình 3D (Canvas)
Vùng màu trắng xám ở giữa để hiển thị hình vẽ 3D. Các cạnh khuất phía sau tự động vẽ nét đứt, các cạnh nhìn thấy vẽ nét liền.

#### 2.4 Cột thông số bên phải (Sidebar)
Nằm ở bên phải, gồm các ô nhập chiều dài cạnh đáy, chiều cao, góc nghiêng mặt cắt, và khung hiển thị kết quả (thể tích $V$, diện tích xung quanh, bán kính mặt cầu ngoại tiếp $R$...). Bạn có thể giữ chuột vào vách ngăn giữa khung vẽ và cột bên phải để kéo rộng hoặc thu hẹp lại.

---

### 3. Cách dùng từng chức năng

#### 3.1 Chọn các hình khối mẫu
1. Bấm vào danh sách **"Chọn Khối Đa Diện"** trên thanh công cụ hoặc vào menu `Tệp -> Mở Khối Đa Diện Mẫu`.
2. Chọn hình bạn muốn vẽ, ví dụ:
   - Chóp tam giác $S.ABC$
   - Tứ diện đều $ABCD$
   - Chóp tứ giác đều $S.ABCD$
   - Chóp có cạnh bên vuông góc đáy
   - Lăng trụ đứng tam giác
   - Lăng trụ tam giác đều
   - Hình hộp chữ nhật, hình lập phương
   - Lăng trụ xiên, bát diện đều, chóp cụt, chóp đáy hình thang.
3. Hình mới sẽ hiện ngay trên khung vẽ cùng các kích thước tương ứng.

#### 3.2 Xoay hình, phóng to, thu nhỏ và đặt lại góc nhìn
- **Xoay hình:** Giữ chuột trái trên khung vẽ rồi kéo chuột sang trái, phải, lên hoặc xuống. Hoặc bạn có thể dùng 4 phím mũi tên `←`, `→`, `↑`, `↓` trên bàn phím.
- **Phóng to, thu nhỏ:** Lăn con lăn chuột tới trước để phóng to, lăn lùi để thu nhỏ. Bạn cũng có thể bấm phím `+` hoặc `-`.
- **Đặt lại góc nhìn ban đầu:** Nhấn **`Ctrl+0`** (hoặc nút `[ ↺ Đặt lại ]`). Góc nhìn sẽ quay về vị trí dễ nhìn nhất lúc ban đầu.

#### 3.3 Kéo dời đỉnh và thêm điểm trên cạnh
- **Kéo dời đỉnh:**
  1. Bấm nút `[ Dời đỉnh ]` hoặc bấm phím `V`.
  2. Rê chuột vào đỉnh cần kéo (con trỏ chuột đổi sang hình bàn tay).
  3. Giữ chuột trái và kéo đến vị trí mong muốn.
  4. Nếu muốn quay về hình dạng ban đầu, nhấn **`Ctrl+R`** hoặc **`Ctrl+Z`**.
- **Thêm điểm trên cạnh:**
  1. Vào menu `Công cụ -> Thêm Điểm Trên Đoạn Thẳng (Tỉ số k)...`
  2. Chọn cạnh cần lấy điểm (ví dụ cạnh $SA$ hoặc $BC$).
  3. Kéo thanh trượt tỉ số $k$ từ $0.0$ đến $1.0$ (ví dụ $k = 0.5$ là trung điểm). Bấm Đồng ý, điểm mới sẽ xuất hiện trên cạnh đó.

#### 3.4 Cắt hình bằng mặt phẳng (thiết diện)
1. Bấm phím **`S`** hoặc bấm nút `[ Thiết diện ]` trên thanh công cụ để mở mặt phẳng cắt.
2. Có 4 nút chọn hướng cắt nhanh:
   - `[ Cắt Oxy ]`: Cắt ngang song song mặt đáy.
   - `[ Cắt Xiên ]`: Cắt chéo qua các cạnh bên.
   - `[ Cắt Oxz ]`: Cắt đứng theo chiều dọc.
   - `[ Cắt Chéo Đáy ]`: Cắt theo đường chéo của đáy.
3. Điều chỉnh vị trí cắt:
   - Kéo thanh trượt vị trí mặt cắt ở cột bên phải để di chuyển mặt cắt lên xuống.
   - Hoặc chuyển sang chế độ **"Độc lập đỉnh"** để bấm kéo từng đỉnh của mặt cắt.

#### 3.5 Gạch sọc mặt cắt (hatching) và đổi màu
- Mặt cắt khi cắt qua khối hình sẽ được gạch các đường chéo nghiêng $45^\circ$ hoặc gạch ca-rô để dễ phân biệt.
- Bạn có thể bấm vào các ô màu (Đỏ, Xanh dương, Đen, Xanh lá, Cam) ở cột bên phải để đổi màu mặt cắt và đường viền.

#### 3.6 Xem mặt cầu ngoại tiếp
- Bấm phím **`C`** hoặc nút `[ Cầu Ngoại Tiếp ]`.
- Phần mềm sẽ vẽ mặt cầu bao quanh các đỉnh của khối đa diện (nếu khối đó có mặt cầu ngoại tiếp), đồng thời hiển thị tọa độ tâm $I$ và độ dài bán kính $R$ ở cột bên phải.

#### 3.7 Xem các bài toán và lời giải mẫu (12 dạng bài)
1. Bấm phím **`F5`** (hoặc phím **`D`**, hoặc nút `[ 💡 Suy Luận 3D ]`).
2. Một bảng hiện ra với 12 dạng bài tập:
   - Chứng minh đường thẳng vuông góc mặt phẳng.
   - Chứng minh hai mặt phẳng vuông góc.
   - Tính góc giữa đường thẳng và mặt phẳng.
   - Tính góc giữa hai mặt phẳng.
   - Tính khoảng cách từ điểm đến mặt phẳng.
   - Tính khoảng cách giữa hai đường chéo nhau.
   - Tìm tâm và bán kính mặt cầu ngoại tiếp.
   - Tính diện tích và thể tích hình chóp.
   - Tính diện tích và thể tích hình lăng trụ.
   - Tìm thiết diện và tính diện tích thiết diện.
   - Tính tỉ số thể tích.
   - Đưa hệ trục tọa độ Oxyz vào khối đa diện.
3. Nhập số liệu kích thước của bài toán vào các ô, bấm nút **Tính toán**.
4. Lời giải sẽ hiện từng bước, có nêu rõ định lý áp dụng. Các kết quả có căn bậc hai (như $\sqrt{3}$, $\frac{\sqrt{41}}{2}$, $\frac{3\sqrt{6}}{2}$) được giữ nguyên dạng căn thức để bạn dễ chép vào bài làm.
5. Bạn có thể bấm **Sao chép lời giải** để dán vào tài liệu Word của mình.

#### 3.8 Xuất ảnh và xuất báo cáo
- **Xuất ảnh (`Ctrl+E`):**
  - Mở hộp thoại xuất ảnh.
  - Bạn có thể tích chọn có hiện trục tọa độ, có hiện mặt cầu, có hiện thiết diện hay không.
  - Tùy chọn **"Nền trong suốt"** rất tiện khi bạn muốn chèn ảnh vào đề thi hay giáo án Word mà không có khung viền màu xám.
  - Chọn độ phân giải: màn hình thường (96 DPI) hoặc in ấn rõ nét (300 DPI). Bấm **Lưu ảnh** để chọn nơi lưu file PNG.
- **Xuất báo cáo HTML (`Ctrl+P`):**
  - Tạo ra một file web gồm hình ảnh 3D và các bảng số liệu chi tiết để xem lại hoặc in ra giấy.

#### 3.9 Hoàn tác (Undo/Redo), sao chép và dán
- **Hoàn tác (`Ctrl+Z`):** Bấm khi bạn vừa chỉnh nhầm và muốn quay lại bước trước.
- **Làm lại (`Ctrl+Y`):** Bấm khi muốn khôi phục bước vừa hoàn tác.
- **Sao chép (`Ctrl+C`):** Bấm để sao chép thông số tọa độ hoặc nội dung lời giải.
- **Dán (`Ctrl+V`):** Bấm để dán dữ liệu vào ô nhập liệu.

---

### 4. Bảng phím tắt và thao tác chuột

| Phím tắt | Tên chức năng | Mô tả |
| :--- | :--- | :--- |
| **`F1`** | **Hướng dẫn sử dụng** | Mở bảng hướng dẫn và phím tắt |
| **`F5`** hoặc **`D`** | **Giải toán 3D** | Mở bảng giải 12 dạng bài tập hình không gian |
| **`Ctrl + Z`** | **Hoàn tác** | Quay lại thao tác trước đó |
| **`Ctrl + Y`** | **Làm lại** | Phục hồi thao tác vừa hoàn tác |
| **`Ctrl + C`** | **Sao chép** | Sao chép thông số, tọa độ hoặc văn bản lời giải |
| **`Ctrl + V`** | **Dán** | Dán thông số vào ô đang chọn |
| **`Ctrl + R`** | **Đặt lại đỉnh** | Đưa các đỉnh về vị trí ban đầu của hình khối |
| **`Ctrl + E`** | **Xuất ảnh** | Mở hộp thoại lưu hình vẽ 3D ra file PNG |
| **`Ctrl + P`** | **Xuất báo cáo** | Xuất tài liệu tóm tắt hình vẽ ra file HTML |
| **`Ctrl + +`** hoặc **`+`** | **Phóng to** | Phóng to hình thêm một chút |
| **`Ctrl + -`** hoặc **`-`** | **Thu nhỏ** | Thu nhỏ hình lại một chút |
| **`Ctrl + 0`** | **Đặt lại góc nhìn** | Đưa góc nhìn và kích thước về mặc định |
| **`M`** | **Chế độ xoay** | Bật chế độ dùng chuột để xoay hình |
| **`V`** | **Chế độ dời đỉnh** | Bật chế độ bấm vào đỉnh để kéo dời |
| **`X`** | **Trục Oxyz** | Bật hoặc tắt hệ trục tọa độ 3 chiều |
| **`H`** | **Nét đứt (nét khuất)** | Bật hoặc tắt hiển thị nét đứt cho cạnh khuất |
| **`S`** | **Mặt phẳng cắt** | Bật hoặc tắt mặt phẳng cắt và hình thiết diện |
| **`C`** | **Mặt cầu ngoại tiếp** | Bật hoặc tắt mặt cầu bao quanh hình |
| **`B`** | **Nét vẽ đậm/mảnh** | Đổi giữa nét vẽ đậm rõ và nét vẽ mảnh |
| **`←` `→` `↑` `↓`** | **Xoay từng bước** | Dùng phím mũi tên để xoay hình từ từ |
| **`Alt + F4`** | **Thoát** | Đóng phần mềm |

#### Thao tác chuột
- **Giữ chuột trái kéo trên vùng trống:** Xoay hình theo hướng di chuyển của tay.
- **Lăn con lăn chuột:** Phóng to hoặc thu nhỏ hình.
- **Giữ chuột trái trên đỉnh đỏ (chế độ V):** Kéo đỉnh tới vị trí mới.
- **Kéo vách ngăn giữa hai khung:** Mở rộng khung vẽ hoặc mở rộng cột thông số bên phải.

---

### 5. Một số lưu ý khi sử dụng

1. **Khi chèn hình vào tài liệu Word hoặc bài kiểm tra:**
   - Bạn nên nhấn `Ctrl+E`, đánh dấu vào ô **"Nền trong suốt"** và chọn mức **"In ấn rõ nét (300 DPI)"**. Ảnh chèn vào trang giấy sẽ vừa vặn, không có viền nền xám.
2. **Khi giảng bài hoặc chiếu lên màn hình lớn:**
   - Nhấn phím `B` để chuyển sang nét vẽ đậm. Nét hình sẽ dày hơn, người ngồi ở xa cũng có thể quan sát rõ.
3. **Khi muốn lấy công thức căn thức chính xác:**
   - Trong bảng giải toán (`F5`), các bài toán liên quan đến góc, khoảng cách, chiều cao đều đưa ra công thức dạng căn thức như $\sqrt{3}$, $\frac{\sqrt{41}}{2}$. Bạn có thể bấm nút **Sao chép** để lấy nguyên văn lời giải.
4. **Đổi ngôn ngữ sang tiếng Anh:**
   - Vào menu `Tùy chọn -> Ngôn ngữ -> English`. Toàn bộ nút bấm, tên hình khối và 12 dạng bài tập sẽ chuyển sang tiếng Anh đơn giản, dễ đọc.

---
*GeoSolver 3D - Phần mềm học tập và vẽ hình học không gian.*
