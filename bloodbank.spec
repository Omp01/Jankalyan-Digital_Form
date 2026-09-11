# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# Base directory
project_dir = os.path.abspath(SPECPATH)

datas = [
    (os.path.join(project_dir, 'templates'), 'templates'),
    (os.path.join(project_dir, 'static'), 'static'),
    (os.path.join(project_dir, 'database', 'schema.sql'), 'database'),
]

hidden_imports = [
    'waitress',
    'openpyxl',
    'openpyxl.styles',
    'openpyxl.utils',
    'jinja2',
    'sqlite3',
    'werkzeug',
    'werkzeug.security',
    'services',
    'services.path_service',
    'services.db_service',
    'services.audit_service',
    'services.excel_service',
    'middleware',
    'middleware.auth_decorator',
    'database',
    'database.db_init',
]

a = Analysis(
    ['desktop_launcher.py'],
    pathex=[project_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest', 'unittest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='JankalyanBloodBank',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to True so logs/server status are visible; can be set to False for windowless
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='JankalyanBloodBank',
)
