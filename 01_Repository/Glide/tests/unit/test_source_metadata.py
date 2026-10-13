import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from notion_reimport import SourceRecord, content_fingerprint
from source_metadata import independent_copy, normalize, records, relocated, restored_source, relocated_collections, staged_source_hashes, selectively_restored


class SourceMetadataTests(unittest.TestCase):
    def page(self, *, identity="page-a", key="notion:"+"a"*32):
        page = {"id":identity,"list_kind":"page","title":"Projekt","items":[],
                "rich_note":{"text":"Ursprung","spans":[],"links":{}},
                "attachments":[{"id":"asset-a","name":"Foto.png","storage":"attachments/alt.png"}]}
        page["notion_source"] = SourceRecord(key, identity, "b"*64,
                content_fingerprint(page,{"asset-a":"c"*64}),"Projekt.md").to_document()
        return page

    def test_normalization_keeps_independent_exact_metadata(self):
        page = self.page()
        actual = normalize(page["notion_source"],page["id"],"page")
        self.assertEqual(actual,page["notion_source"])
        actual["source_path"] = "anders.md"
        self.assertEqual(page["notion_source"]["source_path"],"Projekt.md")
        self.assertIsNone(normalize(None,"page-a","tasks"))

    def test_wrong_owner_kind_and_unsafe_paths_are_rejected(self):
        page=self.page()
        for identity,kind in (("andere-id","page"),("page-a","tasks")):
            with self.assertRaises(ValueError):normalize(page["notion_source"],identity,kind)
        for path in ("../Projekt.md","/Projekt.md","C:/Projekt.md","a\\Projekt.md","a\n.md"):
            value=dict(page["notion_source"],source_path=path)
            with self.assertRaises(ValueError):normalize(value,"page-a","page")

    def test_duplicate_sources_or_targets_are_rejected(self):
        first=self.page()
        for second in (self.page(identity="page-b"),self.page(key="notion:"+"d"*32)):
            with self.assertRaises(ValueError):records([first,second])
        self.assertEqual(len(records([first,{"id":"tasks","list_kind":"tasks"}])),1)

    def test_independent_copy_clears_only_source_mapping(self):
        original=self.page();before=copy.deepcopy(original)
        duplicate=independent_copy(original)
        self.assertNotIn("notion_source",duplicate)
        self.assertEqual(original,before)
        self.assertEqual(duplicate,{k:v for k,v in original.items()if k!="notion_source"})
        duplicate["rich_note"]["text"]="anders"
        self.assertEqual(original["rich_note"]["text"],"Ursprung")

    def test_clean_relocation_reanchors_hash_without_changing_source(self):
        original=self.page();before=copy.deepcopy(original);after=copy.deepcopy(original)
        after["attachments"][0]["storage"]="attachments/neu.png"
        actual=relocated(original,after,{"asset-a":"c"*64},{"asset-a":"c"*64})
        self.assertEqual(actual["notion_source"]["local_hash"],content_fingerprint(actual,{"asset-a":"c"*64}))
        self.assertEqual(actual["notion_source"]["source_hash"],"b"*64)
        self.assertEqual(original,before)
        self.assertEqual(after["notion_source"],original["notion_source"])

    def test_local_edits_are_not_marked_as_clean_by_relocation(self):
        original=self.page();original["rich_note"]["text"]="Eigene Bearbeitung"
        after=copy.deepcopy(original);after["attachments"][0]["storage"]="attachments/neu.png"
        actual=relocated(original,after,{"asset-a":"c"*64},{"asset-a":"c"*64})
        self.assertEqual(actual["notion_source"]["local_hash"],original["notion_source"]["local_hash"])
        self.assertNotEqual(actual["notion_source"]["local_hash"],content_fingerprint(actual,{"asset-a":"c"*64}))

    def test_changed_page_text_cannot_be_reanchored_as_a_relocation(self):
        page=self.page();after=copy.deepcopy(page);after["rich_note"]["text"]="Ungeprüfte Änderung"
        with self.assertRaisesRegex(ValueError,"Seiteninhalt"):
            relocated(page,after,{"asset-a":"c"*64},{"asset-a":"c"*64})

    def test_changed_asset_bytes_cannot_be_reanchored_as_a_relocation(self):
        page=self.page();after=copy.deepcopy(page);after["attachments"][0]["storage"]="attachments/neu.png"
        with self.assertRaisesRegex(ValueError,"Anhangsbytes"):
            relocated(page,after,{"asset-a":"c"*64},{"asset-a":"d"*64})

    def test_real_restore_changes_attachment_ids_and_image_targets(self):
        page=self.page()
        page["rich_note"]["images"]={"image-1":{"attachment":"asset-a"}}
        page["cover"]={"kind":"image","attachment":"asset-a"}
        page["notion_source"]["local_hash"]=content_fingerprint(page,{"asset-a":"c"*64})
        after=copy.deepcopy(page)
        after["attachments"][0].update(id="asset-new",storage="attachments/neu.png")
        after["rich_note"]["images"]["image-1"]["attachment"]="asset-new"
        after["cover"]["attachment"]="asset-new"
        actual=relocated(page,after,{"asset-a":"c"*64},{"asset-new":"c"*64})
        self.assertEqual(actual["notion_source"]["local_hash"],content_fingerprint(actual,{"asset-new":"c"*64}))
        self.assertEqual(actual["cover"]["attachment"],"asset-new")

    def test_task_attachments_are_hashed_and_relocated_too(self):
        page=self.page()
        page["items"]=[{"id":"task-a","text":"Unterpunkt","children":[],"attachments":[{"id":"asset-task","name":"Datei.pdf","storage":"attachments/alt.pdf"}]}]
        old_hashes={"asset-a":"c"*64,"asset-task":"d"*64}
        clean=content_fingerprint(page,old_hashes)
        self.assertNotEqual(clean,content_fingerprint(page,dict(old_hashes,**{"asset-task":"e"*64})))
        page["notion_source"]["local_hash"]=clean
        after=copy.deepcopy(page);after["items"][0]["attachments"][0].update(id="asset-task-new",storage="attachments/neu.pdf")
        new_hashes={"asset-a":"c"*64,"asset-task-new":"d"*64}
        actual=relocated(page,after,old_hashes,new_hashes)
        self.assertEqual(actual["notion_source"]["local_hash"],content_fingerprint(actual,new_hashes))

    def test_incomplete_hashes_or_changed_identity_are_rejected(self):
        page=self.page()
        with self.assertRaises(ValueError):relocated(page,page,{}, {})
        with self.assertRaises(ValueError):relocated(page,dict(page,id="andere-id"),{"asset-a":"c"*64},{"asset-a":"c"*64})

    def test_trash_return_keeps_baseline_and_can_retarget_a_colliding_identity(self):
        page=self.page();before=copy.deepcopy(page)
        result=restored_source(page,'freie-id',[])
        self.assertEqual(result['target_id'],'freie-id')
        self.assertEqual(result['local_hash'],page['notion_source']['local_hash'])
        self.assertEqual(page,before)

    def test_trash_return_does_not_duplicate_a_live_source(self):
        page=self.page();live=self.page(identity='lebende-seite')
        self.assertIsNone(restored_source(page,'zurueck', [live]))
        unrelated=self.page(identity='andere',key='notion:'+'d'*32)
        self.assertEqual(restored_source(page,'zurueck',[unrelated])['key'],page['notion_source']['key'])

    def test_trash_return_preserves_local_edits_as_a_conflict(self):
        page=self.page();baseline=page['notion_source']['local_hash']
        page['rich_note']['text']='Eigene Bearbeitung';page['folder_id']='verschoben'
        result=restored_source(page,page['id'],[])
        self.assertEqual(result['local_hash'],baseline)
        self.assertNotEqual(content_fingerprint(page,{'asset-a':'c'*64}),result['local_hash'])

    def test_full_restore_reanchors_live_and_trashed_source_pages_only(self):
        page=self.page();trashed=self.page(identity='papierkorb',key='notion:'+'e'*32)
        before=([page,{'id':'andere','title':'Unverändert'}],[{'kind':'list','list':trashed}])
        after=copy.deepcopy(before)
        for target in (after[0][0],after[1][0]['list']):
            target['attachments'][0].update(id='asset-neu',storage='attachments/neu.png')
        snapshot=copy.deepcopy((before,after))
        actual=relocated_collections(before,after,{'attachments/alt.png':'c'*64},{'attachments/neu.png':'c'*64})
        self.assertEqual((before,after),snapshot)
        self.assertEqual(actual[0][1],before[0][1])
        for target in (actual[0][0],actual[1][0]['list']):
            self.assertEqual(target['notion_source']['local_hash'],content_fingerprint(target,{'asset-neu':'c'*64}))

    def test_full_restore_keeps_local_changes_dirty(self):
        page=self.page();baseline=page['notion_source']['local_hash'];page['note']='Eigene Ergänzung'
        after=copy.deepcopy(page);after['attachments'][0].update(id='asset-neu',storage='attachments/neu.png')
        actual=relocated_collections(([page],[]),([after],[]),{'attachments/alt.png':'c'*64},{'attachments/neu.png':'c'*64})
        self.assertEqual(actual[0][0]['notion_source']['local_hash'],baseline)

    def test_full_restore_rejects_missing_or_changed_file_bytes(self):
        page=self.page();after=copy.deepcopy(page);after['attachments'][0].update(id='asset-neu',storage='attachments/neu.png')
        for hashes in ({},{'attachments/neu.png':'d'*64}):
            with self.subTest(hashes=hashes),self.assertRaises(ValueError):
                relocated_collections(([page],[]),([after],[]),{'attachments/alt.png':'c'*64},hashes)

    def test_staged_source_hashes_include_task_assets_and_ignore_other_pages(self):
        page=self.page();page['items']=[{'attachments':[{'id':'aufgabe','storage':'attachments/task.pdf'}]}]
        with tempfile.TemporaryDirectory() as directory:
            a,b=Path(directory)/'foto',Path(directory)/'aufgabe';a.write_bytes(b'foto');b.write_bytes(b'task')
            files={'attachments/alt.png':a,'attachments/task.pdf':b,'attachments/irrelevant.pdf':Path(directory)/'fehlt'}
            other={'id':'andere','attachments':[{'storage':'attachments/irrelevant.pdf'}]}
            result=staged_source_hashes(([page,other],[]),files,max_bytes=8)
            self.assertEqual(result,{'attachments/alt.png':hashlib.sha256(b'foto').hexdigest(),
                                    'attachments/task.pdf':hashlib.sha256(b'task').hexdigest()})
            with self.assertRaisesRegex(ValueError,'Gesamtgrenze'):
                staged_source_hashes(([page],[]),files,max_bytes=7)

    def test_staged_source_hashes_reject_missing_files_and_invalid_limits(self):
        with self.assertRaisesRegex(ValueError,'Zwischenstand'):
            staged_source_hashes(([self.page()],[]),{},max_bytes=4)
        for limit in (-1,True):
            with self.subTest(limit=limit),self.assertRaisesRegex(ValueError,'Dateiprüfgrenze'):
                staged_source_hashes(([],[]),{},max_bytes=limit)


    def test_selective_restore_reanchors_clean_technical_task_and_file_ids(self):
        page=self.page();page['items']=[{'id':'task-old','text':'Aufgabe','links':['task-old'],
                                      'blocked_by':['task-old']}]
        page['notion_source']['local_hash']=content_fingerprint(page,{'asset-a':'c'*64})
        before=copy.deepcopy(page);after=copy.deepcopy(page)
        after['items'][0].update(id='task-new',links=['task-new'],blocked_by=['task-new'])
        after['attachments'][0].update(id='asset-new',storage='attachments/neues.png')
        actual=selectively_restored(page,after,{'asset-a':'c'*64},{'asset-new':'c'*64},[page],
                                   [('task-old','task-new')])
        self.assertEqual(actual['notion_source']['local_hash'],content_fingerprint(actual,{'asset-new':'c'*64}))
        self.assertEqual(actual['items'][0]['id'],'task-new');self.assertEqual(page,before)
        self.assertEqual(after['notion_source'],page['notion_source'])

    def test_selective_restore_keeps_saved_local_edits_as_conflicts(self):
        page=self.page();page['rich_note']['text']='Eigener Stand in der Sicherung'
        after=copy.deepcopy(page);after['attachments'][0]['storage']='attachments/neu.png'
        actual=selectively_restored(page,after,{'asset-a':'c'*64},{'asset-a':'c'*64},[])
        self.assertEqual(actual['notion_source']['local_hash'],page['notion_source']['local_hash'])
        self.assertNotEqual(actual['notion_source']['local_hash'],content_fingerprint(actual,{'asset-a':'c'*64}))

    def test_selective_restore_keeps_changed_current_folder_as_local_edit(self):
        page=self.page();page['folder_id']='frueher'
        page['notion_source']['local_hash']=content_fingerprint(page,{'asset-a':'c'*64})
        after=copy.deepcopy(page);after['folder_id']='heute'
        actual=selectively_restored(page,after,{'asset-a':'c'*64},{'asset-a':'c'*64},[])
        self.assertEqual(actual['folder_id'],'heute')
        self.assertEqual(actual['notion_source']['local_hash'],page['notion_source']['local_hash'])

    def test_selective_restore_does_not_duplicate_a_live_source_binding(self):
        page=self.page();other=self.page(identity='andere-seite')
        actual=selectively_restored(page,page,{'asset-a':'c'*64},{'asset-a':'c'*64},[other])
        self.assertNotIn('notion_source',actual);self.assertIn('notion_source',other)

    def test_selective_restore_rejects_unplanned_content_or_asset_changes(self):
        page=self.page();after=copy.deepcopy(page);after['rich_note']['text']='Nicht aus der Sicherung'
        with self.assertRaisesRegex(ValueError,'Seiteninhalt'):
            selectively_restored(page,after,{'asset-a':'c'*64},{'asset-a':'c'*64},[])
        with self.assertRaisesRegex(ValueError,'Anhangsbytes'):
            selectively_restored(page,page,{'asset-a':'c'*64},{'asset-a':'d'*64},[])
        with self.assertRaisesRegex(ValueError,'eindeutig'):
            selectively_restored(page,page,{'asset-a':'c'*64},{'asset-a':'c'*64},[],[('a','b'),('c','b')])


if __name__=="__main__":unittest.main()
