@echo off
chcp 65001 >nul
title AI CAD LAB - DeepSeek-R1 1.5B Text-to-CAD Demo
cd /d "%~dp0"

echo ========================================================
echo  KHOI DONG PHONG THI NGHIEM TEXT-TO-CAD ^& AI SINH DE THI
echo  Moi truong: Python Tkinter + Ollama Local (deepseek-r1:1.5b)
echo  Thu muc goc: %CD%
echo ========================================================
echo.

python -X utf8 stem_shared_core\tools\demo_ai_canvas_studio.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [LOI] Chuong trinh gap loi hoac dung dot ngot voi ma loi: %ERRORLEVEL%
    echo Vui long chup lai man hinh nay de duoc ho tro.
)

pause
