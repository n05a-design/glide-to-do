import copy
import unittest
from datetime import datetime, timezone
from occupied_time import Block
import day_relief as relief

UTC = timezone.utc
DAY = "2026-10-10"
NEXT = "2026-10-11"


def task(identity, minutes=60, day=DAY, done=False):
    return dict(id=identity, text=identity, planned_date=day, planned_time="10:00", estimated_minutes=minutes,
                due="2026-10-12", due_time="14:00", done=done, kind="task", repeat={"art":"daily"})


def schedulable(item): return item.get("kind") == "task"


class Relief(unittest.TestCase):
    def setUp(self):
        self.items = [task("a", 90), task("b", 90), task("c", 30, NEXT), task("unknown", None)]
        self.options = dict(capacity=lambda day:120, blocks=lambda day:(), zone=UTC, schedulable=schedulable)

    def test_multiple_explicit_selection_preserves_due_and_input(self):
        original = copy.deepcopy(self.items)
        plan = relief.propose(self.items, ["a", "b", "a"], NEXT, **self.options)
        self.assertEqual([move.identity for move in plan.moves], ["a", "b"])
        self.assertEqual(plan.before[0]["remaining"], -60)
        self.assertEqual(plan.after[0]["remaining"], 120)
        self.assertEqual(plan.after[0]["without_estimate"], 1)
        self.assertEqual(plan.after[1]["remaining"], -90)
        self.assertEqual(relief.validate(plan, self.items, schedulable), (("a", NEXT, "10:00"),("b", NEXT, "10:00")))
        self.assertEqual(self.items, original)

    def test_backlog_clears_time_without_guessing_estimate(self):
        plan = relief.propose(self.items, ["a", "unknown"], None, **self.options)
        self.assertEqual(len(plan.before), 1)
        self.assertEqual(plan.after[0]["minutes"], 90)
        self.assertEqual(relief.validate(plan,self.items,schedulable), (("a",None,None),("unknown",None,None)))

    def test_busy_union_in_both_balances(self):
        busy = (Block(datetime(2026,10,10,9,tzinfo=UTC),datetime(2026,10,10,10,tzinfo=UTC)),
                Block(datetime(2026,10,10,9,30,tzinfo=UTC),datetime(2026,10,10,10,30,tzinfo=UTC)))
        self.options["blocks"] = lambda day:busy
        plan = relief.propose(self.items,["a"],NEXT,**self.options)
        self.assertEqual(plan.before[0]["occupied_minutes"],90)
        self.assertEqual(plan.before[0]["capacity"],30)
        self.assertEqual(plan.before[0]["remaining"],-150)
        self.assertEqual(plan.after[0]["remaining"],-60)
        self.assertEqual(plan.after[1]["remaining"],0)

    def test_fully_busy_is_known_zero(self):
        busy=(Block(datetime(2026,10,10,9,tzinfo=UTC),datetime(2026,10,10,12,tzinfo=UTC)),)
        summary=relief.day_summary(self.items,DAY,120,busy,UTC,schedulable)
        self.assertEqual((summary["capacity"],summary["remaining"]),(0,-180))
        unknown=relief.day_summary(self.items,DAY,0,(),UTC,schedulable)
        self.assertIsNone(unknown["remaining"])

    def test_all_day_even_without_capacity_is_blocked(self):
        busy=(Block(datetime(2026,10,10,tzinfo=UTC),datetime(2026,10,11,tzinfo=UTC),all_day=True),)
        summary=relief.day_summary(self.items,DAY,0,busy,UTC,schedulable)
        self.assertTrue(summary["occupied_all_day"])
        self.assertEqual(summary["remaining"],-180)

    def test_no_automatic_movement_or_reallocation(self):
        plan=relief.propose(self.items,["a"],NEXT,**self.options)
        self.assertEqual(len(plan.moves),1)
        self.assertEqual(plan.after[0]["minutes"],90)
        self.assertEqual(plan.after[1]["minutes"],120)
        self.assertEqual(relief.propose(self.items,["a"],DAY,**self.options).moves,())

    def test_invalid_selection_is_atomic(self):
        original=copy.deepcopy(self.items)
        for selected in ([],["missing"],["a","missing"]):
            with self.assertRaises(ValueError):relief.propose(self.items,selected,NEXT,**self.options)
        self.assertEqual(self.items,original)
        for field,value in (("done",True),("kind","heading"),("planned_date",None)):
            invalid=copy.deepcopy(self.items);invalid[0][field]=value
            with self.assertRaises(ValueError):relief.propose(invalid,["a"],NEXT,**self.options)
        with self.assertRaises(ValueError):relief.propose(self.items+[self.items[0]],["a"],NEXT,**self.options)

    def test_invalid_target(self):
        for day in ("", "2026-1-1", "2026-02-30", False):
            with self.assertRaises(ValueError):relief.propose(self.items,["a"],day,**self.options)

    def test_stale_item_planning_and_load(self):
        plan=relief.propose(self.items,["a"],NEXT,**self.options)
        for index,field,value in ((0,"planned_date",NEXT),(0,"planned_time",None),(0,"done",True),
                                  (1,"estimated_minutes",200),(1,"planned_date",NEXT)):
            changed=copy.deepcopy(self.items);changed[index][field]=value
            with self.assertRaises(ValueError):relief.validate(plan,changed,schedulable)
        with self.assertRaises(ValueError):relief.validate(plan,self.items[1:],schedulable)
        with self.assertRaises(ValueError):relief.validate(plan,self.items+[task("new")],schedulable)

    def test_stale_calendar_and_capacity(self):
        plan=relief.propose(self.items,["a"],NEXT,**self.options)
        self.assertEqual(len(relief.validate(plan,self.items,schedulable,capacity=self.options["capacity"],blocks=self.options["blocks"],zone=UTC)),1)
        with self.assertRaises(ValueError):relief.validate(plan,self.items,schedulable,capacity=lambda day:100,blocks=lambda day:(),zone=UTC)
        busy=(Block(datetime(2026,10,10,9,tzinfo=UTC),datetime(2026,10,10,10,tzinfo=UTC)),)
        with self.assertRaises(ValueError):relief.validate(plan,self.items,schedulable,capacity=self.options["capacity"],blocks=lambda day:busy,zone=UTC)


class ProjectionAndUnavailableTests(unittest.TestCase):
    def test_projected_source_day_is_not_filtered_again(self):
        from datetime import timezone
        import day_relief
        item = {"id":"selected", "planned_date":"2026-10-10", "estimated_minutes":90}
        result = day_relief.summary([item], "2026-10-11", 120, (), timezone.utc, lambda item: True)
        self.assertEqual((result["items"],result["remaining"]),(1,30))
        self.assertEqual(day_relief.day_summary([item], "2026-10-11", 120, (), timezone.utc,
                                               lambda item:True)["items"],0)

    def test_unknown_calendar_never_claims_free_capacity(self):
        import day_relief
        for status in ("loading","error","closed"):
            value={"remaining":120,"without_estimate":1,"calendar_state":status,
                   "calendar_message":"Quelle fehlt"}
            text=day_relief.available_text(value)
            self.assertIn("Freie Zeit unbekannt",text)
            self.assertIn("Quelle fehlt",text)
            self.assertNotIn("frei 2 h",text)
            self.assertIn("1 ohne Schätzung",text)

    def test_busy_and_partial_calendar_are_named_even_without_tasks(self):
        import day_relief
        value={"remaining":0,"without_estimate":0,"occupied_all_day":True,
               "calendar_issues":(("uid","unsupported"),)}
        self.assertIn("ganztägig belegt",day_relief.available_text(value))
        self.assertIn("Kalenderhinweise",day_relief.available_text(value))


if __name__ == "__main__": unittest.main()
