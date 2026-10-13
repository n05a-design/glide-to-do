"""Formatbrücke: alte statische Daten bewahren, vollständige Bildfolge atomar speichern."""
import copy
import unittest
from animation import Animation, entry_fields, from_entry
from drawing import DrawingFormatError, DrawingModel


class EntryContract(unittest.TestCase):
    def test_legacy_all_sizes_preserved_without_mutating_entry(self):
        for size in (16, 32, 64, 128):
            with self.subTest(size=size):
                model = DrawingModel.blank(size)
                entry = {"drawing": model.to_document(), "title": "Alte Zeichnung"}
                before = copy.deepcopy(entry)
                animation = from_entry(entry)
                self.assertEqual(animation.frames[0].model.to_document(), before["drawing"])
                self.assertEqual(entry, before)
                self.assertEqual(len(animation.frames), 1)

    def test_roundtrip_keeps_all_frames_order_ids_and_duration(self):
        animation = Animation.from_legacy(DrawingModel.blank(16).to_document())
        added = animation.duplicate("frame-1", new_identity="second")
        animation.set_duration(420)
        animation.set_duration(75, added)
        stored = entry_fields(animation)
        self.assertEqual(from_entry(stored).to_document(), animation.to_document())
        self.assertEqual(stored["drawing"], animation.frames[0].model.to_document())
        animation.remove(added)
        self.assertEqual(len(stored["animation"]["frames"]), 2)

    def test_invalid_sequence_is_never_replaced_by_static_preview(self):
        entry = {"drawing": DrawingModel.blank(16).to_document(), "animation": {"frames": []}}
        with self.assertRaises(DrawingFormatError):
            from_entry(entry)
        self.assertEqual(entry["animation"], {"frames": []})

    def test_different_static_preview_is_rejected(self):
        animation = Animation.from_legacy(DrawingModel.blank(16).to_document())
        stored = entry_fields(animation)
        stored["drawing"] = DrawingModel.blank(32).to_document()
        with self.assertRaisesRegex(DrawingFormatError, "statische Vorschau"):
            from_entry(stored)

    def test_mutated_inconsistent_frame_size_is_rejected_before_save(self):
        animation = Animation.from_legacy(DrawingModel.blank(16).to_document())
        animation.add(identity="second")
        animation.frames[1].model = DrawingModel.blank(32)
        with self.assertRaises(DrawingFormatError):
            entry_fields(animation)

    def test_single_frame_duration_and_identity_survive_save(self):
        animation = Animation.from_legacy(DrawingModel.blank(16).to_document())
        animation.set_duration(860, "frame-1")
        restored = from_entry(entry_fields(animation))
        self.assertEqual(restored.durations(), (860,))
        self.assertEqual(restored.frames[0].id, "frame-1")


if __name__ == "__main__":
    unittest.main()
