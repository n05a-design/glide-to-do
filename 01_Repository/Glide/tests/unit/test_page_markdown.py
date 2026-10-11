import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import page_markdown as markdown


class MarkdownTests(unittest.TestCase):
    def test_reference_export_uses_real_title_and_state(self):
        doc = dict(text='Alter Titel', links={}, spans=[dict(tag='task', start=0, end=11),
                    dict(tag='taskref:a', start=0, end=11)])
        self.assertEqual(markdown.page_to_markdown(doc, lambda _: ('Neuer Titel 😀', True)), '- [x] Neuer Titel 😀\n')

    def test_block_insertion_splits_format_and_keeps_images(self):
        doc = dict(text='a😀b', links={}, images={'img:x': {'attachment': 'x'}},
                   spans=[dict(tag='bold', start=0, end=3)])
        old = copy.deepcopy(doc)
        addition = dict(text='Aufgabe', spans=[dict(tag='item:a', start=0, end=7)], links={})
        result = markdown.insert_blocks(doc, addition, 2, {})
        self.assertEqual(result['text'], 'a😀\nAufgabe\nb')
        self.assertEqual(result['spans'], [dict(tag='bold', start=0, end=2),
            dict(tag='bold', start=11, end=12), dict(tag='item:a', start=3, end=10)])
        self.assertEqual(result['images'], doc['images'])
        self.assertEqual(doc, old)

    def test_link_collision_remap(self):
        doc = dict(text='x', spans=[], links={'link:a': 'https://old.example'})
        addition = dict(text='y', spans=[dict(tag='link:a', start=0, end=1)], links={'link:a': 'https://new.example'})
        result = markdown.insert_blocks(doc, addition, 1, {'link:a': 'link:b'})
        self.assertEqual(result['links'], {'link:a': 'https://old.example', 'link:b': 'https://new.example'})
        self.assertEqual(result['spans'][0]['tag'], 'link:b')
        with self.assertRaises(ValueError):
            markdown.insert_blocks(doc, addition, True, {})


class BilderImRundlauf(unittest.TestCase):
    """B4 (3.34.0): Bildverweise werden mit gefundener Datei wieder Seitenbilder."""

    def test_local_image_path(self):
        import os
        from page_markdown import local_image_path
        basis = Path.cwd() / "Bildquellen"
        absolut = basis / "a b.png"
        self.assertEqual(local_image_path(absolut.as_uri()), os.path.normpath(str(absolut)))
        self.assertEqual(local_image_path("Bilder/a%20b.png", basis),
                         os.path.normpath(str(basis / "Bilder/a b.png")))
        self.assertEqual(local_image_path(str(absolut)), os.path.normpath(str(absolut)))
        # Seit Python 3.13 ist ein einzelner führender Slash unter Windows
        # laufwerksrelativ. Ohne Basis wird kein solches Bild geladen.
        if os.name == "nt":
            self.assertIsNone(local_image_path("/abs/c.png"))
            self.assertIsNone(local_image_path(r"C:relativ.png"))
        else:
            self.assertEqual(local_image_path("/abs/c.png"), "/abs/c.png")
        for fremd in ("https://example.org/a.png", "data:image/png;base64,AAAA", "file://server/a.png", "", None):
            self.assertIsNone(local_image_path(fremd, basis), fremd)
        self.assertIsNone(local_image_path("relativ.png"))

    def test_image_line_becomes_anchor_only_when_resolved(self):
        from page_markdown import IMAGE_ANCHOR, markdown_to_page
        gesehen = []

        def finden(beschreibung, quelle):
            gesehen.append((beschreibung, quelle))
            return ("img:" + "a" * 16, {"attachment": "x1", "mode": "center", "width": 300}) if quelle == "da.png" else None

        dokument = markdown_to_page("Text\n\n![Da](da.png)\n\n![Weg](weg.png)\n\nInline ![Im](da.png) Satz", finden)
        zeilen = dokument["text"].split("\n")
        self.assertEqual(zeilen[1], IMAGE_ANCHOR)
        self.assertIn("Bild: Weg", zeilen[2])
        self.assertIn("Bild: Im", zeilen[3])  # nur Bilder allein auf ihrer Zeile werden Seitenbilder
        self.assertEqual(gesehen, [("Da", "da.png"), ("Weg", "weg.png")])
        self.assertEqual(dokument["images"], {"img:" + "a" * 16: {"attachment": "x1", "mode": "center", "width": 300}})
        anker = next(span for span in dokument["spans"] if span["tag"].startswith("img:"))
        self.assertEqual(dokument["text"][anker["start"]:anker["end"]], IMAGE_ANCHOR)
        self.assertNotIn("images", markdown_to_page("![Da](da.png)"))

    def test_insert_blocks_keeps_both_image_sets(self):
        from page_markdown import IMAGE_ANCHOR, insert_blocks
        alt = {"text": IMAGE_ANCHOR + "\nAlt", "spans": [{"tag": "img:" + "1" * 16, "start": 0, "end": 1}],
               "links": {}, "images": {"img:" + "1" * 16: {"attachment": "a"}}}
        neu = {"text": IMAGE_ANCHOR, "spans": [{"tag": "img:" + "2" * 16, "start": 0, "end": 1}], "links": {},
               "images": {"img:" + "2" * 16: {"attachment": "b"}}}
        ergebnis = insert_blocks(alt, neu, len(alt["text"]), {})
        self.assertEqual(set(ergebnis["images"]), {"img:" + "1" * 16, "img:" + "2" * 16})
        self.assertEqual(insert_blocks(alt, dict(neu, images={}), 0, {})["images"], alt["images"])

    def test_export_and_import_round_trip(self):
        from page_markdown import IMAGE_ANCHOR, markdown_to_page, page_to_markdown
        seite = {"text": "Vorher\n" + IMAGE_ANCHOR + "\nNachher",
                 "spans": [{"tag": "img:" + "c" * 16, "start": 7, "end": 8}], "links": {},
                 "images": {"img:" + "c" * 16: {"attachment": "a9", "mode": "left", "width": 200}}}
        markdown = page_to_markdown(seite, image_source=lambda info: ("Foto", "Seite%20Bilder/foto.png"))
        self.assertIn("![Foto](Seite%20Bilder/foto.png)", markdown)
        zurueck = markdown_to_page(markdown, lambda b, q: ("img:" + "d" * 16, {"attachment": "neu", "src": q}))
        self.assertEqual(zurueck["text"].split("\n"), ["Vorher", IMAGE_ANCHOR, "Nachher"])
        self.assertEqual(list(zurueck["images"].values()), [{"attachment": "neu", "src": "Seite%20Bilder/foto.png"}])


if __name__ == '__main__':
    unittest.main()
