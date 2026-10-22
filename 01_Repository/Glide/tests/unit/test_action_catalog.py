"""Stabile Kennungen: Gruppen und Editorverhalten ohne Beschriftungsabhängigkeit."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import action_catalog as actions


class ActionCatalogTests(unittest.TestCase):
    def test_all_declared_actions_have_a_known_group(self):
        self.assertGreater(len(actions.GROUPS), 90)
        self.assertTrue(set(actions.GROUPS.values()) <= set(actions.GROUP_ORDER))
        self.assertEqual(actions.group_for("export_as_csv"), "Export")
        self.assertEqual(actions.group_for("show_about_dialog"), "Programm und Hilfe")

    def test_saved_view_actions_share_the_view_group(self):
        # FP-03 Stufe 2: „Als Ansicht speichern …“ steht neben den gespeicherten
        # Filtern; ohne Eintrag landete es in „Weitere Aktionen“ (Vollprüfung 3.44.0).
        for name in ("show_manager", "capture_current", "explain_saved_filter"):
            self.assertEqual(actions.group_for(name), "Ansichten", name)
        for label in ("Gespeicherte Filter …", "Als Ansicht speichern …"):
            self.assertEqual(actions.legacy_group(label), "Ansichten", label)

    def test_dynamic_variants_are_grouped_by_id(self):
        for name in ("backdrop.none", "backdrop.pixel-night", "grouping.eisenhower"):
            self.assertEqual(actions.group_for(name), "Ansichtseinstellungen")
        self.assertEqual(actions.group_for("unknown"), "Weitere Aktionen")

    def test_editor_events_use_ids(self):
        for name, event in actions.EDITOR_EVENTS.items():
            self.assertEqual(actions.editor_event(name), event)
        self.assertIsNone(actions.editor_event("Kopieren"))
        self.assertIsNone(actions.editor_event("delete_item"))

    def test_anonymous_callbacks_require_an_explicit_id(self):
        with self.assertRaises(ValueError):
            actions.method_id(lambda: None)
        self.assertEqual(actions.method_id(self.test_editor_events_use_ids),
                         "test_editor_events_use_ids")


if __name__ == "__main__":
    unittest.main()
