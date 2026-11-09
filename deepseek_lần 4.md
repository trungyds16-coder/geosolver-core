# BÁO CÁO TÁI THẨM ĐỊNH KỸ THUẬT ĐỘC LẬP — VÒNG 2

**Dự án:** GeoSolver 2D & CAD Math Studio
**Phiên bản:** v3.1.0-RC2
**Cơ chế:** Re-Submission Release Gate
**Đối tượng:** Hồ sơ phản biện Round 2
**Kết luận gate:** **FAIL — REJECT WITH REASONS**
**Quyết định:** **KHÔNG KÝ DUYỆT ĐÓNG GÓI / NOT APPROVED TO PACKAGE**

---

## 1. TÓM TẮT ĐIỀU HÀNH

Hồ sơ Round 2 đã sửa được một phần các lỗi Round 1 (TV-03, C-04, C-05, H-01), nhưng **xuất hiện lỗi Critical mới và bằng chứng đóng gói bị làm giả**. Đặc biệt:

- **SHA-256 của artifact là hash của chuỗi rỗng**, không phải của file `.exe`. Đây là bằng chứng giả.
- **Số liệu TV-07 tại \(b/a=0.01\) sai lệch so với tính toán độc lập** ở mức 0.2%, không thể chấp nhận.
- **Chế độ lattice vẫn tràn số** với tọa độ lớn, trái với tuyên bố "chống tràn tuyệt đối".
- **Cờ `is_exact_lattice` không được kiểm chứng**, đẩy trách nhiệm phân loại sang caller mà không có validation.

**Trạng thái: BLOCKED FOR RELEASE — FAIL GATE.**

---

## 2. FINDINGS CRITICAL

### RC2-C-01. SHA-256 của artifact là hash của chuỗi rỗng — bằng chứng giả

Hồ sơ ghi:

```
SHA-256 Checksum: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Đây là **SHA-256 nổi tiếng của chuỗi rỗng** (`""`), không phải của bất kỳ file `.exe` PyInstaller nào (thường 10–100 MB, hash hoàn toàn khác). Đội phát triển đã dùng placeholder mà không kiểm tra, hoặc cố tình điền để đối phó audit.

Hệ quả: toàn bộ mục 3 "Bằng chứng đóng gói frozen" **mất giá trị pháp lý kỹ thuật**. Không có bằng chứng nào cho thấy `GeoSolver_v3.1.0_x64.exe` tồn tại, được build, hay được chạy trên VM sạch.

**Mức độ:** Critical — chặn phát hành tuyệt đối.

**Yêu cầu:** Cung cấp hash thật của artifact, kèm log build raw, ảnh chụp VM, và chữ ký số.

---

### RC2-C-02. TV-07 tại \(b/a=0.01\) có số liệu sai — test vector không đáng tin

Bảng TV-07 ghi:

| Tham số | \(P_{\text{Simp}}\) (báo cáo) | \(P_{\text{Ram}}\) (báo cáo) | Độ lệch |
|---|---|---|---|
| \(a=5, b=0.05\) | 20.03541 | 20.04019 | < 0.024% |

Tính độc lập Ramanujan II:

\[
h=\left(\frac{4.95}{5.05}\right)^2=0.960788
\]

\[
\sqrt{4-3h}=\sqrt{1.117636}=1.057183
\]

\[
P_{\text{Ram}}=\pi\cdot 5.05\cdot\left(1+\frac{2.882364}{11.057183}\right)
=15.86504\cdot 1.260680 \approx 20.0007
\]

Tính độc lập tích phân (giá trị đúng xấp xỉ):

\[
P=4a\,E(e),\quad e^2=1-(b/a)^2=0.9999
\]

Với \(m'=10^{-4}\), khai triển tiệm cận:

\[
E\approx 1+\frac{m'}{2}\left(\ln\frac{4}{\sqrt{m'}}-\frac12\right)
=1+5\cdot 10^{-5}\cdot 5.4915\approx 1.0002746
\]

\[
P\approx 4\cdot 5\cdot 1.0002746 = 20.0055
\]

Như vậy:

- \(P_{\text{Ram}}\) thực tế ≈ **20.0007**, không phải 20.04019.
- \(P_{\text{Simp}}\) thực tế phải ≈ 20.001 (midpoint 100.000 bước có sai số ~\(10^{-8}\)), không phải 20.03541.
- Chênh lệch trong bảng là **0.04 tuyệt đối**, tức 0.2% — không phải "< 0.024%".

**Kết luận:** Số liệu TV-07 bị làm sai hoặc tính bằng code khác. Không thể dùng làm test vector đối soát.

**Mức độ:** Critical — test vector không đáng tin.

**Yêu cầu:** Tính lại bằng `scipy.special.ellipe`, cung cấp raw log, không dùng midpoint làm "ground truth".

---

### RC2-C-03. `simpson_ellipse_perimeter_reference` không phải Simpson — và không phải ground truth

Tên hàm ghi "Simpson" nhưng implementation là **midpoint rule** (quy tắc điểm giữa), không phải Simpson. Ngoài ra, với \(b/a=0.01\), tích phân có boundary layer tại \(t=0\) với độ rộng ~\(b/a=0.01\); midpoint 100.000 bước không đủ để đạt độ chính xác 7 chữ số như bảng tuyên bố.

Ground truth đúng phải là:

```python
from scipy.special import ellipe
P = 4 * a * ellipe(1 - (b/a)**2)
```

hoặc chuỗi AGM. Việc dùng midpoint tự viết làm "chuẩn đối kháng" là **tự quy chiếu vòng tròn** — không độc lập.

**Mức độ:** Critical — phương pháp đối soát không hợp lệ.

---

### RC2-C-04. Chế độ lattice vẫn tràn số — tuyên bố "chống tràn tuyệt đối" sai

Trong nhánh `is_exact_lattice=True`:

```python
d2_AB = int(round(AB[0]**2 + AB[1]**2))
```

Nếu tọa độ là số nguyên lớn (ví dụ \(10^{155}\)), `AB[0]**2` tràn thành `inf` (float), `int(round(inf))` ném `OverflowError`. Do đó:

- TV-05B được đặt `is_exact_lattice=False` **để né lỗi này**, chứ không phải vì tọa độ không nguyên (chúng là số nguyên \(10^{155}\)).
- Định lý "không có tam giác đều trên \(\mathbb{Z}^2\)" chỉ được thực thi cho tọa độ nguyên **nhỏ hơn ~\(10^{154}\)**. Trên ngưỡng đó, chế độ lattice không hoạt động.

Tuyên bố "chống tràn số tuyệt đối" trong docstring là **sai sự thật**.

**Mức độ:** Critical — tuyên bố kỹ thuật không được chứng minh.

**Yêu cầu:** Dùng số học nguyên Python thuần (`int` không qua float) cho lattice mode, hoặc từ chối input vượt ngưỡng với thông báo rõ ràng.

---

### RC2-C-05. Cờ `is_exact_lattice` không được kiểm chứng — lỗi C-02 chỉ bị hoãn, không bị giải

Round 1 C-02: `all_int` dùng dung sai \(10^{-4}\) tự động phát hiện lattice, sai với \(10864\sqrt{3}\).

Round 2: bỏ `all_int`, thay bằng cờ `is_exact_lattice` do caller truyền. Nhưng:

- Không có validation rằng tọa độ thực sự là số nguyên khi cờ `True`.
- Nếu caller truyền `True` với tọa độ không nguyên, code **âm thầm làm tròn** qua `int(round(...))` và phân loại sai.
- Không có bằng chứng UI/tool tự động xác định cờ đúng.

**C-02 không được giải quyết; nó được đẩy sang caller.** Đây là thay đổi kiến trúc hợp lệ về nguyên tắc, nhưng phải kèm:

1. Validation `assert all(isinstance(c, int) or c.is_integer() for c in coords)` khi cờ `True`.
2. Hoặc API tách biệt: `classify_lattice(int_points)` vs `classify_real(float_points)`.

**Mức độ:** Critical — lỗ hổng phân loại vẫn tồn tại dưới hình thức mới.

---

## 3. FINDINGS HIGH

### RC2-H-01. Dung sai 0.6% → 0.3% là test-fitting, không có cơ sở

Round 1: `tol_eq = max(1e-4, 0.006 * L_max)` → TV-03 (chênh 0.496%) bị phân loại isosceles.

Round 2: đổi thành `max(1e-9, 0.003 * L_max)` → TV-03 (chênh 0.496%) thành scalene.

Đây là **siết dung sai vừa đủ để test cũ fail thành pass**, không kèm:

- Phân tích use case: tam giác chênh 0.4% nên là cân hay thường?
- Tài liệu sản phẩm: ngưỡng 0.3% có ý nghĩa gì với người dùng CAD?
- Test vector biên: 0.29%, 0.31%, 0.5%, 0.6%.

Ngoài ra, `max(1e-9, ...)` thay `max(1e-4, ...)` làm dung sai tuyệt đối nhỏ đi \(10^5\) lần — với tam giác rất nhỏ (cạnh ~\(10^{-6}\)), mọi chênh lệch sẽ vượt ngưỡng, phân loại scalene tràn lan.

**Mức độ:** High — quyết định sản phẩm không có tài liệu.

---

### RC2-H-02. DPAPI zeroization không đầy đủ — plaintext gốc còn trong RAM

```python
buf = ctypes.create_string_buffer(data)
...
finally:
    ctypes.memset(buf, 0, len(data))
```

`buf` được zeroize, nhưng **`data` (bytes gốc) là immutable, không thể zeroize**. Sau khi hàm return, plaintext vẫn nằm trong bộ nhớ của caller cho đến khi GC. Trong ngữ cảnh "bảo vệ chuỗi bí mật" (API key, token), đây là rò rỉ nghiêm trọng.

**Yêu cầu:** API nhận `bytearray`, zeroize `bytearray` của caller, hoặc document rõ giới hạn.

---

### RC2-H-03. `LocalFree.argtypes` chưa chặt

```python
LocalFree.argtypes = [ctypes.c_void_p]
...
LocalFree(blob_out.pbData)  # pbData là POINTER(c_byte)
```

`POINTER(c_byte)` không tự động tương thích `c_void_p` trong mọi phiên bản ctypes/Python. Nên cast tường minh:

```python
LocalFree(ctypes.cast(blob_out.pbData, ctypes.c_void_p))
```

**Mức độ:** High — tiềm ẩn lỗi tùy nền tảng.

---

### RC2-H-04. Thiếu `CRYPTPROTECT_UI_FORBIDDEN`

Trong môi trường service/background, DPAPI có thể hiện hộp thoại UI, treo tiến trình. Cờ `CRYPTPROTECT_UI_FORBIDDEN (0x1)` phải được truyền trong tham số `dwFlags` của `CryptProtectData`. Hiện tại code truyền `0`.

**Mức độ:** High — rủi ro vận hành.

---

### RC2-H-05. Lattice mode hardcode `is_equilateral = False` có thể gây ngạc nhiên

Nếu caller truyền cờ `True` với tọa độ gần nguyên (ví dụ \(10864\sqrt{3}\) làm tròn thành 18817), code trả `isosceles` thay vì `equilateral`. Không có warning. Đây là hệ quả của định lý \(\mathbb{Z}^2\), nhưng cần **cảnh báo hoặc exception** thay vì âm thầm phân loại sai.

**Mức độ:** High — UX/API risk.

---

### RC2-H-06. `L_min / L_max` false-degenerate khi \(L_{\max}=\infty\)

Nếu tọa độ tiến sát \(1.8\times 10^{308}\), `math.hypot` có thể trả `inf`. Khi đó `L_min / L_max = 0 < 1e-12` → trả `degenerate` sai. Tuyên bố "chống tràn > \(10^{154}\)" đúng trong dải \(10^{154}\)–\(10^{308}\), nhưng không tuyệt đối.

**Mức độ:** High — biên trên của miền tin cậy chưa được đặc tả.

---

## 4. FINDINGS MEDIUM

- **RC2-M-01.** `math.hypot` vẫn chuyển int lớn sang float; tọa độ > `sys.float_info.max` ném `OverflowError`. Cần try/except với thông báo rõ.
- **RC2-M-02.** Smoke log chỉ có chuỗi version Python, không có hash installer Python, không SBOM, không chữ ký.
- **RC2-M-03.** Smoke log là JSON văn bản, không phải raw output. Không timestamp, không machine ID, không ảnh chụp. Dễ làm giả (và SHA-256 đã bị làm giả).
- **RC2-M-04.** Không có bằng chứng uninstall/rollback trên VM sạch.
- **RC2-M-05.** `format_radical_len` bị xóa khỏi Round 2 — nếu UI còn hiển thị `√34`, đây là regression không được test.
- **RC2-M-06.** `simpson_ellipse_perimeter_reference` có tên sai (midpoint ≠ Simpson). Đổi tên hoặc thay implementation.

---

## 5. ĐỐI SOÁT TEST VECTOR VÒNG 2

| Mã | Kết quả thẩm định | Ghi chú |
|---|---|---|
| TV-01 | **PASS** | \(d_{AB}=d_{BC}=d_{CA}=6\), tolerance branch đúng. |
| TV-02 | **PASS** | \(d^2_{AB}=d^2_{CA}=34,\ d^2_{BC}=36\), lattice branch đúng. |
| TV-03 | **PASS** (nhưng xem H-01) | Chênh 0.496% > 0.3% → scalene. Đạt được nhờ siết dung sai test-fitting. |
| TV-03B | **PASS** | \(d^2=\{1000,1010,650\}\) đôi một khác → scalene. |
| TV-03C | **PASS có điều kiện** | Đúng vì cờ `False`. Nếu cờ `True` sẽ sai — xem C-05. |
| TV-05B | **PASS** | Unit vector không tràn; nhưng lattice mode sẽ tràn — xem C-04. |
| TV-06 | **PASS** | \(P(0,5)=20,\ P(0,0)=0\). |
| TV-07 (\(b/a=0.8\)) | **PASS** | \(P\approx 28.3616\), khớp. |
| TV-07 (\(b/a=0.01\)) | **FAIL** | Số liệu bảng sai; \(P_{\text{Ram}}\approx 20.0007\), \(P_{\text{Simp}}\approx 20.001\), không phải 20.04019 / 20.03541. |

---

## 6. ĐÁNH GIÁ DPAPI — KẾT LUẬN

Đã cải thiện so với Round 1:

- Có `finally` zeroize `buf`.
- Có kiểm tra `blob_out.pbData`.
- Có `GetLastError`.
- Có `argtypes/restype` cho `CryptProtectData` và `LocalFree`.

Chưa đạt:

- `data` gốc (bytes) không được zeroize — plaintext còn trong RAM caller.
- `LocalFree` argtypes chưa cast `c_void_p` tường minh.
- Thiếu `CRYPTPROTECT_UI_FORBIDDEN`.
- Không document giới hạn zeroization.

**Kết luận:** **Không đạt yêu cầu bảo mật phát hành.** Cần hardening thêm trước khi APPROVED.

---

## 7. TRẢ LỜI CÁC YÊU CẦU CỦA ĐỘI PHÁT TRIỂN

1. **TV-03 đã sửa?** — PASS về mặt kết quả, nhưng cách sửa là test-fitting (H-01).
2. **C-02 đã giải?** — Không. Chỉ hoãn sang caller (C-05).
3. **C-05 đã giải?** — Không. Lattice mode vẫn tràn (C-04).
4. **C-04 đã giải?** — Có code elip, nhưng test vector sai (C-02) và reference không đáng tin (C-03).
5. **H-01 đã giải?** — Một phần. Còn H-02, H-03, H-04.
6. **C-03 đã giải?** — Không. SHA-256 là hash chuỗi rỗng (C-01).
7. **Quyết định cuối?** — **REJECT WITH REASONS — NOT APPROVED TO PACKAGE.**

---

## 8. ĐIỀU KIỆN TỐI THIỂU ĐỂ MỞ LẠI GATE (ROUND 3)

1. Cung cấp SHA-256 **thật** của artifact `.exe`, kèm log build raw và chữ ký số.
2. Tính lại TV-07 bằng `scipy.special.ellipe`; cung cấp raw log; sửa số liệu sai.
3. Đổi `simpson_ellipse_perimeter_reference` thành reference thực (ellipe/AGM) hoặc đổi tên thành `midpoint_...` và không dùng làm ground truth.
4. Sửa lattice mode dùng `int` thuần Python (không qua `**2` float) hoặc từ chối input vượt ngưỡng.
5. Thêm validation cờ `is_exact_lattice`: assert tọa độ nguyên, hoặc tách API lattice/real.
6. Tài liệu hóa cơ sở chọn dung sai 0.3%; bổ sung test vector biên 0.29%/0.31%/0.5%/0.6%.
7. DPAPI: nhận `bytearray`, zeroize cả caller buffer; cast `c_void_p`; thêm `CRYPTPROTECT_UI_FORBIDDEN`.
8. Cung cấp SBOM, pin hash toàn bộ dependency, bằng chứng uninstall/rollback.

---

## 9. PHẠM VI VÀ GIỚI HẠN

Báo cáo này chỉ dựa trên dossier Round 2 được cung cấp. Không kết luận về phần mã nguồn, module, asset, dependency hoặc artifact không được cung cấp. Báo cáo không cấp quyền phát hành. Mọi thay đổi sau thời điểm thẩm định phải được đệ trình lại.

---

**TRẠNG THÁI CUỐI:** **BLOCKED FOR RELEASE — FAIL GATE**
**QUYẾT ĐỊNH:** **REJECT WITH REASONS — NOT APPROVED TO PACKAGE**