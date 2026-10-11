import copy
import unittest
from task_editing import FIELDS, Conflict, merge


def snapshot():
    result = {key:None for key in FIELDS}
    result.update(text="Aufgabe", kind="task", importance=0, labels=["l"], description="",
                  attachments=[{"id":"a","name":"Bild.png"}], checklist=[{"id":"c","done":False}],
                  links=[], blocked_by=[], due="2026-10-10", planned_date="2026-10-11")
    return result


class TaskEditing(unittest.TestCase):
    def setUp(self):
        self.old=snapshot();self.entered=copy.deepcopy(self.old);self.current=copy.deepcopy(self.old)

    def test_unchanged_form_preserves_fresh_external_fields(self):
        self.current.update(due="2026-10-15", time_spent_minutes=30)
        result=merge(self.old,self.entered,self.current)
        self.assertEqual(result.details,self.current)
        self.assertFalse(result.changed)
        self.assertEqual(result.baseline,self.entered)

    def test_own_title_and_external_due_are_both_retained(self):
        self.entered["text"]="Mein Titel";self.current["due"]="2026-10-15"
        result=merge(self.old,self.entered,self.current)
        self.assertEqual(result.changed,("text",))
        self.assertEqual(result.details["text"],"Mein Titel")
        self.assertEqual(result.details["due"],"2026-10-15")
        self.assertEqual(result.baseline["due"],"2026-10-10")

    def test_repeated_commit_does_not_overwrite_invisible_change(self):
        self.entered["text"]="Mein Titel";self.current["due"]="2026-10-15"
        first=merge(self.old,self.entered,self.current)
        second=merge(first.baseline,self.entered,first.details)
        self.assertFalse(second.changed)
        self.assertEqual(second.details["due"],"2026-10-15")

    def test_conflict_is_atomic_and_names_all_affected_fields(self):
        self.entered.update(text="Mein Titel",due="2026-10-12");self.current.update(text="Anderer Titel",due="2026-10-13")
        originals=copy.deepcopy((self.old,self.entered,self.current))
        with self.assertRaises(Conflict) as error:merge(self.old,self.entered,self.current)
        self.assertEqual(error.exception.fields,("due","text"))
        self.assertEqual((self.old,self.entered,self.current),originals)

    def test_conflict_names_are_german_and_keep_stable_field_ids(self):
        self.entered.update(text="Mein Titel", due="2026-10-12")
        self.current.update(text="Anderer Titel", due="2026-10-13")
        with self.assertRaises(Conflict) as error:
            merge(self.old, self.entered, self.current)
        self.assertEqual(error.exception.fields, ("due", "text"))
        self.assertIn("Fälligkeit", str(error.exception))
        self.assertIn("Titel", str(error.exception))
        self.assertNotIn("due", str(error.exception))

    def test_same_target_is_no_conflict(self):
        self.entered["text"]=self.current["text"]="Gleicher Titel"
        result=merge(self.old,self.entered,self.current)
        self.assertEqual(result.details["text"],"Gleicher Titel")

    def test_deletion_and_zero_are_explicit_edits(self):
        self.entered.update(due=None,attachments=[],importance=0)
        self.old["importance"]=self.current["importance"]=3
        result=merge(self.old,self.entered,self.current)
        self.assertEqual(set(result.changed),{"due","attachments","importance"})
        self.assertIsNone(result.details["due"])
        self.assertEqual(result.details["attachments"],[])

    def test_all_nested_fields_compared_and_copied(self):
        self.entered["checklist"][0]["done"]=True
        self.current["attachments"][0]["name"]="Neuer Name.png"
        original=copy.deepcopy((self.old,self.entered,self.current))
        result=merge(self.old,self.entered,self.current)
        self.assertTrue(result.details["checklist"][0]["done"])
        self.assertEqual(result.details["attachments"][0]["name"],"Neuer Name.png")
        result.details["checklist"][0]["done"]=False
        result.baseline["attachments"].clear()
        self.assertEqual((self.old,self.entered,self.current),original)

    def test_dates_times_and_repeat_are_not_accidentally_combined(self):
        for local,external in (({"due_time":"10:00"},{"due":"2026-10-15"}),
                               ({"planned_date":"2026-10-12"},{"planned_time":"09:00"}),
                               ({"due":"2026-10-12"},{"repeat":{"art":"weekly"}})):
            old=snapshot();entered=copy.deepcopy(old);current=copy.deepcopy(old)
            entered.update(local);current.update(external)
            with self.subTest(local=local,external=external),self.assertRaises(Conflict)as caught:
                merge(old,entered,current)
            self.assertEqual(set(caught.exception.fields),set(local)|set(external))

    def test_identical_concurrent_date_is_not_a_false_conflict(self):
        self.entered.update(due="2026-10-12",due_time="10:00")
        self.current.update(due="2026-10-12")
        result=merge(self.old,self.entered,self.current)
        self.assertEqual(result.details["due_time"],"10:00")
        self.current.update(due_time="11:00")
        self.entered.update(due_time=None)
        result=merge(self.old,self.entered,self.current)
        self.assertEqual(result.details["due_time"],"11:00")

    def test_invalid_contract_never_drops_unknown_fields(self):
        for place in range(3):
            for invalid in ({},dict(self.old,unknown="nicht verlieren"),None):
                args=[self.old,self.entered,self.current];args[place]=invalid
                with self.assertRaises(ValueError):merge(*args)


if __name__=="__main__":unittest.main()
