# SPDX-License-Identifier: MPL-2.0
"""Modusauswahl und Begrenzung des nativen CI-Hilfswerkzeugs ohne OS-Änderung."""
from pathlib import Path
import plistlib
import unittest
from unittest.mock import patch, Mock
import macos_desktop


class MacDesktopTests(unittest.TestCase):
    def test_dock_setting_is_restored_after_a_failed_test(self):
        for preferences in ({}, {'autohide':False}):
            with self.subTest(preferences=preferences):
                result = Mock(stdout=plistlib.dumps(preferences))
                evidence = {}
                with patch.object(macos_desktop.subprocess, 'run', return_value=result) as execute:
                    with self.assertRaisesRegex(ValueError, 'fehlgeschlagen'):
                        with macos_desktop.dock_workarea(evidence):
                            raise ValueError('Test fehlgeschlagen')
                commands = [call.args[0] for call in execute.call_args_list]
                self.assertEqual(commands[1], ['defaults','write','com.apple.dock','autohide','-bool','true'])
                self.assertEqual(commands[-1], ['killall','Dock'])
                self.assertEqual(commands[-2],
                    ['defaults','delete','com.apple.dock','autohide'] if not preferences else
                    ['defaults','write','com.apple.dock','autohide','-bool','false'])
                self.assertTrue(evidence['dock_autohide_restored'])

    def test_existing_autohide_is_not_rewritten(self):
        with patch.object(macos_desktop.subprocess, 'run',
                          return_value=Mock(stdout=plistlib.dumps({'autohide':True}))) as execute:
            with macos_desktop.dock_workarea({}):
                pass
        self.assertEqual(execute.call_count, 1)

    def test_workarea_reports_actual_geometry_instead_of_assuming_display_size(self):
        with patch.object(macos_desktop.subprocess, 'run', return_value=Mock(
                stdout='{"requested":[1720,960],"actual":[1720,954],"tk":"9.1"}', stderr='')):
            self.assertEqual(macos_desktop.verify_workarea()['actual'], [1720,954])

    def test_smallest_usable_mode_meets_both_dimensions(self):
        modes = [dict(width=w, height=h, pixel_width=pw, pixel_height=ph, usable=u)
                 for w, h, pw, ph, u in ((1024,768,1024,768,True), (1920,1080,3840,2160,True),
                                        (1920,1080,1920,1080,True), (2560,1440,2560,1440,True),
                                        (1920,1080,1900,1000,False))]
        selected = macos_desktop.select_mode(modes, 1920, 1080)
        self.assertEqual((selected['width'],selected['height'],selected['pixel_width']), (1920,1080,1920))

    def test_unavailable_height_is_a_prerequisite_failure(self):
        with self.assertRaisesRegex(RuntimeError, "Kein nativer Bildschirmmodus"):
            macos_desktop.select_mode([dict(width=1920,height=700,pixel_width=1920,pixel_height=700,usable=True)],1920,1080)

    def test_personal_machine_is_rejected_before_loading_native_libraries(self):
        with patch.dict(macos_desktop.os.environ, {'GITHUB_ACTIONS':'false'}), \
                patch.object(macos_desktop.ctypes,'CDLL') as load:
            with self.assertRaisesRegex(RuntimeError,"GitHub Actions"):
                macos_desktop.run(['never'],1920,1080,Path('never.json'))
            load.assert_not_called()


if __name__ == '__main__':
    unittest.main()
