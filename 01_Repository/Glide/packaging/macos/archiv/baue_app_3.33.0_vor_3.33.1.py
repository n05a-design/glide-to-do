#!/usr/bin/env python3
"""Baut ein Entwicklungsbundle „Glide.app“ für macOS – ohne neue Abhängigkeit.

Das Bundle ist eine Vorstufe, kein Release:

- Es enthält die Glide-Quellen und Ressourcen, aber kein eigenes Python. Es
  startet mit dem installierten Python von python.org (Framework unter
  /Library/Frameworks/Python.framework) samt Tk.
- Als ausführbare Datei dient eine Kopie des Python-Starters aus dem
  Framework. Er bindet die Python-Bibliothek über einen absoluten Pfad ein und
  läuft deshalb auch aus dem Bundle heraus. Das Dock zeigt so „Glide“ mit
  eigenem Symbol statt „Python“, und macOS ordnet den Prozess dem
  Bundle-Identifikator de.shaye.glide zu – die Voraussetzung für echte
  Systembenachrichtigungen (Entscheidung SYSTEMBENACHRICHTIGUNGEN, Stufe B).
- Signiert wird nur ad hoc (`codesign -s -`): gültig für diesen Rechner, nicht
  für die Weitergabe. Signatur mit Developer-ID und Notarisierung folgen erst
  mit dem Release-Build (PyInstaller, requirements/build-macos.txt).

Werkzeuge: nur `iconutil`, `sips` und `codesign`, die macOS mitbringt.

Aufruf (aus dem Repository):

    python3 packaging/macos/baue_app.py --ziel build/macos
    python3 packaging/macos/baue_app.py --ziel build/macos --symbol anderes_1024.png

Das Programmsymbol kommt seit dem 29.09.2026 aus dem Logo-Master:
`assets/icons/glide_macos_1024.png`, erzeugt von `packaging/baue_symbole.py`
aus `src/glide/resources/logo/glide-app-icon.svg`. Bis dahin entstand hier ein
Pixel-„G“ als Platzhalter.
"""

from __future__ import annotations

import argparse
import os
import plistlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
QUELLE = REPO / "src" / "glide"
DATEIEN = ("app.pyw", "drawing.py", "drawing_image.py", "backdrop.py", "page_markdown.py", "image_preview.py",
           "logo.py", "glide_start.py", "schema_backups.py")
SYMBOL = REPO / "assets" / "icons" / "glide_macos_1024.png"


def lade_konstanten():
    """Version und Kennungen aus app.pyw lesen, ohne die Oberfläche zu starten."""
    werte = {}
    for zeile in (QUELLE / "app.pyw").read_text(encoding="utf-8").splitlines():
        for name in ("APP_NAME", "APP_VERSION", "APP_BUNDLE_ID", "APP_TAGLINE"):
            if zeile.startswith(f"{name} = "):
                werte[name] = zeile.split("=", 1)[1].strip().strip('"')
    fehlend = {"APP_NAME", "APP_VERSION", "APP_BUNDLE_ID"} - set(werte)
    if fehlend:
        raise SystemExit(f"In app.pyw fehlen: {', '.join(sorted(fehlend))}")
    return werte


def python_starter():
    """Der GUI-Starter des Python-Frameworks, mit dem dieses Skript läuft."""
    kandidat = Path(sys.base_prefix) / "Resources" / "Python.app" / "Contents" / "MacOS" / "Python"
    if not kandidat.is_file():
        raise SystemExit(
            "Kein Python-Framework gefunden. Das Entwicklungsbundle braucht Python von python.org "
            f"(gesucht: {kandidat}).")
    return kandidat


def baue_icns(png, ziel_icns):
    """Erzeugt aus einem quadratischen PNG (ab 1024 px empfohlen) eine .icns-Datei."""
    with tempfile.TemporaryDirectory() as ordner:
        satz = Path(ordner) / "Glide.iconset"
        satz.mkdir()
        for groesse in (16, 32, 128, 256, 512):
            for faktor, endung in ((1, ""), (2, "@2x")):
                pixel = groesse * faktor
                subprocess.run(["sips", "-z", str(pixel), str(pixel), str(png), "--out",
                                str(satz / f"icon_{groesse}x{groesse}{endung}.png")],
                               check=True, capture_output=True)
        subprocess.run(["iconutil", "-c", "icns", str(satz), "-o", str(ziel_icns)], check=True)


def baue(ziel, symbol=None):
    konstanten = lade_konstanten()
    app = Path(ziel) / f"{konstanten['APP_NAME']}.app"
    if app.exists():
        shutil.rmtree(app)
    inhalt = app / "Contents"
    (inhalt / "MacOS").mkdir(parents=True)
    ressourcen = inhalt / "Resources"
    glide = ressourcen / "glide"
    glide.mkdir(parents=True)
    for name in DATEIEN:
        shutil.copy2(QUELLE / name, glide / name)
    shutil.copytree(QUELLE / "resources", glide / "resources",
                    ignore=shutil.ignore_patterns("archiv", "__pycache__", ".DS_Store"))
    # tkdnd für das Ziehen aus dem Finder (27.09.2026); nur die macOS-Teile.
    if (QUELLE / "vendor").is_dir():
        shutil.copytree(QUELLE / "vendor", glide / "vendor",
                        ignore=shutil.ignore_patterns("__pycache__", ".DS_Store", "win-*", "linux-*"))

    # Die ausführbare Datei ist ein Shell-Starter, der die kopierte Python-
    # Datei im selben Bundle mit app.pyw aufruft. `exec` ersetzt den Prozess;
    # macOS sieht danach die Python-Kopie in Contents/MacOS und damit dieses
    # Bundle – mit Name, Symbol und Kennung aus der Info.plist.
    shutil.copy2(python_starter(), inhalt / "MacOS" / "glide-python")
    starter = inhalt / "MacOS" / konstanten["APP_NAME"]
    starter.write_text(
        "#!/bin/sh\n"
        "# Startet Glide mit dem Python im Bundle. Daten liegen wie immer unter\n"
        "# ~/Library/Application Support/Glide (oder dem gewählten Datenordner).\n"
        "# glide_start.py nutzt den Bytecode-Cache in ~/Library/Caches/Glide.\n"
        'HIER="$(cd "$(dirname "$0")" && pwd)"\n'
        'exec "$HIER/glide-python" "$HIER/../Resources/glide/glide_start.py" "$@"\n',
        encoding="utf-8")
    starter.chmod(0o755)

    symbol_png = Path(symbol) if symbol else SYMBOL
    if not symbol_png.is_file():
        raise SystemExit(f"Programmsymbol fehlt: {symbol_png}. Erst `python3 packaging/baue_symbole.py` ausführen.")
    baue_icns(symbol_png, ressourcen / "Glide.icns")

    info = {
        "CFBundleName": konstanten["APP_NAME"],
        "CFBundleDisplayName": konstanten["APP_NAME"],
        "CFBundleIdentifier": konstanten["APP_BUNDLE_ID"],
        "CFBundleShortVersionString": konstanten["APP_VERSION"],
        "CFBundleVersion": konstanten["APP_VERSION"],
        "CFBundleExecutable": konstanten["APP_NAME"],
        "CFBundleIconFile": "Glide.icns",
        "CFBundlePackageType": "APPL",
        "CFBundleInfoDictionaryVersion": "6.0",
        "CFBundleDevelopmentRegion": "de",
        "LSApplicationCategoryType": "public.app-category.productivity",
        "NSHighResolutionCapable": True,
        "NSHumanReadableCopyright": "Entwicklungsbundle – nicht zur Weitergabe",
    }
    with open(inhalt / "Info.plist", "wb") as datei:
        plistlib.dump(info, datei)
    (inhalt / "PkgInfo").write_text("APPL????", encoding="ascii")

    # Ad-hoc-Signatur: Apple-Silicon-Rechner starten unsignierte Programme
    # nicht, und die kopierte Python-Datei passt nach dem Umzug nicht mehr zu
    # ihrer alten Signatur.
    subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(app)],
                   check=True, capture_output=True)
    return app


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ziel", default=str(REPO / "build" / "macos"), help="Ausgabeordner")
    parser.add_argument("--symbol", help="Quadratisches PNG (mindestens 1024 px) statt des Glide-Symbols")
    argumente = parser.parse_args()
    if sys.platform != "darwin":
        raise SystemExit("Dieses Skript baut nur unter macOS.")
    Path(argumente.ziel).mkdir(parents=True, exist_ok=True)
    app = baue(argumente.ziel, argumente.symbol)
    print(f"Gebaut: {app}")
    print("Hinweis: Entwicklungsbundle mit Ad-hoc-Signatur; es nutzt das installierte Python "
          f"{sys.version.split()[0]} und dieselben Daten wie jede andere Glide-Fassung.")


if __name__ == "__main__":
    main()
