"""Druckseite einer Seite mit eingebetteten Bildern (B4) ohne Oberfläche."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import page_markdown as pm


def dokument_mit_bild(name="Foto"):
    text = "Einleitung\n" + pm_anchor() + "\nSchluss"
    return {"text": text, "spans": [{"tag": "img:1", "start": 11, "end": 12}], "links": {},
            "images": {"img:1": {"attachment": "a1", "width": 300}}}


def pm_anchor():
    return "￼"


class Druckseite(unittest.TestCase):
    def test_blocks_and_escaping(self):
        html = pm.markdown_to_print_html("# Kapitel\n\nText mit <b> und **fett** und `code`.\n\n---\n\n> Zitat")
        self.assertIn("<h2>Kapitel</h2>", html)
        self.assertIn("&lt;b&gt;", html)
        self.assertIn("<b>fett</b>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn("<hr>", html)
        self.assertIn("<blockquote>Zitat</blockquote>", html)

    def test_only_safe_links(self):
        html = pm.markdown_to_print_html("[gut](https://a.de) und [böse](javascript:alert(1))")
        self.assertIn('<a href="https://a.de">gut</a>', html)
        self.assertNotIn("javascript:alert", html.replace("[böse](javascript:alert(1))", ""))
        self.assertNotIn('href="javascript', html)

    def test_image_embedded_as_data_url(self):
        html = pm.page_to_print_html(dokument_mit_bild(), image_data=lambda info: ("Foto", "image/png", b"\x89PNG-roh"))
        self.assertIn('<img src="data:image/png;base64,iVBORy1yb2g=" alt="Foto">', html)
        self.assertNotIn("file:", html)
        self.assertIn("Einleitung", html)
        self.assertIn("Schluss", html)

    def test_large_or_missing_image_stays_named_placeholder(self):
        gross = pm.page_to_print_html(dokument_mit_bild(), image_data=lambda info: ("Riesig", "image/jpeg", b"x" * 20),
                                      max_image_bytes=10)
        self.assertIn("[Bild: Riesig]", gross)
        self.assertNotIn("<img", gross)
        fehlt = pm.page_to_print_html(dokument_mit_bild(), image_data=lambda info: None)
        self.assertIn("[Bild: Bild]", fehlt)

    def test_tasks_and_tables(self):
        html = pm.markdown_to_print_html("- [ ] offen\n- [x] erledigt\n\n| a | b |\n|---|---|\n| 1 | 2 |")
        self.assertIn('<span class="box"></span>offen', html)
        self.assertIn("<s>erledigt</s>", html)
        self.assertIn("<td>1</td><td>2</td>", html)


if __name__ == "__main__":
    unittest.main()
