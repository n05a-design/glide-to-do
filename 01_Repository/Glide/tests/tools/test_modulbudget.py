# SPDX-License-Identifier: MPL-2.0
"""Werkzeugtest T322: Qualitätsbudget für neue und ausgelagerte Module (WA-50).

Prüft die Budgetregeln aus dem Entwicklungsplan (§21.89/§21.100) und der Fable-Migration:
- 0 Tkinter-Imports in Tk-freier Fachlogik
- Funktionslänge <= 50 Zeilen
- Maximale Verzweigungstiefe <= 15
- Negative Gegenproben für verletztes Budget
"""

import ast
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyse_statisch as analyse

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src" / "glide"


class ModulbudgetPruefung(unittest.TestCase):
    def test_window_lifetime_meets_budget(self):
        path = SRC / "glide_shell" / "window_lifetime.py"
        _text, tree = analyse.load(path)
        violations = analyse.check_module_budget(tree, max_length=50, max_nesting=15, allow_tk=True)
        self.assertEqual(violations, [])

    def test_modal_session_meets_budget(self):
        path = SRC / "glide_shell" / "modal_session.py"
        _text, tree = analyse.load(path)
        violations = analyse.check_module_budget(tree, max_length=50, max_nesting=15, allow_tk=True)
        self.assertEqual(violations, [])

    def test_i18n_meets_budget(self):
        path = SRC / "i18n.py"
        _text, tree = analyse.load(path)
        violations = analyse.check_module_budget(tree, max_length=50, max_nesting=15, allow_tk=False)
        self.assertEqual(violations, [])

    def test_gegenprobe_tkinter_import_in_tk_freier_logik_erkannt(self):
        code = "import tkinter as tk\n\ndef helper():\n    return 42\n"
        tree = ast.parse(code)
        violations = analyse.check_module_budget(tree, allow_tk=False)
        self.assertTrue(any("Tkinter-Import" in v for v in violations))

    def test_gegenprobe_tkinter_from_import_erkannt(self):
        code = "from tkinter import messagebox\n\ndef helper():\n    return 42\n"
        tree = ast.parse(code)
        violations = analyse.check_module_budget(tree, allow_tk=False)
        self.assertTrue(any("Tkinter-Import" in v for v in violations))

    def test_gegenprobe_funktion_ueber_fuenfzig_zeilen_erkannt(self):
        lines = ["def lange_funktion():"] + [f"    x_{i} = {i}" for i in range(55)] + ["    return x_0"]
        code = "\n".join(lines)
        tree = ast.parse(code)
        violations = analyse.check_module_budget(tree, max_length=50)
        self.assertTrue(any("überschreitet Längenbudget" in v for v in violations))

    def test_gegenprobe_verschachtelungstiefe_ueber_fuenfzehn_erkannt(self):
        indent = "    "
        code_lines = ["def tiefe_funktion(x):"]
        for i in range(16):
            code_lines.append(f"{indent * (i + 1)}if x > {i}:")
        code_lines.append(f"{indent * 17}return x")
        code = "\n".join(code_lines)
        tree = ast.parse(code)
        violations = analyse.check_module_budget(tree, max_nesting=15)
        self.assertTrue(any("überschreitet Verschachtelungsbudget" in v for v in violations))

    def test_cli_budget_exitcodes(self):
        skript = REPO / "tests" / "tools" / "analyse_statisch.py"
        with tempfile.TemporaryDirectory() as tempdir:
            gut = Path(tempdir) / "gut.py"
            gut.write_text("def ok():\n    return 1\n", encoding="utf-8")
            res_gut = subprocess.run([sys.executable, "-B", str(skript), "--quelle", str(gut), "--budget"],
                                     capture_output=True, text=True)
            self.assertEqual(res_gut.returncode, 0)
            self.assertIn("BUDGET EINGEHALTEN", res_gut.stdout)

            schlecht = Path(tempdir) / "schlecht.py"
            schlecht.write_text("import tkinter\ndef ok():\n    return 1\n", encoding="utf-8")
            res_schlecht = subprocess.run([sys.executable, "-B", str(skript), "--quelle", str(schlecht), "--budget"],
                                          capture_output=True, text=True)
            self.assertEqual(res_schlecht.returncode, 1)
            self.assertIn("BUDGET FEHLGESCHLAGEN", res_schlecht.stdout)


if __name__ == "__main__":
    unittest.main()
