"""Unprofilierter Vorher/Nachher-Vergleich mit identischen, isolierten Inhalten.

--app erlaubt einen gesicherten Quellstand; --items auch 1000 oder 10000 Punkte.
Erster Wechsel, warme Stichproben, Median und p95 werden getrennt ausgewiesen.
Kein Latenzversprechen: lokale Messung inklusive drei Tk-Zeichendurchläufen.
"""
import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import math
import os
import platform
import statistics
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def verteilung(werte):
    sortiert = sorted(werte)
    return {"median_ms": round(statistics.median(werte), 3),
            "p95_ms": round(sortiert[math.ceil(len(sortiert) * .95) - 1], 3),
            "stichproben_ms": [round(w, 3) for w in werte]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--items", type=int, default=100)
    parser.add_argument("--rounds", type=int, default=8)
    args = parser.parse_args()
    if args.items < 1 or args.rounds < 2:
        parser.error("Mindestens ein Punkt und zwei warme Runden erforderlich")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(args.app.resolve().parent))
    with tempfile.TemporaryDirectory(prefix="glide-messung-") as folder:
        os.environ["GLIDE_DATA_DIR"] = folder
        os.environ["GLIDE_TEST_MODE"] = "1"
        loader = importlib.machinery.SourceFileLoader("glide_messung", str(args.app))
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
            # Keine Zufallsdaten: Titel, Kennungen, Aufteilung und Text sind fest.
            inbox = app.ensure_inbox_list()
            inbox["items"] = []
            app.lists = [inbox]
            app.folders = []
            for number in range(12):
                items = [app.new_item(f"Aufgabe {i:05d} mit Beschreibung", item_id=f"perf-{i}",
                         description="Prüftext " * 8) for i in range(number, args.items, 12)]
                app.lists.append(app.new_list_object(f"Messliste {number:02d}", items,
                    list_id=f"perf-list-{number}", created_at="2026-09-30T08:00:00"))
            task_list = app.lists[1]
            text = "# Messseite\n\n" + "\n\n".join(f"Absatz {i}: " + "Text " * 30 for i in range(50))
            page = app.new_page_from_markdown(text, title="Messseite")
            note = app.new_list_object("Messnotiz", [], list_kind="note", list_id="perf-note",
                rich_note={"text": "Notiztext\n" + "Notizen " * 300, "spans": [], "links": {}},
                created_at="2026-09-30T08:00:00")
            app.lists.append(note)
            png = Path(folder, "messbild.png")
            photo = mod.tk.PhotoImage(master=root, width=160, height=100)
            photo.put("#3366CC", to=(0, 0, 160, 100))
            photo.write(str(png), format="png")
            app.rich_note_editor.insert_images([str(png)], "3.0")
            app.rich_note_editor.insert_images([str(png)], "15.0")
            app.save_items()
            app.update_sidebar_list()
            idle()

            def listing():
                app.set_active_list(task_list["id"])
            def table():
                listing()
                app.set_table_view()
            views = [("Startseite", app.set_home_view), ("Bibliothek", app.set_library_view),
                     ("Liste", listing), ("Tabelle", table),
                     ("Seite mit zwei Bildern", lambda: app.set_active_list(page["id"])),
                     ("Notiz", lambda: app.set_active_list(note["id"]))]
            timings = {name: [] for name, _ in views}
            for _ in range(args.rounds + 1):
                for name, action in views:
                    start = time.perf_counter()
                    action()
                    idle()
                    timings[name].append((time.perf_counter() - start) * 1000)

            fonts = []
            flows = []
            for _ in range(args.rounds):
                start = time.perf_counter()
                for i in range(3000):
                    mod.app_font(8 + i % 6, "bold" if i % 2 else "normal")
                fonts.append((time.perf_counter() - start) * 1000)
                start = time.perf_counter()
                flow = mod.ButtonFlow(root, bg=app.theme["card"])
                flow.pack(fill="x")
                for i in range(30):
                    flow.add(mod.tk.Button(flow, text=f"Aktion {i}", width=12))
                idle()
                flows.append((time.perf_counter() - start) * 1000)
                flow.destroy()
                idle()
            assert not errors, errors
            result = {"version": mod.APP_VERSION, "source_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(),
                      "python": platform.python_version(), "platform": platform.platform(),
                      "tk": root.tk.call("info", "patchlevel"), "profiling": False,
                      "fixture": {"tasks": args.items, "lists": 12, "page_paragraphs": 50,
                                  "page_images": 2, "notes": 1, "window": "1400x950", "idle_rounds": 3},
                      "warm_rounds": args.rounds,
                      "views": {name: dict(verteilung(values[1:]), first_ms=round(values[0], 3))
                                for name, values in timings.items()},
                      "font_3000_calls": verteilung(fonts), "toolbar_30_buttons": verteilung(flows),
                      "callback_errors": errors}
            args.json.parent.mkdir(parents=True, exist_ok=True)
            args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            for name, values in result["views"].items():
                print(f"{name}: Median {values['median_ms']} ms, p95 {values['p95_ms']} ms")
            print("Schrift:", result["font_3000_calls"]["median_ms"], "ms; Formatleiste:",
                  result["toolbar_30_buttons"]["median_ms"], "ms; Callbackfehler:", len(errors))
        finally:
            root.destroy()


if __name__ == "__main__":
    main()
