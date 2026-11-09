# Phản biện đợt 7: thẩm định báo cáo v2.6 (08/11/2026)

**Đối tượng:** `BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_6.md`: hai hàm `solve_radical_pedagogical`, `solve_underdetermined_or_diophantine`, các bảng kiểm thử, Rubric và bảng đặc tính vận hành.

---

## 0. Phạm vi và cách làm

Như đợt 6, tôi **trích tự động hai khối mã từ chính file v2.6 và chạy thật** với SymPy 1.14.0 (bọc `self`, `tk` và các đối tượng giao diện bằng đối tượng giả để ghi lại đầu ra). Đã chạy:

- toàn bộ ca căn thức và Diophantine trong báo cáo, cộng một số ca tự chọn;
- oracle vét cạn trên **598 hệ ngẫu nhiên** (2 phương trình, 3 ẩn, đúng một tham số tự do, hệ số trong [−6, 6]), so tập nghiệm trong hộp 1..40;
- đo thời gian một số ca (trên máy của tôi, chỉ để kiểm tra tính hợp lý của con số trong báo cáo).

**Chưa làm được:** không có file `stem_shared_core/tools/run_batch_auto_test.py` mà báo cáo nói là kèm theo; không thấy nơi gọi hàm, `clean_display_expr` và giao diện. Các nhận xét về những phần đó là suy luận.

---

## 1. Kết luận

**Phần lớn các điểm đợt 6 đã được sửa đúng, và tôi xác nhận bằng chạy mã.** Lỗi hồi quy nghiêm trọng của v2.5 (loại nhầm nghiệm thực) đã hết, số liệu bài Trăm trâu đã đúng, hàm Diophantine vượt oracle (598/598, không ngoại lệ, không bỏ sót, không lệch tập).

Tuy vậy còn một số điểm cần xử lý trước khi nộp, **không điểm nào làm sai đáp số**, nhưng có điểm làm sai nội dung hiển thị cho học sinh hoặc sai mô tả trong báo cáo:

| Mức | Vấn đề | Mục |
|---|---|---|
| Trung bình | Báo cáo ghi nghiệm phức của √x = x²+1 là "0.1607 ± 0.7686i", **không khớp** kết quả chạy (±0.3438 ± …i) | 3.1 |
| Trung bình | Nhãn "Miền D_sign" in `[]` cho cả trường hợp luôn đúng lẫn luôn sai | 3.2 |
| Trung bình | Bước kết luận in "S = ∅" kể cả khi còn nghiệm "chưa xác định"; nhánh `unknown` vẫn chưa có ca test | 3.3 |
| Trung bình | Thông điệp liệt kê Diophantine tự mâu thuẫn ("liệt kê toàn bộ 29 bộ" rồi chỉ hiện 10; "hiển thị 1000" nhưng chỉ hiện 10) | 3.4 |
| Trung bình | Nghiệm Cardano của phương trình bậc ba in nguyên biểu thức dài, không có giá trị gần đúng | 3.5 |
| Trung bình | Con số "< 0.05 s" không khớp đo thực; tuyên bố "100% ngoại tuyến/cục bộ", "MIT" thiếu bằng chứng | 4 |
| Trung bình | Bộ test và log chạy được nhắc đến nhưng không đính kèm; dòng cuối "xác thực tự động…" chưa có cơ sở | 4 |
| Trung bình | Còn cụm tuyệt đối dù dòng 7 nói đã rà soát toàn bộ | 4 |
| Thấp–TB | Rubric: Fleiss' kappa chưa phù hợp thang thứ tự; chấm mù khó thực hiện được | 5 |

---

## 2. Những điểm đã sửa đúng (xác nhận bằng chạy mã)

| Hạng mục đợt 6 | Kết quả chạy thực |
|---|---|
| (1) Bộ lọc nghiệm thực `real_status` | √(x³−3x+1) = 1/2: **nhận đủ 3 nghiệm thực**; √x = x²+1: loại 4 nghiệm phức, S = ∅ |
| (2) Số liệu Trăm trâu | Mã cho (4,18,78), (8,11,81), (12,4,84), miền z ∈ [76, 85]; `SYS_DIO_02` cho (6,20,74), (13,10,77), z ∈ [72, 79]. Khớp bảng 3.2 |
| (3) Chạm trần | x + z = 10⁹, y = 1: in "tổng cộng 999999999 bộ nghiệm", không còn "liệt kê toàn bộ", không còn `S = {1000 bộ}` |
| (4) Trả 4 phần tử và bước kết luận | Hàm trả đúng `(steps, valid, rejected, indeterminate)`, có Bước 4 |
| (5) Họ nghiệm k ≥ 0 | Ca A: `z = 256 + 251·k (k ≥ 0)`; ca CRT: `z = 8 + 12·k (k ≥ 0)` |
| (6) Nhãn d ≥ 2 | "Họ nghiệm trên ℝ … (chưa xét trên ℤ⁺)" |
| Ca còn lại | Đảo vế, hệ số trước căn, hai căn → từ chối, phản ví dụ B, √(x−1)=x−3, √(x+1)=−2, √(x²−4)=0 (g = 0 được nhận đúng) đều đúng |
| Oracle vét cạn | **598 hệ: 0 ngoại lệ, 0 bỏ sót, 0 lệch tập** |
| Rubric | Đủ 5 mức; C3 đã bỏ phụ thuộc định dạng LaTeX; có kế hoạch cỡ mẫu và người chấm |

---

## 3. Các vấn đề còn lại

### 3.1. Báo cáo ghi sai nghiệm phức của √x = x² + 1 (mức: trung bình)

Bảng 3.1 ghi: "x ≈ 0.1607 ± 0.7686i". Mã v2.6 thực tế in bốn nghiệm của x⁴ + 2x² − x + 1 = 0:

≈ −0.3438 ± 1.3584i và ≈ 0.3438 ± 0.6254i.

Giá trị trong bảng không phải nghiệm của phương trình hệ quả. Cần sửa bảng theo kết quả chạy thật.

Lỗi hiển thị nhỏ cùng chỗ: dòng in `x = ≈ -0.3438 + -1.3584i` (có "= ≈" và "+ -"); nên định dạng dấu phần ảo và bỏ "x =" thừa.

### 3.2. Nhãn "Miền D_sign" sai khi g là hằng số (mức: trung bình)

`sp.solve(gx >= 0, x)` trả `[]` khi bất đẳng thức **luôn đúng** (g = 1/2, g = 0) và cũng trả `[]` khi **luôn sai** (g = −2). Chạy thực:

- √(x³−3x+1) = 1/2 (g = 1/2 ≥ 0 luôn đúng): in "Miền D_sign: []";
- √(x²−4) = 0 (g = 0 luôn đúng): in "Miền D_sign: []";
- √(x+1) = −2 (g = −2 luôn sai): in "Miền D_sign: []".

Học sinh đọc `[]` sẽ hiểu miền rỗng ở cả ba ca, trong khi hai ca đầu miền là toàn bộ ℝ. Đề xuất: xử lý riêng khi `gx` là hằng (in "luôn đúng với mọi x" hoặc "không có x nào thỏa") và định dạng lại kết quả của `sp.solve` thành khoảng.

### 3.3. Bước kết luận chưa khớp với nhánh "chưa xác định" (mức: trung bình)

Mã Bước 4:

```python
if valid_sols: ... "Tập nghiệm chính thức: S = {...}"
else:          ... "Phương trình vô nghiệm trên tập số thực ℝ (S = ∅)."
if indeterminate_sols: ... "CẢNH BÁO..."
```

Nếu `valid_sols` rỗng nhưng `indeterminate_sols` khác rỗng, hàm vẫn in **"vô nghiệm (S = ∅)"** rồi mới cảnh báo ở dòng sau. Kết luận và cảnh báo mâu thuẫn nhau. Tương tự, khi có cả nghiệm hợp lệ lẫn nghiệm chưa xác định, dòng "Tập nghiệm **chính thức**" dễ bị đọc là đầy đủ. Đề xuất: khi `indeterminate_sols` khác rỗng, kết luận phải là "Chưa kết luận được tập nghiệm đầy đủ" (kèm nghiệm đã xác nhận và nghiệm chưa xác định), không dùng "chính thức" hay "S = ∅".

Ngoài ra nhánh `unknown` **vẫn chưa có ca test nào** trong báo cáo (đợt 6 mục 3.4 đã đề nghị). Tôi không dựng được ca tự nhiên làm hai hàm dấu cùng thất bại, nên đề nghị tác giả thêm test bằng cách giả lập (ví dụ thay `real_status` hoặc `check_sign_exact` bằng bản luôn trả `None`) để kiểm chứng đường kết luận này.

### 3.4. Thông điệp liệt kê Diophantine tự mâu thuẫn (mức: trung bình)

Mã in `Liệt kê toàn bộ {len(int_sols)} bộ`, nhưng vòng in chỉ hiển thị `int_sols[:10]` rồi "... [còn N bộ nghiệm tiếp theo]". Chạy thực:

- x + z = 30, y = 1: in "**Liệt kê toàn bộ 29** bộ nghiệm", hiện 10 bộ, rồi "[còn 19 bộ…]";
- x + z = 10⁹, y = 1: in "hiển thị **1000** bộ nghiệm đầu tiên", nhưng chỉ hiện 10 bộ rồi "[còn 990…]". Nhãn LaTeX cũng ghi "hiển thị 1000 nghiệm".

Cần thống nhất: hoặc in đủ, hoặc ghi đúng "hiển thị 10 bộ đầu tiên trong tổng số N". Đây chính là loại sai lệch thông điệp mà đợt 6 mục 3.3 đã nêu, mới chỉ xử lý một nửa.

### 3.5. Nghiệm Cardano hiển thị nguyên biểu thức (mức: trung bình, sư phạm)

Với √(x³−3x+1) = 1/2, ba nghiệm thực được **nhận đúng** nhưng bước "NHẬN" và dòng "S = {…}" in ba biểu thức căn phức lồng dài hàng trăm ký tự, không có giá trị số. Phần rút gọn hiển thị mới chỉ áp dụng cho nghiệm **bị loại** là phức, chưa áp dụng cho nghiệm **được nhận**. Báo cáo ghi "≈ 0.2556, 1.5901, −1.8456" nhưng đầu ra giao diện không có các giá trị này. Đề xuất: khi biểu thức quá dài, hiển thị dạng "x ≈ 0.2556 (nghiệm thực của x³ − 3x + 3/4 = 0)" kèm giá trị gần đúng, cả ở bước NHẬN lẫn trong S.

---

## 4. Báo cáo lệch thực tế và ngôn ngữ

1. **"< 0.05 s" cho hệ x + z = 10⁹ không khớp đo thực.** Trên máy của tôi, ca này chạy ~0.4 s (1000 lần `simplify` trong vòng lặp thế ngược). Máy khác sẽ khác, nhưng cần ghi phương pháp đo (số lần lặp, máy, trung bình/trung vị) hoặc bỏ con số. Hai ô "< 0.05 s" của SymPy thuần và CAD Math Studio ở bảng 4.2 cũng chưa có phương pháp đo; ca căn thức đầu tiên của tôi chạy ~0.2 s.
2. **Tuyên bố "Hoạt động ngoại tuyến 100%", "Xử lý hoàn toàn cục bộ, không gửi dữ liệu ra ngoài", "Mã nguồn mở (MIT)":** tôi không có bằng chứng nào trong tài liệu (không thấy giấy phép, không thấy danh sách phụ thuộc, không thấy cấu hình mạng). Nên dẫn tới tệp LICENSE và nêu rõ điều kiện (ví dụ không bật tính năng gọi dịch vụ ngoài, nếu ứng dụng có).
3. **Bảng so sánh với Symbolab/Photomath** (thuê bao, 1–3 s, tải dữ liệu lên máy chủ): chưa có nguồn, ngày kiểm tra, gói dịch vụ. Tôi không kiểm chứng được phần này.
4. **Bộ test được nhắc nhưng không đính kèm:** tiêu đề ghi `run_batch_auto_test.py`, và dòng cuối ghi "xác thực tự động bởi bộ kiểm thử STEM Core". Không có mã test hay log chạy. Các test của tôi ở trên là độc lập; nên đính kèm test của tác giả (kèm lệnh chạy, phiên bản SymPy, kết quả) và thêm các ca của đợt 6 (√(x³−3x+1)=1/2, D_sign hằng, nhánh `unknown`).
5. **Cụm tuyệt đối còn sót**, dù dòng 7 của bảng tiếp thu ghi đã "rà soát và thay thế toàn bộ". Đếm trong văn bản: "dứt điểm" ×3 (kể cả "Khắc phục dứt điểm" ở bảng 3.1 và 3.2), "triệt để" ×2 (kể cả "Loại bỏ triệt để" ở mục 0), "100%" ×3 ("khớp 100%", "ngoại tuyến 100%"), "Đồng bộ hoàn toàn", "Báo cáo đạt chuẩn mực phản biện học thuật nghiêm túc" (tự khen), "Rubric hoàn thiện, sẵn sàng…", "xác thực tự động". Gợi ý: nói cụ thể "đã sửa … ; còn hạn chế …", bỏ các lời tự đánh giá.
6. **Mô tả "7 trạng thái cấu trúc"** (docstring) và "Phân định rõ 7 trạng thái" nay khớp với mã. Phần này ổn.

---

## 5. Rubric và kế hoạch thực nghiệm

**Cải thiện đáng ghi nhận:** đủ 5 mức cho 4 tiêu chí, C3 không còn phụ thuộc định dạng, có cỡ mẫu 30 bài với tỉ lệ nêu rõ (có cả bài ngoài phạm vi), 5 giáo viên, mục tiêu độ tin cậy.

**Còn hạn chế:**

1. **Fleiss' kappa chưa phù hợp.** Fleiss' κ coi các mức là danh nghĩa (nominal), không tính đến việc lệch 1 mức nhẹ hơn lệch 3 mức. Thang 1–5 là thang thứ tự; nên dùng **Krippendorff's α (ordinal)** hoặc **ICC**, hoặc kappa trọng số. Ngưỡng "κ ≥ 0.70" cần dẫn nguồn (thang diễn giải thường dùng).
2. **Chấm mù khó thành công như mô tả.** "Chuẩn hóa văn bản đồng nhất" không che được việc SymPy thuần **không có lời giải từng bước**, còn CAD Math Studio xuất tiếng Việt, các dịch vụ khác tiếng Anh. Người chấm có thể nhận ra công cụ chỉ qua ngôn ngữ và độ dài. Cần: dịch/viết lại về cùng ngôn ngữ, cùng khuôn trình bày, và **kiểm tra tính mù** (hỏi người chấm đoán công cụ, báo cáo tỉ lệ đoán đúng).
3. **Thiếu tiêu chí "phù hợp trình độ học sinh"** (đợt 4 đã nêu; chưa thêm, chưa giải thích lý do bỏ).
4. **SymPy thuần** cho sẵn 0 bước giải thích; đưa vào chấm sư phạm cạnh tranh sẽ luôn thấp. Nên nói rõ vai trò (mốc cơ sở, không phải đối thủ cạnh tranh), hoặc ghi "không áp dụng" cho C2–C4.
5. Chưa nêu quy trình khi người chấm bất đồng lớn (chấm lại, thảo luận), chưa nêu cách công bố dữ liệu thô.
6. Tên "double-blind" đã bỏ, nay dùng "blind review". Đó là cách gọi chính xác hơn.

---

## 6. Việc cần làm trước khi nộp (theo thứ tự ưu tiên)

| # | Việc | Mức |
|---|---|---|
| 1 | Sửa bảng 3.1: nghiệm phức của √x = x²+1 theo kết quả chạy; sửa định dạng "= ≈", "+ -" | Trung bình |
| 2 | Xử lý `Miền D_sign` khi g hằng (luôn đúng/luôn sai) | Trung bình |
| 3 | Sửa Bước 4: không in "S = ∅" / "chính thức" khi còn nghiệm chưa xác định; thêm test giả lập nhánh `unknown` | Trung bình |
| 4 | Thống nhất thông điệp liệt kê (đủ hay "10 đầu tiên trong tổng N") và nhãn LaTeX | Trung bình |
| 5 | Hiển thị giá trị gần đúng cho nghiệm Cardano ở bước NHẬN và trong S | Trung bình |
| 6 | Đính kèm bộ test và log chạy; bỏ câu "xác thực tự động" nếu không có | Trung bình |
| 7 | Bỏ hoặc chứng minh các con số "< 0.05 s", "100% ngoại tuyến", "MIT"; nguồn cho bảng Symbolab/Photomath | Trung bình |
| 8 | Rà lại toàn văn bỏ cụm tuyệt đối còn sót (mục 4.5) | Trung bình |
| 9 | Rubric: đổi Fleiss' κ sang Krippendorff's α hoặc ICC; kế hoạch kiểm tra tính mù; thêm tiêu chí trình độ | Thấp–TB |

---

## 7. Kết luận

Hai hàm đã đạt mức đáng tin cho phạm vi đã nêu: không còn lỗi về **đáp số** nào mà tôi tìm được, kể cả sau 598 hệ ngẫu nhiên và các ca biên căn thức. Những điểm còn lại tập trung vào **chất lượng hiển thị và độ khớp giữa báo cáo với kết quả chạy**: một số liệu sai trong bảng, vài thông điệp tự mâu thuẫn, nhãn `[]` gây hiểu nhầm, và các tuyên bố vận hành chưa có bằng chứng đi kèm. Đây đều là điểm sửa nhanh. Khung Rubric đã tiến bộ rõ, cần thêm chỉ số đồng thuận phù hợp và kế hoạch kiểm tra tính mù trước khi dùng làm bằng chứng.

---

*Phản biện này dựa trên việc trích và chạy thật hai hàm trong báo cáo v2.6 (SymPy 1.14.0, giao diện được thay bằng đối tượng giả) và oracle vét cạn nêu ở mục 0. Không kiểm chứng các phát biểu về dịch vụ thương mại, giấy phép và bộ test của tác giả. Đây là tham vấn kỹ thuật bằng công cụ AI, không thay thế thẩm định bởi người thật.*
