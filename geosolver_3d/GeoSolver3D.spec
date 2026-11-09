# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

# SPECPATH is the directory of GeoSolver3D.spec (d:\AI DATA\STEM_APP\geosolver_3d)
BASE = os.path.abspath(SPECPATH)
ROOT = os.path.dirname(BASE)

block_cipher = None

# Filter test submodules of sympy and mpmath to keep package compact
hidden_imports = (
    collect_submodules('sympy', filter=lambda n: '.tests' not in n)
    + collect_submodules('mpmath', filter=lambda n: '.tests' not in n)
    + [
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'stem_shared_core',
        'stem_shared_core.report_engine',
        'stem_shared_core.ai_model_hub',
        'stem_shared_core.hf_downloader',
        'stem_shared_core.ai_config_dialog',
        'geosolver_3d',
        'geosolver_3d.geometry3d_kernel',
        'geosolver_3d.deductive3d_engine',
        'geosolver_3d.ui_state_manager',
    ]
)

a = Analysis(
    [os.path.join(BASE, 'app.py')],
    pathex=[BASE, ROOT],
    binaries=[],
    datas=[
        (os.path.join(BASE, 'assets'), 'geosolver_3d/assets'),
        (os.path.join(BASE, 'assets'), 'assets'),
        (os.path.join(ROOT, 'CAM_NANG_SU_DUNG_GEOSOLVER_3D.md'), '.'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter.test', 'test', 'pytest'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GeoSolver3D',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=os.path.join(BASE, 'file_version_info.txt'),
    icon=[os.path.join(BASE, 'assets', 'geosolver_3d.ico')],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='GeoSolver_3D',
)
