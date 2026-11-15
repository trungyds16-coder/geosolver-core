# -*- coding: utf-8 -*-
"""
GeoSolver 2D Core Package
"""

from geosolver_core.provenance import (
    point_provenance_flag,
    _point_flag,
    snap_to_grid,
    _FREE_SOURCES,
    _EXACT_SOURCES,
    _DERIVED_SOURCES,
)
from geosolver_core.classifier import (
    classify_triangle,
    as_scaled_ints,
    _finite,
)

__all__ = [
    "point_provenance_flag",
    "_point_flag",
    "snap_to_grid",
    "_FREE_SOURCES",
    "_EXACT_SOURCES",
    "_DERIVED_SOURCES",
    "classify_triangle",
    "as_scaled_ints",
    "_finite",
]
