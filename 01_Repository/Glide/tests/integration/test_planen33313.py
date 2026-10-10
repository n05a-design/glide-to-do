"""KO01/AU02: echte Menüs/Kürzel, mehrere Quellen, Undo und Kapazitätsanzeigen.

--observe dokumentiert die Vorversion ohne neue Anforderungen. Bilder erfassen
nur das eigene Fenster mit künstlichem Bestand; --report hält Rohmessungen fest.
"""
import argparse
import copy
from datetime import date, timedelta
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import time
from types import SimpleNamespace
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--observe", action="store_true")
parser.add_argument("--capture", type=Path)
parser.add_argument("--report", type=Path)
parser.add_argument("--measure", action="store_true")
args = parser.parse_args()
sys.path.insert(0, str(REPO / "src/glide"))
sys.path.insert(0, str(REPO / "tests/tools"))


def labels(menu):
    return [menu.entrycget(i, "label") for i in range((menu.index("end") or 0) + 1)
            if menu.type(i) != "separator"]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix="glide-planen-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_planen_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    errors, observations, timings = [], [], []
    root = mod.tk.Tk()
    root.geometry("1280x800+20+20")
    root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **kw: errors.append(repr(a))
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    def fresh(identity):
        return app.find_item_in_lists(identity)[0]

    def select(view, ids):
        if view == "today":
            app.set_plan_day_view(day=today)
            rows = [f"in-progress:{app.find_item_in_lists(i)[3]['id']}:{i}" for i in ids]
        else:
            app.set_active_list(first["id"])
            if view == "table":
                app.set_table_view()
            rows = list(ids)
        idle()
        app.tree.selection_set(rows)
        app.tree.focus(rows[-1])
        app.tree.focus_force()
        idle()
        return rows

    def popup(action):
        opened = []
        with patch.object(mod.tk.Menu, "tk_popup", lambda menu, *a, **kw: opened.append(menu)):
            action()
            idle()
        assert opened, "Einplanen-Menü wurde nicht geöffnet"
        return opened[-1]

    def invoke(menu, prefix):
        index = next(i for i in range(menu.index("end") + 1) if menu.entrycget(i, "label").startswith(prefix))
        menu.invoke(index)
        idle()

    try:
        idle()
        a = app.new_item("Unterlagen prüfen", planned_date=today, estimated_minutes=30, due=tomorrow)
        b = app.new_item("Entwurf besprechen", planned_date=today, estimated_minutes=50, due=today)
        a["planned_time"], a["due_time"] = "09:00", "17:00"
        b["planned_time"] = "10:00"
        complete = app.new_item("Schon erledigt", planned_date=today, estimated_minutes=40)
        complete["done"] = True
        overdue = app.new_item("Überfällig ohne Bearbeitungstag", due=(date.today() - timedelta(days=1)).isoformat(), estimated_minutes=300)
        unknown = app.new_item("Aufwand noch offen", planned_date=today)
        group = app.new_item("Gliederung", kind=app.ITEM_KIND_GROUP)
        first = app.new_list_object("Projekt Nord", [a, complete, group])
        second = app.new_list_object("Projekt Süd", [b, overdue, unknown])
        app.lists.extend([first, second])
        app.settings["daily_capacity_minutes"] = 180
        profile = [180] * 7
        profile[date.today().weekday()] = 150
        profile[(date.today() + timedelta(days=1)).weekday()] = 60
        app.settings["daily_capacity_by_weekday"] = profile
        app.save_items()
        original = copy.deepcopy(app.lists)
        if not args.observe:
            assert hasattr(app, "build_quick_plan_menu"), "KO01: gemeinsames Einplanen-Menü fehlt"
            # Group/headings excluded, completed estimate retained, no capacity guessed.
            summary = app.planning_available(today)
            assert (summary["minutes"], summary["done_minutes"], summary["without_estimate"], summary["remaining"]) == (120, 40, 1, 30), summary
            preview = app.planning_available(tomorrow, [a["id"], b["id"], a["id"]])
            assert (preview["minutes"], preview["remaining"]) == (80, -20), preview
            assert app.lists == original, "Vorschau verändert Daten"

        # Layout before/after: light/dark, minimum/reference window, large font.
        for width, height in ((860, 700), (1280, 800)):
            for design in ("light", "dark"):
                for size in ("mittel", "gross"):
                    app.settings["ui_font_size"] = size
                    app.set_design(design, apply_now=False)
                    app.apply_ui_font()
                    app.apply_theme()
                    root.geometry(f"{width}x{height}+20+20")
                    rows = select("today", [a["id"], b["id"]])
                    text = app._stats_full_text
                    observations.append(dict(width=width, height=height, design=design, font=size, stats=text,
                                             selection_bar=bool(app.selection_bar.winfo_ismapped())))
                    if not args.observe:
                        assert text.startswith("frei 30 min · 1 ohne Schätzung"), text
                        assert app.plan_button.winfo_ismapped(), "Einplanen fehlt bei Mindestgröße"
                        assert app.plan_button.winfo_rootx() + app.plan_button.winfo_width() <= root.winfo_rootx() + width
                    if args.capture and size == "mittel":
                        from releasedaten import save_windows_screenshot
                        args.capture.mkdir(parents=True, exist_ok=True)
                        save_windows_screenshot(root, args.capture / f"today_{width}x{height}_{design}.png")

        if not args.observe:
            # Selection bar and multi-list selection; one Undo, all unrelated fields exact.
            rows = select("today", [a["id"], b["id"]])
            before = copy.deepcopy(app.lists)
            undo_count = len(app.undo_stack)
            menu = popup(app.plan_button.command)
            assert len(labels(menu)) == 6, labels(menu)
            assert any(x.startswith("Morgen · 20 min überplant") for x in labels(menu)), labels(menu)
            invoke(menu, "Morgen")
            assert len(app.undo_stack) == undo_count + 1
            for identity in (a["id"], b["id"]):
                assert fresh(identity)["planned_date"] == tomorrow
            expected = copy.deepcopy(before)
            for entry in expected:
                for item in app.walk_items(entry["items"]):
                    if item["id"] in (a["id"], b["id"]):
                        item["planned_date"] = tomorrow
            assert app.lists == expected, "Einplanen hat weitere Felder verändert"
            app.tree.focus_force()
            app.tree.event_generate("<Control-z>")
            idle()
            assert app.lists == before, "Ein Undo stellt beide Quelllisten nicht wieder her"
            # An already visible menu keeps preview and target on the same day.
            select("list", [a["id"]])
            menu = app.build_quick_plan_menu()
            class FollowingDate(date):
                @classmethod
                def today(cls):
                    return date.today() + timedelta(days=1)
            count = len(app.undo_stack)
            with patch.object(mod, "date", FollowingDate):
                invoke(menu, "Heute")
            assert fresh(a["id"])["planned_date"] == today and len(app.undo_stack) == count, "Menüziel wechselt nach Vorschau über Mitternacht"
            # Right click retains the multi-selection, not just the clicked source.
            rows = select("today", [a["id"], b["id"]])
            bbox = app.tree.bbox(rows[0])
            with patch.object(mod.tk.Menu, "tk_popup", lambda *a, **kw: None):
                app.tree.event_generate("<Button-3>", x=100, y=bbox[1] + bbox[3] // 2)
                idle()
            assert set(app.quick_plan_selection()) == {a["id"], b["id"]}
            # Keyboard opens exactly the same choices.
            menu = popup(lambda: app.tree.event_generate("<Control-Shift-P>"))
            invoke(menu, "Ohne Tag")
            assert fresh(a["id"])["planned_date"] is None and fresh(a["id"])["planned_time"] == "09:00"
            app.undo_last_change(); idle()
            # List/table row action and existing item_change contract.
            for view in ("list", "table"):
                select(view, [a["id"]])
                bbox = app.tree.bbox(a["id"])
                app.tree.event_generate("<Motion>", x=120, y=bbox[1] + bbox[3] // 2)
                idle()
                assert hasattr(app, "quick_plan_row_button") and app.quick_plan_row_button.winfo_ismapped(), (view, bbox, app.view_mode, app.tree.bind("<Motion>"), errors)
                menu = popup(app.quick_plan_row_button.command)
                invoke(menu, "Heute")
                count = len(app.undo_stack)
                app.apply_quick_plan([a["id"], group["id"]], today)
                assert len(app.undo_stack) == count, "No-op erzeugt Undo"
                app.hide_quick_plan_row()
            # Arbitrary date uses the actual modal calendar; cancel remains a no-op.
            select("list", [a["id"]])
            original_modal = app.run_modal
            modal_errors = []
            def modal_operation(dialog, parent, action):
                def perform():
                    try:
                        assert dialog.winfo_ismapped(), "Kalender muss vor der Bedienung sichtbar sein"
                        assert str(root.focus_get()).startswith(str(dialog)), "Tastaturfokus muss im Kalender liegen"
                        action(dialog)
                    except Exception as exc:
                        modal_errors.append(repr(exc))
                    finally:
                        if dialog.winfo_exists():
                            dialog.destroy()
                root.after(30, perform)
                return original_modal(dialog, parent)
            def cancel(dialog, parent=None):
                return modal_operation(dialog, parent, lambda window: window.event_generate("<Escape>"))
            count = len(app.undo_stack)
            with patch.object(app, "run_modal", cancel):
                app.choose_quick_plan("date")
            idle()
            assert not modal_errors, modal_errors
            assert len(app.undo_stack) == count
            chosen = (date.today() + timedelta(days=10)).isoformat()
            assert a["id"] in app.quick_plan_selection(), ("Auswahl nach Kalenderabbruch verloren", app.quick_plan_selection(), errors)
            confirmed = []
            def confirm(dialog, parent=None):
                def choose(window):
                    confirmed.append(True)
                    field = next(w for w in descendants(window) if isinstance(w, mod.DueField))
                    field.set_due(chosen)
                    assert field.read() == ((chosen, None), None), (field.read(), chosen, errors)
                    texts = [str(w.cget("text")) for w in descendants(window) if isinstance(w, mod.tk.Label)]
                    assert any("frei" in text for text in texts), texts
                    next(w for w in descendants(window) if isinstance(w, mod.RoundedButton) and w.text == "Übernehmen").command()
                return modal_operation(dialog, parent, choose)
            with patch.object(app, "run_modal", confirm): app.choose_quick_plan("date")
            idle()
            assert not modal_errors, modal_errors
            assert confirmed, ("Kalender zum Bestätigen nicht geöffnet", app.quick_plan_selection(), errors)
            assert fresh(a["id"])["planned_date"] == chosen, (fresh(a["id"])["planned_date"], chosen, errors)
            app.undo_last_change(); idle()
            # Real drag bindings announce projected capacity at minimum size.
            root.geometry("860x700+20+20")
            select("list", [a["id"]])
            bbox = app.tree.bbox(a["id"])
            app.tree.event_generate("<ButtonPress-1>", x=110, y=bbox[1] + bbox[3] // 2)
            idle()
            target = app.system_listbox.bbox(app.PLAN_DAY_ROW_ID)
            x = app.system_listbox.winfo_rootx() + target[0] + 40 - app.tree.winfo_rootx()
            y = app.system_listbox.winfo_rooty() + target[1] + target[3] // 2 - app.tree.winfo_rooty()
            app.tree.event_generate("<B1-Motion>", x=x, y=y)
            idle()
            assert app._stats_full_text.startswith("Einplanen auf "), app._stats_full_text
            assert "frei 30 min" in app._stats_full_text, app._stats_full_text
            assert "frei 30 min" in app.stats_label.cget("text"), app.stats_label.cget("text")
            count = len(app.undo_stack)
            app.tree.event_generate("<ButtonRelease-1>", x=x, y=y)
            idle()
            assert len(app.undo_stack) == count, "Ziehen auf bestehenden Tag muss wirkungslos sein"
            # Selection filter and day navigation never change the capacity basis.
            app.set_plan_day_view(day=tomorrow); idle()
            assert app._stats_full_text.startswith("frei 1 h"), app._stats_full_text
            app.set_plan_day_view(day=today); idle()
            # Palette resolves its stable action ID after rebuilding menus.
            select("list", [a["id"]])
            action = next(x for x in app.app_action_entries() if x["id"] == "show_quick_plan_menu")
            menu = popup(lambda: app.invoke_app_action(action, app.tree))
            assert len(labels(menu)) == 6
            # Day review offers all six choices; unplan preserves time and due.
            app._day_review = dict(queue=[dict(list_id=first["id"], item_id=a["id"], reason="carried")],
                                   index=0, counts=dict(today=0, later=0, done=0, skipped=0))
            menu = app.build_quick_plan_menu(item_ids=[a["id"]], review=True)
            assert len(labels(menu)) == 6
            app.day_review_decide("unplan"); idle()
            assert fresh(a["id"])["planned_time"] == "09:00" and fresh(a["id"])["due"] == tomorrow
            app.undo_last_change(); idle()
            # Save failure must not announce successful scheduling or advance review.
            select("list", [a["id"]])
            with patch.object(app, "save_items", return_value=False), patch.object(app, "show_undo_toast") as toast:
                assert app.apply_quick_plan([a["id"]], tomorrow) == 0
                assert not toast.called
            app.undo_last_change(); idle()
            assert fresh(a["id"])["planned_date"] == today
            # Persist and reload after a real menu mutation; stable IDs survive restart.
            app.apply_quick_plan([a["id"], b["id"]], tomorrow)
            saved = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
            serialized = json.dumps(saved, ensure_ascii=False)
            assert a["id"] in serialized and b["id"] in serialized
            restart_ids = (a["id"], b["id"], tomorrow)

        if args.measure:
            for count in (1000, 10000):
                large = app.new_list_object("Messbestand", [app.new_item(f"Aufgabe {i}", estimated_minutes=20,
                                              planned_date=today) for i in range(count)])
                app.lists.append(large)
                app.set_active_list(large["id"]); app.save_items(); idle()
                ids = [item["id"] for item in large["items"][:3]]
                app.tree.selection_set(ids); idle()
                for repeat in range(6):
                    started = time.perf_counter()
                    if args.observe:
                        menu = app.build_item_context_menu()
                    else:
                        menu = app.build_quick_plan_menu()
                    elapsed = (time.perf_counter() - started) * 1000
                    menu.destroy()
                    if repeat: timings.append(dict(items=count, repeat=repeat, menu_ms=elapsed,
                                                    menu="old_context" if args.observe else "quick_plan"))
                app.lists.remove(large)
        idle()
        assert not errors, errors
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(dict(version=mod.APP_VERSION, observe=args.observe,
                app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(), observations=observations,
                timings=timings, callback_errors=errors), ensure_ascii=False, indent=2), encoding="utf-8")
        if not args.observe:
            app.on_close()
            reload_code = """
import importlib.machinery, importlib.util, sys
loader = importlib.machinery.SourceFileLoader('glide_reload', sys.argv[1])
mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
loader.exec_module(mod)
root = mod.tk.Tk()
app = mod.ListApp(root)
try:
    a, b = (app.find_item_in_lists(identity)[0] for identity in sys.argv[2:4])
    assert a['planned_date'] == b['planned_date'] == sys.argv[4]
    assert a['planned_time'] == '09:00' and a['due_time'] == '17:00'
finally:
    app.on_close()
"""
            result = subprocess.run([sys.executable, "-B", "-c", reload_code, str(args.app.resolve()), *restart_ids],
                                    capture_output=True, text=True, encoding="utf-8", timeout=60)
            assert result.returncode == 0, result.stderr
        print("test_planen33313: OK;" + (" Baseline erfasst" if args.observe else
              " Menü/Kürzel/Palette/Zeile, Quelllisten-Mehrfachauswahl, Undo, Kapazität, Datum/Abbruch, Speicherfehler"))
    finally:
        try:
            if root.winfo_exists(): app.on_close()
        except mod.tk.TclError: pass
