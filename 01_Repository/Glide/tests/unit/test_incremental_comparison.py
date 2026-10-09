"""P08b: gemerkte Vergleichswerte gegen unabhängigen Vollvergleich."""
import copy
from pathlib import Path
import random
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import save_comparison as comparison

OPTIONS = dict(item_fields=("text", "done", "description", "labels"),
               schedulable=lambda item: item.get("kind", "task") == "task",
               drawing_hash=lambda entry: None)


def fixture():
    return [{"id": f"l{n}", "title": f"Liste {n}", "items": [
        {"id": f"i{n}", "text": str(n), "children": [
            {"id": f"c{n}", "text": "Kind", "children": []}]}]} for n in range(8)]


def prepare(entries, previous=None, changed=None):
    return comparison.prepare_comparison(entries, previous_parts=previous,
                                         changed_ids=changed, **OPTIONS)


class IncrementalComparisonTests(unittest.TestCase):
    def test_only_declared_list_is_read_and_input_is_unchanged(self):
        entries = fixture()
        before = prepare(entries)
        entries[3]["items"][0]["children"][0]["text"] = "Neu"
        original = copy.deepcopy(entries)
        with patch.object(comparison, "compare_lists", wraps=comparison.compare_lists) as build:
            current = prepare(entries, before.parts, {"l3"})
        self.assertEqual(build.call_count, 1)
        self.assertEqual(current, comparison.compare_lists(entries, **OPTIONS))
        self.assertEqual(entries, original)
        self.assertEqual(before.items["c3"]["text"], "Kind")

    def test_full_comparison_recovers_an_undeclared_change(self):
        entries = fixture()
        before = prepare(entries)
        entries[5]["items"][0]["text"] = "Nicht gemeldet"
        self.assertEqual(prepare(entries, before.parts, set()).items["i5"]["text"], "5")
        after = prepare(entries, before.parts)
        self.assertEqual(after, comparison.compare_lists(entries, **OPTIONS))
        self.assertEqual(after.items["i5"]["text"], "Nicht gemeldet")

    def test_move_delete_create_and_reorder_match_full_comparison(self):
        entries = fixture()
        before = prepare(entries)
        entries[4]["items"].append(entries[1]["items"].pop())
        del entries[2]
        entries.append({"id": "new", "title": "Neu", "items": []})
        entries.reverse()
        after = prepare(entries, before.parts, {"l1", "l4"})
        self.assertEqual(after, comparison.compare_lists(entries, **OPTIONS))
        self.assertEqual(after.items["i1"]["list"], "l4")
        self.assertNotIn("i2", after.items)
        self.assertEqual(list(after.lists), [entry["id"] for entry in entries])

    def test_duplicate_list_ids_never_reuse_an_ambiguous_part(self):
        entries = fixture()
        entries[1]["id"] = entries[0]["id"]
        before = prepare(entries)
        entries[0]["items"][0]["text"] = "Andere erste Liste"
        self.assertEqual(prepare(entries, before.parts, set()),
                         comparison.compare_lists(entries, **OPTIONS))

    def test_empty_and_replaced_objects_do_not_depend_on_identity(self):
        entries = fixture()
        before = prepare(entries)
        entries = copy.deepcopy(entries)
        entries[7]["items"] = []
        self.assertEqual(prepare(entries, before.parts, {"l7"}),
                         comparison.compare_lists(entries, **OPTIONS))
        self.assertEqual(prepare([], before.parts, set()).parts, {})

    def test_200_differential_changes(self):
        entries = fixture()
        before = prepare(entries)
        randomizer = random.Random(33311)
        for number in range(200):
            index = randomizer.randrange(len(entries))
            entry = entries[index]
            scope = {entry["id"]}
            if number % 3 == 0:
                target = entries[(index + 1) % len(entries)]
                scope.add(target["id"])
                if entry["items"]:
                    target["items"].append(entry["items"].pop())
            elif entry["items"]:
                entry["items"][0]["description"] = f"Inhalt {number}"
            entry["title"] = f"Liste {number}"
            if number % 5 == 0:
                entries.reverse()
            current = prepare(entries, before.parts, scope)
            self.assertEqual(current, comparison.compare_lists(entries, **OPTIONS), number)
            before = current


if __name__ == "__main__":
    unittest.main()
