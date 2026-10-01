"""Isolierte Tk-Prüfung: Hilfe, Hinweise und verschachtelte Rückfragen."""

import ast
import importlib.machinery
import importlib.util
import os
import pathlib
import tempfile
import traceback


REPOSITORY_ROOT = pathlib.Path(__file__).parents[2]
SOURCE = REPOSITORY_ROOT / "src" / "glide" / "app.pyw"


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix="glide-dialog-test-") as temp_root:
    os.environ["GLIDE_DATA_DIR"] = temp_root
    loader = importlib.machinery.SourceFileLoader("glide_dialog_test", str(SOURCE))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    assert pathlib.Path(mod.BASE_DIR).resolve() == pathlib.Path(temp_root).resolve()

    # Der Dialog braucht keinen geladenen Aufgabenbestand und keinen Autosave.
    root = mod.tk.Tk()
    root.geometry("900x700+20+20")
    root.update()
    app = mod.ListApp.__new__(mod.ListApp)
    app.root = root
    app._after_ids = set()

    def inspect_next_dialog(check, choice="close"):
        errors = []

        def inspect():
            dialog = root.grab_current()
            try:
                assert isinstance(dialog, mod.tk.Toplevel), dialog
                dialog.update_idletasks()
                assert dialog.cget("background") == app.theme["bg"]
                check(dialog)
                if choice == "close":
                    dialog.tk.call(dialog.protocol("WM_DELETE_WINDOW"))
                else:
                    button = next(
                        widget for widget in descendants(dialog)
                        if isinstance(widget, mod.RoundedButton) and widget.text == choice
                    )
                    button.command()
            except Exception as exc:
                errors.append(traceback.format_exc())
            finally:
                if isinstance(dialog, mod.tk.Toplevel) and dialog.winfo_exists():
                    dialog.destroy()

        root.after(35, inspect)
        return errors

    def check_message(dialog):
        texts = [widget for widget in descendants(dialog) if isinstance(widget, mod.tk.Text)]
        assert len(texts) == 1
        assert texts[0].cget("background") == app.theme["bg"]
        assert texts[0].cget("foreground") == app.theme["text"]
        assert str(texts[0].cget("state")) == "disabled"

    try:
        for theme in ("dark", "light"):
            app.set_design(theme, apply_now=False)
            app.theme = app.THEMES[theme]
            for method, expected in ((app.show_info, "ok"), (app.show_warning, "ok"),
                                     (app.show_error, "ok"), (app.ask_yes_no, False),
                                     (app.ask_yes_no_cancel, None)):
                errors = inspect_next_dialog(check_message)
                assert method("Prüfung", "Ein Hinweis im aktuellen Theme.") == expected
                assert not errors, errors

            for method, choice, expected in (
                (app.ask_yes_no, "Ja", True), (app.ask_yes_no, "Nein", False),
                (app.ask_yes_no_cancel, "Ja", True), (app.ask_yes_no_cancel, "Nein", False),
                (app.ask_yes_no_cancel, "Abbrechen", None),
            ):
                errors = inspect_next_dialog(check_message, choice=choice)
                assert method("Rückfrage", "Fortfahren?") is expected
                assert not errors, errors

            def check_about(dialog):
                check_message(dialog)
                text = next(widget for widget in descendants(dialog) if isinstance(widget, mod.tk.Text))
                content = text.get("1.0", "end-1c")
                assert "Danke, dass du meine App benutzt." in content
                assert "Shaye.de – mailme@shaye.de" in content
                assert f"Version {mod.APP_VERSION}" in content
                assert "Warum mir Glide wichtig ist" in content
                assert mod.BASE_DIR in content
                # Auch auf niedrigem Bildschirm bleiben Text und Knopf erreichbar.
                dialog.geometry("600x340")
                dialog.update()
                dialog.update_idletasks()
                assert text.winfo_height() > 60, (dialog.winfo_height(), text.winfo_height())
                assert text.yview()[1] < 1
                knoepfe = [widget for widget in descendants(dialog)
                           if isinstance(widget, mod.RoundedButton)]
                for button in knoepfe:
                    assert button.winfo_y() + button.winfo_height() <= button.master.winfo_height()
                # Punkt 8 (3.25.0): „Über Glide“ führt zur Datenablage – die
                # Folgeaktionen stehen als eigene Flächen neben „OK“.
                beschriftungen = [button.text for button in knoepfe]
                assert "Arbeitsdateien verschieben" in beschriftungen, beschriftungen
                assert "Standardordner benutzen" in beschriftungen, beschriftungen
                assert "Ordner öffnen" in beschriftungen, beschriftungen
                # Jede Fläche zeigt ihre Beschriftung vollständig.
                for button in knoepfe:
                    assert int(button.cget("width")) >= button.text_width() + 8, button.text

            errors = inspect_next_dialog(check_about, choice="OK")
            assert app.show_about_dialog() == "ok"
            assert not errors, errors

            def check_shortcuts(dialog):
                labels = [widget for widget in descendants(dialog) if isinstance(widget, mod.tk.Label)]
                key = next(widget for widget in labels if widget.cget("text") == app.accel("T"))
                meaning = next(widget for widget in labels if widget.cget("text") == "Fälligkeitsdatum setzen oder entfernen")
                assert key.grid_info()["column"] == 0
                assert meaning.grid_info()["column"] == 1
                assert key.grid_info()["row"] == meaning.grid_info()["row"]
                assert mod.tkfont.Font(root=root, font=key.cget("font")).actual("weight") == "bold"
                assert mod.tkfont.Font(root=root, font=meaning.cget("font")).actual("weight") == "normal"
                assert all(widget.cget("background") == app.theme["bg"] for widget in labels)
                canvas = next(widget for widget in descendants(dialog)
                              if type(widget) is mod.tk.Canvas and widget.find_all())
                assert canvas.yview()[1] < 1
                for geometry in ("520x400", "900x650"):
                    dialog.geometry(geometry)
                    dialog.update()
                    dialog.update_idletasks()
                    assert meaning.winfo_x() + meaning.winfo_width() <= meaning.master.winfo_width() + 1
                    assert float(meaning.cget("wraplength")) > 100
                canvas.yview_moveto(1)
                assert canvas.yview()[0] > 0

            errors = inspect_next_dialog(check_shortcuts, choice="Schließen")
            app.show_shortcuts_dialog()
            assert not errors, errors

        # Der automatische Elternbezug muss auch ohne parent= den modalen
        # Eingabedialog treffen und dessen Griff anschließend wiederherstellen.
        parent = mod.tk.Toplevel(root)
        parent.grab_set()

        def check_nested(dialog):
            assert str(dialog.transient()) == str(parent)
            assert dialog.master is parent
            check_message(dialog)

        errors = inspect_next_dialog(check_nested, choice="Nein")
        assert app.ask_yes_no("Unterdialog", "Diesen Punkt ändern?") is False
        assert not errors, errors
        assert root.grab_current() is parent
        parent.destroy()

        # App-eigene Rückfragen dürfen nicht später wieder am Theme vorbei
        # direkt auf die native Tk-Messagebox ausweichen.
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        app_class = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "ListApp")
        assert not [node.lineno for node in ast.walk(app_class) if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "messagebox"]
    finally:
        app.cancel_pending_callbacks()
        root.destroy()

print("Dialog-Themes: OK (Hell/Dunkel, Rückgaben, Hilfe, Resize, modaler Unterdialog)")
