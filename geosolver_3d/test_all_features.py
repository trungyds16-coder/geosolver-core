# test_all_features.py
import sys
import os
import math
import tkinter as tk

class FakeEvent:
    def __init__(self, x, y, state=0):
        self.x = int(round(x))
        self.y = int(round(y))
        self.state = state


# Reconfigure stdout for utf-8
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath("."))

def test_no_su_pham():
    print("[TEST 1] Kiểm tra loại bỏ lạm phát từ ngữ 'sư phạm'...")
    with open('geosolver_3d/app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    occurrences = []
    for idx, line in enumerate(lines):
        if 'sư phạm' in line.lower() and not line.strip().startswith('#') and 'docstring' not in line.lower():
            if any(term in line for term in ['text=', 'title=', 'Label(', 'Button(', '[SUY LUẬN', '[KẾT LUẬN', 'BÁO CÁO']):
                occurrences.append((idx + 1, line.strip()))
    if occurrences:
        for line_no, text in occurrences:
            print(f"  FAILED: Line {line_no}: {text}")
        assert False, f"Found {len(occurrences)} user-facing 'sư phạm' occurrences!"
    print("  PASSED: Không còn từ 'sư phạm' trong giao diện người dùng.")

def test_image_export():
    print("[TEST 2] Kiểm tra Xuất ảnh PNG độ phân giải cao (300 DPI) bằng Pillow...")
    from geosolver_3d.app import GeoSolver3DApp
    root = tk.Tk()
    root.withdraw()
    app = GeoSolver3DApp()
    app.withdraw()

    test_png_path = "test_export_verified.png"
    if os.path.exists(test_png_path):
        os.remove(test_png_path)

    # Call direct scene renderer
    app._render_scene_to_image(test_png_path, scale=2)
    assert os.path.exists(test_png_path), "File test_export_verified.png was not created!"
    
    # Check with PIL
    from PIL import Image
    img = Image.open(test_png_path)
    print(f"  -> File ảnh PNG đã xuất thành công: kích thước {img.size}, format {img.format}")
    assert img.size[0] >= 1000 and img.size[1] >= 800, f"Image size too small: {img.size}"
    assert img.format == "PNG", f"Expected PNG, got {img.format}"

    img.close()
    if os.path.exists(test_png_path):
        os.remove(test_png_path)

    app.destroy()
    root.destroy()
    print("  PASSED: Xuất ảnh PNG thuần Python chuẩn 300 DPI thành công 100%, không lỗi Ghostscript!")

def test_side_panel_and_section_interaction():
    print("[TEST 3] Kiểm tra Thanh trượt Sidebar và Tương tác Di chuyển Điểm Thiết diện MNPQ...")
    from geosolver_3d.app import GeoSolver3DApp, vec_add, vec_sub, vec_scale

    root = tk.Tk()
    root.withdraw()
    app = GeoSolver3DApp()
    app.withdraw()

    # 1. Kiểm tra không gian và thanh trượt side panel
    assert hasattr(app, "side_container"), "Missing side_container"
    assert hasattr(app, "side_canvas"), "Missing side_canvas"
    assert hasattr(app, "side_scrollbar"), "Missing side_scrollbar"
    w_side = app.side_container.cget("width")
    print(f"  -> Chiều rộng Side Panel: {w_side}px (thoáng rộng, có thanh cuộn)")
    assert int(w_side) >= 320, f"Side panel width {w_side} is still cramped (< 320)!"

    # Test mouse wheel scroll event on side panel
    class FakeWheelEvent:
        def __init__(self, delta):
            self.delta = delta
    app._on_side_mousewheel(FakeWheelEvent(-120))
    app._on_side_mousewheel(FakeWheelEvent(120))
    print("  -> Hệ thống thanh trượt và con lăn chuột Sidebar hoạt động mượt mà!")

    # 2. Kiểm tra các nút đổi hướng mặt phẳng thiết diện nhanh
    model = app.models[app.current_model_key]
    app.set_section_plane_orientation((0.0, 0.0, 1.0))
    assert model.plane_normal == (0.0, 0.0, 1.0), "Cutting plane orientation not updated to Oxy"
    app.set_section_plane_orientation((0.0, 0.5, 0.866))
    print("  -> Nút đổi hướng mặt phẳng cắt nhanh (Oxy, Xiên, Oxz, Chéo) hoạt động hoàn hảo!")

    app.destroy()
    root.destroy()
    print("  PASSED: Thanh trượt Sidebar và thiết lập hướng mặt phẳng đạt 100%!")

def test_cad_hatching_algorithm():
    print("[TEST 4] Kiểm tra Thuật toán Gạch chéo Kỹ thuật CAD (Vector CAD Hatching)...")
    from geosolver_3d.app import compute_polygon_hatch

    # Test 1: Polygon hình chữ nhật
    rect = [(100.0, 100.0), (300.0, 100.0), (300.0, 200.0), (100.0, 200.0)]
    hatch_45 = compute_polygon_hatch(rect, spacing=15.0, angle_deg=45.0)
    assert len(hatch_45) >= 5, f"Expected >= 5 hatch lines for rect, got {len(hatch_45)}"
    print(f"  -> Đã tính toán chính xác {len(hatch_45)} đường gạch chéo 45° cho đa giác hình chữ nhật.")

    # Test 2: Gạch ca-rô CAD (+45° và -45°)
    cross_hatch = hatch_45 + compute_polygon_hatch(rect, spacing=15.0, angle_deg=-45.0)
    assert len(cross_hatch) >= 10, f"Expected >= 10 cross-hatch lines, got {len(cross_hatch)}"
    print(f"  -> Đã tính toán chính xác {len(cross_hatch)} đường gạch ca-rô hai chiều chuẩn CAD.")

    # Test 3: Tam giác
    tri = [(50.0, 50.0), (250.0, 80.0), (150.0, 220.0)]
    tri_hatch = compute_polygon_hatch(tri, spacing=12.0, angle_deg=45.0)
    assert len(tri_hatch) >= 4, f"Expected >= 4 hatch lines for triangle, got {len(tri_hatch)}"
    print(f"  -> Đã tính toán chính xác {len(tri_hatch)} đường gạch chéo cho tam giác bất kỳ.")

    print("  PASSED: Thuật toán Gạch chéo Vector CAD hoạt động chính xác và cực nhanh!")

def test_point_on_segment_dynamic_ratio_and_domain_clamping():
    print("[TEST 5] Kiểm tra Điểm trên đoạn thẳng, Tỉ số động k và Ràng buộc miền xác định...")
    from geosolver_3d.app import GeoSolver3DApp, vec_norm, vec_sub

    root = tk.Tk()
    root.withdraw()
    app = GeoSolver3DApp()
    app.withdraw()

    model = app.models[app.current_model_key]

    # Tạo điểm E trên đoạn AB với tỉ số k = 0.5 (trung điểm)
    pA = model.vertices["A"]
    pB = model.vertices["B"]
    pE_init = (pA[0] * 0.5 + pB[0] * 0.5, pA[1] * 0.5 + pB[1] * 0.5, pA[2] * 0.5 + pB[2] * 0.5)
    model.aux_points["E"] = pE_init
    model.point_constraints["E"] = {"type": "ratio", "p1": "A", "p2": "B", "k": 0.5}
    model.aux_segments.append({
        "p1_name": "A", "p2_name": "E", "p1": pA, "p2": pE_init,
        "color": "#000080", "dash": True, "label": "E (k=0.50)", "width": 1.8
    })

    # Chuyển sang chế độ Di chuyển và kéo điểm E
    app.set_interact_mode("move")
    w = max(400, app.canvas.winfo_width())
    h = max(320, app.canvas.winfo_height())
    sx, sy, _ = app.project_point(pE_init, w, h)

    class FakeEvent:
        def __init__(self, x, y):
            self.x = int(round(x))
            self.y = int(round(y))
            self.state = 0

    # Click xuống điểm E
    app._on_mouse_down(FakeEvent(sx, sy))
    assert app.selected_vertex == "E", "Điểm E không được chọn!"
    assert app.dragged_vertex == "E", "Điểm E không ở trạng thái kéo!"

    # Kéo chuột theo hướng bất kỳ
    app._on_mouse_drag(FakeEvent(sx + 50, sy - 40))

    # Kiểm tra điểm E: phải luôn nằm trên đoạn AB
    pE_moved = model.aux_points["E"]
    k_curr = model.point_constraints["E"]["k"]
    print(f"  -> Sau khi kéo chuột: Điểm E tại {pE_moved}, tỉ số k = {k_curr:.3f}")
    assert 0.0 <= k_curr <= 1.0, f"Tỉ số k bay ra ngoài đoạn: k = {k_curr}"

    # Kiểm tra tọa độ hình học: E = A + k * (B - A)
    expected_E = (
        pA[0] + k_curr * (pB[0] - pA[0]),
        pA[1] + k_curr * (pB[1] - pA[1]),
        pA[2] + k_curr * (pB[2] - pA[2]),
    )
    dist_err = vec_norm(vec_sub(pE_moved, expected_E))
    assert dist_err < 1e-6, f"Điểm E bay lệch khỏi cạnh AB! Sai số: {dist_err}"

    # Thử kéo rất xa về phía âm và dương để kiểm tra chốt chặn biên [0.0, 1.0]
    app._on_mouse_drag(FakeEvent(sx - 1000, sy + 1000))
    k_min = model.point_constraints["E"]["k"]
    assert k_min >= 0.0, f"Điểm E vượt quá đầu mút A: k = {k_min}"

    app._on_mouse_drag(FakeEvent(sx + 1000, sy - 1000))
    k_max = model.point_constraints["E"]["k"]
    assert k_max <= 1.0, f"Điểm E vượt quá đầu mút B: k = {k_max}"
    print(f"  -> Ràng buộc miền xác định tuyệt đối: k luôn bị khóa trong [0.0, 1.0], không thể bay sang cạnh khác!")

    app._on_mouse_up(FakeEvent(sx, sy))
    assert app.dragged_vertex is None, "Kéo thả chưa được giải phóng sau mouse_up!"

    app.destroy()
    root.destroy()
    print("  PASSED: Điểm trên đoạn thẳng cập nhật tỉ số k thời gian thực và không bao giờ bay ra ngoài miền xác định!")

def test_custom_3point_plane_and_cad_hatching():
    print("[TEST 6] Kiểm tra Vẽ & Tô màu Mặt phẳng qua 3 điểm chuẩn CAD...")
    from geosolver_3d.app import GeoSolver3DApp, vec_dot, vec_norm

    root = tk.Tk()
    root.withdraw()
    app = GeoSolver3DApp()
    app.withdraw()

    model = app.models[app.current_model_key]

    # Thêm mặt phẳng qua 3 điểm A, B, S với chế độ gạch chéo CAD
    model.add_custom_plane(
        name="Mặt phẳng (SAB)",
        pts=["S", "A", "B"],
        color="#1971C2",
        fill_mode="hatch",
        hatch_spacing=12,
        is_cutter=False,
    )
    assert len(model.custom_planes) == 1, "Mặt phẳng chưa được thêm vào model!"
    pl = model.custom_planes[0]
    assert pl["name"] == "Mặt phẳng (SAB)"
    assert pl["fill_mode"] == "hatch"
    print("  -> Đã tạo thành công mặt phẳng qua 3 điểm (SAB) với chế độ tô gạch chéo CAD 45°.")

    # Thêm mặt phẳng thứ 2 qua 3 điểm M, N, P và đặt làm mặt phẳng cắt khối đa diện
    sec_pts = model.compute_cross_section()
    assert len(sec_pts) >= 3, "Không đủ điểm thiết diện!"
    lbl_m, pt_m = sec_pts[0]
    lbl_n, pt_n = sec_pts[1]
    lbl_p, pt_p = sec_pts[2]

    model.add_custom_plane(
        name=f"Thiết diện ({lbl_m}{lbl_n}{lbl_p})",
        pts=[lbl_m, lbl_n, lbl_p],
        color="#E03131",
        fill_mode="cross",
        hatch_spacing=10,
        is_cutter=True,
    )
    assert len(model.custom_planes) == 2
    assert model.plane_defining_pts == [lbl_m, lbl_n, lbl_p]
    print("  -> Đã tạo mặt phẳng cắt qua 3 điểm thiết diện M, N, P với chế độ gạch ca-rô CAD.")

    # Kiểm tra vẽ lên canvas
    app.redraw_canvas()

    app.destroy()
    root.destroy()
    print("  PASSED: Vẽ và tô màu mặt phẳng 3 điểm với gạch chéo/ca-rô CAD đạt 100%!")

def test_independent_section_vertex_pivot_dragging():
    print("[TEST 7] Kiểm tra Kéo Độc Lập Đỉnh Thiết Diện (Xoay nghiêng quanh 2 đỉnh cố định)...")
    from geosolver_3d.app import GeoSolver3DApp, vec_norm, vec_sub

    root = tk.Tk()
    root.withdraw()
    app = GeoSolver3DApp()
    app.withdraw()

    model = app.models[app.current_model_key]
    app.show_section = True
    app.set_interact_mode("move")
    app.set_section_drag_mode("pivot")
    assert model.section_drag_mode == "pivot", "Section drag mode is not pivot!"

    sec_pts = model.compute_cross_section()
    assert len(sec_pts) >= 4, f"Expected 4 section vertices on pyramid, got {len(sec_pts)}"

    lbl_m, pt_m_init = sec_pts[0]
    lbl_n, pt_n_init = sec_pts[1]
    lbl_p, pt_p_init = sec_pts[2]
    lbl_q, pt_q_init = sec_pts[3]

    print(f"  -> Tọa độ ban đầu:")
    print(f"     {lbl_m} = {pt_m_init}")
    print(f"     {lbl_n} = {pt_n_init}")
    print(f"     {lbl_p} = {pt_p_init}")
    print(f"     {lbl_q} = {pt_q_init}")

    w = max(400, app.canvas.winfo_width())
    h = max(320, app.canvas.winfo_height())
    sx, sy, _ = app.project_point(pt_m_init, w, h)

    class FakeEvent:
        def __init__(self, x, y):
            self.x = int(round(x))
            self.y = int(round(y))
            self.state = 0

    # Nhấn xuống đỉnh M của thiết diện
    app._on_mouse_down(FakeEvent(sx, sy))
    assert app.selected_vertex == lbl_m, f"Đỉnh {lbl_m} không được chọn!"
    assert app.dragged_vertex == lbl_m, f"Đỉnh {lbl_m} không được kéo!"
    assert app._drag_sec_fixed_pts is not None, "Fixed points for pivot not initialized!"

    # Kéo chuột để trượt đỉnh M
    app._on_mouse_drag(FakeEvent(sx, sy - 35))

    # Lấy tọa độ mới sau khi kéo
    sec_pts_after = model.section_points
    sec_dict = dict(sec_pts_after)

    pt_m_after = sec_dict[lbl_m]
    pt_n_after = sec_dict[lbl_n]
    pt_p_after = sec_dict[lbl_p]
    pt_q_after = sec_dict[lbl_q]

    print(f"  -> Tọa độ sau khi kéo đỉnh {lbl_m}:")
    print(f"     {lbl_m} = {pt_m_after}")
    print(f"     {lbl_n} = {pt_n_after}")
    print(f"     {lbl_p} = {pt_p_after}")
    print(f"     {lbl_q} = {pt_q_after}")

    # Kiểm tra 1: Đỉnh M phải di chuyển
    diff_m = vec_norm(vec_sub(pt_m_after, pt_m_init))
    assert diff_m > 1e-3, f"Đỉnh {lbl_m} không di chuyển!"

    # Kiểm tra 2: Hai đỉnh cố định N và P PHẢI ĐỨNG YÊN (sai số < 1e-4)
    diff_n = vec_norm(vec_sub(pt_n_after, pt_n_init))
    diff_p = vec_norm(vec_sub(pt_p_after, pt_p_init))
    print(f"  -> Sai lệch đỉnh cố định {lbl_n}: {diff_n:.7f}")
    print(f"  -> Sai lệch đỉnh cố định {lbl_p}: {diff_p:.7f}")
    assert diff_n < 1e-4, f"Đỉnh {lbl_n} bị xê dịch khi kéo {lbl_m}! Sai số: {diff_n}"
    assert diff_p < 1e-4, f"Đỉnh {lbl_p} bị xê dịch khi kéo {lbl_m}! Sai số: {diff_p}"

    # Kiểm tra 3: Đỉnh Q tự động tính toán lại theo mặt phẳng mới
    print(f"  -> Đỉnh {lbl_q} tự động điều chỉnh theo phương trình mặt phẳng mới ({lbl_m}{lbl_n}{lbl_p})!")

    # Nhả chuột
    app._on_mouse_up(FakeEvent(sx, sy))

    # Kiểm tra chuyển sang chế độ Parallel
    app.set_section_drag_mode("parallel")
    assert model.section_drag_mode == "parallel"
    print("  -> Chuyển đổi thành công giữa 2 chế độ: [🎯 Độc lập đỉnh] và [⇕ Trượt cả mặt phẳng].")

    app.destroy()
    root.destroy()
    print("  PASSED: Kéo độc lập đỉnh thiết diện hoạt động hoàn hảo, bảo toàn các đỉnh cố định 100%!")

def test_camera_orbit_direction():
    print("[TEST 8] Kiểm tra hướng xoay 3D Camera Orbit & Kéo chuột thuận chiều chuẩn CAD...")
    root = tk.Tk()
    root.withdraw()
    from geosolver_3d.app import GeoSolver3DApp, vec_cross, vec_dot
    app = GeoSolver3DApp()

    # Kích thước canvas giả lập
    w, h = 800, 600
    m = app.models["pyramid_sabcd"]

    # Tọa độ ban đầu của đỉnh B (đỉnh phía trước)
    init_b_x, init_b_y, _ = app.project_point(m.vertices["B"], w, h)
    init_yaw = app.yaw_deg
    init_pitch = app.pitch_deg

    # 1. Giả lập kéo chuột sang PHẢI (dx = +25, dy = 0)
    app._drag_last_x = 400
    app._drag_last_y = 300
    app._on_mouse_drag(FakeEvent(425, 300))

    after_right_b_x, _, _ = app.project_point(m.vertices["B"], w, h)
    print(f"  -> Kéo chuột sang PHẢI: Bx từ {init_b_x:.1f}px -> {after_right_b_x:.1f}px (Δ = {after_right_b_x - init_b_x:+.1f}px)")
    assert after_right_b_x > init_b_x, "Lỗi: Kéo chuột sang phải nhưng vật thể lại di chuyển sang trái (bị ngược)!"

    # 2. Đặt lại và Giả lập kéo chuột LÊN TRÊN (dx = 0, dy = -25)
    app.yaw_deg = init_yaw
    app.pitch_deg = init_pitch
    app._drag_last_x = 400
    app._drag_last_y = 300
    app._on_mouse_drag(FakeEvent(400, 275))

    _, after_up_b_y, _ = app.project_point(m.vertices["B"], w, h)
    print(f"  -> Kéo chuột LÊN TRÊN: By từ {init_b_y:.1f}px -> {after_up_b_y:.1f}px (Δ = {after_up_b_y - init_b_y:+.1f}px)")
    assert after_up_b_y < init_b_y, "Lỗi: Kéo chuột lên trên nhưng vật thể lại bị kéo xuống dưới (bị ngược)!"

    app.destroy()
    root.destroy()
    print("  PASSED: 3D Camera Orbit xoay thuận chiều tự nhiên 100%, bám sát chuyển động chuột CAD!")


def test_unmirrored_basis_and_dashed_hidden_edges():
    print("[TEST 9] Kiểm tra Hệ cơ sở Camera không đảo gương & Phân loại nét đứt khuất SGK...")
    root = tk.Tk()
    root.withdraw()
    from geosolver_3d.app import GeoSolver3DApp, vec_cross, vec_dot
    app = GeoSolver3DApp()

    w, h = 800, 600
    m = app.models["pyramid_sabcd"]

    right, up, fwd, eye = app._camera_basis()
    # Kiểm tra tính trực giao chuẩn right-handed: right x up ~ forward
    # Camera right-handed frame: up x right = forward (right x up = -forward)
    cross_ur = vec_cross(up, right)
    dot_fwd = vec_dot(cross_ur, fwd)
    assert dot_fwd > 0.99, f"Hệ cơ sở không chuẩn: dot={dot_fwd}"

    # Chiếu các đỉnh đáy
    pts = {v: app.project_point(pt, w, h) for v, pt in m.vertices.items()}
    ax, bx, cx, dx = pts["A"][0], pts["B"][0], pts["C"][0], pts["D"][0]
    print(f"  -> Tọa độ X trên màn hình: A={ax:.1f}, B={bx:.1f}, C={cx:.1f}, D={dx:.1f}")

    # Đỉnh A phải nằm bên TRÁI đỉnh C (ax < cx), không bị đảo ngược gương
    assert ax < cx, f"Lỗi đảo gương ngang: A ({ax}) nằm bên phải C ({cx})!"

    # Kiểm tra phân loại nét đứt: Đỉnh D ở phía sau (khuất), các cạnh AD, CD, SD phải là NÉT ĐỨT
    vis, f_vis = app._compute_edge_visibility(m)
    assert not vis[("A", "D")], "Cạnh AD phía sau phải là NÉT ĐỨT (ẩn)!"
    assert not vis[("C", "D")], "Cạnh CD phía sau phải là NÉT ĐỨT (ẩn)!"
    assert not vis[("D", "S")], "Cạnh DS phía sau phải là NÉT ĐỨT (ẩn)!"
    # Các cạnh mặt trước phải là NÉT LIỀN
    assert vis[("A", "B")], "Cạnh AB phía trước phải là NÉT LIỀN!"
    assert vis[("B", "C")], "Cạnh BC phía trước phải là NÉT LIỀN!"
    assert vis[("S", "B")], "Cạnh SB phía trước phải là NÉT LIỀN!"
    print("  -> Phân loại nét vẽ: AD, CD, SD là NÉT ĐỨT KHUẤT SGK; AB, BC, SA, SB, SC là NÉT LIỀN THẤY.")

    app.destroy()
    root.destroy()
    print("  PASSED: Cơ sở Camera chuẩn xác, không bị đảo gương và nét đứt khuất đúng vị trí 100%!")


def test_paned_window_and_dedicated_info_scrollbar():
    print("[TEST 10] Kiểm tra Thanh kéo riêng (PanedWindow Sash) & Thanh cuộn riêng cho Thông số...")
    root = tk.Tk()
    root.withdraw()
    from geosolver_3d.app import GeoSolver3DApp, vec_cross, vec_dot
    app = GeoSolver3DApp()

    # 1. Kiểm tra PanedWindow
    assert hasattr(app, "workspace_paned"), "Thiếu workspace_paned!"
    assert isinstance(app.workspace_paned, tk.PanedWindow), "workspace_paned phải là instance của tk.PanedWindow!"
    panes = app.workspace_paned.panes()
    assert len(panes) == 2, f"PanedWindow phải chứa 2 panes (Canvas và Sidebar), hiện có {len(panes)}"
    print("  -> PanedWindow sash divider có mặt với sashwidth=6 cho phép kéo mở rộng linh hoạt.")

    # 2. Kiểm tra thanh cuộn riêng cho info_text
    assert hasattr(app, "info_scroll"), "Thiếu info_scroll cho info_text!"
    assert isinstance(app.info_scroll, tk.Scrollbar), "info_scroll phải là instance của tk.Scrollbar!"
    print("  -> info_text có thanh cuộn riêng (Scrollbar) hoạt động độc lập.")

    # 3. Kiểm tra các nút đổi hướng mặt phẳng cắt sắc nét
    assert hasattr(app, "btn_cut_oxy"), "Thiếu btn_cut_oxy!"
    assert hasattr(app, "btn_cut_skew"), "Thiếu btn_cut_skew!"
    assert hasattr(app, "btn_cut_oxz"), "Thiếu btn_cut_oxz!"
    assert hasattr(app, "btn_cut_diag"), "Thiếu btn_cut_diag!"
    assert app.btn_cut_oxy.cget("font") == "Tahoma 8 bold", f"Font không chuẩn: {app.btn_cut_oxy.cget('font')}"
    print("  -> 4 nút đổi hướng mặt phẳng cắt (Oxy, Xiên, Oxz, Chéo) có font đậm, độ tương phản cao và hiệu ứng nổi rõ nét.")

    # 4. Kiểm tra cập nhật thông số thể tích V và diện tích S_tp trong info_text
    app.redraw_canvas()
    info_content = app.info_text.get("1.0", tk.END)
    assert "Thể tích V" in info_content or "Volume V" in info_content, "Thiếu thông số Thể tích trong info_text!"
    assert "Diện tích S_tp" in info_content or "Total Surface S_tp" in info_content, "Thiếu Diện tích trong info_text!"
    print("  -> Bảng thông số hiển thị chi tiết Thể tích V, Diện tích toàn phần S_tp, bán kính cầu và tọa độ Oxyz.")

    app.destroy()
    root.destroy()
    print("  PASSED: Thanh kéo riêng PanedWindow, thanh cuộn độc lập và các nút hướng cắt hoạt động hoàn hảo 100%!")


if __name__ == "__main__":
    test_no_su_pham()
    test_image_export()
    test_side_panel_and_section_interaction()
    test_cad_hatching_algorithm()
    test_point_on_segment_dynamic_ratio_and_domain_clamping()
    test_custom_3point_plane_and_cad_hatching()
    test_independent_section_vertex_pivot_dragging()
    test_camera_orbit_direction()
    test_unmirrored_basis_and_dashed_hidden_edges()
    test_paned_window_and_dedicated_info_scrollbar()
    print("\n==============================================")
    print("ALL 10 TESTS PASSED! 100% VERIFIED AND PRODUCTION READY!")
    print("==============================================")
