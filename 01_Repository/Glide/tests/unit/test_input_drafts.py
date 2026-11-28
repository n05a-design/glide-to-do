# SPDX-License-Identifier: MPL-2.0
"""Teil 05: dauerhafte Eingabeentwürfe (Neustart, Absturz, Schreibfehler)."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src' / 'glide'))

import input_drafts
from input_drafts import DraftStore


class InputDrafts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, input_drafts.FILE_NAME)

    def tearDown(self):
        self.tmp.cleanup()

    def test_restart_restores_draft_for_exact_target(self):
        store = DraftStore(self.path)
        store.set("a.json", "L1", "Angebot prüfen")
        self.assertTrue(store.flush())
        again = DraftStore(self.path)
        self.assertEqual(again.get("a.json", "L1"), "Angebot prüfen")
        self.assertEqual(again.get("a.json", "L2"), "")
        self.assertEqual(again.get("b.json", "L1"), "")

    def test_empty_and_discarded_drafts_are_not_stored(self):
        store = DraftStore(self.path)
        store.set("a.json", "L1", "   ")
        self.assertFalse(store.dirty)
        store.set("a.json", "L1", "x")
        store.flush()
        store.discard("a.json", "L1")
        store.flush()
        self.assertEqual(DraftStore(self.path).items(), {})

    def test_unchanged_text_causes_no_write(self):
        store = DraftStore(self.path)
        store.set("a.json", "L1", "x")
        store.flush()
        store.set("a.json", "L1", "x")
        self.assertFalse(store.dirty)

    def test_crash_before_replace_keeps_previous_state(self):
        store = DraftStore(self.path)
        store.set("a.json", "L1", "alt")
        store.flush()
        store.set("a.json", "L1", "neu")
        with mock.patch("local_json_store.os.replace", side_effect=OSError("simulierter Abbruch")):
            with self.assertRaises(OSError):
                store.flush()
        self.assertTrue(store.dirty)
        self.assertEqual(DraftStore(self.path).get("a.json", "L1"), "alt")
        self.assertEqual([n for n in os.listdir(self.tmp.name) if n.endswith(".tmp")], [])

    def test_disk_full_keeps_previous_state(self):
        store = DraftStore(self.path)
        store.set("a.json", "L1", "alt")
        store.flush()
        store.set("a.json", "L1", "neu")
        with mock.patch("local_json_store.json.dump", side_effect=OSError(28, "No space left")):
            with self.assertRaises(OSError):
                store.flush()
        self.assertEqual(DraftStore(self.path).get("a.json", "L1"), "alt")

    def test_corrupt_file_is_quarantined_not_overwritten(self):
        Path(self.path).write_text("{kaputt", encoding="utf-8")
        store = DraftStore(self.path)
        self.assertTrue(store.load_problem.startswith("unreadable"))
        self.assertEqual(store.items(), {})
        self.assertFalse(os.path.exists(self.path))
        self.assertTrue(any(".unlesbar_" in n for n in os.listdir(self.tmp.name)))

    def test_newer_version_is_read_but_never_overwritten(self):
        payload = {"format": input_drafts.FORMAT, "version": input_drafts.VERSION + 1,
                   "drafts": [{"save_file": "a.json", "list_id": "L1", "text": "t", "zukunft": 1}]}
        Path(self.path).write_text(json.dumps(payload), encoding="utf-8")
        store = DraftStore(self.path)
        self.assertEqual(store.get("a.json", "L1"), "t")
        store.set("a.json", "L1", "geändert")
        self.assertFalse(store.flush())
        self.assertEqual(json.loads(Path(self.path).read_text(encoding="utf-8")), payload)

    def test_prune_removes_drafts_of_deleted_lists_only(self):
        store = DraftStore(self.path)
        store.set("a.json", "L1", "bleibt")
        store.set("a.json", "L2", "weg")
        store.set("b.json", "L2", "andere Datei")
        store.prune("a.json", {"L1"})
        self.assertEqual(store.items(), {("a.json", "L1"): "bleibt", ("b.json", "L2"): "andere Datei"})

    def test_invalid_entries_are_skipped(self):
        payload = {"format": input_drafts.FORMAT, "version": 1, "drafts": [
            {"save_file": "a.json", "list_id": "L1", "text": "ok", "updated": "x"},
            {"save_file": "", "list_id": "L2", "text": "ohne Datei"}, "kein Objekt"]}
        Path(self.path).write_text(json.dumps(payload), encoding="utf-8")
        self.assertEqual(DraftStore(self.path).items(), {("a.json", "L1"): "ok"})

    def test_limits(self):
        store = DraftStore(self.path, clock=iter(range(10_000)).__next__)
        store.set("a.json", "L", "x" * (input_drafts.MAX_TEXT + 5))
        self.assertEqual(len(store.get("a.json", "L")), input_drafts.MAX_TEXT)
        for i in range(input_drafts.MAX_DRAFTS + 3):
            store.set("a.json", f"N{i}", "t")
        self.assertEqual(len(store.items()), input_drafts.MAX_DRAFTS)
        self.assertEqual(store.get("a.json", "L"), "")


if __name__ == "__main__":
    unittest.main()
