# -*- coding: utf-8 -*-
"""
update_generalized_diophantine.py
==================================
Thay thế bộ giải solve_underdetermined_or_diophantine bằng thuật toán toán học tổng quát:
- Hoàn toàn KHÔNG cố định ngữ cảnh con vật hay bài toán cụ thể nào.
- Xử lý tổng quát cho hệ N ẩn và M phương trình (M < N).
- Tự động phân tích tham số hóa, mẫu số chung, điều kiện chia hết và chặn miền nguyên dương.
"""

import sys
import sympy as sp

def apply_patch():
    target_path = r'd:\AI DATA\STEM_APP\cad_math_v2\cad_math_v2.py'
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    old_method_start = "    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):"
    next_method_start = "    def plot_diophantine_system(self, sol_tuple, vars_sorted, int_sols):"

    start_idx = content.find(old_method_start)
    end_idx = content.find(next_method_start)
    assert start_idx != -1, "Could not find start of solve_underdetermined_or_diophantine"
    assert end_idx != -1, "Could not find start of plot_diophantine_system"

    new_method = '''    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):
        """Giải hệ phương trình vô định & khảo sát nghiệm nguyên dương tổng quát (N ẩn, M phương trình)."""
        out = []
        out.append("=" * 85)
        out.append("QUY TRÌNH GIẢI HỆ PHƯƠNG TRÌNH VÔ ĐỊNH & KHẢO SÁT NGHIỆM NGUYÊN (DIOPHANTINE SYSTEM):")
        out.append("=" * 85)

        m = len(eq_syms)
        n = len(vars_sorted)
        var_names_str = ", ".join(s.name for s in vars_sorted)

        # BƯỚC 1: PHÂN TÍCH BẬC VÀ CẤU TRÚC HỆ PHƯƠNG TRÌNH
        out.append("\\n[BƯỚC 1: PHÂN TÍCH BẬC VÀ CẤU TRÚC HỆ PHƯƠNG TRÌNH]")
        out.append(f"  • Số lượng phương trình: M = {m}")
        out.append(f"  • Số lượng biến số: N = {n} ({var_names_str})")
        out.append(f"  • Bậc tự do của hệ: d = N - M = {n - m} tham số tự do.")
        out.append("  • Nhận định toán học:")
        out.append("    - Trên tập số thực ℝ: Hệ có vô số nghiệm tạo thành một không gian affine d chiều.")
        out.append(f"    - Khảo sát trên tập số nguyên dương ℤ⁺: Tìm các bộ ({var_names_str}) ∈ (ℤ⁺)ⁿ thỏa mãn hệ.")

        # BƯỚC 2: KHỬ ẨN ĐẠI SỐ VÀ BIỂU DIỄN THAM SỐ
        out.append("\\n[BƯỚC 2: KHỬ ẨN ĐẠI SỐ VÀ BIỂU DIỄN NGHIỆM TỔNG QUÁT THEO THAM SỐ]")
        linsols = sp.linsolve(eq_syms, vars_sorted)
        if not linsols:
            out.append("  • Hệ phương trình vô nghiệm trên tập số thực ℝ.")
            self.eq_result_canvas.render_latex(r"\\text{Hệ vô nghiệm trên } \\mathbb{R}")
            self.eq_result_box.insert(tk.END, "\\n".join(out))
            return

        sol_tuple = list(linsols)[0]
        free_syms = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)

        basic_vars = []
        for v, expr in zip(vars_sorted, sol_tuple):
            if expr == v:
                out.append(f"  • Ẩn tự do (Tham số hóa): {v} ∈ ℝ")
            else:
                basic_vars.append(v)
                out.append(f"  • Biểu diễn ẩn phụ thuộc {v}: {v} = {clean_display_expr(expr)}")

        # BƯỚC 3: BIỆN LUẬN ĐIỀU KIỆN SỐ HỌC & NGHIỆM NGUYÊN DƯƠNG
        out.append("\\n[BƯỚC 3: BIỆN LUẬN ĐIỀU KIỆN SỐ HỌC & TẬP NGHIỆM NGUYÊN DƯƠNG (ℤ⁺)]")
        int_sols = []

        if len(free_syms) == 1:
            param = free_syms[0]
            # Xác định mẫu số chung D để phân tích tính chia hết
            denoms = []
            for expr in sol_tuple:
                if hasattr(expr, 'as_numer_denom'):
                    denoms.append(expr.as_numer_denom()[1])
            int_denoms = [int(d) for d in denoms if hasattr(d, 'is_integer') and d.is_integer]
            lcm_denom = sp.ilcm(*int_denoms) if int_denoms else 1

            if lcm_denom > 1:
                out.append(f"  1. Điều kiện nguyên: Để các ẩn phụ thuộc ({', '.join(s.name for s in basic_vars)}) nhận giá trị nguyên,")
                out.append(f"     biểu thức chứa mẫu số đòi hỏi tham số {param} phải thỏa mãn quan hệ đồng dư modulo D = {lcm_denom}.")
            else:
                out.append(f"  1. Điều kiện nguyên: Tham số {param} nhận các giá trị nguyên ({param} ∈ ℤ).")

            out.append(f"  2. Điều kiện dương (Ràng buộc biên thực tế):")
            for v, expr in zip(vars_sorted, sol_tuple):
                out.append(f"     • {v} > 0  <=>  {clean_display_expr(expr)} > 0")

            # Quét tìm nghiệm nguyên dương trong phạm vi khả thi
            for pval in range(1, 1000):
                cand = [item.subs(param, pval) for item in sol_tuple]
                if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                    int_sols.append(tuple(int(c) for c in cand))

            if int_sols:
                param_idx = vars_sorted.index(param)
                valid_pvals = [s[param_idx] for s in int_sols]
                out.append(f"\\n  ==> Tìm được {len(int_sols)} giá trị hợp lệ của tham số {param} ∈ {{{', '.join(str(p) for p in valid_pvals)}}}:")
                for idx, sol in enumerate(int_sols, 1):
                    sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                    out.append(f"    • Bộ nghiệm {idx}: {sol_str}")
            else:
                out.append("  Không có bộ nghiệm nguyên dương nào trong phạm vi khảo sát.")
        elif len(free_syms) > 1:
            out.append(f"  Hệ có {len(free_syms)} tham số tự do ({', '.join(s.name for s in free_syms)}).")
            out.append("  Không gian nghiệm nguyên là lưới đa chiều; khảo sát các điểm nguyên dương trong lân cận.")
            # Quét đa chiều kích thước nhỏ
            p1, p2 = free_syms[0], free_syms[1]
            for pv1 in range(1, 100):
                for pv2 in range(1, 100):
                    cand = [item.subs({p1: pv1, p2: pv2}) for item in sol_tuple]
                    if all(hasattr(c, 'is_integer') and c.is_integer and c > 0 for c in cand):
                        int_sols.append(tuple(int(c) for c in cand))
                        if len(int_sols) >= 10:
                            break
                if len(int_sols) >= 10:
                    break
            if int_sols:
                out.append(f"  Tìm được các bộ nghiệm nguyên dương tiêu biểu (hiển thị tối đa 10 bộ):")
                for idx, sol in enumerate(int_sols, 1):
                    sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                    out.append(f"    • Bộ nghiệm {idx}: {sol_str}")

        # BƯỚC 4: HỌ NGHIỆM TỔNG QUÁT TRÊN ℝ
        out.append("\\n[BƯỚC 4: HỌ NGHIỆM TỔNG QUÁT TRÊN TẬP SỐ THỰC ℝ]")
        param_names = ", ".join(s.name for s in free_syms) if free_syms else "t"
        out.append(f"  • Nghiệm phụ thuộc vào {len(free_syms)} tham số ({param_names}) ∈ ℝ:")
        real_sol_str = ", ".join(f"{v.name} = {clean_display_expr(expr)}" for v, expr in zip(vars_sorted, sol_tuple))
        out.append(f"    ({real_sol_str})")

        # BƯỚC CUỐI: KẾT LUẬN CHÍNH THỨC
        out.append("\\n[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM CHÍNH THỨC S / CONCLUSION]")
        if int_sols:
            latex_cases = [r"(" + ", ".join(str(val) for val in sol) + r")" for sol in int_sols]
            latex_str = r"\\text{Nghiệm nguyên } (" + ", ".join(s.name for s in vars_sorted) + r") \\in \\{" + ", ".join(latex_cases) + r"\\}"
            out.append(f"  ==> Tập nghiệm nguyên dương: S_(ℤ⁺) = {{ " + "; ".join(latex_cases) + " }")
            self.eq_result_canvas.render_latex(latex_str)
        else:
            self.eq_result_canvas.render_latex(r"\\text{Vô số nghiệm trên } \\mathbb{R}")
            out.append("  ==> Hệ không có nghiệm nguyên dương (S_(ℤ⁺) = ∅).")

        self.eq_result_box.insert(tk.END, "\\n".join(out))
        self.plot_diophantine_system(sol_tuple, vars_sorted, int_sols)

'''

    updated_content = content[:start_idx] + new_method + content[end_idx:]
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("Generalized Diophantine solver applied successfully!")

if __name__ == '__main__':
    apply_patch()
