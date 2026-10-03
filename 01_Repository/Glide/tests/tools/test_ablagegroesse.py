"""Regeln der Ablagegröße; ohne Git, ohne App-Import, ohne Nutzerdaten."""

import unittest

import ablagegroesse as ablage

Q = ablage.QUELLBAUM
MB = 1024 * 1024


def regeln(*eintraege, aktuell=None):
    return [(regel, pfad) for regel, pfad, _ in ablage.befunde(eintraege, aktuell)]


def nachweis(version, datei="README.md"):
    return Q + f"tests/qa-{version}/lauf_2026-10-03/{datei}"


def releaseplanung(version):
    return Q + f"tests/fixtures/beispiele/glide_releaseplanung_{version}.glidebackup"


def archivdatei(version):
    return f"07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v{version}.pyw"


class Ablagegroesse(unittest.TestCase):
    def test_archive_copies_of_data_files_are_rejected(self):
        for pfad in (Q + "tests/fixtures/showcase/archiv/Glide-Showcase_App_3.33.6_vor_3.33.7.glideapp",
                     Q + "tests/fixtures/beispiele/archiv/glide_rundgang_3.33.6_vor_3.33.7.glidebackup",
                     "05_Probelisten_Testdaten/Showcase/archiv/Glide-Showcase_vor_Abgleich_2026-10-03.glidetemplates",
                     "05_Probelisten_Testdaten/Showcase/Archiv/Glide-Showcase.glidebackup"):
            with self.subTest(pfad=pfad):
                self.assertEqual(regeln((pfad, 2 * MB)), [("Archivkopie", pfad)])

    def test_current_data_files_stay_allowed(self):
        erlaubt = [(Q + "tests/fixtures/showcase/Glide-Showcase_App.glideapp", 36 * MB),
                   ("05_Probelisten_Testdaten/Showcase/Glide-Showcase.glidebackup", 31 * MB),
                   (Q + "tests/fixtures/beispiele/glide_beispieldaten.glidebackup", MB),
                   ("05_Probelisten_Testdaten/Showcase/archiv/README_3.33.0_vor_3.33.1.md", 4096)]
        self.assertEqual(regeln(*erlaubt, aktuell="3.33.6"), [])

    def test_archives_and_evidence_keep_only_the_seven_newest_versions(self):
        versionen = [f"3.33.{n}" for n in range(8)]          # 3.33.0 … 3.33.7
        eintraege = [(nachweis(v), 4096) for v in versionen]
        eintraege += [(releaseplanung(v), MB) for v in versionen]
        eintraege += [(archivdatei(v), MB) for v in versionen[:-1]]
        funde = regeln(*eintraege, aktuell="3.33.7")
        self.assertEqual(sorted(funde), sorted([("Archivalter", nachweis("3.33.0")),
                                                ("Archivalter", releaseplanung("3.33.0")),
                                                ("Archivalter", archivdatei("3.33.0"))]))

    def test_current_version_counts_before_anything_exists_for_it(self):
        eintraege = [(nachweis(f"3.33.{n}"), 4096) for n in range(7)]   # 3.33.0 … 3.33.6
        self.assertEqual(regeln(*eintraege, aktuell="3.33.6"), [])
        self.assertEqual(regeln(*eintraege, aktuell="3.33.7"), [("Archivalter", nachweis("3.33.0"))])

    def test_format_evidence_and_tempo_fixture_stay_outside_the_window(self):
        eintraege = [(pfad, MB) for pfad in sorted(ablage.DAUERHAFT)]
        eintraege.append((releaseplanung("3.22.0"), MB))
        eintraege += [(releaseplanung(f"3.33.{n}"), MB) for n in range(7)]
        self.assertIn(releaseplanung("3.30.0"), ablage.DAUERHAFT)
        self.assertEqual(regeln(*eintraege, aktuell="3.33.6"), [("Archivalter", releaseplanung("3.22.0"))])

    def test_fetch_remnants_are_rejected(self):
        pfad = Q + "tests/fixtures/showcase/Glide-Showcase_App.glideapp.fetch"
        self.assertIn(("Fehlrest", pfad), regeln((pfad, 36 * MB)))

    def test_window_screenshots_after_3_33_6_are_rejected(self):
        neu = Q + "tests/qa-3.33.7/heute_2026-10-03/vollpruefung/fenster/01_start.png"
        spaeter = Q + "tests/qa-3.33.8/x/vollpruefung_2/fenster/sub/02.png"
        self.assertEqual(regeln((neu, MB), (spaeter, MB), aktuell="3.33.8"),
                         [("Fensterbilder", neu), ("Fensterbilder", spaeter)])

    def test_window_screenshots_only_in_the_three_newest_versions(self):
        bilder = [(nachweis(f"3.33.{n}", "vollpruefung/fenster/01.png"), MB) for n in range(4, 7)]
        self.assertEqual(regeln(*bilder, aktuell="3.33.6"), [])
        self.assertEqual(regeln(*bilder, aktuell="3.33.7"),
                         [("Fensterbilder", nachweis("3.33.4", "vollpruefung/fenster/01.png"))])

    def test_other_evidence_stays_allowed(self):
        erlaubt = [(Q + "tests/qa-3.33.6/heute_2026-10-02/vollpruefung/fenster/01_start.png", MB),
                   (Q + "tests/qa-3.33.6/heute_2026-10-02/vollpruefung/ergebnis.json", 4096),
                   (Q + "tests/qa-3.33.6/ansicht_2026-10-03/ansichten/startseite.png", MB),
                   (Q + "tests/qa-3.33.6/x/fenster.png", MB)]
        self.assertEqual(regeln(*erlaubt, aktuell="3.33.6"), [])

    def test_files_above_github_warning_limit_are_rejected(self):
        pfad = "20_Grafik_Master/riesig.psd"
        self.assertEqual(regeln((pfad, 51 * MB)), [("Dateigröße", pfad)])
        self.assertEqual(regeln((pfad, 50 * MB)), [])

    def test_summary_names_rules_totals_and_remedy(self):
        eintraege = [("a.fetch", MB), ("b.md", MB)]
        eintraege += [(nachweis(f"3.33.{n}"), MB) for n in range(8)]
        text = ablage.zusammenfassung(eintraege, ablage.befunde(eintraege, "3.33.7"))
        self.assertIn("10 versionierte Dateien, 10 MB", text)
        self.assertIn("Fehlrest", text)
        self.assertIn("Archivalter", text)
        self.assertIn("ablage_kuerzen.py", text)


if __name__ == "__main__":
    unittest.main()
