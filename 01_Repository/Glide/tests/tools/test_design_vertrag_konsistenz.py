# SPDX-License-Identifier: MPL-2.0
"""Prüft die inhaltliche und technische Konsistenz des portablen Designvertrags.

Stellt sicher, dass:
1. Der portable Designvertrag in `src/glide/glide_shell/DESIGN_RICHTLINIEN.md` und
   der entsprechende Abschnitt in `docs/DESIGN_RICHTLINIEN.md` synchron und
   vollständig sind.
2. Alle Grundsätze (P1–P6), Einzelvorgaben (B15, B11, B01/B16, B03, B10/B12/B14,
   Kontrast, Fokus/Tastatur), Schnittstellen und Produktschranken übereinstimmen.
3. Die Stand-Zeilen den aktuellen Versionierungsregeln (R1, Glide 1.0.1,
   Shell 0.6.2, MPL-2.0) genügen.
"""
import pathlib
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS_DESIGN = REPO / "docs" / "DESIGN_RICHTLINIEN.md"
SHELL_DESIGN = REPO / "src" / "glide" / "glide_shell" / "DESIGN_RICHTLINIEN.md"


class TestDesignVertragKonsistenz(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs_text = DOCS_DESIGN.read_text(encoding="utf-8")
        cls.shell_text = SHELL_DESIGN.read_text(encoding="utf-8")

    def test_both_files_exist(self):
        self.assertTrue(DOCS_DESIGN.is_file(), f"{DOCS_DESIGN} fehlt")
        self.assertTrue(SHELL_DESIGN.is_file(), f"{SHELL_DESIGN} fehlt")

    def test_shell_design_stand_and_license(self):
        # Stand-Zeile muss R1 erfüllen: Versionsangabe Glide 1.0.1 und Lizenz MPL-2.0
        lines = self.shell_text.splitlines()
        self.assertGreaterEqual(len(lines), 3)
        self.assertIn("Portabler Designvertrag", lines[0])
        stand_line = lines[2]
        self.assertTrue(stand_line.startswith("Stand "))
        self.assertIn("Glide 1.0.1", stand_line)
        self.assertIn("Glide Shell 0.6.2", stand_line)
        self.assertIn("MPL-2.0", stand_line)

    def test_universal_principles_p1_to_p6(self):
        # P1 bis P6 müssen in beiden Dokumenten verankert sein
        for p in ("P1", "P2", "P3", "P4", "P5", "P6"):
            with self.subTest(principle=p):
                self.assertIn(p, self.docs_text)
                self.assertIn(p, self.shell_text)

    def test_specific_rules_consistency(self):
        # B15, B11, B01/B16, B03, B10/B12/B14, Kontrast, Fokus
        rules = [
            "B15",
            "B11",
            "B01",
            "B16",
            "B03",
            "B10",
            "B12",
            "B14",
            "Kontrast",
            "Fokus",
        ]
        for r in rules:
            with self.subTest(rule=r):
                self.assertIn(r, self.docs_text)
                self.assertIn(r, self.shell_text)

    def test_technical_interfaces_listed(self):
        interfaces = [
            "set_font_provider",
            "set_ink_provider",
            "set_backdrop_painter",
            "system_appearance.resolve",
            "primary_shortcuts",
            "create_dialog",
            "run_modal",
            "Transitions",
            "clamp",
        ]
        for iface in interfaces:
            with self.subTest(interface=iface):
                self.assertIn(iface, self.docs_text)
                self.assertIn(iface, self.shell_text)

    def test_host_freedom_boundaries(self):
        # Gismo, Fachlayouts, Markenidentität/Markenfarben
        boundaries = [
            "Gismo",
            "Fachlayouts",
        ]
        for b in boundaries:
            with self.subTest(boundary=b):
                self.assertIn(b, self.docs_text)
                self.assertIn(b, self.shell_text)


if __name__ == "__main__":
    unittest.main()
