import math
import struct
import unittest
import zlib
from logo_raster import alpha_mask, rgba_png

class RasterTests(unittest.TestCase):
    def test_fractional_width_keeps_the_vertical_scale(self):
        from logo_raster import proportional_box
        # A 4.25 × 8 rectangle at height 16 occupies 8.5 pixels, not 9.
        width, box = proportional_box((0., 0., 4.25, 8.), 16)
        mask = alpha_mask((((0., 0.), (4.25, 0.), (4.25, 8.), (0., 8.)),),
                          box, width, 16)
        self.assertEqual(width, 9)
        self.assertEqual(mask[:9], bytes([255] * 8 + [128]))
        self.assertEqual(mask[-9:], mask[:9])
        for height in (0, 4097):
            with self.assertRaises(ValueError): proportional_box((0, 0, 1, 1), height)
        with self.assertRaises(ValueError): proportional_box((0, 0, 1, 0), 16)

    def test_solid_clipping_and_fractional_coverage(self):
        rings = (((-.5, .25), (1.5, .25), (1.5, 2), (-.5, 2)),)
        self.assertEqual(alpha_mask(rings, (0, 0, 2, 2), 2, 2), bytes((191, 96, 255, 128)))

    def test_hole_is_transparent_and_winding_independent(self):
        outer = ((0, 0), (5, 0), (5, 5), (0, 5))
        hole = ((1, 1), (4, 1), (4, 4), (1, 4))
        mask = alpha_mask((outer, hole), (0, 0, 5, 5), 5, 5)
        self.assertEqual(mask, bytes([255] * 5 + [255, 0, 0, 0, 255] * 3 + [255] * 5))
        self.assertEqual(mask, alpha_mask((outer, hole[::-1]), (0, 0, 5, 5), 5, 5))

    def test_separate_shapes_do_not_create_a_bridge(self):
        left = ((0, 0), (1, 0), (1, 1), (0, 1))
        right = tuple((x + 2, y) for x, y in left)
        self.assertEqual(alpha_mask((left, right), (0, 0, 3, 1), 3, 1), b"\xff\0\xff")

    def test_png_channels_size_and_crc(self):
        png = rgba_png(bytes((0, 127, 255, 64)), 2, 2, (1, 133, 225))
        self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
        offset, compressed = 8, b""
        while offset < len(png):
            size = struct.unpack(">I", png[offset:offset + 4])[0]
            kind = png[offset + 4:offset + 8]
            data = png[offset + 8:offset + 8 + size]
            crc = struct.unpack(">I", png[offset + 8 + size:offset + 12 + size])[0]
            self.assertEqual(crc, zlib.crc32(kind + data))
            if kind == b"IHDR":
                self.assertEqual(struct.unpack(">IIBBBBB", data), (2, 2, 8, 6, 0, 0, 0))
            if kind == b"IDAT":
                compressed += data
            offset += size + 12
        self.assertEqual(zlib.decompress(compressed), b"\0\1\x85\xe1\0\1\x85\xe1\x7f\0\1\x85\xe1\xff\1\x85\xe1\x40")

    def test_bad_inputs_rejected(self):
        ring = (((0, 0), (1, 0), (1, 1)),)
        for box, w, h, samples in [((0, 0, 0, 1), 1, 1, 8), ((0, math.nan, 1, 1), 1, 1, 8), ((0, 0, 1, 1), 0, 1, 8), ((0, 0, 1, 1), 1, 1, 0)]:
            with self.assertRaises(ValueError):
                alpha_mask(ring, box, w, h, samples)
        with self.assertRaises(ValueError):
            rgba_png(b"\0", 2, 1, (0, 0, 0))
        with self.assertRaises(ValueError):
            rgba_png(b"\0", 1, 1, (0, 256, 0))

if __name__ == "__main__":
    unittest.main()
