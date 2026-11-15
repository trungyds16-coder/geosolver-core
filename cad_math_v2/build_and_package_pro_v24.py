import os
import sys
import shutil
import subprocess
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DIST_DIR = os.path.join(BASE_DIR, "dist")
BUILD_DIR = os.path.join(BASE_DIR, "build")
DIST_APP_DIR = os.path.join(DIST_DIR, "CADMathStudio")
PACKAGE_DIR = os.path.join(BASE_DIR, "msix_package")
ASSETS_DIR = os.path.join(PACKAGE_DIR, "Assets")

MSIX_PRO_OUTPUT = os.path.join(BASE_DIR, "CADMathStudio_Pro_2.4.0.0.msix")
MSIX_STORE_OUTPUT = os.path.join(BASE_DIR, "CADMathStudio_2.4.0.0.msix")

SDK_DIR = os.path.join(BASE_DIR, "tools")
MAKEAPPX = os.path.join(SDK_DIR, "makeappx.exe")
SIGNTOOL = os.path.join(SDK_DIR, "signtool.exe")

CERT_SUBJECT = "CN=CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE"
CERT_THUMBPRINT = "CC17C387DE28E461F417F24FB4FC699600CDD100"

APPX_MANIFEST_XML = r"""<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
         IgnorableNamespaces="uap rescap">
  <Identity Name="TLabtool.CADMathStudio"
            Publisher="CN=CF7A4DC0-CCBC-4FCE-BBA6-7EC14C731FEE"
            Version="2.4.0.0"
            ProcessorArchitecture="x64" />
  <Properties>
    <DisplayName>CAD Math Studio Pro</DisplayName>
    <PublisherDisplayName>TLabtool</PublisherDisplayName>
    <Logo>Assets\StoreLogo.png</Logo>
    <Description>CAD Math Studio Pro v2.4 - CAS Algebra, Calculus, Statistics, AI Integration and Advanced Print Engine.</Description>
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
      <uap:VisualElements DisplayName="CAD Math Studio Pro"
                          Description="CAD Math Studio Pro Desktop Application"
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

def generate_brand_assets():
    print("[1/5] Tao bo icon thuong hieu Pro sac net cho MSIX...")
    src_logo = os.path.join(BASE_DIR, "assets", "cad_math_logo_pro.png")
    if not os.path.exists(src_logo):
        src_logo = os.path.join(BASE_DIR, "assets", "cad_math_feather_90pct_navy_dark.png")

    master = Image.open(src_logo).convert("RGBA")

    # 1. Update .ico file
    ico_path = os.path.join(BASE_DIR, "assets", "cad_math_pro.ico")
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    master.save(ico_path, format="ICO", sizes=ico_sizes)
    # Also save standard ico if not present
    std_ico = os.path.join(BASE_DIR, "assets", "cad_math.ico")
    if not os.path.exists(std_ico):
        master.save(std_ico, format="ICO", sizes=ico_sizes)

    # 2. Assets in package
    os.makedirs(ASSETS_DIR, exist_ok=True)

    master.resize((150, 150), Image.Resampling.LANCZOS).save(os.path.join(ASSETS_DIR, "Square150x150Logo.png"), "PNG")
    master.resize((44, 44), Image.Resampling.LANCZOS).save(os.path.join(ASSETS_DIR, "Square44x44Logo.png"), "PNG")
    master.resize((50, 50), Image.Resampling.LANCZOS).save(os.path.join(ASSETS_DIR, "StoreLogo.png"), "PNG")

    wide = Image.new("RGBA", (310, 150), color=(15, 23, 42, 255))
    logo_w = master.resize((130, 130), Image.Resampling.LANCZOS)
    wide.paste(logo_w, ((310 - 130) // 2, (150 - 130) // 2), mask=logo_w)
    wide.save(os.path.join(ASSETS_DIR, "Wide310x150Logo.png"), "PNG")

    splash = Image.new("RGBA", (620, 300), color=(15, 23, 42, 255))
    logo_s = master.resize((220, 220), Image.Resampling.LANCZOS)
    splash.paste(logo_s, ((620 - 220) // 2, (300 - 220) // 2), mask=logo_s)
    splash.save(os.path.join(ASSETS_DIR, "SplashScreen.png"), "PNG")
    print("      ✓ Da tao bo icon MSIX Pro hoan chinh!")

def compile_pyinstaller():
    print("[2/5] Bien dich PyInstaller cad_math_v2.py (Pro v2.4) -> dist/CADMathStudio...")
    ico_path = os.path.join(BASE_DIR, "assets", "cad_math_pro.ico")
    if not os.path.exists(ico_path):
        ico_path = os.path.join(BASE_DIR, "assets", "cad_math.ico")
    assets_src = os.path.join(BASE_DIR, "assets")
    entry_script = os.path.join(BASE_DIR, "cad_math_v2.py")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "CADMathStudio",
        "--icon", ico_path,
        "--distpath", DIST_DIR,
        "--workpath", BUILD_DIR,
        "--paths", ROOT_DIR,
        "--add-data", f"{assets_src};assets",
        entry_script
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Loi PyInstaller:", res.stderr or res.stdout)
        raise RuntimeError("PyInstaller that bai!")
    print("      ✓ Bien dich PyInstaller Pro hoan tat thanh cong!")

def prepare_package():
    print("[3/5] Dong bo layout thu muc goi MSIX Pro...")
    if not os.path.exists(DIST_APP_DIR):
        raise FileNotFoundError(f"Khong tim thay {DIST_APP_DIR}")

    for item in os.listdir(DIST_APP_DIR):
        s = os.path.join(DIST_APP_DIR, item)
        d = os.path.join(PACKAGE_DIR, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    lic = os.path.join(BASE_DIR, "LICENSE.txt")
    if os.path.exists(lic):
        shutil.copy2(lic, os.path.join(PACKAGE_DIR, "LICENSE.txt"))

    shared_core_src = os.path.join(ROOT_DIR, "stem_shared_core")
    if os.path.exists(shared_core_src):
        for target in [os.path.join(PACKAGE_DIR, "stem_shared_core"), os.path.join(PACKAGE_DIR, "_internal", "stem_shared_core")]:
            if os.path.exists(target):
                shutil.rmtree(target)
            shutil.copytree(shared_core_src, target)

    generate_brand_assets()

    manifest_path = os.path.join(PACKAGE_DIR, "AppxManifest.xml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(APPX_MANIFEST_XML.strip())
    print("      ✓ Dong bo layout va AppxManifest Pro v2.4 thanh cong!")

def pack_and_sign_msix():
    print("[4/5] Dong goi MSIX bang makeappx.exe...")
    for out in [MSIX_PRO_OUTPUT, MSIX_STORE_OUTPUT]:
        if os.path.exists(out):
            os.remove(out)

    cmd = [MAKEAPPX, "pack", "/d", PACKAGE_DIR, "/p", MSIX_PRO_OUTPUT, "/o"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"MakeAppx that bai: {res.stderr or res.stdout}")
    print(f"      ✓ Tao file MSIX thanh cong: {MSIX_PRO_OUTPUT}")

    # Copy to MSIX_STORE_OUTPUT as well
    shutil.copy2(MSIX_PRO_OUTPUT, MSIX_STORE_OUTPUT)

    print("[5/5] Ky so goi MSIX bang signtool.exe voi chung chi Microsoft...")
    for out in [MSIX_PRO_OUTPUT, MSIX_STORE_OUTPUT]:
        cmd_ts = [
            SIGNTOOL, "sign",
            "/fd", "SHA256",
            "/sha1", CERT_THUMBPRINT,
            "/tr", "http://timestamp.digicert.com",
            "/td", "SHA256",
            out
        ]
        res = subprocess.run(cmd_ts, capture_output=True, text=True)
        if res.returncode != 0:
            cmd_notime = [
                SIGNTOOL, "sign",
                "/fd", "SHA256",
                "/sha1", CERT_THUMBPRINT,
                out
            ]
            res2 = subprocess.run(cmd_notime, capture_output=True, text=True)
            if res2.returncode != 0:
                raise RuntimeError(f"Ky so signtool that bai: {res2.stderr or res2.stdout}")
    print("      ✓ Ky so thanh cong ca 2 file MSIX Pro!")

def create_installer_script():
    bat_content = r"""@echo off
title Cai Dat CAD Math Studio Pro v2.4
chcp 65001 >nul
cls

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ===============================================================================
    echo [YÊU CẦU QUYỀN ADMINISTRATOR]: Kịch bản cài đặt yêu cầu quyền Administrator!
    echo Vui lòng nhấp chuột phải vào file Install_CADMathStudio_Pro_v2.4.bat và chọn:
    echo                         'Run as administrator'
    echo ===============================================================================
    echo.
    pause
    exit /b 1
)

echo ===============================================================================
echo          CÀI ĐẶT ỨNG DỤNG CAD MATH STUDIO PRO v2.4 CHUẨN MICROSOFT
echo ===============================================================================
echo.
echo [1/2] Đang cài đặt Chứng chỉ số vào Trusted People (Sideloading Store Trust)...
powershell -NoProfile -Command "Import-Certificate -FilePath '%~dp0CADMathCert.cer' -CertStoreLocation Cert:\LocalMachine\TrustedPeople"

echo.
echo [2/2] Đang cài đặt gói ứng dụng MSIX CAD Math Studio Pro v2.4...
powershell -NoProfile -Command "Add-AppxPackage -Path '%~dp0CADMathStudio_Pro_2.4.0.0.msix'"
if %errorlevel% equ 0 (
    echo.
    echo ===============================================================================
    echo   CÀI ĐẶT THÀNH CÔNG! BẠN CÓ THỂ MỞ 'CAD Math Studio Pro' TỪ START MENU.
    echo ===============================================================================
) else (
    echo.
    echo [LỖI]: Không thể cài đặt gói MSIX. Nếu máy đang cài bản từ Store, vui lòng gỡ cài đặt bản Store trước khi cài bản nội bộ này.
)
echo.
pause
"""
    bat_path = os.path.join(BASE_DIR, "Install_CADMathStudio_Pro_v2.4.bat")
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)

if __name__ == "__main__":
    generate_brand_assets()
    compile_pyinstaller()
    prepare_package()
    pack_and_sign_msix()
    create_installer_script()
    print("\n============================================================")
    print("HOÀN TẤT BIÊN DỊCH VÀ ĐÓNG GÓI CAD MATH STUDIO PRO v2.4.0.0!")
    print("============================================================")
