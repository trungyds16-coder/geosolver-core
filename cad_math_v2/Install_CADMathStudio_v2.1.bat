@echo off
title Cai Dat CAD Math Studio v2.1
chcp 65001 >nul
cls
echo ===============================================================================
echo            CÀI ĐẶT ỨNG DỤNG CAD MATH STUDIO v2.1 CHUẨN MICROSOFT
echo ===============================================================================
echo.
echo [1/2] Đang cài đặt Chứng chỉ số vào hệ thống (Trusted Root Certification Authorities)...
powershell -NoProfile -Command "Import-Certificate -FilePath '%~dp0CADMathCert.cer' -CertStoreLocation Cert:\LocalMachine\Root" >nul 2>&1
if %errorlevel% neq 0 (
    powershell -NoProfile -Command "Import-Certificate -FilePath '%~dp0CADMathCert.cer' -CertStoreLocation Cert:\CurrentUser\Root" >nul 2>&1
)

echo [2/2] Đang cài đặt gói ứng dụng MSIX CAD Math Studio v2.1...
powershell -NoProfile -Command "Add-AppxPackage -Path '%~dp0CADMathStudio_2.1.0.0.msix'"
if %errorlevel% equ 0 (
    echo.
    echo ===============================================================================
    echo   CÀI ĐẶT THÀNH CÔNG! BẠN CÓ THỂ MỞ 'CAD Math Studio v2.1' TỪ START MENU.
    echo ===============================================================================
) else (
    echo.
    echo [LƯU Ý]: Nếu máy yêu cầu quyền Admin, vui lòng nhấp chuột phải vào file này và chọn 'Run as administrator'.
    echo Hoặc bạn có thể nhấp đúp trực tiếp vào file CADMathStudio_2.1.0.0.msix để cài đặt.
)
echo.
pause
