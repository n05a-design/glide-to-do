"""P03/E01: Teilabgleich, aktuelle Inhalte und wiederverwendbare Dialoge.

Künstliche Daten, echte Mutations-/Modalwege. --app und --fall erlauben
getrennte rote Gegenproben aller drei Bereiche gegen die Vorversion 3.35.0.
Zeitziele werden getrennt mit messung_fundament3360.py gemessen.
"""
import argparse
import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--app", type=Path, default=Path(__file__).resolve().parents[2] / "src/glide/app.pyw")
parser.add_argument("--fall", choices=("home", "library", "settings", "alle"), default="alle")
args = parser.parse_args()
sys.path.insert(0, str(args.app.resolve().parent))

with tempfile.TemporaryDirectory(prefix="glide-fundament-") as data:
    os.environ["GLIDE_DATA_DIR"] = data
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_fundament_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1280x800+20+20")
    errors = []
    root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *a, **k: None

    def settle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    def labels(host):
        result = []
        for widget in app.iter_descendants(host):
            if isinstance(widget, mod.tk.Label):
                result.append(str(widget.cget("text")))
            elif isinstance(widget, mod.tk.Canvas):
                result.extend(str(widget.itemcget(item, "text")) for item in widget.find_all()
                              if widget.type(item) == "text")
        return result

    def card(identity):
        return app._library_card_cache["cards"][("list", identity)][1]

    try:
        inbox = app.ensure_inbox_list()
        inbox["items"] = []
        app.lists = [inbox]
        for n in range(30):
            app.lists.append(app.new_list_object(f"Liste {n:02d}",
                [app.new_item(f"Prüfaufgabe {n}.{i}") for i in range(3)], list_id=f"fundament-{n}"))
        app.lists[1]["items"][0]["planned_date"] = mod.date.today().isoformat()
        app.save_items()
        first_id = app.lists[1]["id"]
        task_id = app.lists[1]["items"][0]["id"]

        if args.fall in ("home", "alle"):
            original_sections = app.plan_day_sections
            section_calls = []
            def sections(*a, **kw):
                section_calls.append(kw)
                return original_sections(*a, **kw)
            app.plan_day_sections = sections
            try:
                with app.render_pass():
                    count = app.count_today_view()
                    assert app.count_today_view() == app.count_today_view() == count
                assert len(section_calls) == 1, "P03: Heute-Zahl mehrfach im selben Aufbau berechnet"
                app.count_today_view()
                assert len(section_calls) == 2, "P03: Heute-Zahl über den Aufbau hinaus gespeichert"
            finally:
                app.plan_day_sections = original_sections
            app.set_home_view()
            settle()
            before = tuple(app.home_content.winfo_children())
            before_labels = labels(app.home_content)
            task_text = app.find_item_in_lists(task_id)[0]["text"]
            assert any(task_text in text for text in before_labels)
            app.toggle_item_done_anywhere(task_id)
            settle()
            app._home_signature = None
            app.refresh_home()
            settle()
            assert tuple(app.home_content.winfo_children()) == before, "P03: Startseitenflächen bei Inhaltsänderung ersetzt"
            assert labels(app.home_content) != before_labels, "P03: sichtbare Tages-/Bestandszahlen veraltet"
            assert not any(task_text in text for text in labels(app.home_content)), "P03: erledigte Aufgabe bleibt als nächster Schritt stehen"
            commands = sum(len(getattr(w, "_tclCommands", ()) or ()) for w in app.iter_descendants(app.home_content))
            for _ in range(5):
                app._home_signature = None
                app.refresh_home()
                settle()
            assert sum(len(getattr(w, "_tclCommands", ()) or ()) for w in app.iter_descendants(app.home_content)) == commands, "P03: Bindungen wachsen"
            app.undo_last_change()
            settle()
            assert not app.find_item_in_lists(task_id)[0]["done"]
            assert any(task_text in text for text in labels(app.home_content)), "P03: Aufgabe nach Undo nicht wieder sichtbar"
            # Erhaltene Flächen dürfen die zuvor versteckte Scrollleiste
            # nicht vom nächsten Configure-Ereignis abhängig machen.
            root.geometry("860x700+20+20")
            app.settings["home_tile_order"] = list(app.home_tile_order())
            app.set_home_view()
            settle()
            assert app.home_canvas.yview()[1] - app.home_canvas.yview()[0] < mod.ThemedAutoScrollbar.FULLY_VISIBLE_RATIO, "Prüfaufbau braucht scrollbaren Inhalt"
            app.set_home_view()
            settle()
            assert app.home_scrollbar.winfo_ismapped(), "P03: Scrollleiste nach erneutem Ansichtsabgleich unsichtbar"
            before_scroll = app.home_canvas.yview()
            app.home_scrollbar.command("moveto", .25)
            settle()
            assert app.home_canvas.yview() != before_scroll, "P03: Scrollleiste bewegt Inhalt nicht"
            root.geometry("1280x800+20+20")
            settle()
            # Monat verwendet grid, Woche pack. Sie dürfen nicht denselben
            # inneren Rahmen mit noch vorhandenen Kindern wiederverwenden.
            app.settings["home_tile_order"] = list(app.HOME_TILE_KEYS)
            app.settings["home_tiles_hidden"] = [key for key in app.HOME_TILE_KEYS
                                                if key not in ("calendar", "progress")]
            app.set_home_view()
            settle()
            calendar_hosts = tuple(app.home_content.winfo_children())
            for mode, _name in (*app.HOME_CALENDAR_CHOICES, *reversed(app.HOME_CALENDAR_CHOICES)):
                app.settings["home_calendar_mode"] = mode
                app.set_home_view()
                settle()
                assert tuple(app.home_content.winfo_children()) == calendar_hosts
                assert any("Kalender" in text for text in labels(app.home_content)), mode
                assert any("Fortschritt" in text for text in labels(app.home_content)), mode
                assert not errors, errors
            # Die bestehende Tageszählung ist kumulativ und kein Teil des
            # Aufgaben-Undo. Hier zählt die tatsächlich wieder offene Aufgabe.
            print("OK P03 Startseite: Inhaltsänderung/Undo, Flächen, Rückrufe")

        if args.fall in ("library", "alle"):
            app.set_library_view()
            settle()
            first = card(first_id)
            others = tuple(app.library_cards[1:])
            heading = app.library_open_buttons[("list", first_id)]
            heading.focus_force()
            settle()
            app.home_canvas.yview_moveto(.25)
            settle()
            scroll = app.home_canvas.yview()[0]
            app.toggle_item_done_anywhere(task_id)
            settle()
            assert card(first_id) is first, "P03: geänderte Bibliothekskarte vollständig ersetzt"
            assert tuple(app.library_cards[1:]) == others, "P03: unbeteiligte Karten ersetzt"
            assert "2 offen   ·   1 erledigt" in labels(first), "P03: Kartenstatus sichtbar veraltet"
            assert app.library_open_buttons[("list", first_id)] is heading, "P03: Fokusziel ersetzt"
            assert abs(app.home_canvas.yview()[0] - scroll) < .02, "P03: Scrollposition verloren"
            app.undo_last_change()
            settle()
            assert "3 offen   ·   0 erledigt" in labels(first), "P03: Undo nicht in Karte angekommen"
            entry = next(e for e in app.lists if e["id"] == first_id)
            entry["title"] = "Aktueller Titel"
            entry["note"] = "Aktueller Vorschautext"
            app.refresh_library_page()
            settle()
            assert card(first_id) is first
            assert any("Aktueller Titel" in text for text in labels(first))
            assert "Aktueller Vorschautext" in labels(first)
            app.lists = copy.deepcopy(app.lists)
            app.refresh_library_page()
            settle()
            assert card(first_id) is first, "P03: neue Python-Objekte mit gleichen IDs"
            # Dynamische Kinder müssen auch bei Einfügen/Entfernen richtig stehen.
            entry = next(e for e in app.lists if e["id"] == first_id)
            entry["note"] = ""
            app.refresh_library_page()
            settle()
            assert "Aktueller Vorschautext" not in labels(first)
            assert [w for w in first.inner.pack_slaves() if isinstance(w, mod.tk.Label)][0] is heading
            app.set_home_view()
            settle()
            assert not first.winfo_exists(), "P03: verlassener Ansichtshost bleibt erhalten"
            print("OK P03 Bibliothek: Teilabgleich, Inhalt/Undo/IDs, Fokus/Scrollen, Reihenfolge/Lebensdauer")

        if args.fall in ("settings", "alle"):
            opened = []
            original_modal = app.run_modal
            def modal(dialog, *a, **kw):
                def inspect():
                    try:
                        opened.append(dialog)
                        capacity = next(w for w in app.iter_descendants(dialog) if w.winfo_name() == "daily_capacity")
                        assert capacity.get() == str(app.daily_capacity_minutes()), "E01: Werte bei Öffnen veraltet"
                        capacity.delete(0, "end")
                        capacity.insert(0, "713")
                    except Exception as exc:
                        errors.append(repr(exc))
                    finally:
                        if len(opened) == 1:
                            dialog.event_generate("<Escape>")
                        else:
                            cancel = next(w for w in app.iter_descendants(dialog)
                                          if getattr(w, "text", None) == "Abbrechen")
                            cancel.command()
                root.after(20, inspect)
                return original_modal(dialog, *a, **kw)
            app.run_modal = modal
            app.show_settings_dialog()
            settle()
            first = opened[-1]
            assert first.winfo_exists() and first.state() == "withdrawn", "E01: wiederverwendbares Einstellungsfenster fehlt"
            assert root.grab_current() is None, "E01: geschlossener Dialog hält den Griff"
            initial_widgets = tuple(app.iter_descendants(first))
            app.show_settings_dialog()
            settle()
            assert opened[-1] is first, "E01: unveränderter Dialog erneut aufgebaut"
            assert tuple(app.iter_descendants(first)) == initial_widgets, "E01: unveränderte Bereiche erneut aufgebaut"
            app.settings["daily_capacity_minutes"] = 481
            app.show_settings_dialog()
            settle()
            assert opened[-1] is not first and not first.winfo_exists(), "E01: geänderter Kontext nicht invalidiert"
            # Zerstören und Fenster-Schließen müssen beide den zentralen Modalweg beenden.
            def destroying_modal(dialog, *a, **kw):
                root.after(20, dialog.destroy)
                return original_modal(dialog, *a, **kw)
            app.run_modal = destroying_modal
            app.show_settings_dialog()
            settle()
            assert root.grab_current() is None
            app.run_modal = original_modal
            print("OK E01: echter Modalweg, Abbruch/Zurücksetzen, Wiederverwendung, Kontextwechsel, Zerstören")
        assert not errors, errors
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
