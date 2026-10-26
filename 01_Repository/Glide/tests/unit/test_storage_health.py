"""WA-40/47: begrenztes Lesen und Zustände ohne Tk."""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import storage_health as storage


class StorageHealthTests(unittest.TestCase):
    def test_encoded_size_includes_windows_line_endings(self):
        text = '{\n    "Größe": 1\n}'
        for newline in ("\n", "\r\n"):
            self.assertEqual(storage.json_size(text, newline),
                             len(text.replace("\n", newline).encode("utf-8")))

    def test_json_boundary_and_unicode(self):
        raw = json.dumps({"text": "Größe"}, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.json"
            path.write_bytes(raw)
            self.assertEqual(storage.read_json(path, len(raw)), {"text": "Größe"})
            with self.assertRaises(storage.SizeLimitError):
                storage.read_json(path, len(raw) - 1)
            self.assertEqual(path.read_bytes(), raw)

    def test_oversized_file_is_not_read(self):
        stream = unittest.mock.Mock()
        with patch.object(storage.os, "fstat", return_value=unittest.mock.Mock(st_size=11)):
            with self.assertRaises(storage.SizeLimitError):
                storage.read_stream(stream, 10)
        stream.read.assert_not_called()

    def test_growth_after_stat_is_bounded(self):
        stream = io.BytesIO(b" " * 11)
        stream.fileno = lambda: 1
        with patch.object(storage.os, "fstat", return_value=unittest.mock.Mock(st_size=1)):
            with self.assertRaises(storage.SizeLimitError):
                storage.read_stream(stream, 10)
        self.assertEqual(stream.tell(), 11)

    def test_invalid_json_remains_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.json"
            path.write_bytes(b"{")
            with self.assertRaises(ValueError):
                storage.read_json(path)

    def test_failure_count_and_log_deduplication(self):
        health = storage.Health()
        self.assertTrue(health.fail("settings", "gesperrt"))
        self.assertFalse(health.fail("settings", "gesperrt"))
        self.assertEqual(health.failures["settings"], ("gesperrt", 2))
        self.assertTrue(health.fail("settings", "voll"))
        self.assertEqual(health.failures["settings"], ("voll", 1))

    def test_success_does_not_clear_other_failure(self):
        health = storage.Health()
        health.fail("data", "gesperrt")
        health.fail("backup", "nicht erreichbar")
        health.success("data", 15)
        self.assertEqual(set(health.failures), {"backup"})
        self.assertEqual(health.sizes["data"], 15)
        self.assertIn("Speicherproblem", health.notice())

    def test_warning_boundary_and_recovery(self):
        health = storage.Health()
        health.success("data", 79)
        self.assertFalse(health.capacity_warning(100))
        health.success("settings", 1)
        self.assertTrue(health.capacity_warning(100))
        self.assertIn("Sicherungsreserve", health.notice(100))
        self.assertIn("Frühwarnung", health.report(100))
        health.success("data", 10)
        self.assertEqual(health.notice(100), "")


if __name__ == "__main__":
    unittest.main()
