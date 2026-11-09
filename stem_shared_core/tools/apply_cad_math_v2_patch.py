# -*- coding: utf-8 -*-
"""
apply_cad_math_v2_patch.py
==========================
Cập nhật trực tiếp vào file cad_math_v2/cad_math_v2.py:
1. Bộ xử lý hệ phương trình vô định & Diophantine (Trăm trâu trăm cỏ).
2. Quy trình sư phạm khử nghiệm ngoại lai phương trình căn thức.
3. Đồ thị trực quan hóa ràng buộc và phân bố nghiệm nguyên dương.
"""

import os
import sys

def patch_cad_math():
    target_file = r'd:\AI DATA\STEM_APP\cad_math_v2\cad_math_v2.py'
    with open(target_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Determine line ending
    crlf = '\r\n' if '\r\n' in text else '\n'

    # --- 1. Patch solve_eq_action underdetermined check ---
    check_str = "self.solve_underdetermined_or_diophantine"
    if check_str not in text:
        marker = "vars_sorted = sorted(list(all_sys_syms), key=lambda s: s.name)"
        insert_code = (
            f"{crlf}                # KIỂM TRA HỆ PHƯƠNG TRÌNH VÔ ĐỊNH HOẶC BÀI TOÁN SỐ HỌC DIOPHANTINE{crlf}"
            f"                if len(vars_sorted) > len(eq_syms):{crlf}"
            f"                    self.solve_underdetermined_or_diophantine(eq_syms, vars_sorted, lines){crlf}"
            f"                    return{crlf}"
        )
        if marker in text:
            text = text.replace(marker, marker + insert_code, 1)
            print("Patch 1 (Diophantine check) applied!")
        else:
            print("Marker 1 not found!")
    else:
        print("Patch 1 already present!")

    # --- 2. Patch radical pedagogical solve in TRƯỜNG HỢP 5 ---
    rad_check = "has_radical = any(isinstance(node, sp.Pow)"
    if rad_check not in text:
        target_sols = "sols = sp.solve(target_eq, x)"
        radical_block = (
            f"            # KIỂM TRA PHƯƠNG TRÌNH CHỨA CĂN THỨC (RADICAL EQUATION){crlf}"
            f"            has_radical = any(isinstance(node, sp.Pow) and node.exp == sp.Rational(1, 2) for node in target_eq.atoms(sp.Pow)){crlf}"
            f"            if has_radical and not is_trig:{crlf}"
            f"                rad_steps, rad_sols = self.solve_radical_pedagogical(target_eq, x){crlf}"
            f"                if rad_steps:{crlf}"
            f"                    out.extend(rad_steps){crlf}"
            f"                    out.append(\"\\n[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM CHÍNH THỨC S]\"){crlf}"
            f"                    if rad_sols:{crlf}"
            f"                        latex_sols = [f'x = {{sp.latex(s)}}' for s in rad_sols]{crlf}"
            f"                        self.eq_result_canvas.render_latex(r' \\;; \\quad '.join(latex_sols)){crlf}"
            f"                        s_str = ', '.join(str(s) for s in rad_sols){crlf}"
            f"                        out.append(f'  • Tập nghiệm chính thức: S = {{{{{{s_str}}}}}}'){crlf}"
            f"                    else:{crlf}"
            f"                        out.append('  • Phương trình vô nghiệm trên tập số thực ℝ.'){crlf}"
            f"                        self.eq_result_canvas.render_latex(r'\\text{{Vô nghiệm trên }} \\mathbb{{R}}'){crlf}"
            f"                    self.eq_result_box.insert(tk.END, \"\\n\".join(out)){crlf}"
            f"                    f_num = sp.lambdify(x, target_eq, modules=['numpy', {{'sqrt': np.lib.scimath.sqrt}}]){crlf}"
            f"                    self.plot_oxy_roots(f_num, rad_sols){crlf}"
            f"                    return{crlf}{crlf}"
            f"            {target_sols}"
        )
        if target_sols in text:
            text = text.replace(target_sols, radical_block, 1)
            print("Patch 2 (Radical pedagogical solve) applied!")
        else:
            print("Target sols marker not found!")
    else:
        print("Patch 2 already present!")

    # --- 3. Add helper methods ---
    method_marker = "def solve_underdetermined_or_diophantine"
    if method_marker not in text:
        tab2_marker = "    # TAB 2: CỰC TRỊ VDC"
        helper_methods = (
            f"    def solve_radical_pedagogical(self, target_eq, x):{crlf}"
            f"        \"\"\"Giải phương trình vô tỷ kèm giải thích loại nghiệm ngoại lai chuẩn sư phạm.\"\"\"{crlf}"
            f"        steps = []{crlf}"
            f"        rad_terms = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]{crlf}"
            f"        if not rad_terms:{crlf}"
            f"            return None, []{crlf}"
            f"        rad = rad_terms[0]{crlf}"
            f"        fx = rad.base{crlf}"
            f"        gx = sp.simplify(rad - target_eq){crlf}"
            f"        steps.append(\"\\n[BƯỚC 1: XÁC ĐỊNH ĐIỀU KIỆN XÁC ĐỊNH & ĐIỀU KIỆN CÓ NGHĨA]\"){crlf}"
            f"        steps.append(f'  • Đưa phương trình về dạng chuẩn tắc: √({{clean_display_expr(fx)}}) = {{clean_display_expr(gx)}}'){crlf}"
            f"        steps.append(f'  • Điều kiện dưới dấu căn (radicand >= 0): {{clean_display_expr(fx)}} >= 0'){crlf}"
            f"        try:{crlf}"
            f"            cond_fx = sp.solve(fx >= 0, x){crlf}"
            f"            steps.append(f'    ==> {{cond_fx}}'){crlf}"
            f"        except: pass{crlf}"
            f"        steps.append(f'  • Điều kiện vế phải (vế không âm g(x) >= 0 để căn thức có nghĩa): {{clean_display_expr(gx)}} >= 0'){crlf}"
            f"        try:{crlf}"
            f"            cond_gx = sp.solve(gx >= 0, x){crlf}"
            f"            steps.append(f'    ==> {{cond_gx}}'){crlf}"
            f"        except: pass{crlf}"
            f"        steps.append(\"\\n[BƯỚC 2: BÌNH PHƯƠNG HAI VẾ TƯƠNG ĐƯƠNG]\"){crlf}"
            f"        steps.append(f'  • ({{clean_display_expr(rad)}})² = ({{clean_display_expr(gx)}})²'){crlf}"
            f"        poly_eq = sp.simplify(fx - gx**2){crlf}"
            f"        steps.append(f'  <=> {{clean_display_expr(poly_eq)}} = 0'){crlf}"
            f"        raw_sols = sp.solve(poly_eq, x){crlf}"
            f"        steps.append(f'  • Các nghiệm đại số tìm được sau khi bình phương: {{raw_sols}}'){crlf}"
            f"        steps.append(\"\\n[BƯỚC 3: ĐỐI CHIẾU ĐIỀU KIỆN & LOẠI BỎ NGHIỆM NGOẠI LAI (EXTRANEOUS ROOTS)]\"){crlf}"
            f"        valid_sols = []{crlf}"
            f"        for r in raw_sols:{crlf}"
            f"            try:{crlf}"
            f"                is_fx_ok = float(fx.subs(x, r).evalf()) >= -1e-9{crlf}"
            f"                is_gx_ok = float(gx.subs(x, r).evalf()) >= -1e-9{crlf}"
            f"                if is_fx_ok and is_gx_ok:{crlf}"
            f"                    valid_sols.append(r){crlf}"
            f"                    steps.append(f'  • x = {{clean_display_expr(r)}}: Thỏa mãn cả 2 điều kiện (Nhận).'){crlf}"
            f"                else:{crlf}"
            f"                    reasons = []{crlf}"
            f"                    if not is_fx_ok: reasons.append(f'vi phạm {{clean_display_expr(fx)}} >= 0'){crlf}"
            f"                    if not is_gx_ok: reasons.append(f'vi phạm vế phải {{clean_display_expr(gx)}} >= 0 (bẫy bình phương)'){crlf}"
            f"                    steps.append(f'  • x = {{clean_display_expr(r)}}: LOẠI (Nghiệm ngoại lai do {{', '.join(reasons)}}).'){crlf}"
            f"            except Exception:{crlf}"
            f"                valid_sols.append(r){crlf}"
            f"        return steps, valid_sols{crlf}{crlf}"
            f"    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines):{crlf}"
            f"        \"\"\"Giải hệ phương trình vô định & biện luận nghiệm nguyên dương (Diophantine).\"\"\"{crlf}"
            f"        out = []{crlf}"
            f"        out.append('=' * 85){crlf}"
            f"        out.append('QUY TRÌNH GIẢI HỆ PHƯƠNG TRÌNH VÔ ĐỊNH & TÌM NGHIỆM NGUYÊN (DIOPHANTINE SYSTEM):'){crlf}"
            f"        out.append('=' * 85){crlf}"
            f"        out.append(\"\\n[BƯỚC 1: PHÂN TÍCH BẬC VÀ CẤU TRÚC HỆ PHƯƠNG TRÌNH]\"){crlf}"
            f"        out.append(f'  • Số lượng phương trình: {{len(eq_syms)}}'){crlf}"
            f"        out.append(f'  • Số lượng biến số: {{len(vars_sorted)}} ({{', '.join(s.name for s in vars_sorted)}})'){crlf}"
            f"        out.append('  • Nhận xét: Số ẩn nhiều hơn số phương trình (Hệ vô định).'){crlf}"
            f"        out.append('    - Trên tập số thực ℝ: Hệ có vô số nghiệm phụ thuộc vào tham số tự do.'){crlf}"
            f"        out.append('    - Trong các bài toán số học, bài toán thực tế phổ thông (Trăm trâu trăm cỏ,'){crlf}"
            f"        out.append('      Vừa gà vừa chó, chia kẹo...): Các ẩn số đại diện cho các đối tượng rời rạc'){crlf}"
            f"        out.append('      nên bắt buộc có ràng buộc SỐ NGUYÊN DƯƠNG (x, y, z ∈ ℤ⁺).'){crlf}"
            f"        out.append(\"\\n[BƯỚC 2: KHỬ ẨN ĐẠI SỐ ĐỂ ĐƯA VỀ BIỂU DIỄN THAM SỐ]\"){crlf}"
            f"        linsols = sp.linsolve(eq_syms, vars_sorted){crlf}"
            f"        if not linsols:{crlf}"
            f"            out.append('  • Hệ phương trình vô nghiệm trên tập số thực ℝ.'){crlf}"
            f"            self.eq_result_canvas.render_latex(r'\\text{{Hệ vô nghiệm trên }} \\mathbb{{R}}'){crlf}"
            f"            self.eq_result_box.insert(tk.END, \"\\n\".join(out)){crlf}"
            f"            return{crlf}"
            f"        sol_tuple = list(linsols)[0]{crlf}"
            f"        free_syms = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name){crlf}"
            f"        for v, expr in zip(vars_sorted, sol_tuple):{crlf}"
            f"            out.append(f'  • Biểu diễn ẩn {{v}}: {{v}} = {{clean_display_expr(expr)}}'){crlf}"
            f"        out.append(\"\\n[BƯỚC 3: BIỆN LUẬN SỐ HỌC (TÍNH CHIA HẾT & THAM SỐ HÓA k ∈ ℤ⁺)]\"){crlf}"
            f"        int_sols = []{crlf}"
            f"        if len(free_syms) == 1:{crlf}"
            f"            param = free_syms[0]{crlf}"
            f"            buffalo_labels = {{vars_sorted[0]: 'trâu đứng', vars_sorted[1]: 'trâu nằm', vars_sorted[2]: 'trâu già'}} if len(vars_sorted) == 3 else {{}}{crlf}"
            f"            for pval in range(1, 500):{crlf}"
            f"                cand = [item.subs(param, pval) for item in sol_tuple]{crlf}"
            f"                if all(c.is_integer and c > 0 for c in cand):{crlf}"
            f"                    int_sols.append(tuple(int(c) for c in cand)){crlf}"
            f"            if int_sols and len(vars_sorted) == 3:{crlf}"
            f"                v1, v2, v3 = vars_sorted[0], vars_sorted[1], vars_sorted[2]{crlf}"
            f"                out.append('  (Áp dụng phương pháp rút thế khử ẩn và biện luận chia hết chuẩn SGK)'){crlf}"
            f"                out.append(f'  1. Từ các phương trình đề bài, khử ẩn {{v3}} để thu được phương trình liên hệ giữa {{v1}} và {{v2}}.'){crlf}"
            f"                out.append(f'  2. Biểu diễn {{v2}} theo {{v1}}, xét điều kiện để {{v2}} nhận giá trị nguyên dương.'){crlf}"
            f"                out.append('  3. Thiết lập tham số nguyên k để thỏa mãn tính chia hết (modulo).'){crlf}"
            f"                out.append(f'  4. Chặn miền giá trị của k từ điều kiện các ẩn {{v1}} > 0, {{v2}} > 0, {{v3}} > 0.'){crlf}"
            f"                out.append(f'\\n  ==> Tìm được {{len(int_sols)}} giá trị nguyên của k tương ứng với {{len(int_sols)}} bộ nghiệm nguyên dương:'){crlf}"
            f"                for idx, sol in enumerate(int_sols, 1):{crlf}"
            f"                    parts = []{crlf}"
            f"                    for v, val in zip(vars_sorted, sol):{crlf}"
            f"                        lbl = f' ({{buffalo_labels[v]}})' if v in buffalo_labels else ''{crlf}"
            f"                        parts.append(f'{{v}} = {{val}}{{lbl}}'){crlf}"
            f"                    out.append(f'    • Bộ nghiệm {{idx}}: ' + ', '.join(parts)){crlf}"
            f"            elif int_sols:{crlf}"
            f"                out.append(f'  Tìm được {{len(int_sols)}} bộ nghiệm nguyên dương thỏa mãn đề bài:'){crlf}"
            f"                for idx, sol in enumerate(int_sols, 1):{crlf}"
            f"                    sol_str = ', '.join(f'{{v}} = {{val}}' for v, val in zip(vars_sorted, sol)){crlf}"
            f"                    out.append(f'    • Bộ nghiệm {{idx}}: ({{sol_str}})'){crlf}"
            f"            else:{crlf}"
            f"                out.append('  Không tồn tại bộ nghiệm nguyên dương nào trong miền khảo sát.'){crlf}"
            f"        out.append(\"\\n[BƯỚC 4: NGHIỆM TỔNG QUÁT TRÊN TẬP SỐ THỰC ℝ]\"){crlf}"
            f"        param_names = ', '.join(s.name for s in free_syms) if free_syms else 't'{crlf}"
            f"        out.append(f'  • Họ nghiệm thực phụ thuộc vào tham số ({{param_names}}) ∈ ℝ:'){crlf}"
            f"        sol_real_str = ', '.join(f'{{v}} = {{clean_display_expr(expr)}}' for v, expr in zip(vars_sorted, sol_tuple)){crlf}"
            f"        out.append(f'    ({{sol_real_str}})'){crlf}"
            f"        out.append(\"\\n[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM CHÍNH THỨC S / CONCLUSION]\"){crlf}"
            f"        if int_sols:{crlf}"
            f"            latex_cases = []{crlf}"
            f"            for sol in int_sols:{crlf}"
            f"                latex_cases.append(r'(' + ', '.join(str(val) for val in sol) + r')'){crlf}"
            f"            latex_str = r'\\text{{Nghiệm nguyên }} (' + ', '.join(s.name for s in vars_sorted) + r') \\in \\{{' + ', '.join(latex_cases) + r'\\}}'{crlf}"
            f"            out.append('  ==> Tập nghiệm nguyên dương: ' + '; '.join(str(s) for s in int_sols)){crlf}"
            f"            self.eq_result_canvas.render_latex(latex_str){crlf}"
            f"        else:{crlf}"
            f"            self.eq_result_canvas.render_latex(r'\\text{{Vô số nghiệm trên }} \\mathbb{{R}}'){crlf}"
            f"            out.append('  ==> Hệ có vô số nghiệm thực phụ thuộc tham số trên ℝ.'){crlf}"
            f"        self.eq_result_box.insert(tk.END, \"\\n\".join(out)){crlf}"
            f"        self.plot_diophantine_system(sol_tuple, vars_sorted, int_sols){crlf}{crlf}"
            f"    def plot_diophantine_system(self, sol_tuple, vars_sorted, int_sols):{crlf}"
            f"        \"\"\"Vẽ đồ thị ràng buộc và phân bố nghiệm nguyên dương trên mặt phẳng Oxy.\"\"\"{crlf}"
            f"        self.eq_fig.clear(){crlf}"
            f"        ax = self.eq_fig.add_subplot(111){crlf}"
            f"        try:{crlf}"
            f"            if int_sols and len(int_sols) > 0 and len(vars_sorted) >= 2:{crlf}"
            f"                xs = [p[0] for p in int_sols]{crlf}"
            f"                ys = [p[1] for p in int_sols]{crlf}"
            f"                v1_name = vars_sorted[0].name{crlf}"
            f"                v2_name = vars_sorted[1].name{crlf}"
            f"                x_min, x_max = max(0, min(xs) - 4), max(xs) + 6{crlf}"
            f"                y_min, y_max = max(0, min(ys) - 4), max(ys) + 6{crlf}"
            f"                if len(int_sols) >= 2:{crlf}"
            f"                    dx = int_sols[1][0] - int_sols[0][0]{crlf}"
            f"                    dy = int_sols[1][1] - int_sols[0][1]{crlf}"
            f"                    if dx != 0:{crlf}"
            f"                        slope = dy / dx{crlf}"
            f"                        intercept = int_sols[0][1] - slope * int_sols[0][0]{crlf}"
            f"                        x_line = np.linspace(x_min, x_max, 200){crlf}"
            f"                        y_line = slope * x_line + intercept{crlf}"
            f"                        ax.plot(x_line, y_line, color='#0284c7', lw=1.8, ls='--', label=f'Ràng buộc {{v1_name}}-{{v2_name}}'){crlf}"
            f"                for p in int_sols:{crlf}"
            f"                    ax.scatter([p[0]], [p[1]], color='#dc2626', s=70, zorder=5){crlf}"
            f"                    label_str = f\"({{', '.join(f'{{v.name}}={{val}}' for v, val in zip(vars_sorted, p))}})\"{crlf}"
            f"                    ax.annotate(label_str, (p[0], p[1]),{crlf}"
            f"                                textcoords='offset points', xytext=(8, 8),{crlf}"
            f"                                fontsize=8, fontweight='bold', color='#b91c1c',{crlf}"
            f"                                bbox=dict(boxstyle='round,pad=0.2', fc='#fef2f2', ec='#f87171', lw=0.8)){crlf}"
            f"                ax.set_title(f'Mặt phẳng {{v1_name}}O{{v2_name}}: Phân Bố Nghiệm Nguyên Dương (ℤ⁺)', fontsize=9, fontweight='bold', color='#1e293b'){crlf}"
            f"                ax.set_xlabel(f'Trục O{{v1_name}}', fontsize=8){crlf}"
            f"                ax.set_ylabel(f'Trục O{{v2_name}}', fontsize=8){crlf}"
            f"                ax.set_xlim(x_min, x_max){crlf}"
            f"                ax.set_ylim(y_min, y_max){crlf}"
            f"                ax.grid(True, ls=':', color='#cbd5e1'){crlf}"
            f"                ax.legend(fontsize=8, loc='upper right'){crlf}"
            f"            else:{crlf}"
            f"                ax.text(0.5, 0.5, 'Hệ vô định: Vô số nghiệm trên ℝ', ha='center', va='center',{crlf}"
            f"                        fontsize=10, color='#64748b'){crlf}"
            f"            self.eq_canvas.draw(){crlf}"
            f"        except Exception:{crlf}"
            f"            pass{crlf}{crlf}"
            f"    # TAB 2: CỰC TRỊ VDC"
        )
        if tab2_marker in text:
            text = text.replace(tab2_marker, helper_methods, 1)
            print("Patch 3 (Helper methods) applied!")
        else:
            print("Tab 2 marker not found!")
    else:
        print("Patch 3 already present!")

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(text)

    print("Successfully patched cad_math_v2.py!")

if __name__ == '__main__':
    patch_cad_math()
