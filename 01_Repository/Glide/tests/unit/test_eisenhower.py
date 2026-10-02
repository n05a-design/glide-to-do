import sys,unittest
from datetime import date
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
import eisenhower as e

HEUTE=date(2026,10,2)

def punkt(**felder):
 return dict({'importance':0,'due':None,'planned_date':None},**felder)

class EisenhowerTests(unittest.TestCase):
 def test_quadranten(self):
  self.assertEqual(e.quadrant(punkt(importance=3,due='2026-10-02'),HEUTE),'q1')
  self.assertEqual(e.quadrant(punkt(importance=2),HEUTE),'q2')
  self.assertEqual(e.quadrant(punkt(importance=1,planned_date='2026-10-04'),HEUTE),'q3')
  self.assertEqual(e.quadrant(punkt(importance=1,planned_date='2026-10-05'),HEUTE),'q4')
  self.assertEqual(e.quadrant(punkt(due='2026-09-01'),HEUTE),'q3')  # überfällig ist dringend
  self.assertEqual(e.quadrant(punkt(importance=True),HEUTE),'q4')
  self.assertEqual(e.quadrant(punkt(due='kaputt'),HEUTE),'q4')
 def test_ziehen_aendert_nur_noetiges(self):
  self.assertEqual(e.aenderung(punkt(),'q2',HEUTE),({'importance':2},None))
  self.assertEqual(e.aenderung(punkt(importance=3),'q4',HEUTE),({'importance':1},None))
  self.assertEqual(e.aenderung(punkt(importance=3),'q1',HEUTE),({'planned_date':'2026-10-02'},None))
  self.assertEqual(e.aenderung(punkt(importance=2,planned_date='2026-10-02'),'q2',HEUTE),({'planned_date':'2026-10-05'},None))
  self.assertEqual(e.aenderung(punkt(importance=2),'q2',HEUTE),({},None))
 def test_faelligkeit_bleibt(self):
  felder,grund=e.aenderung(punkt(importance=3,due='2026-10-03'),'q2',HEUTE)
  self.assertIsNone(felder);self.assertIn('Fälligkeit',grund)
  # Eine Fälligkeit außerhalb des Fensters stört nicht, sie bleibt unverändert.
  self.assertEqual(e.aenderung(punkt(due='2026-12-24',planned_date='2026-10-02'),'q4',HEUTE),({'planned_date':'2026-10-05'},None))
 def test_unbekannt(self):
  self.assertEqual(e.aenderung(punkt(),'q9',HEUTE)[0],None)
  self.assertEqual(e.KEYS,('q1','q2','q3','q4'))
if __name__=='__main__':unittest.main()
