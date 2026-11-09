# -*- coding: utf-8 -*-
"""
Script cập nhật Phiên bản 2.7 vào cad_math_v2/cad_math_v2.py
Giải quyết toàn diện 9 điểm góp ý từ phản biện đợt 7 của Claude.
"""

def patch_cad_math_v2():
    path = "cad_math_v2/cad_math_v2.py"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    p_start = text.find("    def solve_radical_pedagogical(self, target_eq, x):")
    p_end = text.find("    def plot_diophantine_system(self, sol_tuple,")
    if p_start == -1 or p_end == -1:
        print("Boundary error in patch.")
        return False

    NEW_CODE = '''    def solve_radical_pedagogical(self, target_eq, x):
        """
        Giải phương trình vô tỷ dạng √(f(x)) = g(x) với kiểm tra tính thực chuẩn xác (real_status),
        xác định dấu đại số chính xác, xử lý D_sign khi g hằng số, rút gọn nghiệm Cardano và kết luận tường minh.
        Trả về: (steps, valid_sols, rejected_sols, indeterminate_sols)
        """
        steps = []
        rads = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
        if len(rads) != 1:
            return ["  • Ngoài phạm vi hỗ trợ: Hệ thống hiện tại chuyên biệt cho phương trình chứa đúng 1 căn thức."], [], [], []

        rad = rads[0]
        expanded = sp.expand(target_eq)
        c = expanded.coeff(rad)
        rest = sp.expand(expanded - c * rad)

        if c == 0 or c.free_symbols or any(t.exp == sp.Rational(1, 2) for t in rest.atoms(sp.Pow)):
            return ["  • Ngoài phạm vi hỗ trợ: Dạng căn thức phi tuyến hoặc không cô lập được."], [], [], []

        # Chuẩn hóa về dạng chính tắc: √f = gx với hệ số căn = 1
        gx = sp.simplify(-rest / c)
        fx = rad.base

        steps.append("\\n[BƯỚC 1: XÁC ĐỊNH ĐIỀU KIỆN CÓ NGHĨA & ĐIỀU KIỆN VẾ PHẢI]")
        steps.append(f"  • Đưa phương trình về dạng chuẩn tắc: √({clean_display_expr(fx)}) = {clean_display_expr(gx)}")

        # 1. Điều kiện xác định căn thức f(x) >= 0
        if not fx.free_symbols:
            try:
                f_const = float(fx.evalf())
                if f_const >= 0:
                    steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0 (Luôn thỏa mãn với mọi x ∈ ℝ).")
                else:
                    steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0 (Không tồn tại x thỏa mãn).")
            except Exception:
                steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
        else:
            steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
            try:
                cond_fx = sp.solve(fx >= 0, x)
                steps.append(f"    ==> Miền D_rad: {cond_fx}")
            except Exception:
                pass

        # 2. Điều kiện vế phải g(x) >= 0 (xử lý riêng khi gx là hằng số)
        if not gx.free_symbols:
            try:
                g_const = float(gx.evalf())
                if g_const >= 0:
                    steps.append(f"  • Điều kiện vế phải (g(x) = {clean_display_expr(gx)} >= 0): Luôn thỏa mãn với mọi x ∈ ℝ.")
                else:
                    steps.append(f"  • Điều kiện vế phải (g(x) = {clean_display_expr(gx)} < 0): Không tồn tại x thỏa mãn.")
            except Exception:
                steps.append(f"  • Điều kiện vế phải: {clean_display_expr(gx)} >= 0")
        else:
            steps.append(f"  • Điều kiện vế phải (Vì căn bậc hai số học √({clean_display_expr(fx)}) >= 0 nên vế phải bắt buộc g(x) >= 0): {clean_display_expr(gx)} >= 0")
            try:
                cond_gx = sp.solve(gx >= 0, x)
                steps.append(f"    ==> Miền D_sign: {cond_gx}")
            except Exception:
                pass

        steps.append("\\n[BƯỚC 2: BÌNH PHƯƠNG HAI VẾ TÌM TẬP NGHIỆM ĐẠI SỐ SƠ BỘ]")
        steps.append(f"  • ({clean_display_expr(rad)})² = ({clean_display_expr(gx)})²")
        poly_eq = sp.simplify(fx - gx**2)
        steps.append(f"  <=> {clean_display_expr(poly_eq)} = 0")

        raw_sols = sp.solve(poly_eq, x)
        steps.append(f"  • Nghiệm đại số sơ bộ từ phương trình hệ quả: {raw_sols}")

        steps.append("\\n[BƯỚC 3: XÁC ĐỊNH DẤU ĐẠI SỐ CHÍNH XÁC & LOẠI BỎ NGHIỆM NGOẠI LAI]")
        valid_sols = []
        rejected_sols = []
        indeterminate_sols = []

        def real_status(r):
            \"\"\"Xác định nghiệm là thực (True), phức (False) hay chưa kết luận (None).\"\"\"
            if r.is_real is True:
                return True
            if r.is_real is False:
                return False
            try:
                a = sp.N(r, 60)
                im = abs(sp.im(a))
                if im < sp.Float('1e-45'):
                    return True
                if im > sp.Float('1e-20'):
                    return False
            except Exception:
                pass
            return None

        def check_sign_exact(expr_sub):
            expr_s = sp.simplify(expr_sub)
            if expr_s.is_real is False:
                return 'nonreal'
            if expr_s.is_zero:
                return 'zero'
            if expr_s.is_positive:
                return 'pos'
            if expr_s.is_negative:
                return 'neg'
            try:
                s = sp.sign(expr_s)
                if s.is_number:
                    if float(s) > 0: return 'pos'
                    elif float(s) < 0: return 'neg'
                    else: return 'zero'
            except Exception:
                pass
            try:
                val = float(sp.N(expr_s, 40))
                if abs(val) > 1e-30:
                    return 'pos' if val > 0 else 'neg'
            except Exception:
                pass
            return 'unknown'

        for r in raw_sols:
            st = real_status(r)
            if st is False:
                rejected_sols.append((r, "nghiệm phức"))
                r_disp = clean_display_expr(r)
                try:
                    c_val = complex(sp.N(r, 10))
                    im_str = f"- {abs(c_val.imag):.4f}i" if c_val.imag < 0 else f"+ {c_val.imag:.4f}i"
                    r_disp = f"≈ {c_val.real:.4f} {im_str}"
                except Exception:
                    pass
                steps.append(f"  • x {r_disp}: LOẠI (Nghiệm phức không thuộc tập số thực ℝ).")
                continue
            elif st is None:
                indeterminate_sols.append((r, "chưa xác định tính thực"))
                steps.append(f"  • x = {clean_display_expr(r)}: CHƯA XÁC ĐỊNH (Không đủ căn cứ chứng minh tính thực).")
                continue

            g_val = gx.subs(x, r)
            f_val = fx.subs(x, r)
            g_sign = check_sign_exact(g_val)
            f_sign = check_sign_exact(f_val)

            # Rút gọn hiển thị nghiệm Cardano nếu quá dài
            r_disp = clean_display_expr(r)
            if len(r_disp) > 40 or 'I' in str(r):
                try:
                    r_disp = f"≈ {float(sp.re(sp.N(r, 10))):.4f}"
                except Exception:
                    r_disp = f"= {clean_display_expr(r)}"
            else:
                r_disp = f"= {clean_display_expr(r)}"

            g_disp = f"g({r_disp.replace('=', '').strip()}) = {clean_display_expr(g_val)}"
            try:
                g_disp += f" ≈ {float(sp.N(g_val, 10)):.4f}"
            except Exception:
                pass

            if g_sign in ['pos', 'zero'] and f_sign in ['pos', 'zero']:
                valid_sols.append(r)
                steps.append(f"  • x {r_disp}: NHẬN (Thỏa mãn {g_disp} >= 0).")
            elif g_sign == 'neg' or f_sign == 'neg':
                rejected_sols.append((r, "g(r) < 0" if g_sign == 'neg' else "f(r) < 0"))
                reason = f"vi phạm điều kiện vế phải {g_disp} < 0 (bẫy bình phương hai vế)" if g_sign == 'neg' else "vi phạm điều kiện căn thức"
                steps.append(f"  • x {r_disp}: LOẠI (Nghiệm ngoại lai do {reason}).")
            else:
                indeterminate_sols.append((r, f"g:{g_sign}, f:{f_sign}"))
                steps.append(f"  • x {r_disp}: CHƯA XÁC ĐỊNH (Dấu biểu thức tiệm cận ngưỡng bất định, không tự động nhận nghiệm).")

        steps.append("\\n[BƯỚC 4: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
        if indeterminate_sols:
            steps.append(f"  ==> CHƯA THỂ KẾT LUẬN TẬP NGHIỆM ĐẦY ĐỦ:")
            if valid_sols:
                s_str = ", ".join(clean_display_expr(s) for s in valid_sols)
                steps.append(f"      - Các nghiệm đã xác nhận hợp lệ: {{{s_str}}}")
            steps.append(f"      - Có {len(indeterminate_sols)} nghiệm chưa thể chứng minh dấu đại số chắc chắn (cần thẩm định chuyên sâu).")
        elif valid_sols:
            def root_disp(s):
                try:
                    s_str = clean_display_expr(s)
                    if len(s_str) > 40 or 'I' in str(s):
                        return f"≈ {float(sp.re(sp.N(s, 10))):.4f}"
                    return s_str
                except Exception:
                    return str(s)
            s_str = ", ".join(root_disp(s) for s in valid_sols)
            steps.append(f"  ==> Tập nghiệm chính thức: S = {{{s_str}}}")
        else:
            steps.append("  ==> Phương trình vô nghiệm trên tập số thực ℝ (S = ∅).")

        if rejected_sols:
            steps.append(f"  • Tổng số nghiệm ngoại lai bị loại bỏ: {len(rejected_sols)} nghiệm.")

        return steps, valid_sols, rejected_sols, indeterminate_sols

    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):
        """Bộ giải Diophantine tuyến tính tổng quát với phân tích đồng dư solve_congruence và chốt an toàn thế ngược."""
        from sympy.ntheory.modular import solve_congruence
        out = []
        out.append("=" * 85)
        out.append("QUY TRÌNH GIẢI HỆ PHƯƠNG TRÌNH VÔ ĐỊNH & KHẢO SÁT NGHIỆM NGUYÊN (DIOPHANTINE SYSTEM):")
        out.append("=" * 85)

        m = len(eq_syms)
        n = len(vars_sorted)
        var_names_str = ", ".join(s.name for s in vars_sorted)

        # BƯỚC 1: PHÂN TÍCH CẤU TRÚC ĐẠI SỐ TUYẾN TÍNH
        out.append("\\n[BƯỚC 1: PHÂN TÍCH CẤU TRÚC ĐẠI SỐ TUYẾN TÍNH]")
        out.append(f"  • Số lượng phương trình: M = {m}")
        out.append(f"  • Số lượng biến số: N = {n} ({var_names_str})")

        linsols = sp.linsolve(eq_syms, vars_sorted)
        if not linsols:
            out.append("  • Hệ phương trình vô nghiệm trên tập số thực ℝ (rank(A) != rank(A|b)).")
            self.eq_result_canvas.render_latex(r"\\text{Hệ vô nghiệm trên } \\mathbb{R}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return

        sol_tuple = list(linsols)[0]
        free_syms = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)
        d = len(free_syms)
        out.append(f"  • Bậc tự do của hệ: d = N - rank(A) = {d} tham số tự do.")

        # Xử lý d = 0 (Hệ xác định, nghiệm duy nhất)
        if d == 0:
            out.append("\\n[BƯỚC 2: KHẢO SÁT NGHIỆM DUY NHẤT (d = 0)]")
            is_pos_int = all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in sol_tuple)
            sol_str = ", ".join(f"{v.name} = {c}" for v, c in zip(vars_sorted, sol_tuple))
            if is_pos_int:
                out.append(f"  ==> Hệ có nghiệm nguyên dương duy nhất: ({sol_str})")
                self.eq_result_canvas.render_latex(r"\\text{Nghiệm nguyên duy nhất } (" + var_names_str + r") = (" + ", ".join(str(c) for c in sol_tuple) + r")")
            else:
                out.append(f"  ==> Hệ có nghiệm thực duy nhất ({sol_str}) nhưng không thuộc tập số nguyên dương (ℤ⁺)ⁿ.")
                self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return

        # Xử lý d >= 2 (Đa tham số, thông báo phạm vi an toàn)
        if d >= 2:
            out.append(f"\\n[BƯỚC 2: HỌ NGHIỆM TỔNG QUÁT ĐA THAM SỐ (d = {d} >= 2)]")
            out.append(f"  • Hệ có {d} tham số tự do ({', '.join(s.name for s in free_syms)}) trên ℝ.")
            out.append("  • Biểu diễn affine nghiệm tổng quát trên ℝ:")
            for v, expr in zip(vars_sorted, sol_tuple):
                out.append(f"    {v} = {clean_display_expr(expr)}")
            out.append("  • Lưu ý sư phạm: Lớp bài toán Diophantine đa tham số (d >= 2) hiện chưa quét tự động trên tập số nguyên dương (ℤ⁺)ⁿ.")
            self.eq_result_canvas.render_latex(r"\\text{Họ nghiệm trên } \\mathbb{R} \\text{ phụ thuộc } " + str(d) + r" \\text{ tham số (chưa xét trên } \\mathbb{Z}^+ \\text{)}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return

        # TRƯỜNG HỢP d = 1: Phân tích đồng dư solve_congruence và các trạng thái cấu trúc
        param = free_syms[0]
        out.append(f"\\n[BƯỚC 2: BIỂU DIỄN THAM SỐ AFFINE THEO ẨN TỰ DO {param}]")
        for v, expr in zip(vars_sorted, sol_tuple):
            if expr == v:
                out.append(f"  • Tham số tự do: {v} ∈ ℝ")
            else:
                out.append(f"  • Biến phụ thuộc {v}: {v} = {clean_display_expr(expr)}")

        out.append("\\n[BƯỚC 3: PHÂN TÍCH HỆ ĐỒNG DƯ VÀ RÀNG BUỘC BIÊN (ℤ⁺)]")
        lo = sp.Integer(1)
        hi = None
        infeasible_constant = False
        congruences = []
        no_integer_point = False

        for v, expr in zip(vars_sorted, sol_tuple):
            e_exp = sp.expand(expr)
            a_sym = sp.Rational(e_exp.coeff(param))
            b_sym = sp.Rational(e_exp.subs(param, 0))
            out.append(f"  • {v} > 0  <=>  {clean_display_expr(expr)} > 0")

            if a_sym > 0:
                bd = sp.floor(-b_sym / a_sym) + 1
                lo = bd if lo is None else max(lo, bd)
            elif a_sym < 0:
                bd = sp.ceiling(-b_sym / a_sym) - 1
                hi = bd if hi is None else min(hi, bd)
            else:
                if b_sym <= 0:
                    infeasible_constant = True

            D_val = sp.ilcm(a_sym.q, b_sym.q)
            A_val = int(a_sym * D_val)
            B_val = int(b_sym * D_val)
            g_val = sp.igcd(A_val, D_val)
            if (-B_val) % g_val != 0:
                no_integer_point = True
            elif A_val != 0:
                Ag = A_val // g_val
                Dg = D_val // g_val
                rem = (-(B_val // g_val) * pow(Ag, -1, Dg)) % Dg if Dg > 1 else 0
                congruences.append((rem, Dg))

        int_sols = []
        category = "UNKNOWN"
        n_total = 0

        if infeasible_constant or (hi is not None and lo > hi):
            category = "INFEASIBLE_BOUNDS_EMPTY"
            out.append("\\n  ==> KẾT QUẢ: Miền ràng buộc rỗng (Hệ bất phương trình biên vô nghiệm).")
        elif no_integer_point:
            category = "INFEASIBLE_NO_INTEGER_POINTS"
            out.append("\\n  ==> KẾT QUẢ: Hệ đồng dư vô nghiệm trên ℤ (Hệ có nghiệm thực dương nhưng không có điểm nguyên).")
        else:
            sc = solve_congruence(*congruences) if congruences else (0, 1)
            if sc is None:
                category = "INFEASIBLE_NO_INTEGER_POINTS"
                out.append("\\n  ==> KẾT QUẢ: Hệ đồng dư vô nghiệm trên ℤ (Không thỏa mãn hệ đồng dư CRT).")
            else:
                p_res, m_mod = int(sc[0]), int(sc[1])
                k_start = int(sp.ceiling((lo - p_res) / m_mod))
                start_val = p_res + k_start * m_mod

                if hi is not None:
                    if start_val > hi:
                        category = "INFEASIBLE_NO_INTEGER_POINTS"
                        out.append(f"\\n  ==> KẾT QUẢ: Không có điểm nguyên nào thỏa mãn đồng dư trong miền bị chặn [{lo}, {hi}].")
                    else:
                        category = "FINITE_BOUNDED"
                        out.append(f"\\n  ==> KẾT QUẢ: Miền nghiệm hữu hạn bị chặn ({param} ∈ [{lo}, {hi}]).")
                        out.append(f"      Điều kiện đồng dư nghiệm nguyên: {param} ≡ {p_res} (mod {m_mod}).")
                        n_total = int((hi - start_val) // m_mod + 1)
                        cap = 1000

                        for k_idx in range(min(n_total, cap)):
                            pval = start_val + k_idx * m_mod
                            cand = [item.subs(param, pval) for item in sol_tuple]
                            if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                                sub_dict = {vr: c_val for vr, c_val in zip(vars_sorted, cand)}
                                if all(sp.simplify(eq_orig.subs(sub_dict)) == 0 for eq_orig in eq_syms):
                                    int_sols.append(tuple(int(c) for c in cand))

                        if n_total <= 10:
                            out.append(f"  ==> Liệt kê toàn bộ {len(int_sols)} bộ nghiệm nguyên dương:")
                        else:
                            out.append(f"  ==> Hệ có tổng cộng {n_total} bộ nghiệm nguyên dương. Hiển thị 10 bộ nghiệm đầu tiên (do giới hạn hiển thị):")

                        for idx, sol in enumerate(int_sols[:10], 1):
                            sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                            out.append(f"    • Bộ nghiệm {idx}: {sol_str}")
                        if n_total > 10:
                            out.append(f"    ... [còn {n_total - 10} bộ nghiệm tiếp theo]")
                else:
                    category = "UNBOUNDED_INFINITE"
                    out.append(f"\\n  ==> KẾT QUẢ: Miền nghiệm vô hạn không bị chặn trên ({param} >= {lo}).")
                    out.append(f"      Họ nghiệm nguyên dương theo tham số: {param} = {start_val} + {m_mod}·k (với k ∈ ℤ, k >= 0).")

                    for k_idx in range(3):
                        pval = start_val + k_idx * m_mod
                        cand = [item.subs(param, pval) for item in sol_tuple]
                        if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                            sub_dict = {vr: c_val for vr, c_val in zip(vars_sorted, cand)}
                            if all(sp.simplify(eq_orig.subs(sub_dict)) == 0 for eq_orig in eq_syms):
                                int_sols.append(tuple(int(c) for c in cand))

                    out.append(f"  ==> Hệ có vô số bộ nghiệm nguyên dương. Ba bộ nghiệm nhỏ nhất đại diện:")
                    for idx, sol in enumerate(int_sols, 1):
                        sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                        out.append(f"    • Bộ nghiệm {idx}: {sol_str}")

        # BƯỚC 4: KẾT LUẬN
        out.append("\\n[BƯỚC 4: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
        if category == "FINITE_BOUNDED" and int_sols:
            if n_total > 10:
                latex_str = r"\\text{Có } " + str(n_total) + r" \\text{ nghiệm nguyên dương}"
                out.append(f"  ==> Hệ có tổng cộng {n_total} bộ nghiệm nguyên dương (đã hiển thị 10 nghiệm đầu tiên).")
                self.eq_result_canvas.render_latex(latex_str)
            else:
                latex_cases = [r"(" + ", ".join(str(val) for val in sol) + r")" for sol in int_sols]
                latex_str = r"\\text{Nghiệm nguyên } (" + var_names_str + r") \\in \\{" + ", ".join(latex_cases) + r"\\}"
                out.append(f"  ==> Tập nghiệm nguyên dương hữu hạn: S_(ℤ⁺) = {{ " + "; ".join(latex_cases) + " }")
                self.eq_result_canvas.render_latex(latex_str)
        elif category == "UNBOUNDED_INFINITE":
            latex_str = r"\\text{Vô số nghiệm nguyên dương } (x_i \\in \\mathbb{Z}^+)"
            out.append("  ==> Hệ có vô số nghiệm nguyên dương phụ thuộc tham số không bị chặn.")
            self.eq_result_canvas.render_latex(latex_str)
        else:
            self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
            out.append("  ==> Hệ không có nghiệm nguyên dương (S_(ℤ⁺) = ∅).")

        self.eq_result_box.insert(tk.END, "\\n".join(out))
'''

    text = text[:p_start] + NEW_CODE + text[p_end:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Version 2.7 code applied successfully.")
    return True

if __name__ == "__main__":
    patch_cad_math_v2()
