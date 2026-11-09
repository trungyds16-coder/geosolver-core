import os
import sys
import shutil
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("="*65)
print("  QUY TRÌNH ĐÓNG GÓI CHUẨN MICROSOFT (MSIX & WIN32 EXECUTABLE)")
print("  Dự án: GeoSolver CAD (v3.1)")
print("="*65)

# 1. Kiểm tra / Cài đặt PyInstaller
try:
    import PyInstaller
    print("[1/4] PyInstaller đã sẵn sàng.")
except ImportError:
    print("[1/4] Đang cài đặt PyInstaller qua pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("      ✓ Cài đặt PyInstaller thành công!")

# 2. Biên dịch GeoSolver.exe với icon và version resource
print("\n[2/4] Đang biên dịch mã nguồn Python thành GeoSolver.exe...")
pyinstaller_cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--windowed",
    "--onedir",
    "--name", "GeoSolver",
    "--icon", "assets/app.ico",
    "--version-file", "file_version_info.txt",
    "geosolver_desktop.py"
]

res = subprocess.run(pyinstaller_cmd)
if res.returncode != 0:
    print("❌ Lỗi biên dịch PyInstaller!")
    sys.exit(1)
print("      ✓ Đã tạo thư mục dist/GeoSolver chứa GeoSolver.exe độc lập!")

# 3. Chuẩn bị cấu trúc thư mục MSIX Package Layout
print("\n[3/4] Đang cấu hình thư mục Layout MSIX chuẩn Microsoft...")
msix_dir = "msix_package"
if os.path.exists(msix_dir):
    shutil.rmtree(msix_dir)
os.makedirs(msix_dir, exist_ok=True)

# Copy AppxManifest.xml
shutil.copy("AppxManifest.xml", os.path.join(msix_dir, "AppxManifest.xml"))

# Copy Assets
assets_dst = os.path.join(msix_dir, "Assets")
os.makedirs(assets_dst, exist_ok=True)
for item in os.listdir("assets"):
    if item.endswith(".png"):
        shutil.copy(os.path.join("assets", item), os.path.join(assets_dst, item))

# Copy VFS (dist/GeoSolver)
vfs_dst = os.path.join(msix_dir, "VFS")
shutil.copytree("dist/GeoSolver", vfs_dst)
print(f"      ✓ Đã tạo thư mục đóng gói MSIX hoàn chỉnh tại: {os.path.abspath(msix_dir)}")

# 4. Tự động đóng gói và ký số nếu tìm thấy Windows SDK
print("\n[4/4] Đang tìm kiếm Windows SDK để đóng gói và ký số MSIX tự động...")
import glob
sdk_candidates = glob.glob(r"C:\Program Files (x86)\Windows Kits\10\bin\*\x64\makeappx.exe")
if not sdk_candidates:
    sdk_candidates = glob.glob(r"C:\Program Files\Windows Kits\10\bin\*\x64\makeappx.exe")

if sdk_candidates:
    makeappx_exe = sdk_candidates[-1]
    sdk_bin_dir = os.path.dirname(makeappx_exe)
    signtool_exe = os.path.join(sdk_bin_dir, "signtool.exe")
    msix_output = os.path.abspath("GeoSolver_v3.1.msix")
    print(f"      ✓ Đã tìm thấy Windows SDK tại: {sdk_bin_dir}")
    print("      -> Đang đóng gói file MSIX...")
    subprocess.check_call([makeappx_exe, "pack", "/d", os.path.abspath(msix_dir), "/p", msix_output, "/o"])
    print(f"      ✓ Đã tạo file gói cài đặt: {msix_output}")

    pfx_file = os.path.abspath("GeoSolverPartner.pfx")
    if not os.path.exists(pfx_file):
        pfx_file = os.path.abspath("GeoSolverTest.pfx")
    if os.path.exists(pfx_file) and os.path.exists(signtool_exe):
        print("      -> Đang ký số gói MSIX với chứng chỉ tự tạo...")
        try:
            subprocess.check_call([signtool_exe, "sign", "/fd", "SHA256", "/f", pfx_file, "/p", "GeoSolver2026!", msix_output])
            print("      ✓ Ký số thành công!")
        except Exception as e:
            print(f"      ⚠ Ký số cảnh báo: {e}")
else:
    print("      ⚠ Không tìm thấy makeappx.exe tự động. Vui lòng đóng gói bằng makeappx thủ công hoặc MSIX Packaging Tool.")

print("\n" + "="*65)
print("  HOÀN TẤT ĐÓNG GÓI CHO MICROSOFT STORE & WINDOWS 10/11!")
print("  1. File MSIX hoàn chỉnh:    GeoSolver_v3.1.msix")
print("  2. Thư mục thực thi Win32:  dist/GeoSolver/GeoSolver.exe")
print("  3. Thư mục layout MSIX:     msix_package/")
print("="*65)
