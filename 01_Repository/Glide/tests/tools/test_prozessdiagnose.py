"""Gegenproben zur WA-41-Einordnung ohne Last oder echte Speicherverletzung."""

import contextlib
import io
import json
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import Mock

import pruefen
from prozessdiagnose import prozessdiagnose, systemkontext, pruefplatz


class ProzessdiagnoseTests(unittest.TestCase):
    def test_apple_silicon_profiles_remain_separate_from_intel_and_amd(self):
        for name in ('Apple M2', 'Apple M2 Pro', 'Apple M2 Max', 'Apple M1 Ultra'):
            self.assertEqual(pruefplatz({'cpu': name})['cpu_familie'], 'apple_silicon')
        for context in ({'cpu': 'arm64'}, {'cpu': 'Apple'},
                        {'cpu': 'Apple M2', 'cpu_hersteller': 'GenuineIntel'}):
            self.assertEqual(pruefplatz(context)['cpu_familie'], 'unbestimmt')

    def apple_context(self, *, translated='0', architecture='arm64'):
        def read(command, **kwargs):
            self.assertEqual(command[:2], ['/usr/sbin/sysctl', '-n'])
            self.assertLessEqual(kwargs['timeout'], 2)
            self.assertNotIn('shell', kwargs)
            values = {'machdep.cpu.brand_string': 'Apple M2\n', 'sysctl.proc_translated': translated+'\n'}
            return subprocess.CompletedProcess(command, 0, stdout=values[command[-1]], stderr='')
        with patch('prozessdiagnose.sys.platform', 'darwin'), \
                patch('prozessdiagnose.platform.processor', return_value='arm'), \
                patch('prozessdiagnose.platform.machine', return_value=architecture), \
                patch('prozessdiagnose.platform.mac_ver', return_value=('15.0', ('', '', ''), architecture)), \
                patch('subprocess.run', side_effect=read) as child:
            context = systemkontext()
        self.assertEqual(child.call_count, 2)
        return context

    def test_darwin_records_m2_without_private_machine_identifiers(self):
        context = self.apple_context()
        self.assertEqual(context['cpu'], 'Apple M2')
        self.assertEqual(context['macos_version'], '15.0')
        self.assertIs(context['rosetta'], False)
        self.assertEqual(pruefplatz(context)['cpu_familie'], 'apple_silicon')
        for key in ('benutzer', 'hostname', 'serial', 'uuid'):
            self.assertNotIn(key, context)

    def test_darwin_rosetta_is_explicit_and_not_inferred_from_architecture(self):
        context = self.apple_context(translated='1', architecture='x86_64')
        self.assertEqual(context['architektur'], 'x86_64')
        self.assertIs(context['rosetta'], True)
        self.assertEqual(context['cpu'], 'Apple M2')
        self.assertIsNone(self.apple_context(translated='unbekannt')['rosetta'])

    def test_darwin_read_errors_keep_unknown_cpu_and_translation_honest(self):
        for result in (OSError('nicht vorhanden'), subprocess.TimeoutExpired('sysctl', 2),
                       subprocess.CompletedProcess([], 1, stdout='', stderr='unsupported')):
            kwargs = {'side_effect': result} if isinstance(result, Exception) else {'return_value': result}
            with patch('prozessdiagnose.sys.platform', 'darwin'), \
                    patch('prozessdiagnose.platform.processor', return_value='arm'), \
                    patch('subprocess.run', **kwargs):
                context = systemkontext()
            self.assertEqual(context['cpu'], 'arm')
            self.assertIsNone(context['rosetta'])
            self.assertEqual(pruefplatz(context)['cpu_familie'], 'unbestimmt')

    def test_hardware_profiles_separate_intel_and_amd_without_diagnosis(self):
        intel = pruefplatz({"cpu": "Intel Core i9-14900K", "cpu_hersteller": "GenuineIntel"})
        amd = pruefplatz({"cpu": "AMD Ryzen 7 5800X3D", "cpu_hersteller": "AuthenticAMD"})
        self.assertEqual(intel["cpu_familie"], "intel")
        self.assertEqual(amd["cpu_familie"], "amd")
        self.assertNotEqual(intel["hardwareprofil_sha256"], amd["hardwareprofil_sha256"])
        self.assertNotIn("ursache_bewiesen", intel)

    def test_hardware_profile_is_independent_of_runtime_and_private_names(self):
        context = {"cpu": " Intel   Core i9 ", "board": "Board"}
        first = pruefplatz(context)
        second = pruefplatz(dict(context, cpu="Intel Core i9", runner_python="neu", benutzer="privat"))
        self.assertEqual(first, second)
        self.assertNotIn("privat", json.dumps(second))
        self.assertEqual(context["cpu"], " Intel   Core i9 ")

    def test_unknown_or_contradictory_cpu_is_not_assigned(self):
        for context in ({}, {"cpu": "unbekannt"}, {"cpu": "Intel", "cpu_hersteller": "AMD"}):
            self.assertEqual(pruefplatz(context)["cpu_familie"], "unbestimmt")

    def diagnose(self, code, text="", **kwargs):
        return prozessdiagnose("test_speicherlast330", code, text, plattform="win32", **kwargs)

    def test_windows_signed_and_unsigned_native_status(self):
        for code in (0xC0000005, 0xC0000409):
            for value in (code, code - 2**32):
                with self.subTest(code=value):
                    result = self.diagnose(value)
                    self.assertEqual(result["spur"], "WA-41A")
                    self.assertIn(f"0x{code:08X}", result["signaturen"])
                    self.assertFalse(result["ursache_bewiesen"])

    def test_intel_hint_requires_failure_and_signature(self):
        intel = {"cpu": "Intel Core i9-14900K", "cpu_hersteller": "GenuineIntel"}
        self.assertIsNone(self.diagnose(0, kontext=intel))
        self.assertIsNone(self.diagnose(1, "AssertionError: falsche Sortierung", kontext=intel))
        result = self.diagnose(0xC0000005, kontext=intel)
        self.assertIn("Intel-Prüfplatz", result["hinweis"])
        self.assertIn("nicht isoliert bewiesen", result["hinweis"])

    def test_amd_crash_is_not_exempted(self):
        result = self.diagnose(0xC0000005, kontext={"cpu": "AMD Ryzen 7 5800X3D"})
        self.assertEqual(result["kategorie"], "prozessabbruch")
        self.assertNotIn("Intel-Prüfplatz", result["hinweis"])
        self.assertFalse(result["ursache_bewiesen"])

    def test_internal_cache_abort_is_recognized(self):
        result = self.diagnose(1, "Fatal Python error: _TAIL_CALL_CACHE: Executing a cache\n")
        self.assertIn("Executing a cache", result["signaturen"][0])

    def test_known_type_symptom_is_only_a_suspect(self):
        result = self.diagnose(1, "TypeError: 'dict_valueiterator' object is not callable\n")
        self.assertEqual(result["kategorie"], "auffaelliger_python_fehler")
        self.assertFalse(result["ursache_bewiesen"])
        self.assertIsNone(self.diagnose(1, "TypeError: unsupported operand type(s)"))

    def test_known_type_symptom_is_not_applied_to_unrelated_suite(self):
        self.assertIsNone(prozessdiagnose("test_drawing", 1,
                          "NameError: name 'isinstance' is not defined\n", plattform="win32"))

    def test_data_mismatch_stays_an_independent_blocker(self):
        for text in ("AssertionError: Runde 5: geladen ≠ gespeichert\n",
                     "AssertionError: großer Bestand verlustfrei\n"):
            result = self.diagnose(1, text, kontext={"cpu": "Intel Core i9-14900K"})
            self.assertEqual(result["spur"], "WA-41B")
            self.assertEqual(result["kategorie"], "datenabweichung")
            self.assertNotIn("Intel-Prüfplatz", result["hinweis"])
            self.assertIn("nicht freigeben", result["hinweis"])

    def test_intentional_writer_crash_does_not_taint_success(self):
        text = "Windows fatal exception: access violation\nFatal Python error: simulated\n"
        self.assertIsNone(self.diagnose(0, text))

    def test_posix_signal_is_distinguished_from_windows_status(self):
        result = prozessdiagnose("test_speicherlast330", -int(signal.SIGABRT), "", plattform="linux")
        self.assertIn("SIGABRT", result["signaturen"])
        self.assertIsNone(prozessdiagnose("test_speicherlast330", -1073741819, "", plattform="linux"))

    def test_native_crash_in_other_suite_gets_general_diagnosis(self):
        result = prozessdiagnose("test_wiederholen", 0xC0000005, "", plattform="win32")
        self.assertEqual(result["spur"], "Prozessdiagnose")
        self.assertNotIn("zehn ausgewertete", result["hinweis"])

    def test_registry_permission_failure_does_not_block_tests(self):
        if sys.platform != "win32":
            self.skipTest("Windows-Registry")
        with patch("winreg.OpenKey", side_effect=PermissionError):
            result = systemkontext()
        self.assertEqual(result["bios"], "nicht ermittelt")
        self.assertEqual(result["runner_python"], sys.version)


class PrueflaufDiagnoseTests(unittest.TestCase):
    def test_integrity_guard_failure_keeps_diagnosis_for_failed_step(self):
        guard = Mock(stopped=False)

        def fail(*args, **kwargs):
            guard.stopped = True
            return subprocess.CompletedProcess([sys.executable], 0xC0000005,
                                               stdout="Fatal Python error: simulated\n", stderr="")

        guard.command.side_effect = fail
        with contextlib.redirect_stdout(io.StringIO()):
            run = pruefen.Prueflauf(None, 10, waechter=guard)
            self.assertFalse(run.prozess("test_speicherlast330", [sys.executable]))
        self.assertEqual(run.results[-1]["status"], "fehlgeschlagen")
        self.assertEqual(run.results[-1]["diagnose"]["spur"], "WA-41A")
        self.assertEqual(guard.command.call_count, 1)

    def test_runner_keeps_native_failure_and_persists_raw_log(self):
        text = "Fatal Python error: _TAIL_CALL_CACHE: Executing a cache\n"
        with tempfile.TemporaryDirectory(prefix="glide-diagnose-test-") as directory:
            target = Path(directory)
            with contextlib.redirect_stdout(io.StringIO()):
                run = pruefen.Prueflauf(target, 10)
                with patch("pruefen.subprocess.run", return_value=subprocess.CompletedProcess(
                        [sys.executable], 0xC0000005, stdout=text, stderr="")) as child:
                    self.assertFalse(run.prozess("test_speicherlast330", [sys.executable, "-B", "probe.py"]))
            self.assertEqual(child.call_count, 1)  # keine automatische Wiederholung
            self.assertEqual(run.results[-1]["status"], "fehlgeschlagen")
            self.assertEqual(run.results[-1]["exitcode"], 0xC0000005)
            self.assertEqual((target / "test_speicherlast330.log").read_text(encoding="utf-8"), text)
            report = json.loads((target / "test_speicherlast330.diagnose.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "fehlgeschlagen")
            self.assertEqual(report["diagnose"]["spur"], "WA-41A")
            self.assertIn("start", report["diagnose"])
            self.assertIn("ende", report["diagnose"])
            self.assertEqual(report["systemkontext"]["app_sha256"], run.systemkontext["app_sha256"])
            self.assertTrue((target / "systemkontext.json").is_file())

    def test_real_short_child_retains_ordinary_failure(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run = pruefen.Prueflauf(None, 10)
            self.assertFalse(run.prozess("probe", [sys.executable, "-B", "-c", "raise SystemExit(7)"]))
        self.assertEqual(run.results[-1]["exitcode"], 7)
        self.assertNotIn("diagnose", run.results[-1])

    def test_timeout_never_becomes_hardware_diagnosis(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run = pruefen.Prueflauf(None, 10)
            with patch("pruefen.subprocess.run", side_effect=subprocess.TimeoutExpired("probe", 10)):
                self.assertFalse(run.prozess("test_speicherlast330", [sys.executable]))
        self.assertEqual(run.results[-1]["status"], "fehlgeschlagen")
        self.assertNotIn("diagnose", run.results[-1])

    def test_success_has_no_diagnosis(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run = pruefen.Prueflauf(None, 10)
            with patch("pruefen.subprocess.run", return_value=subprocess.CompletedProcess(
                    [sys.executable], 0, stdout="test_speicherlast330: OK", stderr="")):
                self.assertTrue(run.prozess("test_speicherlast330", [sys.executable]))
        self.assertEqual(run.results[-1]["status"], "ausgeführt")
        self.assertNotIn("diagnose", run.results[-1])


if __name__ == "__main__":
    unittest.main()
