"""Aktive Typen und tatsächlichen Ablageort ohne erfundene Importherkunft bestimmen."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import attachment_policy as policy


class AttachmentPolicy(unittest.TestCase):
    def test_active_types_uppercase_and_double_extension(self):
        for name in ('Rechnung.pdf.EXE', 'Start.cmd', 'script.ps1', 'Link.lnk',
                     'Bild.js', 'Befehl.command', 'Anwendung.desktop', 'Programm.app'):
            with self.subTest(name=name):
                self.assertIsNotNone(policy.question(name))

    def test_images_documents_and_folders_are_quiet(self):
        for name in ('Notiz.pdf', 'Bild.png', 'Tabelle.csv', 'Sicherung.glideapp', '/ordner'):
            self.assertIsNone(policy.question(name))

    def test_stored_extension_checked_independently_of_display_name(self):
        self.assertEqual(policy.active_type('id.exe', 'Bild.png'), '.exe')
        self.assertEqual(policy.active_type('id.png', 'Start.exe'), '.exe')

    def test_message_names_file_type_and_origin(self):
        text = policy.question('script.ps1', 'Mein Skript.ps1', 'Gerade lokal gewählt')
        for part in ('Mein Skript.ps1', '.ps1', 'Gerade lokal gewählt', 'jetzt öffnen'):
            self.assertIn(part, text)

    def test_origin_uses_path_boundary_and_reports_unknown_history(self):
        with tempfile.TemporaryDirectory(prefix='glide-herkunft-') as folder:
            base = Path(folder) / 'daten'
            self.assertIn('Sicherung oder Vorlage', policy.origin_text(base / 'attachments/start.cmd', base))
            self.assertIn('außerhalb', policy.origin_text(Path(str(base) + '-alt/start.cmd'), base))


if __name__ == '__main__':
    unittest.main()
