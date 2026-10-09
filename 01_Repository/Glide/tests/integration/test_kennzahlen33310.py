"""P09b: Aufbaugrenzen, echte Undo-Bindung, Schrift-/Host- und Tageswechsel.

--app für rote Gegenprobe; --baseline-app für unabhängige 3.33.9-Differenzprobe.
"""
import argparse
import copy
from datetime import date, datetime, timedelta
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import random
import sys
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--baseline-app", type=Path)
args = parser.parse_args()
sys.path.insert(0, str(REPO / "src/glide"))


def load(path, name):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader))
    sys.modules[name] = mod
    loader.exec_module(mod)
    return mod


with tempfile.TemporaryDirectory(prefix="glide-kennzahlen-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    mod = load(args.app, "glide_metrics_test")
    assert hasattr(mod.ListApp, "list_metrics"), "P09b: gemeinsamer Kennzahlenstand fehlt"
    old = load(args.baseline_app, "glide_metrics_old") if args.baseline_app else None
    errors = []
    root = mod.tk.Tk()
    root.geometry("860x700")
    root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **kw: errors.append(repr(a))
    second_root = None
    try:
        root.update()
        entry = app.new_list_object("Kennzahlen")
        task = app.new_item("Heute", due=date.today().isoformat())
        group = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP)
        child = app.new_item("Kind", due=(date.today() - timedelta(days=1)).isoformat())
        group["children"] = [child]
        entry["items"] = [task, group]
        app.lists.append(entry)
        container = app.new_folder_object("Kennzahlenordner")
        app.folders.append(container)
        entry["folder_id"] = container["id"]
        app.set_active_list(entry["id"])
        app.save_items()
        with patch.object(mod.glide_metrics, "summarize", wraps=mod.glide_metrics.summarize) as builder:
            with app.render_pass():
                first = app.page_chips()
                with app.render_pass():
                    assert app.page_chips() == first
                    assert app.list_metrics(entry["id"]).stats == (2, 0, 1)
                first.append("must not mutate cache")
                assert "must not mutate cache" not in app.page_chips()
            assert builder.call_count == 1, builder.call_count
            app.page_chips()
            assert builder.call_count == 2, "Kennzahlen außerhalb des Aufbaus gehalten"
        assert app._render_cache is None
        with app.render_pass():
            app.page_chips()
            task["done"] = True
            app.save_items()
            with patch.object(mod.glide_metrics, "summarize", wraps=mod.glide_metrics.summarize) as builder:
                assert "1 erledigt" in app.page_chips()
                app.page_chips()
                assert builder.call_count == 1, "Invalidierung verlor die Aufbaugrenze"
        # Reale Tastaturbindung: Save/Undo ersetzen Listen- und Aufgabenobjekte.
        with app.item_change([task["id"]]) as change:
            task["done"] = False
            change.mark()
        app.tree.focus_set()
        root.update()
        app.tree.event_generate("<Command-z>" if mod.IS_MACOS else "<Control-z>")
        root.update()
        current = app.find_item_in_lists(task["id"])[0]
        assert current is not task and current["done"]
        assert "1 erledigt" in app.page_chips()

        actual_today = date.today()
        class Tomorrow(date):
            @classmethod
            def today(cls):
                return actual_today + timedelta(days=1)
        current["done"] = False
        with app.render_pass():
            assert app.list_metrics(entry["id"]).overdue == 1
            with patch.object(mod, "date", Tomorrow):
                assert app.list_metrics(entry["id"]).overdue == 2

        # Messschrift und Zeilenraum werden wiederverwendet, Rand bleibt aktuell.
        label = app.hint_label
        spec = label.cget("font")
        app._measurement_fonts = {}
        app._measurement_linespaces = {}
        with patch.object(mod.tkfont, "Font", wraps=mod.tkfont.Font) as fonts:
            expected = app.hint_line_height(2)
            for _ in range(10):
                assert app.hint_line_height(2) == expected
            assert fonts.call_count == 1, fonts.call_count
        label.configure(pady=5)
        exact = mod.tkfont.Font(root=root, font=spec).metrics("linespace") * 2 + 2 * (5 + mod.CanvasLabel.LABEL_INSET_Y)
        assert app.hint_line_height(2) == exact
        label.configure(font=(app.ui_font_family(), 20, "bold"))
        assert app.hint_line_height(2) != exact
        label.configure(font=spec)
        named = mod.tkfont.nametofont("TkDefaultFont", root=root)
        old_size = named.cget("size")
        a = app.measurement_linespace("TkDefaultFont")
        named.configure(size=old_size + 5)
        assert app.measurement_linespace("TkDefaultFont") > a
        named.configure(size=old_size)
        scaling = float(root.tk.call("tk", "scaling"))
        key = app.measurement_font_key(spec)
        root.tk.call("tk", "scaling", scaling * 1.25)
        assert app.measurement_font_key(spec) != key
        root.tk.call("tk", "scaling", scaling)
        for size in ("klein", "gross", "mittel"):
            app.settings["ui_font_size"] = size
            app.apply_ui_font()
            assert not app._measurement_fonts and not app._measurement_linespaces
            app.apply_theme()
            app.refresh_tree()
            root.update()
        second_root = mod.tk.Tk()
        second_root.withdraw()
        host = object.__new__(mod.ListApp)
        host.root = second_root
        first_font = app.measurement_font(spec)
        second_font = host.measurement_font(spec)
        assert first_font is not second_font and second_font._tk is second_root.tk
        for size in range(8, 150):
            app.measurement_linespace((app.ui_font_family(), size))
        assert len(app._measurement_fonts) <= 128 and len(app._measurement_linespaces) <= 128

        # Unabhängige alte Implementierung, wechselnde Daten und Ansichten.
        if old:
            legacy = object.__new__(old.ListApp)
            legacy.__dict__.update(app.__dict__)
            legacy._render_cache = None
            randomizer = random.Random(33310)
            for number in range(120):
                active = app.current_list()
                for item in app.walk_items(active["items"]):
                    item["done"] = randomizer.choice([True, False])
                    item["due"] = randomizer.choice([None, "bad", actual_today.isoformat(),
                                                     (actual_today + timedelta(days=number % 5 - 2)).isoformat()])
                assert legacy.page_chips() == app.page_chips(), number
                assert legacy.compute_stats(app.items) == app.compute_stats(app.items), number
            # Auch leere Listen, Galerien, Zeichnungen und Ordnersummen.
            modes = [("folder", None), ("list", app.LIST_KIND_GALLERY),
                     ("list", app.LIST_KIND_DRAWING), (app.HOME_VIEW, None)]
            saved_mode = app.view_mode
            saved_kind = active.get("list_kind")
            for mode, kind in modes:
                app.view_mode = legacy.view_mode = mode
                if mode == "folder":
                    app.active_folder_id = legacy.active_folder_id = container["id"]
                if kind:
                    active["list_kind"] = kind
                assert legacy.page_chips() == app.page_chips(), mode
            active["list_kind"] = saved_kind
            app.view_mode = legacy.view_mode = saved_mode
            app.active_folder_id = None
            original_items = active["items"]
            active["items"] = []
            assert legacy.page_chips() == app.page_chips()
            active["items"] = original_items
        app.save_items()
        expected_stats = app.compute_stats(app.items)
        app.schedule_sidebar_heights()
        height_after = app._sidebar_heights_after
        assert height_after in app._after_ids
        app.cancel_pending_callbacks()
        assert height_after not in root.tk.call("after", "info")
        assert not app._sidebar_heights_pending
        assert not errors, errors
        print("OK P09b: Aufbau-/Speichergrenzen, Tastatur-Undo, Tageswechsel, Schrift/Skalierung/Host, Timerabbau; "
              + ("120 alte/neue Kennzahlen identisch" if old else "keine Callbackfehler"))
    finally:
        if second_root is not None:
            second_root.destroy()
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
    # Neustart lädt denselben gespeicherten Bestand ohne alte Kennzahlencaches.
    restarted_root = mod.tk.Tk()
    restarted_root.withdraw()
    restarted_root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
    try:
        restarted = mod.ListApp(restarted_root)
        restarted.set_active_list(entry["id"])
        restarted_root.update()
        assert restarted.list_metrics(entry["id"]).stats == expected_stats
        assert not errors, errors
    finally:
        restarted.cancel_pending_callbacks()
        restarted.release_data_lock()
        restarted_root.destroy()
