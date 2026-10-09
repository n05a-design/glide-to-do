"""Schnellstart für Glide: lädt die App als Modul und nutzt den Bytecode-Cache.

Python übersetzt ein direkt gestartetes Skript bei jedem Start neu – bei Glide
mehr als 50.000 Zeilen und etwa eine halbe Sekunde (Messung 26.09.2026). Als Modul
geladen, legt Python den übersetzten Stand einmal ab und liest ihn danach in
wenigen Millisekunden.

Der Bytecode liegt im Cache des Systems, nicht neben den Quellen: Im
signierten macOS-Bundle darf nichts hinzukommen, und im synchronisierten
Ablageordner soll kein `__pycache__` wandern.

Gestartet wird die erste `.pyw` im selben Ordner, deren Name mit „Glide“ oder
„app“ beginnt – im Repository `app.pyw`, in `07_Python-Versionen` die
versionierte Datei.
"""

import importlib.machinery
import importlib.util
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))


def cache_ordner():
    if sys.platform == "darwin":
        basis = os.path.expanduser("~/Library/Caches/Glide")
    elif os.name == "nt":
        basis = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "Glide", "Cache")
    else:
        basis = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "glide")
    return os.path.join(basis, "bytecode")


def app_datei():
    kandidaten = sorted(name for name in os.listdir(HIER)
                        if name.endswith(".pyw") and (name.startswith("Glide") or name == "app.pyw"))
    if not kandidaten:
        raise SystemExit(f"Keine Glide-Datei (.pyw) neben {__file__} gefunden.")
    return os.path.join(HIER, "app.pyw" if "app.pyw" in kandidaten else kandidaten[-1])


def main():
    # Zuerst den Cache umlenken: Schon die Prüfung unten wird übersetzt, und
    # im signierten Bundle darf neben den Quellen nichts entstehen.
    if not getattr(sys, "pycache_prefix", None):
        sys.pycache_prefix = cache_ordner()
    if HIER not in sys.path:
        sys.path.insert(0, HIER)
    # Mindestversion vor jedem Datenzugriff (AB08): Ein zu altes Python
    # bekommt eine verständliche Meldung statt eines Syntaxfehlers.
    import runtime_check
    runtime_check.pruefen_oder_beenden()
    loader = importlib.machinery.SourceFileLoader("glide_app", app_datei())
    spec = importlib.util.spec_from_loader(loader.name, loader)
    modul = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = modul
    loader.exec_module(modul)
    modul.main()


if __name__ == "__main__":
    main()
