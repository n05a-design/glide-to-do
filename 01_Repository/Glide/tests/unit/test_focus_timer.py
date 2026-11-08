# SPDX-License-Identifier: MPL-2.0
"""Pausen, Neustart, Rundung und Wiederaufnahme vorbereiteter Zeitbuchungen."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import focus_timer as f

START = datetime(2026, 10, 7, 9, tzinfo=timezone(timedelta(hours=2)))


def timer(**fields):
    value = dict(item_id="a", started_at=START.isoformat(), focus=True, elapsed_seconds=0, goal_seconds=1500)
    value.update(fields)
    return value


class TimerTest(unittest.TestCase):
    def test_legacy_minutes_and_naive_timestamp_remain_valid(self):
        value = dict(item_id="a", started_at=START.isoformat())
        self.assertEqual(f.minutes(value, START + timedelta(seconds=125)), 3)
        self.assertIsNotNone(f.normalize(dict(item_id="a", started_at="2026-10-07T09:00:00")))

    def test_subsecond_zero_and_minute_rounding(self):
        for seconds, minutes in ((0, 0), (.5, 0), (1, 1), (60, 1), (61, 2)):
            self.assertEqual(f.minutes(timer(), START + timedelta(seconds=seconds)), minutes)

    def test_pause_resume_does_not_count_pause(self):
        paused = f.pause(timer(), START + timedelta(seconds=125))
        self.assertEqual(f.elapsed(paused, START + timedelta(hours=10)), 125)
        resumed = f.resume(paused, START + timedelta(minutes=10))
        self.assertEqual(f.elapsed(resumed, START + timedelta(minutes=10, seconds=55)), 180)
        self.assertEqual(f.minutes(resumed, START + timedelta(minutes=10, seconds=55)), 3)

    def test_interval_caps_closed_app_time_and_can_continue(self):
        self.assertEqual(f.minutes(timer(), START + timedelta(days=1)), 25)
        paused = f.pause(timer(), START + timedelta(days=1))
        resumed = f.resume(paused, START + timedelta(days=1))
        self.assertEqual(resumed["goal_seconds"], 3000)
        self.assertEqual(f.minutes(resumed, START + timedelta(days=1, minutes=5)), 30)

    def test_chosen_duration_is_kept_and_used_for_the_next_interval(self):
        self.assertEqual([f.normalize_minutes(v) for v in (15, 25, 50, 30, '15', True, None)], [15, 25, 50, 25, 25, 25, 25])
        kurz = dict(timer(), goal_seconds=900, interval_seconds=900)
        self.assertEqual(f.normalize(kurz)["interval_seconds"], 900)
        self.assertEqual(f.interval_minutes(kurz), 15)
        self.assertEqual(f.minutes(kurz, START + timedelta(hours=2)), 15)
        weiter = f.resume(f.pause(kurz, START + timedelta(hours=2)), START + timedelta(hours=2))
        self.assertEqual(weiter["goal_seconds"], 1800)
        self.assertNotIn("interval_seconds", f.normalize(dict(timer(), interval_seconds=1234)))
        self.assertNotIn("interval_seconds", f.normalize(dict(timer(), interval_seconds=181 * 60)))
        self.assertEqual(f.normalize(dict(timer(), goal_seconds=5400, interval_seconds=5400))["interval_seconds"], 5400)
        self.assertEqual(f.interval_minutes(dict(timer(), interval_seconds=5400)), 90)
        self.assertEqual([f.estimate_option(v) for v in (30, 90, 25, 4, 181, None, True)], [30, 90, None, None, None, None, None])
        self.assertEqual(f.interval_minutes(timer()), 25)
        self.assertEqual(f.interval_minutes(None), 25)

    def test_extend_adds_five_minutes_and_resumes_only_at_interval_end(self):
        laufend = f.extend(timer(), START + timedelta(minutes=10))
        self.assertEqual(laufend["goal_seconds"], 1800)
        self.assertIsNotNone(laufend["started_at"])
        ende = f.pause(timer(), START + timedelta(minutes=30))
        weiter = f.extend(ende, START + timedelta(minutes=31))
        self.assertEqual(weiter["goal_seconds"], 1800)
        self.assertEqual(f.minutes(weiter, START + timedelta(minutes=33)), 27)
        pause = f.pause(timer(), START + timedelta(minutes=5))
        verlaengert = f.extend(pause, START + timedelta(minutes=8))
        self.assertIsNone(verlaengert["started_at"])
        self.assertEqual(verlaengert["goal_seconds"], 1800)
        with self.assertRaises(ValueError):
            f.extend(dict(item_id="x", started_at=START.isoformat()), START)

    def test_clock_backwards_and_changed_timezone(self):
        self.assertEqual(f.elapsed(timer(), START - timedelta(hours=1)), 0)
        self.assertEqual(f.elapsed(timer(), (START + timedelta(minutes=5)).astimezone(timezone.utc)), 300)

    def test_normalization_rejects_corrupt_state(self):
        for value in (None, {}, timer(item_id=""), timer(started_at="bad"), timer(elapsed_seconds=True),
                      timer(elapsed_seconds=float("nan")), timer(goal_seconds=float("inf")), timer(goal_seconds=-1)):
            self.assertIsNone(f.normalize(value))
        self.assertIsNotNone(f.normalize(timer(started_at=None, elapsed_seconds=60)))

    def test_booking_replay_is_idempotent_and_refuses_external_edits(self):
        booking = f.normalize_booking(dict(item_id="a", before=10, after=13))
        self.assertEqual(booking["minutes"], 3)
        self.assertEqual(f.booking_action(booking, 10), "apply")
        self.assertEqual(f.booking_action(booking, 13), "committed")
        self.assertEqual(f.booking_action(booking, 18), "conflict")

    def test_next_candidates_keep_rank_order_and_first_choice(self):
        rows = [((2, 0), "c", "C"), ((1, 5), "b", "B"), ((1, 5), "a", "A"), ((0, 9), "z", "Z")]
        self.assertEqual(f.next_candidates(rows), ["Z", "A", "B", "C"])
        self.assertEqual(f.next_candidates(rows, limit=2), ["Z", "A"])
        self.assertEqual(f.next_candidates(rows, limit=1), [min(rows, key=lambda r: (r[0], r[1]))[2]])
        self.assertEqual(f.next_candidates([], limit=5), [])
        self.assertEqual(f.next_candidates(rows, limit=0), [])
        self.assertEqual(f.SWITCH_LIMIT, 5)

    def test_switch_label_is_single_line_and_bounded(self):
        self.assertEqual(f.switch_label("  Bericht\n schreiben "), "Bericht schreiben")
        self.assertEqual(f.switch_label(""), "Ohne Titel")
        self.assertEqual(f.switch_label(None), "Ohne Titel")
        lang = f.switch_label("Wort " * 30)
        self.assertTrue(lang.endswith("…") and len(lang) <= f.SWITCH_TITLE_LIMIT, lang)
        self.assertEqual(f.switch_label("x" * f.SWITCH_TITLE_LIMIT), "x" * f.SWITCH_TITLE_LIMIT)

    def test_next_label_names_following_task_or_none(self):
        self.assertEqual(f.next_label("Angebot  prüfen"), "Als Nächstes: Angebot prüfen")
        self.assertEqual(f.next_label(""), "Als Nächstes: Ohne Titel")
        self.assertEqual(f.next_label(None), "Danach keine weitere Aufgabe für heute")
        self.assertTrue(f.next_label("Wort " * 30).endswith("…"))

    def test_more_label_only_beyond_limit(self):
        self.assertEqual(f.more_label(2), "… und 2 weitere für heute")
        self.assertEqual(f.more_label(1), "… und 1 weitere für heute")
        self.assertEqual(f.more_label(0), "")
        self.assertEqual(f.more_label(-1), "")
        self.assertEqual(f.more_label(None), "")

    def test_next_label_counts_remaining_tasks(self):
        self.assertEqual(f.next_label("Angebot", 1), "Als Nächstes: Angebot · danach noch 1 Aufgabe")
        self.assertEqual(f.next_label("Angebot", 3), "Als Nächstes: Angebot · danach noch 3 Aufgaben")
        self.assertEqual(f.next_label("Angebot", 0), "Als Nächstes: Angebot")
        self.assertEqual(f.next_label("Angebot", -2), "Als Nächstes: Angebot")
        self.assertEqual(f.next_label("Angebot", None), "Als Nächstes: Angebot")
        self.assertEqual(f.next_label(None, 4), "Danach keine weitere Aufgabe für heute")
        lang = f.next_label("Wort " * 30, 2)
        self.assertTrue(lang.endswith("· danach noch 2 Aufgaben") and "…" in lang)

    def test_booking_validation(self):
        for value in (None, {}, dict(item_id="a", before=13, after=10),
                      dict(item_id="a", before=True, after=10)):
            self.assertIsNone(f.normalize_booking(value))


if __name__ == "__main__":
    unittest.main()
