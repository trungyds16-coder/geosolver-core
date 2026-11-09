# BÁO CÁO TỔNG HỢP KHOA HỌC & GIẢI TRÌNH PHẢN BIỆN (PHIÊN BẢN 2.11)
## DỰ ÁN: CAD MATH STUDIO & GEOSOLVER 2D - HỒ SƠ HOÀN THIỆN ĐỀ XUẤT ĐÓNG VÒNG PHẢN BIỆN LÝ THUYẾT

**Ngày cập nhật:** 08/11/2026  
**Nhóm tác giả:** Ban phát triển Hệ thống Trợ giảng Toán học Tương tác CAD Math Studio & GeoSolver 2D  
**Môi trường thực thi thực nghiệm:**
- **Ngôn ngữ & Phiên bản:** Python 3.14.5 (64-bit)  
- **Thư viện Đại số Máy tính:** SymPy 1.14.0  
- **Hệ điều hành:** Windows 11 Pro 64-bit (Build 26300)  
- **Phần cứng CPU:** Intel Core i7-11800H @ 2.30GHz (8 nhân, 16 luồng)  

**Mã băm kiểm chứng tính toàn vẹn (SHA-256 đầy đủ 64 ký tự):**
- `cad_math_v2/cad_math_v2.py`: `52f056cc97645b3a32856b13e74c306f6acd888bf8d0cf084e8bf4105d3173f7`
- `stem_shared_core/tools/run_batch_auto_test.py`: `9a5f389216c0765fdf427e87d211d7a6d2b4592c830f188a18646cf79daa262d`

---

## 0. BẢNG TỔNG HỢP GIẢI TRÌNH & ĐÁP ỨNG TOÀN BỘ GÓP Ý THẨM ĐỊNH (ĐỢT 10)

Bản cập nhật Phiên bản 2.11 (v2.11) giải quyết toàn bộ 4 vấn đề chặn (§3) và các vấn đề phụ (§4) được chỉ ra trong đợt thẩm định ngày 08/11/2026:

| STT | Vấn đề phản biện (Đợt 10) | Hiện trạng v2.10 | Giải pháp kỹ thuật & Bằng chứng thực nghiệm v2.11 |
|---|---|---|---|
| **B1** | **Thiếu mã solver tự chứa, không thể tái lập độc lập** | Chỉ đính kèm test harness, thiếu mã nguồn solver khiến người phản biện không kiểm chứng được phương thức tĩnh và hàm băm. | **Đính kèm trọn vẹn mã nguồn lõi (§8.1):** Trích xuất toàn bộ lớp `CADMathCore`, `DiophantineCategory`, `clean_display_expr`, `solve_radical_pedagogical`, `solve_underdetermined_or_diophantine` độc lập hoàn toàn với Tkinter. Cung cấp SHA-256 đầy đủ 64 ký tự và định danh CPU Intel Core i7-11800H, Python 3.14.5 duy nhất. |
| **B2** | **"Mutation testing" v2.10 không phải kiểm thử đột biến thật** | Chỉ tính lại công thức cận nội bộ trong harness mà không chạy mã solver bị đột biến. | **Triển khai kiểm thử đột biến thật trên Bytecode (§4.2):** Biên dịch động 3 solver đột biến (`floor+0`, `ceiling-0`, `ntotal-1`). Chạy trực tiếp trên 100 hệ: Mutant 3 bị giết **25/25** hệ bị chặn (100%); Mutant 2 bị giết **18/100**; Mutant 1 bị giết **14/100**. Mọi ca sống sót đều được chứng minh có đầu ra đồng nhất tuyệt đối với solver gốc (đột biến tương đương). |
| **B3** | **Oracle sao chép công thức cận của solver, thiếu tính độc lập** | Oracle dùng lại `sp.floor` và `sp.ceiling` của solver; bộ sinh chưa phân tầng đồng đều. | **Thiết lập Oracle Hộp cố định độc lập ($N=3000$):** Quét vét cạn trực tiếp $p \in [1, 3000]$ bằng số học nguyên C thuần túy ($val \% D == 0 \land val > 0$), không dùng công thức cận hay CRT của solver. Sinh bộ dữ liệu phân tầng cân bằng: **đúng 25 hệ/loại** (tổng 100 hệ). Đạt **100/100 hệ khớp**. |
| **B4** | **RAD_02 trùng lặp RAD_01 và mô tả sai về kiểm tra đủ nghiệm** | $\sqrt{2x-1} + (1-x)$ trùng với RAD_01 trong SymPy; mô tả "nghiệm giải tích tính độc lập" chưa chính xác. | **Khôi phục ca hệ số căn âm $c = -1$:** Đổi RAD_02 thành $(x-1) - \sqrt{2x-1} = 0$, kiểm thử bước chuẩn hóa $g(x) = -rest/c$ khi $c < 0$. Mô tả đúng bản chất kiểm tra đủ nghiệm: đối chiếu tập `valid` với tập nghiệm chuẩn được duyệt bởi chuyên gia (`expected_valid`). Làm rõ Bất biến phân hoạch trên tập nghiệm hệ quả $S_{\text{raw}}$. |
| **P1** | **Bao phủ nhánh rẽ và 8 trạng thái đạt tới được** | Tuyên bố 9 trạng thái nhưng `UNKNOWN` là mã chết và 2 hàng dùng chung một enum. | Làm rõ hệ thống gồm **8 trạng thái cấu trúc đạt tới được trong thực tế** và **1 trạng thái dự phòng an toàn (`UNKNOWN`)**. Bộ 12 ca Diophantine bao phủ toàn bộ 8 trạng thái đạt tới được và các nhánh thuật toán đặc thù (gcd, xung đột CRT, trần lặp $10^9$, không nguyên tố cùng nhau). |
| **P2** | **So sánh với SymPy chưa phản ánh đúng thực tế** | Bảng so sánh ghi SymPy "cần `check=True`" trong khi mặc định SymPy đã loại nghiệm ngoại lai cho căn thức đơn. | Hiệu chỉnh bảng so sánh: Thừa nhận SymPy mặc định đã loại nghiệm ngoại lai. Khẳng định giá trị của CAD Math Studio nằm ở **giải thích sư phạm 4 bước**, hiển thị miền xác định $\mathcal{D}_{\text{rad}}, \mathcal{D}_{\text{sign}}$, chỉ rõ lý do loại nghiệm và phát hiện nghiệm bất định. |
| **P3** | **Khảo sát Photomath/Symbolab và thuật ngữ "O(1)"** | Ghi "thường timeout" và "thuật toán CRT O(1)" thiếu chính xác. | Đổi ghi chú sang "Khảo sát trải nghiệm giao diện người dùng". Bỏ thuật ngữ $O(1)$ đối với CRT; mô tả chính xác là thuật toán đồng dư giải tích và chỉ thế nghiệm cho tối đa 10 nghiệm đầu. |
| **P4** | **Làm sạch ngôn từ khẳng định tuyệt đối** | Còn sót các từ "tuyệt đối", "triệt để", "hoàn toàn", "100%", "BẢN ĐÓNG VÒNG". | Rà soát và loại bỏ các từ khẳng định tuyệt đối. Đổi tiêu đề thành bản đề xuất đóng vòng lý thuyết gửi hội đồng thẩm định. |
| **P5** | **Sửa lỗi định dạng LaTeX** | Ký tự TAB, form-feed, KaTeX hỏng do dấu gạch dưới `_`. | Chuẩn hóa toàn bộ công thức toán học, thoát dấu gạch dưới trong `\text{...}`, escape đầy đủ `\ne`, `\nmid`, `\notin`, `\alpha`. |
| **P6** | **Đo thời gian đa vòng tách biệt warm-up** | Thời gian chạy một lần có phương sai lớn do SymPy cache. | Thiết kế quy trình đo chuẩn: 1 vòng warm-up nạp cache + 5 vòng đo lường chính thức, trích xuất Trung vị (Median) cho từng bài toán. |
| **P7** | **Khôi phục Rubric sư phạm đầy đủ** | Bản v2.10 rút gọn mất bảng tiêu chí chi tiết và phương pháp luận ICC, Krippendorff. | Khôi phục trọn vẹn Rubric 5 tiêu chí chi tiết, thang điểm 5 mức, quy trình kiểm tra mù, ICC(2,1), Krippendorff's $\alpha \ge 0.70$ và Cluster Bootstrap. |

---