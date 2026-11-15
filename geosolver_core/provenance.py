# -*- coding: utf-8 -*-
"""
GeoSolver 2D Core - Dynamic Taint Tracking & Geometric Provenance Engine
License: GNU General Public License v3 (GPLv3)
"""

from __future__ import annotations
import math
from typing import Dict, Any, Optional, Set, Tuple, List, Union

_FREE_SOURCES: Tuple[str, ...] = ("free", "mouse", "dragged")
_EXACT_SOURCES: Tuple[str, ...] = ("typed", "grid_snap", "snapped", "exact")
_DERIVED_SOURCES: Tuple[str, ...] = (
    "midpoint", "intersection", "formula",
    "proj_foot", "translate_vec", "orthocenter", "incenter"
)


def point_provenance_flag(
    p: Any,
    _visiting: Optional[Set[int]] = None,
    memo: Optional[Dict[int, Optional[bool]]] = None,
    _depth: int = 0
) -> Optional[bool]:
    """
    Evaluates exactness flag through the construction Directed Acyclic Graph (DAG):
      - True:  Exact input (typed, grid-snapped, or derived solely from exact parents).
      - False: Freehand tainted input, mouse drag, or cyclic ancestry violation.
      - None:  Unknown/unspecified provenance.

    Guarantees:
      1. Taint Conservation Law: If any parent in the derivation tree is tainted,
         the derived point is unconditionally tainted (False). Stored flags on
         derived points are not trusted over dynamic parent state.
      2. Cycle Safety: Detects self-referential or cyclic ancestry via `_visiting`
         set and terminates safely with False.
      3. Order Independence: Traversal is strictly order-invariant across parent permutations.
      4. Complexity: Amortized O(V+E) memoized DAG traversal.
    """
    if not isinstance(p, dict):
        return None

    if memo is None:
        memo = {}

    obj_id = id(p)
    if obj_id in memo:
        return memo[obj_id]

    if _visiting is None:
        _visiting = set()

    if obj_id in _visiting:
        # Cyclic reference detected in construction ancestry graph
        return False

    # 1. Explicit freehand or tainted status
    if p.get("source") in _FREE_SOURCES or p.get("exact") is False:
        memo[obj_id] = False
        return False

    # 2. Derived point DAG propagation (evaluated before trusting any stored exact flag)
    parents = p.get("parents") or p.get("dependencies")
    if parents or p.get("source") in _DERIVED_SOURCES:
        if not parents:
            memo[obj_id] = False
            return False
        _visiting.add(obj_id)
        try:
            flags = [point_provenance_flag(q, _visiting, memo, _depth + 1) for q in parents]
            if any(f is False for f in flags):
                res = False
            elif all(f is True for f in flags):
                res = True
            else:
                res = None
            memo[obj_id] = res
            return res
        finally:
            _visiting.discard(obj_id)

    # 3. Explicit exact status or typed source
    if p.get("exact") is True or p.get("source") in _EXACT_SOURCES:
        memo[obj_id] = True
        return True

    memo[obj_id] = None
    return None


# Backward-compatible alias for existing test suites
_point_flag = point_provenance_flag


def snap_to_grid(x: float, y: float, grid_step: float = 1.0) -> Tuple[Union[int, float], Union[int, float], str, bool]:
    """
    Snaps continuous coordinates to the nearest multiple of grid_step.
    Restores exact integer/rational status under the Taint Conservation Law:
    When snapped coordinates fall on integer grid points, returns Python integers.
    Returns (snapped_x, snapped_y, source='grid_snap', exact=True).
    """
    if grid_step <= 0:
        raise ValueError(f"grid_step must be positive, got {grid_step}")
    sx = round(x / grid_step) * grid_step
    sy = round(y / grid_step) * grid_step
    # Return integer type if mathematically integral
    ix = int(round(sx)) if abs(sx - round(sx)) < 1e-9 else sx
    iy = int(round(sy)) if abs(sy - round(sy)) < 1e-9 else sy
    return (0 if ix == 0 else ix, 0 if iy == 0 else iy, "grid_snap", True)
