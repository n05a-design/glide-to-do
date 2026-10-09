"""KI-Austausch Stufe 2 (G24): Kontextpaket, Änderungsvorschlag, Konflikte – ohne Oberfläche."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import exchange_patch as ep

LABELS = {"L-a": "Kunde", "L-b": "Intern"}


def bestand():
    liste = {"id": "liste-1", "title": "Projekt", "note": "Wozu"}
    eltern = {"id": "p-1", "text": "Angebot", "importance": 2, "due": "2026-10-12", "labels": ["L-a"], "children": []}
    kind = {"id": "p-2", "text": "Preis klären", "done": False, "children": []}
    eltern["children"].append(kind)
    return liste, eltern, kind


class Austausch(unittest.TestCase):
    def test_context_has_refs_checksums_and_no_ids(self):
        liste, eltern, kind = bestand()
        paket = ep.build_context([(liste, eltern, None), (liste, kind, eltern)], LABELS, "2026-10-09T12:00")
        text = repr(paket)
        for kennung in ("liste-1", "p-1", "p-2", "L-a"):
            self.assertNotIn(kennung, text)
        self.assertEqual(paket["format"], "glide.context")
        self.assertEqual(paket["items"][1]["parent"], ep.ref("p-1"))
        self.assertEqual(paket["items"][0]["fields"]["labels"], ["Kunde"])
        self.assertEqual(paket["items"][0]["base"], ep.checksum(ep.item_state(eltern, LABELS)))

    def test_patch_frame_is_checked(self):
        for kaputt in (None, {"format": "x"}, {"format": "glide.exchange", "format_version": 1, "mode": "patch",
                                                "changes": [{}]},
                       {"format": "glide.exchange", "format_version": 2, "mode": "patch", "changes": []},
                       {"format": "glide.exchange", "format_version": 2, "mode": "patch", "changes": [{"ref": "x"}]}):
            with self.subTest(kaputt=kaputt):
                with self.assertRaises(ep.PatchError):
                    ep.parse_patch(kaputt)

    def test_ok_conflict_unknown_invalid_unchanged(self):
        liste, eltern, kind = bestand()
        punkte = {ep.ref("p-1"): eltern, ep.ref("p-2"): kind}
        basis = {r: ep.checksum(ep.item_state(p, LABELS)) for r, p in punkte.items()}
        vorschlag = {"format": "glide.exchange", "format_version": 2, "mode": "patch", "changes": [
            {"ref": ep.ref("p-1"), "base": basis[ep.ref("p-1")], "set": {"due": "2026-10-15", "labels": ["Intern"]}},
            {"ref": ep.ref("p-2"), "base": "0" * 16, "set": {"done": True}},
            {"ref": ep.ref("weg"), "base": "x", "set": {"title": "Neu"}},
        ]}
        vorher = copy.deepcopy((eltern, kind))
        aenderungen = ep.parse_patch(vorschlag)
        resolve = lambda r: (punkte[r], LABELS) if r in punkte else None
        ergebnis = ep.check_patch(aenderungen, resolve, known_labels=LABELS.values())
        self.assertEqual([e["status"] for e in ergebnis], ["ok", "conflict", "unknown"])
        self.assertEqual(ergebnis[0]["diffs"], [("Fälligkeit", "2026-10-12", "2026-10-15"),
                                                ("Labels", ["Kunde"], ["Intern"])])
        self.assertEqual(ergebnis[0]["values"], {"due": "2026-10-15", "labels": ["Intern"]})
        self.assertEqual((eltern, kind), vorher)  # Vorschau ändert nichts
        ungueltig = ep.check_patch([{"ref": ep.ref("p-1"), "base": basis[ep.ref("p-1")],
                                     "set": {"importance": 7, "farbe": "rot", "labels": ["Neu"]}}],
                                   resolve, known_labels=LABELS.values())
        self.assertEqual(ungueltig[0]["status"], "invalid")
        self.assertEqual(len(ungueltig[0]["messages"]), 3)
        gleich = ep.check_patch([{"ref": ep.ref("p-1"), "base": basis[ep.ref("p-1")], "set": {"importance": 2}}],
                                resolve)
        self.assertEqual(gleich[0]["status"], "unchanged")
        self.assertIn("1 anwendbar", ep.summary(ergebnis))
        self.assertIn("1 Konflikte", ep.summary(ergebnis))

    def test_values(self):
        self.assertEqual(ep.validate_value("title", "  Neuer   Titel "), "Neuer Titel")
        self.assertIsNone(ep.validate_value("due", None))
        for feld, wert in (("due", "12.10.2026"), ("due_time", "25:00"), ("estimated_minutes", 0),
                           ("done", "ja"), ("labels", "Kunde"), ("title", "")):
            with self.subTest(feld=feld):
                with self.assertRaises(ValueError):
                    ep.validate_value(feld, wert)

    def test_duplicate_ref_is_invalid(self):
        liste, eltern, kind = bestand()
        b = ep.checksum(ep.item_state(eltern, LABELS))
        ergebnis = ep.check_patch([{"ref": ep.ref("p-1"), "base": b, "set": {"done": True}}] * 2,
                                  lambda r: (eltern, LABELS))
        self.assertEqual([e["status"] for e in ergebnis], ["ok", "invalid"])


if __name__ == "__main__":
    unittest.main()
