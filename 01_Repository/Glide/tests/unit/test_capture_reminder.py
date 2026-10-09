"""Erinnerung in der Schnelleingabe (KO03) ohne Oberfläche."""
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import capture_parser as c

HEUTE = date(2026, 10, 8)  # Donnerstag


def lesen(text, ignore=()):
    return c.parse_capture(text, (), HEUTE, ignore)


class Erinnerung(unittest.TestCase):
    def test_fixed_time_today_without_dates(self):
        e = lesen("Steuer erklären erinnere 9 Uhr")
        self.assertEqual(e.titel, "Steuer erklären")
        self.assertEqual(e.felder, {"reminder": {"mode": "fixed", "day": "2026-10-08", "time": "09:00"}})
        self.assertIn("nur bei laufender Glide", e.teile[0].text)

    def test_fixed_time_follows_planned_day_then_due(self):
        e = lesen("Bericht morgen erinnere um 14:30")
        self.assertEqual(e.felder["planned_date"], "2026-10-09")
        self.assertEqual(e.felder["reminder"], {"mode": "fixed", "day": "2026-10-09", "time": "14:30"})
        e = lesen("Bericht bis Freitag Erinnerung um 8")
        self.assertEqual(e.felder["due"], "2026-10-09")
        self.assertEqual(e.felder["reminder"]["day"], "2026-10-09")
        self.assertEqual(e.felder["reminder"]["time"], "08:00")

    def test_explicit_reminder_day_does_not_set_planned_day(self):
        e = lesen("Anrufen Erinnerung Montag 10:15")
        self.assertNotIn("planned_date", e.felder)
        self.assertEqual(e.felder["reminder"], {"mode": "fixed", "day": "2026-10-12", "time": "10:15"})
        self.assertEqual(e.titel, "Anrufen")

    def test_relative_needs_due(self):
        e = lesen("Antrag fällig Freitag erinnern 30 min vorher")
        self.assertEqual(e.felder["reminder"], {"mode": "relative", "minutes": 30})
        self.assertIn("30 Min. vor Fälligkeit", [t.text for t in e.teile if "Erinnerung" in t.text][0])
        e = lesen("Antrag bis morgen 14:00 erinnere 1 Tag vorher")
        self.assertEqual(e.felder["reminder"], {"mode": "relative", "minutes": 1440})
        e = lesen("Termin bis morgen /erinnern bei Fälligkeit")
        self.assertEqual(e.felder["reminder"], {"mode": "relative", "minutes": 0})

    def test_relative_without_due_stays_text_with_hint(self):
        e = lesen("Antrag erinnern 2h vorher")
        self.assertNotIn("reminder", e.felder)
        self.assertEqual(e.titel, "Antrag erinnern 2h vorher")
        self.assertTrue(any("braucht eine Fälligkeit" in t.text for t in e.teile))

    def test_ordinary_text_is_not_a_reminder(self):
        for text in ("Erinnerung an Mama schicken", "Erinnerungen sortieren", "an Erinnerung denken morgen"):
            e = lesen(text)
            self.assertNotIn("reminder", e.felder, text)
        self.assertEqual(lesen("an Erinnerung denken morgen").felder, {"planned_date": "2026-10-09"})

    def test_ignore_keeps_text(self):
        e = lesen("Bericht erinnere 9 Uhr")
        schluessel = [t.schluessel for t in e.teile][0]
        zurueck = lesen("Bericht erinnere 9 Uhr", ignore=(schluessel,))
        self.assertNotIn("reminder", zurueck.felder)
        # Zurückgenommen bleibt der Text Titel; die Uhrzeit wird nicht neu gedeutet.
        self.assertEqual(zurueck.titel, "Bericht erinnere 9 Uhr")
        self.assertEqual(zurueck.felder, {})

    def test_slash_suggestion_lists_reminder(self):
        self.assertIn("erinnern", c.slash_suggestions("eri"))


if __name__ == "__main__":
    unittest.main()
