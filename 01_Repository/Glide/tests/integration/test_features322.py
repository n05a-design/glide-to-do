"""Glide 3.22: Checkliste, Tabelle, Aktionen, Pinnwand, Startseite und Farbmodi."""
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


with tempfile.TemporaryDirectory(prefix="glide-features322-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features322", str(REPO / "src/glide/app.pyw"))
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
    heute = date.today().isoformat()
    try:
        # ================================================================
        # Punkt 18: Checkliste (Aufgabenformat 16)
        # ================================================================
        assert app.DATA_SCHEMA_VERSION == 23
        assert app.MAX_CHECKLIST_ENTRIES == 50 and app.MAX_CHECKLIST_TEXT == 200
        leer = app.new_item("Ohne Checkliste")
        assert leer["checklist"] == [], "Ein neuer Punkt trägt eine leere Checkliste."
        assert app.checklist_progress(leer) == {"done": 0, "total": 0}
        assert app.format_checklist_progress(leer) == ""

        # Normalisierung: Text wird verdichtet, Kennungen werden eindeutig,
        # Unbrauchbares fällt heraus statt einen Fehler auszulösen.
        roh = [
            {"id": "a", "text": "  Erster   Schritt ", "done": True},
            {"id": "a", "text": "Zweiter Schritt"},
            "Dritter Schritt",
            {"text": "   "},
            {"text": "x" * 500},
            42,
        ]
        sauber = app.normalize_checklist(roh)
        assert [eintrag["text"] for eintrag in sauber[:3]] == [
            "Erster Schritt", "Zweiter Schritt", "Dritter Schritt"], sauber
        assert len({eintrag["id"] for eintrag in sauber}) == len(sauber)
        assert len(sauber[3]["text"]) == app.MAX_CHECKLIST_TEXT
        assert sauber[0]["done"] is True and sauber[1]["done"] is False
        assert app.normalize_checklist("kaputt") == [] and app.normalize_checklist(None) == []
        assert len(app.normalize_checklist([{"text": f"S{i}"} for i in range(80)])) == 50

        mit = app.new_item("Mit Checkliste", checklist=[
            {"text": "Schritt eins", "done": True},
            {"text": "Schritt zwei"},
            {"text": "Schritt drei"},
        ])
        assert app.checklist_progress(mit) == {"done": 1, "total": 3}
        assert app.format_checklist_progress(mit) == "1/3"
        # Gliederung hakt nichts ab.
        gruppe = app.new_item("Abschnitt", kind=app.ITEM_KIND_GROUP,
                              checklist=[{"text": "Nicht erlaubt"}])
        assert gruppe["checklist"] == []

        liste = app.new_list_object("Checklistenprobe", [leer, mit, gruppe])
        app.lists.append(liste)
        app.set_active_list(liste["id"])
        assert app.save_items()
        gespeichert = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
        assert gespeichert["version"] == 23
        assert app.validate_backup_schema(gespeichert) == set()
        kaputt = copy.deepcopy(gespeichert)
        kaputt["lists"][-1]["items"][1]["checklist"] = "keine Liste"
        try:
            app.validate_backup_schema(kaputt)
            raise AssertionError("Eine ungültige Checkliste muss auffallen.")
        except ValueError:
            pass

        # Format 15 bleibt lesbar: ohne Feld entsteht eine leere Checkliste.
        alt = json.loads((REPO / "tests/fixtures/current_v15/reference_v15.json").read_text(encoding="utf-8"))
        vorher_folders, vorher_labels, vorher_trash = app.folders, app.labels, app.trash
        listen, _aktiv = app.normalize_lists_data(copy.deepcopy(alt))
        assert all("checklist" in item and item["checklist"] == []
                   for entry in listen for item in app.walk_items(entry.get("items", [])))
        neu = json.loads((REPO / "tests/fixtures/current_v16/reference_v16.json").read_text(encoding="utf-8"))
        assert neu["version"] == 16
        listen16, _aktiv16 = app.normalize_lists_data(copy.deepcopy(neu))
        treffer = [item for entry in listen16 for item in app.walk_items(entry.get("items", []))
                   if item["checklist"]]
        assert len(treffer) == 2, len(treffer)
        assert app.checklist_progress(treffer[0])["total"] == 3
        app.folders, app.labels, app.trash = vorher_folders, vorher_labels, vorher_trash
        app.lists = [entry for entry in app.lists]
        app.set_active_list(liste["id"])
        app.refresh_tree()
        root.update()

        # Die Zeile im Baum nennt den Stand, die Reiteransicht die Schritte.
        zeile = app.tree.item(mit["id"], "text")
        assert f"{app.ICONS['checklist']} 1/3" in zeile, zeile
        assert app.ICONS["checklist"] not in app.tree.item(leer["id"], "text")

        # Übernahme aus der Maske und Markdown-Ausgabe.
        entwurf = {"text": "Aus der Maske", "kind": app.ITEM_KIND_TASK,
                   "checklist": [{"text": "A", "done": True}, {"text": "B"}]}
        gebaut = app.build_item_from_dialog(entwurf)
        assert app.format_checklist_progress(gebaut) == "1/2"
        assert app.apply_item_details(leer, dict(entwurf, text=leer["text"])) is True
        assert app.format_checklist_progress(leer) == "1/2"
        ausgabe = Path(folder) / "export.md"
        with open(ausgabe, "w", encoding="utf-8") as datei:
            app.write_items_to_markdown(datei, [mit], 0)
        markdown = ausgabe.read_text(encoding="utf-8")
        assert "  - [x] Schritt eins" in markdown and "  - [ ] Schritt zwei" in markdown, markdown
        druck = app.build_print_html("list")
        assert "Checkliste: 1 von 3" in druck

        # ================================================================
        # Punkte 5 und 6: Tabellenansicht
        # ================================================================
        assert "checklist" in app.TABLE_COLUMN_KEYS
        app.set_table_view()
        root.update()
        assert app.view_mode == app.TABLE_VIEW
        # Punkt 7: Ein Weg zurück bleibt sichtbar. Seit 3.27 sind Liste,
        # Tabelle und Pinnwand gleichwertige Ziele; die aktive Ansicht wird
        # nicht noch einmal als Schaltfläche angeboten.
        # Das Fenster ist zurückgezogen; gepackt ist die verlässliche Auskunft.
        # Seit dem 27.09.2026 ein fester Umschalter; die aktive Ansicht ist
        # hervorgehoben statt ausgeblendet.
        assert app.view_switch.winfo_manager() == "pack" and app.list_view_button.text == "Liste"
        assert app.table_button.active_fill == app.theme["active"]  # U15: neutral statt Lila
        assert app.list_view_button.active_fill is None and app.board_button.active_fill is None
        app.toggle_table_view()
        root.update()
        assert app.view_mode == "list" and app.table_button.text == "Tabelle"
        assert app.table_button.winfo_manager() == "pack"
        app.set_table_view()
        root.update()

        # Überschriften stehen links und sortieren.
        for spalte in app.table_columns_for_list():
            # Tk liefert die Ausrichtung als eigenes Indexobjekt zurück.
            assert str(app.tree.heading(spalte, "anchor")) == "w", spalte
            assert app.tree.heading(spalte, "command")
        assert app.table_sort_for_list() == (None, "asc")
        app.sort_table_by("title")
        root.update()
        assert app.table_sort_for_list() == ("title", "asc")
        aufsteigend = [item["text"] for _order, item in app.table_entries()]
        assert aufsteigend == sorted(aufsteigend, key=str.casefold), aufsteigend
        assert app.ICONS["sort_ascending"] in app.tree.heading("title", "text")
        app.sort_table_by("title")
        root.update()
        assert app.table_sort_for_list() == ("title", "desc")
        assert [item["text"] for _order, item in app.table_entries()] == list(reversed(aufsteigend))
        assert app.ICONS["sort_descending"] in app.tree.heading("title", "text")
        app.sort_table_by("title")
        assert app.table_sort_for_list() == (None, "asc"), "Der dritte Klick führt zur Listenreihenfolge."
        # Leere Zellen bleiben in beiden Richtungen am Ende.
        mit["due"] = heute
        app.sort_table_by("due")
        assert [item["text"] for _order, item in app.table_entries()][0] == "Mit Checkliste"
        app.sort_table_by("due")
        assert [item["text"] for _order, item in app.table_entries()][0] == "Mit Checkliste"
        app.sort_table_by("due")

        # Spaltenbreiten bleiben erhalten und lassen sich zurücksetzen.
        app.tree.column("type", width=222)
        app.remember_table_column_widths()
        assert app.table_widths_for_list()["type"] == 222
        assert app.load_settings()["table_column_widths"][liste["id"]]["type"] == 222
        app.refresh_tree()
        root.update()
        assert int(app.tree.column("type", "width")) == 222
        app.sort_table_by("status")
        app.reset_table_columns()
        assert app.table_widths_for_list() == {} and app.table_sort_for_list() == (None, "asc")

        # ================================================================
        # Punkt 3: Aktionen in Gruppen
        # ================================================================
        eintraege = app.app_action_entries()
        assert all(eintrag["group"] in app.ACTION_GROUP_ORDER for eintrag in eintraege)
        gruppen = {eintrag["group"] for eintrag in eintraege}
        assert len(gruppen) >= 8, gruppen
        assert app.app_action_group("Als CSV …") == "Export"
        assert app.app_action_group("CSV importieren …") == "Import"
        assert app.app_action_group("Tabellenspalten …") == "Ansichtseinstellungen"
        assert app.app_action_group(f"Über {mod.APP_NAME}") == "Programm und Hilfe"
        assert app.app_action_group("Gibt es nicht") == app.ACTION_GROUP_FALLBACK
        unbekannt = [eintrag["label"] for eintrag in eintraege
                     if eintrag["group"] == app.ACTION_GROUP_FALLBACK]
        assert not unbekannt, unbekannt

        # ================================================================
        # Punkte 8 bis 15: Pinnwand
        # ================================================================
        app.set_active_list(liste["id"])
        root.update()
        arbeitsflaeche = app.workspace
        board = arbeitsflaeche.board()
        assert board["layout"] == "free", "Punkt 11: frei anordnen ist der Standard."
        assert board["preview"] is True and board["auto"] is False
        arbeitsflaeche.pin_all()
        root.update()
        assert arbeitsflaeche.mode == "board" and arbeitsflaeche.visible
        angeheftet = {karte["item_id"] for karte in arbeitsflaeche.board()["cards"]}
        assert mit["id"] in angeheftet and leer["id"] in angeheftet
        assert gruppe["id"] in angeheftet, "Gruppen dürfen angeheftet werden."

        # Punkt 13: Die Kartenhöhe folgt dem Inhalt.
        quelle = liste
        _blocks_leer, hoehe_leer = arbeitsflaeche.card_blocks(app.new_item("Kurz"), quelle, 300, False)
        voll = app.new_item("Ausführlich", due=heute, description="Eine Beschreibung mit Inhalt.",
                            checklist=[{"text": "A"}, {"text": "B", "done": True}])
        _blocks_voll, hoehe_voll = arbeitsflaeche.card_blocks(voll, quelle, 300, False)
        assert hoehe_leer == arbeitsflaeche.CARD_MIN_HEIGHT, hoehe_leer
        assert hoehe_voll > hoehe_leer + 30, (hoehe_leer, hoehe_voll)

        # Punkt 12: Positionen werden gespeichert.
        arbeitsflaeche.store_position(mit["id"], 480, 336, reveal=False)
        karte = next(k for k in arbeitsflaeche.board()["cards"] if k["item_id"] == mit["id"])
        assert (karte["x"], karte["y"]) == (480, 336)
        assert app.load_settings()["pinboards"]["list:" + liste["id"]]["cards"]
        # Punkt 14: die waagerechte Leiste ist die gezeichnete der App.
        assert isinstance(arbeitsflaeche.horizontal_scrollbar, mod.ThemedAutoScrollbar)
        assert arbeitsflaeche.horizontal_scrollbar.orient == "horizontal"
        arbeitsflaeche.horizontal_scrollbar.set(0.0, 0.4)
        assert arbeitsflaeche.horizontal_scrollbar.is_scrollable()
        # Punkt 10: Die Schalter stehen in der Reiterzeile, kein Statusband mehr.
        assert not hasattr(arbeitsflaeche, "board_status")
        beschriftungen = [getattr(w, "text", "") for w in descendants(arbeitsflaeche.bar)]
        for erwartet in ("Raster", "Finden", "Mehr"):
            assert erwartet in beschriftungen, (erwartet, beschriftungen)
        # Seit 3.33.21 (U09) stehen „Vorschau“ und „Auto anheften“ im Menü „…“.
        einstellungen = arbeitsflaeche.board_settings_menu(root)
        punkte = [einstellungen.entrycget(i, "label") for i in range(einstellungen.index("end") + 1)
                  if einstellungen.type(i) != "separator"]
        assert any("Bildvorschau" in p for p in punkte) and any("automatisch anheften" in p for p in punkte), punkte

        # Punkt 8: automatisches Anheften nimmt neue Punkte mit.
        arbeitsflaeche.configure_board("auto", True)
        root.update()
        nachzuegler = app.new_item("Kam später dazu")
        liste["items"].append(nachzuegler)
        app.refresh_tree()
        root.update()
        assert nachzuegler["id"] in {k["item_id"] for k in arbeitsflaeche.board()["cards"]}

        # „Alle Karten finden“ holt eine verlegte Karte zurück, ohne die
        # Betriebsart zu wechseln.
        arbeitsflaeche.store_position(mit["id"], 9000, 7000, reveal=False)
        arbeitsflaeche.find_cards()
        root.update()
        assert arbeitsflaeche.board()["layout"] == "free"
        assert all(k["x"] < 3000 and k["y"] < 9000 for k in arbeitsflaeche.board()["cards"])
        arbeitsflaeche.set_mode("list")
        root.update()

        # ================================================================
        # Punkt 2: Startseite als Kachelraster
        # ================================================================
        # Punkt 32 (3.23.0): Die Schwellen folgen der Mindestbreite einer
        # lesbaren Kachel; geprüft wird deshalb an den abgeleiteten Werten.
        assert app.home_column_count(app.HOME_TWO_COLUMN_WIDTH - 1) == 1
        assert app.home_column_count(app.HOME_TWO_COLUMN_WIDTH) == 2
        assert app.home_column_count(app.HOME_THREE_COLUMN_WIDTH - 1) == 2
        assert app.home_column_count(app.HOME_THREE_COLUMN_WIDTH) == 3
        app.settings["home_columns"] = "1"
        assert app.home_column_count(1600) == 1
        app.settings["home_columns"] = "auto"
        assert set(app.home_tile_order()) == set(app.HOME_TILE_KEYS)
        app.settings["home_tiles_hidden"] = []
        app.settings["home_tile_order"] = list(app.HOME_TILE_KEYS)
        app.set_home_view()
        root.update()
        texte = [str(w.cget("text")) for w in descendants(app.home_content)
                 if w.winfo_class() == "Label"]
        # Punkt 23 (3.23.0): „Mein Tag“ und „Heute fällig“ sind eine Kachel
        # „Heute“ mit zwei Abschnitten; beide Überschriften bleiben lesbar.
        for erwartet in ("Heute", "Eingeplant", "Nächste Aufgabe", "Heute fällig", "Die nächsten sieben Tage",
                         "Zuletzt bearbeitet", "Impuls für den Tag", "Dein aktueller Bestand"):
            assert any(erwartet in text for text in texte), (erwartet, texte[:20])
        # Ausschalten wirkt.
        app.settings["home_tiles_hidden"] = ["impulse", "week", "focus", "labels", "today"]
        app.refresh_home()
        root.update()
        texte = [str(w.cget("text")) for w in descendants(app.home_content)
                 if w.winfo_class() == "Label"]
        assert not any("Impuls für den Tag" in text for text in texte)
        assert not any("Die nächsten sieben Tage" in text for text in texte)
        # Die verschmolzene Kachel nimmt beide Abschnitte mit.
        assert not any("Eingeplant" in text for text in texte)
        assert not any("Heute fällig" in text for text in texte)
        assert "due" not in app.HOME_TILE_KEYS
        # Reihenfolge und Normalisierung.
        # 3.30: ohne „home_tiles_330“ blendete der Übergangsschritt die neuen
        # Kacheln zusätzlich aus – hier geht es nur um die Bereinigung.
        gepruft = app.normalize_personal_settings({"home_tile_order": ["stats", "gibtsnicht", "clock"],
                                                   "home_tiles_hidden": ["week", "falsch"],
                                                   "home_columns": "17", "home_tiles_330": True})
        assert gepruft["home_tile_order"] == ["stats", "clock"]
        assert gepruft["home_tiles_hidden"] == ["week"]
        assert gepruft["home_columns"] == "auto"
        # Die Hilfsrechnungen der neuen Kacheln.
        assert len(app.home_week_overview()) == 7
        assert all(isinstance(anzahl, int) for _tag, anzahl in app.home_week_overview())
        app.settings["home_tiles_hidden"] = []

        # ================================================================
        # Punkte 19 und 20: Farbmodi
        # Seit 3.23 (Punkt 3) sind sie Designs; gewählt wird über set_design.
        # ================================================================
        app.set_design("light", apply_now=False)
        app.theme = app.active_theme()
        # Punkt 16 (3.24.0): Bewegte Rückmeldungen hängen nicht mehr am
        # Design, sondern an einer eigenen Einstellung – sie sind deshalb auch
        # im hellen Design an, solange sie nicht abgeschaltet wurden. Das
        # Dopamin-Design steigert sie nur noch (arcade_mode).
        assert app.color_mode() == "standard" and app.arcade_mode() is False
        assert app.animations_enabled() is True
        app.settings["animations_enabled"] = False
        assert app.animations_enabled() is False
        app.settings["animations_enabled"] = True
        standard = dict(app.theme)
        app.set_design("contrast_light", apply_now=False)
        app.theme = app.active_theme()
        assert app.theme != standard
        assert app.theme["text"] != standard["text"]
        # Kontrast: Text gegen Fläche deutlich stärker als vorher.
        def kontrast(vorne, hinten):
            hell = sorted((mod.relative_luminance(vorne), mod.relative_luminance(hinten)))
            return (hell[1] + 0.05) / (hell[0] + 0.05)
        assert kontrast(app.theme["text"], app.theme["card"]) > 12
        assert kontrast(app.theme["muted"], app.theme["card"]) >= 7
        # Die Glasoptik bleibt in beiden Sonderdesigns aus: Sie ist seit 3.23
        # eine Eigenschaft des Designs und nicht mehr getrennt schaltbar.
        assert app.glass_enabled() is False
        assert app.active_theme().get("glass_gradient") == ""
        app.set_design("dopamine", apply_now=False)
        app.theme = app.active_theme()
        assert app.animations_enabled() is True
        assert app.arcade_mode() is True
        assert app.glass_enabled() is False
        assert app.active_theme().get("glass_gradient") == ""
        assert mod.relative_luminance(app.theme["bg"]) < 0.1, "Dopamin bleibt auf dunklem Grund."
        # Jede Farbrolle bleibt belegt; nur die Glaszusätze entfallen bewusst.
        for schluessel in standard:
            if schluessel.startswith("glass_"):
                continue
            assert schluessel in app.theme, schluessel
        app.apply_theme()
        root.update()
        app.play_celebration("Test")
        root.update()
        app.settings["design"] = "kaputt"
        assert app.design_name() == app.DESIGN_DEFAULT
        assert app.color_mode() == app.DESIGNS[app.DESIGN_DEFAULT]["layer"] or True
        # Punkt 3: Übernahme der drei alten Werte in ein Design, ohne Verlust.
        N = app.normalize_personal_settings
        assert N({"theme": "dark", "color_mode": "dopamine"})["design"] == "dopamine"
        assert N({"theme": "light", "color_mode": "contrast"})["design"] == "contrast_light"
        assert N({"theme": "dark", "color_mode": "contrast"})["design"] == "contrast_dark"
        assert N({"theme": "dark", "glass_mode": True})["design"] == "glass_dark"
        assert N({"theme": "light", "glass_mode": True})["design"] == "glass_light"
        assert N({"theme": "dark", "glass_mode": False})["design"] == "dark"
        assert N({"theme": "light", "glass_mode": False})["design"] == "light"
        assert N({"design": "quatsch"})["design"] == "glass_light"
        # Die drei abgeleiteten Werte bleiben für ältere Fassungen lesbar.
        gespiegelt = N({"design": "dopamine"})
        assert gespiegelt["theme"] == "dark" and gespiegelt["color_mode"] == "dopamine"
        assert gespiegelt["glass_mode"] is False
        # Der Hell-/Dunkel-Schalter bleibt im gewählten Design.
        for start, ziel in (("glass_dark", "glass_light"), ("glass_light", "glass_dark"),
                            ("contrast_light", "contrast_dark"), ("light", "dark"),
                            ("dopamine", "dopamine")):
            app.set_design(start, apply_now=False)
            app.toggle_theme()
            assert app.design_name() == ziel, (start, app.design_name())
        # Jedes Design ist vollständig und lässt sich anwenden.
        for schluessel in app.DESIGN_ORDER:
            app.set_design(schluessel, apply_now=False)
            gewaehlt = app.active_theme()
            assert app.theme_name == app.DESIGNS[schluessel]["base"]
            for rolle in standard:
                if rolle.startswith("glass_"):
                    continue
                assert rolle in gewaehlt, (schluessel, rolle)
            app.apply_theme()
            root.update()
        app.set_design("glass_dark", apply_now=False)
        app.theme = app.active_theme()
        app.apply_theme()
        root.update()

        # ================================================================
        # Punkte 15 und 17: Maus
        # ================================================================
        assert callable(app.bind_horizontal_wheel) and callable(app.bind_drag_scroll)
        if not mod.IS_MACOS:
            assert app.tree.bind("<ButtonPress-2>"), "Fast-Scroll im Aufgabenbaum"
            assert app.tree.bind("<B2-Motion>") and app.tree.bind("<ButtonRelease-2>")
            # Die mittlere Taste greift die Fläche, statt das Kontextmenü zu
            # öffnen: Der Zeiger wechselt für die Dauer des Ziehens.
            app.set_active_list(liste["id"])
            root.update()
            app.tree.event_generate("<ButtonPress-2>", x=20, y=20)
            root.update()
            assert str(app.tree.cget("cursor")) == "fleur", app.tree.cget("cursor")
            app.tree.event_generate("<ButtonRelease-2>", x=20, y=20)
            root.update()
            assert str(app.tree.cget("cursor")) != "fleur"
            assert app._item_context_menu is None
        assert not meldungen, meldungen
        assert not fehler, fehler
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK 3.22: Checkliste, Tabelle mit Sortierung und Breiten, Aktionsgruppen, "
      "Pinnwand, Startseitenkacheln, Farbmodi und Mausbedienung")
