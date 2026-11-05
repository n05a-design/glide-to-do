"""Native UI-Diagnose bleibt von Vollmatrix, Kalibrierung und Paketfreigabe getrennt."""
from pathlib import Path
import unittest


SOURCE = Path(__file__).resolve().parents[4] / ".github/workflows/python-app.yml"


class UINachlaufWorkflow(unittest.TestCase):
    def test_manual_ui_has_separate_concurrency_and_full_ui_reports_on_both_platforms(self):
        text = SOURCE.read_text(encoding="utf-8")
        self.assertIn("options: [voll, ui-nachlauf,", text)
        self.assertIn("github.event.inputs.bereich || 'voll'", text)
        self.assertEqual(text.count("- name: Arbeitsmodi vollständig nativ prüfen"), 2)
        self.assertEqual(text.count("tests/integration/test_arbeitsmodi.py --fall alle --report"), 2)
        self.assertIn('dbus-run-session -- xvfb-run -a --server-args="-screen 0 1400x1100x24" python -B tests/integration/test_arbeitsmodi.py', text)
        self.assertEqual(text.count("- name: UI-/UX-Verträge vollständig nativ prüfen"), 2)
        self.assertEqual(text.count("tests/integration/test_uiux_paket.py --fall alle --report"), 2)
        for job in ("  integrationssuiten-linux:", "  vollpruefung-windows:"):
            section = text.split(job, 1)[1].split("      - name: Kalibrierte", 1)[0]
            self.assertLess(section.index("UI-/UX-Verträge vollständig nativ prüfen"),
                            section.index("Arbeitsmodi vollständig nativ prüfen"))

    def test_full_modes_and_positive_calibration_gate_are_preserved(self):
        text = SOURCE.read_text(encoding="utf-8")
        for name in ("Vollprüfstand Linux", "Vollprüfstand Windows"):
            self.assertIn(f"- name: {name}\n        if: github.event.inputs.bereich != 'ui-nachlauf'", text)
        self.assertEqual(text.count("tests/tools/pruefen.py --zugang-nativ --modus voll"), 2)
        calibration = text.split("- name: Kalibrierte Erwartungen gegen Defekte prüfen", 1)[1].split("- name:", 1)[0]
        self.assertIn("github.event.inputs.bereich != 'ui-nachlauf'", calibration)
        self.assertIn('--basis-ergebnis "$RUNNER_TEMP/integration/ergebnis.json"', calibration)
        package = text.split("  paket-windows:", 1)[1].split("    runs-on:", 1)[0]
        self.assertIn("needs.vollpruefung-windows.result == 'success' && github.event.inputs.bereich != 'ui-nachlauf'", package)


if __name__ == "__main__":
    unittest.main()
