"""Erinnerungen: Migration, Zustellung, Serien, Fehler und echte Tk-Dialoge."""
import copy
from datetime import datetime, timedelta, timezone
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix="glide-reminders-") as tmp:
    os.environ["GLIDE_DATA_DIR"] = tmp
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_reminders", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    A = mod.ListApp
    root = mod.tk.Tk()
    root.withdraw()
    errors = []
    root.report_callback_exception = lambda *args: errors.append(args)
    app = A(root)
    app.show_error = lambda *args, **kwargs: errors.append(args)
    app.show_warning = lambda *args, **kwargs: errors.append(args)
    app.show_info = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: True
    root.after_cancel(app._reminder_tick_id)
    app._after_ids.discard(app._reminder_tick_id)
    app._reminder_tick_id = None
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    past = (now - timedelta(hours=2)).isoformat(timespec="seconds")

    def fixed(at=past):
        return {"mode": "fixed", "at": at}

    def find(item):
        return app.find_item_in_lists(item["id"])[0]

    def new_list(*items):
        entry = app.new_list_object("Erinnerungstest", list(items))
        app.lists.append(entry)
        app.set_active_list(entry["id"])
        assert app.save_items()
        return entry

    try:
        # Format-12-Datei bleibt vor jeder ersten Format-13-Speicherung bytegleich gesichert.
        old = (REPO / "tests/fixtures/current_v12/reference_v12.json").read_bytes()
        Path(mod.SAVE_FILE).write_bytes(old)
        # Seit 29.09.2026 stellt schon das Laden um (`migrate_on_start`).
        # Scheitert dabei die Vorsicherung, bleibt die Datei bytegleich, und
        # erst ein späteres Speichern mit Sicherung stellt um.
        with patch.object(mod.shutil, "copy2", side_effect=OSError("Originalkopie gesperrt")):
            app.load_items()
            assert Path(mod.SAVE_FILE).read_bytes() == old
            assert not app.save_items(show_error=False)
        assert all(item["reminder"] is None for entry in app.lists for item in app.walk_items(entry["items"]))
        assert Path(mod.SAVE_FILE).read_bytes() == old
        assert app.save_items()
        backups = list(Path(mod.BACKUP_DIR).glob("liste_vor_format13_*.json"))
        assert len(backups) == 1 and backups[0].read_bytes() == old
        assert json.loads(Path(mod.SAVE_FILE).read_text())["version"] == 20
        assert app.save_items() and len(list(Path(mod.BACKUP_DIR).glob("liste_vor_format13_*.json"))) == 1

        # Persistente Zustellung; Hintergrundvorgänge zählen nicht als Bearbeitung oder Undo.
        item = app.new_item("Exposé abgeben", due="2090-09-14", due_time="12:00", reminder=fixed())
        entry = new_list(item)
        app.snapshot_undo()
        activity = copy.deepcopy(app.settings.get("activity_history"))
        undo_count = len(app.undo_stack)
        assert app.process_reminders(now) == 1
        assert app.process_reminders(now + timedelta(minutes=1)) == 0
        assert next(row for row in app.reminder_rows(now - timedelta(days=1))
                    if row["item"]["id"] == item["id"])["state"] == "Offen / verpasst"
        assert len(app.undo_stack) == undo_count
        assert app.settings.get("activity_history") == activity
        delivered = copy.deepcopy(item["reminder"])
        app.load_items()
        item = find(item)
        assert item["reminder"] == delivered and app.process_reminders(now) == 0
        app.undo_last_change()
        item = find(item)
        assert app.process_reminders(now) == 0, "Undo darf keine Zustellung wiederholen"

        # Aufschub bleibt über Neustart erhalten und verändert weder Frist noch Regel.
        due_before = (item["due"], item["due_time"], item["repeat"])
        until = (now + timedelta(hours=1)).isoformat(timespec="seconds")
        assert app.change_reminder(item["id"], "snooze", until)
        app.load_items()
        item = find(item)
        assert (item["due"], item["due_time"], item["repeat"]) == due_before
        assert app.process_reminders(now + timedelta(minutes=59)) == 0
        assert app.process_reminders(now + timedelta(hours=1)) == 1
        assert app.process_reminders(now + timedelta(hours=2)) == 0
        assert app.change_reminder(item["id"], "acknowledge")
        assert not item["done"]

        # Relative Erinnerungen reagieren auf Friständerung und entfernen einen alten Aufschub.
        relative = app.new_item("Serienaufgabe", due="2090-09-14", due_time="12:00",
            reminder={"mode": "relative", "minutes": 1440}, repeat={"art": app.REPEAT_DAILY})
        fixed_repeat = app.new_item("Einmaliger Serienhinweis", due="2090-09-14", due_time="12:00",
            reminder=fixed(), repeat={"art": app.REPEAT_DAILY})
        new_list(relative, fixed_repeat)
        before = app.reminder_event(relative)
        assert before["at"] == (datetime.fromisoformat(app.local_reminder_time("2090-09-14", "12:00")) - timedelta(days=1)).isoformat(timespec="seconds")
        assert app.change_reminder(relative["id"], "snooze", until)
        with app.item_change([relative["id"]]) as change:
            relative["due"] = "2090-09-15"
            change.mark()
        after = app.reminder_event(relative)
        assert after["key"] != before["key"] and after["at"] != until
        # Abschließen funktioniert auch aus einer anderen aktiven Liste.
        app.set_active_list(entry["id"])
        assert app.change_reminder(relative["id"], "complete")
        assert relative["due"] == "2090-09-16" and not relative["done"]
        assert relative["reminder"] == {"mode": "relative", "minutes": 1440}
        assert app.reminder_event(relative)["key"] != after["key"]
        assert app.change_reminder(fixed_repeat["id"], "complete")
        assert fixed_repeat["reminder"] is None and not fixed_repeat["done"]
        relative["due_time"] = None
        relative["reminder"]["minutes"] = 0
        assert app.reminder_event(relative)["at"] == app.local_reminder_time("2090-09-16", "09:00")
        relative["due"] = None
        assert app.reminder_event(relative) is None
        relative["done"] = True
        assert app.reminder_event(relative) is None

        # Fehler dürfen keinen Zustellbeleg oder Abschluss vortäuschen.
        failed = app.new_item("Speicherfehler", reminder=fixed())
        new_list(failed)
        original_write = app.write_json_atomic
        def fail_task_save(path, payload):
            if path == mod.SAVE_FILE:
                raise OSError("Test: Speicher nicht verfügbar")
            return original_write(path, payload)
        before = copy.deepcopy(failed)
        with patch.object(app, "write_json_atomic", side_effect=fail_task_save):
            assert app.process_reminders(now) == 0
            assert failed == before and app._reminder_error
            completion_before = copy.deepcopy(app.settings.get("completion_history"))
            assert not app.change_reminder(failed["id"], "complete")
            assert failed == before and app.settings.get("completion_history") == completion_before
        assert len(errors) == 1 and "Speicher" in str(errors.pop())
        assert app.process_reminders(now) == 1
        app.load_items()
        failed = find(failed)
        assert app.process_reminders(now) == 0
        # Bekannte Fremdbelegung sperrt auch Zustellmetadaten.
        with patch.object(app, "refresh_data_lock"):
            app._data_read_only = True
            saved = Path(mod.SAVE_FILE).read_bytes()
            assert app.process_reminders(now) == 0
            assert Path(mod.SAVE_FILE).read_bytes() == saved
            app._data_read_only = False

        # Papierkorb und Wiederherstellung bewahren die Identität und Zustellbelege.
        app.open_task_in_source_list(app.find_item_in_lists(failed["id"])[3]["id"], failed["id"])
        app.move_item_to_trash(failed["id"])
        assert not any(row["item"]["id"] == failed["id"] for row in app.reminder_rows())
        trash_id = next(trash["id"] for trash in app.trash if trash.get("item", {}).get("id") == failed["id"])
        assert app.restore_trash_entry(trash_id)
        failed = find(failed)
        assert app.process_reminders(now) == 0

        # Backups enthalten Konfiguration und Aufschub. Eine alte unzugestellte
        # Sammlung erzeugt einen gemeinsamen Bestand, keine Reihe modaler Fenster.
        missed = [app.new_item(f"Verpasst {index}", reminder=fixed()) for index in range(25)]
        new_list(*missed)
        backup_path = str(Path(tmp) / "reminders.glidebackup")
        expected = copy.deepcopy(app.complete_backup_payload())
        app.write_complete_backup(backup_path, expected)
        assert app.import_full_backup(path=backup_path, show_success=False)
        assert app.process_reminders(now) == 25
        assert app.process_reminders(now) == 0
        assert not [w for w in root.winfo_children() if isinstance(w, mod.tk.Toplevel)]
        assert app.save_items()
        before_restart = {row["item"]["id"]: copy.deepcopy(row["item"]["reminder"]) for row in app.reminder_rows()}
        app.load_items()
        assert before_restart == {row["item"]["id"]: row["item"]["reminder"] for row in app.reminder_rows()}
        assert app.process_reminders(now) == 0
        clone = app.copy_items_with_new_ids([find(missed[0])])[0]
        assert clone["id"] != missed[0]["id"] and clone["reminder"] == fixed()
        bad = app.complete_backup_payload()
        bad["lists"][0]["items"].append({"id": "bad-reminder", "text": "Ungültig", "reminder": {"mode": "fixed", "at": "2090-01-01T10:00"}})
        try:
            app.validate_backup_schema(bad, portable=True)
            raise AssertionError("Mehrdeutiger Importzeitpunkt wurde akzeptiert")
        except ValueError:
            pass
        # Nur gültige Konfigurationen akzeptieren, bool ist kein Minutenabstand.
        for invalid in ({"mode": "relative", "minutes": True}, {"mode": "relative", "minutes": -1},
                        {"mode": "fixed", "at": "ungültig"}, {"mode": "unbekannt"}):
            try:
                A.normalize_reminder(invalid)
                raise AssertionError(invalid)
            except ValueError:
                pass

        # Aufmerksamkeit bei laufender App: ein Anstoß je Prüflauf, keiner je
        # Aufgabe, keiner ohne gespeicherten Beleg, keiner bei offenem Dialog.
        anstoesse = []
        app._attention_backend = lambda: anstoesse.append(1)

        def tick():
            """Prüflauf wie zur Laufzeit, ohne den Folgetimer stehen zu lassen."""
            app.reminder_tick()
            pending = getattr(app, "_reminder_tick_id", None)
            if pending:
                root.after_cancel(pending)
                app._after_ids.discard(pending)
                app._reminder_tick_id = None

        erste, zweite = app.new_item("Anstoß A", reminder=fixed()), app.new_item("Anstoß B", reminder=fixed())
        new_list(erste, zweite)
        app.settings["reminder_attention"] = True
        tick()
        assert len(anstoesse) == 1, f"Zwei fällige Hinweise, ein Anstoß erwartet: {anstoesse}"
        assert find(erste)["reminder"]["delivered_key"] and find(zweite)["reminder"]["delivered_key"]
        tick()
        assert len(anstoesse) == 1, "Ohne neue Zustellung darf nichts hervorgehoben werden"

        # Ein offener modaler Dialog wird weder unterbrochen noch übergangen.
        gesperrt = app.new_item("Anstoß bei Dialog", reminder=fixed())
        new_list(gesperrt)
        with patch.object(app.root, "grab_current", return_value=app.root):
            tick()
        assert len(anstoesse) == 1 and find(gesperrt)["reminder"].get("delivered_key") is None
        tick()
        assert len(anstoesse) == 2 and find(gesperrt)["reminder"]["delivered_key"]

        # Ein Speicherfehler erzeugt weder Beleg noch Anstoß.
        misslungen = app.new_item("Anstoß ohne Beleg", reminder=fixed())
        new_list(misslungen)
        with patch.object(app, "write_json_atomic", side_effect=fail_task_save):
            tick()
        assert len(anstoesse) == 2 and find(misslungen)["reminder"].get("delivered_key") is None
        # Die Hintergrundzustellung meldet nicht modal, sondern über die
        # Statuszeile; ein Fenster mitten in fremder Arbeit wäre der falsche Ort.
        assert not errors, errors
        assert app._reminder_error and "nicht gespeichert" in app._reminder_error

        # Abgeschaltet bleibt abgeschaltet, auch nach erneutem Laden.
        app.settings["reminder_attention"] = False
        assert app.save_settings()
        tick()
        assert len(anstoesse) == 2 and find(misslungen)["reminder"]["delivered_key"]
        assert not app._reminder_error, "Ein geglückter Prüflauf räumt die Meldung weg"
        gespeichert = A.normalize_personal_settings(json.loads(Path(mod.SETTINGS_FILE).read_text(encoding="utf-8")))
        assert gespeichert["reminder_attention"] is False
        app.settings["reminder_attention"] = True
        assert app.save_settings()
        # Die echte Plattformermittlung läuft einmal auf dieser Maschine und
        # darf nie werfen; ohne tragfähigen Weg bleibt der Anstoß folgenlos.
        del app._attention_backend
        app.request_reminder_attention()
        assert hasattr(app, "_attention_backend") and not errors

        # Sommerzeit, doppelte Herbststunde und Wechsel der lokalen Zeitzone.
        if hasattr(time, "tzset"):
            previous_zone = os.environ.get("TZ")
            try:
                os.environ["TZ"] = "Europe/Berlin"
                time.tzset()
                assert A.local_reminder_time("2026-10-25", "02:30") == "2026-10-25T00:30:00+00:00"
                try:
                    A.local_reminder_time("2026-03-29", "02:30")
                    raise AssertionError("Nicht existierende Uhrzeit akzeptiert")
                except ValueError:
                    pass
                assert A.local_reminder_time("2026-03-29", "02:30", strict=False) == "2026-03-29T01:30:00+00:00"
                zone_item = app.new_item("Zeitzone", due="2026-10-25", due_time="10:00", reminder={"mode": "relative", "minutes": 60})
                berlin = A.reminder_event(zone_item)
                fixed_item = app.new_item("Fester Zeitpunkt", reminder=fixed(A.local_reminder_time("2026-10-25", "10:00")))
                fixed_berlin = A.reminder_event(fixed_item)
                os.environ["TZ"] = "America/New_York"
                time.tzset()
                new_york = A.reminder_event(zone_item)
                assert berlin["at"] != new_york["at"] and berlin["key"] == new_york["key"]
                assert A.reminder_event(fixed_item) == fixed_berlin
            finally:
                if previous_zone is None:
                    os.environ.pop("TZ", None)
                else:
                    os.environ["TZ"] = previous_zone
                time.tzset()

        # Echte Eingabemasken: Speichern/Abbruch, eigene Abstände, thematisierte
        # Übersicht und feste Aktionsleiste bei kleiner Fenstergröße.
        root.geometry("1000x760+10+10")
        root.deiconify()
        real_modal = app.run_modal
        for theme in ("light", "dark"):
            app.set_design(theme, apply_now=False)
            app.apply_theme()
            source = find(missed[0])
            original = copy.deepcopy(source)
            def edit_dialog(dialog, parent=None):
                dialog.update()
                editor = next(w for w in descendants(dialog) if w.winfo_name() == "reminder_editor")
                editor.mode_var.set("Eigener Abstand")
                editor.minutes_var.set("90")
                dialog.update()
                assert editor.winfo_ismapped()
                # Abbruch darf weder Konfiguration noch Zustellstatus anfassen.
                dialog.destroy()
            app.run_modal = edit_dialog
            assert app.themed_item_details_dialog(source) is None
            assert source == original
            def overview(dialog, parent=None):
                dialog.geometry("720x520")
                dialog.update()
                tree = next(w for w in descendants(dialog) if w.winfo_name() == "reminders_tree")
                assert len(tree.get_children()) >= 25
                buttons = [w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)]
                assert len(buttons) == 5
                for button in buttons:
                    assert button.winfo_ismapped()
                    assert button.winfo_rooty() + button.winfo_height() <= dialog.winfo_rooty() + dialog.winfo_height()
                    assert mod.tkfont.Font(font=button.font).measure(button.text) + 24 <= button.winfo_width()
                target_id = tree.selection()[0]
                app.search_placeholder_active = False
                app.search_var.set("Nicht zutreffender Suchfilter")
                next(button for button in buttons if button.text == "Aufgabe öffnen").command()
                assert not app.current_search_query()
                assert app.tree.exists(target_id) and app.tree.selection() == (target_id,)
            app.run_modal = overview
            app.open_reminders()
            holder = mod.tk.Toplevel(root)
            editor, read = app.make_reminder_editor(holder, holder, {"reminder": None})
            editor.pack(fill="x")
            editor.mode_var.set("1 Tag vorher")
            assert read("2090-01-01") == {"mode": "relative", "minutes": 1440}
            editor.mode_var.set("Eigener Abstand")
            editor.minutes_var.set("90")
            assert read("2090-01-01") == {"mode": "relative", "minutes": 90}
            editor.mode_var.set("Fester Zeitpunkt (einmalig)")
            assert read(None)["mode"] == "fixed"
            editor.mode_var.set("Keine Benachrichtigung")
            assert read(None) is None
            holder.destroy()
            # Der tatsächliche Speichern-Button liefert das neue Feld; Anwenden
            # und erneutes Öffnen bewahren den bereits gespeicherten Beleg.
            def save_form(dialog, parent=None):
                dialog.update()
                editor = next(w for w in descendants(dialog) if w.winfo_name() == "reminder_editor")
                editor.mode_var.set("Zur Fälligkeit")
                due_fields = [w for w in descendants(dialog) if isinstance(w, mod.DueField)]
                due_fields[0].set_due("2090-09-14")
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton) and w.text == "Speichern").command()
            app.run_modal = save_form
            details_result = app.themed_item_details_dialog(source)
            assert details_result["reminder"] == {"mode": "relative", "minutes": 0}
            details_result["text"] += " " + theme
            with app.item_change((), restore=False) as change:
                assert app.apply_item_details(source, details_result)
                change.mark()
            # Vorlagen erhalten denselben relativen Hinweis, aber keine alten
            # Zustellbelege beim Einsetzen als neue Aufgabenidentität.
            template = app.capture_template(list_id=app.find_item_in_lists(source["id"])[3]["id"])
            with mod.TemplateDraft(app, template) as draft:
                record = draft.export_record()
            assert record["payload"]["version"] == 20
            assert any(task.get("reminder") == {"mode": "relative", "minutes": 0}
                       for entry_record in record["payload"]["lists"] for task in app.walk_items(entry_record["items"]))
        app.run_modal = real_modal
        assert not errors, errors
        # Tatsächlicher Neustart des App-Objekts mit demselben isolierten Datenordner.
        assert app.save_items()
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
        root = mod.tk.Tk()
        root.withdraw()
        app = A(root)
        assert app.process_reminders(now) == 0
        print("OK: Format 13, Originalkopie, einmalige Zustellung, Aufschub, Serien, Papierkorb, Backup, Fehler, Aufmerksamkeit, Zeitwechsel, Hell/Dunkel und Neustart")
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
