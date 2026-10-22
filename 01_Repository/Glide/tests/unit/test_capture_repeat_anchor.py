"""Wiederholungsangaben ganz oder gar nicht (FP-00, A29): Ankertag, Wochentage, Hinweise."""
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import capture_parser as c

HEUTE = date(2026, 10, 13)  # Dienstag


def p(text):
    return c.parse_capture(text, (), HEUTE)


def regel(text):
    erfassung = p(text)
    return erfassung.felder.get("repeat"), erfassung.felder.get("due"), erfassung.titel


class AnkerTests(unittest.TestCase):
    def test_monatlich_mit_tag(self):
        self.assertEqual(regel("Miete monatlich am 15."), ({"art": "monatlich", "start": "2026-10-15"}, "2026-10-15", "Miete"))
        self.assertEqual(regel("Miete jeden Monat am Ersten"), ({"art": "monatlich", "start": "2026-11-01"}, "2026-11-01", "Miete"))
        self.assertEqual(regel("Miete jeden 15.")[0], {"art": "monatlich", "start": "2026-10-15"})
        self.assertEqual(regel("Abrechnung monatlich am 31.")[0], {"art": "monatlich", "start": "2026-10-31"})
        self.assertEqual(regel("Miete monatlich am 13.")[1], "2026-10-13", "heute zählt")
        self.assertEqual(p("Miete monatlich am 15. um 9 Uhr").felder["due_time"], "09:00")
        self.assertEqual(p("Miete monatlich am 15.").teile[0].text,
                         "Wiederholung monatlich am 15. · fällig ab Do 15.10.2026")

    def test_monatlich_ohne_tag_bleibt_wie_bisher(self):
        self.assertEqual(regel("Miete monatlich"), ({"art": "monatlich", "start": "2026-10-13"}, "2026-10-13", "Miete"))
        erfassung = p("Ablage monatlich 15 min")
        self.assertEqual(erfassung.felder["estimated_minutes"], 15, "Aufwand ist kein Ankertag")

    def test_jaehrlich_mit_datum(self):
        self.assertEqual(regel("Geschenk jährlich am 24.12."), ({"art": "jaehrlich", "start": "2026-12-24"}, "2026-12-24", "Geschenk"))

    def test_woechentlich_mit_wochentagen(self):
        self.assertEqual(regel("Sport wöchentlich montags"), ({"art": "woechentlich", "start": "2026-10-19"}, "2026-10-19", "Sport"))
        self.assertEqual(regel("Sport jede Woche am Donnerstag")[0], {"art": "woechentlich", "start": "2026-10-15"})
        self.assertEqual(regel("Kurs wöchentlich montags und donnerstags")[0],
                         {"art": "wochentage", "tage": [0, 3], "start": "2026-10-15"})
        self.assertEqual(regel("Sport wöchentlich dienstags")[1], "2026-10-13", "heute zählt")

    def test_intervall_mit_wochentag(self):
        for text in ("Jour fixe alle 2 Wochen montags", "Jour fixe alle 2 Wochen am Montag",
                     "Jour fixe alle zwei Wochen montags"):
            self.assertEqual(regel(text), ({"art": "tage", "abstand": 14, "start": "2026-10-19"}, "2026-10-19", "Jour fixe"), text)
        self.assertEqual(p("Jour fixe alle 2 Wochen montags").teile[0].text,
                         "Wiederholung alle 2 Wochen montags · fällig ab Mo 19.10.2026")
        self.assertNotIn("planned_date", p("Jour fixe alle 2 Wochen am Montag").felder)

    def test_ordinal_ohne_monat_heisst_jede_n_te_woche(self):
        self.assertEqual(regel("Zahnarzt jeden zweiten Dienstag"), ({"art": "tage", "abstand": 14, "start": "2026-10-13"}, "2026-10-13", "Zahnarzt"))
        self.assertEqual(regel("Zahnarzt jeden 2. Dienstag")[0], {"art": "tage", "abstand": 14, "start": "2026-10-13"})
        self.assertEqual(regel("Treffen jeden dritten Freitag")[0], {"art": "tage", "abstand": 21, "start": "2026-10-16"})
        self.assertEqual(regel("Gießen jeden zweiten Tag")[0], {"art": "tage", "abstand": 2, "start": "2026-10-13"})
        self.assertEqual(regel("Sport jede zweite Woche")[0], {"art": "tage", "abstand": 14, "start": "2026-10-13"})
        self.assertEqual(regel("Sport jede zweite Woche montags")[0], {"art": "tage", "abstand": 14, "start": "2026-10-19"})

    def test_bisherige_formen_unveraendert(self):
        self.assertEqual(regel("Sport jeden Montag")[0], {"art": "woechentlich", "start": "2026-10-19"})
        self.assertEqual(regel("Kurs jeden Montag und Donnerstag")[0], {"art": "wochentage", "tage": [0, 3], "start": "2026-10-15"})
        self.assertEqual(regel("Kurs montags, mittwochs und freitags")[0]["tage"], [0, 2, 4])
        self.assertEqual(regel("Wäsche alle zwei Wochen")[0], {"art": "tage", "abstand": 14, "start": "2026-10-13"})
        self.assertEqual(regel("Standup werktags")[0]["tage"], [0, 1, 2, 3, 4])


class GanzOderGarNichtTests(unittest.TestCase):
    NICHT_ABBILDBAR = ("Zahltag jeden letzten Freitag", "Team jeden ersten Montag")

    def test_fp02_neue_formen_erzeugen_ankertag_und_einen_chip(self):
        for text in ("Team jeden ersten Montag im Monat", "Team jeden 2. Dienstag im Monat",
                     "Team jeden zweiten Dienstag des Monats", "Abschluss monatlich am letzten Tag",
                     "Jour fixe alle 2 Wochen montags und donnerstags", "Bericht alle 2 Monate",
                     "Wartung alle 2 Jahre", "Steuer jedes Quartal", "Sport jede zweite Woche montags und donnerstags"):
            result=p(text)
            self.assertEqual(result.felder['repeat']['art'],'serie',text)
            self.assertEqual(len(result.teile),1,text)
            self.assertIn('due',result.felder,text)
            self.assertNotIn('planned_date',result.felder,text)
            self.assertIn('erster Termin',result.teile[0].text,text)

    def test_nicht_abbildbar_bleibt_vollstaendig_text(self):
        for text in self.NICHT_ABBILDBAR:
            erfassung = p(text)
            self.assertEqual(erfassung.titel, text, text)
            self.assertEqual(erfassung.felder, {}, text)
            self.assertEqual(len(erfassung.teile), 1, text)
            self.assertTrue(erfassung.teile[0].text.endswith(c.UNSUPPORTED_REPEAT), erfassung.teile[0].text)
            self.assertEqual(erfassung.teile[0].felder, {})

    def test_keine_teilerkennung_der_wochentage(self):
        for text in self.NICHT_ABBILDBAR:
            self.assertNotIn("planned_date", p(text).felder, text)

    def test_andere_felder_bleiben_erkennbar(self):
        erfassung = p("Bericht alle 2 Monate !hoch 30 min")
        self.assertEqual(erfassung.felder["importance"],3)
        self.assertEqual(erfassung.felder["estimated_minutes"],30)
        self.assertEqual(erfassung.felder["repeat"]["rrule"],"FREQ=MONTHLY;INTERVAL=2")
        self.assertEqual(erfassung.titel, "Bericht")

    def test_gewoehnlicher_text_bleibt_ohne_hinweis(self):
        for text in ("alle Unterlagen sortieren", "jeden Kunden anrufen", "jede Woche zählt", "jeden Tag"):
            erfassung = p(text)
            self.assertFalse(any(t.text.endswith(c.UNSUPPORTED_REPEAT) for t in erfassung.teile), text)


if __name__ == "__main__":
    unittest.main()
