# Recette de construction : python -m PyInstaller DisplaySwitch.spec

import os
from pathlib import Path
import sys

# Limiter la recherche des DLL à Python et Windows pendant la construction.
windows_dir = Path(os.environ['SystemRoot'])
os.environ['PATH'] = os.pathsep.join(str(path) for path in (
    Path(sys.executable).parent,
    Path(sys.base_prefix),
    windows_dir / 'System32',
    windows_dir,
))

# Analyser main.py et ses dépendances ; config.json reste un fichier externe.
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
# Regrouper les modules Python dans l'archive interne.
pyz = PYZ(a.pure)

# Construire DisplaySwitch.exe en un seul fichier, sans console.
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DisplaySwitch',
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
)
