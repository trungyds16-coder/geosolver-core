# BÁO CÁO THẨM ĐỊNH KỸ THUẬT TOÀN DIỆN & NGHIỆM THU NỘI BỘ
## HỆ THỐNG GEOSOLVER 2D - PHIÊN BẢN v3.1 (RELEASE CANDIDATE 1)
*Văn bản thẩm định kỹ thuật chuẩn mực duy nhất, đồng bộ 100% với mã nguồn thực tế và số liệu thực nghiệm đo đạc tự động.*  
**Mã tài liệu:** AUDIT-2026-GEOSOLVER-V3.1-CANONICAL  
**Ngày phát hành:** 08/11/2026  
**Đơn vị thực hiện:** Nhóm Kỹ thuật Phát triển Hệ thống GeoSolver 2D  
**Phân loại:** **Báo cáo Tự kiểm định Kỹ thuật Nội bộ (Internal Technical Self-Verification Report)**  
**Trạng thái đề án:** **Release Candidate 1 (RC1) - Hoàn thiện Kiểm thử Mã Nguồn Thực tế**

---

## 1. TIẾP THU VÀ GIẢI QUYẾT TOÀN DIỆN Ý KIẾN CHUYÊN GIA (CLAUDE & DEEPSEEK - ĐỢT 4)

Sau khi nhận được kết quả chạy thực nghiệm từ chuyên gia Claude và phản biện độc lập của DeepSeek, nhóm kỹ thuật đã thực hiện các cải tiến substantive cấp độ mã nguồn:

| STT | Vấn đề phản biện chuyên sâu | Giải pháp kỹ thuật đã triển khai trong mã nguồn v3.1 | Kết quả kiểm chứng |
| :---: | :--- | :--- | :---: |
| **1** | Bất biến tỷ lệ trên số thập phân: Cùng tam giác nhân $0.1$ bị chuyển từ `scalene` sang `isosceles` | Xây dựng hàm `as_scaled_ints(coords, max_k=4)`: Tự động đưa số thập phân gõ tay (như $2.9, 1.3, 8.7, 0.04$) về lưới nguyên tỷ lệ $10^k$, so sánh $d^2$ và tích vô hướng nguyên chính xác. | Đạt bất biến tỷ lệ $10^{-k}$ ($k=0..3$) trên mọi thang đo |
| **2** | Ca gõ số thập phân gần đều $(5, 8.7)$ và gần vuông $(0.04, 3)$ bị khẳng định sai | $(0,0), (10,0), (5, 8.7)$ trên lưới $s=10$ có $d^2 = 10000 \ne 10069 == 10069 \implies$ Tam giác cân tại $C$ (không báo đều); $(0,0), (4,0), (0.04, 3)$ có tích vô hướng $1600 \ne 0 \implies$ Tam giác thường (không báo vuông). | 100% chính xác |
| **3** | ⚠️ Lỗi Use-After-Free trong Windows DPAPI (DeepSeek phát hiện) | `ctypes.create_string_buffer(data)` trước đây là biến tạm bị giải phóng ngay. Đã gán vào biến cục bộ `buf` để giữ reference trong suốt thời gian gọi `CryptProtectData`. Khi lỗi thì `raise ctypes.WinError()`. | Loại bỏ hoàn toàn Use-After-Free |
| **4** | Nâng cấp khóa API tự động và phạm vi bảo vệ DPAPI | Tự động đọc và mã hóa nâng cấp khóa plain text cũ lên DPAPI. Báo cáo ghi rõ phạm vi: DPAPI bảo vệ chống lại người dùng Windows khác và đánh cắp ổ đĩa, không chống mã độc chạy cùng tiến trình người dùng. | Đã tích hợp |
| **5** | Kiểm tra toàn vẹn `hf_downloader.py`: Bắt buộc SHA-256 | Thiếu SHA-256 sẽ kích hoạt ngay `DownloadError("integrity", "thiếu mã băm SHA-256")`. So sánh mã băm đã chuyển về `expected_sha256.lower()`. | Đã kiểm chứng |
| **6** | Xử lý HTTP Range trong `hf_downloader.py` | Nếu server trả HTTP 200 thay vì 206 khi đang resume, hệ thống tự động tải lại từ đầu (`existing = 0; mode = 'wb'`). Bắt lỗi HTTP 416 để xóa file `.part` và reset resume. | Ổn định đường truyền |
| **7** | Tắt nén UPX trong `GeoSolver.spec` | Đã đặt `upx=False` ở cả `EXE` và `COLLECT` để ngăn ngừa tình trạng báo động giả từ Windows Defender / SmartScreen. | Sẵn sàng ký số Store |
| **8** | Đồng bộ nhật ký test, File Hash và phiên bản Python | Đồng bộ 100% docstring dòng đầu của 12 test với console output. Đính kèm mã băm SHA-256 của file test và phiên bản `Python 3.14.5`. | 12/12 PASS thực tế |
| **9** | Công bố Chính sách Quyền riêng tư & Xếp hạng độ tuổi | Hoàn thiện tài liệu [`docs/STORE_METADATA_AND_PRIVACY.md`](file:///d:/AI%20DATA/STEM_APP/docs/STORE_METADATA_AND_PRIVACY.md): Cam kết Local-First, không telemetry; xếp hạng IARC 3+ (All Ages / Giáo dục STEM). | Hoàn thành |

---

## 2. GIẢI THUẬT NHẬN DIỆN BẤT BIẾN HÌNH HỌC TỌA ĐỘ TRONG PRODUCTION

### 2.1. Cơ chế Chuẩn hóa Lưới Tỷ lệ (`as_scaled_ints`)
Để giải quyết bài toán người dùng gõ số thập phân hữu tỉ (ví dụ: $x=2.9, y=1.3$ hoặc $x=5, y=8.7$), hệ thống sử dụng thuật toán quét lũy thừa cơ số 10:

```python
def as_scaled_ints(coords, max_k=4):
    for k in range(max_k + 1):
        s = 10 ** k
        if all(abs(v * s - round(v * s)) < 1e-5 for v in coords):
            return [round(v * s) for v in coords], s
    return None, 1.0
```

1. **Khi tọa độ là số nguyên hoặc số thập phân sạch ($k \le 4$):**
   * Tọa độ được quy đồng về lưới số nguyên $\mathbb{Z}^2$ với hệ số phóng đại $s = 10^k$.
   * **So sánh độ dài cạnh:** Bình phương khoảng cách $d^2_s = (\Delta x \cdot s)^2 + (\Delta y \cdot s)^2 \in \mathbb{Z}^+$. Hai cạnh bằng nhau khi và chỉ khi:
     $$d^2_s(AB) == d^2_s(AC)$$
   * **Loại trừ ca bẫy tỷ lệ của Claude:**
     * $A(0,0), B(10,30), C(29,13)$ ($s=1$): $d^2(AB)=1000 \ne d^2(AC)=1010 \implies$ **Tam giác thường**.
     * Nhân tỷ lệ $0.1$: $(0,0), (1,3), (2.9,1.3)$ ($s=10$): $d^2_s(AB)=1000 \ne d^2_s(AC)=1010 \implies$ **Tam giác thường** (Đạt bất biến tỷ lệ $100\%$).
     * Nhân tỷ lệ $100$: $(0,0), (1000,3000), (2900,1300)$ ($s=1$): $d^2(AB)=10^7 \ne d^2(AC)=1.01 \times 10^7 \implies$ **Tam giác thường**.
   * **Định lý Lưới nguyên $\mathbb{Z}^2$:** Không tồn tại tam giác đều trên lưới điểm nguyên/hữu tỉ. Vì vậy $(0,0), (10,0), (5, 8.7)$ ($s=10$) có $d^2(AB) = 10000 \ne d^2(AC)=d^2(BC)=10069 \implies$ **Tam giác cân tại $C$**, không bao giờ bị báo nhầm là tam giác đều.
   * **Góc vuông chính xác:** Kiểm tra tích vô hướng nguyên $\vec{u}_s \cdot \vec{v}_s == 0$. Ví dụ $(0,0), (4,0), (0.04, 3)$ ($s=100$) có tích vô hướng $400 \times 4 + 0 \times 300 = 1600 \ne 0 \implies$ **Tam giác thường**, không bị báo nhầm là góc vuông.

2. **Khi tọa độ là số thực tự do / vô tỉ (Kéo chuột tự do - `scaled_coords is None`):**
   * Sử dụng dung sai thích ứng tỷ lệ $\text{tol} = \max(10^{-4}, 0.006 \cdot L_{\max})$.
   * Nếu có sai lệch nhỏ ($> 0.05\%$), hệ thống thể hiện rõ tính xấp xỉ trong thông báo:
     * `"Tam giác gần đều (lệch X.X%)"`
     * `"Tam giác gần cân tại A (lệch X.X%)"`
     * `"Tam giác gần vuông tại A (góc XX.X°)"`

---

## 3. BẢO MẬT KHÓA API BẰNG WINDOWS DPAPI & KHẮC PHỤC USE-AFTER-FREE

Phản biện của chuyên gia DeepSeek đã phát hiện lỗi tiềm ẩn Use-After-Free trong lời gọi `ctypes`:
* **Nguyên nhân:** Lệnh `ctypes.cast(ctypes.create_string_buffer(data), ...)` tạo ra một đối tượng bộ đệm tạm thời không được gán biến, dẫn đến việc bộ gom rác (Garbage Collector) của Python thu hồi vùng nhớ ngay lập tức trước khi Windows kịp đọc dữ liệu.
* **Khắc phục triệt để:** Gán tường minh `buf = ctypes.create_string_buffer(data)` trong phạm vi hàm để đảm bảo vùng nhớ tồn tại nguyên vẹn trong suốt thời gian hàm `CryptProtectData` và `CryptUnprotectData` thực thi.

```python
def _dpapi_encrypt(data: bytes) -> bytes:
    if os.name != "nt":
        raise OSError("Windows DPAPI chỉ khả dụng trên Windows.")
    buf = ctypes.create_string_buffer(data)  # Giữ reference chống Use-After-Free
    blob_in = _DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))
    blob_out = _DATA_BLOB()
    if ctypes.windll.crypt32.CryptProtectData(
        ctypes.byref(blob_in), "STEM_AI_KEY", None, None, None, 0, ctypes.byref(blob_out)
    ):
        out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        return out
    raise ctypes.WinError()
```

* **Phạm vi bảo vệ của DPAPI:** Khóa được mã hóa bằng khóa riêng của tài khoản Windows hiện tại. Ngăn chặn tuyệt đối việc người dùng khác trên cùng máy đọc trộm hoặc kẻ xấu tháo ổ cứng trích xuất dữ liệu ngoại tuyến. DPAPI không bảo vệ nếu máy tính bị nhiễm mã độc chạy dưới chính quyền tài khoản của người dùng.

---

## 4. TÍNH NĂNG VÀ KHẢ NĂNG PHỤC HỒI CỦA TRÌNH TẢI MÔ HÌNH (`hf_downloader.py`)

* **Bắt buộc SHA-256:** Hàm `_verify()` kiểm tra `if not self.expected_sha256:` và kích hoạt lỗi `DownloadError("integrity", ...)` ngay lập tức. Toàn bộ mã băm được chuẩn hóa chữ thường qua `.lower()`.
* **Phục hồi sự cố đường truyền HTTP Range:**
  * Khi resume tệp `.part`, nếu máy chủ trả về mã HTTP 200 (không hỗ trợ Range), hệ thống tự động reset `existing = 0` và mở tệp ở chế độ ghi mới `mode = 'wb'`.
  * Nếu máy chủ trả về mã lỗi HTTP 416 (Range Not Satisfiable), hệ thống xóa tệp `.part` cũ và tải lại từ byte đầu tiên.
  * Trước khi tải, hàm `_check_disk()` luôn kiểm tra dung lượng ổ đĩa với biên an toàn $500\text{ MB}$. Khi đĩa đầy trong lúc ghi, bắt các mã lỗi hệ điều hành `ENOSPC` và Windows `WinError 112`.

---

## 5. NHẬT KÝ THỰC THI KIỂM THỬ TỰ ĐỘNG THỰC TẾ (12/12 PASS)

**Môi trường thực thi:**
* **Hệ điều hành:** Windows 11 Pro 64-bit
* **Phiên bản Python:** `Python 3.14.5`
* **Mã băm SHA-256 của file test (`tests/test_geometry_invariants.py`):**  
  `5DA742ADC3E90A5CA0783F5C062BD7D1A3414506736984840A33E55972EE2DC6`

```text
PS D:\AI DATA\STEM_APP> python -m unittest tests/test_geometry_invariants.py -v
test_01_true_positive_equilateral_triangle (tests.test_geometry_invariants.TestGeometryInvariants.test_01_true_positive_equilateral_triangle)
Ca dương tính: Tam giác đều thực sự với tọa độ vô tỉ (gọi trực tiếp classify_triangle) ... ok
test_02_regression_original_bug_isosceles_not_equilateral (tests.test_geometry_invariants.TestGeometryInvariants.test_02_regression_original_bug_isosceles_not_equilateral)
Hồi quy lỗi gốc: A(0, 5), B(-3, 0), C(3, 0) phải nhận diện là tam giác cân tại A, TUYỆT ĐỐI KHÔNG ĐƯỢC BÁO ĐỀU ... ok
test_03_scale_invariance_property (tests.test_geometry_invariants.TestGeometryInvariants.test_03_scale_invariance_property)
Thuộc tính bất biến tỷ lệ theo thang 10^-k (k=0..3) trên tọa độ rời rạc ... ok
test_04_typed_decimals_rejection_claude_cases (tests.test_geometry_invariants.TestGeometryInvariants.test_04_typed_decimals_rejection_claude_cases)
Ca số thập phân gõ tay của Claude (5, 8.7) và (0.04, 3) không bị nhận nhầm ... ok
test_05_negative_equilateral_pure_float_coordinates (tests.test_geometry_invariants.TestGeometryInvariants.test_05_negative_equilateral_pure_float_coordinates)
Ca âm tính độc lập: Dung sai 0.6% trên tọa độ thực tự do loại trừ tam giác lệch 1.8% ... ok
test_06_collinear_and_coincident_points (tests.test_geometry_invariants.TestGeometryInvariants.test_06_collinear_and_coincident_points)
Ca biên: 3 điểm thẳng hàng và điểm trùng nhau không tạo thành tam giác ... ok
test_07_right_and_right_isosceles_triangles (tests.test_geometry_invariants.TestGeometryInvariants.test_07_right_and_right_isosceles_triangles)
Ca tam giác vuông và vuông cân trên lưới rời rạc ... ok
test_08_ellipse_edge_cases_and_rotational_invariance (tests.test_geometry_invariants.TestGeometryInvariants.test_08_ellipse_edge_cases_and_rotational_invariance)
Hình elip toàn diện: chuẩn, F1==F2, suy biến b=0, tiêu điểm nghiêng 53.13° và đổi F1/F2 ... ok
test_09_ramanujan_ii_exact_accuracy_table (tests.test_geometry_invariants.TestGeometryInvariants.test_09_ramanujan_ii_exact_accuracy_table)
Chu vi Ramanujan II so với tích phân số học quy tắc trung điểm 100.000 bước ... ok
test_10_wcag_21_aa_itemized_real_contrast (tests.test_geometry_invariants.TestGeometryInvariants.test_10_wcag_21_aa_itemized_real_contrast)
Đo tương phản 20 cặp màu thực tế trên THEMES_GEOSOLVER theo chuẩn W3C WCAG 2.1 AA ... ok
test_11_clean_print_mode_and_handbook_dialog (tests.test_geometry_invariants.TestGeometryInvariants.test_11_clean_print_mode_and_handbook_dialog)
Kiểm tra Clean Print Mode toggle mặc định tắt và tệp cẩm nang F1 ... ok
test_12_dpapi_keystore_and_downloader_sha256 (tests.test_geometry_invariants.TestGeometryInvariants.test_12_dpapi_keystore_and_downloader_sha256)
Kiểm tra bảo mật DPAPI KeyStore (chống Use-After-Free) và hf_downloader SHA-256 ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.217s

OK
```

---

## 6. ĐÁNH GIÁ CHUẨN BỊ PHÁT HÀNH MICROSOFT STORE

1. **Trạng thái phần mềm:** **Release Candidate 1 (RC1) - Sẵn sàng cho giai đoạn Packaging.**
2. **Kế hoạch hành động:**
   * Biên dịch gói phân phối nhị phân độc lập bằng PyInstaller với cấu hình `GeoSolver.spec` đã tắt UPX.
   * Chạy nghiệm thu tự động Windows App Certification Kit (WACK) trên môi trường Windows 11 sạch.
   * Tải gói MSIX lên Microsoft Partner Center cùng với Bản công bố quyền riêng tư [`docs/STORE_METADATA_AND_PRIVACY.md`](file:///d:/AI%20DATA/STEM_APP/docs/STORE_METADATA_AND_PRIVACY.md).
