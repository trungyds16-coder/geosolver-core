# -*- coding: utf-8 -*-
"""
UNIT TEST SUITE FOR DEDUCTIVE GEOMETRY ENGINE
Kiểm thử bộ suy luận diễn dịch hình học thuần túy (Area Method & Full-Angle)
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from deductive_engine import (
    Fact, FactDatabase, DeductiveEngine, canonical_seg, canonical_pair_lines,
    solve_with_deductive_engine
)

def test_midline_and_parallel():
    print("--- [TEST 1]: Đường trung bình tam giác suy ra song song ---")
    points = [
        {"name": "A", "x": 0.0, "y": 4.0},
        {"name": "B", "x": -3.0, "y": 0.0},
        {"name": "C", "x": 5.0, "y": 0.0},
        {"name": "M", "x": -1.5, "y": 2.0},  # Trung điểm AB
        {"name": "N", "x": 2.5, "y": 2.0},   # Trung điểm AC
    ]
    segments = [
        {"p1": {"name": "A"}, "p2": {"name": "B"}},
        {"p1": {"name": "A"}, "p2": {"name": "C"}},
        {"p1": {"name": "B"}, "p2": {"name": "C"}},
        {"p1": {"name": "M"}, "p2": {"name": "N"}},
    ]
    lines = []
    circles = []

    proof_vi = solve_with_deductive_engine(points, segments, lines, circles, "parallel", "MN, BC", lang="vi")
    assert proof_vi is not None, "FAILED: Không tìm thấy chứng minh MN // BC bằng tiếng Việt!"
    print(proof_vi)

    proof_en = solve_with_deductive_engine(points, segments, lines, circles, "parallel", "MN, BC", lang="en")
    assert proof_en is not None, "FAILED: Không tìm thấy chứng minh MN // BC bằng tiếng Anh!"
    print(proof_en)
    print("✓ TEST 1 PASSED!\n")


def test_perpendicular_to_parallel():
    print("--- [TEST 2]: Từ vuông góc đến song song (L1 ⊥ L2 và L2 // L3 => L1 ⊥ L3) ---")
    points = [
        {"name": "A", "x": 0.0, "y": 4.0},
        {"name": "B", "x": -3.0, "y": 0.0},
        {"name": "C", "x": 5.0, "y": 0.0},
        {"name": "M", "x": -1.5, "y": 2.0},  # Trung điểm AB
        {"name": "N", "x": 2.5, "y": 2.0},   # Trung điểm AC
        {"name": "D", "x": 0.0, "y": 0.0},   # Chân đường cao từ A (AD ⊥ BC)
    ]
    segments = [
        {"p1": {"name": "A"}, "p2": {"name": "D"}},
        {"p1": {"name": "B"}, "p2": {"name": "C"}},
        {"p1": {"name": "M"}, "p2": {"name": "N"}},
    ]
    lines = []
    circles = []

    # AD ⊥ BC, mà MN // BC => AD ⊥ MN
    proof_vi = solve_with_deductive_engine(points, segments, lines, circles, "perp", "AD, MN", lang="vi")
    assert proof_vi is not None, "FAILED: Không tìm thấy chứng minh AD ⊥ MN!"
    print(proof_vi)
    print("✓ TEST 2 PASSED!\n")


def test_two_right_angles_cyclic():
    print("--- [TEST 3]: Tứ giác nội tiếp đường kính từ 2 góc vuông cùng nhìn 1 đoạn ---")
    # Tứ giác ABCD có góc BAD = 90° và góc BCD = 90° => nội tiếp đường tròn đường kính BD
    points = [
        {"name": "A", "x": 0.0, "y": 4.0},
        {"name": "B", "x": -4.0, "y": 0.0},
        {"name": "D", "x": 4.0, "y": 0.0},
        {"name": "C", "x": 0.0, "y": -4.0},
    ]
    segments = [
        {"p1": {"name": "B"}, "p2": {"name": "A"}},
        {"p1": {"name": "A"}, "p2": {"name": "D"}},
        {"p1": {"name": "B"}, "p2": {"name": "C"}},
        {"p1": {"name": "C"}, "p2": {"name": "D"}},
    ]
    lines = []
    circles = []

    proof_vi = solve_with_deductive_engine(points, segments, lines, circles, "concyclic", "A, B, C, D", lang="vi")
    assert proof_vi is not None, "FAILED: Không tìm thấy chứng minh ABCD nội tiếp!"
    print(proof_vi)
    print("✓ TEST 3 PASSED!\n")


def test_parallel_transitivity():
    print("--- [TEST 4]: Tính chất bắc cầu của quan hệ song song (L1 // L2 và L2 // L3 => L1 // L3) ---")
    points = [
        {"name": "A", "x": 0.0, "y": 2.0}, {"name": "B", "x": 4.0, "y": 2.0},
        {"name": "C", "x": 0.0, "y": 1.0}, {"name": "D", "x": 4.0, "y": 1.0},
        {"name": "E", "x": 0.0, "y": 0.0}, {"name": "F", "x": 4.0, "y": 0.0},
    ]
    segments = [
        {"p1": {"name": "A"}, "p2": {"name": "B"}},
        {"p1": {"name": "C"}, "p2": {"name": "D"}},
        {"p1": {"name": "E"}, "p2": {"name": "F"}},
    ]
    lines = []
    circles = []

    # AB // CD và CD // EF => AB // EF
    proof_vi = solve_with_deductive_engine(points, segments, lines, circles, "parallel", "AB, EF", lang="vi")
    assert proof_vi is not None, "FAILED: Không tìm thấy chứng minh AB // EF!"
    print(proof_vi)
    print("✓ TEST 4 PASSED!\n")


def test_euler_line_collinear():
    print("--- [TEST 5]: Đường thẳng Euler (Trực tâm H, Trọng tâm G, Tâm ngoại tiếp O thẳng hàng) ---")
    points = [
        {"name": "A", "x": 0.0, "y": 4.0},
        {"name": "B", "x": -3.0, "y": 0.0},
        {"name": "C", "x": 3.0, "y": 0.0},
        {"name": "G", "x": 0.0, "y": 4.0 / 3.0},       # Trọng tâm G (0; 1.333)
        {"name": "H", "x": 0.0, "y": 2.25},            # Trực tâm H (0; 2.25)
        {"name": "O", "x": 0.0, "y": 0.875},           # Tâm ngoại tiếp O (0; 0.875)
    ]
    segments = [
        {"p1": {"name": "A"}, "p2": {"name": "B"}},
        {"p1": {"name": "B"}, "p2": {"name": "C"}},
        {"p1": {"name": "C"}, "p2": {"name": "A"}},
    ]
    lines = []
    circles = []

    proof_vi = solve_with_deductive_engine(points, segments, lines, circles, "collinear", "H, G, O", lang="vi")
    assert proof_vi is not None, "FAILED: Không tìm thấy chứng minh đường thẳng Euler H, G, O thẳng hàng!"
    print(proof_vi)
    print("✓ TEST 5 PASSED!\n")


def test_ceva_medians_concurrency():
    print("--- [TEST 6]: Định lý Ceva cho 3 đường trung tuyến đồng quy ---")
    points = [
        {"name": "A", "x": 0.0, "y": 4.0},
        {"name": "B", "x": -3.0, "y": 0.0},
        {"name": "C", "x": 3.0, "y": 0.0},
        {"name": "D", "x": 0.0, "y": 0.0},             # Trung điểm BC
        {"name": "E", "x": 1.5, "y": 2.0},             # Trung điểm AC
        {"name": "F", "x": -1.5, "y": 2.0},            # Trung điểm AB
    ]
    segments = [
        {"p1": {"name": "A"}, "p2": {"name": "B"}},
        {"p1": {"name": "B"}, "p2": {"name": "C"}},
        {"p1": {"name": "C"}, "p2": {"name": "A"}},
        {"p1": {"name": "A"}, "p2": {"name": "D"}},
        {"p1": {"name": "B"}, "p2": {"name": "E"}},
        {"p1": {"name": "C"}, "p2": {"name": "F"}},
    ]
    lines = []
    circles = []

    proof_vi = solve_with_deductive_engine(points, segments, lines, circles, "concurrent", "AD, BE, CF", lang="vi")
    assert proof_vi is not None, "FAILED: Không tìm thấy chứng minh 3 đường trung tuyến đồng quy theo Ceva!"
    print(proof_vi)
    print("✓ TEST 6 PASSED!\n")


def test_area_method_parallel_triangles():
    print("--- [TEST 7]: Phương pháp diện tích (Chou's Area Method) cho tam giác cùng đáy giữa 2 đường song song ---")
    points = [
        {"name": "A", "x": 0.0, "y": 2.0}, {"name": "B", "x": 4.0, "y": 2.0},
        {"name": "C", "x": 1.0, "y": 0.0}, {"name": "D", "x": 5.0, "y": 0.0},
    ]
    segments = [
        {"p1": {"name": "A"}, "p2": {"name": "B"}},
        {"p1": {"name": "C"}, "p2": {"name": "D"}},
    ]
    lines = []
    circles = []

    # AB // CD => S(ABC) = S(ABD)
    db = FactDatabase()
    engine = DeductiveEngine(db)
    engine.load_from_cad(points, segments, lines, circles)
    engine.run_deduction()
    areas = engine.db.by_pred.get("equal_area", [])
    assert len(areas) > 0, "FAILED: Không tìm thấy đẳng thức diện tích bằng phương pháp Chou's Area Method!"
    proof = engine._build_proof_text(areas[0], lang="vi")
    print(proof)
    print("✓ TEST 7 PASSED!\n")


if __name__ == "__main__":
    print("=================================================================")
    print("  CHẠY BỘ KIỂM THỬ TỰ ĐỘNG CHO DEDUCTIVE GEOMETRY ENGINE")
    print("=================================================================\n")
    test_midline_and_parallel()
    test_perpendicular_to_parallel()
    test_two_right_angles_cyclic()
    test_parallel_transitivity()
    test_euler_line_collinear()
    test_ceva_medians_concurrency()
    test_area_method_parallel_triangles()
    print("=================================================================")
    print("  🎉 TẤT CẢ CÁC BÀI KIỂM THỬ ĐÃ VƯỢT QUA 100%!")
    print("=================================================================")
