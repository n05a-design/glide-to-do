# SPDX-License-Identifier: MPL-2.0
"""Unit-Tests für `component_gallery` (D105, Komponenten-Galerie, Tk-frei)."""
import json
from pathlib import Path
import sys
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
sys.path.insert(0, str(SRC))

import component_gallery as galerie  # noqa: E402


class Galerie(unittest.TestCase):
    def test_register_vollstaendig_und_ohne_probleme(self):
        registry = galerie.build_registry()
        self.assertEqual(galerie.missing_components(registry), [])
        self.assertEqual(galerie.registry_problems(registry), [])
        self.assertEqual(set(galerie.GLIDE_USAGE), set(galerie.expected_components()))
        self.assertEqual(registry.frameworks(), ["Glide Shell", "Glide Bento"])

    def test_fehlender_einsatzort_faellt_auf(self):
        usage = dict(galerie.GLIDE_USAGE)
        usage.pop("bento.metric")
        probleme = galerie.registry_problems(galerie.build_registry(usage))
        self.assertEqual(probleme, ["bento.metric: no productive usage noted (write 'gallery only' explicitly)"])

    def test_versionen_kommen_aus_den_paketen(self):
        import glide_bento
        import glide_shell
        for entry in galerie.build_registry():
            erwartet = glide_shell.SHELL_VERSION if entry.framework == "Glide Shell" else glide_bento.BENTO_VERSION
            self.assertEqual(entry.version, erwartet, entry.id)

    def test_breiten_und_rueckfall(self):
        self.assertEqual(galerie.width_for("narrow"), 360)
        self.assertEqual(galerie.width_for("unbekannt"), galerie.width_for(galerie.DEFAULT_WIDTH))

    def test_einsatztexte_in_beiden_katalogen(self):
        locales = SRC / "resources" / "locales"
        kataloge = {s: json.loads((locales / f"{s}.json").read_text(encoding="utf-8")) for s in ("de", "en")}
        schluessel = {"ui.component_gallery.usage.gallery_only"}
        for eintraege in galerie.GLIDE_USAGE.values():
            for item in eintraege:
                if item != galerie.GALLERY_ONLY:
                    schluessel.add(item[0])
                    self.assertEqual(kataloge["de"][item[0]], item[1])
        for sprache, katalog in kataloge.items():
            self.assertEqual(schluessel - set(katalog), set(), sprache)
        entry = galerie.build_registry().get("bento.metric")
        self.assertEqual(galerie.usage_texts(entry, lambda k, f: f), ["Nur in der Galerie"])


if __name__ == "__main__":
    unittest.main()
