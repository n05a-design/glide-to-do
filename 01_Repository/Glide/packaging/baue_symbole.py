#!/usr/bin/env python3
"""Erzeugt die Programmsymbole aus dem SVG-Master – reproduzierbar, ohne neue Abhängigkeit.

Quelle ist `src/glide/resources/logo/glide-app-icon.svg`, eine unveränderte
Kopie von `20_Grafik_Master/03_Fav-Icon/App-Icon-transparent-02.svg`. Tk 9 rechnet das
SVG in jeder Größe scharf (nanosvg); daraus entstehen unter `assets/icons/`:

- `glide.ico` – Windows: 16, 24, 32, 48, 64, 128 und 256 px, randlos, jede
  Größe als PNG im ICO-Container (Windows Vista und neuer);
- `glide_macos_1024.png` – macOS: die Fläche mit Apples Rand (824 von 1024 px);
  `packaging/macos/baue_app.py` macht daraus `Glide.icns`;
- `glide_512.png` – Linux (`.desktop`) und Stores, randlos.

Aufruf aus dem Repository (braucht Tk 9 und eine grafische Sitzung):

    python3 packaging/baue_symbole.py [--ziel assets/icons]
"""

from __future__ import annotations

import argparse
import base64
import struct
import sys
import tkinter as tk
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
QUELLE = REPO / "src" / "glide"
ICO_GROESSEN = (16, 24, 32, 48, 64, 128, 256)


def logo_modul():
    sys.dont_write_bytecode = True  # kein __pycache__ in src/glide
    sys.path.insert(0, str(QUELLE))
    import logo  # noqa: E402 – bewusst erst hier, aus src/glide
    return logo


def png_bytes(bild):
    """PNG-Bytes eines Tk-Bilds (Tk 9 liefert `data -format png` als Base64)."""
    daten = bild.tk.call(bild.name, "data", "-format", "png")
    if isinstance(daten, bytes):
        return daten
    return base64.b64decode(daten)


def ico_bytes(pngs):
    """ICO-Container aus (Kante, PNG-Bytes); Kante 256 wird als 0 geschrieben."""
    kopf = struct.pack("<HHH", 0, 1, len(pngs))
    eintraege, daten = b"", b""
    versatz = 6 + 16 * len(pngs)
    for kante, png in pngs:
        seite = 0 if kante >= 256 else kante
        eintraege += struct.pack("<BBBBHHII", seite, seite, 0, 0, 1, 32, len(png), versatz)
        daten += png
        versatz += len(png)
    return kopf + eintraege + daten


def erzeugen(ziel):
    logo = logo_modul()
    root = tk.Tk()
    root.withdraw()
    try:
        if not logo.has_svg(root):
            raise SystemExit("Dieses Tk liest kein SVG (nötig ist Tk 9).")
        ziel.mkdir(parents=True, exist_ok=True)
        randlos = logo.icon_svg(0.0)
        mit_rand = logo.icon_svg((1 - logo.MACOS_ICON_SHARE) / 2)

        def bild(svg, kante):
            return logo.square_icon(root, svg, kante)

        pngs = [(kante, png_bytes(bild(randlos, kante))) for kante in ICO_GROESSEN]
        (ziel / "glide.ico").write_bytes(ico_bytes(pngs))
        (ziel / "glide_macos_1024.png").write_bytes(png_bytes(bild(mit_rand, 1024)))
        (ziel / "glide_512.png").write_bytes(png_bytes(bild(randlos, 512)))
    finally:
        root.destroy()
    return [ziel / name for name in ("glide.ico", "glide_macos_1024.png", "glide_512.png")]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ziel", default=str(REPO / "assets" / "icons"), help="Ausgabeordner")
    argumente = parser.parse_args()
    for pfad in erzeugen(Path(argumente.ziel)):
        print(f"Geschrieben: {pfad} ({pfad.stat().st_size} Bytes)")


if __name__ == "__main__":
    main()
