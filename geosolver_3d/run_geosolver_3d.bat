@echo off
title GeoSolver 3D
cd /d "%~dp0\.."
python geosolver_3d\app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Co loi xay ra khi khoi chay GeoSolver 3D!
    pause
)
