"""Identische Startseitenmessung vor/nach WA-39; ausschließlich künstliche Daten."""
import argparse
import ast
import copy
from contextlib import ExitStack
from datetime import date, timedelta
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import tempfile
from time import perf_counter
from types import MethodType
from unittest.mock import patch


def timings(action, repeats=7):
    started = perf_counter()
    action()
    cold = (perf_counter() - started) * 1000
    values = []
    for _ in range(repeats):
        started = perf_counter()
        action()
        values.append((perf_counter() - started) * 1000)
    return {"cold_ms": cold, "raw_ms": values, "median_ms": statistics.median(values),
            "p95_ms": sorted(values)[-1]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reference-ref", help="Lokaler Gitstand für gepaarte Messung derselben Fixture")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[3]
    source = repo / "src/glide/app.pyw"
    result = {"app_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "runtime_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                 for path in sorted(source.parent.glob("*.py*")) if path.is_file()},
              "python": platform.python_version(), "samples": {}, "errors": []}
    with tempfile.TemporaryDirectory(prefix="glide-home-model-") as directory:
        os.environ["GLIDE_DATA_DIR"] = directory
        os.environ["GLIDE_TEST_MODE"] = "1"
        loader = importlib.machinery.SourceFileLoader("glide_home_probe", str(source))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        loader.exec_module(mod)
        previous = {}
        if args.reference_ref:
            relative = "01_Repository/Glide/src/glide/app.pyw"
            old_source = subprocess.check_output(["git", "show", f"{args.reference_ref}:{relative}"], cwd=repo)
            old_tree = ast.parse(old_source.decode("utf-8-sig"))
            old_class = next(node for node in old_tree.body if isinstance(node, ast.ClassDef) and node.name == "ListApp")
            names = {"home_summary", "home_focus_candidate", "home_week_overview", "home_label_overview",
                     "next_scheduled_item", "_refresh_home"}
            functions = ast.Module(body=[node for node in old_class.body
                                        if isinstance(node, ast.FunctionDef) and node.name in names], type_ignores=[])
            namespace = dict(vars(mod))
            exec(compile(functions, f"git:{args.reference_ref}", "exec"), namespace)
            previous = {name: namespace[name] for name in names}
            result["reference_ref"] = args.reference_ref
            result["reference_app_sha256"] = hashlib.sha256(old_source).hexdigest()
        root = mod.tk.Tk()
        root.report_callback_exception = lambda *exc: result["errors"].append(str(exc[1]))
        app = mod.ListApp(root)
        result["tk"] = root.tk.call("info", "patchlevel")

        def idle():
            root.update_idletasks()
            root.update()

        try:
            app.settings["animations_enabled"] = False
            app.settings["release_notes_seen"] = mod.APP_VERSION
            app.settings["home_tile_order"] = list(mod.glide_home.KEYS)
            visible = {"today", "week", "focus", "labels", "recent", "clock"}
            app.settings["home_tiles_hidden"] = [k for k in mod.glide_home.KEYS if k not in visible]
            app.set_home_view()
            root.geometry("1280x860+30+30")
            idle()
            prototype = copy.deepcopy(app.lists[0])
            today = date.today()
            for size in (100, 1000, 5000, 10000):
                lists = []
                for n in range(10):
                    entry = copy.deepcopy(prototype)
                    entry.update(id=f"bench-list-{n}", name=f"Messliste {n}", items=[])
                    lists.append(entry)
                for i in range(size):
                    due = (today + timedelta(days=i % 12 - 2)).isoformat()
                    lists[i % 10]["items"].append(app.new_item(
                        f"Aufgabe {i:05d}", item_id=f"bench-{i}", due=due,
                        planned_date=today.isoformat() if i % 3 == 0 else None,
                        done=i % 7 == 0, labels=[], importance=i % 4))
                app.lists = lists
                app.items = lists[0]["items"]
                app.active_list_id = lists[0]["id"]
                app._data_revision += 1
                app.clear_render_cache()

                def helpers():
                    app.home_summary()
                    app.home_focus_candidate()
                    app.home_week_overview()
                    app.home_label_overview()
                    app.next_scheduled_item()

                def render():
                    app._home_signature = None
                    app._refresh_home()
                    idle()

                result["samples"][str(size)] = {"helpers_fresh": timings(helpers),
                    "home_refresh_and_idle": timings(render),
                    "geometry": [root.winfo_width(), root.winfo_height()]}
                if previous:
                    paired = {"reference_helpers": [], "current_helpers": [],
                              "reference_refresh": [], "current_refresh": []}
                    # Alten und neuen echten Weg im Wechsel an denselben Objekten messen.
                    # Patching liegt außerhalb der Messzeit; kein zweiter Appzustand.
                    for repetition in range(9):
                        variants = ("reference", "current") if repetition % 2 == 0 else ("current", "reference")
                        for variant in variants:
                            with ExitStack() as patches:
                                if variant == "reference":
                                    for name, function in previous.items():
                                        patches.enter_context(patch.object(app, name, MethodType(function, app)))
                                for name, action in (("helpers", helpers), ("refresh", render)):
                                    start = perf_counter()
                                    action()
                                    elapsed = (perf_counter() - start) * 1000
                                    if repetition:
                                        paired[f"{variant}_{name}"].append(elapsed)
                    result["samples"][str(size)]["paired"] = {
                        name: {"raw_ms": values, "median_ms": statistics.median(values),
                               "p95_ms": sorted(values)[-1]} for name, values in paired.items()}
            assert not result["errors"], result["errors"]
        finally:
            root.destroy()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"app": result["app_sha256"], "samples": {
        k: {"refresh_median_ms": v["home_refresh_and_idle"]["median_ms"]}
        for k, v in result["samples"].items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
