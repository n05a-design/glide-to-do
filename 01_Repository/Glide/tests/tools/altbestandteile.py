#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Prüfung auf Bedienelemente im Systemaltstil (D66, menschliche Abnahme 07.11.2026).

Anlass: In der Live-Liste einer Seite stand noch eine native `ttk.Scrollbar`,
die unter Windows wie „Windows XP“ aussah und auch auf GitHub-Aufnahmen
auffiel. Glide zeichnet seine Bedienelemente selbst (`ThemedAutoScrollbar`,
`RoundedButton`, `AppOptionMenu` …), damit sie in jedem Design, Hell/Dunkel
und auf allen Plattformen gleich hochwertig aussehen. Diese Prüfung sorgt dafür,
dass kein Systemelement im Altstil zurückkehrt.

Zwei Stufen, eine Liste:

1. **Statisch** (`pruefen_quelle`, ohne Tk, Werkzeugtest der CI-Grundstufe):
   Jeder Aufruf eines Konstruktors aus `VERBOTEN` in den ausgelieferten
   Modulen ist ein Befund. Für `BESTAND` gilt eine Sperrklinke: Die heutige
   Anzahl darf nur sinken; jedes zusätzliche Vorkommen ist ein Befund.
2. **Laufzeit** (`fremdklassen`): Der Integrationsfall `altbestandteile`
   (`tests/integration/test_arbeitsmodi.py`) öffnet Hauptansichten, eine Seite
   mit Live-Liste und Dialoge und meldet jedes Widget einer Klasse aus
   `WIDGETKLASSEN_VERBOTEN` – auch wenn es über einen Umweg entsteht.

Aufruf: `python3 -B tests/tools/altbestandteile.py` (Exitcode 1 bei Befund).
"""
import ast
from collections import Counter
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
QUELLE = REPO / "src/glide"

# Ohne Ausnahme verboten: Glide hat dafür eigene, gezeichnete Bausteine oder
# braucht das Element nicht. Kanonische Namen nach Auflösung der Importe.
VERBOTEN = {
    "tkinter.Scrollbar": "ThemedAutoScrollbar (_dialog_scrollbar, _attach_field_scrollbar)",
    "tkinter.ttk.Scrollbar": "ThemedAutoScrollbar (_dialog_scrollbar, _attach_field_scrollbar)",
    "tkinter.scrolledtext.ScrolledText": "tk.Text mit ThemedAutoScrollbar",
    "tkinter.Spinbox": "eigenes Feld mit Glide-Knöpfen",
    "tkinter.ttk.Spinbox": "eigenes Feld mit Glide-Knöpfen",
    "tkinter.ttk.Combobox": "AppOptionMenu / LabelDropdown",
    "tkinter.OptionMenu": "AppOptionMenu",
    "tkinter.ttk.OptionMenu": "AppOptionMenu",
    "tkinter.Menubutton": "RoundedButton mit Menü",
    "tkinter.ttk.Menubutton": "RoundedButton mit Menü",
    "tkinter.ttk.Progressbar": "ProgressBar (Canvas)",
    "tkinter.ttk.Scale": "eigener Regler",
    "tkinter.ttk.LabeledScale": "eigener Regler",
    "tkinter.ttk.Notebook": "eigene Reiterleiste",
    "tkinter.ttk.Button": "RoundedButton",
    "tkinter.ttk.Checkbutton": "Glide-Schalter",
    "tkinter.ttk.Radiobutton": "Glide-Auswahl",
    "tkinter.ttk.Entry": "tk.Entry in _make_field",
    "tkinter.LabelFrame": "RoundedContainer",
    "tkinter.ttk.Labelframe": "RoundedContainer",
    "tkinter.ttk.LabelFrame": "RoundedContainer",
    "tkinter.ttk.Sizegrip": "kein Ersatz nötig",
    "tkinter.simpledialog.askstring": "Glide-Eingabedialog (run_modal)",
    "tkinter.simpledialog.askinteger": "Glide-Eingabedialog (run_modal)",
    "tkinter.simpledialog.askfloat": "Glide-Eingabedialog (run_modal)",
    "tkinter.simpledialog.Dialog": "Glide-Dialog (run_modal)",
}

# Sperrklinke für den heutigen Restbestand klassischer Tk-Elemente. Auf macOS
# zeichnet Tk sie nativ; unter Windows/Linux erscheinen sie im Systemaltstil.
# Ihr Ersatz ist ein eigener Auftrag (Plan §21.76); bis dahin darf ihre Zahl
# nur sinken. Nach einem Abbau die Zahl hier im selben Schritt senken.
BESTAND = {
    "tkinter.Checkbutton": 28,
    "tkinter.Radiobutton": 2,
    "tkinter.Listbox": 4,
    "tkinter.Scale": 1,
}

# Winfo-Klassen zur Laufzeit. „Scrollbar“ ist die klassische Tk-Leiste,
# „TScrollbar“ die ttk-Leiste; beide sind ausgeschlossen.
WIDGETKLASSEN_VERBOTEN = frozenset({
    "Scrollbar", "TScrollbar", "Spinbox", "TSpinbox", "TCombobox", "TProgressbar", "TScale",
    "Menubutton", "TMenubutton", "TNotebook", "TButton", "TCheckbutton", "TRadiobutton", "TEntry",
    "Labelframe", "TLabelframe", "TSizegrip",
})
WIDGETKLASSEN_BESTAND = frozenset({"Checkbutton", "Radiobutton", "Listbox", "Scale"})


def ausgelieferte_dateien(quelle=QUELLE):
    """Was in Python-Lieferung und Paketen landet; die Bedienprobe nicht."""
    return sorted([*quelle.glob("*.py"), quelle / "app.pyw"])


def _aliase(baum):
    namen = {}
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            for alias in knoten.names:
                if alias.name.split(".")[0] == "tkinter":
                    if alias.asname:
                        namen[alias.asname] = alias.name
                    else:
                        namen["tkinter"] = "tkinter"
        elif isinstance(knoten, ast.ImportFrom) and (knoten.module or "").split(".")[0] == "tkinter":
            for alias in knoten.names:
                namen[alias.asname or alias.name] = f"{knoten.module}.{alias.name}"
    return namen


def _kanonisch(funktion, aliase):
    teile = []
    while isinstance(funktion, ast.Attribute):
        teile.append(funktion.attr)
        funktion = funktion.value
    if not isinstance(funktion, ast.Name) or funktion.id not in aliase:
        return None
    return ".".join([aliase[funktion.id], *reversed(teile)])


def aufrufe(pfad=None, text=None):
    """(Zeile, kanonischer Name) jedes tkinter-Aufrufs einer Datei oder eines Quelltexts."""
    quelltext = text if text is not None else Path(pfad).read_text(encoding="utf-8-sig")
    baum = ast.parse(quelltext, filename=str(pfad or "<text>"))
    aliase = _aliase(baum)
    gefunden = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Call):
            name = _kanonisch(knoten.func, aliase)
            if name:
                gefunden.append((knoten.lineno, name))
    return gefunden


def befunde_aus(funde, bestand=None):
    """Bewertet [(Ort, Name)]: verbotene Konstrukte und überschrittene Sperrklinke."""
    bestand = BESTAND if bestand is None else bestand
    befunde, zaehlung = [], Counter()
    for ort, name in funde:
        if name in VERBOTEN:
            befunde.append(f"{ort}: {name} im Systemaltstil – stattdessen {VERBOTEN[name]}")
        elif name in bestand:
            zaehlung[name] += 1
    for name, erlaubt in bestand.items():
        if zaehlung[name] > erlaubt:
            befunde.append(f"{name}: {zaehlung[name]} statt höchstens {erlaubt} – neues klassisches Element; "
                           "Glide-Baustein verwenden")
    return befunde, dict(zaehlung)


def pruefen_quelle(dateien=None, bestand=None):
    """Liefert (Befunde, Zählung des Restbestands) für die ausgelieferten Module."""
    funde = [(f"{pfad.name}:{zeile}", name)
             for pfad in (dateien or ausgelieferte_dateien()) for zeile, name in aufrufe(pfad)]
    return befunde_aus(funde, bestand)


def _widgets(wurzel):
    stapel = [wurzel]
    while stapel:
        for kind in stapel.pop().winfo_children():
            yield kind
            stapel.append(kind)


def fremdklassen(wurzel):
    """Pfade und Klassen aller Widgets im Systemaltstil unter `wurzel` (Laufzeit)."""
    return [(str(kind), kind.winfo_class()) for kind in _widgets(wurzel)
            if kind.winfo_class() in WIDGETKLASSEN_VERBOTEN]


def bestandsklassen(wurzel):
    """Zählung des geduldeten Restbestands zur Laufzeit (nur Bericht)."""
    return dict(Counter(kind.winfo_class() for kind in _widgets(wurzel)
                        if kind.winfo_class() in WIDGETKLASSEN_BESTAND))


def main():
    befunde, zaehlung = pruefen_quelle()
    for befund in befunde:
        print("BEFUND", befund)
    print("Restbestand (Sperrklinke):", ", ".join(
        f"{name.split('.')[-1]} {zaehlung.get(name, 0)}/{grenze}" for name, grenze in sorted(BESTAND.items())))
    print("Altbestandteile: " + ("keine verbotenen Systemelemente" if not befunde else f"{len(befunde)} Befund(e)"))
    return 1 if befunde else 0


if __name__ == "__main__":
    sys.exit(main())
