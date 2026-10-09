"""P08a: JSON-Gegenprobe und Grenzen des gemeinsamen Vergleichs ohne Tk."""
import copy
import json
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import save_comparison as comparison


FIELDS = ("text", "done", "importance", "description", "labels", "attachments", "repeat")


def schedulable(item):
    return item.get("kind", "task") in ("task", "long")


def build(lists, **kwargs):
    return comparison.compare_lists(lists, item_fields=FIELDS, schedulable=schedulable,
                                    drawing_hash=lambda entry: None, **kwargs)


def fixture():
    return [{"id": "l1", "title": "Änderungen ☑", "items": [
        {"id": "a", "text": "Elternaufgabe", "kind": "long", "done": False, "children": [
            {"id": "b", "text": "Kind", "kind": "task", "done": False, "children": []}]},
        {"id": "g", "text": "Gruppe", "kind": "group", "children": []},
    ]}, {"id": "l2", "title": "Leer", "items": []}]


def legacy_signatures(lists):
    """Unabhängige Gleichheitsprobe: der bisherige vollständige JSON-Vergleich."""
    item_values = {}

    def walk(items):
        for item in items:
            if schedulable(item):
                item_values[item["id"]] = json.dumps(item, sort_keys=True, ensure_ascii=False)
            walk(item.get("children", []))

    for entry in lists:
        walk(entry.get("items", []))
    return ({entry["id"]: json.dumps(entry, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")) for entry in lists}, item_values)


def changed(before, after):
    return {key for key in before.keys() | after.keys() if before.get(key) != after.get(key)}


class SaveComparisonTests(unittest.TestCase):
    def test_history_projection_and_read_only_query(self):
        lists = fixture()
        before = copy.deepcopy(lists)
        result = build(lists, include_edits=False)
        self.assertEqual(lists, before)
        self.assertEqual(list(result.items), ["a", "b", "g"])
        self.assertEqual(result.items["b"], {
            "list": "l1", "list_title": "Änderungen ☑", "parent": "a", "text": "Kind",
            "werte": dict(zip(FIELDS, ["Kind", False, None, "", (), 0, None])),
        })
        self.assertEqual(result.lists["l2"], {
            "title": "Leer", "folder": None, "note": None, "kind": None, "drawing": None, "references": None, "page_features": (None, None),
        })
        self.assertEqual(result.list_signatures, {})
        self.assertEqual(result.item_signatures, {})
        lists[1]['live_lists'] = ['glide://list/l1']
        lists[1]['cover'] = {'kind':'image','attachment':'image23'}
        changed = build(lists, include_edits=False)
        self.assertNotEqual(changed.lists['l2']['page_features'], result.lists['l2']['page_features'])
        self.assertEqual(changed.items, result.items)

    def test_subtree_change_counts_parent_and_child(self):
        lists = fixture()
        before = build(lists)
        lists[0]["items"][0]["children"][0]["text"] = "Anderes Kind"
        after = build(lists)
        self.assertEqual(changed(before.item_signatures, after.item_signatures), {"a", "b"})
        self.assertEqual(changed(before.list_signatures, after.list_signatures), {"l1"})
        self.assertNotIn("g", after.item_signatures)

    def test_every_json_field_and_array_order_matches_legacy(self):
        original = fixture()
        old_lists, old_items = legacy_signatures(original)
        old = build(original)
        randomizer = random.Random(81)
        values = [None, True, False, 0, 1, 1.0, "", "ä\n☑", [], {},
                  [1, False], {"a": True, "b": [1, 2]}]
        for number in range(160):
            lists = copy.deepcopy(original)
            parent = lists[0]["items"][0]
            child = parent["children"][0]
            target = randomizer.choice([lists[0], parent, child])
            target[randomizer.choice(["description", "custom", "reminder", "done_at"])] = randomizer.choice(values)
            if number % 4 == 0:
                lists[0]["items"].reverse()
            if number % 7 == 0:
                parent["children"].append({"id": "new", "text": "Neu", "children": []})
            legacy_lists, legacy_items = legacy_signatures(lists)
            new = build(lists)
            self.assertEqual(changed(old_lists, legacy_lists),
                             changed(old.list_signatures, new.list_signatures), number)
            self.assertEqual(changed(old_items, legacy_items),
                             changed(old.item_signatures, new.item_signatures), number)

    def test_keys_and_object_identity_do_not_matter(self):
        lists = fixture()
        reordered = json.loads(json.dumps(lists, sort_keys=True))
        first, second = build(lists), build(reordered)
        self.assertEqual(first, second)
        lists[0]["items"][0]["text"] = "Geändert"
        self.assertEqual(second, build(reordered))
        self.assertNotEqual(first.list_signatures, build(lists).list_signatures)

    def test_missing_empty_and_json_types_remain_distinct(self):
        signatures = []
        for value in (None, False, 0, 0.0, "", [], {}):
            item = {"id": "a", "custom": value, "children": []}
            signatures.append(build([{"id": "l", "items": [item]}]).item_signatures["a"])
        self.assertEqual(len(set(signatures)), len(signatures))
        item = {"id": "a"}
        first = build([{"id": "l", "items": [item]}])
        item["children"] = []
        self.assertNotEqual(first.item_signatures, build([{"id": "l", "items": [item]}]).item_signatures)

    def test_move_delete_and_container_metadata(self):
        lists = fixture()
        before = build(lists)
        parent = lists[0]["items"].pop(0)
        lists[1]["items"].append(parent)
        moved = build(lists)
        self.assertEqual(changed(before.item_signatures, moved.item_signatures), set())
        self.assertEqual(moved.items["a"]["list"], "l2")
        lists[1]["description"] = "Listenbeschreibung"
        metadata = build(lists)
        self.assertEqual(changed(moved.list_signatures, metadata.list_signatures), {"l2"})
        self.assertEqual(moved.item_signatures, metadata.item_signatures)
        lists[1]["items"].clear()
        self.assertEqual(changed(metadata.item_signatures, build(lists).item_signatures), {"a", "b"})

    def test_done_stamp_is_in_signatures_and_old_done_is_not_redated(self):
        lists = fixture()
        baseline = {"items": build(lists).items}
        item = lists[0]["items"][0]
        item["done"] = True
        result = build(lists, baseline=baseline, completed_at="2026-10-05T20:00:00+02:00")
        self.assertEqual(item["done_at"], "2026-10-05T20:00:00+02:00")
        self.assertEqual(result, build(lists))
        item["done_at"] = None
        build(lists, baseline={"items": result.items}, completed_at="2026-10-06T20:00:00+02:00")
        self.assertIsNone(item["done_at"])

    def test_reopen_clears_stamp_and_structural_items_are_not_stamped(self):
        lists = fixture()
        parent, group = lists[0]["items"]
        parent["done_at"] = "2026-10-04T20:00:00+02:00"
        group["done"] = True
        build(lists, completed_at="2026-10-05T20:00:00+02:00")
        self.assertIsNone(parent["done_at"])
        self.assertNotIn("done_at", group)

    def test_history_field_privacy_and_normalization(self):
        value = comparison.history_value
        item = {"labels": ["b", "a", 4], "description": "Privat",
                "attachments": [{"name": "Privat"}], "repeat": {}, "checklist": []}
        self.assertEqual(value(item, "labels"), ("a", "b"))
        self.assertEqual(value(item, "attachments"), 1)
        self.assertEqual(len(value(item, "description")), 16)
        self.assertNotIn("Privat", value(item, "description"))
        self.assertEqual(value(item, "repeat"), "{}")
        self.assertEqual(value(item, "checklist"), "[]")

    def test_deep_tree_encodes_each_item_once(self):
        from unittest.mock import patch
        item = {"id": "leaf", "text": "Tief", "children": []}
        for depth in range(60):
            item = {"id": f"a{depth}", "text": "Eltern", "children": [item]}
        lists = [{"id": "l", "items": [item]}]
        with patch.object(comparison.json, "dumps", wraps=json.dumps) as dumps:
            result = build(lists)
        self.assertEqual(dumps.call_count, 62)
        self.assertEqual(len(result.item_signatures), 61)


if __name__ == "__main__":
    unittest.main()
