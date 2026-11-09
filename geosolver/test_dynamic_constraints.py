import math
from geosolver_desktop import GeoSolverApp

def test_dynamic_constraints():
    # Instantiate app mock
    app = GeoSolverApp.__new__(GeoSolverApp)
    app.points = []
    app.segments = []
    app.lines = []
    app.circles = []

    # 1. Test Midpoint constraint
    A = {'id': 'A', 'name': 'A', 'x': 0.0, 'y': 0.0}
    B = {'id': 'B', 'name': 'B', 'x': 4.0, 'y': 0.0}
    M = {'id': 'M', 'name': 'M', 'x': 2.0, 'y': 0.0, 'constraint': {'type': 'midpoint', 'p1': A, 'p2': B}}
    app.points.extend([A, B, M])

    B['x'], B['y'] = 6.0, 4.0
    app._recompute_dependent_objects(exclude_points=[B])
    assert abs(M['x'] - 3.0) < 1e-6 and abs(M['y'] - 2.0) < 1e-6, f"Midpoint error: {M}"
    print("✓ Test 1: Midpoint constraint propagation: PASSED!")

    # 2. Test Circumcenter & Circumcircle constraint
    P1 = {'id': 'P1', 'x': 0.0, 'y': 0.0}
    P2 = {'id': 'P2', 'x': 4.0, 'y': 0.0}
    P3 = {'id': 'P3', 'x': 0.0, 'y': 3.0}
    O = {'id': 'O', 'x': 2.0, 'y': 1.5, 'constraint': {'type': 'circumcenter', 'pts': [P1, P2, P3]}}
    C = {'id': 'C_out', 'center': O, 'r': 2.5, 'constraint': {'type': 'circumcircle', 'pts': [P1, P2, P3], 'center': O}}
    app.points.extend([P1, P2, P3, O])
    app.circles.append(C)

    P2['x'] = 6.0
    app._recompute_dependent_objects(exclude_points=[P2])
    assert abs(O['x'] - 3.0) < 1e-5 and abs(O['y'] - 1.5) < 1e-5, f"Circumcenter error: {O}"
    assert abs(C['r'] - math.hypot(3.0, 1.5)) < 1e-5, f"Circumcircle error: {C}"
    print("✓ Test 2: Circumcenter & Circumcircle auto-update: PASSED!")

    # 3. Test Point on segment sliding constraint
    S_pt = {'id': 'S', 'x': 3.0, 'y': 2.0, 'constraint': {'type': 'on_segment', 'p1': A, 'p2': B, 't': 0.5}}
    app.points.append(S_pt)
    A['x'] = 2.0
    app._recompute_dependent_objects(exclude_points=[A])
    assert abs(S_pt['x'] - 4.0) < 1e-5 and abs(S_pt['y'] - 2.0) < 1e-5, f"On segment error: {S_pt}"
    print("✓ Test 3: Point on segment constraint: PASSED!")

    # 4. Test Incenter & Incircle constraint
    T1 = {'id': 'T1', 'x': 0.0, 'y': 0.0}
    T2 = {'id': 'T2', 'x': 4.0, 'y': 0.0}
    T3 = {'id': 'T3', 'x': 0.0, 'y': 3.0}
    I_pt = {'id': 'I', 'x': 1.0, 'y': 1.0, 'constraint': {'type': 'incenter', 'pts': [T1, T2, T3]}}
    C_in = {'id': 'C_in', 'center': I_pt, 'r': 1.0, 'constraint': {'type': 'incircle', 'pts': [T1, T2, T3], 'center': I_pt}}
    app.points.extend([T1, T2, T3, I_pt])
    app.circles.append(C_in)

    T2['x'] = 8.0 # Changes triangle shape
    app._recompute_dependent_objects(exclude_points=[T2])
    # For (0,0), (8,0), (0,3): a=sqrt(64+9)=sqrt(73), b=3, c=8, peri=11+sqrt(73), area=12
    # r = area / (peri/2) = 24 / (11 + sqrt(73))
    expected_r = 24.0 / (11.0 + math.sqrt(73.0))
    assert abs(C_in['r'] - expected_r) < 1e-4, f"Incircle error: {C_in['r']} != {expected_r}"
    print("✓ Test 4: Incenter & Incircle dynamic propagation: PASSED!")

    # 5. Test Cascade Multi-level Dependency (A -> Midpoint M -> Projection H -> Circle)
    # A(2,0), B(6,4) -> M(4,2)
    # H is proj of P3(0,3) on line OM
    P_foot = {'id': 'H', 'x': 0.0, 'y': 0.0, 'constraint': {'type': 'proj_foot', 'p': P3, 'line_p1': A, 'line_p2': M}}
    app.points.append(P_foot)
    app._recompute_dependent_objects()
    # Line AM: A(2,0) to M(4,2), direction (2,2) ~ (1,1). Projection of (0,3):
    # dx=2, dy=2, L2=8. t = ((0-2)*2 + (3-0)*2)/8 = (-4+6)/8 = 2/8 = 0.25
    # Hx = 2 + 0.25*2 = 2.5, Hy = 0 + 0.25*2 = 0.5
    assert abs(P_foot['x'] - 2.5) < 1e-5 and abs(P_foot['y'] - 0.5) < 1e-5, f"Cascade proj failed: {P_foot}"
    print("✓ Test 5: Multi-level cascade dependency propagation: PASSED!")

    print("\n🎉 ALL 5 DYNAMIC GEOMETRY PROPAGATION TESTS PASSED 100%!")

if __name__ == "__main__":
    test_dynamic_constraints()
