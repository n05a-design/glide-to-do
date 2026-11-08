# SPDX-License-Identifier: MPL-2.0
"""Modusauswahl und Begrenzung des nativen CI-Hilfswerkzeugs ohne OS-Änderung."""
from pathlib import Path
import unittest
from unittest.mock import patch
import macos_desktop


class MacDesktopTests(unittest.TestCase):
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
