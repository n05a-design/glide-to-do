# SPDX-License-Identifier: MPL-2.0
"""Darstellungsregeln ohne Tk: Platz, Auslassung und unveränderte Skalen."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import ui_design as design


class DesignTest(unittest.TestCase):
    def test_remaining_counter_and_limit_message(self):
        # D67 (07.11.2026): von 40 herunterzählen, Überschreitung klar benennen.
        self.assertEqual(design.remaining_text(0), "noch 40 Zeichen")
        self.assertEqual(design.remaining_text(39), "noch 1 Zeichen")
        self.assertEqual(design.remaining_text(40), "keine Zeichen mehr frei")
        self.assertEqual(design.remaining_text(43), "3 Zeichen zu viel")
        self.assertEqual(design.remaining_text(17, short=True), "noch 23")
        self.assertEqual(design.remaining_text(40, short=True), "0 übrig")
        self.assertEqual(design.remaining_text(41, short=True), "1 zu viel")
        self.assertEqual(design.limit_message(), "Höchstens 40 Zeichen")
        self.assertEqual(design.limit_message(40, 17), "Höchstens 40 Zeichen · 17 nicht übernommen")
        self.assertEqual(design.limit_message(40, short=True), "max. 40")
        self.assertEqual(design.limit_message(40, 5, short=True), "5 gekürzt")

    def test_edited_task_title_keeps_full_input_once_and_preserves_legacy(self):
        legacy = "Ü" * 300
        self.assertEqual(design.edited_task_title(legacy, legacy, "Notiz"), (legacy, "Notiz"))
        for size in (39, 40, 41, 300):
            original = "Ü" * size
            title, note = design.edited_task_title(original, "Alt", "Notiz")
            self.assertLessEqual(len(title), design.TITLE_MAX_CHARS)
            if size > 40:
                self.assertIn(original, note)
                self.assertEqual(note.count("Originaltitel:"), 1)
            else:
                self.assertEqual((title, note), (original, "Notiz"))
            self.assertEqual(design.edited_task_title(title, title, note), (title, note))

    def test_imported_title_keeps_original_in_description_without_changing_legacy(self):
        original = "Langer Originaltitel " * 5
        title, description = design.task_title(original, "Bestehende Beschreibung")
        self.assertEqual(len(title), 40)
        self.assertTrue(title.endswith("..."))
        self.assertIn(original, description)
        self.assertTrue(description.startswith("Bestehende Beschreibung"))
        self.assertEqual(design.task_title(original, "unverändert", preserve=True), (original, "unverändert"))

    def test_title_limits_preserve_legacy_until_title_changes(self):
        legacy = "Änderung " * 20
        self.assertEqual(design.TITLE_MAX_CHARS, 40)
        self.assertEqual(design.BUTTON_TEXT_MAX_CHARS, 24)
        self.assertEqual(design.edited_title(legacy, legacy), legacy)
        for text in ("", "a" * 39, "a" * 40, "a" * 41, legacy):
            shown = design.clip_title(text)
            self.assertLessEqual(len(shown), 40)
            self.assertEqual(design.edited_title(text, "alt"), shown)
            if len(text) > 40:
                self.assertTrue(shown.endswith("..."))

    def test_title_display_fits_glyphs_and_character_limit(self):
        measure = lambda text: sum(12 if char == "W" else 3 for char in text)
        for text in ("Kurz", "W" * 40, "Titel " * 100, "ÄÖÜ ß Emoji 😀"):
            for width in range(300):
                shown = design.display_title(text, measure, width)
                self.assertLessEqual(len(shown), 40)
                self.assertLessEqual(measure(shown), width)
                if shown and shown != text:
                    self.assertTrue(shown.endswith("..."))

    def test_page_icon_stays_before_text_and_inside_reading_margin(self):
        for padding in (0, 12, 24, 28, 40, 80, 240):
            for height in (12, 16, 30, 38, 76):
                for preferred in (1, 2, 4):
                    layout = design.page_icon_layout(padding, height, preferred)
                    if padding < 24 or height < 16:
                        self.assertIsNone(layout)
                        continue
                    scale, x, y = layout
                    self.assertGreaterEqual(scale, 1)
                    self.assertLessEqual(scale, preferred)
                    self.assertGreaterEqual(x, -padding)
                    self.assertEqual(x + 16 * scale, -8)
                    self.assertGreaterEqual(y, 0)
                    self.assertLessEqual(y + 16 * scale, height)

    def test_scales_keep_existing_values_and_are_immutable(self):
        self.assertEqual(design.RADII["card"], 18)
        self.assertEqual(design.FONT_SIZES["title"], 22)
        self.assertEqual(design.ROW_HEIGHTS["task"], 36)
        with self.assertRaises(TypeError):
            design.SPACING[12] = 14

    def test_fit_text_at_edges(self):
        for text in ("", "Heute", "äöüß", "Aufgabe   mit Rand", "x" * 10000):
            for width in range(30):
                shown = design.fit_text(text, len, width)
                self.assertLessEqual(len(shown), width)
                if len(text) <= width:
                    self.assertEqual(shown, text)
                elif shown:
                    self.assertTrue(shown.endswith("…"))
                    self.assertTrue(text.startswith(shown[:-1]))

    def test_fit_text_measures_glyphs_and_bounds_calls(self):
        calls = []
        def measure(text):
            calls.append(text)
            return sum(3 if c == "W" else 1 for c in text)
        self.assertEqual(design.fit_text("WWWabc", measure, 7), "WW…")
        calls.clear()
        self.assertEqual(design.fit_text("W" * 10000, measure, 20), "W" * 6 + "…")
        self.assertLess(len(calls), 20)
        self.assertEqual(design.fit_text("W", measure, 0), "")

    def test_today_title_and_source_fit_at_supported_widths(self):
        for width in range(400, 1800):
            title, due, labels, source, gap = design.today_columns(width, 132, 160)
            self.assertGreaterEqual(title, 260)
            self.assertGreaterEqual(source, 100)
            self.assertLessEqual(source, 180)
            self.assertLessEqual(title + due + labels + source + gap + 6, width)
        self.assertEqual(design.today_columns(480, 132, 160)[1:3], (0, 0))
        self.assertEqual(design.today_columns(1200, 132, 160)[1:3], (132, 160))

    def test_today_title_stays_widest_with_wide_due_column(self):
        # B11/D59: Fälligkeit mit Bearbeitungstag in Roboto Mono, große Schrift.
        for width in range(400, 1800):
            title, due, labels, _source, _gap = design.today_columns(width, 343, 160)
            self.assertGreater(title, max(due, labels), width)



class LoeschtasteTest(unittest.TestCase):
    """Mac-Abnahme 07.11.2026: Rücktaste im Feld löschte den markierten Punkt."""

    def test_pfad_mit_trenner(self):
        self.assertTrue(design.widget_within(".!frame7", ".!frame7"))
        self.assertTrue(design.widget_within(".!frame7.!entry", ".!frame7"))
        self.assertFalse(design.widget_within(".!frame70.!entry", ".!frame7"))
        self.assertFalse(design.widget_within(".!frame7", None))
        self.assertFalse(design.widget_within("", ".!frame7"))

    def test_textfelder_bearbeiten_text(self):
        for klasse in ("Entry", "Text", "TEntry"):
            self.assertTrue(design.delete_key_edits_text(klasse, ".!x.!feld"))
        self.assertTrue(design.delete_key_edits_text("Canvas", ".!suche", [".!suche"]))
        self.assertTrue(design.delete_key_edits_text("Canvas", ".!inspektor.!knopf", (), ".!inspektor"))

    def test_baum_und_fenster_loeschen_punkte(self):
        self.assertFalse(design.delete_key_edits_text("Treeview", ".!liste.!baum", [".!suche"], ".!inspektor"))
        self.assertFalse(design.delete_key_edits_text("Tk", ".", [".!suche"], ".!inspektor"))
        self.assertFalse(design.delete_key_edits_text("Canvas", ".!inspektor70", (), ".!inspektor"))


class RestflaechenTest(unittest.TestCase):
    """Mac-Abnahme 07.11.2026: leere Rahmen behielten die Höhe entfernter Kinder."""

    def test_leerer_rahmen_mit_alter_hoehe(self):
        self.assertTrue(design.stale_empty_frame(False, 0, 0, 406, 168))
        self.assertTrue(design.stale_empty_frame(False, 0, 0, 1, 2))

    def test_ruhegroesse_kinder_oder_eigene_groesse(self):
        self.assertFalse(design.stale_empty_frame(False, 0, 0, 1, 1))
        self.assertFalse(design.stale_empty_frame(True, 0, 0, 406, 168))
        self.assertFalse(design.stale_empty_frame(False, 0, 24, 1, 24))
        self.assertFalse(design.stale_empty_frame(False, 200, 0, 200, 1))


class GleicheMarkenbreiteTest(unittest.TestCase):
    """Mac-Abnahme 07.11.2026: erledigte Punkte waren weiter eingerückt."""

    @staticmethod
    def messen(text):
        breiten = {"✓": 9, "□": 12, design.HAIR_SPACE: 1, "☑": 13}
        return sum(breiten.get(z, 7) for z in text)

    def test_schmaleres_zeichen_wird_aufgefuellt(self):
        paar = design.aligned_markers(("✓", "□"), self.messen)
        self.assertEqual(self.messen(paar["✓"]), self.messen(paar["□"]))
        self.assertEqual(paar["□"], "□")
        self.assertTrue(paar["✓"].startswith("✓"))

    def test_naechste_breite_ohne_ueberschuss(self):
        grob = lambda text: sum(10 if z == "□" else 4 if z == design.HAIR_SPACE else 7 for z in text)
        self.assertEqual(grob(design.pad_to_width("✓", 10, grob)), 11)
        self.assertEqual(design.pad_to_width("□", 10, grob), "□")

    def test_gleiche_zeichen(self):
        self.assertEqual(design.aligned_markers(("□", "□"), self.messen), {"□": "□"})


class BeruhigterUmbruchTest(unittest.TestCase):
    """Umbruchbreite im Einstellungsdialog: neue Breiten gelten, wiederkehrende beenden die Runde."""

    def test_neue_breiten_gelten_wie_gemeldet(self):
        gesehen = set()
        self.assertEqual([design.settled_wrap_width(breite, gesehen) for breite in (300, 402, 483)], [300, 402, 483])
        self.assertEqual(gesehen, {300, 402, 483})

    def test_wiederkehrende_breite_ergibt_die_engste(self):
        # Gemessene Schaukel mit DM Serif Display in kleiner Schrift: 402 → 411 → 428 → 402 → …
        gesehen, gesetzt = set(), []
        for breite in (402, 411, 428, 402, 411, 428, 402):
            gesetzt.append(design.settled_wrap_width(breite, gesehen))
        self.assertEqual(gesetzt, [402, 411, 428, 402, 402, 402, 402])

    def test_geleerte_menge_gibt_breitere_spalte_wieder_frei(self):
        gesehen = {402, 411, 428}
        self.assertEqual(design.settled_wrap_width(411, gesehen), 402)
        gesehen.clear()
        self.assertEqual(design.settled_wrap_width(483, gesehen), 483)

if __name__ == "__main__":
    unittest.main()
