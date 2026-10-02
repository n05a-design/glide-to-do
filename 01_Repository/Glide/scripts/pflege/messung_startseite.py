"""Unprofilierte Messung der Startseite (P03): Wechsel, Aktualisierung an Ort und Stelle, Widgetzahl.

--kacheln alt zeigt die zwölf Standardkacheln bis 3.33.1, --kacheln d12 die sieben nach D12.
--app erlaubt einen gesicherten Quellstand. --profil schreibt zusätzlich ein cProfile einer warmen
Aktualisierung (nur zur Ursachensuche; die Zeitwerte stammen aus den unprofilierten Runden).
Feste Inhalte, temporärer Datenordner, keine echten Nutzerdaten. Kein Latenzversprechen.
"""
import argparse
import cProfile
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import math
import os
import platform
import pstats
import statistics
import sys
import tempfile
import time
import traceback
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KACHELN = {
    "alt": ("clock", "welcome", "mascot", "today", "focus", "week", "recent", "templates",
            "boardpreview", "drawings", "pinned", "stats"),
    "d12": ("mascot", "today", "week", "recent", "boardpreview", "drawings", "pinned"),
}


def verteilung(werte):
    sortiert = sorted(werte)
    return {"median_ms": round(statistics.median(werte), 3),
            "p95_ms": round(sortiert[math.ceil(len(sortiert) * .95) - 1], 3),
            "stichproben_ms": [round(w, 3) for w in werte]}


def widgets(widget):
    anzahl, stapel = 0, [widget]
    while stapel:
        aktuell = stapel.pop()
        anzahl += 1
        stapel.extend(aktuell.winfo_children())
    return anzahl


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--items", type=int, default=1000)
    parser.add_argument("--rounds", type=int, default=8)
    parser.add_argument("--kacheln", choices=sorted(KACHELN), default="alt")
    parser.add_argument("--profil", action="store_true")
    args = parser.parse_args()
    if args.items < 1 or args.rounds < 2:
        parser.error("Mindestens ein Punkt und zwei warme Runden erforderlich")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(args.app.resolve().parent))
    with tempfile.TemporaryDirectory(prefix="glide-startseite-") as folder:
        os.environ["GLIDE_DATA_DIR"] = folder
        os.environ["GLIDE_TEST_MODE"] = "1"
        loader = importlib.machinery.SourceFileLoader("glide_startseite", str(args.app))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        loader.exec_module(mod)
        root = mod.tk.Tk()
        root.geometry("1400x950+20+20")
        errors = []

        def callback_error(*exc):
            errors.append(str(exc[1]))
            traceback.print_exception(*exc)
        root.report_callback_exception = callback_error
        app = mod.ListApp(root)

        def idle():
            for _ in range(3):
                root.update_idletasks()
                root.update()

        try:
            # Feste Inhalte: Jeder dritte Punkt hat einen Bearbeitungstag, jeder fünfte eine
            # Fälligkeit zwischen drei Tagen vorher und zehn Tagen nachher; jeder siebte ist erledigt.
            heute = date.today()
            inbox = app.ensure_inbox_list()
            inbox["items"] = []
            app.lists = [inbox]
            app.folders = []
            for number in range(12):
                items = []
                for i in range(number, args.items, 12):
                    item = app.new_item(f"Aufgabe {i:05d} mit Beschreibung", item_id=f"start-{i}",
                                        description="Prüftext " * 8)
                    if i % 3 == 0:
                        item["planned_date"] = (heute + timedelta(days=i % 7 - 1)).isoformat()
                    if i % 5 == 0:
                        item["due"] = (heute + timedelta(days=i % 14 - 3)).isoformat()
                    item["done"] = i % 7 == 0
                    items.append(item)
                app.lists.append(app.new_list_object(f"Messliste {number:02d}", items,
                                                     list_id=f"start-list-{number}",
                                                     created_at="2026-09-30T08:00:00"))
            for number in range(3):
                app.lists.append(app.new_list_object(
                    f"Skizze {number}", [], list_kind=app.LIST_KIND_DRAWING, list_id=f"start-drawing-{number}",
                    drawing=mod.glide_drawing.DrawingModel.blank(32).to_document(),
                    created_at="2026-09-30T08:00:00"))
            seite = app.new_page_from_markdown("# Projektseite\n\n" + "Absatz. " * 40, title="Projektseite")
            app.settings["pinned_pages"] = [{"kind": "list", "id": seite["id"]},
                                            {"kind": "list", "id": "start-list-0"}]
            sichtbar = KACHELN[args.kacheln]
            app.settings["home_tile_order"] = list(app.HOME_TILE_KEYS)
            app.settings["home_tiles_hidden"] = [key for key in app.HOME_TILE_KEYS if key not in sichtbar]
            app.settings["show_home_stats"] = "stats" in sichtbar
            app.save_items()
            app.update_sidebar_list()
            idle()
            liste = app.lists[1]

            def wechsel():
                app.set_active_list(liste["id"])
                idle()
                start = time.perf_counter()
                app.set_home_view()
                idle()
                return (time.perf_counter() - start) * 1000

            def aktualisierung():
                start = time.perf_counter()
                app._refresh_home()
                idle()
                return (time.perf_counter() - start) * 1000

            wechsel_werte = [wechsel() for _ in range(args.rounds + 1)]
            aktual_werte = [aktualisierung() for _ in range(args.rounds + 1)]
            anzahl_widgets = widgets(app.home_content)
            profil_text = None
            if args.profil:
                profiler = cProfile.Profile()
                profiler.enable()
                app._refresh_home()
                idle()
                profiler.disable()
                puffer = io.StringIO()
                pstats.Stats(profiler, stream=puffer).sort_stats("cumulative").print_stats(30)
                profil_text = puffer.getvalue()
            assert not errors, errors
            sichtbare = [key for key in app.home_tile_order() if app.home_tile_visible(key)]
            result = {"version": mod.APP_VERSION, "source_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(),
                      "python": platform.python_version(), "platform": platform.platform(),
                      "tk": root.tk.call("info", "patchlevel"), "profiling": False,
                      "fixture": {"tasks": args.items, "lists": 12, "drawings": 3, "pinned": 2,
                                  "window": "1400x950", "idle_rounds": 3, "kacheln": args.kacheln,
                                  "sichtbare_kacheln": sichtbare},
                      "warm_rounds": args.rounds,
                      "wechsel": dict(verteilung(wechsel_werte[1:]), first_ms=round(wechsel_werte[0], 3)),
                      "aktualisierung": dict(verteilung(aktual_werte[1:]), first_ms=round(aktual_werte[0], 3)),
                      "widgets_startseite": anzahl_widgets, "callback_errors": errors}
            args.json.parent.mkdir(parents=True, exist_ok=True)
            args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            if profil_text:
                args.json.with_suffix(".profil.txt").write_text(profil_text, encoding="utf-8")
            print(f"{args.kacheln} ({len(sichtbare)} Kacheln, {args.items} Punkte): Wechsel Median "
                  f"{result['wechsel']['median_ms']} ms, Aktualisierung Median {result['aktualisierung']['median_ms']} ms, "
                  f"{anzahl_widgets} Widgets, Callbackfehler {len(errors)}")
        finally:
            root.destroy()


if __name__ == "__main__":
    main()
