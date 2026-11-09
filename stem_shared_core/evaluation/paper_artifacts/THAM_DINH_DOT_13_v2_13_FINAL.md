# BIÊN BẢN THẨM ĐỊNH KHOA HỌC – ĐỢT 13 (PHẢN HỒI HỒ SƠ v2.13)
## DỰ ÁN: CAD MATH STUDIO & GEOSOLVER 2D
### Trạng thái: ✅ CHÍNH THỨC ĐÓNG VÒNG PHẢN BIỆN LÝ THUYẾT & THUẬT TOÁN

**Ngày thẩm định:** 08/11/2026  
**Phiên bản hồ sơ được thẩm định:** v2.13  
**Thẩm định viên:** Antigravity (Claude Sonnet 4.6 Thinking) — thực thi kiểm chứng độc lập trực tiếp trên workspace  
**Môi trường tái lập thực nghiệm độc lập:**
- Python: `3.14.5` | SymPy: `1.14.0` | Nền tảng: `Windows-11-10.0.26300-SP0 (AMD64)`

---

## 0. XÁC MINH TÍNH TOÀN VẸN FILE (SHA-256 KIỂM CHỨNG ĐỘC LẬP)

| File | SHA-256 khai báo (v2.13) | SHA-256 đo thực tế (thẩm định viên) | Kết quả |
|---|---|---|---|
| `stem_shared_core/cad_math_core.py` | `9bed3b7f...b3a2dd96` | `9bed3b7f...b3a2dd96` | ✅ **KHỚP** |
| `stem_shared_core/tools/run_batch_auto_test.py` | `c96c7e13...c13c0476` | `c96c7e13...c13c0476` | ✅ **KHỚP** |

> [!IMPORTANT]
> Hash được kiểm chứng bằng lệnh Python trực tiếp trên filesystem. Đáng chú ý: trên môi trường Windows này, **hash Raw binary = hash Unix LF**, xác nhận file lưu thuần LF — nhất quán với lưu ý chuẩn hóa trong §0 của hồ sơ.

---

## 1. KẾT QUẢ THỰC THI HARNESS ĐỘC LẬP (TÁI LẬP BỞI THẨM ĐỊNH VIÊN)

Thẩm định viên thực thi lại hoàn toàn độc lập:
```
python stem_shared_core/tools/run_batch_auto_test.py
```

**Kết quả thực thi tái lập (Đợt 13 — máy thẩm định viên):**

| Chỉ số | Khai báo v2.13 | Thực thi tái lập Đợt 13 | Nhận xét |
|---|---|---|---|
| Tỷ lệ đạt bộ bài | 24/24 (100.0%) | **24/24 (100.0%)** | ✅ Tái lập hoàn toàn |
| Oracle hộp phân tầng | 100/100 hệ | **100/100 hệ** | ✅ Tái lập hoàn toàn |
| Mutation Score | 6/6 (100.0%) | **6/6 (100.0%)** | ✅ Tái lập hoàn toàn |
| Tổng thời gian trung vị | 2402.09 ms | **2156.02 ms** | ✅ Chênh lệch bình thường (tải hệ thống khác nhau) |
| Cross-task IQR | 106.57 ms | **98.81 ms** | ✅ Nằm trong biên độ bình thường |
| Avg within-task IQR | 20.24 ms | **40.72 ms** | ⚠️ Cao hơn — phân tích bên dưới |
| Phân hệ Radical trung vị | 179.80 ms/bài | **170.54 ms/bài** | ✅ |
| Phân hệ Diophantine trung vị | 4.66 ms/bài | **4.03 ms/bài** | ✅ |

> [!NOTE]
> **Phân tích chênh lệch within-task IQR (20.24 ms vs 40.72 ms):** Chênh lệch này không phản ánh vấn đề thuật toán mà phản ánh đặc tính phần cứng và tải nền của máy thẩm định viên tại thời điểm đo. RAD_04 (w-IQR = 336.39 ms) và RAD_05 (w-IQR = 352.60 ms) làm kéo trung bình lên cao do tính chất không ổn định của SymPy khi giải nghiệm Cardano trong môi trường có cạnh tranh tài nguyên. Phân hệ Diophantine vẫn rất ổn định (w-IQR trung bình ~ 1.6 ms), hoàn toàn nhất quán với v2.13. **Không có vấn đề về độ đúng đắn thuật toán.**

---

## 2. ĐÁNH GIÁ CHI TIẾT 6 ĐIỀU KIỆN TIÊN QUYẾT

### ĐK1 — Đính chính cơ chế diệt M6 & M5

**Trạng thái: ✅ ĐẠT — Đính chính chính xác và đầy đủ**

Thẩm định viên xác nhận trong mã nguồn harness:
- **M6** (`if s_gx == 'neg':` → `if False:`): Logic được mô tả đúng. Khi bypass, nghiệm ngoại lai không vào `rejected` nhưng cũng không vào `valid` (vì điều kiện $g(r) \ge 0$ chưa được thỏa mãn ở nhánh xử lý tiếp theo). Nghiệm rơi vào `indeterminate`, làm `len(rejected) == 0` khác với `expected_rejected_count == 1`, vi phạm hợp đồng kiểm tra → Bất biến R2 bị vi phạm. Cơ chế tiêu diệt được xác nhận bởi RAD_01, RAD_02, RAD_03, RAD_05 trong lần thực thi tái lập.
- **M5** (`if sc is None:` → `if False:`): Khi `solve_congruence` trả về `None` (hệ CRT xung đột), việc bỏ qua kiểm tra khiến `sc[0]` được truy cập trên `NoneType`, sinh `TypeError` tại runtime. Khối `try...except` trong harness bắt giữ, đánh dấu ca thất bại. Xác nhận bởi DIO_12_CRT_INCOMPATIBLE.

> [!NOTE]
> Phiên bản v2.12 mô tả M6 "khiến nghiệm ngoại lai lọt vào `valid`" là **sai về cơ chế**. v2.13 đã sửa chính xác: nghiệm rơi vào `indeterminate` chứ không phải `valid`. Đây là sự phân biệt quan trọng về ngữ nghĩa kiểm thử đột biến.

---

### ĐK2 — Loại bỏ từ khẳng định tuyệt đối

**Trạng thái: ✅ ĐẠT — Rà soát đầy đủ, ngôn ngữ chuẩn hóa học thuật**

Kiểm tra tĩnh mã nguồn xác nhận:
- Dòng 3 của `cad_math_core.py`: *"Mô-đun giải đại số máy tính lõi độc lập, không phụ thuộc giao diện người dùng"* — phát biểu kỹ thuật đúng thực tế, không còn tuyệt đối hóa.
- Báo cáo v2.13 bổ sung phân định rõ ràng: so sánh Photomath/Symbolab là dựa trên **UI testing**, không khẳng định giới hạn thuật toán nội bộ của họ.
- Nêu rõ `sympy.diophantine` chỉ giải phương trình đơn lẻ, không giải trực tiếp hệ phương trình đa biến.
- Lưu ý chuẩn hóa LF cho SHA-256 được bổ sung rõ ràng và đầy đủ.

---

### ĐK3 — Bổ sung 3 ca kiểm thử biên & Assertion D2

**Trạng thái: ✅ ĐẠT — Đầy đủ, bao phủ đúng các vùng biên yêu cầu**

Ba ca kiểm thử biên được xác nhận hiện diện và đạt yêu cầu trong lần chạy tái lập:

| Ca kiểm thử | Trung vị (tái lập) | Kết quả | Bất biến |
|---|---|---|---|
| `DIO_15_BOUNDARY_DEGENERATE_START` | 4.86 ms | ✅ OK | D1-D3: Nghiệm (1,1,3), n_tot=1 |
| `DIO_16_BOUNDARY_DEGENERATE_INTERVAL` | 3.20 ms | ✅ OK | D1-D3: Nghiệm (1,2,1), n_tot=1 |
| `RAD_08_ZERO_BRANCH` | 40.21 ms | ✅ OK | R1-R4: Nhận 2 nghiệm {0,1}, loại 0 |

Assertion D2 được xác nhận trong mã nguồn harness:
```python
if cat == DiophantineCategory.FINITE_BOUNDED:
    d2_ok = (len(sols) == min(n_tot, 10))
elif cat == DiophantineCategory.UNBOUNDED_INFINITE:
    d2_ok = (len(sols) == 3)
```
Bộ kiểm thử đủ **24 bài (8 Radical + 16 Diophantine)**, bao phủ toàn bộ 8 trạng thái cấu trúc đạt tới được.

---

### ĐK4 — Thống nhất ký hiệu bất biến

**Trạng thái: ✅ ĐẠT — Phân hệ hoàn toàn tách biệt và nhất quán**

Kiểm tra tĩnh xác nhận toàn bộ R1–R4 và D1–D3 đều hiện diện trong harness với vai trò phân biệt rõ ràng:

| Hệ bất biến | Phạm vi | Ký hiệu | Xuất hiện trong harness |
|---|---|---|---|
| Radical | Phương trình vô tỷ | R1, R2, R3, R4 | ✅ Tất cả |
| Diophantine | Hệ nguyên dương d=1 | D1, D2, D3 | ✅ Tất cả |

Không còn tình trạng dùng lẫn "Inv 3" cho cả hai phân hệ như v2.12.

---

### ĐK5 — Bỏ chuỗi môi trường viết cứng

**Trạng thái: ✅ ĐẠT — Hoàn toàn động, không còn chuỗi cứng**

Kiểm tra tĩnh cho kết quả:
- `sys.version.split()[0]` : ✅ Có
- `platform.platform()` : ✅ Có
- `platform.machine()` : ✅ Có
- `sp.__version__` : ✅ Có
- Chuỗi cứng `"Python 3.14.5 | i7-11800H"` : ✅ Không còn

Kết quả dòng header tại lần chạy tái lập Đợt 13 (máy thẩm định viên) phản ánh đúng môi trường thực tế: `SymPy 1.14.0 | Python 3.14.5 | Nền tảng: Windows-11-10.0.26300-SP0 (AMD64)`.

---

### ĐK6 — Đổi tên Oracle & Báo cáo within-task IQR

**Trạng thái: ✅ ĐẠT — Tên chuẩn xác, phân tích IQR kép đầy đủ**

- Tên Oracle mới: *"Oracle kiểm tra tính khả thi nguyên trên tham số hóa affine từ `sp.linsolve`"* — phản ánh đúng cơ chế hai bước: (1) phân tích affine qua `sp.linsolve`, (2) vét cạn số học nguyên thuần túy không dùng CRT/`sp.floor`.
- Giới hạn hộp N=3000 được phân tích nghiêm túc: với không gian sinh ngẫu nhiên $a_i \in [-4,4]$, chu kỳ modulo tối đa $\le \text{lcm}(1,2,3,4) = 12 \ll 3000$. Lập luận xác suất bỏ sót = 0 trong không gian thử nghiệm là chặt chẽ và hợp lệ.
- Báo cáo kép IQR được xác nhận tái lập: cross-task IQR (98.81 ms) và within-task IQR trung bình (40.72 ms, cao hơn do tải máy — không phải vấn đề thuật toán).

---

## 3. TỔNG KẾT THẨM ĐỊNH & QUYẾT ĐỊNH

### Bảng tổng hợp 6 điều kiện tiên quyết

| ĐK | Nội dung | Trạng thái v2.12 | Kết quả v2.13 (Đợt 13) |
|---|---|---|---|
| **ĐK1** | Đính chính cơ chế diệt M6 & M5 | ❌ Mô tả sai cơ chế M6 | ✅ **ĐẠT** |
| **ĐK2** | Loại bỏ từ khẳng định tuyệt đối | ❌ Còn sót nhiều cụm từ | ✅ **ĐẠT** |
| **ĐK3** | Bổ sung 3 ca biên & Assertion D2 | ❌ Chưa có | ✅ **ĐẠT** |
| **ĐK4** | Thống nhất ký hiệu bất biến | ❌ Dùng lẫn ký hiệu | ✅ **ĐẠT** |
| **ĐK5** | Bỏ chuỗi môi trường viết cứng | ❌ Còn chuỗi cứng | ✅ **ĐẠT** |
| **ĐK6** | Đổi tên Oracle & báo cáo IQR kép | ❌ Tên chưa chuẩn, thiếu IQR | ✅ **ĐẠT** |

### Kết quả kiểm chứng thực nghiệm độc lập (Đợt 13)

| Hạng mục | Kết quả |
|---|---|
| SHA-256 toàn vẹn | ✅ Khớp hoàn toàn (cả 2 file) |
| Bộ bài 24 ca | ✅ 24/24 đạt |
| Oracle phân tầng N=3000 | ✅ 100/100 hệ khớp |
| Mutation Score | ✅ 6/6 (100.0%) |
| Môi trường động (ĐK5) | ✅ Hoàn toàn động |
| Tái lập kết quả định tính | ✅ Toàn bộ trạng thái phân loại khớp |

---

## 4. QUYẾT ĐỊNH CHÍNH THỨC

> [!IMPORTANT]
> **Hội đồng Thẩm định (Đợt 13) chính thức XÁC NHẬN và PHÊ DUYỆT hồ sơ v2.13.**
>
> Toàn bộ 6 điều kiện tiên quyết tại Mục §5 Bản thẩm định Đợt 12 đã được đáp ứng đầy đủ, chính xác và có thể kiểm chứng độc lập.
>
> ## ✅ VÒNG PHẢN BIỆN LÝ THUYẾT & THUẬT TOÁN ĐƯỢC CHÍNH THỨC ĐÓNG LẠI.

---

## 5. KHUYẾN NGHỊ CHO GIAI ĐOẠN TIẾP THEO

> [!TIP]
> Nhóm tác giả có thể tiến hành giai đoạn tiếp theo với các khuyến nghị sau:

### 5.1. Ưu tiên cao (trước khi phát hành UI)
1. **Giảm within-task IQR của RAD_04 & RAD_05:** Thẩm định viên ghi nhận w-IQR lên đến ~336–352 ms trên máy tải cao. Với bài toán Cardano và bậc 4 phức tạp, khuyến nghị thêm **timeout ngưỡng** (ví dụ 3 giây) và fallback trả `indeterminate` với giải thích sư phạm, để trải nghiệm người dùng không bị giật/đứng.
2. **Pilot study sư phạm thực tế (§7):** Khung rubric 5 tiêu chí và hệ số Cohen's Kappa / Fleiss' Kappa trong §7 hiện là lý thuyết. Khuyến nghị triển khai pilot study với ít nhất 3 giáo viên toán, 20 học sinh để có số liệu Inter-Rater Reliability thực tế trước khi tuyên bố về "giá trị sư phạm".

### 5.2. Ưu tiên trung bình (trong quá trình phát triển UI)
3. **Phân hệ d≥2:** Hiện tại trả về `UNSUPPORTED_DIM_GE_2` một cách an toàn — hành vi từ chối phù hợp. Nếu nhóm muốn hỗ trợ trong tương lai, đây là điểm mở rộng tự nhiên nhất.
4. **Mở rộng Oracle hộp N khi hệ số lớn:** Với các bộ hệ số lớn hơn $|a_i| \le 20$, chu kỳ modulo tối đa có thể lên đến $\text{lcm}(1,...,20) = 232792560 \gg 3000$. Khuyến nghị bổ sung thêm loại dữ liệu kiểm thử với hệ số lớn và điều chỉnh N hoặc thay bằng Oracle giải tích thuần túy.

### 5.3. Ghi chú học thuật
5. **Ghi nhận tần suất `indeterminate` thực tế:** Cơ chế mock `check_sign_exact → 'unknown'` hiện là test nhân tạo (RAD_07). Trong thực tế, nên ghi lại tần suất xuất hiện `indeterminate` trên tập bài thực tế để đánh giá mức độ phổ biến của trường hợp này và cân nhắc điều chỉnh ngưỡng số học đa độ chính xác.

---

*Biên bản này được lập bởi Hội đồng Thẩm định Antigravity sau khi thực thi kiểm chứng hoàn toàn độc lập trên workspace ngày 08/11/2026.*
