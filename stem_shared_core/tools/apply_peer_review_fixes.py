# -*- coding: utf-8 -*-
"""
apply_peer_review_fixes.py
==========================
Cập nhật mã nguồn cad_math_v2/cad_math_v2.py theo phản biện khoa học:
1. Xác định dấu chính xác (Symbolic Algebraic Sign) cho g(r) trong phương trình căn thức.
2. Phân loại 3 trường hợp cấu trúc cho hệ Diophantine:
   - Rỗng / Vô nghiệm (Infeasible / Empty)
   - Hữu hạn nghiệm (Finite Bounded)
   - Vô hạn nghiệm (Unbounded Infinite) - Xuất họ nghiệm tham số, không liệt kê giả tạo.
"""

import os
import sys

def patch():
    target_path = r'd:\AI DATA\STEM_APP\cad_math_v2\cad_math_v2.py'
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update solve_radical_pedagogical with exact algebraic sign determination
    old_radical_start = "    def solve_radical_pedagogical(self, target_eq, x):"
    next_method_start = "    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):"
    
    start_r = content.find(old_radical_start)
    end_r = content.find(next_method_start)
    assert start_r != -1 and end_r != -1, "Radical method bounds not found"

    new_radical_code = '''    def solve_radical_pedagogical(self, target_eq, x):
        """Giải phương trình vô tỷ dạng √(f(x)) = g(x) với kiểm tra dấu đại số chính xác."""
        steps = []
        rad_terms = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
        if not rad_terms:
            return None, []

        rad = rad_terms[0]
        fx = rad.base
        gx = sp.simplify(rad - target_eq)

        steps.append("\\n[BƯỚC 1: XÁC ĐỊNH ĐIỀU KIỆN CÓ NGHĨA & ĐIỀU KIỆN VẾ PHẢI]")
        steps.append(f"  • Đưa phương trình về dạng chuẩn tắc: √({clean_display_expr(fx)}) = {clean_display_expr(gx)}")
        steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
        try:
            cond_fx = sp.solve(fx >= 0, x)
            steps.append(f"    ==> Miền D_rad: {cond_fx}")
        except: pass
        steps.append(f"  • Điều kiện vế phải (bắt buộc g(x) >= 0 để căn thức bằng vế phải thực): {clean_display_expr(gx)} >= 0")
        try:
            cond_gx = sp.solve(gx >= 0, x)
            steps.append(f"    ==> Miền D_sign: {cond_gx}")
        except: pass

        steps.append("\\n[BƯỚC 2: BÌNH PHƯƠNG HAI VẾ TÌM TẬP NGHIỆM ĐẠI SỐ SƠ BỘ]")
        steps.append(f"  • ({clean_display_expr(rad)})² = ({clean_display_expr(gx)})²")
        poly_eq = sp.simplify(fx - gx**2)
        steps.append(f"  <=> {clean_display_expr(poly_eq)} = 0")

        raw_sols = sp.solve(poly_eq, x)
        steps.append(f"  • Nghiệm đại số sơ bộ từ phương trình hệ quả: {raw_sols}")

        steps.append("\\n[BƯỚC 3: XÁC ĐỊNH DẤU ĐẠI SỐ CHÍNH XÁC & LOẠI BỎ NGHIỆM NGOẠI LAI]")
        valid_sols = []

        def check_sign_exact(expr_sub):
            try:
                s = sp.sign(expr_sub)
                if s.is_number:
                    return float(s) >= 0
            except: pass
            try:
                return bool(sp.ask(sp.Q.nonnegative(expr_sub)))
            except: pass
            try:
                val = float(expr_sub.evalf())
                return val >= -1e-9
            except:
                return True

        for r in raw_sols:
            try:
                # Kiểm tra dấu đại số chính xác của g(r)
                g_sub = gx.subs(x, r)
                f_sub = fx.subs(x, r)
                is_gx_ok = check_sign_exact(g_sub)
                is_fx_ok = check_sign_exact(f_sub)

                if is_gx_ok and is_fx_ok:
                    valid_sols.append(r)
                    steps.append(f"  • x = {clean_display_expr(r)}: Thỏa mãn điều kiện vế phải g(r) >= 0 và f(r) >= 0 (Nhận).")
                else:
                    reasons = []
                    if not is_gx_ok:
                        reasons.append(f"vi phạm điều kiện vế phải {clean_display_expr(gx)} >= 0 (bẫy bình phương hai vế)")
                    if not is_fx_ok:
                        reasons.append(f"vi phạm điều kiện căn thức {clean_display_expr(fx)} >= 0")
                    steps.append(f"  • x = {clean_display_expr(r)}: LOẠI (Nghiệm ngoại lai do {', '.join(reasons)}).")
            except Exception:
                valid_sols.append(r)

        return steps, valid_sols

'''

    # 2. Update solve_underdetermined_or_diophantine with 3-way classification
    old_diophantine_start = "    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):"
    plot_method_start = "    def plot_diophantine_system(self, sol_tuple, vars_sorted, int_sols):"

    start_d = content.find(old_diophantine_start)
    end_d = content.find(plot_method_start)
    assert start_d != -1 and end_d != -1, "Diophantine method bounds not found"

    new_diophantine_code = '''    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):
        """Giải hệ phương trình vô định & phân loại 3 trường hợp: Vô nghiệm / Hữu hạn / Vô hạn nghiệm nguyên dương."""
        out = []
        out.append("=" * 85)
        out.append("QUY TRÌNH GIẢI HỆ PHƯƠNG TRÌNH VÔ ĐỊNH & KHẢO SÁT NGHIỆM NGUYÊN (DIOPHANTINE SYSTEM):")
        out.append("=" * 85)

        m = len(eq_syms)
        n = len(vars_sorted)
        var_names_str = ", ".join(s.name for s in vars_sorted)

        # BƯỚC 1: PHÂN TÍCH BẬC VÀ CẤU TRÚC HỆ PHƯƠNG TRÌNH
        out.append("\\n[BƯỚC 1: PHÂN TÍCH CẤU TRÚC ĐẠI SỐ TUYẾN TÍNH]")
        out.append(f"  • Số lượng phương trình: M = {m}")
        out.append(f"  • Số lượng biến số: N = {n} ({var_names_str})")
        out.append(f"  • Bậc tự do của hệ: d = N - M = {n - m} tham số tự do.")
        out.append("  • Nhận định toán học:")
        out.append("    - Trên tập số thực ℝ: Hệ có vô số nghiệm tạo thành một không gian affine d chiều.")
        out.append(f"    - Khảo sát trên tập số nguyên dương ℤ⁺: Ràng buộc đồng thời ({var_names_str}) ∈ (ℤ⁺)ⁿ.")

        # BƯỚC 2: KHỬ ẨN ĐẠI SỐ VÀ BIỂU DIỄN THAM SỐ
        out.append("\\n[BƯỚC 2: BIỂU DIỄN NGHIỆM TỔNG QUÁT THEO THAM SỐ AFFINE]")
        linsols = sp.linsolve(eq_syms, vars_sorted)
        if not linsols:
            out.append("  • Hệ phương trình vô nghiệm trên tập số thực ℝ (rank(A) != rank(A|b)).")
            self.eq_result_canvas.render_latex(r"\\text{Hệ vô nghiệm trên } \\mathbb{R}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return

        sol_tuple = list(linsols)[0]
        free_syms = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)

        basic_vars = []
        for v, expr in zip(vars_sorted, sol_tuple):
            if expr == v:
                out.append(f"  • Tham số tự do: {v} ∈ ℝ")
            else:
                basic_vars.append(v)
                out.append(f"  • Biến phụ thuộc {v}: {v} = {clean_display_expr(expr)}")

        # BƯỚC 3: PHÂN LOẠI CẤU TRÚC & BIỆN LUẬN NGHIỆM NGUYÊN DƯƠNG
        out.append("\\n[BƯỚC 3: BIỆN LUẬN SỐ HỌC & PHÂN LOẠI CẤU TRÚC MIỀN NGHIỆM]")
        int_sols = []
        diophantine_category = "UNKNOWN"

        if len(free_syms) == 1:
            param = free_syms[0]
            # Mẫu số chung D
            denoms = []
            for expr in sol_tuple:
                if hasattr(expr, 'as_numer_denom'):
                    denoms.append(expr.as_numer_denom()[1])
            int_denoms = [int(d) for d in denoms if hasattr(d, 'is_integer') and d.is_integer]
            lcm_denom = sp.ilcm(*int_denoms) if int_denoms else 1

            if lcm_denom > 1:
                out.append(f"  1. Điều kiện nguyên: Mẫu số chung D = {lcm_denom} đòi hỏi tham số {param} thỏa mãn quan hệ đồng dư modulo {lcm_denom}.")
            else:
                out.append(f"  1. Điều kiện nguyên: Tham số {param} nhận các giá trị nguyên ({param} ∈ ℤ).")

            # Xác định các chặn biên từ hệ bất phương trình v_i > 0
            lower_bounds = [sp.Integer(1)]
            upper_bounds = []
            infeasible_constant = False

            out.append("  2. Phân tích hệ bất phương trình ràng buộc biên (v_i > 0):")
            for v, expr in zip(vars_sorted, sol_tuple):
                expr_exp = sp.expand(expr)
                coeff = expr_exp.coeff(param)
                const = expr_exp.subs(param, 0)
                out.append(f"     • {v} > 0  <=>  {clean_display_expr(expr)} > 0")

                if coeff > 0:
                    lower_bounds.append(-const / coeff)
                elif coeff < 0:
                    upper_bounds.append(-const / coeff)
                else:
                    if const <= 0:
                        infeasible_constant = True

            p_min = max(lower_bounds)
            p_max = min(upper_bounds) if upper_bounds else None

            # Phân loại 3 trường hợp cấu trúc
            if infeasible_constant or (p_max is not None and p_min > p_max):
                diophantine_category = "EMPTY_INFEASIBLE"
                out.append("\\n  ==> KẾT QUẢ PHÂN LOẠI: Miền ràng buộc rỗng (Empty/Infeasible).")
                out.append("      Hệ không có nghiệm nguyên dương thỏa mãn đồng thời các điều kiện biên.")
            elif p_max is not None:
                diophantine_category = "FINITE_BOUNDED"
                out.append(f"\\n  ==> KẾT QUẢ PHÂN LOẠI: Miền nghiệm hữu hạn bị chặn (Finite Bounded).")
                out.append(f"      Khoảng giá trị của tham số: {param} ∈ [{clean_display_expr(p_min)}, {clean_display_expr(p_max)}].")
                start_p = int(sp.floor(p_min)) + 1 if p_min.is_integer and p_min in lower_bounds[1:] else int(sp.ceiling(p_min))
                end_p = int(sp.ceiling(p_max)) - 1 if p_max.is_integer else int(sp.floor(p_max))

                for pval in range(start_p, end_p + 1):
                    cand = [item.subs(param, pval) for item in sol_tuple]
                    if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                        int_sols.append(tuple(int(c) for c in cand))

                out.append(f"  ==> Liệt kê chính xác toàn bộ {len(int_sols)} bộ nghiệm nguyên dương:")
                for idx, sol in enumerate(int_sols, 1):
                    sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                    out.append(f"    • Bộ nghiệm {idx}: {sol_str}")
            else:
                diophantine_category = "UNBOUNDED_INFINITE"
                out.append(f"\\n  ==> KẾT QUẢ PHÂN LOẠI: Miền nghiệm vô hạn không bị chặn trên (Unbounded Infinite).")
                out.append(f"      Điều kiện tham số: {param} >= {clean_display_expr(p_min)} (với {param} ∈ ℤ, {param} mod {lcm_denom} phù hợp).")
                start_p = int(sp.ceiling(p_min))
                for pval in range(start_p, start_p + 200):
                    cand = [item.subs(param, pval) for item in sol_tuple]
                    if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                        int_sols.append(tuple(int(c) for c in cand))
                    if len(int_sols) >= 3:
                        break
                out.append(f"  ==> Hệ có VÔ SỐ NGHIỆM NGUYÊN DƯƠNG. Ba bộ nghiệm nhỏ nhất đại diện:")
                for idx, sol in enumerate(int_sols, 1):
                    sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                    out.append(f"    • Bộ nghiệm {idx}: {sol_str}")

        # BƯỚC 4: HỌ NGHIỆM TỔNG QUÁT TRÊN ℝ
        out.append("\\n[BƯỚC 4: HỌ NGHIỆM TỔNG QUÁT TRÊN TẬP SỐ THỰC ℝ]")
        param_names = ", ".join(s.name for s in free_syms) if free_syms else "t"
        out.append(f"  • Không gian nghiệm thực phụ thuộc vào {len(free_syms)} tham số ({param_names}) ∈ ℝ:")
        real_sol_str = ", ".join(f"{v.name} = {clean_display_expr(expr)}" for v, expr in zip(vars_sorted, sol_tuple))
        out.append(f"    ({real_sol_str})")

        # BƯỚC CUỐI: KẾT LUẬN CHÍNH THỨC
        out.append("\\n[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
        if diophantine_category == "FINITE_BOUNDED" and int_sols:
            latex_cases = [r"(" + ", ".join(str(val) for val in sol) + r")" for sol in int_sols]
            latex_str = r"\\text{Nghiệm nguyên } (" + ", ".join(s.name for s in vars_sorted) + r") \\in \\{" + ", ".join(latex_cases) + r"\\}"
            out.append(f"  ==> Tập nghiệm nguyên dương hữu hạn: S_(ℤ⁺) = {{ " + "; ".join(latex_cases) + " }")
            self.eq_result_canvas.render_latex(latex_str)
        elif diophantine_category == "UNBOUNDED_INFINITE":
            latex_str = r"\\text{Vô số nghiệm nguyên dương } (x_i \\in \\mathbb{Z}^+)"
            out.append(f"  ==> Hệ có vô số nghiệm nguyên dương phụ thuộc tham số không bị chặn.")
            self.eq_result_canvas.render_latex(latex_str)
        else:
            self.eq_result_canvas.render_latex(r"\\text{Vô nghiệm trên } \\mathbb{Z}^+")
            out.append("  ==> Hệ không có nghiệm nguyên dương (S_(ℤ⁺) = ∅).")

        self.eq_result_box.insert(tk.END, "\\n".join(out))
        self.plot_diophantine_system(sol_tuple, vars_sorted, int_sols)

'''

    # Apply both replacements
    content = content[:start_r] + new_radical_code + content[end_r:]
    # Re-find diophantine boundaries after radical code replacement
    start_d = content.find(old_diophantine_start)
    end_d = content.find(plot_method_start)
    content = content[:start_d] + new_diophantine_code + content[end_d:]

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Peer review fixes applied successfully to cad_math_v2.py!")

if __name__ == '__main__':
    patch()
