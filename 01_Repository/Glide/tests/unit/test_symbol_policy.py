# SPDX-License-Identifier: MPL-2.0
import unittest
from symbol_policy import resolve, TEXT_FALLBACKS, split_heading

class SymbolPolicyTests(unittest.TestCase):
    def test_complete_table_and_semantic_known_corrections(self):
        icons={key: "■" for key in TEXT_FALLBACKS}
        result,changes=resolve(icons,lambda text: True)
        self.assertEqual(set(result),set(icons))
        # B10 (15.10.2026): Die Suche zeigt die Lupe, sobald eine Schrift sie trägt.
        self.assertEqual([result[k] for k in ("search","print","notifications","trash")],["⌕","Dr","!","♲"])
        self.assertEqual(result["home"],"■")
        self.assertEqual(set(changes),{"search","print","notifications","trash"})
        self.assertTrue(all(v=="■" for v in icons.values()))

    def test_ascii_only_font_remains_readable(self):
        result,changes=resolve({key:"■" for key in TEXT_FALLBACKS},str.isascii)
        self.assertEqual(result,TEXT_FALLBACKS)
        self.assertEqual(result["trash"],"Pk")
        self.assertEqual(len(changes),len(TEXT_FALLBACKS))

    def test_different_actions_keep_distinct_ascii_meanings(self):
        for a,b in (("details","description"),("undo","back"),("swap","symmetry_x"),
                    ("notifications","priority_low"),("check","remove")):
            self.assertNotEqual(TEXT_FALLBACKS[a],TEXT_FALLBACKS[b])

    def test_complete_ascii_fallback_preserves_action_roles(self):
        # D29: Nur Verschieben/Sortieren derselben Richtung sind gemeinsame
        # Rollen. Gruppenöffnung und Auswahlpfeile sind andere Aktionen.
        from collections import defaultdict
        resolved, _ = resolve({key: "■" for key in TEXT_FALLBACKS}, str.isascii)
        roles = defaultdict(set)
        for key, text in resolved.items():
            roles[text].add(key)
        duplicates = {frozenset(keys) for keys in roles.values() if len(keys) > 1}
        self.assertEqual(duplicates, {
            frozenset(("move_up", "sort_ascending")),
            frozenset(("move_down", "sort_descending")),
        })

    def test_caption_keeps_pixel_font_without_icon_font_fallback(self):
        icons = {"calendar": "▦", "search": "Su"}
        self.assertEqual(split_heading("▦  Kalender", icons), ("▦", "Kalender"))
        self.assertEqual(split_heading("Su  Suchen", icons), ("Su", "Suchen"))
        self.assertEqual(split_heading("Eigener  Titel", icons), ("", "Eigener  Titel"))

    def test_magnifier_comes_from_a_system_symbol_font_when_ui_font_lacks_it(self):
        from symbol_policy import resolve_with_fonts, SYMBOL_FONT_FALLBACKS, SYMBOL_FONT_FAMILIES
        icons={key:"■" for key in TEXT_FALLBACKS}
        ohne_lupe=lambda text: "⌕" not in text
        result,changes,fonts=resolve_with_fonts(icons,ohne_lupe,lambda family,text: family=="Segoe UI Symbol")
        self.assertEqual(result["search"],"⌕")
        self.assertEqual(fonts,{"search":"Segoe UI Symbol"})
        # Ohne passende Systemschrift bleibt der lesbare Text „Su“.
        result,_,fonts=resolve_with_fonts(icons,ohne_lupe,lambda family,text: False)
        self.assertEqual((result["search"],fonts),("Su",{}))
        result,_,fonts=resolve_with_fonts(icons,ohne_lupe)
        self.assertEqual((result["search"],fonts),("Su",{}))
        # Nur die Lupe darf eine Systemschrift nutzen; kein Emoji-Font in der Liste.
        self.assertEqual(set(SYMBOL_FONT_FALLBACKS),{"search"})
        self.assertFalse(any("emoji" in name.lower() for name in SYMBOL_FONT_FAMILIES))

    def test_bundled_companion_supplies_symbols_missing_in_ui_font(self):
        # D59 (03.11.2026): Roboto Mono enthält keine geometrischen Zeichen.
        # Sie kommen aus der mitgelieferten DejaVu Sans, nicht aus dem Text.
        from symbol_policy import resolve_with_fonts, BUNDLED_SYMBOL_FAMILY
        icons={key:"■" for key in TEXT_FALLBACKS}
        nur_ascii=lambda text: text.isascii()
        begleiter=lambda family,text: family==BUNDLED_SYMBOL_FAMILY and "⌕" not in text
        result,changes,fonts=resolve_with_fonts(icons,nur_ascii,begleiter)
        self.assertEqual(result["home"],"■")
        self.assertEqual(fonts["home"],BUNDLED_SYMBOL_FAMILY)
        self.assertEqual(result["trash"],"♲")
        # Die Lupe fehlt auch im Begleiter: lesbarer Text ohne Systemschrift.
        self.assertEqual((result["search"],fonts.get("search")),("Su",None))
        # Enthält die UI-Schrift das Zeichen selbst, bleibt sie maßgeblich.
        result,_,fonts=resolve_with_fonts(icons,lambda text: True,begleiter)
        self.assertEqual(fonts,{})

    def test_first_covered_candidate_and_table_contract(self):
        icons={key:"■" for key in TEXT_FALLBACKS}
        result,_=resolve(icons,lambda value: value!="♲")
        self.assertEqual(result["trash"],"Pk")
        with self.assertRaises(ValueError):resolve({},lambda text:True)
        with self.assertRaises(ValueError):resolve(icons,lambda text:False)

if __name__=="__main__":unittest.main()
