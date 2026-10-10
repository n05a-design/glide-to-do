"""Geglättete transparente Logo-Flächen und PNG-Ausgabe, ohne Tk.

Die freigegebenen Konturen verwenden die Gerade-Ungerade-Füllregel.
Jede Teilzeile integriert die horizontale Pixelfläche; mehrere Teilzeilen
nähern die vertikale Abdeckung an. Innenräume bleiben transparent.
"""
from functools import lru_cache
import math
import struct
import zlib


def proportional_box(box, height):
    """Gleicher Maßstab in beiden Achsen; nur der Bildrand wird aufgerundet.

    Ein gerundetes Pixelmaß darf die Kontur nicht horizontal strecken.
    Der zusätzliche Bruchteil bleibt als transparenter Rand erhalten.
    """
    if not isinstance(height, int) or not 1 <= height <= 4096:
        raise ValueError("Ungültige Rasterhöhe")
    bx, by, bw, bh = box
    if not all(math.isfinite(v) for v in box) or bw <= 0 or bh <= 0:
        raise ValueError("Ungültiger Bildausschnitt")
    width = max(1, math.ceil(bw * height / bh))
    if width > 4096:
        raise ValueError("Ungültige Rasterbreite")
    return width, (bx, by, width * bh / height, bh)


@lru_cache(maxsize=32)
def alpha_mask(rings, box, width, height, samples=8):
    """Abdeckungswerte in Zeilenfolge, unveränderlich und begrenzt gepuffert."""
    if not (isinstance(width, int) and isinstance(height, int)
            and 1 <= width <= 4096 and 1 <= height <= 4096
            and isinstance(samples, int) and 1 <= samples <= 64):
        raise ValueError("Ungültige Rastermaße oder Abtastung")
    bx, by, bw, bh = box
    if not all(math.isfinite(v) for v in box) or bw <= 0 or bh <= 0:
        raise ValueError("Ungültiger Bildausschnitt")
    edges = []
    for ring in rings:
        if len(ring) < 3:
            raise ValueError("Kontur braucht mindestens drei Punkte")
        if not all(math.isfinite(v) for point in ring for v in point):
            raise ValueError("Kontur enthält ungültige Koordinaten")
        points = [((x - bx) * width / bw, (y - by) * height / bh) for x, y in ring]
        for i, (x1, y1) in enumerate(points):
            x2, y2 = points[(i + 1) % len(points)]
            if y1 != y2:
                edges.append((x1, y1, x2, y2))
    result = bytearray(width * height)
    for row in range(height):
        coverage = [0.] * width
        for sample in range(samples):
            y = row + (sample + .5) / samples
            crossings = sorted(x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                               for x1, y1, x2, y2 in edges if (y1 > y) != (y2 > y))
            for left, right in zip(crossings[::2], crossings[1::2]):
                left, right = max(0., left), min(float(width), right)
                if left >= right:
                    continue
                for col in range(int(left), min(width, math.ceil(right))):
                    coverage[col] += min(right, col + 1.) - max(left, float(col))
        result[row * width:(row + 1) * width] = bytes(
            min(255, max(0, round(value * 255 / samples))) for value in coverage)
    return bytes(result)


def rgba_png(mask, width, height, color):
    """PNG mit unverändertem RGB und eigener Alpha-Abdeckung; kein Hintergrund."""
    if not isinstance(width, int) or not isinstance(height, int) or width < 1 or height < 1 or len(mask) != width * height:
        raise ValueError("Maske passt nicht zu den Bildmaßen")
    if (len(color) != 3 or not all(isinstance(v, int) and 0 <= v <= 255 for v in color)):
        raise ValueError("Farbe braucht drei Werte von 0 bis 255")
    rows = bytearray()
    rgb = bytes(color)
    for row in range(height):
        rows.append(0)  # PNG-Filter: kein Filter, zlib übernimmt die Kompression.
        for alpha in mask[row * width:(row + 1) * width]:
            rows.extend(rgb)
            rows.append(alpha)
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))
