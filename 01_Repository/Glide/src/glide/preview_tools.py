"""Systemwerkzeuge für Bildvorschauen unter Linux, ohne Tk (N08 seit 3.34.0).

Glide bringt keine Bildbibliothek mit. Unter Linux liest Tk nur PNG, GIF, PPM
und (ab Tk 9) SVG. Ist ein Systemwerkzeug vorhanden, wandelt es andere
Formate für die Vorschau um – sonst bleibt der Platzhalter mit der Endung:

- `gdk-pixbuf-thumbnailer` (GNOME) schreibt ein verkleinertes PNG und kennt
  alles, was gdk-pixbuf lesen kann (JPEG, WebP, TIFF, BMP …);
- `djpeg` (libjpeg) wandelt JPEG in PPM; verkleinert wird in den Stufen, die
  libjpeg beim Dekodieren selbst kann (1/2, 1/4, 1/8).

Keine Laufzeitabhängigkeit: Gesucht wird nur, was im Pfad steht.
"""
import shutil
import struct

JPEG = (".jpg", ".jpeg")
# Formate, die gdk-pixbuf üblicherweise liest (HEIC nur mit Zusatzmodul).
PIXBUF = (".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp", ".heic", ".heif")
# Startmarker eines JPEG-Bildes mit Größenangabe (SOF0–SOF15 ohne DHT/JPG/DAC).
_SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


def jpeg_size(daten):
    """(Breite, Höhe) aus den Bytes eines JPEG-Kopfes oder None."""
    if not isinstance(daten, (bytes, bytearray)) or daten[:2] != b"\xff\xd8":
        return None
    pos = 2
    while pos + 4 <= len(daten):
        if daten[pos] != 0xFF:
            return None
        marker = daten[pos + 1]
        if marker == 0xFF:  # Füllbyte
            pos += 1
            continue
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        laenge = struct.unpack(">H", daten[pos + 2:pos + 4])[0]
        if marker in _SOF:
            if pos + 9 > len(daten):
                return None
            hoehe, breite = struct.unpack(">HH", daten[pos + 5:pos + 9])
            return (breite, hoehe) if breite and hoehe else None
        if laenge < 2:
            return None
        pos += 2 + laenge
    return None


def djpeg_scale(groesse, max_kante):
    """Kleinste libjpeg-Stufe 1/1, 1/2, 1/4 oder 1/8, deren längste Kante noch ≥ max_kante ist."""
    if not groesse:
        return "1/1"
    kante = max(groesse)
    for nenner in (8, 4, 2):
        if kante / nenner >= max_kante:
            return f"1/{nenner}"
    return "1/1"


def linux_plan(path, ziel_ohne_endung, groesse=None, max_kante=1600, which=None):
    """(Befehl, Zieldatei) für die Linux-Vorschau oder None, wenn kein Werkzeug passt.

    `which` sucht ein Programm im Pfad; ohne Angabe `shutil.which` zum Zeitpunkt des Aufrufs.
    """
    which = which or shutil.which
    endung = "." + str(path).rsplit(".", 1)[-1].lower() if "." in str(path) else ""
    vorschau = which("gdk-pixbuf-thumbnailer")
    if vorschau and endung in PIXBUF:
        ziel = ziel_ohne_endung + ".png"
        return [vorschau, "-s", str(int(max_kante)), str(path), ziel], ziel
    dekoder = which("djpeg")
    if dekoder and endung in JPEG:
        ziel = ziel_ohne_endung + ".ppm"
        return [dekoder, "-scale", djpeg_scale(groesse, max_kante), "-outfile", ziel, str(path)], ziel
    return None
