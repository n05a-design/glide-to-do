# SPDX-License-Identifier: MPL-2.0
"""Übernahmewerkzeug der Glide Shell (D95): Kopie, Manifest, Prüfung und Schutz lokaler Änderungen.

Prüft `scripts/pflege/shell_uebernehmen.py` gegen Temporärordner, nie gegen
den Quellbaum: Erstkopie mit Manifest und Lizenztext, Prüfung „aktuell“,
verweigerte Übernahme bei lokaler Änderung, bewusstes Ersetzen, veraltete
Kopie, Entfernen nicht mehr gelieferter Dateien bei Erhalt fremder Dateien,
Schutz eigener Dateien vor neuen Shell-Dateien gleichen Namens und die Sperre
gegen ein Ziel im Glide-Quellbaum. Negative Vertragsfälle: manipulierte Datei,
inkonsistentes Manifest, abweichende Version, fehlende Datei, zusätzliches
Modul, lokal veränderte Quelle, fehlende oder beschädigte Quelle und
unbekannter Commit, jeweils mit eindeutigem Exitcode (1 Abweichung, 2 Konflikt
im Ziel, 3 Quelle unbrauchbar). Die Quellfälle laufen gegen ein temporäres
Git-Repository mit derselben Ordnerstruktur, nie gegen die Arbeitskopie.
Ohne Tk-Import.

Aufruf: python3 -B -m unittest tests/tools/test_shell_uebernahme.py
"""
import contextlib
import importlib.util
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.parse

REPO = pathlib.Path(__file__).resolve().parents[2]
WERKZEUG = REPO / "scripts" / "pflege" / "shell_uebernehmen.py"
QUELLE = REPO / "src" / "glide" / "glide_shell"

spec = importlib.util.spec_from_file_location("glide_shell_uebernehmen_pruefling", WERKZEUG)
werkzeug = importlib.util.module_from_spec(spec)
spec.loader.exec_module(werkzeug)


def lauf(*argumente):
    """Ruft das Werkzeug gegen die Arbeitskopie auf; deren Sauberkeit prüfen die Quellfälle getrennt."""
    ausgabe = io.StringIO()
    with contextlib.redirect_stdout(ausgabe):
        try:
            code = werkzeug.main(["--unsauber-erlauben"] + [str(a) for a in argumente])
        except SystemExit as fehler:
            code = fehler.code
    return code, ausgabe.getvalue()


class Uebernahme(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory(prefix="glide-shell-ueb-")
        self.projekt = pathlib.Path(self._temp.name) / "folgeprojekt"
        self.kopie = self.projekt / "glide_shell"

    def tearDown(self):
        self._temp.cleanup()

    def test_erstkopie_mit_manifest_und_pruefung_aktuell(self):
        code, text = lauf(self.projekt)
        self.assertEqual(code, 0, text)
        quelle = sorted([p.name for p in QUELLE.iterdir() if p.suffix in (".py", ".md")] + ["LICENSE"])
        self.assertIn("README.md", quelle)
        self.assertIn("README.de.md", quelle)
        self.assertIn("selftest.py", quelle)
        self.assertEqual(sorted(p.name for p in self.kopie.iterdir() if p.name != "SHELL_MANIFEST.json"), quelle)
        manifest = json.loads((self.kopie / "SHELL_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["paket"], "glide_shell")
        self.assertEqual(manifest["shell_version"], werkzeug.shell_version())
        self.assertEqual(manifest["lizenz"], "MPL-2.0")
        self.assertIn(manifest["quelle_unveraendert"], (True, False, None))
        self.assertTrue((self.kopie / "LICENSE").read_text(encoding="utf-8").startswith("Mozilla Public License Version 2.0"))
        self.assertEqual(sorted(manifest["dateien"]), quelle)
        for name, wert in manifest["dateien"].items():
            self.assertEqual(werkzeug.sha(self.kopie / name), wert, name)
        code, text = lauf("--pruefen", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertNotIn("veraltet", text)
        self.assertIn("motion.py: aktuell", text)

    def test_kopie_ist_ohne_glide_importierbar(self):
        lauf(self.projekt)
        kind = ("import sys; sys.path[:] = [p for p in sys.path if 'src' not in p]; "
                f"sys.path.insert(0, {str(self.projekt)!r}); "
                "import glide_shell, glide_shell.motion as m, glide_shell.window_lifetime; "
                f"assert glide_shell.__file__.startswith({str(self.projekt)!r}); "
                "print(glide_shell.SHELL_VERSION, m.progress(0.06, 120) > 0)")
        ergebnis = subprocess.run([sys.executable, "-B", "-c", kind], capture_output=True, text=True,
                                  cwd=self.projekt, timeout=60)
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)
        self.assertEqual(ergebnis.stdout.split(), [werkzeug.shell_version(), "True"])

    def test_lokale_aenderung_wird_nicht_ueberschrieben(self):
        lauf(self.projekt)
        datei = self.kopie / "motion.py"
        datei.write_text(datei.read_text(encoding="utf-8") + "\n# lokale Anpassung\n", encoding="utf-8")
        code, text = lauf("--pruefen", self.projekt)
        self.assertEqual(code, 1)
        self.assertIn("motion.py: verändert", text)
        code, text = lauf(self.projekt)
        self.assertEqual(code, 2, text)
        self.assertIn("lokale Anpassung", datei.read_text(encoding="utf-8"))
        code, text = lauf("--ersetzen", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertEqual(werkzeug.sha(datei), werkzeug.sha(QUELLE / "motion.py"))

    def test_fremder_ordner_ohne_manifest_bleibt_unberuehrt(self):
        self.kopie.mkdir(parents=True)
        (self.kopie / "eigen.py").write_text("x = 1\n", encoding="utf-8")
        code, text = lauf(self.projekt)
        self.assertEqual(code, 2, text)
        self.assertEqual(sorted(p.name for p in self.kopie.iterdir()), ["eigen.py"])

    def test_veraltete_kopie_wird_aktualisiert_und_alte_dateien_entfernt(self):
        lauf(self.projekt)
        pfad = self.kopie / "SHELL_MANIFEST.json"
        manifest = json.loads(pfad.read_text(encoding="utf-8"))
        # Älterer Stand: motion.py hatte anderen Inhalt, dazu ein inzwischen entfallenes Modul.
        alt = b"# SPDX-License-Identifier: MPL-2.0\n# alte Fassung\n"
        (self.kopie / "motion.py").write_bytes(alt)
        (self.kopie / "entfallen.py").write_bytes(alt)
        (self.kopie / "notizen.txt").write_text("vom Folgeprojekt\n", encoding="utf-8")
        init = self.kopie / "__init__.py"
        init.write_text(init.read_text(encoding="utf-8").replace(werkzeug.shell_version(), "0.0.9"), encoding="utf-8")
        manifest["shell_version"] = "0.0.9"
        manifest["dateien"]["__init__.py"] = werkzeug.sha(init)
        manifest["dateien"]["motion.py"] = werkzeug.sha(self.kopie / "motion.py")
        manifest["dateien"]["entfallen.py"] = werkzeug.sha(self.kopie / "entfallen.py")
        pfad.write_text(json.dumps(manifest), encoding="utf-8")
        code, text = lauf("--pruefen", self.projekt)
        self.assertEqual(code, 1)
        self.assertIn("Kopie 0.0.9", text)
        self.assertIn("motion.py: veraltet", text)
        self.assertIn("entfallen.py: nicht mehr in der Quelle", text)
        code, text = lauf(self.projekt)
        self.assertEqual(code, 0, text)
        self.assertFalse((self.kopie / "entfallen.py").exists())
        self.assertTrue((self.kopie / "notizen.txt").is_file())
        self.assertIn("notizen.txt: bleibt stehen", text)
        self.assertEqual(lauf("--pruefen", self.projekt)[0], 0)

    def test_eigene_datei_mit_neuem_shellnamen_bleibt_geschuetzt(self):
        lauf(self.projekt)
        pfad = self.kopie / "SHELL_MANIFEST.json"
        manifest = json.loads(pfad.read_text(encoding="utf-8"))
        # Älteres Manifest ohne motion.py; das Folgeprojekt hat eine eigene motion.py angelegt.
        del manifest["dateien"]["motion.py"]
        pfad.write_text(json.dumps(manifest), encoding="utf-8")
        datei = self.kopie / "motion.py"
        datei.write_text("# eigenes Modul des Folgeprojekts\n", encoding="utf-8")
        code, text = lauf(self.projekt)
        self.assertEqual(code, 2, text)
        self.assertIn("motion.py: eigene Datei ohne Manifesteintrag", text)
        self.assertEqual(datei.read_text(encoding="utf-8"), "# eigenes Modul des Folgeprojekts\n")
        self.assertNotIn("motion.py", json.loads(pfad.read_text(encoding="utf-8"))["dateien"])
        code, text = lauf("--ersetzen", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertEqual(werkzeug.sha(datei), werkzeug.sha(QUELLE / "motion.py"))

    def test_ziel_im_glide_quellbaum_wird_abgelehnt(self):
        for ziel in (QUELLE.parent, QUELLE, QUELLE / "unter"):
            with self.subTest(ziel=ziel):
                code, _ = lauf(ziel)
                self.assertNotEqual(code, 0)
        self.assertFalse((QUELLE / "SHELL_MANIFEST.json").exists())
        self.assertFalse((QUELLE / "glide_shell").exists())

    def _manifest(self):
        return json.loads((self.kopie / "SHELL_MANIFEST.json").read_text(encoding="utf-8"))

    def _manifest_schreiben(self, daten):
        (self.kopie / "SHELL_MANIFEST.json").write_text(json.dumps(daten), encoding="utf-8")

    def test_inkonsistentes_manifest_wird_erkannt_und_nicht_ueberschrieben(self):
        faelle = {
            "falsches Paket": lambda m: m.update(paket="anderes"),
            "kein SemVer": lambda m: m.update(shell_version="neu"),
            "Pfad im Dateinamen": lambda m: m["dateien"].update({"../host.py": "0" * 64}),
            "kein SHA-256": lambda m: m["dateien"].update({"motion.py": "abc"}),
            "falsche Lizenz": lambda m: m.update(lizenz="MIT"),
            "abweichende Version": lambda m: m.update(shell_version="9.9.9"),
        }
        lauf(self.projekt)
        gut = self._manifest()
        for name, aendern in faelle.items():
            with self.subTest(fall=name):
                daten = json.loads(json.dumps(gut))
                aendern(daten)
                self._manifest_schreiben(daten)
                code, text = lauf("--pruefen", self.projekt)
                self.assertEqual(code, 1, text)
                self.assertIn("SHELL_MANIFEST.json: ungültig", text)
                code, text = lauf(self.projekt)
                self.assertEqual(code, 2, text)
                self.assertEqual(self._manifest(), daten, "verweigerte Übernahme darf nichts schreiben")
        (self.kopie / "SHELL_MANIFEST.json").write_text("{kaputt", encoding="utf-8")
        self.assertEqual(lauf(self.projekt)[0], 2)
        self.assertEqual(lauf("--ersetzen", self.projekt)[0], 0)
        self.assertEqual(lauf("--pruefen", self.projekt)[0], 0)

    def test_fehlende_datei_und_zusaetzliches_modul(self):
        lauf(self.projekt)
        (self.kopie / "text_fit.py").unlink()
        code, text = lauf("--pruefen", self.projekt)
        self.assertEqual(code, 1)
        self.assertIn("text_fit.py: fehlt", text)
        self.assertEqual(lauf(self.projekt)[0], 2)
        lauf("--ersetzen", self.projekt)
        (self.kopie / "fremd.py").write_text("import os\n", encoding="utf-8")
        code, text = lauf("--pruefen", self.projekt)
        self.assertEqual(code, 1)
        self.assertIn("fremd.py: zusätzlich", text)

    def test_update_laesst_hostdateien_ausserhalb_unberuehrt(self):
        (self.projekt / "app.py").parent.mkdir(parents=True, exist_ok=True)
        (self.projekt / "app.py").write_text("# Host\n", encoding="utf-8")
        (self.projekt / "glide_shell_extra.py").write_text("# Host\n", encoding="utf-8")
        vorher = {p.name: p.read_bytes() for p in self.projekt.iterdir() if p.is_file()}
        lauf(self.projekt)
        lauf(self.projekt)
        nachher = {p.name: p.read_bytes() for p in self.projekt.iterdir() if p.is_file()}
        self.assertEqual(vorher, nachher)
        self.assertEqual(sorted(p.name for p in self.projekt.iterdir()), ["app.py", "glide_shell", "glide_shell_extra.py"])

    def test_rollback_stellt_ausgangszustand_bei_abbruch_wieder_her(self):
        lauf(self.projekt)
        datei = self.kopie / "motion.py"
        inhalt_vorher = datei.read_bytes()
        manifest_vorher = (self.kopie / "SHELL_MANIFEST.json").read_bytes()
        host_datei = self.kopie / "host_config.json"
        host_datei.write_text('{"host": true}', encoding="utf-8")

        original_schreiben = werkzeug.schreiben_atomar
        aufrufe = [0]

        def fehlerhaftes_schreiben(ziel, inhalt):
            aufrufe[0] += 1
            if aufrufe[0] >= 3:
                raise OSError("Simulierter I/O-Fehler beim Kopieren")
            return original_schreiben(ziel, inhalt)

        try:
            werkzeug.schreiben_atomar = fehlerhaftes_schreiben
            code, meldungen = werkzeug.uebernehmen(self.kopie, ersetzen=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback ausgeführt" in m for m in meldungen))
        finally:
            werkzeug.schreiben_atomar = original_schreiben

        self.assertEqual(datei.read_bytes(), inhalt_vorher)
        self.assertEqual((self.kopie / "SHELL_MANIFEST.json").read_bytes(), manifest_vorher)
        self.assertTrue(host_datei.is_file())
        self.assertEqual(host_datei.read_text(encoding="utf-8"), '{"host": true}')

    def test_rollback_entfernt_neu_angelegten_ordner_bei_abbruch(self):
        ziel_neu = self.projekt / "neu_glide_shell"
        self.assertFalse(ziel_neu.exists())

        original_schreiben = werkzeug.schreiben_atomar

        def fehlerhaftes_schreiben(ziel, inhalt):
            raise OSError("Simulierter Plattenfehler")

        try:
            werkzeug.schreiben_atomar = fehlerhaftes_schreiben
            code, meldungen = werkzeug.uebernehmen(ziel_neu, ersetzen=False)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback ausgeführt" in m for m in meldungen))
        finally:
            werkzeug.schreiben_atomar = original_schreiben

        self.assertFalse(ziel_neu.exists(), "Neuer Ordner muss nach fehlgeschlagener Übernahme entfernt werden")

    def test_snapshot_erstellung_fehler_laesst_ziel_unberuehrt(self):
        lauf(self.projekt)
        vorher = {p.name: p.read_bytes() for p in self.kopie.iterdir() if p.is_file()}
        self.assertGreater(len(vorher), 10)

        original_copy2 = shutil.copy2
        aufrufe = [0]

        def fehlerhafter_snapshot(src, dst, **kw):
            aufrufe[0] += 1
            if aufrufe[0] >= 2:
                raise OSError("Simulierter Lese-/Kopierfehler während Snapshot-Erstellung")
            return original_copy2(src, dst, **kw)

        try:
            shutil.copy2 = fehlerhafter_snapshot
            code, meldungen = werkzeug.uebernehmen(self.kopie, ersetzen=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Sicherung fehlgeschlagen" in m for m in meldungen))
        finally:
            shutil.copy2 = original_copy2

        nachher = {p.name: p.read_bytes() for p in self.kopie.iterdir() if p.is_file()}
        self.assertEqual(sorted(vorher.keys()), sorted(nachher.keys()))
        for name, inhalt in vorher.items():
            self.assertEqual(inhalt, nachher[name], f"Datei {name} wurde trotz Snapshot-Abbruch verändert!")

    def test_symlinks_im_zielordner_werden_verweigert(self):
        self.kopie.mkdir(parents=True)
        link = self.kopie / "link.py"
        try:
            link.symlink_to(QUELLE / "motion.py")
        except OSError:
            self.skipTest("Symlinks auf diesem Dateisystem nicht unterstützt")

        code, text = lauf(self.projekt)
        self.assertEqual(code, 2, text)
        self.assertIn("symbolischer Link", text)

    def test_symlink_als_manifest_oder_modul_wird_als_ungueltig_erkannt(self):
        lauf(self.projekt)
        manifest_pfad = self.kopie / "SHELL_MANIFEST.json"
        manifest_pfad.unlink()
        try:
            manifest_pfad.symlink_to(QUELLE / "README.md")
        except OSError:
            self.skipTest("Symlinks auf diesem Dateisystem nicht unterstützt")

        code, text = lauf("--pruefen", self.projekt)
        self.assertEqual(code, 1, text)
        self.assertIn("symbolischer Link ist unzulässig", text)

    def test_agenten_bootstrap_in_leerem_workspace(self):
        code, text = lauf("--agenten-bootstrap", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertIn("AGENTS.md: angelegt", text)
        self.assertIn("Antigravity/Codex-Skill", text)
        self.assertIn("Claude-Skill", text)

        agents_md = self.projekt / "AGENTS.md"
        self.assertTrue(agents_md.is_file())
        inhalt_agents = agents_md.read_text(encoding="utf-8")
        self.assertIn("KI_ANLEITUNG_NEUE_PROJEKTE.md", inhalt_agents)
        self.assertIn("STARTPROMPT_KI.md", inhalt_agents)
        self.assertIn("DESIGN_RICHTLINIEN.md", inhalt_agents)
        self.assertIn("selftest", inhalt_agents)
        # Sicherstellen: Keine Glide-internen Domänenbegriffe
        self.assertNotIn("D86", inhalt_agents)
        self.assertNotIn("Aufgabenformat", inhalt_agents)

        skill_agents = self.projekt / ".agents" / "skills" / "glide-shell" / "SKILL.md"
        self.assertTrue(skill_agents.is_file())
        self.assertIn("name: glide-shell", skill_agents.read_text(encoding="utf-8"))

        skill_claude = self.projekt / ".claude" / "skills" / "glide-shell" / "SKILL.md"
        self.assertTrue(skill_claude.is_file())
        self.assertIn("name: glide-shell", skill_claude.read_text(encoding="utf-8"))

        design_md = self.kopie / "DESIGN_RICHTLINIEN.md"
        self.assertTrue(design_md.is_file())
        inhalt_design = design_md.read_text(encoding="utf-8")
        self.assertIn("Portabler Designvertrag", inhalt_design)
        self.assertIn("B15", inhalt_design)
        self.assertIn("B11", inhalt_design)

        # Re-Run überschreibt existierende AGENTS.md nicht ohne --ersetzen
        agents_md.write_text("# Eigener Titel\n", encoding="utf-8")
        code, text = lauf("--agenten-bootstrap", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertEqual(agents_md.read_text(encoding="utf-8"), "# Eigener Titel\n")
        self.assertIn("existiert bereits", text)

        # Mit --ersetzen wird auch AGENTS.md aktualisiert
        code, text = lauf("--agenten-bootstrap", "--ersetzen", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertIn("aktualisiert", text)
        self.assertNotEqual(agents_md.read_text(encoding="utf-8"), "# Eigener Titel\n")

    def test_agenten_bootstrap_verschachtelte_struktur_und_link_gueltigkeit(self):
        """Prüft verschachtelte Struktur projekt/src/app/glide_shell und die Gültigkeit aller Links."""
        nested_proj = pathlib.Path(self._temp.name) / "nested_project"
        nested_proj.mkdir(parents=True)
        (nested_proj / "pyproject.toml").write_text("[project]\nname='nested'\n", encoding="utf-8")
        app_dir = nested_proj / "src" / "myapp"
        app_dir.mkdir(parents=True)

        code, text = lauf("--agenten-bootstrap", app_dir)
        self.assertEqual(code, 0, text)

        # 1. Platzierung an der Projektwurzel (nicht in src/myapp!)
        agents_md = nested_proj / "AGENTS.md"
        self.assertTrue(agents_md.is_file(), "AGENTS.md muss an der Projektwurzel liegen")
        self.assertFalse((app_dir / "AGENTS.md").exists(), "AGENTS.md darf nicht in src/myapp liegen")

        skill_agents = nested_proj / ".agents" / "skills" / "glide-shell" / "SKILL.md"
        skill_claude = nested_proj / ".claude" / "skills" / "glide-shell" / "SKILL.md"
        self.assertTrue(skill_agents.is_file())
        self.assertTrue(skill_claude.is_file())

        shell_dir = app_dir / "glide_shell"
        self.assertTrue(shell_dir.is_dir())
        self.assertTrue((shell_dir / "DESIGN_RICHTLINIEN.md").is_file())

        # 2. Automatisierter Linktest für alle generierten Dokumente
        for doc_file in (agents_md, skill_agents, skill_claude):
            doc_text = doc_file.read_text(encoding="utf-8")
            raw_links = re.findall(r'\[(?:[^\]]+)\]\(([^)]+)\)', doc_text)
            self.assertGreater(len(raw_links), 0, f"Keine Links in {doc_file.name} gefunden")
            for link in raw_links:
                if link.startswith("http://") or link.startswith("https://"):
                    continue
                # URL-Decoding für lokale Dateilinks
                decoded_path = urllib.parse.unquote(link)
                target = (doc_file.parent / decoded_path).resolve()
                self.assertTrue(target.is_file(),
                                f"In {doc_file.relative_to(nested_proj)}: Link '{link}' -> '{target}' existiert nicht!")

    def test_agenten_bootstrap_explizite_projekt_root(self):
        """Prüft explizite Vorgabe von --projekt-root / --project-root und Ablehnung im Glide-Quellbaum."""
        custom_root = pathlib.Path(self._temp.name) / "custom_root"
        custom_root.mkdir()
        target_shell = pathlib.Path(self._temp.name) / "irgendwo" / "tief" / "glide_shell"

        code, text = lauf("--agenten-bootstrap", "--projekt-root", custom_root, target_shell)
        self.assertEqual(code, 0, text)
        self.assertTrue((custom_root / "AGENTS.md").is_file())
        self.assertTrue((custom_root / ".agents" / "skills" / "glide-shell" / "SKILL.md").is_file())
        self.assertTrue((target_shell / "SHELL_MANIFEST.json").is_file())

        # Ablehnung wenn projekt-root im Glide-Quellbaum liegt
        code, text = lauf("--agenten-bootstrap", "--projekt-root", QUELLE, target_shell)
        self.assertEqual(code, 2, text)
        self.assertIn("Projektwurzel unzulässig", text)

    def test_agenten_bootstrap_pfade_mit_leerzeichen_und_unicode(self):
        """Prüft Pfade mit Leerzeichen und Sonderzeichen/Unicode."""
        space_proj = pathlib.Path(self._temp.name) / "Mein Projekt 2026 🚀"
        app_dir = space_proj / "src" / "Haupt App"
        app_dir.mkdir(parents=True)

        code, text = lauf("--agenten-bootstrap", app_dir)
        self.assertEqual(code, 0, text)

        agents_md = space_proj / "AGENTS.md"
        self.assertTrue(agents_md.is_file())
        skill_file = space_proj / ".agents" / "skills" / "glide-shell" / "SKILL.md"
        self.assertTrue(skill_file.is_file())

        for doc_file in (agents_md, skill_file):
            doc_text = doc_file.read_text(encoding="utf-8")
            raw_links = re.findall(r'\[(?:[^\]]+)\]\(([^)]+)\)', doc_text)
            for link in raw_links:
                if link.startswith("http"):
                    continue
                decoded = urllib.parse.unquote(link)
                target = (doc_file.parent / decoded).resolve()
                self.assertTrue(target.is_file(), f"Ungültiger Link '{link}' in {doc_file}")

    def test_agenten_bootstrap_transaktions_rollback_bei_fehler(self):
        """Simuliert Fehler beim Schreiben von Agentendateien und beweist vollständigen Rollback."""
        proj = pathlib.Path(self._temp.name) / "fail_proj"
        shell_target = proj / "glide_shell"

        original_schreiben = werkzeug.schreiben_atomar
        aufrufe = [0]

        def fehler_beim_zweiten_skill(ziel, inhalt):
            # Erlaube Schreiben der Shell-Dateien
            if ".claude" in str(ziel):
                raise OSError("Künstlicher Plattenfehler beim Schreiben des Claude-Skills")
            return original_schreiben(ziel, inhalt)

        try:
            werkzeug.schreiben_atomar = fehler_beim_zweiten_skill
            code, meldungen = werkzeug.uebernehmen(shell_target, agenten_bootstrap=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback ausgeführt" in m for m in meldungen))
        finally:
            werkzeug.schreiben_atomar = original_schreiben

        # Verifikation: Vollständiger Rollback – keine halben Agentenordner oder Shell-Reste
        self.assertFalse((proj / "AGENTS.md").exists(), "AGENTS.md muss nach Rollback entfernt sein")
        self.assertFalse((proj / ".agents").exists(), ".agents muss nach Rollback entfernt sein")
        self.assertFalse((proj / ".claude").exists(), ".claude muss nach Rollback entfernt sein")
        self.assertFalse(shell_target.exists(), "glide_shell muss nach Rollback entfernt sein")

    def test_agenten_bootstrap_pruefen_konsistenz(self):
        """Prüft --pruefen zusammen mit --agenten-bootstrap und den genauen Statuswerten."""
        lauf("--agenten-bootstrap", self.projekt)
        code, text = lauf("--pruefen", "--agenten-bootstrap", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertIn("Agenten-Bootstrap", text)
        self.assertIn("AGENTS.md: korrekt verwaltet", text)
        self.assertIn(".agents/skills/glide-shell/SKILL.md: korrekt verwaltet", text)

        # Gültig angepasste Datei wird als "gültig angepasst" und Exitcode 0 akzeptiert
        skill_file = self.projekt / ".agents" / "skills" / "glide-shell" / "SKILL.md"
        custom_skill = (
            "---\n"
            "name: glide-shell\n"
            "description: Eigene angepasste Skill-Beschreibung.\n"
            "---\n\n"
            "# Angepasster Skill\n"
            f"- Anleitung: [KI_ANLEITUNG_NEUE_PROJEKTE.md]({werkzeug._rel_url(self.kopie / 'KI_ANLEITUNG_NEUE_PROJEKTE.md', skill_file.parent)})\n"
            "Nutzung von glide_shell im Projekt.\n"
        )
        skill_file.write_text(custom_skill, encoding="utf-8")
        code, text = lauf("--pruefen", "--agenten-bootstrap", self.projekt)
        self.assertEqual(code, 0, text)
        self.assertIn(".agents/skills/glide-shell/SKILL.md: gültig angepasst", text)

        # Beschädigtes YAML-Frontmatter wird als "beschädigt" erkannt (Exitcode 1)
        skill_file.write_text("# Kein Frontmatter\nNutzung von glide_shell.\n", encoding="utf-8")
        code, text = lauf("--pruefen", "--agenten-bootstrap", self.projekt)
        self.assertEqual(code, 1, text)
        self.assertIn(".agents/skills/glide-shell/SKILL.md: beschädigt", text)

        # Toter Dokumentlink wird als "veraltet" erkannt (Exitcode 1)
        skill_file.write_text(
            "---\nname: glide-shell\ndescription: Test.\n---\n[Toter Link](nicht_vorhanden.md)\nglide_shell.\n",
            encoding="utf-8"
        )
        code, text = lauf("--pruefen", "--agenten-bootstrap", self.projekt)
        self.assertEqual(code, 1, text)
        self.assertIn(".agents/skills/glide-shell/SKILL.md: veraltet", text)

        # Löschen von AGENTS.md macht --pruefen rot ("nicht vorhanden")
        (self.projekt / "AGENTS.md").unlink()
        code, text = lauf("--pruefen", "--agenten-bootstrap", self.projekt)
        self.assertEqual(code, 1, text)
        self.assertIn("AGENTS.md: nicht vorhanden", text)

    def test_fehlinjektion_zehn_szenarien_und_rollback_verifikation(self):
        """Simuliert die geforderten 10 Fehlerzustände und beweist vollständige oder erkannte Rollbacks."""
        # 1. Fehler beim Schreiben der ersten Agentendatei (AGENTS.md)
        ziel_1 = self.projekt / "sub1"
        ziel_1.mkdir(parents=True)
        orig_schreiben = werkzeug.schreiben_atomar
        def fail_agents(z, c):
            if z.name == "AGENTS.md":
                raise IOError("Fehler 1: AGENTS.md blockiert")
            return orig_schreiben(z, c)
        try:
            werkzeug.schreiben_atomar = fail_agents
            code, msgs = werkzeug.uebernehmen(ziel_1 / "glide_shell", agenten_bootstrap=True, ersetzen=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback ausgeführt" in m for m in msgs))
            self.assertFalse((ziel_1 / "AGENTS.md").exists())
            self.assertFalse((ziel_1 / ".agents").exists())
        finally:
            werkzeug.schreiben_atomar = orig_schreiben

        # 2. Fehler beim Schreiben des zweiten Skills (.claude/skills/.../SKILL.md)
        ziel_2 = self.projekt / "sub2"
        ziel_2.mkdir(parents=True)
        def fail_claude(z, c):
            if ".claude" in str(z):
                raise IOError("Fehler 2: Claude-Skill blockiert")
            return orig_schreiben(z, c)
        try:
            werkzeug.schreiben_atomar = fail_claude
            code, msgs = werkzeug.uebernehmen(ziel_2 / "glide_shell", agenten_bootstrap=True, ersetzen=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback ausgeführt" in m for m in msgs))
            self.assertFalse((ziel_2 / "AGENTS.md").exists())
            self.assertFalse((ziel_2 / ".agents").exists())
            self.assertFalse((ziel_2 / ".claude").exists())
        finally:
            werkzeug.schreiben_atomar = orig_schreiben

        # 3. Fehler während Snapshot-Erstellung (mit agenten_bootstrap)
        ziel_3 = self.projekt / "sub3"
        ziel_3.mkdir(parents=True)
        orig_copy2 = shutil.copy2
        def fail_copy(s, d, **kw):
            raise OSError("Fehler 3: Snapshot Lesefehler")
        try:
            werkzeug.uebernehmen(ziel_3 / "glide_shell", agenten_bootstrap=True)
            shutil.copy2 = fail_copy
            code, msgs = werkzeug.uebernehmen(ziel_3 / "glide_shell", agenten_bootstrap=True, ersetzen=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Sicherung fehlgeschlagen" in m for m in msgs))
        finally:
            shutil.copy2 = orig_copy2

        # 4. Fehler mitten während der Shell-Kopie (nach 5 Dateien)
        ziel_4 = self.projekt / "sub4"
        ziel_4.mkdir(parents=True)
        counts = [0]
        def fail_mid_copy(z, c):
            counts[0] += 1
            if counts[0] >= 5 and z.name.endswith(".py"):
                raise OSError("Fehler 4: Plattenabbruch mitten im Shell-Kopieren")
            return orig_schreiben(z, c)
        try:
            werkzeug.schreiben_atomar = fail_mid_copy
            code, msgs = werkzeug.uebernehmen(ziel_4 / "glide_shell", agenten_bootstrap=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback ausgeführt" in m for m in msgs))
            self.assertFalse((ziel_4 / "glide_shell").exists())
        finally:
            werkzeug.schreiben_atomar = orig_schreiben

        # 5. Fehler beim Zurückschreiben einer gesicherten Datei -> unvollständiger Rollback gemeldet!
        ziel_5 = self.projekt / "sub5"
        ziel_5.mkdir(parents=True)
        werkzeug.uebernehmen(ziel_5 / "glide_shell")
        phase = [0]
        def fail_rollback_restore(s, d, **kw):
            if phase[0] == 2 and str(ziel_5) in str(d):
                raise OSError("Fehler 5: Wiederherstellung im Rollback blockiert")
            return orig_copy2(s, d, **kw)
        try:
            def fail_both(z, c):
                phase[0] = 2  # Mutation abgebrochen, Rollback beginnt
                raise IOError("Kopierabbruch")
            werkzeug.schreiben_atomar = fail_both
            shutil.copy2 = fail_rollback_restore
            code, msgs = werkzeug.uebernehmen(ziel_5 / "glide_shell", ersetzen=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback unvollständig" in m for m in msgs), f"Unerwartete Meldung: {msgs}")
            self.assertFalse(any("Rollback ausgeführt (Zustand vollständig wiederhergestellt)" in m for m in msgs))
        finally:
            werkzeug.schreiben_atomar = orig_schreiben
            shutil.copy2 = orig_copy2

        # 6. Fehler beim Entfernen neu angelegter Dateien während Rollback -> Rollback unvollständig!
        ziel_6 = self.projekt / "sub6"
        ziel_6.mkdir(parents=True)
        werkzeug.uebernehmen(ziel_6 / "glide_shell")
        orig_unlink = pathlib.Path.unlink
        phase_6 = [0]
        def fail_unlink(p, missing_ok=False):
            if phase_6[0] == 2 and p.name == "extra_temp.py":
                raise OSError("Fehler 6: Unlink blockiert")
            return orig_unlink(p, missing_ok=missing_ok)
        try:
            def fail_write(z, c):
                (ziel_6 / "glide_shell" / "extra_temp.py").write_text("# neu\n", encoding="utf-8")
                phase_6[0] = 2
                raise IOError("Abbruch")
            werkzeug.schreiben_atomar = fail_write
            pathlib.Path.unlink = fail_unlink
            code, msgs = werkzeug.uebernehmen(ziel_6 / "glide_shell", ersetzen=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback unvollständig" in m for m in msgs))
        finally:
            werkzeug.schreiben_atomar = orig_schreiben
            pathlib.Path.unlink = orig_unlink

        # 7. Fehler beim Aufräumen erstellter Ordner
        tx = werkzeug.BootstrapTransaction(self.projekt, self.projekt / "glide_shell")
        tx.dirs_created = [self.projekt / ".nonexistent_dir_dummy"]
        errors = tx.rollback()
        self.assertIsInstance(errors, list)

        # 8. Unzulässige Zugriffsrechte / Verzeichnis als Zieldatei
        ziel_8 = self.projekt / "sub8"
        ziel_8.mkdir(parents=True)
        (ziel_8 / "AGENTS.md").mkdir()
        code, msgs = werkzeug.uebernehmen(ziel_8 / "glide_shell", agenten_bootstrap=True)
        self.assertEqual(code, werkzeug.VERWEIGERT)
        self.assertTrue(any("Verzeichnis (Dateityp unzulässig)" in m for m in msgs))

        # 9. Unterbrochene Dateisystemoperation: Broken replace in schreiben_atomar
        ziel_9 = self.projekt / "sub9"
        ziel_9.mkdir(parents=True)
        orig_replace = os.replace
        def fail_replace(src, dst):
            raise OSError("Fehler 9: Dateisystemunterbrechung bei os.replace")
        try:
            os.replace = fail_replace
            code, msgs = werkzeug.uebernehmen(ziel_9 / "glide_shell")
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback ausgeführt" in m for m in msgs))
        finally:
            os.replace = orig_replace

        # 10. Teilweise beschädigte Sicherung (Integritätsprüfung erkennt Hash-Mismatch nach Rollback)
        ziel_10 = self.projekt / "sub10"
        ziel_10.mkdir(parents=True)
        werkzeug.uebernehmen(ziel_10 / "glide_shell")
        phase_10 = [1]
        def corrupt_copy2(s, d, **kw):
            orig_copy2(s, d, **kw)
            if phase_10[0] == 2 and pathlib.Path(d).name == "motion.py":
                pathlib.Path(d).write_bytes(b"corrupt payload")
        try:
            shutil.copy2 = corrupt_copy2
            def fail_mutation(z, c):
                if z.name == "selftest.py":
                    phase_10[0] = 2
                    raise IOError("Abbruch")
                return orig_schreiben(z, c)
            werkzeug.schreiben_atomar = fail_mutation
            code, msgs = werkzeug.uebernehmen(ziel_10 / "glide_shell", ersetzen=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback unvollständig" in m for m in msgs))
            self.assertTrue(any("weicht nach Wiederherstellung ab" in m for m in msgs))
        finally:
            shutil.copy2 = orig_copy2
            werkzeug.schreiben_atomar = orig_schreiben

    def test_symlink_und_pfad_schutz_im_bootstrap(self):
        """Verifiziert Symlink-Schutz und Pfadtraversierungsabwehr im Agenten-Bootstrap."""
        sub = self.projekt / "symlink_safety_test"
        sub.mkdir(parents=True)
        agents_target = sub / "AGENTS.md"

        # 1. Externer Symlink auf Datei außerhalb des Projekts muss vor Mutation abgewiesen werden
        outside_file = self.projekt / "outside_secret.txt"
        outside_file.write_text("sensibler Inhalt", encoding="utf-8")
        try:
            agents_target.symlink_to(outside_file)
        except OSError:
            self.skipTest("Symlinks auf diesem Dateisystem nicht unterstützt")

        code, msgs = werkzeug.uebernehmen(sub / "glide_shell", agenten_bootstrap=True)
        self.assertEqual(code, werkzeug.VERWEIGERT)
        self.assertTrue(any("externes Ziel außerhalb des Projekts" in m for m in msgs))
        self.assertEqual(outside_file.read_text(encoding="utf-8"), "sensibler Inhalt")

        # 2. Interner Symlink auf projektinterne Datei
        internal_file = sub / "my_custom_agents.md"
        internal_file.write_text("# Interne Vorlage\n", encoding="utf-8")
        agents_target.unlink()
        agents_target.symlink_to(internal_file.name)

        # 2a. Ohne --ersetzen: Vorhandener interner Symlink bleibt unberührt
        code, msgs = werkzeug.uebernehmen(sub / "glide_shell", agenten_bootstrap=True, ersetzen=False)
        self.assertEqual(code, 0)
        self.assertTrue(agents_target.is_symlink())
        self.assertEqual(os.readlink(agents_target), internal_file.name)
        self.assertEqual(internal_file.read_text(encoding="utf-8"), "# Interne Vorlage\n")

        # 2b. Mit --ersetzen: Symlink wird ersetzt
        code, msgs = werkzeug.uebernehmen(sub / "glide_shell", agenten_bootstrap=True, ersetzen=True)
        self.assertEqual(code, 0)
        self.assertFalse(agents_target.is_symlink())
        self.assertTrue(agents_target.is_file())
        self.assertIn("Glide Shell", agents_target.read_text(encoding="utf-8"))
        self.assertEqual(internal_file.read_text(encoding="utf-8"), "# Interne Vorlage\n")

        # 2c. Rollback stellt bestehenden internen Symlink wieder her
        agents_target.unlink()
        agents_target.symlink_to(internal_file.name)
        orig_schreiben = werkzeug.schreiben_atomar
        phase_sym = [1]
        def fail_at_skill(z, c):
            if phase_sym[0] == 1 and ".claude" in str(z):
                phase_sym[0] = 2  # Ab jetzt darf Rollback wieder ungestört schreiben
                raise IOError("Abbruch")
            return orig_schreiben(z, c)
        try:
            werkzeug.schreiben_atomar = fail_at_skill
            code, msgs = werkzeug.uebernehmen(sub / "glide_shell", agenten_bootstrap=True, ersetzen=True)
            self.assertEqual(code, werkzeug.ABWEICHUNG)
            self.assertTrue(any("Rollback ausgeführt" in m for m in msgs))
            self.assertTrue(agents_target.is_symlink(), "Symlink muss nach Rollback wieder ein Symlink sein")
            self.assertEqual(os.readlink(agents_target), internal_file.name)
        finally:
            werkzeug.schreiben_atomar = orig_schreiben

    def test_pfade_mit_leerzeichen_klammern_und_unicode(self):
        """Prüft Projektpfade mit Leerzeichen, Klammern und Unicode wie 'Mein Projekt 2026/Haupt App (v2)'."""
        complex_proj = pathlib.Path(self._temp.name) / "Mein Projekt 2026" / "Haupt App (v2)"
        complex_proj.mkdir(parents=True)
        (complex_proj / "pyproject.toml").write_text("[project]\nname='complex'\n", encoding="utf-8")

        code, text = lauf("--agenten-bootstrap", complex_proj)
        self.assertEqual(code, 0, text)

        agents_md = complex_proj / "AGENTS.md"
        self.assertTrue(agents_md.is_file())
        inhalt = agents_md.read_text(encoding="utf-8")

        self.assertIn("KI_ANLEITUNG_NEUE_PROJEKTE.md", inhalt)
        self.assertIn("python3 -m glide_shell.selftest", inhalt)

        code, text = lauf("--pruefen", "--agenten-bootstrap", complex_proj)
        self.assertEqual(code, 0, text)
        self.assertIn("AGENTS.md: korrekt verwaltet", text)


def git(ordner, *argumente):
    return subprocess.run(["git", "-C", str(ordner), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                           "-c", "commit.gpgsign=false", *argumente], capture_output=True, text=True, check=True)


class Quelle(unittest.TestCase):
    """Quellfälle in einem temporären Git-Repository mit der Struktur von Glide (Exitcode 3)."""

    def setUp(self):
        self._temp = tempfile.TemporaryDirectory(prefix="glide-shell-quelle-")
        basis = pathlib.Path(self._temp.name)
        self.repo, self.ziel = basis / "repo", basis / "ziel"
        glide = self.repo / "01_Repository" / "Glide"
        shutil.copytree(QUELLE, glide / "src" / "glide" / "glide_shell", ignore=shutil.ignore_patterns("__pycache__"))
        (glide / "scripts" / "pflege").mkdir(parents=True)
        shutil.copy2(WERKZEUG, glide / "scripts" / "pflege" / WERKZEUG.name)
        shutil.copy2(REPO / "GLIDE_SYSTEM_VERSION", glide / "GLIDE_SYSTEM_VERSION")
        shutil.copy2(REPO.parents[1] / "LICENSE", self.repo / "LICENSE")
        git(self.repo, "init", "-q")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "basis")
        self.commit = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.shell = glide / "src" / "glide" / "glide_shell"
        self.werkzeug = glide / "scripts" / "pflege" / WERKZEUG.name

    def tearDown(self):
        self._temp.cleanup()

    def aufruf(self, *argumente):
        lauf_ = subprocess.run([sys.executable, "-B", str(self.werkzeug), *map(str, argumente)], capture_output=True,
                               text=True, timeout=60)
        return lauf_.returncode, lauf_.stdout + lauf_.stderr

    def manifest(self):
        return json.loads((self.ziel / "glide_shell" / "SHELL_MANIFEST.json").read_text(encoding="utf-8"))

    def test_saubere_quelle_mit_commit_herkunft(self):
        code, text = self.aufruf(self.ziel)
        self.assertEqual(code, 0, text)
        self.assertEqual(self.manifest()["quell_commit"], self.commit)
        self.assertIs(self.manifest()["quelle_unveraendert"], True)

    def test_lokale_quellaenderung_braucht_zustimmung(self):
        datei = self.shell / "motion.py"
        datei.write_text(datei.read_text(encoding="utf-8") + "\n# lokal\n", encoding="utf-8")
        code, text = self.aufruf(self.ziel)
        self.assertEqual(code, 3, text)
        self.assertIn("lokal verändert", text)
        self.assertFalse((self.ziel / "glide_shell").exists())
        (self.shell / "unversioniert.py").write_text("x = 1\n", encoding="utf-8")
        code, text = self.aufruf(self.ziel)
        self.assertEqual(code, 3, text)
        code, text = self.aufruf("--unsauber-erlauben", self.ziel)
        self.assertEqual(code, 0, text)
        self.assertIs(self.manifest()["quelle_unveraendert"], False)
        self.assertIn("lokale Änderungen", text)

    def test_commit_pin_ist_reproduzierbar_trotz_lokaler_aenderung(self):
        init = self.shell / "__init__.py"
        init.write_text(init.read_text(encoding="utf-8").replace("SHELL_VERSION = \"", "SHELL_VERSION = \"9"), encoding="utf-8")
        (self.shell / "unversioniert.py").write_text("x = 1\n", encoding="utf-8")
        code, text = self.aufruf("--commit", self.commit[:10], self.ziel)
        self.assertEqual(code, 0, text)
        manifest = self.manifest()
        self.assertEqual(manifest["quell_commit"], self.commit)
        self.assertEqual(manifest["shell_version"], werkzeug.shell_version())
        self.assertNotIn("unversioniert.py", manifest["dateien"])
        self.assertIn("LICENSE", manifest["dateien"])
        self.assertEqual(self.aufruf("--pruefen", "--commit", self.commit, self.ziel)[0], 0)

    def test_unbekannter_commit_fehlende_und_beschaedigte_quelle(self):
        self.assertEqual(self.aufruf("--commit", "0" * 40, self.ziel)[0], 3)
        init = self.shell / "__init__.py"
        init.write_text("# ohne Version\n", encoding="utf-8")
        git(self.repo, "commit", "-qam", "kaputt")
        code, text = self.aufruf(self.ziel)
        self.assertEqual(code, 3, text)
        self.assertIn("SHELL_VERSION", text)
        (self.repo / "LICENSE").unlink()
        git(self.repo, "commit", "-qam", "ohne Lizenz")
        code, text = self.aufruf("--commit", "HEAD", self.ziel)
        self.assertEqual(code, 3, text)
        shutil.rmtree(self.shell)
        git(self.repo, "commit", "-qam", "ohne Shell")
        code, text = self.aufruf(self.ziel)
        self.assertEqual(code, 3, text)
        self.assertIn("Shell-Quelle fehlt", text)
        self.assertFalse((self.ziel / "glide_shell" / "SHELL_MANIFEST.json").exists())


if __name__ == "__main__":
    unittest.main()
