@echo off
chcp 65001 > nul
title GeoSolver 2D CAD Studio
cd /d "%~dp0"

python geosolver_desktop.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Co loi xay ra khi khoi chay GeoSolver 2D CAD Studio!
    pause
)
