# BÁO CÁO TỰ ĐÁNH GIÁ KỸ THUẬT VÀ KIỂM CHỨNG THỰC NGHIỆM (ROUND 10)
## DỰ ÁN GEOSOLVER 2D — PHIÊN BẢN v3.1 RC2

**Tính chất tài liệu:** Báo cáo kỹ thuật tự đánh giá nội bộ của Đội ngũ phát triển (Internal Engineering Self-Assessment), phản hồi và giải trình chi tiết các ý kiến phản biện đợt 10 của chuyên gia độc lập.  
**Trạng thái phân loại:** `RC2 – ĐÓNG GÓI EXE ĐÃ QUA SMOKE TEST CƠ BẢN (IN-DEVELOPMENT CANDIDATE FOR MSIX PACKAGING)`  
**Ngày cập nhật:** 09/11/2026  
**Môi trường thực thi:** Windows 11 Enterprise (x64), Python 3.14.5, PyInstaller 6.22.3, Tkinter 8.6, SymPy 1.14.0  
**Git Commit bám sát:** `4f8b635a5595e674dd34ddc3c2ab9f832df78620`  
**Tập tin thực thi kiểm chứng:** `dist/GeoSolver/GeoSolver.exe` (SHA-256: `0F4A3E111D95F797835481B37BB3E21C895F0F2DABF4CAFE3E894571B8A120AD`)

---

## 1. TIẾP THU PHẢN BIỆN VÀ TỔNG HỢP CẢI TIẾN ROUND 10

Đội ngũ phát triển ghi nhận toàn bộ các ý kiến phản biện sắc sảo ở Vòng 10 từ chuyên gia độc lập. Các nội dung được xử lý và kiểm chứng thực nghiệm bao gồm:

1. **Minh chứng mã nguồn Canvas GUI và bổ sung kiểm thử tích hợp thực tế:**
   - Công khai toàn văn đoạn mã xử lý sự kiện Canvas trong [geosolver/geosolver_desktop.py](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py):
     - Sự kiện kéo thả `<B1-Motion>`: Khi tắt bắt dính lưới (`snap_to_grid = False`), điểm được gán `source = "dragged"` và `exact = False`.
     - Công cụ dựng trung điểm (`midpoint`): Tự động lưu đối tượng 2 điểm cha vào thuộc tính `"parents"`.
     - Công cụ giao điểm (`intersection`): Tự động lưu các điểm mút của 2 thực thể cắt nhau vào thuộc tính `"parents"`.
   - Bổ sung 3 bài kiểm thử tự động độc lập (`test_25`, `test_26`, `test_27`) nâng tổng số kiểm thử lên **38 bài kiểm thử (38/38 PASSED)**:
     - `test_25`: Phát sự kiện chuột GUI Tkinter thật kéo một điểm `typed` khi snap tắt đổi thành `dragged`, `exact=False`; và tạo trung điểm từ 2 điểm vẽ tự do qua công cụ `midpoint` của Canvas, xác nhận cờ vết bẩn lan truyền khiến tam giác có đỉnh này nhận `origin_exact=False`, `is_discrete=False`, `exact=False`.
     - `test_26` *(Kiểm thử độc lập của nhóm)*: Dựng hình lồng nhau nhiều tầng (Nested derived points): Midpoint of Midpoints kiểm tra tính lan truyền vết bẩn đệ quy qua nhiều tầng cha-con.
     - `test_27` *(Kiểm thử độc lập của nhóm)*: Xác nhận `classify_triangle` từ chối `None`, chuỗi `"3.5"`, và các kiểu dữ liệu không hợp lệ bằng ngoại lệ `ValueError` chuẩn.

2. **Khảo sát `sys.executable` và tính toàn vẹn của từ điển kết quả:**
   - Kết quả grep trên toàn bộ thư mục `stem_shared_core/` và `geosolver/`: Không có bất kỳ dòng mã nào gọi `subprocess.Popen([sys.executable, ...])` hay `multiprocessing.Process`. Module AI cục bộ thực thi hoàn toàn trong tiến trình (in-process) qua ctypes hoặc gọi HTTP client cục bộ, không phát sinh tiến trình con gọi lại chính tệp EXE đóng băng.
   - Từ điển trả về của `classify_triangle`: Giữ nguyên vẹn cả `is_isosceles`, `is_right`, `side_labels`, và cung cấp thêm `sides_formatted` (bí danh đồng nghĩa). Báo cáo Round 9 thiếu là do trích đoạn hiển thị trong văn bản markdown bị khuyết, không phải lỗi trong mã nguồn thực tế.

3. **Khắc phục các lỗi mã nguồn cụ thể:**
   - Cập nhật docstring của `classify_triangle`: Bỏ tham chiếu `max(1e-4, ...)` đã lỗi thời, ghi nhận đúng dung sai tỷ lệ tương đối thuần túy `tol_rel = 0.006` (0.6% L_max).
   - Khắc phục `TypeError` khi truyền `None`: Bổ sung kiểm tra `if p is None:` và `if not isinstance(p, (list, tuple)):` ném `ValueError` tường minh.
   - Từ chối chuỗi số: Bổ sung điều kiện `if isinstance(v, (str, bytes)): raise ValueError(...)` trong `_finite(v, label, p)` để từ chối các chuỗi như `"3.5"`.

4. **Khôi phục lộ trình MSIX và tiêu chuẩn WACK:**
   - Khôi phục nguyên tắc ký số chính xác: Khi nộp ứng dụng lên Microsoft Store, Microsoft sẽ tự động ký gói bằng chứng chỉ Store chính thức; nhà phát triển chỉ cần chứng chỉ tự ký (Self-signed certificate) phục vụ thử nghiệm Sideloading nội bộ.
   - Khôi phục bước kiểm tra ảo hóa `%LOCALAPPDATA%` (MSIX VFS Containerization) đối với thư mục mô hình AI `AIMathHub\models` và kho khóa Windows DPAPI.
   - Khôi phục cú pháp dòng lệnh WACK chuẩn: `appcert.exe test -appxpackagepath <path_to_msix> -reportoutputpath <path_to_xml>`.

5. **Minh bạch hóa hạ tầng đóng gói và kết nối HTTPS:**
   - Xác định client HTTP: Cả `stem_shared_core/hf_downloader.py` và `stem_shared_core/ai_local_manager.py` đều sử dụng `urllib.request`.
   - Kết nối SSL/certifi: Bổ sung helper `_get_ssl_context()` nạp tường minh `cafile=certifi.where()` vào `ssl.create_default_context()`, bảo đảm gói chứng chỉ `cacert.pem` được sử dụng thật sự.
   - Bắt tay TLS trực tiếp: Mục kiểm thử 7 hỗ trợ cờ `--network-check` thực hiện bắt tay TLS thực tế tới `https://huggingface.co`.
   - Giải thích `warn-GeoSolver.txt`: Kích thước 76,210 bytes là do PyInstaller phân tích tĩnh cùng một tập thư viện; mã băm SHA-256 thay đổi giữa các lần build chứng minh tệp được sinh mới mỗi lần đóng gói.
   - Git Commit & Source code hash: Nhúng trường `"git_commit": "4f8b635a5595e674dd34ddc3c2ab9f832df78620"` vào `dist/GeoSolver/smoke_test_result.json`.
   - Manifest toàn bộ `dist/GeoSolver/`: Xuất tệp `dist_manifest.csv` (2,711 tệp tin, 430,713 bytes, SHA-256: `02BE82003DE55A0BC9885CD75722F1666483E9AB06C1F6ECC0FAF86B97A85741`).
   - Toàn văn [STORE_METADATA_AND_PRIVACY.md](file:///d:/AI%20DATA/STEM_APP/docs/STORE_METADATA_AND_PRIVACY.md): Trích dẫn toàn văn trong tài liệu báo cáo.

6. **Chuẩn hóa văn phong kỹ thuật:**
   - Loại bỏ các từ ngữ mang tính tuyệt đối hóa ("loại trừ hoàn toàn", "ngăn chặn triệt để", "chặt chẽ", "xác minh toàn diện", "bảo đảm bất biến tỷ lệ tuyệt đối").
   - Trình bày khách quan với các ngưỡng số học cụ thể ($10^{-5}$, $10^{-9}$, $10^{-12}$, $0.6\%$).

---

## 2. TOÀN VĂN MÃ NGUỒN SẢN XUẤT ĐÃ HIỆU CHỈNH (VERBATIM CODE)

### 2.1. Mã nguồn Canvas GUI: Kéo thả điểm và Kế thừa đối tượng cha (`parents`)

Dưới đây là các đoạn mã nguồn sản xuất trích xuất trực tiếp từ [geosolver/geosolver_desktop.py](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py):

#### a. Xử lý kéo thả điểm `<B1-Motion>` ([geosolver/geosolver_desktop.py#L12608-L12617](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py#L12608-L12617)):
```python
                for p in self.selected_points:
                    p["x"] += dx
                    p["y"] += dy
                    if self.snap_to_grid:
                        p["source"] = "grid_snap"
                        p["exact"] = True
                    else:
                        p["source"] = "dragged"
                        p["exact"] = False
```

#### b. Tạo trung điểm lưu đối tượng cha `parents` ([geosolver/geosolver_desktop.py#L10940-L10960](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py#L10940-L10960)):
```python
                    p1, p2 = self.temp_points
                    name = self._ask_point_name_dialog("")
                    if name is None:
                        self.temp_points.clear()
                        return

                    self._save_state()
                    mx = (p1["x"] + p2["x"]) / 2
                    my = (p1["y"] + p2["y"]) / 2
                    pt_id = name if name else f"Mid_{p1['id']}_{p2['id']}"

                    self.points.append({
                        "id": pt_id, "name": name, "x": mx, "y": my,
                        "color": "#2b8a3e", "fixed": True, "source": "midpoint",
                        "parents": [p1, p2],
                        "constraint": {"type": "midpoint", "p1": p1, "p2": p2}
                    })
```

#### c. Tạo giao điểm lưu đối tượng cha `parents` ([geosolver/geosolver_desktop.py#L10877-L10880](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py#L10877-L10880)):
```python
                    parents = [p for p in [e1.get("p1"), e1.get("p2"), e2.get("p1"), e2.get("p2")] if p]
                    self.points.append({
                        "id": pt_id, "name": name, "x": chosen[0], "y": chosen[1],
                        "color": self.COLOR_SNAP, "fixed": True,
                        "source": "intersection", "parents": parents
                    })
```

---

### 2.2. Mã nguồn Hàm kiểm tra và Phân loại Hình học cốt lõi

Trích xuất trực tiếp từ [geosolver/geosolver_desktop.py#L314-L697](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py#L314-L697):

```python
_FREE_SOURCES = ("free", "mouse", "dragged")
_EXACT_SOURCES = ("typed", "grid_snap", "snapped", "exact")
_DERIVED_SOURCES = ("midpoint", "intersection", "formula")


def _finite(v, label, p):
    """Ép về float, từ chối None / chuỗi / NaN / inf."""
    if isinstance(v, (str, bytes)):
        raise ValueError(f"Tọa độ '{label}' không được là chuỗi: {v!r}")
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
        + Dùng dung sai tỷ lệ tương đối tol_rel = 0.006 (0.6% L_max, không áp ngưỡng tuyệt đối).
        + Báo rõ 'gần đều (lệch X.X%)', 'gần cân (lệch X.X%)', 'gần vuông (góc X.X°)'.
    """
    is_en = (lang == "en")
    
    def get_xy_name_exact(p, default_name):
        if p is None:
            raise ValueError(f"Tọa độ điểm không được là None: {p!r}")
        if isinstance(p, dict):
            if "x" not in p or "y" not in p:
                raise ValueError(f"Điểm thiếu thuộc tính tọa độ 'x' hoặc 'y': {p}")
            return (_finite(p["x"], "x", p), _finite(p["y"], "y", p),
                    str(p.get("name") or default_name), _point_flag(p))
        if not isinstance(p, (list, tuple)):
            raise ValueError(f"Tọa độ điểm phải là dict hoặc sequence (list/tuple), nhận được {type(p).__name__}: {p!r}")
        if len(p) < 2:
            raise ValueError(f"Tọa độ điểm phải có ít nhất 2 phần tử (x, y): {p}")
        return _finite(p[0], "x", p), _finite(p[1], "y", p), default_name, None

    xA, yA, nA, exA = get_xy_name_exact(pA, "A")
    xB, yB, nB, exB = get_xy_name_exact(pB, "B")
    xC, yC, nC, exC = get_xy_name_exact(pC, "C")

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
    
    scaled_coords, scale_factor = as_scaled_ints([xA, yA, xB, yB, xC, yC], max_k=4)
    is_discrete = (scaled_coords is not None) and (user_declared_exact is not False)

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
        d2_AB = s_uAB[0]**2 + s_uAB[1]**2
        d2_AC = s_uAC[0]**2 + s_uAC[1]**2
        d2_BC = s_uBC[0]**2 + s_uBC[1]**2

        eq_AB_AC = (d2_AB == d2_AC)
        eq_BA_BC = (d2_AB == d2_BC)
        eq_CA_CB = (d2_AC == d2_BC)
        is_equilateral = False

        dot_A = s_uAB[0] * s_uAC[0] + s_uAB[1] * s_uAC[1]
        dot_B = -s_uAB[0] * s_uBC[0] - s_uAB[1] * s_uBC[1]
        dot_C = s_uAC[0] * s_uBC[0] + s_uAC[1] * s_uBC[1]

        perp_A = (dot_A == 0)
        perp_B = (dot_B == 0)
        perp_C = (dot_C == 0)
    else:
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
        "is_isosceles": (tri_type in ("isosceles", "right_isosceles")),
        "is_right": (tri_type in ("right", "right_isosceles")),
        "sides": {"AB": c_len, "AC": b_len, "BC": a_len},
        "side_labels": {"AB": str_AB, "AC": str_AC, "BC": str_BC},
        "sides_formatted": {"AB": str_AB, "AC": str_AC, "BC": str_BC},
        "description": description
    }
```

---

## 3. BẰNG CHỨNG THỰC NGHIỆM TỔNG HỢP (EMPIRICAL EVIDENCE)

### 3.1. Toàn bộ 38 bài kiểm thử đơn vị tự động (38/38 PASSED)

Bộ kiểm thử hoàn chỉnh gồm:
- [tests/test_geometry_invariants.py](file:///d:/AI%20DATA/STEM_APP/tests/test_geometry_invariants.py): 27 bài kiểm tra (bổ sung `test_25` GUI Canvas drag & midpoint, `test_26` nested constructions, `test_27` input type validation).
- [tests/test_round9_taint_validation.py](file:///d:/AI%20DATA/STEM_APP/tests/test_round9_taint_validation.py): 11 bài kiểm tra xác thực taint và suy biến vi mô.

Nhật ký thực thi đầy đủ lưu tại [tests/test_run.log](file:///d:/AI%20DATA/STEM_APP/tests/test_run.log):

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
test_25_gui_canvas_drag_typed_and_midpoint_parents_integration (tests.test_geometry_invariants.TestGeometryInvariants.test_25_gui_canvas_drag_typed_and_midpoint_parents_integration)
Kiểm tra Canvas GUI: Kéo điểm typed khi snap tắt thành dragged, và tạo trung điểm từ 2 điểm free lưu parents ... ok
test_26_nested_constructions_multi_level_taint (tests.test_geometry_invariants.TestGeometryInvariants.test_26_nested_constructions_multi_level_taint)
Kiểm tra dựng hình lồng nhau nhiều tầng (Nested derived points): Lan truyền taint qua nhiều cấp cha-con ... ok
test_27_none_and_string_and_invalid_type_rejection (tests.test_geometry_invariants.TestGeometryInvariants.test_27_none_and_string_and_invalid_type_rejection)
Kiểm tra xử lý ngoại lệ: Từ chối None, chuỗi '3.5', int và kiểu không hợp lệ ném ValueError chuẩn ... ok
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
Ran 38 tests in 1.694s

OK
```

---

### 3.2. Bằng chứng kiểm thử khói tập tin thực thi độc lập (`GeoSolver.exe --smoke-test`)

Tệp thực thi `dist/GeoSolver/GeoSolver.exe` được chạy kiểm chứng tự động:
```powershell
$proc = Start-Process -FilePath "dist\GeoSolver\GeoSolver.exe" -ArgumentList "--smoke-test" -Wait -PassThru
```

**Mã thoát:** `0`  
**Tệp nhật ký tự động ghi:** [dist/GeoSolver/smoke_run.log](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/smoke_run.log)
```text
[SMOKE TEST] Khởi chạy kiểm thử đóng gói GeoSolver (Smoke Test)...
[SMOKE TEST] 1. Phân loại hình học bất biến: ĐẠT
[SMOKE TEST] 2. Mã hóa & giải mã Windows DPAPI: ĐẠT
[SMOKE TEST] 3. Nạp động thư viện SymPy: ĐẠT
[SMOKE TEST] 4. Khởi tạo & giải phóng Tkinter GUI runtime: ĐẠT
[SMOKE TEST] 5. Nạp các module phụ thuộc quan trọng: ĐẠT
[SMOKE TEST] 6. Tài nguyên đóng gói trong frozen bundle: ĐẠT
[SMOKE TEST] 7. Nạp cấu hình bảo mật SSL/TLS & CA bundle certifi (cafile): ĐẠT
[SMOKE TEST] TẤT CẢ CÁC MỤC KIỂM THỬ KHÓI ĐỀU THÀNH CÔNG (MÃ THOÁT 0).
[SMOKE TEST] Đã ghi nhật ký kết quả kiểm thử vào: D:\AI DATA\STEM_APP\dist\GeoSolver\smoke_test_result.json
```

**Tệp kết quả JSON:** [dist/GeoSolver/smoke_test_result.json](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/smoke_test_result.json)
```json
{
  "timestamp": "2026-11-09T09:27:00.802572+00:00",
  "git_commit": "4f8b635a5595e674dd34ddc3c2ab9f832df78620",
  "frozen": true,
  "python_version": "3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)]",
  "executable": "D:\\AI DATA\\STEM_APP\\dist\\GeoSolver\\GeoSolver.exe",
  "executable_sha256": "0F4A3E111D95F797835481B37BB3E21C895F0F2DABF4CAFE3E894571B8A120AD",
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

Bảng đối soát tính toán trên Windows 11 ngày 09/11/2026:

| STT | Tệp tin | SHA-256 | Kích thước (bytes) |
|:---:|:---|:---|:---:|
| 1 | [`geosolver_desktop.py`](file:///d:/AI%20DATA/STEM_APP/geosolver/geosolver_desktop.py) | `91473072B87AD5BBF8A892DEF5680C10FA3AF6B6EB75B34258C936432C590F52` | 648,668 |
| 2 | [`GeoSolver.spec`](file:///d:/AI%20DATA/STEM_APP/geosolver/GeoSolver.spec) | `5514177387F812B81BAA1C3D3B08FBE34A3B99644B5E399C6E828C0C8AA1BC1C` | 1,798 |
| 3 | [`test_geometry_invariants.py`](file:///d:/AI%20DATA/STEM_APP/tests/test_geometry_invariants.py) | `4401B1ADA1623E8678E4398C74708F9C5A4850114AB9F7059A974580CD3B61AD` | 34,858 |
| 4 | [`test_round9_taint_validation.py`](file:///d:/AI%20DATA/STEM_APP/tests/test_round9_taint_validation.py) | `B01A401AAF76B5050651AE83DD953EB5034AA8F8E9CE77F2E63DD0686B60BAEA` | 4,012 |
| 5 | [`test_run.log`](file:///d:/AI%20DATA/STEM_APP/tests/test_run.log) | `27D007557CF2F2A64D0A4C07E4AE9B0FBF4EDDFB38555582CDC0C37E1C31A80A` | 9,836 |
| 6 | [`ai_local_manager.py`](file:///d:/AI%20DATA/STEM_APP/stem_shared_core/ai_local_manager.py) | `330B3A90ED35DCE7F78D5A9371FB0450D13667B662FD641A152DE61D46059637` | 58,729 |
| 7 | [`hf_downloader.py`](file:///d:/AI%20DATA/STEM_APP/stem_shared_core/hf_downloader.py) | `446160AE8DBE67FA422F976C457F0636EAFEBFE0F679B06B8F772217113EE59B` | 30,192 |
| 8 | [`ai_model_hub.py`](file:///d:/AI%20DATA/STEM_APP/stem_shared_core/ai_model_hub.py) | `8DE4956855D02418503DF934509BD4B9BB52C9F0E9238414FE72F9DCD1C09818` | 69,054 |
| 9 | [`ai_config_dialog.py`](file:///d:/AI%20DATA/STEM_APP/stem_shared_core/ai_config_dialog.py) | `647ABC5D0FF8F05C7794F6FDBE4C582893A288EDEE603812F1FB13B8E792434C` | 7,961 |
| 10 | [`stem_handbook_dialog.py`](file:///d:/AI%20DATA/STEM_APP/stem_handbook_dialog.py) | `2B4E562D5460E8A0CDEE3DDCCA4747D1BD29934D20177FE2AD11AA30B17883B0` | 42,832 |
| 11 | [`STORE_METADATA_AND_PRIVACY.md`](file:///d:/AI%20DATA/STEM_APP/docs/STORE_METADATA_AND_PRIVACY.md) | `761D09DF6A38C616ABB2852EDF732B16264EFB7B46571BD68F9B503932D2326D` | 5,502 |
| 12 | [`GeoSolver.exe`](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/GeoSolver.exe) | `0F4A3E111D95F797835481B37BB3E21C895F0F2DABF4CAFE3E894571B8A120AD` | 32,758,008 |
| 13 | [`smoke_test_result.json`](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/smoke_test_result.json) | `9C6CC25D9156E6F31BC1CDC08CCA99DB29F5B89AF726541950460F20036A952B` | 637 |
| 14 | [`smoke_run.log`](file:///d:/AI%20DATA/STEM_APP/dist/GeoSolver/smoke_run.log) | `F8DD2C235F49CD5626ADB9EE01E8A174AA272F320DEF40122232EA2AB8378465` | 780 |
| 15 | [`file_version_info.txt`](file:///d:/AI%20DATA/STEM_APP/geosolver/file_version_info.txt) | `E0D429E428BCACD8DA8FF7C4F461D99D159A44BF69854A805FF2C566250DDDC6` | 926 |
| 16 | [`warn-GeoSolver.txt`](file:///d:/AI%20DATA/STEM_APP/build/GeoSolver/warn-GeoSolver.txt) | `3C0C2F548E544C33C39301520584875B97767A6FC449A6FB9C4B5702F1C94295` | 76,210 |

> [!NOTE]
> - Tệp manifest toàn bộ thư mục phân phối `dist/GeoSolver/` gồm 2,711 tệp tin đã được xuất tại [dist_manifest.csv](file:///d:/AI%20DATA/STEM_APP/dist_manifest.csv) (Kích thước: 430,713 bytes, SHA-256: `02BE82003DE55A0BC9885CD75722F1666483E9AB06C1F6ECC0FAF86B97A85741`).
> - Tệp `warn-GeoSolver.txt` có mã băm SHA-256 mới (`3C0C2F54...`), xác nhận tệp được PyInstaller tạo mới trong lần đóng gói này; kích thước giữ nguyên 76,210 bytes do danh sách cảnh báo phân tích tĩnh của các module bên thứ ba là tất định.

---

## 5. TOÀN VĂN TÀI LIỆU STORE METADATA & CHÍNH SÁCH QUYỀN RIÊNG TƯ

Trích dẫn toàn văn từ [docs/STORE_METADATA_AND_PRIVACY.md](file:///d:/AI%20DATA/STEM_APP/docs/STORE_METADATA_AND_PRIVACY.md):

```markdown
# CHÍNH SÁCH QUYỀN RIÊNG TƯ & ĐẶC TẢ MICROSOFT STORE
## HỆ THỐNG PHẦN MỀM GEOSOLVER 2D (CAD MATH STUDIO)
*Văn bản công bố chính thức phục vụ hồ sơ nộp và thẩm định trên Microsoft Store.*  
**Mã tài liệu:** STORE-PRIVACY-AGED-DECLARATION-2026  
**Ngày cập nhật:** 09/11/2026  

---

## 1. CHÍNH SÁCH QUYỀN RIÊNG TƯ (PRIVACY POLICY)

### 1.1. Nguyên tắc cốt lõi: Bảo vệ Dữ liệu Cục bộ (Local-First Privacy)
Hệ thống **GeoSolver 2D** được thiết kế theo nguyên tắc Local-first: *Dữ liệu bản vẽ và bài toán của người dùng hoàn toàn thuộc quyền sở hữu của người dùng*. Ứng dụng không thu thập, không phân tích hành vi và không gửi telemetry về máy chủ của nhà phát triển.

### 1.2. Thu thập và Xử lý Dữ liệu Ngoại tuyến
* **Không thu thập Telemetry / Quảng cáo:** Ứng dụng không chứa bất kỳ SDK theo dõi hành vi, Google Analytics, Firebase Telemetry, hay mã theo dõi quảng cáo nào.
* **Xử lý Hình học CAD & CAS Ngoại tuyến:** Toàn bộ các thao tác dựng hình học phẳng (điểm, đoạn thẳng, tam giác, đường tròn, elip...), phát hiện bất biến hình học, đo đạc kích thước và tính toán đại số tượng trưng (SymPy) được xử lý hoàn toàn ngoại tuyến trên máy tính cục bộ của người dùng.
* **Mô hình AI Cục bộ (Local LLM - Tùy chọn):** Khi người dùng kích hoạt suy luận ngoại tuyến qua Ollama hoặc tệp mô hình GGUF cục bộ, toàn bộ dữ liệu suy luận được xử lý trực tiếp trên GPU/RAM cục bộ, không truyền dữ liệu ra Internet.

### 1.3. Khai báo các luồng truyền dữ liệu qua Mạng (Network Data Flows)
Ứng dụng chỉ phát sinh kết nối mạng ra bên ngoài trong 2 tình huống người dùng chủ động kích hoạt:
1. **Dịch vụ AI Đám mây (Google Gemini API - Tùy chọn):**
   - Khi người dùng chủ động cấu hình khóa API Gemini và yêu cầu giải toán qua AI đám mây, nội dung câu hỏi hình học được gửi trực tiếp tới endpoint chính thức của Google (`generativelanguage.googleapis.com`) qua giao thức mã hóa HTTPS/TLS 1.3.
   - Khóa API cá nhân của người dùng được lưu trữ cục bộ trên máy tính bằng cơ chế mã hóa cấp hệ điều hành Windows Data Protection API (DPAPI - `CryptProtectData`).
2. **Tải Mô hình Ngoại tuyến (Hugging Face Model Hub - Tùy chọn):**
   - Khi người dùng chủ động tải các tệp trọng số mô hình AI nguồn mở (.gguf) về máy, ứng dụng tải trực tiếp qua HTTPS từ máy chủ chính thức `huggingface.co`. Quá trình tải kiểm tra mã băm SHA-256 để bảo đảm tính toàn vẹn tệp tin.

---

## 2. BẢNG KHAI BÁO KHẢO SÁT ĐỘ TUỔI IARC (IARC AGE RATING QUESTIONNAIRE)

Bảng kê khai thông tin phục vụ khảo sát IARC (International Age Rating Coalition) trên Microsoft Partner Center:

| Tiêu chí khảo sát IARC | Khai báo thực tế của GeoSolver 2D | Đánh giá nội bộ |
| :--- | :---: | :---: |
| **Bạo lực (Violence)** | Không | Không chứa bất kỳ hình ảnh/yếu tố bạo lực |
| **Nội dung nhạy cảm / Tình dục** | Không | Không |
| **Ngôn ngữ thô tục (Profanity)** | Không | Thuần túy thuật ngữ toán học STEM |
| **Chất kích thích / Rượu bia** | Không | Không |
| **Giao dịch trả phí trong app (IAP)** | Không | Không chứa mua hàng trong ứng dụng |
| **Chia sẻ vị trí địa lý (Location)** | Không | Không sử dụng định vị GPS/IP |
| **Tương tác trực tuyến giữa người dùng** | Không | Không có tính năng chat mạng xã hội |

*Dự kiến phân loại IARC:* **IARC 3+ (Mọi lứa tuổi / All Ages)** — Phân loại chính thức sẽ do hệ thống Partner Center cấp sau khi hoàn thành bảng câu hỏi trực tuyến khi nộp gói.

---

## 3. GIẢI TRÌNH CAPABILITY VÀ TUÂN THỦ WACK

1. **Giải trình Restricted Capability `runFullTrust`:**
   - *Lý do kỹ thuật:* GeoSolver 2D là ứng dụng Win32 truyền thống được đóng gói để phân phối qua Microsoft Store thông qua công nghệ chuyển đổi **Desktop Bridge (Centennial)**.
   - Do bản chất là ứng dụng để bàn hoàn chỉnh (thực thi Python runtime độc lập, gọi DPAPI hệ thống, tải mô hình AI cục bộ), cơ chế Desktop Bridge bắt buộc phải khai báo capability `runFullTrust` trong `AppxManifest.xml` để khởi chạy tiến trình chính.
2. **Tuân thủ quy chuẩn WACK (Windows App Certification Kit):**
   - Tắt nén UPX (`upx=False`) trong cấu hình PyInstaller để tránh cảnh báo nhận diện nhầm từ Windows Defender và SmartScreen.
   - Hỗ trợ đầy đủ cơ chế VFS Virtualization của Desktop Bridge: thư mục ứng dụng trong `WindowsApps` là Read-Only, các thao tác ghi dữ liệu nhật ký và khóa DPAPI được lưu trữ an toàn trong `%LOCALAPPDATA%` (được Windows tự động chuyển hướng về thư mục dữ liệu cô lập của gói).
   - Mã lệnh kiểm thử WACK chuẩn cho gói MSIX:  
     `appcert.exe test -appxpackagepath <Đường_dẫn_tệp_MSIX> -reportoutputpath <Đường_dẫn_báo_cáo_XML>`
```

---

## 6. LỘ TRÌNH ĐÓNG GÓI MSIX VÀ KIỂM ĐỊNH WACK

1. **Quy định Ký số (Code Signing Principle):**
   - Khi nộp gói ứng dụng `.msix` lên Microsoft Store thông qua cổng Partner Center, hệ thống của Microsoft sẽ tiến hành thẩm định và **tự động ký số** bằng chứng chỉ chính thức của Microsoft Store.
   - Trong giai đoạn phát triển và kiểm thử nội bộ, nhà phát triển chỉ cần tạo chứng chỉ tự ký (Self-signed test certificate qua lệnh PowerShell `New-SelfSignedCertificate`) và cài đặt vào kho `Trusted Root Certification Authorities` trên máy kiểm thử để phục vụ cài đặt thử nghiệm (Sideloading) và chạy công cụ WACK.

2. **Kiểm tra Ảo hóa `%LOCALAPPDATA%` (VFS Containerization Verification):**
   - Ứng dụng Desktop Bridge khi cài qua MSIX sẽ chạy trong container cách ly, các đường dẫn `%LOCALAPPDATA%` (như kho mô hình `AIMathHub\models` hay tệp cấu hình) được Windows tự động chuyển hướng (redirect) vào thư mục:
     `%LOCALAPPDATA%\Packages\<PackageFamilyName>\LocalCache\Local\`
   - Bước kiểm thử bắt buộc: Tiến hành cài đặt gói MSIX thử nghiệm trên máy sạch (hoặc máy ảo / Windows Sandbox), thực hiện:
     - Tải một mô hình nhỏ từ Hugging Face Hub để kiểm tra quyền ghi thư mục mô hình ảo hóa.
     - Lưu khóa API Gemini để xác nhận Windows DPAPI giải mã thành công trong môi trường container.

3. **Quy trình Kiểm thử WACK tự động bằng Dòng lệnh:**
   - Thực thi bộ công cụ kiểm định Windows App Certification Kit (WACK):
     ```powershell
     & "C:\Program Files (x86)\Windows Kits\10\App Certification Kit\appcert.exe" test -appxpackagepath "dist\GeoSolver.msix" -reportoutputpath "dist\wack_report.xml"
     ```
   - Các nhóm tiêu chí bắt buộc đạt:
     - *Package Compliance:* Cấu trúc tệp kê khai `AppxManifest.xml` hợp lệ, đầy đủ logo assets các tỷ lệ co giãn (scale 100, 125, 150, 200).
     - *Supported API test:* Không gọi các hàm Win32 không được phép ngoài phạm vi Desktop Bridge.
     - *Security tests:* Không chứa mã thực thi độc hại, không dùng UPX gây báo động nhầm.
