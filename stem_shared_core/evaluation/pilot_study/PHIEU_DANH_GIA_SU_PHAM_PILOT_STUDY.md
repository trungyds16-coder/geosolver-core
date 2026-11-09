# HỒ SƠ KHẢO SÁT THỰC NGHIỆM SƯ PHẠM (PILOT STUDY PROTOCOL)
## DỰ ÁN: CAD MATH STUDIO & GEOSOLVER 2D
### CÔNG CỤ ĐO LƯỜNG HIỆU QUẢ TRỢ GIẢNG & ĐỘ TIN CẬY LIÊN THẨM ĐỊNH VIÊN (INTER-RATER RELIABILITY)

**Ngày ban hành:** 08/11/2026  
**Nhóm tác giả:** Ban phát triển Hệ thống Trợ giảng Toán học CAD Math Studio & GeoSolver 2D  
**Mục tiêu nghiên cứu:** Đánh giá định lượng tính sư phạm, độ chuẩn mực toán học và khả năng hỗ trợ nhận thức của hệ thống CAD Math Studio trên đối tượng giáo viên và học sinh phổ thông theo Khung Rubric 5 tiêu chí (§7).

---

## 1. THIẾT KẾ MẪU KHẢO SÁT (SAMPLE DESIGN)

- **Nhóm Chuyên gia / Giáo viên (Raters):** 03 giáo viên Toán THPT độc lập (tối thiểu 5 năm kinh nghiệm giảng dạy chương trình Đại số 10 - 11 - 12).
- **Nhóm Người học (Students):** 20 học sinh THPT (chia thành 2 nhóm: 10 học sinh lực học Khá/Giỏi và 10 học sinh lực học Trung bình).
- **Hình thức thực nghiệm:**
  + Học sinh giải 5 bài toán thực nghiệm đối chứng trên giấy và sau đó tương tác với lời giải từng bước của CAD Math Studio.
  + Giáo viên quan sát, chấm điểm độc lập lời giải sư phạm của CAD Math Studio theo Rubric 5 tiêu chí.

---

## 2. BỘ ĐỀ THỰC NGHIỆM ĐỐI CHỨNG (5 BÀI TOÁN TIÊU BIỂU)

| Mã bài | Dạng bài toán | Phương trình / Hệ | Đặc trưng sư phạm kiểm chứng |
|---|---|---|---|
| **P_01** | Vô tỷ chính tắc | $\sqrt{2x-1} = x - 1$ | Bẫy nghiệm ngoại lai $x = 2 - \sqrt{2} \approx 0.5858$ do vi phạm vế phải $g(x) < 0$. |
| **P_02** | Vô tỷ bậc 3 Cardano | $\sqrt{x^3 - 3x + 1} = \frac{1}{2}$ | Nghiệm Cardano thực phức tạp; kiểm tra năng lực giải thích bước trung gian và biểu diễn vô tỷ. |
| **P_03** | Bẫy nghiệm phức | $\sqrt{x} = x^2 + 1$ | Khử căn sinh phương trình bậc 4 vô nghiệm thực; kiểm tra cách từ chối và cảnh báo người học. |
| **P_04** | Diophantine hữu hạn | $x + y + z = 100, \quad 5x + 3y + \frac{z}{3} = 100$ | Bài toán Trăm trâu cổ điển; phân tích đồng dư bước nhảy 4 và hiển thị 3 nghiệm nguyên dương. |
| **P_05** | Diophantine vô hạn | $251x - z + 5 = 0, \quad y = 2$ | Hệ vô hạn nghiệm; kiểm tra năng lực biểu diễn họ nghiệm tham số $k \ge 0$ và bước nhảy lớn 251. |

---

## 3. PHIẾU CHẤM ĐIỂM DÀNH CHO GIÁO VIÊN (THANG ĐIỂM 1 - 5)

Mỗi giáo viên đánh giá độc lập từng bài toán theo 5 tiêu chí:

### Tiêu chí 1: Tính chuẩn mực toán học (Mathematical Correctness)
- **1 điểm:** Có sai sót về mặt toán học hoặc biến đổi sai tương đương.
- **2 điểm:** Kết quả đúng nhưng thiếu điều kiện xác định (ĐKXD).
- **3 điểm:** Đủ ĐKXD, biến đổi đúng nhưng còn bước giải thích tắt gây khó hiểu.
- **4 điểm:** Lập luận toán học chính xác, đầy đủ các bước đại số cần thiết.
- **5 điểm:** Chuẩn mực tuyệt đối, chặt chẽ từ điều kiện, biến đổi hệ quả đến thẩm định nghiệm.

### Tiêu chí 2: Tính minh bạch của tiến trình lập luận (Reasoning Transparency)
- **1 điểm:** Chỉ hiện kết quả dạng "hộp đen", không có lời giải chi tiết.
- **2 điểm:** Lời giải sơ sài, người học không theo dõi được mối liên hệ giữa các bước.
- **3 điểm:** Có tiến trình 4 bước nhưng chưa nhấn mạnh bản chất phép bình phương hệ quả.
- **4 điểm:** Tiến trình rõ ràng, giải thích tốt lý do chuyển đổi giữa các bước.
- **5 điểm:** Tiến trình mạch lạc, làm nổi bật phương pháp tư duy toán học cho học sinh.

### Tiêu chí 3: Giá trị sư phạm của giải thích nghiệm ngoại lai (Pedagogical Extraneous Roots)
- **1 điểm:** Bỏ qua nghiệm ngoại lai mà không có bất kỳ lời giải thích nào.
- **2 điểm:** Chỉ thông báo "loại nghiệm" mà không chỉ rõ điều kiện vi phạm.
- **3 điểm:** Nêu lý do loại nhưng còn mang tính hình thức (ví dụ: "thử lại thấy sai").
- **4 điểm:** Chỉ rõ nghiệm vi phạm vế phải $g(x) < 0$ hoặc điều kiện dưới căn $f(x) < 0$.
- **5 điểm:** Minh chứng sâu sắc bản chất phép bình phương làm nới rộng tập nghiệm, giúp người học tránh bẫy tư duy.

### Tiêu chí 4: Tính trực quan và cấu trúc hóa của kết quả (Visual & Structural Presentation)
- **1 điểm:** Định dạng lộn xộn, khó nhìn, khó phân biệt giữa các bước.
- **2 điểm:** Trình bày dạng văn bản thuần túy, thiếu công thức toán học chuyên dụng.
- **3 điểm:** Có công thức LaTeX nhưng bố cục chưa thật sự khoa học.
- **4 điểm:** Công thức LaTeX trực quan, có đồ thị Oxy minh họa phân bố nghiệm.
- **5 điểm:** Trình bày chuyên nghiệp chuẩn ấn phẩm sư phạm, đồ thị minh họa sắc nét.

### Tiêu chí 5: Tính trung thực khoa học và an toàn nhận thức (Epistemic Honesty)
- **1 điểm:** Đưa ra kết luận sai hoặc khẳng định kết quả khi chưa đủ căn cứ toán học.
- **2 điểm:** Bỏ qua các trường hợp biên nhạy cảm.
- **3 điểm:** Xử lý tốt các ca chuẩn nhưng lúng túng khi gặp bài toán ngoài phạm vi.
- **4 điểm:** Từ chối an toàn dạng bài ngoài phạm vi chuyên biệt.
- **5 điểm:** Chủ động cảnh báo bất định (`indeterminate`) khi biểu thức vượt ngưỡng phân giải đại số, bảo đảm an toàn nhận thức cho học sinh.

---

## 4. BIỂU MẪU GHI NHẬN ĐIỂM SỐ LIÊN THẨM ĐỊNH VIÊN (INTER-RATER DATA TABLE)

Bảng tổng hợp điểm số chấm độc lập từ 3 giáo viên (GV 1, GV 2, GV 3) trên 5 bài thực nghiệm:

| Bài | Tiêu chí đánh giá | Điểm GV 1 | Điểm GV 2 | Điểm GV 3 | Điểm Trung bình | Mức độ đồng thuận |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **P_01** | TC1: Chuẩn mực toán học | | | | | |
| | TC2: Minh bạch tiến trình | | | | | |
| | TC3: Giải thích ngoại lai | | | | | |
| | TC4: Trực quan kết quả | | | | | |
| | TC5: An toàn nhận thức | | | | | |
| **P_02** | TC1 - TC5 (Trung bình) | | | | | |
| **P_03** | TC1 - TC5 (Trung bình) | | | | | |
| **P_04** | TC1 - TC5 (Trung bình) | | | | | |
| **P_05** | TC1 - TC5 (Trung bình) | | | | | |

---

## 5. CÔNG THỨC & TIÊU CHUẨN XÁC NHẬN ĐỘ TIN CẬY (FLEISS' KAPPA & COHEN'S KAPPA)

- **Hệ số Fleiss' Kappa ($\kappa$):** Đánh giá mức độ đồng thuận thực chất giữa 3 giáo viên trên thang điểm phân loại.
  $$\kappa = \frac{\bar{P} - \bar{P}_e}{1 - \bar{P}_e}$$
- **Thang phân loại Landis & Koch:**
  + $\kappa < 0.20$: Đồng thuận rất thấp (Slight agreement)
  + $0.21 \le \kappa \le 0.40$: Đồng thuận trung bình thấp (Fair agreement)
  + $0.41 \le \kappa \le 0.60$: Đồng thuận vừa phải (Moderate agreement)
  + $0.61 \le \kappa \le 0.80$: **Đồng thuận đáng kể (Substantial agreement - MỤC TIÊU ĐẠT)**
  + $0.81 \le \kappa \le 1.00$: **Đồng thuận gần như tuyệt đối (Almost perfect agreement)**
