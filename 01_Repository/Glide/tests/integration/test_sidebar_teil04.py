# SPDX-License-Identifier: MPL-2.0
"""NAV-01 bis NAV-04 und DESIGN-01/02 auf der echten Tk-Oberfläche."""
import argparse
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import time
from types import SimpleNamespace

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
        page = app.new_list_object("Projektseite", [], list_kind="page")
        note = app.new_list_object("Planungsnotiz", [], list_kind="note")
        app.lists.extend((page, note))
        assert app.save_items()
        app.set_home_view()
        settle()
        plus = app.add_pages_button
        assert plus.winfo_width() == plus.winfo_height() == 28
        home = (app.overview_search_border.winfo_rooty(), app.overview_search_border.winfo_height(),
                app.overview_search_entry.winfo_rooty(), app.overview_search_entry.winfo_x())
        app.set_plan_day_view()
        settle()
        today = (app.search_border.winfo_rooty(), app.search_border.winfo_height(),
                 app.search_entry.winfo_rooty(), app.search_entry.winfo_x())
        assert today == home, (today, home)
        opened = []
        build_menu = app.build_sidebar_section_menu

        def build_observed_menu(key):
            menu = build_menu(key)
            def record(x, y):
                opened.append((key, x, y, menu.index("end")))
            menu.tk_popup = record
            return menu

        app.build_sidebar_section_menu = build_observed_menu
        heading = app.pages_title
        prior_selection = app.pages_listbox.selection()
        heading.event_generate("<Button-3>", x=8, y=6)
        heading.focus_force()
        heading.event_generate("<Shift-F10>")
        settle()
        assert [entry[0] for entry in opened] == ["pages", "pages"], opened
        assert all(entry[3] >= 6 for entry in opened)
        assert app.pages_listbox.selection() == prior_selection
        app.build_sidebar_section_menu = build_menu
        assert app.change_sidebar_preference("sidebar_open_targets", {"pages": "side"})
        settle()
        iid = "list:" + page["id"]
        assert app.pages_listbox.exists(iid), app.sidebar_iid_to_row
        app.pages_listbox.focus_force()
        app.pages_listbox.focus(iid)
        app.pages_listbox.selection_set(iid)
        app.pages_listbox.event_generate("<<TreeviewSelect>>")
        settle()
        assert app.side_view_entry() is not None, (app.settings.get("sidebar_open_targets"),
            app.view_mode, app.pages_listbox.selection(), app._updating_sidebar,
            getattr(app, "_sidebar_context_selection", None), getattr(app, "_sidebar_board_drag", None))
        assert app.side_view_entry()["id"] == page["id"]
        assert app.view_mode == app.PLAN_DAY_VIEW
        app.close_side_view()
        assert app.change_sidebar_preference("sidebar_section_order", ["notes", "lists", "drawings", "pages"])
        settle()
        assert app.notes_title_row.winfo_y() < app.sidebar_title_row.winfo_y() < app.pages_title_row.winfo_y()
        app.show_info = lambda *_args, **_options: None
        app.hide_sidebar_section("lists")
        settle()
        assert not app.sidebar_title_row.winfo_ismapped()
        assert not app.sidebar_listbox.winfo_ismapped()
        app.change_sidebar_preference("sidebar_sections_visible", {})
        settle()
        assert app.sidebar_title_row.winfo_ismapped()
        app.ask_yes_no = lambda *_args: False
        assert not app.move_sidebar_roots("notes", "lists")
        assert app.sidebar_section_for("list", note["id"]) == "notes"
        app.ask_yes_no = lambda *_args: True
        save_settings = app.save_settings
        undo_depth = len(app.undo_stack)
        app.save_settings = lambda **_kwargs: False
        assert not app.move_sidebar_roots("notes", "lists")
        app.save_settings = save_settings
        assert len(app.undo_stack) == undo_depth
        assert app.sidebar_section_for("list", note["id"]) == "notes"
        assert app.move_sidebar_roots("notes", "lists")
        settle()
        assert app.sidebar_listbox.exists("list:" + note["id"])
        assert not app.notes_listbox.exists("list:" + note["id"])
        assert app.sidebar_policy().entries[note["id"]]["list_kind"] == "note"
        app.undo_last_change()
        settle()
        assert app.notes_listbox.exists("list:" + note["id"])
        app.redo_last_change()
        settle()
        assert app.sidebar_listbox.exists("list:" + note["id"])
        assert app.load_settings()["sidebar_open_targets"]["pages"] == "side"
        assert app.load_settings()["sidebar_locations"]["list:" + note["id"]] == "lists"
        app.show_info = lambda title, info: inventory.append((title, info))
        inventory = []
        app.show_sidebar_section_inventory("lists")
        assert inventory and str(len(app.sidebar_section_roots("lists"))) in inventory[0][1]
        first = app.new_folder_object("Erster Ordner")
        second = app.new_folder_object("Zweiter Ordner")
        app.folders.extend((first, second))
        assert app.save_items()
        settle()
        tree = app.sidebar_listbox
        first_iid, second_iid = ("folder:" + folder["id"] for folder in (first, second))

        def point(iid, fraction):
            x, y, _width, height = tree.bbox(iid)
            x += 20
            y += int(height*fraction)
            return SimpleNamespace(widget=tree, x=x, y=y, state=0,
                x_root=tree.winfo_rootx()+x, y_root=tree.winfo_rooty()+y)

        app.on_sidebar_drag_start(point(first_iid, .5))
        for fraction, zone in ((.1, "before"), (.5, "into"), (.9, "after")):
            pointer = point(second_iid, fraction)
            app.on_sidebar_drag_motion(pointer)
            settle()
            assert app.sidebar_drop_placement(("folder", first["id"]), tree, second_iid,
                ("folder", second["id"]), pointer) == zone
            assert app._sidebar_drag_indicator.winfo_ismapped()
            assert app.get_folder(first["id"]).get("parent_id") is None
        app.cancel_sidebar_drag()
        assert app._sidebar_drag_indicator is None
        app.on_sidebar_drag_start(point(first_iid, .5))
        app.on_sidebar_drag_motion(point(second_iid, .5))
        app.on_sidebar_drag_end(point(second_iid, .5))
        settle()
        assert app.get_folder(first["id"])["parent_id"] == second["id"]
        pointer = point(first_iid, .5)
        assert app.sidebar_drop_placement(("folder", second["id"]), tree, first_iid,
            ("folder", first["id"]), pointer) is None
        app.undo_last_change()
        settle()
        assert app.get_folder(first["id"]).get("parent_id") is None

        print(f"Sidebar and search geometry verified: {home}")
    finally:
        app.on_close()
