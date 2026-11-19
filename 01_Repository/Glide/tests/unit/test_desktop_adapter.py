# SPDX-License-Identifier: MPL-2.0
"""Prüfung für desktop_adapter (Shell-Paket 5, D86, D88).

Prüft Plattform-Erkennung, Beschleuniger-Formatierung, rekursiven Menüaufbau,
Aktionszuordnung, Menüleisten-Erzeugung und Zwischenablage-Operationen.
"""

from pathlib import Path
import sys
import tkinter as tk
import unittest
from unittest.mock import MagicMock, patch

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import desktop_adapter


class TestPlattformUndModifikatoren(unittest.TestCase):
    def test_plattform_flags(self):
        self.assertIsInstance(desktop_adapter.is_macos(), bool)
        self.assertIsInstance(desktop_adapter.is_windows(), bool)
        self.assertIsInstance(desktop_adapter.is_linux(), bool)
        self.assertIn(desktop_adapter.platform_name(), ("macos", "windows", "linux"))

    def test_primary_modifier(self):
        self.assertEqual(desktop_adapter.primary_modifier(macos_override=True), "Cmd")
        self.assertEqual(desktop_adapter.primary_modifier(macos_override=False), "Strg")
        labels = {"command": "Cmd", "control": "Ctrl"}
        self.assertEqual(
            desktop_adapter.primary_modifier(macos_override=False, modifier_labels=labels),
            "Ctrl",
        )

    def test_format_accelerator(self):
        self.assertEqual(
            desktop_adapter.format_accelerator("O", macos_override=True),
            "Cmd+O",
        )
        self.assertEqual(
            desktop_adapter.format_accelerator("O", macos_override=False),
            "Strg+O",
        )
        self.assertEqual(
            desktop_adapter.format_accelerator("Shift", "P", macos_override=True),
            "Cmd+Shift+P",
        )
        self.assertEqual(
            desktop_adapter.format_accelerator("Shift", "N", macos_override=False),
            "Strg+Shift+N",
        )
        self.assertEqual(
            desktop_adapter.format_accelerator(
                "P", macos_override=False, modifier_labels={"control": "Ctrl"}
            ),
            "Ctrl+P",
        )

    def test_format_redo_accelerator(self):
        self.assertEqual(
            desktop_adapter.format_redo_accelerator(windows_override=True),
            "Strg+Y",
        )
        self.assertEqual(
            desktop_adapter.format_redo_accelerator(
                windows_override=False, macos_override=True
            ),
            "Cmd+Shift+Z",
        )
        self.assertEqual(
            desktop_adapter.format_redo_accelerator(
                windows_override=False, macos_override=False
            ),
            "Strg+Shift+Z",
        )
        self.assertEqual(
            desktop_adapter.format_redo_accelerator(
                windows_override=False, macos_override=False,
                modifier_labels={"control": "Ctrl", "shift": "Shift"},
            ),
            "Ctrl+Shift+Z",
        )


class TestMenuTreeBuilder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.root = tk.Tk()
            cls.root.withdraw()
        except tk.TclError as exc:
            raise unittest.SkipTest(f"Tk-Display nicht verfügbar: {exc}")

    @classmethod
    def tearDownClass(cls):
        try:
            if hasattr(cls, "root"):
                cls.root.destroy()
        except Exception:
            pass

    def test_build_menu_tree_flach_und_trennlinien(self):
        menus = []
        action_map = {}
        dummy_cb = lambda: None

        def resolve_action(target):
            return "action.dummy" if target is dummy_cb else None

        eintraege = (
            ("Neu", dummy_cb, "Cmd+N", "action.custom_neu"),
            None,
            ("Beenden", dummy_cb, "Cmd+Q"),
        )
        menu = desktop_adapter.build_menu_tree(
            self.root, eintraege, menus_out=menus, tearoff=0, action_resolver=resolve_action
        )
        self.assertIn(menu, menus)
        # Menü hat 3 Einträge: 0 (Neu), 1 (Separator), 2 (Beenden)
        self.assertEqual(menu.entrycget(0, "label"), "Neu")
        self.assertEqual(menu.entrycget(0, "accelerator"), "Cmd+N")
        self.assertEqual(menu.type(1), "separator")
        self.assertEqual(menu.entrycget(2, "label"), "Beenden")
        self.assertEqual(menu._glide_action_ids[0], "action.custom_neu")
        self.assertEqual(menu._glide_action_ids[2], "action.dummy")

    def test_build_menu_tree_rekursive_untermenues(self):
        menus = []
        target_obj = type("Target", (), {})()
        dummy_cb = lambda: None

        eintraege = (
            ("Exportieren", (
                ("Als Text", dummy_cb, "Cmd+E"),
                ("Als CSV", dummy_cb),
            )),
            ("Dynamisch", "dynamic_submenu_attr"),
        )
        menu = desktop_adapter.build_menu_tree(
            self.root, eintraege, menus_out=menus, tearoff=0, attr_target=target_obj
        )
        self.assertEqual(len(menus), 3)  # Hauptmenü + Untermenü Exportieren + Dynamisches Menü
        self.assertTrue(hasattr(target_obj, "dynamic_submenu_attr"))
        self.assertIsInstance(getattr(target_obj, "dynamic_submenu_attr"), tk.Menu)


class TestDesktopMenuBar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.root = tk.Tk()
            cls.root.withdraw()
        except tk.TclError as exc:
            raise unittest.SkipTest(f"Tk-Display nicht verfügbar: {exc}")

    @classmethod
    def tearDownClass(cls):
        try:
            if hasattr(cls, "root"):
                cls.root.destroy()
        except Exception:
            pass

    def test_create_menubar_frame(self):
        frame = desktop_adapter.DesktopMenuBar.create_menubar_frame(self.root, "#ffffff")
        self.assertIsInstance(frame, tk.Frame)
        self.assertEqual(frame.cget("bg"), "#ffffff")
        frame.destroy()

    def test_post_popup_menu(self):
        btn = tk.Button(self.root, text="Datei")
        btn.pack()
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Test")

        restored = []
        prev_focus = "prev_widget"

        def mock_restore(widget):
            restored.append(widget)

        with patch.object(menu, "tk_popup") as mock_popup, \
             patch.object(menu, "grab_release") as mock_release:
            result = desktop_adapter.DesktopMenuBar.post_popup_menu(
                btn, menu, previous_focus=prev_focus, restore_cb=mock_restore
            )
            self.assertEqual(result, "break")
            mock_popup.assert_called_once()
            mock_release.assert_called_once()
            self.assertEqual(restored, [prev_focus])

        btn.destroy()
        menu.destroy()


class TestDesktopHelfer(unittest.TestCase):
    """Ohne Tk-Fenster: Startwege und Zwischenablage über Attrappen."""

    def test_launch_path_windows(self):
        with patch("os.startfile", create=True) as mock_startfile:
            res = desktop_adapter.launch_path("test.txt", windows_override=True)
            self.assertTrue(res)
            mock_startfile.assert_called_once_with("test.txt")

    def test_launch_path_macos(self):
        with patch("subprocess.Popen") as mock_popen:
            res = desktop_adapter.launch_path(
                "test.txt", windows_override=False, macos_override=True
            )
            self.assertTrue(res)
            mock_popen.assert_called_once_with(["open", "test.txt"])

    def test_launch_path_linux(self):
        with patch("subprocess.Popen") as mock_popen:
            res = desktop_adapter.launch_path(
                "test.txt", windows_override=False, macos_override=False
            )
            self.assertTrue(res)
            mock_popen.assert_called_once_with(["xdg-open", "test.txt"])

    def test_clipboard_roundtrip(self):
        # Attrappe statt echter Zwischenablage: Der Test darf die Zwischenablage
        # des Prüfrechners nicht überschreiben, und clipboard_clear auf einem
        # zurückgezogenen Wurzelfenster stürzte im Windows-CI unter Tk 9.1 mit
        # 0xC0000005 ab (Lauf 43955007037, 16.11.2026).
        ablage = []
        widget = MagicMock()
        widget.clipboard_clear.side_effect = ablage.clear
        widget.clipboard_append.side_effect = ablage.append
        widget.clipboard_get.side_effect = lambda: "".join(ablage)
        ablage.append("alter Inhalt")
        desktop_adapter.copy_to_clipboard(widget, "Glide Shell Test")
        widget.clipboard_clear.assert_called_once_with()
        widget.clipboard_append.assert_called_once_with("Glide Shell Test")
        self.assertEqual(desktop_adapter.read_from_clipboard(widget), "Glide Shell Test")

    def test_read_from_clipboard_error_fallback(self):
        mock_widget = MagicMock()
        mock_widget.clipboard_get.side_effect = tk.TclError("No clipboard content")
        self.assertEqual(desktop_adapter.read_from_clipboard(mock_widget), "")


if __name__ == "__main__":
    unittest.main()
