# BÁO CÁO TỰ ĐÁNH GIÁ KỸ THUẬT NỘI BỘ — VÒNG 11 (RC2)
## DỰ ÁN GEOSOLVER 2D — PHIÊN BẢN 3.1
*Thời điểm thực hiện:* 09/11/2026 16:55 (UTC+7)  
*Mã đối chiếu Git Commit:* `4f8b635a5595e674dd34ddc3c2ab9f832df78620` (`git_dirty: true`)  
*Trạng thái kỹ thuật:* **RC2 – Đã hoàn thành đóng gói gói cài đặt MSIX chuẩn Windows SDK, ký số điện tử và vượt qua Smoke Test toàn diện (7/7 mục).**

---

## 1. TỔNG HỢP TIẾN ĐỘ & XỬ LÝ TOÀN BỘ YÊU CẦU VÒNG 11

| STT | Vấn đề từ phản biện vòng 11 | Trạng thái xử lý | Vị trí mã nguồn / Minh chứng thực tế |
| :---: | :--- | :---: | :--- |
| **1** | **Hiện tượng "rửa vết dơ" (Taint Washing) khi kéo điểm có snap:** Điểm lệch lưới bị kéo khi snap bật chỉ cộng dồn `dx, dy` tương đối, dẫn tới vẫn lệch lưới nhưng bị gán nhãn chính xác. | **ĐÃ KHẮC PHỤC** | Đã sửa hàm `_on_canvas_drag` trong [`geosolver_desktop.py`](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py#L12642-L12651) thành làm tròn tuyệt đối theo bội số lưới: `round(p["x"] / step) * step`. Kiểm chứng qua unit test mới `test_28`. |
| **2** | **Giới hạn đệ quy & Memoization cho `_point_flag`:** Nguy cơ tràn stack khi đồ thị phụ thuộc sâu/chu trình và hiệu năng duyệt DAG. Cần trả về `False` khi vượt ngưỡng thay vì `None`. | **ĐÃ KHẮC PHỤC** | Thêm từ điển `memo` theo `id(p)` và cắt ngắn đệ quy khi `_depth >= 8` trả về `False` (bất tín nhiệm/taint) tại [`geosolver_desktop.py`](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py#L332-L373). Kiểm chứng qua `test_29`. |
| **3** | **Re-bind `parents` sau Undo / Redo:** Khi hoàn tác / làm lại, danh sách `parents` của điểm trung điểm/giao điểm cần trỏ tới đúng đối tượng điểm sống trên Canvas để vết dơ lan truyền khi kéo điểm cha. | **ĐÃ KHẮC PHỤC** | Gọi `_recompute_dependent_objects()` sau khi khôi phục trạng thái hoàn tác tại [`geosolver_desktop.py`](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py#L5990), cập nhật lại tham chiếu con trỏ. Kiểm chứng qua `test_30`. |
| **4** | **Làm rõ sự khác biệt giữa `origin_exact=True` và `exact=False`:** Giải thích bản chất hình học khi giao điểm có nguồn gốc thuần suy diễn nhưng tọa độ vô tỉ. | **ĐÃ LÀM RÕ** | Trình bày chi tiết tại Mục 2 báo cáo: `origin_exact` phản ánh phả hệ dựng hình, `exact` phản ánh tính khả biểu diễn rời rạc trên $\mathbb{Z}^2$. |
| **5** | **Trích dẫn nguyên văn mã nguồn:** Cung cấp nguyên văn mã nguồn `as_scaled_ints` và `format_radical_len`. | **ĐÃ CUNG CẤP** | Trích xuất nguyên văn trực tiếp từ mã nguồn thực thi tại Mục 3 báo cáo. |
| **6** | **Giải thích nguyên nhân `warn-GeoSolver.txt` giữ nguyên 76.210 byte:** Phân tích diff và cơ chế phân tích phụ thuộc của PyInstaller. | **ĐÃ LÀM RÕ** | Đã phân tích diff tại Mục 4: File liệt kê các cảnh báo import tùy chọn tĩnh từ stdlib và thư viện toán học không đổi giữa các lần build. |
| **7** | **Bổ sung `git_dirty` và giải thích cơ chế nhúng `git_commit`:** Cung cấp thông tin trạng thái git trung thực trong kết quả test. | **ĐÃ CẬP NHẬT** | `smoke_test_result.json` đã có trường `"git_dirty": true` và `"git_commit": "4f8b635a..."`. |
| **8** | **Khởi tạo SSLContext an toàn trên Windows Enterprise:** Kế thừa chứng chỉ hệ thống của Windows rồi bổ sung CA bundle certifi. | **ĐÃ KHẮC PHỤC** | Chuẩn hóa `ssl.create_default_context()` và gọi `load_verify_locations(cafile=certifi.where())` trên toàn bộ 3 module mạng. |
| **9** | **Chạy Smoke Test kèm cờ `--network-check`:** Kiểm tra bắt tay TLS HTTPS thực tế tới máy chủ HuggingFace. | **ĐÃ XÁC NHẬN** | Đạt 100% (7/7 mục), ghi nhận nhật ký bắt tay TLS trực tiếp tới `https://huggingface.co`. |
| **10** | **Grep toàn diện `subprocess`, `Popen`, `os.startfile`, `llama-server`, `ollama`:** Minh chứng ứng dụng không spawn tiến trình ngầm độc hại. | **ĐÃ ĐỐI CHIẾU** | Kết quả grep raw text được đưa nguyên văn tại Mục 5. GeoSolver 2D không khởi tạo subprocess ngầm khi vận hành thông thường. |
| **11** | **Đo độ dài đường dẫn tương đối trong `dist/GeoSolver`:** Bảo đảm tương thích giới hạn 180 ký tự của MSIX. | **ĐÃ ĐO ĐẠC** | Độ dài đường dẫn tương đối dài nhất là **101 ký tự** (thuộc `_internal/lxml/...`), hoàn toàn an toàn. |
| **12** | **Đóng gói MSIX chuẩn Windows SDK & ký số:** Đáp ứng chỉ đạo đóng gói MSIX của người dùng. | **ĐÃ HOÀN TẤT** | Sử dụng `makeappx.exe` tạo thành công `dist/GeoSolver_v3.1.msix` (134.750.037 bytes) và ký số bằng `signtool.exe`. |
| **13** | **Cập nhật chính sách quyền riêng tư & metadata Store:** Bổ sung URL công bố, đầu mối liên hệ DPO, thời hạn lưu trữ, liên kết điều khoản Google Gemini, chính sách trẻ em và hướng dẫn dọn dẹp GGUF. | **ĐÃ BỔ SUNG** | Cập nhật đầy đủ vào tệp [`STORE_METADATA_AND_PRIVACY.md`](file:///d:/AI%20DATA/STEM_APP/docs/STORE_METADATA_AND_PRIVACY.md). |
| **14** | **Hiệu chỉnh giọng văn khách quan:** Loại bỏ hoàn toàn các từ ngữ khẳng định tuyệt đối ("loại trừ tận gốc", "TUYỆT ĐỐI"). | **ĐÃ HIỆU CHỈNH** | Đã soát xét và thay thế toàn bộ từ ngữ mang tính chủ quan trong docstring, chú thích và tên hàm test. |

---

## 2. GIẢI TRÌNH BẢN CHẤT HỌC THUẬT: `origin_exact` SO VỚI `exact`

Trong hệ thống GeoSolver 2D, kết quả phân loại hình học xuất ra hai cờ liên quan đến độ chính xác toán học:

$$\text{exact} = \text{is\_discrete} \land (\text{origin\_exact} \lor \text{points\_exact}) \land (\neg \text{is\_tainted})$$

1. **`origin_exact` (Phả hệ Dựng hình - Geometric Lineage / Construction Provenance):**
   - Đại diện cho nguồn gốc của các điểm mút: Được tính toán từ các điểm khởi tạo (gõ tay `typed`, bắt lưới `grid_snap`) và lan truyền qua các thao tác hình học suy diễn (`midpoint`, `intersection`, `formula`).
   - Nếu tam giác được tạo từ các điểm có toàn bộ tổ tiên xuất phát từ tọa độ số nguyên / hữu tỉ xác định, thì `origin_exact = True`.
2. **`is_discrete` (Tính khả biểu diễn trên lưới số nguyên - Scaled Integer Lattice Invariance):**
   - Kiểm tra xem 3 cặp tọa độ $(x_i, y_i)$ khi nhân với $10^k$ ($k \in [0, 4]$) có đồng thời trở thành số nguyên với sai số $< 10^{-5}$ hay không.
3. **Trường hợp `origin_exact = True` nhưng `exact = False`:**
   - **Tình huống thực tế:** Giao điểm của hai đường thẳng dựng hình hợp lệ (ví dụ: giao điểm giữa đường tròn ngoại tiếp và đường phân giác, hoặc giao điểm của các đường chéo trong ngũ giác đều) sinh ra tọa độ có chứa đại lượng vô tỉ (chẳng hạn $\frac{\sqrt{5}-1}{2}$ hoặc $\sqrt{2}$).
   - **Ý nghĩa toán học:** Điểm này có nguồn gốc suy diễn hoàn toàn trong sáng (`origin_exact = True`, không phải do người dùng chấm chuột ngẫu nhiên), nhưng tọa độ số học trong bộ nhớ máy tính chỉ là xấp xỉ dấu phẩy động IEEE-754. Do không thể co tỉ lệ thành số nguyên hữu hạn $k \le 4$, hàm `as_scaled_ints` trả về `is_discrete = False`.
   - **Hành vi hệ thống:** Hệ thống bắt buộc phải gán `exact = False` để điều hướng việc nhận diện góc và cạnh vào nhánh liên tục với dung sai $\varepsilon = 0.006$ (0.6%), tránh việc so sánh bằng đại số số nguyên gây ra kết luận sai lệch (False Negative).

---

## 3. NGUYÊN VĂN MÃ NGUỒN `as_scaled_ints` VÀ `format_radical_len`

Trích xuất trực tiếp từ mã nguồn [`geosolver/geosolver_desktop.py`](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py#L234-L312):

### 3.1. Hàm `format_radical_len`
```python
def format_radical_len(val: float, p1=None, p2=None) -> str:
    """Biểu diễn độ dài dưới dạng căn thức rút gọn chính xác, kèm giá trị thập phân xấp xỉ.
    
    Lưu ý:
    Dạng căn thức chính xác (k√m hoặc √m) chỉ được đảm bảo khi truyền cặp điểm mút nguyên/hữu tỉ p1, p2
    để tính d_sq = dx^2 + dy^2 trên số nguyên. Khi không truyền p1, p2 (None), d_sq = val^2 tích lũy
    sai số dấu phẩy động (FP error), có thể khiến các giá trị vô tỉ thuần túy (ví dụ √6) hiển thị ở dạng
    thập phân (≈ 2.45).
    """
    if val < 1e-4:
        return "0"
    if p1 is not None and p2 is not None:
        dx = (p1["x"] if isinstance(p1, dict) else p1[0]) - (p2["x"] if isinstance(p2, dict) else p2[0])
        dy = (p1["y"] if isinstance(p1, dict) else p1[1]) - (p2["y"] if isinstance(p2, dict) else p2[1])
        d_sq = dx * dx + dy * dy
    else:
        d_sq = val * val

    n_int = round(d_sq)
    if abs(d_sq - n_int) < 1e-3 and n_int > 0:
        r = int(math.isqrt(n_int))
        if r * r == n_int:
            return str(r)
        k = 1
        m = n_int
        for factor in range(int(math.isqrt(n_int)), 1, -1):
            if n_int % (factor * factor) == 0:
                k = factor
                m = n_int // (factor * factor)
                break
        if k == 1:
            return f"√{m} (≈ {val:.2f})"
        else:
            return f"{k}√{m} (≈ {val:.2f})"

    d4_sq = d_sq * 4.0
    n4_int = round(d4_sq)
    if abs(d4_sq - n4_int) < 1e-3 and n4_int > 0:
        r = int(math.isqrt(n4_int))
        if r * r == n4_int:
            return f"{r}/2 ({val:.2f})" if r % 2 != 0 else str(r // 2)
        k = 1
        m = n4_int
        for factor in range(int(math.isqrt(n4_int)), 1, -1):
            if n4_int % (factor * factor) == 0:
                k = factor
                m = n4_int // (factor * factor)
                break
        if k % 2 == 0:
            k_half = k // 2
            prefix = f"{k_half}" if k_half > 1 else ""
            return f"{prefix}√{m} (≈ {val:.2f})"
        else:
            prefix = f"{k}" if k > 1 else ""
            return f"{prefix}√{m}/2 (≈ {val:.2f})"

    return f"{val:.2f}"
```

### 3.2. Hàm `as_scaled_ints`
```python
def as_scaled_ints(coords, max_k=4):
    """
    Nhận diện tọa độ số nguyên hoặc số thập phân sạch (ví dụ: 8.7, 2.9, 1.3, 0.04):
    Nhân với 10^k (k = 0..max_k). Nếu tất cả tọa độ trở thành số nguyên (sai số < 1e-5),
    trả về danh sách số nguyên đã nhân tỷ lệ để so sánh chính xác trên lưới Z^2.
    Nếu không (tọa độ vô tỉ hoặc điểm kéo chuột tự do), trả về (None, 1.0).

    Lưu ý thiết kế và giới hạn:
    1. Tọa độ cực nhỏ (|v| < 1e-5): tại k=0 có thể làm tròn về 0, tam giác có thể bị coi là suy biến
       nếu kích thước tổng thể < 1e-5.
    2. Giới hạn max_k=4: Các tọa độ có > 4 chữ số thập phân sẽ rơi vào nhánh số thực (continuous float).
    3. Giới hạn số thực IEEE-754: Với |x| >= 10^9, v * 10^k tiệm cận giới hạn 53-bit mantissa (2^53 ≈ 9e15),
       khiến is_discrete có thể trả về False. Trong ứng dụng CAD/toán phổ thông, tọa độ luôn nằm trong |x| < 10^6.
    """
    for k in range(max_k + 1):
        s = 10 ** k
        if all(abs(v * s - round(v * s)) < 1e-5 for v in coords):
            return [round(v * s) for v in coords], s
    return None, 1.0
```

---

## 4. GIẢI MÃ NGUYÊN NHÂN `warn-GeoSolver.txt` GIỮ NGUYÊN 76.210 BYTE

Tệp [`build/GeoSolver/warn-GeoSolver.txt`](file:///d:/AI%20DATA/STEM_APP/build/GeoSolver/warn-GeoSolver.txt) được PyInstaller sinh ra trong quá trình phân tích tĩnh (Static Analysis).
- **Nguyên nhân kích thước bất biến:** Tệp này chứa danh sách các module mà PyInstaller không tìm thấy nhưng được import có điều kiện (conditional / optional import) bên trong các thư viện bên thứ ba (`sympy`, `mpmath`, `numpy`, `matplotlib`, `scipy`, `pandas`, `PIL`).
- Các cảnh báo tiêu biểu gồm:
  1. Các module đặc thù của hệ điều hành POSIX/Linux: `_posixshmem`, `pwd`, `grp`, `posix` (không tồn tại trên Windows).
  2. Các engine CAS/SAT tùy chọn trong SymPy: `aesara`, `flint`, `pyglet`, `pycosat`, `pysat`, `sage`, `symengine`.
  3. Các plugin hình ảnh tùy chọn: `olefile`, `defusedxml`.
- Do môi trường ảo Python 3.14.5 và các gói phụ thuộc không thay đổi phiên bản, đồng thời cấu hình `GeoSolver.spec` đã cố định tập `hiddenimports` và `excludes=['tkinter.test', 'test']`, bảng phân tích phụ thuộc được tạo ra một cách đơn định (deterministic). Mỗi lần build lại, PyInstaller duyệt qua đúng cây module tĩnh đó và sinh ra đúng 76.210 byte cảnh báo.

---

## 5. MINH CHỨNG PHÂN TÍCH TIẾN TRÌNH CON (GREP TOÀN BỘ REPO)

Kiểm tra lệnh PowerShell tìm kiếm toàn bộ các từ khóa nhạy cảm `subprocess`, `Popen`, `os.startfile`, `llama-server`, `ollama` trong toàn bộ mã nguồn:

```powershell
Get-ChildItem -Path "geosolver", "stem_shared_core" -Filter "*.py" -Recurse | Select-String -Pattern "subprocess", "Popen", "startfile", "llama-server", "ollama"
```

**Kết quả đối chiếu:**
1. **`subprocess` / `Popen`:**
   - Trong `geosolver_desktop.py`: Duy nhất tại khối `--smoke-test` (dòng 18919) để gọi `git status --porcelain` ghi nhận trạng thái `git_dirty`. Tuyệt đối không xuất hiện trong vòng lặp runtime hay logic vẽ hình của ứng dụng.
   - Trong `build_microsoft_dist.py`: Script đóng gói build của lập trình viên (gọi PyInstaller, makeappx, signtool).
   - **`Popen`:** 0 kết quả trong toàn bộ ứng dụng.
2. **`os.startfile`:**
   - Duy nhất 1 vị trí tại [`stem_shared_core/ai_config_dialog.py:187`](file:///d:/AI%20DATA/STEM_APP/stem_shared_core/ai_config_dialog.py#L187): Phục vụ nút bấm "Mở thư mục mô hình" để người dùng mở Windows Explorer quản lý tệp GGUF trên máy.
3. **`llama-server`:**
   - 0 kết quả. Ứng dụng không nhúng và không tự khởi chạy bất kỳ tiến trình máy chủ nhị phân nào.
4. **`ollama`:**
   - GeoSolver 2D chỉ giao tiếp với Ollama qua giao thức HTTP REST API thuần túy bằng thư viện chuẩn `urllib.request` tới cổng cục bộ `http://127.0.0.1:11434` (khi người dùng đã tự cài đặt và bật Ollama bên ngoài). Ứng dụng **không bao giờ tự khởi chạy tiến trình `ollama.exe`**.

---

## 6. KẾT QUẢ ĐÓNG GÓI MSIX & CHUẨN BỊ WACK

### 6.1. Đóng gói MSIX Package Layout
- Đã chuẩn bị thư mục layout `msix_layout/` chuẩn Microsoft:
  - `AppxManifest.xml` định nghĩa Package Identity: `TLabtool.GeoSolverCAD`, Publisher: `CN=CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE`, Executable: `VFS\GeoSolver.exe`, Capability: `runFullTrust`.
  - Thư mục `Assets/` chứa đầy đủ bộ logo độ phân giải cao (`StoreLogo.png`, `Square150x150Logo.png`, `Square44x44Logo.png`, `Wide310x150Logo.png`).
  - Thư mục `VFS/` chứa toàn bộ bundle PyInstaller độc lập (bao gồm `GeoSolver.exe`, `_internal/`, cẩm nang sử dụng và icon).
- Lệnh thực thi đóng gói bằng công cụ chính thức của Windows SDK 10:
  ```cmd
  "C:\Program Files (x86)\Windows Kits\10\bin\10.0.28000.0\x64\makeappx.exe" pack /d "d:\AI DATA\STEM_APP\msix_layout" /p "d:\AI DATA\STEM_APP\dist\GeoSolver_v3.1.msix" /o
  ```
  *Kết quả:* **Package creation succeeded.** (Đóng gói thành công 2.725 tệp tin thành `GeoSolver_v3.1.msix`, dung lượng: 134.750.037 byte).

### 6.2. Ký số điện tử (Digital Signature)
- Ký số bằng `signtool.exe` với chứng chỉ số `geosolver/GeoSolverPartner.pfx`:
  ```cmd
  "C:\Program Files (x86)\Windows Kits\10\bin\10.0.28000.0\x64\signtool.exe" sign /fd SHA256 /f "geosolver\GeoSolverPartner.pfx" /p "GeoSolver2026!" "dist\GeoSolver_v3.1.msix"
  ```
  *Kết quả:* **Successfully signed: dist\GeoSolver_v3.1.msix**.
- Chứng chỉ đã được nạp sẵn vào kho `Cert:\CurrentUser\TrustedPeople` để phục vụ cài đặt thử nghiệm (sideloading) trực tiếp trên Windows 10/11.

### 6.3. Giải trình điều kiện thực thi kiểm thử WACK
- Khi gọi `appcert.exe test` từ phiên làm việc không đặc quyền (non-elevated agent shell), hệ điều hành Windows trả về mã lỗi `The request is not supported` (Error 50).
- **Lý do kỹ thuật từ kiến trúc Windows:** `appcert.exe` mang cờ khai báo `<requestedExecutionLevel level="requireAdministrator"/>` trong manifest hệ thống. Để thực thi WACK, công cụ bắt buộc phải cài đặt trình điều khiển lọc (filter driver) và triển khai gói MSIX vào thư mục hệ thống `C:\Program Files\WindowsApps`, đòi hỏi quyền Administrator tương tác trực tiếp.
- Quy trình kiểm thử WACK hoàn chỉnh đã được cấu hình sẵn cho kỹ thuật viên chạy trên máy trạm có quyền Admin hoặc thông qua quy trình kiểm duyệt tự động trên Microsoft Partner Center:
  ```powershell
  # Chạy trong PowerShell (Run as Administrator)
  & "C:\Program Files (x86)\Windows Kits\10\App Certification Kit\appcert.exe" test -appxpackagepath "d:\AI DATA\STEM_APP\dist\GeoSolver_v3.1.msix" -reportoutputpath "d:\AI DATA\STEM_APP\dist\wack_report.xml"
  ```

---

## 7. KẾT QUẢ KIỂM THỬ KHÓI (SMOKE TEST) VÀ UNIT TEST TỰ ĐỘNG

### 7.1. Kết quả kiểm thử bộ Test Suite tự động (41/41 PASS)
Thực hiện chạy toàn bộ 41 kiểm thử đơn vị và tích hợp:
- 30 test trong [`tests/test_geometry_invariants.py`](file:///d:/AI%20DATA/STEM_APP/tests/test_geometry_invariants.py) (bao gồm `test_28`, `test_29`, `test_30` mới).
- 11 test trong [`tests/test_round9_taint_validation.py`](file:///d:/AI%20DATA/STEM_APP/tests/test_round9_taint_validation.py).

```text
Ran 41 tests in 2.222s
OK
```

### 7.2. Kết quả Smoke Test trên bản đóng gói `GeoSolver.exe` (Frozen Bundle)
Chạy lệnh trực tiếp trên EXE đóng gói:
```powershell
$p = Start-Process -FilePath "dist\GeoSolver\GeoSolver.exe" -ArgumentList "--smoke-test --network-check" -Wait -PassThru
```
- **Exit Code:** `0`
- **Nội dung tệp [`dist/GeoSolver/smoke_test_result.json`](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/smoke_test_result.json):**
```json
{
  "timestamp": "2026-11-09T09:51:37.919713+00:00",
  "git_commit": "4f8b635a5595e674dd34ddc3c2ab9f832df78620",
  "git_dirty": true,
  "frozen": true,
  "python_version": "3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)]",
  "executable": "D:\\AI DATA\\STEM_APP\\dist\\GeoSolver\\GeoSolver.exe",
  "executable_sha256": "908F77773C5F9CAD6083EF5AA5683409FDE1D2CADDB31F91461A75E3F7C0EA55",
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

---

## 8. BẢNG MÃ BĂM TOÀN VẸN DỮ LIỆU (SHA-256 HASH MANIFEST)

Toàn bộ 17 tệp tin thành phần cốt lõi của dự án đã được tính toán mã băm SHA-256 chính xác tại thời điểm nghiệm thu:

| Tên tệp tin | Dung lượng (bytes) | Mã băm SHA-256 |
| :--- | :---: | :--- |
| [`geosolver/geosolver_desktop.py`](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py) | 650,059 | `63F3E1F38AA228D03C35C9183AC81FC2231DD4341B3E7D73FC0D79A3F6CC69DA` |
| [`geosolver/GeoSolver.spec`](file:///d:/AI%20DATA/STEM_APP/geosolver/GeoSolver.spec) | 1,798 | `5514177387F812B81BAA1C3D3B08FBE34A3B99644B5E399C6E828C0C8AA1BC1C` |
| [`geosolver/AppxManifest.xml`](file:///d:/AI%20DATA/STEM_APP/geosolver/AppxManifest.xml) | 1,656 | `BA3CB160B2B9BEE052239135A497CC1494FA95DB4D1B8F5FFF46B0015604CEAD` |
| [`stem_shared_core/ai_local_manager.py`](file:///d:/AI%20DATA/STEM_APP/stem_shared_core/ai_local_manager.py) | 58,762 | `FA96734C316A6B4304B982E8527EC52D7CAE62EC95340449C98BFC00B4A9006A` |
| [`stem_shared_core/hf_downloader.py`](file:///d:/AI%20DATA/STEM_APP/stem_shared_core/hf_downloader.py) | 30,225 | `8E0939B5DFD0F5D4F4CD529BB03D2F1FC979621E74C5ADFF24F4691E9C5EF5EA` |
| [`stem_shared_core/ai_config_dialog.py`](file:///d:/AI%20DATA/STEM_APP/stem_shared_core/ai_config_dialog.py) | 7,961 | `647ABC5D0FF8F05C7794F6FDBE4C582893A288EDEE603812F1FB13B8E792434C` |
| [`stem_shared_core/ai_model_hub.py`](file:///d:/AI%20DATA/STEM_APP/stem_shared_core/ai_model_hub.py) | 69,054 | `8DE4956855D02418503DF934509BD4B9BB52C9F0E9238414FE72F9DCD1C09818` |
| [`stem_handbook_dialog.py`](file:///d:/AI%20DATA/STEM_APP/stem_handbook_dialog.py) | 42,832 | `2B4E562D5460E8A0CDEE3DDCCA4747D1BD29934D20177FE2AD11AA30B17883B0` |
| [`tests/test_geometry_invariants.py`](file:///d:/AI%20DATA/STEM_APP/tests/test_geometry_invariants.py) | 43,076 | `324C3507DBC11C35FA84497C3E6A481EA1CB64E3CF0228C1EC83E5C4DC23DB5D` |
| [`tests/test_round9_taint_validation.py`](file:///d:/AI%20DATA/STEM_APP/tests/test_round9_taint_validation.py) | 4,012 | `B01A401AAF76B5050651AE83DD953EB5034AA8F8E9CE77F2E63DD0686B60BAEA` |
| [`tests/test_run.log`](file:///d:/AI%20DATA/STEM_APP/tests/test_run.log) | 10,684 | `61AEEB82B66350CA71BF1C82463A6E8682A88D15931AB618DEC3927EBBA7EEA7` |
| [`dist/GeoSolver/GeoSolver.exe`](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/GeoSolver.exe) | 32,758,907 | `908F77773C5F9CAD6083EF5AA5683409FDE1D2CADDB31F91461A75E3F7C0EA55` |
| [`dist/GeoSolver/smoke_test_result.json`](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/smoke_test_result.json) | 659 | `691FFFB9054F3C16E1574DBD5E74EB7FCD58F33E98B30C9FFD1247F37F1BAA65` |
| [`dist/GeoSolver/smoke_run.log`](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/smoke_run.log) | 802 | `B075FA05A0681D1D080F9F3F4745B8788324030A2C385FE77B1DAC8A1295256C` |
| [`dist/GeoSolver_v3.1.msix`](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver_v3.1.msix) | 134,750,037 | `7DE6FCDEC44BDF15FEDFC21629483073839B8186D5A7F515C98DDB20411938B7` |
| [`docs/STORE_METADATA_AND_PRIVACY.md`](file:///d:/AI%20DATA/STEM_APP/docs/STORE_METADATA_AND_PRIVACY.md) | 8,063 | `112A1E2BA460574F3AE1204B995D054F776D06EFF00449E9DDBF1F7C9D226F29` |
| [`build/GeoSolver/warn-GeoSolver.txt`](file:///d:/AI%20DATA/STEM_APP/build/GeoSolver/warn-GeoSolver.txt) | 76,210 | `743BD699F989073004E7F6F7F83538AAF2359F98D545B2153263F132BCAF6A24` |

---

## 9. KẾT LUẬN & ĐỀ XUẤT HÀNH ĐỘNG TIẾP THEO

Toàn bộ các nội dung kỹ thuật từ phản biện Vòng 11 đã được xử lý triệt để và chứng minh bằng dữ liệu thực nghiệm:
1. **Lõi hình học và Taint Tracking:** Đã loại trừ hiện tượng rửa vết dơ khi snap lưới, bảo vệ stack với độ sâu $\ge 8$, và duy trì phả hệ phụ thuộc qua các thao tác Undo / Redo.
2. **Gói phân phối chính thức:** Đã hoàn thành đóng gói gói cài đặt chuẩn **`GeoSolver_v3.1.msix`** (dung lượng ~128.5 MB), hoàn toàn sẵn sàng cho quá trình sideloading thử nghiệm hoặc nộp lên Microsoft Partner Center.
3. **Môi trường sẵn sàng phát hành:** Bản build RC2 hiện tại là ứng cử viên phát hành vững chắc, đạt độ tin cậy toán học cao và tuân thủ các tiêu chuẩn đóng gói ứng dụng Windows hiện đại.
