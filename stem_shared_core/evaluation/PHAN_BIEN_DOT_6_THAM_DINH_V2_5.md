# Phản biện đợt 6: thẩm định báo cáo v2.5 (08/11/2026)

**Đối tượng:** `BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_5.md`, gồm hai hàm `solve_radical_pedagogical`, `solve_underdetermined_or_diophantine`, các bảng kiểm thử và khung Rubric dự thảo.

---

## 0. Phạm vi và cách làm

Khác đợt 4, lần này **mã được chạy thật**. Tôi trích tự động hai khối mã Python từ chính file v2.5, chạy với SymPy 1.14.0 (bọc `self` và các đối tượng giao diện bằng đối tượng giả để ghi lại đầu ra), rồi:

- chạy lại toàn bộ bộ test căn thức và Diophantine trong báo cáo, cộng thêm các ca tôi tự chọn;
- đối chiếu hàm Diophantine với **oracle vét cạn**: 398 hệ ngẫu nhiên (2 phương trình, 3 ẩn, đúng một tham số tự do, hệ số trong [−6, 6]), so tập nghiệm trong hộp 1..40.

**Chưa làm được:** chỉ thấy hai hàm, không thấy nơi gọi, `clean_display_expr`, giao diện, và không thấy bộ test tự động mà báo cáo nói đã đạt 100%. Các nhận xét về nơi gọi là suy luận.

---

## 1. Kết luận

Báo cáo v2.5 là **một bước tiến thật**: hầu hết lỗi đợt 4 và đợt 5 đã được sửa đúng, và tôi xác nhận bằng chạy mã. Tuy vậy **chưa nên nộp**, vì còn một lỗi hồi quy nghiêm trọng do chính bản sửa gây ra, một số liệu sai trong bảng kiểm thử, và một kết luận sai khi chạm trần.

| Mức | Vấn đề | Mục |
|---|---|---|
| Cao | Bộ lọc nghiệm phức mới **loại nhầm nghiệm thực** (ví dụ ba nghiệm thực bị in là "nghiệm phức", kết luận sai) | 3.1 |
| Cao | Bảng 3.2 ghi nghiệm bài "Trăm trâu trăm cỏ" **không thỏa hệ đã nêu** | 3.2 |
| Trung bình | Chạm trần 1000 vẫn in "liệt kê toàn bộ" và "Tập nghiệm S = {…}" | 3.3 |
| Trung bình | Hàm căn thức không trả về tập `rejected`/`indeterminate`; báo cáo nói có bước kết luận mà mã dán không có | 3.4 |
| Trung bình | Nhãn họ nghiệm "k ∈ ℤ" thiếu cận; nhãn "vô số nghiệm" cho d ≥ 2 sai trên ℤ⁺ | 3.5, 3.6 |
| Trung bình | Văn bản còn nhiều cụm tuyệt đối, **mâu thuẫn với chính mục 7 của bảng tiếp thu** | 4 |
| Trung bình | Mô tả báo cáo lệch mã (số trạng thái, tên nhãn, "x ≡ 1 mod 1") | 3.7 |
| Thấp–TB | Rubric còn hạn chế (neo điểm, C3, thiếu bộ bài) và bảng 4.2 thiếu nguồn | 5 |

---

## 2. Những điểm đã sửa đúng (xác nhận bằng chạy mã)

| Hạng mục | Kết quả chạy thực |
|---|---|
| Nhận dạng dạng phương trình | x−1 = √(2x−1) và 2√(2x−1) = x−1 cho đúng g(x), đúng nghiệm: nhận 2+√2, 5+2√5; loại 2−√2, 5−2√5; hiển thị g(r) bằng số |
| Nghiệm phức của √x = x²+1 | Không nhận nghiệm nào, 4 nghiệm phức bị loại (xem thêm 3.1 về hệ quả phụ) |
| Từ chối hai căn | √x + √(x+1) = 2 → "Ngoài phạm vi hỗ trợ", không in lời giải |
| Phản ví dụ A (251x − z = −5, y = 2) | `UNBOUNDED_INFINITE`; nghiệm nhỏ nhất (1, 2, 256), kế tiếp (2, 2, 507), (3, 2, 758) |
| Phản ví dụ B (2x − 2z = 1, y = 5) | Phân biệt được "vô nghiệm nguyên" với "vô hạn nghiệm" |
| Biến hằng ≤ 0 | x = z − 5, y = 0 → miền rỗng |
| d ≥ 2 | Có thông báo tường minh, không im lặng |
| CRT với mô-đun không nguyên tố cùng nhau | z/4 và (z−2)/6 → z ≡ 8 (mod 12), nghiệm (2,1,8), (5,3,20), (8,5,32); đúng |
| **Oracle vét cạn** | 398 hệ, **0 ngoại lệ, 0 bỏ sót, 0 lệch tập** |
| Câu chữ bước 1 | Đã sửa đúng: "vì √f ≥ 0 nên g ≥ 0" |
| Rubric | Đã đổi nhãn thành dự thảo, tách bảng đặc tính kỹ thuật |

Phần Diophantine nhìn chung vững. Đây là phần sửa tốt nhất của v2.5.

---

## 3. Các vấn đề còn lại

### 3.1. Lỗi hồi quy: nghiệm thực bị loại như nghiệm phức (mức: cao)

Mã v2.5:

```python
if not r.is_real or abs(complex(r.evalf()).imag) > 1e-25:
    rejected_sols.append(r) ...   # "Nghiệm phức không thuộc tập số thực ℝ"
```

Hai điều kiện đều sai với nghiệm thực viết bằng căn phức (trường hợp bất khả quy của phương trình bậc ba, SymPy xuất dạng có `I`):

- `r.is_real` là `None` (không phải `False`), và `not None` là `True`, nên bị loại;
- `evalf()` chỉ 15 chữ số nên phần ảo còn nhiễu cỡ 1e-16, lớn hơn ngưỡng 1e-25.

**Chạy thực:** √(x³ − 3x + 1) = 1/2. Phương trình hệ quả x³ − 3x + 3/4 = 0 có **ba nghiệm thực** (≈ 0.2556; 1.5901; −1.8456), đều thỏa g = 1/2 > 0. Mã v2.5 in cả ba là "LOẠI (Nghiệm phức…)", `valid = []`, tức kết luận phương trình vô nghiệm, **sai**.

Báo cáo (bảng mục 1, dòng 2) mô tả bộ lọc là `r.is_real is False` hoặc `abs(im) > 1e-25`, **không khớp với mã dán** ở điều kiện đầu. Đây cũng là một ví dụ cho thấy "kiểm thử tự động đạt 100%" chưa phủ ca này.

**Bản vá đã chạy thử:**

```python
def real_status(r):
    """True / False / None (chưa kết luận)."""
    if r.is_real is True:  return True
    if r.is_real is False: return False
    a = sp.N(r, 60)
    im = abs(sp.im(a))
    if im < sp.Float('1e-45'): return True
    if im > sp.Float('1e-20'): return False
    return None

# trong vòng lặp:
st = real_status(r)
if st is False:   # loại: nghiệm phức
    ...
elif st is None:  # chưa xác định, KHÔNG nhận, KHÔNG loại
    ...
```

Kết quả sau vá: √(x³−3x+1)=1/2 → nhận 3 nghiệm thực (đúng); √x = x²+1 → không nhận nghiệm nào; hai ca có hệ số căn và đảo vế → kết quả như cũ (đúng).

**Lưu ý phụ:** với √x = x²+1, phần giải thích hiển thị cả bốn nghiệm phức dưới dạng biểu thức căn lồng dài hàng trăm ký tự. Với học sinh nên rút gọn thành "phương trình hệ quả có 4 nghiệm phức, không có nghiệm thực" thay vì in từng biểu thức.

### 3.2. Số liệu sai trong bảng 3.2: bài "Trăm trâu trăm cỏ" (mức: cao về tính nhất quán)

Báo cáo ghi hệ x + y + z = 100, 5x + 3y + z/3 = 100 và hai nghiệm (6, 20, 74), (13, 10, 77). **Hai bộ này không thỏa hệ đã nêu:** với (6, 20, 74), 5·6 + 3·20 + 74/3 = 344/3 ≠ 100; với (13, 10, 77) được 362/3 ≠ 100.

Vét cạn và chính mã v2.5 đều cho **ba** nghiệm: **(4, 18, 78), (8, 11, 81), (12, 4, 84)**. Mã đúng, bảng báo cáo sai (có vẻ lấy kết quả của một hệ khác từ các đợt trước). Cần sửa bảng; nếu hai nghiệm kia thuộc hệ khác thì ghi rõ hệ đó.

### 3.3. Chạm trần vẫn kết luận như đã liệt kê đủ (mức: trung bình)

Hệ x + z = 10⁹, y = 1: miền z ∈ [1, 10⁹] có 999 999 999 nghiệm. Mã quét 1000 bước rồi in "Cảnh báo trần", nhưng ngay sau đó in **"Liệt kê toàn bộ 1000 bộ nghiệm"** và **"Tập nghiệm nguyên dương hữu hạn: S = {…}"** (kèm vẽ LaTeX 1000 bộ). Cảnh báo bị chính các dòng sau phủ định. Đề xuất:

- khi chạm trần: không in "toàn bộ", không in `S = {…}`;
- tính số nghiệm thật trực tiếp, `n = (hi − start)//M + 1`, và in "có n nghiệm, hiển thị 1000 đầu tiên";
- hoặc xuất họ tham số `p = p0 + M·k, 0 ≤ k ≤ K` thay cho liệt kê.

### 3.4. Hàm căn thức: ba tập chưa thực sự được tách ở đầu ra (mức: trung bình)

Hàm khai báo `rejected_sols`, `indeterminate_sols` nhưng chỉ `return steps, valid_sols`. Hệ quả:

- Nơi gọi không biết có nghiệm "chưa xác định" nào. Nếu nơi gọi kết luận "S = valid_sols", nghiệm chưa xác định **biến mất khỏi kết luận** mà không có cảnh báo nổi bật (chỉ nằm lẻ trong các dòng bước).
- Báo cáo ghi với √x = x²+1 "kết luận chính xác S = ∅", nhưng trong mã dán **không có bước kết luận nào**. Nếu bước đó nằm ở nơi gọi thì cần dán; nếu chưa có thì cần thêm.
- Nhánh `unknown` vẫn **chưa có ca test nào** trong báo cáo (phần 5, mục 3 chỉ mô tả bằng lời). Cần một ca cụ thể, ví dụ nghiệm lồng căn mà g(r) = 0 đúng nhưng SymPy không tự rút gọn.

Đề xuất: trả về `(steps, valid, rejected, indeterminate)` hoặc dict; bước kết luận phải nêu riêng số nghiệm chưa xác định ("Chưa kết luận được x = …").

### 3.5. Nhãn họ nghiệm "k ∈ ℤ" thiếu cận (mức: trung bình)

Ở nhánh vô hạn, mã in `z = 5 + 251·k (k ∈ ℤ)`. Với k = 0 được z = 5, x = 0 (không dương); với k âm càng sai. Nghiệm nguyên dương cần k ≥ k_start (ở ca A là k ≥ 1). Với học sinh, câu này dạy sai. Cần in rõ "với k nguyên, k ≥ 1" hoặc viết lại họ nghiệm theo k bắt đầu từ 0 như bản tôi đã thử: (k+1, 2, 251k+256), k ≥ 0.

### 3.6. Nhãn "vô số nghiệm" cho d ≥ 2 (mức: trung bình–thấp)

Với x + y + z = 10, nhãn LaTeX xuất "Vô số nghiệm phụ thuộc 2 tham số". Trên ℝ thì đúng, nhưng đề bài là nghiệm **nguyên dương**, nơi hệ này có đúng **36** nghiệm. Học sinh đọc "vô số" sẽ hiểu sai. Cần ghi "trên ℝ" và nói rõ chưa khảo sát ℤ⁺. Gợi ý nâng cấp: khi mọi biến bị chặn (hệ số cùng dấu) có thể vét cạn có trần như nhánh d = 1.

### 3.7. Báo cáo lệch mã ở các chi tiết

| Báo cáo ghi | Thực tế |
|---|---|
| "phân định 4 trạng thái cấu trúc" | Mã có ít nhất 7 trạng thái/nhánh: vô nghiệm thực, d = 0, d ≥ 2, `INFEASIBLE_BOUNDS_EMPTY`, `INFEASIBLE_NO_INTEGER_POINTS`, `FINITE_BOUNDED`, `UNBOUNDED_INFINITE` |
| Nhãn `EMPTY_NO_INTEGER` (dòng 4 bảng 1) và `INFEASIBLE_NO_INTEGER_POINTS` (bảng 3.2) | Hai tên khác nhau cho cùng trạng thái; mã dùng tên thứ hai |
| "tìm được x ≡ 1 (mod 1)" cho ca A | Vô nghĩa: mã in z ≡ 5 (mod 251) |
| "O(1)" | Còn các lệnh `simplify` mỗi bước; nên bỏ cụm này hoặc nói rõ đo cái gì |
| "Phân ví dụ B" | Lỗi chính tả ("Phản ví dụ B") |
| Bảng v2.4, dòng "x−1 = √(2x−1)… in bước giải sai" | Đúng với kết quả đợt 5; không có vấn đề |

---

## 4. Ngôn ngữ tuyệt đối còn sót (mâu thuẫn với dòng 7 của bảng tiếp thu)

Dòng 7 của bảng mục 1 khẳng định đã "thay thế toàn bộ" ngôn ngữ khẳng định mạnh. Thực tế văn bản còn:

- "hoàn toàn tiếp thu", "văn bản mới hoàn toàn", "Tiếp thu triệt để", "kiểm thử tự động đạt 100%";
- "Giải quyết dứt điểm" (hai chỗ), "Khắc phục dứt điểm";
- "Đạt chuẩn mực liêm chính học thuật" (tự khen trong bảng);
- "tuân thủ nguyên tắc an toàn sư phạm tối đa", "xử lý an toàn 100%", "Cực nhanh";
- chú thích trong mã "loại bỏ triệt để nghiệm phức", đúng là câu bị lỗi ở 3.1;
- dòng cuối "xác thực tự động bởi môi trường kiểm thử STEM Core" khi **không đính kèm bộ test hay log chạy**.

Gợi ý: nói cụ thể "đã sửa các điểm X, Y, Z; còn hạn chế A, B", và đính kèm bộ test + log chạy (lệnh, phiên bản SymPy, kết quả) thay cho câu "100%".

---

## 5. Rubric và bảng đặc tính kỹ thuật

**Cải thiện đáng ghi nhận:** đã đổi nhãn thành dự thảo, thừa nhận điểm cũ không có giá trị chứng minh, tách bảng vận hành riêng, có neo điểm.

**Còn hạn chế:**

1. Neo điểm chỉ ở mức 1, 3, 5; chưa định nghĩa mức 2 và 4, người chấm sẽ chấm lệch nhau ở đúng những mức này.
2. **C3** ("công thức 2D chuẩn LaTeX") là tính năng giao diện. Ghi chú nói sẽ "định dạng đồng nhất" lời giải trước khi chấm mù, nên C3 và cách chấm mù **mâu thuẫn nhau**: sau khi chuẩn hóa định dạng thì không còn gì để phân biệt ở C3.
3. Mức 5 của C3 và C4 mô tả gần như đúng đầu ra hiện tại của công cụ (bẫy bình phương hai vế, giá trị g(r) < 0). Thiên lệch cấu trúc đã giảm nhưng chưa hết; nên viết neo theo hành vi sư phạm mong muốn, không theo định dạng đầu ra.
4. Chưa có bộ bài: bao nhiêu bài, chọn từ đâu (SGK, đề thi), phân bố độ khó, có cả bài **không có nghiệm ngoại lai** (kiểm tra công cụ khác không cố "loại" thừa) và bài ngoài phạm vi.
5. Chưa nêu cách tính độ đồng thuận (kappa trọng số, hệ số Krippendorff) và quy trình khi người chấm lệch nhiều.
6. Vẫn thiếu tiêu chí "dễ hiểu, phù hợp trình độ học sinh" mà đợt 4 đã nêu.
7. "Double-Blind" dùng chưa chính xác; thiết kế mô tả là chấm mù (người chấm không biết công cụ). Gọi đúng tên để tránh bị hỏi.

**Bảng 4.2:** các con số "< 0.05s", "1–3s", "< 0.02s" không có phương pháp đo, thiết bị, số lần lặp; các phát biểu về mô hình phí của Symbolab/Photomath thay đổi theo gói và theo thời gian, cần ghi ngày kiểm tra và nguồn; "Nguồn mở, miễn phí" cần ghi tên giấy phép của chính dự án; "rủi ro rò rỉ = Không, an toàn 100%" nên giới hạn theo điều kiện (chỉ khi không bật chức năng gọi dịch vụ ngoài, nếu có). Tôi **không kiểm chứng** các phát biểu về dịch vụ thương mại; cần tác giả cung cấp nguồn.

---

## 6. Việc cần làm trước khi nộp (theo thứ tự ưu tiên)

| # | Việc | Mức |
|---|---|---|
| 1 | Thay bộ lọc nghiệm thực bằng `real_status` (mục 3.1); thêm test √(x³−3x+1)=1/2 | Cao |
| 2 | Sửa bảng 3.2 bài Trăm trâu: (4,18,78), (8,11,81), (12,4,84) | Cao |
| 3 | Sửa nhánh chạm trần: bỏ "toàn bộ" và `S = {…}`, in tổng số nghiệm hoặc họ tham số (3.3) | Trung bình |
| 4 | Trả đủ ba tập từ hàm căn thức; có bước kết luận nêu riêng nghiệm chưa xác định; thêm một ca test cho `unknown` (3.4) | Trung bình |
| 5 | Sửa nhãn họ nghiệm (k ≥ …) và nhãn d ≥ 2 trên ℤ⁺ (3.5, 3.6) | Trung bình |
| 6 | Đính kèm bộ test tự động và log chạy, kể cả oracle vét cạn; bỏ câu "100%" | Trung bình |
| 7 | Rà lại toàn văn bỏ cụm tuyệt đối (mục 4); sửa "4 trạng thái", tên nhãn, "mod 1", "Phân" | Trung bình |
| 8 | Hoàn thiện Rubric (neo 2 và 4, bộ bài, độ đồng thuận) và đưa nguồn cho bảng 4.2 (mục 5) | Thấp–TB |

---

## 7. Kết luận

Hai hàm đã tốt hơn nhiều so với v2.4: các lỗi nhận dạng dạng phương trình, nhận nghiệm khi bất định, cửa sổ 200 và im lặng khi d ≠ 1 đã được xử lý, và hàm Diophantine vượt qua oracle vét cạn 398 hệ không sai sót. Ba chỗ cần xử lý trước khi nộp: **bộ lọc nghiệm phức đang loại nhầm nghiệm thực** (do bản sửa mới), **bảng kiểm thử có số liệu sai ở bài Trăm trâu**, và **văn bản vẫn dùng các cụm tuyệt đối** trái với tuyên bố của chính nó. Phần Rubric đúng hướng nhưng chưa đủ để dùng làm bằng chứng.

---

*Phản biện này dựa trên việc trích và chạy thật hai hàm trong báo cáo v2.5 (SymPy 1.14.0, các đối tượng giao diện được thay bằng đối tượng giả) và oracle vét cạn nêu ở mục 0. Đây là tham vấn kỹ thuật bằng công cụ AI, không thay thế thẩm định bởi người thật.*
