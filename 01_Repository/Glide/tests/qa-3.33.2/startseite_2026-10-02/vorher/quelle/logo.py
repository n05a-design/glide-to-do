"""Glide-Logo und App-Symbol aus den SVG-Mastern (29.09.2026).

Die Master liegen in `20_Grafik_Master`; Kopien stehen unverändert unter
`resources/logo/`:

- `glide-logo.svg` – das Zeichen, eine Fläche in einer Farbe;
- `glide-app-icon.svg` – das App-Symbol: blaue Fläche mit ausgespartem Zeichen;
- `glide-logo.png`, `glide-app-icon.png` – dieselben Motive als PNG für Tk 8.6.

**Warum SVG:** Tk 9 liest SVG selbst (nanosvg) und rechnet es für jede Größe
scharf. Die Farbe steht im SVG als Füllwert. Für die Akzentfarbe wird genau
dieser Wert ersetzt, bevor Tk das Bild rechnet – eine Textersetzung an einer
bekannten Stelle, kein Nachfärben von Pixeln. Das Motiv selbst bleibt
unangetastet; ein neu exportierter Master braucht keine Codeänderung, solange
er die freigegebene Füllfarbe in CSS oder Inline-Stil trägt (`test_logo330` prüft das).

**Tk 8.6** kennt kein SVG. Dann zeichnet Glide das Zeichen als Fläche auf eine
Canvas: Der Pfad besteht nur aus Geraden und kubischen Bézierkurven, die hier
in einen Polygonzug zerlegt werden. Das App-Symbol kommt dort aus dem PNG.

Nur Standardbibliothek und tkinter.
"""

import functools
import math
import os
import re
import sys
import tkinter as tk
import svg_geometry

# Füllfarbe der Master (Glide-Blau). Genau dieser Wert wird ersetzt.
MASTER_FILL = "#0185e1"
BRAND_BLUE = "#0185E1"
LOGO_FILE = "glide-logo.svg"
ICON_FILE = "glide-app-icon.svg"
LOGO_PNG = "glide-logo.png"
ICON_PNG = "glide-app-icon.png"
# Luft um das Zeichen, damit geglättete Kanten nicht angeschnitten werden –
# in Einheiten der Master (841,89 × 841,89).
BOX_MARGIN = 4.0
# macOS zeichnet Programmsymbole mit Rand: Die Fläche füllt 824 von 1024
# Pixeln (Apple-Raster seit macOS 11). Windows und Linux nutzen die volle
# Fläche.
MACOS_ICON_SHARE = 824 / 1024

_SVG_NS = "{http://www.w3.org/2000/svg}"


def resource_dir():
    """Ordner `resources/logo` neben diesem Modul – auch im Bundle und in 07_Python-Versionen."""
    basis = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.abspath(__file__))
    return os.path.join(basis, "resources", "logo")


@functools.lru_cache(maxsize=8)
def read_svg(name=LOGO_FILE):
    with open(os.path.join(resource_dir(), name), "r", encoding="utf-8") as datei:
        return datei.read()


tinted = svg_geometry.tinted


# --- Geometrie ---------------------------------------------------------------
# Keep existing geometry entry points while the implementation remains Tk-free.
_matrix = svg_geometry._matrix
_multiply = svg_geometry._multiply
_apply = svg_geometry._apply
_tokens = svg_geometry._tokens
subpaths = svg_geometry.subpaths


@functools.lru_cache(maxsize=8)
def outline(name=LOGO_FILE):
    return svg_geometry.outline(read_svg(name))


def bounding_box(name=LOGO_FILE):
    """(x, y, Breite, Höhe) der gezeichneten Fläche – die Kurvenpunkte schließen sie ein."""
    punkte = [punkt for teil in outline(name) for punkt in teil]
    x0 = min(px for px, _py in punkte) - BOX_MARGIN
    y0 = min(py for _px, py in punkte) - BOX_MARGIN
    x1 = max(px for px, _py in punkte) + BOX_MARGIN
    y1 = max(py for _px, py in punkte) + BOX_MARGIN
    return x0, y0, x1 - x0, y1 - y0


def aspect(name=LOGO_FILE):
    """Breite je Höhe des Zeichens ohne den leeren Rand des Masters."""
    _x, _y, breite, hoehe = bounding_box(name)
    return breite / hoehe


def cropped_svg(svg, box):
    """Setzt die viewBox auf den Ausschnitt `box` und die Maße auf dessen Seitenverhältnis."""
    x, y, breite, hoehe = box
    kopf = re.search(r"<svg\b[^>]*>", svg)
    if kopf is None:
        raise ValueError("Kein <svg>-Element")
    neu = kopf.group(0)
    neu = re.sub(r'\sviewBox="[^"]*"', "", neu)
    neu = re.sub(r'\swidth="[^"]*"', "", neu)
    neu = re.sub(r'\sheight="[^"]*"', "", neu)
    neu = neu.replace("<svg", f'<svg width="{breite:.3f}" height="{hoehe:.3f}" '
                              f'viewBox="{x:.3f} {y:.3f} {breite:.3f} {hoehe:.3f}"', 1)
    return svg[:kopf.start()] + neu + svg[kopf.end():]


# --- Tk-Bilder ---------------------------------------------------------------
def has_svg(master):
    """Tk 9 liest SVG; Tk 8.6 nicht."""
    try:
        probe = tk.PhotoImage(master=master, format="svg",
                              data='<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>')
        probe.tk.call("image", "delete", probe.name)
        return True
    except tk.TclError:
        return False


def logo_photo(master, hoehe, farbe=BRAND_BLUE, name=LOGO_FILE):
    """Das Zeichen als Bild in `farbe`, `hoehe` Pixel hoch und randlos – oder None ohne SVG."""
    if not has_svg(master):
        return None
    svg = cropped_svg(tinted(read_svg(name), farbe), bounding_box(name))
    return tk.PhotoImage(master=master, data=svg, format=f"svg -scaletoheight {max(1, int(hoehe))}")


def icon_svg(rand=0.0):
    """App-Symbol als SVG-Text, mit `rand` (Anteil je Seite) Luft um die Fläche."""
    svg = svg_geometry.inline_styles(read_svg(ICON_FILE))
    x, y, breite, hoehe = bounding_box(ICON_FILE)
    seite = max(breite, hoehe)
    zusatz = seite * rand / max(1e-6, 1 - 2 * rand)
    box = (x - (seite - breite) / 2 - zusatz, y - (seite - hoehe) / 2 - zusatz,
           seite + 2 * zusatz, seite + 2 * zusatz)
    return cropped_svg(svg, box)


def icon_margin(plattform=None):
    """Rand je Seite für das Programmsymbol: nur macOS setzt die Fläche kleiner in das Quadrat."""
    return (1 - MACOS_ICON_SHARE) / 2 if (plattform or sys.platform) == "darwin" else 0.0


def square_icon(master, svg, kante):
    """Quadratisches Bild aus einem quadratischen SVG.

    Tk rundet die zweite Kante beim Skalieren auf; aus 16 × 16 wurden sonst
    16 × 17 Pixel. Der überzählige Rand ist leer und wird abgeschnitten.
    """
    kante = int(kante)
    bild = tk.PhotoImage(master=master, data=svg, format=f"svg -scaletowidth {kante}")
    if bild.width() == kante and bild.height() == kante:
        return bild
    genau = tk.PhotoImage(master=master, width=kante, height=kante)
    genau.tk.call(genau.name, "copy", bild.name, "-from", 0, 0, min(kante, bild.width()), min(kante, bild.height()))
    bild.tk.call("image", "delete", bild.name)
    return genau


def icon_photos(master, groessen=(256, 64, 32, 16)):
    """App-Symbol in mehreren Größen für `wm iconphoto` – aus SVG, sonst aus dem PNG."""
    fotos = []
    if has_svg(master):
        svg = icon_svg(icon_margin())
        for groesse in groessen:
            fotos.append(square_icon(master, svg, groesse))
        return fotos
    pfad = os.path.join(resource_dir(), ICON_PNG)
    if not os.path.isfile(pfad):
        return []
    quelle = tk.PhotoImage(master=master, file=pfad)
    for groesse in groessen:
        faktor = max(1, math.ceil(quelle.width() / groesse))
        fotos.append(quelle.subsample(faktor, faktor))
    return fotos


def draw_logo_polygons(canvas, x, y, hoehe, farbe, tag="logo", name=LOGO_FILE):
    """Zeichnet das Zeichen als Fläche auf `canvas` (Rückfall ohne SVG)."""
    bx, by, _breite, bhoehe = bounding_box(name)
    faktor = hoehe / bhoehe
    for teil in svg_geometry.canvas_polygons(outline(name)):
        punkte = []
        for px, py in teil:
            punkte.extend((x + (px - bx) * faktor, y + (py - by) * faktor))
        if len(punkte) >= 6:
            canvas.create_polygon(punkte, fill=farbe, outline="", tags=(tag,))
