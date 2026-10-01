"""Breitenprüfung: jede Ansicht, jedes Design, jede Menüaktion, jede Kachel.

Punkt 1 (5. Prüfung, 3.25.0): „Die Dauer ist mir egal, ich möchte, dass alles
getestet wird." Die übrigen Suiten prüfen in die Tiefe – eine Funktion, ihre
Randfälle, ihre Daten. Diese hier prüft in die Breite: Sie baut jede Ansicht in
jedem Design auf, öffnet jeden Dialog, den die Menüzeile anbietet, zeichnet
jede Startseitenkachel einzeln und ruft jede Pinnwandaktion auf.

Das findet eine andere Art Fehler als eine Tiefenprüfung: den Aufruf einer
Methode, die es in dieser Klasse nicht gibt, einen Themeschlüssel, den ein
Design nicht kennt, ein Fenster, das ohne Inhalt aufgeht. Tk verschluckt so
etwas im Callback – sichtbar ist nur, dass nichts passiert. Deshalb sammelt
jeder Abschnitt `report_callback_exception` mit und prüft am Ende, dass die
Liste leer ist.

Dialoge werden gebaut und sofort geschlossen: Der Aufbau ist die Stelle, an der
solche Fehler entstehen. Datei- und Ordnerauswahl liefern nichts zurück, damit
kein Prüflauf ins Dateisystem greift.
"""
import importlib.machinery
import importlib.util
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix="glide-voll325-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_voll325", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    # Kein Prüflauf greift ins Dateisystem des Benutzers.
    mod.filedialog.askopenfilename = lambda *a, **k: ""
    mod.filedialog.askopenfilenames = lambda *a, **k: ()
    mod.filedialog.asksaveasfilename = lambda *a, **k: ""
    mod.filedialog.askdirectory = lambda *a, **k: ""

    geoeffnet = []

    def sofort_schliessen(self, dialog, parent=None):
        """Baut den Dialog fertig auf und schließt ihn sofort wieder."""
        geoeffnet.append(dialog)
        try:
            dialog.update_idletasks()
        except mod.tk.TclError:
            pass
        try:
            if dialog.winfo_exists():
                dialog.destroy()
        except mod.tk.TclError:
            pass

    mod.ListApp.run_modal = sofort_schliessen
    # Native Windows-Kontextmenüs warten synchron auf eine Benutzerwahl.
    # Menüaufbau und Befehle werden unten separat geprüft.
    mod.tk.Menu.tk_popup = lambda self, *args, **kwargs: None

    root = mod.tk.Tk()
    root.withdraw()
    root.geometry("1500x1000+0+0")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    meldungen = []
    app.show_warning = app.show_error = lambda *args, **kwargs: meldungen.append(args)
    app.show_info = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: False
    app.ask_yes_no_cancel = lambda *args, **kwargs: None
    app.themed_input_dialog = lambda *args, **kwargs: None
    app.themed_choice_dialog = lambda *args, **kwargs: None
    # Kein Prüflauf startet ein fremdes Programm.
    geoeffnete_pfade = []
    app.open_external_path = lambda pfad: geoeffnete_pfade.append(pfad)
    heute = date.today()

    try:
        # --- Prüfbestand: jede Art, jede Lage --------------------------
        ordner = app.new_folder_object("Prüfordner")
        app.folders.append(ordner)
        liste = app.new_list_object("Prüfliste", [], folder_id=ordner["id"])
        app.lists.append(liste)
        unterpunkt = app.new_item("Unterpunkt")
        gruppe = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP, children=[unterpunkt])
        punkte = [
            app.new_item("Überfällig", due=(heute - timedelta(days=3)).isoformat(), importance=3),
            app.new_item("Heute fällig", due=heute.isoformat(), importance=2),
            app.new_item("Später fällig", due=(heute + timedelta(days=9)).isoformat()),
            app.new_item("Erledigt", done=True),
            app.new_item("Mit Beschreibung", description="Eine Beschreibung."),
            app.new_item("Long-Task", kind=app.ITEM_KIND_LONG),
            app.new_item("Überschrift", kind=app.ITEM_KIND_HEADING),
            gruppe,
        ]
        liste["items"].extend(punkte)
        punkte[1]["planned_date"] = heute.isoformat()
        punkte[1]["estimated_minutes"] = 45
        punkte[2]["checklist"] = app.normalize_checklist([{"text": "Schritt", "done": False}])
        etikett = app.new_label_object("Prüflabel", None, "accent")
        app.labels.append(etikett)
        punkte[0]["labels"] = [etikett["id"]]
        app.set_active_list(liste["id"])
        app.save_items()
        app.workspace.pin([punkte[0]["id"], punkte[1]["id"]])
        app.workspace.toggle_connection(punkte[0]["id"], punkte[1]["id"])

        # ================================================================
        # 1. Jede Ansicht in jedem Design und in drei Breiten
        # ================================================================
        ansichten = [
            ("Startseite", app.set_home_view),
            ("Mein Tag", app.set_today_view),
            ("In Bearbeitung", app.set_in_progress_view),
            ("Verspätet", app.set_overdue_view),
            ("Labels", app.set_labels_view),
            ("Listen und Ordner", app.set_library_view),
            ("Vorlagen", app.set_template_view),
            ("Papierkorb", app.set_trash_view),
            ("Globale Pinnwand", app.open_global_board),
            ("Liste", lambda: app.set_active_list(liste["id"])),
            ("Tabelle", app.set_table_view),
            ("Ordner", lambda: app.set_active_folder(ordner["id"])),
        ]
        aufbauten = 0
        for design in app.DESIGN_ORDER:
            app.set_design(design)
            app.apply_theme()
            for breite in (860, 1180, 1500):
                root.geometry(f"{breite}x1000+0+0")
                for name, oeffnen in ansichten:
                    oeffnen()
                    root.update()
                    aufbauten += 1
                    assert not fehler, (design, breite, name, fehler[:1])
                    # Das Design sitzt tatsächlich auf der Fläche.
                    assert app.home_canvas.cget("bg") == app.theme["bg"], (design, name)
        assert aufbauten == len(app.DESIGN_ORDER) * 3 * len(ansichten)

        # ================================================================
        # 2. Jeder Anzeigeumfang in jeder Ansicht mit Punkten
        # ================================================================
        root.geometry("1500x1000+0+0")
        app.set_design("dark")
        app.apply_theme()
        for schluessel, _name, _hinweis in app.LIST_DETAIL_MODES:
            app.set_list_detail_mode(schluessel)
            for _name, oeffnen in ansichten:
                oeffnen()
                root.update()
                assert not fehler, (schluessel, fehler[:1])
        app.set_list_detail_mode(app.LIST_DETAIL_DEFAULT)

        # ================================================================
        # 3. Jede Startseitenkachel einzeln in beiden Grundrichtungen
        # ================================================================
        for design in ("light", "dark", "minimal_light", "minimal_dark", "dopamine"):
            app.set_design(design)
            app.apply_theme()
            for kachel in app.HOME_TILE_KEYS:
                app.settings["home_tile_order"] = [kachel]
                app.settings["home_tiles_hidden"] = [k for k in app.HOME_TILE_KEYS if k != kachel]
                app.set_home_view()
                app.refresh_home()
                root.update()
                assert not fehler, (design, kachel, fehler[:1])
                assert app.home_content.winfo_children(), (design, kachel)
        app.settings["home_tile_order"] = []
        app.settings["home_tiles_hidden"] = []
        app.set_design("dark")
        app.apply_theme()

        # ================================================================
        # 4. Jede Menüaktion, die kein Fenster verlässt
        # ================================================================
        # Was den Prüflauf beenden oder den Bestand unwiederbringlich ändern
        # würde, bleibt außen vor; alles andere wird aufgerufen.
        AUSGENOMMEN = {"Beenden", "Papierkorb leeren", "Aktive Liste löschen"}
        aktionen = app.app_action_entries()
        assert len(aktionen) >= 70, len(aktionen)
        app.set_active_list(liste["id"])
        root.update()
        for eintrag in aktionen:
            if eintrag["label"] in AUSGENOMMEN:
                continue
            meldungen.clear()
            eintrag["menu"].invoke(eintrag["index"])
            root.update()
            assert not fehler, (eintrag["path"], eintrag["label"], fehler[:1])
            # Nach jeder Aktion bleibt die Anwendung bedienbar.
            assert app.view_mode in (
                app.DERIVED_ITEM_VIEWS + ("list", "folder", "trash", app.HOME_VIEW,
                                          app.TEMPLATE_VIEW, app.LIBRARY_VIEW, app.HISTORY_VIEW,
                                          app.TABLE_VIEW, app.GLOBAL_BOARD_VIEW)), eintrag["label"]
            app.set_active_list(liste["id"])
            root.update()
        assert geoeffnet, "Kein einziger Dialog wurde aufgebaut."
        # Wege nach außen führen über eine Stelle und wurden aufgerufen.
        assert geoeffnete_pfade, "Keine Aktion hat einen Pfad nach außen gereicht."

        # ================================================================
        # 5. Jede Pinnwandaktion und jedes Pinnwandmenü
        # ================================================================
        app.set_active_list(liste["id"])
        flaeche = app.workspace
        flaeche.set_mode("board")
        root.update()
        flaeche.select_card(punkte[0]["id"])
        for gruppe_name in flaeche.BOARD_ACTION_GROUPS:
            for beschriftung, befehl in flaeche.board_action_groups()[gruppe_name]:
                if "entfernen" in beschriftung or "Drucken" in beschriftung:
                    continue
                befehl()
                root.update()
                assert not fehler, (beschriftung, fehler[:1])
                flaeche.set_mode("board")
                flaeche.select_card(punkte[0]["id"])
                root.update()
        for art in flaeche.CONNECTION_STYLE_KEYS:
            flaeche.configure_board("connection_style", art)
            root.update()
            assert not fehler, (art, fehler[:1])
        for stufe, _name, _faktor in flaeche.CARD_SCALES:
            flaeche.set_card_scale(stufe)
            root.update()
            assert not fehler, (stufe, fehler[:1])
        for anordnung in ("free", "columns"):
            flaeche.configure_board("layout", anordnung)
            root.update()
            assert not fehler, (anordnung, fehler[:1])
        flaeche.set_mode("list")

        # ================================================================
        # 6. Jede Rückmeldungsstufe in jedem Design
        # ================================================================
        for design in app.DESIGN_ORDER:
            app.set_design(design)
            app.apply_theme()
            for stufe in app.ACTION_FEEDBACK_KEYS:
                app.settings["action_feedback"] = stufe
                for schluessel in app.ACTION_FEEDBACK_TEXTS:
                    app.feedback(schluessel, 2)
                app.play_celebration("Prüfung")
                root.update()
                assert not fehler, (design, stufe, fehler[:1])
        app.settings["action_feedback"] = app.ACTION_FEEDBACK_DEFAULT
        app.set_design("dark")
        app.apply_theme()

        # ================================================================
        # 7. Jeder Abschnittszustand der Übersichten
        # ================================================================
        for kennung in app.OVERVIEW_SECTION_ROW_IDS:
            for offen in (False, True):
                app.set_overview_section_open(kennung, offen)
                app.set_in_progress_view()
                app.set_today_view()
                root.update()
                assert not fehler, (kennung, offen, fehler[:1])

        # ================================================================
        # 8. Jeder Zustand des Begleiters und jede Handbuchsuche
        # ================================================================
        figur = mod.MascotCanvas(root, app, size=100)
        for zustand in mod.MascotCanvas.STATES:
            for design in ("light", "dark", "minimal_light", "dopamine"):
                app.set_design(design)
                app.apply_theme()
                figur.set_state(zustand)
                figur.react(zustand)
                root.update()
                assert figur.find_all(), (zustand, design)
                assert not fehler, (zustand, design, fehler[:1])
        figur.destroy()
        for begriff in ("", "pinnwand", "label", "backup", "design", "gibtesnicht"):
            app.manual_entries(begriff)
        app.set_design("dark")
        app.apply_theme()
        root.update()

        assert not fehler, fehler
        print(f"OK Vollprüfung 3.25: {len(app.DESIGN_ORDER)} Designs × 3 Breiten × "
              f"{len(ansichten)} Ansichten, {len(app.LIST_DETAIL_MODES)} Anzeigeumfänge, "
              f"{len(app.HOME_TILE_KEYS)} Kacheln, {len(aktionen)} Menüaktionen, "
              f"{len(geoeffnet)} Dialoge, alle Pinnwandaktionen und Rückmeldungsstufen")
    finally:
        try:
            root.destroy()
        except Exception:
            pass
