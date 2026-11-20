# SPDX-License-Identifier: MPL-2.0
"""Native PyInstaller-Spezifikation für die beiden gewählten Zielsysteme."""
from pathlib import Path
from package_sources import TARGETS


# Ordner im Bau-Quellordner, die keine App-Pakete sind.
NICHT_APP_PAKETE = frozenset({"vendor", "resources", "licenses"})


def stage_modules(stage, bootstrap_name):
    """App-Module im Bau-Quellordner als {Importname: Pfad}.

    Flache Module heißen nach ihrem Dateinamen; App-Pakete wie `glide_shell`
    (D95) erscheinen als Paket und als `paket.modul`. PyInstaller sieht die
    Importe von `glide_app.py` nicht, weil es als Datei geladen wird; ohne
    diese Liste fehlte das Paket im Bundle.
    """
    stage = Path(stage)
    found = {p.stem: p for p in stage.glob("*.py") if p.name != bootstrap_name}
    for package in sorted(stage.iterdir()):
        init = package / "__init__.py"
        if package.is_dir() and package.name not in NICHT_APP_PAKETE and init.is_file():
            found[package.name] = init
            for module in sorted(package.glob("*.py")):
                if module.name != "__init__.py":
                    found[package.name + "." + module.stem] = module
    return found


def specification(stage, target, product, icon, *, modules=()):
    if target not in TARGETS:
        raise ValueError('Unbeauftragte Paketplattform.')
    stage=Path(stage)
    mac=target=='macos-arm64'
    lines=[
        '# Generated native development build; PyInstaller 6.22.3.',
        'a = Analysis(',
        '    '+repr([str(stage/'start_glide.py')])+',',
        '    pathex='+repr([str(stage),str(stage/'vendor')])+',',
        '    binaries=[],',
        '    datas='+repr([(str(stage/'resources'),'resources'),(str(stage/'licenses'),'licenses'),
                           (str(stage/'glide-input.json'),'.')])+',',
        "    hiddenimports="+repr(sorted(set(modules) | {"tkinterdnd2"}))+",",
        '    hookspath=[], hooksconfig={}, runtime_hooks=[],',
        "    excludes=['pip','setuptools','PyInstaller','drawing_prototype'],",
        '    noarchive=False, optimize=0,',
        ')',
        'pyz = PYZ(a.pure)',
        'exe = EXE(pyz, a.scripts, [], exclude_binaries=True,',
        '    name='+repr(product['APP_NAME'])+',',
        '    debug=False, bootloader_ignore_signals=False, strip=False, upx=False,',
        '    console=False, disable_windowed_traceback=False, argv_emulation=False,',
        '    target_arch='+repr('arm64'if mac else None)+',',
        '    codesign_identity=None, entitlements_file=None,',
        '    icon='+repr(str(icon))+',',
        '    version='+repr(None if mac else str(stage/'windows-version.txt'))+',',
        ')',
        'coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='+repr(product['APP_NAME'])+')',
    ]
    if not mac:
        # Python 3.14 verlangt Windows 10. UCRT und API-set-Verträge kommen
        # dort vom Betriebssystem; die von PyInstaller gesammelten alten
        # Kompatibilitätskopien sollen diese Anbieter nicht überlagern.
        position = lines.index('pyz = PYZ(a.pure)')
        lines[position:position] = [
            "def system_runtime_stub(name):",
            "    name = name.replace('\\\\', '/').rsplit('/', 1)[-1].casefold()",
            "    return name == 'ucrtbase.dll' or (name.endswith('.dll') and name.startswith(('api-ms-win-', 'ext-ms-win-')))",
            "a.binaries = [record for record in a.binaries if not system_runtime_stub(record[0])]",
        ]
    if mac:
        info=dict(CFBundleName=product['APP_NAME'],CFBundleDisplayName=product['APP_NAME'],
                  CFBundleShortVersionString=product['APP_VERSION'],CFBundleVersion=product['APP_VERSION'],
                  CFBundleDevelopmentRegion='de',LSApplicationCategoryType='public.app-category.productivity',
                  NSHighResolutionCapable=True)
        lines += ['app = BUNDLE(coll, name='+repr(product['APP_NAME']+'.app')+',',
                  '    icon='+repr(str(icon))+', bundle_identifier='+repr(product['APP_BUNDLE_ID'])+',',
                  '    info_plist='+repr(info)+',',')']
    return '\n'.join(lines)+'\n'


def windows_version(product):
    numbers=tuple(map(int,product['APP_VERSION'].split('.')))+(0,)
    strings=dict(FileDescription='Glide – Aufgaben und Listen',FileVersion=product['APP_VERSION'],
                 ProductName=product['APP_NAME'],ProductVersion=product['APP_VERSION'],
                 OriginalFilename='Glide.exe',InternalName='Glide')
    return ('VSVersionInfo(ffi=FixedFileInfo(filevers='+repr(numbers)+', prodvers='+repr(numbers)+', '
            'mask=0x3f, flags=0, OS=0x40004, fileType=0x1, subtype=0, date=(0,0)), kids=['
            'StringFileInfo([StringTable("040704b0", ['+
            ','.join('StringStruct('+repr(key)+','+repr(value)+')'for key,value in strings.items())+
            '])]), VarFileInfo([VarStruct("Translation", [1031,1200])])])\n')
