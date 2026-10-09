"""N04/AU04/G08/G30: echte UI, Formattor, Verweise, Drag, Undo und Neustart."""
import argparse
import copy
from datetime import date,timedelta
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch
from types import SimpleNamespace

REPO=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--app',type=Path,default=REPO/'src/glide/app.pyw')
parser.add_argument('--previous',type=Path)
parser.add_argument('--counterprobe',action='store_true')
parser.add_argument('--report',type=Path)
parser.add_argument('--capture',type=Path)
args=parser.parse_args()
sys.path.insert(0,str(Path(__file__).resolve().parent))
import vorversion
args.previous=vorversion.finden(REPO.parents[1],'3.33.16',REPO/'CHANGELOG.md',args.previous)
checks=[]
observations=[]

with tempfile.TemporaryDirectory(prefix='glide-woche-') as directory:
    os.environ['GLIDE_DATA_DIR']=directory
    os.environ['GLIDE_TEST_MODE']='1'
    original=(REPO/'tests/fixtures/current_v21/reference_v21.json').read_bytes()
    Path(directory,'liste_speicher.json').write_bytes(original)
    loader=importlib.machinery.SourceFileLoader('glide_woche',str(args.app.resolve()))
    mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader))
    sys.modules[loader.name]=mod;loader.exec_module(mod)
    if args.counterprobe:
        available=all(hasattr(mod.ListApp,name) for name in ('object_graph','calendar_plan_selection','calendar_free_slot'))
        result=dict(version=mod.APP_VERSION,exitcode=0 if available else 1,available=available,app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest())
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(result);raise SystemExit(result['exitcode'])
    root=mod.tk.Tk();root.geometry('1280x800+10+10')
    errors=[]
    root.report_callback_exception=lambda *exc:errors.append(repr(exc[1]))
    mod.ListApp.show_info=mod.ListApp.show_warning=lambda *a,**kw:None
    app=mod.ListApp(root)
    app.show_error=lambda *a,**kw:errors.append(str(a))
    def idle():
        for _ in range(3):root.update_idletasks();root.update()
    def stop():
        app.cancel_pending_callbacks();app.release_data_lock()
        for job in root.tk.call('after','info'):root.tk.call('after','cancel',job)
        root.destroy()
    def task(identity):return app.find_item_in_lists(identity)[0]
    def entry(identity):return next(e for e in app.lists if e['id']==identity)
    try:
        assert app.DATA_SCHEMA_VERSION==23
        backups=list(Path(mod.BACKUP_DIR).glob('liste_vor_format22_*.json'))
        assert len(backups)==1 and backups[0].read_bytes()==original
        assert json.loads(Path(mod.SAVE_FILE).read_text(encoding='utf-8'))['version']==23
        checks.append(f'Format 21 → {app.DATA_SCHEMA_VERSION}: bytegenaue Vorsicherung und Startmigration')
        today=date.today();first=app.calendar_week_start(today)
        due=(today+timedelta(days=10)).isoformat()
        a=app.new_item('Kundenangebot prüfen',due=due,estimated_minutes=60)
        b=app.new_item('Rückmeldung einholen',planned_date=first.isoformat(),estimated_minutes=None)
        done=app.new_item('Vorbereitung',done=True,planned_date=first.isoformat(),estimated_minutes=30,planned_time='09:00')
        source=app.new_list_object('Wochenarbeit',[a,b,done])
        page=app.new_list_object('Besprechung',[],list_kind='page')
        app.lists.extend([source,page]);app.settings['daily_capacity_minutes']=120;app.save_items()
        a_id,b_id,source_id,page_id=a['id'],b['id'],source['id'],page['id']
        app.set_active_list(page_id);idle();ed=app.rich_note_editor
        ed.text.focus_force();ed.text.mark_set('insert','1.0')
        count=len(app.undo_stack)
        ed.insert_object_reference(mod.glide_objects.uri('list',source_id));idle()
        assert len(app.undo_stack)==count+1
        assert list(entry(page_id)['rich_note']['links'].values())==[mod.glide_objects.uri('list',source_id)]
        index,outgoing,incoming=app.object_graph()
        assert ('list',page_id) in incoming[('list',source_id)]
        # Native @ key enters the same path; plain email typing does not.
        ed.text.insert('end-1c','\n');ed.text.mark_set('insert','end-1c');ed.text.focus_force();idle()
        with patch.object(app,'themed_choice_dialog',return_value=mod.glide_objects.uri('item',a_id)) as choice:
            ed.text.event_generate('<KeyPress>',keysym='at');idle();assert choice.called
        assert ('item',a_id) in app.object_graph()[1][('list',page_id)]
        ed.text.event_generate('<Control-z>');idle();assert ('item',a_id) not in app.object_graph()[1][('list',page_id)]
        ed.text.event_generate('<Control-y>');idle();assert ('item',a_id) in app.object_graph()[1][('list',page_id)]
        with patch.object(app,'themed_choice_dialog',return_value=None):
            old=copy.deepcopy(app.lists);ed.insert_object_reference();assert app.lists==old
        text=entry(page_id)['rich_note']['text'];assert 'Wochenarbeit' in text
        doc=entry(page_id)['rich_note']
        assert mod.glide_objects.parse(next(iter(doc['links'].values())))
        markdown=mod.glide_page_markdown.page_to_markdown(doc)
        imported=mod.glide_page_markdown.markdown_to_page(markdown)
        assert set(imported['links'].values())==set(doc['links'].values())
        bounds=ed.text.bbox('1.0');assert bounds
        ed.text.event_generate('<Control-Button-1>',x=bounds[0]+2,y=bounds[1]+2);idle()
        assert app.active_list_id==source_id
        app.set_active_list(page_id);idle()
        checks.append('Seiteneditor: Verweis, @-Tastaturweg, Abbruch, Rückverweis, Markdown-Roundtrip, ein Undo-Schritt')
        count=len(app.undo_stack)
        assert app.change_object_reference(('item',a_id),mod.glide_objects.uri('list',page_id))
        assert len(app.undo_stack)==count+1
        app.undo_last_change();idle();assert not task(a_id).get('references')
        assert app.change_object_reference(('item',a_id),mod.glide_objects.uri('list',page_id));idle();assert task(a_id)['references']==[mod.glide_objects.uri('list',page_id)]
        old=copy.deepcopy(app.lists)
        with patch.object(app,'save_items',return_value=False):
            assert not app.change_object_reference(('list',source_id),mod.glide_objects.uri('list',page_id))
        assert app.lists==old
        assert app.change_object_reference(("list",source_id),mod.glide_objects.uri("list",page_id))
        assert any(e.get('kind')=='list' and e.get('action')=='updated' and e.get('target')=='Wochenarbeit' for e in app.history)
        # Fresh graph uses replacement objects after Undo, rename, archive and trash.
        with app.sidebar_change() as change:entry(source_id)['title']='Neuer Wochenplan';change.mark()
        assert 'Neuer Wochenplan' in mod.glide_objects.caption(('item',a_id),app.object_graph()[0])[1]
        app.set_archived('list',source_id,True);idle()
        assert mod.glide_objects.caption(('item',a_id),app.object_graph()[0])[0]=='archived'
        app.set_archived('list',source_id,False);idle()
        with patch.object(app,'ask_yes_no',return_value=True):app.delete_list_by_id(source_id)
        idle();assert mod.glide_objects.caption(('item',a_id),app.object_graph()[0])[0]=='trash'
        menu=app.build_object_reference_menu(('list',page_id))
        link_menu=root.nametowidget(menu.entrycget(next(i for i in range(menu.index('end')+1) if menu.type(i)=='cascade' and menu.entrycget(i,'label').startswith('Verweise (')),'menu'))
        assert all(link_menu.entrycget(i,'state')=='disabled' and 'Papierkorb' in link_menu.entrycget(i,'label') for i in range(link_menu.index('end')+1))
        assert not app.open_object_reference(mod.glide_objects.uri('item',a_id))
        trash_id=next(t['id'] for t in app.trash if (t.get('list') or {}).get('id')==source_id)
        app.set_trash_view();idle();app.tree.selection_set('trash:'+trash_id)
        app.restore_selected_trash_entries();idle()
        assert entry(source_id)['references']==[mod.glide_objects.uri('list',page_id)]
        assert task(a_id)['references']==[mod.glide_objects.uri('list',page_id)]
        app.undo_last_change();idle();assert mod.glide_objects.caption(('item',a_id),app.object_graph()[0])[0]=='trash'
        app.undo_last_change();idle();assert mod.glide_objects.caption(('item',a_id),app.object_graph()[0])[0]=='active' 
        checks.append('IDs und Zustände: Umbenennen, Archiv, Papierkorb, globales Undo und Text-Redo, fehlende Ziele; Speicherfehler ohne Datenänderung')
        copied=copy.deepcopy([entry(source_id),entry(page_id)])
        app.prepare_additive_import(copied,[],[])
        mapping=app._additive_import_maps
        cpage=next(e for e in copied if e['id']==mapping['containers'][page_id])
        assert set(cpage['rich_note']['links'].values())=={mod.glide_objects.uri('list',mapping['containers'][source_id]),mod.glide_objects.uri('item',mapping['items'][a_id])}
        ca=next(i for e in copied for i in app.walk_items(e['items']) if i['id']==mapping['items'][a_id])
        assert ca['references']==[mod.glide_objects.uri('list',mapping['containers'][page_id])]
        app.duplicate_list(source_id);idle()
        duplicate=app.current_list()
        assert duplicate['id']!=source_id and duplicate['references']==entry(source_id)['references']
        assert duplicate['items'][0]['id']!=a_id and duplicate['items'][0]['references']==task(a_id)['references']
        app.undo_last_change();idle();assert len([e for e in app.lists if e['id']==duplicate['id']])==0
        old=copy.deepcopy(app.lists)
        with patch.object(app,'save_items',return_value=False):app.duplicate_list(source_id)
        assert app.lists==old
        checks.append('Additiver Import remappt Seiten-, Listen- und Aufgabenkennungen konsistent')
        before=copy.deepcopy(app.lists);undo_count=len(app.undo_stack)
        for font in ('mittel','gross'):
            app.settings['ui_font_size']=font;app.apply_ui_font()
            for design in ('light','dark'):
                app.set_design(design,apply_now=False);app.apply_theme()
                for width,height in [(1280,800),(860,700)]:
                    root.geometry(f'{width}x{height}+10+10')
                    app._calendar_anchor=today
                    for mode in ('week','month'):
                        app._calendar_mode=mode;started=time.perf_counter();app.open_calendar_view();idle()
                        observations.append(dict(font=font,design=design,width=width,height=height,mode=mode,render_ms=round((time.perf_counter()-started)*1000,2),days=len(app._calendar_day_cells)))
                        assert app.home_mode()=='calendar' and app.view_mode==app.HOME_VIEW
                        assert root.grab_current() is None
                        assert not [w for w in root.winfo_children() if isinstance(w,mod.tk.Toplevel)]
                        assert app._calendar_pool.winfo_reqwidth()<=app.home_content.winfo_width()
                        assert len(app._calendar_day_cells) in (7,28,35,42)
                        for day,summary in app._calendar_summaries.items():
                            self_summary=app.planning_summary([item for e in app.planning_lists() for item in app.walk_items(e['items']) if item.get('planned_date')==day],day=day)
                            assert summary==self_summary
                        if args.capture and font=='gross':
                            sys.path.insert(0,str(REPO/'tests/tools'))
                            from releasedaten import save_windows_screenshot
                            save_windows_screenshot(root,args.capture/f'{mode}-{design}-{width}.png')
        assert app.lists==before and len(app.undo_stack)==undo_count
        checks.append('16 Layouts: Woche/Monat eingebettet, Mindestgröße/große Schrift/hell/dunkel, gleiche Tagesbilanz ohne Mutation')
        root.geometry('1280x800+10+10')
        app._calendar_mode='week';app.open_calendar_view();idle()
        app.home_canvas.yview_moveto(1);idle()
        target=(first+timedelta(days=2)).isoformat()
        app.calendar_choose_day(target)
        pool=app._calendar_pool;pool.selection_set(a_id);pool.focus(a_id)
        pool.see(a_id)
        assert app.current_object_key()==('item',a_id)
        if len(pool.get_children()) > 5:
            before_scroll=app.home_canvas.yview()
            pool.event_generate('<MouseWheel>',delta=-120);idle()
            assert pool.yview()[0] > 0 and app.home_canvas.yview()==before_scroll
            pool.yview_moveto(0)
        root.focus_force();pool.focus_set();idle()
        count=len(app.undo_stack);pool.event_generate('<Return>');idle()
        assert task(a_id)['planned_date']==target and task(a_id)['due']==due
        assert len(app.undo_stack)==count+1
        app.undo_last_change();idle();assert task(a_id)['planned_date'] is None
        assert app.calendar_plan_selection([a_id],target);idle();assert task(a_id)['planned_date']==target
        app.open_calendar_view();idle();app.home_canvas.yview_moveto(1);idle()
        pool=app._calendar_pool;pool.selection_set(a_id);pool.see(a_id);idle()
        box=pool.bbox(a_id);assert box
        before_scroll=app.home_canvas.yview()[0];old=copy.deepcopy(app.lists);count=len(app.undo_stack)
        pool.event_generate('<ButtonPress-1>',x=10,y=box[1]+3);idle()
        canvas=app.home_canvas
        pool.event_generate('<B1-Motion>',x=10,y=box[1]+3,rootx=canvas.winfo_rootx()+40,rooty=canvas.winfo_rooty()+5)
        ready=mod.tk.BooleanVar(value=False);root.after(150,lambda:ready.set(True));root.wait_variable(ready);idle()
        assert app.home_canvas.yview()[0] < before_scroll
        pool.event_generate('<ButtonRelease-1>',x=10,y=box[1]+3,rootx=canvas.winfo_rootx()+40,rooty=canvas.winfo_rooty()-10);idle()
        assert app.lists==old and len(app.undo_stack)==count and app._calendar_drag_job is None
        app.open_calendar_view();idle()
        source_widget=app._calendar_task_widgets[(target,a_id)]
        day=(first+timedelta(days=3)).isoformat();cell=app._calendar_day_cells[day]
        # A real press/move/release sequence on the task label, carrying its stable ID.
        source_widget.event_generate('<ButtonPress-1>',x=5,y=5);idle()
        source_widget.event_generate('<B1-Motion>',x=5,y=5,rootx=cell.winfo_rootx()+10,rooty=cell.winfo_rooty()+10);idle()
        source_widget.event_generate('<ButtonRelease-1>',x=5,y=5,rootx=cell.winfo_rootx()+10,rooty=cell.winfo_rooty()+10);idle()
        assert task(a_id)['planned_date']==day and task(a_id)['due']==due
        old=copy.deepcopy(app.lists)
        with patch.object(app,'save_items',return_value=False):assert not app.calendar_plan_selection([a_id],target)
        assert app.lists==old
        checks.append('Kalender: echter Return- und Dragweg, Randscrollen und Abbruch außerhalb des Inhalts, ausschließlich Bearbeitungstag, ein Undo, Speicherfehler zurückgenommen')
        app.open_calendar_view();idle();app._calendar_pool.selection_set(a_id);app.calendar_choose_day(day)
        with patch.object(app,'themed_choice_dialog',return_value=None):
            old=copy.deepcopy(app.lists);assert not app.calendar_free_slot();assert app.lists==old
        with patch.object(app,'themed_choice_dialog',return_value='08:00'):assert app.calendar_free_slot()
        assert task(a_id)['planned_time']=='08:00' and task(a_id)['due']==due
        app.calendar_open_week_review();idle();assert app.home_mode()=='week_review'
        app.calendar_from_week_review();idle();assert app.home_mode()=='calendar'
        checks.append('Freie Zeitfenster: Abbruch, bestätigte Übernahme, Uhrzeit/Fälligkeit; Verbindung zum Wochenrückblick')
        with patch.object(app,'new_item_dialog',return_value=None):
            old=copy.deepcopy(app.lists);assert not app.calendar_add_task(day);assert app.lists==old
        for due_mode in (False,True):
            details=dict(text='Neue Kalenderaufgabe',list_id=source_id,due=day if due_mode else None,planned_date=None if due_mode else day)
            count=len(app.undo_stack)
            with patch.object(app,'new_item_dialog',return_value=details) as dialog:
                assert app.calendar_add_task(day,due=due_mode)
                assert dialog.call_args.kwargs['default_due']==(day if due_mode else None)
                assert dialog.call_args.kwargs['default_planned']==(None if due_mode else day)
            created=next(i for i in entry(source_id)['items'] if i['text']=='Neue Kalenderaufgabe')
            assert created['due']==details['due'] and created['planned_date']==details['planned_date']
            assert len(app.undo_stack)==count+1
            app.undo_last_change();idle();assert not any(i['text']=='Neue Kalenderaufgabe' for i in entry(source_id)['items'])
        checks.append('Tagesmenü: Anlegen mit Bearbeitungstag oder ausdrücklicher Fälligkeit, Abbruch und je ein Undo')
        assert not errors,errors
        app.save_items();app.save_settings();stored=Path(mod.SAVE_FILE).read_bytes();stop()
        with tempfile.TemporaryDirectory(prefix='glide-format22-failure-') as failure_dir:
            Path(failure_dir,'liste_speicher.json').write_bytes(original)
            failure_script='''import importlib.machinery,importlib.util,sys,pathlib
from unittest.mock import patch
l=importlib.machinery.SourceFileLoader('gate',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));sys.modules[l.name]=m;l.exec_module(m)
m.ListApp.show_error=m.ListApp.show_warning=m.ListApp.show_info=lambda *a,**kw:None
r=m.tk.Tk();r.withdraw();before=pathlib.Path(m.SAVE_FILE).read_bytes()
with patch.object(m.shutil,'copy2',side_effect=OSError('synthetic backup failure')):
 a=m.ListApp(r);assert not a.save_items(show_error=False);assert pathlib.Path(m.SAVE_FILE).read_bytes()==before
a.dirty=False;a.cancel_pending_callbacks();a.release_data_lock();r.destroy()'''
            result=subprocess.run([sys.executable,'-B','-c',failure_script,str(args.app.resolve())],env=dict(os.environ,GLIDE_DATA_DIR=failure_dir),capture_output=True,text=True,timeout=90)
            assert result.returncode==0,(result.stdout,result.stderr)
            checks.append('Format-22-Vorsicherung: Kopierfehler verhindert Überschreiben der alten Datei')
        if args.previous is None:
            checks.append(vorversion.hinweis('3.33.16'))
        if args.previous:
            script="""
import hashlib,importlib.machinery,importlib.util,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.argv[1]).parent.parent if Path(sys.argv[1]).parent.name=='Archiv' else Path(sys.argv[1]).parent))
loader=importlib.machinery.SourceFileLoader('previous',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));loader.exec_module(m)
m.ListApp.show_error=m.ListApp.show_info=m.ListApp.show_warning=lambda *a,**kw:None
p=Path(m.SAVE_FILE);before=p.read_bytes();r=m.tk.Tk();a=m.ListApp(r)
assert a.DATA_SCHEMA_VERSION==21 and a._data_read_only
assert not a.save_items() and p.read_bytes()==before
a.cancel_pending_callbacks();a.release_data_lock();r.destroy()
print('Vorversion Format 21 liest neueres Format schreibgeschützt; unveränderte Bytes')
"""
            result=subprocess.run([sys.executable,'-B','-c',script,str(args.previous.resolve())],capture_output=True,text=True,timeout=90)
            assert result.returncode==0,(result.stdout,result.stderr)
            checks.append(f'Unveränderte 3.33.16: Format {app.DATA_SCHEMA_VERSION} schreibgeschützt, Daten bytegleich')
        root=mod.tk.Tk();app=mod.ListApp(root);idle()
        assert task(a_id)['planned_time']=='08:00' and task(a_id)['due']==due
        assert ('item',a_id) in app.object_graph()[1][('list',page_id)]
        assert task(a_id)['references']==[mod.glide_objects.uri('list',page_id)]
        checks.append('Neustart erhält Planung, Uhrzeit, IDs, ausgehende Verweise und Rückverweise')
        stop()
        result=dict(version=mod.APP_VERSION,format=app.DATA_SCHEMA_VERSION,exitcode=0,checks=checks,
                    app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),observations=observations)
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        print('OK: Wissen und Woche,',len(checks),'gemeinsame Prüfabschnitte')
    finally:
        try:
            if root.winfo_exists():stop()
        except mod.tk.TclError:pass
