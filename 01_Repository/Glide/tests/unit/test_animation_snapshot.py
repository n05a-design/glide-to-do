"""Zwischenstände und ersetzte Einzelbilder erhalten den Rest der Bildfolge."""
import unittest
from animation import Animation, from_snapshot
from drawing import DrawingFormatError, DrawingModel


class SnapshotContract(unittest.TestCase):
    def test_existing_snapshots_of_all_four_sizes_remain_lossless(self):
        for size in (16, 32, 64, 128):
            model = DrawingModel.blank(size)
            restored = from_snapshot(model.to_json().encode('utf-8'))
            self.assertEqual(restored.frames[0].model.to_document(), model.to_document())
            self.assertEqual(len(restored.frames), 1)

    def test_snapshot_keeps_all_ids_order_and_individual_timing(self):
        sequence = Animation.from_legacy(DrawingModel.blank(32).to_document())
        sequence.add(identity='middle');sequence.duplicate('middle',new_identity='last')
        sequence.move('last',0);sequence.set_duration(625);sequence.set_duration(50,'middle')
        restored = from_snapshot(sequence.to_json())
        self.assertEqual(restored.to_document(),sequence.to_document())
        sequence.remove('middle')
        self.assertEqual([frame.id for frame in restored.frames],['last','frame-1','middle'])
        self.assertEqual(restored.durations(),(625,625,50))

    def test_corrupt_animation_and_duplicate_json_keys_do_not_fall_back(self):
        for text in ('{"format":"glide.animation","frames":[]}',
                     '{"format":"glide.animation","format":"glide.drawing"}',
                     '[1,2]',b'\xff'):
            with self.subTest(text=text), self.assertRaises(DrawingFormatError):
                from_snapshot(text)

    def test_replacing_active_image_keeps_other_frames_and_timing(self):
        sequence = Animation.from_legacy(DrawingModel.blank(16).to_document())
        sequence.add(identity='second');sequence.set_duration(75,'second')
        first = sequence.frames[0]
        incoming = DrawingModel.blank(16)
        sequence.replace_model('second',incoming)
        self.assertIs(sequence.frames[0],first)
        self.assertEqual(sequence.durations(),(150,75))
        self.assertEqual(sequence.frames[1].id,'second')
        self.assertIsNot(sequence.frames[1].model,incoming)
        before = sequence.to_document()
        with self.assertRaises(DrawingFormatError):
            sequence.replace_model('second',DrawingModel.blank(32))
        self.assertEqual(sequence.to_document(),before)

    def test_existing_single_image_can_still_change_size(self):
        sequence = Animation.from_legacy(DrawingModel.blank(16).to_document())
        sequence.set_duration(90,'frame-1')
        sequence.replace_model('frame-1',DrawingModel.blank(128))
        self.assertEqual(sequence.size,128)
        self.assertEqual(sequence.durations(),(90,))
        self.assertEqual(sequence.frames[0].id,'frame-1')


if __name__=='__main__':
    unittest.main()
