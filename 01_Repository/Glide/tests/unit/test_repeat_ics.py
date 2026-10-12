"""Glide-Wiederholung ↔ RRULE (FP-00, A28): gleiche Terminfolge in Glide und RFC-5545-Lesern."""
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import ics_recurrence
import repeat_ics
import repeat_rules


def glide_folge(regel, start, anzahl=24):
    regel = dict(regel, start=start.isoformat())
    folge, termin = [start], start
    while len(folge) < anzahl:
        termin = repeat_rules.next_date(regel, termin, start)
        folge.append(termin)
    return folge


def leser_folge(teile, start, anzahl=24):
    folge = []
    for tag in ics_recurrence.dates(start, ";".join(teile), start + timedelta(days=366 * 30)):
        folge.append(tag)
        if len(folge) == anzahl:
            break
    return folge


class AusgabeTests(unittest.TestCase):
    def test_einfache_arten(self):
        start = date(2026, 10, 13)
        for regel, erwartet in (({"art": "taeglich"}, ["FREQ=DAILY"]),
                                ({"art": "tage", "abstand": 3}, ["FREQ=DAILY", "INTERVAL=3"]),
                                ({"art": "wochentage", "tage": [0, 2, 4]}, ["FREQ=WEEKLY", "BYDAY=MO,WE,FR"]),
                                ({"art": "woechentlich"}, ["FREQ=WEEKLY"]),
                                ({"art": "monatlich"}, ["FREQ=MONTHLY"]),
                                ({"art": "jaehrlich"}, ["FREQ=YEARLY"])):
            self.assertEqual(repeat_ics.rule_parts(regel, start), erwartet)
        self.assertIsNone(repeat_ics.rule_parts({"art": "wochentage", "tage": []}, start))
        self.assertIsNone(repeat_ics.rule_parts({"art": "unbekannt"}, start))

    def test_monatsreihe_jeden_starttag_wie_glide(self):
        for monat in (1, 3, 8, 11):
            for tag in range(1, 32):
                try:
                    start = date(2027, monat, tag)
                except ValueError:
                    continue
                teile = repeat_ics.rule_parts({"art": "monatlich"}, start)
                self.assertEqual(leser_folge(teile, start), glide_folge({"art": "monatlich"}, start), (start, teile))

    def test_jahresreihe_schalttag_wie_glide(self):
        for start in (date(2028, 2, 29), date(2027, 2, 28), date(2026, 12, 31), date(2026, 10, 13)):
            teile = repeat_ics.rule_parts({"art": "jaehrlich"}, start)
            self.assertEqual(leser_folge(teile, start, 12), glide_folge({"art": "jaehrlich"}, start, 12), (start, teile))

    def test_bisherige_ausgabe_vor_dem_29_unveraendert(self):
        self.assertEqual(repeat_ics.rule_parts({"art": "monatlich"}, date(2026, 10, 28)), ["FREQ=MONTHLY"])
        self.assertEqual(repeat_ics.rule_parts({"art": "monatlich"}, None), ["FREQ=MONTHLY"])


class RueckwegTests(unittest.TestCase):
    def r(self, text, start=None):
        return repeat_ics.from_parts(repeat_ics.parse_parts(text), start)

    def test_rundlauf_aller_starttage(self):
        for regel in ({"art": "taeglich"}, {"art": "tage", "abstand": 5}, {"art": "wochentage", "tage": [1, 3]},
                      {"art": "woechentlich"}, {"art": "monatlich"}, {"art": "jaehrlich"}):
            for start in (date(2026, 1, 31), date(2026, 4, 30), date(2028, 2, 29), date(2026, 10, 13)):
                teile = repeat_ics.rule_parts(regel, start)
                self.assertEqual(self.r(";".join(teile), start), regel, (regel, start, teile))

    def test_rfc_monatsreihe_am_monatsende_wird_abgelehnt(self):
        self.assertIsNone(self.r("FREQ=MONTHLY", date(2026, 1, 31)))
        self.assertIsNone(self.r("FREQ=MONTHLY", date(2026, 1, 29)))
        self.assertIsNone(self.r("FREQ=YEARLY", date(2028, 2, 29)))
        self.assertEqual(self.r("FREQ=MONTHLY", date(2026, 1, 28)), {"art": "monatlich"})
        self.assertEqual(self.r("FREQ=MONTHLY;BYMONTHDAY=-1", date(2026, 1, 31)), {"art": "monatlich"})
        self.assertIsNone(self.r("FREQ=MONTHLY;BYMONTHDAY=-1", date(2026, 4, 30)))
        self.assertIsNone(self.r("FREQ=MONTHLY;BYMONTHDAY=28,29,30,31;BYSETPOS=-1", date(2026, 1, 30)))

    def test_ohne_starttag_bisherige_abbildung(self):
        self.assertEqual(self.r("FREQ=MONTHLY"), {"art": "monatlich"})
        self.assertEqual(self.r("FREQ=YEARLY"), {"art": "jaehrlich"})

    def test_nicht_abbildbar(self):
        for text in ("FREQ=WEEKLY;COUNT=10", "FREQ=MONTHLY;BYMONTHDAY=15", "FREQ=WEEKLY;INTERVAL=2",
                     "FREQ=MONTHLY;BYDAY=2MO", "FREQ=HOURLY", "", "FREQ=YEARLY;INTERVAL=4",
                     "FREQ=DAILY;BYHOUR=9", "FREQ=MONTHLY;INTERVAL=2"):
            self.assertIsNone(self.r(text, date(2026, 10, 13)), text)


if __name__ == "__main__":
    unittest.main()
