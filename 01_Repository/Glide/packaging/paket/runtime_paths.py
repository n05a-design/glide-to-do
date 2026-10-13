"""Filesystem- und DLL-eingebettete Tcl/Tk-Skriptpfade im eigenen Paket prüfen."""
from pathlib import Path, PureWindowsPath
import re


def validate_loaded(package, windows, libraries):
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
