# -*- coding: utf-8 -*-
"""
Patch cad_math_v2/cad_math_v2.py for Round 8 refinements:
1. solve_radical_pedagogical: S formatting for approximate roots.
2. solve_underdetermined_or_diophantine: evaluate only displayed roots (min(n_total, 10)), remove duplicate message.
"""

def patch_v2_8():
    path = "cad_math_v2/cad_math_v2.py"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Step 4 S formatting in solve_radical_pedagogical
    old_step4_rad = '''        elif valid_sols:
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
        else:'''

    new_step4_rad = '''        elif valid_sols:
            has_approx = any(len(clean_display_expr(s)) > 40 or 'I' in str(s) for s in valid_sols)
            if has_approx:
                approx_vals = [f"{float(sp.re(sp.N(s, 10))):.4f}" for s in valid_sols]
                steps.append(f"  ==> Tập nghiệm chính thức: S gồm {len(valid_sols)} nghiệm thực, giá trị gần đúng: S ≈ {{{', '.join(approx_vals)}}}")
            else:
                s_str = ", ".join(clean_display_expr(s) for s in valid_sols)
                steps.append(f"  ==> Tập nghiệm chính thức: S = {{{s_str}}}")
        else:'''

    if old_step4_rad in text:
        text = text.replace(old_step4_rad, new_step4_rad)
        print("Updated radical Step 4 format.")
    else:
        print("Warning: old_step4_rad not matched.")

    # 2. Diophantine display optimization & duplicate message removal
    old_dio_loop = '''                        for k_idx in range(min(n_total, cap)):
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
                            out.append(f"    ... [còn {n_total - 10} bộ nghiệm tiếp theo]")'''

    new_dio_loop = '''                        eval_count = min(n_total, 10)
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
                            out.append(f"    ... [còn {n_total - 10} bộ nghiệm tiếp theo]")'''

    if old_dio_loop in text:
        text = text.replace(old_dio_loop, new_dio_loop)
        print("Updated Diophantine evaluation loop.")
    else:
        print("Warning: old_dio_loop not matched.")

    # 3. Step 4 conclusion duplicate removal
    old_dio_step4 = '''        if category == "FINITE_BOUNDED" and int_sols:
            if n_total > 10:
                latex_str = r"\\text{Có } " + str(n_total) + r" \\text{ nghiệm nguyên dương}"
                out.append(f"  ==> Hệ có tổng cộng {n_total} bộ nghiệm nguyên dương (đã hiển thị 10 nghiệm đầu tiên).")
                self.eq_result_canvas.render_latex(latex_str)'''

    new_dio_step4 = '''        if category == "FINITE_BOUNDED" and int_sols:
            if n_total > 10:
                latex_str = r"\\text{Có } " + str(n_total) + r" \\text{ nghiệm nguyên dương}"
                out.append(f"  ==> Kết luận: Hệ có {n_total} bộ nghiệm nguyên dương hữu hạn (chi tiết 10 bộ nghiệm đầu như trên).")
                self.eq_result_canvas.render_latex(latex_str)'''

    if old_dio_step4 in text:
        text = text.replace(old_dio_step4, new_dio_step4)
        print("Updated Diophantine Step 4 conclusion.")
    else:
        print("Warning: old_dio_step4 not matched.")

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("cad_math_v2.py patched successfully.")

if __name__ == "__main__":
    patch_v2_8()
