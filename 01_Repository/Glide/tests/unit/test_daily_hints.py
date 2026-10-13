"""Künstliche Uhr, Neustart, Sammelhinweise und ausdrückliche Nutzeraktionen."""
import copy
from datetime import datetime, timedelta, timezone
import unittest
import daily_hints as hints
import timezones

# Mitgelieferte IANA-Daten statt Systemdatenbank: Windows bringt keine mit,
# Glide selbst löst Zonen ebenfalls über timezones.Resolver auf.
IANA = timezones.Resolver()


def at(value):
    return datetime.fromisoformat(value).replace(tzinfo=timezone(timedelta(hours=2)))


class DailyHintTests(unittest.TestCase):
    def setUp(self):
        self.config = {"enabled": True}
        self.now = at("2026-10-10T08:30:00")

    def test_defaults_are_off_and_clocks_validate(self):
        self.assertFalse(hints.normalize(None)["enabled"])
        self.assertEqual(hints.normalize({"enabled": 1, "start": "25:00", "close": "8:00"}),
                         {"enabled": False, "start": "08:30", "close": "17:30", "weekdays": list(range(7))})
        self.assertEqual(hints.collect_due({}, {}, self.now), ())

    def test_boundary_and_no_initial_historical_flood(self):
        self.assertEqual(hints.collect_due(self.config, {}, self.now - timedelta(seconds=1)), ())
        due = hints.collect_due(self.config, {}, self.now)
        self.assertEqual([(x.kind, x.day, x.missed) for x in due], [("start", "2026-10-10", False)])

    def test_persistent_dedup_after_restart_and_clock_rollback(self):
        due = hints.collect_due(self.config, {}, self.now)
        state = hints.mark_presented({}, due, self.now)
        self.assertEqual(hints.collect_due(self.config, copy.deepcopy(state), self.now + timedelta(minutes=1)), ())
        self.assertEqual(hints.collect_due(self.config, state, self.now - timedelta(days=1)), ())

    def test_all_missed_weekdays_collected_without_mutation(self):
        state = {"last_check": at("2026-10-08T18:00:00").isoformat(), "receipts": {
            "2026-10-08/start": {"status": "completed"}, "2026-10-08/close": {"status": "completed"}}}
        before = copy.deepcopy(state)
        due = hints.collect_due(self.config, state, at("2026-10-10T18:00:00"))
        self.assertEqual([(x.day, x.kind) for x in due], [("2026-10-09", "start"), ("2026-10-09", "close"),
                                                       ("2026-10-10", "start"), ("2026-10-10", "close")])
        self.assertEqual(sum(x.missed for x in due), 2)
        self.assertEqual(state, before)

    def test_selected_weekdays_and_no_days(self):
        self.assertEqual(hints.collect_due({"enabled": True, "weekdays": [0, 1, 2, 3, 4]}, {}, self.now), ())
        self.assertEqual(hints.collect_due({"enabled": True, "weekdays": []}, {}, self.now), ())
        self.assertEqual(hints.normalize({"weekdays": [True, -1, 6, 6, 7]})["weekdays"], [6])

    def test_snooze_survives_restart_and_fires_once(self):
        hint = hints.collect_due(self.config, {}, self.now)[0]
        state = hints.snooze({}, hint, self.now, 15)
        self.assertEqual(hints.collect_due(self.config, state, self.now + timedelta(minutes=14)), ())
        due = hints.collect_due(self.config, copy.deepcopy(state), self.now + timedelta(minutes=15))
        self.assertEqual(len(due), 1)
        self.assertTrue(due[0].snoozed)
        state = hints.mark_presented(state, due, self.now + timedelta(minutes=15))
        self.assertEqual(hints.collect_due(self.config, state, self.now + timedelta(minutes=16)), ())

    def test_skip_day_and_complete_do_not_mutate_original(self):
        hint = hints.collect_due(self.config, {}, self.now)[0]
        original = {}
        self.assertEqual(hints.complete(original, hint, self.now)["receipts"][hint.identity]["status"], "completed")
        state = hints.skip_day(original, self.now.date(), self.now)
        self.assertEqual(hints.collect_due(self.config, state, at("2026-10-10T18:00:00")), ())
        self.assertEqual(original, {})

    def test_changed_clock_keeps_same_day_identity(self):
        due = hints.collect_due(self.config, {}, self.now)
        state = hints.mark_presented({}, due, self.now)
        changed = {"enabled": True, "start": "09:00"}
        self.assertEqual(hints.collect_due(changed, state, at("2026-10-10T09:00:00")), ())

    def test_snooze_into_next_day_is_collected_alongside_new_hint(self):
        now = at("2026-10-10T23:55:00")
        due = hints.collect_due(self.config, {}, now)
        state = hints.mark_presented({}, due, now)
        state = hints.snooze(state, due[-1], now, 10)
        due = hints.collect_due(self.config, state, at("2026-10-11T08:30:00"))
        self.assertEqual([(x.day, x.kind, x.snoozed) for x in due],
                         [("2026-10-10", "close", True), ("2026-10-11", "start", False)])

    def test_snooze_uses_elapsed_minutes_across_both_dst_changes(self):
        berlin=IANA("Europe/Berlin")
        for day in ((2026,3,29),(2026,10,25)):
            hour=1 if day[1]==3 else 2
            now=datetime(*day,hour,55,tzinfo=berlin)
            hint=hints.Hint(hints.key(now.date(),"start"),"start",now.date().isoformat(),now,False)
            state=hints.snooze({},hint,now,15)
            actual=datetime.fromisoformat(state["receipts"][hint.identity]["wake_at"])
            self.assertEqual(actual.astimezone(timezone.utc)-now.astimezone(timezone.utc),timedelta(minutes=15))
            before=(now.astimezone(timezone.utc)+timedelta(minutes=14)).astimezone(berlin)
            after=(now.astimezone(timezone.utc)+timedelta(minutes=15)).astimezone(berlin)
            config=dict(enabled=True,start="23:59",close="23:59")
            self.assertEqual(hints.collect_due(config,state,before),())
            self.assertEqual(len(hints.collect_due(config,state,after)),1)

    def test_first_ambiguous_clock_is_due_during_second_occurrence(self):
        berlin=IANA("Europe/Berlin")
        now=datetime(2026,10,25,2,15,tzinfo=berlin,fold=1)
        due=hints.collect_due(dict(enabled=True,start="02:30",close="23:59"),{},now)
        self.assertEqual([(h.kind,h.due.fold)for h in due],[("start",0)])
        state=hints.mark_presented({},due,now)
        self.assertEqual(hints.collect_due(dict(enabled=True,start="02:30",close="23:59"),state,
                                         now+timedelta(minutes=30)),())

    def test_invalid_receipt_keys_are_ignored_and_last_date_does_not_overflow(self):
        state={"receipts":{None:{"status":"snoozed","wake_at":self.now.isoformat()},
                           "ungültig":{"status":"snoozed","wake_at":self.now.isoformat()}}}
        self.assertEqual(len(hints.collect_due(self.config,state,self.now)),1)
        maximum=datetime(9999,12,31,18,tzinfo=timezone.utc)
        self.assertEqual(len(hints.collect_due(self.config,{},maximum)),2)
        for day in (None,True,datetime(2026,10,10),3):
            with self.assertRaises(ValueError):hints.key(day,"start")

    def test_disabled_time_is_not_replayed_after_configuration_checkpoint(self):
        old={"last_check":at("2026-10-01T08:00:00").isoformat(),"receipts":{}}
        before=copy.deepcopy(old)
        state=hints.checkpoint(old,self.now)
        self.assertEqual(old,before)
        self.assertEqual([(h.day,h.kind)for h in hints.collect_due(self.config,state,self.now)],
                         [("2026-10-10","start")])
        self.assertEqual(hints.checkpoint(state,self.now-timedelta(days=1)),state)

    def test_corrupt_known_receipt_cannot_silently_suppress_hint(self):
        for value in ({"status":"unknown"},None,{},"completed"):
            state={"receipts":{"2026-10-10/start":value}}
            with self.assertRaisesRegex(ValueError,"Unbekannter gespeicherter Zustand"):
                hints.collect_due(self.config,state,self.now)

    def test_unreasonable_stored_history_is_visible_error_without_large_allocation(self):
        with self.assertRaisesRegex(ValueError,"zehn Jahre"):
            hints.collect_due(self.config,{"last_check":"0001-01-01T12:00:00+00:00"},self.now)
        self.assertEqual(hints.collect_due(self.config,{"last_check":"9999-12-31T12:00:00+00:00"},self.now),())

    def test_pending_after_restart_is_readable_without_automatic_redelivery(self):
        hint = hints.collect_due(self.config, {}, self.now)[0]
        state = hints.mark_presented({}, (hint,), self.now)
        before = copy.deepcopy(state)
        self.assertEqual(hints.pending(self.config, state, self.now), (hint,))
        self.assertEqual(hints.collect_due(self.config, state, self.now), ())
        self.assertEqual(state, before)
        state = hints.snooze(state, hint, self.now, 15)
        pending = hints.pending(self.config, state, self.now)
        self.assertEqual(len(pending), 1)
        self.assertTrue(pending[0].snoozed)
        self.assertGreater(pending[0].due, self.now)
        self.assertEqual(hints.collect_due(self.config, state, self.now), ())
        state = hints.complete(state, pending[0], self.now)
        self.assertEqual(hints.pending(self.config, state, self.now), ())

    def test_invalid_container_checkpoint_and_delay_are_visible(self):
        for state in ([], True, {"receipts": []}, {"last_check": "keine Uhrzeit"},
                      {"receipts": {"2026-10-10/start": {"status": "snoozed", "wake_at": "kaputt"}}}):
            with self.subTest(state=state), self.assertRaises(ValueError):
                hints.collect_due(self.config, state, self.now)
            with self.subTest(state=state), self.assertRaises(ValueError):
                hints.pending(self.config, state, self.now)

    def test_missing_spring_clock_moves_forward_without_double_delivery(self):
        zone = IANA("Europe/Berlin")
        config = dict(enabled=True, start="02:30", close="23:59")
        before = datetime(2026, 3, 29, 3, 29, tzinfo=zone)
        self.assertEqual(hints.collect_due(config, {}, before), ())
        now = datetime(2026, 3, 29, 3, 30, tzinfo=zone)
        due = hints.collect_due(config, {}, now)
        self.assertEqual([(hint.kind, hint.due.hour, hint.due.minute) for hint in due], [("start", 3, 30)])
        state = hints.mark_presented({}, due, now)
        self.assertEqual(hints.collect_due(config, state, now + timedelta(minutes=1)), ())

    def test_prepared_delivery_persists_before_display_without_repeated_writes(self):
        due, state = hints.prepare_delivery(self.config, {}, self.now)
        self.assertEqual(len(due), 1)
        self.assertEqual(state["receipts"][due[0].identity]["status"], "presented")
        before = copy.deepcopy(state)
        later, unchanged = hints.prepare_delivery(self.config, state, self.now + timedelta(minutes=1))
        self.assertEqual(later, ())
        self.assertEqual(unchanged, before)
        self.assertEqual(state, before)
        tomorrow = self.now + timedelta(days=1, hours=-1)
        later, checked = hints.prepare_delivery(self.config, state, tomorrow)
        self.assertEqual([(hint.day, hint.kind) for hint in later], [("2026-10-10", "close")])
        self.assertIn("2026-10-11", checked["last_check"])
        self.assertEqual(hints.prepare_delivery({}, state, tomorrow), ((), state))

    def test_requires_explicit_zone_and_valid_delay(self):
        with self.assertRaises(ValueError): hints.collect_due(self.config, {}, datetime(2026, 10, 10))
        hint = hints.collect_due(self.config, {}, self.now)[0]
        for value in (True, 0, 1441, "15"):
            with self.assertRaises(ValueError): hints.snooze({}, hint, self.now, value)


if __name__ == "__main__":
    unittest.main()
