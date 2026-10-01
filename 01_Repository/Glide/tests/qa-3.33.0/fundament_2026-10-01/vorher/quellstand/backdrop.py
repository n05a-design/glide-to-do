"""Hintergrundverläufe für Glide: Mesh, Aurora, Körnung und Pixelraster.

Reine Standardbibliothek, ohne Tk: Das Modul rechnet RGB-Bytes und kodiert sie
als PNG. Die Anwendung legt das Ergebnis als Bild hinter die Oberfläche.

Ein Verlauf entsteht aus weichen Farbwolken (Gauß-Glocken) über einer
Grundfarbe. Eine sanfte Sinusverzerrung formt daraus die organischen Bänder
eines Nordlichts; feines Rauschen gibt Körnung und verdeckt Stufen. Das
Pixel-Design rechnet grob, rastert mit geordnetem Dithering auf seine Palette
und vergrößert blockweise.

Lesbarkeit geht vor Farbe: `fit_intensity` schwächt einen Entwurf so weit ab,
dass die übergebenen Schriftfarben auf jedem Punkt mindestens 4,5:1 erreichen
(WCAG AA). Die Farbe soll man spüren, nicht über den Text hinweg sehen.
"""

from __future__ import annotations

import math
import random
import struct
import zlib
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Farben


def hex_rgb(value):
    text = str(value).lstrip("#")
    return tuple(int(text[index:index + 2], 16) for index in (0, 2, 4))


def rgb_hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(kanal)))) for kanal in rgb)


def _linear(kanal):
    kanal /= 255.0
    return kanal / 12.92 if kanal <= 0.03928 else ((kanal + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (_linear(kanal) for kanal in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(first, second):
    hell, dunkel = sorted((luminance(first), luminance(second)), reverse=True)
    return (hell + 0.05) / (dunkel + 0.05)


def mix(first, second, anteil):
    return tuple(a + (b - a) * anteil for a, b in zip(first, second))


# ---------------------------------------------------------------------------
# Entwürfe


@dataclass(frozen=True)
class Blob:
    """Eine weiche Farbwolke: Mitte, Halbachsen (Anteile der Fläche), Farbe, Gewicht."""

    x: float
    y: float
    rx: float
    ry: float
    color: str
    strength: float = 1.0


@dataclass(frozen=True)
class Preset:
    key: str
    name: str
    blobs: tuple
    warp: tuple = (0.0, 1.0, 0.0, 0.0, 1.0, 0.0)  # (ax, fx, px, ay, fy, py)
    grain: float = 3.0      # Rauschen in Farbstufen (±)
    intensity: float = 1.0  # 0 = nur Grundfarbe, 1 = volle Wolkenfarben
    pixel: int = 0          # > 0: Blockgröße des Pixelrasters
    palette: tuple = ()     # Pixelraster: erlaubte Farben
    vignette: float = 0.0   # Abdunkeln (bzw. Aufhellen) zum Rand, 0 bis 1
    description: str = ""


def _p(key, name, blobs, **kwargs):
    return Preset(key, name, tuple(Blob(*blob) for blob in blobs), **kwargs)


AURORA = (0.07, 1.2, 0.6, 0.05, 1.0, 1.7)
WELLE = (0.05, 0.8, 2.1, 0.04, 1.4, 0.3)
RUHIG = (0.02, 0.7, 0.0, 0.02, 0.6, 1.0)

PRESETS = {
    "dark": (
        _p("aurora", "Aurora", ((0.18, 0.28, 0.32, 0.42, "#5B2CA0"), (0.62, 0.18, 0.30, 0.32, "#1F9E9A"),
                                (0.78, 0.62, 0.28, 0.34, "#C23B7A", 0.8), (0.30, 0.86, 0.34, 0.26, "#23307A")),
           warp=AURORA, description="Violett, Petrol und Magenta in weichen Bändern"),
        _p("mitternacht", "Mitternacht", ((0.25, 0.25, 0.45, 0.40, "#1A2150"), (0.80, 0.35, 0.35, 0.40, "#2B1F5C"),
                                          (0.50, 0.74, 0.55, 0.05, "#C9A14A", 0.7)),
           warp=RUHIG, grain=2.0, description="Tiefes Blau mit einer feinen goldenen Horizontlinie"),
        _p("ozean", "Ozean", ((0.20, 0.70, 0.40, 0.35, "#0E5A6B"), (0.70, 0.30, 0.35, 0.40, "#1AA0B8", 0.8),
                              (0.85, 0.85, 0.30, 0.30, "#1D3F9A")), warp=WELLE, description="Petrol, Cyan und Tiefblau"),
        _p("glut", "Glut", ((0.20, 0.25, 0.40, 0.40, "#4A1640"), (0.60, 0.55, 0.30, 0.30, "#A3245E", 0.8),
                            (0.88, 0.88, 0.30, 0.28, "#D98A2B", 0.8)), warp=WELLE,
           description="Pflaume und Magenta mit bernsteinfarbenem Glühen"),
        _p("nebel", "Nebel", ((0.15, 0.20, 0.30, 0.30, "#3B2A8F"), (0.80, 0.25, 0.30, 0.30, "#B0306F", 0.7),
                              (0.30, 0.80, 0.32, 0.30, "#2394B0", 0.8), (0.75, 0.80, 0.25, 0.25, "#3B2A8F", 0.6)),
           description="Mesh aus Indigo, Rosa und Cyan"),
    ),
    "glass_dark": (
        _p("nordlicht", "Nordlicht", ((0.22, 0.35, 0.30, 0.45, "#18A07A"), (0.55, 0.20, 0.30, 0.30, "#2A8FD0"),
                                      (0.80, 0.55, 0.30, 0.40, "#7B3FD6"), (0.35, 0.85, 0.40, 0.25, "#153A7A")),
           warp=AURORA, description="Grün, Blau und Violett wie ein Polarlicht"),
        _p("lagune", "Lagune", ((0.25, 0.30, 0.40, 0.40, "#0F7F8C"), (0.75, 0.25, 0.30, 0.35, "#35C3C9", 0.7),
                                (0.60, 0.85, 0.40, 0.30, "#2551B0")), warp=WELLE, description="Türkis und Lagunenblau"),
        _p("amethyst", "Amethyst", ((0.20, 0.25, 0.35, 0.40, "#6B2FB5"), (0.75, 0.35, 0.30, 0.35, "#B23FA8", 0.8),
                                    (0.45, 0.85, 0.40, 0.30, "#2E2A8F")), warp=AURORA,
           description="Violett und Orchidee"),
        _p("sonnenwind", "Sonnenwind", ((0.12, 0.30, 0.30, 0.40, "#D0406E"), (0.40, 0.55, 0.20, 0.35, "#E88A6A", 0.8),
                                        (0.65, 0.25, 0.30, 0.35, "#2FB39F"), (0.70, 0.85, 0.35, 0.30, "#5C3AD0")),
           warp=AURORA, description="Rosa, Koralle, Mint und Violett – das Farbspiel deines Bildes"),
        _p("polarnacht", "Polarnacht", ((0.30, 0.20, 0.40, 0.35, "#1E3E8F"), (0.70, 0.60, 0.35, 0.40, "#2F9FD0", 0.7),
                                        (0.20, 0.85, 0.30, 0.25, "#1A2360")), warp=RUHIG,
           description="Kühles Blau mit hellem Eishauch"),
    ),
    "light": (
        _p("pastell", "Pastell", ((0.22, 0.45, 0.30, 0.40, "#8FB3E8"), (0.45, 0.30, 0.25, 0.30, "#D9A1D0", 0.9),
                                  (0.80, 0.80, 0.30, 0.25, "#E8C4DE", 0.7)), warp=RUHIG, grain=1.5,
           description="Hellblau, Rosa und viel Weiß"),
        _p("herbstlicht", "Herbstlicht", ((0.30, 0.20, 0.35, 0.35, "#F7C9A0"), (0.60, 0.40, 0.30, 0.35, "#F4B06A", 0.8),
                                          (0.20, 0.80, 0.35, 0.30, "#F4A6B8", 0.8), (0.85, 0.30, 0.25, 0.30, "#C9C3E8")),
           warp=WELLE, grain=1.5, description="Apricot, Orange, Rosé und ein Hauch Lavendel"),
        _p("morgenrot", "Morgenrot", ((0.05, 0.10, 0.40, 0.40, "#8FE3F0"), (0.50, 0.45, 0.40, 0.40, "#C7B3F5"),
                                      (0.95, 0.90, 0.40, 0.40, "#F6B3E0")), warp=RUHIG, grain=1.5,
           description="Cyan über Lavendel zu Rosa"),
        _p("salbei", "Salbei", ((0.25, 0.30, 0.35, 0.35, "#B8DCC5"), (0.70, 0.60, 0.35, 0.35, "#E3ECD0"),
                                (0.85, 0.20, 0.25, 0.25, "#CFE3E8")), warp=RUHIG, grain=1.5,
           description="Salbei, Creme und Wasserblau"),
        _p("perlmutt", "Perlmutt", ((0.20, 0.25, 0.30, 0.30, "#E8D9F5"), (0.60, 0.60, 0.30, 0.30, "#D4F0E8"),
                                    (0.85, 0.25, 0.25, 0.25, "#F9E3D3")), warp=AURORA, grain=1.0,
           description="Schimmerndes Flieder, Mint und Pfirsich"),
    ),
    "glass_light": (
        _p("iris", "Iris", ((0.20, 0.35, 0.30, 0.40, "#7FA6F0"), (0.55, 0.25, 0.30, 0.30, "#C58BE0"),
                            (0.80, 0.75, 0.30, 0.30, "#F0A3C8")), warp=AURORA, grain=2.0,
           description="Blau, Violett und Rosa, kräftiger für Glas"),
        _p("pfirsich", "Pfirsich", ((0.25, 0.25, 0.35, 0.35, "#FFB88A"), (0.70, 0.40, 0.30, 0.35, "#FF9FA8"),
                                    (0.40, 0.85, 0.35, 0.25, "#FFD48A")), warp=WELLE, grain=2.0,
           description="Pfirsich, Koralle und Honig"),
        _p("lavendel", "Lavendel", ((0.25, 0.30, 0.35, 0.40, "#B9A4F2"), (0.75, 0.30, 0.30, 0.30, "#E3B5F0"),
                                    (0.55, 0.85, 0.35, 0.25, "#A8C8F5")), warp=RUHIG, grain=2.0,
           description="Lavendel und Himmelblau"),
        _p("minze", "Minze", ((0.25, 0.25, 0.35, 0.35, "#8FE0C0"), (0.70, 0.55, 0.30, 0.35, "#A8E6F0"),
                              (0.30, 0.85, 0.30, 0.25, "#E0F0A8")), warp=WELLE, grain=2.0,
           description="Minze, Eisblau und Limette"),
        _p("himmel", "Himmel", ((0.10, 0.10, 0.45, 0.40, "#6FD0F5"), (0.60, 0.40, 0.40, 0.40, "#9AA8F5"),
                                (0.95, 0.95, 0.40, 0.40, "#F09BE6")), warp=RUHIG, grain=2.0,
           description="Klarer Verlauf von Cyan über Blau nach Magenta"),
    ),
    "minimal_light": (
        _p("papier", "Papier", ((0.30, 0.30, 0.50, 0.50, "#ECE4D6"), (0.80, 0.80, 0.40, 0.40, "#E4DCCD")),
           grain=2.5, description="Warmes Papierweiß mit Körnung"),
        _p("kuehl", "Kühl", ((0.25, 0.25, 0.50, 0.45, "#DDE4EC"), (0.80, 0.75, 0.40, 0.40, "#E6EAEF")),
           grain=1.5, description="Kühles Hellgrau"),
        _p("licht", "Lichtkegel", ((0.50, -0.10, 0.60, 0.55, "#FFFFFF", 1.4), (0.50, 1.10, 0.70, 0.40, "#E2E2E2")),
           grain=1.0, description="Helles Licht von oben"),
        _p("stein", "Stein", ((0.20, 0.30, 0.35, 0.35, "#DADADA"), (0.70, 0.70, 0.35, 0.35, "#E8E8E8"),
                              (0.85, 0.20, 0.25, 0.25, "#D2D2D2")), warp=RUHIG, grain=2.0,
           description="Grauer Stein, leicht bewegt"),
        _p("koernung", "Körnung", ((0.50, 0.50, 0.80, 0.80, "#EFEFEF", 0.3),), grain=5.0,
           description="Nur Körnung, keine Farbe"),
    ),
    "minimal_dark": (
        _p("graphit", "Graphit", ((0.30, 0.30, 0.50, 0.50, "#2A2A2A"), (0.80, 0.80, 0.40, 0.40, "#222222")),
           grain=2.5, description="Graphit mit Körnung"),
        _p("schiefer", "Schiefer", ((0.25, 0.25, 0.50, 0.45, "#232A33"), (0.80, 0.75, 0.40, 0.40, "#1E242B")),
           grain=2.0, description="Kühles Schiefergrau"),
        _p("rauch", "Rauch", ((0.30, 0.70, 0.45, 0.35, "#2E2925"), (0.75, 0.25, 0.40, 0.35, "#27231F")),
           warp=WELLE, grain=2.0, description="Warmer Rauch"),
        _p("lichtkegel", "Lichtkegel", ((0.50, -0.10, 0.60, 0.55, "#3A3A3A", 1.3),), grain=1.5,
           description="Schwaches Licht von oben"),
        _p("koernung", "Körnung", ((0.50, 0.50, 0.80, 0.80, "#202020", 0.3),), grain=5.0,
           description="Nur Körnung, keine Farbe"),
    ),
    "dopamine": (
        _p("neon", "Neon", ((0.20, 0.30, 0.30, 0.35, "#FF2BD6"), (0.75, 0.25, 0.30, 0.35, "#00E5FF"),
                            (0.50, 0.85, 0.40, 0.30, "#7C3CFF")), warp=AURORA, description="Pink, Cyan und Violett"),
        _p("synthwave", "Synthwave", ((0.50, 0.95, 0.70, 0.18, "#FFB347", 0.9), (0.50, 0.70, 0.60, 0.25, "#FF5E9C"),
                                      (0.50, 0.15, 0.70, 0.40, "#4B2BFF")), warp=RUHIG,
           description="Violetter Himmel über einem glühenden Horizont"),
        _p("lava", "Lava", ((0.25, 0.70, 0.35, 0.35, "#FF3D3D"), (0.70, 0.35, 0.30, 0.30, "#FF9F1C", 0.8),
                            (0.80, 0.85, 0.30, 0.30, "#B3175C")), warp=WELLE, description="Rot, Orange und Beere"),
        _p("tropen", "Tropen", ((0.20, 0.25, 0.30, 0.35, "#00F5A0"), (0.70, 0.35, 0.30, 0.35, "#00D9FF"),
                                (0.55, 0.85, 0.30, 0.25, "#FFD400", 0.8)), warp=AURORA,
           description="Grün, Cyan und Sonnengelb"),
        _p("candy", "Candy", ((0.20, 0.30, 0.35, 0.35, "#FF7EB3"), (0.70, 0.25, 0.30, 0.35, "#B388FF"),
                              (0.60, 0.80, 0.35, 0.30, "#7AFCFF")), warp=WELLE, description="Bonbonrosa, Flieder, Eisblau"),
    ),
    "pixel": (
        _p("pixelnacht", "Pixel-Aurora", ((0.25, 0.35, 0.35, 0.40, "#3D7BFF"), (0.70, 0.30, 0.30, 0.35, "#FF3EA5"),
                                          (0.50, 0.85, 0.40, 0.25, "#3D7BFF")), warp=AURORA, grain=0.0, pixel=12,
           palette=("#0D0D12", "#121833", "#1B2656", "#2A1433", "#3F1A4A"), description="Nordlicht aus Pixelblöcken"),
        _p("abendrot", "8-Bit-Abend", ((0.50, 1.00, 0.80, 0.30, "#FFD21F"), (0.50, 0.75, 0.80, 0.25, "#FF3EA5"),
                                       (0.50, 0.20, 0.80, 0.40, "#1A2350")), grain=0.0, pixel=12,
           palette=("#0D0D12", "#141A38", "#2E1638", "#4A1D3F", "#5C3A1A"), description="Sonnenuntergang in Bändern"),
        _p("sterne", "Sternenhimmel", ((0.50, 0.50, 0.90, 0.90, "#141A38"),), grain=0.0, pixel=10,
           palette=("#0D0D12", "#141A38", "#3D7BFF", "#FFD21F"), description="Dunkler Himmel mit einzelnen Pixelsternen"),
        _p("plasma", "Plasma", ((0.20, 0.30, 0.30, 0.30, "#3D7BFF"), (0.70, 0.25, 0.30, 0.30, "#FFD21F"),
                                (0.50, 0.80, 0.30, 0.30, "#FF3EA5")), warp=WELLE, grain=0.0, pixel=16,
           palette=("#0D0D12", "#15204A", "#2A1433", "#3A2F12", "#1F2E6B", "#4A1A48"),
           description="Alle drei Pixelfarben gemischt, gedämpft"),
        _p("raster", "Rasterlinien", ((0.50, 0.50, 0.90, 0.90, "#1A2350"),), grain=0.0, pixel=8,
           palette=("#0D0D12", "#131A33", "#1A2350"), description="Ruhiges Raster, fast schwarz"),
    ),
    "contrast_light": (
        _p("hauch_blau", "Hauch Blau", ((0.30, 0.30, 0.50, 0.50, "#E4ECF8"),), grain=0.0, description="Kaum sichtbares Blau"),
        _p("hauch_sand", "Hauch Sand", ((0.30, 0.30, 0.50, 0.50, "#F5EEDF"),), grain=0.0, description="Kaum sichtbarer Sand"),
        _p("hauch_mint", "Hauch Mint", ((0.30, 0.30, 0.50, 0.50, "#E3F4EC"),), grain=0.0, description="Kaum sichtbares Mint"),
        _p("hauch_flieder", "Hauch Flieder", ((0.30, 0.30, 0.50, 0.50, "#EEE6F7"),), grain=0.0,
           description="Kaum sichtbares Flieder"),
        _p("hauch_grau", "Hauch Grau", ((0.50, 0.00, 0.60, 0.60, "#EDEDED"),), grain=0.0, description="Leichtes Grau von oben"),
    ),
    "contrast_dark": (
        _p("tiefblau", "Tiefblau", ((0.30, 0.30, 0.50, 0.50, "#161E33"),), grain=0.0, description="Sehr dunkles Blau"),
        _p("tiefgruen", "Tiefgrün", ((0.30, 0.30, 0.50, 0.50, "#122620"),), grain=0.0, description="Sehr dunkles Grün"),
        _p("tiefviolett", "Tiefviolett", ((0.30, 0.30, 0.50, 0.50, "#221633"),), grain=0.0,
           description="Sehr dunkles Violett"),
        _p("tiefrot", "Tiefrot", ((0.30, 0.30, 0.50, 0.50, "#2E1418"),), grain=0.0, description="Sehr dunkles Rot"),
        _p("graphit", "Graphit", ((0.50, 0.00, 0.60, 0.60, "#24242A"),), grain=0.0, description="Leichtes Grau von oben"),
    ),
}

NONE_KEY = "none"


def presets_for(design):
    return PRESETS.get(design, ())


def find_preset(design, key):
    return next((preset for preset in presets_for(design) if preset.key == key), None)


# ---------------------------------------------------------------------------
# Rechnen

_BAYER4 = (0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5)


ENGINE_VERSION = 1


def zone_intensity_at(v, staerke, zone):
    """Stärke an der Höhe v (0 oben, 1 unten): in der Lesezone gedämpft, mit weichem Übergang."""
    if not zone:
        return staerke
    ende, gedaempft, uebergang = zone
    if v <= ende:
        return gedaempft
    if v >= ende + uebergang:
        return staerke
    anteil = (v - ende) / max(1e-6, uebergang)
    anteil = anteil * anteil * (3 - 2 * anteil)
    return gedaempft + (staerke - gedaempft) * anteil


def render(preset, width, height, base, intensity=None, seed=7, zone=None):
    """RGB-Bytes (Zeile für Zeile) eines Entwurfs in der gegebenen Größe.

    `zone` = (Ende als Anteil der Höhe, Stärke darin, Übergang): Oben, wo Titel
    und Unterzeile direkt auf dem Verlauf stehen, bleibt er leiser.
    """
    breite, hoehe = max(1, int(width)), max(1, int(height))
    grund = hex_rgb(base)
    staerke = preset.intensity if intensity is None else intensity
    rohfarben = [hex_rgb(blob.color) for blob in preset.blobs]

    def wolken_fuer(anteil):
        return [(blob.x, blob.y, 1.0 / max(0.02, blob.rx), 1.0 / max(0.02, blob.ry),
                 mix(grund, farbe, anteil), blob.strength) for blob, farbe in zip(preset.blobs, rohfarben)]

    wolken = wolken_fuer(staerke)
    ax, fx, px, ay, fy, py = preset.warp
    tau = 2.0 * math.pi
    exp, sin = math.exp, math.sin
    zufall = random.Random(seed)
    koernung = preset.grain
    vignette = preset.vignette
    palette = [hex_rgb(farbe) for farbe in preset.palette] if preset.pixel and preset.palette else None
    ausgabe = bytearray(breite * hoehe * 3)
    index = 0
    spalten = [x / max(1, breite - 1) for x in range(breite)]
    verzug_y = [ay * sin(tau * fy * u + py) for u in spalten]
    for y in range(hoehe):
        v = y / max(1, hoehe - 1)
        zeilenstaerke = zone_intensity_at(v, staerke, zone)
        if zone:
            wolken = wolken_fuer(zeilenstaerke)
        # Akzentpunkte (Sterne) nur bei voller Stärke – nie unter Text.
        akzente = zeilenstaerke >= staerke * 0.95 and staerke > 0.5
        verzug_x = ax * sin(tau * fx * v + px)
        for x, u in enumerate(spalten):
            uu = u + verzug_x
            vv = v + verzug_y[x]
            r, g, b, summe = float(grund[0]), float(grund[1]), float(grund[2]), 1.0
            for bx, by, kx, ky, farbe, gewicht in wolken:
                dx = (uu - bx) * kx
                dy = (vv - by) * ky
                w = gewicht * exp(-(dx * dx + dy * dy))
                r += w * farbe[0]
                g += w * farbe[1]
                b += w * farbe[2]
                summe += w
            r /= summe
            g /= summe
            b /= summe
            if vignette:
                rand = min(1.0, ((u - 0.5) ** 2 + (v - 0.5) ** 2) * 2.0)
                faktor = 1.0 - vignette * rand
                r, g, b = r * faktor, g * faktor, b * faktor
            if palette is not None:
                r, g, b = _dither(palette, (r, g, b), _BAYER4[(y & 3) * 4 + (x & 3)] / 16.0 - 0.5, zufall, preset,
                                  akzente)
            elif koernung:
                rausch = (zufall.random() - 0.5) * 2.0 * koernung
                r, g, b = r + rausch, g + rausch, b + rausch
            ausgabe[index] = 0 if r < 0 else 255 if r > 255 else int(r)
            ausgabe[index + 1] = 0 if g < 0 else 255 if g > 255 else int(g)
            ausgabe[index + 2] = 0 if b < 0 else 255 if b > 255 else int(b)
            index += 3
    return ausgabe


def _dither(palette, farbe, schwelle, zufall, preset, akzente=True):
    """Geordnetes Dithering zwischen den zwei nächsten Palettenfarben."""
    abstaende = sorted(((sum((a - b) ** 2 for a, b in zip(farbe, eintrag)), eintrag) for eintrag in palette))
    erste, zweite = abstaende[0][1], abstaende[1][1] if len(abstaende) > 1 else abstaende[0][1]
    d1, d2 = math.sqrt(abstaende[0][0]), math.sqrt(abstaende[1][0]) if len(abstaende) > 1 else 1.0
    anteil = d1 / max(1e-6, d1 + d2)
    # Schwaches Dithering: Nur nahe der Mitte zwischen zwei Stufen mischen,
    # sonst gilt die nächste Farbe. Ein volles Schachbrett wäre als
    # Hintergrund zu unruhig.
    gewaehlt = zweite if anteil + schwelle * 0.35 > 0.5 else erste
    if preset.key == "sterne" and akzente and zufall.random() < 0.004:
        gewaehlt = palette[-1] if zufall.random() < 0.3 else palette[-2]
    return gewaehlt


def render_scaled(preset, width, height, base, intensity=None, seed=7, zone=None):
    """Wie `render`, beim Pixelraster aber grob gerechnet und blockweise vergrößert.

    Liefert (rgb, breite, hoehe, faktor): die gerechneten Bytes und den ganzzahligen
    Faktor, um den die Anwendung das Bild vergrößert.
    """
    faktor = max(2, preset.pixel) if preset.pixel else 2
    breite = max(1, -(-int(width) // faktor))
    hoehe = max(1, -(-int(height) // faktor))
    return render(preset, breite, hoehe, base, intensity, seed, zone), breite, hoehe, faktor


def fit_intensity(preset, base, text_colors, minimum=4.5, probe=(48, 30), rows=None):
    """Höchste Intensität (bis zur Vorgabe des Entwurfs), bei der alle Schriftfarben tragen.

    `rows` = (von, bis) als Anteile der Höhe: nur dieser Streifen zählt – die
    Lesezone, in der Text direkt auf dem Verlauf steht.
    """
    farben = [hex_rgb(farbe) for farbe in text_colors if farbe]
    if not farben:
        return preset.intensity

    def traegt(staerke):
        daten = render(preset, probe[0], probe[1], base, staerke, seed=3)
        if rows:
            von = int(rows[0] * (probe[1] - 1)) * probe[0] * 3
            bis = (int(rows[1] * (probe[1] - 1)) + 1) * probe[0] * 3
            daten = daten[von:bis]
        punkte = {tuple(daten[i:i + 3]) for i in range(0, len(daten), 3)}
        # Körnung schwankt um ± grain; der ungünstigste Fall zählt.
        spiel = preset.grain
        for punkt in punkte:
            for abweichung in ((spiel, spiel, spiel), (-spiel, -spiel, -spiel)):
                probe_rgb = tuple(max(0, min(255, kanal + delta)) for kanal, delta in zip(punkt, abweichung))
                if any(contrast(farbe, probe_rgb) < minimum for farbe in farben):
                    return False
        return True

    if traegt(preset.intensity):
        return preset.intensity
    unten, oben = 0.0, preset.intensity
    for _ in range(9):
        mitte = (unten + oben) / 2
        if traegt(mitte):
            unten = mitte
        else:
            oben = mitte
    return unten


def average(rgb, schritt=97):
    """Mittelwert einer RGB-Folge (Stichprobe über jeden n-ten Punkt)."""
    summe, anzahl = [0, 0, 0], 0
    for index in range(0, len(rgb) - 2, 3 * schritt):
        summe[0] += rgb[index]
        summe[1] += rgb[index + 1]
        summe[2] += rgb[index + 2]
        anzahl += 1
    return rgb_hex([kanal / max(1, anzahl) for kanal in summe])


def encode_png(rgb, width, height):
    """RGB-Bytes als PNG (Farbtyp 2, Filter 0) – ohne Fremdbibliothek."""
    zeile = width * 3
    roh = b"".join(b"\x00" + bytes(rgb[y * zeile:(y + 1) * zeile]) for y in range(height))

    def block(art, daten):
        return struct.pack(">I", len(daten)) + art + daten + struct.pack(">I", zlib.crc32(art + daten) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + block(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + block(b"IDAT", zlib.compress(roh, 6)) + block(b"IEND", b""))


def decode_png(daten):
    """Liest ein PNG, das `encode_png` geschrieben hat (RGB, 8 Bit, Filter 0).

    Kein allgemeiner PNG-Leser: Er dient nur dem Zwischenspeicher. Andere
    Formen weist er mit ValueError zurück.
    """
    if not daten.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("kein PNG")
    position, breite, hoehe, roh = 8, 0, 0, b""
    while position < len(daten):
        laenge = struct.unpack(">I", daten[position:position + 4])[0]
        art = daten[position + 4:position + 8]
        inhalt = daten[position + 8:position + 8 + laenge]
        position += 12 + laenge
        if art == b"IHDR":
            breite, hoehe, tiefe, farbtyp, _k, _f, verschachtelt = struct.unpack(">IIBBBBB", inhalt)
            if (tiefe, farbtyp, verschachtelt) != (8, 2, 0):
                raise ValueError("nicht von Glide geschrieben")
        elif art == b"IDAT":
            roh += inhalt
        elif art == b"IEND":
            break
    daten_roh = zlib.decompress(roh)
    zeile = breite * 3
    rgb = bytearray(breite * hoehe * 3)
    for y in range(hoehe):
        start = y * (zeile + 1)
        if daten_roh[start] != 0:
            raise ValueError("unerwarteter Filter")
        rgb[y * zeile:(y + 1) * zeile] = daten_roh[start + 1:start + 1 + zeile]
    return rgb, breite, hoehe

