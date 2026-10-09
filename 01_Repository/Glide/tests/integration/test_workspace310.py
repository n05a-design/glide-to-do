"""Reiter/Pinnwand: Objektidentität, Persistenz, Mutationen und reale Tk-Ereignisse."""
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory(prefix="glide-workspace310-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_workspace310", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    errors = []
    warnings = []

    def start():
        root = mod.tk.Tk()
        root.withdraw()
        root.report_callback_exception = lambda *error: errors.append(error)
        app = mod.ListApp(root)
        app.show_warning = lambda *a, **kw: warnings.append(a)
        app.show_error = lambda *a, **kw: warnings.append(a)
        app.show_info = lambda *a, **kw: warnings.append(a)
        root.geometry("1280x860+10+10")
        root.deiconify(); root.update()
        return root, app

    def stop(app):
        app.cancel_pending_callbacks()
        app.release_data_lock()
        app.root.destroy()

    def backup_content(app):
        payload = copy.deepcopy(app.complete_backup_payload())
        payload.pop("exported_at", None)
        # Punkt 8 (3.24.0): Seit 3.24 trägt ein Komplettbackup auch die
        # Pinnwandanordnung. Diese Prüfung fragt nach den Aufgabendaten –
        # dass Anheften und Verschieben sie nicht anfassen –, deshalb bleibt
        # der Anordnungsabschnitt hier außen vor. Seine eigene Prüfung steht
        # in test_features324.py.
        payload.pop("pinboards", None)
        return payload

    root, app = start()
    try:
        app.settings["startup_view"] = "last"
        source = app.current_list()
        label = {"id": "workspace-label", "name": "Besprechung", "color": "label_blue"}
        app.labels.append(label)
        items = [app.new_item(f"Punkt {index}: " + "Langer Titel " * 12,
                             description="Vollständige Beschreibung\nmit eigener zweiter Zeile", labels=[label["id"]]) for index in range(14)]
        repeat_date = (mod.date.today() + mod.timedelta(days=2)).isoformat()
        repeat = app.new_item("Täglich prüfen", due=repeat_date, due_time="10:00",
                             repeat={"art": app.REPEAT_DAILY}, reminder={"mode": "relative", "minutes": 60})
        child = app.new_item("Unterpunkt", description="Kindbeschreibung")
        group = app.new_item("Projektgruppe", kind=app.ITEM_KIND_GROUP, children=[child])
        heading = app.new_item("Nur Überschrift", kind=app.ITEM_KIND_HEADING)
        app.items.extend(items + [repeat, group, heading])
        app.save_items(); app.refresh_tree(); root.update()
        baseline = backup_content(app)
        original_order = list(app.content_frame.pack_slaves())
        karte_vorher = (app.list_frame_outer.winfo_rooty(), app.list_frame_outer.winfo_height())
        assert not app.workspace.bar.winfo_ismapped()

        # Schließen ist ausschließlich ein Ansichtswechsel; vollständiges Aufgabenbackup identisch.
        w = app.workspace
        w.open_tab(items[0]["id"]); root.update()
        assert w.detail_title.cget("text") == items[0]["text"]
        assert app.get_selected_item_id() == items[0]["id"]
        w.close_tab(); root.update()
        assert backup_content(app) == baseline
        # Seit dem festen Layout (27.09.2026) steht bei markiertem Punkt die
        # Auswahlleiste an der Stelle des Hinweises; die Fläche bleibt gleich.
        root.update_idletasks(); root.update()
        assert (app.list_frame_outer.winfo_rooty(), app.list_frame_outer.winfo_height()) == karte_vorher
        app.tree.selection_set(()); root.update_idletasks(); root.update()
        assert app.content_frame.pack_slaves() == original_order, ([str(w) for w in app.content_frame.pack_slaves()], [str(w) for w in original_order])
        assert not w.bar.winfo_ismapped()
        w.open_tab(heading["id"])
        assert not app.settings["open_tabs"]

        # LRU global über alle Listen; mehrfaches Öffnen erzeugt keine Dublette.
        for item in items[:12]:
            w.open_tab(item["id"])
        w.open_tab(items[0]["id"])
        w.open_tab(items[12]["id"]); root.update()
        tabs = app.settings["open_tabs"]
        assert len(tabs) == 12
        assert items[0]["id"] in [tab["item_id"] for tab in tabs]
        assert items[1]["id"] not in [tab["item_id"] for tab in tabs]
        assert "maximal 12" in w.notice.cget("text")
        assert backup_content(app) == baseline
        order = [item["id"] for item in app.items]
        w.reorder_tab(-1); root.update()
        assert [item["id"] for item in app.items] == order
        assert len(app.settings["open_tabs"]) == 12

        # Reiter bleibt nach Erledigung offen; Undo aktualisiert dieselbe Ansicht.
        w.open_tab(items[0]["id"]); root.update()
        w.toggle(); root.update()
        assert app.find_item_in_lists(items[0]["id"])[0]["done"] is True
        assert w.mode == items[0]["id"]
        app.undo_last_change(); root.update()
        assert app.find_item_in_lists(items[0]["id"])[0]["done"] is False
        items = [app.find_item_in_lists(item["id"])[0] for item in items]
        repeat = app.find_item_in_lists(repeat["id"])[0]
        group = app.find_item_in_lists(group["id"])[0]
        w.open_tab(group["id"]); root.update()
        w.toggle(child["id"]); root.update()
        assert app.find_item_in_lists(child["id"])[0]["done"]
        assert not group["done"]
        w.open_tab(repeat["id"]); root.update()
        w.toggle(); root.update()
        assert repeat["due"] == (mod.date.fromisoformat(repeat_date) + mod.timedelta(days=1)).isoformat() and not repeat["done"]
        assert w.mode == repeat["id"]

        # Editieren verwendet den gemeinsamen Details-Dialog und bewahrt die Identität.
        target = items[0]
        original_details = app.themed_item_details_dialog
        seen = []
        with patch.object(app, "themed_item_details_dialog", side_effect=lambda item: seen.append(item) or None):
            w.edit(target["id"])
        assert seen[0] is target
        with app.item_change([target["id"]], restore=False) as change:
            target["text"] = "Geänderter Punkt"
            change.mark()
        w.open_tab(target["id"]); root.update()
        assert w.detail_title.cget("text") == "Geänderter Punkt"

        # Leeren, Positionen und Filter verändern keine Aufgabendaten oder Reihenfolge.
        before_board = backup_content(app)
        w.pin([target["id"], repeat["id"], group["id"]]); root.update()
        assert w.mode == "board" and len(w.card_ids) == 3
        assert backup_content(app) == before_board
        w.set_label_filter(label["id"]); root.update()
        assert w.card_ids == [target["id"]]
        w.set_label_filter("")
        app.search_var.set("Täglich"); root.update()
        assert w.card_ids == [repeat["id"]]
        app.search_var.set(""); root.update()
        def descendants(widget):
            for child in widget.winfo_children():
                yield child
                yield from descendants(child)
        # Seit 3.33.21 (U09) steht „Anordnung“ in der Schalterzeile über der Fläche.
        field = next(widget for widget in list(descendants(w.bar)) + list(descendants(w.body))
                     if isinstance(widget, mod.AppOptionMenu) and "Frei anordnen" in widget.options)
        field._open_popup(); root.update()
        field._choices.event_generate("<End>")
        field._choices.event_generate("<Return>"); root.update()
        assert w.board()["layout"] == "free"
        assert not getattr(app, "_active_dropdown", None)
        assert root.grab_current() is None
        assert not errors, errors
        w.focus_card(target["id"]); root.update()
        old_card = copy.deepcopy(next(card for card in w.board()["cards"] if card["item_id"] == target["id"]))
        w.canvas.event_generate("<Alt-Right>"); root.update()
        new_card = copy.deepcopy(next(card for card in w.board()["cards"] if card["item_id"] == target["id"]))
        assert new_card["x"] > old_card["x"] and new_card["x"] % 24 == 0
        x, y, width, height = w.card_boxes[target["id"]]
        px, py = int(x-w.canvas.canvasx(0)+20), int(y-w.canvas.canvasy(0)+20)
        w.canvas.event_generate("<ButtonPress-1>", x=px, y=py)
        w.canvas.event_generate("<B1-Motion>", x=px+80, y=py+50)
        w.canvas.event_generate("<ButtonRelease-1>", x=px+80, y=py+50); root.update()
        assert next(card for card in w.board()["cards"] if card["item_id"] == target["id"])["x"] > new_card["x"]
        assert backup_content(app) == before_board
        w.store_position(target["id"], 16000, 12000); root.update()
        assert w.canvas.xview()[0] > 0 and w.canvas.yview()[0] > 0
        w.find_cards(); root.update()
        # Seit 3.22 räumt „Alle Karten finden" auf, ohne die Betriebsart zu
        # wechseln: Die freie Anordnung bleibt, die Karten kommen zurück.
        assert w.board()["layout"] == "free" and len(w.card_ids) == 3
        assert w.card_boxes[target["id"]][0] < 1000
        assert all(card["x"] < 3000 and card["y"] < 8000 for card in w.board()["cards"])
        w.focus_card(target["id"])
        # Nach einem Fensterwechsel übernimmt Tk den Fokus asynchron. Erst
        # nach dessen Zustellung prüft Entf die tatsächliche Pinnwandbindung.
        root.update()
        assert root.focus_get() == w.canvas, "Pinnwand muss vor Entf den Tastaturfokus besitzen"
        w.canvas.event_generate("<Delete>"); root.update()
        assert target["id"] not in w.card_ids
        assert app.find_item_in_lists(target["id"])
        assert backup_content(app) == before_board

        # Kleine/große Fenster, beide Themes, Seitenleiste und Rückkehr zur normalen Liste.
        for theme in ("light", "dark"):
            app.set_design(theme, apply_now=False); app.apply_theme()
            for size in ("860x700", "1440x1000"):
                root.geometry(size); root.update()
                assert w.canvas.winfo_height() >= 100, (size, w.canvas.winfo_height())
                assert w.canvas.winfo_width() >= 350
                assert w.canvas.cget("bg") == app.theme["bg"]
                w.open_tab(target["id"]); root.update()
                assert w.detail_title.winfo_width() <= app.list_frame_outer.winfo_width()
                w.set_mode("board"); root.update()
                old_width = w.canvas.winfo_width()
                app.toggle_sidebar(); root.update()
                assert w.canvas.winfo_width() > old_width
                app.toggle_sidebar(); root.update()
            app.set_home_view(); root.update()
            app.set_template_view(); root.update()
            app.set_active_list(source["id"]); root.update()
            assert w.mode == "board"
            w.set_mode("list"); root.update()
            # Markierte Punkte zeigen seit dem 27.09.2026 die Auswahlleiste statt
            # des Hinweises; ohne Auswahl gilt wieder die ursprüngliche Ordnung.
            app.tree.selection_set(()); root.update_idletasks(); root.update()
            assert app.content_frame.pack_slaves() == original_order, ([str(w) for w in app.content_frame.pack_slaves()], [str(w) for w in original_order])
            w.set_mode("board"); root.update()

        # Der echte Anheften-Dialog akzeptiert Mehrfachauswahl und schließt regulär.
        def choose_modal(dialog, parent=None):
            dialog.update()
            choices = next(widget for widget in descendants(dialog) if isinstance(widget, mod.ttk.Treeview))
            choices.selection_set(items[2]["id"], items[3]["id"])
            choices.focus_force()
            choices.event_generate("<Return>")
            root.update()
        with patch.object(app, "run_modal", side_effect=choose_modal):
            w.choose_cards()
        assert items[2]["id"] in w.card_ids and items[3]["id"] in w.card_ids

        # Gespeicherte Referenzen überleben Neustart; gelöschte Referenzen und Kopien erben nichts.
        w.open_tab(target["id"]); root.update()
        expected_tabs = copy.deepcopy(app.settings["open_tabs"])
        expected_boards = copy.deepcopy(app.settings["pinboards"])
        app.save_settings()
        stop(app)
        root, app = start(); w = app.workspace
        assert app.settings["open_tabs"] == expected_tabs
        assert app.settings["pinboards"] == expected_boards
        assert w.mode == target["id"]
        assert w.detail_title.cget("text") == "Geänderter Punkt"
        app.delete_item(); root.update()
        assert not app.find_item_in_lists(target["id"])
        assert target["id"] not in [tab["item_id"] for tab in app.settings["open_tabs"]]
        app.undo_last_change(); root.update()
        assert app.find_item_in_lists(target["id"])
        assert target["id"] not in [tab["item_id"] for tab in app.settings["open_tabs"]]

        # Pinnwand eines Ordners enthält echte Punkte aus seinen Unterlisten.
        folder = app.new_folder_object("Sammlung")
        app.folders.append(folder)
        nested = app.new_folder_object("Unterordner", parent_id=folder["id"])
        app.folders.append(nested)
        other = app.new_list_object("Zweite Liste", folder_id=nested["id"])
        foreign = app.new_item("Fremde Aufgabe", due="2026-10-03")
        other["items"].append(foreign); app.lists.append(other)
        app.save_items(); app.set_active_folder(folder["id"]); root.update()
        assert foreign["id"] in w.valid_items()
        w.pin([foreign["id"]]); root.update()
        w.toggle(); root.update()
        assert foreign["done"] is True
        w.open_tab(foreign["id"]); root.update()
        assert app.active_list_id == other["id"] and w.mode == foreign["id"]
        w.open_source(); root.update()
        assert w.mode == "list" and app.tree.selection() == (foreign["id"],)

        # Schreibfehler lassen vorhandene Ansichtseinstellungen und Dateien bestehen.
        previous = copy.deepcopy(app.settings)
        with patch.object(app, "save_settings", return_value=False):
            w.open_tab(foreign["id"])
        assert app.settings == previous
        dirty = app.normalize_personal_settings({"open_tabs": [None, {"item_id": "bad"}],
                      "active_tab": ["bad"], "pinboards": {"bad": {}, "list:x": {"cards": [None], "width": float('nan')}}})
        assert dirty["open_tabs"] == [] and dirty["active_tab"] == {}
        assert dirty["pinboards"]["list:x"]["width"] == 300
        assert not errors, errors
        print("OK: Reiter, Pinnwand, Objektidentität, Wiederholung, Persistenz, Papierkorb, Tastatur und Geometrie")
    finally:
        stop(app)
