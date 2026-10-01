"""Seitenleisten-Ziehen und Layoutoptimierung mit echten Tk-Bindungen.

Prüft Inhalte, IDs, Datumsfelder, Rückgängig und Neustart. Keine echten Daten.
Absolute Laufzeiten stehen separat in messung_performance.py, nicht in Assertions.
"""
import copy
import importlib.machinery
import importlib.util
import os
import tempfile
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory(prefix="glide-drag-performance-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_drag_performance", str(REPO / "src/glide/app.pyw"))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    assert mod.app_font() == ("TkDefaultFont", 11), "ohne Tk keine implizite Fenstererzeugung"
    root = mod.tk.Tk()
    root.geometry("1450x1100+0+30")
    errors = []
    def callback_error(*exc):
        errors.append(str(exc[1]))
        traceback.print_exception(*exc)
    root.report_callback_exception = callback_error
    app = mod.ListApp(root)
    notices = []
    app.show_info = app.show_warning = app.show_error = lambda *a, **k: notices.append(a)
    click_time = 10000

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    def drag(source, target, zone="into"):
        global click_time
        click_time += 1000
        tree = app.get_sidebar_tree_for_iid(source)
        tree.see(source)
        idle()
        bx, by, _bw, bh = tree.bbox(source)
        x, y = bx + 40, by + bh // 2
        tree.event_generate("<ButtonPress-1>", x=x, y=y, time=click_time)
        idle()
        destination = app.get_sidebar_tree_for_iid(target)
        destination.see(target)
        idle()
        tx, ty, _tw, th = destination.bbox(target)
        offset = {"before": 1, "into": th // 2, "after": th - 1}[zone]
        rx, ry = destination.winfo_rootx() + tx + 50, destination.winfo_rooty() + ty + offset
        dx, dy = rx - tree.winfo_rootx(), ry - tree.winfo_rooty()
        tree.event_generate("<B1-Motion>", x=dx, y=dy, rootx=rx, rooty=ry,
                            state=0x100, time=click_time + 10)
        assert "drop_target" in destination.item(target, "tags"), "sichtbare Zielmarkierung"
        tree.event_generate("<ButtonRelease-1>", x=dx, y=dy, rootx=rx, rooty=ry,
                            time=click_time + 20)
        idle()
        assert not app.sidebar_drag_start_iid and not app.sidebar_drag_has_moved
        for sidebar in app.sidebar_trees():
            stack = list(sidebar.get_children(""))
            while stack:
                iid = stack.pop()
                stack.extend(sidebar.get_children(iid))
                assert "drop_target" not in sidebar.item(iid, "tags"), "Zielmarkierung entfernt"

    def entry(identifier):
        return next(e for e in app.lists if e["id"] == identifier)

    def parent(identifier):
        return app.get_folder(identifier).get("parent_id")

    def content(e):
        return {key: copy.deepcopy(e[key]) for key in ("id", "title", "list_kind", "items", "rich_note", "attachments")}

    try:
        idle()
        # Schriftwechsel invalidieren den Cache; unabhängige Tk-Interpreter
        # dürfen keine Schriftwerte voneinander übernehmen.
        old_size = app.settings["ui_font_size"]
        first = mod.app_font(10, "bold")
        for size in ("klein", "gross", "mittel"):
            if size not in app.UI_FONT_SIZE_CHOICES:
                continue
            app.settings["ui_font_size"] = size
            app.apply_ui_font()
            actual = mod.tkfont.nametofont("TkDefaultFont", root=root).actual()
            expected = (actual["family"], 10 + max(-1, min(1, actual["size"] - 11)), "bold")
            assert mod.app_font(10, "bold") == expected
            assert mod.app_font(10, "bold", root=root) == expected
        app.settings["ui_font_size"] = old_size
        app.apply_ui_font()
        assert mod.app_font(10, "bold") == first
        second = mod.tk.Tk()
        second.withdraw()
        second_font = mod.tkfont.nametofont("TkDefaultFont", root=second)
        second_font.configure(size=12)
        assert mod.app_font(10, root=second)[1] == 11
        assert mod.app_font(10, "bold", root=root) == first
        second.destroy()
        print("OK Schrift: Stile, Größenwechsel und getrennte Tk-Interpreter")

        # Reales Layout: Umbruch, kompakte Auswahl, längere Beschriftung,
        # Fokus, neue/entfernte Knöpfe und Zerstören vor dem Leerlauf.
        window = mod.tk.Toplevel(root)
        window.geometry("640x400")
        flow = mod.ButtonFlow(window, bg=app.theme["card"])
        flow.pack(fill="x")
        called = []
        controls = [flow.add(mod.tk.Button(flow, text=f"Aktion {i}", width=12,
                          command=lambda i=i: called.append(i)), key=str(i)) for i in range(9)]
        idle()
        assert all(b.winfo_ismapped() for b in controls)
        wide_rows = len({b.grid_info()["in"] for b in controls})
        focused = controls[3]
        focused.focus_set()
        before_focus = window.focus_get()
        flow.reflow()
        flow.reflow()
        assert window.focus_get() is before_focus
        window.geometry("280x400")
        idle()
        assert len({b.grid_info()["in"] for b in controls}) > wide_rows, "schmale Leiste bricht um"
        for frame in flow._rows:
            mapped = [b for b in controls if b.winfo_ismapped() and b.grid_info().get("in") is frame]
            assert all(b.winfo_x() + b.winfo_width() <= flow.winfo_width() for b in mapped)
        flow.compact_keys, flow.compact_below = {"0", "3"}, 500
        flow.reflow()
        idle()
        assert [i for i, b in enumerate(controls) if b.winfo_ismapped()] == [0, 3]
        flow.compact_keys = None
        controls[0].configure(text="Längere Aktion", width=19)
        flow.reflow()
        idle()
        assert all(b.winfo_ismapped() for b in controls)
        controls[2].destroy()
        flow.reflow()
        controls[3].invoke()
        assert called == [3]
        flow.entries = []
        flow.reflow()
        idle()
        assert not any(frame.winfo_ismapped() for frame in flow._rows)
        pending = mod.ButtonFlow(window, bg=app.theme["card"])
        pending.add(mod.tk.Button(pending, text="Kurzlebig"))
        pending.destroy()
        idle()
        window.destroy()
        print("OK Formatleisten: Umbruch, kompakte Auswahl, Beschriftung, Fokus und Lebenszyklus")

        # Ein synchroner Layoutleser darf nicht die noch leere, gebündelte
        # Leiste messen. Werkzeugwechsel müssen die Zeichenfläche ruhig halten.
        drawing = app.new_list_object("Zeichenleistenprobe", [], list_kind="drawing")
        app.lists.append(drawing)
        app.set_active_list(drawing["id"])
        idle()
        editor = app.current_drawing_editor()
        assert editor is not None
        for width in (1450, 860, 1200):
            root.geometry(f"{width}x1100+0+30")
            editor.set_tool("brush")
            idle()
            editor.reserve_context_rows()
            idle()
            height = editor.canvas.winfo_height()
            for tool in ("select", "line", "fill", "rect", "ellipse", "brush"):
                editor.set_tool(tool)
                idle()
                assert editor.canvas.winfo_height() == height, (width, tool, height, editor.canvas.winfo_height())
        root.geometry("1450x1100+0+30")
        app.set_home_view()
        idle()
        print("OK Zeichenleiste: reservierte Höhe bleibt bei Werkzeug- und Breitenwechsel stabil")

        library = app.new_folder_object("Bibliothek", folder_kind="library")
        library2 = app.new_folder_object("Zweite Bibliothek", folder_kind="library")
        journal = app.new_folder_object("Notizbuch", folder_kind="journal")
        journal2 = app.new_folder_object("Zweites Notizbuch", folder_kind="journal")
        normal = app.new_folder_object("Arbeitsordner")
        app.folders.extend([library, library2, journal, journal2, normal])
        point = app.new_item("Einzelne Aufgabe", due="2026-10-05", planned_date="2026-10-02")
        page = app.new_list_object("Seite", [point], list_kind="page",
            rich_note={"text": "Seiteninhalt\nEinzelne Aufgabe", "spans": [
                {"tag": "item:" + point["id"], "start": 13, "end": 29},
                {"tag": "task", "start": 13, "end": 29}], "links": {}})
        page2 = app.new_list_object("Zweite Seite", [], list_kind="page")
        note = app.new_list_object("Notiz", [], list_kind="note",
            rich_note={"text": "Notizinhalt", "spans": [], "links": {}}, created_at="2026-09-30T08:00:00")
        note2 = app.new_list_object("Zweite Notiz", [], list_kind="note")
        tasks = app.new_list_object("Aufgaben", [app.new_item("Bleibt erhalten")])
        app.lists.extend([page, page2, note, note2, tasks])
        app.set_home_view()
        app.update_sidebar_list()
        idle()
        originals = {e["id"]: content(e) for e in (page, note, tasks)}

        # Umordnen und Verschieben in jedem vorhandenen Bereich.
        for source, target in ((page, page2), (note, note2)):
            drag(f"list:{source['id']}", f"list:{target['id']}", "after")
            assert app.lists.index(entry(source["id"])) > app.lists.index(entry(target["id"]))
            assert content(entry(source["id"])) == originals[source["id"]], (source["title"], content(entry(source["id"])), originals[source["id"]])
        for source, target in ((page, library), (note, journal), (tasks, normal)):
            undo_before = len(app.undo_stack)
            drag(f"list:{source['id']}", f"folder:{target['id']}")
            assert entry(source["id"])["folder_id"] == target["id"]
            assert len(app.undo_stack) == undo_before + 1
            assert content(entry(source["id"])) == originals[source["id"]]
            app.undo_last_change()
            idle()
            assert entry(source["id"])["folder_id"] is None
            drag(f"list:{source['id']}", f"folder:{target['id']}")
        assert entry(note["id"])["journal"]["moment_date"] == "2026-09-30"
        print("OK Seiten/Notizen/Listen: native Drag-Bindungen, Reihenfolge, Ordner, Undo, Datum und Inhalte")

        # Quellkoordinaten dürfen im anderen Bereich nicht als Zielkoordinaten
        # interpretiert werden. Typ und Termine bleiben beim Ordnerwechsel.
        drag(f"list:{page['id']}", f"folder:{normal['id']}")
        assert entry(page["id"])["folder_id"] == normal["id"]
        drag(f"list:{page['id']}", f"folder:{library['id']}")
        assert content(entry(page["id"])) == originals[page["id"]]
        undo_before = len(app.undo_stack)
        drag(f"list:{page['id']}", f"list:{note2['id']}", "after")
        assert entry(page["id"])["folder_id"] == library["id"]
        assert len(app.undo_stack) == undo_before, "kein Umwandeln durch Ziehen in einen anderen Typbereich"
        drag(f"list:{page['id']}", f"list:{page2['id']}", "after")
        assert entry(page["id"])["folder_id"] is None, "aus dem Ordner wieder zur Hauptebene"
        drag(f"list:{page['id']}", f"folder:{library['id']}")
        for source, target in ((library, library2), (journal, journal2)):
            drag(f"folder:{source['id']}", f"folder:{target['id']}", "before")
            assert app.folders.index(app.get_folder(source["id"])) < app.folders.index(app.get_folder(target["id"]))
            drag(f"folder:{source['id']}", f"folder:{target['id']}", "into")
            assert parent(source["id"]) == target["id"]
            undo_before = len(app.undo_stack)
            drag(f"folder:{target['id']}", f"folder:{source['id']}", "into")
            assert parent(target["id"]) is None and len(app.undo_stack) == undo_before
            assert notices, "unzulässige Verschachtelung wird gemeldet"
            app.undo_last_change()
            idle()
            assert parent(source["id"]) is None
        print("OK Bereiche übergreifend: Koordinaten, Bibliothek/Notizbuch, Zyklenabwehr und Rückgängig")

        # Klick ohne Zug ist kein Umbau; Klapppfeile bleiben nativ bedienbar.
        tree = app.pages_listbox
        iid = f"folder:{library['id']}"
        tree.see(iid)
        idle()
        bx, by, bw, bh = tree.bbox(iid)
        y = by + bh // 2
        arrow_x = next(x for x in range(bx, bx + min(bw, 100))
                       if "indicator" in str(tree.identify_element(x, y)))
        before = bool(tree.item(iid, "open"))
        undo_before = len(app.undo_stack)
        click_time += 1000
        tree.event_generate("<ButtonPress-1>", x=arrow_x, y=y, time=click_time)
        tree.event_generate("<ButtonRelease-1>", x=arrow_x, y=y, time=click_time + 1)
        idle()
        assert bool(tree.item(iid, "open")) != before
        assert len(app.undo_stack) == undo_before
        app.save_items()
        stored = copy.deepcopy(app.lists)
        app.load_items()
        assert app.lists == stored, "Speichern/Laden erhält Reihenfolge, Aufgaben und Arten"
        assert not errors, errors
        print("OK Klapppfeil ohne Umbau, Speichern/Laden und keine Tk-Callbackfehler")
    finally:
        root.destroy()
