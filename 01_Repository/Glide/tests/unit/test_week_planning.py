from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
import copy
from datetime import date, timedelta
import unittest
import week_planning as week
import planning

class WeekPlanningTests(unittest.TestCase):
    def test_shared_day_capacity_with_done_unknown_and_overload(self):
        dates=week.days(date(2026,10,7))
        self.assertEqual(dates[0], date(2026,10,5))
        self.assertEqual(week.days(date(2026,10,7),'sunday')[0],date(2026,10,4))
        items=[dict(id='a',planned_date='2026-10-05',estimated_minutes=60,done=True),
               dict(id='b',planned_date='2026-10-05',estimated_minutes=None),
               dict(id='c',planned_date='2026-10-06',estimated_minutes=130)]
        settings={'daily_capacity_by_weekday':[90,120,0,90,90,0,0]}
        previous=copy.deepcopy((items,settings))
        summary=week.summarize(items,dates,settings,lambda item:True)
        for day in dates:
            iso=day.isoformat()
            self.assertEqual(summary[iso],planning.summarize([i for i in items if i['planned_date']==iso],planning.capacity_for(settings,iso),lambda item:True))
        self.assertEqual(summary['2026-10-05']['done_minutes'],60)
        self.assertEqual(summary['2026-10-05']['without_estimate'],1)
        self.assertEqual(summary['2026-10-06']['remaining'],-10)
        self.assertIsNone(summary['2026-10-07']['remaining'])
        self.assertEqual((items,settings),previous)

    def test_slots_overlap_clip_and_unknown_are_explicit(self):
        day='2026-10-07'
        items=[dict(planned_date=day,planned_time='07:30',estimated_minutes=60),
               dict(planned_date=day,planned_time='09:00',estimated_minutes=60),
               dict(planned_date=day,planned_time='09:30',estimated_minutes=60),
               dict(planned_date=day,planned_time='17:30',estimated_minutes=120),
               dict(planned_date=day,planned_time='12:00',estimated_minutes=None),
               dict(due=day,due_time='11:00',estimated_minutes=60)]
        previous=copy.deepcopy(items)
        self.assertEqual(week.free_slots(items,day,60),[('10:30','17:30')])
        self.assertEqual(week.free_slots(items,day,30),[('08:30','09:00'),('10:30','17:30')])
        self.assertEqual(week.free_slots(items,day,None),[])
        self.assertEqual(week.free_slots(items,day,601),[])
        self.assertEqual(items,previous)

    def test_due_and_planned_are_distinct_but_same_day_is_one_row(self):
        dates=week.days(date(2026,10,7))
        entries=[({},dict(id='a',due='2026-10-05',planned_date='2026-10-06')),
                 ({},dict(id='b',due='2026-10-07',planned_date='2026-10-07'))]
        result=week.calendar_buckets(entries,dates,lambda value:value)
        self.assertEqual([i['id'] for _,i in result['2026-10-05']],['a'])
        self.assertEqual([i['id'] for _,i in result['2026-10-06']],['a'])
        self.assertEqual([i['id'] for _,i in result['2026-10-07']],['b'])

if __name__=='__main__':
    unittest.main()
