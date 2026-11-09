import os
import sys
import math
from flask import Flask, render_template, request, jsonify
import sympy as sp

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

app = Flask(__name__)

# --- BỘ GIẢI TOÁN TỌA ĐỘ VÀ SUY LUẬN HÌNH HỌC (GEOMETRIC & OXY SOLVER) ---

def solve_problem_cau_viii(data=None):
    """
    Giải bài toán Câu VIII:
    Tứ giác ABCD nội tiếp (O) đường kính BD.
    M(0, 4) là hình chiếu của A trên BC.
    N(2, 2) là hình chiếu của A trên BD.
    P = MN cắt AC.
    AC: x - y - 1 = 0.
    xA < 2.
    Tìm P, A, B.
    """
    steps = []
    
    # Bước 1: Suy luận hình học thuần túy
    steps.append({
        "stage": "Phát hiện tính chất hình học ẩn",
        "detail": "1. Vì BD là đường kính của đường tròn ngoại tiếp ABCD nên $\\widehat{BAD} = \\widehat{BCD} = 90^\\circ$ (góc nội tiếp chắn nửa đường tròn).<br>"
                 "2. Lại có $AM \\perp BC$ mà $CD \\perp BC \\implies AM \\parallel CD$. Suy ra $\\widehat{MAC} = \\widehat{ACD}$ (hai góc so le trong).<br>"
                 "3. Xét tứ giác $ABNM$: có $\\widehat{AMB} = 90^\\circ$ (do $AM \\perp BC$) và $\\widehat{ANB} = 90^\\circ$ (do $AN \\perp BD$). Do đó tứ giác $ABNM$ nội tiếp đường tròn đường kính $AB$.<br>"
                 "4. Suy ra góc nội tiếp $\\widehat{AMN} = \\widehat{ABN} = \\widehat{ABD}$.<br>"
                 "5. Trong đường tròn $(ABCD)$, $\\widehat{ABD} = \\widehat{ACD}$ (hai góc nội tiếp cùng chắn cung $AD$).<br>"
                 "6. Từ các điều trên suy ra: $\\widehat{AMN} = \\widehat{MAC} \\iff \\widehat{PMA} = \\widehat{PAM}$.<br>"
                 "$\\implies \\mathbf{\\Delta PAM \\text{ cân tại } P \\implies PA = PM}$."
    })
    
    # Bước 2: Tọa độ hóa bằng SymPy
    x, y, t = sp.symbols('x y t', real=True)
    
    # Tọa độ M, N
    M = (0, 4)
    N = (2, 2)
    
    # Đường thẳng MN: vector chỉ phương MN = (2, -2) => vector pháp tuyến (1, 1)
    # MN qua M(0, 4): 1*(x - 0) + 1*(y - 4) = 0 <=> x + y - 4 = 0
    line_MN = x + y - 4
    line_AC = x - y - 1
    
    # Tọa độ điểm P = MN giao AC
    sol_P = sp.solve([line_MN, line_AC], (x, y))
    P_x = sol_P[x]
    P_y = sol_P[y]
    
    steps.append({
        "stage": "Tìm tọa độ điểm P",
        "detail": f"Đường thẳng $MN$ đi qua $M(0;4)$ và $N(2;2)$ có phương trình: $x + y - 4 = 0$.<br>"
                 f"Tọa độ giao điểm $P = MN \\cap AC$ là nghiệm hệ: $\\begin{{cases}} x + y - 4 = 0 \\\\ x - y - 1 = 0 \\end{{cases}} \\implies \\mathbf{{P\\left(\\frac{{{P_x.p}}}{{{P_x.q}}}; \\frac{{{P_y.p}}}{{{P_y.q}}}\\right)}} = P(2.5; 1.5)$."
    })
    
    # Tính PM^2
    PM_sq = (M[0] - P_x)**2 + (M[1] - P_y)**2
    
    # Điểm A thuộc AC: x - y - 1 = 0 => y = x - 1 => A(t, t - 1)
    A_x = t
    A_y = t - 1
    PA_sq = (A_x - P_x)**2 + (A_y - P_y)**2
    
    # Giải phương trình PA^2 = PM^2
    eq_A = sp.Eq(PA_sq, PM_sq)
    sol_A_t = sp.solve(eq_A, t)
    
    # Điều kiện hoành độ xA < 2
    valid_t = [val for val in sol_A_t if val < 2][0]
    A_coord = (float(valid_t), float(valid_t - 1))
    
    steps.append({
        "stage": "Tìm tọa độ điểm A",
        "detail": f"Độ dài $PM^2 = (0 - 2.5)^2 + (4 - 1.5)^2 = {float(PM_sq)}$.<br>"
                 f"Vì $A \\in AC$ nên gọi $A(t; t - 1)$. Do $PA = PM \\iff PA^2 = PM^2$:<br>"
                 f"$(t - 2.5)^2 + (t - 1 - 1.5)^2 = {float(PM_sq)} \\iff 2(t - 2.5)^2 = 12.5 \\iff (t - 2.5)^2 = 6.25$.<br>"
                 f"Suy ra $t = 5$ hoặc $t = 0$. Do điều kiện $x_A < 2$, ta nhận $t = 0 \\implies \\mathbf{{A(0; -1)}}$."
    })
    
    # Tìm B:
    # 1. Đường thẳng BC đi qua M(0, 4) và vuông góc với AM.
    # Vector AM = (0 - 0, 4 - (-1)) = (0, 5) => đường thẳng AM có phương trình x = 0.
    # Vì BC vuông góc AM tại M => BC có phương trình y = 4.
    # 2. Đường thẳng BD đi qua N(2, 2) và vuông góc với AN.
    # Vector AN = (2 - 0, 2 - (-1)) = (2, 3) => BD nhận AN=(2,3) làm VTPT.
    # Phương trình BD: 2(x - 2) + 3(y - 2) = 0 <=> 2x + 3y - 10 = 0.
    # B = BC giao BD => y = 4, 2x + 3(4) - 10 = 0 => 2x = -2 => x = -1.
    
    B_x = -1
    B_y = 4
    
    steps.append({
        "stage": "Tìm tọa độ điểm B",
        "detail": f"Ta có $M(0;4)$ là hình chiếu của $A(0;-1)$ lên $BC \\implies BC \\perp AM$.<br>"
                 f"Đoạn $AM$ nằm trên trục tung $Oy$ ($x = 0$) nên đường thẳng $BC$ có phương trình: $y = 4$.<br>"
                 f"Lại có $N(2;2)$ là hình chiếu của $A(0;-1)$ lên $BD \\implies BD \\perp AN$.<br>"
                 f"Vectơ $\\vec{{AN}} = (2; 3)$ là vectơ pháp tuyến của $BD$.<br>"
                 f"Phương trình đường thẳng $BD$: $2(x - 2) + 3(y - 2) = 0 \\iff 2x + 3y - 10 = 0$.<br>"
                 f"Tọa độ điểm $B$ là giao điểm của $BC$ và $BD$:<br>"
                 f"$\\begin{{cases}} y = 4 \\\\ 2x + 3y - 10 = 0 \\end{{cases}} \\implies 2x + 12 - 10 = 0 \\implies x = -1 \\implies \\mathbf{{B(-1; 4)}}$."
    })
    
    return {
        "P": [float(P_x), float(P_y)],
        "A": [float(A_coord[0]), float(A_coord[1])],
        "B": [float(B_x), float(B_y)],
        "steps": steps
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/solve_cau_viii', methods=['POST'])
def api_solve():
    try:
        data = request.json or {}
        res = solve_problem_cau_viii(data)
        return jsonify({"success": True, "result": res})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  ỨNG DỤNG HÌNH HỌC TƯƠNG TÁC VÀ BỘ GIẢI LAI THÔNG MINH")
    print("  Mở trình duyệt tại: http://localhost:5000")
    print("="*60 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=True)
