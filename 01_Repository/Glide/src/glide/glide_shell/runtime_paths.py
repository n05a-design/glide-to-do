# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 14: Daten- und Cacheordner nach Plattformkonvention auflösen, ohne Tk (D98).

Rein rechnerisch und ohne Dateisystemmutation:
- `platform_data_dir` und `platform_cache_dir` folgen macOS
  (`~/Library/…`), Windows (`APPDATA`/`LOCALAPPDATA`) und XDG unter Linux,
- `env_dir` liest einen Ordner aus einer Umgebungsvariablen,
- `read_pointer` liest einen Zeiger auf einen gewählten Datenordner aus
  einer JSON-Datei (auch mit Byte-Order-Mark),
- `resolve_base` wählt in fester Reihenfolge: ausdrücklicher Ordner,
  Umgebungsvariable, Zeiger, Standard.

Produktname, Variablen- und Dateinamen liefert der Host (Glide:
`runtime_config.py` mit `GLIDE_DATA_DIR`, `datenordner.json`). Plattform,
Umgebung und `os.path` lassen sich einreichen, damit Tests jede Plattform
simulieren. Vertrag: `tests/unit/test_shell_d98.py`.
"""

import json
import os
import sys


def _platform(platform):
    platform = sys.platform if platform is None else platform
    if platform == "darwin":
        return "macos"
    if platform in ("win32", "cygwin", "nt"):
        return "windows"
    return "linux"


def platform_data_dir(app_name, platform=None, environ=None, path=None):
    """Standardordner für Nutzerdaten von `app_name` nach Plattformkonvention."""
    environ = os.environ if environ is None else environ
    path = os.path if path is None else path
    kind = _platform(platform)
    if kind == "macos":
        base = path.join(path.expanduser("~/Library/Application Support"), app_name)
    elif kind == "windows":
        base = path.join(environ.get("APPDATA") or path.expanduser("~"), app_name)
    else:
        root = environ.get("XDG_DATA_HOME") or path.join(path.expanduser("~"), ".local", "share")
        base = path.join(root, app_name)
    return path.abspath(base)


def platform_cache_dir(app_name, platform=None, environ=None, path=None, windows_subdir="Cache", linux_name=None):
    """Standardordner für Cache von `app_name`; Linux nutzt `linux_name` (Vorgabe: klein geschrieben)."""
    environ = os.environ if environ is None else environ
    path = os.path if path is None else path
    kind = _platform(platform)
    if kind == "macos":
        base = path.join(path.expanduser("~/Library/Caches"), app_name)
    elif kind == "windows":
        base = path.join(environ.get("LOCALAPPDATA") or path.expanduser("~"), app_name, windows_subdir)
    else:
        root = environ.get("XDG_CACHE_HOME") or path.expanduser("~/.cache")
        base = path.join(root, linux_name or app_name.lower())
    return path.abspath(base)


def env_dir(environ, name, path=None):
    """Absoluter Ordner aus der Umgebungsvariablen `name` oder None, wenn sie leer ist."""
    path = os.path if path is None else path
    value = environ.get(name)
    return path.abspath(path.expanduser(value)) if value else None


def read_pointer(pointer_file, key="path"):
    """Gewählter Ordner aus einer JSON-Zeigerdatei oder None (fehlt, unlesbar, leer)."""
    if not os.path.isfile(pointer_file):
        return None
    try:
        # utf-8-sig: Ein von Hand mit Byte-Order-Mark gespeicherter Zeiger bleibt gültig.
        with open(pointer_file, "r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except (OSError, ValueError, TypeError):
        return None
    selected = data.get(key) if isinstance(data, dict) else None
    if isinstance(selected, str) and selected.strip():
        return os.path.abspath(os.path.expanduser(selected.strip()))
    return None


def resolve_base(explicit, environ, env_name, default_dir, pointer_file=None):
    """(Ordner, überschrieben): ausdrücklich, dann Umgebung, dann Zeiger, dann Standard."""
    override = explicit or environ.get(env_name)
    if override:
        return os.path.abspath(os.path.expanduser(override)), True
    if pointer_file:
        selected = read_pointer(pointer_file)
        if selected:
            return selected, False
    return default_dir, False
