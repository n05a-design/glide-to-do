"""Werkzeugwahl für Bildvorschauen unter Linux (N08) ohne Oberfläche."""
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import preview_tools as pt


def jpeg_kopf(breite, hoehe, marker=0xC0, app=True):
    daten = b"\xff\xd8"
    if app:
        daten += b"\xff\xe0" + struct.pack(">H", 16) + b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    daten += bytes((0xFF, marker)) + struct.pack(">HBHHB", 17, 8, hoehe, breite, 3) + b"\x01\x11\x00" * 3
    return daten


class Werkzeuge(unittest.TestCase):
    def test_jpeg_size(self):
        self.assertEqual(pt.jpeg_size(jpeg_kopf(6000, 4000)), (6000, 4000))
        self.assertEqual(pt.jpeg_size(jpeg_kopf(640, 480, marker=0xC2, app=False)), (640, 480))  # progressiv
        self.assertIsNone(pt.jpeg_size(b"\x89PNG\r\n"))
        self.assertIsNone(pt.jpeg_size(jpeg_kopf(0, 10)))
        self.assertIsNone(pt.jpeg_size(b"\xff\xd8\xff\xe0\x00"))  # abgeschnitten

    def test_djpeg_scale(self):
        self.assertEqual(pt.djpeg_scale((6000, 4000), 1600), "1/2")
        self.assertEqual(pt.djpeg_scale((14000, 9000), 1600), "1/8")
        self.assertEqual(pt.djpeg_scale((2000, 1500), 1600), "1/1")
        self.assertEqual(pt.djpeg_scale(None, 1600), "1/1")

    def test_tool_choice(self):
        beide = {"gdk-pixbuf-thumbnailer": "/usr/bin/gdk-pixbuf-thumbnailer", "djpeg": "/usr/bin/djpeg"}.get
        befehl, ziel = pt.linux_plan("/a/Bild.JPG", "/c/x", which=beide)
        self.assertEqual((befehl[0], ziel), ("/usr/bin/gdk-pixbuf-thumbnailer", "/c/x.png"))
        nur_djpeg = {"djpeg": "/usr/bin/djpeg"}.get
        befehl, ziel = pt.linux_plan("/a/Bild.jpeg", "/c/x", groesse=(6000, 4000), which=nur_djpeg)
        self.assertEqual(befehl, ["/usr/bin/djpeg", "-scale", "1/2", "-outfile", "/c/x.ppm", "/a/Bild.jpeg"])
        self.assertEqual(ziel, "/c/x.ppm")
        self.assertIsNone(pt.linux_plan("/a/Bild.webp", "/c/x", which=nur_djpeg))  # djpeg nur für JPEG
        self.assertIsNone(pt.linux_plan("/a/Bild.jpg", "/c/x", which=lambda _name: None))
        self.assertEqual(pt.linux_plan("/a/Bild.webp", "/c/x", which=beide)[1], "/c/x.png")


if __name__ == "__main__":
    unittest.main()
