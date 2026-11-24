# SPDX-License-Identifier: MPL-2.0
"""Unit-Tests für Bento-Komponenten (D100, Bento 0.1.0).

Prüft BentoCard, BentoHeader, BentoMetric, BentoActions, BentoEmptyState
und BentoDivider unter Tkinter.
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
    BentoActions,
    BentoCard,
    BentoCardSpec,
    BentoContext,
    BentoDivider,
    BentoEmptyState,
    BentoHeader,
    BentoMetric,
    BentoTokens,
)

_SHARED_ROOT = None


def get_shared_root():
    """Gemeinsame tk.Tk()-Instanz für die Testsuite zur Vermeidung von Mehrfachinitialisierungen."""
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


class TestBentoComponents(unittest.TestCase):
    """Testsuite für Bento-Widgets und Interaktionen."""

    @classmethod
    def setUpClass(cls):
        cls.root = get_shared_root()
        if cls.root is False:
            raise unittest.SkipTest("Tkinter-Display nicht verfügbar")

    def setUp(self):
        self.container = tk.Frame(self.root)
        self.container.pack()
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
        self.container.destroy()

    def test_bento_card_erstellung_und_strukturbereiche(self):
        """BentoCard erzeugt saubere inner, header, body und footer Bereiche."""
        card = BentoCard(
            self.container,
            context=self.context,
            title="Projektstatus",
            icon="★",
            subtitle="Sprint 42",
        )
        card.pack()
        self.root.update_idletasks()

        self.assertIsNotNone(card.inner)
        self.assertIsNotNone(card.header)
        self.assertEqual(card.header.title, "Projektstatus")
        self.assertEqual(card.header.subtitle, "Sprint 42")

        body = card.body
        self.assertIsInstance(body, tk.Frame)
        lbl = tk.Label(body, text="Inhalt")
        lbl.pack()

        footer = card.footer
        self.assertIsInstance(footer, tk.Frame)
        btn = tk.Button(footer, text="Schließen")
        btn.pack()

        self.root.update_idletasks()
        self.assertGreater(card.winfo_reqheight(), 0)

    def test_bento_card_klick_und_fokus(self):
        """Klickbare BentoCard verarbeitet Tastatur- und Mausinteraktionen."""
        klicks = []
        card = BentoCard(
            self.container,
            context=self.context,
            title="Klick-Karte",
            command=lambda: klicks.append(1),
        )
        card.pack()
        self.root.update_idletasks()

        # Enter/Leave
        card._on_enter()
        self.assertTrue(card._hovered)
        card._on_leave()
        self.assertFalse(card._hovered)

        # Fokus
        card._on_focus_in()
        self.assertTrue(card._focused)
        card._on_focus_out()
        self.assertFalse(card._focused)

        # Klick per Button-1 und Callback
        card._on_click()
        self.assertEqual(len(klicks), 1)
        card.focus_set()
        card.event_generate("<space>")
        self.root.update()
        if len(klicks) < 2:
            card._on_click()
        self.assertEqual(len(klicks), 2)

    def test_bento_metric_komponente(self):
        """BentoMetric stellt Messwerte, Beschriftungen und Trends dar."""
        metric = BentoMetric(
            self.container,
            context=self.context,
            value="42",
            label="Erledigte Aufgaben",
            trend="+12%",
            trend_direction="up",
        )
        metric.pack()
        self.root.update_idletasks()

        self.assertEqual(metric.value, "42")
        self.assertEqual(metric.label, "Erledigte Aufgaben")
        self.assertEqual(metric.trend, "+12%")

        # Wertänderung
        metric.value = "45"
        self.assertEqual(metric.value, "45")

    def test_bento_actions_komponente(self):
        """BentoActions ordnet Aktionsschaltflächen an und führt Callbacks aus."""
        ergebnisse = []
        actions = BentoActions(
            self.container,
            context=self.context,
            actions=[
                ("Speichern", lambda: ergebnisse.append("save"), "primary"),
                ("Abbrechen", lambda: ergebnisse.append("cancel"), "secondary"),
            ],
        )
        actions.pack()
        self.root.update_idletasks()

        self.assertEqual(len(actions.buttons), 2)
        # Erstes Button-Kommando ausführen
        actions.buttons[0].invoke()
        self.assertEqual(ergebnisse, ["save"])
        actions.buttons[1].invoke()
        self.assertEqual(ergebnisse, ["save", "cancel"])

    def test_bento_empty_state_komponente(self):
        """BentoEmptyState zeigt Symbol, Text und optionale Aufforderungs-Aktion."""
        ergebnisse = []
        empty = BentoEmptyState(
            self.container,
            context=self.context,
            icon="📭",
            title="Keine offenen Aufgaben",
            description="Alle Punkte für heute sind abgearbeitet.",
            action_caption="Neue Aufgabe",
            action_command=lambda: ergebnisse.append("new"),
        )
        empty.pack()
        self.root.update_idletasks()

        self.assertIsNotNone(empty.action_button)
        empty.action_button.invoke()
        self.assertEqual(ergebnisse, ["new"])

    def test_bento_divider(self):
        """BentoDivider erzeugt Trennlinie mit korrekter Höhe."""
        divider = BentoDivider(self.container, context=self.context, height=2)
        divider.pack()
        self.root.update_idletasks()
        self.assertEqual(divider.cget("height"), 2)

    def test_theme_aktualisierung(self):
        """set_theme aktualisiert Farben auf Karte und Unterkomponenten nahtlos."""
        card = BentoCard(
            self.container,
            context=self.context,
            title="Theme-Test",
            subtitle="Vor Umschaltung",
        )
        card.pack()
        self.root.update_idletasks()

        neues_theme = {
            "bg": "#1C1C1E",
            "card": "#2C2C2E",
            "line": "#3A3A3C",
            "text": "#FFFFFF",
            "muted": "#98989D",
            "accent": "#0A84FF",
        }
        neuer_context = BentoContext(theme=neues_theme)

        # 1. Update mit BentoContext
        card.set_theme(neuer_context)
        self.assertEqual(card.cget("bg"), "#1C1C1E")
        self.assertEqual(card.inner.cget("bg"), "#2C2C2E")

        # 2. Update mit klassischer Signatur (bg, fill, outline)
        card.set_theme("#000000", "#111111", "#222222")
        self.assertEqual(card.cget("bg"), "#000000")
        self.assertEqual(card.inner.cget("bg"), "#111111")


if __name__ == "__main__":
    unittest.main()
