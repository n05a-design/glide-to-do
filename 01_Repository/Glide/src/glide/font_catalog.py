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
    FontStyle("roboto_mono", "Technisch", "Roboto Mono", "Roboto Mono",
              "RobotoMono-Regular.ttf", "RobotoMono-Bold.ttf"),
    FontStyle("playfair_display", "Kreativ", "Playfair Display", "Playfair Display",
              "PlayfairDisplay-Regular.ttf", "PlayfairDisplay-Bold.ttf",
              "Playfair Display SemiBold", "PlayfairDisplay-SemiBold.ttf", "PlayfairDisplay-SemiBold"),
    FontStyle("fraunces", "Klassisch", "Fraunces", "Fraunces 72pt",
              "Fraunces_72pt-Regular.ttf", "Fraunces_72pt-Bold.ttf",
              "Fraunces 72pt SemiBold", "Fraunces_72pt-SemiBold.ttf", "Fraunces72pt-SemiBold"),
)
DEFAULT = STYLES[0]
LABELS = tuple(style.label for style in STYLES)


def style_for(value):
    """Anzeige, stabile Kennung und alte Familienangaben eindeutig zuordnen.

    Leere oder nicht mehr angebotene Familien folgen der aktuellen Vorgabe.
    Die native Fraunces-Familie bleibt ein Alias der öffentlichen Bezeichnung.
    """
    key = str(value or "").strip().casefold()
    return next((style for style in STYLES
                 if key in {style.key.casefold(), style.family.casefold(),
                            style.tk_family.casefold(), style.body_family.casefold(),
                            style.body_postscript.casefold(), (style.body_postscript + "Italic").casefold(),
                            style.label.casefold()}), DEFAULT)


def family_for_weight(family, bold=False, italic=False, platform=None):
    """SemiBold für Lesetext, echte Bold-Familie für Hervorhebungen.

    Tk unterscheidet nur normal/bold. Windows/Linux wählen die separate
    SemiBold-Familie; macOS den konkreten PostScript-Schnitt einschließlich
    Italic. Bold verwendet weiter die Stammfamilie mit ihrem echten 700er.
    """
    key = str(family or "").casefold()
    style = next((style for style in STYLES
                  if key and key in (style.tk_family.casefold(), style.body_family.casefold(),
                             style.body_postscript.casefold(),
                             (style.body_postscript + "Italic").casefold())), None)
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
            if style.body_family and key in {name.casefold() for name in names}:
                return style.tk_family
    return family


def face_options(description, platform=None):
    """Einen konkreten Schnitt beim Kopieren eines Tk-Tupels erhalten.

    tkinter.Font löst Tupel über `font actual` auf. AppKit meldet dabei nur
    die Stammfamilie, ebenso Fontconfig bei Familienaliasen; ein erneuter
    Aufbau würde den 600er-Schnitt verlieren.
    Benannte und gewöhnliche Schriften bleiben auf dem normalen Tk-Weg.
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
