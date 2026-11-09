# Phản biện khoa học: Phần mềm hỗ trợ giải toán phổ thông

Nov 7, 2026 · @Trump

## 1. Có "đóng góp khoa học mới" không?

**Không theo nghĩa chặt, nhưng có giá trị kỹ thuật.** Bản chất dự án là Applied Software Engineering / Tool Paper. Mọi thành phần lõi đều có sẵn: SymPy giải, SciPy tối ưu, LLM viết lời giải. Việc chặn nghiệm ngoại lai bằng tập xác định là kiến thức giáo khoa, và SymPy cũng có cơ chế kiểm tra nghiệm.

Có hai điểm có thể gọi là đóng góp **ở mức thiết kế hệ thống**, chứ chưa phải đóng góp lý thuyết:

- **Kiểm tra đầu vào hình học trước khi vẽ** (thiếu đỉnh, tam giác suy biến, nhãn đè nhau) kèm phân loại lỗi rõ ràng. Đây là mẫu thiết kế "fail loudly" hợp lý cho phần mềm giáo dục.
- **Tách vai trò**: tính toán do engine tất định đảm nhiệm, LLM chỉ diễn đạt lại. Đây là hướng đúng, nhưng chỉ có giá trị khoa học nếu đo được nó giúp giảm lỗi bao nhiêu (xem mục 4).

## 2. Nộp vào đâu?

Hiện trạng phù hợp nhất với đồ án hoặc hội thảo trong nước; hội nghị quốc tế chỉ nên thử sau khi có user study. Xếp theo độ phù hợp:

1. **Đồ án tốt nghiệp / báo cáo NCKH sinh viên / cuộc thi KHKT hoặc Tin học trẻ**: phù hợp nhất ở hiện trạng.
2. **Hội thảo trong nước** (ví dụ FAIR, các hội thảo CNTT và giáo dục quốc gia) hoặc tạp chí chuyên ngành trong nước: khả thi nếu bổ sung đánh giá thực nghiệm.
3. **Workshop/hội nghị quốc tế về công nghệ giáo dục**: chỉ nên thử sau khi có user study. Đề xuất IEEE TALE; lưu ý ICCE do APSCE tổ chức chứ không thuộc IEEE, cần kiểm tra lại. Ngoài ra có các workshop nhỏ về phần mềm giáo dục toán và hình học tự động (như ThEdu hay ADG), nhưng cần tự xác nhận phạm vi và hạn nộp hiện tại.

Hiện tại **không khuyên** nhắm vào hội nghị AI/ML hoặc tạp chí hạng cao.

## 3. Điểm yếu cốt tử sẽ bị bắt bẻ ngay

Có hai nhóm: thuật ngữ quá lớn so với thực tế, và các điểm yếu còn lại ngay cả khi dùng từ khiêm tốn.

**Nếu dùng từ lớn:**

- **Neuro-Symbolic**: LLM chỉ viết lại văn bản, không tham gia suy luận và không có vòng phản hồi giữa hai phần. Đó là pipeline, không phải kiến trúc neuro-symbolic.
- **Formal Verification**: validator kiểm tra tính hợp lệ của đầu vào theo ngưỡng, không chứng minh tính đúng đắn của lời giải. Không dùng Lean/Coq thì không nên dùng thuật ngữ này.
- **Deep Learning**: không huấn luyện mô hình nào cả.

**Ngay cả khi dùng từ khiêm tốn:**

- **Dữ liệu kiểm định mang tính vòng tròn.** 1.000 bài sinh từ template do chính tác giả viết chỉ chứng minh code chạy đúng trên các dạng đã lường trước, không chứng minh khả năng tổng quát. 40 bài thật là quá ít, và tài liệu chưa nêu tỷ lệ đúng, tỷ lệ thất bại, phân tích lỗi.
- **Không có baseline.** Hệ thống hơn gì so với SymPy thuần, GeoGebra, Photomath, Symbolab, hay chỉ hỏi thẳng LLM? Thiếu so sánh thì không có luận điểm.
- **Không kiểm soát ảo giác của LLM.** Tài liệu không nói lời giải do LLM viết có được đối chiếu với kết quả SymPy hay không. Đây là lỗ hổng lớn nhất cho một sản phẩm giáo dục.
- **Nelder-Mead cho cực trị chỉ là xấp xỉ**, không đảm bảo tối ưu toàn cục, nhạy với điểm khởi đầu và với hàm không trơn. Đưa kết quả này vào lời giải "chuẩn" cho học sinh là rủi ro sư phạm.
- **Ngưỡng 15 px và 10⁻⁴ là heuristic phụ thuộc thang đo.** Diện tích 10⁻⁴ có thể quá lớn hoặc quá nhỏ tùy đơn vị toạ độ. Cần chuẩn hoá (ví dụ theo độ dài cạnh lớn nhất) hoặc giải thích rõ.
- **Chưa có đánh giá người dùng**: học sinh, giáo viên chưa dùng, nên "giá trị thực tiễn" chưa có bằng chứng.
- **Phạm vi hẹp và chưa mô tả đầy đủ**: chưa rõ hệ thống nhận đề dạng gì (văn bản tự do hay nhập cấu trúc), xử lý được bao nhiêu % dạng bài trong chương trình phổ thông.
