# BÁO CÁO TÁI THẨM ĐỊNH KỸ THUẬT ĐỘC LẬP — VÒNG 3 (FINAL RELEASE GATE)

**Dự án:** GeoSolver 2D & CAD Math Studio
**Phiên bản:** v3.1.0-RC3
**Cơ chế:** Round 3 — Final Release Gate
**Kết luận tổng hợp:**
- **Code/Math Gate: PASS** — các lỗi Critical Vòng 2 đã được giải quyết thực chất.
- **Packaging Gate: CONDITIONAL / BLOCKED** — phát hiện mâu thuẫn Critical mới giữa phiên bản Python và dependency; bằng chứng đóng gói chưa thể xác minh độc lập.
- **Quyết định cuối:** **CONDITIONAL APPROVAL TO PACKAGE** — chưa phải **RELEASE PASS** tuyệt đối.

---

## 1. TÓM TẮT ĐIỀU HÀNH

Vòng 3 là bước tiến thực chất so với Vòng 2. Các lỗi Critical về toán học và kiến trúc đã được sửa đúng bản chất, không còn là test-fitting hay placeholder:

- **Hash artifact** không còn là hash chuỗi rỗng; định dạng SHA-256 hợp lệ, kích thước ~32.75 MB phù hợp PyInstaller one-folder.
- **Ellipse** chuyển sang `scipy.special.ellipe` làm ground truth; số liệu khớp tính toán độc lập của Ban Thẩm định ở Vòng 2.
- **Lattice mode** dùng số học nguyên thuần Python (`int` arbitrary precision) — thực sự chống tràn.
- **API tách rời** `classify_triangle_lattice` / `classify_triangle_continuous` — không còn cờ `is_exact_lattice` thiếu validation.
- **DPAPI** zeroize caller buffer, cast `c_void_p`, thêm `CRYPTPROTECT_UI_FORBIDDEN`.

Tuy nhiên, **bằng chứng đóng gói vẫn chưa thể chấp nhận vô điều kiện** vì một mâu thuẫn Critical mới: smoke test báo **Python 3.14.5** nhưng không công bố phiên bản dependency; trong khi Vòng 2 pin **scipy 1.10.1 / numpy 1.24.3 / sympy 1.12 / PyInstaller 6.4.0** — tất cả đều **không tương thích** Python 3.14. Chi tiết tại §4.

---

## 2. XÁC NHẬN GIẢI QUYẾT RC2 CRITICAL

### RC2-C-01 — Hash placeholder: **PROVISIONAL PASS**
- Hash mới `21A54331D66A2A48E218A682F4C3ABDBE2CE201EEEC9872DECA25224BF2A9D97` — 64 ký tự hex hợp lệ.
- Không phải hash chuỗi rỗng (`e3b0c442...`).
- Kích thước `32,754,766 bytes` phù hợp PyInstaller one-folder (~31.23 MiB).
- **Chưa thể xác minh độc lập** vì không có artifact. Cần đối chiếu khi có file.

### RC2-C-02 — Số liệu TV-07 sai: **PASS**

Ban Thẩm định đã tính lại độc lập:

$$
P_{\text{Ram}}(a{=}5,b{=}0.05)\approx 20.0007108,\quad P_{\text{true}}=4a\,E(1-(b/a)^2)\approx 20.0054916
$$

Sai số tương đối:

$$
\frac{20.0054916-20.0007108}{20.0054916}\approx 2.3898\times 10^{-4}=0.0239\%
$$

Khớp chính xác với bảng Round 3. **RC2-C-02 RESOLVED.**

### RC2-C-03 — Simpson giả: **PASS**

`scipy.special.ellipe` được dùng làm ground truth. Đây là chuẩn học thuật (Abramowitz & Stegun 17.3.36; Carlson symmetric forms). **RESOLVED.**

### RC2-C-04 — Lattice overflow: **PASS**

```python
d2_AB = AB[0] * AB[0] + AB[1] * AB[1]   # int * int = arbitrary precision
```

Không có phép nhân float nào trong lattice path. TV-L01 với tọa độ \(10^{200}\) cho \(d^2 \approx 10^{400}\) — Python int xử lý chính xác. **RESOLVED.**

### RC2-C-05 — Cờ `is_exact_lattice` thiếu validation: **PASS**

Hai API tách biệt, `classify_triangle_lattice` kiểm tra `isinstance(pt[0], int)`. **RESOLVED** (minor: `isinstance(True, int)` là `True` — xem RC3-M-02).

---

## 3. XÁC NHẬN GIẢI QUYẾT RC2 HIGH

| Mã | Trạng thái | Ghi chú |
|---|---|---|
| RC2-H-01 (test-fitting 0.3%) | **PARTIAL PASS** | Đổi sang `tol_ratio=0.005` mặc định, viện dẫn "CAD sketch tolerance 0.5%". Có cơ sở hơn nhưng vẫn chưa có test biên 0.49%/0.51%. |
| RC2-H-02 (zeroize caller) | **PARTIAL PASS** | `bytearray` được zeroize qua vòng lặp. Nhưng `bytes(secret_input)` trong `create_string_buffer` tạo **bản sao plaintext thứ ba** không zeroize — xem RC3-M-01. |
| RC2-H-03 (c_void_p cast) | **PASS** | `LocalFree(ctypes.cast(blob_out.pbData, ctypes.c_void_p))`. |
| RC2-H-04 (UI_FORBIDDEN) | **PASS** | Cờ `0x1` được truyền. |
| RC2-H-05 (lattice false-positive) | **PASS** | Tách API. |
| RC2-H-06 (L_max=inf) | **PARTIAL** | Chưa xử lý trường hợp `math.hypot` trả `inf`. |

---

## 4. FINDING CRITICAL MỚI — RC3-C-01

### Phiên bản Python 3.14.5 không tương thích dependency đã pin ở Vòng 2

**Dữ kiện:**

| Nguồn | Python | SciPy | NumPy | SymPy | PyInstaller |
|---|---|---|---|---|---|
| Round 2 | 3.10.11 | 1.10.1 | 1.24.3 | 1.12 | 6.4.0 |
| Round 3 | **3.14.5** | *(không công bố)* | *(không công bố)* | *(không công bố)* | *(không công bố)* |

**Đối chiếu ma trận tương thích chính thức:**

- **SciPy 1.10.1** (04/2023): hỗ trợ Python 3.8–3.11. **Không hỗ trợ 3.14.**
- **NumPy 1.24.3** (04/2023): hỗ trợ Python 3.8–3.11. **Không hỗ trợ 3.14.**
- **SymPy 1.12** (05/2023): hỗ trợ Python 3.8–3.11. **Không hỗ trợ 3.14.**
- **PyInstaller 6.4.0** (03/2024): hỗ trợ tối đa Python 3.12. **Không hỗ trợ 3.14.** Hỗ trợ 3.14 bắt đầu từ **PyInstaller 6.15.0** (10/2025).

**Hệ quả logic:**

1. **Nếu** các dependency đã được nâng cấp (scipy ≥ 1.16, numpy ≥ 2.3, sympy ≥ 1.14, PyInstaller ≥ 6.15) — đây là **thay đổi lớn chưa được công bố**, cần một vòng audit riêng cho regression risk.
2. **Nếu** các dependency vẫn giữ Vòng 2 — **không thể build được** artifact báo Python 3.14.5. Smoke test bị **làm giả hoặc gán nhãn sai**.
3. **Nếu** Python version trong smoke test bị gán nhãn sai — bằng chứng đóng gói **không đáng tin**.

Bất kể nhánh nào, **smoke test không thể dùng làm bằng chứng Release Gate** cho đến khi làm rõ.

**Mức độ:** Critical — blocking cho Packaging Gate.

**Yêu cầu:** Cung cấp `pip freeze` / `conda list` raw từ môi trường build, `PyInstaller --version`, và `python -VV` raw output trên chính VM đã tạo artifact.

---

## 5. FINDINGS MỚI KHÁC

### RC3-M-01 (Medium) — DPAPI: bản sao plaintext thứ ba không zeroize

```python
buf = ctypes.create_string_buffer(bytes(secret_input), length)
```

`bytes(secret_input)` tạo **một đối tượng `bytes` bất biến mới** trong RAM. Đối tượng này **không được zeroize** trong `finally`; nó tồn tại cho đến khi GC thu hồi, có thể bị copy bởi allocator. Với API "bảo vệ bí mật", đây là rò rỉ tàn dư.

**Khuyến nghị:** Dùng `ctypes.create_string_buffer(length)` rồi `ctypes.memmove(buf, secret_input, length)` để tránh `bytes(...)`.

### RC3-M-02 (Medium) — `isinstance(x, int)` chấp nhận `bool`

`isinstance(True, int)` là `True` trong Python. Nếu caller truyền `(True, False)` cho `classify_triangle_lattice`, code chấp nhận và tính toán với `1`/`0` thay vì từ chối. Cần `type(x) is int` hoặc `not isinstance(x, bool)`.

### RC3-M-03 (Low) — Nhãn dung lượng

`32,754,766 bytes = 31.235 MiB = 32.755 MB`. Hồ sơ ghi "~31.23 MB" là nhầm nhãn MiB → MB. Không ảnh hưởng toán học nhưng phản ánh thiếu cẩn trọng.

### RC3-M-04 (Medium) — Không công bố PyInstaller version

Không có trong smoke test Round 3. Với Python 3.14 yêu cầu PyInstaller ≥ 6.15.

### RC3-M-05 (Medium) — Vẫn thiếu chữ ký số và SBOM

Không có code signing certificate, không có CycloneDX/SPDX SBOM, không có hash của toàn bộ file trong `dist/GeoSolver/` (chỉ hash `.exe`, chưa có `_internal/*.dll`).

---

## 6. ĐỐI SOÁT ĐỘC LẬP TEST VECTOR VÒNG 3

| Mã | Xác minh độc lập | Kết luận |
|---|---|---|
| **TV-L01** | \(A(0,0),B(10^{200},0),C(0,10^{200})\); \(d^2_{AB}=d^2_{CA}=10^{400}\), \(d^2_{BC}=2\cdot 10^{400}\); `dot_A = 0` chính xác nguyên; `right_isosceles`. | **PASS** |
| **TV-L02** | `10864*sqrt(3)` là float → `isinstance(float, int) = False` → `TypeError`. | **PASS** |
| **TV-L03** | \(d^2=\{1000,650,1010\}\), đôi một khác → `scalene`. | **PASS** |
| **TV-C01** | \(A(0,0),B(21728,0),C(10864,18816.99997)\); \(d_{AB}=21728\), \(d_{AC}\approx 21728.0002\), \(d_{BC}\approx 21728.0002\); \(\Delta\approx 2\times10^{-4}\ll \text{tol}=108.64\); `equilateral`. | **PASS** |
| **TV-C02** | \(\Delta_{CA\text{-}AB}=0.01577\), \(\text{tol}=0.005\cdot 3.178=0.01589\), \(0.01577\le 0.01589\) → `isosceles`. \(\min\cos\approx 0.397 > 0.015\) → không right. | **PASS** |
| **TV-C03** | \(\text{tol}=0.003\cdot 3.178=0.009534\), \(\Delta=0.01577 > \text{tol}\) → `scalene`. | **PASS** |
| **TV-E01** | \(P_{\text{Ram}}=20.0007108\), \(P_{\text{true}}=20.0054916\), sai số \(0.023898\%\). | **PASS** |

**Toàn bộ 7/7 test vector Vòng 3 khớp tính toán độc lập.** Đây là điểm khác biệt rõ rệt so với Vòng 2.

---

## 7. ĐÁNH GIÁ DPAPI — KẾT LUẬN

**Đã đạt:**
- `bytearray` caller được zeroize qua vòng lặp `for i in range(length): secret_input[i] = 0`.
- `buf` (ctypes buffer) được zeroize qua `ctypes.memset`.
- `CRYPTPROTECT_UI_FORBIDDEN = 0x1` được truyền.
- `LocalFree` có cast `c_void_p` tường minh.
- `GetLastError` được đọc khi fail.
- `blob_out.pbData == NULL` được kiểm tra.

**Chưa đạt:**
- `bytes(secret_input)` — bản sao plaintext thứ ba — không được zeroize (RC3-M-01).
- Không document giới hạn zeroization của Python GC.

**Kết luận:** **Đạt yêu cầu phát hành có điều kiện** — cần sửa RC3-M-01 hoặc document rõ ràng.

---

## 8. ĐÁNH GIÁ BẰNG CHỨNG ĐÓNG GÓI

| Yếu tố | Trạng thái |
|---|---|
| Hash SHA-256 định dạng hợp lệ | ✅ |
| Không phải hash chuỗi rỗng | ✅ |
| Kích thước hợp lý | ✅ |
| `frozen: true` | ✅ |
| `exit_code: 0` | ✅ |
| **Tương thích Python 3.14.5 ↔ dependency** | ❌ **RC3-C-01** |
| **PyInstaller version công bố** | ❌ |
| **Chữ ký số (code signing)** | ❌ |
| **SBOM** | ❌ |
| **Hash của `_internal/*.dll`** | ❌ |
| **Xác minh độc lập hash** | ⏸ Chưa thể (không có artifact) |

---

## 9. QUYẾT ĐỊNH GATE VÀ ĐIỀU KIỆN

### **CONDITIONAL APPROVAL TO PACKAGE**
### Code/Math Gate: **PASS**
### Packaging Gate: **CONDITIONAL — BLOCKED until RC3-C-01 resolved**

### Điều kiện bắt buộc trước khi **RELEASE PASS**:

1. **Giải trình RC3-C-01:** Cung cấp `pip freeze`, `python -VV`, `PyInstaller --version` raw từ chính VM đã tạo artifact. Xác nhận dependency thực tế.
2. **Nếu dependency đã nâng cấp:** Cung cấp test suite chạy lại trên bộ dependency mới, xác nhận không regression. Đây là audit bổ sung.
3. **Nếu Python version bị gán nhãn sai:** Sửa smoke test, cung cấp lại hash thật của artifact đúng.
4. **Chữ ký số:** Ký artifact bằng certificate (EV hoặc OV) và cung cấp chuỗi chứng thư.
5. **SBOM:** CycloneDX hoặc SPDX cho toàn bộ dependency + DLL bundled.
6. **Hash toàn bộ `dist/GeoSolver/`:** Manifest SHA-256 cho từng file.
7. **Sửa RC3-M-01:** Dùng `ctypes.memmove` thay `bytes(secret_input)`.
8. **Sửa RC3-M-02:** Đổi `isinstance(x, int)` thành `type(x) is int`.
9. **Bổ sung test biên dung sai:** 0.49%, 0.51%, 0.4%, 0.6% ở `tol_ratio=0.005`.

---

## 10. PHẠM VI VÀ GIỚI HẠN

Báo cáo này dựa trên dossier Vòng 3 được cung cấp. Không xác minh được:
- Sự tồn tại thực tế của `D:\AI DATA\STEM_APP\dist\GeoSolver\GeoSolver.exe`.
- Nội dung thực của `smoke_test_result.json` trên ổ đĩa.
- Hash SHA-256 có khớp file thật hay không.

Các điểm này cần được xác minh khi có artifact hoặc qua kênh độc lập (ví dụ: gửi file cho Ban Thẩm định).

---

**TRẠNG THÁI CUỐI:**
- **Code/Math:** PASS — Round 2 Critical resolved.
- **Packaging:** CONDITIONAL — RC3-C-01 blocking.
- **Quyết định:** **CONDITIONAL APPROVAL TO PACKAGE — NOT YET RELEASE PASS.**