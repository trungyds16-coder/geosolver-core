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
      2. Cycle Safety: Detects self-referential or cyclic ancestry via active `visiting`
         set and terminates safely with False.
      3. Stack Safety: Evaluated via an explicit stack (iterative topological DFS),
         guaranteeing zero RecursionError regardless of DAG depth (tested up to 2,000+).
      4. Order Independence: Traversal is strictly order-invariant across parent permutations.
      5. Complexity: Strictly O(V + E) linear traversal via `done` set and `memo`,
         guaranteeing zero re-expansion on shared ancestors (e.g. diamond ladders).
    """
    if not isinstance(p, dict):
        return None

    if memo is None:
        memo = {}

    root_id = id(p)
    if root_id in memo:
        return memo[root_id]

    stack: List[dict] = [p]
    visiting: Set[int] = set()
    done: Set[int] = set()
    post_order: List[dict] = []

    # Phase 1: Iterative topological traversal with cycle detection & diamond memoization
    while stack:
        node = stack[-1]
        node_id = id(node)

        if node_id in memo or node_id in done:
            stack.pop()
            continue

        if node_id in visiting:
            visiting.discard(node_id)
            done.add(node_id)
            stack.pop()
            post_order.append(node)
            continue

        visiting.add(node_id)

        # 1. Tainted / dragged status unconditionally yields False
        if node.get("source") in _FREE_SOURCES or node.get("exact") is False:
            memo[node_id] = False
            done.add(node_id)
            visiting.discard(node_id)
            stack.pop()
            continue

        parents = node.get("parents") or node.get("dependencies")
        if parents or node.get("source") in _DERIVED_SOURCES:
            if not parents:
                memo[node_id] = False
                done.add(node_id)
                visiting.discard(node_id)
                stack.pop()
                continue
            has_cycle = False
            for parent in parents:
                if not isinstance(parent, dict):
                    continue
                p_id = id(parent)
                if p_id in visiting:
                    has_cycle = True
                elif p_id not in memo and p_id not in done:
                    stack.append(parent)
            if has_cycle:
                memo[node_id] = False
                done.add(node_id)
                visiting.discard(node_id)
                stack.pop()
        else:
            # Base leaf point
            if node.get("exact") is True or node.get("source") in _EXACT_SOURCES:
                memo[node_id] = True
            else:
                memo[node_id] = None
            done.add(node_id)
            visiting.discard(node_id)
            stack.pop()

    # Phase 2: Post-order bottom-up evaluation
    for node in post_order:
        node_id = id(node)
        if node_id in memo:
            continue
        parents = node.get("parents") or node.get("dependencies")
        if parents:
            flags = [memo.get(id(q)) for q in parents if isinstance(q, dict)]
            if any(f is False for f in flags):
                memo[node_id] = False
            elif all(f is True for f in flags):
                memo[node_id] = True
            else:
                memo[node_id] = None
        else:
            if node.get("exact") is True or node.get("source") in _EXACT_SOURCES:
                memo[node_id] = True
            else:
                memo[node_id] = None

    return memo.get(root_id)


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
