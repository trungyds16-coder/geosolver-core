"""
CAD Math Studio - Module Giải thuật Lõi (CADMathCore)
Phiên bản: 2.2.0-RC5 (Release Candidate 5 - Bản Chung Khảo Toàn Diện)

Bao gồm:
- DiophantineCategory: Enum định nghĩa các trạng thái cấu trúc đạt tới được và dự phòng.
- clean_display_expr: Chuẩn hóa chuỗi biểu thức SymPy.
- matrix_multiply: Nhân hai ma trận kèm kiểm tra tương thích kích thước (m x k) * (k x n).
- compute_matrix_inverse: Tính ma trận nghịch đảo qua adjugate, hỗ trợ ma trận exact (không dùng float tolerance),
  ma trận số thực với dung sai tương đối dựa trên cận Hadamard (Hadamard bound), và ma trận ký hiệu 3-valued guard.
- CADMathCore:
  + real_status: Xác định tính thực/phức.
  + check_sign_exact: Xác định dấu đại số ký hiệu và số học đa độ chính xác.
  + solve_radical_pedagogical: Giải phương trình vô tỷ 4 bước sư phạm, xử lý hằng đẳng thức f-g^2=0 (trả về Set/Interval
    nếu có nghiệm thực, trả về [] nếu miền rỗng), lưới an toàn ưu tiên đối soát giải tích chính xác.
  + solve_underdetermined_or_diophantine: Phân tích cấu trúc hệ phương trình vô định tuyến tính và giải Diophantine d=1
    bằng tham số affine + solve_congruence, đếm nghiệm bằng công thức đóng O(1) chống treo hệ thống với số lớn (10^9),
    phân biệt chuẩn xác giữa INFEASIBLE_BOUNDS_EMPTY và INFEASIBLE_NO_INTEGER_POINTS.
"""

import re
import math
from enum import Enum
import sympy as sp
from sympy.ntheory.modular import solve_congruence


class DiophantineCategory(str, Enum):
    INCONSISTENT = "INCONSISTENT"
    UNIQUE = "UNIQUE"
    EMPTY_NO_POSITIVE_INTEGER = "EMPTY_NO_POSITIVE_INTEGER"
    UNSUPPORTED_DIM_GE_2 = "UNSUPPORTED_DIM>=2"
    UNSUPPORTED_NON_INTEGER = "UNSUPPORTED_NON_INTEGER"
    INFEASIBLE_BOUNDS_EMPTY = "INFEASIBLE_BOUNDS_EMPTY"
    INFEASIBLE_NO_INTEGER_POINTS = "INFEASIBLE_NO_INTEGER_POINTS"
    FINITE_BOUNDED = "FINITE_BOUNDED"
    UNBOUNDED_INFINITE = "UNBOUNDED_INFINITE"
    UNKNOWN = "UNKNOWN"


def clean_display_expr(expr):
    """Làm sạch định dạng chuỗi biểu thức SymPy để hiển thị trực quan."""
    s = str(expr)
    s = s.replace("**", "^").replace("*", " ")
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def matrix_multiply(A: sp.Matrix, B: sp.Matrix) -> sp.Matrix:
    """
    Nhân hai ma trận với kiểm tra điều kiện tương thích kích thước nghiêm ngặt (m x k) * (k x n).
    Raise ValueError nếu kích thước không khớp.
    """
    if not isinstance(A, sp.Matrix) or not isinstance(B, sp.Matrix):
        A = sp.Matrix(A)
        B = sp.Matrix(B)
    if A.cols != B.rows:
        raise ValueError(
            f"Kích thước ma trận không tương thích để nhân: Ma trận A ({A.rows}x{A.cols}) "
            f"không thể nhân với Ma trận B ({B.rows}x{B.cols}) vì số cột của A ({A.cols}) "
            f"khác số hàng của B ({B.rows})!"
        )
    return A * B


def compute_matrix_inverse(A: sp.Matrix):
    """
    Tính ma trận nghịch đảo qua adjugate matrix:
    1. Ma trận số nguyên / hữu tỷ chính xác (Exact): Tuyệt đối không dùng dung sai float.
       Khả nghịch khi và chỉ khi det(A) != 0.
    2. Ma trận số thực (Floating-Point): Áp dụng dung sai tương đối dựa trên cận Hadamard (Hadamard bound).
       Tránh báo suy biến sai cho ma trận thang đo lệch như diag(1.0, 1e-13).
    3. Ma trận ký hiệu (Symbolic): Hỗ trợ 3-valued guard khi det(A) phụ thuộc tham số tự do.
    """
    if not isinstance(A, sp.Matrix):
        A = sp.Matrix(A)

    if A.rows != A.cols:
        raise ValueError("Chỉ ma trận vuông (n x n) mới có ma trận nghịch đảo!")

    detA = A.det()

    # 1. Kiểm tra suy biến đại số chính xác hoặc rút gọn ký hiệu bằng 0
    is_singular = False
    if hasattr(detA, "is_zero") and detA.is_zero is True:
        is_singular = True
    elif sp.simplify(detA) == 0:
        is_singular = True

    # 2. Kiểm tra dung sai số học CHỈ KHI ma trận hoặc định thức thực sự chứa sp.Float hoặc float
    has_float = any(elem.has(sp.Float) or isinstance(elem, float) for elem in A) or detA.has(sp.Float)
    if not is_singular and has_float:
        try:
            # Cận Hadamard: Tích độ dài vector hàng
            hadamard_bound = 1.0
            for r_idx in range(A.rows):
                row_norm_sq = sum(float(elem.evalf())**2 for elem in A.row(r_idx))
                hadamard_bound *= math.sqrt(row_norm_sq) or 1.0
            
            det_val = abs(float(detA.evalf()))
            if det_val < 1e-12 * hadamard_bound:
                is_singular = True
        except Exception:
            pass

    if is_singular:
        return {
            "invertible": False,
            "det": detA,
            "desc": f"Ma trận suy biến (Singular Matrix), không khả nghịch vì det(A) = {clean_display_expr(detA)}."
        }

    # 3. Guard 3 giá trị (3-valued logic): Khi det(A) phụ thuộc tham số
    if getattr(detA, "is_zero", None) is None and len(detA.free_symbols) > 0:
        adjA = A.adjugate()
        return {
            "invertible": None,
            "det": detA,
            "adjugate": adjA,
            "inverse": adjA / detA,
            "desc": "Tính khả nghịch phụ thuộc tham số (Singularity undecidable trên toàn miền; khả nghịch khi det(A) ≠ 0)."
        }

    adjA = A.adjugate()
    invA = adjA / detA
    return {
        "invertible": True,
        "det": detA,
        "adjugate": adjA,
        "inverse": invA
    }


class CADMathCore:
    def __init__(self, listener=None):
        self.listener = listener
        self.last_dioph_category = None
        self.last_dioph_solutions = []
        self.last_dioph_n_total = 0

    def _notify(self, event_type, data):
        if self.listener is not None and callable(self.listener):
            try:
                self.listener(event_type, data)
            except Exception:
                pass

    @staticmethod
    def real_status(r):
        """Xác định nghiệm r là thực (True), phức (False) hay chưa kết luận (None)."""
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

    @staticmethod
    def check_sign_exact(expr_sub):
        """
        Xác định dấu của biểu thức kết hợp đại số ký hiệu và số học đa độ chính xác.
        """
        if expr_sub in (sp.zoo, sp.nan) or (hasattr(expr_sub, "has") and expr_sub.has(sp.zoo, sp.nan)):
            return 'nonreal'
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
                if float(s) > 0:
                    return 'pos'
                elif float(s) < 0:
                    return 'neg'
                else:
                    return 'zero'
        except Exception:
            pass
        try:
            val = float(sp.N(expr_s, 40))
            if abs(val) > 1e-30:
                return 'pos' if val > 0 else 'neg'
        except Exception:
            pass
        return 'unknown'

    def solve_radical_pedagogical(self, target_eq, x):
        """
        Giải phương trình vô tỷ dạng c*sqrt(f(x)) + h(x) = 0 qua 4 bước sư phạm chuẩn.
        - Trả về: (steps, valid_sols, rejected_sols, indeterminate_sols)
        - Khi hằng đẳng thức f - g^2 = 0: Nếu miền g(x) >= 0 khác rỗng, trả [domain_sol]; nếu rỗng, trả [].
        """
        if isinstance(target_eq, sp.Eq):
            target_eq = target_eq.lhs - target_eq.rhs

        steps = []
        expanded = sp.expand(target_eq)
        rads = [t for t in expanded.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
        if len(rads) != 1:
            rads = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
        if len(rads) != 1:
            return ["Bước 1: Ngoài phạm vi hỗ trợ: Hệ thống hiện tại chuyên biệt cho phương trình chứa đúng 1 căn thức."], [], [], []

        rad = rads[0]
        c = expanded.coeff(rad)
        rest = sp.expand(expanded - c * rad)

        # Validate hệ số c: phải là số thực hằng khác 0
        if c == 0 or c.free_symbols or (hasattr(c, "is_real") and c.is_real is False) or any(t.exp == sp.Rational(1, 2) for t in rest.atoms(sp.Pow)):
            return ["Bước 1: Ngoài phạm vi hỗ trợ: Dạng căn thức phi tuyến, phức hoặc không cô lập được."], [], [], []

        # Chuẩn hóa về dạng chính tắc: sqrt(f) = gx với hệ số căn = 1
        gx = sp.simplify(-rest / c)
        fx = rad.base

        steps.append("Bước 1: Xác định điều kiện có nghĩa và điều kiện vế phải")
        steps.append(f"  • Đưa phương trình về dạng chuẩn tắc: √({clean_display_expr(fx)}) = {clean_display_expr(gx)}")

        # 1. Điều kiện xác định căn thức f(x) >= 0
        if not fx.free_symbols:
            try:
                f_const = float(fx.evalf())
                if f_const >= 0:
                    steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0 (Luôn thỏa mãn với mọi x ∈ ℝ).")
                else:
                    steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0 (Không tồn tại x thỏa mãn).")
            except Exception:
                steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
        else:
            steps.append(f"  • Điều kiện xác định căn thức: {clean_display_expr(fx)} >= 0")
            try:
                cond_fx = sp.solve_univariate_inequality(fx >= 0, x, relational=False)
                steps.append(f"    ==> Miền D_rad: {cond_fx}")
            except Exception:
                pass

        # 2. Điều kiện vế phải g(x) >= 0 (Có kiểm tra early-exit nếu hằng số âm)
        if not gx.free_symbols:
            try:
                g_const = float(gx.evalf())
                if g_const >= 0:
                    steps.append(f"  • Điều kiện vế phải (g(x) = {clean_display_expr(gx)} >= 0): Luôn thỏa mãn với mọi x ∈ ℝ.")
                else:
                    steps.append(f"  • Điều kiện vế phải (g(x) = {clean_display_expr(gx)} < 0): Không tồn tại x thỏa mãn.")
                    steps.append(f"  • Nhận xét sư phạm: Vế trái √({clean_display_expr(fx)}) >= 0 với mọi x thuộc D_rad, nhưng vế phải g(x) = {clean_display_expr(gx)} < 0.")
                    steps.append("  • Mâu thuẫn dấu đại số: Phương trình vô nghiệm trên ℝ (S = ∅).")
                    self._notify('radical_result', {'steps': steps, 'valid': [], 'rejected': [], 'indeterminate': []})
                    return steps, [], [], []
            except Exception:
                steps.append(f"  • Điều kiện vế phải: {clean_display_expr(gx)} >= 0")
        else:
            steps.append(f"  • Điều kiện vế phải (Do √({clean_display_expr(fx)}) >= 0 nên bắt buộc g(x) >= 0): {clean_display_expr(gx)} >= 0")
            try:
                cond_gx = sp.solve_univariate_inequality(gx >= 0, x, relational=False)
                steps.append(f"    ==> Miền D_sign: {cond_gx}")
            except Exception:
                pass

        steps.append("Bước 2: Bình phương hai vế tìm tập nghiệm đại số sơ bộ")
        steps.append(f"  • ({clean_display_expr(rad)})² = ({clean_display_expr(gx)})²")
        poly_eq = sp.simplify(fx - gx**2)

        # Xử lý trường hợp đặc biệt: Bình phương thành hằng đẳng thức f(x) - [g(x)]^2 = 0
        if poly_eq == 0 or getattr(poly_eq, "is_zero", False):
            steps.append(f"  <=> {clean_display_expr(poly_eq)} = 0 (Phương trình hệ quả là đồng nhất thức 0 = 0).")
            steps.append("  • Nhận xét đại số: Biểu thức dưới căn f(x) đồng nhất bằng [g(x)]².")
            steps.append("  • Do đó, phương trình nghiệm đúng với mọi x thỏa mãn điều kiện vế phải g(x) >= 0 (khi đó f(x) = [g(x)]² >= 0 tự động thỏa mãn).")
            
            # P1-2 & P1-7: Giải bất phương trình g(x) >= 0
            try:
                domain_sol = sp.solve_univariate_inequality(gx >= 0, x, relational=False)
            except Exception:
                try:
                    domain_sol = sp.solveset(gx >= 0, x, domain=sp.S.Reals)
                except Exception:
                    domain_sol = sp.ConditionSet(x, gx >= 0, sp.S.Reals)

            # Kiểm tra miền rỗng (P1-7)
            if domain_sol is sp.S.EmptySet or getattr(domain_sol, "is_empty", False):
                steps.append("  • Không có giá trị x nào thỏa mãn điều kiện vế phải g(x) >= 0.")
                steps.append("Bước 3: Đối soát điều kiện xác định")
                steps.append("Bước 4: Kết luận tập nghiệm")
                steps.append("  ==> Phương trình vô nghiệm trên ℝ (S = ∅).")
                self._notify('radical_result', {'steps': steps, 'valid': [], 'rejected': [], 'indeterminate': []})
                return steps, [], [], []

            steps.append(f"  ==> Miền nghiệm đúng: {domain_sol}")
            steps.append("Bước 3: Đối soát điều kiện xác định")
            steps.append("  • Với mọi x thỏa mãn g(x) >= 0, f(x) = [g(x)]² >= 0 nên căn thức luôn có nghĩa và hai vế bằng nhau.")
            steps.append("Bước 4: Kết luận tập nghiệm")
            steps.append(f"  ==> Tập nghiệm: S = {{ x ∈ ℝ | {clean_display_expr(gx)} >= 0 }} = {domain_sol}")
            self._notify('radical_result', {'steps': steps, 'valid': [domain_sol], 'rejected': [], 'indeterminate': []})
            return steps, [domain_sol], [], []

        steps.append(f"  <=> {clean_display_expr(poly_eq)} = 0")
        raw_sols = sp.solve(poly_eq, x)
        steps.append(f"  • Nghiệm đại số sơ bộ từ phương trình hệ quả: {raw_sols}")

        steps.append("Bước 3: Xác định dấu đại số chính xác và loại bỏ nghiệm ngoại lai")
        valid_sols = []
        rejected_sols = []
        indeterminate_sols = []

        for r in raw_sols:
            r_st = self.real_status(r)
            if r_st is False:
                rejected_sols.append((r, "Nghiệm phức không thuộc tập số thực ℝ"))
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Loại bỏ (Nghiệm phức, Im(r) ≠ 0).")
                continue

            s_gx = self.check_sign_exact(gx.subs(x, r))
            s_fx = self.check_sign_exact(fx.subs(x, r))

            if s_gx == 'neg':
                rejected_sols.append((r, f"Vi phạm điều kiện vế phải g({clean_display_expr(r)}) < 0"))
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Loại bỏ (Nghiệm ngoại lai do vế phải g(r) < 0).")
            elif s_fx == 'neg':
                rejected_sols.append((r, f"Vi phạm điều kiện xác định căn thức f({clean_display_expr(r)}) < 0"))
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Loại bỏ (f(r) < 0 vi phạm điều kiện có nghĩa).")
            elif s_gx in ['pos', 'zero'] and s_fx in ['pos', 'zero']:
                # Lưới an toàn: ưu tiên kiểm tra giải tích chính xác tuyệt đối (Exact Verification)
                is_exact_valid = False
                try:
                    exact_sub = sp.simplify(target_eq.subs(x, r))
                    if exact_sub == 0:
                        is_exact_valid = True
                except Exception:
                    pass

                if not is_exact_valid:
                    try:
                        val_check = abs(sp.N(target_eq.subs(x, r), 40))
                        if val_check > sp.Float('1e-20'):
                            rejected_sols.append((r, f"Thay ngược không triệt tiêu phương trình gốc (|VT-VP| = {val_check:.2e})"))
                            steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Loại bỏ (Lưới an toàn thay ngược 40 chữ số vi phạm: |VT - VP| = {val_check:.2e} > 1e-20).")
                            continue
                    except Exception:
                        indeterminate_sols.append((r, "Lỗi số học khi đối soát lưới thay ngược"))
                        steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Lỗi số học khi đối soát ==> Chuyển sang indeterminate.")
                        continue

                valid_sols.append(r)
                val_approx = None
                try:
                    if not r.is_Integer:
                        val_approx = f"{float(sp.N(r, 6)):.4f}"
                except Exception:
                    pass
                approx_str = f" (≈ {val_approx})" if val_approx else ""
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}{approx_str}: Thỏa mãn cả D_rad và D_sign ==> Nhận.")
            else:
                indeterminate_sols.append((r, f"g:{s_gx}, f:{s_fx}"))
                steps.append(f"  • Nghiệm r = {clean_display_expr(r)}: Dấu đại số chưa quyết định chắc chắn (g:{s_gx}, f:{s_fx}) ==> Cần kiểm tra giải tích nâng cao.")

        # BƯỚC 4: KẾT LUẬN TẬP NGHIỆM S
        steps.append("Bước 4: Kết luận tập nghiệm")
        if indeterminate_sols:
            indet_strs = [clean_display_expr(r) for r, _ in indeterminate_sols]
            steps.append(f"  ==> CHƯA THỂ KẾT LUẬN ĐẦY ĐỦ: Phát hiện {len(indeterminate_sols)} nghiệm chưa xác định được dấu đại số ({', '.join(indet_strs)}).")
        elif not valid_sols:
            steps.append("  ==> Phương trình vô nghiệm trên ℝ (S = ∅).")
        else:
            sol_items = []
            for r in valid_sols:
                val_approx = None
                try:
                    if not r.is_Integer:
                        val_approx = f"{float(sp.N(r, 6)):.4f}"
                except Exception:
                    pass
                if val_approx:
                    sol_items.append(f"{clean_display_expr(r)} (≈ {val_approx})")
                else:
                    sol_items.append(f"{clean_display_expr(r)}")
            steps.append(f"  ==> Tập nghiệm hợp lệ: S = {{ {', '.join(sol_items)} }}")

        self._notify('radical_result', {'steps': steps, 'valid': valid_sols, 'rejected': rejected_sols, 'indeterminate': indeterminate_sols})
        return steps, valid_sols, rejected_sols, indeterminate_sols

    def solve_underdetermined_or_diophantine(self, eq_syms, vars_sorted, lines=None):
        """
        Bộ giải Diophantine tuyến tính d=1 và phân loại cấu trúc hệ vô định.
        Sử dụng phân tích tham số affine và hệ đồng dư solve_congruence.
        - Đếm nghiệm bằng công thức đóng O(1) chống treo giao diện khi miền lớn (10^9).
        - Phân loại chính xác: b_sym <= 0 -> INFEASIBLE_BOUNDS_EMPTY; b_sym > 0 không nguyên -> INFEASIBLE_NO_INTEGER_POINTS.
        """
        def _check_eq_valid(eq_o, s_dict):
            if isinstance(eq_o, sp.Eq):
                return sp.simplify((eq_o.lhs - eq_o.rhs).subs(s_dict)) == 0
            return sp.simplify(eq_o.subs(s_dict)) == 0

        out = []
        out.append("=" * 85)
        out.append("QUY TRÌNH GIẢI HỆ PHƯƠNG TRÌNH VÔ ĐỊNH & KHẢO SÁT NGHIỆM NGUYÊN (DIOPHANTINE SYSTEM):")
        out.append("=" * 85)

        m = len(eq_syms)
        n = len(vars_sorted)
        var_names_str = ", ".join(s.name for s in vars_sorted)

        out.append("\n[BƯỚC 1: PHÂN TÍCH CẤU TRÚC ĐẠI SỐ TUYẾN TÍNH]")
        out.append(f"  • Số lượng phương trình: M = {m}")
        out.append(f"  • Số lượng biến số: N = {n} ({var_names_str})")

        linsols = sp.linsolve(eq_syms, vars_sorted)
        if not linsols:
            out.append("  • Hệ phương trình vô nghiệm trên tập số thực ℝ (rank(A) != rank(A|b)).")
            category = DiophantineCategory.INCONSISTENT
            self.last_dioph_category = category
            self.last_dioph_solutions = []
            self.last_dioph_n_total = 0
            self._notify('diophantine_result', {'category': category, 'sols': [], 'n_total': 0, 'out': out})
            return category, [], 0, out

        sol_tuple = list(linsols)[0]
        free_syms = sorted(list(set().union(*[it.free_symbols for it in sol_tuple])), key=lambda s: s.name)
        d = len(free_syms)
        out.append(f"  • Bậc tự do của hệ: d = N - rank(A) = {d} tham số tự do.")

        # Xử lý d = 0 (Hệ xác định, nghiệm duy nhất)
        if d == 0:
            out.append("\n[BƯỚC 2: KHẢO SÁT NGHIỆM DUY NHẤT (d = 0)]")
            is_pos_int = all(hasattr(c, 'is_Integer') and c.is_Integer and c > 0 for c in sol_tuple)
            sol_str = ", ".join(f"{v.name} = {c}" for v, c in zip(vars_sorted, sol_tuple))
            if is_pos_int:
                out.append(f"  ==> Hệ có nghiệm nguyên dương duy nhất: ({sol_str})")
                category = DiophantineCategory.UNIQUE
                sols = [tuple(int(c) for c in sol_tuple)]
                self.last_dioph_category = category
                self.last_dioph_solutions = sols
                self.last_dioph_n_total = 1
                self._notify('diophantine_result', {'category': category, 'sols': sols, 'n_total': 1, 'out': out})
                return category, sols, 1, out
            else:
                out.append(f"  ==> Hệ có nghiệm thực duy nhất ({sol_str}) nhưng không thuộc tập số nguyên dương (ℤ⁺)ⁿ.")
                category = DiophantineCategory.EMPTY_NO_POSITIVE_INTEGER
                self.last_dioph_category = category
                self.last_dioph_solutions = []
                self.last_dioph_n_total = 0
                self._notify('diophantine_result', {'category': category, 'sols': [], 'n_total': 0, 'out': out})
                return category, [], 0, out

        # Xử lý d >= 2 (Đa tham số, thông báo phạm vi an toàn)
        if d >= 2:
            out.append(f"\n[BƯỚC 2: HỌ NGHIỆM TỔNG QUÁT ĐA THAM SỐ (d = {d} >= 2)]")
            out.append(f"  • Hệ có {d} tham số tự do ({', '.join(s.name for s in free_syms)}) trên ℝ.")
            out.append("  • Biểu diễn affine nghiệm tổng quát trên ℝ:")
            for v, expr in zip(vars_sorted, sol_tuple):
                out.append(f"    {v} = {clean_display_expr(expr)}")
            out.append("  • Lưu ý phạm vi sư phạm: Lớp bài toán Diophantine đa tham số (d >= 2) chưa hỗ trợ tự động tìm nghiệm nguyên dương.")
            category = DiophantineCategory.UNSUPPORTED_DIM_GE_2
            self.last_dioph_category = category
            self.last_dioph_solutions = []
            self.last_dioph_n_total = 0
            self._notify('diophantine_result', {'category': category, 'sols': [], 'n_total': 0, 'out': out})
            return category, [], 0, out

        # TRƯỜNG HỢP d = 1: Phân tích đồng dư solve_congruence và các trạng thái cấu trúc
        param = free_syms[0]
        out.append(f"\n[BƯỚC 2: BIỂU DIỄN THAM SỐ AFFINE THEO ẨN TỰ DO {param}]")
        for v, expr in zip(vars_sorted, sol_tuple):
            if expr == v:
                out.append(f"  • Tham số tự do: {v} ∈ ℝ")
            else:
                out.append(f"  • Biến phụ thuộc {v}: {v} = {clean_display_expr(expr)}")

        out.append("\n[BƯỚC 3: PHÂN TÍCH HỆ ĐỒNG DƯ VÀ RÀNG BUỘC BIÊN (ℤ⁺)]")
        lo = sp.Integer(1)
        hi = None
        infeasible_bounds_empty = False
        no_integer_point = False
        congruences = []

        for v, expr in zip(vars_sorted, sol_tuple):
            e_exp = sp.expand(expr)
            try:
                # Kiểm tra hệ số exact
                c_param = e_exp.coeff(param)
                c_const = e_exp.subs(param, 0)
                if c_param.has(sp.Float) or c_const.has(sp.Float):
                    category = DiophantineCategory.UNSUPPORTED_NON_INTEGER
                    out.append(f"  • Hệ chứa hệ số số thực (Float) không chính xác: {clean_display_expr(expr)}")
                    self.last_dioph_category = category
                    self.last_dioph_solutions = []
                    self.last_dioph_n_total = 0
                    self._notify('diophantine_result', {'category': category, 'sols': [], 'n_total': 0, 'out': out})
                    return category, [], 0, out

                a_sym = sp.Rational(c_param)
                b_sym = sp.Rational(c_const)
            except Exception:
                category = DiophantineCategory.UNSUPPORTED_NON_INTEGER
                self.last_dioph_category = category
                self.last_dioph_solutions = []
                self.last_dioph_n_total = 0
                self._notify('diophantine_result', {'category': category, 'sols': [], 'n_total': 0, 'out': out})
                return category, [], 0, out

            out.append(f"  • {v} > 0  <=>  {clean_display_expr(expr)} > 0")

            if a_sym > 0:
                bd = sp.floor(-b_sym / a_sym) + 1
                lo = bd if lo is None else max(lo, bd)
            elif a_sym < 0:
                bd = sp.ceiling(-b_sym / a_sym) - 1
                hi = bd if hi is None else min(hi, bd)
            else:
                # a_sym == 0: biến nhận giá trị hằng số b_sym (P1-6)
                if b_sym <= 0:
                    infeasible_bounds_empty = True  # Miền thực rỗng
                elif not b_sym.is_Integer:
                    no_integer_point = True        # Miền thực dương có nhưng hằng số không nguyên

            D_val = math.lcm(a_sym.q, b_sym.q)
            A_val = int(a_sym * D_val)
            B_val = int(b_sym * D_val)
            g_val = math.gcd(A_val, D_val)

            if (-B_val) % g_val != 0:
                no_integer_point = True
            elif A_val != 0:
                Ag = A_val // g_val
                Dg = D_val // g_val
                if Dg > 1:
                    rem = (-(B_val // g_val) * pow(Ag, -1, Dg)) % Dg
                    congruences.append((rem, Dg))

        int_sols = []
        category = DiophantineCategory.UNKNOWN
        n_total = 0

        if infeasible_bounds_empty or (hi is not None and lo > hi):
            category = DiophantineCategory.INFEASIBLE_BOUNDS_EMPTY
            out.append("\n  ==> KẾT QUẢ: Miền ràng buộc rỗng (Hệ bất phương trình biên vô nghiệm trên ℤ⁺).")
        elif no_integer_point:
            category = DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS
            out.append("\n  ==> KẾT QUẢ: Không có điểm nguyên nào thỏa mãn hệ (Hệ có nghiệm thực dương nhưng không có điểm nguyên).")
        else:
            sc = solve_congruence(*congruences) if congruences else (0, 1)
            if sc is None:
                category = DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS
                out.append("\n  ==> KẾT QUẢ: Hệ đồng dư vô nghiệm trên ℤ (Không thỏa mãn hệ đồng dư CRT).")
            else:
                p_res, m_mod = int(sc[0]), int(sc[1])
                k_start = int(sp.ceiling((lo - p_res) / m_mod))
                start_val = p_res + k_start * m_mod

                if hi is not None:
                    if start_val > hi:
                        category = DiophantineCategory.INFEASIBLE_NO_INTEGER_POINTS
                        out.append(f"\n  ==> KẾT QUẢ: Không có điểm nguyên nào thỏa mãn đồng dư trong miền bị chặn [{lo}, {hi}].")
                    else:
                        category = DiophantineCategory.FINITE_BOUNDED
                        # Tính n_total bằng công thức đóng O(1) chống treo giao diện
                        n_total = int((hi - start_val) // m_mod + 1)
                        out.append(f"\n  ==> KẾT QUẢ: Miền nghiệm hữu hạn bị chặn ({param} ∈ [{lo}, {hi}]).")
                        out.append(f"      Điều kiện đồng dư nghiệm nguyên: {param} ≡ {p_res} (mod {m_mod}).")
                        out.append(f"      Tổng số bộ nghiệm nguyên dương: {n_total} bộ nghiệm.")

                        # Dựng và xác thực nghiệm chi tiết cho tối đa 10 bộ nghiệm đầu tiên
                        eval_count = min(n_total, 10)
                        verification_failed = False
                        for k_idx in range(eval_count):
                            pval = start_val + k_idx * m_mod
                            cand = [item.subs(param, pval) for item in sol_tuple]
                            if all(hasattr(c, 'is_Integer') and c.is_Integer and c > 0 for c in cand):
                                sub_dict = {vr: c_val for vr, c_val in zip(vars_sorted, cand)}
                                if all(_check_eq_valid(eq_orig, sub_dict) for eq_orig in eq_syms):
                                    int_sols.append(tuple(int(c) for c in cand))
                                else:
                                    verification_failed = True
                            else:
                                verification_failed = True

                        if verification_failed or (eval_count > 0 and len(int_sols) != eval_count):
                            category = DiophantineCategory.UNKNOWN
                            out.append("  ==> CẢNH BÁO: Phát hiện sai lệch giữa công thức đồng dư và phương trình gốc.")
                            out.append("      Chuyển trạng thái sang UNKNOWN để bảo toàn tính đúng đắn toán học.")
                        elif n_total <= 10:
                            out.append(f"  ==> Liệt kê toàn bộ {len(int_sols)} bộ nghiệm nguyên dương:")
                        else:
                            out.append(f"  ==> Hiển thị {len(int_sols)} bộ nghiệm tiêu biểu đầu tiên (trên tổng số {n_total} bộ nghiệm):")

                        for idx, sol in enumerate(int_sols, 1):
                            sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                            out.append(f"    • Bộ nghiệm {idx}: {sol_str}")
                        if n_total > 10:
                            out.append(f"    ... [còn {n_total - 10} bộ nghiệm tiếp theo]")
                else:
                    category = DiophantineCategory.UNBOUNDED_INFINITE
                    out.append(f"\n  ==> KẾT QUẢ: Miền nghiệm vô hạn không bị chặn trên ({param} >= {lo}).")
                    out.append(f"      Họ nghiệm nguyên dương theo tham số: {param} = {start_val} + {m_mod}·k (với k ∈ ℤ, k >= 0).")

                    for k_idx in range(3):
                        pval = start_val + k_idx * m_mod
                        cand = [item.subs(param, pval) for item in sol_tuple]
                        if all(hasattr(c, 'is_Integer') and c.is_Integer and c > 0 for c in cand):
                            sub_dict = {vr: c_val for vr, c_val in zip(vars_sorted, cand)}
                            if all(_check_eq_valid(eq_orig, sub_dict) for eq_orig in eq_syms):
                                int_sols.append(tuple(int(c) for c in cand))

                    out.append("  ==> Hệ có vô số bộ nghiệm nguyên dương. Ba bộ nghiệm nhỏ nhất đại diện:")
                    for idx, sol in enumerate(int_sols, 1):
                        sol_str = ", ".join(f"{v.name} = {val}" for v, val in zip(vars_sorted, sol))
                        out.append(f"    • Bộ nghiệm {idx}: {sol_str}")

        # BƯỚC 4: KẾT LUẬN
        out.append("\n[BƯỚC 4: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
        if category == DiophantineCategory.FINITE_BOUNDED and int_sols:
            if n_total > 10:
                out.append(f"  ==> Kết luận: Hệ có {n_total} bộ nghiệm nguyên dương hữu hạn (chi tiết 10 bộ nghiệm đầu như trên).")
            else:
                latex_cases = [f"({', '.join(str(val) for val in sol)})" for sol in int_sols]
                out.append(f"  ==> Tập nghiệm nguyên dương hữu hạn: S_(ℤ⁺) = {{ {'; '.join(latex_cases)} }}")
        elif category == DiophantineCategory.UNBOUNDED_INFINITE:
            out.append("  ==> Hệ có vô số nghiệm nguyên dương phụ thuộc tham số không bị chặn.")
        elif category == DiophantineCategory.UNIQUE:
            out.append("  ==> Hệ có nghiệm nguyên dương duy nhất.")
        else:
            out.append("  ==> Hệ không có nghiệm nguyên dương (S_(ℤ⁺) = ∅).")

        self.last_dioph_category = category
        self.last_dioph_solutions = int_sols
        self.last_dioph_n_total = n_total
        self._notify('diophantine_result', {'category': category, 'sols': int_sols, 'n_total': n_total, 'out': out})
        return category, int_sols, n_total, out
