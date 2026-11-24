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
    span: int | str = "auto"                # 1, 2, 3, "col", "full", "auto"
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


@dataclass(frozen=True, slots=True)
class BentoGridSpec:
    """Konfiguration für ein BentoGrid-Raster."""

    columns: int | str = "auto"             # "auto" oder 1, 2, 3 feste Spalten
    gap: int | None = None                  # Abstand zwischen Karten (None = Token-Vorgabe)
    margin: int | None = None               # Außenabstand (None = Token-Vorgabe)
    card_min_width: int | None = None       # Mindestbreite einer Spalte
    uniform_columns: bool = True            # Gleichmäßige Spaltenbreiten erzwingen


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

    @property
    def total_visible_cards(self) -> int:
        return len(self.header_cards) + sum(len(col) for col in self.columns)
