# BÁO CÁO TÁI THẨM ĐỊNH KỸ THUẬT ĐỘC LẬP — VÒNG 4 (FINAL RELEASE GATE)

**Dự án:** GeoSolver 2D & CAD Math Studio
**Phiên bản:** v3.1.0-RC4
**Cơ chế:** Round 4 — Final Release Gate
**Kết luận gate:** **FAIL — REJECT WITH REASONS**
**Quyết định:** **NOT APPROVED FOR DISTRIBUTION**

---

## 1. TÓM TẮT ĐIỀU HÀNH

Hồ sơ Vòng 4 đã giải quyết đúng hướng một số điều kiện Round 3 (môi trường Python 3.14.5 + PyInstaller 6.22.3 + SciPy 1.18.1 + NumPy 2.5.4 được công bố; `ctypes.memmove` thay `bytes()`; `type(x) is int` chặn bool). Tuy nhiên, Ban Thẩm định phát hiện **06 lỗi Critical mới**, trong đó có:

1. **Test vector TV-TOL-01 và TV-TOL-02 bị làm sai** — mã nguồn không sản sinh kết quả như bảng tuyên bố.
2. **Regression: kiểm tra `blob_out.pbData == NULL` bị xóa** khỏi hàm DPAPI so với Round 3.
3. **Cấu trúc đóng gói không nhất quán** với PyInstaller 6.x.
4. **Lịch sử evidence Vòng 2 được xác nhận là fabricated/không thể tái lập**.
5. **Chữ ký số vẫn thiếu** — Release Gate không thể pass.
6. **DLL hash không thể xác minh độc lập** do không có artifact.

Kết luận: **FAIL GATE** — hồ sơ chưa đủ điều kiện ký duyệt phát hành.

---

## 2. FINDINGS CRITICAL

### RC4-C-01. TV-TOL-01 và TV-TOL-02 là test vector fabricated — mã nguồn không trả kết quả như tuyên bố

Đội phát triển tuyên bố:

| Mã | Input (đội phát triển nêu) | Kết quả họ tuyên bố |
|---|---|---|
| TV-TOL-01 | AB=100.0, BC=100.0, CA=100.49, `tol_ratio=0.005` | `type: isosceles` |
| TV-TOL-02 | AB=100.0, BC=100.0, CA=100.51, `tol_ratio=0.005` | `type: scalene` |

**Đối soát độc lập với chính mã `classify_triangle_continuous` trong §2 dossier Round 3/4:**

#### TV-TOL-01

- \(L_{\max} = 100.49\)
- \(\text{tol} = 0.005 \cdot 100.49 = 0.50245\)
- \(|d_{AB} - d_{BC}| = 0 \le 0.50245\) ✓
- \(|d_{BC} - d_{CA}| = 0.49 \le 0.50245\) ✓
- \(|d_{CA} - d_{AB}| = 0.49 \le 0.50245\) ✓

→ **`is_equilateral = True`** → `tri_type = "equilateral"`

**Kết quả mã nguồn thực tế: `equilateral`. Kết quả đội phát triển tuyên bố: `isosceles`. SAI.**

#### TV-TOL-02

- \(L_{\max} = 100.51\)
- \(\text{tol} = 0.50255\)
- \(|d_{AB} - d_{BC}| = 0 \le \text{tol}\) ✓ → `is_isosceles = True`
- \(|d_{BC} - d_{CA}| = 0.51 > \text{tol}\) → `is_equilateral = False`

→ `is_equilateral = False`, `is_isosceles = True` → **`tri_type = "isosceles"`**

**Kết quả mã nguồn thực tế: `isosceles`. Kết quả đội phát triển tuyên bố: `scalene`. SAI.**

**Hệ quả logic:** Với \(AB = BC = 100\) (hai cạnh bằng nhau tuyệt đối), không tồn tại bất kỳ phiên bản `tol_ratio` nào trong mã nguồn khiến tam giác bị phân loại `scalene` — vì `diff_AB_BC = 0` luôn ≤ mọi tol dương. Do đó TV-TOL-02 **không thể PASS** với bất kỳ cấu hình nào của hàm hiện tại.

**Đây là fabrication test vector hoặc test chạy trên code khác với dossier.** Cả hai khả năng đều Critical.

**Yêu cầu:** Cung cấp raw stdout/log của lần chạy test, với `print()` trực tiếp kết quả `tri_type`, và chỉ rõ mã nguồn nào đã tạo ra kết quả tuyên bố.

---

### RC4-C-02. Regression: kiểm tra `blob_out.pbData == NULL` bị xóa khỏi DPAPI

Round 3 code:

```python
if not success:
    raise RuntimeError(...)

if not blob_out.pbData:              # <-- kiểm tra defensive
    raise RuntimeError("CryptProtectData returned NULL pbData.")

return ctypes.string_at(blob_out.pbData, blob_out.cbData)
```

Round 4 code:

```python
if not success:
    raise RuntimeError(...)
return ctypes.string_at(blob_out.pbData, blob_out.cbData)   # <-- kiểm tra đã bị xóa
```

**Đánh giá:** Khi `CryptProtectData` trả TRUE nhưng vẫn để `pbData = NULL` (edge case bảo vệ), `ctypes.string_at(None, cbData)` sẽ gọi `ctypes.string_at(NULL, size)` → đọc từ địa chỉ 0 → Access Violation trên Windows.

Đây là **regression so với Round 3** — đội phát triển đã sửa M-01 nhưng vô tình xóa defensive check M-03 cũ.

**Mức độ:** Critical — mã DPAPI bảo vệ bí mật bị crash trên edge case.

**Yêu cầu:** Khôi phục check `if not blob_out.pbData: raise RuntimeError(...)` trước `return`.

---

### RC4-C-03. Lịch sử evidence Vòng 2 được xác nhận là fabricated hoặc không thể tái lập

Round 4 tuyên bố:

> "Bảng Vòng 2 đã ghi nhầm thông số từ cấu hình build cũ (legacy config)."

Nhưng Round 2 đã công bố chuỗi phiên bản cực kỳ đặc thù:

```
"python_version": "3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)]"
```

Đây là **chuỗi thật, chính xác đến từng commit hash** của Python 3.10.11 (CPython tag `7d4cc5a`, ngày phát hành 05/04/2023, MSVC v.1929). Không thể "ghi nhầm từ legacy config" một chuỗi có độ chính xác cao như vậy.

Hai khả năng:

1. **Vòng 2 chạy thật trên Python 3.10.11** (máy khác), rồi Vòng 3/4 chuyển sang 3.14.5 — nghĩa là artifact Round 2 khác Round 3/4 và **đội phát triển đã không công bố việc rebuild**.
2. **Vòng 2 tự tạo chuỗi giả** (copy từ tài liệu CPython) — nghĩa là **fabrication evidence**.

Cả hai khả năng đều vi phạm tính toàn vẹn của audit trail. Vòng 2 từng ghi `"frozen": false` — xác nhận Round 2 không chạy trên exe frozen mà trên source. Do đó Round 2 evidence **không thể dùng làm mốc so sánh** với Round 3/4.

**Mức độ:** Critical — audit trail không đáng tin cậy.

**Yêu cầu:** Công bố rõ lịch sử build: Round 1/2/3/4 chạy trên máy nào, hash của exe từng round là gì, có rebuild giữa các round không.

---

### RC4-C-04. Cấu trúc đóng gói không nhất quán với PyInstaller 6.22.3

Dossier Round 4 tuyên bố:

- `dist/GeoSolver/GeoSolver.exe` — **32,754,766 bytes**
- `dist/GeoSolver/python314.dll` — 6,776,544 bytes
- `dist/GeoSolver/vcruntime140.dll` — 120,400 bytes

**Đối chiếu với hành vi chuẩn của PyInstaller 6.x:**

| Chế độ | Exe size | DLLs location |
|---|---|---|
| **`--onefile`** | 30–60 MB (self-extracting) | Không có DLL bên ngoài — extract vào `%TEMP%/_MEIxxxx/` lúc runtime |
| **`--onedir`** (mặc định 6.x) | ~1–2 MB (launcher stub) | Trong `_internal/` subfolder |
| **`--onedir --contents-directory .`** (6.x flag) | ~1–2 MB (launcher) | Trực tiếp trong `dist/GeoSolver/` |

**Không có cấu hình PyInstaller 6.x tiêu chuẩn nào đồng thời tạo ra:**

- Exe 32 MB **VÀ**
- DLL (`python314.dll`, `vcruntime140.dll`) nằm cạnh exe trong `dist/GeoSolver/`

Trừ khi đội phát triển dùng **custom post-build script** không được công bố, cấu trúc này là bất khả thi.

**Khả năng thực tế:**

- Hash `21A54331...` là của **artifact onedir** (launcher + `_internal/`), và size 32 MB chỉ là tổng cả folder, không phải exe.
- Hoặc hash là của **artifact onefile** nhưng đội phát triển ghi nhầm DLL vào dist/ thay vì `_internal/`.
- Hoặc size exe 32 MB là **fabricated**.

**Mức độ:** Critical — bằng chứng đóng gói không đáng tin.

**Yêu cầu:** Cung cấp raw output `dir /s dist\GeoSolver\` (hoặc `ls -laR`) và `Get-Item GeoSolver.exe | Format-List *` từ máy trạm.

---

### RC4-C-05. Chữ ký số (code signing) vẫn thiếu

Dossier Vòng 2, 3, 4 đều không cung cấp:

- Certificate issuer (EV/OV)
- Timestamp authority
- `signtool verify /pa /v GeoSolver.exe` output
- Chuỗi chứng thư

**Hệ quả thực tế:** Windows SmartScreen sẽ hiển thị "Unknown publisher" — người dùng không thể xác minh nguồn gốc. Với STEM app phát hành cho trường học/doanh nghiệp, đây là **blocking requirement**.

**Mức độ:** Critical.

**Yêu cầu:** Ký artifact bằng code signing certificate và cung cấp `signtool verify` output.

---

### RC4-C-06. DLL hash không thể xác minh độc lập

Hash được cung cấp:

- `python314.dll` = `18310593C50AD109FC5C95DB1FD5C92ECEC9E1BFC66C976DF9FC11DD62616D5A`
- `vcruntime140.dll` = `052AD6A20D375957E82AA6A3C441EA548D89BE0981516CA7EB306E063D5027F4`

Không có artifact để đối chiếu. **Không thể xác nhận đây là hash thật hay fabricated.**

**Yêu cầu:** Cung cấp file (hoặc gửi qua kênh độc lập), hoặc ít nhất so khớp hash `python314.dll` với bản phân phối chính thức từ `python.org` (Python 3.14.5 Windows x64 installer).

---

## 3. FINDINGS HIGH

### RC4-H-01. SBOM vẫn chưa được cung cấp

Không có CycloneDX/SPDX SBOM cho toàn bộ dependency (NumPy, SciPy, SymPy, tkinter, PyInstaller hooks). Đây là yêu cầu bắt buộc cho release gate.

### RC4-H-02. Không có raw log/ảnh chụp VM

Dossier chỉ có text claim, không có:

- Screenshot Windows Sandbox
- Raw console output của smoke test
- Timestamp + machine ID của VM
- `Get-FileHash` raw output

Không thể phân biệt bằng chứng thật với bằng chứng viết tay.

### RC4-H-03. `from_buffer(secret_input)` — edge cases chưa document

```python
ctypes.memmove(buf, (ctypes.c_char * length).from_buffer(secret_input), length)
```

- `from_buffer` yêu cầu buffer writable. `bytearray` OK, nhưng `memoryview` của `bytes` read-only sẽ raise `TypeError`.
- Nếu caller truyền subclass của `bytearray` có override `__setitem__`, việc zeroize qua vòng lặp `secret_input[i] = 0` có thể không hoạt động đúng.
- Không document giới hạn: hàm chỉ nhận `bytearray` cụ thể, không nhận `bytes`/`memoryview`.

### RC4-H-04. `GeoSolverKey` hardcoded trong DPAPI description

```python
CryptProtectData(..., "GeoSolverKey", ...)
```

Description nên khác nhau cho các secret khác nhau để tránh cross-application DPAPI confusion. Hiện tại tất cả secret đều có cùng description — không phân biệt được khi decrypt sau này.

### RC4-H-05. Round 3 vẫn chưa được giải trình đầy đủ

Round 3 không công bố dependency list. Round 4 giải thích "Round 3 was correct all along" nhưng không cung cấp `pip freeze` raw từ Round 3. Không thể xác nhận Round 3 và Round 4 dùng cùng environment.

---

## 4. FINDINGS MEDIUM

- **RC4-M-01.** `for i in range(length): secret_input[i] = 0` chậm hơn `ctypes.memset(secret_input, 0, length)` với input lớn — không phải vấn đề bảo mật nhưng là performance regression.
- **RC4-M-02.** Round 4 sử dụng `type(x) is not int` thay vì `isinstance(x, int) and not isinstance(x, bool)`. Đúng chức năng nhưng không cho phép subclass của int (hiếm gặp nhưng có thể).
- **RC4-M-03.** Nhãn dung lượng: `32,754,766 bytes = 31.237 MiB = 32.755 MB` — lần này đã đúng, ghi nhận cải thiện.
- **RC4-M-04.** Không có test cho trường hợp `GeoSolver.exe` bị antivirus flag (false positive phổ biến với PyInstaller).
- **RC4-M-05.** Không có test uninstall — registry key và file còn sót lại trên VM sạch chưa được xác minh.

---

## 5. ĐỐI SOÁT TEST VECTOR VÒNG 4

| Mã | Xác minh độc lập | Kết luận |
|---|---|---|
| TV-L01 (lattice \(10^{200}\)) | `int` arbitrary precision, `dot_A = 0` chính xác → `right_isosceles` ✓ | **PASS** |
| TV-L02 (chặn float) | `type(x) is int` → `TypeError` ✓ | **PASS** |
| TV-L03 (lattice scalene) | \(d^2=\{1000,650,1010\}\) đôi một khác → `scalene` ✓ | **PASS** |
| TV-C01 (equilateral thực) | Chênh lệch ~\(2\times10^{-4} \ll \text{tol}\) → `equilateral` ✓ | **PASS** |
| TV-C02 (biên 0.5%) | Diff \(0.49\% < 0.5\%\) → `isosceles` ✓ | **PASS** |
| TV-C03 (biên 0.3%) | Diff \(0.49\% > 0.3\%\) → `scalene` ✓ | **PASS** |
| TV-E01 (ellipe) | \(P_{\text{Ram}} = 20.0007108\), \(P_{\text{true}} = 20.0054916\) ✓ | **PASS** |
| **TV-TOL-01** | Code trả `equilateral`, dossier claim `isosceles` | **FAIL — fabricated** |
| **TV-TOL-02** | Code trả `isosceles`, dossier claim `scalene` | **FAIL — fabricated** |

**Kết quả: 7/9 PASS, 2/9 FAIL (fabricated).**

---

## 6. ĐÁNH GIÁ DPAPI — KẾT LUẬN

**Đã đạt:**

- `ctypes.memmove` loại bỏ `bytes()` trung gian ✓
- `bytearray` caller được zeroize qua vòng lặp ✓
- `buf` được zeroize qua `ctypes.memset` ✓
- `CRYPTPROTECT_UI_FORBIDDEN` được truyền ✓
- `LocalFree` cast `c_void_p` ✓
- `GetLastError` được đọc khi fail ✓

**Chưa đạt:**

- **Regression:** `blob_out.pbData == NULL` check bị xóa (RC4-C-02)
- Description hardcoded không phân biệt (RC4-H-04)
- Không document giới hạn `bytearray` only (RC4-H-03)

**Kết luận:** **Không đạt yêu cầu phát hành** — regression C-02 phải được khôi phục.

---

## 7. ĐÁNH GIÁ BẰNG CHỨNG ĐÓNG GÓI

| Yếu tố | Trạng thái |
|---|---|
| Hash SHA-256 định dạng hợp lệ | ✅ |
| Không phải hash chuỗi rỗng | ✅ |
| **Cấu trúc PyInstaller nhất quán** | ❌ **RC4-C-04** |
| **Chữ ký số** | ❌ **RC4-C-05** |
| **SBOM** | ❌ RC4-H-01 |
| **DLL hash verify được** | ⏸ RC4-C-06 |
| **Raw log/ảnh chụp VM** | ❌ RC4-H-02 |
| **Lịch sử build rõ ràng** | ❌ RC4-C-03 |

---

## 8. ĐÁNH GIÁ TÍNH TOÀN VẸN AUDIT TRAIL

Tổng hợp qua 4 vòng:

| Vòng | Finding | Đánh giá |
|---|---|---|
| Round 1 | Code có bug, không có test evidence | Thiếu sót |
| Round 2 | Hash = hash chuỗi rỗng; smoke test `frozen: false` | Placeholder + evidence yếu |
| Round 3 | Hash thật, nhưng Round 2 evidence không được giải trình | Thiếu minh bạch |
| **Round 4** | **Test TV-TOL fabricated; Round 2 "misconfiguration" không giải thích được chuỗi version cụ thể** | **Fabrication lặp lại** |

**Kết luận:** Có **pattern fabrication** xuyên suốt 4 vòng. Đây là vấn đề quy trình, không chỉ là lỗi kỹ thuật.

---

## 9. QUYẾT ĐỊNH GATE

### **FINAL VERDICT: REJECT WITH REASONS**
### **Code/Math Gate: FAIL** (TV-TOL fabricated + DPAPI regression)
### **Packaging Gate: FAIL** (cấu trúc không nhất quán + thiếu chữ ký số + thiếu SBOM)

---

## 10. ĐIỀU KIỆN BẮT BUỘC ĐỂ MỞ LẠI GATE (ROUND 5)

1. **Sửa TV-TOL-01 và TV-TOL-02** để phản ánh đúng output của code; hoặc sửa code để đạt output tuyên bố (đổi cách kiểm tra `is_isosceles` yêu cầu đúng 2 cạnh bằng nhau và cạnh thứ 3 vượt tol).
2. **Khôi phục `if not blob_out.pbData: raise`** trong DPAPI.
3. **Cung cấp raw `dir /s dist\GeoSolver\`** và `Get-Item GeoSolver.exe` từ máy trạm.
4. **Cung cấp `signtool verify` output** và chứng thư số.
5. **Cung cấp SBOM CycloneDX/SPDX**.
6. **Cung cấp raw log smoke test** (không phải JSON tự soạn).
7. **Giải trình lịch sử build** qua 4 vòng: máy nào, hash nào, rebuild khi nào.
8. **Cung cấp `pip freeze` raw** của cả Round 3 và Round 4.
9. **Bổ sung test TV-TOL-03/04** cho biên 0.49%/0.51% với tam giác scalene thực sự (ba cạnh đôi một khác).

---

## 11. PHẠM VI VÀ GIỚI HẠN

Báo cáo này dựa trên dossier Vòng 4 được cung cấp. Không xác minh được:

- Sự tồn tại thực tế của `D:\AI DATA\STEM_APP\dist\GeoSolver\GeoSolver.exe`.
- Nội dung thực của bất kỳ file DLL nào.
- Hash SHA-256 có khớp file thật.
- Chữ ký số.

Khuyến nghị Ban Thẩm định (hoặc bên thứ ba độc lập) **nhận file trực tiếp qua kênh ngoài chat** để verify hash, packaging structure, và code signing trước khi cấp Release Pass.

---

**TRẠNG THÁI CUỐI:**

- **Code/Math:** FAIL — TV-TOL fabricated, DPAPI regression.
- **Packaging:** FAIL — structure inconsistent, signing missing.
- **Integrity:** FAIL — fabricated evidence confirmed.
- **Quyết định:** **REJECT WITH REASONS — NOT APPROVED FOR DISTRIBUTION.**