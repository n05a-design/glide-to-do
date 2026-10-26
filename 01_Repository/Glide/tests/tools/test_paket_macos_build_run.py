"""Mac-Baulauf vorab prüfen, ohne Laufzeitinstallation, Paketstart oder GUI."""
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock

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

    def test_missing_and_appledouble_extra_remain_errors_with_complete_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, report = root / "Glide.tar.gz", root / "archiv-inventar.json"
            with tarfile.open(archive, "w:gz") as stream:
                member = tarfile.TarInfo("Glide.app/Contents/._Glide")
                member.size = 4
                stream.addfile(member, io.BytesIO(b"meta"))
            with self.assertRaisesRegex(ValueError, "fehlend.*Missing.*zusätzlich.*_Glide"):
                runner.verify_archive(archive, root / "Glide.app", {"Contents/Missing": "missing"}, report=report)
            result = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(result["exitcode"], 1)
            self.assertEqual(result["missing"], ["Contents/Missing"])
            self.assertEqual(result["extra"], ["Contents/._Glide"])
            self.assertEqual(result["members"][0]["name"], "Glide.app/Contents/._Glide")

    def test_duplicate_archive_entries_are_not_hidden_by_dictionary_lookup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, report = root / "Glide.tar.gz", root / "archiv-inventar.json"
            with tarfile.open(archive, "w:gz") as stream:
                for _ in range(2):
                    member = tarfile.TarInfo("Glide.app/duplicate")
                    stream.addfile(member, io.BytesIO(b""))
            with self.assertRaisesRegex(ValueError, "Doppelte.*duplicate"):
                runner.verify_archive(archive, root / "Glide.app", {"duplicate": "hash"}, report=report)
            result = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(result["duplicates"], ["Glide.app/duplicate"])
            self.assertEqual(len(result["members"]), 2)

    def test_hardlinks_count_as_files_and_their_resolved_payload_is_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "Glide.app"
            package.mkdir()
            payload = b"same payload; never executed"
            for name in ("original", "hardlink"):
                (package / name).write_bytes(payload)
            archive, report = root / "Glide.tar.gz", root / "archiv-inventar.json"
            with tarfile.open(archive, "w:gz") as stream:
                stream.add(package / "original", arcname="Glide.app/original")
                member = tarfile.TarInfo("Glide.app/hardlink")
                member.type, member.linkname = tarfile.LNKTYPE, "Glide.app/original"
                member.mode = (package / "hardlink").stat().st_mode & 0o7777
                stream.addfile(member)
            expected = {name: hashlib.sha256(payload).hexdigest() for name in ("original", "hardlink")}
            result = runner.verify_archive(archive, package, expected, report=report)
            self.assertEqual(result["files"], 2)
            proof = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(proof["checked_files"], 2)
            self.assertIn("1", [member["type"] for member in proof["members"]])

    def test_symlink_targets_are_separate_and_changes_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, report = root / "Glide.tar.gz", root / "archiv-inventar.json"
            with tarfile.open(archive, "w:gz") as stream:
                member = tarfile.TarInfo("Glide.app/Contents/Current")
                member.type, member.linkname = tarfile.SYMTYPE, "Versions/3.14"
                stream.addfile(member)
            original = mock.Mock()
            original.is_symlink.return_value = True
            original.relative_to.return_value = Path("Contents/Current")
            with mock.patch.object(Path, "rglob", return_value=[original]), mock.patch.object(
                    runner.os, "readlink", return_value="Versions/3.14"):
                result = runner.verify_archive(archive, root / "Glide.app", {}, report=report)
                self.assertEqual((result["files"], result["symlinks"]), (0, 1))
            with mock.patch.object(Path, "rglob", return_value=[original]), mock.patch.object(
                    runner.os, "readlink", return_value="Versions/3.15"):
                with self.assertRaisesRegex(ValueError, "Symlinks.*Current"):
                    runner.verify_archive(archive, root / "Glide.app", {}, report=report)
            proof = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(proof["symlink_changed"], ["Contents/Current"])
            self.assertEqual(proof["exitcode"], 1)

    def test_matching_file_bytes_cannot_hide_changed_permissions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "Glide.app"
            package.mkdir()
            (package / "Glide").write_bytes(b"payload")
            archive, report = root / "Glide.tar.gz", root / "archiv-inventar.json"
            with tarfile.open(archive, "w:gz") as stream:
                member = stream.gettarinfo(package / "Glide", arcname="Glide.app/Glide")
                member.mode ^= 0o001
                stream.addfile(member, io.BytesIO(b"payload"))
            with self.assertRaisesRegex(ValueError, "Dateimodus"):
                runner.verify_archive(archive, package, {"Glide": hashlib.sha256(b"payload").hexdigest()}, report=report)
            proof = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(proof["file_issues"], [dict(name="Glide", hash_matches=True, mode_matches=False)])

    def test_shell_syntax_help_and_malformed_arguments_need_no_native_build(self):
        executable = shell()
        if executable is None:
            self.skipTest("Keine lokale POSIX-Shell für Syntax-/CLI-Prüfung verfügbar")
        script = str(TOOLS / "baue_und_pruefe_macos.sh")
        source = Path(script).read_text(encoding="utf-8")
        self.assertIn("env COPYFILE_DISABLE=1 /usr/bin/tar --no-mac-metadata --no-xattrs", source)
        for arguments, expected in ((["-n", script], 0), ([script, "--help"], 0),
                                    ([script, "--unbekannt"], 2), ([script, "--python"], 2),
                                    ([script, "--ziel", "--python"], 2)):
            with self.subTest(arguments=arguments):
                result = subprocess.run([executable] + arguments, capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
