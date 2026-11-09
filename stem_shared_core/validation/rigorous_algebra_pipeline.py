# -*- coding: utf-8 -*-
"""
rigorous_algebra_pipeline.py
============================
Quy trình 5 bước kiểm soát nghiệm nghiêm ngặt cho phương trình chứa căn thức:
Mục tiêu giải quyết triệt để lỗi logic toán học mà Reviewer chỉ ra:
  f(x) >= 0 (điều kiện trong căn) là CHƯA ĐỦ.
  BẮT BUỘC phải có điều kiện vế đối diện g(x) >= 0 trước khi bình phương!

Quy trình 5 bước (Formal 5-Stage Verification Pipeline):
  1. Phân tích miền xác định của các biểu thức trong căn: D_rad = {x | f(x) >= 0}.
  2. Bổ sung điều kiện dấu cần thiết trước khi nâng lũy thừa: D_sign = {x | g(x) >= 0}.
  3. Tìm nghiệm ứng viên đa thức (Polynomial Candidates) bằng SymPy solve.
  4. Lọc nghiệm sơ bộ qua tập giao D = D_rad ∩ D_sign.
  5. Thử lại trực tiếp vào phương trình gốc (Direct Residual Verification) để bảo chứng 100%.
"""

from __future__ import annotations
import sys
import math
import sympy as sp
from typing import Dict, List, Any, Tuple

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class RigorousAlgebraPipeline:
    """Bộ giải và kiểm soát nghiệm phương trình chứa căn thức chuẩn xác."""

    def __init__(self):
        self.x = sp.Symbol('x', real=True)

    def solve_radical_equation(self, eq_str: str) -> Dict[str, Any]:
        """
        Giải phương trình dạng sqrt(f(x)) = g(x) hoặc sqrt(f(x)) - g(x) = 0.
        Trả về chi tiết: nghiệm ứng viên, nghiệm ngoại lai bị loại, và tập nghiệm đúng.
        """
        # Chuẩn hóa chuỗi đầu vào
        if '=' in eq_str:
            lhs_str, rhs_str = eq_str.split('=', 1)
            lhs_expr = sp.sympify(lhs_str.strip())
            rhs_expr = sp.sympify(rhs_str.strip())
        else:
            lhs_expr = sp.sympify(eq_str.strip())
            rhs_expr = sp.Integer(0)

        diff_expr = lhs_expr - rhs_expr

        # Lấy chính xác Symbol x từ biểu thức đầu vào để tránh lệch assumptions
        syms = list(diff_expr.free_symbols)
        x = syms[0] if syms else sp.Symbol('x')

        # 1. Thu thập tất cả các biểu thức dưới dấu căn
        radicands = []
        for atom in diff_expr.atoms(sp.Pow):
            if atom.exp == sp.Rational(1, 2):
                radicands.append(atom.base)

        # 2. Bước 1: Điều kiện trong căn f(x) >= 0
        rad_conds = [r >= 0 for r in radicands]

        # 3. Bước 2: Nhận diện cấu trúc sqrt(f(x)) = g(x) để đặt điều kiện vế đối diện g(x) >= 0
        sign_conds = []
        # Trường hợp kinh điển: sqrt(f(x)) = g(x)
        if len(radicands) == 1:
            # Tách riêng căn thức ra một vế
            sqrt_term = sp.sqrt(radicands[0])
            # diff = sqrt_term + remainder => sqrt_term = -remainder
            remainder = sp.simplify(diff_expr - sqrt_term)
            g_expr = -remainder
            sign_conds.append(g_expr >= 0)

        # 4. Bước 3: Tìm nghiệm ứng viên đa thức (SymPy giải phương trình bình phương)
        # Bằng cách nâng lũy thừa loại bỏ căn
        candidates = []
        if len(radicands) == 1:
            squared_eq = sp.simplify(radicands[0] - (g_expr)**2)
            raw_candidates = sp.solve(squared_eq, x)
            candidates = [c for c in raw_candidates if c.is_real]
        else:
            # Dùng sp.solve trực tiếp nhưng không lọc
            raw_candidates = sp.solve(diff_expr, x)
            candidates = [c for c in raw_candidates if c.is_real]

        # 5. Bước 4 & 5: Lọc nghiệm và Thử lại trực tiếp vào phương trình gốc
        verified_roots = []
        extraneous_roots = []
        rejection_reasons = {}

        for c in candidates:
            c_val = float(c.evalf())
            
            # Kiểm tra điều kiện trong căn
            rad_ok = True
            for r in radicands:
                val_r = float(r.subs(x, c).evalf())
                if val_r < -1e-7:
                    rad_ok = False
                    rejection_reasons[str(c)] = f"Vi phạm điều kiện biểu thức dưới dấu căn không âm: {r} = {val_r:.3f} < 0"
                    break

            if not rad_ok:
                extraneous_roots.append(c)
                continue

            # Kiểm tra điều kiện vế đối diện không âm (g(x) >= 0)
            sign_ok = True
            for s in sign_conds:
                val_s = float(s.lhs.subs(x, c).evalf())
                if val_s < -1e-7:
                    sign_ok = False
                    rejection_reasons[str(c)] = f"Vi phạm điều kiện vế đối diện không âm trước khi bình phương: {s.lhs} = {val_s:.3f} < 0"
                    break

            if not sign_ok:
                extraneous_roots.append(c)
                continue

            # Thử lại trực tiếp vào phương trình gốc (Direct Residual Check)
            residual = float(abs(diff_expr.subs(x, c).evalf()))
            if residual < 1e-6:
                verified_roots.append(c)
            else:
                extraneous_roots.append(c)
                rejection_reasons[str(c)] = f"Thử lại phương trình gốc sai khác (residual = {residual:.4f} > 0)"

        return {
            "equation": eq_str,
            "raw_candidates": [str(c) for c in candidates],
            "verified_roots": [str(r) for r in verified_roots],
            "extraneous_roots": [str(e) for e in extraneous_roots],
            "rejection_reasons": rejection_reasons,
            "radicand_conditions": [str(c) for c in rad_conds],
            "sign_conditions": [str(c) for c in sign_conds]
        }

if __name__ == "__main__":
    pipeline = RigorousAlgebraPipeline()
    test_eq = "sqrt(x - 1) = 3 - x"
    res = pipeline.solve_radical_equation(test_eq)
    print("=" * 60)
    print(f"Phương trình kiểm thử: {test_eq}")
    print(f"1. Nghiệm ứng viên SymPy sinh ra: {res['raw_candidates']}")
    print(f"2. Điều kiện vế đối diện g(x) >= 0: {res['sign_conditions']}")
    print(f"3. Nghiệm ngoại lai bị loại: {res['extraneous_roots']}")
    print(f"   -> Lý do loại: {res['rejection_reasons']}")
    print(f"4. Nghiệm đúng được xác nhận: {res['verified_roots']}")
    print("=" * 60)
