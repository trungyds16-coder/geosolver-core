# -*- coding: utf-8 -*-
"""
GeoSolver 3D - Phân hệ Trực quan hóa & Giải toán Hình học Không gian Sư phạm
"""
from .geometry3d_kernel import (
    Point3D,
    Vector3D,
    Plane3D,
    Sphere3D,
    create_pyramid_sabcd,
    create_tetrahedron_sabc,
    create_prism_abc_a1b1c1,
    create_cuboid,
    create_truncated_pyramid,
    create_octahedron,
    distance_point_to_plane,
    distance_between_skew_lines,
    angle_between_planes,
    angle_line_and_plane,
    intersect_plane_with_polyhedron,
    compute_polygon_area_and_perimeter,
    compute_polyhedron_volume,
)
from .deductive3d_engine import (
    Deductive3DEngine,
    DeductiveProofResult,
    ProofStep,
)

__all__ = [
    "Point3D",
    "Vector3D",
    "Plane3D",
    "Sphere3D",
    "create_pyramid_sabcd",
    "create_tetrahedron_sabc",
    "create_prism_abc_a1b1c1",
    "create_cuboid",
    "create_truncated_pyramid",
    "create_octahedron",
    "distance_point_to_plane",
    "distance_between_skew_lines",
    "angle_between_planes",
    "angle_line_and_plane",
    "intersect_plane_with_polyhedron",
    "compute_polygon_area_and_perimeter",
    "compute_polyhedron_volume",
    "Deductive3DEngine",
    "DeductiveProofResult",
    "ProofStep",
]
