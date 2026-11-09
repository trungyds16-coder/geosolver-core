# Phản biện đợt 8: thẩm định báo cáo v2.7 (08/11/2026)

**Đối tượng:** `BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_7.md`: hai hàm lõi, bộ test `run_batch_auto_test.py` và nhật ký chạy đính kèm, Rubric 5 tiêu chí, bảng đặc tính kỹ thuật.

---

## 0. Phạm vi và cách làm

Như các đợt trước, tôi **trích tự động các khối mã từ chính file v2.7 và chạy thật** với SymPy 1.14.0 (giao diện được thay bằng đối tượng giả). Đã làm:

- chạy hai hàm lõi trên các ca căn thức và Diophantine (kể cả ca hằng số, ca giả lập nhánh `unknown`);
- chạy **bộ test đính kèm** nguyên văn, và chạy riêng logic của bộ test đó trên các ca khó;
- **oracle độc lập** cho hàm Diophantine: 699 hệ ngẫu nhiên (2 phương trình, 3 ẩn, đúng một tham số tự do, luôn có ít nhất một nghiệm thực nguyên dương ban đầu), đối chiếu tập nghiệm với bộ liệt kê tham số trong cửa sổ k ∈ [−3000, 3000] (không dùng CRT). Một lần chạy đầu của tôi dùng hộp vét cạn quá nhỏ (1..40) nên báo lệch giả; tôi đã thay bằng oracle trên và loại kết quả đó.

**Chưa làm được:** không thấy nơi gọi hàm, `clean_display_expr` và giao diện; không có tệp `LICENSE` hay đường dẫn kho mã.

---

## 1. Kết luận

**Chín ý kiến đợt 7 đã được xử lý ở phần mã và phần văn bản, và hầu hết đúng.** Các lỗi hiển thị đợt 7 đã hết, hàm Diophantine vẫn không sai (699 hệ, 0 lỗi). Tuy vậy còn một vấn đề lớn về **bằng chứng kiểm thử**, và vài điểm cần sửa trước khi nộp.

| Mức | Vấn đề | Mục |
|---|---|---|
| **Cao** | Bộ test đính kèm **không gọi hai hàm lõi**; nó chạy một bản cài đặt riêng, cũ hơn, nên "8/8 (100%)" không chứng minh gì cho v2.7 | 3.1 |
| Trung bình | Khối mã dán trong báo cáo **không chạy nguyên văn** (IndentationError) | 3.2 |
| Trung bình | Số liệu thời gian và cấu hình máy không nhất quán, không khớp log; giấy phép chỉ có tên tệp, không có đường dẫn | 3.3 |
| Thấp–TB | Chi tiết hiển thị còn sót (S gồm giá trị gần đúng, vòng quét thừa, nhãn "tiệm cận") | 3.4 |
| Thấp–TB | Kế hoạch thực nghiệm: chỉ số chính, kiểm định tính mù, người biên tập, kế hoạch phân tích | 4 |
| Thấp | Còn vài cụm tự đánh giá | 3.5 |

---

## 2. Điểm đã sửa đúng (xác nhận bằng chạy mã)

| Hạng mục | Kết quả chạy thực |
|---|---|
| (1) Nghiệm phức √x = x²+1 | Mã in `x ≈ -0.3438 + 1.3584i`, `x ≈ 0.3438 - 0.6254i`…; không còn "= ≈" và "+ -". Giá trị trong báo cáo khớp mã |
| (2) Nhãn D_sign khi g là hằng | g = 1/2 và g = 0: "Luôn thỏa mãn với mọi x ∈ ℝ"; g = −2: "Không tồn tại x thỏa mãn". Đúng cả ba |
| (3) Bước kết luận khi có `indeterminate` | Giả lập `check_sign_exact` luôn trả `unknown`: hàm in "CHƯA THỂ KẾT LUẬN TẬP NGHIỆM ĐẦY ĐỦ", không còn in "S = ∅" hay "chính thức" |
| (4) Thông điệp liệt kê | ≤ 10 nghiệm: "Liệt kê toàn bộ n"; > 10: "tổng cộng n … hiển thị 10 đầu tiên"; ca 29 nghiệm và 10⁹ nghiệm đều nhất quán với nhãn LaTeX |
| (5) Nghiệm Cardano | Ba nghiệm thực của √(x³−3x+1) = 1/2 hiển thị ≈ 0.2556, 1.5901, −1.8456 ở cả bước NHẬN lẫn S |
| Các ca còn lại | Đảo vế, hệ số trước căn, hai căn → từ chối, √(x−1)=x−3, √(x+1)=−2, √(x²−4)=0, Trăm trâu, `SYS_DIO_03` (4 ẩn), phản ví dụ A, B, d ≥ 2: đều đúng |
| Oracle độc lập | **699 hệ** (491 hữu hạn, 208 vô hạn): 0 ngoại lệ, 0 bỏ sót, 0 sai số lượng/phân loại |
| Nhật ký chạy | Tôi chạy lại bộ test đính kèm: kết quả khớp log (chỉ khác thời gian). Log là thật |
| Rubric | Đã thêm C5, đổi sang Krippendorff's α (ordinal)/ICC, thêm kiểm tra tính mù, đưa SymPy về vai trò mốc cơ sở |
| Ngôn ngữ | Các cụm "dứt điểm", "triệt để", "100%", "an toàn tuyệt đối" đã gần như hết (còn vài chỗ ở 3.5) |

---

## 3. Các vấn đề còn lại

### 3.1. Bộ test đính kèm không kiểm thử mã của báo cáo (mức: cao)

Tôi đọc toàn văn `run_batch_auto_test.py` và chạy nó. **Nó không import và không gọi `solve_radical_pedagogical` hay `solve_underdetermined_or_diophantine`.** Thay vào đó mỗi nhánh tự cài đặt lại logic ngay trong tệp test, theo phiên bản cũ hơn nhiều:

- **Nhánh căn thức:** dùng `gx = sp.simplify(rad - eq_expr)` (công thức sai ở v2.4), `float(...evalf())` thay cho `real_status`, không lọc nghiệm phức.
- **Nhánh Diophantine:** quét tham số `range(1, 1000)`, không dùng đồng dư, không có phân loại trạng thái, không có trần hay thông báo.

Hậu quả: "8/8 bài đạt (100.0%)" cho biết logic **cũ** trong tệp test đạt 8 ca dễ, không cho biết gì về mã v2.7. Tôi chạy riêng logic đó trên các ca khó:

| Ca | Logic của bộ test | Hàm lõi v2.7 |
|---|---|---|
| √x = x² + 1 | **Sập** `TypeError: Cannot convert complex to float` | Đúng, S = ∅ |
| √(x³−3x+1) = 1/2 | **Sập** cùng lỗi | Đúng, 3 nghiệm thực |
| x + z = 10⁹, y = 1 | Đếm **999** nghiệm (thực tế 999 999 999) | Đúng |

Ba vấn đề phụ cùng chỗ:

1. Với các ca Diophantine, `expected_count` (3, 2, 4) trùng đúng với kết quả mà chính vòng quét đếm ra, nên phép so sánh có tính **vòng tròn**, không có đối chiếu độc lập.
2. Cả 8 ca đều là ca dễ. **Không có ca nào** trong số các ca đã gây lỗi ở các đợt trước (đảo vế, hệ số trước căn, nghiệm phức, Cardano, phản ví dụ A, B, trần, d ≥ 2, nhánh `unknown`, hằng số D_sign).
3. Thời gian trong log (1.8–592 ms) là thời gian của **đoạn logic trong bộ test**, không phải của CAD Math Studio. Dòng "xác thực bởi bộ kiểm thử STEM Core" ở cuối báo cáo và con số thời gian ở bảng 5 cũng dựa trên log này.

**Đề xuất:**

- Tách hai hàm lõi khỏi giao diện (hoặc dùng đối tượng giả như tôi đã làm) để bộ test **gọi trực tiếp hàm thật**.
- Kiểm tra các mệnh đề thay cho "số nghiệm kỳ vọng" tự đếm: ví dụ mọi nghiệm trả về thỏa phương trình gốc; mọi nghiệm bị loại có g(r) < 0 hoặc là nghiệm phức; số nghiệm khớp một oracle độc lập.
- Thêm các ca nêu ở trên và một oracle ngẫu nhiên (kiểu mục 0), ghi rõ hạt giống (seed) và phiên bản SymPy.
- Nếu chưa kịp, bỏ câu "xác thực bởi bộ kiểm thử" và ghi rõ bộ test hiện chỉ là "kiểm tra sơ bộ logic độc lập, chưa gọi mã chính".

### 3.2. Mã dán trong báo cáo không chạy nguyên văn (mức: trung bình)

Báo cáo nói mã "được trích xuất trực tiếp từ `cad_math_v2.py`". Khi ghép hai khối mã thành một tệp và chạy, Python báo `IndentationError: unindent does not match any outer indentation level` ở dòng khai báo hàm thứ hai: hàm thứ nhất được dán ở cột 0 nhưng thân hàm thụt 8 ký tự, hàm thứ hai thụt 4. Có vẻ là lỗi dán (cả hai là phương thức của một lớp). Sau khi tôi thụt lề hàm thứ nhất thêm 4 ký tự và bọc trong `class`, mã chạy bình thường. Cần dán lại với thụt lề nhất quán (cả lớp, hoặc cả hai hàm cùng mức) để người đọc chạy được.

### 3.3. Số liệu thời gian, cấu hình, giấy phép (mức: trung bình)

1. **Ba chỗ khác nhau:** dòng 7 của bảng tiếp thu ghi "trung bình 0.1 – 0.4 s"; bảng 5 ghi "0.05 – 0.40 s"; log ghi từ 1.8 ms đến 592 ms (và đó là thời gian của bộ test, xem 3.1). Cần một phương pháp đo duy nhất áp dụng cho hàm thật (số lần lặp, trung vị, các ca đo) và một dải số duy nhất.
2. **Cấu hình máy "Intel Core i7":** cần khớp với máy đo thực tế. Nếu máy đo là máy khác (ví dụ Core i3 thế hệ 14), phải sửa mô tả; thời gian trên máy khác nhau có thể lệch đáng kể.
3. **Số liệu của đối chiếu:** "SymPy 0.05–0.20 s" và "Symbolab/Photomath 1.0–3.0 s" chưa có phương pháp đo hay nguồn. "Bắt buộc kết nối Internet liên tục" và "đăng ký thuê bao trả phí" cũng chưa có nguồn, ngày kiểm tra, gói dịch vụ; nhiều dịch vụ có bậc miễn phí. Tôi không kiểm chứng được các phát biểu này.
4. **Giấy phép:** bảng tiếp thu nói đã "dẫn link", nhưng văn bản chỉ có tên tệp `LICENSE`, không có đường dẫn kho mã hay nội dung giấy phép. Cần đường dẫn công khai (hoặc đính kèm văn bản giấy phép).

### 3.4. Chi tiết hiển thị còn sót (mức: thấp–trung bình)

- Dòng kết luận in `S = {≈ 0.2556, ≈ 1.5901, ≈ -1.8456}`: giá trị gần đúng bị viết như phần tử của tập nghiệm. Nên ghi "S gồm 3 nghiệm thực, gần đúng: …" hoặc "(nghiệm thực của x³ − 3x + 3/4 = 0)".
- Với hệ chạm trần, mã vẫn thế ngược và gọi `simplify` cho 1000 ứng viên dù chỉ hiển thị 10 (ca x + z = 10⁹ chạy ~0.46 s trên máy của tôi). Số nghiệm đã được tính trực tiếp bằng công thức, nên có thể chỉ kiểm tra thế ngược trên các bộ được hiển thị (kèm kiểm tra mẫu ngẫu nhiên) để nhanh hơn nhiều lần.
- Dòng "Hệ có tổng cộng n bộ nghiệm…" xuất hiện hai lần liền nhau (ở bước liệt kê và ở bước kết luận).
- Câu "Dấu biểu thức tiệm cận ngưỡng bất định" dùng chữ "tiệm cận" chưa chính xác (không có giới hạn nào ở đây); nên viết "chưa xác định được dấu bằng phương pháp đại số hay số học độ chính xác cao".
- Nhánh `unknown` vẫn **chưa có ca tự nhiên** (chỉ kiểm bằng giả lập). Có thể ghi rõ điều này như một hạn chế thay vì để người đọc suy đoán.

### 3.5. Câu chữ còn lại (mức: thấp)

Phần lớn các cụm tuyệt đối đã được gỡ. Còn: "Phương pháp luận nghiên cứu **vững chắc**" (dòng 9, tự khen), "Thông điệp **hoàn toàn** nhất quán" (dòng 4), "Lời kết luận logic, **chặt chẽ**" (dòng 3), và dòng cuối "**xác thực** bởi bộ kiểm thử STEM Core" (xem 3.1). Gợi ý: đổi thành mô tả sự việc ("đã thống nhất thông điệp ở các ca X, Y") thay cho nhận xét chất lượng.

---

## 4. Rubric và kế hoạch thực nghiệm

**Tiến bộ rõ:** thêm C5, chuyển sang thang thứ tự phù hợp, có bộ bài 30 mục với tỉ lệ cụ thể, có kiểm tra tính mù, SymPy được nêu là mốc cơ sở.

**Còn nên chỉnh:**

1. **"α ≥ 0.70 hoặc ICC ≥ 0.75":** chữ "hoặc" cho phép chọn chỉ số nào đạt ngưỡng sau khi xem dữ liệu. Nên chỉ định **trước** một chỉ số chính và ngưỡng, chỉ số còn lại là phụ.
2. **Kiểm định χ² "để chứng minh tính vô tư":** không có ý nghĩa thống kê không chứng minh người chấm đã bị che mù, nhất là khi mẫu nhỏ. Nên báo tỉ lệ đoán đúng kèm khoảng tin cậy và so với 25%, thay vì dùng từ "chứng minh".
3. **Người biên tập lời giải:** "biên tập về cùng khuôn mẫu và cùng ngôn ngữ" do ai làm? Nếu là nhóm tác giả, có nguy cơ thiên lệch khi viết lại đầu ra của đối thủ. Nên có người độc lập hoặc quy tắc biên tập công bố trước, kèm lưu bản gốc.
4. **Kế hoạch phân tích:** chưa nêu giả thuyết chính, phép so sánh nào (từng tiêu chí hay tổng điểm), cách xử lý bài ngoài phạm vi (công cụ từ chối có được tính điểm không), và độ mạnh thống kê của cỡ mẫu. Nên đăng ký trước.
5. **Thang C5:** ranh giới giữa mức 3 ("khá giỏi lớp 10–12") và mức 4 ("mặt bằng chung") dễ chồng lấn; nên mô tả bằng hành vi quan sát được (ví dụ có dùng thuật ngữ ngoài chương trình không) thay cho đặc điểm học sinh.
6. Chưa nêu việc xin sự đồng ý của giáo viên tham gia và cách lưu/công bố dữ liệu thô.

---

## 5. Việc cần làm trước khi nộp (theo thứ tự ưu tiên)

| # | Việc | Mức |
|---|---|---|
| 1 | Làm bộ test **gọi hai hàm lõi thật**, kiểm mệnh đề thay cho số đếm tự tính, thêm các ca then chốt và oracle (3.1) | Cao |
| 2 | Nếu chưa kịp: gỡ câu "xác thực bởi bộ kiểm thử", ghi rõ giới hạn của bộ test hiện tại | Cao |
| 3 | Dán lại khối mã với thụt lề nhất quán để chạy được nguyên văn (3.2) | Trung bình |
| 4 | Thống nhất số liệu thời gian, đo trên hàm thật, ghi cấu hình máy đúng; thêm đường dẫn giấy phép; nguồn cho bảng so sánh (3.3) | Trung bình |
| 5 | Xử lý chi tiết hiển thị còn sót (3.4) | Thấp–TB |
| 6 | Chỉnh kế hoạch thực nghiệm: chỉ số chính, báo cáo tính mù, người biên tập, kế hoạch phân tích (mục 4) | Thấp–TB |
| 7 | Gỡ các cụm tự đánh giá còn lại (3.5) | Thấp |

---

## 6. Kết luận

Hai hàm lõi giờ cho kết quả đúng và hiển thị rõ trên tất cả ca tôi thử, kể cả sau 699 hệ ngẫu nhiên và ca giả lập nhánh bất định. Điểm yếu lớn nhất đã chuyển từ **mã** sang **bằng chứng**: bộ test và log đính kèm kiểm một bản cài đặt khác, nên chưa thể dùng làm bằng chứng cho v2.7. Gọi trực tiếp hai hàm thật trong bộ test (và thêm các ca then chốt) là việc quan trọng nhất còn lại; các điểm khác chủ yếu là nhất quán số liệu và trình bày.

---

*Phản biện này dựa trên việc trích và chạy thật các khối mã trong báo cáo v2.7 (SymPy 1.14.0, giao diện được thay bằng đối tượng giả), chạy lại bộ test đính kèm và oracle nêu ở mục 0. Không kiểm chứng các phát biểu về dịch vụ thương mại, giấy phép và cấu hình máy của tác giả. Đây là tham vấn kỹ thuật bằng công cụ AI, không thay thế thẩm định bởi người thật.*
