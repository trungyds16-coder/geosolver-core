# -*- coding: utf-8 -*-
"""
Module: algebra_kernel.py
Mô tả: Lõi tính toán Đại số & Giải tích (Symbolic Computation Kernel) cho phần mềm CAD Math v2.
Thư viện cốt lõi: SymPy
Đường dẫn triển khai mục tiêu: D:\\AI DATA\\cad_math_v2\\algebra_kernel.py
"""

from __future__ import annotations

import math
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import sympy as sp
from sympy.calculus.util import continuous_domain
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


class AlgebraKernelError(Exception):
    """Ngoại lệ tùy chỉnh cho các lỗi toán học và cú pháp trong lõi CAD Math v2."""
    pass


# Cấu hình bộ chuyển đổi cú pháp giúp người dùng nhập tự nhiên (vd: "2x^2 + 3x - 5")
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def parse_math_expr(
    expr_str: str,
    local_vars: Optional[Dict[str, sp.Symbol]] = None,
    evaluate: bool = True,
) -> sp.Expr:
    """
    Phân tích chuỗi biểu thức toán học thành đối tượng SymPy Expr an toàn.

    Tham số:
        expr_str (str): Chuỗi biểu thức toán học đầu vào.
        local_vars (dict, optional): Từ điển ánh xạ tên biến sang Symbol của SymPy.
        evaluate (bool): Cho phép SymPy rút gọn sơ bộ ngay khi phân tích hay không.

    Trả về:
        sp.Expr: Biểu thức SymPy tương ứng.

    Ngoại lệ:
        AlgebraKernelError: Khi chuỗi rỗng, sai cú pháp hoặc có phép chia trực tiếp cho 0.
    """
    if not isinstance(expr_str, str) or not expr_str.strip():
        raise AlgebraKernelError("Biểu thức đầu vào không được để trống.")

    cleaned = expr_str.strip().replace("ln(", "log(")

    default_locals: Dict[str, Any] = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "cot": sp.cot,
        "sqrt": sp.sqrt,
        "Abs": sp.Abs,
        "abs": sp.Abs,
        "log": sp.log,
        "exp": sp.exp,
        "pi": sp.pi,
        "E": sp.E,
    }
    if local_vars:
        default_locals.update(local_vars)

    try:
        expr = parse_expr(
            cleaned,
            local_dict=default_locals,
            transformations=TRANSFORMATIONS,
            evaluate=evaluate,
        )
    except Exception as exc:
        raise AlgebraKernelError(
            f"Biểu thức không hợp lệ: '{expr_str}'. Chi tiết: {exc}"
        ) from exc

    # Kiểm tra lỗi chia cho 0 tĩnh (ComplexInfinity: zoo, hoặc NaN)
    if expr.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
        raise AlgebraKernelError(
            f"Phát hiện phép chia cho 0 hoặc giá trị không xác định trong: '{expr_str}'."
        )

    return expr


def _split_equation(
    eq_str: str, local_vars: Optional[Dict[str, sp.Symbol]] = None
) -> sp.Expr:
    """
    Chuyển chuỗi phương trình 'A = B' hoặc biểu thức 'A' về dạng chuẩn f(x) = A - B = 0.
    """
    if not isinstance(eq_str, str) or not eq_str.strip():
        raise AlgebraKernelError("Phương trình đầu vào không được để trống.")

    if "=" in eq_str:
        parts = eq_str.split("=")
        if len(parts) != 2:
            raise AlgebraKernelError(f"Cú pháp phương trình không hợp lệ: '{eq_str}'.")
        lhs = parse_math_expr(parts[0], local_vars=local_vars)
        rhs = parse_math_expr(parts[1], local_vars=local_vars)
        return lhs - rhs
    return parse_math_expr(eq_str, local_vars=local_vars)


# ==============================================================================
# 1. GIẢI PHƯƠNG TRÌNH ĐẠI SỐ, VÔ TỈ, TRỊ TUYỆT ĐỐI, LƯỢNG GIÁC & HỆ PHƯƠNG TRÌNH
# ==============================================================================


def solve_polynomial_equation(eq_str: str, var: str = "x") -> Dict[str, Any]:
    """
    Giải phương trình đa thức bậc 1, bậc 2, bậc 3, bậc 4 với đầy đủ bước phân tích
    nhân tử, tính biệt thức Delta và phân loại nghiệm thực / phức.

    Tham số:
        eq_str (str): Chuỗi phương trình đa thức (vd: 'x^2 - 5*x + 6 = 0').
        var (str): Tên biến cần giải (mặc định là 'x').

    Trả về:
        dict: Gồm các khóa:
            - degree (int): Bậc của đa thức.
            - coefficients (list): Danh sách hệ số từ bậc cao xuống thấp.
            - factored_form (str): Dạng phân tích thành nhân tử.
            - delta (sp.Expr | None): Giá trị biệt thức Delta.
            - steps (list[str]): Các bước giải chi tiết tiếng Việt.
            - real_roots (list[sp.Expr]): Danh sách nghiệm thực chính xác.
            - complex_roots (list[sp.Expr]): Danh sách nghiệm phức (không thực).
            - status (str): Trạng thái nghiệm ('has_real_roots', 'no_real_roots', 'infinite_roots').
    """
    x = sp.Symbol(var)
    expr = sp.expand(_split_equation(eq_str, {var: x}))

    if expr == 0:
        return {
            "degree": 0,
            "coefficients": [0],
            "factored_form": "0 = 0",
            "delta": None,
            "steps": ["Phương trình nghiệm đúng với mọi giá trị của ẩn."],
            "real_roots": [],
            "complex_roots": [],
            "status": "infinite_roots",
        }

    if not expr.is_polynomial(x):
        raise AlgebraKernelError(
            f"Biểu thức '{eq_str}' không phải là đa thức theo biến '{var}'."
        )

    poly = sp.Poly(expr, x)
    deg = poly.degree()

    if deg == 0:
        return {
            "degree": 0,
            "coefficients": poly.all_coeffs(),
            "factored_form": f"{expr} = 0",
            "delta": None,
            "steps": [f"Hằng số {expr} khác 0 nên phương trình vô nghiệm."],
            "real_roots": [],
            "complex_roots": [],
            "status": "no_real_roots",
        }

    if deg > 4:
        raise AlgebraKernelError(
            f"Hàm chuyên biệt hỗ trợ đa thức bậc 1 đến 4 (bậc hiện tại: {deg})."
        )

    coeffs = poly.all_coeffs()
    factored = sp.factor(expr)
    steps: List[str] = [
        f"Bước 1: Chuyển vế và thu gọn về dạng chuẩn: {expr} = 0 (Bậc {deg}).",
        f"Bước 2: Phân tích đa thức thành nhân tử: {factored} = 0.",
    ]

    delta: Optional[sp.Expr] = None
    if deg == 1:
        a, b = coeffs
        sol = -b / a
        steps.append(f"Bước 3: Phương trình bậc nhất ax + b = 0 có nghiệm x = -b/a = {sol}.")
    elif deg == 2:
        a, b, c = coeffs
        delta = sp.simplify(b**2 - 4 * a * c)
        steps.append(f"Bước 3: Tính biệt thức Delta = b^2 - 4ac = ({b})^2 - 4*({a})*({c}) = {delta}.")
        if delta.is_positive:
            steps.append("Bước 4: Vì Delta dương nên phương trình có 2 nghiệm thực phân biệt.")
        elif delta.is_zero:
            steps.append("Bước 4: Vì Delta = 0 nên phương trình có nghiệm kép x = -b/(2a).")
        else:
            steps.append("Bước 4: Vì Delta âm nên phương trình vô nghiệm trên tập số thực (có 2 nghiệm phức).")
    else:
        delta = sp.simplify(sp.discriminant(poly))
        steps.append(f"Bước 3: Biệt thức tổng quát (Discriminant) của đa thức bậc {deg} là Delta = {delta}.")
        steps.append("Bước 4: Giải các nhân tử hoặc áp dụng công thức Cardano / Ferrari để tìm nghiệm.")

    all_roots = sp.solve(expr, x)
    real_roots: List[sp.Expr] = []
    complex_roots: List[sp.Expr] = []

    for r in all_roots:
        r_simp = sp.simplify(r)
        im_part = sp.im(r_simp.evalf())
        if abs(float(im_part)) <= 1e-12:
            # Làm sạch phần ảo nhiễu số học nếu biểu thức thực bị biểu diễn dạng căn phức (casus irreducibilis)
            real_val = sp.re(r_simp) if not r_simp.is_real else r_simp
            real_roots.append(sp.simplify(real_val))
        else:
            complex_roots.append(r_simp)

    real_roots.sort(key=lambda val: float(val.evalf()))
    status = "has_real_roots" if real_roots else "no_real_roots"

    return {
        "degree": deg,
        "coefficients": coeffs,
        "factored_form": f"{factored} = 0",
        "delta": delta,
        "steps": steps,
        "real_roots": real_roots,
        "complex_roots": complex_roots,
        "status": status,
    }


def solve_radical_abs_equation(eq_str: str, var: str = "x") -> Dict[str, Any]:
    """
    Giải phương trình chứa căn thức (vô tỉ) và phương trình chứa giá trị tuyệt đối trên R.
    Tự động tìm điều kiện xác định và thử lại nghiệm để loại nghiệm ngoại lai.

    Tham số:
        eq_str (str): Chuỗi phương trình (vd: 'sqrt(2*x + 3) = x' hoặc 'Abs(2*x - 1) = x + 2').
        var (str): Tên biến thực (mặc định là 'x').

    Trả về:
        dict: Gồm điều kiện xác định (domain), danh sách nghiệm thực chính xác (roots),
              nghiệm xấp xỉ (roots_float) và trạng thái (status).
    """
    x = sp.Symbol(var, real=True)
    expr = _split_equation(eq_str, {var: x})

    try:
        dom = continuous_domain(expr, x, sp.S.Reals)
    except Exception:
        dom = sp.S.Reals

    candidate_roots: List[sp.Expr] = []

    # Chiến lược 1: Dùng sp.solve với biến thực và check=True
    try:
        solved = sp.solve(expr, x, check=True)
        if isinstance(solved, list):
            candidate_roots.extend(solved)
    except Exception:
        pass

    # Chiến lược 2: Bổ sung từ solveset trên miền thực nếu solve bỏ sót
    try:
        sol_set = sp.solveset(expr, x, domain=sp.S.Reals)
        if isinstance(sol_set, sp.FiniteSet):
            for item in sol_set:
                if item not in candidate_roots:
                    candidate_roots.append(item)
    except Exception:
        pass

    verified_roots: List[sp.Expr] = []
    for cand in candidate_roots:
        try:
            if not dom.contains(cand):
                continue
            residual = sp.simplify(expr.subs(x, cand))
            if residual == 0 or abs(complex(residual.evalf())) <= 1e-9:
                if not any(sp.simplify(cand - r) == 0 for r in verified_roots):
                    verified_roots.append(sp.simplify(cand))
        except Exception:
            continue

    verified_roots.sort(key=lambda val: float(val.evalf()))

    # Tính nghiệm ngoại lai từ phương trình hệ quả (bình phương hoặc phá trị tuyệt đối)
    if "=" in eq_str:
        lhs_s, rhs_s = eq_str.split("=", 1)
        lhs = parse_math_expr(lhs_s, {var: x})
        rhs = parse_math_expr(rhs_s, {var: x})
    else:
        lhs = parse_math_expr(eq_str, {var: x})
        rhs = sp.Integer(0)

    consequence_eqs: List[sp.Expr] = [sp.expand(lhs**2 - rhs**2)]
    abs_atoms = list((lhs - rhs).atoms(sp.Abs))
    if abs_atoms:
        target_abs = abs_atoms[0]
        inner_arg = target_abs.args[0]
        consequence_eqs.append((lhs - rhs).subs(target_abs, inner_arg))
        consequence_eqs.append((lhs - rhs).subs(target_abs, -inner_arg))

    algebraic_candidates: List[sp.Expr] = list(candidate_roots)
    for ceq in consequence_eqs:
        try:
            sols = sp.solve(ceq, x)
            for s in sols:
                if s.is_real:
                    s_simp = sp.simplify(s)
                    if not any(sp.simplify(s_simp - c) == 0 for c in algebraic_candidates):
                        algebraic_candidates.append(s_simp)
        except Exception:
            continue

    extraneous_roots: List[sp.Expr] = []
    for cand in algebraic_candidates:
        if not any(sp.simplify(cand - r) == 0 for r in verified_roots):
            extraneous_roots.append(cand)
    extraneous_roots.sort(key=lambda val: float(val.evalf()))

    return {
        "domain": str(dom),
        "roots": verified_roots,
        "official_roots": verified_roots,
        "extraneous_roots": extraneous_roots,
        "roots_float": [round(float(r.evalf()), 8) for r in verified_roots],
        "status": "has_solution" if verified_roots else "no_solution",
    }


def _extract_roots_from_set(
    sol_set: sp.Set, a: sp.Expr, b: sp.Expr, sample_range: int = 20
) -> List[sp.Expr]:
    """
    Trích xuất danh sách các nghiệm cụ thể nằm trong đoạn [a, b] từ tập nghiệm SymPy
    (hỗ trợ FiniteSet, Union, Intersection và ImageSet họ nghiệm lượng giác).
    """
    roots: List[sp.Expr] = []
    a_val = float(sp.sympify(a).evalf())
    b_val = float(sp.sympify(b).evalf())

    def _collect(s: sp.Set) -> None:
        if s == sp.EmptySet or s is sp.S.EmptySet:
            return
        if isinstance(s, sp.FiniteSet):
            for elem in s:
                try:
                    val = float(elem.evalf())
                    if a_val - 1e-9 <= val <= b_val + 1e-9:
                        roots.append(sp.simplify(elem))
                except Exception:
                    pass
        elif isinstance(s, sp.Union):
            for arg in s.args:
                _collect(arg)
        elif isinstance(s, sp.Intersection):
            for arg in s.args:
                if isinstance(arg, (sp.ImageSet, sp.FiniteSet, sp.Union)):
                    _collect(arg)
        elif isinstance(s, sp.ImageSet):
            lamda = s.lamda
            for k in range(-sample_range, sample_range + 1):
                try:
                    cand = sp.simplify(lamda(k))
                    val = float(cand.evalf())
                    if a_val - 1e-9 <= val <= b_val + 1e-9:
                        roots.append(cand)
                except Exception:
                    continue

    _collect(sol_set)

    unique_roots: List[sp.Expr] = []
    for r in roots:
        if not any(abs(float((r - u).evalf())) <= 1e-9 for u in unique_roots):
            unique_roots.append(r)

    unique_roots.sort(key=lambda val: float(val.evalf()))
    return unique_roots


def solve_trig_equation(
    eq_str: str,
    var: str = "x",
    interval: Tuple[Any, Any] = (0, 2 * sp.pi),
) -> Dict[str, Any]:
    """
    Giải phương trình lượng giác cơ bản: trả về họ nghiệm tổng quát và các nghiệm
    thuộc đoạn [a, b] cho trước (mặc định là [0, 2*pi]).

    Tham số:
        eq_str (str): Chuỗi phương trình lượng giác (vd: '2*sin(x) - 1 = 0').
        var (str): Tên biến góc (mặc định 'x').
        interval (tuple): Đoạn cần lọc nghiệm cụ thể (a, b).

    Trả về:
        dict: Gồm họ nghiệm tổng quát (general_solution), nghiệm trong đoạn (roots_in_interval)
              và trạng thái.
    """
    x = sp.Symbol(var, real=True)
    expr = _split_equation(eq_str, {var: x})
    a, b = sp.sympify(interval[0]), sp.sympify(interval[1])

    try:
        general_sol = sp.solveset(expr, x, domain=sp.S.Reals)
    except Exception as exc:
        raise AlgebraKernelError(f"Không thể giải phương trình lượng giác '{eq_str}': {exc}") from exc

    roots_in_interval = _extract_roots_from_set(general_sol, a, b)

    # Bổ sung nghiệm từ sp.solve nếu solveset trả về cấu trúc phức tạp chưa đánh giá hết
    if not roots_in_interval:
        try:
            base_roots = sp.solve(expr, x)
            for br in base_roots:
                if br.is_real:
                    for k in range(-10, 11):
                        for period in (sp.pi, 2 * sp.pi):
                            cand = sp.simplify(br + k * period)
                            if (
                                float(a.evalf()) - 1e-9
                                <= float(cand.evalf())
                                <= float(b.evalf()) + 1e-9
                            ):
                                res = sp.simplify(expr.subs(x, cand))
                                if res == 0 or abs(complex(res.evalf())) <= 1e-9:
                                    if not any(
                                        abs(float((cand - u).evalf())) <= 1e-9
                                        for u in roots_in_interval
                                    ):
                                        roots_in_interval.append(cand)
            roots_in_interval.sort(key=lambda val: float(val.evalf()))
        except Exception:
            pass

    return {
        "general_solution": str(general_sol),
        "interval": f"[{a}, {b}]",
        "roots_in_interval": roots_in_interval,
        "status": "has_solution" if (roots_in_interval or general_sol != sp.EmptySet) else "no_solution",
    }


def solve_system_2vars(
    eq1_str: str,
    eq2_str: str,
    vars_tuple: Tuple[str, str] = ("x", "y"),
) -> Dict[str, Any]:
    """
    Giải hệ phương trình 2 ẩn (hệ bậc nhất, hệ đối xứng loại 1, loại 2, hệ đa thức).

    Tham số:
        eq1_str (str): Phương trình thứ nhất (vd: 'x + y = 5').
        eq2_str (str): Phương trình thứ hai (vd: 'x*y = 6').
        vars_tuple (tuple): Tên 2 ẩn, mặc định ('x', 'y').

    Trả về:
        dict: Gồm danh sách các cặp nghiệm thực (solutions), số nghiệm và trạng thái.
    """
    var_x, var_y = vars_tuple
    x = sp.Symbol(var_x, real=True)
    y = sp.Symbol(var_y, real=True)
    local_map = {var_x: x, var_y: y}

    expr1 = _split_equation(eq1_str, local_map)
    expr2 = _split_equation(eq2_str, local_map)

    # Kiểm tra hệ vô số nghiệm (2 phương trình phụ thuộc tuyến tính tương đương)
    if sp.simplify(expr1) == 0 and sp.simplify(expr2) == 0:
        return {"solutions": [], "count": -1, "status": "infinite_solutions"}

    try:
        raw_sols = sp.solve([expr1, expr2], (x, y), dict=True)
    except Exception as exc:
        raise AlgebraKernelError(f"Lỗi khi giải hệ phương trình: {exc}") from exc

    real_solutions: List[Tuple[sp.Expr, sp.Expr]] = []
    for sol_dict in raw_sols:
        if x in sol_dict and y in sol_dict:
            val_x = sp.simplify(sol_dict[x])
            val_y = sp.simplify(sol_dict[y])
            # Nếu nghiệm còn chứa biến tự do -> hệ có vô số nghiệm
            if val_x.free_symbols or val_y.free_symbols:
                return {
                    "solutions": [(val_x, val_y)],
                    "count": -1,
                    "status": "infinite_solutions",
                }
            if val_x.is_real is not False and val_y.is_real is not False:
                if abs(float(sp.im(val_x.evalf()))) <= 1e-9 and abs(float(sp.im(val_y.evalf()))) <= 1e-9:
                    real_solutions.append((sp.re(val_x), sp.re(val_y)))

    status = "has_solution" if real_solutions else "no_solution"
    return {
        "solutions": real_solutions,
        "count": len(real_solutions),
        "status": status,
    }


# ==============================================================================
# 2. RÚT GỌN BIỂU THỨC VÀ BIẾN ĐỔI ĐẠI SỐ
# ==============================================================================


def simplify_algebraic_expression(expr_str: str) -> Dict[str, Any]:
    """
    Rút gọn căn thức, phân thức đại số và quy đồng mẫu thức.

    Tham số:
        expr_str (str): Biểu thức đầu vào (căn thức hoặc phân thức đại số).

    Trả về:
        dict:
            - simplified: Biểu thức rút gọn tổng quát.
            - radical_simplified: Biểu thức trục căn thức ở mẫu / khử căn lồng nhau.
            - rational_canceled: Phân thức đã giản ước nhân tử chung.
            - common_denominator_form: Biểu thức sau khi quy đồng mẫu thức.
            - numerator: Tử thức sau khi quy đồng.
            - denominator: Mẫu thức chung sau khi quy đồng.
    """
    expr = parse_math_expr(expr_str, evaluate=True)

    try:
        denested = sp.sqrtdenest(expr)
    except Exception:
        denested = expr

    try:
        rad_simp = sp.radsimp(denested)
    except Exception:
        rad_simp = denested

    canceled = sp.cancel(rad_simp)
    simplified = sp.simplify(canceled)
    together_expr = sp.together(expr)
    num, den = sp.fraction(together_expr)

    if den == 0:
        raise AlgebraKernelError("Mẫu thức bằng 0 sau khi biến đổi.")

    return {
        "original": expr,
        "simplified": simplified,
        "radical_simplified": rad_simp,
        "rational_canceled": canceled,
        "common_denominator_form": together_expr,
        "numerator": sp.expand(num),
        "denominator": sp.factor(den),
    }


def expand_and_factor_polynomial(expr_str: str) -> Dict[str, Any]:
    """
    Khai triển nhị thức / đa thức và phân tích đa thức thành nhân tử.

    Tham số:
        expr_str (str): Biểu thức đại số đầu vào (vd: '(x + 2)^4' hoặc 'x^3 - 3*x^2 + 3*x - 1').

    Trả về:
        dict: Gồm dạng khai triển (expanded) và dạng nhân tử (factored).
    """
    expr = parse_math_expr(expr_str, evaluate=False)
    expanded = sp.expand(expr)
    factored = sp.factor(expanded)

    return {
        "original": expr,
        "expanded": expanded,
        "factored": factored,
    }


# ==============================================================================
# 3. GIẢI TÍCH CƠ BẢN THPT (TẬP XÁC ĐỊNH, ĐẠO HÀM, CỰC TRỊ, TÍCH PHÂN, TIỆM CẬN)
# ==============================================================================


def find_function_domain(expr_str: str, var: str = "x") -> Dict[str, Any]:
    """
    Tìm tập xác định D của hàm số y = f(x) trên tập số thực R.

    Tham số:
        expr_str (str): Biểu thức hàm số theo biến var.
        var (str): Tên biến (mặc định 'x').

    Trả về:
        dict: Tập xác định dạng đối tượng SymPy Set (domain_set) và chuỗi mô tả (domain_str).
    """
    x = sp.Symbol(var, real=True)
    expr = parse_math_expr(expr_str, {var: x})

    try:
        dom = continuous_domain(expr, x, sp.S.Reals)
    except Exception as exc:
        raise AlgebraKernelError(f"Không thể xác định tập xác định của '{expr_str}': {exc}") from exc

    return {
        "domain_set": dom,
        "domain_str": str(dom),
    }


def analyze_derivatives_and_extrema(expr_str: str, var: str = "x") -> Dict[str, Any]:
    """
    Tính đạo hàm cấp 1, đạo hàm cấp 2 và tìm tọa độ các điểm cực trị (cực đại, cực tiểu)
    của hàm số y = f(x).

    Tham số:
        expr_str (str): Biểu thức hàm số y = f(x).
        var (str): Tên biến số (mặc định 'x').

    Trả về:
        dict:
            - derivative_1 (sp.Expr): Đạo hàm cấp 1 f'(x).
            - derivative_2 (sp.Expr): Đạo hàm cấp 2 f''(x).
            - local_maxima (list[tuple]): Danh sách các điểm cực đại (x_CD, y_CD).
            - local_minima (list[tuple]): Danh sách các điểm cực tiểu (x_CT, y_CT).
            - critical_points (list[sp.Expr]): Các nghiệm thực của f'(x) = 0 thuộc TXĐ.
    """
    x = sp.Symbol(var, real=True)
    expr = parse_math_expr(expr_str, {var: x})
    dom = continuous_domain(expr, x, sp.S.Reals)

    f1 = sp.simplify(sp.diff(expr, x))
    f2 = sp.simplify(sp.diff(expr, x, 2))

    # Tìm nghiệm thực của f'(x) = 0
    try:
        crit_set = sp.solveset(f1, x, domain=dom)
        if isinstance(crit_set, sp.FiniteSet):
            crit_points = sorted(list(crit_set), key=lambda v: float(v.evalf()))
        else:
            raw_pts = sp.solve(f1, x)
            crit_points = sorted(
                [p for p in raw_pts if p.is_real and dom.contains(p)],
                key=lambda v: float(v.evalf()),
            )
    except Exception:
        crit_points = []

    local_maxima: List[Tuple[sp.Expr, sp.Expr]] = []
    local_minima: List[Tuple[sp.Expr, sp.Expr]] = []

    for x0 in crit_points:
        y0 = sp.simplify(expr.subs(x, x0))
        d2_val = sp.simplify(f2.subs(x, x0))

        if d2_val.is_real and d2_val != 0:
            if d2_val < 0:
                local_maxima.append((x0, y0))
            elif d2_val > 0:
                local_minima.append((x0, y0))
        else:
            # Trường hợp f''(x0) = 0: Xét sự đổi dấu của f'(x) qua x0
            eps = sp.Rational(1, 10000)
            left_slope = f1.subs(x, x0 - eps).evalf()
            right_slope = f1.subs(x, x0 + eps).evalf()
            if left_slope > 0 and right_slope < 0:
                local_maxima.append((x0, y0))
            elif left_slope < 0 and right_slope > 0:
                local_minima.append((x0, y0))

    return {
        "derivative_1": f1,
        "derivative_2": f2,
        "critical_points": crit_points,
        "local_maxima": local_maxima,
        "local_minima": local_minima,
    }


def compute_integral_and_by_parts(
    expr_str: str,
    var: str = "x",
    limits: Optional[Tuple[Any, Any]] = None,
    u_str: Optional[str] = None,
    dv_str: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Tính nguyên hàm, tích phân xác định và trình bày chi tiết nguyên hàm từng phần:
    Integral(u * dv) = u * v - Integral(v * du).

    Tham số:
        expr_str (str): Biểu thức dưới dấu tích phân f(x).
        var (str): Biến tích phân (mặc định 'x').
        limits (tuple, optional): Cận tích phân xác định (a, b).
        u_str (str, optional): Biểu thức đặt u(x) khi tính nguyên hàm từng phần.
        dv_str (str, optional): Biểu thức đặt dv = g(x)dx khi tính nguyên hàm từng phần.

    Trả về:
        dict: Gồm nguyên hàm (antiderivative), tích phân xác định (definite_integral),
              và chi tiết từng bước nguyên hàm từng phần (by_parts_detail).
    """
    x = sp.Symbol(var, real=True)
    expr = parse_math_expr(expr_str, {var: x})

    antiderivative = sp.integrate(expr, x)

    definite_val: Optional[sp.Expr] = None
    if limits is not None:
        if len(limits) != 2:
            raise AlgebraKernelError("Cận tích phân phải gồm đúng 2 giá trị (a, b).")
        a = sp.sympify(limits[0])
        b = sp.sympify(limits[1])
        definite_val = sp.integrate(expr, (x, a, b))
        if definite_val.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
            raise AlgebraKernelError(
                f"Tích phân xác định của '{expr_str}' trên [{a}, {b}] phân kỳ hoặc không xác định."
            )

    by_parts_detail: Optional[Dict[str, Any]] = None
    if u_str is not None and dv_str is not None:
        u_expr = parse_math_expr(u_str, {var: x})
        dv_expr = parse_math_expr(dv_str, {var: x})
        du_expr = sp.diff(u_expr, x)
        v_expr = sp.integrate(dv_expr, x)
        uv_term = u_expr * v_expr
        v_du_integral = sp.integrate(v_expr * du_expr, x)
        final_by_parts = sp.simplify(uv_term - v_du_integral)

        by_parts_detail = {
            "u": u_expr,
            "du": du_expr,
            "dv": dv_expr,
            "v": v_expr,
            "uv": uv_term,
            "integral_v_du": v_du_integral,
            "result": final_by_parts,
            "formula_str": f"({u_expr})*({v_expr}) - Integral(({v_expr})*({du_expr}), {var}) = {final_by_parts} + C",
        }

    return {
        "antiderivative": antiderivative,
        "definite_integral": definite_val,
        "by_parts_detail": by_parts_detail,
    }


def find_asymptotes(expr_str: str, var: str = "x") -> Dict[str, List[sp.Expr]]:
    """
    Tìm tiệm cận đứng (TCĐ) và tiệm cận ngang (TCN) của hàm phân thức y = f(x).

    Tham số:
        expr_str (str): Biểu thức hàm phân thức (vd: '(2*x + 1)/(x - 3)').
        var (str): Tên biến số (mặc định 'x').

    Trả về:
        dict:
            - vertical_asymptotes (list[sp.Expr]): Danh sách các giá trị x = x0 là TCĐ.
            - horizontal_asymptotes (list[sp.Expr]): Danh sách các giá trị y = y0 là TCN.
    """
    x = sp.Symbol(var, real=True)
    expr = parse_math_expr(expr_str, {var: x})

    # 1. Tìm tiệm cận ngang: xét giới hạn khi x -> +oo và x -> -oo
    horizontal: List[sp.Expr] = []
    for direction in (sp.oo, -sp.oo):
        try:
            lim_val = sp.limit(expr, x, direction)
            if lim_val.is_real and not lim_val.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                lim_simp = sp.simplify(lim_val)
                if lim_simp not in horizontal:
                    horizontal.append(lim_simp)
        except Exception:
            continue

    # 2. Tìm tiệm cận đứng: tìm nghiệm của mẫu số và kiểm tra giới hạn một bên ra vô cực
    together_expr = sp.together(expr)
    _, denom = sp.fraction(together_expr)
    vertical: List[sp.Expr] = []

    try:
        cand_roots = sp.solve(denom, x)
    except Exception:
        cand_roots = []

    for x0 in cand_roots:
        if not x0.is_real:
            continue
        is_va = False
        for dir_sign in ("+", "-"):
            try:
                lim_side = sp.limit(expr, x, x0, dir=dir_sign)
                if lim_side in (sp.oo, -sp.oo, sp.zoo) or abs(lim_side) == sp.oo:
                    is_va = True
                    break
            except Exception:
                continue
        if is_va and x0 not in vertical:
            vertical.append(sp.simplify(x0))

    vertical.sort(key=lambda v: float(v.evalf()))
    horizontal.sort(key=lambda v: float(v.evalf()))

    return {
        "vertical_asymptotes": vertical,
        "horizontal_asymptotes": horizontal,
    }


# ==============================================================================
# 4. XUẤT DỮ LIỆU ĐỒ THỊ CHO MÀN HÌNH ĐỒ HỌA CANVAS
# ==============================================================================


def get_plot_points(
    expr_str: str,
    x_min: float,
    x_max: float,
    num_points: int = 500,
    var: str = "x",
    y_clip: float = 1e4,
) -> Tuple[List[float], List[float]]:
    """
    Sinh dữ liệu tọa độ (x_list, y_list) của hàm số trên đoạn [x_min, x_max] để vẽ
    lên màn hình đồ họa Canvas, có tự động phát hiện và lọc bỏ các điểm gián đoạn
    (tiệm cận đứng, chia cho 0, căn bậc chẵn của số âm, hoặc giá trị vượt ngưỡng tràn).

    Tham số:
        expr_str (str): Biểu thức hàm số y = f(x).
        x_min (float): Giá trị hoành độ nhỏ nhất.
        x_max (float): Giá trị hoành độ lớn nhất.
        num_points (int): Số lượng điểm lấy mẫu (mặc định 500).
        var (str): Tên biến độc lập (mặc định 'x').
        y_clip (float): Ngưỡng cắt tung độ tối đa để lọc điểm tiệm cận đứng (mặc định 1e4).

    Trả về:
        Tuple[List[float], List[float]]: Hai danh sách (x_list, y_list) có cùng độ dài,
        chứa các tọa độ số thực hợp lệ sẵn sàng hiển thị trên Canvas.
    """
    if x_min >= x_max:
        raise AlgebraKernelError(
            f"Khoảng vẽ đồ thị không hợp lệ: x_min ({x_min}) phải nhỏ hơn x_max ({x_max})."
        )
    if num_points < 2:
        raise AlgebraKernelError("Số lượng điểm lấy mẫu (num_points) phải từ 2 trở lên.")

    x = sp.Symbol(var, real=True)
    expr = parse_math_expr(expr_str, {var: x})

    # Xác định trước danh sách các điểm tiệm cận đứng / nghiệm của mẫu thức để lọc vùng lân cận
    _, denom = sp.fraction(sp.together(expr))
    singular_points: List[float] = []
    if denom != 1:
        try:
            for r in sp.solve(denom, x):
                if r.is_real:
                    singular_points.append(float(r.evalf()))
        except Exception:
            pass

    step = (x_max - x_min) / (num_points - 1)
    singularity_tol = max(step * 0.45, 1e-7)

    # Tạo hàm tính nhanh bằng lambdify với module 'math'
    fast_func = sp.lambdify(x, expr, modules=["math"])

    x_list: List[float] = []
    y_list: List[float] = []

    for i in range(num_points):
        xi = x_min + i * step

        # Bỏ qua điểm trùng hoặc nằm sát điểm kỳ dị / tiệm cận đứng
        if any(abs(xi - sp_pt) <= singularity_tol for sp_pt in singular_points):
            continue

        try:
            yi = fast_func(xi)
            if isinstance(yi, complex):
                if abs(yi.imag) > 1e-9:
                    continue
                yi = yi.real
            yi_float = float(yi)
        except (ValueError, ZeroDivisionError, OverflowError, TypeError):
            # Dự phòng đánh giá bằng SymPy nếu math module gặp lỗi miền xác định cục bộ (vd căn bậc lẻ số âm)
            try:
                val_sym = expr.subs(x, xi).evalf()
                if not val_sym.is_real:
                    continue
                yi_float = float(val_sym)
            except Exception:
                continue

        if math.isnan(yi_float) or math.isinf(yi_float):
            continue

        if abs(yi_float) > y_clip:
            continue

        x_list.append(round(xi, 8))
        y_list.append(round(yi_float, 8))

    return x_list, y_list


def deploy_to_target_directory(
    target_dir: str = r"D:\AI DATA\cad_math_v2",
    filename: str = "algebra_kernel.py",
) -> Optional[str]:
    """
    Hỗ trợ tự động sao chép module hiện tại vào thư mục đích D:\\AI DATA\\cad_math_v2
    khi chạy trên hệ thống Windows của người dùng.
    """
    try:
        current_file = Path(__file__).resolve()
        target_path = Path(target_dir)
        # Chỉ tự động ghi nếu ổ đĩa gốc (vd D:\) tồn tại hoặc đang ở môi trường cho phép tạo
        drive_root = target_path.drive
        if drive_root and not os.path.exists(drive_root + "\\"):
            return None
        target_path.mkdir(parents=True, exist_ok=True)
        dest_file = target_path / filename
        if current_file != dest_file.resolve():
            shutil.copy2(current_file, dest_file)
        return str(dest_file)
    except Exception:
        return None


def analyze_function_variation(
    expr_str: str,
    var: str = "x",
    parameter: Optional[str] = None,
    parameter_substitution: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    x = sp.Symbol(var, real=True)
    local_vars: Dict[str, sp.Symbol] = {var: x}
    if parameter:
        local_vars[parameter] = sp.Symbol(parameter, real=True)

    raw_expr = parse_math_expr(expr_str, local_vars=local_vars)

    # Đạo hàm chứa tham số (nếu bài toán có tham số m)
    parametric_derivative_1: Optional[sp.Expr] = None
    if parameter:
        parametric_derivative_1 = sp.simplify(sp.diff(raw_expr, x))

    # Thế giá trị tham số cụ thể để lập bảng biến thiên chi tiết
    expr = raw_expr
    if parameter_substitution:
        subs_map = {
            local_vars.get(k, sp.Symbol(k, real=True)): parse_math_expr(str(v))
            for k, v in parameter_substitution.items()
        }
        expr = sp.simplify(raw_expr.subs(subs_map))

    # 1. Tập xác định và điểm gián đoạn (nghiệm mẫu thức)
    dom = continuous_domain(expr, x, sp.S.Reals)
    together_expr = sp.together(expr)
    numer, denom = sp.fraction(together_expr)

    forbidden_points: List[sp.Expr] = []
    if denom != 1:
        for r in sp.solve(denom, x):
            if r.is_real:
                forbidden_points.append(sp.simplify(r))
    forbidden_points.sort(key=lambda val: float(val.evalf()))

    if not forbidden_points and dom == sp.S.Reals:
        domain_str = "Reals"
    elif forbidden_points:
        pts_str = ", ".join(str(p) for p in forbidden_points)
        domain_str = f"R \\ {{{pts_str}}}"
    else:
        domain_str = str(dom)

    # 2. Đạo hàm cấp 1 và các điểm tới hạn f'(x) = 0
    f1 = sp.simplify(sp.diff(expr, x))
    f1_num, _ = sp.fraction(sp.together(f1))

    critical_points: List[sp.Expr] = []
    for r in sp.solve(f1_num, x):
        if r.is_real and dom.contains(r):
            if not any(sp.simplify(r - cp) == 0 for cp in critical_points):
                critical_points.append(sp.simplify(r))
    critical_points.sort(key=lambda val: float(val.evalf()))

    # 3. Lập bảng biến thiên (xét dấu y' trên từng khoảng và gộp khoảng nếu chỉ bằng 0 tại hữu hạn điểm)
    breakpoints = sorted(
        forbidden_points + critical_points,
        key=lambda val: float(val.evalf()),
    )
    unique_bps: List[sp.Expr] = []
    for bp in breakpoints:
        if not any(sp.simplify(bp - u) == 0 for u in unique_bps):
            unique_bps.append(bp)

    raw_intervals: List[Tuple[Any, Any, int]] = []
    bounds: List[Any] = [-sp.oo] + unique_bps + [sp.oo]

    for idx in range(len(bounds) - 1):
        left_b, right_b = bounds[idx], bounds[idx + 1]
        if left_b == -sp.oo and right_b == sp.oo:
            test_pt = sp.Integer(0)
        elif left_b == -sp.oo:
            test_pt = right_b - sp.Integer(1)
        elif right_b == sp.oo:
            test_pt = left_b + sp.Integer(1)
        else:
            test_pt = (left_b + right_b) / 2

        slope_val = float(f1.subs(x, test_pt).evalf())
        sign = 1 if slope_val > 1e-9 else (-1 if slope_val < -1e-9 else 0)
        raw_intervals.append((left_b, right_b, sign))

    # Gộp hai khoảng kề nhau cùng dấu nếu điểm ngăn cách thuộc tập xác định (quy tắc SGK GDPT 2018)
    merged_intervals: List[Tuple[Any, Any, int]] = []
    for seg in raw_intervals:
        if not merged_intervals:
            merged_intervals.append(seg)
        else:
            prev_l, prev_r, prev_sign = merged_intervals[-1]
            curr_l, curr_r, curr_sign = seg
            is_forbidden = any(sp.simplify(curr_l - fp) == 0 for fp in forbidden_points)
            if prev_sign == curr_sign and not is_forbidden:
                merged_intervals[-1] = (prev_l, curr_r, prev_sign)
            else:
                merged_intervals.append(seg)

    increasing_intervals = [
        f"({l}, {r})" for l, r, s in merged_intervals if s > 0
    ]
    decreasing_intervals = [
        f"({l}, {r})" for l, r, s in merged_intervals if s < 0
    ]

    # 4. Tìm tọa độ điểm cực đại, cực tiểu dựa trên sự đổi dấu của f'(x) qua điểm tới hạn
    local_maxima: List[Tuple[sp.Expr, sp.Expr]] = []
    local_minima: List[Tuple[sp.Expr, sp.Expr]] = []

    for cp in critical_points:
        eps = sp.Rational(1, 1000)
        # Đảm bảo eps nhỏ hơn khoảng cách tới các điểm đặc biệt lân cận
        other_dists = [
            abs(float((cp - bp).evalf()))
            for bp in unique_bps
            if sp.simplify(cp - bp) != 0
        ]
        if other_dists:
            eps = min(eps, sp.Rational(int(min(other_dists) * 100), 400))

        left_s = float(f1.subs(x, cp - eps).evalf())
        right_s = float(f1.subs(x, cp + eps).evalf())
        y_val = sp.simplify(expr.subs(x, cp))

        if left_s > 1e-9 and right_s < -1e-9:
            local_maxima.append((cp, y_val))
        elif left_s < -1e-9 and right_s > 1e-9:
            local_minima.append((cp, y_val))

    # 5. Tìm tiệm cận đứng, tiệm cận ngang và tiệm cận xiên
    vertical_asymptotes: List[sp.Expr] = []
    for fp in forbidden_points:
        for dir_sign in ("+", "-"):
            lim_v = sp.limit(expr, x, fp, dir=dir_sign)
            if lim_v in (sp.oo, -sp.oo, sp.zoo) or abs(lim_v) == sp.oo:
                vertical_asymptotes.append(fp)
                break

    horizontal_asymptotes: List[sp.Expr] = []
    for inf_dir in (sp.oo, -sp.oo):
        try:
            lim_h = sp.limit(expr, x, inf_dir)
            if lim_h.is_real and not lim_h.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                lim_h_simp = sp.simplify(lim_h)
                if lim_h_simp not in horizontal_asymptotes:
                    horizontal_asymptotes.append(lim_h_simp)
        except Exception:
            pass

    oblique_asymptotes: List[sp.Expr] = []
    if not horizontal_asymptotes and denom != 1:
        try:
            a_coeff = sp.limit(expr / x, x, sp.oo)
            if (
                a_coeff.is_real
                and a_coeff != 0
                and not a_coeff.has(sp.oo, -sp.oo, sp.zoo, sp.nan)
            ):
                b_coeff = sp.limit(expr - a_coeff * x, x, sp.oo)
                if b_coeff.is_real and not b_coeff.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                    oblique_line = sp.simplify(a_coeff * x + b_coeff)
                    oblique_asymptotes.append(oblique_line)
        except Exception:
            pass

    return {
        "domain": domain_str,
        "domain_set": dom,
        "forbidden_points": forbidden_points,
        "derivative_1": f1,
        "parametric_derivative_1": parametric_derivative_1,
        "critical_points": critical_points,
        "variation_table": {
            "increasing_intervals": increasing_intervals,
            "decreasing_intervals": decreasing_intervals,
        },
        "extrema": {
            "local_maxima": local_maxima,
            "local_minima": local_minima,
        },
        "asymptotes": {
            "vertical": vertical_asymptotes,
            "horizontal": horizontal_asymptotes,
            "oblique": oblique_asymptotes,
        },
    }



# ==============================================================================
# 5. KHỐI KIỂM THỬ TỰ ĐỘNG (UNIT TESTS VỚI ASSERT)
# ==============================================================================

if __name__ == "__main__":
    print("=" * 72)
    print("KHỞI CHẠY BỘ KIỂM THỬ LÕI ĐẠI SỐ CAD MATH V2 (algebra_kernel.py)")
    print("=" * 72)

    # 1. Kiểm thử giải phương trình đa thức bậc 1, 2, 3, 4
    res_deg1 = solve_polynomial_equation("2*x - 6 = 0")
    assert res_deg1["degree"] == 1
    assert res_deg1["real_roots"] == [sp.Integer(3)]

    res_deg2 = solve_polynomial_equation("x^2 - 5*x + 6 = 0")
    assert res_deg2["degree"] == 2
    assert res_deg2["delta"] == sp.Integer(1)
    assert res_deg2["real_roots"] == [sp.Integer(2), sp.Integer(3)]

    res_deg3 = solve_polynomial_equation("x^3 - 6*x^2 + 11*x - 6 = 0")
    assert res_deg3["degree"] == 3
    assert res_deg3["real_roots"] == [sp.Integer(1), sp.Integer(2), sp.Integer(3)]

    res_deg4 = solve_polynomial_equation("x^4 - 5*x^2 + 4 = 0")
    assert res_deg4["degree"] == 4
    assert res_deg4["real_roots"] == [
        sp.Integer(-2),
        sp.Integer(-1),
        sp.Integer(1),
        sp.Integer(2),
    ]
    print("[PASS] 1.1: Phương trình đa thức bậc 1, 2, 3, 4 & biệt thức Delta.")

    # 2. Kiểm thử phương trình vô tỉ (căn thức) và trị tuyệt đối
    # Phương trình sqrt(2x + 3) = x có nghiệm thực duy nhất x = 3 (loại nghiệm ngoại lai x = -1)
    res_rad = solve_radical_abs_equation("sqrt(2*x + 3) = x")
    assert res_rad["roots"] == [sp.Integer(3)], f"Sai nghiệm căn thức: {res_rad}"

    res_abs = solve_radical_abs_equation("Abs(2*x - 1) = x + 2")
    assert res_abs["roots"] == [sp.Rational(-1, 3), sp.Integer(3)]
    print("[PASS] 1.2: Phương trình chứa căn thức (loại nghiệm ngoại lai) & trị tuyệt đối.")

    # 3. Kiểm thử phương trình lượng giác & hệ phương trình 2 ẩn
    res_trig = solve_trig_equation("2*sin(x) - 1 = 0", interval=(0, 2 * sp.pi))
    assert sp.pi / 6 in res_trig["roots_in_interval"]
    assert 5 * sp.pi / 6 in res_trig["roots_in_interval"]

    res_sys_linear = solve_system_2vars("2*x + y = 5", "x - y = 1")
    assert res_sys_linear["solutions"] == [(sp.Integer(2), sp.Integer(1))]

    res_sys_sym = solve_system_2vars("x + y = 5", "x*y = 6")
    assert (sp.Integer(2), sp.Integer(3)) in res_sys_sym["solutions"]
    assert (sp.Integer(3), sp.Integer(2)) in res_sys_sym["solutions"]
    print("[PASS] 1.3: Phương trình lượng giác & hệ phương trình 2 ẩn bậc nhất/đối xứng.")

    # 4. Kiểm thử rút gọn biểu thức, quy đồng mẫu thức, khai triển & phân tích nhân tử
    res_simp = simplify_algebraic_expression("1/(x - 1) + 1/(x + 1)")
    assert sp.simplify(res_simp["common_denominator_form"] - (2 * sp.Symbol("x")) / (sp.Symbol("x") ** 2 - 1)) == 0

    res_binom = expand_and_factor_polynomial("(x + 2)^3")
    x_sym = sp.Symbol("x")
    assert res_binom["expanded"] == x_sym**3 + 6 * x_sym**2 + 12 * x_sym + 8
    assert res_binom["factored"] == (x_sym + 2) ** 3
    print("[PASS] 2.0: Rút gọn phân thức, quy đồng mẫu thức, khai triển & nhân tử.")

    # 5. Kiểm thử Giải tích THPT: Tập xác định, Đạo hàm, Cực trị, Tích phân, Tiệm cận
    dom_info = find_function_domain("sqrt(x - 1)/(x - 3)")
    assert dom_info["domain_set"].contains(2) is True
    assert dom_info["domain_set"].contains(3) is False
    assert dom_info["domain_set"].contains(0) is False

    extrema_info = analyze_derivatives_and_extrema("x^3 - 3*x + 2")
    assert extrema_info["local_maxima"] == [(sp.Integer(-1), sp.Integer(4))]
    assert extrema_info["local_minima"] == [(sp.Integer(1), sp.Integer(0))]

    int_info = compute_integral_and_by_parts(
        "x * exp(x)",
        var="x",
        limits=(0, 1),
        u_str="x",
        dv_str="exp(x)",
    )
    assert int_info["definite_integral"] == sp.Integer(1)
    assert sp.simplify(int_info["by_parts_detail"]["result"] - (x_sym - 1) * sp.exp(x_sym)) == 0

    asymp_info = find_asymptotes("(2*x + 1)/(x - 3)")
    assert asymp_info["vertical_asymptotes"] == [sp.Integer(3)]
    assert asymp_info["horizontal_asymptotes"] == [sp.Integer(2)]
    print("[PASS] 3.0: Tập xác định, đạo hàm, cực trị, tích phân từng phần & tiệm cận.")

    # 6. Kiểm thử xuất dữ liệu đồ thị Canvas và lọc điểm gián đoạn
    x_pts, y_pts = get_plot_points("(2*x + 1)/(x - 1)", x_min=0.0, x_max=2.0, num_points=201)
    assert len(x_pts) == len(y_pts)
    assert len(x_pts) > 150
    assert 1.0 not in x_pts, "Điểm tiệm cận đứng x = 1.0 phải được lọc bỏ!"

    # 7. Kiểm thử bắt lỗi biểu thức không hợp lệ & chia cho 0
    error_caught = False
    try:
        parse_math_expr("1/0 + x")
    except AlgebraKernelError:
        error_caught = True
    assert error_caught is True, "Phải bắt được lỗi chia cho 0!"
    print("[PASS] 4.0 & 5.0: Xuất dữ liệu Canvas (lọc tiệm cận) & kiểm soát ngoại lệ.")

    saved_location = deploy_to_target_directory()
    if saved_location:
        print(f"[INFO] Đã tự động sao chép module vào: {saved_location}")
    else:
        print(r"[INFO] Để lưu trực tiếp vào D:\AI DATA\cad_math_v2\algebra_kernel.py, hãy đảm bảo ổ đĩa D: đang kết nối.")

    print("=" * 72)
    print("TẤT CẢ CÁC BÀI KIỂM THỬ (ASSERTIONS) ĐỀU THÀNH CÔNG 100%!")
    print("=" * 72)