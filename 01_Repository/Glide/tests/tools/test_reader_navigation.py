import unittest

from reader_navigation import select_task


class TreeTaskNavigation(unittest.TestCase):
    def test_flat_first_task_needs_no_extra_arrow(self):
        keys=[]
        self.assertIn('Angebot',select_task(keys.append,lambda:'Aufgaben Angebot Offen', 'Angebot'))
        self.assertEqual(keys,['home'])

    def test_section_header_is_expanded_then_real_task_must_be_spoken(self):
        keys=[];speech=iter(['Keine Aufgabe ausgewählt', 'Abschnitt Heute', 'Angebot Offen'])
        self.assertEqual(select_task(keys.append,lambda:next(speech),'Angebot'),'Angebot Offen')
        self.assertEqual(keys,['home','right','down','down'])

    def test_missing_task_fails_without_activating_an_unrelated_row(self):
        keys=[]
        with self.assertRaises(AssertionError):
            select_task(keys.append,lambda:'Keine Aufgabe ausgewählt','Angebot',limit=2)
        self.assertNotIn('enter',keys)
        self.assertEqual(keys,['home','right','down','down'])


if __name__=='__main__':
    unittest.main()
