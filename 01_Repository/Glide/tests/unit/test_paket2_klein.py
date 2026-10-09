"""KO05 Zeilen, KO06 zuletzt benutzte Ziele, N07 „Neu in …“ ohne Oberfläche."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import capture_parser as c
import interaction_policy as ip
import release_notes as rn


class Zeilen(unittest.TestCase):
    def test_bullets_numbers_and_boxes(self):
        text = "- Milch kaufen\n\n* Brot  holen\n1. Bank\n2) Post\n- [ ] offen\n- [x] erledigt\n[✓] auch fertig\n• Punkt\na) Buchstabe"
        zeilen, ab = c.split_capture_lines(text)
        self.assertFalse(ab)
        self.assertEqual([z["text"] for z in zeilen],
                         ["Milch kaufen", "Brot holen", "Bank", "Post", "offen", "erledigt", "auch fertig", "Punkt", "Buchstabe"])
        self.assertEqual([z["done"] for z in zeilen], [False] * 5 + [True, True, False, False])

    def test_limit_and_empty(self):
        zeilen, ab = c.split_capture_lines("\n".join(f"Zeile {i}" for i in range(205)))
        self.assertEqual((len(zeilen), ab), (200, True))
        self.assertEqual(c.split_capture_lines("  \n\n "), ([], False))

    def test_dates_stay_for_parser(self):
        zeilen, _ = c.split_capture_lines("- Bericht morgen 14:00\n- Steuer bis Freitag")
        self.assertEqual(zeilen[0]["text"], "Bericht morgen 14:00")


class ZuletztBenutzt(unittest.TestCase):
    def test_remember(self):
        self.assertEqual(ip.remember_recent(["b", "a", "c"], "a"), ["a", "b", "c"])
        self.assertEqual(ip.remember_recent(["1", "2", "3", "4", "5"], "6"), ["6", "1", "2", "3", "4"])
        self.assertEqual(ip.remember_recent("kaputt", "x"), ["x"])
        self.assertEqual(ip.remember_recent(["a", 5, "", "a"], "b"), ["b", "a"])

    def test_recent_first_keeps_every_key_once(self):
        vorn, rest = ip.recent_first(["l1", "l2", "l3", "l4"], ["l3", "weg", "l1", "l3"])
        self.assertEqual((vorn, rest), (["l3", "l1"], ["l2", "l4"]))
        vorn, rest = ip.recent_first(["a"], None)
        self.assertEqual((vorn, rest), ([], ["a"]))


class NeuIn(unittest.TestCase):
    KATALOG = {"3.33.19": ["Schneller"], "3.33.20": ["A", "B", "C", "D", "E", "F"], "3.34.0": ["Wissen"]}

    def test_first_start_shows_nothing(self):
        self.assertEqual(rn.notes_since(None, "3.33.20", self.KATALOG), [])
        self.assertFalse(rn.should_show({}, "3.33.20", self.KATALOG))

    def test_versions_between_newest_first_max_five(self):
        notes = rn.notes_since("3.33.18", "3.33.20", self.KATALOG)
        self.assertEqual([v for v, _ in notes], ["3.33.20", "3.33.19"])
        self.assertEqual(len(notes[0][1]), 5)
        self.assertEqual(rn.notes_since("3.33.20", "3.33.20", self.KATALOG), [])
        self.assertEqual(rn.notes_since("3.34.0", "3.33.20", self.KATALOG), [])

    def test_seen_is_remembered(self):
        settings = {"release_notes_seen": "3.33.18"}
        self.assertTrue(rn.should_show(settings, "3.33.19", self.KATALOG))
        neu = rn.remember_seen(settings, "3.33.19")
        self.assertEqual(settings["release_notes_seen"], "3.33.18")
        self.assertFalse(rn.should_show(neu, "3.33.19", self.KATALOG))

    def test_existing_install_without_key_sees_catalog(self):
        self.assertEqual(rn.last_seen({}, existing_install=True), rn.BEFORE_CATALOG)
        self.assertIsNone(rn.last_seen({}, existing_install=False))
        self.assertTrue(rn.should_show({}, "3.33.20", existing_install=True))
        self.assertFalse(rn.should_show({}, "3.33.20", existing_install=False))
        self.assertTrue(all(len(punkte) <= 5 for punkte in rn.CATALOG.values()))

    def test_version_tuple(self):
        self.assertEqual(rn.version_tuple("3.33.20"), (3, 33, 20))
        self.assertIsNone(rn.version_tuple("3.33.x"))
        self.assertLess(rn.version_tuple("3.33.9"), rn.version_tuple("3.33.10"))


if __name__ == "__main__":
    unittest.main()
