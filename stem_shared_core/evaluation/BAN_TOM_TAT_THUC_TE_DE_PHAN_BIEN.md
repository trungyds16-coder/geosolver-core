# TÓM TẮT THỰC TRẠNG DỰ ÁN ĐỂ PHẢN BIỆN KHOA HỌC (SYSTEM REALITY AUDIT)
Dành cho: Chuyên gia Phản biện / Reviewer AI (OpenAI o1, Claude 3.5 Sonnet, DeepSeek-R1)

---

## 1. THÔNG TIN BẢN CHẤT DỰ ÁN
- **Tác giả:** Người phát triển độc lập (không phải giáo sư chuyên ngành Toán lý thuyết hay AI Core).
- **Mục tiêu:** Xây dựng phần mềm hỗ trợ giải toán Đại số và Hình học phẳng 2D cho học sinh phổ thông trên nền tảng máy tính cá nhân (Windows Desktop).
- **Công nghệ thực tế sử dụng (Tech Stack):**
  - **Ngôn ngữ:** Python 3.14.
  - **Giao diện (UI):** Thư viện `Tkinter` thuần và Canvas 2D của Python (Matplotlib hỗ trợ biểu đồ).
  - **Lõi tính toán (Back-end Engine):** 
    + Sử dụng thư viện mã nguồn mở `SymPy` để giải phương trình và phân tích biểu thức tượng trưng.
    + Dùng `NumPy` và `SciPy (minimize Nelder-Mead)` để tính toán xấp xỉ cực trị đa biến.
  - **AI tích hợp:** Gọi API ngoài (Google Gemini / DeepSeek) để viết lại lời giải bằng văn phong tự nhiên.

---

## 2. NHỮNG GÌ HỆ THỐNG ĐÃ LÀM ĐƯỢC (TÍNH NĂNG THỰC TẾ)
1. **Phân hệ Đại số (CAD Math):**
   - Giải phương trình vô tỉ và hệ phương trình: Viết hàm tự động đặt tập xác định $\mathcal{D} = \{x \mid f(x) \ge 0\}$ trước khi bình phương, sau đó đối chiếu các nghiệm của SymPy với $\mathcal{D}$ để loại bỏ các nghiệm ngoại lai (ví dụ: loại nghiệm $x=5$ trong bài $\sqrt{x-1} = 3-x$).
   - Khảo sát hàm số bậc ba: Lập bảng biến thiên và vẽ đồ thị Oxy.
   - Sửa lỗi giới hạn mảng `index 1 is out of bounds for axis 0 with size 1` khi khảo sát hàm 1 biến bằng hàm `np.atleast_1d()`.

2. **Phân hệ Hình học phẳng (GeoSolver 2D):**
   - Viết module kiểm tra trước khi vẽ (`geometry_validator.py`):
     + Nếu thiếu toạ độ một đỉnh bất kỳ (ví dụ tam giác thiếu đỉnh C) -> quăng lỗi `MissingGeometricNodeError` dừng lại, không vẽ bậy.
     + Nếu diện tích tam giác $S < 10^{-4}$ (3 điểm thẳng hàng) -> báo lỗi hình suy biến.
     + Đo khoảng cách Euclidean giữa 2 đỉnh: Nếu khoảng cách $< 15\text{ px}$ -> cảnh báo có nguy cơ đè chữ nhãn điểm.

3. **Tập dữ liệu kiểm định:**
   - Dùng mã Python tự động sinh tham số (Procedural code) cho 1.000 bài toán (400 bài Conic, 300 bài hàm số, 300 bài phương trình căn).
   - Nạp thêm khoảng 40 bài toán đề thi thật từ sách PDF (VMO Việt Nam, Sharygin, Gaokao Trung Quốc).

---

## 3. NHỮNG GÌ HỆ THỐNG KHÔNG CÓ (GIỚI HẠN THỰC TẾ)
- **KHÔNG** phát minh ra thuật toán giải phương trình mới (hoàn toàn dựa vào thuật toán có sẵn của SymPy).
- **KHÔNG** tự huấn luyện (train) mô hình AI hay mạng nơ-ron nào (chỉ gọi API hoặc mô hình nạp sẵn).
- **KHÔNG** dùng ngôn ngữ toán học hình thức như Lean 4 hay Coq.
- Phần mềm chạy offline trên máy tính Windows cá nhân, chưa triển khai diện rộng trên môi trường Web hay trường học.

---

## 4. YÊU CẦU ĐỐI VỚI CHUYÊN GIA PHẢN BIỆN (REVIEWER INSTRUCTIONS)
Hãy đọc bản tóm tắt thực tế ở trên và trả lời thẳng thắn các câu hỏi sau:
1. Về mặt Khoa học Máy tính: Dự án này có yếu tố nào được coi là "đóng góp khoa học mới" (Novel Contribution) không, hay bản chất là một sản phẩm Kỹ thuật phần mềm ứng dụng (Applied Software Engineering / Tool Paper)?
2. Nếu muốn viết bài báo khoa học, đề tài này phù hợp nộp vào đâu? (Hội nghị Công nghệ Giáo dục IEEE TALE/ICCE, Kỷ yếu hội thảo trong nước, hay chỉ nên làm Đồ án tốt nghiệp / Báo cáo sáng tạo)?
3. Những điểm yếu cốt tử nào sẽ bị phản biện bắt bẻ ngay lập tức nếu tác giả cố tình dùng các từ đao to búa lớn (như Neuro-Symbolic, Formal Verification, Deep Learning)?
4. Tác giả nên viết bài báo theo hướng nào để trung thực, khiêm tốn nhưng vẫn được hội đồng đánh giá cao về giá trị thực tiễn?
