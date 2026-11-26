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

        # Bis 0.1.0 prüfte diese Schleife nur Kinder der Spaltenrahmen; Karten
        # gehören aber dem Raster, die Prüfung lief leer. Jetzt über echte
        # Bildschirmrechtecke aller Kartenpaare.
        self.assert_rechtecke_disjunkt(cards)

    def assert_rechtecke_disjunkt(self, widgets):
        boxes = []
        for w in widgets:
            self.assertTrue(w.winfo_ismapped(), f"{w.spec.key} nicht platziert")
            x0, y0 = w.winfo_rootx(), w.winfo_rooty()
            boxes.append((w.spec.key, x0, y0, x0 + w.winfo_width(), y0 + w.winfo_height()))
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                getrennt = a[3] <= b[1] or b[3] <= a[1] or a[4] <= b[2] or b[4] <= a[2]
                self.assertTrue(getrennt, f"Überlappung {a} / {b}")

    def test_multi_span_geometrie_retention_und_reflow(self):
        """T344-Erweiterung: span=2 belegt zwei Spalten, Resize behält Widgets, kein Dauer-Reflow."""
        grid = BentoGrid(self.host_window, context=self.context)
        grid.pack(fill="both", expand=True)
        specs = [BentoCardSpec("A", span=2, weight=3), BentoCardSpec("B", weight=2), BentoCardSpec("C", weight=1),
                 BentoCardSpec("F", span="full"), BentoCardSpec("D"), BentoCardSpec("E"), BentoCardSpec("G")]
        cards = {}
        for spec in specs:
            card = BentoCard(grid, context=self.context, title=spec.key, spec=spec)
            tk.Label(card.body, text="Zeile\nZeile", bg=card.fill_color).pack()
            grid.add_card(card)
            cards[spec.key] = card
        identitaet = {k: str(v) for k, v in cards.items()}
        for breite, spalten in ((1100, 3), (750, 2), (500, 1), (1100, 3), (750, 2)):
            self.host_window.geometry(f"{breite}x900")
            self.host_window.update()
            grid.reflow()
            self.host_window.update()
            self.assertEqual(grid.current_columns, spalten, breite)
            self.assert_rechtecke_disjunkt(list(cards.values()))
            if spalten == 3:
                a, b = cards["A"], cards["B"]
                self.assertGreater(a.winfo_width(), b.winfo_width() * 1.6)
                self.assertLessEqual(a.winfo_rootx() + a.winfo_width(), b.winfo_rootx())
            if spalten >= 2:
                self.assertGreaterEqual(cards["F"].winfo_width(), grid.winfo_width() - 4)
        self.assertEqual(identitaet, {k: str(v) for k, v in cards.items()})
        self.assertTrue(all(v.winfo_exists() for v in cards.values()))
        laeufe = grid.layout_runs
        for _ in range(5):
            grid.reflow()
            self.host_window.update()
        self.assertEqual(grid.layout_runs, laeufe, "unveränderter Plan darf nicht neu platzieren")
        # Abbau: ausstehender Auftrag wird freigegeben
        grid.schedule_layout()
        grid.destroy()
        self.host_window.update()


if __name__ == "__main__":
    unittest.main()
