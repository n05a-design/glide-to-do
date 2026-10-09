"""Glide 3.28: Tagebuch, responsive Hierarchie und funktionale UI-Politur."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)

with tempfile.TemporaryDirectory(prefix="glide-features328-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features328", str(ROOT / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    errors = []
    root.report_callback_exception = lambda *args: errors.append(args)
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: True
    try:
        # Die 3.28-Funktionen bleiben in jeder späteren Fassung erhalten.
        assert tuple(map(int, mod.APP_VERSION.split("."))) >= (3, 28, 0)
        assert app.DATA_SCHEMA_VERSION == 23
        assert app.ENTRY_MIN_WIDTH == 180

        journal_folder = app.new_folder_object("Tagebuch", folder_kind="journal")
        entry = app.new_list_object(
            "Tagebuch · 23.09.2026", [], folder_id=journal_folder["id"], list_kind="note",
            journal={"favorite": True, "mood": "grateful", "location": " Berlin ",
                     "moment_date": "2026-09-23", "prompt": "Dankbarkeit"},
        )
        assert journal_folder["folder_kind"] == "journal"
        assert entry["journal"] == {
            "favorite": True, "mood": "grateful", "location": "Berlin",
            "moment_date": "2026-09-23", "prompt": "Dankbarkeit",
        }
        assert app.normalize_journal({"mood": "unbekannt", "moment_date": "kaputt"})["mood"] == ""

        app.folders.append(journal_folder)
        app.lists.append(entry)
        app.set_active_list(entry["id"], refresh=False)
        assert app.save_items()
        payload = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
        assert payload["version"] == 23
        loaded, active_id = app.normalize_lists_data(payload)
        restored = next(value for value in loaded if value["id"] == entry["id"])
        assert restored["journal"]["favorite"] is True
        assert restored["journal"]["location"] == "Berlin"
        assert next(value for value in app.folders if value["id"] == journal_folder["id"])["folder_kind"] == "journal"
        assert active_id == entry["id"]

        old_payload = dict(payload)
        old_payload["version"] = 17
        old_bytes = json.dumps(old_payload, ensure_ascii=False, indent=4).encode("utf-8")
        Path(mod.SAVE_FILE).write_bytes(old_bytes)
        app._schema18_backup_checked = False
        app.ensure_schema18_backup()
        migrations = list(Path(mod.BACKUP_DIR).glob("liste_vor_format18_*.json"))
        assert len(migrations) == 1 and migrations[0].read_bytes() == old_bytes

        template_ids = {value["id"] for value in app.default_template_records()}
        assert {"journal-note", "journal-gratitude", "journal-weekly", "journal-folder"} <= template_ids
        assert "Drei gute Dinge" in app.journal_note_document("journal-gratitude")["text"]
        assert "Wochenrückblick" in app.journal_note_document("journal-weekly")["text"]

        # Menüleiste ohne dekorative Umrandung; unbedeutende Fußaktionen neutral.
        # Die eigene Menüzeile existiert nur unter Windows; macOS und Linux
        # verwenden die native Menüleiste ohne eigene Schaltflächen.
        assert bool(app.custom_menu_buttons) == bool(mod.IS_WINDOWS)
        assert all(button.outline is False for button in app.custom_menu_buttons)
        # Die Auswahlleiste (27.09.2026): nur Löschen trägt Farbe.
        for button in (app.flag_button, app.due_button, app.plan_button, app.labels_button):
            assert button.color_key == "muted"

        # Notizwerkzeuge: häufige Funktionen direkt, alles Weitere in „Mehr“.
        app.lists = loaded
        app.set_active_list(entry["id"], refresh=False)
        app.refresh_tree()
        root.update_idletasks()
        editor = app.rich_note_editor
        labels = [widget.text for widget in editor.winfo_children()[0].entries for widget in [widget[0]]]
        # Seit 29.09.2026 (R5) schreibt die Notiz wie eine Seite: dieselben
        # Blockwerkzeuge; seit G29/3.33.15 auch echte Aufgabenzeilen.
        # Formatieren bleibt über Rechtsklick, Formatleiste und Kürzel.
        assert isinstance(editor, mod.NoteEditor)
        assert labels == ["Überschrift", "Liste", "Nummeriert", f"{app.ICONS['task_open']} Aufgabe", "Zitat", "Code", "Bild", "Mehr"], labels

        # Gismo aktualisiert beim Füttern nur seinen Karteninhalt. Ein kompletter
        # Startseiten-Neuaufbau erzeugte besonders im Dopamin-Design einen
        # sichtbaren weißen Blitz.
        app.settings["design"] = "dopamine"
        app.apply_theme()
        app.set_home_view()
        root.update()
        feed = next(widget for widget in descendants(app.home_content)
                    if isinstance(widget, mod.RoundedButton) and widget.text == "Füttern")
        care_bars = [widget for widget in descendants(feed.master.master)
                     if isinstance(widget, mod.ProgressBar)]
        assert len(care_bars) == 3
        before_satiety = care_bars[0].value
        refreshes = []
        app.refresh_home = lambda: refreshes.append(True)
        feed.command()
        assert care_bars[0].value > before_satiety
        deadline = time.monotonic() + 1.05
        while time.monotonic() < deadline:
            root.update()
            time.sleep(0.01)
        assert care_bars[0].winfo_exists()
        assert refreshes == []
        assert not errors, errors
    finally:
        root.destroy()

print("test_features328: OK")
