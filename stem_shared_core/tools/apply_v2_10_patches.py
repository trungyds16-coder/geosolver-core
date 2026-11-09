import re, sys

with open("cad_math_v2/cad_math_v2.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add DiophantineCategory after imports
if "class DiophantineCategory" not in code:
    import_anchor = "import sympy as sp\n"
    enum_def = """import sympy as sp
from enum import Enum

class DiophantineCategory(str, Enum):
    INCONSISTENT = "INCONSISTENT"
    UNIQUE = "UNIQUE"
    EMPTY_NO_POSITIVE_INTEGER = "EMPTY_NO_POSITIVE_INTEGER"
    UNSUPPORTED_DIM_GE_2 = "UNSUPPORTED_DIM>=2"
    INFEASIBLE_BOUNDS_EMPTY = "INFEASIBLE_BOUNDS_EMPTY"
    INFEASIBLE_NO_INTEGER_POINTS = "INFEASIBLE_NO_INTEGER_POINTS"
    FINITE_BOUNDED = "FINITE_BOUNDED"
    UNBOUNDED_INFINITE = "UNBOUNDED_INFINITE"
    UNKNOWN = "UNKNOWN"
"""
    code = code.replace(import_anchor, enum_def, 1)

# 2. Sanitize "chính thức"
code = code.replace("KẾT QUẢ TẬP NGHIỆM CHÍNH THỨC 2D (HERO RESULT CARD)", "KẾT QUẢ TẬP NGHIỆM HỢP LỆ 2D (HERO RESULT CARD)")
code = code.replace("[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM CHÍNH THỨC S]", "[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
code = code.replace("[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM CHÍNH THỨC S / CONCLUSION]", "[BƯỚC CUỐI: KẾT LUẬN TẬP NGHIỆM S / CONCLUSION]")
code = code.replace("[KẾT QUẢ NGUYÊN HÀM CHÍNH THỨC]:", "[KẾT QUẢ NGUYÊN HÀM]:")
code = code.replace("# Bước 3: Tìm tập nghiệm chính thức", "# Bước 3: Xác định tập nghiệm hợp lệ")

# 3. Add static methods real_status and check_sign_exact to CADMathDesktopAppV2 if not present
static_methods = '''    @staticmethod
    def real_status(r):
        """Xác định nghiệm là thực (True), phức (False) hay chưa kết luận (None)."""
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
        """Xác định dấu đại số chính xác của biểu thức."""
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
                if float(s) > 0: return 'pos'
                elif float(s) < 0: return 'neg'
                else: return 'zero'
        except Exception:
            pass
        try:
            val = float(sp.N(expr_s, 40))
            if abs(val) > 1e-30:
                return 'pos' if val > 0 else 'neg'
        except Exception:
            pass
        return 'unknown'
'''

# Find class CADMathDesktopAppV2:
class_match = re.search(r'class CADMathDesktopAppV2\b.*?:', code)
if class_match and "def real_status(r):" not in code[:class_match.end() + 2000]:
    insert_pos = class_match.end() + 1
    code = code[:insert_pos] + "\n" + static_methods + "\n" + code[insert_pos:]

# In solve_radical_pedagogical, replace local calls to use self.real_status and self.check_sign_exact
# And remove the inner def real_status and def check_sign_exact
solve_rad_pattern = r'def solve_radical_pedagogical\(self, target_eq, x\):'
rad_idx = code.find("def solve_radical_pedagogical(self, target_eq, x):")
if rad_idx != -1:
    # Find next method: def solve_underdetermined_or_diophantine
    dioph_idx = code.find("def solve_underdetermined_or_diophantine(self,", rad_idx)
    rad_block = code[rad_idx:dioph_idx]
    
    # Replace inner definitions if they exist inside rad_block
    # Check if 'def real_status(r):' is inside
    if "        def real_status(r):" in rad_block:
        # replace the inner functions with delegating calls or remove them
        # simpler and safest: have the inner functions delegate to self
        delegates = """        def real_status(r):
            return self.real_status(r)

        def check_sign_exact(expr_sub):
            return self.check_sign_exact(expr_sub)
"""
        old_inner = re.search(r'        def real_status\(r\):.*?return \'unknown\'\n', rad_block, re.DOTALL)
        if old_inner:
            rad_block = rad_block[:old_inner.start()] + delegates + rad_block[old_inner.end():]
            code = code[:rad_idx] + rad_block + code[dioph_idx:]

with open("cad_math_v2/cad_math_v2.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Patch applied to cad_math_v2.py successfully")
