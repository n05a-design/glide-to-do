# SPDX-License-Identifier: MPL-2.0
"""Bento 0.2.0 im isolierten Fremdhost (Phase B 3.7): Kopie von `glide_bento` und
`glide_shell` in einen leeren Ordner, Start mit `python -I` ohne Glide-Quellbaum.

Prüft Importierbarkeit, eigene Theme-/Token-Provider, Multi-Span, Breakpoints,
Themen- und Sprachwechsel, Abbau und den autonomen Selbsttest.
"""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
HOST = Path(__file__).resolve().parents[1] / "fixtures" / "bento_referenzhost" / "host.py"


class BentoReferenzhostTests(unittest.TestCase):
    def setUp(self):
        try:
            import tkinter
            tkinter.Tk().destroy()
        except Exception as exc:  # noqa: BLE001
            self.skipTest(f"Tk nicht verfügbar: {exc}")
        self.ordner = Path(tempfile.mkdtemp(prefix="bento-ref-"))
        for paket in ("glide_bento", "glide_shell"):
            shutil.copytree(SRC / paket, self.ordner / paket, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy(HOST, self.ordner / "host.py")

    def tearDown(self):
        shutil.rmtree(self.ordner, ignore_errors=True)

    def lauf(self, code):
        return subprocess.run([sys.executable, "-B", "-I", "-c", "import sys; sys.path.insert(0, '.'); " + code],
                              cwd=self.ordner, capture_output=True, text=True, timeout=180)

    def test_fremdhost_ohne_glide(self):
        r = self.lauf("import runpy; runpy.run_path('host.py', run_name='__main__')")
        self.assertEqual(r.returncode, 0, r.stderr[-2000:])
        self.assertIn("Referenzhost OK", r.stdout)

    def test_selbsttest_in_der_kopie(self):
        r = self.lauf("from glide_bento import selftest; sys.exit(0 if selftest.BentoSelftestRunner().run_all() else 1)")
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-1000:])
        self.assertIn("16/16", r.stdout)


if __name__ == "__main__":
    unittest.main()
