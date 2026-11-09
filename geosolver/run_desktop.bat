@echo off
chcp 65001 > nul
title GeoSolver Desktop Launcher
cd /d "%~dp0"

echo Dang khoi dong GeoSolver Desktop...
python geosolver_desktop.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Phat hien loi khi khoi chay GeoSolver!
    pause
)
