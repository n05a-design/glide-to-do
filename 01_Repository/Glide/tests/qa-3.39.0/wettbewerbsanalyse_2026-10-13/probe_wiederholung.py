"""Lesende Proben zu Wiederholungen in Glide 3.39.0 (Nachweis 13.10.2026, kein Teil der App).

1. Schnelleingabe: wie `capture_parser.parse_capture` Wiederholungsangaben heute erkennt (A29).
2. ICS-Ausgabe: Glides Terminfolge (`repeat_rules.next_date`) gegen die Folge, die ein
   RFC-5545-Leser aus der heutigen Ausgabe `FREQ=MONTHLY`/`FREQ=YEARLY` rechnet, und gegen
   einen Korrekturvorschlag mit BYSETPOS (A28). Gerechnet mit `ics_recurrence.dates`, dessen
   Übereinstimmung mit einer unabhängigen Referenz `gegenprobe_rrule.py` belegt.

Aufruf aus `01_Repository/Glide`:
    python3 -B -I tests/qa-3.39.0/wettbewerbsanalyse_2026-10-13/probe_wiederholung.py src/glide
Nur Standardbibliothek, keine Schreibzugriffe; Ausgabe JSON auf stdout.
"""
import json
import sys
from datetime import date

sys.path.insert(0, sys.argv[1])
import capture_parser  # noqa: E402
import ics_recurrence  # noqa: E402
import repeat_rules  # noqa: E402

HEUTE = date(2026, 10, 13)  # Dienstag
EINGABEN = [
    ("Zahnarzt jeden 2. Dienstag", "zweiter Dienstag im Monat oder jede zweite Woche (mehrdeutig)"),
    ("Zahnarzt jeden zweiten Dienstag", "alle 2 Wochen dienstags"),
    ("Team jeden ersten Montag im Monat", "erster Montag im Monat"),
    ("F jeden dritten Freitag", "mehrdeutig; nicht teilweise deuten"),
    ("B alle 2 Wochen am Montag", "alle 2 Wochen montags"),
    ("C alle 2 Wochen montags", "alle 2 Wochen montags"),
    ("Jour fixe alle 2 Wochen montags und donnerstags", "alle 2 Wochen montags und donnerstags"),
    ("J wöchentlich montags", "wöchentlich montags"),
    ("G monatlich am 15.", "monatlich am 15."),
    ("H jeden Monat am Ersten", "monatlich am 1."),
    ("Bericht alle 2 Monate", "alle 2 Monate"),
    ("A jeden Montag und Donnerstag", "montags und donnerstags"),
    ("D jeden Montag", "wöchentlich montags"),
    ("I alle zwei Wochen", "alle 14 Tage"),
]
FAELLE_ICS = [
    ("monatlich", date(2026, 1, 31), "FREQ=MONTHLY", "FREQ=MONTHLY;BYMONTHDAY=28,29,30,31;BYSETPOS=-1"),
    ("monatlich", date(2026, 1, 30), "FREQ=MONTHLY", "FREQ=MONTHLY;BYMONTHDAY=28,29,30;BYSETPOS=-1"),
    ("monatlich", date(2026, 1, 29), "FREQ=MONTHLY", "FREQ=MONTHLY;BYMONTHDAY=28,29;BYSETPOS=-1"),
    ("monatlich", date(2026, 1, 15), "FREQ=MONTHLY", "FREQ=MONTHLY"),
    ("jaehrlich", date(2028, 2, 29), "FREQ=YEARLY", "FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=28,29;BYSETPOS=-1"),
]


def glide_folge(art, start, anzahl=8):
    regel = {"art": art, "start": start.isoformat()}
    folge, termin = [start], start
    for _ in range(anzahl - 1):
        termin = repeat_rules.next_date(regel, termin, start)
        folge.append(termin)
    return [tag.isoformat() for tag in folge]


def ics_folge(rrule, start, anzahl=8):
    folge = []
    for tag in ics_recurrence.dates(start, rrule, date(2040, 12, 31)):
        folge.append(tag.isoformat())
        if len(folge) == anzahl:
            break
    return folge


def main():
    eingaben = []
    for text, gemeint in EINGABEN:
        titel, felder, _teile = capture_parser.parse_capture(text, today=HEUTE)
        eingaben.append({"eingabe": text, "gemeint": gemeint, "titel": titel,
                         "felder": {k: v for k, v in felder.items() if k in ("due", "planned_date", "repeat")}})
    ics = []
    for art, start, heute_ausgabe, vorschlag in FAELLE_ICS:
        glide = glide_folge(art, start)
        ics.append({"art": art, "start": start.isoformat(), "glide": glide,
                    "heutige_ausgabe": heute_ausgabe, "leser_aus_heutiger_ausgabe": ics_folge(heute_ausgabe, start),
                    "gleich_heute": ics_folge(heute_ausgabe, start) == glide,
                    "vorschlag": vorschlag, "gleich_vorschlag": ics_folge(vorschlag, start) == glide})
    print(json.dumps({"stichtag": HEUTE.isoformat(), "schnelleingabe": eingaben, "ics_ausgabe": ics},
                     ensure_ascii=False, indent=1))


main()
