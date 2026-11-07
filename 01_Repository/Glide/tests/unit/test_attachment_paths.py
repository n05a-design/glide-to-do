import unittest
from attachment_paths import validate_storage, storage_key

class PathTests(unittest.TestCase):
    def test_flat_portable_names_and_normalized_collision_keys(self):
        self.assertEqual(validate_storage(" attachments/Bild ä.png "),"attachments/Bild ä.png")
        self.assertEqual(validate_storage("attachments/a "),"attachments/a")
        self.assertEqual(storage_key("attachments/Café.PNG"),storage_key("attachments/Cafe\u0301.png"))
        self.assertNotEqual(storage_key("attachments/a.png"),storage_key("attachments/b.png"))

    def test_escape_and_windows_reserved_names_are_rejected(self):
        for value in (None, [], "", "/attachments/x", "attachments/../x", "attachments/x/y", "attachments/x\\y",
                      "attachments/a.", "attachments/a:stream", "attachments/x\x00y",
                      "attachments/a\ny", "attachments/CON.txt", "attachments/com9", "attachments/LPT1.png"):
            with self.subTest(value=value), self.assertRaises(ValueError):validate_storage(value)

if __name__=="__main__":unittest.main()


class NameLimitTests(unittest.TestCase):
    """D67 (menschliche Abnahme 07.11.2026): Anhangsnamen höchstens 40 Zeichen."""

    def test_limit_and_stored_name_bound(self):
        import attachment_paths as ap
        self.assertEqual(ap.NAME_MAX_CHARS, 40)
        self.assertEqual(ap.STORED_NAME_MAX_CHARS, 73)
        self.assertIsNone(ap.name_problem("Bericht.pdf"))
        self.assertIsNone(ap.name_problem("x" * 40))
        self.assertIn("41 Zeichen", ap.name_problem("x" * 41))
        for falsch in ("", "   ", "a:b.png", "Bild."):
            self.assertIsNotNone(ap.name_problem(falsch), falsch)
        self.assertTrue(ap.stored_name_too_long("attachments/" + "a" * 74))
        self.assertTrue(ap.too_long("x" * 41))
        self.assertFalse(ap.too_long("report."))  # Zeichenregeln nur beim Eintippen
        self.assertFalse(ap.too_long("  " + "x" * 40 + "  "))
        self.assertFalse(ap.stored_name_too_long("attachments/" + "a" * 73))

    def test_shortened_name_keeps_extension_and_is_always_valid(self):
        import attachment_paths as ap
        lang = "Sehr langer Dateiname für das Projekt Parkquartier Version 3 final.jpeg"
        kurz = ap.shortened_name(lang)
        self.assertEqual(kurz, "Sehr langer Dateiname für das Proje.jpeg")
        self.assertTrue(kurz.endswith(".jpeg") and len(kurz) <= 40)
        self.assertEqual(ap.shortened_name("Bericht.pdf"), "Bericht.pdf")
        for name in ("a" * 300, "x" + ".pdf" * 30, "C:\\Pfad\\" + "b" * 80 + ".png", " . ", "Bild:1?.png",
                     "ä" * 60 + ".tar.gz", "." + "z" * 50):
            with self.subTest(name=name):
                vorschlag = ap.shortened_name(name)
                self.assertIsNone(ap.name_problem(vorschlag), vorschlag)
                validate_storage("attachments/" + "0" * 32 + "_" + vorschlag)

    def test_keep_extension(self):
        import attachment_paths as ap
        self.assertEqual(ap.keep_extension("Grundriss", "sehr-lang.PDF"), "Grundriss.PDF")
        self.assertEqual(ap.keep_extension("Grundriss.pdf", "sehr-lang.PDF"), "Grundriss.pdf")
        self.assertEqual(ap.keep_extension("Notiz", "ohne_endung"), "Notiz")

    def test_group_long_storages_and_restore_names_by_id(self):
        import attachment_paths as ap
        lang = "attachments/" + "a" * 32 + "_" + "x" * 60 + ".jpg"
        kurz = "attachments/" + "b" * 32 + "_kurz.jpg"
        a1 = {"id": "1", "storage": lang, "name": "x" * 40}
        a2 = {"id": "2", "storage": lang, "name": "x" * 40}
        a3 = {"id": "3", "storage": kurz, "name": "x" * 40}
        gruppen = ap.group_long_storages([a1, a2, a3, None, "kaputt"])
        self.assertEqual(list(gruppen), [lang])
        self.assertEqual([a["id"] for a in gruppen[lang]], ["1", "2"])
        # Zwei Anhänge mit gleichem Kurznamen: nur der aufgezeichnete kehrt zurück.
        self.assertEqual(ap.restore_names([a1, a2, a3], [("2", "Original zwei.jpg", "x" * 40)]), 1)
        self.assertEqual((a1["name"], a2["name"], a3["name"]), ("x" * 40, "Original zwei.jpg", "x" * 40))
        # Inzwischen umbenannt: nicht überschreiben.
        a1["name"] = "Neu.jpg"
        self.assertEqual(ap.restore_names([a1], [("1", "Original eins.jpg", "x" * 40)]), 0)
        self.assertEqual(a1["name"], "Neu.jpg")

