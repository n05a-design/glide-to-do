"""Planung: Datenmigration, gemeinsame Aktionen, Dialoge und Austausch."""
import copy
import csv
import importlib.machinery
import importlib.util
import io
import json
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def rejects(action):
    try:
        action()
    except ValueError:
        return
    raise AssertionError("Ungültige Planung wurde angenommen")


with tempfile.TemporaryDirectory(prefix="glide-features314-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features314", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    callbacks = []
    root.report_callback_exception = lambda *args: callbacks.append(args)
    app = mod.ListApp(root)
    app.confirm_template_preview = lambda template: True
    messages = []
    app.show_warning = app.show_error = lambda *args, **kwargs: messages.append(args)
    app.show_info = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: True
    try:
        assert app.DATA_SCHEMA_VERSION == 23, "Format 23 bewahrt lokale Verweise, Live-Listen und Titelbilder."
        assert app.new_item("Alt")["planned_date"] is None
        assert app.normalize_items([{"text": "Alt"}])[0]["estimated_minutes"] is None
        for value in (0, -1, True, 1.5, "60", [], 60001):
            rejects(lambda: app.new_item("Ungültig", estimated_minutes=value))
        for value in ("2026-02-30", "2026-1-2", "morgen", 123, True):
            rejects(lambda: app.new_item("Ungültig", planned_date=value))
        for value in (1, 60, 90, 60000):
            assert app.new_item("Gültig", estimated_minutes=value)["estimated_minutes"] == value
        assert app.format_estimated_minutes(90) == "1 h 30 min"

        target = app.new_list_object("Planungsprüfung", [])
        first = app.new_item("Konzept", due="2090-09-20", planned_date="2090-09-15", estimated_minutes=45)
        second = app.new_item("Freigabe", estimated_minutes=90, kind=app.ITEM_KIND_LONG)
        group = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP, planned_date="2090-09-15", estimated_minutes=60)
        assert group["planned_date"] is group["estimated_minutes"] is None
        group["children"] = [first]
        target["items"] = [group, second]
        app.lists.append(target)
        app.set_active_list(target["id"])
        app.set_table_view()
        root.update()
        ids = [first["id"], second["id"], group["id"]]
        app.apply_planning_selected(ids, {"planned_date": "2090-09-16"})
        assert first["estimated_minutes"] == 45 and second["estimated_minutes"] == 90
        assert first["due"] == "2090-09-20" and second["due"] is None
        assert group["planned_date"] is None
        assert "16.09.2090" in app.tree.item(first["id"], "values")
        assert "45 min" in app.tree.item(first["id"], "values")
        snapshot = copy.deepcopy(target)
        rejects(lambda: app.apply_planning_selected(ids, {"planned_date": "2090-09-17", "estimated_minutes": 0}))
        assert target == snapshot
        app.apply_planning_selected(ids, {"estimated_minutes": None})
        assert first["planned_date"] == "2090-09-16" and first["estimated_minutes"] is None
        app.undo_last_change()
        first = app.find_item_in_lists(ids[0])[0]
        second = app.find_item_in_lists(ids[1])[0]
        assert first["estimated_minutes"] == 45 and second["estimated_minutes"] == 90
        clone = app.copy_items_with_new_ids([first])[0]
        assert clone["id"] != first["id"] and clone["planned_date"] == first["planned_date"]
        assert clone["estimated_minutes"] == 45
        app.set_item_kind(clone, app.ITEM_KIND_HEADING)
        assert clone["planned_date"] is clone["estimated_minutes"] is None
        rejects(lambda: app.apply_item_details(first, {"kind": app.ITEM_KIND_GROUP, "estimated_minutes": 0}))
        assert app.is_schedulable_item(first)

        # Originalbytes bleiben bei der Migration und bei Sicherungsfehlern intakt.
        legacy = copy.deepcopy(app.data_payload())
        legacy["version"] = 13
        for entry in legacy["lists"]:
            for item in app.walk_items(entry["items"]):
                item.pop("planned_date", None)
                item.pop("estimated_minutes", None)
        original = json.dumps(legacy, ensure_ascii=False).encode()
        Path(mod.SAVE_FILE).write_bytes(original)
        app._schema14_backup_checked = False
        with patch.object(mod.shutil, "copy2", side_effect=OSError("Test: Sicherung gesperrt")):
            assert not app.save_items(show_error=False)
        assert Path(mod.SAVE_FILE).read_bytes() == original and app.dirty
        assert app.save_items()
        backups = list(Path(mod.BACKUP_DIR).glob("liste_vor_format14_*.json"))
        assert len(backups) == 1 and backups[0].read_bytes() == original
        assert app.save_items() and len(list(Path(mod.BACKUP_DIR).glob("liste_vor_format14_*.json"))) == 1
        app.load_items()
        first = app.find_item_in_lists(ids[0])[0]
        assert first["estimated_minutes"] == 45 and first["planned_date"] == "2090-09-16"

        # Voll- und Teilbackups, Papierkorb und Vorlage verwenden dieselben Felder.
        backup = Path(folder) / "planung.glidebackup"
        payload = app.complete_backup_payload()
        bad = copy.deepcopy(payload)
        next(item for entry in bad["lists"] for item in app.walk_items(entry["items"]) if item["id"] == ids[0])["estimated_minutes"] = -1
        rejects(lambda: app.validate_backup_schema(bad, portable=True))
        app.write_complete_backup(str(backup), payload)
        assert app.import_full_backup(path=str(backup), show_success=False)
        first = app.find_item_in_lists(ids[0])[0]
        assert first["estimated_minutes"] == 45
        assert app.move_item_to_trash(ids[0]) is not False
        trash = next(entry for entry in app.trash if (entry.get("item") or {}).get("id") == ids[0])
        bad = app.complete_backup_payload()
        next(entry for entry in bad["trash"] if entry["id"] == trash["id"])["item"]["planned_date"] = "kaputt"
        rejects(lambda: app.validate_backup_schema(bad, portable=True))
        assert app.restore_trash_entry(trash["id"])
        first = app.find_item_in_lists(ids[0])[0]
        assert first["estimated_minutes"] == 45
        template = app.capture_template(list_id=target["id"])
        template = app.template_by_id(template["id"])
        template["schedule_anchor"] = (date.today() - timedelta(days=2)).isoformat()
        with mod.TemplateDraft(app, template) as draft:
            assert any(item.get("estimated_minutes") == 45 for entry in draft.lists for item in draft.walk_items(entry["items"]))
        created = app.create_list_from_template(template["id"])
        copied = next(item for item in app.walk_items(created["items"]) if item["text"] == "Konzept")
        assert copied["planned_date"] == "2090-09-18" and copied["due"] == "2090-09-22", copied
        assert copied["estimated_minutes"] == 45

        # Fristlose Aufgaben und Aufwand überstehen den TXT-Rundlauf.
        sample = app.new_item("Ohne Frist", planned_date="2090-09-15", estimated_minutes=90)
        text = io.StringIO()
        app.write_items_to_txt(text, [sample], [])
        restored = app.parse_txt_items(text.getvalue().splitlines())[0]
        assert restored["due"] is None and restored["planned_date"] == sample["planned_date"]
        assert restored["estimated_minutes"] == 90
        markdown = io.StringIO()
        app.write_items_to_markdown(markdown, [sample], 0)
        assert "Bearbeitungstag: 15.09.2090" in markdown.getvalue() and "1 h 30 min" in markdown.getvalue()
        output = io.StringIO()
        app.write_items_to_csv(csv.writer(output, delimiter=";"), [sample], [])
        row = next(csv.reader(io.StringIO(output.getvalue()), delimiter=";"))
        assert len(row) == 13 and row[-2:] == ["15.09.2090", "90"]

        app.set_active_list(target["id"])
        first = app.find_item_in_lists(ids[0])[0]
        with app.item_change([ids[0]]) as change:
            first["repeat"] = app.normalize_repeat({"art": app.REPEAT_DAILY}, default_start=first["due"])
            first["done"] = True
            assert app.advance_repeating_items([ids[0]]) == 1
            change.mark()
        assert first["planned_date"] is None and first["estimated_minutes"] == 45 and not first["done"]
        app.undo_last_change()

        # Echte Dialoge in beiden Themes; Fehler halten die Eingabe offen.
        root.deiconify()
        root.geometry("1100x780+10+10")
        for theme in ("light", "dark"):
            app.set_design(theme, apply_now=False)
            app.apply_theme()
            first = app.find_item_in_lists(ids[0])[0]
            before = copy.deepcopy(first)

            def form(dialog, parent=None):
                dialog.geometry("780x640")
                dialog.update()
                widgets = list(descendants(dialog))
                planning = next(w for w in widgets if isinstance(w, mod.DueField) and not w.show_time)
                assert not planning.time_entry.winfo_ismapped()
                planning.set_due("2090-09-19")
                effort = next(w for w in widgets if w.winfo_name() == "estimated_minutes")
                effort.delete(0, mod.tk.END)
                effort.insert(0, "1.5")
                save = next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == "Speichern")
                assert save.winfo_ismapped() and save.winfo_rooty() + save.winfo_height() <= dialog.winfo_rooty() + dialog.winfo_height()
                save.command()
                assert dialog.winfo_exists()
                effort.delete(0, mod.tk.END)
                effort.insert(0, "120")
                save.command()
            app.run_modal = form
            details = app.themed_item_details_dialog(first)
            assert first == before
            assert details["estimated_minutes"] == 120 and details["planned_date"] == "2090-09-19"
            built = app.build_item_from_dialog(details)
            assert built["estimated_minutes"] == 120
            with app.item_change([ids[0]]) as change:
                assert app.apply_item_details(first, details)
                change.mark()

            def bulk(dialog, parent=None):
                dialog.update()
                widgets = list(descendants(dialog))
                check = next(w for w in widgets if w.winfo_name() == "apply_estimated_minutes")
                check.invoke()
                effort = next(w for w in widgets if w.winfo_name() == "estimated_minutes")
                effort.delete(0, mod.tk.END)
                effort.insert(0, "30")
                next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == "Übernehmen").command()
            app.run_modal = bulk
            app.tree.selection_set(ids[:2])
            app.set_planning_selected()
            assert first["estimated_minutes"] == 30 and first["planned_date"] == "2090-09-19"
            assert app.find_item_in_lists(ids[1])[0]["estimated_minutes"] == 30
            app.run_modal = lambda dialog, parent=None: dialog.destroy()
            before = copy.deepcopy(app.data_payload())
            assert app.themed_item_details_dialog(first) is None
            app.set_planning_selected()
            assert app.data_payload() == before
        assert not callbacks, callbacks
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: Planung, Aufwand, Migration/Sicherungsfehler, Undo, Vorlagen, Backups, Export und Dialoge in beiden Themes")
