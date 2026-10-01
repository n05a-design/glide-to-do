"""Kalenderausgabe: Umfänge, Termine, Wiederholungen, Alarme, Format, Grenzen, Dialog."""
import copy
import importlib.machinery
import importlib.util
import os
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def bloecke(text):
    """Die VEVENT-Blöcke einer ICS-Datei als Liste entfalteter Zeilenlisten."""
    zeilen = []
    for rohzeile in text.split("\r\n"):
        if rohzeile.startswith(" ") and zeilen:
            zeilen[-1] += rohzeile[1:]
        else:
            zeilen.append(rohzeile)
    ergebnis, aktuell = [], None
    for zeile in zeilen:
        if zeile == "BEGIN:VEVENT":
            aktuell = []
        elif zeile == "END:VEVENT":
            ergebnis.append(aktuell or [])
            aktuell = None
        elif aktuell is not None:
            aktuell.append(zeile)
    return ergebnis


def wert(block, name):
    for zeile in block:
        if zeile.startswith(name + ":") or zeile.startswith(name + ";"):
            return zeile.split(":", 1)[1]
    return None


def block_mit(bloecke_liste, text):
    return next((b for b in bloecke_liste if text in (wert(b, "SUMMARY") or "")), None)


with tempfile.TemporaryDirectory(prefix="glide-features320-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features320", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    callbacks = []
    root.report_callback_exception = lambda *args: callbacks.append(args)
    app = mod.ListApp(root)
    meldungen = []
    app.show_warning = app.show_error = lambda *args, **kwargs: meldungen.append(args)
    infos = []
    app.show_info = lambda *args, **kwargs: infos.append(args)
    app.ask_yes_no = lambda *args, **kwargs: True
    geoeffnet = []
    app.open_external_path = lambda pfad: geoeffnet.append(pfad) or True
    A = mod.ListApp
    try:
        heute = date.today().isoformat()
        morgen = (date.today() + timedelta(days=1)).isoformat()
        assert A.MAX_ICS_EVENTS == 2000 and A.ICS_DEFAULT_MINUTES == 30
        assert [key for key, _text in A.ICS_SCOPES] == ["list", "all", "today", "planday"]
        assert A.ICS_WEEKDAYS[0] == "MO" and A.ICS_WEEKDAYS[6] == "SU"

        # --- Bestand mit allen Merkmalen -------------------------------------
        liste = app.new_list_object("Termine, Fristen; Prüfung", [])
        mit_zeit = app.new_item("Zählerstand & Ablesung", due=heute, due_time="09:30",
                                estimated_minutes=45, importance=3, planned_date=morgen)
        mit_zeit["description"] = "Zeile eins\nZeile zwei; mit Komma, und Semikolon"
        ganztag = app.new_item("Ganztägig fällig", due=heute, importance=1)
        ohne_frist = app.new_item("Ohne Frist")
        erledigt = app.new_item("Schon fertig", due=heute)
        erledigt["done"] = True
        serie = app.new_item("An Wochentagen", due=heute,
                             repeat={"art": A.REPEAT_WEEKDAYS, "tage": [0, 2, 4], "ende": "2027-01-31"})
        erinnerung = app.new_item("Mit Erinnerung", due=heute, due_time="14:00",
                                  reminder={"mode": "relative", "minutes": 30})
        gruppe = app.new_item("Gliederung", kind=A.ITEM_KIND_GROUP)
        gruppe["children"] = [app.new_item("Unterpunkt mit Frist", due=heute)]
        liste["items"] = [mit_zeit, ganztag, ohne_frist, erledigt, serie, erinnerung, gruppe]
        app.lists.append(liste)
        app.set_active_list(liste["id"])
        etikett = app.ensure_label_by_name("Vor Ort")
        mit_zeit["labels"] = list(mit_zeit.get("labels") or []) + [etikett["id"]]
        assert app.save_items()

        # --- 1. Grundaufbau aller vier Umfänge -------------------------------
        for key, _text in A.ICS_SCOPES:
            text, bericht = app.build_ics_document(key, day=heute)
            assert text.startswith("BEGIN:VCALENDAR\r\n"), key
            assert text.rstrip().endswith("END:VCALENDAR"), key
            assert "VERSION:2.0" in text and "PRODID:-//Glide//" in text, key
            assert mod.APP_VERSION in text and "CALSCALE:GREGORIAN" in text, key
            assert text.endswith("\r\n"), key
            assert "\n" not in text.replace("\r\n", ""), (key, "nur CRLF als Zeilenende")
            assert "" not in text.split("\r\n")[:-1], (key, "keine Leerzeilen")
            assert all(len(zeile.encode("utf-8")) <= A.ICS_LINE_LIMIT
                       for zeile in text.split("\r\n")), key
        try:
            app.build_ics_document("unbekannt")
        except ValueError:
            pass
        else:
            raise AssertionError("Ein unbekannter Umfang wurde angenommen")

        # --- 2. Termin mit Uhrzeit und Ganztagstermin ------------------------
        text, bericht = app.build_ics_document("list")
        einzeln = bloecke(text)
        assert bericht["events"] == len(einzeln) == 5, bericht  # ohne Frist und erledigt bleiben draußen
        assert bericht["skipped"] == 1 and not bericht["truncated"], bericht
        zeit_block = block_mit(einzeln, "Zählerstand")
        assert wert(zeit_block, "DTSTART") == heute.replace("-", "") + "T093000"
        assert wert(zeit_block, "DTEND") == heute.replace("-", "") + "T101500", "45 Minuten Aufwand"
        assert wert(zeit_block, "PRIORITY") == "1"
        assert wert(zeit_block, "CATEGORIES") == "Vor Ort"
        assert wert(zeit_block, "UID") == f"glide-{mit_zeit['id']}@{A.ICS_UID_DOMAIN}"
        assert "SEQUENCE:0" in zeit_block and any(z.startswith("DTSTAMP:") for z in zeit_block)
        ganz_block = block_mit(einzeln, "Ganztägig")
        assert "DTSTART;VALUE=DATE:" + heute.replace("-", "") in ganz_block
        assert "DTEND;VALUE=DATE:" + (date.today() + timedelta(days=1)).strftime("%Y%m%d") in ganz_block
        assert wert(ganz_block, "PRIORITY") == "9", "niedrig wird 9"
        assert block_mit(einzeln, "Ohne Frist") is None
        assert block_mit(einzeln, "Schon fertig") is None
        assert block_mit(einzeln, "Gliederung") is None, "Gruppen tragen keine Fälligkeit"
        assert block_mit(einzeln, "Unterpunkt mit Frist") is not None, "Unterpunkte erscheinen"

        # --- 3. Escaping und Zeilenfaltung -----------------------------------
        beschreibung = wert(zeit_block, "DESCRIPTION")
        assert "\\n" in beschreibung and "\\;" in beschreibung and "\\," in beschreibung
        assert "\n" not in beschreibung
        assert "Termine\\, Fristen\\; Prüfung" in text, "Auch der Kalendername wird escaped."
        lang = app.new_item("Ü" * 300, due=heute)
        liste["items"].append(lang)
        assert app.save_items()
        text_lang, _b = app.build_ics_document("list")
        assert all(len(zeile.encode("utf-8")) <= A.ICS_LINE_LIMIT for zeile in text_lang.split("\r\n"))
        entfaltet = block_mit(bloecke(text_lang), "Ü" * 50)
        assert entfaltet is not None and wert(entfaltet, "SUMMARY") == "Ü" * 300, "Faltung ist umkehrbar"
        liste["items"].remove(lang)
        assert app.save_items()

        # --- 4. Optionen wirken einzeln --------------------------------------
        aus = {key: False for key, _text in A.ICS_OPTION_LABELS}
        schlicht, bericht_aus = app.build_ics_document("list", aus)
        schlicht_block = block_mit(bloecke(schlicht), "Zählerstand")
        assert "CATEGORIES:" not in schlicht
        assert "Zeile eins" not in schlicht
        assert wert(schlicht_block, "DTEND") == heute.replace("-", "") + "T100000", "ohne Aufwand 30 Minuten"
        assert "BEGIN:VALARM" not in schlicht
        assert block_mit(bloecke(schlicht), "Planung:") is None
        mit_done = app.build_ics_document("list", dict(aus, done=True))[0]
        assert block_mit(bloecke(mit_done), "Erledigt: Schon fertig") is not None
        assert "Zeile eins" in app.build_ics_document("list", dict(aus, description=True))[0]
        assert "CATEGORIES:Vor Ort" in app.build_ics_document("list", dict(aus, labels=True))[0]
        assert "BEGIN:VALARM" in app.build_ics_document("list", dict(aus, alarms=True))[0]
        mit_plan, plan_bericht = app.build_ics_document("list", dict(aus, planned=True))
        plan_block = block_mit(bloecke(mit_plan), "Planung: Zählerstand")
        assert plan_block is not None and plan_bericht["events"] == bericht_aus["events"] + 1
        assert wert(plan_block, "UID") == f"glide-{mit_zeit['id']}-plan@{A.ICS_UID_DOMAIN}"
        assert "DTSTART;VALUE=DATE:" + morgen.replace("-", "") in plan_block
        assert "RRULE" not in " ".join(plan_block), "Ein Bearbeitungstag wiederholt sich nicht."

        # --- 5. Wiederholungen ------------------------------------------------
        for regel, erwartet in (
            ({"art": A.REPEAT_DAILY}, "FREQ=DAILY"),
            ({"art": A.REPEAT_EVERY_N_DAYS, "abstand": 3}, "FREQ=DAILY;INTERVAL=3"),
            ({"art": A.REPEAT_WEEKDAYS, "tage": [0, 2, 4]}, "FREQ=WEEKLY;BYDAY=MO,WE,FR"),
            ({"art": A.REPEAT_WEEKLY}, "FREQ=WEEKLY"),
            ({"art": A.REPEAT_MONTHLY}, "FREQ=MONTHLY"),
            ({"art": A.REPEAT_YEARLY}, "FREQ=YEARLY"),
        ):
            probe = app.new_item("Serienprobe", due=heute, repeat=dict(regel))
            assert app.ics_repeat_rule(probe) == erwartet, (regel, app.ics_repeat_rule(probe))
        mit_ende = app.new_item("Mit Ende", due=heute,
                                repeat={"art": A.REPEAT_DAILY, "ende": "2027-03-01"})
        # UNTIL trägt dieselbe Zeitform wie DTSTART: schwebende Ortszeit ohne
        # „Z" beim Uhrzeittermin, reines Datum beim Ganztagstermin. Ein „Z"
        # wäre UTC und verschöbe das Enddatum beim Wiedereinlesen um einen
        # Tag – in 3.21.0 war genau das der Fall.
        assert app.ics_repeat_rule(mit_ende) == "FREQ=DAILY;UNTIL=20270301T235959"
        assert app.ics_repeat_rule(mit_ende, ganztaegig=True) == "FREQ=DAILY;UNTIL=20270301"
        assert app.ics_repeat_rule(app.new_item("Ohne", due=heute)) is None
        serien_block = block_mit(einzeln, "An Wochentagen")
        assert "Z" not in wert(serien_block, "RRULE"), "UNTIL darf nicht in UTC stehen."

        # --- 6. Erinnerungen --------------------------------------------------
        alarm_block = block_mit(einzeln, "Mit Erinnerung")
        assert "BEGIN:VALARM" in alarm_block and "ACTION:DISPLAY" in alarm_block
        assert "TRIGGER:-PT30M" in alarm_block
        fest = app.new_item("Feste Erinnerung", due=morgen, due_time="08:00")
        fest["reminder"] = {"mode": "fixed", "at": app.local_reminder_time(morgen, "07:15")}
        liste["items"].append(fest)
        assert app.save_items()
        fest_block = block_mit(bloecke(app.build_ics_document("list")[0]), "Feste Erinnerung")
        trigger = next(z for z in fest_block if z.startswith("TRIGGER"))
        assert trigger.startswith("TRIGGER;VALUE=DATE-TIME:") and trigger.endswith("Z")
        assert app.ics_alarm_lines(app.new_item("Ohne Erinnerung", due=heute)) == []

        # --- 7. Umfänge liefern die richtigen Mengen -------------------------
        app.update_today_plan([mit_zeit["id"]], add=True)
        assert app.save_items()
        heute_text, heute_bericht = app.build_ics_document("today")
        assert block_mit(bloecke(heute_text), "Zählerstand") is not None
        # Derselbe Punkt steht in „Mein Tag" und „Heute fällig" – und erscheint einmal.
        assert len([b for b in bloecke(heute_text) if "Zählerstand" in (wert(b, "SUMMARY") or "")]) == 1
        plan_text, _b = app.build_ics_document("planday", day=morgen)
        assert bloecke(plan_text) == [] or all("Planung" not in (wert(b, "SUMMARY") or "")
                                               for b in bloecke(plan_text))
        zweite = app.new_list_object("Zweite Liste", [app.new_item("Aus Liste zwei", due=heute)])
        app.lists.append(zweite)
        assert app.save_items()
        alle_text, alle_bericht = app.build_ics_document("all")
        assert block_mit(bloecke(alle_text), "Aus Liste zwei") is not None
        assert block_mit(bloecke(alle_text), "Zählerstand") is not None
        assert "alle Listen" in alle_text
        nur_liste = app.build_ics_document("list")[0]
        assert block_mit(bloecke(nur_liste), "Aus Liste zwei") is None
        # Der Ordnerfall fasst die enthaltenen Listen zusammen.
        ordner = app.new_folder_object("Objekte", color="accent")
        app.folders.append(ordner)
        liste["folder_id"] = ordner["id"]
        zweite["folder_id"] = ordner["id"]
        assert app.save_items()
        app.set_active_folder(ordner["id"])
        ordner_text, _b = app.build_ics_document("list")
        assert block_mit(bloecke(ordner_text), "Aus Liste zwei") is not None
        assert block_mit(bloecke(ordner_text), "Zählerstand") is not None
        app.set_active_list(liste["id"])

        # --- 8. Obergrenze ----------------------------------------------------
        gross = app.new_list_object("Massenprobe", [app.new_item(f"Punkt {n}", due=heute)
                                                    for n in range(A.MAX_ICS_EVENTS + 30)])
        app.lists.append(gross)
        app.set_active_list(gross["id"])
        assert app.save_items()
        begrenzt, grenz_bericht = app.build_ics_document("list")
        assert grenz_bericht["events"] == A.MAX_ICS_EVENTS and grenz_bericht["truncated"]
        assert len(bloecke(begrenzt)) == A.MAX_ICS_EVENTS
        assert str(A.MAX_ICS_EVENTS) in begrenzt
        app.set_active_list(liste["id"])

        # --- 9. Datei schreiben ------------------------------------------------
        ziel = os.path.join(folder, "unterordner", "termine.ics")
        pfad, datei_bericht = app.write_ics_document(ziel, "list")
        assert os.path.isfile(pfad) and pfad == os.path.abspath(ziel)
        inhalt = Path(pfad).read_bytes().decode("utf-8")
        assert inhalt.startswith("BEGIN:VCALENDAR") and "\r\n" in inhalt
        assert datei_bericht["events"] > 0
        assert not list(Path(os.path.dirname(pfad)).glob(".glide-ics-*")), "Temporärdatei blieb liegen."
        # Zwei Ausgaben desselben Punkts tragen dieselbe UID.
        zweite_ausgabe = app.build_ics_document("list")[0]
        uid_eins = wert(block_mit(bloecke(inhalt), "Zählerstand"), "UID")
        uid_zwei = wert(block_mit(bloecke(zweite_ausgabe), "Zählerstand"), "UID")
        assert uid_eins == uid_zwei and uid_eins
        vorher = copy.deepcopy(app.data_payload())
        verlauf_vorher = len(app.history)
        app.write_ics_document(ziel, "all")
        assert app.data_payload() == vorher, "Die Ausgabe verändert keine Daten."
        assert len(app.history) == verlauf_vorher, "Eine Ausgabe ist kein Verlaufsereignis."
        try:
            app.write_ics_document(mod.SAVE_FILE, "list")
        except ValueError:
            pass
        else:
            raise AssertionError("Die Nutzdatendatei wurde als Ziel akzeptiert")

        # --- 10. Dialog in Hell und Dunkel ------------------------------------
        root.deiconify()
        root.geometry("1100x780+10+10")
        for theme in ("light", "dark"):
            app.theme_name = theme
            app.apply_theme()
            geoeffnet.clear()
            infos.clear()
            dialogziel = os.path.join(folder, f"dialog_{theme}.ics")
            mod.filedialog.asksaveasfilename = lambda *args, **kwargs: dialogziel

            def ausgeben(dialog, parent=None):
                dialog.geometry("780x640")
                dialog.update()
                widgets = list(descendants(dialog))
                haken = {key: next(w for w in widgets if w.winfo_name() == "ics_" + key)
                         for key, _text in A.ICS_OPTION_LABELS}
                assert all(str(w.cget("state")) != "disabled" for w in haken.values())
                haken["planned"].invoke()
                knopf = next(w for w in widgets if isinstance(w, mod.RoundedButton)
                             and w.text == "Speichern und öffnen")
                assert knopf.winfo_ismapped()
                assert (knopf.winfo_rooty() + knopf.winfo_height()
                        <= dialog.winfo_rooty() + dialog.winfo_height())
                knopf.command()
            app.run_modal = ausgeben
            assert app.show_calendar_export_dialog() == "break"
            assert len(geoeffnet) == 1 and geoeffnet[0] == os.path.abspath(dialogziel)
            # read_bytes: read_text würde CRLF zu LF vereinheitlichen und die
            # Blockzerlegung unbrauchbar machen.
            geschrieben = Path(dialogziel).read_bytes().decode("utf-8")
            assert "BEGIN:VCALENDAR" in geschrieben
            assert block_mit(bloecke(geschrieben), "Planung:") is not None, "Die Option wirkt."
            assert infos and "Termin" in infos[-1][1]

            def abbrechen(dialog, parent=None):
                dialog.update()
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)
                     and w.text == "Abbrechen").command()
            app.run_modal = abbrechen
            geoeffnet.clear()
            zustand = copy.deepcopy(app.data_payload())
            app.show_calendar_export_dialog()
            assert not geoeffnet and app.data_payload() == zustand
        assert not callbacks, callbacks
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: Kalenderausgabe mit vier Umfängen, Optionen, Wiederholungen, Alarmen, Format, Grenzen und Dialog")
