# SPDX-License-Identifier: MPL-2.0
"""UX-05: echte Tk-Eingabe, Wiederöffnen und Undo/Redo mit künstlichen Daten."""
import argparse
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))

with tempfile.TemporaryDirectory(prefix="glide-teil04-") as directory:
    os.environ["GLIDE_DATA_DIR"] = directory
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_inline_teil04", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    errors = []

    def open_app():
        root = mod.tk.Tk()
        root.geometry("1280x840+20+20")
        root.report_callback_exception = lambda *_exc: errors.append(repr(_exc[1]))
        app = mod.ListApp(root)
        app.show_error = lambda *a, **k: errors.append(repr(a))
        app.show_warning = lambda *a, **k: errors.append(repr(a))
        return root, app

    def settle():
        deadline = time.monotonic() + 0.25
        while time.monotonic() < deadline:
            root.update()
            time.sleep(0.01)
        assert not errors, errors

    root, app = open_app()
    try:
        entry = app.new_list_object("Inline-Test", [])
        app.lists.append(entry)
        label = app.new_label_object("Material")
        app.labels.append(label)
        list_id = entry["id"]
        assert app.save_items()
        app.set_active_list(list_id)
        settle()
        row = app.list_frame.nametowidget("inline_task_row")
        field = row.nametowidget("task")
        assert field.winfo_ismapped() and row.master is app.tree.master and field.winfo_rootx() >= app.tree.winfo_rootx()
        app.tree.focus_force()
        settle()
        # Griffachse (Design Richtlinien): Der Griff der Eingabezeile steht senkrecht
        # unter den Griffen der Aufgabenzeilen, gleich breit und gleich gezeichnet;
        # die Markierung beginnt, wo der Baum den Aufgabentext beginnt.
        app.add_item(raw_text="Achsenprobe")
        settle()
        app.show_quick_plan_row()
        settle()
        aufgabengriff = app._row_action_buttons[0]
        eingabegriff = app.inline_task_grip
        assert aufgabengriff.winfo_rootx() == eingabegriff.winfo_rootx(), (aufgabengriff.winfo_rootx(), eingabegriff.winfo_rootx())
        assert aufgabengriff.winfo_width() == eingabegriff.winfo_width()
        assert (aufgabengriff.font, aufgabengriff.text) == (eingabegriff.font, eingabegriff.text)
        erste = app.tree.get_children("")[0]
        assert app.inline_task_mark.winfo_rootx() == app.tree.winfo_rootx() + app.tree_text_inset(erste), (
            app.inline_task_mark.winfo_rootx(), app.tree.winfo_rootx(), app.tree_text_inset(erste))
        app.current_list()["items"].clear()
        assert app.save_items()
        app.refresh_tree()
        settle()
        app.inline_task_placeholder.event_generate("<Button-1>", x=4, y=4)
        settle()
        assert root.focus_get() is field
        field.insert(0, "Material sichten /morgen #Material")
        assert root.focus_get() is field and not app.get_entry_text()
        field.event_generate("<Return>")
        settle()
        item, = app.current_list()["items"]
        assert item["text"] == "Material sichten"
        assert item["planned_date"] == (mod.date.today() + mod.timedelta(days=1)).isoformat()
        assert label["id"] in item["labels"]
        assert app.tree.exists(item["id"]) and app.tree.bbox(item["id"])
        assert field.winfo_ismapped() and field.get() == "" and root.focus_get() is field
        field.event_generate("<Return>")
        settle()
        assert len(app.current_list()["items"]) == 1

        write = app.write_json_atomic

        def fail_data_write(path, data):
            if Path(path) == Path(mod.SAVE_FILE):
                raise OSError("synthetic data write failure")
            return write(path, data)

        field.insert(0, "Versuch mit Schreibfehler")
        app.write_json_atomic = fail_data_write
        field.event_generate("<Return>")
        app.write_json_atomic = write
        assert errors and "synthetic data write failure" in errors[-1], errors
        errors.pop()
        settle()
        assert field.get() == "Versuch mit Schreibfehler" and len(app.current_list()["items"]) == 1
        field.event_generate("<Escape>")

        field.insert(0, "Offener Entwurf")
        app.set_home_view()
        settle()
        assert not field.winfo_ismapped()
        app.set_active_list(list_id)
        settle()
        assert field.get() == "Offener Entwurf"
        field.focus_force()
        field.event_generate("<Escape>")
        assert field.get() == ""
        app.undo_last_change()
        settle()
        assert not app.current_list()["items"] and field.winfo_ismapped()
        app.redo_last_change()
        settle()
        assert app.current_list()["items"][0]["id"] == item["id"]
        app.set_table_view()
        settle()
        assert field.winfo_ismapped()
        app.search_placeholder_active = False
        app.search_var.set("keine Treffer")
        app.on_filter_changed()
        settle()
        assert not field.winfo_ismapped()
        app.reset_filters_for_empty_state()
        app._data_read_only = True
        app.refresh_tree()
        settle()
        assert not field.winfo_ismapped()
        app._data_read_only = False
        app.on_close()
        root, app = open_app()
        app.set_active_list(list_id)
        settle()
        assert app.current_list()["items"][0]["id"] == item["id"]
        assert app.inline_task_entry.winfo_ismapped()
    finally:
        if root.winfo_exists():
            app.on_close()
print("UX-05: Inline-Eingabe, Fokus, Entwurf, Undo/Redo und Wiederöffnen geprüft.")
