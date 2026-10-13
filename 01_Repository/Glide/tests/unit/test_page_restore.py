import copy
import itertools
import unittest
from page_restore import prepare, with_attachments, validate


def task(identity, children=()):
    return dict(id=identity,text=identity,children=list(children),done=False,labels=[],attachments=[])


def page(identity="page", items=()):
    return dict(id=identity,title="Seite",list_kind="page",items=list(items),folder_id=None,
                rich_note=dict(text="Text",spans=[],links={},images={}),attachments=[],labels=[])


def data(*pages, trash=(), labels=(), folders=()):
    return dict(lists=list(pages),trash=list(trash),labels=list(labels),folders=list(folders))


def deleted(kind, payload, identity="trash", origin=None):
    value=dict(id=identity,kind=kind,deleted_at="2026-10-09T12:00:00",list=None,folder=None,item=None,
               origin_folder_id=None,origin_folder_title="",origin=origin)
    value[kind]=payload
    return value


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.ids = (f"new-{n}" for n in itertools.count())

    def plan(self, current, backup, assets=(), **kwargs):
        return prepare(current,backup,"page",assets,new_id=lambda:next(self.ids),**kwargs)

    def test_only_chosen_page_and_its_current_folder_are_restored(self):
        current=data(page(items=[task("owned")]),page("other"),folders=[dict(id="folder")])
        current["lists"][0]["title"]="Heute"
        current["lists"][0]["folder_id"]="folder"
        backup=data(page(items=[task("owned")]),page("other"))
        backup["lists"][0]["title"]="Gestern"
        originals=copy.deepcopy((current,backup))
        plan=self.plan(current,backup)
        self.assertEqual(plan.page["title"],"Gestern")
        self.assertEqual(plan.page["folder_id"],"folder")
        self.assertTrue(validate(plan,current))
        self.assertEqual((current,backup),originals)
        self.assertTrue(plan.warnings)
        plan.page["items"][0]["text"]="Entwurf"
        self.assertEqual(backup["lists"][0]["items"][0]["text"],"owned")

    def test_current_unrestored_children_are_preserved_in_trash(self):
        current=data(page(items=[task("kept",[task("new-child")]),task("new-root")]))
        plan=self.plan(current,data(page(items=[task("kept")])))
        self.assertEqual([entry["item"]["id"] for entry in plan.trash],["new-child","new-root"])
        self.assertTrue(all(entry["origin"]["list_id"]=="page" for entry in plan.trash))
        with self.assertRaisesRegex(ValueError,"Papierkorb"):
            self.plan(current,data(page(items=[task("kept")])),max_trash=1)

    def test_deleted_task_returns_without_losing_its_later_children(self):
        own=deleted("item",task("owned",[task("later-child")]),origin=dict(list_id="page",list_title="Seite"))
        foreign=deleted("item",task("foreign"),identity="foreign-trash",origin=dict(list_id="other"))
        current=data(page(),trash=[own,foreign])
        plan=self.plan(current,data(page(items=[task("owned")])))
        self.assertEqual(plan.remapped_items,())
        self.assertEqual(plan.trash[0]["item"]["id"],"later-child")
        self.assertEqual(plan.trash[0]["deleted_at"],own["deleted_at"])
        self.assertEqual(plan.trash[1],foreign)

    def test_deleted_page_and_nested_folder_restore_keep_unselected_content(self):
        restored=page(items=[task("owned"),task("later")])
        current=data(trash=[deleted("list",restored)])
        plan=self.plan(current,data(page(items=[task("owned")])))
        self.assertEqual([entry["item"]["id"] for entry in plan.trash],["later"])
        folder=dict(id="folder",title="Ordner",lists=[restored,page("other")])
        current=data(trash=[deleted("folder",folder)])
        plan=self.plan(current,data(page(items=[task("owned")])))
        self.assertEqual(plan.trash[0]["item"]["id"],"later")
        self.assertEqual(plan.trash[1]["folder"]["lists"],[folder["lists"][1]])
        self.assertEqual(current["trash"][0]["folder"],folder)

    def test_moved_or_foreign_deleted_task_gets_fresh_id_and_all_internal_links_follow(self):
        saved=page(items=[task("moved"),task("dependent")])
        saved["items"][1].update(links=["moved"],blocked_by=["moved"],references=["glide://item/moved"])
        saved["rich_note"].update(text="Aufgabe",spans=[dict(tag="item:moved",start=0,end=7),
            dict(tag="taskref:moved",start=0,end=7),dict(tag="link:x",start=0,end=7)],links={"link:x":"glide://item/moved"})
        for current in (data(page(),page("other",[task("moved")])),
                        data(page(),trash=[deleted("item",task("moved"),origin=dict(list_id="other"))])):
            plan=self.plan(current,data(saved))
            old,new=plan.remapped_items[0]
            self.assertEqual(old,"moved")
            self.assertNotEqual(new,old)
            self.assertEqual(plan.page["items"][1]["links"],[new])
            self.assertEqual(plan.page["items"][1]["blocked_by"],[new])
            self.assertEqual(plan.page["items"][1]["references"],["glide://item/"+new])
            self.assertEqual(plan.page["rich_note"]["spans"][0]["tag"],"item:"+new)
            self.assertEqual(plan.page["rich_note"]["spans"][1]["tag"],"taskref:"+new)
            self.assertEqual(plan.page["rich_note"]["links"]["link:x"],"glide://item/"+new)

    def test_missing_archived_and_deleted_external_targets_are_reported(self):
        saved=page(items=[task("owned")]);saved["items"][0]["blocked_by"]=["gone"]
        saved["rich_note"].update(text="Verweis",spans=[dict(tag="taskref:deleted",start=0,end=7)])
        saved.update(live_lists=["glide://list/archive"],references=["glide://list/missing"])
        archive=page("archive");archive["archived"]=True
        current=data(page(),archive,trash=[deleted("item",task("deleted"),origin=dict(list_id="other"))])
        plan=self.plan(current,data(saved))
        self.assertEqual(set(plan.missing_targets),{("list","archive","archived"),("list","missing","missing"),
            ("item","gone","missing"),("item","deleted","trash")})
        self.assertTrue(plan.ready)

    def test_labels_are_added_only_when_used_existing_definitions_stay(self):
        saved=page(items=[task("owned")]);saved["labels"]=["a"];saved["items"][0]["labels"]=["b"]
        a=dict(id="a",title="Alt");b=dict(id="b",title="Neu");unused=dict(id="unused",title="Unbenutzt")
        current=data(page(),labels=[dict(a,title="Heute")]);backup=data(saved,labels=[a,b,unused])
        plan=self.plan(current,backup)
        self.assertEqual(plan.added_labels,(b,));self.assertTrue(plan.warnings)
        with self.assertRaisesRegex(ValueError,"Labelgrenze"):
            self.plan(current,backup,max_labels=1)
        with self.assertRaisesRegex(ValueError,"Labeldefinition"):
            self.plan(current,data(saved))

    def test_images_cover_and_task_attachments_need_files_and_fresh_storage(self):
        asset=dict(id="old",name="Foto.png",storage="attachments/old.png",size=3,mime="image/png")
        saved=page(items=[task("owned")]);saved["items"][0]["attachments"]=[asset]
        saved["rich_note"]["images"]={"img:a":dict(attachment="old",mode="left",width=200)}
        saved["cover"]=dict(kind="image",attachment="old")
        current=data(page())
        blocked=self.plan(current,data(saved))
        self.assertFalse(blocked.ready);self.assertEqual(blocked.missing_files,("old",))
        with self.assertRaises(ValueError):validate(blocked,current)
        plan=self.plan(current,data(saved),[asset["storage"]])
        with self.assertRaisesRegex(ValueError,"neu abgelegt"):validate(plan,current)
        new=dict(asset,id="fresh",storage="attachments/fresh.png")
        staged=with_attachments(plan,{"old":new})
        self.assertTrue(validate(staged,current))
        self.assertEqual(staged.page["cover"]["attachment"],"fresh")
        self.assertEqual(staged.page["rich_note"]["images"]["img:a"]["attachment"],"fresh")
        self.assertEqual(staged.page["items"][0]["attachments"],[new])
        self.assertEqual(plan.page["cover"]["attachment"],"old")
        for replacement in ({}, {"old":asset}, {"old":dict(new,size=4)},
                            {"old":dict(new,storage="attachments/../old.png")},
                            {"old":dict(new,storage="attachments/old.png")}):
            with self.assertRaises(ValueError):with_attachments(plan,replacement)
        with self.assertRaises(ValueError):with_attachments(staged,{"old":new})

    def test_foreign_current_attachment_cannot_be_overwritten(self):
        asset=dict(id="old",name="Foto.png",storage="attachments/old.png",size=3)
        saved=page();saved["attachments"]=[asset]
        other=page("other");other["attachments"]=[dict(asset,id="foreign",storage="attachments/foreign.png")]
        current=data(page(),other);plan=self.plan(current,data(saved),[asset["storage"]])
        for replacement in (dict(asset,id="foreign",storage="attachments/fresh.png"),
                            dict(asset,id="fresh",storage="attachments/foreign.png")):
            with self.assertRaises(ValueError):with_attachments(plan,{"old":replacement})

    def test_staged_attachments_keep_metadata_and_portable_fresh_ids(self):
        asset=dict(id="old",name="Bild.png",storage="attachments/old.png",size=1,
                   mime="image/png",title="Titel",note="Notiz")
        saved=page();saved["attachments"]=[asset]
        plan=self.plan(data(page()),data(saved),[asset["storage"]])
        fresh=dict(asset,id="fresh",storage="attachments/fresh.png")
        for identity in (None, [], {}, True, "ä", "a"*65, "bad/path"):
            with self.subTest(identity=identity), self.assertRaises(ValueError):
                with_attachments(plan,{"old":dict(fresh,id=identity)})
        for field,value in (("size",True),("name","Andere.png"),("mime","text/plain"),
                            ("title","Anderer Titel"),("note","Andere Notiz")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                with_attachments(plan,{"old":dict(fresh,**{field:value})})
        self.assertTrue(with_attachments(plan,{"old":fresh}).staged)

    def test_storage_collisions_are_portable_across_case_and_unicode(self):
        asset=dict(id="old",name="Bild",storage="attachments/old.png",size=1)
        saved=page();saved["attachments"]=[asset]
        other=page("other");other["attachments"]=[dict(asset,id="foreign",storage="attachments/Café.png")]
        plan=self.plan(data(page(),other),data(saved),[asset["storage"]])
        for storage in ("attachments/café.PNG","attachments/Cafe\u0301.png","attachments/OLD.png",
                        "attachments/new.","attachments/new ","attachments/NUL.png","attachments/new:stream"):
            with self.subTest(storage=storage), self.assertRaises(ValueError):
                with_attachments(plan,{"old":dict(asset,id="fresh",storage=storage)})

    def test_missing_metadata_blocks_and_ambiguous_attachment_metadata_rejects(self):
        saved=page();saved["rich_note"]["images"]={"img:a":dict(attachment="missing")}
        self.assertEqual(self.plan(data(page()),data(saved)).missing_files,("missing",))
        saved=page(items=[task("owned")]);saved["attachments"]=[dict(id="a",storage="attachments/a",size=1)]
        saved["items"][0]["attachments"]=[dict(id="a",storage="attachments/b",size=1)]
        with self.assertRaisesRegex(ValueError,"mehrdeutig"):self.plan(data(page()),data(saved))

    def test_changed_current_state_blocks_stale_preview(self):
        current=data(page(),page("other"));plan=self.plan(current,data(page()))
        changed=copy.deepcopy(current);changed["lists"][1]["title"]="Anderer Stand"
        with self.assertRaisesRegex(ValueError,"geändert"):validate(plan,changed)

    def test_target_kind_ambiguity_and_unusable_id_factory_are_rejected(self):
        with self.assertRaises(ValueError):self.plan(data(dict(page(),list_kind="tasks")),data(page()))
        with self.assertRaises(ValueError):self.plan(data(page()),data(page(),page()))
        with self.assertRaises(ValueError):self.plan(data(page()),data(page(items=[task("x"),task("x")])))
        with self.assertRaises(ValueError):prepare(data(page(),page("other",[task("moved")])),
            data(page(items=[task("moved")])),"page",(),new_id=lambda:"moved")


if __name__=="__main__":unittest.main()
