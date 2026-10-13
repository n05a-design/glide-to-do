"""Native PyInstaller-Spezifikation für die beiden gewählten Zielsysteme."""
from pathlib import Path
from package_sources import TARGETS


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
