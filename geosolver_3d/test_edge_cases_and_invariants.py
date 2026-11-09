# -*- coding: utf-8 -*-
"""
test_edge_cases_and_invariants.py
Suite kiểm tra bất biến hình học, trường hợp suy biến và ma trận Test Vectors (TV-3D-01 -> TV-3D-15)
cho Phân hệ GeoSolver 3D (Spatial Geometry Kernel & DGS).
"""

import sys
import os
import math
import pytest

# Ensure parent directory is in sys.path
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_CURRENT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

from geosolver_3d.geometry3d_kernel import (
    Point3D,
    Vector3D,
    Plane3D,
    create_pyramid_sabcd,
    create_tetrahedron_sabc,
    create_prism_abc_a1b1c1,
    create_cuboid,
    create_truncated_pyramid,
    create_octahedron,
    distance_point_to_plane,
    distance_point_to_line,
    distance_between_lines,
    distance_between_skew_lines,
    find_common_perpendicular,
    angle_between_two_lines,
    angle_between_planes,
    angle_line_and_plane,
    intersect_plane_with_polyhedron,
    compute_polygon_area_and_perimeter,
    compute_polyhedron_volume,
    circumscribed_sphere,
    great_circle_distance,
    spherical_triangle_area,
    intersect_sphere_with_plane,
    Sphere3D,
    GeometricConstraintSolver,
    DistancePointToPlaneConstraint,
)


def test_tv_3d_01_euler_polyhedron_formula():
    """TV-3D-01: Bất biến đặc trưng Euler V - E + F = 2 cho 7 khối đa diện chuẩn."""
    polyhedra = [
        ("Tứ diện S.ABC", create_tetrahedron_sabc(4.0, 5.0)),
        ("Chóp tứ giác S.ABCD", create_pyramid_sabcd(4.0, 3.0, 5.0)),
        ("Hình hộp chữ nhật", create_cuboid(4.0, 3.0, 5.0)),
        ("Lăng trụ tam giác", create_prism_abc_a1b1c1(4.0, 5.0)),
        ("Bát diện đều", create_octahedron(4.0)),
        ("Chóp cụt tứ giác", create_truncated_pyramid(4.0, 2.0, 3.0, base_sides=4)),
        ("Chóp cụt tam giác", create_truncated_pyramid(4.0, 2.0, 3.0, base_sides=3)),
    ]
    for name, poly in polyhedra:
        V = len(poly["vertices"])
        E = len(poly["edges"])
        F = len(poly["faces"])
        euler = V - E + F
        assert euler == 2, f"Khối '{name}' vi phạm định lý Euler: V={V}, E={E}, F={F} => V-E+F={euler} != 2"
    print("  [TV-3D-01] PASS: 7/7 khối đa diện chuẩn tuân thủ tuyệt đối định lý Euler V - E + F = 2.")


def test_tv_3d_02_degenerate_collinear_plane():
    """TV-3D-02: Bẫy suy biến - 3 điểm thẳng hàng phải ném ValueError."""
    P1 = Point3D("A", 1.0, 2.0, 3.0)
    P2 = Point3D("B", 2.0, 4.0, 6.0)
    P3 = Point3D("C", 3.0, 6.0, 9.0)  # Thẳng hàng: P3 = 2*P2 - P1
    try:
        Plane3D.from_three_points(P1, P2, P3)
        assert False, "Không ném ValueError khi 3 điểm thẳng hàng!"
    except ValueError as e:
        assert "thẳng hàng" in str(e)
    print("  [TV-3D-02] PASS: Phát hiện và xử lý chính xác 3 điểm thẳng hàng (ném ValueError có thông báo).")


def test_tv_3d_03_angle_lines_boundary_clamping():
    """TV-3D-03: Góc giữa 2 đường thẳng với công thức atan2 chống mất số có nghĩa và bảo vệ biên."""
    # Song song cùng chiều
    u1 = Vector3D(1.0, 2.0, 3.0)
    u2 = Vector3D(2.0, 4.0, 6.0)
    deg_par = angle_between_two_lines(u1, u2)
    assert abs(deg_par - 0.0) < 1e-9

    # Song song ngược chiều
    u3 = Vector3D(-1.0, -2.0, -3.0)
    deg_opp = angle_between_two_lines(u1, u3)
    assert abs(deg_opp - 0.0) < 1e-9

    # Vuông góc
    u_orth = Vector3D(2.0, -1.0, 0.0)  # u1 . u_orth = 2 - 2 + 0 = 0
    deg_orth = angle_between_two_lines(u1, u_orth)
    assert abs(deg_orth - 90.0) < 1e-9

    # Nhiễu 1 ULP (Unit in the Last Place) bằng math.nextafter:
    x_pert = math.nextafter(1.0, 2.0)
    u_almost = Vector3D(x_pert, 2.0, 3.0)
    deg_almost = angle_between_two_lines(u1, u_almost)
    assert not math.isnan(deg_almost) and not math.isinf(deg_almost)
    # atan2 phân giải được góc vi mô khác 0 tuyệt đối (~3.3e-15 độ), hiển thị giao diện 0.0000 độ
    assert 0.0 < deg_almost < 1e-12
    assert f"{deg_almost:.4f}" == "0.0000"
    print("  [TV-3D-03] PASS: Góc giữa 2 đường thẳng tính chuẩn biên [0, 90 độ], bảo vệ acos/atan2 chống NaN (atan2 micro-angle ~3.3e-15 deg).")


def test_tv_3d_04_angle_between_planes():
    """TV-3D-04: Góc giữa 2 mặt phẳng."""
    p_xy = Plane3D(0.0, 0.0, 1.0, 0.0)  # z = 0
    p_yz = Plane3D(1.0, 0.0, 0.0, 0.0)  # x = 0
    deg = angle_between_planes(p_xy, p_yz)
    assert abs(deg - 90.0) < 1e-9

    p_xy_shifted = Plane3D(0.0, 0.0, 1.0, -10.0)  # z = 10 (song song)
    deg_par = angle_between_planes(p_xy, p_xy_shifted)
    assert abs(deg_par - 0.0) < 1e-9
    print("  [TV-3D-04] PASS: Góc giữa 2 mặt phẳng vuông góc (90 độ) và song song (0 độ) chính xác.")


def test_tv_3d_05_angle_line_and_plane():
    """TV-3D-05: Góc giữa đường thẳng và mặt phẳng trong [0, 90 deg]."""
    p_xy = Plane3D(0.0, 0.0, 1.0, 0.0)
    # Đường thẳng vuông góc mặt phẳng (VTCP = (0, 0, 1))
    u_perp = Vector3D(0.0, 0.0, 1.0)
    deg_perp = angle_line_and_plane(u_perp, p_xy)
    assert abs(deg_perp - 90.0) < 1e-9

    # Đường thẳng song song mặt phẳng (VTCP = (1, 1, 0))
    u_par = Vector3D(1.0, 1.0, 0.0)
    deg_par = angle_line_and_plane(u_par, p_xy)
    assert abs(deg_par - 0.0) < 1e-9
    print("  [TV-3D-05] PASS: Góc giữa đường thẳng và mặt phẳng tính chính xác cho các trường hợp đặc biệt.")


def test_tv_3d_06_distance_between_lines():
    """TV-3D-06: Khoảng cách giữa hai đường thẳng song song vs chéo nhau."""
    # 2 đường song song: d1 qua O(0,0,0) vtcp (1,0,0); d2 qua (0,3,4) vtcp (1,0,0)
    A1 = Point3D("A1", 0.0, 0.0, 0.0)
    A2 = Point3D("A2", 0.0, 3.0, 4.0)
    u = Vector3D(1.0, 0.0, 0.0)
    d_par = distance_between_lines(A1, u, A2, u)
    assert abs(d_par - 5.0) < 1e-9  # sqrt(3^2 + 4^2) = 5.0
    print(f"  [TV-3D-06] PASS: Khoảng cách giữa 2 đường thẳng song song d={d_par:.4f} (kỳ vọng 5.0000).")


def test_tv_3d_07_common_perpendicular_skew_lines():
    """TV-3D-07: Đoạn vuông góc chung giữa 2 đường chéo nhau thỏa mãn điều kiện trực giao."""
    # d1: qua A(0,0,0) vtcp (1,0,0) trục Ox
    # d2: qua B(0,2,3) vtcp (0,1,0) song song Oy
    A = Point3D("A", 0.0, 0.0, 0.0)
    u1 = Vector3D(1.0, 0.0, 0.0)
    B = Point3D("B", 0.0, 2.0, 3.0)
    u2 = Vector3D(0.0, 1.0, 0.0)

    M1, M2, d = find_common_perpendicular(A, u1, B, u2)
    # Đoạn vuông góc chung phải song song với Oz, có độ dài 3.0
    assert abs(d - 3.0) < 1e-9
    assert M1.is_close(Point3D("M1", 0.0, 0.0, 0.0))
    assert M2.is_close(Point3D("M2", 0.0, 0.0, 3.0))

    # Kiểm tra trực giao: (M1 - M2) . u1 == 0 và (M1 - M2) . u2 == 0
    m_vec = M1.vector_to(M2)
    assert abs(m_vec.dot_product(u1)) < 1e-9
    assert abs(m_vec.dot_product(u2)) < 1e-9
    print(f"  [TV-3D-07] PASS: Đường vuông góc chung thỏa mãn trực giao 100% với cả 2 VTCP.")


def test_tv_3d_08_cube_cross_section_and_area():
    """TV-3D-08: Thiết diện hình hộp chữ nhật cắt bởi mặt phẳng song song đáy."""
    cuboid = create_cuboid(a=4.0, b=3.0, c=5.0)
    plane = Plane3D(0.0, 0.0, 1.0, -2.5)  # Mặt phẳng z = 2.5 cắt ngang khối
    section_pts = intersect_plane_with_polyhedron(cuboid, plane)
    assert len(section_pts) == 4
    area, perim = compute_polygon_area_and_perimeter(section_pts)
    assert abs(area - 12.0) < 1e-6  # S = 4 * 3 = 12
    assert abs(perim - 14.0) < 1e-6  # P = 2 * (4 + 3) = 14
    print(f"  [TV-3D-08] PASS: Thiết diện hình hộp chữ nhật có diện tích S={area:.2f}, chu vi P={perim:.2f} chuẩn xác.")


def test_tv_3d_09_pyramid_cross_section_homothety():
    """TV-3D-09: Thiết diện hình chóp cắt bởi mặt phẳng song song đáy tại z = h/2."""
    h = 6.0
    a = 4.0
    b = 4.0
    pyramid = create_pyramid_sabcd(a=a, b=b, h=h, sa_perp=True)
    # Cắt tại z = 3.0 (trung điểm chiều cao) -> tỉ số vị tự k = 1/2
    plane = Plane3D(0.0, 0.0, 1.0, -3.0)
    section_pts = intersect_plane_with_polyhedron(pyramid, plane)
    assert len(section_pts) == 4
    area, perim = compute_polygon_area_and_perimeter(section_pts)
    # Diện tích đáy = 16, tại z = h/2 diện tích phải bằng 16 * (1/2)^2 = 4.0
    assert abs(area - 4.0) < 1e-6
    print(f"  [TV-3D-09] PASS: Vị tự thiết diện hình chóp S_sec={area:.4f} khớp hoàn toàn tỉ số đồng dạng (1/2)^2*S_đáy.")


def test_tv_3d_10_segment_plane_intersection_endpoints():
    """TV-3D-10: Giao điểm đoạn thẳng - mặt phẳng khi đầu mút nằm trên mặt phẳng."""
    p_plane = Plane3D(0.0, 0.0, 1.0, 0.0)  # Oxy (z = 0)
    P1 = Point3D("P1", 1.0, 2.0, 0.0)     # Nằm trên mặt phẳng
    P2 = Point3D("P2", 3.0, 4.0, 5.0)     # Nằm ngoài mặt phẳng

    from geosolver_3d.geometry3d_kernel import _intersect_segment_with_plane
    pts = _intersect_segment_with_plane(P1, P2, p_plane)
    assert len(pts) == 1
    assert pts[0].is_close(P1)
    print("  [TV-3D-10] PASS: Xử lý chính xác trường hợp biên đoạn thẳng có mút nằm trên mặt phẳng.")


def test_tv_3d_11_polyhedron_volume_exact_formulas():
    """TV-3D-11: Thể tích khối đa diện phân rã tứ diện khớp với công thức giải tích chuẩn."""
    # 1. Hình hộp chữ nhật: V = a * b * c = 4 * 3 * 5 = 60
    cuboid = create_cuboid(4.0, 3.0, 5.0)
    v_cuboid = compute_polyhedron_volume(cuboid)
    assert abs(v_cuboid - 60.0) < 1e-5

    # 2. Hình chóp S.ABCD đáy chữ nhật 4x3, h=5: V = (1/3) * S * h = (1/3) * 12 * 5 = 20.0
    pyramid = create_pyramid_sabcd(4.0, 3.0, 5.0, sa_perp=True)
    v_pyramid = compute_polyhedron_volume(pyramid)
    assert abs(v_pyramid - 20.0) < 1e-5

    # 3. Bát diện đều cạnh a=4: V = (sqrt(2)/3) * a^3 = (sqrt(2)/3) * 64 ≈ 30.16996
    octa = create_octahedron(4.0)
    v_octa = compute_polyhedron_volume(octa)
    expected_v_octa = (math.sqrt(2.0) / 3.0) * (4.0 ** 3)
    assert abs(v_octa - expected_v_octa) < 1e-5
    print(f"  [TV-3D-11] PASS: Thể tích giải tích: Hình hộp=60.0, Chóp=20.0, Bát diện={v_octa:.4f} đạt chuẩn 100%.")


def test_tv_3d_12_circumscribed_sphere_invariants():
    """TV-3D-12: Mặt cầu ngoại tiếp bảo toàn khoảng cách từ tâm đến mọi đỉnh."""
    pyramid = create_pyramid_sabcd(4.0, 3.0, 5.0, sa_perp=True)
    sp = circumscribed_sphere(pyramid)
    I = sp.center
    R = sp.radius

    # Mọi đỉnh S, A, B, C, D phải có khoảng cách đến I bằng R
    for v_name, v_pt in pyramid["vertices"].items():
        dist = I.distance_to(v_pt)
        assert abs(dist - R) < 1e-6, f"Đỉnh {v_name} không nằm trên mặt cầu ngoại tiếp: dist={dist}, R={R}"
    print(f"  [TV-3D-12] PASS: Tất cả các đỉnh của đa diện đều nằm trên mặt cầu ngoại tiếp (sai số < 1e-6).")


def test_tv_3d_13_girard_spherical_excess_theorem():
    """TV-3D-13: Định lý Girard về diện tích tam giác cầu E = (A + B + C - pi) * R^2."""
    R = 100.0
    sphere = Sphere3D(Point3D("O", 0.0, 0.0, 0.0), R)
    # 3 điểm tạo góc phần tám mặt cầu (3 góc vuông A=B=C=pi/2 => E = pi/2)
    P1 = Point3D("P1", R, 0.0, 0.0)
    P2 = Point3D("P2", 0.0, R, 0.0)
    P3 = Point3D("P3", 0.0, 0.0, R)

    area = spherical_triangle_area(P1, P2, P3, sphere)
    expected_area = 0.5 * math.pi * (R ** 2)
    assert abs(area - expected_area) / expected_area < 1e-6
    print(f"  [TV-3D-13] PASS: Định lý Girard đạt chuẩn xác: Diện tích góc phần tám S={area:.4f} (Kỳ vọng {expected_area:.4f}).")


def test_tv_3d_14_haversine_great_circle_invariants():
    """TV-3D-14: Bất biến đối xứng và đối cực khoảng cách vòng lớn Haversine."""
    R = 6371.0
    lat1, lon1 = 21.0285, 105.8542  # Hà Nội
    lat2, lon2 = 10.8231, 106.6297  # TP.HCM

    d_forward = great_circle_distance(lat1, lon1, lat2, lon2, R)
    d_backward = great_circle_distance(lat2, lon2, lat1, lon1, R)
    assert abs(d_forward - d_backward) < 1e-9

    # Hai điểm đối cực (antipodal): khoảng cách phải bằng nửa chu vi pi*R
    d_anti = great_circle_distance(0.0, 0.0, 0.0, 180.0, R)
    assert abs(d_anti - math.pi * R) < 1e-4
    print(f"  [TV-3D-14] PASS: Khoảng cách Haversine đối xứng hoàn hảo và đạt cực đại pi*R tại 2 điểm đối cực.")


def test_tv_3d_15_constraint_solver_convergence():
    """TV-3D-15: Hệ giải ràng buộc hình học động hội tụ chính xác sau nhiễu loạn."""
    plane = Plane3D(1.0, 2.0, 2.0, -9.0)  # Pháp tuyến độ dài sqrt(1+4+4)=3
    solver = GeometricConstraintSolver()
    solver.add_constraint(DistancePointToPlaneConstraint("M", plane, distance=4.0))

    # Điểm M bị kéo tới vị trí ngẫu nhiên
    perturbed_pt = Point3D("M", 100.5, -45.2, 88.7)
    solved_pt = solver.solve_point(perturbed_pt)
    dist = distance_point_to_plane(solved_pt, plane)
    assert abs(dist - 4.0) < 1e-6
    print(f"  [TV-3D-15] PASS: Ràng buộc d(M, plane) = 4.0 hội tụ chính xác từ điểm nhiễu loạn bất kỳ.")


def test_tv_3d_16_skew_orthogonal_lines():
    """TV-3D-16: Hai đường chéo nhau vuông góc u1 . u2 = 0 nhưng không cắt nhau."""
    A1 = Point3D("A1", 1.0, 2.0, 3.0)
    u1 = Vector3D(1.0, 0.0, 0.0)  # song song Ox
    A2 = Point3D("A2", 5.0, 7.0, 9.0)
    u2 = Vector3D(0.0, 1.0, 0.0)  # song song Oy -> u1 . u2 = 0
    M1, M2, d = find_common_perpendicular(A1, u1, A2, u2)
    # Đoạn vuông góc chung phải song song với Oz: M1=(5, 2, 3), M2=(5, 2, 9), d = |9 - 3| = 6.0
    assert abs(d - 6.0) < 1e-9
    assert M1.is_close(Point3D("M1", 5.0, 2.0, 3.0))
    assert M2.is_close(Point3D("M2", 5.0, 2.0, 9.0))
    # Kiểm tra trực giao
    m_vec = M1.vector_to(M2)
    assert abs(m_vec.dot_product(u1)) < 1e-9
    assert abs(m_vec.dot_product(u2)) < 1e-9
    print(f"  [TV-3D-16] PASS: Hai đường vuông góc chéo nhau u1 ⊥ u2, d={d:.4f} (Kỳ vọng 6.0000).")


def test_tv_3d_17_parallel_lines_common_perpendicular():
    """TV-3D-17: Hai đường thẳng song song trong find_common_perpendicular."""
    A1 = Point3D("A1", 2.0, 1.0, 0.0)
    u1 = Vector3D(1.0, 2.0, 2.0)  # length = 3
    A2 = Point3D("A2", 0.0, 4.0, 5.0)
    u2 = Vector3D(2.0, 4.0, 4.0)  # song song cùng chiều (u2 = 2*u1)
    M1, M2, d = find_common_perpendicular(A1, u1, A2, u2)
    # d phải khớp tuyệt đối với distance_between_lines
    d_expected = distance_between_lines(A1, u1, A2, u2)
    assert abs(d - d_expected) < 1e-9
    # M1 thuộc d1, M2 thuộc d2
    assert distance_point_to_line(M1, A1, u1) < 1e-9
    assert distance_point_to_line(M2, A2, u2) < 1e-9
    # M1M2 trực giao với vector chỉ phương
    if d > 1e-9:
        m_vec = M1.vector_to(M2)
        assert abs(m_vec.dot_product(u1.normalize())) < 1e-9
    print(f"  [TV-3D-17] PASS: Nhánh song song find_common_perpendicular: d={d:.4f} khớp distance_between_lines.")


def test_tv_3d_18_nearly_parallel_under_threshold():
    """TV-3D-18: Hai vector lệch cực nhỏ 1e-5 rad (< sqrt(EPSILON)), rẽ nhánh song song có offset dọc trục."""
    # theta = 1e-5 rad => sin^2(theta) ≈ 1e-10 <= EPSILON = 1e-9 -> rẽ nhánh song song
    # Thử nghiệm với offset lớn trên đường d1: A1(1000, 0, 0), u1=(1,0,0); A2(0, 0, 5), u2=(cos 1e-5, sin 1e-5, 0)
    A1 = Point3D("A1", 1000.0, 0.0, 0.0)
    u1 = Vector3D(1.0, 0.0, 0.0)
    theta = 1e-5
    u2 = Vector3D(math.cos(theta), math.sin(theta), 0.0)
    A2 = Point3D("A2", 0.0, 0.0, 5.0)
    M1, M2, d = find_common_perpendicular(A1, u1, A2, u2)
    assert not math.isnan(d) and not math.isinf(d)
    # Khoảng cách hình học trong nhánh song song d = sqrt(25 + 1000^2 * sin^2(1e-5)) ≈ 5.000010
    assert abs(d - 5.0) < 2e-5
    assert abs(d - 5.000010) < 1e-6
    print(f"  [TV-3D-18] PASS: Góc lệch dưới ngưỡng 1e-5 rad (rẽ nhánh song song ổn định, offset A1=(1000,0,0)), d={d:.6f}.")


def test_tv_3d_19_nearly_parallel_above_threshold_skew():
    """TV-3D-19: Hai vector lệch góc 1e-3 rad (> sqrt(EPSILON)), rẽ nhánh chéo nhau với trực giao hoàn hảo."""
    # theta = 1e-3 rad => sin^2(theta) ≈ 1e-6 > EPSILON = 1e-9 -> rẽ nhánh chéo nhau
    A1 = Point3D("A1", 10.0, 0.0, 0.0)
    u1 = Vector3D(1.0, 0.0, 0.0)
    theta = 1e-3
    u2 = Vector3D(math.cos(theta), math.sin(theta), 0.0)
    A2 = Point3D("A2", 0.0, 0.0, 5.0)
    M1, M2, d = find_common_perpendicular(A1, u1, A2, u2)
    # Cấu hình chéo nhau này có khoảng cách thực d=5.000000 (trục Oz là đường vuông góc chung)
    assert abs(d - 5.0) < 1e-7
    # Kiểm tra tính trực giao của đoạn vuông góc chung M1M2 với v1 và v2 (sai số máy O(eps/denom) ~ 1e-9 < 1e-7)
    v1 = u1.normalize()
    v2 = u2.normalize()
    m_vec = M1.vector_to(M2)
    assert abs(m_vec.dot_product(v1)) < 1e-7
    assert abs(m_vec.dot_product(v2)) < 1e-7
    print(f"  [TV-3D-19] PASS: Góc lệch trên ngưỡng 1e-3 rad (rẽ nhánh chéo nhau, trực giao < 1e-7), d={d:.4f}.")


def test_tv_3d_20_circumscribed_sphere_negative_case():
    """TV-3D-20: Ca âm (negative test) - Khối đa diện không thể nội tiếp mặt cầu phải ném ValueError."""
    # Tạo hình chóp S.ABCD có đáy là hình thang vuông (không nội tiếp đường tròn do tổng 2 góc đối != 180)
    # A(0,0,0), B(4,0,0), C(3,3,0), D(0,3,0), S(0,0,4)
    # Tứ giác ABCD có: góc A = 90, B != 90, C != 90, D = 90 => góc B + D != 180 => không thể nội tiếp mặt cầu!
    non_inscribable_pyramid = {
        "vertices": {
            "S": Point3D("S", 0.0, 0.0, 4.0),
            "A": Point3D("A", 0.0, 0.0, 0.0),
            "B": Point3D("B", 4.0, 0.0, 0.0),
            "C": Point3D("C", 3.0, 3.0, 0.0),
            "D": Point3D("D", 0.0, 3.0, 0.0),
        },
        "edges": [
            ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
            ("S", "A"), ("S", "B"), ("S", "C"), ("S", "D"),
        ],
        "faces": [
            ["A", "B", "C", "D"],
            ["S", "A", "B"], ["S", "B", "C"], ["S", "C", "D"], ["S", "D", "A"]
        ]
    }
    try:
        circumscribed_sphere(non_inscribable_pyramid, strict=True)
        assert False, "Không ném ValueError khi khối đa diện không nội tiếp được mặt cầu!"
    except ValueError as e:
        assert "không thể nội tiếp mặt cầu" in str(e)
    print("  [TV-3D-20] PASS: Ca âm (Negative Test) phát hiện chính xác đa diện không thể nội tiếp mặt cầu (ném ValueError).")


def test_tv_3d_21_micro_scale_invariance():
    """TV-3D-21: Khối đa diện siêu nhỏ (Micro-scale L = 10^-3) kiểm chứng tính bất biến thang đo hai chiều (Dương & Âm)."""
    # 1. Chiều dương: Tứ diện vuông kích thước L = 1e-3
    L = 1e-3
    micro_tetra = {
        "vertices": {
            "A": Point3D("A", 0.0, 0.0, 0.0),
            "B": Point3D("B", L, 0.0, 0.0),
            "C": Point3D("C", 0.0, L, 0.0),
            "S": Point3D("S", 0.0, 0.0, L),
        },
        "edges": [
            ("A", "B"), ("A", "C"), ("A", "S"),
            ("B", "C"), ("C", "S"), ("S", "B"),
        ],
        "faces": [
            ["A", "B", "C"], ["A", "B", "S"], ["A", "C", "S"], ["B", "C", "S"],
        ]
    }
    # Thể tích giải tích: V = (1/6) * L^3 = (1/6) * 1e-9 ≈ 1.666667e-10
    vol = compute_polyhedron_volume(micro_tetra)
    expected_vol = (1.0 / 6.0) * (L ** 3)
    assert abs(vol - expected_vol) / expected_vol < 1e-9, f"Lệch thể tích micro tương đối: {vol} != {expected_vol}"

    # Mặt cầu ngoại tiếp dương: Tâm I(L/2, L/2, L/2), bán kính R = (sqrt(3)/2) * L ≈ 8.660254e-4
    sp = circumscribed_sphere(micro_tetra, strict=True)
    expected_R = (math.sqrt(3.0) / 2.0) * L
    rel_R_err = abs(sp.radius - expected_R) / expected_R
    assert rel_R_err < 1e-12, f"Lệch bán kính micro: {sp.radius} != {expected_R}"

    # 2. Chiều âm: Khối chóp 5 đỉnh ở thang micro L = 1e-3, đỉnh E bị lệch 5% bán kính
    # Đỉnh E bị lệch delta = 0.05 * R ≈ 4.33e-5 -> rel_err = 5e-2 > TOL_SPHERE (1e-4) -> phải ném ValueError!
    micro_distorted = {
        "vertices": {
            "A": Point3D("A", 0.0, 0.0, 0.0),
            "B": Point3D("B", L, 0.0, 0.0),
            "C": Point3D("C", 0.0, L, 0.0),
            "S": Point3D("S", 0.0, 0.0, L),
            "E": Point3D("E", L, L, 0.05 * L),  # Đỉnh thứ 5 lệch 5%
        },
        "edges": [
            ("A", "B"), ("B", "C"), ("C", "A"), ("A", "S"), ("B", "S"), ("C", "S"),
        ],
        "faces": [
            ["A", "B", "C"], ["A", "B", "S"], ["B", "C", "S"], ["C", "A", "S"]
        ]
    }
    try:
        circumscribed_sphere(micro_distorted, strict=True)
        assert False, "Không ném ValueError khi khối micro bị lệch không đồng cầu!"
    except ValueError as e:
        assert "không thể nội tiếp mặt cầu" in str(e)

    print(f"  [TV-3D-21] PASS: Khối siêu nhỏ L=1e-3: V={vol:.2e}, R={sp.radius:.6e} (sai số tương đối < 1e-12) & bắt ca âm 5% chính xác.")


def test_tv_3d_22_macro_scale_strict_rejection():
    """TV-3D-22: Khối vĩ mô (Macro-scale L = 10^3) kiểm chứng tính bất biến thang đo hai chiều (Dương & Âm)."""
    L = 1000.0
    # 1. Chiều dương: Khối hộp lập phương chuẩn L = 1000.0 (phải được chấp nhận)
    macro_valid = create_cuboid(L, L, L)
    sp_macro = circumscribed_sphere(macro_valid, strict=True)
    expected_R_macro = (math.sqrt(3.0) / 2.0) * L  # 500 * sqrt(3) ≈ 866.0254
    assert abs(sp_macro.radius - expected_R_macro) / expected_R_macro < 1e-12

    # 2. Chiều âm: Khối hộp L = 1000.0, một đỉnh C1 bị nhiễu lệch nhẹ Delta_z = 2.0
    # Sai số tương đối = 2.0 / 866.025 ≈ 2.31e-3 > TOL_SPHERE (1e-4) -> phải ném ValueError!
    macro_poly = {
        "vertices": {
            "A": Point3D("A", 0.0, 0.0, 0.0),
            "B": Point3D("B", L, 0.0, 0.0),
            "C": Point3D("C", L, L, 0.0),
            "D": Point3D("D", 0.0, L, 0.0),
            "A1": Point3D("A1", 0.0, 0.0, L),
            "B1": Point3D("B1", L, 0.0, L),
            "C1": Point3D("C1", L, L, L + 2.0),  # Đỉnh bị lệch nhẹ 2 đơn vị trên thang 1000
            "D1": Point3D("D1", 0.0, L, L),
        },
        "edges": [
            ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
            ("A1", "B1"), ("B1", "C1"), ("C1", "D1"), ("D1", "A1"),
            ("A", "A1"), ("B", "B1"), ("C", "C1"), ("D", "D1"),
        ],
        "faces": [
            ["A", "B", "C", "D"], ["A1", "B1", "C1", "D1"],
            ["A", "B", "B1", "A1"], ["B", "C", "C1", "B1"],
            ["C", "D", "D1", "C1"], ["D", "A", "A1", "D1"],
        ]
    }
    try:
        circumscribed_sphere(macro_poly, strict=True)
        assert False, "Không ném ValueError khi khối vĩ mô bị biến dạng không đồng cầu!"
    except ValueError as e:
        assert "không thể nội tiếp mặt cầu" in str(e)
    print("  [TV-3D-22] PASS: Khối vĩ mô L=1e3: Chiều dương R=866.0254 đạt chuẩn & Chiều âm lệch 2.0 bị strict mode từ chối chính xác.")


if __name__ == "__main__":
    print("=" * 75)
    print("CHẠY BỘ KIỂM TRA BẤT BIẾN HÌNH HỌC VÀ TRƯỜNG HỢP BIÊN (TV-3D-01 -> TV-3D-22)")
    print("=" * 75)
    test_tv_3d_01_euler_polyhedron_formula()
    test_tv_3d_02_degenerate_collinear_plane()
    test_tv_3d_03_angle_lines_boundary_clamping()
    test_tv_3d_04_angle_between_planes()
    test_tv_3d_05_angle_line_and_plane()
    test_tv_3d_06_distance_between_lines()
    test_tv_3d_07_common_perpendicular_skew_lines()
    test_tv_3d_08_cube_cross_section_and_area()
    test_tv_3d_09_pyramid_cross_section_homothety()
    test_tv_3d_10_segment_plane_intersection_endpoints()
    test_tv_3d_11_polyhedron_volume_exact_formulas()
    test_tv_3d_12_circumscribed_sphere_invariants()
    test_tv_3d_13_girard_spherical_excess_theorem()
    test_tv_3d_14_haversine_great_circle_invariants()
    test_tv_3d_15_constraint_solver_convergence()
    test_tv_3d_16_skew_orthogonal_lines()
    test_tv_3d_17_parallel_lines_common_perpendicular()
    test_tv_3d_18_nearly_parallel_under_threshold()
    test_tv_3d_19_nearly_parallel_above_threshold_skew()
    test_tv_3d_20_circumscribed_sphere_negative_case()
    test_tv_3d_21_micro_scale_invariance()
    test_tv_3d_22_macro_scale_strict_rejection()
    print("=" * 75)
    print("TẤT CẢ 22 TEST VECTORS ĐÃ VƯỢT QUA 100%!")
    print("=" * 75)
