"""Gleicher künstlicher Tagesbestand: Heute-Aufbau vor/nach U19.

Kalte erste Messung getrennt von fünf warmen Messungen, Median/p95 und
Rohwerte. Keine Aussage über Speichern oder andere Ansichten.
"""
import argparse
from datetime import date
import hashlib
import importlib.machinery
import importlib.util
import json
import math
import os
from pathlib import Path
import statistics
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]


def measure(path):
    with tempfile.TemporaryDirectory(prefix="glide-titelmessung-") as directory:
        os.environ["GLIDE_DATA_DIR"] = directory
        os.environ["GLIDE_TEST_MODE"] = "1"
        sys.path.insert(0, str(REPO / "src/glide"))
        loader = importlib.machinery.SourceFileLoader("glide_titelmessung", str(path))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = mod
        loader.exec_module(mod)
        root = mod.tk.Tk()
        root.geometry("1280x800+20+20")
        errors = []
        root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
        app = mod.ListApp(root)
        result = dict(version=mod.APP_VERSION, source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), measurements=[])
        try:
            root.update()
            for count in (1000, 10000):
                items = [app.new_item(f"Aufgabe {number:05d}", planned_date=date.today().isoformat()) for number in range(count)]
                entry = app.new_list_object("Messbestand", items)
                app.lists.append(entry)
                app.set_active_list(entry["id"], refresh=False)
                app.lists = [entry]
                app.clear_render_cache()
                app.set_today_view(refresh=False)
                times = []
                for n in range(6):
                    start = time.perf_counter()
                    app.refresh_tree()
                    root.update_idletasks()
                    times.append((time.perf_counter() - start) * 1000)
                    assert len(app.in_progress_item_sources) == count, (count, len(app.in_progress_item_sources), app.view_mode, app.plan_day())
                    print(f"{mod.APP_VERSION} {count}: Lauf {n + 1}: {times[-1]:.1f} ms", flush=True)
                warm = times[1:]
                result["measurements"].append(dict(items=count, cold_ms=times[0], warm_ms=warm,
                                                    median_ms=statistics.median(warm), p95_ms=sorted(warm)[math.ceil(len(warm) * .95) - 1]))
            assert not errors, errors
            result["callback_errors"] = errors
            return result
        finally:
            app.cancel_pending_callbacks()
            app.release_data_lock()
            root.destroy()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--app", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    result = measure(args.app)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
