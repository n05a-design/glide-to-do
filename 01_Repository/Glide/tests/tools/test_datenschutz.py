"""Werkzeugtests für den Datenschutzschritt; keine App, keine Nutzerdaten."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import ci_grundstufe

_pfad = Path(__file__).resolve().parents[2] / "scripts/pflege/pfade_bereinigen.py"
_spec = importlib.util.spec_from_file_location("pfade_bereinigen", _pfad)
pfade_bereinigen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pfade_bereinigen)


# Zur Laufzeit zusammengesetzt: Als Literal würde der Datenschutzschritt
# diese Datei selbst melden.
KONTO = "an" + "na"


def konten(text):
    return [next(g for g in t.groups() if g) for t in ci_grundstufe.BENUTZERPFAD.finditer(text)]


class Benutzerpfade(unittest.TestCase):
    def test_plain_paths(self):
        self.assertEqual(konten(f"/Users/{KONTO}/Dokumente"), [KONTO])
        self.assertEqual(konten("C:\\Users\\" + KONTO + "\\Desktop"), [KONTO])
        self.assertEqual(konten(f"/home/{KONTO}/x"), [KONTO])

    def test_json_escaped_paths(self):
        # So schreibt Swifts JSONEncoder; bis 03.10.2026 blieb das unerkannt.
        self.assertEqual(konten('"\\/Users\\/' + KONTO + '\\/Library"'), [KONTO])
        self.assertEqual(konten('"C:\\\\Users\\\\' + KONTO + '\\\\x"'), [KONTO])
        self.assertEqual(konten('"\\/home\\/' + KONTO + '\\/x"'), [KONTO])

    def test_placeholders_stay_allowed(self):
        for text in ("/Users/Shared/x", "~/Library", "/Users/<Name>/", "/home/runner/work"):
            with self.subTest(text=text):
                erlaubt = all(k.lower() in ci_grundstufe.ERLAUBTE_KONTEN for k in konten(text))
                self.assertTrue(erlaubt)

    def test_cleaner_replaces_escaped_paths_and_keeps_json_valid(self):
        daten = {"pfad": f"/Users/{KONTO}/Library/x", "liste": ["/Users/Shared/y"]}
        roh = json.dumps(daten).replace("/", "\\/").encode()
        with tempfile.TemporaryDirectory(prefix="glide-datenschutz-") as ordner:
            datei = Path(ordner) / "probe.json"
            datei.write_bytes(roh)
            neu, anzahl = pfade_bereinigen.MAC.subn(lambda t: b"~" + t.group(1), roh)
            self.assertEqual(anzahl, 1)
            self.assertEqual(json.loads(neu)["pfad"], "~/Library/x")
            self.assertEqual(json.loads(neu)["liste"], ["/Users/Shared/y"])
            self.assertEqual(pfade_bereinigen.MAC.sub(lambda t: b"~" + t.group(1), f"/Users/{KONTO}/x".encode()), b"~/x")


if __name__ == "__main__":
    unittest.main()
