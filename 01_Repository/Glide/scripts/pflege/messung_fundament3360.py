"""P03/E01: tatsächlicher Startseiten-Neuaufbau und Einstellungen, isoliert.

Unprofilierte Erst-/Folgeserien mit identischen künstlichen Daten. --profil
schreibt ausschließlich zur Ursachensuche eine zusätzliche getrennte Reihe.
Die bestehende Startseitensignatur wird vor jeder Messung ungültig gemacht;
Cachetreffer sind damit ausdrücklich nicht der gemessene Neuaufbau.
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
from pathlib import Path
import platform
import pstats
import statistics
import sys
import tempfile
import time


def distribution(samples):
    return {"first_ms": round(samples[0], 3),
            "median_ms": round(statistics.median(samples[1:]), 3),
            "p95_ms": round(sorted(samples[1:])[math.ceil((len(samples) - 1) * .95) - 1], 3),
            "samples_ms": [round(value, 3) for value in samples]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--items", type=int, default=1000)
    parser.add_argument("--rounds", type=int, default=8)
    parser.add_argument("--profil", action="store_true")
    parser.add_argument("--lebensdauer", action="store_true",
                        help="Zusätzlich fünf Serien je 20 UI-Abgleiche und Dialogöffnungen beobachten")
    args = parser.parse_args()
    if args.items < 1 or args.rounds < 2:
        parser.error("Mindestens ein Punkt und zwei Folgerunden erforderlich")
    sys.path.insert(0, str(args.app.resolve().parent))
    with tempfile.TemporaryDirectory(prefix="glide-fundament-messung-") as data:
        os.environ["GLIDE_DATA_DIR"] = data
        os.environ["GLIDE_TEST_MODE"] = "1"
        loader = importlib.machinery.SourceFileLoader("glide_fundament_messung", str(args.app))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = mod
        loader.exec_module(mod)
        root = mod.tk.Tk()
        root.geometry("1280x800+20+20")
        errors = []
        root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
        app = mod.ListApp(root)
        app.show_info = app.show_warning = app.show_error = lambda *a, **k: None

        def settle():
            for _ in range(3):
                root.update_idletasks()
                root.update()

        try:
            inbox = app.ensure_inbox_list()
            inbox["items"] = []
            app.lists = [inbox]
            for number in range(12):
                items = [app.new_item(f"Aufgabe {i:05d}", item_id=f"fundament-{i}",
                         due=(mod.date.today() + mod.timedelta(days=i % 7)).isoformat())
                         for i in range(number, args.items, 12)]
                for item in items:
                    item["planned_date"] = mod.date.today().isoformat()
                app.lists.append(app.new_list_object(f"Messliste {number:02d}", items,
                                 list_id=f"fundament-list-{number}"))
            app.save_items()
            app.set_active_list(app.lists[1]["id"])
            settle()
            timings = {"startseite_neuaufbau": [], "einstellungen": []}
            counts = {}

            def home():
                app._home_signature = None
                app.set_home_view()
                settle()

            pending_dialog = [None]
            original_modal = app.run_modal
            original_wait_window = root.wait_window
            original_wait_variable = root.wait_variable
            # Den echten Modalweg einschließlich Mindestbreite, Mapping,
            # Fokus und Griff messen. Nur die Benutzerwartezeit entfällt.
            root.wait_window = lambda *a, **k: None
            root.wait_variable = lambda *a, **k: None
            def modal(dialog, *a, **k):
                original_modal(dialog, *a, **k)
                settle()
                counts["einstellungen"] = len(tuple(app.iter_descendants(dialog)))
                pending_dialog[0] = dialog
            app.run_modal = modal
            for key, action in (("startseite_neuaufbau", home), ("einstellungen", app.show_settings_dialog)):
                for _ in range(args.rounds + 1):
                    start = time.perf_counter()
                    action()
                    timings[key].append((time.perf_counter() - start) * 1000)
                    if pending_dialog[0] is not None:
                        dialog, pending_dialog[0] = pending_dialog[0], None
                        getattr(dialog, "glide_close", dialog.destroy)()
                        settle()
                settle()
            counts["startseite"] = len(tuple(app.iter_descendants(app.home_content)))
            lifetime = {}
            if args.lebensdauer:
                import gc
                import tracemalloc
                # UI-Lebensdauer getrennt vom gewollt wachsenden Undo-Verlauf:
                # erzwungener Builder, sichtbare Titeländerung und echter Modalweg.
                def library():
                    entry = app.lists[1]
                    entry["title"] = ("Messliste aktuell" if entry["title"] != "Messliste aktuell"
                                      else "Messliste geändert")
                    app.refresh_library_page()
                    settle()
                def settings():
                    app.show_settings_dialog()
                    dialog, pending_dialog[0] = pending_dialog[0], None
                    getattr(dialog, "glide_close", dialog.destroy)()
                    settle()
                def state(host):
                    gc.collect()
                    widgets = tuple(app.iter_descendants(host))
                    return {"python_bytes": tracemalloc.get_traced_memory()[0],
                            "widgets": len(widgets),
                            "tcl_callbacks": sum(len(getattr(w, "_tclCommands", ()) or ()) for w in widgets),
                            "pending_after": len(root.tk.splitlist(root.tk.call("after", "info")))}
                tracemalloc.start()
                for name, prepare, action, host in (
                    ("startseite", app.set_home_view, home, lambda: app.home_content),
                    ("bibliothek", app.set_library_view, library, lambda: app.home_content),
                    ("einstellungen", lambda: None, settings,
                     lambda: pending_dialog[0] or app._settings_dialog_cache[1]),
                ):
                    prepare()
                    settle()
                    for _ in range(5):
                        action()
                    samples = [state(host())]
                    for _ in range(5):
                        for _ in range(20):
                            action()
                        samples.append(state(host()))
                    lifetime[name] = {"warmup": 5, "series": 5, "rounds_per_series": 20,
                                      "samples": samples}
                tracemalloc.stop()
            profiles = {}
            if args.profil:
                for key, action in (("startseite_neuaufbau", home), ("einstellungen", app.show_settings_dialog)):
                    profiler = cProfile.Profile()
                    profiler.runcall(action)
                    output = io.StringIO()
                    pstats.Stats(profiler, stream=output).sort_stats("cumulative").print_stats(35)
                    profiles[key] = output.getvalue()
            app.run_modal = original_modal
            root.wait_window = original_wait_window
            root.wait_variable = original_wait_variable
            assert not errors, errors
            result = {"version": mod.APP_VERSION, "source_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(),
                      "python": platform.python_version(), "platform": platform.platform(),
                      "tk": root.tk.call("info", "patchlevel"), "profiling": False,
                      "fixture": {"tasks": args.items, "task_lists": 12, "window": "1280x800",
                                  "idle_rounds": 3, "forced_home_rebuild": True,
                                  "settings_close_excluded": True,
                                  "actual_modal_setup": True, "user_wait_excluded": True},
                      "warm_rounds": args.rounds,
                      "timings": {key: distribution(values) for key, values in timings.items()},
                      "widget_counts": counts, "callback_errors": errors}
            if lifetime:
                result["ui_lifetime"] = lifetime
            args.json.parent.mkdir(parents=True, exist_ok=True)
            args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            if profiles:
                args.json.with_suffix(".profil.txt").write_text(json.dumps(profiles, ensure_ascii=False, indent=2))
            print(json.dumps({"timings": result["timings"], "widget_counts": counts}, ensure_ascii=False))
        finally:
            app.cancel_pending_callbacks()
            app.release_data_lock()
            root.destroy()


if __name__ == "__main__":
    main()
