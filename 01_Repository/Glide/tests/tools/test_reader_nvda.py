"""Test-Synthesizerfall und verpflichtende tatsächliche Sprache ohne NVDA/GUI."""
import json
from pathlib import Path
import unittest

from reader_nvda import SPEECH_SPY_MODULE, Spy, profile_configuration


class ReaderNvda(unittest.TestCase):
    def test_config_uses_exact_original_synth_module_case(self):
        lock = json.loads(Path(__file__).with_name('reader_nvda_lock.json').read_text())
        original = next(record['file'] for record in lock['files'] if record['file'].endswith('SynthDriver.py'))
        self.assertEqual(SPEECH_SPY_MODULE, Path(original).stem)
        self.assertIn('synth = '+Path(original).stem+'\n', profile_configuration())
        self.assertIn('autoCheck = False', profile_configuration())
        self.assertIn('allowUsageStats = False', profile_configuration())

    def test_arrow_aliases_match_nvda_and_foreign_focus_prevents_input(self):
        spy = object.__new__(Spy)
        spy.foreground_pid = lambda: 123
        calls = []
        spy.call = lambda *args: calls.append(args)
        spy.key(123, 'down');spy.key(123, 'control+up')
        self.assertEqual(calls, [('emulateKeyPress','downArrow'), ('emulateKeyPress','control+upArrow')])
        with self.assertRaisesRegex(RuntimeError, 'Vordergrund'):
            spy.key(999, 'down')
        self.assertEqual(len(calls), 2)

    def test_empty_or_missing_remote_speech_is_a_clear_failure(self):
        spy = object.__new__(Spy)
        for value in (None, '', '  ', 0):
            spy.call = lambda name, *args: value
            with self.subTest(value=value), self.assertRaisesRegex(AssertionError, 'keine tatsächliche Sprachausgabe'):
                spy.speech(0)
        spy.call = lambda name, *args: 'Neue Aufgabe edit'
        self.assertEqual(spy.speech(0), 'Neue Aufgabe edit')


if __name__ == '__main__':
    unittest.main()
