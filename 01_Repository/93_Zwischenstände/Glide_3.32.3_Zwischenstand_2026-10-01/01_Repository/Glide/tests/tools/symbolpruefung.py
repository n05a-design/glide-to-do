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


def lade_symbole():
    """Liest die Symboltabelle aus dem Quelltext, ohne die App zu starten."""
    import ast

    quelle = (REPO / "src/glide/app.pyw").read_text(encoding="utf-8-sig")
    baum = ast.parse(quelle)
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name) and ziel.id == "ICONS":
                    return ast.literal_eval(knoten.value)
    raise SystemExit("ICONS nicht gefunden – liegt app.pyw an der erwarteten Stelle?")


def main():
    symbole = lade_symbole()
    loader = importlib.machinery.SourceFileLoader("glide_symbols", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    registered = mod.register_private_fonts()
    root = tk.Tk()
    root.withdraw()
    available = set(tkfont.families(root))
    family = next((name for name in mod.ListApp.PREFERRED_UI_FONTS if name in available),
                  tkfont.nametofont("TkDefaultFont", root=root).actual("family"))

    schriften = {
        "Seitenleiste und Liste (App-Schrift 12)": tkfont.Font(root=root, family=family, size=12),
        "Knöpfe (App-Schrift 10)": tkfont.Font(root=root, family=family, size=10),
    }

    print(f"Plattform: {sys.platform} · Tcl/Tk {root.tk.call('info', 'patchlevel')}")
    print(f"Privat registrierte Dateien: {len(registered)} · App-Familie: {family}")
    print()

    fazit = []
    for beschreibung, schrift in schriften.items():
        eingestellt = schrift.actual("family")
        print(f"{beschreibung} – eingestellt: {eingestellt}")
        print(f"  {'Symbol':<10} {'Zeichen':<8} {'Breite':>7} {'Höhe':>6}  Schrift")
        for name, zeichen in symbole.items():
            # Je Zeichen fragen, nicht je Zeichenkette: „⚑⚑" besteht aus zwei
            # Zeichen, und `font actual` beantwortet immer nur genau eines.
            familien = []
            for einzeln in zeichen:
                try:
                    gefunden = root.tk.call("font", "actual", schrift.name, "-family", einzeln)
                except tk.TclError:
                    gefunden = "(nicht ermittelbar)"
                if gefunden not in familien:
                    familien.append(gefunden)
            familie = " + ".join(familien)
            breite = schrift.measure(zeichen)
            hoehe = schrift.metrics("linespace")
            ersatz = familie != eingestellt
            marke = "  ← Ersatzschrift" if ersatz else ""
            codepunkte = " ".join(f"U+{ord(z):04X}" for z in zeichen)
            print(f"  {name:<10} {zeichen:<8} {breite:>7} {hoehe:>6}  {familie}{marke}")
            if ersatz:
                fazit.append((beschreibung, name, zeichen, codepunkte, familie))
        print()

    if not fazit:
        print("Alle Symbole kommen aus der eingestellten Schrift. Größe und Strichstärke")
        print("benötigen auf diesem Rechner keine Ersatzfamilie; weitere Plattformen getrennt prüfen.")
        root.destroy()
        return 0

    print("Aus einer Ersatzschrift gezeichnet:")
    for beschreibung, name, zeichen, codepunkte, familie in fazit:
        print(f"  {name} „{zeichen}\" ({codepunkte}) → {familie}  [{beschreibung}]")
    print()
    print("Das erklärt Größen- und Stärkeunterschiede zwischen den Systemen. Zwei Wege:")
    print("  1. Für diese Symbole Zeichen wählen, die die Systemschrift selbst enthält.")
    print("  2. Eine Schrift für die Symbole festlegen, die alle Zeichen mitbringt.")
    print("Die Entscheidung gehört in docs/ – dieses Werkzeug liefert nur den Befund.")
    root.destroy()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
