# SPDX-License-Identifier: MPL-2.0
"""Mitgelieferte Textschriften und dauerhafte Stilzuordnung, ohne Tk.

Einstellungen und späteres Onboarding verwenden dieselben Kennungen.
Symbol- und Pixelschriften sind keine auswählbaren Textstile.
"""
from dataclasses import dataclass
import sys


@dataclass(frozen=True)
class FontStyle:
    key: str
    classification: str
    family: str
    tk_family: str
    regular: str
    bold: str
    body_family: str = ""
    body_regular: str = ""
    body_postscript: str = ""
    automatic_bold: bool = False
    aliases: tuple = ()

    @property
    def label(self):
        return f"{self.classification}: {self.family}"

    @property
    def default_family(self):
        return self.family_for_platform()

    def family_for_platform(self, platform=None):
        # AppKit gruppiert SemiBold unter der typografischen Stammfamilie.
        # Tk/macOS unterstützt dafür den eindeutigen PostScript-Schnittnamen.
        if (platform or sys.platform) == "darwin" and self.body_postscript:
            return self.body_postscript
        return self.body_family or self.tk_family


STYLES = (
    FontStyle("rubik", "Modern", "Rubik", "Rubik", "Rubik-Regular.ttf", "Rubik-Bold.ttf"),
    FontStyle("dm_mono", "Technisch", "DM Mono", "DM Mono",
              "DMMono-Regular.ttf", "DMMono-Medium.ttf",
              aliases=("roboto_mono", "Roboto Mono")),
    FontStyle("dm_serif_display", "Kreativ", "DM Serif Display", "DM Serif Display",
              "DMSerifDisplay-Regular.ttf", "DMSerifDisplay-Regular.ttf",
              automatic_bold=True, aliases=("playfair_display", "Playfair Display")),
    FontStyle("charis_sil", "Klassisch", "Charis SIL", "Charis SIL",
              "CharisSIL-Regular.ttf", "CharisSIL-Bold.ttf",
              automatic_bold=True, aliases=("fraunces", "Fraunces")),
)
DEFAULT = STYLES[0]
LABELS = tuple(style.label for style in STYLES)


def style_for(value):
    """Anzeige, stabile Kennung und bisher gespeicherte Familien zuordnen.

    Ausgewählte Familien behalten nach einem Fontwechsel ihre Stilklasse.
    Leere oder unbekannte Werte folgen der aktuellen Vorgabe.
    """
    key = str(value or "").strip().casefold()
    return next((style for style in STYLES
                 if key in {style.key.casefold(), style.family.casefold(),
                            style.tk_family.casefold(), style.body_family.casefold(),
                            style.body_postscript.casefold(), (style.body_postscript + "Italic").casefold(),
                            style.label.casefold(),
                            *(str(alias).casefold() for alias in style.aliases)}), DEFAULT)


def family_for_weight(family, bold=False, italic=False, platform=None):
    """Resolve style aliases while preserving the requested Tk weight.

    Tk exposes normal/bold rather than arbitrary font weights. DM Mono maps
    its bold request to the bundled Medium face; fonts without a bold face use
    Tk's weight selection from their regular family.
    """
    key = str(family or "").casefold()
    style = next((style for style in STYLES
                  if key and key in {style.tk_family.casefold(), style.body_family.casefold(),
                                     style.body_postscript.casefold(),
                                     (style.body_postscript + "Italic").casefold(),
                                     *(str(alias).casefold() for alias in style.aliases)}), None)
    if style is None:
        return family
    chosen = style.tk_family if bold else style.family_for_platform(platform)
    if not bold and italic and (platform or sys.platform) == "darwin" and style.body_postscript:
        chosen += "Italic"
    return chosen


def actual_family(family, platform=None):
    """Native Stammfamilie für AppKit- und Fontconfig-Schnittnamen."""
    native = platform or sys.platform
    if native in ("darwin", "linux"):
        key = str(family or "").casefold()
        for style in STYLES:
            names = ((style.body_postscript, style.body_postscript + "Italic") if native == "darwin"
                     else (style.body_family,))
            names = (*names, *(str(alias) for alias in style.aliases))
            if key and key in {name.casefold() for name in names}:
                return style.tk_family
    return family


def face_options(description, platform=None):
    """Preserve a resolved Tk face when reconstructing a font tuple.

    AppKit and Fontconfig may report a base family for a resolved face; this
    recreates the original family, weight, and slant instead of losing them.
    Named and ordinary fonts remain on Tk's normal path.
    """
    native = platform or sys.platform
    if native not in ("darwin", "linux") or len(description) < 2:
        return None
    family = description[0]
    if actual_family(family, native) == family:
        return None
    styles = " ".join(str(value) for value in description[2:]).split()
    return {"family": family, "size": int(description[1]),
            "weight": "bold" if "bold" in styles else "normal",
            "slant": "italic" if "italic" in styles else "roman",
            "underline": int("underline" in styles), "overstrike": int("overstrike" in styles)}
