"""Pixel-Paket (G19 Palette umfärben, G-03 Symbolvorschau) am Zellmodell, ohne Oberfläche."""
from pathlib import Path
import struct
import sys
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import drawing as d


def ico_bilder(daten):
    """(Größe, RGBA-Zeilen) je Bild einer ICO-Datei mit PNG-Bildern."""
    _reserviert, _typ, anzahl = struct.unpack("<HHH", daten[:6])
    bilder = []
    for nummer in range(anzahl):
        breite, _h, _f, _r, _p, _b, laenge, start = struct.unpack("<BBBBHHII", daten[6 + 16 * nummer:22 + 16 * nummer])
        png = daten[start:start + laenge]
        groesse = struct.unpack(">I", png[16:20])[0]
        idat, pos = b"", 8
        while pos < len(png):
            n = struct.unpack(">I", png[pos:pos + 4])[0]
            art = png[pos + 4:pos + 8]
            if art == b"IDAT":
                idat += png[pos + 8:pos + 8 + n]
            pos += 12 + n
        roh = zlib.decompress(idat)
        zeilen = []
        for y in range(groesse):
            zeile = roh[y * (groesse * 4 + 1) + 1:(y + 1) * (groesse * 4 + 1)]
            zeilen.append([tuple(zeile[i:i + 4]) for i in range(0, len(zeile), 4)])
        bilder.append((groesse, zeilen))
    return bilder


def modell():
    m = d.DrawingModel.blank(16)
    m.paint_cells([(x, y) for x in range(4, 12) for y in range(4, 12)], "#C43BFF")
    m.paint_cells([(0, 0), (15, 15)], "#0072B2")
    m.clear_history()
    return m


class Symbolvorschau(unittest.TestCase):
    def test_preview_matches_exported_ico_pixels(self):
        m = modell()
        for grund in ("#FFFFFF", "#1C1C1E"):
            for groesse, zeilen in ico_bilder(m.to_ico(sizes=(16, 32, 48))):
                vorschau = d.icon_preview_rows(m.width, m.palette, m.cells, groesse, background=grund)
                for y in range(groesse):
                    for x in range(groesse):
                        r, g, b, a = zeilen[y][x]
                        erwartet = d.normalize_color(grund) if a == 0 else f"#{r:02X}{g:02X}{b:02X}"
                        self.assertEqual(d.normalize_color(vorschau[y][x]), d.normalize_color(erwartet),
                                         (grund, groesse, x, y))

    def test_preview_without_transparency_shows_white_ground(self):
        m = modell()
        zeilen = d.icon_preview_rows(m.width, m.palette, m.cells, 16, background="#000000",
                                     transparent_background=False)
        self.assertEqual(d.normalize_color(zeilen[2][2]), "#FFFFFF")


class PaletteUmfaerben(unittest.TestCase):
    def test_replace_is_one_undo_and_keeps_other_colors(self):
        m = modell()
        vorher = bytes(m.cells)
        with m.action("Farbe ersetzen"):
            geaendert = m.replace_color("#C43BFF", "#22813A")
        self.assertEqual(geaendert, 64)
        self.assertEqual(m.undo_count, 1)
        self.assertEqual(m.color_at(5, 5), d.normalize_color("#22813A"))
        self.assertEqual(m.color_at(0, 0), d.normalize_color("#0072B2"))
        self.assertIn(d.normalize_color("#C43BFF"), m.palette)  # alte Farbe bleibt in der Palette
        m.undo()
        self.assertEqual(bytes(m.cells), vorher)

    def test_preview_can_be_reverted_without_history(self):
        m = modell()
        vorher = bytes(m.cells)
        m.begin_action("Farbe ersetzen")
        m.replace_color("#C43BFF", "#22813A")
        self.assertEqual(m.revert_open_action(), 64)
        self.assertIsNone(m.end_action())
        self.assertEqual(bytes(m.cells), vorher)
        self.assertEqual(m.undo_count, 0)

    def test_discard_restores_cells_palette_and_history(self):
        m = modell()
        vorher, palette = bytes(m.cells), list(m.palette)
        m.begin_action("Farbe ersetzen")
        self.assertEqual(m.replace_color("#C43BFF", "#22813A"), 64)
        self.assertIn(d.normalize_color("#22813A"), m.palette)
        self.assertEqual(m.discard_open_action(len(palette)), 64)
        self.assertEqual((bytes(m.cells), m.palette, m.undo_count, m.action_open), (vorher, palette, 0, False))
        # Eine vorhandene Palettenfarbe bleibt, auch wenn sie unbenutzt ist.
        m.ensure_color("#123456")
        lang = len(m.palette)
        m.begin_action("Farbe ersetzen")
        m.replace_color("#C43BFF", "#123456")
        m.discard_open_action(lang)
        self.assertEqual(len(m.palette), lang)


if __name__ == "__main__":
    unittest.main()
