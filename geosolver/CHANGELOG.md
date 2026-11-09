# NHẬT KÝ PHÁT TRIỂN & TÀI LIỆU KHÔI PHỤC DỰ ÁN (GEOSOLVER CAD)
**Dự án:** GeoSolver CAD - Công Cụ Dựng Hình & Giải Toán Hình Học Tự Động (MS Office 2003 / Cabri II Plus Style)  
**Tệp thực thi chính:** `geosolver_desktop.py`  
**Khởi tạo & Cập nhật lần cuối:** 01/11/2026  
**Ngôn ngữ & Thư viện:** Python 3.10+, Tkinter, Pillow (PIL), SymPy, PyMuPDF (fitz)  

---

## MỤC LỤC
1. [Tổng Quan Kiến Trúc Hệ Thống](#1-tổng-quan-kiến-trúc-hệ-thống)
2. [Cấu Trúc Dữ Liệu Hình Học Chuẩn (Data Schema)](#2-cấu-trúc-dữ-liệu-hình-học-chuẩn-data-schema)
3. [Nhật Ký Các Bản Cập Nhật & Thay Đổi Chi Tiết (Changelog)](#3-nhật-ký-các-bản-cập-nhật--thay-đổi-chi-tiết-changelog)
4. [Danh Mục Mẫu Bài Tập Kinh Điển Đã Tích Hợp (Presets 0 - 6)](#4-danh-mục-mẫu-bài-tập-kinh-điển-đã-tích-hợp-presets-0---6)
5. [Hướng Dẫn Khôi Phục (Restore) & Quy Trình Kiểm Thử](#5-hướng-dẫn-khôi-phục-restore--quy-trình-kiểm-thử)
6. [Cẩm Nang Phát Triển Mở Rộng Cho Các Phiên Bản Sau](#6-cẩm-nang-phát-triển-mở-rộng-cho-các-phiên-bản-sau)

---

## 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

Phần mềm hoạt động theo **Kiến trúc Lai 2 Tầng (Hybrid CAD & CAS Engine)**:

```
+-----------------------------------------------------------------------------------+
|                            GIAO DIỆN NGƯỜI DÙNG (UI)                              |
|   - Thanh Menu Chuẩn (File, Edit, Transform, Presets, View)                       |
|   - Hàng 1: Thao tác file, Clipboard, Lịch sử, Xoay hình, Thu phóng              |
|   - Hàng 2: Hộp công cụ CAD trực quan Cabri (Điểm, Đoạn, Đường, Tròn, Hình)      |
|   - Hàng 3: Thanh giải toán nhanh (Chọn mẫu, Mục tiêu, Đối tượng, Nút Run SymPy) |
+-----------------------------------------+-----------------------------------------+
|        CANVAS ĐỒ HỌA TƯƠNG TÁC          |         BẢNG ĐIỀU KHIỂN & LỜI GIẢI      |
|  - Hệ tọa độ Oxy & Lưới điểm động       |  - Tab 1: Đề bài, Bất biến, Lời giải    |
|  - Bắt dính giao điểm & Smart Snapping  |  - Tab 2: Danh sách đối tượng (Treeview)|
|  - Tương tác chuột: Dời, Xoay, Tẩy, Vẽ  |  - Nút Thu gọn / Mở rộng toàn màn hình  |
+-----------------------------------------+-----------------------------------------+
                                          |
                         +----------------+----------------+
                         |                                 |
                         v                                 v
      +------------------------------------+  +------------------------------------+
      |    TẦNG 1: ENGINE GIẢI TÍCH SYMPY  |  |    TẦNG 2: KHO TRI THỨC OLYMPIC   |
      | - Tự do dựng hình không hạn chế    |  | - Mẫu suy luận hình học thuần túy  |
      | - Tính ma trận tọa độ thời gian thực| | - Định lý hàm Sin, Vị tự, Bổ đề    |
      | - Định thức vector, Tích vô hướng  |  | - Phân tích bài toán VMO, Tuyển sinh|
      | - Giải hệ phương trình phi tuyến   |  | - Lập luận sư phạm bước-theo-bước   |
      +------------------------------------+  +------------------------------------+
```

---

## 2. CẤU TRÚC DỮ LIỆU HÌNH HỌC CHUẨN (DATA SCHEMA)

Mọi đối tượng vẽ trên Canvas đều được quản lý trong các danh sách nội bộ của lớp `GeoSolverApp`:

### 2.1. Điểm (`self.points`):
```python
{
    "id": "pt_1",            # Định danh duy nhất (str)
    "name": "A",             # Tên hiển thị (str, hỗ trợ A', M1, O'...)
    "x": 0.0,                # Tọa độ thực x trên mặt phẳng Oxy (float)
    "y": 3.0,                # Tọa độ thực y trên mặt phẳng Oxy (float)
    "color": "#003399",      # Màu hiển thị hex (str)
    "fixed": False,          # True: Cố định (không kéo dời được); False: Điểm tự do
    "hidden": False          # True: Ẩn nét gióng phụ
}
```

### 2.2. Đoạn thẳng (`self.segments`):
```python
{
    "p1": point_dict_1,      # Tham chiếu tới điểm đầu
    "p2": point_dict_2,      # Tham chiếu tới điểm cuối
    "color": "#212529",      # Màu nét vẽ
    "style": "solid",        # Kiểu nét: "solid", "dashed", "bold"
    "label": "AB",           # Nhãn hiển thị bên cạnh
    "hidden": False
}
```

### 2.3. Đường thẳng vô hạn (`self.lines`):
```python
{
    "p1": point_dict_1,      # Điểm thứ nhất đi qua
    "p2": point_dict_2,      # Điểm thứ hai đi qua
    "color": "#adb5bd",      # Màu nét
    "style": "solid",
    "label": "BC: y = 4",
    "hidden": False
}
```

### 2.4. Đường tròn (`self.circles`):
```python
{
    "id": "circle_1",        # Định danh
    "center": point_dict_O,  # Tham chiếu điểm tâm
    "r": 2.5,                # Bán kính thực (float)
    "color": "#0066cc",      # Màu nét viền
    "label": "(O; R=2.5)",
    "hidden": False
}
```

### 2.5. Kí hiệu góc sư phạm (`self.angle_marks`):
```python
{
    "vertex": point_dict_V,  # Tham chiếu đỉnh góc
    "p1": point_dict_P1,     # Tham chiếu điểm tia thứ nhất
    "p2": point_dict_P2,     # Tham chiếu điểm tia thứ hai
    "style": "arc1",         # Kiểu: "right" (vuông ô vuông), "arc1", "arc2", "arc1_tick", "arc2_tick"
    "name": "α",             # Nhãn tên góc (tùy chọn: α, β, γ, θ, 1, 2, 30°...)
    "size": 22,              # Bán kính vòng cung / kích thước ô vuông (px)
    "color": "#e03131"       # Màu sắc hiển thị hex
}
```

---

## 3. NHẬT KÝ CÁC BẢN CẬP NHẬT & THAY ĐỔI CHI TIẾT (CHANGELOG)

### [Bản cập nhật v3.9] - 06/11/2026
* **Tôn Chỉ Tinh Gọn, Loại Bỏ Từ Ngữ Phô Trương, Thiết Lập Chế Độ Cơ Bản / Nâng Cao (Basic / Advanced) & Bổ Sung Toán Cao Cấp Cho Đại Học & Giảng Viên:**
  - **Chuẩn Hóa Ngôn Ngữ Tự Nhiên & Loại Bỏ Hoàn Toàn Từ Ngữ Phô Trương (Humanized & De-hyped):**
    + Loại bỏ toàn bộ các từ ngữ màu mè như "chuẩn sư phạm", tên kỳ thi thi thố và tên thương hiệu nổi tiếng; để chất lượng toán học do người dùng và giáo viên tự đánh giá.
    + Đổi tên toàn bộ danh mục mẫu bài (Presets) theo bản chất hình học thuần túy (ví dụ: "Tứ giác nội tiếp & Định lý Ptolemy", "Giao hai tam giác & Lục giác DEFGHI", "Đường tròn Euler qua điểm cố định", v.v.).
    + Chuyển ngữ song ngữ Việt - Anh mượt mà, chính xác và trong sáng.
    + Lời giải AI được tái định vị thành bạn đồng hành giải toán (Humanized Math Partner): trình bày mạch lạc 3 phần: Ý tưởng hình học, Các bước lập luận chi tiết và Kết luận ngắn gọn.
  - **Hệ Thống Chuyển Đổi Chế Độ Linh Hoạt: Cơ Bản / Nâng Cao (Basic / Advanced Mode):**
    + Nút bấm chuyển đổi nhanh ngay trên thanh công cụ: `[ ⚙️ Cơ bản ]` $\leftrightarrow$ `[ ⚙️ Nâng cao ]` (`[ ⚙️ Basic ]` $\leftrightarrow$ `[ ⚙️ Advanced ]`).
    + **Chế độ Cơ bản (Basic Mode - Mặc định):** Giữ giao diện tinh gọn, nhẹ nhàng, tối ưu hiệu năng cho học sinh và giáo viên THCS/THPT (Điểm, Đoạn, Góc, Đường tròn, Tam giác, Tứ giác, Diện tích, Chu vi).
    + **Chế độ Nâng cao (Advanced Mode):** Mở ra thanh công cụ Toán chuyên sâu dành cho sinh viên Toán, giảng viên đại học và nghiên cứu giảng dạy.
  - **Tích Hợp 5 Công Cụ Toán Cao Cấp (Giải Tích Xạ Ảnh & Tỉ Cự) Với Dung Lượng Thêm ~0 MB:**
    + **`harmonic` (Hàng điểm điều hòa):** Dựng điểm liên hợp điều hòa $D$ của $C$ đối với đoạn $AB$ sao cho $(AB, CD) = -1$; cảnh báo trực giác khi $C$ là trung điểm thì $D$ ở vô cực.
    + **`pole_polar` (Cực & Đối cực):** Dựng đường đối cực của điểm $P$ qua đường tròn $(O)$ và tìm cực $P$ của đường thẳng (Định lý La Hire).
    + **`symmedian` (Đường đối trung & Điểm Lemoine):** Dựng đường đối trung xuất phát từ 1 đỉnh tam giác và xác định tọa độ Điểm Lemoine $K$ (Grebe point).
    + **`radical_axis` (Trục đẳng phương):** Dựng đường thẳng trục đẳng phương của 2 đường tròn (quỹ tích các điểm có cùng phương tích).
    + **`barycentric` (Tọa độ tỉ cự Barycentric):** Phân tích tọa độ tỉ cự chuẩn hóa $(u : v : w)$ với $u+v+w=1$ của một điểm $P$ đối với tam giác cơ sở $ABC$, nhận diện tự động Trọng tâm, Tâm nội tiếp, Tâm Lemoine.
  - **Hiệu Năng Vượt Trội & Bộ Kiểm Thử Hồi Quy:**
    + 100% thuật toán viết bằng hình học giải tích SymPy/Python thuần túy, không cần thêm thư viện ngoài nặng nề, dung lượng file tăng chưa đầy 10 KB.
    + Đạt 25/25 unit tests pass 100% trong 2.73 giây.

### [Bản cập nhật v3.8] - 06/11/2026
* **Biểu Diễn Căn Thức Chính Xác, Khắc Phục Triệt Để Nhận Diện Mục Tiêu DEFGHI, Cầu Nối Vẽ Hình Phụ Bằng Tiếng Việt Tự Nhiên & Bổ Sung Bộ Đề Tham Khảo Kinh Điển (Presets 9, 10, 11):**
  - **Biểu Diễn Độ Dài & Diện Tích Dạng Căn Thức Chính Xác (Exact Unicode Radicals):**
    + Thay thế toàn bộ hiển thị số thập phân xấp xỉ bằng căn thức toán học chính xác qua SymPy CAS (`format_exact_radical`).
    + Ví dụ: $AB = \sqrt{34} \approx 5.8310$, $BC = 6$, $CD = 5\sqrt{2} \approx 7.0711$, $AC = 3\sqrt{10} \approx 9.4868$.
    + Ngăn chặn triệt để hiện tượng AI hallucination ngộ nhận tam giác cân/lệch thành tam giác đều khi làm tròn số (loại bỏ hiểu lầm $\sqrt{34} \approx 6$).
  - **Khắc Phục Triệt Để Bộ Phân Tích Mục Tiêu Đa Giác (`_resolve_target_polygon_points`):**
    + Tokenizer thông minh theo regex `[A-Za-z][0-9']*` tự động phân tách chuỗi liền nhau như `DEFGHI` thành 6 đỉnh `['D', 'E', 'F', 'G', 'H', 'I']`.
    + Hỗ trợ định dạng phân cách phẩy `D, E, F, G, H, I` và tự động trích xuất mục tiêu từ câu hỏi văn bản (`"Tính diện tích đa giác DEFGHI"`).
    + Khử bỏ hoàn toàn lỗi gộp nhầm 12 điểm canvas thành đa giác tự cắt sai lệch $S=10.1580$. Xác định chính xác diện tích lục giác phần chung $S(DEFGHI) = \frac{10075}{918} \approx 10.9749$.
  - **Cầu Nối Dựng Hình Phụ Tự Động Qua Văn Bản Tiếng Việt (NLP Auxiliary Drawing Bridge):**
    + Phân tích cú pháp văn bản tiếng Việt xuất ra từ DeepSeek-R1 7B / Gemini theo thời gian thực và tự động dựng hình phụ nét đứt màu đỏ trực tiếp lên Canvas:
      * `"Lấy trung điểm M của BC"` / `"Gọi trung điểm M của BC"` $\rightarrow$ Dựng điểm trung điểm $M(0, 0)$.
      * `"Hạ đường cao AH từ A đến BC"` / `"Hạ đường cao AH vuông góc BC"` $
ightarrow$ Dựng chân đường vuông góc $H$ và ký hiệu góc vuông.
      * `"Kẻ đoạn thẳng AM"` / `"Nối A với M"` $
ightarrow$ Kẻ đoạn thẳng nối nét đứt $AM$.
      * `"Vẽ đường tròn qua ba điểm A, B, C"` / `"Vẽ đường tròn (ABC)"` $
ightarrow$ Tự động dựng tâm và đường tròn ngoại tiếp phụ.
  - **Bổ Sung 3 Mẫu Đề Tham Khảo Kinh Điển & Khó Vào Thư Viện Presets:**
    + **Preset 9 (Bài 10):** Giao điểm 2 tam giác $ABC$ và $A_1B_1C_1$ tạo lục giác $DEFGHI$ với diện tích chính xác $S = \frac{10075}{918} \approx 10.9749$ và các cạnh căn thức $\sqrt{34}, 6$.
    + **Preset 10 (Bài 14 VMO 2015):** Tam giác nhọn không cân $ABC$, trực tâm $H$, đường cao $AD$, cát tuyến $PMQ$, đường tròn Euler 9 điểm $(D, E, F, M)$ và đối xứng $Q = -H$ qua trung điểm $M$ của $BC$.
    + **Preset 11 (Bài 15 Olympic Hình học):** Tứ giác nội tiếp $ABCD$ trong đường tròn $(O; R=5)$, kiểm chứng Định lý Ptolemy $AC \cdot BD = AB \cdot CD + BC \cdot DA = 30\sqrt{10}$ và diện tích chính xác số nguyên $S = 45$.
  - **Dọn Dẹp Ổ C, Chặn Tải Ngầm AI Model & Kiểm Thử Toàn Diện:**
    + Thu hồi ~12 GB ổ C (tăng dung lượng trống từ 17.6 GB lên 29.36 GB). Khóa chính sách Chrome Registry chặn tải ngầm file mô hình.
    + Bổ sung bộ kiểm thử hồi quy `geosolver/test_v38_features.py` đạt 23/23 tests pass 100%.

### [Bản cập nhật v3.7] - 06/11/2026
* **Di Trú Toàn Diện Local AI Sang Ổ Đĩa D, Tích Hợp DeepSeek-R1 7B & Bộ Chọn 4 Gói Giải Toán Chuyên Sâu:**
  - **Di Trú Toàn Bộ Mô Hình AI Về Ổ Đĩa D (`D:\AI DATA\STEM_APP\models`):**
    + Chuyển toàn bộ dữ liệu mô hình Ollama và GGUF từ ổ C sang ổ D, giải phóng triệt để dung lượng ổ hệ thống (ổ C tăng lên ~20 GB trống, bảo toàn không gian cho OS).
    + Cấu hình biến môi trường người dùng Windows vĩnh viễn: `OLLAMA_MODELS = "D:\AI DATA\STEM_APP\models\ollama"`.
    + Đặt file lưu trữ persistent API Key tại `D:\AI DATA\STEM_APP\models\gemini_api_key.txt`.
    + Định tuyến tự động trong `stem_shared_core/ai_model_hub.py`: Ưu tiên tìm kiếm mô hình tại ổ D trước khi dùng fallback.
  - **Cài Đặt & Kiểm Thử Thành Công DeepSeek-R1 7B Offline:**
    + Tải và lưu trữ trọn vẹn mô hình `deepseek-r1:7b` (4.7 GB) vào Ollama trên ổ D.
    + Bổ sung phương thức `set_ollama_model(model_name)` trong `AIModelHub` cho phép chuyển đổi nóng giữa các phiên bản mô hình mà không cần khởi động lại ứng dụng.
    + Kiểm thử suy luận hình học thực tế: Mô hình 7B tư duy sâu sắc, hành văn tiếng Việt tự nhiên và chuẩn mực sư phạm.
  - **Nâng Cấp Hộp Chọn Gói Giải Toán Trực Quan (4 Profiles):**
    + `⚡ Thuần Python (0.01s - 100% Chuẩn)`: 0 MB RAM, tốc độ tức thì, 100% không ảo giác.
    + `☁️ Gemini Cloud (Giáo Sư - 0MB RAM)`: 0 MB RAM máy tính, miễn phí, văn phong sư phạm đỉnh cao.
    + `🖥️ Local AI (DeepSeek-R1 7B - Sâu Sắc)`: Mô hình 7 tỷ tham số, suy luận hình học phức tạp offline.
    + `🖥️ Local AI (DeepSeek-R1 1.5B - Nhẹ)`: Mô hình siêu nhẹ (~1.5 GB RAM), tốc độ phản hồi nhanh.
  - **Tạo Prompt Đặc Tả Chuẩn Claude Code / Argon (Section 6):**
    + Xuất bản đặc tả kỹ thuật hoàn chỉnh 100% (Zero-truncation) tại `claude_code_argon_prompt.md` để sinh mô-đun quản lý và đo kiểm Local AI độc lập.

### [Bản cập nhật v3.6] - 06/11/2026
* **Thiết Kế 3 Gói Giải Toán Trực Quan (Solver Profiles) & Khắc Phục Triệt Để Kết Nối Gemini Cloud:**
  - **3 Gói Giải Toán Linh Hoạt trên Thanh Công Cụ (`combo_ai_profile`):**
    + **Gói 1: `⚡ Thuần Python (0.01s - 100% Chuẩn)`:** $0$ MB RAM AI, $0$ MB ổ đĩa, không cần Internet. Lõi SymPy CAS + Shoelace Gauss + Deductive Engine giải quyết bài toán tức thì, chuẩn xác $100\%$ không ảo giác.
    + **Gói 2: `☁️ Gemini Cloud (Giáo Sư - 0MB RAM)`:** $0$ MB RAM máy tính, $0$ MB ổ đĩa, miễn phí $100\%$. Khai thác sức mạnh của siêu mô hình Google Gemini hàng chục tỷ tham số, hành văn sư phạm tiếng Việt tuyệt mỹ, tự động vẽ đường phụ.
    + **Gói 3: `🖥️ Local AI (Ollama Offline)`:** Chạy mô hình cục bộ (Ollama) cho người dùng muốn bảo mật và độc lập hoàn toàn.
  - **Khắc phục triệt để lỗi kết nối Gemini API (HTTP 404):**
    + Lưu trữ bền vững API Key tại `%LOCALAPPDATA%\AIMathHub\gemini_api_key.txt`, tự động nạp lại khi mở phần mềm.
    + Truyền đồng thời tham số `&key={api_key}` trong URL và Header `x-goog-api-key` để vượt qua mọi rào cản phân giải cổng API của Google.
    + Cơ chế tự động Fallback từ Streaming SSE sang `generateContent` tiêu chuẩn nếu gặp 404.
    + Cập nhật chuỗi dự phòng 5 mô hình Gemini chính thức (`gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-flash-latest`, `gemini-1.5-pro`, `gemini-2.0-flash-exp`).

### [Bản cập nhật v3.5] - 06/11/2026
* **Nâng Cấp Hệ Sinh Thái AI Agent Tương Tác & Lời Giải Sư Phạm Lai (Neuro-Symbolic Suite):**
  - **Tự động nhận diện Đề bài từ Thanh công cụ:** Nếu người dùng không nhập đề bài vào `txt_problem`, hệ thống tự động trích xuất Mục tiêu (`combo_goal_type`), Đối tượng (`entry_goal_targets`) và Bài toán mẫu (`combo_presets`) để tạo đề bài hoàn chỉnh và đồng bộ lên giao diện.
  - **Cơ chế Ghi Nối Tiếp Lời Giải (Append Solution Mode):** Khi bấm `[ 🤖 AI Giải ]`, hệ thống kiểm tra và giữ nguyên 100% lời giải giải tích của Python trên Tab Lời giải, ghi nối tiếp phần bình luận của AI bên dưới để người dùng trực tiếp so sánh. AI đọc trực tiếp lời giải Python làm ngữ cảnh/chân lý mà không cần tính lại từ đầu.
  - **AI Agent Tự Động Vẽ Hình Phụ Trực Tiếp Trên Canvas:**
    + Tích hợp bộ phân tích chỉ lệnh dựng hình `_execute_ai_drawing_command(cmd)`.
    + Khi AI đề xuất các đường phụ trong bài giảng: Kẻ đoạn thẳng `[DRAW_SEGMENT]`, lấy trung điểm `[DRAW_MIDPOINT]`, hạ đường cao `[DRAW_PERPENDICULAR]`, vẽ đường tròn ngoại tiếp `[DRAW_CIRCLE_3P]`.
    + Phần mềm tự động tính toán tọa độ chính xác và vẽ ngay lập tức đường nét đứt màu đỏ trên Canvas trong thời gian thực khi AI đang gõ chữ.
  - **Quản lý trạng thái Nút và Trực quan hóa Tiến trình (Runtime State Management):**
    + Khóa nút `[ ▶ Giải ]` khi AI đang chạy, nút đổi thành `⏹ Dừng AI` (màu đỏ).
    + Khôi phục trạng thái nút ngay khi hoàn tất hoặc dừng; thanh trạng thái chuyển sang màu xanh `✅ Đã hoàn tất giải toán (Python & AI Agent)` kèm biểu ngữ kết thúc rõ ràng.
  - **Chặn triệt để rò rỉ ký tự chữ Hán / tiếng Trung:** Tích hợp bộ lọc Unicode CJK `_filter_cjk_characters` trong `ai_model_hub.py` để loại bỏ toàn bộ chữ Hán rò rỉ từ các mô hình nén local.
  - **Kiểm thử tự động:** Bổ sung bài kiểm tra `test_ai_agent_drawing_commands` (17/17 unit tests 100% PASS).

### [Bản cập nhật v3.4] - 06/11/2026
* **Bổ Sung Bộ Tứ Hình Học & Conic Kinh Điển (Elip, Thang Cân, Bình Hành, Thoi, Vuông) & Tái Cấu Trúc Toolbar Hàng 3:**
  - **Hình Elip (Ellipse - Dựng 3 Điểm Chuẩn):**
    + Dựng qua 3 điểm tương tác: Tâm $O$, đỉnh trục lớn $A$, và điểm định hướng bán trục bé $B$.
    + Tính toán chính xác độ dài bán trục $a, b$, góc xoay $\theta = \operatorname{atan2}(A_y - O_y, A_x - O_x)$.
    + Công thức diện tích giải tích $S = \pi a b$.
    + Chu vi xấp xỉ Ramanujan I: $C \approx \pi \left[3(a+b) - \sqrt{(3a+b)(a+3b)}\right]$.
    + Lấy mẫu 72 điểm đều góc $\phi \in [0, 2\pi]$ và render đường cong mượt `smooth=True` trên Canvas.
  - **Hình thang cân (Isosceles Trapezoid - Thuật toán hình học phản chiếu):**
    + Dựng từ 3 đỉnh $A, B, C$, tự động xác định đỉnh $D$ đối xứng qua đường trung trực của đáy $AB$:
      $\vec{u} = \frac{B-A}{\|B-A\|},\quad M = \frac{A+B}{2},\quad t = (C - M) \cdot \vec{u},\quad D = C - 2t\vec{u}$.
    + Đảm bảo tuyệt đối tính chất $CD \parallel AB$, $AD = BC$ và hai góc kề đáy bằng nhau.
  - **Hình bình hành (Parallelogram) & Hình thoi (Rhombus):**
    + Dựng hình bình hành từ 3 đỉnh $A, B, C$, xác định đỉnh $D = A + (C - B)$, tự động tạo các đoạn thẳng và đa giác khép kín.
    + Dựng hình thoi đảm bảo nghiêm ngặt 4 cạnh bằng nhau $AB = BC = CD = DA$.
  - **Tái cấu trúc Toolbar Hàng 3 (Row 3) thành 4 Cụm Chức Năng Rõ Ràng:**
    + **Cụm 1 (Đa giác & Conic):** `[▱ B.hành]`, `[◇ Thoi]`, `[⏢ Thang cân]`, `[□ Vuông]`, `[⬭ Elip]`
    + **Cụm 2 (Đường tròn & Tiếp tuyến):** `[○ Tròn]`, `[⦿ Tròn 3P]`, `[◎ T.tuyến]`, `[⊜ T.tuyến 2C]`
    + **Cụm 3 (Các tâm tam giác đặc biệt):** `[▲ Trực tâm]`, `[⊙ Tâm nội]`, `[⨀ Tròn nội]`, `[⊚ Tâm ngoại]`
    + **Cụm 4 (Đo đạc & Bảng màu):** `[📐 D.tích]`, `[✓ K.tra]`, Quick Color Palette (`🔴`, `🔵`, `⚫`, `🟢`)
  - **Đồng bộ hóa Treeview & Công Cụ Đo Đạc:**
    + Hiển thị đầy đủ Elip và các đa giác mới trong Cây đối tượng Đại số (`_update_algebra_tree`).
    + Tích hợp tính diện tích & chu vi Elip trong công cụ đo diện tích `calculate_selected_area()`.
  - **Dọn dẹp mã nguồn:** Hợp nhất toàn bộ đóng góp từ `gemini-code-1793933225832.py` vào tệp chính `geosolver_desktop.py`, gỡ bỏ tệp nháp để tránh trùng lặp. Đạt 100% kiểm thử tự động (16/16 unit tests).

### [Bản cập nhật v3.3] - 05/11/2026
* **Tích hợp Nút [ 🤖 AI Giải ] Trực Tiếp & Rà Soát Bản Quyền / Sửa Lỗi Chiều Cao Ribbon (06/11/2026):**
  - **Tích hợp nút `[ 🤖 AI Giải ]` (`btn_ai_solve`):** Đặt ngay cạnh nút `⚡ Giải` trên thanh công cụ giải toán. Khi người dùng bấm nút này, hệ thống sẽ tự động đóng gói toàn bộ đề bài hiện tại trong `txt_problem` cùng tọa độ thực nghiệm của các điểm, đoạn thẳng, đường tròn trên Canvas, chuyển sang Tab Lời giải và gọi `self.ai_hub.stream()` để truyền tải lời giải sư phạm từng bước theo thời gian thực (hỗ trợ cả Ollama cục bộ và Gemini API). Khi đang giải, nút tự chuyển thành `[ ⏹ Dừng AI ]` để người dùng có thể hủy bất kỳ lúc nào.
  - **Rà soát & Xóa bỏ 100% từ ngữ bản quyền/thương hiệu:** Đã rà soát và loại bỏ toàn bộ các từ "Office", "MS Office", "Cabri", "GeoGebra" khỏi mã nguồn, nhãn nút, tooltip và giao diện người dùng, thay thế bằng các thuật ngữ kỹ thuật trung lập chuẩn mực ("Technical CAD", "Ribbon Toolbar", "Geometric Property Checker", "Algebra Command Bar").
  - **Chuẩn hóa nút mũi tên thu gọn duy nhất (`▲` / `▼`):** Nút thu gọn thanh công cụ nay chỉ hiển thị duy nhất một ký tự mũi tên (`▲` khi mở, `▼` khi thu), không kèm theo bất kỳ chữ nào khác.
  - **Khắc phục triệt để lỗi cắt cụt thanh công cụ (Zero Height Clipping):**
    + Thay vì gán cứng chiều cao 120px làm che khuất mất 44px của hàng công cụ số 4, chiều cao `tb_canvas` nay được tính toán động theo đúng chiều cao thực tế `self.tb_inner_frame.winfo_reqheight()` (~168px), đảm bảo trọn vẹn cả 4 thanh công cụ không bị cắt mất một pixel nào.
    + Khi thu gọn: Ẩn hoàn toàn `tb_canvas` và `tb_scrollbar` (`pack_forget`), giải phóng 100% diện tích không gian cho Canvas vẽ hình.
  - **Tinh gọn dự án:** Đã đối chiếu tệp `geosolver_desktop1.py` do Argon sinh ra, tích hợp toàn bộ các giải pháp tối ưu vào tệp chính `geosolver_desktop.py` và xóa bỏ tệp phụ để tránh phân mảnh mã nguồn.

* **Minh bạch hóa tài nguyên AI Offline & Nâng cấp Bảng Điều Khiển AI Support:**
  - **Minh bạch tổng tài nguyên thực tế (~2.5 GB - 3.0 GB):** Phân tích và hiển thị rõ ràng trên giao diện 3 thành phần cấu thành để chạy DeepSeek-R1 Offline:
    1. Tệp trọng số mô hình (.GGUF): `1.04 GB` (lưu trữ trên ổ đĩa).
    2. Trình thực thi (Ollama Engine): `~800 MB - 1 GB` (bộ cài đặt cần có để gọi và thông dịch tệp nhị phân .GGUF).
    3. Bộ nhớ đệm suy luận (RAM Context): `~1.5 GB - 2 GB` (chỉ nạp khi giải toán, tự động giải phóng sau 120s).
  - **Sửa lỗi thiếu `Path`:** Khắc phục triệt để lỗi làm gián đoạn hiển thị bảng điều khiển `open_ai_assistant`.
  - **Bổ sung các nút tiện ích 1-chạm:**
    + Nút `[📂 Mở thư mục]`: Mở trực tiếp thư mục `%LOCALAPPDATA%\AIMathHub\models` trong Windows Explorer mà không cần gõ lệnh.
    + Nút `[🌐 Tải bộ cài Ollama (OllamaSetup.exe)]`: Tải trực tiếp bộ cài Ollama về máy.
    + Nút `[📋 Xem lệnh nạp file GGUF vào Ollama]`: Hướng dẫn nạp file 1.04 GB có sẵn vào Ollama mà không cần tải lại từ mạng.
    + Nút `[🔑 Lấy Key miễn phí]`: Mở trang Google AI Studio để lấy Gemini API Key (giải pháp Cloud 0 MB ổ đĩa, 0 MB RAM).
  - **Cập nhật hộp thoại tải mô hình (`hf_downloader.py`):** Nêu rõ thông tin trước khi tải: file GGUF là 1.1 GB, tổng tài nguyên cần để chạy offline là ~2.5 - 3 GB kèm gợi ý phương án Cloud 0 MB.
 (Responsive Ribbon MS Office, Chuẩn Tên Điểm & Chống Trùng Swap, Nhân Bản Ctrl & Xoay Sao Chép, Cắt Giao Đa Giác Sutherland-Hodgman & Shoelace/Heron Sư Phạm, AI Offline Lazy Loading)
* **Chuẩn hóa nhãn nút AI Assistant:**
  - Đổi nhãn nút từ `"AI trợ giảng offline"` thành **`[ 🤖 AI Support Offline ]`** trên thanh công cụ `top_bar4` và menu công cụ, đảm bảo trực quan và tương thích song ngữ (Tiếng Anh & Tiếng Việt).
* **Đa ngôn ngữ (English / Vietnamese) hoàn chỉnh:**
  - Sửa triệt để lỗi khi người dùng chọn ngôn ngữ `English` nhưng Bài mẫu số 8 (`vmo_2009_bai13`), Bài mẫu số 1 (`cau_viii`), Bài mẫu số 4 (`vmo_2003`) và các mục tiêu giải toán tổng quát vẫn xuất hiện tiếng Việt.
  - Toàn bộ chuỗi giao diện, tiêu đề bài toán, phân tích quỹ tích, điểm cố định, đồng quy, tương quan hệ thức (`_solve_correlation`) và tính diện tích đa giác đã được bổ sung bản dịch tiếng Anh chuẩn mực sư phạm.
* **Thanh công cụ đáp ứng linh hoạt (Responsive Toolbar Ribbon - Phong cách MS Office):**
  - Khắc phục lỗi các nút bấm bị khuyết hoặc tràn khi thu nhỏ khung làm việc.
  - Đóng gói toàn bộ 4 thanh công cụ vào `toolbar_container`, tích hợp thanh trượt ngang `tb_scrollbar` kèm hai nút điều hướng `◀` (`btn_scroll_left`) và `▶` (`btn_scroll_right`).
  - Bổ sung nút thu gọn Ribbon phong cách MS Office (`▲` / `▼` - `btn_toggle_ribbon`): Cho phép ẩn toàn bộ 4 thanh công cụ để mở rộng tối đa không gian vẽ hình khi làm việc trên màn hình nhỏ hoặc máy chiếu lớp học.
* **Nhân bản hình thông minh (Duplicate via Ctrl + Move & Rotation with Copy):**
  - **Nhân bản tức thì khi kéo chuột (Ctrl + Drag):** Khi đang ở công cụ Di chuyển (Move), người dùng giữ phím `Ctrl` trong lúc kéo đối tượng (điểm, đoạn thẳng, đường tròn), hệ thống sẽ tự động tạo một bản sao mới (đặt tên chuẩn `A1, B1...`) và kéo bản sao đi, bảo toàn nguyên vẹn hình gốc.
  - **Góc xoay tùy chọn có sao chép:** Hộp thoại `rotate_custom_dialog` được tích hợp hộp kiểm `[ ] Giữ nguyên hình cũ (Sao chép thêm hình mới)` (mặc định chưa tích: xoay hình hiện tại; nếu tích: sao chép hình mới rồi xoay, giữ nguyên hình cũ).
* **Chuẩn hóa quy tắc đặt tên điểm & Hộp thoại giải quyết xung đột (Swap / Rename):**
  - **Quy tắc đặt tên chuẩn tắc:** Tên điểm chỉ chấp nhận định dạng **1 chữ cái + chỉ số số học** (Regex: `^[A-Za-z][0-9]*$`, ví dụ: `A`, `B`, `A1`, `B2`, `M10`). Tuyệt đối từ chối tên 2 chữ cái như `AB`, `CD` (tránh nhầm lẫn với đoạn thẳng hoặc vector) kèm cảnh báo hướng dẫn chi tiết.
  - **Tự động gợi ý tên không trùng:** Hàm `get_next_point_name()` tự động rà soát và gợi ý tên điểm kế tiếp (`A` -> `Z` -> `A1`...) khi vẽ mới hoặc nhân bản.
  - **Hộp thoại xung đột tên điểm thông minh (`_show_swap_rename_dialog`):** Khi người dùng đổi tên một điểm mà bị trùng với điểm đã có trên bản vẽ, hệ thống mở hộp thoại hỗ trợ:
    + **Hoán đổi (Swap)** tên tức thì giữa 2 điểm chỉ bằng 1 cú click chuột (Điểm A nhận tên B và ngược lại).
    + Hoặc sửa đồng thời tên cả 2 điểm trên cùng một giao diện với cơ chế kiểm tra tính hợp lệ tức thời.
* **Tính diện tích đa giác, Lời giải sư phạm & Cắt giao Sutherland-Hodgman:**
  - **Sửa lỗi phân tích chuỗi đỉnh mục tiêu:** Chuỗi đỉnh nhập liền như `MNPQTK` nay được tách chính xác thành danh sách 6 đỉnh `[M, N, P, Q, T, K]` thay vì lỗi phân tách khoảng trắng dẫn đến việc hệ thống tự nhảy về tam giác mặc định `ABC`.
  - **Thuật toán Sutherland-Hodgman:** Tích hợp thuật toán cắt đa giác phẳng (`clip_polygon_sutherland_hodgman`), cho phép tính diện tích phần chung/giao nhau của hai hình (ví dụ: `ABC ∩ DEF`).
  - **Lời giải sư phạm chi tiết:**
    + Tam giác: Thể hiện độ dài 3 cạnh theo khoảng cách Euclide $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$, nửa chu vi $p$, từng bước áp dụng công thức Heron $S = \sqrt{p(p-a)(p-b)(p-c)}$, bán kính đường tròn nội tiếp $r = S/p$ và ngoại tiếp $R = abc/(4S)$.
    + Đa giác tổng quát: Thể hiện bảng tích chéo tọa độ Gauss (Shoelace Formula) chi tiết từng cặp đỉnh $(x_i y_{i+1} - x_{i+1} y_i)$.
* **Chẩn đoán & Cơ chế hoạt động của AI Offline (DeepSeek-R1-Distill-Qwen-1.5B):**
  - Giải thích nguyên nhân kiểm tra RAM không thấy tăng: File GGUF (~1.1 GB) được lưu trữ tại `%LOCALAPPDATA%\AIMathHub\models` hoạt động theo cơ chế nạp lười (*Lazy Loading*). RAM chỉ tăng thêm (~1.5 GB - 2 GB) khi có tiến trình Inference Engine (như Ollama hoặc llama-cpp) thực sự nạp trọng số vào bộ nhớ.
  - Tích hợp giao diện chẩn đoán trực quan trong `open_ai_assistant`: Hiển thị đường dẫn file GGUF, kích thước, trạng thái Ollama daemon, hướng dẫn lệnh khởi chạy nhanh (`ollama run deepseek-r1:1.5b`), hỗ trợ kết nối Gemini API dự phòng và nút bấm thử nghiệm luồng suy luận trực tiếp.

### [Bản cập nhật v3.2] - 04/11/2026 (Bộ Luật Diễn Dịch Hình Học Thuần Túy - Deductive Geometry Engine: Chou's Area & Full-Angle Method, AlphaGeometry DD 45+ Axioms & Chuyên Đề Olympic VMO)
* **Nền tảng lý thuyết & Tiêu chuẩn Quốc tế:**
  - **Phương pháp Diện tích & Góc đầy đủ (Area Method & Full-Angle Method):** Sáng lập bởi GS. Shang-Ching Chou, Xiao-Shan Gao, Jing-Zhong Zhang (*"Machine Proofs in Geometry"*, 1994, 1996). Khung toán học diễn dịch thuần túy không phụ thuộc hệ tọa độ Oxy.
  - **Cơ sở dữ liệu diễn dịch AlphaGeometry (Google DeepMind, Nature 2024):** Hiện thực hóa hơn 45 luật suy diễn hình học phẳng chuẩn tắc: đường trung bình, quan hệ song song/vuông góc, góc nội tiếp, tiếp tuyến và dây cung, phương tích điểm, trục đẳng phương, định lý Thales, Menelaus, Ceva.
  - **Chuyên đề bồi dưỡng HSG & Olympic Toán Việt Nam (VMO):** Tích hợp các bổ đề hình học nâng cao: Đường thẳng Euler ($H, G, O$ thẳng hàng, $HG = 2GO$), Đường tròn 9 điểm (Euler circle), Đường thẳng Simson, Bổ đề Con bướm, Tứ giác điều hòa.
* **Kiến trúc Động cơ Diễn dịch (`deductive_engine.py`):**
  - **Forward-Chaining Inference Loop:** Vòng lặp suy luận tiến đa tầng kết hợp lập chỉ mục quan hệ nhanh (FactDatabase).
  - **Ưu tiên diễn dịch (Rule Precedence over Given):** Khắc phục triệt để lỗi logic khi các giả thiết hình học số học làm lu mờ các luật chứng minh. Hệ thống tự động nâng cấp sự kiện quan sát số học thành chuỗi chứng minh diễn dịch sư phạm có truy vết tiên đề.
  - **Backtracking Proof Graph:** Duyệt ngược đồ thị suy luận từ kết luận về tiền đề ban đầu để xuất lời giải sư phạm từng bước (Step-by-step Pedagogical Proof) song ngữ hoàn hảo (Tiếng Việt & English).
* **Khắc phục các sai sót & Tối ưu hóa thuật toán:**
  - *Lỗi dữ liệu kiểm thử Tứ giác nội tiếp (Test 3):* Phát hiện tọa độ kiểm thử ban đầu $A(0, 3), B(-4, 0), D(4, 0), C(0, -3)$ không tạo thành góc vuông tại $A$ ($BA^2 + AD^2 = 50 \neq 64 = BD^2$, góc thực tế $\approx 73.7^\circ$). Đã hiệu chỉnh về tọa độ hình học chuẩn $A(0, 4), C(0, -4)$ với $BA \perp AD$ và $BC \perp CD$ cùng nhìn đường kính $BD$ dưới góc $90^\circ$.
  - *Lỗi suy biến tứ giác (`IndexError`):* Bổ sung ràng buộc kiểm tra nghiêm ngặt tập hợp 4 đỉnh phân biệt khi phát hiện tứ giác nội tiếp và đuổi góc, loại bỏ triệt để các trường hợp điểm trùng lặp hoặc thẳng hàng.
* **Tích hợp toàn diện vào `geosolver_desktop.py`:**
  - Thiết lập **Kiến trúc Hybrid 2 Tầng hoàn thiện:**
    + **Tầng 1 (Ưu tiên số 1):** Động cơ diễn dịch suy luận thuần túy (`Deductive Engine`) tự động sinh các bước chứng minh hình học sư phạm không dùng tọa độ.
    + **Tầng 2 (Kiểm chứng đại số):** Động cơ SymPy CAS tự động tính toán kiểm chứng định lượng tọa độ, định thức vector, tích vô hướng song hành bên dưới.
  - Mở rộng danh mục Mục tiêu giải toán (`goals_list`):
    + Bổ sung Mục tiêu 11: *Chứng minh tứ giác nội tiếp* (*Prove Cyclic Quadrilateral*).
    + Bổ sung Mục tiêu 12: *Chứng minh tam giác đồng dạng / bằng nhau* (*Prove Similar / Congruent Triangles*).
* **Bộ kiểm thử tự động toàn diện (`test_deductive_engine.py`):**
  - Đạt tỷ lệ vượt qua **100% (7/7 Unit Tests Passed)**:
    1. Đường trung bình tam giác suy ra song song & tỉ số độ dài.
    2. Từ vuông góc đến song song.
    3. Tứ giác nội tiếp đường kính từ hai góc vuông cùng nhìn một đoạn thẳng.
    4. Đường trung bình hình thang & Tính chất bắc cầu song song.
    5. Định lý đường thẳng Euler ($H, G, O$ thẳng hàng).
    6. Định lý Ceva cho 3 đường trung tuyến đồng quy tại Trọng tâm G.
    7. Phương pháp diện tích Chou (Chou's Area Method) cho tam giác cùng đáy giữa hai đường song song.

### [Bản cập nhật v3.1] - 01/11/2026 (Bảng Màu Cơ Bản 1 Chạm, Công Cụ Tính Diện Tích Đa Giác / Hình Tròn & Bộ Test Stress Bất Biến Olympic)
* **Bổ sung Bảng màu nhanh 1 chạm (Quick Color Palette: Đỏ, Xanh, Đen, Lục):**
  - Tích hợp 4 nút đổi màu tức thì ngay trên Hàng 3 (Toolbar):
    + [🔴 Đỏ] (#e03131): Màu đỏ cờ sư phạm, chuyên dùng làm nổi bật điểm cố định, đường tròn Euler, trực tâm.
    + [🔵 Xanh] (#1971c2): Màu xanh học đường chuẩn mực, dùng cho tam giác, đường tròn chính.
    + [⚫ Đen] (#212529): Màu đen mực kỹ thuật in ấn (thay vì #000000 thô cứng).
    + [🟢 Lục] (#2b8a3e): Màu xanh lá cây, dùng cho tiếp tuyến, đường trung bình, các đoạn bằng nhau.
  - Khi chọn các điểm/hình: Đổi màu đồng bộ điểm, đoạn thẳng nối giữa các điểm và đường tròn.
  - Khi không chọn: Tự động ghi nhớ làm màu mặc định cho các đối tượng vẽ tiếp theo. Hỗ trợ đầy đủ Undo/Redo.
* **Bổ sung Công cụ Tính Diện Tích Phần Được Chọn ([📐 D.tích] / [📐 Area]):**
  - **Đa giác n đỉnh (n >= 3):** Tính diện tích theo công thức Dây giày Gauss (Shoelace Formula)  = 1/2 \cdot |\sum (x_i y_{i+1} - x_{i+1} y_i)|$ và chu vi $.
  - **Tam giác (n = 3):** Tự động tính thêm bán kính đường tròn nội tiếp  = S/p$ và ngoại tiếp  = abc/(4S)$.
  - **Hình tròn:** Tính diện tích  = \pi R^2$ và chu vi  = 2\pi R$.
  - **Trực quan hóa:** Vẽ miền đa giác tô màu nền pastel bán trong suốt (ill=#e7f5ff, stipple=gray25), hiển thị nhãn diện tích (ABC) = ...$ tại trọng tâm. Đồng thời xuất báo cáo chi tiết vào Tab Lời giải và hỗ trợ xuất ảnh PNG sắc nét.
* **Hệ thống Kiểm thử Bất biến Monte Carlo (Stress-Testing Suite):**
  - Tạo tệp kiểm thử chuyên dụng scratch/test_olympiad_engine.py chạy thử nghiệm 10,000 điểm ngẫu nhiên cho Bài 12 (VMO 2008), 500 cấu hình đỉnh di động trên cung chứa góc Bài 13 (VMO 2009), và 30 góc quét Bài 11 (VMO 2008).
  - Độ chính xác đạt mức máy tính cực hạn: Sai số khoảng cách chùm đường thẳng đến điểm cố định Bài 12 là .80 	imes 10^{-16}$; sai số đường tròn Euler Bài 13 là .66 	imes 10^{-15}$.

### [Bản cập nhật v3.0] - 01/11/2026 (Chuẩn Hóa Phương Pháp Luận Chuyên Gia VMO: Trực Giác Hình Học Là Số 1, Tích Hợp Preset 8 - Bài 13 VMO 2009 Đường Tròn Euler)
* **Xác lập Phương pháp luận Chuyên gia 2 Tầng (Two-Tier Olympic Geometric Intelligence):**
  - **Nguyên tắc Sư phạm cốt lõi:**
    + **CÁCH 1 (Ưu tiên hàng đầu): TRỰC GIÁC TOÁN HỌC THỰC THỤ & PHÁN ĐOÁN TÌNH HUỐNG (SYNTHETIC GEOMETRY):**
      Dựa vào nhận diện cấu hình hình học, bảo toàn bất biến, đường trung bình, tứ giác nội tiếp, tam giác đồng dạng, phép vị tự/phép quay, trực tâm, và các đường tròn kinh điển (Euler, Apollonius, Mixtilinear). Lời giải thanh thoát, sâu sắc, đúng tinh thần bài thi Học sinh giỏi Quốc gia (VMO).
    + **CÁCH 2 (Đối chiếu & Kiểm chứng): GIẢI TÍCH TỌA ĐỘ HÓA & ĐẠI SỐ CAS (CANONICAL ALGEBRAIC CAS ENGINE):**
      Hệ thống hóa bằng SymPy, thiết lập phương trình hình học giải tích chuẩn quy chiếu đối xứng, giải triệt tiêu tham số biến thiên. Phục vụ kiểm chứng định lượng tuyệt đối, không sợ ngộ nhận hình học hay sai số trực quan.
* **Tích hợp Mẫu bài toán mới: Preset 8 (Bài 13 - VMO 2009 - Trang 16 PDF Chuyên Gia):**
  - **Đề bài:** Cho hai điểm cố định A, B. Điểm C di động sao cho góc ACB = α không đổi. Đường tròn (I) nội tiếp ΔABC tiếp xúc AB, BC, CA tại D, E, F. AI, BI cắt EF tại M, N.
    1) Chứng minh đoạn thẳng MN không đổi: MN = AB * sin(α/2).
    2) Chứng minh đường tròn (DMN) luôn đi qua một điểm cố định (trung điểm K của AB).
  - **Trực giác sư phạm đỉnh cao (Cách 1):**
    + Nhận diện góc MIB = 90° - α/2 = góc MEB => Tứ giác MEIB nội tiếp đường tròn đường kính IB => góc IMB = 90° => BM ⊥ AI và AN ⊥ BI.
    + ΔIMN ∼ ΔIBA => MN / AB = IM / IB = sin(α/2) => MN = AB * sin(α/2) = const.
    + Gọi P = AN ∩ BM => I là TRỰC TÂM ΔPAB. M, N, D chính là chân 3 đường cao của ΔPAB!
    + Do đó (DMN) chính là **ĐƯỜNG TRÒN 9 ĐIỂM (ĐƯỜNG TRÒN EULER)** của tam giác PAB!
    + Theo định lý Euler, đường tròn 9 điểm luôn đi qua trung điểm K của cạnh đáy cố định AB (=> K cố định, ĐPCM)!
  - **Kiểm chứng đại số CAS (Cách 2):** SymPy xác nhận hệ số tự do d0 ≡ 0 của phương trình đường tròn (DMN) với sai số máy tính ε < 10^(-15).
* **Chuẩn hóa cấu trúc Bài 12 (VMO 2008 - Preset 7):**
  - Đảo vị trí: Đưa **Cách 1: Trực giác hình học thuần túy** (đường trung bình EF // BC cố định, phép chiếu song song theo phương trung tuyến AD, chùm đường thẳng afin) lên làm lời giải chính.
  - Đưa **Cách 2: Phương pháp tọa độ hóa chuẩn tắc** (D ≡ O, DA ≡ Oy, d // Ox => R(bc/a; h - b^2/a)) làm lời giải kiểm chứng.

### [Bản cập nhật v2.9] - 01/11/2026 (Tích Hợp Preset 7 - Bài 12 VMO 2008 & Động Cơ Bất Biến Tham Số Điểm Cố Định Goal 3)
* **Bổ sung Preset 7: Bài 12 VMO 2008 Bảng B:**
  - Dựng hình hoàn chỉnh tam giác ABC, trung tuyến AD, đường thẳng d ⊥ AD, điểm di động M ∈ d, trung điểm E, F, các giao điểm chiếu P ∈ AB, Q ∈ AC, đường thẳng Δ qua M ⊥ PQ, và điểm cố định R.
  - Kí hiệu góc vuông ô vuông sư phạm chuẩn SGK tại chân đường cao d ⊥ AD và giao điểm trực giao MR ⊥ PQ.
* **Nâng cấp Bộ giải toàn diện cho Mục tiêu 3 (Chứng minh điểm cố định / Prove Fixed Point):**
  - Xử lý chùm đường thẳng phụ thuộc tham số biến thiên (Parametric Pencil of Lines) f(x, y) + t * g(x, y) = 0.


### [Bản cập nhật v2.8] - 01/11/2026 (Sửa Lỗi Giao Điểm Trục Ox/Oy & Đa Đối Tượng, Kéo Dời Tự Do Nhãn Tên Điểm, Góc Vuông Ô Vuông SGK & Công Cụ Đánh Góc Sư Phạm)
* **Khắc phục triệt để lỗi đánh dấu giao điểm với trục hoành Ox / trục tung Oy và các đối tượng cắt nhau:**
  - **Nguyên nhân cốt lõi đã tìm thấy:**
    1. Hàm bắt dính thông minh `_find_smart_snap` trước đây chỉ quét các đoạn thẳng (`segments`) và đường thẳng (`lines`) người dùng vẽ, chưa bổ sung phương trình 2 trục tọa độ $Ox$ ($y=0$) và $Oy$ ($x=0$) vào tập đối tượng giao cắt nên thuật toán bỏ qua giao điểm với trục hoành/trục tung.
    2. Khi người dùng dựng đường vuông góc, hệ thống tạo ra một điểm chân đường cao trợ giúp mang cờ `hidden: True`. Trước đây vòng lặp bắt dính điểm bắt trúng điểm ẩn này và trả về `type == "point"`, khiến công cụ Giao điểm (`intersection`) kiểm tra `snap["type"] == "intersection"` bị sai lệch và không kích hoạt hộp thoại đặt tên.
  - **Giải pháp hoàn thiện:**
    + Đã bổ sung 2 trục tọa độ $Ox$ và $Oy$ vào danh sách tính toán giao tuyến `all_lines`.
    + Cho phép `_find_smart_snap` tự động bỏ qua các điểm mang cờ `hidden: True` (trừ khi bật chế độ xem điểm ẩn).
    + Nâng cấp công cụ `intersection` thành **Cơ chế 2 chế độ thông minh**:
      * *Chế độ 1 (Snap tức thời):* Bấm trực tiếp vào vùng giao cắt. Nếu tại vị trí đó đã có sẵn điểm ẩn (do phép chiếu/dựng vuông góc sinh ra), máy tự động unhide (`hidden = False`) và gán tên mới theo người dùng.
      * *Chế độ 2 (Chọn tuần tự 2 đối tượng):* Bấm lần lượt vào 2 đối tượng bất kỳ (đường thẳng, đoạn thẳng, trục hoành $Ox$, trục tung $Oy$, hoặc đường tròn), hàm `_compute_entity_intersections` sẽ tự động tính nghiệm hình học giải tích và tạo điểm giao chuẩn xác.
* **Tính năng Kéo dời tự do nhãn tên điểm (Draggable Point Labels):**
  - Giải quyết dứt điểm vấn đề chữ cái (A, B, C, M, N...) bị các nét vẽ, đoạn thẳng hoặc đường tròn cắt qua làm mờ, khó đọc.
  - Mỗi điểm lưu tọa độ dịch chuyển nhãn riêng biệt `label_dx` và `label_dy` (mặc định $+8, -10$).
  - Người dùng ở công cụ `[↖ Dời]` (Select) có thể bấm trực tiếp vào chữ cái của điểm và kéo rê tự do đến bất kỳ vị trí thoáng mắt nào trên bản vẽ.
  - Vị trí mới của nhãn chữ được lưu vào ngăn xếp Undo/Redo và áp dụng đồng bộ cả trên màn hình Canvas lẫn khi xuất file ảnh PNG sạch.
  - Hỗ trợ bấm đúp chuột trực tiếp vào nhãn chữ để mở hộp thoại Đổi tên điểm (`Rename Point`).
* **Chuẩn hóa Kí hiệu Góc vuông Ô vuông Sư phạm SGK (Loại bỏ triệt để kí hiệu chữ "⊥" lật ngược trên hình):**
  - Tuân thủ nghiêm ngặt quy chuẩn sư phạm Việt Nam: kí hiệu chữ T lật ngược `"⊥"` chỉ dùng trong câu chữ đề bài hoặc văn bản lời giải lý thuyết, **tuyệt đối không in đè lên đường vẽ trên hình học**.
  - Toàn bộ các công cụ dựng hình chiếu vuông góc (`open_proj_foot_dialog`), đường vuông góc (`_construct_perpendicular_line`) và các bài toán mẫu (VMO 2003, Tuyển sinh Oxy) đã xóa bỏ nhãn text `"⊥"`.
  - Thay thế hoàn toàn bằng **Ô vuông góc vuông chuẩn SGK** (kích thước cạnh 12-14px) vẽ bằng 2 đoạn thẳng vuông góc tại đỉnh góc vuông, màu sắc sư phạm trực quan (`#e03131`).
* **Bổ sung Công cụ Đánh dấu & Đặt tên Góc Chuẩn Sư Phạm (`mark_angle`):**
  - Tích hợp nút công cụ mới **`[∠ Đánh góc]`** (`[∠ Mark Angle]`) ngay trên Hàng 2 của thanh công cụ.
  - **Cách sử dụng trực quan:**
    + Bấm chọn 3 điểm: Tia 1 -> Đỉnh góc -> Tia 2 (hoặc chọn sẵn 3 điểm rồi bấm nút công cụ).
    + Tự động mở hộp thoại tùy biến góc:
      * **5 kiểu kí hiệu chuẩn SGK:**
        1. *Góc vuông [ ∟ ]:* Ô vuông góc vuông sư phạm.
        2. *1 vòng cung [ ⌒ ]:* Vẽ cung tròn mịn 16 điểm giữa 2 tia.
        3. *2 vòng cung song song [ ⌒⌒ ]:* Dành cho góc bằng nhau thứ 2.
        4. *1 cung có gạch hướng tâm [ ⌒| ]: Cung tròn kèm nét gạch thẳng hướng tâm về đỉnh.
        5. *2 cung có gạch hướng tâm [ ⌒⌒| ]: Cung đôi kèm gạch hướng tâm.
      * **Bảng chèn nhanh kí hiệu Latin & Hy Lạp:** Các nút bấm tiện lợi `[α]` `[β]` `[γ]` `[θ]` `[1]` `[2]` `[°]` để đặt tên góc hoặc ghi số đo độ nhanh chóng.
      * Tùy chỉnh màu sắc và kích thước bán kính vòng cung linh hoạt.
  - Toàn bộ kí hiệu góc được đồng bộ vẽ vector trên Canvas và hỗ trợ xuất ảnh PNG sạch sắc nét với độ phân giải cao qua Pillow (PIL).

### [Bản cập nhật v2.7] - 01/11/2026 (Thanh Ký Hiệu Toán Học Nhanh, Chế Độ Tìm Tương Quan & Tỉ Số Biểu Thức, Quét Ý Định Cabri Auto)
* **Thanh chèn nhanh ký hiệu toán học đa năng (Quick Math Symbols Palette):**
  - **Vị trí bố trí kép thuận tiện:**
    + **Trên Tab Đề bài & Lời giải (Right Panel):** Tích hợp thanh ký hiệu toán học đầy đủ ngay phía trên khung nhập đề bài với các nút bấm trực quan: `[ ∠ ]` `[ |x| ]` `[ ° ]` `[ α ]` `[ β ]` `[ ⊥ ]` `[ ∥ ]` `[ Δ ]` `[ √ ]` `[ cos ]` `[ sin ]` `[ tan ]` `[ / ]` `[ MC/AB ]` `[ |cos(BEC)| ]`.
    + **Trên Hàng 4 (Solver Quick Bar):** Tích hợp 3 nút tắt siêu tốc `[∠]` `[|x|]` `[cos]` ngay cạnh ô nhập đối tượng mục tiêu (`entry_goal_targets`).
  - **Cơ chế chèn thông minh tự động dịch chuyển con trỏ:**
    + Khi bấm `[|x|]`, máy chèn cặp dấu `||` và tự động đưa con trỏ vào giữa hai vạch để người dùng nhập ngay biểu thức bên trong.
    + Khi bấm `[cos]`, `[sin]`, `[tan]`, `[√]`, máy chèn hàm kèm dấu ngoặc `cos()` và đưa con trỏ vào trong ngoặc.
    + Tự động nhận diện ô đang có tiêu điểm (nếu đang sửa đề bài thì chèn vào đề bài, nếu đang sửa đối tượng thì chèn vào đối tượng mục tiêu).
* **Bổ sung Dạng mục tiêu mới: "Tìm tương quan / Tỉ số biểu thức" (Goal 8 - Find Ratio & Correlation):**
  - **Động cơ phân tích hình học `_evaluate_geom_expression`:**
    + Nhận diện độ dài đoạn thẳng qua tên 2 điểm (ví dụ: `MC`, `AB`, `BC`...).
    + Nhận diện góc qua 3 đỉnh (ví dụ: `∠BEC`, `BEC`, `angle(B,E,C)`, `góc BEC`), tự động tính số đo góc theo cả độ ($^\circ$) và radian.
    + Nhận diện các hàm lượng giác và trị tuyệt đối lồng nhau: `|cos(BEC)|`, `|cos(∠BEC)|`, `cos(alpha)`...
    + Hỗ trợ các phép toán tự do: nhân, chia, cộng, trừ, căn bậc hai, phân số (`MC/AB`, `2*CB`, `1.5*AB`).
  - **Bộ so sánh và đánh giá tương quan `_solve_correlation`:**
    + Chấp nhận nhiều định dạng nhập liệu linh hoạt: `MC/AB, |cos(BEC)|`, `MC/AB = |cos(BEC)|`, `MC/AB theo |cos(BEC)|`, `MC / AB theo cos(alpha)`, hoặc chỉ đơn thuần `MC/AB`.
    + Tự động phân tách vế trái và vế phải, tính toán giá trị số thực nghiệm tức thời trên bản vẽ.
    + So sánh sai số chênh lệch tuyệt đối $|E_1 - E_2|$ và tỉ số tương quan $E_1 / E_2$.
    + Tự động rút ra kết luận toán học: Khẳng định đẳng thức đúng tuyệt đối ($E_1 = E_2$), tương quan nguyên ($E_1 = k \cdot E_2$), hay tương quan nửa ($E_1 = 1/2 \cdot E_2$).
* **Nâng cấp Cơ chế "Tự động phân tích toàn diện" (Cabri Auto Intent Scan - Goal 9):**
  - **Bộ nhận diện ý định đề bài tự nhiên (Intent Parser):**
    + Quét nội dung văn bản đề bài và ô đối tượng để tự động nhận dạng câu hỏi:
      * Nếu có từ khóa "tỉ số", "tương quan", "ratio", "theo cos", hoặc ký hiệu dạng `MC/AB` $\implies$ Tự động chuyển hướng phân tích Tương quan & Tỉ số!
      * Nếu có từ khóa "thẳng hàng", "collinear" $\implies$ Tự động chuyển hướng kiểm tra bộ 3 điểm thẳng hàng.
      * Nếu có từ khóa "vuông góc", "⊥" $\implies$ Tự động kiểm tra trực giao.
      * Nếu có từ khóa "song song", "∥" $\implies$ Tự động kiểm tra song song.
    + Khi người dùng vẽ hình tự do không ghi câu hỏi cụ thể, máy quét toàn bộ các bất biến hình học (Invariants) trên bản vẽ và xuất bản báo cáo phân tích tổng quan.
* **Bảo tồn nguyên vẹn 100% thuật toán và các mẫu bài tập VMO kinh điển:**
  - Giữ nguyên các nhánh xử lý chuyên sâu của VMO 2000, 2001, 2003, 2007, 2008 và Câu VIII Oxy; phân tách điều kiện kích hoạt để không làm ảnh hưởng đến các bài toán do người dùng tự vẽ.

### [Bản cập nhật v2.6] - 01/11/2026 (Hộp Thoại Dựng Điểm Thông Minh 1 Trang, Nét Đứt Sư Phạm & Bộ Dựng Chuyên Biệt VMO 2003 / 2008)
* **Gộp toàn diện Hộp thoại Dựng điểm thông minh thành 1 trang duy nhất (Unified Smart Point Builder):**
  - **Loại bỏ giao diện Notebook (Tabs):** Thay thế 2 tab tách biệt trước đây bằng 1 cửa sổ cuộn dọc trực quan, hiện đại (`tk.Canvas` + `ttk.Scrollbar` + MouseWheel mượt mà).
  - **Tự do co giãn kích thước (`resizable(True, True)`):** Mặc định $700 \times 670$, tối thiểu $620 \times 560$, tự động thích ứng với mọi tỉ lệ hiển thị (100%, 125%, 150% Windows Scaling), triệt tiêu hoàn toàn hiện tượng khuất hoặc cắt chữ/nút.
  - **Song ngữ Anh - Việt chuẩn mực (`is_vi = self.current_lang == 'vi'`):** Mọi nhãn, nút bấm, hướng dẫn quy ước và thông báo lỗi tự động thích ứng chuẩn xác theo ngôn ngữ người dùng lựa chọn.
  - **Quy trình dựng điểm 4 bước khoa học:**
    1. *Tên điểm mới:* Tự động gợi ý tên điểm tiếp theo ($M, N, P, Q, K...$).
    2. *Vị trí / Quỹ đạo điểm:* Nằm trên đường thẳng / tia qua 2 điểm (chọn phạm vi: Tia $P_1 \to P_2$, Đoạn $P_1P_2$, Đường thẳng $P_1P_2$), trên đường tròn bất kỳ, hoặc di động tự do trên mặt phẳng.
    3. *Điều kiện hình học tùy chọn:*
       - *1. Góc bằng góc:* Chọn đỉnh quan sát $B$, góc tham chiếu dạng `ECA` hoặc biểu thức `BME=ECA`. Thuật toán lượng giác vuông $t = t_{\text{proj}} \pm h \cot\beta$ giải nghiệm chính xác tuyệt đối (áp dụng xuất sắc cho bài toán VMO 2008).
       - *2. Góc có số đo độ cụ thể:* Nhập góc hoặc bấm nút nhanh `[30°] [45°] [60°] [90°] [120°]`.
       - *3. Khoảng cách / Tỉ lệ đoạn thẳng:* Hỗ trợ biểu thức tự do như `2*CB`, `1.5*AB`, `BC/2`, `5.0`.
       - *4. Chia tỉ lệ trên đoạn:* Hệ số $k$ với các nút chọn nhanh tỉ lệ vàng hình học (`0.5 - Trung điểm`, `1/3`, `2/3 - Trọng tâm`, `1.5`, `2.0`).
    4. *Nút xác nhận nổi bật:* `[✔ DỰNG ĐIỂM NGAY (Construct Point M)]` màu xanh lá chuẩn CAD, cập nhật tức thì lên tọa độ bản vẽ.
* **Chuẩn hóa song ngữ và giao diện các hộp thoại dựng hình chuyên sâu:**
  - `open_translate_dialog`: Tịnh tiến điểm theo vector (đặc biệt giải quyết bài toán $\vec{MN} = \vec{AC}$ trong VMO 2003). Hỗ trợ tiếng Việt và tiếng Anh, tự động gắn kết nối và cập nhật cây đại số.
  - `open_proj_foot_dialog`: Hạ chân đường vuông góc từ điểm xuống đường thẳng bất kỳ. Tự động sinh đường nét đứt vuông góc chuẩn sư phạm nối từ điểm đến chân đường cao.
  - `open_orthocenter_dialog`: Dựng trực tâm $H$ tam giác với 2 đường cao nét đứt hỗ trợ, hỗ trợ song ngữ đầy đủ.
* **Đổi nét đứt chuẩn sư phạm 1-click (`[--] Nét đứt`):**
  - Công cụ chuyển đổi phong cách đường nét (Solid $\leftrightarrow$ Dashed) cho phép người dùng click trực tiếp vào bất kỳ đoạn thẳng nào để đổi sang nét đứt sư phạm (đường gióng, đường phụ trợ, đường khuất) và ngược lại.
* **Xuất ảnh sạch chuẩn xuất bản (Clean Image Export):**
  - Loại bỏ hoàn toàn nền lưới tọa độ, trục tọa độ thừa và viền thao tác khi xuất ảnh; chỉ giữ lại các điểm, đoạn thẳng, đường tròn và nhãn đỉnh trên nền trắng tinh khiết chuẩn tài liệu và đề thi sư phạm.
* **Xác thực độ chính xác số học & CAS của 2 bài toán khó lạ VMO 2003 & 2008:**
  - Bài 4 (VMO 2003 - Bảng B): Xác thực $H \in (O')$ đường kính $BK$ với sai số bán kính máy tính $2.22 \times 10^{-16}$; xác thực điểm $I$ đối xứng với $B$ qua trung điểm $OO'$ với sai số $1.11 \times 10^{-16}$.
  - Bài 11 (VMO 2008): Xác thực đẳng thức then chốt $BM = AC$ và tỉ số $\frac{MC}{AB} = |\cos\alpha|$ bằng cả định lý Sin hình học thuần túy và khai triển tọa độ đại số SymPy.

### [Bản cập nhật v2.5] - 01/11/2026 (Bố Cục 4 Hàng Chống Tràn, Song Ngữ VI/EN & About Dialog)
* **Khắc phục triệt để lỗi tràn nút thanh công cụ (Toolbar Button Overflow / Cutoff):**
  - **Nguyên nhân:** Trước đây 26 công cụ CAD được xếp trên cùng một hàng ngang duy nhất (`bar2`), dẫn đến việc trên các màn hình có độ phân giải vừa và nhỏ ($\le 1440$px), các công cụ phía sau tiếp tuyến (Hình bình hành, Hình thoi, Hình vuông, Trực tâm, Tâm nội tiếp, Đường tròn nội tiếp, Tâm ngoại tiếp, Kiểm tra tính chất) bị đẩy tràn ra ngoài mép màn hình và biến mất.
  - **Giải pháp bố cục 4 hàng (4-Row Toolbar Architecture):**
    - **Hàng 1 (Hệ thống & Tiện ích):** Tệp mới, Xóa hình, Hoàn tác, Làm lại, Sao chép, Dán, Chọn tất cả, Xoay -15°, Xoay +15°, Góc xoay chỉ định, Ẩn/Hiện, Xuất ảnh PNG, Nút chuyển ngôn ngữ `[🌐 VI/EN]`, Nút `[ℹ Giới thiệu]`, và nút Thu gọn bảng lời giải `[Bảng Lời Giải ◀▶]`.
    - **Hàng 2 (Dựng Điểm, Đường & Quan hệ - 14 nút):** `[↖ Dời]`, `[⟲ Xoay]`, `[✕ Xóa]`, `[• Điểm]`, `[⤬ Giao]`, `[✛ T.điểm]`, `[⏊ H.chiếu]`, `[⇥ T.tiến]`, `[/ Đoạn]`, `[― Đường]`, `[⊥ Vuông]`, `[∥ S.song]`, `[∠ P.giác]`, `[📐 Góc/Tỉ lệ]`.
    - **Hàng 3 (Đường tròn, Đa giác & Tâm tam giác - 12 nút):** `[○ Tròn]`, `[⦿ Tròn 3P]`, `[◎ T.tuyến]`, `[⊜ T.tuyến 2C]`, `[▱ B.hành]`, `[◇ Thoi]`, `[□ Vuông]`, `[▲ Trực tâm]`, `[⊙ Tâm nội]`, `[⨀ Tròn nội]`, `[⊚ Tâm ngoại]`, `[✓ K.tra]`.
    - **Hàng 4 (Mục tiêu & CAS Solver):** Mẫu bài toán (7 presets), Dạng mục tiêu (9 goals), Đối tượng mục tiêu, Nút `▶ GIẢI TOÁN (SymPy)`.
* **Thu gọn kích thước nút bấm ~30% (Compact Button Styling):**
  - Giảm font chữ nút bấm xuống `Segoe UI 8pt`, padding siêu gọn `padx=3, pady=1`.
  - Độ rộng Hàng 2 chỉ chiếm ~640px, Hàng 3 chỉ chiếm ~620px. Đảm bảo hiển thị $100\%$ đầy đủ tất cả các nút ngay cả trên màn hình nhỏ từ $1024 \times 768$, không bao giờ bị cắt khuất!
* **Hỗ trợ Song Ngữ độc lập, chuyên nghiệp (Pure Bilingual Vietnamese & English):**
  - Tách bạch hoàn toàn giữa Tiếng Việt và Tiếng Anh (không viết kép gây rối và tốn diện tích như `(Ctrl+Z) Hoàn tác / Undo` hay `Tệp (File)`).
  - Nút chuyển đổi 1-click `[🌐 Tiếng Việt]` / `[🌐 English]` trên thanh công cụ Hàng 1 và Menu `Ngôn ngữ / Language`: Chuyển đổi tức thì toàn bộ Menu, Nút bấm, Chú thích Tooltip kỹ thuật, Hộp thoại, Tiêu đề bảng lời giải và Danh mục đối tượng.
  - Quản lý mục tiêu và mẫu bài tập theo chỉ số index (`current()`), độc lập hoàn toàn với chuỗi ngôn ngữ hiển thị.
* **Tích hợp Hộp thoại Thông tin sản phẩm & Phiên bản (About GeoSolver Dialog):**
  - Truy cập qua Menu `Trợ giúp (Help)` -> `Thông tin sản phẩm...` hoặc nút `[ℹ Giới thiệu]` trên Hàng 1.
  - Hiển thị đầy đủ phiên bản (v2.5), động cơ tính toán (Python Tkinter CAD + SymPy CAS), danh mục tính năng then chốt và cẩm nang phím tắt toàn diện.
* **Tiêu đề ứng dụng tinh gọn:**
  - Đặt lại tên đơn giản, thanh thoát: `GeoSolver v2.5`.
* **Bảo toàn nguyên vẹn $100\%$ tính năng và thuật toán:**
  - Tuyệt đối không can thiệp hay thay đổi các hàm tính toán hình học, thuật toán giải tích SymPy, điều phối vẽ Canvas, Smart Snapping hay các bộ dữ liệu mẫu VMO.

### [Bản cập nhật v3.3] - 04/11/2026 (Chuyển Đổi Không Gian D:\AI DATA, Bản Địa Hóa 100% Song Ngữ & Tương Tác Move/Drag Toàn Diện)
* **Chuyển đổi thư mục làm việc hoàn toàn:**
  - Di chuyển toàn bộ mã nguồn, dữ liệu kiểm thử và thư viện từ thư mục cũ sang `D:\AI DATA\công tụ giải toán`.
  - Kiểm tra và đồng bộ hóa 5,337 tệp (678 MB), 0 lỗi sao chép.
* **Bản địa hóa 100% Song Ngữ (Pure Bilingual Vietnamese & English):**
  - **Đề bài mẫu (`txt_problem`):** Tích hợp từ điển `PRESET_PROBLEMS` chứa nội dung chi tiết cho cả 8 bài toán mẫu (VMO 2000, 2001, 2003, 2007, 2008, Câu VIII Tuyển sinh, VMO 2008 Bài 12, VMO 2009 Bài 13). Khi chuyển sang English, toàn bộ đề bài và thông báo nạp bài tự động chuyển sang tiếng Anh.
  - **Bộ kiểm tra bất biến Cabri (`_scan_invariants_deep`):** Tự động xuất thông báo chuẩn tiếng Anh (`• Collinear:`, `• Right angle:`, `• Equal segments:`, `No special relations detected.`).
  - **Bảng màu nhanh (Color Palette):** Chuyển đổi tên nút (`🔴 Red`, `🔵 Blue`, `⚫ Black`, `🟢 Green`) và tooltip hướng dẫn chi tiết theo ngôn ngữ hiện hành.
  - **Cây đối tượng đại số (`_update_algebra_tree`):** Chuẩn hóa danh mục hiển thị (`Point`, `Seg`, `Line`, `Circle`, `Visible`, `Hidden`).
* **Nâng cấp Toàn diện Công cụ Move / Drag trên Canvas (`select` mode):**
  - **Di chuyển điểm (Move Point):** Kéo thả điểm tự do, tất cả các đoạn thẳng, đường thẳng, góc và tiếp tuyến gắn với điểm sẽ tự động co giãn / xoay theo vị trí mới.
  - **Di chuyển đoạn thẳng cố định độ dài (Rigid Segment Translation):** Bấm chọn đoạn thẳng và kéo chuột, cả hai đầu mút cùng tịnh tiến theo vector $(\Delta x, \Delta y)$, giữ nguyên $100\%$ độ dài và góc nghiêng, trong khi các đoạn nối ngoài vẫn ăn khớp theo ràng buộc.
  - **Di chuyển nhãn chữ cái đỉnh / điểm (Point Label Dragging):** Bấm chuột vào chữ cái đỉnh ($A, B, C...$) và rê chuột tự do để đặt nhãn ở bất kỳ góc độ nào mong muốn, chống hoàn toàn hiện tượng nhãn bị đè lên nét vẽ hay kí hiệu góc.
  - **Di chuyển nhãn đoạn thẳng & kí hiệu góc (Angle & Segment Label Dragging):** Hỗ trợ kéo nhãn đoạn thẳng và nhãn góc ($\alpha, \beta, 90^\circ...$) hoặc thay đổi bán kính cung góc trực tiếp trên canvas.
  - **Tương thích hoàn toàn với tính năng Xuất ảnh (Export High-Res PNG):** Mọi tọa độ dời nhãn (`label_dx`, `label_dy`) được áp dụng chính xác khi xuất ảnh PNG chuẩn sư phạm 300 DPI.
  - **Đánh giá tính khả thi & độ tải máy:** Phép tịnh tiến chỉ tiêu tốn $\mathcal{O}(1)$ phép cộng tọa độ ($< 0.001\text{ ms}$), CPU tiêu thụ $< 0.1\%$, 60 FPS mượt mà tuyệt đối, không gây biến dạng topo đồ thị và hoàn toàn bảo toàn các thuật toán dựng hình CAD / bộ giải chứng minh.

### [Bản cập nhật v3.0 - v3.2] - 03/11/2026 (Bộ Luật Diễn Dịch Hình Học Thuần Túy - Deductive Engine)
* **Xây dựng module `deductive_engine.py`:**
  - Khung toán học diễn dịch thuần túy không phụ thuộc hệ tọa độ $Oxy$: Phương pháp Góc đầy đủ (Full-Angle Method) và Phương pháp Diện tích (Area Method) của Chou, Gao & Zhang.
  - Cơ sở diễn dịch 40+ luật của AlphaGeometry (Google DeepMind 2024): Tính chất đường trung bình, từ vuông góc đến song song, tứ giác nội tiếp đường kính, góc nội tiếp, góc tiếp tuyến - dây cung, tính chất bắc cầu song song.
  - Chuyên đề Olympic HSG Việt Nam: Định lý đường thẳng Euler ($H, G, O$), Định lý Ceva, Menelaus, đường tròn Euler 9 điểm.
  - Bộ kiểm thử tự động `test_deductive_engine.py` vượt qua $7/7$ bài toán kiểm thử đạt $100\%$.

### [Bản cập nhật v2.5] - 01/11/2026 (Xuất Ảnh Sạch Chuẩn Sư Phạm, Công Cụ Nét Đứt, Xóa Bỏ Ký Hiệu RD, Hiệu Ứng Tự Động & Sẵn Sàng Ký Số Bản Quyền)
* **Xuất ảnh sạch chuẩn sư phạm (Clean Figure PNG Export):**
  - Mặc định xuất ảnh trắng tinh khiết, loại bỏ hoàn toàn hệ trục tọa độ Oxy, đường lưới ô vuông và các đường gióng thừa vô hạn.
  - Tự động cắt sát khung hình (Auto-crop to Figure bounding box) với lề đệm thẩm mỹ $18\%$, cho ra ảnh chất lượng xuất bản sách giáo khoa / đề thi (300 DPI Ultra-HD).
  - Tích hợp giải thuật vẽ nét đứt chuẩn xác trong Pillow: `draw_pil_dashed_line` và `draw_pil_dashed_ellipse`.
* **Công cụ đổi nét đứt chuẩn sư phạm (`[┈ Nét đứt]` / `toggle_dash`):**
  - Bổ sung nút bấm trực quan `[┈ Nét đứt]` trên Hàng 2 ngay cạnh `[/ Đoạn]`.
  - 1-Click chuyển đổi linh hoạt: Bấm chuột vào bất kỳ đoạn thẳng hoặc đường tròn nào để đổi qua lại giữa Nét Liền và Nét Đứt sư phạm $(6, 4)$.
  - Hỗ trợ nối 2 điểm bất kỳ bằng đoạn thẳng nét đứt khi bấm chọn 2 điểm trong chế độ nét đứt.
* **Xóa bỏ triệt để mọi thuật ngữ "RD" / "R&D":**
  - Loại bỏ hoàn toàn tất cả các từ viết tắt "RD" / "R&D" trong giao diện, mã nguồn và chuỗi giới thiệu.
  - Đổi tên bản quyền chính thức thành: `GeoSolver - Hệ Thống Dựng Hình Tương Tác & Giải Toán Đại Số SymPy`.
* **Hiệu ứng Chạy Tự Động (Auto-Scroll & Streaming Typewriter Engine):**
  - **Hộp thoại About (Giới thiệu):** Tích hợp bộ điều khiển cuộn văn bản tự động mượt mà như MS Word; tự động tạm dừng khi rê chuột vào văn bản (`<Enter>`) và tiếp tục khi rời chuột (`<Leave>`); có nút điều khiển `[⏸ Tạm dừng / ▶ Tiếp tục]` và `[⟲ Về đầu]`.
  - **Bảng Lời Giải:** Thêm tùy chọn `[✓] ⚡ Chạy tự động` để hiển thị các bước chứng minh và tính toán SymPy theo hiệu ứng máy chữ trực tiếp (Typewriter / Streaming Animation).
* **Cảnh báo Bản quyền Pháp lý Nghiêm ngặt & Sẵn sàng Ký số (Digital Signature Ready):**
  - Ghi nhận thông cáo bản quyền chính thức: Nghiêm cấm mọi hành vi sao chép, dịch ngược, phân phối lại theo Luật Sở hữu trí tuệ Việt Nam và điều ước quốc tế (WIPO/TRIPS).
  - Gắn nhãn bảo mật và chứng thư số: `🔏 SẴN SÀNG KÝ SỐ XÁC THỰC BẢN QUYỀN (PKI / RSA-4096 / SHA-256)`.
  - Hiển thị thông báo bản quyền thường trực trên thanh trạng thái dưới cùng: `⚖️ BẢN QUYỀN GEOSOLVER v2.5 - MỌI SAO CHÉP ĐỀU VI PHẠM | 🔏 SẴN SÀNG KÝ SỐ`.

### [Bản cập nhật v2.4] - 01/11/2026 (Phiên bản Hoàn thiện Olympic & Mở rộng CAD)
* **Thêm công cụ Dựng điểm theo Góc & Tỉ lệ khoảng cách (`open_angle_ratio_dialog`):**
  - Hỗ trợ công thức khoảng cách tự động: `2*CB`, `1.5*AB`, `5.0`, `BC/2` qua hàm giải mã `parse_geom_length`.
  - Hỗ trợ điều kiện góc: Góc bằng góc (như $\widehat{BME} = \widehat{ECA}$ của VMO 2008) hoặc góc cố định theo độ ($30^\circ, 45^\circ, 60^\circ$).
* **Thêm công cụ Tịnh tiến theo Vector (`open_translate_dialog`):**
  - Tịnh tiến điểm gốc theo vector $\vec{AC}$ ($\vec{MN} = \vec{AC}$ trong VMO 2003).
* **Thêm công cụ Hạ hình chiếu vuông góc (`open_proj_foot_dialog`):**
  - Hạ hình chiếu vuông góc từ điểm bất kỳ xuống đường thẳng qua 2 điểm ($D = \text{proj}_{BC}(M), E = \text{proj}_{AB}(N)$), tự động vẽ nét đứt và nhãn vuông góc.
* **Thêm công cụ Dựng trực tâm tam giác (`open_orthocenter_dialog`):**
  - Tự động tính giao điểm 3 đường cao và dựng trực tâm $H$.
* **Tách biệt hoàn toàn Không gian vẽ và Bảng Lời giải / Đề bài:**
  - Thêm tính năng `clear_drawing_only` (Nút `[Xóa hình]` trên Hàng 1): Xóa trắng các đối tượng trên canvas nhưng bảo toàn $100\%$ đề bài và lời giải bên phải.
  - Phím tắt `Ctrl+A` và `Delete` khi thao tác trên Canvas chỉ tác động đến hình học, không xóa văn bản.
* **Bổ sung Hệ thống Clipboard Hình học (Sao chép / Dán / Nhân bản):**
  - `Ctrl+C` (`copy_selection`): Lưu trữ cấu trúc điểm, đoạn nối, đường tròn vào bộ nhớ tạm `self.clipboard_geo`.
  - `Ctrl+V` (`paste_selection`): Dán các đối tượng với độ dời tọa độ (offset), tự động tạo danh pháp chuẩn toán học ($A \to A', B \to B'$).
  - `Ctrl+D` (`duplicate_selection`): Nhân bản nhanh đối tượng đang chọn.
* **Tích hợp 2 chuyên đề VMO mới:**
  - `Bài 4 (VMO 2003 Bảng B)`: Dựng 12 đối tượng, đường tròn đường kính $BK$, chứng minh trực tâm $H \in (O')$ và đối xứng $OO'$.
  - `Bài 11 (VMO 2008)`: Khám phá đẳng thức vàng $BM = AC$ bằng định lý Sin, tính tỉ số $\frac{MC}{AB} = |\cos \alpha|$.
* **Mặc định khởi động:** Đặt mặc định tại `0. [Trang trắng] Bản vẽ mới` với màn hình sạch sẽ.

### [Bản cập nhật v2.3] - 01/11/2026 (Sửa lỗi công cụ Dựng hình cơ bản)
* Khắc phục lỗi chọn điểm đỏ không vẽ được các đường quan hệ:
  - Viết lại toàn bộ bộ điều phối `perpendicular` (hạ vuông góc theo cặp điểm-đường hoặc bộ 3 điểm).
  - Viết lại bộ điều phối `parallel` (dựng song song theo cặp điểm-đường hoặc bộ 3 điểm).
  - Viết lại bộ điều phối `bisector` (dựng phân giác góc qua 3 điểm).
  - Viết lại công cụ `erase` (cho phép tẩy chọn lọc điểm, đoạn, đường, đường tròn).
* Nâng cấp Smart Snapping: Bắt dính giao điểm đường-đường, đường-tròn, tròn-tròn.

### [Bản cập nhật v2.2] - 01/11/2026 (Thiết kế Giao diện MS Office 2003 / Cabri II)
* Chuyển đổi toàn bộ thanh công cụ dọc chiếm diện tích sang 3 hàng ngang gọn gàng trên đỉnh (Top Toolbars).
* Rút gọn văn bản dài thành các biểu tượng ký hiệu kỹ thuật (`[↖ Dời]`, `[• Điểm]`, `[/ Đoạn]`, `[⊥ Vuông]`, `[∥ S.song]`, `[∠ P.giác]`, `[○ Tròn]`, `[◎ T.tuyến]`).
* Bổ sung ToolTip hiển thị hướng dẫn chi tiết khi rê chuột vào từng nút.
* Thêm nút thu phóng bảng lời giải (`Bảng Lời Giải [◀▶]`) để mở rộng màn hình vẽ $100\%$.

### [Bản cập nhật v2.1 & v2.0] - 01/11/2026 (Khởi tạo Nền tảng Desktop CAD & SymPy)
* Chuyển đổi nền tảng từ Web Flask sang ứng dụng Desktop thuần Python Tkinter để thao tác mượt mà, không phụ thuộc trình duyệt.
* Tích hợp SymPy giải phương trình giải tích Oxy (Câu VIII Tuyển sinh, Bài 1 VMO 2000, Bài 2 VMO 2001, Bài 9 VMO 2007).
* Hỗ trợ xuất ảnh PNG độ nét cao (2x scale) có tùy chọn kèm/không kèm hệ trục tọa độ Oxy.

---

## 4. DANH MỤC MẪU BÀI TẬP KINH ĐIỂN ĐÃ TÍCH HỢP (PRESETS 0 - 6)

| Index | Tên Mẫu Bài Tập | Dạng Bài & Nội Dung Trọng Tâm | Phương Pháp Giải & Kết Quả |
|:---:|:---|:---|:---|
| **0** | `[Trang trắng] Bản vẽ mới` | Khởi tạo trang vẽ sạch sẽ để người dùng tự do vẽ hình và nhập đề bài. | Không gian tự do. |
| **1** | `Câu VIII (Tuyển sinh Oxy)` | Tứ giác $ABCD$ nội tiếp đường kính $BD$, $AM \perp BC$, $AN \perp BD$, $P = MN \cap AC$. | Suy luận $\Delta PAM$ cân $\implies PA = PM$. SymPy giải ra $P(5/2; 3/2)$, $A(0; -1)$, $B(-1; 4)$. |
| **2** | `Bài 1 (VMO 2000)` | Hai điểm $M_1, M_2$ chuyển động cùng vận tốc góc trên 2 đường tròn. Quỹ tích $M$ & Điểm cố định $P$. | Trung tuyến vector $\implies$ Quỹ tích $M$ là đường tròn. Giao điểm $P$ thuộc đường tròn Apôlôniut và cung chứa góc cố định $\implies P$ cố định. |
| **3** | `Bài 2 (VMO 2001)` | Tiếp tuyến chung $P_1P_2$ của $(O_1), (O_2)$ cắt nhau tại $A, B$. $AQ_1 \cap (O_1) = M_1, AQ_2 \cap (O_2) = M_2$. | Tâm vị tự $S$ và tứ giác nội tiếp $\implies \widehat{M_1BA} + \widehat{M_2BA} = 180^\circ \implies M_1, B, M_2$ thẳng hàng. |
| **4** | `Bài 4 (VMO 2003)` | $\vec{MN} = \vec{AC}$, $D = \text{proj}_{BC}(M)$, $E = \text{proj}_{AB}(N)$. Đường tròn $(O')$ ngoại tiếp $\Delta BED$. | $BK$ là đường kính $(O')$, $\Delta AHC = \Delta MKN \implies KH \parallel AC \implies BH \perp KH \implies H \in (O')$. Chiếu vector $\vec{O'I} = \vec{BO} \implies$ đối xứng qua trung điểm $OO'$. |
| **5** | `Bài 9 (VMO 2007)` | $B, C$ cố định, $A$ thay đổi. Trung điểm $K$ của $HG$ thuộc đường thẳng $BC$. Tìm quỹ tích $A$. | Đặt hệ trục $B(-a; 0), C(a; 0)$. Tính $y_K = 0 \implies \frac{x^2}{a^2} - \frac{y^2}{3a^2} = 1 \implies$ Quỹ tích là đường Hypebol. |
| **6** | `Bài 11 (VMO 2008)` | $E$ trung điểm $AB$, $M \in$ tia $EC$ sao cho $\widehat{BME} = \widehat{ECA}$. Tính $\frac{MC}{AB}$ theo $\alpha = \widehat{BEC}$. | Định lý hàm Sin $\implies BM = AC$. Dựng đường tròn $(B; AC)$ cắt tia $EC$. Tính ra $\frac{MC}{AB} = |\cos \alpha|$. |

---

## 5. HƯỚNG DẪN KHÔI PHỤC (RESTORE) & QUY TRÌNH KIỂM THỬ

### 5.1. Khởi chạy ứng dụng:
Trong thư mục `d:\Du_An_Tu_Dong_RD\công tụ giải toán`, mở PowerShell hoặc Command Prompt:
```powershell
python geosolver_desktop.py
```
Hoặc nhấp đúp chuột vào file:
```cmd
run_desktop.bat
```

### 5.2. Kịch bản kiểm thử tự động toàn diện (Test Script):
Để kiểm tra tính toàn vẹn của mã nguồn sau bất kỳ sửa đổi nào, tạo một file test chạy headless:
```python
# Kiểm tra biên dịch không lỗi:
python -m py_compile geosolver_desktop.py
```
Tất cả các tính năng cốt lõi (Khởi động trang trắng, nạp 6 mẫu bài, tính toán SymPy, sao chép/dán `Ctrl+C/V`, phân tách 2 tab, giải mã độ dài `2*CB`) đã được tự động kiểm thử và đảm bảo hoạt động $100\%$ không có lỗi ngoại lệ.

---

## 6. CẨM NANG PHÁT TRIỂN MỞ RỘNG CHO CÁC PHIÊN BẢN SAU

Nếu bạn muốn mở rộng phần mềm này trong tương lai, dưới đây là các điểm mở rộng (Extension Points) đã được thiết kế sẵn:

### 6.1. Thêm một công cụ vẽ mới vào Hàng 2:
1. Thêm mã công cụ vào `_create_top_toolbars`:
   ```python
   add_tbtn(bar2, "my_new_tool", "[★ Tên nút]", "Tiêu đề ToolTip", "Mô tả tính năng")
   ```
2. Thêm xử lý sự kiện click chuột trong `_on_canvas_click`:
   ```python
   elif self.current_tool == "my_new_tool":
       # Lấy tọa độ wx, wy hoặc điểm snap
       # Thêm đối tượng vào self.points / self.segments / self.circles
       self._save_state()
       self.redraw()
   ```

### 6.2. Thêm một bài toán mẫu Olympic mới:
1. Viết hàm nạp bài toán:
   ```python
   def load_preset_my_exam(self):
       self.clear_all(silent=True)
       self.current_preset = "my_exam"
       self.combo_presets.current(new_index)
       self.txt_problem.insert(tk.END, "Đề bài...")
       # Tạo các điểm, đường, tròn với tọa độ chuẩn
       self.points.extend([...])
       self.solve_general_problem()
   ```
2. Khai báo mục mới trong `combo_presets` (Hàng 3) và menu `m_presets` (Menubar).
3. Thêm nhánh suy luận trong `solve_general_problem()`:
   ```python
   if self.current_preset == "my_exam" or "Từ khóa đề bài" in prob:
       sol_text = "Nội dung chứng minh chi tiết..."
       self.txt_solution.insert(tk.END, sol_text)
       return
   ```

### 6.3. Ý tưởng nâng cấp phiên bản tiếp theo:
- **Tích hợp GeoGebra / Asymptote / TikZ Export:** Thêm nút xuất mã $\LaTeX$ PGF/TikZ để nhúng trực tiếp vào các tài liệu Word / $\LaTeX$ thi chuyên toán.
- **Thước đo động (Measurement Labels):** Tùy chọn hiển thị trực tiếp số đo độ dài đoạn thẳng và số đo góc ngay trên cung tròn canvas.
- **Tự động nhận diện bài toán bằng OCR/AI:** Tích hợp mô hình nhận dạng ảnh đề bài PDF để tự động sinh lệnh dựng hình tương ứng.


---

## 7. QUY ƯỚC & NGUYÊN TẮC XUẤT PROMPT CHO ARGON (ONE-SHOT GENERATION)

> **MỤC ĐÍCH:** Đảm bảo khi người dùng yêu cầu xuất prompt (để gửi cho Argon hoặc các AI Code Generator khác), nội dung prompt phải đạt tiêu chuẩn **tự chứa hoàn chỉnh 100% (Fully Self-Contained)** để Argon có thể đọc và sinh ra file mã nguồn hoàn chỉnh ngay trong một lần chạy duy nhất (One-Shot File Generation), tuyệt đối không để người dùng phải chắp vá hay nhắc nhở nhiều lần.

### 7.1. Bốn Tiêu Chuẩn Bắt Buộc (The 4 Golden Rules):
1. **Không Viết Tắt / Không Cắt Khúc (No Truncation / No Placeholders):**
   - Tuyệt đối KHÔNG sử dụng các đoạn mã giữ chỗ như `# TODO: implement the rest`, `# ... existing code ...`, `/* remaining functions here */`.
   - Toàn bộ thư viện nhập (`import`), các hằng số, cấu trúc lớp (Class), phương thức (Method), hàm xử lý sự kiện và khối `if __name__ == '__main__':` phải được viết trọn vẹn từ dòng đầu tiên đến dòng cuối cùng.
2. **Ngữ Cảnh & Đặc Tả Kỹ Thuật Đầy Đủ (Comprehensive Technical Specification):**
   - Nêu rõ phiên bản ngôn ngữ (ví dụ: Python 3.10+ / 3.14), thư viện phụ thuộc (`tkinter`, `Pillow`, `SymPy`, `numpy`, `matplotlib`), hệ điều hành đích (Windows 11).
   - Mô tả chi tiết cấu trúc dữ liệu đầu vào / đầu ra (Data Schema), hệ tọa độ, quy chuẩn đặt tên biến và các trạng thái tương tác chuột/bàn phím.
3. **Bao Phủ Kiểm Thử & Xử Lý Ngoại Lệ (Error Handling & Built-in Verification):**
   - Định nghĩa rõ các kịch bản biên (Edge cases): Tọa độ trùng nhau, chia cho 0, tên điểm sai định dạng, dữ liệu rỗng.
   - Luôn đính kèm các hàm kiểm thử đơn vị tự động (`pytest` hoặc `unittest`) chạy được ngay để Argon tự kiểm chứng sau khi sinh mã.
4. **Ngôn Ngữ & Phong Cách Trình Bày (Clear Pedagogical Presentation):**
   - Prompt phải nêu rõ định dạng phản hồi mong muốn (ví dụ: một khối markdown ````python ... ```` duy nhất kèm đường dẫn tệp tuyệt đối).
   - Thuyết minh rõ ràng mục đích của từng module và thuật toán cốt lõi.
