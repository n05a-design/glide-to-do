# SPDX-License-Identifier: MPL-2.0
"""Release-Entwurf: nur aus Tags, nur Entwurf/Vorabversion, dieselben Paketbauten wie die Prüfung."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_macos_paket_workflow import run_blocks, shell  # noqa: E402


WORKFLOWS = Path(__file__).resolve().parents[4] / ".github/workflows"


def job(source, name):
    """Abschnitt eines Jobs bis zum nächsten Job auf gleicher Einrückung."""
    body = source.split(f"\n  {name}:\n", 1)[1]
    return re.split(r"\n  [a-z0-9-]+:\n", body, maxsplit=1)[0]


class ReleaseWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.source = (WORKFLOWS / "release.yml").read_text(encoding="utf-8")

    def test_only_tags_trigger_and_tag_must_match_version_on_main(self):
        trigger = self.source.split("\non:\n", 1)[1].split("\npermissions:", 1)[0]
        self.assertIn('tags: ["v*"]', trigger)
        self.assertNotIn("branches", trigger)
        self.assertNotIn("pull_request", trigger)
        check = job(self.source, "vorpruefung")
        self.assertIn('refs/tags/v*) ;;', check)
        self.assertIn('"$tag" != "v$version"', check)
        self.assertIn('git merge-base --is-ancestor "$GITHUB_SHA" origin/main', check)
        self.assertIn('"^## $version "', check)

    def test_never_publishes_and_never_touches_published_release(self):
        draft = job(self.source, "entwurf")
        self.assertEqual(draft.count("gh release create"), 1)
        self.assertIn("--verify-tag --draft --prerelease", draft)
        self.assertIn("gh release edit \"$tag\" --repo \"$GITHUB_REPOSITORY\" --draft --prerelease", draft)
        self.assertIn('!= "true"', draft)
        self.assertNotIn("--draft=false", self.source)
        self.assertNotIn("--latest", self.source)

    def test_permissions_are_minimal_per_job_and_no_secrets(self):
        self.assertRegex(self.source, r"(?m)^permissions:\n  contents: read\n")
        self.assertEqual(self.source.count("contents: write"), 1)
        self.assertIn("contents: write", job(self.source, "entwurf"))
        self.assertIn("actions: read", job(self.source, "vorpruefung"))
        self.assertNotIn("secrets.", self.source)
        self.assertEqual(self.source.count("persist-credentials: false"), 2)

    def test_packages_come_from_the_same_reusable_builds_as_the_checks(self):
        self.assertIn("uses: ./.github/workflows/windows-paket.yml", job(self.source, "paket-windows"))
        self.assertIn("uses: ./.github/workflows/macos-paket.yml", job(self.source, "paket-macos"))
        app = (WORKFLOWS / "python-app.yml").read_text(encoding="utf-8")
        self.assertIn("uses: ./.github/workflows/windows-paket.yml", job(app, "paket-windows"))
        windows = (WORKFLOWS / "windows-paket.yml").read_text(encoding="utf-8")
        self.assertRegex(windows, r"(?m)^  workflow_call:$")
        self.assertRegex(windows, r"(?m)^permissions:\n  contents: read\n")
        self.assertIn("pruefe_start_windows.py", windows)
        self.assertIn("name: paket-windows-glide", windows)
        for text in (self.source, windows):
            for action in re.findall(r"uses:\s*(actions/[^\s]+)", text):
                self.assertRegex(action, r"^actions/[a-z-]+@[0-9a-f]{40}$")

    def test_assets_and_notes_name_unsigned_beta_and_checksums(self):
        draft = job(self.source, "entwurf")
        for name in ("windows-x64.zip", "macos-arm64.dmg", "macos-arm64.tar.gz"):
            self.assertIn(name, draft)
        self.assertIn('sha256sum "$datei" > "$datei.sha256"', draft)
        self.assertIn("Trotzdem ausführen", draft)
        self.assertIn("Dennoch öffnen", draft)
        self.assertIn("unsigniert", draft)
        self.assertIn("01_Repository/Glide/LICENSE.md", draft)
        self.assertIn("Glide-Lizenzstatus.md", draft)

    def test_all_shell_steps_have_valid_syntax_without_running_commands(self):
        executable = shell()
        if executable is None:
            self.skipTest("Keine lokale Bash für Shell-Syntaxprüfung verfügbar")
        blocks = list(run_blocks(self.source))
        self.assertEqual(len(blocks), 5)
        with tempfile.TemporaryDirectory() as directory:
            for index, block in enumerate(blocks):
                path = Path(directory) / f"step-{index}.sh"
                path.write_text(block, encoding="utf-8")
                result = subprocess.run([executable, "-n", str(path)], capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
