# SPDX-License-Identifier: MPL-2.0
"""Werkzeugtest L4 (Glide 1.1.0): drei Referenzvorlagen DE/EN im mitgelieferten Katalog.

Prüft ohne Tk, dass `scripts/pflege/vorlagen_l4.py` den Katalog aktuell hält,
beide Sprachfassungen Vorlagenformat 2 und dieselben Kennungen, Termine und
Platzhalter tragen, Beziehungen nur auf Punkte derselben Vorlage zeigen,
Label- und Listenfarben gültig sind und keine Verweise auf Beispiel- oder
Showcase-Daten enthalten sind.
"""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "src/glide/resources/templates"
L4 = ("client-project", "design-project", "weekly-review")
FARBEN = {"accent", "clear", "due_action", "export", "flag", "delete"}
PLATZHALTER = re.compile(r"\{\{\s*([^{}\n]{1,40}?)\s*\}\}")


def lade(name):
    return json.loads((TEMPLATES / name).read_text(encoding="utf-8"))


def werkzeug():
    spec = importlib.util.spec_from_file_location("vorlagen_l4", ROOT / "scripts/pflege/vorlagen_l4.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def punkte(liste):
    stapel = list(liste.get("items", []))
    while stapel:
        punkt = stapel.pop(0)
        yield punkt
        stapel.extend(punkt.get("children", []))


class VorlagenL4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.de = lade("glide_vorlagen.glidetemplates")
        cls.en = lade("glide_vorlagen.en.glidetemplates")

    def vorlage(self, katalog, vid):
        return next(t for t in katalog["templates"] if t["id"] == vid)

    def test_werkzeug_haelt_katalog_aktuell(self):
        katalog, kern = werkzeug().erzeugen()
        self.assertEqual(katalog, (TEMPLATES / "glide_vorlagen.glidetemplates").read_text(encoding="utf-8"))
        self.assertEqual(json.loads(kern), json.loads((ROOT / "scripts/pflege/vorlagen_en.json").read_text(encoding="utf-8")))

    def test_formatversion_und_bestand_bleibt(self):
        for katalog in (self.de, self.en):
            self.assertEqual(katalog["format_version"], 2)
            ids = [t["id"] for t in katalog["templates"]]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertTrue(set(L4) <= set(ids))
            for alt in ("daily", "project", "week", "folder-project", "construction"):
                self.assertIn(alt, ids, "vorhandene Vorlagen bleiben")

    def test_sprachparitaet(self):
        for vid in L4:
            de, en = self.vorlage(self.de, vid), self.vorlage(self.en, vid)
            self.assertEqual(de["kind"], en["kind"])
            self.assertEqual(de["schedule_anchor"], en["schedule_anchor"])
            self.assertNotEqual(de["title"], en["title"])
            pd, pe = de["payload"], en["payload"]
            self.assertEqual(pd["version"], 26)
            self.assertEqual([l["id"] for l in pd["lists"]], [l["id"] for l in pe["lists"]])
            for ld, le in zip(pd["lists"], pe["lists"]):
                for a, b in zip(punkte(ld), punkte(le)):
                    self.assertEqual((a["id"], a["due"], a["planned_date"], a["blocked_by"], a["kind"]),
                                     (b["id"], b["due"], b["planned_date"], b["blocked_by"], b["kind"]))
                    self.assertEqual(len(PLATZHALTER.findall(a["text"])), len(PLATZHALTER.findall(b["text"])))
                    self.assertNotRegex(b["text"] + b["description"], "[äöüßÄÖÜ]", b["text"])

    def test_beziehungen_farben_und_keine_fremdverweise(self):
        for katalog in (self.de, self.en):
            for vid in L4:
                vorlage = self.vorlage(katalog, vid)
                payload = vorlage["payload"]
                alle = {p["id"] for l in payload["lists"] for p in punkte(l)}
                label_ids = {l["id"] for l in payload["labels"]}
                self.assertTrue(set(vorlage["labels"]) <= label_ids)
                for liste in payload["lists"]:
                    self.assertIn(liste["color"], FARBEN | {None})
                    for punkt in punkte(liste):
                        self.assertTrue(set(punkt["blocked_by"]) <= alle, punkt["text"])
                        self.assertNotIn(punkt["id"], punkt["blocked_by"])
                        self.assertTrue(set(punkt["labels"]) <= label_ids, punkt["text"])
                for label in payload["labels"]:
                    self.assertIn(label["color"], FARBEN)
                text = json.dumps(vorlage, ensure_ascii=False)
                for fremd in ("Stadtlicht", "City Light", "Wuppertal", "showcase"):
                    self.assertNotIn(fremd, text)

    def test_inhalte_der_spezifikation(self):
        texte = {vid: json.dumps(self.vorlage(self.de, vid)["payload"], ensure_ascii=False) for vid in L4}
        for begriff in ("Kundenbriefing", "Ziele und Anforderungen", "Phase 1", "Meilenstein", "Feedback",
                        "Abnahme", "Übergabe"):
            self.assertIn(begriff, texte["client-project"], begriff)
        for begriff in ("Inspiration", "Moodboard", "Konzept", "Entwurfsrunde", "Variante", "Revision", "Freigabe",
                        "Asset"):
            self.assertIn(begriff, texte["design-project"], begriff)
        for begriff in ("Wochenabsichten", "Fokusziele", "Termine", "Puffer", "Aufgaben der Woche", "Wochenrückblick"):
            self.assertIn(begriff, texte["weekly-review"], begriff)


if __name__ == "__main__":
    unittest.main()
