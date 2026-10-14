"""Filesystem- und DLL-eingebettete Tcl/Tk-Skriptpfade im eigenen Paket prüfen."""
from pathlib import Path, PureWindowsPath
import re


def defender_provider(path, programdata):
    """Nur den dokumentierten Defender-AMSI-Anbieter im Systembestand erkennen."""
    if not programdata:
        return None
    root = PureWindowsPath(programdata)
    path = PureWindowsPath(path)
    base = root/'Microsoft/Windows Defender/Platform'
    if not root.is_absolute() or '..' in path.parts or not path.is_relative_to(base):
        return None
    relative = path.relative_to(base)
    if (len(relative.parts) != 2 or relative.name.casefold() != 'mpoav.dll' or
            not re.fullmatch(r'\d+\.\d+\.\d+\.\d+(?:-\d+)?', relative.parts[0])):
        return None
    return relative.as_posix()


def authenticode(path, windows):
    """Native Signaturprüfung nur für die isolierte Windows-Paketprobe."""
    import json
    import ctypes
    import os
    import subprocess
    import sys
    if sys.platform != 'win32':
        raise RuntimeError('Authenticode braucht den nativen Windows-Prüfstand.')
    powershell = Path(windows)/'System32/WindowsPowerShell/v1.0/powershell.exe'
    literal = "'"+str(Path(path).resolve()).replace("'", "''")+"'"
    script = ('$s=Get-AuthenticodeSignature -LiteralPath '+literal+'; '
              '[pscustomobject]@{Status=$s.Status.ToString();Subject=$s.SignerCertificate.Subject}'
              ' | ConvertTo-Json -Compress')
    # PyInstaller setzt SetDllDirectoryW auf seine Paketbibliotheken. Ein
    # Systemprogramm muss dessen eigene DLLs laden; danach den Paketpfad erhalten.
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    get_directory = kernel.GetDllDirectoryW
    get_directory.argtypes = [ctypes.c_uint32, ctypes.c_wchar_p]
    get_directory.restype = ctypes.c_uint32
    set_directory = kernel.SetDllDirectoryW
    set_directory.argtypes = [ctypes.c_wchar_p]
    set_directory.restype = ctypes.c_int
    previous = ctypes.create_unicode_buffer(32768)
    length = get_directory(len(previous), previous)
    if length >= len(previous) or not set_directory(None):
        raise RuntimeError('System-DLL-Suchpfad nicht sicher herstellbar.')
    try:
        result = subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-NoLogo',
                                 '-Command', script], capture_output=True, text=True,
                                encoding='utf-8', errors='strict', timeout=30,
                                cwd=str(Path(windows)/'System32'),
                                env=dict(os.environ, PATH=str(Path(windows)/'System32'),
                                         PSModulePath=str(powershell.parent/'Modules')))
    finally:
        if not set_directory(previous.value if length else None):
            raise RuntimeError('Paket-DLL-Suchpfad konnte nicht wiederhergestellt werden.')
    if result.returncode:
        raise RuntimeError('Native Authenticode-Prüfung fehlgeschlagen: '+str(result.returncode)+
                           ' '+(result.stdout+result.stderr)[-3000:])
    return json.loads(result.stdout)


def validate_loaded(package, windows, libraries, *, programdata=None, authenticate=None):
    """Tatsächlich geladene Windows-Bibliotheken zusätzlich zum Baugraph prüfen."""
    package, windows = PureWindowsPath(package), PureWindowsPath(windows)
    if not package.is_absolute() or not windows.is_absolute():
        raise ValueError('Paket und Windows-Systemordner brauchen absolute Pfade.')
    system_roots = tuple(windows/name for name in ('System32', 'SysWOW64', 'WinSxS'))
    records, errors = [], []
    for name in libraries:
        path = PureWindowsPath(name)
        if not path.is_absolute():
            errors.append('Geladener Bibliothekspfad ist nicht absolut.')
        elif path.is_relative_to(package):
            records.append({'bereich': 'paket', 'datei': path.relative_to(package).as_posix()})
        elif any(path.is_relative_to(root) for root in system_roots):
            records.append({'bereich': 'windows', 'datei': path.relative_to(windows).as_posix()})
        elif defender_provider(path, programdata) is not None and authenticate is not None:
            signature = authenticate(str(path))
            if (signature.get('Status') == 'Valid' and
                    re.search(r'(?:^|,\s*)O=Microsoft Corporation(?:,|$)', signature.get('Subject', ''))):
                records.append({'bereich': 'windows-defender', 'datei': defender_provider(path, programdata),
                                'signatur': 'Valid', 'herausgeber': 'Microsoft Corporation'})
            else:
                errors.append('Windows-Defender-Anbieter ohne gültige Microsoft-Signatur: '+path.name)
        else:
            errors.append('Geladene Bibliothek liegt außerhalb des Pakets und Windows-Systemordners: '+path.name)
    return {'bibliotheken': records, 'fehler': errors, 'exitcode': int(bool(errors))}


def script_library(value, kind, package, *, provider=None):
    if kind not in ('tcl', 'tk'):
        raise ValueError('Unbekannte Skriptbibliothek.')
    package = Path(package).resolve()
    value = str(value)
    if value.startswith('//zipfs:/'):
        if value != f'//zipfs:/lib/{kind}/{kind}_library':
            raise ValueError('Unbekannter eingebetteter Tcl/Tk-Skriptpfad.')
        if provider is None:
            raise ValueError('Eingebettete Skripte brauchen einen nachgewiesenen geladenen Paketanbieter.')
        provider = Path(provider).resolve()
        if not provider.is_file() or not provider.is_relative_to(package):
            raise ValueError('Anbieter der eingebetteten Skripte liegt außerhalb des Pakets.')
        return {'modus': 'eingebettetes-zip', 'ort': value,
                'anbieter': provider.relative_to(package).as_posix()}
    library = Path(value).resolve()
    if not library.is_dir() or not library.is_relative_to(package):
        raise ValueError('Tcl/Tk-Skriptbibliothek liegt außerhalb des Pakets oder fehlt.')
    return {'modus': 'dateien', 'ort': library.relative_to(package).as_posix()}


_TK = re.compile(r"(?:lib)?(?:tcl9)?tk9[0-9]*(?:\.[0-9]+)*\.(?:dylib|dll|so)")
_TCL = re.compile(r"(?:lib)?tcl9[0-9]*(?:\.[0-9]+)*\.(?:dylib|dll|so)")


def tk_providers(libraries):
    """Geladene Tcl/Tk-Bibliotheken erkennen.

    Exakte Namensmuster: macOS-Frameworks `Tcl`/`Tk`, Windows `tcl90.dll`/
    `tcl9tk90.dll`, Linux/macOS `libtcl9.0.dylib`/`libtcl9tk9.0.dylib`.
    Erweiterungen wie `libtcl9tkdnd2.10.2.dylib` sind keine Anbieter.
    """
    found = {'tcl': [], 'tk': []}
    for value in libraries:
        name = Path(value).name.casefold()
        if name == 'tk' or _TK.fullmatch(name):
            found['tk'].append(value)
        elif name == 'tcl' or _TCL.fullmatch(name):
            found['tcl'].append(value)
    if any(len(values) > 1 for values in found.values()):
        raise ValueError('Mehrere Tcl-/Tk-Anbieter sind gleichzeitig geladen.')
    return {kind: values[0] for kind, values in found.items() if values}
