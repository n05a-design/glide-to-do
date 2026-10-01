#!/usr/bin/env python3
"""Findet Aufrufe von `self.x(...)`, die es in der eigenen Klasse nicht gibt.

Warum dieses Werkzeug seit 3.23 dabei ist: Der Dialog „Tabellenspalten“ öffnete
sich seit 3.21.4 als leeres Fenster. Die Ursache war eine einzige Zeile –
`self.label(...)` in `ListApp`, obwohl es diese Methode nur in `ItemWorkspace`
gibt. Tk führt den Aufbau eines Dialogs aus einem Callback heraus aus; der
AttributeError landete dort in `report_callback_exception` und war für den
Nutzer unsichtbar. Das Fenster stand offen und blieb leer.

Weder die Syntaxprüfung noch die Erreichbarkeitsanalyse finden so etwas: Die
eine sieht gültiges Python, die andere sucht nach dem Gegenteil – Methoden, die
niemand ruft. Gesucht wird hier der Aufruf ohne Ziel.

Wie geprüft wird: Für jede Klasse im Quelltext werden alle über `self`
erreichbaren Namen gesammelt – Methoden, Klassenattribute, alles, was irgendwo
`self.x = …` zugewiesen bekommt, und dasselbe aus allen Basisklassen. Erbt eine
Klasse von etwas Fremdem (`tk.Frame`, `ttk.Treeview`), werden dessen Namen zur
Laufzeit über `dir()` ermittelt; ohne das wären alle geerbten Tk-Methoden
falsche Treffer.

Gemeldet wird nur, was mit hoher Sicherheit zur Laufzeit scheitert. Dynamisch
gesetzte Namen (`setattr`) werden mitgelesen, soweit sie im Quelltext als
Zeichenkette stehen.

Aufruf aus dem Quellordner:

    python tests/tools/attributpruefung.py

Rückgabewert 0, wenn nichts gefunden wurde; sonst 1.
Braucht ausschließlich die Standardbibliothek.
"""

from __future__ import annotations

import ast
import sys
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
QUELLE = REPO / "src/glide/app.pyw"

# Basisklassen außerhalb des Quelltexts: Ihre Namen kommen aus der Laufzeit.
FREMDE_BASEN = {
    "tk.Frame": tk.Frame, "tk.Canvas": tk.Canvas, "tk.Label": tk.Label,
    "tk.Toplevel": tk.Toplevel, "tk.Text": tk.Text, "tk.Entry": tk.Entry,
    "tk.Menu": tk.Menu, "ttk.Treeview": ttk.Treeview, "ttk.Frame": ttk.Frame,
    "RuntimeError": RuntimeError, "Exception": Exception, "ValueError": ValueError,
    "object": object,
}

# Attribute, die Tk erst beim Erzeugen einer Instanz setzt und die deshalb in
# `dir()` der Klasse fehlen. Sie sind vorhanden, sobald ein Widget existiert.
TK_INSTANZATTRIBUTE = {"master", "tk", "children", "widgetName", "_w", "_name", "_last_child_ids"}


def basisname(knoten):
    if isinstance(knoten, ast.Name):
        return knoten.id
    if isinstance(knoten, ast.Attribute):
        return f"{basisname(knoten.value)}.{knoten.attr}"
    return ""


def sammle_namen(klasse, klassen, gesehen=None):
    """Alle über `self` erreichbaren Namen einer Klasse."""
    gesehen = gesehen or set()
    if klasse.name in gesehen:
        return set()
    gesehen.add(klasse.name)
    namen = set()
    for basis in klasse.bases:
        name = basisname(basis)
        if name in klassen:
            namen |= sammle_namen(klassen[name], klassen, gesehen)
        elif name in FREMDE_BASEN:
            namen |= set(dir(FREMDE_BASEN[name]))
            if name.startswith(("tk.", "ttk.")):
                namen |= TK_INSTANZATTRIBUTE
        else:
            # Unbekannte Basis: Die Klasse wird nicht geprüft, statt falsche
            # Treffer zu melden.
            return None
    for kind in klasse.body:
        if isinstance(kind, (ast.FunctionDef, ast.AsyncFunctionDef)):
            namen.add(kind.name)
        elif isinstance(kind, ast.Assign):
            for ziel in kind.targets:
                if isinstance(ziel, ast.Name):
                    namen.add(ziel.id)
        elif isinstance(kind, ast.AnnAssign) and isinstance(kind.target, ast.Name):
            namen.add(kind.target.id)
        elif isinstance(kind, ast.ClassDef):
            namen.add(kind.name)
    for knoten in ast.walk(klasse):
        if (isinstance(knoten, ast.Attribute) and isinstance(knoten.value, ast.Name)
                and knoten.value.id == "self" and isinstance(knoten.ctx, (ast.Store, ast.Del))):
            namen.add(knoten.attr)
        if (isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Name)
                and knoten.func.id == "setattr" and len(knoten.args) >= 2
                and isinstance(knoten.args[1], ast.Constant)
                and isinstance(knoten.args[1].value, str)):
            namen.add(knoten.args[1].value)
    return namen


def pruefe(pfad=QUELLE):
    quelltext = pfad.read_text(encoding="utf-8-sig")
    baum = ast.parse(quelltext, filename=str(pfad))
    klassen = {knoten.name: knoten for knoten in ast.walk(baum)
               if isinstance(knoten, ast.ClassDef)}
    befunde = []
    ungeprueft = []
    for name, klasse in klassen.items():
        bekannt = sammle_namen(klasse, klassen)
        if bekannt is None:
            ungeprueft.append(name)
            continue
        for knoten in ast.walk(klasse):
            if (isinstance(knoten, ast.Attribute) and isinstance(knoten.value, ast.Name)
                    and knoten.value.id == "self" and isinstance(knoten.ctx, ast.Load)
                    and knoten.attr not in bekannt):
                befunde.append((knoten.lineno, name, knoten.attr))
    return sorted(set(befunde)), sorted(ungeprueft)


def main():
    befunde, ungeprueft = pruefe()
    for zeile, klasse, attribut in befunde:
        print(f"{QUELLE.name}:{zeile}: {klasse}.self.{attribut} gibt es in dieser Klasse nicht")
    if ungeprueft:
        print(f"Nicht geprüft (unbekannte Basisklasse): {', '.join(ungeprueft)}")
    if befunde:
        print(f"\n{len(befunde)} Aufruf(e) ohne Ziel. Das endet zur Laufzeit in einem "
              "AttributeError – in einem Dialogaufbau unsichtbar, aber wirksam.")
        return 1
    geprueft = len([knoten for knoten in ast.walk(ast.parse(
        QUELLE.read_text(encoding="utf-8-sig"))) if isinstance(knoten, ast.ClassDef)])
    print(f"Attributprüfung: keine Befunde in {geprueft - len(ungeprueft)} von {geprueft} Klassen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
