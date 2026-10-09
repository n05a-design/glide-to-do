"""Sicherungsstände vergleichen (F-03) ohne Oberfläche und ohne Dateien."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import backup_diff as bd


def punkt(kennung, text, **werte):
    basis = {"id": kennung, "text": text, "done": False, "children": []}
    basis.update(werte)
    return basis


def stand():
    return {"lists": [
        {"id": "L1", "title": "Arbeit", "items": [punkt("a", "Bericht", children=[punkt("a1", "Entwurf")]),
                                                   punkt("b", "Angebot", due="2026-10-09")]},
        {"id": "L2", "title": "Privat", "items": [punkt("c", "Einkauf")]},
        {"id": "L3", "title": "Alt", "items": []},
    ]}


class Vergleich(unittest.TestCase):
    def test_identical_has_no_differences(self):
        ergebnis = bd.compare(stand(), stand())
        self.assertTrue(all(not werte for werte in ergebnis.values()))
        self.assertEqual(bd.summary(ergebnis), "Keine Unterschiede bei Listen und Aufgaben")

    def test_all_kinds_of_change(self):
        alt, neu = stand(), stand()
        neu["lists"][0]["title"] = "Arbeit 2026"
        neu["lists"][0]["items"][1].update(done=True, due="2026-10-10")
        neu["lists"][0]["items"][0]["children"][0]["text"] = "Entwurf fertig"
        neu["lists"][1]["items"].append(punkt("d", "Neu"))
        neu["lists"][1]["items"].append(neu["lists"][0]["items"].pop(1))  # „Angebot“ wandert nach Privat
        del neu["lists"][2]
        neu["lists"].append({"id": "L4", "title": "Projekt", "items": []})
        vorher = copy.deepcopy(alt)
        ergebnis = bd.compare(alt, neu)
        self.assertEqual(alt, vorher)  # liest nur
        self.assertEqual(ergebnis["lists_added"], [("L4", "Projekt")])
        self.assertEqual(ergebnis["lists_removed"], [("L3", "Alt")])
        self.assertEqual(ergebnis["lists_changed"], [("L1", "Arbeit 2026", [("Titel", "Arbeit", "Arbeit 2026")])])
        self.assertEqual(ergebnis["items_added"], [("d", "Neu", "Privat")])
        self.assertEqual(ergebnis["items_moved"], [("b", "Angebot", "Arbeit", "Privat")])
        geaendert = {kennung: felder for kennung, _n, _l, felder in ergebnis["items_changed"]}
        self.assertEqual(geaendert["b"], [("Erledigt", "nein", "ja"), ("Fälligkeit", "2026-10-09", "2026-10-10")])
        self.assertEqual(geaendert["a1"], [("Titel", "Entwurf", "Entwurf fertig")])
        self.assertIn("1 Listen neu", bd.summary(ergebnis))
        self.assertIn("2 Aufgaben geändert", bd.summary(ergebnis))

    def test_empty_values_are_equal_and_removed_items(self):
        alt, neu = stand(), stand()
        alt["lists"][1]["items"][0]["labels"] = []
        neu["lists"][1]["items"][0]["labels"] = None
        neu["lists"][0]["items"][0]["children"] = []
        ergebnis = bd.compare(alt, neu)
        self.assertEqual(ergebnis["items_removed"], [("a1", "Entwurf", "Arbeit")])
        self.assertEqual(ergebnis["items_changed"], [])

    def test_describe_is_short(self):
        self.assertEqual(bd.describe(None), "–")
        self.assertEqual(bd.describe(["x", "y"]), "x, y")
        self.assertTrue(bd.describe("a" * 200).endswith("…"))
        self.assertEqual(bd.describe({"text": "Seitentext"}), "Seitentext")
        self.assertEqual(bd.compare(None, {})["lists_added"], [])


if __name__ == "__main__":
    unittest.main()
