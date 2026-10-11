"""Glide 3.25: Übersichtlichkeit, Hierarchie und eine minimalistische Oberfläche.

Jeder Abschnitt trägt die Nummer des Auftragspunkts, den er nachweist.
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


def menu_labels(menu):
    """Alle Beschriftungen eines Menüs samt Untermenüs mit ihrem Pfad."""
    ergebnis = []

    def besuchen(aktuell, pfad):
        ende = aktuell.index("end")
        for index in range((ende if ende is not None else -1) + 1):
            art = aktuell.type(index)
            if art == "cascade":
                kind = aktuell.nametowidget(aktuell.entrycget(index, "menu"))
                besuchen(kind, pfad + [aktuell.entrycget(index, "label")])
            elif art == "command":
                ergebnis.append((" › ".join(pfad), aktuell.entrycget(index, "label")))

    besuchen(menu, [])
    return ergebnis


with tempfile.TemporaryDirectory(prefix="glide-features325-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features325", str(REPO / "src/glide/app.pyw"))
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
        # Punkt 1.7: Eine Schaltfläche ist so breit wie ihre Beschriftung
        # ================================================================
        rahmen = mod.tk.Frame(root, bg=app.theme["bg"])
        for text in ("OK", "Als HTML speichern", "Öffnen und drucken",
                     "Arbeitsdateien verschieben …"):
            knopf = app._make_dialog_button(rahmen, text, lambda: None, "muted")
            assert int(knopf.cget("width")) >= knopf.text_width() + 8, text
        # Eine längere Beschriftung lässt die Fläche mitwachsen.
        knopf = app._make_dialog_button(rahmen, "Kurz", lambda: None, "muted")
        vorher = int(knopf.cget("width"))
        knopf.set_text("Eine deutlich längere Beschriftung für dieselbe Fläche")
        assert int(knopf.cget("width")) > vorher
        assert int(knopf.cget("width")) >= knopf.text_width() + 8
        # Ein unbekannter Farbschlüssel darf kein Fenster verhindern.
        assert app.dialog_color("gibt_es_nicht") == app.theme["accent"]
        assert app.dialog_color("#123456") == "#123456"
        rahmen.destroy()

        # ================================================================
        # Punkt 1.1 und 2.1: Feldpaare stehen auf einer Linie
        # ================================================================
        raster = mod.FieldPairGrid(root, bg=app.theme["bg"], gap=16)
        raster.pack(fill="x")
        for spalte, text in enumerate(("Eine sehr lange Beschriftung, die umbricht",
                                       "Kurz")):
            kopf, fuss = raster.cell(spalte)
            beschriftung = mod.tk.Label(kopf, text=text, bg=app.theme["bg"],
                                        wraplength=120, justify="left")
            beschriftung.pack(side="bottom", fill="x")
            mod.tk.Entry(fuss).pack(fill="x")
        root.update()
        felder = [w for w in descendants(raster) if isinstance(w, mod.tk.Entry)]
        assert len(felder) == 2
        assert felder[0].winfo_rooty() == felder[1].winfo_rooty(), (
            felder[0].winfo_rooty(), felder[1].winfo_rooty())
        # Beide Spalten sind gleich breit – der Zwischenraum wird geteilt.
        assert abs(felder[0].winfo_width() - felder[1].winfo_width()) <= 1
        raster.destroy()

        # ================================================================
        # Punkte 1.2 und 1.3: „Erweitert" arbeitet in abgeleiteten Ansichten
        # ================================================================
        liste = app.new_list_object("Fristen 3.25", [])
        app.lists.append(liste)
        vergangen = (heute - timedelta(days=5)).isoformat()
        auch_alt = (heute - timedelta(days=2)).isoformat()
        kuenftig = (heute + timedelta(days=6)).isoformat()
        alt = app.new_item("Längst fällig", due=vergangen)
        zweit = app.new_item("Auch überfällig", due=auch_alt)
        spaeter = app.new_item("Kommt noch", due=kuenftig)
        liste["items"].extend([alt, zweit, spaeter])
        app.set_active_list(liste["id"])
        app.save_items()

        aufrufe = {}

        def maske(*args, **kwargs):
            aufrufe.update(kwargs)
            return None

        app.new_item_dialog = maske
        for ansicht, setzen in (("in_progress", app.set_in_progress_view),
                                ("overdue", app.set_overdue_view),
                                (app.PLAN_DAY_VIEW, app.set_today_view),
                                (app.LABELS_VIEW, app.set_labels_view)):
            aufrufe.clear()
            meldungen.clear()
            setzen()
            root.update()
            assert app.view_mode == ansicht, ansicht
            assert app.add_item_advanced() == "break", ansicht
            # Die Maske wurde geöffnet – nicht ein Hinweis gezeigt.
            assert aufrufe.get("allow_list_choice") is True, (ansicht, aufrufe)
            assert not meldungen, (ansicht, meldungen)
        # „Mein Tag" bringt seinen Tag als Vorbelegung mit.
        aufrufe.clear()
        app.set_today_view()
        app.add_item_advanced()
        assert aufrufe.get("default_planned") == app.plan_day()
        del app.new_item_dialog

        # ================================================================
        # Punkte 1.5, 1.6 und 2.2: Abschnitte mit Hierarchie
        # ================================================================
        # Seit 3.33.6 (D14) steht die nächste Aufgabe oben in „Heute“;
        # „Demnächst“ (bis 3.33.5 „In Bearbeitung“) zeigt chronologisch ohne sie.
        app.set_in_progress_view()
        root.update()
        abschnitte = [zeile for zeile in app.tree.get_children("")
                      if zeile in app.OVERVIEW_SECTION_ROW_IDS]
        assert app.NEXT_TASK_SECTION_ROW_ID not in abschnitte
        assert abschnitte[0] == app.OVERDUE_SECTION_ROW_ID
        assert app.IN_PROGRESS_SECTION_ROW_ID in abschnitte
        # Ein Abschnitt lässt sich zuklappen, und das übersteht den Aufbau.
        app.set_overview_section_open(app.OVERDUE_SECTION_ROW_ID, False)
        app.refresh_tree()
        root.update()
        assert not app.tree.item(app.OVERDUE_SECTION_ROW_ID, "open")
        assert app.tree.item(app.IN_PROGRESS_SECTION_ROW_ID, "open")
        assert app.OVERDUE_SECTION_ROW_ID in app.settings["overview_sections_closed"]
        # Eine unbekannte Kennung überlebt die Normalisierung nicht.
        bereinigt = app.normalize_personal_settings(
            {"overview_sections_closed": [app.OVERDUE_SECTION_ROW_ID, "section:erfunden"]})
        assert bereinigt["overview_sections_closed"] == [app.OVERDUE_SECTION_ROW_ID]
        app.set_overview_section_open(app.OVERDUE_SECTION_ROW_ID, True)
        app.set_today_view()
        root.update()
        abschnitte = [zeile for zeile in app.tree.get_children("")
                      if zeile in app.OVERVIEW_SECTION_ROW_IDS]
        assert abschnitte[0] == app.NEXT_TASK_SECTION_ROW_ID
        # Genau eine Aufgabe steht im Abschnitt „Nächste Aufgabe".
        assert len(app.tree.get_children(app.NEXT_TASK_SECTION_ROW_ID)) == 1
        # Und sie steht in keinem anderen Abschnitt noch einmal.
        naechste = app.tree.get_children(app.NEXT_TASK_SECTION_ROW_ID)[0]
        for abschnitt in abschnitte[1:]:
            assert naechste not in app.tree.get_children(abschnitt)
        # Startseite und Übersicht nennen dieselbe Aufgabe.
        fokus_item, _quelle = app.home_focus_candidate()
        assert fokus_item["id"] == app.in_progress_item_sources[naechste][1]
        assert fokus_item["id"] == alt["id"]
        # Die Rangfolge steht an einer Stelle und ist begründbar.
        assert app.task_urgency_rank(alt) < app.task_urgency_rank(spaeter)
        # Der Eingang in „Mein Tag" ist ebenfalls ein Abschnitt mit Kindern.
        eingang_punkt = app.new_item("Ohne Tag und ohne Frist")
        liste["items"].append(eingang_punkt)
        app.save_items()
        app.set_today_view()
        root.update()
        if app.PLAN_INBOX_HEADING_ROW_ID in app.tree.get_children(""):
            kinder = app.tree.get_children(app.PLAN_INBOX_HEADING_ROW_ID)
            assert kinder, "Der Eingang trägt seine Punkte als Kinder."
        # Der Weg zur nächsten Aufgabe führt in ihren Abschnitt.
        app.set_home_view()
        assert app.open_next_task() == "break"
        assert app.view_mode == app.PLAN_DAY_VIEW
        assert app.tree.selection() and app.tree.parent(app.tree.selection()[0]) == \
            app.NEXT_TASK_SECTION_ROW_ID

        # ================================================================
        # Punkt 1.4: Die Anzeigeauswahl ist kurz und öffnet am Auslöser
        # ================================================================
        for _key, name, hinweis in app.LIST_DETAIL_MODES:
            assert len(hinweis) <= 60, hinweis
            assert not hinweis.endswith("."), hinweis
            assert name and hinweis
        app.set_active_list(liste["id"])
        # Die Lage einer Fläche lässt sich nur an einem sichtbaren Fenster
        # messen; ein zurückgezogenes Fenster meldet Ersatzkoordinaten.
        root.deiconify()
        root.update()
        assert app.show_detail_mode_menu() == "break"
        popup = getattr(app, "_active_dropdown", None)
        assert popup is not None and popup.winfo_exists()
        root.update()
        knopf = app.detail_button
        # Rechte Kanten fluchten, statt die Fläche nach rechts hinauszuschieben.
        assert popup.winfo_rootx() + popup.winfo_width() <= \
            knopf.winfo_rootx() + knopf.winfo_width() + 2, (
                popup.winfo_rootx(), popup.winfo_width(),
                knopf.winfo_rootx(), knopf.winfo_width())
        # Und sie steht unter ihrem Auslöser, nicht daneben.
        assert popup.winfo_rooty() >= knopf.winfo_rooty()
        popup.close()
        root.update()
        root.withdraw()
        root.update()

        # ================================================================
        # Punkte 1.9 und 1.10: Menüs gruppiert, Handbuch vorhanden
        # ================================================================
        eintraege = app.app_action_entries()
        assert eintraege
        # Jede Aktion ist einer Aufgabengruppe zugeordnet.
        ohne = [e["label"] for e in eintraege if e["group"] == app.ACTION_GROUP_FALLBACK]
        assert not ohne, ohne
        # Kein Hauptmenü trägt mehr als zwölf Einträge auf oberster Ebene.
        for titel, menu in app.action_menus:
            ende = menu.index("end")
            anzahl = sum(1 for index in range((ende if ende is not None else -1) + 1)
                         if menu.type(index) in ("command", "cascade"))
            assert anzahl <= 12, (titel, anzahl)
        pfade = dict((label, pfad) for pfad, label in menu_labels(app.menubar))
        for label, erwartet in (("Handbuch …", "Hilfe"),
                                ("Fehlerprotokoll öffnen", "Hilfe"),
                                ("Nächste Aufgabe", "Ansicht › Ansichten"),
                                ("Verspätet", "Ansicht › Ansichten"),
                                ("Drucken und PDF …", "Datei › Exportieren"),
                                ("Datenordner wechseln …", "Datei › Datenablage"),
                                ("Globale Pinnwand öffnen", "Ansicht › Pinnwand")):
            assert pfade.get(label) == erwartet, (label, pfade.get(label))
        # Jedes Menü ist dem Theme gemeldet – sonst bliebe es ungefärbt.
        assert len(app.menus) >= 20
        # Das Handbuch nennt jeden Bereich und lässt sich durchsuchen.
        assert len(app.MANUAL_SECTIONS) >= 8
        for bereich, zeilen in app.MANUAL_SECTIONS:
            assert bereich.strip() and zeilen
            for name, zweck, ort in zeilen:
                assert name.strip() and zweck.strip() and ort.strip()
        assert [b for b, _z in app.manual_entries("pinnwand")]
        assert app.manual_entries("gibtesnichtimhandbuch") == []

        # ================================================================
        # Punkt 1.11: Zwei Designs ohne Farbe
        # ================================================================
        def neutral(wert):
            return len(wert) == 7 and wert[1:3] == wert[3:5] == wert[5:7]

        for schluessel in ("minimal_light", "minimal_dark"):
            assert schluessel in app.DESIGNS and schluessel in app.DESIGN_ORDER
            app.set_design(schluessel, apply_now=False)
            tafel = app.active_theme()
            bunt = sorted(name for name, wert in tafel.items()
                          if isinstance(wert, str) and wert.startswith("#") and not neutral(wert))
            assert set(bunt) <= {"ui_accent", "selection", "selection_text"}, (schluessel, bunt)
            for flaeche in ("bg", "card", "input", "hover"):
                for schrift, schwelle in (("text", 4.5), ("muted", 4.5), ("placeholder", 3.0)):
                    wert = mod.contrast_ratio(tafel[flaeche], tafel[schrift])
                    assert wert >= schwelle, (schluessel, flaeche, schrift, wert)
            assert mod.contrast_ratio(tafel["selection"], tafel["selection_text"]) >= 4.5
            # Dringlichkeit bleibt unterscheidbar – über Helligkeit.
            assert tafel["overdue"] != tafel["due_today"] != tafel["priority_low"]
        app.set_design("dark", apply_now=False)
        app.apply_theme()

        # ================================================================
        # Punkt 1.12: Rückmeldung auf jede Aktion
        # ================================================================
        gezeigt = []
        echte_fahne = app.play_celebration
        app.play_celebration = lambda text: gezeigt.append(text)
        app.settings["action_feedback"] = "auto"
        app.set_design("light", apply_now=False)
        assert app.action_feedback_level() == "milestones"
        gezeigt.clear()
        app.feedback("list_created")
        assert not gezeigt
        app.set_design("dopamine", apply_now=False)
        assert app.action_feedback_level() == "all"
        app.feedback("list_created")
        assert gezeigt == [f"{app.ICONS['list']}  Liste angelegt"], gezeigt
        # Jeder Vorgang hat einen Text in Einzahl und Mehrzahl.
        gezeigt.clear()
        for schluessel, (symbol, einzahl, mehrzahl) in app.ACTION_FEEDBACK_TEXTS.items():
            assert symbol in app.ICONS, schluessel
            assert einzahl.strip() and mehrzahl.strip(), schluessel
            app.feedback(schluessel, 3)
        assert len(gezeigt) == len(app.ACTION_FEEDBACK_TEXTS)
        # Ein unbekannter Vorgang bleibt still, statt zu scheitern.
        gezeigt.clear()
        app.feedback("gibt_es_nicht")
        assert not gezeigt
        # Abgeschaltete Bewegung schweigt in jeder Stufe.
        app.settings["animations_enabled"] = False
        app.feedback("list_created", milestone=True)
        assert not gezeigt
        app.settings["animations_enabled"] = True
        app.settings["action_feedback"] = "milestones"
        app.set_design("dopamine", apply_now=False)
        assert app.action_feedback_level() == "milestones"
        app.settings["action_feedback"] = app.ACTION_FEEDBACK_DEFAULT
        app.set_design("dark", apply_now=False)
        app.apply_theme()
        app.play_celebration = echte_fahne

        # ================================================================
        # Punkte 3.1 bis 3.4: Pinnwand
        # ================================================================
        k1 = app.new_item("Karte eins")
        k2 = app.new_item("Karte zwei")
        tafel_liste = app.new_list_object("Pinnwand 3.25", [k1, k2])
        app.lists.append(tafel_liste)
        app.set_active_list(tafel_liste["id"])
        flaeche = app.workspace
        flaeche.pin([k1["id"], k2["id"]])
        flaeche.set_mode("board")
        root.update()
        flaeche.configure_board("connection_style", "forward")
        assert flaeche.toggle_connection(k1["id"], k2["id"]) is True
        # Punkt 3.1: Die Linie endet am Kartenrand und liegt vor den Karten.
        flaeche.store_position(k1["id"], 40, 40)
        flaeche.store_position(k2["id"], 500, 400)
        root.update()
        linien = flaeche.canvas.find_withtag("connection")
        assert len(linien) == 1
        koordinaten = flaeche.canvas.coords(linien[0])
        links = flaeche.card_boxes[k1["id"]]
        rechts = flaeche.card_boxes[k2["id"]]

        def innerhalb(x, y, box):
            return box[0] <= x <= box[0] + box[2] and box[1] <= y <= box[1] + box[3]

        assert not innerhalb(koordinaten[0], koordinaten[1], links)
        assert not innerhalb(koordinaten[-2], koordinaten[-1], rechts)
        # Vor den Karten heißt: höher gestapelt als jede Karte.
        karten = flaeche.canvas.find_withtag("card:" + k2["id"])
        assert karten and linien[0] > max(karten)
        # Der Randpunkt liegt auf dem Rechteck, nicht irgendwo davor.
        punkt = flaeche.border_point((0.0, 0.0, 100.0, 50.0), 200.0, 25.0)
        assert abs(punkt[0] - 100.0) < 0.01 and abs(punkt[1] - 25.0) < 0.01
        # Punkt 3.3: Der Reiter ist kurz und schneidet am Wortende.
        assert mod.ItemWorkspace.tab_label("Anstehende Aufgaben sammeln") == "Anstehende…"
        assert mod.ItemWorkspace.tab_label("Kurz") == "Kurz"
        # Ein Wort ohne Lücke wird hart geschnitten; das Auslassungszeichen
        # kommt hinzu und zählt nicht zur Zeichengrenze.
        lang = mod.ItemWorkspace.tab_label("Donaudampfschifffahrtsgesellschaft")
        assert lang.endswith("…") and len(lang) == mod.ItemWorkspace.TAB_LABEL_CHARS + 1, lang
        assert mod.ItemWorkspace.TAB_TEXT_INSET >= 40
        # Punkt 3.4: Das Kontextmenü wählt die getroffene Karte aus.
        flaeche.select_card(None)
        menues = []
        echtes_menu = app._new_themed_popup_menu

        class Attrappe:
            def __init__(self):
                self.labels = []

            def add_command(self, label="", **kwargs):
                self.labels.append(label.strip())

            def add_separator(self):
                self.labels.append("---")

            def tk_popup(self, *args, **kwargs):
                return None

            def grab_release(self):
                return None

        def gefangen():
            menues.append(Attrappe())
            return menues[-1]

        app._new_themed_popup_menu = gefangen
        kasten = flaeche.card_boxes[k1["id"]]

        class Klick:
            x = int(kasten[0] + 10 - flaeche.canvas.canvasx(0))
            y = int(kasten[1] + 10 - flaeche.canvas.canvasy(0))
            x_root = 100
            y_root = 100

        assert flaeche.show_card_context_menu(Klick()) == "break"
        assert flaeche.selection() == [k1["id"]]
        assert any("Bearbeiten" in text for text in menues[-1].labels)
        assert any("Neue Aufgabe hier" in text for text in menues[-1].labels)
        app._new_themed_popup_menu = echtes_menu

        # Punkt 3.2: Aus der globalen Pinnwand führt ein Weg zurück
        app.open_global_board()
        root.update()
        assert app.view_mode == app.GLOBAL_BOARD_VIEW
        zurueck = [w for w in descendants(app.workspace.bar)
                   if isinstance(w, mod.RoundedButton) and "Übersicht" in w.text]
        assert zurueck, [w.text for w in descendants(app.workspace.bar)
                         if isinstance(w, mod.RoundedButton)]
        zurueck[0].command()
        root.update()
        assert app.view_mode == app.LIBRARY_VIEW

        # ================================================================
        # Punkte 4.1 bis 4.3: Startseite
        # ================================================================
        app.settings["home_tile_order"] = list(app.HOME_TILE_KEYS)
        app.settings["home_tiles_hidden"] = []
        app.set_home_view()
        root.update()
        vorschauen = [w for w in descendants(app.home_content) if isinstance(w, mod.BoardPreview)]
        figuren = [w for w in descendants(app.home_content) if isinstance(w, mod.MascotCanvas)]
        assert len(vorschauen) == 1 and len(figuren) == 1
        # Die Vorschau zeigt die echten Karten der globalen Fläche.
        flaechen, verbindungen, anzahl = app.global_board_preview()
        assert anzahl == len(flaechen)
        vorschauen[0].set_content(flaechen, verbindungen)
        root.update()
        assert bool(vorschauen[0].find_all()) == bool(flaechen), "Leere Pinnwände haben keine erfundenen Karten."
        # Punkt 4.3: Vier Wege stehen als Fläche da, der Rest im Menü.
        sichtbar = [key for _button, key in app.home_quick_actions.entries]
        assert sichtbar == ["today", "progress", "inbox", "board", "more"], sichtbar
        gruppen = [name for name, _eintraege in app.home_more_actions()]
        assert gruppen == ["Ansichten", "Anlegen", "Einrichten"]
        # Punkt 4.2: Der Begleiter spiegelt den Bestand, nicht den Menschen.
        zustand, satz = app.mascot_state()
        assert zustand in mod.MascotCanvas.STATES and satz.strip()
        assert zustand == "sorgt", zustand
        for name in mod.MascotCanvas.STATES:
            figuren[0].set_state(name)
            root.update()
            assert figuren[0].find_all(), name
        app.settings["mascot_name"] = "  Bo  "
        assert app.normalize_personal_settings(dict(app.settings))["mascot_name"] == "Bo"
        app.settings["mascot_name"] = ""

        # ================================================================
        # Punkt 5.2: Ein Fehler hält die Anwendung nicht an
        # ================================================================
        assert hasattr(mod.sys.stdout, "write") and hasattr(mod.sys.stderr, "write")
        vorher_gross = os.path.getsize(mod.ERROR_LOG_FILE) if os.path.isfile(mod.ERROR_LOG_FILE) else 0
        app.report_callback_exception(ValueError, ValueError("Prüffehler 3.25"), None)
        inhalt = Path(mod.ERROR_LOG_FILE).read_text(encoding="utf-8")
        assert "Prüffehler 3.25" in inhalt
        assert os.path.getsize(mod.ERROR_LOG_FILE) > vorher_gross
        # Der eigene Bericht ersetzt den des Prüflaufs nicht.
        assert fehler, "Der vorhandene Bericht wird weiterhin aufgerufen."
        fehler.clear()
        # Ein sehr großes Protokoll wird gekürzt statt unbegrenzt zu wachsen.
        Path(mod.ERROR_LOG_FILE).write_text("x" * (mod.ERROR_LOG_MAX_BYTES + 5000), encoding="utf-8")
        app.log_error("Nach dem Kürzen\n")
        assert os.path.getsize(mod.ERROR_LOG_FILE) <= mod.ERROR_LOG_MAX_BYTES
        assert "Nach dem Kürzen" in Path(mod.ERROR_LOG_FILE).read_text(encoding="utf-8")
        # Ein modaler Dialog ohne Griff blockiert nicht.
        probe = mod.tk.Toplevel(root)
        probe.withdraw()
        probe.after(60, probe.destroy)
        app.run_modal(probe)
        assert not probe.winfo_exists()

        # ================================================================
        # Punkt 1.8: „Über Glide" führt zur Datenablage
        # ================================================================
        aktionen = [text for text, _befehl, _farbe in app.about_actions()]
        assert "Arbeitsdateien verschieben …" in aktionen
        assert mod.BASE_DIR in app.about_text()
        assert f"Version {mod.APP_VERSION}" in app.about_text()

        assert not fehler, fehler
        print("OK 3.25: Feldraster, erweiterte Eingabe in Übersichten, aufklappbare Abschnitte, "
              "nächste Aufgabe, Menügruppen, Handbuch, Minimaldesigns, Rückmeldungen, "
              "Pinnwandverbindungen, Startseite und Fehlerbericht")
    finally:
        try:
            root.destroy()
        except Exception:
            pass
