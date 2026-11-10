#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Prüft die freigegebene Schriftzuordnung jedes tatsächlich gezeichneten Symbols.

Warum das nötig ist: Tk misst und setzt mit der eingestellten Schrift. Fehlt
darin ein Zeichen, springt das Betriebssystem still auf eine Ersatzschrift um.
Unter Windows ist das für die geometrischen Formen meist „Segoe UI Symbol",
unter Linux „DejaVu Sans". Beide zeichnen dieselben Zeichen unterschiedlich
groß und unterschiedlich stark – deshalb sieht dieselbe Seitenleiste auf zwei
Systemen verschieden aus, ohne dass am Programm etwas anders wäre.

Das Werkzeug fragt Tk direkt: `font actual <Schrift> -family <Zeichen>` nennt
die Familie, die für genau dieses Zeichen zum Einsatz kommt. Weicht sie von der
eingestellten Schrift ab, kommt das Zeichen aus einer Ersatzschrift.

Aufruf aus dem Quellordner:

    python tests/tools/symbolpruefung.py

Ausgabe: je Symbol die verwendete Familie, die gemessene Breite und Höhe sowie
eine Markierung, wenn eine Ersatzschrift einspringt. Am Ende ein Fazit.

Braucht ausschließlich die Standardbibliothek und eine Anzeige.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys
import tempfile
import importlib.machinery
import importlib.util
import tkinter as tk
import tkinter.font as tkfont

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

REPO = Path(__file__).resolve().parents[2]

# Tests und Werkzeuge dürfen niemals den echten Nutzerdatenordner benutzen.
_isolated = tempfile.TemporaryDirectory(prefix="glide-symbols-")
os.environ["GLIDE_DATA_DIR"] = _isolated.name


def main():
    loader = importlib.machinery.SourceFileLoader("glide_symbols", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader.exec_module(mod)
    root = tk.Tk()
    root.withdraw()
    app = None
    try:
        app = mod.ListApp(root)
        root.withdraw()
        print(f"Plattform: {sys.platform} · Tk {root.tk.call('package', 'provide', 'Tk')}")
        fazit = []
        for style in mod.glide_fonts.STYLES:
            app.settings["ui_font_family"] = style.family
            app._ui_font_family = None
            app.apply_ui_font()
            symbole = app.ICONS
            family = app.ui_font_family()
            print(f"\nStil {style.label} · UI-Familie: {family} · "
                  f"{len(symbole)} Symbole · {len(app._symbol_changes)} angepasste Zeichen")
            for weight in ("normal", "bold"):
                print(f"\nSchnitt {weight} – UI-Schrift: {family}")
                for name, zeichen in symbole.items():
                    erwartet = getattr(app, "_symbol_fonts", {}).get(name, family)
                    erlaubt = {family, mod.glide_symbols.BUNDLED_SYMBOL_FAMILY,
                               *mod.glide_symbols.SYMBOL_FONT_FALLBACKS.get(name, ())}
                    schrift = tkfont.Font(root=root, font=app.symbol_font(name, 12))
                    schrift.configure(weight=weight)
                    eingestellt = str(schrift.actual("family"))
                    familien = list(dict.fromkeys(str(root.tk.call("font", "actual", schrift.name,
                                                                   "-family", char)) for char in zeichen))
                    ersatz = (erwartet not in erlaubt or eingestellt.casefold() != erwartet.casefold()
                              or any(f.casefold() != erwartet.casefold() for f in familien))
                    print(f"  {name:<18} {zeichen:<8} {schrift.measure(zeichen):>5} px · "
                          f"{schrift.metrics('linespace'):>3} px hoch · {' + '.join(familien)}"
                          + (" ← Ersatzschrift" if ersatz else ""))
                    if ersatz:
                        fazit.append((style.label, weight, name, zeichen, familien))
        if fazit:
            print(f"FEHLER: {len(fazit)} Zeichen verwenden eine nicht freigegebene oder unerwartete Schrift.")
            return 1
        print("Alle Zeichen kommen aus ihrer freigegebenen UI-, Begleit- oder gezielten Systemschrift.")
        print("Größe, Ausrichtung und DPI weiterhin auf jeder Plattform sichtbar prüfen.")
        return 0
    finally:
        if app is not None:
            app.cancel_pending_callbacks()
            app.release_data_lock()
        root.destroy()


if __name__ == "__main__":
    raise SystemExit(main())
