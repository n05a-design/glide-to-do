"""Namens- und Verweisprüfung der Design Richtlinien (B20, 15.10.2026).

Der aktive Gestaltungsskill heißt neutral `design-richtlinien` und verweist auf
das zentrale Dokument. Der übernommene Fremdtext bleibt mit Lizenz und
Herkunft erhalten. Aktive Dokumente nennen den früheren markenbezogenen
Skillnamen nicht mehr als Projektnamen; historische Belege (Originalauftrag,
Prompt, frühere Nachweise) bleiben unverändert.
"""
import re
import unittest
from pathlib import Path

PROJEKT = Path(__file__).resolve().parents[4]
GLIDE = PROJEKT / "01_Repository" / "Glide"
SKILL = PROJEKT / ".claude" / "skills" / "design-richtlinien"
ALTER_NAME = "apple-" + "design"

# Aktive Einstiegs- und Regeldokumente. Historische Eingangsbelege und datierte
# Nachweise gehören nicht dazu.
AKTIVE_DOKUMENTE = (
    PROJEKT / "CLAUDE.md",
    PROJEKT / "README.md",
    GLIDE / "AGENTS.md",
    GLIDE / "docs" / "DESIGN_RICHTLINIEN.md",
    GLIDE / "docs" / "00_INDEX.md",
    GLIDE / "docs" / "DOKUMENTENPFLEGE.md",
    PROJEKT / "00_Arbeitsvorbereitung" / "Glide_Uebergabe.md",
    PROJEKT / "00_Arbeitsvorbereitung" / "README.md",
)


@unittest.skipUnless(SKILL.parent.is_dir(), "Projekt-Skills liegen nur in der vollständigen Arbeitskopie")
class DesignRichtlinienTests(unittest.TestCase):
    def test_active_skill_has_neutral_name_and_points_to_central_document(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        kopf = re.match(r"---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(kopf, "Skillkopf fehlt")
        self.assertIn("name: design-richtlinien", kopf.group(1))
        self.assertNotIn(ALTER_NAME, text.lower())
        self.assertIn("docs/DESIGN_RICHTLINIEN.md", text)
        self.assertTrue((GLIDE / "docs" / "DESIGN_RICHTLINIEN.md").is_file())

    def test_no_second_active_design_skill(self):
        self.assertFalse((SKILL.parent / ALTER_NAME).exists(), "früherer Skillordner ist noch aktiv")
        aktive = [pfad for pfad in SKILL.parent.glob("*/SKILL.md")
                  if ALTER_NAME in pfad.read_text(encoding="utf-8").lower().split("---")[1]]
        self.assertEqual(aktive, [], "ein aktiver Skillkopf trägt noch den früheren Namen")

    def test_license_and_provenance_are_kept(self):
        lizenz = (SKILL / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", lizenz)
        self.assertIn("Emil Kowalski", lizenz)
        referenzen = list((SKILL / "referenzen").glob("*.md"))
        self.assertTrue(referenzen, "Fremdreferenz fehlt")
        for pfad in referenzen:
            text = pfad.read_text(encoding="utf-8")
            self.assertIn("emilkowalski/skills", text, pfad.name)
            self.assertIn("MIT", text, pfad.name)

    def test_active_documents_do_not_use_the_former_name(self):
        for pfad in AKTIVE_DOKUMENTE:
            if not pfad.is_file():
                continue
            with self.subTest(dokument=pfad.name):
                self.assertNotIn(f"skills/{ALTER_NAME}", pfad.read_text(encoding="utf-8"))
                self.assertNotIn(f"`{ALTER_NAME}`", pfad.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
