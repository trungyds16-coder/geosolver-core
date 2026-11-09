"""
================================================================================
MSIX PACKAGING & MICROSOFT SIGNING AUTOMATION - CAD MATH STUDIO v2.2.0-RC5
================================================================================
"""

import os
import sys
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_APP_DIR = os.path.join(BASE_DIR, "dist", "CADMathStudio")
PACKAGE_DIR = os.path.join(BASE_DIR, "msix_package")
ASSETS_DIR = os.path.join(PACKAGE_DIR, "Assets")
MSIX_OUTPUT = os.path.join(BASE_DIR, "CADMathStudio_2.2.0.0.msix")

SDK_DIR = os.path.join(BASE_DIR, "tools")
MAKEAPPX = os.path.join(SDK_DIR, "makeappx.exe")
SIGNTOOL = os.path.join(SDK_DIR, "signtool.exe")

CERT_SUBJECT = "CN=CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE"
PFX_PATH = os.path.join(BASE_DIR, "CADMathCert.pfx")
CER_PATH = os.path.join(BASE_DIR, "CADMathCert.cer")


def get_cert_password():
    """
    Lấy mật khẩu chứng chỉ độc quyền từ biến môi trường CADMATH_CERT_PASS.
    B1: Tuyệt đối không dùng giá trị mặc định hardcoded trong mã nguồn.
    """
    pwd = os.environ.get("CADMATH_CERT_PASS")
    if not pwd:
        raise RuntimeError(
            "Biến môi trường 'CADMATH_CERT_PASS' chưa được thiết lập! "
            "Để đảm bảo an toàn bí mật ký số, vui lòng set CADMATH_CERT_PASS trước khi chạy đóng gói."
        )
    return pwd


# Raw string template chuẩn XML Microsoft AppxManifest (Hỗ trợ Windows 10/11 24H2)
APPX_MANIFEST_XML = r"""<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
         IgnorableNamespaces="uap rescap">
  <Identity Name="TLabtool.CADMathStudio"
            Publisher="CN=CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE"
            Version="2.2.0.0"
            ProcessorArchitecture="x64" />
  <Properties>
    <DisplayName>CAD Math Studio</DisplayName>
    <PublisherDisplayName>TLabtool</PublisherDisplayName>
    <Logo>Assets\StoreLogo.png</Logo>
    <Description>CAD Math Studio v2.2 - CAS Algebra, Calculus, Statistics and Oxy Function Graphing.</Description>
  </Properties>
  <Resources>
    <Resource Language="vi-VN" />
    <Resource Language="en-US" />
  </Resources>
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.26100.0" />
  </Dependencies>
  <Capabilities>
    <rescap:Capability Name="runFullTrust" />
  </Capabilities>
  <Applications>
    <Application Id="App"
                 Executable="CADMathStudio.exe"
                 EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName="CAD Math Studio"
                          Description="CAD Math Studio Desktop Application"
                          BackgroundColor="transparent"
                          Square150x150Logo="Assets\Square150x150Logo.png"
                          Square44x44Logo="Assets\Square44x44Logo.png">
        <uap:DefaultTile Wide310x150Logo="Assets\Wide310x150Logo.png" />
        <uap:SplashScreen Image="Assets\SplashScreen.png" />
      </uap:VisualElements>
    </Application>
  </Applications>
</Package>
"""

REQUIRED_ASSETS = {
    "Square150x150Logo.png": (150, 150),
    "Square44x44Logo.png": (44, 44),
    "StoreLogo.png": (50, 50),
    "Wide310x150Logo.png": (310, 150),
    "SplashScreen.png": (620, 300),
}


def create_icon(path, size, text="CAD"):
    img = Image.new("RGBA", size, color=(15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    w, h = size
    margin = int(min(w, h) * 0.08)
    draw.rounded_rectangle([margin, margin, w - margin, h - margin], radius=int(min(w, h) * 0.16), fill=(9, 105, 218, 255))
    try:
        font = ImageFont.truetype("arial.ttf", int(h * 0.42))
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((w - tw) / 2, (h - th) / 2 - bbox[1]), text, fill=(255, 255, 255, 255), font=font)
    img.save(path, "PNG")


def verify_assets_integrity(assets_dir):
    for filename, expected_size in REQUIRED_ASSETS.items():
        file_path = os.path.join(assets_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Thiếu asset bắt buộc: {file_path}")
        with Image.open(file_path) as im:
            if im.size != expected_size:
                raise ValueError(f"Kích thước {filename} không đúng: thực tế {im.size}, yêu cầu {expected_size}")
    return True


def prepare_package_files():
    if not os.path.exists(DIST_APP_DIR):
        raise FileNotFoundError(f"Thư mục ứng dụng đã biên dịch không tồn tại: {DIST_APP_DIR}. Hãy chạy PyInstaller trước.")

    if os.path.exists(PACKAGE_DIR):
        shutil.rmtree(PACKAGE_DIR)

    os.makedirs(PACKAGE_DIR, exist_ok=True)
    for item in os.listdir(DIST_APP_DIR):
        s = os.path.join(DIST_APP_DIR, item)
        d = os.path.join(PACKAGE_DIR, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    license_src = os.path.join(BASE_DIR, "LICENSE.txt")
    if os.path.exists(license_src):
        shutil.copy2(license_src, os.path.join(PACKAGE_DIR, "LICENSE.txt"))

    os.makedirs(ASSETS_DIR, exist_ok=True)
    create_icon(os.path.join(ASSETS_DIR, "Square150x150Logo.png"), (150, 150), "CAD")
    create_icon(os.path.join(ASSETS_DIR, "Square44x44Logo.png"), (44, 44), "C")
    create_icon(os.path.join(ASSETS_DIR, "StoreLogo.png"), (50, 50), "CAD")
    create_icon(os.path.join(ASSETS_DIR, "Wide310x150Logo.png"), (310, 150), "CAD MATH")
    create_icon(os.path.join(ASSETS_DIR, "SplashScreen.png"), (620, 300), "CAD MATH STUDIO")

    verify_assets_integrity(ASSETS_DIR)

    manifest_path = os.path.join(PACKAGE_DIR, "AppxManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(APPX_MANIFEST_XML.strip())


def create_certificate():
    # B1: Đọc và xác thực biến môi trường tồn tại, không nội suy mật khẩu vào chuỗi PowerShell
    get_cert_password()
    ps_cmd = f"""
    $cert = New-SelfSignedCertificate -Type Custom -Subject "{CERT_SUBJECT}" `
        -KeyUsage DigitalSignature -KeySpec Signature `
        -KeyAlgorithm RSA -KeyLength 2048 `
        -HashAlgorithm SHA256 `
        -TextExtension @("2.5.29.37={{text}}1.3.6.1.5.5.7.3.3") `
        -CertStoreLocation "Cert:\\CurrentUser\\My" `
        -NotAfter (Get-Date).AddYears(5)
    
    $pwd = ConvertTo-SecureString -String $env:CADMATH_CERT_PASS -Force -AsPlainText
    Export-PfxCertificate -Cert $cert -FilePath "{PFX_PATH}" -Password $pwd -Force | Out-Null
    Export-Certificate -Cert $cert -FilePath "{CER_PATH}" -Force | Out-Null
    Write-Output "CERT_SUCCESS"
    """
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    if "CERT_SUCCESS" not in res.stdout:
        err = res.stderr or res.stdout
        raise RuntimeError(f"Khong the tao chung chi ky so: {err}")


def build_msix():
    if os.path.exists(MSIX_OUTPUT):
        os.remove(MSIX_OUTPUT)
    cmd = [MAKEAPPX, "pack", "/d", PACKAGE_DIR, "/p", MSIX_OUTPUT, "/o"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        err = res.stderr or res.stdout
        raise RuntimeError(f"MakeAppx that bai: {err}")


def sign_msix():
    """
    Ký số tệp MSIX:
    Sử dụng Thumbprint (/sha1) từ Windows Certificate Store để bảo mật tuyệt đối:
    KHÔNG BAO GIỜ truyền mật khẩu /p trên dòng lệnh của tiến trình.
    """
    ps_cmd = f"""
    $c = Get-ChildItem -Path Cert:\\CurrentUser\\My | Where-Object {{ $_.Subject -eq "{CERT_SUBJECT}" }} | Sort-Object NotAfter -Descending | Select-Object -First 1
    if ($c) {{ Write-Output $c.Thumbprint }}
    """
    res_t = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    thumb = res_t.stdout.strip()

    if not thumb:
        raise RuntimeError(f"Khong tim thay chung chi ky so voi Subject '{CERT_SUBJECT}' trong Cert:\\CurrentUser\\My")

    cmd_ts = [
        SIGNTOOL, "sign",
        "/fd", "SHA256",
        "/sha1", thumb,
        "/tr", "http://timestamp.digicert.com",
        "/td", "SHA256",
        MSIX_OUTPUT
    ]
    res = subprocess.run(cmd_ts, capture_output=True, text=True)
    if res.returncode != 0:
        err = res.stderr or res.stdout
        raise RuntimeError(f"Ky so signtool voi /sha1 that bai: {err}")


def create_installer_scripts():
    """
    B2: Tạo script cài đặt sideloading an toàn vào LocalMachine\\TrustedPeople thay vì Root CA.
    Tích hợp kiểm tra quyền Administrator ngay đầu script.
    """
    bat_content = r"""@echo off
title Cai Dat CAD Math Studio v2.2
chcp 65001 >nul
cls

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ===============================================================================
    echo [YÊU CẦU QUYỀN ADMINISTRATOR]: Kịch bản cài đặt yêu cầu quyền Administrator!
    echo Vui lòng nhấp chuột phải vào file Install_CADMathStudio_v2.2.bat và chọn:
    echo                         'Run as administrator'
    echo ===============================================================================
    echo.
    pause
    exit /b 1
)

echo ===============================================================================
echo            CÀI ĐẶT ỨNG DỤNG CAD MATH STUDIO v2.2 CHUẨN MICROSOFT
echo ===============================================================================
echo.
echo [1/2] Đang cài đặt Chứng chỉ số vào Trusted People (Sideloading Store Trust)...
powershell -NoProfile -Command "Import-Certificate -FilePath '%~dp0CADMathCert.cer' -CertStoreLocation Cert:\LocalMachine\TrustedPeople"

echo.
echo [2/2] Đang cài đặt gói ứng dụng MSIX CAD Math Studio v2.2...
powershell -NoProfile -Command "Add-AppxPackage -Path '%~dp0CADMathStudio_2.2.0.0.msix'"
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
"""
    bat_path = os.path.join(BASE_DIR, "Install_CADMathStudio_v2.2.bat")
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)


if __name__ == "__main__":
    try:
        print("[1/5] Chuan bi thu muc dong goi MSIX chuan Microsoft...", flush=True)
        prepare_package_files()
        print("[2/5] Tao chung chi ky so Microsoft Code Signing...", flush=True)
        create_certificate()
        print("[3/5] Dong goi tep tin bang makeappx.exe...", flush=True)
        build_msix()
        print("[4/5] Ky so goi MSIX bang signtool.exe...", flush=True)
        sign_msix()
        print("[5/5] Tao trinh cai dat 1-Click chuan Windows...", flush=True)
        create_installer_scripts()
        print("\nHOAN TAT TOAN BO QUY TRINH DONG GOI CHUAN MICROSOFT v2.2-RC5!", flush=True)
    except Exception as e:
        print("\n[THAT BAI]:", e, flush=True)
        sys.exit(1)
