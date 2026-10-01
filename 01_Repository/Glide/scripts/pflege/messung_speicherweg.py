"""Unprofilierter Vergleich des Speicherwegs bei wachsendem Bestand (P08, T2).

Misst je Bestandsgröße das erste Speichern einer Sitzung (mit den
Schema-Sicherungsprüfungen), `snapshot_undo`, `save_items`, `history_snapshot`,
JSON mit und ohne Einrückung und einen vollständigen Abhak-Vorgang über
`item_change`. --app erlaubt einen gesicherten Quellstand für Vorher/Nachher.
--profil schlüsselt drei Abhak-Vorgänge zusätzlich mit cProfile auf.

Künstliche Daten mit festem Zufallskeim (200 Punkte je Liste, Beschreibung und
Fälligkeit wechselnd), isolierter GLIDE_DATA_DIR. Kein Latenzversprechen: Werte
gelten für Gerät, Python und Tk der Messung; Vergleiche nur in gleicher
Umgebung. Je Größe ein eigener Prozess.

    python3 -B scripts/pflege/messung_speicherweg.py --items 1000 --json <Ausgabe>
    python3 -B scripts/pflege/messung_speicherweg.py --items 10000 --profil --json <Ausgabe>
"""
import argparse
import cProfile
import importlib.machinery
import importlib.util
import io
import json
import math
import os
import platform
import pstats
import random
import statistics
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROFIL_FILTER = ("save_items|write_json_atomic|update_history|history_snapshot|history_events|"
                 "record_recent_list_edits|list_edit_signatures|update_sidebar_list|"
                 "refresh_reminder_status|refresh_tree|snapshot_undo|write_backup_copy|fsync")


def verteilung(werte):
    sortiert = sorted(werte)
    return {"median_ms": round(statistics.median(werte), 3),
            "p95_ms": round(sortiert[math.ceil(len(sortiert) * .95) - 1], 3),
            "stichproben_ms": [round(w, 3) for w in werte]}


def messen(funktion, runden):
    funktion()  # Aufwärmen, nicht gewertet
    werte = []
    for _ in range(runden):
        start = time.perf_counter()
        funktion()
        werte.append((time.perf_counter() - start) * 1000)
    return verteilung(werte)


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


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--items", type=int, default=1000)
    parser.add_argument("--rounds", type=int, default=9)
    parser.add_argument("--profil", action="store_true")
    args = parser.parse_args()
    if args.items < 1 or args.rounds < 2:
        parser.error("Mindestens ein Punkt und zwei warme Runden erforderlich")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(args.app.resolve().parent))
    with tempfile.TemporaryDirectory(prefix="glide-speicherweg-") as folder:
        os.environ["GLIDE_DATA_DIR"] = folder
        os.environ["GLIDE_TEST_MODE"] = "1"
        loader = importlib.machinery.SourceFileLoader("glide_messung", str(args.app))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        loader.exec_module(mod)
        root = mod.tk.Tk()
        root.geometry("1280x840+20+20")
        errors = []

        def callback_error(*exc):
            errors.append(str(exc[1]))
            traceback.print_exception(*exc)

        root.report_callback_exception = callback_error
        app = mod.ListApp(root)
        root.update()
        bestand_anlegen(app, args.items)
        app.save_items()
        datei = Path(folder) / "liste_speicher.json"
        # Zustand „erstes Speichern der Sitzung“: Schema-Sicherungsprüfungen erneut scharf
        for name in [n for n in dir(app) if n.startswith("_schema") and n.endswith("_backup_checked")]:
            setattr(app, name, False)
        start = time.perf_counter()
        app.save_items()
        erstes = (time.perf_counter() - start) * 1000
        punkt = app.lists[0]["items"][0]

        def abhaken():
            with app.item_change([punkt["id"]]) as aenderung:
                punkt["done"] = not punkt["done"]
                aenderung.mark()

        ergebnis = {
            "werkzeug": "messung_speicherweg.py",
            "app": os.path.relpath(args.app.resolve(), REPO.parent.parent),
            "app_version": mod.APP_VERSION,
            "punkte": args.items,
            "datei_kb": datei.stat().st_size // 1024,
            "runden_warm": args.rounds,
            "umgebung": {"python": platform.python_version(), "tk": root.tk.call("info", "patchlevel"),
                         "plattform": platform.platform(), "prozessor": platform.processor() or platform.machine()},
            "erstes_speichern_ms": round(erstes, 3),
            "snapshot_undo": messen(lambda: (app.snapshot_undo(), app.undo_stack.pop()), args.rounds),
            "save_items": messen(app.save_items, args.rounds),
            "history_snapshot": messen(app.history_snapshot, args.rounds),
            "json_eingerueckt": messen(lambda: json.dumps(app.data_payload(), ensure_ascii=False, indent=4),
                                       args.rounds),
            "json_kompakt": messen(lambda: json.dumps(app.data_payload(), ensure_ascii=False,
                                                      separators=(",", ":")), args.rounds),
            "abhaken_item_change": messen(abhaken, args.rounds),
        }
        if args.profil:
            profiler = cProfile.Profile()
            profiler.enable()
            for _ in range(3):
                abhaken()
            profiler.disable()
            text = io.StringIO()
            pstats.Stats(profiler, stream=text).sort_stats("cumulative").print_stats(PROFIL_FILTER)
            ergebnis["profil_3x_abhaken"] = text.getvalue().replace(str(REPO.parent.parent) + os.sep, "")
        ergebnis["callbackfehler"] = errors
        root.destroy()
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for name in ("snapshot_undo", "save_items", "history_snapshot", "abhaken_item_change"):
        print(f"{name}: Median {ergebnis[name]['median_ms']} ms, p95 {ergebnis[name]['p95_ms']} ms")
    print(f"erstes Speichern: {ergebnis['erstes_speichern_ms']} ms · Datei {ergebnis['datei_kb']} KB")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
