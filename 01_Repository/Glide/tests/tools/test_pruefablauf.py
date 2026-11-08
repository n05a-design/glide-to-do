# SPDX-License-Identifier: MPL-2.0
"""WA-42: echte kleine Kindprozesse; keine Glide-/Last-/Nutzerdatenprüfung."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
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

    def test_timeout_exports_partial_output_stack_and_case_progress(self):
        logdir = self.root / "ausgabe"
        report = self.root / "arbeitsmodi.json"
        integration = Path(__file__).resolve().parents[1] / "integration"
        code = f"""import sys,time,faulthandler
from types import SimpleNamespace
sys.path.insert(0, {str(integration)!r})
import test_arbeitsmodi as suite
class FakeLauf:
    def __init__(self, *args):
        self.errors=[]
        self.root=SimpleNamespace(tk=SimpleNamespace(call=lambda *args: 'test'))
suite.Lauf=FakeLauf
def blockierender_fall(run):
    from pathlib import Path
    Path({str(report.with_suffix(".ready"))!r}).touch()
    time.sleep(30)
suite.fall_werkzeugzeile=blockierender_fall
dump=faulthandler.dump_traceback_later
faulthandler.dump_traceback_later=lambda seconds,repeat=False: dump(.1,repeat=repeat)
sys.argv=['test_arbeitsmodi.py','--fall','werkzeugzeile','--report',{str(report)!r}]
suite.main()
"""
        run = pruefen.Prueflauf(logdir, 1, waechter=self.guard)
        original_popen = flow.subprocess.Popen
        def gestarteter_fall(*args, **kwargs):
            process = original_popen(*args, **kwargs)
            # Diese Gegenprobe misst den blockierenden Fall, nicht den
            # Import des Kindprozesses. Das eigentliche Limit bleibt 1 s.
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if report.with_suffix(".ready").is_file():
                    return process
                if process.poll() is not None:
                    break
                time.sleep(.01)
            process.kill()
            stdout, stderr = process.communicate()
            self.fail("Timeout-Gegenprobe erreicht den Testfall nicht: " + (stdout + stderr)[-1600:])
        wall_start = time.time()
        with patch.object(flow.subprocess, "Popen", side_effect=gestarteter_fall), contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(run.prozess("arbeitsmodi", [sys.executable, "-B", "-c", code]))
            self.assertFalse(run.prozess("folge", [sys.executable, "-B", "-c", "pass"]))
        output = (logdir / "arbeitsmodi.log").read_text(encoding="utf-8")
        self.assertIn("START werkzeugzeile", output)
        self.assertIn("test_arbeitsmodi.py", output)
        self.assertIn("Timeout (", output)
        progress = json.loads(report.read_text(encoding="utf-8"))
        started = progress["laufender_fall"]["gestartet_unix"]
        self.assertIsInstance(started, (float, int))
        self.assertGreaterEqual(started, wall_start)
        self.assertLessEqual(started, time.time())
        self.assertEqual(progress["laufender_fall"], {
            "name": "werkzeugzeile", "phase": "test", "gestartet_unix": started})
        self.assertEqual(progress["faelle"], {})
        self.assertTrue(self.guard.stopped)
        self.assertEqual(len(self.guard.rows), 1)

    def test_timeout_exports_byte_output_without_guard(self):
        logdir = self.root / "ausgabe"
        run = pruefen.Prueflauf(logdir, 1)
        error = subprocess.TimeoutExpired(["probe"], 1, output="Anfang ä\n".encode(), stderr=b"Stack\n")
        with patch.object(pruefen.subprocess, "run", side_effect=error), contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(run.prozess("probe", ["probe"]))
        self.assertEqual((logdir / "probe.log").read_text(encoding="utf-8"), "Anfang ä\nStack\n")

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

    def test_failed_result_stops_before_later_checks(self):
        run = pruefen.Prueflauf(None, 10, waechter=self.guard)
        called = []
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(run.funktion('rot', lambda: ('fehlgeschlagen', 'Konkreter Fehler')))
            self.assertFalse(run.funktion('folge', lambda: called.append(True)))
        self.assertEqual(called, [])
        self.assertEqual([r['status'] for r in run.results], ['fehlgeschlagen','übersprungen'])

    def test_zero_exit_with_uncaught_tcl_callback_error_stops_the_sequence(self):
        logdir = self.root / "callback-log"
        run = pruefen.Prueflauf(logdir, 30, waechter=self.guard)
        error = 'invalid command name "123collapse_emptied_frames"'
        command = [sys.executable, "-B", "-c", "import sys; print(" + repr(error) + ", file=sys.stderr)"]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(run.prozess("abbau", command))
            self.assertFalse(run.prozess("folge", [sys.executable, "-B", "-c", "pass"]))
        self.assertEqual(run.results[0]["exitcode"], 0)
        self.assertEqual(run.results[0]["callback_errors"], [error])
        self.assertEqual(run.results[1]["status"], "übersprungen")
        self.assertEqual(len(self.guard.rows), 1)
        self.assertFalse(self.guard.rows[0]["passed"])
        self.assertIn(error, (logdir / "abbau.log").read_text(encoding="utf-8"))

    def test_hint_does_not_stop_and_stays_a_hint(self):
        run = pruefen.Prueflauf(None, 10, waechter=self.guard)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(run.funktion('hinweis', lambda: ('Hinweis', 'Alter Lieferstand')))
            self.assertTrue(run.funktion('folge', lambda: 'Geprüft'))
        self.assertFalse(self.guard.stopped)
        self.assertEqual([r['status'] for r in run.results], ['Hinweis','ausgeführt'])

    def test_reported_failure_prevents_additional_process(self):
        run = pruefen.Prueflauf(None, 10, waechter=self.guard)
        with contextlib.redirect_stdout(io.StringIO()):
            run.meldung('Voraussetzung', 'fehlgeschlagen', 'Kein Display')
            self.assertFalse(run.prozess('folge', [sys.executable,'-B','-c','raise SystemExit(3)']))
        self.assertEqual(len(self.guard.rows), 0)
        self.assertEqual(run.results[-1]['status'], 'übersprungen')

    def test_ci_uses_guard_and_does_not_launch_after_failed_child(self):
        import ci_grundstufe as ci
        real_run = pruefen.Prueflauf
        started = []
        def create(logdir, timeout, *, waechter=None):
            self.assertIsNotNone(waechter, 'CI benötigt denselben Prozess-/Integritätswächter')
            run = real_run(logdir, timeout, waechter=waechter)
            process = run.prozess
            def child(name, command, **kwargs):
                if not waechter.stopped:
                    started.append(name)
                return process(name, [sys.executable,'-B','-c','raise SystemExit(7)'], **kwargs)
            run.prozess = child
            return run
        args = ['ci_grundstufe.py','--protokoll',str(self.root/'ci'),
                '--arbeitsablage',str(self.root/'ci-arbeit')]
        with patch.object(sys,'argv',args), patch.object(ci,'REPO',self.repo), \
                patch.object(ci.pruefen,'Prueflauf',side_effect=create), \
                patch.object(ci.pruefen,'syntax_pruefen',return_value='ok'), \
                patch.object(ci.pruefen,'versionen_pruefen',return_value='ok'), \
                patch.object(ci.pruefen,'dokumentation_pruefen',return_value='ok'), \
                patch.object(ci.pruefen,'fixtures_pruefen',return_value='ok'), \
                patch.object(ci,'fremdcode_pruefen') as vendor, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ci.main(), 1)
        report = json.loads((self.root/'ci/ergebnis.json').read_text())
        self.assertEqual(started,['Werkzeugtests'])
        self.assertEqual([r['schritt'] for r in report['schritte'] if r['status']=='fehlgeschlagen'], ['Werkzeugtests'])
        self.assertFalse(vendor.called, 'Kein Netz-/Folgecheck nach rotem Kind')

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
        objects = self.project / ".git/objects"
        for original_object in objects.glob("??/*"):
            copied_object = frozen.parents[1] / ".git/objects" / original_object.relative_to(objects)
            self.assertEqual(copied_object.read_bytes(), original_object.read_bytes())
            self.assertFalse(os.path.samefile(original_object, copied_object))
        proof = json.loads((root / "quellstand.json").read_text(encoding="utf-8"))
        self.assertTrue(proof["source_unchanged"] and proof["copy_equal"])


if __name__ == "__main__":
    unittest.main()
