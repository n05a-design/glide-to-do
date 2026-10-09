"""Paket Komfort 3.33.20: KO02, KO03, KO05, KO06, U04, U20, N07, AB08, AU06.

Über echte Einstiege (Kontextmenüs, Eingabezeile, Einfügeereignis,
Startseite, „Heute“): Wiederholungen überspringen ohne Erledigung und mit
einem Undo-Schritt, Erinnerung aus der Schnelleingabe, mehrzeiliges Einfügen
mit Rückfrage, zuletzt benutzte Ziele vorn, „+“ und Umschalt+Enter, ein
Anlegeweg je Leerzustand, Karte „Neu in …“ nur nach einem Update, Abweisung
zu alter Laufzeiten vor jedem Datenzugriff und Routinen in „Heute“. Dazu der
Befund aus der Analyse: „Als erledigt markieren“ in einer Übersicht nimmt
denselben Weg wie das Abhaken in der Liste.

--app wählt den Quellstand; mit der unveränderten 3.33.19 muss die Suite rot
sein (Gegenprobe). Künstliche Daten in einem temporären GLIDE_DATA_DIR.
"""
import argparse
from datetime import date, timedelta
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import subprocess
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


def eintraege(menu):
    """Beschriftung → Index aller Befehle eines Menüs."""
    ende = menu.index("end")
    return {menu.entrycget(i, "label"): i for i in range(-1 if ende is None else ende + 1)
            if menu.type(i) not in ("separator", "tearoff")}


def tag(versatz):
    return (date.today() + timedelta(days=versatz)).isoformat()


with tempfile.TemporaryDirectory(prefix="glide-komfort-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_komfort_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    fehler, infos, toasts = [], [], []
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
    app.show_info = lambda *a, **k: infos.append(a)
    app.ask_yes_no = lambda *a, **k: True
    toast = app.show_undo_toast
    app.show_undo_toast = lambda text, *a, **k: (toasts.append(text), toast(text, *a, **k))[1]
    pruefungen = []

    def ruhe(sekunden=0.15):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    def auswaehlen(*items):
        app.tree.selection_set([item["id"] for item in items])
        app.tree.focus(items[-1]["id"])

    try:
        # --- KO02: Wiederholung überspringen --------------------------------
        alle3 = app.new_item("Pflanzen gießen", due=tag(-7), repeat={"art": "tage", "abstand": 3},
                             reminder={"mode": "fixed", "at": app.local_reminder_time(tag(-7), "08:00")})
        woche = app.new_item("Wochenbericht", due=tag(0), repeat={"art": "woechentlich"},
                             reminder={"mode": "relative", "minutes": 30})
        einmal = app.new_item("Einmalig", due=tag(-1))
        arbeit = app.new_list_object("Arbeit", [alle3, woche, einmal])
        app.lists.append(arbeit)
        app.save_items()
        app.set_active_list(arbeit["id"])
        ruhe()
        gebucht = []
        buchen = app.book_completions
        app.book_completions = lambda anzahl: (gebucht.append(anzahl), buchen(anzahl))[1]

        auswaehlen(alle3)
        menue = eintraege(app.build_item_context_menu())
        assert "Diesen Termin überspringen" in menue and "Verpasste Termine überspringen" in menue, sorted(menue)
        auswaehlen(woche)
        menue = eintraege(app.build_item_context_menu())
        assert "Diesen Termin überspringen" in menue and "Verpasste Termine überspringen" not in menue
        auswaehlen(einmal)
        menue = eintraege(app.build_item_context_menu())
        assert not any("überspringen" in text for text in menue), sorted(menue)
        pruefungen.append("KO02: Kontextmenü nur bei Wiederholung, „verpasst“ nur bei Überfälligem")

        auswaehlen(alle3)
        tiefe = len(app.undo_stack)
        menu = app.build_item_context_menu()
        menu.invoke(eintraege(menu)["Diesen Termin überspringen"])
        ruhe()
        alle3 = app.find_item_in_lists(alle3["id"])[0]
        assert alle3["due"] == tag(-4) and not alle3.get("done"), alle3
        assert alle3.get("reminder") is None, alle3.get("reminder")  # feste Erinnerung gehörte zum Termin
        assert app.normalize_repeat(alle3.get("repeat"))["abstand"] == 3, alle3.get("repeat")
        assert len(app.undo_stack) == tiefe + 1 and not any(gebucht), (len(app.undo_stack), gebucht)
        assert toasts[-1].startswith("Termin übersprungen · nächster"), toasts[-1]
        app.undo_last_change()
        ruhe()
        alle3 = app.find_item_in_lists(alle3["id"])[0]
        assert alle3["due"] == tag(-7) and alle3["reminder"]["mode"] == "fixed", alle3
        pruefungen.append("KO02: „Diesen Termin“ rückt einen Termin vor, ohne Erledigung, ein Undo-Schritt")

        auswaehlen(alle3)
        menu = app.build_item_context_menu()
        menu.invoke(eintraege(menu)["Verpasste Termine überspringen"])
        ruhe()
        alle3 = app.find_item_in_lists(alle3["id"])[0]
        assert alle3["due"] == tag(2), alle3["due"]  # erster Termin am oder nach heute: −7 + 9
        assert toasts[-1].startswith("Verpasste Termine übersprungen"), toasts[-1]
        app.undo_last_change()
        ruhe()
        # Mehrfachauswahl: ein Undo-Schritt, Vorlauf-Erinnerung bleibt, Einmaliges zählt nicht.
        alle3, woche = app.find_item_in_lists(alle3["id"])[0], app.find_item_in_lists(woche["id"])[0]
        auswaehlen(alle3, woche, einmal)
        tiefe = len(app.undo_stack)
        assert app.skip_repeat_selected() == "break"
        ruhe()
        alle3, woche = app.find_item_in_lists(alle3["id"])[0], app.find_item_in_lists(woche["id"])[0]
        assert (alle3["due"], woche["due"]) == (tag(-4), tag(7)), (alle3["due"], woche["due"])
        assert woche["reminder"] == {"mode": "relative", "minutes": 30}, woche["reminder"]
        assert app.find_item_in_lists(einmal["id"])[0]["due"] == tag(-1)
        assert len(app.undo_stack) == tiefe + 1 and toasts[-1] == "2 Wiederholungen vorgerückt", toasts[-1]
        app.undo_last_change()
        ruhe()
        # Detailbereich: derselbe Weg, nur bei gespeicherter Regel mit Termin.
        app.toggle_detail_pane()
        root.update()

        def detailknopf(item):
            auswaehlen(app.find_item_in_lists(item["id"])[0])
            app.tree.event_generate("<<TreeviewSelect>>")
            root.update()
            app.sync_detail_pane(force=True)
            root.update()
            return [w for w in descendants(app.detail_pane) if getattr(w, "text", None) == "Diesen Termin überspringen"]
        knopf = detailknopf(alle3)
        assert len(knopf) == 1 and knopf[0].winfo_ismapped(), knopf
        knopf[0].command()
        ruhe()
        assert app.find_item_in_lists(alle3["id"])[0]["due"] == tag(-4)
        app.undo_last_change()
        ruhe()
        assert not detailknopf(einmal), "Überspringen bei einer Aufgabe ohne Wiederholung"
        app.toggle_detail_pane()
        root.update()
        auswaehlen(app.find_item_in_lists(einmal["id"])[0])
        infos.clear()
        app.skip_missed_repeats_selected()
        assert infos and "keine Wiederholung" in infos[-1][1], infos
        aktionen = {eintrag["id"] for eintrag in app.app_action_entries()}
        assert {"skip_repeat_selected", "skip_missed_repeats_selected"} <= aktionen
        pruefungen.append("KO02: „Verpasste Termine“ springt auf den ersten Termin ab heute; "
                          "Mehrfachauswahl ein Schritt; Detailbereich, Menüleiste und Befehlspalette")
        assert not any(gebucht), gebucht

        # --- Befund: „Als erledigt markieren“ in einer Übersicht -------------
        app.set_today_view()
        ruhe()
        zeile = f"in-progress:{arbeit['id']}:{woche['id']}"
        assert app.tree.exists(zeile), app.tree.get_children("")
        menu = app.build_in_progress_context_menu(zeile)
        bisher = len(gebucht)
        menu.invoke(eintraege(menu)["Als erledigt markieren"])
        ruhe()
        woche = app.find_item_in_lists(woche["id"])[0]
        assert woche["due"] == tag(7) and not woche.get("done"), woche  # vorgerückt wie in der Liste
        assert sum(gebucht[bisher:]) == 1, gebucht[bisher:]  # die Tageszahl zählt genau einmal
        app.undo_last_change()
        ruhe()
        assert app.find_item_in_lists(woche["id"])[0]["due"] == tag(0)
        pruefungen.append("Übersicht: „Als erledigt markieren“ rückt Wiederholungen vor und bucht wie in der Liste")

        # --- KO03: Erinnerung aus der Schnelleingabe --------------------------
        app.set_active_list(arbeit["id"])
        ruhe()

        def eingeben(text):
            app.entry.focus_set()
            app.clear_entry_placeholder()
            app.entry.delete(0, "end")
            app.entry.insert(0, text)
            app.update_slash_hint()
            root.update()
            chips = [w.cget("text") for w in descendants(app._capture_hint) if isinstance(w, mod.tk.Label)]
            app.add_item()
            ruhe(0.05)
            return app.items[-1], chips

        neu, chips = eingeben("Bericht schreiben erinnere morgen 9:00")
        assert neu["text"] == "Bericht schreiben", neu["text"]
        def fest(tag_iso, uhr):
            return app.reminder_config({"mode": "fixed", "at": app.local_reminder_time(tag_iso, uhr)})
        assert neu["reminder"] == fest(tag(1), "09:00"), neu["reminder"]
        assert not neu.get("due") and not neu.get("planned_date"), neu
        assert any("nur bei laufender Glide" in text for text in chips), chips
        neu, chips = eingeben("Abgabe fällig morgen 14:00 Erinnerung 30 min vorher")
        assert (neu["text"], neu["due"], neu["due_time"]) == ("Abgabe", tag(1), "14:00"), neu
        assert neu["reminder"] == {"mode": "relative", "minutes": 30}, neu["reminder"]
        # „morgen“ ohne „fällig“ ist der Bearbeitungstag (D01): ein Vorlauf bleibt dann Text.
        neu, chips = eingeben("Abgabe morgen Erinnerung 30 min vorher")
        assert neu["planned_date"] == tag(1) and not neu.get("reminder"), neu
        neu, chips = eingeben("Anruf erinnerung 30 min vorher")
        assert not neu.get("reminder") and "erinnerung 30 min vorher" in neu["text"], neu
        assert any("braucht eine Fälligkeit" in text for text in chips), chips
        neu = app.capture_item("Zahnarzt /erinnern 9:00", arbeit["id"])
        assert neu["reminder"] == fest(tag(0), "09:00"), neu["reminder"]
        pruefungen.append("KO03: feste Erinnerung und Vorlauf aus Eingabezeile und Schnellerfassung; "
                          "Vorlauf ohne Fälligkeit bleibt Text mit Hinweis")

        # --- KO05: Mehrere Zeilen einfügen -----------------------------------
        root.clipboard_clear()
        root.clipboard_append("- [ ] Milch\n- [x] Brot\n\n3. Eier /wichtig\n")
        fragen = []

        def waehle(antwort):
            def dialog(titel, text, choices, item_colors=None):
                fragen.append((titel, text, [wert for wert, _ in choices]))
                return antwort
            return dialog
        app.clear_entry_text()
        app.entry.focus_set()
        vorher, tiefe = len(app.items), len(app.undo_stack)
        with patch.object(app, "themed_choice_dialog", side_effect=waehle("einzeln")):
            app.entry.event_generate("<<Paste>>")
            ruhe(0.05)
        assert fragen and "3 Zeilen" in fragen[-1][1], fragen
        assert [i["text"] for i in app.items[vorher:]] == ["Milch", "Brot", "Eier"], app.items[vorher:]
        assert [bool(i["done"]) for i in app.items[vorher:]] == [False, True, False]
        assert app.items[-1]["importance"] == 3 and app.entry.get() in ("", app.entry_placeholder_text), app.entry.get()
        assert len(app.undo_stack) == tiefe + 1
        app.undo_last_change()
        ruhe(0.05)
        assert len(app.items) == vorher
        app.clear_entry_text()
        with patch.object(app, "themed_choice_dialog", side_effect=waehle("eine")):
            app.entry.event_generate("<<Paste>>")
        assert app.entry.get() == "Milch, Brot, Eier /wichtig" and len(app.items) == vorher, app.entry.get()
        app.clear_entry_text()
        with patch.object(app, "themed_choice_dialog", side_effect=waehle(None)):
            app.entry.event_generate("<<Paste>>")
        assert app.entry.get() == "" and len(app.items) == vorher
        root.clipboard_clear()
        root.clipboard_append("Nur eine Zeile")
        anzahl = len(fragen)
        app.entry.event_generate("<<Paste>>")
        root.update()
        assert len(fragen) == anzahl and app.entry.get() == "Nur eine Zeile", app.entry.get()
        app.clear_entry_text()
        pruefungen.append("KO05: Rückfrage bei mehreren Zeilen – einzeln (ein Undo-Schritt), als eine Aufgabe, "
                          "Abbrechen; eine Zeile fügt normal ein")

        # --- KO06: zuletzt benutzte Ziele vorn --------------------------------
        for name in ("Alpha", "Beta", "Gamma"):
            app.labels.append(app.new_label_object(name))
        app.save_items()
        gamma = next(label for label in app.labels if label["name"] == "Gamma")
        ziel_a = app.new_list_object("Ziel A", [])
        ziel_b = app.new_list_object("Ziel B", [])
        app.lists.extend([ziel_a, ziel_b])
        app.save_items()
        app.set_active_list(arbeit["id"])
        ruhe()
        einmal = app.find_item_in_lists(einmal["id"])[0]
        auswaehlen(einmal)
        app.toggle_label_on_selected_items(gamma["id"])
        assert app.settings["recent_labels"][0] == gamma["id"]
        auswaehlen(app.find_item_in_lists(einmal["id"])[0])
        menu = app.build_item_context_menu()
        labels = menu.nametowidget(menu.entrycget(eintraege(menu)["Labels"], "menu"))
        assert labels.entrycget(0, "label").strip(" ✓–") == "Gamma" and labels.type(1) == "separator", \
            [labels.entrycget(i, "label") for i in range(labels.index("end") + 1) if labels.type(i) != "separator"]
        ziele = []

        def verschieben(titel, text, choices, item_colors=None):
            ziele.append([wert for wert, _ in choices])
            return ziel_b["id"] if len(ziele) == 1 else None
        schreiben = app.write_json_atomic
        geschrieben = []
        app.write_json_atomic = lambda pfad, daten, *a, **k: (geschrieben.append(os.path.basename(pfad)),
                                                              schreiben(pfad, daten, *a, **k))[1]
        with patch.object(app, "themed_choice_dialog", side_effect=verschieben):
            auswaehlen(app.find_item_in_lists(einmal["id"])[0])
            app.move_selected_to_list_dialog()
            ruhe()
            assert geschrieben.count("settings.json") <= 1, geschrieben
            auswaehlen(app.find_item_in_lists(woche["id"])[0])
            app.move_selected_to_list_dialog()
        app.write_json_atomic = schreiben
        assert ziele[0].index(ziel_a["id"]) < ziele[0].index(ziel_b["id"]) and ziele[1][0] == ziel_b["id"], ziele
        assert app.settings["recent_move_targets"][0] == ziel_b["id"]
        pruefungen.append("KO06: zuletzt benutztes Label und Verschiebeziel stehen vorn; ein Einstellungsschreiben")

        # --- U04: „+“ und Umschalt+Enter --------------------------------------
        assert app.add_button.text == "+" and app.add_button.command == app.add_item
        assert not app.advanced_add_button.winfo_ismapped()
        geoeffnet = []
        with patch.object(app, "add_item_advanced", side_effect=lambda *a: geoeffnet.append(True)):
            app.entry.focus_force()
            root.update()
            app.entry.event_generate("<Shift-Return>")
            root.update()
        assert geoeffnet, "Umschalt+Enter öffnet die erweiterte Eingabe nicht"
        # Ohne Dauerknopf bleibt ein Menü- und Palettenweg zur vollständigen Maske.
        erweitert = next(eintrag for eintrag in app.app_action_entries() if eintrag["id"] == "add_item_advanced")
        assert erweitert["label"] == "Neuer Punkt mit allen Angaben …" and erweitert["group"] == "Neu anlegen", erweitert
        vorher = len(app.items)
        app.clear_entry_placeholder()
        app.entry.insert(0, "Über den Plusknopf")
        app.add_button.command()
        ruhe(0.05)
        assert len(app.items) == vorher + 1 and app.items[-1]["text"] == "Über den Plusknopf"
        pruefungen.append("U04: runder „+“-Knopf legt an, Umschalt+Enter und Datei › Neu anlegen öffnen die Maske, "
                          "„Erweitert“ entfällt als Dauerknopf")

        # --- U20: ein Anlegeweg je Leerzustand --------------------------------
        leer = app.new_list_object("Leer", [])
        app.lists.append(leer)
        app.save_items()
        app.set_active_list(leer["id"])
        ruhe()
        assert app.entry_line_visible()
        assert app.empty_state_action() is None, app.empty_state_action()
        app.set_table_view()
        ruhe()
        assert app.entry_line_visible() and app.empty_state_action() is None, app.empty_state_action()
        app.set_active_list(leer["id"])
        app.search_var.set("gibt es nicht")
        ruhe()
        assert app.empty_state_action()[0] == "Suche zurücksetzen", app.empty_state_action()
        app.search_var.set("")
        ruhe()
        mappe = app.new_folder_object("Leerer Ordner")
        buch = app.new_folder_object("Tagebuch", folder_kind="journal")
        app.folders.extend([mappe, buch])
        app.save_items()
        app.set_active_folder(mappe["id"])
        ruhe()
        assert app.entry_line_visible() and app.empty_state_action() is None, app.empty_state_action()
        app.set_active_folder(buch["id"])
        ruhe()
        assert app.empty_state_action()[0] == "Ersten Eintrag anlegen", app.empty_state_action()
        app.set_trash_view()
        ruhe()
        assert not app.entry_line_visible() and app.empty_state_action()[0] == "Zur Startseite"
        pruefungen.append("U20: Inventar der Leerzustände – Liste, Tabelle und Ordner ohne zweiten Anlegeknopf, "
                          "Notizbuch, Papierkorb und Suche behalten ihre Aktion")

        # --- AU06: Routinen in „Heute“ ----------------------------------------
        routine = app.new_list_object("Morgenroutine", [app.new_item("Wasser trinken"), app.new_item("Strecken"),
                                                         app.new_item("Tag planen", due=tag(0))])
        app.lists.append(routine)
        app.save_items()
        menue = eintraege(app.build_list_menu(routine["id"]))
        assert "In Heute als Routine zeigen" not in menue  # nur für wiederkehrende Checklisten
        app.set_recurring_checklist(routine["id"], True)
        menu = app.build_list_menu(routine["id"])
        menu.invoke(eintraege(menu)["In Heute als Routine zeigen"])
        ruhe()  # Menübefehle laufen nach dem Schließen des Menüs
        assert app.settings["today_routines"] == [routine["id"]], (app.settings.get("today_routines"), fehler, toasts[-2:])
        app.set_today_view()
        ruhe()
        kopf = app.ROUTINE_ROW_PREFIX + routine["id"]
        assert app.ROUTINES_SECTION_ROW_ID in app.tree.get_children(""), app.tree.get_children("")
        assert "Routinen · 1" in app.tree.item(app.ROUTINES_SECTION_ROW_ID, "text")
        assert app.tree.item(kopf, "text") == "Morgenroutine · 0/3", app.tree.item(kopf, "text")
        punkte = [f"in-progress:{routine['id']}:{item['id']}" for item in routine["items"]]
        # „Tag planen“ ist heute fällig und steht oben – nicht doppelt.
        assert list(app.tree.get_children(kopf)) == punkte[:2], app.tree.get_children(kopf)
        assert punkte[2] in app.tree.get_children(app.DUE_TODAY_SECTION_ROW_ID)
        app.toggle_item_done_anywhere(routine["items"][0]["id"])
        ruhe()
        assert app.tree.item(kopf, "text") == "Morgenroutine · 1/3"
        with patch.object(app, "CHECKLIST_RESET_DELAY_MS", 10):
            app.toggle_item_done_anywhere(routine["items"][1]["id"])
            app.toggle_item_done_anywhere(routine["items"][2]["id"])
            ruhe(0.4)
        routine = next(entry for entry in app.lists if entry["id"] == routine["id"])
        assert not any(item.get("done") for item in routine["items"]), "Routine öffnet sich nicht wieder"
        assert app.settings["routine_done_days"] == {routine["id"]: tag(0)}, app.settings.get("routine_done_days")
        app.set_today_view()
        ruhe()
        assert "heute schon einmal erledigt" in app.tree.item(kopf, "text"), app.tree.item(kopf, "text")
        app.tree.focus(kopf)
        app.open_in_progress_source_item()
        ruhe()
        assert app.view_mode == "list" and app.active_list_id == routine["id"]
        app.toggle_today_routine(routine["id"])
        app.set_today_view()
        ruhe()
        assert app.ROUTINES_SECTION_ROW_ID not in app.tree.get_children("")
        pruefungen.append("AU06: Routine über das Listenmenü in „Heute“, Fortschritt, kein Doppel, "
                          "Durchgang gemerkt, Doppelklick öffnet, abwählbar")

        # --- N07: Karte „Neu in …“ ---------------------------------------------
        rn = mod.glide_release

        def karte():
            app.set_home_view()
            ruhe(0.1)
            return [w for w in descendants(app.home_content)
                    if isinstance(w, mod.tk.Label) and str(w.cget("text")).endswith(f"Neu in Glide {mod.APP_VERSION}")]
        assert not karte(), "Karte beim Erststart"
        assert app.settings.get("release_notes_seen") == mod.APP_VERSION  # Erststart: nur merken
        app._settings_existed = True
        app.settings.pop("release_notes_seen")
        app.save_settings()
        erwartet = rn.notes_since(rn.BEFORE_CATALOG, mod.APP_VERSION)
        assert erwartet, "Katalog ohne Eintrag für die laufende Version"
        assert karte(), "Karte fehlt nach einem Update"
        texte = [str(w.cget("text")) for w in descendants(app.home_content) if isinstance(w, mod.tk.Label)]
        for _version, punkte in erwartet:
            for punkt in punkte:
                assert f"• {punkt}" in texte, punkt
        gelesen = next(w for w in descendants(app.home_content) if getattr(w, "text", None) == "Gelesen")
        gelesen.command()
        ruhe(0.1)
        assert app.settings["release_notes_seen"] == mod.APP_VERSION and not karte()
        pruefungen.append("N07: Karte nur nach Update, alle Punkte der neuen Versionen, „Gelesen“ merkt die Version")

        # --- AB08: zu alte Laufzeit vor jedem Datenzugriff abweisen --------------
        laufzeit = mod.glide_runtime
        assert laufzeit.python_status((3, 11, 9))[0] == "zu_alt"
        assert laufzeit.python_status((3, 13, 1))[0] == "eingeschränkt"
        assert laufzeit.tk_status(8.5)[0] == "zu_alt" and laufzeit.tk_status(mod.tk.TkVersion)[0] != "zu_alt"
        altes = Path("/usr/bin/python3")
        start = args.app.parent / "glide_start.py"
        if altes.exists() and subprocess.run([str(altes), "-c", "import sys; sys.exit(sys.version_info < (3, 12))"]
                                             ).returncode:
            leer_ordner = Path(ordner) / "ab08"
            ergebnis = subprocess.run(
                [str(altes), "-B", "-c",
                 "import sys, runpy; sys.path.insert(0, sys.argv[1]); import runtime_check;"
                 "runtime_check.melden = lambda t: sys.stderr.write(t);"
                 "sys.argv = [sys.argv[2]]; runpy.run_path(sys.argv[0], run_name='__main__')",
                 str(start.parent), str(start)],
                capture_output=True, text=True, timeout=60,
                env=dict(os.environ, GLIDE_DATA_DIR=str(leer_ordner), PYTHONPYCACHEPREFIX=str(Path(ordner) / "cache")))
            assert ergebnis.returncode == 1 and "Python 3.12 oder neuer" in ergebnis.stderr, ergebnis
            assert not leer_ordner.exists(), "Datenordner vor der Prüfung angelegt"
            pruefungen.append("AB08: glide_start weist ein altes Python ab, bevor der Datenordner entsteht")
        else:
            pruefungen.append("AB08: Stufen geprüft (kein altes Python für die Startprobe vorhanden)")
        assert "pycache_prefix" in start.read_text(encoding="utf-8").split("import runtime_check")[0]

        # --- Neustart aus den gespeicherten Dateien -----------------------------
        app.skip_repeat_occurrences([alle3["id"]])
        app.toggle_today_routine(routine["id"])
        ruhe()
        assert not fehler, fehler
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
        root = mod.tk.Tk()
        root.geometry("1280x840+20+20")
        root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
        app = mod.ListApp(root)
        app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
        app.show_info = lambda *a, **k: infos.append(a)
        ruhe()
        assert app.find_item_in_lists(alle3["id"])[0]["due"] == tag(-4)
        assert app.settings["today_routines"] == [routine["id"]]
        assert app.settings["routine_done_days"] == {routine["id"]: tag(0)}
        assert app.settings["recent_labels"][0] == gamma["id"] and app.settings["recent_move_targets"][0] == ziel_b["id"]
        assert app._settings_existed and not karte(), "Karte nach Neustart erneut"
        app.set_today_view()
        ruhe()
        assert "heute schon einmal erledigt" in app.tree.item(kopf, "text"), app.tree.item(kopf, "text")
        pruefungen.append("Neustart: übersprungener Termin, Routinen, zuletzt benutzte Ziele und gelesene Karte bleiben")

        # Beschädigte Einstellungen: neue Schlüssel fallen auf das frühere Verhalten zurück.
        normal = mod.ListApp.normalize_settings_330({
            "today_routines": 5, "routine_done_days": [1], "recent_labels": "x",
            "recent_move_targets": [3, "a", "a"], "release_notes_seen": 7})
        assert (normal["today_routines"], normal["routine_done_days"], normal["recent_labels"],
                normal["recent_move_targets"]) == ([], {}, [], ["a"]), normal
        assert "release_notes_seen" not in normal
        pruefungen.append("Einstellungen: neue Schlüssel normalisiert, Unlesbares ergibt das frühere Verhalten")

        ruhe(0.2)
        assert not fehler, fehler
        print("test_komfort33320: OK; " + "; ".join(pruefungen))
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
