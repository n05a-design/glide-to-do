"""Seitenleiste vom 29.09.2026: Einklappen, Bereich „Notizen“, Ordner in allen Bereichen.

- Ein Ordner mit der geöffneten Liste bleibt zu, wenn die Seitenleiste neu
  aufgebaut wird (Fehler „Listen lassen sich nicht zuklappen“). Aufgeklappt
  wird nur, wenn eine andere Zeile geöffnet wird.
- Eine zugeklappte Bibliothek im Seitenbereich bleibt nach dem Neuaufbau zu.
- „Notizen +“ steht unter den Listen: Notizen ohne Ordner und Notizbücher mit
  ihrem Inhalt; Notizen in gewöhnlichen Ordnern bleiben bei ihrem Ordner.
- Pfeil klappt, Titel öffnet die Notizübersicht, „+“ legt an.
- Bibliotheken und Notizbücher haben „+“ und „…“ beim Überfahren; ein
  Unterordner erbt die Ordnerart.
- Bei 860 × 700 behält der Listenbaum mindestens drei Zeilen mit allen vier Bereichsüberschriften, und die
  Überschrift „Notizen“ bleibt sichtbar.
"""
import importlib.machinery
import importlib.util
import json
import os
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True

with tempfile.TemporaryDirectory(prefix="glide-notizbereich-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        daten = json.loads(archiv.read("data.json"))
    Path(ordner, "liste_speicher.json").write_text(json.dumps(daten, ensure_ascii=False), encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader("glide_notizbereich", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    mod.ListApp.show_info = lambda self, *args, **kwargs: None
    root = mod.tk.Tk()
    root.geometry("1300x900+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    app.show_warning = app.show_error = lambda *args, **kwargs: fehler.append(args)

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    def eintraege(menu):
        return [menu.entrycget(index, "label") for index in range(menu.index("end") + 1)
                if menu.type(index) in ("command", "cascade")]

    def offen(baum, iid):
        return bool(baum.item(iid, "open"))

    try:
        time.sleep(0.5)
        ruhe()

        # --- Einklappen im Listenbaum -------------------------------------------
        baum = app.sidebar_listbox
        ordner_mit_liste = next(folder for folder in app.folders if not folder.get("parent_id")
                                and any(entry.get("folder_id") == folder["id"] for entry in app.lists))
        liste = next(entry for entry in app.lists if entry.get("folder_id") == ordner_mit_liste["id"])
        andere = next(entry for entry in app.lists if entry.get("folder_id") == ordner_mit_liste["id"]
                      and entry is not liste and not app.is_surface_list(entry))
        ordner_iid = f"folder:{ordner_mit_liste['id']}"
        app.set_active_list(liste["id"])
        ruhe()
        assert baum.selection() == (f"list:{liste['id']}",) and offen(baum, ordner_iid)
        baum.item(ordner_iid, open=False)
        app.update_sidebar_list()
        ruhe()
        assert not offen(baum, ordner_iid), "Neuaufbau klappt den Ordner der geöffneten Liste nicht wieder auf"
        # Eine Änderung an der Liste baut die Seitenleiste ebenfalls neu auf.
        with app.sidebar_change() as change:
            liste["note"] = "geändert"
            change.mark()
        ruhe()
        assert not offen(baum, ordner_iid), "auch nicht nach einer Änderung"
        assert baum.selection() == (f"list:{liste['id']}",), "die Auswahl bleibt"
        # Wer eine andere Liste im zugeklappten Ordner öffnet, sieht sie.
        app.set_active_list(andere["id"])
        ruhe()
        assert offen(baum, ordner_iid) and baum.selection() == (f"list:{andere['id']}",)
        # Globales Zuklappen hält ebenfalls.
        app.set_folder_open(ordner_mit_liste["id"], False)
        app.update_sidebar_list()
        ruhe()
        assert not offen(baum, ordner_iid)
        app.set_folder_open(ordner_mit_liste["id"], True)
        ruhe()

        # --- Seitenbereich: Bibliothek bleibt zu --------------------------------
        bibliothek = app.new_folder_object("Bücher", folder_kind="library")
        app.folders.append(bibliothek)
        buch = app.new_page_from_markdown("# Hobbit\n\nText\n")
        buch["folder_id"] = bibliothek["id"]
        app.save_items()
        app.update_sidebar_list()
        ruhe()
        seiten = app.pages_listbox
        bib_iid = f"folder:{bibliothek['id']}"
        assert seiten.exists(bib_iid) and seiten.exists(f"list:{buch['id']}")
        seiten.item(bib_iid, open=False)
        app.update_sidebar_list()
        ruhe()
        assert not offen(seiten, bib_iid), "zugeklappte Bibliothek bleibt zu"

        # --- Notizbereich ---------------------------------------------------------
        notizen = app.notes_listbox
        assert app.SIDEBAR_SECTIONS == ("views", "pinned", "pages", "lists", "notes", "drawings")
        assert app.pages_title_row.winfo_y() < app.sidebar_title_row.winfo_y() < app.notes_title_row.winfo_y()
        assert app.notes_title.cget("text") == "Notizen"
        # Ohne Notizen nur die Überschrift mit „+“.
        assert notizen.winfo_manager() == "" and app.add_notes_button.winfo_ismapped()
        lose = app.new_list_object("Einkaufsideen", [], list_kind="note")
        im_ordner = app.new_list_object("Protokoll", [], folder_id=ordner_mit_liste["id"], list_kind="note")
        buch_ordner = app.new_folder_object("Notizbuch 2026", folder_kind="journal")
        quartal = app.new_folder_object("Q3", parent_id=buch_ordner["id"], folder_kind="journal")
        app.folders.extend([buch_ordner, quartal])
        eintrag = app.new_list_object("Tagesnotiz · 29.09.2026", [], folder_id=quartal["id"], list_kind="note")
        app.lists.extend([lose, im_ordner, eintrag])
        app.save_items()
        app.update_sidebar_list()
        ruhe()
        assert notizen.winfo_manager() == "pack"
        assert notizen.exists(f"list:{lose['id']}") and not baum.exists(f"list:{lose['id']}")
        assert notizen.exists(f"folder:{buch_ordner['id']}") and not baum.exists(f"folder:{buch_ordner['id']}")
        assert notizen.parent(f"folder:{quartal['id']}") == f"folder:{buch_ordner['id']}"
        assert notizen.parent(f"list:{eintrag['id']}") == f"folder:{quartal['id']}"
        assert baum.exists(f"list:{im_ordner['id']}") and not notizen.exists(f"list:{im_ordner['id']}"), \
            "Notizen in gewöhnlichen Ordnern bleiben bei ihrem Ordner"
        # Öffnen markiert die Zeile im Notizbaum und nur dort.
        app.set_active_list(eintrag["id"])
        ruhe()
        assert notizen.selection() == (f"list:{eintrag['id']}",)
        assert not baum.selection() and not seiten.selection()
        assert app.get_selected_sidebar_row() == ("list", eintrag["id"])
        # Zuklappen im Notizbaum hält wie im Listenbaum.
        notizen.item(f"folder:{quartal['id']}", open=False)
        app.update_sidebar_list()
        ruhe()
        assert not offen(notizen, f"folder:{quartal['id']}")
        # Auswahl im Notizbaum öffnet die Liste.
        notizen.selection_set(f"list:{lose['id']}")
        ruhe()
        assert app.active_list_id == lose["id"] and app.view_mode == "list"
        assert notizen.selection() == (f"list:{lose['id']}",)

        # --- Pfeil und Titel ---------------------------------------------------
        assert app.notes_heading_icon.cget("text") == app.SIDEBAR_SECTION_ARROWS[True]
        app.toggle_sidebar_section("notes")
        ruhe()
        assert notizen.winfo_manager() == "" and app.notes_heading_icon.cget("text") == "▷"
        assert app.settings["sidebar_sections_closed"] == ["notes"]
        app.toggle_sidebar_section("notes")
        ruhe()
        assert notizen.winfo_manager() == "pack" and app.settings["sidebar_sections_closed"] == []
        assert app.normalize_personal_settings({"sidebar_sections_closed": ["notes", "folders"]})[
            "sidebar_sections_closed"] == ["notes"]
        app.notes_title.event_generate("<Button-1>")
        ruhe()
        assert app.view_mode == app.NOTES_VIEW and app.get_display_title() == "Notizen"
        assert app.notes_heading_frame.cget("bg") == app.theme["selection"]
        assert app.pages_heading_frame.cget("bg") != app.theme["selection"]
        assert app._stats_full_text == "3 Notizen", app._stats_full_text
        def uebersicht():
            texte, stapel = [], [app.home_content]
            while stapel:
                widget = stapel.pop()
                stapel.extend(widget.winfo_children())
                if isinstance(widget, mod.RoundedButton):
                    texte.append(widget.text)
                elif isinstance(widget, mod.tk.Label):
                    texte.append(widget.cget("text"))
            return texte

        texte = uebersicht()
        # Knöpfe zeigen „…“ nicht (RoundedButton.action_text).
        for erwartet in ("Neue Notiz", "Neues Notizbuch", "Notizbücher", "Alle Notizen",
                         "Einkaufsideen", "Protokoll", "Tagesnotiz · 29.09.2026", "1 Eintrag", "Notizbuch 2026"):
            assert any(erwartet in text for text in texte), (erwartet, texte)
        assert not any("Exposé" in text for text in texte), "nur Notizen, keine Listen"
        assert "Zuletzt bearbeitet" not in texte, "bei wenigen Notizen keine doppelten Zeilen"
        assert sum(text == "Einkaufsideen" for text in texte) == 1
        # Knöpfe und Hinweise fluchten über alle Abschnitte.
        stapel, zeilenknoepfe = [app.home_content], []
        while stapel:
            widget = stapel.pop()
            stapel.extend(widget.winfo_children())
            if isinstance(widget, mod.RoundedButton) and widget.winfo_manager() == "grid" \
                    and not isinstance(widget.master, mod.ButtonFlow):
                zeilenknoepfe.append(widget)
        assert len(zeilenknoepfe) == 4, len(zeilenknoepfe)
        assert len({knopf.winfo_rootx() + knopf.winfo_width() for knopf in zeilenknoepfe}) == 1, "rechte Kanten"
        # Die Übersicht hat keinen Datensatz, dessen Titel sich ändern ließe.
        aufrufe = []
        app.edit_list_details = lambda *args, **kwargs: aufrufe.append(args)
        app.edit_title()
        app.set_pages_view()
        ruhe()
        app.edit_title()
        assert not aufrufe
        del app.edit_list_details

        # --- „+“ neben „Notizen“ -------------------------------------------------
        gerufen = []

        def merken(*args, **kwargs):
            gerufen.append((args, kwargs))
            return "break"
        app._popup_at_widget = lambda menu, widget: gerufen.append(("menu", eintraege(menu), widget))
        app.show_notes_add_menu()
        _art, labels, knopf = gerufen.pop()
        assert labels == ["Neue Notiz", "Aus Vorlage", "Neuer Ordner …", "Neues Notizbuch …"], labels
        assert knopf is app.add_notes_button
        app.set_active_folder(quartal["id"])
        ruhe()
        app.show_notes_add_menu()
        _art, labels, _knopf = gerufen.pop()
        assert labels[0] == "Tagesnotiz in „Q3“", labels
        # Vorlagen: Notizvorlagen und der Jahresordner.
        vorlagen = [vorlage["title"] for vorlage in app.note_templates()]
        assert "Notizbuch – Tagesnotiz" in vorlagen and all("Seite" not in titel for titel in vorlagen)
        app.set_home_view()
        ruhe()
        vorher = len(app.lists)
        app.create_new_note()
        ruhe()
        neu = app.lists[-1]
        assert len(app.lists) == vorher + 1 and neu["list_kind"] == "note" and not neu.get("folder_id")
        assert app.active_list_id == neu["id"] and notizen.selection() == (f"list:{neu['id']}",)
        app.create_new_note(quartal["id"])
        ruhe()
        datiert = app.lists[-1]
        assert datiert["folder_id"] == quartal["id"] and datiert["title"].startswith("Tagesnotiz · ")

        # --- „+“ und „…“ in Seiten- und Notizbaum ---------------------------------
        seiten.item(bib_iid, open=True)
        for bereich, iid, erwartet in (
                (seiten, bib_iid, ["Neue Seite", "Seite aus Vorlage", "Neuer Unterordner …", "Neues Buch …"]),
                (notizen, f"folder:{buch_ordner['id']}", None)):
            bereich.see(iid)
            ruhe()
            box = bereich.bbox(iid)
            assert box, iid
            app.on_sidebar_quick_motion(SimpleNamespace(widget=bereich, x=20, y=box[1] + box[3] // 2))
            ruhe()
            plus, mehr = app.sidebar_quick_pair(bereich)
            assert app.sidebar_quick_tree is bereich and app.sidebar_quick_kind == "folder"
            assert plus.winfo_manager() == "place" and mehr.winfo_manager() == "place"
            assert app.sidebar_quick_add_button.winfo_manager() == "", "nur ein Baum zeigt Knöpfe"
            app.sidebar_quick_add()
            _art, labels, knopf = gerufen.pop()
            assert knopf is plus
            if erwartet:
                assert labels == erwartet, labels
            else:
                assert labels[0] == "Neue Tagesnotiz" and "Neuer Unterordner …" in labels, labels
            app.sidebar_quick_more()
            _art, labels, knopf = gerufen.pop()
            assert knopf is mehr and labels
            app.hide_sidebar_quick_actions()
            assert plus.winfo_manager() == "" and mehr.winfo_manager() == ""
        # Ein Unterordner erbt die Ordnerart.
        app.create_container_dialog = merken
        for folder, art in ((bibliothek, "library"), (buch_ordner, "journal")):
            menu = app.folder_quick_add_menu(folder["id"])
            menu.invoke(menu.index("end"))
            ruhe(2)
            assert gerufen.pop() == (("folder",), {"parent_id": folder["id"], "folder_kind": art, "sidebar_section": "pages" if art == "library" else "notes"})
        menu = app.folder_quick_add_menu(ordner_mit_liste["id"])
        menu.invoke(menu.index("end"))
        # Ein Eintrag mit „…“ öffnet ein Fenster und läuft erst nach dem
        # Schließen des Menüs (R11, 29.09.2026).
        assert not gerufen
        ruhe(2)
        assert gerufen.pop() == (("folder",), {"parent_id": ordner_mit_liste["id"], "folder_kind": "journal", "sidebar_section": "lists"})
        menu = app.folder_quick_add_menu(None)
        assert "Neuer Ordner …" in eintraege(menu) and eintraege(menu)[-1] == "Listen importieren …"
        del app.create_container_dialog
        del app._popup_at_widget

        # --- Kontextmenü im Notizbaum ------------------------------------------
        app.set_active_list(liste["id"])
        ruhe()
        notizen.see(f"list:{lose['id']}")
        ruhe()
        box = notizen.bbox(f"list:{lose['id']}")
        app._destroy_sidebar_context_menu()
        gezeigt = []
        original_popup = mod.tk.Menu.tk_popup
        mod.tk.Menu.tk_popup = lambda self, *args: gezeigt.append(self)
        try:
            app.show_sidebar_context_menu(SimpleNamespace(widget=notizen, x=20, y=box[1] + box[3] // 2,
                                                          x_root=0, y_root=0))
        finally:
            mod.tk.Menu.tk_popup = original_popup
        assert gezeigt and notizen.selection() == (f"list:{lose['id']}",) and not baum.selection()
        app._destroy_sidebar_context_menu()

        # --- Kleines Fenster ---------------------------------------------------
        for _ in range(12):
            app.lists.append(app.new_list_object("Notiz", [], list_kind="note"))
        app.save_items()
        app.update_sidebar_list()
        app.set_notes_view()
        ruhe()
        texte = uebersicht()
        assert "Zuletzt bearbeitet" in texte and texte.count("Notiz") >= 6
        # Seitenübersicht: dieselbe Tabelle, Sterne davor.
        app.set_pages_view()
        ruhe()
        zeilenknoepfe, stapel = [], [app.home_content]
        while stapel:
            widget = stapel.pop()
            stapel.extend(widget.winfo_children())
            if isinstance(widget, mod.RoundedButton) and widget.winfo_manager() == "grid" \
                    and not isinstance(widget.master, mod.ButtonFlow):
                zeilenknoepfe.append(widget)
        sterne = [knopf for knopf in zeilenknoepfe if knopf.text in ("☆", "★")]
        titel = [knopf for knopf in zeilenknoepfe if knopf not in sterne]
        assert sterne and len(sterne) == len(titel)
        assert len({knopf.winfo_rootx() + knopf.winfo_width() for knopf in titel}) == 1, "rechte Kanten"
        app.set_active_list(eintrag["id"])
        root.geometry("860x700")
        ruhe(10)
        # Der Notiztext behält bei Mindesthöhe seine Zeilen (vorher ein Strich).
        editor = app.rich_note_editor
        assert editor is not None and editor.text.winfo_height() >= 4 * 18, editor.text.winfo_height()
        assert int(editor.text.cget("highlightthickness")) == 0
        zeile = int(mod.ttk.Style().lookup("Sidebar.Treeview", "rowheight") or 20)
        assert baum.winfo_height() / zeile >= 3.0, baum.winfo_height() / zeile
        unten = app.sidebar_frame.winfo_rooty() + app.sidebar_frame.winfo_height()
        assert app.notes_title_row.winfo_ismapped()
        assert app.notes_title_row.winfo_rooty() + app.notes_title_row.winfo_height() <= unten
        assert notizen.winfo_rooty() + notizen.winfo_height() <= unten + 1, "Notizbaum ragt nicht heraus"
        assert 1 <= int(notizen.cget("height")) <= app.PAGES_SIDEBAR_MAX_ROWS
        vorher = int(notizen.cget("height"))
        root.geometry("1300x1000")
        ruhe(10)
        assert vorher <= int(notizen.cget("height")) <= app.PAGES_SIDEBAR_MAX_ROWS, "mehr Platz gibt Zeilen zurück"
        if app.sidebar_tree_row_budget() >= 2 * app.PAGES_SIDEBAR_MAX_ROWS + app.SIDEBAR_LISTS_MIN_ROWS:
            assert int(notizen.cget("height")) == app.PAGES_SIDEBAR_MAX_ROWS, "bei ausreichendem Platz acht Zeilen"
        assert baum.winfo_height() / zeile >= 3.0

        assert not fehler, fehler[:1]
    finally:
        try:
            root.destroy()
        except Exception:
            pass

print("OK: Einklappen, Notizbereich, Ordner in Seiten und Notizen, kleine Fenster geprüft.")
