# -*- coding: utf-8 -*-
"""
Clean, error-free replacement of solve_underdetermined_or_diophantine in cad_math_v2.py
"""

CLEAN_DIOPH = '''    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):
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
            self.last_dioph_category = "INCONSISTENT"
            self.last_dioph_solutions = []
            self.last_dioph_n_total = 0
            return "INCONSISTENT", [], 0, out

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
                self.eq_result_box.insert(tk.END, "\\n".join(out))
                self.last_dioph_category = "UNIQUE"
                self.last_dioph_solutions = [tuple(int(c) for c in sol_tuple)]
                self.last_dioph_n_total = 1
                return "UNIQUE", [tuple(int(c) for c in sol_tuple)], 1, out
            else:
                out.append(f"  ==> Hệ có nghiệm thực duy nhất ({sol_str}) nhưng không thuộc tập số nguyên dương (ℤ⁺)ⁿ.")
                self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } (\\mathbb{Z}^+)^n")
                self.eq_result_box.insert(tk.END, "\\n".join(out))
                self.last_dioph_category = "EMPTY_NO_POSITIVE_INTEGER"
                self.last_dioph_solutions = []
                self.last_dioph_n_total = 0
                return "EMPTY_NO_POSITIVE_INTEGER", [], 0, out

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
            self.last_dioph_category = "UNSUPPORTED_DIM>=2"
            self.last_dioph_solutions = []
            self.last_dioph_n_total = 0
            return "UNSUPPORTED_DIM>=2", [], 0, out

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

                        eval_count = min(n_total, 10)
                        for k_idx in range(eval_count):
                            pval = start_val + k_idx * m_mod
                            cand = [item.subs(param, pval) for item in sol_tuple]
                            if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                                sub_dict = {vr: c_val for vr, c_val in zip(vars_sorted, cand)}
                                if all(sp.simplify(eq_orig.subs(sub_dict)) == 0 for eq_orig in eq_syms):
                                    int_sols.append(tuple(int(c) for c in cand))

                        if n_total <= 10:
                            out.append(f"  ==> Liệt kê toàn bộ {len(int_sols)} bộ nghiệm nguyên dương:")
                        else:
                            out.append(f"  ==> Hệ có tổng cộng {n_total} bộ nghiệm nguyên dương. Hiển thị 10 bộ nghiệm đầu tiên (do giới hạn không gian giao diện):")

                        for idx, sol in enumerate(int_sols, 1):
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
                out.append(f"  ==> Kết luận: Hệ có {n_total} bộ nghiệm nguyên dương hữu hạn (chi tiết 10 bộ nghiệm đầu như trên).")
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
        self.last_dioph_category = category
        self.last_dioph_solutions = int_sols
        self.last_dioph_n_total = n_total
        return category, int_sols, n_total, out
'''

with open('cad_math_v2/cad_math_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

p_start = text.find("    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):")
p_end = text.find("    def plot_diophantine_system(self, sol_tuple,")

if p_start != -1 and p_end != -1:
    text = text[:p_start] + CLEAN_DIOPH + text[p_end:]
    with open('cad_math_v2/cad_math_v2.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Cleanly replaced solve_underdetermined_or_diophantine.")
else:
    print("Could not find start or end boundary!")
