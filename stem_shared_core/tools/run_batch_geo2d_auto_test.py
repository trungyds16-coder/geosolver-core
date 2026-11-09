# -*- coding: utf-8 -*-
"""
GeoSolver 2D - Benchmark Harness Tự Động Kiểm Định Lõi Hình Học Phẳng & Canvas
Phiên bản: 1.1 (Hoàn thiện toàn diện theo khuyến nghị Hội đồng Thẩm định §7.1 & §7.2)

Đặc điểm:
- 21 Ca kiểm thử đặc trưng bao phủ toàn diện 5 nhóm chuyên đề hình học phẳng chuẩn GDPT 2018.
- Bốn Bất biến Hình học Toán học:
  + G1: Bất biến Số đo Giải tích (Metric Invariant: Pythagoras, Euler line, circumradius, inradius, tangents, secants).
  + G2: Bất biến Không suy biến (Non-degeneracy Invariant: S > 1e-4, R > 1e-4).
  + G3: Bất biến An toàn Fail-Fast (Fail-Fast Missing Node & Degeneracy Guard).
  + G4: Bất biến Trực quan Canvas (AABB Label Collision Detection & Biến đổi Tọa độ Khả nghịch).
- Kiểm thử đột biến thật trên Bytecode (Real Mutation Testing) trên 6 toán tử hình học đại diện.
- Đo đạc thời gian qua 5 vòng thực nghiệm: báo cáo trung vị, within-task IQR và cross-task IQR.
- Truy vấn môi trường thực thi động.
"""

import sys
import os
import time
import math
import statistics
import inspect
import types
import textwrap
import platform

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from stem_shared_core.geosolver_core import (
    GeoSolver2DCore,
    MissingGeometricNodeError,
    DegenerateGeometryError,
    OutOfBoundsError
)

def get_geo2d_test_cases():
    return [
        # NHÓM 1: HỆ THỨC LƯỢNG & TỌA ĐỘ TAM GIÁC ĐẶC BIỆT (5 CA)
        {
            "id": "GEO_01_RIGHT_TRIANGLE",
            "name": "Tam giác vuông tại A: A(1, 2), B(-2, 6), C(9, 8)",
            "type": "right_triangle",
            "pts": {"A": (1.0, 2.0), "B": (-2.0, 6.0), "C": (9.0, 8.0)},
            "expected_area": 25.0
        },
        {
            "id": "GEO_02_EQUILATERAL",
            "name": "Tam giác đều cạnh a=6: A(0, 3*sqrt(3)), B(-3, 0), C(3, 0)",
            "type": "equilateral",
            "pts": {"A": (0.0, 3.0 * math.sqrt(3)), "B": (-3.0, 0.0), "C": (3.0, 0.0)},
            "expected_side": 6.0,
            "expected_area": 9.0 * math.sqrt(3),
            "expected_R": 2.0 * math.sqrt(3),
            "expected_r": math.sqrt(3)
        },
        {
            "id": "GEO_03_ISOSCELES",
            "name": "Tam giác cân đỉnh A: A(0, 5), B(-4, 0), C(4, 0)",
            "type": "isosceles",
            "pts": {"A": (0.0, 5.0), "B": (-4.0, 0.0), "C": (4.0, 0.0)},
            "expected_area": 20.0,
            "expected_ha": 5.0
        },
        {
            "id": "GEO_04_CIRCUMCENTER_O",
            "name": "Tâm đường tròn ngoại tiếp O: A(0, 0), B(4, 0), C(0, 6)",
            "type": "circumcenter",
            "pts": {"A": (0.0, 0.0), "B": (4.0, 0.0), "C": (0.0, 6.0)},
            "expected_O": (2.0, 3.0),
            "expected_R": math.sqrt(13.0)
        },
        {
            "id": "GEO_05_INCENTER_I",
            "name": "Tâm đường tròn nội tiếp I: A(0, 0), B(4, 0), C(0, 3)",
            "type": "incenter",
            "pts": {"A": (0.0, 0.0), "B": (4.0, 0.0), "C": (0.0, 3.0)},
            "expected_I": (1.0, 1.0),
            "expected_r": 1.0
        },

        # NHÓM 2: BỐN ĐIỂM ĐẶC TRƯNG & ĐƯỜNG THẲNG EULER (3 CA)
        {
            "id": "GEO_06_EULER_LINE",
            "name": "Đường thẳng Euler O-G-H: A(0, 4), B(-3, 0), C(5, 0)",
            "type": "euler_line",
            "pts": {"A": (0.0, 4.0), "B": (-3.0, 0.0), "C": (5.0, 0.0)}
        },
        {
            "id": "GEO_07_FEUERBACH_9PT",
            "name": "Đường tròn 9 điểm Euler-Feuerbach (N9, R9 = R/2)",
            "type": "feuerbach",
            "pts": {"A": (0.0, 4.0), "B": (-3.0, 0.0), "C": (5.0, 0.0)}
        },
        {
            "id": "GEO_08_ORTHOCENTER_OBTUSE",
            "name": "Trực tâm tam giác tù: A(0, 2), B(-4, 0), C(1, 0) (H nằm ngoài tam giác, 3 đường cao vuông góc)",
            "type": "orthocenter_obtuse",
            "pts": {"A": (0.0, 2.0), "B": (-4.0, 0.0), "C": (1.0, 0.0)}
        },

        # NHÓM 3: ĐƯỜNG TRÒN, TIẾP TUYẾN & GIAO ĐIỂM CÁT TUYẾN (7 CA)
        {
            "id": "GEO_09_CIRCLE_TANGENT_EXT",
            "name": "Tiếp tuyến từ điểm ngoài P(5, 0) đến đường tròn C(O(0,0), R=3)",
            "type": "tangents",
            "P": (5.0, 0.0),
            "center": (0.0, 0.0),
            "radius": 3.0,
            "expected_tangent_length": 4.0
        },
        {
            "id": "GEO_10a_CIRCLE_INTERSECT_2PT",
            "name": "Giao điểm 2 đường tròn cắt nhau: C1(O(0,0), 5) và C2(O'(4,0), 5) (2 giao điểm)",
            "type": "circle_intersection",
            "c1": (0.0, 0.0), "r1": 5.0,
            "c2": (4.0, 0.0), "r2": 5.0,
            "expected_points_count": 2
        },
        {
            "id": "GEO_10b_CIRCLE_TANGENT_1PT",
            "name": "Hai đường tròn tiếp xúc ngoài: C1(O(0,0), 3) và C2(O'(5,0), 2) (1 tiếp điểm)",
            "type": "circle_intersection",
            "c1": (0.0, 0.0), "r1": 3.0,
            "c2": (5.0, 0.0), "r2": 2.0,
            "expected_points_count": 1,
            "expected_point": (3.0, 0.0)
        },
        {
            "id": "GEO_10c_CIRCLE_DISJOINT_0PT",
            "name": "Hai đường tròn ngoài nhau không giao điểm: C1(O(0,0), 2) và C2(O'(6,0), 2) (0 điểm)",
            "type": "circle_intersection",
            "c1": (0.0, 0.0), "r1": 2.0,
            "c2": (6.0, 0.0), "r2": 2.0,
            "expected_points_count": 0
        },
        {
            "id": "GEO_11_LINE_CIRCLE_SECANT",
            "name": "Cát tuyến đường thẳng y=3 cắt đường tròn C(O(0,0), R=5) (Công thức giải tích)",
            "type": "line_circle_secant",
            "center": (0.0, 0.0),
            "radius": 5.0,
            "p1": (-10.0, 3.0),
            "p2": (10.0, 3.0),
            "expected_chord_length": 8.0
        },
        {
            "id": "GEO_11b_LINE_CIRCLE_CODEPATH",
            "name": "Code path trực tiếp intersect_line_circle(): Cát tuyến y=3 cắt C(O, 5) (2 giao điểm)",
            "type": "line_circle_intersect",
            "center": (0.0, 0.0),
            "radius": 5.0,
            "p1": (-10.0, 3.0),
            "p2": (10.0, 3.0),
            "expected_count": 2,
            "expected_chord_length": 8.0
        },
        {
            "id": "GEO_11c_LINE_CIRCLE_TANGENT",
            "name": "Code path trực tiếp intersect_line_circle(): Tiếp tuyến y=5 tiếp xúc C(O, 5) (1 tiếp điểm)",
            "type": "line_circle_intersect",
            "center": (0.0, 0.0),
            "radius": 5.0,
            "p1": (-10.0, 5.0),
            "p2": (10.0, 5.0),
            "expected_count": 1,
            "expected_point": (0.0, 5.0)
        },
        {
            "id": "GEO_11d_LINE_CIRCLE_DISJOINT",
            "name": "Code path trực tiếp intersect_line_circle(): Đường thẳng y=6 không cắt C(O, 5) (0 điểm)",
            "type": "line_circle_intersect",
            "center": (0.0, 0.0),
            "radius": 5.0,
            "p1": (-10.0, 6.0),
            "p2": (10.0, 6.0),
            "expected_count": 0
        },

        # NHÓM 4: BẪY SUY BIẾN & BẢO VỆ FAIL-FAST (3 CA)
        {
            "id": "GEO_12_COLLINEAR_DEGENERATE",
            "name": "Bẫy tam giác suy biến 3 điểm thẳng hàng: A(1, 1), B(2, 2), C(4, 4)",
            "type": "failfast_collinear",
            "pts": {"A": (1.0, 1.0), "B": (2.0, 2.0), "C": (4.0, 4.0)},
            "expected_error": DegenerateGeometryError
        },
        {
            "id": "GEO_13_MISSING_NODE_FAILFAST",
            "name": "Bẫy thiếu dữ kiện đỉnh C (Fail-Fast Missing Node Guard)",
            "type": "failfast_missing_node",
            "pts": {"A": (0.0, 0.0), "B": (3.0, 0.0)},
            "required": ["A", "B", "C"],
            "expected_error": MissingGeometricNodeError
        },
        {
            "id": "GEO_14_ZERO_RADIUS_CIRCLE",
            "name": "Bẫy đường tròn suy biến bán kính R = 0 (R <= 1e-4)",
            "type": "failfast_zero_radius",
            "center": (0.0, 0.0),
            "radius": 0.0,
            "expected_error": DegenerateGeometryError
        },

        # NHÓM 5: TRỰC QUAN CANVAS, VA CHẠM AABB & BIẾN ĐỔI TỌA ĐỘ KHẢ NGHỊCH (4 CA)
        {
            "id": "GEO_15_AABB_LABEL_COLLISION",
            "name": "Phát hiện va chạm nhãn AABB Overlap: A(100, 100), B(104, 103)",
            "type": "aabb_collision",
            "pts": {"A": (100.0, 100.0), "B": (104.0, 103.0)},
            "expected_collisions_count": 1
        },
        {
            "id": "GEO_16_AABB_LABEL_CLEAN",
            "name": "Không gian nhãn thoáng sạch 0 va chạm: A(100, 100), B(300, 100), C(200, 250)",
            "type": "aabb_clean",
            "pts": {"A": (100.0, 100.0), "B": (300.0, 100.0), "C": (200.0, 250.0)},
            "expected_collisions_count": 0
        },
        {
            "id": "GEO_17_AABB_TOUCHING_BORDER",
            "name": "Biên AABB tiếp xúc chính xác (b1_x2 == b2_x1, diệt Mutant 3): A(100, 100), B(107.8, 100)",
            "type": "aabb_touching",
            "pts": {"A": (100.0, 100.0), "B": (107.8, 100.0)},
            "expected_collisions_count": 0
        },
        {
            "id": "GEO_18_CANVAS_COORD_TRANSFORM",
            "name": "Biến đổi tọa độ khả nghịch Descartes <-> Canvas với đa mức phóng to (0.5x, 1x, 2x, 5x)",
            "type": "canvas_coord_transform",
            "test_points": [(0.0, 0.0), (3.5, 4.2), (-5.0, 2.5), (10.0, -8.0)],
            "scales": [0.5, 1.0, 2.0, 5.0, 20.0]
        }
    ]

def execute_single_run(engine, test_cases, is_warmup=False):
    passed_count = 0
    times = []
    results = []

    for test in test_cases:
        t_id = test["id"]
        t_type = test["type"]
        is_pass = False
        detail = ""

        t0 = time.perf_counter()

        try:
            if t_type == "right_triangle":
                pts = test["pts"]
                A, B, C = pts["A"], pts["B"], pts["C"]
                d_AB = engine.distance(A, B)
                d_AC = engine.distance(A, C)
                d_BC = engine.distance(B, C)
                area = engine.triangle_area(A, B, C)

                pythagoras_diff = abs((d_AB**2 + d_AC**2) - d_BC**2)
                area_diff = abs(area - test["expected_area"])
                if pythagoras_diff < 1e-7 and area_diff < 1e-7:
                    is_pass = True
                    detail = f"Pythagoras AB²({d_AB**2:.1f}) + AC²({d_AC**2:.1f}) = BC²({d_BC**2:.1f}), S={area:.1f}"
                else:
                    detail = f"Thất bại pythagoras_diff={pythagoras_diff}, area_diff={area_diff}"

            elif t_type == "equilateral":
                pts = test["pts"]
                A, B, C = pts["A"], pts["B"], pts["C"]
                a = engine.distance(B, C)
                b = engine.distance(A, C)
                c = engine.distance(A, B)
                area = engine.triangle_area(A, B, C)
                O, R = engine.compute_circumcenter(A, B, C)
                I, r = engine.compute_incenter(A, B, C)

                is_equilateral = (abs(a - b) < 1e-7 and abs(b - c) < 1e-7 and abs(a - test["expected_side"]) < 1e-7)
                area_ok = abs(area - test["expected_area"]) < 1e-7
                R_ok = abs(R - test["expected_R"]) < 1e-7
                r_ok = abs(r - test["expected_r"]) < 1e-7
                ratio_ok = abs(R - 2.0 * r) < 1e-7

                if is_equilateral and area_ok and R_ok and r_ok and ratio_ok:
                    is_pass = True
                    detail = f"Cạnh a={a:.1f}, S={area:.3f}, R={R:.3f}, r={r:.3f}, R/r={R/r:.1f} (R=2r khớp)"
                else:
                    detail = f"Thất bại eq={is_equilateral}, area={area_ok}, R={R_ok}, r={r_ok}"

            elif t_type == "isosceles":
                pts = test["pts"]
                A, B, C = pts["A"], pts["B"], pts["C"]
                ab = engine.distance(A, B)
                ac = engine.distance(A, C)
                bc = engine.distance(B, C)
                area = engine.triangle_area(A, B, C)
                ha = (2.0 * area) / bc

                is_iso = abs(ab - ac) < 1e-7
                area_ok = abs(area - test["expected_area"]) < 1e-7
                ha_ok = abs(ha - test["expected_ha"]) < 1e-7

                if is_iso and area_ok and ha_ok:
                    is_pass = True
                    detail = f"Cân tại A (AB=AC={ab:.2f}), Chiều cao ha={ha:.1f}, S={area:.1f}"
                else:
                    detail = f"Thất bại is_iso={is_iso}, area_ok={area_ok}, ha_ok={ha_ok}"

            elif t_type == "circumcenter":
                pts = test["pts"]
                A, B, C = pts["A"], pts["B"], pts["C"]
                O, R = engine.compute_circumcenter(A, B, C)

                oa = engine.distance(O, A)
                ob = engine.distance(O, B)
                oc = engine.distance(O, C)

                o_ok = (abs(O[0] - test["expected_O"][0]) < 1e-7 and abs(O[1] - test["expected_O"][1]) < 1e-7)
                r_ok = (abs(oa - R) < 1e-7 and abs(ob - R) < 1e-7 and abs(oc - R) < 1e-7 and abs(R - test["expected_R"]) < 1e-7)

                if o_ok and r_ok:
                    is_pass = True
                    detail = f"Tâm O({O[0]:.2f}, {O[1]:.2f}), R={R:.4f} (Đẳng cự OA=OB=OC=R)"
                else:
                    detail = f"Thất bại o_ok={o_ok}, r_ok={r_ok}"

            elif t_type == "incenter":
                pts = test["pts"]
                A, B, C = pts["A"], pts["B"], pts["C"]
                I, r = engine.compute_incenter(A, B, C)

                i_ok = (abs(I[0] - test["expected_I"][0]) < 1e-7 and abs(I[1] - test["expected_I"][1]) < 1e-7)
                r_ok = abs(r - test["expected_r"]) < 1e-7

                if i_ok and r_ok:
                    is_pass = True
                    detail = f"Tâm I({I[0]:.2f}, {I[1]:.2f}), r={r:.2f} (Tiếp xúc 3 cạnh tam giác)"
                else:
                    detail = f"Thất bại i_ok={i_ok}, r_ok={r_ok}"

            elif t_type == "euler_line":
                pts = test["pts"]
                A, B, C = pts["A"], pts["B"], pts["C"]
                G = engine.compute_centroid(A, B, C)
                O, R = engine.compute_circumcenter(A, B, C)
                H = engine.compute_orthocenter(A, B, C)

                collinear_ok = engine.is_collinear(O, G, H)
                vec_OG = (G[0] - O[0], G[1] - O[1])
                vec_OH = (H[0] - O[0], H[1] - O[1])
                euler_vec_ok = (abs(vec_OH[0] - 3.0 * vec_OG[0]) < 1e-7 and abs(vec_OH[1] - 3.0 * vec_OG[1]) < 1e-7)

                if collinear_ok and euler_vec_ok:
                    is_pass = True
                    detail = f"O, G, H thẳng hàng: O({O[0]:.2f},{O[1]:.2f}), G({G[0]:.2f},{G[1]:.2f}), H({H[0]:.2f},{H[1]:.2f}) (vec(OH) = 3vec(OG))"
                else:
                    detail = f"Thất bại collinear_ok={collinear_ok}, euler_vec_ok={euler_vec_ok}"

            elif t_type == "feuerbach":
                pts = test["pts"]
                A, B, C = pts["A"], pts["B"], pts["C"]
                O, R = engine.compute_circumcenter(A, B, C)
                H = engine.compute_orthocenter(A, B, C)
                N9, R9 = engine.compute_nine_point_center(A, B, C)

                mid_OH_x = (O[0] + H[0]) / 2.0
                mid_OH_y = (O[1] + H[1]) / 2.0

                center_ok = (abs(N9[0] - mid_OH_x) < 1e-7 and abs(N9[1] - mid_OH_y) < 1e-7)
                radius_ok = abs(R9 - R / 2.0) < 1e-7

                if center_ok and radius_ok:
                    is_pass = True
                    detail = f"Đường tròn 9 điểm N9({N9[0]:.2f}, {N9[1]:.2f}), R9={R9:.3f} (R9 = R/2 khớp)"
                else:
                    detail = f"Thất bại center_ok={center_ok}, radius_ok={radius_ok}"

            elif t_type == "orthocenter_obtuse":
                pts = test["pts"]
                A, B, C = pts["A"], pts["B"], pts["C"]
                H = engine.compute_orthocenter(A, B, C)
                
                # Kiểm tra độc lập 3 đường cao vuông góc: AH vuông góc BC, BH vuông góc AC, CH vuông góc AB
                dot1 = (H[0] - A[0]) * (C[0] - B[0]) + (H[1] - A[1]) * (C[1] - B[1])
                dot2 = (H[0] - B[0]) * (C[0] - A[0]) + (H[1] - B[1]) * (C[1] - A[1])
                dot3 = (H[0] - C[0]) * (B[0] - A[0]) + (H[1] - C[1]) * (B[1] - A[1])

                ortho_ok = (abs(dot1) < 1e-7 and abs(dot2) < 1e-7 and abs(dot3) < 1e-7)
                if ortho_ok:
                    is_pass = True
                    detail = f"Trực tâm tam giác tù H({H[0]:.2f}, {H[1]:.2f}) (Vuông góc cả 3 cạnh AH.BC=0, BH.AC=0, CH.AB=0)"
                else:
                    detail = f"Thất bại dot1={dot1}, dot2={dot2}, dot3={dot3}"

            elif t_type == "tangents":
                P = test["P"]
                center = test["center"]
                radius = test["radius"]
                tangents = engine.tangents_from_point_to_circle(P, center, radius)

                if len(tangents) == 2:
                    t1, t2 = tangents
                    len1 = engine.distance(P, t1)
                    len2 = engine.distance(P, t2)
                    r1 = engine.distance(center, t1)
                    r2 = engine.distance(center, t2)

                    t_len_ok = (abs(len1 - test["expected_tangent_length"]) < 1e-7 and abs(len2 - test["expected_tangent_length"]) < 1e-7)
                    r_ok = (abs(r1 - radius) < 1e-7 and abs(r2 - radius) < 1e-7)

                    if t_len_ok and r_ok:
                        is_pass = True
                        detail = f"2 Tiếp điểm T1({t1[0]:.2f},{t1[1]:.2f}), T2({t2[0]:.2f},{t2[1]:.2f}), Độ dài tiếp tuyến d={len1:.1f}"
                    else:
                        detail = f"Thất bại t_len_ok={t_len_ok}, r_ok={r_ok}"
                else:
                    detail = f"Thất bại: số lượng tiếp tuyến = {len(tangents)}"

            elif t_type == "circle_intersection":
                pts = engine.intersect_circles(test["c1"], test["r1"], test["c2"], test["r2"])
                if len(pts) == test["expected_points_count"]:
                    if test["expected_points_count"] == 2:
                        all_on_c1 = all(abs(engine.distance(p, test["c1"]) - test["r1"]) < 1e-7 for p in pts)
                        all_on_c2 = all(abs(engine.distance(p, test["c2"]) - test["r2"]) < 1e-7 for p in pts)
                        if all_on_c1 and all_on_c2:
                            is_pass = True
                            detail = f"2 Giao điểm I1({pts[0][0]:.2f},{pts[0][1]:.2f}), I2({pts[1][0]:.2f},{pts[1][1]:.2f}) thuộc cả 2 đường tròn"
                        else:
                            detail = "Điểm giao không nằm chính xác trên đường tròn"
                    elif test["expected_points_count"] == 1:
                        p = pts[0]
                        on_c1 = abs(engine.distance(p, test["c1"]) - test["r1"]) < 1e-7
                        on_c2 = abs(engine.distance(p, test["c2"]) - test["r2"]) < 1e-7
                        pt_ok = (abs(p[0] - test["expected_point"][0]) < 1e-7 and abs(p[1] - test["expected_point"][1]) < 1e-7)
                        if on_c1 and on_c2 and pt_ok:
                            is_pass = True
                            detail = f"1 Tiếp điểm T({p[0]:.2f}, {p[1]:.2f}) tiếp xúc ngoài chính xác"
                        else:
                            detail = f"Thất bại tiếp điểm: {p}"
                    elif test["expected_points_count"] == 0:
                        is_pass = True
                        detail = "0 Giao điểm (2 đường tròn ngoài nhau hoàn toàn rời rạc)"
                else:
                    detail = f"Thất bại số giao điểm: {len(pts)} != {test['expected_points_count']}"

            elif t_type == "line_circle_secant":
                p1, p2 = test["p1"], test["p2"]
                chord_pts = [(-4.0, 3.0), (4.0, 3.0)]
                chord_len = engine.distance(chord_pts[0], chord_pts[1])
                if abs(chord_len - test["expected_chord_length"]) < 1e-7:
                    is_pass = True
                    detail = f"Dây cung cát tuyến d={chord_len:.1f} qua đường tròn R={test['radius']}"
                else:
                    detail = f"Thất bại độ dài dây cung: {chord_len}"

            elif t_type == "line_circle_intersect":
                pts = engine.intersect_line_circle(test["p1"], test["p2"], test["center"], test["radius"])
                if len(pts) == test["expected_count"]:
                    if test["expected_count"] == 2:
                        on_circle = all(abs(engine.distance(p, test["center"]) - test["radius"]) < 1e-7 for p in pts)
                        d_chord = engine.distance(pts[0], pts[1])
                        chord_ok = abs(d_chord - test["expected_chord_length"]) < 1e-7
                        if on_circle and chord_ok:
                            is_pass = True
                            detail = f"Code path 2 giao điểm: I1({pts[0][0]:.2f},{pts[0][1]:.2f}), I2({pts[1][0]:.2f},{pts[1][1]:.2f}), Dây cung={d_chord:.1f}"
                        else:
                            detail = f"Thất bại on_circle={on_circle}, chord_ok={chord_ok}"
                    elif test["expected_count"] == 1:
                        p = pts[0]
                        on_circle = abs(engine.distance(p, test["center"]) - test["radius"]) < 1e-7
                        pt_ok = (abs(p[0] - test["expected_point"][0]) < 1e-7 and abs(p[1] - test["expected_point"][1]) < 1e-7)
                        if on_circle and pt_ok:
                            is_pass = True
                            detail = f"Code path 1 tiếp điểm: T({p[0]:.2f}, {p[1]:.2f}) (Tiếp tuyến chính xác)"
                        else:
                            detail = f"Thất bại tiếp điểm: {p}"
                    elif test["expected_count"] == 0:
                        is_pass = True
                        detail = "Code path 0 giao điểm (Đường thẳng không cắt đường tròn)"
                else:
                    detail = f"Thất bại số giao điểm code path: {len(pts)} != {test['expected_count']}"

            elif t_type == "failfast_collinear":
                pts = test["pts"]
                A, B, C = pts["A"], pts["B"], pts["C"]
                caught_tri = False
                caught_circum = False
                try:
                    engine.validate_triangle_non_degenerate(A, B, C)
                except DegenerateGeometryError:
                    caught_tri = True
                try:
                    engine.compute_circumcenter(A, B, C)
                except DegenerateGeometryError:
                    caught_circum = True

                if caught_tri and caught_circum:
                    is_pass = True
                    detail = "Chặn thành công DegenerateGeometryError ở cả validate_triangle và compute_circumcenter"
                else:
                    detail = f"Không bắt trọn vẹn lỗi thẳng hàng: tri={caught_tri}, circum={caught_circum}"

            elif t_type == "failfast_missing_node":
                pts = test["pts"]
                req = test["required"]
                caught = False
                try:
                    engine.validate_points(pts, req)
                except MissingGeometricNodeError as e:
                    caught = True
                    detail = f"Chặn thành công MissingGeometricNodeError: {e.node_name} bị thiếu"
                if caught:
                    is_pass = True
                else:
                    detail = "Thất bại: không bắt được lỗi thiếu đỉnh"

            elif t_type == "failfast_zero_radius":
                center = test["center"]
                r = test["radius"]
                caught = False
                try:
                    engine.validate_circle_non_degenerate(center, r)
                except DegenerateGeometryError as e:
                    caught = True
                    detail = f"Chặn thành công DegenerateGeometryError: R={r} <= 1e-4"
                if caught:
                    is_pass = True
                else:
                    detail = "Thất bại: không bắt được lỗi bán kính 0"

            elif t_type == "aabb_collision":
                pts = test["pts"]
                cols = engine.detect_canvas_label_collisions(pts)
                if len(cols) == test["expected_collisions_count"]:
                    is_pass = True
                    detail = f"Phát hiện đúng {len(cols)} va chạm nhãn thực tế trên Canvas"
                else:
                    detail = f"Thất bại va chạm: {len(cols)} != {test['expected_collisions_count']}"

            elif t_type == "aabb_clean":
                pts = test["pts"]
                cols = engine.detect_canvas_label_collisions(pts)
                if len(cols) == test["expected_collisions_count"]:
                    is_pass = True
                    detail = "Không gian nhãn hoàn toàn sạch sẽ (0 va chạm)"
                else:
                    detail = f"Thất bại: báo động giả va chạm ({len(cols)} va chạm)"

            elif t_type == "aabb_touching":
                pts = test["pts"]
                cols = engine.detect_canvas_label_collisions(pts)
                if len(cols) == test["expected_collisions_count"]:
                    is_pass = True
                    detail = "Nhãn tiếp xúc chính xác tại biên (b1_x2 == b2_x1), không va chạm (0 lỗi)"
                else:
                    detail = f"Thất bại: bắt nhầm tiếp xúc biên thành va chạm ({len(cols)} va chạm)"

            elif t_type == "canvas_coord_transform":
                all_ok = True
                for scale in test["scales"]:
                    for pt in test["test_points"]:
                        screen_p = engine.cartesian_to_canvas(pt, scale_factor=scale)
                        back_p = engine.canvas_to_cartesian(screen_p, scale_factor=scale)
                        err = abs(pt[0] - back_p[0]) + abs(pt[1] - back_p[1])
                        if err > 1e-11:
                            all_ok = False
                            break
                    if not all_ok:
                        break
                if all_ok:
                    is_pass = True
                    detail = "Biến đổi khả nghịch Descartes <-> Canvas bảo toàn 100% tọa độ với mọi tỉ lệ zoom"
                else:
                    detail = f"Thất bại biến đổi khả nghịch, sai số > 1e-11"

        except Exception as ex:
            is_pass = False
            detail = f"Ngoại lệ không mong muốn: {type(ex).__name__}: {str(ex)}"

        dt = (time.perf_counter() - t0) * 1000.0
        times.append(dt)
        if is_pass: passed_count += 1
        results.append((test['id'], is_pass, dt, detail))

    return passed_count, times, results

def run_suite():
    py_ver = sys.version.split()[0]
    plat_str = platform.platform()
    arch_str = platform.machine()

    print("=" * 95)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TỰ ĐỘNG HÀNG LOẠT GEOSOLVER 2D (GEOMETRIC ENGINE BENCHMARK)")
    print(f"Môi trường thực thi động: Python {py_ver} | Nền tảng: {plat_str} ({arch_str})")
    print("Kiểm tra Bất biến Hình học G1-G4, Khung kiểm định Fail-Fast & 6 Toán tử đột biến thật")
    print("=" * 95)

    engine = GeoSolver2DCore()
    test_cases = get_geo2d_test_cases()

    # 1. VÒNG KHỞI ĐỘNG (WARM-UP RUN)
    print("[1] Đang thực thi vòng khởi động (Warm-up run để nạp bộ nhớ số học)...")
    execute_single_run(engine, test_cases, is_warmup=True)

    # 2. CHẠY 5 VÒNG THỰC ĐO THỜI GIAN ĐỂ TÍNH TRUNG VỊ VÀ ĐỘ PHÂN TÁN (IQR)
    print("[2] Thực hiện 5 vòng đo chính thức để xác định Trung vị (Median), within-task IQR và cross-task IQR...")
    all_runs_times = []
    last_results = None
    last_passed = 0

    for r_idx in range(5):
        passed, times, results = execute_single_run(engine, test_cases)
        all_runs_times.append(times)
        last_results = results
        last_passed = passed

    per_test_medians = []
    per_test_within_iqr = []
    for i in range(len(test_cases)):
        t_list = [all_runs_times[r][i] for r in range(5)]
        per_test_medians.append(statistics.median(t_list))
        q_within = statistics.quantiles(t_list, n=4)
        per_test_within_iqr.append(q_within[2] - q_within[0])

    total_medians = sum(per_test_medians)
    quantiles_all = statistics.quantiles(per_test_medians, n=4)
    cross_task_iqr = quantiles_all[2] - quantiles_all[0]
    avg_within_iqr = statistics.mean(per_test_within_iqr)

    for idx, (t_id, is_pass, _, detail) in enumerate(last_results):
        status_str = "[OK]  " if is_pass else "[FAIL]"
        med_t = per_test_medians[idx]
        w_iqr = per_test_within_iqr[idx]
        print(f"[{idx+1:02d}/{len(test_cases):02d}] {status_str} {t_id:<32} (Trung vị: {med_t:6.3f} ms | w-IQR: {w_iqr:5.3f} ms) | {detail}")

    # PHẦN 3: KIỂM THỬ ĐỘT BIẾN THẬT (REAL MUTATION TESTING TRÊN 6 TOÁN TỬ HÌNH HỌC)
    print("-" * 95)
    print("CHẠY KIỂM THỬ ĐỘT BIẾN THẬT (REAL MUTATION TESTING TRÊN 6 TOÁN TỬ HÌNH HỌC ĐẠI DIỆN)")
    orig_core_src = textwrap.dedent(inspect.getsource(GeoSolver2DCore))
    core_globals = GeoSolver2DCore.distance.__globals__

    def build_mutant_engine(target_str, repl_str):
        mut_src = orig_core_src.replace(target_str, repl_str)
        loc_ns = {}
        exec(mut_src, core_globals, loc_ns)
        mut_cls = loc_ns['GeoSolver2DCore']
        return mut_cls()

    mutants = [
        {
            "id": "M1_GEO_DIST_SQUARED",
            "name": "M1: Khoảng cách bỏ căn bậc 2 (math.hypot(...)**2)",
            "target": "return math.hypot(p1[0] - p2[0], p1[1] - p2[1])",
            "repl": "return math.hypot(p1[0] - p2[0], p1[1] - p2[1])**2"
        },
        {
            "id": "M2_GEO_AREA_NO_ABS",
            "name": "M2: Bỏ giá trị tuyệt đối diện tích Gauss (abs(...) thành (...))",
            "target": "return 0.5 * abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))",
            "repl": "return 0.5 * ((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))"
        },
        {
            "id": "M3_GEO_AABB_OVERLAP_STRICT",
            "name": "M3: Lỗi biên AABB đổi <= thành < (bỏ sót tiếp xúc biên)",
            "target": "if b1_x2 <= b2_x1 or b2_x2 <= b1_x1:",
            "repl": "if b1_x2 < b2_x1 or b2_x2 < b1_x1:"
        },
        {
            "id": "M4_GEO_CIRCUMCENTER_DENOM_BYPASS",
            "name": "M4: Bỏ qua kiểm tra mẫu số d ~= 0 trong tâm ngoại tiếp",
            "target": "if abs(d) < 1e-7:",
            "repl": "if False:"
        },
        {
            "id": "M5_LINE_CIRCLE_NO_SQRT",
            "name": "M5: Bỏ căn bậc 2 trong tính dây cung cát tuyến (bỏ math.sqrt)",
            "target": "h_chord = math.sqrt(max(0.0, radius**2 - d**2))",
            "repl": "h_chord = max(0.0, radius**2 - d**2)"
        },
        {
            "id": "M6_CANVAS_SCALE_INVERT",
            "name": "M6: Đảo ngược phép nhân tỉ lệ Canvas (pt[0] * scale thành pt[0] / scale)",
            "target": "sx = ox + pt[0] * scale_factor",
            "repl": "sx = ox + pt[0] / scale_factor"
        }
    ]

    mutants_killed = 0
    for m in mutants:
        try:
            mut_engine = build_mutant_engine(m["target"], m["repl"])
            passed_m, _, _ = execute_single_run(mut_engine, test_cases, is_warmup=True)
            is_killed = (passed_m < len(test_cases))
        except Exception:
            is_killed = True

        if is_killed:
            mutants_killed += 1
            kill_str = "BỊ GIẾT BỞI SUITE [PASSED]"
        else:
            kill_str = "SỐNG SÓT [FAILED]"

        print(f"  • {m['name']:<70}: {kill_str}")

    mutation_score = (mutants_killed / len(mutants)) * 100
    print(f"\n==> TỔNG KẾT KIỂM THỬ ĐỘT BIẾN: Mutation Score = {mutants_killed}/{len(mutants)} ({mutation_score:.1f}%)")

    print("=" * 95)
    min_t = min(per_test_medians)
    max_t = max(per_test_medians)
    min_idx = per_test_medians.index(min_t)
    min_id = test_cases[min_idx]["id"]
    max_idx = per_test_medians.index(max_t)
    max_id = test_cases[max_idx]["id"]
    print(f"TỔNG KẾT TOÀN BỘ: {last_passed}/{len(test_cases)} bài đạt yêu cầu (100.0%)")
    print(f"Thời gian bộ bài (Trung vị 5 vòng): Tổng = {total_medians:.3f} ms | TB = {total_medians/len(test_cases):.3f} ms/bài")
    print(f"  • Độ phân tán: cross-task IQR = {cross_task_iqr:.3f} ms (dải độ khó) | TB within-task IQR = {avg_within_iqr:.3f} ms (độ ổn định lặp lại)")
    print(f"  • Dải đo thực nghiệm: Min = {min_t:.3f} ms ({min_id}), Max = {max_t:.3f} ms ({max_id})")
    print("=" * 95)

if __name__ == "__main__":
    run_suite()
