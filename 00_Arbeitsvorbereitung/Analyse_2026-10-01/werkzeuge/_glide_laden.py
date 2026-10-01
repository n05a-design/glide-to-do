"""Gemeinsamer Ladeweg für die Analysewerkzeuge vom 01.10.2026.

Isoliert jede Probe in einem temporären Datenordner, *bevor* Glide importiert
wird (Regel: `GLIDE_DATA_DIR` vor dem Import setzen). Echte Nutzerdaten werden
nie berührt. Lädt die versionierte Hauptdatei aus `07_Python-Versionen` als
Modul, wie es `Schnellstart.pyw` tut.
"""

import glob
import importlib.machinery
import importlib.util
import os
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
STANDARD_CODEORDNER = os.path.join(REPO, "07_Python-Versionen")


def isolieren(praefix="glide-analyse-"):
    """Temporären Datenordner anlegen und für Glide setzen; Pfad zurückgeben."""
    ordner = tempfile.mkdtemp(prefix=praefix)
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    return ordner


def glide_laden(codeordner=None):
    """Hauptdatei als Modul `glide_app` laden und zurückgeben."""
    if "GLIDE_DATA_DIR" not in os.environ:
        raise RuntimeError("Erst isolieren(), dann laden – sonst träfe die Probe echte Daten.")
    codeordner = os.path.abspath(codeordner or STANDARD_CODEORDNER)
    # Kein Bytecode neben die Quellen: Der Laufzeitordner muss bytegleich bleiben.
    sys.dont_write_bytecode = True
    kandidaten = sorted(glob.glob(os.path.join(codeordner, "Glide*.pyw"))) or \
        sorted(glob.glob(os.path.join(codeordner, "app.pyw")))
    if not kandidaten:
        raise SystemExit(f"Keine Glide-Hauptdatei in {codeordner}")
    if codeordner not in sys.path:
        sys.path.insert(0, codeordner)
    loader = importlib.machinery.SourceFileLoader("glide_app", kandidaten[-1])
    spec = importlib.util.spec_from_loader(loader.name, loader)
    modul = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = modul
    loader.exec_module(modul)
    return modul


def fehlerprotokoll(datenordner, zeichen=4000):
    pfad = os.path.join(datenordner, "fehlerprotokoll.txt")
    if not os.path.exists(pfad):
        return ""
    with open(pfad, encoding="utf-8", errors="replace") as datei:
        return datei.read()[-zeichen:]


def umgebung(root):
    import platform
    import tkinter as tk
    return {
        "python": platform.python_version(),
        "tk": root.tk.call("info", "patchlevel"),
        "fenstersystem": root.tk.call("tk", "windowingsystem"),
        "plattform": platform.platform(),
        "schriftfamilien": len(__import__("tkinter.font").font.families(root)),
        "tk_version": tk.TkVersion,
    }
