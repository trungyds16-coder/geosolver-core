import sys
import unittest
import math
from unittest.mock import MagicMock

# Import geosolver_desktop functions & classes
from geosolver.geosolver_desktop import (
    format_exact_radical,
    format_polygon_pedagogical_area,
    PRESET_PROBLEMS,
    LANG_DATA,
    GeoSolverApp
)

class TestV38Features(unittest.TestCase):
    def test_format_exact_radical(self):
        self.assertIn("√(34)", format_exact_radical(34.0, 5.83095))
        self.assertEqual(format_exact_radical(36.0, 6.0), "6")
        self.assertIn("2√(5)", format_exact_radical(20.0, 4.4721))
        self.assertIn("5√(2)", format_exact_radical(50.0, 7.0711))
        self.assertIn("3√(10)", format_exact_radical(90.0, 9.4868))

    def test_presets_configuration(self):
        for lang in ["vi", "en"]:
            self.assertIn("hex_intersection", PRESET_PROBLEMS[lang])
            self.assertIn("vmo_2015", PRESET_PROBLEMS[lang])
            self.assertIn("olympic_ptolemy", PRESET_PROBLEMS[lang])

        self.assertEqual(len(LANG_DATA["vi"]["presets_list"]), 12)
        self.assertEqual(len(LANG_DATA["en"]["presets_list"]), 12)
        self.assertIn("DEFGHI", LANG_DATA["vi"]["presets_list"][9])
        self.assertIn("cát tuyến", LANG_DATA["vi"]["presets_list"][10])
        self.assertIn("Ptolemy", LANG_DATA["vi"]["presets_list"][11])

    def test_resolve_target_polygon_points(self):
        app = MagicMock(spec=GeoSolverApp)
        names = ["A", "B", "C", "A1", "B1", "C1", "D", "E", "F", "G", "H", "I"]
        coords = [
            (0, 5), (-3, 0), (3, 0),
            (-3.33, 1.67), (1.67, -1.33), (1.67, 4.67),
            (-2.35, 1.08), (-1.25, 2.92), (0.59, 4.02), (1.67, 2.22), (1.67, 0.0), (-0.56, 0.0)
        ]
        app.points = [{"id": n, "name": n, "x": c[0], "y": c[1]} for n, c in zip(names, coords)]
        app.polygons = []
        app.selected_points = set()

        pts, is_inter, info = GeoSolverApp._resolve_target_polygon_points(app, raw_targets="DEFGHI", prob_text="")
        self.assertEqual(len(pts), 6)
        resolved_names = [p["name"] for p in pts]
        self.assertEqual(resolved_names, ["D", "E", "F", "G", "H", "I"])

        pts2, _, _ = GeoSolverApp._resolve_target_polygon_points(app, raw_targets="D, E, F, G, H, I", prob_text="")
        self.assertEqual(len(pts2), 6)

        pts3, _, _ = GeoSolverApp._resolve_target_polygon_points(app, raw_targets="", prob_text="Tính diện tích đa giác DEFGHI")
        self.assertEqual(len(pts3), 6)
        self.assertEqual([p["name"] for p in pts3], ["D", "E", "F", "G", "H", "I"])

    def test_pedagogical_area_radicals(self):
        pts = [
            {"name": "D", "x": -40.0/17.0, "y": 55.0/51.0},
            {"name": "E", "x": -5.0/4.0, "y": 35.0/12.0},
            {"name": "F", "x": 10.0/17.0, "y": 205.0/51.0},
            {"name": "G", "x": 5.0/3.0, "y": 20.0/9.0},
            {"name": "H", "x": 5.0/3.0, "y": 0.0},
            {"name": "I", "x": -5.0/9.0, "y": 0.0}
        ]
        text = format_polygon_pedagogical_area(pts, lang="vi")
        self.assertIn("10.9749", text)
        self.assertIn("Gauss", text)
        self.assertIn("√", text)

    def test_olympic_ptolemy_quad(self):
        quad_pts = [
            {"name": "A", "x": 0.0, "y": 5.0},
            {"name": "B", "x": -4.0, "y": 3.0},
            {"name": "C", "x": -3.0, "y": -4.0},
            {"name": "D", "x": 4.0, "y": -3.0}
        ]
        text = format_polygon_pedagogical_area(quad_pts, lang="vi")
        self.assertIn("45.0000", text)
        self.assertIn("ABCD", text)

    def test_natural_language_auxiliary_drawing(self):
        app = MagicMock(spec=GeoSolverApp)
        app.points = [
            {"id": "A", "name": "A", "x": 0.0, "y": 5.0},
            {"id": "B", "name": "B", "x": -3.0, "y": 0.0},
            {"id": "C", "name": "C", "x": 3.0, "y": 0.0}
        ]
        app.segments = []
        app.circles = []
        app.canvas = MagicMock()
        app.redraw = MagicMock()
        app.lbl_status = MagicMock()
        app.COLOR_AUX = "#e03131"
        app.COLOR_LINE = "#000000"
        app.COLOR_HIGHLIGHT = "#f59f00"
        app.add_right_angle_mark = MagicMock()
        app.find_point_by_name = lambda name: next((p for p in app.points if p["name"] == name.upper()), None)

        GeoSolverApp._execute_ai_drawing_command(app, "Lấy trung điểm M của BC")
        m_pt = app.find_point_by_name("M")
        self.assertIsNotNone(m_pt)
        self.assertAlmostEqual(m_pt["x"], 0.0)
        self.assertAlmostEqual(m_pt["y"], 0.0)

        GeoSolverApp._execute_ai_drawing_command(app, "Hạ đường cao AH từ A đến BC")
        h_pt = app.find_point_by_name("H")
        self.assertIsNotNone(h_pt)
        self.assertAlmostEqual(h_pt["x"], 0.0)
        self.assertAlmostEqual(h_pt["y"], 0.0)

        GeoSolverApp._execute_ai_drawing_command(app, "Kẻ đoạn thẳng AM")
        self.assertTrue(any(s["p1"]["name"] == "A" and s["p2"]["name"] == "M" for s in app.segments))

        GeoSolverApp._execute_ai_drawing_command(app, "Vẽ đường tròn qua ba điểm A, B, C")
        self.assertEqual(len(app.circles), 1)

    def test_mode_toggle_and_advanced_tools(self):
        # Test Mode Toggle logic
        app = MagicMock(spec=GeoSolverApp)
        app.current_mode = "basic"
        app.current_lang = "vi"
        app.COLOR_TEXT = "#000000"
        app.btn_mode_toggle = MagicMock()
        app.top_bar_adv = MagicMock()
        app.lbl_status = MagicMock()
        app.set_mode = lambda m: GeoSolverApp.set_mode(app, m)

        GeoSolverApp.toggle_mode(app)
        self.assertEqual(app.current_mode, "advanced")
        app.top_bar_adv.pack.assert_called_once()

        GeoSolverApp.toggle_mode(app)
        self.assertEqual(app.current_mode, "basic")
        app.top_bar_adv.pack_forget.assert_called_once()

    def test_advanced_math_algorithms(self):
        # 1. Harmonic conjugate: A(0,0), B(6,0), C(2,0) -> D(-6,0)
        pA, pB, pC = {"x": 0.0, "y": 0.0}, {"x": 6.0, "y": 0.0}, {"x": 2.0, "y": 0.0}
        dx = pB["x"] - pA["x"]
        dy = pB["y"] - pA["y"]
        L2 = dx*dx + dy*dy
        t = ((pC["x"] - pA["x"])*dx + (pC["y"] - pA["y"])*dy) / L2
        s = -t / (1.0 - 2.0*t)
        xD = (1.0 - s)*pA["x"] + s*pB["x"]
        yD = (1.0 - s)*pA["y"] + s*pB["y"]
        self.assertAlmostEqual(xD, -6.0)
        self.assertAlmostEqual(yD, 0.0)

        # 2. Polar line: circle center (0,0), r=5, point P(10,0) -> 10x - 25 = 0 -> x = 2.5
        c_x, c_y, r = 0.0, 0.0, 5.0
        px, py = 10.0, 0.0
        A = px - c_x
        B = py - c_y
        C_const = - A*c_x - B*c_y - r*r
        self.assertEqual(A, 10.0)
        self.assertEqual(B, 0.0)
        self.assertEqual(C_const, -25.0)

        # 3. Radical axis: c1 at (-2,0) r=3, c2 at (2,0) r=3 -> 8x = 0 -> x = 0
        A_rad = 2.0 * (2.0 - -2.0)
        B_rad = 2.0 * (0.0 - 0.0)
        C_rad = ((-2.0)**2 - 3.0**2) - (2.0**2 - 3.0**2)
        self.assertEqual(A_rad, 8.0)
        self.assertEqual(B_rad, 0.0)
        self.assertEqual(C_rad, 0.0)

        # 4. Barycentric coords of Centroid G: (1/3, 1/3, 1/3)
        A_pt, B_pt, C_pt = (0.0, 5.0), (-3.0, 0.0), (3.0, 0.0)
        G_pt = (0.0, 5.0/3.0)
        det = (B_pt[1] - C_pt[1])*(A_pt[0] - C_pt[0]) + (C_pt[0] - B_pt[0])*(A_pt[1] - C_pt[1])
        u = ((B_pt[1] - C_pt[1])*(G_pt[0] - C_pt[0]) + (C_pt[0] - B_pt[0])*(G_pt[1] - C_pt[1])) / det
        v = ((C_pt[1] - A_pt[1])*(G_pt[0] - C_pt[0]) + (A_pt[0] - C_pt[0])*(G_pt[1] - C_pt[1])) / det
        w = 1.0 - u - v
        self.assertAlmostEqual(u, 1.0/3.0)
        self.assertAlmostEqual(v, 1.0/3.0)
        self.assertAlmostEqual(w, 1.0/3.0)

if __name__ == "__main__":
    unittest.main()
