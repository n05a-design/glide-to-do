# SPDX-License-Identifier: MPL-2.0
"""Bento Design Tokens – semantische Gestaltungsskalen ohne Anwendungsfachlogik.

Leitet neutrale Tokens aus den bewährten Skalen von Glide ab (D100, D102).
Das Modul importiert weder Glide-Fachmodule noch Tkinter und bleibt unabhängig
von globalen Anwendungszuständen.
"""
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

# Grundlegende Skalen (abgeleitet aus ui_design.py und den bestehenden Glide-Maßen)
_SPACING_SCALE = MappingProxyType({
    val: val for val in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 22, 24, 28, 30)
})

_RADII_SCALE = MappingProxyType({
    "card": 18,
    "field": 16,
    "badge": 8,
    "button": 10,
    "pill": 999,
})

_FONT_SIZES_SCALE = MappingProxyType({
    "caption": 9,
    "small": 10,
    "body": 12,
    "subtitle": 13,
    "section": 16,
    "title": 22,
})

_ROW_HEIGHTS_SCALE = MappingProxyType({
    "task": 36,
    "compact": 28,
    "action": 40,
})


@dataclass(frozen=True, slots=True)
class BentoTokens:
    """Unveränderliche semantische Design-Tokens für Bento-Komponenten und Layouts."""

    # Layout- und Rasterabstände
    gap_compact: int = _SPACING_SCALE[8]        # 8 px
    gap_default: int = _SPACING_SCALE[12]       # 12 px (HOME_CARD_GAP)
    gap_relaxed: int = _SPACING_SCALE[16]       # 16 px (HOME_TILE_GAP)
    grid_margin: int = _SPACING_SCALE[16]       # 16 px Außenabstand

    # Karten-Innenabstände (Padding)
    card_padding_x: int = _SPACING_SCALE[18]    # 18 px (HOME_CARD_PAD_X)
    card_padding_y: int = _SPACING_SCALE[15]    # 15 px (HOME_CARD_PAD_Y)
    card_compact_padding_x: int = _SPACING_SCALE[12]  # 12 px
    card_compact_padding_y: int = _SPACING_SCALE[10]  # 10 px

    # Radien
    card_radius: int = _RADII_SCALE["card"]     # 18 px
    field_radius: int = _RADII_SCALE["field"]   # 16 px
    badge_radius: int = _RADII_SCALE["badge"]   # 8 px
    button_radius: int = _RADII_SCALE["button"] # 10 px

    # Rahmen & Kontur
    border_width: int = 1
    focus_width: int = 2

    # Kopf- und Inhaltsstrukturen
    header_gap: int = _SPACING_SCALE[8]         # 8 px Abstand Header zu Body
    header_icon_gap: int = _SPACING_SCALE[6]    # 6 px Abstand Icon zu Titel
    footer_gap: int = _SPACING_SCALE[8]         # 8 px Abstand Body zu Footer
    icon_size: int = 16                         # Standard-Icongröße in px
    action_button_height: int = 32              # Standard-Aktionshöhe
    dialog_button_height: int = 40              # Standard-Knopfhöhe (Dialog/Home)

    # Layout-Grenzwerte und Spaltenbildung
    card_min_width: int = 300                   # HOME_TILE_MIN_WIDTH (300 px)
    two_column_min_width: int = 616             # 300 * 2 + 16 (HOME_TWO_COLUMN_WIDTH)
    three_column_min_width: int = 932           # 300 * 3 + 16 * 2 (HOME_THREE_COLUMN_WIDTH)

    # Typografie-Größen
    font_size_caption: int = _FONT_SIZES_SCALE["caption"]    # 9
    font_size_small: int = _FONT_SIZES_SCALE["small"]        # 10
    font_size_body: int = _FONT_SIZES_SCALE["body"]          # 12
    font_size_subtitle: int = _FONT_SIZES_SCALE["subtitle"]  # 13
    font_size_title: int = _FONT_SIZES_SCALE["section"]      # 16
    font_size_headline: int = _FONT_SIZES_SCALE["title"]     # 22

    # Zeilenhöhen
    row_height_task: int = _ROW_HEIGHTS_SCALE["task"]        # 36 px
    row_height_compact: int = _ROW_HEIGHTS_SCALE["compact"]  # 28 px

    # Textbegrenzungen (B11 / P5)
    title_max_chars: int = 40
    button_text_max_chars: int = 24

    # Host-Overrides
    custom: Mapping[str, int | str] = field(default_factory=dict)

    def with_overrides(self, **kwargs) -> "BentoTokens":
        """Erzeugt eine Kopie mit gezielt überschriebenen Token-Werten."""
        fields = {k: getattr(self, k) for k in self.__slots__}
        fields.update(kwargs)
        return BentoTokens(**fields)

    @classmethod
    def field_names(cls) -> tuple[str, ...]:
        """Alle ganzzahligen Token-Namen des Vertrags (ohne ``custom``)."""
        return tuple(name for name in cls.__slots__ if name != "custom")

    @classmethod
    def from_host(
        cls,
        values: Mapping[str, object] | None,
        base: "BentoTokens | None" = None,
        strict: bool = False,
    ) -> "BentoTokens":
        """Host-Context-Token-Vertrag (Variante C, Bento 0.2.0).

        Der Host übergibt seine aktiven Skalen als Mapping. Bekannte Namen
        ersetzen den Fallback, unbekannte landen unverändert in ``custom``.
        Werte müssen nichtnegative ganze Zahlen sein; ungültige Werte werden
        übergangen (``strict=True``: ``ValueError``). Fehlen die Schwellen für
        zwei und drei Spalten, folgen sie aus Mindestbreite und Abstand.
        """
        base = base or DEFAULT_TOKENS
        if not values:
            return base
        known = set(cls.field_names())
        overrides: dict[str, int] = {}
        custom = dict(base.custom)
        for name, value in values.items():
            if name not in known:
                custom[name] = value
                continue
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                if strict:
                    raise ValueError(f"Bento token {name!r} needs a non-negative int, got {value!r}")
                continue
            overrides[name] = value
        min_w = overrides.get("card_min_width", base.card_min_width)
        gap = overrides.get("gap_relaxed", base.gap_relaxed)
        overrides.setdefault("two_column_min_width", min_w * 2 + gap)
        overrides.setdefault("three_column_min_width", min_w * 3 + gap * 2)
        overrides["custom"] = MappingProxyType(custom)
        return base.with_overrides(**overrides)


# Globale Standard-Instanz
DEFAULT_TOKENS = BentoTokens()
