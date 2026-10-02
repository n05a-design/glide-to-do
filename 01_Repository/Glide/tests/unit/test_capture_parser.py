import sys,unittest
from datetime import date
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
import capture_parser as c

HEUTE=date(2026,10,2)  # Freitag
L=[{'id':'l1','name':'Büro'},{'id':'l2','name':'Privat'}]

def p(text,ignore=()):
 return c.parse_capture(text,L,HEUTE,ignore)

class CaptureTests(unittest.TestCase):
 def test_plan_example_d01_d10(self):
  # Abnahme aus dem Entwicklungsplan: drei einzeln rücknehmbare Chips.
  e=p('Angebot schicken morgen bis Freitag /wichtig')
  self.assertEqual(e.titel,'Angebot schicken')
  self.assertEqual(e.felder,{'planned_date':'2026-10-03','due':'2026-10-02','importance':3})
  self.assertEqual([t.text for t in e.teile],['Bearbeitungstag Sa 03.10.2026','Fällig Fr 02.10.2026','Wichtigkeit hoch'])
  self.assertEqual(len({t.schluessel for t in e.teile}),3)
 def test_b01_time_and_estimate(self):
  e=p('Exposé morgen 14:30, 45 Minuten')
  self.assertEqual((e.titel,e.felder),('Exposé',{'planned_date':'2026-10-03','planned_time':'14:30','estimated_minutes':45}))
 def test_slash_date_sets_planned_day_d10(self):
  e=p('Milch /morgen /wichtig')
  self.assertEqual(e.felder,{'planned_date':'2026-10-03','importance':3});self.assertNotIn('due',e.felder)
  self.assertEqual(p('Steuer /bis Montag 9:00').felder,{'due':'2026-10-05','due_time':'09:00'})
  self.assertEqual(p('Zahlung /24.12.2026').felder,{'planned_date':'2026-12-24'})
  self.assertEqual(p('Fokus /meintag').felder,{'planned_date':'2026-10-02'})
 def test_due_prefixes(self):
  self.assertEqual(p('Abgabe fällig am 01.11.2026').felder,{'due':'2026-11-01'})
  self.assertEqual(p('Bericht bis 24.12. um 10 Uhr').felder,{'due':'2026-12-24','due_time':'10:00'})
  self.assertEqual(p('Antwort bis 14 Uhr').felder,{'due':'2026-10-02','due_time':'14:00'})
  self.assertEqual(p('Bis bald').felder,{})
 def test_dates(self):
  self.assertEqual(p('A heute').felder['planned_date'],'2026-10-02')
  self.assertEqual(p('A übermorgen').felder['planned_date'],'2026-10-04')
  self.assertEqual(p('A Freitag').felder['planned_date'],'2026-10-02')
  self.assertEqual(p('A nächsten Freitag').felder['planned_date'],'2026-10-09')
  self.assertEqual(p('A in 3 Tagen').felder['planned_date'],'2026-10-05')
  self.assertEqual(p('A in einer Woche').felder['planned_date'],'2026-10-09')
  self.assertEqual(p('A am 01.01.').felder['planned_date'],'2027-01-01')
  self.assertEqual(p('A 31.02.2026').felder,{});self.assertEqual(p('A 31.02.2026').titel,'A 31.02.2026')
 def test_time_alone_means_today(self):
  e=p('Anruf um 15 Uhr')
  self.assertEqual(e.felder,{'planned_time':'15:00','planned_date':'2026-10-02'});self.assertEqual(e.teile[0].text,'Uhrzeit 15:00 (heute)')
  self.assertEqual(p('Anruf um 25 Uhr').felder,{})
 def test_estimates(self):
  self.assertEqual(p('Tee 2h').felder,{'estimated_minutes':120})
  self.assertEqual(p('Lesen 1 Std. 30 Min.').felder,{'estimated_minutes':90})
  self.assertEqual(p('Lesen 1,5 Stunden').felder,{'estimated_minutes':90})
  self.assertEqual(p('Lesen 0 min').felder,{})
 def test_labels_and_importance(self):
  e=p('Bericht #büro #Privat !hoch #unbekannt')
  self.assertEqual(e.felder,{'labels':['l1','l2'],'importance':3});self.assertEqual(e.titel,'Bericht #unbekannt')
  self.assertEqual(p('Notiz /Büro').felder,{'labels':['l1']})
 def test_text_stays_literal(self):
  for text in ('und/oder prüfen','Ja !','Termin "morgen" absagen','Zimmer 14','Version 2.0 testen'):
   self.assertEqual((p(text).titel,p(text).felder),(text,{}),text)
  self.assertEqual(p('Buch „Momo“ heute').titel,'Buch „Momo“')
 def test_ignore_keeps_text_and_blocks_partial_reparse(self):
  e=p('Angebot morgen bis Freitag',ignore={'bis freitag'})
  self.assertEqual(e.titel,'Angebot bis Freitag');self.assertEqual(e.felder,{'planned_date':'2026-10-03'})
  e=p('Exposé morgen 14:30',ignore={'morgen 14:30'})
  self.assertEqual((e.titel,e.felder),('Exposé morgen 14:30',{}))
 def test_only_first_of_each_kind(self):
  e=p('A morgen Montag')
  self.assertEqual(e.felder,{'planned_date':'2026-10-03'});self.assertEqual(e.titel,'A Montag')
 def test_punctuation_cleanup_only_where_removed(self):
  self.assertEqual(p('Angebot, morgen, schicken').titel,'Angebot schicken')
  self.assertEqual(p('Exposé morgen.').titel,'Exposé')
 def test_capture_due_field_unchanged(self):
  self.assertEqual(c.parse_capture_due('morgen um 14:30',HEUTE),('2026-10-03','14:30'))
  with self.assertRaises(ValueError):c.parse_capture_due('irgendwann',HEUTE)
 def test_repeat_sets_first_due(self):
  # Entscheidung 02.10.2026: Eine Wiederholung setzt die Fälligkeit, damit sie im Kalender steht.
  self.assertEqual(p('Sport jeden Montag').felder,{'repeat':{'art':'woechentlich','start':'2026-10-05'},'due':'2026-10-05'})
  self.assertEqual(p('Zeitung täglich').felder['repeat'],{'art':'taeglich','start':'2026-10-02'})
  self.assertEqual(p('Lauf jeden Tag').felder['due'],'2026-10-02')
  self.assertEqual(p('Standup werktags um 9:30').felder,{'repeat':{'art':'wochentage','tage':[0,1,2,3,4],'start':'2026-10-02'},'due':'2026-10-02','due_time':'09:30'})
  self.assertEqual(p('Meeting montags und donnerstags').felder['repeat']['tage'],[0,3])
  self.assertEqual(p('Kurs montags, mittwochs und freitags').felder['repeat']['tage'],[0,2,4])
  self.assertEqual(p('Kurs jeden Montag und Donnerstag 18 Uhr').felder,{'repeat':{'art':'wochentage','tage':[0,3],'start':'2026-10-05'},'due':'2026-10-05','due_time':'18:00'})
  self.assertEqual(p('Gießen alle 3 Tage').felder['repeat'],{'art':'tage','abstand':3,'start':'2026-10-02'})
  self.assertEqual(p('Wäsche alle zwei Wochen').felder['repeat'],{'art':'tage','abstand':14,'start':'2026-10-02'})
  self.assertEqual(p('Miete monatlich').felder['repeat']['art'],'monatlich')
  self.assertEqual(p('Feier jedes Jahr').felder['repeat']['art'],'jaehrlich')
  self.assertEqual(p('Sport jeden Montag').titel,'Sport')
  self.assertEqual(p('Sport jeden Montag').teile[0].text,'Wiederholung jeden Montag · fällig ab Mo 05.10.2026')
 def test_repeat_explicit_due_wins(self):
  e=p('Steuer jährlich bis 31.05.2027')
  self.assertEqual(e.felder,{'repeat':{'art':'jaehrlich','start':'2027-05-31'},'due':'2027-05-31'})
  self.assertEqual([t.text for t in e.teile],['Wiederholung jährlich ab der Fälligkeit','Fällig Mo 31.05.2027'])
 def test_repeat_not_in_ordinary_text(self):
  for text in ('alle Unterlagen sortieren','jeden Kunden anrufen','Montagsrunde vorbereiten','alle 3 Monate prüfen','alle 400 Tage'):
   e=p(text);self.assertNotIn('repeat',e.felder,text)
  self.assertEqual(p('Sport jeden Montag',ignore={'jeden montag'}).felder,{})
 def test_suggestions(self):
  self.assertEqual(c.slash_suggestions('bi',L),['bis']);self.assertIn('Büro',c.slash_suggestions('bü',L))
if __name__=='__main__':unittest.main()
