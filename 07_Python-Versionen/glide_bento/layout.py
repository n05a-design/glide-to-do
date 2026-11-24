# SPDX-License-Identifier: MPL-2.0
"""Bento Layout Planner – Tk-freie, deterministische Layoutberechnung.

Berechnet Spaltenanzahl, Spaltenbreiten und Kartenplatzierung rein mathematisch
vor der eigentlichen Widget-Darstellung (D100, D102). Vollständig unabhängig
von Tkinter und grafischen Bibliotheken.
"""
from typing import Sequence

from .specs import BentoCardSpec, BentoGridSpec, BentoLayoutPlan
from .tokens import BentoTokens, DEFAULT_TOKENS


class BentoLayoutPlanner:
    """Berechnet deterministische Rasteranordnungen für Bento-Karten."""

    def __init__(self, tokens: BentoTokens = DEFAULT_TOKENS):
        self.tokens = tokens

    def compute_column_count(
        self,
        available_width: int,
        grid_spec: BentoGridSpec | None = None,
    ) -> int:
        """Ermittelt die Anzahl der Spalten anhand der gemessenen Breite."""
        if grid_spec and isinstance(grid_spec.columns, int) and grid_spec.columns > 0:
            return min(3, max(1, grid_spec.columns))

        min_w = (grid_spec.card_min_width if grid_spec and grid_spec.card_min_width else self.tokens.card_min_width)
        gap = (grid_spec.gap if grid_spec and grid_spec.gap is not None else self.tokens.gap_relaxed)

        two_col_threshold = min_w * 2 + gap
        three_col_threshold = min_w * 3 + gap * 2

        if available_width >= three_col_threshold:
            return 3
        if available_width >= two_col_threshold:
            return 2
        return 1

    def plan(
        self,
        available_width: int,
        cards: Sequence[BentoCardSpec],
        grid_spec: BentoGridSpec | None = None,
        column_count: int | None = None,
    ) -> BentoLayoutPlan:
        """Erstellt einen vollständigen Layoutplan für eine Menge von Kartenspezifikationen."""
        spec = grid_spec or BentoGridSpec()
        if column_count is not None:
            col_count = min(3, max(1, column_count))
        else:
            col_count = self.compute_column_count(available_width, spec)
        gap = spec.gap if spec.gap is not None else self.tokens.gap_relaxed
        card_gap = self.tokens.gap_default

        # Spaltenbreite berechnen
        usable_w = max(1, available_width)
        total_gaps = max(0, col_count - 1) * gap
        col_width = max(1, (usable_w - total_gaps) // col_count)

        # 1. Trennung sichtbar vs. ausgeblendet
        visible_cards = [c for c in cards if c.visible]
        hidden_cards = tuple(c for c in cards if not c.visible)

        # Sortierung nach Order-Index erhalten
        visible_cards.sort(key=lambda c: c.order)

        # 2. Vollbreitenkarten (Header/Top) vs. Spaltenkarten
        header_cards = [c for c in visible_cards if c.is_full_width]
        column_cards = [c for c in visible_cards if not c.is_full_width]

        # 3. Greedy-Verteilung auf Spalten (kürzeste Spalte nach kumuliertem Gewicht)
        columns: list[list[BentoCardSpec]] = [[] for _ in range(col_count)]
        weights = [0] * col_count

        for card in column_cards:
            target_idx = min(range(col_count), key=lambda idx: weights[idx])
            columns[target_idx].append(card)
            weights[target_idx] += max(1, card.weight)

        return BentoLayoutPlan(
            column_count=col_count,
            available_width=usable_w,
            column_width=col_width,
            gap=gap,
            header_cards=tuple(header_cards),
            columns=tuple(tuple(col) for col in columns),
            column_weights=tuple(weights),
            hidden_cards=hidden_cards,
        )
