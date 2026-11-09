# THẨM ĐỊNH HỒ SƠ BÁO CÁO KHOA HỌC & GIẢI TRÌNH PHẢN BIỆN v2.10

**Đối tượng thẩm định:** `BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_10.md` (CAD Math Studio & GeoSolver 2D)  
**Ngày thẩm định:** 08/11/2026  
**Câu hỏi cần trả lời:** Hồ sơ v2.10 đã đủ điều kiện đóng vòng phản biện lý thuyết và giải thuật chưa?

---

## 1. KẾT LUẬN

**Chưa đủ điều kiện đóng ngay. Đề xuất đóng có điều kiện** sau khi xử lý 4 mục chặn (§3) trong một bản v2.11 ngắn. Các mục này đều sửa được và không cần thêm vòng thực nghiệm mới.

So với v2.9, hồ sơ tiến bộ rõ rệt. Tuy nhiên có hai tuyên bố then chốt không đúng với mã nộp kèm: "mutation testing 100%" và "tái lập 100% không cần mã sản phẩm". Ngoài ra còn một số mô tả sai về bất biến, ca kiểm thử và so sánh với SymPy.

---

## 2. NHỮNG ĐIỂM ĐÃ KIỂM CHỨNG VÀ GHI NHẬN

Phương pháp: trích khối mã harness trong tài liệu, chạy lại bằng stub. Hồ sơ **không đính kèm mã solver v2.10**, nên phần solver được thay bằng lõi v2.9 làm đại diện. Kết quả dưới đây vì vậy chỉ có giá trị tương đối với v2.10.

| Hạng mục | Kết quả |
|---|---|
| SHA-256 của harness | Khối mã trong tài liệu (chuẩn hóa LF, có xuống dòng cuối) cho hash khớp 16 ký tự hex đầu với `f7921ec28969dcf9…` đã khai báo (chưa đối chiếu đủ 64 ký tự) |
| Phân bổ phân loại của oracle | Lõi v2.9 + bộ sinh v2.10 (seed 42) cho đúng `{FINITE_BOUNDED: 9, INFEASIBLE_BOUNDS_EMPTY: 64, INFEASIBLE_NO_INTEGER_POINTS: 15, UNBOUNDED_INFINITE: 12}`, khớp log |
| Đúng đắn giải thuật | Với oracle **hộp cố định độc lập** (vét cạn p ∈ [1, 3000], không dùng công thức cận): 100/100 hệ khớp tuyệt đối về phân loại, `n_total` và nghiệm |
| Số liệu thời gian | Nhất quán nội bộ: 4469,38 / 19 = 235,23 ms; radical 615,10 ms; Diophantine 13,64 ms; min 0,13 ms; max 1874,07 ms |
| Ca mới | DIO_10 (z ≡ 11 mod 12 → (2,3,11)), DIO_09, DIO_11, DIO_12 đều đúng. DIO_12 đi qua nhánh `sc is None` (đã xác nhận trong đầu ra có dòng "Không thỏa mãn hệ đồng dư CRT") |
| Bất biến 2 | Đã tính lại số học cho từng nghiệm bị loại thay vì đọc nhãn chuỗi, khắc phục lỗi vòng tròn của v2.9 |

---

## 3. VẤN ĐỀ CHẶN

### B1. Thiếu mã solver; tuyên bố "tự chứa, tái lập 100%" không đúng

- §8 nói harness cho phép tái lập "trên bất kỳ máy tính nào mà không phụ thuộc GUI". Nhưng harness có dòng `from cad_math_v2.cad_math_v2 import CADMathDesktopAppV2, DiophantineCategory`, tức là cần tệp sản phẩm.
- Tài liệu chỉ chứa lớp Enum (12 dòng) và harness (518 dòng). v2.9 có trọn vẹn mã solver, v2.10 thì không.
- Hậu quả: các tuyên bố sau không kiểm chứng được:
  - `check_sign_exact` đã tách thành phương thức tĩnh. Trong lõi v2.9 hàm này là hàm lồng trong solver nên `patch.object(app, ...)` sẽ không tác động được; cần xem mã v2.10 để biết RAD_07 có thật sự đi qua mã sản phẩm.
  - Hash `52f056cc…` của `cad_math_v2.py`.
  - Mọi kết quả log.
- Liên kết `file:///D:/AI%20DATA/...` là đường dẫn máy cục bộ, người phản biện không mở được.
- **Cần sửa:** đính kèm đầy đủ `cad_math_v2.py` (hoặc phần solver), ghi hash toàn bộ 64 ký tự, nêu model CPU (v2.9 ghi i7-11800H, v2.10 chỉ ghi "Intel Core i7") và chỉ một phiên bản Python (hiện ghi "Python 3.14 / 3.12").

### B2. "Mutation Testing 9/9, 4/9" không phải kiểm thử đột biến

Mã ở "PHẦN 3" không hề chạy solver đã bị đột biến:

- **Đột biến 1 và 2:** harness tự tính lại cận `lo`, `hi` bằng công thức đột biến rồi so `lo_m1 != lo` và `hi_m2 != hi`. Đây là so sánh hai giá trị cận trong chính harness, không phải kiểm tra oracle có phát hiện lỗi hay không.
- **Đột biến 3:** là lệnh cộng cứng `mutations_caught[...] += 1` kèm chú thích "luôn bị bắt". Không có phép chạy nào.
- Con số "4/9" thực chất là số hệ mà giá trị cận đổi, không phải số hệ mà *đầu ra solver* đổi. Lời giải thích "5 hệ còn lại là đột biến tương đương" cần được chứng minh bằng cách so đầu ra, chưa được chứng minh.
- Kiểm tra cho thấy làm đúng thì khả thi: chèn từng đột biến vào mã solver rồi chạy oracle hộp cố định, bắt được cả ba (số hệ bị đánh dấu sai trên 100 hệ: **7, 8, 9**).
- **Cần sửa:** sinh mã đột biến thật (thay chuỗi/AST hoặc `mock.patch`), chạy toàn bộ suite 19 ca + oracle, báo cáo mutant bị giết / tổng. Mutant sống phải được kiểm tra tương đương bằng cách so đầu ra trên cùng tập hệ.

### B3. Oracle chưa độc lập về logic cận

- Oracle sao chép nguyên công thức của solver: `lo = 1`, `floor(-b/a)+1`, `ceiling(-b/a)-1`, `infeasible_const`. Chỉ khâu liệt kê số nguyên trong `[lo, hi]` là độc lập.
- Hậu quả: một lỗi cùng chiều ở cả hai bản sao (ví dụ sai công thức cận) sẽ không bị phát hiện. Với 64/100 hệ `INFEASIBLE_BOUNDS_EMPTY`, việc "xác nhận rỗng" chỉ là chạy lại cùng công thức.
- Kiểm tra bằng oracle hộp cố định cho kết quả 100/100, nên chưa phát hiện lỗi chung nào. Nhưng bản thân harness chưa chứng minh điều đó.
- Phân bố thiên lệch: chỉ 21/100 hệ (9 + 12) thực sự kiểm tra việc đếm nghiệm.
- **Cần sửa:**
  - Oracle vét cạn trong hộp cố định, không dùng công thức cận. Có thể chặn hộp theo |rhs| ≤ 40 và |hệ số| ≤ 4, hoặc dùng N đủ lớn rồi đối chiếu `n_total` với số nghiệm đếm được.
  - Sinh phân tầng để mỗi loại có đủ số hệ (ví dụ ≥ 25 hệ cho `FINITE_BOUNDED`).

### B4. Mô tả sai về "kiểm tra đủ nghiệm" và ca RAD_02 trùng RAD_01

- §0 và §2.2 nói tập `valid` được so với "nghiệm giải tích thực được tính độc lập". Mã thực tế chỉ so với danh sách `expected_valid` / `expected_valid_count` gõ tay (RAD_04 chỉ so số lượng = 3). Đây vẫn là kiểm tra hợp lý, nhưng phải mô tả đúng bản chất (đáp án tay đã duyệt), không gọi là tính độc lập.
- Bất biến phân hoạch gọi lại `sp.solve(f - g², x)` y hệt solver. Nó bảo vệ khỏi mất nghiệm trong phân loại nhưng không độc lập với bước chuẩn hóa.
- **RAD_02 trùng RAD_01:** `sqrt(2x-1) + (1-x)` và `sqrt(2x-1) - (x-1)` là **cùng một biểu thức SymPy** (đã kiểm tra: `True`). v2.9 có `(x-1) - sqrt(2x-1)` kiểm thử trường hợp hệ số căn `c = -1`; bản mới làm mất độ phủ này. Bộ suite thực chất chỉ có 6 ca radical khác nhau.
- **Cần sửa:** khôi phục ca `c = -1`, ví dụ `(x - 1) - sp.sqrt(2*x - 1)`; mô tả lại đúng bản chất của kiểm tra đủ nghiệm.

---

## 4. VẤN ĐỀ PHỤ

| # | Vấn đề | Chi tiết |
|---|---|---|
| P1 | "Bao phủ toàn bộ nhánh rẽ" và "9 trạng thái" | Không có đo độ phủ nhánh (coverage.py `--branch`). Bảng §3.2 có 9 hàng nhưng hàng 6 và 7 cùng một giá trị Enum `INFEASIBLE_NO_INTEGER_POINTS`, nên chỉ có 8 giá trị Enum xuất hiện. Giá trị `UNKNOWN` không có hàng nào; trong lõi v2.9 nó chỉ là giá trị khởi tạo và không có đường nào trả về (không thể đạt tới). Cần ghi rõ "8 trạng thái đạt tới được + 1 dự phòng" hoặc loại `UNKNOWN`. |
| P2 | So sánh với SymPy sai thực tế (§6) | Bảng ghi SymPy "cần tham số bổ sung `check=True`". Thực tế `sp.solve(sqrt(2x−1)−(x−1), x)` mặc định trả `[2 + √2]`, tức là đã loại nghiệm ngoại lai. Ưu thế của CAD Math Studio nằm ở *giải thích sư phạm*, không phải ở *phát hiện* nghiệm ngoại lai. |
| P3 | Ô của Photomath/Symbolab và "O(1)" | "Thường timeout", "Không" ở hàng cảnh báo bất định, "Hỗ trợ hạn chế" đều chưa có bằng chứng (ảnh chụp có ngày, bản ghi thao tác). "Định dạng GDPT 2018" chưa có đối chiếu với tài liệu chương trình. "Thuật toán CRT O(1)" không đúng: còn `sp.simplify` lên đến 10 nghiệm, và việc giải đồng dư không phải O(1) theo độ lớn đầu vào. |
| P4 | Ngôn từ tuyệt đối chưa được làm sạch | Mục #6 trong lời nhắn nói đã làm sạch. Tài liệu vẫn có: "tuyệt đối" ≥ 11 lần, "triệt để" 4, "hoàn toàn" 6, "100%" ≥ 9, "bảo đảm" 2, "chặt chẽ" 1, "chuẩn mực" 1. Tiêu đề ghi sẵn "BẢN ĐÓNG VÒNG LÝ THUYẾT", trong khi việc đóng vòng thuộc về hội đồng. |
| P5 | LaTeX hỏng | Có 41 ký tự TAB, 1 form-feed, 2 ký tự BEL (`\alpha` thành `␇lpha` ở Krippendorff), 3 chỗ `\ne`/`\nmid`/`\notin` bị ăn thành xuống dòng do thiếu escape ngược; thêm `\text{INFEASIBLE_NO_INTEGER_POINTS}` có dấu `_` chưa escape gây lỗi KaTeX (đúng lỗi bạn gặp khi dán). Cần chuẩn hóa toàn bộ công thức. |
| P6 | Thời gian chỉ chạy một lần | RAD_01 là 616 ms ở v2.10 và 197 ms ở v2.9, chênh gấp ~3. Nên đo nhiều lượt (trung vị, IQR), tách lượt khởi động (SymPy cache). |
| P7 | Rubric bị rút gọn so với v2.9 | v2.9 có bảng mô tả mức 5×5, kiểm tra mù, ICC(2,1), Wilson CI, quy trình chuẩn hóa hai giáo viên, kế hoạch xử lý bất đồng. v2.10 chỉ còn 5 tiêu chí một dòng, α và cluster bootstrap (điểm cộng). C1–C4 đo độ đúng và độ an toàn của phần mềm, đã được bộ test bao phủ, nên không phải đại lượng sư phạm. "Bảo đảm tính độc lập thống kê chặt chẽ" là nói quá: cluster bootstrap xử lý sự phụ thuộc chứ không tạo ra độc lập. Nên khôi phục các mục đã bỏ trước khi sang pha thực nghiệm. |
| P8 | Mô tả §0 hàng 2 | "100% các hệ có cận dưới do độ dốc affine quy định" chưa được chứng minh; còn phụ thuộc vào bước nhảy của lớp đồng dư `m_mod` (đột biến có thể tương đương dù cận đổi). |

---

## 5. ĐIỀU KIỆN ĐÓNG VÒNG ĐỀ XUẤT (v2.11)

1. Đính kèm đầy đủ mã solver (hoặc tệp `cad_math_v2.py`), hash 64 ký tự cho cả hai tệp, model CPU và một phiên bản Python.
2. Thay "mutation testing" bằng kiểm thử đột biến thật, báo cáo mutant bị giết / tổng và xử lý mutant sống.
3. Oracle hộp cố định độc lập, phân tầng đủ số hệ cho từng loại; có thể giữ oracle hiện tại như kiểm tra bổ sung.
4. Sửa mô tả "kiểm tra đủ nghiệm"; thay RAD_02 bằng ca `c = -1`.
5. Sửa bảng so sánh SymPy (P2), đánh dấu rõ các ô chưa có bằng chứng, bỏ "O(1)".
6. Chuẩn hóa LaTeX, bỏ từ tuyệt đối, bỏ chữ "ĐÓNG VÒNG" khỏi tiêu đề.

**Mẫu sửa cho B2 và B3** (tinh thần, cần thích ứng với mã thật):

```python
# Oracle hộp cố định, không dùng công thức cận
def brute_box(sol_tuple, p, N=3000):
    return [tuple(int(e.subs(p, v)) for e in sol_tuple)
            for v in range(1, N + 1)
            if all(e.subs(p, v).is_integer and e.subs(p, v) > 0 for e in sol_tuple)]

# Đột biến thật: sửa mã nguồn solver rồi chạy lại toàn bộ oracle
MUTANTS = {
    "floor+0":   ("sp.floor(-b_sym / a_sym) + 1", "sp.floor(-b_sym / a_sym) + 0"),
    "ceiling-0": ("sp.ceiling(-b_sym / a_sym) - 1", "sp.ceiling(-b_sym / a_sym) - 0"),
    "ntotal-1":  ("(hi - start_val) // m_mod + 1", "(hi - start_val) // m_mod"),
}
# killed = số hệ mà oracle phát hiện sai; mutant sống thì so đầu ra để xét tương đương
```

Nếu v2.11 kèm mã solver và log chạy lại, mình có thể đối chiếu nhanh bằng cùng quy trình đã dùng ở trên.
