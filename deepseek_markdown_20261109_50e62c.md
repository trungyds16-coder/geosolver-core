# Round 2 Re-Submission Audit Report: CAD Math Studio

## CAS Algebra, Calculus, Matrix & MSIX Packaging — Round 2 Peer Review

**Project:** CAD Math Studio (Pedagogical Mathematical Computation & Oxy Graphing System)  
**Submitted version:** v2.2.0-RC2 (Release Candidate 2)  
**Previous verdict:** REJECT WITH REASONS (Round 1)  
**Audit standard:** Adversarial re-verification of all corrected findings, independent recalculation, and regression inspection of the modified CAS kernel and MSIX configuration.

---

## Final Verdict

**REJECT WITH REASONS — narrower scope.**

The Round 2 submission **correctly resolves** the most critical Round 1 finding (TV-MAT-02 sign error) and **substantially improves** the radical-equation pedagogy, Defensive/Display handling, and numeric safety net.

However, **three Round 1 findings remain partially resolved or unresolved**, and **two new implementation-level defects** are introduced by the Diophantine code and the symbolic-matrix singularity path. The MSIX configuration still **does not provide evidence** of the two blocking items raised in Round 1 (Publisher/Partner Center mapping, multi-scale icon assets).

The Board **does not approve** `APPROVED TO PACKAGE MSIX` at this time. The re-submission is closer to release but requires one more correction cycle on the specific items listed below.

---

## 1. Resolved Round 1 Findings (Verified)

### ✅ TV-MAT-02 — Corrected and Independently Verified

For

$$
A = \begin{bmatrix} 1 & 0 & 2 \\ 2 & -1 & 3 \\ 4 & 1 & 8 \end{bmatrix},
$$

independent recalculation confirms:

$$
\det(A) = 1 \cdot (-8 - 3) - 0 + 2 \cdot (2 + 4) = -11 + 12 = 1.
$$

The adjugate is:

$$
\operatorname{adj}(A)
=
\begin{bmatrix}
-11 & 2 & 2 \\
-4 & 0 & 1 \\
6 & -1 & -1
\end{bmatrix}.
$$

Since $\det(A)=1$, the inverse is exactly the adjugate, which matches the corrected dossier. The Round 1 sign-flip finding is **fully resolved**.

### ✅ TV-ALG-02 — Early Exit Implemented Correctly

For $\sqrt{x-5} = -2$, the new code detects $g_x = -2$ has no free symbols, evaluates $g_{\text{const}} < 0$, and returns `S = ∅` at **Step 1**, before Step 2 is executed. The Round 1 pedagogical inconsistency is **resolved**.

### ✅ Real-Equation Handling, Step Numbering, zoo/nan, Reverse-Substitution Net

- `isinstance(target_eq, sp.Eq)` normalization added.
- Steps are now numbered continuously 1 → 2 → 3 → 4.
- `expr.has(sp.zoo, sp.nan)` returns `'nonreal'` and is excluded early.
- Reverse-substitution safety net at 40-digit precision is present.

These items are **verified as resolved**.

---

## 2. Partially Resolved Findings

### 2.1 Indeterminate Solutions — Better Surfaced, but Still Not Retained in `valid_sols`

**Severity: Medium — partial resolution**

Round 1 required:

> "For the `'unknown'` status, the candidate solution must be **retained by default** and marked as 'pending manual confirmation', rather than silently excluded."

In RC2, the `'unknown'` branch still does **not** append the candidate to `valid_sols`; it continues to append to `indeterminate_sols`:

```python
else:
    indeterminate_sols.append((r, f"g:{s_gx}, f:{s_fx}"))
```

However, RC2 does add an explicit Step 4 reporting block:

```python
if indeterminate_sols:
    steps.append(f"  ==> Chưa thể kết luận đầy đủ: {indeterminate_sols}")
```

**Assessment:** The candidate is no longer silently lost from the step output. This is a meaningful improvement. But the candidate still does **not** appear in `valid_sols`, so any downstream caller that consumes only `valid_sols` will still lose it. The requirement of "retained by default" is only partially satisfied.

**Required correction:** Return a third state (e.g., `pending_sols`) and require the UI layer to render it explicitly, or append the `'unknown'` candidate to `valid_sols` with an `"unverified"` tag.

---

### 2.2 Symbolic-Matrix Singularity — `is_zero` Added, but `None` Case Still Falls Through

**Severity: Medium — partial resolution**

The RC2 code now uses:

```python
if hasattr(detA, "is_zero") and detA.is_zero:
    is_singular = True
elif sp.simplify(detA) == 0:
    is_singular = True
```

This is an improvement over `detA == 0`. **However**, when `detA.is_zero` is `None` and `sp.simplify(detA) != 0`, `is_singular` remains `False` and the code proceeds to:

```python
adjA = A.adjugate()
invA = adjA / detA
```

For a genuinely singular symbolic matrix whose determinant cannot be simplified to zero, this produces a **mathematically invalid inverse** or an exception, with no three-valued guard.

**Required correction:** Add an explicit `None` branch:

```python
if detA.is_zero is None and sp.simplify(detA) != 0:
    return {
        "invertible": None,
        "det": detA,
        "desc": "Singularity undecidable for symbolic matrix."
    }
```

This was the Round 1 requirement and is **not yet satisfied**.

---

### 2.3 Diophantine Solver — Correct for the TV-ALG-03 Case, but Claims Generality It Does Not Deliver

**Severity: High — misleading return status for general systems**

The new function `solve_underdetermined_or_diophantine` is present and does produce `[(2, 3), (5, 1)]` for the TV-ALG-03 case. The 2-variable, 1-equation branch is correct.

However, the function only handles the special case:

```python
if n == 2 and m == 1:
    ...
```

For **all other systems**, `int_sols` remains `[]` and the function returns:

```python
return "FINITE_BOUNDED", int_sols, len(int_sols), out
```

This is **dangerously misleading**: a system with, for example, 3 variables and 2 equations that does have positive-integer solutions will be reported as `"FINITE_BOUNDED"` with zero solutions. A downstream UI that trusts this label will present a false "no solutions" result.

Additional edge-case defects in the 2×1 branch:

1. `a_c = int(A_mat[0, 0])` will raise `TypeError` for symbolic coefficients, and will give a wrong bound for negative `a_c`.
2. The loop `for x_val in range(1, int(c_val / a_c) + 1)` divides by `a_c` **without checking `a_c == 0`**, producing a `ZeroDivisionError` for equations of the form $0x + by = c$.
3. For $a < 0$, `int(c_val / a_c)` is negative, so the range is empty and all positive solutions are missed.
4. `solve_congruence` is imported but never used.

**Required corrections:**

1. Rename or restrict the return status so that `"FINITE_BOUNDED"` is only returned when the system is actually fully solved; otherwise return `"NOT_IMPLEMENTED"` or `"PARTIAL"`.
2. Add explicit guards for `a_c == 0`, `a_c < 0`, and non-integer symbolic coefficients.
3. Either use `solve_congruence` or remove the import.
4. Do not present this function as a general Diophantine solver in the audit dossier; describe it as a **2-variable 1-equation positive-integer enumerator**.

---

## 3. Unresolved Round 1 Findings (Blocking)

### 3.1 MSIX `Publisher` / `PublisherDisplayName` — Still Unverified

**Severity: Blocking**

RC2 reuses the same value:

```xml
Publisher="CN=CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE"
PublisherDisplayName="TLabtool"
```

The submission provides **no evidence** that:

1. `TLabtool` has been reserved as an application name in Partner Center;
2. The Seller ID associated with that reserved name is exactly `CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE`;
3. `Identity Name="TLabtool.CADMathStudio"` maps correctly to the reserved name.

Without this evidence, the Board cannot confirm that Store certification will not fail with "package identity does not match Store registration information."

**Required correction:** Include a Partner Center reservation confirmation (redacted screenshot or export) as part of the audit dossier, or explicitly state that this is a release-time gate to be verified by the release manager.

---

### 3.2 Multi-Scale Icon Assets — Still Not Addressed

**Severity: Blocking**

The Round 1 finding required:

> "Ensure `Assets/` contains: `StoreLogo.png` (50×50), `Square44x44Logo.png` (44×44), `Square150x150Logo.png` (150×150), `Wide310x150Logo.png` (310×150), and the `scale-100/125/150/200/400` variants for each."

RC2 does **not** list the asset directory contents, does **not** add scale qualifiers, and does **not** add a pre-packaging asset-integrity check. The manifest still contains only base filenames:

```xml
<Logo>Assets\StoreLogo.png</Logo>
Square150x150Logo="Assets\Square150x150Logo.png"
Square44x44Logo="Assets\Square44x44Logo.png"
Wide310x150Logo="Assets\Wide310x150Logo.png"
```

There is no evidence that the multi-scale variants exist. `makeappx pack` may pass with only base assets, but Store certification commonly requires the scale variants for correct rendering on high-DPI displays.

**Required correction:** Add one of the following to the dossier:

1. A directory listing of `Assets/` showing all required scale variants and their dimensions; or
2. A pre-packaging asset-check function in `package_msix.py` that verifies presence and dimensions, and blocks `makeappx pack` on failure.

---

### 3.3 Pre-Packaging Asset Integrity Check — Still Absent

Round 1 required the packaging script to validate asset existence and dimensions before `makeappx pack`. RC2 does not add this check. This is a direct continuation of 3.2 and is not satisfied.

---

## 4. New Observations (Not Blocking, but Should Be Noted)

1. **`sp.solve(poly_eq, x)` remains in use.** RC2 did not switch to `sp.solveset(poly_eq, x, domain=sp.S.Reals)`. The polynomial branch is usually safe, but `solveset` is the more defensible choice for a CAS that claims pedagogical rigor. This was a Round 1 recommendation, not a blocking item, and remains a recommendation.

2. **`c = expanded.coeff(rad)`** can return a non-constant expression in pathological cases; the existing `c.free_symbols` guard catches most of them, but the audit does not see a unit test for the case where `rest` contains a fractional-power term with exponent other than `1/2`. This is a low-probability edge case and not a blocking item.

3. **`ProcessorArchitecture="x64"` and `Version="2.2.0.0"`** are valid for Microsoft Store.

4. **`EntryPoint="Windows.FullTrustApplication"`** is redundant on newer Windows 10/11 builds for FullTrust desktop apps but harmless.

---

## 5. Final Verdict and Gate Conditions

| Category | Finding | Round 1 Status | RC2 Status | Gate Condition |
|:---|:---|:---:|:---:|:---|
| CAS | TV-MAT-02 sign error | Blocking | **Resolved** ✅ | — |
| CAS | TV-ALG-02 early exit | Medium | **Resolved** ✅ | — |
| CAS | Step numbering, `sp.Eq`, zoo/nan, reverse-substitution net | Medium | **Resolved** ✅ | — |
| CAS | `indeterminate_sols` silent loss | High | **Partially resolved** ⚠️ | Return a `pending_sols` state and require UI to render it |
| CAS | Diophantine general-case handling | High | **Partially resolved** ⚠️ | Restrict status label; guard `a_c==0`, `a_c<0`, symbolic coefficients |
| Matrix | Symbolic-matrix `is_zero=None` fallthrough | Medium | **Partially resolved** ⚠️ | Return `invertible: None` for undecidable symbolic determinants |
| MSIX | Publisher/Partner Center mapping | Blocking | **Unverified** ❌ | Provide Partner Center reservation evidence |
| MSIX | Multi-scale icon assets | Blocking | **Unresolved** ❌ | Provide asset inventory or pre-packaging checker |
| MSIX | Pre-packaging asset integrity check | Blocking | **Unresolved** ❌ | Add check and block pack on failure |

### Gate Decision

**REJECT WITH REASONS — narrower scope.**

The Round 2 submission represents substantial progress and **resolves the most severe mathematical error** (TV-MAT-02) and the most visible pedagogical inconsistency (TV-ALG-02). The remaining defects are narrower and more tractable:

- **Two blocking MSIX items** (Publisher verification, multi-scale icon assets + pre-packaging integrity check) are **unresolved** and must be addressed before any Store submission.
- **Three partial fixes** (indeterminate solutions, Diophantine general case, symbolic-matrix `None` case) should be closed out in the same correction cycle to avoid a third round.

Once the three gate conditions in the table above are satisfied, the Board will re-audit **only the affected modules** — the CAS kernel, `compute_matrix_inverse`, and the MSIX packaging script. A full re-audit is not required.

---

## Appendix A: Corrected TV-MAT-02 Values (RC2 Confirmation)

For

$$
A = \begin{bmatrix} 1 & 0 & 2 \\ 2 & -1 & 3 \\ 4 & 1 & 8 \end{bmatrix},
$$

the independently verified values are:

$$
\det(A) = 1,
$$

$$
\operatorname{adj}(A)
=
\begin{bmatrix}
-11 & 2 & 2 \\
-4 & 0 & 1 \\
6 & -1 & -1
\end{bmatrix},
$$

$$
A^{-1}
=
\begin{bmatrix}
-11 & 2 & 2 \\
-4 & 0 & 1 \\
6 & -1 & -1
\end{bmatrix}.
$$

RC2 matches these values exactly. The Round 1 finding is closed.

---

## Appendix B: Required Code Changes Summary

```python
# 1. Indeterminate solutions: retain as pending
pending_sols = []
# in the 'unknown' branch:
pending_sols.append(r)
# return pending_sols alongside valid_sols

# 2. Symbolic-matrix singularity: three-valued guard
if detA.is_zero is None and sp.simplify(detA) != 0:
    return {"invertible": None, "det": detA,
            "desc": "Singularity undecidable for symbolic matrix."}

# 3. Diophantine status: do not claim FINITE_BOUNDED unless fully solved
if n != 2 or m != 1:
    return "NOT_IMPLEMENTED", [], 0, out
if a_c == 0 or a_c < 0:
    return "EDGE_CASE_UNSUPPORTED", [], 0, out
```

---

## Appendix C: Required MSIX Additions

1. Partner Center reservation evidence for `TLabtool` and `CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE`.
2. `Assets/` inventory proving scale-100/125/150/200/400 variants for all four base icons.
3. Pre-packaging checker in `package_msix.py` that raises on missing or dimensionally invalid assets **before** `makeappx pack`.