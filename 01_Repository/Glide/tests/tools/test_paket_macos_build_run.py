"""Mac-Baulauf vorab prüfen, ohne Laufzeitinstallation, Paketstart oder GUI."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[2] / "packaging/paket"
sys.path.insert(0, str(TOOLS))
import macos_build_run as runner


def shell():
    if os.name == "nt":
        candidate = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe"
        return str(candidate) if candidate.is_file() else None
    return shutil.which("sh")


class MacBuildRunTests(unittest.TestCase):
    def test_runtime_requires_exact_original_license_versions(self):
        expected = json.loads((TOOLS / "lizenzen/macos/manifest.json").read_text(encoding="utf-8"))["runtime"]
        runner.validate_runtime(expected, expected)
        for name in ("python", "tcl", "tk_compiled", "platform", "machine"):
            changed = dict(expected, **{name: "anderer Stand"})
            with self.subTest(field=name), self.assertRaisesRegex(ValueError, "Original-Lizenzbelegen"):
                runner.validate_runtime(expected, changed)

    def test_existing_source_and_onedrive_destinations_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            repo.mkdir()
            for target in (repo, repo / "build", root, root / "OneDrive" / "build"):
                if target.parent.name == "OneDrive":
                    target.parent.mkdir()
                with self.subTest(target=target), self.assertRaises(ValueError):
                    runner.validate_destination(repo, target)
            safe = runner.validate_destination(repo, root / "neuer Bau")
            self.assertEqual(safe, root / "neuer Bau")
            self.assertFalse(safe.exists(), "Validierung legt keinen Ordner an")

    def test_source_inventory_includes_new_modules_and_build_orchestration(self):
        repo = TOOLS.parents[1]
        inventory = runner.source_inventory(repo)
        self.assertIn("src/glide/home_dashboard.py", inventory)
        self.assertIn("packaging/paket/baue_und_pruefe_macos.sh", inventory)
        self.assertIn("packaging/paket/macos_build_run.py", inventory)
        runner.verify_sources(repo, dict(source_sha256=inventory))
        changed = copy.deepcopy(inventory)
        changed["src/glide/home_dashboard.py"] = "wrong hash"
        with self.assertRaisesRegex(ValueError, "verändert"):
            runner.verify_sources(repo, dict(source_sha256=changed))

    def test_archive_hashes_file_modes_and_inventory_must_match(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "Glide.app"
            binary = package / "Contents/MacOS/Glide"
            binary.parent.mkdir(parents=True)
            binary.write_bytes(b"native fixture, never executed")
            binary.chmod(0o755)
            archive = root / "Glide.tar.gz"
            with tarfile.open(archive, "w:gz") as stream:
                stream.add(package, arcname=package.name)
            expected = {"Contents/MacOS/Glide": hashlib.sha256(binary.read_bytes()).hexdigest()}
            result = runner.verify_archive(archive, package, expected)
            self.assertEqual(result, dict(files=1, symlinks=0, modes_preserved=True))
            with self.assertRaisesRegex(ValueError, "Dateimenge"):
                runner.verify_archive(archive, package, {})
            with self.assertRaisesRegex(ValueError, "weicht ab"):
                runner.verify_archive(archive, package, dict.fromkeys(expected, "wrong hash"))

    def test_foreign_host_fails_before_destination_creation(self):
        if sys.platform == "darwin" and __import__("platform").machine().lower() == "arm64":
            self.skipTest("Native Plattform; kein echter Baulauf in Werkzeugtests")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "never-created"
            result = subprocess.run([sys.executable, "-B", str(TOOLS / "macos_build_run.py"), "prepare",
                                     "--repo", str(TOOLS.parents[1]), "--ziel", str(target)],
                                    capture_output=True, text=True, timeout=20)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("echten macOS-arm64", result.stderr)
            self.assertFalse(target.exists())

    def test_shell_syntax_help_and_malformed_arguments_need_no_native_build(self):
        executable = shell()
        if executable is None:
            self.skipTest("Keine lokale POSIX-Shell für Syntax-/CLI-Prüfung verfügbar")
        script = str(TOOLS / "baue_und_pruefe_macos.sh")
        for arguments, expected in ((["-n", script], 0), ([script, "--help"], 0),
                                    ([script, "--unbekannt"], 2), ([script, "--python"], 2),
                                    ([script, "--ziel", "--python"], 2)):
            with self.subTest(arguments=arguments):
                result = subprocess.run([executable] + arguments, capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
