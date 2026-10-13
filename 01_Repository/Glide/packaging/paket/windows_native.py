"""PE-Architektur und interne DLL-Abhängigkeiten des nativen Windows-Pakets."""
from pathlib import Path, PurePosixPath, PureWindowsPath
import hashlib
import sys
from runtime_paths import validate_loaded

SYSTEM_DLLS = frozenset(name+'.dll' for name in (
    'advapi32', 'bcrypt', 'bcryptprimitives', 'cabinet', 'cfgmgr32', 'comctl32',
    'comdlg32', 'crypt32', 'cryptbase', 'cryptsp', 'dbghelp', 'dnsapi', 'dwmapi',
    'gdi32', 'imm32', 'iphlpapi', 'kernel32', 'kernelbase', 'mpr', 'msimg32',
    'msvcrt', 'ncrypt', 'netapi32', 'normaliz', 'ntdll', 'ole32', 'oleaut32',
    'powrprof', 'profapi', 'psapi', 'rpcrt4', 'sechost', 'secur32', 'setupapi',
    'shell32', 'shlwapi', 'ucrtbase', 'user32', 'userenv', 'usp10', 'uxtheme',
    'version', 'winhttp', 'wininet', 'winmm', 'winspool', 'wintrust', 'ws2_32',
    'wtsapi32'))


def system_library(name):
    name = name.casefold()
    return name in SYSTEM_DLLS or (name.endswith('.dll') and name.startswith(('api-ms-win-', 'ext-ms-win-')))


def validate_graph(records):
    """Keine fremden Python-/Tcl-/OpenSSL-/VC-Runtimes aus der Suchumgebung beziehen."""
    errors, by_name, paths = [], {}, set()
    for record in records:
        name = record['path']
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
            raise ValueError('Native Datei verlässt das Paket.')
        if name.casefold() in paths:
            raise ValueError('Mehrdeutige native Dateipfade.')
        paths.add(name.casefold())
        if record['machine'] != 0x8664:
            errors.append({'datei': name, 'fehler': 'Native Datei ist nicht Windows x64.'})
        key = path.name.casefold()
        if system_library(key):
            errors.append({'datei': name, 'fehler': 'Paket darf eine System-DLL nicht überlagern.'})
        by_name.setdefault(key, []).append(record)
    for name, values in by_name.items():
        if len({record['sha256'] for record in values}) != 1:
            errors.append({'datei': name, 'fehler': 'Gleichnamige native Dateien haben verschiedene Bytes.'})
    for record in records:
        for dependency in record['imports']:
            name = dependency.casefold()
            if PureWindowsPath(name).name != name or '/' in name or '\\' in name:
                errors.append({'datei': record['path'], 'abhaengigkeit': dependency,
                               'fehler': 'DLL-Import enthält einen fremden Pfad.'})
            elif name not in by_name and not system_library(name):
                errors.append({'datei': record['path'], 'abhaengigkeit': dependency,
                               'fehler': 'Nicht-systemweite DLL fehlt im Paket.'})
    return {'dateien': records, 'fehler': errors, 'exitcode': int(bool(errors))}


def audit(package):
    if sys.platform != 'win32':
        raise RuntimeError('PE-Prüfung ausschließlich auf dem nativen Windows-Prüfstand.')
    import pefile
    package = Path(package).resolve()
    records = []
    for path in sorted(package.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in ('.exe', '.dll', '.pyd'):
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(package):
            raise ValueError('Native Datei verlässt das Paket.')
        pe = pefile.PE(str(path), fast_load=True)
        try:
            pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
                                                  pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT']])
            imports = {entry.dll.decode('ascii') for key in ('DIRECTORY_ENTRY_IMPORT', 'DIRECTORY_ENTRY_DELAY_IMPORT')
                       for entry in getattr(pe, key, ())}
            records.append({'path': path.relative_to(package).as_posix(), 'machine': pe.FILE_HEADER.Machine,
                            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'imports': sorted(imports)})
        finally:
            pe.close()
    if not records:
        raise ValueError('Paket enthält keine nativen Windows-Dateien.')
    return validate_graph(records)
