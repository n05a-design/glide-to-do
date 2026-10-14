"""Lizenzzuordnung der tatsächlich analysierten Pakete, ohne Tk/Appimport."""
from pathlib import Path, PurePosixPath
import re


def pure_components(records, *, stage, stdlib, pyinstaller):
    stage, stdlib, pyinstaller = map(lambda p: Path(p).resolve(), (stage, stdlib, pyinstaller))
    result = {}
    for name, origin, kind in records:
        if kind != "PYMODULE" or name in result:
            raise ValueError("Mehrdeutiger oder unbekannter Python-Analysebestand: " + name)
        path = Path(origin).resolve()
        if path == stage / (name + ".py") and "." not in name:
            component = "Glide"
        elif path.is_relative_to(stage / "vendor/tkinterdnd2"):
            component = "tkinterdnd2"
        elif path.is_relative_to(stdlib) and not {"site-packages", "dist-packages"} & set(path.relative_to(stdlib).parts):
            component = "Python"
        elif path.is_relative_to(pyinstaller):
            component = "PyInstaller"
        else:
            raise ValueError("Python-Modul ohne belegte Herkunft: " + name)
        result[name] = [component]
    if not result:
        raise ValueError("Leerer Python-Analysebestand")
    return result


def macos_native_components(names):
    result = {}
    fixed = {
        "Contents/MacOS/Glide": ["PyInstaller"],
        "Contents/Frameworks/Tcl": ["Tcl", "libtommath", "Henry-Spencer-Regex"],
        "Contents/Frameworks/Tk": ["Tk", "NanoSVG"],
        "Contents/Frameworks/libtcl9.1.dylib": ["Tcl", "libtommath", "Henry-Spencer-Regex", "utf8proc"],
        "Contents/Frameworks/libtcl9tk9.1.dylib": ["Tk", "NanoSVG"],
        "Contents/Frameworks/_tkinter.cpython-314-darwin.so": ["Python"],
        "Contents/Frameworks/libcrypto.3.dylib": ["OpenSSL"],
        "Contents/Frameworks/libssl.3.dylib": ["OpenSSL"],
        "Contents/Frameworks/libzstd.1.dylib": ["Zstandard"],
        "Contents/Frameworks/tkinterdnd2/tkdnd/osx-arm64-tcl9/libtcl9tkdnd2.10.2.dylib": ["tkdnd"],
    }
    extension = re.compile(r"Contents/Frameworks/python3__dot__14/lib-dynload/([A-Za-z_][A-Za-z_0-9]*)\.cpython-314-darwin\.so")
    # Aus der nativen CPython-3.14-Analyse; unbekannte Erweiterungen brauchen
    # eine eigene Herkunftsprüfung statt pauschal die Python-Lizenz zu erben.
    allowed = set("_bisect _blake2 _bz2 _codecs_cn _codecs_hk _codecs_iso2022 _codecs_jp _codecs_kr _codecs_tw _csv _ctypes _decimal _elementtree _hashlib _heapq _json _lzma _md5 _multibytecodec _pickle _posixsubprocess _queue _random _scproxy _sha1 _sha2 _sha3 _socket _ssl _statistics _struct _tkinter _uuid _zoneinfo _zstd array binascii fcntl grp math pyexpat resource select unicodedata zlib _sqlite3".split())
    for name in names:
        path = PurePosixPath(name)
        if path.as_posix() != name or path.is_absolute() or ".." in path.parts or "\\" in name or name in result:
            raise ValueError("Ungültiger oder doppelter Binärpfad: " + name)
        if name in fixed:
            components = fixed[name]
        elif name == "Contents/Frameworks/Python.framework/Versions/3.14/Python":
            components = ["Python"]
        elif (match := extension.fullmatch(name)) and match[1] in allowed:
            components = ["Python"]
            extra = {"_lzma": "liblzma", "_decimal": "libmpdec", "_zstd": "Zstandard",
                     "_ssl": "OpenSSL", "_hashlib": "OpenSSL", "_sqlite3": "SQLite"}.get(match[1])
            if extra:
                components.append(extra)
            # Expat-Beleg steht im originalen Python-LICENSE/THIRD-PARTY-NOTICES.
        else:
            raise ValueError("Native Datei ohne belegte Lizenzzuordnung: " + name)
        result[name] = list(components)
    if not result:
        raise ValueError("Leerer nativer Analysebestand")
    return result


def resource_components(names):
    result = {}
    for name in names:
        path = PurePosixPath(name)
        if path.as_posix() != name or path.is_absolute() or '..' in path.parts or '\\' in name or name in result:
            raise ValueError('Ungültiger oder doppelter Ressourcenpfad: ' + name)
        if path.parts[:2] in (('resources', 'logo'), ('resources', 'templates')):
            components = ['Glide']
        elif path.parts[:2] == ('resources', 'fonts'):
            components = ['Glide-Schriften']
        elif name in ('resources/timezones/iana-2026e.zip', 'resources/timezones/LICENSE-iana.txt'):
            components = ['IANA-Zeitzonen']
        elif name in ('resources/timezones/windowsZones.xml', 'resources/timezones/LICENSE-CLDR.txt'):
            components = ['Unicode-CLDR']
        elif name == 'resources/timezones/provenance.json':
            components = ['IANA-Zeitzonen', 'Unicode-CLDR']
        else:
            raise ValueError('Ressource ohne belegte Herkunft: ' + name)
        result[name] = components
    if not result:
        raise ValueError('Leerer Ressourcenbestand')
    return result


def windows_native_components(names):
    """Geprüfte CPython-/Tcl-/Tk-9-Dateinamen; neue DLLs brauchen neue Belege."""
    fixed = {
        'Glide.exe': ['PyInstaller'],
        '_internal/python314.dll': ['Python', 'zlib-ng'],
        '_internal/python3.dll': ['Python'],
        '_internal/tcl90.dll': ['Tcl', 'Henry-Spencer-Regex'],
        '_internal/tcl9tk90.dll': ['Tk', 'NanoSVG'],
        '_internal/libtommath.dll': ['libtommath'],
        '_internal/libcrypto-3.dll': ['OpenSSL'],
        '_internal/libssl-3.dll': ['OpenSSL'],
        '_internal/libffi-8.dll': ['libffi'],
        '_internal/sqlite3.dll': ['SQLite'],
        '_internal/zlib1.dll': ['zlib'],
        '_internal/VCRUNTIME140.dll': ['Microsoft-VC-Runtime'],
        '_internal/VCRUNTIME140_1.dll': ['Microsoft-VC-Runtime'],
        '_internal/tkinterdnd2/tkdnd/win-x64-tcl9/libtkdnd2.10.2.dll': ['tkdnd'],
    }
    allowed = set('_asyncio _bz2 _ctypes _decimal _elementtree _hashlib _lzma _multiprocessing _overlapped _queue _socket _sqlite3 _ssl _tkinter _uuid _wmi _zoneinfo _zstd pyexpat select unicodedata winsound'.split())
    extra = {'_lzma': 'liblzma', '_decimal': 'libmpdec', '_zstd': 'Zstandard'}
    result = {}; seen = set()
    for name in names:
        path = PurePosixPath(name)
        if path.as_posix() != name or path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name or name.casefold() in seen:
            raise ValueError('Ungültiger oder doppelter Windows-Binärpfad: ' + name)
        seen.add(name.casefold())
        if name in fixed:
            components = fixed[name]
        elif path.parent == PurePosixPath('_internal') and path.suffix == '.pyd' and path.stem in allowed:
            components = ['Python'] + ([extra[path.stem]] if path.stem in extra else [])
        else:
            raise ValueError('Windows-Datei ohne belegte Lizenzzuordnung: ' + name)
        result[name] = list(components)
    if not result:
        raise ValueError('Leerer nativer Windows-Analysebestand')
    return result


def validate_components(matrix, components):
    by_name = {}
    for record in components:
        name = record.get("name")
        if not name or name in by_name or not record.get("version") or not record.get("source") or not record.get("files"):
            raise ValueError("Unvollständiger oder doppelter Lizenzbeleg")
        by_name[name] = record
    needed = {name for names in matrix.values() for name in names}
    missing = needed - by_name.keys()
    if missing:
        raise ValueError("Fehlende Lizenzbelege: " + ", ".join(sorted(missing)))
    return {name: by_name[name] for name in sorted(needed)}
