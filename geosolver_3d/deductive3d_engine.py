# -*- coding: utf-8 -*-
"""
================================================================================
MODULE: geosolver_3d.deductive3d_engine
TARGET PATH: D:\\AI DATA\\STEM_APP\\geosolver_3d\\deductive3d_engine.py
COMPATIBILITY: Python 3.10+ / 3.14
DESCRIPTION:
    Step-by-step Pedagogical Deductive Proof Engine for 3D Spatial & Spherical
    Geometry (VN GDPT 2018 + SAT / AP Calculus / IB HL / Gaokao).
    Supports exact symbolic algebra via SymPy, bilingual (Vietnamese & English)
    pedagogical reasoning, and Win32/CAD-ready LaTeX formula rendering.
================================================================================
"""

from __future__ import annotations

import math
import re
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import sympy as sp

# ==============================================================================
# KERNEL IMPORT WITH SELF-CONTAINED FALLBACK FOR STANDALONE EXECUTION
# ==============================================================================
try:
    from geosolver_3d.geometry3d_kernel import (
        Plane3D,
        Point3D,
        Sphere3D,
        Vector3D,
    )
except ImportError:

    @dataclass(frozen=True)
    class Point3D:
        """3D Cartesian Point representation."""
        x: float
        y: float
        z: float
        name: str = "P"

        def to_tuple(self) -> Tuple[float, float, float]:
            return (float(self.x), float(self.y), float(self.z))

        def to_sympy(self) -> Tuple[sp.Expr, sp.Expr, sp.Expr]:
            return (sp.nsimplify(self.x), sp.nsimplify(self.y), sp.nsimplify(self.z))

        def distance_to(self, other: "Point3D") -> float:
            return math.sqrt(
                (self.x - other.x) ** 2
                + (self.y - other.y) ** 2
                + (self.z - other.z) ** 2
            )

    @dataclass(frozen=True)
    class Vector3D:
        """3D Spatial Vector representation."""
        x: float
        y: float
        z: float

        @classmethod
        def from_points(cls, start: Point3D, end: Point3D) -> "Vector3D":
            return cls(end.x - start.x, end.y - start.y, end.z - start.z)

        def to_tuple(self) -> Tuple[float, float, float]:
            return (float(self.x), float(self.y), float(self.z))

        def to_sympy_matrix(self) -> sp.Matrix:
            return sp.Matrix([
                sp.nsimplify(self.x),
                sp.nsimplify(self.y),
                sp.nsimplify(self.z),
            ])

        def dot(self, other: "Vector3D") -> float:
            return float(self.x * other.x + self.y * other.y + self.z * other.z)

        def cross(self, other: "Vector3D") -> "Vector3D":
            return Vector3D(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
            )

        def norm(self) -> float:
            return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

        def is_zero(self, tol: float = 1e-12) -> bool:
            return self.norm() <= tol

    @dataclass(frozen=True)
    class Plane3D:
        """3D Plane in general form: A*x + B*y + C*z + D = 0."""
        A: float
        B: float
        C: float
        D: float
        name: str = "(P)"

        def __post_init__(self) -> None:
            if math.sqrt(self.A ** 2 + self.B ** 2 + self.C ** 2) <= 1e-12:
                raise ValueError(
                    "Lỗi hình học / Geometry Error: Pháp tuyến mặt phẳng không được bằng vector không "
                    "(Plane normal vector cannot be zero vector)."
                )

        @property
        def normal(self) -> Vector3D:
            return Vector3D(self.A, self.B, self.C)

        def distance_to_point(self, pt: Point3D) -> float:
            num = abs(self.A * pt.x + self.B * pt.y + self.C * pt.z + self.D)
            den = math.sqrt(self.A ** 2 + self.B ** 2 + self.C ** 2)
            return num / den

    @dataclass(frozen=True)
    class Sphere3D:
        """3D Sphere with center I(x0, y0, z0) and radius R > 0."""
        center: Point3D
        radius: float
        name: str = "(S)"

        def __post_init__(self) -> None:
            if self.radius <= 0:
                raise ValueError(
                    "Lỗi hình học / Geometry Error: Bán kính mặt cầu phải dương (Sphere radius must be > 0)."
                )


# ==============================================================================
# CUSTOM PEDAGOGICAL EXCEPTION
# ==============================================================================
class PedagogicalGeometryError(ValueError):
    """
    Structured bilingual exception for invalid, degenerate, or out-of-domain
    3D geometric configurations.
    """

    def __init__(self, message_vi: str, message_en: str, error_code: str = "GEO3D_ERR") -> None:
        self.message_vi = message_vi
        self.message_en = message_en
        self.error_code = error_code
        super().__init__(f"[{error_code}] VI: {message_vi} | EN: {message_en}")


# ==============================================================================
# 1. CẤU TRÚC DỮ LIỆU SƯ PHẠM (PEDAGOGICAL SCHEMA)
# ==============================================================================
@dataclass
class ProofStep:
    """
    Represents a single deductive step in a bilingual geometric proof.
    Designed for direct rendering in Win32 / CAD / LaTeX educational views.
    """
    step_number: int
    title_vi: str
    title_en: str
    statement_vi: str
    statement_en: str
    latex_formula: str
    math_reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return OrderedDict([
            ("step_number", self.step_number),
            ("title_vi", self.title_vi),
            ("title_en", self.title_en),
            ("statement_vi", self.statement_vi),
            ("statement_en", self.statement_en),
            ("latex_formula", self.latex_formula),
            ("math_reasons", list(self.math_reasons)),
        ])


@dataclass
class DeductiveProofResult:
    """
    Encapsulates a complete step-by-step 3D deductive proof, including exact
    SymPy symbolic results, floating-point evaluations, and auxiliary metadata.
    """
    problem_id: str
    topic: str
    steps: List[ProofStep]
    symbolic_result: sp.Expr
    numeric_value: float
    unit: str
    conclusion_vi: str
    conclusion_en: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return OrderedDict([
            ("problem_id", self.problem_id),
            ("topic", self.topic),
            ("steps", [step.to_dict() for step in self.steps]),
            ("symbolic_result", str(self.symbolic_result)),
            ("symbolic_latex", sp.latex(self.symbolic_result)),
            ("numeric_value", float(self.numeric_value)),
            ("unit", self.unit),
            ("conclusion_vi", self.conclusion_vi),
            ("conclusion_en", self.conclusion_en),
            ("metadata", self.metadata),
        ])


# ==============================================================================
# 5. CLASS ĐIỀU PHỐI CHÍNH: Deductive3DEngine
# ==============================================================================
class Deductive3DEngine:
    """
    Master Deductive Reasoning & Step-by-Step Proof Engine for 3D Geometry.
    Covers Vietnamese GDPT 2018 (Grades 11-12) and International Curricula
    (SAT Math Level 2, AP Calculus AB/BC, IB Mathematics AA HL, Gaokao).
    """

    EPSILON: float = 1e-10

    def __init__(self, precision: int = 6) -> None:
        self.precision = precision

    # --------------------------------------------------------------------------
    # INTERNAL VALIDATION & SYMBOLIC HELPERS
    # --------------------------------------------------------------------------
    @staticmethod
    def _to_sym(value: Union[int, float, sp.Expr]) -> sp.Expr:
        """Converts numeric input to an exact SymPy expression where possible."""
        if isinstance(value, sp.Expr):
            return value
        return sp.nsimplify(value, rational=True, tolerance=1e-10)

    @classmethod
    def _require_positive(cls, value: Union[int, float, sp.Expr], name_vi: str, name_en: str) -> sp.Expr:
        """Validates that a geometric measure is strictly positive."""
        val_float = float(value)
        if math.isnan(val_float) or math.isinf(val_float) or val_float <= cls.EPSILON:
            raise PedagogicalGeometryError(
                f"Đại lượng '{name_vi}' phải là số thực dương lớn hơn 0 (nhận giá trị: {value}).",
                f"Quantity '{name_en}' must be a strictly positive real number (got: {value}).",
                error_code="ERR_NON_POSITIVE_MEASURE",
            )
        return cls._to_sym(value)

    @classmethod
    def _require_non_negative_radicand(
        cls, expr: sp.Expr, context_vi: str, context_en: str
    ) -> sp.Expr:
        """Ensures the expression inside a square root is non-negative."""
        val_float = float(expr.evalf())
        if val_float < -cls.EPSILON:
            raise PedagogicalGeometryError(
                f"Biểu thức dưới dấu căn âm ({val_float:.6f}) trong {context_vi}. Dữ kiện hình học không tồn tại.",
                f"Negative radicand ({val_float:.6f}) encountered in {context_en}. Geometric configuration is impossible.",
                error_code="ERR_NEGATIVE_RADICAND",
            )
        if abs(val_float) <= cls.EPSILON:
            return sp.Integer(0)
        return sp.simplify(expr)

    @staticmethod
    def _format_plane_latex(A: sp.Expr, B: sp.Expr, C: sp.Expr, D: sp.Expr) -> str:
        """Formats a 3D linear plane equation Ax + By + Cz + D = 0 into clean LaTeX."""
        x, y, z = sp.symbols("x y z")
        expr = sp.simplify(A * x + B * y + C * z + D)
        return f"{sp.latex(expr)} = 0"

    # ==========================================================================
    # 2a. MẶT CẦU NGOẠI TIẾP (CIRCUMSCRIBED SPHERE)
    # ==========================================================================
    def prove_circumscribed_sphere(
        self,
        case_type: str,
        problem_id: str = "CIRCUM_SPHERE_01",
        **kwargs: Any,
    ) -> DeductiveProofResult:
        """
        Generates a complete deductive proof for the circumscribed sphere radius R.

        Supported `case_type` values:
        1. 'perp_lateral_edge': Pyramid with lateral edge SA perp to base (R = sqrt(R_base^2 + (h/2)^2)).
           Accepts `h` (or `SA`) and either `r_base`, or right-triangle base legs (`ab`, `bc`),
           or general triangle sides (`a`, `b`, `c`).
        2. 'regular_pyramid': Regular pyramid with lateral edge `b` and height `h` (R = b^2 / (2h)),
           or regular tetrahedron with edge `a` (where h = a*sqrt(6)/3, R = a*sqrt(6)/4).
        3. 'right_prism': Right prism with base circumradius `r_base` and height `h`
           (R = sqrt(R_base^2 + (h/2)^2)).
        4. 'rectangular_box': Rectangular cuboid with dimensions `a`, `b`, `c`
           (R = sqrt(a^2 + b^2 + c^2) / 2).
        5. 'orthogonal_tetrahedron': Tri-rectangular tetrahedron O.ABC with mutually perpendicular
           edges `oa`, `ob`, `oc` at vertex O (R = sqrt(OA^2 + OB^2 + OC^2) / 2).
        6. 'dispisphenoid' / 'isoceles_tetrahedron': Equifacial (almost-regular) tetrahedron
           with opposite edge pairs `a`, `b`, `c` (R = sqrt((a^2 + b^2 + c^2) / 8)).
        """
        steps: List[ProofStep] = []
        case_key = case_type.strip().lower()

        if case_key in ("perp_lateral_edge", "right_prism"):
            is_prism = case_key == "right_prism"
            h_raw = kwargs.get("h", kwargs.get("SA", kwargs.get("height")))
            if h_raw is None:
                raise PedagogicalGeometryError(
                    "Thiếu chiều cao h (hoặc cạnh bên vuông góc đáy SA).",
                    "Missing height h (or perpendicular lateral edge SA).",
                    error_code="ERR_MISSING_HEIGHT",
                )
            h_sym = self._require_positive(h_raw, "chiều cao h", "height h")

            # Determine base circumradius R_base
            if "r_base" in kwargs and kwargs["r_base"] is not None:
                r_base_sym = self._require_positive(
                    kwargs["r_base"], "bán kính ngoại tiếp đáy R_đáy", "base circumradius R_base"
                )
                steps.append(
                    ProofStep(
                        step_number=1,
                        title_vi="Xác định bán kính đường tròn ngoại tiếp mặt đáy",
                        title_en="Determine the circumradius of the base polygon",
                        statement_vi=f"Từ giả thiết, mặt đáy nội tiếp đường tròn có bán kính $R_{{\\text{{đáy}}}} = {sp.latex(r_base_sym)}$ và chiều cao $h = {sp.latex(h_sym)}$.",
                        statement_en=f"From the given data, the base is inscribed in a circle of radius $R_{{\\text{{base}}}} = {sp.latex(r_base_sym)}$ and altitude $h = {sp.latex(h_sym)}$.",
                        latex_formula=f"R_{{\\text{{base}}}} = {sp.latex(r_base_sym)}, \\quad h = {sp.latex(h_sym)}",
                        math_reasons=[
                            "Định nghĩa đường tròn ngoại tiếp đa giác đáy / Definition of base circumcircle"
                        ],
                    )
                )
            elif "ab" in kwargs and "bc" in kwargs:
                ab_sym = self._require_positive(kwargs["ab"], "cạnh góc vuông AB", "leg AB")
                bc_sym = self._require_positive(kwargs["bc"], "cạnh góc vuông BC", "leg BC")
                ac_sym = sp.sqrt(ab_sym ** 2 + bc_sym ** 2)
                r_base_sym = sp.simplify(ac_sym / 2)
                steps.append(
                    ProofStep(
                        step_number=1,
                        title_vi="Tính bán kính ngoại tiếp đáy tam giác vuông",
                        title_en="Compute circumradius of the right-angled triangular base",
                        statement_vi=(
                            f"Tam giác $ABC$ vuông tại $B$ có $AB = {sp.latex(ab_sym)}, BC = {sp.latex(bc_sym)}$. "
                            f"Theo định lý Pythagore, cạnh huyền $AC = \\sqrt{{AB^2 + BC^2}} = {sp.latex(ac_sym)}$. "
                            f"Tâm đường tròn ngoại tiếp đáy là trung điểm cạnh huyền $AC$ nên $R_{{\\text{{đáy}}}} = \\frac{{AC}}{{2}} = {sp.latex(r_base_sym)}$."
                        ),
                        statement_en=(
                            f"Right triangle $ABC$ at $B$ has legs $AB = {sp.latex(ab_sym)}, BC = {sp.latex(bc_sym)}$. "
                            f"By the Pythagorean theorem, hypotenuse $AC = \\sqrt{{AB^2 + BC^2}} = {sp.latex(ac_sym)}$. "
                            f"The circumcenter is the midpoint of hypotenuse $AC$, so $R_{{\\text{{base}}}} = \\frac{{AC}}{{2}} = {sp.latex(r_base_sym)}$."
                        ),
                        latex_formula=(
                            f"R_{{\\text{{base}}}} = \\frac{{AC}}{{2}} = \\frac{{\\sqrt{{AB^2 + BC^2}}}}{{2}} "
                            f"= \\frac{{\\sqrt{{{sp.latex(ab_sym)}^2 + {sp.latex(bc_sym)}^2}}}}{{2}} = {sp.latex(r_base_sym)}"
                        ),
                        math_reasons=[
                            "Định lý Pythagore trong tam giác vuông / Pythagorean Theorem",
                            "Tâm ngoại tiếp tam giác vuông là trung điểm cạnh huyền / Circumcenter of right triangle is hypotenuse midpoint",
                        ],
                    )
                )
            else:
                raise PedagogicalGeometryError(
                    "Cần cung cấp 'r_base' hoặc hai cạnh góc vuông đáy ('ab', 'bc').",
                    "Must provide either 'r_base' or right-triangle base legs ('ab', 'bc').",
                    error_code="ERR_MISSING_BASE_DATA",
                )

            R_sym = sp.simplify(sp.sqrt(r_base_sym ** 2 + (h_sym / 2) ** 2))
            solid_name_vi = "hình lăng trụ đứng" if is_prism else "hình chóp có cạnh bên vuông góc với đáy"
            solid_name_en = "right prism" if is_prism else "pyramid with lateral edge perpendicular to base"

            steps.append(
                ProofStep(
                    step_number=2,
                    title_vi="Xác định tâm mặt cầu ngoại tiếp bằng trục đường tròn đáy",
                    title_en="Locate circumsphere center via the base circumcircle axis",
                    statement_vi=(
                        f"Gọi $O$ là tâm đường tròn ngoại tiếp đáy và $d$ là trục của đường tròn ngoại tiếp đáy ($d \\perp (\\text{{đáy}})$ tại $O$). "
                        f"Trong mặt phẳng chứa cạnh bên vuông góc đáy và trục $d$, mặt phẳng trung trực của chiều cao $h$ cắt $d$ tại tâm mặt cầu $I$, cách mặt đáy một khoảng $\\frac{{h}}{{2}} = {sp.latex(h_sym / 2)}$."
                    ),
                    statement_en=(
                        f"Let $O$ be the base circumcenter and $d$ be the axis perpendicular to the base at $O$. "
                        f"The perpendicular bisector plane of altitude $h$ intersects $d$ at circumcenter $I$, located at distance $\\frac{{h}}{{2}} = {sp.latex(h_sym / 2)}$ from the base."
                    ),
                    latex_formula=f"OI = \\frac{{h}}{{2}} = {sp.latex(sp.simplify(h_sym / 2))}",
                    math_reasons=[
                        "Tính chất trục đường tròn ngoại tiếp đáy / Property of base circumcircle axis",
                        "Tính chất mặt phẳng trung trực của đoạn thẳng / Perpendicular bisector plane theorem",
                    ],
                )
            )

            steps.append(
                ProofStep(
                    step_number=3,
                    title_vi=f"Tính bán kính mặt cầu ngoại tiếp {solid_name_vi}",
                    title_en=f"Calculate circumsphere radius of the {solid_name_en}",
                    statement_vi=(
                        f"Áp dụng định lý Pythagore trong tam giác vuông tạo bởi tâm $I$, tâm đáy $O$ và một đỉnh đáy, "
                        f"ta thu được bán kính mặt cầu ngoại tiếp $R = \\sqrt{{R_{{\\text{{đáy}}}}^2 + \\left(\\frac{{h}}{{2}}\\right)^2}} = {sp.latex(R_sym)}$."
                    ),
                    statement_en=(
                        f"Applying the Pythagorean theorem to the right triangle formed by circumcenter $I$, base center $O$, and a base vertex "
                        f"yields $R = \\sqrt{{R_{{\\text{{base}}}}^2 + \\left(\\frac{{h}}{{2}}\\right)^2}} = {sp.latex(R_sym)}$."
                    ),
                    latex_formula=(
                        f"R = \\sqrt{{R_{{\\text{{base}}}}^2 + \\left(\\frac{{h}}{{2}}\\right)^2}} "
                        f"= \\sqrt{{\\left({sp.latex(r_base_sym)}\\right)^2 + \\left(\\frac{{{sp.latex(h_sym)}}}{{2}}\\right)^2}} = {sp.latex(R_sym)}"
                    ),
                    math_reasons=["Định lý Pythagore không gian / 3D Pythagorean Theorem"],
                )
            )

            R_num = float(R_sym.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Circumscribed Sphere - Perpendicular Lateral Edge / Right Prism",
                steps=steps,
                symbolic_result=R_sym,
                numeric_value=R_num,
                unit="length",
                conclusion_vi=f"Bán kính mặt cầu ngoại tiếp {solid_name_vi} là R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
                conclusion_en=f"The circumscribed sphere radius of the {solid_name_en} is R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
                metadata={"r_base": float(r_base_sym.evalf()), "h": float(h_sym.evalf())},
            )

        elif case_key in ("regular_pyramid", "regular_tetrahedron"):
            if case_key == "regular_tetrahedron" or ("a" in kwargs and "b" not in kwargs and "h" not in kwargs):
                a_sym = self._require_positive(kwargs.get("a"), "cạnh tứ diện đều a", "regular tetrahedron edge a")
                b_sym = a_sym
                r_base_sym = sp.simplify(a_sym * sp.sqrt(3) / 3)
                h_sym = sp.simplify(sp.sqrt(b_sym ** 2 - r_base_sym ** 2))
                steps.append(
                    ProofStep(
                        step_number=1,
                        title_vi="Xác định bán kính ngoại tiếp đáy và chiều cao tứ diện đều",
                        title_en="Determine base circumradius and altitude of the regular tetrahedron",
                        statement_vi=(
                            f"Tứ diện đều cạnh $a = {sp.latex(a_sym)}$ có đáy là tam giác đều cạnh $a$, "
                            f"bán kính ngoại tiếp đáy $R_{{\\text{{đáy}}}} = \\frac{{a\\sqrt{{3}}}}{{3}} = {sp.latex(r_base_sym)}$ "
                            f"và chiều cao $h = \\sqrt{{a^2 - R_{{\\text{{đáy}}}}^2}} = \\frac{{a\\sqrt{{6}}}}{{3}} = {sp.latex(h_sym)}$."
                        ),
                        statement_en=(
                            f"A regular tetrahedron with edge $a = {sp.latex(a_sym)}$ has an equilateral triangle base with "
                            f"$R_{{\\text{{base}}}} = \\frac{{a\\sqrt{{3}}}}{{3}} = {sp.latex(r_base_sym)}$ "
                            f"and altitude $h = \\sqrt{{a^2 - R_{{\\text{{base}}}}^2}} = \\frac{{a\\sqrt{{6}}}}{{3}} = {sp.latex(h_sym)}$."
                        ),
                        latex_formula=(
                            f"R_{{\\text{{base}}}} = \\frac{{a\\sqrt{{3}}}}{{3}} = {sp.latex(r_base_sym)}, \\quad "
                            f"h = \\frac{{a\\sqrt{{6}}}}{{3}} = {sp.latex(h_sym)}"
                        ),
                        math_reasons=[
                            "Hệ thức lượng trong tam giác đều / Metric relations in an equilateral triangle",
                            "Định lý Pythagore cho đường cao hình chóp đều / Pythagorean theorem for regular pyramid altitude",
                        ],
                    )
                )
            else:
                b_sym = self._require_positive(kwargs.get("b"), "cạnh bên b", "lateral edge b")
                h_sym = self._require_positive(kwargs.get("h"), "chiều cao h", "altitude h")
                if float(b_sym.evalf()) <= float(h_sym.evalf()) + self.EPSILON:
                    raise PedagogicalGeometryError(
                        f"Cạnh bên b ({b_sym}) phải lớn hơn chiều cao h ({h_sym}) trong hình chóp đều.",
                        f"Lateral edge b ({b_sym}) must strictly exceed altitude h ({h_sym}) in a regular pyramid.",
                        error_code="ERR_INVALID_PYRAMID_DIMENSIONS",
                    )
                steps.append(
                    ProofStep(
                        step_number=1,
                        title_vi="Xác định dữ kiện cạnh bên và chiều cao hình chóp đều",
                        title_en="Identify lateral edge and altitude of the regular pyramid",
                        statement_vi=f"Hình chóp đều có độ dài cạnh bên $b = {sp.latex(b_sym)}$ và chiều cao $h = {sp.latex(h_sym)}$ ($b > h > 0$).",
                        statement_en=f"The regular pyramid has lateral edge $b = {sp.latex(b_sym)}$ and altitude $h = {sp.latex(h_sym)}$ ($b > h > 0$).",
                        latex_formula=f"b = {sp.latex(b_sym)}, \\quad h = {sp.latex(h_sym)}",
                        math_reasons=["Tính chất hình chóp đều / Regular pyramid properties"],
                    )
                )

            R_sym = sp.simplify(b_sym ** 2 / (2 * h_sym))
            steps.append(
                ProofStep(
                    step_number=2,
                    title_vi="Áp dụng hệ thức lượng mặt cầu ngoại tiếp hình chóp đều",
                    title_en="Apply circumscribed sphere metric formula for a regular pyramid",
                    statement_vi=(
                        "Gọi $SO = h$ là đường cao hình chóp đều. Đường trung trực của cạnh bên $SA = b$ trong mặt phẳng $(SOA)$ "
                        f"cắt trục $SO$ tại tâm $I$ của mặt cầu ngoại tiếp. Nhờ hai tam giác đồng dạng, ta có $R = \\frac{{b^2}}{{2h}} = {sp.latex(R_sym)}$."
                    ),
                    statement_en=(
                        "Let $SO = h$ be the altitude of the regular pyramid. The perpendicular bisector of lateral edge $SA = b$ in plane $(SOA)$ "
                        f"intersects axis $SO$ at circumcenter $I$. By similar triangles, $R = \\frac{{b^2}}{{2h}} = {sp.latex(R_sym)}$."
                    ),
                    latex_formula=f"R = \\frac{{b^2}}{{2h}} = \\frac{{\\left({sp.latex(b_sym)}\\right)^2}}{{2 \\cdot {sp.latex(h_sym)}}} = {sp.latex(R_sym)}",
                    math_reasons=[
                        "Tam giác đồng dạng trên mặt phẳng chứa trục hình chóp đều / Similar triangles in the axial plane"
                    ],
                )
            )

            R_num = float(R_sym.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Circumscribed Sphere - Regular Pyramid / Regular Tetrahedron",
                steps=steps,
                symbolic_result=R_sym,
                numeric_value=R_num,
                unit="length",
                conclusion_vi=f"Bán kính mặt cầu ngoại tiếp hình chóp đều là R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
                conclusion_en=f"The circumscribed sphere radius of the regular pyramid is R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
                metadata={"b": float(b_sym.evalf()), "h": float(h_sym.evalf())},
            )

        elif case_key == "rectangular_box":
            a_sym = self._require_positive(kwargs.get("a"), "kích thước a", "dimension a")
            b_sym = self._require_positive(kwargs.get("b"), "kích thước b", "dimension b")
            c_sym = self._require_positive(kwargs.get("c"), "kích thước c", "dimension c")
            R_sym = sp.simplify(sp.sqrt(a_sym ** 2 + b_sym ** 2 + c_sym ** 2) / 2)

            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Tính độ dài đường chéo chính của khối hộp chữ nhật",
                    title_en="Compute the main space diagonal of the rectangular cuboid",
                    statement_vi=(
                        f"Khối hộp chữ nhật có ba kích thước $a = {sp.latex(a_sym)}, b = {sp.latex(b_sym)}, c = {sp.latex(c_sym)}$. "
                        "Tâm mặt cầu ngoại tiếp là giao điểm các đường chéo chính, và bán kính bằng một nửa đường chéo chính."
                    ),
                    statement_en=(
                        f"The rectangular cuboid has dimensions $a = {sp.latex(a_sym)}, b = {sp.latex(b_sym)}, c = {sp.latex(c_sym)}$. "
                        "The circumcenter is the intersection of the space diagonals, so the radius equals half the space diagonal."
                    ),
                    latex_formula=(
                        f"R = \\frac{{\\sqrt{{a^2 + b^2 + c^2}}}}{{2}} "
                        f"= \\frac{{\\sqrt{{{sp.latex(a_sym)}^2 + {sp.latex(b_sym)}^2 + {sp.latex(c_sym)}^2}}}}{{2}} = {sp.latex(R_sym)}"
                    ),
                    math_reasons=["Định lý Pythagore trong không gian 3 chiều / 3D Pythagorean Theorem"],
                )
            )
            R_num = float(R_sym.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Circumscribed Sphere - Rectangular Cuboid",
                steps=steps,
                symbolic_result=R_sym,
                numeric_value=R_num,
                unit="length",
                conclusion_vi=f"Bán kính mặt cầu ngoại tiếp khối hộp chữ nhật là R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
                conclusion_en=f"The circumscribed sphere radius of the rectangular box is R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
            )

        elif case_key == "orthogonal_tetrahedron":
            oa_sym = self._require_positive(kwargs.get("oa"), "cạnh OA", "edge OA")
            ob_sym = self._require_positive(kwargs.get("ob"), "cạnh OB", "edge OB")
            oc_sym = self._require_positive(kwargs.get("oc"), "cạnh OC", "edge OC")
            R_sym = sp.simplify(sp.sqrt(oa_sym ** 2 + ob_sym ** 2 + oc_sym ** 2) / 2)

            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Bổ sung tứ diện vuông thành khối hộp chữ nhật",
                    title_en="Embed the tri-rectangular tetrahedron into a rectangular cuboid",
                    statement_vi=(
                        f"Tứ diện $O.ABC$ có $OA = {sp.latex(oa_sym)}, OB = {sp.latex(ob_sym)}, OC = {sp.latex(oc_sym)}$ đôi một vuông góc tại $O$. "
                        "Mặt cầu ngoại tiếp tứ diện $O.ABC$ trùng với mặt cầu ngoại tiếp khối hộp chữ nhật có 3 kích thước $OA, OB, OC$."
                    ),
                    statement_en=(
                        f"Tetrahedron $O.ABC$ has mutually perpendicular edges $OA = {sp.latex(oa_sym)}, OB = {sp.latex(ob_sym)}, OC = {sp.latex(oc_sym)}$ at $O$. "
                        "Its circumsphere coincides with that of the rectangular box with dimensions $OA, OB, OC$."
                    ),
                    latex_formula=(
                        f"R = \\frac{{\\sqrt{{OA^2 + OB^2 + OC^2}}}}{{2}} "
                        f"= \\frac{{\\sqrt{{{sp.latex(oa_sym)}^2 + {sp.latex(ob_sym)}^2 + {sp.latex(oc_sym)}^2}}}}{{2}} = {sp.latex(R_sym)}"
                    ),
                    math_reasons=["Phương pháp bổ sung hình hộp chữ nhật / Cuboid embedding method"],
                )
            )
            R_num = float(R_sym.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Circumscribed Sphere - Tri-rectangular Tetrahedron",
                steps=steps,
                symbolic_result=R_sym,
                numeric_value=R_num,
                unit="length",
                conclusion_vi=f"Bán kính mặt cầu ngoại tiếp tứ diện vuông là R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
                conclusion_en=f"The circumscribed sphere radius of the orthogonal tetrahedron is R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
            )

        elif case_key in ("dispisphenoid", "isoceles_tetrahedron", "equifacial_tetrahedron"):
            a_sym = self._require_positive(kwargs.get("a"), "cặp cạnh đối a", "opposite edge pair a")
            b_sym = self._require_positive(kwargs.get("b"), "cặp cạnh đối b", "opposite edge pair b")
            c_sym = self._require_positive(kwargs.get("c"), "cặp cạnh đối c", "opposite edge pair c")
            R_sym = sp.simplify(sp.sqrt((a_sym ** 2 + b_sym ** 2 + c_sym ** 2) / 8))

            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Nội tiếp tứ diện gần đều vào hình hộp chữ nhật",
                    title_en="Inscribe the equifacial tetrahedron inside a rectangular box",
                    statement_vi=(
                        f"Tứ diện gần đều có các cặp cạnh đối bằng nhau $a = {sp.latex(a_sym)}, b = {sp.latex(b_sym)}, c = {sp.latex(c_sym)}$ "
                        "nội tiếp trong hình hộp chữ nhật có các đường chéo mặt là $a, b, c$. Khi đó $x^2 + y^2 + z^2 = \\frac{a^2 + b^2 + c^2}{2}$."
                    ),
                    statement_en=(
                        f"An equifacial tetrahedron with opposite edges $a = {sp.latex(a_sym)}, b = {sp.latex(b_sym)}, c = {sp.latex(c_sym)}$ "
                        "can be inscribed in a rectangular box whose face diagonals are $a, b, c$, giving $x^2 + y^2 + z^2 = \\frac{a^2 + b^2 + c^2}{2}$."
                    ),
                    latex_formula=(
                        f"R = \\sqrt{{\\frac{{a^2 + b^2 + c^2}}{{8}}}} "
                        f"= \\sqrt{{\\frac{{{sp.latex(a_sym)}^2 + {sp.latex(b_sym)}^2 + {sp.latex(c_sym)}^2}}{{8}}}} = {sp.latex(R_sym)}"
                    ),
                    math_reasons=[
                        "Định lý ngoại tiếp tứ diện gần đều bằng hình hộp chữ nhật / Equifacial tetrahedron cuboid theorem"
                    ],
                )
            )
            R_num = float(R_sym.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Circumscribed Sphere - Equifacial Tetrahedron",
                steps=steps,
                symbolic_result=R_sym,
                numeric_value=R_num,
                unit="length",
                conclusion_vi=f"Bán kính mặt cầu ngoại tiếp tứ diện gần đều là R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
                conclusion_en=f"The circumscribed sphere radius of the equifacial tetrahedron is R = {sp.latex(R_sym)} ≈ {R_num:.4f}.",
            )

        raise PedagogicalGeometryError(
            f"Loại khối đa diện '{case_type}' không được hỗ trợ trong bài toán mặt cầu ngoại tiếp.",
            f"Polyhedron case_type '{case_type}' is not supported for circumscribed sphere proof.",
            error_code="ERR_UNSUPPORTED_CIRCUM_CASE",
        )

    # ==========================================================================
    # 2b. MẶT CẦU NỘI TIẾP (INSCRIBED SPHERE)
    # ==========================================================================
    def prove_inscribed_sphere(
        self,
        case_type: str,
        problem_id: str = "INSCRIBED_SPHERE_01",
        **kwargs: Any,
    ) -> DeductiveProofResult:
        """
        Generates a complete deductive proof for the inscribed sphere radius r.

        Supported `case_type` values:
        1. 'general_polyhedron': Given Volume `V` and total surface area `S_tp` (r = 3V / S_tp).
        2. 'regular_quad_pyramid': Regular square pyramid with base edge `a` and height `h`.
           Computes V = (1/3)*a^2*h, slant height d_slant = sqrt(h^2 + (a/2)^2),
           S_tp = a^2 + 2*a*d_slant, and r = 3V / S_tp.
        3. 'cone': Right circular cone with base radius `r_cone` and height `h` (or slant height `l`):
           r = (r_cone * h) / (r_cone + l).
        4. 'cube': Cube with edge `a`: r = a / 2.
        """
        steps: List[ProofStep] = []
        case_key = case_type.strip().lower()

        if case_key == "regular_quad_pyramid":
            a_sym = self._require_positive(kwargs.get("a"), "cạnh đáy hình vuông a", "square base edge a")
            h_sym = self._require_positive(kwargs.get("h"), "chiều cao hình chóp h", "pyramid height h")

            s_base = sp.simplify(a_sym ** 2)
            V_sym = sp.simplify(sp.Rational(1, 3) * s_base * h_sym)
            apothem_sym = sp.simplify(sp.sqrt(h_sym ** 2 + (a_sym / 2) ** 2))
            s_lateral = sp.simplify(4 * sp.Rational(1, 2) * a_sym * apothem_sym)
            s_tp_sym = sp.simplify(s_base + s_lateral)
            r_sym = sp.simplify(3 * V_sym / s_tp_sym)

            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Tính diện tích đáy và thể tích khối chóp tứ giác đều",
                    title_en="Calculate base area and volume of the regular square pyramid",
                    statement_vi=(
                        f"Đáy là hình vuông cạnh $a = {sp.latex(a_sym)}$ nên $S_{{\\text{{đáy}}}} = a^2 = {sp.latex(s_base)}$. "
                        f"Với chiều cao $h = {sp.latex(h_sym)}$, thể tích khối chóp là $V = \\frac{{1}}{{3}} S_{{\\text{{đáy}}}} \\cdot h = {sp.latex(V_sym)}$."
                    ),
                    statement_en=(
                        f"The square base of side $a = {sp.latex(a_sym)}$ has area $S_{{\\text{{base}}}} = a^2 = {sp.latex(s_base)}$. "
                        f"With altitude $h = {sp.latex(h_sym)}$, the pyramid volume is $V = \\frac{{1}}{{3}} S_{{\\text{{base}}}} \\cdot h = {sp.latex(V_sym)}$."
                    ),
                    latex_formula=f"S_{{\\text{{base}}}} = a^2 = {sp.latex(s_base)}, \\quad V = \\frac{{1}}{{3}} a^2 h = {sp.latex(V_sym)}",
                    math_reasons=["Công thức thể tích khối chóp / Pyramid volume formula"],
                )
            )

            steps.append(
                ProofStep(
                    step_number=2,
                    title_vi="Tính trung đoạn và diện tích toàn phần của hình chóp",
                    title_en="Compute slant height (apothem) and total surface area",
                    statement_vi=(
                        f"Trung đoạn mặt bên là $d_m = \\sqrt{{h^2 + \\left(\\frac{{a}}{{2}}\\right)^2}} = {sp.latex(apothem_sym)}$. "
                        f"Diện tích xung quanh $S_{{xq}} = 4 \\cdot \\frac{{1}}{{2}} a \\cdot d_m = {sp.latex(s_lateral)}$, "
                        f"suy ra diện tích toàn phần $S_{{tp}} = S_{{\\text{{đáy}}}} + S_{{xq}} = {sp.latex(s_tp_sym)}$."
                    ),
                    statement_en=(
                        f"The lateral slant height is $d_m = \\sqrt{{h^2 + \\left(\\frac{{a}}{{2}}\\right)^2}} = {sp.latex(apothem_sym)}$. "
                        f"The lateral surface area is $S_{{lat}} = 2 a d_m = {sp.latex(s_lateral)}$, "
                        f"giving total surface area $S_{{tp}} = S_{{\\text{{base}}}} + S_{{lat}} = {sp.latex(s_tp_sym)}$."
                    ),
                    latex_formula=(
                        f"d_m = \\sqrt{{h^2 + \\frac{{a^2}}{{4}}}} = {sp.latex(apothem_sym)}, \\quad "
                        f"S_{{tp}} = a^2 + 2 a d_m = {sp.latex(s_tp_sym)}"
                    ),
                    math_reasons=[
                        "Định lý Pythagore cho trung đoạn mặt bên / Pythagorean theorem for slant height"
                    ],
                )
            )

            steps.append(
                ProofStep(
                    step_number=3,
                    title_vi="Tính bán kính mặt cầu nội tiếp theo công thức phân hoạch thể tích",
                    title_en="Compute inscribed sphere radius via volume decomposition",
                    statement_vi=(
                        f"Nối tâm mặt cầu nội tiếp $I$ với các đỉnh chia khối đa diện thành các khối chóp con có cùng chiều cao $r$. "
                        f"Do đó $V = \\frac{{1}}{{3}} S_{{tp}} \\cdot r \\implies r = \\frac{{3V}}{{S_{{tp}}}} = {sp.latex(r_sym)}$."
                    ),
                    statement_en=(
                        f"Connecting incenter $I$ to all vertices partitions the polyhedron into sub-pyramids of altitude $r$. "
                        f"Thus $V = \\frac{{1}}{{3}} S_{{tp}} \\cdot r \\implies r = \\frac{{3V}}{{S_{{tp}}}} = {sp.latex(r_sym)}$."
                    ),
                    latex_formula=f"r = \\frac{{3V}}{{S_{{tp}}}} = \\frac{{3 \\cdot {sp.latex(V_sym)}}}{{{sp.latex(s_tp_sym)}}} = {sp.latex(r_sym)}",
                    math_reasons=[
                        "Định lý bán kính mặt cầu nội tiếp đa diện lồi / Convex polyhedron insphere radius theorem"
                    ],
                )
            )

            r_num = float(r_sym.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Inscribed Sphere - Regular Square Pyramid",
                steps=steps,
                symbolic_result=r_sym,
                numeric_value=r_num,
                unit="length",
                conclusion_vi=f"Bán kính mặt cầu nội tiếp hình chóp tứ giác đều là r = {sp.latex(r_sym)} ≈ {r_num:.4f}.",
                conclusion_en=f"The inscribed sphere radius of the regular square pyramid is r = {sp.latex(r_sym)} ≈ {r_num:.4f}.",
                metadata={
                    "V": float(V_sym.evalf()),
                    "S_tp": float(s_tp_sym.evalf()),
                    "V_symbolic": V_sym,
                    "S_tp_symbolic": s_tp_sym,
                },
            )

        elif case_key == "general_polyhedron":
            V_sym = self._require_positive(kwargs.get("V"), "thể tích V", "volume V")
            s_tp_sym = self._require_positive(kwargs.get("S_tp"), "diện tích toàn phần S_tp", "total surface area S_tp")
            r_sym = sp.simplify(3 * V_sym / s_tp_sym)

            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Áp dụng định lý mặt cầu nội tiếp khối đa diện",
                    title_en="Apply polyhedron inscribed sphere theorem",
                    statement_vi=(
                        f"Với khối đa diện ngoại tiếp mặt cầu có thể tích $V = {sp.latex(V_sym)}$ và diện tích toàn phần $S_{{tp}} = {sp.latex(s_tp_sym)}$, "
                        f"bán kính mặt cầu nội tiếp được xác định bởi $r = \\frac{{3V}}{{S_{{tp}}}} = {sp.latex(r_sym)}$."
                    ),
                    statement_en=(
                        f"For a tangential polyhedron with volume $V = {sp.latex(V_sym)}$ and total surface area $S_{{tp}} = {sp.latex(s_tp_sym)}$, "
                        f"the insphere radius is given by $r = \\frac{{3V}}{{S_{{tp}}}} = {sp.latex(r_sym)}$."
                    ),
                    latex_formula=f"r = \\frac{{3V}}{{S_{{tp}}}} = \\frac{{3 \\cdot {sp.latex(V_sym)}}}{{{sp.latex(s_tp_sym)}}} = {sp.latex(r_sym)}",
                    math_reasons=["Phương pháp phân hoạch thể tích / Volume decomposition theorem"],
                )
            )
            r_num = float(r_sym.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Inscribed Sphere - General Polyhedron",
                steps=steps,
                symbolic_result=r_sym,
                numeric_value=r_num,
                unit="length",
                conclusion_vi=f"Bán kính mặt cầu nội tiếp đa diện là r = {sp.latex(r_sym)} ≈ {r_num:.4f}.",
                conclusion_en=f"The inscribed sphere radius of the polyhedron is r = {sp.latex(r_sym)} ≈ {r_num:.4f}.",
            )

        elif case_key == "cone":
            r_cone_sym = self._require_positive(kwargs.get("r_cone"), "bán kính đáy nón R_cone", "cone base radius R_cone")
            if "h" in kwargs and kwargs["h"] is not None:
                h_sym = self._require_positive(kwargs["h"], "chiều cao nón h", "cone altitude h")
                l_sym = sp.simplify(sp.sqrt(r_cone_sym ** 2 + h_sym ** 2))
            elif "l" in kwargs and kwargs["l"] is not None:
                l_sym = self._require_positive(kwargs["l"], "đường sinh l", "slant height l")
                radicand = self._require_non_negative_radicand(
                    l_sym ** 2 - r_cone_sym ** 2,
                    "tính chiều cao hình nón",
                    "cone altitude calculation",
                )
                h_sym = self._require_positive(sp.sqrt(radicand), "chiều cao nón h", "cone altitude h")
            else:
                raise PedagogicalGeometryError(
                    "Cần cung cấp chiều cao 'h' hoặc đường sinh 'l' cho hình nón.",
                    "Must provide either altitude 'h' or slant height 'l' for the cone.",
                    error_code="ERR_MISSING_CONE_PARAM",
                )

            r_sym = sp.simplify((r_cone_sym * h_sym) / (r_cone_sym + l_sym))
            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Xét thiết diện qua trục của hình nón tròn xoay",
                    title_en="Analyze the axial cross-section of the right circular cone",
                    statement_vi=(
                        f"Thiết diện qua trục là tam giác cân có cạnh đáy $2R_{{\\text{{cone}}}} = {sp.latex(2 * r_cone_sym)}$, "
                        f"chiều cao $h = {sp.latex(h_sym)}$, đường sinh $l = \\sqrt{{R_{{\\text{{cone}}}}^2 + h^2}} = {sp.latex(l_sym)}$. "
                        f"Bán kính mặt cầu nội tiếp bằng bán kính đường tròn nội tiếp thiết diện: $r = \\frac{{R_{{\\text{{cone}}}} \\cdot h}}{{R_{{\\text{{cone}}}} + l}} = {sp.latex(r_sym)}$."
                    ),
                    statement_en=(
                        f"The axial cross-section is an isosceles triangle with base $2R_{{\\text{{cone}}}} = {sp.latex(2 * r_cone_sym)}$, "
                        f"altitude $h = {sp.latex(h_sym)}$, and slant height $l = {sp.latex(l_sym)}$. "
                        f"The insphere radius equals the inradius of the axial triangle: $r = \\frac{{R_{{\\text{{cone}}}} \\cdot h}}{{R_{{\\text{{cone}}}} + l}} = {sp.latex(r_sym)}$."
                    ),
                    latex_formula=f"r = \\frac{{R_{{\\text{{cone}}}} \\cdot h}}{{R_{{\\text{{cone}}}} + l}} = {sp.latex(r_sym)}",
                    math_reasons=["Công thức bán kính đường tròn nội tiếp thiết diện qua trục / Axial inradius theorem"],
                )
            )
            r_num = float(r_sym.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Inscribed Sphere - Right Circular Cone",
                steps=steps,
                symbolic_result=r_sym,
                numeric_value=r_num,
                unit="length",
                conclusion_vi=f"Bán kính mặt cầu nội tiếp hình nón là r = {sp.latex(r_sym)} ≈ {r_num:.4f}.",
                conclusion_en=f"The inscribed sphere radius of the cone is r = {sp.latex(r_sym)} ≈ {r_num:.4f}.",
            )

        elif case_key == "cube":
            a_sym = self._require_positive(kwargs.get("a"), "cạnh hình lập phương a", "cube edge a")
            r_sym = sp.simplify(a_sym / 2)
            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Tính bán kính mặt cầu nội tiếp hình lập phương",
                    title_en="Compute the inscribed sphere radius of the cube",
                    statement_vi=(
                        f"Mặt cầu nội tiếp hình lập phương cạnh $a = {sp.latex(a_sym)}$ tiếp xúc với 6 mặt tại tâm của chúng, "
                        f"nên đường kính bằng cạnh hình lập phương: $2r = a \\implies r = \\frac{{a}}{{2}} = {sp.latex(r_sym)}$."
                    ),
                    statement_en=(
                        f"The sphere inscribed in a cube of edge $a = {sp.latex(a_sym)}$ touches all 6 faces at their centers, "
                        f"so its diameter equals the cube edge: $2r = a \\implies r = \\frac{{a}}{{2}} = {sp.latex(r_sym)}$."
                    ),
                    latex_formula=f"r = \\frac{{a}}{{2}} = {sp.latex(r_sym)}",
                    math_reasons=["Tính chất đối xứng của hình lập phương / Symmetry of the cube"],
                )
            )
            r_num = float(r_sym.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Inscribed Sphere - Cube",
                steps=steps,
                symbolic_result=r_sym,
                numeric_value=r_num,
                unit="length",
                conclusion_vi=f"Bán kính mặt cầu nội tiếp hình lập phương là r = {sp.latex(r_sym)} ≈ {r_num:.4f}.",
                conclusion_en=f"The inscribed sphere radius of the cube is r = {sp.latex(r_sym)} ≈ {r_num:.4f}.",
            )

        raise PedagogicalGeometryError(
            f"Loại hình '{case_type}' không được hỗ trợ trong bài toán mặt cầu nội tiếp.",
            f"Case type '{case_type}' is not supported for inscribed sphere proof.",
            error_code="ERR_UNSUPPORTED_INSCRIBED_CASE",
        )

    # ==========================================================================
    # 2c. TƯƠNG GIAO MẶT PHẲNG VÀ MẶT CẦU (PLANE-SPHERE INTERSECTION & CAP)
    # ==========================================================================
    def prove_plane_sphere_intersection(
        self,
        sphere: Optional[Sphere3D] = None,
        plane: Optional[Plane3D] = None,
        *,
        R: Optional[Union[int, float, sp.Expr]] = None,
        d: Optional[Union[int, float, sp.Expr]] = None,
        problem_id: str = "PLANE_SPHERE_01",
    ) -> DeductiveProofResult:
        """
        Proves the positional relationship between a sphere (S) and a plane (P),
        computing:
        - Distance d = d(I, (P))
        - Intersection circle radius r = sqrt(R^2 - d^2) and area S_circle = pi * r^2
        - Spherical cap height h = R - d, surface area S_cap = 2*pi*R*h,
          and volume V_cap = (pi * h^2 / 3) * (3R - h) when d < R.

        Can be called either with geometric objects `(sphere, plane)` OR directly
        with scalar parameters `(R=..., d=...)` for spherical cap / section analysis.
        """
        steps: List[ProofStep] = []

        if sphere is not None and plane is not None:
            x0, y0, z0 = sphere.center.to_sympy()
            R_sym = self._require_positive(sphere.radius, "bán kính mặt cầu R", "sphere radius R")
            A_sym = self._to_sym(plane.A)
            B_sym = self._to_sym(plane.B)
            C_sym = self._to_sym(plane.C)
            D_sym = self._to_sym(plane.D)

            norm_sq = sp.simplify(A_sym ** 2 + B_sym ** 2 + C_sym ** 2)
            if float(norm_sq.evalf()) <= self.EPSILON:
                raise PedagogicalGeometryError(
                    "Vector pháp tuyến của mặt phẳng không hợp lệ (bằng vector 0).",
                    "Plane normal vector is degenerate (zero vector).",
                    error_code="ERR_ZERO_PLANE_NORMAL",
                )

            num_sym = sp.Abs(A_sym * x0 + B_sym * y0 + C_sym * z0 + D_sym)
            den_sym = sp.sqrt(norm_sq)
            d_sym = sp.simplify(num_sym / den_sym)

            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Tính khoảng cách từ tâm mặt cầu đến mặt phẳng",
                    title_en="Compute the distance from the sphere center to the plane",
                    statement_vi=(
                        f"Mặt cầu $(S)$ có tâm $I({sp.latex(x0)}; {sp.latex(y0)}; {sp.latex(z0)})$ và bán kính $R = {sp.latex(R_sym)}$. "
                        f"Khoảng cách từ tâm $I$ đến mặt phẳng $(P): {self._format_plane_latex(A_sym, B_sym, C_sym, D_sym)}$ là $d = d(I, (P)) = {sp.latex(d_sym)}$."
                    ),
                    statement_en=(
                        f"Sphere $(S)$ has center $I({sp.latex(x0)}; {sp.latex(y0)}; {sp.latex(z0)})$ and radius $R = {sp.latex(R_sym)}$. "
                        f"The distance from $I$ to plane $(P): {self._format_plane_latex(A_sym, B_sym, C_sym, D_sym)}$ is $d = d(I, (P)) = {sp.latex(d_sym)}$."
                    ),
                    latex_formula=(
                        f"d(I, (P)) = \\frac{{|A x_0 + B y_0 + C z_0 + D|}}{{\\sqrt{{A^2 + B^2 + C^2}}}} "
                        f"= \\frac{{{sp.latex(num_sym)}}}{{{sp.latex(den_sym)}}} = {sp.latex(d_sym)}"
                    ),
                    math_reasons=["Công thức khoảng cách từ một điểm đến mặt phẳng / Point-to-plane distance formula"],
                )
            )
        elif R is not None and d is not None:
            R_sym = self._require_positive(R, "bán kính mặt cầu R", "sphere radius R")
            d_float = float(d)
            if d_float < -self.EPSILON:
                raise PedagogicalGeometryError(
                    f"Khoảng cách d không thể âm (d = {d}).",
                    f"Distance d cannot be negative (d = {d}).",
                    error_code="ERR_NEGATIVE_DISTANCE",
                )
            d_sym = sp.Integer(0) if abs(d_float) <= self.EPSILON else self._to_sym(d)
            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Xác định bán kính mặt cầu và khoảng cách từ tâm đến mặt phẳng cắt",
                    title_en="Identify sphere radius and distance from center to the secant plane",
                    statement_vi=f"Mặt cầu có bán kính $R = {sp.latex(R_sym)}$ và khoảng cách từ tâm $I$ đến mặt phẳng $(P)$ là $d = {sp.latex(d_sym)}$.",
                    statement_en=f"The sphere has radius $R = {sp.latex(R_sym)}$ and distance from center $I$ to plane $(P)$ equal to $d = {sp.latex(d_sym)}$.",
                    latex_formula=f"R = {sp.latex(R_sym)}, \\quad d = d(I, (P)) = {sp.latex(d_sym)}",
                    math_reasons=["Dữ kiện hình học tương giao mặt phẳng - mặt cầu / Given plane-sphere parameters"],
                )
            )
        else:
            raise PedagogicalGeometryError(
                "Phải cung cấp cặp (sphere, plane) hoặc cặp tham số (R, d).",
                "Must provide either (sphere, plane) objects or scalar parameters (R, d).",
                error_code="ERR_MISSING_INTERSECTION_INPUTS",
            )

        d_val = float(d_sym.evalf())
        R_val = float(R_sym.evalf())

        # Case 1: d > R (No intersection)
        if d_val > R_val + self.EPSILON:
            steps.append(
                ProofStep(
                    step_number=2,
                    title_vi="So sánh khoảng cách d với bán kính mặt cầu R",
                    title_en="Compare distance d with sphere radius R",
                    statement_vi=f"Vì $d = {sp.latex(d_sym)} > R = {sp.latex(R_sym)}$, mặt phẳng $(P)$ và mặt cầu $(S)$ không có điểm chung.",
                    statement_en=f"Since $d = {sp.latex(d_sym)} > R = {sp.latex(R_sym)}$, plane $(P)$ and sphere $(S)$ do not intersect.",
                    latex_formula=f"d = {sp.latex(d_sym)} > R = {sp.latex(R_sym)} \\implies (P) \\cap (S) = \\varnothing",
                    math_reasons=["Vị trí tương đối giữa mặt phẳng và mặt cầu / Relative position of plane and sphere"],
                )
            )
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Plane-Sphere Intersection (Disjoint)",
                steps=steps,
                symbolic_result=sp.Integer(0),
                numeric_value=0.0,
                unit="length",
                conclusion_vi="Mặt phẳng (P) không cắt mặt cầu (S).",
                conclusion_en="Plane (P) does not intersect sphere (S).",
                metadata={"relation": "disjoint", "d": d_val, "R": R_val, "r_section": 0.0},
            )

        # Case 2: d == R (Tangent plane)
        if abs(d_val - R_val) <= self.EPSILON:
            steps.append(
                ProofStep(
                    step_number=2,
                    title_vi="Xác định điều kiện tiếp xúc giữa mặt phẳng và mặt cầu",
                    title_en="Verify tangency condition between plane and sphere",
                    statement_vi=f"Vì $d = {sp.latex(d_sym)} = R = {sp.latex(R_sym)}$, mặt phẳng $(P)$ tiếp xúc với mặt cầu $(S)$ tại duy nhất một tiếp điểm $H$.",
                    statement_en=f"Since $d = {sp.latex(d_sym)} = R = {sp.latex(R_sym)}$, plane $(P)$ is tangent to sphere $(S)$ at a unique point of tangency $H$.",
                    latex_formula=f"d = R = {sp.latex(R_sym)} \\implies r = \\sqrt{{R^2 - d^2}} = 0",
                    math_reasons=["Điều kiện mặt phẳng tiếp xúc mặt cầu / Tangency condition of plane and sphere"],
                )
            )
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="Plane-Sphere Intersection (Tangent)",
                steps=steps,
                symbolic_result=sp.Integer(0),
                numeric_value=0.0,
                unit="length",
                conclusion_vi="Mặt phẳng (P) tiếp xúc với mặt cầu (S) (bán kính thiết diện r = 0).",
                conclusion_en="Plane (P) is tangent to sphere (S) (section radius r = 0).",
                metadata={"relation": "tangent", "d": d_val, "R": R_val, "r_section": 0.0},
            )

        # Case 3: d < R (Secant plane -> intersection circle + spherical cap)
        r_sym = sp.simplify(sp.sqrt(R_sym ** 2 - d_sym ** 2))
        s_circle_sym = sp.simplify(sp.pi * r_sym ** 2)
        h_cap_sym = sp.simplify(R_sym - d_sym)
        s_cap_sym = sp.simplify(2 * sp.pi * R_sym * h_cap_sym)
        v_cap_sym = sp.simplify(sp.Rational(1, 3) * sp.pi * (h_cap_sym ** 2) * (3 * R_sym - h_cap_sym))

        steps.append(
            ProofStep(
                step_number=2,
                title_vi="Tính bán kính và diện tích đường tròn giao tuyến (thiết diện)",
                title_en="Calculate the radius and area of the intersection circle",
                statement_vi=(
                    f"Vì $d = {sp.latex(d_sym)} < R = {sp.latex(R_sym)}$, mặt phẳng $(P)$ cắt mặt cầu $(S)$ theo giao tuyến là đường tròn "
                    f"có bán kính $r = \\sqrt{{R^2 - d^2}} = {sp.latex(r_sym)}$ và diện tích thiết diện $S = \\pi r^2 = {sp.latex(s_circle_sym)}$."
                ),
                statement_en=(
                    f"Since $d = {sp.latex(d_sym)} < R = {sp.latex(R_sym)}$, plane $(P)$ intersects sphere $(S)$ in a circle "
                    f"of radius $r = \\sqrt{{R^2 - d^2}} = {sp.latex(r_sym)}$ and cross-sectional area $S = \\pi r^2 = {sp.latex(s_circle_sym)}$."
                ),
                latex_formula=(
                    f"r = \\sqrt{{R^2 - d^2}} = \\sqrt{{{sp.latex(R_sym)}^2 - {sp.latex(d_sym)}^2}} = {sp.latex(r_sym)}, \\quad "
                    f"S_{{\\text{{section}}}} = \\pi r^2 = {sp.latex(s_circle_sym)}"
                ),
                math_reasons=[
                    "Định lý Pythagore cho tam giác vuông tạo bởi tâm cầu, tâm thiết diện và điểm trên đường tròn giao tuyến / Pythagorean theorem on sphere section"
                ],
            )
        )

        steps.append(
            ProofStep(
                step_number=3,
                title_vi="Tính chiều cao, diện tích và thể tích chỏm cầu (Spherical Cap)",
                title_en="Calculate altitude, surface area, and volume of the spherical cap",
                statement_vi=(
                    f"Chỏm cầu bị cắt bởi mặt phẳng $(P)$ có chiều cao $h = R - d = {sp.latex(h_cap_sym)}$. "
                    f"Diện tích bề mặt chỏm cầu là $S_{{\\text{{cap}}}} = 2\\pi R h = {sp.latex(s_cap_sym)}$ "
                    f"và thể tích khối chỏm cầu là $V_{{\\text{{cap}}}} = \\frac{{\\pi h^2}}{{3}}(3R - h) = {sp.latex(v_cap_sym)}$."
                ),
                statement_en=(
                    f"The spherical cap cut off by plane $(P)$ has height $h = R - d = {sp.latex(h_cap_sym)}$. "
                    f"Its curved surface area is $S_{{\\text{{cap}}}} = 2\\pi R h = {sp.latex(s_cap_sym)}$ "
                    f"and its volume is $V_{{\\text{{cap}}}} = \\frac{{\\pi h^2}}{{3}}(3R - h) = {sp.latex(v_cap_sym)}$."
                ),
                latex_formula=(
                    f"h = R - d = {sp.latex(h_cap_sym)}, \\quad "
                    f"S_{{\\text{{cap}}}} = 2\\pi R h = {sp.latex(s_cap_sym)}, \\quad "
                    f"V_{{\\text{{cap}}}} = \\frac{{\\pi h^2}}{{3}}(3R - h) = {sp.latex(v_cap_sym)}"
                ),
                math_reasons=[
                    "Công thức tích phân thể tích và diện tích chỏm cầu / Integral formulas for spherical cap area and volume"
                ],
            )
        )

        r_num = float(r_sym.evalf())
        return DeductiveProofResult(
            problem_id=problem_id,
            topic="Plane-Sphere Intersection & Spherical Cap",
            steps=steps,
            symbolic_result=r_sym,
            numeric_value=r_num,
            unit="length",
            conclusion_vi=(
                f"Khoảng cách d = {sp.latex(d_sym)}, bán kính thiết diện r = {sp.latex(r_sym)} ≈ {r_num:.4f}, "
                f"diện tích chỏm cầu S_cap = {sp.latex(s_cap_sym)}, thể tích chỏm cầu V_cap = {sp.latex(v_cap_sym)}."
            ),
            conclusion_en=(
                f"Distance d = {sp.latex(d_sym)}, section radius r = {sp.latex(r_sym)} ≈ {r_num:.4f}, "
                f"spherical cap area S_cap = {sp.latex(s_cap_sym)}, spherical cap volume V_cap = {sp.latex(v_cap_sym)}."
            ),
            metadata={
                "relation": "secant",
                "d": d_val,
                "d_symbolic": d_sym,
                "R": R_val,
                "R_symbolic": R_sym,
                "r_section": r_num,
                "r_symbolic": r_sym,
                "S_section_symbolic": s_circle_sym,
                "S_section": float(s_circle_sym.evalf()),
                "h_cap_symbolic": h_cap_sym,
                "h_cap": float(h_cap_sym.evalf()),
                "S_cap_symbolic": s_cap_sym,
                "S_cap": float(s_cap_sym.evalf()),
                "V_cap_symbolic": v_cap_sym,
                "V_cap": float(v_cap_sym.evalf()),
            },
        )

    # ==========================================================================
    # 2c (cont.). PHƯƠNG TRÌNH MẶT PHẲNG TIẾP DIỆN TẠI M0
    # ==========================================================================
    def prove_tangent_plane_at_point(
        self,
        sphere: Sphere3D,
        point_m0: Point3D,
        problem_id: str = "TANGENT_PLANE_01",
    ) -> DeductiveProofResult:
        """
        Derives the equation of the tangent plane to `sphere` at point `M0(x0, y0, z0)`:
            (x0 - a)(x - a) + (y0 - b)(y - b) + (z0 - c)(z - c) = R^2
        Verifies strictly that M0 lies on the sphere surface.
        """
        steps: List[ProofStep] = []
        a_sym, b_sym, c_sym = sphere.center.to_sympy()
        x0_sym, y0_sym, z0_sym = point_m0.to_sympy()
        R_sym = self._require_positive(sphere.radius, "bán kính mặt cầu R", "sphere radius R")

        dist_sq_sym = sp.simplify((x0_sym - a_sym) ** 2 + (y0_sym - b_sym) ** 2 + (z0_sym - c_sym) ** 2)
        if abs(float(dist_sq_sym.evalf()) - float((R_sym ** 2).evalf())) > 1e-6:
            raise PedagogicalGeometryError(
                f"Điểm M0{point_m0.to_tuple()} không thuộc mặt cầu tâm I{sphere.center.to_tuple()} bán kính R={sphere.radius}.",
                f"Point M0{point_m0.to_tuple()} does not lie on the sphere with center I{sphere.center.to_tuple()} and radius R={sphere.radius}.",
                error_code="ERR_POINT_NOT_ON_SPHERE",
            )

        nx_sym = sp.simplify(x0_sym - a_sym)
        ny_sym = sp.simplify(y0_sym - b_sym)
        nz_sym = sp.simplify(z0_sym - c_sym)
        D_sym = sp.simplify(-(nx_sym * x0_sym + ny_sym * y0_sym + nz_sym * z0_sym))

        x, y, z = sp.symbols("x y z")
        plane_lhs = sp.simplify(nx_sym * x + ny_sym * y + nz_sym * z + D_sym)
        plane_latex = self._format_plane_latex(nx_sym, ny_sym, nz_sym, D_sym)

        steps.append(
            ProofStep(
                step_number=1,
                title_vi="Kiểm tra điểm tiếp xúc và xác định vector pháp tuyến tiếp diện",
                title_en="Verify point of tangency and determine the tangent plane normal vector",
                statement_vi=(
                    f"Ta có $IM_0^2 = ({sp.latex(x0_sym)} - {sp.latex(a_sym)})^2 + ({sp.latex(y0_sym)} - {sp.latex(b_sym)})^2 + "
                    f"({sp.latex(z0_sym)} - {sp.latex(c_sym)})^2 = {sp.latex(dist_sq_sym)} = R^2$, nên $M_0 \\in (S)$. "
                    f"Mặt phẳng tiếp diện nhận $\\vec{{IM_0}} = ({sp.latex(nx_sym)}; {sp.latex(ny_sym)}; {sp.latex(nz_sym)})$ làm vector pháp tuyến."
                ),
                statement_en=(
                    f"We have $IM_0^2 = {sp.latex(dist_sq_sym)} = R^2$, confirming $M_0 \\in (S)$. "
                    f"The tangent plane at $M_0$ has normal vector $\\vec{{n}} = \\vec{{IM_0}} = ({sp.latex(nx_sym)}; {sp.latex(ny_sym)}; {sp.latex(nz_sym)})$."
                ),
                latex_formula=f"\\vec{{n}} = \\vec{{IM_0}} = ({sp.latex(nx_sym)}, {sp.latex(ny_sym)}, {sp.latex(nz_sym)})",
                math_reasons=[
                    "Mặt phẳng tiếp diện vuông góc với bán kính tại tiếp điểm / Tangent plane is perpendicular to radius at point of contact"
                ],
            )
        )

        steps.append(
            ProofStep(
                step_number=2,
                title_vi="Viết phương trình mặt phẳng tiếp diện",
                title_en="Formulate the tangent plane equation",
                statement_vi=(
                    "Áp dụng công thức phương trình mặt phẳng tiếp diện tại $M_0(x_0, y_0, z_0)$: "
                    f"$(x_0 - a)(x - a) + (y_0 - b)(y - b) + (z_0 - c)(z - c) = R^2$, thu gọn thành ${plane_latex}$."
                ),
                statement_en=(
                    "Applying the sphere tangent plane equation at $M_0(x_0, y_0, z_0)$: "
                    f"$(x_0 - a)(x - a) + (y_0 - b)(y - b) + (z_0 - c)(z - c) = R^2$, which simplifies to ${plane_latex}$."
                ),
                latex_formula=(
                    f"(x_0 - a)(x - a) + (y_0 - b)(y - b) + (z_0 - c)(z - c) = R^2 \\iff {plane_latex}"
                ),
                math_reasons=["Phương trình mặt phẳng tiếp diện của mặt cầu / Equation of tangent plane to a sphere"],
            )
        )

        return DeductiveProofResult(
            problem_id=problem_id,
            topic="Tangent Plane to Sphere at Point M0",
            steps=steps,
            symbolic_result=plane_lhs,
            numeric_value=float(R_sym.evalf()),
            unit="equation",
            conclusion_vi=f"Phương trình mặt phẳng tiếp diện tại M0 là: {plane_latex}.",
            conclusion_en=f"The equation of the tangent plane at M0 is: {plane_latex}.",
            metadata={
                "A": float(nx_sym.evalf()),
                "B": float(ny_sym.evalf()),
                "C": float(nz_sym.evalf()),
                "D": float(D_sym.evalf()),
                "plane_latex": plane_latex,
            },
        )

    # ==========================================================================
    # 2d. HÌNH HỌC MẶT CẦU (GIRARD'S THEOREM & GREAT-CIRCLE DISTANCE)
    # ==========================================================================
    def prove_girard_spherical_area(
        self,
        R: Union[int, float, sp.Expr],
        angle_A: Union[int, float, sp.Expr],
        angle_B: Union[int, float, sp.Expr],
        angle_C: Union[int, float, sp.Expr],
        *,
        angles_in_degrees: bool = False,
        lat_lon_pair: Optional[Tuple[Tuple[float, float], Tuple[float, float]]] = None,
        problem_id: str = "GIRARD_SPHERICAL_01",
    ) -> DeductiveProofResult:
        """
        Proves the area of a spherical triangle on a sphere of radius R using
        Girard's Theorem:
            E = A + B + C - pi   (Spherical Excess in radians)
            S = R^2 * (A + B + C - pi)
        Optionally also computes the Great-Circle (orthodromic) distance between two
        geographic coordinates (phi_1, lambda_1) and (phi_2, lambda_2) in degrees.
        """
        steps: List[ProofStep] = []
        R_sym = self._require_positive(R, "bán kính mặt cầu R", "sphere radius R")

        if angles_in_degrees:
            A_rad = sp.simplify(self._to_sym(angle_A) * sp.pi / 180)
            B_rad = sp.simplify(self._to_sym(angle_B) * sp.pi / 180)
            C_rad = sp.simplify(self._to_sym(angle_C) * sp.pi / 180)
        else:
            A_rad = self._to_sym(angle_A)
            B_rad = self._to_sym(angle_B)
            C_rad = self._to_sym(angle_C)

        for lbl, ang in (("A", A_rad), ("B", B_rad), ("C", C_rad)):
            ang_val = float(ang.evalf())
            if ang_val <= self.EPSILON or ang_val >= math.pi - self.EPSILON:
                raise PedagogicalGeometryError(
                    f"Góc tam giác cầu {lbl} phải nằm trong khoảng (0, pi) radian.",
                    f"Spherical triangle angle {lbl} must lie strictly within (0, pi) radians.",
                    error_code="ERR_INVALID_SPHERICAL_ANGLE",
                )

        excess_sym = sp.simplify(A_rad + B_rad + C_rad - sp.pi)
        if float(excess_sym.evalf()) <= self.EPSILON:
            raise PedagogicalGeometryError(
                "Tổng ba góc của tam giác cầu phải lớn hơn pi radian (Độ dư cầu E = A + B + C - pi > 0).",
                "The sum of spherical triangle angles must exceed pi radians (Spherical excess E = A + B + C - pi > 0).",
                error_code="ERR_NON_POSITIVE_SPHERICAL_EXCESS",
            )

        area_sym = sp.simplify((R_sym ** 2) * excess_sym)

        steps.append(
            ProofStep(
                step_number=1,
                title_vi="Tính độ dư cầu (Spherical Excess) của tam giác cầu",
                title_en="Compute the spherical excess of the spherical triangle",
                statement_vi=(
                    f"Tam giác cầu $ABC$ trên mặt cầu bán kính $R = {sp.latex(R_sym)}$ có ba góc "
                    f"$\\hat{{A}} = {sp.latex(A_rad)}, \\hat{{B}} = {sp.latex(B_rad)}, \\hat{{C}} = {sp.latex(C_rad)}$ (radian). "
                    f"Độ dư cầu là $E = \\hat{{A}} + \\hat{{B}} + \\hat{{C}} - \\pi = {sp.latex(excess_sym)}$ (rad)."
                ),
                statement_en=(
                    f"Spherical triangle $ABC$ on a sphere of radius $R = {sp.latex(R_sym)}$ has interior angles "
                    f"$\\hat{{A}} = {sp.latex(A_rad)}, \\hat{{B}} = {sp.latex(B_rad)}, \\hat{{C}} = {sp.latex(C_rad)}$ (radians). "
                    f"The spherical excess is $E = \\hat{{A}} + \\hat{{B}} + \\hat{{C}} - \\pi = {sp.latex(excess_sym)}$ (rad)."
                ),
                latex_formula=f"E = \\hat{{A}} + \\hat{{B}} + \\hat{{C}} - \\pi = {sp.latex(excess_sym)}",
                math_reasons=["Định nghĩa độ dư cầu trong Hình học Cầu / Definition of Spherical Excess"],
            )
        )

        steps.append(
            ProofStep(
                step_number=2,
                title_vi="Áp dụng Định lý Girard tính diện tích tam giác cầu",
                title_en="Apply Girard's Theorem to compute the spherical triangle area",
                statement_vi=(
                    f"Theo Định lý Girard, diện tích tam giác cầu tỉ lệ thuận với độ dư cầu $E$ và bình phương bán kính $R^2$: "
                    f"$S = R^2 \\cdot (\\hat{{A}} + \\hat{{B}} + \\hat{{C}} - \\pi) = {sp.latex(area_sym)}$."
                ),
                statement_en=(
                    f"By Girard's Theorem, the area of a spherical triangle equals the product of $R^2$ and the spherical excess $E$: "
                    f"$S = R^2 \\cdot (\\hat{{A}} + \\hat{{B}} + \\hat{{C}} - \\pi) = {sp.latex(area_sym)}$."
                ),
                latex_formula=(
                    f"S = R^2 \\left(\\hat{{A}} + \\hat{{B}} + \\hat{{C}} - \\pi\\right) "
                    f"= \\left({sp.latex(R_sym)}\\right)^2 \\cdot {sp.latex(excess_sym)} = {sp.latex(area_sym)}"
                ),
                math_reasons=["Định lý Girard (Albert Girard, 1629) / Girard's Spherical Excess Theorem"],
            )
        )

        great_circle_dist: Optional[float] = None
        if lat_lon_pair is not None:
            (lat1_deg, lon1_deg), (lat2_deg, lon2_deg) = lat_lon_pair
            phi1, lam1 = math.radians(lat1_deg), math.radians(lon1_deg)
            phi2, lam2 = math.radians(lat2_deg), math.radians(lon2_deg)
            cos_val = math.sin(phi1) * math.sin(phi2) + math.cos(phi1) * math.cos(phi2) * math.cos(lam2 - lam1)
            cos_val = max(-1.0, min(1.0, cos_val))
            central_angle = math.acos(cos_val)
            great_circle_dist = float(R_sym.evalf()) * central_angle

            steps.append(
                ProofStep(
                    step_number=3,
                    title_vi="Tính khoảng cách cung lớn (Great-Circle Distance)",
                    title_en="Compute the Great-Circle orthodromic distance",
                    statement_vi=(
                        f"Khoảng cách ngắn nhất theo cung tròn lớn giữa hai tọa độ địa lý "
                        f"$(\\phi_1={lat1_deg}^\\circ, \\lambda_1={lon1_deg}^\\circ)$ và $(\\phi_2={lat2_deg}^\\circ, \\lambda_2={lon2_deg}^\\circ)$ "
                        f"là $d = {great_circle_dist:.4f}$."
                    ),
                    statement_en=(
                        f"The shortest great-circle distance between $(\\phi_1={lat1_deg}^\\circ, \\lambda_1={lon1_deg}^\\circ)$ "
                        f"and $(\\phi_2={lat2_deg}^\\circ, \\lambda_2={lon2_deg}^\\circ)$ is $d = {great_circle_dist:.4f}$."
                    ),
                    latex_formula=(
                        "d = R \\cdot \\arccos\\left(\\sin\\phi_1\\sin\\phi_2 + \\cos\\phi_1\\cos\\phi_2\\cos(\\Delta\\lambda)\\right) "
                        f"\\approx {great_circle_dist:.4f}"
                    ),
                    math_reasons=["Định lý Cosin trong Hình học Cầu / Spherical Law of Cosines"],
                )
            )

        area_num = float(area_sym.evalf())
        return DeductiveProofResult(
            problem_id=problem_id,
            topic="Spherical Geometry - Girard's Theorem & Great-Circle Distance",
            steps=steps,
            symbolic_result=area_sym,
            numeric_value=area_num,
            unit="area",
            conclusion_vi=f"Diện tích tam giác cầu theo Định lý Girard là S = {sp.latex(area_sym)} ≈ {area_num:.4f}.",
            conclusion_en=f"The spherical triangle area by Girard's Theorem is S = {sp.latex(area_sym)} ≈ {area_num:.4f}.",
            metadata={
                "spherical_excess_symbolic": excess_sym,
                "spherical_excess": float(excess_sym.evalf()),
                "great_circle_distance": great_circle_dist,
            },
        )

    # ==========================================================================
    # 3. BÀI TOÁN TỐI ƯU HÓA KHÔNG GIAN (AP CALCULUS & SAT OPTIMIZATION)
    # ==========================================================================
    def prove_inscribed_solid_optimization(
        self,
        solid_type: str,
        R: Union[int, float, sp.Expr],
        problem_id: str = "OPTIMIZATION_3D_01",
    ) -> DeductiveProofResult:
        """
        Solves AP Calculus / SAT / Gaokao 3D extremal optimization problems for solids
        inscribed in a sphere of radius R using symbolic differentiation (`sympy.diff`):
        1. `solid_type='cylinder'`: Right circular cylinder of maximum volume in sphere R.
           r_cyl = R * sqrt(2/3), h_cyl = 2R / sqrt(3), V_max = 4 * pi * R^3 / (3 * sqrt(3)).
        2. `solid_type='cone'`: Right circular cone of maximum volume in sphere R.
           h_cone = 4R / 3, r_cone = 2*sqrt(2)*R / 3, V_max = 32 * pi * R^3 / 81.
        """
        steps: List[ProofStep] = []
        R_sym = self._require_positive(R, "bán kính mặt cầu R", "sphere radius R")
        solid_key = solid_type.strip().lower()

        if solid_key == "cylinder":
            h_var = sp.Symbol("h", positive=True)
            r_sq_expr = R_sym ** 2 - (h_var / 2) ** 2
            V_expr = sp.pi * r_sq_expr * h_var
            dV_dh = sp.simplify(sp.diff(V_expr, h_var))

            h_opt = sp.simplify(2 * R_sym / sp.sqrt(3))
            r_opt = sp.simplify(R_sym * sp.sqrt(sp.Rational(2, 3)))
            V_max = sp.simplify(4 * sp.pi * (R_sym ** 3) / (3 * sp.sqrt(3)))

            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Thiết lập hàm mục tiêu thể tích khối trụ theo chiều cao h",
                    title_en="Formulate the cylinder volume objective function in terms of height h",
                    statement_vi=(
                        f"Gọi $h \\in (0, 2R)$ là chiều cao và $r$ là bán kính đáy của hình trụ nội tiếp mặt cầu bán kính $R = {sp.latex(R_sym)}$. "
                        "Theo định lý Pythagore trong thiết diện qua trục: $r^2 + \\left(\\frac{h}{2}\\right)^2 = R^2 \\implies r^2 = R^2 - \\frac{h^2}{4}$. "
                        "Hàm thể tích khối trụ là $V(h) = \\pi r^2 h = \\pi\\left(R^2 h - \\frac{h^3}{4}\\right)$."
                    ),
                    statement_en=(
                        f"Let $h \\in (0, 2R)$ be the altitude and $r$ be the base radius of the cylinder inscribed in a sphere of radius $R = {sp.latex(R_sym)}$. "
                        "By the Pythagorean theorem in the axial section: $r^2 = R^2 - \\frac{h^2}{4}$. "
                        "The cylinder volume function is $V(h) = \\pi\\left(R^2 h - \\frac{h^3}{4}\\right)$."
                    ),
                    latex_formula=f"V(h) = \\pi \\left(R^2 - \\frac{{h^2}}{{4}}\\right) h = {sp.latex(sp.expand(V_expr))}",
                    math_reasons=["Biểu diễn hàm số một biến trên miền xác định (0, 2R) / Single-variable objective formulation"],
                )
            )

            steps.append(
                ProofStep(
                    step_number=2,
                    title_vi="Khảo sát đạo hàm cấp 1 và cấp 2 tìm điểm cực đại toàn cục",
                    title_en="Perform first and second derivative tests for global maximum",
                    statement_vi=(
                        f"Tính đạo hàm $V'(h) = \\pi\\left(R^2 - \\frac{{3h^2}}{{4}}\\right) = {sp.latex(dV_dh)}$. "
                        f"Giải phương trình $V'(h) = 0$ với $h > 0$ ta được $h = \\frac{{2R}}{{\\sqrt{{3}}}} = {sp.latex(h_opt)}$. "
                        f"Vì $V''(h) = -\\frac{{3\\pi h}}{{2}} < 0, \\forall h \\in (0, 2R)$, hàm số đạt cực đại tuyệt đối tại $h = {sp.latex(h_opt)}$."
                    ),
                    statement_en=(
                        f"Differentiating gives $V'(h) = \\pi\\left(R^2 - \\frac{{3h^2}}{{4}}\\right) = {sp.latex(dV_dh)}$. "
                        f"Setting $V'(h) = 0$ for $h > 0$ yields $h = \\frac{{2R}}{{\\sqrt{{3}}}} = {sp.latex(h_opt)}$. "
                        f"Since $V''(h) = -\\frac{{3\\pi h}}{{2}} < 0$ on $(0, 2R)$, this critical point is the unique global maximum."
                    ),
                    latex_formula=(
                        f"V'(h) = 0 \\iff h_{{\\text{{cylinder}}}} = \\frac{{2R}}{{\\sqrt{{3}}}} = {sp.latex(h_opt)}, \\quad "
                        f"r_{{\\text{{cylinder}}}} = R\\sqrt{{\\frac{{2}}{{3}}}} = {sp.latex(r_opt)}"
                    ),
                    math_reasons=[
                        "Định lý Fermat về cực trị khả vi / Fermat's theorem on stationary points",
                        "Tiêu chuẩn đạo hàm cấp hai cho hàm lõm / Second derivative concavity test",
                    ],
                )
            )

            steps.append(
                ProofStep(
                    step_number=3,
                    title_vi="Tính giá trị thể tích cực đại của khối trụ",
                    title_en="Evaluate the maximum volume of the inscribed cylinder",
                    statement_vi=(
                        f"Thay $r = {sp.latex(r_opt)}$ và $h = {sp.latex(h_opt)}$ vào công thức thể tích, "
                        f"ta thu được $V_{{\\max}} = \\frac{{4\\pi R^3}}{{3\\sqrt{{3}}}} = {sp.latex(V_max)}$."
                    ),
                    statement_en=(
                        f"Substituting $r = {sp.latex(r_opt)}$ and $h = {sp.latex(h_opt)}$ into the volume formula "
                        f"gives $V_{{\\max}} = \\frac{{4\\pi R^3}}{{3\\sqrt{{3}}}} = {sp.latex(V_max)}$."
                    ),
                    latex_formula=f"V_{{\\max}} = \\frac{{4\\pi R^3}}{{3\\sqrt{{3}}}} = {sp.latex(V_max)}",
                    math_reasons=["Thay thế điểm dừng tối ưu vào hàm mục tiêu / Evaluation at optimal critical point"],
                )
            )

            v_num = float(V_max.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="3D Optimization - Maximum Volume Cylinder in Sphere",
                steps=steps,
                symbolic_result=V_max,
                numeric_value=v_num,
                unit="volume",
                conclusion_vi=(
                    f"Khối trụ nội tiếp mặt cầu có thể tích lớn nhất V_max = {sp.latex(V_max)} ≈ {v_num:.4f} "
                    f"khi h = {sp.latex(h_opt)} và r = {sp.latex(r_opt)}."
                ),
                conclusion_en=(
                    f"The inscribed cylinder achieves maximum volume V_max = {sp.latex(V_max)} ≈ {v_num:.4f} "
                    f"at height h = {sp.latex(h_opt)} and radius r = {sp.latex(r_opt)}."
                ),
                metadata={
                    "h_opt_symbolic": h_opt,
                    "h_opt": float(h_opt.evalf()),
                    "r_opt_symbolic": r_opt,
                    "r_opt": float(r_opt.evalf()),
                    "V_max_symbolic": V_max,
                    "V_max": v_num,
                },
            )

        elif solid_key == "cone":
            h_var = sp.Symbol("h", positive=True)
            # In a sphere of radius R, a cone of height h has base distance |h - R| from sphere center:
            # r^2 = R^2 - (h - R)^2 = 2*R*h - h^2
            r_sq_expr = 2 * R_sym * h_var - h_var ** 2
            V_expr = sp.Rational(1, 3) * sp.pi * r_sq_expr * h_var
            dV_dh = sp.simplify(sp.diff(V_expr, h_var))

            h_opt = sp.simplify(sp.Rational(4, 3) * R_sym)
            r_opt = sp.simplify(2 * sp.sqrt(2) * R_sym / 3)
            V_max = sp.simplify(sp.Rational(32, 81) * sp.pi * (R_sym ** 3))

            steps.append(
                ProofStep(
                    step_number=1,
                    title_vi="Thiết lập hàm thể tích khối nón nội tiếp mặt cầu theo chiều cao h",
                    title_en="Formulate the inscribed cone volume function in terms of height h",
                    statement_vi=(
                        f"Gọi $h \\in (0, 2R)$ là chiều cao khối nón nội tiếp mặt cầu bán kính $R = {sp.latex(R_sym)}$. "
                        "Khoảng cách từ tâm cầu $I$ đến đáy nón là $|h - R|$, suy ra bán kính đáy nón thỏa mãn "
                        "$r^2 = R^2 - (h - R)^2 = 2Rh - h^2$. Khi đó $V(h) = \\frac{1}{3}\\pi r^2 h = \\frac{\\pi}{3}(2Rh^2 - h^3)$."
                    ),
                    statement_en=(
                        f"Let $h \\in (0, 2R)$ be the altitude of the cone inscribed in a sphere of radius $R = {sp.latex(R_sym)}$. "
                        "The distance from sphere center $I$ to the cone base is $|h - R|$, so the base radius satisfies "
                        "$r^2 = R^2 - (h - R)^2 = 2Rh - h^2$. Hence $V(h) = \\frac{\\pi}{3}(2Rh^2 - h^3)$."
                    ),
                    latex_formula=f"r^2 = 2Rh - h^2, \\quad V(h) = \\frac{{\\pi}}{{3}}\\left(2Rh^2 - h^3\\right) = {sp.latex(sp.expand(V_expr))}",
                    math_reasons=["Hệ thức Pythagore trong thiết diện qua trục của khối nón nội tiếp mặt cầu / Axial Pythagorean relation"],
                )
            )

            steps.append(
                ProofStep(
                    step_number=2,
                    title_vi="Giải phương trình đạo hàm V'(h) = 0 tìm kích thước tối ưu",
                    title_en="Solve V'(h) = 0 for optimal cone dimensions",
                    statement_vi=(
                        f"Đạo hàm theo biến $h$: $V'(h) = \\frac{{\\pi}}{{3}}(4Rh - 3h^2) = {sp.latex(dV_dh)}$. "
                        f"Trên miền $h \\in (0, 2R)$, $V'(h) = 0 \\iff h = \\frac{{4}}{{3}}R = {sp.latex(h_opt)}$. "
                        f"Từ đó bán kính đáy tối ưu là $r = \\sqrt{{2Rh - h^2}} = \\frac{{2\\sqrt{{2}}}}{{3}}R = {sp.latex(r_opt)}$."
                    ),
                    statement_en=(
                        f"Differentiating with respect to $h$ gives $V'(h) = \\frac{{\\pi}}{{3}}(4Rh - 3h^2) = {sp.latex(dV_dh)}$. "
                        f"On $(0, 2R)$, $V'(h) = 0 \\iff h = \\frac{{4}}{{3}}R = {sp.latex(h_opt)}$. "
                        f"The corresponding optimal base radius is $r = \\frac{{2\\sqrt{{2}}}}{{3}}R = {sp.latex(r_opt)}$."
                    ),
                    latex_formula=(
                        f"V'(h) = 0 \\iff h_{{\\text{{cone}}}} = \\frac{{4}}{{3}}R = {sp.latex(h_opt)}, \\quad "
                        f"r_{{\\text{{cone}}}} = \\frac{{2\\sqrt{{2}}}}{{3}}R = {sp.latex(r_opt)}"
                    ),
                    math_reasons=["Ứng dụng đạo hàm tìm giá trị lớn nhất của hàm số / Calculus optimization test"],
                )
            )

            steps.append(
                ProofStep(
                    step_number=3,
                    title_vi="Tính thể tích cực đại của khối nón nội tiếp mặt cầu",
                    title_en="Compute the maximum volume of the inscribed cone",
                    statement_vi=(
                        f"Thay $h = {sp.latex(h_opt)}$ và $r = {sp.latex(r_opt)}$ vào công thức thể tích, "
                        f"ta thu được $V_{{\\max}} = \\frac{{32}}{{81}}\\pi R^3 = {sp.latex(V_max)}$ (bằng $\\frac{{8}}{{27}}$ thể tích khối cầu)."
                    ),
                    statement_en=(
                        f"Substituting $h = {sp.latex(h_opt)}$ and $r = {sp.latex(r_opt)}$ into the volume formula "
                        f"yields $V_{{\\max}} = \\frac{{32}}{{81}}\\pi R^3 = {sp.latex(V_max)}$ (which is $\\frac{{8}}{{27}}$ of the sphere's volume)."
                    ),
                    latex_formula=f"V_{{\\max}} = \\frac{{32}}{{81}}\\pi R^3 = {sp.latex(V_max)}",
                    math_reasons=["Tính giá trị hàm mục tiêu tại điểm cực đại / Objective evaluation at maximum"],
                )
            )

            v_num = float(V_max.evalf())
            return DeductiveProofResult(
                problem_id=problem_id,
                topic="3D Optimization - Maximum Volume Cone in Sphere",
                steps=steps,
                symbolic_result=V_max,
                numeric_value=v_num,
                unit="volume",
                conclusion_vi=(
                    f"Khối nón nội tiếp mặt cầu có thể tích cực đại V_max = {sp.latex(V_max)} ≈ {v_num:.4f} "
                    f"khi chiều cao h = {sp.latex(h_opt)} và bán kính đáy r = {sp.latex(r_opt)}."
                ),
                conclusion_en=(
                    f"The inscribed cone achieves maximum volume V_max = {sp.latex(V_max)} ≈ {v_num:.4f} "
                    f"at height h = {sp.latex(h_opt)} and base radius r = {sp.latex(r_opt)}."
                ),
                metadata={
                    "h_opt_symbolic": h_opt,
                    "h_opt": float(h_opt.evalf()),
                    "r_opt_symbolic": r_opt,
                    "r_opt": float(r_opt.evalf()),
                    "V_max_symbolic": V_max,
                    "V_max": v_num,
                },
            )

        raise PedagogicalGeometryError(
            f"Loại khối '{solid_type}' không được hỗ trợ trong bài toán tối ưu nội tiếp mặt cầu (chỉ hỗ trợ 'cylinder' hoặc 'cone').",
            f"Solid type '{solid_type}' is not supported for sphere optimization (use 'cylinder' or 'cone').",
            error_code="ERR_UNSUPPORTED_OPTIMIZATION_SOLID",
        )

    # ==========================================================================
    # 4a. KHOẢNG CÁCH GIỮA HAI ĐƯỜNG THẲNG CHÉO NHAU & ĐOẠN VUÔNG GÓC CHUNG
    # ==========================================================================
    def prove_distance_skew_lines(
        self,
        m1: Point3D,
        u1: Vector3D,
        m2: Point3D,
        u2: Vector3D,
        problem_id: str = "SKEW_LINES_01",
    ) -> DeductiveProofResult:
        """
        Computes the exact shortest distance between two skew lines:
            Delta_1 passing through M1 with direction vector u1
            Delta_2 passing through M2 with direction vector u2
        Formula:
            d(Delta_1, Delta_2) = |[u1, u2] . M1M2| / |[u1, u2]|
        Also solves analytically for the exact coordinates of the common perpendicular
        segment endpoints A in Delta_1 and B in Delta_2.
        """
        if u1.is_zero() or u2.is_zero():
            raise PedagogicalGeometryError(
                "Vector chỉ phương của đường thẳng không được bằng vector không.",
                "Line direction vector cannot be the zero vector.",
                error_code="ERR_ZERO_DIRECTION_VECTOR",
            )

        steps: List[ProofStep] = []
        u1_mat = u1.to_sympy_matrix()
        u2_mat = u2.to_sympy_matrix()
        m1_mat = sp.Matrix(list(m1.to_sympy()))
        m2_mat = sp.Matrix(list(m2.to_sympy()))
        m1m2_mat = m2_mat - m1_mat

        cross_mat = u1_mat.cross(u2_mat)
        cross_norm_sq = sp.simplify(cross_mat.dot(cross_mat))
        if float(cross_norm_sq.evalf()) <= self.EPSILON:
            raise PedagogicalGeometryError(
                "Hai đường thẳng có vector chỉ phương cùng phương (song song hoặc trùng nhau), không phải hai đường thẳng chéo nhau.",
                "The two lines have collinear direction vectors (parallel or coincident); they are not skew lines.",
                error_code="ERR_LINES_PARALLEL_OR_COINCIDENT",
            )

        scalar_triple = sp.simplify(cross_mat.dot(m1m2_mat))
        cross_norm = sp.simplify(sp.sqrt(cross_norm_sq))
        dist_sym = sp.simplify(sp.Abs(scalar_triple) / cross_norm)

        steps.append(
            ProofStep(
                step_number=1,
                title_vi="Tính tích có hướng của hai vector chỉ phương và vector nối M1M2",
                title_en="Compute the cross product of direction vectors and connecting vector M1M2",
                statement_vi=(
                    f"Đường thẳng $\\Delta_1$ đi qua $M_1{m1.to_tuple()}$ có VTCP $\\vec{{u}}_1 = {u1.to_tuple()}$; "
                    f"$\\Delta_2$ đi qua $M_2{m2.to_tuple()}$ có VTCP $\\vec{{u}}_2 = {u2.to_tuple()}$. "
                    f"Ta có $[\\vec{{u}}_1, \\vec{{u}}_2] = ({sp.latex(cross_mat[0])}; {sp.latex(cross_mat[1])}; {sp.latex(cross_mat[2])})$ "
                    f"và $\\overrightarrow{{M_1 M_2}} = ({sp.latex(m1m2_mat[0])}; {sp.latex(m1m2_mat[1])}; {sp.latex(m1m2_mat[2])})$."
                ),
                statement_en=(
                    f"Line $\\Delta_1$ passes through $M_1{m1.to_tuple()}$ with direction $\\vec{{u}}_1 = {u1.to_tuple()}$; "
                    f"$\\Delta_2$ passes through $M_2{m2.to_tuple()}$ with direction $\\vec{{u}}_2 = {u2.to_tuple()}$. "
                    f"We obtain $[\\vec{{u}}_1, \\vec{{u}}_2] = ({sp.latex(cross_mat[0])}; {sp.latex(cross_mat[1])}; {sp.latex(cross_mat[2])})$ "
                    f"and $\\overrightarrow{{M_1 M_2}} = ({sp.latex(m1m2_mat[0])}; {sp.latex(m1m2_mat[1])}; {sp.latex(m1m2_mat[2])})$."
                ),
                latex_formula=(
                    f"[\\vec{{u}}_1, \\vec{{u}}_2] = \\begin{{pmatrix}} {sp.latex(cross_mat[0])} \\\\ {sp.latex(cross_mat[1])} \\\\ {sp.latex(cross_mat[2])} \\end{{pmatrix}}, \\quad "
                    f"\\overrightarrow{{M_1 M_2}} = \\begin{{pmatrix}} {sp.latex(m1m2_mat[0])} \\\\ {sp.latex(m1m2_mat[1])} \\\\ {sp.latex(m1m2_mat[2])} \\end{{pmatrix}}"
                ),
                math_reasons=["Tích có hướng của hai vector trong không gian Oxyz / 3D vector cross product"],
            )
        )

        steps.append(
            ProofStep(
                step_number=2,
                title_vi="Áp dụng công thức tích hỗn tạp tính khoảng cách giữa hai đường thẳng chéo nhau",
                title_en="Apply scalar triple product formula for distance between skew lines",
                statement_vi=(
                    f"Tích hỗn tạp $[\\vec{{u}}_1, \\vec{{u}}_2] \\cdot \\overrightarrow{{M_1 M_2}} = {sp.latex(scalar_triple)}$ "
                    f"và $\\|[\\vec{{u}}_1, \\vec{{u}}_2]\\| = {sp.latex(cross_norm)}$. "
                    f"Khoảng cách giữa $\\Delta_1$ và $\\Delta_2$ là $d(\\Delta_1, \\Delta_2) = {sp.latex(dist_sym)}$."
                ),
                statement_en=(
                    f"The scalar triple product is $[\\vec{{u}}_1, \\vec{{u}}_2] \\cdot \\overrightarrow{{M_1 M_2}} = {sp.latex(scalar_triple)}$ "
                    f"with norm $\\|[\\vec{{u}}_1, \\vec{{u}}_2]\\| = {sp.latex(cross_norm)}$. "
                    f"Thus the distance between $\\Delta_1$ and $\\Delta_2$ is $d(\\Delta_1, \\Delta_2) = {sp.latex(dist_sym)}$."
                ),
                latex_formula=(
                    f"d(\\Delta_1, \\Delta_2) = \\frac{{|[\\vec{{u}}_1, \\vec{{u}}_2] \\cdot \\overrightarrow{{M_1 M_2}}|}}{{\\|[\\vec{{u}}_1, \\vec{{u}}_2]\\|}} "
                    f"= \\frac{{|{sp.latex(scalar_triple)}|}}{{{sp.latex(cross_norm)}}} = {sp.latex(dist_sym)}"
                ),
                math_reasons=[
                    "Công thức khoảng cách giữa hai đường thẳng chéo nhau bằng tích hỗn tạp / Skew lines distance via scalar triple product"
                ],
            )
        )

        # Step 3: Find exact coordinates of common perpendicular endpoints A(t1) on Delta_1 and B(t2) on Delta_2
        t1, t2 = sp.symbols("t1 t2", real=True)
        A_vec = m1_mat + t1 * u1_mat
        B_vec = m2_mat + t2 * u2_mat
        AB_vec = B_vec - A_vec

        eq1 = sp.Eq(AB_vec.dot(u1_mat), 0)
        eq2 = sp.Eq(AB_vec.dot(u2_mat), 0)
        sol = sp.solve([eq1, eq2], (t1, t2), dict=True)

        A_pt_sym = tuple(sp.simplify(A_vec[i].subs(sol[0])) for i in range(3))
        B_pt_sym = tuple(sp.simplify(B_vec[i].subs(sol[0])) for i in range(3))
        A_pt = Point3D(float(A_pt_sym[0].evalf()), float(A_pt_sym[1].evalf()), float(A_pt_sym[2].evalf()), name="A")
        B_pt = Point3D(float(B_pt_sym[0].evalf()), float(B_pt_sym[1].evalf()), float(B_pt_sym[2].evalf()), name="B")

        steps.append(
            ProofStep(
                step_number=3,
                title_vi="Xác định tọa độ hai đầu mút đoạn vuông góc chung AB",
                title_en="Determine the coordinates of the common perpendicular segment AB",
                statement_vi=(
                    "Gọi $A(t_1) \\in \\Delta_1$ và $B(t_2) \\in \\Delta_2$ là hai đầu mút đoạn vuông góc chung. "
                    "Giải hệ $\\begin{cases} \\overrightarrow{AB} \\cdot \\vec{u}_1 = 0 \\\\ \\overrightarrow{AB} \\cdot \\vec{u}_2 = 0 \\end{cases}$ "
                    f"ta được $A({sp.latex(A_pt_sym[0])}; {sp.latex(A_pt_sym[1])}; {sp.latex(A_pt_sym[2])})$ và "
                    f"$B({sp.latex(B_pt_sym[0])}; {sp.latex(B_pt_sym[1])}; {sp.latex(B_pt_sym[2])})$."
                ),
                statement_en=(
                    "Let $A(t_1) \\in \\Delta_1$ and $B(t_2) \\in \\Delta_2$ be the endpoints of the common perpendicular. "
                    "Solving $\\overrightarrow{AB} \\cdot \\vec{u}_1 = 0$ and $\\overrightarrow{AB} \\cdot \\vec{u}_2 = 0$ yields "
                    f"$A({sp.latex(A_pt_sym[0])}; {sp.latex(A_pt_sym[1])}; {sp.latex(A_pt_sym[2])})$ and "
                    f"$B({sp.latex(B_pt_sym[0])}; {sp.latex(B_pt_sym[1])}; {sp.latex(B_pt_sym[2])})$."
                ),
                latex_formula=(
                    f"A = \\left({sp.latex(A_pt_sym[0])}, {sp.latex(A_pt_sym[1])}, {sp.latex(A_pt_sym[2])}\\right), \\quad "
                    f"B = \\left({sp.latex(B_pt_sym[0])}, {sp.latex(B_pt_sym[1])}, {sp.latex(B_pt_sym[2])}\\right)"
                ),
                math_reasons=["Điều kiện vuông góc của đoạn vuông góc chung với hai đường thẳng / Orthogonality conditions of common perpendicular"],
            )
        )

        dist_num = float(dist_sym.evalf())
        return DeductiveProofResult(
            problem_id=problem_id,
            topic="Distance & Common Perpendicular Between Skew Lines",
            steps=steps,
            symbolic_result=dist_sym,
            numeric_value=dist_num,
            unit="length",
            conclusion_vi=(
                f"Khoảng cách giữa hai đường thẳng là d = {sp.latex(dist_sym)} ≈ {dist_num:.4f}; "
                f"đoạn vuông góc chung nối A{A_pt.to_tuple()} và B{B_pt.to_tuple()}."
            ),
            conclusion_en=(
                f"The distance between the skew lines is d = {sp.latex(dist_sym)} ≈ {dist_num:.4f}; "
                f"the common perpendicular connects A{A_pt.to_tuple()} and B{B_pt.to_tuple()}."
            ),
            metadata={
                "point_A": A_pt,
                "point_B": B_pt,
                "point_A_tuple": A_pt.to_tuple(),
                "point_B_tuple": B_pt.to_tuple(),
            },
        )

    # ==========================================================================
    # 4b. KHOẢNG CÁCH TỪ ĐIỂM ĐẾN MẶT PHẲNG & HÌNH CHIẾU VUÔNG GÓC
    # ==========================================================================
    def prove_distance_point_to_plane(
        self,
        point: Point3D,
        plane: Plane3D,
        problem_id: str = "DIST_POINT_PLANE_01",
    ) -> DeductiveProofResult:
        """
        Computes the exact distance from point M0(x0, y0, z0) to plane (P): Ax + By + Cz + D = 0:
            d(M0, (P)) = |A*x0 + B*y0 + C*z0 + D| / sqrt(A^2 + B^2 + C^2)
        Also determines the exact projection coordinates of H on (P).
        """
        A_sym = sp.Rational(str(round(plane.A, 6))) if isinstance(plane.A, float) else sp.sympify(plane.A)
        B_sym = sp.Rational(str(round(plane.B, 6))) if isinstance(plane.B, float) else sp.sympify(plane.B)
        C_sym = sp.Rational(str(round(plane.C, 6))) if isinstance(plane.C, float) else sp.sympify(plane.C)
        D_sym = sp.Rational(str(round(plane.D, 6))) if isinstance(plane.D, float) else sp.sympify(plane.D)

        x0 = sp.Rational(str(round(point.x, 6))) if isinstance(point.x, float) else sp.sympify(point.x)
        y0 = sp.Rational(str(round(point.y, 6))) if isinstance(point.y, float) else sp.sympify(point.y)
        z0 = sp.Rational(str(round(point.z, 6))) if isinstance(point.z, float) else sp.sympify(point.z)

        numerator = sp.Abs(A_sym * x0 + B_sym * y0 + C_sym * z0 + D_sym)
        denom_sq = A_sym**2 + B_sym**2 + C_sym**2
        denom = sp.sqrt(denom_sq)
        dist_sym = sp.simplify(numerator / denom)
        dist_val = float(dist_sym.evalf())

        # Projection H:
        t_val = -(A_sym * x0 + B_sym * y0 + C_sym * z0 + D_sym) / denom_sq
        hx = sp.simplify(x0 + A_sym * t_val)
        hy = sp.simplify(y0 + B_sym * t_val)
        hz = sp.simplify(z0 + C_sym * t_val)

        steps = [
            ProofStep(
                step_number=1,
                title_vi="Xác định tọa độ điểm và phương trình tổng quát của mặt phẳng",
                title_en="Identify point coordinates and plane equation",
                statement_vi=(
                    f"Điểm cần tính khoảng cách là ${point.name}({point.x:.2f}; {point.y:.2f}; {point.z:.2f})$. "
                    f"Mặt phẳng $(P)$ có phương trình tổng quát: ${sp.latex(A_sym)}x + {sp.latex(B_sym)}y + {sp.latex(C_sym)}z + {sp.latex(D_sym)} = 0$ "
                    f"với vector pháp tuyến $\\vec{{n}} = ({sp.latex(A_sym)}; {sp.latex(B_sym)}; {sp.latex(C_sym)})$."
                ),
                statement_en=(
                    f"Point is ${point.name}({point.x:.2f}; {point.y:.2f}; {point.z:.2f})$. "
                    f"Plane $(P)$ has equation: ${sp.latex(A_sym)}x + {sp.latex(B_sym)}y + {sp.latex(C_sym)}z + {sp.latex(D_sym)} = 0$ "
                    f"with normal vector $\\vec{{n}} = ({sp.latex(A_sym)}; {sp.latex(B_sym)}; {sp.latex(C_sym)})$."
                ),
                latex_formula=f"\\vec{{n}} = ({sp.latex(A_sym)}, {sp.latex(B_sym)}, {sp.latex(C_sym)}), \\quad \\|\\vec{{n}}\\| = {sp.latex(denom)}",
                math_reasons=["Phương trình mặt phẳng trong không gian Oxyz / General plane equation"],
            ),
            ProofStep(
                step_number=2,
                title_vi="Áp dụng công thức khoảng cách từ một điểm đến mặt phẳng",
                title_en="Apply distance formula from a point to a plane",
                statement_vi=(
                    f"Khoảng cách từ điểm ${point.name}$ đến mặt phẳng $(P)$ được tính theo công thức: "
                    f"$d({point.name}, (P)) = \\frac{{|A x_0 + B y_0 + C z_0 + D|}}{{\\sqrt{{A^2 + B^2 + C^2}}}} = {sp.latex(dist_sym)}$, "
                    f"xấp xỉ bằng ${dist_val:.4f}$ đơn vị độ dài."
                ),
                statement_en=(
                    f"The distance from point ${point.name}$ to plane $(P)$ is given by: "
                    f"$d({point.name}, (P)) = \\frac{{|A x_0 + B y_0 + C z_0 + D|}}{{\\sqrt{{A^2 + B^2 + C^2}}}} = {sp.latex(dist_sym)}$, "
                    f"approximately ${dist_val:.4f}$ length units."
                ),
                latex_formula=(
                    f"d({point.name}, (P)) = \\frac{{|{sp.latex(A_sym)}({sp.latex(x0)}) + {sp.latex(B_sym)}({sp.latex(y0)}) + {sp.latex(C_sym)}({sp.latex(z0)}) + {sp.latex(D_sym)}|}}{{\\sqrt{{{sp.latex(A_sym)}^2 + {sp.latex(B_sym)}^2 + {sp.latex(C_sym)}^2}}}} = {sp.latex(dist_sym)}"
                ),
                math_reasons=["Công thức tính khoảng cách từ điểm đến mặt phẳng (SGK Hình học 12 GDPT 2018) / Point-plane distance"],
            ),
            ProofStep(
                step_number=3,
                title_vi="Xác định tọa độ hình chiếu vuông góc H lên mặt phẳng",
                title_en="Determine projection point H onto the plane",
                statement_vi=(
                    f"Đường thẳng qua ${point.name}$ vuông góc với $(P)$ nhận $\\vec{{n}}$ làm VTCP. "
                    f"Hình chiếu vuông góc $H$ có tọa độ: $H({sp.latex(hx)}; {sp.latex(hy)}; {sp.latex(hz)})$, "
                    f"với độ dài đoạn $MH = d({point.name}, (P)) = {sp.latex(dist_sym)}$."
                ),
                statement_en=(
                    f"The line through ${point.name}$ perpendicular to $(P)$ has direction $\\vec{{n}}$. "
                    f"The orthogonal projection $H$ is: $H({sp.latex(hx)}; {sp.latex(hy)}; {sp.latex(hz)})$, "
                    f"with segment length $MH = d({point.name}, (P)) = {sp.latex(dist_sym)}$."
                ),
                latex_formula=f"H = ({sp.latex(hx)}, {sp.latex(hy)}, {sp.latex(hz)})",
                math_reasons=["Hình chiếu vuông góc của điểm lên mặt phẳng / Orthogonal projection"],
            ),
        ]

        return DeductiveProofResult(
            problem_id=problem_id,
            topic="Distance from Point to Plane",
            steps=steps,
            symbolic_result=dist_sym,
            numeric_value=dist_val,
            unit="length units",
            conclusion_vi=f"Khoảng cách d({point.name}, (P)) = {sp.latex(dist_sym)} ≈ {dist_val:.4f}. Hình chiếu H = ({float(hx.evalf()):.2f}, {float(hy.evalf()):.2f}, {float(hz.evalf()):.2f}).",
            conclusion_en=f"Distance d({point.name}, (P)) = {sp.latex(dist_sym)} ≈ {dist_val:.4f}. Projection H = ({float(hx.evalf()):.2f}, {float(hy.evalf()):.2f}, {float(hz.evalf()):.2f}).",
            metadata={"projection_H": (float(hx.evalf()), float(hy.evalf()), float(hz.evalf())), "dist": dist_val},
        )

    # ==========================================================================
    # 4c. GÓC GIỮA ĐƯỜNG THẲNG VÀ MẶT PHẲNG
    # ==========================================================================
    def prove_angle_line_plane(
        self,
        u_line: Vector3D,
        plane: Plane3D,
        problem_id: str = "ANGLE_LINE_PLANE_01",
    ) -> DeductiveProofResult:
        """
        Proves the angle phi in [0, 90 deg] between a line with direction vector `u_line`
        and a plane with normal vector `n_plane`:
            sin(phi) = |u . n| / (||u|| * ||n||)
        Returns symbolic_result = sin(phi) and numeric_value = angle in degrees.
        """
        if u_line.is_zero():
            raise PedagogicalGeometryError(
                "Vector chỉ phương của đường thẳng không được bằng vector không.",
                "Line direction vector cannot be the zero vector.",
                error_code="ERR_ZERO_DIRECTION_VECTOR",
            )

        u_mat = u_line.to_sympy_matrix()
        n_mat = plane.normal.to_sympy_matrix()

        dot_abs = sp.Abs(u_mat.dot(n_mat))
        u_norm = sp.sqrt(u_mat.dot(u_mat))
        n_norm = sp.sqrt(n_mat.dot(n_mat))
        sin_phi_sym = sp.simplify(dot_abs / (u_norm * n_norm))
        sin_val = max(0.0, min(1.0, float(sin_phi_sym.evalf())))
        phi_deg = math.degrees(math.asin(sin_val))

        steps = [
            ProofStep(
                step_number=1,
                title_vi="Xác định vector chỉ phương đường thẳng và vector pháp tuyến mặt phẳng",
                title_en="Identify the line direction vector and plane normal vector",
                statement_vi=(
                    f"Đường thẳng $d$ có vector chỉ phương $\\vec{{u}} = {u_line.to_tuple()}$ với $\\|\\vec{{u}}\\| = {sp.latex(u_norm)}$. "
                    f"Mặt phẳng $(P)$ có vector pháp tuyến $\\vec{{n}} = {plane.normal.to_tuple()}$ với $\\|\\vec{{n}}\\| = {sp.latex(n_norm)}$."
                ),
                statement_en=(
                    f"Line $d$ has direction vector $\\vec{{u}} = {u_line.to_tuple()}$ with $\\|\\vec{{u}}\\| = {sp.latex(u_norm)}$. "
                    f"Plane $(P)$ has normal vector $\\vec{{n}} = {plane.normal.to_tuple()}$ with $\\|\\vec{{n}}\\| = {sp.latex(n_norm)}$."
                ),
                latex_formula=f"\\|\\vec{{u}}\\| = {sp.latex(u_norm)}, \\quad \\|\\vec{{n}}\\| = {sp.latex(n_norm)}",
                math_reasons=["Chuẩn Euclid của vector trong không gian Oxyz / Euclidean vector norm"],
            ),
            ProofStep(
                step_number=2,
                title_vi="Tính sin của góc giữa đường thẳng và mặt phẳng",
                title_en="Compute the sine of the angle between the line and the plane",
                statement_vi=(
                    f"Gọi $\\varphi \\in [0^\\circ, 90^\\circ]$ là góc giữa đường thẳng $d$ và mặt phẳng $(P)$. "
                    f"Ta có $\\sin\\varphi = \\frac{{|\\vec{{u}} \\cdot \\vec{{n}}|}}{{\\|\\vec{{u}}\\| \\cdot \\|\\vec{{n}}\\|}} = {sp.latex(sin_phi_sym)}$, "
                    f"suy ra $\\varphi \\approx {phi_deg:.4f}^\\circ$."
                ),
                statement_en=(
                    f"Let $\\varphi \\in [0^\\circ, 90^\\circ]$ be the angle between line $d$ and plane $(P)$. "
                    f"Then $\\sin\\varphi = \\frac{{|\\vec{{u}} \\cdot \\vec{{n}}|}}{{\\|\\vec{{u}}\\| \\cdot \\|\\vec{{n}}\\|}} = {sp.latex(sin_phi_sym)}$, "
                    f"which gives $\\varphi \\approx {phi_deg:.4f}^\\circ$."
                ),
                latex_formula=(
                    f"\\sin\\varphi = \\frac{{|\\vec{{u}} \\cdot \\vec{{n}}|}}{{\\|\\vec{{u}}\\| \\|\\vec{{n}}\\|}} "
                    f"= \\frac{{{sp.latex(dot_abs)}}}{{{sp.latex(u_norm)} \\cdot {sp.latex(n_norm)}}} = {sp.latex(sin_phi_sym)}"
                ),
                math_reasons=["Công thức góc giữa đường thẳng và mặt phẳng (SGK Toán 12 GDPT 2018) / Line-plane angle formula"],
            ),
        ]

        return DeductiveProofResult(
            problem_id=problem_id,
            topic="Angle Between Line and Plane",
            steps=steps,
            symbolic_result=sin_phi_sym,
            numeric_value=phi_deg,
            unit="degrees",
            conclusion_vi=f"sin(phi) = {sp.latex(sin_phi_sym)}, góc giữa đường thẳng và mặt phẳng là phi ≈ {phi_deg:.4f}°.",
            conclusion_en=f"sin(phi) = {sp.latex(sin_phi_sym)}, the angle between the line and plane is phi ≈ {phi_deg:.4f}°.",
            metadata={"sin_phi": sin_val, "angle_rad": math.asin(sin_val), "angle_deg": phi_deg},
        )

    # ==========================================================================
    # 4c. GÓC GIỮA HAI MẶT PHẲNG
    # ==========================================================================
    def prove_angle_between_planes(
        self,
        plane1: Plane3D,
        plane2: Plane3D,
        problem_id: str = "ANGLE_PLANES_01",
    ) -> DeductiveProofResult:
        """
        Proves the dihedral angle theta in [0, 90 deg] between two planes:
            cos(theta) = |n1 . n2| / (||n1|| * ||n2||)
        Returns symbolic_result = cos(theta) and numeric_value = angle in degrees.
        """
        n1_mat = plane1.normal.to_sympy_matrix()
        n2_mat = plane2.normal.to_sympy_matrix()

        dot_abs = sp.Abs(n1_mat.dot(n2_mat))
        n1_norm = sp.sqrt(n1_mat.dot(n1_mat))
        n2_norm = sp.sqrt(n2_mat.dot(n2_mat))
        cos_theta_sym = sp.simplify(dot_abs / (n1_norm * n2_norm))
        cos_val = max(0.0, min(1.0, float(cos_theta_sym.evalf())))
        theta_deg = math.degrees(math.acos(cos_val))

        steps = [
            ProofStep(
                step_number=1,
                title_vi="Xác định cặp vector pháp tuyến của hai mặt phẳng",
                title_en="Identify the normal vectors of the two planes",
                statement_vi=(
                    f"Mặt phẳng $(P_1)$ có VTPT $\\vec{{n}}_1 = {plane1.normal.to_tuple()}$ ($\\|\\vec{{n}}_1\\| = {sp.latex(n1_norm)}$); "
                    f"mặt phẳng $(P_2)$ có VTPT $\\vec{{n}}_2 = {plane2.normal.to_tuple()}$ ($\\|\\vec{{n}}_2\\| = {sp.latex(n2_norm)}$)."
                ),
                statement_en=(
                    f"Plane $(P_1)$ has normal $\\vec{{n}}_1 = {plane1.normal.to_tuple()}$ ($\\|\\vec{{n}}_1\\| = {sp.latex(n1_norm)}$); "
                    f"plane $(P_2)$ has normal $\\vec{{n}}_2 = {plane2.normal.to_tuple()}$ ($\\|\\vec{{n}}_2\\| = {sp.latex(n2_norm)}$)."
                ),
                latex_formula=f"\\|\\vec{{n}}_1\\| = {sp.latex(n1_norm)}, \\quad \\|\\vec{{n}}_2\\| = {sp.latex(n2_norm)}",
                math_reasons=["Vector pháp tuyến của mặt phẳng trong Oxyz / Plane normal vectors"],
            ),
            ProofStep(
                step_number=2,
                title_vi="Tính cosin của góc giữa hai mặt phẳng",
                title_en="Compute the cosine of the angle between the two planes",
                statement_vi=(
                    f"Gọi $\\theta \\in [0^\\circ, 90^\\circ]$ là góc giữa hai mặt phẳng $(P_1)$ và $(P_2)$. "
                    f"Ta có $\\cos\\theta = \\frac{{|\\vec{{n}}_1 \\cdot \\vec{{n}}_2|}}{{\\|\\vec{{n}}_1\\| \\cdot \\|\\vec{{n}}_2\\|}} = {sp.latex(cos_theta_sym)}$, "
                    f"suy ra $\\theta \\approx {theta_deg:.4f}^\\circ$."
                ),
                statement_en=(
                    f"Let $\\theta \\in [0^\\circ, 90^\\circ]$ be the angle between planes $(P_1)$ and $(P_2)$. "
                    f"Then $\\cos\\theta = \\frac{{|\\vec{{n}}_1 \\cdot \\vec{{n}}_2|}}{{\\|\\vec{{n}}_1\\| \\cdot \\|\\vec{{n}}_2\\|}} = {sp.latex(cos_theta_sym)}$, "
                    f"giving $\\theta \\approx {theta_deg:.4f}^\\circ$."
                ),
                latex_formula=(
                    f"\\cos\\theta = \\frac{{|\\vec{{n}}_1 \\cdot \\vec{{n}}_2|}}{{\\|\\vec{{n}}_1\\| \\|\\vec{{n}}_2\\|}} "
                    f"= \\frac{{{sp.latex(dot_abs)}}}{{{sp.latex(n1_norm)} \\cdot {sp.latex(n2_norm)}}} = {sp.latex(cos_theta_sym)}"
                ),
                math_reasons=["Công thức góc giữa hai mặt phẳng (SGK Toán 12 GDPT 2018) / Angle between two planes"],
            ),
        ]

        return DeductiveProofResult(
            problem_id=problem_id,
            topic="Angle Between Two Planes",
            steps=steps,
            symbolic_result=cos_theta_sym,
            numeric_value=theta_deg,
            unit="degrees",
            conclusion_vi=f"cos(theta) = {sp.latex(cos_theta_sym)}, góc giữa hai mặt phẳng là theta ≈ {theta_deg:.4f}°.",
            conclusion_en=f"cos(theta) = {sp.latex(cos_theta_sym)}, the angle between the two planes is theta ≈ {theta_deg:.4f}°.",
            metadata={"cos_theta": cos_val, "angle_rad": math.acos(cos_val), "angle_deg": theta_deg},
        )


# ==============================================================================
# 6. BỘ KIỂM THỬ TỰ ĐỘNG BẢO ĐẢM CHẤT LƯỢNG (8 MANDATORY UNIT TESTS)
# ==============================================================================
def run_all_unit_tests() -> None:
    """
    Executes the 8 mandatory quality-assurance tests verifying exact symbolic
    and floating-point compliance.
    """
    engine = Deductive3DEngine()
    print("=" * 78)
    print("RUNNING DEDUCTIVE 3D ENGINE VERIFICATION SUITE (8 MANDATORY UNIT TESTS)")
    print("=" * 78)

    # --------------------------------------------------------------------------
    # Test 1: Mặt cầu ngoại tiếp hình chóp S.ABC có SA perp (ABC),
    # tam giác ABC vuông tại B (AB=3, BC=4, SA=12). Kỳ vọng R = 6.5.
    # --------------------------------------------------------------------------
    res1 = engine.prove_circumscribed_sphere(
        case_type="perp_lateral_edge",
        ab=3,
        bc=4,
        SA=12,
        problem_id="TEST_01_CIRCUM_PYRAMID",
    )
    assert math.isclose(res1.numeric_value, 6.5, rel_tol=1e-9), f"Test 1 Failed: got {res1.numeric_value}"
    assert sp.simplify(res1.symbolic_result - sp.Rational(13, 2)) == 0
    print(f"[PASS] Test 1: R = {res1.symbolic_result} = {res1.numeric_value:.4f} (Expected: 6.5)")

    # --------------------------------------------------------------------------
    # Test 2: Mặt cầu ngoại tiếp tứ diện đều cạnh a=6.
    # Kỳ vọng R = 6*sqrt(6)/4 = 3*sqrt(6)/2 ≈ 3.6742346.
    # --------------------------------------------------------------------------
    res2 = engine.prove_circumscribed_sphere(
        case_type="regular_tetrahedron",
        a=6,
        problem_id="TEST_02_REGULAR_TETRAHEDRON",
    )
    expected_r2 = 6.0 * math.sqrt(6.0) / 4.0
    assert math.isclose(res2.numeric_value, expected_r2, rel_tol=1e-9), f"Test 2 Failed: got {res2.numeric_value}"
    assert math.isclose(res2.numeric_value, 3.6742, abs_tol=1e-4)
    print(f"[PASS] Test 2: R = {res2.symbolic_result} ≈ {res2.numeric_value:.4f} (Expected: 3.6742)")

    # --------------------------------------------------------------------------
    # Test 3: Thiết diện mặt cầu tâm I(1, 2, -1), bán kính R=5 cắt bởi mặt phẳng
    # (P): 2x - 2y + z + 6 = 0. Khoảng cách d=1, bán kính thiết diện r=sqrt(24)≈4.899.
    # --------------------------------------------------------------------------
    sphere3 = Sphere3D(center=Point3D(1, 2, -1, name="I"), radius=5.0)
    plane3 = Plane3D(2, -2, 1, 6, name="(P)")
    res3 = engine.prove_plane_sphere_intersection(
        sphere=sphere3,
        plane=plane3,
        problem_id="TEST_03_PLANE_SPHERE_SECANT",
    )
    assert math.isclose(res3.metadata["d"], 1.0, rel_tol=1e-9), f"Test 3 d Failed: {res3.metadata['d']}"
    assert math.isclose(res3.numeric_value, math.sqrt(24.0), rel_tol=1e-9), f"Test 3 r Failed: {res3.numeric_value}"
    assert math.isclose(res3.numeric_value, 4.8990, abs_tol=1e-3)
    print(f"[PASS] Test 3: d = {res3.metadata['d']}, r = {res3.symbolic_result} ≈ {res3.numeric_value:.4f}")

    # --------------------------------------------------------------------------
    # Test 4: Chỏm cầu có R=5, d=3 => h=2.
    # Diện tích chỏm cầu S_cap = 20*pi, thể tích V_cap = 52*pi/3.
    # --------------------------------------------------------------------------
    res4 = engine.prove_plane_sphere_intersection(
        R=5,
        d=3,
        problem_id="TEST_04_SPHERICAL_CAP",
    )
    assert math.isclose(res4.metadata["h_cap"], 2.0, rel_tol=1e-9)
    assert sp.simplify(res4.metadata["S_cap_symbolic"] - 20 * sp.pi) == 0
    assert sp.simplify(res4.metadata["V_cap_symbolic"] - sp.Rational(52, 3) * sp.pi) == 0
    assert math.isclose(res4.metadata["S_cap"], 20.0 * math.pi, rel_tol=1e-9)
    assert math.isclose(res4.metadata["V_cap"], (52.0 * math.pi) / 3.0, rel_tol=1e-9)
    print(
        f"[PASS] Test 4: h = {res4.metadata['h_cap']}, "
        f"S_cap = {res4.metadata['S_cap_symbolic']}, V_cap = {res4.metadata['V_cap_symbolic']}"
    )

    # --------------------------------------------------------------------------
    # Test 5: Mặt cầu nội tiếp hình chóp tứ giác đều có đáy cạnh a=4, chiều cao h=4.
    # Kiểm tra bán kính r = 3V / S_tp.
    # --------------------------------------------------------------------------
    res5 = engine.prove_inscribed_sphere(
        case_type="regular_quad_pyramid",
        a=4,
        h=4,
        problem_id="TEST_05_INSCRIBED_QUAD_PYRAMID",
    )
    expected_v5 = (1.0 / 3.0) * (4.0 ** 2) * 4.0
    expected_slant5 = math.sqrt(4.0 ** 2 + 2.0 ** 2)
    expected_stp5 = 16.0 + 2.0 * 4.0 * expected_slant5
    expected_r5 = (3.0 * expected_v5) / expected_stp5
    assert math.isclose(res5.numeric_value, expected_r5, rel_tol=1e-9), f"Test 5 Failed: got {res5.numeric_value}"
    print(f"[PASS] Test 5: r = 3V/S_tp = {res5.symbolic_result} ≈ {res5.numeric_value:.4f}")

    # --------------------------------------------------------------------------
    # Test 6: Khoảng cách giữa 2 đường thẳng chéo nhau:
    # Trục Ox (qua O(0,0,0), vtcp (1,0,0)) và đường thẳng qua M(0, 1, 2) có vtcp (0, 1, 0).
    # Khoảng cách kỳ vọng = 2.
    # --------------------------------------------------------------------------
    res6 = engine.prove_distance_skew_lines(
        m1=Point3D(0, 0, 0, name="O"),
        u1=Vector3D(1, 0, 0),
        m2=Point3D(0, 1, 2, name="M"),
        u2=Vector3D(0, 1, 0),
        problem_id="TEST_06_SKEW_LINES",
    )
    assert math.isclose(res6.numeric_value, 2.0, rel_tol=1e-9), f"Test 6 Failed: got {res6.numeric_value}"
    assert res6.metadata["point_A_tuple"] == (0.0, 0.0, 0.0)
    assert res6.metadata["point_B_tuple"] == (0.0, 0.0, 2.0)
    print(
        f"[PASS] Test 6: d(Ox, Delta_2) = {res6.symbolic_result} = {res6.numeric_value:.4f}, "
        f"AB = {res6.metadata['point_A_tuple']} -> {res6.metadata['point_B_tuple']}"
    )

    # --------------------------------------------------------------------------
    # Test 7: Định lý Girard - Tam giác cầu trên Trái Đất (bán kính R=6371)
    # có 3 góc vuông pi/2, pi/2, pi/2. Diện tích kỳ vọng = (1/8)*4*pi*R^2 = (1/2)*pi*R^2.
    # --------------------------------------------------------------------------
    res7 = engine.prove_girard_spherical_area(
        R=6371,
        angle_A=sp.pi / 2,
        angle_B=sp.pi / 2,
        angle_C=sp.pi / 2,
        problem_id="TEST_07_GIRARD_OCTANT",
    )
    expected_area7_sym = sp.Rational(1, 2) * sp.pi * (sp.Integer(6371) ** 2)
    expected_area7_num = 0.5 * math.pi * (6371.0 ** 2)
    assert sp.simplify(res7.symbolic_result - expected_area7_sym) == 0
    assert math.isclose(res7.numeric_value, expected_area7_num, rel_tol=1e-9)
    print(f"[PASS] Test 7: S_Girard = {res7.symbolic_result} ≈ {res7.numeric_value:.2f} km^2")

    # --------------------------------------------------------------------------
    # Test 8: Cực trị tối ưu SAT/AP: Khối nón thể tích lớn nhất nội tiếp mặt cầu
    # bán kính R=9. Chiều cao h = (4/3)*9 = 12, bán kính đáy r = 6*sqrt(2).
    # --------------------------------------------------------------------------
    res8 = engine.prove_inscribed_solid_optimization(
        solid_type="cone",
        R=9,
        problem_id="TEST_08_OPTIMAL_CONE_IN_SPHERE",
    )
    assert math.isclose(res8.metadata["h_opt"], 12.0, rel_tol=1e-9)
    assert math.isclose(res8.metadata["r_opt"], 6.0 * math.sqrt(2.0), rel_tol=1e-9)
    assert sp.simplify(res8.metadata["h_opt_symbolic"] - 12) == 0
    assert sp.simplify(res8.metadata["r_opt_symbolic"] - 6 * sp.sqrt(2)) == 0
    print(
        f"[PASS] Test 8: h_cone = {res8.metadata['h_opt_symbolic']}, "
        f"r_cone = {res8.metadata['r_opt_symbolic']}, V_max = {res8.symbolic_result}"
    )

    print("=" * 78)
    print("ALL 8 MANDATORY UNIT TESTS PASSED 100% SUCCESSFULLY!")
    print("=" * 78)


if __name__ == "__main__":
    run_all_unit_tests()
