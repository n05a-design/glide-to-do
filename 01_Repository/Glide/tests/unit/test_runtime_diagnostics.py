"""Diagnose nach echtem Prozessende, begrenzte Ablage und Datenschutz."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[2] / "src/glide"
sys.path.insert(0, str(SOURCE))
import runtime_diagnostics as diagnostic


class RuntimeDiagnostics(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="glide-diagnose-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        self.environment = patch.dict(os.environ, {"GLIDE_DATA_DIR": str(self.data)})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.addCleanup(setattr, diagnostic, "_current", diagnostic._current)
        self.addCleanup(setattr, diagnostic, "_warning", diagnostic._warning)
        diagnostic._current = None
        diagnostic._warning = ""

    def records(self):
        return [json.loads(path.read_text(encoding="utf-8"))
                for path in (self.data / "diagnostics").glob("*.json")]

    def test_completed_start_records_only_technical_metadata(self):
        session = diagnostic.start_session("3.48.0", "a" * 64)
        diagnostic.record_phase("ui_ready", tk_version="9.0.4")
        diagnostic.record_phase("closed")
        diagnostic.finish(0)
        record = self.records()[0]
        self.assertEqual(record["version"], "3.48.0")
        self.assertEqual(record["build"], "a" * 64)
        self.assertEqual(record["tk"], "9.0.4")
        self.assertEqual(record["last_completed_phase"], "closed")
        self.assertTrue(record["completed"])
        self.assertEqual(record["exit_code"], 0)
        self.assertLess(session.path.stat().st_size, diagnostic.MAX_BYTES)
        with self.assertRaises(ValueError):
            diagnostic.record_phase("Geheimer Aufgabentitel")
        with self.assertRaises(ValueError):
            diagnostic.record_phase("ui_ready", tk_version="Aufgabeninhalt")
        self.assertNotIn("Geheimer", session.path.read_text(encoding="utf-8"))
        self.assertNotIn("Aufgabeninhalt", session.path.read_text(encoding="utf-8"))

    def test_direct_hard_exit_preserves_incomplete_last_phase(self):
        code = ("import sys,os;sys.path.insert(0,sys.argv[1]);import runtime_diagnostics as d;"
                "d.start_session('3.48.0');d.record_phase('data_saved');os._exit(17)")
        outcome = subprocess.run([sys.executable, "-B", "-c", code, str(SOURCE)], timeout=20)
        self.assertEqual(outcome.returncode, 17)
        record = self.records()[0]
        self.assertFalse(record["completed"])
        self.assertIsNone(record["exit_code"])
        self.assertEqual(record["last_completed_phase"], "data_saved")

    def test_phase_and_finish_adapters_never_start_a_session_implicitly(self):
        self.assertFalse(diagnostic.record_phase("data_saved"))
        self.assertFalse(diagnostic.finish())
        self.assertFalse((self.data / "diagnostics").exists())

    def test_changed_test_directory_does_not_touch_old_session(self):
        old = diagnostic.start_session()
        before = old.path.read_bytes()
        second = self.data / "second"
        with patch.dict(os.environ, {"GLIDE_DATA_DIR": str(second)}):
            self.assertFalse(diagnostic.record_phase("data_saved"))
            self.assertEqual(diagnostic.warning(), "")
            self.assertEqual(old.path.read_bytes(), before)
            fresh = diagnostic.start_session()
            self.assertNotEqual(fresh.session, old.session)
            self.assertEqual(fresh.directory, second / "diagnostics")

    def test_completed_session_is_not_reopened_by_another_start(self):
        previous = diagnostic.start_session()
        diagnostic.finish(0)
        fresh = diagnostic.start_session()
        self.assertNotEqual(fresh.session, previous.session)
        self.assertFalse(fresh.state["completed"])

    def test_supervisor_records_actual_hard_exit_and_child_phase(self):
        code = ("import sys,os;sys.path.insert(0,sys.argv[1]);import runtime_diagnostics as d;"
                "assert d.child_launch();d.start_session('3.48.0');"
                "d.record_phase('ui_ready',tk_version='9.0.4');os._exit(23)")
        outcome = diagnostic.supervise([sys.executable, "-B", "-c", code, str(SOURCE)], build="b" * 64)
        self.assertEqual(outcome, 23)
        records = self.records()
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["version"], "3.48.0")
        self.assertEqual(record["build"], "b" * 64)
        self.assertEqual(record["exit_code"], 23)
        self.assertEqual(record["last_completed_phase"], "ui_ready")
        self.assertTrue(record["completed"])
        self.assertTrue(record["supervised"])
        self.assertNotEqual(record["process_id"], record["supervisor_id"])

    def test_supervisor_handles_failure_before_module_import(self):
        outcome = diagnostic.supervise([sys.executable, "-B", "-c", "raise ImportError('SECRET_TASK_CONTENT')"])
        self.assertNotEqual(outcome, 0)
        record = self.records()[0]
        self.assertEqual(record["last_completed_phase"], "startup")
        self.assertEqual(record["exit_code"], outcome)
        self.assertNotIn("SECRET_TASK_CONTENT", json.dumps(record))

    def test_supervisor_explicit_environment_keeps_both_processes_isolated(self):
        second = self.data / "second"
        code = ("import sys;sys.path.insert(0,sys.argv[1]);import runtime_diagnostics as d;"
                "assert d.child_launch();d.start_session();d.record_phase('data_loaded')")
        environment = dict(os.environ, GLIDE_DATA_DIR=str(second))
        self.assertEqual(diagnostic.supervise([sys.executable, "-B", "-c", code, str(SOURCE)],
                                              env=environment), 0)
        self.assertFalse((self.data / "diagnostics").exists())
        files = list((second / "diagnostics").glob("*.json"))
        self.assertEqual(len(files), 1)
        self.assertEqual(json.loads(files[0].read_text(encoding="utf-8"))["last_completed_phase"], "data_loaded")

    def test_foreign_content_in_diagnostic_record_is_not_republished(self):
        original = diagnostic.Journal()
        original.state["supervised"] = True
        original.state["supervisor_id"] = os.getpid()
        original._write()
        tampered = json.loads(original.path.read_text(encoding="utf-8"))
        tampered["task_text"] = "PRIVATE_CONTENT"
        original.path.write_text(json.dumps(tampered), encoding="utf-8")
        self.assertFalse(original.record_child_exit(0))
        self.assertFalse(original.enabled)

    def test_unwritable_directory_is_reported_without_app_failure(self):
        with patch.object(diagnostic.Path, "mkdir", side_effect=PermissionError("PRIVATE_TEXT")):
            session = diagnostic.start_session("3.48.0")
        self.assertFalse(session.enabled)
        self.assertFalse(diagnostic.record_phase("ui_ready"))
        self.assertIn("PermissionError", diagnostic.warning())
        self.assertIn(str(self.data / "diagnostics"), diagnostic.warning())
        self.assertNotIn("PRIVATE_TEXT", diagnostic.warning())

    def test_repeated_saves_do_not_rewrite_identical_phase(self):
        session = diagnostic.start_session()
        diagnostic.record_phase("data_saved")
        before = session.path.stat().st_mtime_ns
        with patch.object(session, "_write", side_effect=AssertionError("unnötiger Schreibzugriff")):
            self.assertTrue(diagnostic.record_phase("data_saved"))
        self.assertEqual(session.path.stat().st_mtime_ns, before)

    def test_rotation_bounds_finished_sessions_and_retains_active_one(self):
        active = diagnostic.Journal()
        for _ in range(16):
            session = diagnostic.Journal()
            session.finish(0)
        self.assertTrue(active.path.is_file())
        # Höchstens acht gewöhnliche Belege plus die laufende alte Sitzung.
        self.assertLessEqual(len(self.records()), diagnostic.MAX_FILES + 1)
        self.assertTrue(all(path.stat().st_size <= diagnostic.MAX_BYTES
                            for path in (self.data / "diagnostics").glob("*.json")))

    def test_forged_parent_marker_does_not_reuse_session(self):
        original = diagnostic.Journal()
        with patch.dict(os.environ, {diagnostic.SESSION_ENV: original.session,
                                     diagnostic.PARENT_ENV: str(os.getppid())}):
            self.assertFalse(diagnostic.child_launch())
            session = diagnostic.start_session()
        self.assertNotEqual(original.session, session.session)

    def test_start_failure_is_completed_without_recording_command(self):
        outcome = diagnostic.supervise([str(self.data / "PRIVATE_EXECUTABLE")])
        self.assertEqual(outcome, 1)
        record = self.records()[0]
        self.assertTrue(record["completed"])
        self.assertEqual(record["start_error"], "FileNotFoundError")
        self.assertNotIn("PRIVATE_EXECUTABLE", json.dumps(record))

    def test_launcher_runs_only_one_child_and_keeps_arguments(self):
        launcher_path = SOURCE / "glide_start.py"
        spec = importlib.util.spec_from_file_location("glide_diagnostic_launcher_test", launcher_path)
        launcher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(launcher)
        with patch.object(sys, "argv", [str(launcher_path), "eine-datei.glideapp"]), \
                patch.object(diagnostic, "supervise", return_value=27) as supervise:
            self.assertEqual(launcher.main(), 27)
        command = supervise.call_args.args[0]
        self.assertEqual(command[-2:], [diagnostic.CHILD_FLAG, "eine-datei.glideapp"])
        self.assertEqual(command[0], sys.executable)
        with patch.dict(os.environ, {diagnostic.PARENT_ENV: str(os.getppid())}), \
                patch.object(sys, "argv", [str(launcher_path), diagnostic.CHILD_FLAG, "x"]), \
                patch.object(launcher, "run_application", return_value=0) as run, \
                patch.object(diagnostic, "supervise", side_effect=AssertionError("Doppelstart")):
            self.assertEqual(launcher.main(), 0)
            run.assert_called_once()
            self.assertNotIn(diagnostic.CHILD_FLAG, sys.argv)

    def test_real_source_launcher_keeps_child_phase_and_native_exit(self):
        program = self.data / "program"
        program.mkdir()
        for name in ("glide_start.py", "runtime_check.py", "runtime_diagnostics.py"):
            shutil.copy2(SOURCE / name, program / name)
        (program / "app.pyw").write_text(
            "import os,sys\nimport runtime_diagnostics as d\nAPP_VERSION='3.48.0'\n"
            "def main():\n"
            " assert sys.argv[1:] == ['datei.glideapp']\n"
            " d.record_phase('ui_ready', tk_version='9.0.4')\n"
            " os._exit(19)\n", encoding="utf-8")
        outcome = subprocess.run([sys.executable, "-B", str(program / "glide_start.py"), "datei.glideapp"], timeout=20)
        self.assertEqual(outcome.returncode, 19)
        records = self.records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["last_completed_phase"], "ui_ready")
        self.assertEqual(records[0]["version"], "3.48.0")
        self.assertEqual(records[0]["exit_code"], 19)


class NativeBootstrapDiagnostics(unittest.TestCase):
    def setUp(self):
        path = SOURCE.parents[1] / "packaging/paket/start_glide.py"
        spec = importlib.util.spec_from_file_location("glide_native_diagnostic_test", path)
        self.bootstrap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.bootstrap)

    def test_native_smoke_contract_skips_supervisor(self):
        with patch.object(sys, "argv", ["Glide.exe", "--paket-pruefen", "ergebnis.json"]), \
                patch.object(self.bootstrap, "smoke", return_value=7) as smoke, \
                patch.object(diagnostic, "supervise", side_effect=AssertionError("unerlaubte Prüfungsschleife")):
            with self.assertRaises(SystemExit) as ended:
                self.bootstrap.main()
            self.assertEqual(ended.exception.code, 7)
            smoke.assert_called_once_with("ergebnis.json")

    def test_frozen_parent_restarts_only_own_executable(self):
        with patch.object(sys, "argv", ["Glide.exe", "datei.glideapp"]), \
                patch.object(sys, "frozen", True, create=True), \
                patch.object(diagnostic, "consume_child_flag", return_value=False), \
                patch.object(diagnostic, "supervise", return_value=29) as supervise:
            self.assertEqual(self.bootstrap.main(), 29)
        self.assertEqual(supervise.call_args.args[0],
                         [sys.executable, diagnostic.CHILD_FLAG, "datei.glideapp"])

    def test_source_parent_keeps_script_path(self):
        with patch.object(sys, "argv", [self.bootstrap.__file__, "datei.glideapp"]), \
                patch.object(sys, "frozen", False, create=True), \
                patch.object(diagnostic, "consume_child_flag", return_value=False), \
                patch.object(diagnostic, "supervise", return_value=31) as supervise:
            self.assertEqual(self.bootstrap.main(), 31)
        self.assertEqual(supervise.call_args.args[0],
                         [sys.executable, str(Path(self.bootstrap.__file__).resolve()),
                          diagnostic.CHILD_FLAG, "datei.glideapp"])


if __name__ == "__main__":
    unittest.main()
