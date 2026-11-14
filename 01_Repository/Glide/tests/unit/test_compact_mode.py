# SPDX-License-Identifier: MPL-2.0
"""E-U1 A: Geometrieregeln des Kompaktmodus (getrennte Fensterlagen, Mindestgröße)."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import compact_mode


class ShortcutTests(unittest.TestCase):
    def test_pair_and_repeated_press_toggle_once(self):
        step = compact_mode.shortcut_transition
        self.assertEqual(step(False, released=False, modifiers=5), (True, 'toggle'))
        self.assertEqual(step(True, released=False, modifiers=5), (True, 'consume'))
        self.assertEqual(step(True, released=True, modifiers=0), (False, 'consume'))

    def test_release_fallback_requires_both_modifiers(self):
        for macos in (True, False):
            for state in range(16):
                valid = bool(state & 1 and state & (12 if macos else 4))
                self.assertEqual(compact_mode.shortcut_transition(
                    False, released=True, modifiers=state, macos=macos),
                    (False, 'toggle' if valid else 'pass'))


class ParseTests(unittest.TestCase):
    def test_parse_and_format(self):
        self.assertEqual(compact_mode.parse('1280x800+20+30'), (1280, 800, 20, 30))
        # „+-5“ ist eine Lage links vom Hauptbildschirm, „-5“ der Abstand vom rechten Rand (keine Lage).
        self.assertEqual(compact_mode.parse('480x560+-5+0'), (480, 560, -5, 0))
        self.assertEqual(compact_mode.parse('480x560-5+0'), (480, 560, None, None))
        self.assertEqual(compact_mode.parse('480x560+5-0'), (480, 560, None, None))
        self.assertEqual(compact_mode.parse('900x700'), (900, 700, None, None))
        for value in ('', None, 'groß', '0x10+1+1', '99999x10', '1x1+2'):
            self.assertIsNone(compact_mode.parse(value), value)
        self.assertEqual(compact_mode.format_geometry(480, 560, -5, 10), '480x560+-5+10')
        self.assertEqual(compact_mode.parse(compact_mode.format_geometry(480, 560, -1700, -20)), (480, 560, -1700, -20))
        self.assertEqual(compact_mode.format_geometry(480, 560), '480x560')

    def test_normalize_saved(self):
        self.assertEqual(compact_mode.normalize_saved('500x700+10+20'), '500x700+10+20')
        self.assertEqual(compact_mode.normalize_saved('400x700+10+20'), '')
        self.assertEqual(compact_mode.normalize_saved('500x500+10+20'), '')
        self.assertEqual(compact_mode.normalize_saved(42), '')


class GeometryTests(unittest.TestCase):
    def test_default_keeps_right_edge_and_height(self):
        result = compact_mode.parse(compact_mode.compact_geometry('1280x860+100+40', '', 1920, 1080))
        self.assertEqual(result, (480, 860, 100 + 1280 - 480, 40))

    def test_minimum_height_and_screen_clamp(self):
        result = compact_mode.parse(compact_mode.compact_geometry('1280x500+1700+40', '', 1920, 1080))
        width, height, x, _y = result
        self.assertEqual((width, height), (480, 560))
        self.assertLessEqual(x, 1920 - compact_mode.VISIBLE_MARGIN)
        tall = compact_mode.parse(compact_mode.compact_geometry('900x1400+0+0', '', 1920, 1000))
        self.assertEqual(tall[1], 1000 - compact_mode.SCREEN_RESERVE)

    def test_saved_geometry_wins_and_stays_visible(self):
        self.assertEqual(compact_mode.compact_geometry('1280x860+0+0', '520x700+30+40', 1920, 1080),
                         '520x700+30+40')
        moved = compact_mode.parse(compact_mode.compact_geometry('1280x860+0+0', '520x700+5000+40', 1920, 1080))
        self.assertEqual(moved[2], 1920 - compact_mode.VISIBLE_MARGIN)
        # Ungültige Merklage fällt auf die Ableitung zurück.
        derived = compact_mode.parse(compact_mode.compact_geometry('1280x860+0+0', '300x300+0+0', 1920, 1080))
        self.assertEqual(derived[:2], (480, 860))

    def test_second_monitor_on_virtual_desktop(self):
        # Windows: Hauptbildschirm 1920 breit, zweiter rechts daneben (virtuell 0..3840).
        rechts = compact_mode.parse(compact_mode.compact_geometry('1280x900+2200+50', '', 3840, 1080))
        self.assertEqual(rechts, (480, 900, 2200 + 1280 - 480, 50))
        gemerkt = compact_mode.compact_geometry('1280x860+0+0', '480x700+3000+40', 3840, 1080)
        self.assertEqual(gemerkt, '480x700+3000+40')
        # Zweiter Bildschirm links: negative Koordinaten bleiben erhalten.
        links = compact_mode.parse(compact_mode.compact_geometry('1280x900+-1700+60', '', 3840, 1080,
                                                                 origin=(-1920, 0)))
        self.assertEqual(links, (480, 900, -1700 + 1280 - 480, 60))
        weit = compact_mode.parse(compact_mode.compact_geometry('1280x860+0+0', '480x700+-5000+40', 3840, 1080,
                                                                origin=(-1920, 0)))
        self.assertEqual(weit[2], -1920 - (480 - compact_mode.VISIBLE_MARGIN))
        # Nur der Hauptbildschirm bekannt (Rückfall): wie bisher auf ihn geholt.
        haupt = compact_mode.parse(compact_mode.compact_geometry('1280x900+2200+50', '', 1920, 1080))
        self.assertEqual(haupt[2], 1920 - compact_mode.VISIBLE_MARGIN)

    def test_without_position(self):
        self.assertEqual(compact_mode.compact_geometry('', '', 1920, 1080), '480x760')
        self.assertEqual(compact_mode.compact_geometry('1000x800', '', 0, 0), '480x800')

    def test_normal_geometry(self):
        self.assertEqual(compact_mode.normal_geometry('1280x860+10+10', '480x700+800+10'), '1280x860+10+10')
        self.assertEqual(compact_mode.normal_geometry('', '480x600+800+10'), '860x700+800+10')
        self.assertEqual(compact_mode.normal_geometry(None, None), '1280x860')


class NormalPositionTests(unittest.TestCase):
    """Lageregel der Normalansicht (`ListApp.clamp_geometry` bleibt die Fassade)."""

    def test_position_on_area_stays(self):
        self.assertEqual(compact_mode.keep_visible(100, 50, 980, (0, 0, 1920, 1080)), (100, 50))
        # Genau an der Grenze bleibt die Lage, ein Pixel weiter wird sie geholt.
        rand = 1920 - compact_mode.VISIBLE_MARGIN
        self.assertEqual(compact_mode.keep_visible(rand, 0, 980, (0, 0, 1920, 1080)), (rand, 0))
        self.assertEqual(compact_mode.keep_visible(rand + 1, -1, 980, (0, 0, 1920, 1080)), (rand, 0))

    def test_left_and_upper_monitor_and_its_removal(self):
        # Bildschirm links und über dem Hauptbildschirm: negative Lage bleibt.
        self.assertEqual(compact_mode.keep_visible(-1550, -90, 860, (-1920, -100, 3840, 1180)), (-1550, -90))
        # Derselbe Stand ohne diesen Bildschirm: Ein 120-px-Streifen bleibt links sichtbar.
        self.assertEqual(compact_mode.keep_visible(-1550, -90, 860, (0, 0, 1920, 1080)), (-740, 0))

    def test_far_outside_and_wider_than_area(self):
        self.assertEqual(compact_mode.keep_visible(6000, 5000, 980, (0, 0, 1920, 1080)), (1800, 960))
        # Die Maße gehören nicht zur Regel: Ein zu breites Fenster behält sie.
        self.assertEqual(compact_mode.keep_visible(-5000, 10, 3000, (0, 0, 1280, 800)), (-2880, 10))

    def test_margin_and_empty_area(self):
        self.assertEqual(compact_mode.keep_visible(6000, 5000, 980, (0, 0, 1920, 1080), margin=200), (1720, 880))
        self.assertEqual(compact_mode.keep_visible(-5000, 0, 980, (0, 0, 1920, 1080), margin=200), (-780, 0))
        # Anders als `clamp` ohne Schutz für eine leere Fläche – der Stand vor der Auslagerung.
        self.assertEqual(compact_mode.keep_visible(10, 10, 980, (0, 0, 0, 0)), (-120, 0))


if __name__ == '__main__':
    unittest.main()
