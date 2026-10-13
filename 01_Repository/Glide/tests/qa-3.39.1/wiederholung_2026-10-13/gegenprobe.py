"""Getrennte Gegenprobe zu A28, A29 und A30 an einem wählbaren Quellstand.

Die Pflichtsuite `test_wiederholung3391` bricht am ersten Befund ab. Diese
Probe prüft die drei Defekte einzeln über dieselben Einstiege (Eingabezeile
mit Anlegen, ICS-Ausgabe, ICS-Import, Zeitzone des Aufgabenimports) und
schreibt je Defekt „behoben“ oder „vorhanden“ als JSON. Erwartung: 3.39.0
dreimal vorhanden, 3.39.1 dreimal behoben. Künstliche Daten in einem
temporären GLIDE_DATA_DIR.

Aufruf aus `01_Repository/Glide`:
    python3 -B tests/qa-3.39.1/wiederholung_2026-10-13/gegenprobe.py --app <app.pyw> --json <Ziel>
"""
import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, required=True)
parser.add_argument("--json", type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))


def kalender(*bloecke):
    zeilen = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Fremd//Test//EN"]
    for block in bloecke:
        zeilen += ["BEGIN:VEVENT", *block, "END:VEVENT"]
    return "\r\n".join(zeilen + ["END:VCALENDAR"]) + "\r\n"


with tempfile.TemporaryDirectory(prefix="glide-gegenprobe3391-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_gegenprobe3391", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    root = mod.tk.Tk()
    app = mod.ListApp(root)
    app.show_error = app.show_warning = app.show_info = lambda *a, **k: None
    A = mod.ListApp
    ergebnis = {"app_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(), "version": mod.APP_VERSION}
    try:
        arbeit = app.new_list_object("Arbeit")
        with app.sidebar_change() as change:
            app.lists.append(arbeit)
            change.mark()
        app.set_active_list(arbeit["id"])
        root.update()

        # A29: Ankertag gehört zur Regel; Eingabe über die echte Eingabezeile.
        app.entry.focus_set()
        app.clear_entry_placeholder()
        app.entry.delete(0, "end")
        app.entry.insert(0, "Miete monatlich am 15.")
        app.add_item()
        root.update()
        neu = app.items[-1]
        ergebnis["A29"] = {"titel": neu["text"], "faellig_tag": int(neu["due"][8:10]) if neu.get("due") else None,
                           "befund": "behoben" if neu["text"] == "Miete" and neu["due"].endswith("-15") else "vorhanden"}

        # A28: Ausgabe am Monatsende und Import einer RFC-Monatsreihe am 31.
        probe = app.new_item("Serie", due="2027-01-31", repeat={"art": A.REPEAT_MONTHLY, "start": "2027-01-31"})
        ausgabe = app.ics_repeat_rule(probe)
        datei = os.path.join(ordner, "serie.ics")
        Path(datei).write_text(kalender(["UID:m-31", "SUMMARY:RFC-Monatsreihe", "DTSTART;VALUE=DATE:20270131",
                                         "RRULE:FREQ=MONTHLY"]), encoding="utf-8")
        _kopf, ereignisse = app.read_ics_file(datei)
        punkte, _bericht = app.ics_events_to_items(ereignisse, None, "all", dry_run=True)
        import_regel = punkte[0].get("repeat")
        ergebnis["A28"] = {"ausgabe": ausgabe, "import": import_regel,
                           "befund": "behoben" if "BYSETPOS=-1" in ausgabe and import_regel is None else "vorhanden"}

        # A30: Windows-Zeitzonenname im Aufgabenimport.
        _tag, _zeit, hinweis = A.parse_ics_moment({"TZID": "W. Europe Standard Time"}, "20270115T090000")
        ergebnis["A30"] = {"hinweis": hinweis, "befund": "behoben" if hinweis is None else "vorhanden"}
    finally:
        try:
            app.cancel_pending_callbacks()
            app.release_data_lock()
        except Exception:
            pass
        root.destroy()

args.json.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v["befund"] for k, v in ergebnis.items() if isinstance(v, dict)}, ensure_ascii=False))
