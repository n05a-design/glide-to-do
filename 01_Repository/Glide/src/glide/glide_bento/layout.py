# SPDX-License-Identifier: MPL-2.0
"""Bento Layout Planner – Tk-freie, deterministische Layoutberechnung.

Berechnet Spaltenanzahl, Spaltenbreiten und Kartenplatzierung rein mathematisch
vor der eigentlichen Widget-Darstellung (D100, D102). Vollständig unabhängig
von Tkinter und grafischen Bibliotheken.
"""
from typing import Sequence


def effective_span(card: BentoCardSpec, column_count: int) -> int:
    """Tatsächlich belegte Spalten einer Karte im Raster mit ``column_count`` Spalten.

    Vollbreite belegt alle Spalten, ``span=2`` höchstens die vorhandenen
    (im Zweispaltenraster also die volle Breite), alles andere eine Spalte.
    """
    requested = card.requested_span
    if requested is None:
        return column_count
    return max(1, min(column_count, requested))

from .specs import BentoBand, BentoCardSpec, BentoGridSpec, BentoLane, BentoLayoutPlan
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

        # 1. Trennung sichtbar vs. ausgeblendet; doppelte Schlüssel verwerfen
        issues: list[str] = []
        seen: set[str] = set()
        visible_cards = []
        for card in cards:
            if card.key in seen:
                issues.append(f"duplicate key {card.key!r} ignored")
                continue
            seen.add(card.key)
            if not card.span_is_valid:
                issues.append(f"unknown span {card.span!r} for {card.key!r} treated as 1")
            if card.visible:
                visible_cards.append(card)
        hidden_cards = tuple(c for c in cards if not c.visible)

        # Sortierung nach Order-Index erhalten (stabil: gleiche Order behält Eingabefolge)
        visible_cards.sort(key=lambda c: c.order)

        # 2. Vollbreitenkarten (Header/Top) vs. Spaltenkarten (0.1.0-Projektion)
        header_cards = [c for c in visible_cards if c.is_full_width]
        column_cards = [c for c in visible_cards if not c.is_full_width]

        # 3. Greedy-Verteilung auf Spalten (kürzeste Spalte nach kumuliertem Gewicht)
        columns: list[list[BentoCardSpec]] = [[] for _ in range(col_count)]
        weights = [0] * col_count

        for card in column_cards:
            target_idx = min(range(col_count), key=lambda idx: weights[idx])
            columns[target_idx].append(card)
            weights[target_idx] += max(1, card.weight)

        bands = self.plan_bands(visible_cards, col_count, spec.full_width_first)

        return BentoLayoutPlan(
            column_count=col_count,
            available_width=usable_w,
            column_width=col_width,
            gap=gap,
            header_cards=tuple(header_cards),
            columns=tuple(tuple(col) for col in columns),
            column_weights=tuple(weights),
            hidden_cards=hidden_cards,
            bands=bands,
            issues=tuple(issues),
        )

    @staticmethod
    def _flow_band(cards: Sequence[BentoCardSpec], col_count: int) -> BentoBand:
        lanes: list[list[BentoCardSpec]] = [[] for _ in range(col_count)]
        weights = [0] * col_count
        for card in cards:
            target = min(range(col_count), key=lambda idx: weights[idx])
            lanes[target].append(card)
            weights[target] += max(1, card.weight)
        return BentoBand("flow", tuple(BentoLane(idx, 1, tuple(lane), weights[idx])
                                       for idx, lane in enumerate(lanes)))

    def plan_bands(
        self,
        cards: Sequence[BentoCardSpec],
        column_count: int,
        full_width_first: bool = False,
    ) -> tuple[BentoBand, ...]:
        """Bandmodell (Bento 0.2.0) für bereits sichtbare, sortierte Karten.

        Regeln in Lesereihenfolge:
        1. Eine Karte über alle Spalten bildet ein eigenes Band ``full``.
        2. Einspaltige Karten sammeln sich in einem Band ``flow``; jede Karte
           kommt in die Bahn mit dem kleinsten Gewicht (Gleichstand: links).
        3. Eine Karte mit ``span=2`` im Dreispaltenraster öffnet ein Band
           ``split``: Sie belegt zwei Spalten (``extra["align"] == "end"``:
           rechts), daneben füllen die nächsten einspaltigen Karten die freie
           Spalte, bis deren Gewicht das der breiten Karte erreicht. Bleibt
           die freie Spalte leer, wird die Karte zur vollen Breite (keine Lücke).
        4. ``full_width_first`` stellt alle Vollbreitenkarten wie in 0.1.0 vor
           das übrige Raster.
        Bahnen eines Bands belegen getrennte Spalten, Bänder liegen
        untereinander: Überlappung ist ausgeschlossen.
        """
        col_count = max(1, min(3, int(column_count)))
        cards = list(cards)
        bands: list[BentoBand] = []
        if full_width_first:
            for card in cards:
                if card.is_full_width:
                    bands.append(BentoBand("full", (BentoLane(0, col_count, (card,), max(1, card.weight)),)))
            cards = [card for card in cards if not card.is_full_width]

        flow: list[BentoCardSpec] = []
        split: dict | None = None

        def flush_flow() -> None:
            if flow:
                bands.append(self._flow_band(flow, col_count))
                flow.clear()

        def close_split() -> None:
            nonlocal split
            if split is None:
                return
            wide = split["wide"]
            if not split["side"]:
                bands.append(BentoBand("full", (BentoLane(0, col_count, (wide,), max(1, wide.weight)),)))
            else:
                wide_column, side_column = (1, 0) if split["end"] else (0, 2)
                wide_lane = BentoLane(wide_column, 2, (wide,), max(1, wide.weight))
                side_lane = BentoLane(side_column, 1, tuple(split["side"]), split["side_weight"])
                lanes = (side_lane, wide_lane) if split["end"] else (wide_lane, side_lane)
                bands.append(BentoBand("split", lanes))
            split = None

        for card in cards:
            span = effective_span(card, col_count)
            if span >= col_count and (col_count > 1 or card.is_full_width):
                close_split()
                flush_flow()
                bands.append(BentoBand("full", (BentoLane(0, col_count, (card,), max(1, card.weight)),)))
            elif span == 1:
                if split is not None and split["side_weight"] < max(1, split["wide"].weight):
                    split["side"].append(card)
                    split["side_weight"] += max(1, card.weight)
                    continue
                close_split()
                flow.append(card)
            else:  # span == 2 im Dreispaltenraster
                close_split()
                flush_flow()
                split = {"wide": card, "side": [], "side_weight": 0,
                         "end": card.extra.get("align") == "end"}
        close_split()
        flush_flow()
        return tuple(bands)
