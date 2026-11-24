# SPDX-License-Identifier: MPL-2.0
"""Unit-Tests für den deterministischen BentoLayoutPlanner (D100, D102).

Prüft Spaltenberechnung, Schwellenwerte, Greedy-Verteilung, Vollbreitenkarten,
Ausblendungen und Grenzwerte rein algorithmisch ohne Tkinter.
"""
from pathlib import Path
import sys
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from glide_bento import (
    BentoCardSpec,
    BentoGridSpec,
    BentoLayoutPlan,
    BentoLayoutPlanner,
    BentoTokens,
    DEFAULT_TOKENS,
)


class TestBentoLayout(unittest.TestCase):
    """Testsuite für die rein mathematische Layoutberechnung."""

    def setUp(self):
        self.tokens = DEFAULT_TOKENS
        self.planner = BentoLayoutPlanner(tokens=self.tokens)

    def test_schwellenwerte_berechnung(self):
        """Prüft exakte Pixel-Schwellenwerte für 1, 2 und 3 Spalten (B11, P4)."""
        # Formeln:
        # 2 Spalten: 300 * 2 + 16 = 616 px
        # 3 Spalten: 300 * 3 + 16 * 2 = 932 px
        grid_spec = BentoGridSpec(card_min_width=300, gap=16)

        # 1 Spalte
        self.assertEqual(self.planner.compute_column_count(0, grid_spec), 1)
        self.assertEqual(self.planner.compute_column_count(300, grid_spec), 1)
        self.assertEqual(self.planner.compute_column_count(615, grid_spec), 1)

        # 2 Spalten
        self.assertEqual(self.planner.compute_column_count(616, grid_spec), 2)
        self.assertEqual(self.planner.compute_column_count(800, grid_spec), 2)
        self.assertEqual(self.planner.compute_column_count(931, grid_spec), 2)

        # 3 Spalten
        self.assertEqual(self.planner.compute_column_count(932, grid_spec), 3)
        self.assertEqual(self.planner.compute_column_count(1400, grid_spec), 3)

    def test_feste_spaltenzahl_override(self):
        """Manuelle Spaltenwahl überstimmt die adaptive Breitenberechnung."""
        spec_1 = BentoGridSpec(columns=1)
        spec_2 = BentoGridSpec(columns=2)
        spec_3 = BentoGridSpec(columns=3)

        self.assertEqual(self.planner.compute_column_count(1500, spec_1), 1)
        self.assertEqual(self.planner.compute_column_count(300, spec_2), 2)
        self.assertEqual(self.planner.compute_column_count(400, spec_3), 3)

    def test_grenzwerte_und_ungueltige_eingaben(self):
        """Negative oder minimale Breiten müssen robust auf 1 Spalte fallen."""
        self.assertEqual(self.planner.compute_column_count(-50), 1)
        self.assertEqual(self.planner.compute_column_count(0), 1)
        self.assertEqual(self.planner.compute_column_count(1), 1)

    def test_leere_kartenmenge(self):
        """Ein Plan ohne Karten muss gültige Spalten ohne Einträge liefern."""
        plan = self.planner.plan(available_width=1000, cards=[])
        self.assertIsInstance(plan, BentoLayoutPlan)
        self.assertEqual(plan.column_count, 3)
        self.assertEqual(len(plan.header_cards), 0)
        self.assertEqual(len(plan.columns), 3)
        for col in plan.columns:
            self.assertEqual(len(col), 0)
        self.assertEqual(plan.total_visible_cards, 0)

    def test_einzelne_karte(self):
        """Eine einzelne Karte landet immer in Spalte 0."""
        card = BentoCardSpec(key="single", weight=2)
        plan = self.planner.plan(available_width=800, cards=[card])
        self.assertEqual(plan.column_count, 2)
        self.assertEqual(len(plan.columns[0]), 1)
        self.assertEqual(plan.columns[0][0].key, "single")
        self.assertEqual(len(plan.columns[1]), 0)

    def test_vollbreitenkarten_header_trennung(self):
        """Vollbreitenkarten landen im Header, normale Karten im Raster."""
        cards = [
            BentoCardSpec(key="head1", span="wide"),
            BentoCardSpec(key="c1", span="single", weight=1),
            BentoCardSpec(key="head2", variant="full_width"),
            BentoCardSpec(key="c2", span="single", weight=1),
        ]
        plan = self.planner.plan(available_width=700, cards=cards)
        self.assertEqual(len(plan.header_cards), 2)
        self.assertEqual([c.key for c in plan.header_cards], ["head1", "head2"])
        # 2 Spalten
        self.assertEqual(plan.column_count, 2)
        self.assertEqual(len(plan.columns[0]), 1)
        self.assertEqual(len(plan.columns[1]), 1)
        self.assertEqual(plan.columns[0][0].key, "c1")
        self.assertEqual(plan.columns[1][0].key, "c2")

    def test_deterministische_greedy_verteilung(self):
        """Greedy-Verteilung verteilt deterministisch nach kumuliertem Spaltengewicht."""
        cards = [
            BentoCardSpec(key="schwer", weight=4),
            BentoCardSpec(key="leicht1", weight=2),
            BentoCardSpec(key="leicht2", weight=2),
        ]
        # 2 Spalten:
        # Karte 1 (Gewicht 4) -> Spalte 0 (Gewichte: 4, 0)
        # Karte 2 (Gewicht 2) -> Spalte 1 (Gewichte: 4, 2)
        # Karte 3 (Gewicht 2) -> Spalte 1 (Gewichte: 4, 4)
        plan = self.planner.plan(available_width=700, cards=cards)
        self.assertEqual(plan.column_count, 2)
        self.assertEqual([c.key for c in plan.columns[0]], ["schwer"])
        self.assertEqual([c.key for c in plan.columns[1]], ["leicht1", "leicht2"])
        self.assertEqual(plan.column_weights, (4, 4))

    def test_reihenfolge_und_ausblendung(self):
        """Versteckte Karten werden aussortiert; sichtbare nach Order sortiert."""
        cards = [
            BentoCardSpec(key="c3", order=3, weight=1),
            BentoCardSpec(key="hidden", visible=False, weight=5),
            BentoCardSpec(key="c1", order=1, weight=1),
            BentoCardSpec(key="c2", order=2, weight=1),
        ]
        plan = self.planner.plan(available_width=400, cards=cards)
        self.assertEqual(plan.column_count, 1)
        self.assertEqual(len(plan.hidden_cards), 1)
        self.assertEqual(plan.hidden_cards[0].key, "hidden")
        self.assertEqual([c.key for c in plan.columns[0]], ["c1", "c2", "c3"])


if __name__ == "__main__":
    unittest.main()
