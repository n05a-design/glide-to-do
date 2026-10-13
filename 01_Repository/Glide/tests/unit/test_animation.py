"""Bildfolgen mit echten Zellmodellen, Archiv-Rundlauf und PNG-Pixelvergleich."""
import copy
import json
import struct
import unittest
import zlib

from animation import Animation, Frame, MAX_FRAMES, MAX_JSON_BYTES
from drawing import DrawingFormatError, DrawingModel


def artwork(color="#1234AB", size=16):
    model = DrawingModel.blank(size)
    model.set_cell(0, 0, color)
    model.set_cell(size - 1, size - 1, "#EE0099")
    model.clear_history()
    return model


def image(png):
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    chunks = {}
    pos = 8
    while pos < len(png):
        count = struct.unpack_from(">I", png, pos)[0]
        kind = png[pos + 4:pos + 8]
        payload = png[pos + 8:pos + 8 + count]
        assert zlib.crc32(kind + payload) == struct.unpack_from(">I", png, pos + 8 + count)[0]
        chunks[kind] = chunks.get(kind, b"") + payload
        pos += count + 12
    width, height, depth, kind, compression, filtering, interlace = struct.unpack(">IIBBBBB", chunks[b"IHDR"])
    assert (depth, compression, filtering, interlace) == (8, 0, 0, 0)
    channels = 4 if kind == 6 else 1
    assert kind in (3, 6)
    raw = zlib.decompress(chunks[b"IDAT"])
    assert len(raw) == height * (width * channels + 1)
    palette = [tuple(chunks[b"PLTE"][offset:offset + 3]) + (255,)
               for offset in range(0, len(chunks.get(b"PLTE", b"")), 3)]
    pixels = []
    for y in range(height):
        offset = y * (width * channels + 1)
        assert raw[offset] == 0
        row = raw[offset + 1:offset + 1 + width * channels]
        pixels.append([tuple(row[x * 4:x * 4 + 4]) if kind == 6 else palette[row[x]]
                       for x in range(width)])
    return width, height, pixels


class AnimationTests(unittest.TestCase):
    def test_legacy_palette_and_all_cells_survive(self):
        for size in (16, 32, 64, 128):
            before = artwork(size=size).to_document()
            animated = Animation.from_legacy(before)
            self.assertEqual(animated.frames[0].model.to_document(), before)
            self.assertEqual(before, artwork(size=size).to_document())
            self.assertEqual(animated.durations(), (150,))

    def test_roundtrip_preserves_order_ids_frames_and_durations(self):
        animation = Animation.from_legacy(artwork().to_document())
        animation.duplicate("frame-1", new_identity="copy")
        animation.add(after="copy", identity="blank")
        animation.move("blank", 0)
        animation.set_duration(220)
        animation.set_duration(65, "copy")
        animation.frames[2].model.set_cell(8, 9, "#FFAA00")
        parsed = Animation.from_json(animation.to_json().encode("utf-8"))
        self.assertEqual(parsed.to_document(), animation.to_document())
        self.assertEqual(parsed.model_hash(), animation.model_hash())
        self.assertEqual(parsed.durations(), (220, 220, 65))

    def test_duplicate_is_independent_and_has_own_pixel_history(self):
        animation = Animation.from_legacy(artwork().to_document())
        identity = animation.duplicate("frame-1", new_identity="copy")
        first, second = animation.frames
        self.assertEqual(identity, "copy")
        with second.model.action("Nur Kopie"):
            second.model.set_cell(5, 5, "#000000")
        self.assertEqual(first.model.color_at(5, 5), "#FFFFFF")
        self.assertEqual(second.model.undo_count, 1)
        self.assertEqual(first.model.undo_count, 0)
        second.model.undo()
        self.assertEqual([first.model.color_at(x, y) for y in range(16) for x in range(16)],
                         [second.model.color_at(x, y) for y in range(16) for x in range(16)])
        self.assertNotIn("#000000", first.model.palette)
        self.assertIn("#000000", second.model.palette)

    def test_insert_move_remove_selects_existing_neighbour(self):
        animation = Animation.from_legacy(artwork().to_document())
        animation.add(identity="end")
        animation.add(after="frame-1", identity="middle")
        self.assertEqual([f.id for f in animation.frames], ["frame-1", "middle", "end"])
        self.assertTrue(animation.move("frame-1", 2))
        before = animation.to_document()
        self.assertFalse(animation.move("frame-1", 2))
        self.assertEqual(before, animation.to_document())
        self.assertEqual(animation.remove("frame-1"), "end")
        self.assertEqual(animation.remove("middle"), "end")
        with self.assertRaises(DrawingFormatError):
            animation.remove("end")

    def test_failed_operations_do_not_change_document(self):
        animation = Animation.from_legacy(artwork().to_document())
        for action in (lambda: animation.add(identity="frame-1"),
                       lambda: animation.duplicate("missing"),
                       lambda: animation.move("frame-1", 3),
                       lambda: animation.move("frame-1", True),
                       lambda: animation.set_duration(19),
                       lambda: animation.set_duration(60_001, "frame-1")):
            before = animation.to_document()
            with self.assertRaises(DrawingFormatError):
                action()
            self.assertEqual(before, animation.to_document())

    def test_frame_limit_rejects_add_and_duplicate(self):
        animation = Animation([Frame(f"f-{i}", DrawingModel.blank(16)) for i in range(MAX_FRAMES)])
        before = animation.model_hash()
        for action in (animation.add, lambda: animation.duplicate("f-0")):
            with self.assertRaises(DrawingFormatError):
                action()
        self.assertEqual(before, animation.model_hash())

    def test_shared_duration_keeps_overrides_and_override_can_be_removed(self):
        animation = Animation.from_legacy(artwork().to_document())
        animation.add(identity="second")
        self.assertTrue(animation.set_duration(80, "second"))
        self.assertTrue(animation.set_duration(400))
        self.assertEqual(animation.durations(), (400, 80))
        self.assertFalse(animation.set_duration(80, "second"))
        self.assertTrue(animation.set_duration(None, "second"))
        self.assertEqual(animation.durations(), (400, 400))

    def test_playback_boundaries_loop_and_late_callback(self):
        animation = Animation([Frame("a", artwork(), 100), Frame("b", artwork(), 200)], 150)
        for elapsed, index, remaining in ((0, 0, 100), (99.5, 0, 1), (100, 1, 200),
                                          (299, 1, 1), (300, 0, 100), (120_250, 1, 50)):
            tick = animation.playback(elapsed)
            self.assertEqual((tick.index, tick.remaining_ms, tick.finished), (index, remaining, False))
            self.assertEqual(tick.frame_id, animation.frames[index].id)
        end = animation.playback(300, loop=False)
        self.assertEqual((end.index, end.remaining_ms, end.finished), (1, 0, True))

    def test_invalid_times_and_durations_are_rejected(self):
        animation = Animation.from_legacy(artwork().to_document())
        for value in (False, -1, float("inf"), float("nan"), "100", None):
            with self.assertRaises(DrawingFormatError):
                animation.playback(value)
        for value in (False, 20.0, 0, 60_001, "150", None):
            with self.assertRaises(DrawingFormatError):
                animation.set_duration(value)

    def test_invalid_contracts_are_visible_errors(self):
        base = Animation.from_legacy(artwork().to_document()).to_document()
        bads = []
        for field, value in (("format_version", True), ("format_version", 2),
                             ("width", 32), ("height", True), ("frames", []), ("duration_ms", False)):
            bad = copy.deepcopy(base); bad[field] = value; bads.append(bad)
        bad = copy.deepcopy(base); bad["future"] = 1; bads.append(bad)
        bad = copy.deepcopy(base); bad["frames"][0]["id"] = "../frame"; bads.append(bad)
        bad = copy.deepcopy(base); bad["frames"] *= 2; bads.append(bad)
        bad = copy.deepcopy(base); bad["frames"][0]["duration_ms"] = 1; bads.append(bad)
        bad = copy.deepcopy(base); bad["frames"][0]["future"] = 1; bads.append(bad)
        for bad in bads:
            with self.subTest(bad=bad), self.assertRaises(DrawingFormatError):
                Animation.from_document(bad)

    def test_invalid_json_and_duplicate_keys_are_rejected(self):
        for text in ('{"format": "a", "format": "b"}', "[]", "{", b"\xff",
                     b"x" * (MAX_JSON_BYTES + 1)):
            with self.assertRaises(DrawingFormatError):
                Animation.from_json(text)

    def test_sequence_pngs_and_manifest_match_frames_exactly(self):
        animation = Animation([Frame("red", artwork("#FF0000"), 100),
                               Frame("blue", artwork("#0000FF"))], 200)
        before = animation.model_hash()
        files = animation.png_sequence(2)
        self.assertEqual(set(files), {"bild-001.png", "bild-002.png", "animation.json"})
        manifest = json.loads(files["animation.json"])
        self.assertEqual([f["duration_ms"] for f in manifest["frames"]], [100, 200])
        for frame, record in zip(animation.frames, manifest["frames"]):
            width, height, pixels = image(files[record["file"]])
            self.assertEqual((width, height), (32, 32))
            for y in range(height):
                for x in range(width):
                    self.assertEqual(pixels[y][x], tuple(bytes.fromhex(frame.model.color_at(x // 2, y // 2)[1:])) + (255,))
        self.assertEqual(before, animation.model_hash())

    def test_sheet_pixel_positions_scale_padding_and_manifest(self):
        animation = Animation([Frame(f"f{i}", artwork(color), 100 + i * 50)
                               for i, color in enumerate(("#FF0000", "#00FF00", "#0000FF"))])
        before = animation.to_document()
        png, manifest = animation.png_spritesheet(scale=3)
        width, height, pixels = image(png)
        self.assertEqual((width, height), (96, 96))
        self.assertEqual((manifest["columns"], manifest["rows"]), (2, 2))
        for index, frame in enumerate(animation.frames):
            record = manifest["frames"][index]
            self.assertEqual(record["duration_ms"], 100 + index * 50)
            for y in range(48):
                for x in range(48):
                    self.assertEqual(pixels[record["y"] + y][record["x"] + x],
                                     tuple(bytes.fromhex(frame.model.color_at(x // 3, y // 3)[1:])) + (255,))
        self.assertTrue(all(pixel[3] == 0 for row in pixels[48:] for pixel in row[48:]))
        self.assertEqual(animation.to_document(), before)

    def test_sheet_can_preserve_more_than_256_distinct_colors(self):
        models = []
        for prefix in (1, 2):
            palette = ["#FFFFFF"] + [f"#{prefix:02X}{value:02X}00" for value in range(255)]
            models.append(DrawingModel(palette, bytes(range(256)), size=16))
        animation = Animation([Frame("a", models[0]), Frame("b", models[1])])
        width, height, pixels = image(animation.png_spritesheet(columns=2)[0])
        self.assertEqual((width, height), (32, 16))
        self.assertEqual(len({pixel for row in pixels for pixel in row}), 511)

    def test_export_size_limits_are_explicit_and_non_destructive(self):
        animation = Animation([Frame(f"f-{i}", DrawingModel.blank(128)) for i in range(18)])
        before = animation.model_hash()
        for options in ({"scale": 0}, {"scale": True}, {"columns": 19}, {"columns": False},
                        {"columns": 1, "scale": 16}, {"columns": 3, "scale": 16}):
            with self.assertRaises(DrawingFormatError):
                animation.png_spritesheet(**options)
        with self.assertRaises(DrawingFormatError):
            animation.png_sequence(17)
        self.assertEqual(before, animation.model_hash())


if __name__ == "__main__":
    unittest.main()
