# Phản biện đợt 9: thẩm định báo cáo v2.8 (08/11/2026)

**Đối tượng:** `BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_8.md`: hai hàm lõi (khối mã thụt lề cấp module), bộ test `run_batch_auto_test.py` viết lại, nhật ký chạy, Rubric, bảng đặc tính kỹ thuật.

---

## 0. Phạm vi và cách làm

- **Mã lõi:** trích tự động khối mã từ file v2.8 và chạy với SymPy 1.14.0 (giao diện thay bằng đối tượng giả).
- **Bộ test đính kèm:** bộ test mới import `cad_math_v2.cad_math_v2.CADMathDesktopAppV2`, tệp mà tôi không có. Tôi dựng một gói giả `cad_math_v2/cad_math_v2.py` chứa đúng hai hàm trong báo cáo (gắn vào lớp `CADMathDesktopAppV2`) rồi chạy bộ test **nguyên văn**.
- **Kiểm thử đột biến (mutation):** cấy từng lỗi vào mã lõi và chạy lại bộ test để xem bộ test có phát hiện không.
- **Oracle độc lập** cho Diophantine: 699 hệ ngẫu nhiên (2 phương trình, 3 ẩn, một tham số tự do, luôn có nghiệm nguyên dương ban đầu), đối chiếu số nghiệm và phân loại với bộ liệt kê tham số k ∈ [−3000, 3000] không dùng CRT.
- Các ca đợt 7–8: D_sign hằng, giả lập nhánh `unknown`, định dạng S, thông điệp liệt kê 10/29/10⁹ nghiệm.

**Chưa làm được:** không thấy tệp `cad_math_v2.py` thật, giao diện, `clean_display_expr`, `LICENSE`. Số đo thời gian của tôi không so sánh được với máy của tác giả.

---

## 1. Kết luận

**Các vấn đề lớn của đợt 8 đã được xử lý.** Bộ test nay gọi hàm thật, khối mã chạy được nguyên văn, vòng quét 10⁹ nghiệm đã nhanh, định dạng S đã đổi. Mã lõi vẫn đúng trên mọi ca tôi thử. Phần còn lại là **độ mạnh của bộ test**, **một số số liệu và câu chữ chưa nhất quán**, và **kế hoạch thực nghiệm chưa hoàn chỉnh**. Không điểm nào làm sai đáp số.

| Mức | Vấn đề | Mục |
|---|---|---|
| Trung bình | Bộ test bắt được 3/4 lỗi cấy; nhánh `unknown` không được kiểm; docstring hứa bất biến mà mã chưa kiểm; so khớp chuỗi dễ sai | 3.1 |
| Trung bình | Số liệu thời gian chưa nhất quán với log; ô đối chiếu SymPy/Symbolab/Photomath và giấy phép vẫn chưa có nguồn | 3.2 |
| Thấp–TB | Kế hoạch thực nghiệm: α tính sau thảo luận, người biên tập, đăng ký trước, bài ngoài phạm vi | 3.3 |
| Thấp | Còn cụm tự đánh giá; dòng cuối "xác thực" | 3.4 |
| Thấp | Chi tiết nhỏ (nhãn "tiệm cận", ngưỡng hiển thị) | 3.5 |

---

## 2. Điểm đã sửa đúng (xác nhận bằng chạy)

| Hạng mục | Kết quả |
|---|---|
| Bộ test gọi hàm thật | Bộ test mới gọi `app.solve_radical_pedagogical` và `app.solve_underdetermined_or_diophantine`. Chạy nguyên văn trên gói giả: **12/12 đạt, exit code 0**. Log trong báo cáo khớp kết quả của tôi (khác nhau chỉ ở thời gian, do máy) |
| Thụt lề khối mã | Khối mã parse được nguyên văn; bọc vào lớp là chạy |
| Tối ưu trần 10⁹ | Ca x + z = 10⁹, y = 1 chạy ở mức vài ms trên máy của tôi (trước ~0.46 s); báo "tổng cộng 999999999 bộ nghiệm", hiển thị 10 bộ đầu |
| Trùng lặp thông điệp | Hết lặp dòng "tổng cộng n bộ"; bước liệt kê và bước kết luận có nội dung khác nhau |
| Định dạng S | In `S gồm 3 nghiệm thực, giá trị gần đúng: S ≈ {0.2556, 1.5901, -1.8456}` |
| Các ca cũ | D_sign hằng (g = 1/2, 0, −2) đúng; giả lập `unknown` cho "CHƯA THỂ KẾT LUẬN" (không in "S = ∅"); √x = x²+1, hai căn, Trăm trâu, `SYS_DIO_03`, phản ví dụ A, B, d ≥ 2 đều đúng |
| Oracle độc lập | **699 hệ** (491 hữu hạn, 208 vô hạn): 0 ngoại lệ, 0 bỏ sót, 0 sai số lượng/phân loại |
| Giới hạn nêu rõ | Mục 6.3 đã thừa nhận nhánh `indeterminate_sols` mới được kiểm bằng giả lập |
| Rubric | Chọn Krippendorff's α (ordinal) làm chỉ số chính, ICC(2,1) là phụ, có CI 95% cho kiểm tra tính mù, có người biên tập độc lập, quy tắc xử lý bất đồng |

---

## 3. Các vấn đề còn lại

### 3.1. Độ mạnh của bộ test (mức: trung bình)

**Kết quả kiểm thử đột biến** (cấy lỗi vào mã lõi, chạy lại bộ test):

| Lỗi cấy | Bộ test |
|---|---|
| Tái hiện lỗi v2.5 (`not r.is_real` loại nhầm nghiệm thực) | **Phát hiện** (RAD_04 sai: valid 0/3) |
| Không loại nghiệm có g < 0 | **Phát hiện** (RAD_01, 02, 03 sai) |
| Bỏ kiểm tra gcd/đồng dư (nhận nhầm hệ vô nghiệm nguyên) | **Phát hiện** (DIO_04 sai) |
| Nghiệm ở nhánh `unknown` bị tự nhận vào `valid` | **Không phát hiện** (vẫn 12/12) |

Bộ test bắt được ba trong bốn lỗi, và lỗi bị sót chính là điểm yếu mà báo cáo đã thừa nhận (nhánh `unknown` chưa có ca nào). Đây là lỗi **nguy hiểm nhất về mặt sư phạm** (nhận nghiệm khi không chắc), nên cần có test.

Các hạn chế khác:

1. **Docstring hứa nhiều hơn mã kiểm.** Docstring nêu bốn bất biến, nhưng:
   - bất biến 2 ("mọi nghiệm bị loại đều vi phạm điều kiện") **chưa được kiểm**: mã chỉ đếm số nghiệm bị loại;
   - bất biến 3 ("mọi bộ nghiệm Diophantine thỏa hệ ban đầu và thuộc (ℤ⁺)ⁿ") **chưa được kiểm**: các ca Diophantine chỉ so khớp chuỗi trong văn bản đầu ra;
   - bất biến 1 chỉ kiểm nghiệm được nhận có thỏa phương trình gốc, không kiểm có bỏ sót nghiệm (ngoài so số lượng).
2. **So khớp chuỗi dễ sai.**
   - `f"{n} bộ nghiệm" in out_text` với n = 3 cũng khớp "13 bộ nghiệm" hoặc "23 bộ nghiệm".
   - Kiểm tra `INFEASIBLE_NO_INTEGER_POINTS` chứa nhánh `... or "Hệ không có nghiệm nguyên dương" in out_text`. Chuỗi này cũng xuất hiện ở kết luận của trạng thái `INFEASIBLE_BOUNDS_EMPTY`, nên bộ test không phân biệt được hai trạng thái.
3. **Phạm vi:** 12 ca đều là các ca lịch sử. Chưa có ca cho `INFEASIBLE_BOUNDS_EMPTY`, d = 0, hệ đồng dư mô-đun không nguyên tố cùng nhau, ranh giới 10/11 nghiệm của thông điệp liệt kê, D_sign hằng, định dạng S, và không có kiểm tra ngẫu nhiên đối chiếu oracle.

**Đề xuất:**

- Cho hàm Diophantine trả thêm một mã trạng thái (ví dụ chuỗi `category`) và hàm căn thức trả cấu trúc dữ liệu, để test kiểm trực tiếp thay cho so khớp chuỗi.
- Thêm kiểm tra bất biến 2 và 3 đúng như docstring.
- Thêm test cho `unknown` bằng cách thay `check_sign_exact` hoặc `real_status` bằng bản luôn trả giá trị bất định (như tôi đã làm).
- Đưa bộ oracle ngẫu nhiên vào kho mã (kèm seed và phiên bản SymPy); đây là cách kiểm tra mạnh nhất cho công thức đếm số nghiệm n_total.

*Lưu ý thiết kế:* sau tối ưu, bước thế ngược chỉ chạy trên tối đa 10 bộ hiển thị, còn `n_total` đến từ công thức đồng dư. Công thức này khớp trên 699 hệ của oracle, nhưng không còn được kiểm bằng chính vòng lặp; vì vậy oracle trong bộ test càng cần thiết.

### 3.2. Số liệu thời gian, nguồn và giấy phép (mức: trung bình)

1. **Khoảng thời gian chưa khớp log.** Bảng tiếp thu (dòng 3) ghi "1.4 – 862 ms"; log có ca nhanh nhất RAD_06 là **0.11 ms**, còn 1.41 ms là ca DIO_06. Bảng 5 ghi "0.01 – 0.86 s", trong khi log thấp nhất là 0.0001 s. Nên ghi đúng dải của log, hoặc dùng trung vị theo nhóm bài.
2. **Đại lượng được đo** là thời gian tính toán lõi của từng bài (không gồm giao diện, vẽ LaTeX) và lần chạy đầu gồm cả khởi động SymPy. Bảng nên ghi nhãn "thời gian tính toán lõi, trung vị n lần" thay cho "thời gian phản hồi".
3. **Chưa xử lý từ đợt 8:** các ô "SymPy 0.05–0.20 s" và "Symbolab/Photomath 1.0–3.0 s" vẫn không có phương pháp đo hay nguồn; "bắt buộc kết nối Internet liên tục" và "đăng ký thuê bao trả phí" vẫn không có nguồn, ngày kiểm tra, gói dịch vụ (nhiều dịch vụ có bậc miễn phí). Tôi không kiểm chứng được các phát biểu này.
4. **Giấy phép:** ghi "đường dẫn: `LICENSE`" vẫn chỉ là tên tệp; chưa có URL kho mã hay nội dung giấy phép.
5. **Cấu hình máy:** báo cáo nêu rõ "Intel Core i7-11800H". Chỉ cần bảo đảm đây đúng là máy đo thực tế; tôi không kiểm chứng được.

### 3.3. Kế hoạch thực nghiệm sư phạm (mức: thấp–trung bình)

Phần này tiến bộ rõ so với v2.7. Còn lại:

1. **Hệ số α có thể bị thổi phồng:** quy trình ghi chỗ bất đồng sẽ được "thảo luận đồng thuận trước khi chốt điểm". Nếu α tính **sau** thảo luận thì đồng thuận bị phóng đại. Nên tính α và ICC trên **điểm độc lập vòng 1**, chỉ dùng điểm sau thảo luận cho phân tích điểm số cuối.
2. **Một giáo viên biên tập bốn bộ lời giải:** nên có người thứ hai đối chiếu, lưu bản gốc và nhật ký thay đổi, kèm quy tắc "không đổi nội dung và thứ tự bước", để phép chuẩn hóa không vô tình làm tăng hay giảm chất lượng của một công cụ.
3. **Kiểm tra tính mù:** CI 95% chứa 25% không chứng minh người chấm đã bị che mù. Nên nêu trước cách diễn giải (ví dụ ngưỡng tỉ lệ đoán đúng) và ghi nhận 5×30 dự đoán không độc lập hoàn toàn.
4. **Chưa có** (đã nêu ở đợt 8): giả thuyết chính và phép so sánh chính đăng ký trước, cách xử lý bài ngoài phạm vi khi công cụ từ chối (có tính điểm không), sự đồng ý của giáo viên tham gia, kế hoạch công bố dữ liệu thô.
5. **C5:** mức 3 ("thuật ngữ chuyên sâu") vẫn khó chấm thống nhất; nên liệt kê thuật ngữ nằm ngoài chương trình để người chấm đối chiếu.

### 3.4. Câu chữ còn lại (mức: thấp)

Dòng 7 của bảng tiếp thu nói đã thay các cụm tự khen bằng mô tả sự việc, nhưng phần tiếp thu còn: "Phương pháp luận thực nghiệm **chặt chẽ**" (dòng 8), "Ký hiệu toán học **chuẩn mực** sư phạm" (dòng 5), "Báo cáo **minh bạch, nhất quán**" (dòng 3), "Văn bản **mạch lạc**" (dòng 6), "cải tiến **căn bản**", "tiếp thu **nghiêm túc**". Cột "Kết quả kiểm chứng" nên ghi kết quả (số liệu, tên ca) thay vì nhận xét chất lượng.

Dòng cuối "hoàn thiện và **xác thực** bởi bộ kiểm thử STEM Core" vẫn quá mạnh so với 12 ca và các kiểm tra chuỗi nêu ở 3.1. Gợi ý: "đã chạy bộ kiểm thử gồm 12 ca (mục 3), kết quả 12/12".

### 3.5. Chi tiết nhỏ (mức: thấp)

- Thông điệp "Dấu biểu thức **tiệm cận** ngưỡng bất định" vẫn còn (đã nêu ở đợt 8, mục 3.4). Gợi ý: "chưa xác định được dấu bằng phương pháp đại số hay số học độ chính xác cao".
- Từ khi chỉ hiển thị 10 bộ, các hệ có 11–vài chục nghiệm không còn được liệt kê đầy đủ ở nhãn LaTeX (trước đây có). Đây là lựa chọn thiết kế; có thể cho người dùng chọn ngưỡng hiển thị.
- Bước kết luận căn thức vẫn dùng chữ "Tập nghiệm chính thức" khi không còn nghiệm chưa xác định; chấp nhận được, nhưng chữ "chính thức" không mang thêm thông tin.

---

## 4. Việc cần làm trước khi nộp (theo thứ tự ưu tiên)

| # | Việc | Mức |
|---|---|---|
| 1 | Thêm test cho nhánh `unknown` (giả lập), kiểm bất biến 2 và 3, kiểm trạng thái bằng mã thay cho chuỗi (3.1) | Trung bình |
| 2 | Đưa oracle ngẫu nhiên vào bộ test; thêm ca cho các trạng thái chưa phủ (3.1) | Trung bình |
| 3 | Sửa khoảng thời gian cho khớp log; ghi rõ đại lượng và phương pháp đo (3.2) | Trung bình |
| 4 | Nguồn cho ô SymPy/Symbolab/Photomath; đường dẫn giấy phép (3.2) | Trung bình |
| 5 | Chỉnh kế hoạch thực nghiệm: α vòng 1, người biên tập thứ hai, đăng ký trước, bài ngoài phạm vi (3.3) | Thấp–TB |
| 6 | Gỡ các cụm tự đánh giá; sửa dòng cuối (3.4) | Thấp |
| 7 | Sửa nhãn "tiệm cận" và cân nhắc ngưỡng hiển thị (3.5) | Thấp |

---

## 5. Kết luận

Hai hàm lõi cho kết quả đúng và hiển thị rõ trên mọi ca tôi thử, và bộ test nay thật sự gọi mã chính, bắt được ba trong bốn lỗi tôi cấy vào. Điểm yếu còn lại là **độ mạnh của bộ test** (nhánh `unknown`, bất biến chưa kiểm, so khớp chuỗi) và **độ nhất quán của số liệu mô tả**. Sau các chỉnh sửa trên, phần kỹ thuật có thể xem là sẵn sàng để chuyển sang giai đoạn thực nghiệm sư phạm, với điều kiện hoàn thiện kế hoạch ở mục 3.3.

---

*Phản biện này dựa trên việc trích và chạy thật mã trong báo cáo v2.8 (SymPy 1.14.0, gói `CADMathDesktopAppV2` do tôi dựng lại từ hai hàm trong báo cáo), chạy bộ test đính kèm nguyên văn, kiểm thử đột biến và oracle nêu ở mục 0. Không kiểm chứng các phát biểu về dịch vụ thương mại, giấy phép và cấu hình máy của tác giả. Đây là tham vấn kỹ thuật bằng công cụ AI, không thay thế thẩm định bởi người thật.*
