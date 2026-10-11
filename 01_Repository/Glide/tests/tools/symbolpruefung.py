#!/usr/bin/env python3
"""Zeigt, aus welcher Schrift Tk jedes Oberflächensymbol tatsächlich zeichnet.

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
        symbole = app.ICONS
        family = app.ui_font_family()
        print(f"Plattform: {sys.platform} · Tk {root.tk.call('package', 'provide', 'Tk')}")
        print(f"App-Familie: {family} · {len(symbole)} aufgelöste Symbole")
        print(f"Angepasste Zeichen: {len(app._symbol_changes)}")
        fazit = []
        for weight in ("normal", "bold"):
            schrift = tkfont.Font(root=root, family=family, size=12, weight=weight)
            eingestellt = str(schrift.actual("family"))
            print(f"\nSchnitt {weight} – eingestellt: {eingestellt}")
            for name, zeichen in symbole.items():
                familien = list(dict.fromkeys(str(root.tk.call("font", "actual", schrift.name,
                                                               "-family", char)) for char in zeichen))
                ersatz = any(f.casefold() != eingestellt.casefold() for f in familien)
                print(f"  {name:<18} {zeichen:<8} {schrift.measure(zeichen):>5} px · "
                      f"{schrift.metrics('linespace'):>3} px hoch · {' + '.join(familien)}"
                      + (" ← Ersatzschrift" if ersatz else ""))
                if ersatz:
                    fazit.append((weight, name, zeichen, familien))
        if fazit:
            print(f"FEHLER: {len(fazit)} Zeichen benötigen eine Ersatzschrift.")
            return 1
        print("Alle aufgelösten Zeichen kommen aus der tatsächlichen UI-Schrift.")
        print("Größe, Ausrichtung und DPI weiterhin auf jeder Plattform sichtbar prüfen.")
        return 0
    finally:
        if app is not None:
            app.cancel_pending_callbacks()
            app.release_data_lock()
        root.destroy()


if __name__ == "__main__":
    raise SystemExit(main())
