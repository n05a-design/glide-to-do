"""Mitgelieferte Textschriften und dauerhafte Stilzuordnung, ohne Tk.

Einstellungen und späteres Onboarding verwenden dieselben Kennungen.
Symbol- und Pixelschriften sind keine auswählbaren Textstile.
"""
from dataclasses import dataclass


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

    @property
    def label(self):
        return f"{self.classification}: {self.family}"

    @property
    def default_family(self):
        return self.body_family or self.tk_family


STYLES = (
    FontStyle("rubik", "Modern", "Rubik", "Rubik", "Rubik-Regular.ttf", "Rubik-Bold.ttf"),
    FontStyle("roboto_mono", "Technisch", "Roboto Mono", "Roboto Mono",
              "RobotoMono-Regular.ttf", "RobotoMono-Bold.ttf"),
    FontStyle("playfair_display", "Kreativ", "Playfair Display", "Playfair Display",
              "PlayfairDisplay-Regular.ttf", "PlayfairDisplay-Bold.ttf",
              "Playfair Display SemiBold", "PlayfairDisplay-SemiBold.ttf"),
    FontStyle("fraunces", "Klassisch", "Fraunces", "Fraunces 72pt",
              "Fraunces_72pt-Regular.ttf", "Fraunces_72pt-Bold.ttf",
              "Fraunces 72pt SemiBold", "Fraunces_72pt-SemiBold.ttf"),
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
                            style.tk_family.casefold(), style.default_family.casefold(),
                            style.label.casefold()}), DEFAULT)


def family_for_weight(family, bold=False):
    """SemiBold für Lesetext, echte Bold-Familie für Hervorhebungen.

    Tk unterscheidet nur normal/bold. SemiBold liegt deshalb als eigene
    Familie vor; ein Bold-Auftrag darf daraus keinen künstlichen Fettschnitt
    erzeugen. Fremde Familien und der Symbolbegleiter bleiben unverändert.
    """
    key = str(family or "").casefold()
    style = next((style for style in STYLES
                  if key in (style.tk_family.casefold(), style.default_family.casefold())), None)
    return (style.tk_family if bold else style.default_family) if style else family
