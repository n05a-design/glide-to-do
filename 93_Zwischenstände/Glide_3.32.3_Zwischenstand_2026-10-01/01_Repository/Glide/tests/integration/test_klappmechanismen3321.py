"""Klappkontrolle: echte Pfeilklicks, native Tastaturwege und Neuaufbau.

Jede Familie erhält eine Bedienprobe; keine echten Nutzerdaten werden geladen.
"""
import copy
import importlib.machinery
import importlib.util
import json
import os
import re
import tempfile
import traceback
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory(prefix="glide-klappkontrolle-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_klapp", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1450x950+0+30")
    errors = []
    def callback_error(*args):
        errors.append(args)
        traceback.print_exception(*args)
    root.report_callback_exception = callback_error
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *a, **k: None
    click_time = 10000

    def click(widget, x, y):
        global click_time
        # Zwei eigenständige Bedienproben sind kein versehentlicher Doppelklick.
        click_time += 1000
        widget.event_generate("<ButtonPress-1>", x=x, y=y, time=click_time)
        if widget.winfo_exists():
            widget.event_generate("<ButtonRelease-1>", x=x, y=y, time=click_time + 1)

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    def arrow(tree, iid):
        tree.see(iid)
        idle()
        box = tree.bbox(iid, "#0")
        assert box, ("Pfeilzeile nicht sichtbar", iid)
        left, top, width, height = box
        y = top + height // 2
        x = next((x for x in range(left, left + min(width, 150))
                  if "indicator" in str(tree.identify_element(x, y)).lower()), None)
        assert x is not None, ("Kein nativer Klapppfeil", iid, box)
        click(tree, x, y)
        idle()

    def key(tree, iid, direction):
        tree.focus(iid)
        tree.selection_set(iid)
        # Native Tcl-Class-Bindung: im Hintergrund ist kein OS-Tastaturfokus nötig.
        tree.tk.call("ttk::treeview::Keynav", tree, direction)
        idle()

    def bound_key(widget, sequence):
        """Tatsächlich registrierte Widget-Bindung ohne OS-Fokus ausführen."""
        script = widget.bind(sequence)
        assert script, ("Fehlende Tastaturbindung", widget, sequence)
        values = dict(zip("#bfh kst wxy AEK NWT XYD".replace(" ", ""),
                          (1, 0, 0, 0, 0, 0, click_time, 0, 0, 0, "", 0, "Return", 13,
                           str(widget), 2, 0, 0, 0)))
        script = re.sub(r"%([#a-zA-Z])", lambda match: "{" + str(values[match[1]]) + "}", script)
        result = widget.tk.call("catch", script)
        assert int(result) in (0, 3), ("Tastaturbindung fehlgeschlagen", sequence, result)
        idle()

    try:
        idle()
        label = {"id": "fold-label", "name": "Kunde", "color": "accent"}
        app.labels.append(label)
        group = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP)
        child = app.new_item("Kind", labels=[label["id"]])
        group["children"] = [child]
        old = (date.today() - timedelta(days=2)).isoformat()
        entry = app.new_list_object("Klappprüfung", [group,
            app.new_item("Fälliger Punkt", due=old), app.new_item("Zweiter fälliger Punkt", due=old),
            app.new_item("Ohne Label"),
            app.new_item("Heute ohne Uhrzeit", planned_date=date.today().isoformat()),
            app.new_item("Heute um neun", planned_date=date.today().isoformat(), planned_time="09:00")])
        app.lists.append(entry)
        app.set_active_list(entry["id"])
        app.save_items()
        before = copy.deepcopy(app.data_payload())

        app.set_labels_view()
        idle()
        label_row = app.LABEL_GROUP_ROW_PREFIX + label["id"]
        arrow(app.tree, label_row)
        assert not app.tree.item(label_row, "open"), "Labels: Pfeilklick muss schließen"
        app.refresh_tree()
        idle()
        assert not app.tree.item(label_row, "open"), "Labels: Neuaufbau darf nicht aufklappen"
        key(app.tree, label_row, "right")
        app.refresh_tree()
        idle()
        assert app.tree.item(label_row, "open"), "Labels: Rechts öffnet dauerhaft"
        assert app.data_payload() == before, "Klappen verändert keine Aufgaben"

        # Labels, einschließlich „Ohne Label“: ausgewähltes Kind darf einen
        # geschlossenen Vorfahren beim Neuaufbau nicht wieder öffnen.
        for row in (label_row, app.LABEL_GROUP_ROW_PREFIX + app.UNLABELLED_GROUP_KEY):
            kid = app.tree.get_children(row)[0]
            app.tree.focus(kid)
            app.tree.selection_set(kid)
            arrow(app.tree, row)
            assert not app.tree.item(row, "open"), ("Label-Klick schließt", row)
            app.refresh_tree(selected_id=kid)
            idle()
            assert not app.tree.item(row, "open"), ("Auswahl öffnet Labelgruppe", row)
            app.set_home_view()
            app.set_labels_view()
            idle()
            assert not app.tree.item(row, "open"), ("Ansichtswechsel öffnet Labelgruppe", row)
            key(app.tree, row, "right")
        key(app.tree, label_row, "left")
        app.search_var.set("Kein Treffer")
        app.refresh_tree()
        idle()
        app.search_var.set("")
        app.refresh_tree()
        idle()
        assert not app.tree.item(label_row, "open"), "Filterwechsel behält Klappzustand"
        app.expand_all()
        app.refresh_tree()
        idle()
        assert all(app.tree.item(row, "open") for row in app.tree.get_children(""))
        app.collapse_all()
        app.refresh_tree()
        idle()
        assert all(not app.tree.item(row, "open") for row in app.tree.get_children(""))
        app.settings = app.load_settings()
        app.refresh_tree()
        idle()
        assert not app.tree.item(label_row, "open"), "Gespeicherte Labels bleiben geschlossen"
        normalized = app.normalize_personal_settings({"label_sections_closed": [label_row, label_row, 3, "falsch"]})
        assert normalized["label_sections_closed"] == [label_row]
        print("OK Labels: Pfeil, Links/Rechts, Auswahl, Filter, Wechsel, globale Aktionen, gespeicherte Einstellungen")

        # Übersicht „In Bearbeitung“ und Mein Tag: jedes tatsächlich gerenderte
        # Fach per Maus und nativer Links/Rechts-Class-Bindung bedienen.
        for setter in (app.set_in_progress_view, app.set_today_view):
            setter()
            idle()
            rows = [iid for iid in app.tree.get_children("") if iid in app.OVERVIEW_SECTION_ROW_IDS]
            assert rows, "Übersichtsprobe braucht gefüllte Abschnitte"
            for row in rows:
                assert app.tree.get_children(row), row
                key(app.tree, row, "right")
                arrow(app.tree, row)
                assert not app.tree.item(row, "open"), row
                app.refresh_tree()
                idle()
                assert not app.tree.item(row, "open"), ("Übersicht zu", row)
                key(app.tree, row, "right")
                app.refresh_tree()
                idle()
                assert app.tree.item(row, "open"), ("Übersicht offen", row)
            app.collapse_all()
            app.refresh_tree()
            idle()
            assert all(not app.tree.item(row, "open") for row in rows)
            app.expand_all()
        print("OK Übersicht/Mein Tag: alle vorhandenen Abschnitte, native Öffnungsreihenfolge, globale Aktionen")

        # Echte Unterpunkte und Gruppen sowie generierte Gruppierungsfächer,
        # jeweils in Liste und Tabelle. Daten und Undo bleiben unberührt.
        app.set_active_list(entry["id"])
        app.workspace.set_mode("list")
        app.expand_all()
        idle()
        before = copy.deepcopy(entry["items"])
        undo_count = len(app.undo_stack)
        arrow(app.tree, group["id"])
        app.refresh_tree(selected_id=child["id"])
        idle()
        assert not app.tree.item(group["id"], "open"), "Ausgewähltes Kind öffnet geschlossene Gruppe"
        key(app.tree, group["id"], "right")
        app.set_list_group("importance")
        idle()
        row = app.group_section_iid("0")
        for table in (False, True):
            if table:
                app.set_table_view()
            idle()
            key(app.tree, row, "right")
            arrow(app.tree, row)
            app.refresh_tree(selected_id=child["id"])
            idle()
            assert not app.tree.item(row, "open"), ("Gruppierung zu", table)
            key(app.tree, row, "right")
            app.refresh_tree()
            idle()
            assert app.tree.item(row, "open"), ("Gruppierung offen", table)
            app.collapse_all()
            app.refresh_tree()
            idle()
            assert not app.tree.item(row, "open")
            app.expand_all()
        app.set_list_group(None)
        app.set_table_nested(True)
        idle()
        arrow(app.tree, group["id"])
        app.refresh_tree(selected_id=child["id"])
        idle()
        assert not app.tree.item(group["id"], "open"), "Verschachtelte Tabelle bleibt zu"
        key(app.tree, group["id"], "right")
        app.refresh_tree()
        idle()
        assert app.tree.item(group["id"], "open")
        assert entry["items"] == before, "Listenklappen verändert keine Aufgaben"
        assert len(app.undo_stack) == undo_count, "Klappen erzeugt keinen Aufgaben-Undo"
        app.set_table_nested(False)
        app.set_active_list(entry["id"])
        print("OK Liste/Tabelle: Unterpunkte, Gruppen, Gruppierungsfächer, Auswahl, globale Aktionen, Undo")

        # Alle drei Seitenleistenbäume einschließlich verschachtelter Ordner.
        for kind, list_kind in (("standard", "list"), ("library", "page"), ("journal", "note")):
            parent = app.new_folder_object("Klappordner " + kind, folder_kind=kind)
            nested = app.new_folder_object("Unterordner " + kind, parent_id=parent["id"], folder_kind=kind)
            nested_entry = app.new_list_object("Inhalt " + kind, [], folder_id=nested["id"], list_kind=list_kind)
            app.folders.extend([parent, nested])
            app.lists.append(nested_entry)
            app.save_items()
            app.update_sidebar_list()
            idle()
            tree = app.sidebar_tree_for_folder(parent)
            for holder in (nested, parent):
                row = "folder:" + holder["id"]
                arrow(tree, row)
                assert not tree.item(row, "open"), ("Ordner zu", kind)
                app.update_sidebar_list()
                idle()
                assert not tree.item(row, "open"), ("Ordner-Neuaufbau", kind)
                key(tree, row, "right")
                app.update_sidebar_list()
                idle()
                assert tree.item(row, "open"), ("Ordner offen", kind)
        for section, widget, tree in (("pages", app.pages_heading_icon, app.pages_listbox),
                                      ("lists", app.sidebar_heading_icon, app.sidebar_listbox),
                                      ("notes", app.notes_heading_icon, app.notes_listbox)):
            click(widget, 3, 3)
            idle()
            assert not app.sidebar_section_open(section) and not tree.winfo_manager(), section
            app.update_sidebar_list()
            idle()
            assert not tree.winfo_manager(), ("Seitenleistenbereich bleibt zu", section)
            click(widget, 3, 3)
            idle()
            assert app.sidebar_section_open(section) and tree.winfo_manager(), section
            assert str(widget.cget("takefocus")) == "1", ("Pfeil im Tab-Weg", section)
            bound_key(widget, "<Return>")
            assert not tree.winfo_manager(), ("Bereich per Tastatur schließen", section)
            bound_key(widget, "<space>")
            assert tree.winfo_manager(), ("Bereich per Tastatur öffnen", section)
        app.set_pinned("list", entry["id"])
        app.set_sidebar_section_open("pinned", True)
        app.render_pinned_sidebar()
        idle()
        for closed in (True, False):
            header = app.pinned_sidebar_header
            control = header.winfo_children()[0]
            if closed:
                click(control, 3, 3)
            else:
                bound_key(control, "<Return>")
            idle()
            assert app.sidebar_section_open("pinned") != closed
            app.update_sidebar_list()
            idle()
            assert app.sidebar_section_open("pinned") != closed
        app.set_sidebar_section_open("views", False)
        idle()
        assert app.views_collapsed_header.winfo_manager() and not app.system_listbox.winfo_manager()
        bound_key(app.views_collapsed_header, "<Return>")
        assert app.system_listbox.winfo_manager() and not app.views_collapsed_header.winfo_manager()
        print("OK Seitenleiste: Seiten/Listen/Notizen, verschachtelte Ordner und Bereichspfeile")

        # Pinnwand: echter Klick auf den Spaltenkopf, Breite und gespeicherter
        # Zustand; erneut Zeichnen darf keine Karten oder Zuordnungen ändern.
        app.set_active_list(entry["id"])
        ws = app.workspace
        ws.set_mode("board")
        ws.configure_board("layout", "columns")
        ws.configure_board("group_by", "importance")
        idle()
        column = ws.column_order[0]["key"]
        before = copy.deepcopy(entry["items"])
        for closed in (True, False):
            left, top, width, height = ws.column_boxes[column]
            click(ws.canvas, int(left + 10 - ws.canvas.canvasx(0)), int(top + 10 - ws.canvas.canvasy(0)))
            idle()
            assert (column in ws.board()["collapsed"]) == closed
            ws._signature = None
            ws.refresh()
            idle()
            assert (column in ws.board()["collapsed"]) == closed
        assert entry["items"] == before
        ws.set_mode("list")
        print("OK Pinnwand: Spaltenkopf-Klick, Schließen/Öffnen und Neuaufbau ohne Datenänderung")

        # Seiten und Notizen nutzen dieselben Aufklappblöcke. Die gespeicherten
        # Tags müssen verschachtelte Kinder verbergen und das Folgekapitel lassen.
        for kind in ("page", "note"):
            document = app.new_list_object("Aufklapptext " + kind, [], list_kind=kind)
            app.lists.append(document)
            app.set_active_list(document["id"])
            idle()
            ed = app.rich_note_editor
            text = ed.text
            text.delete("1.0", "end")
            text.insert("1.0", "Kopf\nKind\nEnkel\nDanach\n")
            text.mark_set("insert", "1.0")
            ed.set_block("toggle")
            text.tag_add("indent1", "2.0", "3.0")
            text.tag_add("indent2", "3.0", "4.0")
            ed.flush()
            idle()
            x, y, width, height = text.bbox("1.0")
            click(text, x + 1, y + height // 2)
            idle()
            assert "folded" in text.tag_names("2.0") and "folded" in text.tag_names("3.0"), kind
            assert "folded" not in text.tag_names("4.0"), kind
            saved = ed.document()
            ed.load(saved)
            idle()
            assert "folded" in text.tag_names("2.0"), ("Text-Neuaufbau", kind)
            x, y, width, height = text.bbox("1.0")
            click(text, x + 1, y + height // 2)
            idle()
            assert "folded" not in text.tag_names("2.0"), kind
            ed.flush()
        print("OK Seiten/Notizen: Pfeilklick, verschachtelte Kinder, Folgekapitel und Speichern/Laden")

        # Aufklappfelder sind transient: Schließen bewahrt die Auswahl.
        picker = mod.LabelDropdown(root, app, [label], selected_ids=[label["id"]])
        picker.pack(fill="x", side="bottom")
        idle()
        click(picker.summary_label, 4, 4)
        idle()
        assert picker._popup is not None
        bound_key(picker._popup, "<Return>")
        assert picker._popup is None and picker.read() == [label["id"]]
        picker.destroy()
        host = mod.tk.Frame(root)
        host.pack(side="bottom", fill="x")
        field = mod.tk.Frame(host)
        field.pack(fill="x")
        variable = mod.tk.StringVar(root, value="Erste Option")
        options = mod.AppOptionMenu(field, app, variable, ["Erste Option", "Zweite Option"])
        options.pack(fill="x")
        idle()
        click(options, 4, 4)
        idle()
        assert options._popup is not None
        click(options, 4, 4)
        idle()
        assert options._popup is None and variable.get() == "Erste Option"
        host.destroy()
        print("OK Auswahlfelder: Label- und Einfachauswahl öffnen/schließen, Auswahl bleibt erhalten")
        assert not errors, errors
        print("OK Klappkontrolle: alle geprüften Bedienwege ohne Tk-Callbackfehler")
    finally:
        root.destroy()
