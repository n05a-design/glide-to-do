# SPDX-License-Identifier: MPL-2.0
"""UX-05 (27.11.2026): Leerzustände als Handlungsaufforderung."""
import json
from pathlib import Path
import sys
import unittest

GLIDE = Path(__file__).resolve().parents[2] / "src/glide"
sys.path.insert(0, str(GLIDE))
import empty_states as es


def alle_zustaende():
    return [es.list_state(), es.list_state(filtered=True), es.list_state(read_only=True),
            es.list_state(accepts_items=False), es.overview_state("pages", read_only=True),
            *es.OVERVIEWS.values(), *es.MENUS.values(),
            *(es.folder_state(art) for art in ("folder", "journal", "book")),
            es.folder_state(searched=True), es.folder_state("journal", period_filtered=True),
            es.folder_state(read_only=True)]


class EmptyStateTests(unittest.TestCase):
    def test_list_rules(self):
        self.assertEqual(es.list_state().action, es.FOCUS_ENTRY)
        self.assertEqual(es.list_state(filtered=True).action, es.RESET_FILTER, "Filter hat Vorrang")
        self.assertEqual(es.list_state(filtered=True, read_only=True).action, es.RESET_FILTER)
        self.assertIsNone(es.list_state(read_only=True).action)
        self.assertIsNone(es.list_state(accepts_items=False).action)

    def test_overviews_and_menus(self):
        for kind, action in (("pages", es.CREATE_PAGE), ("notes", es.CREATE_NOTE),
                             ("drawings", es.CREATE_DRAWING), ("notebooks", es.CREATE_NOTEBOOK),
                             ("galleries", es.CREATE_GALLERY), ("boards", es.OPEN_GLOBAL_BOARD),
                             ("labels", es.MANAGE_LABELS), ("library", es.CREATE_LIST),
                             ("templates", es.IMPORT_TEMPLATES), ("gallery_images", es.ADD_IMAGES)):
            self.assertEqual(es.overview_state(kind).action, action)
            self.assertIsNone(es.overview_state(kind, read_only=True).action)
        self.assertIsNone(es.overview_state("unbekannt"))
        self.assertEqual(es.menu_state("labels").action, es.MANAGE_LABELS)
        self.assertEqual(es.menu_state("areas").action, es.CREATE_AREA)
        self.assertIsNone(es.menu_state("unbekannt"))

    def test_folder_rules(self):
        self.assertEqual(es.folder_state().action, es.FOCUS_ENTRY)
        self.assertEqual(es.folder_state("book").action, es.FOCUS_ENTRY)
        self.assertEqual(es.folder_state("journal").action, es.CREATE_JOURNAL_ENTRY,
                         "die Eingabezeile legt im Notizbuch keinen Eintrag an")
        self.assertEqual(es.folder_state("journal", searched=True).action, es.RESET_FILTER, "Suche zuerst")
        self.assertEqual(es.folder_state("journal", period_filtered=True).action, es.SHOW_ALL_DAYS)
        self.assertEqual(es.folder_state("folder", period_filtered=True).action, es.FOCUS_ENTRY,
                         "Zeitraum gilt nur im Notizbuch")
        self.assertIsNone(es.folder_state("journal", read_only=True).action)

    def test_texts_are_prompts_and_ellipsis_only_for_dialogs(self):
        for zustand in alle_zustaende():
            if zustand.action is None or zustand.action in (es.RESET_FILTER, es.SHOW_ALL_DAYS):
                continue  # Grund statt Aufforderung
            self.assertIn(zustand.action, es.ACTIONS)
            self.assertFalse(zustand.fallback.startswith(("Noch keine", "Keine")), zustand.fallback)
            self.assertEqual("…" in zustand.fallback, zustand.action in es.DIALOG_ACTIONS, zustand.fallback)

    def test_every_key_is_translated(self):
        sprachen = {s: json.loads((GLIDE / "resources/locales" / f"{s}.json").read_text(encoding="utf-8"))
                    for s in ("de", "en")}
        for zustand in alle_zustaende():
            for sprache, daten in sprachen.items():
                self.assertIn(zustand.key, daten, (sprache, zustand.key))
            self.assertEqual(sprachen["de"][zustand.key], zustand.fallback, zustand.key)
            self.assertEqual("…" in sprachen["de"][zustand.key], "…" in sprachen["en"][zustand.key], zustand.key)


if __name__ == "__main__":
    unittest.main()
