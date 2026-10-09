"""Glide 3.30.0: Modernisierung, Pinnwand-Board, Ordner, Planung und Pixel-Werkstatt."""
import base64
import copy
import hashlib
from datetime import datetime as datetime_mod, timedelta as timedelta_mod
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import struct
import tempfile
from types import SimpleNamespace
import zlib

ROOT = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def painted(document):
    cells = bytes.fromhex("".join(document["rows"]))
    return len(cells) - cells.count(0)


def png_size(data):
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", data[16:24])


with tempfile.TemporaryDirectory(prefix="glide-features330-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features330", str(ROOT / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    drawing_core = mod.glide_drawing
    image_core = mod.glide_drawing_image

    root = mod.tk.Tk()
    errors = []
    root.report_callback_exception = lambda *exc: errors.append(exc)
    app = mod.ListApp(root)
    app.confirm_template_preview = lambda template: True
    app.show_error = lambda *args, **kwargs: errors.append(args)
    app.show_warning = lambda *args, **kwargs: errors.append(args)
    app.show_info = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: True
    root.geometry("1280x900+20+20")
    root.update()

    def press(label):
        """Ersetzt run_modal: löst im Dialog die Schaltfläche mit dieser Beschriftung aus."""
        def run(dialog, parent=None):
            root.update()
            button = next(widget for widget in descendants(dialog)
                          if isinstance(widget, mod.RoundedButton) and widget.text.startswith(label))
            button.command()
            if dialog.winfo_exists():
                dialog.destroy()
        return run

    def event_at(editor, x, y, state=0):
        """Ereignis in der Mitte einer Zelle – unabhängig vom Scrollstand."""
        zoom = editor.zoom
        return SimpleNamespace(x=int((x + 0.5) * zoom - editor.canvas.canvasx(0)),
                               y=int((y + 0.5) * zoom - editor.canvas.canvasy(0)), state=state, delta=0)

    def stroke(editor, cells, which="primary", state=0):
        editor._press(event_at(editor, *cells[0], state), which)
        for cell in cells[1:]:
            editor._drag(event_at(editor, *cell, state))
        editor._release()

    try:
        # ================================================================
        # Mitbehoben: Leisten nach Zeichnung, Startseite und Pinnwand
        # ================================================================
        # Bis 3.29 fehlte die Eingabezeile nach Startseite → neue Zeichnung →
        # Startseite dauerhaft, und nach Zeichnung → Pinnwand-Liste stand sie
        # über der Fläche.
        erste = app.new_list_object("Leisten A", [app.new_item("a")])
        zweite = app.new_list_object("Leisten B", [app.new_item("b")])
        app.lists.extend([erste, zweite])
        app.save_items()
        app.set_active_list(zweite["id"])
        root.update()
        grundordnung = list(app.content_frame.pack_slaves())
        assert app.input_frame in grundordnung
        app.set_home_view()
        app.create_new_drawing()
        root.update()
        app.set_home_view()
        root.update()
        app.set_active_list(zweite["id"])
        root.update()
        assert list(app.content_frame.pack_slaves()) == grundordnung
        app.set_active_list(erste["id"])
        app.workspace.set_mode("board")
        app.create_new_drawing()
        root.update()
        app.set_active_list(erste["id"])
        root.update()
        assert app.workspace.visible and app.input_frame.winfo_manager() == ""
        app.workspace.set_mode("list")
        root.update()
        assert list(app.content_frame.pack_slaves()) == grundordnung

        # ================================================================
        # Zeichen-Editor: Kontextleiste, zwei Farben, Aktions-Undo
        # ================================================================
        standard = app.new_folder_object("Werkstatt")
        app.folders.append(standard)
        app.create_new_drawing(standard["id"])
        root.update()
        entry = app.current_list()
        editor = app.current_drawing_editor()
        assert editor is not None and editor.model.width == 128
        assert set(editor.tool_buttons) == {"brush", "fill", "eyedropper", "line", "rect", "ellipse", "select"}
        # Die Kontextleiste zeigt nur, was das Werkzeug braucht.
        editor.set_tool("brush")
        assert set(editor.size_buttons) == {1, 2, 4, 8}
        assert {"pixel_perfect", "wrap", "symmetry_x"} <= set(editor.option_buttons)
        editor.set_tool("fill")
        assert not editor.size_buttons and "pattern_checker" in editor.option_buttons
        editor.set_tool("select")
        assert {"copy", "cut", "paste", "clear", "all"} <= set(editor.option_buttons)
        editor.set_tool("rect")
        assert "filled" in editor.option_buttons and set(editor.size_buttons) == {1, 2, 4, 8}
        editor.set_tool("brush")
        editor.zoom = 5
        editor._auto_zoom = False
        editor.render_full()
        root.update()

        # Linksklick malt Vordergrund, Rechtsklick Hintergrund; ein Zug ist ein Schritt.
        editor.set_color("#FF0000")
        editor.set_color("#0000FF", secondary=True)
        editor.set_brush_size(4)
        stroke(editor, [(10, 10), (20, 10), (30, 10)])
        red = editor.model.palette.index("#FF0000")
        count_red = sum(1 for value in editor.model.cells if value == red)
        assert count_red > 64 and editor.model.undo_count == 1
        assert editor.model.peek_undo().label == "Pinselzug"
        stroke(editor, [(10, 40)], which="secondary")
        blue = editor.model.palette.index("#0000FF")
        assert any(value == blue for value in editor.model.cells)
        editor.undo()
        assert not any(value == blue for value in editor.model.cells)
        editor.undo()
        assert not any(editor.model.cells) and editor.save_state == "unsaved"
        editor.redo()
        assert sum(1 for value in editor.model.cells if value == red) == count_red
        # X tauscht, D setzt Schwarz/Weiß zurück; zuletzt verwendete Farben bleiben.
        editor.swap_colors()
        assert (editor.color, editor.secondary) == ("#0000FF", "#FF0000")
        editor.reset_colors()
        assert (editor.color, editor.secondary) == ("#000000", "#FFFFFF")
        assert app.drawing_tool_settings()["recent_colors"][:2] == ["#0000FF", "#FF0000"]
        root.update()
        # Farbleiste: Klick setzt Vordergrund, Rechtsklick Hintergrund.
        editor.draw_strip()
        assert editor._strip_hits, "Die Farbleiste zeigt keine Farben"
        left, right, strip_color = editor._strip_hits[0]
        editor._strip_click(SimpleNamespace(x=int((left + right) / 2), y=10), "secondary")
        assert editor.secondary == strip_color

        # ================================================================
        # Symmetrie, Formen, Muster, pixelgenaue Linie, Umlauf
        # ================================================================
        editor.model = drawing_core.DrawingModel.blank(128)
        editor.render_full()
        editor.set_symmetry("x")
        editor.set_brush_size(1)
        editor.set_color("#000000")
        stroke(editor, [(5, 5)])
        assert editor.model.color_at(5, 5) == "#000000" and editor.model.color_at(122, 5) == "#000000"
        assert editor.model.undo_count == 1
        editor.set_symmetry("none")
        # Rechteck aufziehen: Vorschau während des Ziehens, ein Schritt beim Loslassen.
        editor.set_tool("rect")
        editor.shape_filled = True
        editor._press(event_at(editor, 40, 40), "primary")
        editor._drag(event_at(editor, 45, 44))
        assert editor.model.color_at(45, 44) == "#000000"  # Vorschau steht bereits im Bild
        editor._drag(event_at(editor, 42, 42))
        assert editor.model.color_at(45, 44) == "#FFFFFF"  # zurückgenommen, als der Zeiger zurückging
        editor._release()
        assert sum(1 for y in range(40, 43) for x in range(40, 43) if editor.model.color_at(x, y) == "#000000") == 9
        assert editor.model.undo_count == 2
        # Escape bricht eine laufende Form ohne Spur ab.
        editor.set_tool("ellipse")
        before = bytes(editor.model.cells)
        editor._press(event_at(editor, 60, 60), "primary")
        editor._drag(event_at(editor, 80, 70))
        editor._escape()
        assert bytes(editor.model.cells) == before and editor.model.undo_count == 2
        # Umschalt beim Aufziehen einer Linie: 45 Grad.
        editor.set_tool("line")
        editor._press(event_at(editor, 10, 100), "primary")
        editor._drag(event_at(editor, 20, 97, state=0x0001))
        editor._release()
        assert editor.model.color_at(20, 100) == "#000000" and editor.model.color_at(15, 100) == "#000000"
        # Füllmuster: Schachbrett aus Vorder- und Hintergrundfarbe.
        editor.model = drawing_core.DrawingModel.blank(16)
        editor.render_full()
        editor.set_tool("fill")
        editor.set_fill_pattern("checker")
        editor.set_color("#00AA00")
        editor.set_color("#FFFF00", secondary=True)
        editor._press(event_at(editor, 3, 3), "primary")
        assert editor.model.color_at(0, 0) == "#00AA00" and editor.model.color_at(1, 0) == "#FFFF00"
        assert editor.model.undo_count == 1
        editor.set_fill_pattern("solid")
        # Pixelgenaue Linie: keine L-Ecken auf einer Diagonale.
        editor.model = drawing_core.DrawingModel.blank(32)
        editor.render_full()
        editor.set_tool("brush")
        editor.set_brush_size(1)
        editor.pixel_perfect = True
        editor.set_color("#000000")
        stroke(editor, [(2, 2), (3, 2), (3, 3), (4, 3), (4, 4), (5, 5)])
        black = {(x, y) for y in range(32) for x in range(32) if editor.model.color_at(x, y) == "#000000"}
        assert black == {(2, 2), (3, 3), (4, 4), (5, 5)}, black
        editor.pixel_perfect = False
        # Über den Rand: Der Tupfer erscheint gegenüber.
        editor.model = drawing_core.DrawingModel.blank(16)
        editor.render_full()
        editor.wrap = True
        editor.set_brush_size(2)
        editor._press(SimpleNamespace(x=int(0.0 * editor.zoom - editor.canvas.canvasx(0)) + 1,
                                      y=int(0.0 * editor.zoom - editor.canvas.canvasy(0)) + 1, state=0), "primary")
        editor._release()
        assert editor.model.color_at(15, 15) == "#000000" or editor.model.color_at(0, 0) == "#000000"
        editor.wrap = False

        # ================================================================
        # Auswahl: aufziehen, kopieren, einfügen, verschieben, leeren
        # ================================================================
        editor.model = drawing_core.DrawingModel.blank(32)
        editor.render_full()
        editor.model.paint_shape("rect_filled", 2, 2, 4, 4, 1, "#AA0000")
        editor.render_full()
        editor.set_tool("select")
        editor._press(event_at(editor, 2, 2), "primary")
        editor._drag(event_at(editor, 4, 4))
        editor._release()
        assert editor.selection == (2, 2, 4, 4)
        editor.copy_selection()
        assert app.drawing_clipboard.width == 3 and set(app.drawing_clipboard.colors) == {"#AA0000"}
        editor.selection = None
        editor.cursor = (20, 20)
        editor.paste_clipboard()
        assert editor.model.color_at(22, 22) == "#AA0000" and editor.selection == (20, 20, 22, 22)
        undo_before_move = editor.model.undo_count
        editor._press(event_at(editor, 21, 21), "primary")
        editor._drag(event_at(editor, 26, 21))
        editor._release()
        assert editor.model.color_at(25, 20) == "#AA0000" and editor.model.color_at(20, 20) == "#FFFFFF"
        assert editor.model.undo_count == undo_before_move + 1 and editor.selection == (25, 20, 27, 22)
        editor.clear_selection()
        assert editor.model.color_at(26, 21) == "#FFFFFF"
        editor._escape()
        assert editor.selection is None

        # ================================================================
        # Zoom mit Strg+Mausrad, Vorschau, Graustufen, Referenzdeckkraft
        # ================================================================
        editor.model = drawing_core.DrawingModel.blank(128)
        editor.render_full()
        zoom_before = editor.zoom
        editor._wheel_zoom(SimpleNamespace(x=40, y=40, delta=120))
        assert editor.zoom > zoom_before and editor._auto_zoom is False
        editor._wheel_zoom(SimpleNamespace(x=40, y=40, delta=-120))
        assert editor.zoom == zoom_before
        editor.preview_visible = False
        editor.toggle_preview()
        root.update()
        editor._render_preview()
        assert editor.preview_panel.winfo_manager() == "grid" and len(editor._preview_images) == 2
        editor.toggle_tiled()
        editor._render_preview()
        assert len(editor.preview_canvas.find_all()) == 9
        editor.toggle_tiled()
        editor.toggle_preview()
        assert editor.preview_panel.winfo_manager() == ""
        # Graustufen verändern nur die Anzeige.
        editor.model.set_cell(0, 0, "#FF0000")
        editor.toggle_grayscale()
        shown = editor._base.get(0, 0)
        assert len(set(shown[:3])) == 1 and editor.model.color_at(0, 0) == "#FF0000"
        editor.toggle_grayscale()

        # ================================================================
        # Flächengrößen, PNG-Export, Paletten, Farbe ersetzen, Zwischenstände
        # ================================================================
        for size in (16, 32, 64):
            app.create_new_drawing(standard["id"], size=size)
            root.update()
            small = app.current_drawing_editor()
            assert small.model.width == size
            assert small.zoom * size <= min(small._visible_size())
            assert app.current_list()["drawing"]["format_version"] == 2
        small_entry = app.current_list()
        small.set_tool("brush")
        small.set_brush_size(1)
        small.set_color("#123456")
        small.cursor = (1, 1)
        small.apply_at_cursor()
        assert small.flush()
        # PNG in ganzzahligen Größen.
        target_png = Path(folder) / "export.png"
        original_save = mod.filedialog.asksaveasfilename
        mod.filedialog.asksaveasfilename = lambda **kwargs: str(target_png)
        try:
            app.drawing_export_png(small, 4)
        finally:
            mod.filedialog.asksaveasfilename = original_save
        assert png_size(target_png.read_bytes()) == (256, 256)
        exported = mod.tk.PhotoImage(master=root, file=str(target_png))
        assert exported.get(4, 4)[:3] == (0x12, 0x34, 0x56) and exported.get(0, 0)[:3] == (255, 255, 255)
        # Eigene Palette importieren, wählen und wieder exportieren.
        gpl = Path(folder) / "meer.gpl"
        gpl.write_text("GIMP Palette\nName: Meer\n0 64 128 Tief\n0 128 255 Hell\n", encoding="utf-8")
        original_open = mod.filedialog.askopenfilename
        mod.filedialog.askopenfilename = lambda **kwargs: str(gpl)
        try:
            app.drawing_import_palette(small)
        finally:
            mod.filedialog.askopenfilename = original_open
        tools = app.drawing_tool_settings()
        assert tools["palettes"][-1]["name"] == "Meer" and tools["palette"] == tools["palettes"][-1]["id"]
        assert [color for _left, _right, color in small._strip_hits][-2:] == ["#004080", "#0080FF"]
        assert app.drawing_palette(drawing_core.GLIDE_PALETTE_ID)[2][5] == "#1E88E5"
        # Farbe in der ganzen Zeichnung ersetzen: ein Rückgängig-Schritt.
        original_color_dialog = app.drawing_color_dialog
        app.drawing_color_dialog = lambda *args, **kwargs: "#654321"
        try:
            steps = small.model.undo_count
            app.drawing_replace_color(small, "#123456")
        finally:
            app.drawing_color_dialog = original_color_dialog
        assert small.model.color_at(1, 1) == "#654321" and small.model.undo_count == steps + 1
        assert small.model.unused_palette_count() == 1
        app.drawing_compact_palette(small)
        assert small.model.palette == ["#FFFFFF", "#654321"]
        # Zwischenstand merken, weitermalen, wiederherstellen.
        app.themed_input_dialog = lambda *args, **kwargs: "Erster Entwurf"
        app.drawing_snapshot_save(small)
        snapshots = app.drawing_snapshots(small_entry)
        assert len(snapshots) == 1 and snapshots[0]["mime"] == app.DRAWING_SNAPSHOT_MIME
        assert app.read_drawing_snapshot(snapshots[0]).color_at(1, 1) == "#654321"
        small.cursor = (5, 5)
        small.apply_at_cursor()
        assert small.flush()
        original_modal = app.run_modal
        app.run_modal = press("Wiederherstellen")
        try:
            app.drawing_snapshot_dialog(small)
        finally:
            app.run_modal = original_modal
        root.update()
        assert drawing_core.DrawingModel.from_document(small_entry["drawing"]).color_at(5, 5) == "#FFFFFF"
        app.undo_last_change()
        root.update()
        # Rückgängig ersetzt den Bestand durch den gesicherten Stand – neu nachschlagen.
        small_entry = next(value for value in app.lists if value["id"] == small_entry["id"])
        assert drawing_core.DrawingModel.from_document(small_entry["drawing"]).color_at(5, 5) == "#123456"
        # Zwischenstände reisen als Anhänge mit (kein neues Datenfeld).
        assert {key for key in app.drawing_snapshots(small_entry)[0]} == {
            "id", "name", "storage", "size", "mime", "added_at"}
        # Einfügen aus Text mit Vorschau: als neue Zeichnung.
        text_model = drawing_core.DrawingModel.blank(16)
        text_model.set_cell(0, 0, "#ABCDEF")
        root.clipboard_clear()
        root.clipboard_append(text_model.to_svg("Aus Text"))
        lists_before = len(app.lists)
        app.run_modal = press("Als neue Zeichnung")
        try:
            app.drawing_paste_text(app.current_drawing_editor())
        finally:
            app.run_modal = original_modal
        assert len(app.lists) == lists_before + 1
        pasted = app.current_list()
        assert drawing_core.DrawingModel.from_document(pasted["drawing"]).color_at(0, 0) == "#ABCDEF"
        root.clipboard_clear()
        root.clipboard_append("kein Glide")
        failures = len(errors)
        app.drawing_paste_text(app.current_drawing_editor())
        assert len(errors) == failures + 1 and len(app.lists) == lists_before + 1
        errors.clear()

        # ================================================================
        # Format 20: Migration mit Vorsicherung, neue Felder, Bereinigung
        # ================================================================
        assert app.DATA_SCHEMA_VERSION == 23
        payload19 = app.data_payload()
        payload19["version"] = 19
        old_bytes = json.dumps(payload19, ensure_ascii=False, indent=4).encode("utf-8")
        Path(mod.SAVE_FILE).write_bytes(old_bytes)
        app._schema20_backup_checked = False
        assert app.save_items()
        backups20 = list(Path(mod.BACKUP_DIR).glob("liste_vor_format20_*.json"))
        assert len(backups20) == 1 and backups20[0].read_bytes() == old_bytes
        assert json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))["version"] == 23
        # Eine Datei aus einer späteren Glide-Fassung wird abgelehnt.
        future_version = app.DATA_SCHEMA_VERSION + 1
        try:
            app.normalize_lists_data({"version": future_version, "lists": []})
        except ValueError:
            pass
        else:
            raise AssertionError(f"Unbekanntes Format {future_version} wurde angenommen")
        # Neue Punktfelder werden streng normalisiert.
        plain = app.new_item("Planung", planned_date="2026-10-01", planned_time="9.30",
                             links=["a", "a", 7, "b"], blocked_by=["c"], time_spent_minutes=45)
        assert plain["planned_time"] == "09:30" and plain["links"] == ["a", "b"]
        assert plain["blocked_by"] == ["c"] and plain["time_spent_minutes"] == 45
        assert app.new_item("Ohne Tag", planned_time="10:00")["planned_time"] is None
        heading = app.new_item("Kapitel", kind=app.ITEM_KIND_HEADING, blocked_by=["x"], time_spent_minutes=5)
        assert heading["blocked_by"] == [] and heading["time_spent_minutes"] is None
        assert app.new_item("Negativ", time_spent_minutes=-4)["time_spent_minutes"] is None
        # Listen und Ordner tragen Pixelsymbol und Archiv; defekte Symbole fallen weg.
        icon = drawing_core.DrawingModel.blank(16)
        icon.set_cell(3, 3, "#1E88E5")
        page = app.new_list_object("Mit Symbol", [], icon=icon.to_document(), archived=True)
        assert page["icon"]["width"] == 16 and page["archived"] is True and page["archived_at"]
        assert app.new_list_object("Kaputt", [], icon={"format": "x"})["icon"] is None
        assert app.new_list_object("Groß", [], icon=drawing_core.DrawingModel.blank(32).to_document())["icon"] is None
        assert app.new_list_object("Eingang", [], system_role="inbox", archived=True)["archived"] is False
        assert app.new_folder_object("Ordner", icon=icon.to_document())["icon"]["width"] == 16

        # ================================================================
        # Verknüpfungen und echte Abhängigkeiten
        # ================================================================
        plan = app.new_list_object("Projektplan", [])
        app.lists.append(plan)
        entwurf = app.new_item("Entwurf schreiben")
        freigabe = app.new_item("Freigabe einholen")
        druck = app.new_item("Druck beauftragen")
        notiz = app.new_item("Besprechungsnotiz", kind=app.ITEM_KIND_LONG)
        plan["items"].extend([entwurf, freigabe, druck, notiz])
        app.set_active_list(plan["id"])
        root.update()
        assert app.add_item_relation(freigabe["id"], "blocked_by", [entwurf["id"]])
        assert app.add_item_relation(druck["id"], "blocked_by", [freigabe["id"]])
        assert app.add_item_relation(notiz["id"], "links", [entwurf["id"], druck["id"]])
        assert app.dependency_creates_cycle(entwurf["id"], druck["id"])
        before_warnings = len(errors)
        assert app.add_item_relation(entwurf["id"], "blocked_by", [druck["id"]]) is False
        assert len(errors) == before_warnings + 1 and "Kreis" in errors[-1][1]
        del errors[before_warnings:]
        index = app.item_index()
        assert [item["id"] for _entry, item in app.item_backlinks(entwurf["id"], index)] == [notiz["id"]]
        assert [item["id"] for _entry, item in app.item_dependents(freigabe["id"], index)] == [druck["id"]]
        assert app.is_blocked(druck, index) and not app.is_blocked(entwurf, index)
        # Die Liste zeigt „wartet“ und die Zahl der Verknüpfungen.
        app.refresh_tree()
        assert app.ICONS["blocked"] in app.tree.item(druck["id"], "text")
        assert f"{app.ICONS['link']} 2" in app.tree.item(notiz["id"], "text")
        # Abhaken eines wartenden Punkts fragt nach; „Nein“ lässt ihn offen.
        app.ask_yes_no = lambda *args, **kwargs: False
        app.tree.selection_set(druck["id"])
        app.toggle_done()
        assert druck["done"] is False
        app.ask_yes_no = lambda *args, **kwargs: True
        app.toggle_done()
        assert druck["done"] is True
        druck["done"] = False
        # Nächste Aufgabe überspringt wartende Punkte.
        assert app.task_urgency_rank(druck)[0] == 4 and app.task_urgency_rank(entwurf)[0] == 3
        # Erledigte Voraussetzung gibt frei.
        entwurf["done"] = True
        assert not app.is_blocked(freigabe)
        entwurf["done"] = False
        # Kopieren zieht Verweise innerhalb der Kopie nach, Verweise nach außen bleiben.
        mapping = {}
        copies = app.copy_items_with_new_ids([entwurf, freigabe], mapping=mapping)
        assert copies[1]["blocked_by"] == [mapping[entwurf["id"]]]
        outside = app.copy_items_with_new_ids([druck])
        assert outside[0]["blocked_by"] == [freigabe["id"]]
        # Beim Laden fallen tote Verweise weg; Kreise aus Handarbeit werden getrennt.
        broken = copy.deepcopy(app.data_payload())
        broken_plan = next(value for value in broken["lists"] if value["id"] == plan["id"])
        for value in broken_plan["items"]:
            if value["id"] == entwurf["id"]:
                value["blocked_by"] = [druck["id"]]
                value["links"] = ["gibt-es-nicht"]
        lists_after, _active = app.normalize_lists_data(broken)
        reloaded = {item["id"]: item for value in lists_after for item in app.walk_items(value["items"])}
        assert reloaded[entwurf["id"]]["links"] == []
        chain = [reloaded[entwurf["id"]]["blocked_by"], reloaded[freigabe["id"]]["blocked_by"],
                 reloaded[druck["id"]]["blocked_by"]]
        assert sum(1 for value in chain if value) == 2, chain
        app.load_items()
        root.update()
        plan = next(value for value in app.lists if value["id"] == plan["id"])
        entwurf, freigabe, druck, notiz = plan["items"]
        # Verknüpfungen reisen durch den additiven Import mit neuen Kennungen.
        exported = copy.deepcopy([plan])
        new_lists, _new_folders, _labels = app.prepare_additive_import(exported, [], copy.deepcopy(app.labels))
        imported_items = new_lists[0]["items"]
        imported_ids = {item["id"] for item in imported_items}
        assert imported_items[3]["links"] and set(imported_items[3]["links"]) <= imported_ids
        assert imported_items[2]["blocked_by"] == [imported_items[1]["id"]]

        # ================================================================
        # Zeiterfassung: starten, im Kopf zeigen, buchen
        # ================================================================
        app.set_active_list(plan["id"])
        root.update()
        assert app.start_time_tracking(entwurf["id"])
        root.update()
        assert app.running_timer()["item_id"] == entwurf["id"]
        assert app.timer_button.winfo_manager() == "pack"
        started = datetime_mod.fromisoformat(app.running_timer()["started_at"])
        booked = app.stop_time_tracking(now=started + timedelta_mod(seconds=125))
        entwurf = app.find_item_in_lists(entwurf["id"])[0]
        assert booked == 3 and entwurf["time_spent_minutes"] == 3
        assert app.running_timer() is None and app.timer_button.winfo_manager() == ""
        # Ein zweiter Start bucht die laufende Erfassung vorher.
        app.start_time_tracking(entwurf["id"])
        app.settings["time_tracking"]["started_at"] = (
            datetime_mod.now().astimezone() - timedelta_mod(minutes=10)).isoformat(timespec="seconds")
        app.start_time_tracking(freigabe["id"])
        assert app.find_item_in_lists(entwurf["id"])[0]["time_spent_minutes"] >= 13
        app.stop_time_tracking()
        # Die Maske übernimmt Uhrzeit, Zeit, Verknüpfungen und Voraussetzungen.
        details = {"text": "Druck beauftragen", "planned_date": "2026-10-02", "planned_time": "14:15",
                   "time_spent_minutes": 30, "links": [notiz["id"]], "blocked_by": [], "labels": []}
        target = app.find_item_in_lists(druck["id"])[0]
        assert app.apply_item_details(target, details)
        assert (target["planned_time"], target["time_spent_minutes"], target["links"], target["blocked_by"]) == \
            ("14:15", 30, [notiz["id"]], [])
        assert app.apply_item_details(target, dict(details, planned_date=None)) and target["planned_time"] is None
        # Der Verlauf nennt die neuen Felder mit Namen.
        assert app.HISTORY_FIELD_NAMES["blocked_by"] == "Abhängigkeiten"

        # ================================================================
        # Pixelsymbol (AO-050), Archiv (MO-070), Galerie-Übersicht (AO-010)
        # ================================================================
        symbol = drawing_core.DrawingModel.blank(16)
        symbol.paint_shape("rect_filled", 4, 4, 11, 11, 1, "#1E88E5")
        app.run_modal = lambda dialog, parent=None: (root.update(), next(
            widget for widget in descendants(dialog)
            if isinstance(widget, mod.DrawingEditor)).replace_model(symbol.copy()),
            press("Übernehmen")(dialog))
        try:
            assert app.page_icon_dialog("list", plan["id"])
        finally:
            app.run_modal = original_modal
        plan = next(value for value in app.lists if value["id"] == plan["id"])
        assert plan["icon"]["width"] == 16 and painted(plan["icon"]) == 64
        app.update_sidebar_list()
        assert app.sidebar_listbox.item(f"list:{plan['id']}", "image")
        # Aus einer Zeichnung übernehmen: Verkleinerung nach Mehrheitsfarbe.
        big = drawing_core.DrawingModel.blank(128)
        big.paint_shape("rect_filled", 0, 0, 127, 63, 1, "#FF4F9A")
        assert big.downscaled(16).color_at(0, 0) == "#FF4F9A" and big.downscaled(16).color_at(0, 15) == "#FFFFFF"
        # Ordner archivieren nimmt seinen Zweig aus Seitenleiste und Planung.
        archive_folder = app.new_folder_object("Altprojekt")
        app.folders.append(archive_folder)
        archived_list = app.new_list_object("Alte Aufgaben", [app.new_item("Alt und fällig", due=mod.date.today().isoformat(),
                                                                           planned_date=mod.date.today().isoformat())],
                                            folder_id=archive_folder["id"])
        app.lists.append(archived_list)
        app.save_items()
        app.update_sidebar_list()
        before_plan = len(app.plan_day_entries(apply_filters=False))
        assert app.set_archived("folder", archive_folder["id"], True)
        root.update()
        assert app.is_archived_entry(archived_list) and archive_folder["archived_at"]
        assert not app.sidebar_listbox.exists(f"folder:{archive_folder['id']}")
        assert len(app.plan_day_entries(apply_filters=False)) == before_plan - 1
        assert all(entry["id"] != archived_list["id"] for _due, _li, _ii, entry, _item in app.get_in_progress_items(False))
        assert ("folder", archive_folder) in app.archived_entries()
        # Die Übersicht zeigt das Archiv auf Wunsch; „Zurückholen“ stellt es wieder her.
        app.set_library_view()
        root.update()
        assert all(entry["id"] != archive_folder["id"] for _kind, entry in app.library_entries())
        app.toggle_library_archive()
        root.update()
        assert [entry["id"] for _kind, entry in app.library_entries(archived=True)] == [archive_folder["id"]]
        restore_menu = app.build_folder_menu(archive_folder['id'])
        index = next(i for i in range(restore_menu.index('end') + 1)
                     if restore_menu.type(i) == 'command' and restore_menu.entrycget(i, 'label') == 'Aus Archiv zurückholen')
        restore_menu.invoke(index)
        root.update()
        assert archive_folder["archived"] is False and not app.is_archived_entry(archived_list)
        app.toggle_library_archive()
        # Kartengröße wechselt und bleibt in den Einstellungen.
        app.cycle_library_card_size()
        assert app.settings["library_card_size"] == "large"
        app.cycle_library_card_size()
        app.cycle_library_card_size()
        assert app.settings["library_card_size"] == "medium"
        # Zeichnungen erscheinen in der Übersicht mit Miniatur statt Zahlen.
        root.update()
        assert any(isinstance(image, mod.tk.PhotoImage) for image in app._library_images)
        # Der Eingang lässt sich nicht archivieren.
        inbox = next(value for value in app.lists if app.is_inbox_list(value))
        assert app.set_archived("list", inbox["id"], True) is False

        # ================================================================
        # Pfadzeile (MO-020), Rückgängig im Hinweis (MO-040), Suche (MO-010)
        # ================================================================
        eltern = app.new_folder_object("Kunden")
        kind_ordner = app.new_folder_object("Nord", parent_id=eltern["id"])
        app.folders.extend([eltern, kind_ordner])
        tief = app.new_list_object("Angebote Nord", [app.new_item("Angebot schreiben")], folder_id=kind_ordner["id"])
        app.lists.append(tief)
        # Seit 27.09.2026 ohne Ordnerpfad über dem Titel: Eine Liste im
        # Unterordner steht exakt dort, wo jede andere Liste steht.
        oben_liste = next(entry for entry in app.lists if not entry.get("folder_id")
                          and entry.get("list_kind", "tasks") == "tasks")
        app.set_active_list(oben_liste["id"])
        root.update()
        titel_y = app.title_label.winfo_rooty()
        app.set_active_list(tief["id"])
        root.update()
        assert app.path_row.winfo_manager() == "" and not app.path_row.winfo_children()
        assert app.title_label.winfo_rooty() == titel_y, "kein Versatz durch Ordnerpfad"
        # Rückgängig im Hinweis: nimmt genau die gemeldete Aktion zurück.
        app.set_active_list(tief["id"])
        root.update()
        punkt = tief["items"][0]
        app.tree.selection_set(punkt["id"])
        app.toggle_done()
        root.update()
        assert punkt["done"] is True and app.undo_toast_valid()
        knopf = app._undo_toast["button"]
        knopf.command()
        root.update()
        tief = next(value for value in app.lists if value["id"] == tief["id"])
        assert tief["items"][0]["done"] is False and app._undo_toast is None
        # Nach einer weiteren Änderung gilt der Hinweis nicht mehr.
        app.set_active_list(tief["id"])
        root.update()
        app.tree.selection_set(tief["items"][0]["id"])
        app.toggle_done()
        app.snapshot_undo()
        assert not app.undo_toast_valid()
        app.hide_undo_toast()
        # Seiten- und Befehlssuche: Seiten, Punkte, Aktionen; Umlaute gleichwertig.
        assert app.search_key("Übersicht Größe") == "uebersicht groesse"
        treffer = app.quick_open_results("angeb")
        gruppen = [value["group"] for value in treffer]
        assert "Seiten" in gruppen and "Punkte" in gruppen
        assert treffer[0]["title"] == "Angebote Nord"
        assert any(value["group"] == "Aktionen" and value["title"] == "Neue Zeichnung"
                   for value in app.quick_open_results("zeichn"))
        leer = app.quick_open_results("")
        assert leer[0]["group"] == "Zuletzt geöffnet" and leer[0]["title"] == "Angebote Nord"
        app.show_quick_open()
        root.update()
        panel = app._quick_open["panel"]
        assert panel.winfo_toplevel() is root  # eingebettet, kein Zusatzfenster
        app._quick_open["entry"].insert(0, "Kunden")
        # Tastenereignisse erreichen nur das fokussierte Feld – auch dann, wenn
        # ein anderes Programm vorn liegt.
        app._quick_open["entry"].focus_force()
        root.update()
        app._quick_open["entry"].event_generate("<Return>")
        root.update()
        assert app._quick_open is None and app.view_mode == "folder" and app.active_folder_id == eltern["id"]
        # Ein Punkt als Treffer öffnet seine Liste und wählt ihn aus.
        punkt_treffer = next(value for value in app.quick_open_results("Angebot schreiben") if value["group"] == "Punkte")
        app.open_quick_result(punkt_treffer)
        root.update()
        assert app.active_list_id == tief["id"] and app.tree.selection() == (tief["items"][0]["id"],)
        assert "Seite, Punkt oder Aktion suchen …" in {entry["label"] for entry in app.app_action_entries()}
        assert not [entry for entry in app.app_action_entries() if entry["group"] == "Weitere Aktionen"]

        # ================================================================
        # Tagesbeginn, Wochenrückblick, Kapazität je Wochentag, Erledigt-Datum
        # ================================================================
        heute = mod.date.today()
        gestern = (heute - mod.timedelta(days=1)).isoformat()
        tagesliste = app.new_list_object("Tagesbeginn", [
            app.new_item("Überfällig", due=gestern),
            app.new_item("Verschleppt", planned_date=gestern),
            app.new_item("Schon heute", due=gestern, planned_date=heute.isoformat()),
        ])
        app.lists.append(tagesliste)
        eingang = next(value for value in app.lists if app.is_inbox_list(value))
        eingang["items"].append(app.new_item("Idee aus dem Eingang"))
        app.save_items()
        queue = app.day_review_queue()
        titles = [app.find_item_in_lists(step["item_id"])[0]["text"] for step in queue]
        assert titles.index("Überfällig") < titles.index("Verschleppt") < titles.index("Idee aus dem Eingang")
        assert "Schon heute" not in titles
        app.start_day_review()
        root.update()
        assert app.view_mode == app.HOME_VIEW and app.home_mode() == "day_review"
        assert app.get_display_title() == "Tagesbeginn"
        assert app.template_actions.winfo_manager() == "pack"
        state = app._day_review
        first = app.find_item_in_lists(state["queue"][0]["item_id"])[0]
        app.day_review_decide("today")
        assert first["planned_date"] == heute.isoformat()
        second = app.find_item_in_lists(state["queue"][1]["item_id"])[0]
        app.day_review_decide("next_week")
        assert second["planned_date"] == app.next_week_start(heute).isoformat()
        while app._day_review["index"] < len(app._day_review["queue"]):
            app.day_review_decide("skip")
        root.update()
        assert app._day_review["counts"]["today"] == 1 and app._day_review["counts"]["later"] == 1
        assert any(isinstance(widget, mod.tk.Label) and "abgeschlossen" in str(widget.cget("text"))
                   for widget in descendants(app.home_content))
        # Erledigt-Datum: beim Abhaken gesetzt, beim Wiederöffnen geleert.
        erledigt = app.find_item_in_lists(first["id"])[0]
        erledigt["done"] = True
        app.save_items()
        erledigt = app.find_item_in_lists(first["id"])[0]
        assert erledigt["done_at"] and erledigt["done_at"][:10] == heute.isoformat()
        erledigt["done"] = False
        app.save_items()
        assert app.find_item_in_lists(first["id"])[0]["done_at"] is None
        erledigt = app.find_item_in_lists(first["id"])[0]
        erledigt["done"] = True
        erledigt["time_spent_minutes"] = 20
        erledigt["estimated_minutes"] = 30
        app.save_items()
        # Wochenrückblick: Erledigtes der Woche, Weitergewandertes, Zeit, Kapazität je Tag.
        app.settings["daily_capacity_minutes"] = 240
        profil = [None] * 7
        profil[heute.weekday()] = 60
        app.settings["daily_capacity_by_weekday"] = profil
        assert app.daily_capacity_minutes(heute.isoformat()) == 60 and app.daily_capacity_minutes() == 240
        normalized = app.normalize_personal_settings({"daily_capacity_by_weekday": [30, "x", None, 99999, -3, 1, 2]})
        assert normalized["daily_capacity_by_weekday"] == [30, None, None, app.DAILY_CAPACITY_MAX, 0, 1, 2]
        daten = app.week_review_data(0)
        assert any(item["id"] == first["id"] for _entry, item in daten["done_items"])
        assert daten["spent"] >= 20 and daten["estimate"] >= 30
        assert daten["rows"][heute.isoformat()]["capacity"] == 60
        assert any(item["text"] == "Verschleppt" for _entry, item in daten["carried"]) or \
            app.find_item_in_lists(second["id"])[0]["planned_date"] > heute.isoformat()
        app.show_week_review()
        root.update()
        assert app.get_display_title() == "Wochenrückblick"
        app.show_week_review(offset=-1)
        root.update()
        assert app._week_offset == -1
        app.set_home_view()
        root.update()
        assert app.home_mode() == "tiles" and app.template_actions.winfo_manager() == ""

        # ================================================================
        # Startseite direkt anpassen, angeheftete Seiten und Filter (ST-010…040)
        # ================================================================
        # Eine bestehende Startseite aus 3.29 bleibt nach dem Update gleich:
        # Die neuen Kacheln sind aus, bis jemand sie einblendet.
        alt = app.normalize_personal_settings({"home_tile_order": ["welcome", "today"], "home_tiles_hidden": []})
        assert {"drawings", "pinned", "filters"} <= set(alt["home_tiles_hidden"]) and alt["home_tiles_330"] is True
        frisch = app.normalize_personal_settings({})
        assert "drawings" not in frisch["home_tiles_hidden"] and frisch["home_tiles_330"] is True
        wieder = app.normalize_personal_settings(dict(alt, home_tiles_hidden=[]))
        assert wieder["home_tiles_hidden"] == []  # nur einmal ausblenden, danach entscheidet die Person
        bereinigt = app.normalize_personal_settings({
            "pinned_pages": [{"kind": "list", "id": "a"}, {"kind": "list", "id": "a"}, {"kind": "x", "id": "b"},
                             "kaputt", {"kind": "folder", "id": ""}],
            "home_tile_span": {"today": "wide", "unbekannt": "wide", "week": "normal"},
            "saved_filters": [{"id": "f1", "name": "Eins"}],
            "home_filter_tiles": ["f1", "f1", "fehlt"]})
        assert bereinigt["pinned_pages"] == [{"kind": "list", "id": "a"}]
        assert bereinigt["home_tile_span"] == {"today": "wide"}
        assert bereinigt["home_filter_tiles"] == ["f1"] and bereinigt["sidebar_sections_closed"] == []
        assert app.normalize_personal_settings({"sidebar_sections_closed": ["views", "x", "views", "pinned"]})[
            "sidebar_sections_closed"] == ["views", "pinned"]

        app.settings["home_tiles_hidden"] = []
        app.settings["home_tile_order"] = []
        zeichnung_start = app.create_new_drawing(size=16)
        assert zeichnung_start is not None
        app.set_home_view()
        root.update()
        texte = {str(widget.cget("text")) for widget in descendants(app.home_content)
                 if isinstance(widget, mod.tk.Label)}
        assert any("Zeichnungen" in text for text in texte) and any("Angeheftet" in text for text in texte)
        assert app._home_drawing_images
        # Anheften: Liste und Ordner, Reihenfolge, Grenze, Archiv fällt heraus.
        anheft_liste = app.new_list_object("Wichtige Seite", [app.new_item("Etwas")])
        app.lists.append(anheft_liste)
        app.save_items()
        assert app.set_pinned("list", anheft_liste["id"]) and app.set_pinned("folder", eltern["id"])
        assert app.is_pinned("list", anheft_liste["id"])
        assert [holder["id"] for _kind, holder in app.pinned_pages()] == [anheft_liste["id"], eltern["id"]]
        root.update()
        assert app.pinned_sidebar_frame.winfo_manager() == "pack"
        assert len(app.pinned_sidebar_rows) == 2
        # Der Block steht direkt unter den Systemzeilen, vor dem Listenbaum.
        assert app.pinned_sidebar_frame.winfo_y() > app.system_listbox.winfo_y()
        assert app.pinned_sidebar_frame.winfo_y() < app.sidebar_listbox.winfo_y()
        (_row_key, zeile) = app.pinned_sidebar_rows[1]
        zeile.event_generate("<Button-1>")
        root.update()
        assert app.view_mode == "folder" and app.active_folder_id == eltern["id"]
        assert app.move_pinned("folder", eltern["id"], -1)
        assert app.pinned_pages()[0][1]["id"] == eltern["id"]
        app.toggle_pinned_sidebar()
        root.update()
        assert app.pinned_sidebar_rows == [] and "pinned" in app.settings["sidebar_sections_closed"]
        app.toggle_pinned_sidebar()
        app.set_archived("list", anheft_liste["id"], True)
        assert [holder["id"] for _kind, holder in app.pinned_pages()] == [eltern["id"]]
        app.set_archived("list", anheft_liste["id"], False)
        voll = [{"kind": "list", "id": f"x{index}"} for index in range(app.MAX_PINNED_PAGES)]
        app.settings["pinned_pages"] = voll
        assert app.set_pinned("list", anheft_liste["id"]) is True  # tote Einträge zählen nicht mit
        assert all(value["id"] in {anheft_liste["id"]} or not value["id"].startswith("x")
                   for value in app.settings["pinned_pages"])
        app.set_pinned("list", anheft_liste["id"], False)
        app.set_pinned("folder", eltern["id"], False)
        root.update()
        assert app.pinned_sidebar_frame.winfo_manager() == ""
        # Kontextmenüs von Liste und Ordner bieten „Anheften“ bzw. „Lösen“.
        def menu_labels(menu):
            return [menu.entrycget(index, "label") for index in range(menu.index("end") + 1)
                    if menu.type(index) == "command"]

        assert "Anheften" in menu_labels(app.build_list_menu(anheft_liste["id"]))
        app.set_pinned("folder", eltern["id"])
        assert "Lösen" in menu_labels(app.build_folder_menu(eltern["id"]))
        app.set_pinned("folder", eltern["id"], False)

        # Anpassen-Modus: eingebettet, ordnen, verbreitern, aus- und einblenden.
        app.set_home_view()
        root.update()
        app.toggle_home_editing()
        root.update()
        assert app._home_editing and app.home_tile_editor_rows
        assert all(row.winfo_toplevel() is root for _key, row in app.home_tile_editor_rows)
        erste, zweite = app.home_tile_editor_rows[0][0], app.home_tile_editor_rows[1][0]
        assert app.move_home_tile(erste, 1)
        sichtbar = [key for key in app.home_tile_order() if app.home_tile_visible(key)]
        assert sichtbar[:2] == [zweite, erste]
        # Tastatur: Alt+Pfeil hoch auf der fokussierten Zeile.
        zeile = dict(app.home_tile_editor_rows)[erste]
        zeile.focus_set()
        zeile.event_generate("<Alt-Up>")
        root.update()
        sichtbar = [key for key in app.home_tile_order() if app.home_tile_visible(key)]
        assert sichtbar[0] == erste
        app.set_home_tile_span("week", "wide")
        assert app.settings["home_tile_span"] == {"week": "wide"}
        app.set_home_tile_hidden("week", True)
        assert not app.home_tile_visible("week")
        assert all(key != "week" for key, _row in app.home_tile_editor_rows)
        app.set_home_tile_hidden("week", False)
        assert app.home_tile_visible("week")
        app.move_home_tile_to("week", 0)
        assert [key for key in app.home_tile_order() if app.home_tile_visible(key)][0] == "week"
        app.toggle_home_editing()
        root.update()
        assert not app._home_editing
        # Die breite Kachel steht jetzt über dem Raster und nimmt die ganze Breite ein.
        titel = next(widget for widget in descendants(app.home_content)
                     if isinstance(widget, mod.tk.Label) and widget.cget("text") == "Die nächsten sieben Tage")
        kachel = titel
        while kachel.master is not app.home_content and kachel.master.master is not app.home_content:
            kachel = kachel.master
        assert kachel.winfo_width() > app.home_content.winfo_width() * 0.8, (kachel.winfo_width(),
                                                                             app.home_content.winfo_width())
        app.set_home_tile_span("week", "normal")
        assert app.settings["home_tile_span"] == {}

        # Angeheftete Filter: Treffer sichtbar, direkt abhaken.
        filterliste = app.new_list_object("Filterziel", [app.new_item("Filtertreffer eins"),
                                                         app.new_item("Filtertreffer zwei")])
        app.lists.append(filterliste)
        app.save_items()
        app.settings["saved_filters"] = [{"id": "f-test", "name": "Filtertest", "query": "filtertreffer",
                                          "list_ids": [], "label_ids": [], "status": "open",
                                          "importance": "all", "due": "any", "label_mode": "any"}]
        app.settings["home_tiles_hidden"] = ["filters"]
        assert app.pin_home_filter("f-test")
        assert "filters" not in app.settings["home_tiles_hidden"]
        root.update()
        assert any(isinstance(widget, mod.tk.Label) and "Filtertest · 2 Treffer" in str(widget.cget("text"))
                   for widget in descendants(app.home_content))
        ziel = filterliste["items"][0]["id"]
        assert app.toggle_item_done_anywhere(ziel)
        assert app.find_item_in_lists(ziel)[0]["done"] is True
        root.update()
        assert any(isinstance(widget, mod.tk.Label) and "Filtertest · 1 Treffer" in str(widget.cget("text"))
                   for widget in descendants(app.home_content))
        app.undo_last_change()
        assert app.find_item_in_lists(ziel)[0]["done"] is False
        # Archivierte Listen fallen auch aus gespeicherten Filtern heraus.
        app.set_archived("list", filterliste["id"], True)
        assert app.saved_filters.entries(criteria=app.settings["saved_filters"][0]) == []
        app.set_archived("list", filterliste["id"], False)
        assert app.pin_home_filter("f-test", False)

        # ================================================================
        # Etappe C: gemeinsame Gruppierung (PW-010/AO-040)
        # ================================================================
        heute = mod.date.today()
        heute_iso = heute.isoformat()
        _h, morgen, wochenende = app.date_group_bounds(heute)
        assert app.date_group_key(None) == "none" and app.date_group_key(heute_iso) == "today"
        assert app.date_group_key((heute - mod.timedelta(days=3)).isoformat()) == "past"
        assert app.date_group_key(morgen.isoformat()) == "tomorrow"
        assert app.date_group_target("past")[0] is None and app.date_group_target("past")[1]
        assert app.date_group_target("none") == ("", None)
        spaet = app.date_group_target("later")[0]
        assert app.date_group_key(spaet) == "later"
        woche_ziel, woche_grund = app.date_group_target("week")
        assert (woche_ziel is None and woche_grund) or app.date_group_key(woche_ziel) == "week"
        rot = {"id": "label-rot", "name": "Rot", "color": "delete"}
        blau = {"id": "label-blau", "name": "Blau", "color": "clear"}
        app.labels.extend([rot, blau])
        assert not app.is_system_label(rot) and not app.is_system_label(blau)
        g1 = app.new_item("Termin mit Uhrzeit", due=heute_iso)
        g1["due_time"] = "09:30"
        g2 = app.new_item("Zwei Labels")
        g2["labels"] = [rot["id"], blau["id"]]
        g3 = app.new_item("Wichtig")
        g3["importance"] = 3
        gruppenliste = app.new_list_object("Gruppiertes", [g1, g2, g3])
        app.lists.append(gruppenliste)
        app.save_items()
        assert app.item_group_keys(g2, "label") == [rot["id"], blau["id"]]
        assert app.item_group_keys(g3, "label") == ["none"]
        # Datum: die Uhrzeit bleibt, nur der Tag wechselt – ein Rückgängig-Schritt.
        assert app.set_group_value([g1["id"]], "due", "tomorrow", "today") == (True, None)
        g1 = app.find_item_in_lists(g1["id"])[0]
        assert g1["due"] == morgen.isoformat() and g1["due_time"] == "09:30"
        app.undo_last_change()
        assert app.find_item_in_lists(g1["id"])[0]["due"] == heute_iso
        assert app.set_group_value([g1["id"]], "due", "tomorrow", "today") == (True, None)
        assert app.set_group_value([g1["id"]], "due", "past", "tomorrow")[0] is False
        assert app.set_group_value([g1["id"]], "due", "none", "tomorrow")[0]
        g1 = app.find_item_in_lists(g1["id"])[0]
        assert g1["due"] is None and g1["due_time"] is None
        # Label: das Ziel ersetzt das Quelllabel; „Ohne Label“ entfernt eigene Labels.
        assert app.set_group_value([g2["id"]], "label", "none", rot["id"])[0]
        assert app.find_item_in_lists(g2["id"])[0]["labels"] == []
        assert app.set_group_value([g2["id"]], "label", blau["id"], "none")[0]
        assert app.set_group_value([g2["id"]], "label", rot["id"], blau["id"])[0]
        assert app.find_item_in_lists(g2["id"])[0]["labels"] == [rot["id"]]
        assert app.set_group_value([g3["id"]], "importance", "1", "3")[0]
        assert app.find_item_in_lists(g3["id"])[0]["importance"] == 1
        assert app.set_group_value([g3["id"]], "done", "done", "open")[0]
        assert app.find_item_in_lists(g3["id"])[0]["done"] is True
        app.undo_last_change()
        assert app.find_item_in_lists(g3["id"])[0]["done"] is False

        # Zweiter Ausbau: Gruppierung behält Zwischenüberschriften und die Nummern der Liste.
        k_a = app.new_item("Kopf A ohne Überschrift")
        k_b = app.new_item("Kopf B wichtig", importance=1)
        k_c = app.new_item("Kopf C normal")
        kopf = app.new_item("Phase zwei", kind=app.ITEM_KIND_HEADING, children=[k_b, k_c])
        kopfliste = app.new_list_object("Kopfliste", [k_a, kopf])
        app.lists.append(kopfliste)
        app.save_items()
        app.set_active_list(kopfliste["id"])
        app.workspace.set_mode("list")
        root.update()
        ungruppiert = {k["id"]: app.tree.item(k["id"], "text").split(".")[0] for k in (k_a, k_b, k_c)}
        assert ungruppiert == {k_a["id"]: "1", k_b["id"]: "1", k_c["id"]: "2"}
        app.set_list_group("importance")
        root.update()
        for k in (k_a, k_b, k_c):
            assert app.tree.item(k["id"], "text").split(".")[0] == ungruppiert[k["id"]], "Nummern laufen durch"
        kopfzeilen = [iid for iid in app.tree.get_children(app.group_section_iid("0")) + app.tree.get_children(app.group_section_iid("1"))
                      if app.GROUP_HEADING_IID_MARKER in iid]
        assert len(kopfzeilen) == 2 and all(app.tree.item(iid, "text").endswith("Phase zwei") for iid in kopfzeilen)
        assert all(app.is_synthetic_row(iid) for iid in kopfzeilen)
        assert not any(app.GROUP_HEADING_IID_MARKER in iid for iid in app.iter_tree_ids())
        reihe0 = list(app.tree.get_children(app.group_section_iid("0")))
        assert reihe0.index(k_a["id"]) < reihe0.index(kopfzeilen[0]) < reihe0.index(k_c["id"])
        # Dritter Ausbau: Die gruppierte Tabelle zeigt dieselben Nummern und Überschriften.
        app.set_table_view()
        root.update()
        assert "tree" in str(app.tree.cget("show"))
        for k in (k_a, k_b, k_c):
            assert app.tree.item(k["id"], "text") == ungruppiert[k["id"]], "Tabellennummer wie in der Liste"
        titel_spalte = list(app.tree.cget("columns")).index("title")
        tabellenkoepfe = [iid for iid in app.tree.get_children(app.group_section_iid("0"))
                          + app.tree.get_children(app.group_section_iid("1"))
                          if app.GROUP_HEADING_IID_MARKER in iid]
        assert len(tabellenkoepfe) == 2
        assert all(app.tree.item(iid, "values")[titel_spalte] == "Phase zwei" for iid in tabellenkoepfe)
        reihe0 = list(app.tree.get_children(app.group_section_iid("0")))
        assert reihe0.index(k_a["id"]) < reihe0.index(tabellenkoepfe[0]) < reihe0.index(k_c["id"])
        assert not any(app.GROUP_HEADING_IID_MARKER in iid for iid in app.iter_tree_ids())
        # Nach Spalte sortiert gilt die Sortierung innerhalb jeder Überschrift; die Überschriften bleiben.
        k_d = app.new_item("Kopf D alpha")
        app.find_item_in_lists(kopf["id"])[0]["children"].append(k_d)
        app.save_items()
        app.sort_table_by("title")
        app.sort_table_by("title")
        root.update()
        assert app.table_sort_for_list() == ("title", "desc")
        reihe0 = list(app.tree.get_children(app.group_section_iid("0")))
        kopf0 = next(iid for iid in reihe0 if app.GROUP_HEADING_IID_MARKER in iid)
        assert reihe0.index(k_a["id"]) < reihe0.index(kopf0) < reihe0.index(k_d["id"]) < reihe0.index(k_c["id"]), \
            "absteigend unter der Überschrift, Überschrift an ihrem Platz"
        app.sort_table_by("title")
        assert not app.table_sort_for_list()[0]
        # Mitbehoben: „Pinnwand öffnen“ aus dem Menü wirkt auch in der Tabelle.
        eintrag = next(entry for entry in app.app_action_entries() if entry["label"] == "Pinnwand öffnen")
        eintrag["menu"].invoke(eintrag["index"])
        root.update()
        assert app.view_mode == "list" and app.workspace.mode == "board" and not errors, errors
        app.workspace.set_mode("list")
        app.set_list_group(None)
        root.update()

        # Liste gruppiert: Abschnittsköpfe, Ziehen zwischen Abschnitten setzt das Feld.
        app.set_active_list(gruppenliste["id"])
        app.workspace.set_mode("list")
        root.update()
        app.set_list_group("importance")
        root.update()
        abschnitte = [iid for iid in app.tree.get_children("") if app.is_group_section_row(iid)]
        assert abschnitte and all(app.tree.get_children(iid) for iid in abschnitte)
        assert set(app.iter_tree_ids()) >= {g1["id"], g2["id"], g3["id"]}
        assert not any(app.is_group_section_row(iid) for iid in app.iter_tree_ids())
        hoch_abschnitt = app.group_section_iid("3")
        assert not app.tree.exists(hoch_abschnitt)
        niedrig = app.group_section_iid("1")
        ohne = app.group_section_iid("0")
        assert app.tree.parent(g3["id"]) == niedrig and app.tree.parent(g1["id"]) == ohne
        assert app.group_drop(g1["id"], g3["id"], [g1["id"]]) is True
        assert app.find_item_in_lists(g1["id"])[0]["importance"] == 1
        root.update()
        # Zugeklappt übersteht der Abschnitt den Neuaufbau.
        app.tree.item(niedrig, open=False)
        app.note_group_section_state(niedrig)
        app.refresh_tree()
        assert app.tree.item(niedrig, "open") in (0, False, "0", "false")
        app.tree.item(niedrig, open=True)
        app.note_group_section_state(niedrig)
        # Tabelle gruppiert und verschachtelt (AO-030).
        g3_kind = app.new_item("Unterpunkt passt")
        app.find_item_in_lists(g3["id"])[0].setdefault("children", []).append(g3_kind)
        app.save_items()
        app.set_table_view()
        root.update()
        assert "tree" in str(app.tree.cget("show"))
        assert any(app.is_group_section_row(iid) for iid in app.tree.get_children(""))
        app.set_list_group(None)
        app.set_table_nested(True)
        root.update()
        assert app.tree.parent(g3_kind["id"]) == g3["id"]
        app.search_var.set("Unterpunkt passt")
        app.refresh_tree()
        assert "context" in app.tree.item(g3["id"], "tags")
        app.search_var.set("")
        app.set_table_nested(False)
        root.update()
        assert "tree" not in str(app.tree.cget("show"))
        # „Ansicht › Liste › Zur Listenansicht“ führt aus der Tabelle zurück (Mitbeheben).
        eintrag = next(entry for entry in app.app_action_entries() if entry["label"] == "Zur Listenansicht")
        eintrag["menu"].invoke(eintrag["index"])
        root.update()
        assert app.view_mode == "list" and not errors, errors
        assert {"Gruppieren: Fälligkeit", "Tabelle: Unterpunkte verschachtelt"} <= {
            entry["label"] for entry in app.app_action_entries()}
        assert not [entry for entry in app.app_action_entries() if entry["group"] == "Weitere Aktionen"]
        assert app.normalize_personal_settings({"list_group_by": {"a": "due", "b": "list", "c": "x"},
                                                "table_nesting": {"a": "nested", "b": "flat"}})[
            "list_group_by"] == {"a": "due"}

        # ================================================================
        # Spaltenboard (PW-010)
        # ================================================================
        app.set_active_list(gruppenliste["id"])
        flaeche = app.workspace
        flaeche.set_mode("board")
        root.update()
        flaeche.configure_board("layout", "columns")
        flaeche.configure_board("group_by", "label")
        root.update()
        assert flaeche.board()["layout"] == "columns"
        g2_neu = app.find_item_in_lists(g2["id"])[0]
        g2_neu["labels"] = [rot["id"], blau["id"]]
        app.save_items()
        flaeche._signature = None
        flaeche.refresh()
        root.update()
        vorkommen = [key for _box, identity, key, _tag in flaeche.column_hits if identity == g2["id"]]
        assert sorted(vorkommen) == sorted([rot["id"], blau["id"]])
        # Ziehen von Blau nach „Ohne Label“: Label-Regel greift.
        assert flaeche.move_to_column(g2["id"], blau["id"], "none")
        assert app.find_item_in_lists(g2["id"])[0]["labels"] == []
        # Fälligkeit: „Überfällig“ nimmt nichts an und sagt warum.
        infos = []
        app.show_info = lambda *args, **kwargs: infos.append(args)
        flaeche.set_board_group_field("due")
        root.update()
        assert [spalte["key"] for spalte in flaeche.column_order][:3] == ["past", "today", "tomorrow"]
        assert flaeche.move_to_column(g3["id"], "none", "past") is False and infos
        app.show_info = lambda *args, **kwargs: None
        # Tastatur: Alt+Rechts in die nächste Spalte, die etwas annimmt.
        flaeche.selected_id = g3["id"]
        flaeche.selected_ids = [g3["id"]]
        flaeche._selected_column = "none"
        flaeche.move_card(-1, 0)
        assert app.date_group_key(app.find_item_in_lists(g3["id"])[0]["due"]) == "later"
        # Einklappen, leere Spalten ausblenden, nur offene.
        flaeche.toggle_column("today")
        assert "today" in flaeche.board()["collapsed"]
        assert flaeche.column_boxes["today"][2] == flaeche.COLUMN_COLLAPSED_WIDTH
        flaeche.toggle_column("today")
        flaeche.configure_board("hide_empty", True)
        root.update()
        assert all(any(key == spalte["key"] for _b, _i, key, _t in flaeche.column_hits)
                   for spalte in flaeche.column_order)
        flaeche.configure_board("hide_empty", False)
        normalisiert = mod.ItemWorkspace.normalize_settings({"pinboards": {
            "list:x": {"layout": "columns", "group_by": "label", "collapsed": ["a", "a", 3],
                       "hide_empty": True, "areas": [{"id": "b1", "name": " Plan ", "color": "nope",
                                                      "x": -5, "y": 10, "w": 5, "h": 900}]},
            "list:y": {"layout": "gibtsnicht", "group_by": "nope"}}, "open_tabs": [], "active_tab": {}})
        board_x = normalisiert["pinboards"]["list:x"]
        assert board_x["layout"] == "columns" and board_x["group_by"] == "label"
        assert board_x["collapsed"] == ["a"] and board_x["hide_empty"] is True
        assert board_x["areas"] == [{"id": "b1", "name": "Plan", "color": "clear", "x": 0, "y": 10,
                                     "w": 120, "h": 900}]
        assert normalisiert["pinboards"]["list:y"]["layout"] == "free"
        assert normalisiert["pinboards"]["list:y"]["group_by"] == "due"
        # 500 Karten in sechs Spalten bleiben im Grenzwert.
        viele = app.new_list_object("Viele Karten", [app.new_item(f"Karte {index}", due=(
            heute + mod.timedelta(days=index % 9 - 2)).isoformat()) for index in range(500)])
        app.lists.append(viele)
        app.save_items()
        app.set_active_list(viele["id"])
        flaeche.set_mode("board")
        flaeche.configure_board("layout", "columns")
        root.update()
        import time as zeitmodul
        start = zeitmodul.perf_counter()
        flaeche.draw_board()
        dauer = zeitmodul.perf_counter() - start
        assert len(flaeche.column_hits) == 500 and len(flaeche.column_order) == 6
        assert dauer < 8.0, dauer
        flaeche.configure_board("layout", "free")
        app.set_active_list(gruppenliste["id"])
        flaeche.set_mode("board")
        flaeche.configure_board("layout", "free")
        root.update()

        # ================================================================
        # Karteninhalt (PW-020), Zeichnungskarte (ZF-100)
        # ================================================================
        schritte_punkt = app.find_item_in_lists(g1["id"])[0]
        schritte_punkt["checklist"] = [{"text": f"Schritt {n}", "done": False} for n in range(7)]
        schritte_punkt["description"] = "x" * 400
        app.save_items()
        flaeche.pin([g1["id"], g2["id"], g3["id"]])
        flaeche.configure_board("show_checklist", True)
        root.update()
        bloecke, _hoehe = flaeche.card_blocks(schritte_punkt, gruppenliste, 300, True)
        schritte = next(block for block in bloecke if block["art"] == "schritte")
        assert len(schritte["zeilen"]) == 5 and schritte["rest"] == 2
        beschreibung = next(block for block in bloecke if block["art"] == "text" and block["text"].startswith("xxx"))
        assert beschreibung["text"].replace("\n", "").endswith("…")
        treffer = next(hit for hit in flaeche._checklist_hits if hit[1] == g1["id"] and hit[2] == 0)
        box = treffer[0]
        flaeche.card_press(SimpleNamespace(x=int(box[0] + 4 - flaeche.canvas.canvasx(0)),
                                           y=int(box[1] + 4 - flaeche.canvas.canvasy(0)), state=0))
        assert app.find_item_in_lists(g1["id"])[0]["checklist"][0]["done"] is True
        flaeche.select_card(g1["id"])
        flaeche.set_card_show("checklist", False)
        karte = next(card for card in flaeche.board()["cards"] if card["item_id"] == g1["id"])
        assert karte["show"] == {"checklist": False}
        bloecke, _h = flaeche.card_blocks(schritte_punkt, gruppenliste, 300, True, card=karte)
        assert not any(block["art"] == "schritte" for block in bloecke)
        flaeche.set_card_show("checklist", None)
        assert "show" not in next(card for card in flaeche.board()["cards"] if card["item_id"] == g1["id"])
        _b, hoehe_streifen = flaeche.card_blocks(schritte_punkt, gruppenliste, 300, True)
        flaeche.configure_board("color_mode", "header")
        _b, hoehe_kopf = flaeche.card_blocks(schritte_punkt, gruppenliste, 300, True)
        assert hoehe_kopf == hoehe_streifen + flaeche.CARD_HEADER_BAND
        flaeche.configure_board("color_mode", "fill")
        flaeche.configure_board("color_source", "label")
        app.find_item_in_lists(g2["id"])[0]["labels"] = [rot["id"]]
        assert flaeche.card_accent(app.find_item_in_lists(g2["id"])[0]) == app.label_color(rot)
        flaeche.configure_board("color_mode", "stripe")
        flaeche.configure_board("color_source", "item")
        flaeche.configure_board("show_checklist", False)
        # Zeichnung als Karte: Verweis, Miniatur, Öffnen mit Rückweg.
        app.create_new_drawing(size=32)
        bild = app.current_list()
        assert app.is_drawing_list(bild) and bild["drawing"]["width"] == 32
        app.set_active_list(gruppenliste["id"])
        flaeche.set_mode("board")
        root.update()
        seite = flaeche.PAGE_CARD_PREFIX + bild["id"]
        assert seite in flaeche.valid_cards()
        flaeche.pin([seite])
        root.update()
        assert seite in flaeche.card_boxes
        bloecke, _h = flaeche.page_card_blocks(bild, 300)
        assert any(block["art"] == "bild" and block.get("rahmen") for block in bloecke)
        # Zweiter Ausbau: Druckseite und Folien zeigen die Zeichnung als pixelscharfes PNG.
        druckseite = flaeche.build_board_print_html()
        assert 'img class="pixel"' in druckseite and "image-rendering: pixelated" in druckseite
        png = base64.b64decode(flaeche.drawing_data_uri(bild).split(",", 1)[1])
        assert png[:8] == b"\x89PNG\r\n\x1a\n" and png_size(png)[0] >= 128
        assert flaeche.drawing_data_uri({"drawing": {"kaputt": True}}) is None
        flaeche.edit(seite)
        root.update()
        assert app.active_list_id == bild["id"] and app.board_return_target()
        assert any("Zurück zur Pinnwand" in str(widget.cget("text")) for widget in descendants(app.path_row)
                   if isinstance(widget, (mod.tk.Label, mod.CanvasLabel)))
        app.return_to_board()
        root.update()
        assert app.active_list_id == gruppenliste["id"] and flaeche.mode == "board"
        umgeordnet = app.pinboards_from_backup({"pinboards": {f"list:{gruppenliste['id']}": flaeche.board()}},
                                               {gruppenliste["id"]: "neu-liste", bild["id"]: "neu-bild"},
                                               {g1["id"]: "n1", g2["id"]: "n2", g3["id"]: "n3"})
        karten_neu = umgeordnet["list:neu-liste"]["cards"]
        assert {card["item_id"] for card in karten_neu} == {"n1", "n2", "n3", flaeche.PAGE_CARD_PREFIX + "neu-bild"}

        # ================================================================
        # Bereiche (PW-030), Aufräumen (PW-040)
        # ================================================================
        for identity, (x, y) in ((g1["id"], (24, 24)), (g2["id"], (360, 48)), (g3["id"], (48, 400)),
                                 (seite, (700, 300))):
            flaeche.store_position(identity, x, y, reveal=False)
        root.update()
        # Ausbau 3.30: Einfaches Verschieben einer Karte ist zurücknehmbar.
        def position(identity):
            return next((card["x"], card["y"]) for card in flaeche.board()["cards"] if card["item_id"] == identity)
        vorher_g3 = position(g3["id"])
        flaeche.store_position(g3["id"], 96, 480, reveal=False)
        assert position(g3["id"]) == (96, 480) and flaeche.view_undo_pending()
        app.undo_last_change()
        assert position(g3["id"]) == vorher_g3
        root.update()
        app.themed_input_dialog = lambda *args, **kwargs: "Planung"
        flaeche.select_card(g1["id"])
        flaeche.select_card(g2["id"], additive=True)
        flaeche.create_area()
        root.update()
        bereich = dict(flaeche.area_list()[0])
        assert bereich["name"] == "Planung" and flaeche.cards_in_area(bereich) == [g1["id"], g2["id"]] or \
            set(flaeche.cards_in_area(bereich)) == {g1["id"], g2["id"]}
        vorher = {card["item_id"]: (card["x"], card["y"]) for card in flaeche.board()["cards"]}
        faktor = flaeche.zoom_factor()
        kopf_x = bereich["x"] * faktor + 20 - flaeche.canvas.canvasx(0)
        kopf_y = bereich["y"] * faktor + 10 - flaeche.canvas.canvasy(0)
        flaeche.card_press(SimpleNamespace(x=int(kopf_x), y=int(kopf_y), state=0))
        assert flaeche._area_drag is not None
        flaeche.card_motion(SimpleNamespace(x=int(kopf_x + 60), y=int(kopf_y + 48), state=0))
        flaeche.card_release(SimpleNamespace(x=int(kopf_x + 60), y=int(kopf_y + 48), state=0))
        root.update()
        nachher = {card["item_id"]: (card["x"], card["y"]) for card in flaeche.board()["cards"]}
        assert nachher[g1["id"]] != vorher[g1["id"]] and nachher[g3["id"]] == vorher[g3["id"]]
        assert flaeche.area_list()[0]["x"] != bereich["x"]
        # Ein Rückgängig-Schritt für Bereich und Karten.
        app.undo_last_change()
        zurueck = {card["item_id"]: (card["x"], card["y"]) for card in flaeche.board()["cards"]}
        assert zurueck == vorher and flaeche.area_list()[0]["x"] == bereich["x"]
        flaeche.rename_area(bereich["id"])
        flaeche.set_area_color(bereich["id"], "export")
        assert flaeche.area_list()[0]["color"] == "export"
        assert "Planung" in flaeche.build_board_print_html()
        flaeche.jump_to_area(bereich["id"])
        assert flaeche.area_selected_only()
        flaeche.delete_area()
        assert flaeche.area_list() == [] and len(flaeche.board()["cards"]) == 4
        # Aufräumen: vier Karten im 2×2-Raster, Fang beachtet, ein Schritt.
        for identity in (g1["id"], g2["id"], g3["id"], seite):
            flaeche.select_card(identity, additive=identity != g1["id"])
        flaeche.tidy_selection()
        root.update()
        lagen = sorted({(card["x"], card["y"]) for card in flaeche.board()["cards"]})
        assert len({x for x, _y in lagen}) == 2 and len({y for _x, y in lagen}) == 2
        assert all(x % 24 == 0 and y % 24 == 0 for x, y in lagen)
        app.undo_last_change()
        assert {card["item_id"]: (card["x"], card["y"]) for card in flaeche.board()["cards"]} == vorher

        # ================================================================
        # Weiterdenken (PW-050), Verbindungen gestalten (PW-060), Hintergrund (PW-070)
        # ================================================================
        flaeche.select_card(g1["id"])
        flaeche.configure_board("auto_connect", True)
        flaeche.quick_next_card()
        root.update()
        entwurf = flaeche._quick_card
        assert entwurf and entwurf["entry"].winfo_toplevel() is root
        entwurf["entry"].insert(0, "Nächster Gedanke")
        flaeche.confirm_quick_card()
        root.update()
        neu_punkt = next(item for item in app.walk_items(app.find_item_in_lists(g1["id"])[3]["items"])
                         if item["text"] == "Nächster Gedanke")
        assert neu_punkt["id"] in flaeche.card_boxes
        assert any({von, nach} == {g1["id"], neu_punkt["id"]} for von, nach, _art in flaeche.connections())
        flaeche.select_card(g1["id"])
        flaeche.quick_next_card()
        flaeche._quick_card["entry"].insert(0, "Verworfen")
        flaeche._quick_card["entry"].focus_force()
        root.update()
        flaeche._quick_card["entry"].event_generate("<Escape>")
        root.update()
        assert flaeche._quick_card is None
        assert not any(item["text"] == "Verworfen" for entry in app.lists for item in app.walk_items(entry["items"]))
        flaeche.configure_board("auto_connect", False)
        # Ziehpunkt am Kartenrand verbindet durch Ziehen.
        flaeche.select_card(g2["id"])
        griff = next(box for box, identity in flaeche._connect_handles if identity == g2["id"])
        ziel_box = flaeche.card_boxes[g3["id"]]
        sx, sy = griff[0] + griff[2] / 2 - flaeche.canvas.canvasx(0), griff[1] + griff[3] / 2 - flaeche.canvas.canvasy(0)
        zx = ziel_box[0] + 20 - flaeche.canvas.canvasx(0)
        zy = ziel_box[1] + 20 - flaeche.canvas.canvasy(0)
        flaeche.card_press(SimpleNamespace(x=int(sx), y=int(sy), state=0))
        flaeche.card_motion(SimpleNamespace(x=int(zx), y=int(zy), state=0))
        flaeche.card_release(SimpleNamespace(x=int(zx), y=int(zy), state=0))
        assert any({von, nach} == {g2["id"], g3["id"]} for von, nach, _art in flaeche.connections())
        # Beschriftung, Strich, Farbe – additiv und im Druck.
        app.themed_input_dialog = lambda *args, **kwargs: "hängt ab von"
        flaeche.label_connection((g2["id"], g3["id"]))
        flaeche.update_connection((g2["id"], g3["id"]), dash=True, color="delete")
        eintrag = next(entry for entry in flaeche.connection_entries()
                       if {entry["from"], entry["to"]} == {g2["id"], g3["id"]})
        assert eintrag["label"] == "hängt ab von" and eintrag["dash"] is True and eintrag["color"] == "delete"
        root.update()
        texte = [flaeche.canvas.itemcget(element, "text") for element in flaeche.canvas.find_withtag("connection")
                 if flaeche.canvas.type(element) == "text"]
        assert "hängt ab von" in texte
        druck = flaeche.build_board_print_html()
        assert "hängt ab von" in druck and 'stroke-dasharray="6 4"' in druck
        mitte = next(element for element in flaeche.canvas.find_withtag("connection")
                     if flaeche.canvas.type(element) == "text")
        mx, my = flaeche.canvas.coords(mitte)
        assert set(flaeche.connection_at(mx, my)) == {g2["id"], g3["id"]}
        # Linien stapeln sich beim Ziehen nicht mehr (Mitbeheben).
        linien_vorher = len(flaeche.canvas.find_withtag("connection"))
        box = flaeche.card_boxes[g3["id"]]
        px, py = box[0] + 30 - flaeche.canvas.canvasx(0), box[1] + 30 - flaeche.canvas.canvasy(0)
        flaeche.card_press(SimpleNamespace(x=int(px), y=int(py), state=0))
        for schritt in range(1, 6):
            flaeche.card_motion(SimpleNamespace(x=int(px + schritt * 7), y=int(py + schritt * 5), state=0))
        assert len(flaeche.canvas.find_withtag("connection")) == linien_vorher
        flaeche.card_release(SimpleNamespace(x=int(px + 35), y=int(py + 25), state=0))
        # Hintergrund: begrenzte Zahl von Marken auch bei kleinem Zoom, mitdruckbar.
        flaeche.configure_board("background", "dots")
        root.update()
        punkte = len(flaeche.canvas.find_withtag("background"))
        assert 0 < punkte <= flaeche.BACKGROUND_MAX_MARKS + 200
        flaeche.configure_board("zoom", 50)
        root.update()
        assert len(flaeche.canvas.find_withtag("background")) <= flaeche.BACKGROUND_MAX_MARKS + 200, (len(flaeche.canvas.find_withtag("background")), flaeche.canvas.winfo_width(), flaeche.canvas.winfo_height(), flaeche.zoom_factor())
        flaeche.configure_board("zoom", 200)
        flaeche.configure_board("background", "grid")
        root.update()
        assert flaeche.canvas.find_withtag("background")
        flaeche.configure_board("print_background", True)
        assert "background-image" in flaeche.build_board_print_html()
        flaeche.configure_board("zoom", 100)
        flaeche.configure_board("background", "none")
        root.update()
        assert not flaeche.canvas.find_withtag("background")
        flaeche.set_mode("list")
        root.update()

        # ================================================================
        # Tagebuch mit allen Inhaltsarten (ZF-120), Anlageoption Pinnwand
        # ================================================================
        tagebuch = app.new_folder_object("Reisetagebuch", folder_kind="journal")
        app.folders.append(tagebuch)
        # Alle Dokumentarten bleiben im Listenbereich möglich, auch in einem Notizbuch.
        # Der reine Notizbereich erlaubt nach dem Ergänzungsauftrag nur Notizen.
        app.locate_sidebar_root("folder", tagebuch["id"], "lists")
        app.save_items()
        app.update_sidebar_list()

        def anlegen(titel, art, tag=None, ordner="Reisetagebuch"):
            def run(dialog, parent=None):
                root.update()
                menues = [widget for widget in descendants(dialog) if isinstance(widget, mod.AppOptionMenu)]
                next(menu for menu in menues if "Pinnwand" in menu.options).variable.set(art)
                if ordner:
                    feld = next(menu for menu in menues if any(option.endswith(ordner) for option in menu.options))
                    feld.variable.set(next(option for option in feld.options if option.endswith(ordner)))
                root.update()
                next(widget for widget in descendants(dialog) if isinstance(widget, mod.tk.Entry)).insert(0, titel)
                if tag:
                    datum = next(widget for widget in descendants(dialog) if isinstance(widget, mod.DueField))
                    datum.date_entry.delete(0, "end")
                    datum.date_entry.insert(0, tag)
                next(widget for widget in descendants(dialog)
                     if isinstance(widget, mod.RoundedButton) and widget.text == "Anlegen").command()
                if dialog.winfo_exists():
                    dialog.destroy()
            return run

        original_modal = app.run_modal
        try:
            app.run_modal = anlegen("Notiz vom Strand", "Notiz", "20.09.2026")
            app.create_list_in_folder(tagebuch["id"])
            app.run_modal = anlegen("Packliste", "Aufgaben", "22.09.2026")
            app.create_container_dialog("list", parent_id=tagebuch["id"])
            app.run_modal = anlegen("Skizzen", "Zeichnung", "22.09.2026")
            app.create_container_dialog("list", parent_id=tagebuch["id"])
            app.run_modal = anlegen("Routenplanung", "Pinnwand", "24.09.2026")
            app.create_container_dialog("list", parent_id=tagebuch["id"])
            app.run_modal = anlegen("Freie Pinnwand", "Pinnwand", None, ordner=None)
            app.create_container_dialog("list")
        finally:
            app.run_modal = original_modal
        root.update()
        freie = next(entry for entry in app.lists if entry["title"] == "Freie Pinnwand")
        assert freie["list_kind"] == "tasks" and app.active_list_id == freie["id"]
        assert app.workspace.mode == "board" and app.workspace.visible
        app.workspace.set_mode("list")
        inhalte = [entry for entry in app.lists if entry.get("folder_id") == tagebuch["id"]]
        assert sorted(app.journal_kind_name(entry) for entry in inhalte) == [
            "Aufgabenliste", "Notiz", "Pinnwand", "Zeichnung"]
        packliste = next(entry for entry in inhalte if entry["title"] == "Packliste")
        assert packliste["list_kind"] == "tasks" and packliste["journal"]["moment_date"] == "2026-09-22"
        route = next(entry for entry in inhalte if entry["title"] == "Routenplanung")
        assert app.settings["active_tab"]["list:" + route["id"]] == "board"
        assert route["journal"]["moment_date"] == "2026-09-24"
        app.set_active_folder(tagebuch["id"])
        root.update()
        assert app.journal_filter_button.winfo_manager() == "pack"

        def tagebuch_titel():
            return [next(entry["title"] for entry in app.lists if entry["id"] == app.folder_list_id_from_iid(iid))
                    for iid in app.tree.get_children("") if iid.startswith("folder-list:")]

        reihenfolge = tagebuch_titel()
        assert reihenfolge[0] == "Routenplanung" and reihenfolge[-1] == "Notiz vom Strand"
        assert set(reihenfolge[1:3]) == {"Packliste", "Skizzen"}
        # Gleicher Tag: stabil über Erstellung und Kennung.
        app.refresh_tree()
        assert tagebuch_titel() == reihenfolge
        zeilentext = next(app.tree.item(iid, "text") for iid in app.tree.get_children("")
                          if iid == f"folder-list:{packliste['id']}")
        assert "22.09.2026" in zeilentext and "Aufgabenliste" in zeilentext
        # Tagesfilter und inklusiver Von-bis-Filter, zusammen mit der Volltextsuche.
        app.set_journal_filter(tagebuch["id"], "2026-09-22", "2026-09-22")
        assert sorted(tagebuch_titel()) == ["Packliste", "Skizzen"]
        assert app.journal_filter_button.text.startswith("Tag: 22.09.2026")
        app.set_journal_filter(tagebuch["id"], "2026-09-22", "2026-09-20")
        assert sorted(tagebuch_titel()) == ["Notiz vom Strand", "Packliste", "Skizzen"]
        app.search_var.set("Pack")
        app.refresh_tree()
        assert tagebuch_titel() == ["Packliste"]
        app.search_var.set("")
        app.set_journal_filter(tagebuch["id"])
        assert len(tagebuch_titel()) == 4
        # Verschieben ins Tagebuch bewahrt das Momentdatum, heraus bleibt es stehen.
        fremd = app.new_list_object("Mitgebracht", [])
        fremd["journal"]["moment_date"] = "2026-08-01"
        app.lists.append(fremd)
        assert app.move_sidebar_list_into_folder(fremd["id"], tagebuch["id"])
        assert fremd["journal"]["moment_date"] == "2026-08-01"
        app.detach_list_from_folder(fremd["id"])
        fremd = next(entry for entry in app.lists if entry["id"] == fremd["id"])
        assert fremd["journal"]["moment_date"] == "2026-08-01"
        # Ohne lesbares Datum fragt Glide vor dem Abschluss; ohne Antwort kein Verschieben.
        ohne = app.new_list_object("Ohne Datum", [])
        ohne["journal"] = {}
        ohne["created_at"] = "kaputt"
        app.lists.append(ohne)
        original_due_dialog = app.themed_due_dialog
        try:
            app.themed_due_dialog = lambda *args, **kwargs: None
            assert app.move_sidebar_list_into_folder(ohne["id"], tagebuch["id"]) is False
            assert ohne.get("folder_id") != tagebuch["id"]
            app.themed_due_dialog = lambda *args, **kwargs: ("2026-09-01", None)
            assert app.move_sidebar_list_into_folder(ohne["id"], tagebuch["id"])
            assert ohne["journal"]["moment_date"] == "2026-09-01"
        finally:
            app.themed_due_dialog = original_due_dialog
        # Duplizieren erhält das Momentdatum.
        vorher_ids = {entry["id"] for entry in app.lists}
        app.duplicate_list(packliste["id"])
        kopie = next(entry for entry in app.lists if entry["id"] not in vorher_ids)
        assert kopie["journal"]["moment_date"] == "2026-09-22"
        assert "Momentdatum …" in [app.build_list_menu(packliste["id"]).entrycget(index, "label")
                                   for index in range(app.build_list_menu(packliste["id"]).index("end") + 1)
                                   if app.build_list_menu(packliste["id"]).type(index) == "command"]

        # ================================================================
        # Abschnitte und Schnellaktionen der Seitenleiste (AO-020)
        # ================================================================
        app.set_home_view()
        root.update()
        systemzeilen = len(app.system_listbox.get_children(""))
        app.set_sidebar_section_open("views", False)
        root.update()
        assert app.system_listbox.winfo_manager() == "" and app.views_collapsed_header.winfo_manager() == "pack"
        assert f"Ansichten ({systemzeilen})" in app.views_collapsed_header.cget("text")
        assert app.views_collapsed_header.winfo_y() < app.sidebar_title_row.winfo_y()
        app.update_sidebar_list()
        root.update()
        assert app.system_listbox.winfo_manager() == ""  # bleibt nach dem Neuaufbau zu
        app.views_collapsed_header.event_generate("<Button-1>")
        root.update()
        assert app.system_listbox.winfo_manager() == "pack" and app.views_collapsed_header.winfo_manager() == ""
        assert app.system_listbox.winfo_y() < app.sidebar_title_row.winfo_y()
        menu = app.build_sidebar_context_menu(("view", app.HOME_VIEW))
        assert "Ansichten einklappen" in [menu.entrycget(index, "label") for index in range(menu.index("end") + 1)
                                          if menu.type(index) == "command"]
        # „Listen und Ordner“ lässt sich seit dem 26.09.2026 nicht mehr
        # einklappen; auch ein gespeicherter Zustand „zu“ gilt nicht mehr.
        assert not hasattr(app, "folders_section_toggle")
        app.toggle_sidebar_section("folders")
        root.update()
        assert app.sidebar_listbox.winfo_manager() == "pack"
        assert app.normalize_personal_settings({"sidebar_sections_closed": ["folders", "views"]})[
            "sidebar_sections_closed"] == ["views"]
        assert app.sidebar_title.winfo_rooty() < app.sidebar_listbox.winfo_rooty()
        assert app.settings["sidebar_sections_closed"] == []
        # „+“ und „…“ erscheinen nur über Ordnerzeilen und verschieben keine Zeile.
        ordner_iid = f"folder:{eltern['id']}"
        app.sidebar_listbox.see(ordner_iid)
        root.update()
        box = app.sidebar_listbox.bbox(ordner_iid)
        vorher = {iid: app.sidebar_listbox.bbox(iid) for iid in app.sidebar_listbox.get_children("")}
        app.on_sidebar_quick_motion(SimpleNamespace(x=20, y=box[1] + box[3] // 2))
        root.update()
        assert app.sidebar_quick_row == eltern["id"]
        assert app.sidebar_quick_add_button.winfo_manager() == "place"
        assert app.sidebar_quick_more_button.winfo_x() > app.sidebar_quick_add_button.winfo_x()
        assert {iid: app.sidebar_listbox.bbox(iid) for iid in app.sidebar_listbox.get_children("")} == vorher
        schnell = app.folder_quick_add_menu(eltern["id"])
        eintraege = [schnell.entrycget(index, "label") for index in range(schnell.index("end") + 1)]
        assert eintraege == ["Aus Vorlage …", "Neue Liste …", "Neue Seite", "Seite aus Vorlage", "Neue Notiz …",
                             "Neue Pinnwand …", "Neue Galerie", "Neue Zeichnung",
                             "Neuer Unterordner …", "Neues Buch …", "Neues Notizbuch …"], eintraege
        # Jede Schnellaktion steht auch im Kontextmenü des Ordners (Tastatur).
        ordnermenue = app.build_folder_menu(eltern["id"])
        neu_index = next(index for index in range(ordnermenue.index("end") + 1)
                         if ordnermenue.type(index) == "cascade" and ordnermenue.entrycget(index, "label") == "Neu anlegen")
        neu_menu = root.nametowidget(ordnermenue.entrycget(neu_index, "menu"))
        assert [neu_menu.entrycget(index, "label") for index in range(neu_menu.index("end") + 1)] == eintraege
        listen_iid = next(iid for iid, row in app.sidebar_iid_to_row.items() if row[0] == "list"
                          and app.sidebar_listbox.exists(iid) and app.sidebar_listbox.bbox(iid))
        lbox = app.sidebar_listbox.bbox(listen_iid)
        app.on_sidebar_quick_motion(SimpleNamespace(x=20, y=lbox[1] + lbox[3] // 2))
        # Seit 27.09.2026: Eine Listenzeile zeigt nur „…“ (Bearbeiten, Löschen).
        assert app.sidebar_quick_row == app.sidebar_iid_to_row[listen_iid][1]
        assert app.sidebar_quick_add_button.winfo_manager() == ""
        assert app.sidebar_quick_more_button.winfo_manager() == "place"
        app.hide_sidebar_quick_actions()

        # ================================================================
        # Eigenschaften im Seitenkopf (AO-060), Leerzustände (MO-050)
        # ================================================================
        heute = mod.date.today()
        chipliste = app.new_list_object("Chipliste", [
            app.new_item("Offen morgen", due=(heute + mod.timedelta(days=1)).isoformat()),
            app.new_item("Überfällig", due=(heute - mod.timedelta(days=2)).isoformat()),
            app.new_item("Erledigt", done=True)])
        chipliste["items"][0]["labels"] = [rot["id"]]
        app.lists.append(chipliste)
        app.save_items()
        app.set_active_list(chipliste["id"])
        root.update()
        assert app.page_chips() == ["2 offen", "1 erledigt", "1 überfällig", "nächste Fälligkeit morgen", "1 Label"]
        assert app.page_chip_row.winfo_manager() == "pack"
        # U10 setzt die Unterzeile in einen eigenen Elternrahmen. Daher die
        # tatsächlichen Fensterpositionen vergleichen, nicht Elternkoordinaten.
        assert app.page_chip_row.winfo_rooty() >= app.title_row.winfo_rooty() + app.title_row.winfo_height()
        # Seit dem 26.09.2026 Text mit Trennpunkt statt Kästen.
        texte = [widget.cget("text").removeprefix("·  ") for widget in app.page_chip_row.winfo_children()
                 if not getattr(widget, "_is_backdrop", False)]
        assert texte == app.page_chips()
        assert app.relative_day_text(heute.isoformat()) == "heute"
        assert app.relative_day_text((heute + mod.timedelta(days=3)).isoformat()) == "in 3 Tagen"
        app.set_active_folder(eltern["id"])
        root.update()
        assert app.page_chips()[0].endswith(("Seite", "Seiten"))
        app.set_home_view()
        root.update()
        # Seit 27.09.2026 steht dort der Untertitel der Startseite – ohne Kennzahlen.
        assert not app.page_chips() and app.header_note_text() == ""
        app.toggle_view_hints();root.update()
        assert app.header_note_text().startswith("Dein Überblick")
        # Leere Liste: Satz in der Leerzeile. Seit 3.33.20 (U20) gibt es keinen
        # zweiten Anlegen-Knopf in der Fläche, wenn die Eingabezeile sichtbar ist.
        leer = app.new_list_object("Ganz leer", [])
        app.lists.append(leer)
        app.save_items()
        app.set_active_list(leer["id"])
        root.update()
        assert app.entry_line_visible()
        knopf = getattr(app, "empty_action_button", None)
        assert knopf is None or knopf.winfo_manager() == ""
        # Ausbau MO-050: Gismo steht klein und still unter dem Leertext (Stufe 2).
        figur = app.empty_state_figure
        assert figur is not None and figur.winfo_manager() == "place" and figur.state_name == "ruhig"
        assert not figur._jobs, "Kein Blinzeln im Leerzustand"
        app.settings["mascot_playful"] = False
        app.refresh_tree()
        root.update()
        assert figur.winfo_manager() == ""
        app.settings["mascot_playful"] = True
        app.refresh_tree()
        root.update()
        # Leere Suche: „Suche zurücksetzen“ leert den Filter.
        app.set_active_list(chipliste["id"])
        app.search_var.set("gibt es nirgends")
        app.refresh_tree()
        root.update()
        assert app.empty_action_button.text == "Suche zurücksetzen"
        app.empty_action_button.command()
        root.update()
        assert app.current_search_query() == "" and app.empty_action_button.winfo_manager() == ""
        # Leerer Ordner und leeres Tagebuch.
        leerer_ordner = app.new_folder_object("Leerer Ordner")
        leeres_tagebuch = app.new_folder_object("Leeres Tagebuch", folder_kind="journal")
        app.folders.extend([leerer_ordner, leeres_tagebuch])
        app.save_items()
        app.set_active_folder(leerer_ordner["id"])
        root.update()
        # Mit sichtbarer Eingabezeile genau ein Anlegeweg (U20); ohne sie der Knopf.
        if app.entry_line_visible():
            assert app.empty_action_button.winfo_manager() == ""
        else:
            assert app.empty_action_button.text == "Neue Liste anlegen"
        app.set_active_folder(leeres_tagebuch["id"])
        root.update()
        # Ein Notizbucheintrag trägt seinen Tag; die Eingabezeile legt nur eine
        # gewöhnliche Liste an. Der eigene Weg bleibt deshalb (U20).
        assert app.empty_action_button.text == "Ersten Eintrag anlegen"
        app.empty_action_button.command()
        root.update()
        assert app.current_list()["folder_id"] == leeres_tagebuch["id"]
        # Papierkorb leer: zurück zur Startseite.
        app.trash = []
        app.set_trash_view()
        root.update()
        assert app.empty_action_button.text == "Zur Startseite"
        # Leere Pinnwand: „Punkte anheften“ auf der Fläche.
        app.set_active_list(leer["id"])
        app.workspace.set_mode("board")
        root.update()
        assert app.workspace._empty_board_button.command == app.workspace.choose_cards
        assert len(app.workspace.canvas.find_withtag("emptyaction")) == 2
        assert app.workspace._empty_board_figure.bg_key == "bg"
        app.workspace.set_mode("list")
        root.update()

        # ================================================================
        # Design „Pixel“ (MO-060)
        # ================================================================
        vorheriges_design = app.design_name()
        assert "pixel" in app.DESIGN_ORDER and app.DESIGNS["pixel"]["partner"] == "pixel"
        app.set_design("pixel", apply_now=False)
        tafel = app.active_theme()
        assert app.color_mode() == "pixel" and app.theme_name == "dark" and app.is_pixel_design()
        for flaeche in ("bg", "card", "input", "hover"):
            for schrift, schwelle in (("text", 4.5), ("muted", 4.5), ("placeholder", 3.0)):
                wert = mod.contrast_ratio(tafel[flaeche], tafel[schrift])
                assert wert >= schwelle, (flaeche, schrift, wert)
        assert mod.contrast_ratio(tafel["selection"], tafel["selection_text"]) >= 4.5
        assert {tafel["clear"], tafel["flag"], tafel["accent"]} == {"#3D7BFF", "#FFD21F", "#FF3EA5"}
        app.set_design("pixel")
        app.set_home_view()
        root.update()
        koepfe = [widget for widget in descendants(app.home_content) if getattr(widget, "pixel_block", False)]
        assert len(koepfe) >= 3
        assert {kopf.cget("bg") for kopf in koepfe} == {tafel["clear"], tafel["flag"], tafel["accent"]}
        assert all(mod.contrast_ratio(kopf.cget("bg"), kopf.cget("fg")) >= 4.5 for kopf in koepfe)
        # Ausbau MO-060: Pixelschrift (Pixelify Sans, SIL OFL) für Seitentitel und Kachelköpfe.
        fonts = ROOT / "src/glide/resources/fonts"
        herkunft = json.loads((fonts / "provenance.json").read_text(encoding="utf-8"))["additional_sources"][0]
        for datei, pruefsumme in herkunft["files"].items():
            assert hashlib.sha256((fonts / datei).read_bytes()).hexdigest() == pruefsumme, datei
        assert "SIL Open Font License" in (fonts / "OFL-PixelifySans.txt").read_text(encoding="utf-8")
        if mod.IS_MACOS or mod.IS_WINDOWS:
            assert app.pixel_heading_family() == "Pixelify Sans"
            assert mod.tkfont.Font(font=app.title_label.cget("font")).actual("family") == "Pixelify Sans"
            assert all(mod.tkfont.Font(font=kopf.cget("font")).actual("family") == "Pixelify Sans" for kopf in koepfe)
        # Dritter Ausbau: Unter Linux nimmt Fontconfig den Schriftordner prozessweit auf.
        aufrufe = []

        def fc_ordner(config, pfad):
            aufrufe.append((config, pfad))
            return 1

        def cdll_ersatz(ergebnis):
            def laden(name):
                if name != "libfontconfig.so.1" or ergebnis is None:
                    raise OSError(name)
                return ergebnis
            return laden

        plattform = {"IS_LINUX": True, "IS_WINDOWS": False, "IS_MACOS": False}
        alt_plattform = {name: getattr(mod, name) for name in plattform}
        alt_cdll = mod.ctypes.CDLL
        try:
            for name, wert in plattform.items():
                setattr(mod, name, wert)
            mod.ctypes.CDLL = cdll_ersatz(SimpleNamespace(FcConfigAppFontAddDir=fc_ordner))
            pfade = mod.register_private_fonts(str(fonts))
            assert aufrufe == [(None, os.fsencode(str(fonts)))]
            assert any(pfad.endswith("PixelifySans-Regular.ttf") for pfad in pfade)
            assert fc_ordner.restype is mod.ctypes.c_int
            # Ohne libfontconfig bleibt es bei der Oberflächenschrift.
            mod.ctypes.CDLL = cdll_ersatz(None)
            assert mod.register_private_fonts(str(fonts)) == []
        finally:
            mod.ctypes.CDLL = alt_cdll
            for name, wert in alt_plattform.items():
                setattr(mod, name, wert)
        assert app.thumbnail_frame_options()["highlightthickness"] == 3
        app.set_active_list(gruppenliste["id"])
        app.workspace.set_mode("board")
        root.update()
        assert app.workspace.canvas.find_withtag("pixelblock")
        app.workspace.set_mode("list")
        app.set_design(vorheriges_design)
        root.update()
        assert not app.is_pixel_design() and app.thumbnail_frame_options()["highlightthickness"] == 0
        assert app.pixel_heading_family() is None
        assert mod.tkfont.Font(font=app.title_label.cget("font")).actual("family") != "Pixelify Sans"
        # Eine ältere Fassung kennt „pixel“ nicht und fällt auf ein gültiges Design zurück.
        alt = app.normalize_personal_settings({"design": "gibtsnicht", "theme": "dark", "color_mode": "pixel",
                                               "glass_mode": True})
        assert alt["design"] == "glass_dark"

        # ================================================================
        # Eingebetteter Detailbereich (MO-030)
        # ================================================================
        d1, d2 = app.new_item("Detail eins", due=heute.isoformat()), app.new_item("Detail zwei")
        detailliste = app.new_list_object("Detailliste", [d1, d2])
        app.lists.append(detailliste)
        app.save_items()
        # Der Schnappschuss ist neutral: Übernehmen ohne Eingabe ändert nichts.
        probe = copy.deepcopy(d1)
        assert app.apply_item_details(probe, app.item_details_snapshot(probe)) is False
        app.set_active_list(detailliste["id"])
        root.update()
        assert not app.detail_pane_enabled()
        app.toggle_detail_pane()
        root.update()
        assert app.detail_pane.winfo_manager() == "pack" and app.detail_pane.winfo_toplevel() is root
        app.tree.selection_set(d1["id"])
        app.tree.focus(d1["id"])
        app.tree.event_generate("<<TreeviewSelect>>")
        root.update()
        felder = app._detail_state["fields"]
        assert app._detail_state["item_id"] == d1["id"] and felder["text"].get() == "Detail eins"
        felder["text"].delete(0, "end")
        felder["text"].insert(0, "Detail eins geändert")
        assert app.commit_detail_pane() is True
        assert app.find_item_in_lists(d1["id"])[0]["text"] == "Detail eins geändert"
        assert app.find_item_in_lists(d1["id"])[0]["due"] == heute.isoformat()
        app.undo_last_change()
        assert app.find_item_in_lists(d1["id"])[0]["text"] == "Detail eins"
        # Beim Wechsel der Auswahl geht keine Eingabe verloren.
        app.tree.selection_set(d1["id"])
        app.tree.event_generate("<<TreeviewSelect>>")
        root.update()
        app.sync_detail_pane(force=True)
        app._detail_state["fields"]["description"].insert("1.0", "Notiz aus dem Bereich")
        app.tree.selection_set(d2["id"])
        app.tree.focus(d2["id"])
        app.tree.event_generate("<<TreeviewSelect>>")
        root.update()
        assert app.find_item_in_lists(d1["id"])[0]["description"] == "Notiz aus dem Bereich"
        assert app._detail_state["item_id"] == d2["id"]
        assert app.tree.selection() == (d2["id"],)
        # Ungültiges Datum: Hinweis im Bereich, keine Übernahme.
        feld = app._detail_state["fields"]["due"]
        feld.date_entry.delete(0, "end")
        feld.date_entry.insert(0, "99.99.9999")
        assert app.commit_detail_pane() is False and app.detail_status.cget("text")
        assert app.find_item_in_lists(d2["id"])[0]["due"] is None
        app.sync_detail_pane(force=True)

        # Ausbau MO-030: alle Felder außer den Anhängen direkt im Bereich.
        def punkt(eintrag):
            return app.find_item_in_lists(eintrag["id"])[0]

        def felder_von(eintrag):
            app.tree.selection_set(eintrag["id"])
            app.tree.focus(eintrag["id"])
            app.tree.event_generate("<<TreeviewSelect>>")
            root.update()
            assert app._detail_state["item_id"] == eintrag["id"]
            return app._detail_state["fields"]

        felder = felder_von(d1)
        assert {"kind", "color", "repeat", "reminder", "time_spent_minutes", "links", "blocked_by"} <= set(felder)
        assert app._detail_state["canvas"] is not None, "Der Bereich scrollt"
        farbname, farbschluessel = app.ITEM_COLOR_CHOICES[0]
        felder["color"][0].set(farbname)
        root.update()
        assert punkt(d1)["color"] == farbschluessel
        teile = app._detail_state["fields"]["repeat"]
        teile["art"].set("an bestimmten Wochentagen")
        root.update()
        assert "Wochentag" in app.detail_status.cget("text") and not punkt(d1).get("repeat")
        teile["tage"][0].set(True)
        assert app.commit_detail_pane() is True
        assert punkt(d1)["repeat"]["art"] == app.REPEAT_WEEKDAYS and punkt(d1)["repeat"]["tage"] == [0]
        block = next(widget for widget in app.iter_descendants(app.detail_pane) if hasattr(widget, "mode_var"))
        assert block.cget("bg") == app.theme["card"], "Der Maskenbaustein passt sich dem Bereich an"
        block.mode_var.set("1 Tag vorher")
        root.update()
        assert punkt(d1)["reminder"]["mode"] == "relative" and punkt(d1)["reminder"]["minutes"] == 1440
        feld = app._detail_state["fields"]["time_spent_minutes"]
        feld.delete(0, "end")
        feld.insert(0, "25")
        assert app.commit_detail_pane() is True and punkt(d1)["time_spent_minutes"] == 25
        assert app.add_detail_pane_step(d1["id"], "  Erster   Schritt ")
        assert [schritt["text"] for schritt in punkt(d1)["checklist"]] == ["Erster Schritt"]
        app.remove_detail_pane_step(d1["id"], 0)
        assert punkt(d1)["checklist"] == []
        app.choose_items_dialog = lambda *args, **kwargs: [d2["id"]]
        app.add_detail_pane_relation("links", False, "Verknüpfen …", "Verknüpft mit")
        assert punkt(d1)["links"] == [d2["id"]]
        app.add_detail_pane_relation("blocked_by", True, "Voraussetzung …", "Wartet auf")
        assert punkt(d1)["blocked_by"] == [d2["id"]]
        # Kreise lehnt der Bereich ab wie die Maske.
        felder_von(d2)
        app.choose_items_dialog = lambda *args, **kwargs: [d1["id"]]
        app.add_detail_pane_relation("blocked_by", True, "Voraussetzung …", "Wartet auf")
        assert errors and errors.pop()[0] == "Abhängigkeit abgelehnt" and not punkt(d2).get("blocked_by")
        del app.choose_items_dialog
        felder_von(d1)
        app.remove_detail_pane_relation("links", d2["id"])
        assert punkt(d1)["links"] == [] and punkt(d1)["blocked_by"] == [d2["id"]]
        # Zweiter Ausbau: Anhänge direkt im Bereich.
        quelle = Path(mod.BASE_DIR) / "detail-anhang.txt"
        quelle.write_text("Anhang aus dem Detailbereich", encoding="utf-8")
        original_dialog = mod.filedialog.askopenfilenames
        mod.filedialog.askopenfilenames = lambda *args, **kwargs: (str(quelle),)
        try:
            felder_von(d1)
            app.add_detail_pane_attachments()
            app.add_detail_pane_attachments()  # dieselbe Datei nicht doppelt
        finally:
            mod.filedialog.askopenfilenames = original_dialog
        anhaenge = punkt(d1)["attachments"]
        assert len(anhaenge) == 1 and anhaenge[0]["name"] == "detail-anhang.txt"
        assert Path(app.resolve_attachment_path(anhaenge[0])).read_text(encoding="utf-8") == "Anhang aus dem Detailbereich"
        geoeffnet_anhang = []
        app.open_external_path = lambda pfad: geoeffnet_anhang.append(pfad)
        app.open_detail_pane_attachment(0)
        del app.open_external_path
        assert geoeffnet_anhang and geoeffnet_anhang[0] == app.resolve_attachment_path(anhaenge[0])
        app.remove_detail_pane_attachment(0)
        assert punkt(d1)["attachments"] == []
        app.undo_last_change()
        assert len(punkt(d1)["attachments"]) == 1
        felder = felder_von(d1)
        felder["kind"][0].set(app.ITEM_KIND_NAMES[app.ITEM_KIND_LONG])
        root.update()
        assert app.item_kind(punkt(d1)) == app.ITEM_KIND_LONG
        felder = felder_von(d1)
        assert isinstance(felder["text"], mod.tk.Text), "Long-Task: mehrzeiliger Titel"
        app.ask_yes_no = lambda *args, **kwargs: False
        felder["kind"][0].set(app.ITEM_KIND_NAMES[app.ITEM_KIND_GROUP])
        root.update()
        assert app.item_kind(punkt(d1)) == app.ITEM_KIND_LONG and punkt(d1)["due"] == heute.isoformat()
        app.ask_yes_no = lambda *args, **kwargs: True
        felder = felder_von(d1)
        felder["kind"][0].set(app.ITEM_KIND_NAMES[app.ITEM_KIND_TASK])
        root.update()
        assert app.item_kind(punkt(d1)) == app.ITEM_KIND_TASK
        # Tabelle: Enter öffnet den Bereich statt der Maske.
        app.set_table_view()
        root.update()
        app.tree.selection_set(d1["id"])
        app.tree.focus(d1["id"])
        maske_offen = []
        original_maske = app.themed_item_details_dialog
        app.themed_item_details_dialog = lambda *args, **kwargs: maske_offen.append(True)
        try:
            app.activate_tree_row()
            root.update()
        finally:
            app.themed_item_details_dialog = original_maske
        assert not maske_offen and app._detail_state["item_id"] == d1["id"]
        app.open_list_view()
        root.update()
        # Breite ziehen und merken.
        app.detail_sash.event_generate("<ButtonPress-1>", x=2, y=10, rootx=900, rooty=300)
        app._detail_sash_press(SimpleNamespace(x_root=900))
        app._detail_sash_drag(SimpleNamespace(x_root=860))
        app._detail_sash_release(SimpleNamespace(x_root=860))
        root.update()
        assert app.settings["detail_pane_width"] == int(app.detail_pane.cget("width"))
        assert app.DETAIL_PANE_WIDTH_RANGE[0] <= app.settings["detail_pane_width"] <= app.DETAIL_PANE_WIDTH_RANGE[1]
        # Schmales Fenster: die Maske bleibt, der Bereich verschwindet.
        root.geometry("900x800+20+20")
        root.update()
        app.sync_detail_pane()
        assert app.detail_pane.winfo_manager() == ""
        root.geometry("1280x900+20+20")
        root.update()
        app.sync_detail_pane()
        assert app.detail_pane.winfo_manager() == "pack"
        app.toggle_detail_pane()
        root.update()
        assert app.detail_pane.winfo_manager() == "" and not app.detail_pane_enabled()
        assert app.normalize_personal_settings({"detail_pane": "ja", "detail_pane_width": 5000})[
            "detail_pane_width"] == 640

        # ================================================================
        # Vorlagen mit Eingabefeldern
        # ================================================================
        assert app.fill_template_text("Projekt {{ Projektname }} am {{Datum}}", {"Projektname": "Nord",
                                                                                 "Datum": "25.09.2026"}) == \
            "Projekt Nord am 25.09.2026"
        notiz = {"text": "Kunde {{Kunde}} anrufen", "spans": [{"tag": "bold", "start": 0, "end": 5},
                                                               {"tag": "italic", "start": 6, "end": 15},
                                                               {"tag": "underline", "start": 16, "end": 23}],
                 "links": {}}
        gefuellt = app.fill_template_rich_note(notiz, {"Kunde": "Mayer GmbH"})
        assert gefuellt["text"] == "Kunde Mayer GmbH anrufen"
        assert [(span["start"], span["end"]) for span in gefuellt["spans"]] == [(0, 5), (6, 16), (17, 24)]
        assert gefuellt["text"][17:24] == "anrufen"
        mod.RichNoteEditor.normalize(gefuellt)
        vorlage_quelle = app.new_list_object("Projekt {{Projektname}}", [
            app.new_item("Angebot für {{Kunde}} schreiben", description="Termin am {{Datum}}"),
            app.new_item("Ortstermin in {{ Ort }}")])
        vorlage_quelle["items"][0]["checklist"] = [{"text": "{{Kunde}} anrufen", "done": False}]
        app.lists.append(vorlage_quelle)
        app.save_items()
        vorlage = app.capture_template(list_id=vorlage_quelle["id"])
        assert app.template_fields(vorlage) == ["Projektname", "Kunde", "Datum", "Ort"]
        assert app.template_field_default("Datum") == heute.strftime("%d.%m.%Y")
        abgefragt = []

        def ausfuellen(felder, titel=""):
            abgefragt.append((tuple(felder), titel))
            return {"Projektname": "Nordbahnhof", "Kunde": "Mayer", "Datum": "01.10.2026", "Ort": "Linz"}

        app.ask_template_fields = ausfuellen
        vorher_ids = {entry["id"] for entry in app.lists}
        neu = app.create_list_from_template(vorlage["id"])
        # Seit 3.32.0 (G11) füllt sich {{Datum}} selbst und wird nicht gefragt.
        assert abgefragt and abgefragt[0][0] == ("Projektname", "Kunde", "Ort"), abgefragt
        neu = next(entry for entry in app.lists if entry["id"] not in vorher_ids)
        assert neu["title"] == "Projekt Nordbahnhof"
        punkte = list(app.walk_items(neu["items"]))
        assert [punkt["text"] for punkt in punkte] == ["Angebot für Mayer schreiben", "Ortstermin in Linz"]
        assert punkte[0]["description"] == "Termin am 01.10.2026"
        assert punkte[0]["checklist"][0]["text"] == "Mayer anrufen"
        # Die Vorlage selbst bleibt unverändert.
        assert app.template_by_id(vorlage["id"])["title"] == "Projekt {{Projektname}}"
        # Abbrechen legt nichts an.
        app.ask_template_fields = lambda *args, **kwargs: None
        anzahl = len(app.lists)
        assert app.create_list_from_template(vorlage["id"]) is None and len(app.lists) == anzahl
        del app.ask_template_fields

        # ================================================================
        # Zeitblöcke in „Mein Tag“ (AO-070)
        # ================================================================
        tag = heute.isoformat()
        z1 = app.new_item("Block Planung", planned_date=tag)
        z1.update(planned_time="09:00", estimated_minutes=60)
        z2 = app.new_item("Block Anruf", planned_date=tag)
        z2.update(planned_time="09:30")
        z3 = app.new_item("Block Mittag", planned_date=tag)
        z3.update(planned_time="11:00", estimated_minutes=30)
        z4 = app.new_item("Ohne Uhrzeit", planned_date=tag)
        zeitliste = app.new_list_object("Zeitplan", [z1, z2, z3, z4])
        app.lists.append(zeitliste)
        app.save_items()
        bloecke = app.time_blocks([(zeitliste, z) for z in (z3, z2, z1, z4)])
        assert [(block["start"], block["end"], block["overlap"]) for block in bloecke] == [
            ("09:00", "10:00", True), ("09:30", "", True), ("11:00", "11:30", False)]
        app.set_plan_day_view()
        root.update()
        assert app.tree.exists(app.TIMEPLAN_SECTION_ROW_ID) and app.tree.exists(app.UNTIMED_SECTION_ROW_ID)
        zeilen = [app.tree.item(iid, "text") for iid in app.tree.get_children(app.TIMEPLAN_SECTION_ROW_ID)]
        assert zeilen[0].startswith("09:00–10:00 · überschneidet sich")
        assert zeilen[1].startswith("09:30 · überschneidet sich") and zeilen[2].startswith("11:00–11:30   ")
        assert "Zeitplan · 3 Blöcke · 09:00–11:30" in app.tree.item(app.TIMEPLAN_SECTION_ROW_ID, "text")
        ohne_zeilen = [app.tree.item(iid, "text") for iid in app.tree.get_children(app.UNTIMED_SECTION_ROW_ID)]
        assert any("Ohne Uhrzeit" in zeile for zeile in ohne_zeilen)
        assert not any("Block " in zeile for zeile in ohne_zeilen)
        # Zugeklappt übersteht der Abschnitt den Neuaufbau.
        app.set_overview_section_open(app.TIMEPLAN_SECTION_ROW_ID, False)
        app.refresh_tree()
        assert app.tree.item(app.TIMEPLAN_SECTION_ROW_ID, "open") in (0, False, "0", "false")
        app.set_overview_section_open(app.TIMEPLAN_SECTION_ROW_ID, True)

        # Ausbau AO-070: Ziehen setzt die Uhrzeit, Alt+↑/↓ schiebt um 15 Minuten.
        app.refresh_tree()
        root.update()

        def zeile(punkt):
            return f"in-progress:{zeitliste['id']}:{punkt['id']}"

        def aktuell(punkt):
            return app.find_item_in_lists(punkt["id"])[0]

        def zeilenbox(punkt):
            app.tree.see(zeile(punkt))
            root.update()
            box = app.tree.bbox(zeile(punkt))
            assert box, "Zeitplanzeile muss sichtbar sein"
            return box

        # Untere Hälfte von „Block Mittag“ (11:00–11:30): der Anruf beginnt am Blockende.
        box = zeilenbox(z3)
        assert app.time_plan_drop(zeile(z3), [zeile(z2)], box[1] + box[3] - 2)
        assert aktuell(z2)["planned_time"] == "11:30" and aktuell(z2)["planned_date"] == tag
        # Obere Hälfte von „Block Planung“ (09:00): der Anruf (30 Minuten) endet dort.
        box = zeilenbox(z1)
        assert app.time_plan_drop(zeile(z1), [zeile(z2)], box[1] + 2)
        assert aktuell(z2)["planned_time"] == "08:30"
        # Aus „Ohne Uhrzeit“ auf die Kopfzeile: vor den ersten Block.
        assert app.time_plan_drop(app.TIMEPLAN_SECTION_ROW_ID, [zeile(z4)], 0)
        assert aktuell(z4)["planned_time"] == "08:00"
        # Alt+↑ schiebt 15 Minuten früher, die Auswahl bleibt für den nächsten Schritt.
        app.tree.selection_set([zeile(z4)])
        app.move_selected_items(-1)
        assert aktuell(z4)["planned_time"] == "07:45" and zeile(z4) in app.tree.selection()
        app.undo_last_change()
        assert aktuell(z4)["planned_time"] == "08:00"
        # Nach „Ohne Uhrzeit“ gezogen, verliert der Punkt die Uhrzeit.
        assert app.time_plan_drop(app.UNTIMED_SECTION_ROW_ID, [zeile(z4)], 0)
        assert aktuell(z4)["planned_time"] is None
        # Ziehen auf sich selbst oder außerhalb des Zeitplans ändert nichts.
        assert not app.time_plan_drop(zeile(z3), [zeile(z3)], 0)
        assert not app.time_plan_drop(None, [zeile(z3)], 0)

        # Zweiter Ausbau: Stundenraster neben dem Zeitplan.
        assert not app.plan_grid_enabled()
        app.toggle_plan_day_grid()
        root.update()
        assert app.plan_grid_frame.winfo_manager() == "pack" and app.plan_day_grid_button.text == "Raster ✓"
        blockdaten = app._plan_grid_blocks
        assert set(blockdaten) >= {z1["id"], z2["id"], z3["id"]} and z4["id"] not in blockdaten
        _block, (x1, y1, x2, y2) = blockdaten[z3["id"]]
        vorher_z3 = aktuell(z3)["planned_time"]
        mitte_x, oben_y = int((x1 + x2) / 2), int(y1 + 4)
        leinwand = app.plan_grid_canvas
        leinwand.yview_moveto(0)
        root.update()
        dy = int(leinwand.canvasy(0))
        app.plan_grid_press(SimpleNamespace(x=mitte_x, y=oben_y - dy))
        app.plan_grid_motion(SimpleNamespace(x=mitte_x, y=oben_y - dy + 24))
        app.plan_grid_release(SimpleNamespace(x=mitte_x, y=oben_y - dy + app.PLAN_GRID_HOUR_PX))
        stunden, minuten = (int(teil) for teil in vorher_z3.split(":"))
        assert aktuell(z3)["planned_time"] == app.clock_text(stunden * 60 + minuten + 60), "eine Stunde später"
        app.undo_last_change()
        assert aktuell(z3)["planned_time"] == vorher_z3
        # Dritter Ausbau: Ein Punkt ohne Uhrzeit wird aus der Liste ins Raster gezogen.
        assert aktuell(z4)["planned_time"] is None
        box = zeilenbox(z4)
        leinwand.yview_moveto(0)
        root.update()
        start = SimpleNamespace(x=box[0] + 30, y=box[1] + 2, x_root=0, y_root=0, state=0)
        app.on_time_plan_drag_start(start)
        assert app.drag_start_id == zeile(z4), "Punktzeile ohne Uhrzeit ist greifbar"
        ziel_x = leinwand.winfo_rootx() + leinwand.winfo_width() // 2
        ziel_y = leinwand.winfo_rooty() + leinwand.winfo_height() // 2
        erwartet = app.plan_grid_minutes_at(ziel_x, ziel_y)
        assert erwartet is not None and erwartet % app.TIME_PLAN_STEP_MINUTES == 0
        assert app.plan_grid_minutes_at(ziel_x - leinwand.winfo_width(), ziel_y) is None
        zug = SimpleNamespace(x=start.x + 200, y=start.y + 5, x_root=ziel_x, y_root=ziel_y, state=0)
        app.on_time_plan_drag_motion(zug)
        assert leinwand.find_withtag("drop_preview"), "Vorschaulinie im Raster"
        app.on_time_plan_drag_end(zug)
        assert not leinwand.find_withtag("drop_preview")
        assert aktuell(z4)["planned_time"] == app.clock_text(erwartet) and aktuell(z4)["planned_date"] == tag
        assert z4["id"] in app._plan_grid_blocks
        app.undo_last_change()
        assert aktuell(z4)["planned_time"] is None
        # Unter 900 px Fensterbreite und außerhalb von „Mein Tag“ bleibt es verborgen.
        app.set_active_list(zeitliste["id"])
        root.update()
        assert app.plan_grid_frame.winfo_manager() == ""
        app.set_plan_day_view()
        root.update()
        assert app.plan_grid_frame.winfo_manager() == "pack"
        # Erweiterung: Unter 900 px steht das Raster statt der Liste.
        def resize_plan_window(width):
            height = max(700, root.winfo_height())
            root.geometry(f"{width}x{height}")
            # Windows übernimmt WM-Größenänderungen asynchron. Erst die
            # tatsächliche Größe prüfen, dann den Layoutvertrag testen.
            for _attempt in range(25):
                root.update()
                if root.winfo_width() == width and root.winfo_height() == height:
                    break
                root.after(20, root.quit)
                root.mainloop()
            assert (root.winfo_width(), root.winfo_height()) == (width, height), root.geometry()
            app.sync_plan_day_grid()
            root.update()

        breite_vorher = root.winfo_width()
        resize_plan_window(860)
        assert app.plan_grid_replaces_list()
        assert app.plan_grid_frame.winfo_manager() == "pack" and not app.list_frame.winfo_manager()
        resize_plan_window(max(1280, breite_vorher))
        assert not app.plan_grid_replaces_list()
        assert app.list_frame.winfo_manager() == "pack" and app.plan_grid_frame.winfo_manager() == "pack"
        # Ein Wechsel der Ansicht holt die Liste auch aus dem schmalen Zustand zurück.
        resize_plan_window(860)
        app.set_active_list(zeitliste["id"])
        root.update()
        assert app.list_frame.winfo_manager() == "pack" and app.plan_grid_frame.winfo_manager() == ""
        resize_plan_window(max(1280, breite_vorher))
        app.set_plan_day_view()
        root.update()
        app.toggle_plan_day_grid()
        root.update()
        assert app.plan_grid_frame.winfo_manager() == "" and not app.plan_grid_enabled()
        # Erweiterung: Aus einer normalen Liste auf „Mein Tag“ in der Seitenleiste ziehen plant ein.
        spaeter = app.new_item("Aus der Liste einplanen")
        # Rückgängig ersetzt die Listenobjekte; die Liste frisch aus dem Bestand holen.
        next(entry for entry in app.lists if entry["id"] == zeitliste["id"])["items"].append(spaeter)
        app.save_items()
        app.set_active_list(zeitliste["id"])
        root.update()
        app.drag_start_id = spaeter["id"]
        app.drag_item_ids = [spaeter["id"]]
        app.drag_has_moved = True
        seitenleiste = app.identify_sidebar_drop_row
        app.identify_sidebar_drop_row = lambda event=None: (app.PLAN_DAY_ROW_ID, ("view", app.PLAN_DAY_VIEW))
        try:
            app.on_drag_end(SimpleNamespace(x=5, y=5, x_root=5, y_root=5, state=0))
        finally:
            app.identify_sidebar_drop_row = seitenleiste
        root.update()
        eingeplant = app.find_item_in_lists(spaeter["id"])
        assert eingeplant and eingeplant[0]["planned_date"] == app.plan_day(), "eingeplant statt verschoben"
        assert eingeplant[3]["id"] == zeitliste["id"], "bleibt in seiner Liste"
        app.undo_last_change()
        assert not app.find_item_in_lists(spaeter["id"])[0].get("planned_date")

        # ================================================================
        # Präsentationsmodus (MO-080)
        # ================================================================
        praesentation = app.new_list_object("Präsentation", [app.new_item("Folienpunkt")])
        app.lists.append(praesentation)
        app.save_items()
        app.set_active_list(praesentation["id"])
        flaeche = app.workspace
        flaeche.set_mode("board")
        flaeche.configure_board("layout", "free")
        root.update()
        infos = []
        app.show_info = lambda *args, **kwargs: infos.append(args)
        flaeche.start_presentation()
        assert infos and not flaeche.presentation_active()
        app.show_info = lambda *args, **kwargs: None
        zaehler = iter(["Einleitung", "Ergebnis"])
        app.themed_input_dialog = lambda *args, **kwargs: next(zaehler)
        flaeche.create_area(around_selection=False, point=(24, 24))
        flaeche.create_area(around_selection=False, point=(700, 24))
        zoom_vorher = flaeche.board()["zoom"]
        flaeche.start_presentation()
        root.update()
        assert flaeche.presentation_active() and flaeche.board_focus_active()
        texte = [flaeche.canvas.itemcget(element, "text") for element in flaeche.canvas.find_withtag("presentation")]
        assert texte and texte[0].startswith("Folie 1 / 2 · Einleitung")
        flaeche.next_card(1)
        root.update()
        assert flaeche._presentation["index"] == 1 and flaeche.selected_area == flaeche.area_list()[1]["id"]
        flaeche.board_escape()
        root.update()
        assert not flaeche.presentation_active() and not flaeche.board_focus_active()
        assert flaeche.board()["zoom"] == zoom_vorher
        # Ausbau MO-080: die Folien als Druckseite – drucken oder als PDF sichern.
        erster = flaeche.area_list()[0]
        karte = praesentation["items"][0]["id"]
        flaeche.pin([karte])
        flaeche.store_position(karte, erster["x"] + 24, erster["y"] + 48, reveal=False)
        root.update()
        assert karte in flaeche.cards_in_area(erster)
        seiten = flaeche.build_presentation_print_html()
        assert seiten.count('<section class="slide">') == 2 and "size: A4 landscape" in seiten
        folie1, folie2 = seiten.split('<section class="slide">')[1:]
        assert "Einleitung" in folie1 and "Folie 1 / 2" in folie1 and "transform:scale(" in folie1
        assert "Folienpunkt" in folie1 and "Folienpunkt" not in folie2 and "Ergebnis" in folie2
        geoeffnet = []
        app.open_external_path = lambda pfad: geoeffnet.append(pfad)
        flaeche.print_presentation()
        assert geoeffnet and Path(geoeffnet[-1]).read_text(encoding="utf-8") == seiten
        Path(geoeffnet[-1]).unlink()
        # Die normale Druckseite nutzt denselben Kartenbaustein weiter.
        assert "Folienpunkt" in flaeche.build_board_print_html()
        flaeche.set_mode("list")
        # Notiz: Überschriften werden zu Folien.
        dokument = {"text": "Vorwort\nZiel\nWir bauen.\nPlan\nSchritt eins",
                    "spans": [{"tag": "h1", "start": 8, "end": 12}, {"tag": "h2", "start": 24, "end": 28}],
                    "links": {}}
        folien = app.note_slides(dokument)
        assert folien == [("", "Vorwort"), ("Ziel", "Wir bauen."), ("Plan", "Schritt eins")]
        assert app.note_slides({"text": "Nur Text", "spans": []}) == [("", "Nur Text")]
        notizseite = app.new_list_object("Vortrag", [], list_kind="note", rich_note=dokument)
        app.lists.append(notizseite)
        app.save_items()
        app.set_active_list(notizseite["id"])
        root.update()
        app.start_note_presentation()
        root.update()
        zustand = app._note_presentation
        assert zustand and zustand["frame"].winfo_toplevel() is root and zustand["frame"].winfo_manager() == "place"
        assert zustand["footer"].cget("text").startswith("Folie 1 / 3")
        app.note_presentation_step(1)
        assert zustand["title"].cget("text") == "Ziel" and zustand["body"].cget("text") == "Wir bauen."
        app.end_note_presentation()
        assert app._note_presentation is None
        # Ausbau MO-080: Notizfolien als Druckseite.
        druck = app.build_note_slides_html("Vortrag", folien + [("<Tag>", "a & b")])
        assert druck.count('<section class="slide">') == 4 and "&lt;Tag&gt;" in druck and "a &amp; b" in druck
        assert "<h1>Vortrag</h1>" in druck, "Die Titelfolie ohne Überschrift trägt den Seitentitel"
        app.print_note_presentation()
        assert "Folie 3 / 3" in Path(geoeffnet[-1]).read_text(encoding="utf-8")
        Path(geoeffnet[-1]).unlink()
        del app.open_external_path

        # ================================================================
        # Referenz-Fixture Format 20 lädt ohne Umdeutung
        # ================================================================
        reference20 = json.loads((ROOT / "tests/fixtures/current_v20/reference_v20.json").read_text(encoding="utf-8"))
        # Die Referenz schrieb 3.30.0, die Version, mit der Format 20 kam; sie
        # bleibt über spätere Versionen gleich (seit 3.31.0 festgeschrieben).
        assert reference20["version"] == 20 and reference20["app_version"] == "3.30.0"
        geladen, _aktiv = app.normalize_lists_data(copy.deepcopy(reference20))
        assert geladen == reference20["lists"]
        beziehungen = next(entry for entry in geladen if entry["id"] == "fixture-tasks")
        assert beziehungen["items"][1]["blocked_by"] == ["fixture-item-prepare"]
        assert beziehungen["items"][2]["time_spent_minutes"] == 25 and beziehungen["icon"]["width"] == 16
        assert next(entry for entry in geladen if entry["id"] == "fixture-drawing-32")["drawing"]["width"] == 32
        assert next(entry for entry in geladen if entry["id"] == "fixture-archived")["archived"] is True

        root.update()
        assert not errors, errors

        # ================================================================
        # Mitbehoben: Unlesbare oder neuere Speicherdatei nie überschreiben.
        # Glide 3.29 hielt Format 20 für beschädigt, begann leer und ersetzte
        # die Datei bei der ersten Eingabe (Echtdatenprobe 25.09.2026).
        # ================================================================
        assert app.save_items(show_error=False)
        speicher = Path(mod.SAVE_FILE)
        gueltig = speicher.read_bytes()
        assert app.settings.get("data_format_written") == 23

        neuer = json.loads(gueltig)
        neuer["version"] = future_version
        speicher.write_text(json.dumps(neuer), encoding="utf-8")
        vorher = speicher.read_bytes()
        app.load_items()
        assert errors and errors.pop()[0] == "Bestand aus neuerer Glide-Version"
        assert app._data_read_only and app._read_only_reason == "newer_format"
        assert "neueren Glide-Version" in app.read_only_notice()
        assert app.save_items(show_error=False) is False
        assert speicher.read_bytes() == vorher
        app._data_read_only = False
        app._read_only_reason = "lock"

        speicher.write_text('{"version": 20, "lists": [', encoding="utf-8")
        kaputt = speicher.read_bytes()
        app.load_items()
        assert errors and "unverändert gesichert" in errors.pop()[1]
        kopien = sorted(Path(mod.BACKUP_DIR).glob("liste_unlesbar_*.json"))
        assert len(kopien) == 1 and kopien[0].read_bytes() == kaputt
        assert not app._data_read_only
        assert app.save_items(show_error=False), "Nach der Kopie muss Speichern wieder gehen"
        assert json.loads(speicher.read_text(encoding="utf-8"))["version"] == 23

        aelter = json.loads(gueltig)
        aelter["version"] = 19
        speicher.write_text(json.dumps(aelter), encoding="utf-8")
        app.load_items()
        assert errors and errors.pop()[0] == "Bestand von älterer Glide-Version gespeichert"
        assert app.save_items(show_error=False)
        app.load_items()
        assert not errors, errors
        speicher.write_bytes(gueltig)
        app.load_items()
        root.update()
        assert not errors, errors

        # ================================================================
        # Mitbehoben: Ein zweites Beenden (Cmd+Q während der Abfrage, von
        # macOS nachgereicht) leerte window.conf. Muss am Ende stehen, weil
        # es das Fenster schließt.
        # ================================================================
        fenster_datei = Path(mod.BASE_DIR) / "window.conf"
        fenster_datei.write_text("1200x820+40+40", encoding="utf-8")
        app.ask_yes_no_cancel = lambda *args, **kwargs: False
        app.on_close()
        gespeichert = fenster_datei.read_text(encoding="utf-8")
        assert gespeichert.split("x")[0].isdigit(), gespeichert
        app.on_close()
        assert fenster_datei.read_text(encoding="utf-8") == gespeichert
        assert not list(Path(mod.BASE_DIR).glob(".glide-window-*.tmp"))
        assert not errors, errors
        print("test_features330: OK")
    finally:
        try:
            root.destroy()
        except Exception:
            pass
