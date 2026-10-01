"""Glide 3.29.0: Zeichnung als eigene Listenart im produktiven Bestand (Format 19)."""
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def painted(document):
    cells = bytes.fromhex("".join(document["rows"]))
    return len(cells) - cells.count(0)


with tempfile.TemporaryDirectory(prefix="glide-features329-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features329", str(ROOT / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    drawing_core = mod.glide_drawing
    image_core = mod.glide_drawing_image

    root = mod.tk.Tk()
    errors = []
    root.report_callback_exception = lambda *exc: errors.append(exc)
    app = mod.ListApp(root)
    app.show_error = lambda *args, **kwargs: errors.append(args)
    app.show_warning = lambda *args, **kwargs: errors.append(args)
    app.show_info = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: True
    root.geometry("1280x850+20+20")
    root.update()
    try:
        # ================================================================
        # Vertrag und Typregistrierung
        # ================================================================
        assert mod.APP_VERSION == "3.33.1"
        assert app.DATA_SCHEMA_VERSION == 20
        # Seit dem 26.09.2026 kommt die Seitenart „Seite“ hinzu (test_seiten330).
        # 27.09.2026: dazu die Galerie (test_aufraeumen330).
        assert set(app.LIST_KINDS) == {"tasks", "note", "drawing", "page", "gallery"}
        assert app.LIST_KINDS["drawing"]["accepts_items"] is False
        blank = app.new_list_object("Skizze", [], list_kind="drawing")
        assert blank["list_kind"] == "drawing" and painted(blank["drawing"]) == 0
        assert blank["drawing"]["format"] == "glide.drawing" and len(blank["drawing"]["rows"]) == 128
        assert blank["drawing_reference"] is None
        assert "drawing" not in app.new_list_object("Aufgaben", [])
        for bad in ({"format": "glide.drawing"}, {**blank["drawing"], "rows": blank["drawing"]["rows"][:3]}):
            try:
                app.new_list_object("Kaputt", [], list_kind="drawing", drawing=bad)
            except ValueError:
                pass
            else:
                raise AssertionError("Ungültiges Zellmodell wurde angenommen")
        try:
            app.new_list_object("Mit Punkt", [app.new_item("x")], list_kind="drawing")
        except ValueError:
            pass
        else:
            raise AssertionError("Eine Zeichnung mit Listenpunkten wurde angenommen")
        assert app.new_list_object("Eingang", [], list_kind="drawing", system_role="inbox")["list_kind"] == "tasks"

        # Unbekannte Arten: ab Format 19 sichtbar abgelehnt, ältere Dateien wie bisher.
        future = {"version": 19, "lists": [{"id": "x", "title": "Neu", "list_kind": "hologram", "items": []}]}
        try:
            app.normalize_lists_data(copy.deepcopy(future))
        except ValueError as exc:
            assert "Listenart" in str(exc)
        else:
            raise AssertionError("Unbekannte Listenart wurde still umgedeutet")
        legacy = dict(future, version=18)
        restored_lists, _active = app.normalize_lists_data(copy.deepcopy(legacy))
        assert restored_lists[0]["list_kind"] == "tasks"
        app.load_items()
        root.update()

        # ================================================================
        # Format-18-Migration: unveränderte Sicherung vor dem ersten Schreiben
        # ================================================================
        payload18 = app.data_payload()
        payload18["version"] = 18
        old_bytes = json.dumps(payload18, ensure_ascii=False, indent=4).encode("utf-8")
        Path(mod.SAVE_FILE).write_bytes(old_bytes)
        app._schema19_backup_checked = False
        assert app.save_items()
        migrations = list(Path(mod.BACKUP_DIR).glob("liste_vor_format19_*.json"))
        assert len(migrations) == 1 and migrations[0].read_bytes() == old_bytes
        assert json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))["version"] == 20

        # ================================================================
        # Anlage und eingebettete Zeichenseite
        # ================================================================
        journal = app.new_folder_object("Tagebuch", folder_kind="journal")
        standard = app.new_folder_object("Projekt")
        app.folders.extend([journal, standard])
        app.create_new_drawing(standard["id"])
        root.update()
        entry = app.current_list()
        assert app.is_drawing_list(entry) and entry["folder_id"] == standard["id"]
        editor = app.current_drawing_editor()
        assert editor is not None and editor.winfo_manager() == "pack"
        # Kein Extrafenster: Die Fläche liegt im Inhaltsbereich der Seite.
        assert editor.winfo_toplevel() is root
        assert str(editor).startswith(str(app.list_frame_outer.inner))
        for widget in (app.input_frame, app.search_frame, app.list_frame):
            assert widget.winfo_manager() == "", widget
        assert app.require_list_view(message=False) is False
        assert app.workspace.context() is None
        # Passt die Fläche hinein, gibt es nichts zu scrollen – keine Leisten,
        # kein Verrutschen durch Trackpadgesten beim Zeichnen.
        root.after(150, root.quit)
        root.mainloop()
        assert editor.canvas.xview() == (0.0, 1.0) and editor.canvas.yview() == (0.0, 1.0)
        # Weder Tabelle noch Pinnwand: Die Seite bleibt die Zeichenfläche.
        app.set_table_view()
        app.workspace.set_mode("board")
        root.update()
        assert app.view_mode == "list" and app.current_drawing_editor() is not None

        # Ohne manuelle Wahl folgt der Zoom der Fläche; danach bleibt er fest.
        root.after(150, root.quit)
        root.mainloop()
        assert editor.zoom * 128 <= min(editor.canvas.winfo_width(), editor.canvas.winfo_height())
        editor.change_zoom(1)
        assert editor._auto_zoom is False
        # Pinselvorschau = tatsächlich getroffene Zellen, für alle Größen und Zoomstufen.
        for zoom in (3, 5, 8):
            editor.zoom = zoom
            editor.render_full()
            for size in (1, 2, 4, 8):
                editor.set_brush_size(size)
                u, v = 40.5 + size / 3, 60.0 + size / 7
                editor.show_brush_preview(u, v)
                previewed = {tuple(int(value) // zoom for value in editor.canvas.coords(item)[:2])
                             for item in editor.preview_items}
                assert previewed == set(drawing_core.DrawingModel.brush_cells(u, v, size)), (zoom, size)
                # Dieselbe Bildschirmposition trifft bei jeder Zoomstufe dieselbe Zelle.
                event = SimpleNamespace(x=int(u * zoom - editor.canvas.canvasx(0)),
                                        y=int(v * zoom - editor.canvas.canvasy(0)))
                assert editor.cell_at(editor.logical_point(event)) == (int(u), int(v))
        editor._clear_preview()
        editor.set_brush_size(1)
        editor.zoom = 5
        editor.render_full()

        # Zwanzig schnelle Zelländerungen erzeugen genau einen Schreibvorgang.
        writes = []
        original_write = app.write_json_atomic
        app.write_json_atomic = lambda path, data: (writes.append(path), original_write(path, data))[1]
        editor.set_color("#FF0000")
        for index in range(20):
            editor.cursor = (index, 3)
            editor.apply_at_cursor()
        assert writes == [] and editor.save_state == "unsaved"
        assert editor.flush() and editor.save_state == "saved"
        assert len([path for path in writes if path == mod.SAVE_FILE]) == 1
        stored = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
        saved_entry = next(value for value in stored["lists"] if value["id"] == entry["id"])
        assert painted(saved_entry["drawing"]) == 20 and saved_entry["drawing"]["palette"] == ["#FFFFFF", "#FF0000"]
        # Zoom, Werkzeug und Raster gehören nicht in die Datei.
        assert set(saved_entry) & {"zoom", "tool", "grid"} == set()
        assert set(saved_entry["drawing"]) == {"format", "format_version", "width", "height", "color_space",
                                               "palette_id", "palette_version", "palette", "encoding", "rows"}

        # Ein Schreibfehler überschreibt nichts; der Status bleibt sichtbar.
        before_failure = Path(mod.SAVE_FILE).read_bytes()
        def failing(path, data):
            raise OSError("Datenträger voll")
        app.write_json_atomic = failing
        editor.cursor = (0, 10)
        editor.apply_at_cursor()
        assert editor.flush() is False and editor.save_state == "error"
        assert "fehlgeschlagen" in editor.status.cget("text")
        assert Path(mod.SAVE_FILE).read_bytes() == before_failure
        app.write_json_atomic = original_write
        assert editor.flush() and editor.save_state == "saved"
        assert painted(next(value for value in json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))["lists"]
                            if value["id"] == entry["id"])["drawing"]) == 21

        # Der Verlauf erhält Prüfsummen, keine Zellen, und fasst Autosaves zusammen.
        drawing_events = [value for value in app.history if value["kind"] == "drawing"]
        assert len(drawing_events) == 1 and drawing_events[0]["action"] == "updated"
        assert app.HISTORY_KIND_NAMES["drawing"] == "Zeichnung"
        assert len(app.history_snapshot()["lists"][entry["id"]]["drawing"]) == 64

        # Das Farbspektrum öffnet mit voller Helligkeit, auch wenn Schwarz aktiv
        # ist; die aktuelle Farbe bleibt im Eingabefeld stehen.
        seen = {}
        def inspect_dialog(dialog, parent=None):
            widgets = list(descendants(dialog))
            seen["scales"] = [widget.get() for widget in widgets if isinstance(widget, mod.tk.Scale)]
            seen["entries"] = [widget.get() for widget in widgets if isinstance(widget, mod.tk.Entry)]
            dialog.destroy()
        original_modal = app.run_modal
        app.run_modal = inspect_dialog
        try:
            assert app.drawing_color_dialog("#000000", ["#FFFFFF"]) is None
        finally:
            app.run_modal = original_modal
        assert seen["scales"] == [100] and seen["entries"] == ["#000000"], seen

        # Tastaturweg: Cursor, Pipette, Werkzeugwechsel.
        editor.canvas.focus_force()
        root.update()
        editor.cursor = (0, 3)
        editor.set_tool("eyedropper")
        editor.set_color("#000000")
        editor.apply_at_cursor()
        assert editor.color == "#FF0000"
        editor.move_cursor(1, 0)
        assert editor.cursor == (1, 3)
        editor.set_tool("brush")

        # Punkte finden keinen Weg in die Zeichnung.
        inbox = next(value for value in app.lists if app.is_inbox_list(value))
        assert not app.list_accepts_items(entry)
        app.set_active_list(inbox["id"])
        root.update()
        # Seitenwechsel blendet Eingabe, Suche und Baum wieder ein.
        assert app.input_frame.winfo_manager() == "pack" and app.list_frame.winfo_manager() == "pack"
        assert app.current_drawing_editor() is None
        task = app.new_item("Nicht in die Zeichnung")
        inbox["items"].append(task)
        app.set_active_list(inbox["id"])
        root.update()
        assert app.move_items_to_list([task["id"]], entry["id"]) is False
        assert task in inbox["items"]
        try:
            app.capture_item("Schnell", entry["id"])
        except ValueError:
            pass
        else:
            raise AssertionError("Schnellerfassung legte einen Punkt in einer Zeichnung an")
        assert all(value["id"] != entry["id"] for value in app.workspace.eligible_lists(app.workspace.GLOBAL_SCOPE))

        # Listenart bleibt fest, auch wenn ein alter Dialogwert sie ändern will.
        app._apply_page_details(entry, {"title": "Skizze Projekt", "note": "", "color": None, "labels": [],
                                        "attachments": [], "list_kind": "tasks"})
        assert entry["list_kind"] == "drawing" and entry["title"] == "Skizze Projekt"

        # ================================================================
        # PNG-Referenz als Anhang, Nachzeichnung und Vorher-Snapshot
        # ================================================================
        app.set_active_list(entry["id"])
        root.update()
        editor = app.current_drawing_editor()
        png = Path(folder) / "referenz.png"
        source_image = mod.tk.PhotoImage(master=root, width=64, height=32)
        source_image.put("#00AA00", to=(0, 0, 64, 32))
        source_image.put("#000000", to=(30, 0, 34, 32))
        source_image.write(str(png), format="png")
        attachment = app.store_attachment(str(png))
        choice = {"frame": {"mode": "fit", "zoom_percent": 100, "offset_x": 0, "offset_y": 0}, "trace_model": None}
        document_before_reference = copy.deepcopy(entry["drawing"])
        app._apply_reference_choice(editor, entry, choice, attachment)
        root.update()
        editor = app.current_drawing_editor()
        assert entry["drawing"] == document_before_reference  # Nur als Referenz: Modell unverändert.
        assert entry["drawing_reference"]["attachment_id"] == attachment["id"]
        assert any(value["id"] == attachment["id"] for value in entry["attachments"])
        assert editor.reference_colors is not None and editor.reference_visible
        # Pipette liest auf weißen Zellen die Referenzfarbe, nicht die blasse Darstellung.
        editor.set_tool("eyedropper")
        editor.pick_color(64, 64)
        assert editor.color == "#000000"  # schwarzer Balken in der Bildmitte
        editor.pick_color(10, 40)
        assert editor.color == "#00AA00"
        editor.set_tool("brush")

        # Rahmen- und Nachzeichnungsdialog wirklich aufbauen und bedienen.
        def press(label):
            def run(dialog, parent=None):
                button = next(widget for widget in descendants(dialog)
                              if isinstance(widget, mod.RoundedButton) and widget.text == label)
                button.command()
                if dialog.winfo_exists():
                    dialog.destroy()
            return run
        original_modal = app.run_modal
        source = app.read_reference_png(str(png))
        try:
            app.run_modal = press("Nur als Referenz")
            framed_choice = app.drawing_reference_frame_dialog(source, "referenz.png", None)
            assert framed_choice == {"frame": {"mode": "fill", "zoom_percent": 100, "offset_x": 0, "offset_y": 0},
                                     "trace_model": None}
            app.run_modal = press("Nachzeichnung übernehmen")
            traced = app.drawing_trace_preview_dialog(image_core.render_trace_reference(source, "fit"), True)
            assert traced is not None and len(traced.palette) <= 64 and traced.palette[0] == "#FFFFFF"
            assert any(traced.cells)
            app.run_modal = press("Zurück zum Rahmen")
            assert app.drawing_trace_preview_dialog(image_core.render_trace_reference(source, "fit")) is None
        finally:
            app.run_modal = original_modal

        trace = image_core.quantize_reference(image_core.render_trace_reference(
            app.read_reference_png(str(png)), "fit", 100, 0, 0))
        undo_depth = len(app.undo_stack)
        app._apply_reference_choice(editor, entry, dict(choice, trace_model=trace), None)
        root.update()
        editor = app.current_drawing_editor()
        assert len(app.undo_stack) == undo_depth + 1 and app.undo_stack[-1]["drawing_restore"] == [entry["id"]]
        assert editor.trace_backup == document_before_reference
        assert len(entry["drawing"]["palette"]) <= 64 and entry["drawing"]["palette"][0] == "#FFFFFF"
        # Globales Rückgängig holt den kompletten Vorher-Stand zurück.
        app.undo_last_change()
        root.update()
        entry = next(value for value in app.lists if value["id"] == entry["id"])
        assert entry["drawing"] == document_before_reference

        # Eine unabhängige ältere Aktion nimmt spätere Zellstriche nicht mit zurück.
        app.set_active_list(entry["id"])
        root.update()
        editor = app.current_drawing_editor()
        with app.sidebar_change() as change:
            inbox["note"] = "geändert"
            change.mark()
        editor.set_color("#00FFFF")
        editor.cursor = (100, 100)
        editor.apply_at_cursor()
        editor.flush()
        app.undo_last_change()
        root.update()
        entry = next(value for value in app.lists if value["id"] == entry["id"])
        assert drawing_core.DrawingModel.from_document(entry["drawing"]).color_at(100, 100) == "#00FFFF"
        assert next(value for value in app.lists if value["id"] == inbox["id"])["note"] == ""

        # Fehlende Referenzdatei: sichtbarer Hinweis, Zeichnung unverändert.
        app.set_active_list(entry["id"])
        root.update()
        reference_path = Path(app.resolve_attachment_path(
            next(value for value in entry["attachments"] if value["id"] == entry["drawing_reference"]["attachment_id"])))
        hidden = reference_path.with_suffix(".versteckt")
        reference_path.rename(hidden)
        missing = mod.DrawingEditor(app.list_frame_outer.inner, app, entry)
        assert missing.reference_colors is None and "fehlt" in missing.reference_message
        assert missing.model.to_document() == entry["drawing"]
        missing.destroy()
        hidden.rename(reference_path)

        # ================================================================
        # Duplizieren, Papierkorb, Backups, Austausch und Vorlagen
        # ================================================================
        app.duplicate_list(entry["id"])
        root.update()
        copy_entry = app.current_list()
        assert copy_entry["id"] != entry["id"] and copy_entry["drawing"] == entry["drawing"]
        assert copy_entry["drawing_reference"] == entry["drawing_reference"]

        app.delete_list_by_id(copy_entry["id"])
        root.update()
        trash_entry = next(value for value in app.trash if (value.get("list") or {}).get("id") == copy_entry["id"])
        assert trash_entry["list"]["drawing"] == entry["drawing"]
        app.restore_trash_entry(trash_entry["id"])
        restored = next(value for value in app.lists if value["id"] == copy_entry["id"])
        assert restored["drawing"] == entry["drawing"] and restored["list_kind"] == "drawing"

        partial = app.partial_backup_payload([entry["id"]], [])
        assert partial["lists"][0]["drawing"] == entry["drawing"]
        assert partial["lists"][0]["drawing_reference"] == entry["drawing_reference"]

        backup_path = Path(folder) / "komplett.glidebackup"
        app.flush_rich_note()
        app.write_complete_backup(str(backup_path), app.complete_backup_payload())
        list_count = len(app.lists)
        assert app.import_full_backup(additive=True, path=str(backup_path), show_success=False, confirm=False)
        imported = [value for value in app.lists if value.get("title") == entry["title"] and value["id"] != entry["id"]
                    and app.is_drawing_list(value)]
        assert len(app.lists) > list_count and imported
        for value in imported:
            assert value["drawing"] == entry["drawing"]
            reference = value["drawing_reference"]
            if reference:
                linked = next(item for item in value["attachments"] if item["id"] == reference["attachment_id"])
                assert Path(app.resolve_attachment_path(linked)).read_bytes() == png.read_bytes()

        exchange = app.build_exchange_payload(lists=[entry])
        text = json.dumps(exchange, ensure_ascii=False)
        parsed, report = app.parse_exchange_document(text)
        assert parsed is not None and not report.errors, report.errors
        before_ids = {value["id"] for value in app.lists}
        app.apply_exchange_payload(parsed)
        exchanged = [value for value in app.lists if value["id"] not in before_ids]
        assert exchanged and exchanged[0]["list_kind"] == "drawing" and exchanged[0]["drawing"] == entry["drawing"]
        broken = copy.deepcopy(exchange)
        broken["lists"][0]["drawing"]["rows"][0] = "ZZ"
        assert app.parse_exchange_document(json.dumps(broken))[0] is None

        template = app.capture_template(list_id=entry["id"])
        from_template = app.create_list_from_template(template["id"])
        assert from_template is not None and from_template["list_kind"] == "drawing"
        assert from_template["drawing"] == entry["drawing"]

        # Datei-Austausch: JSON und Glide-SVG verlustfrei, Import legt standardmäßig neu an.
        model = drawing_core.DrawingModel.from_document(entry["drawing"])
        svg_path = Path(folder) / "export.svg"
        json_path = Path(folder) / "export.json"
        app.write_text_atomic(str(svg_path), model.to_svg(entry["title"]))
        app.write_text_atomic(str(json_path), model.to_json() + "\n")
        for path in (svg_path, json_path):
            loaded, warnings = app.read_drawing_file(str(path))
            assert loaded.to_document() == entry["drawing"] and warnings == []
        try:
            app.write_text_atomic(mod.SAVE_FILE, "überschreiben")
        except (OSError, ValueError):
            pass
        else:
            raise AssertionError("Eine Nutzdatendatei wurde als Exportziel akzeptiert")
        original_dialog = mod.filedialog.askopenfilename
        mod.filedialog.askopenfilename = lambda **kwargs: str(svg_path)
        # Seit 3.30 zeigt der Import eine Vorschau (ZF-050); sie wird hier
        # bestätigt, statt auf eine Eingabe zu warten.
        original_modal = app.run_modal
        app.run_modal = press("Als neue Zeichnung")
        try:
            before_ids = {value["id"] for value in app.lists}
            app.import_drawing_as_new()
        finally:
            mod.filedialog.askopenfilename = original_dialog
            app.run_modal = original_modal
        new_pages = [value for value in app.lists if value["id"] not in before_ids]
        assert len(new_pages) == 1 and new_pages[0]["title"] == "export" and new_pages[0]["drawing"] == entry["drawing"]

        # ================================================================
        # Tagebuch: Zeichnung mit Momentdatum in der gemeinsamen Übersicht
        # ================================================================
        app.create_new_drawing(journal["id"])
        root.update()
        journal_drawing = app.current_list()
        assert journal_drawing["journal"]["moment_date"] and journal_drawing["title"].startswith("Zeichnung · ")
        assert app.note_date_header.winfo_manager() == "pack"
        app.set_active_folder(journal["id"])
        root.update()
        rows = [app.tree.item(iid, "text") for iid in app.tree.get_children("")]
        assert any(app.ICONS["drawing"] in row and journal_drawing["title"] in row for row in rows), rows
        app.set_active_folder(standard["id"])
        root.update()
        rows = [app.tree.item(iid, "text") for iid in app.tree.get_children("")]
        assert any("Zellen bemalt" in row for row in rows), rows

        # ================================================================
        # Abnahme ZF-080 / ZF-090 im Einzelnen
        # ================================================================
        entry = next(value for value in app.lists if value["id"] == entry["id"])
        drawing_before_move = copy.deepcopy(entry["drawing"])
        target_folder = app.new_folder_object("Zielordner")
        app.folders.append(target_folder)
        with app.sidebar_change() as change:
            assert app.move_sidebar_list_into_folder(entry["id"], target_folder["id"])
            change.mark()
        entry = next(value for value in app.lists if value["id"] == entry["id"])
        assert entry["folder_id"] == target_folder["id"] and entry["drawing"] == drawing_before_move

        # Teilbackup eines Zweigs: alle Zeichnungen darin, keine fremden Seiten.
        branch = app.partial_backup_payload([], [target_folder["id"]])
        assert {value["id"] for value in branch["lists"]} == {
            value["id"] for value in app.lists if value.get("folder_id") == target_folder["id"]}
        assert entry["id"] in {value["id"] for value in branch["lists"]}

        # Ein beschädigtes Archiv verändert den Bestand nicht.
        import zipfile
        damaged = copy.deepcopy(app.complete_backup_payload())
        next(value for value in damaged["lists"] if value["id"] == entry["id"])["drawing"]["rows"][5] = "00"
        damaged_path = Path(folder) / "beschaedigt.glidebackup"
        with zipfile.ZipFile(damaged_path, "w") as archive:
            archive.writestr("data.json", json.dumps(damaged, ensure_ascii=False))
        lists_before = copy.deepcopy(app.lists)
        error_count = len(errors)
        assert not app.import_full_backup(additive=True, path=str(damaged_path), show_success=False, confirm=False)
        assert app.lists == lists_before and len(errors) == error_count + 1
        del errors[error_count:]

        # Scheitert die unveränderte Vorsicherung, bleibt die alte Datei stehen.
        Path(mod.SAVE_FILE).write_bytes(old_bytes)
        app._schema19_backup_checked = False
        original_copy = mod.shutil.copy2
        def refuse_copy(*args, **kwargs):
            raise OSError("Sicherungsziel nicht beschreibbar")
        mod.shutil.copy2 = refuse_copy
        try:
            assert app.save_items(show_error=False) is False
            assert Path(mod.SAVE_FILE).read_bytes() == old_bytes
        finally:
            mod.shutil.copy2 = original_copy
        assert app.save_items()
        assert json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))["version"] == 20

        # Bestehende Tagebuchnotiz aus Format 18 bleibt nach der Normalisierung gleich.
        reference18 = json.loads((ROOT / "tests/fixtures/current_v18/reference_v18.json").read_text(encoding="utf-8"))
        lists18, _active = app.normalize_lists_data(copy.deepcopy(reference18))
        for key, value in reference18["lists"][0].items():
            assert lists18[0][key] == value, key
        assert "drawing" not in lists18[0]
        app.load_items()
        root.update()

        # Vollbackup → Wiederherstellung in einem leeren, isolierten Datenordner.
        import subprocess
        import sys
        restore_path = Path(folder) / "wiederherstellung.glidebackup"
        app.flush_rich_note()
        app.write_complete_backup(str(restore_path), app.complete_backup_payload())
        expected_drawings = {value["title"]: value["drawing"] for value in app.lists if app.is_drawing_list(value)}
        with tempfile.TemporaryDirectory(prefix="glide-features329-leer-") as empty:
            script = (
                "import importlib.machinery, importlib.util, json, sys\n"
                "loader = importlib.machinery.SourceFileLoader('glide_restore', sys.argv[1])\n"
                "spec = importlib.util.spec_from_loader(loader.name, loader)\n"
                "mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)\n"
                "root = mod.tk.Tk(); root.withdraw(); app = mod.ListApp(root)\n"
                "problems = []\n"
                "app.show_error = lambda *a, **k: problems.append(a); app.show_info = lambda *a, **k: None\n"
                "app.ask_yes_no = lambda *a, **k: True\n"
                "ok = app.import_full_backup(additive=False, path=sys.argv[2], show_success=False, confirm=False)\n"
                "result = {'ok': bool(ok), 'problems': [str(p) for p in problems], 'drawings': {}, 'references': 0}\n"
                "for entry in app.lists:\n"
                "    if entry.get('list_kind') == 'drawing':\n"
                "        result['drawings'][entry['title']] = entry['drawing']\n"
                "        ref = entry.get('drawing_reference')\n"
                "        if ref:\n"
                "            att = next(a for a in entry['attachments'] if a['id'] == ref['attachment_id'])\n"
                "            if open(app.resolve_attachment_path(att), 'rb').read(8) == b'\\x89PNG\\r\\n\\x1a\\n':\n"
                "                result['references'] += 1\n"
                "app.cancel_pending_callbacks(); app.release_data_lock(); root.destroy()\n"
                "print(json.dumps(result))\n"
            )
            environment = dict(os.environ, GLIDE_DATA_DIR=empty)
            completed = subprocess.run([sys.executable, "-c", script, str(ROOT / "src/glide/app.pyw"), str(restore_path)],
                                       env=environment, capture_output=True, text=True, timeout=300)
            assert completed.returncode == 0, completed.stderr
            restored_state = json.loads(completed.stdout.strip().splitlines()[-1])
            assert restored_state["ok"] and not restored_state["problems"], restored_state["problems"]
            assert restored_state["drawings"] == expected_drawings
            assert restored_state["references"] >= 1

        # Referenz-Fixture Format 19 lädt ohne Umdeutung.
        reference19 = json.loads((ROOT / "tests/fixtures/current_v19/reference_v19.json").read_text(encoding="utf-8"))
        assert reference19["version"] == 19
        fixture_lists, _active = app.normalize_lists_data(copy.deepcopy(reference19))
        fixture_drawing = next(value for value in fixture_lists if value["id"] == "fixture-journal-drawing")
        assert fixture_drawing["list_kind"] == "drawing"
        assert fixture_drawing["drawing"] == reference19["lists"][1]["drawing"]
        assert painted(fixture_drawing["drawing"]) == 48 * 48
        app.load_items()
        root.update()

        # Neustart: der bestätigte Stand ist identisch.
        app.flush_rich_note()
        expected = {value["id"]: value.get("drawing") for value in app.lists if app.is_drawing_list(value)}
        app.load_items()
        root.update()
        assert {value["id"]: value.get("drawing") for value in app.lists if app.is_drawing_list(value)} == expected
        assert not errors, errors
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("test_features329: OK")
