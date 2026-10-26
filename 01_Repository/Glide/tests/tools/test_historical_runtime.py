"""Historische Altleser verwenden echte gepinnte Gitmodule, keine aktuellen."""
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "integration"))
import historical_runtime as history


class HistoricalRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="glide-history-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "--quiet")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.app_bytes = b'APP_VERSION = "3.43.1"\nraise RuntimeError("never import fixture")\n'
        self.name = "Glide-Aufgaben-und-Listen_v3.43.1.pyw"
        self.delivery = self.repo / history.DELIVERY
        for name, data in ((self.name, self.app_bytes), ("policy.py", b"VALUE = 'historical'\n"),
                           ("resources/logo.svg", b"<svg/>"), ("vendor/example/__init__.py", b"old = True\n"),
                           ("Archiv/old.pyw", b"archive must not be copied"), ("README.md", b"not runtime")):
            path = self.delivery / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.git("add", ".")
        self.git("-c", "core.autocrlf=false", "commit", "--quiet", "-m", "historical")
        self.commit = self.git("rev-parse", "HEAD").decode().strip()
        self.archived = self.root / self.name
        self.archived.write_bytes(self.app_bytes)
        self.pin = patch.dict(history.SNAPSHOTS, {"3.43.1": self.commit}, clear=True)
        self.pin.start()
        self.addCleanup(self.pin.stop)

    def git(self, *arguments):
        result = subprocess.run(["git", "-C", str(self.repo), *arguments], capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_complete_pinned_runtime_is_isolated_and_removed(self):
        # Die aktuelle Lieferung ist inzwischen anders; nur Git ist maßgeblich.
        (self.delivery / "policy.py").write_text("VALUE = 'current'\n", encoding="utf-8")
        with history.historical_app(self.repo, self.archived) as app:
            self.assertEqual(app.read_bytes(), self.app_bytes)
            self.assertEqual((app.parent / "policy.py").read_bytes(), b"VALUE = 'historical'\n")
            self.assertTrue((app.parent / "resources/logo.svg").is_file())
            self.assertTrue((app.parent / "vendor/example/__init__.py").is_file())
            self.assertFalse((app.parent / "Archiv").exists())
            self.assertFalse((app.parent / "README.md").exists())
            evidence = json.loads((app.parent / "historical-runtime.json").read_text(encoding="utf-8"))
            self.assertEqual((evidence["commit"], evidence["modules"]), (self.commit, ["policy.py"]))
            temporary = app.parent
        self.assertFalse(temporary.exists())
        self.assertEqual(self.archived.read_bytes(), self.app_bytes)

    def test_modified_archived_app_cannot_use_valid_version_pin(self):
        self.archived.write_bytes(self.app_bytes + b"# modified\n")
        with self.assertRaisesRegex(ValueError, "unterscheiden"):
            with history.historical_app(self.repo, self.archived):
                self.fail("modified historical reader accepted")

    def test_unknown_version_is_failure_without_fallback(self):
        self.archived.write_bytes(b'APP_VERSION = "9.99.0"\n')
        with self.assertRaisesRegex(ValueError, "gepinnter"):
            with history.historical_app(self.repo, self.archived):
                self.fail("unknown historical version accepted")

    def test_missing_pinned_history_fails_with_actionable_message(self):
        with patch.dict(history.SNAPSHOTS, {"3.43.1": "f" * 40}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "Git-Historie.*kein automatischer Fetch"):
                with history.historical_app(self.repo, self.archived):
                    self.fail("missing pinned history accepted")

    def test_incomplete_runtime_cannot_use_current_vendor(self):
        self.git("rm", "-r", history.DELIVERY + "/vendor")
        self.git("commit", "--quiet", "-m", "missing vendor")
        commit = self.git("rev-parse", "HEAD").decode().strip()
        with patch.dict(history.SNAPSHOTS, {"3.43.1": commit}, clear=True):
            with self.assertRaisesRegex(ValueError, "unvollständig"):
                with history.historical_app(self.repo, self.archived):
                    self.fail("incomplete historical runtime accepted")

    def test_unsafe_paths_and_links_are_rejected_without_extraction(self):
        for name, link in (("../outside.py", False), ("resources/link", True), ("C:\\outside.py", False)):
            with self.subTest(name=name):
                buffer = io.BytesIO()
                with tarfile.open(fileobj=buffer, mode="w") as archive:
                    member = tarfile.TarInfo(name)
                    if link:
                        member.type, member.linkname = tarfile.SYMTYPE, "../../outside"
                    archive.addfile(member)
                with self.assertRaises(ValueError):
                    history._write_archive(buffer.getvalue(), self.root / "extract")


if __name__ == "__main__":
    unittest.main()
