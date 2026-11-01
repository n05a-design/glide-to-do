"""Werkzeugtests für die Linux-Defektgegenproben; keine App, keine Nutzerdaten."""

from pathlib import Path
import unittest

import linux_gegenproben

APP = Path(__file__).resolve().parents[2] / "src/glide/app.pyw"
INTEGRATION = Path(__file__).resolve().parents[2] / "tests/integration"


class MutationTests(unittest.TestCase):
    """Die Linux-Vollprüfung bricht ab, sobald eine Mutation nicht genau einmal passt (01.11.2026)."""

    def test_every_mutation_matches_exactly_once(self):
        source = APP.read_text(encoding="utf-8")
        for name, _suite, old, *_rest in linux_gegenproben.CASES:
            with self.subTest(name):
                self.assertEqual(source.count(old), 1, f"Mutation {name} ist nicht mehr eindeutig")

    def test_every_suite_exists(self):
        # Das Parsen der Mutante übernimmt die Gegenprobe selbst; hier bliebe es für die Grundstufe zu teuer.
        for name, suite, *_rest in linux_gegenproben.CASES:
            with self.subTest(name):
                self.assertTrue((INTEGRATION / suite).is_file(), suite)


if __name__ == "__main__":
    unittest.main()
