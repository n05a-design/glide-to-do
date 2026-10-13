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
