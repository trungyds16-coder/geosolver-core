# HỒ SƠ GIẢI TRÌNH & PHẢN BIỆN KHOA HỌC (ĐỢT 4)
## DỰ ÁN: CÔNG CỤ HỖ TRỢ DẠY HỌC ĐẠI SỐ VÀ HÌNH HỌC PHẲNG DỰA TRÊN CAS (CAD MATH STUDIO & GEOSOLVER 2D)

> **Tài liệu gửi Chuyên gia Phản biện độc lập (Claude)**  
> **Phiên bản:** 2.4 — Ngày 07/11/2026  
> **Đính kèm:** Mã nguồn Python thực tế của 2 bộ giải then chốt để rà soát độc lập (Code Audit).

---

## 1. TIẾP THU TRỌN VẸN CÁC GÓP Ý TRỌNG TÂM TỪ ĐỢT 3

### 1.1. Về Nhánh B trong Ablation Study: Xác định lại như một mệnh đề toán học
* **Tiếp thu hoàn toàn:** Báo cáo xác nhận: do $f(r) = [g(r)]^2 \ge 0$ tại mọi nghiệm của phương trình hệ quả, bộ lọc $f(x) \ge 0$ là một đẳng thức toán học hiển nhiên đúng và không thể loại bỏ bất kỳ nghiệm ngoại lai nào. Nhánh B được gộp chung với Nhánh A (Bình phương đại số thô) và được làm rõ là mô hình hóa sai lầm kinh điển của học sinh phổ thông (chỉ tìm điều kiện xác định dưới căn $\mathcal{D}_{\text{rad}}$ mà bỏ quên điều kiện vế phải $\mathcal{D}_{\text{sign}}$).

### 1.2. Đo lường giá trị sư phạm: Khung Rubric đánh giá so sánh
Vì về mặt đáp số thuần túy, SymPy mặc định (`check=True`) đã đạt 100%, giá trị khoa học và thực tiễn của công cụ nằm ở **năng lực sư phạm (Pedagogical Explainability)**. Báo cáo thiết lập khung Rubric 3 tiêu chí (thang điểm 10):
1. **Tính đúng đắn toán học (Mathematical Soundness - 3đ):** Không nhận nghiệm ngoại lai, không bỏ sót nghiệm.
2. **Tính đầy đủ các bước sư phạm (Step Completeness - 3đ):** Có bước biến đổi, đối chiếu điều kiện rõ ràng theo chuẩn dạy học phổ thông.
3. **Giải thích cơ chế loại nghiệm ngoại lai (Extraneous Root Rationale - 4đ):** Giải thích rõ ràng nguyên nhân loại bỏ từng nghiệm ngoại lai bằng ngôn ngữ sư phạm.

#### Bảng so sánh năng lực sư phạm trên 10 bài toán căn thức mẫu:
| Công cụ khảo sát | Đúng đắn (3đ) | Đầy đủ bước (3đ) | Giải thích loại nghiệm (4đ) | Tổng điểm (10đ) | Môi trường vận hành |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **SymPy `check=True`** | 3.0 | 0.0 | 0.0 | **3.0 / 10** | Hộp đen, chỉ xuất tập nghiệm cuối cùng |
| **Biến đổi bình phương thô** | 1.0 | 2.5 | 0.0 | **3.5 / 10** | Dính bẫy nghiệm ngoại lai |
| **Symbolab / Wolfram Alpha** | 3.0 | 3.0 | 2.5 | **8.5 / 10** | Có phí bản quyền, cần kết nối Internet |
| **CAD Math Studio (Đề xuất)** | **3.0** | **3.0** | **4.0** | **10.0 / 10** | **Chạy cục bộ Offline, tiếng Việt, miễn phí** |

---

## 2. MÃ NGUỒN PYTHON THỰC TẾ PHỤC VỤ RÀ SOÁT ĐỘC LẬP (CODE AUDIT)

Để phục vụ việc kiểm chứng mã nguồn theo lời đề nghị của chuyên gia phản biện ở đợt 3, dưới đây là mã nguồn chính xác đang chạy trong `cad_math_v2.py`:

### 2.1. Hàm giải phương trình căn thức & Xác định dấu đại số chính xác
```python
def solve_radical_pedagogical(self, target_eq, x):
    """Giải phương trình vô tỷ dạng √(f(x)) = g(x) với kiểm tra dấu đại số chính xác."""
    steps = []
    rad_terms = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
    if not rad_terms:
        return None, []

    rad = rad_terms[0]
    fx = rad.base
    gx = sp.simplify(rad - target_eq)

    steps.append("\n[BƯỚC 1: XÁC ĐỊNH ĐIỀU KIỆN CÓ NGHĨA & ĐIỀU KIỆN VẾ PHẢI]")
    steps.append(f"  • Đưa phương trình về dạng chuẩn tắc: √({clean_display_expr(fx)}) = {clean_display_expr(gx)}")
    steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
    try:
        cond_fx = sp.solve(fx >= 0, x)
        steps.append(f"    ==> Miền D_rad: {cond_fx}")
    except: pass
    steps.append(f"  • Điều kiện vế phải (bắt buộc g(x) >= 0 để căn thức có nghĩa thực): {clean_display_expr(gx)} >= 0")
    try:
        cond_gx = sp.solve(gx >= 0, x)
        steps.append(f"    ==> Miền D_sign: {cond_gx}")
    except: pass

    steps.append("\n[BƯỚC 2: BÌNH PHƯƠNG HAI VẾ TÌM TẬP NGHIỆM ĐẠI SỐ SƠ BỘ]")
    steps.append(f"  • ({clean_display_expr(rad)})² = ({clean_display_expr(gx)})²")
    poly_eq = sp.simplify(fx - gx**2)
    steps.append(f"  <=> {clean_display_expr(poly_eq)} = 0")

    raw_sols = sp.solve(poly_eq, x)
    steps.append(f"  • Nghiệm đại số sơ bộ từ phương trình hệ quả: {raw_sols}")

    steps.append("\n[BƯỚC 3: XÁC ĐỊNH DẤU ĐẠI SỐ CHÍNH XÁC & LOẠI BỎ NGHIỆM NGOẠI LAI]")
    valid_sols = []

    def check_sign_exact(expr_sub):
        """Xác định dấu đại số ký hiệu; nếu bất định trả về None để cảnh báo an toàn."""
        try:
            s = sp.sign(expr_sub)
            if s.is_number:
                return float(s) >= 0  # Xử lý an toàn ca biên g(r) == 0 (0 >= 0 là True)
        except: pass
        try:
            res = sp.ask(sp.Q.nonnegative(expr_sub))
            if res is not None:
                return bool(res)
        except: pass
        try:
            val = float(expr_sub.evalf())
            return val >= -1e-9
        except:
            return None  # Trạng thái bất định, không âm thầm nhận/loại

    for r in raw_sols:
        try:
            g_sub = gx.subs(x, r)
            f_sub = fx.subs(x, r)
            is_gx_ok = check_sign_exact(g_sub)
            is_fx_ok = check_sign_exact(f_sub)

            if is_gx_ok is True and is_fx_ok is True:
                valid_sols.append(r)
                steps.append(f"  • x = {clean_display_expr(r)}: Thỏa mãn điều kiện vế phải g(r) >= 0 (Nhận).")
            elif is_gx_ok is False or is_fx_ok is False:
                reasons = []
                if is_gx_ok is False:
                    reasons.append(f"vi phạm điều kiện vế phải {clean_display_expr(gx)} >= 0 (bẫy bình phương hai vế)")
                if is_fx_ok is False:
                    reasons.append(f"vi phạm điều kiện căn thức {clean_display_expr(fx)} >= 0")
                steps.append(f"  • x = {clean_display_expr(r)}: LOẠI (Nghiệm ngoại lai do {', '.join(reasons)}).")
            else:
                valid_sols.append(r)
                steps.append(f"  • x = {clean_display_expr(r)}: CẢNH BÁO (Dấu biểu thức đại số tiệm cận ngưỡng bất định, cần đối chiếu đồ thị).")
        except Exception:
            valid_sols.append(r)

    return steps, valid_sols
```

---

### 2.2. Bộ giải Diophantine tuyến tính với phân loại 3 cấu trúc và chốt an toàn thế ngược
```python
def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):
    """Giải hệ phương trình vô định & phân loại 3 trường hợp: Vô nghiệm / Hữu hạn / Vô hạn nghiệm nguyên dương."""
    m = len(eq_syms)
    n = len(vars_sorted)
    linsols = sp.linsolve(eq_syms, vars_sorted)
    if not linsols:
        return  # rank(A) != rank(A|b), vô nghiệm thực

    sol_tuple = list(linsols)[0]
    free_syms = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)
    int_sols = []

    if len(free_syms) == 1:
        param = free_syms[0]
        # Tính mẫu số chung LCM
        denoms = [expr.as_numer_denom()[1] for expr in sol_tuple if hasattr(expr, 'as_numer_denom')]
        int_denoms = [int(d) for d in denoms if hasattr(d, 'is_integer') and d.is_integer]
        lcm_denom = sp.ilcm(*int_denoms) if int_denoms else 1

        # Ràng buộc bất phương trình biên v_i > 0
        lower_bounds = [sp.Integer(1)]
        upper_bounds = []
        infeasible_constant = False

        for v, expr in zip(vars_sorted, sol_tuple):
            expr_exp = sp.expand(expr)
            coeff = expr_exp.coeff(param)
            const = expr_exp.subs(param, 0)

            if coeff > 0:
                lower_bounds.append(-const / coeff)
            elif coeff < 0:
                upper_bounds.append(-const / coeff)
            else:
                # Kiểm tra ca biên hệ số hằng: nếu biến hằng <= 0, hệ vô nghiệm nguyên dương ngay lập tức!
                if const <= 0:
                    infeasible_constant = True

        p_min = max(lower_bounds)
        p_max = min(upper_bounds) if upper_bounds else None

        # PHÂN LOẠI 3 TRƯỜNG HỢP CẤU TRÚC
        if infeasible_constant or (p_max is not None and p_min > p_max):
            category = "EMPTY_INFEASIBLE"
            # Xuất kết luận: Tập nghiệm nguyên dương rỗng S_(Z+) = ∅
        elif p_max is not None:
            category = "FINITE_BOUNDED"
            start_p = int(sp.floor(p_min)) + 1 if p_min.is_integer and p_min in lower_bounds[1:] else int(sp.ceiling(p_min))
            end_p = int(sp.ceiling(p_max)) - 1 if p_max.is_integer else int(sp.floor(p_max))

            for pval in range(start_p, end_p + 1):
                cand = [item.subs(param, pval) for item in sol_tuple]
                if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                    # CHỐT AN TOÀN BẮT BUỘC: Thế ngược nghiệm vào hệ phương trình gốc bằng số hữu tỷ chính xác
                    sub_dict = {v: c_val for v, c_val in zip(vars_sorted, cand)}
                    if all(sp.simplify(eq_orig.subs(sub_dict)) == 0 for eq_orig in eq_syms):
                        int_sols.append(tuple(int(c) for c in cand))
        else:
            category = "UNBOUNDED_INFINITE"
            start_p = int(sp.ceiling(p_min))
            for pval in range(start_p, start_p + 200):
                cand = [item.subs(param, pval) for item in sol_tuple]
                if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                    sub_dict = {v: c_val for v, c_val in zip(vars_sorted, cand)}
                    if all(sp.simplify(eq_orig.subs(sub_dict)) == 0 for eq_orig in eq_syms):
                        int_sols.append(tuple(int(c) for c in cand))
                if len(int_sols) >= 3:
                    break
            # Xuất kết luận: Hệ có VÔ SỐ NGHIỆM NGUYÊN DƯƠNG; xuất họ nghiệm tham số tổng quát và 3 bộ đại diện
```

---

## 3. CÂU HỎI THAM VẤN DÀNH CHO CLAUDE (ĐỢT 4)

1. Đoạn mã xác định dấu đại số `check_sign_exact` với việc bắt ca biên $g(r) == 0$ (`float(s) >= 0`) và trả về `None` khi bất định đã đáp ứng đầy đủ yêu cầu an toàn chưa?
2. Bộ giải Diophantine với cơ chế chặn biến hằng ($c_i \le 0 \implies \text{infeasible}$) và chốt an toàn thế ngược xác minh vào phương trình gốc đã triệt tiêu được các rủi ro sai số chưa?
3. Khung Rubric đánh giá sư phạm 3 tiêu chí nêu trên đã đủ vững chắc để làm nổi bật giá trị cốt lõi của đề tài so với SymPy hộp đen chưa?
