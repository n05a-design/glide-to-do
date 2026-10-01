"""Glide 3.23: Designsystem, Navigation, Tabellen, Dialoge, Pinnwand und Austauschformat.

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


def texte(widget):
    werte = []
    for kind in descendants(widget):
        try:
            if "text" in kind.keys():
                werte.append(str(kind.cget("text")))
        except Exception:
            continue
    return werte


with tempfile.TemporaryDirectory(prefix="glide-features323-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features323", str(REPO / "src/glide/app.pyw"))
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
        # Punkt 3: Eine Designauswahl statt dreier Schalter
        # ================================================================
        assert app.DESIGN_ORDER and set(app.DESIGN_ORDER) == set(app.DESIGNS)
        for schluessel, info in app.DESIGNS.items():
            assert info["base"] in app.THEMES, schluessel
            # Punkt 11 (3.25.0): „minimal" ist die vierte Schicht.
            # MO-060 (3.30.0): „pixel" ist die fünfte.
            assert info["layer"] in (None, "contrast", "dopamine", "minimal", "pixel"), schluessel
            assert isinstance(info["glass"], bool), schluessel
            assert info["partner"] in app.DESIGNS, schluessel
            assert info["note"].strip(), schluessel
            # Das Gegenstück des Gegenstücks ist wieder das Design selbst.
            assert app.DESIGNS[info["partner"]]["partner"] == schluessel, schluessel
            assert schluessel in app.DESIGN_SWATCH

        # Jedes Design liefert eine vollständige Farbtafel.
        app.set_design("light", apply_now=False)
        rollen = {name for name in app.active_theme() if not name.startswith("glass_")}
        for schluessel in app.DESIGN_ORDER:
            app.set_design(schluessel, apply_now=False)
            tafel = app.active_theme()
            assert app.theme_name == app.DESIGNS[schluessel]["base"]
            assert app.color_mode() == (app.DESIGNS[schluessel]["layer"] or "standard")
            assert app.glass_enabled() is app.DESIGNS[schluessel]["glass"]
            fehlend = rollen - set(tafel)
            assert not fehlend, (schluessel, fehlend)
            # Punkt 4: Der Verlauf gehört zum Glasdesign und nur dorthin.
            if app.DESIGNS[schluessel]["glass"]:
                assert tafel["glass_gradient"], schluessel
            else:
                assert tafel["glass_gradient"] == "", schluessel

        # Übernahme der drei alten Werte, ohne dass eine Einstellung verloren geht.
        N = app.normalize_personal_settings
        for alt, erwartet in (
            ({"theme": "dark", "glass_mode": True}, "glass_dark"),
            ({"theme": "light", "glass_mode": True}, "glass_light"),
            ({"theme": "dark", "glass_mode": False}, "dark"),
            ({"theme": "light", "glass_mode": False}, "light"),
            ({"theme": "dark", "color_mode": "dopamine"}, "dopamine"),
            ({"theme": "dark", "color_mode": "contrast"}, "contrast_dark"),
            ({"theme": "light", "color_mode": "contrast"}, "contrast_light"),
            ({}, "glass_light"),
            ({"design": "unbekannt"}, "glass_light"),
        ):
            ergebnis = N(dict(alt))
            assert ergebnis["design"] == erwartet, (alt, ergebnis["design"])
            info = app.DESIGNS[erwartet]
            assert ergebnis["theme"] == info["base"]
            assert ergebnis["color_mode"] == (info["layer"] or "standard")
            assert ergebnis["glass_mode"] is info["glass"]
        # Eine bereits übernommene Datei bleibt unverändert.
        assert N({"design": "dopamine", "theme": "light"})["theme"] == "dark"

        # Punkt 19 und 20 bleiben als Designs erhalten.
        app.set_design("contrast_dark", apply_now=False)
        tafel = app.active_theme()

        def kontrast(vorne, hinten):
            hell = sorted((mod.relative_luminance(vorne), mod.relative_luminance(hinten)))
            return (hell[1] + 0.05) / (hell[0] + 0.05)

        assert kontrast(tafel["text"], tafel["card"]) > 12
        # Punkte 16 und 17 (3.24.0): Die Rückmeldung gibt es in jedem Design;
        # „arcade" bleibt dem Dopamin-Design vorbehalten.
        app.set_design("dopamine", apply_now=False)
        assert app.animations_enabled() is True and app.arcade_mode() is True
        app.set_design("glass_dark", apply_now=False)
        assert app.animations_enabled() is True and app.arcade_mode() is False

        # ================================================================
        # Punkt 19: Lesbarkeit unter dem Mauszeiger, in jedem Design
        # ================================================================
        for schluessel in app.DESIGN_ORDER:
            app.set_design(schluessel, apply_now=False)
            app.theme = app.active_theme()
            kopf_hover = mod.mix_hex_colors(app.theme["hover"], app.theme["ui_accent"], 0.22)
            schrift = mod.readable_text_color(kopf_hover)
            assert kontrast(schrift, kopf_hover) >= 4.5, (schluessel, kontrast(schrift, kopf_hover))
            # Die Zeile unter dem Mauszeiger trägt lesbaren Text.
            assert kontrast(app.theme["text"], app.theme["hover"]) >= 4.5, schluessel
            assert kontrast(app.theme["selection_text"], app.theme["selection"]) >= 4.0, schluessel
        assert mod.readable_text_color("#000000") == "#FFFFFF"
        assert mod.readable_text_color("#FFFFFF") == "#15171C"
        app.set_design("glass_dark", apply_now=True)
        root.update()

        # ================================================================
        # Punkte 6 und 7: Navigation
        # ================================================================
        app.update_sidebar_list()
        root.update()
        eingang = app.ensure_inbox_list()
        reihenfolge = app.system_listbox.get_children("")
        # Punkte 1 und 2 (3.24.0): Die beiden eingerückten Zeilen aus 3.23 sind
        # Abschnitte ihrer Ansicht geworden. Die Reihenfolge der verbliebenen
        # sechs Zeilen folgt weiterhin dem Tagesablauf.
        # Seit dem 26.09.2026 ohne „In Bearbeitung“ (Abschnitt in „Mein Tag“)
        # und ohne „Verlauf“ (Knopf in der Kopfzeile).
        assert reihenfolge == (
            app.HOME_ROW_ID, app.PLAN_DAY_ROW_ID, app.LABELS_ROW_ID,
            app.TEMPLATE_ROW_ID, app.TRASH_ROW_ID,
        ), reihenfolge
        assert app.system_row_depth(("view", app.PLAN_DAY_VIEW)) == 0
        # Der Eingang bleibt eine echte Liste und bleibt erreichbar.
        app.open_inbox_list()
        root.update()
        assert app.active_list_id == eingang["id"]

        # ================================================================
        # Punkt 8: Tagespfeile in Leserichtung
        # ================================================================
        app.set_today_view()
        root.update()
        vorher = app.plan_day()
        app.plan_day_backward()
        assert app.plan_day() < vorher
        app.plan_day_forward()
        assert app.plan_day() == vorher
        # Der Rückwärtspfeil steht links vom Vorwärtspfeil. Bei side="right"
        # bestimmt die Reihenfolge in der Packliste die Anordnung: Wer zuerst
        # gepackt ist, steht am weitesten rechts. Geprüft wird deshalb die
        # Packliste und nicht die Pixelposition – die bliebe im verborgenen
        # Testfenster bei null.
        assert app.plan_day_prev_button.winfo_manager() == "pack"
        assert app.plan_day_next_button.winfo_manager() == "pack"
        geschwister = list(app.search_frame.pack_slaves())
        assert geschwister.index(app.plan_day_next_button) < geschwister.index(app.plan_day_prev_button)
        assert geschwister.index(app.plan_day_prev_button) < geschwister.index(app.clear_search_button)
        assert app.plan_day_prev_button.text == "◀" and app.plan_day_next_button.text == "▶"

        # ================================================================
        # Punkt 22: globales Auf- und Zuklappen mit sichtbarem Pfad
        # ================================================================
        ordner = app.new_folder_object("Oberordner")
        unterordner = app.new_folder_object("Unterordner")
        unterordner["parent_id"] = ordner["id"]
        app.folders.extend([ordner, unterordner])
        tief = app.new_list_object("Tiefe Liste", [app.new_item("Punkt")])
        tief["folder_id"] = unterordner["id"]
        nebenordner = app.new_folder_object("Nebenordner")
        app.folders.append(nebenordner)
        neben = app.new_list_object("Nebenliste", [])
        neben["folder_id"] = nebenordner["id"]
        app.lists.extend([tief, neben])
        app.set_active_list(tief["id"])
        app.update_sidebar_list()
        root.update()
        assert app.active_folder_chain() == [unterordner["id"], ordner["id"]]
        app.collapse_all()
        root.update()
        # Der Weg zur geöffneten Liste bleibt offen, alles daneben schließt.
        assert app.sidebar_folder_open_states[ordner["id"]] is True
        assert app.sidebar_folder_open_states[unterordner["id"]] is True
        assert app.sidebar_folder_open_states[nebenordner["id"]] is False
        app.expand_all()
        root.update()
        assert all(app.sidebar_folder_open_states[f["id"]] for f in app.folders)
        # Kein Datenverlust: Auf- und Zuklappen fasst den Bestand nicht an.
        assert any(entry["id"] == tief["id"] for entry in app.lists)
        assert app.count_items(tief["items"]) == 1

        # ================================================================
        # Punkt 23: eine Kachel „Heute" statt zweier gleicher
        # ================================================================
        assert "due" not in app.HOME_TILE_KEYS
        app.settings["home_tiles_hidden"] = []
        app.settings["home_tile_order"] = list(app.HOME_TILE_KEYS)
        app.set_home_view()
        root.update()
        beschriftungen = texte(app.home_content)
        assert any("Eingeplant" in wert for wert in beschriftungen)
        assert any("Heute fällig" in wert for wert in beschriftungen)
        # Wer die alte Kachel ausgeblendet hatte, verliert nichts.
        gepruft = N({"home_tiles_hidden": ["due"], "home_tile_order": list(app.HOME_TILE_KEYS)})
        assert "due" not in gepruft["home_tiles_hidden"]
        assert "today" in gepruft["home_tile_order"]

        # ================================================================
        # Punkt 25: Der Spaltendialog baut seinen Inhalt auf
        # ================================================================
        liste = app.new_list_object("Tabellenliste", [
            app.new_item("Erste Aufgabe", due=heute),
            app.new_item("Zweite Aufgabe"),
        ])
        app.lists.append(liste)
        app.set_active_list(liste["id"])
        app.toggle_table_view()
        root.update()
        assert app.view_mode == app.TABLE_VIEW
        gesehen = {}

        def fange(dialog, parent=None):
            dialog.update_idletasks()
            kinder = list(descendants(dialog))
            gesehen["anzahl"] = len(kinder)
            gesehen["klassen"] = [kind.winfo_class() for kind in kinder]
            gesehen["texte"] = texte(dialog)
            gesehen["knoepfe"] = [kind.text for kind in kinder if isinstance(kind, mod.RoundedButton)]
            dialog.destroy()

        echtes_modal = app.run_modal
        app.run_modal = fange
        app.show_table_columns_dialog()
        app.run_modal = echtes_modal
        assert gesehen, "Der Dialog erreichte run_modal nicht – der Aufbau brach ab."
        assert gesehen["anzahl"] > 5, gesehen["anzahl"]
        assert any("Tabellenspalten" in wert for wert in gesehen["texte"])
        # Jede wählbare Spalte steht als Kästchen im Dialog.
        assert gesehen["klassen"].count("Checkbutton") == len(app.TABLE_COLUMN_KEYS), gesehen["klassen"]
        assert "Speichern" in gesehen["knoepfe"] and "Abbrechen" in gesehen["knoepfe"]
        assert not fehler, fehler

        # ================================================================
        # Punkt 15: Spaltenbreiten bleiben nach dem Ziehen stehen
        # ================================================================
        app.refresh_tree()
        root.update()
        app._table_separator_drag = True
        app.tree.column("due", width=248)
        app.remember_table_column_widths(event=None)
        gespeichert = app.settings["table_column_widths"][liste["id"]]
        assert gespeichert["due"] == 248, gespeichert
        # Der nächste Aufbau übernimmt die gezogene Breite.
        app.refresh_tree()
        root.update()
        assert int(app.tree.column("due", "width")) == 248
        # Ein gewöhnlicher Klick auf die Überschrift schreibt keine Breite fest.
        app._table_separator_drag = False

        class Klick:
            x = 5
            y = 5

        app.tree.column("due", width=300)
        app.remember_table_column_widths(event=Klick())
        assert app.settings["table_column_widths"][liste["id"]]["due"] == 248

        # Punkt 16: ein Klick sortiert, dreistufig.
        app.sort_table_by("due")
        assert app.table_sort_for_list() == ("due", "asc")
        app.sort_table_by("due")
        assert app.table_sort_for_list() == ("due", "desc")
        app.sort_table_by("due")
        assert app.table_sort_for_list() == (None, "asc")

        # ================================================================
        # Punkte 17 und 18: jede Tabelle linksbündig und breit genug
        # ================================================================
        probe = mod.ttk.Treeview(root, columns=("a", "b"), show="tree headings")
        app.prepare_table(probe, (("#0", "Kurz", 40), ("a", "Eine sehr lange Überschrift", 40),
                                  ("b", "Mittel", 300)), stretch="b")
        assert str(probe.heading("#0", "anchor")) == "w"
        assert str(probe.column("a", "anchor")) == "w"
        assert int(probe.column("a", "minwidth")) > int(probe.column("#0", "minwidth"))
        assert int(probe.column("a", "width")) >= int(probe.column("a", "minwidth"))
        assert bool(probe.column("b", "stretch")) is True
        assert bool(probe.column("a", "stretch")) is False
        assert int(probe.column("#0", "minwidth")) >= app.TABLE_CELL_MIN_WIDTH
        probe.destroy()

        # ================================================================
        # Punkt 9: Ansichtswechsel rechnet nicht mehrfach dasselbe
        # ================================================================
        aufrufe = {"zahl": 0}
        echte_sammlung = app._collect_in_progress_items

        def gezaehlt(apply_filters=True):
            aufrufe["zahl"] += 1
            return echte_sammlung(apply_filters)

        app._collect_in_progress_items = gezaehlt
        app.set_in_progress_view()
        root.update()
        # Seitenleiste, Zähler, Zeilentexte und die Ansicht selbst fragen
        # dieselbe Menge; berechnet wird sie je Filterzustand einmal.
        assert aufrufe["zahl"] <= 2, aufrufe["zahl"]
        app._collect_in_progress_items = echte_sammlung
        # Außerhalb eines Aufbaus gibt es keinen Zwischenspeicher: Eine
        # Änderung am Bestand wirkt sofort.
        vorher = len(app.get_in_progress_items(apply_filters=False))
        frisch = app.new_item("Frisch fällig", due=heute)
        liste["items"].append(frisch)
        assert len(app.get_in_progress_items(apply_filters=False)) == vorher + 1
        liste["items"].remove(frisch)
        assert len(app.get_in_progress_items(apply_filters=False)) == vorher
        # Innerhalb eines Aufbaus bleibt der Wert stabil.
        with app.render_pass():
            erst = app.get_in_progress_items(apply_filters=False)
            assert app.get_in_progress_items(apply_filters=False) is erst
        assert app.get_in_progress_items(apply_filters=False) is not erst
        assert mod._parse_iso_date("2026-02-30") is None
        assert mod._parse_iso_date("2026-09-18") == "2026-09-18"

        # ================================================================
        # Punkt 10: Schnellerfassung mit Beschreibung und Kalender
        # ================================================================
        eingang = app.ensure_inbox_list()
        erfasst = app.capture_item("Mit Beschreibung", eingang["id"], "",
                                   "Der Zusammenhang, den man später vergisst.")
        assert erfasst is not None
        assert erfasst["description"] == "Der Zusammenhang, den man später vergisst."
        gesehen.clear()
        app.run_modal = fange
        app.show_quick_capture()
        app.run_modal = echtes_modal
        assert gesehen, "Die Schnellerfassung erreichte run_modal nicht."
        assert any("Beschreibung" in wert for wert in gesehen["texte"])
        assert any("Kalender" in wert for wert in gesehen["texte"])
        # Punkt 10: kein natives ttk-Kästchen mehr im Glide-Dialog.
        assert "TCheckbutton" not in gesehen["klassen"]
        assert gesehen["klassen"].count("Checkbutton") >= 1

        # Punkt 11: Die Kalenderauswahl hängt an jedem Datumsfeld.
        assert callable(app.attach_calendar_picker)
        probe_frame = mod.tk.Frame(root)
        probe_var = mod.tk.StringVar()
        knopf = app.attach_calendar_picker(probe_frame, probe_var)
        assert isinstance(knopf, mod.RoundedButton)
        assert knopf.text == app.ICONS["calendar"]
        probe_frame.destroy()

        # ================================================================
        # Punkte 24, 28, 29, 30: Kopfzeile und schmale Fenster
        # ================================================================
        assert app.header_density(1400) == "full"
        assert app.header_density(1000) == "compact"
        assert app.header_density(700) == "minimal"
        for breite, sichtbar in ((1400, True), (700, False)):
            app._header_density = None
            app.sync_header_density(type("E", (), {"width": breite})())
            assert (app.print_button.winfo_manager() == "pack") is sichtbar, breite
            assert (app.header_overflow_button.winfo_manager() == "pack") is (not sichtbar), breite
        app._header_density = None
        app.sync_header_density(type("E", (), {"width": 1400})())
        root.update()
        # Punkt 24: Drucken ist ohne Menü erreichbar und liegt neben dem
        # Seitenleistenschalter.
        geschwister = list(app.header_controls.pack_slaves())
        assert app.print_button in geschwister and app.sidebar_toggle_button in geschwister

        # ================================================================
        # Punkte 33, 34: Anzeigemodi der Listenansicht
        # ================================================================
        detail_item = app.new_item("Mit Details", description="Eine Beschreibung.")
        detail_item["checklist"] = app.normalize_checklist([{"text": "Schritt 1", "done": True},
                                                            {"text": "Schritt 2"}])
        detail_liste = app.new_list_object("Detailprobe", [detail_item])
        app.lists.append(detail_liste)
        app.set_active_list(detail_liste["id"])
        root.update()

        def zeilentexte():
            return [app.tree.item(iid, "text") for iid in app.tree.get_children("")]

        app.set_list_detail_mode("compact")
        root.update()
        assert len(zeilentexte()) == 1
        assert app.ICONS["checklist"] not in zeilentexte()[0]
        app.set_list_detail_mode("standard")
        root.update()
        assert len(zeilentexte()) == 1
        assert app.ICONS["checklist"] in zeilentexte()[0]
        app.set_list_detail_mode("checklist")
        root.update()
        assert len(zeilentexte()) == 3, zeilentexte()
        assert "Schritt 1" in zeilentexte()[1] and "Schritt 2" in zeilentexte()[2]
        app.set_list_detail_mode("full")
        root.update()
        assert any("Eine Beschreibung." in wert for wert in zeilentexte())
        # Eine Checklistenzeile hakt ihren eigenen Schritt ab, nicht den Punkt.
        schritt_iid = next(iid for iid in app.tree.get_children("")
                           if app.checklist_row_index(iid) == 1)
        assert app.owner_row_id(schritt_iid) == detail_item["id"]
        assert app.is_synthetic_row(schritt_iid)
        app.tree.selection_set(schritt_iid)
        app.toggle_done()
        root.update()
        assert detail_item["checklist"][1]["done"] is True
        assert detail_item["done"] is False, "Der Punkt selbst bleibt offen."
        app.tree.selection_set(schritt_iid)
        app.toggle_done()
        root.update()
        assert detail_item["checklist"][1]["done"] is False
        # Detailzeilen sind keine Punkte: Die Zahl im Bestand bleibt gleich.
        assert app.count_items(detail_liste["items"]) == 1
        gepruefte = N({"list_detail_mode": "unsinn"})
        assert gepruefte["list_detail_mode"] == app.LIST_DETAIL_DEFAULT
        assert N({})["list_detail_mode"] == "standard"
        app.set_list_detail_mode("standard")
        root.update()

        # ================================================================
        # Punkte 36 bis 40: Austauschformat
        # ================================================================
        assert app.EXCHANGE_FORMAT_VERSION == 1
        faehigkeiten = app.exchange_capabilities()
        assert faehigkeiten["checklists"] == 1 and faehigkeiten["attachments"] == 0
        quelle_item = app.new_item("Hauptpunkt", description="Kontext", due=heute,
                                   importance=3)
        quelle_item["checklist"] = app.normalize_checklist(["A", "B"])
        quelle_item["children"] = [app.new_item("Unterpunkt")]
        etikett = app.ensure_label_by_name("Austausch")
        quelle_item["labels"] = [etikett["id"]]
        gruppe = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP,
                              children=[app.new_item("In der Gruppe")])
        quelle = app.new_list_object("Austauschquelle", [quelle_item, gruppe])
        app.lists.append(quelle)
        nutzlast = app.build_exchange_payload(lists=[quelle])
        text = json.dumps(nutzlast, ensure_ascii=False)
        # Keine internen Kennungen in der Austauschdatei.
        assert quelle_item["id"] not in text and etikett["id"] not in text
        gelesen, bericht = app.parse_exchange_document(text)
        assert gelesen is not None and not bericht.errors, bericht.errors
        assert bericht.counts["tasks"] == 3 and bericht.counts["groups"] == 1
        assert bericht.counts["checklist"] == 2 and bericht.counts["labels"] == 1
        assert not bericht.unknown_fields
        listen_vorher = len(app.lists)
        angelegt = app.apply_exchange_payload(gelesen)
        assert angelegt and len(app.lists) == listen_vorher + 1
        # Punkt 37: verlustfreier Rundlauf.
        assert app.build_exchange_payload(lists=angelegt)["lists"][0]["items"] == \
            nutzlast["lists"][0]["items"]
        # Punkt 40: Ein Import ist ein einziger Rückgängig-Schritt.
        app.undo_last_change()
        assert len(app.lists) == listen_vorher
        # Unbekannte Felder werden gemeldet statt verschluckt.
        fremd = json.loads(text)
        fremd["lists"][0]["items"][0]["telepathie"] = True
        fremd["unbekannter_block"] = 1
        _gelesen, fremd_bericht = app.parse_exchange_document(json.dumps(fremd))
        assert "items.telepathie" in fremd_bericht.unknown_fields
        assert "unbekannter_block" in fremd_bericht.unknown_fields
        # Falsche Formate werden abgewiesen, nicht geraten.
        for probe in ("{}", "kein json",
                      json.dumps({"format": "glide.exchange", "format_version": 99}),
                      json.dumps({"format": "glide.exchange", "format_version": 1,
                                  "mode": "patch", "lists": []})):
            ergebnis, fehlerbericht = app.parse_exchange_document(probe)
            assert ergebnis is None and fehlerbericht.errors, probe
        # Punkt 39: Die Gliederung in Markdown als zweiter Weg.
        aus_markdown = app.exchange_payload_from_markdown(
            "# Projektplan\n## Vorbereitung\n- Angebot einholen\n"
            "  - [ ] Preise vergleichen\n  - [x] Anbieter wählen\n"
            "- Termin abstimmen\n  - Unterpunkt\n")
        assert aus_markdown is not None
        md_gelesen, md_bericht = app.parse_exchange_document(
            json.dumps(aus_markdown, ensure_ascii=False))
        assert md_gelesen is not None and not md_bericht.errors
        assert md_bericht.counts["headings"] == 1 and md_bericht.counts["checklist"] == 2
        assert md_bericht.counts["children"] == 1
        # Punkt 38: Die Anweisung entsteht aus den echten Konstanten.
        anweisung = app.exchange_prompt_text()
        assert app.EXCHANGE_FORMAT_NAME in anweisung
        assert str(app.MAX_CHECKLIST_ENTRIES) in anweisung
        assert "planned_date" in anweisung and "heading" in anweisung

        # ================================================================
        # Punkte 12, 13, 14: Pinnwand
        # ================================================================
        k1 = app.new_item("Karte A")
        k2 = app.new_item("Karte B")
        k3 = app.new_item("Karte C")
        board_liste = app.new_list_object("Pinnwandprobe", [k1, k2, k3])
        app.lists.append(board_liste)
        app.set_active_list(board_liste["id"])
        arbeitsflaeche = app.workspace
        arbeitsflaeche.pin([k1["id"], k2["id"], k3["id"]])
        arbeitsflaeche.set_mode("board")
        root.update()
        assert len(arbeitsflaeche.card_boxes) == 3
        # Punkt 13: Verbindungen sind Beziehungen, keine gezeichneten Linien.
        assert arbeitsflaeche.toggle_connection(k1["id"], k2["id"]) is True
        # Punkt 9 (3.24.0): Eine Verbindung trägt seit 3.24 zusätzlich ihre
        # Richtung und ihre Art. Gespeichert bleibt sie eine Beziehung zwischen
        # zwei Punktkennungen, keine gezeichnete Linie.
        assert arbeitsflaeche.connections() == [
            (k1["id"], k2["id"], mod.ItemWorkspace.CONNECTION_STYLE_DEFAULT)]
        gespeicherte = app.settings["pinboards"][arbeitsflaeche.context()]["connections"]
        assert gespeicherte and set(gespeicherte[0]) == {"from", "to", "style"}
        # Sie übersteht die Normalisierung der Einstellungen.
        nach_normalisierung = mod.ItemWorkspace.normalize_settings(copy.deepcopy(app.settings))
        assert nach_normalisierung["pinboards"][arbeitsflaeche.context()]["connections"]
        # Ein zweiter Aufruf nimmt sie zurück; ein Selbstbezug entsteht nie.
        assert arbeitsflaeche.toggle_connection(k2["id"], k1["id"]) is True
        assert arbeitsflaeche.connections() == []
        assert arbeitsflaeche.toggle_connection(k1["id"], k1["id"]) is False
        arbeitsflaeche.toggle_connection(k1["id"], k2["id"])
        arbeitsflaeche.toggle_connection(k2["id"], k3["id"])
        root.update()
        assert len(arbeitsflaeche.canvas.find_withtag("connection")) == 2
        # Beim Verschieben wandert die Linie mit, weil sie neu berechnet wird.
        arbeitsflaeche.store_position(k1["id"], 500, 400)
        root.update()
        assert len(arbeitsflaeche.canvas.find_withtag("connection")) == 2
        # Punkt 12: Gedruckt wird die belegte Fläche.
        geometrie = arbeitsflaeche.board_print_geometry()
        assert geometrie is not None and geometrie[2] > 0 and geometrie[3] > 0
        druck = arbeitsflaeche.build_board_print_html()
        assert druck.count('class="card') == 3
        assert druck.count("<line") == 2
        assert "@page" in druck and "Pinnwand" in druck
        # Punkt 14: Fokusmodus blendet aus und stellt wieder her.
        assert arbeitsflaeche.board_focus_active() is False
        arbeitsflaeche.enter_board_focus()
        root.update()
        assert arbeitsflaeche.board_focus_active() is True
        assert app.settings["sidebar_visible"] is False
        assert app.header_frame.winfo_manager() != "pack"
        arbeitsflaeche.board_escape()
        root.update()
        assert arbeitsflaeche.board_focus_active() is False
        assert app.settings["sidebar_visible"] is True
        assert app.header_frame.winfo_manager() == "pack"
        # Escape bricht zuerst das Verbinden ab.
        arbeitsflaeche.selected_id = k1["id"]
        arbeitsflaeche.start_connect_mode()
        assert arbeitsflaeche._connect_from == k1["id"]
        arbeitsflaeche.board_escape()
        assert arbeitsflaeche._connect_from is None
        assert arbeitsflaeche.mode == "board", "Escape darf die Pinnwand hier nicht verlassen."
        # Punkt 13: Ein neuer Punkt auf der Fläche ist ein echter Punkt.
        vorher_punkte = app.count_items(board_liste["items"])
        # Punkt 5 (3.24.0): Der neue Punkt entsteht seit 3.24 in der
        # vollständigen Punktmaske statt in einer einzeiligen Eingabe – mit
        # Beschreibung, Labels, Checkliste und Anhängen.
        app.new_item_dialog = lambda *args, **kwargs: {
            "text": "Direkt auf der Fläche", "kind": app.ITEM_KIND_TASK,
            "importance": 0, "color": None, "due": None, "due_time": None,
            "planned_date": None, "estimated_minutes": None, "repeat": None,
            "reminder": None, "labels": [], "description": "Aus der Fläche heraus",
            "checklist": [], "attachments": [], "list_id": board_liste["id"],
        }
        arbeitsflaeche.create_card_item(320, 240)
        root.update()
        assert app.count_items(board_liste["items"]) == vorher_punkte + 1
        neuer = next(wert for wert in board_liste["items"]
                     if wert.get("text") == "Direkt auf der Fläche")
        assert any(karte["item_id"] == neuer["id"]
                   for karte in app.settings["pinboards"][arbeitsflaeche.context()]["cards"])
        # Er steht auch in der Liste – es gibt keine zweite Datenhaltung.
        arbeitsflaeche.set_mode("list")
        root.update()
        assert neuer["id"] in app.tree.get_children("")
        # Eine entfernte Karte nimmt ihre Verbindungen mit.
        arbeitsflaeche.set_mode("board")
        root.update()
        arbeitsflaeche.selected_id = k2["id"]
        arbeitsflaeche.unpin()
        root.update()
        assert all(k2["id"] not in paar for paar in arbeitsflaeche.connections())
        arbeitsflaeche.set_mode("list")
        root.update()

        assert not fehler, fehler
        print("OK 3.23: Design, Navigation, Startseite, Tabellen, Dialoge, Anzeigemodi, Austauschformat, Pinnwand und Leistung")
    finally:
        try:
            root.destroy()
        except Exception:
            pass
