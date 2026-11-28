# SPDX-License-Identifier: MPL-2.0
"""`scripts/pflege/arbeitsstand_sichern.py`: Sicherung, Prüfung und Wiederherstellung (Master-Serie Teil 02).

Arbeitet in einem künstlichen Git-Repository im Temp-Ordner: geänderte,
gelöschte, umbenannte, binäre und neue Dateien werden gesichert und in einer
isolierten Kopie bytegleich wiederhergestellt; eine manipulierte Sicherung
und eine Geheimnisdatei werden abgewiesen; ignorierte Dateien bleiben draußen.
"""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

WERKZEUG = Path(__file__).resolve().parents[2] / "scripts" / "pflege" / "arbeitsstand_sichern.py"
spec = importlib.util.spec_from_file_location("arbeitsstand_sichern", WERKZEUG)
sichern = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sichern)


def git(ordner, *args):
    subprocess.run(["git", "-C", str(ordner), *args], check=True, capture_output=True)


class Sicherung(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="glide-sich-"))
        self.repo = self.temp / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "test@example.invalid")
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "config", "core.autocrlf", "false")
        (self.repo / "a.txt").write_text("eins\n", encoding="utf-8")
        (self.repo / "weg.txt").write_text("weg\n", encoding="utf-8")
        (self.repo / "alt.txt").write_text("umbenannt\n", encoding="utf-8")
        (self.repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "start")
        (self.repo / "a.txt").write_text("zwei\n", encoding="utf-8")
        (self.repo / "weg.txt").unlink()
        git(self.repo, "mv", "alt.txt", "neu.txt")
        (self.repo / "bild.png").write_bytes(bytes(range(256)))
        (self.repo / "ordner").mkdir()
        (self.repo / "ordner" / "notiz.md").write_text("neu\n", encoding="utf-8")
        (self.repo / "roh.log").write_text("nicht sichern\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.temp, ignore_errors=True)

    def test_gemischte_zeilenenden_werden_bytegenau_wiederhergestellt(self):
        """Teil 05B: Eine Arbeitskopie mit CRLF- und LF-Dateien, unverändert seit dem Commit.

        Ein frischer Klon würde Zeilenenden nach `core.autocrlf` setzen; der
        Baum-Abdruck stellt die tatsächlichen Bytes jeder Datei wieder her und
        meldet Abweichungen auch für nicht geänderte Dateien.
        """
        crlf = bytes((13, 10))
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "zwischen")
        (self.repo / "windows.txt").write_bytes(b"eins" + crlf + b"zwei" + crlf)
        (self.repo / "unix.txt").write_bytes(b"eins" + bytes((10,)))
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "gemischt")
        ordner, manifest = sichern.sichern(self.repo, self.temp / "ablage", "eol")
        self.assertTrue(manifest["baum"]["windows.txt"]["crlf"])
        self.assertFalse(manifest["baum"]["unix.txt"]["crlf"])
        _, abweichungen = sichern.wiederherstellen(ordner, self.temp / "kopie", quelle_repo=self.repo)
        self.assertEqual(abweichungen, [])
        kopie = self.temp / "kopie"
        self.assertEqual((kopie / "windows.txt").read_bytes(), b"eins" + crlf + b"zwei" + crlf)
        self.assertEqual((kopie / "unix.txt").read_bytes(), b"eins" + bytes((10,)))

    def test_unveraenderte_datei_mit_fremden_bytes_wird_gemeldet(self):
        ordner, _ = sichern.sichern(self.repo, self.temp / "ablage", "abdruck")
        manifest = sichern.manifest_lesen(ordner)
        # .gitignore ist seit dem Commit unverändert, steht also nur im Abdruck.
        manifest["baum"][".gitignore"]["sha256"] = "0" * 64
        import json
        (ordner / sichern.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
        _, abweichungen = sichern.wiederherstellen(ordner, self.temp / "kopie", quelle_repo=self.repo)
        self.assertEqual(abweichungen, ["abweichend (Bytes): .gitignore"])

    def test_rundlauf(self):
        ordner, manifest = sichern.sichern(self.repo, self.temp / "ablage", "probe")
        self.assertEqual(sichern.pruefen(ordner)[1], [])
        self.assertNotIn("roh.log", manifest["dateien"])
        self.assertIsNone(manifest["dateien"]["weg.txt"]["sha256"])
        manifest, abweichungen = sichern.wiederherstellen(ordner, self.temp / "kopie", quelle_repo=self.repo)
        self.assertEqual(abweichungen, [])
        kopie = self.temp / "kopie"
        self.assertEqual((kopie / "bild.png").read_bytes(), bytes(range(256)))
        self.assertFalse((kopie / "weg.txt").exists())
        self.assertTrue((kopie / "neu.txt").is_file())
        self.assertFalse((kopie / "roh.log").exists())

    def test_manipulierte_sicherung(self):
        ordner, _ = sichern.sichern(self.repo, self.temp / "ablage", "probe")
        with open(ordner / sichern.UNVERSIONIERT / "ordner" / "notiz.md", "a", encoding="utf-8") as datei:
            datei.write("x")
        self.assertEqual(sichern.pruefen(ordner)[1], ["verändert: unversioniert/ordner/notiz.md"])
        with self.assertRaises(sichern.SicherungsFehler):
            sichern.wiederherstellen(ordner, self.temp / "kopie", quelle_repo=self.repo)

    def test_geheimnis_und_ziel_in_der_arbeitskopie(self):
        (self.repo / ".env").write_text("TOKEN=x\n", encoding="utf-8")
        with self.assertRaises(sichern.SicherungsFehler) as fall:
            sichern.sichern(self.repo, self.temp / "ablage", "probe")
        self.assertEqual(fall.exception.code, 3)
        (self.repo / ".env").unlink()
        with self.assertRaises(sichern.SicherungsFehler):
            sichern.sichern(self.repo, self.repo / "innen", "probe")

    def test_zu_wenig_speicher_und_abbruch_hinterlassen_nichts(self):
        with self.assertRaises(sichern.SicherungsFehler) as fall:
            sichern.sichern(self.repo, self.temp / "ablage", "probe", reserve_mb=10 ** 9)
        self.assertEqual(fall.exception.code, 4)
        self.assertEqual(list((self.temp / "ablage").iterdir()), [])
        echt = sichern.shutil.copy2

        def kaputt(quelle, ziel, *a, **k):
            if str(quelle).endswith("notiz.md"):
                raise OSError("Datentraeger voll (simuliert)")
            return echt(quelle, ziel, *a, **k)

        sichern.shutil.copy2 = kaputt
        try:
            with self.assertRaises(OSError):
                sichern.sichern(self.repo, self.temp / "ablage", "probe")
        finally:
            sichern.shutil.copy2 = echt
        self.assertEqual(list((self.temp / "ablage").iterdir()), [], "halbe Sicherung liegengeblieben")


if __name__ == "__main__":
    unittest.main()
