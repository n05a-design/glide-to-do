"""Glide 3.24: Navigation, Pinnwand, Anzeige, Startansicht und Rückmeldungen.

Jeder Abschnitt trägt die Nummer des Auftragspunkts, den er nachweist.
"""
import copy
import importlib.machinery
import importlib.util
import json
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix="glide-features324-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features324", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    root.geometry("1500x1000+0+0")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    meldungen = []
    app.show_warning = app.show_error = lambda *args, **kwargs: meldungen.append(args)
    app.show_info = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: True
    heute = date.today()

    try:
        # ================================================================
        # Punkte 1 und 2: Eingang und Verspätet sind Abschnitte, keine Zeilen
        # ================================================================
        app.update_sidebar_list()
        root.update()
        eingang = app.ensure_inbox_list()
        zeilen = app.system_listbox.get_children("")
        assert zeilen == (app.HOME_ROW_ID, app.PLAN_DAY_ROW_ID,
                          app.LABELS_ROW_ID, app.TEMPLATE_ROW_ID, app.TRASH_ROW_ID), zeilen
        assert int(app.system_listbox.cget("height")) == len(zeilen)
        assert app.SYSTEM_NESTED_VIEWS == ()
        assert app.system_row_depth(("view", "overdue")) == 0
        assert app.system_row_depth(("list", eingang["id"])) == 0
        assert not app.sidebar_listbox.exists(f"list:{eingang['id']}")

        # Beide Ansichten bleiben benannt erreichbar – über Menü und Aktionen.
        for beschriftung in ("Verspätet", "Eingang öffnen", "Globale Pinnwand öffnen"):
            assert beschriftung in mod.ListApp.ACTION_GROUPS["Ansichten"], beschriftung
            assert app.app_action_group(beschriftung) == "Ansichten", beschriftung

        # Der Eingang ist weiterhin eine echte Liste mit einem eigenen Weg.
        assert app.open_inbox_list() == "break"
        assert app.view_mode == "list" and app.active_list_id == eingang["id"]

        # „Verspätet" steht als erster Abschnitt in „In Bearbeitung".
        fristen = app.new_list_object("Fristen 3.24", [])
        app.lists.append(fristen)
        vergangen = (heute - timedelta(days=4)).isoformat()
        kuenftig = (heute + timedelta(days=4)).isoformat()
        alt = app.new_item("Längst fällig", due=vergangen)
        # Punkt 5 (3.25.0): Der früheste überfällige Punkt wandert in den
        # Abschnitt „Nächste Aufgabe“. Damit „Verspätet“ überhaupt noch etwas
        # zu zeigen hat, braucht die Probe einen zweiten überfälligen Punkt.
        alt_zwei = app.new_item("Auch überfällig", due=(heute - timedelta(days=2)).isoformat())
        neu = app.new_item("Kommt noch", due=kuenftig)
        fristen["items"].extend([alt, alt_zwei, neu])
        app.save_items()
        app.set_in_progress_view()
        root.update()
        # Punkte 5 und 6 (3.25.0): Die Abschnitte sind seit 3.25 Elternzeilen
        # und tragen ihre Punkte als Kinder. Seit 3.33.6 (D14) steht die
        # nächste Aufgabe in „Heute“; „Demnächst“ beginnt mit „Verspätet“.
        alle = app.tree.get_children("")
        assert app.OVERDUE_SECTION_ROW_ID in alle
        assert app.NEXT_TASK_SECTION_ROW_ID not in alle
        assert alle.index(app.OVERDUE_SECTION_ROW_ID) == 0
        assert app.IN_PROGRESS_SECTION_ROW_ID in alle
        assert alle.index(app.OVERDUE_SECTION_ROW_ID) < alle.index(app.IN_PROGRESS_SECTION_ROW_ID)
        # Die Überschriften sind keine Punkte: Sie tragen keine Quellzuordnung.
        for abschnitt in app.OVERVIEW_SECTION_ROW_IDS:
            assert abschnitt not in app.in_progress_item_sources
        # Beide überfälligen Punkte stehen unter „Verspätet“; alles Übrige
        # hängt unter „Noch offen".
        ueberfaellig_zeile = next(row for row, quelle in app.in_progress_item_sources.items()
                                  if quelle[1] == alt["id"])
        kuenftig_zeile = next(row for row, quelle in app.in_progress_item_sources.items()
                              if quelle[1] == neu["id"])
        zweite_zeile = next(row for row, quelle in app.in_progress_item_sources.items()
                            if quelle[1] == alt_zwei["id"])
        assert app.tree.parent(ueberfaellig_zeile) == app.OVERDUE_SECTION_ROW_ID
        assert app.tree.parent(zweite_zeile) == app.OVERDUE_SECTION_ROW_ID
        assert app.tree.parent(kuenftig_zeile) == app.IN_PROGRESS_SECTION_ROW_ID
        # Ein Doppelklick auf die Überschrift führt in die eigene Ansicht.
        app.tree.focus(app.OVERDUE_SECTION_ROW_ID)
        assert app.open_in_progress_source_item() == "break"
        assert app.view_mode == "overdue"
        app.set_in_progress_view()
        # Ohne Überfälliges bleibt der Abschnitt „Verspätet" weg.
        alt["done"] = True
        alt_zwei["done"] = True
        app.refresh_tree()
        root.update()
        assert app.OVERDUE_SECTION_ROW_ID not in app.tree.get_children("")
        alt["done"] = False
        alt_zwei["done"] = False
        app.refresh_tree()

        # ================================================================
        # Punkt 3: Das Zahnrad steht auf der rechten Flucht
        # ================================================================
        app.sync_header_density(None)
        app._header_density = None
        app.sync_header_density(None)
        rand = app.settings_button.pack_info().get("padx")
        assert str(rand) in ("0", "(0, 0)", "0 0"), rand
        # Die Schaltflächen darunter enden auf derselben Flucht: kein rechter
        # Abstand an der jeweils äußersten.
        assert str(app.add_button.pack_info().get("padx")) in ("0", "(0, 0)", "0 0")
        # U03: Flucht am sichtbaren Löschkreuz prüfen, ohne eine leere Suche
        # dauerhaft mit einem wirkungslosen Knopf zu belegen.
        app.search_placeholder_active = False
        app.search_var.set("Aufgabe")
        app.sync_clear_search_visibility()
        assert str(app.clear_search_button.pack_info().get("padx")) in ("0", "(0, 0)", "0 0")
        app.clear_search()

        # ================================================================
        # Punkte 4, 9 und 10: Mehrfachauswahl, Verbindungsarten, Kartengröße
        # ================================================================
        k1, k2, k3 = (app.new_item(f"Karte {name}") for name in "ABC")
        tafel_liste = app.new_list_object("Pinnwand 3.24", [k1, k2, k3])
        app.lists.append(tafel_liste)
        app.set_active_list(tafel_liste["id"])
        flaeche = app.workspace
        flaeche.pin([k1["id"], k2["id"], k3["id"]])
        flaeche.set_mode("board")
        root.update()
        assert len(flaeche.card_boxes) == 3

        flaeche.select_card(k1["id"])
        assert flaeche.selection() == [k1["id"]]
        flaeche.select_card(k2["id"], additive=True)
        flaeche.select_card(k3["id"], additive=True)
        assert flaeche.selection() == [k1["id"], k2["id"], k3["id"]]
        # Dieselbe Karte noch einmal nimmt sie wieder heraus.
        flaeche.select_card(k3["id"], additive=True)
        assert flaeche.selection() == [k1["id"], k2["id"]]
        flaeche.select_card(k3["id"], additive=True)

        # Verbinden bei Mehrfachauswahl: die erste Karte ist der Ausgangspunkt.
        flaeche.start_connect_mode()
        verbindungen = flaeche.connections()
        assert len(verbindungen) == 2
        assert {(von, nach) for von, nach, _art in verbindungen} == {
            (k1["id"], k2["id"]), (k1["id"], k3["id"])}
        assert all(art == mod.ItemWorkspace.CONNECTION_STYLE_DEFAULT for _v, _n, art in verbindungen)
        # Ein zweiter Aufruf legt nichts doppelt an.
        flaeche.start_connect_mode()
        assert len(flaeche.connections()) == 2

        # Die Verbindungsart gilt für die nächste Verbindung und übersteht
        # Speichern und Normalisieren.
        flaeche.configure_board("connection_style", "forward")
        root.update()
        assert flaeche.connection_style() == "forward"
        flaeche.toggle_connection(k2["id"], k3["id"])
        gerichtet = [eintrag for eintrag in flaeche.connections()
                     if {eintrag[0], eintrag[1]} == {k2["id"], k3["id"]}]
        assert gerichtet and gerichtet[0] == (k2["id"], k3["id"], "forward")
        normalisiert = mod.ItemWorkspace.normalize_settings(copy.deepcopy(app.settings))
        gespeicherte = normalisiert["pinboards"][flaeche.context()]["connections"]
        assert any(eintrag["style"] == "forward" for eintrag in gespeicherte)
        assert all(eintrag["style"] in mod.ItemWorkspace.CONNECTION_STYLE_KEYS
                   for eintrag in gespeicherte)
        # Eine unbekannte Art fällt auf die Linie zurück, die Verbindung bleibt.
        verbogen = copy.deepcopy(app.settings)
        verbogen["pinboards"][flaeche.context()]["connections"][0]["style"] = "regenbogen"
        assert mod.ItemWorkspace.normalize_settings(verbogen)["pinboards"][
            flaeche.context()]["connections"][0]["style"] == "line"
        # Gezeichnet wird mit Spitze; gedruckt ebenso.
        root.update()
        assert len(flaeche.canvas.find_withtag("connection")) == 3
        druck = flaeche.build_board_print_html()
        assert 'marker-end="url(#pfeil)"' in druck

        # Kartengröße: Maßstab an der Karte, nicht am Punkt.
        flaeche.select_card(k1["id"])
        flaeche.set_card_scale("large")
        root.update()
        karte = next(wert for wert in flaeche.board()["cards"] if wert["item_id"] == k1["id"])
        assert karte["scale"] == "large"
        assert flaeche.card_scale_factor(karte) == mod.ItemWorkspace.CARD_SCALE_FACTORS["large"]
        assert flaeche.card_boxes[k1["id"]][2] > flaeche.card_boxes[k2["id"]][2]
        ohne_angabe = mod.ItemWorkspace.normalize_settings(
            {"pinboards": {f"list:{tafel_liste['id']}": {"cards": [
                {"list_id": tafel_liste["id"], "item_id": k2["id"]}]}}})
        assert ohne_angabe["pinboards"][f"list:{tafel_liste['id']}"]["cards"][0]["scale"] == "normal"

        # ================================================================
        # Punkte 6, 7 und 8: Vollbild, Rückweg und portable Anordnung
        # ================================================================
        schalter = {getattr(knopf, "text", "") for knopf in flaeche.board_controls(flaeche.bar)}
        assert "Vollbild" in schalter and "Fläche" not in schalter
        reihenfolge_vorher = list(app.shell.pack_slaves())
        inhalt_vorher = list(app.content_frame.pack_slaves())
        flaeche.enter_board_focus()
        root.update()
        assert flaeche.board_focus_active() is True
        aktiv = [knopf for knopf in flaeche.board_controls(flaeche.bar)
                 if getattr(knopf, "text", "") == "Vollbild beenden"]
        # Seit 27.09.2026 sind eingeschaltete Schalter hervorgehoben, seit 3.33.21
        # (U15) mit der neutralen Rolle „active“ statt der Auswahlfarbe.
        assert aktiv and aktiv[0].active_fill == app.theme["active"]
        flaeche.exit_board_focus()
        root.update()
        assert flaeche.board_focus_active() is False
        # Punkt 7: Kopfzeile und Eingabezeile stehen wieder an ihrer Stelle.
        assert list(app.shell.pack_slaves()) == reihenfolge_vorher
        assert list(app.content_frame.pack_slaves()) == inhalt_vorher

        # Punkt 8: Anordnung und Verbindungen reisen im Komplettbackup mit.
        nutzlast = app.complete_backup_payload()
        assert flaeche.context() in nutzlast["pinboards"]
        assert nutzlast["pinboards"][flaeche.context()]["connections"]
        # Ein vollständiger Import übernimmt sie unverändert.
        zurueck = app.pinboards_from_backup(nutzlast)
        assert zurueck[flaeche.context()]["cards"]
        # Beim Hinzufügen wandern sie auf die neuen Kennungen.
        container_map = {tafel_liste["id"]: "neue-liste"}
        item_map = {k1["id"]: "neu-1", k2["id"]: "neu-2", k3["id"]: "neu-3"}
        umgezogen = app.pinboards_from_backup(nutzlast, container_map, item_map)
        assert "list:neue-liste" in umgezogen
        assert {karte["item_id"] for karte in umgezogen["list:neue-liste"]["cards"]} == set(item_map.values())
        assert all(eintrag["from"] in item_map.values() and eintrag["to"] in item_map.values()
                   for eintrag in umgezogen["list:neue-liste"]["connections"])
        # Eine Liste, die nicht mitkommt, hinterlässt keine verwaiste Pinnwand.
        assert app.pinboards_from_backup(nutzlast, {}, item_map) == {}

        # ================================================================
        # Punkt 5: Der neue Punkt entsteht in der vollständigen Maske
        # ================================================================
        aufrufe = []

        def maske(*args, **kwargs):
            aufrufe.append(kwargs)
            return {"text": "Auf der Fläche", "kind": app.ITEM_KIND_TASK, "importance": 0,
                    "color": None, "due": None, "due_time": None, "planned_date": None,
                    "estimated_minutes": None, "repeat": None, "reminder": None,
                    "labels": [], "description": "Mit Beschreibung", "checklist": [],
                    "attachments": [], "list_id": kwargs.get("default_list_id")}

        app.new_item_dialog = maske
        vorher = app.count_items(tafel_liste["items"])
        flaeche.create_card_item(300, 200)
        root.update()
        assert app.count_items(tafel_liste["items"]) == vorher + 1
        angelegt = next(wert for wert in tafel_liste["items"] if wert.get("text") == "Auf der Fläche")
        assert angelegt["description"] == "Mit Beschreibung"
        assert aufrufe and aufrufe[0]["allow_list_choice"] is False

        # ================================================================
        # Punkt 12: Die globale Pinnwand
        # ================================================================
        assert app.open_global_board() == "break"
        root.update()
        assert app.view_mode == app.GLOBAL_BOARD_VIEW
        assert flaeche.context() == mod.ItemWorkspace.GLOBAL_SCOPE
        assert flaeche.mode == "board" and flaeche.visible is True
        assert app.get_display_title() == app.GLOBAL_BOARD_TITLE
        # Ihr Bereich ist der gesamte Bestand.
        assert {eintrag["id"] for eintrag in flaeche.eligible_lists()} == {
            eintrag["id"] for eintrag in app.lists}
        flaeche.pin([k1["id"], alt["id"]])
        root.update()
        assert set(flaeche.card_ids) == {k1["id"], alt["id"]}
        # Sie übersteht Normalisierung und Aufräumen.
        assert mod.ItemWorkspace.GLOBAL_SCOPE in mod.ItemWorkspace.normalize_settings(
            copy.deepcopy(app.settings))["pinboards"]
        flaeche.prune()
        assert mod.ItemWorkspace.GLOBAL_SCOPE in app.settings["pinboards"]
        # Auf ihr entsteht ein neuer Punkt mit Listenauswahl.
        aufrufe.clear()
        flaeche.create_card_item(60, 60)
        root.update()
        assert aufrufe and aufrufe[0]["allow_list_choice"] is True
        # Escape führt in die Übersicht statt in eine Liste, die es hier nicht gibt.
        flaeche.board_escape()
        root.update()
        assert app.view_mode == app.LIBRARY_VIEW
        app.set_active_list(tafel_liste["id"])

        # ================================================================
        # Punkt 11: Die Pinnwandaktionen sind gruppiert
        # ================================================================
        gruppen = flaeche.board_action_groups()
        assert list(gruppen) == list(mod.ItemWorkspace.BOARD_ACTION_GROUPS)
        beschriftungen = [text for name in gruppen for text, _befehl in gruppen[name]]
        assert len(beschriftungen) == len(set(beschriftungen)), beschriftungen
        assert all(callable(befehl) for name in gruppen for _text, befehl in gruppen[name])

        # ================================================================
        # Punkt 13: „Anzeige" ist eine Fläche im App-Stil
        # ================================================================
        app.set_active_list(tafel_liste["id"])
        flaeche.set_mode("list")
        root.update()
        assert app.show_detail_mode_menu() == "break"
        root.update()
        panel = getattr(app, "_active_dropdown", None)
        assert isinstance(panel, mod.DropdownPopup)
        namen = {str(kind.cget("text")) for kind in descendants(panel)
                 if "text" in kind.keys()}
        for _schluessel, name, hinweis in app.LIST_DETAIL_MODES:
            assert name in namen, name
            assert hinweis in namen, hinweis
        panel.close()
        root.update()
        assert getattr(app, "_active_dropdown", None) is None

        # ================================================================
        # Punkt 14: Die Ansicht beim Öffnen kennt mehr als drei Ziele
        # ================================================================
        assert set(app.STARTUP_VIEW_KEYS) >= {
            "last", "home", "planday", "in_progress", "library", "templates",
            "globalboard", "list"}
        for schluessel, name, hinweis in app.STARTUP_VIEW_CHOICES:
            assert name.strip() and hinweis.strip(), schluessel
        vorherige_ansicht = app.view_mode
        app.settings["startup_view"] = "in_progress"
        app.apply_startup_view()
        assert app.view_mode == "in_progress"
        app.settings["startup_view"] = "list"
        app.settings["startup_list_id"] = tafel_liste["id"]
        app.apply_startup_view()
        assert app.view_mode == "list" and app.active_list_id == tafel_liste["id"]
        # Eine Liste, die es nicht mehr gibt, führt auf die Startseite.
        app.settings["startup_list_id"] = "gibt-es-nicht"
        app.apply_startup_view()
        assert app.view_mode == app.HOME_VIEW
        app.settings["startup_view"] = "last"
        app.settings["startup_list_id"] = ""
        # Unbekannte Werte fallen auf „Letzte Ansicht" zurück.
        assert mod.ListApp.normalize_personal_settings(
            {"startup_view": "mondphase"})["startup_view"] == "last"

        # ================================================================
        # Punkt 20: Zweispaltige Masken bekommen die Breite zweier Spalten
        # ================================================================
        assert mod.ResponsiveColumns.MIN_COLUMN_WIDTH >= 360
        noetig = mod.ResponsiveColumns.required_width(chrome=2 * app.DIALOG_PAD_X + 40)
        probe = mod.ResponsiveColumns(root, bg=app.theme["bg"])
        assert probe.wide_enough(noetig - 2 * app.DIALOG_PAD_X - 40) is True
        assert probe.wide_enough(mod.ResponsiveColumns.MIN_COLUMN_WIDTH * 2) is False
        probe.destroy()

        # ================================================================
        # Punkte 16, 17 und 18: Rückmeldung in jedem Design, Arcade im Dopamin
        # ================================================================
        app.set_design("glass_dark", apply_now=False)
        app.theme = app.active_theme()
        assert app.animations_enabled() is True and app.arcade_mode() is False
        app.settings["animations_enabled"] = False
        assert app.animations_enabled() is False
        app.settings["animations_enabled"] = True
        assert mod.ListApp.normalize_personal_settings({})["animations_enabled"] is True
        assert mod.ListApp.normalize_personal_settings(
            {"animations_enabled": "ja"})["animations_enabled"] is True
        # Ohne Dopamin genau eine Fahne, mit Dopamin ein Stapel.
        def fahnen():
            # Seit 27.09.2026 steigt die Fahne im Arbeitsbereich vom unteren Rand auf.
            return [kind for kind in app.main_area.winfo_children()
                    if isinstance(kind, mod.tk.Label) and kind.winfo_manager() == "place"]

        app.play_celebration("Test")
        root.update()
        assert len(fahnen()) == 1
        for kind in fahnen():
            kind.destroy()
        app.set_design("dopamine", apply_now=False)
        app.theme = app.active_theme()
        assert app.arcade_mode() is True
        app.play_celebration("Test")
        for _schritt in range(mod.ListApp.CELEBRATION_STACK + 2):
            root.update()
            root.after(mod.ListApp.CELEBRATION_STACK_DELAY, root.quit)
            root.mainloop()
        assert len(fahnen()) > 1, len(fahnen())
        for kind in fahnen():
            kind.destroy()
        # Die Kombo zählt nur im Dopamin-Design und lebt in der Sitzung.
        assert app.register_completion_combo(1) == 1
        assert app.register_completion_combo(1) == 2
        app._combo_time = None
        assert app.register_completion_combo(1) == 1
        app.set_design("glass_dark", apply_now=False)
        app.theme = app.active_theme()
        assert app.register_completion_combo(1) == 0
        # Punkt 18: Die Dopamin-Farben bleiben lesbar.
        app.set_design("dopamine", apply_now=False)
        tafel = app.active_theme()

        def kontrast(vorne, hinten):
            hell = sorted((mod.relative_luminance(vorne), mod.relative_luminance(hinten)))
            return (hell[1] + 0.05) / (hell[0] + 0.05)

        for flaechenfarbe in ("bg", "card", "input"):
            assert kontrast(tafel["text"], tafel[flaechenfarbe]) >= 7, flaechenfarbe
            assert kontrast(tafel["muted"], tafel[flaechenfarbe]) >= 4.5, flaechenfarbe
        app.set_design("glass_dark", apply_now=True)
        root.update()

        # ================================================================
        # Punkt 19: Mehr Bausteine auf der Startseite
        # ================================================================
        for schluessel in ("calendar", "overdue", "progress", "boards"):
            assert schluessel in app.HOME_TILE_KEYS, schluessel
        assert app.home_calendar_mode() == app.HOME_CALENDAR_DEFAULT
        assert app.home_density() == app.HOME_DENSITY_DEFAULT
        assert app.home_row_limit() == app.HOME_DENSITY_ROWS[app.HOME_DENSITY_DEFAULT]
        assert mod.ListApp.normalize_personal_settings(
            {"home_calendar_mode": "mondphase"})["home_calendar_mode"] == app.HOME_CALENDAR_DEFAULT
        assert mod.ListApp.normalize_personal_settings(
            {"home_density": "riesig"})["home_density"] == app.HOME_DENSITY_DEFAULT
        # Die Vorschau liest Fälligkeit und Bearbeitungstag offener Punkte.
        tage = app.home_calendar_days()
        assert tage.get(kuenftig, 0) >= 1
        assert [eintrag[0] for eintrag in app.home_next_events()] == sorted(
            eintrag[0] for eintrag in app.home_next_events())
        eintraege, gesamt = app.home_overdue_entries()
        assert gesamt >= 1 and eintraege and eintraege[0][2].get("id")
        # Jede der drei Darstellungen baut die Kachel vollständig auf.
        # Die Einrichtung schreibt Reihenfolge und Auswahl gemeinsam; ohne
        # Reihenfolge gilt weiterhin die Vorgabe „neue Kacheln bleiben aus".
        app.settings["home_tile_order"] = list(app.HOME_TILE_KEYS)
        app.settings["home_tiles_hidden"] = [
            key for key in app.HOME_TILE_KEYS
            if key not in ("calendar", "overdue", "progress", "boards")]
        app.settings["daily_goal"] = 3
        for modus, _name in app.HOME_CALENDAR_CHOICES:
            app.settings["home_calendar_mode"] = modus
            app.set_home_view()
            root.update()
            assert not fehler, fehler
            beschriftungen = [str(kind.cget("text")) for kind in descendants(app.home_content)
                              if "text" in kind.keys()]
            assert any("Kalender" in text for text in beschriftungen), modus
            assert any("Verspätet" in text for text in beschriftungen), modus
            assert any("Fortschritt" in text for text in beschriftungen), modus
            assert any("Pinnwände" in text for text in beschriftungen), modus
        app.settings["home_tiles_hidden"] = []
        app.settings["home_tile_order"] = []
        app.settings["home_calendar_mode"] = app.HOME_CALENDAR_DEFAULT
        app.set_home_view()
        root.update()

        assert not fehler, fehler
        print("OK 3.24: Navigation, Pinnwand mit Mehrfachauswahl und Verbindungsarten, "
              "globale Fläche, Anzeigefläche, Startansicht, Dialogbreiten und Rückmeldungen")
    finally:
        try:
            root.destroy()
        except Exception:
            pass
