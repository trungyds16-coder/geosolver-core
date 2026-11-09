# HỒ SƠ THẨM ĐỊNH TOÀN DIỆN & TRÌNH DUYỆT XUẤT BẢN CHÍNH THỨC
## DỰ ÁN GEOSOLVER 2D — PHIÊN BẢN v3.1 RC4 (Release Candidate 4)

---

- **Sản phẩm thẩm định:** GeoSolver 2D (Phiên bản v3.1 RC4 — Hệ thống CAD Hình học Phẳng & Đại số Tự động)
- **Ngày lập hồ sơ:** 09/11/2026 (Giờ địa phương: 22:35 GMT+7)
- **Tổ chức phát triển:** Nhóm Kỹ thuật Cốt lõi STEM CAD / TLabtool
- **Đơn vị / Chuyên gia thẩm định độc lập:** Claude Code (Chuyên gia Thẩm định Kiến trúc Phần mềm & An toàn Hệ thống)
- **Git Commit Hash:** `a428da857f18909274137f1c86d05a8f621f19b8`
- **Git Tag phát hành:** `v3.1.0-rc4`
- **Trạng thái cây Git:** SẠCH 100% (`git status --porcelain` rỗng, không có tệp dư thừa hoặc chưa commit)
- **SHA-256 Bản phân phối Nhị phân:**
  - `dist\GeoSolver\GeoSolver.exe`: `058B5F209AB985198A97D382670346C383302D3DB0502E5D53E7764095DAAC6A`
  - `dist\GeoSolver_v3.1.msix`: `6164C2774E0C0707745D40BD9D09EDD7437078F39BED9469008736657695B19C`

---

## MỤC LỤC HỒ SƠ

1. **XÁC NHẬN HIỆN TRẠNG & BÁO CÁO TIẾP THU Ý KIẾN THẨM ĐỊNH RC3**
   - 1.1. Hiện trạng và Phạm vi Thẩm định Độc lập (Không nhầm lẫn với CAD Math 3D)
   - 1.2. Giải trình và xử lý 5 điều kiện tiên quyết của Claude trong thẩm định RC3
2. **BÁO CÁO KỸ THUẬT NÂNG CẤP & KHẮC PHỤC TRIỆT ĐỂ (RC3 -> RC4)**
   - 2.1. Động cơ phân loại tam giác & Chuẩn hóa Collinear $rel\_cross = |cross| / l_{max}^2$ đối xứng qua 6 hoán vị
   - 2.2. Tái cấu trúc `_point_flag` dùng tập `_visiting` chống chu trình, nới lỏng giới hạn 100 tầng và memoization $O(1)$
   - 2.3. Khắc phục lỗi taint lỗi thời khi di chuyển điểm dẫn xuất (`_recompute_dependent_objects`)
   - 2.4. Xác nhận kiến trúc Win32 DPAPI với `ctypes.WinDLL` chuyên dụng và `use_last_error=True`
   - 2.5. Cơ chế cách ly bảo mật chứng chỉ số PFX và giải trình định dạng khóa nhị phân `GeminiKeyStore`
3. **TOÀN VĂN MÃ NGUỒN CỐT LÕI TRONG PRODUCTION (VERBATIM 100%)**
   - 3.1. Lõi Phân loại Tam giác & Bất biến Tỷ lệ (`classify_triangle`)
   - 3.2. Quản lý Phả hệ Dựng hình trên Canvas GUI (`_point_flag`, `_recompute_dependent_objects`, `_save_state`, `undo`, `redo`, `_restore_state`, `_on_canvas_drag`)
   - 3.3. Bảo mật DPAPI & Kết nối HTTPS an toàn (`_DATA_BLOB`, `_dpapi_encrypt`, `_dpapi_decrypt`, `GeminiKeyStore`, `_get_ssl_context`)
   - 3.4. Toàn văn Cấu hình Đóng gói Production (`GeoSolver.spec` và `msix_layout\AppxManifest.xml`)
4. **TOÀN VĂN BỘ KIỂM THỬ TỰ ĐỘNG (VERBATIM 100%)**
   - 4.1. Toàn văn Các Bài Test Tích hợp Canvas GUI, Taint, Undo/Redo & Hoán vị (Tests 24 đến 32 trong `test_geometry_invariants.py`)
   - 4.2. Toàn văn 11 Bài Test Taint Propagation Chuyên biệt (`test_round9_taint_validation.py`)
5. **DỮ LIỆU THỰC NGHIỆM CHẠY THỰC TẾ TRÊN MÁY TÍNH (LOGS XÁC THỰC)**
   - 5.1. Nhật ký chạy toàn bộ 43/43 Unittest tự động (`test_run.log`)
   - 5.2. Nhật ký Smoke Test thực tế và tệp JSON trên bản đóng gói `GeoSolver.exe`
   - 5.3. Kết quả đóng gói (`makeappx.exe`) và ký số (`signtool.exe`) gói `dist\GeoSolver_v3.1.msix`
   - 5.4. Bằng chứng cài đặt và kiểm thử khói gói MSIX thực tế trong sandbox `C:\Program Files\WindowsApps\...`
   - 5.5. Kết quả kiểm tra độ dài đường dẫn (MAX_PATH Check)
   - 5.6. Kết quả kiểm tra tiến trình con (`ai_local_manager.py` không chạy subprocess)
6. **GIT DIFF GIỮA RC3 VÀ RC4 & BẢNG MÃ BĂM SHA-256 TOÀN VẸN DỮ LIỆU**
   - 6.1. Bảng thống kê `git diff --stat 5f1efd3..v3.1.0-rc4`
   - 6.2. Git diff chi tiết các thay đổi mã nguồn cốt lõi
   - 6.3. Bảng mã băm SHA-256 toàn vẹn của tất cả các file cấu thành
7. **BIÊN BẢN & PHIẾU QUYẾT ĐỊNH NGHIỆM THU DÀNH CHO CLAUDE CODE** (ĐỂ TRỐNG)

---

## 1. XÁC NHẬN HIỆN TRẠNG & BÁO CÁO TIẾP THU Ý KIẾN THẨM ĐỊNH RC3

### 1.1. Hiện trạng và Phạm vi Thẩm định Độc lập
- **Phạm vi kiểm toán duy nhất:** Toàn bộ hồ sơ này chỉ thẩm định **GeoSolver 2D** (nằm trong thư mục `geosolver/`, `stem_shared_core/`, và `tests/`). Mọi module thuộc nhánh `cad_math_v2` (CAD Math 3D) là một ứng dụng riêng biệt, đang được thẩm định ở kênh riêng và hoàn toàn không nằm trong phạm vi hay tiêu chí đánh giá của văn bản này.
- **Tính độc lập và tính nguyên văn:** Đội ngũ phát triển ghi nhận toàn bộ phản hồi khắt khe của Claude trong đợt thẩm định RC3. Trong phiên bản RC4 này, hồ sơ được biên soạn với nguyên tắc: **Cung cấp dữ liệu thực nghiệm 100%, mã nguồn trích xuất tự động không qua chỉnh sửa tay, log chạy thực tế từ hệ điều hành Windows, và để trống hoàn toàn biểu mẫu quyết định nghiệm thu ở Mục 7 dành riêng cho Claude.**

### 1.2. Giải trình và xử lý 5 điều kiện tiên quyết của Claude trong thẩm định RC3

| STT | Điều kiện thẩm định của Claude (RC3) | Giải pháp kỹ thuật và Bằng chứng cung cấp trong RC4 |
| :---: | :--- | :--- |
| **1** | **Thiếu Mục 3.4 và Mục 5 trong tài liệu RC3** (Không thấy log 42 test, smoke test EXE mới, log makeappx/signtool, AppxManifest.xml, bằng chứng cài MSIX máy sạch). | **Cung cấp đầy đủ toàn bộ Mục 3.4 và Mục 5.** Toàn văn `GeoSolver.spec` và `AppxManifest.xml` (có thẻ `<Resources>` và đường dẫn `VFS\GeoSolver.exe`). Toàn bộ log chạy 43 test OK, log smoke test thực tế của EXE mới, log `makeappx`/`signtool`, và log cài đặt MSIX vào `C:\Program Files\WindowsApps\...` kèm kết quả smoke test chạy từ bên trong sandbox. |
| **2** | **Nghi vấn Tkinter nuốt ngoại lệ callback & lỗi `TypeError: unhashable type: 'dict'` trong `_recompute_dependent_objects`.** | **Đã gài bẫy bắt lỗi Tkinter callback:** Gán `app.report_callback_exception` trong toàn bộ các test GUI canvas (`test_24`, `test_25`, `test_28`, `test_30`, `test_32`) và khẳng định `errors == []`. Kiểm tra mã nguồn thực tế: Dòng lệnh trong production luôn là `exclude_ids = {id(p) for p in exclude_points}` và `if id(p) in exclude_ids: continue`, do đó không hề có `TypeError: unhashable type: 'dict'`. |
| **3** | **Test 31 chỉ chạy nhánh rời rạc; Test 30 chưa chứng minh thay thế đối tượng.** | **Đã nâng cấp triệt để:**<br>- `test_31`: Bổ sung toàn bộ 6 hoán vị cho 7 ca thử nghiệm trên nhánh liên tục (`source="free"`). Bổ sung 2 ca kim: ca kim thẳng hàng ($y=0.004 \implies rel\_cross = 4 \times 10^{-6} < 10^{-5}$) và ca kim tạo tam giác ($y=0.02 \implies rel\_cross = 2 \times 10^{-5} > 10^{-5}$) đều qua 6 hoán vị.<br>- `test_30`: Bổ sung `assertIsNot` chứng minh instance được thay thế bằng dict mới sau undo/redo; kiểm tra số điểm đổi từ 3 -> 2 -> 3; kiểm tra tọa độ trung điểm tự động cập nhật theo $(pA + pB)/2$ khi kéo cha. |
| **4** | **Sửa `_point_flag` bằng tập `_visiting` và xử lý taint lỗi thời sau recompute.** | **Đã tái cấu trúc:**<br>- `_point_flag` sử dụng tập `_visiting = set()` để phát hiện chu trình (cycle detection) an toàn; mở rộng giới hạn độ sâu an toàn lên 100 tầng (chỉ làm chốt chặn tràn stack, không gán taint giả cho cây sạch 10 tầng); memoization $O(1)$ an toàn.<br>- `_recompute_dependent_objects`: Khi điểm dẫn xuất (`midpoint`, `formula`, `intersection`) được tính lại do cha di chuyển, hàm tự động gán lại `p["source"] = c_type` và xóa cờ lỗi thời qua `p.pop("exact", None)`. Đã kiểm chứng qua bài test mới `test_32`. |
| **5** | **Bảo mật chứng chỉ PFX và giải trình định dạng khóa `GeminiKeyStore`.** | **Đã hoàn thiện:**<br>- Tệp PFX được đưa vào `.gitignore` (`*.pfx`, `**/*.pfx`), mật khẩu được truyền qua biến môi trường an toàn `$env:SIGN_PFX_PASSWORD`.<br>- Giải trình rõ ràng về định dạng nhị phân thô của `GeminiKeyStore`: Dữ liệu được mã hóa trực tiếp bằng Windows DPAPI (`CryptProtectData`) trả về chuỗi byte nhị phân thô ghi xuống đĩa, loại bỏ overhead Base64 và phụ thuộc dư thừa. |

---

## 2. BÁO CÁO KỸ THUẬT NÂNG CẤP & KHẮC PHỤC TRIỆT ĐỂ (RC3 -> RC4)

### 2.1. Động cơ phân loại tam giác & Chuẩn hóa Collinear $rel\_cross = |cross| / l_{max}^2$
- **Khắc phục lỗi xét lệch đỉnh A:** Trong hàm `classify_triangle`, hệ thống thu thập đầy đủ tính chất vuông góc và bằng nhau của cả 3 đỉnh:
  - Góc vuông: $\perp_A$ (dot product $AB \cdot AC$), $\perp_B$ (dot product $BA \cdot BC$), $\perp_C$ (dot product $CA \cdot CB$).
  - Cặp cạnh bằng nhau: $eq\_AB\_AC$ ($|c - b|$), $eq\_BA\_BC$ ($|c - a|$), $eq\_CA\_CB$ ($|b - a|$).
  - Thang bậc logic phân loại duyệt tuần tự qua cả 3 đỉnh: Đều $\rightarrow$ Vuông cân tại A/B/C $\rightarrow$ Cân tại A/B/C $\rightarrow$ Vuông tại A/B/C $\rightarrow$ Thường.
- **Chuẩn hóa diện tích không thứ nguyên đối xứng hoán vị:**
  $$rel\_cross = \frac{|cross|}{l_{max}^2} = \frac{|u_{AB}^x u_{AC}^y - u_{AB}^y u_{AC}^x|}{\max(a, b, c)^2}$$
  Đại lượng này độc lập với việc chọn đỉnh gốc $A, B$ hay $C$, vì tích có hướng giữa hai cạnh bất kỳ của tam giác luôn có độ lớn bằng $2 \times \text{Diện tích}(\Delta ABC)$. Khi chia cho $l_{max}^2$, chỉ số này có thứ nguyên 0, bất biến tuyệt đối qua phép co giãn tỷ lệ và bảo toàn 100% kết quả trên cả 6 hoán vị của 3 đỉnh.
  - Ngưỡng xác định thẳng hàng: $rel\_cross < 10^{-5}$.

### 2.2. Tái cấu trúc `_point_flag` dùng tập `_visiting` và memoization $O(1)$
- **Khắc phục lỗi cắt cụt độ sâu 8:** Trước đây, `_depth >= 8` ngắt đệ quy và trả về `False`, khiến một cây dựng hình sạch có độ sâu 9 tầng bị đánh dấu "bẩn" (tainted) giả mạo.
- **Kiến trúc mới:**
  ```python
  def _point_flag(p, _visiting=None, memo=None, _depth=0):
      if not isinstance(p, dict):
          return None
      obj_id = id(p)
      if memo is None:
          memo = {}
      if obj_id in memo:
          return memo[obj_id]
      if _visiting is None:
          _visiting = set()
      if obj_id in _visiting:
          return False  # Phát hiện chu trình tham chiếu vòng
      if _depth >= 100:
          return False  # Chốt chặn tràn ngăn xếp đệ quy
      ...
  ```
  Nhờ có tập `_visiting.add(obj_id)` và `_visiting.discard(obj_id)` trong khối `finally:`, thuật toán phát hiện chu trình đồ thị có hướng (DAG Cycle Detection) chính xác, cho phép các cây phụ thuộc sâu 10–20 tầng sạch vẫn trả về `True` chính xác, đồng thời bảng `memo` lưu trữ kết quả giúp thời gian duyệt 100 lần đồ thị kim cương hội tụ chỉ mất $< 0.005$ giây.

### 2.3. Khắc phục lỗi taint lỗi thời khi di chuyển điểm dẫn xuất
- **Vấn đề:** Khi người dùng kéo một điểm trung điểm $M$ khi đang bật snap, điểm $M$ tạm thời nhận `source="grid_snap"` và `exact=True`. Nhưng sau đó, nếu người dùng kéo điểm cha $A$ tự do mà không snap, tọa độ của $M$ được tự động tính lại theo $A$, nhưng cờ cũ của $M$ vẫn ghi nhớ `exact=True`, dẫn đến tam giác chứa $M$ không bị đánh dấu taint.
- **Giải pháp trong RC4:** Trong phương thức `_recompute_dependent_objects`, mỗi khi một điểm có ràng buộc hình học (`midpoint`, `on_segment`, `intersection`) được cập nhật lại tọa độ từ các điểm cha:
  ```python
  p["parents"] = [p1, p2]
  p["source"] = c_type       # Làm tươi nguồn gốc: "midpoint", "formula", "intersection"
  p.pop("exact", None)       # Xóa bỏ cờ exact thủ công cũ để kế thừa taint từ cha
  ```
  Được kiểm chứng tự động bằng bài test mới `test_32_drag_derived_point_then_drag_parent`.

### 2.4. Xác nhận kiến trúc Win32 DPAPI với `ctypes.WinDLL` chuyên dụng
- Khắc phục nguy cơ xung đột luồng khi cấu hình `argtypes`/`restype` trên thư viện chia sẻ `ctypes.windll`.
- Khởi tạo đối tượng DLL riêng biệt với cơ chế lưu mã lỗi hệ điều hành:
  ```python
  _crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
  _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
  ```
- Thu hồi mã lỗi chính xác qua `ctypes.get_last_error()` và bọc trong `ctypes.WinError(err)`.

### 2.5. Cơ chế cách ly bảo mật chứng chỉ số PFX & Định dạng khóa `GeminiKeyStore`
- **Cách ly chứng chỉ:** Đưa `*.pfx`, `**/*.pfx`, `*.cer`, `*.key` vào `.gitignore`. Mật khẩu ký số được truyền hoàn toàn qua biến môi trường phiên `$env:SIGN_PFX_PASSWORD` và hủy ngay sau khi lệnh ký kết thúc (`Remove-Item env:\SIGN_PFX_PASSWORD`).
- **Định dạng nhị phân thô của `GeminiKeyStore`:** Khóa API Gemini được mã hóa bằng hàm `CryptProtectData` với entropy định danh `"STEM_AI_KEY"`. Kết quả trả về là chuỗi byte nhị phân được lưu trực tiếp vào tệp `gemini_api.key` trong thư mục cấu hình an toàn `%LOCALAPPDATA%\GeoSolver\gemini_api.key`. Khi đọc, hàm đọc nhị phân `rb` và giải mã qua `CryptUnprotectData`. Cơ chế này loại bỏ lớp trung gian Base64 thừa, tối ưu tốc độ và tương thích hoàn toàn với cơ chế bảo vệ DPAPI theo từng tài khoản người dùng Windows.

---

## 3. TOÀN VĂN MÃ NGUỒN CỐT LÕI TRONG PRODUCTION (VERBATIM 100%)

### 3.1. Lõi Phân loại Tam giác & Bất biến Tỷ lệ (`classify_triangle`)
*Trích xuất nguyên văn từ `geosolver/geosolver_desktop.py` (Dòng 385 đến 731):*

```python
def classify_triangle(pA, pB, pC, lang: str = "vi", points_exact: bool | None = None) -> dict:
    """
    Phân loại hình học tam giác thuần túy (Pure Function - Production Code):
    - Kiểm tra điểm trùng, 3 điểm thẳng hàng.
    - Nhận diện cờ nguồn gốc points_exact / metadata 'source' ('typed', 'grid_snap' vs 'free'):
        + Nếu người dùng vẽ chuột tự do (source='free' hoặc points_exact=False):
          exact luôn là False dù tọa độ rơi vào số nguyên do ngẫu nhiên hoặc mức zoom pixel.
        + Nếu người dùng gõ tay hoặc snap lưới (points_exact=True):
          exact là True khi tọa độ thỏa mãn lưới số nguyên/hữu tỉ.
    - Nhận diện tọa độ số nguyên hoặc thập phân gõ tay (as_scaled_ints):
        + So sánh d^2 chính xác bằng số nguyên trên lưới tỷ lệ (tránh sai số d^2=1000 vs 1010 do làm tròn số thực).
        + Tích vô hướng nguyên == 0 cho góc vuông.
        + Áp dụng Định lý lưới nguyên Z^2: Tam giác có đỉnh trên lưới số nguyên/hữu tỉ không thể là tam giác đều.
    - Với tọa độ thực tự do / vô tỉ:
        + Dùng dung sai tỷ lệ tương đối tol_rel = 0.006 (0.6% L_max, không áp ngưỡng tuyệt đối).
        + Báo rõ 'gần đều (lệch X.X%)', 'gần cân (lệch X.X%)', 'gần vuông (góc X.X°)'.
    """
    is_en = (lang == "en")
    
    def get_xy_name_exact(p, default_name):
        if p is None:
            raise ValueError(f"Tọa độ điểm không được là None: {p!r}")
        if isinstance(p, dict):
            if "x" not in p or "y" not in p:
                raise ValueError(f"Điểm thiếu thuộc tính tọa độ 'x' hoặc 'y': {p}")
            return (_finite(p["x"], "x", p), _finite(p["y"], "y", p),
                    str(p.get("name") or default_name), _point_flag(p))
        if not isinstance(p, (list, tuple)):
            raise ValueError(f"Tọa độ điểm phải là dict hoặc sequence (list/tuple), nhận được {type(p).__name__}: {p!r}")
        if len(p) < 2:
            raise ValueError(f"Tọa độ điểm phải có ít nhất 2 phần tử (x, y): {p}")
        return _finite(p[0], "x", p), _finite(p[1], "y", p), default_name, None

    xA, yA, nA, exA = get_xy_name_exact(pA, "A")
    xB, yB, nB, exB = get_xy_name_exact(pB, "B")
    xC, yC, nC, exC = get_xy_name_exact(pC, "C")

    # Thứ tự ưu tiên xác định nguồn gốc điểm (Taint Precedence Hierarchy):
    # 1. Lan truyền vết bẩn (Taint propagation): Nếu BẤT KỲ điểm nào là False (vẽ chuột tự do),
    #    toàn bộ tam giác bắt buộc là False. Tham số points_exact=True KHÔNG ĐƯỢC PHÉP đè lên cờ False này!
    # 2. Nếu caller chỉ định points_exact=False tường minh: Toàn bộ tam giác là False.
    # 3. Nếu caller chỉ định points_exact=True tường minh (và không có điểm nào bị taint False): Toàn bộ tam giác là True.
    # 4. Nếu tất cả 3 điểm đều có cờ True: Toàn bộ tam giác là True.
    # 5. Ngược lại (có điểm None - thiếu metadata): user_declared_exact = None (chuyển sang chế độ Heuristic số học is_discrete).
    pt_flags = [exA, exB, exC]
    if any(f is False for f in pt_flags):
        user_declared_exact = False
    elif points_exact is False:
        user_declared_exact = False
    elif points_exact is True:
        user_declared_exact = True
    elif all(f is True for f in pt_flags):
        user_declared_exact = True
    else:
        user_declared_exact = None

    u_AB = (xB - xA, yB - yA)
    u_AC = (xC - xA, yC - yA)
    u_BC = (xC - xB, yC - yB)

    c_sq = u_AB[0]**2 + u_AB[1]**2
    b_sq = u_AC[0]**2 + u_AC[1]**2
    a_sq = u_BC[0]**2 + u_BC[1]**2

    c_len = math.sqrt(c_sq)  # AB
    b_len = math.sqrt(b_sq)  # AC
    a_len = math.sqrt(a_sq)  # BC

    cross = u_AB[0] * u_AC[1] - u_AB[1] * u_AC[0]
    
    # Nhận diện tọa độ số nguyên hoặc số thập phân sạch (ví dụ gõ 8.7, 2.9, 1.3, 0.04)
    scaled_coords, scale_factor = as_scaled_ints([xA, yA, xB, yB, xC, yC], max_k=4)
    # Điểm vẽ tay có tọa độ rơi vào lưới pixel/40 sẽ lọt nhánh "rời rạc"
    # và bị so sánh bằng chính xác. Ép về nhánh dung sai tương đối khi user_declared_exact is False.
    is_discrete = (scaled_coords is not None) and (user_declared_exact is not False)

    # Kiểm tra trùng điểm bất biến theo tỷ lệ (không dùng ngưỡng tuyệt đối 1e-4)
    if is_discrete:
        sxA, syA, sxB, syB, sxC, syC = scaled_coords
        s_uAB = (sxB - sxA, syB - syA)
        s_uAC = (sxC - sxA, syC - syA)
        s_uBC = (sxC - sxB, syC - syB)
        is_coincident = (s_uAB == (0, 0)) or (s_uAC == (0, 0)) or (s_uBC == (0, 0))
        is_collinear = (s_uAB[0] * s_uAC[1] - s_uAB[1] * s_uAC[0] == 0)
    else:
        l_max = max(a_len, b_len, c_len)
        if l_max < 1e-12:
            is_coincident = True
        else:
            is_coincident = (c_len / l_max < 1e-6) or (b_len / l_max < 1e-6) or (a_len / l_max < 1e-6)
        # Chuẩn hóa diện tích theo l_max^2 (bảo đảm bất biến hoán vị 100% giữa 6 hoán vị của 3 đỉnh)
        rel_cross = abs(cross) / (l_max * l_max) if l_max > 1e-12 else 0.0
        is_collinear = (rel_cross < 1e-5)

    if is_coincident:
        msg = "Coincident points; not a valid triangle." if is_en else "Có điểm trùng nhau; không tạo thành tam giác."
        return {
            "is_triangle": False, "type": "coincident",
            "message": msg, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}
        }

    if is_collinear:
        msg = "Collinear points; not a triangle." if is_en else "3 điểm thẳng hàng; không tạo thành tam giác."
        return {
            "is_triangle": False, "type": "collinear",
            "message": msg, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}
        }

    l_max = max(a_len, b_len, c_len)
    l_min = min(a_len, b_len, c_len)

    str_AB = format_radical_len(c_len, (xA, yA), (xB, yB))
    str_AC = format_radical_len(b_len, (xA, yA), (xC, yC))
    str_BC = format_radical_len(a_len, (xB, yB), (xC, yC))

    is_equilateral = False
    perp_A = False
    perp_B = False
    perp_C = False
    eq_AB_AC = False
    eq_BA_BC = False
    eq_CA_CB = False
    diff_AB_AC = 0.0
    diff_BA_BC = 0.0
    diff_CA_CB = 0.0
    diff_eq = 0.0
    angle_A = 90.0
    angle_B = 90.0
    angle_C = 90.0

    if is_discrete:
        # CHẾ ĐỘ RỜI RẠC: Số nguyên hoặc số thập phân sạch (as_scaled_ints)
        d2_AB = s_uAB[0]**2 + s_uAB[1]**2
        d2_AC = s_uAC[0]**2 + s_uAC[1]**2
        d2_BC = s_uBC[0]**2 + s_uBC[1]**2

        eq_AB_AC = (d2_AB == d2_AC)
        eq_BA_BC = (d2_AB == d2_BC)
        eq_CA_CB = (d2_AC == d2_BC)
        is_equilateral = False  # Theo định lý lưới nguyên Z^2, không thể tồn tại tam giác đều

        dot_A = s_uAB[0] * s_uAC[0] + s_uAB[1] * s_uAC[1]
        dot_B = -s_uAB[0] * s_uBC[0] - s_uAB[1] * s_uBC[1]
        dot_C = s_uAC[0] * s_uBC[0] + s_uAC[1] * s_uBC[1]

        perp_A = (dot_A == 0)
        perp_B = (dot_B == 0)
        perp_C = (dot_C == 0)
    else:
        # CHẾ ĐỘ LIÊN TỤC: Tọa độ thực tự do / vô tỉ (Bảo đảm bất biến tỷ lệ tuyệt đối)
        tol_rel = 0.006  # 0.6%
        max_AB_AC = max(c_len, b_len)
        max_BA_BC = max(c_len, a_len)
        max_CA_CB = max(b_len, a_len)

        eq_AB_AC = (abs(c_len - b_len) <= tol_rel * max_AB_AC) if max_AB_AC > 1e-12 else True
        eq_BA_BC = (abs(c_len - a_len) <= tol_rel * max_BA_BC) if max_BA_BC > 1e-12 else True
        eq_CA_CB = (abs(b_len - a_len) <= tol_rel * max_CA_CB) if max_CA_CB > 1e-12 else True

        diff_AB_AC = (abs(c_len - b_len) / max_AB_AC * 100.0) if max_AB_AC > 1e-12 else 0.0
        diff_BA_BC = (abs(c_len - a_len) / max_BA_BC * 100.0) if max_BA_BC > 1e-12 else 0.0
        diff_CA_CB = (abs(b_len - a_len) / max_CA_CB * 100.0) if max_CA_CB > 1e-12 else 0.0

        is_equilateral = ((l_max - l_min) <= tol_rel * l_max) if l_max > 1e-12 else False
        diff_eq = ((l_max - l_min) / l_max * 100.0) if l_max > 1e-12 else 0.0

        dot_A = u_AB[0] * u_AC[0] + u_AB[1] * u_AC[1]
        dot_B = -u_AB[0] * u_BC[0] - u_AB[1] * u_BC[1]
        dot_C = u_AC[0] * u_BC[0] + u_AC[1] * u_BC[1]

        cos_A = dot_A / (c_len * b_len)
        cos_B = dot_B / (c_len * a_len)
        cos_C = dot_C / (b_len * a_len)

        angle_A = math.degrees(math.acos(max(-1.0, min(1.0, cos_A))))
        angle_B = math.degrees(math.acos(max(-1.0, min(1.0, cos_B))))
        angle_C = math.degrees(math.acos(max(-1.0, min(1.0, cos_C))))

        perp_A = (abs(cos_A) <= 0.015)
        perp_B = (abs(cos_B) <= 0.015)
        perp_C = (abs(cos_C) <= 0.015)

    tri_type = "scalene"
    vertex = None
    description = ""

    if is_equilateral:
        tri_type = "equilateral"
        avg_s = (a_len + b_len + c_len) / 3.0
        s_str = format_radical_len(avg_s, (xA, yA), (xB, yB))
        mod_eq = f" (gần đều, lệch {diff_eq:.1f}%)" if (not is_discrete and diff_eq > 0.05) else ""
        description = f"Equilateral triangle: Δ{nA}{nB}{nC} (AB=BC=CA = {s_str}){mod_eq}" if is_en else f"Tam giác đều: Δ{nA}{nB}{nC} (ba cạnh bằng nhau = {s_str}){mod_eq}"

    elif perp_A and eq_AB_AC:
        tri_type = "right_isosceles"
        vertex = nA
        avg_leg = (c_len + b_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xA, yA), (xB, yB))
        notes = []
        if not is_discrete:
            if diff_AB_AC > 0.05:
                notes.append(f"lệch cạnh {diff_AB_AC:.1f}%" if not is_en else f"leg dev {diff_AB_AC:.1f}%")
            if abs(angle_A - 90.0) > 0.05:
                notes.append(f"góc {angle_A:.1f}°" if not is_en else f"angle {angle_A:.1f}°")
        mod_ri = f" (gần vuông cân: {', '.join(notes)})" if notes else ""
        description = f"Right isosceles triangle at {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, ∠{nA}=90°){mod_ri}" if is_en else f"Tam giác vuông cân tại {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, ∠{nA}=90°){mod_ri}"
    elif perp_B and eq_BA_BC:
        tri_type = "right_isosceles"
        vertex = nB
        avg_leg = (c_len + a_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xB, yB), (xC, yC))
        notes = []
        if not is_discrete:
            if diff_BA_BC > 0.05:
                notes.append(f"lệch cạnh {diff_BA_BC:.1f}%" if not is_en else f"leg dev {diff_BA_BC:.1f}%")
            if abs(angle_B - 90.0) > 0.05:
                notes.append(f"góc {angle_B:.1f}°" if not is_en else f"angle {angle_B:.1f}°")
        mod_ri = f" (gần vuông cân: {', '.join(notes)})" if notes else ""
        description = f"Right isosceles triangle at {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, ∠{nB}=90°){mod_ri}" if is_en else f"Tam giác vuông cân tại {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, ∠{nB}=90°){mod_ri}"
    elif perp_C and eq_CA_CB:
        tri_type = "right_isosceles"
        vertex = nC
        avg_leg = (b_len + a_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xC, yC), (xA, yA))
        notes = []
        if not is_discrete:
            if diff_CA_CB > 0.05:
                notes.append(f"lệch cạnh {diff_CA_CB:.1f}%" if not is_en else f"leg dev {diff_CA_CB:.1f}%")
            if abs(angle_C - 90.0) > 0.05:
                notes.append(f"góc {angle_C:.1f}°" if not is_en else f"angle {angle_C:.1f}°")
        mod_ri = f" (gần vuông cân: {', '.join(notes)})" if notes else ""
        description = f"Right isosceles triangle at {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, ∠{nC}=90°){mod_ri}" if is_en else f"Tam giác vuông cân tại {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, ∠{nC}=90°){mod_ri}"

    elif eq_AB_AC:
        tri_type = "isosceles"
        vertex = nA
        avg_leg = (c_len + b_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xA, yA), (xB, yB))
        base_str = format_radical_len(a_len, (xB, yB), (xC, yC))
        mod_text = f" (gần cân, lệch {diff_AB_AC:.1f}%)" if (not is_discrete and diff_AB_AC > 0.05) else ""
        description = (f"Isosceles triangle at {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, base {nB}{nC} = {base_str}){mod_text}" if is_en 
                       else f"Tam giác cân tại {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, đáy {nB}{nC} = {base_str}){mod_text}")
    elif eq_BA_BC:
        tri_type = "isosceles"
        vertex = nB
        avg_leg = (c_len + a_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xB, yB), (xC, yC))
        base_str = format_radical_len(b_len, (xC, yC), (xA, yA))
        mod_text = f" (gần cân, lệch {diff_BA_BC:.1f}%)" if (not is_discrete and diff_BA_BC > 0.05) else ""
        description = (f"Isosceles triangle at {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, base {nA}{nC} = {base_str}){mod_text}" if is_en 
                       else f"Tam giác cân tại {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, đáy {nA}{nC} = {base_str}){mod_text}")
    elif eq_CA_CB:
        tri_type = "isosceles"
        vertex = nC
        avg_leg = (b_len + a_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xC, yC), (xA, yA))
        base_str = format_radical_len(c_len, (xA, yA), (xB, yB))
        mod_text = f" (gần cân, lệch {diff_CA_CB:.1f}%)" if (not is_discrete and diff_CA_CB > 0.05) else ""
        description = (f"Isosceles triangle at {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, base {nA}{nB} = {base_str}){mod_text}" if is_en 
                       else f"Tam giác cân tại {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, đáy {nA}{nB} = {base_str}){mod_text}")

    elif perp_A:
        tri_type = "right"
        vertex = nA
        ang_dev = abs(angle_A - 90.0)
        mod_r = f" (gần vuông, góc {angle_A:.1f}°)" if (not is_discrete and ang_dev > 0.05) else ""
        description = f"Right triangle at {nA}: Δ{nA}{nB}{nC} ({nA}{nB} ⊥ {nA}{nC}){mod_r}" if is_en else f"Tam giác vuông tại {nA}: Δ{nA}{nB}{nC} ({nA}{nB} ⊥ {nA}{nC}){mod_r}"
    elif perp_B:
        tri_type = "right"
        vertex = nB
        ang_dev = abs(angle_B - 90.0)
        mod_r = f" (gần vuông, góc {angle_B:.1f}°)" if (not is_discrete and ang_dev > 0.05) else ""
        description = f"Right triangle at {nB}: Δ{nA}{nB}{nC} ({nB}{nA} ⊥ {nB}{nC}){mod_r}" if is_en else f"Tam giác vuông tại {nB}: Δ{nA}{nB}{nC} ({nB}{nA} ⊥ {nB}{nC}){mod_r}"
    elif perp_C:
        tri_type = "right"
        vertex = nC
        ang_dev = abs(angle_C - 90.0)
        mod_r = f" (gần vuông, góc {angle_C:.1f}°)" if (not is_discrete and ang_dev > 0.05) else ""
        description = f"Right triangle at {nC}: Δ{nA}{nB}{nC} ({nC}{nA} ⊥ {nC}{nB}){mod_r}" if is_en else f"Tam giác vuông tại {nC}: Δ{nA}{nB}{nC} ({nC}{nA} ⊥ {nC}{nB}){mod_r}"
    else:
        tri_type = "scalene"
        description = f"Scalene triangle: Δ{nA}{nB}{nC}" if is_en else f"Tam giác thường: Δ{nA}{nB}{nC}"

    deviations = {}
    if not is_discrete:
        if tri_type == "equilateral":
            deviations["equilateral_diff_pct"] = round(diff_eq, 2)
        elif tri_type == "isosceles":
            if vertex == nA:
                deviations["leg_diff_pct"] = round(diff_AB_AC, 2)
            elif vertex == nB:
                deviations["leg_diff_pct"] = round(diff_BA_BC, 2)
            elif vertex == nC:
                deviations["leg_diff_pct"] = round(diff_CA_CB, 2)
        elif tri_type == "right":
            if vertex == nA:
                deviations["angle_deg"] = round(angle_A, 2)
                deviations["angle_diff_deg"] = round(abs(angle_A - 90.0), 2)
            elif vertex == nB:
                deviations["angle_deg"] = round(angle_B, 2)
                deviations["angle_diff_deg"] = round(abs(angle_B - 90.0), 2)
            elif vertex == nC:
                deviations["angle_deg"] = round(angle_C, 2)
                deviations["angle_diff_deg"] = round(abs(angle_C - 90.0), 2)
        elif tri_type == "right_isosceles":
            if vertex == nA:
                deviations["leg_diff_pct"] = round(diff_AB_AC, 2)
                deviations["angle_deg"] = round(angle_A, 2)
                deviations["angle_diff_deg"] = round(abs(angle_A - 90.0), 2)
            elif vertex == nB:
                deviations["leg_diff_pct"] = round(diff_BA_BC, 2)
                deviations["angle_deg"] = round(angle_B, 2)
                deviations["angle_diff_deg"] = round(abs(angle_B - 90.0), 2)
            elif vertex == nC:
                deviations["leg_diff_pct"] = round(diff_CA_CB, 2)
                deviations["angle_deg"] = round(angle_C, 2)
                deviations["angle_diff_deg"] = round(abs(angle_C - 90.0), 2)

    def _is_near_int(v: float) -> bool:
        if abs(v) < 1e-9:
            return True
        if abs(v) < 0.5:
            return False
        return abs(v - round(v)) < 1e-5

    all_int = all(_is_near_int(v) for v in (xA, yA, xB, yB, xC, yC))
    exact_math = False if user_declared_exact is False else (is_discrete if user_declared_exact is None else (is_discrete and user_declared_exact))
    return {
        "is_triangle": True,
        "type": tri_type,
        "vertex": vertex,
        "all_int": all_int,
        "is_discrete": is_discrete,
        "exact": exact_math,
        "origin_exact": user_declared_exact,
        "deviations": deviations,
        "scale_factor": scale_factor,
        "is_equilateral": is_equilateral,
        "is_isosceles": (tri_type in ("isosceles", "right_isosceles")),
        "is_right": (tri_type in ("right", "right_isosceles")),
        "sides": {"AB": c_len, "AC": b_len, "BC": a_len},
        "side_labels": {"AB": str_AB, "AC": str_AC, "BC": str_BC},
        "sides_formatted": {"AB": str_AB, "AC": str_AC, "BC": str_BC},
        "description": description
    }



```

### 3.2. Quản lý Phả hệ Dựng hình trên Canvas GUI

#### (a) Hàm kiểm tra và lan truyền cờ nguồn gốc (`_point_flag`):
*Trích xuất nguyên văn từ `geosolver/geosolver_desktop.py` (Dòng 332 đến 384):*

```python
def _point_flag(p, _visiting=None, memo=None, _depth=0):
    """True = chính xác, False = vẽ tay (taint) hoặc chu trình, None = không rõ nguồn.

    Điểm dựng hình (midpoint/intersection/formula) kế thừa cờ từ điểm cha
    qua khóa "parents". Không có "parents" thì coi là không rõ (None),
    trừ khi có exact=True tường minh.
    Sử dụng tập _visiting để phát hiện chu trình (cycle detection) và memo để tối ưu O(1).
    Nếu vượt quá giới hạn độ sâu an toàn (_depth >= 100), hàm trả False để chống tràn ngăn xếp.
    """
    if not isinstance(p, dict):
        return None
    if memo is None:
        memo = {}
    obj_id = id(p)
    if obj_id in memo:
        return memo[obj_id]

    if _visiting is None:
        _visiting = set()
    if obj_id in _visiting:
        # Chu trình tham chiếu vòng trong đồ thị phả hệ
        return False
    if _depth >= 100:
        # Bảo vệ tràn ngăn xếp đệ quy
        return False

    if p.get("source") in _FREE_SOURCES or p.get("exact") is False:
        memo[obj_id] = False
        return False

    if p.get("source") in _DERIVED_SOURCES and p.get("parents"):
        _visiting.add(obj_id)
        try:
            flags = [_point_flag(q, _visiting, memo, _depth + 1) for q in p["parents"]]
            if any(f is False for f in flags):
                res = False
            elif all(f is True for f in flags):
                res = True
            else:
                res = None
            memo[obj_id] = res
            return res
        finally:
            _visiting.discard(obj_id)

    if p.get("exact") is True or p.get("source") in _EXACT_SOURCES:
        memo[obj_id] = True
        return True

    memo[obj_id] = None
    return None



```

#### (b) Động cơ lan truyền tọa độ và làm tươi cờ nguồn gốc (`_recompute_dependent_objects`):
*Trích xuất nguyên văn từ `geosolver/geosolver_desktop.py` (Dòng 8507 đến 8775):*

```python
    def _recompute_dependent_objects(self, exclude_points=None):

        """Cơ chế Ràng buộc Hình học Động (Dynamic Geometry Constraint Propagation Engine):

        Tự động lan truyền tọa độ cho các điểm phụ thuộc (trung điểm, điểm trên đoạn, hình chiếu,

        tịnh tiến vector, giao điểm, trực tâm, tâm nội, tâm ngoại) và cập nhật đường tròn tương ứng."""

        if exclude_points is None:

            exclude_ids = set()

        else:

            exclude_ids = {id(p) for p in exclude_points}



        for _ in range(3):

            # 1. Cập nhật các điểm có ràng buộc hình học

            for p in self.points:

                if id(p) in exclude_ids:

                    continue

                c = p.get("constraint")

                if not c:

                    continue

                c_type = c.get("type")



                if c_type == "midpoint":
                    p1 = self._resolve_point(c.get("p1"))
                    p2 = self._resolve_point(c.get("p2"))
                    if p1 and p2:
                        p["x"] = (p1["x"] + p2["x"]) / 2.0
                        p["y"] = (p1["y"] + p2["y"]) / 2.0
                        p["parents"] = [p1, p2]
                        p["source"] = "midpoint"
                        p.pop("exact", None)

                elif c_type in ("on_segment", "on_line"):
                    p1 = self._resolve_point(c.get("p1"))
                    p2 = self._resolve_point(c.get("p2"))
                    if p1 and p2:
                        t = c.get("t", 0.5)
                        p["x"] = p1["x"] + t * (p2["x"] - p1["x"])
                        p["y"] = p1["y"] + t * (p2["y"] - p1["y"])
                        p["parents"] = [p1, p2]
                        p["source"] = "formula"
                        p.pop("exact", None)



                elif c_type == "proj_foot":

                    pt = self._resolve_point(c.get("p"))

                    p1 = self._resolve_point(c.get("line_p1"))

                    p2 = self._resolve_point(c.get("line_p2"))

                    if pt and p1 and p2:

                        dx = p2["x"] - p1["x"]

                        dy = p2["y"] - p1["y"]

                        L2 = dx * dx + dy * dy

                        if L2 > 1e-9:

                            t = ((pt["x"] - p1["x"]) * dx + (pt["y"] - p1["y"]) * dy) / L2

                            p["x"] = p1["x"] + t * dx

                            p["y"] = p1["y"] + t * dy



                elif c_type == "translate_vec":

                    base = self._resolve_point(c.get("base_pt"))

                    v1 = self._resolve_point(c.get("v1"))

                    v2 = self._resolve_point(c.get("v2"))

                    if base and v1 and v2:

                        p["x"] = base["x"] + (v2["x"] - v1["x"])

                        p["y"] = base["y"] + (v2["y"] - v1["y"])



                elif c_type == "intersection":

                    p1 = self._resolve_point(c.get("p1"))

                    p2 = self._resolve_point(c.get("p2"))

                    p3 = self._resolve_point(c.get("p3"))

                    p4 = self._resolve_point(c.get("p4"))

                    if p1 and p2 and p3 and p4:

                        pt_int = self._intersect_lines(p1, p2, p3, p4)

                        if pt_int:
                            p["x"], p["y"] = pt_int[0], pt_int[1]
                            p["parents"] = [p1, p2, p3, p4]
                            p["source"] = "intersection"
                            p.pop("exact", None)



                elif c_type == "orthocenter":

                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]

                    if len(pts) == 3 and all(pts):

                        pA, pB, pC = pts

                        dx1, dy1 = -(pC["y"] - pB["y"]), pC["x"] - pB["x"]

                        dx2, dy2 = -(pC["y"] - pA["y"]), pC["x"] - pA["x"]

                        A2 = {"x": pA["x"] + dx1, "y": pA["y"] + dy1}

                        B2 = {"x": pB["x"] + dx2, "y": pB["y"] + dy2}

                        pt_h = self._intersect_lines(pA, A2, pB, B2)

                        if pt_h:

                            p["x"], p["y"] = pt_h[0], pt_h[1]



                elif c_type == "incenter":

                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]

                    if len(pts) == 3 and all(pts):

                        pA, pB, pC = pts

                        a = math.hypot(pB["x"] - pC["x"], pB["y"] - pC["y"])

                        b = math.hypot(pA["x"] - pC["x"], pA["y"] - pC["y"])

                        c_len = math.hypot(pA["x"] - pB["x"], pA["y"] - pB["y"])

                        peri = a + b + c_len

                        if peri > 1e-6:

                            p["x"] = (a * pA["x"] + b * pB["x"] + c_len * pC["x"]) / peri

                            p["y"] = (a * pA["y"] + b * pB["y"] + c_len * pC["y"]) / peri



                elif c_type == "circumcenter":

                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]

                    if len(pts) == 3 and all(pts):

                        p1, p2, p3 = pts

                        d = 2 * (p1["x"] * (p2["y"] - p3["y"]) + p2["x"] * (p3["y"] - p1["y"]) + p3["x"] * (p1["y"] - p2["y"]))

                        if abs(d) > 1e-7:

                            ux = ((p1["x"]**2 + p1["y"]**2)*(p2["y"] - p3["y"]) + (p2["x"]**2 + p2["y"]**2)*(p3["y"] - p1["y"]) + (p3["x"]**2 + p3["y"]**2)*(p1["y"] - p2["y"])) / d

                            uy = ((p1["x"]**2 + p1["y"]**2)*(p3["x"] - p2["x"]) + (p2["x"]**2 + p2["y"]**2)*(p1["x"] - p3["x"]) + (p3["x"]**2 + p3["y"]**2)*(p2["x"] - p1["x"])) / d

                            p["x"], p["y"] = ux, uy



            # 2. Cập nhật các đường tròn có ràng buộc bán kính động

            for circ in self.circles:

                c = circ.get("constraint")

                if not c:

                    continue

                c_type = c.get("type")

                if c_type == "circumcircle":

                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]

                    center = self._resolve_point(c.get("center") or circ.get("center"))

                    if pts and center and pts[0]:

                        circ["r"] = math.hypot(pts[0]["x"] - center["x"], pts[0]["y"] - center["y"])

                elif c_type == "incircle":

                    pts = [self._resolve_point(pt) for pt in c.get("pts", [])]

                    if len(pts) == 3 and all(pts):

                        pA, pB, pC = pts

                        a = math.hypot(pB["x"] - pC["x"], pB["y"] - pC["y"])

                        b = math.hypot(pA["x"] - pC["x"], pA["y"] - pC["y"])

                        c_len = math.hypot(pA["x"] - pB["x"], pA["y"] - pB["y"])

                        peri = a + b + c_len

                        area = 0.5 * abs((pB["x"] - pA["x"]) * (pC["y"] - pA["y"]) - (pB["y"] - pA["y"]) * (pC["x"] - pA["x"]))

                        if peri > 1e-6:

                            circ["r"] = area / (peri / 2.0)

                elif c_type == "circle_2p":

                    p_center = self._resolve_point(c.get("center") or circ.get("center"))

                    p_rim = self._resolve_point(c.get("p_rim"))

                    if p_center and p_rim:

                        circ["r"] = math.hypot(p_rim["x"] - p_center["x"], p_rim["y"] - p_center["y"])

            # 3. Cập nhật các hình elip động khi các điểm tiêu điểm / tâm / điểm M di chuyển
            for el in getattr(self, "ellipses", []):
                pF1 = self._resolve_point(el.get("f1"))
                pF2 = self._resolve_point(el.get("f2"))
                pM = self._resolve_point(el.get("pM"))
                if pF1 and pF2 and pM:
                    new_p = compute_ellipse_from_foci(pF1["x"], pF1["y"], pF2["x"], pF2["y"], pM["x"], pM["y"])
                    el["ox"], el["oy"] = new_p["ox"], new_p["oy"]
                    el["a"], el["b"], el["c"], el["theta"] = new_p["a"], new_p["b"], new_p["c"], new_p["theta"]
                    el["area"], el["perimeter"] = new_p["area"], new_p["perimeter"]
                else:
                    pO = self._resolve_point(el.get("center"))
                    pA = self._resolve_point(el.get("pA"))
                    pB = self._resolve_point(el.get("pB"))
                    if pO and pA and pB:
                        new_p = compute_ellipse_parameters(pO["x"], pO["y"], pA["x"], pA["y"], pB["x"], pB["y"])
                        el["ox"], el["oy"] = new_p["ox"], new_p["oy"]
                        el["a"], el["b"], el["theta"] = new_p["a"], new_p["b"], new_p["theta"]
                        el["area"], el["perimeter"] = new_p["area"], new_p["perimeter"]




```

#### (c) Cơ chế lưu trữ và phục hồi Undo/Redo (`_save_state`, `undo`, `redo`, `_restore_state`):
*Trích xuất nguyên văn từ `geosolver/geosolver_desktop.py` (Dòng 5812 đến 6029):*

```python
    def _save_state(self):

        state = {

            "points": copy.deepcopy(self.points),

            "segments": copy.deepcopy(self.segments),

            "lines": copy.deepcopy(self.lines),

            "circles": copy.deepcopy(self.circles),

            "equal_angles": copy.deepcopy(self.equal_angles),

            "angle_marks": copy.deepcopy(self.angle_marks),

            "polygons": copy.deepcopy(getattr(self, "polygons", [])),

            "ellipses": copy.deepcopy(getattr(self, "ellipses", [])),

            "problem": self.txt_problem.get("1.0", tk.END),

            "goal_type_idx": self.combo_goal_type.current() if hasattr(self, "combo_goal_type") else 0,

            "goal_type": self.combo_goal_type.get() if hasattr(self, "combo_goal_type") else "",

            "goal_targets": self.entry_goal_targets.get() if hasattr(self, "entry_goal_targets") else "",

            "scale": self.scale,

            "ox": self.origin_x,

            "oy": self.origin_y

        }

        self.undo_stack.append(state)

        if len(self.undo_stack) > 40:

            self.undo_stack.pop(0)

        self.redo_stack.clear()



    def undo(self):

        if not self.undo_stack:

            self.lbl_status.config(text="Không có thao tác nào để hoàn tác.")

            return

        curr = {

            "points": copy.deepcopy(self.points),

            "segments": copy.deepcopy(self.segments),

            "lines": copy.deepcopy(self.lines),

            "circles": copy.deepcopy(self.circles),

            "equal_angles": copy.deepcopy(self.equal_angles),

            "angle_marks": copy.deepcopy(self.angle_marks),

            "polygons": copy.deepcopy(getattr(self, "polygons", [])),

            "ellipses": copy.deepcopy(getattr(self, "ellipses", [])),

            "problem": self.txt_problem.get("1.0", tk.END),

            "goal_type_idx": self.combo_goal_type.current() if hasattr(self, "combo_goal_type") else 0,

            "goal_type": self.combo_goal_type.get(),

            "goal_targets": self.entry_goal_targets.get(),

            "scale": self.scale,

            "ox": self.origin_x,

            "oy": self.origin_y

        }

        self.redo_stack.append(curr)

        state = self.undo_stack.pop()

        self._restore_state(state)

        self.lbl_status.config(text="Đã hoàn tác (Undo).")



    def redo(self):

        if not self.redo_stack:

            self.lbl_status.config(text="Không có thao tác nào để làm lại.")

            return

        curr = {

            "points": copy.deepcopy(self.points),

            "segments": copy.deepcopy(self.segments),

            "lines": copy.deepcopy(self.lines),

            "circles": copy.deepcopy(self.circles),

            "equal_angles": copy.deepcopy(self.equal_angles),

            "angle_marks": copy.deepcopy(self.angle_marks),

            "polygons": copy.deepcopy(getattr(self, "polygons", [])),

            "ellipses": copy.deepcopy(getattr(self, "ellipses", [])),

            "problem": self.txt_problem.get("1.0", tk.END),

            "goal_type_idx": self.combo_goal_type.current() if hasattr(self, "combo_goal_type") else 0,

            "goal_type": self.combo_goal_type.get(),

            "goal_targets": self.entry_goal_targets.get(),

            "scale": self.scale,

            "ox": self.origin_x,

            "oy": self.origin_y

        }

        self.undo_stack.append(curr)

        state = self.redo_stack.pop()

        self._restore_state(state)

        self.lbl_status.config(text="Đã làm lại (Redo).")



    def _restore_state(self, state):

        self.points = state["points"]

        self.segments = state["segments"]

        self.lines = state["lines"]

        self.circles = state["circles"]

        self.equal_angles = state["equal_angles"]

        self.angle_marks = state.get("angle_marks", [])

        self.polygons = copy.deepcopy(state.get("polygons", []))

        self.ellipses = copy.deepcopy(state.get("ellipses", []))

        self.txt_problem.delete("1.0", tk.END)

        self.txt_problem.insert(tk.END, state.get("problem", ""))

        if "goal_type_idx" in state and hasattr(self, "combo_goal_type") and state["goal_type_idx"] >= 0:

            self.combo_goal_type.current(state["goal_type_idx"])

        elif "goal_type" in state and hasattr(self, "combo_goal_type"):

            try:

                self.combo_goal_type.set(state["goal_type"])

            except Exception:

                pass

        if "goal_targets" in state and hasattr(self, "entry_goal_targets"):

            self.entry_goal_targets.delete(0, tk.END)

            self.entry_goal_targets.insert(0, state["goal_targets"])

        self.scale = state.get("scale", 50.0)

        self.origin_x = state.get("ox", 450.0)

        self.origin_y = state.get("oy", 420.0)

        self.selected_points.clear()

        self.temp_points.clear()

        self.temp_line = None

        self._update_algebra_tree()

        self._scan_invariants_deep()

        self.redraw()



    # =========================================================================

    # THAO TÁC CHỌN VÀ BIẾN HÌNH (ROTATE / SELECT ALL)

    # =========================================================================


```

#### (d) Xử lý sự kiện kéo chuột trên Canvas (`_on_canvas_drag`):
*Trích xuất nguyên văn từ `geosolver/geosolver_desktop.py` (Dòng 12359 đến 12671):*

```python
    def _on_canvas_drag(self, event):

        wx, wy = self.to_world(event.x, event.y)



        # 0a. KÉO DI CHUYỂN NHÃN TÊN ĐIỂM (TÙY Ý DI CHUYỂN TRÁNH BỊ GHI ĐÈ)

        if getattr(self, "dragging_label_point", None):

            p = self.dragging_label_point

            px, py = self.to_screen(p["x"], p["y"])

            p["label_dx"] = event.x - px

            p["label_dy"] = event.y - py

            self.redraw()

            return



        # 0b. KÉO DI CHUYỂN NHÃN ĐOẠN THẲNG

        if getattr(self, "dragging_seg_label", None):

            s = self.dragging_seg_label

            x1, y1 = self.to_screen(s["p1"]["x"], s["p1"]["y"])

            x2, y2 = self.to_screen(s["p2"]["x"], s["p2"]["y"])

            base_x = (x1 + x2) / 2 + 6

            base_y = (y1 + y2) / 2 - 6

            s["label_dx"] = event.x - base_x

            s["label_dy"] = event.y - base_y

            self.redraw()

            return



        # 0c. KÉO DI CHUYỂN KÍ HIỆU HOẶC NHÃN GÓC (ĐỘ, ALPHA, VUÔNG)

        if getattr(self, "dragging_angle_mark", None):

            m = self.dragging_angle_mark

            v = m.get("vertex")

            if v:

                vx, vy = self.to_screen(v["x"], v["y"])

                mode = getattr(self, "dragging_angle_mode", "label")

                if mode == "label":

                    p1, p2 = m.get("p1"), m.get("p2")

                    if p1 and p2:

                        x1, y1 = self.to_screen(p1["x"], p1["y"])

                        x2, y2 = self.to_screen(p2["x"], p2["y"])

                        dx1, dy1 = x1 - vx, y1 - vy

                        dx2, dy2 = x2 - vx, y2 - vy

                        L1, L2 = math.hypot(dx1, dy1), math.hypot(dx2, dy2)

                        size = m.get("size", 14 if m.get("style") == "right" else 22)

                        if m.get("style") == "right" and L1 > 1e-3 and L2 > 1e-3:

                            u1x, u1y = dx1 / L1, dy1 / L1

                            u2x, u2y = dx2 / L2, dy2 / L2

                            base_tx = vx + size * u1x + size * u2x + 6

                            base_ty = vy + size * u1y + size * u2y - 6

                        elif L1 > 1e-3 and L2 > 1e-3:

                            ang1 = math.atan2(dy1, dx1)

                            ang2 = math.atan2(dy2, dx2)

                            diff = (ang2 - ang1) % (2 * math.pi)

                            if diff > math.pi: diff -= 2 * math.pi

                            mid_ang = ang1 + diff / 2.0

                            base_tx = vx + (size + 14) * math.cos(mid_ang)

                            base_ty = vy + (size + 14) * math.sin(mid_ang)

                        else:

                            base_tx, base_ty = vx + 15, vy - 15

                        m["label_dx"] = event.x - base_tx

                        m["label_dy"] = event.y - base_ty

                else:  # mode == "size"

                    new_sz = int(math.hypot(event.x - vx, event.y - vy))

                    m["size"] = max(10, min(80, new_sz))

            self.redraw()

            return



        # 1. XOAY HÌNH BẰNG CHUỘT

        if (self.current_tool == "rotate_mouse" or (event.state & 0x0001)) and self.rotate_center:

            cx, cy = self.rotate_center

            curr_angle = math.atan2(wy - cy, wx - cx)

            d_angle = curr_angle - self.rotate_start_angle



            cos_a = math.cos(d_angle)

            sin_a = math.sin(d_angle)

            for p in self.selected_points:

                dx = p["x"] - cx

                dy = p["y"] - cy

                p["x"] = cx + dx * cos_a - dy * sin_a

                p["y"] = cy + dx * sin_a + dy * cos_a



            self.rotate_start_angle = curr_angle

            self.lbl_status.config(text=f"Đang xoay toàn bộ hình theo chuột quanh tâm ({cx:.1f}; {cy:.1f})...")

            self._update_algebra_tree()

            self._scan_invariants_deep()

            self.redraw()

            return



        # 2. DI CHUYỂN CÁC ĐIỂM ĐƯỢC CHỌN (HOẶC ĐOẠN THẲNG CỐ ĐỊNH CHIỀU DÀI & GÓC)

        if self.selected_points and self.drag_start_world:

            dx = wx - self.drag_start_world[0]

            dy = wy - self.drag_start_world[1]



            # TH 1: Điểm đơn lẻ nằm trên đường tròn (on_circle)

            if len(self.selected_points) == 1 and self.selected_points[0].get("on_circle"):

                p = self.selected_points[0]

                circ = next((c for c in self.circles if c["id"] == p["on_circle"]), None)

                if circ:

                    ang = math.atan2(wy - circ["center"]["y"], wx - circ["center"]["x"])

                    p["x"] = circ["center"]["x"] + circ["r"] * math.cos(ang)

                    p["y"] = circ["center"]["y"] + circ["r"] * math.sin(ang)



                    # Cập nhật tiếp tuyến động gắn với điểm này

                    rx = p["x"] - circ["center"]["x"]

                    ry = p["y"] - circ["center"]["y"]

                    for l in self.lines:

                        if l.get("type") == "tangent_dynamic" and (l["p1"] == p or l["p2"] == p):

                            helper = l["p2"] if l["p1"] == p else l["p1"]

                            helper["x"] = p["x"] - ry

                            helper["y"] = p["y"] + rx



            # TH 2: Điểm đơn lẻ có ràng buộc trượt trên đoạn thẳng hoặc đường thẳng

            elif len(self.selected_points) == 1 and self.selected_points[0].get("constraint") and self.selected_points[0]["constraint"].get("type") in ("on_segment", "on_line"):

                p = self.selected_points[0]

                c = p["constraint"]

                p1 = self._resolve_point(c.get("p1"))

                p2 = self._resolve_point(c.get("p2"))

                if p1 and p2:

                    dx_seg = p2["x"] - p1["x"]

                    dy_seg = p2["y"] - p1["y"]

                    L2 = dx_seg * dx_seg + dy_seg * dy_seg

                    if L2 > 1e-9:

                        t = ((wx - p1["x"]) * dx_seg + (wy - p1["y"]) * dy_seg) / L2

                        if c.get("type") == "on_segment":

                            t = max(0.0, min(1.0, t))

                        c["t"] = t

                        p["x"] = p1["x"] + t * dx_seg

                        p["y"] = p1["y"] + t * dy_seg



            # TH 3: Điểm đơn lẻ là trung điểm (khi kéo trực tiếp trung điểm M, cả 2 đầu mút đoạn di chuyển theo)

            elif len(self.selected_points) == 1 and self.selected_points[0].get("constraint") and self.selected_points[0]["constraint"].get("type") == "midpoint":

                p = self.selected_points[0]

                c = p["constraint"]

                p1 = self._resolve_point(c.get("p1"))

                p2 = self._resolve_point(c.get("p2"))

                p["x"] += dx

                p["y"] += dy

                if p1 and p2:

                    p1["x"] += dx

                    p1["y"] += dy

                    p2["x"] += dx

                    p2["y"] += dy



            else:

                # Dời các điểm được chọn (nếu chọn đoạn thẳng thì cả 2 đầu mút dời cùng dx, dy => giữ nguyên 100% độ dài & góc!)

                for p in self.selected_points:
                    p["x"] += dx
                    p["y"] += dy
                    if self.snap_to_grid:
                        step = getattr(self, "grid_step", 0.5)
                        p["x"] = round(p["x"] / step) * step
                        p["y"] = round(p["y"] / step) * step
                        p["source"] = "grid_snap"
                        p["exact"] = True
                    else:
                        p["source"] = "dragged"
                        p["exact"] = False



            # Lan truyền cập nhật cho các đối tượng phụ thuộc khác (Dynamic Constraint Propagation)

            self._recompute_dependent_objects(exclude_points=self.selected_points)



            self.drag_start_world = (wx, wy)

            self._update_algebra_tree()

            self._scan_invariants_deep()

            self.redraw()




```

### 3.3. Bảo mật DPAPI & Kết nối HTTPS an toàn

#### (a) Mã hóa/Giải mã DPAPI và Lớp Lưu trữ `GeminiKeyStore`:
*Trích xuất nguyên văn từ `stem_shared_core/ai_local_manager.py` (Dòng 125 đến 310):*

```python
# =============================================================================
# KHÓA API GEMINI
# =============================================================================

class _DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.c_ulong), ("pbData", ctypes.POINTER(ctypes.c_byte))]

if os.name == "nt":
    try:
        _crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
        _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        _crypt32.CryptProtectData.argtypes = [
            ctypes.POINTER(_DATA_BLOB), ctypes.c_wchar_p, ctypes.POINTER(_DATA_BLOB),
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_DATA_BLOB)
        ]
        _crypt32.CryptProtectData.restype = ctypes.c_int

        _crypt32.CryptUnprotectData.argtypes = [
            ctypes.POINTER(_DATA_BLOB), ctypes.POINTER(ctypes.c_wchar_p), ctypes.POINTER(_DATA_BLOB),
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_DATA_BLOB)
        ]
        _crypt32.CryptUnprotectData.restype = ctypes.c_int

        _kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        _kernel32.LocalFree.restype = ctypes.c_void_p
    except Exception:
        pass

def _dpapi_encrypt(data: bytes) -> bytes:
    if os.name != "nt":
        raise OSError("Windows DPAPI chỉ khả dụng trên hệ điều hành Windows.")
    # FIX Use-After-Free: Gán buffer vào biến 'buf' để giữ reference trong suốt thời gian gọi API
    buf = ctypes.create_string_buffer(data)
    blob_in = _DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))
    blob_out = _DATA_BLOB()
    if _crypt32.CryptProtectData(
        ctypes.byref(blob_in), "STEM_AI_KEY", None, None, None, 0, ctypes.byref(blob_out)
    ):
        out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        _kernel32.LocalFree(blob_out.pbData)
        return out
    err = ctypes.get_last_error()
    raise ctypes.WinError(err)

def _dpapi_decrypt(data: bytes) -> bytes:
    if os.name != "nt":
        raise OSError("Windows DPAPI chỉ khả dụng trên hệ điều hành Windows.")
    # FIX Use-After-Free: Gán buffer vào biến 'buf' để giữ reference trong suốt thời gian gọi API
    buf = ctypes.create_string_buffer(data)
    blob_in = _DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))
    blob_out = _DATA_BLOB()
    if _crypt32.CryptUnprotectData(
        ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)
    ):
        out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        _kernel32.LocalFree(blob_out.pbData)
        return out
    err = ctypes.get_last_error()
    raise ctypes.WinError(err)

_LOGGER_INITIALIZED = False

def _init_logger():
    global _LOGGER_INITIALIZED
    if _LOGGER_INITIALIZED:
        return
    import logging
    from logging.handlers import RotatingFileHandler
    try:
        base = os.environ.get("LOCALAPPDATA")
        root = Path(base) if base else Path.home() / ".local" / "share"
        log_dir = root / "AIMathHub" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "geosolver.log"
        handler = RotatingFileHandler(str(log_file), maxBytes=1024 * 1024, backupCount=3, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger = logging.getLogger("geosolver")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            logger.addHandler(handler)
        _LOGGER_INITIALIZED = True
    except Exception:
        pass

def _log_warning(msg: str, *args):
    """Ghi log cảnh báo an toàn ra rotating file log cục bộ của geosolver."""
    _init_logger()
    import logging
    try:
        logging.getLogger("geosolver").warning(msg, *args)
    except Exception:
        pass

def _log_info(msg: str, *args):
    """Ghi log thông tin an toàn ra rotating file log cục bộ của geosolver."""
    _init_logger()
    import logging
    try:
        logging.getLogger("geosolver").info(msg, *args)
    except Exception:
        pass


class GeminiKeyStore:
    """Đọc và lưu gemini_api_key.txt an toàn với Windows DPAPI (CryptProtectData)."""

    def __init__(self, key_file: Path) -> None:
        self.key_file: Path = key_file
        self.last_warning: str | None = None

    def read(self) -> str | None:
        """Đọc khóa API (giải mã Windows DPAPI hoặc nâng cấp khóa cũ).
        Nguyên tắc fail-soft tại ranh giới người dùng: Bắt lỗi khi tệp bị sao chép sang máy khác
        (SID khác), tài khoản Windows thay đổi hoặc dữ liệu bị hỏng; ghi log warning ra file và fallback
        về biến môi trường thay vì làm sập ứng dụng lúc khởi động.
        """
        self.last_warning = None
        if self.key_file.is_file():
            try:
                content = self.key_file.read_text(encoding="utf-8").strip()
                if content.startswith("DPAPI:"):
                    raw_b64 = content[6:]
                    encrypted_bytes = base64.b64decode(raw_b64)
                    decrypted = _dpapi_decrypt(encrypted_bytes).decode("utf-8").strip()
                    return decrypted or None
                elif content:
                    # Nâng cấp khóa văn bản thường cũ lên DPAPI tự động trên Windows
                    # Lưu ý đa nền tảng: Chỉ tự nâng cấp khi chạy trên Windows NT
                    if os.name == "nt":
                        try:
                            self.save(content)
                            _log_info("Tự động nâng cấp khóa API plaintext sang Windows DPAPI thành công.")
                        except Exception as e:
                            _log_warning("Không thể nâng cấp khóa plaintext sang DPAPI (%s); khóa vẫn lưu ở dạng thô.", e)
                    return content
            except Exception as e:
                self.last_warning = f"DPAPI decryption failed ({e}); falling back to environment variable"
                _log_warning("%s", self.last_warning)
        env_value = os.environ.get("GEMINI_API_KEY", "").strip()
        return env_value or None

    def save(self, api_key: str) -> None:
        """Lưu khóa API an toàn bằng Windows DPAPI (CryptProtectData).
        Sử dụng cơ chế ghi nguyên tử (atomic write qua file tạm có f.flush() + os.fsync())
        để chống hỏng file khi mất nguồn đột ngột, và áp dụng chmod 0o600 trên nền tảng POSIX.
        """
        cleaned = api_key.strip()
        if not cleaned:
            raise ValueError("Khóa API rỗng, không thể lưu.")
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            enc = _dpapi_encrypt(cleaned.encode("utf-8"))
            payload = "DPAPI:" + base64.b64encode(enc).decode("ascii")
        else:
            payload = cleaned

        tmp_fd, tmp_path = tempfile.mkstemp(dir=self.key_file.parent, prefix="gemini_key_", suffix=".tmp")
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(payload)
                f.flush()
                os.fsync(f.fileno())  # Flush xuống đĩa vật lý trước khi rename
            if os.name != "nt":
                try:
                    os.chmod(tmp_path, 0o600)
                except Exception:
                    pass
            os.replace(tmp_path, self.key_file)
            if os.name != "nt":
                try:
                    os.chmod(self.key_file, 0o600)
                except Exception:
                    pass
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass


# =============================================================================
# THEO DÕI RAM
# =============================================================================


```

#### (b) Khởi tạo Ngữ cảnh Bảo mật SSL/TLS với CA Bundle certifi (`_get_ssl_context`):
*Trích xuất nguyên văn từ `stem_shared_core/ai_local_manager.py` (Dòng 721 đến 734):*

```python
def _get_ssl_context():
    """Tạo SSLContext kế thừa chứng chỉ hệ thống Windows và bổ sung CA bundle certifi."""
    import ssl
    ctx = ssl.create_default_context()
    try:
        import certifi
        ca = certifi.where()
        if os.path.isfile(ca):
            ctx.load_verify_locations(cafile=ca)
    except Exception:
        pass
    return ctx



```

### 3.4. Toàn văn Cấu hình Đóng gói Production

#### (a) Toàn văn cấu hình PyInstaller (`geosolver/GeoSolver.spec`):
```python
# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

# SPECPATH đã là thư mục chứa file .spec (d:\AI DATA\STEM_APP\geosolver)
BASE = os.path.abspath(SPECPATH)
ROOT = os.path.dirname(BASE)

block_cipher = None

# Lọc bỏ các submodule test của sympy/mpmath để tối ưu kích thước gói
hidden_imports = (
    collect_submodules('sympy', filter=lambda n: '.tests' not in n)
    + collect_submodules('mpmath', filter=lambda n: '.tests' not in n)
    + [
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'stem_shared_core',
        'stem_shared_core.ai_model_hub',
        'stem_shared_core.hf_downloader',
        'stem_shared_core.ai_config_dialog',
        'stem_handbook_dialog',
    ]
)

a = Analysis(
    [os.path.join(BASE, 'geosolver_desktop.py')],
    pathex=[BASE, ROOT],
    binaries=[],
    datas=[
        (os.path.join(BASE, 'assets'), 'assets'),
        (os.path.join(ROOT, 'CAM_NANG_SU_DUNG_STEM_CAD_MATH.md'), '.'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter.test', 'test'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GeoSolver',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=os.path.join(BASE, 'file_version_info.txt'),
    icon=[os.path.join(BASE, 'assets', 'app.ico')],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='GeoSolver',
)

```

#### (b) Toàn văn AppX Manifest (`msix_layout/AppxManifest.xml`):
```xml
<?xml version="1.0" encoding="utf-8"?>
<Package
  xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
  xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
  xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities">

  <Identity
    Name="TLabtool.GeoSolverCAD"
    Publisher="CN=CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE"
    Version="3.1.0.0"
    ProcessorArchitecture="x64" />

  <Properties>
    <DisplayName>GeoSolver CAD</DisplayName>
    <PublisherDisplayName>TLabtool</PublisherDisplayName>
    <Logo>Assets\StoreLogo.png</Logo>
    <Description>GeoSolver CAD - Cong cu dung hinh va giai toan hinh hoc tu dong chuan Olympic VMO va THCS/THPT.</Description>
  </Properties>

  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.22621.0" />
  </Dependencies>

  <Resources>
    <Resource Language="vi-VN" />
    <Resource Language="en-US" />
  </Resources>

  <Applications>
    <Application Id="GeoSolverApp"
      Executable="VFS\GeoSolver.exe"
      EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements
        DisplayName="GeoSolver CAD"
        Description="Interactive Dynamic Geometry CAD and SymPy CAS Solver"
        BackgroundColor="transparent"
        Square150x150Logo="Assets\Square150x150Logo.png"
        Square44x44Logo="Assets\Square44x44Logo.png">
        <uap:DefaultTile Wide310x150Logo="Assets\Wide310x150Logo.png" />
      </uap:VisualElements>
    </Application>
  </Applications>

  <Capabilities>
    <rescap:Capability Name="runFullTrust" />
  </Capabilities>
</Package>



```

---

## 4. TOÀN VĂN BỘ KIỂM THỬ TỰ ĐỘNG (VERBATIM 100%)

### 4.1. Toàn văn Các Bài Test Tích hợp Canvas GUI, Taint, Undo/Redo & Hoán vị (Tests 24 đến 32)
*Trích xuất nguyên văn từ `tests/test_geometry_invariants.py` (Dòng 423 đến 1021):*

```python
    def test_24_gui_canvas_point_source_and_invariants_integration(self):
        """Kiểm tra tích hợp GUI Canvas: phát sự kiện click chuột thật để kiểm tra gán cờ source='free' và 'grid_snap'"""
        from geosolver.geosolver_desktop import GeoSolverApp
        import tkinter as tk
        app = None
        errors = []
        try:
            app = GeoSolverApp(with_splash=False)
            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
            app.current_tool = "point"
            app.update()  # Map canvas lên Tkinter display pipeline

            # 1. Phát sự kiện click chuột thật khi KHÔNG bật snap_to_grid -> phải sinh ra source='free', exact=False
            app.snap_to_grid = False
            app._ask_point_name_dialog = lambda default_name: "P_free"
            app.canvas.event_generate("<ButtonPress-1>", x=150, y=150)
            app.update()

            self.assertTrue(len(app.points) >= 1, "Phát sự kiện <ButtonPress-1> phải sinh ra điểm trên Canvas")
            p_free = app.points[-1]
            self.assertEqual(p_free["source"], "free", "Click tự do không snap bắt buộc sinh ra source='free'")
            self.assertFalse(p_free["exact"], "Điểm sinh ra từ click chuột tự do bắt buộc có exact=False")

            # 2. Phát sự kiện click chuột thật khi BẬT snap_to_grid -> phải sinh ra source='grid_snap', exact=True
            app.snap_to_grid = True
            app._ask_point_name_dialog = lambda default_name: "P_snap"
            app.canvas.event_generate("<ButtonPress-1>", x=200, y=200)
            app.update()

            self.assertTrue(len(app.points) >= 2)
            p_snap = app.points[-1]
            self.assertEqual(p_snap["source"], "grid_snap", "Click khi bật snap bắt buộc sinh ra source='grid_snap'")
            self.assertTrue(p_snap["exact"], "Điểm sinh ra từ snap lưới bắt buộc có exact=True")

            # 3. Dựng tam giác từ điểm vẽ chuột tự do và quét bất biến
            app.points = [
                {"id": "A", "name": "A", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False},
                {"id": "B", "name": "B", "x": 3.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False},
                {"id": "C", "name": "C", "x": 0.0, "y": 4.0, "color": "#000", "fixed": False, "source": "free", "exact": False}
            ]
            app._scan_invariants_deep()
            invariants_text = app.txt_invariants.get("1.0", tk.END)
            self.assertIn("Tam giác vuông tại A", invariants_text)

            res = classify_triangle(app.points[0], app.points[1], app.points[2])
            self.assertFalse(res["exact"], "Điểm vẽ tự do từ Canvas GUI bắt buộc cho kết quả exact=False dù tọa độ nguyên")

            # 4. Kiểm tra kéo thả điểm (drag event): Điểm grid_snap bị kéo tự do khi tắt snap phải đổi thành source='dragged', exact=False
            app.snap_to_grid = False
            app.selected_points = [p_snap]
            app.drag_start_world = (p_snap["x"], p_snap["y"])
            app.canvas.event_generate("<B1-Motion>", x=250, y=250)
            app.update()
            self.assertEqual(p_snap["source"], "dragged", "Điểm bị kéo tự do bắt buộc đổi source='dragged'")
            self.assertFalse(p_snap["exact"], "Điểm bị kéo tự do bắt buộc có exact=False")
            self.assertEqual(errors, [], f"Không được có ngoại lệ trong Tkinter callback: {errors}")
        finally:
            if app is not None:
                app.destroy()

    def test_25_gui_canvas_drag_typed_and_midpoint_parents_integration(self):
        """Kiểm tra Canvas GUI: Kéo điểm typed khi snap tắt thành dragged, và tạo trung điểm từ 2 điểm free lưu parents"""
        from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
        app = None
        errors = []
        try:
            app = GeoSolverApp(with_splash=False)
            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
            app.update()

            # 1. Kéo điểm typed khi snap tắt -> source thành 'dragged', exact=False
            p_typed = {"id": "T1", "name": "T1", "x": 10.0, "y": 10.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            app.points = [p_typed]
            app.snap_to_grid = False
            app.selected_points = [p_typed]
            app.drag_start_world = (10.0, 10.0)
            app.canvas.event_generate("<B1-Motion>", x=320, y=320)
            app.update()

            self.assertEqual(p_typed["source"], "dragged", "Kéo điểm typed khi snap_to_grid=False phải đổi source thành 'dragged'")
            self.assertFalse(p_typed["exact"], "Điểm typed sau khi bị kéo tự do bắt buộc có exact=False")

            # 2. Tạo trung điểm từ 2 điểm vẽ chuột tự do (free) thông qua công cụ 'midpoint' của Canvas
            p_free1 = {"id": "F1", "name": "F1", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False}
            p_free2 = {"id": "F2", "name": "F2", "x": 4.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False}
            app.points = [p_free1, p_free2]
            app.redraw()
            app.current_tool = "midpoint"
            app._ask_point_name_dialog = lambda default_name: "Mid_Free"

            sx1, sy1 = app.to_screen(p_free1["x"], p_free1["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sx1), y=int(sy1))
            app.update()

            sx2, sy2 = app.to_screen(p_free2["x"], p_free2["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sx2), y=int(sy2))
            app.update()

            self.assertEqual(len(app.points), 3, "Công cụ midpoint phải tạo thêm điểm thứ 3 trên Canvas")
            m_pt = app.points[-1]
            self.assertEqual(m_pt["source"], "midpoint")
            self.assertIn("parents", m_pt, "Điểm trung điểm bắt buộc phải lưu thuộc tính 'parents'")
            self.assertEqual(m_pt["parents"], [p_free1, p_free2], "parents phải chứa đúng 2 đối tượng điểm cha")

            # 3. Phân loại tam giác có chứa điểm trung điểm tạo từ 2 điểm free
            p_ext = {"id": "C", "name": "C", "x": 2.0, "y": 3.0, "source": "typed", "exact": True}
            res = classify_triangle(m_pt, p_free1, p_ext)
            self.assertFalse(res["exact"], "Tam giác có đỉnh là trung điểm kế thừa taint từ cha free bắt buộc exact=False")
            self.assertFalse(res["is_discrete"], "Điểm tainted bắt buộc đi vào nhánh liên tục (is_discrete=False)")
            self.assertIs(res["origin_exact"], False)
            self.assertEqual(errors, [], f"Không được có ngoại lệ trong Tkinter callback: {errors}")
        finally:
            if app is not None:
                app.destroy()

    def test_26_nested_constructions_multi_level_taint(self):
        """Kiểm tra dựng hình lồng nhau nhiều tầng (Nested derived points): Lan truyền taint qua nhiều cấp cha-con"""
        from geosolver.geosolver_desktop import classify_triangle

        # Cấp 0 (Lá gốc)
        p_free_A = {"x": 0.0, "y": 0.0, "source": "free", "exact": False}
        p_free_B = {"x": 4.0, "y": 0.0, "source": "free", "exact": False}
        p_typed_C = {"x": 0.0, "y": 4.0, "source": "typed", "exact": True}
        p_typed_D = {"x": 4.0, "y": 4.0, "source": "typed", "exact": True}

        # Cấp 1
        m_tainted_1 = {"x": 2.0, "y": 0.0, "source": "midpoint", "parents": [p_free_A, p_free_B]}
        m_clean_1 = {"x": 2.0, "y": 4.0, "source": "midpoint", "parents": [p_typed_C, p_typed_D]}

        # Cấp 2: Trung điểm của 2 trung điểm (một bên sạch, một bên bẩn)
        m_nested_tainted = {"x": 2.0, "y": 2.0, "source": "midpoint", "parents": [m_tainted_1, m_clean_1]}
        # Cấp 2 sạch hoàn toàn: Trung điểm của 2 điểm typed
        p_typed_E = {"x": 0.0, "y": 8.0, "source": "typed", "exact": True}
        m_nested_clean = {"x": 1.0, "y": 6.0, "source": "midpoint", "parents": [m_clean_1, p_typed_E]}

        # Kiểm tra tam giác với điểm lồng bẩn cấp 2
        res_tainted = classify_triangle(m_nested_tainted, p_typed_C, p_typed_D)
        self.assertIs(res_tainted["origin_exact"], False, "Cờ False phải lan truyền qua 2 tầng trung điểm lồng nhau")
        self.assertFalse(res_tainted["exact"])
        self.assertFalse(res_tainted["is_discrete"])

        # Kiểm tra tam giác với điểm lồng sạch cấp 2
        res_clean = classify_triangle(m_nested_clean, p_typed_C, p_typed_D)
        self.assertIs(res_clean["origin_exact"], True, "Dựng hình lồng nhau nếu toàn bộ tổ tiên là typed phải giữ exact=True")
        self.assertTrue(res_clean["exact"])

    def test_27_none_and_string_and_invalid_type_rejection(self):
        """Kiểm tra xử lý ngoại lệ: Từ chối None, chuỗi '3.5', int và kiểu không hợp lệ ném ValueError chuẩn"""
        from geosolver.geosolver_desktop import classify_triangle

        # None ở tham số đầu
        with self.assertRaises(ValueError) as cm:
            classify_triangle(None, (1, 0), (0, 1))
        self.assertIn("None", str(cm.exception))

        # None ở tham số thứ 2
        with self.assertRaises(ValueError):
            classify_triangle((0, 0), None, (0, 1))

        # Chuỗi số '3.5' trong tuple
        with self.assertRaises(ValueError) as cm:
            classify_triangle(("3.5", 0), (1, 0), (0, 1))
        self.assertIn("không được là chuỗi", str(cm.exception))

        # Chuỗi số '3.5' trong dict
        with self.assertRaises(ValueError) as cm:
            classify_triangle({"x": "3.5", "y": 0}, (1, 0), (0, 1))
        self.assertIn("không được là chuỗi", str(cm.exception))

        # Số nguyên int trực tiếp không phải sequence
        with self.assertRaises(ValueError) as cm:
            classify_triangle(12345, (1, 0), (0, 1))
        self.assertIn("dict hoặc sequence", str(cm.exception))

    def test_28_drag_with_snap_on_snaps_absolute_coordinates(self):
        """Kiểm tra Canvas GUI: Kéo điểm tự do (lệch lưới) khi snap bật phải bắt tuyệt đối vào bội số của lưới"""
        from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
        app = None
        errors = []
        try:
            app = GeoSolverApp(with_splash=False)
            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
            app.update()

            # Điểm tự do vốn có tọa độ lệch lưới (3.025, 4.025)
            p_free = {
                "id": "P_Free", "name": "Free1",
                "x": 3.025, "y": 4.025,
                "color": "#000", "fixed": False,
                "source": "free", "exact": False
            }
            app.points = [p_free]
            app.snap_to_grid = True
            app.grid_step = 0.5
            app.selected_points = [p_free]
            app.drag_start_world = (3.025, 4.025)

            # Mô phỏng kéo chuột dời một lượng dx = 0.5, dy = 0.5
            sx, sy = app.to_screen(3.525, 4.525)
            app.canvas.event_generate("<B1-Motion>", x=int(sx), y=int(sy))
            app.update()

            # Tọa độ sau kéo phải được làm tròn tuyệt đối vào lưới 0.5, không được giữ phần dư .025
            self.assertEqual(p_free["x"] % 0.5, 0.0, f"x={p_free['x']} phải là bội số của grid_step=0.5")
            self.assertEqual(p_free["y"] % 0.5, 0.0, f"y={p_free['y']} phải là bội số của grid_step=0.5")
            self.assertEqual(p_free["source"], "grid_snap", "Khi snap bật, kéo điểm phải gán source='grid_snap'")
            self.assertTrue(p_free["exact"], "Khi snap bật, kéo điểm phải gán exact=True")
            self.assertEqual(errors, [], f"Không được có ngoại lệ trong Tkinter callback: {errors}")
        finally:
            if app is not None:
                app.destroy()

    def test_29_depth_limit_and_memoization_point_flag(self):
        """Kiểm tra _point_flag: Phát hiện chu trình bằng _visiting, không taint giả cây sạch 10 tầng, bảo vệ đệ quy sâu >= 100, và memoization O(1)"""
        import time
        from geosolver.geosolver_desktop import _point_flag

        # 1. Cây phụ thuộc sạch 10 tầng (depth 10) toàn bộ là typed -> phải giữ True (không bị taint giả)
        cur_clean = {"id": "P0", "source": "typed", "exact": True}
        for i in range(1, 11):
            cur_clean = {"id": f"P{i}", "source": "midpoint", "parents": [cur_clean, cur_clean]}
        flag_clean = _point_flag(cur_clean)
        self.assertIs(flag_clean, True, "Cây phụ thuộc sạch 10 tầng toàn bộ typed bắt buộc trả về True")

        # 2. Kiểm tra chuỗi phụ thuộc vượt quá ngưỡng an toàn (_depth >= 100) trả về False để chống tràn stack
        cur_deep = {"id": "D0", "source": "typed", "exact": True}
        for i in range(1, 102):
            cur_deep = {"id": f"D{i}", "source": "midpoint", "parents": [cur_deep, cur_deep]}
        flag_deep = _point_flag(cur_deep)
        self.assertIs(flag_deep, False, "Cây phụ thuộc vượt quá ngưỡng sâu an toàn (>=100) phải trả về False để chống tràn ngăn xếp")

        # 3. Kiểm tra bảo vệ chu trình (cycle / self-reference qua tập _visiting)
        p_cycle_a = {"id": "C_A", "source": "midpoint", "parents": []}
        p_cycle_b = {"id": "C_B", "source": "midpoint", "parents": [p_cycle_a]}
        p_cycle_a["parents"] = [p_cycle_b]
        # Không được ném RecursionError, kết thúc an toàn và trả về False
        flag_cycle = _point_flag(p_cycle_a)
        self.assertIs(flag_cycle, False, "Chu trình đệ quy phải kết thúc an toàn qua tập _visiting và trả về False")

        # 4. Kiểm tra hiệu năng memoization trên đồ thị kim cương (DAG)
        base = {"id": "Root", "source": "typed", "exact": True}
        layer = [base]
        for l in range(6):
            next_layer = []
            for i in range(len(layer) + 1):
                parents = []
                if i < len(layer):
                    parents.append(layer[i])
                if i > 0:
                    parents.append(layer[i - 1])
                node = {"id": f"L{l}_{i}", "source": "midpoint", "parents": parents}
                next_layer.append(node)
            layer = next_layer
        top_node = layer[len(layer) // 2]

        t0 = time.perf_counter()
        for _ in range(100):
            res = _point_flag(top_node)
        elapsed = time.perf_counter() - t0
        self.assertIs(res, True)
        self.assertLess(elapsed, 0.05, f"Memoization phải hoàn thành 100 lần duyệt DAG trong < 0.05s, thực tế: {elapsed:.4f}s")

    def test_30_undo_redo_parent_taint_propagation(self):
        """Kiểm tra Canvas GUI: Undo/Redo khôi phục liên kết cha-con, thay thế instance mới, và lan truyền tọa độ + taint khi điểm cha bị kéo"""
        from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
        app = None
        errors = []
        try:
            app = GeoSolverApp(with_splash=False)
            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
            app.update()

            # Tạo 2 điểm typed ban đầu
            pA = {"id": "P_A", "name": "A", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            pB = {"id": "P_B", "name": "B", "x": 4.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            app.points = [pA, pB]
            app.redraw()
            app.current_tool = "midpoint"
            app._ask_point_name_dialog = lambda default_name: "M_AB"

            sxA, syA = app.to_screen(pA["x"], pA["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sxA), y=int(syA))
            app.update()

            sxB, syB = app.to_screen(pB["x"], pB["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sxB), y=int(syB))
            app.update()

            self.assertEqual(len(app.points), 3)
            pM = app.points[2]
            self.assertEqual(pM["name"], "M_AB")
            self.assertEqual(pM["source"], "midpoint")

            # Lưu instance gốc trước undo/redo
            pA_orig = app.points[0]
            pB_orig = app.points[1]
            pM_orig = app.points[2]

            # Kiểm tra tam giác với điểm C typed ban đầu: cả 3 điểm đều sạch
            pC = {"id": "P_C", "name": "C", "x": 2.0, "y": 4.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            res_before = classify_triangle(pM, pA, pC)
            self.assertIs(res_before["origin_exact"], True, "Trước khi kéo, tam giác gồm điểm dựng hình sạch phải có origin_exact=True")
            self.assertTrue(res_before["exact"])

            # Thực hiện Undo -> điểm M_AB bị xóa khỏi danh sách points (hoàn tác thao tác tạo trung điểm)
            app.undo()
            app.update()
            self.assertEqual(len(app.points), 2, "Undo tạo trung điểm phải đưa danh sách điểm về 2")

            # Thực hiện Redo -> điểm M_AB được phục hồi
            app.redo()
            app.update()
            self.assertEqual(len(app.points), 3, "Redo phải khôi phục lại đủ 3 điểm")

            # Sau Redo, lấy lại tham chiếu điểm từ app.points
            pA_restored = app.points[0]
            pB_restored = app.points[1]
            pM_restored = app.points[2]

            # Kiểm tra thay thế instance: đối tượng restored phải là instance mới, không phải đối tượng cũ
            self.assertIsNot(pA_restored, pA_orig, "Undo/redo phải thay thế instance pA bằng dict mới khôi phục")
            self.assertIsNot(pB_restored, pB_orig, "Undo/redo phải thay thế instance pB bằng dict mới khôi phục")
            self.assertIsNot(pM_restored, pM_orig, "Undo/redo phải thay thế instance pM bằng dict mới khôi phục")

            # Kiểm tra parents đã được re-bind sau Redo tới đúng instance mới
            self.assertIn("parents", pM_restored)
            self.assertIs(pM_restored["parents"][0], pA_restored, "parents[0] phải trỏ tới đúng instance pA sống trên Canvas sau redo")
            self.assertIs(pM_restored["parents"][1], pB_restored, "parents[1] phải trỏ tới đúng instance pB sống trên Canvas sau redo")

            # Kéo điểm cha pA_restored khi snap tắt -> kiểm tra tọa độ pM di chuyển theo và nhận taint
            app.snap_to_grid = False
            app.selected_points = [pA_restored]
            app.drag_start_world = (pA_restored["x"], pA_restored["y"])
            dx_drag, dy_drag = 1.234, 0.567
            sx_drag, sy_drag = app.to_screen(pA_restored["x"] + dx_drag, pA_restored["y"] + dy_drag)
            app.canvas.event_generate("<B1-Motion>", x=int(sx_drag), y=int(sy_drag))
            app.update()

            # Xác minh pA đã bị vấy bẩn (dragged, exact=False)
            self.assertEqual(pA_restored["source"], "dragged")
            self.assertFalse(pA_restored["exact"])

            # Điểm trung điểm pM_restored phải tự động di chuyển tọa độ theo công thức trung điểm (pA + pB)/2
            expected_mx = (pA_restored["x"] + pB_restored["x"]) / 2.0
            expected_my = (pA_restored["y"] + pB_restored["y"]) / 2.0
            self.assertAlmostEqual(pM_restored["x"], expected_mx, places=5, msg="Tọa độ x của trung điểm phải tự động chạy theo cha pA")
            self.assertAlmostEqual(pM_restored["y"], expected_my, places=5, msg="Tọa độ y của trung điểm phải tự động chạy theo cha pA")

            # Điểm trung điểm pM_restored nhận diện vết dơ từ cha
            res_after_drag = classify_triangle(pM_restored, pB_restored, pC)
            self.assertIs(res_after_drag["origin_exact"], False, "Sau khi điểm cha bị kéo tự do, điểm con dựng hình phải bị vấy bẩn (origin_exact=False)")
            self.assertFalse(res_after_drag["exact"], "exact phải là False khi có điểm vấy bẩn trong tam giác")
            self.assertEqual(errors, [], f"Không được có ngoại lệ trong Tkinter callback: {errors}")
        finally:
            if app is not None:
                app.destroy()

    def test_31_permutation_invariance_all_six_orderings(self):
        """Kiểm tra bất biến hoán vị tuyệt đối trên cả 2 nhánh (Rời rạc & Liên tục): Thử cả 6 hoán vị của 3 đỉnh cho mọi loại tam giác"""
        import itertools
        from geosolver.geosolver_desktop import classify_triangle

        # --- PHẦN 1: NHÁNH RỜI RẠC (DISCRETE - Số nguyên & Thập phân sạch) ---
        cases_discrete = [
            # 1. Tam giác vuông tại B: A(0,0), B(4,0), C(4,3)
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0},
                           {"name": "B", "x": 4.0, "y": 0.0},
                           {"name": "C", "x": 4.0, "y": 3.0}],
                "expected_type": "right",
                "apex_node": "B"
            },
            # 2. Tam giác cân tại B: A(-3,0), B(0,5), C(3,0)
            {
                "points": [{"name": "A", "x": -3.0, "y": 0.0},
                           {"name": "B", "x": 0.0, "y": 5.0},
                           {"name": "C", "x": 3.0, "y": 0.0}],
                "expected_type": "isosceles",
                "apex_node": "B"
            },
            # 3. Tam giác vuông cân tại C: A(0,4), B(4,0), C(0,0)
            {
                "points": [{"name": "A", "x": 0.0, "y": 4.0},
                           {"name": "B", "x": 4.0, "y": 0.0},
                           {"name": "C", "x": 0.0, "y": 0.0}],
                "expected_type": "right_isosceles",
                "apex_node": "C"
            },
            # 4. Tam giác đều: A(0,0), B(2,0), C(1, √3) -> y vô tỉ nên tự chuyển liên tục
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0},
                           {"name": "B", "x": 2.0, "y": 0.0},
                           {"name": "C", "x": 1.0, "y": math.sqrt(3)}],
                "expected_type": "equilateral",
                "apex_node": None
            },
            # 5. Tam giác thường (Claude scale test 1000 vs 1010): A(0,0), B(10,30), C(29,13)
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0},
                           {"name": "B", "x": 10.0, "y": 30.0},
                           {"name": "C", "x": 29.0, "y": 13.0}],
                "expected_type": "scalene",
                "apex_node": None
            },
            # 6. Tam giác thon dài rời rạc (Needle triangle): A(0,0), B(100,0), C(50,0.5)
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0},
                           {"name": "B", "x": 100.0, "y": 0.0},
                           {"name": "C", "x": 50.0, "y": 0.5}],
                "expected_type": "isosceles",
                "apex_node": "C"
            }
        ]

        for case in cases_discrete:
            pts = case["points"]
            expected_type = case["expected_type"]
            expected_apex = case["apex_node"]

            # Thử tất cả 6 hoán vị (P1, P2, P3)
            for perm in itertools.permutations(pts):
                p1, p2, p3 = perm
                res = classify_triangle(p1, p2, p3)
                self.assertTrue(res["is_triangle"], f"Hoán vị {p1['name']},{p2['name']},{p3['name']} phải là tam giác")
                self.assertEqual(res["type"], expected_type, 
                                 f"Hoán vị {p1['name']},{p2['name']},{p3['name']} phải có type={expected_type}, thực tế={res['type']}")
                if expected_apex is not None:
                    self.assertEqual(res["vertex"], expected_apex,
                                     f"Đỉnh đặc biệt phải luôn là {expected_apex} bất kể thứ tự truyền vào")
                else:
                    self.assertIsNone(res["vertex"])

        # --- PHẦN 2: NHÁNH LIÊN TỤC (CONTINUOUS - Ép qua source='free') & CA KIM CHUẨN HÓA L_MAX^2 ---
        cases_continuous = [
            # 1. Vuông tại B qua dung sai góc
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
                           {"name": "B", "x": 4.0, "y": 0.0, "source": "free"},
                           {"name": "C", "x": 4.0, "y": 3.0, "source": "free"}],
                "expected_type": "right",
                "apex_node": "B"
            },
            # 2. Cân tại B qua dung sai cạnh 0.6%
            {
                "points": [{"name": "A", "x": -3.0, "y": 0.0, "source": "free"},
                           {"name": "B", "x": 0.0, "y": 5.0, "source": "free"},
                           {"name": "C", "x": 3.0, "y": 0.0, "source": "free"}],
                "expected_type": "isosceles",
                "apex_node": "B"
            },
            # 3. Vuông cân tại C
            {
                "points": [{"name": "A", "x": 0.0, "y": 4.0, "source": "free"},
                           {"name": "B", "x": 4.0, "y": 0.0, "source": "free"},
                           {"name": "C", "x": 0.0, "y": 0.0, "source": "free"}],
                "expected_type": "right_isosceles",
                "apex_node": "C"
            },
            # 4. Đều
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
                           {"name": "B", "x": 2.0, "y": 0.0, "source": "free"},
                           {"name": "C", "x": 1.0, "y": math.sqrt(3), "source": "free"}],
                "expected_type": "equilateral",
                "apex_node": None
            },
            # 5. Tam giác thường liên tục: không cạnh nào gần nhau trong 0.6%
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
                           {"name": "B", "x": 10.0, "y": 0.0, "source": "free"},
                           {"name": "C", "x": 3.0, "y": 6.0, "source": "free"}],
                "expected_type": "scalene",
                "apex_node": None
            },
            # 6. Ca 10/30/29/13 qua dung sai 0.6% (lệch 0.5% < 0.6% -> gần cân tại A)
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
                           {"name": "B", "x": 10.0, "y": 30.0, "source": "free"},
                           {"name": "C", "x": 29.0, "y": 13.0, "source": "free"}],
                "expected_type": "isosceles",
                "apex_node": "A"
            },
            # 7. Ca kim thật tạo thành tam giác (Needle triangle): y=0.02, l_max=1000, rel_cross=2e-5 >= 1e-5 -> tam giác cân tại A
            {
                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
                           {"name": "B", "x": 1000.0, "y": 0.0, "source": "free"},
                           {"name": "C", "x": 1000.0, "y": 0.02, "source": "free"}],
                "expected_type": "isosceles",
                "apex_node": "A"
            }
        ]

        for case in cases_continuous:
            pts = case["points"]
            expected_type = case["expected_type"]
            expected_apex = case["apex_node"]

            for perm in itertools.permutations(pts):
                p1, p2, p3 = perm
                res = classify_triangle(p1, p2, p3)
                self.assertTrue(res["is_triangle"], f"Hoán vị {p1['name']},{p2['name']},{p3['name']} phải là tam giác")
                self.assertFalse(res["is_discrete"], "Các điểm source='free' bắt buộc phải chạy qua nhánh liên tục (is_discrete=False)")
                self.assertEqual(res["type"], expected_type, 
                                 f"Nhánh liên tục hoán vị {p1['name']},{p2['name']},{p3['name']} type={expected_type}, thực tế={res['type']}")
                if expected_apex is not None:
                    self.assertEqual(res["vertex"], expected_apex,
                                     f"Đỉnh đặc biệt nhánh liên tục phải là {expected_apex}")
                else:
                    self.assertIsNone(res["vertex"])

        # --- PHẦN 3: CA KIM THẬT THẲNG HÀNG (rel_cross < 1e-5 theo công thức chuẩn hóa l_max^2) ---
        # A(0,0), B(1000,0), C(1000, 0.004) -> l_max=1000, cross=4.0, rel_cross = 4.0 / 1000^2 = 4e-6 < 1e-5
        pts_collinear_needle = [
            {"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
            {"name": "B", "x": 1000.0, "y": 0.0, "source": "free"},
            {"name": "C", "x": 1000.0, "y": 0.004, "source": "free"}
        ]
        for perm in itertools.permutations(pts_collinear_needle):
            p1, p2, p3 = perm
            res = classify_triangle(p1, p2, p3)
            self.assertFalse(res["is_triangle"], f"Ca kim y=0.004 với hoán vị {p1['name']},{p2['name']},{p3['name']} phải bị nhận diện là thẳng hàng (rel_cross < 1e-5)")
            self.assertEqual(res["type"], "collinear")
            self.assertIn("thẳng hàng", res["message"].lower())

    def test_32_drag_derived_point_then_drag_parent(self):
        """Kiểm tra Canvas GUI: Kéo trung điểm có snap, sau đó kéo cha tự do thì tọa độ trung điểm tự cập nhật và cờ cũ bị xóa bỏ"""
        from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
        app = None
        errors = []
        try:
            app = GeoSolverApp(with_splash=False)
            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
            app.update()

            # 1. Tạo 2 điểm cha typed ban đầu
            pA = {"id": "PA", "name": "A", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            pB = {"id": "PB", "name": "B", "x": 4.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
            app.points = [pA, pB]
            app.redraw()
            app.current_tool = "midpoint"
            app._ask_point_name_dialog = lambda default_name: "M"

            sxA, syA = app.to_screen(pA["x"], pA["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sxA), y=int(syA))
            app.update()

            sxB, syB = app.to_screen(pB["x"], pB["y"])
            app.canvas.event_generate("<ButtonPress-1>", x=int(sxB), y=int(syB))
            app.update()

            self.assertEqual(len(app.points), 3)
            pM = app.points[2]
            self.assertEqual(pM["source"], "midpoint")
            self.assertEqual(pM["x"], 2.0)
            self.assertEqual(pM["y"], 0.0)

            # 2. Người dùng kéo trung điểm M khi snap_to_grid bật
            app.snap_to_grid = True
            app.grid_step = 0.5
            app.selected_points = [pM]
            app.drag_start_world = (pM["x"], pM["y"])
            sxM, syM = app.to_screen(2.5, 0.5)
            app.canvas.event_generate("<B1-Motion>", x=int(sxM), y=int(syM))
            app.update()

            # 3. Sau đó người dùng kéo điểm cha pA tự do (snap_to_grid tắt)
            app.snap_to_grid = False
            app.selected_points = [pA]
            app.drag_start_world = (pA["x"], pA["y"])
            dxA, dyA = 1.234, 0.567
            sxDrag, syDrag = app.to_screen(pA["x"] + dxA, pA["y"] + dyA)
            app.canvas.event_generate("<B1-Motion>", x=int(sxDrag), y=int(syDrag))
            app.update()

            # Điểm cha pA bị taint
            self.assertEqual(pA["source"], "dragged")
            self.assertFalse(pA["exact"])

            # Điểm trung điểm pM phải được tự động recompute: tọa độ cập nhật theo (pA + pB)/2
            expected_mx = (pA["x"] + pB["x"]) / 2.0
            expected_my = (pA["y"] + pB["y"]) / 2.0
            self.assertAlmostEqual(pM["x"], expected_mx, places=5, msg="Tọa độ x của trung điểm phải cập nhật theo cha pA")
            self.assertAlmostEqual(pM["y"], expected_my, places=5, msg="Tọa độ y của trung điểm phải cập nhật theo cha pA")

            # Cờ lỗi thời của pM bị xóa bỏ và làm tươi lại: source trở về 'midpoint', không còn exact=True
            self.assertEqual(pM["source"], "midpoint")
            self.assertIsNone(pM.get("exact"), "Cờ exact cũ phải bị loại bỏ (pop) để kế thừa taint từ cha")

            # 4. Phân loại tam giác tạo bởi pM, pB và một điểm typed khác pC -> bắt buộc bị taint (exact=False, origin_exact=False)
            pC = {"id": "PC", "name": "C", "x": 2.0, "y": 4.0, "source": "typed", "exact": True}
            res = classify_triangle(pM, pB, pC)
            self.assertIs(res["origin_exact"], False, "Tam giác chứa trung điểm có cha bị kéo tự do bắt buộc có origin_exact=False")
            self.assertFalse(res["exact"])
            self.assertFalse(res["is_discrete"], "Điểm tainted bắt buộc đi vào nhánh dung sai liên tục (is_discrete=False)")

            self.assertEqual(errors, [], f"Không được có ngoại lệ trong Tkinter callback: {errors}")
        finally:
            if app is not None:
                app.destroy()

```

### 4.2. Toàn văn 11 Bài Test Taint Propagation Chuyên biệt (`tests/test_round9_taint_validation.py`)
```python
"""Test hồi quy Round 9: taint, nhánh dung sai cho điểm vẽ tay, validate đầu vào.

Đặt vào tests/ và chạy:
python -m unittest tests.test_round9_taint_validation -v
"""
import math
import unittest

from geosolver.geosolver_desktop import classify_triangle


def P(x, y, source=None, exact=None, **kw):
    d = {"x": x, "y": y}
    if source is not None:
        d["source"] = source
    if exact is not None:
        d["exact"] = exact
    d.update(kw)
    return d


class TestInputValidation(unittest.TestCase):
    def test_nan_inf_none_rejected_in_dict(self):
        for bad in (float("nan"), float("inf"), float("-inf"), None, "abc"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    classify_triangle(P(bad, 0), P(1, 0), P(0, 1))

    def test_nan_inf_none_rejected_in_tuple(self):
        for bad in (float("nan"), float("inf"), None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    classify_triangle((0, bad), (1, 0), (0, 1))


class TestFreehandTaint(unittest.TestCase):
    def test_free_integer_right_triangle_uses_tolerance_branch(self):
        r = classify_triangle(P(0, 0, "free"), P(3, 0, "free"), P(0, 4, "free"))
        self.assertEqual(r["type"], "right")
        self.assertFalse(r["is_discrete"])
        self.assertFalse(r["exact"])
        self.assertIs(r["origin_exact"], False)

    def test_free_near_isosceles_is_flagged_but_typed_is_not(self):
        # Hai cạnh góc vuông 1000 và 1004: lệch ~0.4% < 0.6%
        free = classify_triangle(P(0, 0, "free"), P(1000, 0, "free"), P(0, 1004, "free"))
        typed = classify_triangle(P(0, 0, "typed"), P(1000, 0, "typed"), P(0, 1004, "typed"))
        self.assertEqual(free["type"], "right_isosceles")
        self.assertIn("gần", free["description"])
        self.assertFalse(free["exact"])
        # Gõ tay thì so sánh chính xác: 1000 != 1004 nên chỉ là vuông thường
        self.assertEqual(typed["type"], "right")
        self.assertTrue(typed["exact"])

    def test_mixed_typed_and_free_is_false(self):
        r = classify_triangle(P(0, 0, "typed"), P(4, 0, "free"), P(0, 3, "typed"))
        self.assertIs(r["origin_exact"], False)
        self.assertFalse(r["exact"])

    def test_points_exact_true_cannot_override_free(self):
        r = classify_triangle(P(0, 0, "free"), P(4, 0, "typed"), P(0, 3, "typed"),
                              points_exact=True)
        self.assertIs(r["origin_exact"], False)
        self.assertFalse(r["exact"])

    def test_explicit_exact_false_beats_exact_source(self):
        r = classify_triangle(P(0, 0, "typed", exact=False), P(4, 0, "typed"), P(0, 3, "typed"))
        self.assertIs(r["origin_exact"], False)


class TestDerivedPointPropagation(unittest.TestCase):
    A = P(0, 0, "typed")
    B = P(4, 0, "typed")

    def test_midpoint_of_free_parents_is_tainted(self):
        c = P(0, 3, "midpoint", parents=[P(0, 2, "free"), P(0, 4, "typed")])
        r = classify_triangle(self.A, self.B, c)
        self.assertIs(r["origin_exact"], False)
        self.assertFalse(r["exact"])

    def test_midpoint_of_typed_parents_is_exact(self):
        c = P(0, 3, "midpoint", parents=[P(0, 2, "typed"), P(0, 4, "typed")])
        r = classify_triangle(self.A, self.B, c)
        self.assertIs(r["origin_exact"], True)
        self.assertTrue(r["exact"])

    def test_derived_without_parents_is_unknown(self):
        c = P(0, 3, "midpoint")
        r = classify_triangle(self.A, self.B, c)
        self.assertIsNone(r["origin_exact"])  # chuyển sang heuristic is_discrete


class TestMicroScaleStillOk(unittest.TestCase):
    def test_3_4_5_at_1e_minus_5(self):
        k = 1e-5
        r = classify_triangle((0, 0), (3 * k, 0), (0, 4 * k))
        self.assertTrue(r["is_triangle"])
        self.assertEqual(r["type"], "right")
        self.assertEqual(r["vertex"], "A")


if __name__ == "__main__":
    unittest.main()

```

---

## 5. DỮ LIỆU THỰC NGHIỆM CHẠY THỰC TẾ TRÊN MÁY TÍNH (LOGS XÁC THỰC)

### 5.1. Nhật ký chạy toàn bộ 43/43 Unittest tự động (`tests/test_run.log`)
*Toàn văn nhật ký thi hành lệnh `python -m unittest discover tests -v` (Mã thoát: 0):*

```text

test_01_true_positive_equilateral_triangle (test_geometry_invariants.TestGeometryInvariants.test_01_true_positive_equilateral_triangle)

Ca d\u01b0\u01a1ng t�nh: Tam gi�c \u0111\u1ec1u th\u1ef1c s\u1ef1 v\u1edbi t\u1ecda \u0111\u1ed9 v� t\u1ec9 (g\u1ecdi tr\u1ef1c ti\u1ebfp classify_triangle) ... ok

test_02_regression_original_bug_isosceles_not_equilateral (test_geometry_invariants.TestGeometryInvariants.test_02_regression_original_bug_isosceles_not_equilateral)

H\u1ed3i quy l\u1ed7i g\u1ed1c: A(0, 5), B(-3, 0), C(3, 0) ph\u1ea3i nh\u1eadn di\u1ec7n l� tam gi�c c�n t\u1ea1i A, kh�ng b�o nh\u1ea7m \u0111\u1ec1u. ... ok

test_03_scale_invariance_property (test_geometry_invariants.TestGeometryInvariants.test_03_scale_invariance_property)

Thu\u1ed9c t�nh b\u1ea5t bi\u1ebfn t\u1ef7 l\u1ec7 theo thang 10^-k (k=0..3) tr�n t\u1ecda \u0111\u1ed9 r\u1eddi r\u1ea1c ... ok

test_04_typed_decimals_rejection_claude_cases (test_geometry_invariants.TestGeometryInvariants.test_04_typed_decimals_rejection_claude_cases)

Ca s\u1ed1 th\u1eadp ph�n g� tay c\u1ee7a Claude (5, 8.7) v� (0.04, 3) kh�ng b\u1ecb nh\u1eadn nh\u1ea7m ... ok

test_05_negative_equilateral_pure_float_coordinates (test_geometry_invariants.TestGeometryInvariants.test_05_negative_equilateral_pure_float_coordinates)

Ca �m t�nh \u0111\u1ed9c l\u1eadp: Dung sai 0.6% tr�n t\u1ecda \u0111\u1ed9 th\u1ef1c t\u1ef1 do lo\u1ea1i tr\u1eeb tam gi�c l\u1ec7ch 1.8% ... ok

test_06_collinear_and_coincident_points (test_geometry_invariants.TestGeometryInvariants.test_06_collinear_and_coincident_points)

Ca bi�n: 3 \u0111i\u1ec3m th\u1eb3ng h�ng v� \u0111i\u1ec3m tr�ng nhau kh�ng t\u1ea1o th�nh tam gi�c ... ok

test_07_right_and_right_isosceles_triangles (test_geometry_invariants.TestGeometryInvariants.test_07_right_and_right_isosceles_triangles)

Ca tam gi�c vu�ng v� vu�ng c�n tr�n l\u01b0\u1edbi r\u1eddi r\u1ea1c ... ok

test_08_ellipse_edge_cases_and_rotational_invariance (test_geometry_invariants.TestGeometryInvariants.test_08_ellipse_edge_cases_and_rotational_invariance)

H�nh elip to�n di\u1ec7n: chu\u1ea9n, F1==F2, suy bi\u1ebfn b=0, ti�u \u0111i\u1ec3m nghi�ng 53.13� v� \u0111\u1ed5i F1/F2 ... ok

test_09_ramanujan_ii_exact_accuracy_table (test_geometry_invariants.TestGeometryInvariants.test_09_ramanujan_ii_exact_accuracy_table)

Chu vi Ramanujan II so v\u1edbi t�ch ph�n s\u1ed1 h\u1ecdc quy t\u1eafc trung \u0111i\u1ec3m 100.000 b\u01b0\u1edbc ... ok

test_10_wcag_21_aa_itemized_real_contrast (test_geometry_invariants.TestGeometryInvariants.test_10_wcag_21_aa_itemized_real_contrast)

\u0110o t\u01b0\u01a1ng ph\u1ea3n 20 c\u1eb7p m�u th\u1ef1c t\u1ebf tr�n THEMES_GEOSOLVER theo chu\u1ea9n W3C WCAG 2.1 AA ... ok

test_11_clean_print_mode_and_handbook_dialog (test_geometry_invariants.TestGeometryInvariants.test_11_clean_print_mode_and_handbook_dialog)

Ki\u1ec3m tra Clean Print Mode toggle m\u1eb7c \u0111\u1ecbnh t\u1eaft v� t\u1ec7p c\u1ea9m nang F1 ... ok

test_12_dpapi_keystore_and_downloader_sha256 (test_geometry_invariants.TestGeometryInvariants.test_12_dpapi_keystore_and_downloader_sha256)

Ki\u1ec3m tra b\u1ea3o m\u1eadt DPAPI KeyStore (ch\u1ed1ng Use-After-Free) v� hf_downloader SHA-256 ... ok

test_13_dpapi_fail_soft_on_corrupt_or_foreign_key (test_geometry_invariants.TestGeometryInvariants.test_13_dpapi_fail_soft_on_corrupt_or_foreign_key)

Ki\u1ec3m tra nguy�n t\u1eafc fail-soft c\u1ee7a GeminiKeyStore: kh�ng s\u1eadp app khi file h\u1ecfng ho\u1eb7c chuy\u1ec3n m�y ... ok

test_14_exact_right_triangle_float_coordinates_no_spurious_annotation (test_geometry_invariants.TestGeometryInvariants.test_14_exact_right_triangle_float_coordinates_no_spurious_annotation)

Tam gi�c vu�ng th\u1ef1c s\u1ef1 c� t\u1ecda \u0111\u1ed9 v� t\u1ec9 (0,0), (\u221a2,0), (0,\u221a3): kh�ng \u0111\u01b0\u1ee3c ch� th�ch '(g\u1ea7n vu�ng, g�c 0.0�)' ... ok

test_15_float_near_right_and_near_right_isosceles_annotation (test_geometry_invariants.TestGeometryInvariants.test_15_float_near_right_and_near_right_isosceles_annotation)

Ca s\u1ed1 th\u1ef1c t\u1ef1 do g\u1ea7n vu�ng v� g\u1ea7n vu�ng c�n: ki\u1ec3m tra ch� th�ch \u0111\u1ed9 l\u1ec7ch v� deviations dict ... ok

test_16_dpapi_stress_round_trip_stability (test_geometry_invariants.TestGeometryInvariants.test_16_dpapi_stress_round_trip_stability)

Ki\u1ec3m tra �p l\u1ef1c 100 l\u1ea7n m� h�a/gi\u1ea3i m� DPAPI v\u1edbi payload ng\u1eabu nhi�n 1KB \u0111\u1ec3 lo\u1ea1i tr\u1eeb r� r\u1ec9 v�ng nh\u1edb ctypes ... ok

test_17_freehand_point_origin_flag_rejection (test_geometry_invariants.TestGeometryInvariants.test_17_freehand_point_origin_flag_rejection)

Ki\u1ec3m tra c\u1edd ngu\u1ed3n g\u1ed1c exact/source: v\u1ebd chu\u1ed9t t\u1ef1 do d� to\u1ea1 \u0111\u1ed9 nguy�n v\u1eabn c� exact=False ... ok

test_18_format_radical_len_direct_unit_tests (test_geometry_invariants.TestGeometryInvariants.test_18_format_radical_len_direct_unit_tests)

Ki\u1ec3m tra tr\u1ef1c ti\u1ebfp format_radical_len v\u1edbi c�c m\u1eabu c\u0103n th\u1ee9c v� ph�n s\u1ed1 ph\u1ed5 bi\u1ebfn ... ok

test_19_ellipse_near_degenerate_a_approx_c (test_geometry_invariants.TestGeometryInvariants.test_19_ellipse_near_degenerate_a_approx_c)

Ki\u1ec3m tra elip g\u1ea7n suy bi\u1ebfn khi a ti\u1ec7m c\u1eadn c (b -> 0) kh�ng b\u1ecb l\u1ed7i chia 0 ho\u1eb7c c\u0103n s\u1ed1 �m ... ok

test_20_hf_downloader_error_paths_comprehensive (test_geometry_invariants.TestGeometryInvariants.test_20_hf_downloader_error_paths_comprehensive)

Ki\u1ec3m tra c�c k\u1ecbch b\u1ea3n l\u1ed7i c\u1ee7a hf_downloader: sai magic GGUF, l\u1ec7ch k�ch th\u01b0\u1edbc, thi\u1ebfu SHA-256 ... ok

test_21_mixed_point_origin_flag_behavior (test_geometry_invariants.TestGeometryInvariants.test_21_mixed_point_origin_flag_behavior)

Ki\u1ec3m tra logic tr\u1ed9n c\u1edd ngu\u1ed3n g\u1ed1c, th\u1ee9 t\u1ef1 \u01b0u ti�n taint v� x\u1eed l� xung \u0111\u1ed9t c\u1edd ... ok

test_22_missing_coordinate_validation (test_geometry_invariants.TestGeometryInvariants.test_22_missing_coordinate_validation)

Ki\u1ec3m tra x�c th\u1ef1c d\u1eef li\u1ec7u \u0111i\u1ec3m: thi\u1ebfu x ho\u1eb7c y ph\u1ea3i n�m ValueError, kh�ng \u0111\u01b0\u1ee3c ng\u1ea7m \u0111\u1ecbnh b\u1eb1ng 0 ... ok

test_23_micro_scale_invariance_scale_10_minus_5 (test_geometry_invariants.TestGeometryInvariants.test_23_micro_scale_invariance_scale_10_minus_5)

Ki\u1ec3m tra b\u1ea5t bi\u1ebfn t\u1ef7 l\u1ec7 vi m� \u1edf thang 10^-5: kh�ng tr�ng \u0111i\u1ec3m v� kh�ng nh\u1eadn nh\u1ea7m all_int ... ok

test_24_gui_canvas_point_source_and_invariants_integration (test_geometry_invariants.TestGeometryInvariants.test_24_gui_canvas_point_source_and_invariants_integration)

Ki\u1ec3m tra t�ch h\u1ee3p GUI Canvas: ph�t s\u1ef1 ki\u1ec7n click chu\u1ed9t th\u1eadt \u0111\u1ec3 ki\u1ec3m tra g�n c\u1edd source='free' v� 'grid_snap' ... ok

test_25_gui_canvas_drag_typed_and_midpoint_parents_integration (test_geometry_invariants.TestGeometryInvariants.test_25_gui_canvas_drag_typed_and_midpoint_parents_integration)

Ki\u1ec3m tra Canvas GUI: K�o \u0111i\u1ec3m typed khi snap t\u1eaft th�nh dragged, v� t\u1ea1o trung \u0111i\u1ec3m t\u1eeb 2 \u0111i\u1ec3m free l\u01b0u parents ... ok

test_26_nested_constructions_multi_level_taint (test_geometry_invariants.TestGeometryInvariants.test_26_nested_constructions_multi_level_taint)

Ki\u1ec3m tra d\u1ef1ng h�nh l\u1ed3ng nhau nhi\u1ec1u t\u1ea7ng (Nested derived points): Lan truy\u1ec1n taint qua nhi\u1ec1u c\u1ea5p cha-con ... ok

test_27_none_and_string_and_invalid_type_rejection (test_geometry_invariants.TestGeometryInvariants.test_27_none_and_string_and_invalid_type_rejection)

Ki\u1ec3m tra x\u1eed l� ngo\u1ea1i l\u1ec7: T\u1eeb ch\u1ed1i None, chu\u1ed7i '3.5', int v� ki\u1ec3u kh�ng h\u1ee3p l\u1ec7 n�m ValueError chu\u1ea9n ... ok

test_28_drag_with_snap_on_snaps_absolute_coordinates (test_geometry_invariants.TestGeometryInvariants.test_28_drag_with_snap_on_snaps_absolute_coordinates)

Ki\u1ec3m tra Canvas GUI: K�o \u0111i\u1ec3m t\u1ef1 do (l\u1ec7ch l\u01b0\u1edbi) khi snap b\u1eadt ph\u1ea3i b\u1eaft tuy\u1ec7t \u0111\u1ed1i v�o b\u1ed9i s\u1ed1 c\u1ee7a l\u01b0\u1edbi ... ok

test_29_depth_limit_and_memoization_point_flag (test_geometry_invariants.TestGeometryInvariants.test_29_depth_limit_and_memoization_point_flag)

Ki\u1ec3m tra _point_flag: Ph�t hi\u1ec7n chu tr�nh b\u1eb1ng _visiting, kh�ng taint gi\u1ea3 c�y s\u1ea1ch 10 t\u1ea7ng, b\u1ea3o v\u1ec7 \u0111\u1ec7 quy s�u >= 100, v� memoization O(1) ... ok

test_30_undo_redo_parent_taint_propagation (test_geometry_invariants.TestGeometryInvariants.test_30_undo_redo_parent_taint_propagation)

Ki\u1ec3m tra Canvas GUI: Undo/Redo kh�i ph\u1ee5c li�n k\u1ebft cha-con, thay th\u1ebf instance m\u1edbi, v� lan truy\u1ec1n t\u1ecda \u0111\u1ed9 + taint khi \u0111i\u1ec3m cha b\u1ecb k�o ... ok

test_31_permutation_invariance_all_six_orderings (test_geometry_invariants.TestGeometryInvariants.test_31_permutation_invariance_all_six_orderings)

Ki\u1ec3m tra b\u1ea5t bi\u1ebfn ho�n v\u1ecb tuy\u1ec7t \u0111\u1ed1i tr�n c\u1ea3 2 nh�nh (R\u1eddi r\u1ea1c & Li�n t\u1ee5c): Th\u1eed c\u1ea3 6 ho�n v\u1ecb c\u1ee7a 3 \u0111\u1ec9nh cho m\u1ecdi lo\u1ea1i tam gi�c ... ok

test_32_drag_derived_point_then_drag_parent (test_geometry_invariants.TestGeometryInvariants.test_32_drag_derived_point_then_drag_parent)

Ki\u1ec3m tra Canvas GUI: K�o trung \u0111i\u1ec3m c� snap, sau \u0111� k�o cha t\u1ef1 do th� t\u1ecda \u0111\u1ed9 trung \u0111i\u1ec3m t\u1ef1 c\u1eadp nh\u1eadt v� c\u1edd c\u0169 b\u1ecb x�a b\u1ecf ... ok

test_derived_without_parents_is_unknown (test_round9_taint_validation.TestDerivedPointPropagation.test_derived_without_parents_is_unknown) ... ok

test_midpoint_of_free_parents_is_tainted (test_round9_taint_validation.TestDerivedPointPropagation.test_midpoint_of_free_parents_is_tainted) ... ok

test_midpoint_of_typed_parents_is_exact (test_round9_taint_validation.TestDerivedPointPropagation.test_midpoint_of_typed_parents_is_exact) ... ok

test_explicit_exact_false_beats_exact_source (test_round9_taint_validation.TestFreehandTaint.test_explicit_exact_false_beats_exact_source) ... ok

test_free_integer_right_triangle_uses_tolerance_branch (test_round9_taint_validation.TestFreehandTaint.test_free_integer_right_triangle_uses_tolerance_branch) ... ok

test_free_near_isosceles_is_flagged_but_typed_is_not (test_round9_taint_validation.TestFreehandTaint.test_free_near_isosceles_is_flagged_but_typed_is_not) ... ok

test_mixed_typed_and_free_is_false (test_round9_taint_validation.TestFreehandTaint.test_mixed_typed_and_free_is_false) ... ok

test_points_exact_true_cannot_override_free (test_round9_taint_validation.TestFreehandTaint.test_points_exact_true_cannot_override_free) ... ok

test_nan_inf_none_rejected_in_dict (test_round9_taint_validation.TestInputValidation.test_nan_inf_none_rejected_in_dict) ... ok

test_nan_inf_none_rejected_in_tuple (test_round9_taint_validation.TestInputValidation.test_nan_inf_none_rejected_in_tuple) ... ok

test_3_4_5_at_1e_minus_5 (test_round9_taint_validation.TestMicroScaleStillOk.test_3_4_5_at_1e_minus_5) ... ok



----------------------------------------------------------------------

Ran 43 tests in 8.080s



OK


```

### 5.2. Nhật ký Smoke Test thực tế và tệp JSON trên bản đóng gói `GeoSolver.exe`
*Lệnh thực thi:*
`dist\GeoSolver\GeoSolver.exe --smoke-test --output=dist\GeoSolver\smoke_test_result.json`

*Nội dung tệp `dist\GeoSolver\smoke_test_result.json`:*
```json
{
  "timestamp": "2026-11-09T15:28:19.765421+00:00",
  "git_commit": "a428da857f18909274137f1c86d05a8f621f19b8",
  "git_dirty": false,
  "frozen": true,
  "python_version": "3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)]",
  "executable": "D:\\AI DATA\\STEM_APP\\dist\\GeoSolver\\GeoSolver.exe",
  "executable_sha256": "058B5F209AB985198A97D382670346C383302D3DB0502E5D53E7764095DAAC6A",
  "checks": {
    "geometry": true,
    "dpapi": true,
    "sympy": true,
    "tkinter_runtime": true,
    "critical_modules": true,
    "assets": true,
    "ssl_certifi": true
  },
  "status": "PASS",
  "exit_code": 0
}
```

*Nội dung tệp `dist\GeoSolver\smoke_run.log`:*
```text
[SMOKE TEST] Khởi chạy kiểm thử đóng gói GeoSolver (Smoke Test)...
[SMOKE TEST] 1. Phân loại hình học bất biến: ĐẠT
[SMOKE TEST] 2. Mã hóa & giải mã Windows DPAPI: ĐẠT
[SMOKE TEST] 3. Nạp động thư viện SymPy: ĐẠT
[SMOKE TEST] 4. Khởi tạo & giải phóng Tkinter GUI runtime: ĐẠT
[SMOKE TEST] 5. Nạp các module phụ thuộc quan trọng: ĐẠT
[SMOKE TEST] 6. Tài nguyên đóng gói trong frozen bundle: ĐẠT
[SMOKE TEST] 7. Nạp cấu hình bảo mật SSL/TLS & CA bundle certifi (cafile): ĐẠT
[SMOKE TEST] TẤT CẢ CÁC MỤC KIỂM THỬ KHÓI ĐỀU THÀNH CÔNG (MÃ THOÁT 0).
[SMOKE TEST] Đã ghi nhật ký kết quả kiểm thử vào: dist\GeoSolver\smoke_test_result.json

```

### 5.3. Kết quả đóng gói (`makeappx.exe`) và ký số (`signtool.exe`) gói `dist\GeoSolver_v3.1.msix`
*Toàn văn nhật ký thi hành lệnh PowerShell đóng gói và ký số:*
```text
Microsoft (R) MakeAppx Tool
Copyright (C) 2013 Microsoft.  All rights reserved.

The path (/p) parameter is: "\\?\D:\AI DATA\STEM_APP\dist\GeoSolver_v3.1.msix"
The content directory (/d) parameter is: "\\?\D:\AI DATA\STEM_APP\msix_layout"
Enumerating files from directory "\\?\D:\AI DATA\STEM_APP\msix_layout"
Packing 2725 file(s) in "\\?\D:\AI DATA\STEM_APP\msix_layout" to "\\?\D:\AI DATA\STEM_APP\dist\GeoSolver_v3.1.msix".
Using "\\?\D:\AI DATA\STEM_APP\msix_layout\AppxManifest.xml" as the manifest for the package.
Processing payload files and VFS virtual filesystem directory...
Package creation succeeded.

Microsoft (R) SignTool
Done Adding Additional Store
Successfully signed: dist\GeoSolver_v3.1.msix

Verifying: dist\GeoSolver_v3.1.msix
Signature Index: 0 (Primary Signature)
Signing Certificate Chain:
    Issued to: CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE
    Issued by: CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE
    Expires:   Tue Nov 02 22:54:43 2027
    SHA1 hash: 9D20C8ED8F274E35CAEB8AAA3F6BCA75CF09298F
```

### 5.4. Bằng chứng cài đặt và kiểm thử khói gói MSIX thực tế trong sandbox `C:\Program Files\WindowsApps\...`
Để đáp ứng yêu cầu cao nhất của Claude về việc **"chứng minh gói MSIX cài đặt và chạy thật sự trên Windows"**, đội ngũ phát triển đã thực hiện quy trình kiểm chứng thực địa trên Windows 11:
1. Gói MSIX cục bộ được đóng gói và ký số bằng chứng chỉ `CN=GeoSolverPublisher` (Thumbprint: `0BB5A4EEC8296ECBFB874962CDE1A19849E75286`) đã được tin cậy trong kho chứng chỉ `Cert:\LocalMachine\TrustedPeople`.
2. Cài đặt trực tiếp vào hệ thống bằng lệnh `Add-AppxPackage -Path dist\GeoSolver_local_test.msix`.
3. Truy vấn gói đã cài đặt bằng lệnh `Get-AppxPackage TLabtool.GeoSolverCAD`.
4. Chạy smoke test trực tiếp từ bên trong đường dẫn cài đặt sandbox `C:\Program Files\WindowsApps\...\VFS\GeoSolver.exe`.
5. Gỡ cài đặt sạch bằng `Remove-AppxPackage`.

*Nhật ký thi hành thực tế từ PowerShell (Mã thoát 0):*
```text
PS D:\AI DATA\STEM_APP> Add-AppxPackage -Path "dist\GeoSolver_local_test.msix"
PS D:\AI DATA\STEM_APP> $pkg = Get-AppxPackage TLabtool.GeoSolverCAD
PS D:\AI DATA\STEM_APP> $pkg | Select-Object Name, Version, Architecture, Publisher, InstallLocation | Format-List

Name            : TLabtool.GeoSolverCAD
Version         : 3.1.0.0
Architecture    : X64
Publisher       : CN=GeoSolverPublisher
InstallLocation : C:\Program Files\WindowsApps\TLabtool.GeoSolverCAD_3.1.0.0_x64__xajtjyx7m791y

PS D:\AI DATA\STEM_APP> $appPath = Join-Path $pkg.InstallLocation "VFS\GeoSolver.exe"
PS D:\AI DATA\STEM_APP> $outJson = "$env:TEMP\msix_smoke_test.json"
PS D:\AI DATA\STEM_APP> & $appPath --smoke-test "--output=$outJson"
PS D:\AI DATA\STEM_APP> Write-Host "Smoke test from WindowsApps exit code: $LASTEXITCODE"
Smoke test from WindowsApps exit code: 0

PS D:\AI DATA\STEM_APP> Get-Content $outJson
{
  "timestamp": "2026-11-09T15:33:04.607425+00:00",
  "git_commit": "a428da857f18909274137f1c86d05a8f621f19b8",
  "git_dirty": false,
  "frozen": true,
  "python_version": "3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)]",
  "executable": "C:\\Program Files\\WindowsApps\\TLabtool.GeoSolverCAD_3.1.0.0_x64__xajtjyx7m791y\\VFS\\GeoSolver.exe",
  "executable_sha256": "058B5F209AB985198A97D382670346C383302D3DB0502E5D53E7764095DAAC6A",
  "checks": {
    "geometry": true,
    "dpapi": true,
    "sympy": true,
    "tkinter_runtime": true,
    "critical_modules": true,
    "assets": true,
    "ssl_certifi": true
  },
  "status": "PASS",
  "exit_code": 0
}

PS D:\AI DATA\STEM_APP> Remove-AppxPackage -Package $pkg.PackageFullName
Uninstalled package successfully.
```

### 5.5. Kết quả kiểm tra độ dài đường dẫn (MAX_PATH Check)
*Lệnh thực thi:*
Quét toàn bộ 2.725 tệp trong cấu trúc `msix_layout\VFS`.
*Kết quả:*
- Đường dẫn dài nhất: `msix_layout\VFS\_internal\lxml\isoschematron\resources\xsl\iso-schematron-xslt1\iso_schematron_skeleton_for_xslt1.xsl`
- Độ dài tối đa: **117 ký tự** (Nằm hoàn toàn trong giới hạn an toàn 260 ký tự của Windows `MAX_PATH`).

### 5.6. Kết quả kiểm tra tiến trình con (`ai_local_manager.py` không chạy subprocess)
*Lệnh thực thi:*
`Select-String -Path "stem_shared_core\*.py", "geosolver\*.py" -Pattern "sys.executable", "subprocess.Popen" -Exclude "_build_info.py"`
*Kết quả:*
Trong toàn bộ module runtime `stem_shared_core/ai_local_manager.py`, hoàn toàn **KHÔNG CÓ** bất kỳ lệnh gọi `sys.executable` hay `subprocess.Popen` nào. `sys.executable` chỉ xuất hiện trong kịch bản đóng gói `build_microsoft_dist.py` và khối lệnh báo cáo đường dẫn thực thi của Smoke Test.

---

## 6. GIT DIFF GIỮA RC3 VÀ RC4 & BẢNG MÃ BĂM SHA-256 TOÀN VẸN DỮ LIỆU

### 6.1. Bảng thống kê `git diff --stat 5f1efd3..v3.1.0-rc4`
```text
 .gitignore                           |   2 +
 geosolver/geosolver_desktop.py       |  65 ++++----
 stem_shared_core/ai_local_manager.py |  29 ++--
 tests/test_geometry_invariants.py    | 309 +++++++++++++++++++++++++++++------
 4 files changed, 307 insertions(+), 98 deletions(-)
```

### 6.2. Git diff chi tiết các thay đổi mã nguồn cốt lõi (`geosolver_desktop.py` & `ai_local_manager.py`)
```patch
diff --git a/.gitignore b/.gitignore
index 26933f8..c6df2f1 100644
--- a/.gitignore
+++ b/.gitignore
@@ -51,6 +51,8 @@ msix_layout_3d/
 
 # PyInstaller temporary specs and manifests
 *.manifest
+_build_info.py
+**/_build_info.py
 
 # Logs & test runtime outputs
 *.log
diff --git a/geosolver/geosolver_desktop.py b/geosolver/geosolver_desktop.py
index d38f5de..9e0c472 100644
--- a/geosolver/geosolver_desktop.py
+++ b/geosolver/geosolver_desktop.py
@@ -329,14 +329,14 @@ def _finite(v, label, p):
     return f
 
 
-def _point_flag(p, _depth=0, memo=None):
-    """True = ch├¡nh x├íc, False = vß║╜ tay (taint) hoß║╖c qu├í ─æß╗Ö s├óu kiß╗âm tra, None = kh├┤ng r├╡ nguß╗ôn.
+def _point_flag(p, _visiting=None, memo=None, _depth=0):
+    """True = ch├¡nh x├íc, False = vß║╜ tay (taint) hoß║╖c chu tr├¼nh, None = kh├┤ng r├╡ nguß╗ôn.
 
     ─Éiß╗âm dß╗▒ng h├¼nh (midpoint/intersection/formula) kß║┐ thß╗½a cß╗¥ tß╗½ ─æiß╗âm cha
     qua kh├│a "parents". Kh├┤ng c├│ "parents" th├¼ coi l├á kh├┤ng r├╡ (None),
     trß╗½ khi c├│ exact=True t╞░ß╗¥ng minh.
-    Nß║┐u v╞░ß╗út qu├í giß╗¢i hß║ín ─æß╗Ö s├óu (_depth >= 8), h├ám mß║╖c ─æß╗ïnh trß║ú False (kh├┤ng tin cß║¡y)
-    ─æß╗â ng─ân chß║╖n viß╗çc l├ám mß║Ñt dß║Ñu vß║┐t taint tr├¬n ─æß╗ô thß╗ï phß╗Ñ thuß╗Öc s├óu.
+    Sß╗¡ dß╗Ñng tß║¡p _visiting ─æß╗â ph├ít hiß╗çn chu tr├¼nh (cycle detection) v├á memo ─æß╗â tß╗æi ╞░u O(1).
+    Nß║┐u v╞░ß╗út qu├í giß╗¢i hß║ín ─æß╗Ö s├óu an to├án (_depth >= 100), h├ám trß║ú False ─æß╗â chß╗æng tr├án ng─ân xß║┐p.
     """
     if not isinstance(p, dict):
         return None
@@ -346,23 +346,33 @@ def _point_flag(p, _depth=0, memo=None):
     if obj_id in memo:
         return memo[obj_id]
 
+    if _visiting is None:
+        _visiting = set()
+    if obj_id in _visiting:
+        # Chu tr├¼nh tham chiß║┐u v├▓ng trong ─æß╗ô thß╗ï phß║ú hß╗ç
+        return False
+    if _depth >= 100:
+        # Bß║úo vß╗ç tr├án ng─ân xß║┐p ─æß╗ç quy
+        return False
+
     if p.get("source") in _FREE_SOURCES or p.get("exact") is False:
         memo[obj_id] = False
         return False
 
     if p.get("source") in _DERIVED_SOURCES and p.get("parents"):
-        if _depth >= 8:
-            # Cß║»t ngß║»n ─æß╗ç quy an to├án: KH├öNG l╞░u False v├áo memo ─æß╗â tr├ính l├ám bß║⌐n c├íc ─æ╞░ß╗¥ng ─æi ngß║»n h╞ín
-            return False
-        flags = [_point_flag(q, _depth + 1, memo) for q in p["parents"]]
-        if any(f is False for f in flags):
-            res = False
-        elif all(f is True for f in flags):
-            res = True
-        else:
-            res = None
-        memo[obj_id] = res
-        return res
+        _visiting.add(obj_id)
+        try:
+            flags = [_point_flag(q, _visiting, memo, _depth + 1) for q in p["parents"]]
+            if any(f is False for f in flags):
+                res = False
+            elif all(f is True for f in flags):
+                res = True
+            else:
+                res = None
+            memo[obj_id] = res
+            return res
+        finally:
+            _visiting.discard(obj_id)
 
     if p.get("exact") is True or p.get("source") in _EXACT_SOURCES:
         memo[obj_id] = True
@@ -8533,34 +8543,25 @@ class GeoSolverApp(tk.Tk):
 
 
                 if c_type == "midpoint":
-
                     p1 = self._resolve_point(c.get("p1"))
-
                     p2 = self._resolve_point(c.get("p2"))
-
                     if p1 and p2:
-
                         p["x"] = (p1["x"] + p2["x"]) / 2.0
-
                         p["y"] = (p1["y"] + p2["y"]) / 2.0
-
                         p["parents"] = [p1, p2]
-
-
+                        p["source"] = "midpoint"
+                        p.pop("exact", None)
 
                 elif c_type in ("on_segment", "on_line"):
-
                     p1 = self._resolve_point(c.get("p1"))
-
                     p2 = self._resolve_point(c.get("p2"))
-
                     if p1 and p2:
-
                         t = c.get("t", 0.5)
-
                         p["x"] = p1["x"] + t * (p2["x"] - p1["x"])
-
                         p["y"] = p1["y"] + t * (p2["y"] - p1["y"])
+                        p["parents"] = [p1, p2]
+                        p["source"] = "formula"
+                        p.pop("exact", None)
 
 
 
@@ -8621,10 +8622,10 @@ class GeoSolverApp(tk.Tk):
                         pt_int = self._intersect_lines(p1, p2, p3, p4)
 
                         if pt_int:
-
                             p["x"], p["y"] = pt_int[0], pt_int[1]
-
                             p["parents"] = [p1, p2, p3, p4]
+                            p["source"] = "intersection"
+                            p.pop("exact", None)
 
 
 
diff --git a/stem_shared_core/ai_local_manager.py b/stem_shared_core/ai_local_manager.py
index e55932b..fa61799 100644
--- a/stem_shared_core/ai_local_manager.py
+++ b/stem_shared_core/ai_local_manager.py
@@ -131,20 +131,23 @@ class _DATA_BLOB(ctypes.Structure):
 
 if os.name == "nt":
     try:
-        ctypes.windll.crypt32.CryptProtectData.argtypes = [
+        _crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
+        _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
+
+        _crypt32.CryptProtectData.argtypes = [
             ctypes.POINTER(_DATA_BLOB), ctypes.c_wchar_p, ctypes.POINTER(_DATA_BLOB),
             ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_DATA_BLOB)
         ]
-        ctypes.windll.crypt32.CryptProtectData.restype = ctypes.c_int
+        _crypt32.CryptProtectData.restype = ctypes.c_int
 
-        ctypes.windll.crypt32.CryptUnprotectData.argtypes = [
+        _crypt32.CryptUnprotectData.argtypes = [
             ctypes.POINTER(_DATA_BLOB), ctypes.POINTER(ctypes.c_wchar_p), ctypes.POINTER(_DATA_BLOB),
             ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_DATA_BLOB)
         ]
-        ctypes.windll.crypt32.CryptUnprotectData.restype = ctypes.c_int
+        _crypt32.CryptUnprotectData.restype = ctypes.c_int
 
-        ctypes.windll.kernel32.LocalFree.argtypes = [ctypes.c_void_p]
-        ctypes.windll.kernel32.LocalFree.restype = ctypes.c_void_p
+        _kernel32.LocalFree.argtypes = [ctypes.c_void_p]
+        _kernel32.LocalFree.restype = ctypes.c_void_p
     except Exception:
         pass
 
@@ -155,13 +158,14 @@ def _dpapi_encrypt(data: bytes) -> bytes:
     buf = ctypes.create_string_buffer(data)
     blob_in = _DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))
     blob_out = _DATA_BLOB()
-    if ctypes.windll.crypt32.CryptProtectData(
+    if _crypt32.CryptProtectData(
         ctypes.byref(blob_in), "STEM_AI_KEY", None, None, None, 0, ctypes.byref(blob_out)
     ):
         out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
-        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
+        _kernel32.LocalFree(blob_out.pbData)
         return out
-    raise ctypes.WinError()
+    err = ctypes.get_last_error()
+    raise ctypes.WinError(err)
 
 def _dpapi_decrypt(data: bytes) -> bytes:
     if os.name != "nt":
@@ -170,13 +174,14 @@ def _dpapi_decrypt(data: bytes) -> bytes:
     buf = ctypes.create_string_buffer(data)
     blob_in = _DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))
     blob_out = _DATA_BLOB()
-    if ctypes.windll.crypt32.CryptUnprotectData(
+    if _crypt32.CryptUnprotectData(
         ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)
     ):
         out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
-        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
+        _kernel32.LocalFree(blob_out.pbData)
         return out
-    raise ctypes.WinError()
+    err = ctypes.get_last_error()
+    raise ctypes.WinError(err)
 
 _LOGGER_INITIALIZED = False
 
diff --git a/tests/test_geometry_invariants.py b/tests/test_geometry_invariants.py
index 85dda3e..7640503 100644
--- a/tests/test_geometry_invariants.py
+++ b/tests/test_geometry_invariants.py
@@ -425,8 +425,10 @@ class TestGeometryInvariants(unittest.TestCase):
         from geosolver.geosolver_desktop import GeoSolverApp
         import tkinter as tk
         app = None
+        errors = []
         try:
             app = GeoSolverApp(with_splash=False)
+            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
             app.current_tool = "point"
             app.update()  # Map canvas l├¬n Tkinter display pipeline
 
@@ -473,6 +475,7 @@ class TestGeometryInvariants(unittest.TestCase):
             app.update()
             self.assertEqual(p_snap["source"], "dragged", "─Éiß╗âm bß╗ï k├⌐o tß╗▒ do bß║»t buß╗Öc ─æß╗òi source='dragged'")
             self.assertFalse(p_snap["exact"], "─Éiß╗âm bß╗ï k├⌐o tß╗▒ do bß║»t buß╗Öc c├│ exact=False")
+            self.assertEqual(errors, [], f"Kh├┤ng ─æ╞░ß╗úc c├│ ngoß║íi lß╗ç trong Tkinter callback: {errors}")
         finally:
             if app is not None:
                 app.destroy()
@@ -481,8 +484,10 @@ class TestGeometryInvariants(unittest.TestCase):
         """Kiß╗âm tra Canvas GUI: K├⌐o ─æiß╗âm typed khi snap tß║»t th├ánh dragged, v├á tß║ío trung ─æiß╗âm tß╗½ 2 ─æiß╗âm free l╞░u parents"""
         from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
         app = None
+        errors = []
         try:
             app = GeoSolverApp(with_splash=False)
+            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
             app.update()
 
             # 1. K├⌐o ─æiß╗âm typed khi snap tß║»t -> source th├ánh 'dragged', exact=False
@@ -501,6 +506,7 @@ class TestGeometryInvariants(unittest.TestCase):
             p_free1 = {"id": "F1", "name": "F1", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False}
             p_free2 = {"id": "F2", "name": "F2", "x": 4.0, "y": 0.0, "color": "#000", "fixed": False, "source": "free", "exact": False}
             app.points = [p_free1, p_free2]
+            app.redraw()
             app.current_tool = "midpoint"
             app._ask_point_name_dialog = lambda default_name: "Mid_Free"
 
@@ -524,6 +530,7 @@ class TestGeometryInvariants(unittest.TestCase):
             self.assertFalse(res["exact"], "Tam gi├íc c├│ ─æß╗ënh l├á trung ─æiß╗âm kß║┐ thß╗½a taint tß╗½ cha free bß║»t buß╗Öc exact=False")
             self.assertFalse(res["is_discrete"], "─Éiß╗âm tainted bß║»t buß╗Öc ─æi v├áo nh├ính li├¬n tß╗Ñc (is_discrete=False)")
             self.assertIs(res["origin_exact"], False)
+            self.assertEqual(errors, [], f"Kh├┤ng ─æ╞░ß╗úc c├│ ngoß║íi lß╗ç trong Tkinter callback: {errors}")
         finally:
             if app is not None:
                 app.destroy()
@@ -591,8 +598,10 @@ class TestGeometryInvariants(unittest.TestCase):
         """Kiß╗âm tra Canvas GUI: K├⌐o ─æiß╗âm tß╗▒ do (lß╗çch l╞░ß╗¢i) khi snap bß║¡t phß║úi bß║»t tuyß╗çt ─æß╗æi v├áo bß╗Öi sß╗æ cß╗ºa l╞░ß╗¢i"""
         from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
         app = None
+        errors = []
         try:
             app = GeoSolverApp(with_splash=False)
+            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
             app.update()
 
             # ─Éiß╗âm tß╗▒ do vß╗æn c├│ tß╗ìa ─æß╗Ö lß╗çch l╞░ß╗¢i (3.025, 4.025)
@@ -618,40 +627,39 @@ class TestGeometryInvariants(unittest.TestCase):
             self.assertEqual(p_free["y"] % 0.5, 0.0, f"y={p_free['y']} phß║úi l├á bß╗Öi sß╗æ cß╗ºa grid_step=0.5")
             self.assertEqual(p_free["source"], "grid_snap", "Khi snap bß║¡t, k├⌐o ─æiß╗âm phß║úi g├ín source='grid_snap'")
             self.assertTrue(p_free["exact"], "Khi snap bß║¡t, k├⌐o ─æiß╗âm phß║úi g├ín exact=True")
+            self.assertEqual(errors, [], f"Kh├┤ng ─æ╞░ß╗úc c├│ ngoß║íi lß╗ç trong Tkinter callback: {errors}")
         finally:
             if app is not None:
                 app.destroy()
 
     def test_29_depth_limit_and_memoization_point_flag(self):
-        """Kiß╗âm tra _point_flag: Giß╗¢i hß║ín ─æß╗ç quy (_depth >= 8) trß║ú False (kh├┤ng tin cß║¡y) v├á memoization xß╗¡ l├╜ ─æß╗ô thß╗ï DAG nhanh"""
+        """Kiß╗âm tra _point_flag: Ph├ít hiß╗çn chu tr├¼nh bß║▒ng _visiting, kh├┤ng taint giß║ú c├óy sß║ích 10 tß║ºng, bß║úo vß╗ç ─æß╗ç quy s├óu >= 100, v├á memoization O(1)"""
         import time
         from geosolver.geosolver_desktop import _point_flag
 
-        # 1. Kiß╗âm tra chuß╗ùi phß╗Ñ thuß╗Öc s├óu >= 8 trß║ú vß╗ü False
-        cur = {"id": "P0", "source": "typed", "exact": True}
-        for i in range(1, 10):
-            cur = {"id": f"P{i}", "source": "midpoint", "parents": [cur, cur]}
-
-        # cur c├│ ─æß╗Ö s├óu 9 tß║ºng, v╞░ß╗út qu├í ng╞░ß╗íng 8 => bß║»t buß╗Öc trß║ú vß╗ü False (coi nh╞░ taint)
-        flag = _point_flag(cur)
-        self.assertIs(flag, False, "C├óy phß╗Ñ thuß╗Öc v╞░ß╗út qu├í ─æß╗Ö s├óu 8 phß║úi trß║ú vß╗ü False ─æß╗â chß╗æng mß║Ñt dß║Ñu vß║┐t")
-
-        # 2. Kiß╗âm tra chuß╗ùi ngß║»n < 8 to├án bß╗Ö l├á typed => trß║ú vß╗ü True
-        cur_shallow = {"id": "S0", "source": "typed", "exact": True}
-        for i in range(1, 5):
-            cur_shallow = {"id": f"S{i}", "source": "midpoint", "parents": [cur_shallow, cur_shallow]}
-        self.assertIs(_point_flag(cur_shallow), True, "C├óy phß╗Ñ thuß╗Öc sß║ích ─æß╗Ö s├óu < 8 phß║úi giß╗» True")
-
-        # 3. Kiß╗âm tra bß║úo vß╗ç chu tr├¼nh (cycle / self-reference)
+        # 1. C├óy phß╗Ñ thuß╗Öc sß║ích 10 tß║ºng (depth 10) to├án bß╗Ö l├á typed -> phß║úi giß╗» True (kh├┤ng bß╗ï taint giß║ú)
+        cur_clean = {"id": "P0", "source": "typed", "exact": True}
+        for i in range(1, 11):
+            cur_clean = {"id": f"P{i}", "source": "midpoint", "parents": [cur_clean, cur_clean]}
+        flag_clean = _point_flag(cur_clean)
+        self.assertIs(flag_clean, True, "C├óy phß╗Ñ thuß╗Öc sß║ích 10 tß║ºng to├án bß╗Ö typed bß║»t buß╗Öc trß║ú vß╗ü True")
+
+        # 2. Kiß╗âm tra chuß╗ùi phß╗Ñ thuß╗Öc v╞░ß╗út qu├í ng╞░ß╗íng an to├án (_depth >= 100) trß║ú vß╗ü False ─æß╗â chß╗æng tr├án stack
+        cur_deep = {"id": "D0", "source": "typed", "exact": True}
+        for i in range(1, 102):
+            cur_deep = {"id": f"D{i}", "source": "midpoint", "parents": [cur_deep, cur_deep]}
+        flag_deep = _point_flag(cur_deep)
+        self.assertIs(flag_deep, False, "C├óy phß╗Ñ thuß╗Öc v╞░ß╗út qu├í ng╞░ß╗íng s├óu an to├án (>=100) phß║úi trß║ú vß╗ü False ─æß╗â chß╗æng tr├án ng─ân xß║┐p")
+
+        # 3. Kiß╗âm tra bß║úo vß╗ç chu tr├¼nh (cycle / self-reference qua tß║¡p _visiting)
         p_cycle_a = {"id": "C_A", "source": "midpoint", "parents": []}
         p_cycle_b = {"id": "C_B", "source": "midpoint", "parents": [p_cycle_a]}
         p_cycle_a["parents"] = [p_cycle_b]
-        # Kh├┤ng ─æ╞░ß╗úc n├⌐m RecursionError
+        # Kh├┤ng ─æ╞░ß╗úc n├⌐m RecursionError, kß║┐t th├║c an to├án v├á trß║ú vß╗ü False
         flag_cycle = _point_flag(p_cycle_a)
-        self.assertIs(flag_cycle, False, "Chu tr├¼nh ─æß╗ç quy phß║úi kß║┐t th├║c an to├án v├á trß║ú vß╗ü False")
+        self.assertIs(flag_cycle, False, "Chu tr├¼nh ─æß╗ç quy phß║úi kß║┐t th├║c an to├án qua tß║¡p _visiting v├á trß║ú vß╗ü False")
 
         # 4. Kiß╗âm tra hiß╗çu n─âng memoization tr├¬n ─æß╗ô thß╗ï kim c╞░╞íng (DAG)
-        # Tß║ío ─æß╗ô thß╗ï kim c╞░╞íng nhiß╗üu nh├ính hß╗Öi tß╗Ñ
         base = {"id": "Root", "source": "typed", "exact": True}
         layer = [base]
         for l in range(6):
@@ -675,17 +683,20 @@ class TestGeometryInvariants(unittest.TestCase):
         self.assertLess(elapsed, 0.05, f"Memoization phß║úi ho├án th├ánh 100 lß║ºn duyß╗çt DAG trong < 0.05s, thß╗▒c tß║┐: {elapsed:.4f}s")
 
     def test_30_undo_redo_parent_taint_propagation(self):
-        """Kiß╗âm tra Canvas GUI: Undo/Redo kh├┤i phß╗Ñc li├¬n kß║┐t cha-con v├á lan truyß╗ün taint ch├¡nh x├íc khi ─æiß╗âm cha bß╗ï k├⌐o"""
+        """Kiß╗âm tra Canvas GUI: Undo/Redo kh├┤i phß╗Ñc li├¬n kß║┐t cha-con, thay thß║┐ instance mß╗¢i, v├á lan truyß╗ün tß╗ìa ─æß╗Ö + taint khi ─æiß╗âm cha bß╗ï k├⌐o"""
         from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
         app = None
+        errors = []
         try:
             app = GeoSolverApp(with_splash=False)
+            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
             app.update()
 
             # Tß║ío 2 ─æiß╗âm typed ban ─æß║ºu
             pA = {"id": "P_A", "name": "A", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
             pB = {"id": "P_B", "name": "B", "x": 4.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
             app.points = [pA, pB]
+            app.redraw()
             app.current_tool = "midpoint"
             app._ask_point_name_dialog = lambda default_name: "M_AB"
 
@@ -702,8 +713,10 @@ class TestGeometryInvariants(unittest.TestCase):
             self.assertEqual(pM["name"], "M_AB")
             self.assertEqual(pM["source"], "midpoint")
 
-            # L╞░u trß║íng th├íi v├áo undo stack
-            app._save_state()
+            # L╞░u instance gß╗æc tr╞░ß╗¢c undo/redo
+            pA_orig = app.points[0]
+            pB_orig = app.points[1]
+            pM_orig = app.points[2]
 
             # Kiß╗âm tra tam gi├íc vß╗¢i ─æiß╗âm C typed ban ─æß║ºu: cß║ú 3 ─æiß╗âm ─æß╗üu sß║ích
             pC = {"id": "P_C", "name": "C", "x": 2.0, "y": 4.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
@@ -711,25 +724,37 @@ class TestGeometryInvariants(unittest.TestCase):
             self.assertIs(res_before["origin_exact"], True, "Tr╞░ß╗¢c khi k├⌐o, tam gi├íc gß╗ôm ─æiß╗âm dß╗▒ng h├¼nh sß║ích phß║úi c├│ origin_exact=True")
             self.assertTrue(res_before["exact"])
 
-            # Thß╗▒c hiß╗çn Undo rß╗ôi Redo
+            # Thß╗▒c hiß╗çn Undo -> ─æiß╗âm M_AB bß╗ï x├│a khß╗Åi danh s├ích points (ho├án t├íc thao t├íc tß║ío trung ─æiß╗âm)
             app.undo()
             app.update()
+            self.assertEqual(len(app.points), 2, "Undo tß║ío trung ─æiß╗âm phß║úi ─æ╞░a danh s├ích ─æiß╗âm vß╗ü 2")
+
+            # Thß╗▒c hiß╗çn Redo -> ─æiß╗âm M_AB ─æ╞░ß╗úc phß╗Ñc hß╗ôi
             app.redo()
             app.update()
+            self.assertEqual(len(app.points), 3, "Redo phß║úi kh├┤i phß╗Ñc lß║íi ─æß╗º 3 ─æiß╗âm")
 
             # Sau Redo, lß║Ñy lß║íi tham chiß║┐u ─æiß╗âm tß╗½ app.points
             pA_restored = app.points[0]
+            pB_restored = app.points[1]
             pM_restored = app.points[2]
 
-            # Kiß╗âm tra parents ─æ├ú ─æ╞░ß╗úc re-bind sau Redo
+            # Kiß╗âm tra thay thß║┐ instance: ─æß╗æi t╞░ß╗úng restored phß║úi l├á instance mß╗¢i, kh├┤ng phß║úi ─æß╗æi t╞░ß╗úng c┼⌐
+            self.assertIsNot(pA_restored, pA_orig, "Undo/redo phß║úi thay thß║┐ instance pA bß║▒ng dict mß╗¢i kh├┤i phß╗Ñc")
+            self.assertIsNot(pB_restored, pB_orig, "Undo/redo phß║úi thay thß║┐ instance pB bß║▒ng dict mß╗¢i kh├┤i phß╗Ñc")
+            self.assertIsNot(pM_restored, pM_orig, "Undo/redo phß║úi thay thß║┐ instance pM bß║▒ng dict mß╗¢i kh├┤i phß╗Ñc")
+
+            # Kiß╗âm tra parents ─æ├ú ─æ╞░ß╗úc re-bind sau Redo tß╗¢i ─æ├║ng instance mß╗¢i
             self.assertIn("parents", pM_restored)
-            self.assertIs(pM_restored["parents"][0], pA_restored, "parents[0] phß║úi trß╗Å tß╗¢i ─æ├║ng ─æß╗æi t╞░ß╗úng pA sß╗æng tr├¬n Canvas sau redo")
+            self.assertIs(pM_restored["parents"][0], pA_restored, "parents[0] phß║úi trß╗Å tß╗¢i ─æ├║ng instance pA sß╗æng tr├¬n Canvas sau redo")
+            self.assertIs(pM_restored["parents"][1], pB_restored, "parents[1] phß║úi trß╗Å tß╗¢i ─æ├║ng instance pB sß╗æng tr├¬n Canvas sau redo")
 
-            # Giß╗¥ k├⌐o ─æiß╗âm cha pA_restored khi snap tß║»t -> l├ám bß║⌐n pA
+            # K├⌐o ─æiß╗âm cha pA_restored khi snap tß║»t -> kiß╗âm tra tß╗ìa ─æß╗Ö pM di chuyß╗ân theo v├á nhß║¡n taint
             app.snap_to_grid = False
             app.selected_points = [pA_restored]
             app.drag_start_world = (pA_restored["x"], pA_restored["y"])
-            sx_drag, sy_drag = app.to_screen(pA_restored["x"] + 1.234, pA_restored["y"] + 0.567)
+            dx_drag, dy_drag = 1.234, 0.567
+            sx_drag, sy_drag = app.to_screen(pA_restored["x"] + dx_drag, pA_restored["y"] + dy_drag)
             app.canvas.event_generate("<B1-Motion>", x=int(sx_drag), y=int(sy_drag))
             app.update()
 
@@ -737,71 +762,79 @@ class TestGeometryInvariants(unittest.TestCase):
             self.assertEqual(pA_restored["source"], "dragged")
             self.assertFalse(pA_restored["exact"])
 
-            # ─Éiß╗âm trung ─æiß╗âm pM_restored tß╗▒ ─æß╗Öng cß║¡p nhß║¡t lß║íi tß╗ìa ─æß╗Ö v├á nhß║¡n diß╗çn vß║┐t d╞í tß╗½ cha
-            res_after_drag = classify_triangle(pM_restored, pB, pC)
+            # ─Éiß╗âm trung ─æiß╗âm pM_restored phß║úi tß╗▒ ─æß╗Öng di chuyß╗ân tß╗ìa ─æß╗Ö theo c├┤ng thß╗⌐c trung ─æiß╗âm (pA + pB)/2
+            expected_mx = (pA_restored["x"] + pB_restored["x"]) / 2.0
+            expected_my = (pA_restored["y"] + pB_restored["y"]) / 2.0
+            self.assertAlmostEqual(pM_restored["x"], expected_mx, places=5, msg="Tß╗ìa ─æß╗Ö x cß╗ºa trung ─æiß╗âm phß║úi tß╗▒ ─æß╗Öng chß║íy theo cha pA")
+            self.assertAlmostEqual(pM_restored["y"], expected_my, places=5, msg="Tß╗ìa ─æß╗Ö y cß╗ºa trung ─æiß╗âm phß║úi tß╗▒ ─æß╗Öng chß║íy theo cha pA")
+
+            # ─Éiß╗âm trung ─æiß╗âm pM_restored nhß║¡n diß╗çn vß║┐t d╞í tß╗½ cha
+            res_after_drag = classify_triangle(pM_restored, pB_restored, pC)
             self.assertIs(res_after_drag["origin_exact"], False, "Sau khi ─æiß╗âm cha bß╗ï k├⌐o tß╗▒ do, ─æiß╗âm con dß╗▒ng h├¼nh phß║úi bß╗ï vß║Ñy bß║⌐n (origin_exact=False)")
             self.assertFalse(res_after_drag["exact"], "exact phß║úi l├á False khi c├│ ─æiß╗âm vß║Ñy bß║⌐n trong tam gi├íc")
+            self.assertEqual(errors, [], f"Kh├┤ng ─æ╞░ß╗úc c├│ ngoß║íi lß╗ç trong Tkinter callback: {errors}")
         finally:
             if app is not None:
                 app.destroy()
 
     def test_31_permutation_invariance_all_six_orderings(self):
-        """Kiß╗âm tra bß║Ñt biß║┐n ho├ín vß╗ï tuyß╗çt ─æß╗æi: Thß╗¡ cß║ú 6 ho├ín vß╗ï cß╗ºa 3 ─æß╗ënh cho mß╗ìi loß║íi tam gi├íc, type v├á t├¡nh chß║Ñt phß║úi ─æß╗ông nhß║Ñt 100%"""
+        """Kiß╗âm tra bß║Ñt biß║┐n ho├ín vß╗ï tuyß╗çt ─æß╗æi tr├¬n cß║ú 2 nh├ính (Rß╗¥i rß║íc & Li├¬n tß╗Ñc): Thß╗¡ cß║ú 6 ho├ín vß╗ï cß╗ºa 3 ─æß╗ënh cho mß╗ìi loß║íi tam gi├íc"""
         import itertools
         from geosolver.geosolver_desktop import classify_triangle
 
-        cases = [
+        # --- PHß║ªN 1: NH├üNH Rß╗£I Rß║áC (DISCRETE - Sß╗æ nguy├¬n & Thß║¡p ph├ón sß║ích) ---
+        cases_discrete = [
             # 1. Tam gi├íc vu├┤ng tß║íi B: A(0,0), B(4,0), C(4,3)
             {
-                "points": [({"name": "A", "x": 0.0, "y": 0.0}),
-                           ({"name": "B", "x": 4.0, "y": 0.0}),
-                           ({"name": "C", "x": 4.0, "y": 3.0})],
+                "points": [{"name": "A", "x": 0.0, "y": 0.0},
+                           {"name": "B", "x": 4.0, "y": 0.0},
+                           {"name": "C", "x": 4.0, "y": 3.0}],
                 "expected_type": "right",
                 "apex_node": "B"
             },
             # 2. Tam gi├íc c├ón tß║íi B: A(-3,0), B(0,5), C(3,0)
             {
-                "points": [({"name": "A", "x": -3.0, "y": 0.0}),
-                           ({"name": "B", "x": 0.0, "y": 5.0}),
-                           ({"name": "C", "x": 3.0, "y": 0.0})],
+                "points": [{"name": "A", "x": -3.0, "y": 0.0},
+                           {"name": "B", "x": 0.0, "y": 5.0},
+                           {"name": "C", "x": 3.0, "y": 0.0}],
                 "expected_type": "isosceles",
                 "apex_node": "B"
             },
             # 3. Tam gi├íc vu├┤ng c├ón tß║íi C: A(0,4), B(4,0), C(0,0)
             {
-                "points": [({"name": "A", "x": 0.0, "y": 4.0}),
-                           ({"name": "B", "x": 4.0, "y": 0.0}),
-                           ({"name": "C", "x": 0.0, "y": 0.0})],
+                "points": [{"name": "A", "x": 0.0, "y": 4.0},
+                           {"name": "B", "x": 4.0, "y": 0.0},
+                           {"name": "C", "x": 0.0, "y": 0.0}],
                 "expected_type": "right_isosceles",
                 "apex_node": "C"
             },
-            # 4. Tam gi├íc ─æß╗üu: A(0,0), B(2,0), C(1, ΓêÜ3)
+            # 4. Tam gi├íc ─æß╗üu: A(0,0), B(2,0), C(1, ΓêÜ3) -> y v├┤ tß╗ë n├¬n tß╗▒ chuyß╗ân li├¬n tß╗Ñc
             {
-                "points": [({"name": "A", "x": 0.0, "y": 0.0}),
-                           ({"name": "B", "x": 2.0, "y": 0.0}),
-                           ({"name": "C", "x": 1.0, "y": math.sqrt(3)})],
+                "points": [{"name": "A", "x": 0.0, "y": 0.0},
+                           {"name": "B", "x": 2.0, "y": 0.0},
+                           {"name": "C", "x": 1.0, "y": math.sqrt(3)}],
                 "expected_type": "equilateral",
                 "apex_node": None
             },
-            # 5. Tam gi├íc th╞░ß╗¥ng (Claude scale test): A(0,0), B(10,30), C(29,13)
+            # 5. Tam gi├íc th╞░ß╗¥ng (Claude scale test 1000 vs 1010): A(0,0), B(10,30), C(29,13)
             {
-                "points": [({"name": "A", "x": 0.0, "y": 0.0}),
-                           ({"name": "B", "x": 10.0, "y": 30.0}),
-                           ({"name": "C", "x": 29.0, "y": 13.0})],
+                "points": [{"name": "A", "x": 0.0, "y": 0.0},
+                           {"name": "B", "x": 10.0, "y": 30.0},
+                           {"name": "C", "x": 29.0, "y": 13.0}],
                 "expected_type": "scalene",
                 "apex_node": None
             },
-            # 6. Tam gi├íc thon d├ái (Needle triangle): kiß╗âm tra collinear kh├┤ng phß╗Ñ thuß╗Öc ─æß╗ënh g├│c nhß╗ìn
+            # 6. Tam gi├íc thon d├ái rß╗¥i rß║íc (Needle triangle): A(0,0), B(100,0), C(50,0.5)
             {
-                "points": [({"name": "A", "x": 0.0, "y": 0.0}),
-                           ({"name": "B", "x": 100.0, "y": 0.0}),
-                           ({"name": "C", "x": 50.0, "y": 0.5})],
+                "points": [{"name": "A", "x": 0.0, "y": 0.0},
+                           {"name": "B", "x": 100.0, "y": 0.0},
+                           {"name": "C", "x": 50.0, "y": 0.5}],
                 "expected_type": "isosceles",
                 "apex_node": "C"
             }
         ]
 
-        for case in cases:
+        for case in cases_discrete:
             pts = case["points"]
             expected_type = case["expected_type"]
             expected_apex = case["apex_node"]
@@ -819,5 +852,173 @@ class TestGeometryInvariants(unittest.TestCase):
                 else:
                     self.assertIsNone(res["vertex"])
 
+        # --- PHß║ªN 2: NH├üNH LI├èN Tß╗ñC (CONTINUOUS - ├ëp qua source='free') & CA KIM CHUß║¿N H├ôA L_MAX^2 ---
+        cases_continuous = [
+            # 1. Vu├┤ng tß║íi B qua dung sai g├│c
+            {
+                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
+                           {"name": "B", "x": 4.0, "y": 0.0, "source": "free"},
+                           {"name": "C", "x": 4.0, "y": 3.0, "source": "free"}],
+                "expected_type": "right",
+                "apex_node": "B"
+            },
+            # 2. C├ón tß║íi B qua dung sai cß║ính 0.6%
+            {
+                "points": [{"name": "A", "x": -3.0, "y": 0.0, "source": "free"},
+                           {"name": "B", "x": 0.0, "y": 5.0, "source": "free"},
+                           {"name": "C", "x": 3.0, "y": 0.0, "source": "free"}],
+                "expected_type": "isosceles",
+                "apex_node": "B"
+            },
+            # 3. Vu├┤ng c├ón tß║íi C
+            {
+                "points": [{"name": "A", "x": 0.0, "y": 4.0, "source": "free"},
+                           {"name": "B", "x": 4.0, "y": 0.0, "source": "free"},
+                           {"name": "C", "x": 0.0, "y": 0.0, "source": "free"}],
+                "expected_type": "right_isosceles",
+                "apex_node": "C"
+            },
+            # 4. ─Éß╗üu
+            {
+                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
+                           {"name": "B", "x": 2.0, "y": 0.0, "source": "free"},
+                           {"name": "C", "x": 1.0, "y": math.sqrt(3), "source": "free"}],
+                "expected_type": "equilateral",
+                "apex_node": None
+            },
+            # 5. Tam gi├íc th╞░ß╗¥ng li├¬n tß╗Ñc: kh├┤ng cß║ính n├áo gß║ºn nhau trong 0.6%
+            {
+                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
+                           {"name": "B", "x": 10.0, "y": 0.0, "source": "free"},
+                           {"name": "C", "x": 3.0, "y": 6.0, "source": "free"}],
+                "expected_type": "scalene",
+                "apex_node": None
+            },
+            # 6. Ca 10/30/29/13 qua dung sai 0.6% (lß╗çch 0.5% < 0.6% -> gß║ºn c├ón tß║íi A)
+            {
+                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
+                           {"name": "B", "x": 10.0, "y": 30.0, "source": "free"},
+                           {"name": "C", "x": 29.0, "y": 13.0, "source": "free"}],
+                "expected_type": "isosceles",
+                "apex_node": "A"
+            },
+            # 7. Ca kim thß║¡t tß║ío th├ánh tam gi├íc (Needle triangle): y=0.02, l_max=1000, rel_cross=2e-5 >= 1e-5 -> tam gi├íc c├ón tß║íi A
+            {
+                "points": [{"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
+                           {"name": "B", "x": 1000.0, "y": 0.0, "source": "free"},
+                           {"name": "C", "x": 1000.0, "y": 0.02, "source": "free"}],
+                "expected_type": "isosceles",
+                "apex_node": "A"
+            }
+        ]
+
+        for case in cases_continuous:
+            pts = case["points"]
+            expected_type = case["expected_type"]
+            expected_apex = case["apex_node"]
+
+            for perm in itertools.permutations(pts):
+                p1, p2, p3 = perm
+                res = classify_triangle(p1, p2, p3)
+                self.assertTrue(res["is_triangle"], f"Ho├ín vß╗ï {p1['name']},{p2['name']},{p3['name']} phß║úi l├á tam gi├íc")
+                self.assertFalse(res["is_discrete"], "C├íc ─æiß╗âm source='free' bß║»t buß╗Öc phß║úi chß║íy qua nh├ính li├¬n tß╗Ñc (is_discrete=False)")
+                self.assertEqual(res["type"], expected_type, 
+                                 f"Nh├ính li├¬n tß╗Ñc ho├ín vß╗ï {p1['name']},{p2['name']},{p3['name']} type={expected_type}, thß╗▒c tß║┐={res['type']}")
+                if expected_apex is not None:
+                    self.assertEqual(res["vertex"], expected_apex,
+                                     f"─Éß╗ënh ─æß║╖c biß╗çt nh├ính li├¬n tß╗Ñc phß║úi l├á {expected_apex}")
+                else:
+                    self.assertIsNone(res["vertex"])
+
+        # --- PHß║ªN 3: CA KIM THß║¼T THß║▓NG H├ÇNG (rel_cross < 1e-5 theo c├┤ng thß╗⌐c chuß║⌐n h├│a l_max^2) ---
+        # A(0,0), B(1000,0), C(1000, 0.004) -> l_max=1000, cross=4.0, rel_cross = 4.0 / 1000^2 = 4e-6 < 1e-5
+        pts_collinear_needle = [
+            {"name": "A", "x": 0.0, "y": 0.0, "source": "free"},
+            {"name": "B", "x": 1000.0, "y": 0.0, "source": "free"},
+            {"name": "C", "x": 1000.0, "y": 0.004, "source": "free"}
+        ]
+        for perm in itertools.permutations(pts_collinear_needle):
+            p1, p2, p3 = perm
+            res = classify_triangle(p1, p2, p3)
+            self.assertFalse(res["is_triangle"], f"Ca kim y=0.004 vß╗¢i ho├ín vß╗ï {p1['name']},{p2['name']},{p3['name']} phß║úi bß╗ï nhß║¡n diß╗çn l├á thß║│ng h├áng (rel_cross < 1e-5)")
+            self.assertEqual(res["type"], "collinear")
+            self.assertIn("thß║│ng h├áng", res["message"].lower())
+
+    def test_32_drag_derived_point_then_drag_parent(self):
+        """Kiß╗âm tra Canvas GUI: K├⌐o trung ─æiß╗âm c├│ snap, sau ─æ├│ k├⌐o cha tß╗▒ do th├¼ tß╗ìa ─æß╗Ö trung ─æiß╗âm tß╗▒ cß║¡p nhß║¡t v├á cß╗¥ c┼⌐ bß╗ï x├│a bß╗Å"""
+        from geosolver.geosolver_desktop import GeoSolverApp, classify_triangle
+        app = None
+        errors = []
+        try:
+            app = GeoSolverApp(with_splash=False)
+            app.report_callback_exception = lambda exc, val, tb: errors.append((exc, val, tb))
+            app.update()
+
+            # 1. Tß║ío 2 ─æiß╗âm cha typed ban ─æß║ºu
+            pA = {"id": "PA", "name": "A", "x": 0.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
+            pB = {"id": "PB", "name": "B", "x": 4.0, "y": 0.0, "color": "#000", "fixed": False, "source": "typed", "exact": True}
+            app.points = [pA, pB]
+            app.redraw()
+            app.current_tool = "midpoint"
+            app._ask_point_name_dialog = lambda default_name: "M"
+
+            sxA, syA = app.to_screen(pA["x"], pA["y"])
+            app.canvas.event_generate("<ButtonPress-1>", x=int(sxA), y=int(syA))
+            app.update()
+
+            sxB, syB = app.to_screen(pB["x"], pB["y"])
+            app.canvas.event_generate("<ButtonPress-1>", x=int(sxB), y=int(syB))
+            app.update()
+
+            self.assertEqual(len(app.points), 3)
+            pM = app.points[2]
+            self.assertEqual(pM["source"], "midpoint")
+            self.assertEqual(pM["x"], 2.0)
+            self.assertEqual(pM["y"], 0.0)
+
+            # 2. Ng╞░ß╗¥i d├╣ng k├⌐o trung ─æiß╗âm M khi snap_to_grid bß║¡t
+            app.snap_to_grid = True
+            app.grid_step = 0.5
+            app.selected_points = [pM]
+            app.drag_start_world = (pM["x"], pM["y"])
+            sxM, syM = app.to_screen(2.5, 0.5)
+            app.canvas.event_generate("<B1-Motion>", x=int(sxM), y=int(syM))
+            app.update()
+
+            # 3. Sau ─æ├│ ng╞░ß╗¥i d├╣ng k├⌐o ─æiß╗âm cha pA tß╗▒ do (snap_to_grid tß║»t)
+            app.snap_to_grid = False
+            app.selected_points = [pA]
+            app.drag_start_world = (pA["x"], pA["y"])
+            dxA, dyA = 1.234, 0.567
+            sxDrag, syDrag = app.to_screen(pA["x"] + dxA, pA["y"] + dyA)
+            app.canvas.event_generate("<B1-Motion>", x=int(sxDrag), y=int(syDrag))
+            app.update()
+
+            # ─Éiß╗âm cha pA bß╗ï taint
+            self.assertEqual(pA["source"], "dragged")
+            self.assertFalse(pA["exact"])
+
+            # ─Éiß╗âm trung ─æiß╗âm pM phß║úi ─æ╞░ß╗úc tß╗▒ ─æß╗Öng recompute: tß╗ìa ─æß╗Ö cß║¡p nhß║¡t theo (pA + pB)/2
+            expected_mx = (pA["x"] + pB["x"]) / 2.0
+            expected_my = (pA["y"] + pB["y"]) / 2.0
+            self.assertAlmostEqual(pM["x"], expected_mx, places=5, msg="Tß╗ìa ─æß╗Ö x cß╗ºa trung ─æiß╗âm phß║úi cß║¡p nhß║¡t theo cha pA")
+            self.assertAlmostEqual(pM["y"], expected_my, places=5, msg="Tß╗ìa ─æß╗Ö y cß╗ºa trung ─æiß╗âm phß║úi cß║¡p nhß║¡t theo cha pA")
+
+            # Cß╗¥ lß╗ùi thß╗¥i cß╗ºa pM bß╗ï x├│a bß╗Å v├á l├ám t╞░╞íi lß║íi: source trß╗ƒ vß╗ü 'midpoint', kh├┤ng c├▓n exact=True
+            self.assertEqual(pM["source"], "midpoint")
+            self.assertIsNone(pM.get("exact"), "Cß╗¥ exact c┼⌐ phß║úi bß╗ï loß║íi bß╗Å (pop) ─æß╗â kß║┐ thß╗½a taint tß╗½ cha")
+
+            # 4. Ph├ón loß║íi tam gi├íc tß║ío bß╗ƒi pM, pB v├á mß╗Öt ─æiß╗âm typed kh├íc pC -> bß║»t buß╗Öc bß╗ï taint (exact=False, origin_exact=False)
+            pC = {"id": "PC", "name": "C", "x": 2.0, "y": 4.0, "source": "typed", "exact": True}
+            res = classify_triangle(pM, pB, pC)
+            self.assertIs(res["origin_exact"], False, "Tam gi├íc chß╗⌐a trung ─æiß╗âm c├│ cha bß╗ï k├⌐o tß╗▒ do bß║»t buß╗Öc c├│ origin_exact=False")
+            self.assertFalse(res["exact"])
+            self.assertFalse(res["is_discrete"], "─Éiß╗âm tainted bß║»t buß╗Öc ─æi v├áo nh├ính dung sai li├¬n tß╗Ñc (is_discrete=False)")
+
+            self.assertEqual(errors, [], f"Kh├┤ng ─æ╞░ß╗úc c├│ ngoß║íi lß╗ç trong Tkinter callback: {errors}")
+        finally:
+            if app is not None:
+                app.destroy()
+
 if __name__ == "__main__":
     unittest.main()

```

### 6.3. Bảng mã băm SHA-256 toàn vẹn của tất cả các file cấu thành
Toàn bộ mã băm dưới đây được tính toán trực tiếp bằng thuật toán SHA-256 trên Windows:

| Đường dẫn tệp | Kích thước | Mã băm SHA-256 Toàn vẹn | Vai trò trong hệ thống |
| :--- | :---: | :--- | :--- |
| `geosolver\geosolver_desktop.py` | 651 KB | `F91F2CDAA31823C41B2947958BA696F0C0E8C9788C235688E221F3B3A5DE1461` | Mã nguồn GUI, Canvas DAG & Lõi hình học |
| `stem_shared_core\ai_local_manager.py` | 54 KB | `5C5127C8DF1C83AA8517614DD28F4E67F132A63B88B1818E8497A43D81A13A9F` | Quản lý Win32 DPAPI, SSL certifi & Local AI |
| `tests\test_geometry_invariants.py` | 46 KB | `14DD2F9F3E016CF20CEC4E28DF0202B0277B33175DC85492B5D83983157AC812` | Bộ 32 bài test bất biến, taint & tích hợp Canvas |
| `tests\test_round9_taint_validation.py` | 5.2 KB | `B77977E44249EC7477D70A37A5C227F37EDBE2E8E034BDCFEB7F7D4279FBFB15` | Bộ 11 bài test xác thực Taint độc lập |
| `geosolver\GeoSolver.spec` | 2.1 KB | `5514177387F812B81BAA1C3D3B08FBE34A3B99644B5E399C6E828C0C8AA1BC1C` | Cấu hình biên dịch đóng gói PyInstaller |
| `msix_layout\AppxManifest.xml` | 1.8 KB | `BBD7CF9D78635B4C1B2DA7C00867A2FEEC4267CBEE17FA6395F39D673B0E57B6` | Tệp kê khai phân phối ứng dụng Windows AppX |
| `dist\GeoSolver\GeoSolver.exe` | 13.9 MB | `058B5F209AB985198A97D382670346C383302D3DB0502E5D53E7764095DAAC6A` | Tệp thực thi nhị phân chính thức (Production) |
| `dist\GeoSolver_v3.1.msix` | 92.4 MB | `6164C2774E0C0707745D40BD9D09EDD7437078F39BED9469008736657695B19C` | Gói cài đặt phân phối chính thức cho Windows |

---

## 7. BIÊN BẢN & PHIẾU QUYẾT ĐỊNH NGHIỆM THU DÀNH CHO CLAUDE CODE

> [!IMPORTANT]
> **DÀNH RIÊNG CHO CLAUDE CODE ĐÁNH GIÁ VÀ ĐIỀN THÔNG TIN.**
> Nhóm phát triển cam kết giữ nguyên trạng toàn bộ các ô lựa chọn và phần nhận xét dưới đây ở trạng thái **hoàn toàn để trống**, không điền sẵn bất kỳ nội dung nào.

### PHIẾU ĐÁNH GIÁ CHẤT LƯỢNG PHẦN MỀM (GEOSOLVER 2D v3.1 RC4)

- **Trụ cột 1: Lõi hình học & Bất biến tỷ lệ / Hoán vị:**
  - Đánh giá của Chuyên gia: `[   ]` ĐẠT  /  `[   ]` CHƯA ĐẠT
  - Nhận xét chi tiết: __________________________________________________________________

- **Trụ cột 2: Cơ chế Taint Tracking & Quản lý Phả hệ Canvas GUI:**
  - Đánh giá của Chuyên gia: `[   ]` ĐẠT  /  `[   ]` CHƯA ĐẠT
  - Nhận xét chi tiết: __________________________________________________________________

- **Trụ cột 3: Độ bao phủ kiểm thử tự động (43/43 Tests):**
  - Đánh giá của Chuyên gia: `[   ]` ĐẠT  /  `[   ]` CHƯA ĐẠT
  - Nhận xét chi tiết: __________________________________________________________________

- **Trụ cột 4: Đóng gói MSIX, Bảo mật DPAPI & Hoạt động trong Sandbox Windows:**
  - Đánh giá của Chuyên gia: `[   ]` ĐẠT  /  `[   ]` CHƯA ĐẠT
  - Nhận xét chi tiết: __________________________________________________________________

---

### KẾT LUẬN THẨM ĐỊNH CUỐI CÙNG

- `[   ]` **CHẤP THUẬN TOÀN DIỆN (APPROVED FOR GENERAL AVAILABILITY)**
  *Đồng ý cho phép GeoSolver 2D v3.1 RC4 xuất bản chính thức lên Microsoft Store và phát hành rộng rãi tới người dùng.*

- `[   ]` **CHẤP THUẬN CÓ ĐIỀU KIỆN (CONDITIONALLY APPROVED)**
  *Yêu cầu bổ sung các điểm nhỏ không ảnh hưởng đến an toàn hệ thống trước khi mở tải.*

- `[   ]` **TỪ CHỐI / YÊU CẦU LÀM LẠI (REJECTED)**
  *Phát hiện lỗi nghiêm trọng, yêu cầu đội ngũ kỹ thuật giải trình và ra bản RC5.*

---

**Ý KIẾN TỔNG QUAN CỦA CLAUDE CODE:**

__________________________________________________________________________________________
__________________________________________________________________________________________
__________________________________________________________________________________________
__________________________________________________________________________________________

**Chữ ký Chuyên gia Thẩm định Độc lập:**

*(Ký và ghi rõ ngày đánh giá)*
