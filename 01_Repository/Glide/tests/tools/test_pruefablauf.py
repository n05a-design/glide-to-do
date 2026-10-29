"""WA-42: echte kleine Kindprozesse; keine Glide-/Last-/Nutzerdatenprüfung."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pruefablauf as flow
import pruefen


class PruefablaufTests(unittest.TestCase):
    def test_runtime_records_hardware_even_without_a_failure(self):
        context = {"cpu": "Intel Core i9-14900K", "cpu_hersteller": "GenuineIntel", "board": "Testboard"}
        with patch.object(flow, "systemkontext", return_value=context):
            runtime = flow.laufzeit()
        self.assertEqual(runtime["systemkontext"], context)
        self.assertEqual(runtime["pruefplatz"]["cpu_familie"], "intel")
        self.assertIn("executable_sha256", runtime)
        self.assertNotIn("diagnose", runtime)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="wa42-test-", dir=flow.lokale_ablage())
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "projekt"
        self.repo = self.project / "01_Repository/Glide"
        self.source = self.repo / "src/glide/app.pyw"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("APP_VERSION = 'test'\n", encoding="utf-8")
        self.doc = self.repo / "docs/test.md"
        self.doc.parent.mkdir()
        self.doc.write_text("Dokument\n", encoding="utf-8")
        self.guard = flow.Pruefablauf(self.repo, self.root / "arbeit", runtime=lambda: {"python": "test"})

    def command(self, code, name="probe", timeout=10):
        return self.guard.command(name, [sys.executable, "-B", "-c", code], timeout=timeout)

    def test_getrennte_daten_und_temp_pro_prozess(self):
        code = "import json,os,tempfile;print(json.dumps([os.environ['GLIDE_DATA_DIR'],tempfile.gettempdir()]))"
        first = json.loads(self.command(code, "eins").stdout)
        second = json.loads(self.command(code, "zwei").stdout)
        self.assertNotEqual(first, second)
        for data, temporary in (first, second):
            self.assertTrue(Path(data).is_relative_to(self.guard.root))
            self.assertTrue(Path(temporary).is_relative_to(self.guard.root))
            self.assertNotEqual(data, temporary)
        self.assertEqual(len(self.guard.rows), 2)
        self.assertTrue(all(row["passed"] for row in self.guard.rows))

    def test_fehlende_datei_vor_fall_stoppt_ohne_prozess(self):
        self.source.unlink()
        self.assertIsNone(self.command("raise AssertionError('darf nicht laufen')"))
        self.assertTrue(self.guard.stopped)
        self.assertEqual(self.guard.rows, [])
        self.assertEqual(len(self.guard.report["integrity_stop"]["source"]), 1)

    def test_neue_eingabedatei_wird_erkannt(self):
        self.source.with_name("neu.py").write_text("x=1\n", encoding="utf-8")
        self.assertIsNone(self.command("pass"))
        self.assertIn("neu.py", self.guard.report["integrity_stop"]["source"][0])

    def test_aenderung_waehrend_fall_stoppt_folge(self):
        code = f"from pathlib import Path;Path({str(self.source)!r}).write_text('geaendert',encoding='utf-8')"
        self.assertEqual(self.command(code).returncode, 0)
        self.assertFalse(self.guard.rows[-1]["passed"])
        self.assertIsNone(self.command("raise AssertionError('Folge darf nicht laufen')", "folge"))
        self.assertEqual(len(self.guard.rows), 1)
        self.assertTrue((self.guard.root / "001-probe/prozess.log").is_file())

    def test_dokumentabweichung_getrennt_mit_stopp(self):
        self.doc.write_text("Neuer Stand", encoding="utf-8")
        self.assertIsNone(self.command("pass"))
        change = self.guard.report["integrity_stop"]
        self.assertEqual(change["source"], [])
        self.assertEqual(change["documents"], ["01_Repository/Glide/docs/test.md"])

    def test_roter_prozess_stoppt_auch_ohne_dateiaenderung(self):
        self.assertEqual(self.command("raise SystemExit(7)").returncode, 7)
        self.assertTrue(self.guard.stopped)
        self.assertIsNone(self.command("pass", "folge"))
        proof = json.loads((self.guard.root / "pruefablauf.json").read_text(encoding="utf-8"))
        self.assertEqual(proof["cases"][0]["returncode"], 7)

    def test_timeout_beleg_und_folgestopp(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            self.command("import time;print('started',flush=True);time.sleep(10)", timeout=.05)
        self.assertTrue(self.guard.stopped)
        self.assertEqual(self.guard.rows[-1]["error"], "TimeoutExpired")
        self.assertIsNone(self.command("pass", "folge"))

    def test_lesefehler_stoppt(self):
        self.guard.inventory = lambda repo: (_ for _ in ()).throw(PermissionError())
        self.assertIsNone(self.command("pass"))
        self.assertEqual(self.guard.report["integrity_stop"]["read_error"], "PermissionError")

    def test_prueflauf_adapter_meldet_folge_als_nicht_ausgefuehrt(self):
        run = pruefen.Prueflauf(None, 10, waechter=self.guard)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(run.prozess("rot", [sys.executable, "-B", "-c", "raise SystemExit(3)"]))
            self.assertFalse(run.prozess("folge", [sys.executable, "-B", "-c", "pass"]))
            called = []
            self.assertFalse(run.funktion("spaeter", lambda: called.append(True)))
        self.assertEqual(called, [])
        self.assertEqual([row["status"] for row in run.results],
                         ["fehlgeschlagen", "übersprungen", "übersprungen"])
        self.assertEqual(len(self.guard.rows), 1)

    def test_unsichere_ablagen_werden_abgelehnt(self):
        for path in (self.root / "OneDrive", Path(tempfile.gettempdir()) / "glide"):
            with self.assertRaises(ValueError):
                flow.lokale_ablage(path)

    def test_einfrieren_erhaelt_aktuelle_bytes_und_eigene_githistorie(self):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.project), *args],
                                  capture_output=True, timeout=30, check=True)
        git("init", "--quiet")
        git("config", "user.name", "Test")
        git("config", "user.email", "test@example.invalid")
        git("add", ".")
        git("commit", "--quiet", "-m", "baseline")
        self.source.write_text("APP_VERSION='lokal'\n", encoding="utf-8")
        new = self.source.with_name("neu.py")
        new.write_text("VALUE=2\n", encoding="utf-8")
        before = git("status", "--porcelain").stdout
        frozen, root = flow.einfrieren(self.repo, self.root / "kopien")
        self.assertEqual((frozen / "src/glide/app.pyw").read_bytes(), self.source.read_bytes())
        self.assertEqual((frozen / "src/glide/neu.py").read_bytes(), new.read_bytes())
        self.assertEqual(git("status", "--porcelain").stdout, before)
        self.assertTrue((frozen.parents[1] / ".git").is_dir())
        proof = json.loads((root / "quellstand.json").read_text(encoding="utf-8"))
        self.assertTrue(proof["source_unchanged"] and proof["copy_equal"])


if __name__ == "__main__":
    unittest.main()
