"""Schnellerfassung und gespeicherte Filter mit isoliertem Datenordner."""
import copy
import importlib.machinery
import importlib.util
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory(prefix="glide-features311-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features311", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    root = mod.tk.Tk()
    root.withdraw()
    errors = []
    root.report_callback_exception = lambda *error: errors.append(error)
    app = mod.ListApp(root)
    app.show_warning = lambda *args, **kwargs: None
    app.show_error = lambda *args, **kwargs: None
    app.show_info = lambda *args, **kwargs: None
    try:
        inbox = app.ensure_inbox_list()
        target = app.new_list_object("Planung", [])
        app.lists.append(target)
        label = {"id": "features-label", "name": "Fokus", "color": "label_blue"}
        app.labels.append(label)
        app.save_items()
        app.refresh_tree()

        # Deutsche Kurzdeutung bleibt explizit und liefert eine Vorschaugrundlage.
        tomorrow = date.today() + timedelta(days=1)
        assert mod.parse_capture_due("morgen um 14:30") == (tomorrow.isoformat(), "14:30")
        assert mod.parse_capture_due("in 3 Tagen")[0] == (date.today() + timedelta(days=3)).isoformat()
        try:
            mod.parse_capture_due("irgendwann")
        except ValueError:
            pass
        else:
            raise AssertionError("Unbekannte Datumsangabe wurde akzeptiert")

        created = app.capture_item("Schnell erfasst", target["id"], "morgen um 14:30")
        assert created and created["due"] == tomorrow.isoformat() and created["due_time"] == "14:30"
        assert any(item["id"] == created["id"] for item in target["items"])
        app.undo_last_change()
        target_after_undo = next(entry for entry in app.lists if entry["id"] == target["id"])
        assert not any(item["id"] == created["id"] for item in target_after_undo["items"])
        try:
            app.capture_item("", inbox["id"])
        except ValueError:
            pass
        else:
            raise AssertionError("Leere Schnellerfassung wurde angelegt")

        open_item = app.new_item("Offener Fokus", labels=[label["id"]], due=date.today().isoformat())
        done_item = app.new_item("Erledigter Fremdpunkt", labels=[label["id"]], done=True)
        target_after_undo["items"].extend([open_item, done_item])
        app.save_items()
        criteria = {
            "id": "focus-filter",
            "name": "Fokus heute",
            "query": "Fokus",
            "list_ids": [target["id"]],
            "label_ids": [label["id"]],
            "status": "open",
            "importance": "all",
            "due": "today",
            "label_mode": "any",
        }
        assert app.saved_filters.save(criteria)
        assert len(app.saved_filters.entries(criteria)) == 1
        app.saved_filters.open(criteria["id"])
        root.update()
        assert app.view_mode == "saved_filter"
        assert app.get_display_title() == "Fokus heute"
        assert len(app.saved_filters.entries()) == 1
        assert app.current_task_overview_items()[0][4] is open_item
        app.saved_filters.open(criteria["id"])
        assert len(app.settings["saved_filters"]) == 1

        # Entfernte Referenzen bleiben sichtbar und liefern keine fremden Treffer.
        missing = copy.deepcopy(criteria)
        missing["id"] = "missing-filter"
        missing["name"] = "Mit entfernter Liste"
        missing["list_ids"] = ["deleted-list"]
        assert app.saved_filters.save(missing)
        assert app.saved_filters.entries(missing) == []
        assert "entfernte Listen" in app.saved_filters.summary(missing)

        # Ein fehlgeschlagenes Einstellungs-Schreiben rollt den Filter zurück.
        before = copy.deepcopy(app.settings)
        original_save = app.save_settings
        app.save_settings = lambda **kwargs: False
        rejected = copy.deepcopy(criteria)
        rejected["id"] = "rejected"
        rejected["name"] = "Nicht speichern"
        assert not app.saved_filters.save(rejected)
        assert app.settings == before
        app.save_settings = original_save
        assert not errors, errors
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: Schnellerfassung, deutsche Fristvorschau, gespeicherte Filter, Persistenz und Rollback")
