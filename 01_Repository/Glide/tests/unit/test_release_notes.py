# SPDX-License-Identifier: MPL-2.0
"""Karte „Neu in …“ (N07) ohne Oberfläche."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import release_notes as rn

KATALOG = {"1.0.1": ("a",), "1.0.2": ("b", "c"), "1.0.3": (), "1.1.0": tuple(f"p{i}" for i in range(7))}


class Neuerungen(unittest.TestCase):
    def test_version_tuple(self):
        self.assertEqual(rn.version_tuple("3.33.20"), (3, 33, 20))
        self.assertEqual(rn.version_tuple(" 3.4 "), (3, 4))
        for unlesbar in (None, "", "3.x", "3..1", "v3.1"):
            self.assertIsNone(rn.version_tuple(unlesbar), unlesbar)

    def test_notes_between_versions_newest_first_and_capped(self):
        self.assertEqual(rn.notes_since("1.0.0", "1.0.2", KATALOG), [("1.0.2", ["b", "c"]), ("1.0.1", ["a"])])
        neu = rn.notes_since("1.0.1", "1.1.0", KATALOG)
        self.assertEqual([version for version, _ in neu], ["1.1.0", "1.0.2"])  # 1.0.3 ohne Eintrag
        self.assertEqual(len(neu[0][1]), 5)  # höchstens fünf Punkte je Version

    def test_card_shows_at_most_three_newest_versions(self):
        # D66 (menschliche Abnahme 07.11.2026): „Gelesen“ ohne langes Scrollen.
        katalog = {f"2.0.{n}": (f"p{n}",) for n in range(1, 9)}
        karte = rn.notes_since("1.0.0", "2.0.8", katalog)
        self.assertEqual([version for version, _ in karte], ["2.0.8", "2.0.7", "2.0.6"])
        self.assertEqual(rn.CARD_VERSIONS, 3)
        self.assertLessEqual(len(rn.notes_since(rn.BEFORE_CATALOG, "3.50.5")), 3)
        # Der Verlauf bleibt vollständig.
        self.assertEqual(len(rn.history("2.0.8", katalog)), 8)
        # Leere Versionen zählen nicht mit.
        katalog["2.0.7"] = ()
        self.assertEqual([v for v, _ in rn.notes_since("1.0.0", "2.0.8", katalog)], ["2.0.8", "2.0.6", "2.0.5"])

    def test_nothing_on_first_start_same_or_older_version(self):
        self.assertEqual(rn.notes_since(None, "1.0.2", KATALOG), [])
        self.assertEqual(rn.notes_since("1.0.2", "1.0.2", KATALOG), [])
        self.assertEqual(rn.notes_since("1.1.0", "1.0.2", KATALOG), [])
        self.assertEqual(rn.notes_since("kaputt", "1.0.2", KATALOG), [])

    def test_last_seen_distinguishes_existing_install(self):
        self.assertEqual(rn.last_seen({"release_notes_seen": "3.33.20"}, False), "3.33.20")
        self.assertEqual(rn.last_seen({}, True), rn.BEFORE_CATALOG)
        self.assertIsNone(rn.last_seen({}, False))
        self.assertEqual(rn.last_seen({"release_notes_seen": 5}, True), rn.BEFORE_CATALOG)
        self.assertTrue(rn.should_show({}, "1.0.1", KATALOG, existing_install=False) is False)

    def test_normalize_seen(self):
        self.assertEqual(rn.normalize_seen(" 3.33.20 "), "3.33.20")
        for unlesbar in (None, 5, "", "neu", ["3.33.20"]):
            self.assertIsNone(rn.normalize_seen(unlesbar), unlesbar)

    def test_remember_seen_leaves_original(self):
        alt = {"x": 1}
        neu = rn.remember_seen(alt, "3.33.20")
        self.assertEqual(neu, {"x": 1, "release_notes_seen": "3.33.20"})
        self.assertEqual(alt, {"x": 1})
        self.assertFalse(rn.should_show(neu, "3.33.20"))

    def test_catalog_entries_are_short_and_versioned(self):
        for version, punkte in rn.CATALOG.items():
            self.assertIsNotNone(rn.version_tuple(version), version)
            self.assertLessEqual(len(punkte), 5, version)
            for punkt in punkte:
                self.assertTrue(punkt.endswith((".", "“")), punkt)
                self.assertLess(len(punkt), 140, punkt)
        self.assertLess(rn.release_rank(rn.BEFORE_CATALOG), min(rn.release_rank(v) for v in rn.CATALOG))

    def test_history_lists_every_version_up_to_current_newest_first(self):
        # B18 (15.10.2026): „Über Glide › Neuerungen“ liest denselben Katalog.
        verlauf = rn.history("1.0.2", KATALOG)
        self.assertEqual(verlauf, [("1.0.2", ["b", "c"]), ("1.0.1", ["a"])])
        self.assertEqual([v for v, _ in rn.history("2.0.0", KATALOG)], ["1.1.0", "1.0.2", "1.0.1"])
        self.assertEqual(len(rn.history("2.0.0", KATALOG)[0][1]), 5)
        # Nach „Gelesen“ bleibt alles nachlesbar: Der Verlauf hängt nicht an der gemerkten Version.
        self.assertEqual(rn.history("1.0.2", KATALOG), rn.history("1.0.2", KATALOG))

    def test_history_text_has_version_headings_and_no_invented_entries(self):
        text = rn.history_text("1.0.2", KATALOG)
        self.assertEqual(text, "Version 1.0.2\n• b\n• c\n\nVersion 1.0.1\n• a")
        self.assertNotIn("1.0.3", rn.history_text("1.1.0", KATALOG))
        self.assertEqual(rn.history_text("0.9", KATALOG), "Für diese Version sind keine Neuerungen hinterlegt.")
        self.assertIn("Version 3.36.0", rn.history_text("3.42.0"))

    def test_official_release_cut_ranks_1_0_0_after_development_series(self):
        # D93 (17.11.2026): 3.70.0 war die letzte Entwicklungsversion, 1.0.0 der erste offizielle Release.
        folge = ["3.33.18", "3.63.0", "3.70.0", "1.0.0", "1.0.1", "1.1.0", "2.0.0"]
        self.assertEqual(sorted(reversed(folge), key=rn.release_rank), folge)
        self.assertIsNone(rn.release_rank("3.x"))

    def test_update_from_development_series_shows_1_0_0_once(self):
        # Bestand mit gemerkter 3.x-Version bekommt die 1.0.0-Karte, danach nie wieder.
        for gemerkt in ("3.70.0", "3.63.0", rn.BEFORE_CATALOG):
            karte = rn.notes_since(gemerkt, "1.0.0")
            self.assertEqual(karte[0][0], "1.0.0", gemerkt)
            self.assertTrue(all(rn.release_rank(v) <= rn.release_rank("1.0.0") for v, _ in karte))
        settings = rn.remember_seen({"release_notes_seen": "3.70.0"}, "1.0.0")
        self.assertFalse(rn.should_show(settings, "1.0.0", existing_install=True))
        # Bestand ohne gemerkte Version zählt als Vorkatalogstand; Erststart zeigt nichts.
        self.assertTrue(rn.should_show({}, "1.0.0", existing_install=True))
        self.assertFalse(rn.should_show({}, "1.0.0", existing_install=False))
        # Rückwärts (1.0.0 gemerkt, 3.x läuft) bleibt leer – keine wiederkehrende Karte.
        self.assertEqual(rn.notes_since("1.0.0", "3.70.0"), [])

    def test_later_official_updates_follow_1_0_0(self):
        katalog = dict(rn.CATALOG, **{"1.0.1": ("x",), "1.1.0": ("y",)})
        self.assertEqual([v for v, _ in rn.notes_since("1.0.0", "1.1.0", katalog)], ["1.1.0", "1.0.1"])
        self.assertEqual([v for v, _ in rn.notes_since("3.70.0", "1.0.1", katalog)][:2], ["1.0.1", "1.0.0"])
        verlauf = [v for v, _ in rn.history("1.0.0")]
        self.assertEqual(verlauf[0], "1.0.0")
        self.assertIn("3.63.0", verlauf)
        self.assertNotIn("1.0.0", [v for v, _ in rn.history("3.70.0")])

    def test_catalog_has_entry_for_running_version(self):
        version = (Path(__file__).resolve().parents[2] / "VERSION").read_text().strip()
        self.assertIn(version, rn.CATALOG)
        self.assertTrue(rn.notes_since(rn.BEFORE_CATALOG, version))

    def test_builtin_notes_follow_interface_language(self):
        import i18n
        vorher = i18n.get_language()
        try:
            i18n.set_language("en")
            englisch = rn.notes_since("1.0.0", "1.0.1")[0][1]
            self.assertIn("tomorrow", englisch[1])
            self.assertNotIn("Schnellerfassung", " ".join(englisch))
            i18n.set_language("de")
            self.assertEqual(rn.notes_since("1.0.0", "1.0.1")[0][1], list(rn.CATALOG["1.0.1"]))
            # Jeder eingebaute Satz hat eine englische Fassung.
            englischer_katalog = i18n.load_catalog("en")
            for version, punkte in rn.CATALOG.items():
                for index, _punkt in enumerate(punkte):
                    self.assertIn(rn.note_key(version, index), englischer_katalog, version)
        finally:
            i18n.set_language(vorher)


if __name__ == "__main__":
    unittest.main()
