"""Fehlerbehebung 3.39.1 (FP-00): Wiederholungen richtig erfassen und austauschen.

Über echte Einstiege: Eingabezeile mit Chipzeile, Anlegen, Rückgängig, ICS-Ausgabe
und -Import mit Verlustbericht. A29: Eine Wiederholungsangabe wird ganz oder gar
nicht gedeutet – Ankertag und Wochentage gehören zur Regel, nicht Abbildbares
bleibt vollständig Titel mit einem Hinweis ohne Wirkung. A28: Monats- und
Jahresreihen ab dem 29. ergeben in Kalenderprogrammen dieselben Termine wie in
Glide; eine RFC-Monatsreihe am 31. wird beim Import sichtbar verworfen. A30: Die
Zeitzone des Aufgabenimports kommt aus den mitgelieferten IANA-Daten, auch für
Windows-Namen.

--app wählt den Quellstand; mit der unveränderten 3.39.0 muss die Suite rot sein
(Gegenprobe). Künstliche Daten in einem temporären GLIDE_DATA_DIR.
"""
import argparse
from datetime import date, timedelta
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def naechster_tag_im_monat(tag):
    kandidat = date.today()
    while kandidat.day != tag:
        kandidat += timedelta(days=1)
    return kandidat.isoformat()


def naechster_wochentag(nummer):
    heute = date.today()
    return (heute + timedelta(days=(nummer - heute.weekday()) % 7)).isoformat()


def kalender(*bloecke):
    zeilen = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Fremd//Test//EN"]
    for block in bloecke:
        zeilen += ["BEGIN:VEVENT", *block, "END:VEVENT"]
    return "\r\n".join(zeilen + ["END:VCALENDAR"]) + "\r\n"


with tempfile.TemporaryDirectory(prefix="glide-wiederholung3391-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_wiederholung3391", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    fehler, infos = [], []
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **k: fehler.append(repr(a))
    app.show_info = lambda *a, **k: infos.append(a)
    app.ask_yes_no = lambda *a, **k: True
    A = mod.ListApp
    pruefungen = []

    def ruhe(sekunden=0.15):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    try:
        arbeit = app.new_list_object("Arbeit")
        with app.sidebar_change() as change:
            app.lists.append(arbeit)
            change.mark()
        app.set_active_list(arbeit["id"])
        ruhe()

        def eingeben(text):
            """Text in die Eingabezeile, Chipzeile lesen, mit Enter-Weg anlegen."""
            app.entry.focus_set()
            app.clear_entry_placeholder()
            app.entry.delete(0, "end")
            app.entry.insert(0, text)
            app.update_slash_hint()
            root.update()
            chips = []
            for chip in descendants(app._capture_hint):
                if isinstance(chip, mod.tk.Frame):
                    labels = [w for w in chip.winfo_children() if isinstance(w, mod.tk.Label)]
                    if labels:
                        chips.append((labels[0].cget("text"), len(labels) > 1))
            vorher = len(app.items)
            app.add_item()
            ruhe(0.05)
            assert len(app.items) == vorher + 1, (text, len(app.items))
            return app.items[-1], chips

        # --- A29: Ankertag und Wochentage gehören zur Regel ---------------------
        neu, chips = eingeben("Miete monatlich am 15.")
        erwartet = naechster_tag_im_monat(15)
        assert (neu["text"], neu["due"]) == ("Miete", erwartet), neu
        assert neu["repeat"]["art"] == A.REPEAT_MONTHLY and neu["repeat"].get("start") == erwartet, neu["repeat"]
        assert any(text.startswith("Wiederholung monatlich am 15.") and zurueck for text, zurueck in chips), chips
        neu, chips = eingeben("Jour fixe alle 2 Wochen montags")
        assert (neu["text"], neu["due"]) == ("Jour fixe", naechster_wochentag(0)), neu
        assert neu["repeat"]["art"] == A.REPEAT_EVERY_N_DAYS and neu["repeat"]["abstand"] == 14, neu["repeat"]
        neu, chips = eingeben("Sport wöchentlich donnerstags")
        assert (neu["text"], neu["due"], neu["repeat"]["art"]) == ("Sport", naechster_wochentag(3), A.REPEAT_WEEKLY), neu
        neu, chips = eingeben("Zahnarzt jeden zweiten Dienstag")
        assert (neu["text"], neu["due"], neu["repeat"]["abstand"]) == ("Zahnarzt", naechster_wochentag(1), 14), neu
        assert not neu.get("planned_date"), "Der Wochentag ist Teil der Regel, kein Bearbeitungstag."
        pruefungen.append("A29: Ankertag, Wochentage und Ordinal ohne „im Monat“ werden vollständig Teil der Regel")

        # --- A29: Nicht Abbildbares bleibt ganz Text, Hinweis ohne Wirkung ------
        for text in ("Team jeden ersten Montag im Monat", "Jour fixe alle 2 Wochen montags und donnerstags",
                     "Bericht alle 2 Monate"):
            neu, chips = eingeben(text)
            assert neu["text"] == text, neu["text"]
            assert not neu.get("repeat") and not neu.get("due") and not neu.get("planned_date"), neu
            assert len(chips) == 1 and chips[0][0].endswith("wird noch nicht unterstützt – bleibt Text"), chips
            assert chips[0][1] is False, "Ein Hinweis ohne Wirkung hat nichts zurückzunehmen."
        anzahl = len(app.items)
        app.undo_last_change()
        ruhe()
        assert len(app.items) == anzahl - 1, "Anlegen bleibt ein Rückgängig-Schritt."
        pruefungen.append("A29: nicht Abbildbares vollständig Titel, gedämpfter Hinweis ohne ×, ein Undo-Schritt")

        # --- A28: ICS-Ausgabe am Monatsende -------------------------------------
        for faellig, regel, erwartet_rrule in (
                ("2027-01-31", {"art": A.REPEAT_MONTHLY}, "FREQ=MONTHLY;BYMONTHDAY=28,29,30,31;BYSETPOS=-1"),
                ("2027-01-30", {"art": A.REPEAT_MONTHLY}, "FREQ=MONTHLY;BYMONTHDAY=28,29,30;BYSETPOS=-1"),
                ("2027-01-29", {"art": A.REPEAT_MONTHLY}, "FREQ=MONTHLY;BYMONTHDAY=28,29;BYSETPOS=-1"),
                ("2027-01-15", {"art": A.REPEAT_MONTHLY}, "FREQ=MONTHLY"),
                ("2028-02-29", {"art": A.REPEAT_YEARLY}, "FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=28,29;BYSETPOS=-1"),
                ("2027-03-01", {"art": A.REPEAT_YEARLY}, "FREQ=YEARLY")):
            probe = app.new_item("Serie", due=faellig, repeat=dict(regel, start=faellig))
            assert app.ics_repeat_rule(probe) == erwartet_rrule, (faellig, app.ics_repeat_rule(probe))
        monatsende = app.new_item("Monatsende", due="2027-01-31",
                                  repeat={"art": A.REPEAT_MONTHLY, "start": "2027-01-31", "ende": "2027-12-31"})
        assert app.ics_repeat_rule(monatsende, ganztaegig=True) == \
            "FREQ=MONTHLY;BYMONTHDAY=28,29,30,31;BYSETPOS=-1;UNTIL=20271231"
        pruefungen.append("A28: Ausgabe klemmt am Monatsende wie Glide, vor dem 29. unverändert, UNTIL erhalten")

        # --- A28: Import mit Starttag, Rundlauf ---------------------------------
        datei = os.path.join(ordner, "serien.ics")
        Path(datei).write_text(kalender(
            ["UID:m-31", "SUMMARY:RFC-Monatsreihe", "DTSTART;VALUE=DATE:20270131", "RRULE:FREQ=MONTHLY"],
            ["UID:m-31k", "SUMMARY:Klemmform", "DTSTART;VALUE=DATE:20270131",
             "RRULE:FREQ=MONTHLY;BYMONTHDAY=28,29,30,31;BYSETPOS=-1"],
            ["UID:m-15", "SUMMARY:Mitte", "DTSTART;VALUE=DATE:20270115", "RRULE:FREQ=MONTHLY"],
            ["UID:j-29", "SUMMARY:Schalttag", "DTSTART;VALUE=DATE:20280229", "RRULE:FREQ=YEARLY"]), encoding="utf-8")
        _kopf, ereignisse = app.read_ics_file(datei)
        punkte, bericht = app.ics_events_to_items(ereignisse, None, "all", dry_run=True)
        nach_titel = {punkt["text"]: punkt for punkt in punkte}
        assert nach_titel["RFC-Monatsreihe"]["repeat"] is None, nach_titel["RFC-Monatsreihe"]
        assert nach_titel["Schalttag"]["repeat"] is None, nach_titel["Schalttag"]
        assert nach_titel["Klemmform"]["repeat"]["art"] == A.REPEAT_MONTHLY
        assert nach_titel["Mitte"]["repeat"]["art"] == A.REPEAT_MONTHLY
        assert bericht["dropped"].get("rrule") == 2, bericht
        for faellig, art in (("2027-01-31", A.REPEAT_MONTHLY), ("2028-02-29", A.REPEAT_YEARLY)):
            probe = app.new_item("Rundlauf", due=faellig, repeat={"art": art, "start": faellig})
            rueck = A.ics_repeat_from_rule(app.ics_repeat_rule(probe, ganztaegig=True), start=faellig)
            assert rueck == {"art": art}, (faellig, rueck)
        pruefungen.append("A28: RFC-Reihen am Monatsende sichtbar verworfen (2), Klemmform und Rundlauf erkannt")

        # --- A30: Zeitzone des Aufgabenimports aus mitgelieferten Daten ---------
        assert A.ics_import_zone("W. Europe Standard Time").key == "Europe/Berlin"
        assert A.ics_import_zone("Asia/Tokyo").key == "Asia/Tokyo"
        _tag, _zeit, hinweis = A.parse_ics_moment({"TZID": "W. Europe Standard Time"}, "20270115T090000")
        assert hinweis is None, hinweis
        _tag, _zeit, hinweis = A.parse_ics_moment({"TZID": "Gibt/Es/Nicht"}, "20270115T090000")
        assert hinweis == "tzid", hinweis
        pruefungen.append("A30: IANA- und Windows-Zeitzonen über timezones, Unbekanntes sichtbar als Ortszeit")

        ruhe(0.2)
        assert not fehler, fehler
        print("test_wiederholung3391: OK; " + "; ".join(pruefungen))
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
