@echo off
title Cai Dat CAD Math Studio v2.3
chcp 65001 >nul
cls

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ===============================================================================
    echo [YÊU CẦU QUYỀN ADMINISTRATOR]: Kịch bản cài đặt yêu cầu quyền Administrator!
    echo Vui lòng nhấp chuột phải vào file Install_CADMathStudio_v2.3.bat và chọn:
    echo                         'Run as administrator'
    echo ===============================================================================
    echo.
    pause
    exit /b 1
)

echo ===============================================================================
echo            CÀI ĐẶT ỨNG DỤNG CAD MATH STUDIO v2.3 CHUẨN MICROSOFT
echo ===============================================================================
echo.
echo [1/2] Đang cài đặt Chứng chỉ số vào Trusted People (Sideloading Store Trust)...
powershell -NoProfile -Command "Import-Certificate -FilePath '%~dp0CADMathCert.cer' -CertStoreLocation Cert:\LocalMachine\TrustedPeople"

echo.
echo [2/2] Đang cài đặt gói ứng dụng MSIX CAD Math Studio v2.3...
powershell -NoProfile -Command "Add-AppxPackage -Path '%~dp0CADMathStudio_2.3.0.0.msix'"
if %errorlevel% equ 0 (
    echo.
    echo ===============================================================================
    echo   CÀI ĐẶT THÀNH CÔNG! BẠN CÓ THỂ MỞ 'CAD Math Studio' TỪ START MENU.
    echo ===============================================================================
) else (
    echo.
    echo [LỖI]: Không thể cài đặt gói MSIX. Vui lòng kiểm tra lại thiết lập Windows App Sideloading.
)
echo.
pause
