# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run_veda_ai.py'],
    pathex=[],
    binaries=[],
    datas=[('python_frontend', 'python_frontend'), ('data', 'data'), ('python_backend', 'python_backend')],
    hiddenimports=['pyttsx3', 'speech_recognition', 'fastapi', 'uvicorn'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='VEDA_AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['veda-icon.ico'],
)
