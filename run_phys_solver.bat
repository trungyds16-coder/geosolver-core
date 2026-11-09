@echo off
title STEM PhysLab Modular CAD Studio v2.0
cd /d "%~dp0"
python phys_solver\app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Co loi xay ra khi khoi chay PhysLab Studio!
    pause
)
