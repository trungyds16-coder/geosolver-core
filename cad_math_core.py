"""CADMathCore: chép nguyên văn từ hồ sơ thẩm định v2.2.0-RC (chưa sửa) để chạy test."""
import sympy as sp


class CADMathCore:
    def __init__(self, listener=None):
        self.listener = listener

    @staticmethod
    def real_status(r):
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
        steps = []
        rads = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
        if len(rads) != 1:
            return ["Ngoài phạm vi: Phương trình chứa nhiều hơn 1 căn thức."], [], [], []

        rad = rads[0]
        expanded = sp.expand(target_eq)
        c = expanded.coeff(rad)
        rest = sp.expand(expanded - c * rad)

        if c == 0 or c.free_symbols or any(t.exp == sp.Rational(1, 2) for t in rest.atoms(sp.Pow)):
            return ["Dạng căn thức không cô lập được."], [], [], []

        gx = sp.simplify(-rest / c)
        fx = rad.base

        steps.append(f"Bước 1: Chuẩn hóa: √({fx}) = {gx}")
        steps.append(f"  • Điều kiện có nghĩa căn thức: {fx} >= 0")
        steps.append(f"  • Điều kiện vế phải số học: {gx} >= 0")

        poly_eq = sp.simplify(fx - gx**2)
        raw_sols = sp.solve(poly_eq, x)
        steps.append(f"Bước 2: Bình phương hai vế thu được: {poly_eq} = 0")
        steps.append(f"  • Nghiệm đại số sơ bộ: {raw_sols}")

        valid_sols = []
        rejected_sols = []
        indeterminate_sols = []

        for r in raw_sols:
            if self.real_status(r) is False:
                rejected_sols.append((r, "Nghiệm phức không thuộc ℝ"))
                continue

            s_gx = self.check_sign_exact(gx.subs(x, r))
            s_fx = self.check_sign_exact(fx.subs(x, r))

            if s_gx == 'neg':
                rejected_sols.append((r, "Nghiệm ngoại lai (g(r) < 0)"))
            elif s_fx == 'neg':
                rejected_sols.append((r, "Vi phạm điều kiện xác định căn thức (f(r) < 0)"))
            elif s_gx in ['pos', 'zero'] and s_fx in ['pos', 'zero']:
                valid_sols.append(r)
            else:
                indeterminate_sols.append((r, f"g:{s_gx}, f:{s_fx}"))

        steps.append(f"Bước 4: Kết luận tập nghiệm hợp lệ: S = {valid_sols}")
        return steps, valid_sols, rejected_sols, indeterminate_sols


def compute_matrix_inverse(A: sp.Matrix):
    if A.rows != A.cols:
        raise ValueError("Chỉ ma trận vuông mới có ma trận nghịch đảo!")

    detA = A.det()
    if detA == 0:
        return {
            "invertible": False,
            "det": 0,
            "desc": "Ma trận suy biến (Singular Matrix), không khả nghịch vì det(A) = 0."
        }

    adjA = A.adjugate()
    invA = A.inv()
    return {
        "invertible": True,
        "det": detA,
        "adjugate": adjA,
        "inverse": invA
    }
