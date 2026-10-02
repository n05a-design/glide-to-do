"""Regeln der Ablagegröße; ohne Git, ohne App-Import, ohne Nutzerdaten."""

import unittest

import ablagegroesse as ablage

Q = ablage.QUELLBAUM
MB = 1024 * 1024


def regeln(*eintraege):
    return [(regel, pfad) for regel, pfad, _ in ablage.befunde(eintraege)]


class Ablagegroesse(unittest.TestCase):
    def test_archive_copies_of_data_files_are_rejected(self):
        for pfad in (Q + "tests/fixtures/showcase/archiv/Glide-Showcase_App_3.33.6_vor_3.33.7.glideapp",
                     Q + "tests/fixtures/beispiele/archiv/glide_rundgang_3.33.6_vor_3.33.7.glidebackup",
                     "05_Probelisten_Testdaten/Showcase/archiv/Glide-Showcase_vor_Abgleich_2026-10-03.glidetemplates",
                     "05_Probelisten_Testdaten/Showcase/Archiv/Glide-Showcase.glidebackup"):
            with self.subTest(pfad=pfad):
                self.assertEqual(regeln((pfad, 2 * MB)), [("Archivkopie", pfad)])

    def test_current_data_files_and_documented_original_stay_allowed(self):
        erlaubt = [(Q + "tests/fixtures/showcase/Glide-Showcase_App.glideapp", 36 * MB),
                   ("05_Probelisten_Testdaten/Showcase/Glide-Showcase.glidebackup", 31 * MB),
                   (Q + "tests/fixtures/beispiele/glide_releaseplanung_3.5.0.glidebackup", MB),
                   ("05_Probelisten_Testdaten/Showcase/archiv/README_3.33.0_vor_3.33.1.md", 4096),
                   ("05_Probelisten_Testdaten/Archiv/Glide-Funktionsvorschau_3.30.0.glidebackup", MB),
                   *((pfad, 24 * 1024) for pfad in ablage.ERLAUBTE_ARCHIVDATEIEN)]
        self.assertEqual(regeln(*erlaubt), [])

    def test_fetch_remnants_are_rejected(self):
        pfad = Q + "tests/fixtures/showcase/Glide-Showcase_App.glideapp.fetch"
        self.assertIn(("Fehlrest", pfad), regeln((pfad, 36 * MB)))

    def test_window_screenshots_after_3_33_6_are_rejected(self):
        neu = Q + "tests/qa-3.33.7/heute_2026-10-03/vollpruefung/fenster/01_start.png"
        spaeter = Q + "tests/qa-3.40.0/x/vollpruefung_2/fenster/sub/02.png"
        self.assertEqual(regeln((neu, MB), (spaeter, MB)), [("Fensterbilder", neu), ("Fensterbilder", spaeter)])

    def test_existing_screenshots_and_other_evidence_stay_allowed(self):
        erlaubt = [(Q + "tests/qa-3.33.6/heute_2026-10-02/vollpruefung/fenster/01_start.png", MB),
                   (Q + "tests/qa-3.30.0/rueckmeldung_abend_2026-09-29/fenster/a.png", MB),
                   (Q + "tests/qa-3.33.7/heute_2026-10-03/vollpruefung/ergebnis.json", 4096),
                   (Q + "tests/qa-3.33.7/ansicht_2026-10-03/ansichten/startseite.png", MB),
                   (Q + "tests/qa-3.33.7/x/fenster.png", MB)]
        self.assertEqual(regeln(*erlaubt), [])

    def test_files_above_github_warning_limit_are_rejected(self):
        pfad = "20_Grafik_Master/riesig.psd"
        self.assertEqual(regeln((pfad, 51 * MB)), [("Dateigröße", pfad)])
        self.assertEqual(regeln((pfad, 50 * MB)), [])

    def test_summary_names_rules_and_totals(self):
        eintraege = [("a.fetch", MB), ("b.md", MB)]
        text = ablage.zusammenfassung(eintraege, ablage.befunde(eintraege))
        self.assertIn("2 versionierte Dateien, 2 MB", text)
        self.assertIn("Fehlrest", text)


if __name__ == "__main__":
    unittest.main()
