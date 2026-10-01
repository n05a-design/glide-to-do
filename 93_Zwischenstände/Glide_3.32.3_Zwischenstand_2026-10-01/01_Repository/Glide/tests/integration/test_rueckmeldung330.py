"""Rückmeldung zu 3.30.0 vom 26.09.2026: Abstände, Kopfzeile, Seitenleiste, Mein Tag, Zeichenfläche.

- Seitenleiste und Inhaltsbereich enden in jeder Ansicht auf derselben Linie.
- Die Kopfzeile packt ihre Knöpfe in fester Reihenfolge; der Änderungsverlauf
  ist ein Knopf neben „Drucken“ und öffnet seine Seite auf einer Karte.
- „In Bearbeitung“ ist ein Abschnitt von „Mein Tag“, keine Seitenleistenzeile;
  „Listen und Ordner“ hat keinen Klapppfeil mehr.
- Zeichenfläche: Die Statuszeile hat immer zwei Zeilen, die Kontextleiste
  reserviert die Zeilen des längsten Werkzeugs – die Fläche springt nicht.
  Ein Klick neben die Auswahl hebt sie auf, über der Auswahl zeigt der Zeiger
  das Verschieben an.

Zweite Rückmeldung (26.09.2026, abends):

- Punktdialog mit Verlauf öffnet ohne Endlosschleife und in voller Größe.
- Kennzahlen unter dem Titel ohne Kasten, „Startseite anpassen“ unten.
- Farbe nur mit Bedeutung; Eingabezeile und Leisten nur, wo sie wirken.
- „Erledigte Punkte löschen“ legt in den Papierkorb, Rückgängig holt zurück.
- Rückgängig-Speicher gepackt, Neuzeichnen nur bei Größenänderung.
"""
import importlib.machinery
import importlib.util
import os
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory(prefix="glide-rueckmeldung-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    sys.dont_write_bytecode = True
    loader = importlib.machinery.SourceFileLoader("glide_rueckmeldung", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1400x900+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: None

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    def unterkante(widget):
        return widget.winfo_rooty() + widget.winfo_height() - root.winfo_rooty()

    def rechte_unterkante():
        """Tiefste sichtbare Karte oder Leiste im Inhaltsbereich."""
        tief = 0
        stapel = [app.content_frame]
        while stapel:
            widget = stapel.pop()
            try:
                if not widget.winfo_ismapped():
                    continue
                # Seit 29.09.2026 stehen Hinweis und Auswahlleiste im Fuß
                # der Inhaltskarte; die Karte selbst schließt die Spalte ab.
                if isinstance(widget, (mod.RoundedContainer, mod.RoundedButton)):
                    grenze = unterkante(app.content_frame)
                    tief = max(tief, min(unterkante(widget), grenze))
                    continue
                stapel.extend(widget.winfo_children())
            except mod.tk.TclError:
                continue
        return tief

    try:
        normal = next(entry for entry in app.lists
                      if entry.get("list_kind") in (None, "", "list", "tasks") and len(entry.get("items", [])) > 5)
        zeichnung = next(entry for entry in app.lists if entry.get("list_kind") == "drawing")
        ansichten = {
            "Startseite": app.set_home_view,
            "Liste": lambda: app.set_active_list(normal["id"]),
            "Pinnwand": lambda: (app.set_active_list(normal["id"]), app.open_board_view()),
            "Zeichenfläche": lambda: app.set_active_list(zeichnung["id"]),
            "Verlauf": app.open_history_view,
            "Vorlagen": app.set_template_view,
            "Mein Tag": app.set_plan_day_view,
        }
        # --- Abstände: beide Spalten enden auf derselben Linie -------------
        for name, oeffnen in ansichten.items():
            oeffnen()
            ruhe()
            links, rechts = unterkante(app.sidebar_shell), rechte_unterkante()
            assert abs(links - rechts) <= 1, (name, links, rechts)

        # --- Kopfzeile: feste Reihenfolge, Verlauf als Knopf ----------------
        erwartet = ["settings_button", "notifications_button", "capture_button", "actions_button",
                    "search_button", "sidebar_toggle_button", "print_button", "history_button"]
        def reihenfolge():
            namen = {str(getattr(app, name)): name for name in erwartet + ["header_overflow_button"]}
            return [namen.get(str(knopf), str(knopf)) for knopf in app.header_controls.pack_slaves()]
        assert reihenfolge() == erwartet, reihenfolge()
        for breite in (1400, 860, 1400):
            app._header_density = None
            app.sync_header_density(type("Ereignis", (), {"width": breite})())
            ruhe()
        assert reihenfolge() == erwartet, ("nach Dichtewechsel", reihenfolge())
        app._header_density = "minimal"
        app.pack_header_controls()
        assert reihenfolge()[0] == "header_overflow_button", reihenfolge()
        app._header_density = None
        app.pack_header_controls()
        app.set_home_view()
        ruhe()
        app.history_button.command()
        ruhe()
        assert app.view_mode == app.HISTORY_VIEW
        karten = [w for w in app.home_content.winfo_children() if isinstance(w, mod.RoundedContainer)]
        assert karten, "Der Verlauf steht auf einer Karte"
        grund = app.theme["bg"].lower()
        stapel = list(karten[0].inner.winfo_children())
        while stapel:
            widget = stapel.pop()
            stapel.extend(widget.winfo_children())
            if isinstance(widget, mod.tk.Label):
                assert str(widget.cget("bg")).lower() != grund, ("Beschriftung in Fensterfarbe", str(widget))
        eintraege = [entry["label"] for entry in app.app_action_entries() if entry["label"] == "Änderungsverlauf"]
        assert eintraege, "Änderungsverlauf in der Aktionssuche"

        # --- Seitenleiste ---------------------------------------------------
        zeilen = app.system_listbox.get_children("")
        assert app.IN_PROGRESS_ROW_ID not in zeilen and "smart:history" not in zeilen, zeilen
        assert not hasattr(app, "folders_section_toggle")
        assert app.sidebar_section_open("folders")

        # --- Mein Tag: „In Bearbeitung“ als Abschnitt -----------------------
        app.set_plan_day_view()
        ruhe()
        abschnitte = list(app.tree.get_children(""))
        assert app.PLAN_IN_PROGRESS_ROW_ID in abschnitte, abschnitte
        if app.PLAN_INBOX_HEADING_ROW_ID in abschnitte:
            assert abschnitte.index(app.PLAN_IN_PROGRESS_ROW_ID) < abschnitte.index(app.PLAN_INBOX_HEADING_ROW_ID)
        zeilen = app.tree.get_children(app.PLAN_IN_PROGRESS_ROW_ID)
        erwartet_anzahl = len(app.plan_in_progress_entries())
        assert len(zeilen) == erwartet_anzahl > 0, (len(zeilen), erwartet_anzahl)
        heute = {eintrag[4].get("id") for eintrag in app.plan_day_entries(apply_filters=False)}
        for zeile in zeilen:
            _liste, punkt = app.in_progress_item_sources[zeile]
            assert punkt not in heute, "Eingeplantes steht nicht doppelt da"
        app.tree.focus(app.PLAN_IN_PROGRESS_ROW_ID)
        app.open_in_progress_source_item()
        ruhe()
        assert app.view_mode == "in_progress", "Doppelklick auf den Abschnitt öffnet die ganze Ansicht"

        # --- Zeichenfläche --------------------------------------------------
        app.set_active_list(zeichnung["id"])
        ruhe(10)
        editor = next(w for w in app.list_frame_outer.inner.winfo_children() if isinstance(w, mod.DrawingEditor))
        editor.reference_message = "Referenz: probe.png · nicht bemalbar"

        def flaeche():
            ruhe()
            return editor.canvas.winfo_height()

        editor.update_status()
        hoehe = flaeche()
        for schritt in (editor.toggle_grid, editor.toggle_grid, lambda: editor.set_tool("select"), editor.select_all,
                        lambda: editor.update_status("Ganze Fläche ausgewählt"), lambda: editor.set_tool("line"),
                        lambda: editor.set_tool("fill"), lambda: editor.set_tool("brush"), editor.update_status):
            schritt()
            assert flaeche() == hoehe, ("Zeichenfläche springt", schritt)
        assert editor.status.cget("text").count("\n") == 1, "Statuszeile hat immer zwei Zeilen"

        editor.set_tool("select")
        editor.deselect()
        ruhe()
        editor._begin_select((2, 2))
        editor._update_marquee((6, 6))
        editor._release()
        assert editor.selection == (2, 2, 6, 6)
        editor._sync_select_cursor((4, 4))
        assert str(editor.canvas.cget("cursor")) == "fleur", "Verschiebe-Zeiger über der Auswahl"
        editor._sync_select_cursor((20, 20))
        assert str(editor.canvas.cget("cursor")) == "crosshair"
        editor._begin_select((20, 20))
        editor._release()
        assert editor.selection is None, "Klick neben die Auswahl hebt sie auf"
        editor.select_all()
        assert editor.option_buttons.get("deselect") is not None, "Knopf „Aufheben“"
        editor.deselect()
        assert editor.selection is None
        assert not fehler, fehler[:1]

        # --- Zweite Rückmeldung ----------------------------------------------
        # Farbe nur mit Bedeutung.
        # Seit 29.09.2026 (R8): „clear“ ist nicht mehr Rot; die Beschriftung entscheidet.
        assert app.button_color_key("confirm") == "confirm" and app.button_color_key("clear") == "muted"
        assert app.button_color_key("clear", "Listen/Ordner hinzufügen …") == "add"
        assert app.button_color_key("confirm", "Globale Pinnwand") == "muted"
        assert app.button_color_key("confirm", "Neue Seite") == "add"
        assert app.button_color_key("muted", "Löschen") == "delete"
        assert app.button_color_key("confirm", "Suche löschen") == "muted"
        assert app.button_color_key("accent", "Wiederherstellen") == "confirm"
        assert app.button_color_key("confirm", "Speichern …") == "muted"
        assert app.theme["add"] and app.theme["add"] != app.theme["delete"]
        assert app.button_color_key("accent") == "muted" and app.button_color_key("export") == "muted"
        assert app.button_color_key(app.theme["confirm"]) == "confirm"
        assert app.add_button.color_key == "add" and app.notifications_button.color_key == "due_today"  # R8: Hinzufügen Lila, Hinweise Gelb
        # Kennzahlen unter dem Titel als Text ohne eigene Fläche.
        app.set_active_list(normal["id"])
        ruhe()
        chips = [w for w in app.page_chip_row.winfo_children() if not getattr(w, "_is_backdrop", False)]
        assert chips and all(isinstance(w, mod.CanvasLabel) for w in chips)
        # Zeichenfläche: um die Zeichnung herum die Kartenfarbe.
        app.set_active_list(zeichnung["id"])
        ruhe()
        editor = next(w for w in app.list_frame_outer.inner.winfo_children() if isinstance(w, mod.DrawingEditor))
        assert str(editor.canvas.cget("bg")).lower() == app.theme["card"].lower()
        # „Startseite anpassen“ steht unter den Kacheln.
        app.set_home_view()
        ruhe()
        knopf = next(w for w in app.home_content.winfo_children()
                     if any(isinstance(k, mod.RoundedButton) and k.text == "Startseite anpassen"
                            for k in w.winfo_children()))
        assert knopf.pack_info()["side"] == "bottom"
        # Papierkorb: keine Eingabezeile, keine Knopfleisten; abgeleitete
        # Ansichten ohne Eingabezeile; in der Liste ist alles wieder da.
        # Seit 29.09.2026 stehen Hinweis und Auswahlleiste im Kartenfuß
        # (`card_foot_mode`); die Leiste erscheint nur bei Auswahl.
        app.set_trash_view()
        ruhe()
        assert app.input_frame.winfo_manager() == "" and app.button_frame.winfo_manager() == ""
        assert app.card_foot_mode() == "hint"
        app.set_plan_day_view()
        ruhe()
        assert app.input_frame.winfo_manager() == "" and app.card_foot_mode() == "hint"
        app.set_active_list(normal["id"])
        app.open_list_view()  # die Liste stand oben noch auf „Pinnwand“
        ruhe()
        assert app.input_frame.winfo_manager() == "pack" and app.card_foot_mode() == "hint"
        assert app.input_frame.winfo_y() < app.search_frame.winfo_y(), "Eingabe steht wieder über der Suche"
        # Erledigte Punkte löschen: in den Papierkorb, Rückgängig holt zurück.
        liste = next(entry for entry in app.lists if entry["id"] == normal["id"])
        erledigt = [item["id"] for item in app.walk_items(liste["items"]) if item.get("done")]
        assert erledigt, "Beispieldaten enthalten Erledigtes"
        papierkorb_vorher = len(app.trash)
        mod.ListApp.ask_yes_no = lambda self, *args, **kwargs: True
        app.remove_done_items()
        liste = next(entry for entry in app.lists if entry["id"] == normal["id"])
        assert not [item for item in app.walk_items(liste["items"]) if item.get("done")
                    and not [kind for kind in item.get("children", []) if not kind.get("done")]]
        assert len(app.trash) > papierkorb_vorher
        # Rückgängig-Speicher: gepackt, und Rückgängig stellt den Stand her.
        assert isinstance(app.undo_stack[-1]["lists"], mod.PackedState)
        app.undo_last_change()
        liste = next(entry for entry in app.lists if entry["id"] == normal["id"])
        assert {item["id"] for item in app.walk_items(liste["items"]) if item.get("done")} >= set(erledigt)
        assert len(app.trash) == papierkorb_vorher
        # Punktdialog mit Verlauf: öffnet, ohne dass Tk endlos neu anordnet.
        app.set_design("dark")
        app.set_backdrop_choice("glut")
        app.wait_for_backdrop(60)
        ruhe()
        gemessen = {}

        def pruefen(self, dialog, parent=None, **kwargs):
            import time as zeit
            start = zeit.monotonic()
            dialog.update_idletasks()
            gemessen["dauer"] = zeit.monotonic() - start
            gemessen["hoehe"] = dialog.winfo_height()
            dialog.destroy()

        mod.ListApp.run_modal = pruefen
        app.tree.selection_set(app.tree.get_children("")[1])
        app.tree.focus(app.tree.get_children("")[1])
        app.edit_item()
        assert gemessen.get("dauer", 99) < 5, gemessen
        # Neuzeichnen nur bei echter Größenänderung.
        knopf = app.add_button
        gezeichnet = []
        alt = knopf._draw
        knopf._draw = lambda: gezeichnet.append(1) or alt()
        knopf.event_generate("<Configure>", width=knopf.winfo_width(), height=knopf.winfo_height(), x=5, y=5)
        assert not gezeichnet, "Verschieben zeichnet nicht neu"
        assert not fehler, fehler[:1]
    finally:
        app.dirty = False
        root.destroy()

print("test_rueckmeldung330: OK; Unterkanten in sieben Ansichten, Kopfzeilenreihenfolge, Verlauf als Knopf "
      "und Karte, Seitenleiste, „In Bearbeitung“ in „Mein Tag“, ruhige Zeichenfläche und Auswahl geprüft.")
