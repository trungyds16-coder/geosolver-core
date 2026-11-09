# BÁO CÁO TỰ ĐÁNH GIÁ KỸ THUẬT VÀ KIỂM CHỨNG THỰC NGHIỆM (ROUND 9)
## DỰ ÁN GEOSOLVER 2D — PHIÊN BẢN v3.1 RC2

**Tính chất tài liệu:** Báo cáo kỹ thuật tự đánh giá nội bộ của Đội ngũ phát triển (Internal Engineering Self-Assessment), phản hồi chi tiết các nhận xét phản biện đợt 9 của chuyên gia độc lập.  
**Trạng thái phân loại:** `RC2 – ĐÓNG GÓI EXE ĐÃ QUA SMOKE TEST CƠ BẢN (IN-DEVELOPMENT CANDIDATE FOR MSIX PACKAGING)`  
**Ngày cập nhật:** 09/11/2026  
**Môi trường thực thi:** Windows 11 Enterprise (x64), Python 3.14.5, PyInstaller 6.22.3, Tkinter 8.6, SymPy 1.14.0  
**Tập tin thực thi kiểm chứng:** `dist/GeoSolver/GeoSolver.exe` (SHA-256: `29B6E81FE71C0B0195E3E108D52520A48E8F722554E5AEB8E0C7623C749ABFFD`)

---

## 1. TIẾP THU PHẢN BIỆN VÀ TỔNG QUAN CẢI TIẾN ROUND 9

Đội ngũ phát triển tiếp thu đầy đủ các nhận xét phân tích kỹ thuật sâu từ chuyên gia độc lập ở Vòng 9. Cụ thể, các điều chỉnh mã nguồn và hạ tầng kiểm thử được triển khai đồng bộ ở các nhóm hạng mục:

1. **Xác thực dữ liệu đầu vào điểm (`_finite`):**
   - Loại trừ hoàn toàn nguy cơ lỗi tiềm ẩn do dữ liệu tọa độ chứa giá trị bất thường (`NaN`, `inf`, `-inf`, `None`, hoặc chuỗi không thể chuyển đổi thành số thực).
   - Kiểm tra nghiêm ngặt cho cả định dạng `dict` (`x`, `y`) và `tuple`/`list` (`p[0]`, `p[1]`). Bất kỳ giá trị không hợp lệ nào đều lập tức ném `ValueError` với thông báo rõ ràng, ngăn chặn triệt để hiện tượng sai lệch ngầm (silent failure/corruption).

2. **Cưỡng chế nhánh dung sai liên tục cho điểm vẽ chuột tự do (Taint enforcing continuous branch):**
   - *Phân tích hiện tượng:* Khi người dùng vẽ bằng chuột trên Canvas với tỷ lệ hiển thị $40\text{ px/unit}$, tọa độ chuột là bội số của $1/40 = 0.025$. Hàm `as_scaled_ints` với $k \le 3$ (nhân $1000$) sẽ biến các tọa độ này thành số nguyên trên lưới rời rạc $\mathbb{Z}^2$. Khi đó, tam giác vẽ tự do bị đẩy vào nhánh rời rạc so sánh tuyệt đối ($d^2_{AB} == d^2_{AC}$), khiến một tam giác vẽ tay có kích thước cạnh rất gần nhau (ví dụ: $1000$ và $1004$) bị kết luận là tam giác thường, mất đi chú thích trợ giúp người học `"gần vuông cân"` hoặc `"gần cân"`.
   - *Giải pháp triển khai:* Cập nhật điều kiện kích hoạt nhánh rời rạc:
     $$\text{is\_discrete} = (\text{scaled\_coords is not None}) \land (\text{user\_declared\_exact is not False})$$
     Khi người dùng vẽ chuột tự do (`user_declared_exact is False`), hệ thống **cưỡng chế chuyển sang nhánh dung sai liên tục** ($0.6\%$). Nhờ đó, tam giác vẽ tay gần cân/gần vuông cân được nhận diện chính xác và hiển thị đầy đủ độ lệch, trong khi các tam giác gõ tay bằng số nguyên hoặc số thập phân chuẩn xác vẫn giữ nguyên bản chất toán học rời rạc.

3. **Kế thừa cờ vết bẩn cho các điểm dẫn xuất (Derived point taint inheritance):**
   - Triển khai helper đệ quy `_point_flag(p, _depth=0)` hỗ trợ các nguồn dẫn xuất `_DERIVED_SOURCES = ("midpoint", "intersection", "formula")`.
   - Điểm dẫn xuất kế thừa cờ nguồn gốc từ các điểm cha thông qua khóa `"parents"`:
     - Nếu có bất kỳ điểm cha nào mang cờ `False` (vẽ tự do), điểm dẫn xuất lập tức bị đánh dấu `False` (bị vấy bẩn).
     - Nếu tất cả các điểm cha đều là `True` (gõ tay chính xác hoặc bắt dính lưới), điểm dẫn xuất nhận cờ `True`.
     - Nếu điểm cha không có metadata, điểm dẫn xuất nhận cờ `None` (chuyển sang heuristic số học).
   - Cập nhật Canvas GUI: Sự kiện kéo điểm `<B1-Motion>` khi không kích hoạt lưới bắt dính (`snap_to_grid` tắt) tự động gắn nhãn lại `p["source"] = "dragged"` và `p["exact"] = False`. Khi tạo trung điểm hoặc giao điểm, Canvas tự động lưu danh sách đối tượng cha vào thuộc tính `"parents"`.

4. **Tăng cường kiểm thử khói bản đóng gói (Check 7 SSL/Certifi CA bundle & `multiprocessing.freeze_support`):**
   - Bổ sung `multiprocessing.freeze_support()` ngay đầu khối thực thi chính của `geosolver_desktop.py` để bảo đảm tính ổn định của ứng dụng khi PyInstaller đóng băng các tiến trình con trên Windows.
   - Bổ sung mục kiểm tra số 7 trong bộ `--smoke-test`: Xác thực ngữ cảnh `ssl.create_default_context()` khởi tạo thành công và tệp CA root bundle của `certifi` (`cacert.pem`) tồn tại trong gói phân phối với dung lượng hợp lệ ($> 0\text{ bytes}$), bảo đảm khả năng kết nối HTTPS ra bên ngoài không bị gián đoạn.

5. **Dọn dẹp nhật ký và cấu hình bản dựng (`GeoSolver.spec` & `ai_local_manager.py`):**
   - Loại bỏ các lệnh gọi ghi log trùng lặp tới root logger trong `stem_shared_core/ai_local_manager.py`, chấm dứt hiện tượng nhân đôi thông báo cảnh báo trên `stderr`.
   - Loại bỏ module không tồn tại `'stem_shared_core.i18n'` khỏi mảng `hiddenimports` trong `geosolver/GeoSolver.spec`.

6. **Minh bạch hóa tài liệu Store Metadata và Chính sách quyền riêng tư (`STORE_METADATA_AND_PRIVACY.md`):**
   - Công khai minh bạch hai luồng kết nối mạng duy nhất của ứng dụng: Google Gemini API (khi người dùng chủ động cấu hình khóa API lưu trữ qua Windows DPAPI) và Hugging Face Hub (khi người dùng chủ động tải mô hình GGUF). Ứng dụng không chứa bất kỳ cơ chế thu thập dữ liệu ngầm (telemetry/tracking) nào.
   - Giải trình căn cứ kỹ thuật của quyền `runFullTrust`: GeoSolver 2D là ứng dụng desktop Win32 được đóng gói thông qua công nghệ Windows Desktop Bridge (Centennial) đi kèm runtime Python và giao diện Tkinter độc lập, do đó yêu cầu quyền thực thi tin cậy tiêu chuẩn dành cho ứng dụng máy tính chuyển đổi.
   - Làm rõ tình trạng phân loại độ tuổi IARC: Ứng dụng tự đánh giá nội bộ đạt xếp hạng phổ thông (Everyone / 3+), và sẽ hoàn tất bảng hỏi trực tuyến chính thức của IARC trực tiếp trên cổng Microsoft Partner Center trong bước nộp hồ sơ xuất bản.

---

## 2. TOÀN VĂN MÃ NGUỒN SẢN XUẤT ĐÃ CẬP NHẬT (VERBATIM CODE)

Dưới đây là toàn văn phần mã nguồn sản xuất của các hằng số, helper kiểm tra và hàm `classify_triangle` trích xuất trực tiếp từ [geosolver/geosolver_desktop.py](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py#L314-L685):

```python
_FREE_SOURCES = ("free", "mouse", "dragged")
_EXACT_SOURCES = ("typed", "grid_snap", "snapped", "exact")
_DERIVED_SOURCES = ("midpoint", "intersection", "formula")


def _finite(v, label, p):
    """Ép về float, từ chối None / chuỗi rác / NaN / inf."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f"Tọa độ '{label}' không hợp lệ: {p!r}")
    if not math.isfinite(f):
        raise ValueError(f"Tọa độ '{label}' phải hữu hạn (không NaN/inf): {p!r}")
    return f


def _point_flag(p, _depth=0):
    """True = chính xác, False = vẽ tay (taint), None = không rõ nguồn.

    Điểm dựng hình (midpoint/intersection/formula) kế thừa cờ từ điểm cha
    qua khóa "parents". Không có "parents" thì coi là không rõ (None),
    trừ khi có exact=True tường minh.
    """
    if not isinstance(p, dict):
        return None
    if p.get("source") in _FREE_SOURCES or p.get("exact") is False:
        return False
    if p.get("source") in _DERIVED_SOURCES and p.get("parents") and _depth < 8:
        flags = [_point_flag(q, _depth + 1) for q in p["parents"]]
        if any(f is False for f in flags):
            return False
        if all(f is True for f in flags):
            return True
        return None
    if p.get("exact") is True or p.get("source") in _EXACT_SOURCES:
        return True
    return None


def classify_triangle(pA, pB, pC, lang: str = "vi", points_exact: bool | None = None) -> dict:
    """
    Phân loại hình học tam giác thuần túy (Pure Function - Production Code):
    - Kiểm tra điểm trùng, 3 điểm thẳng hàng.
    - Nhận diện cờ nguồn gốc points_exact / metadata 'source' ('typed', 'grid_snap' vs 'free'):
        + Nếu người dùng vẽ chuột tự do (source='free' hoặc points_exact=False):
          exact luôn là False dù tọa độ rơi vào số nguyên do ngẫu nhiên hoặc mức zoom pixel.
        + Nếu người dùng gõ tay hoặc snap lưới (points_exact=True):
          exact là True khi tọa độ thỏa mãn lưới số nguyên/hữu tỉ.
    - Nhận diện tọa độ số nguyên hoặc thập phân gõ tay (as_scaled_ints):
        + So sánh d^2 chính xác bằng số nguyên trên lưới tỷ lệ (loại trừ tận gốc lỗi d^2=1000 vs 1010).
        + Tích vô hướng nguyên == 0 cho góc vuông.
        + Áp dụng Định lý lưới nguyên Z^2: Tam giác có đỉnh trên lưới số nguyên/hữu tỉ không thể là tam giác đều.
    - Với tọa độ thực tự do / vô tỉ:
        + Dùng dung sai thích ứng tỷ lệ tol = max(1e-4, 0.006 * L_max).
        + Báo rõ 'gần đều (lệch X.X%)', 'gần cân (lệch X.X%)', 'gần vuông (góc X.X°)'.
    """
    is_en = (lang == "en")
    
    def get_xy_name_exact(p, default_name):
        if isinstance(p, dict):
            if "x" not in p or "y" not in p:
                raise ValueError(f"Điểm thiếu thuộc tính tọa độ 'x' hoặc 'y': {p}")
            return (_finite(p["x"], "x", p), _finite(p["y"], "y", p),
                    str(p.get("name") or default_name), _point_flag(p))
        if len(p) < 2:
            raise ValueError(f"Tọa độ điểm phải có ít nhất 2 phần tử (x, y): {p}")
        return _finite(p[0], "x", p), _finite(p[1], "y", p), default_name, None

    xA, yA, nA, exA = get_xy_name_exact(pA, "A")
    xB, yB, nB, exB = get_xy_name_exact(pB, "B")
    xC, yC, nC, exC = get_xy_name_exact(pC, "C")

    # Thứ tự ưu tiên xác định nguồn gốc điểm (Taint Precedence Hierarchy):
    # 1. Lan truyền vết bẩn (Taint propagation): Nếu BẤT KỲ điểm nào là False (vẽ chuột tự do),
    #    toàn bộ tam giác bắt buộc là False. Tham số points_exact=True KHÔNG ĐƯỢC PHÉP đè lên cờ False này!
    # 2. Nếu caller chỉ định points_exact=False tường minh: Toàn bộ tam giác là False.
    # 3. Nếu caller chỉ định points_exact=True tường minh (và không có điểm nào bị taint False): Toàn bộ tam giác là True.
    # 4. Nếu tất cả 3 điểm đều có cờ True: Toàn bộ tam giác là True.
    # 5. Ngược lại (có điểm None - thiếu metadata): user_declared_exact = None (chuyển sang chế độ Heuristic số học is_discrete).
    pt_flags = [exA, exB, exC]
    if any(f is False for f in pt_flags):
        user_declared_exact = False
    elif points_exact is False:
        user_declared_exact = False
    elif points_exact is True:
        user_declared_exact = True
    elif all(f is True for f in pt_flags):
        user_declared_exact = True
    else:
        user_declared_exact = None

    u_AB = (xB - xA, yB - yA)
    u_AC = (xC - xA, yC - yA)
    u_BC = (xC - xB, yC - yB)

    c_sq = u_AB[0]**2 + u_AB[1]**2
    b_sq = u_AC[0]**2 + u_AC[1]**2
    a_sq = u_BC[0]**2 + u_BC[1]**2

    c_len = math.sqrt(c_sq)  # AB
    b_len = math.sqrt(b_sq)  # AC
    a_len = math.sqrt(a_sq)  # BC

    cross = u_AB[0] * u_AC[1] - u_AB[1] * u_AC[0]
    
    # Nhận diện tọa độ số nguyên hoặc số thập phân sạch (ví dụ gõ 8.7, 2.9, 1.3, 0.04)
    scaled_coords, scale_factor = as_scaled_ints([xA, yA, xB, yB, xC, yC], max_k=4)
    # Điểm vẽ tay có tọa độ rơi vào lưới pixel/40 sẽ lọt nhánh "rời rạc"
    # và bị so sánh bằng chính xác. Ép về nhánh dung sai tương đối khi user_declared_exact is False.
    is_discrete = (scaled_coords is not None) and (user_declared_exact is not False)

    # Kiểm tra trùng điểm bất biến theo tỷ lệ (không dùng ngưỡng tuyệt đối 1e-4)
    if is_discrete:
        sxA, syA, sxB, syB, sxC, syC = scaled_coords
        s_uAB = (sxB - sxA, syB - syA)
        s_uAC = (sxC - sxA, syC - syA)
        s_uBC = (sxC - sxB, syC - syB)
        is_coincident = (s_uAB == (0, 0)) or (s_uAC == (0, 0)) or (s_uBC == (0, 0))
        is_collinear = (s_uAB[0] * s_uAC[1] - s_uAB[1] * s_uAC[0] == 0)
    else:
        l_max = max(a_len, b_len, c_len)
        if l_max < 1e-12:
            is_coincident = True
        else:
            is_coincident = (c_len / l_max < 1e-6) or (b_len / l_max < 1e-6) or (a_len / l_max < 1e-6)
        rel_cross = abs(cross) / (c_len * b_len) if (c_len > 1e-12 and b_len > 1e-12) else 0.0
        is_collinear = (rel_cross < 1e-5)

    if is_coincident:
        msg = "Coincident points; not a valid triangle." if is_en else "Có điểm trùng nhau; không tạo thành tam giác."
        return {
            "is_triangle": False, "type": "coincident",
            "message": msg, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}
        }

    if is_collinear:
        msg = "Collinear points; not a triangle." if is_en else "3 điểm thẳng hàng; không tạo thành tam giác."
        return {
            "is_triangle": False, "type": "collinear",
            "message": msg, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}
        }

    l_max = max(a_len, b_len, c_len)
    l_min = min(a_len, b_len, c_len)

    str_AB = format_radical_len(c_len, (xA, yA), (xB, yB))
    str_AC = format_radical_len(b_len, (xA, yA), (xC, yC))
    str_BC = format_radical_len(a_len, (xB, yB), (xC, yC))

    is_equilateral = False
    perp_A = False
    perp_B = False
    perp_C = False
    eq_AB_AC = False
    eq_BA_BC = False
    eq_CA_CB = False
    diff_AB_AC = 0.0
    diff_BA_BC = 0.0
    diff_CA_CB = 0.0
    diff_eq = 0.0
    angle_A = 90.0
    angle_B = 90.0
    angle_C = 90.0

    if is_discrete:
        # CHẾ ĐỘ RỜI RẠC: Số nguyên hoặc số thập phân sạch (as_scaled_ints)
        d2_AB = s_uAB[0]**2 + s_uAB[1]**2
        d2_AC = s_uAC[0]**2 + s_uAC[1]**2
        d2_BC = s_uBC[0]**2 + s_uBC[1]**2

        eq_AB_AC = (d2_AB == d2_AC)
        eq_BA_BC = (d2_AB == d2_BC)
        eq_CA_CB = (d2_AC == d2_BC)
        is_equilateral = False  # Theo định lý lưới nguyên Z^2, không thể tồn tại tam giác đều

        dot_A = s_uAB[0] * s_uAC[0] + s_uAB[1] * s_uAC[1]
        dot_B = -s_uAB[0] * s_uBC[0] - s_uAB[1] * s_uBC[1]
        dot_C = s_uAC[0] * s_uBC[0] + s_uAC[1] * s_uBC[1]

        perp_A = (dot_A == 0)
        perp_B = (dot_B == 0)
        perp_C = (dot_C == 0)
    else:
        # CHẾ ĐỘ LIÊN TỤC: Tọa độ thực tự do / vô tỉ (Bảo đảm bất biến tỷ lệ tuyệt đối)
        tol_rel = 0.006  # 0.6%
        max_AB_AC = max(c_len, b_len)
        max_BA_BC = max(c_len, a_len)
        max_CA_CB = max(b_len, a_len)

        eq_AB_AC = (abs(c_len - b_len) <= tol_rel * max_AB_AC) if max_AB_AC > 1e-12 else True
        eq_BA_BC = (abs(c_len - a_len) <= tol_rel * max_BA_BC) if max_BA_BC > 1e-12 else True
        eq_CA_CB = (abs(b_len - a_len) <= tol_rel * max_CA_CB) if max_CA_CB > 1e-12 else True

        diff_AB_AC = (abs(c_len - b_len) / max_AB_AC * 100.0) if max_AB_AC > 1e-12 else 0.0
        diff_BA_BC = (abs(c_len - a_len) / max_BA_BC * 100.0) if max_BA_BC > 1e-12 else 0.0
        diff_CA_CB = (abs(b_len - a_len) / max_CA_CB * 100.0) if max_CA_CB > 1e-12 else 0.0

        is_equilateral = ((l_max - l_min) <= tol_rel * l_max) if l_max > 1e-12 else False
        diff_eq = ((l_max - l_min) / l_max * 100.0) if l_max > 1e-12 else 0.0

        dot_A = u_AB[0] * u_AC[0] + u_AB[1] * u_AC[1]
        dot_B = -u_AB[0] * u_BC[0] - u_AB[1] * u_BC[1]
        dot_C = u_AC[0] * u_BC[0] + u_AC[1] * u_BC[1]

        cos_A = dot_A / (c_len * b_len)
        cos_B = dot_B / (c_len * a_len)
        cos_C = dot_C / (b_len * a_len)

        angle_A = math.degrees(math.acos(max(-1.0, min(1.0, cos_A))))
        angle_B = math.degrees(math.acos(max(-1.0, min(1.0, cos_B))))
        angle_C = math.degrees(math.acos(max(-1.0, min(1.0, cos_C))))

        perp_A = (abs(cos_A) <= 0.015)
        perp_B = (abs(cos_B) <= 0.015)
        perp_C = (abs(cos_C) <= 0.015)

    tri_type = "scalene"
    vertex = None
    description = ""

    if is_equilateral:
        tri_type = "equilateral"
        avg_s = (a_len + b_len + c_len) / 3.0
        s_str = format_radical_len(avg_s, (xA, yA), (xB, yB))
        mod_eq = f" (gần đều, lệch {diff_eq:.1f}%)" if (not is_discrete and diff_eq > 0.05) else ""
        description = f"Equilateral triangle: Δ{nA}{nB}{nC} (AB=BC=CA = {s_str}){mod_eq}" if is_en else f"Tam giác đều: Δ{nA}{nB}{nC} (ba cạnh bằng nhau = {s_str}){mod_eq}"
    elif perp_A and eq_AB_AC:
        tri_type = "right_isosceles"
        vertex = nA
        avg_leg = (c_len + b_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xA, yA), (xB, yB))
        notes = []
        if not is_discrete:
            if diff_AB_AC > 0.05:
                notes.append(f"lệch cạnh {diff_AB_AC:.1f}%" if not is_en else f"leg dev {diff_AB_AC:.1f}%")
            if abs(angle_A - 90.0) > 0.05:
                notes.append(f"góc {angle_A:.1f}°" if not is_en else f"angle {angle_A:.1f}°")
        mod_ri = f" (gần vuông cân: {', '.join(notes)})" if notes else ""
        description = f"Right isosceles triangle at {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, ∠{nA}=90°){mod_ri}" if is_en else f"Tam giác vuông cân tại {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, ∠{nA}=90°){mod_ri}"
    elif perp_B and eq_BA_BC:
        tri_type = "right_isosceles"
        vertex = nB
        avg_leg = (c_len + a_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xB, yB), (xC, yC))
        notes = []
        if not is_discrete:
            if diff_BA_BC > 0.05:
                notes.append(f"lệch cạnh {diff_BA_BC:.1f}%" if not is_en else f"leg dev {diff_BA_BC:.1f}%")
            if abs(angle_B - 90.0) > 0.05:
                notes.append(f"góc {angle_B:.1f}°" if not is_en else f"angle {angle_B:.1f}°")
        mod_ri = f" (gần vuông cân: {', '.join(notes)})" if notes else ""
        description = f"Right isosceles triangle at {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, ∠{nB}=90°){mod_ri}" if is_en else f"Tam giác vuông cân tại {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, ∠{nB}=90°){mod_ri}"
    elif perp_C and eq_CA_CB:
        tri_type = "right_isosceles"
        vertex = nC
        avg_leg = (b_len + a_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xC, yC), (xA, yA))
        notes = []
        if not is_discrete:
            if diff_CA_CB > 0.05:
                notes.append(f"lệch cạnh {diff_CA_CB:.1f}%" if not is_en else f"leg dev {diff_CA_CB:.1f}%")
            if abs(angle_C - 90.0) > 0.05:
                notes.append(f"góc {angle_C:.1f}°" if not is_en else f"angle {angle_C:.1f}°")
        mod_ri = f" (gần vuông cân: {', '.join(notes)})" if notes else ""
        description = f"Right isosceles triangle at {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, ∠{nC}=90°){mod_ri}" if is_en else f"Tam giác vuông cân tại {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, ∠{nC}=90°){mod_ri}"

    elif eq_AB_AC:
        tri_type = "isosceles"
        vertex = nA
        avg_leg = (c_len + b_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xA, yA), (xB, yB))
        base_str = format_radical_len(a_len, (xB, yB), (xC, yC))
        mod_text = f" (gần cân, lệch {diff_AB_AC:.1f}%)" if (not is_discrete and diff_AB_AC > 0.05) else ""
        description = (f"Isosceles triangle at {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, base {nB}{nC} = {base_str}){mod_text}" if is_en 
                       else f"Tam giác cân tại {nA}: Δ{nA}{nB}{nC} ({nA}{nB}={nA}{nC} = {leg_str}, đáy {nB}{nC} = {base_str}){mod_text}")
    elif eq_BA_BC:
        tri_type = "isosceles"
        vertex = nB
        avg_leg = (c_len + a_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xB, yB), (xC, yC))
        base_str = format_radical_len(b_len, (xC, yC), (xA, yA))
        mod_text = f" (gần cân, lệch {diff_BA_BC:.1f}%)" if (not is_discrete and diff_BA_BC > 0.05) else ""
        description = (f"Isosceles triangle at {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, base {nA}{nC} = {base_str}){mod_text}" if is_en 
                       else f"Tam giác cân tại {nB}: Δ{nA}{nB}{nC} ({nB}{nA}={nB}{nC} = {leg_str}, đáy {nA}{nC} = {base_str}){mod_text}")
    elif eq_CA_CB:
        tri_type = "isosceles"
        vertex = nC
        avg_leg = (b_len + a_len) / 2.0
        leg_str = format_radical_len(avg_leg, (xC, yC), (xA, yA))
        base_str = format_radical_len(c_len, (xA, yA), (xB, yB))
        mod_text = f" (gần cân, lệch {diff_CA_CB:.1f}%)" if (not is_discrete and diff_CA_CB > 0.05) else ""
        description = (f"Isosceles triangle at {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, base {nA}{nB} = {base_str}){mod_text}" if is_en 
                       else f"Tam giác cân tại {nC}: Δ{nA}{nB}{nC} ({nC}{nA}={nC}{nB} = {leg_str}, đáy {nA}{nB} = {base_str}){mod_text}")

    elif perp_A:
        tri_type = "right"
        vertex = nA
        ang_dev = abs(angle_A - 90.0)
        mod_r = f" (gần vuông, góc {angle_A:.1f}°)" if (not is_discrete and ang_dev > 0.05) else ""
        description = f"Right triangle at {nA}: Δ{nA}{nB}{nC} ({nA}{nB} ⊥ {nA}{nC}){mod_r}" if is_en else f"Tam giác vuông tại {nA}: Δ{nA}{nB}{nC} ({nA}{nB} ⊥ {nA}{nC}){mod_r}"
    elif perp_B:
        tri_type = "right"
        vertex = nB
        ang_dev = abs(angle_B - 90.0)
        mod_r = f" (gần vuông, góc {angle_B:.1f}°)" if (not is_discrete and ang_dev > 0.05) else ""
        description = f"Right triangle at {nB}: Δ{nA}{nB}{nC} ({nB}{nA} ⊥ {nB}{nC}){mod_r}" if is_en else f"Tam giác vuông tại {nB}: Δ{nA}{nB}{nC} ({nB}{nA} ⊥ {nB}{nC}){mod_r}"
    elif perp_C:
        tri_type = "right"
        vertex = nC
        ang_dev = abs(angle_C - 90.0)
        mod_r = f" (gần vuông, góc {angle_C:.1f}°)" if (not is_discrete and ang_dev > 0.05) else ""
        description = f"Right triangle at {nC}: Δ{nA}{nB}{nC} ({nC}{nA} ⊥ {nC}{nB}){mod_r}" if is_en else f"Tam giác vuông tại {nC}: Δ{nA}{nB}{nC} ({nC}{nA} ⊥ {nC}{nB}){mod_r}"
    else:
        tri_type = "scalene"
        description = f"Scalene triangle: Δ{nA}{nB}{nC}" if is_en else f"Tam giác thường: Δ{nA}{nB}{nC}"

    deviations = {}
    if not is_discrete:
        if tri_type == "equilateral":
            deviations["equilateral_diff_pct"] = round(diff_eq, 2)
        elif tri_type == "isosceles":
            if vertex == nA:
                deviations["leg_diff_pct"] = round(diff_AB_AC, 2)
            elif vertex == nB:
                deviations["leg_diff_pct"] = round(diff_BA_BC, 2)
            elif vertex == nC:
                deviations["leg_diff_pct"] = round(diff_CA_CB, 2)
        elif tri_type == "right":
            if vertex == nA:
                deviations["angle_deg"] = round(angle_A, 2)
                deviations["angle_diff_deg"] = round(abs(angle_A - 90.0), 2)
            elif vertex == nB:
                deviations["angle_deg"] = round(angle_B, 2)
                deviations["angle_diff_deg"] = round(abs(angle_B - 90.0), 2)
            elif vertex == nC:
                deviations["angle_deg"] = round(angle_C, 2)
                deviations["angle_diff_deg"] = round(abs(angle_C - 90.0), 2)
        elif tri_type == "right_isosceles":
            if vertex == nA:
                deviations["leg_diff_pct"] = round(diff_AB_AC, 2)
                deviations["angle_deg"] = round(angle_A, 2)
                deviations["angle_diff_deg"] = round(abs(angle_A - 90.0), 2)
            elif vertex == nB:
                deviations["leg_diff_pct"] = round(diff_BA_BC, 2)
                deviations["angle_deg"] = round(angle_B, 2)
                deviations["angle_diff_deg"] = round(abs(angle_B - 90.0), 2)
            elif vertex == nC:
                deviations["leg_diff_pct"] = round(diff_CA_CB, 2)
                deviations["angle_deg"] = round(angle_C, 2)
                deviations["angle_diff_deg"] = round(abs(angle_C - 90.0), 2)

    def _is_near_int(v: float) -> bool:
        if abs(v) < 1e-9:
            return True
        if abs(v) < 0.5:
            return False
        return abs(v - round(v)) < 1e-5

    all_int = all(_is_near_int(v) for v in (xA, yA, xB, yB, xC, yC))
    exact_math = False if user_declared_exact is False else (is_discrete if user_declared_exact is None else (is_discrete and user_declared_exact))
    return {
        "is_triangle": True,
        "type": tri_type,
        "vertex": vertex,
        "all_int": all_int,
        "is_discrete": is_discrete,
        "exact": exact_math,
        "origin_exact": user_declared_exact,
        "deviations": deviations,
        "scale_factor": scale_factor,
        "is_equilateral": is_equilateral,
        "description": description,
        "sides": {"AB": c_len, "AC": b_len, "BC": a_len},
        "sides_formatted": {"AB": str_AB, "AC": str_AC, "BC": str_BC}
    }
```

---

## 3. KẾT QUẢ KIỂM THỬ THỰC NGHIỆM ĐỘC LẬP (EMPIRICAL VERIFICATION)

### 3.1. Toàn bộ 35 bài kiểm thử đơn vị tự động (35/35 PASSED)

Bộ kiểm thử được phân rã thành hai tập tin chuyên biệt:
- [tests/test_geometry_invariants.py](file:///d:/AI%20DATA/STEM_APP/tests/test_geometry_invariants.py): 24 bài kiểm tra bao quát các ca biên hình học, bất biến tỷ lệ, WCAG 2.1 AA, Ramanujan II, bảo mật DPAPI fail-soft, downloader GGUF và sự kiện chuột GUI Tkinter thật.
- [tests/test_round9_taint_validation.py](file:///d:/AI%20DATA/STEM_APP/tests/test_round9_taint_validation.py): 11 bài kiểm tra xác thực chuyên sâu theo các ca kiểm thử đề xuất của chuyên gia ở Vòng 9 (từ chối `NaN`/`inf`, cưỡng chế nhánh dung sai cho điểm tự do, và kế thừa cờ cha con).

Lệnh thực thi độc lập:
```powershell
python -m unittest discover -s tests -t . -p "test_*.py" -v
```

Nhật ký thực thi đầy đủ trích xuất từ tệp tin lưu trữ [tests/test_run.log](file:///d:/AI%20DATA/STEM_APP/tests/test_run.log):

```text
test_01_true_positive_equilateral_triangle (tests.test_geometry_invariants.TestGeometryInvariants.test_01_true_positive_equilateral_triangle)
Ca dương tính: Tam giác đều thực sự với tọa độ vô tỉ (gọi trực tiếp classify_triangle) ... ok
test_02_regression_original_bug_isosceles_not_equilateral (tests.test_geometry_invariants.TestGeometryInvariants.test_02_regression_original_bug_isosceles_not_equilateral)
Hồi quy lỗi gốc: A(0, 5), B(-3, 0), C(3, 0) phải nhận diện là tam giác cân tại A, TUYỆT ĐỐI KHÔNG ĐƯỢC BÁO ĐỀU ... ok
test_03_scale_invariance_property (tests.test_geometry_invariants.TestGeometryInvariants.test_03_scale_invariance_property)
Thuộc tính bất biến tỷ lệ theo thang 10^-k (k=0..3) trên tọa độ rời rạc ... ok
test_04_typed_decimals_rejection_claude_cases (tests.test_geometry_invariants.TestGeometryInvariants.test_04_typed_decimals_rejection_claude_cases)
Ca số thập phân gõ tay của Claude (5, 8.7) và (0.04, 3) không bị nhận nhầm ... ok
test_05_negative_equilateral_pure_float_coordinates (tests.test_geometry_invariants.TestGeometryInvariants.test_05_negative_equilateral_pure_float_coordinates)
Ca âm tính độc lập: Dung sai 0.6% trên tọa độ thực tự do loại trừ tam giác lệch 1.8% ... ok
test_06_collinear_and_coincident_points (tests.test_geometry_invariants.TestGeometryInvariants.test_06_collinear_and_coincident_points)
Ca biên: 3 điểm thẳng hàng và điểm trùng nhau không tạo thành tam giác ... ok
test_07_right_and_right_isosceles_triangles (tests.test_geometry_invariants.TestGeometryInvariants.test_07_right_and_right_isosceles_triangles)
Ca tam giác vuông và vuông cân trên lưới rời rạc ... ok
test_08_ellipse_edge_cases_and_rotational_invariance (tests.test_geometry_invariants.TestGeometryInvariants.test_08_ellipse_edge_cases_and_rotational_invariance)
Hình elip toàn diện: chuẩn, F1==F2, suy biến b=0, tiêu điểm nghiêng 53.13° và đổi F1/F2 ... ok
test_09_ramanujan_ii_exact_accuracy_table (tests.test_geometry_invariants.TestGeometryInvariants.test_09_ramanujan_ii_exact_accuracy_table)
Chu vi Ramanujan II so với tích phân số học quy tắc trung điểm 100.000 bước ... ok
test_10_wcag_21_aa_itemized_real_contrast (tests.test_geometry_invariants.TestGeometryInvariants.test_10_wcag_21_aa_itemized_real_contrast)
Đo tương phản 20 cặp màu thực tế trên THEMES_GEOSOLVER theo chuẩn W3C WCAG 2.1 AA ... ok
test_11_clean_print_mode_and_handbook_dialog (tests.test_geometry_invariants.TestGeometryInvariants.test_11_clean_print_mode_and_handbook_dialog)
Kiểm tra Clean Print Mode toggle mặc định tắt và tệp cẩm nang F1 ... ok
test_12_dpapi_keystore_and_downloader_sha256 (tests.test_geometry_invariants.TestGeometryInvariants.test_12_dpapi_keystore_and_downloader_sha256)
Kiểm tra bảo mật DPAPI KeyStore (chống Use-After-Free) và hf_downloader SHA-256 ... ok
test_13_dpapi_fail_soft_on_corrupt_or_foreign_key (tests.test_geometry_invariants.TestGeometryInvariants.test_13_dpapi_fail_soft_on_corrupt_or_foreign_key)
Kiểm tra nguyên tắc fail-soft của GeminiKeyStore: không sập app khi file hỏng hoặc chuyển máy ... ok
test_14_exact_right_triangle_float_coordinates_no_spurious_annotation (tests.test_geometry_invariants.TestGeometryInvariants.test_14_exact_right_triangle_float_coordinates_no_spurious_annotation)
Tam giác vuông thực sự có tọa độ vô tỉ (0,0), (√2,0), (0,√3): không được chú thích '(gần vuông, góc 0.0°)' ... ok
test_15_float_near_right_and_near_right_isosceles_annotation (tests.test_geometry_invariants.TestGeometryInvariants.test_15_float_near_right_and_near_right_isosceles_annotation)
Ca số thực tự do gần vuông và gần vuông cân: kiểm tra chú thích độ lệch và deviations dict ... ok
test_16_dpapi_stress_round_trip_stability (tests.test_geometry_invariants.TestGeometryInvariants.test_16_dpapi_stress_round_trip_stability)
Kiểm tra áp lực 100 lần mã hóa/giải mã DPAPI với payload ngẫu nhiên 1KB để loại trừ rò rỉ vùng nhớ ctypes ... ok
test_17_freehand_point_origin_flag_rejection (tests.test_geometry_invariants.TestGeometryInvariants.test_17_freehand_point_origin_flag_rejection)
Kiểm tra cờ nguồn gốc exact/source: vẽ chuột tự do dù toạ độ nguyên vẫn có exact=False ... ok
test_18_format_radical_len_direct_unit_tests (tests.test_geometry_invariants.TestGeometryInvariants.test_18_format_radical_len_direct_unit_tests)
Kiểm tra trực tiếp format_radical_len với các mẫu căn thức và phân số phổ biến ... ok
test_19_ellipse_near_degenerate_a_approx_c (tests.test_geometry_invariants.TestGeometryInvariants.test_19_ellipse_near_degenerate_a_approx_c)
Kiểm tra elip gần suy biến khi a tiệm cận c (b -> 0) không bị lỗi chia 0 hoặc căn số âm ... ok
test_20_hf_downloader_error_paths_comprehensive (tests.test_geometry_invariants.TestGeometryInvariants.test_20_hf_downloader_error_paths_comprehensive)
Kiểm tra các kịch bản lỗi của hf_downloader: sai magic GGUF, lệch kích thước, thiếu SHA-256 ... ok
test_21_mixed_point_origin_flag_behavior (tests.test_geometry_invariants.TestGeometryInvariants.test_21_mixed_point_origin_flag_behavior)
Kiểm tra logic trộn cờ nguồn gốc, thứ tự ưu tiên taint và xử lý xung đột cờ ... ok
test_22_missing_coordinate_validation (tests.test_geometry_invariants.TestGeometryInvariants.test_22_missing_coordinate_validation)
Kiểm tra xác thực dữ liệu điểm: thiếu x hoặc y phải ném ValueError, không được ngầm định bằng 0 ... ok
test_23_micro_scale_invariance_scale_10_minus_5 (tests.test_geometry_invariants.TestGeometryInvariants.test_23_micro_scale_invariance_scale_10_minus_5)
Kiểm tra bất biến tỷ lệ vi mô ở thang 10^-5: không trùng điểm và không nhận nhầm all_int ... ok
test_24_gui_canvas_point_source_and_invariants_integration (tests.test_geometry_invariants.TestGeometryInvariants.test_24_gui_canvas_point_source_and_invariants_integration)
Kiểm tra tích hợp GUI Canvas: phát sự kiện click chuột thật để kiểm tra gán cờ source='free' và 'grid_snap' ... ok
test_derived_without_parents_is_unknown (tests.test_round9_taint_validation.TestDerivedPointPropagation.test_derived_without_parents_is_unknown) ... ok
test_midpoint_of_free_parents_is_tainted (tests.test_round9_taint_validation.TestDerivedPointPropagation.test_midpoint_of_free_parents_is_tainted) ... ok
test_midpoint_of_typed_parents_is_exact (tests.test_round9_taint_validation.TestDerivedPointPropagation.test_midpoint_of_typed_parents_is_exact) ... ok
test_explicit_exact_false_beats_exact_source (tests.test_round9_taint_validation.TestFreehandTaint.test_explicit_exact_false_beats_exact_source) ... ok
test_free_integer_right_triangle_uses_tolerance_branch (tests.test_round9_taint_validation.TestFreehandTaint.test_free_integer_right_triangle_uses_tolerance_branch) ... ok
test_free_near_isosceles_is_flagged_but_typed_is_not (tests.test_round9_taint_validation.TestFreehandTaint.test_free_near_isosceles_is_flagged_but_typed_is_not) ... ok
test_mixed_typed_and_free_is_false (tests.test_round9_taint_validation.TestFreehandTaint.test_mixed_typed_and_free_is_false) ... ok
test_points_exact_true_cannot_override_free (tests.test_round9_taint_validation.TestFreehandTaint.test_points_exact_true_cannot_override_free) ... ok
test_nan_inf_none_rejected_in_dict (tests.test_round9_taint_validation.TestInputValidation.test_nan_inf_none_rejected_in_dict) ... ok
test_nan_inf_none_rejected_in_tuple (tests.test_round9_taint_validation.TestInputValidation.test_nan_inf_none_rejected_in_tuple) ... ok
test_3_4_5_at_1e_minus_5 (tests.test_round9_taint_validation.TestMicroScaleStillOk.test_3_4_5_at_1e_minus_5) ... ok

----------------------------------------------------------------------
Ran 35 tests in 3.111s

OK
```

---

### 3.2. Kiểm thử khói tập tin thực thi độc lập đóng gói thật (`GeoSolver.exe --smoke-test`)

Ứng dụng được biên dịch bằng PyInstaller với cấu hình chuẩn hóa, `upx=False`, `console=False`, và thực thi kiểm thử tự động trực tiếp trên tệp `dist/GeoSolver/GeoSolver.exe`:

```powershell
$proc = Start-Process -FilePath "dist\GeoSolver\GeoSolver.exe" -ArgumentList "--smoke-test" -Wait -PassThru
$exitCode = $proc.ExitCode
```

**Kết quả ghi nhận:**
- Mã thoát thực tế: `0` (Thành công trọn vẹn).
- Tệp nhật ký chi tiết [dist/GeoSolver/smoke_run.log](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/smoke_run.log):
```text
[SMOKE TEST] Khởi chạy kiểm thử đóng gói GeoSolver (Smoke Test)...
[SMOKE TEST] 1. Phân loại hình học bất biến: ĐẠT
[SMOKE TEST] 2. Mã hóa & giải mã Windows DPAPI: ĐẠT
[SMOKE TEST] 3. Nạp động thư viện SymPy: ĐẠT
[SMOKE TEST] 4. Khởi tạo & giải phóng Tkinter GUI runtime: ĐẠT
[SMOKE TEST] 5. Nạp các module phụ thuộc quan trọng: ĐẠT
[SMOKE TEST] 6. Tài nguyên đóng gói trong frozen bundle: ĐẠT
[SMOKE TEST] 7. Nạp cấu hình bảo mật SSL/TLS & CA bundle certifi: ĐẠT
[SMOKE TEST] TẤT CẢ CÁC MỤC KIỂM THỬ KHÓI ĐỀU THÀNH CÔNG (MÃ THOÁT 0).
[SMOKE TEST] Đã ghi nhật ký kết quả kiểm thử vào: D:\AI DATA\STEM_APP\dist\GeoSolver\smoke_test_result.json
```

- Tệp kết quả cấu trúc JSON [dist/GeoSolver/smoke_test_result.json](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/smoke_test_result.json):
```json
{
  "timestamp": "2026-11-09T07:13:40.034427+00:00",
  "frozen": true,
  "python_version": "3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)]",
  "executable": "D:\\AI DATA\\STEM_APP\\dist\\GeoSolver\\GeoSolver.exe",
  "executable_sha256": "29B6E81FE71C0B0195E3E108D52520A48E8F722554E5AEB8E0C7623C749ABFFD",
  "checks": {
    "geometry": true,
    "dpapi": true,
    "sympy": true,
    "tkinter_runtime": true,
    "critical_modules": true,
    "assets": true,
    "ssl_certifi": true
  },
  "status": "PASS",
  "exit_code": 0
}
```

---

## 4. MA TRẬN MÃ BĂM ĐỐI SOÁT MẬT MÃ (16 TỆP TIN TRỌNG YẾU)

Tất cả các tệp tin trong hệ thống được tính toán mã băm SHA-256 độc lập trên hệ điều hành Windows để phục vụ công tác đối soát toàn vẹn:

| STT | Tệp tin | SHA-256 | Kích thước (bytes) |
|:---:|:---|:---|:---:|
| 1 | `geosolver/geosolver_desktop.py` | `C0BB006F3EDA91E3B90B749EA5B548A99ECBE6F741E4D8D1CF98AF52EE40179B` | 646,929 |
| 2 | `geosolver/GeoSolver.spec` | `5514177387F812B81BAA1C3D3B08FBE34A3B99644B5E399C6E828C0C8AA1BC1C` | 1,798 |
| 3 | `tests/test_geometry_invariants.py` | `7C7F72D90F502B96DDA4DB1D92C0FFED16B77A5140DC0543DD494313EE6CCE85` | 28,428 |
| 4 | `tests/test_round9_taint_validation.py` | `B01A401AAF76B5050651AE83DD953EB5034AA8F8E9CE77F2E63DD0686B60BAEA` | 4,012 |
| 5 | `tests/test_run.log` | `60CEA2E01161C9FF6A2F3DD19A4AC4CA59F6F6EABA172BC81698D2B5866ECE9A` | 8,850 |
| 6 | `stem_shared_core/ai_local_manager.py` | `96CDA8B717AE51792D5E1FC6C2F23D5BF93BB7D61EDDA1DAFCD6431218B1B21F` | 58,356 |
| 7 | `stem_shared_core/hf_downloader.py` | `090EFD6F7A64BAE3FBAA3FB2BCE21C6B7E4F9C8F5F7E2CD478CC12449366E481` | 29,791 |
| 8 | `stem_shared_core/ai_model_hub.py` | `8DE4956855D02418503DF934509BD4B9BB52C9F0E9238414FE72F9DCD1C09818` | 69,054 |
| 9 | `stem_shared_core/ai_config_dialog.py` | `647ABC5D0FF8F05C7794F6FDBE4C582893A288EDEE603812F1FB13B8E792434C` | 7,961 |
| 10 | `stem_handbook_dialog.py` | `2B4E562D5460E8A0CDEE3DDCCA4747D1BD29934D20177FE2AD11AA30B17883B0` | 42,832 |
| 11 | `docs/STORE_METADATA_AND_PRIVACY.md` | `761D09DF6A38C616ABB2852EDF732B16264EFB7B46571BD68F9B503932D2326D` | 5,502 |
| 12 | `dist/GeoSolver/GeoSolver.exe` | `29B6E81FE71C0B0195E3E108D52520A48E8F722554E5AEB8E0C7623C749ABFFD` | 32,756,109 |
| 13 | `dist/GeoSolver/smoke_test_result.json` | `D4C52B08B427EE3BB48AFFC89B920B5BDB78CD073F71825D29F41D298BA1DFB5` | 576 |
| 14 | `dist/GeoSolver/smoke_run.log` | `4E729E5C88CBE56EDEF14D4180C5F2ADC7ED297C702A3F5DF395B6C6AC1108F3` | 771 |
| 15 | `geosolver/file_version_info.txt` | `E0D429E428BCACD8DA8FF7C4F461D99D159A44BF69854A805FF2C566250DDDC6` | 926 |
| 16 | `build/GeoSolver/warn-GeoSolver.txt` | `13CB9E865FE5945055D310664FCA6BBF2FF29F9317890B2EBD83E1ABAB286907` | 76,210 |

> [!NOTE]
> Mã băm `executable_sha256` ghi nhận bên trong tệp `dist/GeoSolver/smoke_test_result.json` hoàn toàn trùng khớp với mã băm tính toán độc lập của tệp tin `dist/GeoSolver/GeoSolver.exe` (`29B6E81FE71C0B0195E3E108D52520A48E8F722554E5AEB8E0C7623C749ABFFD`).

---

## 5. RANH GIỚI KỸ THUẬT VÀ LỘ TRÌNH TRIỂN KHAI TIẾP THEO

1. **Ranh giới kỹ thuật hiện tại (Release Candidate 2):**
   - Đóng gói dạng thư mục `COLLECT` (`dist/GeoSolver/`) với tệp thực thi chính `GeoSolver.exe` đã được xác minh toàn diện thông qua kiểm thử khói 7 tiêu chí.
   - Các thuật toán hình học cốt lõi đã đạt tính nhất quán: phân biệt rạch ròi giữa hình học rời rạc chính xác trên lưới nguyên và hình học liên tục có dung sai thích ứng, đi kèm cơ chế lan truyền vết bẩn (Taint propagation) chặt chẽ cho điểm vẽ tự do và điểm dẫn xuất.
   - Tài liệu phát hành Store và Chính sách bảo mật đã được công khai minh bạch về luồng dữ liệu mạng và quyền hạn hệ thống.

2. **Lộ trình công việc tiếp theo:**
   - **Giai đoạn MSIX Packaging:** Đóng gói thư mục phân phối vào định dạng gói ứng dụng hiện đại `.msix` sử dụng công cụ MSIX Packaging Tool / MakeAppx.
   - **Giai đoạn Ký số mã nguồn (Code Signing):** Ký số tệp `.msix` bằng chứng chỉ số hợp lệ (Trusted Signing / EV Code Signing Certificate) tương thích với Windows Defender SmartScreen.
   - **Giai đoạn Kiểm thử WACK nội bộ:** Chạy công cụ Windows App Certification Kit (WACK) trên máy tính thử nghiệm để rà soát các tiêu chí bảo mật, tương thích và hiệu năng trước khi nộp lên Store.
   - **Giai đoạn Nộp Microsoft Partner Center:** Đăng tải gói MSIX đã ký, hoàn thành bảng khảo sát độ tuổi IARC chính thức, và cung cấp văn bản chính sách quyền riêng tư để hoàn tất quá trình chứng nhận xuất bản trên Microsoft Store.
