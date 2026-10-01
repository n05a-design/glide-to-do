#!/usr/bin/env python3
"""Erzeugt den „Rundgang“: je eine Liste, Notiz, Seite und Zeichnung (27.09.2026).

Kein Test, sondern ein Werkzeug. Der Nutzer wünschte sich Probedaten, die je
Seitenart zeigen, was Glide kann – die Seite als bebilderte Erklärung der
Funktionen. Die Bilder sind Aufnahmen des Glide-Fensters mit den künstlichen
Beispieldaten und liegen unter `tests/fixtures/rundgang/`.

Die Datei ist ein Teilbackup mit dem Ordner „Rundgang“. Einlesen über
„Listen/Ordner hinzufügen …“ ergänzt einen vorhandenen Bestand.

Aufruf:

    python3 tests/tools/rundgang.py [--ziel PFAD]

Braucht eine Tk-Anzeige, weil die Seitenbilder über den Seiteneditor
eingesetzt werden – derselbe Weg wie beim Nutzer.
"""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import os
import pathlib
import sys
import tempfile
from datetime import date, timedelta

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
APP_PATH = REPOSITORY_ROOT / "src" / "glide" / "app.pyw"
BILDER = REPOSITORY_ROOT / "tests" / "fixtures" / "rundgang"
DEFAULT_TARGET = REPOSITORY_ROOT / "tests" / "fixtures" / "beispiele" / "glide_rundgang.glidebackup"

SEITE = """# Glide in Bildern

Diese Seite ist selbst eine **Seite**: Text, Überschriften, Aufgaben und Bilder in einem ruhigen Lesefluss. Ziehe ein Bild an eine andere Stelle, ziehe an seiner Ecke oder klicke es mit der rechten Maustaste an.

## Listen

Die Liste ist das Herz von Glide: Punkte mit Fälligkeit, Wichtigkeit, Labels, Unterpunkten und Checklisten. Oben wird eingegeben – mit „/“-Befehlen wie /morgen oder /wichtig –, darunter steht die Liste. Wer Punkte markiert, bekommt unten die Auswahlleiste mit Wichtigkeit, Fällig, Einplanen, Labels und Löschen.

Seitenleiste, Kopfzeile und Fläche stehen in jeder Ansicht an derselben Stelle. Nichts springt beim Wechseln.

## Pinnwand

Jede Liste lässt sich als Pinnwand ansehen: Karten frei anordnen, Bereiche benennen, Karten verbinden und beschriften. Das Spaltenboard setzt ein Feld, sobald eine Karte in eine andere Spalte wandert.

## Zeichnungen

Die Pixel-Werkstatt zeichnet auf 16 bis 128 Zellen: Pinsel, Füllen, Pipette, Linie, Rechteck, Ellipse und Auswahl, zwei Farben, Symmetrie, Paletten und PNG-Export. Pixelsymbole schmücken Listen und Ordner.

## Mein Tag

„Mein Tag“ sammelt, was heute dran ist – mit Stundenraster, in das Punkte gezogen werden. „In Bearbeitung“ zeigt, was fällig oder überfällig ist.

## Suchen

Strg/Cmd+O öffnet die Suche über Seiten, Listen, Ordner, Punkte und Befehle. Ohne Eingabe zeigt sie, was zuletzt offen war.

## Zum Ausprobieren

- [ ] Ein Bild auf dieser Seite nach rechts ziehen
- [ ] Ein Bild an der Ecke größer ziehen
- [ ] „/“ am Anfang einer leeren Zeile tippen
- [x] Den Rundgang öffnen

> Seiten sind für längere Inhalte gedacht, etwa Berichte, die eine KI geschrieben hat: Markdown einfügen genügt.
"""

NOTIZ = """# Notizen

Eine **Notiz** ist eine Liste mit Textbereich: Oben stehen Aufgaben, darunter schreibt man frei. Text lässt sich *kursiv*, **fett** oder als `Code` setzen.

## Was eine Notiz kann

- Überschriften, Aufzählungen und nummerierte Listen
- Zitate und Codeblöcke
- Zeitstempel und Tagesabschnitte (Mehr › Zeitstempel)
- Präsentieren: Jede Überschrift wird eine Folie

1. Text markieren
2. B, I oder U wählen
3. Strg/Cmd+Z nimmt es zurück

> Im Notizbuch bekommt jeder Eintrag ein Datum – für Tagebuch, Protokolle und Wochenrückblicke.
"""


def load_module(data_dir):
    os.environ["GLIDE_DATA_DIR"] = str(data_dir)
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_rundgang", str(APP_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["glide_rundgang"] = module
    loader.exec_module(module)
    return module


def ruhe(root, runden=8):
    for _ in range(runden):
        root.update_idletasks()
        root.update()


def zeichnung(mod):
    """32 × 32 Pixel: Haus mit Garten, Baum und Sonne."""
    bild = mod.glide_drawing.DrawingModel.blank(32)
    def fuelle(x1, y1, x2, y2, farbe):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                bild.set_cell(x, y, farbe)
    fuelle(0, 0, 31, 22, "#CFE8F7")      # Himmel
    fuelle(0, 23, 31, 31, "#6FAF5B")     # Wiese
    for y in range(3, 8):                 # Sonne
        for x in range(23, 29):
            if (x - 25.5) ** 2 + (y - 5) ** 2 <= 7:
                bild.set_cell(x, y, "#F4C542")
    fuelle(7, 15, 18, 24, "#E9C99A")      # Wand
    for stufe in range(6):                # Dach
        fuelle(6 + stufe, 14 - stufe, 19 - stufe, 14 - stufe, "#B03A2E")
    fuelle(9, 17, 11, 19, "#4F7CAC")      # Fenster
    fuelle(14, 19, 16, 24, "#7A4B2A")     # Tür
    fuelle(24, 15, 25, 24, "#7A4B2A")     # Stamm
    for y in range(9, 17):                # Krone
        for x in range(20, 30):
            if (x - 24.5) ** 2 + (y - 12.5) ** 2 <= 14:
                bild.set_cell(x, y, "#3E7D3A")
    return bild.to_document()


def build(app, mod, root):
    heute = date.today()
    tag = lambda n: (heute + timedelta(days=n)).isoformat()
    ordner = app.new_folder_object("Rundgang", None, "accent")
    app.folders.append(ordner)
    label = {}
    for name, farbe in (("Rundgang", "accent"), ("Einkauf", "export")):
        eintrag = app.new_label_object(name, None, farbe if farbe in app.LABEL_COLOR_KEYS else None)
        app.labels.append(eintrag)
        label[name] = eintrag["id"]

    # --- Liste ---------------------------------------------------------------
    punkte = [
        app.new_item("Punkte anlegen", kind=app.ITEM_KIND_HEADING),
        app.new_item("Einkauf für das Wochenende", importance=3, due=tag(1), labels=[label["Einkauf"]],
                     checklist=[{"text": "Brot"}, {"text": "Milch", "done": True}, {"text": "Äpfel"}]),
        app.new_item("„/“-Befehle beim Eintippen", kind=app.ITEM_KIND_LONG, description=(
            "Tippe oben „Milch /morgen /wichtig“ und Enter: Der Punkt heißt „Milch“, ist morgen fällig und "
            "wichtig. Weitere Befehle: /heute, /übermorgen, ein Wochentag, /24.12.2026, /hoch, /mittel, "
            "/niedrig, /meintag und /Labelname. Tab ergänzt ein angefangenes Wort.")),
        app.new_item("Angebot vergleichen", due=tag(-1), importance=2, labels=[label["Rundgang"]]),
        app.new_item("Ordnen", kind=app.ITEM_KIND_HEADING),
        app.new_item("Urlaub vorbereiten", kind=app.ITEM_KIND_GROUP, children=[
            app.new_item("Pass prüfen", due=tag(7)),
            app.new_item("Unterkunft buchen", done=True),
        ]),
        app.new_item("Punkte markieren: unten erscheint die Auswahlleiste"),
        app.new_item("Erledigtes bleibt durchgestrichen stehen", done=True),
        app.new_item("Wiederkehrende Checkliste", kind=app.ITEM_KIND_LONG, description=(
            "Rechtsklick auf eine Aufgabenliste in der Seitenleiste › Wiederkehrende Checkliste: Sobald alles "
            "abgehakt ist, öffnet sich die Liste wieder – für Einkauf, Packliste oder Routinen.")),
    ]
    liste = app.new_list_object("Rundgang · Liste", punkte, None, ordner["id"], "accent",
                                "Aufgaben, Gruppen, Checklisten und „/“-Befehle.", None, [label["Rundgang"]])
    app.lists.append(liste)

    # --- Notiz ----------------------------------------------------------------
    notiz_doc = mod.glide_page_markdown.markdown_to_page(NOTIZ)
    notiz_doc.pop("tasks", None)
    notiz = app.new_list_object("Rundgang · Notiz", [app.new_item("Notiz lesen")], None, ordner["id"], None,
                                "Aufgaben oben, freier Text darunter.", None, [], list_kind="note",
                                rich_note=notiz_doc)
    app.lists.append(notiz)

    # --- Zeichnung --------------------------------------------------------------
    bild = app.new_list_object("Rundgang · Zeichnung", [], None, ordner["id"], None,
                               "32 × 32 Pixel. Pinsel B, Füllen F, Pipette I – oder die Werkzeugleiste oben.",
                               None, [], list_kind="drawing", drawing=zeichnung(mod))
    app.lists.append(bild)
    app.save_items()

    # --- Seite mit Bildern --------------------------------------------------------
    seite = app.new_page_from_markdown(SEITE, title="Rundgang · Seite", folder_id=ordner["id"])
    ruhe(root)
    app.set_active_list(seite["id"])
    ruhe(root)
    editor = app.rich_note_editor
    zeilen = editor.text.get("1.0", "end-1c").split("\n")

    def zeile(anfang):
        return f"{next(i for i, text in enumerate(zeilen, start=1) if text.startswith(anfang))}.0"

    # Von unten nach oben einsetzen: Zeilennummern darüber bleiben gültig.
    plan = [
        ("Strg/Cmd+O öffnet", "suche.png", "right", 300),
        ("„Mein Tag“ sammelt", "mein_tag.png", "left", 300),
        ("Die Pixel-Werkstatt", "zeichnung.png", "right", 300),
        ("Jede Liste lässt sich", "pinnwand.png", "center", 640),
        ("Die Liste ist das Herz", "liste.png", "left", 320),
    ]
    for anfang, datei, modus, breite in plan:
        schluessel = editor.insert_images([str(BILDER / datei)], zeile(anfang))[0]
        editor.images[schluessel]["mode"] = modus
        editor.images[schluessel]["width"] = breite
    editor.flush()
    ruhe(root)
    app.set_active_list(liste["id"])
    app.save_items()
    # Ein Teilbackup nur mit dem Ordner „Rundgang“: Beim Hinzufügen kommt kein
    # zweiter Eingang und keine leere „Meine Liste“ mit.
    return app.partial_backup_payload([], [ordner["id"]])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ziel", default=str(DEFAULT_TARGET))
    args = parser.parse_args()
    target = pathlib.Path(args.ziel).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_root:
        mod = load_module(pathlib.Path(temp_root) / "Glide")
        root = mod.tk.Tk()
        root.geometry("1200x820+0+30")
        app = mod.ListApp(root)
        app.show_info = app.show_warning = app.show_error = lambda *a, **k: None
        ruhe(root)
        payload = build(app, mod, root)
        app.write_complete_backup(str(target), payload)
        arten = {}
        for entry in app.lists:
            if entry.get("title", "").startswith("Rundgang"):
                arten[entry["title"]] = entry.get("list_kind")
        bilder = sum(len((entry.get("rich_note") or {}).get("images") or {}) for entry in app.lists)
        print(f"Geschrieben: {target}")
        for titel, art in arten.items():
            print(f"  {titel}  ({art})")
        print(f"  {bilder} Bilder in der Seite")
        root.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
