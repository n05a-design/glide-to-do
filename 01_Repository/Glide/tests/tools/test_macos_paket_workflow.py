# SPDX-License-Identifier: MPL-2.0
"""Mac-Paketworkflow: Shell/Python-Syntax und begrenzte CI-Vertrauensgrenzen."""
import ast
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest


WORKFLOW = Path(__file__).resolve().parents[4] / ".github/workflows/macos-paket.yml"


def run_blocks(source):
    """Nur die eingerückten Shell-Literale lesen, kein eigener YAML-Parser."""
    lines = source.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "run: |":
            continue
        indent = len(line) - len(line.lstrip())
        body = []
        for child in lines[index + 1:]:
            if child.strip() and len(child) - len(child.lstrip()) <= indent:
                break
            body.append(child)
        yield textwrap.dedent("\n".join(body)) + "\n"


def shell():
    if os.name == "nt":
        candidate = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe"
        return str(candidate) if candidate.is_file() else None
    return shutil.which("bash")


class MacWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.source = WORKFLOW.read_text(encoding="utf-8")

    def test_native_runner_branch_and_minimum_permission_contract(self):
        self.assertIn('branches: ["main", "codex/**"]', self.source)
        self.assertRegex(self.source, r"(?m)^  workflow_dispatch:$")
        self.assertRegex(self.source, r"(?m)^  workflow_call:$")
        self.assertIn("runs-on: macos-15", self.source)
        self.assertIn("cancel-in-progress: false", self.source)
        self.assertRegex(self.source, r"(?m)^permissions:\n  contents: read\n")
        self.assertEqual(len(re.findall(r"(?m)^\s*permissions:", self.source)), 1)
        self.assertNotIn("secrets.", self.source)
        self.assertIn("persist-credentials: false", self.source)
        checkout = self.source.split('- name: Unveränderten Commit auschecken',1)[1].split('      - name:',1)[0]
        self.assertIn('fetch-depth: 0',checkout)

    def test_only_verified_actions_and_original_installer_are_used(self):
        actions = re.findall(r"uses:\s*([^\s]+)", self.source)
        self.assertEqual(len(actions), 3)
        for action in actions:
            self.assertRegex(action, r"^actions/(checkout|upload-artifact)@[0-9a-f]{40}$")
        self.assertIn("https://www.python.org/ftp/python/3.14.5/python-3.14.5-macos11.pkg", self.source)
        self.assertIn("b28a8dc33c456dd06c97024697d63ca916cfb494594c06fa3e4ef4d41fa82335", self.source)
        self.assertIn("shasum -a 256 -c -", self.source)
        self.assertIn("pkgutil --check-signature", self.source)
        self.assertIn('test "$(uname -m)" = arm64', self.source)

    def test_embedded_python_proofs_compile_without_execution(self):
        scripts = []
        for block in run_blocks(self.source):
            scripts.extend(re.findall(r"<<'PY'\n(.*?)^PY$", block, re.MULTILINE | re.DOTALL))
        self.assertEqual(len(scripts), 2)
        for script in scripts:
            ast.parse(script, filename=str(WORKFLOW))

    def test_all_shell_steps_have_valid_syntax_without_running_commands(self):
        executable = shell()
        if executable is None:
            self.skipTest("Keine lokale Bash für Shell-Syntaxprüfung verfügbar")
        blocks = list(run_blocks(self.source))
        self.assertEqual(len(blocks), 8)
        with tempfile.TemporaryDirectory() as directory:
            for index, block in enumerate(blocks):
                path = Path(directory) / f"step-{index}.sh"
                path.write_text(block, encoding="utf-8")
                result = subprocess.run([executable, "-n", str(path)], capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_optional_full_qa_uses_native_runtime_and_preserves_evidence(self):
        self.assertRegex(self.source, r"vollpruefung:\n\s+description:.*\n\s+type: boolean\n\s+default: false")
        step = self.source.split("- name: Vollständige native macOS-Prüfung", 1)[1].split("      - name:", 1)[0]
        self.assertIn("github.event_name == 'workflow_dispatch' && inputs.vollpruefung", step)
        self.assertIn('"$MAC_PYTHON" -B tests/tools/pruefen.py --zugang-nativ --modus voll --vordergrund', step)
        self.assertIn('tests/tools/macos_desktop.py --breite 1920 --hoehe 1080', step)
        self.assertIn('${{ runner.temp }}/glide-macos-desktop.json', self.source)
        self.assertIn('--protokoll "$RUNNER_TEMP/glide-macos-voll" --timeout 900', step)
        self.assertNotIn("continue-on-error", self.source)
        self.assertIn("tests/integration/test_bedienung33316.py", self.source)
        focused = self.source.split('- name: Bekannten Mac-Bedienbefund gezielt nachprüfen',1)[1].split('      - name:',1)[0]
        self.assertIn('tests/tools/macos_desktop.py --breite 1920 --hoehe 1080', focused)
        self.assertIn('glide-macos-bedienung-desktop.json', focused)
        self.assertIn("steps.runtime_bau.outcome == 'success'", step)
        freeze = self.source.split('- name: Originalruntime und konkrete Bauquellen einfrieren',1)[1].split('      - name:',1)[0]
        self.assertIn('GLIDE_VOLLPRUEFUNG',freeze)
        self.assertIn('from historical_runtime import SNAPSHOTS, DELIVERY',freeze)
        self.assertIn('"cat-file", "-e"',freeze)
        self.assertIn('cwd=outer, check=True',freeze)
        self.assertIn("${{ runner.temp }}/glide-macos-voll", self.source)
        self.assertLess(self.source.index("PYTHONPATH=%s"), self.source.index("- name: Vollständige native macOS-Prüfung"))

    def test_dmg_is_built_from_checked_archive_and_compared_after_mount(self):
        step = self.source.split("- name: Geprüftes Archiv als DMG verpacken und Inhalt gegenprüfen", 1)[1].split("      - name:", 1)[0]
        self.assertIn('/usr/bin/tar -xzf "$archiv" -C "$inhalt"', step)
        self.assertNotIn("bau/dist", step)
        self.assertIn("hdiutil create", step)
        self.assertIn("hdiutil verify", step)
        self.assertIn("hdiutil attach -readonly", step)
        self.assertIn('cmp "$bau/dmg-soll.txt" "$bau/dmg-ist.txt"', step)
        self.assertIn('codesign --verify --deep --strict "$mnt/Glide.app"', step)
        self.assertIn("Glide-*-macos-arm64.dmg.sha256", self.source)
        order = [self.source.index(name) for name in (
            "- name: Eingefrorenen Stand nach Archiv- und Startprüfung erneut abgleichen",
            "- name: Geprüftes Archiv als DMG verpacken und Inhalt gegenprüfen",
            "- name: Geprüftes Mac-Archiv mit erhaltenen Dateimodi und Symlinks sichern")]
        self.assertEqual(order, sorted(order))


if __name__ == "__main__":
    unittest.main()
