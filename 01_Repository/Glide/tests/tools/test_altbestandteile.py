# SPDX-License-Identifier: MPL-2.0
"""Werkzeugtest der Altbestandteilprüfung (D66, menschliche Abnahme 07.11.2026)."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import altbestandteile as alt  # noqa: E402


def funde(text):
    return [(f"probe:{zeile}", name) for zeile, name in alt.aufrufe(text=text)]


class Altbestandteile(unittest.TestCase):
    def test_delivered_source_has_no_legacy_system_widgets(self):
        befunde, zaehlung = alt.pruefen_quelle()
        self.assertEqual(befunde, [])
        for name, grenze in alt.BESTAND.items():
            self.assertLessEqual(zaehlung.get(name, 0), grenze, name)

    def test_every_import_spelling_of_a_system_scrollbar_is_found(self):
        proben = (
            "import tkinter as tk\nimport tkinter.ttk as ttk\nttk.Scrollbar(None)\ntk.Scrollbar(None)\n",
            "from tkinter import ttk\nttk.Scrollbar(None)\n",
            "from tkinter import Scrollbar\nScrollbar(None)\n",
            "import tkinter\ntkinter.Scrollbar(None)\n",
            "from tkinter.scrolledtext import ScrolledText\nScrolledText(None)\n",
            "from tkinter import ttk as t\nt.Combobox(None)\n",
            "from tkinter import simpledialog\nsimpledialog.askstring('a', 'b')\n",
        )
        for text in proben:
            befunde, _ = alt.befunde_aus(funde(text))
            self.assertTrue(befunde, text)
            self.assertIn("Systemaltstil", befunde[0])

    def test_glide_widgets_and_unrelated_calls_are_not_findings(self):
        text = ("import tkinter as tk\nclass ThemedAutoScrollbar(tk.Canvas):\n    pass\n"
                "ThemedAutoScrollbar(None)\ntk.Frame(None)\ntk.Canvas(None)\nScrollbar = list\nScrollbar()\n")
        self.assertEqual(alt.befunde_aus(funde(text)), ([], {}))

    def test_ratchet_allows_only_fewer_classic_widgets(self):
        text = "import tkinter as tk\n" + "tk.Checkbutton(None)\n" * 3
        self.assertEqual(alt.befunde_aus(funde(text), {"tkinter.Checkbutton": 3})[0], [])
        befunde, zaehlung = alt.befunde_aus(funde(text), {"tkinter.Checkbutton": 2})
        self.assertEqual(zaehlung, {"tkinter.Checkbutton": 3})
        self.assertEqual(len(befunde), 1)
        self.assertIn("höchstens 2", befunde[0])

    def test_runtime_classes_cover_both_scrollbar_families(self):
        self.assertTrue({"Scrollbar", "TScrollbar", "TCombobox", "Spinbox"} <= alt.WIDGETKLASSEN_VERBOTEN)
        self.assertFalse(alt.WIDGETKLASSEN_VERBOTEN & {"Canvas", "Frame", "Label", "Text", "Entry", "Treeview"})
        self.assertFalse(alt.WIDGETKLASSEN_VERBOTEN & alt.WIDGETKLASSEN_BESTAND)


if __name__ == "__main__":
    unittest.main()
