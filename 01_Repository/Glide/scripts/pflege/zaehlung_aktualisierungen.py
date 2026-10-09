#!/usr/bin/env python3
"""Speicher- und Neuaufbauanforderungen je Aktion zählen (P06r).

Aufruf (aus `01_Repository/Glide`):
    python3 -B scripts/pflege/zaehlung_aktualisierungen.py [--code ORDNER] [--json DATEI] [--aufgaben N]

Jede Aktion läuft über denselben Einstieg wie in der Oberfläche (Methode des
Menüs bzw. Kontextmenüs, Bestätigungen werden bejaht). Gezählt werden
Aufrufe von `save_items` und `save_settings`, tatsächlich geschriebene Dateien
(`datei_daten`, `datei_einstellungen`, `datei_sperre`), Neuaufbauten der Seitenleiste
(`_update_sidebar_list`) und des Inhalts (`_refresh_tree`). Eine
Aktion, die einen dieser Wege mehrfach anstößt, ohne dass sich dazwischen etwas
geändert hat, ist ein Kandidat für P06r; Zählen belegt Doppelarbeit, nicht
ihren Zeitanteil.

Künstliche Daten in einem temporären `GLIDE_DATA_DIR`; echte Daten werden nie
berührt.
"""

import argparse
from datetime import date, timedelta
import json
import os
import sys

import _glide_laden as gl

GEZAEHLT = ("save_items", "save_settings", "_update_sidebar_list", "_refresh_tree")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--code", help="Codeordner (Standard: src/glide)")
    parser.add_argument("--json", help="Ergebnisdatei")
    parser.add_argument("--aufgaben", type=int, default=200)
    args = parser.parse_args()
    datenordner = gl.isolieren("glide-zaehlung-")
    mod = gl.glide_laden(args.code)
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    fehler = []
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
    app.show_info = lambda *a, **k: None
    app.ask_yes_no = lambda *a, **k: True
    morgen = (date.today() + timedelta(days=1)).isoformat()

    ordner = app.new_folder_object("Projekte") if hasattr(app, "new_folder_object") else None
    if ordner is not None:
        app.folders.append(ordner)
    listen = []
    for nummer in range(3):
        eintrag = app.new_list_object(f"Liste {nummer + 1}", [app.new_item(f"Aufgabe {nummer}.{i}")
                                                              for i in range(args.aufgaben // 3)])
        app.lists.append(eintrag)
        listen.append(eintrag)
    app.save_items()
    app.update_sidebar_list()
    app.set_active_list(listen[0]["id"])
    root.update()

    zaehler = {name: 0 for name in GEZAEHLT}
    zaehler.update(datei_daten=0, datei_einstellungen=0, datei_sperre=0)
    for name in GEZAEHLT:
        original = getattr(app, name)

        def gezaehlt(*a, _name=name, _original=original, **k):
            zaehler[_name] += 1
            return _original(*a, **k)
        setattr(app, name, gezaehlt)
    schreiben = app.write_json_atomic

    def geschrieben(pfad, *a, **k):
        # Tatsächliche Dateischreibvorgänge; `save_settings` kann seit P06r
        # aufgeschoben oder bei gleichem Inhalt übersprungen werden.
        name = os.path.basename(pfad)
        if name == os.path.basename(mod.SAVE_FILE):
            zaehler["datei_daten"] += 1
        elif name == os.path.basename(mod.SETTINGS_FILE):
            zaehler["datei_einstellungen"] += 1
        elif name == os.path.basename(mod.LOCK_FILE):
            zaehler["datei_sperre"] += 1
        return schreiben(pfad, *a, **k)
    app.write_json_atomic = geschrieben

    def erste_aufgabe(liste_id):
        eintrag = next(e for e in app.lists if e["id"] == liste_id)
        return eintrag["items"][0]["id"]

    def auswaehlen(liste_id):
        app.set_active_list(liste_id)
        root.update()
        kennung = erste_aufgabe(liste_id)
        app.tree.selection_set(kennung)
        app.tree.focus(kennung)
        return kennung

    def eingabe():
        app.set_active_list(listen[0]["id"])
        app.entry.delete(0, "end")
        app.entry.insert(0, "Neue Aufgabe aus der Zählung")

    keine = lambda: None  # noqa: E731
    # (Name, Vorbereitung ungezählt, gezählte Aktion)
    aktionen = (
        ("Aufgabe anlegen (Eingabezeile)", eingabe, app.add_item),
        ("Abhaken", lambda: auswaehlen(listen[0]["id"]), app.toggle_done),
        ("Wichtigkeit setzen", lambda: auswaehlen(listen[0]["id"]), lambda: app.set_importance_selected(3)),
        ("Einplanen morgen", keine, lambda: app.plan_items_for_day([erste_aufgabe(listen[1]["id"])], morgen)),
        ("Aufgabe löschen", lambda: auswaehlen(listen[1]["id"]), app.delete_item),
        ("Rückgängig", keine, app.undo_last_change),
        ("Liste umbenennen", keine, lambda: app.apply_sidebar_rename(("list", listen[2]["id"]), "Umbenannt")),
        ("Liste archivieren", keine, lambda: app.set_archived("list", listen[2]["id"], True)),
        ("Liste zurückholen", keine, lambda: app.set_archived("list", listen[2]["id"], False)),
        ("Liste duplizieren", keine, lambda: app.duplicate_list(listen[1]["id"])),
        ("Liste in Ordner", lambda: app.get_selected_sidebar_list_ids.__func__ and setattr(
            app, "get_selected_sidebar_list_ids", lambda: [listen[1]["id"]]),
         lambda: app.move_selected_lists_to_folder(ordner["id"])),
        ("Liste löschen", keine, lambda: app.delete_list_by_id(listen[2]["id"])),
        ("Papierkorb leeren", keine, app.empty_trash),
    )
    ergebnis = []
    for name, vorbereitung, aktion in aktionen:
        vorbereitung()
        root.update()
        for schluessel in zaehler:
            zaehler[schluessel] = 0
        aktion()
        root.update()
        ergebnis.append({"aktion": name, **zaehler})
        print(f"{name:34} " + "  ".join(f"{k}={v}" for k, v in zaehler.items()), flush=True)
    umgebung = gl.umgebung(root)
    root.destroy()
    protokoll = gl.fehlerprotokoll(datenordner)
    gl.aufraeumen()
    if args.json:
        with open(args.json, "w", encoding="utf-8") as datei:
            json.dump({"version": mod.APP_VERSION, "umgebung": umgebung, "aufgaben": args.aufgaben,
                       "ergebnis": ergebnis, "callbackfehler": fehler, "fehlerprotokoll": protokoll[-2000:]},
                      datei, ensure_ascii=False, indent=2)
    if fehler or protokoll.strip():
        print("Fehler:", fehler, protokoll[-2000:], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    raise SystemExit(main())
