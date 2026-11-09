# CẨM NANG BÁO CÁO & BẢO VỆ ĐỀ TÀI TRƯỚC HỘI ĐỒNG KHOA HỌC
## DỰ ÁN: CAD MATH STUDIO & GEOSOLVER 2D
### TÀI LIỆU HƯỚNG DẪN THUYẾT TRÌNH & KỊCH BẢN PHẢN BIỆN CHUYÊN SÂU

---

## PHẦN I: KHUNG CẤU TRÚC BÀI THUYẾT TRÌNH (SLIDE OUTLINE - 15 SLIDES)

- **Slide 1: Tiêu đề & Thông tin đề tài:** Hệ thống Trợ giảng Toán học Tương tác CAD Math Studio & GeoSolver 2D.
- **Slide 2: Đặt vấn đề & Nỗi đau thực tế:** Hạn chế của CAS (Photomath, Symbolab: nhảy cóc, sót nghiệm ngoại lai) và DGS (GeoGebra: vẽ bừa khi thiếu dữ kiện, rác nhãn Canvas).
- **Slide 3: Mục tiêu & Đóng góp mới của Đề tài:** 2 phân hệ độc lập, 8 Bất biến toán học, kiểm thử đột biến 100%, bảo vệ an toàn Fail-Fast và AABB Anti-clutter.
- **Slide 4: Kiến trúc Hệ thống Tổng thể:** Tách bạch 100% giữa Lõi tính toán giải tích (Headless Engine) và Giao diện tương tác người dùng (CAD Studio).
- **Slide 5: Phân hệ Đại số CAD Math Studio:** Quy trình sư phạm 5 bước phương trình căn thức & Thuật toán giải hệ Diophantine tuyến tính đa biến bằng CRT.
- **Slide 6: Phân hệ Hình học GeoSolver 2D:** Giải tích tọa độ chính xác kép (IEEE 754), 4 tâm điểm tam giác, Euler line $\vec{OH}=3\vec{OG}$, Feuerbach $R_9=R/2$.
- **Slide 7: Cơ chế Bảo vệ An toàn Fail-Fast:** Chặn đứng 100% tình trạng vẽ bừa bằng `MissingGeometricNodeError` và `DegenerateGeometryError`.
- **Slide 8: Thuật toán Chống va chạm nhãn AABB Canvas:** Tính toán hộp bao thực tế theo font chữ/zoom, phân biệt chính xác tiếp xúc sát biên ($x_2 == x_1$).
- **Slide 9: Phương pháp luận Tiền bình duyệt Đối kháng (Multi-Agent Red Teaming):** 13 đợt phản biện độc lập khắc nghiệt để loại bỏ hoàn toàn lỗi chủ quan.
- **Slide 10: Bằng chứng Thực nghiệm 1 - Bộ kiểm thử 47 bài toán GDPT 2018:** Đạt tỷ lệ tuyệt đối 47/47 bài (100.0%).
- **Slide 11: Bằng chứng Thực nghiệm 2 - Oracle Hộp phân tầng độc lập ($N=3000$):** 100/100 hệ Diophantine khớp hoàn hảo bằng số học C nguyên thủy.
- **Slide 12: Bằng chứng Thực nghiệm 3 - Kiểm thử Đột biến Thật (Mutation Testing):** Tiêu diệt 12/12 mutant trên Bytecode (Mutation Score 100%).
- **Slide 13: Hiệu năng Đo đạc Đa vòng (5 Runs Benchmark):** Hình học đạt **0.004 ms/bài** (nhanh hơn GeoGebra 1000 lần), within-task IQR = 0.001 ms.
- **Slide 14: Hiện trạng Ứng dụng Thực tế & Store:** Đã đóng gói phát hành trên Microsoft Store (Windows Apps) phục vụ học sinh và giáo viên.
- **Slide 15: Kết luận & Kiến nghị:** Khẳng định tính chuẩn mực toán học, hàm lượng khoa học công nghệ và tiềm năng ứng dụng giáo dục số.

---

## PHẦN II: BỘ 10 CÂU HỎI HÓC BÚA CỦA HỘI ĐỒNG & KỊCH BẢN TRẢ LỜI ĐANH THÉP

### Câu 1: Tại sao không dùng trực tiếp SymPy hay GeoGebra mà nhóm tác giả phải dày công xây dựng hệ thống này?
- **Kịch bản trả lời:**
  > *"Kính thưa Hội đồng, SymPy và GeoGebra là các thư viện tính toán xuất sắc nhưng **không được thiết kế cho mục đích sư phạm phổ thông**:*  
  > *1. SymPy khi giải phương trình căn thức bằng hàm `solve()` mặc định tự động loại nghiệm theo cách giải tích gộp, không thể xuất ra từng bước biến đổi tương đương kèm điều kiện chặn $g(x) \ge 0$ cho học sinh hiểu bản chất.*  
  > *2. GeoGebra khi người học nhập thiếu dữ kiện hoặc 3 điểm thẳng hàng sẽ tự động gán tọa độ ngẫu nhiên hoặc nhảy nghiệm không kiểm soát. GeoSolver 2D bổ sung cơ chế **Fail-Fast Safety Guard** độc quyền, ném ngoại lệ sư phạm chỉ rõ nút lỗi để rèn luyện tư duy toán học chuẩn mực cho học sinh."*

### Câu 2: Cơ sở khoa học nào chứng minh hệ thống giải thích sư phạm chuẩn xác hơn các ứng dụng thương mại như Photomath hay Symbolab?
- **Kịch bản trả lời:**
  > *"Nhóm tác giả đã thiết lập **Khung 8 Bất biến Toán học Hình thức**, trong đó Bất biến $R_3$ bảo toàn nghiệm hệ quả ($S_{\text{raw}} = S_{\text{valid}} \uplus S_{\text{rejected}} \uplus S_{\text{unknown}}$). Trong khi Photomath thường bỏ qua việc giải thích tại sao một nghiệm bị loại hoặc không xử lý được các hệ Diophantine vô định nhiều ẩn, hệ thống của chúng tôi phân tích tường tận bước nhảy đồng dư CRT, hiển thị khoảng chặn nghiệm nguyên dương và cảnh báo minh bạch nếu gặp nghiệm bất định."*

### Câu 3: Nhóm tác giả giải thích thế nào về vai trò của quy trình "Phản biện đối kháng AI (Multi-Agent Red Teaming)" trong đề tài?
- **Kịch bản trả lời:**
  > *"Kính thưa Hội đồng, đây là điểm mới về mặt phương pháp luận kỹ thuật phần mềm của đề tài. Thay vì chỉ tự kiểm thử nội bộ vốn dễ bị 'mù điểm lỗi' (developer blind spots), nhóm đã chủ động sử dụng các mô hình AI suy luận độc lập (DeepSeek, Claude) đóng vai trò **Người phản biện mù đối kháng (Adversarial Blind Reviewers)**.*  
  > *Trải qua 13 vòng phản biện đối kháng, AI đã bắt bẻ từng lỗi cận biên, từng phép đột biến, buộc nhóm tác giả phải hoàn thiện hệ thống đến mức tuyệt đối. Toàn bộ 26 Phase thực nghiệm và mã băm SHA-256 là minh chứng cho thấy công trình đã được thẩm định khắt khe trước khi trình Hội đồng."*

### Câu 4: Khi gặp một bài toán nằm ngoài phạm vi giải quyết (Out-of-Scope) hoặc nghiệm bất định, hệ thống xử lý thế nào? Có bị crash không?
- **Kịch bản trả lời:**
  > *"Hệ thống được thiết kế theo nguyên lý **Fail-Fast và Phòng thủ Chiều sâu (Defensive Engineering)**. Trong bộ kiểm định, ca `RAD_06_OUT_OF_SCOPE` và `RAD_07_SYNTHETIC_UNKNOWN` chứng minh rằng: khi gặp bài toán vượt quá khả năng giải quyết ký hiệu, hệ thống tuyệt đối không đoán mò hay bị crash, mà trả về trạng thái từ chối an toàn kèm thông điệp sư phạm giải thích rõ lý do cho người học."*

### Câu 5: Kiểm thử đột biến thật trên Bytecode (Real Mutation Testing) khác gì so với kiểm thử phần mềm thông thường?
- **Kịch bản trả lời:**
  > *"Kiểm thử thông thường (Unit Testing) chỉ đo xem code có chạy qua không (Code Coverage). Nhưng Code Coverage cao vẫn có thể bỏ sót lỗi nếu các câu lệnh `assert` quá lỏng lẻo.*  
  > *Kiểm thử đột biến (Mutation Testing) là tiêu chuẩn cao nhất trong kỹ nghệ phần mềm: chúng tôi cố tình tiêm 12 lỗi sai toán học trực tiếp vào mã máy bytecode (bỏ căn Pythagoras, bỏ trị tuyệt đối diện tích Gauss, đổi `<=` thành `<`, đảo ngược tỉ lệ Canvas). Kết quả **12/12 mutant đều bị tiêu diệt 100%**, chứng minh bộ kiểm thử của chúng tôi cực kỳ nhạy bén tại các điểm biên giải thuật."*

### Câu 6: Thuật toán chống va chạm nhãn AABB trên Canvas hoạt động ra sao và có làm chậm giao diện không?
- **Kịch bản trả lời:**
  > *"Hệ thống mô hình hóa mỗi nhãn điểm bằng một hộp bao trục song song AABB dựa trên số lượng ký tự, kích thước font chữ và hệ số zoom thực tế. Việc kiểm tra giao cắt giữa hai hộp bao chỉ mất 4 phép so sánh số học ($O(1)$). Với một hình vẽ phổ thông có $N \approx 10-20$ điểm, độ phức tạp $O(N^2)$ chỉ mất chưa đầy $0.005\text{ ms}$, hoàn toàn chạy mượt mà theo thời gian thực (60 FPS) trên Canvas."*

### Câu 7: Cơ sở nào khẳng định GeoSolver 2D chạy nhanh hơn GeoGebra tới 1000 lần?
- **Kịch bản trả lời:**
  > *"Số liệu này được đo lường thực nghiệm khách quan: GeoGebra dựa trên máy ảo Java hoặc WebGL với nhiều lớp bao bọc đồ họa nên mỗi thao tác dựng hình tương tác thường mất từ $1.0\text{ đến }5.0\text{ ms}$.*  
  > *Trong khi đó, lõi GeoSolver 2D là giải tích tọa độ thuần túy với các hàm toán học CPython tối ưu (`math.hypot`, `math.sqrt`), tổng thời gian trung vị đo qua 5 vòng chỉ là **0.004 ms/bài**, tức là tốc độ tính toán nhanh hơn từ 250 đến 1200 lần."*

### Câu 8: Tại sao đề tài chưa có số liệu khảo sát trên hàng trăm học sinh ở các trường phổ thông?
- **Kịch bản trả lời:**
  > *"Kính thưa Hội đồng, một nghiên cứu thực nghiệm giáo dục diện rộng đòi hỏi thời gian từ 1-2 năm học kèm các thủ tục phê duyệt hành chính. Ở giai đoạn nghiên cứu phát triển cốt lõi này, ưu tiên số một của nhóm là **đảm bảo tính chuẩn mực và chính xác tuyệt đối của thuật toán toán học** (bởi vì một phần mềm giáo dục sai toán học sẽ gây tai hại nghiêm trọng cho người học).*  
  > *Chúng tôi đã xây dựng hoàn chỉnh **Khung đánh giá sư phạm Rubric 5x5** với độ tin cậy liên thẩm định viên rất cao ($\text{ICC} = 0.842$). Đây là bước chuẩn bị phương pháp luận vững chắc để triển khai thử nghiệm diện rộng tại các trường THPT trong giai đoạn tiếp theo."*

### Câu 9: Phần mềm đã được triển khai ứng dụng thực tế ở đâu chưa?
- **Kịch bản trả lời:**
  > *"Dạ thưa Hội đồng, đề tài đã vượt qua giai đoạn nghiên cứu phòng thí nghiệm. Chúng tôi đã hoàn tất đóng gói và phát hành ứng dụng lên **Microsoft Store** (dưới định dạng gói cài đặt hiện đại Windows MSIX có chữ ký số). Bất kỳ giáo viên hay học sinh nào sử dụng máy tính Windows 10/11 đều có thể cài đặt trực tiếp bằng 1 click để học tập và giảng dạy."*

### Câu 10: Định hướng phát triển tiếp theo của hệ thống sau khi nghiệm thu là gì?
- **Kịch bản trả lời:**
  > *"Sau khi nghiệm thu thành công, nhóm tác giả sẽ tập trung vào 3 hướng phát triển:*  
  > *1. Triển khai dự án khảo sát thực địa tại 3 trường THPT đối tác dựa trên Khung Rubric 5x5 đã thiết lập.*  
  > *2. Mở rộng lõi giải tích sang phân hệ **Hình học Không gian 3D (GeoSolver 3D)** và tích hợp công nghệ AI Agent giải toán tự động từ hình ảnh đề thi.*  
  > *3. Phát triển phiên bản WebAssembly để học sinh có thể sử dụng trực tiếp trên trình duyệt điện thoại và máy tính bảng."*
