"""Wiederholungsregeln: Prüfen, Weiterrechnen, Überspringen (KO02) ohne Oberfläche."""
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import repeat_rules as r


def aufgabe(identity, due, regel, done=False):
    return {"id": identity, "due": due, "repeat": regel, "done": done}


class Regeln(unittest.TestCase):
    def test_unknown_or_broken_rules_are_none(self):
        for wert in (None, "täglich", {"art": "stündlich"}, {"art": r.EVERY_N_DAYS, "abstand": True},
                     {"art": r.EVERY_N_DAYS, "abstand": 0}, {"art": r.EVERY_N_DAYS, "abstand": 366},
                     {"art": r.WEEKDAYS, "tage": []}, {"art": r.WEEKDAYS, "tage": [7, True]},
                     {"art": r.DAILY, "ende": "31.12.2026"}):
            self.assertIsNone(r.normalize(wert), wert)

    def test_normalize_keeps_start_and_sorts_weekdays(self):
        self.assertEqual(r.normalize({"art": r.WEEKDAYS, "tage": [4, 0, 4]}, default_start="2026-10-01"),
                         {"art": r.WEEKDAYS, "tage": [0, 4], "start": "2026-10-01", "ende": None})
        self.assertEqual(r.normalize({"art": r.DAILY, "start": "kaputt"}), {"art": r.DAILY, "start": None, "ende": None})

    def test_monthly_keeps_month_end_from_anchor(self):
        regel = {"art": r.MONTHLY}
        anker = date(2026, 1, 31)
        feb = r.next_date(regel, anker, anker)
        self.assertEqual(feb, date(2026, 2, 28))
        self.assertEqual(r.next_date(regel, feb, anker), date(2026, 3, 31))
        self.assertEqual(r.next_date({"art": r.YEARLY}, date(2028, 2, 29), date(2028, 2, 29)), date(2029, 2, 28))

    def test_weekdays_daily_interval_and_end(self):
        self.assertEqual(r.next_date({"art": r.WEEKDAYS, "tage": [0, 3]}, date(2026, 10, 8)), date(2026, 10, 12))
        self.assertEqual(r.next_date({"art": r.EVERY_N_DAYS, "abstand": 3}, date(2026, 10, 8)), date(2026, 10, 11))
        self.assertIsNone(r.next_date({"art": r.DAILY, "ende": "2026-10-08"}, date(2026, 10, 8)))
        self.assertEqual(r.next_date({"art": r.DAILY, "ende": "2026-10-09"}, date(2026, 10, 8)), date(2026, 10, 9))

    def test_anchor_date(self):
        self.assertEqual(r.anchor_date({"start": "2026-01-31"}), date(2026, 1, 31))
        self.assertIsNone(r.anchor_date({"start": "31.01."}))
        self.assertIsNone(r.anchor_date(None))


class Ueberspringen(unittest.TestCase):
    HEUTE = date(2026, 10, 8)

    def test_skip_moves_exactly_one_occurrence(self):
        plan, gruende = r.skip_plan([aufgabe("a", "2026-10-08", {"art": r.DAILY}),
                                     aufgabe("b", "2026-10-12", {"art": r.WEEKLY}),
                                     aufgabe("c", "2026-01-31", {"art": r.MONTHLY, "start": "2026-01-31"})],
                                    self.HEUTE)
        self.assertEqual(plan, {"a": "2026-10-09", "b": "2026-10-19", "c": "2026-02-28"})
        self.assertEqual(gruende, {})

    def test_skip_missed_goes_to_first_occurrence_from_today(self):
        plan, gruende = r.skip_plan([aufgabe("a", "2026-10-01", {"art": r.DAILY}),
                                     aufgabe("b", "2026-09-28", {"art": r.WEEKDAYS, "tage": [0, 2]}),
                                     aufgabe("c", "2026-10-08", {"art": r.DAILY}),
                                     aufgabe("d", "2026-06-30", {"art": r.MONTHLY, "start": "2026-01-31"})],
                                    self.HEUTE, missed=True)
        # Heute ist Donnerstag: täglich → heute, Mo/Mi → Montag 12.10., Monatsende → 31.10.
        self.assertEqual(plan, {"a": "2026-10-08", "b": "2026-10-12", "d": "2026-10-31"})
        self.assertEqual(gruende, {"c": "nicht überfällig"})

    def test_reasons_for_inapplicable_tasks(self):
        plan, gruende = r.skip_plan([aufgabe("ohne", "2026-10-08", None),
                                     aufgabe("fertig", "2026-10-08", {"art": r.DAILY}, done=True),
                                     aufgabe("keinTermin", None, {"art": r.DAILY}),
                                     aufgabe("ende", "2026-10-08", {"art": r.DAILY, "ende": "2026-10-08"})],
                                    self.HEUTE)
        self.assertEqual(plan, {})
        self.assertEqual(gruende, {"ohne": "keine Wiederholung", "fertig": "bereits erledigt",
                                   "keinTermin": "ohne Fälligkeit", "ende": "die Reihe hat keinen weiteren Termin"})

    def test_missed_series_ending_before_today_has_no_target(self):
        plan, gruende = r.skip_plan([aufgabe("a", "2026-10-01", {"art": r.DAILY, "ende": "2026-10-05"})],
                                    self.HEUTE, missed=True)
        self.assertEqual(plan, {})
        self.assertEqual(gruende["a"], "die Reihe hat keinen weiteren Termin")

    def test_plan_does_not_mutate_items(self):
        item = aufgabe("a", "2026-10-01", {"art": r.DAILY})
        vorher = dict(item, repeat=dict(item["repeat"]))
        r.skip_plan([item], self.HEUTE, missed=True)
        self.assertEqual(item, vorher)


if __name__ == "__main__":
    unittest.main()
