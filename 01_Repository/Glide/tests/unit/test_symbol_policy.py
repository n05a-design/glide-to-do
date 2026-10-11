import unittest
from symbol_policy import resolve, TEXT_FALLBACKS, split_heading

class SymbolPolicyTests(unittest.TestCase):
    def test_complete_table_and_semantic_known_corrections(self):
        icons={key: "■" for key in TEXT_FALLBACKS}
        result,changes=resolve(icons,lambda text: True)
        self.assertEqual(set(result),set(icons))
        self.assertEqual([result[k] for k in ("search","print","notifications","trash")],["Su","Dr","!","♲"])
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

    def test_caption_keeps_pixel_font_without_icon_font_fallback(self):
        icons = {"calendar": "▦", "search": "Su"}
        self.assertEqual(split_heading("▦  Kalender", icons), ("▦", "Kalender"))
        self.assertEqual(split_heading("Su  Suchen", icons), ("Su", "Suchen"))
        self.assertEqual(split_heading("Eigener  Titel", icons), ("", "Eigener  Titel"))

    def test_first_covered_candidate_and_table_contract(self):
        icons={key:"■" for key in TEXT_FALLBACKS}
        result,_=resolve(icons,lambda value: value!="♲")
        self.assertEqual(result["trash"],"Pk")
        with self.assertRaises(ValueError):resolve({},lambda text:True)
        with self.assertRaises(ValueError):resolve(icons,lambda text:False)

if __name__=="__main__":unittest.main()
