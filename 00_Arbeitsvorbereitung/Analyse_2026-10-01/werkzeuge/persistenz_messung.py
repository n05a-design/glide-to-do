"""Messung des Speicherpfads bei wachsendem Bestand (Befund T1/T2, 01.10.2026).

Misst je Bestandsgröße: erstes Speichern einer Sitzung (mit den neun
Schema-Sicherungsprüfungen), `snapshot_undo`, `save_items`, JSON-Kodierung mit
und ohne Einrückung, `history_snapshot` und einen kompletten Abhak-Vorgang
über `item_change`. Optional mit cProfile-Aufschlüsselung.

Aufruf (je Bestandsgröße ein eigener Prozess mit frischem Datenordner):
    xvfb-run -a -s "-screen 0 1280x860x24" python3 persistenz_messung.py --punkte 1000
    xvfb-run -a -s "-screen 0 1280x860x24" python3 persistenz_messung.py --punkte 10000 --profil

Künstliche Daten (Listen à 200 Punkte, zufällige Beschreibung/Fälligkeit, fester
Zufallskeim). Werte gelten nur für Gerät, Python und Tk der Messung; für
Vergleiche dieselbe Umgebung verwenden. Median aus 7 (Abhaken: 5) warmen Läufen.
"""

import argparse
import cProfile
import io
import json
import os
import pstats
import random
import statistics
import time

import _glide_laden as gl

PROFIL_FILTER = ("save_items|write_json_atomic|update_history|history_snapshot|history_events|"
                 "record_recent_list_edits|list_edit_signatures|update_sidebar_list|"
                 "refresh_reminder_status|refresh_tree|snapshot_undo|write_backup_copy|fsync")


def bestand_anlegen(app, punkte, je_liste=200):
    random.seed(1)
    vorlage = json.loads(json.dumps(app.lists[0]))
    for nummer in range(max(1, punkte // je_liste)):
        if nummer == 0:
            liste = app.lists[0]
        else:
            liste = json.loads(json.dumps(vorlage))
            liste.update({"id": f"messliste{nummer}", "title": f"Liste {nummer}", "items": []})
            app.lists.append(liste)
        for i in range(je_liste):
            liste["items"].append(app.new_item(
                f"Aufgabe {nummer}-{i} mit etwas Text", importance=random.randint(0, 3),
                description="Beschreibung " * random.randint(0, 20),
                due="2026-10-%02d" % random.randint(1, 28) if i % 3 == 0 else None))


def zeit(funktion, wiederholungen=7):
    werte = []
    for _ in range(wiederholungen):
        start = time.perf_counter()
        funktion()
        werte.append((time.perf_counter() - start) * 1000)
    werte.sort()
    return {"median_ms": round(statistics.median(werte), 1), "max_ms": round(werte[-1], 1)}


def messen(modul, punkte, profil):
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1280x840")
    app = modul.ListApp(root)
    root.update()
    bestand_anlegen(app, punkte)
    app.save_items()
    # Zustand „erstes Speichern der Sitzung“ nachstellen
    for version in range(12, 21):
        setattr(app, f"_schema{version}_backup_checked", False)
    datei = os.path.join(os.environ["GLIDE_DATA_DIR"], "liste_speicher.json")
    ergebnis = {"punkte": punkte, "datei_kb": os.path.getsize(datei) // 1024, "umgebung": gl.umgebung(root)}
    start = time.perf_counter()
    app.save_items()
    ergebnis["erstes_speichern_ms"] = round((time.perf_counter() - start) * 1000, 1)
    ergebnis["snapshot_undo"] = zeit(lambda: (app.snapshot_undo(), app.undo_stack.pop()))
    ergebnis["save_items"] = zeit(app.save_items)
    ergebnis["json_dumps_indent4"] = zeit(lambda: json.dumps(app.data_payload(), ensure_ascii=False, indent=4))
    ergebnis["json_dumps_kompakt"] = zeit(lambda: json.dumps(app.data_payload(), ensure_ascii=False,
                                                             separators=(",", ":")))
    ergebnis["history_snapshot"] = zeit(app.history_snapshot)
    punkt = app.lists[0]["items"][0]

    def abhaken():
        with app.item_change([punkt["id"]]) as aenderung:
            punkt["done"] = not punkt["done"]
            aenderung.mark()

    ergebnis["abhaken_item_change"] = zeit(abhaken, 5)
    if profil:
        profiler = cProfile.Profile()
        profiler.enable()
        for _ in range(3):
            abhaken()
        profiler.disable()
        text = io.StringIO()
        pstats.Stats(profiler, stream=text).sort_stats("cumulative").print_stats(PROFIL_FILTER)
        ergebnis["profil_3x_abhaken"] = text.getvalue()
    root.destroy()
    return ergebnis


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", default=None)
    parser.add_argument("--punkte", type=int, default=1000)
    parser.add_argument("--profil", action="store_true")
    args = parser.parse_args()
    gl.isolieren("glide-persistenz-")
    modul = gl.glide_laden(args.code)
    print(json.dumps(messen(modul, args.punkte, args.profil), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
