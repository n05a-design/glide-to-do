"""Starter für Sicht-/Bedienabnahmen am Quellstand (25.10.2026): Ordner und Showcase-Wahl."""
import importlib.machinery
import importlib.util
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

PFAD = Path(__file__).resolve().parent / "kandidat_starten.pyw"
_loader = importlib.machinery.SourceFileLoader("kandidat_starten", str(PFAD))
ks = importlib.util.module_from_spec(importlib.util.spec_from_loader(_loader.name, _loader))
_loader.exec_module(ks)


class KandidatStartenTests(unittest.TestCase):
    def test_pruefordner_liegt_ausserhalb_des_projekts(self):
        ordner = ks.pruefordner("/heim/nutzer")
        self.assertEqual(ordner, Path("/heim/nutzer/GlidePruefung/kandidat_showcase"))
        self.assertFalse(ordner.is_relative_to(ks.ABLAGE))

    def test_showcase_wahl_mit_rueckfall(self):
        with tempfile.TemporaryDirectory() as tmp:
            ablage, repo = Path(tmp) / "ablage", Path(tmp) / "repo"
            self.assertIsNone(ks.showcase_backup(ablage, repo))
            fixture = repo / "tests/fixtures/showcase/Glide-Showcase_App.glideapp"
            fixture.parent.mkdir(parents=True)
            fixture.write_bytes(b"x")
            self.assertEqual(ks.showcase_backup(ablage, repo), fixture)
            aktiv = ablage / "05_Probelisten_Testdaten/Showcase/Glide-Showcase_App.glideapp"
            aktiv.parent.mkdir(parents=True)
            aktiv.write_bytes(b"y")
            self.assertEqual(ks.showcase_backup(ablage, repo), aktiv)

    def test_neu_beginnen_benennt_um_statt_zu_loeschen(self):
        with tempfile.TemporaryDirectory() as tmp:
            ordner = Path(tmp) / "kandidat_showcase"
            self.assertIsNone(ks.neu_beginnen(ordner))
            ordner.mkdir()
            (ordner / "liste_speicher.json").write_text("{}", encoding="utf-8")
            ziel = ks.neu_beginnen(ordner, datetime(2026, 10, 25, 15, 30, 0))
            self.assertEqual(ziel.name, "kandidat_showcase_20261025-153000")
            self.assertFalse(ordner.exists())
            self.assertTrue((ziel / "liste_speicher.json").is_file())

    def test_echter_showcase_im_projekt_vorhanden(self):
        self.assertIsNotNone(ks.showcase_backup())
        self.assertTrue((ks.REPO / "src/glide/app.pyw").is_file())


if __name__ == "__main__":
    unittest.main()
