# SPDX-License-Identifier: MPL-2.0
"""Prüft die inhaltliche und technische Konsistenz des portablen Designvertrags (T339).

Stellt sicher, dass:
1. Der portable Designvertrag in `src/glide/glide_shell/DESIGN_RICHTLINIEN.md` und
   der entsprechende Abschnitt in `docs/DESIGN_RICHTLINIEN.md` synchron und
   inhaltlich konsistent sind.
2. Alle Grundsätze (P1–P6), Einzelvorgaben (B15, B11, B01/B16, B03, B10/B12/B14,
   Kontrast, Fokus/Tastatur), Schnittstellen und Produktschranken übereinstimmen.
3. Die Stand-Zeilen den aktuellen Versionierungsregeln (R1, Glide 1.0.1,
   Shell 0.6.2, MPL-2.0) genügen.
4. Negative Proben beweisen, dass fehlende Regeln, widersprüchliche Inhalte,
   veränderte Kontrastwerte, fehlende Schnittstellen oder Markenvermischung
   zuverlässig zum Prüffehler führen.
"""
import pathlib
import re
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
VERSION = (REPO / "VERSION").read_text(encoding="utf-8").strip()
DOCS_DESIGN = REPO / "docs" / "DESIGN_RICHTLINIEN.md"
SHELL_DESIGN = REPO / "src" / "glide" / "glide_shell" / "DESIGN_RICHTLINIEN.md"


def pruefe_designvertrag_inhaltlich(shell_text, docs_text):
    """Validiert die inhaltliche und semantische Konsistenz des portablen Designvertrags.

    Gibt eine Liste von Fehlern zurück (leer bei vollständiger Konsistenz).
    """
    fehler = []

    # 1. P1 bis P6 Grundsätze
    prinzipien = {
        "P1": ("Funktioniert selbstverständlich", "Systemkonventionen"),
        "P2": ("Form folgt Funktion", "Visuelle Hierarchie"),
        "P3": ("Keine Funktion doppelt", "primärer"),
        "P4": ("Kein Platz verschwenden", "Inhalt"),
        "P5": ("Nur das Wesentliche", "Standard"),
        "P6": ("Geringe Komplexität", "stabile"),
    }
    for p_id, (titel_teil, bedeutung_teil) in prinzipien.items():
        if p_id not in shell_text:
            fehler.append(f"Grundsatz {p_id} fehlt im Shell-Designvertrag")
        elif titel_teil.lower() not in shell_text.lower():
            fehler.append(f"Grundsatz {p_id} Titel '{titel_teil}' fehlt im Shell-Designvertrag")

        if p_id not in docs_text:
            fehler.append(f"Grundsatz {p_id} fehlt in Haupt-Designrichtlinien")

    # 2. Einzelvorgaben (B15, B11, B01/B16, B03, B10/B12/B14, Kontrast, Fokus)
    # B15: Buttonschutz, Sichtbarkeit, keine Überdeckung, clamp
    if "B15" not in shell_text or "Knopf" not in shell_text and "Button" not in shell_text:
        fehler.append("B15 (Buttonschutz) fehlt oder ist unvollständig im Shell-Designvertrag")
    if "clamp" not in shell_text:
        fehler.append("B15 Mindestgrößen-Absicherung via window_geometry.clamp fehlt im Shell-Designvertrag")

    # B11: Informationshierarchie vor Metadatenbreite, Messung auf Inhalt, text_fit
    if "B11" not in shell_text:
        fehler.append("B11 (Informationshierarchie) fehlt im Shell-Designvertrag")
    if "text_fit" not in shell_text:
        fehler.append("B11 Schnittstelle text_fit fehlt im Shell-Designvertrag")

    # B01 / B16: Unmittelbare Rückmeldung, keine blockierenden Schlafzeiten
    if "B01" not in shell_text or "B16" not in shell_text:
        fehler.append("B01/B16 (Rückmeldung) fehlt im Shell-Designvertrag")
    if "time.sleep" not in shell_text and "schlaf" not in shell_text.lower():
        fehler.append("B01/B16 Ausschluss blockierender Schlafzeiten fehlt im Shell-Designvertrag")

    # B03: Bewegung <= 150 ms, motion.Transitions
    if "B03" not in shell_text:
        fehler.append("B03 (Ergonomische Bewegung) fehlt im Shell-Designvertrag")
    if "150" not in shell_text or "Transitions" not in shell_text:
        fehler.append("B03 Begrenzung auf 150 ms oder Transitions fehlt im Shell-Designvertrag")

    # B10 / B12 / B14: Semantische Symbole (Dreiecke zum Blättern/Klappen)
    if not all(k in shell_text for k in ("B10", "B12", "B14")):
        fehler.append("B10/B12/B14 Symbolregeln fehlen im Shell-Designvertrag")
    if "◂" not in shell_text and "▸" not in shell_text:
        fehler.append("Semantische Symbolglyphen ◂/▸ fehlen im Shell-Designvertrag")

    # Kontrast: WCAG 2.2 AA (4,5:1 Text, 3:1 Groß/UI)
    if "4,5:1" not in shell_text and "4.5:1" not in shell_text:
        fehler.append("Mindestkontrast 4,5:1 für Text fehlt im Shell-Designvertrag")
    if "3:1" not in shell_text and "3.0:1" not in shell_text:
        fehler.append("Mindestkontrast 3:1 für UI/Großtext fehlt im Shell-Designvertrag")

    # Fokus & Tastatur: Tab, Shift+Tab, Escape
    if "Tab" not in shell_text or "Escape" not in shell_text:
        fehler.append("Fokus- und Tastaturregeln (Tab, Escape) fehlen im Shell-Designvertrag")

    # 3. Technische Shell-Schnittstellen
    schnittstellen = [
        "set_font_provider",
        "set_ink_provider",
        "set_backdrop_painter",
        "system_appearance.resolve",
        "primary_shortcuts",
        "bind_shortcuts",
        "install_close",
        "create_dialog",
        "run_modal",
        "Transitions",
        "CommandHistory",
        "clamp",
        "format_geometry",
    ]
    for iface in schnittstellen:
        if iface not in shell_text:
            fehler.append(f"Verbindliche Shell-Schnittstelle '{iface}' fehlt im Shell-Designvertrag")
        if iface not in docs_text:
            fehler.append(f"Verbindliche Shell-Schnittstelle '{iface}' fehlt in Haupt-Designrichtlinien")

    # 4. Produktschranken & Trennung von Markenidentität
    # Markenregeln (wie Gismo, Glides spezifische Farbe #9E4AC8) gehören in Abschnitt 4 (Host-Freiheit),
    # dürfen aber keinesfalls als universelle Shell-Regel in Abschnitt 1 oder 2 gefordert werden.
    abschnitt_1_2 = shell_text.split("## 4.")[0] if "## 4." in shell_text else shell_text
    if "Gismo" in abschnitt_1_2:
        fehler.append("Produktmaskottchen 'Gismo' unzulässig als universelle Shell-Regel deklariert")
    if "#9E4AC8" in abschnitt_1_2:
        fehler.append("Glide-Markenfarbe '#9E4AC8' unzulässig als universelle Shell-Regel deklariert")

    # Abschnitt 4 muss die Domänenfreiheit des Hosts garantieren
    if "## 4." not in shell_text or "Markenidentität" not in shell_text:
        fehler.append("Abschnitt 4 (Gestaltungsfreiheit des Hosts) fehlt oder ist unvollständig")

    return fehler


class TestDesignVertragKonsistenz(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs_text = DOCS_DESIGN.read_text(encoding="utf-8")
        cls.shell_text = SHELL_DESIGN.read_text(encoding="utf-8")

    def test_both_files_exist(self):
        self.assertTrue(DOCS_DESIGN.is_file(), f"{DOCS_DESIGN} fehlt")
        self.assertTrue(SHELL_DESIGN.is_file(), f"{SHELL_DESIGN} fehlt")

    def test_shell_design_stand_and_license(self):
        lines = self.shell_text.splitlines()
        self.assertGreaterEqual(len(lines), 3)
        self.assertIn("Portabler Designvertrag", lines[0])
        stand_line = lines[2]
        self.assertTrue(stand_line.startswith("Stand "))
        self.assertIn(f"Glide {VERSION}", stand_line)
        shell = (REPO / "src" / "glide" / "glide_shell" / "__init__.py").read_text(encoding="utf-8")
        version = shell.split('SHELL_VERSION = "', 1)[1].split('"', 1)[0]
        self.assertIn(f"Glide Shell {version}", stand_line)
        self.assertIn("MPL-2.0", stand_line)

    def test_substantive_design_contract_consistency(self):
        fehler = pruefe_designvertrag_inhaltlich(self.shell_text, self.docs_text)
        self.assertEqual(fehler, [], f"Inhaltliche Konsistenzfehler im Designvertrag:\n" + "\n".join(fehler))

    # --- Negativ-Tests für den Nachweis robuster Prüfungen ---

    def test_negative_fehlende_regel_wird_erkannt(self):
        mutated_shell = self.shell_text.replace("### B15", "### X15")
        fehler = pruefe_designvertrag_inhaltlich(mutated_shell, self.docs_text)
        self.assertTrue(any("B15" in f for f in fehler), f"Fehlendes B15 wurde nicht erkannt: {fehler}")

    def test_negative_widerspruechlicher_inhalt_wird_erkannt(self):
        # Entferne die Schutzvorgabe via clamp vollständig
        mutated_shell = self.shell_text.replace("clamp", "unlimited")
        fehler = pruefe_designvertrag_inhaltlich(mutated_shell, self.docs_text)
        self.assertTrue(any("clamp" in f for f in fehler), f"Entferntes clamp wurde nicht erkannt: {fehler}")

    def test_negative_veraenderte_mindestkontraste_wird_erkannt(self):
        mutated_shell = self.shell_text.replace("4,5:1", "2,0:1").replace("4.5:1", "2.0:1")
        fehler = pruefe_designvertrag_inhaltlich(mutated_shell, self.docs_text)
        self.assertTrue(any("Mindestkontrast 4,5:1" in f for f in fehler), f"Veränderter Kontrast wurde nicht erkannt: {fehler}")

    def test_negative_entfernte_schnittstelle_wird_erkannt(self):
        mutated_shell = self.shell_text.replace("create_dialog", "create_window_generic")
        fehler = pruefe_designvertrag_inhaltlich(mutated_shell, self.docs_text)
        self.assertTrue(any("create_dialog" in f for f in fehler), f"Entferntes create_dialog wurde nicht erkannt: {fehler}")

    def test_negative_markenregel_als_universell_wird_erkannt(self):
        # Füge Gismo fälschlich in Abschnitt 1 ein
        mutated_shell = "Gismo muss immer sichtbar sein.\n" + self.shell_text
        fehler = pruefe_designvertrag_inhaltlich(mutated_shell, self.docs_text)
        self.assertTrue(any("Gismo" in f for f in fehler), f"Unzulässiges Gismo in universeller Regel wurde nicht erkannt: {fehler}")

    def test_negative_fehlende_universelle_regel_in_docs_wird_erkannt(self):
        mutated_docs = re.sub(r"\bP3\b", "PX", self.docs_text)
        fehler = pruefe_designvertrag_inhaltlich(self.shell_text, mutated_docs)
        self.assertTrue(any("P3" in f for f in fehler), f"Fehlendes P3 in Docs wurde nicht erkannt: {fehler}")


if __name__ == "__main__":
    unittest.main()
