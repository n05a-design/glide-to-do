# SPDX-License-Identifier: MPL-2.0
"""P08b, stabile Aktionskennungen und U03/U07 über echte Tk-Bindungen.

--app erlaubt die rote Gegenprobe; --baseline-app den unabhängigen Verlauf-
und Ereignisvergleich mit der vorher ausgelieferten Klasse.
"""
import argparse
import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
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


with tempfile.TemporaryDirectory(prefix="glide-fortsetzung-") as directory:
    os.environ["GLIDE_DATA_DIR"] = directory
    os.environ["GLIDE_TEST_MODE"] = "1"
    mod = load(args.app, "glide_fortsetzung_test")
    root = mod.tk.Tk()
    root.geometry("860x700")
    errors = []
    root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **kw: errors.append(repr(a))
    try:
        root.update()
        assert hasattr(app, "changed_item_lists"), "P08b: deklarierter Listenvergleich fehlt"
        entries = [app.new_list_object(f"Vergleich {n}", [app.new_item(f"Aufgabe {n}")]) for n in range(6)]
        app.lists.extend(entries)
        first, second = entries[:2]
        app.set_active_list(first["id"])
        assert app.save_items(record_activity=False)
        point = first["items"][0]
        old_parts = app._saved_comparison_parts
        with patch.object(mod.glide_comparison, "compare_lists", wraps=mod.glide_comparison.compare_lists) as build:
            app.toggle_item_done_anywhere(point["id"])
        assert build.call_count == 1, ("lokale Änderung muss genau eine Liste lesen", build.call_count)
        assert app._saved_comparison_parts[second["id"]] is old_parts[second["id"]]
        assert point["done_at"]
        assert app.history_snapshot() == app.history_snapshot(app.list_comparison())


        # Gescheiterte Speicherung: keine Cacheübernahme; Retry liest alle Listen.
        point["text"] = "Retry"
        written = Path(mod.SAVE_FILE).read_bytes()
        activity = copy.deepcopy(app._activity_item_signatures)
        # Nur der Bestand scheitert. Fällt der Aufruf auf einen Sekundenwechsel,
        # erneuert `refresh_data_lock` vorher glide.lock über dieselbe Funktion;
        # ein pauschaler Fehler träfe dann die Sperre statt des Schreibwegs.
        write_json_atomic = app.write_json_atomic

        def gesperrt(path, payload):
            if path == mod.SAVE_FILE:
                raise OSError("Test: gesperrt")
            return write_json_atomic(path, payload)
        with patch.object(app, "write_json_atomic", side_effect=gesperrt):
            assert not app.save_items(show_error=False, changed_list_ids={first["id"]})
        assert Path(mod.SAVE_FILE).read_bytes() == written
        assert app._saved_comparison_parts is None and app.dirty
        assert app._activity_item_signatures == activity
        with patch.object(mod.glide_comparison, "compare_lists", wraps=mod.glide_comparison.compare_lists) as build:
            assert app.save_items(changed_list_ids={first["id"]})
        assert build.call_count == len(app.lists)

        # Autosave liest auch einen nicht deklarierten Weg bei dirty=False voll.
        hidden = second["items"][0]
        hidden["description"] = "Autosave-Sicherheitsnetz"
        app.dirty = False
        if app._autosave_id is not None:
            root.after_cancel(app._autosave_id)
            app._after_ids.discard(app._autosave_id)
            app._autosave_id = None
        with patch.object(mod.glide_comparison, "compare_lists", wraps=mod.glide_comparison.compare_lists) as build:
            app.autosave_tick()
        assert build.call_count == len(app.lists)
        assert app._history_baseline["items"][hidden["id"]]["werte"]["description"] == app.history_value(hidden, "description")

        differential = 0
        if args.baseline_app:
            legacy_mod = load(args.baseline_app, "glide_fortsetzung_baseline")
            legacy = object.__new__(legacy_mod.ListApp)
            for number in range(120):
                for name in ("lists", "folders", "labels", "trash"):
                    setattr(legacy, name, copy.deepcopy(getattr(app, name)))
                before = app.history_snapshot()
                assert legacy.history_snapshot() == before
                with app.item_change([point["id"]], restore=False, local=True) as change:
                    point["description"] = f"Differenz {number}"
                    point["due"] = "2090-12-10" if number % 2 else None
                    change.mark()
                current = app.history_snapshot(app.list_comparison())
                assert current == app._history_baseline, number
                for name in ("lists", "folders", "labels", "trash"):
                    setattr(legacy, name, copy.deepcopy(getattr(app, name)))
                assert legacy.history_snapshot() == current, number
                assert legacy.history_events(before, current) == app.history_events(before, current), number
                differential += 1

        # U03: leer/Platzhalter verborgen, Inhalt sichtbar, echte Escape-Bindung.
        for width in (860, 1280):
            root.geometry(f"{width}x800")
            app.search_placeholder_active = False
            app.search_var.set("")
            root.update()
            app.sync_clear_search_visibility()
            assert not app.clear_search_button.winfo_manager(), width
            app.search_var.set("Aufgabe")
            root.update()
            app.sync_clear_search_visibility()
            assert app.clear_search_button.winfo_manager() == "pack", width
            root.focus_force()
            app.search_entry.focus_set()
            root.update()
            assert root.focus_get() is app.search_entry
            root.event_generate("<Escape>")
            root.update()
            assert not app.current_search_query()
            assert not app.clear_search_button.winfo_manager()

        # U07: echte Listenzeile nur bei Inhalt, Auswahl, Leerwerden und Undo.
        inbox = app.ensure_inbox_list()
        inbox_row = app.get_sidebar_iid_for_row(("list", inbox["id"]))
        assert not app.system_listbox.exists(inbox_row)
        inbox["items"].append(app.new_item("Eingangstest"))
        assert app.save_items()
        assert app.system_listbox.exists(inbox_row)
        assert app.system_listbox.set(inbox_row, "count") == "(1)"
        app.system_listbox.selection_set(inbox_row)
        app.system_listbox.event_generate("<<TreeviewSelect>>")
        root.update()
        assert app.active_list_id == inbox["id"] and app.view_mode == "list"
        with app.item_change((), restore=False) as change:
            inbox["items"].clear()
            change.mark()
        root.update()
        assert not app.system_listbox.exists(inbox_row)
        app.tree.focus_set()
        root.focus_force()
        root.event_generate("<Command-z>" if sys.platform == "darwin" else "<Control-z>")
        root.update()
        assert app.system_listbox.exists(inbox_row)
        assert app.find_item_in_lists(point["id"])[0] is not point

        # Kennungen bleiben bei anderer Beschriftung und anderem Menüindex gleich.
        actions = app.app_action_entries()
        assert len({action["id"] for action in actions}) == len(actions)
        assert not [action for action in actions if action["group"] == "Weitere Aktionen"]
        copy_action = next(action for action in actions if action["id"] == "copy_selected_to_clipboard")
        copy_action["menu"].entryconfigure(copy_action["index"], label="Auswahl übernehmen")
        renamed = next(action for action in app.app_action_entries() if action["id"] == copy_action["id"])
        assert renamed["group"] == "Bearbeiten" and renamed["label"] == "Auswahl übernehmen"
        editor = mod.tk.Text(root, undo=True)
        editor.pack()
        editor.insert("1.0", "Kopiert")
        editor.tag_add("sel", "1.0", "end-1c")
        app.invoke_app_action(renamed, editor)
        root.update()
        assert root.clipboard_get() == "Kopiert"
        editor.tag_remove("sel", "1.0", "end")
        editor.mark_set("insert", "end-1c")
        editor.edit_separator()
        app.invoke_app_action(next(action for action in app.app_action_entries()
                                   if action["id"] == "paste_items_from_clipboard"), editor)
        root.update()
        assert editor.get("1.0", "end-1c") == "KopiertKopiert"
        editor.edit_separator()
        app.invoke_app_action(next(action for action in app.app_action_entries()
                                   if action["id"] == "undo_last_change"), editor)
        root.update()
        assert editor.get("1.0", "end-1c") == "Kopiert"
        editor.tag_add("sel", "1.0", "end-1c")
        original_menus = app.action_menus
        replacement = app.build_menu(root, (("Rückgängig", app.undo_last_change),
                                           ("Andere Beschriftung", app.copy_selected_to_clipboard)))
        app.action_menus = [("Bearbeiten", replacement)]
        app.invoke_app_action(copy_action, editor)
        root.update()
        assert root.clipboard_get() == "Kopiert"
        assert app.invoke_app_action({"id": "removed.action"}, editor) is False
        app.action_menus = original_menus
        app.invoke_app_action(next(action for action in app.app_action_entries()
                                   if action["id"] == "select_all_items"), editor)
        assert editor.tag_ranges("sel")
        editor.edit_separator()
        editor.insert("end", " mehr")
        editor.edit_separator()
        app.invoke_app_action(next(action for action in app.app_action_entries()
                                   if action["id"] == "undo_last_change"), editor)
        root.update()
        assert editor.get("1.0", "end-1c") == "Kopiert"
        assert not errors, errors
        assert app.save_items(record_activity=False)
        app.load_items()
        assert app._saved_comparison_parts is None
        assert app.find_item_in_lists(hidden["id"])[0]["description"] == "Autosave-Sicherheitsnetz"
        root.update()
        assert not errors, errors
        # WA-36 (31.10.2026): Anlegen, Verschieben, Löschen und weitere Wege nennen
        # ihre Listen ausdrücklich; unberührte Listen behalten ihren Vergleichsteil.
        # Am Ende der Suite, damit nachlaufende Hinweise/Animationen die Originalprüfungen nicht berühren.
        # Laden und Undo haben die Objekte ersetzt: die Listen über ihre IDs auflösen.
        quelle, ziel, fremd = (next(e for e in app.lists if e["id"] == entries[k]["id"]) for k in (2, 3, 4))
        app.set_active_list(quelle["id"]); root.update()
        assert app.save_items(record_activity=False)

        vergleichsklasse = load(args.baseline_app, "glide_fortsetzung_wa36").ListApp if args.baseline_app else None

        def nur_gelesen(erwartet, aktion, text, ereignis=None):
            alt = app._saved_comparison_parts
            stand_vorher = app._history_baseline
            with patch.object(mod.glide_comparison, "compare_lists", wraps=mod.glide_comparison.compare_lists) as build:
                aktion()
            assert not errors, errors
            assert build.call_count == erwartet, (text + ": gelesene Listen", build.call_count, erwartet)
            assert app._saved_comparison_parts[fremd["id"]] is alt[fremd["id"]], text + ": fremde Liste neu gelesen"
            assert app.history_snapshot() == app.history_snapshot(app.list_comparison()), text + ": Vollvergleich weicht ab"
            assert not app.dirty, text
            ereignisse = app.history_events(stand_vorher, app._history_baseline)
            if ereignis:
                assert any(e["action"] == ereignis for e in ereignisse), (text, ereignisse)
            if vergleichsklasse is not None:
                # Verlaufsereignisse wie in der ausgelieferten Klasse (WA-36-Abkürzung in history_events).
                assert object.__new__(vergleichsklasse).history_events(stand_vorher, app._history_baseline) == ereignisse, text

        def anlegen():
            app.entry.delete(0, "end"); app.entry.insert(0, "WA-36 neu"); app.entry_placeholder_active = False
            app.add_item(); root.update()
        nur_gelesen(1, anlegen, "Anlegen", "created")
        neu = next(item for item in quelle["items"] if item["text"] == "WA-36 neu")
        nur_gelesen(2, lambda: app.move_items_to_list([neu["id"]], ziel["id"]), "Verschieben", "moved")
        assert any(item["id"] == neu["id"] for item in ziel["items"])

        def loeschen():
            alt_id = quelle["items"][0]["id"]
            app.tree.selection_set(alt_id); app.tree.focus(alt_id); app.delete_item(); root.update()
            assert app.find_item_in_lists(alt_id) is None
        nur_gelesen(1, loeschen, "Löschen", "trashed")

        # Weitere Wege mit ausdrücklichen Listen: Sortieren, Gruppe auflösen,
        # listenübergreifender Zeitplan und Erinnerung (Aufbau außerhalb der Messung).
        gruppe = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP, children=[app.new_item("Kind")])
        quelle["items"][:] = [app.new_item("b"), app.new_item("a"), gruppe]
        # Zukünftiger Zeitpunkt: Die Hintergrundzustellung darf den Bestand nicht
        # zeitabhängig zwischen den Prüfungen ändern.
        erinnerung = app.new_item("Erinnerung", due="2090-09-14", due_time="12:00",
                                  reminder={"mode": "fixed", "at": "2090-09-14T08:00:00+00:00"})
        ziel["items"].append(erinnerung)
        assert app.save_items(record_activity=False); app.set_active_list(quelle["id"]); root.update()
        nur_gelesen(1, lambda: app.sort_current_list("alpha"), "Sortieren")
        def aufloesen():
            app.tree.selection_set(gruppe["id"]); app.tree.focus(gruppe["id"]); app.dissolve_selected_group(); root.update()
            assert not any(app.is_group_item(item) for item in quelle["items"])
        nur_gelesen(1, aufloesen, "Gruppe auflösen")
        nur_gelesen(2, lambda: app.apply_time_plan([(quelle["items"][0], "09:30"), (erinnerung, "10:00")]), "Zeitplan")
        spaeter = "2090-09-14T10:00:00+00:00"
        # Erinnerung liegt in der Zielliste; die aktive Liste liest der Vergleich immer mit.
        nur_gelesen(2, lambda: app.change_reminder(erinnerung["id"], "snooze", spaeter), "Erinnerung")
        app.undo_last_change(); root.update()
        assert app.history_snapshot() == app.history_snapshot(app.list_comparison())
        assert not errors, errors
        # WA-36 Seitenleiste (01.11.2026): Baumdurchlauf ohne Generator für
        # kinderlose Punkte, Rohwert-Vorprüfung in Heute-/Labelzählern und
        # ein Listenzähler je Aufbau. Referenz ist der ungekürzte Durchlauf.
        def ref_walk(items):
            for item in items:
                yield item
                yield from ref_walk(item.get("children", []))
        heute_iso = mod.date.today().isoformat()
        label = app.new_label_object("WA36", label_id="wa36-label")
        app.labels.append(label)
        werte = [None, "", "  ", "kein Datum", "2026-13-40", heute_iso, heute_iso + " ", "2000-01-01", "2090-01-01"]
        def baum(tiefe, n):
            punkte = []
            for k in range(n):
                p = app.new_item(f"WA36 {tiefe}.{k}")
                p["kind"] = app.ITEM_KINDS[k % len(app.ITEM_KINDS)]
                p["done"] = k % 5 == 0
                p["due"] = werte[k % len(werte)]
                p["planned_date"] = werte[(k * 3) % len(werte)]
                p["labels"] = [None, [], ["unbekannt"], [label["id"]], [app.SYSTEM_LABEL_LONG]][k % 5]
                p["children"] = baum(tiefe + 1, 3) if tiefe < 2 and k % 3 == 0 else []
                punkte.append(p)
            return punkte
        # Undo hat die Objekte ersetzt: die Liste über ihre ID auflösen.
        fremd = next(e for e in app.lists if e["id"] == entries[4]["id"])
        fremd["items"][:] = baum(0, 12)
        assert app.save_items(record_activity=False); app.update_sidebar_list(); root.update()
        planung = app.planning_lists()
        for entry in app.lists:
            assert [i["id"] for i in app.walk_items(entry["items"])] == [i["id"] for i in ref_walk(entry["items"])]
            assert app.count_items(entry["items"]) == sum(1 for i in ref_walk(entry["items"]) if app.is_schedulable_item(i))
        ref_pool = [i["id"] for e in planung for i in ref_walk(e["items"])
                    if app.is_schedulable_item(i) and not i.get("done")
                    and (app.normalize_due(i.get("due")) or app.normalize_due(i.get("planned_date")))]
        ref_plan = [i["id"] for e in planung for i in ref_walk(e["items"])
                    if app.is_schedulable_item(i) and app.normalize_due(i.get("planned_date")) == heute_iso]
        ref_labels = sum(1 for e in planung for i in ref_walk(e["items"]) if app.column_labels(i))
        with app.render_pass():
            assert sorted(t[4]["id"] for t in app.today_view_pool(apply_filters=False)) == sorted(ref_pool)
            assert sorted(t[4]["id"] for t in app.plan_day_entries(apply_filters=False, day=heute_iso)) == sorted(ref_plan)
            assert app.count_labelled_items() == ref_labels and ref_labels > 0, (app.count_labelled_items(), ref_labels)
            with patch.object(app, "count_items", wraps=app.count_items) as zaehlen:
                assert app.list_item_count(fremd) == app.list_item_count(fremd) == sum(
                    1 for i in ref_walk(fremd["items"]) if app.is_schedulable_item(i))
                # Rekursive Aufrufe zählen Unterpunkte; die Liste selbst wird einmal gezählt.
                oben = [c for c in zaehlen.call_args_list if c.args and c.args[0] is fremd["items"]]
                assert len(oben) == 1, len(oben)
        zeile = app.get_sidebar_iid_for_row(("list", fremd["id"]))
        baumansicht = app.get_sidebar_tree_for_iid(zeile)
        assert f"({app.count_items(fremd['items'])})" in baumansicht.item(zeile, "values"), baumansicht.item(zeile, "values")
        # Erinnerungsstatus: Vorprüfung auf das Feld; Referenz ohne Abkürzung über alle Arten/Zustände.
        for punkt in fremd["items"]:
            punkt["reminder"] = {"mode": "fixed", "at": "2090-01-01T08:00:00+00:00"}
        assert app.save_items(record_activity=False)
        jetzt = mod.datetime.now(mod.timezone.utc)
        ref_erinnerungen = [i["id"] for e in app.planning_lists() for i in ref_walk(e["items"]) if app.reminder_event(i)]
        assert ref_erinnerungen and sorted(r["item"]["id"] for r in app.reminder_rows(jetzt)) == sorted(ref_erinnerungen)
        assert not errors, errors
        print(f"OK: P08b lokale Liste/Retry/Autosave/Undo/Reload, Aktions-ID/Editorfokus, U03/U07, WA-36-Listenumfang/Seitenleiste/Erinnerungen; {differential} Differenzfälle")
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
