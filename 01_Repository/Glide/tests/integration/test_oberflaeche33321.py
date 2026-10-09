"""Paket Ruhige Oberfläche 3.33.21: N01 und folgende Aufgaben über echte Einstiege.

N01: Einstellung „Automatisch hell/dunkel nach System“ merkt das Paar des
gewählten Designs, wechselt bei simuliertem Systemwechsel ohne Neustart,
lässt ohne Erkennung das Design stehen, bleibt nach Neustart erhalten und
fällt bei unlesbarem Wert auf „aus“ zurück. Pixel steht in der Auswahl vorn.

--app wählt den Quellstand; mit der unveränderten 3.33.20 muss die Suite rot
sein (Gegenprobe). Künstliche Daten in einem temporären GLIDE_DATA_DIR.
"""
import argparse
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import time
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix="glide-oberflaeche-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_oberflaeche_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    fehler = []
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
    app.show_info = lambda *a, **k: None
    pruefungen = []

    def ruhe(sekunden=0.15):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    def neu_starten():
        global root, app
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
        root = mod.tk.Tk()
        root.geometry("1280x840+20+20")
        root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
        app = mod.ListApp(root)
        app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
        app.show_info = lambda *a, **k: None
        ruhe()

    try:
        # --- N01: Einstellung und Wechsel ohne Neustart ---------------------
        assert app.DESIGN_ORDER[0] == "pixel", app.DESIGN_ORDER
        system = {"dunkel": False}
        app.system_is_dark = lambda: system["dunkel"]
        app.set_design("glass_dark")
        ruhe()

        def einstellungen(auto):
            def run_modal(dialog, *a, **k):
                dialog.update()
                haken = next(w for w in descendants(dialog) if w.winfo_name() == "setting_design_auto")
                if (str(haken.getvar(str(haken.cget("variable")))) in ("1", "True", "true")) != auto:
                    haken.invoke()
                knopf = next(w for w in descendants(dialog) if getattr(w, "text", None) == "Speichern")
                knopf.command()
            with patch.object(app, "run_modal", side_effect=run_modal):
                app.show_settings_dialog()
            ruhe()

        einstellungen(True)
        assert app.settings["design_auto"] == {"light": "glass_light", "dark": "glass_dark"}, app.settings.get("design_auto")
        assert app.design_name() == "glass_light", app.design_name()  # System hell
        system["dunkel"] = True
        assert app.sync_system_appearance() is True and app.design_name() == "glass_dark"
        assert app.theme_name == "dark"
        assert app.sync_system_appearance() is False  # unverändert: nichts zu tun
        system["dunkel"] = None
        assert app.sync_system_appearance() is False and app.design_name() == "glass_dark"
        pruefungen.append("N01: Paar aus dem gewählten Design, Wechsel ohne Neustart, ohne Erkennung bleibt das Design")

        # Pixel ohne helles Gegenstück: bei hellem System „Hell“.
        app.set_design("pixel")
        system["dunkel"] = False
        einstellungen(True)
        assert app.settings["design_auto"] == {"light": "light", "dark": "pixel"}
        assert app.design_name() == "light"
        system["dunkel"] = True
        app.sync_system_appearance()
        assert app.design_name() == "pixel"
        pruefungen.append("N01: Pixel folgt dem System mit „Hell“ als hellem Gegenstück")

        # Neustart: Wahl bleibt; ausschalten beendet das Folgen.
        neu_starten()
        app.system_is_dark = lambda: system["dunkel"]
        assert app.settings["design_auto"] == {"light": "light", "dark": "pixel"} and app.design_name() == "pixel"
        einstellungen(False)
        assert "design_auto" not in app.settings
        system["dunkel"] = False
        assert app.sync_system_appearance() is False and app.design_name() == "pixel"
        normal = mod.ListApp.normalize_settings_330({"design_auto": {"light": "weg", "dark": "pixel"}})
        assert "design_auto" not in normal
        echte = app.__class__.system_is_dark(app)
        assert echte in (True, False, None), echte
        pruefungen.append("N01: Wahl übersteht Neustart; aus beendet das Folgen; Unlesbares ergibt aus")

        # --- U15: Lila nur für Hinzufügen -------------------------------------
        liste = app.new_list_object("Umschalter", [app.new_item("Punkt")])
        app.lists.append(liste)
        app.save_items()
        for design in app.DESIGN_ORDER:
            app.set_design(design)
            app.set_active_list(liste["id"])
            ruhe(0.05)
            theme = app.theme
            assert mod.contrast_ratio(theme["active_text"], theme["active"]) >= 4.5, design
            if app.design_info()["layer"] != "minimal":
                # In den Minimaldesigns ist alles grau; sonst unterscheiden sich die Rollen.
                assert theme["active"] not in (theme["add"], theme["selection"]), design
            assert app.list_view_button.active_fill == theme["active"], design
            assert app.table_button.active_fill is None, design
            plus = app.add_button
            assert app.button_color_key(plus.color_key if hasattr(plus, "color_key") else "add", "+") == "add"
        app.set_design("glass_dark")
        app.set_table_view()
        ruhe()
        assert app.table_button.active_fill == app.theme["active"] and app.list_view_button.active_fill is None
        pruefungen.append("U15: offene Ansicht in allen zehn Designs neutral und lesbar, Lila bleibt bei „+“")

        # --- U05r: Gismo-Kachel in Ruhe ohne Knöpfe ----------------------------
        app.set_home_view()
        ruhe(0.3)
        leiste = app._mascot_care_bar
        kachel = leiste.master
        texte = [w.text for w in descendants(leiste) if isinstance(w, mod.RoundedButton)]
        assert texte == ["Füttern", "Spielen", "Ruhen", "Spielereien aus", "Benennen"], texte
        assert leiste.winfo_manager() == "", "Pflegeknöpfe im Ruhezustand sichtbar"
        hoehe = kachel.winfo_height()
        neubau = []
        bauen = app.refresh_home
        app.refresh_home = lambda: neubau.append(True)
        kachel.event_generate("<Enter>")
        ruhe(0.05)
        assert leiste.winfo_manager() == "place" and kachel.winfo_height() == hoehe, (leiste.winfo_manager(), hoehe)
        figur = next(w for w in descendants(kachel) if isinstance(w, mod.MascotCanvas))
        app.root.focus_set()
        kachel.event_generate("<Leave>")
        ruhe(0.25)
        assert leiste.winfo_manager() == "", "Leiste bleibt nach dem Verlassen stehen"
        figur.event_generate("<FocusIn>")
        ruhe(0.05)
        assert leiste.winfo_manager() == "place", "Tastaturfokus zeigt die Leiste nicht"
        assert all(int(str(w.cget("takefocus")) or 0) for w in descendants(leiste)
                   if isinstance(w, mod.RoundedButton)), "Pflegeknöpfe nicht per Tastatur erreichbar"
        assert neubau == [], "Überfahren baute die Startseite neu"
        app.refresh_home = bauen
        pruefungen.append("U05r: Gismo-Kachel in Ruhe nur Figur und Balken; Überfahren und Fokus zeigen die Pflege "
                          "ohne Höhenänderung und ohne Neuaufbau")

        # --- U09: eine Zeile über der Pinnwand ---------------------------------
        label = app.new_label_object("Wichtig")
        app.labels.append(label)
        pinnwand = app.new_list_object("Pinnwand", [app.new_item(f"Karte {i}", labels=[label["id"]] if i == 0 else [])
                                                     for i in range(3)])
        app.lists.append(pinnwand)
        app.save_items()
        app.set_active_list(pinnwand["id"])
        app.open_board_view()
        ruhe(0.3)
        w = app.workspace
        oben = w.canvas.winfo_rooty() - w.bar.winfo_rooty()
        auswahl = [x for x in descendants(w.body) if isinstance(x, mod.AppOptionMenu)]
        assert not auswahl, [x.options for x in auswahl]  # keine zweite Zeile mit Auswahlfeldern
        texte = [getattr(x, "text", "") for x in descendants(w.bar)]
        assert "Mehr" in texte and "Raster" in texte and "Vorschau" not in texte, texte
        menu = w.board_settings_menu(root)
        eintraege = [menu.entrycget(i, "label") for i in range(menu.index("end") + 1) if menu.type(i) != "separator"]
        assert eintraege[:5] == ["Anordnung", "Labelfilter", "Kartengröße", "Verbindungsart", "Zoom"], eintraege
        assert any("Navigator" in e for e in eintraege) and any("Bildvorschau" in e for e in eintraege)
        zoom = menu.nametowidget(menu.entrycget(4, "menu"))
        zoom.invoke([zoom.entrycget(i, "label").strip(" ✓") for i in range(zoom.index("end") + 1)].index("150 %"))
        ruhe(0.2)
        assert w.board()["zoom"] == 150, w.board().get("zoom")
        menu = w.board_settings_menu(root)
        filtermenu = menu.nametowidget(menu.entrycget(1, "menu"))
        filtermenu.invoke([filtermenu.entrycget(i, "label").strip(" ✓") for i in range(filtermenu.index("end") + 1)].index("Wichtig"))
        ruhe(0.2)
        assert w.filter_label == label["id"], w.filter_label
        mehr = next(x for x in descendants(w.bar) if getattr(x, "text", "") == "Mehr")
        assert mehr.active_fill == app.theme["active"], "aktiver Labelfilter nicht sichtbar"
        w.set_label_filter("")
        pruefungen.append(f"U09: Pinnwand mit einer Werkzeugzeile ({oben} px bis zur Fläche), seltene Einstellungen "
                          "im Menü „…“, aktiver Labelfilter markiert")

        # --- U18: Seitentitel im Dokument, Schreibhinweis in leerer Seite ------
        seite = app.new_list_object("Wochenbericht", [], list_kind=app.LIST_KIND_PAGE)
        app.lists.append(seite)
        app.save_items()
        app.set_active_list(seite["id"])
        ruhe(0.3)
        editor = app.rich_note_editor
        assert isinstance(editor, mod.PageEditor) and not isinstance(editor, mod.NoteEditor)
        assert editor.title_label.cget("text") == "Wochenbericht"
        assert editor.title_label.winfo_ismapped() and editor._placeholder.winfo_manager() == "place"
        assert editor.title_label.winfo_rooty() < editor.text.winfo_rooty(), "Titel steht nicht über dem Text"
        editor.text.focus_set()
        editor.text.insert("1.0", "Erster Satz")
        editor.text.event_generate("<<Modified>>")
        ruhe(0.6)
        assert editor._placeholder.winfo_manager() == "", "Hinweis bleibt beim Tippen stehen"
        editor.flush()
        ruhe(0.1)
        gespeichert = app.page_entry(seite["id"]).get("rich_note") or {}
        assert gespeichert.get("text") == "Erster Satz", gespeichert  # Hinweis und Titel nicht im Text

        # Der echte Umbenennen-Weg; nur der Dialog liefert die neue Eingabe.
        with patch.object(app, "themed_page_details_dialog",
                          side_effect=lambda *a, **k: {"title": "Monatsbericht"}) as dialog:
            # Klick auf den Titel; Return und Leertaste sind an dieselbe Stelle gebunden.
            editor.title_label.event_generate("<Button-1>", x=4, y=4)
            ruhe(0.2)
        assert dialog.call_count == 1, dialog.call_count
        aktuell = app.rich_note_editor
        assert aktuell.title_label.cget("text") == "Monatsbericht", aktuell.title_label.cget("text")
        assert "<Key-Return>" in aktuell.title_label.bind(), aktuell.title_label.bind()
        assert app.get_display_title().startswith("Monatsbericht"), app.get_display_title()
        notiz = app.new_list_object("Notiz", [], list_kind=app.LIST_KIND_NOTE)
        app.lists.append(notiz)
        app.save_items()
        app.set_active_list(notiz["id"])
        ruhe(0.2)
        assert app.rich_note_editor.title_label is None, "Notizen zeigen keinen zweiten Titel"
        pruefungen.append("U18: Seitentitel über der Lesespalte, Klick/Return benennt über den bestehenden Weg um, "
                          "Schreibhinweis nur leer und nie gespeichert; Notizen unverändert")

        # --- OB05: schmale Seitenleiste ------------------------------------------
        app.set_home_view()
        ruhe(0.2)
        assert app.sidebar_shell.winfo_ismapped() and not app.sidebar_rail.winfo_ismapped()
        kopf = app.header_controls.winfo_rooty()
        inhalt_vorher = app.content_frame.winfo_width()
        app.set_pinned("list", pinnwand["id"], True)
        aktionen = {eintrag["id"] for eintrag in app.app_action_entries()}
        assert "toggle_sidebar_narrow" in aktionen
        app.toggle_sidebar_narrow()
        ruhe(0.2)
        assert app.sidebar_rail.winfo_ismapped() and not app.sidebar_shell.winfo_ismapped()
        assert app.header_controls.winfo_rooty() == kopf, "Kopf springt"
        assert app.content_frame.winfo_width() > inhalt_vorher
        knoepfe = app.sidebar_rail_buttons
        titel = [k.rail_title for k in knoepfe]
        systemzeilen = len(app.system_listbox.get_children(""))
        assert len(knoepfe) == systemzeilen + len(app.pinned_pages()) + 1, titel
        assert any(t.startswith("Heute") for t in titel) and "Pinnwand" in titel, titel
        assert all(int(str(k.cget("takefocus")) or 0) for k in knoepfe)
        assert all("<Key-Down>" in k.bind() and "<Key-Return>" in k.bind() for k in knoepfe)
        heute = next(k for k in knoepfe if k.rail_title.startswith("Heute"))
        heute.event_generate("<Button-1>")
        ruhe(0.3)
        assert app.view_mode == app.PLAN_DAY_VIEW, app.view_mode
        heute = next(k for k in app.sidebar_rail_buttons if k.rail_title.startswith("Heute"))
        assert heute.cget("bg") == app.theme["selection"], "geöffnete Ansicht nicht markiert"
        app.toggle_sidebar()  # ausblenden …
        ruhe(0.1)
        assert not app.sidebar_rail.winfo_ismapped() and not app.sidebar_shell.winfo_ismapped()
        app.toggle_sidebar()  # … und wieder schmal einblenden
        ruhe(0.1)
        assert app.sidebar_rail.winfo_ismapped()
        assert app.load_settings().get("sidebar_narrow") is True
        app.set_design("pixel")
        ruhe(0.2)
        assert app.sidebar_rail_buttons and app.sidebar_rail_buttons[0].winfo_exists()
        app.toggle_sidebar_narrow()
        ruhe(0.2)
        assert app.sidebar_shell.winfo_ismapped() and not app.sidebar_rail.winfo_ismapped()
        pruefungen.append("OB05: schmale Seitenleiste mit Systemsymbolen und Angeheftetem, Hinweis mit Titel, "
                          "öffnet Ansichten, Tastaturbindungen, gemerkt, Kopf ruhig, Wechsel zurück")

        # --- W05: Dialoge nach Mindestbreite, Knopfreihe rechts -----------------
        app.set_active_list(liste["id"])
        ruhe(0.1)
        gemessen = {}

        def dialog_messen(name):
            def run_modal(dialog, *a, **k):
                for _ in range(25):
                    dialog.update()
                knoepfe = [w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)]
                rechts = max(w.winfo_rootx() + w.winfo_width() for w in knoepfe) - dialog.winfo_rootx()
                gemessen[name] = (dialog.winfo_width(), rechts)
                dialog.destroy()
            return run_modal
        with patch.object(app, "run_modal", side_effect=dialog_messen("spalten")):
            app.show_table_columns_dialog()
        with patch.object(app, "run_modal", side_effect=dialog_messen("ki")):
            app.show_exchange_export_dialog()
        ruhe(0.1)
        for name, (breite, rechts) in gemessen.items():
            assert breite <= 760, (name, breite)  # 3.33.20: 1251 bzw. 1504 px
            assert breite - rechts <= 40, (name, breite, rechts)  # Knöpfe rechts
        pruefungen.append("W05: „Tabellenspalten“ und „Für KI bereitstellen“ nach Mindestbreite "
                          f"({', '.join(str(b) for b, _r in gemessen.values())} px), Knopfreihe rechts")

        ruhe(0.2)
        assert not fehler, fehler
        print("test_oberflaeche33321: OK; " + "; ".join(pruefungen))
    finally:
        try:
            app.cancel_pending_callbacks()
            app.release_data_lock()
        except Exception:
            pass
        try:
            root.destroy()
        except mod.tk.TclError:
            pass
