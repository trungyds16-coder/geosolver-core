# COVER LETTER FOR SUBMISSION TO SOFTWARX

**To:**  
The Editors-in-Chief  
*SoftwareX*  
Elsevier

**Date:** November 15, 2026  
**Subject:** Submission of Original Software Publication: "GeoSolver 2D: A Provenance-Aware Dynamic Geometry Engine with Dual-Regime and Permutation-Invariant Classification"

Dear Editors,

I am pleased to submit our original software manuscript titled **"GeoSolver 2D: A Provenance-Aware Dynamic Geometry Engine with Dual-Regime and Permutation-Invariant Classification"** for consideration as an **Original Software Publication (OSP)** in *SoftwareX*.

### Context and Motivation
Dynamic Geometry Systems (DGS) are essential tools in mathematics education, CAD, and geometric modeling. However, interactive canvas gestures introduce floating-point perturbations that interact poorly with heuristic relative tolerance checks. This design produces two prevalent failure modes: (1) false-positive classifications on integer-lattice triangles (provably violating Gauss area rational constraints); and (2) permutation-dependent classifications (where the recognized shape or apex varies depending on vertex enumeration order).

### Software Contribution & Scientific Rigor
GeoSolver 2D resolves these issues through a lightweight, mathematically verified architecture:
1. **Dynamic Taint Tracking Engine:** Employs an iterative topological traversal with explicit stack safety and cycle detection, guaranteeing strictly linear $O(V+E)$ traversal complexity on acyclic construction graphs.
2. **Dual-Regime Partitioning:** Distinguishes between exact integer lattices ($\mathbb{Z}^2$) and continuous floating-point approximations via the `as_scaled_ints` kernel.
3. **Specificity-Ordered Classification:** Enforces an invariant hypothesis hierarchy operating on scale-normalized edge lengths and cosine predicates, guaranteeing bitwise permutation invariance and apex equivariance.

### Verification and Software Availability
- **Test Suite:** 62 automated unit tests (27 headless CI tests + 35 GUI integration tests, 100% PASS).
- **Benchmark Suite:** Fully reproducible synthetic sensitivity benchmarks achieving 91.4% accuracy on canonical prototypes and 0% false positives on integer-lattice triples.
- **Dependencies:** Pure Python 3.10+ standard library with zero external compilation requirements.
- **Repository:** `https://github.com/trungyds16-coder/geosolver-core` (Release tag: `v3.2.1`).
- **Persistent Identifier (DOI):** `10.5281/zenodo.24249595` (Open access under GNU GPLv3).

This manuscript has not been published previously and is not under consideration for publication elsewhere. All authors have approved the submission.

Thank you very much for your time and consideration of our work.

Sincerely,

**Bao-Trung Nguyen**  
Independent Researcher  
Ho Chi Minh City, Vietnam  
Email: `trungyds16@gmail.com`  
ORCID: `https://orcid.org/0009-0009-5780-3385`
