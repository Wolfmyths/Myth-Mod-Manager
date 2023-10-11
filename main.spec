# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

DATA = [
    ('src/icon.ico', '.'), 
    ('src/graphics', 'graphics')
    ]


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[('src\\runGame.bat', '.')],
    datas=DATA,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Myth Mod Manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    icon='src\\icon.ico',
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
