"""Windows-Sandbox-Lauf (23.10.2026): Einfrieren, Konfiguration, Startskript, Bildschirmwahl.

Die Windows-Schritte selbst (Sandbox starten, Fenster legen) brauchen echtes
Windows; geprüft wird hier alles, was ohne Windows entscheidbar ist.
"""
import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import windows_sandbox as ws  # noqa: E402


class EinfrierenTests(unittest.TestCase):
    def baum(self, wurzel):
        dateien = {
            "01_Repository/Glide/VERSION": "3.44.0\n",
            "01_Repository/Glide/src/glide/app.pyw": "print('glide')\n",
            "01_Repository/Glide/src/glide/__pycache__/app.cpython-314.pyc": "x",
            "01_Repository/Glide/build/paket.zip": "x",
            "01_Repository/Glide/tests/tools/rest.pyc": "x",
            ".claude/skills/design-richtlinien/SKILL.md": "Skill\n",
            ".claude/worktrees/alt/datei.txt": "x",
            "00_Arbeitsvorbereitung/~$Plan.docx": "x",
            "00_Arbeitsvorbereitung/Glide_Uebergabe.md": "Übergabe\n",
            ".git/HEAD": "ref: refs/heads/arbeit\n",
            ".git/packed-refs": "# pack-refs\n0123abcd refs/heads/arbeit\n",
        }
        for name, inhalt in dateien.items():
            pfad = wurzel / name
            pfad.parent.mkdir(parents=True, exist_ok=True)
            pfad.write_text(inhalt, encoding="utf-8")

    def test_kopie_und_manifest(self):
        with tempfile.TemporaryDirectory() as ordner:
            quelle, ziel = Path(ordner) / "projekt", Path(ordner) / "kopie"
            self.baum(quelle)
            manifest = ws.einfrieren(quelle, ziel)
            kopiert = sorted(p.relative_to(ziel).as_posix() for p in ziel.rglob("*") if p.is_file())
            self.assertEqual(kopiert, [".claude/skills/design-richtlinien/SKILL.md",
                                       "00_Arbeitsvorbereitung/Glide_Uebergabe.md",
                                       "01_Repository/Glide/VERSION", "01_Repository/Glide/src/glide/app.pyw"])
            self.assertEqual(manifest["dateien"], 4)
            self.assertEqual(manifest["version"], "3.44.0")
            self.assertEqual(manifest["git_commit"], "0123abcd")
            erwartet = hashlib.sha256((quelle / "01_Repository/Glide/src/glide/app.pyw").read_bytes()).hexdigest()
            self.assertEqual(manifest["app_sha256"], erwartet)
            self.assertEqual(set(manifest["sha256"]), set(kopiert))
            with self.assertRaises(FileExistsError):
                ws.einfrieren(quelle, ziel)

    def test_git_commit_lose_und_ohne(self):
        with tempfile.TemporaryDirectory() as ordner:
            wurzel = Path(ordner)
            self.assertIsNone(ws.git_commit(wurzel))
            (wurzel / ".git/refs/heads").mkdir(parents=True)
            (wurzel / ".git/HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
            (wurzel / ".git/refs/heads/main").write_text("feedbeef\n", encoding="utf-8")
            self.assertEqual(ws.git_commit(wurzel), "feedbeef")
            (wurzel / ".git/HEAD").write_text("c0ffee\n", encoding="utf-8")
            self.assertEqual(ws.git_commit(wurzel), "c0ffee")


class PfadTests(unittest.TestCase):
    def test_onedrive_erkennen(self):
        wurzeln = ws.onedrive_wurzeln({"OneDrive": r"D:\Ablage\OneDrive", "PATH": "x"})
        self.assertEqual(wurzeln, [r"D:\Ablage\OneDrive"])
        self.assertTrue(ws.liegt_unter(r"d:\ablage\onedrive\Github\glide", wurzeln))
        self.assertFalse(ws.liegt_unter(r"D:\Ablage\GlidePruefung\lauf_1", wurzeln))
        self.assertFalse(ws.liegt_unter(r"D:\Ablage\OneDriveAlt\x", wurzeln))
        self.assertFalse(ws.liegt_unter(r"C:\x", []))


class DateiTests(unittest.TestCase):
    def test_konfiguration(self):
        text = ws.wsb_xml(r"C:\Prüfung\lauf & co\projekt", r"C:\Python314", r"C:\Prüfung\ergebnis", speicher=1000)
        self.assertTrue(text.isascii())
        wurzel = ET.fromstring(text)
        self.assertEqual(wurzel.findtext("Networking"), "Disable")
        self.assertEqual(wurzel.findtext("ClipboardRedirection"), "Disable")
        self.assertEqual(wurzel.findtext("MemoryInMB"), "2048")
        ordner = [(m.findtext("HostFolder"), m.findtext("SandboxFolder"), m.findtext("ReadOnly"))
                  for m in wurzel.iter("MappedFolder")]
        self.assertEqual(ordner, [(r"C:\Prüfung\lauf & co\projekt", ws.SANDBOX_PROJEKT, "false"),
                                  (r"C:\Python314", ws.SANDBOX_PYTHON, "true"),
                                  (r"C:\Prüfung\ergebnis", ws.SANDBOX_ERGEBNIS, "false")])
        self.assertEqual(wurzel.findtext("LogonCommand/Command"),
                         f"cmd.exe /c {ws.SANDBOX_ERGEBNIS}\\{ws.STARTSKRIPT}")

    def test_startskript(self):
        skript = ws.startskript()
        self.assertIn("\r\n", skript)
        self.assertIn(r'"C:\Python\python.exe" -B tests\tools\pruefen.py --modus voll --protokoll "C:\Ergebnis\protokoll"'
                      r' --timeout 900', skript)
        self.assertIn(r'cd /d "C:\Glide\01_Repository\Glide"', skript)
        # Exitcode über vorangestellte Umleitung, nicht „echo 1> Datei“.
        self.assertIn(r'> "C:\Ergebnis\FERTIG.txt" echo %ERRORLEVEL%', skript)
        self.assertNotIn("shutdown", skript)
        self.assertIn("shutdown /s", ws.startskript(schliessen=True))


class LaufzeitTests(unittest.TestCase):
    def test_grenze_und_auswahl(self):
        self.assertTrue(ws.laufzeit_geeignet("3.14.7", "9.0.4"))
        self.assertFalse(ws.laufzeit_geeignet("3.13.5", "9.0.1"))
        self.assertFalse(ws.laufzeit_geeignet("3.14.7", "8.6.15"))
        self.assertFalse(ws.laufzeit_geeignet("kaputt", "9"))
        with tempfile.TemporaryDirectory() as heim:
            self.assertEqual(ws.standard_python(heim, "/aufrufer"), Path("/aufrufer"))
            eigene = Path(heim) / ws.QA_LAUFZEIT
            eigene.mkdir(parents=True)
            (eigene / "python.exe").write_bytes(b"")
            self.assertEqual(ws.standard_python(heim, "/aufrufer"), eigene)


class BildschirmTests(unittest.TestCase):
    MONITORE = [{"links": 1920, "oben": 0, "breite": 2560, "hoehe": 1400, "haupt": False},
                {"links": 0, "oben": 0, "breite": 1920, "hoehe": 1040, "haupt": True},
                {"links": -1280, "oben": 100, "breite": 1280, "hoehe": 984, "haupt": False}]

    def test_wahl(self):
        self.assertTrue(ws.bildschirm_waehlen(self.MONITORE, 1)["haupt"])
        self.assertEqual(ws.bildschirm_waehlen(self.MONITORE)["links"], -1280)
        self.assertEqual(ws.bildschirm_waehlen(self.MONITORE, 3)["links"], 1920)
        self.assertTrue(ws.bildschirm_waehlen(self.MONITORE[1:2])["haupt"])
        with self.assertRaises(ValueError) as fehler:
            ws.bildschirm_waehlen(self.MONITORE, 4)
        self.assertIn("Hauptbildschirm", str(fehler.exception))
        with self.assertRaises(ValueError):
            ws.bildschirm_waehlen([])


class ErgebnisTests(unittest.TestCase):
    def test_zusammenfassung(self):
        text = ws.zusammenfassung({"exitcode": 1, "schritte": [
            {"schritt": "Syntax", "status": "ausgeführt"},
            {"schritt": "test_speicherlast330", "status": "fehlgeschlagen", "grund": "Exitcode 1"},
            {"schritt": "Sichtprüfung", "status": "übersprungen"}]})
        self.assertIn("3 Schritte", text)
        self.assertIn("1 fehlgeschlagen", text)
        self.assertIn("Exitcode 1", text)
        self.assertIn("rot: test_speicherlast330 – Exitcode 1", text)

    def test_ohne_windows_nur_dateien(self):
        if sys.platform == "win32":
            self.skipTest("Gegenprobe für andere Systeme")
        with contextlib.redirect_stderr(io.StringIO()) as meldung:
            self.assertEqual(ws.main(["--ziel", tempfile.gettempdir() + "/glide-sandbox-probe"]), 3)
        self.assertIn("--nur-dateien", meldung.getvalue())


if __name__ == "__main__":
    unittest.main()
