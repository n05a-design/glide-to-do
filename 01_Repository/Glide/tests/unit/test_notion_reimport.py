"""Drei Zustände unabhängig verändern und jede Übernahme ausdrücklich auswählen."""
import copy
from dataclasses import replace
import unittest

from notion_archive import Export, Page
from notion_reimport import SourceRecord, compare, content_fingerprint, selected_changes

KEY = "notion:" + "a" * 32
BASE = {"id": "page-a", "title": "Titel", "rich_note": {"text": "Inhalt", "spans": [], "links": {}},
        "items": [{"id": "task-a", "text": "Aufgabe", "done": False}], "attachments": [{"id": "file-a", "storage": "attachments/file.png"}]}
PAGE = Page(KEY, "Titel.md", "Titel", (), "# Titel", "1" * 64, ())
SOURCE = SourceRecord(KEY, "page-a", "1" * 64, content_fingerprint(BASE), "Titel.md")


class ReimportTests(unittest.TestCase):
    def export(self, page=PAGE):
        return Export((page,), {}, ())

    def test_unchanged_source_and_local_state_do_not_duplicate(self):
        plan = compare(self.export(), [SOURCE], {"page-a": SOURCE.local_hash})
        self.assertEqual(plan.rows[0].status, "unchanged")
        self.assertEqual(selected_changes(plan, []), ())
        with self.assertRaises(ValueError):
            selected_changes(plan, [KEY])

    def test_new_sources_and_changed_sources_require_selection(self):
        new = compare(self.export(), [], {})
        changed = compare(self.export(replace(PAGE, source_hash="2" * 64)), [SOURCE], {"page-a": SOURCE.local_hash})
        self.assertEqual(new.rows[0].status, "new")
        self.assertEqual(changed.rows[0].status, "changed")
        for plan in (new, changed):
            self.assertEqual(selected_changes(plan, []), ())
            self.assertEqual(selected_changes(plan, [KEY]), plan.rows)

    def test_local_edits_are_kept_when_source_is_unchanged(self):
        local = copy.deepcopy(BASE); local["rich_note"]["text"] = "Eigene Ergänzung"
        plan = compare(self.export(), [SOURCE], {"page-a": content_fingerprint(local)})
        self.assertEqual(plan.rows[0].status, "local-only")
        with self.assertRaises(ValueError):
            selected_changes(plan, [KEY], [KEY])

    def test_real_conflict_needs_additional_explicit_choice(self):
        local = copy.deepcopy(BASE); local["items"][0]["done"] = True
        plan = compare(self.export(replace(PAGE, source_hash="2" * 64)), [SOURCE], {"page-a": content_fingerprint(local)})
        self.assertEqual(plan.rows[0].status, "conflict")
        self.assertEqual(selected_changes(plan, []), ())
        with self.assertRaises(ValueError):
            selected_changes(plan, [KEY])
        self.assertEqual(selected_changes(plan, [KEY], [KEY]), plan.rows)

    def test_missing_target_is_visible_and_never_recreated_implicitly(self):
        plan = compare(self.export(), [SOURCE], {})
        self.assertEqual(plan.rows[0].status, "missing-target")
        self.assertEqual(plan.rows[0].target_id, "page-a")
        self.assertEqual(selected_changes(plan, []), ())
        self.assertEqual(selected_changes(plan, [KEY]), plan.rows)

    def test_sources_absent_from_export_do_not_trigger_deletion(self):
        plan = compare(Export((), {}, ()), [SOURCE], {"page-a": SOURCE.local_hash})
        self.assertEqual(plan.rows, ())
        self.assertEqual(plan.absent_source_keys, (KEY,))
        self.assertEqual(selected_changes(plan, []), ())

    def test_metadata_and_timestamps_do_not_create_local_conflicts(self):
        entry = copy.deepcopy(BASE)
        entry.update(id="other-id", created_at="2026-01-01", updated_at="2026-10-10", notion_source=SOURCE.to_document())
        self.assertEqual(content_fingerprint(entry), content_fingerprint(BASE))

    def test_meaningful_nested_changes_are_detected_without_mutating_state(self):
        original = copy.deepcopy(BASE)
        for field, value in (("title", "Geändert"), ("icon", {"pixels": "neu"}),
                             ("references", ["glide://list/z"]), ("live_lists", ["glide://list/x"]),
                             ("attachments", [])):
            changed = copy.deepcopy(BASE); changed[field] = value
            self.assertNotEqual(content_fingerprint(changed), content_fingerprint(BASE))
        self.assertEqual(BASE, original)

    def test_changed_or_missing_local_attachment_bytes_are_detected(self):
        first = content_fingerprint(BASE, {"file-a": "a" * 64})
        changed = content_fingerprint(BASE, {"file-a": "b" * 64})
        missing = content_fingerprint(BASE, {"file-a": None})
        self.assertEqual(len({first, changed, missing}), 3)
        with self.assertRaises(ValueError):
            content_fingerprint(BASE, {})

    def test_records_roundtrip_and_reject_unknown_version_or_fields(self):
        self.assertEqual(SourceRecord.from_document(SOURCE.to_document()), SOURCE)
        for key, value in (("format_version", 2), ("format_version", True), ("source_hash", "bad"),
                           ("key", "notion:bad"), ("target_id", ""), ("future", 1)):
            raw = SOURCE.to_document(); raw[key] = value
            with self.assertRaises(ValueError):
                SourceRecord.from_document(raw)

    def test_stale_or_unknown_selections_are_rejected(self):
        plan = compare(self.export(), [], {})
        for selected, overwrite in ((["unknown"], []), ([], [KEY])):
            with self.assertRaises(ValueError):
                selected_changes(plan, selected, overwrite)

    def test_duplicate_sources_or_targets_are_rejected(self):
        for records in ([SOURCE, SOURCE], [SOURCE, replace(SOURCE, key="notion:" + "b" * 32)]):
            with self.assertRaises(ValueError):
                compare(self.export(), records, {})
        with self.assertRaises(ValueError):
            compare(Export((PAGE, PAGE), {}, ()), [], {})


if __name__ == "__main__":
    unittest.main()
