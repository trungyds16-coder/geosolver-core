# Phản biện đợt 5: tái rà soát sau khi tác giả báo đã xử lý đợt 4

**Đối tượng:** file `TONG_HOP_BAO_CAO_KHOA_HOC_CHO_CLAUDE_PHAN_BIEN.md` (phiên bản ghi trên đầu file: **2.4, 07/11/2026**), so với `PHAN_BIEN_DOT_4_RA_SOAT_MA_NGUON_v2_4.md`.

---

## 0. Kết luận ngắn

**File được tải lên chưa chứa bất kỳ chỉnh sửa nào của đợt 4.** Nó vẫn là bản v2.4 mà đợt 4 đã rà soát: mã nguồn, bảng Rubric, các câu hỏi tham vấn và cả những cụm từ tuyệt đối bị nhắc đều còn nguyên. Vì vậy tôi **không thể xác nhận là đã sửa đúng**. Có hai khả năng: (a) đã sửa trong mã/báo cáo nhưng tải nhầm file cũ; (b) chưa sửa vào file này.

Để bù lại, lần này tôi **đã cài SymPy 1.14.0 và chạy mã thật** (đợt 4 chưa chạy được). Kết quả: các lỗi nêu ở đợt 4 **được xác nhận bằng chạy thực**, kèm một lỗi mới nghiêm trọng hơn dự đoán (mục 2.2). Mục 3 là bản mã đã sửa và đã test, bạn có thể dùng hoặc đối chiếu với bản sửa của bạn.

---

## 1. Đối chiếu từng mục đợt 4 với file đã tải lên

| # | Yêu cầu đợt 4 | Trong file v2.4 | Trạng thái |
|---|---|---|---|
| 1 | Sửa nhận dạng dạng phương trình (`gx = rad - target_eq`) | Còn nguyên `rad_terms[0]`, `gx = sp.simplify(rad - target_eq)` | Chưa sửa |
| 2 | Tách ba tập hợp lệ / loại / chưa xác định | Nhánh `else` và `except Exception` vẫn `valid_sols.append(r)` | Chưa sửa |
| 3 | Dùng đồng dư thay cửa sổ 200 | Vẫn `range(start_p, start_p + 200)`; `lcm_denom` vẫn không dùng | Chưa sửa |
| 4 | Thông báo khi d ≠ 1, trần vòng lặp | Không có nhánh `else` cho `len(free_syms) != 1`; nhánh hữu hạn không có trần | Chưa sửa |
| 5 | Đồng bộ báo cáo với mã | Chưa có mô tả khớp mã | Chưa sửa |
| 6 | Bộ test và oracle vét cạn | Không có | Chưa có |
| 7 | Rubric chấm bởi người độc lập, đổi nhãn | Bảng vẫn 10.0 / 10, không nhãn "tự đánh giá" | Chưa sửa |
| 8 | Sửa câu chữ bước 1, hiển thị giá trị g(r) | Vẫn "để căn thức có nghĩa thực" | Chưa sửa |
| 9 | Lọc nghiệm phức, bỏ `except:` trần | Còn `except: pass` và không lọc nghiệm thực | Chưa sửa |
| 10 | Bỏ cụm tuyệt đối | Vẫn "TIẾP THU TRỌN VẸN", "triệt tiêu được các rủi ro" | Chưa sửa |

---

## 2. Kết quả chạy mã gốc (SymPy 1.14.0)

Mã gốc được chạy nguyên văn logic (thay `clean_display_expr` bằng `str`, bỏ `self`).

### 2.1. Nhận dạng dạng phương trình: xác nhận

| Phương trình | `g` mà mã tính ra | Nghiệm hệ quả mã in | Đánh giá |
|---|---|---|---|
| √(2x−1) = x−1 | `x - 1` | 2±√2 | Đúng |
| x−1 = √(2x−1) | `-x + 2√(2x-1) + 1` | 10+3√10, 2+√2 | **Sai:** in lời giải của phương trình khác |
| 2√(2x−1) = x−1 | `x - √(2x-1) - 1` | 1, 5+2√5 | **Sai:** nghiệm "1" không thuộc hệ quả đúng |

Đáp số cuối của hai dòng sai tình cờ đúng (2+√2 và 5+2√5), nhưng **các bước hiển thị cho học sinh là sai** mà không có cảnh báo. Đúng thứ mà đề tài cam kết cung cấp.

### 2.2. Lỗi mới: nghiệm phức được nhận (nghiêm trọng)

Với √x = x² + 1 (vô nghiệm thực), mã gốc trả `valid` gồm **cả 4 nghiệm phức** của hệ quả. Nguyên nhân: `float()` trên số phức ném lỗi, `ask` không kết luận, `evalf` ném lỗi, hàm trả `None`, nhánh `else` nhận nghiệm. Đây chính là đường "bất định thì nhận" mà đợt 4 cảnh báo, nhưng hậu quả nặng hơn dự đoán: kết luận "có 4 nghiệm" cho phương trình vô nghiệm.

### 2.3. Hai căn bị xử lý im lặng: xác nhận

√x + √(x+1) = 2: mã lấy một căn, không từ chối, trả 9/16. Ở ví dụ này kết quả tình cờ đúng, nhưng quy trình không có cơ sở cho dạng hai căn.

### 2.4. Diophantine

Hành vi của mã gốc ở các phản ví dụ A, B (cửa sổ 200) đã được mô phỏng ở đợt 4; lần này bản sửa cho đúng kỳ vọng (mục 3.2).

---

## 3. Bản mã đã sửa và kết quả kiểm thử

### 3.1. Căn thức

```python
import sympy as sp

def sign_status(v):
    """'pos' | 'neg' | 'zero' | 'nonreal' | 'unknown'; không bao giờ đoán."""
    v = sp.simplify(v)
    if v.is_real is False: return 'nonreal'
    if v.is_zero: return 'zero'
    if v.is_positive: return 'pos'
    if v.is_negative: return 'neg'
    try:
        a = sp.N(v, 60)
        if abs(sp.im(a)) > sp.Float('1e-40'): return 'nonreal'
        a = sp.re(a)
        if abs(a) > sp.Float('1e-40'): return 'pos' if a > 0 else 'neg'
    except Exception:
        pass
    return 'unknown'   # có thể bằng 0 đúng; chưa chứng minh được

def solve_radical_fixed(target_eq, x):
    """target_eq = VT - VP (biểu thức, không phải Eq)."""
    out = {"valid": [], "rejected": [], "unknown": [], "scope_error": None}
    rads = [t for t in target_eq.atoms(sp.Pow) if t.exp == sp.Rational(1, 2)]
    if len(rads) != 1:
        out["scope_error"] = "Ngoài phạm vi: cần đúng một căn bậc hai."
        return out
    rad = rads[0]
    expanded = sp.expand(target_eq)
    c = expanded.coeff(rad)
    rest = sp.expand(expanded - c * rad)
    if c == 0 or c.free_symbols or any(t.exp == sp.Rational(1, 2) for t in rest.atoms(sp.Pow)):
        out["scope_error"] = "Ngoài phạm vi: dạng căn không chuẩn."
        return out
    fx = rad.base
    gx = sp.simplify(-rest / c)                      # √f = g
    out["fx"], out["gx"] = fx, gx
    for r in sp.solve(sp.expand(fx - gx**2), x):
        if r.is_real is False or abs(sp.N(r, 30).as_real_imag()[1]) > sp.Float('1e-25'):
            out["rejected"].append((r, "nghiệm không thực")); continue
        sg, sf = sign_status(gx.subs(x, r)), sign_status(fx.subs(x, r))
        if sg == 'neg':   out["rejected"].append((r, "g(r) < 0"))
        elif sf == 'neg': out["rejected"].append((r, "f(r) < 0"))
        elif 'unknown' in (sg, sf) or 'nonreal' in (sg, sf):
            out["unknown"].append((r, f"g:{sg}, f:{sf}"))   # KHÔNG đưa vào đáp số
        else: out["valid"].append(r)
    return out
```

Kết quả chạy:

| Phương trình | Kết quả |
|---|---|
| √(2x−1) = x−1 | Nhận 2+√2; loại 2−√2 (g<0) |
| x−1 = √(2x−1) | Giống dòng trên (lỗi nhận dạng đã hết) |
| 2√(2x−1) = x−1 | Nhận 5+2√5; loại 5−2√5 (g<0) |
| √x = x²+1 | Không có nghiệm hợp lệ; 4 nghiệm phức đều bị loại |
| √x + √(x+1) = 2 | Từ chối: ngoài phạm vi |

### 3.2. Diophantine (đồng dư + CRT, thay cho cửa sổ 200)

Ý tưởng: với mỗi biến v = a·p + b (a, b hữu tỷ), quy đồng thành đồng dư tuyến tính; giải bằng gcd và nghịch đảo modular; hợp nhất bằng CRT; cận từ các bất đẳng thức v > 0 cho cận số nguyên; quét theo bước M hoặc xuất họ nghiệm tham số.

```python
import sympy as sp
from sympy.ntheory.modular import solve_congruence

def solve_dioph_fixed(eqs, vars_, cap=1000):
    """eqs: biểu thức (VT-VP). Nghiệm nguyên dương."""
    res = {"category": None, "solutions": [], "family": None, "note": ""}
    ls = sp.linsolve(eqs, vars_)
    if not ls:
        res["category"] = "INCONSISTENT"; return res
    sol = list(ls)[0]
    free = sorted(set().union(*[sp.sympify(e).free_symbols for e in sol]), key=lambda s: s.name)
    if len(free) == 0:
        ok = all(sp.sympify(e).is_integer and e > 0 for e in sol)
        res["category"] = "UNIQUE" if ok else "EMPTY_NO_POSITIVE_INTEGER"
        if ok: res["solutions"] = [tuple(int(e) for e in sol)]
        return res
    if len(free) >= 2:
        res["category"] = "UNSUPPORTED_DIM>=2"; return res     # thông báo tường minh
    p = free[0]
    lo = hi = None; cong = []
    for e in sol:
        e = sp.expand(e); a = sp.Rational(e.coeff(p)); b = sp.Rational(e.subs(p, 0))
        D = sp.ilcm(a.q, b.q); A = int(a*D); B = int(b*D); g = sp.igcd(A, D)
        if (-B) % g: res["category"] = "EMPTY_NO_INTEGER"; return res
        if A != 0:
            Ag, Dg = A//g, D//g
            cong.append(((-(B//g) * pow(Ag, -1, Dg)) % Dg if Dg > 1 else 0, Dg))
        if a > 0:   bd = sp.floor(-b/a) + 1;   lo = bd if lo is None else max(lo, bd)
        elif a < 0: bd = sp.ceiling(-b/a) - 1; hi = bd if hi is None else min(hi, bd)
        elif b <= 0: res["category"] = "EMPTY_INFEASIBLE"; return res
    sc = solve_congruence(*cong) if cong else (0, 1)
    if sc is None: res["category"] = "EMPTY_NO_INTEGER"; return res
    r, M = int(sc[0]), int(sc[1])
    if lo is None: lo = -10**9
    start = int(lo) + ((r - int(lo)) % M)
    if hi is not None:
        hi = int(hi)
        if start > hi: res["category"] = "EMPTY_INFEASIBLE"; return res
        n = (hi - start)//M + 1
        res["category"] = "FINITE_BOUNDED"
        res["solutions"] = [tuple(int(e.subs(p, start + M*k)) for e in sol) for k in range(min(n, cap))]
        if n > cap: res["note"] = f"cắt ở {cap}/{n} nghiệm"
    else:
        res["category"] = "UNBOUNDED_INFINITE"
        k = sp.Symbol('k', integer=True, nonnegative=True)
        res["family"] = tuple(sp.expand(e.subs(p, start + M*k)) for e in sol)
        res["solutions"] = [tuple(int(e.subs(p, start + M*j)) for e in sol) for j in range(3)]
    return res
```

Kết quả chạy:

| Hệ | Phân loại | Kết quả |
|---|---|---|
| 251x − z = −5, y = 2 | `UNBOUNDED_INFINITE` | (1,2,256), (2,2,507), (3,2,758); họ (k+1, 2, 251k+256) |
| 2x − 2z = 1, y = 5 | `EMPTY_NO_INTEGER` | Vô nghiệm nguyên (nhãn riêng) |
| x = z − 5, y = 0 | `EMPTY_INFEASIBLE` | Rỗng |
| x = 3, y = 4, z = 1 | `UNIQUE` | (3,4,1) |
| x + y + z = 10 | `UNSUPPORTED_DIM>=2` | Thông báo, không im lặng |
| x + z = 10⁹, y = 1 | `FINITE_BOUNDED` | Cắt ở 1000 nghiệm, ghi chú số nghiệm thật; không treo |

**Oracle vét cạn:** 395 hệ ngẫu nhiên 2 phương trình, 3 ẩn, hệ số trong [−4, 4], đúng một tham số tự do, so tập nghiệm với vét cạn trong hộp 1..80: **0 sai lệch**.

### 3.3. Giới hạn của phần kiểm thử này

- Mới thử trên các ca trên và 395 hệ ngẫu nhiên; chưa phủ hệ có nhiều hơn 2 phương trình hoặc hệ số lớn.
- Nhánh `unknown` của căn thức (nghiệm lồng căn với g(r) = 0 mà SymPy không tự rút gọn) **chưa được thử**; cần một ca cụ thể từ bộ test của bạn.
- Mã trên chưa được ghép vào `cad_math_v2.py` thật; tên hàm, định dạng `steps` và `clean_display_expr` cần bạn tích hợp. Bản sửa trả về dict, cần viết lại phần in lời giải (hiển thị giá trị g(r), lý do loại).
- Chạy trên SymPy 1.14.0; nếu bạn dùng phiên bản khác, cần chạy lại.

---

## 4. Rubric: không đổi so với đợt 4

Bảng vẫn là tự đánh giá của nhóm tác giả (10.0/10), chưa có người chấm độc lập, và vẫn trộn cột "Môi trường vận hành" vào bảng điểm. Việc sửa phần này không cần mã mà cần quy trình:

1. Đổi nhãn bảng thành **"tự đánh giá sơ bộ của nhóm, chưa có người chấm độc lập"**.
2. Công bố mốc điểm cho từng mức của từng tiêu chí trước khi chấm.
3. Nhờ ít nhất 3 giáo viên chấm mù (ẩn tên công cụ, chuẩn hóa định dạng lời giải); báo cáo trung vị, dải điểm, độ đồng thuận.
4. Chấm SymPy `check=True` là "không áp dụng" ở hai tiêu chí giải thích thay vì 0 điểm.
5. Tách "offline, tiếng Việt, miễn phí" ra thành bảng lợi thế sản phẩm riêng.
6. Ghi nguồn dòng Symbolab/Wolfram Alpha: 10 bài nào, ngày chạy, gói sử dụng, nơi lưu ảnh chụp.

Cũng nên đổi ba cụm đang còn: "TIẾP THU TRỌN VẸN", "Tiếp thu hoàn toàn", và câu hỏi 2 ("đã triệt tiêu được các rủi ro chưa?") sang cách nói có giới hạn, ví dụ "đã xử lý các điểm A, B, C; còn các hạn chế X, Y".

---

## 5. Việc cần làm tiếp

| # | Việc | Mức |
|---|---|---|
| 1 | Tải lên **file đã sửa thật** (mã và báo cáo) để tôi tái rà soát | Cao |
| 2 | Tích hợp hoặc đối chiếu hai hàm sửa ở mục 3 với bản của bạn | Cao |
| 3 | Thêm bộ test mục 3 và oracle vét cạn vào repo, ghi phiên bản SymPy | Cao |
| 4 | Thêm một ca nghiệm lồng căn với g(r) = 0 để thử nhánh `unknown` | Cao |
| 5 | Làm lại Rubric theo mục 4; chưa có người chấm thì giữ nhãn "dự thảo" | Cao |
| 6 | Sửa câu chữ bước 1: "Vì √f(x) ≥ 0 nên vế phải phải không âm: g(x) ≥ 0" | Trung bình |
| 7 | Cập nhật báo cáo thành v2.5, ghi rõ cái gì đã sửa, cái gì còn hạn chế | Trung bình |

---

*Phản biện này dựa trên đọc file đã tải lên và chạy thực mã trên SymPy 1.14.0 (các hàm được chép nguyên văn logic, không phải toàn bộ `cad_math_v2.py`). Đây là tham vấn kỹ thuật bằng công cụ AI, không thay thế thẩm định bởi người thật.*
