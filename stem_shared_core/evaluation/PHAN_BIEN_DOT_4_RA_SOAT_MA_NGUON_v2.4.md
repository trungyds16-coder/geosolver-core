# Phản biện đợt 4: rà soát mã nguồn (báo cáo phiên bản 2.4)

**Đối tượng:** `solve_radical_pedagogical` và `solve_underdetermined_or_diophantine` trong báo cáo v2.4 (07/11/2026), cùng khung Rubric sư phạm.

---

## 0. Phạm vi và cách làm (đọc kỹ trước khi dùng kết luận)

**Đã làm:**

- Đọc từng dòng hai hàm trong báo cáo.
- **Mô phỏng phần số học của hàm Diophantine bằng `Fraction`** (Python chuẩn): chuyển nguyên văn logic cận dưới/cận trên/quét tham số, với dạng affine của từng ca được suy tay từ ma trận. Kết quả nằm ở mục 4.

**Chưa làm được:**

- **Không chạy mã gốc.** Máy phản biện không có SymPy và không cài được. Mọi nhận định về hành vi của `sp.sign`, `sp.ask`, `sp.solve` là **suy luận từ mã và hiểu biết về SymPy, chưa kiểm chứng**, và được đánh dấu "cần test".
- Chỉ thấy hai hàm, không thấy nơi gọi, `clean_display_expr`, hay các phần còn lại của `cad_math_v2.py`. Một số nhận xét phụ thuộc vào cách nơi gọi chuẩn hóa dữ liệu; các chỗ đó được nêu rõ.

---

## 1. Trả lời ba câu hỏi của báo cáo

**Câu 1 — `check_sign_exact` đã đủ an toàn chưa?** **Chưa.** Ý tưởng đúng (ca $g(r)=0$ được xử lý, có trạng thái `None`), nhưng ở nơi gọi trạng thái bất định vẫn **bị nhận nghiệm**, mọi ngoại lệ **nhận nghiệm im lặng**, và nhánh dự phòng dùng ngưỡng số thực $-10^{-9}$. Ngoài ra, hàm có lỗi **nhận dạng dạng phương trình** nghiêm trọng hơn cả vấn đề dấu (mục 3.1).

**Câu 2 — Bộ giải Diophantine đã triệt tiêu rủi ro chưa?** **Chưa.** Hai chốt (chặn hằng số ≤ 0, thế ngược) làm đúng việc của chúng và đã giải quyết các điểm tôi nêu ở đợt 3. Nhưng thế ngược chỉ bảo đảm **tính đúng đắn** (không in nghiệm sai), không bảo đảm **tính đầy đủ**. Mô phỏng cho thấy cửa sổ quét 200 giá trị **bỏ sót nghiệm** và hệ không phân biệt được "vô số nghiệm" với "vô nghiệm nguyên" (mục 4). Rủi ro ở đây không phải sai số làm tròn (số hữu tỷ chính xác không có sai số) mà là lỗi logic liệt kê.

**Câu 3 — Rubric đã vững chưa?** **Chưa.** Bảng điểm hiện là tự đánh giá của nhóm tác giả cho chính công cụ của mình (10/10), không chấm mù, không có người chấm độc lập, tiêu chí có thiên lệch. Nên trình bày như "khung rubric dự thảo" cho đến khi có điểm của người chấm độc lập (mục 5).

---

## 2. Những điểm đã làm đúng

- **Chặn biến hằng $\le0$** trong hàm Diophantine: mô phỏng ca $x=z-5,\ y=0$ cho `EMPTY_INFEASIBLE`, đúng. Đây là lỗ hổng tôi nêu ở đợt 3 và đã được sửa.
- **Thế ngược vào hệ gốc** bằng số hữu tỷ chính xác: chốt an toàn đúng hướng cho tính đúng đắn.
- **Ca 1–3 của báo cáo:** mô phỏng cho đúng kết quả: Ca 1 → $(6,20,74),(13,10,77)$; Ca 2 → bốn nghiệm; Ca 3 → họ nghiệm $(z-5,2,z)$.
- **Ca $g(r)=0$** được xử lý có chủ đích (`0 >= 0` là `True`).
- **Có trạng thái bất định `None`** và cảnh báo hiển thị cho người dùng (nhưng xem 3.2).
- Báo cáo đã bỏ khẳng định "luôn có khoảng chặn đóng" và nêu rõ các trường hợp.

---

## 3. Hàm căn thức `solve_radical_pedagogical`

### 3.1. Lỗi nhận dạng dạng phương trình (mức: cao, từ đại số, không cần chạy mã)

Mã tính:

```python
rad = rad_terms[0]
gx = sp.simplify(rad - target_eq)
```

Nếu `target_eq` là biểu thức "vế trái − vế phải" và căn xuất hiện với **hệ số +1**, tức `target_eq = rad + h`, thì `rad - target_eq = -h = g`. Đúng.

Nhưng trong các dạng sau, `gx` **sai**:

| Phương trình nhập | `target_eq` | `rad - target_eq` | Hệ quả |
|---|---|---|---|
| $\sqrt{2x-1}=x-1$ | $\sqrt{2x-1}-x+1$ | $x-1$ | Đúng |
| $x-1=\sqrt{2x-1}$ | $x-1-\sqrt{2x-1}$ | $2\sqrt{2x-1}-x+1$ (còn chứa căn) | **Sai** |
| $2\sqrt{2x-1}=x-1$ | $2\sqrt{2x-1}-x+1$ | $-\sqrt{2x-1}+x-1$ | **Sai** |

Với cả hai dạng sai, các bước 1–3 sẽ hiển thị điều kiện và nghiệm cho một phương trình khác với phương trình học sinh nhập, mà không có cảnh báo nào. Đây là lỗi nặng vì nó làm **lời giải sư phạm sai**, đúng thứ công cụ định cung cấp.

**Lưu ý:** nhận xét này đúng nếu nơi gọi không chuẩn hóa `target_eq` trước. Nếu nơi gọi đã đưa căn về vế trái với hệ số +1, lỗi không xảy ra; khi đó cần ghi rõ tiền điều kiện ở hàm và kiểm tra nó (assert hoặc trả "ngoài phạm vi").

**Đề xuất (phác thảo, chưa chạy thử):**

```python
rads = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
if len(rads) != 1:
    return None, ["Ngoài phạm vi: cần đúng một căn bậc hai."]
rad = rads[0]
expanded = sp.expand(target_eq)
c = expanded.coeff(rad)                 # hệ số của căn
rest = sp.expand(expanded - c * rad)    # phần không chứa căn
if c == 0 or c.free_symbols or any(t.exp == sp.Rational(1, 2) for t in rest.atoms(sp.Pow)):
    return None, ["Ngoài phạm vi: dạng căn không chuẩn."]
gx = sp.simplify(-rest / c)             # √f = g
```

### 3.2. Nhận nghiệm khi bất định (mức: cao)

Docstring ghi "không âm thầm nhận/loại", nhưng mã làm ngược lại:

1. Nhánh `else` (cả hai `None`) thực hiện `valid_sols.append(r)`: **nghiệm bất định được đưa vào tập nghiệm hợp lệ**, chỉ kèm dòng cảnh báo.
2. Khối `except Exception: valid_sols.append(r)`: **mọi lỗi tính toán → nhận nghiệm im lặng**, không cả cảnh báo.
3. Nhánh số thực cuối `val >= -1e-9` vẫn chấp nhận giá trị âm rất nhỏ. Đó là lỗi cùng loại như ngưỡng $10^{-7}$ ở đợt 3, chỉ thu hẹp ngưỡng.

Thiết kế an toàn: trả về **ba tập tách biệt**: nghiệm hợp lệ, nghiệm bị loại, nghiệm **chưa xác định** (hiển thị riêng, không đưa vào đáp số cuối). Chỉ khi xác định được dấu mới kết luận.

### 3.3. "Dấu đại số chính xác" chưa chắc là chính xác (mức: trung bình – cao, cần test)

`float(sp.sign(expr)) >= 0` chỉ chính xác khi `sp.sign` tự đánh giá được. Nếu `sp.sign(expr)` trả về dạng chưa đánh giá, `float()` buộc phải **đánh giá số thực**, tức là quay về kiểm tra số thực. Các nhánh `ask` và `evalf` phía sau gần như không bao giờ được chạm tới cho số thực vì nhánh đầu đã trả kết quả.

Cần test (theo hiểu biết của tôi, chưa kiểm chứng): nghiệm là số đại số lồng căn mà $g(r)=0$ đúng nhưng SymPy không tự rút gọn về 0. Khi đó `float(sign)` có thể trả $\pm1$ do nhiễu số, và hệ thống **loại nhầm một nghiệm đúng** hoặc nhận nhầm.

**Đề xuất (phác thảo, chưa chạy thử):** tách trạng thái rõ ràng và không đoán.

```python
def sign_status(v):
    """Trả về 'pos' | 'neg' | 'zero' | 'nonreal' | 'unknown'; không bao giờ đoán."""
    v = sp.simplify(v)
    if v.is_real is False:
        return 'nonreal'
    if v.is_zero:
        return 'zero'
    if v.is_positive:
        return 'pos'
    if v.is_negative:
        return 'neg'
    approx = v.evalf(60)
    if abs(approx) > sp.Float('1e-40'):
        return 'pos' if approx > 0 else 'neg'
    return 'unknown'  # có thể bằng 0 đúng; cần minimal_polynomial / equals
```

### 3.4. Các vấn đề phụ

1. **Nhiều căn bị bỏ qua im lặng:** `rad_terms[0]` lấy căn đầu tiên mà không kiểm tra có đúng một căn. Phương trình hai căn (đã khai báo ngoài phạm vi) sẽ vẫn được xử lý và cho kết quả sai thay vì bị từ chối.
2. **Nghiệm phức:** `sp.solve` có thể trả nghiệm phức (cần test). Với giá trị phức, `float(s)` ném `TypeError`; nếu `ask` cũng không xác định thì rơi xuống nhánh nhận nghiệm. Cần lọc nghiệm thực trước (`r.is_real`).
3. **`except:` trần** (không chỉ `Exception`) cũng nuốt `KeyboardInterrupt`; nên dùng `except Exception` và ghi lại lý do.
4. **Nhánh "vi phạm điều kiện căn thức $f\ge0$" gần như không bao giờ xảy ra** với nghiệm thực (vì $f=g^2$); nếu xuất hiện thì là dấu hiệu nghiệm phức hoặc lỗi nhập dạng (3.1).

### 3.5. Câu chữ sư phạm (đáng chú ý vì giá trị đề tài nằm ở lời giải)

- Bước 1 ghi: "bắt buộc $g(x)\ge0$ **để căn thức có nghĩa thực**". Lý do này không chính xác. $g\ge0$ là cần vì **căn bậc hai số học luôn không âm**: $\sqrt{f}\ge0$ nên $g=\sqrt{f}\ge0$. Câu này có thể dạy học sinh một lý do sai. Gợi ý: *"Vì $\sqrt{f(x)}\ge0$ nên vế phải phải không âm: $g(x)\ge0$."*
- Dòng "Nhận" nên **hiển thị giá trị** (ví dụ "$g(r)=2.41\ge0$"), và dòng "Loại" nên hiển thị giá trị âm tương ứng. Lời giải có số liệu thuyết phục hơn lời khẳng định.

---

## 4. Hàm Diophantine: kết quả mô phỏng và lỗi logic

### 4.1. Kết quả mô phỏng (bằng `Fraction`, không phải chạy mã gốc)

| Ca | Phân loại | Nghiệm tìm được |
|---|---|---|
| Ca 1 | `FINITE_BOUNDED`, $p\in[72,79]$ | $(6,20,74),(13,10,77)$ ✓ |
| Ca 2 | `FINITE_BOUNDED`, $p\in[6,9]$ | 4 nghiệm đúng báo cáo ✓ |
| Ca 3 | `UNBOUNDED_INFINITE` | $(1,2,6),(2,2,7),(3,2,8)$ ✓ |
| $x=z-5,\ y=0$ | `EMPTY_INFEASIBLE` | rỗng ✓ |
| $z>5$ và $z<5$ | `FINITE_BOUNDED`, quét $(6,4)$ | rỗng (xem 4.5) |
| **Phản ví dụ A:** $251x-z=-5,\ y=2$ | `UNBOUNDED_INFINITE`, quét $[5,204]$ | **rỗng** |
| **Phản ví dụ B:** $2x-2z=1,\ y=5$ | `UNBOUNDED_INFINITE`, quét $[1,200]$ | **rỗng** |
| Phản ví dụ A, cửa sổ 1000 | `UNBOUNDED_INFINITE` | $(1,2,256),(2,2,507),(3,2,758)$ |

### 4.2. Cửa sổ quét 200 giá trị (mức: cao)

Ở nhánh `UNBOUNDED_INFINITE`, mã chỉ quét `range(start_p, start_p + 200)`. Phản ví dụ A có **vô số nghiệm nguyên dương** (mọi $z\equiv5 \pmod{251}$, $z>5$), nhưng nghiệm nhỏ nhất là $z=256$, nằm ngoài cửa sổ nên **không tìm thấy gì**. Phản ví dụ B thì **thật sự vô nghiệm nguyên** ($x=z+\tfrac12$). Hai hệ có cùng kết quả (`UNBOUNDED_INFINITE`, danh sách rỗng) nhưng đáp án đúng **trái ngược nhau**. Nếu hệ thống kết luận "có vô số nghiệm nguyên dương" (như comment cuối nhánh gợi ý) khi danh sách rỗng, nó **sai ở ca B**; nếu kết luận "không có nghiệm", nó **sai ở ca A**.

### 4.3. Phân tích đồng dư được tính nhưng không dùng (mức: cao về tính nhất quán báo cáo–mã)

`lcm_denom` được tính và **không bao giờ được dùng** (mã chết). Mã thực tế là **vét cạn tham số nguyên trong khoảng chặn** rồi kiểm tra nguyên. Báo cáo (mục 3.2 v2.2, và v2.3/v2.4) vẫn mô tả "phân tích đồng dư động, điều kiện chia hết modulo $D$". Báo cáo cần mô tả đúng phương pháp đang chạy, hoặc mã cần thực sự dùng modulus. Cách dùng đúng chính là cách khắc phục 4.2:

Với mỗi biến $v=\frac{a}{q}p+\frac{b}{r}$, quy đồng được một đồng dư tuyến tính $Ap\equiv B \pmod{M}$. Giải từng đồng dư bằng `gcd` và nghịch đảo modular, kiểm tra tương thích, hợp nhất bằng CRT. Kết quả là: (a) vô nghiệm nguyên (không còn lớp đồng dư), hoặc (b) $p\equiv r \pmod{M}$. Khi đó: ở nhánh hữu hạn, quét theo bước $M$; ở nhánh vô hạn, nghiệm tham số $p=r+Mk$ với giá trị nhỏ nhất tính trực tiếp, không còn phụ thuộc cửa sổ.

### 4.4. Im lặng khi ngoài phạm vi (mức: cao)

Trong đoạn mã gửi, nếu `len(free_syms) != 1` (nghiệm duy nhất, $d=0$, hoặc $d\ge2$) **không có nhánh `else`**: hàm không in gì, không báo lỗi. Người dùng không biết hệ bị bỏ qua. Cần thông báo tường minh: $d=0$ (kiểm tra dương, nguyên của nghiệm duy nhất), $d\ge2$ ("chưa hỗ trợ").

### 4.5. Các điểm phụ

1. **Không có trần số lần lặp ở nhánh `FINITE_BOUNDED`:** khoảng như $[1,10^9]$ sẽ treo ứng dụng. Cần trần hoặc quét theo bước modulus (4.3).
2. **Nhãn có thể gây hiểu nhầm:** mô phỏng cho ca $z>5,\ z<5$ nhãn `FINITE_BOUNDED` (quét $(6,4)$) với danh sách rỗng. Nên xuất `EMPTY_INFEASIBLE` khi không có điểm nguyên trong khoảng.
3. **Cần xác nhận `eq_syms` là biểu thức "vế trái − vế phải", không phải `Eq`:** nếu là `Eq`, `eq_orig.subs(...)` cho ra `True/False` và so sánh `== 0` luôn sai, khiến chốt an toàn loại mọi nghiệm. Các ca 1–3 trong báo cáo cho kết quả đúng nên khả năng cao đây là biểu thức, nhưng nên ghi rõ.
4. **Thế ngược chỉ bảo vệ tính đúng đắn.** Chưa có bất biến nào kiểm tra tính đầy đủ (không bỏ sót nghiệm). Cần oracle vét cạn độc lập (mục 6).

---

## 5. Khung Rubric sư phạm

**Điểm mạnh:** hướng đi đúng (đo giá trị sư phạm thay vì đáp số), có ba tiêu chí rõ ràng, và công khai việc SymPy `check=True` đúng về đáp số.

**Vấn đề:**

1. **Người chấm là chính tác giả, chấm công cụ của mình, kết quả 10/10.** Một điểm tuyệt đối do người làm ra công cụ tự chấm không có giá trị chứng minh, kể cả khi chấm trung thực. Cần người chấm độc lập, chấm mù.
2. **Không mô tả quy trình chấm.** Điểm lẻ (2.5, 8.5) ngầm cho thấy có thang chi tiết, nhưng báo cáo không nêu mốc điểm cho từng mức. Không có số người chấm, độ đồng thuận giữa người chấm.
3. **Tiêu chí thiết kế theo đúng tính năng của công cụ.** Tiêu chí 3 chiếm 4/10 điểm và mô tả đúng việc công cụ làm. Thiên lệch cấu trúc.
4. **Chấm SymPy 0 điểm ở hai tiêu chí là so sánh khác loại.** Một bộ giải không nhằm giải thích thì nên ghi "không áp dụng" thay vì 0. So sánh có ý nghĩa là giữa các công cụ có lời giải từng bước.
5. **Dòng Symbolab/Wolfram Alpha chưa có nguồn:** 10 bài nào, chạy ngày nào, phiên bản/gói nào, lưu ảnh chụp ở đâu? Kết quả các dịch vụ này đổi theo thời gian và gói sử dụng. Cột "có phí bản quyền" cũng cần kiểm chứng theo gói cụ thể.
6. **Thiếu tiêu chí "dễ hiểu, phù hợp trình độ"**, vốn là tiêu chí nhóm đã nêu ở kế hoạch khảo sát giáo viên (mục 6 của v2.3).
7. **Cột "Môi trường vận hành"** gộp các ưu điểm thật (chạy offline, tiếng Việt, miễn phí) vào bảng điểm sư phạm. Đó là lợi thế sản phẩm hợp lệ, nên trình bày **riêng**, không cộng vào điểm.

**Đề xuất:**

- Chấm bởi ít nhất 3 người độc lập (giáo viên), **chấm mù**: ẩn tên công cụ, đưa lời giải đã chuẩn hóa định dạng.
- Mô tả mốc điểm (anchor) cho từng mức của từng tiêu chí, công bố trước khi chấm.
- Báo cáo trung vị, dải điểm và độ đồng thuận (ví dụ kappa trọng số hoặc hệ số Krippendorff).
- Giữ bảng hiện tại với nhãn **"tự đánh giá sơ bộ của nhóm, chưa có người chấm độc lập"**.

---

## 6. Bộ test đề xuất

**Căn thức (kết quả kỳ vọng suy từ đại số):**

| Phương trình | Kỳ vọng |
|---|---|
| $\sqrt{2x-1}=x-1$ | Nhận $2+\sqrt2$; loại $2-\sqrt2$ |
| $x-1=\sqrt{2x-1}$ (đảo vế) | Cùng đáp án với dòng trên; kiểm tra lỗi 3.1 |
| $2\sqrt{2x-1}=x-1$ | Nhận $5+2\sqrt5$; loại $5-2\sqrt5$ |
| $\sqrt{x}=x^2+1$ | Vô nghiệm thực; bốn nghiệm phức của hệ quả đều phải bị loại |
| $\sqrt{x}+\sqrt{x+1}=2$ | Từ chối: ngoài phạm vi (kiểm tra 3.4.1) |
| Nghiệm đại số lồng căn với $g(r)=0$ | Không được loại nhầm; trạng thái `unknown` nếu không chứng minh được (kiểm tra 3.3) |

**Diophantine:**

| Hệ | Kỳ vọng |
|---|---|
| $251x-z=-5,\ y=2$ | Vô hạn nghiệm, nghiệm nhỏ nhất $(1,2,256)$ |
| $2x-2z=1,\ y=5$ | Vô nghiệm nguyên (trạng thái riêng) |
| $x=3,\ y=4$ ($d=0$) | Nghiệm duy nhất $(3,4)$ |
| $x+y+z=10$ ($d=2$) | Thông báo "chưa hỗ trợ", không im lặng |
| $x+z=10^9,\ y=1$ | Không treo; trần hoặc họ nghiệm tham số |
| Hệ không nhất quán | Vô nghiệm thực |

Kèm **oracle vét cạn** trên hộp nhỏ cho mọi ca ngẫu nhiên, so sánh *tập nghiệm* (không chỉ kiểm tra từng nghiệm in ra).

---

## 7. Danh sách việc cần làm, theo thứ tự ưu tiên

| # | Việc | Mức |
|---|------|-----|
| 1 | Sửa nhận dạng dạng phương trình (3.1) hoặc từ chối dạng ngoài tiền điều kiện | Cao |
| 2 | Tách ba tập (hợp lệ / loại / chưa xác định); bỏ nhận nghiệm khi bất định và khi ngoại lệ (3.2) | Cao |
| 3 | Dùng đồng dư (CRT) thay cửa sổ 200; phân biệt vô hạn nghiệm với vô nghiệm nguyên (4.2, 4.3) | Cao |
| 4 | Thông báo tường minh khi $d\ne1$; trần số vòng lặp (4.4, 4.5.1) | Cao |
| 5 | Đồng bộ báo cáo với mã: bỏ mô tả "modulo $D$" nếu mã không dùng (4.3) | Cao |
| 6 | Bộ test mục 6 và oracle vét cạn; báo cáo kết quả chạy thực | Cao |
| 7 | Chấm rubric bởi người độc lập, chấm mù; đổi nhãn bảng hiện tại (mục 5) | Cao |
| 8 | Sửa câu chữ bước 1 và hiển thị giá trị $g(r)$ (3.5) | Trung bình |
| 9 | Lọc nghiệm phức; thay `except:` trần (3.4) | Trung bình |
| 10 | Bỏ các cụm tuyệt đối còn sót ("triệt tiêu được các rủi ro", "tiếp thu trọn vẹn") | Trung bình |

---

## 8. Kết luận

Hai hàm đã tiến bộ so với đợt 3: chặn hằng số ≤ 0, thế ngược chính xác, có trạng thái bất định. Tuy nhiên ba điều cần sửa trước khi nộp: **(a)** nhận dạng dạng phương trình trong hàm căn thức có thể làm lời giải sai mà không cảnh báo; **(b)** nghiệm bất định và mọi ngoại lệ đang bị nhận thay vì được tách riêng; **(c)** hàm Diophantine bỏ sót nghiệm khi nghiệm nhỏ nhất vượt cửa sổ 200 và không phân biệt vô hạn với vô nghiệm nguyên. Rubric hiện chưa đủ sức làm bằng chứng cho giá trị sư phạm vì chưa có người chấm độc lập.

Mọi kết luận ở mục 3.3 và các ghi chú "cần test" cần được đối chiếu bằng cách chạy mã thật với SymPy phiên bản đang dùng. Mô phỏng ở mục 4 chỉ kiểm tra logic số học, không thay thế việc chạy mã.

---

*Phản biện này dựa trên đọc mã trong báo cáo và mô phỏng `Fraction` nêu ở mục 4. Phản biện bằng công cụ AI là tham vấn kỹ thuật, không thay thế thẩm định bởi người thật.*
