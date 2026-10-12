import unittest
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import occupied_time as busy

class OccupancyTests(unittest.TestCase):
    def setUp(self):
        self.zone = ZoneInfo("Europe/Berlin")
        self.day = date(2026, 10, 10)
    def at(self, hour, minute=0):
        return datetime(2026, 10, 10, hour, minute, tzinfo=self.zone)
    def test_union_clipping_and_unchanged_input(self):
        blocks = [busy.Block(self.at(9),self.at(10)), busy.Block(self.at(9,30),self.at(11)),
                  busy.Block(self.at(11),self.at(12)), busy.Block(self.at(13),self.at(14))]
        before = blocks[:]
        union = busy.merged_intervals(blocks,self.at(9,45),self.at(13,30))
        self.assertEqual(tuple((b-a).total_seconds()/60 for a,b in union),(135,30))
        self.assertEqual(blocks,before)
    def test_budget_subtracts_union_once(self):
        blocks=[busy.Block(self.at(9),self.at(11)),busy.Block(self.at(10),self.at(12))]
        result=busy.day_occupancy(blocks,self.day,self.zone,480)
        self.assertEqual((result['minutes'],result['capacity']),(180,300))
    def test_all_day_blocks_entire_budget(self):
        start,end=busy.day_bounds(self.day,self.zone)
        result=busy.day_occupancy([busy.Block(start,end,all_day=True)],self.day,self.zone,480)
        self.assertEqual((result['minutes'],result['capacity'],result['all_day']),(1440,0,True))
    def test_midnight_is_exclusive(self):
        start,end=busy.day_bounds(self.day,self.zone)
        block=busy.Block(start,end)
        self.assertFalse(busy.overlaps([block],end,end+timedelta(hours=1)))
        self.assertEqual(busy.day_occupancy([block],self.day+timedelta(days=1),self.zone,480)['minutes'],0)
    def test_dst_days(self):
        for day,minutes in ((date(2026,3,29),1380),(date(2026,10,25),1500)):
            start,end=busy.day_bounds(day,self.zone)
            result=busy.day_occupancy([busy.Block(start,end)],day,self.zone,480)
            self.assertEqual((result['minutes'],result['day_minutes'],result['capacity']),(minutes,minutes,0))
    def test_fold_counts_both_physical_hours(self):
        start=datetime(2026,10,25,2,30,tzinfo=self.zone,fold=0)
        end=start.replace(fold=1)
        self.assertEqual((busy.utc(end)-busy.utc(start)).total_seconds(),3600)
        result=busy.day_occupancy([busy.Block(start,end)],start.date(),self.zone,480)
        self.assertEqual(result['minutes'],60)
    def test_free_intervals(self):
        result=busy.free_intervals([busy.Block(self.at(9),self.at(10)),busy.Block(self.at(11),self.at(12))],self.at(8),self.at(13))
        self.assertEqual(tuple((b-a).total_seconds()/60 for a,b in result),(60,60,60))
    def test_validation_and_seconds(self):
        with self.assertRaises(ValueError): busy.Block(datetime(2026,1,1),datetime(2026,1,2))
        with self.assertRaises(ValueError): busy.Block(self.at(9),self.at(9))
        with self.assertRaises(ValueError): busy.day_occupancy([],self.day,self.zone,True)
        block=busy.Block(self.at(9),self.at(9)+timedelta(seconds=1))
        self.assertEqual(busy.day_occupancy([block],self.day,self.zone,480)['minutes'],1)

if __name__ == '__main__': unittest.main()
