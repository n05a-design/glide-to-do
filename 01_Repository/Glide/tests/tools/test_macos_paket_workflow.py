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
        self.assertIn('branches: ["codex/glide-paketabschluss-3.45.0"]', self.source)
        self.assertRegex(self.source, r"(?m)^  workflow_dispatch:$")
        self.assertIn("runs-on: macos-15", self.source)
        self.assertIn("cancel-in-progress: false", self.source)
        self.assertRegex(self.source, r"(?m)^permissions:\n  contents: read\n")
        self.assertEqual(len(re.findall(r"(?m)^\s*permissions:", self.source)), 1)
        self.assertNotIn("secrets.", self.source)
        self.assertIn("persist-credentials: false", self.source)

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
        self.assertEqual(len(blocks), 4)
        with tempfile.TemporaryDirectory() as directory:
            for index, block in enumerate(blocks):
                path = Path(directory) / f"step-{index}.sh"
                path.write_text(block, encoding="utf-8")
                result = subprocess.run([executable, "-n", str(path)], capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
