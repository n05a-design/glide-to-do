import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
import home_tiles as h

# D12 mit B04 (15.10.2026): Galeriebilder gehören zum Standard.
D12=['mascot','today','week','recent','boardpreview','drawings','gallery','pinned']
ALT12=['clock','welcome','mascot','today','focus','week','recent','templates','boardpreview','drawings','pinned','stats']

def sichtbar(order,hidden):
 return [k for k in h.ordered(order) if k not in hidden]

class HomeTileTests(unittest.TestCase):
 def test_standard_is_d12(self):
  self.assertEqual(sorted(h.STANDARD),sorted(D12));self.assertEqual(len(h.KEYS),20)
  self.assertEqual(len({d[0] for d in h.DEFINITIONS}),20)
 def test_new_and_untouched_start_page_get_standard(self):
  # Altbestand vor B04 kannte die Galeriekachel nicht und kann sie nicht ausgeblendet haben.
  for order,hidden in [(None,None),([],[]),([], [k for k in h.KEYS if k not in ALT12 and k!='gallery'])]:
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
  self.assertEqual(h.ordered(['week','clock','x','week'])[:2],['week','clock']);self.assertEqual(len(h.ordered(['week'])),20)
 def test_today_sections_avoid_duplicates(self):
  self.assertEqual(h.today_sections(D12),{'goal':True,'next':True})
  self.assertEqual(h.today_sections(ALT12),{'goal':False,'next':False})
  self.assertEqual(h.today_sections(['today','focus']),{'goal':True,'next':False})
class B03B04Tests(unittest.TestCase):
 def test_own_selection_is_not_overwritten_by_the_new_gallery_tile(self):
  alt={'home_tile_order':[k for k in h.KEYS if k!='gallery'],'home_tiles_hidden':['clock']}
  neu=h.hide_new_tiles_once(alt)
  self.assertIn('gallery',neu['home_tiles_hidden']);self.assertIs(neu['home_tiles_gallery'],True)
  self.assertEqual(alt['home_tiles_hidden'],['clock'],'Original bleibt unverändert')
  o,hid=h.normalize(neu['home_tile_order'],neu['home_tiles_hidden'])
  self.assertNotIn('gallery',sichtbar(o,hid));self.assertIn('mascot',sichtbar(o,hid))
  # Nur einmal: Danach entscheidet die Person, auch ohne erweiterte Reihenfolge.
  wieder=h.hide_new_tiles_once(dict(neu,home_tiles_hidden=[]))
  self.assertEqual(wieder['home_tiles_hidden'],[])
 def test_untouched_or_fresh_settings_only_get_the_marker(self):
  for alt in ({},{'home_tile_order':[]},{'home_tile_order':'kaputt'}):
   neu=h.hide_new_tiles_once(alt)
   self.assertIs(neu['home_tiles_gallery'],True);self.assertNotIn('gallery',neu.get('home_tiles_hidden',[]))
 def test_untouched_start_page_shows_the_gallery_tile(self):
  o,hid=h.normalize([],[]);self.assertIn('gallery',sichtbar(o,hid))
 def test_gismo_name_and_retired_settings(self):
  self.assertEqual(h.MASCOT_NAME,'Gismo')
  alt={'mascot_name':'Mika','mascot_playful':False,'profile_name':'X'}
  neu=h.retire_mascot_settings(alt)
  self.assertEqual(neu,{'profile_name':'X'});self.assertIn('mascot_name',alt)
  self.assertEqual(h.retire_mascot_settings(None),{})
 def test_gismo_visibility_follows_only_his_tile(self):
  self.assertTrue(h.mascot_visible([]));self.assertTrue(h.mascot_visible(['clock']))
  self.assertFalse(h.mascot_visible(['mascot']));self.assertTrue(h.mascot_visible('kaputt'))
if __name__=='__main__':unittest.main()
