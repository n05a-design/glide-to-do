"""Gesamte Übernahmeplanung mit den echten Glide-Datenkonstruktoren, ohne Tk."""
import copy
import hashlib
import io
import itertools
from pathlib import Path
import unittest
import zipfile

from test_source_schema_bridge import m
import notion_import as ni


class NotionImportTests(unittest.TestCase):
    def setUp(self):
        self.a=m.ListApp.__new__(m.ListApp);self.a.labels=[];self.a.settings={}
        self.current=dict(lists=[self.a.new_list_object('Unberührt',[],list_id='fremd')],folders=[],trash=[],labels=[])
        self.png=m.glide_drawing.DrawingModel.blank(16).to_png()
        self.first='Wissen '+'a'*32+'.md'
        self.second='Wissen '+'a'*32+'/Unterseite '+'b'*32+'.md'
        self.files={self.first:'# Wissen\n\n- [ ] Prüfen\n\n![Foto](foto.png)\n\n[Weiter](Wissen%20'+'a'*32+'/Unterseite%20'+'b'*32+'.md)',
                    self.second:'# Unterseite\n\nText', 'foto.png':self.png, 'Daten.csv':'Name,Wert\nA,1'}

    def export(self,files=None):
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w')as archive:
            for name,value in (files or self.files).items():
                archive.writestr(name,value.encode()if isinstance(value,str)else value)
        raw=stream.getvalue()
        return m.glide_notion_archive.inspect_export(io.BytesIO(raw)),raw

    def compare(self,export,current=None,hashes=None):
        current=current or self.current
        records=m.glide_source_metadata.records(current['lists'])
        if hashes is None:
            hashes={asset['id']:hashlib.sha256(self.png).hexdigest()
                    for page in current['lists']if page.get('notion_source')
                    for asset in page.get('attachments',[])}
        current_hashes={page['id']:m.glide_notion_reimport.content_fingerprint(page,hashes or {})
                        for page in current['lists']if page.get('notion_source')}
        return m.glide_notion_reimport.compare(export,records,current_hashes)

    def select(self,export,raw,current=None,keys=None,overwrite=()):
        current=current or self.current
        return ni.select(current,export,self.compare(export,current),keys or tuple(page.key for page in export.pages),
                         overwrite,raw,new_id=lambda:'container'+str(next(self.numbers)))

    def staged(self,selection):
        return {value['id']:dict(value,id='datei'+str(index),storage=f'attachments/datei{index}.dat',added_at='2026-10-12T12:00:00')
                for index,value in enumerate(selection.assets)}

    def apply(self,selection,export,current=None,stored=None,**kw):
        return ni.content(selection,current or self.current,export,stored or self.staged(selection),
                          page_factory=self.a.new_list_object,item_factory=self.a.new_item,
                          folder_factory=self.a.new_folder_object,now='2026-10-12T12:00:00',
                          new_id=lambda:'aufgabe'+str(next(self.numbers)),**kw)

    def test_complete_selection_images_tasks_links_report_and_subfolders(self):
        self.numbers=itertools.count();export,raw=self.export();before=copy.deepcopy(self.current)
        selection=self.select(export,raw);stored=self.staged(selection)
        result=self.apply(selection,export,stored=stored)
        self.assertEqual(self.current,before)
        self.assertEqual(result.lists[0],before['lists'][0]);self.assertEqual(len(result.imported_ids),2)
        page=next(p for p in result.lists if p.get('notion_source',{}).get('key')==export.pages[0].key)
        self.assertEqual(len(page['items']),1);self.assertFalse(page['items'][0]['done'])
        self.assertIn('item:'+page['items'][0]['id'],[v['tag']for v in page['rich_note']['spans']])
        self.assertEqual(len(page['rich_note']['images']),1)
        self.assertIn('glide://list/',str(page['rich_note']['links']))
        self.assertEqual(len(result.folders),1)
        report=next(p for p in result.lists if p['id']==result.report_id)
        self.assertEqual(report['attachments'],[stored[selection.report_asset_id]])
        self.assertIn('CSV-Datenbank',report['rich_note']['text'])
        self.assertEqual(len(raw),report['attachments'][0]['size'])

    def test_same_export_is_unchanged_after_normalization_and_does_not_duplicate(self):
        self.numbers=itertools.count();export,raw=self.export();selection=self.select(export,raw)
        result=self.apply(selection,export)
        current=dict(self.current,lists=list(result.lists),folders=list(result.folders),trash=list(result.trash))
        hashes={p['attachments'][0]['id']:hashlib.sha256(self.png).hexdigest()
                for p in current['lists']if p.get('notion_source')and p['attachments']}
        normalized=[dict(p,rich_note=m.RichNoteEditor.normalize(p['rich_note']))for p in current['lists']]
        comparison=self.compare(export,dict(current,lists=normalized),hashes)
        self.assertEqual({row.status for row in comparison.rows},{'unchanged'})
        with self.assertRaisesRegex(ValueError,'Unveränderte'):
            ni.select(current,export,comparison,[export.pages[0].key],(),raw)

    def test_unselected_page_link_is_reported_and_stays_unresolved(self):
        self.numbers=itertools.count();export,raw=self.export()
        selection=self.select(export,raw,keys=[export.pages[0].key])
        self.assertTrue(any(loss.code=='unselected-page'for loss in selection.losses))
        result=self.apply(selection,export);page=result.lists[1]
        self.assertNotIn('glide://list/',str(page['rich_note']['links']))
        self.assertEqual(len(result.imported_ids),1)

    def test_changed_source_keeps_identity_and_all_old_tasks_in_trash(self):
        self.numbers=itertools.count();export,raw=self.export()
        first=self.apply(self.select(export,raw),export)
        current=dict(self.current,lists=list(first.lists),folders=list(first.folders),trash=list(first.trash))
        page=next(p for p in current['lists']if p.get('notion_source')and p['items'])
        original_id=page['id'];old_task=copy.deepcopy(page['items'][0]);old_other=copy.deepcopy(current['lists'][0])
        page['note']='Eigene Notiz';page['items'].append(self.a.new_item('Eigene Aufgabe'))
        files=dict(self.files);files[self.first]='# Wissen geändert\n\n- [x] Neue Aufgabe'
        updated,newraw=self.export(files);comparison=self.compare(updated,current)
        row=next(r for r in comparison.rows if r.page.path==self.first)
        self.assertEqual(row.status,'conflict')
        with self.assertRaisesRegex(ValueError,'ausdrückliche'):
            ni.select(current,updated,comparison,[row.page.key],(),newraw)
        selection=ni.select(current,updated,comparison,[row.page.key],[row.page.key],newraw)
        result=self.apply(selection,updated,current)
        changed=next(p for p in result.lists if p['id']==original_id)
        self.assertEqual(changed['title'],'Wissen geändert');self.assertEqual(changed['note'],'Eigene Notiz')
        self.assertTrue(changed['items'][0]['done']);self.assertEqual(result.lists[0],old_other)
        self.assertEqual(len(result.trash),2);self.assertIn(old_task,[d['item']for d in result.trash])

    def test_stale_selection_aborts_without_mutation(self):
        self.numbers=itertools.count();export,raw=self.export();selection=self.select(export,raw)
        self.current['lists'][0]['title']='Geändert'
        before=copy.deepcopy(self.current)
        with self.assertRaisesRegex(ValueError,'Bestand hat sich geändert'):
            self.apply(selection,export)
        self.assertEqual(self.current,before)

    def test_incomplete_files_and_full_trash_are_rejected(self):
        self.numbers=itertools.count();export,raw=self.export();selection=self.select(export,raw)
        stored=self.staged(selection);stored.pop(selection.report_asset_id)
        with self.assertRaisesRegex(ValueError,'Importdateien'):
            self.apply(selection,export,stored=stored)
        first=self.apply(selection,export)
        current=dict(self.current,lists=list(first.lists),folders=list(first.folders))
        files=dict(self.files);files[self.first]='# Neu'
        updated,raw=self.export(files);cmp=self.compare(updated,current)
        key=updated.pages[0].key
        plan=ni.select(current,updated,cmp,[key],[key],raw)
        with self.assertRaisesRegex(ValueError,'Papierkorb kürzen'):
            self.apply(plan,updated,current,max_trash=0)

    def test_retained_glide_cover_needs_real_bytes_and_stays_in_source_baseline(self):
        self.numbers=itertools.count();export,raw=self.export()
        result=self.apply(self.select(export,raw),export)
        current=dict(self.current,lists=list(result.lists),folders=list(result.folders))
        page=next(p for p in current['lists']if p.get('notion_source')and p['attachments'])
        cover=page['attachments'][0];page['cover']=dict(kind='image',attachment=cover['id'])
        files=dict(self.files);files[self.first]='# Titelbild bleibt\n\nNeuer Text'
        updated,raw=self.export(files);cmp=self.compare(updated,current);key=page['notion_source']['key']
        selection=ni.select(current,updated,cmp,[key],[key],raw)
        with self.assertRaisesRegex(ValueError,'Titelbild braucht'):
            self.apply(selection,updated,current)
        copied=self.apply(selection,updated,current,current_asset_hashes={cover['id']:hashlib.sha256(self.png).hexdigest()})
        restored=next(p for p in copied.lists if p['id']==page['id'])
        self.assertEqual(restored['cover'],page['cover']);self.assertEqual(restored['attachments'],[cover])
        self.assertEqual(restored['notion_source']['local_hash'],m.glide_notion_reimport.content_fingerprint(
            restored,{cover['id']:hashlib.sha256(self.png).hexdigest()}))

    def test_wrong_export_stale_source_binding_and_exhausted_ids_are_rejected(self):
        self.numbers=itertools.count();export,raw=self.export();cmp=self.compare(export)
        other,_=self.export({'Andere '+'d'*32+'.md':'# Andere'})
        with self.assertRaisesRegex(ValueError,'nicht zu diesem Export'):
            ni.select(self.current,other,cmp,[export.pages[0].key],(),raw)
        with self.assertRaisesRegex(ValueError,'Keine freie Kennung'):
            ni.select(self.current,export,cmp,[export.pages[0].key],(),raw,new_id=lambda:'fremd')
        with self.assertRaisesRegex(ValueError,'Keine Seite'):
            ni.select(self.current,export,cmp,[],(),raw)

    def test_current_source_file_changes_missing_bytes_and_limits_are_visible(self):
        import tempfile
        self.numbers=itertools.count();export,raw=self.export()
        result=self.apply(self.select(export,raw),export)
        pages=list(result.lists)
        source=next(p for p in pages if p.get('notion_source')and p['attachments'])
        with tempfile.TemporaryDirectory()as folder:
            path=Path(folder)/'foto.png';path.write_bytes(self.png)
            resolve=lambda _:path
            baseline,assets,issues=ni.current_sources(pages,resolve,max_bytes=1024)
            self.assertEqual(issues,());self.assertEqual(baseline[source['id']],source['notion_source']['local_hash'])
            path.write_bytes(b'Veraendertes Bild')
            changed,assets,issues=ni.current_sources(pages,resolve,max_bytes=1024)
            self.assertNotEqual(changed[source['id']],baseline[source['id']])
            self.assertEqual(issues[0].code,'local-asset-size')
            with self.assertRaisesRegex(ValueError,'Gesamtgrenze'):
                ni.current_sources(pages,resolve,max_bytes=0)
            path.unlink()
            missing,assets,issues=ni.current_sources(pages,resolve,max_bytes=1024)
            self.assertEqual(issues[0].code,'local-asset-missing')
            self.assertNotEqual(missing[source['id']],baseline[source['id']])
            with self.assertRaisesRegex(ValueError,'Dateiprüfgrenze'):
                ni.current_sources(pages,resolve,max_bytes=True)


if __name__=='__main__':unittest.main()
