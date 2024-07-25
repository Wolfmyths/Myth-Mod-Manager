# -*- mode: python ; coding: utf-8 -*-
import os
import sys

import patoolib

block_cipher = None

HIDDEN_IMPORTS = [
    'patoolib.programs',
    'patoolib.programs.ar',
    'patoolib.programs.arc',
    'patoolib.programs.archmage',
    'patoolib.programs.bsdcpio',
    'patoolib.programs.bsdtar',
    'patoolib.programs.bzip2',
    'patoolib.programs.cabextract',
    'patoolib.programs.chmlib',
    'patoolib.programs.clzip',
    'patoolib.programs.compress',
    'patoolib.programs.cpio',
    'patoolib.programs.dpkg',
    'patoolib.programs.flac',
    'patoolib.programs.genisoimage',
    'patoolib.programs.gzip',
    'patoolib.programs.isoinfo',
    'patoolib.programs.lbzip2',
    'patoolib.programs.lcab',
    'patoolib.programs.lha',
    'patoolib.programs.lhasa',
    'patoolib.programs.lrzip',
    'patoolib.programs.lzip',
    'patoolib.programs.lzma',
    'patoolib.programs.lzop',
    'patoolib.programs.mac',
    'patoolib.programs.nomarch',
    'patoolib.programs.p7azip',
    'patoolib.programs.p7rzip',
    'patoolib.programs.p7zip',
    'patoolib.programs.pbzip2',
    'patoolib.programs.pdlzip',
    'patoolib.programs.pigz',
    'patoolib.programs.plzip',
    'patoolib.programs.py_bz2',
    'patoolib.programs.py_echo',
    'patoolib.programs.py_gzip',
    'patoolib.programs.py_lzma',
    'patoolib.programs.py_tarfile',
    'patoolib.programs.py_zipfile',
    'patoolib.programs.rar',
    'patoolib.programs.rpm',
    'patoolib.programs.rpm2cpio',
    'patoolib.programs.rzip',
    'patoolib.programs.shar',
    'patoolib.programs.shorten',
    'patoolib.programs.star',
    'patoolib.programs.tar',
    'patoolib.programs.unace',
    'patoolib.programs.unadf',
    'patoolib.programs.unalz',
    'patoolib.programs.uncompress',
    'patoolib.programs.unrar',
    'patoolib.programs.unshar',
    'patoolib.programs.unzip',
    'patoolib.programs.zip',
]

DATA = [
    (os.path.join('src', 'icon.ico'), os.path.join('.', 'src')), 
    (os.path.join('src', 'graphics'), os.path.join('.', 'src', 'graphics')),
    (os.path.join('src', 'lang'), os.path.join('.', 'src', 'lang'))
    ]

BINARIES = []

if sys.platform.startswith('win'):

    ICON = os.path.join('src', 'icon.ico')

else:
    ICON = os.path.join('assets', 'icon.png')

a = Analysis(
    [os.path.join('src', '__main__.py')],
    pathex=[],
    binaries=BINARIES,
    datas=DATA,
    hiddenimports=HIDDEN_IMPORTS,
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
