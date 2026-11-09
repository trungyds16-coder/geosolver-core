# -*- coding: utf-8 -*-
"""
Module: higher_math_kernel.py
Mô tả: Lõi Tính Toán & Suy Luận Toán Cao Cấp Đại Học (Higher Mathematics Kernel)
Thuộc hệ sinh thái: STEM Shared Core (cad_math_v2 / STEM_APP)
Các phân hệ chính:
  1. Đại số tuyến tính, Hệ phương trình, Không gian Vector, Trị riêng, Dạng toàn phương
  2. Giải tích đơn biến nâng cao: Giới hạn vô định, Khai triển Taylor/Maclaurin, Tích phân suy rộng
  3. Chuỗi số (D'Alembert, Cauchy, Leibniz), Chuỗi lũy thừa & Chuỗi Fourier
  4. Giải tích đa biến: Đạo hàm riêng, Ma trận Hessian, Cực trị tự do & Cực trị Lagrange, Tích phân kép/bội ba
  5. Tích phân Đường - Mặt & Lý thuyết trường (Gradient, Divergence, Curl, Hàm thế vị)
  6. Phương trình vi phân (Cấp 1, Cấp 2 hệ số hằng) & Biến đổi Laplace
"""

from __future__ import annotations

import re
import math
from typing import Any, Dict, List, Optional, Tuple, Union

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

# Cấu hình bộ biến đổi cú pháp tự nhiên
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


class HigherMathKernelError(Exception):
    """Ngoại lệ chuyên dụng cho các lỗi toán học cao cấp trong lõi."""
    pass


def parse_higher_math_expr(
    expr_str: str,
    local_vars: Optional[Dict[str, Any]] = None,
    evaluate: bool = True,
) -> sp.Expr:
    """
    Phân tích chuỗi toán học thành đối tượng SymPy Expr an toàn, hỗ trợ hàm cao cấp.
    """
    if not isinstance(expr_str, str) or not expr_str.strip():
        raise HigherMathKernelError("Biểu thức toán học không được để trống.")

    cleaned = expr_str.strip()
    cleaned = cleaned.replace("ln(", "log(")
    cleaned = re.sub(r"\bexp\(", "sp_exp(", cleaned)

    default_locals: Dict[str, Any] = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "cot": sp.cot,
        "arcsin": sp.asin,
        "arccos": sp.acos,
        "arctan": sp.atan,
        "sinh": sp.sinh,
        "cosh": sp.cosh,
        "tanh": sp.tanh,
        "sqrt": sp.sqrt,
        "Abs": sp.Abs,
        "abs": sp.Abs,
        "log": sp.log,
        "sp_exp": sp.exp,
        "exp": sp.exp,
        "pi": sp.pi,
        "E": sp.E,
        "e": sp.E,
        "oo": sp.oo,
        "inf": sp.oo,
        "I": sp.I,
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
        raise HigherMathKernelError(
            f"Lỗi cú pháp biểu thức: '{expr_str}'. Chi tiết: {exc}"
        ) from exc

    if expr.has(sp.zoo, sp.nan):
        raise HigherMathKernelError(
            f"Phát hiện phép chia cho 0 hoặc giá trị không xác định trong: '{expr_str}'."
        )

    return expr


def parse_matrix_input(text: str) -> sp.Matrix:
    """
    Chuyển đổi chuỗi ma trận đa định dạng thành đối tượng SymPy Matrix.
    Hỗ trợ:
      - [[1, 2], [3, 4]]
      - 1 2; 3 4
      - Từng dòng:
          1  2  3
          4  5  6
      - Hỗ trợ tham số ký hiệu: m, k, a...
    """
    if not text or not text.strip():
        raise HigherMathKernelError("Dữ liệu ma trận không được để trống.")

    cleaned = text.strip()

    # Dạng 1: Python/JSON list of lists: [[1, 2], [3, 4]]
    if cleaned.startswith("[") and "]" in cleaned:
        try:
            # Thử evaluate an toàn qua parse_higher_math_expr
            rows_raw = re.findall(r"\[([^\[\]]+)\]", cleaned)
            if rows_raw:
                grid = []
                for row_str in rows_raw:
                    items = [parse_higher_math_expr(x.strip()) for x in row_str.split(",") if x.strip()]
                    if items:
                        grid.append(items)
                if grid:
                    return sp.Matrix(grid)
        except Exception:
            pass

    # Dạng 2: Phân cách bằng dấu chấm phẩy ';' giữa các hàng
    if ";" in cleaned:
        row_strs = [r.strip() for r in cleaned.split(";") if r.strip()]
        grid = []
        for r_s in row_strs:
            # Phân tách phần tử bằng phẩy hoặc dấu cách
            elements = re.split(r"[,\s]+", r_s.strip())
            row_items = [parse_higher_math_expr(el) for el in elements if el]
            if row_items:
                grid.append(row_items)
        if grid:
            return sp.Matrix(grid)

    # Dạng 3: Xuống dòng từng hàng
    lines = [ln.strip() for ln in cleaned.splitlines() if ln.strip()]
    grid = []
    for line in lines:
        elements = re.split(r"[,\s]+", line)
        row_items = [parse_higher_math_expr(el) for el in elements if el]
        if row_items:
            grid.append(row_items)

    if not grid:
        raise HigherMathKernelError(f"Không thể phân tích dữ liệu ma trận từ: '{text}'.")

    # Kiểm tra tính đồng đều số cột
    cols_count = len(grid[0])
    for idx, row in enumerate(grid):
        if len(row) != cols_count:
            raise HigherMathKernelError(
                f"Hàng {idx+1} có {len(row)} phần tử, không khớp với hàng 1 ({cols_count} phần tử)."
            )

    return sp.Matrix(grid)


def format_matrix_latex(mat: sp.Matrix) -> str:
    """Định dạng ma trận thành mã LaTeX chuẩn."""
    return sp.latex(mat)


def format_matrix_plain(mat: sp.Matrix) -> str:
    """Định dạng ma trận thành bảng văn bản căn lề thẳng hàng."""
    rows, cols = mat.shape
    str_cells = [[str(mat[r, c]) for c in range(cols)] for r in range(rows)]
    col_widths = [max(len(str_cells[r][c]) for r in range(rows)) for c in range(cols)]
    lines = []
    for r in range(rows):
        row_str = "  ".join(str_cells[r][c].rjust(col_widths[c]) for c in range(cols))
        lines.append(f"│  {row_str}  │")
    header = "┌" + " " * (sum(col_widths) + 2 * cols + 2) + "┐"
    footer = "└" + " " * (sum(col_widths) + 2 * cols + 2) + "┘"
    return "\n".join([header] + lines + [footer])


# ==============================================================================
# PHÂN HỆ 1: ĐẠI SỐ TUYẾN TÍNH & KHÔNG GIAN VECTOR (LINEAR ALGEBRA)
# ==============================================================================

class LinearAlgebraEngine:
    """Lõi giải toán Đại số tuyến tính, Ma trận và Không gian Vector."""

    @staticmethod
    def analyze_matrix(mat_input: Union[str, sp.Matrix]) -> Dict[str, Any]:
        """Phân tích toàn diện thuộc tính ma trận: Định thức, Hạng, Vết, Nghịch đảo, Bậc thang."""
        mat = parse_matrix_input(mat_input) if isinstance(mat_input, str) else mat_input
        rows, cols = mat.shape
        is_square = (rows == cols)

        det_val = None
        det_steps = []
        inv_mat = None
        inv_steps = []
        trace_val = None

        if is_square:
            det_val = mat.det()
            trace_val = mat.trace()
            det_steps.append(f"Kích thước ma trận vuông: {rows} x {cols}")
            det_steps.append(f"Định thức |A| = {det_val}")

            if det_val != 0:
                inv_mat = mat.inv()
                inv_steps.append("Do |A| ≠ 0 nên ma trận A khả nghịch (khác suy biến).")
                inv_steps.append("Ma trận nghịch đảo A^(-1) tồn tại.")
            else:
                inv_steps.append("Do |A| = 0 nên ma trận A suy biến, KHÔNG có ma trận nghịch đảo.")

        rank_val = mat.rank()
        rref_mat, pivot_cols = mat.rref()

        return {
            "status": "SUCCESS",
            "shape": (rows, cols),
            "is_square": is_square,
            "det": det_val,
            "trace": trace_val,
            "rank": rank_val,
            "inv": inv_mat,
            "rref": rref_mat,
            "pivots": pivot_cols,
            "det_steps": det_steps,
            "inv_steps": inv_steps,
            "plain_text": format_matrix_plain(mat),
            "latex": format_matrix_latex(mat),
        }

    @staticmethod
    def solve_linear_system(
        A_input: Union[str, sp.Matrix],
        B_input: Union[str, sp.Matrix, List[Any]],
    ) -> Dict[str, Any]:
        """
        Giải hệ phương trình tuyến tính Ax = B theo định lý Kronecker-Capelli & Gauss-Jordan.
        """
        A = parse_matrix_input(A_input) if isinstance(A_input, str) else A_input
        if isinstance(B_input, str):
            B = parse_matrix_input(B_input)
            if B.cols != 1 and B.rows == 1:
                B = B.T
        elif isinstance(B_input, list):
            B = sp.Matrix([parse_higher_math_expr(str(x)) for x in B_input])
        else:
            B = B_input

        if A.rows != B.rows:
            raise HigherMathKernelError(
                f"Kích thước không tương thích: A có {A.rows} hàng nhưng B có {B.rows} hàng."
            )

        augmented = A.row_join(B)
        rank_A = A.rank()
        rank_aug = augmented.rank()
        num_vars = A.cols

        steps = [
            f"1. Ma trận hệ số A kích thước: {A.rows} x {A.cols}",
            f"2. Ma trận mở rộng [A|B] kích thước: {augmented.rows} x {augmented.cols}",
            f"3. Hạng của A: rank(A) = {rank_A}",
            f"4. Hạng của ma trận mở rộng: rank(A|B) = {rank_aug}",
        ]

        # Áp dụng định lý Kronecker - Capelli
        if rank_A < rank_aug:
            steps.append("5. Theo định lý Kronecker - Capelli: rank(A) < rank(A|B) => Hệ PHƯƠNG TRÌNH VÔ NGHIỆM.")
            return {
                "status": "SUCCESS",
                "solution_type": "NO_SOLUTION",
                "message": "Hệ phương trình vô nghiệm (Inconsistent).",
                "rank_A": rank_A,
                "rank_aug": rank_aug,
                "steps": steps,
            }

        rref_aug, pivots = augmented.rref()
        steps.append(f"5. Đưa [A|B] về dạng ma trận bậc thang rút gọn (RREF), các cột chốt: {pivots}")

        if rank_A == rank_aug == num_vars:
            # Nghiệm duy nhất
            sol = A.LUsolve(B) if A.rows == A.cols else A.pinv() * B
            steps.append(f"6. Do rank(A) = rank(A|B) = số ẩn ({num_vars}) => Hệ có NGHIỆM DUY NHẤT.")
            sol_dict = {f"x_{i+1}": sol[i, 0] for i in range(num_vars)}
            return {
                "status": "SUCCESS",
                "solution_type": "UNIQUE",
                "solution": sol,
                "solution_dict": sol_dict,
                "rank_A": rank_A,
                "rank_aug": rank_aug,
                "steps": steps,
            }
        else:
            # Vô số nghiệm phụ thuộc tham số
            free_count = num_vars - rank_A
            steps.append(
                f"6. Do rank(A) = rank(A|B) = {rank_A} < số ẩn ({num_vars}) => Hệ có VÔ SỐ NGHIỆM phụ thuộc {free_count} tham số tự do."
            )
            # Dùng sp.linsolve để lấy nghiệm dạng tham số
            vars_symbols = [sp.Symbol(f"x_{i+1}") for i in range(num_vars)]
            gen_sol = sp.linsolve((A, B), vars_symbols)
            return {
                "status": "SUCCESS",
                "solution_type": "INFINITE",
                "free_variables_count": free_count,
                "general_solution": gen_sol,
                "rank_A": rank_A,
                "rank_aug": rank_aug,
                "steps": steps,
            }

    @staticmethod
    def eigen_analysis(mat_input: Union[str, sp.Matrix]) -> Dict[str, Any]:
        """
        Tìm đa thức đặc trưng, trị riêng, vector riêng và khảo sát chéo hóa ma trận.
        """
        mat = parse_matrix_input(mat_input) if isinstance(mat_input, str) else mat_input
        if mat.rows != mat.cols:
            raise HigherMathKernelError("Chỉ có thể tìm trị riêng cho ma trận vuông.")

        n = mat.rows
        lam = sp.Symbol("lambda")
        char_poly = mat.charpoly(lam)
        eigenvals_dict = {}
        try:
            eigenvals_dict = mat.eigenvals()
        except Exception:
            pass

        steps = [
            f"1. Phương trình đặc trưng: det(A - λ·I) = {char_poly.as_expr()} = 0",
            f"2. Các trị riêng (kèm bội đại số):",
        ]
        for val, mult in eigenvals_dict.items():
            approx_str = ""
            try:
                c_val = complex(sp.N(val))
                if abs(c_val.imag) < 1e-9:
                    approx_str = f" ≈ {c_val.real:.4f}"
                else:
                    approx_str = f" ≈ {c_val.real:.4f} + {c_val.imag:.4f}i"
            except Exception:
                pass
            steps.append(f"   • λ = {val}{approx_str} (bội đại số = {mult})")

        eigen_details = []
        total_geom_mult = 0
        P_cols = []
        diag_vals = []
        eigenvects_raw = []
        try:
            eigenvects_raw = mat.eigenvects(simplify=False)
        except Exception as e_ev:
            steps.append(f"   (Lưu ý: Không thể tìm dạng đóng giải tích cho toàn bộ vector riêng: {e_ev})")

        for val, alg_mult, v_list in eigenvects_raw:
            geom_mult = len(v_list)
            total_geom_mult += geom_mult
            eigen_details.append({
                "eigenvalue": val,
                "algebraic_mult": alg_mult,
                "geometric_mult": geom_mult,
                "eigenvectors": v_list,
            })
            steps.append(f"3. Không gian riêng tương ứng λ = {val}: có {geom_mult} vector độc lập tuyến tính.")
            for v in v_list:
                P_cols.append(v)
                diag_vals.append(val)

        is_diagonalizable = (total_geom_mult == n)
        P_mat = None
        D_mat = None
        if is_diagonalizable and len(P_cols) == n:
            P_mat = sp.Matrix.hstack(*P_cols)
            D_mat = sp.diag(*diag_vals)
            steps.append("4. KẾT LUẬN: Ma trận A chéo hóa được (tổng số vector riêng độc lập = n).")
            steps.append("   Tồn tại ma trận chuyển cơ sở P sao cho P^(-1) A P = D.")
        else:
            steps.append("4. KẾT LUẬN: Ma trận A không chéo hóa được trên trường số đang xét.")

        return {
            "status": "SUCCESS",
            "characteristic_polynomial": char_poly.as_expr(),
            "eigenvalues": eigenvals_dict,
            "eigen_details": eigen_details,
            "is_diagonalizable": is_diagonalizable,
            "P_matrix": P_mat,
            "D_matrix": D_mat,
            "steps": steps,
        }

    @staticmethod
    def analyze_quadratic_form(
        q_expr_or_mat: Union[str, sp.Matrix],
        vars_list: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Phân tích dạng toàn phương Q(x): Tìm ma trận đối xứng, định thức con chính Sylvester và phân loại dấu.
        """
        if isinstance(q_expr_or_mat, (str, sp.Matrix)) and (
            isinstance(q_expr_or_mat, sp.Matrix) or "[" in str(q_expr_or_mat) or ";" in str(q_expr_or_mat)
        ):
            mat = parse_matrix_input(q_expr_or_mat) if isinstance(q_expr_or_mat, str) else q_expr_or_mat
        else:
            # Phân tích từ biểu thức đa thức thuần nhất bậc 2
            expr_str = str(q_expr_or_mat)
            if not vars_list:
                vars_list = ["x_1", "x_2", "x_3"] if "x_1" in expr_str else ["x", "y", "z"]
            symbols = [sp.Symbol(v) for v in vars_list]
            expr = parse_higher_math_expr(expr_str, local_vars={v: s for v, s in zip(vars_list, symbols)})
            n = len(symbols)
            grid = [[0 for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i == j:
                        coeff = expr.coeff(symbols[i] ** 2)
                        grid[i][j] = coeff
                    else:
                        coeff = expr.coeff(symbols[i] * symbols[j])
                        grid[i][j] = coeff / 2
            mat = sp.Matrix(grid)

        if mat.rows != mat.cols or mat != mat.T:
            raise HigherMathKernelError("Ma trận của dạng toàn phương phải là ma trận đối xứng.")

        n = mat.rows
        # Tính các định thức con chính góc (Principal Minors - Sylvester)
        minors = []
        steps = ["1. Ma trận đối xứng A liên kết với dạng toàn phương:"]
        steps.append(format_matrix_plain(mat))
        steps.append("2. Tính các định thức con chính góc (Tiêu chuẩn Sylvester):")

        for k in range(1, n + 1):
            sub_mat = mat[:k, :k]
            d_k = sub_mat.det()
            minors.append(d_k)
            steps.append(f"   • Δ_{k} = det(A_{k}) = {d_k}")

        # Phân loại theo tiêu chuẩn Sylvester
        has_symbols = any(hasattr(m, 'free_symbols') and bool(m.free_symbols) for m in minors)
        classification = "Biện luận theo tham số" if has_symbols else "Không xác định dấu (Indefinite)"

        if not has_symbols:
            try:
                num_minors = [float(sp.N(m)) for m in minors]
                if all(m > 0 for m in num_minors):
                    classification = "XÁC ĐỊNH DƯƠNG (Positive Definite)"
                    steps.append("3. Do tất cả Δ_k > 0 => Dạng toàn phương xác định dương (Q > 0 với mọi x ≠ 0).")
                elif all((-1) ** (i + 1) * num_minors[i] > 0 for i in range(n)):
                    classification = "XÁC ĐỊNH ÂM (Negative Definite)"
                    steps.append("3. Do các định thức con chính đan dấu (Δ_1 < 0, Δ_2 > 0, ...) => Dạng toàn phương xác định âm.")
                else:
                    steps.append(f"3. Dạng toàn phương: {classification}.")
            except Exception:
                steps.append(f"3. Dạng toàn phương: {classification}.")
        else:
            steps.append("3. Biện luận dấu dạng toàn phương theo tham số dựa trên hệ định thức con chính:")
            steps.append("   • Để xác định dương: cần hệ điều kiện Δ_k > 0 với mọi k = 1..n.")
            steps.append("   • Để xác định âm: cần hệ điều kiện (-1)^k · Δ_k > 0 với mọi k = 1..n.")

        return {
            "status": "SUCCESS",
            "matrix": mat,
            "minors": minors,
            "classification": classification,
            "steps": steps,
        }


# ==============================================================================
# PHÂN HỆ 2: GIẢI TÍCH ĐƠN BIẾN NÂNG CAO (CALCULUS I & IMPROPER INTEGRALS)
# ==============================================================================

class AdvancedCalculusEngine:
    """Lõi Giới hạn vô định, Khai triển Taylor và Tích phân suy rộng."""

    @staticmethod
    def compute_advanced_limit(
        expr_str: str,
        var_str: str = "x",
        point_str: str = "0",
        direction: str = "+-",
    ) -> Dict[str, Any]:
        """Tính giới hạn nâng cao kèm nhận diện dạng vô định."""
        var = sp.Symbol(var_str)
        point = parse_higher_math_expr(point_str, local_vars={var_str: var})
        expr = parse_higher_math_expr(expr_str, local_vars={var_str: var})

        dir_param = "+-"
        if direction in ("+", "right", "phải"):
            dir_param = "+"
        elif direction in ("-", "left", "trái"):
            dir_param = "-"

        lim_val = sp.limit(expr, var, point, dir=dir_param)
        steps = [
            f"1. Khảo sát giới hạn: lim ({expr}) khi {var_str} -> {point_str} (hướng: {dir_param})",
            f"2. Giá trị giới hạn tính được: {lim_val}",
        ]

        # Kiểm tra khai triển Taylor xung quanh điểm đó nếu điểm hữu hạn
        if point.is_finite:
            try:
                taylor_approx = sp.series(expr, var, point, n=3).removeO()
                steps.append(f"3. Xấp xỉ Taylor địa phương lân cận {point_str}: {taylor_approx}")
            except Exception:
                pass

        return {
            "status": "SUCCESS",
            "limit": lim_val,
            "steps": steps,
            "latex": f"\\lim_{{{var_str} \\to {sp.latex(point)}}} \\left({sp.latex(expr)}\\right) = {sp.latex(lim_val)}",
        }

    @staticmethod
    def compute_taylor_series(
        expr_str: str,
        var_str: str = "x",
        center_str: str = "0",
        order: int = 5,
    ) -> Dict[str, Any]:
        """Khai triển Taylor / Maclaurin với phần dư Peano cấp n."""
        var = sp.Symbol(var_str)
        center = parse_higher_math_expr(center_str, local_vars={var_str: var})
        expr = parse_higher_math_expr(expr_str, local_vars={var_str: var})

        series_with_O = sp.series(expr, var, center, n=order + 1)
        polynomial_part = series_with_O.removeO()

        steps = [
            f"1. Hàm số f({var_str}) = {expr}",
            f"2. Điểm khai triển x_0 = {center_str}, cấp khai triển n = {order}",
            f"3. Khai triển chuỗi Taylor kèm phần dư Peano:",
            f"   f({var_str}) = {series_with_O}",
        ]

        return {
            "status": "SUCCESS",
            "series": series_with_O,
            "polynomial": polynomial_part,
            "steps": steps,
            "latex": sp.latex(series_with_O),
        }

    @staticmethod
    def compute_improper_integral(
        expr_str: str,
        var_str: str = "x",
        lower_str: str = "0",
        upper_str: str = "oo",
    ) -> Dict[str, Any]:
        """Tính tích phân suy rộng loại 1 & 2 và khảo sát tính hội tụ/phân kỳ."""
        var = sp.Symbol(var_str)
        a = parse_higher_math_expr(lower_str, local_vars={var_str: var})
        b = parse_higher_math_expr(upper_str, local_vars={var_str: var})
        expr = parse_higher_math_expr(expr_str, local_vars={var_str: var})

        # Nguyên hàm F(x)
        antideriv = sp.integrate(expr, var)
        steps = [
            f"1. Xét tích phân suy rộng I = ∫[{lower_str} đến {upper_str}] ({expr}) d{var_str}",
            f"2. Họ nguyên hàm: F({var_str}) = {antideriv}",
        ]

        integral_val = sp.integrate(expr, (var, a, b))
        is_convergent = not (integral_val.has(sp.oo, -sp.oo, sp.zoo, sp.nan))

        if is_convergent:
            steps.append(f"3. Tích phân HỘI TỤ, giá trị hữu hạn: I = {integral_val}")
        else:
            steps.append(f"3. Tích phân PHÂN KỲ (Divergent), giá trị tiến ra: {integral_val}")

        return {
            "status": "SUCCESS",
            "is_convergent": is_convergent,
            "value": integral_val,
            "antiderivative": antideriv,
            "steps": steps,
            "latex": f"\\int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} {sp.latex(expr)}\\, d{var_str} = {sp.latex(integral_val)}",
        }


# ==============================================================================
# PHÂN HỆ 3: CHUỖI SỐ, CHUỖI LŨY THỪA & FOURIER (SERIES & FOURIER)
# ==============================================================================

class SeriesEngine:
    """Lõi khảo sát sự hội tụ của chuỗi số và khai triển Fourier."""

    @staticmethod
    def test_series_convergence(an_str: str, n_str: str = "n") -> Dict[str, Any]:
        """
        Khảo sát sự hội tụ chuỗi số: Điều kiện cần, tiêu chuẩn D'Alembert và Cauchy.
        """
        n = sp.Symbol(n_str, integer=True, positive=True)
        an = parse_higher_math_expr(an_str, local_vars={n_str: n})

        steps = [f"1. Chuỗi số có số hạng tổng quát a_{n_str} = {an}"]

        # Điều kiện cần: lim a_n khi n -> oo
        lim_an = sp.limit(an, n, sp.oo)
        steps.append(f"2. Kiểm tra điều kiện cần: lim(n->oo) a_n = {lim_an}")

        if lim_an != 0:
            steps.append("   => Do lim a_n ≠ 0 nên chuỗi PHÂN KỲ theo điều kiện cần.")
            return {
                "status": "SUCCESS",
                "convergent": False,
                "reason": "Điều kiện cần không thỏa mãn (lim a_n ≠ 0)",
                "steps": steps,
            }

        # Thử tiêu chuẩn tỷ số D'Alembert
        an_plus_1 = an.subs(n, n + 1)
        ratio = sp.simplify(sp.Abs(an_plus_1 / an))
        d_alembert_lim = sp.limit(ratio, n, sp.oo)
        steps.append(f"3. Tiêu chuẩn D'Alembert: D = lim |a_(n+1) / a_n| = {d_alembert_lim}")

        if d_alembert_lim < 1:
            steps.append("   => D < 1: Chuỗi HỘI TỤ TUYỆT ĐỐI theo tiêu chuẩn D'Alembert.")
            return {
                "status": "SUCCESS",
                "convergent": True,
                "test_used": "D'Alembert (Ratio Test)",
                "ratio_limit": d_alembert_lim,
                "steps": steps,
            }
        elif d_alembert_lim > 1:
            steps.append("   => D > 1: Chuỗi PHÂN KỲ theo tiêu chuẩn D'Alembert.")
            return {
                "status": "SUCCESS",
                "convergent": False,
                "test_used": "D'Alembert (Ratio Test)",
                "ratio_limit": d_alembert_lim,
                "steps": steps,
            }

        # Nếu D = 1, thử tiêu chuẩn căn số Cauchy
        root_expr = sp.simplify(sp.Abs(an) ** (1 / n))
        cauchy_lim = sp.limit(root_expr, n, sp.oo)
        steps.append(f"4. Tiêu chuẩn căn Cauchy: C = lim ⁿ√|a_n| = {cauchy_lim}")

        if cauchy_lim < 1:
            steps.append("   => C < 1: Chuỗi HỘI TỤ TUYỆT ĐỐI theo tiêu chuẩn Cauchy.")
            return {"status": "SUCCESS", "convergent": True, "test_used": "Cauchy Root Test", "steps": steps}
        elif cauchy_lim > 1:
            steps.append("   => C > 1: Chuỗi PHÂN KỲ theo tiêu chuẩn Cauchy.")
            return {"status": "SUCCESS", "convergent": False, "test_used": "Cauchy Root Test", "steps": steps}

        # Thử tính tổng chuỗi trực tiếp bằng SymPy
        try:
            total_sum = sp.summation(an, (n, 1, sp.oo))
            if total_sum.is_finite:
                steps.append(f"5. Tính tổng chuỗi trực tiếp: S = {total_sum} (Hội tụ)")
                return {"status": "SUCCESS", "convergent": True, "sum": total_sum, "steps": steps}
            else:
                steps.append(f"5. Chuỗi phân kỳ, tổng S = {total_sum}")
                return {"status": "SUCCESS", "convergent": False, "sum": total_sum, "steps": steps}
        except Exception:
            pass

        return {
            "status": "SUCCESS",
            "convergent": "UNDETERMINED",
            "message": "Các tiêu chuẩn cơ bản chưa đủ kết luận (D=1, C=1). Cần dùng tiêu chuẩn so sánh hoặc Raabe.",
            "steps": steps,
        }

    @staticmethod
    def compute_power_series_radius(an_str: str, n_str: str = "n", center_str: str = "0") -> Dict[str, Any]:
        """Tìm bán kính hội tụ R và khoảng hội tụ của chuỗi lũy thừa ∑ a_n (x - x_0)^n."""
        n = sp.Symbol(n_str, integer=True, positive=True)
        an = parse_higher_math_expr(an_str, local_vars={n_str: n})
        x0 = parse_higher_math_expr(center_str)

        # R = lim |a_n / a_{n+1}|
        an_plus_1 = an.subs(n, n + 1)
        ratio = sp.simplify(sp.Abs(an / an_plus_1))
        radius = sp.limit(ratio, n, sp.oo)

        steps = [
            f"1. Chuỗi lũy thừa có hệ số a_n = {an}, tâm khai triển x_0 = {x0}",
            f"2. Công thức D'Alembert tính bán kính hội tụ: R = lim(n->oo) |a_n / a_(n+1)|",
            f"3. Bán kính hội tụ: R = {radius}",
        ]

        if radius == sp.oo:
            steps.append(f"4. Chuỗi hội tụ trên toàn trục số thực: (-oo, +oo).")
        elif radius == 0:
            steps.append(f"4. Chuỗi chỉ hội tụ tại duy nhất điểm tâm x = {x0}.")
        else:
            steps.append(f"4. Khoảng hội tụ mở: ({x0 - radius}, {x0 + radius}).")

        return {
            "status": "SUCCESS",
            "radius": radius,
            "center": x0,
            "steps": steps,
        }

    @staticmethod
    def compute_fourier_series(
        expr_str: str,
        var_str: str = "x",
        period_L_str: str = "pi",
        terms: int = 3,
    ) -> Dict[str, Any]:
        """Khai triển chuỗi Fourier hàm tuần hoàn f(x) chu kỳ 2L trên [-L, L]."""
        x = sp.Symbol(var_str)
        L = parse_higher_math_expr(period_L_str, local_vars={var_str: x})
        expr = parse_higher_math_expr(expr_str, local_vars={var_str: x})

        # a_0 = 1/L ∫_{-L}^L f(x) dx
        a_0 = sp.simplify((1 / L) * sp.integrate(expr, (x, -L, L)))

        a_coeffs = []
        b_coeffs = []
        partial_sum = a_0 / 2

        steps = [
            f"1. Khai triển Fourier cho hàm f({var_str}) = {expr} trên [-{period_L_str}, {period_L_str}]",
            f"2. Hệ số a_0 = (1/L) ∫ f(x) dx = {a_0}",
            f"3. Các hệ số điều hòa a_n và b_n (tính {terms} số hạng đầu):",
        ]

        for k in range(1, terms + 1):
            ak = sp.simplify((1 / L) * sp.integrate(expr * sp.cos(k * sp.pi * x / L), (x, -L, L)))
            bk = sp.simplify((1 / L) * sp.integrate(expr * sp.sin(k * sp.pi * x / L), (x, -L, L)))
            a_coeffs.append(ak)
            b_coeffs.append(bk)
            partial_sum += ak * sp.cos(k * sp.pi * x / L) + bk * sp.sin(k * sp.pi * x / L)
            steps.append(f"   • n = {k}: a_{k} = {ak},  b_{k} = {bk}")

        steps.append(f"4. Đa thức Fourier tổng riêng cấp {terms}:")
        steps.append(f"   S_{terms}({var_str}) = {partial_sum}")

        return {
            "status": "SUCCESS",
            "a_0": a_0,
            "a_coefficients": a_coeffs,
            "b_coefficients": b_coeffs,
            "partial_sum": partial_sum,
            "steps": steps,
            "latex": sp.latex(partial_sum),
        }


# ==============================================================================
# PHÂN HỆ 4: GIẢI TÍCH ĐA BIẾN & TÍCH PHÂN BỘI (MULTIVARIABLE CALCULUS)
# ==============================================================================

class MultivariableEngine:
    """Lõi Đạo hàm riêng, Ma trận Hessian, Cực trị tự do/Lagrange và Tích phân bội."""

    @staticmethod
    def compute_partial_derivatives(expr_str: str, vars_str: str = "x, y") -> Dict[str, Any]:
        """Tính đạo hàm riêng cấp 1, cấp 2, vi phân toàn phần df và ma trận Hessian."""
        var_names = [v.strip() for v in vars_str.split(",") if v.strip()]
        symbols = [sp.Symbol(v) for v in var_names]
        local_dict = {v: s for v, s in zip(var_names, symbols)}
        expr = parse_higher_math_expr(expr_str, local_vars=local_dict)

        grad_list = [sp.diff(expr, s) for s in symbols]
        gradient_dict = {f"d/d{v}": g for v, g in zip(var_names, grad_list)}

        # Ma trận Hessian
        hessian_mat = sp.hessian(expr, symbols)

        steps = [
            f"1. Hàm nhiều biến f({', '.join(var_names)}) = {expr}",
            f"2. Vectơ Gradient ∇f:",
        ]
        for v, g in gradient_dict.items():
            steps.append(f"   • {v} = {g}")

        steps.append("3. Ma trận Hessian H(f):")
        steps.append(format_matrix_plain(hessian_mat))

        # Vi phân toàn phần df
        df_str = " + ".join([f"({g}) d{v}" for v, g in zip(var_names, grad_list)])
        steps.append(f"4. Vi phân toàn phần cấp 1: df = {df_str}")

        return {
            "status": "SUCCESS",
            "gradient": gradient_dict,
            "hessian": hessian_mat,
            "df_expression": df_str,
            "steps": steps,
        }

    @staticmethod
    def find_local_extrema_2vars(expr_str: str, vars_str: str = "x, y") -> Dict[str, Any]:
        """
        Tìm cực trị tự do hàm 2 biến z = f(x, y): Điểm dừng, ma trận Hessian và kết luận.
        """
        var_names = [v.strip() for v in vars_str.split(",") if v.strip()]
        if len(var_names) != 2:
            raise HigherMathKernelError("Hàm tìm cực trị 2 biến yêu cầu đúng 2 biến số (vd: 'x, y').")

        x, y = sp.Symbol(var_names[0]), sp.Symbol(var_names[1])
        expr = parse_higher_math_expr(expr_str, local_vars={var_names[0]: x, var_names[1]: y})

        fx = sp.diff(expr, x)
        fy = sp.diff(expr, y)
        fxx = sp.diff(fx, x)
        fxy = sp.diff(fx, y)
        fyy = sp.diff(fy, y)

        steps = [
            f"1. Hàm số z = f({x}, {y}) = {expr}",
            f"2. Đạo hàm riêng cấp 1: z'_x = {fx}, z'_y = {fy}",
            f"3. Giải hệ điểm dừng z'_x = 0, z'_y = 0:",
        ]

        crit_points = sp.solve([fx, fy], (x, y), dict=True)
        stationary_results = []

        if not crit_points:
            steps.append("   => Hệ không có nghiệm thực => Hàm số KHÔNG có điểm dừng.")
            return {"status": "SUCCESS", "points": [], "steps": steps}

        for idx, pt in enumerate(crit_points):
            x_val, y_val = pt[x], pt[y]
            # Bỏ qua nghiệm phức
            if not (x_val.is_real and y_val.is_real):
                continue

            A_val = fxx.subs({x: x_val, y: y_val})
            B_val = fxy.subs({x: x_val, y: y_val})
            C_val = fyy.subs({x: x_val, y: y_val})
            # Biệt thức Hessian Delta = AC - B^2
            delta = sp.simplify(A_val * C_val - B_val ** 2)
            z_val = expr.subs({x: x_val, y: y_val})

            point_desc = f"M_{idx+1}({x_val}, {y_val})"
            steps.append(f"   • Xét điểm dừng {point_desc}: A = {A_val}, B = {B_val}, C = {C_val} => Δ = AC - B² = {delta}")

            conclusion = "KHÔNG XÁC ĐỊNH (Δ = 0)"
            if delta > 0:
                if A_val > 0:
                    conclusion = "CỰC TIỂU ĐỊA PHƯƠNG (Local Minimum)"
                    steps.append(f"     Do Δ > 0 và A > 0 => {point_desc} là điểm CỰC TIỂU, z_min = {z_val}")
                else:
                    conclusion = "CỰC ĐẠI ĐỊA PHƯƠNG (Local Maximum)"
                    steps.append(f"     Do Δ > 0 và A < 0 => {point_desc} là điểm CỰC ĐẠI, z_max = {z_val}")
            elif delta < 0:
                conclusion = "ĐIỂM YÊN NGỰA (Saddle Point - Không là cực trị)"
                steps.append(f"     Do Δ < 0 => {point_desc} là ĐIỂM YÊN NGỰA.")

            stationary_results.append({
                "point": (x_val, y_val),
                "z_value": z_val,
                "A": A_val,
                "B": B_val,
                "C": C_val,
                "delta": delta,
                "type": conclusion,
            })

        return {
            "status": "SUCCESS",
            "critical_points": stationary_results,
            "steps": steps,
        }

    @staticmethod
    def solve_lagrange_multipliers(
        obj_expr_str: str,
        constraint_str: str,
        vars_str: str = "x, y",
    ) -> Dict[str, Any]:
        """
        Tìm cực trị có điều kiện bằng phương pháp nhân tử Lagrange:
        Hàm mục tiêu f(x, y), điều kiện ràng buộc g(x, y) = 0.
        """
        var_names = [v.strip() for v in vars_str.split(",") if v.strip()]
        symbols = [sp.Symbol(v) for v in var_names]
        lam = sp.Symbol("lambda")
        local_dict = {v: s for v, s in zip(var_names, symbols)}

        f_expr = parse_higher_math_expr(obj_expr_str, local_vars=local_dict)

        # Xử lý chuỗi điều kiện g(x, y) = c hoặc g(x, y)
        if "=" in constraint_str:
            lhs_s, rhs_s = constraint_str.split("=")
            g_expr = parse_higher_math_expr(lhs_s, local_vars=local_dict) - parse_higher_math_expr(
                rhs_s, local_vars=local_dict
            )
        else:
            g_expr = parse_higher_math_expr(constraint_str, local_vars=local_dict)

        # Hàm Lagrange: L = f - λ * g
        L = f_expr - lam * g_expr
        grad_L = [sp.diff(L, s) for s in symbols] + [sp.diff(L, lam)]

        steps = [
            f"1. Hàm mục tiêu f({', '.join(var_names)}) = {f_expr}",
            f"2. Điều kiện ràng buộc g = {g_expr} = 0",
            f"3. Lập hàm Lagrange: L = f - λ·g = {L}",
            f"4. Thiết lập hệ phương trình điểm dừng ∇L = 0:",
        ]
        for eq_part in grad_L:
            steps.append(f"   • {eq_part} = 0")

        all_syms = symbols + [lam]
        solutions = sp.solve(grad_L, all_syms, dict=True)

        results = []
        steps.append("5. Giải hệ tìm các điểm dừng Lagrange (x, y, λ):")
        for idx, sol in enumerate(solutions):
            pt_coords = {str(s): sol[s] for s in symbols}
            lam_val = sol[lam]
            val_f = f_expr.subs(sol)
            results.append({
                "point": pt_coords,
                "lambda": lam_val,
                "f_value": val_f,
            })
            coord_str = ", ".join(f"{k} = {v}" for k, v in pt_coords.items())
            steps.append(f"   • Điểm {idx+1}: ({coord_str}) với λ = {lam_val} => Giá trị f = {val_f}")

        return {
            "status": "SUCCESS",
            "lagrange_function": L,
            "solutions": results,
            "steps": steps,
        }

    @staticmethod
    def compute_double_integral(
        expr_str: str,
        inner_var: str,
        inner_lower: str,
        inner_upper: str,
        outer_var: str,
        outer_lower: str,
        outer_upper: str,
    ) -> Dict[str, Any]:
        """
        Tính tích phân kép ∬_D f(x, y) dy dx theo thứ tự tích phân lặp.
        """
        x_sym = sp.Symbol(outer_var)
        y_sym = sp.Symbol(inner_var)
        local_dict = {outer_var: x_sym, inner_var: y_sym}

        expr = parse_higher_math_expr(expr_str, local_vars=local_dict)
        y1 = parse_higher_math_expr(inner_lower, local_vars=local_dict)
        y2 = parse_higher_math_expr(inner_upper, local_vars=local_dict)
        x1 = parse_higher_math_expr(outer_lower, local_vars=local_dict)
        x2 = parse_higher_math_expr(outer_upper, local_vars=local_dict)

        steps = [
            f"1. Tích phân kép: I = ∫[{x1} đến {x2}] d{outer_var} ∫[{y1} đến {y2}] ({expr}) d{inner_var}",
        ]

        # Tích phân lớp trong theo y_sym
        inner_res = sp.integrate(expr, (y_sym, y1, y2))
        steps.append(f"2. Kết quả tích phân lớp trong theo {inner_var}:")
        steps.append(f"   Inner({outer_var}) = {inner_res}")

        # Tích phân lớp ngoài theo x_sym
        final_res = sp.integrate(inner_res, (x_sym, x1, x2))
        steps.append(f"3. Kết quả tích phân lớp ngoài theo {outer_var}:")
        steps.append(f"   I = {final_res}")

        return {
            "status": "SUCCESS",
            "value": final_res,
            "inner_integral": inner_res,
            "steps": steps,
            "latex": f"\\int_{{{sp.latex(x1)}}}^{{{sp.latex(x2)}}} d{outer_var} \\int_{{{sp.latex(y1)}}}^{{{sp.latex(y2)}}} {sp.latex(expr)}\\, d{inner_var} = {sp.latex(final_res)}",
        }


# ==============================================================================
# PHÂN HỆ 5: TÍCH PHÂN ĐƯỜNG - MẶT & LÝ THUYẾT TRƯỜNG (FIELD THEORY)
# ==============================================================================

class FieldTheoryEngine:
    """Lõi Toán tử vi phân Vector (Grad, Div, Curl), Tích phân đường/mặt và Trường thế."""

    @staticmethod
    def analyze_vector_field(
        P_str: str,
        Q_str: str,
        R_str: Optional[str] = None,
        vars_str: str = "x, y, z",
    ) -> Dict[str, Any]:
        """
        Tính Div, Curl của trường vector F = (P, Q, R), kiểm tra trường thế và tìm hàm thế vị U.
        """
        x, y, z = sp.symbols("x y z")
        local_dict = {"x": x, "y": y, "z": z}

        P = parse_higher_math_expr(P_str, local_vars=local_dict)
        Q = parse_higher_math_expr(Q_str, local_vars=local_dict)
        R = parse_higher_math_expr(R_str, local_vars=local_dict) if R_str else sp.Integer(0)

        steps = [
            f"1. Trường vector F = ({P}) i + ({Q}) j + ({R}) k",
        ]

        # Divergence: div F = dP/dx + dQ/dy + dR/dz
        div_F = sp.diff(P, x) + sp.diff(Q, y) + sp.diff(R, z)
        steps.append(f"2. Độ phân kỳ Divergence: div(F) = ∇ · F = {div_F}")

        # Curl / Rotor: rot F = (dR/dy - dQ/dz) i + (dP/dz - dR/dx) j + (dQ/dx - dP/dy) k
        curl_x = sp.diff(R, y) - sp.diff(Q, z)
        curl_y = sp.diff(P, z) - sp.diff(R, x)
        curl_z = sp.diff(Q, x) - sp.diff(P, y)
        curl_F = (curl_x, curl_y, curl_z)
        steps.append(f"3. Vectơ xoáy Rotor: rot(F) = ∇ × F = ({curl_x}, {curl_y}, {curl_z})")

        # Kiểm tra trường thế (Conservative Field): rot F = 0
        is_conservative = (curl_x == 0 and curl_y == 0 and curl_z == 0)
        potential_U = None

        if is_conservative:
            steps.append("4. Do rot(F) = (0, 0, 0) => F là TRƯỜNG THẾ (Conservative Vector Field).")
            # Tìm hàm thế vị U sao cho dU/dx = P, dU/dy = Q, dU/dz = R
            # U = ∫ P dx + C(y, z)
            U1 = sp.integrate(P, x)
            diff_y = sp.diff(U1, y)
            C_y = sp.integrate(Q - diff_y, y)
            U2 = U1 + C_y
            diff_z = sp.diff(U2, z)
            C_z = sp.integrate(R - diff_z, z)
            potential_U = sp.simplify(U2 + C_z)
            steps.append(f"5. Hàm thế vị tương ứng U(x, y, z) sao cho ∇U = F:")
            steps.append(f"   U(x, y, z) = {potential_U} + C")
        else:
            steps.append("4. Do rot(F) ≠ 0 => F KHÔNG PHẢI là trường thế (công phụ thuộc đường đi).")

        return {
            "status": "SUCCESS",
            "divergence": div_F,
            "curl": curl_F,
            "is_conservative": is_conservative,
            "potential_function": potential_U,
            "steps": steps,
        }


# ==============================================================================
# PHÂN HỆ 6: PHƯƠNG TRÌNH VI PHÂN & BIẾN ĐỔI LAPLACE (ODEs & LAPLACE)
# ==============================================================================

class DifferentialEquationsEngine:
    """Lõi Giải phương trình vi phân cấp 1, cấp 2 hệ số hằng và Biến đổi Laplace."""

    @staticmethod
    def solve_ode(
        eq_str: str,
        y_str: str = "y",
        x_str: str = "x",
        ics_dict: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Giải phương trình vi phân cấp 1 & cấp 2 hệ số hằng bằng SymPy dsolve.
        Hỗ trợ:
          - y' + 2*y = exp(x)
          - y'' - 3*y' + 2*y = sin(x)
          - Kèm điều kiện đầu: y(0)=1, y'(0)=2
        """
        x = sp.Symbol(x_str)
        y_func = sp.Function(y_str)(x)

        # Chuyển đổi ký hiệu đạo hàm: y'' -> diff(y, x, 2), y' -> diff(y, x)
        cleaned = eq_str.strip()
        cleaned = cleaned.replace("y''", f"Derivative({y_str}({x_str}), {x_str}, 2)")
        cleaned = cleaned.replace("y'", f"Derivative({y_str}({x_str}), {x_str})")
        # Thay thế y đơn lẻ (không đi kèm ngoặc) thành y(x)
        cleaned = re.sub(rf"\b{y_str}\b(?!\s*\()", f"{y_str}({x_str})", cleaned)

        local_dict = {
            x_str: x,
            y_str: sp.Function(y_str),
            "Derivative": sp.Derivative,
            "exp": sp.exp,
            "sin": sp.sin,
            "cos": sp.cos,
        }

        if "=" in cleaned:
            lhs_s, rhs_s = cleaned.split("=")
            lhs = parse_higher_math_expr(lhs_s, local_vars=local_dict)
            rhs = parse_higher_math_expr(rhs_s, local_vars=local_dict)
            ode_eq = sp.Eq(lhs, rhs)
        else:
            expr = parse_higher_math_expr(cleaned, local_vars=local_dict)
            ode_eq = sp.Eq(expr, 0)

        steps = [
            f"1. Phương trình vi phân cần giải: {ode_eq}",
        ]

        # Giải bằng dsolve
        try:
            # Xử lý điều kiện ban đầu nếu có
            ics = None
            if ics_dict:
                ics = {}
                for k, v in ics_dict.items():
                    # k có thể là "y(0)" hoặc "y'(0)"
                    val = parse_higher_math_expr(str(v))
                    if "'" in k:
                        ics[y_func.diff(x).subs(x, 0)] = val
                    else:
                        ics[y_func.subs(x, 0)] = val

            solution = sp.dsolve(ode_eq, y_func, ics=ics)
            steps.append(f"2. Nghiệm của phương trình vi phân:")
            steps.append(f"   {solution}")

            return {
                "status": "SUCCESS",
                "solution": solution,
                "steps": steps,
                "latex": sp.latex(solution),
            }
        except Exception as exc:
            raise HigherMathKernelError(f"Không thể giải phương trình vi phân: {exc}")

    @staticmethod
    def compute_laplace(
        expr_str: str,
        t_str: str = "t",
        s_str: str = "s",
        mode: str = "forward",
    ) -> Dict[str, Any]:
        """
        Biến đổi Laplace thuận L{f(t)} = F(s) hoặc Laplace nghịch L^(-1){F(s)} = f(t).
        """
        t = sp.Symbol(t_str, positive=True)
        s = sp.Symbol(s_str)
        local_dict = {t_str: t, s_str: s}

        expr = parse_higher_math_expr(expr_str, local_vars=local_dict)

        if mode == "forward":
            res = sp.laplace_transform(expr, t, s, noconds=True)
            steps = [
                f"1. Biến đổi Laplace thuận: L{{{expr}}} với t > 0",
                f"2. Kết quả ảnh trong miền tần số s: F(s) = {res}",
            ]
            latex_str = f"\\mathcal{{L}}\\left\\{{{sp.latex(expr)}\\right\\}} = {sp.latex(res)}"
        else:
            res = sp.inverse_laplace_transform(expr, s, t)
            steps = [
                f"1. Biến đổi Laplace ngược: L^(-1){{{expr}}}",
                f"2. Kết quả hàm gốc theo thời gian t: f(t) = {res}",
            ]
            latex_str = f"\\mathcal{{L}}^{{-1}}\\left\\{{{sp.latex(expr)}\\right\\}} = {sp.latex(res)}"

        return {
            "status": "SUCCESS",
            "result": res,
            "steps": steps,
            "latex": latex_str,
        }
