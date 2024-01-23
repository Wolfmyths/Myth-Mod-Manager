# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

DATA = [
    (os.path.join('src', 'icon.ico'), os.path.join('.', 'src')), 
    (os.path.join('src', 'graphics'), os.path.join('.', 'src', 'graphics'))
    ]

BINARIES = []

if sys.platform.startswith('win'):
    BINARIES.append(('src\\runGame.bat', '.'))

    ICON = os.path.join('src', 'icon.ico')

else:
    ICON = os.path.join('assets', 'icon.png')

a = Analysis(
    [os.path.join('src', '__main__.py')],
    pathex=[],
    binaries=BINARIES,
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
    icon=ICON,
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
