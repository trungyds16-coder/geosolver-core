# NHẬT KÝ PHÁT TRIỂN & QUY CHUẨN KHOA HỌC DỰ ÁN STEM APP
**Hệ sinh thái:** CAD Math Studio v2.1 & GeoSolver 2D  
**Trọng tâm:** Đại số, Giải tích phổ thông & Hình học phẳng 2D  
**Cập nhật lần cuối:** 07/11/2026

---

## I. QUY ƯỚC THỐNG NHẤT VỀ VĂN PHONG VÀ THUẬT NGỮ KHOA HỌC

Nhằm đảm bảo tính trung thực học thuật, khiêm tốn khoa học và tuân thủ các chuẩn mực bình duyệt quốc tế, toàn bộ tài liệu báo cáo, nhật ký nghiên cứu, giao diện người dùng và bài báo khoa học thống nhất áp dụng các nguyên tắc sau:

### 1. Danh mục thuật ngữ nghiêm cấm sử dụng (Prohibited Superlatives & Inflated Terms)
* **Tuyệt đối không dùng:**
  * `"chuẩn SGK"`, `"chuẩn 100%"`, `"chính xác tuyệt đối"`, `"hoàn hảo"`.
  * `"thuyết phục mọi chuyên gia"`, `"đáp ứng 85% chương trình"`, `"hệ thống thông minh toàn năng"`.
  * `"Neuro-Symbolic"`, `"Toán học hình thức (Formal Verification)"`, `"Theorem Prover"` khi thực tế chỉ sử dụng SymPy, thư viện đồ họa và mô hình ngôn ngữ hỗ trợ sư phạm.

### 2. Danh mục thuật ngữ chuẩn mực thay thế (Approved Scholarly Terminology)
| Cụm từ cần tránh | Cụm từ chuẩn mực thay thế | Ý nghĩa học thuật |
| :--- | :--- | :--- |
| *chuẩn SGK* | **theo nguyên lý sư phạm** / **phù hợp chương trình phổ thông** | Tránh lạm dụng danh xưng cơ quan nhà nước; nhấn mạnh tính sư phạm. |
| *chính xác tuyệt đối / chuẩn 100%* | **tính toán chính xác trên tập dữ liệu kiểm nghiệm** | Tôn trọng giới hạn của tập mẫu thực nghiệm (Ablation study). |
| *Neuro-Symbolic / Formal Verification* | **Hệ thống CAS kết hợp kiểm tra ràng buộc (Constraint-Checking CAS)** | Phản ánh đúng bản chất kỹ thuật: Python CAS + Ràng buộc toán học. |
| *Văn phong khoa trương, tự khen* | **Văn phong trang trọng, khách quan, trung thực, khiêm tốn khoa học** | Trình bày số liệu thực tế, nêu rõ ưu điểm và các hạn chế còn tồn đọng. |

---

## II. NHẬT KÝ THAY ĐỔI KỸ THUẬT GẦN NHẤT (CHANGELOG & AUDIT LOG)

### Giai đoạn 9: Nâng cấp trực tiếp Lõi giải toán GUI (`cad_math_v2.py`)
* **Thời gian ghi nhận:** 07/11/2026.
* **Tệp tác động:** [`cad_math_v2/cad_math_v2.py`](file:///d:/AI%20DATA/STEM_APP/cad_math_v2/cad_math_v2.py).
* **Nội dung thực hiện:**
  1. **Tích hợp bộ giải Hệ phương trình vô định & Diophantine tuyến tính:**
     * *Vấn đề phát hiện trước đó:* Khi nhập hệ 2 phương trình 3 ẩn (như bài toán cổ *"Trăm trâu trăm cỏ"*), hệ thống cũ chuyển sang thuật toán tối ưu số thực Nelder-Mead trên 2 biến và báo lỗi sai *"Vô nghiệm trên tập số thực $\mathbb{R}$"*.
     * *Giải pháp khắc phục:* Bổ sung hàm `solve_underdetermined_or_diophantine`. Nhận diện hệ có số ẩn nhiều hơn số phương trình ($N > M$), khử biến đại số biểu diễn nghiệm tổng quát theo tham số, biện luận tính chia hết và điều kiện nghiệm nguyên dương $x, y, z \in \mathbb{Z}^+$.
     * *Kết quả kiểm thử:* Tìm chính xác 3 bộ nghiệm nguyên dương: $(4, 18, 78)$, $(8, 11, 81)$, $(12, 4, 84)$ cho cả hai dạng đề bài ($15x + 9y + z = 300$ và $5x + 3y + z/3 = 100$).
  2. **Trực quan hóa ràng buộc và nghiệm rời rạc:**
     * Bổ sung hàm `plot_diophantine_system`.
     * Vẽ đường thẳng ràng buộc giữa hai biến đại diện trên mặt phẳng Oxy và hiển thị các điểm nghiệm nguyên bằng chấm đỏ kèm nhãn tọa độ chi tiết.
  3. **Khử nghiệm ngoại lai phương trình căn thức:**
     * Bổ sung hàm `solve_radical_pedagogical`.
     * Phân tách rõ ràng điều kiện trong căn $\mathcal{D}_{\text{rad}}: f(x) \ge 0$ và điều kiện vế phải $\mathcal{D}_{\text{sign}}: g(x) \ge 0$.
     * Đối chiếu nghiệm đại số sau khi bình phương, chỉ rõ lý do loại bỏ nghiệm ngoại lai (ví dụ phương trình $\sqrt{x-1} = x - 3$ loại bỏ $x = 2$ do vi phạm vế phải, chỉ nhận $x = 5$).

---

### Giai đoạn 10: Đồng bộ hóa quy chuẩn văn phong & Làm sạch mã nguồn
* **Thời gian ghi nhận:** 07/11/2026.
* **Nội dung thực hiện:**
  1. Quét toàn bộ mã nguồn `cad_math_v2.py` và các tệp báo cáo, loại bỏ triệt để các từ ngữ khoa trương ("chuẩn SGK", "chính xác tuyệt đối").
  2. Cập nhật nhãn thông báo hướng dẫn giải toán sang văn phong sư phạm chuẩn mực: *"Áp dụng phương pháp khử ẩn đại số và biện luận chia hết theo số học"*.
  3. Ghi nhận nhật ký kiểm nghiệm khoa học vào `EXPERIMENTAL_LOG.jsonl` (Phase 9 và Phase 10).

---

### Giai đoạn 11: Tổng quát hóa bộ giải Diophantine cho $N$ ẩn và $M$ phương trình ($M < N$)
* **Thời gian ghi nhận:** 07/11/2026.
* **Vấn đề được phản biện:** Trong phiên bản trước, bộ giải còn gắn nhãn ngữ cảnh bài toán cụ thể ("trâu đứng", "trâu nằm", "trâu già") và cố định khung giải theo 3 ẩn, không bao quát được các hệ phương trình đại số tổng quát có $N$ biến số và $M$ phương trình ($M < N$).
* **Giải pháp kỹ thuật tổng quát hóa:**
  1. **Tuyệt đối không gán nhãn đối tượng:** Biến số được giữ thuần túy dưới dạng toán học ($x, y, z$, $a, b, c, d\dots$).
  2. **Thuật toán tham số hóa tự động:** Sử dụng `sp.linsolve` để xác định không gian nghiệm affine $d = N - M$ chiều, tự động tách biến phụ thuộc và tham số tự do.
  3. **Biện luận chia hết động (Dynamic Modular Congruence):** Tự động tính bội chung nhỏ nhất (LCM) của các mẫu số biểu thức nghiệm để đưa ra điều kiện chia hết cho tham số.
  4. **Hệ bất phương trình chặn biên đa chiều:** Tự động sinh hệ điều kiện $v_i > 0$ cho toàn bộ $N$ biến số để chặn chính xác tập giá trị của tham số.
* **Kết quả nghiệm thu thực nghiệm:**
  * Hệ 3 ẩn 2 phương trình của người dùng: Trả về chính xác 2 bộ nghiệm $(6, 20, 74)$ và $(13, 10, 77)$.
  * Hệ 4 ẩn 3 phương trình $(a, b, c, d)$: Trả về chính xác 4 bộ nghiệm $(2, 8, 14, 6)$, $(4, 6, 13, 7)$, $(6, 4, 12, 8)$, $(8, 2, 11, 9)$.

---

### Giai đoạn 12: Hoàn thiện tính chặt chẽ giải tích và cấu trúc Diophantine theo phản biện đợt 2
* **Thời gian ghi nhận:** 07/11/2026.
* **Các điểm then chốt tiếp thu:**
  1. **Xác định dấu đại số chính xác:** Thay thế hoàn toàn phép kiểm tra phần dư số thực $10^{-7}$ bằng kiểm tra dấu đại số ký hiệu (`sp.sign()`, `sp.ask(sp.Q.nonnegative())`), triệt tiêu rủi ro sai số dấu với số vô tỷ.
  2. **Phân loại 3 trường hợp Diophantine:** Xóa bỏ khẳng định "luôn thu được khoảng chặn đóng". Thiết lập phân loại 3 nhánh rõ ràng: Rỗng (Infeasible), Hữu hạn bị chặn (Finite Bounded), và Vô hạn không bị chặn trên (Unbounded Infinite - xuất họ nghiệm nguyên tham số $k \ge k_{\min}$, không chạy vòng lặp vô nghĩa).
  3. **Tái định nghĩa ý nghĩa học thuật của Nhánh B:** Làm rõ Nhánh B (chỉ kiểm tra $f(x) \ge 0$) phản ánh mô hình sai lầm điển hình của học sinh phổ thông khi giải phương trình căn thức.
  4. **Công bố ma trận hệ số cụ thể:** Đưa toàn bộ ma trận $[A \mid \mathbf{b}]$ của các ca kiểm thử vào báo cáo phục vụ tái lập khoa học độc lập.
  5. **Chuẩn hóa thuật ngữ hình học:** Sử dụng thuật ngữ chuẩn "8 hướng la bàn".

---

### Giai đoạn 12: Chuẩn hóa nhận diện GeoSolver 3D, khắc phục hiển thị nét khuất và bổ sung công cụ gạch chéo diện tích
* **Thời gian ghi nhận:** 07/11/2026.
* **Tệp tác động:**
  - [`geosolver_3d/app.py`](file:///d:/AI%20DATA/STEM_APP/geosolver_3d/app.py)
  - [`run_geosolver_3d.bat`](file:///d:/AI%20DATA/STEM_APP/run_geosolver_3d.bat)
  - [`geosolver_3d/run_geosolver_3d.bat`](file:///d:/AI%20DATA/STEM_APP/geosolver_3d/run_geosolver_3d.bat)
* **Nội dung thực hiện chi tiết:**
  1. **Thống nhất tên gọi phần mềm:**
     - Chuẩn hóa tên định danh của phần mềm thành `GeoSolver 3D` trên tiêu đề cửa sổ chính, màn hình khởi động (Splash Screen) và các bảng điều khiển giao diện.
  2. **Khắc phục lỗi thứ tự hiển thị lớp (Z-Order Layering) trên Canvas và xuất ảnh:**
     - *Hiện tượng:* Khi người dùng tô màu hoặc kẻ gạch chéo diện tích mặt phẳng, mảng đa giác màu che lấp các đường nét đứt biểu diễn cạnh khuất bên dưới, dẫn đến việc chỉ nhìn thấy mảng màu mà mất đường nét đứt.
     - *Biện pháp kỹ thuật:* Sắp xếp lại thứ tự kết xuất đồ họa: Chuyển toàn bộ các mảng đa giác tô màu và các đường kẻ gạch chéo xuống lớp nền (vẽ trước), sau đó mới kết xuất các cạnh khuất nét đứt và cạnh thấy nét liền lên trên. Nhờ đó, đường nét đứt luôn hiển thị rõ ràng trên nền diện tích đã tô màu, không bị che khuất.
     - Đồng bộ quy trình kết xuất tương tự cho chức năng xuất ảnh tĩnh PNG độ phân giải 300 DPI.
  3. **Bổ sung và làm rõ công cụ kẻ gạch chéo / tô màu diện tích:**
     - Đổi nhãn nút công cụ trên thanh công cụ thành `[ ▨ Tô màu & Gạch chéo CAD ]` để người dùng dễ nhận diện.
     - Bổ sung nút truy cập nhanh `[ ▨ Tô màu / Gạch chéo diện tích... ]` trên thanh điều khiển bên trái.
     - Nâng cấp hộp thoại thiết lập diện tích: Bổ sung danh sách chọn nhanh các mặt của khối đa diện (mặt đáy, các mặt bên) và hỗ trợ linh hoạt cho cả tam giác (3 điểm) lẫn tứ giác (4 điểm).
  4. **Bảo vệ phím tắt và trực quan hóa trạng thái hiển thị nét khuất:**
     - Bổ sung điều kiện kiểm tra tiêu điểm cho phím tắt `H`, tránh việc người dùng vô tình làm thay đổi chế độ hiển thị nét khuất khi đang gõ văn bản hoặc đặt tên điểm.
     - Hiển thị trực quan trạng thái nút bấm nét khuất trên thanh công cụ để người dùng dễ theo dõi trạng thái hiện tại.
  5. **Tạo bộ khởi chạy thuận tiện:**
     - Tạo tệp kịch bản `run_geosolver_3d.bat` tại thư mục gốc dự án và thư mục `geosolver_3d`.
     - Tạo biểu tượng lối tắt (Shortcut) `GeoSolver 3D.lnk` trực tiếp trên màn hình Desktop của người dùng.
  6. **Đồng bộ nguyên tắc văn phong khoa học:**
     - Rà soát và loại bỏ các từ ngữ mang tính chủ quan, khẳng định quá mức; duy trì ngôn ngữ báo cáo trang trọng, khách quan, trung thực và khiêm tốn theo đúng quy chuẩn tại Mục I của nhật ký.

---

## III. NGUYÊN TẮC BẢO VỆ PHÁP LÝ & BẢN QUYỀN TÀI LIỆU
1. **Không định danh tài liệu bên ngoài:** Tuyệt đối không trích dẫn tên sách, tiêu đề tài liệu ôn tập, tác giả hoặc nhà xuất bản chưa được cấp phép trong các tệp mã nguồn và báo cáo khoa học.
2. **Ẩn danh tập dữ liệu kiểm thử (Anonymized Benchmarking):** Mọi bài toán trích xuất từ các tài liệu tham khảo được mã hóa dưới dạng ký hiệu trung tính (ví dụ: `BENCH_ALG_RAD_01`, `BENCH_GEO_2D_TRI_04`) và chỉ dùng cho mục đích đối sánh khoa học nội bộ.
3. **Độc lập và tự chủ công nghệ:** Toàn bộ thuật toán kiểm tra va chạm nhãn (AABB Collision Detector), thuật toán phân tích căn thức và bộ giải Diophantine đều chạy độc lập trên máy tính người dùng bằng Python và SymPy, không phụ thuộc vào dịch vụ AI đám mây đóng gói.
