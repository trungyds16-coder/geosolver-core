# MASTER AUDIT & REBUTTAL SESSION LOG
## PROJECT: GEOSOLVER 2D (DYNAMIC GEOMETRY & PROVENANCE KERNEL)
### CONTINUOUS REVISION LEDGER ACROSS AUDIT ROUNDS & AI SESSIONS

> **Document Status:** Active Persistent Ledger  
> **Repository Baseline:** `D:\AI DATA\STEM_APP`  
> **Source Commit:** `177ad96c894d6a189809cf252beef057863df569` (`v3.2.0`)  
> **Target Journal:** Elsevier *SoftwareX* (SCIE / Scopus Q2)  
> **Last Updated:** November 15, 2026 (Local Time: 19:32:00 UTC+7)

---

## CONTEXT RECOVERY INSTRUCTIONS FOR NEW SESSIONS

> [!IMPORTANT]
> **HOW TO RESUME FROM A NEW AI SESSION WITHOUT REPEATING:**
> 1. Read this master document (`docs/audit_reports/MASTER_AUDIT_AND_REBUTTAL_SESSION_LOG.md`).
> 2. Read the latest finalized manuscript: `docs/audit_reports/GEOSOLVER_2D_SOFTWARX_MANUSCRIPT_FINAL.md`.
> 3. Read the complete single submission bundle: `docs/audit_reports/CLAUDE_FINAL_SUBMISSION_BUNDLE.md`.
> 4. Do not re-litigate Sessions 1–13.

---

## INDEX OF NUMBERED SESSIONS

- **Session 01–05 (Historical):** Initial exploratory architecture, SymPy wrapping, initial desktop GUI. Discarded early naive assumptions.
- **Session 06 (Compact Acceptance):** Separation of pure math classification functions from Tkinter GUI.
- **Session 07 (Experimental Audit):** Introduction of Ramanujan-II ellipse formula ($0.040\%$ max error) and WCAG 2.1 AA luminance contrast calculations.
- **Session 08 (RC2 Self-Evaluation):** Independent unit test separation; eliminating mocked tests.
- **Session 09 (Taint Tracking & Provenance):** First formal introduction of the Taint Conservation Law and input boundary validation (11 tests).
- **Session 10 (RC2 Consolidation):** Resolving Taint Washing during snapped canvas drag and cycle-guarded traversal.
- **Session 11 (Unified RC5 Release Dossier):** Single MSIX package creation, Authenticode signature verification, 46/46 automated unit tests passing.
- **Session 12 (SoftwareX Deep Peer Review - Major Revision):** Decoupling CAD Math / 3D to focus 100% on GeoSolver 2D.
- **Session 13 (SoftwareX Refinement - Minor-to-Moderate Revisions):** Fixes to Invariance Proof via sorted lengths $s_{(1)} \le s_{(2)} \le s_{(3)}$.
- **Session 14 (SoftwareX Gating Item Resolution):**
  - Resolved Gating Item 2.1 by embedding the complete verbatim production code and raw test logs directly into the submission package.
  - Resolved Gating Item 2.2 by completely removing all unsubstantiated GeoGebra benchmark claims and replacing with an empirical parameter sensitivity table.
  - Added dedicated *Impact* Section (§5), author names/affiliations, and Elsevier AI-use declaration.
  - Created unified submission bundle: `docs/audit_reports/CLAUDE_FINAL_SUBMISSION_BUNDLE.md`.
- **Session 15 (Round 12 v4 Resolution & Standalone Kernel):**
  - Resolved `UnboundLocalError: diff_CA_CB` on discrete lattice triangles.
  - Created initial `geosolver_core/classifier.py` and initial 52-test suite.
- **Session 16 (Round 12 v6 Referee Resolution & Final Benchmark Overhaul):**
  - Evaluated Claude's Round 12 v6 Referee Report ("Accept, conditional on minor revisions").
  - Fixed provenance memo order-dependence when `_depth >= 100` by returning `False` defensively without caching cutoff results into `memo`.
  - Added O(1) construction-time fast-path in `point_provenance_flag(p)` when points already carry evaluated exactness flags.
  - Updated `snap_to_grid` to return Python `int` types when coordinates land on integer grid points.
  - Upgraded §4.1 with a fully reproducible synthetic sensitivity benchmark generator (`scripts/sensitivity_benchmark.py`, seed 42) yielding 91.4% overall accuracy and 100% precision on regular shapes.
  - Expanded test suite to 55 tests: split cleanly into 20 headless core tests (0.003s) and 35 GUI integration tests (9.848s).
  - Added GitHub Actions CI matrix (`.github/workflows/ci.yml`) across Ubuntu/Windows and Python 3.10–3.13.
  - Tagged Git release **`v3.1.0`** (Commit: `069082b8f8f7935032dbb87b0609b55e02f1a304`).
- **Session 17 (Author Profile & Biography Integration):**
  - Integrated real author profile: Bao-Trung Nguyen (Nguyễn Bảo Trung), Independent Researcher, Ho Chi Minh City, Vietnam (`trungyds16@gmail.com`).
  - Added formal *Author Biography* section: Graduated with Pharmacy degree from University of Medicine and Pharmacy at Ho Chi Minh City (2021), 5 years of pharmaceutical R&D experience, currently an independent researcher specializing in scientific software and computational geometry.
  - Synchronized `docs/audit_reports/CLAUDE_FINAL_SUBMISSION_BUNDLE.md`, `GEOSOLVER_2D_SOFTWARX_MANUSCRIPT_FINAL.md`, and workspace artifact.
- **Session 18 (Round 12 v7 Referee Resolution):**
  - Evaluated Claude's Round 12 v7 Referee Report.
  - Fixed Item 2.1 (Taint Washing): Removed flawed O(1) fast path; enforced inductive check order: free/exact=False -> derived-with-parents -> explicit exact. Verified via `test_item_2_1_stale_flag_after_parent_drag`.
  - Fixed Item 2.2 (Order Dependence): Removed artificial depth cutoff (`_depth >= 100`), ensuring full acyclic DAG evaluation with cycle protection via `_visiting`. Verified via `test_item_2_2_parent_order_independence_deep_dag` on depth 110.
  - Overhauled §4.1 Sensitivity Benchmark (`scripts/sensitivity_benchmark.py --all`): Added CLI arguments, reported exact empirical sweep numbers matching Claude's run, removed unsupported "optimal trade-off" claim.
  - Updated CI & Test Partitioning: Moved core permutation tests to headless suite (24 tests in 0.005s; 35 GUI tests in 10.826s; Total 59/59 PASS).
- **Session 19 (Round 12 v8 Resolution):**
  - Resolved Decimal Lattice Float Discrepancy: Evaluated exact scaled integer differences (`d2_AB == d2_AC`) and integer candidate sorting keys.
  - Resolved Stack Safety on Deep Provenance Graphs: Fully replaced recursive traversal with iterative topological DFS using explicit Python stack, supporting 2,000+ deep parent chains with 0 RecursionError.
  - Implemented `run_hard_negatives_benchmark()` and `run_decimal_lattice_sweep()` in `scripts/sensitivity_benchmark.py`.
- **Session 20 (Current — Final Release v3.2.0: Strict O(V+E) Diamond Traversal, Decoupled Negative Families & Frozen Git Tag):**
  - Item 1 (Tag Immutability & Release Freeze): Cut fresh, immutable Git tag **`v3.2.0`** to guarantee a 1:1 frozen snapshot matching the paper and Zenodo archive.
  - Item 2 (Strict O(V+E) Linear DAG Traversal): Added `done` set to iterative topological DFS in `geosolver_core/provenance.py`, eliminating exponential re-expansions across shared ancestors (e.g. iterated midpoints / diamond ladders). At depth 25, traversal time dropped from minutes to 0.00016s. Added `test_diamond_ladder_linear_complexity_depth_25` to unit test suite.
  - Item 3 (Hard Negatives Decoupling & Transparency): Separated Near-Isosceles ($N=100$) and Near-Right ($N=100$) families in `scripts/sensitivity_benchmark.py` and manuscript. Dropped phrase "direct empirical justification"; explicitly documented that Near-Iso false positives reflect the synthesized $0.8\% - 1.5\%$ mismatch band, while Near-Right remains 0/100 FP across all $\text{tol\_rel}$ due to the decoupled fixed cosine bound ($|\cos \theta| \le 0.015$).
  - Item 4 (Repository & Zenodo Verification): Addressed public GitHub visibility and Zenodo persistent identifier archive synchronization for the frozen release `v3.2.0`.
  - Minor Edits: Reconciled full-suite discovery execution time (17.060s in `unittest discover` vs 0.019s headless + 10.826s isolated GUI); reformulated Theorem 1 continuous-regime claim as winner uniqueness; replaced vague "zero regression" in abstract with concrete mathematical invariance and $O(V+E)$ complexity guarantees.
  - Verified Test Suite: **62 / 62 Tests PASS** (27 headless CI in 0.019s + 35 GUI integration). All benchmarks reproduce exactly.
  - Fully regenerated master submission package in `docs/audit_reports/CLAUDE_FINAL_SUBMISSION_BUNDLE.md`.

---

## 3. MASTER DOCUMENTATION POINTERS
- **Single Master Submission Bundle:** [`docs/audit_reports/CLAUDE_FINAL_SUBMISSION_BUNDLE.md`](file:///D:/AI%20DATA/STEM_APP/docs/audit_reports/CLAUDE_FINAL_SUBMISSION_BUNDLE.md)
- **Finalized Manuscript:** [`docs/audit_reports/GEOSOLVER_2D_SOFTWARX_MANUSCRIPT_FINAL.md`](file:///D:/AI%20DATA/STEM_APP/docs/audit_reports/GEOSOLVER_2D_SOFTWARX_MANUSCRIPT_FINAL.md)
- **Author Rebuttal Archive:** [`docs/audit_reports/12_AUTHOR_REBUTTAL_AND_POINT_BY_POINT_RESPONSE.md`](file:///D:/AI%20DATA/STEM_APP/docs/audit_reports/12_AUTHOR_REBUTTAL_AND_POINT_BY_POINT_RESPONSE.md)
