@echo off
title CAD Math Studio v2.1
cd /d "%~dp0.."
python cad_math_v2\cad_math_v2.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Co loi xay ra khi khoi chay CAD Math Studio!
    pause
)
