# SPDX-License-Identifier: MPL-2.0
"""Werkzeugtests für die Linux-Defektgegenproben; keine App, keine Nutzerdaten."""

from pathlib import Path
import contextlib
import io
import json
import tempfile
import unittest
from unittest import mock

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

    def test_missing_positive_basis_is_visible_and_keeps_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            basis = root / "basis.json"
            basis.write_text(json.dumps({"schritte": []}), encoding="utf-8")
            output = io.StringIO()
            argv = ["linux_gegenproben", "--protokoll", str(root / "logs"),
                    "--fall", "dialogbildlauf", "--basis-ergebnis", str(basis)]
            with mock.patch("sys.argv", argv), contextlib.redirect_stdout(output):
                self.assertEqual(linux_gegenproben.main(), 1)
            self.assertIn("dialogbildlauf: NICHT BELEGT", output.getvalue())
            self.assertIn("test_glide nicht grün oder nicht ausgeführt", output.getvalue())
            result = json.loads((root / "logs/ergebnis.json").read_text(encoding="utf-8"))
            self.assertFalse(result["gegenproben"][0]["gegenprobe_rot"])

    def test_image_scroll_faults_require_their_green_uiux_basis(self):
        for name in ("bildscrollen", "bildscrollen-ohne-wirkung"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                basis = root / "basis.json"
                basis.write_text(json.dumps({"schritte": []}), encoding="utf-8")
                argv = ["linux_gegenproben", "--protokoll", str(root / "logs"),
                        "--fall", name, "--basis-ergebnis", str(basis)]
                with mock.patch("sys.argv", argv), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(linux_gegenproben.main(), 1)
                result = json.loads((root / "logs/ergebnis.json").read_text(encoding="utf-8"))
                self.assertEqual(result["gegenproben"][0]["suite"], "test_uiux_paket.py")
                self.assertFalse(result["gegenproben"][0]["gegenprobe_rot"])


if __name__ == "__main__":
    unittest.main()
