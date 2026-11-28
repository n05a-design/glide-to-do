# SPDX-License-Identifier: MPL-2.0
"""Format 27 ohne Tk: stabile Kapitelanker, Kapitelverweise, Navigationsort (Teil 05)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src' / 'glide'))

import chapters
import object_references as refs
import sidebar_policy as sidebar

A = "a" * 32
B = "b" * 32


def doc(text, spans):
    return {"text": text, "spans": [dict(tag=t, start=s, end=e) for t, s, e in spans], "links": {}}


def anchors(document):
    return [(s["tag"], s["start"], s["end"]) for s in document["spans"] if s["tag"].startswith("anchor:")]


class Anchors(unittest.TestCase):
    def setUp(self):
        # "Eins\nText\nZwei\nmehr"
        self.base = doc("Eins\nText\nZwei\nmehr", [("h1", 0, 5), ("h2", 10, 15)])

    def test_every_heading_gets_one_anchor_and_key_is_anchor(self):
        ids = iter([A, B])
        neu, changed = chapters.ensure_anchors(self.base, new_id=lambda: next(ids))
        self.assertTrue(changed)
        self.assertEqual(anchors(neu), [("anchor:" + A, 0, 5), ("anchor:" + B, 10, 15)])
        keys = [k.key for k in chapters.outline(neu)]
        self.assertEqual(keys, [A, B])
        again, changed = chapters.ensure_anchors(neu)
        self.assertFalse(changed)
        self.assertIs(again, neu)

    def test_legacy_document_keeps_derived_keys(self):
        self.assertEqual([k.key for k in chapters.outline(self.base)], ["1:Eins#1", "2:Zwei#1"])

    def prepared(self):
        ids = iter([A, B])
        return chapters.ensure_anchors(self.base, new_id=lambda: next(ids))[0]

    def test_rename_keeps_anchor(self):
        neu = self.prepared()
        k = chapters.find(chapters.outline(neu), A)
        renamed = chapters.rename(neu, k, "Ganz anders")
        self.assertEqual(chapters.find(chapters.outline(renamed), A).title, "Ganz anders")
        self.assertFalse(chapters.ensure_anchors(renamed)[1])

    def test_level_change_keeps_anchor(self):
        neu = self.prepared()
        k = chapters.find(chapters.outline(neu), B)
        changed = chapters.set_level(neu, k, 1)
        self.assertEqual(chapters.find(chapters.outline(changed), B).level, 1)

    def test_move_keeps_anchors(self):
        neu = doc("Eins\nx\nZwei\ny", [("h1", 0, 5), ("h1", 7, 12)])
        ids = iter([A, B])
        neu = chapters.ensure_anchors(neu, new_id=lambda: next(ids))[0]
        kapitel = chapters.outline(neu)
        moved = chapters.move(neu, kapitel, chapters.find(kapitel, B), -1)
        self.assertEqual([k.key for k in chapters.outline(moved)], [B, A])
        self.assertEqual([k.title for k in chapters.outline(moved)], ["Zwei", "Eins"])

    def test_dissolve_removes_anchor_on_ensure(self):
        neu = self.prepared()
        k = chapters.find(chapters.outline(neu), A)
        flat, changed = chapters.ensure_anchors(chapters.dissolve(neu, k))
        self.assertTrue(changed)
        self.assertEqual([a[0] for a in anchors(flat)], ["anchor:" + B])

    def test_duplicate_ids_keep_first_and_renew_second(self):
        dup = doc("Eins\nEins\n", [("h1", 0, 5), ("h1", 5, 10), ("anchor:" + A, 0, 5), ("anchor:" + A, 5, 10)])
        self.assertEqual(chapters.outline(dup)[1].anchor, None)
        neu, changed = chapters.ensure_anchors(dup)
        self.assertTrue(changed)
        ids = [a[0] for a in anchors(neu)]
        self.assertEqual(ids[0], "anchor:" + A)
        self.assertNotEqual(ids[1], ids[0])

    def test_retyped_heading_keeps_anchor_via_newline(self):
        # Überschrift komplett neu getippt: nur der Zeilenumbruch trug den Anker noch.
        typed = doc("Neu\nText", [("h1", 0, 4), ("anchor:" + A, 3, 4)])
        neu, _ = chapters.ensure_anchors(typed)
        self.assertEqual(anchors(neu), [("anchor:" + A, 0, 4)])

    def test_renew_for_copies(self):
        neu = self.prepared()
        copy_doc, mapping = chapters.renew_anchors(neu)
        self.assertEqual(set(mapping), {A, B})
        self.assertFalse(set(mapping.values()) & {A, B})
        self.assertEqual([k.key for k in chapters.outline(copy_doc)], [mapping[A], mapping[B]])

    def test_invalid_anchor_tags_ignored(self):
        bad = doc("Eins\n", [("h1", 0, 5), ("anchor:XYZ", 0, 5)])
        self.assertIsNone(chapters.outline(bad)[0].anchor)


class ChapterReferences(unittest.TestCase):
    def test_uri_roundtrip_and_page_target(self):
        value = refs.chapter_uri("L1", A)
        self.assertEqual(value, "glide://list/L1#" + A)
        self.assertEqual(refs.parse(value), ("list", "L1"))
        self.assertEqual(refs.anchor(value), A)
        self.assertIsNone(refs.anchor("glide://list/L1"))

    def test_invalid_fragments(self):
        for value in ("glide://item/I1#" + A, "glide://list/L1#kurz", "glide://list/L1#" + A.upper()):
            self.assertIsNone(refs.parse(value), value)

    def test_normalize_keeps_anchor(self):
        self.assertEqual(refs.normalize(["glide://list/L1#" + A, "glide://list/L1"]),
                         ["glide://list/L1#" + A, "glide://list/L1"])


class Navigation(unittest.TestCase):
    def setUp(self):
        self.folders = [{"id": "F", "title": "Projekt", "folder_kind": "standard"},
                        {"id": "LIB", "title": "Buch", "folder_kind": "library"}]
        self.lists = [{"id": "P", "list_kind": "page", "folder_id": None, "nav_parent_id": "F"},
                      {"id": "T", "list_kind": "tasks", "folder_id": "F"}]

    def test_page_shown_under_folder_keeps_home_and_kind(self):
        policy = sidebar.SidebarPolicy(self.lists, self.folders)
        self.assertEqual(policy.nav_parent(policy.entries["P"]), "F")
        self.assertEqual(policy.entries["P"]["folder_id"], None)
        self.assertEqual(policy.entries["P"]["list_kind"], "page")
        self.assertEqual(policy.section("list", "P"), "lists")
        self.assertEqual({e["id"] for e in policy.contents["F"]}, {"P", "T"})

    def test_missing_or_archived_target_falls_back_to_home(self):
        self.lists[0]["nav_parent_id"] = "WEG"
        policy = sidebar.SidebarPolicy(self.lists, self.folders)
        self.assertIsNone(policy.nav_parent(policy.entries["P"]))
        self.assertEqual(policy.section("list", "P"), "pages")
        self.folders[0]["archived"] = True
        self.lists[0]["nav_parent_id"] = "F"
        policy = sidebar.SidebarPolicy(self.lists, self.folders)
        self.assertIsNone(policy.nav_parent(policy.entries["P"]))

    def test_nav_problem(self):
        policy = sidebar.SidebarPolicy(self.lists, self.folders)
        self.assertIsNone(policy and sidebar.nav_problem(policy, "P", "F"))
        self.assertIsNone(sidebar.nav_problem(policy, "P", "LIB"))
        self.assertEqual(sidebar.nav_problem(policy, "T", "LIB"), "kind_not_accepted")
        self.assertEqual(sidebar.nav_problem(policy, "P", "WEG"), "missing_folder")
        self.assertEqual(sidebar.nav_problem(policy, "X", "F"), "missing_entry")

    def test_siblings_follow_navigation(self):
        policy = sidebar.SidebarPolicy(self.lists, self.folders)
        self.assertEqual(set(sidebar.sibling_ids(policy, "list", "P")), {"P", "T"})


if __name__ == "__main__":
    unittest.main()
