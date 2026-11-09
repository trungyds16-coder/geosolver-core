# PHÁN QUYẾT ĐÓNG HỒ SƠ KIỂM TOÁN — CAD Math Studio v2.2.0-RC5 (FINAL)
## (Phản hồi Bản Trích xuất Mã nguồn Trực tiếp — Vòng 7)

**Kính gửi:** Hội đồng Kiểm toán / Independent Audit Board  
**Đối tượng thẩm định:** Bản Phản hồi Kỹ thuật & Trích xuất Mã nguồn Trực tiếp — CAD Math Studio v2.2.0-RC5  
**Căn cứ phán quyết:**  
- Nguyên văn các đoạn code lõi được yêu cầu đối soát  
- Giải trình cơ chế sideloading Windows (`LocalMachine\TrustedPeople`)  
- Định hướng phát hành Store (out of scope)  

**Trạng thái hồ sơ:** **ĐẦY ĐỦ** — Hội đồng đã có đủ bằng chứng để đóng hồ sơ kiểm toán sideload.

---

## 1. PHÁN QUYẾT

### **CLOSED — FINAL CERTIFICATION CONFIRMED (SCOPE: SIDELOAD RELEASE)**

Hồ sơ kiểm toán **CAD Math Studio v2.2.0-RC5** chính thức **được khép lại**.

Chứng nhận **FULL CERTIFICATION — SCOPE: SIDELOAD RELEASE** đã ban hành ở Vòng 6 **được giữ nguyên hiệu lực**, với các ghi nhận bổ sung từ Vòng 7.

**Không còn P1/P2 tồn đọng ở mức correctness có thể phát hiện từ bằng chứng vận hành + trích xuất mã nguồn.**

---

## 2. ĐỐI SOÁT CÁC ĐOẠN CODE ĐƯỢC YÊU CẦU

### 2.1. Hadamard tolerance & phân lập Exact (`compute_matrix_inverse`) — P1-1

```python
# Exact check trước (det == 0 hoặc simplify == 0)
if hasattr(detA, "is_zero") and detA.is_zero is True:
    is_singular = True
elif sp.simplify(detA) == 0:
    is_singular = True

# Float check CHỈ khi có sp.Float/float
has_float = any(elem.has(sp.Float) or isinstance(elem, float) for elem in A) or detA.has(sp.Float)
if not is_singular and has_float:
    hadamard_bound = 1.0
    for r_idx in range(A.rows):
        row_norm_sq = sum(float(elem.evalf())**2 for elem in A.row(r_idx))
        hadamard_bound *= math.sqrt(row_norm_sq) or 1.0
    det_val = abs(float(detA.evalf()))
    if det_val < 1e-12 * hadamard_bound:
        is_singular = True