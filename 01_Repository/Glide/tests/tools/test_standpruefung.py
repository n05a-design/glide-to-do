"""Regressionen für gepflegte Einstiege; kein App-Import, keine Nutzerdaten."""

import unittest
from pathlib import Path
import tempfile

import standpruefung as stand


class Einstiegspruefung(unittest.TestCase):
    def check(self, path, text):
        result = stand.Befund("3.32.3", {"DATA_SCHEMA_VERSION": 20}, suiten=58)
        stand.datei_pruefen(result, path, text)
        return result

    def test_live_documents_require_current_version(self):
        for path in stand.GEPFLEGT + ("00_Arbeitsvorbereitung/Glide_Uebergabe.md",
                                      "00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md"):
            with self.subTest(path=path):
                old = self.check(path, "# Arbeitsgrundlage\n\nStand 30.09.2026 · Glide 3.32.2\n")
                self.assertTrue(old.fehler)
                self.assertEqual(old.festgeschrieben, 0)
                current = self.check(path, "# Arbeitsgrundlage\n\nStand 01.10.2026 · Glide 3.32.3\n")
                self.assertEqual(current.fehler, [])

    def test_dated_research_and_old_contract_remain_historical(self):
        for path in ("Recherche_2026-09-30.md", "docs/70_DRAG_UND_PERFORMANCE_3.32.2.md"):
            with self.subTest(path=path):
                result = self.check(path, "# Vertrag 3.32.2\nStand 30.09.2026 · Glide 3.32.2\n"
                                    "`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.32.2/a`\n")
                self.assertEqual(result.fehler, [])
                self.assertEqual(result.festgeschrieben, 1)

    def test_current_banner_does_not_hide_stale_title(self):
        result = self.check("docs/05_QA_TESTPLAN.md",
                            "# Prüfplan – Glide 3.30.0\n\nStand 01.10.2026 · Glide 3.32.3\n")
        self.assertTrue(any("(R12)" in f for f in result.fehler))

    def test_old_first_command_inside_code_is_rejected(self):
        result = self.check("README.md", "# Glide\nStand 01.10.2026 · Glide 3.32.3\n\n"
                            "```sh\npython3 -B tests/tools/pruefen.py --modus voll --protokoll\n"
                            "tests/qa-3.30.0/abschluss\n```\n")
        self.assertTrue(any("(R13)" in f for f in result.fehler))

    def test_current_first_command_allows_later_historical_example(self):
        result = self.check("README.md", "# Glide\nStand 01.10.2026 · Glide 3.32.3\n"
                            "`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.32.3/a`\n"
                            "Historisch: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.30.0/a`\n")
        self.assertEqual(result.fehler, [])

    def test_placeholders_and_windows_paths(self):
        for path in ("tests/qa-<Version>/a", "tests\\qa-3.32.3\\a"):
            with self.subTest(path=path):
                result = self.check("README.md", "# Glide\nStand 01.10.2026 · Glide 3.32.3\n"
                                    f"`python3 tests/tools/pruefen.py --modus voll --protokoll {path}`\n")
                self.assertEqual(result.fehler, [])
        old = self.check("README.md", "# Glide\nStand 01.10.2026 · Glide 3.32.3\n"
                         "`python3 tests/tools/pruefen.py --modus voll --protokoll tests\\qa-3.30.0\\a`\n")
        self.assertTrue(any("(R13)" in f for f in old.fehler))

    def test_skill_files_need_no_stand_line_but_keep_r3(self):
        path = ".claude/skills/apple-design/SKILL.md"
        skill = self.check(path, "---\nname: apple-design\ndescription: Gestaltung\n---\n\n"
                                 "# Apple Design\n\nWWDC 2018, Tabelle 1.0 / 0.4\n")
        self.assertEqual(skill.fehler, [])
        self.assertEqual(skill.ohne_stand, 1)
        stale = self.check(path, "# Skill\n\nAktueller Entwicklungsstand: Glide 3.32.2\n")
        self.assertTrue(any("(R3)" in f for f in stale.fehler))
        other = self.check(".claude/skills/apple-design/NOTES.md", "# Notizen\n")
        self.assertTrue(any("(R1)" in f for f in other.fehler))

    def test_historical_banner_still_cannot_claim_current_old_version(self):
        result = self.check("Recherche_2026-09-30.md",
                            "# Recherche\nStand 30.09.2026 · Glide 3.32.2\n"
                            "Aktueller Entwicklungsstand: Glide 3.32.2\n")
        self.assertTrue(any("(R3)" in f for f in result.fehler))

    def test_inventory_keeps_active_documents_and_excludes_dated_snapshots(self):
        with tempfile.TemporaryDirectory(prefix="glide-standregeln-") as folder:
            root = Path(folder)
            active = root / "00_Arbeitsvorbereitung/Glide_Uebergabe.md"
            snapshot = root / "Glide_3.32.3_Zwischenstand_2026-10-01/README.md"
            archived = root / "docs/archiv/README.md"
            for file in (active, snapshot, archived):
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("# Prüfdokument\n", encoding="utf-8")
            self.assertEqual(list(stand.dokumente(root)), [active])

    def test_nested_git_worktrees_have_their_own_documentation_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            active = root / 'docs/current.md'
            active.parent.mkdir();active.write_text('# Aktuell')
            for name, directory in [('worktree', False), ('checkout', True)]:
                nested = root / name;nested.mkdir()
                if directory:
                    (nested / '.git').mkdir()
                else:
                    (nested / '.git').write_text('gitdir: elsewhere')
                (nested / 'README.md').write_text('# Eigener Stand')
            self.assertEqual(list(stand.dokumente(root)), [active])

    def test_module_lists_follow_their_own_folder(self):
        with tempfile.TemporaryDirectory() as ordner:
            wurzel = Path(ordner)
            for name in ("a.py", "b.py", "drawing_prototype.py", "app.pyw"):
                (wurzel / name).write_text("", encoding="utf-8")
            self.assertEqual(stand.modulnamen(wurzel), ["a.py", "b.py"])
        self.assertEqual(stand.fehlende_module("`a.py`", ["a.py", "b.py"]), ["b.py"])
        self.assertEqual(stand.fehlende_module("`Schnellstart.pyw`", ["glide_start.py"]), [])

    def test_current_stand_line_uses_actual_suite_count(self):
        old = self.check("tests/README.md",
                         "# Prüfungen\nStand 01.10.2026 · Glide 3.32.3 · 55 Suiten\n")
        self.assertTrue(any("(R14)" in f for f in old.fehler))
        current = self.check("tests/README.md",
                             "# Prüfungen\nStand 01.10.2026 · Glide 3.32.3 · 58 Integrationssuiten\n"
                             "Historischer Lauf 3.32.2: 57 Suiten.\n")
        self.assertEqual(current.fehler, [])
        self.assertGreater(stand.suite_anzahl(), 0)


if __name__ == "__main__":
    unittest.main()
