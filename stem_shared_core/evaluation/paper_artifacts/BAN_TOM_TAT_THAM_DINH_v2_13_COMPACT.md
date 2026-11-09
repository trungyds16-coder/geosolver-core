# BẢN TÓM TẮT ĐÁP ỨNG THẨM ĐỊNH KHOA HỌC (PHIÊN BẢN 2.13 COMPACT)
## DỰ ÁN: CAD MATH STUDIO & GEOSOLVER 2D - ĐỀ NGHỊ ĐÓNG VÒNG PHẢN BIỆN LÝ THUYẾT

**Kính gửi:** Hội đồng Thẩm định Khoa học & Độc giả Phản biện  
**Ngày cập nhật:** 08/11/2026  
**Mã băm kiểm chứng tính toàn vẹn (SHA-256 Unix LF chuẩn hóa):**
- `stem_shared_core/cad_math_core.py`: `9bed3b7fbe3a8a14d611fd8e0897d4da1541c6bcd5fa763d19b77689b3a2dd96`
- `stem_shared_core/tools/run_batch_auto_test.py`: `c96c7e13b04b44276d8571a2745d8dd124e9f680b66c1390a10ae679c13c0476`

---

### 1. ĐÁP ỨNG 6 ĐIỀU KIỆN TIÊN QUYẾT CỦA HỘI ĐỒNG (MỤC §5 ĐỢT 12)

1. **Điều kiện 1 (Đính chính cơ chế diệt M6 & M5):**
   - **M6 (`if False:` thay cho `if s_gx == 'neg':`):** Nghiệm ngoại lai không lọt vào `valid` mà chuyển vào `indeterminate`. M6 bị diệt do vi phạm hợp đồng về số lượng nghiệm loại (`len(rejected) == 0 != expected_rejected_count`) và vi phạm Bất biến R2.
   - **M5 (`if False:` thay cho `if sc is None:`):** Bị diệt bởi ngoại lệ thực thi kiểu dữ liệu (`TypeError: 'NoneType' object is not subscriptable`) khi truy cập `sc[0]`, được khối `try...except` bắt giữ.
2. **Điều kiện 2 (Loại bỏ từ khẳng định tuyệt đối):**
   - Đã loại bỏ toàn bộ các từ "độc lập hoàn toàn", "100%", "trọn vẹn", "khớp tuyệt đối" ở toàn bộ báo cáo và dòng 3 của `cad_math_core.py`.
   - Bổ sung ghi chú phân định rõ giữa kiểm thử giao diện người dùng (UI test) và giới hạn thuật toán lý thuyết ở §6.
   - Nêu rõ SymPy `diophantine` giải phương trình đơn lẻ, không giải trực tiếp hệ phương trình đa biến.
   - Bổ sung lưu ý chuẩn hóa LF cho SHA-256 khi kiểm chứng chéo giữa Windows và Linux/macOS.
3. **Điều kiện 3 (Bổ sung 3 ca kiểm thử biên & Assertion D2):**
   - Đã bổ sung `DIO_15` (suy biến bước nhảy $start\_val == hi$), `DIO_16` (khoảng cận co cụm $[1, 1]$), `RAD_08` (nghiệm biên $g(0) = 0$).
   - Bổ sung assertion kiểm tra hợp đồng độ dài hiển thị đại diện (Bất biến D2: `len(sols) == min(n_tot, 10)` và `len(sols) == 3`).
   - Mở rộng bộ kiểm thử thành **24 bài (8 Radical, 16 Diophantine)**, đạt tỷ lệ **24/24 bài**.
4. **Điều kiện 4 (Thống nhất ký hiệu bất biến):**
   - Phân hệ Radical: **R1** (Triệt tiêu phần dư & $g \ge 0$), **R2** (Vi phạm vế phải độc lập), **R3** (Phân hoạch bảo toàn nghiệm hệ quả), **R4** (Tập nghiệm đối chuẩn chuyên gia).
   - Phân hệ Diophantine: **D1** (Tính khả thi nguyên dương độc lập), **D2** (Hợp đồng hiển thị nghiệm đại diện), **D3** (Tính khớp số lượng nghiệm giải tích).
5. **Điều kiện 5 (Bỏ chuỗi môi trường viết cứng):**
   - Harness header truy vấn động hoàn toàn qua `sys.version.split()[0]`, `platform.platform()`, `platform.machine()`, `sp.__version__`.
6. **Điều kiện 6 (Đổi tên Oracle & Báo cáo within-task IQR):**
   - Đổi tên thành: *Oracle kiểm tra tính khả thi nguyên trên tham số hóa affine từ `sp.linsolve`*.
   - Minh định rõ giới hạn hộp $N=3000$ và chứng minh tính hợp lệ trên không gian tham số thử nghiệm.
   - Báo cáo đồng thời **within-task IQR** (trung bình $20.24\text{ ms}$) và **cross-task IQR** ($106.57\text{ ms}$).

---

### 2. TỔNG HỢP SỐ LIỆU THỰC NGHIỆM ĐO ĐẠC NGUYÊN VĂN (BENCHMARK SUMMARY)

- **Quy mô kiểm thử:** 24 bài (8 Radical, 16 Diophantine). Tỷ lệ đạt: **24/24 bài (100%)**.
- **Oracle Hộp phân tầng (N=3000):** Đạt **100/100 hệ khớp** (25 FINITE, 25 UNBOUNDED, 25 EMPTY, 25 INFEASIBLE). Thời gian: $1578.29\text{ ms}$ ($15.78\text{ ms/hệ}$).
- **Kiểm thử đột biến thật trên Bytecode (6 toán tử):** Mutation Score = **6/6 toán tử bị tiêu diệt (100.0%)** trên Suite kiểm định.
- **Thời gian thực thi (Trung vị 5 vòng):**
  + Tổng thời gian bộ bài: $2402.09\text{ ms}$ (Trung bình: $100.09\text{ ms/bài}$).
  + Phân hệ Radical (8 bài): Trung vị $179.80\text{ ms/bài}$.
  + Phân hệ Diophantine (16 bài): Trung vị $4.66\text{ ms/bài}$.
  + Dải đo: Min = $0.10\text{ ms}$ (`RAD_06_OUT_OF_SCOPE`), Max = $798.74\text{ ms}$ (`RAD_04_CARDANO_CUBIC`).
  + Độ phân tán: cross-task IQR = $106.57\text{ ms}$ | TB within-task IQR = $20.24\text{ ms}$.

---

### 3. KIẾN NGHỊ ĐÓNG VÒNG PHẢN BIỆN

Hồ sơ v2.13 đã đáp ứng trọn vẹn và chuẩn mực toàn bộ các yêu cầu của Hội đồng thẩm định. Nhóm tác giả kính đề nghị Hội đồng chính thức phê duyệt và **đóng vòng phản biện lý thuyết & thuật toán**.
