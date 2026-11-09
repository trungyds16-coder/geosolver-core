# MA TRẬN ĐỐI CHIẾU SO SÁNH TRƯỚC VÀ SAU THẨM ĐỊNH
## [PRE- & POST-AUDIT COMPARATIVE MATRIX]
*Bảng tổng hợp đối chiếu trực quan tiến trình hoàn thiện kỹ thuật từ v3.0 lên v3.1 qua 2 đợt phản biện chuyên sâu của Claude.*  
**Mã hồ sơ:** AUDIT-2026-COMPARISON-MATRIX  
**Ngày lập:** 08/11/2026  

---

### BẢNG ĐỐI CHIẾU SO SÁNH CHI TIẾT TỪNG HẠNG MỤC

| Hạng mục đối chiếu | Bản Ban đầu (v3.0) | Nhận xét Phản biện của Claude (Đợt 1 & 2) | Bản Hoàn thiện & Giải trình (v3.1) | Vị trí mã nguồn / Minh chứng |
| :--- | :--- | :--- | :--- | :--- |
| **1. Bản chất văn bản & Chữ ký** | Tự phong "Xác thực độc lập", đưa chữ ký danh nghĩa "Claude Validator Review". | AI lập trình tự viết báo cáo thì không thể là "độc lập". Claude chưa chạy code nên không thể ký duyệt. | Đổi thành "Báo cáo Tự kiểm định Kỹ thuật Nội bộ (Internal Technical Self-Verification)"; gỡ bỏ toàn bộ chữ ký danh nghĩa. | `docs/audit_reports/03_BAO_CAO_GIAI_TRINH_VA_KIEM_DINH_THUC_NGHIEM_V3.1.md` |
| **2. Thuật ngữ & Lỗi gõ công thức** | Dùng từ "ảo giác AI", "khử triệt để 100%". Lỗi gõ $AB = \sqrt{0^2 + 5^2 - (-3)^2...}$ | Thuật toán Oxy là giải thuật số học tất định, sai số do dung sai. Công thức khoảng cách gõ sai làm giảm uy tín. | Chuẩn hóa thuật ngữ "Lỗi ngưỡng dung sai hình học"; sửa công thức: $AB = \sqrt{(0 - (-3))^2 + (5 - 0)^2} = \sqrt{3^2 + 5^2} = \sqrt{34}$. | `geosolver_desktop.py` (Dòng 13180-13230) & Báo cáo v3.1 |
| **3. Ngưỡng dung sai & Thang đo** | Dùng $\max(0.025, 0.006 \cdot L_{\max})$ có sàn cố định $0.025$. | Sàn $0.025$ sẽ sai khi tỉ lệ thu nhỏ $0.001$ hoặc phóng to $10000$. Cần test âm tính tọa độ thực. | Chuyển sang dung sai thích ứng: $\text{tol} = \max(10^{-4}, 0.006 \cdot L_{\max})$; Tích hợp Định lý lưới nguyên $\mathbb{Z}^2$ và test âm tính $1 : 1.02 : 1$. | `tests/test_geometry_invariants.py` (`test_02`, `test_03`, `test_06`) |
| **4. Hiển thị nhãn trên Canvas** | Xóa vĩnh viễn lệnh `create_text` của các đoạn thẳng và đường thẳng. | Mâu thuẫn với tên gọi "Clean Print Mode". Học sinh/giáo viên rất cần xem độ dài cạnh. Nên làm công tắc bật/tắt. | Thêm công tắc **"Hiện kích thước cạnh (Dimensions)"** trong menu *Hiển thị*, mặc định tắt để in sạch, bật lên để học tập. | `geosolver_desktop.py` (Dòng 2658 & 18324) |
| **5. Công thức chu vi Elip** | Dùng Ramanujan I và ghi "chu vi chính xác". | Ramanujan I sai tới $0.415\%$ khi $b \to 0$. Cần chuyển sang Ramanujan II ($<0.05\%$) và ghi rõ là xấp xỉ. | Nâng cấp lên **Ramanujan II**: $P \approx \pi (a+b)(1 + 3h/(10+\sqrt{4-3h}))$; kết hợp $P=4a$ khi $b=0$. Sai số toàn dải $\le 0.038\% < 0.05\%$. | `geosolver_desktop.py` (Dòng 179-194) & `test_08` |
| **6. Xử lý Elip suy biến & Tiêu điểm** | Ép cứng $a \ge c + 0.15$ khi $a \le c$. | Chưa xử lý trường hợp suy biến khi $M \in F_1F_2$ ($b = 0$), hoặc hai tiêu điểm trùng nhau $F_1 = F_2$. | Xử lý $F_1 = F_2 \implies b = a$ (đường tròn); $M \in F_1F_2 \implies b = 0$ (đoạn thẳng); kẹp an toàn $\max(0, a^2 - c^2)$. | `geosolver_desktop.py` (Dòng 200-230) & `test_07` |
| **7. Độ tương phản WCAG 2.1** | Đánh giá chung chung $\ge 4.0:1$, nút Dark Studio `#0284C7` + chữ trắng chỉ đạt $4.12:1$. | Ngưỡng $4.0:1$ không phải chuẩn WCAG AA ($\ge 4.5:1$). Bảng contrast thiếu chi tiết từng cặp màu. | Nâng nút chọn Dark Studio lên `#38BDF8` + chữ `#09090B` ($8.84:1$). Bảng đối soát chi tiết từng cặp màu, tất cả đều $\ge 4.71:1$ (đạt AA/AAA). | `tests/test_geometry_invariants.py` (`test_09`) |
| **8. Kiểm tra 3 điểm thẳng hàng** | So sánh tích có hướng trực tiếp với số 0 tuyệt đối. | So sánh với 0 bằng số thực không ổn định, cần chuẩn hóa theo độ dài 2 cạnh. | Chuẩn hóa tích có hướng tương đối: $\frac{\|u \times v\|}{\|u\| \cdot \|v\|} < 10^{-7}$ (tương đương $\sin \theta < 10^{-7}$, ổn định tuyệt đối). | `tests/test_geometry_invariants.py` (`test_04`) |
| **9. Bộ kiểm thử tự động** | Chỉ có 10 ca kiểm tra chung chung, thiếu script tự động cụ thể. | Cần script tự động chạy độc lập được, kiểm tra cả ca dương tính, âm tính thực và ca biên. | Xây dựng bộ Unit Test 9 ca toàn diện chạy tự động qua `unittest`: Đạt 9/9 PASS ($0.043$s). | `tests/test_geometry_invariants.py` |
| **10. Cấu hình PyInstaller Spec** | File mã `.py` vừa nằm trong `datas` vừa nằm trong `hiddenimports`. | Thừa và làm lộ mã nguồn thô trong gói cài đặt. Đường dẫn tương đối `../` dễ lỗi trên CI. | Gỡ bỏ toàn bộ `.py` khỏi `datas`; đưa vào `pathex` và `hiddenimports` để nén an toàn bytecode trong `PYZ`. | `geosolver/GeoSolver.spec` |
| **11. Tải mô hình AI đa ổ đĩa** | Mặc định tải về `%LOCALAPPDATA%` trên ổ C:. | Nếu ổ C: đầy sẽ không tải được, cần cho phép lưu sang ổ đĩa khác. | Bổ sung nút **`[📁 Chọn ổ đĩa...]`** trong `ModelDownloadDialog`, tự động kiểm tra dung lượng ổ đĩa D:, E:, USB... | `stem_shared_core/hf_downloader.py` (Dòng 565-580) |

---

### HƯỚNG DẪN TRA CỨU THEO BỘ HỒ SƠ:
* Xem bản khởi thảo ban đầu: [`01_BAO_CAO_THAM_DINH_BAN_DAU_V3.0.md`](file:///d:/AI%20DATA/STEM_APP/docs/audit_reports/01_BAO_CAO_THAM_DINH_BAN_DAU_V3.0.md)
* Xem toàn văn ý kiến phản biện của Claude: [`02_Y_KIEN_PHAN_BIEN_CHUYEN_GIA_CLAUDE.md`](file:///d:/AI%20DATA/STEM_APP/docs/audit_reports/02_Y_KIEN_PHAN_BIEN_CHUYEN_GIA_CLAUDE.md)
* Xem báo cáo giải trình và kết quả kiểm định thực nghiệm: [`03_BAO_CAO_GIAI_TRINH_VA_KIEM_DINH_THUC_NGHIEM_V3.1.md`](file:///d:/AI%20DATA/STEM_APP/docs/audit_reports/03_BAO_CAO_GIAI_TRINH_VA_KIEM_DINH_THUC_NGHIEM_V3.1.md)
* Xem mã nguồn bộ kiểm thử tự động: [`tests/test_geometry_invariants.py`](file:///d:/AI%20DATA/STEM_APP/tests/test_geometry_invariants.py)
