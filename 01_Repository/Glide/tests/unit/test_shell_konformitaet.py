# SPDX-License-Identifier: MPL-2.0
"""Shell 0.7.0: Versionsprüfung, Galerie-Register und Konformitätsprüfung (Master-Serie Teil 02).

Positiv gegen den echten Quellbaum, negativ gegen künstliche Projektbäume in
einem temporären Ordner: unzulässiger Import, privates Shell-Modul, Zyklus,
inkompatible Version und fehlende Galerie-Registrierung müssen erkannt werden.
"""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
sys.path.insert(0, str(SRC))

import glide_shell  # noqa: E402
from glide_shell import compat, conformance  # noqa: E402
from glide_shell.showcase import SHELL_COMPONENTS, ShowcaseEntry, ShowcaseRegistry, shell_entries  # noqa: E402


class Versionen(unittest.TestCase):
    def test_paketwerte(self):
        self.assertEqual(glide_shell.SHELL_VERSION, "0.10.0", "erwartete Fassung nach E02: allgemeine Bedienelemente, Farbrollen, Einstellungen, Arbeitsbereiche (unabhängig vom Paketwert gepflegt)")
        self.assertEqual(glide_shell.SHELL_COMPAT_SINCE, "0.6.2", "E02 erweitert nur kompatibel; Folgeprojekte mit 0.6.2 bleiben gültig")
        self.assertTrue(compat.compatible(glide_shell.SHELL_VERSION, "0.7.0", glide_shell.SHELL_COMPAT_SINCE))

    def test_regeln(self):
        self.assertTrue(compat.compatible("0.8.1", "0.7.0", "0.6.2"))
        self.assertFalse(compat.compatible("0.6.9", "0.7.0", "0.6.2"), "zu alte Shell")
        self.assertFalse(compat.compatible("0.9.0", "0.7.0", "0.9.0"), "Verbraucher vor einem inkompatiblen Schnitt")
        with self.assertRaises(ValueError):
            compat.parse_version("0.7")

    def test_require_shell_meldet_beide_faelle(self):
        with self.assertRaises(compat.ShellVersionError):
            compat.require_shell("0.8.0", "probe", installed="0.7.0", compat_since="0.6.2")
        with self.assertRaises(compat.ShellVersionError):
            compat.require_shell("0.7.0", "probe", installed="0.9.0", compat_since="0.9.0")
        self.assertEqual(compat.require_shell("0.7.0", "probe"), glide_shell.SHELL_VERSION)

    def test_bento_verlangt_passende_shell(self):
        import glide_bento
        self.assertEqual(glide_bento.BENTO_VERSION, "0.3.0")
        self.assertEqual(glide_bento.SHELL_MIN_VERSION, "0.7.0")


class Register(unittest.TestCase):
    def test_shell_eintraege_vollstaendig(self):
        registry = ShowcaseRegistry(shell_entries())
        self.assertEqual(registry.coverage(SHELL_COMPONENTS), [])
        self.assertTrue(all(e.build for e in registry))
        self.assertTrue(all(e.version == glide_shell.SHELL_VERSION for e in registry))

    def test_doppelte_kennung_und_fehlende_angaben(self):
        registry = ShowcaseRegistry(shell_entries())
        with self.assertRaises(ValueError):
            registry.register(shell_entries()[0])
        with self.assertRaises(ValueError):
            ShowcaseEntry("x", "", framework="f", version="1", module="m", summary="s")

    def test_fehlende_registrierung_wird_erkannt(self):
        registry = ShowcaseRegistry(shell_entries()[1:])
        self.assertEqual(registry.coverage(SHELL_COMPONENTS), [SHELL_COMPONENTS[0]])
        self.assertTrue(any("no productive usage" in p for p in registry.problems()))
        ohne = ShowcaseEntry("x.y", "Y", framework="f", version="1", module="m", summary="s", used_in=("a",))
        self.assertEqual(ShowcaseRegistry([ohne]).problems(), ["x.y: no builder"])


class Konformitaet(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="glide-konform-"))
        for paket in ("glide_shell", "glide_bento"):
            shutil.copytree(SRC / paket, self.temp / paket, ignore=shutil.ignore_patterns("__pycache__", "*.md"))
        (self.temp / "host.py").write_text("from glide_shell import modal_session\nimport glide_bento\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.temp, ignore_errors=True)

    def regeln(self):
        return sorted({f.rule for f in conformance.check_project(self.temp)})

    def test_echter_quellbaum_ist_konform(self):
        self.assertEqual(conformance.check_project(SRC), [])

    def test_kopie_ist_konform(self):
        self.assertEqual(self.regeln(), [])

    def test_shell_importiert_host_oder_bento(self):
        with open(self.temp / "glide_shell" / "motion.py", "a", encoding="utf-8") as datei:
            datei.write("\nimport host\nimport glide_bento\n")
        self.assertEqual(self.regeln(), ["shell-imports"])

    def test_bento_importiert_fachlogik_oder_privates(self):
        with open(self.temp / "glide_bento" / "layout.py", "a", encoding="utf-8") as datei:
            datei.write("\nimport host\nfrom glide_shell import _intern\n")
        befunde = conformance.check_project(self.temp)
        self.assertEqual({f.rule for f in befunde}, {"bento-imports"})
        self.assertEqual(len(befunde), 2)

    def test_host_nutzt_nicht_oeffentliches_modul(self):
        (self.temp / "host.py").write_text("from glide_shell import _intern\nimport glide_shell.geheim\n", encoding="utf-8")
        self.assertEqual([f.rule for f in conformance.check_project(self.temp)], ["public-api", "public-api"])

    def test_host_api_fehlender_name(self):
        """E02, Regel host-api: ein Host, der gegen eine andere Shell-Fassung geschrieben ist, fällt vor dem Import auf."""
        (self.temp / "host.py").write_text("from glide_shell.app_host import AppHost, gibt_es_nicht\n"
                                           "from glide_shell.controls import ShellButton, _font\n", encoding="utf-8")
        befunde = conformance.check_project(self.temp)
        self.assertEqual(sorted((f.rule, f.message.split(" ")[0]) for f in befunde),
                         [("host-api", "glide_shell.app_host.gibt_es_nicht"), ("host-api", "glide_shell.controls._font")])

    def test_host_api_aeltere_kopie(self):
        """Ein Host mit 0.10.0-Bausteinen gegen eine Kopie ohne `controls.py` meldet das fehlende Modul."""
        (self.temp / "host.py").write_text("from glide_shell.controls import ShellButton\n", encoding="utf-8")
        (self.temp / "glide_shell" / "controls.py").unlink()
        self.assertIn("host-api", self.regeln())

    def test_zyklus(self):
        with open(self.temp / "glide_bento" / "tokens.py", "a", encoding="utf-8") as datei:
            datei.write("\nfrom . import grid\n")
        self.assertIn("cycles", self.regeln())

    def test_inkompatible_version(self):
        kopf = self.temp / "glide_bento" / "__init__.py"
        kopf.write_text(kopf.read_text(encoding="utf-8").replace('SHELL_MIN_VERSION = "0.7.0"',
                                                                   'SHELL_MIN_VERSION = "0.11.0"'), encoding="utf-8")
        self.assertEqual(self.regeln(), ["versions"])

    def test_fehlende_mindestversion(self):
        kopf = self.temp / "glide_bento" / "__init__.py"
        kopf.write_text(kopf.read_text(encoding="utf-8").replace('SHELL_MIN_VERSION = "0.7.0"', ''), encoding="utf-8")
        self.assertEqual(self.regeln(), ["versions"])


if __name__ == "__main__":
    unittest.main()
