import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
import home_tiles as h

D12=['mascot','today','week','recent','boardpreview','drawings','pinned']
ALT12=['clock','welcome','mascot','today','focus','week','recent','templates','boardpreview','drawings','pinned','stats']

def sichtbar(order,hidden):
 return [k for k in h.ordered(order) if k not in hidden]

class HomeTileTests(unittest.TestCase):
 def test_standard_is_d12(self):
  self.assertEqual(sorted(h.STANDARD),sorted(D12));self.assertEqual(len(h.KEYS),19)
  self.assertEqual(len({d[0] for d in h.DEFINITIONS}),19)
 def test_new_and_untouched_start_page_get_standard(self):
  for order,hidden in [(None,None),([],[]),([], [k for k in h.KEYS if k not in ALT12])]:
   o,hid=h.normalize(order,hidden);self.assertEqual(o,[]);self.assertEqual(sichtbar(o,hid),D12)
 def test_own_selection_survives(self):
  order=list(h.KEYS);hidden=[k for k in h.KEYS if k not in ALT12]
  o,hid=h.normalize(order,hidden);self.assertEqual(sichtbar(o,hid),ALT12)
 def test_explicit_hides_and_stats_switch(self):
  o,hid=h.normalize([],['week','unbekannt','week']);self.assertNotIn('week',sichtbar(o,hid));self.assertEqual(hid.count('week'),1)
  o,hid=h.normalize(list(h.KEYS),[],show_stats=False);self.assertIn('stats',hid)
  o,hid=h.normalize('kaputt',{'x':1});self.assertEqual(sichtbar(o,hid),D12)
 def test_showing_a_tile_is_kept_after_restart(self):
  order,hidden=h.normalize([],[])
  order,hidden=h.own_selection(order,hidden,'clock',hide=False)
  self.assertTrue(order);o,hid=h.normalize(order,hidden);self.assertIn('clock',sichtbar(o,hid))
  order,hidden=h.own_selection(o,hid,'week',hide=True);o,hid=h.normalize(order,hidden)
  self.assertNotIn('week',sichtbar(o,hid));self.assertIn('clock',sichtbar(o,hid))
 def test_reset_restores_standard(self):
  o,hid=h.normalize(*h.standard_selection());self.assertEqual(sichtbar(o,hid),D12)
 def test_ordered_keeps_saved_order_and_appends_new(self):
  self.assertEqual(h.ordered(['week','clock','x','week'])[:2],['week','clock']);self.assertEqual(len(h.ordered(['week'])),19)
 def test_today_sections_avoid_duplicates(self):
  self.assertEqual(h.today_sections(D12),{'goal':True,'next':True})
  self.assertEqual(h.today_sections(ALT12),{'goal':False,'next':False})
  self.assertEqual(h.today_sections(['today','focus']),{'goal':True,'next':False})
if __name__=='__main__':unittest.main()
