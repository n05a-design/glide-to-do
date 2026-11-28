# SPDX-License-Identifier: MPL-2.0
"""Unit-Tests für kontextuelle Leerzustände (WA-52, Glide 1.1.0, Tk-frei nach D17)."""
from pathlib import Path
import json
import sys
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import empty_states  # noqa: E402
import i18n  # noqa: E402


class EmptyStateTests(unittest.TestCase):
    def tearDown(self):
        i18n.set_language("de")

    def test_alle_sechs_kontexte_haben_titel_erklaerung_und_aktion(self):
        for context in empty_states.CONTEXTS:
            state = empty_states.empty_state(context)
            self.assertTrue(state.title, context)
            self.assertTrue(state.description, context)
            if context != "list":
                self.assertIsNotNone(state.primary, context)
            for action_id in state.action_ids:
                self.assertIn(action_id, empty_states.ACTIONS)

    def test_filter_fuehrt_zu_zuruecksetzen_statt_anlegen(self):
        for context, kwargs in (("today", {"filtered": True}),
                                ("pinboard", {"has_cards": True}), ("journal", {"filtered": True})):
            state = empty_states.empty_state(context, **kwargs)
            self.assertEqual(state.primary[0], "clear_filter", context)
            self.assertIsNone(state.secondary)
        self.assertEqual(empty_states.empty_state("journal", date_range=True).primary[0], "show_all_days")

    def test_heute_ohne_offene_aufgaben_fuehrt_zum_eingang(self):
        self.assertEqual(empty_states.empty_state("today").primary[0], "plan_day")
        self.assertEqual(empty_states.empty_state("today", has_tasks=False).primary[0], "open_inbox")
        anderer = empty_states.empty_state("today", other_day=True)
        self.assertNotEqual(anderer.title, empty_states.empty_state("today").title)

    def test_pinnwand_aktion_fuehrt_zur_objektauswahl(self):
        self.assertEqual(empty_states.empty_state("pinboard").primary[0], "pin_items")

    def test_hinweise_aus_kuerzen_nur_den_bedienhinweis(self):
        for context in empty_states.CONTEXTS:
            self.assertTrue(empty_states.empty_state(context, hints=False).description, context)
        self.assertEqual(empty_states.empty_state("pages", hints=False).action_ids, ("new_page", "use_template"))

    def test_text_ist_titel_und_erklaerung(self):
        state = empty_states.empty_state("journal")
        self.assertEqual(state.text, f"{state.title}\n{state.description}")

    def test_knopftexte_hoechstens_24_zeichen_b11(self):
        import ui_design
        varianten = [dict(), dict(filtered=True), dict(has_tasks=False),
                     dict(has_cards=True), dict(date_range=True), dict(other_day=True)]
        for sprache in ("de", "en"):
            i18n.set_language(sprache)
            for context in empty_states.CONTEXTS:
                for kwargs in varianten:
                    for action in (empty_states.empty_state(context, **kwargs).primary,
                                   empty_states.empty_state(context, **kwargs).secondary):
                        if action:
                            self.assertLessEqual(len(action[1]), ui_design.BUTTON_TEXT_MAX_CHARS, action)

    def test_unbekannter_kontext(self):
        with self.assertRaises(ValueError):
            empty_states.empty_state("dashboard")

    def test_sprachparitaet_de_en(self):
        katalog = {}
        for sprache in ("de", "en"):
            pfad = SRC / "resources" / "locales" / f"{sprache}.json"
            katalog[sprache] = {k for k in json.loads(pfad.read_text(encoding="utf-8")) if k.startswith("mod.empty_states.")}
        self.assertTrue(katalog["de"])
        self.assertEqual(katalog["de"], katalog["en"])
        quelltext = (SRC / "empty_states.py").read_text(encoding="utf-8")
        import re
        benutzt = {f"mod.empty_states.{k}" for k in re.findall(r'_t\("([a-z_.]+)"', quelltext)}
        benutzt |= {f"mod.empty_states.action.{k}" for k in re.findall(r'"([a-z_]+)": \("\1", ', quelltext)}
        self.assertTrue(benutzt <= katalog["de"], benutzt - katalog["de"])
        i18n.set_language("en")
        en = empty_states.empty_state("today")
        self.assertEqual(en.title, "Nothing is planned for today yet")
        self.assertEqual(en.primary[1], "Plan the workday …")
        for context in empty_states.CONTEXTS:
            state = empty_states.empty_state(context)
            self.assertNotRegex(state.title + state.description, "[äöüß]", context)


if __name__ == "__main__":
    unittest.main()
