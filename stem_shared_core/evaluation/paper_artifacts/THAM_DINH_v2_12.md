# BIÊN BẢN THẨM ĐỊNH LẠI HỒ SƠ v2.12
## CAD Math Studio & GeoSolver 2D – Báo cáo khoa học & Giải trình phản biện

**Ngày thẩm định:** 08/11/2026
**Đối tượng:** `BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_12.md`
**Phương pháp:** đọc toàn văn; trích hai khối mã (§8.1, §8.2) ra tệp, băm SHA-256, chạy lại harness; viết thêm các đột biến ngoài 6 toán tử của nhóm tác giả để thăm dò độ mạnh của bộ kiểm thử.

---

## 1. KẾT LUẬN

**Chấp thuận có điều kiện.** Đề nghị đóng vòng phản biện **sau khi** nhóm tác giả hoàn tất 6 mục bắt buộc ở §5. Các mục này chỉ là sửa văn bản và thêm 3 ca kiểm thử nhỏ, **không cần mở vòng phản biện mới**.

| Vấn đề | Kết luận | Lý do tóm tắt |
|---|---|---|
| **B1** – mã lõi tự chứa, hash khớp | **Đóng** | Hash khớp, mã chạy được, không còn đối tượng Tkinter, kết quả đúng/sai tái lập được. |
| **B2** – kiểm thử đột biến | **Chưa đóng** | 6/6 tái lập được, nhưng mô tả cơ chế M6 sai, kết luận quá đà, và bộ Suite còn khoảng trống (§3). |
| **B3** – oracle không dùng `sp.ilcm` | **Đóng có điều kiện** | `sp.ilcm` đã bỏ khỏi mã; giới hạn phương pháp luận được thừa nhận. Cần bỏ chữ "độc lập" hoặc làm oracle độc lập thật (§4). |
| **P1–P7** | P1, P2, P3, P7 đạt; **P4 chưa đạt**; P6 đạt về số học nhưng đặt tên chưa đúng; P5 chỉ kiểm tra một phần | Xem §4–§5. |

---

## 2. KẾT QUẢ TÁI LẬP (B1)

Môi trường của tôi: Python 3.12.3, SymPy 1.14.0, Linux (không phải Python 3.14.5 / i7-11800H của nhóm tác giả).

| Hạng mục | Kết quả |
|---|---|
| SHA-256 `cad_math_core.py` (khối §8.1, đầu dòng 267 đến hết dòng 701, ký tự xuống dòng LF) | `ddb945c9…586e` → **khớp** |
| SHA-256 `run_batch_auto_test.py` (khối §8.2) | `b01a8fc3…d9d5` → **khớp** |
| Cú pháp, import | Hợp lệ; không còn import Tkinter (chỉ còn một dòng chú thích nhắc tên Tkinter) |
| 21 ca Suite | **21/21 đạt** |
| Oracle hộp cố định | **100/100 khớp** |
| Mutation Score trên Suite | **6/6**; số hệ ngẫu nhiên bị giết **14, 18, 25, 11, 0** cho M1–M5, **trùng từng số** với log của nhóm tác giả |
| Số học trong log của nhóm | Tôi tính lại từ 21 trung vị: tổng 1987.01, TB 94.62, trung vị phân hệ Radical 161.19 và Diophantine 3.59, **IQR 128.83** → đều nhất quán |
| Thời gian | Máy tôi: tổng 444.28 ms, IQR 28.01 ms. Khác máy nên khác số, không phải lỗi |

Lưu ý khi đọc hash: giá trị chỉ khớp khi tệp dùng LF và có đúng một ký tự xuống dòng cuối. Tệp .md gốc dùng CRLF. Nên ghi chú điều này trong §8 để người tái lập không băm lệch.

**Một điểm làm yếu giá trị của "bản ghi nguyên văn" (§5.1):** dòng thông tin môi trường (`Python 3.14.5 | i7-11800H…`) là **chuỗi gõ cứng** trong `print`. Khi tôi chạy trên Python 3.12.3, log vẫn in "Python 3.14.5". Vì vậy dòng này không chứng minh được phần cứng hay phiên bản đã dùng.

---

## 3. B2 – KIỂM THỬ ĐỘT BIẾN

### 3.1. Điều đã đúng
- Hai ca `DIO_13` và `DIO_14` có thật và tiêu diệt đúng M1, M2, M3 như mô tả.
- M4 bị `DIO_04` giết, M5 bị `DIO_12` giết, kết quả tái lập được.

### 3.2. Mô tả cơ chế M6 trong §4.2 là sai
Báo cáo viết M6 làm "nghiệm sai **lọt vào tập `valid`**". Tôi chạy thực tế trên `RAD_01`:

> M6 → `valid = 1`, `rejected = 0`, `indeterminate = 1`

Nghiệm ngoại lai 2−√2 **không** vào `valid`. Do `s_gx == 'neg'` không thỏa nhánh nhận, nó rơi vào `indeterminate`. Mutant vẫn bị giết (vì số nghiệm bị loại lệch kỳ vọng), nhưng lời giải thích cần sửa.

Tương tự M5: mutant bị giết vì **`TypeError`** (`sc[0]` trên `None`), tức bị giết bằng sập chương trình chứ không phải bằng đầu ra sai. Nên ghi rõ. Khối kiểm thử ngẫu nhiên của M5 không bọc `try/except`, nên chỉ chạy được vì không có hệ nào trong 100 hệ chạm nhánh xung đột CRT.

### 3.3. Kết luận "6/6 = 100%" bị diễn đạt quá mức
Câu "bảo đảm toàn bộ các toán tử đột biến đều bị phát hiện và ngăn chặn" (§4.2, cuối) không đúng phạm vi. Đúng ra là: *6 mutant do chính nhóm tác giả chọn đều bị giết bởi Suite*. Suite lại được bổ sung `DIO_12/13/14` đúng để giết các mutant đó, nên 6/6 phản ánh việc Suite khớp với danh sách mutant hơn là độ mạnh tổng quát.

### 3.4. Thăm dò bằng đột biến ngoài danh sách
Tôi chạy thêm 12 đột biến đơn giản trên Suite (21 ca). **7 sống sót:**

| Đột biến (sửa trong mã lõi) | Sống sót | Đánh giá |
|---|:---:|---|
| `if start_val > hi` → `>=` | Có | **Khoảng trống thật**: không có ca nghiệm đúng ở biên trên sau đồng dư |
| `lo > hi` → `lo >= hi` | Có | **Khoảng trống thật**: không có ca miền một điểm |
| `min(n_total, 10)` → `min(n_total, 9)` | Có | **Khoảng trống thật**: `DIO_05` không kiểm tra số nghiệm hiển thị |
| `range(3)` → `range(2)` (liệt kê 3 nghiệm nhỏ nhất) | Có | **Khoảng trống thật**: các ca vô hạn chỉ kiểm `sample in sols`, không kiểm độ dài |
| Bỏ `'zero'` khỏi nhánh nhận nghiệm | Có | **Khoảng trống thật**: không có ca nghiệm với g(r) = 0 |
| `elif s_fx == 'neg'` → `False` | Có | Có thể tương đương: tại nghiệm của phương trình bình phương f(r) = g(r)² ≥ 0 nên nhánh này không thể chạy (chỉ chạy được qua `mock` của RAD_07) |
| `lo = Integer(1)` → `Integer(0)` | Có | Có thể tương đương: chính biến tự do luôn áp cận dưới ≥ 1 |

Năm đột biến còn lại (đổi `a_sym > 0`, `a_sym < 0`, `b_sym <= 0`, dấu trong `rem`, tắt nhánh `d == 0`) đều bị giết. Đột biến "bỏ nhánh loại nghiệm phức" tôi không chạy xong trong giới hạn thời gian nên không kết luận.

Tôi đã thử và xác nhận 3 ca bổ sung sau đây giết được các mutant tương ứng:

| Ca đề xuất | Kết quả solver gốc | Giết được |
|---|---|---|
| **DIO_15**: `[2x − z + 1, y + z − 4]` | `FINITE_BOUNDED`, n = 1, nghiệm `(1, 1, 3)` | `start_val >= hi` |
| **DIO_16**: `[x + z − 2, y − 2]` | `FINITE_BOUNDED`, n = 1, nghiệm `(1, 2, 1)` | `lo >= hi` và `start_val >= hi` |
| **RAD_08**: `√x − x = 0` | `valid = [0, 1]` (g(0) = 0 hợp lệ) | bỏ nhánh `'zero'` |

Với hai khoảng trống còn lại (`min(n_total, 10)`, `range(3)`), cần thêm kiểm tra `len(sols)` đúng 10 và đúng 3 trong harness.

---

## 4. CÁC NHẬN XÉT KHÁC

### 4.1. B3 – Oracle chưa "độc lập" như tên gọi
- Đã đạt: `sp.ilcm` không còn trong mã (chỉ còn nhắc trong chú thích và văn bản).
- Còn lại: oracle vẫn dùng `sp.linsolve` để lấy biểu diễn affine, **phân tầng 25/25/25/25 theo nhãn do chính solver gán**, và tái dùng cùng logic `has_neg_slope` với solver. Nhóm tác giả đã thừa nhận phần `linsolve`; hai điểm sau chưa được nêu.
- Tích cực: tôi kiểm tra trong tập 100 hệ, số nghiệm lớn nhất của nhóm `FINITE_BOUNDED` là 40, nên hộp N = 3000 dư rộng. Nên **thêm `assert`** vào harness (hi < N và điểm bắt đầu + 3·mod ≤ N) thay vì chỉ nêu giả định.
- Gợi ý oracle độc lập thật: với 3 ẩn, 2 phương trình, cho z chạy 1…N, giải (x, y) bằng quy tắc Cramer trên `fractions.Fraction` từ **hệ số gốc**, không qua `linsolve`; phân tầng theo kết quả oracle.

### 4.2. P4 – Ngôn từ khẳng định tuyệt đối **chưa được làm sạch**
Giải trình P4 nói đã loại bỏ, nhưng văn bản còn sót:
- "hoàn toàn": dòng 144, 145, 148 ("tiêu diệt hoàn toàn"), 269, 1340
- "100%": dòng 146, 264, 1340, 1341
- "trọn vẹn": dòng 1339; "khớp tuyệt đối": dòng 1340; "bảo đảm toàn bộ": dòng 153
- "độc lập" xuất hiện 13 lần, phần lớn gắn với oracle (xem §4.1)

### 4.3. Nhãn "Invariant 3" bị dùng với hai nghĩa
§2.2 định nghĩa Bất biến 3 là **phân hoạch** (valid + rejected + indet = raw). Nhưng bảng §3.2 và log lại dùng "Inv 3" cho Diophantine với nghĩa **nghiệm nguyên dương thỏa hệ gốc**, một bất biến không được định nghĩa ở §2.2. Cần đặt tên riêng (ví dụ Bất biến D).

### 4.4. P6 – IQR đo cái khác với điều được nói
Giá trị 128.83 ms được tính trên 21 trung vị của **21 bài khác nhau**; nó mô tả độ chênh khối lượng giữa các bài (0.09 đến 705 ms), không phải độ nhiễu đo giữa các vòng. Để minh họa độ ổn định của phép đo, nên báo IQR (hoặc min–max) giữa 5 vòng **cho từng bài**.

### 4.5. §6 – So sánh công cụ
- Ô "Phân tích nghiệm nguyên Diophantine / SymPy thuần: *Cần người dùng tự viết thuật toán*" quá mạnh. SymPy có `sympy.solvers.diophantine.diophantine` cho **một** phương trình, trả họ nghiệm nguyên tham số. Điều đề tài bổ sung là xử lý hệ, miền nghiệm dương và đếm nghiệm; nên viết như vậy.
- Cột Photomath/Symbolab dựa trên "khảo sát định tính tháng 10/2026" nhưng không nêu số bài thử, cách chọn bài, phiên bản ứng dụng. Cần bổ sung hoặc chuyển thành ghi chú giới hạn.
- "Bám sát SGK GDPT 2018" cần chỉ ra bộ sách và bài cụ thể.

### 4.6. §7 – Rubric (giai đoạn sau, không chặn vòng này)
- Tiêu chí **C4** (crash, chạy chậm) không quan sát được từ văn bản lời giải nên giáo viên chấm mù không đánh giá được.
- Việc "ẩn danh nguồn gốc" khó thực hiện khi SymPy chỉ trả danh sách nghiệm còn CAD Math Studio trả 4 bước; hai kiểu đầu ra nhận ra ngay.
- Chưa nêu số giáo viên, số bài, tính toán cỡ mẫu. Cluster bootstrap theo giáo viên kém tin cậy khi số giáo viên nhỏ.
- Cần nêu thủ tục đạo đức nghiên cứu (đồng thuận, phụ huynh) trước khi thực nghiệm trên học sinh.

### 4.7. Điều tôi chưa kiểm tra
- Phần cứng và Python 3.14.5 của nhóm tác giả (không thể kiểm chứng từ bên ngoài).
- Việc hiển thị toàn bộ công thức LaTeX (P5): chỉ đọc lướt.
- Nội dung so sánh Photomath/Symbolab.

---

## 5. MỤC BẮT BUỘC TRƯỚC KHI ĐÓNG VÒNG

1. **Sửa mô tả M6** (§4.2): nghiệm ngoại lai chuyển sang `indeterminate`, không vào `valid`; ghi rõ M5 bị giết bằng `TypeError`.
2. **Gỡ ngôn từ tuyệt đối** còn sót ở các dòng nêu trong §4.2; sửa "bảo đảm toàn bộ toán tử" thành "6 mutant do nhóm lựa chọn".
3. **Thêm `DIO_15`, `DIO_16`, `RAD_08`** và kiểm tra `len(sols)` bằng 10 và 3; chạy lại và cập nhật log (kỳ vọng 24/24 trên Suite). Báo cáo trung thực các mutant còn sống sót nếu có.
4. **Thống nhất tên bất biến** ("Inv 3" đang mang hai nghĩa).
5. **Bỏ chuỗi gõ cứng về môi trường** trong harness; lấy từ `sys.version`, `platform`, `sympy.__version__` để log tự chứng minh.
6. **Đổi chữ "độc lập" của oracle** thành mô tả đúng ("oracle vét cạn trên biểu diễn affine của `linsolve`") **hoặc** triển khai oracle Cramer/`Fraction`; đổi tên chỉ số IQR (§5.2) hoặc bổ sung IQR giữa các vòng.

**Khuyến nghị (không chặn):** sửa ô SymPy `diophantine` ở §6, bổ sung quy trình khảo sát Photomath/Symbolab, ghi chú CRLF/LF khi băm, và thêm `assert` hộp N.

Sau khi hoàn tất 6 mục trên, tôi đề nghị chấp thuận chính thức đóng vòng phản biện lý thuyết và giải thuật.
