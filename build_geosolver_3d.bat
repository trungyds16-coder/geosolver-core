@echo off
title Build and Verify GeoSolver 3D Release
cd /d "%~dp0"

echo ============================================================
echo [1/3] DONG GOI PYINSTALLER GEOSOLVER 3D
echo ============================================================
python -m PyInstaller --noconfirm --distpath dist --workpath build geosolver_3d\GeoSolver3D.spec
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Loi bien dich PyInstaller!
    exit /b %ERRORLEVEL%
)

echo ============================================================
echo [2/3] CHAY KIEM THU SMOKE TEST TRUC TIEP TREN TEP NHI PHAN
echo ============================================================
dist\GeoSolver_3D\GeoSolver3D.exe --smoke-test --output=dist\GeoSolver_3D\smoke_test_result.json
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Smoke test that bai!
    exit /b %ERRORLEVEL%
)

echo ============================================================
echo [3/3] TAO BANG BAM TOAN VEN SHA-256 MANIFEST
echo ============================================================
python scratch\generate_manifest.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Loi tao manifest!
    exit /b %ERRORLEVEL%
)

echo ============================================================
echo HOAN TAT DONG GOI VA KIEM DINH GEOSOLVER 3D THANH CONG!
echo ============================================================
