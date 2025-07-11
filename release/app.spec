# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('C:\\2_WorkSpace\\SYL\\venv\\Lib\\site-packages\\safehttpx\\version.txt', 'safehttpx'),
         ('C:\\2_WorkSpace\\SYL\\venv\\Lib\\site-packages\\groovy\\version.txt', 'groovy'),
         ('C:\\2_WorkSpace\\SYL\\src\\prompts\\summarize_daily_update.txt', 'src\\prompts'),
         ('C:\\2_WorkSpace\\SYL\\src\\prompts\\summarize_file_changes.txt', 'src\\prompts')]
datas += collect_data_files('gradio')
datas += collect_data_files('gradio_client')


a = Analysis(
    ['../app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['pywin32ctypes', 'win32ctypes.pywin32'],
    hookspath=['./release/hooks'],
    hooksconfig={},
    runtime_hooks=['./release/runtime_hook.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SYL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='SYL',
)
