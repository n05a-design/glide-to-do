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

    def test_booking_validation(self):
        for value in (None, {}, dict(item_id="a", before=13, after=10),
                      dict(item_id="a", before=True, after=10)):
            self.assertIsNone(f.normalize_booking(value))


if __name__ == "__main__":
    unittest.main()
