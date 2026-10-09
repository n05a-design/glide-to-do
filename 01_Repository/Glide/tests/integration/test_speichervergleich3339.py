"""P08a: gemeinsamer Speichervergleich, Undo/Reload und Fehler/Retry.

--app erlaubt die rote Gegenprobe; --baseline-ref vergleicht zusätzlich alle
Verlaufssnapshots/-ereignisse mit dem unveränderten App-Code aus Git.
"""
import argparse
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--baseline-ref")
args = parser.parse_args()
sys.path.insert(0, str(REPO / "src/glide"))


def load(path, name):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader))
    sys.modules[name] = mod
    loader.exec_module(mod)
    return mod


def legacy_json_items(app):
    return {item["id"]: json.dumps(item, sort_keys=True, ensure_ascii=False)
            for entry in app.lists for item in app.walk_items(entry.get("items", []))
            if app.is_schedulable_item(item)}


with tempfile.TemporaryDirectory(prefix="glide-speichervergleich-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    mod = load(args.app, "glide_save_comparison_test")
    legacy = None
    if args.baseline_ref:
        source = subprocess.check_output([
            "git", "show", f"{args.baseline_ref}:01_Repository/Glide/src/glide/app.pyw"], cwd=REPO)
        old_source = Path(folder) / "baseline.pyw"
        old_source.write_bytes(source)
        old_mod = load(old_source, "glide_save_comparison_baseline")
        legacy = object.__new__(old_mod.ListApp)
    errors = []
    root = mod.tk.Tk()
    root.geometry("860x700")
    root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **kw: errors.append(repr(a))
    try:
        root.update()
        first = app.new_list_object("Vergleich")
        second = app.new_list_object("Ziel")
        parent = app.new_item("Eltern", kind=app.ITEM_KIND_LONG)
        child = app.new_item("Kind", due="2090-12-10")
        parent["children"] = [child]
        group = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP)
        first["items"] = [parent, group]
        app.lists.extend([first, second])
        app.set_active_list(first["id"])
        assert hasattr(app, "list_comparison"), "P08a: gemeinsamer Vergleich fehlt"
        with patch.object(app, "list_comparison", wraps=app.list_comparison) as builder:
            assert app.save_items()
        assert builder.call_count == 1, f"{builder.call_count} Vergleichsdurchläufe statt einem"

        # Vollständige Ergebnisgleichheit mit dem alten Verlauf, einschließlich
        # Metadaten, Strukturaktionen, Labels, Papierkorb und Zeichnungsmodell.
        differential = 0
        if legacy is not None:
            randomizer = random.Random(3339)
            for number in range(120):
                for name in ("lists", "folders", "labels", "trash"):
                    setattr(legacy, name, copy.deepcopy(getattr(app, name)))
                before = legacy.history_snapshot()
                assert before == app.history_snapshot(), number
                target = first["items"][0]
                field = randomizer.choice(list(app.HISTORY_ITEM_FIELDS) + ["collapsed", "done_at"])
                values = {
                    "text": f"Änderung {number}", "done": not target.get("done"),
                    "importance": number % 4, "due": "2090-12-12", "due_time": "12:00",
                    "repeat": {"art": "taeglich"}, "reminder": {"mode": "relative", "minutes": 15},
                    "planned_date": "2090-12-11", "estimated_minutes": 30,
                    "kind": app.ITEM_KIND_LONG, "color": "#123456", "labels": ["l2", "l1"],
                    "description": f"Beschreibung {number}", "attachments": [{"name": str(number)}],
                    "checklist": [{"text": str(number), "done": False}], "links": [child["id"]],
                    "blocked_by": [], "planned_time": "11:00", "time_spent_minutes": number,
                    "collapsed": number % 2 == 0, "done_at": None,
                }
                target[field] = values[field]
                first["title"] = f"Vergleich {number}"
                first["folder_id"] = str(number % 3)
                first["rich_note"] = {"text": str(number), "spans": []}
                app.folders = [{"id": "f", "title": str(number), "parent_id": None}]
                app.labels = [{"id": str(number), "name": f"Label {number}"}]
                app.trash = [{"kind": app.TRASH_KIND_ITEM, "item": app.new_item(f"Gelöscht {number}")}]
                for name in ("lists", "folders", "labels", "trash"):
                    setattr(legacy, name, copy.deepcopy(getattr(app, name)))
                after = legacy.history_snapshot()
                assert after == app.history_snapshot(), number
                assert legacy.history_events(before, after) == app.history_events(before, after), number
                differential += 1
            # Zurück zu gültigen App-Daten, ohne die Fremdprobe zu speichern.
            app.load_items()
            first = next(entry for entry in app.lists if entry["id"] == first["id"])
            parent = first["items"][0]
            child = parent["children"][0]
            second = next(entry for entry in app.lists if entry["id"] == second["id"])
            app.set_active_list(first["id"])

        # Der gespeicherte Unterbaum bleibt der Aktivitätsvertrag: ein geändertes
        # Kind zählt auch als Änderung seiner echten Elternaufgabe.
        app.save_items(record_activity=False)
        before_items = legacy_json_items(app)
        old_activity = sum(app.settings.get("activity_history", {}).values())
        with app.item_change([child["id"]]) as change:
            child["description"] = "Neuer Inhalt"
            change.mark()
        after_items = legacy_json_items(app)
        expected = sum(before_items.get(key) != value for key, value in after_items.items())
        expected += len(set(before_items) - set(after_items))
        assert expected == 2
        assert sum(app.settings["activity_history"].values()) - old_activity == expected
        assert app.settings["recent_lists"][0]["id"] == first["id"]
        undo_depth = len(app.undo_stack)
        app.tree.focus_set()
        root.focus_force()
        root.event_generate("<Command-z>" if sys.platform == "darwin" else "<Control-z>")
        root.update()
        assert len(app.undo_stack) == undo_depth - 1
        assert app.find_item_in_lists(child["id"])[0]["description"] != "Neuer Inhalt"
        root.update()
        # Undo ersetzt die Objekte: danach stets über die ID wiederfinden.
        child = app.find_item_in_lists(child["id"])[0]

        # Kein Vergleichsstand für Aktivität/Zuletzt bearbeitet nach Schreibfehler.
        source = Path(mod.SAVE_FILE)
        written = source.read_bytes()
        activity_before = copy.deepcopy(app.settings.get("activity_history"))
        signatures_before = copy.deepcopy(app._activity_item_signatures)
        recent_before = copy.deepcopy(app.settings.get("recent_lists"))
        child["text"] = "Retry"
        with patch.object(app, "write_json_atomic", side_effect=OSError("Test: Schreiben gesperrt")):
            assert not app.save_items(show_error=False)
        assert source.read_bytes() == written and app.dirty
        assert app.settings.get("activity_history") == activity_before
        assert app._activity_item_signatures == signatures_before
        assert app.settings.get("recent_lists") == recent_before
        assert app.save_items() and not app.dirty
        assert sum(app.settings["activity_history"].values()) - sum(activity_before.values()) == 2

        # Ohne Aufzeichnung trotzdem Baseline fortführen; anschließend kein Nachbuchen.
        activity_before = copy.deepcopy(app.settings["activity_history"])
        recent_before = copy.deepcopy(app.settings["recent_lists"])
        app.settings["history_enabled"] = False
        child["done"] = True
        assert app.save_items(record_activity=False)
        assert child["done_at"]
        assert app.settings["activity_history"] == activity_before
        assert app.settings["recent_lists"] == recent_before
        assert app.save_items()
        assert app.settings["activity_history"] == activity_before
        app.load_items()
        assert app.find_item_in_lists(child["id"])[0]["done_at"] == child["done_at"]
        root.update()
        assert not errors, errors
        print(f"OK: P08a ein Vergleich, Unterbäume, Undo, Fehler/Retry, record=False, Reload; "
              f"{differential} Differenzfälle gegen Git-Baseline")
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
