"""Bibliothekskarten: Wiederverwendung, Invalidierung und native Bedienung.

--measure JSON --app SNAPSHOT misst denselben isolierten Aufbau vor/nach.
Keine harten Zeitgrenzen; Identität und beobachtbare Inhalte sind die Abnahme.
"""
import argparse
import copy
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
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--measure", type=Path)
parser.add_argument("--items", type=int, default=1000)
parser.add_argument("--lists", type=int, default=12)
parser.add_argument("--rounds", type=int, default=8)
args = parser.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str(args.app.resolve().parent))

with tempfile.TemporaryDirectory(prefix="glide-library-cards-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_library_cards", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1400x950+0+30")
    errors = []
    def callback_error(*exc):
        errors.append(str(exc[1]))
        traceback.print_exception(*exc)
    root.report_callback_exception = callback_error
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *a, **k: None

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    class CardObservation:
        def __init__(self, surface):
            self.surface = surface
            # Der alte Test verlangte den Austausch geänderter Karten. Seit dem
            # Teilabgleich zählt stattdessen ihr tatsächlich sichtbarer Inhalt.
            self.content = []
            for widget in app.iter_descendants(surface):
                options = widget.keys()
                self.content.append((type(widget).__name__, tuple((key, str(widget.cget(key)))
                    for key in ("text", "image", "font", "fg", "bg") if key in options)))
                if isinstance(widget, mod.tk.Canvas):
                    self.content.append(tuple((widget.type(item), tuple(widget.coords(item)))
                        for item in widget.find_all()))
        def winfo_exists(self):
            return self.surface.winfo_exists()

    def cards():
        return dict(zip([(kind, entry["id"]) for kind, entry in app.library_entries(
            archived=bool(getattr(app, "_library_show_archive", False)))],
            (CardObservation(surface) for surface in app.library_cards)))

    def changed(before, after):
        return {key for key in before.keys() & after.keys()
                if before[key].surface is not after[key].surface or before[key].content != after[key].content}

    try:
        inbox = app.ensure_inbox_list()
        inbox["items"] = []
        folder_entry = app.new_folder_object("Projekt", folder_id="perf-folder")
        app.folders = [folder_entry]
        app.lists = [inbox]
        for number in range(args.lists):
            items = [app.new_item(f"Aufgabe {i:05d}", item_id=f"task-{i}",
                     due=(mod.date.today() - mod.timedelta(days=1)).isoformat(),
                     description="Prüftext " * 5) for i in range(number, args.items, args.lists)]
            app.lists.append(app.new_list_object(f"Liste {number:02d}", items,
                list_id=f"list-{number}", folder_id=folder_entry["id"] if number == 0 else None))
        first = app.lists[1]
        task = first["items"][0]
        note = app.new_list_object("Notiz", [], list_kind="note", list_id="note-fixture",
            rich_note={"text": "Notizinhalt", "spans": [], "links": {}})
        app.lists.append(note)
        drawing = app.new_list_object("Zeichnung", [], list_kind="drawing", list_id="drawing-fixture")
        model = mod.glide_drawing.DrawingModel(["#FFFFFF", "#000000"], size=16)
        drawing["drawing"] = model.to_document()
        app.lists.append(drawing)
        app.save_items()
        app.set_library_view()
        idle()
        creations = [0]
        original_make = app.make_rounded_container
        def make(*a, **k):
            creations[0] += 1
            return original_make(*a, **k)
        app.make_rounded_container = make

        if args.measure:
            timings = {}
            counts = {}
            def unchanged():
                app.refresh_library_page()
            def toggle():
                task["done"] = not task["done"]
                app.clear_render_cache()
                app.refresh_library_page()
            def reorder():
                app.lists[1:] = reversed(app.lists[1:])
                app.refresh_library_page()
            for name, action in [("Unverändert", unchanged), ("Aufgabenstatus", toggle),
                                 ("Reihenfolge", reorder)]:
                values, built = [], []
                warmup_start = time.perf_counter()
                action()
                idle()
                warmup_ms = (time.perf_counter() - warmup_start) * 1000
                for _ in range(args.rounds):
                    start_count = creations[0]
                    start = time.perf_counter()
                    action()
                    idle()
                    values.append((time.perf_counter() - start) * 1000)
                    built.append(creations[0] - start_count)
                timings[name] = {"warmup_ms": round(warmup_ms, 3), "median_ms": round(statistics.median(values), 3),
                    "p95_ms": round(sorted(values)[math.ceil(len(values) * .95) - 1], 3),
                    "samples_ms": [round(v, 3) for v in values]}
                counts[name] = built
            assert not errors, errors
            result = {"version": mod.APP_VERSION, "source_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(),
                "python": platform.python_version(), "platform": platform.platform(), "tk": root.tk.call("info", "patchlevel"),
                "profiling": False, "fixture": {"tasks": args.items, "task_lists": args.lists,
                    "notes": 1, "drawings": 1, "folders": 1, "window": "1400x950", "idle_rounds": 3},
                "scope": "Render-only repeated refresh within existing library, not cross-view switches or save latency",
                "warm_rounds": args.rounds, "timings": timings, "rounded_container_creations": counts,
                "callback_errors": errors}
            args.measure.parent.mkdir(parents=True, exist_ok=True)
            args.measure.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps({"timings": timings, "creations": counts}, ensure_ascii=False))
        else:
            before = cards()
            buttons = dict(app.library_open_buttons)
            action_groups = tuple(app.template_actions.winfo_children())
            app.refresh_library_page()
            idle()
            assert not changed(before, cards()), "unveränderte Karten neu erzeugt"
            assert creations[0] == 0, "unveränderte Karten/Aktionsleiste neu aufgebaut"
            assert action_groups == tuple(app.template_actions.winfo_children())
            assert buttons == app.library_open_buttons
            called = []
            first_command = lambda: called.append("erster")
            second_command = lambda: called.append("zweiter")
            old_density = getattr(app, "_height_density", None)
            old_view = app.view_mode
            # Die allgemeine Leiste isoliert prüfen: Resize darf hier nicht
            # automatisch die Bibliotheksaktionen statt der Prüfbefehle einsetzen.
            app.view_mode = "list"
            app._height_density = "full"
            footer_specs = (("Prüfaktion", first_command, "muted", 148),
                            ("Weitere Aktion", first_command, "muted", 148),
                            ("Import", app.import_partial_backup, "import", 148))
            app.refresh_page_actions(footer_specs)
            idle()
            actions_before = tuple(app.template_actions.winfo_children())
            commands_before = len(app.template_actions._tclCommands)
            app._height_density = "full"
            app.refresh_page_actions(footer_specs)
            idle()
            assert tuple(app.template_actions.winfo_children()) == actions_before
            for _ in range(5):
                app._height_density = "full"
                command = second_command if _ % 2 == 0 else first_command
                app.refresh_page_actions((("Prüfaktion", command, "muted", 148), *footer_specs[1:]))
                idle()
            assert len(app.template_actions._tclCommands) == commands_before, "Aktionsleisten-Rückrufe wachsen"
            button = app.template_action_groups[0].inner.winfo_children()[0]
            button.event_generate("<ButtonPress-1>", x=10, y=10)
            button.event_generate("<ButtonRelease-1>", x=10, y=10)
            idle()
            assert called == ["zweiter"], "gleiche Beschriftung hält veralteten Befehl"
            app._height_density = "compact"
            app.refresh_page_actions(footer_specs)
            idle()
            assert len(app.template_action_groups) == 1, "Importaktion bleibt im niedrigen Fenster"
            app.view_mode = old_view
            app._height_density = old_density
            app.refresh_library_page()
            idle()
            target = buttons[("list", first["id"])]
            target.focus_force()
            idle()
            focus_before = str(root.tk.call("focus", "-lastfor", root))
            scroll_before = app.home_canvas.yview()[0]
            app.refresh_library_page()
            idle()
            # Accessory-Fenster erzwingen keinen macOS-Fokus; vorhandenen Tk-Fokus erhalten.
            assert str(root.tk.call("focus", "-lastfor", root)) == focus_before
            assert abs(app.home_canvas.yview()[0] - scroll_before) < .01
            target.event_generate("<FocusIn>")
            idle()
            assert target.winfo_exists(), "Fokusziel bei unveränderter Vorschau zerstört"
            with app.item_change([task["id"]], restore=False) as change:
                task["done"] = True
                change.mark()
            idle()
            assert changed(before, cards()) == {("list", first["id"]), ("folder", folder_entry["id"])}, "Status invalidiert falsche Karten"
            app.undo_last_change()
            idle()
            first = next(e for e in app.lists if e["id"] == "list-0")
            task = first["items"][0]
            assert not task["done"], "Undo verlor Aufgabenstatus"
            before = cards()
            first["title"] = "Umbenannt"
            app.refresh_library_page()
            idle()
            assert changed(before, cards()) == {("list", first["id"]), ("folder", folder_entry["id"])}
            before = cards()
            note = next(e for e in app.lists if e["id"] == "note-fixture")
            note["rich_note"]["text"] = "Geänderter Notizinhalt"
            app.refresh_library_page()
            idle()
            assert changed(before, cards()) == {("list", note["id"])}
            before = cards()
            app.lists[1:] = reversed(app.lists[1:])
            app.refresh_library_page()
            idle()
            assert not changed(before, cards()), "Umordnen zerstört unveränderte Karten"
            before = cards()
            app.lists = copy.deepcopy(app.lists)
            app.refresh_library_page()
            idle()
            assert not changed(before, cards()), "gleiche Daten mit neuen Python-Objekten ungültig"
            target = app.library_open_buttons[("list", "list-0")]
            target.event_generate("<ButtonPress-1>", x=10, y=10)
            target.event_generate("<ButtonRelease-1>", x=10, y=10)
            idle()
            assert app.active_list_id == "list-0", "wiederverwendeter Befehl öffnet falsches Ziel"
            app.set_library_view()
            idle()
            first = next(e for e in app.lists if e["id"] == "list-0")
            before = cards()
            label_entry = app.new_label_object("Testlabel", label_id="library-label")
            app.labels.append(label_entry)
            first["labels"] = [label_entry["id"]]
            app.refresh_library_page()
            idle()
            assert changed(before, cards()) == {("list", first["id"])}
            before = cards()
            label_entry["name"] = "Neuer Labelname"
            app.refresh_library_page()
            idle()
            assert changed(before, cards()) == {("list", first["id"])}
            before = cards()
            app.get_folder("perf-folder")["title"] = "Neuer Ordnerpfad"
            app.refresh_library_page()
            idle()
            assert changed(before, cards()) == {("list", first["id"]), ("folder", "perf-folder")}
            before = cards()
            drawing = next(e for e in app.lists if e["id"] == "drawing-fixture")
            model.cells[0] = 1
            drawing["drawing"] = model.to_document()
            app.refresh_library_page()
            idle()
            assert changed(before, cards()) == {("list", drawing["id"])}
            assert app._library_images, "Zeichnungsvorschau verlor PhotoImage"
            before = cards()
            first["icon"] = model.to_document()
            app.refresh_library_page()
            idle()
            assert changed(before, cards()) == {("list", first["id"])}
            before = cards()
            old_day, old_clock = mod.date, mod.datetime
            class FollowingClock(old_clock):
                @classmethod
                def now(cls, tz=None):
                    return old_clock.now(tz) + mod.timedelta(days=2)
            class FollowingDay(old_day):
                @classmethod
                def today(cls):
                    return old_day.today() + mod.timedelta(days=2)
            first["items"][0]["due"] = (old_day.today() + mod.timedelta(days=1)).isoformat()
            app.refresh_library_page()
            idle()
            before = cards()
            mod.date, mod.datetime = FollowingDay, FollowingClock
            try:
                app.clear_render_cache()
                app.refresh_library_page()
                idle()
                assert changed(before, cards()) == {("list", first["id"]), ("folder", "perf-folder")}, "neue Überfälligkeit nicht frisch berechnet"
                assert before[("list", "note-fixture")].surface is cards()[("list", "note-fixture")].surface
                assert before[("list", "drawing-fixture")].surface is cards()[("list", "drawing-fixture")].surface
            finally:
                mod.date, mod.datetime = old_day, old_clock
            app.clear_render_cache()
            app.refresh_library_page()
            idle()
            before = cards()
            before_bindings = len(app._library_card_cache["grid"]._tclCommands)
            for _ in range(5):
                app.refresh_library_page()
            idle()
            assert not changed(before, cards())
            assert len(app._library_card_cache["grid"]._tclCommands) == before_bindings, "Configure-Bindungen wachsen pro Refresh"
            for width in (860, 1200, 1400):
                root.geometry(f"{width}x950")
                idle()
                assert not changed(before, cards()), "Breitenwechsel zerstört Karten"
                assert all(surface.winfo_ismapped() for surface in app.library_cards), "neue Spalten verlieren Karte"
            before = cards()
            app.cycle_library_card_size()
            idle()
            assert changed(before, cards()) == set(before), "Kartengröße nicht invalidiert"
            before = cards()
            app.settings["ui_font_size"] = "gross"
            app.apply_ui_font()
            app.refresh_library_page()
            idle()
            assert changed(before, cards()) == set(before), "Schriftgröße nicht invalidiert"
            before = cards()
            alternate = next(key for key in app.DESIGNS if key != app.design_name())
            app.set_design(alternate)
            app.refresh_library_page()
            idle()
            assert changed(before, cards()) == set(before), "Designwechsel nicht invalidiert"
            app.set_archived("list", "list-0", True)
            idle()
            assert ("list", "list-0") not in cards()
            app.toggle_library_archive()
            idle()
            assert ("list", "list-0") in cards()
            # U13: Rückholen über denselben Kontextbefehl, keine zweite Knopfleiste.
            refresh_calls = [0]
            original_refresh = app.refresh_library_page
            def count_refresh(*a, **k):
                refresh_calls[0] += 1
                return original_refresh(*a, **k)
            app.refresh_library_page = count_refresh
            menu = app.build_list_menu("list-0")
            index = next(i for i in range(menu.index("end") + 1)
                         if menu.type(i) == "command" and menu.entrycget(i, "label") == "Aus Archiv zurückholen")
            menu.invoke(index)
            idle()
            app.refresh_library_page = original_refresh
            assert refresh_calls[0] == 1, "Zurückholen zeichnet doppelt oder nicht"
            assert not next(e for e in app.lists if e["id"] == "list-0").get("archived")
            assert not cards(), "Archiv nach Rückholen nicht leer"
            hint = app._library_card_cache["empty_hint"]
            app.refresh_library_page()
            idle()
            assert app._library_card_cache["empty_hint"] is hint, "leere Hinweise wachsen bei Refresh"
            app.toggle_library_archive()
            idle()
            old = app._library_card_cache
            app.set_home_view()
            idle()
            assert not old["grid"].winfo_exists(), "Ansichtshost bleibt doppelt erhalten"
            assert getattr(app, "_library_card_cache", None) is None, "zerstörter Host hält Cache"
            app.set_library_view()
            idle()
            assert app._library_card_cache is not old
            current = cards()
            new_entry = app.new_list_object("Neu", [], list_id="new-library-list")
            with app.sidebar_change(refresh_tree=True) as change:
                app.lists.append(new_entry)
                change.mark()
            idle()
            assert not changed(current, cards())
            assert ("list", new_entry["id"]) in cards()
            surface = cards()[("list", new_entry["id"])]
            with app.sidebar_change(refresh_tree=True) as change:
                app.lists.remove(new_entry)
                change.mark()
            idle()
            assert not surface.winfo_exists(), "entfernte Karte bleibt erhalten"
            assert not errors, errors
            print("OK Bibliothek: unverändert, Status, Titel, Notiz, Reihenfolge, IDs, Undo, Fokus, Befehl, Breite, Größe, Lebensdauer, Neu/Entfernt")
    finally:
        root.destroy()
