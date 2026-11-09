# Báo Cáo Giải Trình Kỹ Thuật & Thực Nghiệm Đóng Gói GeoSolver 2D v3.1 (Lần 7)

**Trạng thái đề xuất:** **Release Candidate 2 (RC2) — Store-Ready (Đã kiểm chứng trên bản đóng gói EXE thật)**  
**Môi trường thử nghiệm:** Windows 11 Enterprise x64 (Build 26300) | CPython 3.14.5 AMD64 | PyInstaller 6.22.3  
**Bộ kiểm thử tự động:** 20/20 bài kiểm thử vượt qua (20 PASS) trong 0.423s | Smoke Test trên gói `GeoSolver.exe` độc lập đạt ExitCode 0  

---

## 1. Tiếp Thu và Xử Lý Các Điểm Phản Biện Thẩm Định Lần 6

| Điểm phản biện của Thẩm định viên | Đánh giá kỹ thuật | Hành động khắc phục thực tế |
|---|---|---|
| **1. Khói test đóng gói trước đó chạy từ mã nguồn dev** | **Chính xác hoàn toàn.** Trước đó lệnh gọi qua `python geosolver/geosolver_desktop.py --smoke-test` chỉ chạy nhánh `dev_tree`. | Đã chạy lệnh đóng gói PyInstaller thực tế, sau đó chạy `Start-Process -FilePath "dist\GeoSolver\GeoSolver.exe" -ArgumentList "--smoke-test" -Wait -PassThru`. File EXE tạo ra `smoke_test_result.json` với `frozen: true`, ExitCode = 0. |
| **2. Sai đường dẫn trong `.spec` (`dirname(SPECPATH)`)** | **Chính xác hoàn toàn.** Trong PyInstaller, `SPECPATH` đã là thư mục chứa `.spec` (`geosolver/`). `dirname(SPECPATH)` trỏ nhầm ra thư mục gốc. | Sửa thành `BASE = os.path.abspath(SPECPATH)` và `ROOT = os.path.dirname(BASE)`. Khôi phục `pyz = PYZ(a.pure)` chuẩn PyInstaller 6.x. Lọc bỏ `.tests` của `sympy` và `mpmath`. Loại bỏ `unittest` khỏi `excludes` để tránh lỗi nạp module. |
| **3. Cờ `exact` chỉ dựa vào heuristic số thập phân** | **Chính xác.** Điểm vẽ chuột tự do ở mức zoom pixel/40 có thể tình cờ rơi vào số nguyên/thập phân sạch. | Bổ sung tham số `points_exact: bool | None` và nhận diện metadata `source` của từng điểm (`"typed"`, `"grid_snap"` vs `"free"`). Nếu điểm có nguồn gốc `"free"` hoặc `points_exact=False`, cờ `exact` bắt buộc bằng `False` bất kể tọa độ rơi vào lưới rời rạc. |
| **4. `logging.warning` trong GUI app `console=False` bị mất** | **Chính xác.** | Bổ sung hàm `_log_warning` tự động ghi log vào file `%LOCALAPPDATA%\AIMathHub\logs\geosolver.log`. Trong `save()`, bổ sung `f.flush()` và `os.fsync(f.fileno())` trước khi gọi `os.replace`. |
| **5. Sửa lỗi Windows File Lock trong `hf_downloader.py`** | **Phát hiện quan trọng khi bổ sung test 20.** | Trong `hf_downloader._verify()`, trước đây lệnh `self.part_path.unlink()` nằm trong khối `with open(...)` gây lỗi `PermissionError: [WinError 32]`. Đã sửa để đóng file handle trước khi xóa file `.part`. |

---

## 2. Mã Nguồn Trọng Tâm Đã Sửa Đổi

### 2.1. File Cấu Hình Đóng Gói Hoàn Chỉnh (`geosolver/GeoSolver.spec`)
```python
# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

# SPECPATH là thư mục chứa file .spec (d:\AI DATA\STEM_APP\geosolver)
BASE = os.path.abspath(SPECPATH)
ROOT = os.path.dirname(BASE)

block_cipher = None

# Lọc bỏ các submodule test của sympy/mpmath để tối ưu kích thước gói
hidden_imports = (
    collect_submodules('sympy', filter=lambda n: '.tests' not in n)
    + collect_submodules('mpmath', filter=lambda n: '.tests' not in n)
    + [
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'stem_shared_core',
        'stem_shared_core.ai_model_hub',
        'stem_shared_core.hf_downloader',
        'stem_shared_core.ai_config_dialog',
        'stem_shared_core.i18n',
        'stem_handbook_dialog',
    ]
)

a = Analysis(
    [os.path.join(BASE, 'geosolver_desktop.py')],
    pathex=[BASE, ROOT],
    binaries=[],
    datas=[
        (os.path.join(BASE, 'assets'), 'assets'),
        (os.path.join(ROOT, 'CAM_NANG_SU_DUNG_STEM_CAD_MATH.md'), '.'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter.test', 'test'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GeoSolver',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=os.path.join(BASE, 'file_version_info.txt'),
    icon=[os.path.join(BASE, 'assets', 'app.ico')],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='GeoSolver',
)
```

### 2.2. Phân Loại Hình Học Với Cờ Nguồn Gốc Điểm (`classify_triangle`)
```python
def classify_triangle(pA, pB, pC, lang: str = "vi", points_exact: bool | None = None) -> dict:
    is_en = (lang == "en")
    
    def get_xy_name_exact(p, default_name):
        if isinstance(p, dict):
            ex = None
            if "exact" in p and p["exact"] is not None:
                ex = bool(p["exact"])
            elif "source" in p:
                ex = p["source"] in ("typed", "grid_snap", "snapped", "formula", "exact")
            return float(p.get("x", 0.0)), float(p.get("y", 0.0)), str(p.get("name") or default_name), ex
        else:
            return float(p[0]), float(p[1]), default_name, None

    xA, yA, nA, exA = get_xy_name_exact(pA, "A")
    xB, yB, nB, exB = get_xy_name_exact(pB, "B")
    xC, yC, nC, exC = get_xy_name_exact(pC, "C")

    # Xác định nguồn gốc điểm do người dùng/giao diện cung cấp
    pt_flags = [exA, exB, exC]
    if points_exact is not None:
        user_declared_exact = bool(points_exact)
    elif all(f is not None for f in pt_flags):
        user_declared_exact = all(pt_flags)
    elif any(f is not None for f in pt_flags):
        user_declared_exact = all(f is True for f in pt_flags if f is not None)
    else:
        user_declared_exact = None

    u_AB = (xB - xA, yB - yA)
    u_AC = (xC - xA, yC - yA)
    u_BC = (xC - xB, yC - yB)

    c_sq = u_AB[0]**2 + u_AB[1]**2
    b_sq = u_AC[0]**2 + u_AC[1]**2
    a_sq = u_BC[0]**2 + u_BC[1]**2

    c_len = math.sqrt(c_sq)
    b_len = math.sqrt(b_sq)
    a_len = math.sqrt(a_sq)

    if c_len < 1e-4 or b_len < 1e-4 or a_len < 1e-4:
        msg = "Coincident points; not a valid triangle." if is_en else "Có điểm trùng nhau; không tạo thành tam giác."
        return {
            "is_triangle": False, "type": "coincident",
            "message": msg, "sides": {"AB": c_len, "AC": b_len, "BC": a_len}
        }

    cross = u_AB[0] * u_AC[1] - u_AB[1] * u_AC[0]
    scaled_coords, scale_factor = as_scaled_ints([xA, yA, xB, yB, xC, yC], max_k=4)
    is_discrete = (scaled_coords is not None)

    # ... [Phần tính toán cạnh, góc và độ lệch] ...

    all_int = all(abs(v - round(v)) < 1e-4 for v in (xA, yA, xB, yB, xC, yC))
    # QUY TẮC CỜ EXACT:
    # Nếu user_declared_exact là False (vẽ chuột tự do), exact bắt buộc là False dù tọa độ nguyên
    exact_math = False if user_declared_exact is False else (is_discrete if user_declared_exact is None else (is_discrete and user_declared_exact))

    return {
        "is_triangle": True,
        "type": tri_type,
        "vertex": vertex,
        "all_int": all_int,
        "is_discrete": is_discrete,
        "exact": exact_math,
        "origin_exact": user_declared_exact,
        "deviations": deviations,
        "scale_factor": scale_factor,
        "is_equilateral": is_equilateral,
        "is_isosceles": (tri_type in ("isosceles", "right_isosceles")),
        "is_right": (tri_type in ("right", "right_isosceles")),
        "sides": {"AB": c_len, "AC": b_len, "BC": a_len},
        "side_labels": {"AB": str_AB, "AC": str_AC, "BC": str_BC},
        "description": description
    }
```

### 2.3. Khắc Phục Log GUI và Ghi Đĩa Nguyên Tử Trong `GeminiKeyStore`
```python
def _log_warning(msg: str, *args):
    """Ghi log cảnh báo an toàn ra cả logging chuẩn và file log cục bộ trong %LOCALAPPDATA%."""
    import logging
    try:
        base = os.environ.get("LOCALAPPDATA")
        root = Path(base) if base else Path.home() / ".local" / "share"
        log_dir = root / "AIMathHub" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "geosolver.log"
        if not logging.getLogger().handlers:
            logging.basicConfig(filename=str(log_file), level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    except Exception:
        pass
    logging.warning(msg, *args)

class GeminiKeyStore:
    def read(self) -> str | None:
        if self.key_file.is_file():
            try:
                content = self.key_file.read_text(encoding="utf-8").strip()
                if content.startswith("DPAPI:"):
                    raw_b64 = content[6:]
                    encrypted_bytes = base64.b64decode(raw_b64)
                    decrypted = _dpapi_decrypt(encrypted_bytes).decode("utf-8").strip()
                    return decrypted or None
                elif content:
                    if os.name == "nt":
                        try: self.save(content)
                        except Exception: pass
                    return content
            except Exception as e:
                _log_warning("DPAPI decryption failed (%s); falling back to environment variable", e)
        env_value = os.environ.get("GEMINI_API_KEY", "").strip()
        return env_value or None

    def save(self, api_key: str) -> None:
        cleaned = api_key.strip()
        if not cleaned:
            raise ValueError("Khóa API rỗng, không thể lưu.")
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            enc = _dpapi_encrypt(cleaned.encode("utf-8"))
            payload = "DPAPI:" + base64.b64encode(enc).decode("ascii")
        else:
            payload = cleaned

        tmp_fd, tmp_path = tempfile.mkstemp(dir=self.key_file.parent, prefix="gemini_key_", suffix=".tmp")
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(payload)
                f.flush()
                os.fsync(f.fileno())  # Flush triệt để xuống đĩa vật lý trước khi rename
            if os.name != "nt":
                try: os.chmod(tmp_path, 0o600)
                except Exception: pass
            os.replace(tmp_path, self.key_file)
            if os.name != "nt":
                try: os.chmod(self.key_file, 0o600)
                except Exception: pass
        finally:
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass
```

---

## 3. Nhật Ký Thực Nghiệm Nguyên Bản (Verbatim Logs)

### 3.1. Trích Nhật Ký Build PyInstaller Thật (Task 3120)
```text
259 INFO: PyInstaller: 6.22.3, contrib hooks: 2026.9
259 INFO: Python: 3.14.5
300 INFO: Platform: Windows-11-10.0.26300-SP0
301 INFO: Python environment: C:\Users\DELL\AppData\Local\Programs\Python\Python314
...
100481 INFO: Building PYZ (ZlibArchive) D:\AI DATA\STEM_APP\build\GeoSolver\PYZ-00.pyz
102668 INFO: Building PYZ (ZlibArchive) D:\AI DATA\STEM_APP\build\GeoSolver\PYZ-00.pyz completed successfully.
102770 INFO: Building PKG (CArchive) GeoSolver.pkg completed successfully.
104125 INFO: Copying bootloader EXE to D:\AI DATA\STEM_APP\build\GeoSolver\GeoSolver.exe
104343 INFO: Copying icon to EXE
104417 INFO: Copying version information to EXE
104676 INFO: Appending PKG archive to EXE
105765 INFO: Building EXE from EXE-00.toc completed successfully.
106258 INFO: Building COLLECT COLLECT-00.toc
108519 INFO: Building COLLECT COLLECT-00.toc completed successfully.
108585 INFO: Build complete! The results are available in: D:\AI DATA\STEM_APP\dist
```

### 3.2. Chạy Smoke Test Trên `GeoSolver.exe` Bằng PowerShell
```powershell
PS D:\AI DATA\STEM_APP> $p = Start-Process -FilePath "dist\GeoSolver\GeoSolver.exe" -ArgumentList "--smoke-test" -Wait -PassThru; Write-Host "ExitCode: $($p.ExitCode)"
ExitCode: 0
```

### 3.3. Nội Dung File Kết Quả `dist\GeoSolver\smoke_test_result.json` Do EXE Tự Sinh
```json
{
  "frozen": true,
  "python_version": "3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)]",
  "executable": "D:\\AI DATA\\STEM_APP\\dist\\GeoSolver\\GeoSolver.exe",
  "checks": {
    "geometry": true,
    "dpapi": true,
    "sympy": true,
    "tkinter_runtime": true,
    "critical_modules": true,
    "assets": true
  },
  "status": "PASS",
  "exit_code": 0
}
```

### 3.4. Nhật Ký 20 Bài Kiểm Thử Tự Động Toàn Diện (`tests/test_run.log`)
```text
test_01_true_positive_equilateral_triangle (tests.test_geometry_invariants.TestGeometryInvariants.test_01_true_positive_equilateral_triangle)
Ca dương tính: Tam giác đều thực sự với tọa độ vô tỉ (gọi trực tiếp classify_triangle) ... ok
test_02_regression_original_bug_isosceles_not_equilateral (tests.test_geometry_invariants.TestGeometryInvariants.test_02_regression_original_bug_isosceles_not_equilateral)
Hồi quy lỗi gốc: A(0, 5), B(-3, 0), C(3, 0) phải nhận diện là tam giác cân tại A, TUYỆT ĐỐI KHÔNG ĐƯỢC BÁO ĐỀU ... ok
test_03_scale_invariance_property (tests.test_geometry_invariants.TestGeometryInvariants.test_03_scale_invariance_property)
Thuộc tính bất biến tỷ lệ theo thang 10^-k (k=0..3) trên tọa độ rời rạc ... ok
test_04_typed_decimals_rejection_claude_cases (tests.test_geometry_invariants.TestGeometryInvariants.test_04_typed_decimals_rejection_claude_cases)
Ca số thập phân gõ tay của Claude (5, 8.7) và (0.04, 3) không bị nhận nhầm ... ok
test_05_negative_equilateral_pure_float_coordinates (tests.test_geometry_invariants.TestGeometryInvariants.test_05_negative_equilateral_pure_float_coordinates)
Ca âm tính độc lập: Dung sai 0.6% trên tọa độ thực tự do loại trừ tam giác lệch 1.8% ... ok
test_06_collinear_and_coincident_points (tests.test_geometry_invariants.TestGeometryInvariants.test_06_collinear_and_coincident_points)
Ca biên: 3 điểm thẳng hàng và điểm trùng nhau không tạo thành tam giác ... ok
test_07_right_and_right_isosceles_triangles (tests.test_geometry_invariants.TestGeometryInvariants.test_07_right_and_right_isosceles_triangles)
Ca tam giác vuông và vuông cân trên lưới rời rạc ... ok
test_08_ellipse_edge_cases_and_rotational_invariance (tests.test_geometry_invariants.TestGeometryInvariants.test_08_ellipse_edge_cases_and_rotational_invariance)
Hình elip toàn diện: chuẩn, F1==F2, suy biến b=0, tiêu điểm nghiêng 53.13° và đổi F1/F2 ... ok
test_09_ramanujan_ii_exact_accuracy_table (tests.test_geometry_invariants.TestGeometryInvariants.test_09_ramanujan_ii_exact_accuracy_table)
Chu vi Ramanujan II so với tích phân số học quy tắc trung điểm 100.000 bước ... ok
test_10_wcag_21_aa_itemized_real_contrast (tests.test_geometry_invariants.TestGeometryInvariants.test_10_wcag_21_aa_itemized_real_contrast)
Đo tương phản 20 cặp màu thực tế trên THEMES_GEOSOLVER theo chuẩn W3C WCAG 2.1 AA ... ok
test_11_clean_print_mode_and_handbook_dialog (tests.test_geometry_invariants.TestGeometryInvariants.test_11_clean_print_mode_and_handbook_dialog)
Kiểm tra Clean Print Mode toggle mặc định tắt và tệp cẩm nang F1 ... ok
test_12_dpapi_keystore_and_downloader_sha256 (tests.test_geometry_invariants.TestGeometryInvariants.test_12_dpapi_keystore_and_downloader_sha256)
Kiểm tra bảo mật DPAPI KeyStore (chống Use-After-Free) và hf_downloader SHA-256 ... ok
test_13_dpapi_fail_soft_on_corrupt_or_foreign_key (tests.test_geometry_invariants.TestGeometryInvariants.test_13_dpapi_fail_soft_on_corrupt_or_foreign_key)
Kiểm tra nguyên tắc fail-soft của GeminiKeyStore: không sập app khi file hỏng hoặc chuyển máy ... ok
test_14_exact_right_triangle_float_coordinates_no_spurious_annotation (tests.test_geometry_invariants.TestGeometryInvariants.test_14_exact_right_triangle_float_coordinates_no_spurious_annotation)
Tam giác vuông thực sự có tọa độ vô tỉ (0,0), (√2,0), (0,√3): không được chú thích '(gần vuông, góc 0.0°)' ... ok
test_15_float_near_right_and_near_right_isosceles_annotation (tests.test_geometry_invariants.TestGeometryInvariants.test_15_float_near_right_and_near_right_isosceles_annotation)
Ca số thực tự do gần vuông và gần vuông cân: kiểm tra chú thích độ lệch và deviations dict ... ok
test_16_dpapi_stress_round_trip_stability (tests.test_geometry_invariants.TestGeometryInvariants.test_16_dpapi_stress_round_trip_stability)
Kiểm tra áp lực 100 lần mã hóa/giải mã DPAPI với payload ngẫu nhiên 1KB để loại trừ rò rỉ vùng nhớ ctypes ... ok
test_17_freehand_point_origin_flag_rejection (tests.test_geometry_invariants.TestGeometryInvariants.test_17_freehand_point_origin_flag_rejection)
Kiểm tra cờ nguồn gốc exact/source: vẽ chuột tự do dù toạ độ nguyên vẫn có exact=False ... ok
test_18_format_radical_len_direct_unit_tests (tests.test_geometry_invariants.TestGeometryInvariants.test_18_format_radical_len_direct_unit_tests)
Kiểm tra trực tiếp format_radical_len với các mẫu căn thức và phân số phổ biến ... ok
test_19_ellipse_near_degenerate_a_approx_c (tests.test_geometry_invariants.TestGeometryInvariants.test_19_ellipse_near_degenerate_a_approx_c)
Kiểm tra elip gần suy biến khi a tiệm cận c (b -> 0) không bị lỗi chia 0 hoặc căn số âm ... ok
test_20_hf_downloader_error_paths_comprehensive (tests.test_geometry_invariants.TestGeometryInvariants.test_20_hf_downloader_error_paths_comprehensive)
Kiểm tra các kịch bản lỗi của hf_downloader: sai magic GGUF, lệch kích thước, thiếu SHA-256 ... ok

----------------------------------------------------------------------
Ran 20 tests in 0.423s

OK
```

---

## 4. Bảng Tra Mã Băm SHA-256 Đối Chiếu Toàn Diện

```text
Algorithm Hash                                                             Path
--------- ----                                                             ----
SHA256    2A381533415FE230E08947B602CC7768236898C5051A7E27467D6BB0451B8179  geosolver/geosolver_desktop.py
SHA256    52D61BD1F54CDD7CE6AE0BF96B4CB0302B719BC5CAF2359CE572C60B801A52F8  geosolver/GeoSolver.spec
SHA256    88931E04AAB589A0160EF8BC52D851FACF77A467F124A5AED90FFC2B0A392D34  stem_shared_core/ai_local_manager.py
SHA256    090EFD6F7A64BAE3FBAA3FB2BCE21C6B7E4F9C8F5F7E2CD478CC12449366E481  stem_shared_core/hf_downloader.py
SHA256    5677EF7D66AD9503B42E0AB1473C2C82C296B17E5BCE6AB05DC9CE67A7F40399  tests/test_geometry_invariants.py
SHA256    41B5E5DD3A08D219ADBBE44FA03B80B406A8420F501BCB732483A10AE415334A  dist/GeoSolver/GeoSolver.exe
SHA256    145B8A6BF7E78EEB5CCB47763430353EE5A39186C9FF5B43C0F6072127F3124E  dist/GeoSolver/smoke_test_result.json
```

---

## 5. Kết Luận & Đề Xuất Trạng Thái

- Toàn bộ bằng chứng xây dựng bản đóng gói và chạy thực tế trên EXE nhị phân độc lập đã được thu thập đầy đủ.
- Trạng thái hiện tại của dự án: **Release Candidate 2 (RC2) — Store Ready**.
- Bước tiếp theo khi tiến hành nộp hồ sơ Store: Tạo gói `.msix` thông qua MSIX Packaging Tool và nộp lên Microsoft Partner Center cùng tài liệu khai báo [STORE_METADATA_AND_PRIVACY.md](file:///d:/AI%20DATA/STEM_APP/docs/STORE_METADATA_AND_PRIVACY.md).
