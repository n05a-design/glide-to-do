"""Mindestlaufzeit (AB08) ohne Oberfläche."""
import ast
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import runtime_check as r


class Laufzeit(unittest.TestCase):
    def test_python_levels(self):
        self.assertEqual(r.python_status((3, 11, 9))[0], "zu_alt")
        self.assertIn("3.11.9", r.python_status((3, 11, 9))[1])
        self.assertEqual(r.python_status((3, 12, 0))[0], "eingeschränkt")
        self.assertEqual(r.python_status((3, 13, 5))[0], "eingeschränkt")
        self.assertEqual(r.python_status((3, 14, 5)), ("ok", ""))
        self.assertEqual(r.python_status((4, 0, 0))[0], "ok")

    def test_tk_levels(self):
        self.assertEqual(r.tk_status(8.5)[0], "zu_alt")
        self.assertEqual(r.tk_status("8.6")[0], "eingeschränkt")
        self.assertEqual(r.tk_status(9.0), ("ok", ""))
        self.assertEqual(r.tk_status(9.1)[0], "ok")
        self.assertEqual(r.tk_status(None)[0], "zu_alt")

    def test_module_stays_parseable_for_old_python(self):
        quelle = (Path(r.__file__)).read_text(encoding="utf-8")
        baum = ast.parse(quelle, feature_version=(3, 6))
        self.assertFalse([n for n in ast.walk(baum) if isinstance(n, (ast.NamedExpr, ast.Match))])
        self.assertNotIn("f\"", quelle)
        self.assertNotIn("f'", quelle)


if __name__ == "__main__":
    unittest.main()
