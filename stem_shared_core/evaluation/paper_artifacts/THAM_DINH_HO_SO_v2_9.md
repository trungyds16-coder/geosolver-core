# THẨM ĐỊNH HỒ SƠ BÁO CÁO KHOA HỌC & GIẢI TRÌNH PHẢN BIỆN v2.9

**Đối tượng thẩm định:** `BAO_CAO_KHOA_HOC_VA_GIAI_TRINH_PHAN_BIEN_v2_9.md` (CAD Math Studio & GeoSolver 2D)  
**Ngày thẩm định:** 08/11/2026  
**Câu hỏi cần trả lời:** Hồ sơ v2.9 đã đạt tiêu chuẩn để đóng vòng phản biện lý thuyết chưa?

---

## 1. KẾT LUẬN

**Chưa nên đóng vòng phản biện với v2.9.**

Thuật toán lõi có vẻ đúng, nhưng bằng chứng kiểm thử chưa chứng minh được điều đó, và còn một số số liệu không khớp với log.

**Phương pháp thẩm định:** trích hai khối mã Python trong tài liệu và chạy bằng stub (không có lớp GUI `CADMathDesktopAppV2`, nên chưa chạy trọn harness). Kết quả:

- Solver Diophantine đúng trên 50/50 hệ khi đối chiếu bằng vét cạn, cả với hệ số dương lẫn hệ số trộn dấu.
- Số nghiệm của RAD_01, RAD_04, RAD_05 và các ca Diophantine khớp bảng trong báo cáo.
- Các vấn đề nằm ở **bằng chứng**, không phải ở thuật toán.

---

## 2. VẤN ĐỀ CHẶN (cần sửa trước khi đóng vòng)

### 2.1. Oracle 50/50 không kiểm chứng được gì

- Điều kiện đạt trong harness là `n_tot <= naive_count or cat in ["FINITE_BOUNDED","UNBOUNDED_INFINITE"]`. Gần như mọi hệ đều thỏa vế sau, và các nhánh `else` tự cộng điểm. Nó không so sánh bằng nhau như báo cáo nói ("khớp số lượng và phân loại").
- Thử cấy 3 đột biến vào solver:

| Đột biến | Oracle của báo cáo | So sánh `n_tot == vét cạn` |
|---|:---:|:---:|
| `floor()+1` → `+0` (cận dưới) | 50/50 | 47/50 |
| `n_total` lệch 1 | 50/50 | 3/50 |
| `ceiling()-1` → `-0` (cận trên) | 50/50 | 23/50 |

- Bộ sinh hệ quá hẹp: hệ số dương cộng với nghiệm cấy sẵn nên 47/50 hệ là `FINITE_BOUNDED`, 3 hệ rơi vào d ≥ 2 (tự qua). Không bao giờ xuất hiện `UNBOUNDED_INFINITE` hay `INFEASIBLE_*`. Khi trộn dấu hệ số thì có 11/50 hệ không bị chặn.
- **Cần sửa:**
  - Dùng `assert n_tot == brute` thay cho điều kiện hiện tại.
  - Trộn dấu hệ số, bỏ nghiệm cấy sẵn.
  - Giải thích vì sao cỡ mẫu giảm từ 699 (v2.8) xuống 50.
  - Chạy lại mutation testing trên harness mới.

### 2.2. `RAD_07` không gọi mã sản phẩm

- Harness tự sao chép logic rồi gán cứng `indet = [... for r in raw_sols]`, nên không kiểm thử `solve_radical_pedagogical`. Lớp `MockAppForUnknown` là mã chết.
- Hàng 3 bảng §1 ("xác nhận được phân loại đúng") mâu thuẫn với §6.3 ("kiểm thử bằng phương pháp giả lập").
- **Cần sửa:**
  - Đưa `real_status` và `check_sign_exact` ra cấp module (hoặc truyền qua tham số).
  - Dùng `unittest.mock.patch` ép trả `'unknown'`, rồi gọi solver thật.
  - Kiểm tra: `indet` khác rỗng, `valid` rỗng, Bước 4 chứa "CHƯA THỂ KẾT LUẬN".

### 2.3. Bất biến 2 mang tính vòng tròn, thiếu kiểm tra đủ nghiệm

- Code kiểm tra *nhãn chuỗi* do chính solver gán (`r_info[1] in [...]`), không kiểm tra tính chất toán học.
- Phải tự tính lại cho từng nghiệm bị loại: |Im r| > 0, hoặc g(r) < 0, hoặc f(r) < 0, và phần dư của phương trình gốc khác 0. Ví dụ x = 2 − √2 ở RAD_01 có g ≈ −0,414 và phần dư ≈ 0,83.
- Còn thiếu:
  - **Bất biến phân hoạch:** valid ∪ rejected ∪ indet = tập nghiệm của phương trình bình phương.
  - **Kiểm tra đủ nghiệm:** valid phải bằng tập nghiệm thực của phương trình gốc, tính bằng phương pháp độc lập.
- Bất biến 3 đúng một cách rỗng khi `sols` rỗng (DIO_04, 06, 07, 08), nhưng log vẫn in "Invariant 3 thỏa mãn". Bất biến 3 cũng chỉ kiểm tối đa 10 nghiệm đầu, không kiểm `n_total`.

### 2.4. Số liệu và phát biểu không khớp

| Phát biểu trong v2.9 | Thực tế |
|---|---|
| Trung bình 637 ms/bài | Log: 2516,4 ms / 17 = **148 ms** (riêng radical: 339 ms) |
| Dải thời gian từ 0,11 ms, "khớp log" | Log nhỏ nhất là **0,12 ms** (RAD_06) |
| 17/17 ca thỏa cả 3 bất biến | Radical chỉ kiểm bất biến 1–2, Diophantine chỉ kiểm bất biến 3, RAD_06/07 không kiểm bất biến nào |
| Cả 7 trạng thái đều có ca kiểm thử | Code có 9 giá trị; `EMPTY_NO_POSITIVE_INTEGER` chưa có ca (đã chạy thử x+y=1, x−y=3 → trả đúng mã này); `UNKNOWN` chưa có ca |
| `NON_COPRIME_CRT` là một trạng thái (§0) | Không phải category nào; DIO_10 chỉ là ca `UNBOUNDED_INFINITE` thông thường, được phân biệt nhờ `expected_sample` |
| "Enum tường minh" | Code dùng chuỗi literal, không phải `enum.Enum`; gõ nhầm tên không bị bắt |
| DIO_08 "hằng số âm" | Ca dùng y = 0 (hằng số bằng 0) |

Ngoài ra, nhánh `sc is None` (CRT vô nghiệm) chưa có ca: DIO_04 đi qua nhánh gcd. Ca đề xuất: `2x − z = 0`, `2y − z + 1 = 0`. Theo phân tích mã, ca này đi qua nhánh `sc is None`, nên gắn bộ đếm nhánh để xác nhận.

---

## 3. VẤN ĐỀ PHỤ

**Văn phong**
- Còn sót "tiệm cận ngưỡng" (hàng 3 §1), "chính thức" (docstring và tiêu đề §3.1), "vững chắc" (§0), trái với hàng 9 bảng §1 và lời nhắn của nhóm tác giả.

**Bảng so sánh §5**
- Ghi "đo đạc thực tế", nhưng số của Symbolab/Photomath chỉ là khảo sát giao diện, và dải 0,05–0,20 s của SymPy không có log. Hai bên chạy bộ bài khác nhau nên không so sánh được. Nên bỏ hàng thời gian hoặc nêu rõ giới hạn.

**Tái lập**
- Khối mã thiếu `clean_display_expr`, `tk` và các import.
- "Commit tích hợp V2.9" không có SHA. Nên ghi hash commit, hash tệp và `requirements.txt`.
- Logic toán gắn với lớp GUI (`self.eq_result_box.insert`). Nên tách hàm toán thuần (trả dữ liệu) khỏi lớp hiển thị.
- §0 nêu "699 hệ" của oracle v2.8 mà không có nguồn đối chiếu trong tài liệu.

**Rubric sư phạm (chưa chặn vòng lý thuyết)**
- Việc chuẩn hóa lời giải về cùng khuôn mẫu có thể xóa chính khác biệt cần đo, vì cấu trúc bước giải là sản phẩm của công cụ.
- Wilson CI giả định các lượt đoán độc lập, trong khi cùng giáo viên và cùng bài bị lặp lại. Nên dùng bootstrap theo cụm hoặc mô hình hỗn hợp.
- Nên báo cáo khoảng tin cậy cho Krippendorff's α, không chỉ ngưỡng 0,70.
- SymPy thuần có thể gặp hiệu ứng sàn điểm ở các tiêu chí sư phạm.

---

## 4. ĐỀ NGHỊ

Đóng vòng sau v2.10, khi các mục 2.1–2.4 được xử lý. Mẫu sửa oracle:

```python
brute = sum(
    1 for p in range(lo, hi + 1)
    if all(c.is_integer and c > 0 for c in (e.subs(par, p) for e in s_tuple))
)
assert n_tot == brute and cat == "FINITE_BOUNDED"   # với hệ bị chặn
```

Với hệ không bị chặn: so sánh 3 nghiệm đầu và kiểm tra `cat == "UNBOUNDED_INFINITE"`.

**Hồ sơ v2.10 nên kèm:**
1. Oracle so sánh bằng nhau, đa dạng dấu hệ số, không nghiệm cấy sẵn.
2. `RAD_07` gọi solver thật qua `mock.patch`.
3. Bất biến 2 tính lại độc lập, cộng bất biến phân hoạch và kiểm tra đủ nghiệm.
4. Số liệu thời gian và số trạng thái khớp log; có ca cho `EMPTY_NO_POSITIVE_INTEGER` và nhánh `sc is None`.
5. Log mutation testing chạy lại trên harness mới.
