"""Kalenderimport: Parser, Abbildung, Zeitzonen, Regeln, Duplikate, Ziele, Dialog."""
import copy
import importlib.machinery
import importlib.util
import os
import tempfile
import time
from datetime import date, datetime, timedelta
from pathlib import Path

# Die Suite läuft absichtlich NICHT in UTC. Ein Zeitzonenfehler im
# ICS-Rundlauf – etwa ein UNTIL, das als UTC geschrieben und als Ortszeit
# gelesen wird – bleibt in UTC unsichtbar, weil Versatz null ist. Genau so
# ist der Fehler in 3.21.0 durch die Linux-Vorabumgebung gerutscht und erst
# im macOS-Lauf aufgefallen. Vor dem Laden des Moduls gesetzt, damit auch
# der Modulzustand die Zone kennt.
os.environ["TZ"] = "Europe/Berlin"
if hasattr(time, "tzset"):  # POSIX; unter Windows gilt die Systemzone
    time.tzset()

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def kalender(*bloecke, name="Testkalender", zeilenende="\r\n"):
    """Eine ICS-Datei aus VEVENT-Rümpfen bauen."""
    zeilen = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Fremd//Test//EN",
              f"X-WR-CALNAME:{name}"]
    for block in bloecke:
        zeilen.append("BEGIN:VEVENT")
        zeilen.extend(block)
        zeilen.append("END:VEVENT")
    zeilen.append("END:VCALENDAR")
    return zeilenende.join(zeilen) + zeilenende


def schreibe(pfad, text, encoding="utf-8"):
    Path(pfad).write_bytes(text.encode(encoding))
    return str(pfad)


with tempfile.TemporaryDirectory(prefix="glide-features321-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features321", str(REPO / "src/glide/app.pyw"))
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
    A = mod.ListApp

    def lese(text, name="Testkalender", encoding="utf-8", datei="probe.ics"):
        pfad = schreibe(os.path.join(folder, datei), text, encoding)
        return app.read_ics_file(pfad)

    def punkte_aus(text, options=None, zeitraum="all", **kwargs):
        _kopf, ereignisse = lese(text, **kwargs)
        return app.ics_events_to_items(ereignisse, options, zeitraum, dry_run=True)

    try:
        heute = date.today()
        assert A.MAX_ICS_IMPORT_EVENTS == 2000
        assert [key for key, _text in A.ICS_IMPORT_OPTION_LABELS][:2] == ["description", "location"]

        # --- 1. Rundlauf über die eigene Ausgabe aus 3.20 --------------------
        quelle = app.new_list_object("Quelle", [])
        original = app.new_item("Zählerstand & Ablesung", due=heute.isoformat(), due_time="09:30",
                                estimated_minutes=45, importance=3)
        original["description"] = "Zeile eins\nmit Semikolon; und Komma,"
        serie = app.new_item("Serie", due=heute.isoformat(),
                             repeat={"art": A.REPEAT_WEEKDAYS, "tage": [0, 2], "ende": "2027-01-31"})
        alarm = app.new_item("Alarm", due=heute.isoformat(), due_time="14:00",
                             reminder={"mode": "relative", "minutes": 30})
        ganztag = app.new_item("Ganztägig", due=heute.isoformat())
        quelle["items"] = [original, serie, alarm, ganztag]
        app.lists.append(quelle)
        app.set_active_list(quelle["id"])
        etikett = app.ensure_label_by_name("Vor Ort")
        original["labels"] = list(original.get("labels") or []) + [etikett["id"]]
        assert app.save_items()
        eigene = os.path.join(folder, "eigene.ics")
        app.write_ics_document(eigene, "list")

        # Unveränderte eigene Datei: alle Termine gelten als Duplikate.
        kopf, ereignisse = app.read_ics_file(eigene)
        assert kopf["name"].startswith("Glide") and "Glide" in kopf["prodid"]
        assert len(ereignisse) == 4
        _punkte, bericht = app.ics_events_to_items(ereignisse, dry_run=True)
        assert bericht["items"] == 0 and bericht["skipped"].get("duplicate") == 4, bericht

        # Dieselbe Datei mit fremden UIDs – so käme sie von einem anderen Gerät.
        fremde_fassung = os.path.join(folder, "eigene_fremd.ics")
        text = Path(eigene).read_bytes().decode("utf-8")
        import re as _re
        text = _re.sub(r"UID:glide-[0-9a-f]+(-plan)?@glide\.local", "UID:fremd-kopie", text)
        Path(fremde_fassung).write_bytes(text.encode("utf-8"))
        kopf, ereignisse = app.read_ics_file(fremde_fassung)
        punkte, bericht = app.ics_events_to_items(ereignisse, dry_run=True)
        assert bericht["items"] == 4 and not bericht["skipped"], bericht
        nach_text = {punkt["text"]: punkt for punkt in punkte}
        zurueck = nach_text["Zählerstand & Ablesung"]
        assert zurueck["due"] == heute.isoformat() and zurueck["due_time"] == "09:30"
        assert zurueck["estimated_minutes"] == 45 and zurueck["importance"] == 3
        assert zurueck["description"].startswith("Zeile eins\nmit Semikolon; und Komma,")
        assert "Aus: Quelle" in zurueck["description"], "Die Exportangaben bleiben lesbar."
        assert nach_text["Ganztägig"]["due"] == heute.isoformat()
        assert nach_text["Ganztägig"]["due_time"] is None
        assert app.normalize_repeat(nach_text["Serie"]["repeat"])["art"] == A.REPEAT_WEEKDAYS
        assert app.normalize_repeat(nach_text["Serie"]["repeat"])["tage"] == [0, 2]
        assert app.normalize_repeat(nach_text["Serie"]["repeat"])["ende"] == "2027-01-31"
        assert nach_text["Alarm"]["reminder"]["minutes"] == 30

        # --- 1b. Enddatum der Wiederholung über Zeitzonen hinweg ------------
        # UNTIL muss dieselbe Zeitform wie DTSTART haben. Ein „Z" wäre UTC:
        # der Leser rechnet um und landet östlich von Greenwich einen Tag zu
        # spät, westlich einen Tag zu früh. Deshalb ohne „Z" – und bei einem
        # Ganztagstermin als reines Datum, wie RFC 5545 es verlangt.
        serie = {"id": "abc123", "text": "Serie", "kind": A.ITEM_KIND_TASK,
                 "repeat": {"art": A.REPEAT_WEEKDAYS, "tage": [0, 2], "ende": "2027-01-31"}}
        regel_mit_zeit = app.ics_repeat_rule(serie, ganztaegig=False)
        regel_ganztag = app.ics_repeat_rule(serie, ganztaegig=True)
        assert regel_mit_zeit.endswith("UNTIL=20270131T235959"), regel_mit_zeit
        assert regel_ganztag.endswith("UNTIL=20270131"), regel_ganztag
        assert "Z" not in regel_mit_zeit and "Z" not in regel_ganztag, "UNTIL darf nicht UTC sein."

        # Beide Formen müssen in jeder Zone denselben Tag zurückgeben. Die
        # beiden Funktionen sind reine Umrechnungen, deshalb genügt es, die
        # Zone im Lauf umzustellen.
        # Die dritte Form kommt von fremden Programmen: Tagesende in UTC.
        # Auch sie muss denselben Tag ergeben – UNTIL ist eine Datumsgrenze,
        # kein Zeitpunkt, und wird deshalb nicht umgerechnet.
        fremde_regel = "FREQ=WEEKLY;BYDAY=MO,WE;UNTIL=20270131T235959Z"
        for zone in ("Europe/Berlin", "America/New_York", "Pacific/Kiritimati", "UTC"):
            os.environ["TZ"] = zone
            if hasattr(time, "tzset"):
                time.tzset()
            for regel in (regel_mit_zeit, regel_ganztag, fremde_regel):
                zurueckgelesen = app.ics_repeat_from_rule(regel)
                assert zurueckgelesen["ende"] == "2027-01-31", (zone, regel, zurueckgelesen)
        # Unbrauchbare Angaben werden verworfen, nicht geraten.
        assert app.parse_ics_until("2027-01-31") is None
        assert app.parse_ics_until("20270132") is None
        assert app.parse_ics_until("") is None
        os.environ["TZ"] = "Europe/Berlin"
        if hasattr(time, "tzset"):
            time.tzset()

        # --- 2. Parser: Faltung, Escaping, LF, BOM, Parameter ----------------
        gefaltet = kalender([
            "UID:fremd-1", "SUMMARY:Ein sehr langer Titel der", "  über zwei Zeilen gefaltet wurde",
            "DTSTART;VALUE=DATE:20261005", "DESCRIPTION:Erste Zeile\\nZweite Zeile\\; mit Semikolon",
            "LOCATION:Raum 2\\, Haus B",
        ])
        punkte, bericht = punkte_aus(gefaltet)
        assert punkte[0]["text"] == "Ein sehr langer Titel der über zwei Zeilen gefaltet wurde"
        assert punkte[0]["description"] == "Erste Zeile\nZweite Zeile; mit Semikolon\nOrt: Raum 2, Haus B"
        mit_lf = kalender([
            "UID:fremd-1", "SUMMARY:Ein sehr langer Titel der", "  über zwei Zeilen gefaltet wurde",
            "DTSTART;VALUE=DATE:20261005",
        ], zeilenende="\n")
        assert punkte_aus(mit_lf)[1]["items"] == 1, "LF-Zeilenenden werden gelesen."
        assert punkte_aus("﻿" + gefaltet)[1]["items"] == 1, "Ein BOM stört nicht."
        assert punkte_aus(gefaltet, encoding="cp1252")[1]["items"] == 1
        assert A.unescape_ics_text("a\\nb\\;c\\,d\\\\e") == "a\nb;c,d\\e"
        assert A.unescape_ics_text(A.escape_ics_text("x;y,z\nq")) == "x;y,z\nq"
        name, parameter, wert = A.parse_ics_property('DTSTART;TZID="Europe/Berlin":20261002T090000')
        assert name == "DTSTART" and parameter["TZID"] == "Europe/Berlin" and wert == "20261002T090000"
        try:
            app.read_ics_file(schreibe(os.path.join(folder, "kein.ics"), "Hallo Welt"))
        except ValueError as fehler:
            assert "VCALENDAR" in str(fehler)
        else:
            raise AssertionError("Eine Datei ohne Kalender wurde angenommen")
        try:
            app.read_ics_file(schreibe(os.path.join(folder, "leer.ics"), kalender()))
        except ValueError as fehler:
            assert "VEVENT" in str(fehler)
        else:
            raise AssertionError("Ein Kalender ohne Termine wurde angenommen")

        # --- 3. Zeitangaben ---------------------------------------------------
        tag, zeit, hinweis = A.parse_ics_moment({}, "20261002T093000")
        assert (tag, zeit, hinweis) == ("2026-10-02", "09:30", None), "Ortszeit bleibt Ortszeit."
        tag, zeit, _h = A.parse_ics_moment({}, "20261002T073000Z")
        erwartet = datetime(2026, 10, 2, 7, 30, tzinfo=mod.timezone.utc).astimezone().replace(tzinfo=None)
        assert (tag, zeit) == (erwartet.date().isoformat(), erwartet.strftime("%H:%M")), (tag, zeit)
        tag, zeit, hinweis = A.parse_ics_moment({"TZID": "Europe/Berlin"}, "20261002T090000")
        assert tag and zeit, (tag, zeit)
        tag, zeit, hinweis = A.parse_ics_moment({"TZID": "Kein/Ort"}, "20261002T090000")
        assert (tag, zeit, hinweis) == ("2026-10-02", "09:00", "tzid"), "Unbekannte Zone → Ortszeit plus Hinweis"
        assert A.parse_ics_moment({}, "unlesbar") == (None, None, None)
        assert A.parse_ics_moment({"VALUE": "DATE"}, "20261005") == ("2026-10-05", None, None)
        mit_tzid = kalender(["UID:tz-1", "SUMMARY:Unbekannte Zone",
                             "DTSTART;TZID=Kein/Ort:20261002T090000"])
        punkte, bericht = punkte_aus(mit_tzid)
        assert bericht["dropped"].get("tzid") == 1 and bericht["notes"], bericht
        # Mehrtagestermin landet auf dem ersten Tag.
        mehrtag = kalender(["UID:mt-1", "SUMMARY:Messe", "DTSTART;VALUE=DATE:20261012",
                            "DTEND;VALUE=DATE:20261015"])
        punkte, _b = punkte_aus(mehrtag)
        assert punkte[0]["due"] == "2026-10-12" and punkte[0]["due_time"] is None

        # --- 4. Dauer ---------------------------------------------------------
        assert A.parse_ics_duration("PT1H30M") == 90 and A.parse_ics_duration("PT45M") == 45
        assert A.parse_ics_duration("P1D") == 1440 and A.parse_ics_duration("P1W") == 10080
        assert A.parse_ics_duration("-PT15M") == -15 and A.parse_ics_duration("PT30S") == 1
        assert A.parse_ics_duration("krumm") is None and A.parse_ics_duration("") is None
        mit_duration = kalender(["UID:d-1", "SUMMARY:Mit Dauer", "DTSTART:20261002T090000",
                                 "DURATION:PT1H30M"])
        mit_dtend = kalender(["UID:d-2", "SUMMARY:Mit Ende", "DTSTART:20261002T090000",
                              "DTEND:20261002T103000"])
        assert punkte_aus(mit_duration)[0][0]["estimated_minutes"] == 90
        assert punkte_aus(mit_dtend)[0][0]["estimated_minutes"] == 90, "DTEND und DURATION sind gleichwertig."
        ohne_option = {key: True for key, _t in A.ICS_IMPORT_OPTION_LABELS}
        ohne_option["effort"] = False
        assert punkte_aus(mit_duration, ohne_option)[0][0]["estimated_minutes"] is None

        # --- 5. Wiederholungen -----------------------------------------------
        for regel, erwartete_art in (
            ("FREQ=DAILY", A.REPEAT_DAILY),
            ("FREQ=DAILY;INTERVAL=3", A.REPEAT_EVERY_N_DAYS),
            ("FREQ=WEEKLY", A.REPEAT_WEEKLY),
            ("FREQ=WEEKLY;BYDAY=MO,WE", A.REPEAT_WEEKDAYS),
            ("FREQ=MONTHLY", A.REPEAT_MONTHLY),
            ("FREQ=YEARLY", A.REPEAT_YEARLY),
        ):
            abgebildet = A.ics_repeat_from_rule(regel)
            assert abgebildet and abgebildet["art"] == erwartete_art, (regel, abgebildet)
        assert A.ics_repeat_from_rule("FREQ=DAILY;INTERVAL=3")["abstand"] == 3
        assert A.ics_repeat_from_rule("FREQ=WEEKLY;BYDAY=MO,WE")["tage"] == [0, 2]
        assert A.ics_repeat_from_rule("FREQ=DAILY;UNTIL=20270301T235959Z")["ende"] == "2027-03-01"
        for nicht_abbildbar in ("FREQ=WEEKLY;COUNT=10", "FREQ=MONTHLY;BYMONTHDAY=15",
                                "FREQ=WEEKLY;INTERVAL=2", "FREQ=MONTHLY;BYDAY=2MO",
                                "FREQ=HOURLY", "", "FREQ=YEARLY;INTERVAL=4"):
            assert A.ics_repeat_from_rule(nicht_abbildbar) is None, nicht_abbildbar
        verworfen = kalender(["UID:r-1", "SUMMARY:Zehnmal", "DTSTART;VALUE=DATE:20261005",
                              "RRULE:FREQ=WEEKLY;COUNT=10"])
        punkte, bericht = punkte_aus(verworfen)
        assert punkte[0]["repeat"] is None and bericht["dropped"].get("rrule") == 1
        assert bericht["items"] == 1, "Die Aufgabe entsteht trotzdem – nur ohne Wiederholung."

        # --- 6. Erinnerungen --------------------------------------------------
        relativ = kalender(["UID:a-1", "SUMMARY:Mit Alarm", "DTSTART:20261002T090000",
                            "BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:-PT15M", "END:VALARM"])
        punkte, _b = punkte_aus(relativ)
        assert punkte[0]["reminder"]["mode"] == "relative" and punkte[0]["reminder"]["minutes"] == 15
        fest = kalender(["UID:a-2", "SUMMARY:Fester Alarm", "DTSTART:20261002T090000",
                         "BEGIN:VALARM", "ACTION:DISPLAY",
                         "TRIGGER;VALUE=DATE-TIME:20261002T063000Z", "END:VALARM"])
        punkte, _b = punkte_aus(fest)
        assert punkte[0]["reminder"]["mode"] == "fixed" and punkte[0]["reminder"]["at"]
        danach = kalender(["UID:a-3", "SUMMARY:Alarm danach", "DTSTART:20261002T090000",
                           "BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:PT15M", "END:VALARM"])
        punkte, bericht = punkte_aus(danach)
        assert punkte[0]["reminder"] is None and bericht["dropped"].get("alarm") == 1
        am_ende = kalender(["UID:a-4", "SUMMARY:Alarm am Ende", "DTSTART:20261002T090000",
                            "BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER;RELATED=END:-PT10M", "END:VALARM"])
        punkte, bericht = punkte_aus(am_ende)
        assert punkte[0]["reminder"] is None and bericht["dropped"].get("alarm") == 1
        ohne_alarm_option = dict(ohne_option, effort=True, alarms=False)
        assert punkte_aus(relativ, ohne_alarm_option)[0][0]["reminder"] is None

        # --- 7. Übersprungsgründe und Zeitraum -------------------------------
        gemischt = kalender(
            ["UID:s-1", "SUMMARY:Ohne Beginn"],
            ["UID:s-2", "DTSTART;VALUE=DATE:20261005"],
            ["UID:s-3", "SUMMARY:Abgesagt", "DTSTART;VALUE=DATE:20261005", "STATUS:CANCELLED"],
            ["UID:s-4", "SUMMARY:Gültig", "DTSTART;VALUE=DATE:20261005"],
        )
        punkte, bericht = punkte_aus(gemischt)
        assert bericht["items"] == 1 and punkte[0]["text"] == "Gültig"
        assert bericht["skipped"] == {"no_start": 1, "no_summary": 1, "cancelled": 1}, bericht
        behalte_abgesagt = dict(ohne_option, skip_cancelled=False)
        assert punkte_aus(gemischt, behalte_abgesagt)[1]["items"] == 2
        vergangen = (heute - timedelta(days=400)).strftime("%Y%m%d")
        kuerzlich = (heute - timedelta(days=10)).strftime("%Y%m%d")
        spaeter = (heute + timedelta(days=10)).strftime("%Y%m%d")
        zeitprobe = kalender(
            ["UID:z-1", "SUMMARY:Lange her", f"DTSTART;VALUE=DATE:{vergangen}"],
            ["UID:z-2", "SUMMARY:Kürzlich", f"DTSTART;VALUE=DATE:{kuerzlich}"],
            ["UID:z-3", "SUMMARY:Später", f"DTSTART;VALUE=DATE:{spaeter}"],
        )
        assert punkte_aus(zeitprobe)[1]["items"] == 3
        nur_heute = punkte_aus(zeitprobe, zeitraum="today")
        assert nur_heute[1]["items"] == 1 and nur_heute[0][0]["text"] == "Später"
        assert nur_heute[1]["skipped"].get("out_of_range") == 2
        nur_jahr = punkte_aus(zeitprobe, zeitraum="year")
        assert nur_jahr[1]["items"] == 2 and nur_jahr[1]["skipped"].get("out_of_range") == 1

        # --- 8. Optionen ------------------------------------------------------
        reich = kalender(["UID:o-1", "SUMMARY:Voller Termin", "DTSTART:20261002T090000",
                          "DESCRIPTION:Innentext", "LOCATION:Halle", "CATEGORIES:Eins,Zwei",
                          "PRIORITY:5", "DURATION:PT20M",
                          "BEGIN:VALARM", "TRIGGER:-PT5M", "END:VALARM"])
        aus = {key: False for key, _text in A.ICS_IMPORT_OPTION_LABELS}
        punkte, _b = punkte_aus(reich, aus)
        schlicht = punkte[0]
        assert schlicht["description"] == "" and schlicht["estimated_minutes"] is None
        assert schlicht["reminder"] is None and schlicht["importance"] == 2, "Priorität wirkt immer."
        assert punkte_aus(reich, dict(aus, description=True))[0][0]["description"] == "Innentext"
        assert punkte_aus(reich, dict(aus, location=True))[0][0]["description"] == "Ort: Halle"
        assert punkte_aus(reich, dict(aus, effort=True))[0][0]["estimated_minutes"] == 20
        assert punkte_aus(reich, dict(aus, alarms=True))[0][0]["reminder"]["minutes"] == 5
        for roh, erwartet in (("1", 3), ("4", 3), ("5", 2), ("6", 1), ("9", 1), ("0", 0), ("", 0), ("x", 0)):
            assert A.ics_importance_from_priority(roh) == erwartet, roh

        # --- 9. Grenzen -------------------------------------------------------
        zu_viele = kalender(*[[f"UID:v-{n}", f"SUMMARY:Punkt {n}", "DTSTART;VALUE=DATE:20261005"]
                              for n in range(A.MAX_ICS_IMPORT_EVENTS + 5)])
        try:
            app.read_ics_file(schreibe(os.path.join(folder, "viele.ics"), zu_viele))
        except ValueError as fehler:
            assert str(A.MAX_ICS_IMPORT_EVENTS) in str(fehler)
        else:
            raise AssertionError("Die Terminobergrenze wirkte nicht")
        gross = os.path.join(folder, "gross.ics")
        with open(gross, "wb") as datei:
            datei.write(b"BEGIN:VCALENDAR\r\n" + b"X" * (A.MAX_ICS_IMPORT_BYTES + 1))
        try:
            app.read_ics_file(gross)
        except ValueError as fehler:
            assert "MB" in str(fehler)
        else:
            raise AssertionError("Die Größengrenze wirkte nicht")
        os.remove(gross)

        # --- 10. Import in beide Ziele und Rückgängig -------------------------
        echte_datei = schreibe(os.path.join(folder, "Fremdkalender.ics"), kalender(
            ["UID:i-1", "SUMMARY:Erster Termin", "DTSTART;VALUE=DATE:20261005",
             "CATEGORIES:Frisch aus ICS"],
            ["UID:i-2", "SUMMARY:Zweiter Termin", "DTSTART:20261006T080000"],
            name="Schulungsplan"), )
        kopf, ereignisse = app.read_ics_file(echte_datei)
        anzahl_listen = len(app.lists)
        bestand_vorher = copy.deepcopy(app.data_payload())
        labels_vorher = copy.deepcopy(app.labels)
        ziel, bericht = app.import_ics_events(kopf, ereignisse)
        assert len(app.lists) == anzahl_listen + 1 and bericht["items"] == 2
        assert ziel["title"] == "Schulungsplan", ziel["title"]
        assert app.get_label_by_name("Frisch aus ICS") is not None
        zusammenfassung = app.ics_import_summary(bericht, ziel)
        assert "2 Punkte übernommen" in zusammenfassung and "Schulungsplan" in zusammenfassung
        app.undo_last_change()
        assert app.get_label_by_name("Frisch aus ICS") is None, "Rückgängig nimmt neue Labels mit."
        assert len(app.labels) == len(labels_vorher)
        assert {key: wert for key, wert in app.data_payload().items() if key != "history"} == \
               {key: wert for key, wert in bestand_vorher.items() if key != "history"}
        app.set_active_list(quelle["id"])
        punkte_vorher = app.count_items(app.items, include_groups=True)
        gleiche, bericht = app.import_ics_events(kopf, ereignisse, append_to_current=True)
        assert gleiche["id"] == quelle["id"]
        assert app.count_items(app.items, include_groups=True) == punkte_vorher + 2
        ordner = app.new_folder_object("Kalender", color="accent")
        app.folders.append(ordner)
        assert app.save_items()
        app.set_active_folder(ordner["id"])
        im_ordner, _b = app.import_ics_events(kopf, ereignisse)
        assert im_ordner["folder_id"] == ordner["id"]
        app.set_active_list(quelle["id"])
        # Ohne Titel im Kalender entsteht der Listenname aus dem Dateinamen.
        ohne_namen = schreibe(os.path.join(folder, "Mein_Plan.ics"), kalender(
            ["UID:n-1", "SUMMARY:Nur einer", "DTSTART;VALUE=DATE:20261005"], name=""))
        kopf2, ereignisse2 = app.read_ics_file(ohne_namen)
        ziel2, _b = app.import_ics_events(kopf2, ereignisse2)
        assert ziel2["title"] == "Mein Plan", ziel2["title"]
        app.set_active_list(quelle["id"])

        # --- 11. Dialog in Hell und Dunkel ------------------------------------
        root.deiconify()
        root.geometry("1100x780+10+10")
        for theme in ("light", "dark"):
            app.theme_name = theme
            app.apply_theme()
            app.set_active_list(quelle["id"])
            vorher = app.count_items(app.items, include_groups=True)
            listenzahl = len(app.lists)
            infos.clear()

            def importieren(dialog, parent=None):
                dialog.geometry("780x640")
                dialog.update()
                widgets = list(descendants(dialog))
                haken = {key: next(w for w in widgets if w.winfo_name() == "icsimp_" + key)
                         for key, _text in A.ICS_IMPORT_OPTION_LABELS}
                haken["append"] = next(w for w in widgets if w.winfo_name() == "icsimp_append")
                assert all(str(w.cget("state")) != "disabled" for w in haken.values())
                vorschau = next(w for w in widgets if w.winfo_name() == "icsimp_preview")
                text = vorschau.get("1.0", "end")
                assert "Erster Termin" in text and "Zweiter Termin" in text, text
                haken["append"].invoke()
                knopf = next(w for w in widgets if isinstance(w, mod.RoundedButton)
                             and w.text == "Importieren")
                assert knopf.winfo_ismapped()
                assert (knopf.winfo_rooty() + knopf.winfo_height()
                        <= dialog.winfo_rooty() + dialog.winfo_height())
                knopf.command()
            app.run_modal = importieren
            assert app.show_ics_import_dialog(path=echte_datei) == "break"
            assert len(app.lists) == listenzahl, "Anhängen legt keine neue Liste an."
            assert app.count_items(app.items, include_groups=True) == vorher + 2
            assert infos and "übernommen" in infos[-1][1], infos

            def abbrechen(dialog, parent=None):
                dialog.update()
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)
                     and w.text == "Abbrechen").command()
            app.run_modal = abbrechen
            zustand = copy.deepcopy(app.data_payload())
            app.show_ics_import_dialog(path=echte_datei)
            assert app.data_payload() == zustand, "Abbrechen ändert nichts."
        assert not callbacks, callbacks
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: Kalenderimport mit Parser, Abbildung, Zeitzonen, Regeln, Duplikaten, Zielen und Dialog")
