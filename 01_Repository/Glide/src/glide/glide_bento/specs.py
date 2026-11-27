# SPDX-License-Identifier: MPL-2.0
"""Bento Spezifikationen und Datenklassen.

Definiert reine Datenträger für Kartenspezifikationen, Rastereinstellungen
und berechnete Layoutpläne. Frei von GUI- und Tk-Abhängigkeiten (D100, D102).
"""
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence


@dataclass(slots=True)
class BentoCardSpec:
    """Spezifikation einer einzelnen Bento-Karte für Layout und Rendering."""

    key: str
    title: str | None = None
    subtitle: str | None = None
    icon: Any | None = None
    variant: str = "standard"               # "standard", "compact", "wide", "tall", "featured", "full_width"
    span: int | str = "auto"                # 1, 2, 3, "col", "double", "full", "wide", "auto" (0.2.0: 2/"double" echt zweispaltig)
    weight: int = 2                         # Gewicht/Höhenschätzung für Greedy-Verteilung
    order: int = 0                          # Reihenfolge-Index
    visible: bool = True                    # Sichtbarkeit
    heading_action: tuple[str, Callable, str] | None = None  # (Beschriftung, Callback, Farbrolle)
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def card_id(self) -> str:
        """Alias für key zur flexiblen Nutzung als Kartenidentifikator."""
        return self.key

    @property
    def is_full_width(self) -> bool:
        """Prüft, ob die Karte die gesamte Rasterbreite beansprucht."""
        return (
            self.variant in ("full_width", "wide")
            or self.span in ("full", "wide", 3)
            or self.extra.get("full_width", False)
        )


    @property
    def requested_span(self) -> int | None:
        """Angeforderte Spaltenzahl (Bento 0.2.0): 1, 2 oder None für volle Breite.

        Unbekannte oder ungültige Werte gelten als eine Spalte; der Planner
        meldet sie in ``BentoLayoutPlan.issues``.
        """
        if self.is_full_width:
            return None
        span = self.span
        if span in (2, "2", "double", "two"):
            return 2
        return 1

    @property
    def span_is_valid(self) -> bool:
        """Ob ``span`` einen dokumentierten Wert trägt."""
        return self.span in (1, 2, 3, "1", "2", "3", "auto", "single", "col", "double", "two",
                             "full", "wide") or self.is_full_width


@dataclass(frozen=True, slots=True)
class BentoGridSpec:
    """Konfiguration für ein BentoGrid-Raster."""

    columns: int | str = "auto"             # "auto" oder 1, 2, 3 feste Spalten
    gap: int | None = None                  # Abstand zwischen Karten (None = Token-Vorgabe)
    margin: int | None = None               # Außenabstand (None = Token-Vorgabe)
    card_min_width: int | None = None       # Mindestbreite einer Spalte
    uniform_columns: bool = True            # Gleichmäßige Spaltenbreiten erzwingen
    full_width_first: bool = False          # 0.1.0-Verhalten: Vollbreitenkarten über dem Raster sammeln


@dataclass(frozen=True, slots=True)
class BentoLane:
    """Senkrechter Stapel von Karten über ``span`` Spalten ab ``column`` (0.2.0)."""

    column: int
    span: int
    cards: tuple[BentoCardSpec, ...]
    weight: int


@dataclass(frozen=True, slots=True)
class BentoBand:
    """Waagerechtes Band des Rasters; seine Bahnen überlappen sich nie (0.2.0).

    ``kind``: ``"full"`` (eine Karte über alle Spalten), ``"flow"`` (eine Bahn
    je Spalte, gierig nach Gewicht befüllt) oder ``"split"`` (eine
    zweispaltige Bahn neben einer einspaltigen im Dreispaltenraster).
    """

    kind: str
    lanes: tuple[BentoLane, ...]

    @property
    def weight(self) -> int:
        return max((lane.weight for lane in self.lanes), default=0)

    @property
    def cards(self) -> tuple[BentoCardSpec, ...]:
        return tuple(card for lane in self.lanes for card in lane.cards)


@dataclass(frozen=True, slots=True)
class BentoLayoutPlan:
    """Ergebnis des Tk-freien Layout-Planners."""

    column_count: int
    available_width: int
    column_width: int
    gap: int
    header_cards: tuple[BentoCardSpec, ...]
    columns: tuple[tuple[BentoCardSpec, ...], ...]
    column_weights: tuple[int, ...]
    hidden_cards: tuple[BentoCardSpec, ...]
    # Bento 0.2.0: Bandmodell mit echten Mehrspaltenkarten. ``header_cards``,
    # ``columns`` und ``column_weights`` bleiben als 0.1.0-Projektion erhalten
    # (Vollbreitenkarten oben, alle übrigen Karten einspaltig).
    bands: tuple[BentoBand, ...] = ()
    issues: tuple[str, ...] = ()

    @property
    def total_visible_cards(self) -> int:
        return len(self.header_cards) + sum(len(col) for col in self.columns)

    def lane_width(self, span: int) -> int:
        """Pixelbreite einer Bahn über ``span`` Spalten einschließlich innerer Abstände."""
        span = max(1, min(self.column_count, int(span)))
        return self.column_width * span + self.gap * (span - 1)

    def placements(self) -> tuple[tuple[str, int, int, int, int], ...]:
        """(key, band, column, span, position) je sichtbarer Karte in Bandreihenfolge."""
        result = []
        for band_index, band in enumerate(self.bands):
            for lane in band.lanes:
                for position, card in enumerate(lane.cards):
                    result.append((card.key, band_index, lane.column, lane.span, position))
        return tuple(result)
