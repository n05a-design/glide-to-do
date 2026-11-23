# SPDX-License-Identifier: MPL-2.0
"""T338: Validierung der agentenübergreifenden Einstiege und Skills.

Prüft:
1. Root-AGENTS.md ist vorhanden und verweist verbindlich auf die Glide-Quellen.
2. Skill-Gleichheit: `.claude/skills/glide-shell/SKILL.md` und
   `.agents/skills/glide-shell/SKILL.md` stimmen überein.
3. Copilot-Instruktionen (`.github/copilot-instructions.md`) und Gemini-Settings
   (`.gemini/settings.json`) existieren und verweisen auf AGENTS.md.
4. Trennung: Der Produkt-Skill `skills/glide-to-do` (Importdaten) und der
   Entwicklungsskill `glide-shell` (Framework-Nutzung) sind distinkt.

Aufruf: python3 -B tests/tools/test_agent_einstieg.py
"""
import pathlib
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
PROJEKT = REPO.parents[1]

class AgentEinstiegTest(unittest.TestCase):
    def test_root_agents_md_existiert_und_hat_grenzen(self):
        agents_file = PROJEKT / "AGENTS.md"
        self.assertTrue(agents_file.is_file(), "Wurzel-AGENTS.md fehlt")
        text = agents_file.read_text(encoding="utf-8")
        self.assertIn("01_Repository/Glide/AGENTS.md", text)
        self.assertIn("DESIGN_RICHTLINIEN.md", text)
        self.assertIn("GLIDE_SHELL_KI_HANDBUCH.md", text)
        self.assertIn("Die Shell bleibt frei von Glide-Fachlogik", text)

    def test_skills_sind_gespiegelt_und_konsistent(self):
        claude_dir = PROJEKT / ".claude" / "skills"
        agent_dir = PROJEKT / ".agents" / "skills"
        self.assertTrue(claude_dir.is_dir(), ".claude/skills fehlt")
        self.assertTrue(agent_dir.is_dir(), ".agents/skills fehlt")
        claude_files = sorted(p.relative_to(claude_dir) for p in claude_dir.rglob("*") if p.is_file())
        agent_files = sorted(p.relative_to(agent_dir) for p in agent_dir.rglob("*") if p.is_file())
        self.assertEqual(claude_files, agent_files, "Dateiliste zwischen .claude/skills und .agents/skills weicht ab")
        for rel in claude_files:
            c_bytes = (claude_dir / rel).read_bytes()
            a_bytes = (agent_dir / rel).read_bytes()
            self.assertEqual(c_bytes, a_bytes, f"Skill-Datei {rel} weicht zwischen .claude und .agents ab")

    def test_copilot_und_gemini_adapter_vorhanden(self):
        copilot = PROJEKT / ".github" / "copilot-instructions.md"
        gemini = PROJEKT / ".gemini" / "settings.json"
        self.assertTrue(copilot.is_file(), "copilot-instructions.md fehlt")
        self.assertTrue(gemini.is_file(), "gemini/settings.json fehlt")
        self.assertIn("AGENTS.md", copilot.read_text(encoding="utf-8"))
        self.assertIn("AGENTS.md", gemini.read_text(encoding="utf-8"))

    def test_produkt_skill_und_entwicklungsskill_sind_getrennt(self):
        prod_skill = REPO / "skills" / "glide-to-do" / "SKILL.md"
        self.assertTrue(prod_skill.is_file(), "Produkt-Skill glide-to-do fehlt")
        prod_text = prod_skill.read_text(encoding="utf-8")
        self.assertIn("glideexchange", prod_text)
        self.assertNotIn("SHELL_MODULE", prod_text)


if __name__ == "__main__":
    unittest.main()
