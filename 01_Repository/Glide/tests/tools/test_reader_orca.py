"""Readerausgabe und Eingabeisolation ohne installierten Orca-Prozess."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pruefe_reader_orca as reader


class ReaderOrca(unittest.TestCase):
    def test_only_actual_orca_speech_output_is_parsed(self):
        data = "spd-say Neue Aufgabe\nSPEECH OUTPUT: 'Neue Aufgabe' voice=default\nSPEECH OUTPUT: 'entry' voice=default\n"
        self.assertEqual(reader.speech_fragments(data), ['Neue Aufgabe', 'entry'])
        self.assertEqual(reader.speech_fragments('AT-SPI name=Neue Aufgabe\nspd-say entry'), [])

    def test_foreign_foreground_prevents_every_keyboard_operation(self):
        actor = reader.Actor(123, Path('unused'), {})
        with patch.object(reader.subprocess, 'check_output', return_value='999'), \
                patch.object(reader.subprocess, 'run') as send:
            for operation in (lambda: actor.key('tab'), lambda: actor.type('Test')):
                with self.assertRaisesRegex(RuntimeError, 'Vordergrund'):
                    operation()
            send.assert_not_called()

    def test_hosted_scope_and_private_destination_are_required(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(reader.sys, 'platform', 'linux'), \
                patch.dict(os.environ, {'GITHUB_ACTIONS': 'true', 'RUNNER_ENVIRONMENT': 'github-hosted',
                                        'RUNNER_TEMP': directory}):
            base = Path(directory).resolve()
            self.assertEqual(reader.require_hosted(base/'probe'), base/'probe')
            for target in (base, base.parent/'outside'):
                with self.assertRaises(ValueError):
                    reader.require_hosted(target)
            with patch.dict(os.environ, {'RUNNER_ENVIRONMENT': 'self-hosted'}):
                with self.assertRaises(RuntimeError):
                    reader.require_hosted(base/'probe')


if __name__ == '__main__':
    unittest.main()
