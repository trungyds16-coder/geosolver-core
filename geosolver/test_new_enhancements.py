import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from geosolver_desktop import (
    GeoSolverApp,
    format_polygon_pedagogical_area,
    clip_polygon_sutherland_hodgman,
    calc_ellipse_area,
    calc_ellipse_perimeter,
    compute_ellipse_parameters,
    sample_ellipse_points,
    compute_isosceles_trapezoid_vertex_d,
    compute_parallelogram_vertex_d,
    compute_rhombus_vertices_cd
)

def test_validate_point_name():
    valid, _ = GeoSolverApp.validate_point_name("A")
    assert valid is True
    valid, _ = GeoSolverApp.validate_point_name("B1")
    assert valid is True
    valid, _ = GeoSolverApp.validate_point_name("M10")
    assert valid is True
    valid, _ = GeoSolverApp.validate_point_name("z99")
    assert valid is True
    
    # Invalid names (2+ letters or illegal chars)
    valid, msg = GeoSolverApp.validate_point_name("AB")
    assert valid is False
    assert "AB" in msg
    
    valid, _ = GeoSolverApp.validate_point_name("MNP")
    assert valid is False
    valid, _ = GeoSolverApp.validate_point_name("1A")
    assert valid is False
    valid, _ = GeoSolverApp.validate_point_name("A_1")
    assert valid is False
    valid, _ = GeoSolverApp.validate_point_name("")
    assert valid is False
    valid, _ = GeoSolverApp.validate_point_name("  ")
    assert valid is False

def test_get_next_point_name():
    class DummySolver:
        def __init__(self, pts):
            self.points = pts
        get_next_point_name = GeoSolverApp.get_next_point_name

    solver0 = DummySolver([])
    assert solver0.get_next_point_name() == "A"
    
    solver2 = DummySolver([{"name": "A"}, {"name": "B"}])
    assert solver2.get_next_point_name() == "C"

def test_format_polygon_pedagogical_area_triangle():
    # Right triangle at (0,0), (4,0), (0,3) -> Area = 6, Perimeter = 12, sides = 4, 5, 3
    pts = [
        {"name": "A", "x": 0.0, "y": 0.0},
        {"name": "B", "x": 4.0, "y": 0.0},
        {"name": "C", "x": 0.0, "y": 3.0}
    ]
    txt_vi = format_polygon_pedagogical_area(pts, lang="vi")
    assert "Heron" in txt_vi
    assert "Shoelace" in txt_vi
    assert "6.0000" in txt_vi
    assert "12.0000" in txt_vi

    txt_en = format_polygon_pedagogical_area(pts, lang="en")
    assert "Heron" in txt_en
    assert "Shoelace" in txt_en
    assert "Perimeter" in txt_en

def test_format_polygon_pedagogical_area_polygon():
    # Square (0,0), (2,0), (2,2), (0,2) -> Area = 4
    pts = [
        {"name": "A", "x": 0.0, "y": 0.0},
        {"name": "B", "x": 2.0, "y": 0.0},
        {"name": "C", "x": 2.0, "y": 2.0},
        {"name": "D", "x": 0.0, "y": 2.0}
    ]
    txt = format_polygon_pedagogical_area(pts, lang="vi")
    assert "Shoelace" in txt
    assert "4.0000" in txt

def test_clip_polygon_sutherland_hodgman():
    poly1 = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]
    poly2 = [(1.0, 1.0), (3.0, 1.0), (3.0, 3.0), (1.0, 3.0)]
    inter = clip_polygon_sutherland_hodgman(poly1, poly2)
    assert len(inter) >= 3
    for x, y in inter:
        assert 0.99 <= x <= 2.01
        assert 0.99 <= y <= 2.01

def test_ellipse_calculations():
    # Ellipse with a = 5, b = 3
    area = calc_ellipse_area(5.0, 3.0)
    expected_area = math.pi * 15.0
    assert abs(area - expected_area) < 1e-6

    perim = calc_ellipse_perimeter(5.0, 3.0)
    # Ramanujan approximation for a=5, b=3 is ~ 25.5269
    assert 25.5 <= perim <= 25.6

    params = compute_ellipse_parameters(0.0, 0.0, 5.0, 0.0, 0.0, 3.0)
    assert abs(params["a"] - 5.0) < 1e-6
    assert abs(params["b"] - 3.0) < 1e-6
    assert abs(params["theta"] - 0.0) < 1e-6

    pts = sample_ellipse_points(0.0, 0.0, 5.0, 3.0, 0.0, num_samples=72)
    assert len(pts) == 73
    # Check bounding box
    for x, y in pts:
        assert -5.01 <= x <= 5.01
        assert -3.01 <= y <= 3.01

def test_isosceles_trapezoid_vertex_d():
    # Base AB along x-axis from (-3, 0) to (3, 0) -> length = 6, midpoint M = (0, 0)
    # Vertex C at (2, 4) -> should reflect to D at (-2, 4)
    dx, dy = compute_isosceles_trapezoid_vertex_d(-3.0, 0.0, 3.0, 0.0, 2.0, 4.0)
    assert abs(dx - (-2.0)) < 1e-6
    assert abs(dy - 4.0) < 1e-6

    # Slanted base: A(0,0), B(4,4) -> midpoint (2,2)
    # Check that distance AD == BC
    ax, ay = 0.0, 0.0
    bx, by = 4.0, 4.0
    cx, cy = 1.0, 5.0
    dx, dy = compute_isosceles_trapezoid_vertex_d(ax, ay, bx, by, cx, cy)
    dist_ad = math.hypot(dx - ax, dy - ay)
    dist_bc = math.hypot(bx - cx, by - cy)
    assert abs(dist_ad - dist_bc) < 1e-6

def test_parallelogram_and_rhombus_helpers():
    # Parallelogram: A(0,0), B(4,0), C(5,3) -> D = A + (C - B) = (1, 3)
    dx, dy = compute_parallelogram_vertex_d(0.0, 0.0, 4.0, 0.0, 5.0, 3.0)
    assert abs(dx - 1.0) < 1e-6
    assert abs(dy - 3.0) < 1e-6

    # Rhombus: A(0,0), B(5,0), direction C(2, 4)
    (cx_n, cy_n), (dx, dy) = compute_rhombus_vertices_cd(0.0, 0.0, 5.0, 0.0, 2.0, 4.0)
    len_ab = 5.0
    len_bc = math.hypot(cx_n - 5.0, cy_n - 0.0)
    len_cd = math.hypot(dx - cx_n, dy - cy_n)
    len_da = math.hypot(dx - 0.0, dy - 0.0)
    assert abs(len_bc - len_ab) < 1e-6
    assert abs(len_cd - len_ab) < 1e-6
    assert abs(len_da - len_ab) < 1e-6

def test_ai_agent_drawing_commands():
    from geosolver.geosolver_desktop import GeoSolverApp
    
    class DummyLabel:
        def config(self, **kwargs): pass

    class MockApp:
        def __init__(self):
            self.points = [
                {"id": "pt_1", "name": "A", "x": 0.0, "y": 0.0},
                {"id": "pt_2", "name": "B", "x": 4.0, "y": 0.0},
                {"id": "pt_3", "name": "C", "x": 0.0, "y": 3.0},
            ]
            self.segments = []
            self.circles = []
            self.lbl_status = DummyLabel()
        
        find_point_by_name = GeoSolverApp.find_point_by_name
        _execute_ai_drawing_command = GeoSolverApp._execute_ai_drawing_command
        def _save_state(self): pass
        def redraw(self): pass
        def _update_algebra_tree(self): pass

    app = MockApp()
    # 1. Test drawing segment
    res = app._execute_ai_drawing_command("Gợi ý kẻ đường phụ: [DRAW_SEGMENT: B, C]")
    assert res is True
    assert len(app.segments) == 1
    assert app.segments[0]["style"] == "dashed"
    assert app.segments[0]["color"] == "#e03131"

    # 2. Test drawing midpoint
    res_m = app._execute_ai_drawing_command("Lấy trung điểm: [DRAW_MIDPOINT: M, B, C]")
    assert res_m is True
    pM = app.find_point_by_name("M")
    assert pM is not None
    assert abs(pM["x"] - 2.0) < 1e-6
    assert abs(pM["y"] - 1.5) < 1e-6

    # 3. Test perpendicular foot
    # From A(0,0) perpendicular to BC (B(4,0), C(0,3))
    res_h = app._execute_ai_drawing_command("Hạ đường cao: [DRAW_PERPENDICULAR: H, A, B, C]")
    assert res_h is True
    pH = app.find_point_by_name("H")
    assert pH is not None

if __name__ == "__main__":
    test_validate_point_name()
    test_get_next_point_name()
    test_format_polygon_pedagogical_area_triangle()
    test_format_polygon_pedagogical_area_polygon()
    test_clip_polygon_sutherland_hodgman()
    test_ellipse_calculations()
    test_isosceles_trapezoid_vertex_d()
    test_parallelogram_and_rhombus_helpers()
    test_ai_agent_drawing_commands()
    print("ALL TESTS PASSED SUCCESSFULLY!")
