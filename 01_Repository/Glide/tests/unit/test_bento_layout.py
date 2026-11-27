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


class TestBentoMultiSpan(unittest.TestCase):
    """T342-Erweiterung (Bento 0.2.0): Bandmodell mit echten Mehrspaltenkarten."""

    def setUp(self):
        self.planner = BentoLayoutPlanner()

    @staticmethod
    def lanes(plan):
        return [(band.kind, [(lane.column, lane.span, [c.key for c in lane.cards]) for lane in band.lanes])
                for band in plan.bands]

    def assert_no_overlap(self, plan):
        keys = [key for key, *_rest in plan.placements()]
        self.assertEqual(len(keys), len(set(keys)), "Karte doppelt platziert")
        for band in plan.bands:
            used = set()
            for lane in band.lanes:
                cols = set(range(lane.column, lane.column + lane.span))
                self.assertFalse(used & cols, f"Bahnen überlappen in {band}")
                self.assertLess(max(cols), plan.column_count)
                used |= cols

    def test_spezifikationsbeispiel_drei_zwei_eine_spalte(self):
        """Konzept §10.2: A(span=2) neben B, darunter C D E; 2 Spalten: A voll; 1 Spalte: Stapel."""
        cards = [BentoCardSpec("A", span=2, weight=2), BentoCardSpec("B", weight=2),
                 BentoCardSpec("C"), BentoCardSpec("D"), BentoCardSpec("E")]
        self.assertEqual(self.lanes(self.planner.plan(1000, cards)), [
            ("split", [(0, 2, ["A"]), (2, 1, ["B"])]),
            ("flow", [(0, 1, ["C"]), (1, 1, ["D"]), (2, 1, ["E"])])])
        self.assertEqual(self.lanes(self.planner.plan(700, cards)), [
            ("full", [(0, 2, ["A"])]),
            ("flow", [(0, 1, ["B", "D"]), (1, 1, ["C", "E"])])])
        self.assertEqual(self.lanes(self.planner.plan(500, cards)), [
            ("flow", [(0, 1, ["A", "B", "C", "D", "E"])])])

    def test_breakpoint_grenzwerte(self):
        cards = [BentoCardSpec("A", span=2), BentoCardSpec("B")]
        for width, cols in ((615, 1), (616, 2), (931, 2), (932, 3)):
            plan = self.planner.plan(width, cards)
            self.assertEqual(plan.column_count, cols, width)
            self.assert_no_overlap(plan)
        self.assertEqual(self.planner.plan(931, cards).bands[0].kind, "full")
        self.assertEqual(self.planner.plan(932, cards).bands[0].kind, "split")

    def test_freie_spalte_fuellt_bis_gewicht(self):
        cards = [BentoCardSpec("W", span="double", weight=3), BentoCardSpec("s1", weight=1),
                 BentoCardSpec("s2", weight=1), BentoCardSpec("s3", weight=1), BentoCardSpec("s4", weight=1)]
        plan = self.planner.plan(1000, cards)
        self.assertEqual(self.lanes(plan)[0], ("split", [(0, 2, ["W"]), (2, 1, ["s1", "s2", "s3"])]))
        self.assertEqual(plan.bands[1].cards[0].key, "s4")

    def test_ausrichtung_rechts(self):
        cards = [BentoCardSpec("W", span=2, extra={"align": "end"}), BentoCardSpec("s")]
        self.assertEqual(self.lanes(self.planner.plan(1000, cards)),
                         [("split", [(0, 1, ["s"]), (1, 2, ["W"])])])

    def test_keine_restflaeche_ohne_nachbarn(self):
        """Ohne einspaltige Folgekarte wird die breite Karte zur vollen Breite statt eine Lücke zu lassen."""
        for cards in ([BentoCardSpec("W", span=2)],
                      [BentoCardSpec("W", span=2), BentoCardSpec("V", span=2), BentoCardSpec("s")]):
            plan = self.planner.plan(1000, cards)
            self.assertEqual(plan.bands[0].kind, "full")
            self.assert_no_overlap(plan)

    def test_vollbreite_bleibt_an_ihrer_stelle_oder_oben(self):
        cards = [BentoCardSpec("a"), BentoCardSpec("F", span="full"), BentoCardSpec("b")]
        self.assertEqual([b.kind for b in self.planner.plan(1000, cards).bands], ["flow", "full", "flow"])
        oben = self.planner.plan(1000, cards, BentoGridSpec(full_width_first=True))
        self.assertEqual([b.kind for b in oben.bands], ["full", "flow"])
        self.assertEqual(oben.bands[0].cards[0].key, "F")

    def test_ausgeblendete_und_fehlerhafte_karten(self):
        cards = [BentoCardSpec("a", span=2, visible=False), BentoCardSpec("b", span="quer"),
                 BentoCardSpec("b", span=2), BentoCardSpec("c", span=-4)]
        plan = self.planner.plan(1000, cards)
        self.assertEqual([k for k, *_ in plan.placements()], ["b", "c"])
        self.assertEqual([c.key for c in plan.hidden_cards], ["a"])
        self.assertEqual(len(plan.issues), 3)
        self.assert_no_overlap(plan)

    def test_determinismus_und_stabile_reihenfolge_ueber_resize_folgen(self):
        import random
        rng = random.Random(4711)
        spans = [1, 1, 1, 2, "full", "auto"]
        for _ in range(40):
            cards = [BentoCardSpec(f"k{i}", span=rng.choice(spans), weight=rng.randint(1, 5), order=rng.randint(0, 3))
                     for i in range(rng.randint(0, 12))]
            ordered = [c.key for c in sorted(cards, key=lambda c: c.order)]
            for width in (400, 700, 1000, 1400, 700, 400, 1000):
                plan = self.planner.plan(width, cards)
                self.assertEqual(plan.placements(), self.planner.plan(width, list(cards)).placements())
                self.assert_no_overlap(plan)
                placed = [k for k, *_ in plan.placements()]
                self.assertEqual(sorted(placed), sorted(ordered))
                # Lesereihenfolge: die erste Karte jedes Bands folgt der Order-Folge
                firsts = [min(ordered.index(c.key) for c in band.cards) for band in plan.bands if band.cards]
                self.assertEqual(firsts, sorted(firsts))

    def test_bahnbreite(self):
        plan = self.planner.plan(1000, [BentoCardSpec("W", span=2), BentoCardSpec("s")])
        self.assertEqual(plan.lane_width(2), plan.column_width * 2 + plan.gap)
        self.assertEqual(plan.lane_width(9), plan.lane_width(3))

    def test_alte_projektion_bleibt(self):
        """0.1.0-Felder header_cards/columns bleiben für bestehende Hosts unverändert."""
        cards = [BentoCardSpec("h", variant="full_width"), BentoCardSpec("W", span=2, weight=3), BentoCardSpec("s")]
        plan = self.planner.plan(1000, cards)
        self.assertEqual([c.key for c in plan.header_cards], ["h"])
        self.assertEqual(sum(len(col) for col in plan.columns), 2)


class TestBentoHostTokens(unittest.TestCase):
    """T342-Erweiterung: Host-Context-Token-Vertrag (Variante C)."""

    def test_fallback_ohne_host(self):
        from glide_bento import BentoContext
        self.assertIs(BentoTokens.from_host(None), DEFAULT_TOKENS)
        self.assertIs(BentoTokens.from_host({}), DEFAULT_TOKENS)
        self.assertEqual(BentoContext().tokens, DEFAULT_TOKENS)

    def test_injection_validierung_und_abgeleitete_schwellen(self):
        tokens = BentoTokens.from_host({"card_min_width": 280, "gap_relaxed": 20, "card_radius": True,
                                        "gap_default": "12", "host_only": 5})
        self.assertEqual(tokens.card_min_width, 280)
        self.assertEqual(tokens.two_column_min_width, 580)
        self.assertEqual(tokens.three_column_min_width, 880)
        self.assertEqual(tokens.card_radius, DEFAULT_TOKENS.card_radius)
        self.assertEqual(tokens.gap_default, DEFAULT_TOKENS.gap_default)
        self.assertEqual(tokens.custom["host_only"], 5)
        with self.assertRaises(ValueError):
            BentoTokens.from_host({"gap_default": -1}, strict=True)

    def test_kontext_liest_provider_neu(self):
        from glide_bento import BentoContext
        state = {"theme": {"card": "#111111"}, "tokens": {"card_radius": 10}}
        ctx = BentoContext.for_host(theme_provider=lambda: state["theme"], token_provider=lambda: state["tokens"])
        self.assertEqual((ctx.resolve_color("card_bg"), ctx.tokens.card_radius), ("#111111", 10))
        state["theme"] = {"card": "#222222"}
        state["tokens"] = {"card_radius": 14}
        same = ctx.refresh_from_host(glass_mode=True)
        self.assertIs(same, ctx)
        self.assertEqual((ctx.resolve_color("card_bg"), ctx.tokens.card_radius, ctx.glass_mode),
                         ("#222222", 14, True))
        clone = ctx.clone_with()
        self.assertIs(clone.token_provider, ctx.token_provider)
        with self.assertRaises(AttributeError):
            ctx.refresh_from_host(unbekannt=1)

    def test_planner_nutzt_host_schwellen(self):
        planner = BentoLayoutPlanner(BentoTokens.from_host({"card_min_width": 200, "gap_relaxed": 10}))
        self.assertEqual(planner.compute_column_count(410), 2)
        self.assertEqual(planner.compute_column_count(620), 3)


if __name__ == "__main__":
    unittest.main()
