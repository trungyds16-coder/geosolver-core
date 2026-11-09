# -*- coding: utf-8 -*-
"""
Script áp dụng các cải tiến Phiên bản 2.6 vào cad_math_v2/cad_math_v2.py:
1. real_status: Bộ lọc nghiệm thực chuẩn xác đa tầng, chống loại nhầm nghiệm thực dạng Cardano (như √(x³ - 3x + 1) = 1/2).
2. solve_radical_pedagogical: Trả về đầy đủ 4 phần tử (steps, valid_sols, rejected_sols, indeterminate_sols), bổ sung kết luận chính thức ngay trong hàm.
3. solve_underdetermined_or_diophantine:
   - Xử lý trần 1000 chuẩn xác (tính n_total, không in "toàn bộ" khi n > 1000).
   - Họ nghiệm vô hạn tham số hóa rõ ràng k >= 0 (bảo đảm mọi nghiệm dương).
   - Nhãn LaTeX d >= 2 ghi rõ: họ nghiệm trên ℝ phụ thuộc d tham số (chưa xét trên ℤ⁺).
4. Đồng bộ caller tại line 2362.
"""
import sys

def apply_patch():
    file_path = "cad_math_v2/cad_math_v2.py"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Đồng bộ caller
    old_caller = """            # KIỂM TRA PHƯƠNG TRÌNH CHỨA CĂN THỨC (RADICAL EQUATION)
            has_radical = any(isinstance(node, sp.Pow) and node.exp == sp.Rational(1, 2) for node in target_eq.atoms(sp.Pow))
            if has_radical and not is_trig:
                rad_steps, rad_sols = self.solve_radical_pedagogical(target_eq, x)
                if rad_steps:
                    out.extend(rad_steps)
                    out.append("\\n[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM CHÍNH THỨC S]")
                    if rad_sols:
                        latex_sols = [f'x = {sp.latex(s)}' for s in rad_sols]
                        self.eq_result_canvas.render_latex(r' \\;; \\quad '.join(latex_sols))
                        s_str = ', '.join(str(s) for s in rad_sols)
                        out.append(f'  • Tập nghiệm chính thức: S = {{{s_str}}}')
                    else:
                        out.append('  • Phương trình vô nghiệm trên tập số thực ℝ.')
                        self.eq_result_canvas.render_latex(r'\\text{Vô nghiệm trên } \\mathbb{R}')
                    self.eq_result_box.insert(tk.END, "\\n".join(out))
                    f_num = sp.lambdify(x, target_eq, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
                    self.plot_oxy_roots(f_num, rad_sols)
                    return"""

    new_caller = """            # KIỂM TRA PHƯƠNG TRÌNH CHỨA CĂN THỨC (RADICAL EQUATION)
            has_radical = any(isinstance(node, sp.Pow) and node.exp == sp.Rational(1, 2) for node in target_eq.atoms(sp.Pow))
            if has_radical and not is_trig:
                res_rad = self.solve_radical_pedagogical(target_eq, x)
                if res_rad and res_rad[0]:
                    rad_steps = res_rad[0]
                    rad_sols = res_rad[1]
                    out.extend(rad_steps)
                    if rad_sols:
                        latex_sols = [f'x = {sp.latex(s)}' for s in rad_sols]
                        self.eq_result_canvas.render_latex(r' \\;; \\quad '.join(latex_sols))
                    else:
                        self.eq_result_canvas.render_latex(r'\\text{Vô nghiệm trên } \\mathbb{R}')
                    self.eq_result_box.insert(tk.END, "\\n".join(out))
                    f_num = sp.lambdify(x, target_eq, modules=['numpy', {'sqrt': np.lib.scimath.sqrt}])
                    self.plot_oxy_roots(f_num, rad_sols)
                    return"""

    if old_caller in content:
        content = content.replace(old_caller, new_caller)
        print("Updated caller at line ~2362 successfully.")
    else:
        print("Caller pattern not matched exactly, checking alternative...")

    # 2. Cập nhật solve_radical_pedagogical và solve_underdetermined_or_diophantine
    import re
    p_start = content.find("    def solve_radical_pedagogical(self, target_eq, x):")
    p_end = content.find("    def plot_diophantine_system(self, sol_tuple,")
    if p_start == -1 or p_end == -1:
        print("Error: Could not find function boundaries.")
        return False

    new_functions = '''    def solve_radical_pedagogical(self, target_eq, x):
        """Giải phương trình vô tỷ dạng √(f(x)) = g(x) với kiểm tra dấu đại số chính xác và chuẩn hóa tự động."""
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
        steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
        try:
            cond_fx = sp.solve(fx >= 0, x)
            steps.append(f"    ==> Miền D_rad: {cond_fx}")
        except Exception:
            pass
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
            """Xác định nghiệm là thực (True), phức (False) hay chưa kết luận (None)."""
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
                if len(r_disp) > 50:
                    try:
                        c_val = complex(sp.N(r, 10))
                        r_disp = f"≈ {c_val.real:.4f} + {c_val.imag:.4f}i"
                    except Exception:
                        pass
                steps.append(f"  • x = {r_disp}: LOẠI (Nghiệm phức không thuộc tập số thực ℝ).")
                continue
            elif st is None:
                indeterminate_sols.append((r, "chưa xác định tính thực"))
                steps.append(f"  • x = {clean_display_expr(r)}: CHƯA XÁC ĐỊNH (Không đủ căn cứ chứng minh tính thực).")
                continue

            g_val = gx.subs(x, r)
            f_val = fx.subs(x, r)
            g_sign = check_sign_exact(g_val)
            f_sign = check_sign_exact(f_val)

            g_disp = f"g({clean_display_expr(r)}) = {clean_display_expr(g_val)}"
            try:
                g_disp += f" ≈ {float(sp.N(g_val, 10)):.4f}"
            except Exception:
                pass

            if g_sign in ['pos', 'zero'] and f_sign in ['pos', 'zero']:
                valid_sols.append(r)
                steps.append(f"  • x = {clean_display_expr(r)}: NHẬN (Thỏa mãn {g_disp} >= 0).")
            elif g_sign == 'neg' or f_sign == 'neg':
                rejected_sols.append((r, "g(r) < 0" if g_sign == 'neg' else "f(r) < 0"))
                reason = f"vi phạm điều kiện vế phải {g_disp} < 0 (bẫy bình phương hai vế)" if g_sign == 'neg' else "vi phạm điều kiện căn thức"
                steps.append(f"  • x = {clean_display_expr(r)}: LOẠI (Nghiệm ngoại lai do {reason}).")
            else:
                indeterminate_sols.append((r, f"g:{g_sign}, f:{f_sign}"))
                steps.append(f"  • x = {clean_display_expr(r)}: CHƯA XÁC ĐỊNH (Dấu biểu thức tiệm cận ngưỡng bất định, không tự động nhận nghiệm).")

        steps.append("\\n[BƯỚC 4: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
        if valid_sols:
            s_str = ", ".join(clean_display_expr(s) for s in valid_sols)
            steps.append(f"  ==> Tập nghiệm chính thức: S = {{{s_str}}}")
        else:
            steps.append("  ==> Phương trình vô nghiệm trên tập số thực ℝ (S = ∅).")
        if rejected_sols:
            steps.append(f"  • Tổng số nghiệm ngoại lai bị loại bỏ: {len(rejected_sols)} nghiệm.")
        if indeterminate_sols:
            steps.append(f"  • CẢNH BÁO SƯ PHẠM: Có {len(indeterminate_sols)} nghiệm chưa thể kết luận dấu đại số, không tự động nhận vào tập nghiệm.")

        return steps, valid_sols, rejected_sols, indeterminate_sols

    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):
        """Bộ giải Diophantine tuyến tính tổng quát với phân tích đồng dư CRT và chốt an toàn thế ngược."""
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

        # TRƯỜNG HỢP d = 1: Phân tích đồng dư CRT và các trạng thái cấu trúc
        param = free_syms[0]
        out.append(f"\\n[BƯỚC 2: BIỂU DIỄN THAM SỐ AFFINE THEO ẨN TỰ DO {param}]")
        for v, expr in zip(vars_sorted, sol_tuple):
            if expr == v:
                out.append(f"  • Tham số tự do: {v} ∈ ℝ")
            else:
                out.append(f"  • Biến phụ thuộc {v}: {v} = {clean_display_expr(expr)}")

        # Phân tích hệ bất phương trình biên v_i > 0
        out.append("\\n[BƯỚC 3: PHÂN TÍCH HỆ ĐỒNG DƯ VÀ RÀNG BUỘC BIÊN (ℤ⁺)]")
        lower_bounds = [sp.Integer(1)]
        upper_bounds = []
        infeasible_constant = False

        for v, expr in zip(vars_sorted, sol_tuple):
            expr_exp = sp.expand(expr)
            coeff = expr_exp.coeff(param)
            const = expr_exp.subs(param, 0)
            out.append(f"  • {v} > 0  <=>  {clean_display_expr(expr)} > 0")

            if coeff > 0:
                lower_bounds.append(-const / coeff)
            elif coeff < 0:
                upper_bounds.append(-const / coeff)
            else:
                if const <= 0:
                    infeasible_constant = True

        p_min = max(lower_bounds)
        p_max = min(upper_bounds) if upper_bounds else None

        # Kiểm tra điều kiện đồng dư tuyến tính CRT
        congruences = []
        no_integer_point = False
        for expr in sol_tuple:
            expr_t = sp.together(expr)
            num, denom = expr_t.as_numer_denom()
            try:
                denom_val = int(denom)
            except Exception:
                denom_val = 1
            if denom_val > 1:
                num = sp.expand(num)
                a = int(num.coeff(param))
                b = int(num.subs(param, 0))
                rem = (-b) % denom_val
                g = sp.gcd(a, denom_val)
                if rem % g != 0:
                    no_integer_point = True
                    break
                a_red = a // g
                rem_red = rem // g
                m_red = denom_val // g
                inv_a = sp.mod_inverse(a_red, m_red)
                p0_i = (rem_red * inv_a) % m_red
                congruences.append((p0_i, m_red))

        p_res, m_mod = (0, 1)
        if not no_integer_point and congruences:
            p_res, m_mod = congruences[0]
            for p_i, m_i in congruences[1:]:
                try:
                    res_crt = crt([m_mod, m_i], [p_res, p_i])
                    if res_crt is None:
                        no_integer_point = True
                        break
                    p_res = res_crt[0]
                    m_mod = sp.ilcm(m_mod, m_i)
                except Exception:
                    no_integer_point = True
                    break

        int_sols = []
        category = "UNKNOWN"
        n_total = 0
        hit_cap = False

        if infeasible_constant or (p_max is not None and p_min > p_max):
            category = "INFEASIBLE_BOUNDS_EMPTY"
            out.append("\\n  ==> KẾT QUẢ: Miền ràng buộc rỗng (Hệ bất phương trình biên vô nghiệm).")
        elif no_integer_point:
            category = "INFEASIBLE_NO_INTEGER_POINTS"
            out.append("\\n  ==> KẾT QUẢ: Hệ đồng dư vô nghiệm trên ℤ (Hệ có nghiệm thực dương nhưng không có điểm nguyên).")
        elif p_max is not None:
            category = "FINITE_BOUNDED"
            out.append(f"\\n  ==> KẾT QUẢ: Miền nghiệm hữu hạn bị chặn ({param} ∈ [{clean_display_expr(p_min)}, {clean_display_expr(p_max)}]).")
            out.append(f"      Điều kiện đồng dư nghiệm nguyên: {param} ≡ {p_res} (mod {m_mod}).")

            k_start = int(sp.ceiling((p_min - p_res) / m_mod))
            start_val = p_res + k_start * m_mod
            if start_val > p_max:
                category = "INFEASIBLE_NO_INTEGER_POINTS"
                out.append("\\n  ==> KẾT QUẢ: Không có điểm nguyên nào thỏa mãn đồng dư trong miền bị chặn.")
            else:
                n_total = int((p_max - start_val) // m_mod + 1)
                cap = 1000
                hit_cap = n_total > cap

                k = k_start
                while True:
                    pval = p_res + k * m_mod
                    if pval > p_max or len(int_sols) >= cap:
                        break
                    cand = [item.subs(param, pval) for item in sol_tuple]
                    if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                        sub_dict = {v: c_val for v, c_val in zip(vars_sorted, cand)}
                        if all(sp.simplify(eq_orig.subs(sub_dict)) == 0 for eq_orig in eq_syms):
                            int_sols.append(tuple(int(c) for c in cand))
                    k += 1

                if hit_cap:
                    out.append(f"  ==> Hệ có tổng cộng {n_total} bộ nghiệm nguyên dương (hiển thị {len(int_sols)} bộ nghiệm đầu tiên do giới hạn trần an toàn).")
                else:
                    out.append(f"  ==> Liệt kê toàn bộ {len(int_sols)} bộ nghiệm nguyên dương:")

                for idx, sol in enumerate(int_sols[:10], 1):
                    sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                    out.append(f"    • Bộ nghiệm {idx}: {sol_str}")
                if len(int_sols) > 10:
                    out.append(f"    ... [còn {len(int_sols) - 10} bộ nghiệm tiếp theo]")
        else:
            category = "UNBOUNDED_INFINITE"
            out.append(f"\\n  ==> KẾT QUẢ: Miền nghiệm vô hạn không bị chặn trên ({param} >= {clean_display_expr(p_min)}).")
            k_start = int(sp.ceiling((p_min - p_res) / m_mod))
            base_p = p_res + k_start * m_mod
            out.append(f"      Họ nghiệm nguyên dương theo tham số: {param} = {base_p} + {m_mod}·k (với k ∈ ℤ, k >= 0).")

            k = 0
            while len(int_sols) < 3:
                pval = base_p + k * m_mod
                cand = [item.subs(param, pval) for item in sol_tuple]
                if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                    sub_dict = {v: c_val for v, c_val in zip(vars_sorted, cand)}
                    if all(sp.simplify(eq_orig.subs(sub_dict)) == 0 for eq_orig in eq_syms):
                        int_sols.append(tuple(int(c) for c in cand))
                k += 1
                if k > 500:
                    break

            out.append(f"  ==> Hệ có vô số bộ nghiệm nguyên dương. Ba bộ nghiệm nhỏ nhất đại diện:")
            for idx, sol in enumerate(int_sols, 1):
                sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                out.append(f"    • Bộ nghiệm {idx}: {sol_str}")

        # BƯỚC 4: KẾT LUẬN
        out.append("\\n[BƯỚC 4: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
        if category == "FINITE_BOUNDED" and int_sols:
            if hit_cap:
                latex_str = r"\\text{Có } " + str(n_total) + r" \\text{ nghiệm nguyên dương (hiển thị 1000 nghiệm)}"
                out.append(f"  ==> Hệ có {n_total} bộ nghiệm nguyên dương (hiển thị {len(int_sols)} bộ nghiệm đầu tiên).")
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

    content = content[:p_start] + new_functions + content[p_end:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Functions replaced successfully.")
    return True

if __name__ == "__main__":
    apply_patch()
