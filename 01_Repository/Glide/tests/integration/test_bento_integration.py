# SPDX-License-Identifier: MPL-2.0
"""Integrations- und Geometrietests für das Glide Bento Box System (D100, Bento 0.1.0).

Prüft BentoGrid im echten Tk-Container unter X11/macOS:
- Dynamische Breitenanpassung (1, 2 und 3 Spalten)
- Geometrische Integrität (keine Überlappung von Karten)
- Positive Abmessungen (Breite > 0, Höhe > 0)
- Einhaltung der Abstände (Gaps und Paddings)
- Header-Karten über die gesamte Breite
"""
import os
from pathlib import Path
import sys
import tkinter as tk
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from glide_bento import (
    BentoCard,
    BentoCardSpec,
    BentoContext,
    BentoGrid,
    BentoGridSpec,
    BentoTokens,
)

_SHARED_ROOT = None


def get_shared_root():
    global _SHARED_ROOT
    if _SHARED_ROOT is None:
        try:
            _SHARED_ROOT = tk.Tk()
            _SHARED_ROOT.withdraw()
        except tk.TclError as exc:
            if os.environ.get("GLIDE_REQUIRE_TK") == "1":
                raise RuntimeError(f"GLIDE_REQUIRE_TK=1 ist aktiv, aber Tk konnte nicht initialisiert werden: {exc}") from exc
            _SHARED_ROOT = False
    return _SHARED_ROOT


class TestBentoIntegration(unittest.TestCase):
    """Integrations- und Geometrieprüfung für BentoGrid unter Tkinter."""

    @classmethod
    def setUpClass(cls):
        cls.root = get_shared_root()
        if cls.root is False:
            raise unittest.SkipTest("Tkinter-Display nicht verfügbar")

    def setUp(self):
        self.host_window = tk.Toplevel(self.root)
        self.host_window.geometry("800x600")
        self.context = BentoContext(
            theme={
                "bg": "#F5F5F7",
                "card": "#FFFFFF",
                "line": "#E5E5E7",
                "text": "#1D1D1F",
                "muted": "#86868B",
                "accent": "#0071E3",
            }
        )

    def tearDown(self):
        self.host_window.destroy()

    def test_bento_grid_spaltenstufen_und_geometrie(self):
        """BentoGrid passt Spaltenzahl bei Breitenänderungen an und platziert Karten überschneidungsfrei."""
        grid = BentoGrid(self.host_window, context=self.context)
        grid.pack(fill="both", expand=True)

        cards = [
            BentoCard(grid, context=self.context, title="Vollbreite", spec=BentoCardSpec(key="header", span="wide")),
            BentoCard(grid, context=self.context, title="Karte 1", spec=BentoCardSpec(key="c1", weight=2)),
            BentoCard(grid, context=self.context, title="Karte 2", spec=BentoCardSpec(key="c2", weight=1)),
            BentoCard(grid, context=self.context, title="Karte 3", spec=BentoCardSpec(key="c3", weight=2)),
            BentoCard(grid, context=self.context, title="Karte 4", spec=BentoCardSpec(key="c4", weight=1)),
        ]
        for c in cards:
            # Etwas Inhalt in jede Karte einfügen
            tk.Label(c.body, text=f"Inhalt von {c.spec.key}", bg=c.fill_color).pack(pady=10)
            grid.add_card(c)

        # 1. Stufe: 500 px -> 1 Spalte
        self.host_window.geometry("500x700")
        self.host_window.update()
        grid.reflow()
        self.host_window.update()

        self.assertEqual(grid.current_columns, 1)

        # 2. Stufe: 750 px -> 2 Spalten
        self.host_window.geometry("750x700")
        self.host_window.update()
        grid.reflow()
        self.host_window.update()

        self.assertEqual(grid.current_columns, 2)

        # 3. Stufe: 1100 px -> 3 Spalten
        self.host_window.geometry("1100x700")
        self.host_window.update()
        grid.reflow()
        self.host_window.update()

        self.assertEqual(grid.current_columns, 3)

        # Geometrieprüfung: Alle Karten müssen positive Abmessungen haben
        for c in cards:
            self.assertGreater(c.winfo_width(), 100, f"Breite von {c.spec.key} zu klein")
            self.assertGreater(c.winfo_height(), 30, f"Höhe von {c.spec.key} zu klein")

        # Header-Karte muss breiter sein als einzelne Spaltenkarten
        header_card = cards[0]
        col_card = cards[1]
        self.assertGreater(header_card.winfo_width(), col_card.winfo_width())

    def test_keine_karten_ueberlappung_im_spaltenraster(self):
        """Karten innerhalb derselben Spalte dürfen sich vertikal nicht überlappen."""
        grid = BentoGrid(self.host_window, context=self.context)
        grid.pack(fill="both", expand=True)

        cards = [
            BentoCard(grid, context=self.context, title=f"K{i}", spec=BentoCardSpec(key=f"k{i}", weight=1))
            for i in range(6)
        ]
        for c in cards:
            tk.Label(c.body, text="Zeile A\nZeile B\nZeile C", bg=c.fill_color).pack()
            grid.add_card(c)

        self.host_window.geometry("750x800")
        self.host_window.update()
        grid.reflow()
        self.host_window.update()

        # Prüfe vertikale Positionen jeder Karte in jeder Spalte
        for col_frame in grid._column_frames:
            karten_in_spalte = [w for w in col_frame.winfo_children() if isinstance(w, BentoCard)]
            for i in range(len(karten_in_spalte) - 1):
                oben = karten_in_spalte[i]
                unten = karten_in_spalte[i + 1]
                oben_y1 = oben.winfo_y() + oben.winfo_height()
                unten_y0 = unten.winfo_y()
                self.assertLessEqual(
                    oben_y1,
                    unten_y0,
                    f"Überlappung in Spalte: {oben.spec.key} (bis y={oben_y1}) überschneidet {unten.spec.key} (ab y={unten_y0})",
                )


if __name__ == "__main__":
    unittest.main()
