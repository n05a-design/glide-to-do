# SPDX-License-Identifier: MPL-2.0
"""Übernahmewerkzeug der Glide Shell (D95): Kopie, Manifest, Prüfung und Schutz lokaler Änderungen.

Prüft `scripts/pflege/shell_uebernehmen.py` gegen Temporärordner, nie gegen
den Quellbaum: Erstkopie mit Manifest, Prüfung „aktuell“, verweigerte
Übernahme bei lokaler Änderung, bewusstes Ersetzen, veraltete Kopie,
Entfernen nicht mehr gelieferter Dateien bei Erhalt fremder Dateien, Schutz
eigener Dateien vor neuen Shell-Dateien gleichen Namens und die
Sperre gegen ein Ziel im Glide-Quellbaum. Ohne Tk-Import.

Aufruf: python3 -B -m unittest tests/tools/test_shell_uebernahme.py
"""
import contextlib
import importlib.util
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
WERKZEUG = REPO / "scripts" / "pflege" / "shell_uebernehmen.py"
QUELLE = REPO / "src" / "glide" / "glide_shell"

spec = importlib.util.spec_from_file_location("glide_shell_uebernehmen_pruefling", WERKZEUG)
werkzeug = importlib.util.module_from_spec(spec)
spec.loader.exec_module(werkzeug)


def lauf(*argumente):
    ausgabe = io.StringIO()
    with contextlib.redirect_stdout(ausgabe):
        try:
            code = werkzeug.main([str(a) for a in argumente])
        except SystemExit as fehler:
            code = fehler.code
    return code, ausgabe.getvalue()


class Uebernahme(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory(prefix="glide-shell-ueb-")
        self.projekt = pathlib.Path(self._temp.name) / "folgeprojekt"
        self.kopie = self.projekt / "glide_shell"

    def tearDown(self):
        self._temp.cleanup()

    def test_erstkopie_mit_manifest_und_pruefung_aktuell(self):
        code, text = lauf(self.projekt)
        self.assertEqual(code, 0, text)
        quelle = sorted(p.name for p in QUELLE.glob("*.py"))
        self.assertEqual(sorted(p.name for p in self.kopie.glob("*.py")), quelle)
        manifest = json.loads((self.kopie / "SHELL_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["paket"], "glide_shell")
        self.assertEqual(manifest["shell_version"], werkzeug.shell_version())
        self.assertEqual(manifest["lizenz"], "MPL-2.0")
        self.assertIn(manifest["quelle_unveraendert"], (True, False, None))
        self.assertEqual(sorted(manifest["dateien"]), quelle)
        for name, wert in manifest["dateien"].items():
            self.assertEqual(werkzeug.sha(self.kopie / name), wert, name)
        code, text = lauf("--pruefen", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertNotIn("veraltet", text)
        self.assertIn("motion.py: aktuell", text)

    def test_kopie_ist_ohne_glide_importierbar(self):
        lauf(self.projekt)
        kind = ("import sys; sys.path[:] = [p for p in sys.path if 'src' not in p]; "
                f"sys.path.insert(0, {str(self.projekt)!r}); "
                "import glide_shell, glide_shell.motion as m, glide_shell.window_lifetime; "
                f"assert glide_shell.__file__.startswith({str(self.projekt)!r}); "
                "print(glide_shell.SHELL_VERSION, m.progress(0.06, 120) > 0)")
        ergebnis = subprocess.run([sys.executable, "-B", "-c", kind], capture_output=True, text=True,
                                  cwd=self.projekt, timeout=60)
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertEqual(ergebnis.stdout.split(), [werkzeug.shell_version(), "True"])

    def test_lokale_aenderung_wird_nicht_ueberschrieben(self):
        lauf(self.projekt)
        datei = self.kopie / "motion.py"
        datei.write_text(datei.read_text(encoding="utf-8") + "\n# lokale Anpassung\n", encoding="utf-8")
        code, text = lauf("--pruefen", self.projekt)
        self.assertEqual(code, 1)
        self.assertIn("motion.py: verändert", text)
        code, text = lauf(self.projekt)
        self.assertEqual(code, 2, text)
        self.assertIn("lokale Anpassung", datei.read_text(encoding="utf-8"))
        code, text = lauf("--ersetzen", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertEqual(werkzeug.sha(datei), werkzeug.sha(QUELLE / "motion.py"))

    def test_fremder_ordner_ohne_manifest_bleibt_unberuehrt(self):
        self.kopie.mkdir(parents=True)
        (self.kopie / "eigen.py").write_text("x = 1\n", encoding="utf-8")
        code, text = lauf(self.projekt)
        self.assertEqual(code, 2, text)
        self.assertEqual(sorted(p.name for p in self.kopie.iterdir()), ["eigen.py"])

    def test_veraltete_kopie_wird_aktualisiert_und_alte_dateien_entfernt(self):
        lauf(self.projekt)
        pfad = self.kopie / "SHELL_MANIFEST.json"
        manifest = json.loads(pfad.read_text(encoding="utf-8"))
        # Älterer Stand: motion.py hatte anderen Inhalt, dazu ein inzwischen entfallenes Modul.
        alt = b"# SPDX-License-Identifier: MPL-2.0\n# alte Fassung\n"
        (self.kopie / "motion.py").write_bytes(alt)
        (self.kopie / "entfallen.py").write_bytes(alt)
        (self.kopie / "notizen.txt").write_text("vom Folgeprojekt\n", encoding="utf-8")
        manifest["shell_version"] = "0.0.9"
        manifest["dateien"]["motion.py"] = werkzeug.sha(self.kopie / "motion.py")
        manifest["dateien"]["entfallen.py"] = werkzeug.sha(self.kopie / "entfallen.py")
        pfad.write_text(json.dumps(manifest), encoding="utf-8")
        code, text = lauf("--pruefen", self.projekt)
        self.assertEqual(code, 1)
        self.assertIn("Kopie 0.0.9", text)
        self.assertIn("motion.py: veraltet", text)
        self.assertIn("entfallen.py: nicht mehr in der Quelle", text)
        code, text = lauf(self.projekt)
        self.assertEqual(code, 0, text)
        self.assertFalse((self.kopie / "entfallen.py").exists())
        self.assertTrue((self.kopie / "notizen.txt").is_file())
        self.assertIn("notizen.txt: bleibt stehen", text)
        self.assertEqual(lauf("--pruefen", self.projekt)[0], 0)

    def test_eigene_datei_mit_neuem_shellnamen_bleibt_geschuetzt(self):
        lauf(self.projekt)
        pfad = self.kopie / "SHELL_MANIFEST.json"
        manifest = json.loads(pfad.read_text(encoding="utf-8"))
        # Älteres Manifest ohne motion.py; das Folgeprojekt hat eine eigene motion.py angelegt.
        del manifest["dateien"]["motion.py"]
        pfad.write_text(json.dumps(manifest), encoding="utf-8")
        datei = self.kopie / "motion.py"
        datei.write_text("# eigenes Modul des Folgeprojekts\n", encoding="utf-8")
        code, text = lauf(self.projekt)
        self.assertEqual(code, 2, text)
        self.assertIn("motion.py: eigene Datei ohne Manifesteintrag", text)
        self.assertEqual(datei.read_text(encoding="utf-8"), "# eigenes Modul des Folgeprojekts\n")
        self.assertNotIn("motion.py", json.loads(pfad.read_text(encoding="utf-8"))["dateien"])
        code, text = lauf("--ersetzen", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertEqual(werkzeug.sha(datei), werkzeug.sha(QUELLE / "motion.py"))

    def test_ziel_im_glide_quellbaum_wird_abgelehnt(self):
        for ziel in (QUELLE.parent, QUELLE, QUELLE / "unter"):
            with self.subTest(ziel=ziel):
                code, _ = lauf(ziel)
                self.assertNotEqual(code, 0)
        self.assertFalse((QUELLE / "SHELL_MANIFEST.json").exists())
        self.assertFalse((QUELLE / "glide_shell").exists())


if __name__ == "__main__":
    unittest.main()
