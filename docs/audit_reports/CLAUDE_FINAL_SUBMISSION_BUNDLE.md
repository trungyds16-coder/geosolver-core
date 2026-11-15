# COMPLETE SUBMISSION BUNDLE: GEOSOLVER 2D
## TARGET: ELSEVIER SOFTWARX — FINAL REVISION (VERIFICATION OF LINEAR TRAVERSAL, DECOUPLED STRESS TESTS & FROZEN RELEASE)
### TAGGED RELEASE: `v3.2.0` | PYTHON 3.14.5 (WIN32)

---

## PART 1: POINT-BY-POINT REBUTTAL TO DESIGN AUDIT REPORT

**Dear Senior Reviewer,**

Thank you for your thorough verification and for confirming that the earlier blocking arithmetic defect (decimal lattice floating-point drift) and the sensitivity benchmark reproduce identically. We are deeply grateful for your sharp algorithmic detection regarding the $O(V+E)$ traversal complexity on diamond ladders and your suggestions on negative family decoupling.

We have addressed every remaining issue, itemized below:

---

### 1. Item 1: Release Versioning, Tag Freezing & Immutability (`v3.2.0`)
- **Reviewer Comment:** *"Across the session log, the prior bundle and your message, v3.1.0 has pointed to at least five different commits... A published tag must never move. A Zenodo archive taken at an earlier release event will not match the code in the paper. Fix: cut a fresh tag (v3.2.0, say), freeze it, create the Zenodo release from it, and put that version in the metadata table."*
- **Author Action:**
  - We have cut and frozen a brand new release tag: **`v3.2.0`**.
  - No further code modifications will touch `v3.2.0`.
  - The metadata table, CI scripts, and submission dossiers are permanently aligned to release tag **`v3.2.0`**.

---

### 2. Item 2: Strict $O(V+E)$ Linear Traversal via `done` Set on Diamond Ladders
- **Reviewer Comment:** *"Phase 1 only marks nodes as memoized in Phase 2, so any node reachable by two paths is re-expanded. On a ladder of shared ancestors, runtime grows about 2.5x per level: 0.12 s at depth 16, 0.45 s at 18, 2.9 s at 20... Fix: keep a done set, add each node to it when it goes into post_order, and skip nodes in done or memo both when popping and when pushing parents. Then add a test on a 25-level diamond ladder."*
- **Author Action:**
  - In `geosolver_core/provenance.py`, we implemented a `done: Set[int] = set()` alongside `visiting` and `memo`.
  - Nodes popped into `post_order` (or terminated early as leaf/tainted/cyclic) are immediately marked in `done`.
  - Nodes in `done` or `memo` are skipped both when pushing parents (`elif p_id not in memo and p_id not in done: stack.append(parent)`) and when popping from `stack` (`if node_id in memo or node_id in done: stack.pop(); continue`).
  - **Empirical Timing Comparison on Diamond Ladder:**
    - Depth 16: dropped from $0.1747\text{s}$ to **$0.000128\text{s}$** (>1,300x speedup).
    - Depth 20: dropped from $2.9\text{s}$ to **$0.000135\text{s}$** (>21,000x speedup).
    - Depth 25: dropped from projected $>5\text{ minutes}$ to **$0.000161\text{s}$**.
    - Even depth 100 ladder completes in **$0.000887\text{s}$**.
  - Added regression test `test_diamond_ladder_linear_complexity_depth_25` in `tests/test_geosolver_core.py`, verifying depth-25 exact, tainted, and cyclic diamond configurations execute in $<0.05\text{s}$.

---

### 3. Item 3: Decoupled Reporting of Hard Negatives & Removal of "Direct Empirical Justification"
- **Reviewer Comment:** *"The near-isosceles generator draws mismatches from 0.8% to 1.5%, exactly the band where tolerances of 0.008 to 0.015 start firing. The 0.006 default therefore looks optimal by construction. The 100 near-right negatives can never produce a false positive. The right-angle test uses a fixed |cos| <= 0.015... Fix: drop the phrase 'direct empirical justification'. Report the two families separately and state that the result reflects the chosen mismatch band."*
- **Author Action:**
  - Dropped the phrase "direct empirical justification" from the manuscript and docstrings.
  - In `scripts/sensitivity_benchmark.py` and manuscript §4.1, we decoupled the output table to report the two families separately:
    ```
    tol_rel | Near-Iso FP (N=100) | Near-Right FP (N=100) | Total Scalene TN | Total FP (N=200) | Combined FP (%)
    --------|---------------------|-----------------------|------------------|------------------|----------------
      0.002 |               0/100 |                 0/100 |          200/200 |            0/200 |           0.0%
      0.004 |               0/100 |                 0/100 |          200/200 |            0/200 |           0.0%
      0.006 |               0/100 |                 0/100 |          200/200 |            0/200 |           0.0%
      0.008 |               1/100 |                 0/100 |          199/200 |            1/200 |           0.5%
      0.010 |              36/100 |                 0/100 |          164/200 |           36/200 |          18.0%
    ```
  - We explicitly state in the paper that:
    1. False positives in the near-isosceles family emerge only when $\text{tol\_rel} \ge 0.008$ because the synthetic generator sampled mismatches specifically within $[0.8\%, 1.5\%]$.
    2. The 100 near-right scalene triangles produce 0/100 FP across all $\text{tol\_rel}$ because right angles are governed by a decoupled fixed angular bound ($|\cos \theta| \le 0.015$, corresponding to $[89.14^\circ, 90.86^\circ]$).

---

### 4. Item 4: Repository Accessibility & Zenodo DOI Confirmation
- **Reviewer Comment:** *"SoftwareX needs a publicly resolvable repository and a persistent identifier at submission. Please open both in a private browser window and confirm."*
- **Author Action:**
  - We explicitly confirm that the repository (`https://github.com/geosolver-lab/geosolver-core`) was maintained locally and in private staging during blinded review, and will be set to **Public** prior to formal editorial upload.
  - The Zenodo record (`10.5281/zenodo.14889201`) will be minted and published directly from the immutable frozen release tag **`v3.2.0`**.

---

### 5. Minor Edits Resolved
1. **Test Timing Reconciled (§4.2):**
   - Clarified that when running the unified discovery runner (`python -m unittest discover tests`), the combined 62-test execution took **17.060s** (which accounts for process startup, Tkinter canvas lifecycle, and discovery overhead).
   - In isolation, the headless CI suite executes in **0.019s** (27 tests), and the desktop integration suite executes in **10.826s** (35 tests).
2. **Theorem 1 Continuous-Regime Claim (Winner Uniqueness):**
   - Reformulated Theorem 1 (§2.3) with mathematical precision: Two non-winning candidates can tie on the candidate key if and only if their opposite sides are bitwise equal; however, the winning apex candidate is strictly unique because the third vertex then has leg mismatch $\Delta = 0$ and strictly wins the candidate sort.
3. **Abstract Clarification:**
   - Replaced vague "zero regression" with: *"the engine demonstrates bitwise permutation invariance, strict apex equivariance, and bounded linear $O(V+E)$ traversal on cycle-free construction graphs."*

---

## PART 2: THE FINAL REVISED MANUSCRIPT

# GeoSolver 2D: A Provenance-Aware Dynamic Geometry Engine with Dual-Regime and Permutation-Invariant Classification

**Author:** Bao-Trung Nguyen$^1$  
**Affiliation:** $^1$Independent Researcher, Ho Chi Minh City, Vietnam  
**Corresponding Author Email:** `trungyds16@gmail.com`  
**Target Journal:** *SoftwareX* (Elsevier) — Original Software Publication (OSP)  

---

### Abstract
Interactive Dynamic Geometry Systems (DGS) are prone to geometric misclassifications when users construct or perturb configurations using freehand gestures. Floating-point rounding errors and non-transitive relative tolerances frequently lead to false-positive recognitions (such as misclassifying near-regular integer-lattice triangles as equilateral) or permutation-dependent outcomes (where the classified type depends on vertex enumeration order). We introduce **GeoSolver 2D**, an open-source, highly reliable geometry engine designed to eliminate these numerical artifacts. GeoSolver 2D implements: (1) a *Dynamic Taint Tracking Engine* that enforces an acyclic dependency graph across interactive constructions using an iterative topological traversal with explicit stack safety and strictly linear $O(V+E)$ complexity; (2) a dual-regime validation model distinguishing between exact integer-lattice coordinates ($\mathbb{Z}^2$) and continuous approximations; and (3) a *Specificity-Ordered Classifier* operating on scale-normalized edge lengths and cosine predicates, which guarantees bitwise vertex-permutation invariance for type classification and equivariance for apex labeling. Scale-invariance holds unconditionally within the continuous regime, with explicit provenance tagging preventing artificial scale-induced transitions. Evaluated across an automated verification suite of 62 regression tests (27 headless core library tests and 35 desktop integration tests) and an empirical benchmark suite achieving 91.4% accuracy on canonical prototypes, the engine demonstrates bitwise permutation invariance, strict apex equivariance, and bounded linear $O(V+E)$ traversal on cycle-free construction graphs. The core computation engine is released as open-source software under the GNU General Public License v3 (GPLv3).

**Keywords:** Dynamic Geometry System, Taint Tracking, Permutation Invariance, Integer Lattice, Geometric Classification, Software Verification.

---

### Metadata Table

| Current code version | v3.2.0 |
| :--- | :--- |
| **Permanent code repository** | `https://github.com/geosolver-lab/geosolver-core` |
| **Legal Code License** | GNU General Public License v3 (GPLv3) |
| **Code versioning system used** | Git (Release tag: `v3.2.0`) |
| **Software code languages** | Python 3.10+ |
| **Compilation requirements** | None (Pure Python standard library) |
| **Supported operating systems** | Windows 10/11, Linux (Ubuntu 22.04+), macOS; CI tested via GitHub Actions |
| **Automated test suite** | Python `unittest` (27 headless CI tests, 35 GUI integration tests, 100% PASS) |
| **Persistent identifier (DOI)** | `10.5281/zenodo.14889201` |
| **Documentation & Support** | `https://github.com/geosolver-lab/geosolver-core/wiki` |

---

### 1. Motivation and Significance

#### 1.1. Background and Problem Statement
Dynamic Geometry Systems (DGS) are foundational tools in computer-assisted mathematics education, automated theorem proving, and computer-aided design (CAD). However, interactive geometry environments operate under a fundamental tension: **the gap between continuous user gestures (such as freehand mouse perturbations) and exact discrete mathematical truth**.

When users manipulate points on an interactive canvas, coordinate values undergo floating-point perturbations ($x \in \mathbb{R}$). Conventional DGS implementations attempt to identify geometric configurations (such as right, isosceles, or equilateral triangles) by evaluating heuristic tolerance thresholds ($\varepsilon$). In practice, this design introduces two major failure modes:
1. **Misclassification on Integer Lattices ($\mathbb{Z}^2$):** By the classical Shoelace Formula (Gauss Area Formula), any triangle whose vertices lie on the integer lattice $\mathbb{Z}^2$ has a strictly rational area:
   $$\text{Area} = \frac{1}{2} |X_A(Y_B - Y_C) + X_B(Y_C - Y_A) + X_C(Y_A - Y_B)| \in \frac{1}{2}\mathbb{Z} \subset \mathbb{Q}$$
   Conversely, an equilateral triangle with side length $a$ requires an area of $\text{Area} = \frac{\sqrt{3}}{4}a^2$. Because the squared distance between any two integer vertices is an integer ($a^2 = d_{\mathbb{Z}}^2 \in \mathbb{Z}$), the area of a lattice equilateral triangle would be strictly irrational due to $\sqrt{3} \notin \mathbb{Q}$. Since an irrational number cannot equal a rational number, **the equilateral hypothesis is provably unreachable on $\mathbb{Z}^2$**. Heuristic DGS engines that blindly apply continuous relative tolerances to lattice points frequently misclassify near-equilateral grid triangles as strictly equilateral, presenting false mathematical information to students.
2. **Permutation Dependence from Non-Transitive Tolerances:** In metric spaces over the real numbers, relative tolerance relations $|a - b| \le \varepsilon$ do not satisfy transitivity:
   $$|a - b| \le \varepsilon \land |b - c| \le \varepsilon \not\implies |a - c| \le \varepsilon$$
   In floating-point arithmetic compliant with IEEE-754 [4], when an interactive engine evaluates candidate hypotheses through sequential conditional logic (`if/elif`), the resulting classification depends on the arbitrary indexing order of the vertices ($\sigma(A, B, C)$ vs $\sigma(B, C, A)$).

#### 1.2. Related Work & Positioning
In computational geometry, the standard defense against numerical instability is **Exact Geometric Computation (EGC)**, exemplified by Shewchuk's adaptive-precision floating-point predicates [1] and the CGAL geometric kernel [2]. EGC solves orientation and incircle tests robustly, but requires rigorous floating-point filtering with multi-precision fallback.

To preserve computational simplicity while eliminating classification artifacts, GeoSolver 2D adapts concepts from dynamic taint analysis [3] into geometric provenance tracking. By classifying objects based on their operational history rather than floating-point coordinates alone, GeoSolver 2D bridges the gap between interactive usability and formal mathematical truth.

---

### 2. Software Architecture and Mathematical Formulation

GeoSolver 2D partitions geometric processing into three decoupled layers:
```
[User Interaction: Freehand Drag / Snap / Typed Input]
                       │
                       ▼
    [Dynamic Taint Engine & DAG Provenance (provenance.py)]
      - Cycle detection via active visiting set
      - Strict linear O(V+E) topological DFS via done set memoization
      - Taint Conservation: (p1_exact ∧ p2_exact) ∧ ¬is_tainted
                       │
                       ▼
  [Dual-Regime Coordinate Partitioning (as_scaled_ints)]
      - Discrete Lattice: Z^2 (Integer Predicates & Area Theorem)
      - Continuous Regime: Scale-Normalized Edge & Cosine Predicates
                       │
                       ▼
     [Specificity-Ordered Invariant Classifier (classifier.py)]
      Equilateral ≻ Right-Isosceles ≻ {Right, Isosceles} ≻ Scalene
      - Label-Free Candidate Key: (diff_leg, opposite_side_sq)
      - Bitwise Permutation Invariance & Equivariant Apex Labeling
```

#### 2.1. Dynamic Taint Tracking Engine
Every geometric entity $E$ maintains a provenance flag:
$$\text{exact}(E) = (\bigwedge_{P \in \text{Parents}(E)} \text{exact}(P)) \land \neg \text{is\_tainted}(E)$$
- **Taint Conservation Law:** Freehand canvas gestures unconditionally inject taint (`exact=False`), which strictly propagates to all descendant constructions (midpoints, intersections, perpendicular feet). Snapping to the coordinate grid (`snap_to_grid`) restores exact integer status (`exact=True`, `source='grid_snap'`). Stored flags on derived entities are never trusted over dynamic parent state.
- **DAG Cycle Safety & Stack Safety:** Traversal is protected against cyclic dependencies via an active `visiting` tracking set. Traversal is evaluated iteratively via an explicit stack (topological post-order DFS), eliminating recursion depth limits and guaranteeing strict traversal-order invariance across subtrees.
- **Strict $O(V+E)$ Linear Complexity:** Traversal maintains a `done` set of completed nodes alongside the active `visiting` set and results cache `memo`. Nodes already present in `done` or `memo` are skipped during parent expansion and popping, guaranteeing zero re-expansion over shared ancestors (e.g. diamond ladders, iterated midpoints).

#### 2.2. Dual-Regime Coordinate Model & `as_scaled_ints`
Input coordinates are evaluated via `as_scaled_ints` across scale factors $10^k$ ($k \in \{0, 1, 2, 3, 4\}$):
- If all coordinates satisfy $|v \cdot 10^k - \text{round}(v \cdot 10^k)| < 10^{-5}$, they are converted to scaled integers $[\text{round}(v \cdot 10^k)]$ and evaluated under exact integer arithmetic on $\mathbb{Z}^2$.
- Untagged coordinate tuples default to exact if they align with the scale grid. Coordinates with freehand provenance unconditionally bypass integer scaling and are quarantined into the continuous floating-point regime until explicitly snapped to grid.
- **Dual-Regime Scale Transitions:** For untagged inputs, uniform coordinate scaling can transition shapes across regime boundaries: $P(0,0), Q(1,0), R(0.51, 0.86598)$ has 5 decimal places and evaluates in the continuous regime as isosceles (`exact=False`). Magnified by $\times 10$, $R'(5.1, 8.6598)$ has 4 decimal places, which aligns with the $k=4$ discrete scale grid and is evaluated over $\mathbb{Z}^2$ as a distinct scalene configuration (`exact=True`). In contrast, when vertices carry freehand provenance tags (`exact=False`), the Taint Conservation Law quarantines them into the continuous regime until explicitly snapped to grid, preserving classification invariance across arbitrary magnifications.

#### 2.3. Specificity Hierarchy and Invariance Theorem
To prevent hypothesis suppression (where less constrained hypotheses like Isosceles trivially absorb more constrained hypotheses like Equilateral), GeoSolver 2D evaluates hypotheses through a strict specificity hierarchy:
$$\text{Equilateral} \succ \text{Right-Isosceles} \succ \{\text{Isosceles}, \text{Right}\} \succ \text{Scalene}$$
Right angles are evaluated via the scale-correct cosine predicate:
$$|\cos \theta| = \left| \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} \right| \le 0.015 \quad (\approx |\theta - 90^\circ| \le 0.86^\circ)$$

**Theorem 1 (Vertex-Permutation Invariance & Apex Equivariance):**  
Let $V = (v_1, v_2, v_3)$ be a triangle with edge lengths $l_{12}, l_{23}, l_{31}$. For each vertex $v \in V$, define its local geometric record $R(v) = (\Delta(v), d^2_{\text{opp}}(v))$ where $\Delta(v)$ is the relative mismatch between the two sides incident to $v$, and $d^2_{\text{opp}}(v)$ is the squared length of the opposite side. Because IEEE-754 subtraction and multiplication satisfy $\text{fl}(a - b)^2 = \text{fl}(b - a)^2$ under round-to-nearest mode, each side length is bitwise symmetric. For any permutation $\sigma \in S_3$, the set of records $\{R(v) \mid v \in V\}$ is mapped bijectively to $\{R(\sigma(v))\}$. Because candidate hypotheses are sorted over the label-free key $(\Delta, d^2_{\text{opp}})$, the classified triangle type is strictly invariant under $\sigma$, and the apex selection satisfies $\text{Apex}(\sigma(V)) \equiv \sigma(\text{Apex}(V))$. In the discrete regime, two apex candidates can tie on opposite squared length $d^2_{\text{opp}}$ if and only if all three sides are equal ($a^2 = b^2 = c^2$); because equilateral configurations are unreachable on $\mathbb{Z}^2$ (Shoelace area formula), candidate keys are strictly unique. In the continuous regime, two non-winning candidates can tie on the candidate key if and only if their opposite sides are bitwise equal; however, the winning apex candidate is strictly unique because the third vertex then has leg mismatch $\Delta = 0$ and strictly wins the candidate sort. Equilateral configurations are resolved at the highest specificity level without apex labeling.

---

### 3. Illustrative Examples
- **Example 1: Near-Equilateral Lattice Triangle on $\mathbb{Z}^2$:** Consider $A(0, 0)$, $B(1000, 0)$, and $C(500, 866)$. Pairwise squared distances: $d^2(AB) = 1,000,000$ and $d^2(AC) = d^2(BC) = 500^2 + 866^2 = 999,956$. Relative difference: $\frac{1000 - \sqrt{999,956}}{1000} \approx 0.0022\% \ll 0.6\%$. A tolerance-based continuous classifier would evaluate this as equilateral. GeoSolver 2D checks integer inequality $1,000,000 \ne 999,956$, provably rejects equilateral via the Shoelace area theorem, and correctly outputs **Isosceles with apex at $C$** across all 6 input permutations.
- **Example 2: Permutation Equivariance on Near-Tie Isosceles Configuration:** Consider $P(0, 0)$, $Q(1, 0)$, and $R(0.51, 0.86598)$ where $PQ = 1.0$, $PR \approx 1.0050$, and $QR \approx 0.9950$. Both pairs $(PQ, PR)$ and $(PQ, QR)$ satisfy the $0.6\%$ tolerance. By sorting candidates via the label-free key $(\text{diff\_leg}, d^2_{\text{opposite}})$, GeoSolver 2D deterministically selects apex $P$ across all 6 input orderings, preserving physical equivariance.

---

### 4. Empirical Verification & Sensitivity Analysis

#### 4.1. Canonical Benchmark, Parameter Sensitivity & Stress Tests
To evaluate tolerance sensitivity against input perturbations, we generated a reproducible benchmark dataset of 1,000 synthetic triangles (250 each of ground-truth Equilateral, Isosceles, Right, and Scalene prototypes) using `scripts/sensitivity_benchmark.py` (`seed = 42`) perturbed by Gaussian coordinate jitter ($\sigma = 0.03$, 0.3% of nominal edge length 10.0). Table 1 measures the tolerance-versus-noise performance on these continuous prototypes:

| Triangle Class | Ground Truth | True Positive (TP) | Recall (%) | Precision (%) | F1-Score (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Equilateral** | 250 | 205 | 82.0% | 100.0% | 90.1% |
| **Isosceles** | 250 | 212 | 84.8% | 82.5% | 83.6% |
| **Right** | 250 | 247 | 98.8% | 100.0% | 99.4% |
| **Scalene** | 250 | 250 | 100.0% | 85.9% | 92.4% |
| **Overall Dataset** | **1,000** | **914** | **91.4%** | **91.4%** | **91.4%** |

*Empirical sensitivity scan across relative edge tolerance $\text{tol\_rel} \in [0.002, 0.010]$:*
- $\text{tol\_rel} = 0.002$: Overall = 62.9%, Equilateral Recall = 15.2%, Precision = 100.0%, Scalene Precision = 55.7% (overly restrictive; rejects valid hand-drawn regular shapes).
- $\text{tol\_rel} = 0.004$: Overall = 77.8%, Equilateral Recall = 47.6%, Precision = 100.0%, Scalene Precision = 72.5%.
- $\text{tol\_rel} = 0.006$ (Default): Overall = 91.4%, Equilateral Recall = 82.0%, Precision = 100.0%, Scalene Precision = 85.9% (practical operational balance for interactive stylus/freehand drawing).
- $\text{tol\_rel} = 0.008$: Overall = 96.8%, Equilateral Recall = 92.8%, Precision = 100.0%, Scalene Precision = 94.7%.
- $\text{tol\_rel} = 0.010$: Overall = 98.5%, Equilateral Recall = 97.6%, Precision = 100.0%, Scalene Precision = 96.5%.

*Hard Negatives Stress Test (Near-Boundary Asymmetric Triangles):*  
To evaluate robustness against near-boundary false positives across distinct geometric families, we evaluated 200 near-boundary scalene triangles (100 near-isosceles with side mismatch drawn from $0.8\%–1.5\%$, and 100 near-right with angles in $[88.0^\circ, 88.8^\circ]$ where $|\cos \theta| \in [0.021, 0.035]$):

| $\text{tol\_rel}$ | Near-Iso FP ($N=100$) | Near-Right FP ($N=100$) | Total Scalene TN ($N=200$) | Total FP ($N=200$) | Combined FP Rate (%) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0.002 | 0/100 | 0/100 | 200/200 | 0/200 | 0.0% |
| 0.004 | 0/100 | 0/100 | 200/200 | 0/200 | 0.0% |
| 0.006 (Default) | 0/100 | 0/100 | 200/200 | 0/200 | 0.0% |
| 0.008 | 1/100 | 0/100 | 199/200 | 1/200 | 0.5% |
| 0.010 | 36/100 | 0/100 | 164/200 | 36/200 | 18.0% |

This empirical behavior directly reflects the underlying geometric design: false positives in the near-isosceles family only begin to emerge as $\text{tol\_rel}$ enters and exceeds the $0.8\%–1.5\%$ perturbation band (1/100 at 0.008, 36/100 at 0.010), while the 100 near-right scalene configurations produce 0/100 false positives across all tolerance levels because the orthogonal classifier employs a decoupled fixed angular bound ($|\cos \theta| \le 0.015$, corresponding to $[89.14^\circ, 90.86^\circ]$).

*Empirical Invariance & Dual-Regime Comparative Baselines:*
1. **Permutation Equivariance vs. Naive Classifier:** Across 200 near-tie configurations under all $3! = 6$ permutations, a naive positional `if/elif` classifier exhibited **100.0% apex-variant outcomes** (200/200), whereas GeoSolver 2D achieved **0.0% variance** (0/200), strictly preserving apex equivariance.
2. **Lattice Exactness on $\mathbb{Z}^2$:** On integer lattice triples (including near-equilateral configurations such as $(0,0), (1000,0), (500,866)$), a standard continuous tolerance classifier suffered a **75.0% false-positive rate** (3/4) by incorrectly asserting equilateral geometry. GeoSolver 2D's discrete regime correctly proved non-existence of equilateral triangles on $\mathbb{Z}^2$ with **0.0% false positives** (0/4).
3. **Decimal Lattice Sweep ($k \in \{1, 2, 3, 4\}$):** Across 496 non-collinear candidate pairs evaluated on decimal-scaled lattices where float squared lengths drift at $10^{-16}$, GeoSolver 2D's discrete integer kernel achieved **100.0% exact isosceles classification** (496/496).

#### 4.2. Automated Regression Test Suite
The codebase was verified using Python's standard `unittest` framework:
- **Headless Core Library Suite (27 tests):** Pure Python standard library, zero GUI dependencies. Automatically executed on GitHub Actions CI across Ubuntu, Windows, and macOS on Python 3.10–3.13. Covers discrete integer arithmetic on decimal lattices, Shoelace area assertions, intra-regime scale invariance, apex equivariance under all 6 permutations, adversarial near-tie test vectors, DAG taint conservation, cycle safety, deep DAG order-independence, stack safety up to 2,000 nodes, 25-level diamond ladder traversal with strict $O(V+E)$ complexity (<0.05s), and integer return types on grid snapping. Execution time: **0.019s** (PASS).
- **Desktop GUI Canvas Integration Suite (35 tests):** Covers Tkinter canvas event handling, mouse drag snapping, undo/redo instance rebinding, and WCAG 2.1 AA luminance contrast. Execution time: **10.826s** (PASS).
- **Aggregate Local Verification Metric:** **62 / 62 Unit Tests PASS (100.0%)**. When run in a single unified test discovery pass (`python -m unittest discover tests`), the complete suite completed in **17.060s** (combining the 0.019s headless CI suite, 10.826s isolated desktop integration suite, plus process startup and discovery overhead).
- **Cross-Platform Verification:** Automated CI pipeline (`.github/workflows/ci.yml`) executes across `ubuntu-latest`, `windows-latest`, and `macos-latest` on Python 3.10 through 3.13.

---

### 5. Impact and Practical Applications
1. **Educational Integrity in Secondary School Geometry:** In dynamic geometry classrooms, students frequently encounter misleading feedback when heuristic software asserts that an imperfect drawing is an equilateral or right triangle. By enforcing lattice exactness and reporting descriptive near-type deviations, GeoSolver 2D reinforces formal deductive reasoning.
2. **CAD and Geometric Modeling Reliability:** By guaranteeing bitwise permutation invariance, the engine ensures that geometric classification and constraint inference algorithms produce identical output regardless of CAD import sequence or vertex serialization order.

---

### 6. Conclusions and Future Work
GeoSolver 2D demonstrates that combining dynamic taint tracking with specificity-ordered predicates resolves the tension between continuous user interaction and discrete mathematical truth. By evaluating exact integer lattice arithmetic when appropriate and sorting candidate hypotheses deterministically under continuous perturbations, the engine guarantees intra-regime scale invariance and permutation-invariant classification. Future work will extend this architecture to 3D spatial geometry and polyhedral cross-sections.

---

### Declaration of Generative AI in Scientific Writing
During the preparation and development of this work, the author utilized generative AI assistants (Claude by Anthropic and Gemini by Google) for code refactoring, test generation, mathematical invariant verification, grammar refinement, and editorial structuring. The iterative review rounds conducted with AI models served as rigorous internal design audits and red-teaming exercises; they do not substitute for formal journal peer review. The author independently verified, executed, and validated all algorithms, mathematical proofs, test suites, and empirical benchmarks, and takes full responsibility for the factual and mathematical veracity of this publication.

### Conflict of Interest
The author develops and distributes educational dynamic geometry software, including packaged distributions of GeoSolver on the Microsoft Store. The core mathematical algorithms, classification engine, and provenance tracking system described in this paper are released as free and open-source software under the GNU General Public License v3 (GPLv3) without commercial restrictions.

### Author Biography
**Bao-Trung Nguyen** received his degree in Pharmacy from the University of Medicine and Pharmacy at Ho Chi Minh City in 2021. With over five years of professional experience in pharmaceutical research and development (R&D), his current research interests include computational geometry, scientific software engineering, dynamic geometry systems, and robust arithmetic algorithms. He currently conducts scientific research as an independent researcher in Ho Chi Minh City, Vietnam.

### References
1. Shewchuk, J. R. (1997). *"Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates"*. Discrete & Computational Geometry, 18(3), pp. 305–363. DOI: 10.1007/PL00009321.
2. The CGAL Project (2024). *"CGAL User and Reference Manual"*. CGAL Editorial Board, 5.6 edition.
3. Schwartz, E. J., Avgerinos, T., & Brumley, D. (2010). *"All You Ever Wanted to Know About Dynamic Taint Analysis and Forward Symbolic Execution (but Might Have Been Afraid to Ask)"*. IEEE Symposium on Security and Privacy (S&P 2010), pp. 317–331. DOI: 10.1109/SP.2010.26.
4. IEEE Computer Society (2019). *"IEEE Standard for Floating-Point Arithmetic"*. IEEE Std 754-2019, pp. 1–84. DOI: 10.1109/IEEESTD.2019.8766229.
5. World Wide Web Consortium (W3C) (2018). *"Web Content Accessibility Guidelines (WCAG) 2.1"*. W3C Recommendation.

---

## PART 3: VERBATIM PRODUCTION SOURCE CODE

### 3.1. `geosolver_core/provenance.py`
```python
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
```

### 3.2. `geosolver_core/classifier.py`
```python
# -*- coding: utf-8 -*-
"""
GeoSolver 2D Core - Pure Mathematical Classification Engine
License: GNU General Public License v3 (GPLv3)
"""

from __future__ import annotations
import math
from typing import Dict, Tuple, List, Optional, Any, Union
from geosolver_core.provenance import point_provenance_flag, _point_flag, snap_to_grid

def as_scaled_ints(coords: List[float], max_k: int = 4) -> Tuple[Optional[List[int]], float]:
    """
    Detect integer lattice coordinates or clean decimal inputs (e.g., 8.7, 2.9, 0.04):
    Multiplies coordinates by 10^k (k = 0..max_k). If all coordinates fall within
    alignment tolerance 1e-5 of an integer, returns the scaled integer coordinates.
    Otherwise (irrational coordinates or freehand float drift), returns (None, 1.0).

    Design and Boundary Characteristics:
    - Alignment Tolerance: 1e-5 absorbs IEEE-754 mantissa rounding around clean decimal representations.
    - Scale Limit: max_k = 4 bounds the maximum multiplier to 10^4. Fractional coordinates
      with more than 4 significant fractional digits fall cleanly into the continuous regime.
    - Epistemic Boundary: Scale invariance holds intra-regime.
      * Downward Crossing: Scaling a discrete shape below 1e-5 moves its coordinates
        across the precision threshold into the continuous regime.
      * Upward Crossing: Conversely, magnifying an untagged continuous coordinate
        with > 4 fractional digits (e.g. by 10x) can reduce its effective fractional digits
        to <= 4, causing it to cross upward into the discrete lattice regime.
        Points carrying explicit freehand provenance (`exact=False`) are quarantined
        against this upward crossing until explicitly snapped to grid.
    """
    for k in range(max_k + 1):
        s = 10 ** k
        if all(abs(v * s - round(v * s)) < 1e-5 for v in coords):
            return [round(v * s) for v in coords], float(s)
    return None, 1.0

def _finite(v: Any, label: str) -> float:
    """Validate and convert to finite float, strictly rejecting None, strings, Inf, and NaN."""
    if isinstance(v, (str, bytes)):
        raise ValueError(f"Coordinate '{label}' cannot be a string: {v!r}")
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f"Coordinate '{label}' invalid numeric value: {v!r}")
    if not math.isfinite(f):
        raise ValueError(f"Coordinate '{label}' must be finite (rejected NaN/Inf): {f}")
    return f

def classify_triangle(
    pA: Union[Dict[str, Any], Tuple[float, float], List[float]],
    pB: Union[Dict[str, Any], Tuple[float, float], List[float]],
    pC: Union[Dict[str, Any], Tuple[float, float], List[float]],
    points_exact: Optional[bool] = None,
    tol_rel: float = 0.006
) -> Dict[str, Any]:
    """
    Pure geometric triangle classifier (Zero GUI / Tkinter dependencies).
    Guarantees bitwise type permutation invariance and apex equivariance.
    Evaluates provenance through the Directed Acyclic Graph (DAG) taint engine.
    """
    def extract_pt(p: Any, default_name: str) -> Tuple[float, float, str, Optional[bool]]:
        if p is None:
            raise ValueError(f"Point coordinate cannot be None: {p!r}")
        if isinstance(p, dict):
            if "x" not in p or "y" not in p:
                raise ValueError(f"Point dict missing 'x' or 'y': {p}")
            provenance = point_provenance_flag(p)
            return _finite(p["x"], "x"), _finite(p["y"], "y"), str(p.get("name") or default_name), provenance
        if not isinstance(p, (list, tuple)) or len(p) < 2:
            raise ValueError(f"Point must be a dict or sequence of at least 2 numbers: {p!r}")
        return _finite(p[0], "x"), _finite(p[1], "y"), default_name, None

    xA, yA, nA, exA = extract_pt(pA, "A")
    xB, yB, nB, exB = extract_pt(pB, "B")
    xC, yC, nC, exC = extract_pt(pC, "C")

    # Strict Taint Conservation Law: Any tainted vertex forces continuous regime
    pt_flags = [exA, exB, exC]
    if any(f is False for f in pt_flags) or points_exact is False:
        user_declared_exact = False
    elif points_exact is True or all(f is True for f in pt_flags):
        user_declared_exact = True
    else:
        user_declared_exact = None

    u_AB = (xB - xA, yB - yA)
    u_AC = (xC - xA, yC - yA)
    u_BC = (xC - xB, yC - yB)

    c_sq = u_AB[0]**2 + u_AB[1]**2
    b_sq = u_AC[0]**2 + u_AC[1]**2
    a_sq = u_BC[0]**2 + u_BC[1]**2

    c_len = math.sqrt(c_sq)  # AB
    b_len = math.sqrt(b_sq)  # AC
    a_len = math.sqrt(a_sq)  # BC

    cross = u_AB[0] * u_AC[1] - u_AB[1] * u_AC[0]
    scaled_coords, scale_factor = as_scaled_ints([xA, yA, xB, yB, xC, yC], max_k=4)
    is_discrete = (scaled_coords is not None) and (user_declared_exact is not False)

    if is_discrete:
        sxA, syA, sxB, syB, sxC, syC = scaled_coords
        s_uAB = (sxB - sxA, syB - syA)
        s_uAC = (sxC - sxA, syC - syA)
        s_uBC = (sxC - sxB, syC - syB)
        is_coincident = (s_uAB == (0, 0)) or (s_uAC == (0, 0)) or (s_uBC == (0, 0))
        is_collinear = (s_uAB[0] * s_uAC[1] - s_uAB[1] * s_uAC[0] == 0)
    else:
        l_max = max(a_len, b_len, c_len)
        if l_max < 1e-12:
            is_coincident = True
        else:
            is_coincident = (c_len / l_max < 1e-6) or (b_len / l_max < 1e-6) or (a_len / l_max < 1e-6)
        rel_cross = abs(cross) / (l_max * l_max) if l_max > 1e-12 else 0.0
        is_collinear = (rel_cross < 1e-5)

    if is_coincident:
        return {"is_triangle": False, "type": "coincident", "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    if is_collinear:
        return {"is_triangle": False, "type": "collinear", "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    l_max = max(a_len, b_len, c_len)
    l_min = min(a_len, b_len, c_len)

    # Initialize deviation metrics to exact zeros for discrete regime
    diff_AB_AC = 0.0
    diff_BA_BC = 0.0
    diff_CA_CB = 0.0

    if is_discrete:
        d2_AB = s_uAB[0]**2 + s_uAB[1]**2
        d2_AC = s_uAC[0]**2 + s_uAC[1]**2
        d2_BC = s_uBC[0]**2 + s_uBC[1]**2

        eq_AB_AC = (d2_AB == d2_AC)
        eq_BA_BC = (d2_AB == d2_BC)
        eq_CA_CB = (d2_AC == d2_BC)

        # Gauss-Shoelace area theorem: Equilateral triangle is provably unreachable on Z^2
        if eq_AB_AC and eq_BA_BC and eq_CA_CB:
            raise AssertionError("Equilateral triangle is provably impossible on Z^2 by Gauss-Shoelace area theorem")
        is_equilateral = False

        dot_A = s_uAB[0] * s_uAC[0] + s_uAB[1] * s_uAC[1]
        dot_B = -s_uAB[0] * s_uBC[0] - s_uAB[1] * s_uBC[1]
        dot_C = s_uAC[0] * s_uBC[0] + s_uAC[1] * s_uBC[1]

        perp_A = (dot_A == 0)
        perp_B = (dot_B == 0)
        perp_C = (dot_C == 0)
    else:
        max_AB_AC = max(c_len, b_len)
        max_BA_BC = max(c_len, a_len)
        max_CA_CB = max(b_len, a_len)

        eq_AB_AC = (abs(c_len - b_len) <= tol_rel * max_AB_AC) if max_AB_AC > 1e-12 else True
        eq_BA_BC = (abs(c_len - a_len) <= tol_rel * max_BA_BC) if max_BA_BC > 1e-12 else True
        eq_CA_CB = (abs(b_len - a_len) <= tol_rel * max_CA_CB) if max_CA_CB > 1e-12 else True

        diff_AB_AC = abs(c_len - b_len) / max_AB_AC if max_AB_AC > 1e-12 else 0.0
        diff_BA_BC = abs(c_len - a_len) / max_BA_BC if max_BA_BC > 1e-12 else 0.0
        diff_CA_CB = abs(b_len - a_len) / max_CA_CB if max_CA_CB > 1e-12 else 0.0

        is_equilateral = ((l_max - l_min) <= tol_rel * l_max) if l_max > 1e-12 else False

        dot_A = u_AB[0] * u_AC[0] + u_AB[1] * u_AC[1]
        dot_B = -u_AB[0] * u_BC[0] - u_AB[1] * u_BC[1]
        dot_C = u_AC[0] * u_BC[0] + u_AC[1] * u_BC[1]

        # Scale-correct perpendicularity check (|cos theta| <= 0.015 corresponds to |theta - 90| <= 0.86 deg)
        perp_A = (abs(dot_A / (c_len * b_len)) <= 0.015)
        perp_B = (abs(dot_B / (c_len * a_len)) <= 0.015)
        perp_C = (abs(dot_C / (b_len * a_len)) <= 0.015)

    # Specificity Hierarchy: Equilateral > Right-Isosceles > Isosceles > Right > Scalene
    if is_equilateral:
        return {"is_triangle": True, "type": "equilateral", "exact": is_discrete, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    opp_A = d2_BC if is_discrete else a_sq
    opp_B = d2_AC if is_discrete else b_sq
    opp_C = d2_AB if is_discrete else c_sq

    # 1. Right-Isosceles: candidate key sorted strictly by label-free (diff_leg, opposite_squared_side)
    ri_candidates = []
    if perp_A and eq_AB_AC: ri_candidates.append((diff_AB_AC, opp_A, nA))
    if perp_B and eq_BA_BC: ri_candidates.append((diff_BA_BC, opp_B, nB))
    if perp_C and eq_CA_CB: ri_candidates.append((diff_CA_CB, opp_C, nC))

    if ri_candidates:
        ri_candidates.sort(key=lambda item: (item[0], item[1]))
        best_apex = ri_candidates[0][2]
        return {"is_triangle": True, "type": "right_isosceles", "vertex": best_apex, "exact": is_discrete, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    # 2. Isosceles: candidate key sorted strictly by label-free (diff_leg, opposite_squared_side)
    iso_candidates = []
    if eq_AB_AC: iso_candidates.append((diff_AB_AC, opp_A, nA))
    if eq_BA_BC: iso_candidates.append((diff_BA_BC, opp_B, nB))
    if eq_CA_CB: iso_candidates.append((diff_CA_CB, opp_C, nC))

    if iso_candidates:
        iso_candidates.sort(key=lambda item: (item[0], item[1]))
        best_apex = iso_candidates[0][2]
        return {"is_triangle": True, "type": "isosceles", "vertex": best_apex, "exact": is_discrete, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    # 3. Right: candidate key sorted strictly by label-free (cosine_deviation, opposite_squared_side)
    right_candidates = []
    if perp_A: right_candidates.append((abs(dot_A / (c_len * b_len)) if not is_discrete else 0.0, opp_A, nA))
    if perp_B: right_candidates.append((abs(dot_B / (c_len * a_len)) if not is_discrete else 0.0, opp_B, nB))
    if perp_C: right_candidates.append((abs(dot_C / (b_len * a_len)) if not is_discrete else 0.0, opp_C, nC))

    if right_candidates:
        right_candidates.sort(key=lambda item: (item[0], item[1]))
        best_apex = right_candidates[0][2]
        return {"is_triangle": True, "type": "right", "vertex": best_apex, "exact": is_discrete, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}

    return {"is_triangle": True, "type": "scalene", "exact": is_discrete, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}}
```

---

## PART 4: VERBATIM SENSITIVITY BENCHMARK SCRIPT

### `scripts/sensitivity_benchmark.py`
```python
# -*- coding: utf-8 -*-
"""
Sensitivity and Robustness Benchmark Generator for GeoSolver 2D
Evaluates classification accuracy, tolerance trade-offs, and permutation equivariance.
License: GNU General Public License v3 (GPLv3)
"""

import math
import random
import itertools
import argparse
from typing import List, Tuple, Dict, Any, Optional
from geosolver_core.classifier import classify_triangle


def generate_standard_dataset(n_per_class: int = 250, seed: int = 42, noise_std: float = 0.03) -> List[Tuple[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]], str]]:
    random.seed(seed)
    dataset = []

    # 1. Equilateral Triangles (nominal side 10.0)
    for _ in range(n_per_class):
        s = 10.0
        pA = (0.0 + random.gauss(0, noise_std), 0.0 + random.gauss(0, noise_std))
        pB = (s + random.gauss(0, noise_std), 0.0 + random.gauss(0, noise_std))
        pC = (s * 0.5 + random.gauss(0, noise_std), s * (math.sqrt(3)/2) + random.gauss(0, noise_std))
        dataset.append(((pA, pB, pC), 'equilateral'))

    # 2. Isosceles Triangles (base 8.0, legs 10.0)
    for _ in range(n_per_class):
        b = 8.0
        h = math.sqrt(10.0**2 - 4.0**2)  # sqrt(84) approx 9.165
        pA = (0.0 + random.gauss(0, noise_std), 0.0 + random.gauss(0, noise_std))
        pB = (b + random.gauss(0, noise_std), 0.0 + random.gauss(0, noise_std))
        pC = (b * 0.5 + random.gauss(0, noise_std), h + random.gauss(0, noise_std))
        dataset.append(((pA, pB, pC), 'isosceles'))

    # 3. Right-Angled Triangles (3-4-5 scaled by 2 -> legs 6.0, 8.0, hyp 10.0)
    for _ in range(n_per_class):
        pA = (0.0 + random.gauss(0, noise_std), 0.0 + random.gauss(0, noise_std))
        pB = (8.0 + random.gauss(0, noise_std), 0.0 + random.gauss(0, noise_std))
        pC = (0.0 + random.gauss(0, noise_std), 6.0 + random.gauss(0, noise_std))
        dataset.append(((pA, pB, pC), 'right'))

    # 4. Scalene Triangles (distinct sides 6.0, 9.0, 12.0)
    for _ in range(n_per_class):
        a, b, c = 6.0, 9.0, 12.0
        xC = (c**2 + b**2 - a**2) / (2.0 * c)
        yC = math.sqrt(max(0.1, b**2 - xC**2))
        pA = (0.0 + random.gauss(0, noise_std), 0.0 + random.gauss(0, noise_std))
        pB = (c + random.gauss(0, noise_std), 0.0 + random.gauss(0, noise_std))
        pC = (xC + random.gauss(0, noise_std), yC + random.gauss(0, noise_std))
        dataset.append(((pA, pB, pC), 'scalene'))

    return dataset


def evaluate_dataset(dataset: List[Tuple[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]], str]], tol_rel: float = 0.006) -> Dict[str, Any]:
    N_per_class = len(dataset) // 4
    tp = {'equilateral': 0, 'isosceles': 0, 'right': 0, 'scalene': 0}
    total_pred = {'equilateral': 0, 'isosceles': 0, 'right': 0, 'scalene': 0, 'right_isosceles': 0}

    for pts, target in dataset:
        res = classify_triangle(pts[0], pts[1], pts[2], points_exact=False, tol_rel=tol_rel)
        pred = res['type']
        total_pred[pred] = total_pred.get(pred, 0) + 1
        if pred == target:
            tp[target] += 1

    metrics = {}
    for cls in tp:
        precision = tp[cls] / total_pred[cls] if total_pred.get(cls, 0) > 0 else 0.0
        recall = tp[cls] / N_per_class
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        metrics[cls] = {'precision': precision, 'recall': recall, 'f1': f1, 'tp': tp[cls]}

    overall_acc = sum(tp.values()) / len(dataset)
    return {'per_class': metrics, 'overall_accuracy': overall_acc, 'tp_sum': sum(tp.values())}


def run_sensitivity_sweep(dataset: List[Tuple[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]], str]]) -> None:
    tolerances = [0.002, 0.004, 0.006, 0.008, 0.010]
    print("\n=== Standard Dataset Sensitivity Sweep ===")
    print("tol_rel | Overall | Eq Rec | Eq Prec | Iso Rec | Iso Prec | Right Rec | Scalene Prec")
    print("--------|---------|--------|---------|---------|----------|-----------|-------------")
    for tol in tolerances:
        res = evaluate_dataset(dataset, tol_rel=tol)
        m = res['per_class']
        print(f"{tol:7.3f} | {res['overall_accuracy']*100:6.1f}% | {m['equilateral']['recall']*100:5.1f}% | {m['equilateral']['precision']*100:6.1f}% | {m['isosceles']['recall']*100:6.1f}% | {m['isosceles']['precision']*100:7.1f}% | {m['right']['recall']*100:8.1f}% | {m['scalene']['precision']*100:11.1f}%")


def run_hard_negatives_benchmark(seed: int = 42) -> None:
    """
    Evaluates 200 near-boundary hard negative scalene triangles across two decoupled families:
      - 100 near-isosceles scalene configurations with 0.8% - 1.5% side length mismatch.
        False positives begin emerging as tol_rel reaches and exceeds the lower bound of the
        mismatch band (1/100 at 0.008; 36/100 at 0.010).
      - 100 near-right scalene configurations with angles in [88.0 deg, 88.8 deg]
        (|cos theta| in [0.021, 0.035]). Yields 0/100 FP across all tol_rel values because
        the right-angle predicate employs a decoupled fixed angular bound |cos| <= 0.015 (~89.14 deg).
    """
    random.seed(seed)
    near_iso = []
    # 100 near-isosceles scalene
    for _ in range(100):
        mismatch = random.uniform(0.008, 0.015)
        base = 12.0
        leg1 = 10.0
        leg2 = 10.0 * (1.0 + mismatch)
        xC = (base**2 + leg1**2 - leg2**2) / (2.0 * base)
        yC = math.sqrt(max(0.1, leg1**2 - xC**2))
        near_iso.append(((0.0, 0.0), (base, 0.0), (xC, yC)))

    # 100 near-right scalene
    near_right = []
    for _ in range(100):
        deg = random.uniform(88.0, 88.8)
        rad = math.radians(deg)
        near_right.append(((0.0, 0.0), (8.0, 0.0), (6.0 * math.cos(rad), 6.0 * math.sin(rad))))

    print("\n=== Hard Negatives Stress Test (Near-Boundary Scalene) ===")
    print("tol_rel | Near-Iso FP (N=100) | Near-Right FP (N=100) | Total TN (N=200) | Total FP (N=200) | Combined FP (%)")
    print("--------|---------------------|-----------------------|------------------|------------------|----------------")
    for tol in [0.002, 0.004, 0.006, 0.008, 0.010]:
        fp_iso = 0
        for pts in near_iso:
            res = classify_triangle(pts[0], pts[1], pts[2], points_exact=False, tol_rel=tol)
            if res['type'] != 'scalene':
                fp_iso += 1

        fp_right = 0
        for pts in near_right:
            res = classify_triangle(pts[0], pts[1], pts[2], points_exact=False, tol_rel=tol)
            if res['type'] != 'scalene':
                fp_right += 1

        total_fp = fp_iso + fp_right
        total_tn = 200 - total_fp
        print(f"{tol:7.3f} | {fp_iso:16d}/100 | {fp_right:18d}/100 | {total_tn:13d}/200 | {total_fp:13d}/200 | {total_fp/200*100:13.1f}%")


def naive_classify_triangle(pA: Tuple[float, float], pB: Tuple[float, float], pC: Tuple[float, float], tol: float = 0.006) -> Tuple[str, Optional[int]]:
    """Naive positional if/elif classifier without label-free tie-breaking."""
    dAB = math.hypot(pB[0] - pA[0], pB[1] - pA[1])
    dBC = math.hypot(pC[0] - pB[0], pC[1] - pB[1])
    dCA = math.hypot(pA[0] - pC[0], pA[1] - pC[1])
    sides = [dAB, dBC, dCA]
    m = max(sides)
    if (m - min(sides)) <= tol * m:
        return 'equilateral', None
    # Positional first-match checks
    if abs(dAB - dCA) <= tol * max(dAB, dCA):
        return 'isosceles', 0  # Apex at first vertex A
    if abs(dAB - dBC) <= tol * max(dAB, dBC):
        return 'isosceles', 1  # Apex at second vertex B
    if abs(dBC - dCA) <= tol * max(dBC, dCA):
        return 'isosceles', 2  # Apex at third vertex C
    # Right angle check
    dotA = (pB[0]-pA[0])*(pC[0]-pA[0]) + (pB[1]-pA[1])*(pC[1]-pA[1])
    dotB = (pA[0]-pB[0])*(pC[0]-pB[0]) + (pA[1]-pB[1])*(pC[1]-pB[1])
    dotC = (pA[0]-pC[0])*(pB[0]-pC[0]) + (pA[1]-pC[1])*(pB[1]-pC[1])
    if abs(dotA) / (dAB * dCA) <= tol: return 'right', 0
    if abs(dotB) / (dAB * dBC) <= tol: return 'right', 1
    if abs(dotC) / (dBC * dCA) <= tol: return 'right', 2
    return 'scalene', None


def run_permutation_baseline(n_triangles: int = 200, seed: int = 42) -> None:
    random.seed(seed)
    naive_variants = 0
    geosolver_variants = 0

    for _ in range(n_triangles):
        d = random.uniform(5.0, 10.0)
        pA = (random.uniform(-5, 5), random.uniform(-5, 5))
        pB = (pA[0] + d, pA[1])
        pC = (pA[0] + d * 0.51, pA[1] + d * 0.86598)
        pts = [pA, pB, pC]
        names = {pA: 'A', pB: 'B', pC: 'C'}

        naive_apex_set = set()
        geo_apex_set = set()

        for perm in itertools.permutations(pts):
            _, n_apex_idx = naive_classify_triangle(perm[0], perm[1], perm[2])
            n_apex_name = names[perm[n_apex_idx]] if n_apex_idx is not None else None
            naive_apex_set.add(n_apex_name)

            dict_perm = [{'x': p[0], 'y': p[1], 'name': names[p]} for p in perm]
            g = classify_triangle(dict_perm[0], dict_perm[1], dict_perm[2], points_exact=False)
            geo_apex_set.add(g.get('vertex'))

        if len(naive_apex_set) > 1:
            naive_variants += 1
        if len(geo_apex_set) > 1:
            geosolver_variants += 1

    print("\n=== Permutation Invariance & Equivariance Comparison ===")
    print(f"Sample size: {n_triangles} near-tie configurations under all 6 permutations")
    print(f"  - Naive Positional Classifier: {naive_variants}/{n_triangles} ({naive_variants/n_triangles*100:.1f}%) apex-variant outcomes")
    print(f"  - GeoSolver 2D Invariant Kernel: {geosolver_variants}/{n_triangles} ({geosolver_variants/n_triangles*100:.1f}%) apex-variant outcomes")


def run_lattice_exactness_benchmark() -> None:
    print("\n=== Dual-Regime Lattice Exactness Benchmark ===")
    lattice_cases = [
        ((0, 0), (1000, 0), (500, 866)),   # Paper Example 1 (866^2 = 749956, AC^2 = BC^2 = 999956)
        ((0, 0), (100, 0), (50, 87)),      # Scaled near-equilateral
        ((0, 0), (10, 0), (5, 9)),         # Integer isosceles
        ((0, 0), (10000, 0), (5000, 8660)) # Higher-scale near-equilateral
    ]
    naive_fp = 0
    geosolver_fp = 0

    for pts in lattice_cases:
        n_type, _ = naive_classify_triangle(pts[0], pts[1], pts[2], tol=0.006)
        if n_type == 'equilateral':
            naive_fp += 1

        g = classify_triangle(pts[0], pts[1], pts[2], points_exact=True)
        if g['type'] == 'equilateral':
            geosolver_fp += 1

    print(f"Test cases on integer lattice Z^2: {len(lattice_cases)}")
    print(f"  - Continuous Tolerance Classifier: {naive_fp}/{len(lattice_cases)} ({naive_fp/len(lattice_cases)*100:.1f}%) false-positive equilateral")
    print(f"  - GeoSolver Discrete Lattice Regime: {geosolver_fp}/{len(lattice_cases)} ({geosolver_fp/len(lattice_cases)*100:.1f}%) false-positive equilateral")


def run_decimal_lattice_sweep(n_samples: int = 500, seed: int = 42) -> None:
    """Tests 500 non-collinear decimal lattice isosceles pairs across k in {1, 2, 3, 4}."""
    random.seed(seed)
    valid_count = 0
    exact_match_count = 0

    for _ in range(n_samples):
        k = random.randint(1, 4)
        scale = 10**k
        sxB = random.randint(-50, 50)
        syB = random.randint(-50, 50)
        d2 = sxB**2 + syB**2
        found_pair = None
        for dx in range(-abs(sxB), abs(sxB) + 1):
            rem = d2 - dx**2
            if rem >= 0:
                dy = int(round(rem**0.5))
                if dy**2 == rem and (dx != sxB or dy != syB) and (dx * syB != dy * sxB):
                    found_pair = (dx, dy)
                    break
        if found_pair:
            sxC, syC = found_pair
            pA = (0.0, 0.0)
            pB = (sxB / scale, syB / scale)
            pC = (sxC / scale, syC / scale)
            res = classify_triangle(pA, pB, pC)
            if res.get('is_triangle'):
                valid_count += 1
                if res.get('type') == 'isosceles' and res.get('exact') is True:
                    exact_match_count += 1

    print("\n=== Decimal Lattice Invariant Sweep (k in {1, 2, 3, 4}) ===")
    print(f"Non-collinear candidate pairs evaluated: {valid_count}")
    print(f"  - GeoSolver Discrete Regime Matches: {exact_match_count}/{valid_count} ({exact_match_count/valid_count*100:.1f}%) exact isosceles")


def main():
    parser = argparse.ArgumentParser(description="GeoSolver 2D Parameter Sensitivity Benchmark")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--tol-rel", type=float, default=0.006, help="Relative edge tolerance (default: 0.006)")
    parser.add_argument("--sweep", action="store_true", help="Run tolerance sweep across [0.002, 0.010]")
    parser.add_argument("--hard-negatives", action="store_true", help="Run hard negatives stress test")
    parser.add_argument("--baseline", action="store_true", help="Run permutation & lattice baseline comparisons")
    parser.add_argument("--decimal-lattice", action="store_true", help="Run decimal lattice sweep across k in 1..4")
    parser.add_argument("--all", action="store_true", help="Run all benchmarks and comparisons")
    args = parser.parse_args()

    dataset = generate_standard_dataset(seed=args.seed)
    
    res = evaluate_dataset(dataset, tol_rel=args.tol_rel)
    print(f"=== GeoSolver 2D Benchmark (tol_rel = {args.tol_rel:.3f}, Seed = {args.seed}) ===")
    print("Triangle Class | Ground Truth | True Positive (TP) | Recall (%) | Precision (%) | F1-Score (%)")
    print("---------------|:------------:|:------------------:|:----------:|:-------------:|:------------:")
    for c, m in res['per_class'].items():
        print(f"{c.capitalize():14s} | {250:12d} | {m['tp']:18d} | {m['recall']*100:9.1f}% | {m['precision']*100:12.1f}% | {m['f1']*100:11.1f}%")
    print(f"Overall Dataset| {len(dataset):12d} | {res['tp_sum']:18d} | {res['overall_accuracy']*100:9.1f}% | {res['overall_accuracy']*100:12.1f}% | {res['overall_accuracy']*100:11.1f}%")

    if args.sweep or args.all:
        run_sensitivity_sweep(dataset)

    if args.hard_negatives or args.all:
        run_hard_negatives_benchmark(seed=args.seed)

    if args.baseline or args.all:
        run_permutation_baseline(n_triangles=200, seed=args.seed)
        run_lattice_exactness_benchmark()

    if args.decimal_lattice or args.all:
        run_decimal_lattice_sweep(n_samples=500, seed=args.seed)


if __name__ == '__main__':
    main()
```

### 4.3. Multi-Platform GitHub Actions CI (`.github/workflows/ci.yml`)
```yaml
name: GeoSolver 2D Core CI

on:
  push:
    branches: [ master, main ]
  pull_request:
    branches: [ master, main ]

jobs:
  test-headless-core:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12', '3.13']
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run Headless Core Test Suite (Zero GUI Dependencies)
        run: |
          python -m unittest -v tests.test_geosolver_core tests.test_rebuttal_invariants tests.test_round9_taint_validation

      - name: Verify Sensitivity Benchmark & Invariants Suite
        run: |
          python scripts/sensitivity_benchmark.py --all
```

---

## PART 5: AUTOMATED TEST EXECUTION LOGS (62 TESTS, 100% PASS)

### 5.1. Headless Core Test Suite (27 tests, 0.019s)
```
test_decimal_lattice_exact_isosceles_regression (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_decimal_lattice_exact_isosceles_regression)
Regression test: Decimal lattice coordinates where float squared lengths differ at 1e-16. ... ok
test_diamond_ladder_linear_complexity_depth_25 (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_diamond_ladder_linear_complexity_depth_25)
Item 2 Audit: Verifies strict O(V+E) linear traversal on a 25-level diamond ladder. ... ok
test_grid_snap_restores_exactness_and_returns_ints (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_grid_snap_restores_exactness_and_returns_ints)
Tests snap_to_grid restores exactness and returns Python int types on integer coordinates. ... ok
test_item_2_1_stale_flag_after_parent_drag (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_item_2_1_stale_flag_after_parent_drag)
Referee Item 2.1: Stored exact flag on derived point must not wash dynamic parent taint. ... ok
test_item_2_2_parent_order_independence_deep_dag (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_item_2_2_parent_order_independence_deep_dag)
Referee Item 2.2: Order independence across parent permutations on deep subtrees (depth 110). ... ok
test_near_tie_permutation_invariance_headless (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_near_tie_permutation_invariance_headless)
Replicated in Headless CI Suite: Adversarial near-tie case across all 6 permutations. ... ok
test_permutation_invariance_all_six_orderings_headless (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_permutation_invariance_all_six_orderings_headless)
Replicated in Headless CI Suite: All 6 permutations on discrete and continuous cases. ... ok
test_provenance_dag_and_taint_conservation (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_provenance_dag_and_taint_conservation) ... ok
test_provenance_deep_stack_iterative_safety (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_provenance_deep_stack_iterative_safety)
Evaluates arbitrary depth (2,000 nodes) without RecursionError via iterative DFS. ... ok
test_shoelace_equilateral_unreachable_assertion (tests.test_geosolver_core.TestGeoSolverCoreDirect.test_shoelace_equilateral_unreachable_assertion)
Equilateral is unreachable on Z^2. ... ok
test_3_4_5_right_triangle_named_equivariance (tests.test_rebuttal_invariants.TestRebuttalInvariants.test_3_4_5_right_triangle_named_equivariance) ... ok
test_example_1_lattice_isosceles_named_equivariance (tests.test_rebuttal_invariants.TestRebuttalInvariants.test_example_1_lattice_isosceles_named_equivariance) ... ok
test_example_2_lattice_isosceles_named_equivariance (tests.test_rebuttal_invariants.TestRebuttalInvariants.test_example_2_lattice_isosceles_named_equivariance) ... ok
test_lattice_scalene_permutation_invariance (tests.test_rebuttal_invariants.TestRebuttalInvariants.test_lattice_scalene_permutation_invariance) ... ok
test_near_tie_equivariance_continuous (tests.test_rebuttal_invariants.TestRebuttalInvariants.test_near_tie_equivariance_continuous) ... ok
test_unit_right_isosceles_named_equivariance (tests.test_rebuttal_invariants.TestRebuttalInvariants.test_unit_right_isosceles_named_equivariance) ... ok
test_derived_without_parents_is_unknown (tests.test_round9_taint_validation.TestDerivedPointPropagation.test_derived_without_parents_is_unknown) ... ok
test_midpoint_of_free_parents_is_tainted (tests.test_round9_taint_validation.TestDerivedPointPropagation.test_midpoint_of_free_parents_is_tainted) ... ok
test_midpoint_of_typed_parents_is_exact (tests.test_round9_taint_validation.TestDerivedPointPropagation.test_midpoint_of_typed_parents_is_exact) ... ok
test_explicit_exact_false_beats_exact_source (tests.test_round9_taint_validation.TestFreehandTaint.test_explicit_exact_false_beats_exact_source) ... ok
test_free_integer_right_triangle_uses_tolerance_branch (tests.test_round9_taint_validation.TestFreehandTaint.test_free_integer_right_triangle_uses_tolerance_branch) ... ok
test_free_near_isosceles_is_flagged_but_typed_is_not (tests.test_round9_taint_validation.TestFreehandTaint.test_free_near_isosceles_is_flagged_but_typed_is_not) ... ok
test_mixed_typed_and_free_is_false (tests.test_round9_taint_validation.TestFreehandTaint.test_mixed_typed_and_free_is_false) ... ok
test_points_exact_true_cannot_override_free (tests.test_round9_taint_validation.TestFreehandTaint.test_points_exact_true_cannot_override_free) ... ok
test_nan_inf_none_rejected_in_dict (tests.test_round9_taint_validation.TestInputValidation.test_nan_inf_none_rejected_in_dict) ... ok
test_nan_inf_none_rejected_in_tuple (tests.test_round9_taint_validation.TestInputValidation.test_nan_inf_none_rejected_in_tuple) ... ok
test_3_4_5_at_1e_minus_5 (tests.test_round9_taint_validation.TestMicroScaleStillOk.test_3_4_5_at_1e_minus_5) ... ok

----------------------------------------------------------------------
Ran 27 tests in 0.019s

OK
```

### 5.2. Desktop GUI Canvas Integration Suite (35 tests, 10.826s)
```
test_01_classify_triangle_comprehensive_cases (tests.test_geometry_invariants.TestGeometryInvariants.test_01_classify_triangle_comprehensive_cases) ... ok
test_02_regression_original_bug_isosceles_not_equilateral (tests.test_geometry_invariants.TestGeometryInvariants.test_02_regression_original_bug_isosceles_not_equilateral) ... ok
test_03_scale_invariance_property (tests.test_geometry_invariants.TestGeometryInvariants.test_03_scale_invariance_property) ... ok
test_04_typed_decimals_rejection_fractional_cases (tests.test_geometry_invariants.TestGeometryInvariants.test_04_typed_decimals_rejection_fractional_cases) ... ok
test_05_negative_equilateral_pure_float_coordinates (tests.test_geometry_invariants.TestGeometryInvariants.test_05_negative_equilateral_pure_float_coordinates) ... ok
test_06_collinear_and_coincident_points (tests.test_geometry_invariants.TestGeometryInvariants.test_06_collinear_and_coincident_points) ... ok
test_07_right_and_right_isosceles_triangles (tests.test_geometry_invariants.TestGeometryInvariants.test_07_right_and_right_isosceles_triangles) ... ok
test_08_ellipse_edge_cases_and_rotational_invariance (tests.test_geometry_invariants.TestGeometryInvariants.test_08_ellipse_edge_cases_and_rotational_invariance) ... ok
test_09_ramanujan_ii_exact_accuracy_table (tests.test_geometry_invariants.TestGeometryInvariants.test_09_ramanujan_ii_exact_accuracy_table) ... ok
test_10_wcag_21_aa_itemized_real_contrast (tests.test_geometry_invariants.TestGeometryInvariants.test_10_wcag_21_aa_itemized_real_contrast) ... ok
test_11_clean_print_mode_and_handbook_dialog (tests.test_geometry_invariants.TestGeometryInvariants.test_11_clean_print_mode_and_handbook_dialog) ... ok
test_12_dpapi_keystore_and_downloader_sha256 (tests.test_geometry_invariants.TestGeometryInvariants.test_12_dpapi_keystore_and_downloader_sha256) ... ok
test_13_dpapi_fail_soft_on_corrupt_or_foreign_key (tests.test_geometry_invariants.TestGeometryInvariants.test_13_dpapi_fail_soft_on_corrupt_or_foreign_key) ... ok
test_14_exact_right_triangle_float_coordinates_no_spurious_annotation (tests.test_geometry_invariants.TestGeometryInvariants.test_14_exact_right_triangle_float_coordinates_no_spurious_annotation) ... ok
test_15_float_near_right_and_near_right_isosceles_annotation (tests.test_geometry_invariants.TestGeometryInvariants.test_15_float_near_right_and_near_right_isosceles_annotation) ... ok
test_16_dpapi_stress_round_trip_stability (tests.test_geometry_invariants.TestGeometryInvariants.test_16_dpapi_stress_round_trip_stability) ... ok
test_17_freehand_point_origin_flag_rejection (tests.test_geometry_invariants.TestGeometryInvariants.test_17_freehand_point_origin_flag_rejection) ... ok
test_18_format_radical_len_direct_unit_tests (tests.test_geometry_invariants.TestGeometryInvariants.test_18_format_radical_len_direct_unit_tests) ... ok
test_19_ellipse_near_degenerate_a_approx_c (tests.test_geometry_invariants.TestGeometryInvariants.test_19_ellipse_near_degenerate_a_approx_c) ... ok
test_20_hf_downloader_error_paths_comprehensive (tests.test_geometry_invariants.TestGeometryInvariants.test_20_hf_downloader_error_paths_comprehensive) ... ok
test_21_mixed_point_origin_flag_behavior (tests.test_geometry_invariants.TestGeometryInvariants.test_21_mixed_point_origin_flag_behavior) ... ok
test_22_missing_coordinate_validation (tests.test_geometry_invariants.TestGeometryInvariants.test_22_missing_coordinate_validation) ... ok
test_23_micro_scale_invariance_scale_10_minus_5 (tests.test_geometry_invariants.TestGeometryInvariants.test_23_micro_scale_invariance_scale_10_minus_5) ... ok
test_24_gui_canvas_point_source_and_invariants_integration (tests.test_geometry_invariants.TestGeometryInvariants.test_24_gui_canvas_point_source_and_invariants_integration) ... ok
test_25_gui_canvas_drag_typed_and_midpoint_parents_integration (tests.test_geometry_invariants.TestGeometryInvariants.test_25_gui_canvas_drag_typed_and_midpoint_parents_integration) ... ok
test_26_nested_constructions_multi_level_taint (tests.test_geometry_invariants.TestGeometryInvariants.test_26_nested_constructions_multi_level_taint) ... ok
test_27_none_and_string_and_invalid_type_rejection (tests.test_geometry_invariants.TestGeometryInvariants.test_27_none_and_string_and_invalid_type_rejection) ... ok
test_28_drag_with_snap_on_snaps_absolute_coordinates (tests.test_geometry_invariants.TestGeometryInvariants.test_28_drag_with_snap_on_snaps_absolute_coordinates) ... ok
test_29_cycle_guard_and_memoization_point_flag (tests.test_geometry_invariants.TestGeometryInvariants.test_29_cycle_guard_and_memoization_point_flag) ... ok
test_30_undo_redo_parent_taint_propagation (tests.test_geometry_invariants.TestGeometryInvariants.test_30_undo_redo_parent_taint_propagation) ... ok
test_31_permutation_invariance_all_six_orderings (tests.test_geometry_invariants.TestGeometryInvariants.test_31_permutation_invariance_all_six_orderings) ... ok
test_32_drag_derived_point_then_drag_parent (tests.test_geometry_invariants.TestGeometryInvariants.test_32_drag_derived_point_then_drag_parent) ... ok
test_33_undo_redo_segment_rebinding (tests.test_geometry_invariants.TestGeometryInvariants.test_33_undo_redo_segment_rebinding) ... ok
test_34_derived_constraints_taint_propagation (tests.test_geometry_invariants.TestGeometryInvariants.test_34_derived_constraints_taint_propagation) ... ok
test_35_non_transitive_tolerance_permutation_invariance (tests.test_geometry_invariants.TestGeometryInvariants.test_35_non_transitive_tolerance_permutation_invariance) ... ok

----------------------------------------------------------------------
Ran 35 tests in 10.826s

OK
```

### 5.3. Unified Test Discovery Pass (`python -m unittest discover tests`)
```
Ran 62 tests in 17.060s

OK
```

### 5.4. Full Sensitivity Benchmark & Invariants Suite (`python scripts/sensitivity_benchmark.py --all`)
```
=== GeoSolver 2D Benchmark (tol_rel = 0.006, Seed = 42) ===
Triangle Class | Ground Truth | True Positive (TP) | Recall (%) | Precision (%) | F1-Score (%)
---------------|:------------:|:------------------:|:----------:|:-------------:|:------------:
Equilateral    |          250 |                205 |      82.0% |        100.0% |        90.1%
Isosceles      |          250 |                212 |      84.8% |         82.5% |        83.6%
Right          |          250 |                247 |      98.8% |        100.0% |        99.4%
Scalene        |          250 |                250 |     100.0% |         85.9% |        92.4%
Overall Dataset|         1000 |                914 |      91.4% |         91.4% |        91.4%

=== Standard Dataset Sensitivity Sweep ===
tol_rel | Overall | Eq Rec | Eq Prec | Iso Rec | Iso Prec | Right Rec | Scalene Prec
--------|---------|--------|---------|---------|----------|-----------|-------------
  0.002 |   62.9% |  15.2% |  100.0% |   37.6% |    35.3% |     98.8% |        55.7%
  0.004 |   77.8% |  47.6% |  100.0% |   64.8% |    56.1% |     98.8% |        72.5%
  0.006 |   91.4% |  82.0% |  100.0% |   84.8% |    82.5% |     98.8% |        85.9%
  0.008 |   96.8% |  92.8% |  100.0% |   95.6% |    93.0% |     98.8% |        94.7%
  0.010 |   98.5% |  97.6% |  100.0% |   97.6% |    97.6% |     98.8% |        96.5%

=== Hard Negatives Stress Test (Near-Boundary Scalene) ===
tol_rel | Near-Iso FP (N=100) | Near-Right FP (N=100) | Total TN (N=200) | Total FP (N=200) | Combined FP (%)
--------|---------------------|-----------------------|------------------|------------------|----------------
  0.002 |                0/100 |                  0/100 |           200/200 |             0/200 |           0.0%
  0.004 |                0/100 |                  0/100 |           200/200 |             0/200 |           0.0%
  0.006 |                0/100 |                  0/100 |           200/200 |             0/200 |           0.0%
  0.008 |                1/100 |                  0/100 |           199/200 |             1/200 |           0.5%
  0.010 |               36/100 |                  0/100 |           164/200 |            36/200 |          18.0%

=== Permutation Invariance & Equivariance Comparison ===
Sample size: 200 near-tie configurations under all 6 permutations
  - Naive Positional Classifier: 200/200 (100.0%) apex-variant outcomes
  - GeoSolver 2D Invariant Kernel: 0/200 (0.0%) apex-variant outcomes

=== Dual-Regime Lattice Exactness Benchmark ===
Test cases on integer lattice Z^2: 4
  - Continuous Tolerance Classifier: 3/4 (75.0%) false-positive equilateral
  - GeoSolver Discrete Lattice Regime: 0/4 (0.0%) false-positive equilateral

=== Decimal Lattice Invariant Sweep (k in {1, 2, 3, 4}) ===
Non-collinear candidate pairs evaluated: 496
  - GeoSolver Discrete Regime Matches: 496/496 (100.0%) exact isosceles
```
