"""Nachstellung des Windows-Befunds aus GitHub #138/#139 unter Linux.

Unter Windows wandelt ein PowerShell-Unterprozess JPEG-Vorschauen und hält die
Quelldatei offen, bis er beendet ist; ein offenes Handle verhindert dort das
Löschen (WinError 32). Diese Nachstellung erzwingt den Windows-Weg
(PreviewCache.PLATFORM = "nt"), ersetzt den Konverter durch einen langsamen,
der wie `run_converter` alle 0,1 s auf Abbruch prüft und die Datei so lange
geöffnet hält, und lässt TemporaryDirectory wie Windows scheitern, solange
eine Datei darin noch geöffnet ist.

Aufruf in `01_Repository/Glide` (Linux, Xvfb):
    xvfb-run -a python3 -B tests/qa-3.44.0/github_pruefung_2026-10-23/nachstellung_b04.py .
Vor der Korrektur von `test_uiux_paket.Lauf.ende` endet das mit PermissionError
(Exitcode 1), danach mit {"gruen": 1, "rot": []}.
"""
import os
import runpy
import sys
import tempfile
import threading
import time
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(REPO / "src/glide"))
sys.path.insert(0, str(REPO / "tests/integration"))
import image_conversion  # noqa: E402
import image_preview  # noqa: E402

image_preview.PreviewCache.PLATFORM = "nt"
offen, sperre = set(), threading.Lock()
gestartet = []


def langsam(path, cache_dir, platform, expected=None, cancel=None, **_kw):
    cancel = cancel or threading.Event()
    with open(path, "rb"):
        with sperre:
            offen.add(os.path.abspath(path))
            gestartet.append(path)
        try:
            ende = time.monotonic() + 3.0  # CI-PowerShell braucht mehrere Sekunden
            while time.monotonic() < ende and not cancel.wait(0.1):
                pass
            time.sleep(0.05)  # Prozessende nach kill
        finally:
            with sperre:
                offen.discard(os.path.abspath(path))
    return None


image_conversion.convert_file = langsam
original = tempfile.TemporaryDirectory.cleanup


def cleanup(self):
    with sperre:
        gehalten = [p for p in offen if p.startswith(os.path.abspath(self.name))]
    original(self)
    if gehalten:
        raise PermissionError(32, "nachgestellt: Datei noch von der Bildkonversion geöffnet",
                              os.path.basename(gehalten[0]))


tempfile.TemporaryDirectory.cleanup = cleanup
sys.argv = ["test_uiux_paket.py", "--fall", "b04"]
try:
    runpy.run_path(str(REPO / "tests/integration/test_uiux_paket.py"), run_name="__main__")
finally:
    print(f"Konversionen gestartet: {len(gestartet)}", flush=True)
