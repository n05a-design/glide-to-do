"""Wächter gegen Synchronisationskopien und geschrumpfte Hauptdokumente (W04); ohne Git, ohne App."""

import unittest

import synchronisationswaechter as waechter


class Synchronisationskopien(unittest.TestCase):
    def test_conflict_copy_next_to_original_is_found(self):
        pfade = ["00_Arbeitsvorbereitung/Glide_Uebergabe.md",
                 "00_Arbeitsvorbereitung/Glide_Uebergabe-DESKTOP-4KQ2.md",
                 "01_Repository/Glide/docs/20_FUNKTIONEN.md",
                 "01_Repository/Glide/docs/20_FUNKTIONEN-Shayes-MacBook-Pro.md"]
        funde = dict(waechter.synchronisationskopien(pfade))
        self.assertEqual(funde["00_Arbeitsvorbereitung/Glide_Uebergabe-DESKTOP-4KQ2.md"],
                         "00_Arbeitsvorbereitung/Glide_Uebergabe.md")
        # Mehrteilige Gerätenamen: Das Original heißt nur „20_FUNKTIONEN.md“.
        self.assertEqual(funde["01_Repository/Glide/docs/20_FUNKTIONEN-Shayes-MacBook-Pro.md"],
                         "01_Repository/Glide/docs/20_FUNKTIONEN.md")

    def test_wanted_variants_stay_allowed(self):
        pfade = ["src/glide/resources/fonts/DejaVuSans.ttf", "src/glide/resources/fonts/DejaVuSans-Bold.ttf",
                 "20_Grafik_Master/01_Logo/Glide-Logo.svg", "20_Grafik_Master/01_Logo/Glide-Logo-01.svg",
                 "docs/plan.md", "docs/plan-2.md", "tests/tools/pruefen.py", "tests/tools/test_pruefen.py"]
        self.assertEqual(waechter.synchronisationskopien(pfade), [])

    def test_copy_in_other_folder_is_not_a_conflict(self):
        self.assertEqual(waechter.synchronisationskopien(["a/README.md", "b/README-Laptop.md"]), [])


class GeschrumpfteDokumente(unittest.TestCase):
    ALT = "# Titel\n\nStand 07.10.2026 · Glide 3.33.17\n\n" + "Zeile\n" * 96

    def test_strong_shrink_without_note_is_found(self):
        neu = "# Titel\n\nStand 08.10.2026 · Glide 3.33.18\n\n" + "Zeile\n" * 20
        funde = waechter.geschrumpfte_dokumente([("00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md", self.ALT, neu)])
        self.assertEqual(funde, [("00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md", 100, 24)])

    def test_note_with_same_date_allows_shrink(self):
        neu = ("# Titel\n\nStand 08.10.2026 · Glide 3.33.18\n\nAm 08.10.2026 gekürzt: erledigte Abschnitte "
               "stehen im QA-Bericht.\n" + "Zeile\n" * 20)
        self.assertEqual(waechter.geschrumpfte_dokumente([("01_Repository/Glide/docs/07_QA_BERICHT.md", self.ALT, neu)]), [])

    def test_old_note_does_not_count(self):
        neu = ("# Titel\n\nStand 08.10.2026 · Glide 3.33.18\n\nAm 03.10.2026 zusammengeführt.\n" + "Zeile\n" * 20)
        self.assertEqual(len(waechter.geschrumpfte_dokumente([("01_Repository/Glide/docs/ARBEITSRICHTUNG.md", self.ALT, neu)])), 1)

    def test_moderate_change_and_other_files_pass(self):
        neu = "# Titel\n\nStand 08.10.2026 · Glide 3.33.18\n\n" + "Zeile\n" * 70
        self.assertEqual(waechter.geschrumpfte_dokumente([("01_Repository/Glide/docs/20_FUNKTIONEN.md", self.ALT, neu)]), [])
        kurz = "x\n"
        self.assertEqual(waechter.geschrumpfte_dokumente([("01_Repository/Glide/tests/qa-3.33.18/a/README.md", self.ALT, kurz)]), [])

    def test_main_documents_are_recognised(self):
        for pfad in ("00_Arbeitsvorbereitung/Glide_Uebergabe.md", "01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md",
                     "01_Repository/Glide/CHANGELOG.md", "00_Arbeitsvorbereitung/Glide_Analyse.md"):
            self.assertTrue(waechter.ist_hauptdokument(pfad), pfad)
        self.assertFalse(waechter.ist_hauptdokument("01_Repository/Glide/tests/README.md"))


if __name__ == "__main__":
    unittest.main()
