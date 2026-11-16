# 🌟 BÁO CÁO KIỂM ĐỊNH TOÀN DIỆN & GÓI HỒ SƠ NỘP BÀI SOFTWAREX (ELSEVIER)
**Tác giả:** Bao-Trung Nguyen (Independent Researcher, Ho Chi Minh City, Vietnam)  
**Phần mềm:** GeoSolver 2D (v3.2.1)  
**Tạp chí mục tiêu:** *SoftwareX* (Elsevier, SCIE / Scopus Q2) — Chuyên mục: *Original Software Publication (OSP)*  
**Gói nộp hồ sơ chuẩn (Master Submission Bundle):** `D:\AI DATA\STEM_APP\docs\audit_reports\ELSEVIER_SUBMISSION_PACKAGE\antigravity_audit`  
**Cập nhật lần cuối:** 16/11/2026 (Đã tích hợp toàn bộ các điểm cải tiến từ Claude và Gemini)

---

## 1. TỔNG KẾT XỬ LÝ 4 ĐIỂM HOÀN THIỆN CUỐI CÙNG

### a) Phân tích Thông lượng (Throughput) & So sánh 4 Baseline (Mục 3a)
- Đã tách bạch và làm rõ 4 baseline so sánh trên 116 tam giác cận tam giác đều trên lưới $20 \times 20$:
  1. **Bare integer check** ($d_{12}^2 == d_{23}^2 == d_{31}^2$): $0.68\,\mu\text{s}$ (đoán nhận đẳng thức thô tối đa).
  2. **`fractions.Fraction`**: $8.62\,\mu\text{s}$ (chuẩn số học hữu tỉ chính xác trên $\mathbb{Q}^2$).
  3. **GeoSolver 2D headless** (`classify_triangle` trên tuple tọa độ thô): $7.13\,\mu\text{s}$ (nhanh hơn nhẹ so với `Fraction` do loại bỏ chi phí rút gọn $\gcd$).
  4. **GeoSolver 2D full pipeline** (đầy đủ DAG provenance, dynamic taint và từ điển metadata): $52.12\,\mu\text{s}$ (vẫn cực nhanh, chỉ tốn $0.3\%$ trong khung hình $16.7\,\text{ms}$ của chuẩn 60 FPS).
  5. **SymPy 1.14**: $1{,}738\,\mu\text{s}$ (minh họa chi phí CAS tổng quát, chậm hơn >30×).
- **Giải trình câu hỏi của Reviewer về Thang $10^k$ vs `Fraction`:**
  * `Fraction` là một thao tác số học chính xác trên $\mathbb{Q}^2$, nhưng GeoSolver 2D dùng thang thập phân $10^k$ để khớp trực tiếp với bộ số hóa giao diện người dùng (GUI digitizer, các mức làm tròn 0.1, 0.01) mà không tốn công tính ước số chung lớn nhất ($\gcd$) ở mỗi phép tính.
  * Đóng góp cốt lõi của GeoSolver 2D không chỉ là phép so sánh số học đơn lẻ, mà là toàn bộ kiến trúc phân loại: phân cấp đặc thù (specificity hierarchy), sắp xếp ứng viên bất biến hoán vị, xác định đỉnh cân/đỉnh vuông (apex equivariance), và lan truyền nguồn gốc (provenance invariant) theo thời gian thực.
- Đã loại bỏ hoàn toàn việc trộn lẫn "median" với $\sigma$, cũng như câu lặp "1,000 evaluations".

### b) Đồng bộ Hóa Cover Letter (`01_COVER_LETTER.docx`) (Mục 3b)
- **Mở đầu bằng ví dụ thực tế:** Nêu ngay ở phần đầu ví dụ tam giác $A(0,0), B(1000,0), C(500,866)$ (độ lệch $0.0022\%$) bị bộ phân loại dung sai dán nhãn tam giác đều sai toán học.
- **Đưa câu "drop-in component" lên ngay đoạn mở đầu:** Nhấn mạnh GeoSolver 2D là vi nhân Python độc lập, không phụ thuộc thư viện ngoài, tích hợp vào autograder hoặc DGS front-end chỉ bằng một lời gọi hàm.
- **Điều chỉnh văn phong phòng thủ:** Thay "Conventional systems evaluate..." bằng "tolerance-based classification, as commonly implemented, can...", loại bỏ các từ phóng đại (như "foundational in CAD").
- **Chuẩn hóa thuật ngữ:** Thay "provenance conservation law" thành "provenance invariant".
- Cập nhật số liệu kiểm thử chính xác: 62 test (100% PASS), 92% statement coverage trên `geosolver_core`.

### c) Văn phong và Thuật ngữ Học thuật (Mục 3c)
- Đổi cụm từ "balanced operational threshold" thành "conservative default".
- Giải thích rõ ràng tại sao cột "Near-Right FP" đạt $0/100$ trong Bảng 3: Do kiểm tra góc vuông dựa trên ngưỡng cosin độc lập ($|\cos \theta| \le 0.015$), được giữ cố định khi quét dung sai cạnh $\mathrm{tol_{rel}}$.
- **Đo lường bất biến đỉnh trên phân bố tự nhiên:**
  * Trên tập chuẩn 1,000 tam giác có nhiễu Gaussian (Bảng 2), bộ phân loại vị trí ngây thơ bị sai lệch đỉnh ở **$10.1\%$** số tam giác cân phát hiện được ($26 / 257$), trong khi GeoSolver 2D đạt **$0.0\%$** ($0 / 257$).
  * Trên 200 cấu hình cận hòa đối kháng, bộ ngây thơ sai **$100.0\%$** ($200 / 200$), trong khi GeoSolver 2D đạt **$0.0\%$** ($0 / 200$).
- **Hợp đồng ngữ nghĩa (Semantic Contract) trong Dual-Regime:**
  * Bổ sung câu giải thích: Tọa độ thập phân người dùng nhập vào được xem là giá trị chính xác, do đó "tính chính xác" trong chế độ rời rạc là chính xác sau lượng tử hóa trên lưới thập phân $\mathbb{Z}^2 / 10^k$, chứ không phải trên mặt phẳng thực $\mathbb{R}^2$.

### d) Triển khai Ví dụ 3 Autograder trong Repo (`examples/autograder.py`) (Mục 3d)
- Đã tạo [examples/autograder.py](file:///d:/AI%20DATA/STEM_APP/examples/autograder.py) hiện thực hóa hàm `grade(pA, pB, pC, expected="isosceles")` khớp 100% với Ví dụ 3 trong bản thảo.
- Đã kiểm tra khớp chính xác các khóa của API `geosolver_core`: `is_triangle`, `type`, `exact`, `vertex`.
- Đã tích hợp kiểm thử tự động vào CI workflow [ci.yml](file:///d:/AI%20DATA/STEM_APP/.github/workflows/ci.yml) trên GitHub Actions.

---

## 2. BỘ 4 FILE CHÍNH THỨC NỘP HỆ THỐNG ELSEVIER EDITORIAL MANAGER

Thư mục lưu trữ: `D:\AI DATA\STEM_APP\docs\audit_reports\ELSEVIER_SUBMISSION_PACKAGE\antigravity_audit`

1. **`01_COVER_LETTER.docx`**: Tải lên mục **Cover Letter**.
2. **`02_HIGHLIGHTS.docx`**: Tải lên mục **Highlights** (4 dòng, tất cả đều $\le 85$ ký tự).
3. **`03_declarationStatement_1.docx`**: Tải lên mục **Declaration of Competing Interests** (mẫu chính thức của Elsevier Declarations Tool).
4. **`GEOSOLVER_2D_LATEX_SOURCE.zip`**: Tải lên mục **Manuscript** (chứa `.tex`, `.bib`, `.cls`, `.bst`, `fig_example1.pdf`, `fig_sensitivity.pdf`).

*(File PDF tham chiếu hoàn chỉnh: `Geosolver_2d_Manuscript.pdf`)*

---

## 3. THÔNG SỐ CODE METADATA & REPO LIÊN KẾT
- **Current Code Version:** `v3.2.1`
- **GitHub Repository:** [https://github.com/trungyds16-coder/geosolver-core](https://github.com/trungyds16-coder/geosolver-core)
- **Zenodo DOI:** [10.5281/zenodo.24249595](https://doi.org/10.5281/zenodo.24249595)
- **Bản quyền:** GNU General Public License v3 (GPLv3)
- **Môi trường CI:** GitHub Actions ma trận 12 luồng (Ubuntu, Windows, macOS trên Python 3.10–3.13) đạt 100% PASS.
