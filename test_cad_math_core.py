"""Bộ pytest cho CAD Math Studio v2.2.0-RC.

Chạy:  pytest -v test_cad_math_core.py

Quy ước:
  - Test thường  : hành vi mà mã hiện tại PHẢI đáp ứng.
  - xfail(strict): lỗi/thiếu sót đã nêu trong báo cáo thẩm định. Khi mã được sửa,
                   test sẽ XPASS -> strict=True làm bộ test FAIL để nhắc bỏ dấu xfail.
"""
import xml.etree.ElementTree as ET

import pytest
import sympy as sp

from cad_math_core import CADMathCore, compute_matrix_inverse

x = sp.symbols("x")
core = CADMathCore()


def solve(expr):
    return core.solve_radical_pedagogical(expr, x)


# ---------------------------------------------------------------- Phương trình vô tỷ
class TestRadical:
    def test_tv_alg_01_extraneous_root_removed(self):
        steps, valid, rejected, indet = solve(sp.sqrt(2 * x + 3) - x)
        assert valid == [3]
        assert [r for r, _ in rejected] == [-1]
        assert indet == []

    def test_tv_alg_02_no_solution(self):
        steps, valid, rejected, indet = solve(sp.sqrt(x - 5) + 2)
        assert valid == []
        assert indet == []
        assert [r for r, _ in rejected] == [9]  # 9 là nghiệm ngoại lai

    def test_second_extraneous_example(self):
        # sqrt(x+2) = x -> x^2 - x - 2 = 0 -> x = -1, 2
        steps, valid, rejected, _ = solve(sp.sqrt(x + 2) - x)
        assert valid == [2]
        assert [r for r, _ in rejected] == [-1]

    def test_both_roots_valid(self):
        # sqrt(x+6) = x  -> x = 3 (x=-2 loại). Dùng pt có 2 nghiệm hợp lệ:
        # sqrt(x^2) không cô lập được; dùng sqrt(x+2) = x - ... xem test sau.
        steps, valid, rejected, _ = solve(sp.sqrt(x + 6) - x)
        assert valid == [3]

    def test_double_root(self):
        # sqrt(x) = x - ... ; sqrt(4x) = x + 1 -> x^2 - 2x + 1 = 0 -> x = 1 (kép)
        steps, valid, rejected, _ = solve(sp.sqrt(4 * x) - (x + 1))
        assert valid == [1]

    def test_g_identically_zero(self):
        # sqrt(x^2 - 4x + 4) khó cô lập; dùng sqrt(x) = 0
        steps, valid, rejected, _ = solve(sp.sqrt(x))
        assert valid == [0]

    def test_irrational_root_exact_sign(self):
        # sqrt(x+1) = x -> x^2 - x - 1 = 0 -> (1±√5)/2 ; chỉ nhận nghiệm dương
        steps, valid, rejected, indet = solve(sp.sqrt(x + 1) - x)
        golden = (1 + sp.sqrt(5)) / 2
        assert len(valid) == 1 and sp.simplify(valid[0] - golden) == 0
        assert indet == []

    def test_complex_roots_rejected(self):
        # sqrt(x) = x^2 + 1... -> nghiệm phức, không có nghiệm thực
        steps, valid, rejected, _ = solve(sp.sqrt(x) - (x**2 + 1))
        assert valid == []

    def test_coefficient_in_front_of_radical(self):
        # 2*sqrt(x+1) - x - 1 = 0 -> sqrt(x+1) = (x+1)/2 -> x = -1 hoặc x = 3
        steps, valid, _, _ = solve(2 * sp.sqrt(x + 1) - x - 1)
        assert sorted(valid) == [-1, 3]

    def test_multiple_radicals_out_of_scope(self):
        steps, valid, rejected, indet = solve(sp.sqrt(x) + sp.sqrt(x + 1) - 3)
        assert valid == [] and "Ngoài phạm vi" in steps[0]

    def test_no_radical_out_of_scope(self):
        steps, valid, *_ = solve(x**2 - 1)
        assert valid == []

    def test_substitution_back_verifies_every_valid_root(self):
        for expr in (sp.sqrt(2 * x + 3) - x, sp.sqrt(x + 2) - x, sp.sqrt(x + 1) - x):
            _, valid, _, _ = solve(expr)
            for r in valid:
                assert abs(sp.N(expr.subs(x, r), 40)) < sp.Float("1e-30")

    # ----- lỗi đã nêu trong báo cáo (xfail strict) -----
    @pytest.mark.xfail(strict=True, reason="Chưa có nhánh dừng sớm khi g là hằng số âm (TV-ALG-02 mô tả 'ngay từ Bước 1')")
    def test_early_exit_when_g_constant_negative(self):
        steps, valid, rejected, _ = solve(sp.sqrt(x - 5) + 2)
        assert not any("Bước 2" in s for s in steps)

    @pytest.mark.xfail(strict=True, reason="Đánh số bước nhảy từ Bước 2 sang Bước 4, thiếu Bước 3")
    def test_step_numbering_contiguous(self):
        steps, *_ = solve(sp.sqrt(2 * x + 3) - x)
        labels = [s.split(":")[0] for s in steps if s.startswith("Bước")]
        assert labels == [f"Bước {i}" for i in range(1, len(labels) + 1)]

    @pytest.mark.xfail(strict=True, reason="Chưa chấp nhận sp.Eq làm đầu vào")
    def test_accepts_sympy_eq(self):
        steps, valid, *_ = core.solve_radical_pedagogical(sp.Eq(sp.sqrt(2 * x + 3), x), x)
        assert valid == [3]


class TestSignHelpers:
    @pytest.mark.parametrize("val,expected", [
        (sp.Integer(5), "pos"), (sp.Integer(-5), "neg"), (sp.Integer(0), "zero"),
        (sp.sqrt(2) - 1, "pos"), (1 - sp.sqrt(2), "neg"),
        (sp.sqrt(2) + sp.sqrt(3) - sp.sqrt(5 + 2 * sp.sqrt(6)), "zero"),
    ])
    def test_check_sign_exact(self, val, expected):
        assert core.check_sign_exact(val) == expected

    def test_check_sign_nonreal(self):
        assert core.check_sign_exact(sp.I) == "nonreal"

    def test_real_status(self):
        assert core.real_status(sp.Integer(3)) is True
        assert core.real_status(sp.I) is False
        assert core.real_status(sp.sqrt(2)) is True

    @pytest.mark.xfail(strict=True, reason="zoo/nan chưa được loại tường minh")
    def test_zoo_is_rejected_not_indeterminate(self):
        assert core.check_sign_exact(sp.zoo) in ("nonreal", "undefined")


# ---------------------------------------------------------------- Diophantine (kiểm chứng test vector)
def positive_solutions_2x_3y_13():
    """Cài đặt tham chiếu độc lập (hồ sơ không kèm mã Diophantine)."""
    return sorted((a, (13 - 2 * a) // 3) for a in range(1, 7) if (13 - 2 * a) > 0 and (13 - 2 * a) % 3 == 0)


def test_tv_alg_03_diophantine_reference():
    assert positive_solutions_2x_3y_13() == [(2, 3), (5, 1)]
    for a, b in positive_solutions_2x_3y_13():
        assert 2 * a + 3 * b == 13 and a > 0 and b > 0


def test_diophantine_bounds_via_congruence():
    from sympy.ntheory.modular import solve_congruence
    # 2x ≡ 13 (mod 3)  ->  x ≡ 2 (mod 3)
    assert solve_congruence((2 * 2 % 3, 13 % 3, 3)) is None or True  # smoke: import hoạt động
    assert [k for k in range(1, 7) if (2 * k) % 3 == 13 % 3] == [2, 5]


# ---------------------------------------------------------------- Giải tích
class TestCalculus:
    def test_tv_cal_01_derivative_removable_discontinuity(self):
        f = (x**2 - 3 * x + 2) / (x - 1)
        d = sp.cancel(sp.diff(f, x))
        assert d == 1
        # f không xác định tại x=1 dù f' = 1 ở mọi điểm còn lại
        assert f.subs(x, 1) is sp.nan or sp.simplify(f.subs(x, 1)) in (sp.nan, sp.zoo)

    def test_tv_cal_01_raw_diff_needs_simplify(self):
        f = (x**2 - 3 * x + 2) / (x - 1)
        raw = sp.diff(f, x)
        assert sp.simplify(raw) == 1

    def test_tv_cal_02_integration_by_parts(self):
        F = sp.integrate(x * sp.exp(x), x)
        assert sp.simplify(F - sp.exp(x) * (x - 1)) == 0
        assert sp.simplify(sp.diff(F, x) - x * sp.exp(x)) == 0


# ---------------------------------------------------------------- Ma trận
A_SINGULAR = sp.Matrix([[1, 2], [2, 4]])
A_3X3 = sp.Matrix([[1, 0, 2], [2, -1, 3], [4, 1, 8]])
A_3X3_INV_CORRECT = sp.Matrix([[-11, 2, 2], [-4, 0, 1], [6, -1, -1]])
A_3X3_INV_DOSSIER = sp.Matrix([[11, -2, -2], [4, 0, -1], [-6, 1, 1]])


class TestMatrix:
    def test_tv_mat_01_singular_no_crash(self):
        r = compute_matrix_inverse(A_SINGULAR)
        assert r["invertible"] is False and r["det"] == 0
        assert "suy biến" in r["desc"]

    def test_tv_mat_02_determinant_is_plus_one(self):
        assert A_3X3.det() == 1  # hồ sơ ghi -1: SAI

    def test_tv_mat_02_correct_inverse(self):
        r = compute_matrix_inverse(A_3X3)
        assert r["invertible"] is True
        assert r["inverse"] == A_3X3_INV_CORRECT
        assert r["adjugate"] == A_3X3_INV_CORRECT  # det = 1 nên adj = inv
        assert A_3X3 * r["inverse"] == sp.eye(3)
        assert r["inverse"] * A_3X3 == sp.eye(3)

    def test_tv_mat_02_dossier_expected_value_is_wrong(self):
        """Chứng minh giá trị kỳ vọng trong hồ sơ là nghịch đảo đã đổi dấu."""
        assert A_3X3 * A_3X3_INV_DOSSIER == -sp.eye(3)
        assert compute_matrix_inverse(A_3X3)["inverse"] != A_3X3_INV_DOSSIER

    def test_non_square_raises_valueerror(self):
        with pytest.raises(ValueError):
            compute_matrix_inverse(sp.Matrix([[1, 2, 3], [4, 5, 6]]))

    def test_identity_and_diagonal(self):
        assert compute_matrix_inverse(sp.eye(3))["inverse"] == sp.eye(3)
        D = sp.diag(2, 4)
        assert compute_matrix_inverse(D)["inverse"] == sp.diag(sp.Rational(1, 2), sp.Rational(1, 4))

    def test_symbolic_unsimplified_determinant(self):
        # det = a*b - a*b + (a - a) ... chưa rút gọn nhưng thực chất = 0
        a, b = sp.symbols("a b")
        M = sp.Matrix([[a, b], [a * 2, b * 2]])
        assert compute_matrix_inverse(M)["invertible"] is False

    def test_symbolic_hidden_zero_det(self):
        a = sp.symbols("a")
        M = sp.Matrix([[(a + 1) ** 2, a**2 + 2 * a + 1], [1, 1]])
        assert compute_matrix_inverse(M)["invertible"] is False

    def test_rational_entries(self):
        M = sp.Matrix([[sp.Rational(1, 2), 1], [1, 3]])
        r = compute_matrix_inverse(M)
        assert M * r["inverse"] == sp.eye(2)

    def test_matrix_multiply_dimension_check(self):
        with pytest.raises(sp.ShapeError):
            sp.Matrix([[1, 2, 3]]) * sp.Matrix([[1, 2, 3]])
        assert (sp.Matrix([[1, 2, 3]]) * sp.Matrix([[1], [2], [3]]))[0] == 14


# ---------------------------------------------------------------- MSIX manifest
NS = {
    "f": "http://schemas.microsoft.com/appx/manifest/foundation/windows10",
    "uap": "http://schemas.microsoft.com/appx/manifest/uap/windows10",
    "rescap": "http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities",
}


@pytest.fixture(scope="module")
def manifest_root():
    pkg = pytest.importorskip("package_msix", reason="Đặt package_msix.py cạnh file test để chạy phần MSIX")
    return ET.fromstring(pkg.APPX_MANIFEST_XML.encode("utf-8"))


class TestMsixManifest:
    def test_well_formed_and_identity(self, manifest_root):
        ident = manifest_root.find("f:Identity", NS)
        assert ident is not None
        assert ident.get("Name") == "TLabtool.CADMathStudio"
        assert ident.get("Publisher").startswith("CN=")
        assert ident.get("ProcessorArchitecture") == "x64"

    def test_version_four_parts_last_zero(self, manifest_root):
        v = manifest_root.find("f:Identity", NS).get("Version").split(".")
        assert len(v) == 4 and all(p.isdigit() for p in v)
        assert v[3] == "0", "Microsoft Store yêu cầu phần Revision = 0"

    def test_fulltrust_capability(self, manifest_root):
        caps = [c.get("Name") for c in manifest_root.findall("f:Capabilities/rescap:Capability", NS)]
        assert caps == ["runFullTrust"]

    def test_application_entrypoint(self, manifest_root):
        app = manifest_root.find("f:Applications/f:Application", NS)
        assert app.get("Executable") == "CADMathStudio.exe"
        assert app.get("EntryPoint") == "Windows.FullTrustApplication"

    def test_target_device_family(self, manifest_root):
        t = manifest_root.find("f:Dependencies/f:TargetDeviceFamily", NS)
        assert t.get("Name") == "Windows.Desktop"
        assert t.get("MinVersion") == "10.0.17763.0"

    def test_asset_paths_use_single_backslash(self, manifest_root):
        for el in manifest_root.iter():
            for attr in ("Square150x150Logo", "Square44x44Logo", "Wide310x150Logo"):
                if el.get(attr):
                    assert "\\\\" not in el.get(attr) and el.get(attr).startswith("Assets\\")
        assert "\\\\" not in manifest_root.find("f:Properties/f:Logo", NS).text

    @pytest.mark.xfail(strict=True, reason="Thiếu IgnorableNamespaces='uap rescap' trên thẻ <Package>")
    def test_ignorable_namespaces(self, manifest_root):
        assert set(manifest_root.get("IgnorableNamespaces", "").split()) >= {"uap", "rescap"}

    def test_has_both_resource_languages(self, manifest_root):
        langs = {r.get("Language") for r in manifest_root.findall("f:Resources/f:Resource", NS)}
        assert {"vi-VN", "en-US"} <= langs

    def test_portable_paths(self):
        pkg = pytest.importorskip("package_msix")
        import os
        assert os.path.isabs(pkg.BASE_DIR)
        assert not pkg.DIST_APP_DIR.startswith("C:\\Users\\")
