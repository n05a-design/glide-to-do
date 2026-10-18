"""Datensperre glide.lock ohne Tk (WA-30, Befund A36).

Nur künstliche Sperrdateien in temporären Ordnern; das Rennen zweier Starts
läuft mit zwei echten Prozessen.
"""
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

SRC = Path(__file__).resolve().parents[2] / "src/glide"
sys.path.insert(0, str(SRC))
import data_lock as dl

NOW = datetime(2026, 10, 18, 12, 0, tzinfo=datetime.now().astimezone().tzinfo)


def record(**overrides):
    value = {"host": "HIER", "pid": 4242, "token": "t", "started_at": NOW.isoformat(),
             "refreshed_at": NOW.isoformat()}
    value.update(overrides)
    return value


class ParseAndRead(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="glide-lock-unit-")
        self.path = Path(self.folder.name) / "glide.lock"

    def tearDown(self):
        self.folder.cleanup()

    def test_valid_and_older_form(self):
        self.assertEqual(dl.parse(json.dumps(record()))["token"], "t")
        older = {"host": "ANDERER-RECHNER", "pid": 1, "started_at": NOW.isoformat()}
        self.assertEqual(dl.parse(json.dumps(older)), older, "ältere Sperren ohne Kennung bleiben gültig")

    def test_defective_contents(self):
        for raw in ("nicht json {", "[1,2]", "{}", json.dumps({"host": "", "started_at": NOW.isoformat()}),
                    json.dumps({"host": "HIER"}), json.dumps({"host": "HIER", "refreshed_at": "gestern"}),
                    b"\xff\xfe", ""):
            self.path.write_bytes(raw if isinstance(raw, bytes) else raw.encode("utf-8"))
            self.assertEqual(dl.read(self.path).kind, dl.DEFECTIVE, raw)

    def test_missing_valid_unreadable_and_oversized(self):
        self.assertEqual(dl.read(self.path).kind, dl.MISSING)
        self.path.write_text(json.dumps(record()), encoding="utf-8")
        state = dl.read(self.path)
        self.assertEqual((state.kind, state.record["token"]), (dl.VALID, "t"))
        self.path.unlink()
        self.path.mkdir()
        state = dl.read(self.path)
        self.assertEqual(state.kind, dl.UNREADABLE, "Sperrpfad als Verzeichnis ist nie frei")
        self.assertTrue(state.detail)
        self.path.rmdir()
        self.path.write_bytes(b" " * (dl.MAX_BYTES + 1))
        self.assertEqual(dl.read(self.path).kind, dl.DEFECTIVE)


class Classify(unittest.TestCase):
    def verdict(self, value, alive=lambda pid: True, now=NOW):
        return dl.classify(value, host="HIER", pid=1000, now=now, max_age_seconds=8 * 3600, alive=alive)

    def test_rules(self):
        self.assertEqual(self.verdict(record(host="ANDERER")), dl.FOREIGN)
        old = (NOW - timedelta(hours=9)).isoformat()
        self.assertEqual(self.verdict(record(host="ANDERER", refreshed_at=old, started_at=old)), dl.FREE)
        self.assertEqual(self.verdict(record()), dl.FOREIGN)
        self.assertEqual(self.verdict(record(), alive=lambda pid: False), dl.FREE)
        self.assertEqual(self.verdict(record(pid=1000)), dl.FREE, "eigener Prozess")
        self.assertEqual(self.verdict(record(pid=0)), dl.FREE)
        self.assertEqual(self.verdict(record(pid="kaputt")), dl.FREE)
        future = (NOW + timedelta(minutes=5)).isoformat()
        self.assertEqual(self.verdict(record(host="ANDERER", refreshed_at=future)), dl.FOREIGN)

    def test_real_process_liveness(self):
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
        try:
            self.assertTrue(dl.process_alive(child.pid))
        finally:
            child.kill()
            child.wait(timeout=10)
        self.assertFalse(dl.process_alive(child.pid))


class CreateExclusive(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="glide-lock-unit-")
        self.path = Path(self.folder.name) / "glide.lock"

    def tearDown(self):
        self.folder.cleanup()

    def leftovers(self):
        return [name for name in os.listdir(self.folder.name) if name.startswith(".glide-lock-")]

    def test_first_wins_second_leaves_content(self):
        self.assertTrue(dl.create_exclusive(self.path, record(token="erste")))
        self.assertFalse(dl.create_exclusive(self.path, record(token="zweite")))
        self.assertEqual(dl.read(self.path).record["token"], "erste")
        self.assertEqual(self.leftovers(), [])

    def test_fallback_without_hardlinks(self):
        with mock.patch.object(dl.os, "link", side_effect=OSError(1, "keine Hardlinks")):
            self.assertTrue(dl.create_exclusive(self.path, record(token="ohne-link")))
            self.assertFalse(dl.create_exclusive(self.path, record(token="zweite")))
        self.assertEqual(dl.read(self.path).record["token"], "ohne-link")
        self.assertEqual(self.leftovers(), [])

    def test_defective_file_is_not_replaced(self):
        self.path.write_text("nicht json {", encoding="utf-8")
        self.assertFalse(dl.create_exclusive(self.path, record()))
        self.assertEqual(self.path.read_text(encoding="utf-8"), "nicht json {")

    def test_two_processes_race(self):
        script = (
            "import sys, time\n"
            f"sys.path.insert(0, {str(SRC)!r})\n"
            "import data_lock as dl\n"
            "start = float(sys.argv[2])\n"
            "while time.time() < start: pass\n"
            "print(dl.create_exclusive(sys.argv[1], dl.new_record('HIER', 1, '2026-10-18T12:00:00+02:00')))\n"
        )
        for runde in range(5):
            path = Path(self.folder.name) / f"rennen{runde}.lock"
            start = time.time() + 1.0
            processes = [subprocess.Popen([sys.executable, "-B", "-c", script, str(path), str(start)],
                                          stdout=subprocess.PIPE, text=True) for _ in range(2)]
            results = [process.communicate(timeout=30)[0].strip() for process in processes]
            self.assertEqual(sorted(results), ["False", "True"], (runde, results))
            self.assertEqual(dl.read(path).kind, dl.VALID)


class Texts(unittest.TestCase):
    def test_questions(self):
        self.assertIn("übernehmen?", dl.defective_question("kein JSON-Objekt"))
        self.assertIn("kein JSON-Objekt", dl.defective_question("kein JSON-Objekt"))
        self.assertIn("schreibgeschützt", dl.takeover_failed("x"))


class Acquisition(unittest.TestCase):
    def test_serializes_existing_lock_replacement(self):
        with tempfile.TemporaryDirectory(prefix="glide-lock-acquire-") as folder:
            path = Path(folder) / "glide.lock"
            path.write_text(json.dumps(record(pid=999999)), encoding="utf-8")
            with dl.acquisition(path) as first:
                self.assertTrue(first)
                with dl.acquisition(path) as second:
                    self.assertFalse(second, "zweiter Erwerb darf verwaiste Sperre nicht parallel ersetzen")
            with dl.acquisition(path) as next_start:
                self.assertTrue(next_start)

    def test_process_death_releases_acquisition(self):
        with tempfile.TemporaryDirectory(prefix="glide-lock-crash-") as folder:
            path = Path(folder) / "glide.lock"
            script = ("import sys,time\n"
                      f"sys.path.insert(0, {str(SRC)!r})\n"
                      "import data_lock as dl\n"
                      "with dl.acquisition(sys.argv[1]) as ok:\n"
                      " print(ok, flush=True)\n"
                      " time.sleep(60)\n")
            child = subprocess.Popen([sys.executable, "-B", "-c", script, str(path)],
                                     stdout=subprocess.PIPE, text=True)
            try:
                self.assertEqual(child.stdout.readline().strip(), "True")
                with dl.acquisition(path) as parallel:
                    self.assertFalse(parallel)
            finally:
                child.kill()
                child.wait(timeout=10)
                child.stdout.close()
            with dl.acquisition(path) as recovered:
                self.assertTrue(recovered, "Prozessabbruch darf keine dauerhafte Erwerbssperre hinterlassen")


if __name__ == "__main__":
    unittest.main()
