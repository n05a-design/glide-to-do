"""Kompakte Tabellenansicht mit listenspezifischer Spaltenauswahl."""
import copy
import importlib.machinery
import importlib.util
import os
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory(prefix="glide-features313-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features313", str(REPO / "src/glide/app.pyw"))
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
        target = app.new_list_object("Tabellenprüfung", [])
        app.lists.append(target)
        group = app.new_item("Abschnitt", kind=app.ITEM_KIND_GROUP)
        first = app.new_item("Konzept prüfen", due="2026-09-14", importance=2)
        second = app.new_item("Text freigeben", done=True, children=[])
        group["children"].append(first)
        target["items"].extend([group, second])
        app.set_active_list(target["id"])
        app.set_table_view()
        root.update()

        assert app.view_mode == app.TABLE_VIEW
        assert app.get_active_page() is target
        assert app.require_list_view(message=False)
        assert [item[1] for item in app.table_entries(apply_filters=False)] == [first, second]
        assert app.tree.exists(first["id"]) and app.tree.exists(second["id"])
        assert app.tree.exists(group["id"]) is False
        assert "headings" in str(app.tree.cget("show"))
        assert app.tree.heading("title", "text") == "Aufgabe"
        assert app.tree.heading("status", "text") == "Status"

        # Die Tabellenzeile arbeitet mit demselben Objekt und denselben Aktionen.
        app.tree.selection_set(first["id"])
        app.tree.focus(first["id"])
        before = copy.deepcopy(first)
        app.toggle_done()
        assert first["done"] is True and first["id"] == before["id"]
        app.toggle_done()
        assert first["done"] is False

        # Suche und „Nur offene Punkte“ gelten auch für die flache Darstellung.
        app.search_placeholder_active = False
        app.search_var.set("freigeben")
        root.update()
        assert [item[1] for item in app.table_entries()] == [second]
        app.search_var.set("")
        # Seit 3.27 gibt es keinen Schalter „Nur offene Punkte“ mehr. Ein
        # übrig gebliebener Variablenwert darf die Tabelle nicht still filtern.
        app.hide_done_var.set(True)
        assert app.get_filter_mode() == "all"
        assert [item[1] for item in app.table_entries()] == [first, second]
        app.hide_done_var.set(False)

        # Spaltenauswahl wird pro Liste in settings.json gespeichert und beim
        # Normalisieren um unbekannte Werte sowie die Pflichtspalte bereinigt.
        app.settings["table_columns"] = {target["id"]: ["title", "due", "bogus", "due"]}
        columns = app.table_columns_for_list(target["id"])
        assert columns == ["title", "due"]
        assert app.save_settings()
        loaded = app.load_settings()
        assert loaded["table_columns"][target["id"]] == ["title", "due"]
        assert mod.ListApp.normalize_personal_settings({"table_columns": {"x": ["due"]}})["table_columns"]["x"] == ["title", "due"]
        assert not errors, errors
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: Tabellenansicht, Filter, gemeinsame Punktaktionen und Spaltenpersistenz")
