import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
import today_view as t

HEUTE='2026-10-02'

def punkt(text,**felder):
 return dict({'text':text,'importance':0,'due':None,'planned_date':None,'done':False},**felder)

def eintrag(item):
 return ((item.get('due') or '9999-12-31'),0,0,{'id':'l'},item)

def rang(item):
 # Vereinfachte Rangfolge wie task_urgency_rank: heute geplant, fällig bis heute, liegen geblieben, Rest; gesperrt zuletzt.
 if item.get('blocked'):stufe=4
 elif item.get('planned_date')==HEUTE:stufe=0
 elif item.get('due') and item['due']<=HEUTE:stufe=1
 elif item.get('planned_date') and item['planned_date']<HEUTE:stufe=2
 else:stufe=3
 return (stufe,-item.get('importance',0),item.get('due') or '9999-12-31')

def texte(eintraege):
 return [e[-1]['text'] for e in eintraege]

class HeuteTests(unittest.TestCase):
 def setUp(self):
  self.plan=punkt('Plan',planned_date=HEUTE)
  self.plan_wichtig=punkt('Plan wichtig',planned_date=HEUTE,importance=3)
  self.alt=punkt('Alt',due='2026-09-28')
  self.uralt=punkt('Uralt',due='2026-09-01')
  self.faellig=punkt('Heute fällig',due=HEUTE)
  self.liegen=punkt('Liegen',planned_date='2026-09-30')
  self.morgen=punkt('Morgen fällig',due='2026-10-03')
  self.erledigt=punkt('Erledigt alt',due='2026-09-01',done=True)
  self.geplant=[eintrag(self.plan_wichtig),eintrag(self.plan)]
  self.bestand=[eintrag(x) for x in (self.uralt,self.alt,self.faellig,self.liegen,self.morgen,self.erledigt,self.plan)]

 def test_reihenfolge_und_naechste(self):
  teile=t.abschnitte(self.geplant,self.bestand,[],HEUTE,HEUTE,rang,2)
  self.assertEqual(teile.naechste[-1]['text'],'Plan wichtig')
  self.assertEqual(texte(teile.verspaetet),['Uralt','Alt'])
  self.assertEqual(texte(teile.liegen),['Liegen'])
  self.assertEqual(texte(teile.plan),['Plan'])
  self.assertEqual(texte(teile.faellig),['Heute fällig'])
  # Künftiges und Erledigtes gehört nicht nach „Heute“.
  alle=[teile.naechste]+teile.verspaetet+teile.liegen+teile.plan+teile.faellig
  self.assertNotIn('Morgen fällig',texte(alle));self.assertNotIn('Erledigt alt',texte(alle))
  self.assertEqual(len({id(e[-1]) for e in alle}),len(alle))
  # Später Fälliges zählt nur für den Verweis auf „Demnächst“.
  self.assertEqual(texte(teile.demnaechst),['Morgen fällig'])

 def test_naechste_aus_verspaetet(self):
  teile=t.abschnitte([],self.bestand,[],HEUTE,HEUTE,rang,2)
  self.assertEqual(teile.naechste[-1]['text'],'Uralt')
  self.assertEqual(texte(teile.verspaetet),['Alt'])

 def test_grenze_und_gesperrt(self):
  gesperrt=punkt('Gesperrt',planned_date=HEUTE,blocked=True)
  teile=t.abschnitte([eintrag(gesperrt)],[],[],HEUTE,HEUTE,rang,2)
  self.assertIsNone(teile.naechste);self.assertEqual(texte(teile.plan),['Gesperrt'])
  # Ohne Rangfolge gibt es keine nächste Aufgabe.
  self.assertIsNone(t.abschnitte(self.geplant,[],[],HEUTE,HEUTE).naechste)

 def test_eingang_ohne_dublette(self):
  eingang_faellig=punkt('Eingang fällig',due=HEUTE)
  eingang_frei=punkt('Eingang frei')
  eingang=[({'id':'in'},eingang_faellig),({'id':'in'},eingang_frei)]
  teile=t.abschnitte([],[eintrag(eingang_faellig)],eingang,HEUTE,HEUTE,rang,2)
  self.assertEqual(teile.naechste[-1]['text'],'Eingang fällig')
  self.assertEqual([e[-1]['text'] for e in teile.eingang],['Eingang frei'])

 def test_anderer_tag(self):
  teile=t.abschnitte([eintrag(self.plan)],self.bestand,[],'2026-10-03',HEUTE,rang,2)
  self.assertIsNone(teile.naechste)
  self.assertEqual(texte(teile.faellig),['Morgen fällig'])
  self.assertEqual(teile.verspaetet,[]);self.assertEqual(teile.liegen,[])
  self.assertEqual(texte(teile.plan),['Plan'])
  self.assertEqual(teile.demnaechst,[])

 def test_leer_und_einordnung(self):
  self.assertTrue(t.leer(t.abschnitte([],[eintrag(self.morgen)],[],HEUTE,HEUTE,rang,2)))
  self.assertTrue(t.leer(t.abschnitte([],[],[],HEUTE,HEUTE,rang,2)))
  self.assertFalse(t.leer(t.abschnitte([],[],[({},punkt('x'))],HEUTE,HEUTE,rang,2)))
  self.assertEqual(t.einordnung(punkt('x',due='kaputt'),HEUTE,HEUTE),None)
  self.assertEqual(t.einordnung(punkt('x',due='2026-10-01',planned_date='2026-09-01'),HEUTE,HEUTE),'verspaetet')
  self.assertEqual(t.einordnung(punkt('x',due=HEUTE,planned_date='2026-09-01'),HEUTE,HEUTE),'faellig')

if __name__=='__main__':unittest.main()
