#!/usr/bin/env python3
"""System-und-Modulpflege: verbindliche Glide-System-Inventarprüfung.

Kontrolliert tatsächliche Quelldateien und die benannten Unit-, Integrations- und
Werkzeugdateien. Features/Bausteine/Risiken bleiben redaktionelle Register; ihre
eindeutigen IDs und die vereinbarten Abschnittsmarker werden ebenfalls geprüft.
Die Prüfung beweist Vollständigkeit, nicht die erfolgreiche Ausführung der Tests.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "src" / "glide" / "README.md"
SECTION = re.compile(r"<!-- GLIDE-SYSTEM:([A-Z]+)-(START|END) -->")
ROW = re.compile(r"^\|\s*([MFBQTG]\d{2,3})\s*\|", re.MULTILINE)
MODULE = re.compile(r"^\|\s*(M\d{3})\s*\|\s*\[`([^`]+\.pyw?)`\]\(([^)]+)\)\s*\|", re.MULTILINE)
TEST = re.compile(r"^\|\s*(T\d{3})\s*\|\s*\[`([^`]+\.py)`\]\(([^)]+)\)\s*\|", re.MULTILINE)
PARTS = ("MODULES", "FEATURES", "PACKAGES", "RISKS", "TESTS")


def sections(document: str) -> dict[str, str]:
    marks = [(m.group(1), m.group(2), m.start(), m.end()) for m in SECTION.finditer(document)]
    result = {}
    for part in PARTS:
        start = [m for m in marks if m[0] == part and m[1] == "START"]
        end = [m for m in marks if m[0] == part and m[1] == "END"]
        if len(start) != 1 or len(end) != 1 or end[0][2] <= start[0][3]:
            raise ValueError("Abschnittsmarker fehlen/stehen falsch: " + part)
        result[part] = document[start[0][3]:end[0][2]]
    return result


def registry() -> tuple[str, dict[str, str]]:
    content = REGISTER.read_text(encoding="utf-8")
    return content, sections(content)


def actual_source_modules() -> set[str]:
    return {p.name for p in (ROOT / "src" / "glide").iterdir()
            if p.is_file() and p.suffix in (".py", ".pyw")}


def actual_test_paths() -> set[str]:
    return {p.relative_to(ROOT).as_posix()
            for folder in ("unit", "integration", "tools")
            for p in (ROOT / "tests" / folder).glob("*.py") if p.is_file()}


class SystemUndModulpflegeTests(unittest.TestCase):
    def test_bereiche_und_eindeutige_ids(self):
        document, sections_by_name = registry()
        self.assertTrue(document.startswith("# Glide-System\n"))
        self.assertIn("## 7. System-und-Modulpflege", document)
        expected = {"MODULES": ("M", 94), "FEATURES": ("F", 127),
                    "PACKAGES": ("B", 22), "RISKS": ("Q", 25)}
        for section, (prefix, count) in expected.items():
            ids = ROW.findall(sections_by_name[section])
            self.assertTrue(ids, section)
            self.assertTrue(all(i.startswith(prefix) for i in ids), section)
            self.assertEqual(len(ids), len(set(ids)), section)
            # IDs may expand as Glide grows, but existing registers must not shrink.
            self.assertGreaterEqual(len(ids), count, section)

    def test_modulliste_entspricht_quellverzeichnis(self):
        _, parts = registry()
        entries = MODULE.findall(parts["MODULES"])
        names = [name for _, name, _ in entries]
        self.assertEqual(len(names), len(set(names)), "Doppelte Moduleinträge")
        self.assertEqual(set(names), actual_source_modules(),
                         "Neue/gelöschte Quelldateien im Glide-System pflegen")
        for _, name, target in entries:
            self.assertEqual(target, name, "Modullink muss lokale Quelldatei sein")
            self.assertTrue((REGISTER.parent / target).is_file())

    def test_testkatalog_entspricht_testdateien(self):
        _, parts = registry()
        entries = TEST.findall(parts["TESTS"])
        paths = []
        for _, filename, link in entries:
            self.assertTrue(link.startswith("../../tests/"), filename)
            absolute = (REGISTER.parent / link).resolve()
            self.assertTrue(absolute.is_file(), filename)
            self.assertEqual(filename, absolute.name)
            paths.append(absolute.relative_to(ROOT).as_posix())
        self.assertEqual(len(paths), len(set(paths)), "Doppelte Testdateieinträge")
        self.assertEqual(set(paths), actual_test_paths(),
                         "Neue/gelöschte Test- und Werkzeugdateien im Glide-System pflegen")

    def test_kein_weiteres_aktives_modulregister(self):
        arch = (ROOT / "docs" / "02_ARCHITECTURE.md").read_text(encoding="utf-8")
        packaging = (ROOT / "packaging" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("| Datei | Aufgabe | Seit |", arch)
        self.assertNotIn("`glide_start.py`, `drawing.py`, `drawing_image.py`", packaging)
        self.assertIn("Glide-System", arch)
        self.assertIn("Glide-System", packaging)


if __name__ == "__main__":
    unittest.main()
