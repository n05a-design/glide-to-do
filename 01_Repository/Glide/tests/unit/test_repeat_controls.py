"""FP-02 vollständig: Bezug, Pause, Restanzahl, Chips und Kalender-Rundweg."""
import copy
from datetime import date
import json
from pathlib import Path
import sys
import unittest

REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'src/glide'))
import repeat_rules as r
import repeat_ics as exchange
import capture_parser as capture


class Seriensteuerung(unittest.TestCase):
    def test_completion_basis_and_purity(self):
        rule=r.apply_options({'art':'tage','abstand':3},basis='erledigt',remaining='3')
        before=copy.deepcopy(rule)
        day,following=r.advance_rule(rule,date(2026,10,30),date(2026,10,21))
        self.assertEqual(day,date(2026,10,24))
        self.assertEqual(following['rest'],2)
        self.assertEqual(following['start'],'2026-10-21')
        self.assertEqual(rule,before)
        self.assertEqual(r.advance_rule(rule,date(2026,10,20),date(2026,10,25))[0],date(2026,10,28))

    def test_pause_remaining_and_preview(self):
        rule=r.apply_options({'art':'taeglich'},remaining='3')
        self.assertEqual(r.preview(rule,'2026-10-21'),['2026-10-22','2026-10-23'])
        for remaining in (2,1):
            day,rule=r.advance_rule(rule,date.fromisoformat(rule.get('start') or '2026-10-21'))
            self.assertEqual(rule['rest'],remaining)
        self.assertIsNone(r.advance_rule(rule,day)[0])
        paused=r.apply_options({'art':'taeglich'},paused=True)
        self.assertEqual(r.preview(paused,'2026-10-21'),[])
        plan,reasons=r.skip_plan([dict(id='p',due='2026-10-21',repeat=paused)],date(2026,10,21))
        self.assertEqual(plan,{})
        self.assertEqual(reasons,{'p':'Serie pausiert'})

    def test_skipped_occurrences_consume_remaining(self):
        item=dict(id='a',due='2026-10-19',repeat=dict(art='taeglich',rest=5))
        plan,reasons=r.skip_plan([item],date(2026,10,21),missed=True,with_rules=True)
        self.assertEqual(plan['a']['due'],'2026-10-21')
        self.assertEqual(plan['a']['repeat']['rest'],3)
        self.assertEqual(item['repeat']['rest'],5)

    def test_default_storage_and_invalid_metadata(self):
        for kind in ('taeglich','woechentlich','monatlich','jaehrlich'):
            self.assertEqual(r.apply_options({'art':kind}),r.normalize({'art':kind}))
        for value in (0,10001,True,'3'):
            self.assertIsNone(r.normalize(dict(art='taeglich',rest=value)))
        for key,value in (('bezug','morgen'),('pausiert',1)):
            self.assertIsNone(r.normalize(dict(art='taeglich',**{key:value})))
        for rule in (dict(art='taeglich',rest=3),dict(art='monatlich',bezug='erledigt')):
            with self.assertRaises(ValueError):r.check_stored_series([{'repeat':rule}],25)

    def test_30_reference_calendar_roundtrips(self):
        fixtures=json.loads((REPO/'tests/fixtures/wiederholungsregeln_fp02.json').read_text(encoding='utf-8'))
        for spec in fixtures['regeln']:
            original=dict(art='serie',rrule=spec['rrule'],start=spec['start'])
            current=date.fromisoformat(spec['expected'][0])
            parts=exchange.export_parts(original,date.fromisoformat(spec['start']),current)
            self.assertIsNotNone(parts,spec)
            restored=exchange.from_parts(exchange.parse_parts(';'.join(parts)),current)
            self.assertIsNotNone(restored,spec)
            actual=[]
            for _ in range(23):
                current,restored=r.advance_rule(restored,current)
                actual.append(current.isoformat())
            self.assertEqual(actual,spec['expected'][1:],spec)

    def test_count_and_end_emit_one_effective_limit(self):
        rule=dict(art='taeglich',rest=10,ende='2026-10-23')
        parts=exchange.export_parts(rule,date(2026,10,21),date(2026,10,21))
        self.assertEqual(parts,['FREQ=DAILY','COUNT=3'])
        self.assertEqual(exchange.from_parts(exchange.parse_parts(';'.join(parts)),date(2026,10,21)),dict(art='taeglich',rest=3))

    def test_dynamic_and_unmatched_rules_are_not_static_calendar_series(self):
        for value in (dict(art='taeglich',pausiert=True),dict(art='tage',abstand=3,bezug='erledigt'),
                      dict(art='serie',rrule='FREQ=MONTHLY;BYDAY=2TU')):
            self.assertIsNone(exchange.export_parts(value,date(2026,1,1),date(2026,1,1)))

    def test_capture_controls_and_independent_chip_reversal(self):
        value=capture.parse_capture('Filter drei Tage nach Erledigung insgesamt 3 Termine',today=date(2026,10,21))
        self.assertEqual(value.titel,'Filter')
        self.assertEqual(value.felder['repeat']['bezug'],'erledigt')
        self.assertEqual(value.felder['repeat']['rest'],3)
        self.assertEqual(len(value.teile),1)
        restored=capture.parse_capture('Filter drei Tage nach Erledigung insgesamt 3 Termine',today=date(2026,10,21),ignore=[value.teile[0].schluessel])
        self.assertNotIn('repeat',restored.felder)


if __name__=='__main__':unittest.main()
