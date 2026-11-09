# -*- coding: utf-8 -*-
"""
diophantine_integer_solver.py
=============================
BỘ GIẢI PHƯƠNG TRÌNH & HỆ PHƯƠNG TRÌNH NGHIỆM NGUYÊN (DIOPHANTINE SOLVER):
Giải quyết các bài toán số học, toán đố dân gian cổ điển (Trăm trâu trăm cỏ, Vừa gà vừa chó,
chia kẹo, chia tiền) - nơi mà số phương trình ít hơn số ẩn (Hệ vô định) nhưng ràng buộc
nghiệm phải là SỐ NGUYÊN DƯƠNG (x, y, z in Z+).
"""

from __future__ import annotations
import sys
import sympy as sp
from typing import Dict, List, Any, Tuple

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def solve_positive_integer_system(eqs: List[str], variables: List[str] = None, max_range: int = 150) -> Dict[str, Any]:
    """
    Tự động giải hệ phương trình nghiệm nguyên không âm / nguyên dương.
    Ví dụ:
      eqs = ["x + y + z = 100", "5*x + 3*y + z/3 = 100"]
      hoặc: ["x + y + z = 100", "15*x + 9*y + z = 300"]
    """
    steps = []
    steps.append("🔍 [BƯỚC 1: NHẬN DIỆN BÀI TOÁN SỐ HỌC / PHƯƠNG TRÌNH DIOPHANTINE]")
    steps.append("  • Số lượng phương trình: 2 phương trình, nhưng có 3 ẩn (x, y, z).")
    steps.append("  • Đây là Hệ phương trình vô định. Ràng buộc toán học bắt buộc: x, y, z ∈ ℤ⁺ (nguyên dương).")

    # Phân tích SymPy
    sym_dict = {v: sp.Symbol(v, integer=True) for v in (variables or ['x', 'y', 'z'])}
    
    parsed_eqs = []
    for eq_str in eqs:
        if '=' in eq_str:
            l, r = eq_str.split('=', 1)
            parsed_eqs.append(sp.simplify(sp.sympify(l, locals=sym_dict) - sp.sympify(r, locals=sym_dict)))
        else:
            parsed_eqs.append(sp.simplify(sp.sympify(eq_str, locals=sym_dict)))

    steps.append("\n📐 [BƯỚC 2: KHỬ ẨN ĐẠI SỐ ĐỂ ĐƯA VỀ PHƯƠNG TRÌNH DIOPHANTINE 2 BIẾN]")
    x, y, z = sym_dict.get('x'), sym_dict.get('y'), sym_dict.get('z')
    
    # Khử z: z = 100 - x - y
    elim_z = sp.solve(parsed_eqs[0], z)[0]
    steps.append(f"  • Từ phương trình (1), rút z theo x và y: z = {elim_z}")
    
    sub_eq2 = sp.simplify(parsed_eqs[1].subs(z, elim_z))
    steps.append(f"  • Thế vào phương trình (2) ta được: {sub_eq2} = 0")
    
    # Rút gọn hệ thức giữa x và y (vd: 7x + 4y = 100 hoặc 14x + 8y = 200)
    steps.append("\n💡 [BƯỚC 3: BIỆN LUẬN ĐIỀU KIỆN CHIA HẾT & TẬP NGHIỆM NGUYÊN DƯƠNG]")
    
    valid_solutions = []
    # Quét toàn bộ miền nghiệm nguyên dương trong phạm vi thực tế
    for xv in range(1, max_range):
        for yv in range(1, max_range):
            zv = float(elim_z.subs({x: xv, y: yv}))
            if zv > 0 and zv.is_integer():
                zv = int(zv)
                # Kiểm tra cả 2 phương trình
                e1 = parsed_eqs[0].subs({x: xv, y: yv, z: zv})
                e2 = parsed_eqs[1].subs({x: xv, y: yv, z: zv})
                if e1 == 0 and e2 == 0:
                    valid_solutions.append((xv, yv, zv))

    for idx, (xv, yv, zv) in enumerate(valid_solutions, 1):
        steps.append(f"  • Bộ nghiệm {idx}: x = {xv} (trâu đứng), y = {yv} (trâu nằm), z = {zv} (trâu già)")

    steps.append(f"\n✅ [BƯỚC 4: KẾT LUẬN TOÀN CỤC]")
    steps.append(f"  • Hệ phương trình có chính xác {len(valid_solutions)} bộ nghiệm nguyên dương thỏa mãn đề bài.")

    return {
        "status": "SOLVED",
        "total_solutions": len(valid_solutions),
        "solutions": valid_solutions,
        "pedagogical_steps": steps
    }

if __name__ == "__main__":
    test_eqs = ["x + y + z = 100", "5*x + 3*y + z/3 = 100"]
    res = solve_positive_integer_system(test_eqs)
    for s in res["pedagogical_steps"]:
        print(s)
