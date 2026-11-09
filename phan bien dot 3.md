# BÁO CÁO THẨM ĐỊNH KỸ THUẬT ĐỘC LẬP

**Dự án:** GeoSolver 2D & CAD Math Studio  
**Phiên bản:** v3.1.0-RC  
**Cơ chế:** Pre-Packaging Release Gate  
**Vai trò thẩm định:** Independent Peer Review Board  
**Thành phần Ban Thẩm định:**
1. Nhà Toán học Tính toán & Hình học Giải tích
2. Kỹ sư Tối ưu hóa & Ổn định Mã nguồn
3. Chuyên gia Kỹ thuật Đóng gói & Phát hành Windows

---

## KẾT LUẬN GATE

**Kết luận gate:** **FAIL — REJECT WITH REASONS**  
**Quyết định:** **KHÔNG KÝ DUYỆT ĐÓNG GÓI / KHÔNG APPROVED TO PACKAGE**  
**Trạng thái:** **BLOCKED FOR RELEASE — FAIL GATE**

---

## 1. XÁC NHẬN TRẠNG THÁI HỒ SƠ

Đã nhận dossier. Tuy nhiên **không thể xác nhận UNBLOCKED để ký duyệt**, vì hồ sơ vẫn thiếu artifact bắt buộc và có lỗi Critical trong chính mã nguồn/test vector được cung cấp.

Trạng thái đúng: **đã mở thẩm định, nhưng gate FAIL**.

---

## 2. FINDINGS CRITICAL

### C-01. TV-03 là false PASS — mã nguồn phân loại sai tam giác Scalene thành Isosceles

Với \(k=1\), đầu vào TV-03 là:

\[
A(0,0),\ B(1,3),\ C(2.9,1.3)
\]

Tính độc lập:

\[
d_{AB}=\sqrt{10}\approx 3.162277660
\]

\[
d_{CA}=\sqrt{10.1}\approx 3.178049716
\]

\[
L_{\max}=3.178049716
\]

\[
\text{tol}_{eq}=\max(10^{-4},0.006\cdot L_{\max})=0.019068298
\]

\[
|d_{CA}-d_{AB}|=0.015772056 \le \text{tol}_{eq}
\]

Trong `classify_triangle`, nhánh `elif diff_CA_AB <= tol_eq` được kích hoạt, gán:

```python
is_isosceles = True
iso_vertex = "A"
```

Do đó `tri_type` trả về **`isosceles`**, không phải `scalene`.

Với \(k=2\): diff \(\approx 0.0015772\), tol \(\approx 0.0019068\) → vẫn Isosceles.  
Với \(k=3\): diff \(\approx 0.00001577\), tol \(=10^{-4}\) → vẫn Isosceles.

**TV-03 FAIL từ \(k=1\) đến \(k=3\)**, trái với bảng “PASS toàn bộ \(k\)”.

**Mức độ:** Critical — test vector đối soát toán học bị báo sai.

---

### C-02. “Định lý Lưới nguyên” đúng về lý thuyết nhưng implementation `all_int` sai bản chất

Chứng minh không tồn tại tam giác đều với 3 đỉnh thuộc \(\mathbb{Z}^2\) là đúng. Nhưng code dùng:

```python
all_int = all(abs(c - round(c)) < 1e-4 for c in (...))
```

Đây **không phải kiểm tra \(\mathbb{Z}^2\) chính xác**, mà là “gần số nguyên trong 1e-4”. Điều này phá vỡ bất biến.

Counterexample cụ thể:

\[
A=(0,0),\quad B=(21728,0),\quad C=(10864,\ 10864\sqrt{3})
\]

với

\[
10864\sqrt{3}\approx 18816.999973428
\]

là tam giác đều chính xác. Tọa độ \(C_y\) cách số nguyên \(18817\) chỉ \(2.657\times 10^{-5}<10^{-4}\), nên `all_int=True`. Khi đó code cưỡng bức:

```python
is_equilateral = False
```

và có thể trả về `scalene` hoặc bỏ sót equilateral. Đây là lỗi Critical vì định lý chỉ áp dụng cho tọa độ nguyên chính xác, không áp dụng cho xấp xỉ.

**Mức độ:** Critical — phân loại sai tam giác đều.

---

### C-03. Smoke test đóng gói không chứng minh được bản frozen

JSON smoke test ghi:

```json
"frozen": false
```

Với release Windows dùng PyInstaller, smoke test bắt buộc phải chạy trên **executable đã đóng gói**. `frozen:false` cho thấy test có thể chạy từ source hoặc môi trường dev, không đại diện cho artifact phát hành. Không có hash, log raw, ảnh chụp VM sạch, mã exit của từng check.

**Mức độ:** Critical — không đủ bằng chứng Packaging Gate.

---

### C-04. Thiếu mã nguồn module Elip

Dossier chỉ có mã `classify_triangle` và `encrypt_secret_dpapi`. Không có implementation cho:

- Ramanujan II perimeter.
- Xử lý suy biến \(b=0\), \(a=0\), \(a=b=0\).
- Simpson reference.

Do đó **TV-06 và TV-07 không thể thẩm định**. Bảng kết quả không phải bằng chứng audit.

**Mức độ:** Critical — thiếu artifact bắt buộc.

---

### C-05. Xử lý tràn số không hoàn chỉnh

`math.hypot` tránh tràn khi tính khoảng cách, nhưng sau đó code vẫn dùng:

```python
abs(cross_product) <= 1e-5 * (L_max ** 2)
```

Nếu \(L_{\max}>10^{154}\), `L_max ** 2` có thể tràn thành `inf`, khiến mọi tam giác lớn bị đánh dấu `degenerate`. Ngoài ra `math.hypot` vẫn có thể lỗi chuyển đổi nếu tọa độ Python int vượt miền float. Tuyên bố “chống tràn > \(10^{154}\)” chưa được chứng minh.

**Mức độ:** Critical đối với miền tọa độ cực lớn.

---

## 3. FINDINGS HIGH

### H-01. DPAPI: không có UAF trực tiếp nhưng chưa đạt yêu cầu bảo mật

Đoạn `encrypt_secret_dpapi` giữ `buf` sống trong suốt lệnh gọi, nên **không thấy Use-After-Free trực tiếp** trong snippet. Tuy nhiên:

- Không zeroize plaintext sau khi dùng (`SecureZeroMemory`/`ctypes.memset`).
- `create_string_buffer(data)` tạo bản sao plaintext; bản gốc `data` vẫn tồn tại.
- `LocalFree` không được khai báo `argtypes/restype`, không kiểm tra return.
- Không kiểm tra `GetLastError` khi `CryptProtectData` fail.
- Không xử lý `blob_out.pbData == NULL`.

**Mức độ:** High — cần hardening trước phát hành.

---

### H-02. `all_int` + so sánh `dot == 0` không nhất quán

Khi `all_int=True` do dung sai, code lại dùng:

```python
if dot_A == 0:
```

So sánh exact trên giá trị float gần nguyên là không ổn định. Cần tách rõ hai chế độ: tọa độ nguyên chính xác dùng số học nguyên; tọa độ thực dùng dung sai hình học nhất quán.

**Mức độ:** High.

---

### H-03. Đóng gói thiếu pin version/hash/SBOM

“Ghim chặt” nhưng không có version cụ thể cho Python, PyInstaller, numpy, sympy, scipy. `ctypes.wintypes` là stdlib, không phải binary dependency. Không có SHA-256 artifact, không có SBOM, không có chữ ký số.

**Mức độ:** High.

---

### H-04. Elip suy biến chưa đầy đủ

Công thức chỉ xử lý \(b=0\). Trường hợp \(a=0,b>0\) hoặc \(a=b=0\) chưa được đặc tả. Với \(a=0,b=5\), công thức Ramanujan không trả đúng \(4b=20\).

**Mức độ:** High.

---

## 4. ĐỐI SOÁT TEST VECTOR ĐỘC LẬP

| Mã Test | Kết quả thẩm định | Ghi chú |
|---|---|---|
| TV-01 | **PASS** | \(AB=BC=CA=6\); non-integer nên đi nhánh tolerance, `equilateral=True`. |
| TV-02 | **PASS** | \(AB=CA=\sqrt{34}\), \(BC=6\); `isosceles` tại A. |
| TV-03 | **FAIL** | \(k=1,2,3\) trả `isosceles` do dung sai \(0.6\%L_{\max}\) và floor \(10^{-4}\). |
| TV-04 | **PASS** | \(AB=CA=4\), \(BC=4\sqrt2\), \(\dot A=0\); `right_isosceles` tại A. |
| TV-05 | **PASS** | Cross = 0; `degenerate`. |
| TV-06 | **KHÔNG THỂ THẨM ĐỊNH** | Không có code elip. |
| TV-07 | **KHÔNG THỂ THẨM ĐỊNH** | Không có code elip/Simpson log. |

---

## 5. TRẢ LỜI TRỰC TIẾP 4 YÊU CẦU

### 5.1. UNBLOCKED?

**Không.** Hồ sơ đã được mở nhưng chưa đủ điều kiện UNBLOCKED để ký duyệt. Còn thiếu code elip, frozen smoke test, pin dependency/hash, và có lỗi Critical.

### 5.2. Đối soát TV-01 → TV-07?

Đã thực hiện. Kết quả: TV-01, 02, 04, 05 PASS; **TV-03 FAIL**; TV-06, 07 không thể thẩm định do thiếu implementation.

### 5.3. Đánh giá `encrypt_secret_dpapi`?

Không phát hiện UAF trực tiếp trong snippet vì buffer còn sống. Nhưng **không đạt yêu cầu bảo mật phát hành** do thiếu zeroization, thiếu kiểm tra lỗi `LocalFree`/`GetLastError`, thiếu `argtypes/restype`.

### 5.4. Quyết định cuối cùng?

**REJECT WITH REASONS — NOT APPROVED TO PACKAGE.**

---

## 6. ĐIỀU KIỆN TỐI THIỂU ĐỂ MỞ LẠI GATE

1. Sửa `all_int` thành kiểm tra số nguyên chính xác; không áp dụng định lý lưới nguyên cho xấp xỉ.
2. Sửa TV-03 hoặc siết dung sai; bổ sung test vector phản hồi cho trường hợp suýt cân.
3. Cung cấp code elip + log Simpson + test vector raw.
4. Chạy smoke test trên frozen executable, có hash, log, VM sạch.
5. Pin version/hash toàn bộ dependency; cung cấp SBOM và artifact tree.
6. Hardening DPAPI: zeroize plaintext, kiểm tra `LocalFree`, khai báo `argtypes/restype`.
7. Chứng minh xử lý tràn số tại \(>10^{154}\) bằng test cụ thể.

---

## 7. PHẠM VI VÀ GIỚI HẠN CỦA BÁO CÁO

Báo cáo này chỉ dựa trên dossier được cung cấp trong file bàn giao thẩm định. Không có kết luận nào về các phần mã nguồn, module, asset, dependency hoặc artifact không được cung cấp.

Báo cáo không cấp quyền phát hành. Mọi thay đổi sau thời điểm thẩm định phải được đệ trình lại cho Ban Thẩm định.

---

**TRẠNG THÁI CUỐI:** **BLOCKED FOR RELEASE — FAIL GATE**