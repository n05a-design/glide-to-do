"""Raster, Zeitumstellung und begrenzte Tagesauswahl aus großen Jahresfenstern."""
from datetime import date, datetime, timedelta, timezone
import random
import unittest
from zoneinfo import ZoneInfo
from occupied_time import Block, BlockIndex, grid_segments, local_interval, merged_intervals, utc, planning_slots

UTC = timezone.utc
BERLIN = ZoneInfo("Europe/Berlin")


class GridTests(unittest.TestCase):
    def test_free_slots_union_calendar_and_tasks_without_losing_later_gap(self):
        day = date(2026, 10, 11)
        blocks = (Block(datetime(2026, 10, 11, 8, tzinfo=BERLIN),
                        datetime(2026, 10, 11, 9, tzinfo=BERLIN)),)
        items = [dict(planned_date=day.isoformat(), planned_time="11:00", estimated_minutes=60)]
        self.assertEqual(planning_slots(items, day, 30, blocks, BERLIN), [("09:00", "11:00"), ("12:00", "18:00")])

    def test_all_day_has_no_slot_and_utc_calendar_is_localized(self):
        day = date(2026, 10, 11)
        blocks = (Block(datetime(2026, 10, 10, 22, tzinfo=UTC),
                        datetime(2026, 10, 11, 22, tzinfo=UTC), all_day=True),)
        self.assertEqual(planning_slots([], day, 30, blocks, BERLIN), [])
        meeting = Block(datetime(2026, 10, 11, 6, tzinfo=UTC), datetime(2026, 10, 11, 8, tzinfo=UTC))
        self.assertEqual(planning_slots([], day, 30, (meeting,), BERLIN), [("10:00", "18:00")])

    def test_free_slots_missing_clock_is_visible_and_short_gap_rejected(self):
        day = date(2026, 3, 29)
        items = [dict(planned_date=day.isoformat(), planned_time="02:30", estimated_minutes=30)]
        with self.assertRaisesRegex(ValueError, "existiert"):
            planning_slots(items, day, 30, (), BERLIN)
        self.assertEqual(planning_slots([], day, 61, (), BERLIN, start=8*60, end=9*60), [])

    def test_regular_and_overnight_clipping_keeps_original(self):
        day = date(2026, 10, 11)
        block = Block(datetime(2026, 10, 10, 23, 30, tzinfo=BERLIN),
                      datetime(2026, 10, 11, 1, 30, tzinfo=BERLIN), "Nacht")
        parts = grid_segments((block,), day, BERLIN)
        self.assertEqual(len(parts), 1)
        self.assertEqual(parts[0].minutes, (0, 90))
        self.assertEqual(parts[0].block, block)
        self.assertEqual(block.start.day, 10)

    def test_fall_hour_has_two_labelled_intervals_with_actual_duration(self):
        day = date(2026, 10, 25)
        block = Block(datetime(2026, 10, 25, 2, 50, tzinfo=BERLIN, fold=0),
                      datetime(2026, 10, 25, 2, 10, tzinfo=BERLIN, fold=1), "Doppelte Stunde")
        parts = grid_segments((block,), day, BERLIN)
        self.assertEqual([part.minutes for part in parts], [(120, 130), (170, 180)])
        self.assertEqual({part.zone_label for part in parts}, {"CEST +0200", "CET +0100"})
        self.assertEqual(sum((part.end-part.start).total_seconds() for part in parts), 20*60)

    def test_spring_gap_is_not_drawn_as_occupied_actual_time(self):
        block = Block(datetime(2026, 3, 29, 1, 30, tzinfo=BERLIN),
                      datetime(2026, 3, 29, 3, 30, tzinfo=BERLIN))
        parts = grid_segments((block,), date(2026, 3, 29), BERLIN)
        self.assertEqual([part.minutes for part in parts], [(90, 120), (180, 210)])
        self.assertEqual(sum((part.end-part.start).total_seconds() for part in parts), 3600)

    def test_half_hour_dst_transition_and_boundary_exactly_at_end(self):
        zone = ZoneInfo("Australia/Lord_Howe")
        block = Block(datetime(2026, 4, 5, 1, 45, tzinfo=zone, fold=0),
                      datetime(2026, 4, 5, 1, 45, tzinfo=zone, fold=1))
        parts = grid_segments((block,), date(2026, 4, 5), zone)
        self.assertEqual([part.minutes for part in parts], [(90, 105), (105, 120)])
        self.assertEqual(sum((part.end-part.start).total_seconds() for part in parts), 1800)
        spring_end = datetime(2026, 3, 29, 1, tzinfo=UTC)
        before = Block(spring_end-timedelta(minutes=30), spring_end)
        parts = grid_segments((before,), date(2026, 3, 29), BERLIN)
        self.assertEqual(len(parts), 1)
        self.assertEqual(parts[0].minutes, (90, 120))

    def test_all_day_and_outside_are_not_timed_segments(self):
        start = datetime(2026, 10, 11, tzinfo=UTC)
        blocks = (Block(start, start+timedelta(days=1), all_day=True),
                  Block(start-timedelta(days=1), start))
        self.assertEqual(grid_segments(blocks, start.date(), UTC), ())

    def test_local_task_interval_preserves_elapsed_duration_and_first_fold(self):
        start, end = local_interval(date(2026, 10, 25), "02:45", 30, BERLIN)
        self.assertEqual(start, datetime(2026, 10, 25, 0, 45, tzinfo=UTC))
        self.assertEqual(end-start, timedelta(minutes=30))
        self.assertEqual(end.astimezone(BERLIN).fold, 1)

    def test_missing_clock_and_invalid_duration_rejected(self):
        with self.assertRaisesRegex(ValueError, "existiert"):
            local_interval(date(2026, 3, 29), "02:30", 30, BERLIN)
        for clock, minutes in (("8:00", 30), ("24:00", 30), ("09:00", True), ("09:00", 0)):
            with self.subTest(clock=clock, minutes=minutes), self.assertRaises(ValueError):
                local_interval(date(2026, 10, 11), clock, minutes, BERLIN)

    def test_index_half_open_boundaries_and_long_spans(self):
        start = datetime(2026, 10, 11, tzinfo=UTC)
        spanning = Block(start-timedelta(days=100), start+timedelta(days=100), "lang")
        left = Block(start-timedelta(hours=1), start, "vorbei")
        right = Block(start+timedelta(days=1), start+timedelta(days=2), "später")
        inside = Block(start+timedelta(hours=1), start+timedelta(hours=2), "innen")
        index = BlockIndex.build((right, inside, spanning, left))
        self.assertEqual(index.between(start, start+timedelta(days=1)), (spanning, inside))
        self.assertEqual(index.between(start-timedelta(days=200), start-timedelta(days=199)), ())
        with self.assertRaises(ValueError):
            index.between(start, start)

    def test_index_matches_reference_for_nested_and_random_intervals(self):
        rng = random.Random(19)
        start = datetime(2026, 1, 1, tzinfo=UTC)
        blocks = tuple(Block(start+timedelta(minutes=left), start+timedelta(minutes=left+length), str(i))
                       for i in range(3000)
                       for left, length in [(rng.randrange(365*1440), rng.randrange(1, 40000))])
        index = BlockIndex.build(reversed(blocks))
        for offset in range(0, 365, 7):
            lower, upper = start+timedelta(days=offset), start+timedelta(days=offset+1)
            expected = {block for block in blocks if utc(block.start)<upper and utc(block.end)>lower}
            actual = index.between(lower, upper)
            self.assertEqual(set(actual), expected)
            self.assertEqual(merged_intervals(actual, lower, upper), merged_intervals(blocks, lower, upper))

    def test_index_cross_zone_midnight_and_empty(self):
        start = datetime(2026, 10, 10, 22, tzinfo=UTC)
        block = Block(start, start+timedelta(hours=2))
        parts = grid_segments(BlockIndex.build((block,)).between(
            datetime(2026, 10, 11, tzinfo=BERLIN),
            datetime(2026, 10, 12, tzinfo=BERLIN)), date(2026, 10, 11), BERLIN)
        self.assertEqual(parts[0].minutes, (0, 120))
        self.assertEqual(BlockIndex.build(()).between(start, start+timedelta(hours=1)), ())


if __name__ == "__main__":
    unittest.main()
