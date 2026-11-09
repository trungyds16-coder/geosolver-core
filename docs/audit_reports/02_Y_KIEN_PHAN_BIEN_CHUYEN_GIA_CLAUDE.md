# BẢN ĐÁNH GIÁ & Ý KIẾN PHẢN BIỆN CHUYÊN MÔN
## [CLAUDE INDEPENDENT EXPERT PEER-REVIEW - ĐỢT 1, 2 & 3]
*Văn bản lưu trữ toàn văn 3 đợt phản biện kỹ thuật độc lập của chuyên gia Claude.*  
**Mã hồ sơ:** AUDIT-2026-CLAUDE-CRITIQUE-FULL  
**Người đánh giá:** Claude Validator Review  
**Ngày cập nhật:** 08/11/2026  

---

## ĐỢT 1: PHẢN BIỆN BẢN KHỞI THẢO v3.0 (TÓM TẮT)
1. **Toán học & Store:** Hướng sửa dùng $d^2$ nguyên và Ramanujan là đúng; quy trình chứng chỉ Store MSIX và Authenticode chính xác.
2. **Vấn đề nghiêm trọng:** Báo cáo tự chứng nhận thiếu tính độc lập; dùng sai từ "ảo giác"; bộ test 10 ca quá mỏng, thiếu ca dương tính tam giác đều và ca biên; chưa có bằng chứng build gói thực tế.
3. **Kỹ thuật:** Dung sai phụ thuộc thang đo; mâu thuẫn Clean Print Mode vs xóa hẳn nhãn; file `.spec` thừa file `.py` trong `datas`.

---

## ĐỢT 2: ĐÁNH GIÁ LẠI BÁO CÁO v3.1 (BẢN 2)
1. **Lỗi gõ công thức mục 2.1:** $AB = \sqrt{0^2 + 5^2 - (-3)^2...}$ phải là $\sqrt{3^2 + 5^2} = \sqrt{34}$.
2. **Ramanujan I sai nhiều ở elip dẹt:** Khi $b \to 0$, $P \approx 3.984a$ (sai số $0.415\% > 0.05\%$). Đề xuất chuyển sang Ramanujan II ($P \approx \pi (a+b)(1 + 3h/(10+\sqrt{4-3h}))$.
3. **Chuẩn WCAG:** Ngưỡng $4.0:1$ không phải chuẩn WCAG AA ($\ge 4.5:1$). Bảng contrast thiếu liệt kê chi tiết từng cặp màu.
4. **Nhận diện:** Cần thêm ca âm tính với tọa độ thực; kiểm tra 3 điểm thẳng hàng cần chuẩn hóa tương đối; elip cần xử lý tiêu điểm trùng và bọc an toàn $\max(0, a^2 - c^2)$.

---

## ĐỢT 3: THẨM ĐỊNH LẦN 3 (CÓ MÃ VÀ LOG TEST)
1. **Tính lại số liệu độc lập:**
   * Ramanujan II sai số lớn nhất: $0.040\%$ tại $b \to 0$ (kết luận đúng).
   * Ramanujan II tại $b=0.5$ ($a=5$): Claude tính được $0.0012\%$ (bảng cũ ghi $0.0160\%$).
   * Ramanujan I tại $b=0.5$: Claude tính được $0.0842\%$ (bảng cũ ghi $0.1532\%$).
   * WCAG 16 cặp màu: Dao động $5.17 - 17.21:1$ (mọi cặp đều $\ge 5.17:1$, đạt chuẩn AA). Status bar Light thực tế là $8.40:1$ (bảng cũ ghi $4.85:1$).
   * Yêu cầu: Sinh bảng số trực tiếp từ chính code chạy thực tế.
2. **Vấn đề nghiêm trọng nhất: Test không gọi mã production:**
   * Test 01-06 tự mock lại công thức bên trong test, không import logic thật. Cần tách thành hàm thuần túy `classify_triangle(A, B, C)` trong production và cho test gọi trực tiếp hàm này.
3. **Lỗi nhận nhầm tam giác cân trên lưới nguyên:**
   * Tam giác $A(0,0), B(10,30), C(29,13)$ có $d^2(AB)=1000$ và $d^2(AC)=1010$ (chênh 0.5%). Hai cạnh không bằng nhau nhưng dung sai $0.6\%$ vẫn nhận nhầm là bằng nhau.
   * Cách sửa: Khi cả 3 điểm là số nguyên (`all_int`), so sánh chính xác $d^2$ nguyên ($1000 \ne 1010 \implies$ không cân); tích vô hướng nguyên bằng 0 cho góc vuông. Chỉ dùng dung sai cho tọa độ tự do.
4. **Đồng bộ tài liệu và mã nguồn:**
   * Khóa từ điển `THEMES_GEOSOLVER` trong báo cáo dùng tên cũ. Cần đồng bộ đúng khóa thực tế.
   * Gộp các file báo cáo thành một bản duy nhất, bỏ bản cũ để tránh mâu thuẫn.
   * Bổ sung thông tin: Lưu trữ API key bằng DPAPI, cơ chế chống lỗi đĩa đầy/đứt mạng/SHA-256 trong `hf_downloader.py`, chính sách quyền riêng tư và xếp hạng độ tuổi.
